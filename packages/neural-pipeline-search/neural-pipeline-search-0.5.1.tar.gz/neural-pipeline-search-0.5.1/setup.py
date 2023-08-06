# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neps',
 'neps.optimizers',
 'neps.optimizers.bayesian_optimization',
 'neps.optimizers.bayesian_optimization.acquisition_functions',
 'neps.optimizers.bayesian_optimization.acquisition_samplers',
 'neps.optimizers.bayesian_optimization.kernels',
 'neps.optimizers.bayesian_optimization.kernels.grakel_replace',
 'neps.optimizers.bayesian_optimization.models',
 'neps.optimizers.grid_search',
 'neps.optimizers.multi_fidelity',
 'neps.optimizers.random_search',
 'neps.optimizers.regularized_evolution',
 'neps.search_spaces',
 'neps.search_spaces.categorical',
 'neps.search_spaces.graph_dense',
 'neps.search_spaces.graph_grammar',
 'neps.search_spaces.graph_grammar.cfg_variants',
 'neps.search_spaces.graph_grammar.graph_utils',
 'neps.search_spaces.numerical',
 'neps.status',
 'neps.utils',
 'neps_examples',
 'neps_examples.cost_aware',
 'neps_examples.fault_tolerance',
 'neps_examples.hierarchical_architecture',
 'neps_examples.hierarchical_architecture_hierarchical_GP',
 'neps_examples.hierarchical_kernels',
 'neps_examples.hyperparameters',
 'neps_examples.hyperparameters_architecture',
 'neps_examples.multi_fidelity',
 'neps_examples.user_priors',
 'neps_examples.user_priors_also_architecture']

package_data = \
{'': ['*']}

install_requires = \
['ConfigSpace>=0.4.19,<0.5.0',
 'grakel>=0.1.8,<0.2.0',
 'matplotlib>=3.4,<4.0',
 'metahyper>=0.5.3,<0.6.0',
 'networkx>=2.6.3,<3.0.0',
 'nltk>=3.6.4,<4.0.0',
 'numpy>=1.21.1,<2.0.0',
 'pandas>=1.3.1,<2.0.0',
 'path>=16.2.0,<17.0.0',
 'scipy>=1.7,<2.0',
 'termcolor>=1.1.0,<2.0.0',
 'torch>=1.7.0',
 'types-termcolor>=1.1.2,<2.0.0',
 'typing-extensions>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'neural-pipeline-search',
    'version': '0.5.1',
    'description': 'Neural Pipeline Search helps deep learning experts find the best neural pipeline.',
    'long_description': '# Neural Pipeline Search (NePS)\n\n[![PyPI version](https://img.shields.io/pypi/v/neural-pipeline-search?color=informational)](https://pypi.org/project/neural-pipeline-search/)\n[![Python versions](https://img.shields.io/pypi/pyversions/neural-pipeline-search)](https://pypi.org/project/neural-pipeline-search/)\n[![License](https://img.shields.io/pypi/l/neural-pipeline-search?color=informational)](LICENSE)\n[![Tests](https://github.com/automl/neps/actions/workflows/tests.yaml/badge.svg)](https://github.com/automl/neps/actions)\n\nNePS helps deep learning experts find the best neural pipeline by helping with setting hyperparameters and designing neural architectures.\n\nPlease have a look at our **[documentation](https://automl.github.io/neps/)** and **[examples](neps_examples)**.\n\n## Note\n\nAs indicated with the `v0.x.x` version number, NePS is early stage code and APIs might change in the future.\n\n## Overview\n\nNePS helps you by performing:\n\n- Hyperparameter optimization (HPO) ([example](neps_examples/hyperparameters))\n- (Hierarchical) Neural architecture search (NAS) ([example](neps_examples/hierarchical_architecture))\n- Joint Architecture and Hyperparameter Search (JAHS) ([example](neps_examples/hyperparameters_architecture))\n\nFor efficiency and convenience NePS allows you to\n\n- Leverage DL expert intuition to speed-up HPO, NAS, and JAHS ([example HPO](neps_examples/user_priors), [example JAHS](neps_examples/user_priors_also_architecture), [paper](https://openreview.net/forum?id=MMAeCXIa89))\n- Asynchronously parallelize without code changes ([documentation](https://automl.github.io/neps/parallelization/))\n- Continue runs across job time limits\n\n## Installation\n\nUsing pip\n\n```bash\npip install neural-pipeline-search\n```\n\nfor more details see [the documentation](https://automl.github.io/neps/).\n\n## Usage\n\nUsing `neps` always follows the same pattern:\n\n1. Define a `run_pipeline` function that evaluates architectures/hyperparameters for your problem\n1. Define a search space `pipeline_space` of architectures/hyperparameters\n1. Call `neps.run` to optimize `run_pipeline` over `pipeline_space`\n\nIn code the usage pattern can look like this:\n\n```python\nimport neps\nimport logging\n\n# 1. Define a function that accepts hyperparameters and computes the validation error\ndef run_pipeline(hyperparameter_a: float, hyperparameter_b: int):\n    validation_error = -hyperparameter_a * hyperparameter_b\n    return validation_error\n\n\n# 2. Define a search space of hyperparameters; use the same names as in run_pipeline\npipeline_space = dict(\n    hyperparameter_a=neps.FloatParameter(lower=0, upper=1),\n    hyperparameter_b=neps.IntegerParameter(lower=1, upper=100),\n)\n\n# 3. Call neps.run to optimize run_pipeline over pipeline_space\nlogging.basicConfig(level=logging.INFO)\nneps.run(\n    run_pipeline=run_pipeline,\n    pipeline_space=pipeline_space,\n    root_directory="usage_example",\n    max_evaluations_total=5,\n)\n```\n\nFor more details and features please have a look at our [documentation](https://automl.github.io/neps/) and [examples](neps_examples).\n\n## Analysing runs\n\nSee our [documentation on analysing runs](https://automl.github.io/neps/analyse).\n\n## Contributing\n\nPlease see the [documentation for contributors](https://automl.github.io/neps/contributing/).\n',
    'author': 'Danny Stoll',
    'author_email': 'stolld@cs.uni-freiburg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/automl/neps',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.8',
}


setup(**setup_kwargs)
