import os
import fnmatch
from pathlib import Path
from typing import List, Optional
from contextlib import contextmanager


def find_files_in_paths(
    directories: List[Path],
    extension: str = ".ipynb",
    exclude_list: Optional[List[str]] = None,
) -> List[Path]:
    """
    Find all files with a certain extension in a list of paths.

    Args:
        directories: List of paths to dirs and files.
        extension: Extension of target files.
        exclude_list: List of globs to exclude.
    """
    assert extension.startswith(".")

    filenames = []  # type: List[Path]

    for fn in directories:

        if not isinstance(fn, Path):
            fn = Path(fn)

        if not fn.is_dir():
            if fn.suffix == extension and not is_excluded(fn, exclude_list):
                filenames.append(fn)
                continue

        files = [f for f in fn.glob(f"**/*{extension}")]
        if extension == ".ipynb":
            files = [f for f in files if not f.suffix == ".ipynb_checkpoints"]

        if exclude_list is not None:
            files = [f for f in files if not is_excluded(f, exclude_list)]

        filenames += files

    return filenames


def is_excluded(src_path: Path, globs: Optional[List[str]] = None) -> bool:
    """
    Determine if a src_path should be excluded.

    Supports globs (e.g. folder/* or *.md).
    Credits: code inspired by / adapted from
    https://github.com/apenwarr/mkdocs-exclude/blob/master/mkdocs_exclude/plugin.py

    Args:
        src_path (Path): Path of file
        globs (list): list of globs

    Returns:
        (bool): whether src_path should be excluded
    """
    if globs is None or len(globs) == 0:
        return False

    assert isinstance(src_path, Path)
    assert isinstance(globs, list)

    for g in globs:
        if fnmatch.fnmatchcase(str(src_path), g):
            return True

        # Windows reports filenames as eg.  a\\b\\c instead of a/b/c.
        # To make the same globs/regexes match filenames on Windows and
        # other OSes, let's try matching against converted filenames.
        # On the other hand, Unix actually allows filenames to contain
        # literal \\ characters (although it is rare), so we won't
        # always convert them.  We only convert if os.sep reports
        # something unusual.  Conversely, some future mkdocs might
        # report Windows filenames using / separators regardless of
        # os.sep, so we *always* test with / above.
        if os.sep != "/":
            src_path_fix = str(src_path).replace(os.sep, "/")
            if fnmatch.fnmatchcase(src_path_fix, g):
                return True

    return False


@contextmanager
def working_directory(path):
    """
    Temporarily change working directory.

    A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.
    Usage:
    ```python
    # Do something in original directory
    with working_directory('/my/new/path'):
        # Do something in new directory
    # Back to old directory
    ```
    """
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def insert_commithash_filename_placeholder(path: Path, commithash: str) -> None:
    """
    Replaces NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER with last commit.

    Args:
        path (str): path to notebook
        commithash (str): short hash of commit to insert
    """
    assert len(commithash) != 0

    p = Path(path)
    stem = Path(path).stem
    if "NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER" not in stem:
        return

    stem = stem.replace("NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER", commithash)
    p.rename(Path(p.parent, f"{stem}{p.suffix}"))
