---
name: notes-setup-interview
description: Branching question sets for the notes-setup interview — adapts to Obsidian experience and existing vault state, surfaces options so newcomers can recognize what they want.
---

# The interview

Goal: let structure emerge from how the user wants to work. Use `AskUserQuestion` so users **recognize** options rather than invent them — newcomers often don't know what's possible. Honor the prose-then-pause rule: explain in one turn, ask in the next.

## Branch on calibration

- **New / dabbled** → more orientation, show concrete examples in each option's description, fewer questions per round, conservative defaults.
- **Regular user** → skip orientation; ask sharper questions; lead with "what's not working."
- **Existing vault** → read folders/notes first (`obsidian folders`, sample a few notes), then frame questions as "I see X — keep it / change it?" rather than building from zero.

## Question areas (pick what's relevant; don't ask all at once)

**Starting structure** — offer a *lens*, not a box. Especially for newcomers, name a few organizing philosophies so they can recognize what resonates (PARA, Zettelkasten, Johnny.Decimal, a navigable-hubs/MOC approach, or minimal flat+tags) — then customize from their use-cases. These are examples, not mandates; mixing is normal. See [philosophies](philosophies.md).

**Capture** — where do thoughts land?
- Daily note (one page per day) · an inbox folder · web clippings · straight into topic notes · not sure
- Follow-up: how messy is capture allowed to be? (Messier capture → stronger case for agent processing.)

**What they keep** — multiSelect:
- Bookmarks/links · project notes · reference/topic notes · reading queue · people · meetings · journal/personal · code snippets · incubating ideas (a "someday" holding stage)

**What they'll ask of it** — the retrieval needs that justify properties/Bases. multiSelect:
- "what's due / what's next" · "what should I read" · "what's stale / forgotten" · "what relates to X" · "what did I do this week" · "everything about project/person Y"

**Effortless interactions** — the one or two things that should feel frictionless. This drives the load-bearing plugin/template choices.

**Agent's role** — field-tested interactions:
- *Process* capture (file/tag/link the inbox & dailies into structure)?
- *Remember* across sessions (a bounded summary over append-only daily logs)?
- *Draft* into a staging area before you trust it?
- *Take requests* — flag a note with what you want done to it (an action-request property + a queue Base; see [patterns](patterns.md))?

**Devices** — already covered by sync posture in calibration; only revisit if it changes the structure (e.g. mobile-heavy capture).

## Turn answers into needs

Each "I want X to feel effortless" or "I'll ask Y" becomes a retrieval/action need. Carry the list into step 4, where each need is assigned to the cheapest primitive that serves both readers. If a need didn't surface, don't invent structure for it — and don't suggest a plugin for it.
