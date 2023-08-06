# DataDict

_Treat dataclasses like dictionaries_

[![v1.0.0](https://img.shields.io/pypi/v/datadict.svg)](https://pypi.org/project/datadict/)
[![Python versions](https://img.shields.io/pypi/pyversions/datadict.svg)](https://pypi.org/project/datadict/)
[![Tests](https://img.shields.io/github/workflow/status/gahjelle/datadict/tests?label=tests)](https://github.com/realpython/codetiming/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Interrogate](https://raw.githubusercontent.com/gahjelle/datadict/master/interrogate_badge.svg)](https://interrogate.readthedocs.io/)


## Installing DataDict

DataDict is available at [PyPI](https://pypi.org/project/datadict/). You can install it using Pip:

    $ python -m pip install datadict


## Using DataDict

You can use a DataDict `dataclass` as a drop-in replacement for `dataclasses.dataclass` in the standard library:

```python
from datadict import dataclass

@dataclass(order=True)
class Point:
    x: int
    y: int
```

For instances of the new data class, you can access attributes using square brackets, similar to dictionary access:

```python
>>> point = Point(1, 2)
>>> point
Point(x=1, y=2)

>>> point.x
1
>>> point["x"]
1

>>> point["y"] = 3
>>> point
Point(x=1, y=3)
```

You can also convert the dataclass instance to a proper dictionary:

```python
>>> point.asdict()
{'x': 1, 'y': 3}
```


## Installing From Source

You can always download the [latest version of DataDict from GitHub](https://github.com/gahjelle/datadict). DataDict uses [Flit](https://flit.pypa.io/) as a build tool.

To install DataDict from the downloaded source, run Flit through `pip`:

    $ python -m pip install .

If you want to change and play with the DataDict source code, you should install it in editable mode:

    $ python -m pip install -w .[dev,test]
