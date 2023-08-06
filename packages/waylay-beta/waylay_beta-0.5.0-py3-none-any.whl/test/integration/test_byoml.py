"""Integration connectivity test for the BYOML service."""

from waylay.service import ByomlService


def test_byoml_about(waylay_byoml: ByomlService):
    """Test connectivity with the byoml model endpoint."""
    assert waylay_byoml.root_url is not None
    assert waylay_byoml.root_url.endswith('/ml/v1')

    about = waylay_byoml.about.health()
    assert 'byoml' in about


def test_byoml_list_model_names(waylay_byoml: ByomlService):
    """Test model name listing."""
    names = waylay_byoml.model.list_names()
    assert names is not None
    if names:
        assert isinstance(names[0], str)
