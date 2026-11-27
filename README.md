# 字幕对齐算法研究

Subtitle Alignment Research

[中文](README.md) · [English](README.en.md) · [日本語](README.ja.md)

文稿是字幕文本的唯一来源，识别结果只提供时间。这是一份独立的文稿优先对齐研究，附带可运行的参考实现，与任何商业剪辑软件无关。

完整算法说明见 [docs/algorithm.zh.md](docs/algorithm.zh.md)。

## 演示

仓库里没有产品截图。下面三张是可直接播放的 SVG 动画，用浏览器打开 [docs/assets/preview.html](docs/assets/preview.html) 即可一并查看。

- [文稿优先](docs/assets/manuscript-first.svg)：错误的识别词会被跳过，字幕仍用文稿原文
- [时间回填](docs/assets/time-fill.svg)：命中片段使用识别时间，未命中的文稿按字插值
- [切条](docs/assets/cue-split.svg)：优先在两个锚点之间的停顿处切开

## 思路

1. 用动态规划把识别词嵌回文稿，尽量多地命中，同时允许跳过无法匹配的片段。
2. 命中处使用识别时间；两端有锚点的空隙按字数插值，并标为估算。
3. 再按句读、字数和时长切成字幕条。

## 使用

```bash
python3 -m caption_timeline_align --script examples/manuscript.txt --asr examples/words.json --duration 3 --out out.srt
python3 -m unittest
```

`words.json` 是对象列表，每项包含 `text`（或 `word`），以及以秒计的 `start`、`end`。

可选中文分词：

```bash
pip install 'caption-timeline-alignment[zh]'
```

未安装 jieba 时，中文按字符切分，对齐仍可运行。

## 致谢

转载或再分发时请保留本致谢。完整说明见 [docs/CREDITS.md](docs/CREDITS.md)。

| 名称 | 许可证 | 作者 / 来源 | 说明 |
| --- | --- | --- | --- |
| [Python](https://www.python.org/) | PSF License | Python Software Foundation | 运行环境 |
| [jieba](https://github.com/fxsjy/jieba) | MIT | Sun Junyi（`fxsjy`） | 可选中文分词 |
| [Claude](https://www.anthropic.com) | — | Anthropic | 整理公开文稿和参考实现时的辅助工具，不是随仓库分发的依赖 |

## 许可

本仓库以 MIT 许可证发布。
