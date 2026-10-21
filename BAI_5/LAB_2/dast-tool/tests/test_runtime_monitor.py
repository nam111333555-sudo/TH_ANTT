import os
import unittest

from runtime_monitor import RuntimeMonitor


class TestRuntimeMonitor(unittest.TestCase):
    def test_current_process(self):
        monitor = RuntimeMonitor(os.getpid())
        self.assertIsInstance(monitor.get_cpu_usage(), float)
        self.assertGreater(monitor.get_memory_usage(), 0)
        self.assertIsInstance(monitor.get_open_files(), list)
