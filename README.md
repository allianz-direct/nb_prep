# precommit_nbconvert_rename

A pre-commit hook that converts any changed jupyter notebooks (`.ipynb`) to `.html` files with a YYYMMDD date prefix and commit hash suffix added:

`my_notebook.ipynb` -> `20211026_my_notebook_eac9e43.ipynb`

## Use case

Jupyter notebooks contain not only code but also outputs (tables, plots, interactive elements) as well as execution counts. You should not commit data to git (also because of security) so a common solution for jupyter notebooks is to use [nbstripout](https://github.com/kynan/nbstripout) as pre-commit hook. This has as added benefit that your notebooks are not more easily version-controlled, as re-running a cell does not lead to a `git diff`. The downside is having to re-execute notebooks when you want to share them with stakeholders.

`precommit_nbconvert_rename` runs [nbconvert](https://github.com/jupyter/nbconvert) each time you make a change a commit that touches a jupyter notebook. Having the commit hash in the file named has the added benefit that you can always find the changes in the file in git. Obviously these `.html` should remain local and not be committed to `git`, so make sure to `*.html` to your `.gitignore` file.

## Installation

```bash
python -m pip install precommit_nbconvert_rename
```

> Why `python -m pip` instead of just `pip`? See this post on [why it has fewer problems](https://adamj.eu/tech/2020/02/25/use-python-m-pip-everywhere/)

## Usage

Once you have [pre-commit](https://pre-commit.com/) installed, add this to the `.pre-commit-config.yaml` in your repository:

```yaml
repos:
- repo: TODO
  rev: v0.0.1
  hooks:
  - id: TODO
```

Then run `pre-commit install` and you're ready to go.

`pre-commit install --hook-type post-commit`

```yaml
-   repo: local
    hooks:
    -   id: post-commit-local
        name: post commit
        always_run: true
        stages: [post-commit]
```

> Since post-commit does not operate on files `always_run` is set to `True`

