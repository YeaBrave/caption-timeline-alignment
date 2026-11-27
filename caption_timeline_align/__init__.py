"""Manuscript-first caption alignment: the script is the text, ASR only donates timing."""

from .align import AsrWord, Cue, TimeSource, align

__all__ = ["AsrWord", "Cue", "TimeSource", "align"]
__version__ = "0.1.0"
