# 字幕对齐算法研究

**Subtitle Alignment Research**

[中文](README.md) · [English](README.en.md) · [日本語](README.ja.md)

文稿优先的字幕对齐：文稿提供文本，识别结果只提供时间。这是一份独立研究，附带可运行的参考实现，与任何商业剪辑软件无关。

开源依赖、作者，以及整理文稿时使用的 Claude（Anthropic）见 [docs/CREDITS.md](docs/CREDITS.md)。转载或再分发时请保留致谢。

## 演示

本仓库没有现成产品图。下面三张是可在浏览器里直接播放的 SVG 动画：

- [文稿优先](docs/assets/manuscript-first.svg)
- [时间回填](docs/assets/time-fill.svg)
- [切条](docs/assets/cue-split.svg)

也可打开 [docs/assets/preview.html](docs/assets/preview.html) 一并查看。算法说明见 [docs/algorithm.zh.md](docs/algorithm.zh.md)。

## 使用

```bash
python3 -m caption_timeline_align --script examples/manuscript.txt --asr examples/words.json --duration 3 --out /tmp/out.srt
python3 -m unittest
```

`words.json` 是对象列表，字段为 `text`（或 `word`），以及秒为单位的 `start`、`end`。

如需更好的中文分词：

```bash
pip install 'caption-timeline-alignment[zh]'
```

未安装 jieba 时，中文按字符切分，核心对齐算法仍可运行。

## 许可证

MIT。第三方许可证、作者与工具致谢见 [docs/CREDITS.md](docs/CREDITS.md)。
