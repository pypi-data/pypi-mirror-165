# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['cortex_xdr_client', 'cortex_xdr_client.api', 'cortex_xdr_client.api.models']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'cortex-xdr-client',
    'version': '1.7.3',
    'description': 'API client for Cortex XDR Prevent',
    'long_description': 'About the cortex-xdr-client\n###########################\n\nA python-based API client for `Cortex XDR\nAPI <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api>`__.\n\nCurrently, it supports the following Cortex XDR **Prevent & Pro** APIs:\n\n*Incidents API:*\n\n-  `Get Incidents <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/incident-management/get-incidents.html>`__\n-  `Get Extra Incident Data <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/incident-management/get-extra-incident-data.html>`__\n\n\n*Alerts API:*\n\n-  `Get Alerts <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/incident-management/get-alerts.html>`__\n\n\n*Endpoints API:*\n\n-  `Get All Endpoints <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/endpoint-management/get-all-endpoints.html>`__\n-  `Get Endpoint <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/endpoint-management/get-endpoints.html>`__\n-  `Isolate Endpoints <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/response-actions/isolate-endpoints.html>`__\n-  `Unisolate Endpoints <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/response-actions/unisolate-endpoints.html>`__\n-  `Scan Endpoints <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/response-actions/scan-endpoints.html>`__\n-  `Retrieve File <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/response-actions/retrieve-file.html>`__\n-  `Quarantine File <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/response-actions/quarantine-file.html>`__\n\n\n*XQL API:*\n\n-  `Start XQL <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/xql-apis/start-xql-query.html>`__\n-  `Get XQL Results <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/xql-apis/get-xql-query-results.html>`__\n-  `Get XQL Result Stream <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/xql-apis/get-xql-query-exported-data.html>`__\n\n\n*Scripts API:*\n\n-  `Get Scripts <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/script-execution/get-scripts.html>`__\n-  `Get Script Metadata <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/script-execution/get-script-metadata.html>`__\n-  `Get Script Execution Status <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/script-execution/get-script-execution-status.html>`__\n-  `Get Script Execution Results <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/script-execution/get-script-execution-results.html>`__\n-  `Get Script Execution Result Files <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/script-execution/get-script-execution-result-files.html>`__\n-  `Run Script <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/script-execution/run-script.html>`__\n-  `Run Snippet Code Script <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/script-execution/run-snippet-code-script.html>`__\n\n\n*Response Actions API:*\n\n-  `Get Action Status <https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/response-actions/get-action-status.html>`__\n\n*Contributing:*\n\nSee `CONTRIBUTING.md <./CONTRIBUTING.md>`__ for details.\n',
    'author': 'ebarti',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ebarti/cortex-xdr-client',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
