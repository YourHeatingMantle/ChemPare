# ChemPare
[![Python application](https://github.com/jhyland87/ChemPare/actions/workflows/python-app.yml/badge.svg)](https://github.com/jhyland87/ChemPare/actions/workflows/python-app.yml)
### Intro
Compares prices from chemical vendors that sell to individuals and residential addresses.

> _*Note:* This project is a work in progress, not yet in Beta mode_


### Example Usage
![chemparecli example](./assets/images/chempare-demo.gif)

---

### How does it work
Magic, mostly.

---

### Installation

#### Python Enviroment Setup

##### Try using the Makefile (OSX)

1. Checkout this repo
```bash
git clone https://github.com/YourHeatingMantle/ChemPare.git
```

2. Go to repo directory and run Makefile
```bash
cd ChemPare
make install
```

3. Run script
```bash
make run
```

##### Manual setup

1. Install Python 3.13

2. Checkout this repo
```bash
git clone https://github.com/YourHeatingMantle/ChemPare.git
```

3. Create pyenv environment

Optional. ([documentation here](https://packaging.python.org/en/latest/tutorials/installing-packages/#optionally-create-a-virtual-environment)).
```bash
cd ./ChemPare
```

4. Go to the folder and create/activate a python3 env

<small>_On Linux/OSX:_</small>

```bash
python3 -m venv .venv
source ./.venv/bin/activate
python3 --version
# Python 3.13.2 
```

<small>_On Windows:_</small>

```powershell
# tbd....
```

5. Install project packages
```bash
pip install -e .
```

6. Run chempare command, and provide a chemical name or CAS.

```bash
# Main script
chemparemain

# CLI Script
chemparecli
```

## Unit Tests

To get the unit tests to fire, you need to install the dev packages.

<small>__On OSX:__</small>

If you're on OSX, just run `make install-dev` then `make test`.

<small>__Other OS:__</small>

1. Follow the regular install steps
2. Run the following:

```bash
# Don't forget to create/activate a local venv environment if you have it
# source ./.venv/bin/activate
pip install --upgrade pip
pip install -e .[test]

```
3. Run the below to execute all unit tests in `./tests` directory:

```bash
pytest -c pyproject.toml
```

## Development

```bash
pip install -e .[dev]
pre-commit install
```

If you're doing development work and using VSCode, then install some useful Python extensions using the [code command](https://code.visualstudio.com/docs/setup/mac#_launch-vs-code-from-the-command-line):

```bash
code --install-extension charliermarsh.ruff
code --install-extension franneck94.vscode-python-config
code --install-extension gydunhn.python3-essentials
code --install-extension leonhard-s.python-sphinx-highlight
code --install-extension leonhard-s.python-sphinx-highlight
code --install-extension mintlify.document
code --install-extension ms-python.black-formatter
code --install-extension ms-python.debugpy
code --install-extension ms-python.flake8
code --install-extension ms-python.isort
code --install-extension ms-python.mypy-type-checker
code --install-extension ms-python.pylint
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension njpwerner.autodocstring
code --install-extension njqdev.vscode-python-typehint
code --install-extension rodolphebarbanneau.python-docstring-highlighter
code --install-extension sr-team.lcov-generator
code --install-extension visualstudioexptteam.vscodeintellicode
code --install-extension vlaraort.opencoverage
```

Running pre-commit hooks manually
```bash
pre-commit run pyupgrade --all-files
pre-commit run trailing-whitespace --all-files
pre-commit run reorder-python-imports --all-files
```

mypy
```bash
mypy --exclude dev --strict --ignore-missing-imports --allow-untyped-defs src/
```

## Suppliers To Add
- https://www.jk-sci.com
- https://www.chemworld.com/searchresults.asp?Search=potassium&Submit=
- https://www.sciencecompany.com/Search?Keywords=acid&ManufacturerId=0&categoryId=670&PageSize=48
