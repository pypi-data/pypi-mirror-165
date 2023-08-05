import typing

from panther_config import detection

__all__ = ["ips_in_cidr"]


def ips_in_cidr(cidr: str, path: str = "p_any_ip_addresses") -> detection.PythonFilter:
    return detection.PythonFilter(
        func=_ip_in_cidr,
        params={
            "path": path,
            "cidr": cidr,
        },
    )


def _ip_in_cidr(obj: typing.Any, params: typing.Any) -> bool:
    import ipaddress
    import functools
    import collections

    path = params["path"]
    cidr = ipaddress.ip_network(params["cidr"])

    keys = path.split(".")

    obj_at_path = functools.reduce(
        lambda d, key: d.get(key, None) if isinstance(d, collections.Mapping) else None,
        keys,
        obj,
    )

    if obj_at_path is None:
        raise RuntimeError(f"no value found at path '{path}'")

    if isinstance(obj_at_path, str):
        return ipaddress.ip_address(obj_at_path) in cidr

    if isinstance(obj_at_path, collections.Iterable):
        for ip in obj_at_path:
            if ipaddress.ip_address(ip) in cidr:
                return True

        return False

    raise RuntimeError(f"IP value at path '{path}' was not a string or iterable")
