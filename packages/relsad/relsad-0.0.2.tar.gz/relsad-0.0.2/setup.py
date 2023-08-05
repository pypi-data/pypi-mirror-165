# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['relsad',
 'relsad.energy',
 'relsad.examples',
 'relsad.examples.CINELDI',
 'relsad.examples.IEEE16_modified',
 'relsad.examples.IEEE33',
 'relsad.examples.IEEE69',
 'relsad.examples.RBTS2',
 'relsad.examples.RBTS6',
 'relsad.examples.TEST10',
 'relsad.examples.load',
 'relsad.load',
 'relsad.loadflow',
 'relsad.network',
 'relsad.network.components',
 'relsad.network.containers',
 'relsad.network.systems',
 'relsad.reliability',
 'relsad.results',
 'relsad.simulation',
 'relsad.simulation.monte_carlo',
 'relsad.simulation.sequence',
 'relsad.topology',
 'relsad.topology.ICT',
 'relsad.topology.load_flow',
 'relsad.visualization']

package_data = \
{'': ['*'], 'relsad.examples.load': ['data/*']}

install_requires = \
['black>=20.8b1,<21.0',
 'flake8>=3.9.0,<4.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pre-commit>=2.12.0,<3.0.0',
 'scipy>=1.8.0,<2.0.0',
 'sphinx-book-theme>=0.3.2,<0.4.0',
 'sphinxcontrib-bibtex>=2.4.2,<3.0.0']

setup_kwargs = {
    'name': 'relsad',
    'version': '0.0.2',
    'description': 'A package that facilitates reliability investigations in power systems',
    'long_description': '######\nRELSAD\n######\n\n`RELSAD` -- RELiability tool for Smart and Active Distribution networks, is a Python-based\nreliability assessment tool that aims to function as a foundation for reliability\ncalculation of modern distribution systems.\nThe tool uses Monte Carlo simulation and stochastic variation to simulate the\nreliability of a distribution system. The package supports user-selected time\nincrement steps over a user-defined time period. In the tool, active components\nsuch as microgrids, wind power, solar power, batteries, and electrical vehicles\nare implemented. To evaluate smart power systems, ICT components such as\nautomated switches, sensors, and control system for the power grid are also implemented.\nIn addition to component implementation, in order to evaluate the reliability of such\ncomplex systems, the complexity, dependencies within a system, and interdependencies\nbetween systems and components are accounted for.\n\nThe tool can be used in modern distribution network development to evaluate\nthe influence of active components on the network reliability. Relevant use cases\ninclude investigating how:\n\n1. The introduction of microgrids with active production\n   affects the customers in the distribution network and vice versa\n2. Vehicle\\-to\\-grid strategies might mitigate load peaks and\n   improve the distribution network reliability\n3. The reliability of the ICT network impacts the\n   distribution network reliability\n\nExamples using well known test networks are included.\n\n============\nInstallation\n============\n\nSee https://relsad.readthedocs.io/en/latest/installation.html.\n\n========\nFeatures\n========\n\n- Monte Carlo simulation based reliability analysis of active distribution networks\n- Sequential simulation of the network behavoir with user defined loading and failure evolution\n\n============\nDependencies\n============\n\n- Numpy\n- Scipy\n- Matplotlib\n- Pandas\n\n=====\nUsage\n=====\n\nSee https://relsad.readthedocs.io/en/latest/usage.html.\n\n=============\nDocumentation\n=============\n\nThe official documentation is hosted on Read the Docs: https://relsad.readthedocs.io/en/latest/\n\n============\nContributors\n============\n\nWe welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/stinefm/relsad/graphs/contributors).\n',
    'author': 'Stine Fleischer Myhre',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stinefm/relsad',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
