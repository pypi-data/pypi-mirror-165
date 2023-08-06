# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wafflesbot']

package_data = \
{'': ['*']}

install_requires = \
['jmapc>=0.2.0,<0.3.0', 'replyowl>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['wafflesbot = wafflesbot.main:main']}

setup_kwargs = {
    'name': 'wafflesbot',
    'version': '0.1.2',
    'description': 'Tech recruiter auto reply bot using JMAP',
    'long_description': '# wafflesbot: Email auto reply bot for [JMAP][jmap] mailboxes\n\n[![PyPI](https://img.shields.io/pypi/v/wafflesbot)][pypi]\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wafflesbot)][pypi]\n[![Build](https://img.shields.io/github/checks-status/smkent/waffles/main?label=build)][gh-actions]\n[![codecov](https://codecov.io/gh/smkent/waffles/branch/main/graph/badge.svg)][codecov]\n[![GitHub stars](https://img.shields.io/github/stars/smkent/waffles?style=social)][repo]\n\n[![wafflesbot][logo]](#)\n\nwafflesbot sends form replies to unreplied emails in a [JMAP][jmap] mailbox\n(such as [Fastmail][fastmail]).\n\nwafflesbot excels at automatically asking tech recruiters for compensation\ninformation.\n\nBuilt on:\n* JMAP client: [jmapc][jmapc]\n* Quoted email reply assembly: [replyowl][replyowl]\n\n## Installation\n\n[wafflesbot is available on PyPI][pypi]:\n\n```\npip install wafflesbot\n```\n\n## Usage\n\nwafflesbot provides the `waffles` command, which can either:\n1. Run as a service and reply to emails received via [JMAP server\n   events][jmap-event-source] (the default)\n2. Run as a script to examine recent emails (such as interactively or via a\n   cronjob)\n\nEnvironment variables:\n* `JMAP_HOST`: JMAP server hostname\n* `JMAP_API_TOKEN`: JMAP account API token\n\nRequired arguments:\n* `-m/--mailbox`: Name of the folder to process\n* `-r/--reply-content`: Path to file with an HTML reply message\n\nOptional arguments:\n* `-d/--debug`: Enable debug logging\n* `-l/--limit`: Maximum number of emails replies to send (only valid with\n  `-s/--script`)\n* `-n/--days`: Only process email received this many days ago or newer (only\n  valid with `-s/--script`)\n* `-p/--pretend`: Print messages to standard output instead of sending email\n* `-s/--script`: Set to run as a script instead of an event-driven service\n\n### Invocation examples\n\nListen for new emails, and reply to unreplied messages that appear in the\n"Recruiters" folder with the message in `my-reply.html`:\n\n```py\nJMAP_HOST=jmap.example.com \\\nJMAP_API_TOKEN=ness__pk_fire \\\nwaffles \\\n    --mailbox "Recruiters" \\\n    --reply-content my-reply.html\n```\n\nRun as a script and reply to unreplied messages in the "Recruiters" folder with\nthe message in `my-reply.html`:\n\n```py\nJMAP_HOST=jmap.example.com \\\nJMAP_API_TOKEN=ness__pk_fire \\\nwaffles \\\n    --script \\\n    --mailbox "Recruiters" \\\n    --reply-content my-reply.html\n```\n\n## Development\n\nPrerequisites: [Poetry][poetry]\n\n* Setup: `poetry install`\n* Run all tests: `poetry run poe test`\n* Fix linting errors: `poetry run poe lint`\n\n---\n\nCreated from [smkent/cookie-python][cookie-python] using\n[cookiecutter][cookiecutter]\n\n[codecov]: https://codecov.io/gh/smkent/waffles\n[cookie-python]: https://github.com/smkent/cookie-python\n[cookiecutter]: https://github.com/cookiecutter/cookiecutter\n[fastmail]: https://fastmail.com\n[gh-actions]: https://github.com/smkent/waffles/actions?query=branch%3Amain\n[jmap]: https://jmap.io\n[jmap-event-source]: https://jmap.io/spec-core.html#event-source\n[jmapc]: https://github.com/smkent/jmapc\n[logo]: https://raw.github.com/smkent/waffles/main/img/waffles.png\n[poetry]: https://python-poetry.org/docs/#installation\n[pypi]: https://pypi.org/project/wafflesbot/\n[replyowl]: https://github.com/smkent/replyowl\n[repo]: https://github.com/smkent/waffles\n',
    'author': 'Stephen Kent',
    'author_email': 'smkent@smkent.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/smkent/waffles',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
