# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cvetrends', 'cvetrends.lib']

package_data = \
{'': ['*']}

install_requires = \
['click',
 'click-config-file',
 'notifiers>=1.3.3,<2.0.0',
 'python-box>=6.0.2,<7.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich-click>=1.5.2,<2.0.0',
 'rich>=12.4.1,<13.0.0']

entry_points = \
{'console_scripts': ['cvet = cvetrends.__main__:main']}

setup_kwargs = {
    'name': 'cvetrends',
    'version': '0.0.1',
    'description': 'cvet is a Python utility for pulling actionable vulnerabilities from cvetrends.com',
    'long_description': '<div align="center">\n \n# cvet\n\n  <img width="1030" alt="02082022_12 53-000469" src="https://user-images.githubusercontent.com/8538866/182379468-62be89b8-a4d3-4232-987a-8576906e0a63.png">\n\n <br><br>\n \ncvet is a Python utility for pulling actionable vulnerabilities from [cvetrends.com](https://cvetrends.com/).\n\nFind out more information at our [blog](https://www.sprocketsecurity.com/resources/cve-trends-command-line-tool).\n<br>\n\n[Installation](#installation) /\n[Usage](#usage)\n\n</div><br>\n\n</div>\n<br>\n\n## Installation\n\ncvet can be installed from PyPi using the following command:\n\n```\npipx install cvet\n```\n\nIf this tool is not yet availible via PyPi, you can install it directly from the repository using:\n\n```\ngit clone https://github.com/Sprocket-Security/cvetrends.git\ncd cvetrends && pip3 install .\n```\n\nFor development, clone the repository and install it locally using poetry.\n\n```\ngit clone https://github.com/Sprocket-Security/cvetrends.git && cd cvetrends\npoetry shell \npoetry install\n```\n\n<br>\n\n## Usage\n\nThe cvet help menu is shown below:\n\n```\n Usage: cvet [OPTIONS] [[day|week]]                                                                                              \n                                                                                                                                 \n cvetrends.com CLI                                                                                                               \n                                                                                                                                 \n╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ TIME_FRAME    [[day|week]]                                                                                                    │\n╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ --notify          -n   TEXT     Slack webhook to notify on run                                                                │\n│ --repo-threshold  -rt  INTEGER  Number of repos needed to show CVE. [default: 1]                                              │\n│ --help            -h            Show this message and exit.                                                                   │\n╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n```\n\ncvet can query time frames of 24 hours or 7 days using a value of `day` or `week`. The default is `day`.\n\n```\ncvet week \n```\n\nResults are returned in a pretty table format and only vulnerabilities that have more than `-rt` PoC GitHub repos published are shown. The default is 1.\n\n```\ncvet day -rt 2\n```\n\ncvet also allows you to specify a Slack webhook to notify on run using the `-n` or `--notify` flag. This is useful if you want to be notified of new vulnerabilities and run this tool on a cron.\n\n```\ncvet -n https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX -rt 2 \n```\n\nAn example Slack notification is shown below:\n\n<img width="877" alt="02082022_12 54-000470" src="https://user-images.githubusercontent.com/8538866/182379759-238c40a8-383f-4808-95c6-928eaf537f85.png">\n\n\n',
    'author': 'Nicholas',
    'author_email': 'nanastasi@sprocketsecurity.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/puzzlepeaches/cvetrends',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
