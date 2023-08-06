# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bdvr']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.3,<2.0.0',
 'quo>=2022.8.2,<2023.0.0',
 'universal-startfile>=0.1.3,<0.2.0']

entry_points = \
{'console_scripts': ['bdvr = bdvr:main']}

setup_kwargs = {
    'name': 'bdvr',
    'version': '0.7.0',
    'description': "customized report generated from set of blackduck reports that gives 'color coded vulnerabilities', and 'source paths' including 'direct' and 'indirect dependencies' details all in one report",
    'long_description': '# bdvr, an Customized Blackduck_Vulnerability_report\n\n# Use case:\n\nProject stakeholders want to know which files are affected with vulnerabilities after a Blackduck HUB scan.\n\n# Drawbacks:\n\nThe current blackduck generates multiple reports. To fulfill above requirement once has to refer 2 different reports to really able to trace the source files affected.\n\n# Features\n\n1. Produces customized report where we can see vulnerability, OSS name, affected source path details all in one report\n2. Color coded\n\n   low risk = no color\n\n   medium risk = Yellow\n\n   High risk = Red\n\n3. Omits all other files which has no vulnerabilities.\n\n### Prerequiites:\n\nGo to Your Blackduck Project > Generate \'Create Version detail report\' > checkbox Source and Vulnerabilities checked.\n\n## How to install\n\n```sh\n\npip install bdvr\n```\n\n## Command to run\n\n```sh\n\n\nusage:bdvr [-h] -p P [-o]\n\noptions:\n  -h, --help  show this help message and exit\n  -p P        Blackduck report folder is ex: D:\\BD_REPORT\\PROJECT_DATETIMESTAMP.zip\n  -o          (Optional) To automatically open the file\n\nbdvr -p Blackduck_generated_reports.zip\n\n#To automatically open the file add -o option\nbdvr -p Blackduck_generated_reports.zip -o\n\n```\n\n## Dependenceis\n\n```sh\n\nThanks to all authors. As this library uses below modules\npandas = "^1.4.3"\nquo = "^2022.8.2"\nuniversal-startfile = "^0.1.3"\n\n```\n\n## Issues\n\nPlease send your bugs to dineshr93@gmail.com\n',
    'author': 'dineshr93gmail.com',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
