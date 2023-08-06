# py-inception
## Description
Python introspection tool.

Generate html page with information about object and classes.

![Screen](/doc/example.png)

## Installation
```
pip install py-inception
```

## Usage

`py_inception.extract(varlist, out=filename)`
* `varlist` - list of variables for inspect
* `filename` - output file name (must ends with ".html")

example:
```
import py_inception
py_inception.extract([__builtins__,], out="test.html")
```