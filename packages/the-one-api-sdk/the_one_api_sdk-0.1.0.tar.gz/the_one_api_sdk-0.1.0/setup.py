# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['theoneapisdk']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'the-one-api-sdk',
    'version': '0.1.0',
    'description': 'the_one_api_sdk is a Python client implemented most of the APIs for the-one-api.dev.',
    'long_description': 'The One API Python SDK\n=================================\n\nPython SDK for ["one API to rule them all"](https://the-one-api.dev/).\n\nDescription\n-----------\nThe one api serves your needs regarding data about The Lord of the Rings, the epic books by J. R. R. Tolkien and the official movie adaptions by Peter Jackson.\n\nThis is a Python developer friendly development kit for querying the one api.\n\nDevelopment\n-----------\n1. Install poetry following: https://python-poetry.org/docs/\n2. Create the env\n```\npoetry install\n```\n\n### Build the whl package\n```\npoetry build\n```\noutput in dist/\n\n### Testing\nRun test with coverage report\n```\npoetry run pytest --cov\n```\n\n### Integration testing\nIntegration tests requires access token to the one api and the module to be installed locally.\n\n1. first install theoneapisdk\n2. Set the env ONEAPI_SDK_ACCESS_TOKEN=\'YOUR_TOKEN\'\n3. Run the integration tests from the package root folder\n\n```\nexport ONEAPI_SDK_ACCESS_TOKEN=${access_token}; python -m pytest -v integration_tests\n```\n\n### python code formatter\nUsing black code formatter: https://black.readthedocs.io/en/stable/\n```\npoetry run black .\n```\n\nInstall\n-------\n\n### pip\n\n1. Install\n```\npython3 -m pip install TODO.\n```\n\n\nUsage\n----\n\n\n#### Init\nMost of the api requires access_token you can set it with Env var\nONEAPI_SDK_ACCESS_TOKEN=<token>\nOr in the configuration\n```\nimport theoneapisdk as oneapi\noneapi.config.access_token = "TOKEN"\n```\n\n#### Get Books\nBooks don\'t require access_token\n```\nfrom theoneapisdk as oneapi\nimport theoneapisdk.books as books\n\nbooks.get_books()\n```\n\n#### Get Movies\nMovies require access_token. If not provided\n```\nfrom theoneapisdk as oneapi\nimport theoneapisdk.movies as movies\n\nmovies = movies.get_movies()\nquote = movies.quotes\n```\n\n###\n\n## Authors\n\n**Yair Rozenberg** \n\n## License\n\nThis project is licensed under the Apache 2.0 [LICENSE](LICENSE) file for details\n\n## Acknowledgments\n',
    'author': 'Yair Rozenberg',
    'author_email': 'yairrose@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
