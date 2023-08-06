# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['groundwork',
 'groundwork.contrib.airtable',
 'groundwork.core',
 'groundwork.core.internal',
 'groundwork.core.management.commands',
 'groundwork.core.templatetags',
 'groundwork.geo',
 'groundwork.geo.templatetags',
 'groundwork.geo.territories.uk',
 'groundwork.geo.territories.uk.internal']

package_data = \
{'': ['*'],
 'groundwork.core': ['static/*', 'static/assets/*'],
 'groundwork.geo': ['docs/*',
                    'templates/groundwork/geo/components/*',
                    'templates/groundwork/geo/examples/*']}

install_requires = \
['djangorestframework-camel-case>=1.2.0,<2.0.0',
 'djangorestframework-dataclasses>=1.0.0,<2.0.0',
 'schedule>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'groundwork-django',
    'version': '0.1.4',
    'description': 'An integrated Django and Javascript framework for people who build tools for organisers.',
    'long_description': '# Groundwork\n\nAn integrated Django and Javascript framework for people who build tools for organisers.\n\nFor more information, check out [the documentation site](https://groundwork.commonknowledge.coop/).\n\nWork on this project kindly supported by [Rosa-Luxemburg-Stiftung](https://www.rosalux.de).\n',
    'author': 'Common Knowledge',
    'author_email': 'hello@commonknowledge.coop',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://groundwork.commonknowledge.coop/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
