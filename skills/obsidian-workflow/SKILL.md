---
name: obsidian-workflow
description: Use when working with the user's Obsidian vault (Main Vault) — creating notes, managing bookmarks, projects, areas, or any vault organisation tasks.
user-invocable: true
allowed-tools: Read, Bash(obsidian read *), Bash(obsidian search *), Bash(obsidian search:context *), Bash(obsidian files *), Bash(obsidian folders *), Bash(obsidian file *), Bash(obsidian folder *), Bash(obsidian tags *), Bash(obsidian tag *), Bash(obsidian properties *), Bash(obsidian property:read *), Bash(obsidian backlinks *), Bash(obsidian links *), Bash(obsidian outline *), Bash(obsidian wordcount *), Bash(obsidian daily:read *), Bash(obsidian daily:path *), Bash(obsidian version *), Bash(obsidian help *), Bash(defuddle *)
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

The `obsidian` binary communicates with the running Obsidian app via XPC. This requires access to macOS system services that may be blocked by the sandbox. If obsidian commands fail silently or return XPC errors, sandbox permissions need to be adjusted.

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

## Protecting existing content

Never use `overwrite` on `obsidian create` unless the user has explicitly asked to replace a file. Overwriting silently destroys content. If a file already exists and needs updating, use `property:set`, `append`, or `prepend` instead — or read the file first and confirm with the user before replacing it.

## Fetching web content

Use the `defuddle` skill (from the official obsidian-skills plugin) instead of WebFetch for standard web pages. It strips navigation, ads, and clutter, reducing token usage and returning clean markdown. Invoke it via the Skill tool when fetching URLs for bookmarks or research.

## Common patterns

```bash
# Read a note
obsidian read path="02 Areas/Twine.md"

# Search
obsidian search query="search term" limit=10

# Set a property
obsidian property:set name="type" value="project" path="01 Projects/My Project.md"

# Remove a property
obsidian property:remove name="github" path="01 Projects/My Project.md"

# Move a file
obsidian move file="Note Name" to="02 Areas/"

# Rename a file
obsidian rename file="Note Name" name="New Name"
```
