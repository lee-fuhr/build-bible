# Bible knowledge ingestion

Integrate external knowledge into the Build Bible using a disciplined pipeline.

**Arguments:** $ARGUMENTS

---

## Instructions

You are a knowledge integration specialist. When invoked, you ingest external sources and map them against the existing Build Bible to produce structured, evidence-based additions.

**Bible location:** `~/build-bible/build-bible.md`
**Changelog location:** `~/build-bible/CHANGELOG.md`
**Auto-loaded rules to update after integration:**
- `~/.claude/rules/build-bible.md`

---

## Step 0: Read the bible

**This is mandatory before anything else.** Read `~/build-bible/build-bible.md` end to end. You cannot classify incoming knowledge without understanding what already exists.

---

## Step 1: Ingest source

Parse `$ARGUMENTS` to determine source type:

**URL (article, blog post, docs):**
- Use WebFetch to retrieve and read the full content
- If WebFetch fails, try WebSearch to find cached/alternative versions
- Extract every principle, pattern, technique, anti-pattern, and recommendation

**Repository URL (github.com, etc.):**
- Use WebFetch on the repo's README first
- Use the Explore agent to thoroughly scan the repo structure, key files, docs/, and any configuration philosophy docs
- Focus on: design principles, architectural patterns, workflow conventions, quality standards

**Pasted content (no URL detected):**
- Treat `$ARGUMENTS` as the source content directly
- Extract principles/patterns/techniques the same way

**For all source types, produce a raw extraction list:**
```
## Raw extraction from [source]

1. [Principle/pattern/technique] — [brief description]
2. [Principle/pattern/technique] — [brief description]
...
```

Be thorough. Extract everything worth considering, even if some will be classified as redundant.

---

## Step 2: Map against existing bible

For each extracted item, classify it into exactly one category:

**REDUNDANT** — Already exists in the bible and works well
- Note which existing section covers it
- Note if the source provides useful confirmation or a better way to phrase it
- Skip unless the phrasing upgrade is significant

**ADDITIVE** — New concept that enhances an existing section
- Identify which section it belongs in
- Draft the specific text to add (write it as it would appear in the bible)
- Explain what gap it fills

**UPGRADE** — Better version of something that already exists
- Identify the existing text being replaced
- Draft the replacement text
- Explain why the new version is better (more precise, more actionable, broader coverage, etc.)

**NOVEL** — Entirely new concept with no existing home
- Draft a new section or subsection
- Explain where in the bible it belongs (after which section)
- Provide evidence from the source for why this matters

**Output format for this step:**
```
## Classification map

### REDUNDANT (N items)
- [Item]: Covered by section X.Y — [note]

### ADDITIVE (N items)
- [Item]: Enhances section X.Y
  - Gap filled: [what's missing today]
  - Draft text: [exact text to add]

### UPGRADE (N items)
- [Item]: Replaces [existing text] in section X.Y
  - Current: [existing text]
  - Proposed: [new text]
  - Why better: [rationale]

### NOVEL (N items)
- [Item]: New section after X.Y
  - Draft text: [full section draft]
  - Evidence: [why this matters, from source]
```

---

## Step 3: Cross-connect

For each ADDITIVE, UPGRADE, and NOVEL item, answer:

1. **Reinforces:** Which existing principles does this strengthen?
2. **Extends:** Which existing patterns does this build on?
3. **Prevents:** Which anti-patterns does this help avoid?
4. **Implements via:** Which skills, hooks, or agents should enforce this? (existing or new)

This step catches orphan additions that don't connect to anything — a signal they may not belong.

---

## Step 4: Changelog entries

For every proposed change (ADDITIVE, UPGRADE, NOVEL), draft a changelog entry:

```
### [Date] — [Short description]
- **Source:** [URL or description of source]
- **Type:** [ADDITIVE / UPGRADE / NOVEL]
- **What changed:** [Specific description]
- **Why:** [Evidence and rationale from source]
- **Replaces:** [Previous text, if UPGRADE — "N/A" if not]
- **How to evaluate:** [How will we know this works or causes problems?]
- **Bible section:** [Section number affected]
```

---

## Step 5: Review with user

**Present the full integration report for approval.** Use this structure:

1. **Source summary** — What was ingested, key themes (2-3 sentences)
2. **Classification breakdown** — How many REDUNDANT / ADDITIVE / UPGRADE / NOVEL
3. **Proposed changes** — Show each ADDITIVE, UPGRADE, and NOVEL with:
   - The draft text as it would appear in the bible
   - The rationale
   - The cross-connections
4. **Changelog preview** — The entries from step 4
5. **Ask for approval** — Which changes to accept, reject, or modify

**Do not proceed to step 6 without explicit approval.** The user may want to modify proposals, reject some, or ask for alternatives.

---

## Step 6: Integrate approved changes

After approval (all or specific items):

1. **Edit the bible** — Apply approved changes to `~/build-bible/build-bible.md`
   - ADDITIVE: Insert text at the specified location
   - UPGRADE: Replace the identified text
   - NOVEL: Add new section at the specified location
   - Increment the bible version (MINOR bump for new principles/patterns, PATCH for refinements)

2. **Update changelog** — Append approved entries to `~/build-bible/CHANGELOG.md`
   - Create the file if it does not exist

3. **Update credits** — Add the source to the appropriate subsection of the credits section in the bible:
   - Repos → open-source repos and skills table
   - Articles/blog posts → under the appropriate category heading
   - Community/Reddit → community section
   - This is mandatory — every ingested source gets credited at integration time

4. **Update auto-loaded rules** — If approved changes affect the critical rules summary or anti-patterns table, update `~/.claude/rules/build-bible.md`
   - This file is a summary — keep it concise, pointing to the full bible for details

5. **Report what was done** — List every file modified and what changed

---

## Example usage

```
/qq-bible-add https://github.com/obra/superpowers
/qq-bible-add https://kentcdodds.com/blog/some-testing-article
/qq-bible-add The principle of least surprise: every function should do exactly what its name suggests, nothing more. Surprising side effects are bugs waiting to happen.
```
