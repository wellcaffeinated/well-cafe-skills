---
name: notes-daily
description: Daily-note processing — works through unprocessed daily notes, extracts anything in the prose worth capturing permanently, files it to the right home, and marks each note processed. Use when processing journal backlog, after a stretch of daily note capture, or when the user asks to "process my daily notes" / "catch up on my journal". Read-only unless the user approves proposed actions.
user-invocable: true
allowed-tools: Read, Bash(obsidian read *), Bash(obsidian search *), Bash(obsidian files *), Bash(obsidian folders *), Bash(obsidian file *), Bash(obsidian tags *), Bash(obsidian backlinks *), Bash(obsidian base:query *)
metadata:
  version: "2026-06-22"
---

# Notes — Daily

Work through the backlog of unprocessed daily notes. For each one, decide whether anything in it deserves to be captured somewhere more permanent, file what does, and mark the note processed. Read-only unless the user approves an action.

## Before starting

**Invoke the `notebook:notes-workflow` skill before proceeding.** It verifies the vault connection, reads `CLAUDE.md` for conventions, and provides the CLI patterns (and gotchas) this skill depends on. If it is not available, ask the user to install the `well-cafe-notebook` plugin.

## What this skill does

1. Get the unprocessed daily notes — see CLAUDE.md for the Daily base / Unprocessed view
2. Read them, newest first
3. For each, separate **tasks** from **prose** (see below), and judge whether the prose holds anything durable
4. Propose where each durable item should go
5. On approval, file it, then mark the daily `processed`
6. Mark notes with nothing durable left straight to `processed`

## Checkboxes are already captured — only prose matters

Daily notes mix two kinds of content, and the distinction is the most important thing in this skill:

- **Checkbox lines** (`- [ ]` / `- [x]`) are Obsidian Tasks. They already persist through the user's task queries — they are captured *by definition*. **Never re-capture a checkbox item into a note**, and don't treat an open task as an uncaptured idea.
- **Prose** — the "what moved / what's stuck" reflections and the scratchwork links — is the only capture material. Durable insights, decisions, and references hide here.

So when judging a daily, read past the task lists and look only at the prose.

## What's worth capturing (and what isn't)

For each piece of prose, decide:

- **Project progress / status / decisions** → roll into the relevant project note, following whatever structure that note already uses.
- **A stray reference, link, or idea** → file it to the project or area it serves. Annotate links with *why they matter*, not just the URL.
- **A cross-project connection** → add it to the note it informs.
- **Transient day-intentions** ("need to get back to X", "should check on Y") → leave them. They're scheduling thoughts, not durable knowledge.
- **Something with no substance** ("chatted with N about ideas", no detail) → flag it to the user; do not invent content to capture.

**Always check whether it's already captured** before adding anything — search the likely home first.

## Filing

For destination decisions, link proposals, and frontmatter conventions, follow the shared filing logic: [filing](../../references/filing.md). Prefer **additive** edits — `append`, `prepend`, or a new section — over overwriting existing prose. Never rewrite the user's words unprompted.

## Marking processed

A daily is "processed" once everything durable in its prose has a home (or there was nothing durable to begin with).

```bash
obsidian property:set name="processed" value="true" type="checkbox" path="00 Daily/YYYY-MM-DD.md"
```

`type=checkbox` is required — without it the value is stored as a string and the Unprocessed view won't drop the note (see the notes-workflow gotchas). After a batch, re-run the Unprocessed query to confirm the notes actually cleared.

**Only mark a daily processed when *all* of its durable prose is captured.** A single note often holds several unrelated threads; if one is handled and another isn't, leave the note unprocessed and say which thread remains.

## Pace and approval

Work in clusters — group the notes that feed one project or theme so related fragments get captured together — but take one cluster per step. Present the proposal, wait for approval, then execute writes one at a time. Batch-marking clearly-empty dailies as processed is the one move the user may pre-approve.

## Read-only by default

Propose before you touch anything. Filing, rolling status into project notes, and marking processed are all writes — present them and get a go-ahead before executing.
