---
name: notes-reflect
description: Periodic review of the vault — synthesises recent daily notes, surfaces themes, summarises project activity, and identifies open questions. Read-only unless the user asks to create or modify notes.
user-invocable: true
allowed-tools: Read, Bash(obsidian read *), Bash(obsidian search *), Bash(obsidian search:context *), Bash(obsidian files *), Bash(obsidian tags *), Bash(obsidian backlinks *), Bash(obsidian outline *)
---

# Notes — Reflect

A periodic review skill. Read the vault, synthesise, present. Do not create or modify anything unless the user explicitly asks.

## What this skill does

1. In parallel: get recent daily notes (`obsidian files folder="00 Daily" | sort | tail -7`) and list projects (`obsidian files folder="01 Projects"`)
2. Read the daily notes and all relevant project notes
3. Identify themes, recurring topics, open questions, and wins
4. Present a structured synthesis to the user

## Dependencies

This skill is part of the `obsidian-workflow` plugin. The `obsidian-workflow` skill must be installed and its setup steps followed — including reading `CLAUDE.md` — before using this skill.

## Before starting

Read `CLAUDE.md` at the vault root for vault conventions.

## Reading daily notes

`obsidian daily:read date=` does not work for past dates — it always returns today's note regardless of the date argument. Do not use it for history.

Instead, get recent daily notes in one shot — filenames are `YYYY-MM-DD.md` so they sort chronologically:

```bash
# Last 7 days
obsidian files folder="00 Daily" | sort | tail -7

# Or adjust tail count for a different period
```

Then read each returned path:

```bash
obsidian read path="00 Daily/YYYY-MM-DD.md"
```

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
