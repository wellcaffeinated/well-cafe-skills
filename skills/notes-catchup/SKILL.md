---
name: notes-catchup
description: Weekly briefing — checks daily notes and project activity to surface what's been neglected, flag what needs attention this week, and give an opinionated heads-up on what might fall through the cracks. Like a secretary giving a Monday morning briefing.
user-invocable: true
allowed-tools: Read, Bash(obsidian read *), Bash(obsidian search *), Bash(obsidian files *), Bash(obsidian file *), Bash(obsidian daily:read *), Bash(obsidian backlinks *), Bash(obsidian outline *)
---

# Notes — Catchup

A weekly briefing skill. The goal is not to summarise what's been active — it's to surface what's been neglected and prepare the user for the week ahead. Read-only unless the user asks otherwise.

## Dependencies

This skill is part of the `well-cafe-notebook` plugin. The `obsidian-workflow` skill must be installed and its setup steps followed — including reading `CLAUDE.md` — before using this skill.

## Before starting

Read `CLAUDE.md` at the vault root for vault conventions.

## Reading daily notes

`obsidian daily:read date=` and `obsidian daily:path date=` do not work for past dates — they always return today's note regardless of the date argument. Do not use them for history.

Instead, get the last 7 daily notes in one shot — filenames are `YYYY-MM-DD.md` so they sort chronologically:

```bash
obsidian files folder="00 Daily" | sort | tail -7
```

Then read each returned path:

```bash
obsidian read path="00 Daily/YYYY-MM-DD.md"
```

If the vault has sparse daily note history, this naturally handles it — you only read notes that actually exist.

## What this skill does

1. In parallel: get recent daily notes (`obsidian files folder="00 Daily" | sort | tail -7`), list Projects (`obsidian files folder="01 Projects"`), and list Areas (`obsidian files folder="02 Areas"`)
2. Read the daily notes; batch-check modification times for all project home notes in a single loop
3. Read all project and Area notes in full
4. Cross-reference: which projects appear in daily notes? Which don't?
5. Produce a briefing

## The briefing

Cover everything, but weight the presentation toward gaps. Structure:

- **Lagging projects** — projects with no recent daily note mentions and stale file modification times. Flag these specifically.
- **At risk this week** — deadlines approaching, or projects that haven't been touched but have a deadline set
- **Areas going quiet** — areas with no recent activity that might need a check-in
- **Active this week** — what has been worked on, briefly — this matters too and gives context for the gaps
- **Prepared for this week** — based on what's been active and what's coming, what should the user expect to work on

## The secretary standard

Be opinionated. Don't just list — say what matters. Active work is worth acknowledging but doesn't need elaboration — the user knows what they've been doing. Gaps and risks deserve the most attention and the plainest language. If a project hasn't been touched in two weeks, say so. If a deadline is close and there's been no activity, flag it as a risk. The user should finish reading the briefing with a clear sense of what they might have let slip, what's coming, and what deserves attention first.

## Handling ambiguity

If a project note is sparse or its current state is unclear, note that it needs a status check rather than guessing. Ask the user if they want to clarify the state of anything flagged.

## Read-only by default

Present the briefing and invite the user to act on any item. Do not move, edit, or create notes unless asked.
