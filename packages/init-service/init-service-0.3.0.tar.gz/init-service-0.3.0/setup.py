# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['init_service']

package_data = \
{'': ['*'],
 'init_service': ['templates/library/*',
                  'templates/library/project/*',
                  'templates/library/src/main/scala/uk/gov/hmrc/hello/*',
                  'templates/library/src/test/scala/uk/gov/hmrc/hello/*',
                  'templates/service/*',
                  'templates/service/app/assets/stylesheets/*',
                  'templates/service/app/config/*',
                  'templates/service/app/controllers/*',
                  'templates/service/app/views/*',
                  'templates/service/conf/*',
                  'templates/service/it/*',
                  'templates/service/project/*',
                  'templates/service/template/*',
                  'templates/service/test/config/*',
                  'templates/service/test/controllers/*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['init-service = init_service:run_cli']}

setup_kwargs = {
    'name': 'init-service',
    'version': '0.3.0',
    'description': 'A templating tool for HMRC MDTP repositories',
    'long_description': 'None',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
