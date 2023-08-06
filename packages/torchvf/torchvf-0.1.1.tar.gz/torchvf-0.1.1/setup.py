# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torchvf',
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
    'version': '0.1.1',
    'description': 'Vector fields for instance segmentation in PyTorch.',
    'long_description': '# TorchVF\n\nWORK IN PROGRESS.\n\nTorchVF is a unifying Python library for using vector fields for lightweight \nproposal-free instance segmentation. The TorchVF library provides generalizable\nfunctions to automate ground truth vector field computation, interpolation of\ndiscretely sampled vector fields, numeric integration solvers, clustering\nfunctions, and various other utilities. \n\nThis repository also provides all configs, code, and tools necessary to\nreproduce the results in my\n[article](https://github.com/ryanirl/torchvf/blob/main/article/first_draft.pdf)\non vector field based methods.\n\n## Quick Start\n\nFor anyone interested in learning about vector field based methods, see my\n[article](https://github.com/ryanirl/torchvf/blob/main/article/first_draft.pdf).\nTorchVF can be used to compute the instance segmentation given the semantic\nsegmentation and vector field via the following code: \n\n```Python\n# Consider we have a vector field `vf` and semantic segmentation `semantic`, \n# we can derive the instance segmentation via the following code: \n\nfrom torchvf.numerics import *\nfrom torchvf.utils import *\n\n# Step 1: Convert our discretely sampled vector field into continuous vector\n# field through bilinear interpolation. \nvf = interp_vf(vf, mode = "bilinear")\n\n# Step 2. Convert our semantic segmentation `semantic` into a set of\n# initial-values to be integrated through our vector field `vf`.\ninit_values = init_values_semantic(semantic, device = "cuda:0")\n\n# Step 3. Integrate our initial-values `init_values` through our vector field\n# `vf` for 25 steps with a step size of 0.1 using Euler\'s method for numeric \n# integration. \nsolutions = ivp_solver(\n    vf, \n    init_values, \n    dx = 0.1,\n    n_steps = 25,\n    solver = "euler"\n)[-1] # Get the final solution. \n\n# Clustering can only be done on the CPU. \nsolutions = solutions.cpu()\nsemantic = semantic.cpu()\n\n# Step 4. Cluster the integrated semantic points `solutions` to obtain the\n# instance segmentation. \ninstance_segmentation = cluster(\n    solutions, \n    semantic[0], \n    eps = 2.25,\n    min_samples = 15,\n    snap_noise = False\n)\n\n```\n\n## Supported Features\n\n<details>\n   <summary>Interpolators:</summary>\n\n</br>\n\n| Interpolator             | Implemented          |\n| ------------------------ | -------------------- |\n| Nearest Neighbor         | :white_check_mark:   |\n| Nearest Neighbor Batched | :white_check_square: |\n| Bilinear                 | :white_check_mark:   |\n| Bilinear Batched         | :white_check_mark:   |\n\n</details>\n\n<details>\n   <summary>Numeric Integration Solvers:</summary>\n\n</br>\n\n| Interpolator            | Implemented          |\n| ----------------------- | -------------------- |\n| Euler\'s Method          | :white_check_mark:   |\n| Midpoint Method         | :white_check_mark:   |\n| Runge Kutta (4th Order) | :white_check_mark:   |\n| Adaptive Dormand Prince | :white_check_square: |\n\n</details>\n\n<details>\n   <summary>Clustering Schemes:</summary>\n\n</br>\n\n| Interpolator            | Implemented          |\n| ----------------------- | -------------------- |\n| DBSCAN (Scikit-learn)   | :white_check_mark:   |\n| DCSCAN (PyTorch)        | :white_check_square: |\n| ...?                    | :white_check_square: | \n\n</details>\n\n<details>\n   <summary>Vector Field Computation:</summary>\n\n</br>\n\n| Interpolator           | Implemented          |\n| ---------------------- | -------------------- |\n| Truncated SDF + Kernel | :white_check_mark:   |\n| Affinity Derived       | :white_check_mark:   |\n| Omnipose               | :white_check_square: |\n| Centroid Based         | :white_check_square: | \n\n</details>\n\n<details>\n   <summary>Other Utilities:</summary>\n\n - Tiler wrapper for models. \n - Semantic -> euclidean conversion.\n - The IVP vector field loss function. \n - Tversky and Dice semantic loss functions. \n - Training and evalution scripts. \n - Various pretrained models on the BPCIS dataset.  \n - Modeling for the presented H1 and H2 models. \n - mAP IoU, F1, IoU metrics. \n\n</details>\n\n## Dependencies\n\nThe ultimate goal of TorchVF is to be solely dependent on PyTorch. Although at\nthe moment, the signed distance function computation relies on Seung Lab\'s\neuclidean distance transform [library](https://github.com/seung-lab/euclidean-distance-transform-3d)\nand the DBSCAN clustering implementation relies on Scikit-learn.  Furthermore,\nNumPy appears in various places (mAP IoU metric, clustering, ...).\n\n## Reproducability\n\nThis installation guide is for people who want to reproduce the results in my\n[article](https://github.com/ryanirl/torchvf/blob/main/article/first_draft.pdf)\non vector field based methods using TorchVF as-is. \n\nI have a PyPI library for TorchVF, though for now just clone the repository as \nthe API is a work in progress. \n\n### Installing the Weights\n\nWeights include H1 and H2 for the bacterial phase contrast, bacterial\nfluorescence, and worm subsets of the BPCIS dataset. And can be found\n[here](https://drive.google.com/drive/folders/14fvNNZkr4ewuy0-Q2mwjCX-fbMVS7X90?usp=sharing)\n(157.5 MB zipped | 185.5 MB unzipped). \n\nOnce you download the weights:\n - Unzip the file.\n - Replace the `torchvf/weights` file with the `torchvf_weights` file. \n - Rename `torchvf/torchvf_weights` to `torchvf/weights`.\n\n### Installing the BPCIS Dataset\n\nFirst, download the BPCIS dataset [here](http://www.cellpose.org/dataset_omnipose).\nThen setup the file system this way:\n\n```bash\n├── torchvf/\n├── data/\n│   └── bpcis/\n│       ├── bact_fluor_train/\n│       ├── bact_fluor_test/\n│       ├── bact_phase_train/\n│       ├── bact_phase_test/\n│       ├── worm_train/\n│       └── worm_test/\n├── weights/\n└── ***\n```\n\nIf you have cloned the library, downloaded the weights, and downloaded the\nBPCIS dataset you *should* be able to do `python3 eval.py --config_dir\n../weights/bact_fluor/h1/eval_config.py`. This will run evaluation on the\nbacterial fluorescence subset using the downloaded weights. \n\n## Usage\n\nWork in progress.\n\n## Citation\n\n```\n@article{TorchVF,\n   author = {Ryan Peters},\n   title = {TorchVF: Vector Fields for Instance Segmentation},\n   year = 2022\n}\n```\n\n## License\n\nDistributed under the Apache-2.0 license. See `LICENSE` for more information.\n\n\n\n\n\n',
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
