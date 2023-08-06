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
    'version': '0.1.2',
    'description': 'Python library for plotting Cellphonedb results. Ported from ktplots R package.',
    'long_description': '|Docs| |PyPI| |Master| |MasterTest| |CodeCov|\n\nktplots-*py*\n------------\n\n|logo|\n\nWelcome! This is a super light-weight python library for plotting \n`CellphoneDB <https://www.github.com/ventolab/CellphoneDB/>`__ results. Ported from \n`ktplots <https://www.github.com/zktuong/ktplots/>`__ R package. For more options, \nplease check out the original R \n`package <https://www.github.com/zktuong/ktplots/>`__.\n\nThe documentation is\n`here <https://ktplotspy.readthedocs.io/>`__.\n\nInstallation\n------------\n\n.. code:: bash\n\n    pip install ktplotspy\n\n\nSupport\n-------\n\nSupport is provided on a voluntary basis, as time permits.\n\nIf there are any ideas, comments, suggestions, thing you would like to\nknow more etc., please feel free to email me at kt16@sanger.ac.uk or\npost in the issue tracker and I will get back to you.\n\nCitation\n--------\n\nIf you find this useful, please consider citing the github repositories. Also leave a star at the \n`ktplotspy <https://www.github.com/zktuong/ktplotspy/>`__ and the original\n`ktplots <https://www.github.com/zktuong/ktplots/>`__ repositories!\n\n.. |Docs| image:: https://readthedocs.org/projects/ktplotspy/badge/?version=latest\n   :target: https://ktplotspy.readthedocs.io/en/latest/?badge=latest\n.. |PyPI| image:: https://img.shields.io/pypi/v/ktplotspy?logo=PyPI\n   :target: https://pypi.org/project/ktplotspy/\n.. |Master| image:: https://byob.yarr.is/zktuong/ktplotspy/version\n   :target: https://github.com/zktuong/ktplotspy/tree/master\n.. |MasterTest| image:: https://github.com/zktuong/ktplotspy/workflows/tests/badge.svg?branch=master\n   :target: https://github.com/zktuong/ktplotspy/actions/workflows/tests.yml\n.. |CodeCov| image:: https://codecov.io/gh/zktuong/ktplotspy/branch/master/graph/badge.svg?token=661BMU1FBO\n   :target: https://codecov.io/gh/zktuong/ktplotspy\n.. |logo| image:: docs/notebooks/logo.png\n',
    'author': 'Kelvin Tuong',
    'author_email': '26215587+zktuong@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zktuong/ktplotspy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
