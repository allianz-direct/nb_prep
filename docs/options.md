---
hide:
  - navigation
---

# Options

Options are also documented in the CLI tool, see 

```shell
nb_prep --help
```

## Using templates

If you want to specify a different template for `nbconvert`, you can add an argument to the `nb_prep process` hook:

=== "CLI"

    ```bash
    nb_prep process --nbconvert-template 'reveal' .
    ```

===  "Pre-commit hook"

    ```yaml
    # .pre-commit-config.yaml
    repos:
    -   repo: https://github.com/allianz-direct/nb_prep
        rev: main
        hooks:
        -   id: nb_prep_precommit
            args: ["--nbconvert-template","reveal"]
        -   id: nb_prep_postcommit
    ```

## Removing cell blocks

You can also choose to remove input code blocks from the converted HTML (equivalent to `jupyter nbconvert --no-input`).


=== "CLI"

    ```bash
    nb_prep process --nbconvert-no-input .
    ```

===  "Pre-commit hook"

    ```yaml
    # .pre-commit-config.yaml
    repos:
    -   repo: https://github.com/allianz-direct/nb_prep
        rev: main
        hooks:
        -   id: nb_prep_precommit
            args: ["--nbconvert-no-input"]
        -   id: nb_prep_postcommit
    ```

## Specifying an output directory

You might want to output all HTML notebooks in a specific folder. The default is using the same folder as the notebook. You can specify different folder relative to the project root or by absolute path using `--output-dir`:

=== "CLI"

    ```bash
    nb_prep process --output-dir "~/workspace/notebook_output" .
    nb_prep rename --output-dir "~/workspace/notebook_output" .
    ```

===  "Pre-commit hook"

    ```yaml
    # .pre-commit-config.yaml
    repos:
    -   repo: https://github.com/allianz-direct/nb_prep
        rev: main
        hooks:
        -   id: nb_prep_precommit
            args: ["--output-dir","~/workspace/notebook_output"]
        -   id: nb_prep_postcommit
            args: ["--output-dir","~/workspace/notebook_output"]
    ```

## Excluding directories and files

You can ignore certain notebooks or even entire directories with [globs](https://docs.python.org/3/library/glob.html), using a relative (to project root) or absolute path with `--exclude`. For example:

=== "CLI"

    ```bash
    nb_prep process --exclude "templates/*", "a_notebook.ipynb" .
    ```

===  "Pre-commit hook"

    ```yaml
    # .pre-commit-config.yaml
    repos:
    -   repo: https://github.com/allianz-direct/nb_prep
        rev: main
        hooks:
        -   id: nb_prep_precommit
            args: ["--exclude","templates/*", "a_notebook.ipynb"]
        -   id: nb_prep_postcommit
    ```
