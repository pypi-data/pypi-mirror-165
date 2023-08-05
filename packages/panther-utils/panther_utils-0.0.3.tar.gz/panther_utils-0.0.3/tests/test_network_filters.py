from panther_config import testing
from panther_utils import network_filters


class TestNetworkFilters(testing.PantherPythonFilterTestCase):
    def test_ips_in_cidr(self) -> None:
        test_filter = network_filters.ips_in_cidr("10.0.0.0/8")

        self.assertFilterIsValid(test_filter)

        self.assertFilterMatches(test_filter, {"p_any_ip_addresses": ["10.0.0.1"]})
        self.assertFilterNotMatches(
            test_filter, {"p_any_ip_addresses": ["192.168.0.1"]}
        )

    def test_ips_in_cidr_custom_path(self) -> None:
        test_filter = network_filters.ips_in_cidr("10.0.0.0/8", path="nested.ips")

        self.assertFilterIsValid(test_filter)

        self.assertFilterMatches(test_filter, {"nested": {"ips": ["10.0.0.1"]}})
        self.assertFilterNotMatches(test_filter, {"nested": {"ips": ["192.168.0.1"]}})

    def test_ips_in_cidr_non_array(self) -> None:
        test_filter = network_filters.ips_in_cidr("10.0.0.0/8", path="nested.ips")

        self.assertFilterIsValid(test_filter)

        self.assertFilterMatches(test_filter, {"nested": {"ips": "10.0.0.1"}})
        self.assertFilterNotMatches(test_filter, {"nested": {"ips": "192.168.0.1"}})

    def test_ips_in_cidr_no_value_at_path(self) -> None:
        test_filter = network_filters.ips_in_cidr("10.0.0.0/8", path="bad.path.to.ips")

        self.assertFilterIsValid(test_filter)

        self.assertRaises(
            RuntimeError,
            lambda: self.assertFilterMatches(
                test_filter, {"nested": {"ips": "10.0.0.1"}}
            ),
        )

    def test_ips_in_cidr_bad_value_at_path(self) -> None:
        test_filter = network_filters.ips_in_cidr("10.0.0.0/8", path="nested.field")

        self.assertFilterIsValid(test_filter)

        self.assertRaises(
            RuntimeError,
            lambda: self.assertFilterMatches(test_filter, {"nested": {"field": True}}),
        )
