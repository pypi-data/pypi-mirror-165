"""Integration tests for waylay.service.queries module."""
from typing import Dict
from datetime import datetime
import csv
import time

import pytest
import pandas as pd

from waylay.service import QueriesService, DataService


@pytest.fixture(scope='session')
def timestamp_millis() -> int:
    """Epoch timestamp millis for this session."""
    return int(datetime.now().timestamp() * 1000)


@pytest.fixture(scope='session')
def resource_id(timestamp_millis: int) -> str:
    """Resource name for this session."""
    return f'wp-int-test-{timestamp_millis}'


@pytest.fixture(scope='session')
def query_name(resource_id: str) -> str:
    """Query name for this session."""
    return f'query-{resource_id}'


@pytest.fixture(scope='session')
def query_definition(resource_id: str) -> Dict:
    """Query definition for this session."""
    return {
        "resource": resource_id,
        "metric": "ticks",
        "data": [{}]
    }


@pytest.fixture(scope='session')
def setup_query(waylay_queries: QueriesService, query_definition: str, query_name: str):
    """Provide query for this session."""
    waylay_queries.query.create(body=dict(
        name=query_name,
        query=query_definition
    ))
    yield "OK"
    waylay_queries.query.remove(query_name)


@pytest.fixture(scope='session')
def setup_data(waylay_data: DataService, resource_id, timestamp_millis: int):
    """Provide data for this session."""
    waylay_data.events.post(resource_id, body={
        "timestamp": timestamp_millis,
        "ticks": 1
    })
    yield "OK"
    waylay_data.events.remove(resource_id)


def test_get_query(waylay_queries: QueriesService, setup_query, query_name: str, query_definition):
    """Get the query definition."""
    assert setup_query == "OK"
    response = waylay_queries.query.get(query_name)
    assert response == query_definition


def test_invoke_query_no_data(waylay_queries: QueriesService, resource_id, setup_query, query_name: str):
    """Invoke query without data."""
    assert setup_query == "OK"
    df_resp = waylay_queries.query.execute(query_name)
    assert df_resp.columns.names == ['resource', 'metric']
    assert list(df_resp.columns) == [(resource_id, 'ticks')]
    assert df_resp.size == 0


def test_invoke_query(
    waylay_queries: QueriesService, setup_data, setup_query, query_name: str, resource_id, timestamp_millis: int
):
    """Invoke query."""
    assert setup_data == "OK"
    assert setup_query == "OK"
    while datetime.now().timestamp() * 1000 < timestamp_millis + 5000:
        data_resp = waylay_queries.query.execute(query_name, raw=True).body
        assert 'data' in data_resp
        data_set = data_resp['data'][0]
        assert data_set['columns'] == ['timestamp',  {'resource': resource_id, 'metric': 'ticks'}]
        data_array = data_set['data']
        if len(data_array) > 0:
            assert data_set['data'] == [[timestamp_millis, 1]]
            return
        time.sleep(1.000)

    assert False, f"could not retrieve data for {resource_id} using query {query_name}"


def test_invoke_query_df(
    waylay_queries: QueriesService, setup_data, setup_query, query_definition: dict, resource_id: str
):
    """Test invocation of a query by definition."""
    assert setup_data == "OK"
    assert setup_query == "OK"
    df_resp = waylay_queries.query.execute(query_definition)
    assert df_resp.columns.names == ['resource', 'metric']
    assert list(df_resp.columns) == [(resource_id, 'ticks')]
    assert df_resp.size == 1
    assert df_resp.iloc[0, 0] == 1


def test_invoke_query_body_arg(
    waylay_queries: QueriesService, setup_data, setup_query, query_definition: dict, resource_id: str
):
    """Test invocation of a query by definition."""
    assert setup_data == "OK"
    assert setup_query == "OK"
    df_resp = waylay_queries.query.execute(body=query_definition)
    assert df_resp.columns.names == ['resource', 'metric']
    assert list(df_resp.columns) == [(resource_id, 'ticks')]
    assert df_resp.size == 1
    assert df_resp.iloc[0, 0] == 1


def test_invoke_query_by_name_df(
    waylay_queries: QueriesService, setup_data, setup_query, query_name: str, resource_id: str
):
    """Invoke default dataframe query."""
    assert setup_data == "OK"
    assert setup_query == "OK"
    df_resp = waylay_queries.query.execute(query_name)
    assert df_resp.columns.names == ['resource', 'metric']
    assert list(df_resp.columns) == [(resource_id, 'ticks')]
    assert df_resp.size == 1
    assert df_resp.iloc[0, 0] == 1


def test_invoke_query_csv(
    waylay_queries: QueriesService, setup_data, setup_query, query_name: str, resource_id: str, timestamp_millis: int
):
    """Invoke a csv query."""
    assert setup_data == "OK"
    assert setup_query == "OK"
    http_resp = waylay_queries.query.execute(
        query_name,  params={'render.mode': 'RENDER_MODE_CSV'}, raw=True)
    assert isinstance(http_resp.body, str)
    reader = csv.reader(http_resp.body.splitlines(), delimiter=',')
    header = next(reader)
    assert header == ['timestamp', f'{resource_id}/ticks']
    data_row = next(reader)
    ts_iso = pd.Timestamp(timestamp_millis, unit='ms').isoformat()
    assert data_row == [f'{ts_iso}Z', '1']
