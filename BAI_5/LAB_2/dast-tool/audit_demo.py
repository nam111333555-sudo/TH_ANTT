"""Observe a trusted demonstration in a fresh interpreter, without global hooks."""
import json
from pathlib import Path
import subprocess
import sys


def collect_demo_events():
    result = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--worker"],
                            capture_output=True, text=True, timeout=5, check=True)
    return json.loads(result.stdout)


if __name__ == "__main__":
    if sys.argv[1:] == ["--worker"]:
        events = []

        def observe(event, args):
            if event in {"compile", "exec", "os.system", "subprocess.Popen", "socket.connect"}:
                events.append({"event": event})

        sys.addaudithook(observe)
        # Harmless, fixed code; an exec audit event is a signal, not proof of malware.
        compiled = compile("result = 2 + 2", "<lab05-demo>", "exec")
        exec(compiled, {})
        print(json.dumps(events))
    else:
        print(json.dumps(collect_demo_events(), indent=2))
