# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oliver',
 'oliver.integrations',
 'oliver.integrations.aws',
 'oliver.integrations.azure',
 'oliver.lib',
 'oliver.subcommands']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'azure-cosmos>=3.1.2,<5.0.0',
 'boto3>=1.11.9,<2.0.0',
 'logzero>=1.5.0,<2.0.0',
 'mypy-boto3[batch,logs]>=1.12.17,<2.0.0',
 'mypy_boto3_batch>=1.12.21,<2.0.0',
 'mypy_boto3_logs>=1.12.21,<2.0.0',
 'pendulum>=2.0.5,<3.0.0',
 'requests>=2.22.0,<3.0.0',
 'tabulate>=0.8.6,<0.9.0',
 'typed-ast==1.5.2',
 'tzlocal<3.0.0']

entry_points = \
{'console_scripts': ['oliver = oliver.__main__:main']}

setup_kwargs = {
    'name': 'stjudecloud-oliver',
    'version': '1.4.9',
    'description': 'An opinionated Cromwell orchestration system',
    'long_description': '<p align="center">\n  <h1 align="center">\n    Oliver\n  </h1>\n\n  <p align="center">\n    <a href="https://actions-badge.atrox.dev/stjudecloud/oliver/goto" target="_blank">\n      <img alt="Actions: CI Status"\n          src="https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fstjudecloud%2Foliver%2Fbadge&style=flat" />\n    </a>\n    <a href="https://pypi.org/project/stjudecloud-oliver/" target="_blank">\n      <img alt="PyPI"\n          src="https://img.shields.io/pypi/v/stjudecloud-oliver?color=orange">\n    </a>\n    <a href="https://pypi.org/project/stjudecloud-oliver/" target="_blank">\n      <img alt="PyPI: Downloads"\n          src="https://img.shields.io/pypi/dm/stjudecloud-oliver?color=orange">\n    </a>\n    <a href="https://anaconda.org/conda-forge/oliver" target="_blank">\n      <img alt="Conda"\n          src="https://img.shields.io/conda/vn/conda-forge/oliver.svg?color=brightgreen">\n    </a>\n    <a href="https://anaconda.org/conda-forge/oliver" target="_blank">\n      <img alt="Conda: Downloads"\n          src="https://img.shields.io/conda/dn/conda-forge/oliver?color=brightgreen">\n    </a>\n    <a href="https://codecov.io/gh/stjudecloud/oliver" target="_blank">\n      <img alt="Code Coverage"\n          src="https://codecov.io/gh/stjudecloud/oliver/branch/master/graph/badge.svg" />\n    </a>\n    <a href="https://github.com/stjudecloud/oliver/blob/master/LICENSE.md" target="_blank">\n    <img alt="License: MIT"\n          src="https://img.shields.io/badge/License-MIT-blue.svg" />\n    </a>\n  </p>\n\n\n  <p align="center">\n    An opinionated Cromwell orchestration manager.\n    <br />\n    <a href="https://stjudecloud.github.io/oliver/"><strong>Explore the docs »</strong></a>\n    <br />\n    <br />\n    <a href="https://github.com/stjudecloud/oliver/issues/new?assignees=&labels=&template=feature_request.md&title=Descriptive%20Title&labels=enhancement">Request Feature</a>\n    ·\n    <a href="https://github.com/stjudecloud/oliver/issues/new?assignees=&labels=&template=bug_report.md&title=Descriptive%20Title&labels=bug">Report Bug</a>\n    ·\n    ⭐ Consider starring the repo! ⭐\n    <br />\n  </p>\n</p>\n\n<!-- ## 🎨 Demo -->\n<br />\n<p align="center">\n  <img alt="Example of Oliver usage" src="https://stjudecloud.github.io/oliver/images/oliver-example.gif"/>\n</p>\n<br />\n\n## 🎨 Features\n\n\n* <b>Workflow Orchestration.</b> Easily submit, inspect, kill, and retry workflows in a Cromwell environment.\n* <b>Better Job Tracking.</b> Jobs can be associated with names and job groups to enable better status reporting.\n* <b>Dynamic Argument Parsing.</b> Specify inputs and options on the command line rather than editing JSON files.\n* <b>Third-party Cloud Integrations.</b> Use the `aws` and `azure` subcommands to explore cloud-specific functionality.\n\n## 📚 Getting Started\n\n### Installation\n\n#### Conda\n\nOliver is distributed as a package using the community-curated Anaconda repository, [conda-forge](https://conda-forge.org/). You\'ll need to [install conda][conda-install], and we recommend that you first follow [the instructions included in the conda-forge documentation][conda-forge-setup] to get everything set up!\n\n```bash\nconda install oliver -c conda-forge\n```\n\n#### Python Package Index\n\nYou can also install Oliver using the Python Package Index ([PyPI](https://pypi.org/)).\n\n```bash\npip install stjudecloud-oliver\n```\n\n### Configuring\n\nNext, we recommend that you configure oliver so that common arguments can be saved. By default, Oliver will prompt you for the answers interactively.\n\n```bash\noliver configure\n```\n\nIf you are setting up Oliver programmatically, you can accept a default configuration (`oliver configure --defaults`) and edit from there using `oliver config`.\n\n## 🚌 A Quick Tour\n\nAt its foundation, Oliver is an opinionated job orchestrator for Cromwell. Commonly, you will want to use it to submit a job, inspect a job\'s status, kill a job, retry a job (possibly with different parameters), and organize job results.\n\nIf you\'re interested in a complete overview of Oliver\'s capabilities, please see [**the documentation pages**](https://stjudecloud.github.io/oliver/)</a>.\n\n#### Submit a Job\n\nThe simplest possible job submission is one which submits a simple workflow with one or more input JSON file(s) and/or key-value pair(s).\n\n```bash\noliver submit workflow.wdl inputs.json input_key=input_value\n```\n\nYou can similarly set workflow options and labels by prepending arguments with `@` and `%` respectively.\n\n```bash\n# works for files too!\noliver submit workflow.wdl @option=foo %label=bar\n```\n\nPlease [**see the docs**](https://stjudecloud.github.io/oliver/getting-started/submit-jobs/) for more details on job submission.\n\n#### Inspect a Job\n\nOnce a job is submitted, you can interrogate the Cromwell server about its status.\n\n```bash\noliver inspect workflow-id\n```\n\nIf you aren\'t sure what workflow identifier was given to your job, you can easily track it down using the `status` subcommand.\n\n```bash\n# detailed view, which shows individual workflow statuses\noliver status -d\n```\n\n#### Kill a Job\n\nIf, for whatever reason, you\'d like to stop a job, you can use Oliver to instruct Cromwell to do so.\n\n```bash\noliver kill workflow-id\n```\n\n#### Retry a Job\n\nRetrying a workflow is similarly easy: even if you need to override previously set parameters (e.g. increase the memory capacity for a task).\n\n```bash\n# override previous inputs by specifying arguments (the same way as you would for `submit`).\noliver retry workflow-id\n```\n\n## 🖥️ Development\n\nIf you are interested in contributing to the code, please first review\nour [CONTRIBUTING.md][contributing-md] document. To bootstrap a\ndevelopment environment, please use the following commands.\n\n```bash\n# Clone the repository\ngit clone git@github.com:stjudecloud/oliver.git\ncd oliver\n\n# Install the project using poetry\npoetry install\n\n# Ensure pre-commit is installed to automatically format\n# code using `black`.\nbrew install pre-commit\npre-commit install\npre-commit install --hook-type commit-msg\n```\n\n## 🚧️ Tests\n\nOliver provides a (currently patchy) set of tests — both unit and end-to-end. To get started with testing, you\'ll\nneed to bootstrap a Docker test environment (one-time operation).\n\n```bash\n# Start development environment\ndocker image build --tag oliver .\ndocker-compose up --build  -d\n\nalias docker-run-oliver="docker container run \\\n  -it \\\n  --rm \\\n  --network oliver_default \\\n  --mount type=bind,source=$PWD/seeds,target=/opt/oliver/seeds \\\n  --mount type=bind,source=$PWD/oliver,target=/opt/oliver/oliver \\\n  --mount type=bind,source=$PWD/tests,target=/opt/oliver/tests \\\n  --entrypoint \'\' \\\n  oliver:latest"\n\n# Seed development environment (make sure Cromwell is live first!)\ndocker-run-oliver bash seeds/seed.sh http://cromwell:8000 seeds/wdl/hello.wdl\ndocker-run-oliver pytest --cov=./ --cov-report=xml\n```\n\nTo reset your entire docker-compose environment, you can run the following:\n\n```bash\ndocker-compose down\n\ndocker image rm oliver:latest\ndocker image rm oliver_cromwell:latest\ndocker image rm mysql:5.7\ndocker volume rm oliver_mysql_data\ndocker network rm oliver_default\n\ndocker image build --tag oliver .\ndocker-compose up --build -d\n```\n\n## 🤝 Contributing\n\nContributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/stjudecloud/oliver/issues). You can also take a look at the [contributing guide][contributing-md].\n\n## 📝 License\n\nCopyright © 2020 [St. Jude Cloud Team](https://github.com/stjudecloud).<br />\nThis project is [MIT][license-md] licensed.\n\n[conda-install]: https://docs.anaconda.com/anaconda/install/\n[conda-forge-setup]: https://conda-forge.org/docs/user/introduction.html#how-can-i-install-packages-from-conda-forge\n[contributing-md]: https://github.com/stjudecloud/oliver/blob/master/CONTRIBUTING.md\n[license-md]: https://github.com/stjudecloud/oliver/blob/master/LICENSE.md',
    'author': 'Clay Mcleod',
    'author_email': 'clay.mcleod@STJUDE.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://stjudecloud.github.io/oliver/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.7,<4.0.0',
}


setup(**setup_kwargs)
