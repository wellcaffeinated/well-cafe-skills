---
name: skill-creation-examples
description: Annotated before/after examples illustrating how to apply skill-creation guidelines.
---

# Worked Examples

## Example 1: Description — adding trigger phrases

**Before:**
```yaml
description: Inbox processing — reads the inbox, understands each item, and proposes where each should be filed or what should be done with it. Read-only unless the user approves proposed actions.
```

**After:**
```yaml
description: Inbox processing — reads the inbox and proposes where each item should be filed or acted on. Use when the inbox has accumulated items, after a capture session, or when the user says "process my inbox" / "clear my inbox". Read-only unless the user approves.
```

What changed: the summary stayed the same; a "Use when..." clause was added listing the concrete situations a user would be in when this skill is relevant. Trigger phrases match natural user phrasing, not internal terminology.

---

## Example 2: Splitting a prose-heavy SKILL.md

A skill that starts as a single file often accumulates sections as it matures. Once the body exceeds ~100 lines, the context overhead starts to outweigh the convenience.

**Before** — one file covering everything:

```
## Gotchas

- Tool X writes a string unless told otherwise. Pass type= for the real type.
- Command Y does not create the destination folder. Create it first.
- Overwrites using piped content need absolute paths.

## Efficiency

Parallelise read operations. Independent reads can all run in parallel.
Never parallelise write operations.

## Common commands

# Read a file
tool read path="..."

# Search
tool search query="..."
```

**After** — slim SKILL.md with a reference table:

```markdown
## References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Common commands | Quick reference for the most-used operations | [core-commands](references/core-commands.md) |
| Gotchas | Silent failures and workarounds | [gotchas-silent-failures](references/gotchas-silent-failures.md) |
| Efficiency | Parallelization rules and batching patterns | [efficiency-parallelism](references/efficiency-parallelism.md) |
```

The SKILL.md body keeps only what must load on every invocation: setup verification, conventions, and the "Before starting" dependency. Everything else moves to references.

---

## Example 3: allowed-tools scope

The test for an `allowed-tools` list: can you point to a specific behaviour in the SKILL.md that justifies each entry?

**Too broad:**
```yaml
allowed-tools: Read, Bash(*)
```
`Bash(*)` allows any shell command. If the skill only reads files and runs one specific CLI tool, this grants far more than needed.

**Appropriately scoped:**
```yaml
allowed-tools: Read, Bash(tool read *), Bash(tool search *), Bash(tool files *)
```
Each glob matches exactly what the SKILL.md instructs Claude to run. Write operations (`tool create`, `tool property:set`) are absent because this skill is read-only — writes require explicit user approval handled in a different skill.

The pattern: start with the minimum, add entries only when SKILL.md prose makes it clear why they're needed.
