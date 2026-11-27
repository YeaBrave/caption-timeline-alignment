<div align="center">

[中文](README.md) · English · [日本語](README.ja.md)

# Subtitle Alignment Research

### 字幕对齐算法研究

Independent research · The manuscript is the text; recognition only donates timing

</div>

---

Given a complete manuscript and a sequence of recognized words with timestamps, this project explains how to align the manuscript to a timeline, split it into cues, and ships a runnable reference implementation.

It is not affiliated with any commercial video editor. The implementation includes no third-party binaries and no reverse-engineering materials.

Read the full notes in [English](docs/algorithm.en.md) and [中文](docs/algorithm.zh.md). Open-source credits, authors, and Claude (Anthropic), used while preparing the public writeup, are listed in [Acknowledgements](docs/CREDITS.md).

## Principles

The manuscript is the only source of subtitle text. Recognition contributes timing only; wrong or homophone words never enter the cues.

Dynamic programming nests recognized words back into the manuscript, maximizing hits while allowing unmatched spans to be skipped. Hits take the corresponding word start and end; unmatched spans between two anchors are interpolated by character weight and marked as estimates.

Cues are then split by sentence, length, and duration.

## Demo

This repository has no product screenshots. These SVG animations play directly in a browser:

- [Manuscript first](docs/assets/manuscript-first.svg)
- [Time fill](docs/assets/time-fill.svg)
- [Cue split](docs/assets/cue-split.svg)

Or open [docs/assets/preview.html](docs/assets/preview.html) to play them together. Runnable sample manuscript and recognized words are in `examples/`.

## Use

```bash
python3 -m caption_timeline_align --script examples/manuscript.txt --asr examples/words.json --duration 3 --out out.srt
python3 -m unittest
```

`words.json` is a list of objects with `text` (or `word`), `start`, and `end` in seconds.

Optional Chinese word segmentation:

```bash
pip install jieba
```

Without jieba, Chinese is split by character; the aligner still runs.

## License and acknowledgements

This repository is licensed under [MIT](LICENSE). Python (PSF License, Python Software Foundation), optional jieba (MIT, Sun Junyi / fxsjy), and Claude (Anthropic), used while preparing the public writeup and reference implementation, are listed in [docs/CREDITS.md](docs/CREDITS.md). Please keep the acknowledgements if you reuse or redistribute this work.
