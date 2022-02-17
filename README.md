[![Unit tests](https://github.com/allianz-direct/nb_prep/actions/workflows/unit_tests.yml/badge.svg)](https://github.com/allianz-direct/nb_prep/actions/workflows/unit_tests.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nb-prep)
![PyPI](https://img.shields.io/pypi/v/nb-prep)
![PyPI - Downloads](https://img.shields.io/pypi/dm/nb-prep)
![GitHub contributors](https://img.shields.io/github/contributors-anon/allianz-direct/nb_prep)
![PyPI - License](https://img.shields.io/pypi/l/nb-prep)

# nb_prep

`nb_prep` automates preparing jupyter notebooks for sharing and storage.

You can use the `nb_prep` CLI to:

- Convert jupyter notebooks to HTML (using [`nbconvert`](https://nbconvert.readthedocs.io/)) and:
    - add a date prefix to the filename.
    - add a git hash suffix to the filename.
    - move the HTML file to a configured output directory
- Strip jupyter notebooks of all cell outputs (using [`nbstripout`](https://github.com/kynan/nbstripout))

You can also configure `nb_prep` once as a pre- and post-commit hook and have notebook output automatically prepared every time you `git commit`.

`nb_prep` is a useful automation tool when you have a lot of analysis notebooks in git that you want to share with stakeholders.
If your main interest is preparing clean notebooks for storing in git commits, consider using [jupytext](https://github.com/mwouts/jupytext) instead.

## Installation

```bash
pip install nb_prep
```

## Documentation

See [allianz-direct.github.io/nb_prep](https://allianz-direct.github.io/nb_prep).
