import typer
import os
from pathlib import Path
from typing import List, Optional

from precommit_nbconvert_rename.files import find_files_in_paths, insert_commithash_filename_placeholder
from precommit_nbconvert_rename._utils import git_version
from precommit_nbconvert_rename.nb_convert_strip import convert_notebook


app = typer.Typer()


@app.command()
def rename(
    paths: Optional[List[Path]] = typer.Argument(None, help="Directories and/or files to find and convert notebooks")
    ):
    """
    Replaces the placeholder NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER with the current commit hash.

    For example:

    "20211026_notebook_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html" 
    "20211026_notebook_26b2841.html"
    """
    if len(paths) == 0:
        paths = [Path(os.getcwd())]
    
    filenames = find_files_in_paths(paths, extension=".html")

    for path in filenames:
        insert_commithash_filename_placeholder(path, commithash=git_version())




@app.command()
def process(
    paths: Optional[List[Path]] = typer.Argument(None, help="Directories and/or files to find and convert notebooks"),
    date_prefix: Optional[str] = typer.Option("%Y%m%d", help="Format of the date prefix. Set to empty for no prefix."),
    output_dir: Optional[Path] = typer.Option(".", help="Path where to place output HTML files."),
    exclude: Optional[List[Path]] = typer.Option(None, help="Directories and/or files to exclude from processing"),
    nbconvert_template: Optional[str] = typer.Option(None, help="Name of the nbconvert template to use."),
    nbconvert_no_input: bool = typer.Option(True, help="Nbconvert: Exclude input cells and output prompts from converted document. Ideal for generating code-free reports."),
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
            template=nbconvert_template,
            no_input=nbconvert_no_input,
            output_dir=output_dir,
        )
