---
name: notes-workflow
description: Foundation skill for all vault operations — verifies the vault connection, reads conventions, and provides CLI patterns. Use when working with the vault directly (creating notes, managing bookmarks, projects, areas) or when invoked by another notebook skill before proceeding.
user-invocable: true
allowed-tools: Read, Bash(obsidian vaults), Bash(obsidian vault=* reload), Bash(obsidian read *), Bash(obsidian search *), Bash(obsidian search:context *), Bash(obsidian files *), Bash(obsidian folders *), Bash(obsidian file *), Bash(obsidian folder *), Bash(obsidian tags *), Bash(obsidian tag *), Bash(obsidian properties *), Bash(obsidian property:read *), Bash(obsidian backlinks *), Bash(obsidian links *), Bash(obsidian outline *), Bash(obsidian wordcount *), Bash(obsidian daily:read *), Bash(obsidian daily:path *), Bash(obsidian plugins:enabled *), Bash(obsidian open *), Bash(obsidian version *), Bash(obsidian help *), Bash(defuddle *)
metadata:
  version: "2026-06-28"
---

# Notes Workflow

## Dependencies

This skill depends on the official **obsidian-cli** skill from [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills). If it is not installed, ask the user to install it:

```
/plugin marketplace add kepano/obsidian-skills
/plugin install obsidian@obsidian-skills
```

## Before doing any vault work

First verify the Obsidian CLI is accessible and list available vaults:

```bash
obsidian vaults
```

If this fails, stop and ask the user to ensure Obsidian is running before proceeding.

**Discover which vault to use.** Check whether the currently active vault has a `CLAUDE.md` — its presence signals the vault is set up for use with these skills:

```bash
obsidian file file="CLAUDE.md"
```

If it returns file metadata, the active vault is the right one. If not, list the available vaults and ask the user which vault to use.

Once confirmed, reload the vault to lock it in as the active vault for the session:

```bash
obsidian vault="Vault Name" reload
```

**Never reload multiple vaults at a time** if you need to do an action across multiple vaults, use the `vault=` parameter on each command instead. (eg: `obsidian vault="Vault A" file file="CLAUDE.md"`, `obsidian vault="Vault B" file file="CLAUDE.md"`).

**Warn the user** which vault is now active and that they should not switch to another vault in Obsidian during this session — all commands run against whichever vault is currently open, and switching would silently redirect them.

Then read `CLAUDE.md` for conventions:

```bash
obsidian read path="CLAUDE.md"
```

## Common patterns

```bash
# Read a note
obsidian read path="Folder/Note Title.md"

# List files in a folder (use folder=, not path=)
obsidian files folder="Folder"

# Search
obsidian search query="search term" limit=10

# Get file info (path, size, created, modified in Unix ms)
obsidian file path="Folder/Note Title.md"

# Set a property (always pass type= — see Gotchas)
obsidian property:set name="type" value="project" type=text path="Folder/Note Title.md"

# Remove a property
obsidian property:remove name="github" path="Folder/Note Title.md"

# Move a file (destination folder must already exist — see Gotchas)
obsidian move file="Note Title" to="Other Folder/"

# Rename a file
obsidian rename file="Note Title" name="New Name"
```

## Resolving paths & editing safely

**Prefer `file=` for wikilink titles, `path=` when you know the exact location.** `obsidian read file="Note Title"` resolves a name the wikilink way and is convenient for `[[Title]]` references. Use `path=` (vault-root relative) whenever placement is precise or a name might collide.

**Resolve the path before any write to an existing note.** `file=` returns the *first* match, so with duplicate titles you can read — and later overwrite — the wrong file. Before writing:

1. Resolve: `obsidian file file="Note Name"` — confirm the returned `path` is the one you mean
2. Use that `path=` for every subsequent operation (export, append, overwrite) — never `file=`

For **additive changes**, prefer `obsidian append path="..."` (or `prepend`) — it can't clobber existing content and skips the export/overwrite cycle entirely. See also *Protecting existing content* below.

**Frontmatter changes go through `property:set` directly** — no export/push-back needed just to change a field:

```bash
obsidian property:set name="type" value="project" type=text path="Folder/Note.md"
```

Move the file first if needed, then set properties at the new path. (Always pass `type=` — see Gotchas.)

**Renaming or moving — use `rename`/`move`, never create-new-and-delete.** Obsidian updates inbound `[[links]]` when you rename or move; recreating a note by hand breaks them.

```bash
obsidian rename file="Old Name" name="New Name"
obsidian move file="Note Title" to="Other Folder/"   # destination folder must already exist
```

**Editing a note's body safely**:

1. Resolve path: `obsidian file file="Note Name"`
2. Export to a staging file: `obsidian read path="<resolved-path>" > /tmp/vault-edits/note.md`
3. Edit the local copy with the Edit tool
4. Push back: `obsidian create path="<resolved-path>" overwrite content="$(cat /tmp/vault-edits/note.md)"`

Use `/tmp/vault-edits/` as the staging area; don't browse the vault filesystem directly. Verify the result after an overwrite.

## Obsidian CLI

`obsidian help` lists every command with its parameters indented beneath it. **Do not keyword-grep the full help.**

Only `vault=` is a global option; every other parameter is scoped to its command.

The `obsidian` binary may need to be run with `dangerouslyDisableSandbox: true`.

**Foot-gun — `vault=` must come *before* the subcommand.** This matters for the `reload` call that sets the active vault:

```bash
obsidian vault="My Vault" reload     # ✅ switches active vault to My Vault
obsidian reload vault="My Vault"     # ❌ vault= after subcommand is silently ignored
```

## Active file awareness

If the user refers to something without naming it explicitly — "this note", "what I'm looking at", "the current one" — check the active file first:

```bash
obsidian file
```

If the user sounds like they're talking about something new or unfamiliar, checking the active file may reveal what they mean before asking for clarification.

## Keeping conventions current

`CLAUDE.md` is a living document. If conventions change during a session — new metadata fields, structural decisions, new areas — update it to reflect them.

The vault may have drifted from `CLAUDE.md` by accident rather than intent. Before updating `CLAUDE.md` to match what you observe in the vault, check with the user:

- If the vault state *contradicts* a convention, ask whether the convention should change or the vault should be corrected
- If something looks like a convention the user may have abandoned, ask before removing it
- Don't silently ratify drift — surface it and let the user decide

## Multi-line content

When creating or appending notes with multi-line content — especially content containing backticks, wikilinks, YAML, or code blocks — use a quoted heredoc to prevent shell interpretation:

````bash
obsidian create path="folder/Note Title.md" silent content="$(cat << 'EOF'
---
tags: [example]
type: reference
---

Content with `backticks`, [[wikilinks]], and code fences all safe.

```yaml
key: value
```

More content.
EOF
)"
````

Key points:
- Wrap in `"$(cat << 'EOF' ... EOF)"` — the outer quotes preserve newlines, `'EOF'` prevents all shell interpretation inside
- Works for `create`, `append`, and `prepend`
- Use `path=` (exact vault-root path) rather than `name=` when folder placement matters
- Use `silent` to prevent files from opening in the app — but avoid `silent` on important files where you want the user to notice the result

## Opening files

After creating or editing a note, offer to open it — or open it immediately if the context makes it obvious the user wants to see it. Use `newtab` so it doesn't displace what's already open:

```bash
obsidian open path="Folder/Note Title.md" newtab
```

Only open notes if the user asks, or it is obvious from the context that they are monitoring your progress.

## Protecting existing content

Never use `overwrite` on `obsidian create` unless the user has explicitly asked to replace a file. Overwriting silently destroys content. If a file already exists and needs updating, use `property:set`, `append`, or `prepend` instead — or read the file first and confirm with the user before replacing it.

## Gotchas

A few CLI behaviours that fail *silently* — worth knowing regardless of task:

- **`property:set` writes a string unless told otherwise.** `obsidian property:set name="x" value="true"` stores the *string* `"true"`, not a boolean. Pass `type=` for the real type: `type=checkbox` for booleans, plus `number`, `date`, `datetime`, `list`. This bites when a base or query filters on the value — a string `"true"` does not match a boolean `true`, so the note silently fails to drop out of (or into) the filtered view. After setting a property a query depends on, re-run the query to confirm it took.
- **`obsidian move` does not create the destination folder.** Moving into a folder that doesn't exist yet fails with `ENOENT`. Create a note inside the target folder first (which creates the folder), then move.
- **Overwrites via piped file contents need absolute paths.** When using `content="$(cat …)"` to overwrite a note, point `cat` at an absolute path (e.g. `/tmp/vault-edits/note.md`). A relative path can silently resolve to the wrong location after a `cd`, passing empty content and clobbering the note to blank. Always verify the result after an `overwrite`.

## Fetching web content

Use the `defuddle` skill, if available (from the official obsidian-skills plugin), instead of WebFetch for standard web pages. It strips navigation, ads, and clutter, reducing token usage and returning clean markdown. Invoke it via the Skill tool when fetching URLs for bookmarks or research.

## References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Daily notes | Prefer the `daily:` subcommands; discover the folder, don't hardcode it; reaching history | [daily-notes](references/daily-notes.md) |
| Efficiency | Parallelizing reads, sequencing writes, batching, timestamps | [efficiency](references/efficiency.md) |
