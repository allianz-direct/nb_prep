# precommit_nbconvert_rename

Use `nbconvert` and `nbstripout` together as precommit hooks.

A pre-commit hook that converts any changed jupyter notebooks (`.ipynb`) to `.html` files with a YYYMMDD date prefix and commit hash suffix added:

`my_notebook.ipynb` -> `20211026_my_notebook_eac9e43.html`

## Use case

Jupyter notebooks contain not only code but also outputs (tables, plots, interactive elements) as well as execution counts. You should not commit data to git (also because of security) so a common solution for jupyter notebooks is to use [nbstripout](https://github.com/kynan/nbstripout) as [pre-commit](https://pre-commit.com/) hook. This has as added benefit that your notebooks are not more easily version-controlled, as re-running a cell does not lead to a `git diff`. The downside is having to re-execute notebooks everytime you want to view or share them.

`precommit_nbconvert_rename` runs [nbconvert](https://github.com/jupyter/nbconvert) each time you make a commit that touches a jupyter notebook, and adds a date prefix and commit hash suffix to the filename. Having the commit hash in the file named has the added benefit that you can always find the changes in the file in git. Obviously these `.html` should remain local and not be committed to `git`, so make sure to `*.html` to your `.gitignore` file. Here's an overview of the workflow:

<img src="images/schema_workflow.png" width="700px">

> Note: `nbstripout` pre-commit hooks will edit your notebook files and fail the pre-commit. When you add the stripped notebook and commit again, `nbconvert-rename` will not run `nbconvert` again because there is already .html file

## Installation

```bash
python -m pip install git+https://github.developer.allianz.io/allianz-direct/precommit_nbconvert_rename.git
```

> Why `python -m pip` instead of just `pip`? See this post on [why it has fewer problems](https://adamj.eu/tech/2020/02/25/use-python-m-pip-everywhere/)

## Usage

You need to update the `.pre-commit-config.yaml` in your repository. We'll assume you want to use `nbconvert_rename` with [nbstripout](https://github.com/kynan/nbstripout#using-nbstripout-as-a-pre-commit-hook) and include that here:

```yaml
default_stages: [commit]
repos:
-   repo: local
    hooks:
    -   id: nbconvert_rename_precommit
        name: precommit_nbconvert_rename (pre-commit; run nbconvert)
        description: 'Converts to .ipynb to .html and adds date prefix and hash placeholder.'
        entry: nbconvert_rename
        language: python
        language_version: python3
        types: [jupyter]
        stages: [commit]
    -   id: nbconvert_rename_postcommit
        name: precommit_nbconvert_rename (post-commit; replace commithash in .html filenames)
        description: 'Replaces NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER with commit hash in any .html filenames.'
        entry: rename_commithash
        types: [html]    
        language: python
        language_version: python3
        always_run: true
        stages: [post-commit]
-   repo: local
    hooks:
      - id: nbstripout
        name: nbstripout
        entry: nbstripout
        language: system
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
# precommit_nbconvert_rename (pre-commit; run nbconvert)............................Passed
# nbstripout........................................................................Failed
# - hook id: nbstripout
# - files were modified by this hook
# precommit_nbconvert_rename (post-commit; replace commithash in .html filenames)...Passed
```

`nbstripout` has overwritten `notebook.ipynb` and `nbconvert-rename` has created a file named something like `20211026_notebook_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html`.
Make sure to avoid committing HTML files by adding `.html` added to your `.gitignore` file. Next:

```shell
git add notebook.ipynb
git commit -m "Add notebook"
# precommit_nbconvert_rename (pre-commit; run nbconvert)............................Passed
# nbstripout........................................................................Passed
# precommit_nbconvert_rename (post-commit; replace commithash in .html filenames)...Passed
```

Now, you've committed a clean, stripped version of `notebook.ipynb` and you have a local snapshot of your notebook named something like `20211026_notebook_eac9e43.html`.

## Options

### Using templates

If you want to specify a different template for `nbconvert`, you can add an argument to the `nbconvert_rename_precommit` hook:

```yaml
-   repo: local
    hooks:
    -   id: nbconvert_rename_precommit
        entry: nbconvert_rename
        ...
        args: ["--template","reveal"]
```

### Removing cell blocks

You can also choose to remove input code blocks (equivalent to `jupyter nbconvert --no-input`)

```yaml
-   repo: local
    hooks:
    -   id: nbconvert_rename_precommit
        entry: nbconvert_rename
        ...
        args: ["--no-input"]
```

### Specifying an output directory

You might want to output all HTML notebooks in a specific folder. You can specify a relative (to project root) or absolute path using `--output-dir`:

```yaml
-   repo: local
    hooks:
    -   id: nbconvert_rename_precommit
        entry: nbconvert_rename
        ...
        args: ["--output-dir","../data/notebooks"]
```

### Excluding directories and files

You can ignore certain notebooks or even entire directories with [globs](https://docs.python.org/3/library/glob.html), using a relative (to project root) or absolute path with `--exclude`. For example:

```yaml
-   repo: local
    hooks:
    -   id: nbconvert_rename_precommit
        entry: nbconvert_rename
        ...
        args: ["--exclude","../data/notebooks/*", "a_notebook.ipynb"]
```
