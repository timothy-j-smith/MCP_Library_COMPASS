# Book Series MCP — Enable + Convert Synopsis/Outline

**Purpose:** How to enable the **Book Series MCP** server suite and convert a
COMPASS Story Bible (`synopsis.md` + `outline.md`) into it.

**Upstream project:** [RLRyals/book-series-mcp](https://github.com/RLRyals/book-series-mcp)

> **Correction to older notes:** Several files in this repo
> (`MCP_Setup/MCP_API_KEYS_AND_SETUP_REFERENCE.md`,
> `MCP_Research/*`) describe `book-series` as *"Python + PostgreSQL,
> `pip install book-series-mcp`, `POSTGRES_URI`"*. That is inaccurate. The
> real project is **Node.js (v16+) + PostgreSQL**, installed by cloning the repo
> and running `npm install`, and it reads **`DATABASE_URL`** (not `POSTGRES_URI`).
> This document is the authoritative setup reference.

---

## 1. What it is

Book Series MCP is a suite of MCP servers backed by a single PostgreSQL
database. The two servers used by the conversion workflow are:

| Server | Entry point | Relevant tools |
|--------|-------------|----------------|
| `book-series-manager` | `src/index.js` | `create_series`, `create_series_book`, `create_series_plot_thread`, `get_series_*` |
| `writing-production` | `src/writing-server/index.js` | `bulk_chapter_operations` (`create_outline_batch`), `get_chapters`, `create_chapter`, ... |

Other servers (`character`, `plot`, `world`, `research`, `elevenlabs-persona`)
share the same database and are configured the same way.

## 2. Enable it (install + database)

Prerequisites: **Node.js v16+** and **PostgreSQL v12+** (or Docker).

```bash
# 1. Clone + install
git clone https://github.com/RLRyals/book-series-mcp.git
cd book-series-mcp
npm install

# 2. Create the database + user
sudo -u postgres psql <<'SQL'
CREATE DATABASE book_series;
CREATE USER writer WITH PASSWORD 'secure_writing_password_2025';
GRANT ALL PRIVILEGES ON DATABASE book_series TO writer;
ALTER DATABASE book_series OWNER TO writer;
SQL

# 3. Initialize schema, then apply migrations in date order
export PGPASSWORD=secure_writing_password_2025
psql -h localhost -U writer -d book_series -f init.sql
for m in migrations/2025*.sql; do
  psql -h localhost -U writer -d book_series -f "$m"
done

# 4. Configure the connection and test
cp .env.template .env   # ensure DATABASE_URL points at the DB above
node test-db-connection.js
```

> **Notes learned during setup:**
> - `init.sql` references a few tables that only exist after migrations
>   (`chapter_structure_plans`, `writing_goals`, `character_knowledge_states`)
>   and ships sample data with an out-of-range foreign key. Those specific
>   `init.sql` errors are safe to ignore; the migrations create the missing
>   tables. A couple of migrations are non-idempotent (e.g. an index that
>   "already exists") and depend on `round()` overloads created by later
>   migrations — running the whole `2025*` set in order resolves it.
> - The servers are **MCP stdio** servers. When launched by an MCP client they
>   talk JSON-RPC over stdin/stdout; the HTTP health server is skipped unless
>   run in a TTY. Set `MCP_SERVER_MODE=1` when embedding.

### Register in an MCP client

Point your MCP client (Claude Desktop, Cursor, etc.) at the server entry points
with `DATABASE_URL` in the env. Example entry:

```json
{
  "mcpServers": {
    "book-series-manager": {
      "command": "node",
      "args": ["/abs/path/book-series-mcp/src/index.js"],
      "env": { "DATABASE_URL": "postgresql://writer:secure_writing_password_2025@localhost:5432/book_series" }
    },
    "writing-production": {
      "command": "node",
      "args": ["/abs/path/book-series-mcp/src/writing-server/index.js"],
      "env": { "DATABASE_URL": "postgresql://writer:secure_writing_password_2025@localhost:5432/book_series" }
    }
  }
}
```

## 3. Convert synopsis + outline

Two COMPASS helper scripts (in `Misc/`) turn a Story Bible into Book Series MCP
records. Neither has third-party dependencies (Python stdlib / Node stdlib), and
the converter makes **no** external API calls, so it is deterministic.

### Mapping

| Story Bible source | Book Series MCP tool | Result |
|--------------------|----------------------|--------|
| Synopsis title / series / genre / premise | `create_series`, `create_series_book` | Series + Book records (`main_case_description` = premise) |
| Synopsis `## Characters` bullets | `create_series_character` (one per entry) | Character records (type inferred: protagonist/antagonist/mentor/...) |
| Synopsis `## Themes` bullets | `create_series_plot_thread` (one per theme) | `series_arc` plot threads |
| Outline `## Chapter N: Title` + text | `bulk_chapter_operations` → `create_outline_batch` | Chapter outlines (`status = outlined`) |

A `## Characters` entry may be written as `Name (type): description`,
`**Name** - type, description`, or `Name — type`; the character type is
inferred from keywords in the descriptor (default `supporting`). A chapter
header's inline trailing text is treated as the **title** when short and
title-like, or as the **summary** when it reads like a sentence.

### Step 1 — build the import bundle (offline, deterministic)

```bash
python3 Misc/convert_synopsis_outline_to_book_series.py \
  --synopsis Misc/examples/synopsis.example.md \
  --outline  Misc/examples/outline.example.md \
  --out bundle.json
```

Defaults read `Story_Bible/synopsis.md` and `Story_Bible/outline.md`. Pass
`--series-id N` to import into an existing series instead of creating a new one,
and `--book-number N` to control the book number (default `1`). The output
`bundle.json` is an ordered list of MCP tool-call "steps".

The parser is forgiving: it recognizes `# Title` / `Title:` / `Series:` /
`Genre:` / `Pen name:` metadata, a `## Themes` bullet list, and chapter headers
in several shapes (`## Chapter 1: X`, `Chapter 01 - X`, `- Ch1: X`).

### Step 2 — apply the bundle to a running Book Series MCP

```bash
BOOK_SERIES_MCP_HOME=/abs/path/book-series-mcp \
DATABASE_URL='postgresql://writer:secure_writing_password_2025@localhost:5432/book_series' \
node Misc/import_to_book_series.mjs bundle.json
```

`import_to_book_series.mjs` is a minimal dependency-free MCP client: it spawns
the `manager` and `writing` servers, speaks newline-delimited JSON-RPC 2.0 over
stdio, and substitutes the `$series_id` / `$book_id` ids captured from earlier
steps into later ones. It prints a per-step progress line and the final
`series_id` / `book_id`.

**Deduplication (default on).** Before each create step the importer lists
existing records and skips creation when one already matches, so imports are
**idempotent** and re-importing (or adding a second book to a series) does not
duplicate the cast:

| Create step | Matched against | Match key |
|-------------|-----------------|-----------|
| `create_series_book` | `get_series_books` | `book_number` (existing id reused for `$book_id`) |
| `create_series_character` | `get_series_characters` | `name` |
| `create_series_plot_thread` | `get_series_plot_threads` | `title` |
| `create_series` | `get_series_overview` | `name` |

Chapter outlines are upserted by `chapter_number` by `create_outline_batch`
itself, so they are already idempotent. Pass `--no-dedupe` to disable the checks
and always create.

> Series dedup depends on the upstream `get_series_overview` tool, which relies
> on a `series_overview` view that current Book Series MCP does not create. If
> that tool is unavailable the importer logs nothing special and simply creates
> a new series; to reliably reuse a series, pass `--series-id`.

### Step 3 — verify

Read the data back through the MCP tools, e.g. `get_chapters { book_id }` on the
writing server and `get_series_characters { series_id }` /
`get_series_plot_threads { series_id }` on the manager server. You should see
the chapter outlines (`status: outlined`), one character per `## Characters`
entry, and one `series_arc` thread per theme.

### Tests

The parser has stdlib-only unit tests (no DB required):

```bash
python3 Misc/tests/test_convert_synopsis_outline.py
```

## 4. Relationship to `build_story_structure_mcp.py`

`Misc/build_story_structure_mcp.py` is a *different* converter: it uses the
Anthropic API to emit a standalone `story_structure.json` file (the "Story
Structure MCP" data format). The scripts in this document instead load the
PostgreSQL-backed Book Series MCP directly and require no API key.
