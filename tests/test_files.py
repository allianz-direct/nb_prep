import os
import shutil

from precommit_nbconvert_rename.files import find_notebooks, is_excluded, working_directory


def test_is_excluded():

    assert is_excluded("c:/data/notebook.ipynb", ["c:/data/notebook.ipynb"])
    assert is_excluded("data/notebook.ipynb", ["*/notebook.ipynb"])
    assert is_excluded("data/notebook.ipynb", ["data/*"])
    assert is_excluded("notebook.ipynb", ["notebook.ipynb"])


def test_find_notebooks(tmp_path):


    shutil.copytree(
        "tests/data/",
        tmp_path / "data"
    )
    with working_directory(str(tmp_path)):

        all_notebooks = [f"data{os.sep}example.ipynb", f"data{os.sep}another_example.ipynb"]
        # all_notebooks = set([os.path.abspath(f) for f in all_notebooks])
        assert set(find_notebooks(".")) == set(all_notebooks)

        assert len(find_notebooks(".", exclude_list=["data/*"])) == 0
