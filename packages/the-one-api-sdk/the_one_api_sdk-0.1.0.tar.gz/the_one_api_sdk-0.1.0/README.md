The One API Python SDK
=================================

Python SDK for ["one API to rule them all"](https://the-one-api.dev/).

Description
-----------
The one api serves your needs regarding data about The Lord of the Rings, the epic books by J. R. R. Tolkien and the official movie adaptions by Peter Jackson.

This is a Python developer friendly development kit for querying the one api.

Development
-----------
1. Install poetry following: https://python-poetry.org/docs/
2. Create the env
```
poetry install
```

### Build the whl package
```
poetry build
```
output in dist/

### Testing
Run test with coverage report
```
poetry run pytest --cov
```

### Integration testing
Integration tests requires access token to the one api and the module to be installed locally.

1. first install theoneapisdk
2. Set the env ONEAPI_SDK_ACCESS_TOKEN='YOUR_TOKEN'
3. Run the integration tests from the package root folder

```
export ONEAPI_SDK_ACCESS_TOKEN=${access_token}; python -m pytest -v integration_tests
```

### python code formatter
Using black code formatter: https://black.readthedocs.io/en/stable/
```
poetry run black .
```

Install
-------

### pip

1. Install
```
python3 -m pip install TODO.
```


Usage
----


#### Init
Most of the api requires access_token you can set it with Env var
ONEAPI_SDK_ACCESS_TOKEN=<token>
Or in the configuration
```
import theoneapisdk as oneapi
oneapi.config.access_token = "TOKEN"
```

#### Get Books
Books don't require access_token
```
from theoneapisdk as oneapi
import theoneapisdk.books as books

books.get_books()
```

#### Get Movies
Movies require access_token. If not provided
```
from theoneapisdk as oneapi
import theoneapisdk.movies as movies

movies = movies.get_movies()
quote = movies.quotes
```

###

## Authors

**Yair Rozenberg** 

## License

This project is licensed under the Apache 2.0 [LICENSE](LICENSE) file for details

## Acknowledgments
