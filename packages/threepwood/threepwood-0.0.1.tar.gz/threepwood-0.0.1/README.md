# threepwood

![Tests](https://github.com/mc7h/threepwood/actions/workflows/tests.yml/badge.svg)

## Pipenv cheat sheet

```shell
# install local package in editable mode
pipenv install -e .

# install dependencies from pip
pipenv install

# install dev dependencies 
pipenv install --dev  

# freeze dependencies into requirements.txt
pipenv requirements > requirements.txt

# freeze dependencies into requirements.txt
pipenv requirements --dev-only > requirements_dev.txt
```