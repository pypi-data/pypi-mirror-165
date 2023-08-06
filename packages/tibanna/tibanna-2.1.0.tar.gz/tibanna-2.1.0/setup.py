# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['awsf3', 'tibanna', 'tibanna.lambdas']

package_data = \
{'': ['*']}

install_requires = \
['Benchmark-4dn>=0.5.8,<0.6.0',
 'boto3>=1.9.0,<2.0.0',
 'botocore>=1.12.1,<2.0.0',
 'python-lambda-4dn==0.12.3',
 'requests>=2.22.0,<3.0.0',
 'tomlkit>=0.10.0,<0.11.0',
 'urllib3>=1.24,<2.0']

entry_points = \
{'console_scripts': ['awsf3 = awsf3.__main__:main',
                     'tibanna = tibanna.__main__:main']}

setup_kwargs = {
    'name': 'tibanna',
    'version': '2.1.0',
    'description': 'Tibanna runs portable pipelines (in CWL/WDL) on the AWS Cloud.',
    'long_description': "# Tibanna\n\n[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/) [![Build Status](https://travis-ci.org/4dn-dcic/tibanna.svg?branch=master)](https://travis-ci.org/4dn-dcic/tibanna) [![Code Quality](https://api.codacy.com/project/badge/Grade/d2946b5bc0704e5c9a4893426a7e0314)](https://www.codacy.com/app/4dn/tibanna?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=4dn-dcic/tibanna&amp;utm_campaign=Badge_Grade) [![Test Coverage](https://api.codacy.com/project/badge/Coverage/d2946b5bc0704e5c9a4893426a7e0314)](https://www.codacy.com/app/4dn/tibanna?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=4dn-dcic/tibanna&amp;utm_campaign=Badge_Coverage) [![Documentation Status](https://readthedocs.org/projects/tibanna/badge/?version=latest)](https://tibanna.readthedocs.io/en/latest/?badge=latest)\n\n***\n\nTibanna runs portable pipelines (in CWL/WDL/Snakemake/shell) on the AWS Cloud.\n\n<br>\n\nInstall Tibanna.\n```bash\npip install tibanna\n```\n\n<br>\n\nUse CLI to set up the cloud component and run workflow.\n```bash\n# Deploy Unicorn to the Cloud (Unicorn = serverless scheduler/resource allocator).\ntibanna deploy_unicorn --usergroup=mygroup\n\n# Run CWL/WDL workflow on the Cloud.\ntibanna run_workflow --input-json=myrun.json\n```\n\n<br>\n\nAlternatively, use Python API.\n\n```python\nfrom tibanna.core import API\n\n# Deploy Unicorn to the Cloud.\nAPI().deploy_unicorn(usergroup='mygroup')\n\n# Run CWL/WDL workflow on the Cloud.\nAPI().run_workflow(input_json='myrun.json')\n```\n\n<br>\n\n---\nNote: Starting `0.8.2`, Tibanna supports local CWL/WDL files as well as shell commands and Snakemake workflows.\n\nNote 2: As of Tibanna version `2.0.0`, Python 3.6 is no longer supported. Please switch to Python 3.8! Python 3.7 is also supported as a fallback, but please prefer 3.8 if you can.\n\nNote 3: Starting `0.8.0`, one no longer needs to `git clone` the Tibanna repo. \n* Please switch from `invoke <command>` to `tibanna <command>`! \n* We also renovated the Python API as an inheritable class to allow development around tibanna.\n\n\nFor more details, see Tibanna [**Documentation**](http://tibanna.readthedocs.io/en/latest).\n* Also check out our [**paper in _Bioinformatics_**](https://doi.org/10.1093/bioinformatics/btz379).\n* A preprint can also be found on [**biorxiv**](https://www.biorxiv.org/content/10.1101/440974v3).\n\n",
    'author': '4DN-DCIC Team',
    'author_email': 'support@4dnucleome.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/4dn-dcic/tibanna',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
