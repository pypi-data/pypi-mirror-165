"""Check setup of a waylay client."""

from waylay import WaylayClient, RestResponseError

from waylay.service import ResourcesService

TEST_RESOURCE_ID = 'waylay-py-integration-test'


def test_resource(waylay_resources: ResourcesService):
    """Test all exposed methods of the /api/resources engine api."""
    assert waylay_resources.root_url is not None

    assert waylay_resources.root_url.endswith('/resources/v1')

    resources_api = waylay_resources.resource

    try:
        result = resources_api.remove(TEST_RESOURCE_ID)
    except RestResponseError as e:
        # not existing
        assert e.response.status_code == 404

    result = resources_api.create(body={'id': TEST_RESOURCE_ID})

    result = resources_api.get(TEST_RESOURCE_ID)
    assert result['id'] == TEST_RESOURCE_ID

    result = resources_api.replace(TEST_RESOURCE_ID, body={
        'id': TEST_RESOURCE_ID, 'name': TEST_RESOURCE_ID
    })
    assert result['id'] == TEST_RESOURCE_ID

    result = resources_api.update(
        TEST_RESOURCE_ID, body={'metrics': [dict(name='temp')]
                                })
    assert result['metrics'][0]['name'] == 'temp'

    result = resources_api.list(params=dict(filter=TEST_RESOURCE_ID))
    assert len(result) == 1
    assert result[0]['id'] == TEST_RESOURCE_ID

    result = resources_api.remove(TEST_RESOURCE_ID)
    assert result is None
