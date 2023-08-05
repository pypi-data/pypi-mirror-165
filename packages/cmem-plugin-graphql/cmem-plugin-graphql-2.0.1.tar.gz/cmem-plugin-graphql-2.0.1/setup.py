# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cmem_plugin_graphql', 'cmem_plugin_graphql.workflow']

package_data = \
{'': ['*']}

install_requires = \
['cmem-plugin-base>=2.1.0,<3.0.0',
 'gql[all]>=3.2.0,<4.0.0',
 'validators>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'cmem-plugin-graphql',
    'version': '2.0.1',
    'description': 'Send a query to GraphQL endpoint and save the results in a JSON dataset.',
    'long_description': '# cmem-plugin-graphql\n\na CMEM Plugin to query GraphQL APIs and write the response to dataset of type JSON.\nIn the current release we are supporting only endpoints without authentication.\n',
    'author': 'Sai Praneeth M',
    'author_email': 'saipraneeth@aarth.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eccenca/cmem-plugin-graphql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
