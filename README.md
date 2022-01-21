[![Unit tests](https://github.com/allianz-direct/nb_prep/actions/workflows/unit_tests.yml/badge.svg)](https://github.com/allianz-direct/nb_prep/actions/workflows/unit_tests.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nb-prep)
![PyPI](https://img.shields.io/pypi/v/nb-prep)
![PyPI - Downloads](https://img.shields.io/pypi/dm/nb-prep)
![GitHub contributors](https://img.shields.io/github/contributors/timvink/nb-prep)
![PyPI - License](https://img.shields.io/pypi/l/nb-prep)

# nb_prep

`nb_prep` prepares jupyter notebooks for storing stripped versions in git and sharing results with stakeholders.

You can use the `nb_prep` CLI to:

- Convert jupyter notebooks to HTML (using [`nbconvert`](https://nbconvert.readthedocs.io/)) and:
    - add a date prefix to the filename.
    - add a git hash suffix to the filename.
    - move the HTML file to a configured output directory
- Strip all cell outputs (using [`nbstripout`](https://github.com/kynan/nbstripout))

You can also configure `nb_prep` once as a pre-commit hook and have notebook output automatically prepared every time you `git commit`.

## Installation

```bash
pip install nb_prep
```

## Documentation

See [allianz-direct.github.io/nb_prep](https://allianz-direct.github.io/nb_prep).