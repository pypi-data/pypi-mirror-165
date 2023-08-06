"""Unit test model for queries utils."""
import pytest
import numpy as np
import pandas as pd
from waylay.service.queries._util.parse_util import to_pandas_freq, to_pandas_freqstr, to_iso_freq
from pandas.tseries.offsets import Day, Hour

import waylay.service.queries._util.df_parser as r

FREQUENCY_TEST_CASES = [
    [Hour(3), "PT3H"],
    [Day(10), "P10D"],
    [Day(31), "P1M"],
    [None, None]
]

ACCESSOR_TEST_CASES = [
    [pd.Timestamp("2018-01-01 00:00:00"), pd.Timestamp("2018-01-01 10:00:00"), 10, Hour(1), 10*60*60],
    [pd.Timestamp("2018-01-01 00:00:00"), pd.Timestamp("2018-01-02 00:00:00"), 24, Hour(1), 24*60*60],
    [pd.Timestamp("2018-01-01 00:00:00"), pd.Timestamp("2018-01-02 00:00:00"), 12, Hour(2), 12*120*60],
    [None, None, 0, None, None],
    [None, None, 10, None, None]
]


@pytest.fixture(params=FREQUENCY_TEST_CASES, ids=lambda t: t[0])
def prepare_settings_frequency_case(request):
    """Parametrize duration test cases."""
    return request.param


def test_to_frequency_converts(prepare_settings_frequency_case):
    """Tests the data conversion of a frequency or interval to a pandas DateOffset."""
    panda_notation, frequency = prepare_settings_frequency_case

    assert to_pandas_freqstr(frequency) == panda_notation
    assert to_pandas_freq(frequency) == panda_notation
    assert to_pandas_freq(to_iso_freq(panda_notation)) == panda_notation


@pytest.fixture(params=ACCESSOR_TEST_CASES, ids=lambda t: t[0])
def prepare_settings_accessor_case(request):
    """Parametrize index accessor test case."""
    return request.param


def test_tsa_index_accessor(prepare_settings_accessor_case):
    """Tests the tsa index accessor."""
    from_date, until_date, nr, pandas_freq, seconds = prepare_settings_accessor_case
    idx = pd.date_range(from_date, periods=nr, freq=pandas_freq) if (from_date is not None) else None
    data = np.transpose([np.linspace(1, 10, num=nr, axis=0)])
    df = pd.DataFrame(data, index=idx, columns=["A"])
    window_length_seconds = df.index.tsa.window_length.seconds + \
        df.index.tsa.window_length.days*24*60*60 if df.index.tsa.window_length is not None else None

    assert df.index.tsa.iso_freqstr == to_iso_freq(pandas_freq)
    assert df.index.tsa.pandas_freqstr == pandas_freq
    assert window_length_seconds == seconds
    assert df.index.tsa.pandas_freq == pandas_freq
    assert df.index.tsa._from == from_date
    assert df.index.tsa.until == until_date
    if isinstance(idx, pd.DatetimeIndex):
        assert df.index.tsa.window_spec["from"] == from_date
        assert df.index.tsa.window_spec["until"] == until_date
    else:
        assert df.index.tsa.window_spec is None


def test_tsa_series_accessor(prepare_settings_accessor_case):
    """Tests the tsa series accessor."""
    from_date, until_date, nr, pandas_freq, seconds = prepare_settings_accessor_case
    idx = pd.date_range(from_date, periods=nr, freq=pandas_freq) if (from_date is not None) else None
    s = pd.Series(np.linspace(1, 10, nr), index=idx)

    window_length_seconds = s.tsa.window_length.seconds + \
        s.tsa.window_length.days*24*60*60 if s.tsa.window_length is not None else None

    assert s.tsa.iso_freqstr == to_iso_freq(pandas_freq)
    assert s.tsa.pandas_freqstr == pandas_freq
    assert s.tsa.pandas_freq == pandas_freq
    assert window_length_seconds == seconds
    assert s.tsa._from == from_date
    assert s.tsa.until == until_date

    if isinstance(idx, pd.DatetimeIndex):
        assert s.tsa.window_spec["from"] == from_date
        assert s.tsa.window_spec["until"] == until_date
    else:
        assert s.tsa.window_spec is None


def test_tsa_dataframe_accessor(prepare_settings_accessor_case):
    """Tests the tsa dataframe accessor."""
    from_date, until_date, nr, pandas_freq, seconds = prepare_settings_accessor_case
    idx = pd.date_range(from_date, periods=nr, freq=pandas_freq) if (from_date is not None) else None
    data = np.transpose([np.linspace(1, 10, num=nr, axis=0)])
    df = pd.DataFrame(data, index=idx, columns=["A"])

    window_length_seconds = df.tsa.window_length.seconds + \
        df.tsa.window_length.days*24*60*60 if df.tsa.window_length is not None else None

    assert df.tsa.iso_freqstr == to_iso_freq(pandas_freq)
    assert df.tsa.pandas_freqstr == pandas_freq
    assert df.tsa.pandas_freq == pandas_freq
    assert window_length_seconds == seconds
    assert df.tsa._from == from_date
    assert df.tsa.until == until_date

    if isinstance(idx, pd.DatetimeIndex):
        assert df.tsa.window_spec["from"] == from_date
        assert df.tsa.window_spec["until"] == until_date
    else:
        assert df.tsa.window_spec is None


def test_header_renderer_datetime():
    """Tests the header renderer for datetimes."""
    idx = pd.date_range(start='1970-01-01T00:00:00Z',
                        end='1970-01-01T00:00:01Z')
    renderer = r._header_renderer(idx, key='timestamp', iso_timestamp=False)
    assert ({'timestamp': 0} == renderer(pd.Timestamp('1970-01-01T00:00:00Z')))
    assert ({'timestamp': 2010} == renderer(pd.Timestamp('1970-01-01T00:00:02.010Z')))

    renderer_iso = r._header_renderer(idx, key='timestamp', iso_timestamp=True)
    assert ({'timestamp': 0, 'timestamp_iso': '1970-01-01T00:00:00+00:00'}
           == renderer_iso(pd.Timestamp('1970-01-01T00:00:00Z')))
    assert ({'timestamp': 2010, 'timestamp_iso': '1970-01-01T00:00:02.010000+00:00'}
           == renderer_iso(pd.Timestamp('1970-01-01T00:00:02.010Z')))


def test_render_mode_compact():
    """Test renderer in compact mode."""
    df = pd.DataFrame(
        data=[[0, 1], [2, 3]],
        columns=pd.MultiIndex.from_tuples([['a', 'x'], ['b', 'x']], names=['l1', 'l2']),
        index=pd.date_range(start='2018-01-01', periods=2, freq='1d'))

    # parse time index
    df_repr = r.df(df, render_mode=r.RENDER_MODE_COMPACT)
    df_r = r.parse_df(df_repr, render_mode=r.RENDER_MODE_COMPACT)
    assert (list(df.columns.values) == list(df_r.columns.values))
    assert (list(df.index.values) == list(df_r.index.values))

    # parse summary
    df_summ = df.aggregate(['min', 'max']).reindex(columns=df.columns)
    df_summ.index.name = 'stat'
    df_summ_repr = r.df(df_summ, render_mode=r.RENDER_MODE_COMPACT)
    df_summ_r = r.parse_df(df_summ_repr, render_mode=r.RENDER_MODE_COMPACT)
    assert (list(df_summ.columns.values) == list(df_summ_r.columns.values))
    assert (list(df_summ.index.values) == list(df_summ_r.index.values))


def test_parse_row_names_and_column_index():
    """Tests the parsing of row names and column index."""
    parsed = r._parse_row_names_and_column_index(
        ['timestamp', {'resource': 'r1', 'metric': 'v1', 'aggregate': 'median'}])

    assert (
        (['timestamp'],
         pd.MultiIndex(
            names=['resource', 'metric', 'aggregate'],
            levels=[['r1'], ['v1'], ['median']],
            codes=[[0], [0], [0]]
        )) ==
        parsed)


def test_parse_row_names_and_column_index_multiple_metrics():
    """Tests the parsing of row names and column index for multiple metrics."""
    parsed = r._parse_row_names_and_column_index(
        ['timestamp', {'resource': 'r1', 'metric': 'v1', 'aggregate': 'median'},
            {'resource': 'r1', 'metric': 'v2', 'aggregate': 'median'}])

    assert (2 == len(parsed))
    assert (['timestamp'] == parsed[0])
    pd.testing.assert_index_equal(parsed[1], pd.MultiIndex(
        names=['resource', 'metric', 'aggregate'],
        levels=[['r1'], ['v1', 'v2'], ['median']],
        codes=[[0, 0], [0, 1], [0, 0]]))


def test_parse_row_names_and_column_index_alternate_sorting():
    """Tests the parsing of row names and column index with alternate sorting."""
    parsed = r._parse_row_names_and_column_index(
        ['timestamp', {'aggregate': 'median', 'metric': 'v1', 'resource': 'r1'}])

    assert (
        (['timestamp'],
            pd.MultiIndex(
                names=['resource', 'metric', 'aggregate'],
                levels=[['r1'], ['v1'], ['median']],
                codes=[[0], [0], [0]]
        )) ==
        parsed)


def test_parse_row_names_and_column_index_multiple_metrics_alternate_sorting():
    """Tests the parsing of row names and column index for multiple metrics with alternate sorting."""
    parsed = r._parse_row_names_and_column_index(
        ['timestamp', {'aggregate': 'median', 'metric': 'v1', 'resource': 'r1'},
            {'aggregate': 'median', 'resource': 'r1', 'metric': 'v2', }])

    assert (2 == len(parsed))
    assert (['timestamp'] == parsed[0])
    pd.testing.assert_index_equal(parsed[1], pd.MultiIndex(
        names=['resource', 'metric', 'aggregate'],
        levels=[['r1'], ['v1', 'v2'], ['median']],
        codes=[[0, 0], [0, 1], [0, 0]]))
