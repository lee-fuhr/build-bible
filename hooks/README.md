# Bible enforcement hooks

4-layer enforcement system that makes the Build Bible physically present in every planning session and decision conversation.

## Problem

Rules files told Claude to "read the Bible before planning" — but Claude lip-serviced it, referencing section numbers without actually reading the content. The summary was treated as sufficient.

## Solution

### Layer 0: `bible_index.py` — FTS5 indexer
Parses the Build Bible into an SQLite FTS5 database for instant full-text search. Same pattern as `sessions.db`. Any hook can call `search_bible("query")` and get ranked results in sub-millisecond time.

### Layer 1: `bible-plan-inject.py` — PreToolUse hook on `EnterPlanMode`
When Claude enters plan mode, physically injects:
- §0 (Quick reference) — always
- §6 (Anti-patterns) — always
- 1-2 FTS5 bonus sections matched to the session topic

Output goes to stdout → becomes `additionalContext` in the conversation. Can't skip what's already in front of you.

### Layer 2: `bible-decision-detector.py` — UserPromptSubmit hook
When the user's message contains decision/architecture phrases ("should we", "how should", "anti-pattern", "refactor this"), runs FTS5 search and outputs relevant Bible section pointers to stderr.

### Layer 3: Rules hardening
The `build-bible.md` rules file now explicitly says:
- Plans without Bible citations are INVALID
- The Read tool must be used on the actual Bible, not the summary
- Every design decision must cite a specific section number

## Configuration

```json
// settings.json — PreToolUse
{
  "matcher": "EnterPlanMode",
  "hooks": [{
    "type": "command",
    "command": "python3 /path/to/hooks/bible-plan-inject.py",
    "timeout": 5000
  }]
}

// settings.json — UserPromptSubmit
{
  "hooks": [{
    "type": "command",
    "command": "python3 /path/to/hooks/bible-decision-detector.py",
    "timeout": 3000
  }]
}
```

## Bypass

- `SKIP_HOOK_BIBLE_INJECT=1` — disables plan injection
- `SKIP_HOOK_BIBLE_DECISION=1` — disables decision detection

## What this catches

| Scenario | Before | After |
|----------|--------|-------|
| Claude enters plan mode | Bible summary in rules file, easily ignored | Bible §0 + §6 physically injected |
| User asks "how should we build X?" | Nothing | Bible sections surfaced |
| Claude writes plan without citations | Nothing prevents it | Rules say plan is INVALID |

## Key design decisions

- **FTS5 over hardcoded keywords**: The Bible's own text is the search index. No keyword map to maintain. Re-index when Bible changes.
- **Multi-word trigger phrases**: Single words cause false positives in code/paths. Only multi-word phrases trigger the decision detector.
- **Session dedup**: Each hook injects once per session to prevent spam.
- **400-line cap**: Prevents context bloat on plan injection.
