# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mediumroast_py',
 'mediumroast_py.api',
 'mediumroast_py.extractors',
 'mediumroast_py.transformers']

package_data = \
{'': ['*']}

install_requires = \
['PyDocX>=0.9.10,<0.10.0',
 'boto3>=1.24.24,<2.0.0',
 'geopy>=2.2.0,<3.0.0',
 'pdfx>=1.4.1,<2.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'python-magic>=0.4.27,<0.5.0',
 'python-pptx>=0.6.21,<0.7.0',
 'requests>=2.28.1,<3.0.0',
 'spacy>=3.3.1,<4.0.0']

setup_kwargs = {
    'name': 'mediumroast-py',
    'version': '0.3.17',
    'description': 'A package to perform ETL (Extract, Transform and Load) and  interact with the mediumroast.io application.',
    'long_description': "# Introduction\nThis is the Python Software Development Kit (SDK) for the mediumroast.io.  Internal tooling from Mediumroast, Inc. uses this SDK, so it will always be a first class citizen. Specifically, we build tools requiring ETL (Extract, Transform and Load), Machine Learning and Natural Language Processing (NLP) with this SDK. As appropriate examples illustrating various capabilities of the SDK can be found in the `mediumroast_examples/` directory of this package. \n\n## Current status\nThis SDK mirrors the capabilities of the mediumroast.io application server.  Therefore it is fully functional mapping to the capabilities aavailable from the server.  Specifically this means the SDK is capable of:\n1. Creating interaction, company, study and user objects\n2. Reporting on or listing interaction, company, study and user objects\n3. Transforming raw inputs into respective objects.\n4. Ingesting metadata from S3 buckets, provided they match a file name specification, into raw inputs that can be transformed.\nMany of these functionalities have example implementations that enable the developer to understand how to use the SDK.  Also the file name specification can be found in the github [mediumroast_examples directory](https://github.com/mediumroast/mediumroast_py/tree/main/mediumroast_examples) of the repository for mediumroast_py.\n\n## The Examples\nTo illustrate how to interact programmatically with the mediumroast.io application several examples have been created to make it easier for developers to interact with the system.  The scope of the examples, over time, will include all aspects of the SDK to speed up 3rd party development processes.  This means that over time examples for all apsects of the SDK will be produced and made available under the Apache Software License.  As with anything in the SDK if you run into problems please make sure that you raise an [issue](https://github.com/mediumroast/mediumroast_py/issues) in the repository.  More detail on the examples can be found within the [examples directory](https://github.com/mediumroast/mediumroast_py/tree/main/mediumroast_examples) of this repository.\n\n# Installation\nSince the package is under heavy development please check in often and upgrade frequently.\n\n## Installation\nThis package is available on PyPi and can be installed via pip use: `pip install mediumroast_py`\n\n## Upgrade\nYou can perform an upgrade using pip: `pip install mediumroast_py --upgrade`\n\n## Availability of mediumroast_examples\nInstallation through pip from [PyPi](https://pypi.org/project/mediumroast-py/) the examples will be installed in `dist-packages/mediumroast_examples`. For example if you're using Python 3.8 with `dist-packages` kept in `/usr/local` then this would be the path for the examples: `/usr/local/lib/python3.8/dist-packages/mediumroast_examples`.\n\n# Structure of the repository\nThe following structure is available for the Python SDK, as new SDK implementations are created additional top level directories will be created.\n```\nmediumnroast_py/\n      mediumroast_examples/\n      mediumroast_py/\n            api/\n            extractors/\n            transformers/\n            helpers.py\n      project.toml\n      README.md\n      LICENSE\n```",
    'author': 'Michael Hay',
    'author_email': 'michael.hay@mediumroast.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mediumroast/mediumroast_py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
