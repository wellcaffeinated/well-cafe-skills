---
name: notes-setup-output-structure
description: The standardized vault container notes-setup writes — CLAUDE.md, 99 Meta/ docs, Templates/, optional _Dashboard/ — and the rules for what goes where.
---

# Output structure

The structure is the *user's*; only the documents that describe it are fixed. Whatever scheme emerged from the interview must be written where the agent reads it, or it doesn't exist.

## The split

- **Portable "how to operate a vault"** (CLI mechanics, safe writes, query syntax) → stays in the `notes-workflow` skill. Never in vault docs.
- **Vault-specific "how *this* vault is organized"** → into the vault, tiered by how often it's needed.

## The container

```
<vault>/
  CLAUDE.md                 # folder map + inviolable rules + index — ALWAYS loaded
  99 Meta/
    conventions/            # principles spanning all note types
    types/                  # one note type each, fully encapsulated
    workflows/              # vault-specific runbooks
  Templates/                # one per significant type — source of truth for frontmatter
  _Dashboard/               # optional Bases for high-frequency queries
```

### `CLAUDE.md` — primary, always loaded

Only what a *majority* (>~60%) of interactions need. Keep it short:
- **Folder map** — each folder + one line on what it means.
- **Inviolable rules** — a few hard constraints (e.g. "never overwrite", "drafts go to staging").
- **Index** — links into every `99 Meta/` doc and each Base, so the agent can find detail on demand.

### `99 Meta/` — supplementary, read on demand

- `conventions/` — principles across types: how to choose a folder, property conventions, capture/processing.
- `types/` — one type each: its location, frontmatter, type-specific behavior.
- `workflows/` — step-by-step routines particular to this user.

## Authoring rules

1. **General doc holds the *rule*; type doc holds the *instance*. Link, don't duplicate.** `where-things-go.md` says *how* to pick a folder; `bookmarks.md` says bookmarks live in folder X and links back.
2. **CLAUDE.md only earns info a majority of interactions need.** Else it's a supplementary doc, named so its scope is self-evident (`where-things-go.md`, not `notes-2.md`).
3. **A type earns its own `types/` doc only with real machinery** — a dedicated location, special frontmatter, or its own lifecycle/dashboard. Otherwise it's a one-liner in a conventions doc (promote later if it accumulates rules). Bookmark/project/area usually qualify; idea/log/meeting/person usually don't.
4. **`99 Meta/` docs are agent-facing reference** — tag as a queryable collection (`type: reference`, `tags: [meta, system]`), mark `ai: true` if generated. Create a folder by creating a note in it.
5. **`Templates/` is the source of truth for frontmatter.** Type docs point at the template, never restate the YAML — so they can't drift.
6. **Dashboards optional → Bases in `_Dashboard/`** for the highest-frequency queries the user named. Start with one or two they'll actually open; list them in the CLAUDE.md index.

## Scaffolds

Starting points to fill in (`{{placeholders}}`), not drop in verbatim:
- `assets/templates/CLAUDE.md.template` — the always-loaded index.
- `assets/templates/type-doc.template.md` — a `99 Meta/types/` doc.

## Delivering it — stage locally, then drag in

Build the whole structure as real files in a **local staging folder that mirrors the vault root**, so the user sees exactly what will exist before anything touches the vault:

```
./vault-setup/                 # staging — mirrors the vault root
  CLAUDE.md
  99 Meta/
    conventions/   types/   workflows/
  Templates/
  _Dashboard/                  # .base files (plain YAML/text)
```

Use the Write tool for these — no vault CLI, no per-file prompts, fully previewable. Start from the scaffolds above and fill the `{{placeholders}}`. Show the user the tree and let them open any file.

Then offer two ways to install:

1. **Drag-in (recommended).** *"Open `./vault-setup/` and drag its **contents** — not the folder itself — into your vault's root folder (in Finder/Explorer, or straight into Obsidian's file list). You'll see precisely what you're getting, and you can leave out anything you don't want."* Safe and reversible — nothing lands until they act, and they can drop individual files.
2. **Agent places them.** If they'd rather, write each file into the vault via the CLI (`create`; make a folder by creating a note inside it). Each write prompts. Use heredoc-quoted content for frontmatter/wikilinks (see `notes-workflow`).

**Verify after install** (either path): confirm the docs resolve (`obsidian file file="CLAUDE.md"`), then run a `base:query` to confirm the Bases work (step 7).
