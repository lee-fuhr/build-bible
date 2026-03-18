# Changelog

All notable changes to the Build Bible are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/) — MAJOR for structural changes, MINOR for new principles/patterns, PATCH for refinements.

## [1.7.0] - 2026-03-18

Studied three open-source AI memory systems and extracted what they got right that we hadn't codified yet. The Bible now has better guardrails for LLM scoring pipelines, data imports, and research workflows — areas where we were relying on instinct instead of written practice.

### Added
- **Pattern 2.20: "Panning for gold"** — three-phase discovery processing (extract everything without filtering, evaluate the best, synthesize with verdicts). Based on OB1's brain dump recipe.
- **Score calibration anchors** for LLM-based scoring (pattern 2.4) — provide 5 anchor examples at different score levels to prevent clustering toward the middle. From cerebellum's gatekeeper.
- **Prompt injection defense** for LLM evaluation pipelines (principle 1.8) — explicitly instruct the scorer to treat content as data, not instructions. From cerebellum.
- **Content fingerprinting** as a companion to fuzzy dedup (pattern 2.6) — SHA-256 hash on normalized content for idempotent imports across multiple sources. From OB1, proven at 75K+ records.
- **Directive type hierarchy** for promoted knowledge (pattern 2.14) — recast learnings into their highest-impact format on promotion: hard prohibition > preference with context > anti-pattern + consequence > process requirement > scope guard. From cerebellum.
- **Sacred core schema constraint** (principle 1.5) — shared data stores should declare core columns as immutable; extensions can add but never alter or drop. From OB1.
- **Extension composability** (pattern 2.2) — extensions should be able to query across each other's data stores for emergent value, not be siloed. From OB1.
- **Automated borderline review** (section 5.5) — add a skeptical critic pass on items scoring in the middle range of any automated pipeline. One cheap LLM call prevents mid-quality noise. From cerebellum.
- Credits for [dandaka/traul](https://github.com/dandaka/traul), [jj-valentine/cerebellum](https://github.com/jj-valentine/cerebellum), and [NateBJones-Projects/OB1](https://github.com/NateBJones-Projects/OB1) in section 10.
- Pattern selection guide entries for research/brain dumps and LLM scoring pipelines.

## [1.6.0] - 2026-03-11

Absorbed hard-won lessons from a 120-agent enterprise system. The Bible now has a clear quality bar for agent definitions and named patterns for two failure modes that had been biting us without names.

### Added
- Agent definition quality bar (section 5.5) — distinct voice, concrete deliverables, measurable success criteria, step-by-step workflow, domain guardrails. From msitarzewski/agency-agents.
- Zero-findings skepticism heuristic — a review with zero findings is almost always a superficial pass, not a clean build.
- Retry limit before approach change (section 5.1) — after 3 failures on the same task, change approach entirely.
- Escalation report format — problem + recommendation + consequence.
- Blameless post-mortem protocol (section 4.6) — timeline, impact, root cause, action items, prevention.
- Anti-patterns 6.9 (silent placeholder) and 6.10 (unenforceable punchlist).
- Credits for [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) in section 10.

## [1.5.1] - 2026-03-06

Closed the gap between "the plan looks good" and "the plan is actually approved." Agents now pause for a human checkpoint before executing, not just after planning.

### Added
- Execution gate for principle 1.2 (QA before code) — agents must articulate their step-by-step plan and wait for human approval before starting. Distinct from steelman (self-review during planning); this is the human checkpoint at the planning-to-execution handoff. From The Neuron newsletter.

## [1.5.0] - 2026-03-04

Tightened how we think about prevention and verification, and added a way to find the best solution instead of settling for the first correct one.

### Added
- Swiss-cheese model framing for principle 1.8 (prevent, don't recover) — each validation layer is imperfect, but independent layers rarely have aligned holes. From Latent Space "How to Kill the Code Review."
- Verification-before-generation rule for principle 1.2 — define the full verification stack before any code generation.
- Pattern 2.19: Competitive generation — parallel solutions with objective ranking for the best artifact.
- Section 5.6: Agent permission architecture — narrowest possible scope per task, escalation triggers for sensitive operations.
- Human's true role addendum to principle 1.1 — in AI-augmented systems, the human defines constraints, not manages output.

## [1.4.1] - 2026-03-03

Three sharp lessons from the Reddit community that gave us new diagnostic tools and a stronger stance on turning mistakes into permanent guardrails.

### Added
- 1-shot prompt test diagnostic (principle 1.4) — if you can't accomplish a task in a single well-formed prompt, diagnose why: code is a mess, docs are wrong, or problem is too big. From r/ClaudeCode.
- AI force multiplier framing (principle 1.14) — AI accelerates the direction you're already going. Clean codebase gets cleaner faster; messy codebase gets messier faster. From Andrej Karpathy via r/ClaudeCode.
- "Codify agent failures as preventive rules" (section 8.3) — convert agent mistakes into CLAUDE.md rules immediately, not just memory notes. Negative rules prevent recurrence at the instruction level.

## [1.4.0] - 2026-03-03

Made multi-agent work safer with pre-run checkpoints and isolation guarantees. Recovering from a bad agent run is now one git command instead of an archaeology project.

### Added
- Git checkpoint protocol for agent runs (section 5.1) — commit before launching multi-file agents so recovery is one command. From r/ClaudeCode cheatsheet thread, u/ultrathink-art.
- Agent memory isolation (section 5.4) — no shared mutable state between concurrent agents. Each gets its own context in the task spec. From r/ClaudeCode, u/ultrathink-art.
- `--resume` targeting note (section 5.1) — use `--resume <id>` instead of `--continue` for reliable session restoration. From r/ClaudeCode, u/quest-master.

## [1.3.0] - 2026-03-02

Every principle and pattern in the Bible can now be traced back to where it came from. No more "I think we got this from..." — full provenance, fully credited.

### Added
- Section 10 (credits and sources) — full provenance for every principle, pattern, and external contribution. Seven subsections covering repos, articles, Reddit, and internal process.

## [1.2.1] - 2026-03-02

Integrated Jesse Vincent's Superpowers patterns — the most directly impactful external contribution to our TDD and agent review practices.

### Added
- Mandatory task dependency tracking (sections 5.1, 5.4) — use `blocks`/`blockedBy` to enforce execution order in multi-task work. From obra/superpowers.
- Two-stage subagent review (section 5.5) — separate spec compliance from code/content quality. From obra/superpowers.
- Pre-test code deletion escalation (anti-pattern 6.4) — code written before its tests should be deleted and rewritten test-first, not retrofitted. From obra/superpowers.

## [1.2.0] - 2026-03-02

Built the enforcement backbone. Every principle now maps to at least one mechanism that actually enforces it, and the gaps are documented honestly.

### Added
- Section 3.6: Enforcement tooling layer with traceability matrix mapping every principle to its enforcement mechanism.
- Section 5.3.1: Cross-model routing for Gemini, Codex, and Perplexity — when to use non-Claude models.
- `/qq-bible-add` ingestion pipeline for structured external knowledge integration.
- Enforcement gaps added to section 9 debt inventory.

### Changed
- Changelog moved from inline bible section to this satellite file.

## [1.1.0] - 2026-03-02

Expanded from 11 principles to 14 and added the patterns that were being used but never written down. The Bible now covers observability, failure testing, and the speed-vs-debt trap.

### Added
- Principles 1.12 (observe everything), 1.13 (unhappy path first), 1.14 (speed hides debt).
- Patterns 2.16 (adversarial teams), 2.17 (backup verification), 2.18 (rate limiting).
- Anti-pattern 6.8 (the silent service).
- Adversarial team protocol with worked example.
- Section 8.5: Memeta synergy — how the Bible and memory system feed each other.
- Conductor question 2b (review intensity selection).

## [1.0.0] - 2026-03-01

The first codification of how we actually build things. Everything before this was scattered across sessions, memory, and instinct.

### Added
- 14 principles, 18 patterns, 8 anti-patterns, 12 debt items.
- Distilled from 10+ products across 68+ sessions.
- Adversarially reviewed by 3 independent agents.
