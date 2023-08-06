# potc_dict

[![PyPI](https://img.shields.io/pypi/v/potc-dict)](https://pypi.org/project/potc-dict/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/potc-dict)](https://pypi.org/project/potc-dict/)

[![Code Test](https://github.com/potc-dev/potc-dict/workflows/Code%20Test/badge.svg)](https://github.com/potc-dev/potc-dict/actions?query=workflow%3A%22Code+Test%22)
[![Package Release](https://github.com/potc-dev/potc-dict/workflows/Package%20Release/badge.svg)](https://github.com/potc-dev/potc-dict/actions?query=workflow%3A%22Package+Release%22)
[![codecov](https://codecov.io/gh/potc-dev/potc-dict/branch/main/graph/badge.svg?token=XJVDP4EFAT)](https://codecov.io/gh/potc-dev/potc-dict)

[![GitHub stars](https://img.shields.io/github/stars/potc-dev/potc-dict)](https://github.com/potc-dev/potc-dict/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/potc-dev/potc-dict)](https://github.com/potc-dev/potc-dict/network)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/potc-dev/potc-dict)
[![GitHub issues](https://img.shields.io/github/issues/potc-dev/potc-dict)](https://github.com/potc-dev/potc-dict/issues)
[![GitHub pulls](https://img.shields.io/github/issues-pr/potc-dev/potc-dict)](https://github.com/potc-dev/potc-dict/pulls)
[![Contributors](https://img.shields.io/github/contributors/potc-dev/potc-dict)](https://github.com/potc-dev/potc-dict/graphs/contributors)
[![GitHub license](https://img.shields.io/github/license/potc-dev/potc-dict)](https://github.com/potc-dev/potc-dict/blob/master/LICENSE)

A simple demo of `potc` plugin, which can make the dict prettier.

## Installation

You can simply install it with `pip` command line from the official PyPI site.

```shell
pip install potc-dict
```

Or install this  plugin by source code

```shell
git clone https://github.com/potc-dev/potc-dict.git
cd potc-dict
pip install .
```

## Effect show

We prepare a python script named `test_data.py`, like this

```python
import math

b = {
    'a': {'a': 3, 'b': None, 'c': math.e},
    'b': (3, 4, 'dfg'),
    'x0': {'a': 3, '02': 4, None: 2},
}

```

Before the installation mentioned above, we try to export the `b` in `test_data.py` by the following CLI command

```shell
potc export -v 'test_data.b'
```

We can get this dumped source code.

```python
import math

__all__ = ['b']
b = {
    'a': {
        'a': 3,
        'b': None,
        'c': math.e
    },
    'b': (3, 4, 'dfg'),
    'x0': {
        'a': 3,
        '02': 4,
        None: 2
    }
}
```

BUT, after the installation, **we try the CLI command which is exactly the same again, we get the new code**

```python
import math
from builtins import dict

__all__ = ['b']
b = dict(a=dict(a=3, b=None, c=math.e),
         b=(3, 4, 'dfg'),
         x0={
             'a': 3,
             '02': 4,
             None: 2
         })
```

That is all of this demo. **When you need to build your own plugin, maybe this demo can help you :smile:.**



