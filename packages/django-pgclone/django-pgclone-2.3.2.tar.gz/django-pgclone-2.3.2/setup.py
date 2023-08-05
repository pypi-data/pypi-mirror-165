# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pgclone', 'pgclone.management', 'pgclone.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['django>=2']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['importlib_metadata>=4']}

setup_kwargs = {
    'name': 'django-pgclone',
    'version': '2.3.2',
    'description': 'Dump and restore Postgres databases with Django.',
    'long_description': "django-pgclone\n##############\n\n``django-pgclone`` makes it easy to dump and restore Postgres databases.\nHere are some key features:\n\n1. Streaming dumps and restores to configurable storage backends like S3.\n   Instances with limited memory aren't a problem for large databases.\n\n2. A restoration process that works behind the scenes, swapping in\n   the restored database when finished.\n\n3. Configurable hooks into the dump and restore process, for example,\n   migrating a restored database before it is swapped.\n\n4. Reversible restores, making it possible to quickly revert to the initial\n   restore or the previous database.\n\n5. Re-usable configurations for instrumenting different types of dumps and restores.\n\nQuickstart\n==========\n\nTo dump a database, do::\n\n    python manage.py pgclone dump\n\nTo list database dump keys, do::\n\n    python manage.py pgclone ls\n\nTo restore a datase, do::\n\n    python manage.py pgclone restore <dump_key>\n\nDatabase dumps are relative to the storage location, which defaults to\nthe local file system. Dump keys are in\nthe format of ``<instance>/<database>/<config>/<timestamp>.dump``.\n\nWhen listing, use an optional prefix. Restoring\nsupports the same interface, using the latest key that matches the\nprefix.\n\nDocumentation\n=============\n\n`View the django-pgclone docs here\n<https://django-pgclone.readthedocs.io/>`_ to learn more about:\n\n* The basics and an overview of how it works.\n* The core command docs.\n* Configuring an S3 storage backend.\n* Running management command hooks during dumping or restoring.\n* Creating restores that can be quickly reverted.\n* Re-using command parameters for different flows.\n* All settings.\n* Additional details on using AWS RDS databases.\n\nInstallation\n============\n\nInstall django-pgclone with::\n\n    pip3 install django-pgclone\n\nAfter this, add ``pgclone`` to the ``INSTALLED_APPS``\nsetting of your Django project.\n\n**Note**  Install the AWS CLI to enable the S3 storage backend. Use ``pip install awscli``\nor follow the\n`installation guide here <https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html>`__.\n\nContributing Guide\n==================\n\nFor information on setting up django-pgclone for development and\ncontributing changes, view `CONTRIBUTING.rst <CONTRIBUTING.rst>`_.\n\nPrimary Authors\n===============\n\n- @wesleykendall (Wes Kendall)\n- @ethanpobrien (Ethan O'Brien)\n",
    'author': 'Wes Kendall',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Opus10/django-pgclone',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4',
}


setup(**setup_kwargs)
