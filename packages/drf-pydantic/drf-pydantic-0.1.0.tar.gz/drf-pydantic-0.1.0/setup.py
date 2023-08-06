# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['drf_pydantic']

package_data = \
{'': ['*']}

install_requires = \
['djangorestframework>=3.13.0,<4.0.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'drf-pydantic',
    'version': '0.1.0',
    'description': 'Use pydantic with the Django REST framework',
    'long_description': '<p align="center">\n  <a href="https://github.com/georgebv/drf-pydantic/actions/workflows/cicd.yml" target="_blank">\n    <img src="https://github.com/georgebv/drf-pydantic/actions/workflows/cicd.yml/badge.svg?branch=main" alt="CI/CD Status">\n  </a>\n  <a href="https://codecov.io/gh/georgebv/drf-pydantic" target="_blank">\n    <img src="https://codecov.io/gh/georgebv/drf-pydantic/branch/main/graph/badge.svg?token=GN9rxzIFMc" alt="Test Coverage"/>\n  </a>\n</p>\n\nUse pydantic with the Django REST framework\n\n# Installation\n\n```shell\npip install drf-pydantic\n```\n\n# Usage\n\n```python\nfrom drf_pydantic import BaseModel\n\nclass MyModel(BaseModel):\n  name: str\n  addresses: list[str]\n\nserializer = MyModel.drf_serializer\n\n```\n',
    'author': 'George Bocharov',
    'author_email': 'bocharovgeorgii@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/georgebv/drf-pydantic',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
