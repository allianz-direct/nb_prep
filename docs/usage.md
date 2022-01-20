---
hide:
  - navigation
---

# Usage

## Use case
You use [jupyter notebooks](https://jupyter.org/) and:

- [nbconvert](https://github.com/jupyter/nbconvert) to convert `.ipynb` files to `.html` files
- [nbstripout](https://github.com/kynan/nbstripout) to avoid committing (potentially sensitive) data to git and get proper `git diff`s on notebooks (only showing changes in code).

Forget to run `nbconvert` or use them in the wrong order (`nbstripout` before `nbconvert`) and you will have to re-run your notebooks before you can output HTML, which can be annoying when they are long-running. Especially when you use `nbstripout` as a [pre-commit](https://pre-commit.com/) hook, this can happen quite often.

`nb_prep` can help to automatically process notebooks and (optionally) store versioned output in an in output directory. 

## Using as a CLI

The CLI command `nb_prep process` takes a list of directories and/or files to find and process notebooks. For each notebook:

- `nbconvert` is used to create an `<filename>.html` export
- A date prefix is added `YYYYMMDD_<filename>.html` (can be turned off)
- A placeholder for git hash is added `YYYYMMDD_<filename>_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html`
- The `.html` file is moved to an `output-dir` (if specified)
- The `nbstripout` is used strip output from the `.ipynb` file

Now you can `git add` and `git commit` the changed notebook files. You can then use `nb_prep rename` to insert the commit hashes in the notebook filenames. For example:

`20220101_my_notebook_NBCONVERT_RENAME_COMMITHASH_PLACEHOLDER.html` -> `20220101_my_notebook_eac9e43.html`

!!! tip

    You'll probably want to `.gitignore` the `.html` files generated. Especially if you use `--output-dir`.

## Setting up as a pre-commit hook

You can setup this entire workflow once as [pre-commit](https://pre-commit.com/) hook, and basically get an up-to-date analysis output directory for free `output-dir`. Schematically:

<img src="/assets/images/schema_workflow.png">


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

