import subprocess
import sys
import unittest
from pathlib import Path


class CourseDownloadTest(unittest.TestCase):
    def test_download_matches_published_lessons(self):
        script = Path(__file__).resolve().parents[1] / "scripts/course_bundle.py"
        subprocess.run([sys.executable, script, "--check"], check=True)
