import os
import shlex

from flask import Flask, jsonify, request
import psutil

from audit_demo import collect_demo_events
from memory_analyzer import MemoryAnalyzer
from network_traffic_analyzer import NetworkTrafficAnalyzer
from runtime_monitor import RuntimeMonitor
from security_behavior_checker import SecurityBehaviorChecker
from virtual_sandbox import VirtualSandbox

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16384


@app.get("/api/monitor")
def monitor():
    runtime = RuntimeMonitor(os.getpid())
    try:
        return jsonify(cpu_usage=runtime.get_cpu_usage(),
                       memory_usage=runtime.get_memory_usage(),
                       open_files=[f.path for f in runtime.get_open_files()])
    except (psutil.Error, OSError) as exc:
        return jsonify(error=str(exc)), 503


@app.get("/api/memory")
def memory():
    analyzer = MemoryAnalyzer()
    return jsonify(memory_leaks=[type(o).__name__ for o in analyzer.check_memory_leaks()],
                   overflow_test=analyzer.check_overflow(2**64),
                   scope="GC uncollectable objects and signed 64-bit range check")


@app.get("/api/network")
def network():
    return jsonify(network_stats={k: v._asdict() for k, v in
                                  NetworkTrafficAnalyzer().get_network_stats().items()})


@app.get("/api/security")
def security():
    events = collect_demo_events()
    return jsonify(suspicious_calls=SecurityBehaviorChecker().suspicious_calls(),
                   runtime_events=events,
                   flagged_events=SecurityBehaviorChecker().check_events(events),
                   scope="Fixed trusted demo in a child interpreter; flags require review")


@app.post("/api/sandbox")
def sandbox():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Expected a JSON object with command"), 400
    command = data.get("command")
    try:
        args = shlex.split(command) if isinstance(command, str) else command
    except ValueError:
        return jsonify(error="Invalid command quoting"), 400
    if (not isinstance(args, list) or not args
            or not all(isinstance(a, str) and a and "\0" not in a for a in args)):
        return jsonify(error="command must be a string or an array of strings"), 400
    # The HTTP lab only needs echo; avoid exposing arbitrary host execution.
    if args[0] != "echo":
        return jsonify(error="This demo API allows only the echo command"), 403
    with VirtualSandbox() as runner:
        stdout, stderr = runner.run_isolated(args)
        return jsonify(stdout=stdout, stderr=stderr, returncode=runner.returncode,
                       backend="process demo; temporary cwd only")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
