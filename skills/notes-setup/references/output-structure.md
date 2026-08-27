---
name: notes-setup-output-structure
description: The standardized vault container notes-setup writes — VAULT.md, _Meta/ docs, Templates/, optional _Dashboard/ — and the rules for what goes where.
---

# Output structure

The structure is the *user's*; only the documents that describe it are fixed. Whatever scheme emerged from the interview must be written where the agent reads it, or it doesn't exist.

## The split

- **Portable "how to operate a vault"** (CLI mechanics, safe writes, query syntax) → stays in the `notes-workflow` skill. Never in vault docs.
- **Vault-specific "how *this* vault is organized"** → into the vault, tiered by how often it's needed.

## The container

```
<vault>/
  VAULT.md                 # folder map + inviolable rules + index — ALWAYS loaded
  _Meta/                    # agent-facing reference; `_` prefix marks it as infrastructure
    conventions/            # principles spanning all note types
    types/                  # one note type each, fully encapsulated
    workflows/              # vault-specific runbooks
  Templates/                # one per significant type — source of truth for frontmatter
  _Dashboard/               # optional Bases for high-frequency queries
```

**Folder-naming default.** `_Meta/` and `_Dashboard/` take the `_` prefix on purpose: it groups the agent/system folders together, reads as "infrastructure, not content," and sorts them away from daily content without imposing an order. If the user instead wants a custom folder order, switch the whole vault to numbered prefixes (where the meta folder becomes `99 Meta/`, pinned to the bottom) — see the numbered-folders pattern in [patterns](patterns.md). Don't mix the two.

### `VAULT.md` — primary, always loaded

Only what a *majority* (>~60%) of interactions need. Keep it short:
- **Folder map** — each folder + one line on what it means.
- **Inviolable rules** — a few hard constraints (e.g. "never overwrite", "drafts go to staging").
- **Index** — links into every `_Meta/` doc and each Base, so the agent can find detail on demand.

### `_Meta/` — supplementary, read on demand

- `conventions/` — principles across types: how to choose a folder, property conventions, capture/processing.
- `types/` — one type each: its location, frontmatter, type-specific behavior.
- `workflows/` — step-by-step routines particular to this user.

## Authoring rules

1. **General doc holds the *rule*; type doc holds the *instance*. Link, don't duplicate.** `where-things-go.md` says *how* to pick a folder; `bookmarks.md` says bookmarks live in folder X and links back.
2. **VAULT.md only earns info a majority of interactions need.** Else it's a supplementary doc, named so its scope is self-evident (`where-things-go.md`, not `notes-2.md`).
3. **A type earns its own `types/` doc only with real machinery** — a dedicated location, special frontmatter, or its own lifecycle/dashboard. Otherwise it's a one-liner in a conventions doc (promote later if it accumulates rules). Bookmark/project/area usually qualify; idea/log/meeting/person usually don't.
4. **`_Meta/` docs are agent-facing reference** — tag as a queryable collection (`type: reference`, `tags: [meta, system]`), mark `ai: true` if generated. Create a folder by creating a note in it.
5. **`Templates/` is the source of truth for frontmatter.** Type docs point at the template, never restate the YAML — so they can't drift.
6. **Dashboards optional → Bases in `_Dashboard/`** for the highest-frequency queries the user named. Start with one or two they'll actually open; list them in the VAULT.md index.

## Scaffolds

Starting points to fill in (`{{placeholders}}`), not drop in verbatim:
- `assets/templates/VAULT.md.template` — the always-loaded index.
- `assets/templates/type-doc.template.md` — a `_Meta/types/` doc.

## Delivering it — stage locally, then drag in

Build the whole structure as real files in a **local staging folder that mirrors the vault root**, so the user sees exactly what will exist before anything touches the vault:

```
./vault-setup/                 # staging — mirrors the vault root
  VAULT.md
  _Meta/
    conventions/   types/   workflows/
  Templates/
  _Dashboard/                  # .base files (plain YAML/text)
```

Use the Write tool for these — no vault CLI, no per-file prompts, fully previewable. Start from the scaffolds above and fill the `{{placeholders}}`. Show the user the tree and let them open any file.

Then offer two ways to install:

1. **Drag-in (recommended).** *"Open `./vault-setup/` and drag its **contents** — not the folder itself — into your vault's root folder (in Finder/Explorer, or straight into Obsidian's file list). You'll see precisely what you're getting, and you can leave out anything you don't want."* Safe and reversible — nothing lands until they act, and they can drop individual files.
2. **Agent places them.** Two ways, depending on the vault:
   - **Fresh/empty vault → one-shot copy (one-time exception).** For an initial setup it is acceptable — *only here* — to bypass the CLI and bulk-copy the staged files in a single command. Discover the vault path, confirm it's the right vault, then copy:
     ```bash
     obsidian vault info=path                  # absolute path of the focused vault — confirm before copying
     cp -rn ./vault-setup/. "<vault-path>/"    # -n never overwrites existing files; copies contents into the vault root
     ```
     The `cp` will prompt (filesystem/vault writes are not pre-authorized) — that prompt is the user's go-ahead. This shortcut is justified *only* by being a one-time greenfield write of many files. **Do not reuse bulk filesystem writes for ordinary vault work** — everything after setup goes through the Obsidian CLI per `notes-workflow`.
   - **Existing vault / selective placement → per-file CLI.** Write each file with `obsidian create` (make a folder by creating a note inside it). Each write prompts. Heredoc-quote frontmatter/wikilinks (see `notes-workflow`).

**Verify after install** (any path): confirm the docs resolve (`obsidian file file="VAULT.md"`); if a freshly copied file isn't seen yet, `obsidian vault="<name>" reload` to re-index. Then run a `base:query` to confirm the Bases work (step 7).
