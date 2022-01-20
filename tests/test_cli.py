import shutil
import git
from typer.testing import CliRunner
from freezegun import freeze_time

from nb_prep.cli import app
from nb_prep.files import working_directory

runner = CliRunner()


def test_app_command_rename(tmp_path):

    shutil.copytree("tests/data/", tmp_path / "data")
    with working_directory(str(tmp_path)):

        # there is no git repo in the tmp_dir
        result = runner.invoke(app, ["rename"])
        assert result.exit_code == 1
        assert "fatal: not a git repository" in str(result.exception)

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

    shutil.copytree("tests/data/", tmp_path / "data")
    with working_directory(str(tmp_path)):
        result = runner.invoke(app, ["process"])
        assert result.exit_code == 0
        newfile = tmp_path / "data" / "20001122_example_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html"
        assert newfile.exists()


@freeze_time("2000-11-22")
def test_app_command_process_with_exclude(tmp_path):

    shutil.copytree("tests/data/", tmp_path / "data")
    with working_directory(str(tmp_path)):
        result = runner.invoke(app, ["process", "--exclude", "example.ipynb"])
        assert result.exit_code == 0

        example = tmp_path / "data" / "20001122_example_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html"
        assert not example.exists()
        another_example = tmp_path / "data" / "20001122_another_example_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html"
        assert another_example.exists()


@freeze_time("2000-11-22")
def test_app_command_process_with_no_hash_suffix(tmp_path):

    shutil.copytree("tests/data/", tmp_path / "data")
    with working_directory(str(tmp_path)):
        result = runner.invoke(app, ["process", "--no-git-hash-suffix"])
        assert result.exit_code == 0

        example = tmp_path / "data" / "20001122_example.html"
        assert example.exists()
        another_example = tmp_path / "data" / "20001122_another_example.html"
        assert another_example.exists()


@freeze_time("2000-11-22")
def test_app_command_process_with_different_date_prefix(tmp_path):

    shutil.copytree("tests/data/", tmp_path / "data")
    with working_directory(str(tmp_path)):
        result = runner.invoke(app, ["process", "--date-prefix", "%Y"])
        assert result.exit_code == 0

        example = tmp_path / "data" / "2000_example_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html"
        assert example.exists()
        another_example = tmp_path / "data" / "2000_another_example_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html"
        assert another_example.exists()
