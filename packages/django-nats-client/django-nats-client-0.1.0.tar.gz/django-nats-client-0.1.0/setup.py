# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nats_client', 'nats_client.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['django', 'nats-py>=2.1']

setup_kwargs = {
    'name': 'django-nats-client',
    'version': '0.1.0',
    'description': '',
    'long_description': "# Django NATS\n\n[![GitHub](https://img.shields.io/github/license/C0D1UM/django-nats-client)](https://github.com/C0D1UM/django-nats-client/blob/main/LICENSE)\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/C0D1UM/django-nats-client/CI)](https://github.com/C0D1UM/django-nats-client/actions/workflows/ci.yml)\n[![codecov](https://codecov.io/gh/C0D1UM/django-nats-client/branch/main/graph/badge.svg?token=PN19DJ3SDF)](https://codecov.io/gh/C0D1UM/django-nats-client)\n[![PyPI](https://img.shields.io/pypi/v/django-nats-client)](https://pypi.org/project/django-nats-client/)  \n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-nats-client)](https://github.com/C0D1UM/django-nats-client)\n[![Django Version](https://img.shields.io/badge/django-3.1%20%7C%203.2%20%7C%204.0-blue)](https://github.com/C0D1UM/django-nats-client)\n\n## Features\n\n- Wrapper of NATS's [nats-py](https://github.com/nats-io/nats.py)\n- Django management command to listen for incoming NATS messages\n- Automatically serialize/deserialize message from/to JSON format\n- Easy-to-call method for sending NATS messages\n\n## Installation\n\n```bash\npip install django-nats-client\n```\n\n## Setup\n\n1. Add `nats_client` into `INSTALLED_APPS`\n\n   ```python\n   # settings.py\n\n   INSTALLED_APPS = [\n       ...\n       'nats_client',\n   ]\n   ```\n\n3. Put NATS connection configuration in settings\n\n   ```python\n   # settings.py\n\n   NATS_OPTIONS = {\n       'servers': ['nats://localhost:4222'],\n       'max_reconnect_attempts': 2,\n       'connect_timeout': 1,\n       ...\n   }\n   NATS_DEFAULT_SUBJECT = 'default'\n   ```\n\n## Usage\n\n### Listen for messages\n\n1. Create a new callback method and register\n\n   ```python\n   # common/nats_callback.py\n\n   import nats_client\n\n   @nats_client.register\n   def get_year_from_date(date: str):\n       return date.year\n\n   # custom subject\n   @nats_client.register('subject')\n   def current_time():\n       return datetime.datetime.now().strftime('%H:%M')\n\n   # custom method name\n   @nats_client.register('subject', 'get_current_time')\n   def current_time():\n       return datetime.datetime.now().strftime('%H:%M')\n   ```\n\n2. Run listener management command\n\n   ```bash\n   python manage.py nats_listener\n   ```\n\n### Sending message\n\n```python\nimport nats_client\n\narg = 'some arg'\nnats_client.send(\n    'subject_name',\n    'method_name',\n    arg,\n    keyword_arg=1,\n    another_keyword_arg=2,\n)\n```\n\nExamples\n\n```python\nimport nats_client\n\nyear = nats_client.send('default', 'get_year_from_date', datetime.date(2022, 1, 1))  # 2022\ncurrent_time = nats_client.send('default', 'get_current_time')  # 12:11\n```\n\n## Settings\n\n| Key                    | Required | Default   | Description                                       |\n|------------------------|----------|-----------|---------------------------------------------------|\n| `NATS_OPTIONS`         | Yes      |           | Configuration to be passed in `nats.connect()`    |\n| `NATS_DEFAULT_SUBJECT` | No       | 'default' | Default subject for registering callback function |\n\n## Development\n\n### Requirements\n\n- Docker\n- Python\n- Poetry\n\n### Linting\n\n```bash\nmake lint\n```\n\n### Testing\n\n```bash\nmake test\n```\n\n### Fix Formatting\n\n```bash\nmake yapf\n```\n",
    'author': 'CODIUM',
    'author_email': 'support@codium.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/C0D1UM/django-nats-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
