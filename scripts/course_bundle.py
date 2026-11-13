"""Build the student download from the published course, or check its contents."""
import argparse
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

COURSE = Path(__file__).resolve().parents[1] / "docs/course"
ARCHIVE = COURSE / "offline-course.zip"


def contents():
    for file in sorted(COURSE.rglob("*")):
        if file.is_file() and file != ARCHIVE and not file.name.startswith("."):
            data = file.read_bytes()
            if file == COURSE / "index.html":
                # The offline copy is already unzipped.
                data = re.sub(rb"<!--bundle-link-->.*?<!--/bundle-link-->", b"", data, flags=re.S)
            yield "course/" + file.relative_to(COURSE).as_posix(), data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = dict(contents())
    if args.check:
        with ZipFile(ARCHIVE) as archive:
            if sorted(archive.namelist()) != sorted(expected):
                raise SystemExit("Course ZIP inventory differs. Run python scripts/course_bundle.py.")
            for name, data in expected.items():
                if archive.read(name) != data:
                    raise SystemExit("Stale ZIP entry: " + name)
    else:
        with ZipFile(ARCHIVE, "w", ZIP_DEFLATED) as archive:
            for name, data in expected.items():
                archive.writestr(name, data)


if __name__ == "__main__":
    main()
