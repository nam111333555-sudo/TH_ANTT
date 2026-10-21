import json
import os

from audit_demo import collect_demo_events
from memory_analyzer import MemoryAnalyzer
from network_traffic_analyzer import NetworkTrafficAnalyzer
from runtime_monitor import RuntimeMonitor
from security_behavior_checker import SecurityBehaviorChecker
from virtual_sandbox import VirtualSandbox


def main():
    runtime = RuntimeMonitor(os.getpid())
    memory = MemoryAnalyzer()
    events = collect_demo_events()
    with VirtualSandbox() as sandbox:
        stdout, stderr = sandbox.run_isolated("echo Hello Sandbox")
    result = {
        "pid": os.getpid(),
        "cpu_usage": runtime.get_cpu_usage(),
        "memory_usage": runtime.get_memory_usage(),
        "open_files": [f.path for f in runtime.get_open_files()],
        "memory_leaks": [type(o).__name__ for o in memory.check_memory_leaks()],
        "overflow_test": memory.check_overflow(2**64),
        "network_stats": {k: v._asdict() for k, v in
                          NetworkTrafficAnalyzer().get_network_stats().items()},
        "suspicious_calls": SecurityBehaviorChecker().suspicious_calls(),
        "runtime_events": events,
        "flagged_events": SecurityBehaviorChecker().check_events(events),
        "sandbox_stdout": stdout, "sandbox_stderr": stderr,
        "sandbox_backend": "process (temporary cwd, trusted commands only)",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    main()
