# well-cafe-skills

Personal agent skills for wellcaffeinated. Every skill is a plain `skills/<name>/SKILL.md`
directory, so it works with any client that reads the Agent Skills format. Each plugin also
ships an [Agent Plugins 1.0](https://agent-plugins.org/) manifest (`plugin.json`) alongside
its Claude Code one (`.claude-plugin/plugin.json`).

- **notebook** — work in an Obsidian vault: notes, bookmarks, projects, areas, capture and review.
- **youtube-transcript** — turn YouTube videos or whole channels into markdown transcripts.
- **coding-conventions** — language-specific coding style skills.

## Skills Quickstart

For Claude Code, add the marketplace once:

```bash
/plugin marketplace add wellcaffeinated/well-cafe-skills
```

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
