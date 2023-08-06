# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['systemstat']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['gridstat3 = systemstat.gridstat3:cli',
                     'gridstat4 = systemstat.gridstat4:cli',
                     'sutstat = systemstat.sutstat:cli']}

setup_kwargs = {
    'name': 'systemstat',
    'version': '0.0.1',
    'description': '',
    'long_description': "# systemstat\nuse http requests to check the status of a system\n\n## Installation\n\n```bash\npip install systemstat\n```\n\nOr from this repo:\n```bash\npip install git+https://github.com/dskard/systemstat.git\n```\n\n## Example Usage:\n\nUse `gridstat3` to check if a Selenium Grid 3 has nodes attached and is ready to accept requests\n```bash\n$ gridstat3 --wait 4 --url http://localhost:4444 --verbose --stdout\n\n2022-08-21 18:07:06,714 starting gridstat3\n2022-08-21 18:07:06,714 command line options: ['--wait', '4', '--url', 'http://localhost:4444', '--verbose', '--stdout']\n2022-08-21 18:07:06,714 checking status of http://localhost:4444\n2022-08-21 18:07:06,714 starting at 2022-08-21 18:07:06.714839\n2022-08-21 18:07:06,714 ending at 2022-08-21 18:07:10.714839\n2022-08-21 18:07:06,721 hub is up at http://localhost:4444/grid/api/hub\n2022-08-21 18:07:06,721 2 of 2 nodes are attached\n2022-08-21 18:07:06,721 all nodes are attached\n2022-08-21 18:07:06,721 2 of 2 nodes are ready\n2022-08-21 18:07:06,721 all nodes are ready\n```\n\nUse `gridstat4` to check if a Selenium Grid 4 has nodes attached and is ready to accept requests\n```bash\n$ gridstat4 --wait 4 --url http://localhost:4444 --verbose --stdout\n\n2022-08-21 18:48:47,497 starting gridstat4\n2022-08-21 18:48:47,497 command line options: ['--wait', '4', '--url', 'http://localhost:4444', '--verbose', '--stdout']\n2022-08-21 18:48:47,497 checking status of http://localhost:4444\n2022-08-21 18:48:47,497 starting at 2022-08-21 18:48:47.497451\n2022-08-21 18:48:47,497 ending at 2022-08-21 18:48:51.497451\n2022-08-21 18:48:47,545 hub is up at http://localhost:4444/wd/hub/status\n2022-08-21 18:48:47,545 all nodes are ready\n```\n\nUse `sutstat` to check if a system is listening on port `4444`\n```bash\n$ sutstat --wait 4 --url http://localhost:4444 --verbose --stdout\n\n2022-08-21 18:08:25,344 starting sutstat\n2022-08-21 18:08:25,344 command line options: ['--wait', '4', '--url', 'http://localhost:4444', '--verbose', '--stdout']\n2022-08-21 18:08:25,345 checking status of http://localhost:4444\n2022-08-21 18:08:25,345 starting at 2022-08-21 18:08:25.345155\n2022-08-21 18:08:25,345 ending at 2022-08-21 18:08:29.345155\n2022-08-21 18:08:25,359 System under test is up at http://localhost:4444\n```\n\n## Development\n\nCreating a Python virtual environment:\n```bash\nmake pyenv\n```\n\nInstalling the development dependencies and current version of the library:\n```bash\nmake install\n```\n\nRunning the test cases:\n```bash\nmake test\n```\n\nRunning the command line tools through the development environment:\n```bash\npoetry run gridstat3 --wait 4 --url http://localhost:4444 --verbose --stdout\npoetry run gridstat4 --wait 4 --url http://localhost:4444 --verbose --stdout\npoetry run sutstat --wait 4 --url http://localhost:8080 --verbose --stdout\n```\n\nClean logs and Python cache files\n```bash\nmake clean\n```\n",
    'author': 'dskard',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://github.com/dskard/systemstat',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
