"""Test byoml decorators."""
import pytest

from waylay.service.byoml._decorators import byoml_raise_not_ready_get
from waylay.service.byoml._exceptions import ByomlActionParseError, ModelNotReadyError


class MockResponse:
    """Class that mocks a byoml response."""

    def __init__(self, response):
        """Initialize a MockResponse instance."""
        self.body = response


@byoml_raise_not_ready_get
def ready_not_available(**kwargs):
    """Return a test response not containing the key `ready`."""
    return MockResponse({'foo': 'bar'})


@byoml_raise_not_ready_get
def model_ready(**kwargs):
    """Return a test response where the `ready` key contains a True value."""
    return MockResponse({'ready': True})


@byoml_raise_not_ready_get
def model_not_ready(**kwargs):
    """Return a test response where the `ready` key contains a False value."""
    return MockResponse({'ready': False})


def test_raise_on_retry():
    """Test raising of ByomlActionParseError."""
    with pytest.raises(ByomlActionParseError) as exc:
        ready_not_available(retry_until_ready=True)
    assert exc.value.message == 'Failed to extract `ready` attribute'


def test_retry_false():
    """Test raising of ModelNotReadyError."""
    with pytest.raises(ModelNotReadyError) as exc:
        model_not_ready(retry_until_ready=True)
    assert str(exc.value) == 'Model is not ready yet.'


def test_retry_true():
    """Test response of model."""
    response = model_ready(retry_until_ready=True)
    assert response.body.get('ready') is True
