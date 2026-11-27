<div align="center">

中文 · [English](README.en.md) · [日本語](README.ja.md)

# 字幕对齐算法研究

### Subtitle Alignment Research

独立技术研究 · 文稿优先，识别只提供时间

</div>

---

已有完整文稿，也有一串带时间戳的识别词。这份研究说明如何把文稿对齐到时间轴上，再切成字幕条，并附带可独立运行的参考实现。

与任何商业剪辑软件无关。实现不含第三方二进制，也不包含逆向材料。

完整说明见 [中文算法说明](docs/algorithm.zh.md) 与 [English notes](docs/algorithm.en.md)。开源依赖、作者，以及整理文稿时使用的 Claude（Anthropic）见 [致谢](docs/CREDITS.md)。

## 原则

文稿是字幕文本的唯一来源。识别结果只提供时间；错误或同音的识别词不会写进字幕。

用动态规划把识别词嵌回文稿，尽量多地命中，同时允许跳过无法匹配的片段。命中处用识别词的起止时间回填；中间未命中的片段按字数插值，并标为估算。

再按句读、字数和时长切成字幕条。

## 演示

本仓库没有产品截图。下面三张 SVG 可在浏览器里直接播放：

- [文稿优先](docs/assets/manuscript-first.svg)
- [时间回填](docs/assets/time-fill.svg)
- [切条](docs/assets/cue-split.svg)

也可打开 [docs/assets/preview.html](docs/assets/preview.html) 一并查看。可运行的示例文稿和识别词在 `examples/`。

## 使用

```bash
python3 -m caption_timeline_align --script examples/manuscript.txt --asr examples/words.json --duration 3 --out out.srt
python3 -m unittest
```

`words.json` 是对象列表，字段为 `text`（或 `word`）、`start`、`end`，时间单位为秒。

可选中文分词：

```bash
pip install jieba
```

未安装 jieba 时，中文按字符切分，对齐算法仍可运行。

## 许可与致谢

本仓库以 [MIT](LICENSE) 授权。Python（PSF License，Python Software Foundation）、可选的 jieba（MIT，作者 Sun Junyi / fxsjy），以及整理公开文稿和参考实现时使用的 Claude（Anthropic）均写在 [docs/CREDITS.md](docs/CREDITS.md)。转载或再分发时请保留致谢。
