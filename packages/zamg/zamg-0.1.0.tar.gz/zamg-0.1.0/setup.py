# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['zamg']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.0']

setup_kwargs = {
    'name': 'zamg',
    'version': '0.1.0',
    'description': 'Asynchronous Python client for ZAMG weather data.',
    'long_description': '# python-zamg\n\n[![GitHub Release][releases-shield]][releases]\n[![GitHub Activity][commits-shield]][commits]\n[![License][license-shield]](LICENSE)\n\n[![pre-commit][pre-commit-shield]][pre-commit]\n[![Black][black-shield]][black]\n\n[![Project Maintenance][maintenance-shield]][user_profile]\n\nPython library to read 10 min weather data from ZAMG\n\n## About\n\nThis package allows you to read the weather data from weather stations of ZAMG weather service.\nZAMG is the Zentralanstalt für Meteorologie und Geodynamik in Austria.\n\n## Installation\n\n```bash\npip install zamg\n```\n\n## Usage\n\n```python\nimport asyncio\n\nimport src.zamg.zamg\n\nasync def main():\n    """Sample of getting data for the closest station to the given coordinates"""\n    async with src.zamg.zamg.ZamgData() as zamg:\n        data = await zamg.closest_station(46.99, 15.499)\n        zamg.set_default_station(data)\n        print("closest_station = " + str(zamg.get_station_name) + " / " + str(data))\n        await zamg.update()\n        print(\n            "---------- Weather for station %s (%s)",\n            str(zamg.get_data("name", data)),\n            str(data),\n        )\n        for param in zamg.get_all_parameters():\n            print(\n                str(zamg.get_data(parameter=param, data_type="name"))\n                + " -> "\n                + str(zamg.get_data(parameter=param))\n                + " "\n                + str(zamg.get_data(parameter=param, data_type="unit"))\n            )\n        print("last update: %s", zamg.last_update)\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n\n## Contributions are welcome!\n\nIf you want to contribute to this please read the [Contribution guidelines](https://github.com/killer0071234/python-zamg/blob/master/CONTRIBUTING.md)\n\n## Credits\n\nCode template to read dataset API was mainly taken from [@LuisTheOne](https://github.com/LuisThe0ne)\'s [zamg-api-cli-client][zamg_api_cli_client]\n\n---\n\n[black]: https://github.com/psf/black\n[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge\n[commits-shield]: https://img.shields.io/github/commit-activity/y/killer0071234/python-zamg.svg?style=for-the-badge\n[commits]: https://github.com/killer0071234/python-zamg/commits/main\n[license-shield]: https://img.shields.io/github/license/killer0071234/python-zamg.svg?style=for-the-badge\n[maintenance-shield]: https://img.shields.io/badge/maintainer-@killer0071234-blue.svg?style=for-the-badge\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge\n[releases-shield]: https://img.shields.io/github/release/killer0071234/python-zamg.svg?style=for-the-badge\n[releases]: https://github.com/killer0071234/python-zamg/releases\n[user_profile]: https://github.com/killer0071234\n[zamg_api_cli_client]: https://github.com/LuisThe0ne/zamg-api-cli-client\n',
    'author': 'Daniel Gangl',
    'author_email': 'killer007@gmx.at',
    'maintainer': 'Daniel Gangl',
    'maintainer_email': 'killer007@gmx.at',
    'url': 'https://github.com/killer0071234/python-zamg',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
