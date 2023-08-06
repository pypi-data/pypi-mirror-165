"""Tests for the base framework."""
from waylay import WaylayClient, WaylayConfig
from waylay.auth import NoCredentials
import waylay.service._base as base


def test_repr():
    """Test representation format of actions."""
    waylay_client = WaylayClient(WaylayConfig(NoCredentials(), fetch_tenant_settings=False))
    query_actions = waylay_client.queries.query.actions
    assert query_actions is not None
    assert 'list' in query_actions
    list_action = query_actions['list']
    assert isinstance(list_action, base.WaylayRESTAction)
    assert repr(list_action) == 'GET /query'
    assert 'execute' in query_actions
    execute_action = query_actions['execute']
    assert isinstance(execute_action, base.WaylayRESTActionsWrapper)
    assert repr(execute_action) == 'execute'
