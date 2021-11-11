from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

setup_args = {
    "name": "precommit_nbconvert_rename",
    "version": "0.0.2",
    "packages": find_packages(),
    "install_requires": ["jupyter-client", "nbconvert", "pre-commit"],
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
