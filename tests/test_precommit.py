import shutil

from freezegun import freeze_time
from pathlib import Path

from precommit_nbconvert_rename.precommit import convert_notebook
from utils import working_directory

@freeze_time("2012-01-14")
def test_convert_notebook(tmp_path):

    shutil.copyfile(
        "tests/data/example.ipynb",
        str(tmp_path / "example.ipynb"),
    )
    with working_directory(str(tmp_path)):
        convert_notebook(str(tmp_path / "example.ipynb"))
        assert Path("20120114_example_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html").exists()
        
        # No date prefix
        convert_notebook(str(tmp_path / "example.ipynb"), date_format="")
        assert Path("example_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html").exists()
