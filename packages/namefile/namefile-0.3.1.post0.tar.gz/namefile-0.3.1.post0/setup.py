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
    'version': '0.3.1.post0',
    'description': 'generate file name from file info',
    'long_description': "# namefile\n\n## Install\n\n```bash\npip install namefile\n```\n\n## Usage\n\n```python\nfrom namefile import namefile, parse\n\n\nfilename = namefile(\n    stem='glue-cola',\n    suffix='csv',\n    tags=('classification', 'processed'),\n    date=True,\n    version='1.2.0.post1'\n)\n# filename: 'glue_cola-classification-processed.20220829.1.2.0.post1-v.csv'\nfileinfo = parse(filename)\n# fileinfo: FileInfo(stem='glue_cola', suffix='csv', tags={'classification', 'processed'}, date=datetime.datetime(2022, 8, 29, 0, 0), version=<Version('1.2.0.post1')>)\nassert filename == fileinfo.name() == str(fileinfo)\n```\n\n## Development\n\n### conda env\n\n```shell\nconda env create\n```\n\n### poetry\n```shell\npoetry install\n```\n\n\n### Makefile\n\n```shell\n# 帮助文档\nmake help\n# 格式化代码\nmake style\n# 静态检查\nmake lint\n...\n```\n\n",
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
