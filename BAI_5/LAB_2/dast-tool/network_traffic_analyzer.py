import psutil


class NetworkTrafficAnalyzer:
    def get_network_stats(self):
        """Host-wide counters per interface, not per-process packet inspection."""
        return psutil.net_io_counters(pernic=True)
