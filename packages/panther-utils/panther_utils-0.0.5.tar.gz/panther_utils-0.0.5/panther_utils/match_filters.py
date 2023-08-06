import typing

from panther_config import detection, PantherEvent

__all__ = ["deep_equal", "deep_equal_pattern", "deep_in"]


def deep_equal(path: str, value: typing.Any) -> detection.PythonFilter:
    def _deep_equal(event: PantherEvent) -> bool:
        import functools
        import collections

        keys = path.split(".")

        actual = functools.reduce(
            lambda d, key: d.get(key, None)
            if isinstance(d, collections.Mapping)
            else None,
            keys,
            event,
        )

        return bool(actual == value)

    return detection.PythonFilter(func=_deep_equal)


def deep_equal_pattern(path: str, pattern: str) -> detection.PythonFilter:
    def _deep_equal_pattern(evt: PantherEvent) -> bool:
        import re
        import functools
        import collections

        keys = path.split(".")
        regex = re.compile(pattern)

        actual = functools.reduce(
            lambda d, key: d.get(key, None)
            if isinstance(d, collections.Mapping)
            else None,
            keys,
            evt,
        )

        return bool(regex.search(actual))

    return detection.PythonFilter(func=_deep_equal_pattern)


def deep_in(path: str, value: typing.List[typing.Any]) -> detection.PythonFilter:
    def _deep_in(evt: PantherEvent) -> bool:
        import functools
        import collections

        keys = path.split(".")

        actual = functools.reduce(
            lambda d, key: d.get(key, None)
            if isinstance(d, collections.Mapping)
            else None,
            keys,
            evt,
        )

        return actual in value

    return detection.PythonFilter(
        func=_deep_in,
    )
