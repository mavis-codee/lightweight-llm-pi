import unittest

from lightweight_llm_pi.calculator import CalculationError, calculate, try_calculate


class CalculatorTest(unittest.TestCase):
    def test_basic_arithmetic(self) -> None:
        self.assertEqual(calculate("128 * 36 + 7"), 4615)

    def test_command_prefix(self) -> None:
        result = try_calculate("/calc sqrt(81) + 1")
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.value, 10)

    def test_blocks_unsafe_expression(self) -> None:
        with self.assertRaises(CalculationError):
            calculate("__import__('os').system('whoami')")


if __name__ == "__main__":
    unittest.main()
