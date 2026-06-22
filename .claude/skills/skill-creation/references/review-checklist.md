---
name: skill-creation-checklist
description: Pre-commit checklist for reviewing a skill's quality before merging.
---

# Skill Review Checklist

## Frontmatter

- [ ] `name` is kebab-case, matches the directory name
- [ ] `description` has two parts: summary + "Use when..." triggers
- [ ] `user-invocable: true` is set if the user should be able to invoke it directly
- [ ] `allowed-tools` lists only tools this skill actually needs
- [ ] `metadata.version` is set to today's date

## SKILL.md body

- [ ] Opens with a short context paragraph (what + why), not a list of instructions
- [ ] Operational sections use imperative, present-tense prose ("Do X", "Check Y before Z")
- [ ] Quick reference / common examples are inline (not hidden in a reference file)
- [ ] No section exceeds ~30 lines — longer sections belong in `references/`
- [ ] If this skill depends on another, "Before starting" section is the first content section
- [ ] Ends with a reference table if any `references/*.md` files exist

## Reference files

- [ ] Each file covers one concept
- [ ] File names use `{category}-{topic}.md` format
- [ ] Each file has its own frontmatter (name + description)
- [ ] Files are linked from the SKILL.md reference table

## Description quality check

Read the description aloud as if the user just said it. Ask: would Claude load this skill given that request?

Pick two or three realistic user phrasings for this skill and confirm the description's trigger phrases would match them. If a user said exactly what they wanted and the description wouldn't fire, the trigger phrases need work — not the user's phrasing.
