# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['namefile']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=21.3,<22.0']

setup_kwargs = {
    'name': 'namefile',
    'version': '0.1.0',
    'description': 'Pydantic to CLI',
    'long_description': '# namefile\n\n \n\n## Usage\n\n### conda env\n\n```shell\nconda env create\n```\n\n### poetry\n```shell\npoetry install\n```\n\n\n### Makefile\n\n```shell\n# 帮助文档\nmake help\n# 格式化代码\nmake style\n# 静态检查\nmake lint\n...\n```\n\n',
    'author': 'wangyuxin',
    'author_email': 'wangyuxin@mokahr.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
