import sys
import argparse
import codecs
from datetime import datetime

from pathlib import Path
from nbconvert import HTMLExporter
from precommit_nbconvert_rename.files import find_notebooks


def convert_notebook(
    path: str,
    date_format: str = "%Y%m%d",
    template: str = "",
    no_input: bool = False,
    output_dir: str = ".",
) -> None:
    """
    Converts .ipynb to .html.

    Args:
        path (str): path to notebook
        date_format (str): format to write date prefix in
        template (str): Name of the nbconvert template
        no_input (bool): Remove code input blocks
        output_dir (str): Path to output directory (rel or abs)
    """
    if not Path(output_dir).exists():
        raise IsADirectoryError(
            f"The --output-dir specified ('{output_dir}') does not exist"
        )

    if template:
        html_exporter = HTMLExporter(template_name=template)
    else:
        html_exporter = HTMLExporter()

    if no_input:
        html_exporter.exclude_output_prompt = True
        html_exporter.exclude_input = True
        html_exporter.exclude_input_prompt = True

    (body, _) = html_exporter.from_filename(path)

    date_prefix = datetime.strftime(datetime.now(), date_format)
    if len(date_prefix) != 0:
        date_prefix += "_"

    html_path = Path(path)

    html_path = html_path.with_name(
        f"{date_prefix}{html_path.stem}_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER"
    )
    html_path = html_path.with_suffix(".html")

    output_path = Path(output_dir)
    if output_path.is_absolute():
        # absolute output directory
        output_file = output_path / html_path.name
    else:
        # relative output directory
        output_file = html_path.parent / output_path / html_path.name
        output_file = output_file.resolve()

    # why not overwrite files?
    # Intended usecase is nbconvert > nbstripout > add commit hash on post-commit
    # nbstripout will edit your notebook and fail on pre-commit
    # then you need to re-add your (stripped) .ipynb and commit again
    # that would mean nbconvert runs again on your stripped file
    # using html_path_.exists() prevents this.
    # If a user would continue editing the .ipynb after the failed precommit nbstripout
    # Then the nbconvert .html would be outdated of course.
    if not html_path.exists():
        with codecs.open(str(html_path), "w", "utf-8") as f:
            f.write(body)


def parse_args(args):
    """
    Parse arguments passed to 'nbconvert_rename'.
    """
    parser = argparse.ArgumentParser(
        description="Convert Jupyter notebooks to HTML and add date prefix and commit hash placeholder."
    )
    parser.add_argument(
        "filenames",
        nargs="+",
        help="List of directories and/or files to find and convert notebooks",
    )
    parser.add_argument(
        "--date-prefix-format",
        type=str,
        help="Format of the date prefix. Defaults to %%Y%%m%%d, set to empty for no prefix",
        default="%Y%m%d",
    )
    parser.add_argument(
        "--template",
        type=str,
        help="Name of the nbconvert template to use.",
        default="",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Path of output directory",
        default=".",
    )
    parser.add_argument(
        "--no-input",
        action="store_true",
        help="When specified code blocks are not include.",
    )
    parser.add_argument(
        "--exclude",
        nargs="+",
        help="List of directories to exclude from processing.",
        required=False,
    )

    return parser.parse_args()


def main():
    """
    The 'nbconvert_rename' command.

    Precommit hook.
    """
    args = parse_args(sys.argv[1:])

    notebook_paths = find_notebooks(args.filenames)

    for path in notebook_paths:
        convert_notebook(
            path,
            date_format=args.date_prefix_format,
            template=args.template,
            no_input=args.no_input,
            output_dir=args.output_dir,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
