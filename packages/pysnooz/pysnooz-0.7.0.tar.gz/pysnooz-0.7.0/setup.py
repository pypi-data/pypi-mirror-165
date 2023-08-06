# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pysnooz']

package_data = \
{'': ['*']}

install_requires = \
['Events>=0.4,<0.5',
 'bleak-retry-connector>=1.11.0',
 'bleak>=0.15.1,<0.16.0',
 'bluetooth-sensor-state-data>=1.5.0',
 'home-assistant-bluetooth>=1.3.0',
 'sensor-state-data>=2.1.2',
 'transitions>=0.8.11,<0.9.0']

setup_kwargs = {
    'name': 'pysnooz',
    'version': '0.7.0',
    'description': 'Control SNOOZ white noise machines.',
    'long_description': '# PySnooz\n\n<p align="center">\n  <a href="https://github.com/AustinBrunkhorst/pysnooz/actions?query=workflow%3ACI">\n    <img src="https://img.shields.io/github/workflow/status/AustinBrunkhorst/pysnooz/CI/main?label=CI&logo=github&style=flat-square" alt="CI Status" >\n  </a>\n  <a href="https://codecov.io/gh/AustinBrunkhorst/pysnooz">\n    <img src="https://img.shields.io/codecov/c/github/AustinBrunkhorst/pysnooz.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">\n  </a>\n</p>\n<p align="center">\n  <a href="https://python-poetry.org/">\n    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAASCAYAAABrXO8xAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJJSURBVHgBfZLPa1NBEMe/s7tNXoxW1KJQKaUHkXhQvHgW6UHQQ09CBS/6V3hKc/AP8CqCrUcpmop3Cx48eDB4yEECjVQrlZb80CRN8t6OM/teagVxYZi38+Yz853dJbzoMV3MM8cJUcLMSUKIE8AzQ2PieZzFxEJOHMOgMQQ+dUgSAckNXhapU/NMhDSWLs1B24A8sO1xrN4NECkcAC9ASkiIJc6k5TRiUDPhnyMMdhKc+Zx19l6SgyeW76BEONY9exVQMzKExGKwwPsCzza7KGSSWRWEQhyEaDXp6ZHEr416ygbiKYOd7TEWvvcQIeusHYMJGhTwF9y7sGnSwaWyFAiyoxzqW0PM/RjghPxF2pWReAowTEXnDh0xgcLs8l2YQmOrj3N7ByiqEoH0cARs4u78WgAVkoEDIDoOi3AkcLOHU60RIg5wC4ZuTC7FaHKQm8Hq1fQuSOBvX/sodmNJSB5geaF5CPIkUeecdMxieoRO5jz9bheL6/tXjrwCyX/UYBUcjCaWHljx1xiX6z9xEjkYAzbGVnB8pvLmyXm9ep+W8CmsSHQQY77Zx1zboxAV0w7ybMhQmfqdmmw3nEp1I0Z+FGO6M8LZdoyZnuzzBdjISicKRnpxzI9fPb+0oYXsNdyi+d3h9bm9MWYHFtPeIZfLwzmFDKy1ai3p+PDls1Llz4yyFpferxjnyjJDSEy9CaCx5m2cJPerq6Xm34eTrZt3PqxYO1XOwDYZrFlH1fWnpU38Y9HRze3lj0vOujZcXKuuXm3jP+s3KbZVra7y2EAAAAAASUVORK5CYII=" alt="Poetry">\n  </a>\n  <a href="https://github.com/ambv/black">\n    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">\n  </a>\n  <a href="https://github.com/pre-commit/pre-commit">\n    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">\n  </a>\n</p>\n<p align="center">\n  <a href="https://pypi.org/project/pysnooz/">\n    <img src="https://img.shields.io/pypi/v/pysnooz.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">\n  </a>\n  <img src="https://img.shields.io/pypi/pyversions/pysnooz.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">\n  <img src="https://img.shields.io/pypi/l/pysnooz.svg?style=flat-square" alt="License">\n</p>\n\nControl SNOOZ white noise machines.\n\n## Installation\n\nInstall this via pip (or your favourite package manager):\n\n`pip install pysnooz`\n\n## Usage\n\n```python\nimport asyncio\nfrom datetime import timedelta\nfrom bleak.backends.client import BLEDevice\nfrom pysnooz.device import SnoozDevice\nfrom pysnooz.commands import SnoozCommandResultStatus, turn_on, turn_off, set_volume\n\n# found with discovery\nble_device = BLEDevice(...)\ntoken = "deadbeef"\n\ndevice = SnoozDevice(ble_device, token, asyncio.get_event_loop())\n\n# optionally specify a volume to set before turning on\nawait device.async_execute_command(turn_on(volume=100))\n\n# you can transition volume by specifying a duration\nawait device.async_execute_command(turn_off(duration=timedelta(seconds=10)))\n\n# you can also set the volume directly\nawait device.async_execute_command(set_volume(50))\n\n# view the result of a command execution\nresult = await device.async_execute_command(turn_on())\nassert result.status == SnoozCommandResultStatus.SUCCESS\nresult.duration # how long the command took to complete\n```\n\n## Contributors ✨\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- prettier-ignore-start -->\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n<!-- prettier-ignore-end -->\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!\n\n## Credits\n\nThis package was created with\n[Cookiecutter](https://github.com/audreyr/cookiecutter) and the\n[browniebroke/cookiecutter-pypackage](https://github.com/browniebroke/cookiecutter-pypackage)\nproject template.\n',
    'author': 'Austin Brunkhorst',
    'author_email': 'contact@austinbrunkhorst.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AustinBrunkhorst/pysnooz',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
