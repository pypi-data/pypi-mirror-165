# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mathmakerlib',
 'mathmakerlib.LaTeX',
 'mathmakerlib.calculus',
 'mathmakerlib.core',
 'mathmakerlib.geometry',
 'mathmakerlib.geometry.polygons',
 'mathmakerlib.geometry.polyhedra',
 'mathmakerlib.geometry.projections']

package_data = \
{'': ['*'], 'mathmakerlib.geometry': ['templates/*']}

install_requires = \
['toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'mathmakerlib',
    'version': '0.7.11',
    'description': 'Collection of various useful tools.',
    'long_description': '|PyPI1| |PyPI2| |PyPI3| |Codecov| |Build Status| |Documentation Status| |Maintenance|\n\n|PyPI4|\n\n\nOverview\n========\n\nMathmaker Lib offers lualatex-printable mathematical objects.\n\n`Repo is here <https://gitlab.com/nicolas.hainaux/mathmakerlib>`__\n\n`See documentation here <http://mathmaker-lib.readthedocs.io/>`__\n\nContact: nh dot techn (hosted by gmail dot com)\n\n.. |PyPI1| image:: https://img.shields.io/pypi/v/mathmakerlib.svg?maxAge=2592000\n   :target: https://pypi.python.org/pypi/mathmakerlib\n.. |PyPI2| image:: https://img.shields.io/pypi/status/mathmakerlib.svg?maxAge=2592000\n.. |PyPI3| image:: https://img.shields.io/pypi/pyversions/mathmakerlib.svg?maxAge=2592000\n.. |Build Status| image:: https://ci.appveyor.com/api/projects/status/7vejgm0hjm6236xo/branch/master?svg=true\n   :target: https://ci.appveyor.com/project/nicolashainaux/mathmakerlib-ho94f\n.. |Codecov| image:: https://codecov.io/gl/nicolas.hainaux/mathmakerlib/branch/master/graph/badge.svg\n  :target: https://codecov.io/gl/nicolas.hainaux/mathmakerlib\n.. |Documentation Status| image:: https://readthedocs.org/projects/mathmaker-lib/badge/?version=latest\n   :target: https://mathmaker-lib.readthedocs.io/en/latest/\n.. |Maintenance| image:: https://img.shields.io/maintenance/yes/2019.svg?maxAge=2592000\n.. |PyPI4| image:: https://img.shields.io/pypi/l/mathmakerlib.svg?maxAge=2592000\n   :target: https://gitlab.com/nicolas.hainaux/mathmakerlib/blob/master/LICENSE\n',
    'author': 'Nicolas Hainaux',
    'author_email': 'nh.techn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
