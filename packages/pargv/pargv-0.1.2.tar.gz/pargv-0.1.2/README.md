# pargv

Parse command line arguments into a list of args and a dict of kwargs.

# Installation

```python
pip install pargv
```

# Usage

By default, `pargv.parse_args()` uses `sys.argv` as command line arguments.
It can be used in the following way.

```python
from pargv import parse_args

args, kwargs = parse_args()
```

The arguments to be parsed can also be specified manually:

```python
from pargv import parse_args

args, kwargs = parse_args(argv=['pargv.py', '--name=pargv'])
```

# Specification

`parse_args` parses arguments in the following way, assuming the following command line arguments (`sys.argv`): `['/pargv/pargv.py', 'command', 'positional', '--flag', '--optional=value', 'test', '--output-file', 'filename', '-ab', 'one', 'two']`

By calling `args, kwargs = parse_args()`, this would return the following list and dict:

```python
args = ['/pargv/pargv.py', 'command', 'positional']
kwargs = {
        'flag': True,
        'optional': ['value', 'test'],
        'output_file': 'filename',
        'a': True,
        'b': ['one', 'two'],
    }
```

## Basic behaviour

- All arguments before the first option (starting with a hyphen) are considered positional arguments (`args`)
- All other arguments are considered optional keyword arguments (`kwargs`)
- Optional arguments without leading hyphens are considered as values to preceding keyword arguments
- One value of an option is stored as a string, multiple values are stored as a list
- Flags are stored with the value `True` in the dict
- Up to 2 leading hyphens are stripped from options, all other hyphens are converted into underscores (`---test-this-` would become the key `_test_this_` in the dict)
