# 字幕对齐算法研究

**Subtitle Alignment Research**

Manuscript-first caption alignment: the script is the text, ASR only donates timing.

这是一份独立的文稿优先字幕对齐研究，附带可运行的参考实现。它与任何商业剪辑软件无关。多语言自述的排版版将另补；算法说明见 `docs/algorithm.zh.md` 与 `docs/algorithm.en.md`。

开源依赖、作者，以及整理文稿时使用的 Claude（Anthropic）致谢见 [docs/CREDITS.md](docs/CREDITS.md)，请保留。

## Demo

本仓库没有现成产品图。演示动画在 `docs/assets/`，用浏览器打开 [docs/assets/preview.html](docs/assets/preview.html) 即可播放：

- [文稿优先](docs/assets/manuscript-first.svg)
- [时间回填](docs/assets/time-fill.svg)
- [切条](docs/assets/cue-split.svg)

## Use

```bash
python3 -m caption_timeline_align --script examples/manuscript.txt --asr examples/words.json --duration 3 --out /tmp/out.srt
python3 -m unittest
```

`words.json` is a list of objects with `text` (or `word`), `start`, and `end` in seconds.

Optional Chinese word segmentation:

```bash
pip install jieba
```

## License

MIT. Third-party licenses, authors, and tool acknowledgements are listed in `docs/CREDITS.md`.
