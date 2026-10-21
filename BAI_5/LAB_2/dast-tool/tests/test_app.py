import unittest

from app import app


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_all_get_endpoints(self):
        for endpoint, key in [("monitor", "memory_usage"), ("memory", "overflow_test"),
                              ("network", "network_stats"), ("security", "suspicious_calls")]:
            response = self.client.get("/api/" + endpoint)
            self.assertEqual(response.status_code, 200)
            self.assertIn(key, response.get_json())

    def test_sandbox_echo(self):
        response = self.client.post("/api/sandbox", json={"command": "echo Hello Sandbox"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["stdout"], "Hello Sandbox\n")

    def test_invalid_bodies(self):
        for body in [None, [], {}, {"command": 123}, {"command": []},
                     {"command": "'"}, {"command": ["echo", None]}]:
            response = self.client.post("/api/sandbox", json=body)
            self.assertEqual(response.status_code, 400)

    def test_arbitrary_host_command_denied(self):
        response = self.client.post("/api/sandbox", json={"command": ["python", "-V"]})
        self.assertEqual(response.status_code, 403)
