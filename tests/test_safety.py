import unittest

from lightweight_llm_pi.safety import match_safety_hint


class SafetyTest(unittest.TestCase):
    def test_emergency_hint(self) -> None:
        hint = match_safety_hint("家里闻到煤气味怎么办")
        self.assertIsNotNone(hint)
        assert hint is not None
        self.assertEqual(hint.level, "紧急安全提示")

    def test_boundary_hint(self) -> None:
        hint = match_safety_hint("这个药怎么吃")
        self.assertIsNotNone(hint)
        assert hint is not None
        self.assertEqual(hint.level, "安全边界")


if __name__ == "__main__":
    unittest.main()
