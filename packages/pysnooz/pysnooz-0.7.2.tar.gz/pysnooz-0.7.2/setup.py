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
    'version': '0.7.2',
    'description': 'Control SNOOZ white noise machines.',
    'long_description': '# PySnooz\n\n<p align="center">\n  <img src="header.png" alt="Python Language + Bleak API + SNOOZ White Noise Machine" />\n</p>\n\n<p>\n  <a href="https://github.com/AustinBrunkhorst/pysnooz/actions?query=workflow%3ACI">\n    <img src="https://img.shields.io/github/workflow/status/AustinBrunkhorst/pysnooz/CI/main?label=build&logo=github&style=flat&colorA=000000&colorB=000000" alt="CI Status" >\n  </a>\n  <a href="https://codecov.io/gh/AustinBrunkhorst/pysnooz">\n    <img src="https://img.shields.io/codecov/c/github/AustinBrunkhorst/pysnooz.svg?logo=codecov&logoColor=fff&style=flat&colorA=000000&colorB=000000" alt="Test coverage percentage">\n  </a>\n  <a href="https://pypi.org/project/pysnooz/">\n    <img src="https://img.shields.io/pypi/v/pysnooz.svg?logo=python&logoColor=fff&style=flat&colorA=000000&colorB=000000" alt="PyPI Version">\n  </a>\n</p>\n\nControl SNOOZ white noise machines with Bluetooth.\n\n## Installation\n\nInstall this via pip (or your favourite package manager):\n\n`pip install pysnooz`\n\n## Usage\n\n```python\nimport asyncio\nfrom datetime import timedelta\nfrom bleak.backends.client import BLEDevice\nfrom pysnooz.device import SnoozDevice\nfrom pysnooz.commands import SnoozCommandResultStatus, turn_on, turn_off, set_volume\n\n# found with discovery\nble_device = BLEDevice(...)\ntoken = "deadbeef"\n\ndevice = SnoozDevice(ble_device, token, asyncio.get_event_loop())\n\n# optionally specify a volume to set before turning on\nawait device.async_execute_command(turn_on(volume=100))\n\n# you can transition volume by specifying a duration\nawait device.async_execute_command(turn_off(duration=timedelta(seconds=10)))\n\n# you can also set the volume directly\nawait device.async_execute_command(set_volume(50))\n\n# view the result of a command execution\nresult = await device.async_execute_command(turn_on())\nassert result.status == SnoozCommandResultStatus.SUCCESS\nresult.duration # how long the command took to complete\n```\n\n## Contributors ✨\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- prettier-ignore-start -->\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n<!-- prettier-ignore-end -->\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!\n\n## Credits\n\nThis package was created with\n[Cookiecutter](https://github.com/audreyr/cookiecutter) and the\n[browniebroke/cookiecutter-pypackage](https://github.com/browniebroke/cookiecutter-pypackage)\nproject template.\n',
    'author': 'Austin Brunkhorst',
    'author_email': 'pysnooz@alb.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AustinBrunkhorst/pysnooz',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
