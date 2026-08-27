---
name: notes-setup-plugins
description: Plugin referrals for notes-setup — one line per need, linking to official Obsidian docs only. Suggest a plugin only against an elicited need, never as a starter pack.
---

# Plugins — referral, not tutorial

Two guardrails:

1. **Suggest only against an elicited need.** A plugin answers "I want X to feel effortless." If the interview didn't surface the need, don't surface the plugin. Four plugins someone uses beats fourteen they forgot.
2. **Plugins are almost entirely for the human reader.** The agent reads markdown/properties/folders regardless of plugins. Two exceptions matter: plugins that change *what gets written to the file* (Templater filling frontmatter, Tasks' date syntax) — the agent reads that residue — and **Daily Notes / Periodic Notes**, which *enable the CLI's `daily:` subcommands*, letting the agent resolve and read the daily note directly instead of guessing its folder.

Name the plugin, say what need it serves, link its official docs. Don't explain configuration; Obsidian's plugin browser and each plugin's docs do that.

## Need → plugin

| Elicited need | Plugin | Why (one line) |
|---------------|--------|----------------|
| Right note, right place, right frontmatter, one keystroke | **Templater** (+ **QuickAdd**) | Makes queried properties automatic *at creation* — the load-bearing one if the agent will query the vault. |
| Track to-dos across notes — due dates, recurrence, what's due today | **Tasks** | Stores metadata as inline markdown (`📅 2026-07-01`) the agent can also read — doubles as an agent-legible due-date axis. |
| In-app dashboards / tables of notes | **Bases** (core, first) | Ships with Obsidian, queries properties — same retrieval layer the agent uses. Reach for **Dataview** only when Bases can't do it (non-table views, computed logic). |
| One page per day — journaling / daily capture | **Daily Notes** (core; **Periodic Notes** instead if they also want weekly/monthly) | The one referral that also serves the *agent*: enabling it gives the CLI's `daily:` commands. Point its new-file **folder** and optional **template** at the vault's daily folder so capture, the plugin, and the agent agree. The **date format** is the user's choice — recommend a lexically-sortable one like `YYYY-MM-DD` (so dailies list chronologically), but whatever they pick, record it; it's read back via `daily:path`, never assumed. |
| A clickable calendar over those daily notes | **Calendar** | Purely human navigation — a month grid that opens each day's note. |
| Stay consistently formatted without thinking | **Linter** | Auto-normalizes frontmatter/formatting on save — human-side janitor for the consistency the agent depends on. |
| Think visually / diagrams & sketches | **Excalidraw** | Purely human-facing — don't let load-bearing meaning live only in a drawing. |

## Official docs

- Obsidian Help — https://help.obsidian.md
- Community plugins (in-app) — https://obsidian.md/plugins
- Bases (core) — https://help.obsidian.md/bases
- Templater — https://silentvoid13.github.io/Templater/
- QuickAdd — https://quickadd.obsidian.guide/
- Tasks — https://publish.obsidian.md/tasks/
- Dataview — https://blacksmithgu.github.io/obsidian-dataview/
- Periodic Notes — https://github.com/liamcain/obsidian-periodic-notes
- Calendar — https://github.com/liamcain/obsidian-calendar-plugin
- Linter — https://platers.github.io/obsidian-linter/
- Excalidraw — https://github.com/zsviczian/obsidian-excalidraw-plugin

## Fallback line

If the user just wants to be told: *"Templater + QuickAdd for frictionless capture, Tasks if you track to-dos, Bases for dashboards — add the rest only when you feel the specific need."*
