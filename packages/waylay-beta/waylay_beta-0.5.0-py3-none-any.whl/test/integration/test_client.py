"""Integration tests for waylay.auth module."""
from waylay import (
    WaylayClient
)

import waylay.config
import waylay.auth_interactive
from waylay.config import (
    DEFAULT_PROFILE
)


def test_create_client_from_credentials(
    waylay_test_user_id, waylay_test_user_secret, waylay_test_gateway_url
):
    """Test authentication with client credentials."""
    waylay_client = WaylayClient.from_client_credentials(
        waylay_test_user_id, waylay_test_user_secret, gateway_url=waylay_test_gateway_url
    )
    assert waylay_client.config is not None

    cfg = waylay_client.config
    assert cfg.profile == DEFAULT_PROFILE

    cred = cfg.credentials
    assert cred.api_key == waylay_test_user_id
    assert cred.api_secret == waylay_test_user_secret
    assert cred.gateway_url == waylay_test_gateway_url
    assert cred.accounts_url is None

    query_version = waylay_client.queries.about.version()
    assert query_version.startswith('v'), query_version


def test_create_client_from_profile(
    waylay_test_user_id, waylay_test_user_secret, waylay_test_gateway_url, monkeypatch
):
    """Test profile creation dialog."""
    user_dialog = (response for response in [
        "alternate gateway", waylay_test_gateway_url,
        "apiKey", waylay_test_user_id,
        "apiSecret", waylay_test_user_secret,
        "store these credentials", 'N'
    ])

    def mock_ask(prompt: str, secret: bool = False) -> str:
        assert secret == ('Secret' in prompt)
        assert next(user_dialog) in prompt
        return next(user_dialog)

    monkeypatch.setattr(waylay.auth_interactive, 'ask', mock_ask)
    waylay_client = WaylayClient.from_profile('example', gateway_url=waylay_test_gateway_url)
    root_url = waylay_client.list_root_urls()
    assert 'query' in root_url
