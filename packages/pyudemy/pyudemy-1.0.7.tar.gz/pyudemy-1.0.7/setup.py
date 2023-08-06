# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyudemy']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pyudemy',
    'version': '1.0.7',
    'description': 'Simple integrate of API udemy.com with python',
    'long_description': '# Pyudemy\n\n[![Python package](https://github.com/hudsonbrendon/pyudemy/actions/workflows/pythonpackage.yml/badge.svg)](https://github.com/hudsonbrendon/pyudemy/actions/workflows/pythonpackage.yml)\n[![Build Status](https://travis-ci.org/hudsonbrendon/pyudemy.svg?branch=master)](https://travis-ci.org/hudsonbrendon/pyudemy)\n[![Github Issues](http://img.shields.io/github/issues/hudsonbrendon/pyudemy.svg?style=flat)](https://github.com/hudsonbrendon/pyudemy/issues?sort=updated&state=open)\n![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)\n\nSimple integrate of API udemy.com with python\n\n# Quick start\n\n```bash\n$ pip install pyudemy\n```\nor\n\n```bash\n$ python setup.py install\n```\n\n# Authentication\n\nTo make any calls to Udemy REST API, you will need to create an API client. API client consists of a bearer token, which is connected to a user account on Udemy.\n\nIf you want to create an API client, [Sign up on udemy.com](https://www.udemy.com/join/) and go to API Clients page in your user profile. Once your API client request is approved, your newly created [API client](https://www.udemy.com/user/edit-api-clients/) will be active and your bearer token will be visible on [API Clients](https://www.udemy.com/user/edit-api-clients/) page.\n\n# Usage\n\nWith your key in hand, it\'s time to authenticate, so run:\n\n```python\n>>> from pyudemy import Udemy\n\n>>> udemy = Udemy(<CLIENT_ID>, <CLIENT_SECRET>)\n```\n\n# Courses\n\nReturns list of courses.\n\nTo see the list of accepted parameters go to:\n[https://www.udemy.com/developers/methods/get-courses-list/](https://www.udemy.com/developers/methods/get-courses-list/)\n\n```python\n>>> udemy.courses()\n```\nor\n\n```python\n>>> udemy.courses(page=1, page_size=1, ...)\n```\n\n# Course detail\n\nReturns course with specified id.\n\nTo see the list of accepted parameters go to:\n[https://www.udemy.com/developers/methods/get-courses-detail/](https://www.udemy.com/developers/methods/get-courses-detail/)\n\n```python\n>>> udemy.course_detail(<id>)\n```\n\n# Public curriculum\n\nReturns list of curriculum items.\n\nTo see the list of accepted parameters go to:\n[https://www.udemy.com/developers/methods/get-publiccurriculum-list/](https://www.udemy.com/developers/methods/get-publiccurriculum-list/)\n\n```python\n>>> udemy.public_curriculum(<id>)\n```\nor\n\n```python\n>>> udemy.public_curriculum(<id>, page=1, page_size=1)\n```\n\n# Course reviews\n\nReturns list of curriculum items.\n\nTo see the list of accepted parameters go to:\n[https://www.udemy.com/developers/methods/get-coursereviews-list/](https://www.udemy.com/developers/methods/get-coursereviews-list/)\n\n```python\n>>> udemy.course_reviews(<id>)\n```\nor\n\n```python\n>>> udemy.course_reviews(<id>, page=1, page_size=1)\n```\n# Controlling return Data\n\nYou can now control the return data from the API using a list of dictionaries passed under a parameter called "fields".\n![image](https://user-images.githubusercontent.com/33434582/160966081-b1f67fe2-48db-45d1-b102-95ef90e7c0cb.png)\n\n\nFor more info check Use of Fields and Field Lists at https://www.udemy.com/developers/affiliate/\n\n# Dependencies\n\n- Python >=3.8\n- [Pipenv](https://github.com/kennethreitz/pipenv)\n\n# License\n\n[MIT](http://en.wikipedia.org/wiki/MIT_License)\n',
    'author': 'Hudson Brendon',
    'author_email': 'contato.hudsonbrendon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hudsonbrendon/pyudemy#readme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
