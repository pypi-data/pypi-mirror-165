# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['featurebyte']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'featurebyte',
    'version': '0.0.1a1',
    'description': 'Python Library for FeatureOps',
    'long_description': '# featurebyte\n\n<div align="center">\n\n[![Build status](https://github.com/featurebyte/featurebyte/workflows/build/badge.svg?branch=main&event=push)](https://github.com/featurebyte/featurebyte/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/featurebyte.svg)](https://pypi.org/project/featurebyte/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/featurebyte/featurebyte/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/featurebyte/featurebyte/blob/main/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/featurebyte/featurebyte/releases)\n[![License](https://img.shields.io/github/license/featurebyte/featurebyte)](https://github.com/featurebyte/featurebyte/blob/main/LICENSE)\n![Coverage Report](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/kchua78/773e2960183c0a6fe24c644d95d71fdb/raw/coverage.json)\n\nManage and serve Machine Learning Features for Data Science applications\n\n</div>\n\n## Installation\n\n```bash\npip install -U featurebyte\n```\n\nThen you can run\n\n```bash\nfeaturebyte --help\n```\n\n### Install from source\n\nCheckout the featurebyte repo:\n```bash\ngit clone git@github.com:featurebyte/featurebyte.git && cd featurebyte\n```\n\nIf you don\'t have `Poetry` installed run:\n\n```bash\nmake poetry-download\n```\n\nInstall module:\n\n```bash\nmake install\n```\n\n## 📝 Documentation\n\nRead the latest [documentation](https://featurebyte.github.io/featurebyte/).\n\n## 🚀 Features\n\n- Supports for `Python 3.8` and higher.\n\n## 📈 Releases\n\nYou can see the list of available releases on the [GitHub Releases](https://github.com/featurebyte/featurebyte/releases) page.\nReleases are versioned using the [Semantic Versions](https://semver.org/) specification.\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/featurebyte/featurebyte)](https://github.com/featurebyte/featurebyte/blob/main/LICENSE)\n\nThis project is licensed under the terms of the `Apache Software License 2.0` license. See [LICENSE](https://github.com/featurebyte/featurebyte/blob/main/LICENSE) for more details.\n\n## 📃 Citation\n\n```bibtex\n@misc{featurebyte,\n  author = {FeatureByte},\n  title = {Python Library for FeatureOps},\n  year = {2022},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/featurebyte/featurebyte}}\n}\n```\n\n## Issues Reporting\nRequest a feature or report a bug using [Github Issues](https://github.com/featurebyte/featurebyte/issues).\n\n## Contributing\nAll contributions are welcomed. Please adhere to the [CODE_OF_CONDUCT](https://github.com/featurebyte/featurebyte/blob/main/CODE_OF_CONDUCT.md) and read the\n[Developer\'s Guide](https://github.com/featurebyte/featurebyte/blob/main/CONTRIBUTING.md) to get started.\n\n## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)\n',
    'author': 'FeatureByte',
    'author_email': 'it-admin@featurebyte.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/featurebyte/featurebyte',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
