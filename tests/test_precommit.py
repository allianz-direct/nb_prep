import shutil
import git
import os
import sys
import pytest

from pathlib import Path
from datetime import date

from nb_prep.files import working_directory


def shell_output(command) -> str:
    """
    Lightweight function to quickly run a shell command.
    For longer queries with json output use 'run_command'
    """
    print(f"Running:\n\t{command}")
    std_out = os.popen(command).read().rstrip()
    std_out = std_out.lstrip('"').rstrip('"')
    return std_out.strip()


@pytest.mark.skipif(sys.platform == "win32", reason="Hard to debug windows when developing on linux")
def test_precommit_hook(tmp_path):
    """
    Tests if the full setup with precommit hooks works properly.

    Equivalent to running:

    ```bash
    mkdir test_prj
    cp nb_prep/tests/data/example.ipynb test_prj/
    cd test_prj
    git init
    git add --all
    pre-commit try-repo ../nb_prep --verbose
    git commit -m "test"
    pre-commit try-repo ../nb_prep --verbose --hook-stage post-commit
    ```
    """

    current_dir = os.getcwd()

    test_prj = tmp_path / "test_prj"
    shutil.copytree("tests/data/", test_prj)
    with working_directory(str(test_prj)):

        # we'll gitignore HTML files
        f = open(".gitignore", "a")
        f.write("*.html")
        f.close()

        # Now setup a git repo
        repo = git.Repo.init(str(test_prj), bare=False)
        author = "Test Person <testtest@gmail.com>"
        repo.git.add(all=True)

        # First pass pre-commit. Will output something like:
        # nb_prep (pre-commit; process notebooks)..................................Failed
        # - hook id: nb_prep_precommit
        out = shell_output(f"pre-commit try-repo '{current_dir}' --verbose")
        assert "nb_prep (pre-commit; process notebooks).." in out
        assert "...Failed" in out

        # Add changes
        repo.git.add(all=True)
        # Second pass should succeed
        out = shell_output(f"pre-commit try-repo '{current_dir}' --verbose")
        assert "nb_prep (pre-commit; process notebooks).." in out
        assert "...Passed" in out

        # Make sure notebook stripping worked
        nb = test_prj / "example.ipynb"
        txt = nb.read_text()
        assert "Hello, World!" not in txt

        # Make sure notebook conversion worked
        assert Path(f"{date.today().strftime('%Y%m%d')}_example_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html").exists()

        # Now for the post-commit hook
        repo.git.add(all=True)
        repo.git.commit(message="add stuff", author=author)

        out = shell_output(f"pre-commit try-repo '{current_dir}' --verbose --hook-stage post-commit")
        assert "nb_prep (post-commit; replace hash placeholder in .html filenames)...." in out
        assert "...Passed" in out
