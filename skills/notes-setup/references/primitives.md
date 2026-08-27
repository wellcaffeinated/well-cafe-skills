---
name: notes-setup-primitives
description: The reasoning model behind notes-setup — two readers (human + agent) and how each organizing primitive serves them. Used to justify structure proposals, not shown verbatim to the user.
---

# Primitives: the reasoning model

This is the agent's thinking aid for step 4 (translate use-cases to structure). Don't dump it on the user; use it to *justify* proposals.

## Two readers, inverted costs

- **The human** reads by recognition and space — glances at the tree, scans tags, feels the graph. Looking is free; *maintaining consistency* is costly.
- **The agent** reads by query and address — every look is a CLI call with a token cost. Looking is expensive; *consistency* is what makes looks cheap.

So Bases and properties are worth far more to the agent than the human; a rich graph is worth far more to the human. The best designs encode the *same fact* for both (e.g. status as a folder *and* a Base).

## Each primitive is an axis — match axis to need

| Primitive | Encodes | Human | Agent | Best for |
|-----------|---------|-------|-------|----------|
| **Folders** | one dominant axis (usually status/actionability) | strongest orientation; but single-membership, nesting rots | free signal in the path; can't infer *meaning* without docs | the one axis you filter your whole brain by |
| **Tags** | many cross-cutting axes (subject) | lightweight, multi-membership; but drift (`#css`/`#CSS`) | cross-cutting recall; but binary and **fails silently** when missing | topic membership across folders |
| **Properties** | typed attributes (`type`, `deadline`, `priority`) | semi-hidden; pays off via queries | keystone — real filtering, the substrate Bases query | machine-readable attributes to filter/sort |
| **Bases** | retrieval layer over properties | spreadsheet/dashboard payoff | one structured call replaces "list 200, read each" — biggest efficiency lever | any question asked repeatedly |
| **Links** | relationships between specific notes | associative, emergent, great for thinking | traversable, esp. a wikilink-valued property; but multi-hop | connection/discovery tasks |
| **Title** | the handle + link target | what you recall and click | resolves by name — **ambiguous on collision** (overwrite hazard) | human handle; not a classification axis |
| **Daily notes** | time / capture | frictionless scratchpad | predictable by date; `daily:read` only reaches today | zero-friction capture |

## Five principles

1. **Assign each axis of *their* thinking to the primitive that carries it best** — don't pick one primitive for everything.
2. **Serve both readers, often by encoding twice.** Redundancy across interfaces is a feature.
3. **Costs are inverted** — spend discipline where each reader's leverage is.
4. **Mind silent failure.** Tags/properties vanish quietly when inconsistent; folders fail loudly. Anything the agent will *query* must be applied consistently → templates.
5. **Small vocabulary, rich retrieval.** Few well-maintained types/properties feeding a few good Bases beats many fields nobody sets.

## The agent-as-processor resolution

Humans won't maintain discipline; agents need it. Resolve by making *consistency-manufacturing a workflow*: capture stays sloppy, the agent files/tags/links it into the queryable form it later depends on. Treat "the agent processes capture into structure" as a first-class, expected interaction.
