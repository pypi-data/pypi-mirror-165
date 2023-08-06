# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datacollector_api_client']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'datacollector-api-client',
    'version': '0.1.4',
    'description': 'Thin client for Azure Monitor DataCollector API.',
    'long_description': 'DataCollector API Client Library\n================================\nA thin client to send log data to Azure Monitor by using the `HTTP Data Collector API <https://docs.microsoft.com/en-us/azure/azure-monitor/logs/data-collector-api>`_.\n\n.. image:: https://github.com/francisco-ltech/datacollector-api-client/actions/workflows/tests.yml/badge.svg\n  :alt: Linux and Windows build status\n  \nInstallation\n------------\n::\n\n   $ pip install datacollector-api-client\n\nUsage\n-----\n\n\n::\n\n    from datacollector_api_client.client import DataCollectorWrapper\n\n    wrapper = DataCollectorWrapper(LOGANALYTICS_WORKSPACE_ID, LOGANALYTICS_WORKSPACE_KEY)\n\n    data = [{\n       "application": "my_app",\n       "message": "my log message"\n    }]\n\n    response = wrapper.log_info(structured_log_message=data)\n    print(response)\n\n\nTo log a message as error, use: *wrapper.log_error(structured_log_message=data)*\n\nYou can also override the default name of the tables by setting parameter: *log_type="your_preferred_table_name"*\n\n\n\nEnriching structured logging with Databricks information\n--------------------------------------------------------\nPass your dbutils instance from your Databricks session to the library\n\n::\n\n    wrapper = DataCollectorWrapper(LOGANALYTICS_WORKSPACE_ID, LOGANALYTICS_WORKSPACE_KEY, dbutils)\n\n    data = [{\n       "application": "Notebook",\n       "message": f\'Number of rows in dataframe: {df.count()}\'\n    }]\n\n    response = wrapper.log_info(structured_log_message=data)\n    print(response)\n\n\nThe following data is also collected and appended to your log:\n - dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()\n - dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().apply(\'clusterId\')\n - dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().apply(\'sessionId\')\n - dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().apply(\'user\')',
    'author': 'Francisco Ruiz A',
    'author_email': 'francisco@ltech.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/francisco-ltech/datacollector-api-client',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
