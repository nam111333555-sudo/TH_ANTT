import unittest

from network_traffic_analyzer import NetworkTrafficAnalyzer


class TestNetworkTrafficAnalyzer(unittest.TestCase):
    def test_host_counters(self):
        stats = NetworkTrafficAnalyzer().get_network_stats()
        self.assertIsInstance(stats, dict)
        for counter in stats.values():
            self.assertGreaterEqual(counter.bytes_sent, 0)
            self.assertGreaterEqual(counter.bytes_recv, 0)
