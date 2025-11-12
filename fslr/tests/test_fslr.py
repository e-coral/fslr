import unittest
import os
from pathlib import Path
import subprocess

class TestConstruct(unittest.TestCase):
    """ Test construction"""
    def test_api(self):

        self.ref = Path("fslr/tests/data/small_ref.fa")
        self.reads = Path("fslr/tests/data")
        outdir_env = os.getenv("FSLR_OUTDIR", "fslr/tests/output")
        self.outdir = Path(outdir_env)
        self.outdir.mkdir(parents=True, exist_ok=True)

        cmd = [
            "fslr",
            "--name", str('fusions'),
            "--ref", str(self.ref),
            "--basecalled", str(self.reads),
            "--out", str(self.outdir),
            "--primers", str('21q1'),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        self.assertEqual(result.returncode, 0, f"FSLR failed:\n{result.stderr}")
        self.assertTrue(
            any(f.suffix in [".bam", ".bed"] for f in self.outdir.iterdir()),
            "No expected output files generated"
        )

        return 0


def main():
    unittest.main()


if __name__ == "__main__":
    unittest.main()