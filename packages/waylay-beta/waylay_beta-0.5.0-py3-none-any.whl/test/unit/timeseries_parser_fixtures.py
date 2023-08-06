"""Timeseries parser test utitlities."""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import tempfile
import pytest

from waylay.service.timeseries.parser import (
    WaylayETLSeriesImport,
    read_etl_import,
)
from waylay.service.timeseries.parser.model import (
    MeasurementIterator,
    SeriesIterator,
    fromisoformat,
)
DONE = 'done'


@pytest.fixture
def temp_dir():
    """Create (and cleanup) a temporary directory."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


def assert_timeseries_equal(timeseries_1: MeasurementIterator, timeseries_2: MeasurementIterator):
    """Assert that two measurement iterators are identical.

    Consumes the iterators.
    """
    while True:
        t_1, v_1 = next(timeseries_1, (DONE, None))
        t_2, v_2 = next(timeseries_2, (DONE, None))
        if t_1 == DONE and t_2 == DONE:
            return
        assert t_1 == t_2, f'{t_1} == {t_2}'
        assert v_1 == v_2, f'{v_1} == {v_2}'


def assert_timeseries_data_equal(timeseries_1: SeriesIterator, timeseries_2: SeriesIterator):
    """Assert that two timeseries iterators are identical."""
    while True:
        r_1, m_1, d_1 = next(timeseries_1, (DONE, None, None))
        r_2, m_2, d_2 = next(timeseries_2, (DONE, None, None))
        if r_1 == DONE and r_2 == DONE:
            return
        assert r_1 == r_2, f'{r_1} == {r_2}'
        assert m_1 == m_2, f'{m_1} == {m_2}'
        if d_1 is not None and d_2 is not None:
            assert_timeseries_equal(d_1, d_2)
        else:
            assert d_1 is None and d_2 is None, f'{d_1} is None and {d_2} is None'


def assert_import_has_timeseries(etl_import: WaylayETLSeriesImport, timeseries: SeriesIterator = None):
    """Assert that a timeseries etl file has the given (or default) series in it."""
    with read_etl_import(etl_import) as timeseries_from_zip:
        assert_timeseries_data_equal(timeseries_from_zip, timeseries or default_timeseries_data())


SERIES_LENGTH = 3


def default_timeseries_data(metric_prefix: str = '', year='1970') -> SeriesIterator:
    """Generate a dataset with two series.

    Test utility.
    """
    def timeseries():
        for i in range(SERIES_LENGTH):
            yield fromisoformat(f'{year}-01-01T0{i}:00:00+00:00'), i

    yield 'test_resource', f'{metric_prefix}test_metric_1', timeseries()
    yield 'test_resource', f'{metric_prefix}test_metric_2', timeseries()


@dataclass
class ArchiveSettings:
    """Group settings of the archive to be generated."""

    amount_of_files: int = 1
    amount_of_metrics: int = 1
    timestamp: datetime = datetime.now(timezone.utc)
    tmp_dir: str = ''
    extension: str = 'zip'
    is_timeseries: bool = False
    is_target: bool = False


def default_multiple_timeseries_data(
    archive: ArchiveSettings = ArchiveSettings(),
    metric_prefix: str = '',
) -> SeriesIterator:
    """Generate a dataset with parametrizable series.

    Test utility.
    """
    def timeseries():
        days = 1
        x_days_ago = archive.timestamp - timedelta(days=days)
        for enum, minutes in enumerate(range(0, 24 * 60 * days, 15)):
            yield fromisoformat(
                (x_days_ago + timedelta(minutes=minutes))
                .replace(second=0, microsecond=0)
                .isoformat()
            ), enum

    for file_number in range(archive.amount_of_files):
        # First half of target files are csv files
        # Second half of target files are -timeseries.csv.gz files
        # In current unit tests
        for metric_number in range(archive.amount_of_metrics):
            if archive.is_timeseries:
                yield (
                    f'timeseries_unit_test_{file_number}-timeseries.csv',
                    f'{metric_prefix}test_metric_{metric_number + 1}',
                    timeseries()
                )
            elif archive.is_target and file_number >= archive.amount_of_files / 2:
                yield (
                    f'timeseries_unit_test_{int(file_number - archive.amount_of_files / 2)}-timeseries.csv',
                    f'{metric_prefix}test_metric_{metric_number + 1}',
                    timeseries()
                )
            else:
                yield f'csv_unit_test_{file_number}', f'{metric_prefix}test_metric_{metric_number + 1}', timeseries()
