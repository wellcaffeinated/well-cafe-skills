---
name: filing
description: Shared filing logic for notebook skills — destination research, link proposals, and frontmatter conventions. Defers to VAULT.md for folder structure.
---

# Filing Logic

## Choosing a destination

The vault's folder structure and filing conventions are defined in `VAULT.md`. Before proposing a destination for any item, check `VAULT.md` for the relevant conventions, then search to confirm whether a better-fit location already exists:

```bash
obsidian search query="relevant term" limit=5
```

File to the most specific applicable location. Check whether the destination folder has subfolders before proposing the top level — prefer an existing subfolder over creating a new one unless nothing fits.

## Proposing links

When filing anything, also propose links in both directions where a related note exists:

- If an existing note clearly relates, propose adding a wikilink in one or both directions
- For bookmarks, identify the note most likely to benefit from discovering the resource
- State links explicitly: `link from [[Some Note]]` or `add related: [[Another Note]] to frontmatter`

## Proposing frontmatter

Every filing proposal must include suggested frontmatter using the type values and field conventions from `VAULT.md`. At minimum propose `type:` and `tags:`. Additional fields depend on the item type — check `VAULT.md` for the full list.

Present the metadata inline with the proposal so the user can approve or edit before execution.

## Additive edits

Prefer additive edits — `append`, `prepend`, or a new section — over overwriting existing prose. Never rewrite the user's words unprompted.
