---
name: notes-organize
description: Inbox processing — reads _Inbox and proposes where each item should be filed or acted on. Use when the inbox has accumulated items, after a capture session, or when the user says "process my inbox" / "clear my inbox". Read-only unless the user approves proposed actions.
user-invocable: true
allowed-tools: Read, Bash(obsidian read *), Bash(obsidian search *), Bash(obsidian files *), Bash(obsidian folders *), Bash(obsidian file *), Bash(obsidian tags *), Bash(obsidian backlinks *), Bash(obsidian base:query *)
metadata:
  version: "2026-06-28"
---

# Notes — Organize

An inbox processing skill. Read `_Inbox`, propose actions, wait for approval before touching anything.

## Before starting

**Invoke the `notebook:notes-workflow` skill before proceeding.** It verifies the vault connection, reads `VAULT.md` for conventions, and provides the CLI patterns this skill depends on. If it is not available, ask the user to install the `notebook` plugin.

## What this skill does

1. Get inbox items — see VAULT.md for how to access the inbox
2. Read each one
3. Research each item in the vault before proposing an action
4. For each item, propose one of: **promote** (file to a specific location), **expand** (turn into a proper note first), **link** (it belongs near an existing note), or **delete** (nothing here worth keeping)
5. Present the full proposal — including destination, metadata, and links — to the user before doing anything
6. Execute only what the user approves

## Research before proposing

Before proposing a destination for any inbox item, search for related existing notes:

```bash
obsidian search query="relevant term" limit=5
```

Use these results to confirm the right destination, identify notes that should link to or from the inbox item, and determine whether the item is a refinement of something existing or genuinely new.

## Handling ambiguity

Inbox notes are often rough captures — voice memo transcripts, one-liners, half-formed thoughts. If a note's content or intent is unclear, ask the user before proposing a destination. A wrong filing proposal is worse than no proposal. When in doubt, flag it as needing clarification rather than guessing.

## Splitting multi-idea notes

A single inbox note may contain multiple distinct ideas that deserve their own notes. Before proposing a single move, ask: does each idea have enough identity to stand alone? If so, propose splitting — give each fragment its own destination and name — rather than filing the note as-is.

## Filing proposals

For each item, name the exact destination path, explain why in one sentence, and if it could go in more than one place, say so and give a recommendation.

For destination decisions, link proposals, and frontmatter conventions, follow the shared filing logic: [filing](../../references/filing.md).

## Read-only by default

Present the full proposal as a list. Ask the user to confirm before executing any moves, renames, or edits. Execute approved actions one at a time so the user can follow along.
