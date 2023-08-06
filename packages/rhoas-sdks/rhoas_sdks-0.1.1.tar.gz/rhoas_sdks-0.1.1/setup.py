# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'sdks/smart_events_mgmt_sdk'}

packages = \
['rhoas_connector_mgmt_sdk',
 'rhoas_connector_mgmt_sdk.api',
 'rhoas_connector_mgmt_sdk.apis',
 'rhoas_connector_mgmt_sdk.model',
 'rhoas_connector_mgmt_sdk.models',
 'rhoas_kafka_instance_sdk',
 'rhoas_kafka_instance_sdk.model',
 'rhoas_kafka_mgmt_sdk',
 'rhoas_kafka_mgmt_sdk.api',
 'rhoas_kafka_mgmt_sdk.apis',
 'rhoas_kafka_mgmt_sdk.model',
 'rhoas_kafka_mgmt_sdk.models',
 'rhoas_registry_instance_sdk',
 'rhoas_registry_instance_sdk.api',
 'rhoas_registry_instance_sdk.apis',
 'rhoas_registry_instance_sdk.model',
 'rhoas_registry_instance_sdk.models',
 'rhoas_service_registry_mgmt_sdk',
 'rhoas_service_registry_mgmt_sdk.api',
 'rhoas_service_registry_mgmt_sdk.apis',
 'rhoas_service_registry_mgmt_sdk.model',
 'rhoas_service_registry_mgmt_sdk.models',
 'rhoas_smart_events_mgmt_sdk',
 'rhoas_smart_events_mgmt_sdk.api',
 'rhoas_smart_events_mgmt_sdk.apis',
 'rhoas_smart_events_mgmt_sdk.model',
 'rhoas_smart_events_mgmt_sdk.models']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil', 'urllib3==1.25.3']

setup_kwargs = {
    'name': 'rhoas-sdks',
    'version': '0.1.1',
    'description': 'A package which includes RHOAS SDKs',
    'long_description': '# RHOAS SDK for Python\n\nPython packages and API clients for Red Had OpenShift Application Services (RHOAS) \n\n[Check us out on GitHub](https://github.com/redhat-developer/app-services-sdk-python)\n\n## Prequisites\n\n- [Python 3.9](https://docs.python.org/3/) or above\n- [pip](https://pypi.org/project/pip/) for installing packages\n\n## Installation\n\nCurrently all RHOAS SDKs are bundled together. To install the RHOAS SDK with the pip package installer:\n\n```shell\n$ python3 -m pip install rhoas-sdks\n```\n\n## RHOAS App Services SDK for Python\n\n> NOTE: Some of these APIs are under development and may sometimes cause backwards-incompatible changes.\n\nAll packages are now available and can be accessed by just importing them as shown below:\n\n\n| API                       | Status | Package                                                                                                                                                         |\n| :------------------------ | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |\n| [KafkaManagement](sdks/kafka_mgmt_sdk/README.md)           | beta   | `import python rhoas_kafka_mgmt_sdk`          |\n| [ServiceRegistryManagement](sdks/registry_mgmt_sdk/README.md)  | alpha   | `import rhoas_service_registry_mgmt_sdk`         |\n| [ConnectorManagement](sdks/connector_mgmt_sdk/README.md)       | alpha  | `import rhoas_connector_mgmt_sdk`  |\n\n \n ## Instances SDKs\n\n| API              | Status | Package                                                                                                                                                                               |\n| ---------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |\n| KafkaInstance    | beta   | `import rhoas_kafka_instance_sdk`|\n| [RegistryInstance](sdks/registry_instance_sdk/README.md) | beta   | `import rhoas_registry_instance_sdk` |\n\n\n## Documentation\n\n[Documentation](./docs)\n\n## Examples\n\n[Examples](./examples)\n\n## Contributing\n\nContributions are welcome. See [CONTRIBUTING](CONTRIBUTING.md) for details.\n',
    'author': 'dimakis',
    'author_email': 'dsaridak@redhat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
