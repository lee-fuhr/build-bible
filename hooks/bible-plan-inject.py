#!/usr/bin/env python3
"""
PreToolUse hook: Bible injection on EnterPlanMode.

When Claude enters plan mode, physically injects relevant Bible sections
into the conversation context. Can't skip what's already in front of you.

Always injects: §0 (Quick reference) + §6 (Anti-patterns)
FTS5 bonus: searches session topic for additional relevant sections.
Cap: ~400 lines total.

Outputs to stdout → becomes additionalContext in conversation.
BYPASS: Set SKIP_HOOK_BIBLE_INJECT=1 to disable.
"""

import sys
import os
import json
import hashlib
from pathlib import Path

if os.environ.get("SKIP_HOOK_BIBLE_INJECT"):
    sys.exit(0)

# Only fire on EnterPlanMode
if sys.stdin.isatty():
    sys.exit(0)

try:
    hook_data = json.loads(sys.stdin.read())
except (json.JSONDecodeError, Exception):
    sys.exit(0)

tool_name = hook_data.get("tool_name", "")
if tool_name != "EnterPlanMode":
    sys.exit(0)

# Session dedup — only inject once per session
session_id = os.environ.get("SESSION_ID", os.environ.get("CLAUDE_SESSION_ID", "default"))
safe_id = hashlib.sha256(session_id.encode()).hexdigest()[:16]
dedup_file = Path(f"/tmp/bible-injected-{safe_id}.json")

if dedup_file.exists():
    try:
        dedup_data = json.loads(dedup_file.read_text())
        if dedup_data.get("injected"):
            sys.exit(0)
    except (json.JSONDecodeError, Exception):
        pass

# Import bible indexer (same directory)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bible_index import search_bible, get_section_content, get_section_with_children, needs_reindex, reindex

# Auto-reindex if needed
if needs_reindex():
    reindex()

# Always-inject sections
ALWAYS_SECTIONS = ["0", "6"]
LINE_CAP = 400

sections_to_inject = []
lines_used = 0

# Get always-inject sections with all subsections (§0 and §6 are top-level)
for sec_num in ALWAYS_SECTIONS:
    content = get_section_with_children(sec_num)
    if content:
        line_count = content.count("\n") + 1
        sections_to_inject.append({
            "section": sec_num,
            "title": f"§{sec_num}",
            "content": content,
            "lines": line_count,
            "source": "always",
        })
        lines_used += line_count

# FTS5 search using session topic
fts_matches = []
session_topic_dir = Path(os.path.expanduser("~/.claude/session-topics"))
topic_file = session_topic_dir / f"{session_id}.txt"
topic_query = ""

if topic_file.exists():
    topic_query = topic_file.read_text().strip()

# Also check tool_input for plan description
plan_input = hook_data.get("tool_input", {})
if isinstance(plan_input, dict):
    plan_desc = plan_input.get("description", "") or plan_input.get("plan", "")
    if plan_desc:
        topic_query = f"{topic_query} {plan_desc}".strip()

if topic_query:
    results = search_bible(topic_query, limit=4)
    for r in results:
        sec = r["section"]
        # Skip if already in always-inject
        if sec in ALWAYS_SECTIONS:
            continue
        # Skip if it's a child of an always-inject section
        if any(sec.startswith(f"{a}.") for a in ALWAYS_SECTIONS):
            continue

        content = get_section_content(sec)
        if not content:
            continue

        line_count = content.count("\n") + 1
        if lines_used + line_count > LINE_CAP:
            continue

        sections_to_inject.append({
            "section": sec,
            "title": r["title"],
            "content": content,
            "lines": line_count,
            "source": "fts5",
            "snippet": r["snippet"],
        })
        lines_used += line_count
        fts_matches.append(r)

        # Max 2 FTS bonus sections
        if len(fts_matches) >= 2:
            break

# Build output
output_lines = []
output_lines.append("🛐 BUILD BIBLE INJECTED — Steelman step 0 satisfied.")
output_lines.append(f"Always loaded: §0 (Quick reference), §6 (Anti-patterns)")

if fts_matches:
    for m in fts_matches:
        output_lines.append(
            f'FTS5 matched: §{m["section"]} ({m["title"]}) — matched topic'
        )

output_lines.append("")

for s in sections_to_inject:
    label = s["section"]
    if s["source"] == "fts5":
        label = f'{s["section"]} ({s["title"]}, FTS5 match)'
    output_lines.append(f"--- §{label} ---")
    output_lines.append(s["content"])
    output_lines.append("")

output_lines.append(f"Total: {lines_used} lines injected. Read additional sections relevant to YOUR SPECIFIC WORK using the Read tool on Work/_ Infrastructure/Build Bible.md.")

# Write to stdout for additionalContext injection
print("\n".join(output_lines))

# Mark session as injected
try:
    dedup_file.write_text(json.dumps({"injected": True, "lines": lines_used}))
except Exception:
    pass

sys.exit(0)
