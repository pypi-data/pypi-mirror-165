# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['codal_tsetmc',
 'codal_tsetmc.config',
 'codal_tsetmc.download',
 'codal_tsetmc.download.codal',
 'codal_tsetmc.download.tsetmc',
 'codal_tsetmc.models']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'SQLAlchemy>=1.4.28,<2.0.0',
 'aiodns>=3.0.0,<4.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'jalali-pandas>=0.2.0,<0.3.0',
 'lxml>=4.8.0,<5.0.0',
 'pandas>=1.3.5,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'tehran_stocks==1.0']

setup_kwargs = {
    'name': 'codal-tsetmc',
    'version': '1.0.0',
    'description': 'Data Downloader for Codal and Tehran stock market',
    'long_description': '# کدال و بورس در پایتون\n',
    'author': 'Mohsen Ebrahimi',
    'author_email': 'mohsenebrahimy.ir@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ghodsizadeh.github.io/codal-tsetmc/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
