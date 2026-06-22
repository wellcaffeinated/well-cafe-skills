---
name: filing-para
description: Shared filing logic for notebook skills — PARA destination decisions, link proposals, and frontmatter conventions. Reference this instead of duplicating filing rules across skills.
---

# Filing Logic (PARA)

## Choosing a destination

Use the PARA logic from `CLAUDE.md` for folder decisions:

- **Does it have a finish line?** → Projects folder
- **Ongoing responsibility, no finish line?** → Areas folder
- **Reference, no obligation?** → Resources folder
- **Done or dormant?** → Archive folder

File to the most specific applicable location. Check whether the destination folder has subfolders before proposing the top level — prefer an existing subfolder over creating a new one unless nothing fits. Research the destination first with a search before proposing:

```bash
obsidian search query="relevant term" limit=5
```

## Proposing links

When filing anything, also propose links in both directions where a related note exists:

- If an existing note clearly relates, propose adding a wikilink in one or both directions
- For bookmarks, identify the project or area most likely to benefit from discovering the resource
- State links explicitly: "link from [[Project X]]" or "add `related: [[Resource Y]]` to frontmatter"

## Proposing frontmatter

Every filing proposal must include suggested frontmatter using the type values and field conventions from `CLAUDE.md`. At minimum propose `type:` and `tags:`. Additional fields by item type:

- **Bookmarks**: also propose `source:`
- **Promoted projects**: propose `outcome:`
- **Promoted areas**: propose `purpose:`

Present the metadata inline with the proposal so the user can approve or edit before execution.

## Additive edits

Prefer additive edits — `append`, `prepend`, or a new section — over overwriting existing prose. Never rewrite the user's words unprompted.
