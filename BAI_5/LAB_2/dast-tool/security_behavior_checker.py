"""Source heuristics and actual runtime audit-event classification."""
import ast


class SecurityBehaviorChecker:
    def suspicious_calls(self, code=None):
        # No self-file scan: finding names inside this checker is meaningless.
        if code is None:
            return []
        found = set()
        for node in ast.walk(ast.parse(code)):
            if isinstance(node, ast.Call):
                name = ast.unparse(node.func)
                if name in {"os.system", "eval", "exec"}:
                    found.add(name)
        return sorted(found)

    def check_events(self, events):
        suspicious = {"os.system", "subprocess.Popen", "socket.connect", "exec"}
        return [dict(event, suspicious=True) for event in events
                if event.get("event") in suspicious]
