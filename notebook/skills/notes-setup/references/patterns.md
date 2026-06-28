---
name: notes-setup-patterns
description: Reusable encoding patterns for notes-setup — conventions that serve both readers (ai:true provenance, staging gates, typed wikilinks, encode-twice). Offered against a need, never mandated.
---

# Encoding patterns

A menu of battle-tested conventions to reach for when translating use-cases into structure (step 4). Each is offered *against a need*, not a starter pack.

## Provenance & trust

- **`ai: true`** — mark agent-generated notes. Makes generated content auditable and queryable, so a human or linting pass can find it. Cheap, high value.
- **Staging gate** — agent-authored content lands provisional (`status: draft`, or a holding folder) and is promoted only after review. The write-path form of "mind silent failure" — keeps generated content from quietly polluting the graph.

## Relationships

- **Typed wikilink property** — `area: "[[Neptune Studios]]"`. A relationship that is both *traversable* (backlinks/links) and *filterable* (Bases) — stronger than a bare link or a bare tag.

## Redundancy for both readers

- **Encode twice** — put a fact in a human-visible primitive *and* an agent-cheap one. Status as a *folder* (free in the path, visible in the tree) **and** a Base that filters on it (one-shot agent answer). Not waste — coverage.

## Keep the queried vocabulary small

- **`type:` as the spine** — one small, controlled set of note types, each with a template, feeding Bases. Beats many ad-hoc properties nobody maintains.
- **Templates set queried properties at creation** — the only reliable defense against silent-failure of property filters. If the agent will query it, a template should set it.

## Agent working memory (if elicited)

- **Session log + hot cache** — `_Meta/log.md` (append-only operation history) and `_Meta/hot.md` (~500-word recent-context cache read first). The agent's notes to itself, distinct from the human's knowledge. Only set this up if the user wants cross-session continuity.

## Retrieval-friendly writing

- **H2 chunking** — write notes in `##` sections; each becomes an independently retrievable unit. Serves the human (scannable) and the agent (smaller hits).

## Privacy

- **Exclude sensitive content** — `.indexignore` or a hidden `.raw/` keeps private notes out of indexes and agent reach.

## Asking the agent for work

- **Action-request property** — a single property whose *value names a task* the user wants the agent to do with the note (e.g. `triage: percolate | draft | research | connect`). A Base grouped by that value becomes the agent's inbound queue — "here's everything you asked me to develop / write up / research." The inverse of a staging gate (which holds agent *output*); this holds human *requests*. Keep the vocabulary short and the values verbs.
- **Processing-state flag** — a boolean like `processed: true` marking "I've reviewed this" on a capture surface (a daily note, an inbox item). Unset = still to review. A "today's note can never be processed" rule stops an in-progress day from showing as done. Lets a Base split the reviewed from the backlog.

## Surfacing what you'd forget

- **Staleness view** — a Base formula such as `days_since: (now() - file.mtime).days`, plus a view filtered to large values, resurfaces notes untouched for a while: forgotten ideas, stale projects, reading never returned to. The cheapest answer to "what have I lost track of?" — the agent reads it in one call instead of crawling the vault.

## Views over `ai:` provenance

- Once notes carry `ai: true`, a Base view filtered `ai != true` gives a **human-only** lens (the user's authentic thinking) and `ai == true` gives an **AI-only** lens — the consumption side of the provenance mark in [Provenance & trust](#provenance--trust).

## A few more lightweight conventions

- **Numbered folders for custom ordering** — offer *only if* the user wants their folders in a deliberate order rather than alphabetical. Prefix each top-level folder with a number (`00 Inbox/`, `10 Projects/`, … `99 Meta/`) so Obsidian sorts by the number: frequent/capture folders up top, archive and agent-facing meta at the bottom (`99` keeps Meta last, out of the way of human browsing). It's all-or-nothing — number *every* top-level folder or none; a lone numbered folder among un-numbered ones orders nothing and just looks orphaned. If they don't want this, default to un-numbered names with a `_` prefix on system folders (`_Meta/`, `_Dashboard/`), which sorts them away from daily content without imposing an order.
- **Incubation type/stage** — a holding `type` (e.g. `seed`) for an idea not yet worth a project, parked until it's ready; a staleness view can resurface it for a second look.
- **Dual-reader inline hints** — a note can carry an agent hint as an HTML comment (`<!-- … -->`, invisible to the human reader) alongside a human hint in plain prose. Both readers, one place.
- **Index / home note for a folder-entity** — when a thing is a *folder* of notes (a project, a topic), give it a home note matching the folder name (a Map of Content). The agent reads the home note first; the human gets an obvious entry point.

## Footguns to encode defensively

- **String `"true"` ≠ boolean `true`.** `property:set` writes a string unless you pass `type=` (`type=checkbox` for booleans; also `number`, `date`, `datetime`, `list`). A base filtering on a boolean silently skips string values. Re-run the query after setting.
- **A missing tag is invisible**, not an error — a note that *should* carry a tag but doesn't simply drops out of recall. Prefer a template-set property over a hand-applied tag for anything load-bearing.
- **Title collisions are an overwrite hazard** — resolve to an exact path before writing.
