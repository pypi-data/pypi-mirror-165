"""Test suite for the timeseries etl tool."""

from typing import Iterator
import tempfile
from datetime import datetime

import pytest
import pandas as pd

from waylay.service.timeseries.tool import TimeSeriesETLTool, ResourceUpdateLevel


class DummyETLToolContext():
    """Service context that returns mocked services."""

    def __init__(self, mocker):
        """Create a mocked context."""
        self.mocker = mocker

    def require(self, cls):
        """Create a mocked service object."""
        return self.mocker.patch(f'waylay.service.{cls.__name__}')


@pytest.fixture
def timeseries_tool(mocker) -> TimeSeriesETLTool:
    """Get a timeseries tool with mocks services injected."""
    etl_tool = TimeSeriesETLTool()
    etl_tool.set_context(DummyETLToolContext(mocker))
    return etl_tool


@pytest.fixture
def temp_dir() -> Iterator[str]:
    """Create (and cleanup) a temporary directory."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


def test_tool_df(timeseries_tool: TimeSeriesETLTool, temp_dir: str):
    """Test tool api general workflow."""
    df = pd.DataFrame(
        list(range(10)),
        index=pd.date_range(start='2020-02-02T08:10+00:00', freq='1h', periods=10)
    )

    import_name = f'unit-test-import-{int(datetime.now().timestamp())}'
    import_job = timeseries_tool.prepare_import(
        df, resource='r1', name=import_name, temp_dir=temp_dir
    )

    timeseries_tool.initiate_import(import_job, ResourceUpdateLevel.NONE)

    timeseries_tool.storage_service.content.put.assert_called_with(  # type: ignore
        'etl-import',
        f'upload/{import_name}-timeseries.csv.gz',
        from_file=import_job.import_file.path,
        content_type='application/gzip',
        progress=False
    )

    result = timeseries_tool.check_import(import_job)

    assert result.status == 'not_found'

    assert result.to_dict()['status'] == 'not_found'

    assert 'not_found' in result.to_html()

    timeseries_tool.storage_service.object.iter_list_all(
        'etl-import', '', params=dict(recursive=True, max_keys=900)
    )


def test_etl_import(timeseries_tool: TimeSeriesETLTool, temp_dir: str):
    """Test tool api general workflow."""
    df = pd.DataFrame(
        list(range(10)),
        index=pd.date_range(start='2020-02-02T08:10+00:00', freq='1h', periods=10)
    )

    import_name = f'unit-test-import-update-{int(datetime.now().timestamp())}'
    import_job = timeseries_tool.prepare_import(
        df, resource='r1', name=import_name, temp_dir=temp_dir
    )

    timeseries_tool.initiate_import(import_job, ResourceUpdateLevel.ALL)

    # timeseries_tool.storage_service.content.put.assert_called_with(  # type: ignore
    #     'etl-import',
    #     f'upload/{import_name}-timeseries.csv.gz',
    #     from_file=import_job.import_file.path,
    #     content_type='application/gzip'
    # )

    result = timeseries_tool.check_import(import_job)

    assert result.status == 'not_found'

    assert result.to_dict()['status'] == 'not_found'

    assert 'not_found' in result.to_html()

    timeseries_tool.storage_service.object.iter_list_all(
        'etl-import', '', params=dict(recursive=True, max_keys=900)
    )
