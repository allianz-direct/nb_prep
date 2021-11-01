import shutil

from pathlib import Path
from precommit_nbconvert_rename.postcommit import convert_filename
from utils import working_directory


def test_convert_filename(tmp_path):
    shutil.copyfile(
        "tests/data/20211028_example_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html",
        str(tmp_path / "20211028_example_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html"),
    )
    with working_directory(str(tmp_path)):
        convert_filename(
            str(tmp_path / "20211028_example_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html"),
            commithash="helloworld",
        )
        assert Path(str(tmp_path / "20211028_example_helloworld.html")).exists()
