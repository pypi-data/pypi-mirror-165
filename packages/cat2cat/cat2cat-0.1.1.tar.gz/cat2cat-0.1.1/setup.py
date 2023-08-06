# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cat2cat', 'cat2cat.data']

package_data = \
{'': ['*']}

install_requires = \
['importlib-resources>=5.9.0,<6.0.0',
 'numpy>=1.23.1,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'scikit-learn>=1.1.2,<2.0.0',
 'scipy>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'cat2cat',
    'version': '0.1.1',
    'description': 'Unifying an inconsistently coded categorical variable in a panel/longtitudal dataset.',
    'long_description': '# cat2cat \n<a href=\'https://github.com/polkas/py-cat2cat\'><img src=\'https://raw.githubusercontent.com/Polkas/cat2cat/master/man/figures/cat2cat_logo.png\' align="right" width="200px" style="margin:5px;"/></a>\n[![Build Status](https://github.com/polkas/py-cat2cat/workflows/ci/badge.svg)](https://github.com/polkas/py-cat2cat/actions)\n[![codecov](https://codecov.io/gh/Polkas/py-cat2cat/branch/main/graph/badge.svg)](https://codecov.io/gh/Polkas/py-cat2cat)\n\nUnifying an inconsistently coded categorical variable in a panel/longtitudal dataset.\n\n## Installation\n\n```bash\n$ pip install cat2cat\n```\n\n## Usage\n\nFor more examples and descriptions please vist [**the example notebook**](https://py-cat2cat.readthedocs.io/en/latest/example.html)\n\n### load example data\n\n```python\n# cat2cat datasets\nfrom cat2cat.datasets import load_trans, load_occup\ntrans = load_trans()\noccup = load_occup()\n```\n\n### Low-level functions\n\n```python\n# Low-level functions\nfrom cat2cat.mappings import get_mappings, get_freqs, cat_apply_freq\n\nmappings = get_mappings(trans)\ncodes_new = occup.code[occup.year == 2010].values\nfreqs = get_freqs(codes_new)\nmapp_new_p = cat_apply_freq(mappings["to_new"], freqs)\nmappings["to_new"][\'3481\']\nmapp_new_p[\'3481\']\n```\n\n### cat2cat function\n\n```python\nfrom cat2cat import cat2cat\nfrom cat2cat.dataclass import cat2cat_data, cat2cat_mappings, cat2cat_ml\n\nfrom pandas import DataFrame\n\no_old = occup.loc[occup.year == 2008, :].copy()\no_new = occup.loc[occup.year == 2010, :].copy()\n\n# dataclasses a core arguments for cat2cat function\ndata = cat2cat_data(old = o_old, new = o_new, "code", "code", "year")\nmappings = cat2cat_mappings(trans, "backward")\n\nc2c = cat2cat(data, mappings)\ndata_final = concat([c2c["old"], c2c["new"]])\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`cat2cat` was created by Maciej Nasinski. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`cat2cat` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Maciej Nasinski',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
