# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_html_report_merger']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0']

entry_points = \
{'console_scripts': ['pytest-html-report-merger = '
                     'pytest_html_report_merger.__main__:cli']}

setup_kwargs = {
    'name': 'pytest-html-report-merger',
    'version': '0.0.1',
    'description': '',
    'long_description': 'None',
    'author': 'dskard',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
