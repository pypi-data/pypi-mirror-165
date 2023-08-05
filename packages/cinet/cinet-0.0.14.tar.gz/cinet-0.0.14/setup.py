# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cinet', 'cinet.testing_utils']

package_data = \
{'': ['*']}

install_requires = \
['ConfigSpace>=0.5.0,<0.6.0',
 'lifelines>=0.27.1,<0.28.0',
 'numpy>=1.23.0,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pytorch-lightning>=1.6.4,<2.0.0',
 'ray>=1.13.0,<2.0.0',
 'sklearn>=0.0,<0.1',
 'tabulate>=0.8.10,<0.9.0',
 'torch>=1.11.0,<2.0.0']

setup_kwargs = {
    'name': 'cinet',
    'version': '0.0.14',
    'description': 'Scikit-Learn interface for CINET PyTorch siamese neural network',
    'long_description': '# cinet\n\nScikit-Learn interface for CINET PyTorch siamese neural network. \n\nDeepCINET is a deep "siamese" neural network architecture, where a contrastive loss function is used to learn feature weights that maximally discriminate relative response/target between valid pairs of training data. A hyper-parameter, delta, is used to define what a valid pair is by setting a minimum difference in response/target value for pairs to be included in model training, with the intuition that useful weights cannot be learned from samples that are too close together in response-space. \n\nConcordance index is then used to assess rank accuracy. Concordance index was chosen because it is a non-parametric statistic that does not make \nassumptions on data distributon or homoscedasticity. It can detect non-linear, monotonic associations.\n\nECINET is a one-dimensional neural network, which makes it essentially a linear regression model with regularization. It is comparable to model architectures like ElasticNet. It can be used\nto assess if improved performance is delivered by the added complexity of DeepCINET.\n\nNote, however, that siamese networks go hand-in-hand with few shot learning approaches. The idea is that features learned from large data in CINET can then be applied to learning done \non smaller real-world data in a transfer learning approach. \n\nAn initial implementation, trained on gene set expression data from cancer cell lines and meant to predict drug sensitivity rank, is available on the BHKLab\'s public GitHub at https://github.com/bhklab/cinet. \n\n## Installation\n\n```bash\n$ pip3 install cinet\n```\n\n## Usage\n\nCINET can be used like any other Scikit-Learn model. \n\n```python\n# Import CINET\nfrom cinet import *\n\n# Create a DeepCINET model\nmodel = deepCINET()\n# Or, create an ECINET model\nmodel = ECINET()\n\n# Standard Scikit-Learn syntax\nmodel.fit(X,y)\nmodel.predict(X)\nmodel.score(X,y)\n\n# You can use it with things like GridSearchCV easily\nGridSearchCV(deepCINET(device=\'cpu\', batch_size=2**12), param_grid, refit = True, verbose = 3,n_jobs=3)\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`cinet` was created by Christopher Eeles. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`cinet` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Christopher Eeles',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
