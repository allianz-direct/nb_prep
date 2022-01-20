[![Unit tests](https://github.com/allianz-direct/nb_prep/actions/workflows/unit_tests.yml/badge.svg)](https://github.com/allianz-direct/nb_prep/actions/workflows/unit_tests.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nb-prep)
![PyPI](https://img.shields.io/pypi/v/nb-prep)
![PyPI - Downloads](https://img.shields.io/pypi/dm/nb-prep)
![GitHub contributors](https://img.shields.io/github/contributors/timvink/nb-prep)
![PyPI - License](https://img.shields.io/pypi/l/nb-prep)

# nb_prep

`nb_prep` makes it easier to prepare jupyter notebooks for storing in git and sharing with stakeholders. 

You can use the `nb_prep` CLI to:

- Convert jupyter notebooks to HTML (using [`nbconvert`](https://nbconvert.readthedocs.io/)) and:
    - add a date prefix to the filename.
    - add a git hash suffix to the filename.
    - move the HTML file to a configured output directory
- Strip all cell outputs (using [`nbstripout`](https://github.com/kynan/nbstripout))

You can also configure `nb_prep` once as a pre-commit hook and have notebook output automatically prepared every time you `git commit`.

## Installation

```bash
pip install nb_prep
```

## Use case

You use [jupyter notebooks](https://jupyter.org/) and:

- [nbconvert](https://github.com/jupyter/nbconvert) to convert `.ipynb` files to `.html` files
- [nbstripout](https://github.com/kynan/nbstripout) to avoid committing (potentially sensitive) data to git and get proper `git diff`s on notebooks (only showing changes in code).

Forget to run `nbconvert` or use them in the wrong order (`nbstripout` before `nbconvert`) and you will have to re-run your notebooks before you can output HTML, which can be annoying when they are long-running. Especially when you use `nbstripout` as a [pre-commit](https://pre-commit.com/) hook, this can happen quite often.

`nb_prep` can help to automatically process notebooks and (optionally) store versioned output in an in output directory. 


## Usage

The CLI command `nb_prep process` takes a list of directories and/or files to find and process notebooks. For each notebook:

- `nbconvert` is used to create an `<filename>.html` export
- A date prefix is added `YYYYMMDD_<filename>.html` (can be turned off)
- A placeholder for git hash is added `YYYYMMDD_<filename>_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html`
- The `.html` file is moved to an `output-dir` (if specified)
- The `nbstripout` is used strip output from the `.ipynb` file

Now you can `git add` and `git commit` the changed notebook files. You can then use `nb_prep rename` to insert the commit hashes in the notebook filenames. For example:

`20220101_my_notebook_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html` -> `20220101_my_notebook_eac9e43.html`

Tip: You'll probably want to `.gitignore` the `.html` files generated. Especially if you use `--output-dir`.

## Setting up as a pre-commit hook

You can setup this entire workflow once as [pre-commit](https://pre-commit.com/) hook, and basically get an up-to-date analysis output directory for free `output-dir`. Schematically:

<img src="images/schema_workflow.png" width="700px">


You need to update the `.pre-commit-config.yaml` in your repository to include `nb_prep`:

```yaml
repos:
-   repo: https://github.com/allianz-direct/nb_prep
    rev: main
    hooks:
    -   id: nb_prep_precommit
    -   id: nb_prep_postcommit
```

You need to install the pre-commit and the post-commit hooks separately:

```shell
pre-commit install
pre-commit install --hook-type post-commit
```

When you commit a notebook, you might see something like:

```shell
git add notebook.ipynb
git commit -m "Add notebook"
# nb_prep (pre-commit; process notebooks)...................................Failed
# - hook id: nb_prep_precommit
# - files were modified by this hook
# nb_prep (post-commit; replace hash placeholder in .html filenames)........Passed
```

`nb_prep` has used [nbstripout](https://github.com/kynan/nbstripout) to overwrite `notebook.ipynb`. It has also created a file in the output directory named something like `20211026_notebook_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html`.

Re-add and re-commit the notebook again:

```shell
git add notebook.ipynb
git commit -m "Add notebook"
# nb_prep (pre-commit; process notebooks)...................................Passed
# nb_prep (post-commit; replace hash placeholder in .html filenames)........Passed
```

Because the output file already exists, `nb_prep` will not overwrite it, because if we would convert again and output it would be a stripped version without any cell outputs. 

Now, you've committed a clean, stripped version of `notebook.ipynb`. and you have a local snapshot of your notebook named something like `20211026_notebook_eac9e43.html`.

## Options

Options are documented also in the CLI tool, see `nb_prep --help`.

### Using templates

If you want to specify a different template for `nbconvert`, you can add an argument to the `nb_prep process` hook:

CLI:

```shell
nb_prep process --nbconvert-template 'reveal' .
```

Pre-commit hook:

```yaml
repos:
-   repo: https://github.com/allianz-direct/nb_prep
    rev: main
    hooks:
    -   id: nb_prep_precommit
        args: ["--nbconvert-template","reveal"]
    -   id: nb_prep_postcommit
```

### Removing cell blocks

You can also choose to remove input code blocks from the converted HTML (equivalent to `jupyter nbconvert --no-input`).

CLI:

```bash
nb_prep process --nbconvert-no-input .
```

Pre-commit hook:

```yaml
repos:
-   repo: https://github.com/allianz-direct/nb_prep
    rev: main
    hooks:
    -   id: nb_prep_precommit
        args: ["--nbconvert-no-input"]
    -   id: nb_prep_postcommit
```

### Specifying an output directory

You might want to output all HTML notebooks in a specific folder. The default is using the same folder as the notebook. You can specify different folder relative to the project root or by absolute path using `--output-dir`:

CLI:

```bash
nb_prep process --output-dir "~/workspace/notebook_output" .
```

Pre-commit hook:


```yaml
repos:
-   repo: https://github.com/allianz-direct/nb_prep
    rev: main
    hooks:
    -   id: nb_prep_precommit
        args: ["--output-dir","~/workspace/notebook_output"]
    -   id: nb_prep_postcommit
```

### Excluding directories and files

You can ignore certain notebooks or even entire directories with [globs](https://docs.python.org/3/library/glob.html), using a relative (to project root) or absolute path with `--exclude`. For example:

CLI:

```bash
nb_prep process --exclude "templates/*", "a_notebook.ipynb" .
```

Pre-commit hook:

```yaml
repos:
-   repo: https://github.com/allianz-direct/nb_prep
    rev: main
    hooks:
    -   id: nb_prep_precommit
        args: ["--exclude","templates/*", "a_notebook.ipynb"]
    -   id: nb_prep_postcommit
```
