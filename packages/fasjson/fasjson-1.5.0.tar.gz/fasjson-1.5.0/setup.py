# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fasjson',
 'fasjson.lib',
 'fasjson.lib.ldap',
 'fasjson.tests',
 'fasjson.tests.unit',
 'fasjson.web',
 'fasjson.web.apis',
 'fasjson.web.extensions',
 'fasjson.web.resources',
 'fasjson.web.utils']

package_data = \
{'': ['*'], 'fasjson.tests': ['fixtures/*']}

install_requires = \
['Flask>=2.0.1,<3.0.0',
 'dnspython>=2.1.0,<3.0.0',
 'flask-healthz>=0.0.3,<0.0.4',
 'flask-mod-auth-gssapi>=0.2.0,<0.3.0',
 'flask-restx>=0.5.0,<0.6.0',
 'python-freeipa>=1.0.5,<2.0.0',
 'python-ldap>=3.2.0,<4.0.0',
 'requests-gssapi>=1.2.3,<2.0.0',
 'requests-kerberos>=0.12.0,<1.0.0',
 'werkzeug<2.1.0']

setup_kwargs = {
    'name': 'fasjson',
    'version': '1.5.0',
    'description': 'fasjson makes it possible for applications to talk to the fedora account system.',
    'long_description': '# Fedora Account System / IPA JSON gateway\n\nA JSON gateway to query FreeIPA, built for the Fedora Account System.\n\nThe documentation is available at https://fasjson.readthedocs.io/\n\n![Tests status](https://github.com/fedora-infra/fasjson/actions/workflows/tests.yml/badge.svg?branch=dev)\n![Documentation](https://readthedocs.org/projects/fasjson/badge/?version=latest)\n\n\n## TODO\n\n- documentation\n- HTTPS\n',
    'author': 'Fedora Infrastructure',
    'author_email': 'admin@fedoraproject.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fedora-infra/fasjson',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
