# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cloudist']

package_data = \
{'': ['*']}

install_requires = \
['meadowrun>=0.2.4,<0.3.0', 'pytest>=7.1.2,<8.0.0']

entry_points = \
{'pytest11': ['cloudist = cloudist.plugin']}

setup_kwargs = {
    'name': 'pytest-cloudist',
    'version': '0.1.0a1',
    'description': 'Distribute tests to cloud machines without fuss',
    'long_description': "# pytest-cloudist\n\npytest-cloudist is a pytest plugin to that distributes your tests to AWS EC2 machines with a minimum of fuss. It is a thin wrapper around [Meadowrun](https://meadowrun.io), which does the heavy lifting of starting EC2 instances and synchronizing environment and code.\n\n## Installation\n\nSimply pip install alongside pytest:\n\n```\npython -m pip install pytest-cloudist\n```\n\nThat makes the following command line arguments on `pytest` available:\n\n```\nDistributed testing in the cloud using Meadowrun:\n  --cloudist={test,file,no}\n                        Set mode for distributing tests to workers.\n                        test: send each test to a worker separately.\n                        file: send each test file to a worker separately.\n                        (default) no: run tests inprocess, don't distribute.\n  --cd-tasks-per-worker-target=tasks_per_worker_target\n                        The number of tasks to target per worker. This number determines whether individual tests or files are grouped and sent as a chunk to the test worker. Chunking is normally more efficient, but may affect load balancing and worsen the effect of stragglers.\n  --cd-num-workers=num_workers\n                        Number of workers to use for distributed testing.\n  --cd-cpu-per-worker=logical_cpu_per_worker\n                        The number of logical CPUs needed per worker.\n  --cd-memory-per-worker=memory_gb_per_worker\n                        The amount of memory (in GiB) needed per worker.\n  --cd-interrupt-prob=INTERRUPTION_PROBABILITY_THRESHOLD\n                        The estimated probability that spot instances are interrupted by AWS. Set to 0 for on-demand instances, which will be up to 10x more expensive.\n  --cd-extra-files=EXTRA_FILES\n                        Extra files to copy as to the remote machines, if needed. .py files on sys.path are copied automatically.\n  --cd-init-command=INIT_COMMAND\n                        Initialization command to run once per worker\n```\n\n## Usage\n\nBy default, pytest-cloudist is not activated, i.e. your tests run locally as normal. To enable pytest-cloudist, pass either `--cloudist test` or `--cloudist file` with any other options.\n\n## Credits\n\nThe code and approach of pytest-cloudist, in terms of pytest integration, are heavily based on the code for [pytest-xdist](https://github.com/pytest-dev/pytest-xdist), and as a result it is also licensed as MIT.\n\n",
    'author': 'Kurt Schelfthout',
    'author_email': 'kurt.schelfthout@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kurtschelfthout/pytest-cloudist',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
