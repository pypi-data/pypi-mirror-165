"""Unit test for waylay.service.timeseries.parser.model."""

import pytest

import pandas as pd
from datetime import date

from waylay.service.timeseries.parser.model import TimestampFormat


TST_TIMESTAMP = pd.Timestamp('2020-09-17T01:38:59+00:00')


@pytest.mark.parametrize(
    ('spec', 'value', 'parsed', 'formatted', 'timezone', 'error'),
    [
        ('iso', '2020-09-17T01:38:59+00:00', TST_TIMESTAMP, None, None, None),
        ('s', 1600306739, TST_TIMESTAMP,  None, None, None),
        ('s', '1600306739', TST_TIMESTAMP,  1600306739, None, None),
        ('ms', 1600306739000, TST_TIMESTAMP, None,  None, None),
        ('ms', '1600306739000', TST_TIMESTAMP, 1600306739000,  None, None),
        ('us', 1600306739000000, TST_TIMESTAMP,  None, None, None),
        ('µs', '1600306739000000', TST_TIMESTAMP,  1600306739000000, None, None),
        ('ns', 1600306739000000000, TST_TIMESTAMP,  None, None, None),
        ('ns', '1600306739000000000', TST_TIMESTAMP,  1600306739000000000, None, None),
        # obvious errors
        *(
            (tt, value, None, None, None,  err)
            for tt, value, err in [
                ('ns', '2020-09-17T01:38:59+00:00', 'invalid literal'),
                ('iso', 'timestamp', 'could not convert'),
                ('iso', '20', 'could not convert'),
            ]
        ),
        # Timezone
        ('iso', '2020-09-17T01:38:59+00:00', TST_TIMESTAMP,  '2020-09-17T01:38:59+00:00',  'UTC',  None),
        ('iso', '2020-09-17T01:38:59', TST_TIMESTAMP, '2020-09-17T01:38:59+00:00', 'UTC',  None),
        ('iso', '2020-09-17T03:38:59+02:00', TST_TIMESTAMP,  '2020-09-17T03:38:59+02:00',  'Europe/Brussels',  None),
        ('iso', '2020-09-17T03:38:59', TST_TIMESTAMP,  '2020-09-17T03:38:59+02:00', 'Europe/Brussels',  None),
        # iso is very lenient
        ('iso', 1600306739000000000, None, '2020-09-17T01:38:59+00:00',  None, None),
        ('iso', '2020-09-17T01:38:59', None, '2020-09-17T01:38:59+00:00',  None, None),
        ('iso', '2020-09-17  01:38:59', None, '2020-09-17T01:38:59+00:00',  None, None),
        ('iso', '17/09/2020 01:38:59', None, '2020-09-17T01:38:59+00:00',  None, None),
        ('iso', '2020-09-17', None, '2020-09-17T00:00:00+00:00',  None, None),
        ('iso', '2020-09', None, '2020-09-01T00:00:00+00:00',  None, None),
        ('iso', '2020', None, '2020-01-01T00:00:00+00:00',  None, None),
        ('iso', '01:38:59', None,  f'{date.today()}T01:38:59+00:00', None, None),
        ('iso', '01:38', None,  f'{date.today()}T01:38:00+00:00', None, None),
    ]
)
def test_timestamp_format(spec: str, value, parsed, formatted, timezone, error):
    """Test basic parsing and formatting with the default formatters."""
    try:
        ts_format = TimestampFormat.lookup(spec)
        if value is not None:
            parser = ts_format.parser(timezone)
            if parsed is not None:
                assert parser(value) == parsed
            else:
                parsed = parser(value)
        if parsed is not None:
            formatter = ts_format.formatter(timezone)
            assert formatter(parsed) == (formatted or value)

        assert error is None
    except (TypeError, ValueError) as exc:
        if error is None:
            raise
        assert error in str(exc)
