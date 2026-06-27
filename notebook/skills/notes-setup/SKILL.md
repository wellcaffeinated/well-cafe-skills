---
name: notes-setup
description: One-time onboarding — orients a user to their Obsidian vault and designs a structure around how they actually want to work, then writes it into the vault (CLAUDE.md, 99 Meta/ docs, templates, optional Bases). Use when setting up a new vault for these skills, or when a user says "set up my notebook" / "help me organize Obsidian from scratch".
user-invocable: true
allowed-tools: Read, AskUserQuestion, Bash(obsidian vaults), Bash(obsidian read *), Bash(obsidian search *), Bash(obsidian files *), Bash(obsidian folders *), Bash(obsidian file *), Bash(obsidian tags *), Bash(obsidian properties *), Bash(obsidian base:query *)
metadata:
  version: "2026-06-27"
---

# Notes — Setup

A **one-time** skill. It orients a user to their notebook, designs a structure around *how they want to work*, and writes that structure into the vault so every other notebook skill has conventions to read.

Output: the standardized container — `CLAUDE.md`, `99 Meta/` docs, `Templates/`, and optional `_Dashboard/` Bases. See [output-structure](references/output-structure.md).

## Before starting

**Invoke `notebook:notes-workflow` first.** It verifies the vault connection and CLI patterns. If it is not available, ask the user to install the `notebook` plugin.

Then **detect existing state** — do not clobber a configured vault:

```bash
obsidian file file="CLAUDE.md"      # already set up?
obsidian folders                    # existing structure?
```

- **`CLAUDE.md` exists** → this vault is already configured. Offer to *revise/extend*, not rebuild. Read it first.
- **Notes but no `CLAUDE.md`** → design *around* what's there; read the existing folders before proposing anything.
- **Empty vault** → full greenfield setup.

## Core rule: never explain and ask in the same turn

`AskUserQuestion` can hide prose the user just needed to read. So:

- After any substantial explanation, **end the turn** with an invitation to continue ("ready?"). Wait for the user before asking.
- Only batch questions *after* the user has read the relevant prose.
- Short recognition-style questions (experience, sync posture) may be asked directly — they need no setup prose.

## The flow

Design emerges from **use-cases, not taxonomy**, and every choice serves **two readers**: the human (browses, recognizes) and the agent (queries, addresses). See [primitives](references/primitives.md) for the reasoning model.

### 1. Calibrate (short questions, no prose first)

Gauge, with `AskUserQuestion`:

- **Obsidian experience** — never used / dabbled / regular. Scales how much orientation to give and how much vocabulary to assume.
- **Existing setup** — empty / has notes I care about / has a working structure.
- **Sync posture** — already syncing & happy / multiple devices, no sync yet / single device / "what's sync?".

These answers branch everything downstream. Record them.

### 2. Orient (prose, then pause)

Scaled to experience. New users get the plain-language version: what a notebook can do, and the two-readers idea. Experienced users get a sentence, not a lecture. **End the turn and wait** before the interview.

### 3. Use-case interview

Menu-driven via `AskUserQuestion` so users *recognize* options rather than invent them. Adapt to their level and existing vault. Offer a starting **organizing philosophy** as a lens, not a mandate (see [philosophies](references/philosophies.md)). See [interview](references/interview.md) for the branching question sets. Elicit:

- How they capture, and how messy capture may be.
- What they keep (bookmarks, projects, reading queue, people…).
- What they'll want to **ask** of the vault.
- Which interactions should feel **effortless**.
- The agent's role: how it **processes** capture, **remembers** across sessions, where its **drafts** land before being trusted.

### 4. Translate to a proposed structure

Turn each recurring interaction into a need, then assign each to the *cheapest primitive that serves both readers* (folder / tag / property / Base / link). Draw on [patterns](references/patterns.md). Present back — folder map, note types, properties, tags, one or two Bases — **with reasoning**. Respect anything already in the vault. Iterate until approved. Write nothing yet.

### 5. Upstream decisions (only the branches their answers selected)

- **Plugins** — referral only, suggested against an elicited need. See [plugins](references/plugins.md).
- **Sync** — route by posture from step 1: *skip* (already sorted), *guide* (constraints interview), or *explain then offer* (the "what's sync?" user — prose, then pause). See [sync](references/sync.md).

### 6. Materialize — build it locally, then deliver

Assemble the agreed structure as real files in a **local staging folder that mirrors the vault root** (`CLAUDE.md`, the tiered `99 Meta/` docs, `Templates/`, optional `_Dashboard/` Bases). Show the user the tree — nothing has touched the vault yet. Then offer two ways to install (detail in [output-structure](references/output-structure.md)):

- **Drag-in (recommended, safe):** the user reviews the files and drags the staging folder's *contents* into their vault root. They see exactly what they're getting and can leave out anything they don't want — before committing.
- **I'll place them:** the agent writes each file into the vault via the CLI (prompts per write).

Vault writes are **not** pre-authorized, which is the point — the local-staging path lets the user preview the whole structure with zero vault changes.

### 7. Seed & verify, then hand off

- Create one real note from a template.
- Run a `base:query` to confirm properties and Bases actually resolve (string `"true"` ≠ boolean `true` — re-run after setting).
- Point them at the everyday skills (`notes-organize`, `notes-daily`, `notes-reflect`) now that conventions exist.

## References

| Topic | Reference |
|-------|-----------|
| Two-readers / primitives reasoning model | [primitives](references/primitives.md) |
| Branching interview question sets | [interview](references/interview.md) |
| Organizing philosophies to offer as starting lenses | [philosophies](references/philosophies.md) |
| The vault container spec (CLAUDE.md, 99 Meta/, Templates/) | [output-structure](references/output-structure.md) |
| Reusable encoding patterns (`ai: true`, staging gate, …) | [patterns](references/patterns.md) |
| Plugin referrals (official docs only) | [plugins](references/plugins.md) |
| Sync decision (constraints-first) | [sync](references/sync.md) |
