# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jdiff', 'jdiff.utils']

package_data = \
{'': ['*']}

install_requires = \
['deepdiff>=5.5.0,<6.0.0', 'jmespath>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'jdiff',
    'version': '0.0.1',
    'description': 'A light-weight library to compare structured output from network devices show commands.',
    'long_description': '# jdiff\n\n`jdiff` is a lightweight Python library allowing you to examine structured data. `jdiff` provides an interface to intelligently compare JSON data objects and test for the presence (or absence) of keys. You can also examine and compare corresponding key-values.\n\nThe library heavily relies on [JMESPath](https://jmespath.org/) for traversing the JSON object and finding the values to be evaluated. More on that [here](#customized-jmespath).\n\n## Installation \n\nInstall from PyPI:\n\n```\npip install jdiff\n```\n\n## Use cases\n\n`jdiff` has been developed around diffing and testing structured data returned from APIs and other Python modules and libraries (such as TextFSM). Our primary use case is the examination of structured data returned from networking devices. However, we found the library fits other use cases where structured data needs to be operated on, and is especially useful when working or dealing with data returned from APIs.\n\n## Documentation\n\nDocumentation is hosted on Read the Docs at [jdiff Documentation](https://jdiff.readthedocs.io/).',
    'author': 'Network to Code, LLC',
    'author_email': 'info@networktocode.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/networktocode/jdiff',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
