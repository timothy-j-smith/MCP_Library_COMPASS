# ACE Learn

Capture learning from a completed task to improve future AI assistance.

## Action Required

Use the `ace_learn` MCP tool to capture what was learned:

```
ace_learn(
  task: "<what you accomplished>",
  trajectory: ["<key step 1>", "<key step 2>"],
  success: true,
  output: "<lessons learned>",
  git: { commit_hash: "<hash-if-available>", branch: "<branch-if-available>" }
)
```

Call `ace_learn` once after substantial work, ideally after the session summary is available.

## Example

After implementing a feature:
```
ace_learn(
  task: "Implemented JWT authentication",
  trajectory: [
    "Added auth middleware",
    "Created login endpoint",
    "Added token refresh flow"
  ],
  success: true,
  output: "Use httpOnly cookies for refresh tokens and short-lived access tokens.",
  git: { commit_hash: "abc1234", branch: "feature/jwt-auth" }
)
```

## When to Use

- After completing a significant task
- When you discovered something important
- After fixing a tricky bug
- When a pattern worked well (or didn't)