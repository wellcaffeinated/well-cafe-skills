---
name: youtube-transcript
description: Fetches YouTube transcripts as markdown using a bundled script. Use this skill whenever a YouTube transcript is needed — whether the user asks for one directly, pastes a YouTube URL and wants its content, or a transcript would help with the current task (summarising, note-taking, vault ingestion, RAG, etc.).
user-invocable: true
arguments: [url]
metadata:
  version: "2026-06-30"
---

# YouTube Transcript

Downloads YouTube auto-captions and converts them to structured markdown via a bundled Python script. Single video → stdout (pipe to a file). Channel or playlist → one `.md` file per video written to the current directory.

**URL:** `$url` — if empty, ask the user for the URL before proceeding.

The bundled script is at `${CLAUDE_SKILL_DIR}/scripts/yt2md.py`.

## 1. Check the dependency

The script imports `yt_dlp` as a Python package. A binary install (mise, brew) is not enough — it must be importable:

```bash
python3 -c "import yt_dlp; print(yt_dlp.version.__version__)"
```

If this errors, install it — try in order until one succeeds:

```bash
pip install yt-dlp                           # standard
pip3 install yt-dlp                          # if pip resolves to Python 2
pip install --user yt-dlp                    # no admin rights needed
pip install --break-system-packages yt-dlp  # system Python on Arch/Debian/Ubuntu
python3 -m pip install yt-dlp               # explicit interpreter fallback
```

Re-run the import check after installing before proceeding.

## 2. Run the script

Always quote URLs — `?` is a glob character in zsh/bash.

**Single video → stdout** (redirect to save):
```bash
python3 '${CLAUDE_SKILL_DIR}/scripts/yt2md.py' 'https://www.youtube.com/watch?v=ID' > transcript.md
```

**Channel or playlist → .md files in the current directory:**
```bash
python3 '${CLAUDE_SKILL_DIR}/scripts/yt2md.py' 'https://www.youtube.com/@Channel/videos'
python3 '${CLAUDE_SKILL_DIR}/scripts/yt2md.py' -n 5 'https://www.youtube.com/@Channel/videos'
```

`-n N` caps the run to the N most recent videos. Ignored for single video URLs.

Print full usage docs:
```bash
python3 '${CLAUDE_SKILL_DIR}/scripts/yt2md.py'
```

## URL patterns

| Type | Recognised forms |
|------|-----------------|
| Single video | `youtube.com/watch?v=ID` · `youtu.be/ID` · `/shorts/ID` · `/live/ID` |
| Channel | `youtube.com/@Name/videos` · `youtube.com/channel/ID` |
| Playlist | `youtube.com/playlist?list=ID` |

## Output format

Each file has YAML frontmatter (`retrieved_at`, `upload_date`, `id`, `title`, `channel`, `duration_string`, `view_count`, `tags`, `webpage_url`) followed by the transcript as prose paragraphs with `[mm:ss]` timestamp markers every ~30 seconds, then the YouTube description after `---`.

Channel output filenames are terminal-safe: `YYYYMMDD-Title-Of-Video.md`.

## Temp files

Intermediate files go to `/tmp/yt2md/` and are deleted after each video converts. The channel archive at `/tmp/yt2md/.downloaded.txt` persists so re-running the same channel URL skips already-converted videos. Delete it to re-fetch everything.
