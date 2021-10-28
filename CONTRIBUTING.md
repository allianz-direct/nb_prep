# CONTRIBUTING

## Dev setup

```shell
pip install -r dev_requirements.txt
pre-commit install
```

## Testing

There are some unit tests you can run with `pytest`. For pre-commit here's how to do a manual test:

```shell
# Start a new project
git clone <this project>
mkdir test_prj
cp precommit_nbconvert_rename/tests/data/example.ipynb test_prj/
cd test_prj
git init
git add --all
pre-commit try-repo ..\precommit_nbconvert_rename\ --verbose
git commit -m "test"
pre-commit try-repo ..\precommit_nbconvert_rename\ --verbose --hook-stage post-commit
```


