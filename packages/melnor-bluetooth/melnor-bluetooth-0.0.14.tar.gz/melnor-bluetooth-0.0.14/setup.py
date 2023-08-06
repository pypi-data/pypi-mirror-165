# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['melnor_bluetooth', 'melnor_bluetooth.parser', 'melnor_bluetooth.utils']

package_data = \
{'': ['*']}

install_requires = \
['aioconsole>=0.4.1,<0.5.0',
 'bleak-retry-connector>=1.11.0,<2.0.0',
 'bleak>=0.15.1,<0.16.0',
 'tzdata>=2022.1,<2023.0',
 'tzlocal>=4.1,<5.0']

setup_kwargs = {
    'name': 'melnor-bluetooth',
    'version': '0.0.14',
    'description': 'A small python library for discovery and interacting with Melnor, Eden, etc Bluetooth water timers.',
    'long_description': '# Melnor Bluetooth\n\n![PyPI](https://img.shields.io/pypi/v/melnor-bluetooth?style=flat-square) ![Codecov branch](https://img.shields.io/codecov/c/github/vanstinator/melnor-bluetooth/main?style=flat-square) ![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/vanstinator/melnor-bluetooth/Build%20and%20Release/main?style=flat-square)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/melnor-bluetooth?style=flat-square)\n\nMelnor Bluetooth is a reverse engineered implementation of the Bluetooth protocol for all "smart" bluetooth-enabled watering valves under the Melnor, EcoAquastar, Eden, and other brands.\n\nThe library _should_ run on MacOS, Linux, or Windows. It\'s primarily developed on MacOS and other platforms likely have bugs. PRs and tests are welcome to improve quality across all platforms.\n\n\n### Getting Started\n\n#### CLI\nA simple CLI has been provided for basic debugging purposes. It\'s not intended for any real use and isn\'t suitable for running a valve in the real world.\n\nThis project uses poetry for dependency management and building. Running this project locally is as simple as the following steps:\n\n1. Clone the repository\n1. `poetry install`\n1. `poetry run cli.py`\n\n\nThe python API has been designed to be as easy to use as possible. A few examples are provided below:\n\n#### Read battery state\n```python\nimport asyncio\n\nfrom bleak import BleakScanner  # type: ignore - bleak has bad export types\n\nfrom melnor_bluetooth.device import Device\n\nADDRESS = "00:00:00:00:00"  # fill with your device mac address\n\n\nasync def main():\n\n    ble_device = await BleakScanner.find_device_by_address(ADDRESS)\n    if ble_device is not None:\n        device = Device(ble_device)\n        await device.connect()\n        await device.fetch_state()\n\n        print(device.battery_level)\n\n        await device.disconnect()\n\n\nasyncio.run(main())\n\n```\n\n#### Turn on a zone\n```python\nimport asyncio\n\nfrom bleak import BleakScanner  # type: ignore - bleak has bad export types\n\nfrom melnor_bluetooth.device import Device\n\naddress = "00:00:00:00:00"  # fill with your device mac address\n\n\nasync def main():\n    ble_device = await BleakScanner.find_device_by_address(ADDRESS)\n    if ble_device is not None:\n        device = Device(ble_device)\n        await device.connect()\n        await device.fetch_state()\n\n        device.zone1.is_watering = True\n\n        await device.push_state()\n        await device.disconnect()\n\n\nasyncio.run(main())\n```\n',
    'author': 'Justin Vanderhooft',
    'author_email': 'justinvdhooft@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
