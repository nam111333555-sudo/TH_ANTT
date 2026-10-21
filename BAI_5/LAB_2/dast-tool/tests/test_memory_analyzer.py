import unittest

from memory_analyzer import MemoryAnalyzer


class TestMemoryAnalyzer(unittest.TestCase):
    def test_signed_64_bit_boundaries(self):
        analyzer = MemoryAnalyzer()
        for value in [-(2**63), 2**63 - 1, 100, True, "large"]:
            self.assertFalse(analyzer.check_overflow(value))
        for value in [-(2**63) - 1, 2**63, 2**64]:
            self.assertTrue(analyzer.check_overflow(value))

    def test_gc_result(self):
        self.assertIsInstance(MemoryAnalyzer().check_memory_leaks(), list)
