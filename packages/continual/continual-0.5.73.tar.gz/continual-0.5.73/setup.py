# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['continual',
 'continual.python',
 'continual.python.blob',
 'continual.python.cli',
 'continual.python.cli.tests',
 'continual.python.sdk',
 'continual.python.sdk.extensions',
 'continual.python.sdk.extensions.algorithms',
 'continual.python.sdk.extensions.models',
 'continual.python.sdk.extensions.templates',
 'continual.python.sdk.features',
 'continual.python.sdk.logger',
 'continual.python.utils',
 'continual.rpc',
 'continual.rpc.graphql',
 'continual.rpc.logging',
 'continual.rpc.logging.v1',
 'continual.rpc.management',
 'continual.rpc.management.v1',
 'continual.rpc.rpc',
 'continual.services',
 'continual.services.compute_services',
 'continual.services.compute_services.pipelines',
 'continual.services.compute_services.pipelines.batchprediction',
 'continual.services.compute_services.pipelines.training',
 'continual.services.compute_services.pipelines.training.tests',
 'continual.services.compute_services.utils',
 'continual.services.dataingest']

package_data = \
{'': ['*'],
 'continual.python': ['examples/bank_marketing/*',
                      'examples/kickstarter/*',
                      'extras/*']}

install_requires = \
['GitPython>=3.1.27',
 'click==8.0.4',
 'cloudpickle>=2.0.0',
 'cron-descriptor>=1.2.24',
 'databricks_api>=0.8.0',
 'dill>=0.3.4',
 'fsspec==2022.3',
 'gitpython>=3.1.7',
 'google-cloud-storage>=1.33.0',
 'grpcio>=1.27.1',
 'grpcio_status>=1.31.0',
 'halo>=0.0.30',
 'humanize>=2.5.0',
 'jinja2>=3.1.1',
 'mlflow>=1.23.1',
 'numpy>=1.21.6',
 'pandas-gbq>=0.14.1',
 'pandas>=1.0.1',
 'poetry>=0.12',
 'protobuf>=3.12.0,<3.19.0',
 'psutil>=5.8.0',
 'pyhive>=0.6.4',
 'pytz>=2020.5',
 'pyyaml>=5.4',
 'requests>=2.23.0',
 'rich>=9.13.0',
 'scikit_learn>=1.1.2',
 'shortuuid>=1.0.9',
 'simplejson>=3.17.6',
 'snowflake-sqlalchemy>=1.3.3',
 'sqlalchemy-bigquery>=1.4.3',
 'sqlalchemy-redshift>=0.8.9',
 'sqlalchemy>=1.4.27',
 'sqlparse>=0.4.2',
 'tableschema>=1.20.2',
 'tabulate>=0.8.6',
 'toml>=0.10.2',
 'tqdm>=4.54.1',
 'typer==0.4.0',
 'yamale>=4.0.0']

entry_points = \
{'console_scripts': ['continual = continual.python.cli.cli:cli']}

setup_kwargs = {
    'name': 'continual',
    'version': '0.5.73',
    'description': 'Operational AI for the Modern Data Stack',
    'long_description': '# Python CLI and SDK for Continual\n\nContinual is an operational AI for the modern data stack. Learn more at\nhttps://continual.ai.\n\n## Getting Started\n\nTo install the Continual CLI and SDK run:\n\n```\npip3 install continual\n```\n',
    'author': 'Continual',
    'author_email': 'support@continual.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
