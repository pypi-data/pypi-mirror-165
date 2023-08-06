# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ktplotspy', 'ktplotspy.plot', 'ktplotspy.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'pandas', 'plotnine', 'seaborn']

extras_require = \
{'docs': ['nbsphinx',
          'sphinx-autodoc-typehints',
          'sphinx_rtd_theme',
          'readthedocs-sphinx-ext',
          'recommonmark'],
 'test': ['anndata>=0.7.6,<0.8.0', 'black', 'pytest-cov']}

setup_kwargs = {
    'name': 'ktplotspy',
    'version': '0.1.1',
    'description': 'Python library for plotting Cellphonedb results. Ported from ktplots R package.',
    'long_description': None,
    'author': 'Kelvin Tuong',
    'author_email': '26215587+zktuong@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
