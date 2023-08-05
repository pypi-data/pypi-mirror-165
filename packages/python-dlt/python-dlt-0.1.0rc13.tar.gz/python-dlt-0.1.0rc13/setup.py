# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dlt',
 'dlt.cli',
 'dlt.common',
 'dlt.common.configuration',
 'dlt.common.configuration.providers',
 'dlt.common.normalizers.json',
 'dlt.common.normalizers.names',
 'dlt.common.runners',
 'dlt.common.schema',
 'dlt.common.storages',
 'dlt.dbt_runner',
 'dlt.extract',
 'dlt.extract.generator',
 'dlt.helpers',
 'dlt.load',
 'dlt.load.bigquery',
 'dlt.load.dummy',
 'dlt.load.redshift',
 'dlt.normalize',
 'dlt.pipeline',
 'examples',
 'examples.schemas',
 'examples.sources']

package_data = \
{'': ['*'],
 'examples': ['data/*', 'data/rasa_trackers/*', 'data/singer_taps/*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'cachetools>=5.2.0,<6.0.0',
 'hexbytes>=0.2.2,<0.3.0',
 'json-logging==1.4.1rc0',
 'jsonlines>=2.0.0,<3.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'prometheus-client>=0.11.0,<0.12.0',
 'randomname>=0.1.5,<0.2.0',
 'requests>=2.26.0,<3.0.0',
 'semver>=2.13.0,<3.0.0',
 'sentry-sdk>=1.4.3,<2.0.0',
 'simplejson>=3.17.5,<4.0.0',
 'tomlkit>=0.11.3,<0.12.0',
 'tzdata>=2022.1,<2023.0']

extras_require = \
{'bigquery': ['grpcio==1.43.0',
              'google-cloud-bigquery>=2.26.0,<3.0.0',
              'google-cloud-bigquery-storage>=2.13.0,<3.0.0',
              'pyarrow>=8.0.0,<9.0.0'],
 'dbt': ['GitPython>=3.1.26,<4.0.0',
         'dbt-core==1.0.6',
         'dbt-redshift==1.0.1',
         'dbt-bigquery==1.0.0'],
 'gcp': ['grpcio==1.43.0',
         'google-cloud-bigquery>=2.26.0,<3.0.0',
         'google-cloud-bigquery-storage>=2.13.0,<3.0.0',
         'pyarrow>=8.0.0,<9.0.0'],
 'postgres': ['psycopg2-binary>=2.9.1,<3.0.0'],
 'redshift': ['psycopg2-binary>=2.9.1,<3.0.0']}

entry_points = \
{'console_scripts': ['dlt = dlt.cli.dlt:main']}

setup_kwargs = {
    'name': 'python-dlt',
    'version': '0.1.0rc13',
    'description': 'DLT is an open-source python-native scalable data loading framework that does not require any devops efforts to run.',
    'long_description': '# Quickstart Guide: Data Load Tool (DLT)\n\n## **TL;DR: This guide shows you how to load a JSON document into Google BigQuery using DLT.**\n\n![](docs/DLT-Pacman-Big.gif)\n\n*Please open a pull request [here](https://github.com/scale-vector/dlt/edit/master/QUICKSTART.md) if there is something you can improve about this quickstart.*\n\n## Grab the demo\n\nClone the example repository:\n```\ngit clone https://github.com/scale-vector/dlt-quickstart-example.git\n```\n\nEnter the directory:\n```\ncd dlt-quickstart-example\n```\n\nOpen the files in your favorite IDE / text editor:\n- `data.json` (i.e. the JSON document you will load)\n- `credentials.json` (i.e. contains the credentials to our demo Google BigQuery warehouse)\n- `quickstart.py` (i.e. the script that uses DLT)\n\n## Set up a virtual environment\n\nEnsure you are using either Python 3.8 or 3.9:\n```\npython3 --version\n```\n\nCreate a new virtual environment:\n```\npython3 -m venv ./env\n```\n\nActivate the virtual environment:\n```\nsource ./env/bin/activate\n```\n\n## Install DLT and support for the target data warehouse\n\nInstall DLT using pip:\n```\npip3 install -U python-dlt\n```\n\nInstall support for Google BigQuery:\n```\npip3 install -U python-dlt[gcp]\n```\n\n## Understanding the code\n\n1. Configure DLT\n\n2. Create a DLT pipeline\n\n3. Load the data from the JSON document\n\n4. Pass the data to the DLT pipeline\n\n5. Use DLT to load the data\n\n## Running the code\n\nRun the script:\n\n```\npython3 quickstart.py\n```\n\nInspect `schema.yml` that has been generated:\n```\nvim schema.yml\n```\n\nSee results of querying the Google BigQuery table:\n\n`json_doc` table\n\n```\nSELECT * FROM `{schema_prefix}_example.json_doc`\n```\n```\n{  "name": "Ana",  "age": "30",  "id": "456",  "_dlt_load_id": "1654787700.406905",  "_dlt_id": "5b018c1ba3364279a0ca1a231fbd8d90"}\n{  "name": "Bob",  "age": "30",  "id": "455",  "_dlt_load_id": "1654787700.406905",  "_dlt_id": "afc8506472a14a529bf3e6ebba3e0a9e"}\n```\n\n`json_doc__children` table\n\n```\nSELECT * FROM `{schema_prefix}_example.json_doc__children` LIMIT 1000\n```\n```\n    # {"name": "Bill", "id": "625", "_dlt_parent_id": "5b018c1ba3364279a0ca1a231fbd8d90", "_dlt_list_idx": "0", "_dlt_root_id": "5b018c1ba3364279a0ca1a231fbd8d90",\n    #   "_dlt_id": "7993452627a98814cc7091f2c51faf5c"}\n    # {"name": "Bill", "id": "625", "_dlt_parent_id": "afc8506472a14a529bf3e6ebba3e0a9e", "_dlt_list_idx": "0", "_dlt_root_id": "afc8506472a14a529bf3e6ebba3e0a9e",\n    #   "_dlt_id": "9a2fd144227e70e3aa09467e2358f934"}\n    # {"name": "Dave", "id": "621", "_dlt_parent_id": "afc8506472a14a529bf3e6ebba3e0a9e", "_dlt_list_idx": "1", "_dlt_root_id": "afc8506472a14a529bf3e6ebba3e0a9e",\n    #   "_dlt_id": "28002ed6792470ea8caf2d6b6393b4f9"}\n    # {"name": "Elli", "id": "591", "_dlt_parent_id": "5b018c1ba3364279a0ca1a231fbd8d90", "_dlt_list_idx": "1", "_dlt_root_id": "5b018c1ba3364279a0ca1a231fbd8d90",\n    #   "_dlt_id": "d18172353fba1a492c739a7789a786cf"}\n```\n\nJoining the two tables above on autogenerated keys (i.e. `p._record_hash = c._parent_hash`)\n\n```\nselect p.name, p.age, p.id as parent_id,\n            c.name as child_name, c.id as child_id, c._dlt_list_idx as child_order_in_list\n        from `{schema_prefix}_example.json_doc` as p\n        left join `{schema_prefix}_example.json_doc__children`  as c\n            on p._dlt_id = c._dlt_parent_id\n```\n```\n    # {  "name": "Ana",  "age": "30",  "parent_id": "456",  "child_name": "Bill",  "child_id": "625",  "child_order_in_list": "0"}\n    # {  "name": "Ana",  "age": "30",  "parent_id": "456",  "child_name": "Elli",  "child_id": "591",  "child_order_in_list": "1"}\n    # {  "name": "Bob",  "age": "30",  "parent_id": "455",  "child_name": "Bill",  "child_id": "625",  "child_order_in_list": "0"}\n    # {  "name": "Bob",  "age": "30",  "parent_id": "455",  "child_name": "Dave",  "child_id": "621",  "child_order_in_list": "1"}\n```\n\n## Next steps\n\n1. Replace `data.json` with data you want to explore\n\n2. Check that the inferred types are correct in `schema.yml`\n\n3. Set up your own Google BigQuery warehouse (and replace the credentials)\n\n4. Use this new clean staging layer as the starting point for a semantic layer / analytical model (e.g. using dbt)',
    'author': 'ScaleVector',
    'author_email': 'services@scalevector.ai',
    'maintainer': 'Marcin Rudolf',
    'maintainer_email': 'marcin@scalevector.ai',
    'url': 'https://github.com/scale-vector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
