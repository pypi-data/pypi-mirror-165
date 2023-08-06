# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycountrycodes',
 'pycountrycodes.core',
 'pycountrycodes.countries_3166_1',
 'pycountrycodes.subdivisions_3166_2']

package_data = \
{'': ['*'], 'pycountrycodes': ['iso/*']}

install_requires = \
['pydantic>=1.9.2,<2.0.0', 'rapidfuzz>=2.5.0,<3.0.0', 'tox>=3.25.1,<4.0.0']

setup_kwargs = {
    'name': 'pycountrycodes',
    'version': '0.1.0',
    'description': 'Python package that replicates the ISO-3166 and ISO-3166-2 standards.',
    'long_description': "![ci](https://github.com/luizhenriquelongo/pyiso3166/actions/workflows/ci.yml/badge.svg)\n[![codecov](https://codecov.io/gh/luizhenriquelongo/pyiso3166/branch/master/graph/badge.svg?token=53G6ZN5K2E)](https://codecov.io/gh/luizhenriquelongo/pyiso3166)\n\n# PyCountryCodes\n\nPyCountryCodes is a Python library for dealing with the ISO 3166-1 and ISO 3166-2 Standards in a simple way.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install `pycountrycodes`.\n\n```bash\npip install pycountrycodes\n```\n\n## Usage\n\n### ISO 3166-1\n\n```python\nfrom pycountrycodes import countries\n\n# Go through the full list of countries available.\nfor country in countries:\n    # prints the country name\n    print(country.name)\n\n# returns a Country object if the given criteria matches.\ncountries.get(name='United Kingdom')\ncountries.get(alpha_2='GB')\ncountries.get(alpha_3='GBR')\n\n# returns a list of Country options fot the given query using fuzzy search.\ncountries.search('United Kingdom')\n\n# returns a list of Country options fot the given query using fuzzy search \n# using the match_score_cutoff to filter the list and only return results with\n# match_score greater or equal to 70.\ncountries.search('United Kingdom', match_score_cutoff=70)\n```\n\n### ISO 3166-2\n\n```python\nfrom pycountrycodes import subdivisions\n\n# Go through the full list of subdivisions available.\nfor subdivisions in subdivisions:\n    # prints the subdivision name\n    print(subdivisions.name)\n\n# returns a Subdivision object if the given criteria matches.\nsubdivisions.get(code='US-NY')\n\n# returns a list of Subdivision objects if the given criteria matches.\n# for name, type and country_code, this method will return a list of options since\n# there can be multiples Subdivision objects with the same attribute values.\nsubdivisions.get(name='New York')  # returns all Subdivision where obj.name is 'New York'\nsubdivisions.get(type='Province')  # returns all Subdivision where obj.type is 'Province'\nsubdivisions.get(country_code='GB')  # returns all Subdivision where obj.country_code is 'GB'\n\n# returns a list of Subdivisions options fot the given query using fuzzy search.\nsubdivisions.search('New York')\n\n# returns a list of Country options fot the given query using fuzzy search \n# using the match_score_cutoff to filter the list and only return results with\n# match_score greater or equal to 70.\nsubdivisions.search('New York', match_score_cutoff=70)\n```\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n",
    'author': 'Luiz Henrique Longo',
    'author_email': 'longo.luizh@gmail.com',
    'maintainer': 'Luiz Henrique Longo',
    'maintainer_email': 'longo.luizh@gmail.com',
    'url': 'https://github.com/luizhenriquelongo/pyiso3166',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
