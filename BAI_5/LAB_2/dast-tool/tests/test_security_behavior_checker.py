import unittest

from audit_demo import collect_demo_events
from security_behavior_checker import SecurityBehaviorChecker


class TestSecurityBehaviorChecker(unittest.TestCase):
    def test_actual_runtime_audit(self):
        events = collect_demo_events()
        self.assertIn("exec", [e["event"] for e in events])
        self.assertTrue(SecurityBehaviorChecker().check_events(events))

    def test_call_detection_ignores_strings(self):
        checker = SecurityBehaviorChecker()
        self.assertEqual(checker.suspicious_calls("# eval('x')\ns = 'exec'"), [])
        self.assertEqual(checker.suspicious_calls("eval('2')\nos.system('echo test')"),
                         ["eval", "os.system"])

    def test_real_event_classification(self):
        events = [{"event": "open"}, {"event": "socket.connect", "port": 443}]
        self.assertEqual(SecurityBehaviorChecker().check_events(events),
                         [{"event": "socket.connect", "port": 443, "suspicious": True}])

    def test_no_fake_self_scan(self):
        self.assertEqual(SecurityBehaviorChecker().suspicious_calls(), [])
