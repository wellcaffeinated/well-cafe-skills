---
name: notes-workflow-daily-notes
description: How to access daily notes — prefer the CLI daily: subcommands when the Daily Notes plugin is enabled, fall back to vault meta info, and how to reach past notes. Never hardcode the daily folder.
---

# Daily Notes

Reach daily notes through the CLI, and **never hardcode the daily folder** — discover it, because every vault configures it differently.

## Prefer the `daily:` subcommands (Daily Notes plugin)

When Obsidian's **Daily Notes** core plugin (id `daily-notes`) is enabled, the CLI exposes subcommands that already know the vault's configured daily folder and filename format:

- `obsidian daily:read` — read today's note
- `obsidian daily:path` — print today's note path
- `obsidian daily:append` / `daily:prepend` — add to today's note
- `obsidian daily` — open today's note

Confirm it's enabled before relying on them:

```bash
obsidian plugins:enabled filter=core    # is `daily-notes` listed?
```

These all target **today** — there is no `date=` parameter, so they can't fetch a past day. Their value for *processing* is discovery: `obsidian daily:path` reveals both the daily **folder** and the **filename format** this vault uses, so you learn where dailies live and how they're named instead of guessing. The format is a per-vault setting — often `YYYY-MM-DD`, but it can be anything (`DD-MM-YYYY`, `MMMM Do YYYY`, or dates nested into subfolders) — so always read it from `daily:path` rather than assuming.

## Reading past daily notes

`daily:read` only reaches today. For history, take the folder and naming pattern from `daily:path` (or the vault meta, below), list the folder, and read by path:

```bash
obsidian daily:path                           # e.g. "00 Daily/2026-06-28.md" → folder "00 Daily", format "YYYY-MM-DD"
obsidian files folder="00 Daily" | sort | tail -7
obsidian read path="00 Daily/2026-03-25.md"
```

Two things to keep in mind: the `00 Daily` / `YYYY-MM-DD` above are only *examples* of what `daily:path` might return — use whatever it actually reports. And the `sort | tail` trick only lands on the most recent notes when the format is **lexically date-sortable** (which `YYYY-MM-DD` is); if the vault uses a non-sortable format or nests dates into subfolders, sort by the parsed date or fall back to file mtime instead.

## Fallback: Daily Notes plugin disabled

If the plugin is off, the `daily:` subcommands won't resolve. Find where dailies live from the vault's own meta info — `CLAUDE.md` (folder map) or `_Meta/` — which the setup skill records. Then list and read by path as above. Still no hardcoded folder name: read it from the vault.
