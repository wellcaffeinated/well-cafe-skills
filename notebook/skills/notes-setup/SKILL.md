---
name: notes-setup
description: One-time onboarding — orients a user to their Obsidian vault and designs a structure around how they actually want to work, then writes it into the vault (CLAUDE.md, _Meta/ docs, templates, optional Bases). Use when setting up a new vault for these skills, or when a user says "set up my notebook" / "help me organize Obsidian from scratch".
user-invocable: true
allowed-tools: Read, AskUserQuestion, Bash(obsidian vaults), Bash(obsidian read *), Bash(obsidian search *), Bash(obsidian files *), Bash(obsidian folders *), Bash(obsidian file *), Bash(obsidian tags *), Bash(obsidian properties *), Bash(obsidian base:query *), Bash(obsidian plugins:enabled *), Bash(obsidian daily:path *)
metadata:
  version: "2026-06-28"
---

# Notes — Setup

A **one-time** skill. It orients a user to their notebook, designs a structure around *how they want to work*, and writes that structure into the vault so every other notebook skill has conventions to read.

Output: the standardized container — `CLAUDE.md`, `_Meta/` docs, `Templates/`, and optional `_Dashboard/` Bases. See [output-structure](references/output-structure.md).

## How this skill is structured — read it

The steps below are a **conductor**; the substance lives in the reference files. Each step names a file to read *before* you act on it — read it then, freshly, not from memory of this summary.

This matters because the whole point of the skill is to replace the generic "Inbox / Projects / Notes" folder list a model produces by reflex with a structure derived from *how this particular user works*. That only happens if you actually load the reasoning ([primitives](references/primitives.md)), the question sets ([interview](references/interview.md)), and the organizing lenses ([philosophies](references/philosophies.md)) at the moment each is needed. **A run that proposes a folder structure without having read these has skipped the skill** — and will produce exactly the bland, un-educational output this skill exists to prevent.

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

**Read [philosophies](references/philosophies.md) before writing this.** Scaled to experience:

- **New / dabbled** — actually *teach* a little. Explain in plain language what a notebook can do, the two-readers idea, and — crucially — that there are a handful of established ways people organize notes (PARA, Zettelkasten, Johnny.Decimal, navigable hubs, minimal flat) and what each is *good at*. A newcomer leaving this skill should understand the landscape a bit, not just have answered questions — give them enough to choose from understanding, not from a cold menu.
- **Regular user** — a sentence, not a lecture; assume the vocabulary.

This is education, not interrogation. **End the turn and wait** for the user before moving to the interview.

### 3. Use-case interview

**Read [interview](references/interview.md) and [philosophies](references/philosophies.md) before this step** — they hold the branching question sets and the lenses. Without them you'll default to a generic menu, which is the failure this skill exists to prevent.

Menu-driven via `AskUserQuestion` so users *recognize* options rather than invent them. Adapt to their level and existing vault. Offer a starting **organizing philosophy** as a lens, not a mandate. Elicit:

- How they capture, and how messy capture may be.
- What they keep (bookmarks, projects, reading queue, people…).
- What they'll want to **ask** of the vault.
- Which interactions should feel **effortless**.
- The agent's role: how it **processes** capture, **remembers** across sessions, where its **drafts** land before being trusted.

**Then close with an open-ended, free-text question — not a menu.** The menus capture what we thought to ask; people always know things about how they work that no menu anticipated. After the structured rounds, ask in prose something like: *"Before I sketch a structure — is there anything else about how you work, or how you'd like this to feel, that I haven't asked about? Anything you've tried that did or didn't stick, pet peeves, the way you actually reach for notes? In your own words — as much or as little as you like."* This is plain prose: **end the turn and wait** for their reply. Fold what they say into step 4.

### 4. Translate to a proposed structure

**Read [primitives](references/primitives.md) and [patterns](references/patterns.md) before proposing** — primitives is the reasoning model you justify choices with; patterns is the menu of encodings to reach for against a need.

Turn each recurring interaction into a need, then assign each to the *cheapest primitive that serves both readers* (folder / tag / property / Base / link). Present back — folder map, note types, properties, tags, one or two Bases — **with reasoning**. Respect anything already in the vault. Iterate until approved. Write nothing yet.

If folder order matters to the user, ask whether they want **numbered folder prefixes** for a custom (non-alphabetical) order — an optional convention; see [patterns](references/patterns.md). The default scaffold is un-numbered with `_`-prefixed system folders.

### 5. Upstream decisions (only the branches their answers selected)

- **Plugins** — referral only, suggested against an elicited need. See [plugins](references/plugins.md). If daily capture was elicited, treat **Daily Notes** specially: it's the one plugin that also serves the agent (it provides the `daily:` CLI commands the everyday skills use). Make sure it's enabled and that its new-file folder and any daily template line up with the daily folder you're building — otherwise the plugin and the structure point at different places. The date format is the user's setting (recommend a sortable `YYYY-MM-DD`, but don't assume it); record whatever they use. (Detect state with `plugins:enabled` / `daily:path`, but enabling and configuring it is a settings change the user makes.)
- **Sync** — route by posture from step 1: *skip* (already sorted), *guide* (constraints interview), or *explain then offer* (the "what's sync?" user — prose, then pause). See [sync](references/sync.md).

### 6. Materialize — build it locally, then deliver

Assemble the agreed structure as real files in a **local staging folder that mirrors the vault root** (`CLAUDE.md`, the tiered `_Meta/` docs, `Templates/`, optional `_Dashboard/` Bases). Show the user the tree — nothing has touched the vault yet. Then offer two ways to install (detail in [output-structure](references/output-structure.md)):

- **Drag-in (recommended, safe):** the user reviews the files and drags the staging folder's *contents* into their vault root. They see exactly what they're getting and can leave out anything they don't want — before committing.
- **I'll place them:** for a fresh vault, a **one-shot bulk copy** of the staged folder into the vault path (`obsidian vault info=path` to find it) — acceptable *only* for this one-time setup; otherwise per-file via the CLI. See [output-structure](references/output-structure.md).

Vault writes are **not** pre-authorized, which is the point — the local-staging path lets the user preview the whole structure with zero vault changes, and the bulk copy still prompts before it runs.

### 7. Seed & verify, then hand off

- Create one real note from a template.
- Run a `base:query` to confirm properties and Bases actually resolve (string `"true"` ≠ boolean `true` — re-run after setting).
- If daily capture is part of the setup, confirm `obsidian daily:path` returns a path **inside the daily folder you built** — that proves the Daily Notes plugin config and the structure agree, so the `daily:` commands work downstream. If it doesn't (or the plugin's off), have the user fix the folder/format in settings, or record the daily location in `CLAUDE.md` / `_Meta/` so the everyday skills can still find it.
- Point them at the everyday skills (`notes-organize`, `notes-daily`, `notes-reflect`) now that conventions exist.

## References

| Topic | Reference |
|-------|-----------|
| Two-readers / primitives reasoning model | [primitives](references/primitives.md) |
| Branching interview question sets | [interview](references/interview.md) |
| Organizing philosophies to offer as starting lenses | [philosophies](references/philosophies.md) |
| The vault container spec (CLAUDE.md, _Meta/, Templates/) | [output-structure](references/output-structure.md) |
| Reusable encoding patterns (`ai: true`, staging gate, …) | [patterns](references/patterns.md) |
| Plugin referrals (official docs only) | [plugins](references/plugins.md) |
| Sync decision (constraints-first) | [sync](references/sync.md) |
