from panther_config import testing
from panther_utils import match_filters


class TestMatchFilters(testing.PantherPythonFilterTestCase):
    def test_deep_equal(self) -> None:
        test_filter = match_filters.deep_equal("a.b", "targeted-value")

        self.assertFilterIsValid(test_filter)

        self.assertFilterMatches(test_filter, {"a": {"b": "targeted-value"}})
        self.assertFilterNotMatches(test_filter, {"a": {"b": "other-value"}})

    def test_deep_in(self) -> None:
        test_filter = match_filters.deep_in("a.b", ["targeted-value"])

        self.assertFilterIsValid(test_filter)

        self.assertFilterMatches(test_filter, {"a": {"b": "targeted-value"}})
        self.assertFilterNotMatches(test_filter, {"a": {"b": "other-value"}})

    def test_deep_equal_pattern(self) -> None:
        test_filter = match_filters.deep_equal_pattern("a.b", r"target")

        self.assertFilterIsValid(test_filter)

        self.assertFilterMatches(test_filter, {"a": {"b": "targeted-value"}})
        self.assertFilterNotMatches(test_filter, {"a": {"b": "other-value"}})
