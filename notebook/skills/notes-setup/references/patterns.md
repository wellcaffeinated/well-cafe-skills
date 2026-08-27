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

Cross-session memory for the agent, kept in `_Meta/` and distinct from the human's knowledge. Two surfaces shaped by one CLI fact: `obsidian read` is **whole-file only** — no tail, no line-range, no section read — so an unbounded log you read back is a cost trap. The fix is a **bounded summary** (read every session) over **append-only daily logs** (the source of truth, never read whole).

**`_Meta/summary.md` — the bounded, load-first cache.** Read it first every session. A `checkpoint:` frontmatter field records the last *completed* day already folded in; two sections split durable from volatile:

```markdown
---
ai: true
type: agent-summary
checkpoint: 2026-06-27        # last completed log folded in
updated: 2026-06-28
---
## Long-term      # conventions, stable project state, lasting threads
## Short-term     # recent activity + open threads; pruned as it ages
```

**`_Meta/log/YYYY-MM-DD.md` — append-only daily logs.** One file per day, `type: agent-log`. Write *eagerly*, the moment something consequential happens (create / move / decision / open-thread change — not every read), so the log survives an abrupt session end. The day's first write must `create` the file (**`append` silently no-ops with exit 0 if the file doesn't exist** — it will not bootstrap); `append` thereafter.

**Update by reconciling at session *start*, not session end.** An agent gets no reliable "session over" signal, so don't hang persistence on one. Instead, every session begins:

1. `property:read name="checkpoint" path="_Meta/summary.md"` and `files folder="_Meta/log"`.
2. **Gap = logs dated `> checkpoint` and `< today`.** If empty, skip straight to the user's request — no fold needed.
3. Otherwise `read` *only the gap logs* (never the whole history): fold their salience into **Short-term**, promote durable items to **Long-term**, prune stale Short-term entries.
4. `create … overwrite` the summary with `checkpoint` advanced to the latest folded date.

Today's log is never the checkpoint *during* today (the "today can never be processed" rule) — it's folded on the next day's first session. This makes the summary self-healing: a missed update just means a larger gap next start, and the logs remain the source of truth. Cost stays flat — each start reads one bounded summary plus only the days since last use, never the full history.

**Keep agent memory out of content searches.** All memory lives under `_Meta/`, so append `-path:_Meta` to any search for *user* content — one operator drops the logs and the summary regardless of type. (Property exclusion like `-["type":"agent-log"]` works too but only removes that one type, so you'd have to enumerate every agent type; the folder boundary is why `_Meta/` earns its own folder.)

**If accepted, write the operating rules into the vault's `VAULT.md`.** The reconciliation routine, the eager-logging cadence, and the `-path:_Meta` search rule are per-session instructions the agent must follow to use this at all — they only take effect if they live where the agent reads them every session. State plainly in `VAULT.md`: read `_Meta/summary.md` first, reconcile the gap before working, log consequential actions to today's `_Meta/log/` file, and exclude `_Meta/` from user-content searches. Without that, the structure exists but nothing drives it.

Only set this up if the user wants cross-session continuity — and note it overlaps with Claude Code's own memory, so it's worth the ceremony mainly when the memory must travel across machines or agents.

## Retrieval-friendly writing

- **H2 chunking** — write notes in `##` sections; each becomes an independently retrievable unit. Serves the human (scannable) and the agent (smaller hits).

## Privacy

Hiding files within a vault is symmetric — the agent and the human read the *same* vault, so anything hidden from the agent is hidden from the human in Obsidian too. The clean answer is separation, not concealment:

- **Separate vault for private notes** — if the user wants notes the agent never touches, keep them in a *different* vault whose `VAULT.md` simply says "this vault is private — do not use it." The agent steers clear by instruction, and the notes stay fully usable in Obsidian.

## Asking the agent for work

- **Action-request property** — a single property whose *value names a task* the user wants the agent to do with the note (e.g. `triage: percolate | draft | research | connect`). A Base grouped by that value becomes the agent's inbound queue — "here's everything you asked me to develop / write up / research." The inverse of a staging gate (which holds agent *output*); this holds human *requests*. Keep the vocabulary short and the values verbs.
- **Processing-state flag** — a boolean like `processed: true` marking "I've reviewed this" on a capture surface (a daily note, an inbox item). Unset = still to review. A "today's note can never be processed" rule stops an in-progress day from showing as done. Lets a Base split the reviewed from the backlog.

## Surfacing what you'd forget

- **Staleness view** — a Base formula such as `days_since: (now() - file.mtime).days`, plus a view filtered to large values, resurfaces notes untouched for a while: forgotten ideas, stale projects, reading never returned to. The cheapest answer to "what have I lost track of?" — the agent reads it in one call instead of crawling the vault.

## Views over `ai:` provenance

- Once notes carry `ai: true`, a Base view filtered `ai != true` gives a **human-only** lens (the user's authentic thinking) and `ai == true` gives an **AI-only** lens — the consumption side of the provenance mark in [Provenance & trust](#provenance--trust).

## A few more lightweight conventions

- **Numbered folders for custom ordering** — offer *only if* the user wants their folders in a deliberate order rather than alphabetical. Prefix each top-level folder with a number (`00 Inbox/`, `01 Projects/`, … `99 Meta/`) so Obsidian sorts by the number: frequent/capture folders up top, archive and agent-facing meta at the bottom (`99` keeps Meta last, out of the way of human browsing). It's all-or-nothing — number *every* top-level folder or none; a lone numbered folder among un-numbered ones orders nothing and just looks orphaned. If they don't want this, default to un-numbered names with a `_` prefix on system folders (`_Meta/`, `_Dashboard/`), which sorts them away from daily content without imposing an order.
- **Incubation type/stage** — a holding `type` (e.g. `seed`) for an idea not yet worth a project, parked until it's ready; a staleness view can resurface it for a second look.
- **Dual-reader inline hints** — a note can carry an agent hint as an HTML comment (`<!-- … -->`, invisible to the human reader) alongside a human hint in plain prose. Both readers, one place.
- **Index / home note for a folder-entity** — when a thing is a *folder* of notes (a project, a topic), give it a home note matching the folder name (a Map of Content). The agent reads the home note first; the human gets an obvious entry point.

## Footguns to encode defensively

- **String `"true"` ≠ boolean `true`.** `property:set` writes a string unless you pass `type=` (`type=checkbox` for booleans; also `number`, `date`, `datetime`, `list`). A base filtering on a boolean silently skips string values. Re-run the query after setting.
- **A missing tag is invisible**, not an error — a note that *should* carry a tag but doesn't simply drops out of recall. Prefer a template-set property over a hand-applied tag for anything load-bearing.
- **Title collisions are an overwrite hazard** — resolve to an exact path before writing.
