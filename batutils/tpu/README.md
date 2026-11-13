# Team Batcave Python Type Utils

Helpers for everyday type juggling: safe casting, nested dict/list access,
enums, singletons, serialization and a few introspection tools.

`batutils.tpu` has no top-level re-exports. Import the subpackage or the name
from its subpackage:

```python
from batutils.tpu import iters
from batutils.tpu.casting import int_eval, bool_eval, enum_eval
from batutils.tpu.iters import nested_get, group_by
from batutils.tpu.structs.singleton import Singleton
```

## Subpackages

| Subpackage | Contents |
|------------|----------|
| `casting` | `int_eval`, `float_eval`, `bool_eval`, `enum_eval`, `enum_value_lookup_map`, `decode_bytes`, IP/bitmask/currency/param parsing, `any_to_json` |
| `iters` | `nested_get`/`nested_set`, `any_getter`/`any_setter`, dict nesting/flattening/merging, `group_by`, list helpers (`venn`, `has`, `startswith`, ...) |
| `structs` | `Empty`/`EmptyDict`, `Singleton`, `EnumEx`, `AttributeFluidObject`, `SentientObject`, JSON serializers |
| `string` | `str_norm`, `slugify`, `maxlen`, `dequote` |
| `strimp` | Import modules, classes and functions from dotted strings (`get_any`, `get_class`, ...) |
| `insp` | `check_type` and callable/attribute introspection |
| `comparison` | `ComparableMixin` |
| `size` | `total_size` |

## Examples

```python
from batutils.tpu.casting import int_eval, bool_eval
from batutils.tpu.iters import nested_get, group_by

int_eval('0x10')                       # 16
int_eval('nope', default=None)         # None
bool_eval('yes')                       # True, only explicit "yes"-ish values count

nested_get({'a': {'b': [1, 2, 3]}}, ('a', 'b', -1))   # 3, or the default if any step is missing

group_by(['apple', 'avocado', 'banana'], lambda s: s[0])
# {'a': ['apple', 'avocado'], 'b': ['banana']}
```

Look up any function in the [Public API index](../../docs/api-index.md).
