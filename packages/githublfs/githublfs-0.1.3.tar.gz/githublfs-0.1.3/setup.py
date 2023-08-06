# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['githublfs']
install_requires = \
['PyGithub>=1.55,<2.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'githublfs',
    'version': '0.1.3',
    'description': 'Simple library to commit lfs files to Github repos',
    'long_description': 'Python Github LFS client\n========================\ngithublfs is a Python library currently exposing a single method to upload and commit a file to a Github repository\nusing git LFS.\n\nSee https://git-lfs.github.com/\n\nInstallation\n------------\n``pip install githublfs``\n\nUsage\n-----\n>>> from githublfs import commit_lfs_file\n>>> commit_lfs_file(repo="AnesFoufa/githublfs",\n                    token="gh_token_with_repo_scope",\n                    branch="main",\n                    path="assets/logo.jpg",\n                    content=b"binary file content",\n                    message="my commit message")\n\nTo authenticate, an access token with repo scope is neede. See: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token\n\nDependencies\n------------\n* python = "^3.7"\n* PyGithub = "^1.55"\n* requests = "^2.28.1"\n\nImplementation details\n----------------------\nThis library uses LFS\' Basic Transfer API. See https://github.com/git-lfs/git-lfs/blob/main/docs/api/basic-transfers.md\n\nProduction warning\n------------------\nThis library is still experimental. If you use it in production, please pin the exact version in your requirements, including the minor number.',
    'author': 'Anès Foufa',
    'author_email': 'anes.foufa@upply.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AnesFoufa/githublfs',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
