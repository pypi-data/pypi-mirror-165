## panther-utils
Panther Config SDK utilities repo


### Match Filters

The `deep_equal` filter allows you to filter events based on a field match.

```python
from panther_config import detection
from panther_utils import match_filters

# example: match server logs with insecure POST requests
detection.Rule(
    rule_id="My.Custom.Rule",
    log_types=["ServerLogs.HTTP"],
    filters=[
        match_filters.deep_equal(path="request.method", value="POST"),
        match_filters.deep_equal(path="request.use_ssl", value=False),
    ]
)
```

### Network Filters

The `ips_in_cidr` filter allows you to filter events based whether IPs are in a CIDR range. The optional `path` argument can target a dot-separated path to a single IP string or a list of IP strings. The `path` argument defaults to the Panther field `p_any_ip_addresses`. This filter uses the python [ipaddress](https://docs.python.org/3.9/library/ipaddress.html#) module to perform the comparison.

```python
from panther_config import detection
from panther_utils import network_filters

# example: match server logs coming from 10.x.x.x
detection.Rule(
    rule_id="My.Custom.Rule",
    log_types=["ServerLogs.HTTP"],
    filters=[
        network_filters.ips_in_cidr(cidr = "10.0.0.0/8"), # by default, source IPs from p_any_ip_addresses
    ]
)

# example: match server logs coming from 192.168.x.x
detection.Rule(
    rule_id="Internal.Logs",
    log_types=["Custom.InternalLogs"],
    filters=[
        network_filters.ips_in_cidr(cidr = "192.168.0.0/16", path="custom.path.to.ips"), 
    ]
)
```
