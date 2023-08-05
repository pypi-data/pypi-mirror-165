# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['modelator',
 'modelator.checker',
 'modelator.cli',
 'modelator.monitors',
 'modelator.pytest',
 'modelator.utils']

package_data = \
{'': ['*'], 'modelator': ['samples/*'], 'modelator.monitors': ['templates/*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'deepdiff>=5.8.1,<6.0.0',
 'modelator-py>=0.2.1,<0.3.0',
 'munch>=2.5.0,<3.0.0',
 'pyrsistent>=0.18.1,<0.19.0',
 'rich>=12.5.1,<13.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'toml>=0.10.2,<0.11.0',
 'typer[all]>=0.6.1,<0.7.0',
 'typing-extensions>=4.2.0,<5.0.0',
 'watchdog>=2.1.8,<3.0.0',
 'wget>=3.2,<4.0']

entry_points = \
{'console_scripts': ['modelator = modelator.cli:app'],
 'pytest11': ['pytest-modelator = modelator.pytest']}

setup_kwargs = {
    'name': 'modelator',
    'version': '0.6.1',
    'description': 'Framework for Model Based Testing',
    'long_description': '# Modelator\n\n| ⚠️ We are working on a new and entirely reworked Modelator architecture for improved performance and interoperability. Therefore, the current version is not maintained. The reworked version will be released in Q3 2022. ⚠️ |\n| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |\n\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)\n[![Release](https://img.shields.io/github/v/release/informalsystems/modelator?sort=semver&include_prereleases)](https://github.com/informalsystems/modelator/releases)\n[![Build Status](https://github.com/informalsystems/modelator/actions/workflows/python.yml/badge.svg)](https://github.com/informalsystems/modelator/actions/workflows/python.yml)\n\nThis repository contains the source code for `modelator` - a framework and tools for model-based testing.\n\n_We deprecated `modelator` support for Rust and Go. `modelator` is used as a python package._\n\n# Instruction\n\nTo install `modelator` via `pip`, execute the following\n\n```sh\n# over https\npip install git+https://github.com/informalsystems/modelator\n# or, over ssh\npip install git+ssh://git@github.com/informalsystems/modelator\npython\n...\n>>> import modelator\n```\n\nIf you are using a Poetry project, execute the following to add `modelator` as a dependency,\n\n```sh\n# over https\npoetry add git+ssh://git@github.com/informalsystems/modelator#dev # `poetry` assumes `master` as default branch\n# or, over ssh\npoetry add git+https://github.com/informalsystems/modelator#dev\n```\n\n## Contributing\n\nIf you wish to contribute to `modelator`, set up the repository as follows,\n\n```\ngit clone git@github.com/informalsystems/modelator\ncd modelator\npoetry install\npoetry shell\n```\n\n## License\n\nCopyright © 2021-2022 Informal Systems Inc. and modelator authors.\n\nLicensed under the Apache License, Version 2.0 (the "License"); you may not use the files in this repository except in compliance with the License. You may obtain a copy of the License at\n\n    https://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.\n',
    'author': 'Andrey Kuprianov',
    'author_email': 'andrey@informal.systems',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/informalsystems/atomkraft',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
