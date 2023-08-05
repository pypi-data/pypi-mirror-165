# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['merakitools']

package_data = \
{'': ['*']}

install_requires = \
['meraki>=1.22.1,<2.0.0', 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['merakitools = merakitools.main:app']}

setup_kwargs = {
    'name': 'merakitools',
    'version': '0.1.11',
    'description': 'CLI tools for managing Meraki networks based on Typer',
    'long_description': '# merakitools\n[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/billyzoellers/merakitools)\n[![CI](https://github.com/billyzoellers/merakitools/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/billyzoellers/merakitools/actions/workflows/ci.yml)\n[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)\n[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)\n\nCLI tools for managing Meraki networks based on [Typer](https://typer.tiangolo.com/).\n\nmerakitools provides CLI based to monitoring and configuration tools available through the Meraki\nDashboard API. It was designed to help with bulk configuration creation and migrations to the Meraki platform.\n\n## Installation\nInstall with `pip` or your favorite PyPi package mananger.\n```\npip install merakitools\n```\n\nSet enviornment variable `MERAKI_DASHBOARD_API_KEY` to your Meraki API key\n\nThen try a command.\n```\nmerakitools orgs list\n```\n\n## Example Commands\nList Meraki Networks in an organization\n```\nmerakitools networks list <YourOrgName>\n```\n\nList Meraki MR devices in a network\n```\nmerakitools devices list <YourOrgName> <YourNetworkName> --type MR\\\n```\n\nCreate a static NAT entry on a Meraki MX security appliance\n```\nmerakitools mx create-staticnat <YourOrgName> <YourNetworkName> --nat <name>!<publicIP>!<privateIP> --port tcp!636!192.0.2.1/32 --port tcp!8080!any\n```\n\n***For more commands check out the [command documentation](COMMANDS.md).***\n\n## Testing\nFor a free and easy to use testing enviornment, use the Cisco DevNet Sandbox [Meraki](https://developer.cisco.com/docs/sandbox/#!networking/meraki).\n*Note: The sandbox is read-only, so you will not be able to test commands that write data to the Dashboard*\n\n## License\nCopyright (C) 2021  Billy Zoellers\n\nThis program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.\nYou should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.\n',
    'author': 'Billy Zoellers',
    'author_email': 'billy.zoellers@mac.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
