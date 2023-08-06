# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['admin_data_views', 'admin_data_views.templatetags']

package_data = \
{'': ['*'], 'admin_data_views': ['templates/admin_data_views/*']}

install_requires = \
['Django>=3.2', 'django-settings-holder>=0.0.4']

setup_kwargs = {
    'name': 'django-admin-data-views',
    'version': '0.2.4',
    'description': 'Add custom data views to django admin panel.',
    'long_description': '# Django Admin Data Views\n\n[![Coverage Status][coverage-badge]][coverage]\n[![GitHub Workflow Status][status-badge]][status]\n[![PyPI][pypi-badge]][pypi]\n[![GitHub][licence-badge]][licence]\n[![GitHub Last Commit][repo-badge]][repo]\n[![GitHub Issues][issues-badge]][issues]\n[![Downloads][downloads-badge]][pypi]\n\n[![Python Version][version-badge]][pypi]\n[![Django Version][django-badge]][pypi]\n\n```shell\npip install django-admin-data-views\n```\n\n---\n\n**Documentation**: [https://mrthearman.github.io/django-admin-data-views/](https://mrthearman.github.io/django-admin-data-views/)\n\n**Source Code**: [https://github.com/MrThearMan/django-admin-data-views/](https://github.com/MrThearMan/django-admin-data-views/)\n\n---\n\nDjango Admin Data Views enables you to easily add non-model data to the django admin panel.\nData from an API or file can be shown in similar table and item views than regular models.\n\n\n![Example](https://github.com/MrThearMan/django-admin-data-views/raw/main/docs/img/example.png?raw=true)\n\n\n[coverage-badge]: https://coveralls.io/repos/github/MrThearMan/django-admin-data-views/badge.svg?branch=main\n[status-badge]: https://img.shields.io/github/workflow/status/MrThearMan/django-admin-data-views/Test\n[pypi-badge]: https://img.shields.io/pypi/v/django-admin-data-views\n[licence-badge]: https://img.shields.io/github/license/MrThearMan/django-admin-data-views\n[repo-badge]: https://img.shields.io/github/last-commit/MrThearMan/django-admin-data-views\n[issues-badge]: https://img.shields.io/github/issues-raw/MrThearMan/django-admin-data-views\n[version-badge]: https://img.shields.io/pypi/pyversions/django-admin-data-views\n[downloads-badge]: https://img.shields.io/pypi/dm/django-admin-data-views\n[django-badge]: https://img.shields.io/pypi/djversions/django-admin-data-views\n\n[coverage]: https://coveralls.io/github/MrThearMan/django-admin-data-views?branch=main\n[status]: https://github.com/MrThearMan/django-admin-data-views/actions/workflows/test.yml\n[pypi]: https://pypi.org/project/django-admin-data-views\n[licence]: https://github.com/MrThearMan/django-admin-data-views/blob/main/LICENSE\n[repo]: https://github.com/MrThearMan/django-admin-data-views/commits/main\n[issues]: https://github.com/MrThearMan/django-admin-data-views/issues\n',
    'author': 'Matti Lamppu',
    'author_email': 'lamppu.matti.akseli@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MrThearMan/django-admin-data-views',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
