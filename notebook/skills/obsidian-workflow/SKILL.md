---
name: obsidian-workflow
description: Use when working with the user's Obsidian vault (Main Vault) — creating notes, managing bookmarks, projects, areas, or any vault organisation tasks.
user-invocable: true
allowed-tools: Read, Bash(obsidian read *), Bash(obsidian search *), Bash(obsidian search:context *), Bash(obsidian files *), Bash(obsidian folders *), Bash(obsidian file *), Bash(obsidian folder *), Bash(obsidian tags *), Bash(obsidian tag *), Bash(obsidian properties *), Bash(obsidian property:read *), Bash(obsidian backlinks *), Bash(obsidian links *), Bash(obsidian outline *), Bash(obsidian wordcount *), Bash(obsidian daily:read *), Bash(obsidian daily:path *), Bash(obsidian open *), Bash(obsidian version *), Bash(obsidian help *), Bash(defuddle *)
---

# Obsidian Workflow

## Dependencies

This skill depends on the official **obsidian-cli** skill from [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills). If it is not installed, ask the user to install it:

```
/plugin marketplace add kepano/obsidian-skills
/plugin install obsidian@obsidian-skills
```

## Before doing any vault work

First verify the Obsidian CLI is accessible and the vault is reachable:

```bash
obsidian vault info=name
```

If this fails or returns unexpected output, stop and ask the user to ensure Obsidian is running with the correct vault open before proceeding.

Then read `CLAUDE.md` at the vault root for conventions:

```bash
obsidian read path="CLAUDE.md"
```

## Active file awareness

If the user refers to something without naming it explicitly — "this note", "what I'm looking at", "the current one" — check the active file first:

```bash
obsidian file
```

This is also useful as context when a request seems ambiguous. If the user sounds like they're talking about something new or unfamiliar, checking the active file may reveal what they mean before asking for clarification.

## Keeping conventions current

`CLAUDE.md` is a living document. If conventions change during a session — new metadata fields, structural decisions, new areas — update it to reflect them.

However, the vault may have drifted from the conventions in `CLAUDE.md` by accident rather than intent. Before updating `CLAUDE.md` to match what you observe in the vault, check with the user:

- If the vault state *contradicts* a convention, ask whether the convention should change or the vault should be corrected
- If something looks like a convention the user may have abandoned, ask before removing it
- Don't silently ratify drift — surface it and let the user decide

The goal is for `CLAUDE.md` to reflect *intentional* conventions, not just the current state of the vault.

## Obsidian CLI

The `obsidian` binary communicates with the running Obsidian app via XPC. This requires access to macOS system services that are always blocked by the sandbox. **Always run `obsidian` commands with `dangerouslyDisableSandbox: true`** — do not wait for a failure before doing so.

The vault name is **Main Vault**. Commands target the most recently focused vault by default. Use `vault="Main Vault"` explicitly if multiple vaults may be open.

## Multi-line content

When creating or appending notes with multi-line content — especially content containing backticks, wikilinks, YAML, or code blocks — use a quoted heredoc to prevent shell interpretation:

```bash
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
```

Key points:
- Wrap in `"$(cat << 'EOF' ... EOF)"` — the outer quotes preserve newlines, `'EOF'` prevents all shell interpretation inside
- Works for `create`, `append`, and `prepend`
- Use `path=` (exact vault-root path) rather than `name=` when folder placement matters
- Use `silent` to prevent files from opening in the app — but avoid `silent` on important files where you want the user to notice the result

## Opening files

After creating or editing a note, offer to open it — or open it immediately if the context makes it obvious the user wants to see it. Use `newtab` so it doesn't displace what's already open:

```bash
obsidian open path="01 Projects/My Project.md" newtab
```

When creating or moving several files in one session, open them in thematic groups rather than one by one or all at once — this keeps the tab order meaningful and gives the user a natural moment to review each batch.

When writing multi-step changes and the user wants to see progress as it happens, omit `silent` from `create`, `append`, and `prepend` so each file opens automatically as it's written. Use `silent` when batching many writes where opening every file would be disruptive — then offer a grouped open at the end.

## Protecting existing content

Never use `overwrite` on `obsidian create` unless the user has explicitly asked to replace a file. Overwriting silently destroys content. If a file already exists and needs updating, use `property:set`, `append`, or `prepend` instead — or read the file first and confirm with the user before replacing it.

## Fetching web content

Use the `defuddle` skill (from the official obsidian-skills plugin) instead of WebFetch for standard web pages. It strips navigation, ads, and clutter, reducing token usage and returning clean markdown. Invoke it via the Skill tool when fetching URLs for bookmarks or research.

## Daily notes

`obsidian daily:read` and `obsidian daily:path` only work for today. Passing a `date=` argument always returns today's note regardless of the value — do not rely on it for history.

To read recent daily notes, list the folder and filter by filename — filenames are `YYYY-MM-DD.md` so they sort chronologically:

```bash
# Get the last N daily notes
obsidian files folder="00 Daily" | sort | tail -7
```

Then read each by path:

```bash
obsidian read path="00 Daily/2026-03-25.md"
```

## Efficiency

**Parallelise read operations.** Independent reads — listing folders, fetching file metadata, reading notes — can all run in parallel. Batch them into a single message rather than waiting for each to complete before starting the next.

**Never parallelise write operations.** Note creation, appending, property changes, moves, and renames must run one at a time. Parallel writes risk race conditions and make it hard to catch errors or confirm results before the next step.

**Batch metadata checks with a loop.** When checking modification times across many files, use a single bash loop rather than one call per file:

```bash
for p in "01 Projects/Foo.md" "01 Projects/Bar.md"; do
  echo "=== $p ===" && obsidian file path="$p"
done
```

**Convert timestamps inline.** Timestamps from `obsidian file` are Unix milliseconds. Convert in the same step rather than as separate follow-up calls:

```bash
date -r $(( 1774463658790 / 1000 )) "+%Y-%m-%d %H:%M"
```

## File modification times

Use `obsidian file path=` to get metadata including `created` and `modified` timestamps (Unix ms):

```bash
obsidian file path="01 Projects/My Project.md"
# returns: path, name, extension, size, created, modified
```

To convert the `modified` value to a human-readable date, divide by 1000 and pass to `date`:

```bash
date -r $(( 1774463658790 / 1000 )) "+%Y-%m-%d %H:%M"
```

## Common patterns

```bash
# Read a note
obsidian read path="02 Areas/Twine.md"

# List files in a folder (use folder=, not path=)
obsidian files folder="01 Projects"

# Search
obsidian search query="search term" limit=10

# Get file info (including modification time)
obsidian file path="01 Projects/My Project.md"

# Set a property
obsidian property:set name="type" value="project" path="01 Projects/My Project.md"

# Remove a property
obsidian property:remove name="github" path="01 Projects/My Project.md"

# Move a file
obsidian move file="Note Name" to="02 Areas/"

# Rename a file
obsidian rename file="Note Name" name="New Name"
```
