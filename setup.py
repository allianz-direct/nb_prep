from setuptools import setup, find_packages

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup_args = {
    'name': 'precommit_nbconvert_rename',
    'version': '0.0.1',
    'packages': find_packages(),
    'install_requires': ["jupyter-core","nbconvert"],
    'author': 'Tim Vink',
    'author_email': 'vinktim@gmail.com',
    'long_description': long_description,
    'long_description_content_type': 'text/markdown',
    'url': '',
    'entry_points': {"console_scripts": ["nbconvert_rename=precommit_nbconvert_rename.precommit:main"]},
}

setup(**setup_args)
