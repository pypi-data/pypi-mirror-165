# Neural Pipeline Search (NePS)

[![PyPI version](https://img.shields.io/pypi/v/neural-pipeline-search?color=informational)](https://pypi.org/project/neural-pipeline-search/)
[![Python versions](https://img.shields.io/pypi/pyversions/neural-pipeline-search)](https://pypi.org/project/neural-pipeline-search/)
[![License](https://img.shields.io/pypi/l/neural-pipeline-search?color=informational)](LICENSE)
[![Tests](https://github.com/automl/neps/actions/workflows/tests.yaml/badge.svg)](https://github.com/automl/neps/actions)

NePS helps deep learning experts find the best neural pipeline by helping with setting hyperparameters and designing neural architectures.

Please have a look at our **[documentation](https://automl.github.io/neps/)** and **[examples](neps_examples)**.

## Note

As indicated with the `v0.x.x` version number, NePS is early stage code and APIs might change in the future.

## Overview

NePS helps you by performing:

- Hyperparameter optimization (HPO) ([example](neps_examples/hyperparameters))
- (Hierarchical) Neural architecture search (NAS) ([example](neps_examples/hierarchical_architecture))
- Joint Architecture and Hyperparameter Search (JAHS) ([example](neps_examples/hyperparameters_architecture))

For efficiency and convenience NePS allows you to

- Leverage DL expert intuition to speed-up HPO, NAS, and JAHS ([example HPO](neps_examples/user_priors), [example JAHS](neps_examples/user_priors_also_architecture), [paper](https://openreview.net/forum?id=MMAeCXIa89))
- Asynchronously parallelize without code changes ([documentation](https://automl.github.io/neps/parallelization/))
- Continue runs across job time limits

## Installation

Using pip

```bash
pip install neural-pipeline-search
```

for more details see [the documentation](https://automl.github.io/neps/).

## Usage

Using `neps` always follows the same pattern:

1. Define a `run_pipeline` function that evaluates architectures/hyperparameters for your problem
1. Define a search space `pipeline_space` of architectures/hyperparameters
1. Call `neps.run` to optimize `run_pipeline` over `pipeline_space`

In code the usage pattern can look like this:

```python
import neps
import logging

# 1. Define a function that accepts hyperparameters and computes the validation error
def run_pipeline(hyperparameter_a: float, hyperparameter_b: int):
    validation_error = -hyperparameter_a * hyperparameter_b
    return validation_error


# 2. Define a search space of hyperparameters; use the same names as in run_pipeline
pipeline_space = dict(
    hyperparameter_a=neps.FloatParameter(lower=0, upper=1),
    hyperparameter_b=neps.IntegerParameter(lower=1, upper=100),
)

# 3. Call neps.run to optimize run_pipeline over pipeline_space
logging.basicConfig(level=logging.INFO)
neps.run(
    run_pipeline=run_pipeline,
    pipeline_space=pipeline_space,
    root_directory="usage_example",
    max_evaluations_total=5,
)
```

For more details and features please have a look at our [documentation](https://automl.github.io/neps/) and [examples](neps_examples).

## Analysing runs

See our [documentation on analysing runs](https://automl.github.io/neps/analyse).

## Contributing

Please see the [documentation for contributors](https://automl.github.io/neps/contributing/).
