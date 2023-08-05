import typing

from panther_config import detection

__all__ = ["deep_equal", "deep_equal_pattern", "deep_in"]


def deep_equal(path: str, value: typing.Any) -> detection.PythonFilter:
    return detection.PythonFilter(
        func=_deep_equal,
        params={"path": path, "expected": value},
    )


def _deep_equal(obj: typing.Any, params: typing.Any) -> bool:
    import functools
    import collections

    path = params["path"]
    keys = path.split(".")
    expected = params["expected"]

    actual = functools.reduce(
        lambda d, key: d.get(key, None) if isinstance(d, collections.Mapping) else None,
        keys,
        obj,
    )

    return bool(actual == expected)


def deep_equal_pattern(path: str, pattern: str) -> detection.PythonFilter:
    return detection.PythonFilter(
        func=_deep_equal_pattern,
        params={"path": path, "pattern": pattern},
    )


def _deep_equal_pattern(obj: typing.Any, params: typing.Any) -> bool:
    import re
    import functools
    import collections

    path = params["path"]
    keys = path.split(".")
    pattern = params["pattern"]
    regex = re.compile(pattern)

    actual = functools.reduce(
        lambda d, key: d.get(key, None) if isinstance(d, collections.Mapping) else None,
        keys,
        obj,
    )

    return bool(regex.search(actual))


def deep_in(path: str, value: typing.List[typing.Any]) -> detection.PythonFilter:
    return detection.PythonFilter(
        func=_deep_in,
        params={"path": path, "expected": value},
    )


def _deep_in(obj: typing.Any, params: typing.Any) -> bool:
    import functools
    import collections

    path = params["path"]
    keys = path.split(".")
    expected = params["expected"]

    actual = functools.reduce(
        lambda d, key: d.get(key, None) if isinstance(d, collections.Mapping) else None,
        keys,
        obj,
    )

    return actual in expected
