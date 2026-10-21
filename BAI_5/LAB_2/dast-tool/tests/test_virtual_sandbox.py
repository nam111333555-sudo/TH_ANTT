from pathlib import Path
import subprocess
import sys
import unittest

from virtual_sandbox import VirtualSandbox


class TestVirtualSandbox(unittest.TestCase):
    def test_echo(self):
        with VirtualSandbox() as sandbox:
            out, err = sandbox.run_isolated("echo test")
            self.assertEqual(out, "test\n")
            self.assertEqual(err, "")

    def test_cwd_output_and_cleanup(self):
        with VirtualSandbox() as sandbox:
            folder = Path(sandbox.temp_dir)
            out, err = sandbox.run_isolated([
                sys.executable, "-c",
                "from pathlib import Path; Path('proof.txt').write_text('ok'); print('ok')"])
            self.assertEqual(out.strip(), "ok")
            self.assertEqual(err, "")
            self.assertEqual((folder / "proof.txt").read_text(), "ok")
        self.assertFalse(folder.exists())

    def test_timeout(self):
        with VirtualSandbox(timeout=0.2) as sandbox:
            with self.assertRaises(subprocess.TimeoutExpired):
                sandbox.run_isolated([sys.executable, "-c", "import time; time.sleep(3)"])

    def test_exit_code(self):
        with VirtualSandbox() as sandbox:
            sandbox.run_isolated([sys.executable, "-c", "raise SystemExit(3)"])
            self.assertEqual(sandbox.returncode, 3)
