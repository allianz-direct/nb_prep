import os
import shutil
from pathlib import Path

from nb_prep.files import find_files_in_paths, is_excluded, working_directory


def test_is_excluded():

    assert is_excluded(Path("c:/data/notebook.ipynb"), ["c:/data/notebook.ipynb"])
    assert is_excluded(Path("data/notebook.ipynb"), ["*/notebook.ipynb"])
    assert is_excluded(Path("data/notebook.ipynb"), ["data/*"])
    assert is_excluded(Path("notebook.ipynb"), ["notebook.ipynb"])


def test_find_files_in_paths(tmp_path):

    shutil.copytree("tests/data/", tmp_path / "data")
    with working_directory(str(tmp_path)):

        all_notebooks = [f"data{os.sep}example.ipynb", f"data{os.sep}another_example.ipynb"]
        # all_notebooks = set([os.path.abspath(f) for f in all_notebooks])

        assert set([str(f) for f in find_files_in_paths(".")]) == set(all_notebooks)
        assert len(find_files_in_paths(".", exclude_list=["data/*"])) == 0

        html_files = [f"data{os.sep}20211028_example_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html"]
        assert set([str(f) for f in find_files_in_paths(".", extension=".html")]) == set(html_files)
