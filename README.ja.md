<div align="center">

[中文](README.md) · [English](README.en.md) · 日本語

# 字幕アラインメント研究

### Subtitle Alignment Research

独立した技術研究 · 原稿が本文、認識は時刻だけを提供する

</div>

---

完成した原稿と、時刻付きの認識語列があるとき、原稿を時間軸に揃え、字幕キューへ分割する方法を説明し、単独で実行できる参照実装を添えています。

いかなる商用映像編集ソフトとも無関係です。実装に第三者のバイナリは含まず、リバースエンジニアリング資料も含みません。

全文は [中文アルゴリズム説明](docs/algorithm.zh.md) と [English notes](docs/algorithm.en.md) を参照してください。オープンソースのクレジット、著者、および公開文の整理に用いた Claude（Anthropic）は [謝辞](docs/CREDITS.md) にあります。

## 原則

原稿は字幕テキストの唯一の出典です。認識結果は時刻だけを提供し、誤認識や同音の語は字幕に入りません。

動的計画法で認識語を原稿へ埋め戻し、命中を最大化しつつ、一致しない区間はスキップできます。命中箇所は当該認識語の開始と終了を用い、二つのアンカーの間の未命中区間は字数で補間し、推定と印を付けます。

その後、句読点、字数、長さに応じてキューへ分割します。

## デモ

本リポジトリに製品スクリーンショットはありません。次の SVG はブラウザでそのまま再生できます。

- [原稿優先](docs/assets/manuscript-first.svg)
- [時刻の埋め戻し](docs/assets/time-fill.svg)
- [キュー分割](docs/assets/cue-split.svg)

[docs/assets/preview.html](docs/assets/preview.html) を開けばまとめて確認できます。実行可能な原稿と認識語の例は `examples/` にあります。

## 使い方

```bash
python3 -m caption_timeline_align --script examples/manuscript.txt --asr examples/words.json --duration 3 --out out.srt
python3 -m unittest
```

`words.json` はオブジェクトの配列で、フィールドは `text`（または `word`）、`start`、`end`、単位は秒です。

中国語の分かち書きは任意です。

```bash
pip install jieba
```

jieba がない場合、中国語は文字単位で切ります。アラインメント自体は実行できます。

## ライセンスと謝辞

本リポジトリは [MIT](LICENSE) です。Python（PSF License、Python Software Foundation）、任意依存の jieba（MIT、作者 Sun Junyi / fxsjy）、および公開文と参照実装の整理に用いた Claude（Anthropic）は [docs/CREDITS.md](docs/CREDITS.md) に記載しています。再利用・再配布の際は謝辞を残してください。
