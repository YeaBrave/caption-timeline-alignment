from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import math
from typing import Iterable

PUNCT = set(
    "，。！？；：、, .!?;: \t\n\r“”‘’\"'（）()【】《》—…·•～～-–－"
)


def is_punct_or_space(ch: str) -> bool:
    return ch in PUNCT or ch.isspace()


def visible_text(text: str) -> str:
    return "".join(ch for ch in text if not is_punct_or_space(ch))


def display_len(text: str) -> int:
    return len(visible_text(text))


def is_cjk(ch: str) -> bool:
    code = ord(ch)
    return (
        0x4E00 <= code <= 0x9FFF
        or 0x3400 <= code <= 0x4DBF
        or 0x20000 <= code <= 0x2A6DF
    )


def strip_for_dp(raw: str) -> str:
    return "".join(ch for ch in raw if not is_punct_or_space(ch)).strip()


class TimeSource(str, Enum):
    ASR_ANCHOR = "asr_anchor"
    ESTIMATED = "estimated"
    UNALIGNABLE = "unalignable"


@dataclass(frozen=True)
class AsrWord:
    text: str
    start: float
    end: float


@dataclass
class Cue:
    start: float
    end: float
    text: str
    words: list[AsrWord] = field(default_factory=list)


@dataclass
class ScriptToken:
    text: str
    script_start: int
    script_end: int
    start: float = 0.0
    end: float = 0.0
    time_source: TimeSource = TimeSource.UNALIGNABLE
    asr_indices: list[int] = field(default_factory=list)


@dataclass(frozen=True)
class MatchSpan:
    script_start: int
    script_end: int
    asr_index: int
    asr_start: float
    asr_end: float


@dataclass
class AlignResult:
    script: str
    cues: list[Cue]
    engine: str
    matched_tokens: int
    total_tokens: int
    estimated_tokens: int
    unalignable_tokens: int


def tokenize_script(script: str, use_jieba: bool = True) -> list[ScriptToken]:
    chars = list(script)
    words: list[ScriptToken] = []
    cursor = 0
    cutter = _jieba_cutter() if use_jieba else None
    while cursor < len(chars):
        start = cursor
        if is_cjk(chars[cursor]):
            while cursor < len(chars) and is_cjk(chars[cursor]):
                cursor += 1
            run = "".join(chars[start:cursor])
            pieces = cutter(run) if cutter else list(run)
            offset = start
            for piece in pieces:
                end = offset + len(piece)
                words.append(ScriptToken(text=piece, script_start=offset, script_end=end))
                offset = end
        elif chars[cursor].isalnum() and chars[cursor].isascii():
            while cursor < len(chars) and chars[cursor].isascii() and chars[cursor].isalnum():
                cursor += 1
            words.append(ScriptToken(text="".join(chars[start:cursor]), script_start=start, script_end=cursor))
        else:
            cursor += 1
            if words:
                words[-1].text += chars[start]
                words[-1].script_end = cursor
            else:
                while (
                    cursor < len(chars)
                    and not is_cjk(chars[cursor])
                    and not (chars[cursor].isascii() and chars[cursor].isalnum())
                ):
                    cursor += 1
                words.append(ScriptToken(text="".join(chars[start:cursor]), script_start=start, script_end=cursor))
    return words


def _jieba_cutter():
    try:
        import jieba
    except ImportError:
        return None

    def cut(run: str) -> list[str]:
        return list(jieba.cut(run, cut_all=False))

    return cut


def dp_spans(script: str, words: list[AsrWord]) -> list[MatchSpan]:
    caps = list(script)
    tokens = [list(strip_for_dp(word.text)) for word in words]
    m, n = len(caps), len(tokens)
    score = [[0] * (n + 1) for _ in range(m + 1)]
    action = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 and j == 0:
                continue
            if i > 0:
                score[i][j] = score[i - 1][j]
            if j > 0 and (score[i][j - 1] > score[i][j] or i == 0):
                score[i][j] = score[i][j - 1]
                action[i][j] = 1
            token = tokens[j - 1] if j > 0 else []
            if j > 0 and token and i >= len(token) and caps[i - len(token) : i] == token:
                candidate = score[i - len(token)][j - 1] + 1
                if candidate > score[i][j]:
                    score[i][j] = candidate
                    action[i][j] = 2
    spans: list[MatchSpan] = []
    i, j = m, n
    while i > 0 or j > 0:
        act = action[i][j]
        if act == 0 and i > 0:
            i -= 1
        elif act == 1 and j > 0:
            j -= 1
        elif act == 2 and j > 0:
            length = len(tokens[j - 1])
            spans.append(
                MatchSpan(
                    script_start=i - length,
                    script_end=i,
                    asr_index=j - 1,
                    asr_start=words[j - 1].start,
                    asr_end=words[j - 1].end,
                )
            )
            i -= length
            j -= 1
        else:
            break
    spans.reverse()
    return spans


def assign_times(script: str, tokens: list[ScriptToken], spans: list[MatchSpan], duration: float) -> None:
    chars = list(script)
    for token in tokens:
        relevant = [
            span
            for span in spans
            if span.script_end > token.script_start and span.script_start < token.script_end
        ]
        needed = [
            index
            for index in range(token.script_start, token.script_end)
            if not is_punct_or_space(chars[index])
        ]
        fully_covered = bool(needed) and all(
            any(span.script_start <= index < span.script_end for span in relevant)
            for index in needed
        )
        if not fully_covered or not relevant:
            continue
        first, last = relevant[0], relevant[-1]
        first_offset = max(token.script_start, first.script_start) - first.script_start
        last_offset = min(token.script_end, last.script_end) - last.script_start
        first_len = first.script_end - first.script_start
        last_len = last.script_end - last.script_start
        token.start = first.asr_start + (first.asr_end - first.asr_start) * first_offset / first_len
        token.end = last.asr_start + (last.asr_end - last.asr_start) * last_offset / last_len
        token.asr_indices = [span.asr_index for span in relevant]
        token.time_source = (
            TimeSource.ASR_ANCHOR
            if first_offset == 0 and last_offset == last_len
            else TimeSource.ESTIMATED
        )

    cursor = 0
    while cursor < len(tokens):
        if tokens[cursor].end > tokens[cursor].start:
            cursor += 1
            continue
        start = cursor
        while cursor < len(tokens) and tokens[cursor].end <= tokens[cursor].start:
            cursor += 1
        left = tokens[start - 1].end if start else None
        right = tokens[cursor].start if cursor < len(tokens) else None
        window_start = left if left is not None else 0.0
        window_end = right if right is not None else duration
        both_anchors = left is not None and right is not None and window_end > window_start
        if window_end <= window_start:
            anchor = tokens[cursor] if cursor < len(tokens) else tokens[start - 1] if start else None
            if anchor is not None:
                window_start, window_end = anchor.start, anchor.end
            else:
                window_start, window_end = 0.0, duration
        weights = [max(display_len(token.text), 1) for token in tokens[start:cursor]]
        total = float(sum(weights))
        done = 0
        for offset, weight in enumerate(weights):
            word = tokens[start + offset]
            word.start = window_start + (window_end - window_start) * done / total
            done += weight
            word.end = window_start + (window_end - window_start) * done / total
            word.time_source = TimeSource.ESTIMATED if both_anchors else TimeSource.UNALIGNABLE


def sentence_ranges(words: list[ScriptToken]) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    start = 0
    for index, word in enumerate(words):
        if any(ch in word.text for ch in "。！？；.!?;\n"):
            ranges.append((start, index + 1))
            start = index + 1
    if start < len(words):
        ranges.append((start, len(words)))
    return ranges


def _raw_text(words: Iterable[ScriptToken]) -> str:
    return "".join(word.text for word in words)


def _cue(words: list[ScriptToken]) -> Cue:
    return Cue(
        start=words[0].start if words else 0.0,
        end=words[-1].end if words else 0.0,
        text=_raw_text(words),
        words=[AsrWord(text=word.text, start=word.start, end=word.end) for word in words],
    )


def split_range(
    words: list[ScriptToken],
    start: int,
    end: int,
    max_chars: int,
    max_duration: float,
    out: list[Cue],
) -> None:
    if start >= end:
        return
    length = display_len(_raw_text(words[start:end]))
    duration = words[end - 1].end - words[start].start
    if end - start == 1 or (length <= max_chars and duration <= max_duration):
        out.append(_cue(words[start:end]))
        return
    pause = None
    for index in range(start + 1, end):
        left, right = words[index - 1], words[index]
        if left.time_source != TimeSource.ASR_ANCHOR or right.time_source != TimeSource.ASR_ANCHOR:
            continue
        gap = right.start - left.end
        if gap >= 0.15 and (pause is None or gap > pause[0]):
            pause = (gap, index)
    if pause is not None:
        _, index = pause
        split_range(words, start, index, max_chars, max_duration, out)
        split_range(words, index, end, max_chars, max_duration, out)
        return
    parts_by_length = (length + max_chars - 1) // max_chars
    parts_by_time = max(math.ceil(duration / max_duration), 1) if max_duration > 0 else 1
    target = (length + max(parts_by_length, parts_by_time, 1) - 1) // max(parts_by_length, parts_by_time, 1)
    best = None
    for index in range(start + 1, end):
        chars = display_len(_raw_text(words[start:index]))
        if chars > max_chars:
            break
        cost = abs(chars - target)
        if best is None or cost < best[0]:
            best = (cost, index)
    index = best[1] if best is not None else start + 1
    split_range(words, start, index, max_chars, max_duration, out)
    split_range(words, index, end, max_chars, max_duration, out)


def merge_short(cues: list[Cue], max_chars: int) -> list[Cue]:
    merged: list[Cue] = []
    for cue in cues:
        if merged and cue.end - cue.start < 0.35 and display_len(merged[-1].text + cue.text) <= max_chars:
            previous = merged[-1]
            previous.end = max(previous.end, cue.end)
            previous.text += cue.text
            previous.words.extend(cue.words)
        else:
            merged.append(
                Cue(start=cue.start, end=cue.end, text=cue.text, words=list(cue.words))
            )
    return merged


def snap_match_edges(cues: list[Cue], words: list[ScriptToken]) -> list[Cue]:
    cursor = 0
    for cue in cues:
        end = cursor + len(cue.words)
        if cursor < len(words) and words[cursor].time_source == TimeSource.ASR_ANCHOR:
            cue.start = words[cursor].start
        if 0 < end <= len(words) and words[end - 1].time_source == TimeSource.ASR_ANCHOR:
            cue.end = words[end - 1].end
        cursor = end
    return cues


def close_gaps(cues: list[Cue]) -> list[Cue]:
    if len(cues) < 2:
        return cues
    closed = [Cue(start=c.start, end=c.end, text=c.text, words=list(c.words)) for c in cues]
    for index in range(len(closed) - 1):
        if closed[index].end < closed[index + 1].start:
            closed[index].end = closed[index + 1].start
    return closed


def validate(script: str, cues: list[Cue], max_chars: int) -> None:
    joined = "".join(visible_text(cue.text) for cue in cues)
    expected = visible_text(script)
    if joined != expected:
        raise ValueError("aligned cues no longer match the manuscript")
    for cue in cues:
        if display_len(cue.text) > max_chars:
            raise ValueError("a cue is longer than the character limit")
        if cue.end + 1e-9 < cue.start:
            raise ValueError("a cue has a reversed time range")


def align(
    script: str,
    asr_words: list[AsrWord],
    duration: float,
    max_chars: int = 16,
    max_duration: float = 6.0,
) -> AlignResult:
    if duration <= 0 or duration != duration:
        raise ValueError("audio duration must be a positive number")
    words: list[AsrWord] = []
    for index, word in enumerate(asr_words):
        if word.start != word.start or word.end != word.end or word.start < 0 or word.end < word.start:
            raise ValueError(f"ASR word {index + 1} has an invalid timestamp")
        if word.end > duration + 0.05:
            raise ValueError(f"ASR word {index + 1} extends past the audio duration")
        words.append(word)

    tokens = tokenize_script(script)
    spans = dp_spans(script, words)
    assign_times(script, tokens, spans, duration)
    split_cues: list[Cue] = []
    for start, end in sentence_ranges(tokens):
        split_range(tokens, start, end, max_chars, max_duration, split_cues)
    merged = merge_short(split_cues, max_chars)
    snapped = snap_match_edges(merged, tokens)
    cleaned: list[Cue] = []
    for cue in snapped:
        text = visible_text(cue.text)
        if not text:
            continue
        cleaned.append(Cue(start=cue.start, end=cue.end, text=text, words=list(cue.words)))
    validate(script, cleaned, max_chars)
    final = close_gaps(cleaned)
    validate(script, final, max_chars)
    estimated = sum(1 for token in tokens if token.time_source == TimeSource.ESTIMATED)
    unalignable = sum(1 for token in tokens if token.time_source == TimeSource.UNALIGNABLE)
    return AlignResult(
        script=script,
        cues=final,
        engine="manuscript-dp",
        matched_tokens=len(spans),
        total_tokens=len(words),
        estimated_tokens=estimated,
        unalignable_tokens=unalignable,
    )
