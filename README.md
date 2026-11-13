# batutils - Team Batcave Python Toolkit

[![PyPI](https://img.shields.io/pypi/v/batutils)](https://pypi.org/project/batutils/)

A grab-bag of small, dependency-free Python utilities for working with dates
and times and for everyday type juggling, originally written by Team Batcave
at CCP Games.

This is a fork of [`ccptools`](https://github.com/ccpgames/ccptools), kept alive
beyond the original team's lifespan. Our two most commonly used internal packages,
`datetimeutils` and `typeutils`, had names that were too generic for PyPI and were
used in 80-90% of our other projects, so they were smooshed together into one
package.

```bash
pip install batutils
```

Requires Python 3.10 or newer.

## What's inside

| Submodule | Formerly | What it is | Docs |
|-----------|----------|------------|------|
| `batutils.dtu` | `datetimeutils` | Casting, parsing, formatting and shortcuts for date/time values | [Date/Time Utils](batutils/dtu/README.md) |
| `batutils.tpu` | `typeutils` | Safe type evaluation, nested dict/list helpers, enums, singletons, serializers and more | [Type Utils](batutils/tpu/README.md) |
| `batutils.structs` | | One-line "usual imports" for your modules | [below](#common-imports) |

**Looking for a specific function?** Use the task-oriented
[Public API index](docs/api-index.md).

## Quick taste

```python
from batutils import dtu
from batutils.tpu.casting import int_eval, bool_eval
from batutils.tpu.iters import nested_get

dtu.any_to_datetime('2024-04-02 13:47:25')   # datetime(2024, 4, 2, 13, 47, 25)
dtu.agostr(dtu.ago(days=5))                  # '5 days'
int_eval('0x10')                             # 16
bool_eval('Yes')                             # True
nested_get({'a': {'b': [1, 2, 3]}}, ('a', 'b', -1))   # 3
```

## Common imports

`from batutils.structs import *` pulls in the imports that nearly every file in
our projects needs:

```python
from typing import *       # for type annotations
import abc                 # interfaces (Abstract Base Classes)
import dataclasses         # dataclass structs
import decimal             # anything involving money
import enum                # also used for struct creation
import logging             # used pretty much everywhere
import re                  # used surprisingly frequently
import time                # very commonly used
```

`datetime` itself is not included. Instead you get the date/time aliases from
`batutils.dtu.structs.aliases`:

```python
Date = datetime.date
Time = datetime.time
Datetime = datetime.datetime
TimeDelta = datetime.timedelta
TzInfo = datetime.tzinfo
TimeZone = datetime.timezone
```

Plus a few of the most commonly used helpers from the type utils:

- the `Singleton` metaclass
- `Empty`, `EmptyDict` and `if_empty`
- the `EnumEx` base class for enums (adds the `from_any` class method)

So one line covers roughly 90% of the imports we need in any given file:

```python
from batutils.structs import *
```

## Changes from `ccptools`

The `legacyapi` submodule has been removed. See the [changelog](CHANGELOG.md)
for the full history.

## Contributing and license

Issues and pull requests are welcome at
[github.com/doddi79/batutils](https://github.com/doddi79/batutils). Released
under the [MIT License](LICENSE).
