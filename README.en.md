# Subtitle Alignment Research

字幕对齐算法研究

[中文](README.md) · [English](README.en.md) · [日本語](README.ja.md)

The manuscript is the only source of subtitle text; recognition contributes timing only. This is an independent, manuscript-first alignment study with a runnable reference implementation. It is not affiliated with any commercial video editor.

The full method is in [docs/algorithm.en.md](docs/algorithm.en.md).

## Demo

This repository has no product screenshots. The three SVG animations below play in a browser. Open [docs/assets/preview.html](docs/assets/preview.html) to view them together.

- [Manuscript first](docs/assets/manuscript-first.svg): unmatched recognition is skipped; cues still use the manuscript
- [Time fill](docs/assets/time-fill.svg): hits use recognized times; unmatched spans are interpolated by character
- [Cue split](docs/assets/cue-split.svg): splits prefer pauses between two anchors

## Approach

1. Dynamic programming nests recognized words back into the manuscript, maximizing hits while allowing unmatched spans to be skipped.
2. Hits keep their recognized times. Gaps between two anchors are interpolated by character weight and marked as estimates.
3. Cues are then split by sentence, length, and duration.

## Usage

```bash
python3 -m caption_timeline_align --script examples/manuscript.txt --asr examples/words.json --duration 3 --out out.srt
python3 -m unittest
```

`words.json` is a list of objects with `text` (or `word`), plus `start` and `end` in seconds.

Optional Chinese word segmentation:

```bash
pip install 'caption-timeline-alignment[zh]'
```

Without jieba, Chinese text is split by character and alignment still runs.

## Acknowledgements

Please keep this list when you reuse or redistribute the project. Full notes are in [docs/CREDITS.md](docs/CREDITS.md).

| Name | License | Author / Source | Role |
| --- | --- | --- | --- |
| [Python](https://www.python.org/) | PSF License | Python Software Foundation | Runtime |
| [jieba](https://github.com/fxsjy/jieba) | MIT | Sun Junyi (`fxsjy`) | Optional Chinese word segmentation |
| [Claude](https://www.anthropic.com) | — | Anthropic | Assistance while preparing the public writeup and reference implementation; not a shipped dependency |

## License

This repository is released under the MIT License.
