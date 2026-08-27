# well-cafe-skills

Personal agent skills for wellcaffeinated.

Every skill lives once, as a plain `skills/<name>/SKILL.md` directory at the repo root — the
layout any Agent Skills client expects. The `notebook/`, `coding-conventions/` and
`youtube-transcript/` directories are Claude Code plugins that group those skills; their
`skills/` entries are symlinks into the canonical set, so there is exactly one copy of
every skill.

- **notebook** — work in an Obsidian vault: notes, bookmarks, projects, areas, capture and review.
- **youtube-transcript** — turn YouTube videos or whole channels into markdown transcripts.
- **coding-conventions** — language-specific coding style skills.

## Skills Quickstart

For Claude Code, add the marketplace once:

```bash
/plugin marketplace add wellcaffeinated/well-cafe-skills
```

For Hermes, see [Installing with Hermes](#installing-with-hermes).

### notebook

```bash
/plugin install notebook@well-cafe-skills
```

Working in an Obsidian vault — note creation, bookmarks, projects, areas, capture, and review. Each skill loads `notes-workflow` first, which verifies the connection and reads `VAULT.md` at the vault root for conventions before any vault work.

### youtube-transcript

```bash
/plugin install youtube-transcript@well-cafe-skills
```

Workflow to efficiently transcribe any youtube video (or a bunch of videos from a channel) into markdown files based on the video's subtitles.

### coding-conventions

```bash
/plugin install coding-conventions@well-cafe-skills
```

Language-specific coding conventions — naming, function design, guard clauses, dispatch tables, iteration, immutability, modules, logging, and TypeScript-specific patterns.

---

## Installing with Hermes

Hermes installs skills individually rather than in groups. Add this repo as a source once,
then pick what you want:

```bash
hermes skills tap add wellcaffeinated/well-cafe-skills
```

Browse what's there, then install by name:

```bash
hermes skills search notes
hermes skills install notes-workflow --category notebook
hermes skills install notes-daily    --category notebook
```

`--category` groups skills on disk, so they stay together in `hermes skills list`.
The notebook skills all expect `notes-workflow` — install it alongside any of them.

**Update everything** with one command. It re-fetches each installed skill, compares
content hashes, and skips anything you've edited locally rather than overwriting it:

```bash
hermes skills update
```

**Turn skills on and off** without uninstalling:

```bash
hermes skills config
```

**Load a group under one slash command** — the Hermes equivalent of installing a plugin:

```bash
hermes bundles create notebook -d "Obsidian vault work" \
  -s notes-workflow -s notes-setup -s notes-daily -s notes-organize \
  -s notes-catchup -s notes-reflect -s notes-connect -s notes-surprise
```

Then `/notebook` loads them together.

---

## Getting started with the notebook skills

The notebook skills drive a **running Obsidian app** through the Obsidian CLI. Three things need to be in place first.

### 1. Install Obsidian and open your vault

Install the [Obsidian desktop app](https://obsidian.md) and open the vault you want Claude to work in.

### 2. Activate the Obsidian CLI

The skills talk to Obsidian through its command-line interface. Enable it by following the official guide: <https://help.obsidian.md/cli>. Then verify it works:

```bash
obsidian vaults      # should list your vaults
```

If the `obsidian` command isn't found, the CLI isn't activated yet.

### 3. Install the skills

The notebook skills depend on Obsidian's official `obsidian-cli` skill, so install both:

```bash
# Obsidian CLI skill (dependency)
/plugin marketplace add kepano/obsidian-skills
/plugin install obsidian@obsidian-skills

# Notebook skills
/plugin marketplace add wellcaffeinated/well-cafe-skills
/plugin install notebook@well-cafe-skills
```

### Keep the vault open and focused

Obsidian CLI commands act on whichever vault was **most recently focused**. For Claude to work in the right place, keep Obsidian running with that vault open — and don't switch to a different vault mid-session, or commands will silently target the other one.

> **New vault?** Run `/notes-setup` once. It orients you, helps design a structure around how you want to work, and writes the conventions the agent reads (`VAULT.md` and the `_Meta/` docs).

> **Upgrading from an earlier version?** The vault convention file was renamed from
> `CLAUDE.md` to `VAULT.md` in notebook 1.8.0. Rename it at your vault root; the skills
> only look for the new name. The name is now agent-neutral, and `CLAUDE.md` tripped
> Hermes' security scanner as a cross-agent persistence risk, which blocked installs.

---

## Repository layout

```
skills/<name>/SKILL.md      every skill, one copy, the canonical location
skills.sh.json              groups the skills for browse/search listings
<plugin>/skills/<name>      symlink into skills/ — Claude Code plugin grouping
<plugin>/.claude-plugin/    Claude Code plugin manifest
.claude-plugin/             the Claude Code marketplace
```

Skills live at the repo root because that is where skill registries look for them, which is
what makes `hermes skills tap add` work. The plugin directories exist to give Claude Code
its per-group install. Because the plugin entries are symlinks, editing a skill in
`skills/` is the only place you ever edit it.

Cloning on Windows needs `git config --global core.symlinks true`, or the plugin
directories come down as plain text files instead of links.
