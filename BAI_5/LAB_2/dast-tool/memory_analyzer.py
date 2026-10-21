import gc


class MemoryAnalyzer:
    def check_memory_leaks(self):
        """Uncollectable GC objects are evidence, not all possible memory leaks."""
        gc.collect()
        return list(gc.garbage)

    def check_overflow(self, value):
        """Check the signed 64-bit domain; Python ints themselves do not overflow."""
        return (isinstance(value, int) and not isinstance(value, bool)
                and not -(2**63) <= value <= 2**63 - 1)
