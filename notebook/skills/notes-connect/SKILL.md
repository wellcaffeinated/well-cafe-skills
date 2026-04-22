---
name: notes-connect
description: Given a note or topic, searches the vault for related notes that aren't yet linked and surfaces potential connections. Read-only unless the user asks to add links.
user-invocable: true
allowed-tools: Read, Bash(obsidian read *), Bash(obsidian search *), Bash(obsidian search:context *), Bash(obsidian files *), Bash(obsidian tags *), Bash(obsidian backlinks *), Bash(obsidian links *), Bash(obsidian outline *)
---

# Notes — Connect

A connection-finding skill. Given a starting point, explore the vault for related notes that aren't yet linked. Read-only unless the user asks to add links.

## What this skill does

1. Identify the starting note — use the active file if the user doesn't specify one
2. Read it fully to understand its ideas, themes, and terminology
3. Search the vault for notes that relate by topic, terminology, or idea — not just by tag
4. Check existing links and backlinks to avoid surfacing connections that already exist
5. Present the most meaningful unlinked connections with a brief explanation of why each is relevant

## Before starting

**Invoke the `notebook:obsidian-workflow` skill before proceeding.** It verifies the vault connection, reads `CLAUDE.md` for conventions, and provides the CLI patterns this skill depends on. If it is not available, ask the user to install the `well-cafe-notebook` plugin.

Check the active file with `obsidian file` if no note is specified.

## Handling ambiguity

If the starting note is sparse or its intent is unclear, ask the user what it's about before searching for connections — a wrong interpretation will produce irrelevant results. Similarly, if a potential connection relies on a generous reading of a messy note, flag that uncertainty rather than presenting it as a confident match.

## Approach

Go beyond tag matching. A note about Finsler geometry might connect to a note about spacetime or physics tools. A song idea might connect to a worldbuilding note. Look for conceptual overlap, not just keyword overlap.

Rank suggestions by how meaningful the connection is, not how obvious. Surface the non-obvious ones first.

## Presenting findings

For each suggested connection:
- Name the note and its location
- Explain in one sentence why it connects
- Quote the specific phrase or idea that bridges them

After the list, always offer a ready-to-paste "See Also" section the user can approve and add to the note:

```
## See Also
- [[Note One]]
- [[Note Two]]
- [[Note Three]]
```

## Read-only by default

If the user approves the "See Also" section (or a subset of it), append it to the note. Confirm which links to include before writing.
