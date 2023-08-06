"""Integration test that cleans up all the models after performing all the tests."""

import os
import pytest

from waylay import (
    WaylayClient,
)

from fixtures import integration_test_id
from model_cleanup import cleanup_models


@pytest.mark.byoml_integration
@pytest.mark.cleanup
def test_byoml_remove_all_models_after_tests(
    waylay_test_client: WaylayClient,
    integration_test_id
):
    """Remove all created models."""
    cleanup_models(waylay_test_client, prefix=integration_test_id)
    assert not waylay_test_client.byoml.model.list_names(params={'name': integration_test_id + '*'})
