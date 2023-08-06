"""Unit tests for the series export tool."""
import io
import math
import tempfile
import os
import zipfile
import tarfile

from typing import (
    Any, Iterator, List, Mapping, Optional, Sequence, Tuple,
    Callable, Union
)
from pathlib import Path

import pandas as pd

import pytest

from waylay.service.data.series import SeriesResource
from waylay.service.timeseries import SeriesSettings, Resource, Metric
from waylay.service.timeseries.parser.model import ArchiveType, CSVOutput, CSVWriteable, Measurement
import waylay.service.timeseries.parser.export_series as export_series

SeriesMockData = Mapping[Tuple[str, str], List[List[Any]]]


@pytest.fixture
def series_data() -> SeriesMockData:
    """Create a series data set per resource,metric type."""
    return {
        ('r1', 'm1'): [[0, 123], [1000, 124], [2000, 125]],
        ('r1', 'm2'): [[0, 223], [1000, 224], [2000, 225]],
        ('r1', 'm3'): [[1000, 324], [1500, 325], [2000, 326], [2500, 327]],
        ('r2', 'm1'): [[0, 2123], [1000, 2124], [2000, 2125]],
        ('r3', 'text'): [[0, 'test 1'], [1000, 'test, 2'], [2000, '{"message": ["json","value"]}']],
    }


def _measurements_for(
    series_data: SeriesMockData, resource_id: str, metric_name: str
) -> Sequence[Measurement]:
    return list(
        (pd.Timestamp(t, unit='ms', tz='UTC'), v)
        for [t, v] in series_data.get((resource_id, metric_name), [])
    )


@pytest.fixture
def series_api(series_data: SeriesMockData) -> SeriesResource:
    """Create a mock SeriesResource."""
    series_resource = SeriesResource()

    def _mock_iter_export(resource_id: str, metric: str, **kwargs):
        params = kwargs.pop('params', {})
        _from = params.get('from', -math.inf)
        _until = params.get('until', math.inf)
        for entry in series_data.get((resource_id, metric), []):
            timestamp = entry[0]
            if timestamp >= _from and timestamp < _until:
                yield entry

    def _mock_export_with_links(resource_id: str, metric: str, select_path='?', **kwargs):
        params = kwargs.pop('params', {})
        assert select_path is None
        if 'next_call' in params:
            return {'series': []}
        return {
            'series': list(_mock_iter_export(resource_id, metric, params=params, **kwargs)),
            '_links': {'next': {'href': '?next_call=true'}}
        }

    series_resource.iter_export = _mock_iter_export
    series_resource.export = _mock_export_with_links
    return series_resource


def test_series_mock(series_api: SeriesResource):
    """Validate correct setup of the series_api mock."""
    assert next(series_api.iter_export('r1', 'm1')) == [0, 123]
    assert next(series_api.iter_export('r?', 'm?'), 'nodata') == 'nodata'


def test_iter_series_export_single(series_api: SeriesResource, series_data: SeriesMockData):
    """Test the export_series.create_export_series_provider function."""
    settings = SeriesSettings(resource='r1', metric='m1')
    series_provider = export_series.create_export_series_provider(settings, series_api)
    assert ('r1', 'm1') in series_provider

    assert list(series_provider[('r1', 'm1')]) == _measurements_for(series_data, 'r1', 'm1')
    assert len(series_provider) == 1


def test_iter_series_export_multiple(series_api: SeriesResource, series_data: SeriesMockData):
    """Test the export_series.create_export_series_provider function on multiple resource and metrics."""
    resource_ids = ['r1', 'r?']
    metric_names = ['m1', 'm2', 'm?']
    settings = SeriesSettings(resources=resource_ids, metrics=metric_names)
    series_provider = export_series.create_export_series_provider(settings, series_api)

    for (resource_id, metric_name), measures_iterable in series_provider.items():
        assert resource_id in resource_ids
        assert metric_name in metric_names
        measures = list(measures_iterable)

        assert bool(measures) == bool((resource_id, metric_name) in series_data.keys())
        if measures:
            assert list(measures) == _measurements_for(series_data, resource_id, metric_name)


def _to_millis(t):
    return int(t.timestamp() * 1000)


def _to_seconds(t):
    return int(t.timestamp())


# settings args, expected csv, expected denormalised csv (values column)
TEST_EXPORT_TO_CSV_CASES = [
    (
        dict(
            resource='r1', metric='m1'
        ), (
            'm1\r\n'
            '123\r\n'
            '124\r\n'
            '125\r\n'
        ), (
            'V\r\n'
            '123\r\n'
            '124\r\n'
            '125\r\n'
        )
    ),
    (
        dict(
            resource='r1', metric='m1',
            timestamp_column='timestamp'
        ), (
            'timestamp,m1\r\n'
            '1970-01-01T00:00:00+00:00,123\r\n'
            '1970-01-01T00:00:01+00:00,124\r\n'
            '1970-01-01T00:00:02+00:00,125\r\n'
        ), (
            'timestamp,V\r\n'
            '1970-01-01T00:00:00+00:00,123\r\n'
            '1970-01-01T00:00:01+00:00,124\r\n'
            '1970-01-01T00:00:02+00:00,125\r\n'
        )
    ),
    (
        dict(
            resource='r1', metric='m1',
            timestamp_column='timestamp',
            timestamp_from=pd.Timestamp('1970-01-01T00:00:01+00:00'),
            timestamp_until=pd.Timestamp('1970-01-01T00:00:02+00:00')
        ), (
            'timestamp,m1\r\n'
            '1970-01-01T00:00:01+00:00,124\r\n'
        ), (
            'timestamp,V\r\n'
            '1970-01-01T00:00:01+00:00,124\r\n'
        )
    ),
    (
        dict(
            resource='r1', metric='m1',
            timestamp_column='timestamp', resource_column='resource'
        ), (
            'resource,timestamp,m1\r\n'
            'r1,1970-01-01T00:00:00+00:00,123\r\n'
            'r1,1970-01-01T00:00:01+00:00,124\r\n'
            'r1,1970-01-01T00:00:02+00:00,125\r\n'
        ), (
            'resource,timestamp,V\r\n'
            'r1,1970-01-01T00:00:00+00:00,123\r\n'
            'r1,1970-01-01T00:00:01+00:00,124\r\n'
            'r1,1970-01-01T00:00:02+00:00,125\r\n'
        )
    ),
    (
        dict(
            resource='r1', metric='m1',
            metric_column='metric',
        ), (
            'm1\r\n'
            '123\r\n'
            '124\r\n'
            '125\r\n'
        ), (
            'metric,V\r\n'
            'm1,123\r\n'
            'm1,124\r\n'
            'm1,125\r\n'
        )
    ),
    (
        dict(
            resource='r1', metric='m1',
            timestamp_column='timestamp',
            timestamp_formatter=_to_seconds
        ), (
            'timestamp,m1\r\n'
            '0,123\r\n'
            '1,124\r\n'
            '2,125\r\n'
        ), (
            'timestamp,V\r\n'
            '0,123\r\n'
            '1,124\r\n'
            '2,125\r\n'
        )
    ),
    (
        dict(
            resources=['r1'], metrics=['m1', 'm2']
        ), (
            'm1,m2\r\n'
            '123,223\r\n'
            '124,224\r\n'
            '125,225\r\n'
        ), (
            'metric,V\r\n'
            'm1,123\r\n'
            'm1,124\r\n'
            'm1,125\r\n'
            'm2,223\r\n'
            'm2,224\r\n'
            'm2,225\r\n'
        )
    ),
    (
        dict(
            resources=['r1', 'r?'], metrics=['m1', 'm2', 'm?']
        ), (
            'resource,m1,m2,m?\r\n'
            'r1,123,223,\r\n'
            'r1,124,224,\r\n'
            'r1,125,225,\r\n'
        ), (
            'resource,metric,V\r\n'
            'r1,m1,123\r\n'
            'r1,m1,124\r\n'
            'r1,m1,125\r\n'
            'r1,m2,223\r\n'
            'r1,m2,224\r\n'
            'r1,m2,225\r\n'
        )
    ),
    (
        dict(
            resources=['r1'], metrics=['m1', 'm2', 'm3'],
            timestamp_column='t',
            timestamp_formatter=_to_millis
        ), (
            't,m1,m2,m3\r\n'
            '0,123,223,\r\n'
            '1000,124,224,324\r\n'
            '1500,,,325\r\n'
            '2000,125,225,326\r\n'
            '2500,,,327\r\n'
        ), (
            'metric,t,V\r\n'
            'm1,0,123\r\n'
            'm1,1000,124\r\n'
            'm1,2000,125\r\n'
            'm2,0,223\r\n'
            'm2,1000,224\r\n'
            'm2,2000,225\r\n'
            'm3,1000,324\r\n'
            'm3,1500,325\r\n'
            'm3,2000,326\r\n'
            'm3,2500,327\r\n'
        )
    ),
    (
        dict(
            resources=[Resource('r1', key='R1')],
            metrics=list(
                Metric(m, key=m.upper()) for m in ['m1', 'm2', 'm3']
            ),
            resource_column='R',
            metric_column='M',
            timestamp_column='T',
            timestamp_formatter=lambda t: int(t.timestamp() * 1000)
        ), (
            'R,T,M1,M2,M3\r\n'
            'R1,0,123,223,\r\n'
            'R1,1000,124,224,324\r\n'
            'R1,1500,,,325\r\n'
            'R1,2000,125,225,326\r\n'
            'R1,2500,,,327\r\n'
        ), (
            'R,M,T,V\r\n'
            'R1,M1,0,123\r\n'
            'R1,M1,1000,124\r\n'
            'R1,M1,2000,125\r\n'
            'R1,M2,0,223\r\n'
            'R1,M2,1000,224\r\n'
            'R1,M2,2000,225\r\n'
            'R1,M3,1000,324\r\n'
            'R1,M3,1500,325\r\n'
            'R1,M3,2000,326\r\n'
            'R1,M3,2500,327\r\n'
        )
    ),
    (
        dict(
            resource='r3',
            metric='text'
        ), (
            'text\r\n'
            'test 1\r\n'
            '"test, 2"\r\n'
            '"{""message"": [""json"",""value""]}"\r\n'
        ), (
            'V\r\n'
            'test 1\r\n'
            '"test, 2"\r\n'
            '"{""message"": [""json"",""value""]}"\r\n'
        )
    )
]


@pytest.mark.parametrize(
    "settings,expected_csv", [
        pytest.param(
            SeriesSettings(**settings_dict),
            expected_column_csv,
            id='C:'+'-'.join(str(v) for v in settings_dict.values())
        )
        for settings_dict, expected_column_csv, _ in TEST_EXPORT_TO_CSV_CASES[:]
    ] + [
        pytest.param(
            SeriesSettings(**settings_dict, value_column='V'),
            expected_value_csv,
            id='V:'+'-'.join(str(v) for v in settings_dict.values())
        )
        for settings_dict, _, expected_value_csv in TEST_EXPORT_TO_CSV_CASES[:]
    ]
)
def test_export_csv_to_file(
    settings: SeriesSettings,
    expected_csv: str,
    series_api: SeriesResource
):
    """Test export to CSV stream."""
    series_provider = export_series.PagingExportSeriesProvider(settings, series_api)
    csv_buffer = io.StringIO()
    export_series.export_csv_to_file(csv_buffer, settings, series_provider)
    assert csv_buffer.getvalue() == expected_csv


def test_export_csv_to_file_filtered_settings(
    series_api: SeriesResource
):
    """Test that settings filter on resource and metric during export."""
    settings = SeriesSettings(resources=['r1', 'r2'], metrics=['m1', 'm2'])
    series_provider = export_series.PagingExportSeriesProvider(settings, series_api)
    csv_buffer = io.StringIO()
    export_settings = SeriesSettings(resource='r1', metric='m1', value_column='V')
    export_series.export_csv_to_file(csv_buffer, export_settings, series_provider)
    assert csv_buffer.getvalue() == (
        'V\r\n'
        '123\r\n'
        '124\r\n'
        '125\r\n'
    )


@pytest.fixture(scope='session')
def temp_dir() -> Iterator[Path]:
    """Get a temporary directory as fixture."""
    test_temp_dir = os.getenv('TEST_TEMP_DIR')
    if test_temp_dir:
        yield Path(test_temp_dir)
    else:
        with tempfile.TemporaryDirectory() as test_temp_dir:
            yield Path(test_temp_dir)


@pytest.mark.parametrize(
    "path_name,per_resource,archive_type,supported", [
        *(
            (name, pr, at, at in fails_except_for and (at.supports_multiple_files or not pr))
            for at in list(ArchiveType)
            for pr in [True, False]
            for name, fails_except_for in (
                (f'{at}-{pr}-with-suffix.csv', [ArchiveType.TEXT]),
                (f'{at}-{pr}-with-suffix.gz', [ArchiveType.GZ]),
                (f'{at}-{pr}-with-suffix.zip', [ArchiveType.ZIP]),
                (f'{at}-{pr}-with-suffix.tar', [ArchiveType.TAR]),
                (f'{at}-{pr}-with-suffix.tar.gz', [ArchiveType.TAR_GZ]),
            )
        ),
        *(
            (f'{at}-{pr}-no-suffix', pr, at, at.supports_multiple_files or not pr)
            for at in list(ArchiveType)
            for pr in [True, False]
        )
    ])
def test_export_csv_with_path(
    path_name: Path,
    per_resource: bool,
    archive_type: Optional[ArchiveType],
    supported: bool,
    series_api: SeriesResource,
    temp_dir: Path
):
    """Test the creation of an export archive."""
    settings = SeriesSettings(
        metrics=['m1', 'm2'], resources=['r1', 'r2'], timestamp_column='timestamp',
        per_resource=per_resource
    )
    series_provider = export_series.PagingExportSeriesProvider(settings, series_api)
    export_path = temp_dir / path_name
    try:
        export_series.export_csv(
            export_path, settings, series_provider,
            archive_type=archive_type,
        )

        assert supported
        assert export_path.exists(), export_path
        assert export_path.is_dir() == (archive_type in (ArchiveType.DIR, ArchiveType.DIR_GZ))
    except (ValueError, TypeError) as e:
        assert not supported, e
        assert not export_path.exists(), export_path


PAGING_EXPORT_PROVIDER_LENGTH_TEST_CASES: List[Tuple[Mapping, int]] = [
    ({}, 0),
    ({'metric': 'm1'}, 0),
    ({'resource': 'r1'}, 0),
    ({'metric': 'm1', 'resource': 'r1'}, 1),
    ({'metric': 'm1', 'resource': 'r1', 'metrics': [], 'resources': []}, 1),
    ({'resource': 'r1', 'metrics': ['m1', 'm2'], 'resources': ['r1', 'r2']}, 2),
    ({'metric': 'm1', 'metrics': ['m1', 'm2'], 'resources': ['r1', 'r2']}, 2),
    ({'metrics': ['m1', 'm2'], 'resources': ['r1', 'r2']}, 4),
    ({'resources': ['r1', 'r2']}, 0),
    ({'metrics': ['m1', 'm2']}, 0),
]


@pytest.mark.parametrize(
    "settings,expected_length", [
        (SeriesSettings(**settings_args), expected_length)
        for settings_args, expected_length
        in PAGING_EXPORT_PROVIDER_LENGTH_TEST_CASES
    ])
def test_paging_export_provider_length(
    settings: SeriesSettings,
    expected_length: int,
    series_api: SeriesResource
):
    """Test __len__ function of PagingExportSeriesProvider."""
    series_provider = export_series.PagingExportSeriesProvider(settings, series_api)

    assert len(series_provider) == expected_length


EMPTY_ZIP_LEN = 22


@pytest.mark.parametrize(
    "per_resource,archive_type,success", [
        (True, None, True),
        (False, None, True),
        *(
            (pr, at, at is ArchiveType.ZIP)
            for pr in [True, False]
            for at in list(ArchiveType)
        )
    ])
def test_export_to_provided_zipfile(
    per_resource: bool,
    archive_type: ArchiveType,
    success: bool,
    series_api: SeriesResource,
):
    """Test csv export to zipfile."""
    settings = SeriesSettings(
        metrics=['m1', 'm2'], resources=['r1', 'r2'], timestamp_column='timestamp',
        per_resource=per_resource
    )
    series_provider = export_series.PagingExportSeriesProvider(settings, series_api)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode='w') as zip_file_write:
        try:
            export_series.export_csv(zip_file_write, settings, series_provider, archive_type)
            assert success
        except (ValueError, TypeError) as e:
            assert not success, e

    bytes_written = zip_buffer.tell()
    assert (bytes_written > EMPTY_ZIP_LEN) if success else (bytes_written == EMPTY_ZIP_LEN)

    zip_buffer.seek(0)
    with zipfile.ZipFile(zip_buffer, mode='r') as zip_file_read:
        assert zip_file_read.namelist() == \
            [] if not success \
            else ['r1.csv', 'r2.csv'] if per_resource \
            else ['series.csv']


@pytest.mark.parametrize(
    "per_resource,archive_type,success", [
        (True, None, True),
        (False, None, True),
        *(
            (pr, at, at in (ArchiveType.TAR, ArchiveType.TAR_GZ))
            for pr in [True, False]
            for at in list(ArchiveType)
        )
    ])
def test_export_to_provided_tarfile(
    per_resource: bool,
    archive_type: ArchiveType,
    success: bool,
    series_api: SeriesResource,
):
    """Test csv export to tarfile."""
    settings = SeriesSettings(
        metrics=['m1', 'm2'], resources=['r1', 'r2'], timestamp_column='timestamp',
        per_resource=per_resource
    )
    series_provider = export_series.PagingExportSeriesProvider(settings, series_api)

    tar_buffer = io.BytesIO()
    compressed = (archive_type == ArchiveType.TAR_GZ)
    with tarfile.open(fileobj=tar_buffer, mode='w:gz' if compressed else 'w') as tar_file_write:
        try:
            export_series.export_csv(tar_file_write, settings, series_provider, archive_type)
            assert success
        except (ValueError, TypeError) as e:
            assert not success, e

    bytes_written = tar_buffer.tell()

    if compressed:
        assert bytes_written < 500, f'{bytes_written} bytes written'
    elif success:
        assert (bytes_written == tarfile.RECORDSIZE), f'{bytes_written} bytes written'
    else:
        assert (bytes_written == tarfile.RECORDSIZE), f'{bytes_written} bytes written'

    tar_buffer.seek(0)
    with tarfile.open(fileobj=tar_buffer, mode='r:*') as tar_file_read:
        assert tar_file_read.getnames() == \
            [] if not success \
            else ['r1.csv', 'r2.csv'] if per_resource \
            else ['series.csv']


class _CSVWritableExample:
    def __init__(self):
        self.text_buffer = io.StringIO()

    def write(self, value: str):
        return self.text_buffer.write(value)

    def seek(self, *args, **kwargs):
        return self.text_buffer.seek(*args, **kwargs)

    def tell(self):
        return self.text_buffer.tell()

    def read(self):
        return self.text_buffer.read()


@pytest.mark.parametrize(
    "per_resource,archive_type,success", [
        (True, None, False),
        (False, None, True),
        *(
            (pr, at, at in (ArchiveType.TEXT) and not pr)
            for pr in [True, False]
            for at in list(ArchiveType)
        )
    ])
@pytest.mark.parametrize(
    "create_buffer",
    [io.StringIO, lambda: io.TextIOWrapper(io.BytesIO()), _CSVWritableExample]
)
def test_export_to_provided_textio(
    per_resource: bool,
    archive_type: ArchiveType,
    success: bool,
    create_buffer: Callable[[], Union[_CSVWritableExample, io.TextIOBase]],
    series_api: SeriesResource,
):
    """Test csv export to textio."""
    settings = SeriesSettings(
        metrics=['m1', 'm2'], resources=['r1', 'r2'],
        timestamp_column='timestamp', per_resource=per_resource
    )
    series_provider = export_series.PagingExportSeriesProvider(settings, series_api)

    text_buffer = create_buffer()
    try:
        export_series.export_csv(text_buffer, settings, series_provider, archive_type)
        assert success
    except (ValueError, TypeError) as e:
        assert not success, e

    bytes_written = text_buffer.tell()

    assert (bytes_written > 0) if success else (bytes_written == 0), f'{bytes_written} bytes written'

    if success:
        text_buffer.seek(0)
        assert text_buffer.read().startswith(
            'resource,timestamp,m1,m2'
        )


@pytest.mark.parametrize(
    "output_constructor,archive_type,error_text", [
        *(
            (list, at, 'Unsupported output') for at in ArchiveType
        ),
        (list, None, 'Unsupported output'),
    ])
def test_unsupported_combinations(
    output_constructor: Callable[[], CSVOutput],
    archive_type: Optional[ArchiveType],
    error_text: str,
    series_api: SeriesResource,
):
    """Test unsupported archivetype and output combinations."""
    settings = SeriesSettings(metrics=['m1', 'm2'], resources=['r1', 'r2'], timestamp_column='timestamp')
    series_provider = export_series.PagingExportSeriesProvider(settings, series_api)

    with pytest.raises((ValueError, TypeError)) as e:
        export_series.export_csv(output_constructor(), settings, series_provider, archive_type=archive_type)

    assert error_text in str(e)


def test_unsupported_zipfile_combination(
    series_api: SeriesResource
):
    """Test zipfile is incompatible with TEXT archivetype."""
    settings = SeriesSettings(metrics=['m1', 'm2'], resources=['r1', 'r2'], timestamp_column='timestamp')
    series_provider = export_series.PagingExportSeriesProvider(settings, series_api)

    with zipfile.ZipFile(io.BytesIO(), mode='w') as zip_file:
        with pytest.raises((ValueError, TypeError)) as e:
            export_series.export_csv(zip_file, settings, series_provider, archive_type=ArchiveType.TEXT)

    assert 'not supported' in str(e)


@pytest.mark.parametrize(
    "per_resource,archive_type,success", [
        (True, None, True),
        (False, None, True),
        *(
            (
                pr,
                at,
                at not in (ArchiveType.DIR, ArchiveType.DIR_GZ)
                and (
                    not pr or at not in (ArchiveType.TEXT, ArchiveType.GZ)
                )
            )
            for pr in [True, False]
            for at in list(ArchiveType)
        )
    ])
def test_export_to_provided_io_stream(
    per_resource: bool,
    archive_type: ArchiveType,
    success: bool,
    series_api: SeriesResource,
):
    """Test csv export to binary stream."""
    settings = SeriesSettings(
        metrics=['m1', 'm2'], resources=['r1', 'r2'], timestamp_column='timestamp',
        per_resource=per_resource
    )
    series_provider = export_series.PagingExportSeriesProvider(settings, series_api)

    bytes_buffer = io.BytesIO()
    try:
        export_series.export_csv(bytes_buffer, settings, series_provider, archive_type)
        assert success
    except (ValueError, TypeError) as e:
        assert not success, e

    assert not bytes_buffer.closed

    if success:
        assert bytes_buffer.tell() > 0
    else:
        assert bytes_buffer.tell() == 0
