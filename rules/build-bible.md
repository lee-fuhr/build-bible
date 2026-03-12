<!-- Auto-loaded rule: how we build -->

## How we build (bible reference)

**Full bible:** `~/build-bible/build-bible.md` (v1.5.1, sections 0-10)
**Load when:** Starting a project, making architecture decisions, reviewing code, or when any trigger below fires.

### Critical rules (always active)

1. **Orchestrate, don't execute** — Delegate to specialist agents. Solo execution only for single atomic actions. Target: 80% delegation rate.
2. **QA before code** — Review intensity spectrum: steelman (every plan) → QA swarm (>2hr builds) → adversarial team (architecture/irreversible). Suggest upgrading when stakes warrant.
3. **TDD: red, green, refactor** — Tests must fail first. No exceptions.
4. **Simplicity wins** — Delete what isn't earning its complexity. 500-line file limit.
5. **Single source of truth** — One canonical store per data domain. No sync jobs, no drift.
6. **Config-driven** — Scale with data files, not code changes.
7. **Checkpoint gates** — Measurable criteria, specific dates, predetermined failure response.
8. **Prevent, don't recover** — Validate before acting. Layered pre-validation for external actions.
9. **Atomic operations** — Temp file + rename. Never leave partial state.
10. **Document when fresh** — Capture decisions during work, not after.
11. **Actionable metrics** — Every metric triggers a specific action at a specific threshold.
12. **Observe everything** — Structured logging, health checks, tiered alerting for every service.
13. **Unhappy path first** — Test error paths and edge cases before happy paths.
14. **Speed hides debt** — Fast shipping without verification creates invisible debt.

### Anti-patterns to catch

| Name | Signal | Bible ref |
|------|--------|-----------|
| The 49-day research agent | Automation running without checkpoint validation | section 6.1 |
| The premature learning engine | Building ML/scoring at low data volume | section 6.2 |
| Solo execution | Conductor writing code instead of delegating | section 6.3 |
| The retrospective test | Tests written after implementation | section 6.4 |
| Multiple sources of truth | Sync jobs between data stores | section 6.5 |
| Validate-then-pray | Try/catch instead of pre-validation | section 6.6 |
| The god file | Any file approaching 500 lines | section 6.7 |
| The silent service | Deployed service with no monitoring/alerting | section 6.8 |

### When to consult the full bible

| Section | Load when... |
|---------|-------------|
| **0** Quick reference | Fast sanity-check: "am I missing anything obvious before I ship?" |
| **1** Core principles | Evaluating a trade-off; someone challenges a decision; "is this the right call?" |
| **2** Reusable patterns | Choosing how to build something; "what's the right pattern for X?" |
| **3** Architecture & integration | Placing a component; planning layer changes; enforcement traceability questions |
| **4** Project playbook | Starting a new project or phase; "what's the full lifecycle for this?" |
| **5** Agent system | Any delegation decision; multi-agent sequencing; routing; "who handles this?" |
| **6** Anti-patterns | Something feels wrong; seeing a code smell or architectural red flag; "have we seen this before?" |
| **7** System inventory | "What exists?"; verifying component counts; rationale for a specific script/agent |
| **8** Evolution protocol | Updating the Bible, Atlas, CLAUDE.md, or any governing doc; codifying a learning |
| **9** Known debt | Prioritizing refactors; assessing technical risk; "is this on the debt list?" |
| **10** Credits & sources | Tracing where a principle came from; audit/provenance questions |

**Also load section 1 or 6 during conversation** (not just plan mode) any time a question involves choosing between technical approaches, evaluating architectural options, or touching anti-pattern territory.
