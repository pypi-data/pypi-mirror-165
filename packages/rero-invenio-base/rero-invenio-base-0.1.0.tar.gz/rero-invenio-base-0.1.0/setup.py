# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rero_invenio_base',
 'rero_invenio_base.cli',
 'rero_invenio_base.cli.es',
 'rero_invenio_base.cli.es.slm',
 'rero_invenio_base.cli.es.snapshot',
 'rero_invenio_base.modules',
 'rero_invenio_base.modules.export']

package_data = \
{'': ['*']}

install_requires = \
['Mako>=1.2.2',
 'PyYAML>=6.0,<7.0',
 'dparse>=0.5.2',
 'invenio-db>=1.0.14,<2.0.0',
 'invenio-records-rest',
 'invenio-search[elasticsearch7]>=1.4.2,<2.0.0',
 'jsonpatch>=1.32,<2.0']

entry_points = \
{'console_scripts': ['check_json = rero_invenio_base.cli.utils:check_json',
                     'check_license = '
                     'rero_invenio_base.cli.utils:check_license',
                     'rero = rero_invenio_base.cli:rero'],
 'flask.commands': ['rero = rero_invenio_base.cli:rero'],
 'invenio_base.api_blueprints': ['rero_ils_exports = '
                                 'rero_invenio_base.modules.export.views:create_blueprint_from_app'],
 'invenio_base.apps': ['rero-invenio-base-export = '
                       'rero_invenio_base.modules.export.ext:ReroInvenioBaseExportApp']}

setup_kwargs = {
    'name': 'rero-invenio-base',
    'version': '0.1.0',
    'description': 'Generic backend libraries for RERO Invenio instances.',
    'long_description': '..\n    RERO Invenio Base\n    Copyright (C) 2022 RERO.\n\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU Affero General Public License as published by\n    the Free Software Foundation, version 3 of the License.\n\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\n    GNU Affero General Public License for more details.\n\n    You should have received a copy of the GNU Affero General Public License\n    along with this program. If not, see <http://www.gnu.org/licenses/>.\n\n===================\n RERO Invenio Base\n===================\n\n.. image:: https://github.com/rero/rero-invenio-base/workflows/CI/badge.svg\n        :target: https://github.com/rero/rero-invenio-base/actions?query=workflow%3ACI\n\n.. image:: https://img.shields.io/github/tag/rero/rero-invenio-base.svg\n        :target: https://github.com/rero/rero-invenio-base/releases\n\n.. image:: https://img.shields.io/pypi/dm/rero-invenio-base.svg\n        :target: https://pypi.python.org/pypi/rero-invenio-base\n\n.. image:: https://img.shields.io/github/license/rero/rero-invenio-base.svg\n        :target: https://github.com/rero/rero-invenio-base/blob/master/LICENSE\n\nGeneric backend libraries for RERO Invenio instances.\n\nFurther documentation is available on\nhttps://rero-invenio-base.readthedocs.io/\n',
    'author': 'RERO',
    'author_email': 'software@rero.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.7,<3.10',
}


setup(**setup_kwargs)
