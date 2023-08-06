# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['trier']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'trier',
    'version': '1.0.2',
    'description': 'Utility wrapper to handle exceptions.',
    'long_description': '# trier\n\n> Utility wrapper class to handle exceptions.\n\n[![PyPI version](https://badge.fury.io/py/trier.svg)](https://badge.fury.io/py/trier)\n[![trier CI](https://github.com/omegatrix/trier/actions/workflows/build.yaml/badge.svg)](https://github.com/omegatrix/trier/actions/workflows/build.yaml)\n[![codecov](https://codecov.io/gh/omegatrix/trier/branch/main/graph/badge.svg?token=2M0QOSUPM0)](https://codecov.io/gh/omegatrix/trier)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/trier)\n\n## Installation\nYou can [install `trier` from PyPI](https://pypi.org/project/trier), with `pip`:\n\n```bash\npython -m pip install trier\n```\n\n## Example usage\nInstead of using `try except` block you could replace it with `trier`.\n\n```py\nfrom trier import Try\n\nerr, val = Try(lambda: 10 / 0).catch(ZeroDivisionError)\n\nif err:\n    # handle error\n\n# do stuff with `val`\n\n# Another way to handle could be\nif not err:\n  # do stuff with `val`\n```\n\nSupports multiple exceptions.\n```py\nfrom trier import Try\n\nerr, file = Try(open, file="doenot_exist.txt").catch(FileNotFoundError, OSError)\n\nif err:\n    # handle error\n\n# do stuff with `file`\n```\n\nSupports async error handling as well.\n```py\nimport asyncio\nfrom httpx import AsyncClient, HTTPStatusError, Response\nfrom trier import Try\n\ndef raise_on_4xx_5xx(response):\n    response.raise_for_status()\n\nasync def main():\n    client = AsyncClient(event_hooks={"response": [raise_on_4xx_5xx]})\n\n    # The endpoint responds with a 404 error\n    err, response = await Try(client.get, "https://run.mocky.io/v3/201f1fe6-5a3b-49c1-9df7-312951618405").async_catch(HTTPStatusError)\n\n    if err:\n        # Handle error\n\n    # do stuff with `response`\n\nasyncio.run(main())\n```\n\n## Changelog\n\nRefer to the [CHANGELOG.md](https://github.com/omegatrix/trier/blob/main/CHANGELOG.md) file.\n',
    'author': 'Arnold Anthonypillai',
    'author_email': 'arnoldbronson16@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
