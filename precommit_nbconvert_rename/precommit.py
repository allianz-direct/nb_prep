import os
import re
import sys
import argparse
import codecs
from datetime import datetime

from pathlib import Path
from nbconvert import HTMLExporter

def convert_notebook(path: str, date_format="%Y%m%d") -> None:
    html_exporter = HTMLExporter()
    html_exporter.template_name = 'classic'
    
    (body, _) = html_exporter.from_filename(path)

    date_prefix = datetime.strftime(datetime.now(), date_format)
    if len(date_prefix) != 0:
        date_prefix += "_"

    html_path = Path(path)
    html_path = html_path.with_stem(f"{date_prefix}{html_path.stem}_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER")
    html_path = html_path.with_suffix(".html")

    with codecs.open(html_path, "w", "utf-8") as f:
        f.write(body)


def main():
    
    parser = argparse.ArgumentParser(description="Convert Jupyter notebooks to HTML and add date prefix and commit hash placeholder.")
    parser.add_argument("filenames", nargs="+", help="files or directories to format")
    parser.add_argument("--date-prefix-format", type=str,
                        help="Format of the date prefix. Defaults to %Y%m%d, set to empty for no prefix", default="%Y%m%d")
    args = parser.parse_args()

    exclude_re = re.compile(r"/(\.ipynb_checkpoints)/")
    filenames = []
    for fn in args.filenames:
        path = Path(os.path.abspath(fn))
        if path.is_dir():
            filenames += list(
                str(fn)
                for fn in path.glob("**/*.ipynb")
                if not exclude_re.search(str(fn))
            )
        else:
            filenames.append(str(path))

    for path in filenames:
        convert_notebook(path, date_format=args.date_prefix_format)

    return 0


if __name__ == "__main__":
    sys.exit(main())