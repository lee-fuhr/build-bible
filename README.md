# Build Bible

**How to build with AI agents. 14 principles, 19 patterns, 8 anti-patterns, a full playbook, and an evolution protocol — all battle-tested across real projects.**

---

## What this is

A methodology document for building software with Claude Code and AI agent systems. Not theory — every principle has evidence from production use, every pattern has a "proven in" citation, and every anti-pattern has a "cost" showing what happens when you ignore it.

The Bible covers:

- **14 principles** — the non-negotiable rules (TDD, simplicity, single source of truth, atomic operations, etc.)
- **19 reusable patterns** — proven approaches you can lift into your own system (tiered agent model, approval queue, config-driven scaling, etc.)
- **8 anti-patterns** — what goes wrong and what it costs (the 49-day research agent, the premature learning engine, the god file, etc.)
- **4-phase playbook** — how to take a project from idea to self-sustaining operation
- **Agent routing** — how to structure multi-agent systems with cost-tier routing
- **Evolution protocol** — how to keep the Bible itself alive as you learn

## Who this is for

Anyone building with Claude Code who wants a structured methodology for:
- Multi-agent orchestration (conductor pattern, agent teams, delegation)
- AI-augmented operations (hooks, LaunchAgents, automated pipelines)
- Sustainable AI development practices (TDD, verification, checkpoints)

## How to use it

**Option 1: Read it.** The document is self-contained. Start with the principles (section 1), then browse patterns (section 2) for things relevant to your current work.

**Option 2: Adopt it.** Fork this repo and make it yours:
1. Replace the evidence citations with your own project examples
2. Add principles you discover through your own work
3. Remove patterns you don't use
4. Use the evolution protocol (section 8) to keep it current

**Option 3: Load it into Claude Code.** Add to your `~/.claude/rules/` directory:
```markdown
<!-- ~/.claude/rules/build-bible.md -->
## How we build (bible reference)
Full bible: /path/to/build-bible.md
Load when: Starting a project, making architecture decisions, reviewing code.
```

## Document structure

| Section | What it covers |
|---------|---------------|
| 0 | Meta — version, scope, how to read |
| 1 | 14 principles with evidence |
| 2 | 19 reusable patterns with pointers |
| 3 | 5-layer architecture model |
| 4 | 4-phase project playbook |
| 5 | Agent routing and cost model |
| 6 | 8 anti-patterns with costs |
| 7 | System inventory and integration map |
| 8 | Evolution protocol |
| 9 | Technical debt inventory |
| 10 | Sources and references |

## Related projects

- **[Memeta](https://github.com/lee-fuhr/memeta)** — FSRS-6 memory system for Claude Code (the memory layer referenced in the Bible)
- **[Atlas](https://github.com/lee-fuhr/atlas)** — Architectural governing document (the KCA model that organizes the system the Bible describes)

## License

MIT — see [LICENSE](LICENSE)

---

*A living document. Use the evolution protocol to keep it honest.*
