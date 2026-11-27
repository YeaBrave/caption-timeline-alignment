# 字幕アライメント研究

Subtitle Alignment Research

[中文](README.md) · [English](README.en.md) · [日本語](README.ja.md)

原稿が字幕テキストの唯一の出典であり、音声認識はタイミングだけを提供します。これは独立した「原稿優先」の字幕アライメント研究で、実行可能な参考実装を含み、特定の商用編集ソフトとは無関係です。

アルゴリズムの詳細は [docs/algorithm.ja.md](docs/algorithm.ja.md) を参照してください。

## デモ

このリポジトリに製品スクリーンショットはありません。以下の 3 つの SVG アニメーションはブラウザで再生できます。[docs/assets/preview.html](docs/assets/preview.html) を開くとまとめて確認できます。

- [原稿優先](docs/assets/manuscript-first.svg)：誤認識はスキップされ、字幕は原稿の文言を使います
- [時間の補完](docs/assets/time-fill.svg)：一致した区間は認識時間を使い、未一致の原稿は文字数で補間します
- [キュー分割](docs/assets/cue-split.svg)：2 つのアンカーの間の間（ま）を優先して分割します

## 考え方

1. 動的計画法で認識語を原稿に埋め戻し、一致を最大化しつつ、マッチできない区間はスキップできます。
2. 一致箇所は認識時間を使います。両端にアンカーがある隙間は文字数で補間し、推定として標記します。
3. 句読点、文字数、長さに応じて字幕キューへ分割します。

## 使い方

```bash
python3 -m caption_timeline_align --script examples/manuscript.txt --asr examples/words.json --duration 3 --out out.srt
python3 -m unittest
```

`words.json` はオブジェクトの配列で、各要素は `text`（または `word`）と、秒単位の `start`、`end` を持ちます。

任意の中国語分かち書き：

```bash
pip install 'caption-timeline-alignment[zh]'
```

jieba がない場合、中国語は文字単位で分割され、アライメントは実行できます。

## 謝辞

再利用や再配布の際は、本謝辞を残してください。詳細は [docs/CREDITS.md](docs/CREDITS.md) にあります。

| 名称 | ライセンス | 作者 / 出典 | 説明 |
| --- | --- | --- | --- |
| [Python](https://www.python.org/) | PSF License | Python Software Foundation | 実行環境 |
| [jieba](https://github.com/fxsjy/jieba) | MIT | Sun Junyi（`fxsjy`） | 任意の中国語分かち書き |
| [Claude](https://www.anthropic.com) | — | Anthropic | 公開文書と参考実装の整理を補助したツールであり、同梱の依存関係ではありません |

## ライセンス

このリポジトリは MIT ライセンスで公開しています。
