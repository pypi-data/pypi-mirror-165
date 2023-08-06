# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cbdf_api']

package_data = \
{'': ['*']}

install_requires = \
['tqdm==4.62.3']

entry_points = \
{'console_scripts': ['generate-templates = cbdf_api.generate_templates:main']}

setup_kwargs = {
    'name': 'cbdf-api',
    'version': '3.0.3',
    'description': 'The API to accomodate creation of custom components integrateable into the cbdf from AICURA medical.',
    'long_description': '# cbdf_api\n\nThe API to accomodate creation of custom components integrateable into the cbdf as part of the AICURA platform.\n\n# Features\n\n\n# Credits\n\nThis package was created with Cookiecutter and the Aicura python package template.\n - Cookiecutter: https://github.com/audreyr/cookiecutter\n - Aicura python package template: https://github.com/aicuramedical/custom-components-template',
    'author': 'Christian Stur',
    'author_email': 'christian.stur@aicura-medical.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
