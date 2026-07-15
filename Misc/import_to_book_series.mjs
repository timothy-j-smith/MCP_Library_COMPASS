#!/usr/bin/env node
// Apply a Book Series MCP import bundle (produced by
// convert_synopsis_outline_to_book_series.py) to a running Book Series MCP
// (https://github.com/RLRyals/book-series-mcp) instance.
//
// This is a minimal, dependency-free MCP client: it spawns the relevant MCP
// server processes and speaks newline-delimited JSON-RPC 2.0 over stdio, so it
// needs nothing beyond the Node standard library.
//
// Usage:
//   BOOK_SERIES_MCP_HOME=/path/to/book-series-mcp \
//   DATABASE_URL=postgresql://writer:...@localhost:5432/book_series \
//   node import_to_book_series.mjs bundle.json
//
// The bundle's steps reference two servers: "manager" (src/index.js) and
// "writing" (src/writing-server/index.js). Steps may declare a `capture`
// (e.g. "series_id" / "book_id"); captured ids replace `$series_id` /
// `$book_id` placeholders in later steps.

import { spawn } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { createInterface } from 'node:readline';
import path from 'node:path';

const SERVER_ENTRYPOINTS = {
  manager: 'src/index.js',
  writing: 'src/writing-server/index.js',
  plot: 'src/plot-server/index.js',
  character: 'src/character-server/index.js',
};

// Dedupe rules per create-tool: before creating, list existing records with
// `listTool` and skip when a record already matches on `field`. This makes the
// import idempotent and avoids duplicate characters/plot threads/books when the
// same synopsis is imported more than once. `create_series` degrades gracefully
// if its list tool is unavailable (e.g. the upstream `series_overview` view is
// missing) — in that case a new series is created.
const DEDUPE_RULES = {
  create_series: { server: 'manager', listTool: 'get_series_overview', listArgs: () => ({}), field: 'name' },
  create_series_book: { server: 'manager', listTool: 'get_series_books', listArgs: (a) => ({ series_id: a.series_id }), field: 'book_number', numeric: true },
  create_series_character: { server: 'manager', listTool: 'get_series_characters', listArgs: (a) => ({ series_id: a.series_id }), field: 'name' },
  create_series_plot_thread: { server: 'manager', listTool: 'get_series_plot_threads', listArgs: (a) => ({ series_id: a.series_id }), field: 'title' },
};

const norm = (v) => String(v ?? '').trim().toLowerCase();

class McpStdioClient {
  constructor(entryPath, env) {
    this.proc = spawn('node', [entryPath], {
      env,
      stdio: ['pipe', 'pipe', 'inherit'],
    });
    this.nextId = 1;
    this.pending = new Map();
    const rl = createInterface({ input: this.proc.stdout });
    rl.on('line', (line) => {
      const trimmed = line.trim();
      if (!trimmed.startsWith('{')) return; // ignore stray non-JSON output
      let msg;
      try { msg = JSON.parse(trimmed); } catch { return; }
      if (msg.id !== undefined && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        if (msg.error) reject(new Error(JSON.stringify(msg.error)));
        else resolve(msg.result);
      }
    });
  }

  _send(msg) {
    this.proc.stdin.write(JSON.stringify(msg) + '\n');
  }

  request(method, params) {
    const id = this.nextId++;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this._send({ jsonrpc: '2.0', id, method, params });
      setTimeout(() => {
        if (this.pending.has(id)) {
          this.pending.delete(id);
          reject(new Error(`Timeout waiting for ${method}`));
        }
      }, 20000);
    });
  }

  async handshake() {
    await this.request('initialize', {
      protocolVersion: '2024-11-05',
      capabilities: {},
      clientInfo: { name: 'compass-importer', version: '1.0.0' },
    });
    this._send({ jsonrpc: '2.0', method: 'notifications/initialized' });
  }

  callTool(name, args) {
    return this.request('tools/call', { name, arguments: args });
  }

  close() {
    try { this.proc.stdin.end(); } catch { /* ignore */ }
    this.proc.kill('SIGTERM');
  }
}

function textOf(result) {
  if (!result || !Array.isArray(result.content)) return '';
  return result.content.map((c) => c.text || '').join('\n');
}

function deepFindId(obj) {
  if (obj == null || typeof obj !== 'object') return undefined;
  for (const key of ['id', 'book_id', 'series_id']) {
    if (typeof obj[key] === 'number') return obj[key];
  }
  for (const v of Object.values(obj)) {
    const found = deepFindId(v);
    if (found !== undefined) return found;
  }
  return undefined;
}

function extractId(result) {
  const text = textOf(result);
  try {
    const parsed = JSON.parse(text);
    const id = deepFindId(parsed);
    if (id !== undefined) return id;
  } catch { /* not JSON, fall through */ }
  const m = text.match(/with ID (\d+)/i);
  return m ? parseInt(m[1], 10) : undefined;
}

function substitute(value, captures) {
  if (typeof value === 'string' && value.startsWith('$')) {
    const key = value.slice(1);
    if (captures[key] === undefined) throw new Error(`Unresolved placeholder ${value}`);
    return captures[key];
  }
  if (Array.isArray(value)) return value.map((v) => substitute(v, captures));
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.entries(value).map(([k, v]) => [k, substitute(v, captures)]));
  }
  return value;
}

async function findExisting(client, rule, args, captures) {
  const listArgs = substitute(rule.listArgs(args), captures);
  const result = await client.callTool(rule.listTool, listArgs);
  if (result && result.isError) return undefined; // list tool unavailable
  let rows;
  try { rows = JSON.parse(textOf(result)); } catch { return undefined; }
  if (!Array.isArray(rows)) return undefined;
  const want = args[rule.field];
  const match = rows.find((r) => (rule.numeric
    ? Number(r[rule.field]) === Number(want)
    : norm(r[rule.field]) === norm(want)));
  return match && match.id !== undefined ? match.id : undefined;
}

async function main() {
  const flags = new Set(process.argv.filter((a) => a.startsWith('--')));
  const positional = process.argv.slice(2).filter((a) => !a.startsWith('--'));
  const dedupe = !flags.has('--no-dedupe');
  const bundlePath = positional[0];
  if (!bundlePath) {
    console.error('Usage: node import_to_book_series.mjs [--no-dedupe] <bundle.json>');
    process.exit(2);
  }
  const home = process.env.BOOK_SERIES_MCP_HOME || positional[1];
  if (!home) {
    console.error('Set BOOK_SERIES_MCP_HOME (or pass it as arg 2) to the book-series-mcp checkout.');
    process.exit(2);
  }
  if (!process.env.DATABASE_URL) {
    console.error('Set DATABASE_URL to the Book Series MCP PostgreSQL connection string.');
    process.exit(2);
  }

  const bundle = JSON.parse(readFileSync(bundlePath, 'utf-8'));
  const env = { ...process.env, NODE_ENV: process.env.NODE_ENV || 'development', MCP_SERVER_MODE: '1' };

  const clients = {};
  const getClient = async (server) => {
    if (clients[server]) return clients[server];
    const entry = SERVER_ENTRYPOINTS[server];
    if (!entry) throw new Error(`Unknown server "${server}"`);
    const client = new McpStdioClient(path.join(home, entry), env);
    await client.handshake();
    clients[server] = client;
    return client;
  };

  const captures = {};
  let stepNum = 0;
  try {
    for (const step of bundle.steps) {
      stepNum += 1;
      const client = await getClient(step.server);
      const args = substitute(step.arguments, captures);

      const rule = dedupe ? DEDUPE_RULES[step.tool] : undefined;
      if (rule) {
        const existingId = await findExisting(await getClient(rule.server), rule, args, captures);
        if (existingId !== undefined) {
          let note = '';
          if (step.capture) { captures[step.capture] = existingId; note = ` -> ${step.capture}=${existingId}`; }
          console.log(`[${stepNum}/${bundle.steps.length}] ${step.server}:${step.tool} skipped (exists id=${existingId})${note}`);
          continue;
        }
      }

      const result = await client.callTool(step.tool, args);
      if (result && result.isError) {
        throw new Error(`Tool ${step.tool} failed: ${textOf(result)}`);
      }
      let note = '';
      if (step.capture) {
        const id = extractId(result);
        if (id === undefined) throw new Error(`Could not capture ${step.capture} from ${step.tool}`);
        captures[step.capture] = id;
        note = ` -> ${step.capture}=${id}`;
      }
      console.log(`[${stepNum}/${bundle.steps.length}] ${step.server}:${step.tool} ok${note}`);
    }
    console.log(`\n✅ Imported "${bundle.meta?.title}" (${bundle.meta?.chapter_count} chapters, ${bundle.meta?.theme_count} themes)`);
    if (captures.series_id !== undefined) console.log(`   series_id=${captures.series_id}`);
    if (captures.book_id !== undefined) console.log(`   book_id=${captures.book_id}`);
  } finally {
    for (const c of Object.values(clients)) c.close();
  }
}

main().then(() => process.exit(0)).catch((e) => { console.error('❌', e.message); process.exit(1); });
