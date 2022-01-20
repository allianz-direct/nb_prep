import typer
import os
from pathlib import Path
from typing import List, Optional

from nb_prep.files import (
    find_files_in_paths,
    insert_commithash_filename_placeholder,
)
from nb_prep._utils import git_version
from nb_prep.nb_convert_strip import convert_notebook


app = typer.Typer()


@app.command()
def rename(
    paths: List[Path] = typer.Argument(None, help="Directories and/or files to find and convert notebooks"),
    output_dir: Optional[Path] = typer.Option(None, help="Additional path where to find and rename HTML files."),
):
    """
    Replaces the placeholder NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER with the current commit hash.

    For example:

    "20211026_notebook_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html"
    "20211026_notebook_26b2841.html"
    """
    if len(paths) == 0:
        paths = [Path(os.getcwd())]

    if output_dir is not None:

        if not isinstance(output_dir, Path):
            output_dir = Path(output_dir)

        output_dir = output_dir.expanduser()

        if not Path(output_dir).exists():
            raise NotADirectoryError(f"The --output-dir specified ('{output_dir}') does not exist")

        paths += [output_dir]

    filenames = find_files_in_paths(paths, extension=".html")

    for path in filenames:
        insert_commithash_filename_placeholder(path, commithash=git_version())


@app.command()
def process(
    paths: List[Path] = typer.Argument(None, help="Directories and/or files to find and convert notebooks"),
    date_prefix: str = typer.Option("%Y%m%d", help="Format of the date prefix. Set to empty for no prefix."),
    git_hash_suffix: bool = typer.Option(
        True, help="Whether to include a placeholder in HTML filename for a git commit hash."
    ),
    output_dir: Path = typer.Option(Path("."), help="Path where to place output HTML files."),
    exclude: Optional[List[str]] = typer.Option(None, help="Globs of directories/files to exclude from processing"),
    nbconvert_template: str = typer.Option("", help="Name of the nbconvert template to use."),
    nbconvert_no_input: bool = typer.Option(
        True,
        help="Nbconvert: Exclude input cells and output prompts from converted document.",
    ),
):
    """
    Process .ipynb files.

    Applies the following steps:\n
    - Convert Jupyter notebooks to HTML\n
    - Applies nbstripout to the notebook\n
    - Optionally add date prefix to .HTML file
    - Add commit hash placeholder.
    """
    if len(paths) == 0:
        paths = [Path(os.getcwd())]

    notebook_paths = find_files_in_paths(paths, extension=".ipynb", exclude_list=exclude)

    for path in notebook_paths:
        convert_notebook(
            path,
            date_format=date_prefix,
            git_hash_suffix=git_hash_suffix,
            template=nbconvert_template,
            no_input=nbconvert_no_input,
            output_dir=output_dir,
        )
