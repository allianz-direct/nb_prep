import shutil
from pathlib import Path

from nb_prep.files import working_directory, insert_commithash_filename_placeholder


def test_insert_commithash_filename_placeholder(tmp_path):
    shutil.copyfile(
        "tests/data/20211028_example_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html",
        str(tmp_path / "20211028_example_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html"),
    )
    with working_directory(str(tmp_path)):
        insert_commithash_filename_placeholder(
            str(tmp_path / "20211028_example_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html"),
            commithash="helloworld",
        )
        assert Path(str(tmp_path / "20211028_example_helloworld.html")).exists()
