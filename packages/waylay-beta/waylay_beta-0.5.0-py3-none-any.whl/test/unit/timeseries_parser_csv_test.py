"""Test timeseries specification parser."""

import io
import gzip
from datetime import tzinfo, timedelta

from waylay.service.timeseries.parser.model import TimestampFormat

from pathlib import Path

import pandas as pd
import pytest

from waylay.service.timeseries.parser import (
    prepare_etl_import,
    create_etl_import,
    ETLFile,
)

from waylay.service.timeseries.parser.model import (
    Resource, Metric,
    fromisoformat,
    ParserRequestError,
)

from timeseries_parser_fixtures import (
    SERIES_LENGTH,
    assert_import_has_timeseries,
    default_timeseries_data,
    temp_dir  # import needed for parameter injection
)

TIMESERIES_YEAR = 2000
TIMESERIES_YEAR_UNIX_MILLI = (pd.to_datetime(str(TIMESERIES_YEAR)) - pd.Timestamp('1970')) // pd.Timedelta('1ms')
HOUR_MILLI = 3600000

TIMESERIES_YEAR_UNIX_SEC = TIMESERIES_YEAR_UNIX_MILLI / 1000
HOUR_SEC = HOUR_MILLI / 1000

TIMESERIES_YEAR_UNIX_MICRO = TIMESERIES_YEAR_UNIX_MILLI * 1000
HOUR_MICRO = HOUR_MILLI * 1000

TIMESERIES_YEAR_UNIX_NANO = TIMESERIES_YEAR_UNIX_MICRO * 1000
HOUR_NANO = HOUR_MICRO * 1000


@pytest.fixture
def csv_path(tmpdir, timestamp_format: TimestampFormat):
    """Return path to a temporary csv file containing timeseries values."""
    csv_input_file_name = f'{tmpdir}/input.csv'
    timestamp_format.formatter()
    if timestamp_format == TimestampFormat.ISO:
        timestamps = [f'{TIMESERIES_YEAR}-01-01T0{t}:00:00+00:00' for t in range(SERIES_LENGTH)]
        pd.DataFrame(
            list((i, i) for i in range(SERIES_LENGTH)),
            index=pd.DatetimeIndex(timestamps, name='timestamp'),
            columns=['test_metric_1', 'test_metric_2'],
        ).to_csv(csv_input_file_name)

    elif timestamp_format == TimestampFormat.NANOS:
        timestamps = [TIMESERIES_YEAR_UNIX_NANO + HOUR_NANO * t for t in range(SERIES_LENGTH)]
        create_csv_file(csv_input_file_name, timestamps, unit='ns')

    elif timestamp_format == TimestampFormat.MICROS:
        timestamps = [TIMESERIES_YEAR_UNIX_MICRO + HOUR_MICRO * t for t in range(SERIES_LENGTH)]
        create_csv_file(csv_input_file_name, timestamps, unit='us')

    elif timestamp_format == TimestampFormat.MILLIS:
        timestamps = [TIMESERIES_YEAR_UNIX_MILLI + HOUR_MILLI * t for t in range(SERIES_LENGTH)]
        create_csv_file(csv_input_file_name, timestamps, unit='ms')

    elif timestamp_format == TimestampFormat.SECONDS:
        timestamps = [TIMESERIES_YEAR_UNIX_SEC + HOUR_SEC * t for t in range(SERIES_LENGTH)]
        create_csv_file(csv_input_file_name, timestamps, unit='s')

    return Path(csv_input_file_name)


def create_csv_file(csv_path, timestamps, unit):
    """Create a timeseries DataFrame and export to a csv file."""
    pd.DataFrame(
        list((i, i) for i in range(SERIES_LENGTH)),
        index=pd.DatetimeIndex([pd.Timestamp(timestamp, unit=unit) for timestamp in timestamps], name='timestamp'),
        columns=['test_metric_1', 'test_metric_2'],
    ).to_csv(csv_path)


UNIX_TIMESTAMP_FORMATS = [TimestampFormat.SECONDS,
                          TimestampFormat.MILLIS, TimestampFormat.MICROS, TimestampFormat.NANOS]
ALL_TIMESTAMP_FORMATS = UNIX_TIMESTAMP_FORMATS + [TimestampFormat.ISO]


@pytest.mark.parametrize('timestamp_format', UNIX_TIMESTAMP_FORMATS)
def test_csv_simple(csv_path):
    """Test parsing of a simple CSV input."""
    csv_dir = csv_path.parent
    etl_import = prepare_etl_import(
        csv_path, resource='test_resource',
        import_file=ETLFile(directory=csv_dir)
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import, default_timeseries_data(year=TIMESERIES_YEAR))


@pytest.mark.parametrize('timestamp_format', ALL_TIMESTAMP_FORMATS)
def test_csv_gzip(csv_path):
    """Test parsing of a gzipped csv."""
    csv_dir = csv_path.parent
    csv_input_file_name_gzip = str(csv_path) + '.gz'
    with open(csv_path, 'rt') as csv_in:
        with gzip.open(csv_input_file_name_gzip, 'wt') as csv_out:
            for line in csv_in:
                csv_out.write(line)
    etl_import = prepare_etl_import(
        csv_input_file_name_gzip, resource='test_resource',
        import_file=ETLFile(prefix='gzipped', directory=csv_dir)
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import, default_timeseries_data(year=TIMESERIES_YEAR))


@pytest.mark.parametrize('timestamp_format', ALL_TIMESTAMP_FORMATS)
def test_csv_as_text(csv_path):
    """Test parsing of a csv as text stream."""
    csv_dir = csv_path.parent
    with open(csv_path, 'rt') as csv_io:
        etl_import = prepare_etl_import(
            csv_io, resource='test_resource',
            import_file=ETLFile(prefix='from-stream', directory=csv_dir)
        )
        etl_import = create_etl_import(etl_import)
        assert_import_has_timeseries(etl_import, default_timeseries_data(year=TIMESERIES_YEAR))


@pytest.mark.parametrize('timestamp_format', [TimestampFormat.ISO])
def test_import_as_parsed_string_ISO(csv_path):
    """Test parsing of a parsed string csv iterable."""
    csv_dir = csv_path.parent
    parsed_lines = [
        ('timestamp', 'test_metric_1', 'test_metric_2'),
        (f'{TIMESERIES_YEAR}-01-01 00:00:00+00:00', '0', '0'),
        (f'{TIMESERIES_YEAR}-01-01 01:00:00+00:00', '1', '1'),
        (f'{TIMESERIES_YEAR}-01-01 02:00:00+00:00', '2', '2')
    ]
    etl_import = prepare_etl_import(
        parsed_lines, resource='test_resource',
        import_file=ETLFile(prefix='from-parsed', directory=csv_dir)
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import, default_timeseries_data(year=TIMESERIES_YEAR))


@pytest.mark.parametrize('timestamp_format', [TimestampFormat.NANOS])
def test_import_as_parsed_string_unix_nano(csv_path):
    """Test parsing of a parsed string csv iterable."""
    csv_dir = csv_path.parent
    parsed_lines = [
        ('timestamp', 'test_metric_1', 'test_metric_2'),
        (TIMESERIES_YEAR_UNIX_NANO, '0', '0'),
        (TIMESERIES_YEAR_UNIX_NANO + HOUR_NANO, '1', '1'),
        (TIMESERIES_YEAR_UNIX_NANO + HOUR_NANO * 2, '2', '2')
    ]
    etl_import = prepare_etl_import(
        parsed_lines, resource='test_resource',
        import_file=ETLFile(prefix='from-parsed', directory=csv_dir)
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import, default_timeseries_data(year=TIMESERIES_YEAR))


@pytest.mark.parametrize('timestamp_format', [TimestampFormat.MICROS])
def test_import_as_parsed_string_unix_micro(csv_path):
    """Test parsing of a parsed string csv iterable."""
    csv_dir = csv_path.parent
    parsed_lines = [
        ('timestamp', 'test_metric_1', 'test_metric_2'),
        (TIMESERIES_YEAR_UNIX_MICRO, '0', '0'),
        (TIMESERIES_YEAR_UNIX_MICRO + HOUR_MICRO, '1', '1'),
        (TIMESERIES_YEAR_UNIX_MICRO + HOUR_MICRO * 2, '2', '2')
    ]
    etl_import = prepare_etl_import(
        parsed_lines, resource='test_resource',
        import_file=ETLFile(prefix='from-parsed', directory=csv_dir)
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import, default_timeseries_data(year=TIMESERIES_YEAR))


@pytest.mark.parametrize('timestamp_format', [TimestampFormat.MILLIS])
def test_import_as_parsed_string_unix_milli(csv_path):
    """Test parsing of a parsed string csv iterable."""
    csv_dir = csv_path.parent
    parsed_lines = [
        ('timestamp', 'test_metric_1', 'test_metric_2'),
        (TIMESERIES_YEAR_UNIX_MILLI, '0', '0'),
        (TIMESERIES_YEAR_UNIX_MILLI + HOUR_MILLI, '1', '1'),
        (TIMESERIES_YEAR_UNIX_MILLI + HOUR_MILLI * 2, '2', '2')
    ]
    etl_import = prepare_etl_import(
        parsed_lines, resource='test_resource',
        import_file=ETLFile(prefix='from-parsed', directory=csv_dir)
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import, default_timeseries_data(year=TIMESERIES_YEAR))


@pytest.mark.parametrize('timestamp_format', [TimestampFormat.SECONDS])
def test_import_as_parsed_string_unix_sec(csv_path):
    """Test parsing of a parsed string csv iterable."""
    csv_dir = csv_path.parent
    parsed_lines = [
        ('timestamp', 'test_metric_1', 'test_metric_2'),
        (TIMESERIES_YEAR_UNIX_SEC, '0', '0'),
        (TIMESERIES_YEAR_UNIX_SEC + HOUR_SEC, '1', '1'),
        (TIMESERIES_YEAR_UNIX_SEC + HOUR_SEC * 2, '2', '2')
    ]
    etl_import = prepare_etl_import(
        parsed_lines, resource='test_resource',
        import_file=ETLFile(prefix='from-parsed', directory=csv_dir)
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import, default_timeseries_data(year=TIMESERIES_YEAR))


@pytest.mark.parametrize('timestamp_format', [TimestampFormat.ISO])
def test_import_as_parsed_values_ISO(csv_path):
    """Test parsing of parsed values csv iterable."""
    csv_dir = csv_path.parent
    parsed_lines = [
        ('timestamp', 'test_metric_1', 'test_metric_2'),
        (fromisoformat(f'{TIMESERIES_YEAR}-01-01T00:00:00+00:00'), 0, 0),
        (pd.Timestamp(f'{TIMESERIES_YEAR}-01-01T01:00:00+00:00'), 1, 1),
        (f'{TIMESERIES_YEAR}-01-01T02:00:00+00:00', 2, 2.0)
    ]
    etl_import = prepare_etl_import(
        parsed_lines, resource='test_resource',
        import_file=ETLFile(prefix='from-parsed-values', directory=csv_dir)
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import, default_timeseries_data(year=TIMESERIES_YEAR))


@pytest.mark.parametrize('timestamp_format', [TimestampFormat.NANOS])
def test_import_as_parsed_values_unix_nano(csv_path):
    """Test parsing of parsed values csv iterable."""
    csv_dir = csv_path.parent
    parsed_lines = [
        ('timestamp', 'test_metric_1', 'test_metric_2'),
        (TIMESERIES_YEAR_UNIX_NANO, 0, 0),
        (TIMESERIES_YEAR_UNIX_NANO + HOUR_NANO * 1, 1, 1),
        (TIMESERIES_YEAR_UNIX_NANO + HOUR_NANO * 2, 2, 2.0)
    ]
    etl_import = prepare_etl_import(
        parsed_lines, resource='test_resource',
        import_file=ETLFile(prefix='from-parsed-values', directory=csv_dir)
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import, default_timeseries_data(year=TIMESERIES_YEAR))


@pytest.mark.parametrize('timestamp_format', [TimestampFormat.MICROS])
def test_import_as_parsed_values_unix_micro(csv_path):
    """Test parsing of parsed values csv iterable."""
    csv_dir = csv_path.parent
    parsed_lines = [
        ('timestamp', 'test_metric_1', 'test_metric_2'),
        (TIMESERIES_YEAR_UNIX_MICRO, 0, 0),
        (TIMESERIES_YEAR_UNIX_MICRO + HOUR_MICRO * 1, 1, 1),
        (TIMESERIES_YEAR_UNIX_MICRO + HOUR_MICRO * 2, 2, 2.0)
    ]
    etl_import = prepare_etl_import(
        parsed_lines, resource='test_resource',
        import_file=ETLFile(prefix='from-parsed-values', directory=csv_dir)
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import, default_timeseries_data(year=TIMESERIES_YEAR))


@pytest.mark.parametrize('timestamp_format', [TimestampFormat.MILLIS])
def test_import_as_parsed_values_unix_milli(csv_path):
    """Test parsing of parsed values csv iterable."""
    csv_dir = csv_path.parent
    parsed_lines = [
        ('timestamp', 'test_metric_1', 'test_metric_2'),
        (TIMESERIES_YEAR_UNIX_MILLI, 0, 0),
        (TIMESERIES_YEAR_UNIX_MILLI + HOUR_MILLI * 1, 1, 1),
        (TIMESERIES_YEAR_UNIX_MILLI + HOUR_MILLI * 2, 2, 2.0)
    ]
    etl_import = prepare_etl_import(
        parsed_lines, resource='test_resource',
        import_file=ETLFile(prefix='from-parsed-values', directory=csv_dir)
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import, default_timeseries_data(year=TIMESERIES_YEAR))


@pytest.mark.parametrize('timestamp_format', [TimestampFormat.SECONDS])
def test_import_as_parsed_values_unix_sec(csv_path):
    """Test parsing of parsed values csv iterable."""
    csv_dir = csv_path.parent
    parsed_lines = [
        ('timestamp', 'test_metric_1', 'test_metric_2'),
        (TIMESERIES_YEAR_UNIX_SEC, 0, 0),
        (TIMESERIES_YEAR_UNIX_SEC + HOUR_SEC * 1, 1, 1),
        (TIMESERIES_YEAR_UNIX_SEC + HOUR_SEC * 2, 2, 2.0)
    ]
    etl_import = prepare_etl_import(
        parsed_lines, resource='test_resource',
        import_file=ETLFile(prefix='from-parsed-values', directory=csv_dir)
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import, default_timeseries_data(year=TIMESERIES_YEAR))


@pytest.mark.parametrize('timestamp_format', [TimestampFormat.ISO])
def test_csv_unparsed_string_iterable_ISO(csv_path):
    """Test parsing of a simple CSV input."""
    csv_dir = csv_path.parent
    unparsed_lines = [
        'timestamp,test_metric_1,test_metric_2',
        f'{TIMESERIES_YEAR}-01-01 00:00:00+00:00,0,0',
        f'{TIMESERIES_YEAR}-01-01 01:00:00+00:00,1,1',
        f'{TIMESERIES_YEAR}-01-01 02:00:00+00:00,2,2'
    ]
    etl_import = prepare_etl_import(
        unparsed_lines, resource='test_resource',
        import_file=ETLFile(prefix='from-unparsed', directory=csv_dir)
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import, default_timeseries_data(year=TIMESERIES_YEAR))


@pytest.mark.skip(reason='Not compatible with unix timestamps.')
@pytest.mark.parametrize('timestamp_format', [TimestampFormat.MILLIS])
def test_csv_unparsed_string_iterable_unix_milli(csv_path):
    """Test parsing of a simple CSV input."""
    csv_dir = csv_path.parent
    unparsed_lines = [
        'timestamp,test_metric_1,test_metric_2',
        '0,0,0',
        '3600,1,1',
        '7200,2,2'
    ]
    etl_import = prepare_etl_import(
        unparsed_lines, resource='test_resource',
        import_file=ETLFile(prefix='from-unparsed', directory=csv_dir)
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import)


def test_csv_import_wrong_iterable(temp_dir):
    """Test failure with interable of numbers."""
    with pytest.raises(ParserRequestError) as exc_info:
        prepare_etl_import(
            list(range(10)),
            resource='test_resource',
            import_file=ETLFile(prefix='wrong-input', directory=temp_dir)
        )
    assert 'Cannot read first line' in format(exc_info.value)


class _FixedTZInfo(tzinfo):
    def __init__(self, hours=0, minutes=0, seconds=0):
        self.delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def tzname(self, dt):
        return f'{self.delta}'

    def utcoffset(self, dt):
        return self.delta

    def dst(self, dt):
        return 0


CSV_IMPORT_TEST_CASES = [
    ('multi_column', dict(resource='test_resource'), (
        "timestamp,test_metric_1,test_metric_2\n"
        "1970-01-01 00:00:00+00:00,0,0\n"
        "1970-01-01 01:00:00+00:00,1,1\n"
        "1970-01-01 02:00:00+00:00,2,2\n"
    )),
    ('multi_column_local_tz', dict(resource='test_resource', timestamp_timezone=_FixedTZInfo(hours=2)), (
        "timestamp,test_metric_1,test_metric_2\n"
        "1970-01-01 02:00:00,0,0\n"
        "1970-01-01 03:00:00,1,1\n"
        "1970-01-01 04:00:00,2,2\n"
    )),
    ('multi_column_local_tz_default_UTC', dict(resource='test_resource'), (
        "timestamp,test_metric_1,test_metric_2\n"
        "1970-01-01 00:00:00,0,0\n"
        "1970-01-01 01:00:00,1,1\n"
        "1970-01-01 02:00:00,2,2\n"
    )),
    ('value_column', dict(resource='test_resource', value_column='value'), (
        "timestamp,metric,value\n"
        "1970-01-01 00:00:00+00:00,test_metric_1,0\n"
        "1970-01-01 00:00:00+00:00,test_metric_2,0\n"
        "1970-01-01 01:00:00+00:00,test_metric_1,1\n"
        "1970-01-01 01:00:00+00:00,test_metric_2,1\n"
        "1970-01-01 02:00:00+00:00,test_metric_1,2\n"
        "1970-01-01 02:00:00+00:00,test_metric_2,2\n"
    )),
    ('resource_column', dict(timestamp_column='t', resource_column='r', metric_column='m', value_column='v'), (
        "r,t,m,v\n"
        "test_resource,1970-01-01T00:00:00+00:00,test_metric_1,0\n"
        "test_resource,1970-01-01T00:00:00+00:00,test_metric_2,0\n"
        "test_resource,1970-01-01T01:00:00+00:00,test_metric_1,1\n"
        "test_resource,1970-01-01T01:00:00+00:00,test_metric_2,1\n"
        "test_resource,1970-01-01T02:00:00+00:00,test_metric_1,2\n"
        "test_resource,1970-01-01T02:00:00+00:00,test_metric_2,2\n"
    )),
    ('resource_columns', dict(timestamp_column='t', resource_column='r'), (
        "r,t,test_metric_1,test_metric_2\n"
        "test_resource,1970-01-01 00:00:00+00:00,0,0\n"
        "test_resource,1970-01-01 01:00:00+00:00,1,1\n"
        "test_resource,1970-01-01 02:00:00+00:00,2,2\n"
    )),
    ('export_format', dict(), (
        "resource,metric,timestamp,value\n"
        "test_resource,waylay.resourcemessage.metric.test_metric_1,1970-01-01T00:00:00.000Z,0\n"
        "test_resource,waylay.resourcemessage.metric.test_metric_1,1970-01-01T01:00:00.000Z,1\n"
        "test_resource,waylay.resourcemessage.metric.test_metric_1,1970-01-01T02:00:00.000Z,2\n"
        "test_resource,waylay.resourcemessage.metric.test_metric_2,1970-01-01T00:00:00.000Z,0\n"
        "test_resource,waylay.resourcemessage.metric.test_metric_2,1970-01-01T01:00:00.000Z,1\n"
        "test_resource,waylay.resourcemessage.metric.test_metric_2,1970-01-01T02:00:00.000Z,2\n"
    )),
    ('export_format_with_empty_values', dict(), (
        "resource,metric,timestamp,value\n"
        "test_resource,test_metric_1,1970-01-01T00:00:00.000Z,0\n"
        "test_resource,test_metric_1,1970-01-01T00:30:00.000Z,\n"
        "test_resource,test_metric_1,1970-01-01T01:00:00.000Z,1\n"
        "test_resource,test_metric_1,1970-01-01T01:30:00.000Z,\n"
        "test_resource,test_metric_1,1970-01-01T02:00:00.000Z,2\n"
        "test_resource,test_metric_2,1970-01-01T00:00:00.000Z,0\n"
        "test_resource,test_metric_2,1970-01-01T01:00:00.000Z,1\n"
        "test_resource,test_metric_2,1970-01-01T02:00:00.000Z,2\n"
    )),
    (
        'export_format filtered',
        dict(
            resources=['test_resource'],
            metrics=['test_metric_1', 'test_metric_2']
        ), (
            "resource,metric,timestamp,value\n"
            "test_resource_0,waylay.resourcemessage.metric.test_metric_1,1970-01-01T00:00:00.000Z,0\n"
            "test_resource_0,waylay.resourcemessage.metric.test_metric_2,1970-01-01T00:00:00.000Z,0\n"
            "test_resource_0,waylay.resourcemessage.metric.test_metric_3,1970-01-01T00:00:00.000Z,0\n"
            "test_resource,waylay.resourcemessage.metric.test_metric_1,1970-01-01T00:00:00.000Z,0\n"
            "test_resource,waylay.resourcemessage.metric.test_metric_1,1970-01-01T01:00:00.000Z,1\n"
            "test_resource,waylay.resourcemessage.metric.test_metric_1,1970-01-01T02:00:00.000Z,2\n"
            "test_resource,waylay.resourcemessage.metric.test_metric_2,1970-01-01T00:00:00.000Z,0\n"
            "test_resource,waylay.resourcemessage.metric.test_metric_2,1970-01-01T01:00:00.000Z,1\n"
            "test_resource,waylay.resourcemessage.metric.test_metric_2,1970-01-01T02:00:00.000Z,2\n"
            "test_resource,waylay.resourcemessage.metric.test_metric_3,1970-01-01T00:00:00.000Z,0\n"
            "test_resource,waylay.resourcemessage.metric.test_metric_3,1970-01-01T01:00:00.000Z,1\n"
            "test_resource,waylay.resourcemessage.metric.test_metric_3,1970-01-01T02:00:00.000Z,2\n"

        )
    ),
    ('mapped resource-metric',
        dict(
            metrics=[
                Metric('test_metric_1', key='m_1'),
                Metric('test_metric_2', key='m_2')
            ],
            resources=[Resource('test_resource', key='0')]
        ),
        (
            "resource,timestamp,m_1,m_2\n"
            "0,1970-01-01 00:00:00+00:00,0,0\n"
            "0,1970-01-01 01:00:00+00:00,1,1\n"
            "0,1970-01-01 02:00:00+00:00,2,2\n"
        )
     ),
]


@pytest.fixture(params=CSV_IMPORT_TEST_CASES[:], ids=lambda t: t[0])
def csv_import_case(request):
    """Get test case for csv conversion."""
    return request.param


def test_csv_import(csv_import_case, temp_dir):
    """Test conversion of csv input."""
    case_name, import_args, csv_text = csv_import_case
    etl_import = prepare_etl_import(
        io.StringIO(csv_text),
        import_file=ETLFile(prefix=case_name, directory=temp_dir),
        **import_args
    )
    etl_import = create_etl_import(etl_import)
    assert_import_has_timeseries(etl_import)


INPUT_SETTINGS_CSV_TEST_CASES = [
    # case name, args,  csv header,  validation error
    ['normalized_default',  {}, "resource,metric,timestamp,value+nr,m,2020-05-01,0", None],
    ['missing timestamp column',  {}, 'resource,metric,value', 'No timestamp column found'],
    [
        'wrong timestamp column',
        dict(timestamp_column='ts'),
        'timestamp,resource,metric,value', 'not in csv header'
    ],
    [
        'timestamp timezone',
        dict(timestamp_timezone='Europe/Brussels'),
        "timestamp,resource,metric,value\n2020-05-01,r,m,0", None
    ],
    [
        'timestamp offset iso',
        dict(timestamp_offset='-P1D'),
        "timestamp,resource,metric,value\n2020-05-01,r,m,0", None
    ],
    [
        'timestamp offset invalid iso',
        dict(timestamp_offset='-PT1D'),
        "timestamp,resource,metric,value\n2020-05-01,r,m,0", 'Unable to parse duration'
    ],
    [
        'timestamp offset pandas',
        dict(timestamp_offset='-1h'),
        "timestamp,resource,metric,value\n2020-05-01,r,m,0", None
    ],
    [
        'missing resource',
        dict(value_column='value'),
        "timestamp,metric,value\n2020-05-01,m,0", 'No valid resource'
    ],
    [
        'default resource column',
        dict(value_column='value'),
        "timestamp,resource,metric,value\n2020-05-01,r,m,0", None
    ],
    [
        'missing default resource column',
        dict(),
        "timestamp,no_resource,metric,value\n2020-05-01,r,m,0", 'No valid resource'
    ],
    [
        'wrong resource column',
        dict(resource_column='abc'),
        "timestamp,metric,value\n2020-05-01,m,0", 'Invalid resource column'
    ],
    [
        'wrong metric column',
        dict(resource='r', metric_column='abc'),
        "timestamp,value\n2020-05-01,0", 'Invalid metric column'
    ],
    [
        'wrong value key',
        dict(resource='r', value_column='abc'),
        "timestamp,value\n2020-05-01,0", 'not in csv header'
    ],
    [
        'no metric or metric key',
        dict(resource='r', value_column='value'),
        "timestamp,value\n2020-05-01,0", 'No valid metric'
    ],
    [
        'filter metrics',
        dict(resource='r', metric_column='m', value_column='v', metrics=['m1']),
        "timestamp,m,v\n2020-05-01,m1,0", None
    ],
    [
        'empty filter metrics',
        dict(resource='r', metric_column='m', value_column='v', metrics=['m1']),
        "timestamp,m,v\n2020-05-01,m2,0", None
    ],
    [
        'ignore empty lines',
        dict(resource='r', metric_column='m', value_column='v', metrics=['m1']),
        "timestamp,m,v\n\n2020-05-01,m1,0\n\n\n", None
    ],
    [
        'wrong filter on metric columns',
        dict(resource='r', metrics=['m1']),
        "timestamp,m2\n\n2020-05-01,0\n\n\n", 'found in the csv header'
    ],
    [
        'resource filter',
        dict(
            resource_column='resource',
            resources=['r1'],
            metrics=['temperature']
        ),
        (
            "resource,timestamp,temperature,humidity\n"
            "r1,2021-03-01T00:00Z,-1,203\n"
            "r2,2021-03-01T03:00Z,-2,201\n"
            "r1,2021-03-01T06:00Z,3,221\n"
            "r2,2021-03-01T09:00Z,10,223\n"
            "r1,2021-03-01T12:00Z,15,243\n"
            "r2,2021-03-01T15:00Z,21,183\n"
            "r1,2021-03-01T18:00Z,14,203\n"
            "r2,2021-03-01T21:00Z,8,200\n"
        ),
        None
    ],
    [
        'etl export format',
        dict(metrics=['activeScore']),
        (
            "resource,metric,timestamp,value\n"
            "fitbitsimulator.00574,waylay.resourcemessage.metric.activeScore,2021-02-21T14:27:02.391Z,-1\n"
            "fitbitsimulator.00574,waylay.resourcemessage.metric.activeScore,2021-02-21T14:48:34.300Z,2\n"
            "fitbitsimulator.00574,waylay.resourcemessage.metric.activeScore,2021-02-21T14:49:10.541Z,2\n"
        ),
        None
    ],
    [
        'local timestamps',
        dict(timestamp_timezone='UTC'),
        (
            "resource,metric,timestamp,value\n"
            "fitbitsimulator.00574,activeScore,2021-02-21T14:27:02.391,-1\n"
        ),
        None
    ]
]


@pytest.fixture(params=INPUT_SETTINGS_CSV_TEST_CASES[:], ids=lambda t: t[0])
def prepare_settings_csv_case(request):
    """Parametrize csv input test cases."""
    return request.param


def test_prepare_settings_csv(prepare_settings_csv_case, temp_dir):
    """Test csv input specifications."""
    case_name, import_args, csv_text, error_text = prepare_settings_csv_case

    try:
        etl_import = prepare_etl_import(
            io.StringIO(csv_text+"\n"),
            import_file=ETLFile(prefix=case_name, directory=temp_dir),
            **import_args
        )
        create_etl_import(etl_import)
        if error_text:
            raise AssertionError(f'expected a failure: {error_text}')

    except ParserRequestError as e:
        if error_text:
            assert error_text in format(e)
        else:
            raise e
