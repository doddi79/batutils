# batutils Public API Index

- Distribution: `batutils` (PyPI) — Import: `batutils`
- Covers: version **2.2.0**, working tree at commit `4acf338` (`main`), Python >= 3.10
- Scope: public names from the `__all__` of each module, as re-exported by the
  package `__init__` files. `_`-prefixed modules are private; import from the
  package shown in **Import** instead.
- Existing narrative docs: [dtu README](../batutils/dtu/README.md) (date/time),
  [tpu README](../batutils/tpu/README.md) (stub only, nothing documented there).

Three areas, three entry points:

| Area | Import | What it is |
|------|--------|------------|
| Date/time utils | `from batutils import dtu` | Casting, parsing, formatting, shortcuts for `datetime` values |
| Type utils | `from batutils.tpu import <sub>` or `from batutils.tpu.<sub> import <name>` | Evaluation, iteration, inspection, string, serialization helpers |
| Common imports | `from batutils.structs import *` | One-line import of `typing.*`, `abc`, `dataclasses`, `decimal`, `enum`, `logging`, `re`, `time`, plus `Singleton`, `Empty`, `EmptyDict`, `if_empty`, `EnumEx` and the `dtu` aliases |

`batutils/tpu/__init__.py` is empty: import the subpackage (`from batutils.tpu import iters`)
or the name from its subpackage. Nothing is re-exported at `batutils.tpu`.

## Find it by task

| I want to… | Use | Section |
|------------|-----|---------|
| Convert "anything" (str / epoch / Windows filetime / date) to a datetime | `dtu.any_to_datetime` | [Casting](#date-time-casting) |
| Convert epoch seconds, epoch milliseconds, or Windows filetime to/from datetime | `dtu.timestamp_to_datetime`, `dtu.instant_to_datetime`, `dtu.filetime_to_datetime` (+ inverses) | [Casting](#date-time-casting) |
| Parse an ISO-ish string, or a string with a custom regex, to a datetime | `dtu.isostr_to_datetime`, `dtu.regex_to_datetime` | [Casting](#date-time-casting) |
| Parse "3 days 2 hours" into a timedelta | `dtu.str_to_delta` | [Parsing](#date-time-parsing) |
| Parse "now"/"yesterday"/"tomorrow", or "date to date" ranges | `dtu.str_to_rel`, `dtu.str_to_2dates` | [Parsing](#date-time-parsing) |
| Print "5 days ago" / "3 weeks" / "1 year and 7 months" | `dtu.agostr`, `dtu.deltastr`, `DeltaSplit.to_str` | [Formatting](#date-time-formatting) |
| JSON-friendly string/number for a date, time, datetime or timedelta | `dtu.serialize`, `dtu.to_str` | [Formatting](#date-time-formatting) |
| Time N days from now / N hours ago; next Monday; next 11:00; truncate to midnight | `dtu.from_now`, `dtu.ago`, `dtu.next_weekday`, `dtu.next_time`, `dtu.set_midnight` | [Shortcuts](#date-time-shortcuts) |
| Is this date in the past/future? | `dtu.is_past`, `dtu.is_future` | [Shortcuts](#date-time-shortcuts) |
| Break a timedelta into years/months/weeks/days/hours/minutes/seconds | `dtu.DeltaSplit` | [Structs](#date-time-structs) |
| Safely cast to int / float / bool with a default, instead of try/except | `float_eval`, `int_eval`, `bool_eval` | [Evaluation](#type-evaluation-and-casting) |
| Turn a string/number/name into an enum member | `EnumEx.from_any`, `enum_eval` | [Enums](#enums) |
| Reverse lookup of an enum by value (incl. multi-value enums) | `enum_value_lookup_map` | [Enums](#enums) |
| Dig into nested dict/list with a path, without KeyError | `nested_get` / `nested_set` | [Iterables](#iterables-and-containers) |
| Get an item/attribute uniformly from dict, list or object | `any_getter` / `any_setter` | [Iterables](#iterables-and-containers) |
| Deep-merge dicts; flatten `{'a': {'b': 1}}` into `{'a.b': 1}`; reverse | `nested_dict_update`, `str_flatten_dict`, `flatten_dict`, `str_nest_dict`, `nest_dict` | [Iterables](#iterables-and-containers) |
| Group a list of objects by an attribute/index/callable | `group_by` | [Iterables](#iterables-and-containers) |
| Diff two lists (only-left, both, only-right); list prefix/suffix/sub-sequence tests | `venn`, `startswith`, `endswith`, `has`, `has_all`, `has_any` | [Iterables](#iterables-and-containers) |
| Import a module/class/function from a dotted string | `get_any`, `get_module`, `get_class`, `get_callable`, `get_function` | [Import by string](#import-by-string) |
| Never-raising "missing" sentinel / default dict; "fluid" attribute object | `Empty`, `EmptyDict`, `if_empty`, `AttributeFluidObject` | [Structs](#structs-and-base-classes) |
| Make a class a singleton | `Singleton` metaclass | [Structs](#structs-and-base-classes) |
| Serialize arbitrary Python objects to JSON/dict | `any_to_json`, `JsonSerializer`, `JsonSafeSerializer`, `UniversalSerializer` | [Serialization](#serialization) |
| Slugify / normalize / trim / dequote a string | `slugify`, `str_norm`, `maxlen`, `dequote` | [Strings](#strings) |
| Decode bytes of unknown encoding | `decode_bytes` | [Misc](#misc-casting-and-inspection) |
| IP address <-> int; split a bitmask; parse "USD 12.50" | `ip_to_int`/`int_to_ip`, `split_bitmask`, `parse_currency_text` | [Misc](#misc-casting-and-inspection) |
| Check a value against a type annotation at runtime | `check_type` | [Misc](#misc-casting-and-inspection) |
| Inspect a callable's signature / test its argument profile | `get_argspec`, `fits_callable_profile` | [Misc](#misc-casting-and-inspection) |
| Approximate memory footprint of an object | `total_size` | [Misc](#misc-casting-and-inspection) |

---

## Date/time (`dtu`)

`from batutils import dtu` — everything below is `dtu.<name>`. Also exposes
`dtu.VERSION` (the package version). All functions are **timezone-naive**
unless stated. Tests: [tests/datetimeutils](../tests/datetimeutils).

### Date/time structs

| Name | Definition |
|------|------------|
| `Date`, `Time`, `Datetime`, `TimeDelta`, `TzInfo`, `TimeZone` | Plain aliases of `datetime.date/time/datetime/timedelta/tzinfo/timezone` (same class objects, not subclasses) |
| `T_DATETIME_VALUE` | `Union[datetime, date, time]` |
| `T_DATE_VALUE` | `Union[datetime, date]` |
| `T_TIME_VALUE` | `Union[datetime, time]` |
| `T_TEMPORAL_VALUE` | `T_DATETIME_VALUE` or `float`, `int`, `str`, `bytes` |
| `T_NUMBER` | `Union[int, float]` |
| `Weekday` | `enum.IntEnum`: `MONDAY=0` … `SUNDAY=6` |
| `DAYS_IN_MEAN_YEAR` 365.2425, `DAYS_IN_MEAN_MONTH` 30.436875, `DAYS_IN_MEDIAN_YEAR` 365, `DAYS_IN_MEDIAN_MONTH` 31, `WHOLE_DAYS_IN_MEAN_YEAR` 365, `WHOLE_DAYS_IN_MEAN_MONTH` 30 | Constants used for approximate year/month splitting |
| `SECONDS_IN_ONE_MINUTE` 60, `SECONDS_IN_ONE_HOUR` 3600, `SECONDS_IN_ONE_DAY` 86400 | Constants |

#### `DeltaSplit`
Dataclass that splits a `timedelta` into approximate units (years and months use the mean-length constants above).

```python
DeltaSplit(time_delta: TimeDelta, include_weeks=True, include_months=True, include_years=True)
```
- Fields: `years`, `months`, `weeks` (each `None` when excluded), `days`, `hours`, `minutes`, `seconds`, `is_past` (True for negative deltas), `field_order`.
- Properties: `largest`, `largest_field_name`, `largest_value`, `second_largest`, `second_largest_field_name`, `second_largest_value` (name `None` / value `0` when there is none).
- `get(field_name) -> str`, `get_value(field_name) -> int`, `to_dict() -> Dict`.
- `to_str(max_number_of_fields=2, include_seconds=False, directionals=<default pair>, no_time_str='no time at all', only_sec_str='a few seconds', granularity_halting_threshold=1) -> str` — human text such as `"1 year and 7 months"`; this is what `deltastr` uses.
- Source: [_deltasplit.py](../batutils/dtu/structs/_deltasplit.py); tests [test_deltasplit.py](../tests/datetimeutils/test_deltasplit.py).

### Date/time casting

| Signature | Notes |
|-----------|-------|
| `any_to_datetime(temporal_object: T_TEMPORAL_VALUE, default=<input>) -> Datetime \| Any` | Best-guess cast. **On failure returns the input unchanged** (or `default` if given); it does not raise. `datetime` returned as-is; `date` becomes midnight. Numbers: treated as timestamp (seconds) if within ±1000 years of now, else as instant (ms) if within range, else Windows filetime. Known misfires: instants within ~1 year of 1970, timestamps > 1000 years from now. For strings ISO is tried first, then day-first, then US month-first, so ambiguous `MM-DD` strings are read as ISO. Use a specific converter when the format is known. Source [_any.py](../batutils/dtu/casting/_any.py), tests [test_datetimeutils.py](../tests/datetimeutils/test_datetimeutils.py) |
| `timestamp_to_datetime(seconds_since_epoch: T_NUMBER, minmax_on_fail=False) -> Datetime` / `datetime_to_timestamp(dt: T_DATE_VALUE) -> float` | Unix seconds, naive datetime. On `OverflowError` re-raises unless `minmax_on_fail=True` (returns `Datetime.max`/`min`). `date` input counts as 00:00 |
| `instant_to_datetime(milliseconds_since_epoch: T_NUMBER, minmax_on_fail=False) -> Datetime` / `datetime_to_instant(dt: T_DATE_VALUE) -> int` | Unix **milliseconds** |
| `filetime_to_datetime(filetime: T_NUMBER) -> Datetime` / `datetime_to_filetime(dt: T_DATE_VALUE) -> int` | Windows FILETIME: 100 ns ticks since 1601-01-01 UTC |
| `isostr_to_datetime(string: str) -> Optional[Datetime]` | ISO-ish string; `None` if unparseable |
| `regex_to_datetime(string: str, regex_pattern) -> Optional[Datetime]` | Pattern uses named groups matching `datetime` keywords (`year`, `month`, `day`, `hour`, …) |

```python
dtu.regex_to_datetime('31/12/2023', r'(?P<day>\d+)/(?P<month>\d+)/(?P<year>\d+)')
```

### Date/time parsing

| Signature | Notes |
|-----------|-------|
| `str_to_delta(string: str, default=0) -> TimeDelta \| Any` | Parses `"2h34m"`, `"12days"`, `"-1.5 hours"`. Keywords: d/day/days, h/hr/hrs/hour/hours, m/i/min/mins/minute/minutes, s/sec/secs/second/seconds, w/wk/wks/week/weeks (no months/years). On failure returns `default`; the default `0` is replaced by `TimeDelta(0)`, so pass `None` to detect failure |
| `str_to_rel(str_value: str) -> Optional[Datetime]` | Only `now`, `today`, `yesterday`, `tomorrow` (case-insensitive); else `None`. Result keeps the current time of day |
| `str_to_2dates(str_value: str) -> Optional[Tuple[Date, Date]]` | `"1969-08-15 to 1967-08-19"`: exactly two ISO dates with any separator. Order is **not** validated. `None` otherwise |
| `split_delta(delta, include_weeks=True, include_months=True, include_years=True)` | Defined in `parsers/_timedelta.py` but only in the module's `__all__` as `str_to_delta`; not exported through `dtu`. Use `DeltaSplit` |

### Date/time formatting

| Signature | Notes |
|-----------|-------|
| `serialize(temporal_object: T_TEMPORAL_VALUE) -> str \| float` | ISO string for datetime/date/time; `timedelta` becomes float `total_seconds()` |
| `to_str(temporal_object: T_TEMPORAL_VALUE) -> str` | `str()` of whatever `serialize` returned |
| `deltastr(delta: TimeDelta, default='') -> str` | `"3 weeks"`, `"a few seconds"`, `"1 year and 7 months"` |
| `agostr(delta_or_date, default='', utc=True) -> str` | Same, but given a date/time/datetime it uses the delta between that value and now (UTC when `utc=True`) |

### Date/time shortcuts

| Signature | Notes |
|-----------|-------|
| `now() -> Datetime`, `now_time() -> Time`, `today() -> Date`, `ticks() -> float` | `datetime.now()`, `.now().time()`, `date.today()`, `time.time()` |
| `is_past(temporal_object)`, `is_future(temporal_object) -> bool` | Casts with `any_to_datetime` first |
| `from_now(days=0, hours=0, minutes=0, seconds=0, weeks=0) -> Datetime`, `ago(...same...) -> Datetime` | Now plus / minus the given amounts |
| `next_time(find_time: Time, start_dt=None) -> Datetime` | Earliest datetime after `start_dt` (default now) with that clock time |
| `next_weekday(day_of_week: Weekday \| int, find_time: Optional[Time]=None, start_dt=None) -> Datetime` | `find_time` defaults to midnight; 0 = Monday |
| `set_midnight(dt: T_DATE_VALUE) -> Datetime` | Zeroes the time part; a `date` becomes a midnight datetime |

---

## Type utils (`tpu`)

### Structs and base classes

| Import | Signature / behavior |
|--------|----------------------|
| `from batutils.tpu.structs.empty import Empty, EmptyDict, if_empty` | `Empty`: a falsy singleton "missing value" instance (`value is Empty` to test). `EmptyDict(*args, **kwargs)`: a `defaultdict` whose missing keys return `Empty`; nested access yields `Empty`s, so `d.a.b.c` never raises. `if_empty(value, return_if_empty=None)` returns `return_if_empty` when `value` is `Empty` |
| `from batutils.tpu.structs.singleton import Singleton` | Metaclass: `class Cfg(metaclass=Singleton)`. Every call to `Cfg(...)` returns the first instance (later constructor arguments are ignored). `Singleton.wrapper` (decorator form) raises `AttributeError` when used in this version; use the metaclass |
| `from batutils.tpu.structs.fluid import AttributeFluidObject` | `AttributeFluidObject(**kwargs)`: attributes from kwargs; unknown attributes return `None` instead of raising `AttributeError` |
| `from batutils.tpu.structs.sentience import SentientObject` | Base class + `@SentientObject.sentient(**meta)` decorator tagging methods with metadata; `cls.sentient_methods(inherited=True)` returns the map of tagged methods |
| `from batutils.tpu.comparison import ComparableMixin` | Subclass must implement `__lt__`; the mixin derives `__eq__`, `__ne__`, `__gt__`, `__ge__`, `__le__` from it (`__new__` raises `NotImplementedError` otherwise) |

These also come via `from batutils.structs import *` (only `Singleton`, `Empty`, `EmptyDict`, `if_empty`, `EnumEx`).
Tests: [test_empty.py](../tests/typeutils/test_empty.py), [test_fluid.py](../tests/typeutils/test_fluid.py), [test_sentient_object.py](../tests/typeutils/test_sentient_object.py).

### Enums

```python
from batutils.structs import EnumEx           # or batutils.tpu.structs.enumex
from batutils.tpu.casting import enum_eval, enum_value_lookup_map
```

| Signature | Behavior |
|-----------|----------|
| `class EnumEx(enum.Enum)` with `from_any(cls, value, default=<unset>) -> member` | **Raises** `ValueError` on failure unless `default` is given (then returns it, `None` allowed) |
| `enum_eval(value, enum_class, default=None, raise_on_fail=False)` | Lookup order: already a member → name (case-insensitive, stripped) → value (incl. each element of multi-value tuples) → numeric string via `int(value, base=0)`. **Returns `default` (`None`) on failure** — opposite of `EnumEx.from_any`. Raises `KeyError` / `ValueError` only if `raise_on_fail` |
| `enum_value_lookup_map(enum_class, allow_collision=False) -> Dict[value, member]` | Value → member including each tuple element of multi-value enums. Raises `KeyError` on colliding values unless `allow_collision=True` |

Aliased members (same value, several names) are supported. Tests: [test_eval_enum.py](../tests/typeutils/test_eval_enum.py).

### Type evaluation and casting

`from batutils.tpu.casting import ...`

| Signature | Behavior |
|-----------|----------|
| `int_eval(value, default=0, raise_on_fail=False) -> int \| None` | Strings go through `int(base=0)` (so `"0x10"` works), then `int(float(value))`. Floats truncate. `timedelta` → seconds; date → local-time epoch. Pass `default=None` to detect failure |
| `float_eval(value, default=0.0, raise_on_fail=False) -> float \| None` | Same idea for floats |
| `bool_eval(value, raise_on_fail=False) -> bool` | `True` only for bools, non-zero numbers/numeric strings, or strings `active`, `enable`, `enabled`, `on`, `true`, `yes`, `y` (case-insensitive). **Any other object, including a non-empty list, is `False`** (not Python truthiness) |

Tests: [test_casting.py](../tests/typeutils/test_casting.py).

### Iterables and containers

`from batutils.tpu.iters import ...`

| Signature | Behavior |
|-----------|----------|
| `any_getter(obj, key: str\|int, default=None, eval_call=False)` | `int` key → `obj[key]` (default on `IndexError`/`KeyError`); `str` key → `Mapping.get` else `getattr`. `eval_call=True` calls a callable result |
| `any_setter(obj, key, value)` | Sets item for mutable mappings/sequences/int keys, else attribute |
| `nested_get(obj, key_list, default=None)` | Walks mixed dict/list/attribute path, e.g. `('a', 7, 'c', -2)`. **Returns `default` if any step is `None`**, so a legitimately-`None` leaf is also reported as `default` |
| `nested_set(obj, key_list, value)` | Mirror of `nested_get` |
| `nested_dict_update(base_map, update_map)` | **Mutates** `base_map` in place, recursively merging dict values |
| `nest_dict(key_list, value=None) -> dict` / `str_nest_dict("a.b.c", value=None, key_seperator='.') -> dict` | Build `{'a': {'b': {'c': value}}}` |
| `flatten_dict(d) -> Dict[tuple, Any]` / `str_flatten_dict(d, joiner='.', caster=str) -> Dict[str, Any]` | Inverse of the nest functions: tuple or joined-string keys |
| `group_by(list_of_stuff, key_getter: str\|int\|Callable) -> Dict[key, list]` | `str` = attribute or dict key, `int` = index, callable = key function. If the resolved key is itself callable it is called (accessor methods) |
| `venn(left, right) -> (only_left, both, only_right)` | Three lists; duplicates collapse |
| `startswith(main_list, sub_list)`, `endswith(...)` | Prefix / suffix test on lists/tuples |
| `has(main_list, sub_list)` | Contiguous, in-order sub-sequence; empty `sub_list` is True |
| `has_all(main_list, sub_list)`, `has_any(main_list, sub_list)` | Membership of all / any, order-insensitive |

Tests: [test_iters.py](../tests/typeutils/test_iters.py), [test_any_getter.py](../tests/typeutils/test_any_getter.py), [test_nested_getter.py](../tests/typeutils/test_nested_getter.py), [test_group_by.py](../tests/typeutils/test_group_by.py).

### Import by string

`from batutils.tpu.strimp import get_any, get_module, get_class, get_callable, get_methfunc, get_function`

All share `(string, default=None, logger=False, reraise=False)`. They are **silent by default**: failure returns `default`. Set `reraise=True` to get the exception, `logger` to log it. A non-string argument is returned unchanged. `get_any` resolves a module or any top-level attribute (`"os.path.join"`). The type-specific variants additionally check the kind of object found (`get_class("os.path.join")` → `None`). Tests use [tests/typeutils/sometypes](../tests/typeutils/sometypes).

### Strings

`from batutils.tpu.string import str_norm, str_norm_eq, maxlen, slugify, dequote`

| Signature | Behavior |
|-----------|----------|
| `str_norm(string, default='') -> str` | `str()` + strip + **lowercase**; `default` for `None` or failure |
| `str_norm_eq(a, b) -> bool` | Equality after `str_norm` |
| `maxlen(string, max_length) -> str` | Truncates the end; non-strings returned unchanged |
| `slugify(string)` | Lowercase; separators → `-`; drops anything outside a-z/0-9 |
| `dequote(string, symbol_list=None) -> str` | Removes one *matching* pair of surrounding quotes (`"hi"` → `hi`; `"hi'` unchanged), or custom symbols |

### Serialization

| Import | Signature / behavior |
|--------|----------------------|
| `from batutils.tpu.casting import any_to_json` | `any_to_json(anything, skip_keys=None, skip_values=None, skip_private=True, skip_nones=False, skip_empties=False, max_depth=0) -> str` — **Known bug**: with the default `skip_keys=None`/`skip_values=None`, dicts and objects return an error string like `"__ERROR__::<class 'dict'>::argument of type 'NoneType'..."` instead of raising. Pass `skip_keys=[], skip_values=[]` explicitly (verified working). Scalars, e.g. datetimes, work with defaults |
| `from batutils.tpu.structs.serializers import UniversalSerializer` | `UniversalSerializer(skip_keys=None, skip_values=None, skip_private=True, skip_nones=False, skip_empties=False, max_depth=0).serialize(obj)` → plain Python structure; works with the constructor defaults (recursive; private `_` attributes skipped by default; `max_depth=0` = unlimited) |
| `JsonSafeSerializer(UniversalSerializer)` | `.serialize(obj)` returns a Python structure (not a string) with `datetime` family values converted to ISO strings |
| `JsonSerializer(JsonSafeSerializer)` | `.serialize(obj, indent=4, sort_keys=True) -> str` |

Note: the `JsonSerializer.serialize` signature differs from the base class's. Source [serializers](../batutils/tpu/structs/serializers).

### Misc casting and inspection

| Import | Signature / behavior |
|--------|----------------------|
| `from batutils.tpu.casting import decode_bytes` (also `from batutils._common import decode_bytes`) | `decode_bytes(byte_str: bytes) -> str`; trial-and-error over encodings; raises `ValueError` if none work |
| `from batutils.tpu.casting import ip_to_int, int_to_ip` | IPv4 dotted string ↔ int |
| `from batutils.tpu.casting import split_bitmask` | `split_bitmask(13)` → `[1, 4, 8]` (the set single-bit values) |
| `from batutils.tpu.casting import parse_currency_text` | `"USD +12.50"` → `('USD', 12.5)`; `(None, None)` style results when unparseable |
| `from batutils.tpu.casting import Params, parse_params` | `parse_params(params: list[str] \| str, list_of_props=None, props_as_kw_dict=None, matcher=None)` `parse_params('a b c=1')` → `Params(args=['a','b'], kwargs={'c':'1'}, props={})` |
| `from batutils.tpu.insp import check_type` | `check_type(val, type_or_annotation) -> bool`; runtime check against `typing` annotations. Tests [test_insp.py](../tests/typeutils/test_insp.py) |
| `from batutils.tpu.insp import is_methfunc, is_callable, get_argspec, fits_callable_profile, get_any_name, get_first_attr, resolve_attr, resolve_first` | Callable/attribute introspection helpers; `fits_callable_profile(callable, required_arg_count=None, total_arg_count=None, default_count=None, has_varargs=None, has_kwargs=None, arg_names=None, raise_error=False)`; `get_first_attr(obj, list_of_attributes, default=None, skip_nones=False)`; `resolve_attr` calls it if it is a callable/property |
| `from batutils.tpu.size import total_size` | `total_size(o, handlers=None, verbose=False)` approximate recursive memory footprint |

---

## Gaps and cautions

- `batutils.tpu` has no top-level re-exports, and its README is a stub.
  `SentientObject`, `check_type`, `fits_callable_profile`, `total_size` and
  `parse_params` (beyond the example shown) are indexed from signatures and
  docstrings only; check the source before relying on edge cases.
- `dtu` README marks Constants and `DeltaSplit` as TODO; this index supplies them.
- `tpu/insp/_insp_old.py` is exported but the filename suggests legacy; treat
  `get_argspec`, `is_methfunc`, `is_callable` as low-priority.
- `from batutils.dtu.parsers._timedelta import split_delta` is not public.
- No deprecated names are declared. The former `legacyapi` submodule was removed in 2.0.0.
