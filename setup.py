from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

base_reqs = [
        "jupyter-client>=7.1.1",  # BSD-3 https://github.com/jupyter/jupyter_client/blob/main/COPYING.md
        "nbconvert>=6.4.0",  # BSD-3 https://github.com/jupyter/nbconvert/blob/main/LICENSE
        "pre-commit>=2.16.0",  # MIT https://github.com/pre-commit/pre-commit/blob/master/LICENSE
        "typer>=0.4.0",  # MIT https://github.com/tiangolo/typer/blob/master/LICENSE
        "nbstripout>=0.5.0",  # MIT https://github.com/kynan/nbstripout/blob/master/LICENSE.txt
    ]

setup_args = {
    "name": "nb_prep",
    "version": "1.0.2",
    "packages": find_packages(),
    "install_requires": base_reqs,
    "author": "Tim Vink",
    "author_email": "tim.vink@allianzdirect.nl",
    "description": "Prepares jupyter notebooks for storing stripped versions in git and sharing results with stakeholders",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    "url": "https://github.com/allianz-direct/nb_prep",
    "keywords": "precommit nbconvert nbstripout jupyter notebook python",
    "license": "MIT",
    "python_requires": ">=3.7",
    "classifiers": [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    "entry_points": {
        "console_scripts": [
            "nb_prep=nb_prep.cli:app",
        ]
    },
}

setup(**setup_args)
