---
name: notes-organize
description: Inbox processing — reads _Inbox, understands each item, and proposes where each should be filed or what should be done with it. Read-only unless the user approves proposed actions.
user-invocable: true
allowed-tools: Read, Bash(obsidian read *), Bash(obsidian search *), Bash(obsidian files *), Bash(obsidian folders *), Bash(obsidian tags *), Bash(obsidian backlinks *), Bash(obsidian base:query *)
---

# Notes — Organize

An inbox processing skill. Read `_Inbox`, propose actions, wait for approval before touching anything.

## What this skill does

1. Get inbox items — see CLAUDE.md for how to access the inbox
2. Read each one
3. Research each item in the vault before proposing an action
4. For each item, propose one of: **promote** (file to a specific location), **expand** (turn into a proper note first), **link** (it belongs near an existing note), or **delete** (nothing here worth keeping)
5. Present the full proposal — including destination, metadata, and links — to the user before doing anything
6. Execute only what the user approves

## Dependencies

This skill is part of the `well-cafe-notebook` plugin. The `obsidian-workflow` skill must be installed and its setup steps followed — including reading `CLAUDE.md` — before using this skill.

## Before starting

Read `CLAUDE.md` at the vault root for vault conventions.

## Research before proposing

Before proposing a destination for any inbox item, run a contextual search to find related existing notes:

```bash
obsidian search query="relevant term" limit=5
```

Use these results to:
- Confirm the right destination (does a note already cover this topic?)
- Identify notes that should link to or from the inbox item
- Determine whether the item is a refinement of something existing or genuinely new

## Handling ambiguity

Inbox notes are often rough captures — voice memo transcripts, one-liners, half-formed thoughts. If a note's content or intent is unclear, ask the user before proposing a destination. A wrong filing proposal is worse than no proposal. When in doubt, flag it as needing clarification rather than guessing.

## Splitting multi-idea notes

A single inbox note may contain multiple distinct ideas that deserve their own notes. Before proposing a single move, ask: does each idea have enough identity to stand alone? If so, propose splitting — give each fragment its own destination and name — rather than filing the note as-is. Scratchwork often lumps unrelated captures together; separation preserves context and makes future discovery easier.

## Exploring destination structure

Before proposing a specific path, check whether the destination folder has subfolders that are more appropriate than the top level — see CLAUDE.md for folder paths. File to the most specific applicable location. Prefer an existing subfolder over creating a new one unless the item genuinely doesn't fit anywhere current.

## Filing proposals

When proposing where to file something, be specific:
- Name the exact destination path
- Explain why in one sentence
- If it could go in more than one place, say so and give a recommendation

Use the PARA logic from `CLAUDE.md` for folder paths:
- Does it have a finish line? → Projects folder
- Ongoing responsibility? → Areas folder
- Reference, no obligation? → Resources folder
- Done or dormant? → Archive folder

When proposing where to file something, also propose **links**:
- If an existing note clearly relates, propose adding a wikilink in one or both directions
- For bookmarks, identify the project or area most likely to benefit from discovering this resource
- State the links explicitly: "link from [[Project X]]" or "add `related: [[Resource Y]]` to frontmatter"

Every filing proposal must include suggested frontmatter. Use the type values and field conventions from `CLAUDE.md`. At minimum propose `type:` and `tags:`. For bookmarks also propose `source:`. For notes being promoted to projects or areas, propose `outcome:` or `purpose:` respectively. Present the metadata inline with the proposal so the user can approve or edit before execution.

## Read-only by default

Present the full proposal as a list. Ask the user to confirm before executing any moves, renames, or edits. Execute approved actions one at a time so the user can follow along.
