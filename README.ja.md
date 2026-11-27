# 字幕アライメント研究

**Subtitle Alignment Research / 字幕对齐算法研究**

[中文](README.md) · [English](README.en.md) · [日本語](README.ja.md)

原稿優先の字幕アライメント：原稿がテキストを担い、音声認識は時刻だけを提供します。これは独立した研究と、実行可能な参照実装です。いずれの商用編集ソフトとも無関係です。

オープンソースの依存関係、作者、および公開稿の整理を手伝った Claude（Anthropic）への謝辞は [docs/CREDITS.md](docs/CREDITS.md) にあります。再利用・再配布の際は、この謝辞を残してください。

## デモ

本リポジトリに製品スクリーンショットはありません。次の SVG アニメーションは、ブラウザでそのまま再生できます。

- [原稿優先](docs/assets/manuscript-first.svg)
- [時刻の埋め戻し](docs/assets/time-fill.svg)
- [字幕の分割](docs/assets/cue-split.svg)

[docs/assets/preview.html](docs/assets/preview.html) を開くと、まとめて確認できます。算法の説明は [docs/algorithm.ja.md](docs/algorithm.ja.md) にあります。

## 使い方

```bash
python3 -m caption_timeline_align --script examples/manuscript.txt --asr examples/words.json --duration 3 --out /tmp/out.srt
python3 -m unittest
```

`words.json` はオブジェクトのリストです。各要素は `text`（または `word`）と、秒単位の `start`・`end` を持ちます。

より良い中国語の分かち書きが必要な場合：

```bash
pip install 'caption-timeline-alignment[zh]'
```

jieba がない場合、中国語は文字単位で分割されます。中核のアライメント処理はそのまま動作します。

## ライセンス

MIT。第三者のライセンス、作者、ツールへの謝辞は [docs/CREDITS.md](docs/CREDITS.md) を参照してください。
