---
name: notes-surprise
description: Serendipity engine — pulls random notes from across the vault, finds unexpected connections and patterns, and surfaces ideas the user wouldn't have looked for. Read-only unless the user asks to create or modify notes.
user-invocable: true
allowed-tools: Read, Bash(obsidian read *), Bash(obsidian search *), Bash(obsidian files *), Bash(obsidian tags *), Bash(obsidian backlinks *), Bash(obsidian links *), Bash(obsidian outline *)
---

# Notes — Surprise

A serendipity skill. Pull random notes, find unexpected threads, present connections. Do not create or modify anything unless the user explicitly asks.

## What this skill does

1. Pull several random notes from different parts of the vault using `obsidian random:read` — run these calls in parallel since they're independent
2. Read each one fully
3. Look for unexpected connections, resonances, or tensions between them
4. Surface anything that seems generative — a question, a contradiction, a pattern the user hasn't noted

## Dependencies

This skill is part of the `obsidian-workflow` plugin. The `obsidian-workflow` skill must be installed and its setup steps followed — including reading `CLAUDE.md` — before using this skill.

## Before starting

Read `CLAUDE.md` at the vault root for vault conventions.

## Handling ambiguity

Notes may be fragmentary, shorthand, or context-dependent. If a note is too sparse to interpret, skip it and pull another rather than guessing. If a connection you've surfaced relies on an interpretation of a messy note, flag that uncertainty to the user when presenting it.

## Approach

Favour surprise over safety. The goal is not to find obvious connections but to bridge distant ideas — a physics note and a dance note, a project concern and a resource, an old archived idea and a current area. Treat the vault as a mind and look for the subconscious links.

Pull at least 4-6 notes to give enough surface area for unexpected connections. Vary the source folders — don't pull only from one area.

## Presenting findings

- Lead with the most unexpected or generative connection
- Be concrete — quote the specific phrases or ideas that sparked the connection
- Suggest what a note bridging these ideas might contain, but don't create it unless asked
- Invite the user to pull another set if nothing landed

## Read-only by default

If the user wants to capture a connection as a new note, ask where they'd like it filed before creating anything.
