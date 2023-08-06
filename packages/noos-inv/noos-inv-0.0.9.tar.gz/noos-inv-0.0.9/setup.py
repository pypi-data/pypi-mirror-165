# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['noos_inv']

package_data = \
{'': ['*']}

install_requires = \
['invoke']

entry_points = \
{'console_scripts': ['noosinv = noos_inv:main.run']}

setup_kwargs = {
    'name': 'noos-inv',
    'version': '0.0.9',
    'description': 'Shared workflows across CI/CD pipelines',
    'long_description': '[![CircleCI](https://circleci.com/gh/noosenergy/noos-invoke.svg?style=svg&circle-token=68d1a71e4f53ab1a1f33110e9a8c24bd3300a8ba)](https://circleci.com/gh/noosenergy/noos-invoke)\n\n# Noos Invoke\n\nSoftware development kit for sharing workflows across CI/CD pipelines.\n\nSuch a project aims to enforce parity and reproducability between local development and CI/CD workflows in remote containers (e.g. executable versions, command line calls, environment variables...) - developped with `inv[oke]`(https://github.com/pyinvoke/invoke).\n\n## Installation\n\nInstall the package from the [PyPi repository](https://pypi.org/project/noos-inv/):\n\n    $ pip install noos-inv\n\nTo enable shell completion, execute the following command (e.g. `zsh`),\n\n    $ noosinv --print-completion-script=zsh\n\nAnd copy/paste its `stdout` into your shell config.\n\n```bash\n# NOOSINV completion script\n\n_complete_noosinv() {\n    collection_arg=\'\'\n    if [[ "${words}" =~ "(-c|--collection) [^ ]+" ]]; then\n        collection_arg=$MATCH\n    fi\n    reply=( $(noosinv ${=collection_arg} --complete -- ${words}) )\n}\n\ncompctl -K _complete_noosinv + -f noosinv\n```\n\nFinally, still in your shell config, enable automatic sub shell loading:\n\n```bash\n# ENV variable sub shell loading with command "source .env"\n\nset -a\n```\n\n## Usage as a command line tool\n\nThe `noos-inv` package installs a CLI binary, for managing common CI/CD tasks.\n\nFrom the terminal,\n\n```\n$ noosinv\n\nUsage: noosinv [--core-opts] <subcommand> [--subcommand-opts] ...\n\nSubcommands:\n\n  docker.build       Build Docker image locally.\n  docker.login       Login to Docker remote registry (AWS ECR or Dockerhub).\n  docker.push        Push Docker image to a remote registry.\n  git.config         Setup git credentials with a Github token.\n  helm.install       Provision local Helm client (Chart Museum Plugin).\n  helm.lint          Check compliance of Helm charts / values.\n  helm.login         Login to Helm remote registry (Chart Museum).\n  helm.push          Push Helm chart to a remote registry.\n  helm.test          Test local deployment in Minikube.\n  local.dotenv       Create local dotenv file.\n  python.clean       Clean project from temp files / dirs.\n  python.coverage    Run coverage test report.\n  python.format      Auto-format source code.\n  python.lint        Run python linters.\n  python.package     Build project wheel distribution.\n  python.release     Publish wheel distribution to PyPi.\n  python.test        Run pytest with optional grouped tests.\n  terraform.run      Run a plan in Terraform cloud.\n  terraform.update   Update variable in Terraform cloud.\n```\n\nSource your environnement variables first for a seamless experience.\n(use command `local.dotenv` to create it from the provided template)\n\n    $ source .env\n\n## Development\n\nOn Mac OSX, make sure [poetry](https://python-poetry.org/) has been installed and pre-configured,\n\n    $ brew install poetry\n\nThis project is shipped with a Makefile, which is ready to do basic common tasks.\n\n```\n$ make\n\nhelp                           Display this auto-generated help message\nupdate                         Lock and install build dependencies\nclean                          Clean project from temp files / dirs\nformat                         Run auto-formatting linters\ninstall                        Install build dependencies from lock file\nlint                           Run python linters\ntest                           Run pytest with all tests\npackage                        Build project wheel distribution\nrelease                        Publish wheel distribution to PyPi\n```\n',
    'author': 'Noos Energy',
    'author_email': 'contact@noos.energy',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noosenergy/noos-invoke',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
