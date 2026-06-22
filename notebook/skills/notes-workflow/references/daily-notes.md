---
name: notes-workflow-daily-notes
description: How to access past daily notes — the limits of daily:read and the folder-listing workaround.
---

# Daily Notes

`obsidian daily:read` and `obsidian daily:path` only work for today. Passing a `date=` argument always returns today's note regardless of the value — do not rely on it for history.

To read recent daily notes, list the folder and filter by filename. Filenames are `YYYY-MM-DD.md` so they sort chronologically:

```bash
# Get the last N daily notes
obsidian files folder="00 Daily" | sort | tail -7
```

Then read each by path:

```bash
obsidian read path="00 Daily/2026-03-25.md"
```
