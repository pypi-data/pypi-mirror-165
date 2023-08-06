# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['work_components', 'work_components.dao']

package_data = \
{'': ['*']}

modules = \
['work']
entry_points = \
{'console_scripts': ['work = work:cli']}

setup_kwargs = {
    'name': 'work-time-log',
    'version': '0.100.1',
    'description': 'Manual time tracking via a CLI that works similarly to git.',
    'long_description': '# Work time log\n\n`work` allows manual time tracking with an interaction model inspired by `git`:\n\n1. Text files are used for storage. This makes it easy to track the log with `git`.\n2. The tool does not run continously and instead only modifies the `work status` on disk.\n3. The `work status` is global, meaning any terminal can be used to check or update it.\n4. Checksums are used to verify that the log was not modified by another tool.\n\n## Features\n\n- Time tracking\n  + Time track while working and (optionally) add a category and message.\n  + Retroactively add and modify any entry.\n- Analyses\n  + Calculate and check the hours worked over arbitrary periods.\n  + List tracked entries by date or category with optional filters.\n- Overtime and undertime\n  + Configure "expected hours" and view the accumulated over-/undertime.\n  + (Optionally) store vacations or holidays.\n- Export entries as CSV.\n\n## Read More\n\nFor more information, including examples and the release history, check the [website](https://vauhoch.zett.cc/work/).\n',
    'author': 'Valentin',
    'author_email': 'noemail@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://vauhoch.zett.cc/work/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
