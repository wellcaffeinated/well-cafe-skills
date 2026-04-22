---
name: notes-reflect
description: Periodic review of the vault — synthesises recent daily notes, surfaces themes, summarises project activity, and identifies open questions. Read-only unless the user asks to create or modify notes.
user-invocable: true
allowed-tools: Read, Bash(obsidian read *), Bash(obsidian search *), Bash(obsidian search:context *), Bash(obsidian files *), Bash(obsidian tags *), Bash(obsidian backlinks *), Bash(obsidian outline *), Bash(obsidian base:query *)
---

# Notes — Reflect

A periodic review skill. Read the vault, synthesise, present. Do not create or modify anything unless the user explicitly asks.

## What this skill does

1. In parallel: query recent daily note activity and project state — see CLAUDE.md for how to access each
2. Read individual daily notes and relevant project notes in full for detail
3. Identify themes, recurring topics, open questions, and wins
4. Present a structured synthesis to the user

## Before starting

**Invoke the `notebook:obsidian-workflow` skill before proceeding.** It verifies the vault connection, reads `CLAUDE.md` for conventions, and provides the CLI patterns this skill depends on. If it is not available, ask the user to install the `well-cafe-notebook` plugin.

## Handling ambiguity

Daily notes and project notes are often messy and lack context. If a note's meaning or intent is unclear, don't guess — flag it when presenting the synthesis and ask the user what they meant or what the outcome was. This is especially useful for single-line entries or cryptic shorthand.

## Suggested structure for the reflection output

- **What you worked on** — projects and topics that appeared across the week
- **Themes** — patterns or ideas that recurred
- **Open questions** — things that came up but weren't resolved
- **Wins** — things that got done
- **Possible next actions** — surfaced from context, not prescriptive

## Read-only by default

Present findings conversationally. If the user wants a weekly reflection note created, ask where they'd like it filed before creating anything.
