---
name: notes-workflow-efficiency
description: Performance patterns for vault operations — parallelizing reads, sequencing writes, batching metadata checks, and converting timestamps.
---

# Efficiency

**Parallelise read operations.** Independent reads — listing folders, fetching file metadata, reading notes — can all run in parallel. Batch them into a single message rather than waiting for each to complete before starting the next.

**Never parallelise write operations.** Note creation, appending, property changes, moves, and renames must run one at a time. Parallel writes risk race conditions and make it hard to catch errors or confirm results before the next step.

**Batch metadata checks with a loop.** When checking modification times across many files, use a single bash loop rather than one call per file:

```bash
for p in "01 Projects/Foo.md" "01 Projects/Bar.md"; do
  echo "=== $p ===" && obsidian file path="$p"
done
```

## File metadata and timestamps

Use `obsidian file path=` to get metadata including `created` and `modified` timestamps (Unix milliseconds):

```bash
obsidian file path="01 Projects/My Project.md"
# returns: path, name, extension, size, created, modified
```

Convert timestamps inline — don't make a separate follow-up call:

```bash
date -r $(( 1774463658790 / 1000 )) "+%Y-%m-%d %H:%M"
```
