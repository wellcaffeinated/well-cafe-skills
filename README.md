# well-cafe-skills

Personal Claude Code skills for wellcaffeinated.

- **notebook** — work in an Obsidian vault: notes, bookmarks, projects, areas, capture and review.
- **coding-conventions** — language-specific coding style skills.

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

> **New vault?** Run `/notes-setup` once. It orients you, helps design a structure around how you want to work, and writes the conventions Claude reads (`CLAUDE.md` and the `99 Meta/` docs).

---

## Skills

### notebook

```bash
/plugin install notebook@well-cafe-skills
```

Working in an Obsidian vault — note creation, bookmarks, projects, areas, capture, and review. Each skill loads `notes-workflow` first, which verifies the connection and reads `CLAUDE.md` at the vault root for conventions before any vault work.

### coding-conventions

```bash
/plugin install coding-conventions@well-cafe-skills
```

Language-specific coding conventions — naming, function design, guard clauses, dispatch tables, iteration, immutability, modules, logging, and TypeScript-specific patterns.
