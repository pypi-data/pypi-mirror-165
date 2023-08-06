# Pyaphid (Experimental)

Pyaphid is a tool for detecting unwanted function calls in Python code.

## Installation and usage

Installation: `pip install pyaphid`

Usage: `python -m pyaphid <files and/or directories to analyze>` or `pyaphid <files and/or directories to analyze>`

### Configuration

Forbidden function calls can be configured via the `pyproject.toml`:

```toml
[tool.pyaphid]
forbidden = [
    "print",
    "pdb.run",
    "werkzeug.debug.*"
]
```

### CLI Options

- -n / --names: `Look-up all func calls and print their identifier`

## As a pre-commit hook

```yaml
- repo: https://github.com/jvllmr/pyaphid
    rev: v0.1.2
    hooks:
      - id: pyaphid
```



## Limitations

```python
# Pyaphid cannot work with star imports
from os.path import *
dirname(".") # undetected

# Pyaphid doesn't track assignments
my_print = print
my_print("Hello world") # undetected
```
