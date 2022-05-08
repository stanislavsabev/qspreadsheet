# qspreadsheet

Show and edit pandas DataFrame in GUI with PySide2.

![tests](https://github.com/stanislavsabev/qspreadsheet/actions/workflows/tests.yaml/badge.svg)

---

## Installation

```text
git clone https://github.com/stanislavsabev/qspreadsheet.git
```

```text
cd qspreadsheet
pip install .
```

---
---

## Development Setup

Clone this repo.

```text
git clone https://github.com/stanislavsabev/qspreadsheet.git
cd qspreadsheet
```

Setup virtual environment and activate it.

```text
python -m venv venv

source ./venv/bin/activate # Linux / Mac
.\venv\Scripts\activate.bat # Windows
```

Install requirements.

```text
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Install as editable package.

```text
pip install -e .
```

## Local development

Run `pytest`, `flake8` and `mypy` in a command line...

```text
$ pytest
...
tests\test_start.py .
[100%]

----------- coverage: platform win32, python 3.9.2-final-0 -----------
Name                             Stmts   Miss  Cover
----------------------------------------------------
src\qspreadsheet\__init__.py       0      0   100%
src\qspreadsheet\start.py          2      0   100%
----------------------------------------------------
TOTAL                                2      0   100%


========================================================================= 1 passed in 0.11s ===
```

```text
$ mypy src
Success: no issues found in 6 source files

$ flake8 src tests
0
```

..or using `tox`

(Change _py37_ according to your python version)

```text
$ tox -e py37,mypy,flake8
...
______________________________________________________________________________ summary ___
  py37: commands succeeded
  mypy: commands succeeded
  flake8: commands succeeded
  congratulations :)
```
