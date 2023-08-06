# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aiai']

package_data = \
{'': ['*']}

install_requires = \
['aiai_eval>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'aiai',
    'version': '0.0.1',
    'description': 'Alexandra Institute Artificial Intelligence, a Python package for Danish data science.',
    'long_description': '<div align=\'center\'>\n<img src="https://raw.githubusercontent.com/alexandrainst/AIAI/main/gfx/aiai-logo.png" width="auto" height="224">\n</div>\n\n### A Python package for Danish data science\n##### _(pronounced as in "Aye aye captain")_\n\n______________________________________________________________________\n[![PyPI Status](https://badge.fury.io/py/aiai.svg)](https://pypi.org/project/aiai/)\n[![Documentation](https://img.shields.io/badge/docs-passing-green)](https://alexandrainst.github.io/aiai/aiai.html)\n[![License](https://img.shields.io/github/license/alexandrainst/aiai)](https://github.com/alexandrainst/aiai/blob/main/LICENSE)\n[![LastCommit](https://img.shields.io/github/last-commit/alexandrainst/aiai)](https://github.com/alexandrainst/aiai/commits/main)\n[![Code Coverage](https://img.shields.io/badge/Coverage-0%25-red.svg)](https://github.com/alexandrainst/aiai/tree/main/tests)\n\n\n## Installation\nTo install the package simply write the following command in your favorite terminal:\n```\n$ pip install aiai\n```\n\n## Quickstart\n### Benchmarking from the Command Line\nThe easiest way to benchmark pretrained models is via the command line interface. After\nhaving installed the package, you can benchmark your favorite model like so:\n```\n$ evaluate --model-id <model_id> --task <task>\n```\n\nHere `model_id` is the HuggingFace model ID, which can be found on the [HuggingFace\nHub](https://huggingface.co/models), and `task` is the task you want to benchmark the\nmodel on, such as "ner" for named entity recognition. See all options by typing\n```\n$ evaluate --help\n```\n\nThe specific model version to use can also be added after the suffix \'@\':\n```\n$ evaluate --model_id <model_id>@<commit>\n```\n\nIt can be a branch name, a tag name, or a commit id. It defaults to \'main\' for latest.\n\nMultiple models and tasks can be specified by just attaching multiple arguments. Here\nis an example with two models:\n```\n$ evaluate --model_id <model_id1> --model_id <model_id2> --task ner\n```\n\nSee all the arguments and options available for the `evaluate` command by typing\n```\n$ evaluate --help\n```\n\n### Benchmarking from a Script\nIn a script, the syntax is similar to the command line interface. You simply initialise\nan object of the `Evaluator` class, and call this evaluate object with your favorite\nmodels and/or datasets:\n```\n>>> from aiai import Evaluator\n>>> evaluator = Evaluator()\n>>> evaluator(\'<model_id>\', \'<task>\')\n```\n\n\n## Contributors\n\nIf you feel like this package is missing a crucial feature, if you encounter a bug or\nif you just want to correct a typo in this readme file, then we urge you to join the\ncommunity! Have a look at the [CONTRIBUTING.md](./CONTRIBUTING.md) file, where you can\ncheck out all the ways you can contribute to this package. :sparkles:\n\n- _Your name here?_ :tada:\n\n\n## Maintainers\n\nThe following are the core maintainers of the `aiai` package:\n\n- [@saattrupdan](https://github.com/saattrupdan) (Dan Saattrup Nielsen; saattrupdan@alexandra.dk)\n- [@AJDERS](https://github.com/AJDERS) (Anders Jess Pedersen; anders.j.pedersen@alexandra.dk)\n\n\n## Project structure\n```\n.\n├── .flake8\n├── .github\n│\xa0\xa0 └── workflows\n│\xa0\xa0     ├── ci.yaml\n│\xa0\xa0     └── docs.yaml\n├── .gitignore\n├── .pre-commit-config.yaml\n├── CHANGELOG.md\n├── CODE_OF_CONDUCT.md\n├── CONTRIBUTING.md\n├── LICENSE\n├── README.md\n├── gfx\n│\xa0\xa0 └── aiai-logo.png\n├── makefile\n├── notebooks\n├── poetry.toml\n├── pyproject.toml\n├── src\n│\xa0\xa0 ├── aiai\n│\xa0\xa0 │\xa0\xa0 └── __init__.py\n│\xa0\xa0 └── scripts\n│\xa0\xa0     ├── fix_dot_env_file.py\n│\xa0\xa0     └── versioning.py\n└── tests\n    └── __init__.py\n```\n',
    'author': 'Dan Saattrup Nielsen',
    'author_email': 'dan.nielsen@alexandra.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
