# qspreadsheet

Show and edit pandas DataFrame in GUI with PySide2.

![tests](https://github.com/stanislavsabev/qspreadsheet/actions/workflows/tests.yaml/badge.svg)

---

## Usage

### Install

```text
git clone https://github.com/stanislavsabev/qspreadsheet.git
```

```text
cd qspreadsheet
pip install .
```

### See example

`python src/example.py`.

## Development Setup

Setup virtual environment and activate it.

### Linux / Mac

```bash
python -m venv .venv

```

``` bash
source ./.venv/bin/activate
```

### Windows

```batch
.\venv\Scripts\activate.bat
```

### Install requirements

```text
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Install as editable package

```text
pip install -e .
```

## Local development

Run `pytest`, `flake8` and `mypy` in a command line...

```text
$ pytest
...
tests\test_imports.py ......x
[100%]

----------- coverage: platform win32, python 3.7.9-final-0 -----
Name                               Stmts   Miss  Cover
------------------------------------------------------
src\qspreadsheet\__init__.py           0      0   100%
src\qspreadsheet\constants.py          3      0   100%
src\qspreadsheet\qt.py                 7      0   100%
src\qspreadsheet\table_view.py        16     10    38%
src\qspreadsheet\table_widget.py      24      0   100%
src\qspreadsheet\types.py              9      0   100%
------------------------------------------------------
TOTAL                                 59     10    83%


======= 13 passed, 1 xfailed, 1 warning in 1.10s ===============

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
