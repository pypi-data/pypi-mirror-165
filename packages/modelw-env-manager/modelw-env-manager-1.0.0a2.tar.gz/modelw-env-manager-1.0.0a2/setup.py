# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['env_manager']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0', 'python-dotenv>=0.11.0,<0.12.0']

setup_kwargs = {
    'name': 'modelw-env-manager',
    'version': '1.0.0a2',
    'description': 'A tool to simplify reading environment variables and .env files',
    'long_description': "# Model W &mdash; Env Manager\n\nThe goal of the env manager is to help managing the loading of environment\nvariables and Django settings (although this is not Django-dependent).\n\nTypical use is:\n\n```python\nfrom model_w.env_manager import EnvManager\n\n\nwith EnvManager() as env:\n    SOME_VALUE = env.get('SOME_VALUE', is_yaml=True, default=False)\n```\n",
    'author': 'Rémy Sanchez',
    'author_email': 'remy.sanchez@hyperthese.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ModelW/py-env-manager',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
