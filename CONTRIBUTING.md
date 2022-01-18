# CONTRIBUTING

## Dev setup

```shell
pip install -r tests/test_requirements.txt
pre-commit install
```

## Edit drawings

We useed excalidraw, you can edit the vector image [here](https://excalidraw.com/#json=5272425855975424,sXm3L5A8Yr5EH9nkuENJIQ).

## Testing

There are some unit tests you can run with `pytest`. 

### manually test a specific hook

In a workspace directory, assuming already have a local clone of this repo:

```shell
mkdir test_prj
cp nb_prep/tests/data/example.ipynb test_prj/
cd test_prj
git init
git add --all
pre-commit try-repo ../nb_prep --verbose
git commit -m "test"
pre-commit try-repo ../nb_prep/ --verbose --hook-stage post-commit
```

### manually test a precommit config

In a workspace directory, assuming already have a local clone of this repo:

```shell
mkdir test_precommit_prj
cp nb_prep/tests/data/example.ipynb test_precommit_prj/
cp nb_prep/tests/data/pre-commit-test-config.yaml test_precommit_prj/.pre-commit-config.yaml
cd test_precommit_prj
git init
pre-commit install
pre-commit install --hook-type post-commit
git add --all
git commit -m "test"
```

