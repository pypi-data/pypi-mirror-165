# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torchvf',
 'torchvf.configs.eval',
 'torchvf.configs.training',
 'torchvf.dataloaders',
 'torchvf.losses',
 'torchvf.metrics',
 'torchvf.models',
 'torchvf.numerics',
 'torchvf.numerics.differentiation',
 'torchvf.numerics.integration',
 'torchvf.numerics.interpolation',
 'torchvf.transforms',
 'torchvf.utils',
 'torchvf.utils.tiling']

package_data = \
{'': ['*']}

install_requires = \
['edt',
 'matplotlib',
 'numpy',
 'opencv-python',
 'pandas',
 'pyyaml',
 'scikit-learn',
 'torch>=1.6.0,<2.0.0',
 'torchvision']

setup_kwargs = {
    'name': 'torchvf',
    'version': '0.1.0',
    'description': 'Vector fields for instance segmentation in PyTorch.',
    'long_description': '# TorchVF\n\nWORK IN PROGRESS.\n\nTorchVF is a unifying Python library for using vector fields for lightweight \nproposal-free instance segmentation. The TorchVF library provides generalizable\nfunctions to automate ground truth vector field computation, interpolation of\ndiscrete vector fields, numeric integration solvers, clustering functions, and\nvarious other utilities. \n\nThis repository also provides all configs, code, and tools necessary to\nreproduce the results in my\n[article](https://github.com/ryanirl/torchvf/blob/main/article/first_draft.pdf)\non vector field based methods.\n\n## Quick Start\n\nFor anyone interested in learning about vector field based methods, see my\n[article](https://github.com/ryanirl/torchvf/blob/main/article/first_draft.pdf).\nTorchVF can be used to compute the instance segmentation given the semantic\nsegmentation and vector field via the following code: \n\n```Python\n# Consider we have a vector field `vf` and semantic segmentation `semantic`, \n# we can derive the instance segmentation via the following code: \n\nfrom torchvf.numerics import *\nfrom torchvf.utils import *\n\n# Step 1: Convert our discretely sampled vector field into continuous vector\n# field through bilinear interpolation. \nvf = interp_vf(vf, mode = "bilinear")\n\n# Step 2. Convert our semantic segmentation `semantic` into a set of\n# initial-values to be integrated through our vector field `vf`.\ninit_values = init_values_semantic(semantic, device = "cuda:0")\n\n# Step 3. Integrate our initial-values `init_values` through our vector field\n# `vf` for 25 steps with a step size of 0.1 using Euler\'s method for numeric \n# integration. \nsolutions = ivp_solver(\n    vf, \n    init_values, \n    dx = 0.1,\n    n_steps = 25,\n    solver = "euler"\n)[-1] # Get the final solution. \n\n# Clustering can only be done on the CPU. \nsolutions = solutions.cpu()\nsemantic = semantic.cpu()\n\n# Step 4. Cluster the integrated semantic points `solutions` to obtain the\n# instance segmentation. \ninstance_segmentation = cluster(\n    solutions, \n    semantic[0], \n    eps = 2.25,\n    min_samples = 15,\n    snap_noise = False\n)\n\n```\n\n## Installation\n\nWork in progress.\n\n## Usage\n\nWork in progress.\n\n## Citation\n\nWork in progress.\n\nTODO:\n - Scripts to reproduce all experiments.\n - Add dependencies and PyPi.\n - Usage.\n - Contributions (Not accepting pulls ATM, but feel free to post issues or send me emails.)\n - Add image/diagram for vector field based methods.\n\n\n## License\n\nDistributed under the MIT License. See `LICENSE` for more information.\n\n\n\n\n\n\n',
    'author': 'Ryan Peters',
    'author_email': 'RyanIRL@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ryanirl/torchvf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
