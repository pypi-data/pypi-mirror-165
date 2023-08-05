# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pennylane_ket']
install_requires = \
['PennyLane>=0.25.1,<0.26.0', 'ket-lang>=0.4,<0.5']

entry_points = \
{'pennylane.plugins': ['ket = pennylane_ket:KetDevice']}

setup_kwargs = {
    'name': 'pennylane-ket',
    'version': '0.1.0',
    'description': 'Ket PennyLane plugin',
    'long_description': "# Ket PennyLane plugin\n\n## Install \n\n\n```shell \npip install pennylane-ket\n```\n\nor\n\n```shell \npip install git+https://gitlab.com/quantuloop/pennylane-ket.git\n```\n\n## Example\n\n```python\nimport pennylane as qml\ndev = qml.device('ket', wires=2)\n```",
    'author': 'Evandro Chagas Ribeiro da Rosa',
    'author_email': 'ev.crr97@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
