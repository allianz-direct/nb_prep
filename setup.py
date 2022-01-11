from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

setup_args = {
    "name": "precommit_nbconvert_rename",
    "version": "0.2",
    "packages": find_packages(),
    "install_requires": [
        "jupyter-client",  # BSD-3 https://github.com/jupyter/jupyter_client/blob/main/COPYING.md 
        "nbconvert", # BSD-3 https://github.com/jupyter/nbconvert/blob/main/LICENSE 
        "pre-commit" # MIT https://github.com/pre-commit/pre-commit/blob/master/LICENSE 
    ],
    "author": "Tim Vink",
    "author_email": "vinktim@gmail.com",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    "url": "",
    "entry_points": {
        "console_scripts": [
            "nbconvert_rename=precommit_nbconvert_rename.precommit:main",
            "rename_commithash=precommit_nbconvert_rename.postcommit:main",
        ]
    },
}

setup(**setup_args)
