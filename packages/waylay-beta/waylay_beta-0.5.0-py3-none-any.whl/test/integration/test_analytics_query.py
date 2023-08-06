"""Integration tests for waylay.service.queries module."""
import pytest

from waylay import WaylayClient


def test_query_no_longer_supported(waylay_test_client: WaylayClient):
    """Assert the correct not supported warning."""
    with pytest.raises(NotImplementedError) as exc_info:
        waylay_test_client.analytics.query.data('anything')

    assert 'no longer supported' in str(exc_info.value)
