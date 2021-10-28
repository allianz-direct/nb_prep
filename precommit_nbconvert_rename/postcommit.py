"""
Should run on post-commit hook

git rev-parse --short HEAD
"""

import os
import subprocess
from pathlib import Path
import argparse


def git_version():
    """
    Return the git revision as a string.

    Credits: this function was copied from numpy.
    https://stackoverflow.com/a/40170206.
    """

    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ["SYSTEMROOT", "PATH"]:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env["LANGUAGE"] = "C"
        env["LANG"] = "C"
        env["LC_ALL"] = "C"
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(["git", "rev-parse", "--short", "HEAD"])
        GIT_REVISION = out.strip().decode("ascii")
    except OSError:
        GIT_REVISION = "Unknown"

    return GIT_REVISION


def convert_filename(path: str, commithash: str) -> None:
    """
    Renames files.

    Replaces NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER with last commit.
    """
    p = Path(path)
    stem = Path(path).stem
    if not "NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER" in stem:
        return

    stem = stem.replace("NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER", commithash)
    p.rename(Path(p.parent, f"{stem}{p.suffix}"))


def main():

    parser = argparse.ArgumentParser(
        description="Replace all NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER occurances in .html filenames with latest hash."
    )
    # parser.add_argument("filenames", nargs="+", help="files or directories to format")
    args = parser.parse_args()

    filenames = []
    path = Path(os.getcwd())
    filenames += list(str(fn) for fn in path.glob("**/*.html"))

    for path in filenames:
        convert_filename(path, commithash=git_version())

    return 0


if __name__ == "__main__":
    sys.exit(main())
