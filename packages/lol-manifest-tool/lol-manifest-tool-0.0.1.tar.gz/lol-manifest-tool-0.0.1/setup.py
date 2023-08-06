# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lol_manifest']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'requests>=2.28.1,<3.0.0', 'zstd>=1.5.2.5,<2.0.0.0']

setup_kwargs = {
    'name': 'lol-manifest-tool',
    'version': '0.0.1',
    'description': '获取英雄联盟最新文件清单文件、清单文件解析、清单文件对比，基于https://github.com/CommunityDragon/CDTB修改而来',
    'long_description': '# lol-manifest-tool\n获取英雄联盟最新文件清单文件、清单文件解析、清单文件对比，基于 https://github.com/CommunityDragon/CDTB 修改而来\n',
    'author': 'Virace',
    'author_email': 'Virace@aliyun.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Virace/lol-manifest-tool',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
