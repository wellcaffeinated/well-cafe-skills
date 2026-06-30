#!/usr/bin/env python3
"""yt2md — download YouTube subtitles and convert to RAG-ready markdown.

USAGE
    yt2md.py <youtube-url>

URL TYPES AND OUTPUT BEHAVIOUR
    Single video  (watch?v=, youtu.be/, /shorts/, /live/)
        Markdown is written to stdout. Redirect with > to save:
            yt2md.py 'https://www.youtube.com/watch?v=ID' > transcript.md
        Progress and warnings go to stderr so they don't corrupt the file.

    Channel or playlist  (@Channel/videos, /channel/ID, playlist?list=)
        One .md file per video is written to the current working directory,
        named  <YYYYMMDD> - <title>.md  (matching the upload date).
        Progress is reported on stderr. Nothing goes to stdout.

OUTPUT FORMAT
    Each .md file has YAML frontmatter (retrieved_at, upload_date, id, title,
    channel, duration_string, view_count, tags, webpage_url, etc.) followed by
    the transcript as prose paragraphs with sparse [mm:ss] timestamp markers
    at sentence boundaries roughly every 30 seconds, then the YouTube
    description after a horizontal rule.

TEMP FILES  (/tmp/yt2md/)
    Intermediate .en.json3 and .info.json files are downloaded here and
    deleted immediately after each video is converted. What remains:

        /tmp/yt2md/video/    — cleared after every single-video run
        /tmp/yt2md/channel/  — cleared after every channel run
        /tmp/yt2md/.downloaded.txt  — channel download archive (kept)

    The archive file makes channel runs resumable: re-running the same channel
    URL skips videos that were already converted. Delete it to re-fetch all.

OPTIONS
    -n N, --limit N
        For channels/playlists only: stop after N videos (most recent first).
        Ignored for single video URLs.

REQUIRES
    yt-dlp importable as a Python package (pip install yt-dlp).
    The binary alone (mise/brew) is not sufficient for the Python API.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    sys.exit("yt-dlp not found. Install with: mise use yt-dlp  # or: pip install yt-dlp")

# ── transcript conversion (mirrors to-rag.py) ─────────────────────────────────

TS_INTERVAL_SEC = 30

SLIM_FIELDS = (
    "id",
    "title",
    "channel",
    "channel_url",
    "uploader",
    "language",
    "duration_string",
    "view_count",
    "like_count",
    "comment_count",
    "tags",
    "categories",
    "thumbnail",
    "webpage_url",
    "chapters",
)

ANNOTATION_RE = re.compile(r"\s*\[[^\]]*[A-Za-z][^\]]*\]\s*")
SPEAKER_RE = re.compile(r"\s*>>+\s*")
FULLWIDTH_DROP = str.maketrans("", "", "？＂：＊＜＞｜／＼")


def clean_filename(name: str) -> str:
    name = name.translate(FULLWIDTH_DROP)
    name = re.sub(r"\s+", " ", name).strip()
    name = re.sub(r"\s*-\s*", " - ", name)
    return name


def safe_filename(name: str) -> str:
    """Produce a terminal-safe filename: ASCII only, spaces→hyphens, no shell specials."""
    name = clean_filename(name)
    # drop non-ASCII (emoji, accented chars, etc.)
    name = name.encode("ascii", errors="ignore").decode()
    # replace spaces with hyphens
    name = name.replace(" ", "-")
    # strip anything that isn't alphanumeric, hyphen, underscore, or dot
    name = re.sub(r"[^\w\-.]", "", name)
    # collapse runs of hyphens
    name = re.sub(r"-{2,}", "-", name)
    return name.strip("-")


def fmt_ts(seconds: int) -> str:
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def fmt_upload_date(yyyymmdd: str | None) -> str | None:
    if not yyyymmdd or len(yyyymmdd) != 8 or not yyyymmdd.isdigit():
        return yyyymmdd
    return f"{yyyymmdd[:4]}-{yyyymmdd[4:6]}-{yyyymmdd[6:]}"


def extract_transcript(events: list, ts_interval: int = TS_INTERVAL_SEC) -> str:
    parts: list[str] = ["[00:00] "]
    last_marker = 0

    for ev in events:
        segs = ev.get("segs")
        if not segs or ev.get("aAppend"):
            continue
        text = "".join(s.get("utf8", "") for s in segs)
        text = text.replace("\xa0", " ").replace("\n", " ")
        text = ANNOTATION_RE.sub(" ", text)
        text = SPEAKER_RE.sub(" ", text).strip()
        if not text:
            continue

        t = ev.get("tStartMs", 0) // 1000
        prev = parts[-1].rstrip() if parts else ""
        crossed = t - last_marker >= ts_interval
        sentence_end = prev.endswith((".", "!", "?"))

        if crossed and sentence_end:
            parts.append(f"\n\n[{fmt_ts(t)}] ")
            last_marker = t
        elif parts and not parts[-1].endswith((" ", "\n", "[")):
            parts.append(" ")

        parts.append(text)

    out = "".join(parts).strip()
    out = re.sub(r"[ \t]{2,}", " ", out)
    return out


def yaml_inline(v) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        return "[" + ", ".join(yaml_inline(x) for x in v) + "]"
    s = str(v).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


def sanitize_tag(tag: str) -> str:
    """Convert a YouTube tag to a valid Obsidian tag (snake_case, no special chars)."""
    tag = tag.lower()
    tag = re.sub(r"[\s\-]+", "_", tag)       # spaces and hyphens → underscore
    tag = re.sub(r"[^\w/]", "", tag)          # strip everything else (keep / for nested)
    tag = re.sub(r"_+", "_", tag)             # collapse runs
    return tag.strip("_")


def build_frontmatter(info: dict, retrieved_at: str) -> str:
    lines = ["---", f"retrieved_at: {retrieved_at}"]
    upload = fmt_upload_date(info.get("upload_date"))
    if upload:
        lines.append(f"upload_date: {upload}")
    for k in SLIM_FIELDS:
        v = info.get(k)
        if v is None:
            continue
        if k == "tags" and isinstance(v, list):
            v = [sanitize_tag(t) for t in v if t]
        lines.append(f"{k}: {yaml_inline(v)}")
    lines.append("---")
    return "\n".join(lines)


def to_markdown(json3_path: Path, info_path: Path, retrieved_at: str) -> str:
    info = json.loads(info_path.read_text())
    j3 = json.loads(json3_path.read_text())
    transcript = extract_transcript(j3.get("events", []))
    fm = build_frontmatter(info, retrieved_at)
    title = info.get("title", json3_path.stem)
    description = (info.get("description") or "").strip()

    body = f"{fm}\n\n# {title}\n\n{transcript}\n"
    if description:
        body += f"\n---\n\n## Description\n\n{description}\n"
    return body


# ── URL detection ──────────────────────────────────────────────────────────────

_SINGLE_VIDEO_RE = re.compile(
    r"youtube\.com/(?:watch\?(?:[^&]*&)*v=|shorts/|live/)|youtu\.be/"
)


def is_single_video(url: str) -> bool:
    return bool(_SINGLE_VIDEO_RE.search(url))


# ── download ──────────────────────────────────────────────────────────────────

TMP_DIR = Path("/tmp/yt2md")


class _StderrLogger:
    """Route all yt-dlp output to stderr so stdout stays clean for piping."""
    def debug(self, msg: str) -> None:
        if msg.startswith("[debug]"):
            return
        print(msg, file=sys.stderr)
    def info(self, msg: str) -> None:
        print(msg, file=sys.stderr)
    def warning(self, msg: str) -> None:
        print(msg, file=sys.stderr)
    def error(self, msg: str) -> None:
        print(msg, file=sys.stderr)


def _build_opts(out_dir: Path, archive: Path | None, limit: int | None = None) -> dict:
    opts: dict = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
        "subtitlesformat": "json3",
        "writeinfojson": True,
        "retries": 10,
        "extractor_retries": 5,
        # exponential backoff matching fetch.sh --retry-sleep exp=1:60
        "retry_sleep_functions": {
            "http": lambda n: min(2**n, 60),
            "fragment": lambda n: min(2**n, 60),
            "file_access": lambda n: min(2**n, 60),
        },
        "ignoreerrors": True,
        "nooverwrites": True,
        # sleep preset matching fetch.sh -t sleep comment
        "sleep_interval_subtitles": 5,
        "sleep_interval_requests": 0.75,
        "sleep_interval": 10,
        "max_sleep_interval": 20,
        "outtmpl": str(out_dir / "%(upload_date)s - %(title)s.%(ext)s"),
        "logger": _StderrLogger(),
        "noprogress": True,
    }
    if archive is not None:
        opts["download_archive"] = str(archive)
    if limit is not None:
        opts["playlistend"] = limit
    return opts


def _find_pairs(d: Path) -> list[tuple[Path, Path]]:
    pairs = []
    for j3 in sorted(d.glob("*.en.json3")):
        info = d / (j3.name[: -len(".en.json3")] + ".info.json")
        if info.exists():
            pairs.append((j3, info))
    return pairs


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False)
    parser.add_argument("url", nargs="?")
    parser.add_argument("-n", "--limit", type=int, metavar="N", help="Channel/playlist only: stop after N videos")
    parser.add_argument("-h", "--help", action="store_true")
    args = parser.parse_args()

    if args.help or not args.url:
        print(__doc__, file=sys.stderr)
        return 0 if args.help else 2

    url = args.url
    single = is_single_video(url)
    retrieved_at = date.today().isoformat()

    if single:
        tmp = TMP_DIR / "video"
        tmp.mkdir(parents=True, exist_ok=True)
        archive = None
    else:
        tmp = TMP_DIR / "channel"
        tmp.mkdir(parents=True, exist_ok=True)
        archive = TMP_DIR / ".downloaded.txt"

    limit = None if single else args.limit
    opts = _build_opts(tmp, archive, limit=limit)
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])

    pairs = _find_pairs(tmp)
    if not pairs:
        print("No subtitle files downloaded — check the URL or try again.", file=sys.stderr)
        return 1

    if single:
        j3, info_path = pairs[0]
        print(to_markdown(j3, info_path, retrieved_at), end="")
        j3.unlink(missing_ok=True)
        info_path.unlink(missing_ok=True)
    else:
        out_dir = Path.cwd()
        for j3, info_path in pairs:
            md = to_markdown(j3, info_path, retrieved_at)
            base = safe_filename(j3.name[: -len(".en.json3")])
            out = out_dir / f"{base}.md"
            out.write_text(md)
            print(out, file=sys.stderr)
            j3.unlink(missing_ok=True)
            info_path.unlink(missing_ok=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
