# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbtc', 'dbtc.client', 'dbtc.client.cloud', 'dbtc.client.metadata']

package_data = \
{'': ['*'], 'dbtc.client.metadata': ['artifacts/*']}

install_requires = \
['requests>=2.27.1,<3.0.0', 'sgqlc>=15.0,<16.0', 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['dbtc = dbtc.cli:main']}

setup_kwargs = {
    'name': 'dbtc',
    'version': '0.2.0',
    'description': 'An unaffiliated python wrapper for dbt Cloud APIs',
    'long_description': '<p align="center">\n    <a href="#"><img src="docs/img/dbt-standalone.png"></a>\n</p>\n<p align="center">\n    <em>An unaffiliated python interface for dbt Cloud APIs</em>\n</p>\n<p align="center">\n    <a href="https://codecov.io/gh/dpguthrie/dbtc" target="_blank">\n        <img src="https://img.shields.io/codecov/c/github/dpguthrie/dbtc" alt="Coverage">\n    </a>\n    <a href="https://pypi.org/project/dbtc" target="_blank">\n        <img src="https://badge.fury.io/py/dbtc.svg" alt="Package version">\n    </a>\n    <a href="https://pepy.tech/project/dbtc" target="_blank">\n        <img src="https://pepy.tech/badge/dbtc" alt="Downloads">\n    </a>\n</p>\n\n---\n\n**Documentation**: <a target="_blank" href="https://dbtc.dpguthrie.com">https://dbtc.dpguthrie.com</a>\n\n**Source Code**: <a target="_blank" href="https://github.com/dpguthrie/dbtc">https://github.com/dpguthrie/dbtc</a>\n\n**V2 Docs**: <a target="_blank" href="https://docs.getdbt.com/dbt-cloud/api-v2">https://docs.getdbt.com/dbt-cloud/api-v2</a>\n\n**V3 Docs (Unofficial)**: <a target="_blank" href="https://documenter.getpostman.com/view/14183654/UVsSNiXC">https://documenter.getpostman.com/view/14183654/UVsSNiXC</a>\n\n**V4 Docs**: <a target="_blank" href="https://docs.getdbt.com/dbt-cloud/api-v4">https://docs.getdbt.com/dbt-cloud/api-v4</a>\n\n---\n\n## Overview\n\ndbtc is an unaffiliated python interface to various dbt Cloud API endpoints.\n\nThis library acts as a convenient interface to two different APIs that dbt Cloud offers:\n\n- Cloud API:  This is a REST API that exposes endpoints that allow users to programatically create, read, update, and delete\nresources within their dbt Cloud Account.\n- Metadata API:  This is a GraphQL API that exposes metadata generated from a job run within dbt Cloud.\n\n## Requirements\n\nPython 3.7+\n\n- [Requests](https://requests.readthedocs.io/en/master/) - The elegant and simple HTTP library for Python, built for human beings.\n- [sgqlc]() - Simple GraphQL Client\n- [Typer](https://github.com/ross/requests-futures) - Library for building CLI applications\n\n## Installation\n\n```bash\npip install dbtc\n```\n## Basic Usage\n\n### Python\n\nThe interface to both APIs are located in the `dbtCloudClient` class.\n\nThe example below shows how you use the `cloud` property on an instance of the `dbtCloudClient` class to to access a method, `trigger_job`, that with certain arguments, allows you to restart a job from the point of failure.\n\n```python\nfrom dbtc import dbtCloudClient\n\n# Assumes that DBT_CLOUD_SERVICE_TOKEN env var is set\nclient = dbtCloudClient()\n\naccount_id = 1\njob_id = 1\npayload = {\'cause\': \'Restarting from failure\'}\n\nrun = client.cloud.trigger_job(\n    account_id,\n    job_id,\n    payload,\n    restart_from_failure=True,\n    should_poll=False,\n)\n\n# This returns a dictionary containing two keys\nrun[\'data\']\nrun[\'status\']\n```\n\nSimilarly, use the `metadata` property to retrieve information about certain resources within your project - the example below shows how to retrieve metadata from models related to the most recent run for a given `job_id`.\n\n```python\nfrom dbtc import dbtCloudClient\n\nclient = dbtCloudClient()\n\njob_id = 1\n\nmodels = client.metadata.get_models(job_id)\n\n# Models nested inside a couple keys\nmodels[\'data\'][\'models\']\n\n# This is a list\nmodels[\'data\'][\'models\'][0]\n```\n\n### CLI\n\nThe CLI example below will map to the python cloud example above:\n\n```bash\ndbtc trigger-job \\\n    --account-id 1\n    --job-id 1\n    --payload \'{"cause": "Restarting from failure"}\' \\\n    --restart_from_failure \\\n    --no-should-poll\n```\n\nSimilarly, for the metadata example above:\n\n```bash\ndbtc get-models \\\n    --job-id 1\n```\n\nIf not setting your service token as an environment variable, do the following:\n\n```bash\ndbtc --token this_is_my_token get_models \\\n    --job-id 1\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Doug Guthrie',
    'author_email': 'douglas.p.guthrie@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
