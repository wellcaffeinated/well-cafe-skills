---
type: reference
tags: [meta, system]
ai: true
---

# Type: {{type name}}

> Agent-facing. One note type, fully encapsulated. Create only if this type has real machinery (dedicated location, special frontmatter, or its own lifecycle). Otherwise keep it as a one-liner in a conventions doc.

## Location

{{Where notes of this type live, e.g. `Bookmarks/`. Link to `_Meta/conventions/where-things-go.md` for the *why*.}}

## Frontmatter

Source of truth is the template: `Templates/{{type}}.md`. Do not restate the YAML here — point at the template so they can't drift.

Key fields: {{`type`, `tags`, plus any type-specific fields and their meaning}}.

## Behavior

{{Creation flow, lifecycle, what links to it, any dashboard that reads it. Omit sections that don't apply.}}
