#!/usr/bin/env python3
"""
UserPromptSubmit hook: Bible reminder on decisions.

When Lee's message involves decisions, architecture, or building,
searches the Bible via FTS5 and injects relevant section pointers.
Lightweight: pointers with snippets, not full content.

BYPASS: Set SKIP_HOOK_BIBLE_DECISION=1 to disable.
"""

import sys
import os
import json
import hashlib
from pathlib import Path

if os.environ.get("SKIP_HOOK_BIBLE_DECISION"):
    sys.exit(0)

if sys.stdin.isatty():
    sys.exit(0)

try:
    hook_data = json.loads(sys.stdin.read())
    message = hook_data.get("message", hook_data.get("content", ""))
    if isinstance(message, list):
        message = " ".join(
            block.get("text", "")
            for block in message
            if isinstance(block, dict) and block.get("type") == "text"
        )
except (json.JSONDecodeError, Exception):
    sys.exit(0)

if not message or len(message) < 25:
    sys.exit(0)

# Multi-word trigger phrases (avoids false positives per feedback_hook_keywords.md)
TRIGGER_PHRASES = [
    # Decision signals
    "should we", "should i", "what approach", "how should",
    "which pattern", "what's the right", "trade-off", "tradeoff",
    # Build signals
    "build this", "implement this", "start building", "start coding",
    "let's build", "time to build", "ready to build",
    # Architecture signals
    "architecture", "where does this live", "how does this fit",
    "system design", "component placement",
    # Anti-pattern signals
    "anti-pattern", "code smell", "something feels wrong",
    "this seems off", "red flag",
    # Debt/refactor signals
    "refactor this", "technical debt", "clean up", "clean this up",
    "rip out", "rip this out", "simplify this",
    # Checkpoint signals
    "checkpoint", "gate criteria", "milestone", "success criteria",
    "how do we know", "definition of done",
]

message_lower = message.lower()
triggered_phrases = [p for p in TRIGGER_PHRASES if p in message_lower]

if not triggered_phrases:
    sys.exit(0)

# Session dedup — don't repeat the same section cluster
session_id = os.environ.get("SESSION_ID", os.environ.get("CLAUDE_SESSION_ID", "default"))
safe_id = hashlib.sha256(session_id.encode()).hexdigest()[:16]
dedup_file = Path(f"/tmp/bible-decisions-{safe_id}.json")

seen_clusters = set()
if dedup_file.exists():
    try:
        seen_clusters = set(json.loads(dedup_file.read_text()).get("seen", []))
    except (json.JSONDecodeError, Exception):
        pass

# FTS5 search the user's message
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bible_index import search_bible, needs_reindex, reindex

if needs_reindex():
    reindex()

results = search_bible(message, limit=3)
if not results:
    sys.exit(0)

# Filter out already-seen section clusters
new_results = []
for r in results:
    if r["section"] not in seen_clusters:
        new_results.append(r)

if not new_results:
    sys.exit(0)

# Build lightweight pointer output
lines = ["🛐 Bible check — decision detected. Relevant sections:"]
for r in new_results[:3]:
    # Clean snippet for display
    snippet = r["snippet"].replace(">>>", "").replace("<<<", "")
    # Truncate long snippets
    if len(snippet) > 120:
        snippet = snippet[:117] + "..."
    lines.append(f'  • §{r["section"]} {r["title"]} — "{snippet}"')

lines.append("  Read these before proceeding: Work/_ Infrastructure/Build Bible.md")

# Output to stderr (context hint, not blocking)
print("\n".join(lines), file=sys.stderr)

# Update dedup
seen_clusters.update(r["section"] for r in new_results)
try:
    dedup_file.write_text(json.dumps({"seen": list(seen_clusters)}))
except Exception:
    pass

sys.exit(0)
