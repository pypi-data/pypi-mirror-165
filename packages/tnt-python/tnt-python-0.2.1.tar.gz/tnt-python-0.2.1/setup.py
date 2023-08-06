# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tnt_python']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0']

setup_kwargs = {
    'name': 'tnt-python',
    'version': '0.2.1',
    'description': 'Telegram notification tool',
    'long_description': '# tnt-python\n[![Dependencies](https://img.shields.io/librariesio/github/watchmanix/tnt-python)](https://pypi.org/project/tnt-python/)\n[![Version](https://img.shields.io/pypi/v/tnt-python?color=green)](https://pypi.org/project/tnt-python/)\n[![Downloads](https://pepy.tech/badge/tnt-python/month)](https://pepy.tech/project/tnt-python)\n[![Downloads](https://pepy.tech/badge/tnt-python/week)](https://pepy.tech/project/tnt-python)\n\ntnt - Telegram notification tool\n\n## Features\n\n* Sending text messages to chat\n* Sending text documents to chat\n\n\n## Installation\n\n```\npoetry add tnt-python\n```\n\nor\n\n```\npip install tnt-python\n```\n\n## Example\n\nThis code sends a message on your behalf to the chat\n\n```python\nimport os\nfrom tnt_python.data import MessageData\nfrom tnt_python.services import NotifyerService\n\n# Your API Token\ntoken = os.getenv("TG_TOKEN")\n\ndata = MessageData(\n    chat_id=os.getenv("CHAT_ID"),\n    text="Hello world"\n)\nNotifyerService().send_message(data, token)\n```\n\n## Debug\n Methods `send_message`, `send_coument` returns `ResponseType` type dataclass.\n You can output `status_code` or the entire response via `result`\n \n ```python\n\nimport os\nfrom tnt_python.data import MessageData\nfrom tnt_python.services import NotifyerService\nfrom tnt_python.types import ResponseType\n\ntoken = os.getenv("TG_TOKEN")\n\ndata = MessageData(\n    chat_id=os.getenv("CHAT_ID"),\n    text="Hello world"\n)\nresponse: ResponseType = NotifyerService().send_message(data, token)\n\n# So you can display the entire response and the response code\nprint(response.status_code, response.result)\n```',
    'author': 'axeman',
    'author_email': 'axeman.ofic@gmail.com',
    'maintainer': 'axeman',
    'maintainer_email': 'axeman.ofic@gmail.com',
    'url': 'https://github.com/watchmanix/tnt-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
