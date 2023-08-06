# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['krausening', 'krausening.logging', 'krausening.properties']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=37.0.4,<38.0.0', 'javaproperties>=0.8.1,<0.9.0']

setup_kwargs = {
    'name': 'krausening',
    'version': '12',
    'description': 'Python implementation of Krausening',
    'long_description': '# Krausening Python - Externalized Property Management and Access for Python Projects #\n![PyPI](https://img.shields.io/pypi/v/krausening)\n[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://opensource.org/licenses/mit)\n\n Krausening property management and encryption for Python is packaged using the open-source Python Maven plugin [Habushu](https://bitbucket.org/cpointe/habushu) and made available as a [PyPI package](https://pypi.org/project/krausening/).  \n\n## Managing Properties with Krausening and Python\n\nManaging properties with Krausening\'s Python library utilizes a similar approach to that required by Krausening Java. Krausening Python expects that developers prime their target environment by configuring the following environment variables (which are named and leveraged in the same manner as the Java System Properties expected by Krausening Java):\n\n* `KRAUSENING_BASE`\n* `KRAUSENING_EXTENSIONS`\n* `KRAUSENING_PASSWORD`\n\nIn order to use the Krausening Python, developers may directly use `PropertyManager` or extend `PropertyManager` to provide a custom interface.  For example, developers may directly use the `PropertyManager` as such:\n\n```python\nfrom krausening.properties import PropertyManager\n\npropertyManager = PropertyManager.get_instance()\nproperties = None\nproperties = propertyManager.get_properties(\'my-property-file.properties\')\nassert properties[\'foo\'] == \'bar2\'\n```\n\nThis has the disadvantage that you must know the property keys in order to find the corresponding property values. To mitigate the need for all property file consumers to rely on specific property keys, consider wrapping the `PropertyManager` and writing your own custom methods to get the corresponding keys and values, abstracting away the exact key values:\n\n```python\nfrom krausening.properties import PropertyManager\n\nclass TestConfig():\n    """\n    Configurations utility class for being able to read in and reload properties\n    """\n\n    def __init__(self):\n        self.properties = None\n        self.reload()\n \n    def integration_test_enabled(self):\n        """\n        Returns whether the integration tests are enabled or not\n        """\n        integration_test_enable = False\n        integration_enable_str = self.properties[\'integration.test.enabled\']\n        if (integration_enable_str):\n            integration_test_enable = (integration_enable_str == \'True\')\n        return integration_test_enable\n    \n    def reload(self):\n        self.properties = PropertyManager.get_instance().get_properties(\'test.properties\')\n```\n\n**Note: Due to updates the M1 Apple Chip, we strongly recommend using Python >= 3.9 for compatibility reasons.**\n\n## Distribution Channel\n\nKrausening Python is published to PyPI under the [krausening](https://pypi.org/project/krausening/) project and may be installed using any package installer/manager that leverages PyPI.  For example:\n\n  * [Poetry](https://python-poetry.org/) - `poetry add krausening`\n  * [pip](https://pip.pypa.io/) - `pip install krausening`\n\n## Releasing to PyPI\n\nReleasing Krausening Python integrates into the project\'s larger utilization of the `maven-release-plugin`, specifically publishing the package to PyPI during the `deploy` phase.  A [PyPI account](https://pypi.org/account/register/) with access to the [krausening](https://pypi.org/project/krausening/) project is required. PyPI account credentials should be specified in your `settings.xml` under the `<id>pypi</id>` `<server>` entry:\n\n```xml\n<settings>\n  <servers>\n    <server>\n      <id>pypi</id>\n      <username>pypi-username</username>\n      <password>pypi-password</password>\n    </server>\n  </servers>\n</settings>\n```\n',
    'author': 'Eric Konieczny',
    'author_email': 'ekonieczny@cpointe-inc.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bitbucket.org/cpointe/krausening',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.9.13',
}


setup(**setup_kwargs)
