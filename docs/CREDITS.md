# Acknowledgements / 致谢

This project’s core library uses only the Python standard library. Optional Chinese word segmentation, when enabled, depends on jieba. Please keep this list when you reuse or redistribute the project.

本项目核心实现只依赖 Python 标准库。若启用中文分词，会用到 jieba。转载或再分发时请保留本致谢。

## Software / 开源软件

| Project | License | Author / Source | Role |
| --- | --- | --- | --- |
| [Python](https://www.python.org/) | PSF License | Python Software Foundation | Runtime |
| [jieba](https://github.com/fxsjy/jieba) | MIT | Sun Junyi (`fxsjy`) | Optional Chinese word segmentation |

jieba is optional (`pip install 'caption-timeline-alignment[zh]'`). The aligner still runs without it, using a simpler character-level split for CJK text.

jieba 为可选依赖。未安装时，中文按字符切分，核心对齐算法仍可运行。

## Tools / 工具

| Name | Author / Source | Role |
| --- | --- | --- |
| [Claude](https://www.anthropic.com) | Anthropic | Assistance while preparing the public writeup and the reference implementation |

Claude is a product of Anthropic, PBC. It is credited here as a tool used in preparing this public package, not as a shipped software dependency.

Claude 是 Anthropic, PBC 的产品。此处作为整理公开文稿和参考实现时使用的辅助工具致谢，不是随仓库分发的软件依赖。

## Notes

- This repository is an independent implementation of manuscript-first caption alignment. It is not affiliated with any commercial video editor, and it does not include third-party binaries, trademarks in the project title, or reverse-engineering materials.
- 本仓库是独立的「文稿优先」字幕对齐实现，与任何商业剪辑软件无关，不含第三方二进制、不以商标作为项目标题，也不包含逆向材料。
