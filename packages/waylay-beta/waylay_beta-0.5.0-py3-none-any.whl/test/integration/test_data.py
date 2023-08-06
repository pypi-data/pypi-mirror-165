"""Integration test for the data service."""
from typing import Tuple, Iterator
from random import random
from waylay.service.data.events import EventsResource

import pytest
import numpy as np
import pandas as pd
from tenacity import Retrying, wait_fixed, stop_after_attempt

from waylay.exceptions import RestResponseError
from waylay import WaylayClient
from waylay.service import DataService
from waylay.service.data.series import SeriesResource
from waylay.service.data.events import EventsResource

NO_SUCH_RESOURCE = '__no_such_resource__'
NO_SUCH_METRIC = '__no_such_metric__'


@pytest.fixture
def series_resource(waylay_data: DataService) -> SeriesResource:
    """Inject a data.series resource."""
    return waylay_data.series


@pytest.fixture
def events_resource(waylay_data: DataService) -> EventsResource:
    """Inject a data.events resource."""
    return waylay_data.events


@pytest.fixture(scope='session')
def stored_series(waylay_session_test_client: WaylayClient) -> Iterator[Tuple[str, pd.DataFrame]]:
    """Inject a few messages for storage only."""
    waylay_api_resource = waylay_session_test_client.resources.resource
    waylay_data_events = waylay_session_test_client.data.events
    waylay_data_series = waylay_session_test_client.data.series

    resource_id = f"_wp_tst_{int(random() * 1000)}"
    metrics = ['rand', 'temp']

    waylay_api_resource.create(body={'id': resource_id})
    df = pd.DataFrame(
        index=pd.date_range(end=pd.Timestamp.utcnow(), freq='10s', periods=20, name='timestamp'),
        data=[(random(), int(20 + 5 * random())) for x in range(20)],
        columns=metrics
    )
    df_parsed = [
        {'resource': resource_id, 'timestamp': int(idx.timestamp()*1000), **row.to_dict()}
        for idx, row in df.iterrows()
    ]
    waylay_data_events.bulk(body=df_parsed, params={'forward': 'false'})
    # check upload succeeded (takes some time)
    for attempt in Retrying(
        stop=stop_after_attempt(5),
        wait=wait_fixed(2),
        reraise=True
    ):
        with attempt:
            # raises NOT FOUND if not yet ingested
            check_metric = metrics[-1]
            last_row = df_parsed[-1]
            assert waylay_data_series.latest(resource_id, metrics[-1]) == {
                'timestamp': last_row['timestamp'], check_metric: [last_row[check_metric]]
            }

    yield resource_id, df
    removed_result = waylay_data_events.remove(resource_id)
    assert 'Deleted messages, series and all metrics' in removed_result['message']
    waylay_api_resource.remove(resource_id)


def test_inspect_service(waylay_data: DataService):
    """Check defined actions."""
    assert series_resource is not None
    for action in ('latest', 'list', 'data', 'query'):
        assert action in waylay_data.series.actions
    for action in ('post', 'bulk', 'remove'):
        assert action in waylay_data.events.actions


def test_retrieve_no_data(series_resource: SeriesResource):
    """Test data retrieval for a non existing resource."""
    result = series_resource.data(NO_SUCH_RESOURCE, NO_SUCH_METRIC)
    assert result == []

    result = series_resource.data(NO_SUCH_RESOURCE, NO_SUCH_METRIC, raw=True)
    assert result.status_code == 200
    assert 'query' in result.body
    assert result.body['query']['metric'] == NO_SUCH_METRIC
    assert result.body['series'] == []

    result = series_resource.data(NO_SUCH_RESOURCE, NO_SUCH_METRIC, response_constructor=np.array)
    assert len(result) == 0


def test_list_no_data(series_resource: SeriesResource):
    """Test listing of series for a non existing resource."""
    result = series_resource.list(NO_SUCH_RESOURCE)
    assert result == []


def test_latest_no_data(series_resource: SeriesResource):
    """Test latest endpoint for a non existing resource."""
    with pytest.raises(RestResponseError) as exc_info:
        series_resource.latest(NO_SUCH_RESOURCE, NO_SUCH_METRIC)
    assert exc_info.value.response.status_code == 404


def test_query_no_data(series_resource: SeriesResource):
    """Test querying non existing data."""
    result = series_resource.query(body={
        'resources': [NO_SUCH_RESOURCE],
        'metric': NO_SUCH_METRIC,
        'aggregates': ['last'],
        'window': 'P1D',
        'grouping': 'PT1H'
    })
    assert len(result) == 24
    assert all(val[0] is not None and val[1] is None for val in result)


def test_remove_no_data(events_resource: EventsResource):
    """Tests removal of non-existing resource."""
    result = events_resource.remove(NO_SUCH_RESOURCE)
    assert 'Deleted messages, series and all metrics' in result['message']


def test_list(series_resource: SeriesResource, stored_series):
    """Test series listing for an existing resource."""
    (resource, df) = stored_series
    last_row = df.iloc[-1, :]
    last_ts = int(last_row.name.timestamp() * 1000)
    series_metadata = series_resource.list(resource)
    for metric in df.columns:
        expected_meta = {'name': metric, 'latest':  {'timestamp':  last_ts, 'value': last_row[metric]}}
        assert expected_meta in series_metadata


def test_latest(series_resource: SeriesResource, stored_series):
    """Test latest data retrieval for an existing resource."""
    (resource, df) = stored_series
    last_row = df.iloc[-1, :]
    last_ts = int(last_row.name.timestamp() * 1000)
    for metric in df.columns:
        result = series_resource.latest(resource, metric)
        # e.g. {'temp': [24], 'timestamp': 1622618925703}
        assert result == {'timestamp':  last_ts, metric: [last_row[metric]]}


def test_retrieve(series_resource: SeriesResource, stored_series):
    """Test latest data retrieval for a resource."""
    (resource, df) = stored_series
    for metric in df.columns:
        # check unaggregated retrieval
        result = series_resource.data(resource, metric)
        assert len(result) == len(df.index)
        assert result == [
            [int(idx.timestamp()*1000), row[metric]]
            for idx, row in df.iterrows()
        ]
        first_ts = int(df.index[0].timestamp()*1000)

        # check count aggregation
        result = series_resource.data(resource, metric, params={
            'grouping': 'PT1H',
            'from': first_ts,
            'aggregate': 'count'
        })
        assert len(result) == 1
        assert result == [[first_ts, len(df.index)]]


def test_query(series_resource: SeriesResource, stored_series):
    """Test latest data query for a resource."""
    (resource, df) = stored_series
    first_ts = int(df.index[0].timestamp()*1000)
    for metric in df.columns:
        result = series_resource.query(body={
            'resources': [resource],
            'metric': metric,
            'aggregates': ['count'],
            'from': first_ts,
            'window': 'P1D',
            'grouping': 'PT1H'
        })
        # check count aggregation
        assert len(result) == 1
        assert result == [[first_ts, len(df.index)]]


def test_export(series_resource: SeriesResource, stored_series):
    """Test the raw export of a single times series."""
    (resource, df) = stored_series
    for metric in df.columns:
        result = series_resource.export(resource, metric, params={'limit': 5})
        assert len(result) == 5
        assert result == [
            [int(ts.timestamp()*1000), value]
            for ts, value in df[metric].iloc[:5].items()
        ]


def test_iter_export(series_resource: SeriesResource, stored_series):
    """Test the raw export of a single times series."""
    (resource, df) = stored_series
    for metric in df.columns:
        result = list(
            series_resource.iter_export(resource, metric, page_size=5)
        )
        assert len(result) == df.index.size
        assert result == [
            [int(ts.timestamp()*1000), value]
            for ts, value in df[metric].items()
        ]


def test_iter_export_descending(series_resource: SeriesResource, stored_series):
    """Test the raw export of a single times series."""
    (resource, df) = stored_series
    for metric in df.columns:
        result = list(
            series_resource.iter_export(resource, metric, page_size=5, descending=True)
        )
        assert len(result) == df.index.size
        result.reverse()
        assert result == [
            [int(ts.timestamp()*1000), value]
            for ts, value in df[metric].items()
        ]
