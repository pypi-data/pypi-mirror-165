# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deciphon_api',
 'deciphon_api.api',
 'deciphon_api.core',
 'deciphon_api.models',
 'deciphon_api.resources']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles',
 'bcbio-gff',
 'biopython',
 'deciphon-sched>=0.0.4',
 'fasta-reader>=1.0.3',
 'fastapi',
 'loguru',
 'pooch',
 'pydantic[dotenv]',
 'python-multipart',
 'typer',
 'uvicorn[standard]']

entry_points = \
{'console_scripts': ['deciphon-api = deciphon_api.console:run']}

setup_kwargs = {
    'name': 'deciphon-api',
    'version': '0.4.3',
    'description': 'RESTful API for Deciphon scheduler',
    'long_description': '# deciphon-api\n\n## Dependencies\n\nIf you happen to be using a supported Linux environment (which is likely the case),\nyou would need:\n\n- [Python](https://www.python.org) >=3.8\n- [Pipx](https://pypa.github.io/pipx/) for easy installation and environment isolation. Feel free to use [Pip](https://pip.pypa.io/en/stable/) instead though.\n\n## Usage\n\nGenerate a configuration file:\n\n```bash\npipx run deciphon-api generate-config > .env\n```\n\nTweak `.env` as needed, and then run\n\n```bash\npipx run deciphon-api start\n```\n\n## Development\n\nMake sure you have [Poetry](https://python-poetry.org/docs/).\n\nEnter\n\n```bash\npoetry install\npoetry shell\n```\n\nto setup and activate a Python environment associated with the project.\nThen enter\n\n```bash\nuvicorn deciphon_api.main:app.api --reload\n```\n\nto start the API.\n\nTests can be performed by entering\n\n```bash\npytest\n```\n\nwhile the corresponding Python environment created by Poetry is active.\n\n## Settings\n\nCopy the file [.env.example](.env.example) to your working directory and rename it to `.env`.\nEdit it accordingly.\nThe rest of the configuration can be tuned by `uvicorn` options.\n',
    'author': 'Danilo Horta',
    'author_email': 'danilo.horta@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/EBI-Metagenomics/deciphon-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
