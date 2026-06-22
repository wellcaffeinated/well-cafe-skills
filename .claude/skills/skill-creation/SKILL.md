---
name: skill-creation
description: Writing and improving Claude Code agent skills — SKILL.md structure, reference file organization, description trigger phrases, and conventions specific to this marketplace. Use when creating a new skill, refactoring an existing one, reviewing skill quality, or deciding how to split content into reference files.
user-invocable: true
metadata:
  version: "2026-06-22"
---

# Skill Creation

This skill covers how to write, structure, and improve agent skills in the `well-cafe-skills` marketplace. Use it to keep skills consistent, discoverable, and maintainable as the collection grows.

## Quick rules

- **SKILL.md = slim navigator.** Operational instructions + quick reference inline. Deep reference content goes in `references/*.md`.
- **Descriptions are trigger phrases**, not summaries. They control when Claude loads the skill.
- **One concept per reference file.** Name files with a category prefix: `core-`, `gotchas-`, `efficiency-`.
- **Prose should tell Claude what to *do*, not what things *are*.** Reference files cover the "what"; SKILL.md covers the "when/how".

## SKILL.md structure

```
---
name: skill-name
description: What it does. Use when <trigger phrases listing concrete user situations>.
user-invocable: true          # omit if Claude-only
allowed-tools: [...]          # omit if unrestricted
metadata:
  version: "YYYY-MM-DD"       # date of last meaningful edit
---

# Title

One-paragraph context: what this skill covers and why it exists.

## When to use
(optional — only if description alone isn't enough)

## Quick reference
(inline table or examples for the most common 20% of use cases)

## [Main operational sections]
(instructions Claude should follow — imperative, present-tense)

## References

| Topic | Description | Reference |
|-------|-------------|-----------|
| ...   | ...         | [name](references/name.md) |
```

The reference table is the last section. Everything above it should be self-contained enough that most invocations don't need to open a reference file.

## Description field

The description is how Claude decides whether to load the skill. Write it in two parts:

1. A one-phrase summary of what the skill does
2. "Use when..." followed by a comma-separated list of concrete situations

**Good:** `"Inbox processing — reads _Inbox and proposes where each item should be filed. Use when inbox has accumulated items, after a capture session, or when the user wants to file unprocessed notes."`

**Bad:** `"Processes the inbox."` (no triggers) or a long paragraph (noisy, hard to scan)

Trigger phrases should match how the user would actually phrase a request, not internal jargon.

## Reference files

When a section in SKILL.md exceeds ~30 lines, or covers a distinct sub-topic, extract it to `references/`.

File naming: `{category}-{topic}.md`
- `core-cli-patterns.md` — primary usage patterns
- `gotchas-property-types.md` — known failure modes
- `efficiency-parallelism.md` — performance/batching guidance

Each reference file has its own frontmatter:

```markdown
---
name: topic-name
description: One line — used if Claude ever loads this file standalone.
---

# Topic Name

...content...
```

Keep one concept per file. If two topics always appear together, they can share a file; if they're ever useful independently, split them.

## Dependent skills (the "Before starting" pattern)

When a skill requires another skill to run first, say so explicitly at the top of the main content section:

```markdown
## Before starting

**Invoke the `plugin:skill-name` skill before proceeding.** [One sentence on what it provides.]
If it is not available, ask the user to install `plugin-name`.
```

This is the correct sharing mechanism — not file imports, not symlinks. Skill invocation is how context is shared between skills.

## allowed-tools

List only tools the skill actually needs. Use the most specific glob that works.

```yaml
# Prefer specific globs over broad wildcards
allowed-tools: Read, Bash(obsidian read *), Bash(obsidian files *)

# Not: Bash(*) unless the skill genuinely needs unrestricted shell
```

Read-only skills should omit write-capable tools (`obsidian create`, `obsidian property:set`, etc.) unless the skill explicitly requires writes with user approval.

## References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Worked examples | Annotated before/after for a real skill in this marketplace | [writing-examples](references/writing-examples.md) |
| Checklist | Quick checklist for reviewing a skill before committing | [review-checklist](references/review-checklist.md) |
