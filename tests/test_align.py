import unittest

from caption_timeline_align import AsrWord, align
from caption_timeline_align.align import visible_text


class TestAlign(unittest.TestCase):
    def test_script_is_source_of_truth(self):
        script = "今天天气很好"
        asr = [
            AsrWord("今天", 0.0, 0.4),
            AsrWord("气候", 0.4, 0.8),
            AsrWord("很好", 0.8, 1.2),
        ]
        result = align(script, asr, duration=1.5, max_chars=16)
        joined = "".join(visible_text(cue.text) for cue in result.cues)
        self.assertEqual(joined, visible_text(script))
        self.assertNotIn("气候", "".join(cue.text for cue in result.cues))

    def test_repeated_words_stay_monotonic(self):
        script = "哈哈哈"
        asr = [
            AsrWord("哈", 0.0, 0.2),
            AsrWord("哈", 0.2, 0.4),
            AsrWord("哈", 0.4, 0.6),
        ]
        result = align(script, asr, duration=0.8, max_chars=16)
        starts = [cue.start for cue in result.cues]
        self.assertEqual(starts, sorted(starts))
        self.assertEqual(result.matched_tokens, 3)

    def test_unmatched_prefix_keeps_script_order(self):
        script = "序言正文结束"
        asr = [
            AsrWord("正文", 1.0, 1.5),
            AsrWord("结束", 1.5, 2.0),
        ]
        result = align(script, asr, duration=2.2, max_chars=16)
        joined = "".join(visible_text(cue.text) for cue in result.cues)
        self.assertEqual(joined, visible_text(script))
        self.assertLessEqual(result.cues[0].start, result.cues[-1].start)

    def test_anchor_times_map_from_asr(self):
        script = "你好世界"
        asr = [
            AsrWord("你好", 0.5, 1.0),
            AsrWord("世界", 1.2, 1.8),
        ]
        result = align(script, asr, duration=2.0, max_chars=16)
        self.assertEqual(result.matched_tokens, 2)
        self.assertTrue(
            abs(result.cues[0].start - 0.5) < 1e-6
            or any(abs(cue.start - 0.5) < 1e-6 for cue in result.cues)
        )

    def test_punctuation_is_ignored_in_matching(self):
        script = "你好，世界！"
        asr = [AsrWord("你好", 0.0, 0.4), AsrWord("世界", 0.5, 0.9)]
        result = align(script, asr, duration=1.2, max_chars=16)
        self.assertEqual(visible_text("".join(cue.text for cue in result.cues)), "你好世界")
        self.assertEqual(result.matched_tokens, 2)


if __name__ == "__main__":
    unittest.main()
