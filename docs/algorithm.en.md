# Subtitle Alignment Research

字幕对齐算法研究

[中文](algorithm.zh.md) · [English](algorithm.en.md) · [日本語](algorithm.ja.md)

This is an independent, manuscript-first description of caption alignment, with a runnable reference implementation. The problem is: given a complete manuscript and a sequence of recognized words with timestamps, align the manuscript to a timeline and split it into cues.

Principles:

1. **The manuscript is the only source of subtitle text.** Recognition contributes timing only. Wrong or homophone words never enter the cues.
2. **Dynamic programming nests recognized words back into the manuscript.** The manuscript is a character sequence. Each recognized word is an exact substring to be matched. The objective is to maximize hits, while allowing unmatched manuscript spans or unmatchable recognized words to be skipped.
3. **Times are filled in from hits.** Matched spans use the corresponding word start and end. Unmatched spans between two anchors are interpolated by character weight and marked estimated. Spans without anchors are marked unalignable, but the manuscript text and order are preserved.
4. **Cues are then split by sentence, length, and duration.** Splits prefer pauses between two anchors. Short cues may merge without exceeding the character limit. Gaps between cues can be closed; overlaps are reported and not rewritten.

This document describes an independently implementable method. It does not include commercial binaries, memory addresses, internal symbols, or unpacking steps.

Optional Chinese segmentation credits are listed in [CREDITS.md](CREDITS.md).

## Demo animations

This repository has no product screenshots. These SVG animations can be opened in a browser and correspond to the steps above:

- [Manuscript first](assets/manuscript-first.svg)
- [Time fill](assets/time-fill.svg)
- [Cue split](assets/cue-split.svg)

Or open [assets/preview.html](assets/preview.html) to play them together.
