from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

setup_args = {
    "name": "precommit_nbconvert_rename",
    "version": "0.2",
    "packages": find_packages(),
    "install_requires": [
        "jupyter-client>=7.1.1",  # BSD-3 https://github.com/jupyter/jupyter_client/blob/main/COPYING.md
        "nbconvert>=6.4.0",  # BSD-3 https://github.com/jupyter/nbconvert/blob/main/LICENSE
        "pre-commit>=2.16.0",  # MIT https://github.com/pre-commit/pre-commit/blob/master/LICENSE
        "typer>=0.4.0",  # MIT https://github.com/tiangolo/typer/blob/master/LICENSE
    ],
    "author": "Tim Vink",
    "author_email": "vinktim@gmail.com",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    "url": "",
    "entry_points": {
        "console_scripts": [
            "nb_convert_strip=precommit_nbconvert_rename.cli:app",
        ]
    },
}

setup(**setup_args)
