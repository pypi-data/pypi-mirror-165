# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nilspodlib']

package_data = \
{'': ['*']}

install_requires = \
['imucal>=2.0.0,<3.0.0',
 'numpy>=1.19.2,<2.0.0',
 'pandas>=1.1.3,<2.0.0',
 'scipy>=1.5.2,<2.0.0',
 'typing-extensions>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'nilspodlib',
    'version': '3.4.1',
    'description': 'A Python library to load and convert sensor data recorded by a NilsPod by Portablies.',
    'long_description': '# NilsPodLib\n\n[![PyPI](https://img.shields.io/pypi/v/nilspodlib)](https://pypi.org/project/nilspodlib/)\n[![codecov](https://codecov.io/gh/mad-lab-fau/NilsPodLib/branch/master/graph/badge.svg?token=2CXLVYMHJF)](https://codecov.io/gh/mad-lab-fau/NilsPodLib)\n![Test and Lint](https://github.com/mad-lab-fau/NilsPodLib/workflows/Test%20and%20Lint/badge.svg)\n[![Documentation Status](https://readthedocs.org/projects/nilspodlib/badge/?version=latest)](https://nilspodlib.readthedocs.io/en/latest/?badge=latest)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/nilspodlib)\n\nA python package to parse logged NilsPod binary files.\n\n## Installation\n\n```\npip install nilspodlib --upgrade\n```\n\nIf you have access to the mad-lab gitlab server, you can further install the `nilspodrefcal` repository, which contains\nreference calibrations for a selected set of NilsPod sensors.\nYou can install it using:\n\n```\npip install git+https://mad-srv.informatik.uni-erlangen.de/MadLab/portabilestools/nilspodrefcal.git --upgrade\n```\n\n## For users of NilsPodLib v1.0\n\nWith v2.0.0 the name of the library was updated from `NilsPodLib` to `nilspodlib` to comply with the recommended naming\nstyle for Python packages.\nTherefore, you need to update your import path, when updating to the new version!\n\n## For developer\n\nInstall Python >=3.8 and [poetry](https://python-poetry.org).\nThen run the commands below to get the latest source and install the dependencies:\n\n```bash\ngit clone https://github.com/mad-lab-fau/NilsPodLib.git\ncd nilspodlib\npoetry install\n```\n\nTo run any of the tools required for the development workflow, use the poe commands:\n\n```\nCONFIGURED TASKS\n  format         \n  lint           Lint all files with Prospector.\n  check          Check all potential format and linting issues.\n  test           Run Pytest with coverage.\n  docs           Build the html docs using Sphinx.\n  bump_version   \n```\n\nby calling\n\n```bash\npoetry run poe <command name>\n````\n',
    'author': 'Arne Küderle',
    'author_email': 'arne.kuederle@fau.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mad-lab-fau/NilsPodLib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<=3.11',
}


setup(**setup_kwargs)
