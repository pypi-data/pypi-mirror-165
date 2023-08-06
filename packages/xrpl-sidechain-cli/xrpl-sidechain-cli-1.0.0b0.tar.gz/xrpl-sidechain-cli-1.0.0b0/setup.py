# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sidechain_cli',
 'sidechain_cli.bridge',
 'sidechain_cli.misc',
 'sidechain_cli.server',
 'sidechain_cli.server.config',
 'sidechain_cli.utils']

package_data = \
{'': ['*'], 'sidechain_cli.server.config': ['templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'click>=8.1.3,<9.0.0',
 'httpx>=0.18.1,<0.19.0',
 'tabulate>=0.8.9,<0.9.0',
 'websockets>=10.3,<11.0',
 'xrpl-py>=1.7.0b0,<2.0.0']

entry_points = \
{'console_scripts': ['sidechain-cli = sidechain_cli.main:main']}

setup_kwargs = {
    'name': 'xrpl-sidechain-cli',
    'version': '1.0.0b0',
    'description': 'A CLI that helps you set up an XRPL sidechain.',
    'long_description': "# xrpl-sidechain-cli\n\n## Install\n\n```bash\npip install xrpl-sidechain-cli\n```\nNOTE: if you're looking at the repo before it's published, this won't work. Instead, you'll do this:\n```bash\ngit clone https://github.com/xpring-eng/sidechain-cli.git\ncd sidechain-cli\n# install poetry\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -\npoetry install\npoetry shell\n```\n\nInstall rippled and the xbridge witness.\n\nrippled: https://xrpl.org/install-rippled.html\n\nwitness: https://github.com/seelabs/xbridge_witness\n\n## Get started\n\n```bash\nexport XCHAIN_CONFIG_DIR={filepath where you want your config files stored}\nexport RIPPLED_EXE={rippled exe filepath}\nexport WITNESSD_EXE={witnessd exe filepath}\n./scripts/tutorial.sh\n```\n\nTo stop the servers:\n```bash\nsidechain-cli server stop --all\n```\n\n## Use Commands\n\n```bash\nsidechain-cli --help\n```\n\nEach subcommand also has a `--help` flag, to tell you what fields you'll need.\n",
    'author': 'Mayukha Vadari',
    'author_email': 'mvadari@ripple.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xpring-eng/sidechain-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
