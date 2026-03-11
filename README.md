# Build Bible

Building with Claude Code without a methodology is just hoping. This document makes it a practice.

---

## The problem

You build something with Claude Code. It works. Three weeks later, the same agent makes different decisions, the same pattern looks different in a new project, the same mistake happens again. You're not building a system -- you're accumulating sessions.

The real cost isn't any single mistake. It's the compounding. Every time you reinvent instead of reuse, every time you skip an anti-pattern you already know, every time a new session starts without the shared vocabulary from the last one -- you're paying for the same work twice.

After enough sessions, you start noticing the debt: god files you can't refactor, sync jobs you can't untangle, research agents running for weeks without checkpoints. The problems don't announce themselves. They're invisible until they're expensive.

## What changes

**You stop reinventing.** 19 proven patterns with specific use cases and production citations. When a problem looks familiar, you reach for the pattern instead of rebuilding from memory.

**You catch mistakes before they cost you.** 8 named failure modes -- the 49-day research agent, the premature learning engine, the god file -- each with specific evidence of what it costs. Naming a thing is most of solving it.

**Your system improves instead of decaying.** The evolution protocol makes the Bible a living document. Principles accumulate production evidence. Patterns get updated when they fail. What you learn doesn't stay in one session.

## What's in it

- **14 principles** -- the non-negotiable rules: TDD, atomic operations, single source of truth, simplicity, checkpoint gates, and nine more. Each backed by evidence, not opinion.
- **19 reusable patterns** -- tiered agent model, approval queue, config-driven scaling, conductor pattern, and sixteen more. Each with a selection guide so you know when to reach for it.
- **8 anti-patterns with costs** -- specific names for the failure modes, specific evidence of what they cost. Recognize them fast.
- **4-phase project playbook** -- from idea to self-sustaining operation: foundation, build, operationalize, evolve.
- **Agent routing and cost model** -- how to structure multi-agent systems with cost-tier routing (80% Haiku / 15% Sonnet / 5% Opus).
- **Evolution protocol** -- how to update the Bible as you learn, so it doesn't go stale.

**Add it to Claude Code:** Create `~/.claude/rules/build-bible.md` pointing at this file. Claude ingests it every session. No cloning, no setup -- just a one-line reference.

---

## Part of the stack

| Repo | Role |
|------|------|
| [Atlas](https://github.com/lee-fuhr/atlas) | Framework -- where every component lives and why |
| [Memeta](https://github.com/lee-fuhr/memeta) | Memory -- what Claude remembers across sessions |
| [ai-ops-starter](https://github.com/lee-fuhr/ai-ops-starter) | Scaffolding -- the folder structure and templates to stand up a system |

---

MIT -- see [LICENSE](LICENSE)
