# Subtitle Alignment Research

**字幕对齐算法研究**

[中文](README.md) · [English](README.en.md) · [日本語](README.ja.md)

Manuscript-first caption alignment: the script supplies the text, and ASR donates only timing. This is an independent study with a runnable reference implementation. It is not affiliated with any commercial editor.

Open-source dependencies, authors, and a credit for Claude (Anthropic), which assisted in preparing the public writeup, are listed in [docs/CREDITS.md](docs/CREDITS.md). Please keep that list if you reuse or redistribute this work.

## Demo

This repository has no product screenshots. The following SVG animations play directly in a browser:

- [Manuscript first](docs/assets/manuscript-first.svg)
- [Time fill](docs/assets/time-fill.svg)
- [Cue split](docs/assets/cue-split.svg)

You can also open [docs/assets/preview.html](docs/assets/preview.html) to view them together. The algorithm note is in [docs/algorithm.en.md](docs/algorithm.en.md).

## Use

```bash
python3 -m caption_timeline_align --script examples/manuscript.txt --asr examples/words.json --duration 3 --out /tmp/out.srt
python3 -m unittest
```

`words.json` is a list of objects with `text` (or `word`), plus `start` and `end` in seconds.

For better Chinese word segmentation:

```bash
pip install 'caption-timeline-alignment[zh]'
```

Without jieba, Chinese is split at the character level. The core aligner still runs.

## License

MIT. Third-party licenses, authors, and tool acknowledgements are listed in [docs/CREDITS.md](docs/CREDITS.md).
