import shutil
import git
from typer.testing import CliRunner
from freezegun import freeze_time

from precommit_nbconvert_rename.cli import app
from precommit_nbconvert_rename.files import working_directory

runner = CliRunner()

def test_app_command_rename(tmp_path):

    shutil.copytree(
        "tests/data/",
        tmp_path / "data"
    )
    with working_directory(str(tmp_path)):

        # there is no git repo in the tmp_dir
        result = runner.invoke(app, ["rename"])
        assert result.exit_code == 1
        assert "fatal: not a git repository"  in str(result.exception)


        # Now setup a git repo
        repo = git.Repo.init(str(tmp_path), bare=False)
        author = "Test Person <testtest@gmail.com>"
        repo.git.add("data/*")
        repo.git.commit(message="add stuff", author=author)

        result = runner.invoke(app, ["rename"])
        assert result.exit_code == 0
        assert not "fatal: not a git repository" in str(result.exception)

        newfile = tmp_path / "data" / "20211028_example_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html"
        assert not newfile.exists()

@freeze_time("2000-11-22")
def test_app_command_process(tmp_path):

    shutil.copytree(
        "tests/data/",
        tmp_path / "data"
    )
    with working_directory(str(tmp_path)):
        result = runner.invoke(app, ["process"])
        assert result.exit_code == 0
        newfile = tmp_path / "data" / "20001122_example_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html"
        assert newfile.exists()
