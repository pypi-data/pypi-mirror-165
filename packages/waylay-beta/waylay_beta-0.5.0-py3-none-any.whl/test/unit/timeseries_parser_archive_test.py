"""Test etl-imports of archive files."""

import csv
import gzip
import math
import os

from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from random import random
from tarfile import TarFile
from zipfile import ZipFile

import pytest

from timeseries_parser_fixtures import (
    ArchiveSettings,
    assert_import_has_timeseries,
    default_multiple_timeseries_data
)

from waylay.service.timeseries.parser.model import WaylayETLSeriesImport

from waylay.service.timeseries.parser import (
    create_etl_import,
    prepare_etl_import,
)


def generate_csv_file(
    tmp_dir,
    file_name=None,
    headers=['timestamp', 'test_metric_1', 'test_metric_2']
) -> str:
    """Generate a csv file."""
    current_timestamp = datetime.now(timezone.utc)
    file_name = file_name or f'upload/example-{current_timestamp:%Y%m%d.%H%M%S}.csv'
    file_name = Path(tmp_dir, file_name)
    os.makedirs(file_name.parents[0], exist_ok=True)

    with open(file_name, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)

        one_day_ago = current_timestamp - timedelta(days=1)
        for minutes in range(0, 24 * 60, 15):
            writer.writerow([
                (one_day_ago + timedelta(minutes=minutes)).isoformat().replace('+00:00', 'Z'),
                100 * math.sin(minutes/500) + 5 * random(),
                100 * math.sin(minutes/500) + 5 * random(),
            ])
    return str(file_name)


def generate_csv_file_archive(
    archive_settings=ArchiveSettings()
):
    """Generate an archive containing csv files and timeseries files."""
    file_name_archive = get_file_name_from_archive_settings(archive_settings)
    os.makedirs(file_name_archive.parents[0], exist_ok=True)

    with open_archive(file_name_archive, archive_settings) as archive:
        add_csv_file_to_archive(archive, archive_settings)
        add_timeseries_file_to_archive(archive, archive_settings)

    return str(file_name_archive)


def add_csv_file_to_archive(archive, archive_settings):
    """
    Add some csv files to the archive in input.

    Amount of csv files and metrics are available in archive_settings.
    """
    for idx, (resource, metric, series) in enumerate(default_multiple_timeseries_data(
        archive=archive_settings
    )):
        write_to_archive = write_file_to_zip if archive_settings.extension == 'zip' else write_file_to_tar
        file_name = resource + '.csv'
        file_path = Path(archive_settings.tmp_dir, file_name)
        with open(file_path, 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            if divmod(idx, archive_settings.amount_of_metrics)[1] == 0:
                csv_writer.writerow(('resource', 'timestamp', 'metric', 'value'))
            for t, v in series:
                csv_writer.writerow((resource, t.isoformat(), metric, f'{v}'))

        if divmod(idx + 1, archive_settings.amount_of_metrics)[1] == 0:
            write_to_archive(file_path, file_name, archive)


def write_file_to_zip(file_path, file_name, archive):
    """Write a file to a zip archive."""
    archive.write(file_path, arcname=file_name)


def write_file_to_tar(file_path, file_name, archive):
    """Write a file to a tar archive."""
    archive.add(file_path, arcname=file_name)


def get_file_name_from_archive_settings(archive_settings):
    """Create a file_name from archive settings."""
    return Path(
        archive_settings.tmp_dir,
        f'upload/example-{archive_settings.timestamp:%Y%m%d.%H%M%S}.{archive_settings.extension}'
    )


@contextmanager
def open_archive(file_name, archive_settings):
    """Open an archive object to write files."""
    open_object = _open_zip_archive if archive_settings.extension == 'zip' else _open_tar_archive
    yield from open_object(file_name)


def _open_zip_archive(file_name):
    """Open a zip archive to write files."""
    with ZipFile(file_name, 'w') as zip_archive:
        yield zip_archive


def _open_tar_archive(file_name):
    """Open a tar archive to write files."""
    with TarFile.open(file_name, 'w') as tar_archive:
        yield tar_archive


def add_timeseries_file_to_archive(archive, archive_settings):
    """Add some timeseries files to the archive in input.

    Amount of timeseries files and metrics are available in archive_settings.
    """
    archive_settings.is_timeseries = True
    for idx, (resource, metric, series) in enumerate(default_multiple_timeseries_data(
        archive=archive_settings
    )):
        write_to_archive = write_file_to_zip if archive_settings.extension == 'zip' else write_file_to_tar

        start_idx = len('timeseries_unit_test_')
        end_idx = len('-timeseries.csv')
        file_number = resource[start_idx:-end_idx]

        file_name = f'file-{file_number}-timeseries.csv.gz'
        file_path = Path(archive_settings.tmp_dir, file_name)
        with gzip.open(file_path, 'at') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            if divmod(idx, archive_settings.amount_of_metrics)[1] == 0:
                csv_writer.writerow(('resource', 'metric', 'timestamp', 'value'))
            for t, v in series:
                csv_writer.writerow((resource, metric, t.isoformat(), f'{v}'))

        if divmod(idx + 1, archive_settings.amount_of_metrics)[1] == 0:
            write_to_archive(file_path, file_name, archive)


@pytest.fixture
def example_csv_archive(tmpdir, amount_of_files, amount_of_metrics, extension):
    """Fixture which creates an archive file."""
    archive_settings = ArchiveSettings(
        amount_of_files=amount_of_files,
        amount_of_metrics=amount_of_metrics,
        timestamp=CURRENT_TIMESTAMP,
        tmp_dir=tmpdir,
        extension=extension
    )
    file_name = generate_csv_file_archive(archive_settings)
    return file_name


CURRENT_TIMESTAMP = datetime.now(timezone.utc)


@pytest.mark.parametrize('extension', ['zip', 'tar', 'tgz'])
@pytest.mark.parametrize('amount_of_files, amount_of_metrics', [(5, 5), (5, 1), (1, 5), (1, 1)])
def test_archive_import(example_csv_archive, amount_of_files, amount_of_metrics):
    """Test etl-import of archive files existing of csv files and timeseries files."""
    start = datetime.now()
    etl_import = prepare_etl_import(example_csv_archive)
    assert isinstance(etl_import, WaylayETLSeriesImport)

    etl_import = create_etl_import(etl_import)
    etl_import_path = Path(etl_import.import_file.directory, etl_import.import_file.prefix + '-timeseries.csv.gz')
    assert os.path.exists(etl_import_path)

    print(f'Took {datetime.now() - start} seconds.')
    assert_import_has_timeseries(etl_import, default_multiple_timeseries_data(
        archive=ArchiveSettings(
            amount_of_files=amount_of_files*2,  # One for csv file and one for -timeseries.csv.gz
            amount_of_metrics=amount_of_metrics,
            timestamp=CURRENT_TIMESTAMP,
            is_target=True
        )
    ))
