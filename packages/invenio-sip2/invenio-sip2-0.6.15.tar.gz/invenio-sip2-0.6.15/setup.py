# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['invenio_sip2',
 'invenio_sip2.actions',
 'invenio_sip2.handlers',
 'invenio_sip2.records',
 'invenio_sip2.views']

package_data = \
{'': ['*'],
 'invenio_sip2': ['templates/invenio_sip2/*',
                  'translations/*',
                  'translations/de/LC_MESSAGES/*',
                  'translations/en/LC_MESSAGES/*',
                  'translations/es/LC_MESSAGES/*',
                  'translations/fr/LC_MESSAGES/*',
                  'translations/it/LC_MESSAGES/*',
                  'translations/nl/LC_MESSAGES/*']}

install_requires = \
['invenio-access>=1.3.1',
 'invenio-base>=1.2.3',
 'jsonpickle>=1.2',
 'mock>=4.0.3,<5.0.0',
 'psutil>=5.9.0,<6.0.0',
 'pycountry>=19.7.15',
 'pytest-mock>=3.7.0,<4.0.0',
 'python-dateutil>=2.8.2,<3.0.0']

entry_points = \
{'flask.commands': ['selfcheck = invenio_sip2.cli:selfcheck'],
 'invenio_base.api_apps': ['invenio_sip2 = invenio_sip2:InvenioSIP2'],
 'invenio_base.api_blueprints': ['invenio_sip2 = '
                                 'invenio_sip2.views.rest:api_blueprint'],
 'invenio_base.apps': ['invenio_sip2 = invenio_sip2:InvenioSIP2'],
 'invenio_base.blueprints': ['invenio_sip2 = '
                             'invenio_sip2.views.views:blueprint']}

setup_kwargs = {
    'name': 'invenio-sip2',
    'version': '0.6.15',
    'description': 'Invenio module that add a SIP2 communication for library self-check service',
    'long_description': '..\n    INVENIO-SIP2\n    Copyright (C) 2020 UCLouvain\n\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU Affero General Public License as published by\n    the Free Software Foundation, version 3 of the License.\n\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\n    GNU Affero General Public License for more details.\n\n    You should have received a copy of the GNU Affero General Public License\n    along with this program. If not, see <http://www.gnu.org/licenses/>.\n\n==============\n Invenio-SIP2\n==============\n\n.. image:: https://img.shields.io/travis/inveniosoftware-contrib/invenio-sip2.svg\n        :target: https://travis-ci.org/inveniosoftware-contrib/invenio-sip2\n\n.. image:: https://img.shields.io/coveralls/inveniosoftware-contrib/invenio-sip2.svg\n        :target: https://coveralls.io/github/inveniosoftware-contrib/invenio-sip2\n\n.. image:: https://img.shields.io/github/tag/inveniosoftware-contrib/invenio-sip2.svg\n        :target: https://github.com/inveniosoftware-contrib/invenio-sip2/releases\n\n.. image:: https://img.shields.io/github/license/inveniosoftware-contrib/invenio-sip2.svg\n        :target: https://github.com/inveniosoftware-contrib/invenio-sip2/blob/master/LICENSE\n\nInvenio module that add a SIP2 communication for library self-check service\n\nThis project is in work in progress. Some features may not yet be implemented.\n\nFurther documentation is available on\nhttps://invenio-sip2.readthedocs.io/\n\nImplemented SIP2 Features\n=========================\n- Patron Information\n- Item Information\n- Checkout\n- Checkin\n- Renew\n',
    'author': 'Laurent Dubois',
    'author_email': 'laurent.dubois@uclouvain.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/inveniosoftware-contrib/invenio-sip2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
