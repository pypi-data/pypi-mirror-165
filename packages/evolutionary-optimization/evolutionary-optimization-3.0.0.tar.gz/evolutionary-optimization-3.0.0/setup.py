# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['evolutionary_optimization',
 'evolutionary_optimization.evolutionary_algorithm',
 'evolutionary_optimization.fitness_functions',
 'evolutionary_optimization.genotype',
 'evolutionary_optimization.genotype.genotype_model',
 'evolutionary_optimization.genotype.implemented_genotypes',
 'evolutionary_optimization.phenotype',
 'evolutionary_optimization.phenotype.implemented_phenotypes',
 'evolutionary_optimization.phenotype.phenotype_model']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.2,<4.0.0', 'numpy>=1.23.0,<2.0.0', 'tqdm>=4.64.0,<5.0.0']

entry_points = \
{'console_scripts': ['run_evolution = '
                     'evolutionary_optimization.main:run_evolutionary_alg']}

setup_kwargs = {
    'name': 'evolutionary-optimization',
    'version': '3.0.0',
    'description': 'A generic evolutionary algorithm for function optimisation.',
    'long_description': '# Evolutionary-Optimization\nA generic evolutionary algorithm for function optimization.\n\n## Introduction\nThis package allows the user to optimise a function using an evolutionary algorithm.\nAn [evolutionary algorithm](https://en.wikipedia.org/wiki/Evolutionary_algorithm) \nuses the principles of evolution to find optimal solutions.\n\n## Using the Package\n### Getting Started \nTo get started with this package install this package:\n\n```bash\npip install evolutionary_optimization\n```\n\n### Running Experiments\nTo run the code type the following in your terminal. The default experiment is a \nsimple optimization of the $x^{2}$ using integers.\n```bash\nrun_evolution\n```\nThe parameters used for the run can be edited within the main.py file.\n\n### Personalising Experiments\nTo personalise your experiment you can either use the prebuilt phenotypes and genotypes using our interface,\nor you can build your own. \nTo do so, you simply need to create a new phenotype / genotype class that \ninherits from the corresponding abstract class and implement the methods to suit your needs.\n',
    'author': 'Marta Wolinska',
    'author_email': 'mswolinska@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mwolinska/Evolutionary-Optimization',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
