import os
from pathlib import Path
from typing import Generator, cast

import pymysql
import pytest
from pytest import FixtureRequest, MonkeyPatch

from .connect import mock_connect
from .util import DatabaseMock, Mode


def pytest_addoption(parser: pytest.Parser) -> None:
    """
    Add the command line options for the plugin.

    Parameters
    ----------
    parser: `pytest.Parser`
        Option parser.
    """
    group = parser.getgroup("pytest-pymysql-autorecord")
    group.addoption(
        "--store-db-data",
        action="store_true",
        dest="store_db_data",
        help="Store the database data in a file for mocking.",
    )
    group.addoption(
        "--mock-db-data",
        action="store_true",
        dest="mock_db_data",
        help="Use previously stored data instead of connecting to the database.",
    )
    group.addoption(
        "--db-data-dir",
        action="store",
        dest="db_data_dir",
        help="Directory where to store the recorded data files.",
    )


@pytest.fixture(autouse=True)
def database_mock(
    request: FixtureRequest, monkeypatch: MonkeyPatch
) -> Generator[DatabaseMock, None, None]:
    """
    Mock PyMySQL's connect function.

    The behaviour of the mock connect function is chosen with a command line argument:

    * If pytest is run with the ``--store-db-data`` flag, PyMySQL's ``connect`` function
      is used for the database queries and the results are stored in a file. Existing
      files are overwritten.
    * If pytest is run with the ``--mock-db-data`` flag, no connection to a database is
      made and the previously stored data is used instead.
    * If neither the ``--store-db-data`` nor the ``--mock-db-data`` flag is used,
      PyMySQL's ``connect`` function is used without any changes.

    A test fails if you use the ``--mock-db-data`` flag, but no data has been stored for
    the test yet.

    The ``--store-db-data`` and ``--mock-db-data`` flag cannot be used together. If you
    use either of them, you have to use the ``--db-data-dir`` flag as well. Its value
    must be the path of the directory where the recorded data files are stored. This
    directory is created if necessary. Alternatively, you can set the environment
    variable ``PMSM_DB_DATA_DIR``.

    Parameters
    ----------
    original_datadir: `~pathlib.Path`
        The directory containing the test file.
    request: `~pytest.FixtureRequest`
        The pytest request details.
    monkeypatch: `~pytest.MonkeyPatch`
        Object for monkeypatching.
    """
    is_storing = request.config.option.store_db_data
    is_mocking = request.config.option.mock_db_data
    db_data_dir = (
        Path(request.config.option.db_data_dir)
        if request.config.option.db_data_dir
        else None
    )
    if not db_data_dir and os.getenv("PMSM_DATA_DIR") is not None:
        db_data_dir = Path(cast(str, os.getenv("PMSM_DATA_DIR")))

    if is_storing and is_mocking:
        pytest.fail(
            "The command line flags --store-db-data and --mock-db-data are "
            "mutually exclusive."
        )
    if (is_storing or is_mocking) and not db_data_dir:
        pytest.fail(
            "The command line option --db-data-dir must be used with the "
            "--store-db-data or --mock-db-data flag. Alternatively, you can "
            "set the environment variable PMSM_DATA_DIR."
        )

    if is_storing:
        mode = Mode.STORE_DATA
    elif is_mocking:
        mode = Mode.MOCK
    else:
        mode = Mode.NORMAL

    os.environ["PMSM_MODE"] = mode.value

    db_mock_fixture = DatabaseMock(mode, db_data_dir, request)
    connect = mock_connect(db_mock_fixture, pymysql.connect)
    monkeypatch.setattr(pymysql, "connect", connect)

    yield db_mock_fixture

    if is_storing:
        db_mock_fixture._write_data()
