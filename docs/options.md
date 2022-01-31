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

    If you use a custom nbconvert template in combination with a pre-commit hook, you'll need to specify it as an `additional_dependencies`. For example when using [nbconvert-acme](https://github.com/SylvainCorlay/nbconvert-acme/):

    ```yaml
    # .pre-commit-config.yaml
    repos:
    -   repo: https://github.com/allianz-direct/nb_prep
        rev: main
        hooks:
        -   id: nb_prep_precommit
            args: ["--nbconvert-template","acme"]
            additional_dependencies: ["git+https://github.com/SylvainCorlay/nbconvert-acme"]
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

## Removing commit hash

Inserting a commit hash into the HTML filename can be useful to track which commit created the content. You can disable it using the `--no-git-hash-suffix` parameter. Note we also do not need the `nb_prep rename` step anymore.

=== "CLI"

    ```bash
    nb_prep process --no-git-hash-suffix .
    ```

===  "Pre-commit hook"

    ```yaml
    # .pre-commit-config.yaml
    repos:
    -   repo: https://github.com/allianz-direct/nb_prep
        rev: main
        hooks:
        -   id: nb_prep_precommit
            args: ["--no-git-hash-suffix"]
    ```

    !!! warning

        `nb_prep process` will not overwrite any output files that already exist.
        When you use the default setting, only the first commit of the day will generate output.

        To fix that, use a more detailed date prefix like `%Y%m%d%H%M%S`.



## Removing date prefix

By default, output HTML will have a YYYYMMDD_ prefix. You can remove it by setting an empty prefix (`""`) or change the prefix by speficying a different format (see [strftime cheatsheet](https://strftime.org/)).

=== "CLI"

    ```bash
    nb_prep process --date-prefix "" .
    ```

===  "Pre-commit hook"

    ```yaml
    # .pre-commit-config.yaml
    repos:
    -   repo: https://github.com/allianz-direct/nb_prep
        rev: main
        hooks:
        -   id: nb_prep_precommit
            args: ["--date-prefix", ""]
    ```
