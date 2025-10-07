import math
import unittest

from fibonacci import FibonacciSummary, generate_fibonacci, summarize


class GenerateFibonacciTests(unittest.TestCase):
    def test_zero_terms_returns_empty_list(self) -> None:
        self.assertEqual(generate_fibonacci(0), [])

    def test_single_term_returns_zero(self) -> None:
        self.assertEqual(generate_fibonacci(1), [0])

    def test_multiple_terms_match_expected_sequence(self) -> None:
        expected = [0, 1, 1, 2, 3, 5, 8, 13]
        self.assertEqual(generate_fibonacci(len(expected)), expected)

    def test_negative_input_is_treated_as_zero(self) -> None:
        self.assertEqual(generate_fibonacci(-10), [])


class SummarizeTests(unittest.TestCase):
    def test_summary_of_empty_sequence(self) -> None:
        summary = summarize([])
        self.assertIsInstance(summary, FibonacciSummary)
        self.assertEqual(summary.count, 0)
        self.assertIsNone(summary.last_value)
        self.assertEqual(summary.total_sum, 0)
        self.assertIsNone(summary.golden_ratio)

    def test_summary_of_sequence(self) -> None:
        sequence = [0, 1, 1, 2, 3, 5, 8, 13]
        summary = summarize(sequence)
        self.assertEqual(summary.count, len(sequence))
        self.assertEqual(summary.last_value, 13)
        self.assertEqual(summary.total_sum, sum(sequence))
        self.assertTrue(math.isclose(summary.golden_ratio or 0, 13 / 8, rel_tol=1e-9))


if __name__ == "__main__":
    unittest.main()
