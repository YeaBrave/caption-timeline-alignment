from __future__ import annotations

import argparse
import json
from pathlib import Path

from .align import AsrWord, align


def _srt_timestamp(seconds: float) -> str:
    if seconds < 0:
        seconds = 0
    ms = int(round(seconds * 1000))
    hours, ms = divmod(ms, 3_600_000)
    minutes, ms = divmod(ms, 60_000)
    secs, ms = divmod(ms, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def cues_to_srt(cues) -> str:
    blocks = []
    for index, cue in enumerate(cues, 1):
        blocks.append(
            f"{index}\n{_srt_timestamp(cue.start)} --> {_srt_timestamp(cue.end)}\n{cue.text}\n"
        )
    return "\n".join(blocks).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Align a manuscript to ASR word timings and write subtitle cues."
    )
    parser.add_argument("--script", required=True, help="Path to the manuscript text file")
    parser.add_argument(
        "--asr",
        required=True,
        help="Path to a JSON list of {text|word, start, end}",
    )
    parser.add_argument("--duration", type=float, required=True, help="Audio duration in seconds")
    parser.add_argument("--out", required=True, help="Output .srt path")
    parser.add_argument("--max-chars", type=int, default=16)
    parser.add_argument("--max-duration", type=float, default=6.0)
    args = parser.parse_args(argv)

    script = Path(args.script).read_text(encoding="utf-8")
    raw = json.loads(Path(args.asr).read_text(encoding="utf-8"))
    words = []
    for item in raw:
        text = item.get("text", item.get("word", ""))
        words.append(AsrWord(text=text, start=float(item["start"]), end=float(item["end"])))
    result = align(script, words, args.duration, max_chars=args.max_chars, max_duration=args.max_duration)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(cues_to_srt(result.cues), encoding="utf-8")
    print(
        f"wrote {out} ({len(result.cues)} cues, "
        f"{result.matched_tokens}/{result.total_tokens} ASR words matched)"
    )
    return 0
