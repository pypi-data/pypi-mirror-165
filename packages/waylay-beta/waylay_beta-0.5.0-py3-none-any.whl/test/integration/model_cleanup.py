"""Clean up models which are created after running integration tests."""

import logging

from waylay import (
    WaylayClient
)

LOG = logging.getLogger(__name__)

# keep prefix short until resolution of https://github.com/waylayio/plug-registry/issues/476
INTEGRATION_TEST_PREFIX = 'tst'


def cleanup_models(client: WaylayClient, prefix: str = INTEGRATION_TEST_PREFIX):
    """Cleanup all models."""
    assert len(prefix) > 2, f'prefix must have length > 2: {prefix}'
    for model_name in client.byoml.model.list_names(params={'name': prefix + '*'}):
        assert model_name.startswith(prefix), f'{model_name} does not start with {prefix}'
        LOG.info('Removing %s', model_name)
        client.byoml.model.remove(model_name)
