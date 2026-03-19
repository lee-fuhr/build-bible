# Build Bible

Building with Claude Code without a methodology is just hoping. This document makes it a practice.

---

## The problem

You build something with Claude Code. It works. Three weeks later, the same agent makes different decisions, the same pattern looks different in a new project, the same mistake happens again. You're not building a system -- you're accumulating sessions.

The real cost isn't any single mistake. It's the compounding. Every time you reinvent instead of reuse, every time you skip an anti-pattern you already know, every time a new session starts without the shared vocabulary from the last one -- you're paying for the same work twice.

After enough sessions, you start noticing the debt: god files you can't refactor, sync jobs you can't untangle, research agents running for weeks without checkpoints. The problems don't announce themselves. They're invisible until they're expensive.

And the meta moves fast. What counted as a best practice six months ago is already outdated. New agent patterns, new orchestration approaches, new failure modes -- the community is learning faster than any individual can track. Most people are building on stale foundations without knowing it.

## What changes

**You stop reinventing.** 19 proven patterns with specific use cases and production citations. When a problem looks familiar, you reach for the pattern instead of rebuilding from memory.

**You catch mistakes before they cost you.** 8 named failure modes -- the 49-day research agent, the premature learning engine, the god file -- each with specific evidence of what it costs. Naming a thing is most of solving it.

**Your system improves instead of decaying.** The evolution protocol makes the Bible a living document. Principles accumulate production evidence. Patterns get updated when they fail. New techniques from the community get synthesized in. What the field learns, you learn.

## What's in it

- **14 principles** -- the non-negotiable rules: TDD, atomic operations, single source of truth, simplicity, checkpoint gates, and nine more. Each backed by evidence, not opinion.
- **20 reusable patterns** -- tiered agent model, approval queue, config-driven scaling, conductor pattern, and sixteen more. Each with a selection guide so you know when to reach for it.
- **10 anti-patterns with costs** -- specific names for the failure modes, specific evidence of what they cost. Recognize them fast.
- **4-phase project playbook** -- from idea to self-sustaining operation: foundation, build, operationalize, evolve.
- **Agent routing and cost model** -- how to structure multi-agent systems with cost-tier routing (80% Haiku / 15% Sonnet / 5% Opus).
- **Evolution protocol** -- how to update the Bible as you learn, so it doesn't go stale.
- **`/qq-bible-add` slash command** -- included in `commands/`. Feed it a URL, a paste, or a link. It judges merit, maps the item against what already exists, and integrates if worthy. This is how the document evolves.

**Add it to Claude Code:**

```
curl -fsSL https://raw.githubusercontent.com/lee-fuhr/build-bible/main/install.sh | bash
```

Installs the reference card (`~/.claude/rules/build-bible.md`) and the `/qq-bible-add` command. Start a new session and the Bible is active. Run `/qq-bible-add [url or paste]` whenever you find something worth keeping.

---

## Contributing

The meta for building with AI agents changes fast. New patterns emerge from production, Reddit, and community experiments constantly. The Build Bible stays useful by synthesizing what actually works -- but it needs input from people building in the field.

If you've found a principle that belongs here, an anti-pattern that should be named, a pattern that's proven out in your own system, or something in the current Bible that no longer holds -- open an issue or a PR. That's the mechanism.

## Part of the stack

These four repos work together. Each one captures best practices from production use, open-source repos, and community experiments — synthesized, deduplicated, and maintained as a single living reference. What the field learns, these learn.

| Repo | What it does |
|------|-------------|
| **[Build Bible](https://github.com/lee-fuhr/build-bible)** | Every engineering principle and pattern that's proven out in production with AI agents, unified into one methodology. |
| **[Atlas](https://github.com/lee-fuhr/atlas)** | Every architectural pattern for where components live in a Claude Code system, so nothing is ad hoc. |
| **[Memeta](https://github.com/lee-fuhr/memeta)** | Every memory technique that works — extraction, scoring, search, decay, recall — all coexisting additively. |
| **[ai-ops-starter](https://github.com/lee-fuhr/ai-ops-starter)** | Everything you need to stand up the system: folder structure, hooks, skills, templates. Minutes, not months. |

---

MIT -- see [LICENSE](LICENSE)
