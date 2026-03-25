---
name: notes-organize
description: Inbox processing — reads _Inbox, understands each item, and proposes where each should be filed or what should be done with it. Read-only unless the user approves proposed actions.
user-invocable: true
allowed-tools: Read, Bash(obsidian read *), Bash(obsidian search *), Bash(obsidian files *), Bash(obsidian folders *), Bash(obsidian tags *), Bash(obsidian backlinks *)
---

# Notes — Organize

An inbox processing skill. Read `_Inbox`, propose actions, wait for approval before touching anything.

## What this skill does

1. List all files currently in `_Inbox`
2. Read each one
3. For each item, propose one of: **promote** (file to a specific location), **expand** (turn into a proper note first), **link** (it belongs near an existing note), or **delete** (nothing here worth keeping)
4. Present the full proposal to the user before doing anything
5. Execute only what the user approves

## Dependencies

This skill is part of the `obsidian-workflow` plugin. The `obsidian-workflow` skill must be installed and its setup steps followed — including reading `CLAUDE.md` — before using this skill.

## Before starting

Read `CLAUDE.md` at the vault root for vault conventions.

## Handling ambiguity

Inbox notes are often rough captures — voice memo transcripts, one-liners, half-formed thoughts. If a note's content or intent is unclear, ask the user before proposing a destination. A wrong filing proposal is worse than no proposal. When in doubt, flag it as needing clarification rather than guessing.

## Filing proposals

When proposing where to file something, be specific:
- Name the exact destination path
- Explain why in one sentence
- If it could go in more than one place, say so and give a recommendation

Use the PARA logic from `CLAUDE.md`:
- Does it have a finish line? → `01 Projects/`
- Ongoing responsibility? → `02 Areas/`
- Reference, no obligation? → `03 Resources/`
- Done or dormant? → `04 Archive/`

## Read-only by default

Present the full proposal as a list. Ask the user to confirm before executing any moves, renames, or edits. Execute approved actions one at a time so the user can follow along.
