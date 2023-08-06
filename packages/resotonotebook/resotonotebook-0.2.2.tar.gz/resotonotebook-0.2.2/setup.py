# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resotonotebook']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.20,<0.21',
 'nbformat>=5.3.0,<6.0.0',
 'pandas-stubs>=1.2.0,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'plotly>=5.7.0,<6.0.0',
 'resotoclient>=0.1.6,<0.2.0']

setup_kwargs = {
    'name': 'resotonotebook',
    'version': '0.2.2',
    'description': 'Resoto Python client library',
    'long_description': '# resotonotebook\nSmall library for using Resoto with Jupyter Notebooks.\n\n## Installation\n\n```bash\npip install resotonotebook\n```\n\n## Usage\n\n```python\nfrom resotonotebook import ResotoNotebook\nrnb = ResotoNotebook("https://localhost:8900", None)\nrnb.search("is(instance)").groupby(["kind"])["kind"].count()\n```\n```\nkind\naws_ec2_instance        497\ndigitalocean_droplet      7\nexample_instance          2\ngcp_instance             12\nName: kind, dtype: int64\n```\n\nFor more see the notebook in the examples directory.\n',
    'author': 'Some Engineering Inc.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/someengineering/resotonotebook',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
