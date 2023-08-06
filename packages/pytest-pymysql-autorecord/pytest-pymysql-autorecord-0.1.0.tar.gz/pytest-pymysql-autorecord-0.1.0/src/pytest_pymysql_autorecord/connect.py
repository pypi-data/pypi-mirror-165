from typing import Any

import pymysql
from pymysql import err
from pymysql.protocol import MysqlPacket

from .util import DatabaseMock, Mode


class _MockCursor:
    def __init__(self, database_mock: DatabaseMock):
        self._database_mock = database_mock

    def _read(self, key: str) -> Any:
        value = self._database_mock._read_value(f"cursor--{key}")
        if isinstance(value, Exception):
            raise value
        return value

    @property
    def connection(self) -> Any:
        return self._connection

    @connection.setter
    def connection(self, value: Any) -> None:
        self._connection = value

    @property
    def description(self) -> Any:
        return self._read("description")

    @description.setter
    def description(self, value: Any) -> None:
        pass

    @property
    def rownumber(self) -> Any:
        return self._read("rownumber")

    @rownumber.setter
    def rownumber(self, value: Any) -> None:
        pass

    @property
    def rowcount(self) -> Any:
        return self._read("rowcount")

    @rowcount.setter
    def rowcount(self, value: Any) -> None:
        pass

    @property
    def arraysize(self) -> Any:
        return self._read("arraysize")

    @arraysize.setter
    def arraysize(self, value: Any) -> None:
        pass

    @property
    def lastrowid(self) -> Any:
        return self._read("lastrowid")

    @lastrowid.setter
    def lastrowid(self, value: Any) -> None:
        pass

    @property
    def max_stmt_length(self) -> Any:
        return self._read("max_stmt_length")

    def close(self) -> None:
        pass

    def __enter__(self) -> Any:
        return self

    def __exit__(self, *exc_info: Any) -> None:
        del exc_info
        pass

    def setinputsizes(self, *args: Any) -> None:
        pass

    def setoutputsizes(self, *args: Any) -> None:
        pass

    def nextset(self) -> Any:
        return self._read("nextset")

    def mogrify(self, query: Any, args: Any = None) -> Any:
        return self._read("mogrify")

    def execute(self, query: Any, args: Any = None) -> Any:
        return self._read("execute")

    def executemany(self, query: Any, args: Any) -> Any:
        return self._read("executemany")

    def callproc(self, procname: Any, args: Any = ()) -> Any:
        return self._read("callproc")

    def fetchone(self) -> Any:
        return self._read("fetchone")

    def fetchmany(self, size: Any = None) -> Any:
        return self._read("fetchmany")

    def fetchall(self) -> Any:
        return self._read("fetchall")

    def scroll(self, value: Any, mode: Any = "relative") -> None:
        pass

    def __iter__(self) -> Any:
        return iter(self.fetchone, None)

    Warning = err.Warning
    Error = err.Error
    InterfaceError = err.InterfaceError
    DatabaseError = err.DatabaseError
    DataError = err.DataError
    OperationalError = err.OperationalError
    IntegrityError = err.IntegrityError
    InternalError = err.InternalError
    ProgrammingError = err.ProgrammingError
    NotSupportedError = err.NotSupportedError


class _RecordingCursor:
    def __init__(
        self, database_mock: DatabaseMock, cursorclass: Any, *args: Any, **kwargs: Any
    ):
        self._database_mock = database_mock
        self._cursor = cursorclass(*args, **kwargs)

    def _record(self, key: str, f: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            res = f(*args, **kwargs)
            self._database_mock._record_value(f"cursor--{key}", res)
        except Exception as e:
            self._database_mock._record_value(f"cursor--{key}", e)
            raise
        return res

    @property
    def connection(self) -> Any:
        return self._record("connection", lambda: self._cursor.connection)

    @connection.setter
    def connection(self, value: Any) -> None:
        self._cursor.connection = value

    @property
    def description(self) -> Any:
        return self._record("description", lambda: self._cursor.description)

    @description.setter
    def description(self, value: Any) -> None:
        self._cursor.description = value

    @property
    def rownumber(self) -> Any:
        return self._record("rownumber", lambda: self._cursor.rownumber)

    @rownumber.setter
    def rownumber(self, value: Any) -> None:
        self._cursor.rownumber = value

    @property
    def rowcount(self) -> Any:
        return self._record("rowcount", lambda: self._cursor.rowcount)

    @rowcount.setter
    def rowcount(self, value: Any) -> None:
        self._cursor.rowcount = value

    @property
    def arraysize(self) -> Any:
        return self._record("arraysize", lambda: self._cursor.arraysize)

    @arraysize.setter
    def arraysize(self, value: Any) -> None:
        self._cursor.arraysize = value

    @property
    def lastrowid(self) -> Any:
        return self._record("lastrowid", lambda: self._cursor.lastrowid)

    @lastrowid.setter
    def lastrowid(self, value: Any) -> Any:
        self._cursor.lastrowid = value

    @property
    def max_stmt_length(self) -> Any:
        return self._record("max_stmt_length", lambda: self._cursor.max_stmt_length)

    def close(self) -> None:
        self._cursor.close()

    def __enter__(self) -> Any:
        return self._cursor

    def __exit__(self, *exc_info: Any) -> None:
        del exc_info
        self._cursor.close()

    def setinputsizes(self, *args: Any) -> None:
        pass

    def setoutputsizes(self, *args: Any) -> None:
        pass

    def nextset(self) -> Any:
        return self._record("nextset", self._cursor.nextset)

    def mogrify(self, query: Any, args: Any = None) -> Any:
        return self._record("mogrify", self._cursor.mogrify, query, args)

    def execute(self, query: Any, args: Any = None) -> Any:
        return self._record("execute", self._cursor.execute, query, args)

    def executemany(self, query: Any, args: Any) -> Any:
        return self._record("executemany", self._cursor.executemany, query, args)

    def callproc(self, procname: Any, args: Any = ()) -> Any:
        return self._record("callproc", self._cursor.callproc, procname, args)

    def fetchone(self) -> Any:
        return self._record("fetchone", self._cursor.fetchone)

    def fetchmany(self, size: Any = None) -> Any:
        return self._record("fetchmany", self._cursor.fetchmany, size)

    def fetchall(self) -> Any:
        return self._record("fetchall", self._cursor.fetchall)

    def scroll(self, value: Any, mode: Any = "relative") -> Any:
        self._record("scroll", self._cursor.scroll, value, mode)

    def __iter__(self) -> Any:
        return iter(self.fetchone, None)

    Warning = err.Warning
    Error = err.Error
    InterfaceError = err.InterfaceError
    DatabaseError = err.DatabaseError
    DataError = err.DataError
    OperationalError = err.OperationalError
    IntegrityError = err.IntegrityError
    InternalError = err.InternalError
    ProgrammingError = err.ProgrammingError
    NotSupportedError = err.NotSupportedError


class _MockConnection:
    def __init__(self, database_mock: DatabaseMock):
        self._database_mock = database_mock

    def _read(self, key: str) -> Any:
        return self._database_mock._read_value(f"connection--{key}")

    def __enter__(self) -> Any:
        return self

    def __exit__(self, *exc_info: Any) -> None:
        del exc_info
        self.close()

    def close(self) -> None:
        pass

    @property
    def open(self) -> Any:
        return self._read("open")

    def _force_close(self) -> None:
        pass

    __del__ = _force_close

    def autocommit(self, value: Any) -> None:
        pass

    def get_autocommit(self) -> Any:
        return self._read("get_autocommit")

    def _read_ok_packet(self) -> None:
        pass

    def _send_autocommit_mode(self) -> None:
        pass

    def begin(self) -> None:
        pass

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    def show_warnings(self) -> Any:
        return self._read("show_warnings")

    def select_db(self, db: Any) -> None:
        pass

    def escape(self, obj: Any, mapping: Any = None) -> Any:
        return self._read("escape")

    def literal(self, obj: Any) -> Any:
        return self._read("literal")

    def escape_string(self, s: Any) -> Any:
        return self._read("escape_string")

    def cursor(self, cursor: Any = None) -> Any:
        return _MockCursor(database_mock=self._database_mock)

    def kill(self, thread_id: Any) -> Any:
        return self._read("kill")

    def ping(self, reconnect: bool = True) -> None:
        pass

    def set_charset(self, charset: Any) -> None:
        pass

    def connect(self, sock: Any = None) -> None:
        pass

    def write_packet(self, payload: Any) -> None:
        pass

    def insert_id(self) -> Any:
        return self._read("insert_id")

    def thread_id(self) -> Any:
        return self._read("thread_id")

    def character_set_name(self) -> Any:
        return self._read("character_set_name")

    def get_host_info(self) -> Any:
        return self._read("get_host_info")

    def get_proto_info(self) -> Any:
        return self._read("get_proto_info")

    def get_server_info(self) -> Any:
        return self._read("get_server_info")

    Warning = err.Warning
    Error = err.Error
    InterfaceError = err.InterfaceError
    DatabaseError = err.DatabaseError
    DataError = err.DataError
    OperationalError = err.OperationalError
    IntegrityError = err.IntegrityError
    InternalError = err.InternalError
    ProgrammingError = err.ProgrammingError
    NotSupportedError = err.NotSupportedError


class _RecordingConnection:
    def __init__(
        self,
        database_mock: DatabaseMock,
        connection: Any,
        cursorclass: Any,
    ):
        self._cursorclass = cursorclass
        self._database_mock = database_mock
        self._connection = connection

    def _record(self, key: str, f: Any, *args: Any, **kwargs: Any) -> Any:
        res = f(*args, **kwargs)
        self._database_mock._record_value(f"connection--{key}", res)
        return res

    @property
    def _result(self) -> Any:
        return self._connection._result

    def __enter__(self) -> Any:
        return self._connection

    def __exit__(self, *exc_info: Any) -> None:
        del exc_info
        self.close()

    def _create_ssl_ctx(self, sslp: Any) -> None:
        return self._connection._create_ssl_ctx(sslp)  # type: ignore

    def close(self) -> None:
        self._connection.close()

    @property
    def open(self) -> Any:
        return self._record("open", lambda: self._connection.open)

    def _force_close(self) -> None:
        self._connection._force_close()

    __del__ = _force_close

    def autocommit(self, value: Any) -> None:
        self._connection.autocommit(value)

    def get_autocommit(self) -> Any:
        return self._record("get_autocommit", self._connection.get_autocommit)

    def _read_ok_packet(self) -> None:
        self._connection._read_ok_packet()

    def _send_autocommit_mode(self) -> None:
        self._connection._send_autocommit_mode()

    def begin(self) -> None:
        self._connection.begin()

    def commit(self) -> None:
        self._connection.commit()

    def rollback(self) -> None:
        self._connection.rollback()

    def show_warnings(self) -> Any:
        return self._record("show_warnings", self._connection.show_warnings)

    def select_db(self, db: Any) -> None:
        self._connection.select_db(db)

    def escape(self, obj: Any, mapping: Any = None) -> Any:
        return self._record("escape", self._connection.escape, obj, mapping)

    def literal(self, obj: Any) -> Any:
        return self._record("literal", self._connection.literal, obj)

    def escape_string(self, s: Any) -> Any:
        return self._record("escape_string", self._connection.escape_string, s)

    def _quote_bytes(self, s: Any) -> Any:
        return self._connection._quote_bytes(s)

    def cursor(self, cursor: Any = None) -> Any:
        return self._cursorclass(self)

    def query(self, sql: Any, unbuffered: bool = False) -> Any:
        return self._connection.query(sql, unbuffered)

    def next_result(self, unbuffered: bool = False) -> Any:
        return self._connection.next_result(unbuffered)

    def affected_rows(self) -> Any:
        return self._connection.affected_rows()

    def kill(self, thread_id: Any) -> Any:
        return self._record("kill", self._connection.kill, thread_id)

    def ping(self, reconnect: bool = True) -> None:
        self._connection.ping(reconnect)

    def set_charset(self, charset: Any) -> None:
        self._connection.set_charset(charset)

    def connect(self, sock: Any = None) -> None:
        self._connection.connect(sock)

    def write_packet(self, payload: Any) -> None:
        self._connection.write_packet(payload)

    def _read_packet(self, packet_type: Any = MysqlPacket) -> Any:
        return self._connection._read_packet(packet_type)

    def _read_bytes(self, num_bytes: Any) -> Any:
        return self._connection._read_bytes(num_bytes)

    def _write_bytes(self, data: Any) -> None:
        self._connection._write_bytes(data)

    def _read_query_result(self, unbuffered: bool = False) -> Any:
        return self._connection._read_query_result(unbuffered)

    def insert_id(self) -> Any:
        return self._record("insert_id", self._connection.insert_id)

    def _execute_command(self, command: Any, sql: Any) -> None:
        self._connection._execute_command(command, sql)

    def _request_authentication(self) -> None:
        self._connection._request_authentication()

    def _process_auth(self, plugin_name: Any, auth_packet: Any) -> Any:
        return self._connection._process_auth(plugin_name, auth_packet)

    def _get_auth_plugin_handler(self, plugin_name: Any) -> Any:
        return self._connection._get_auth_plugin_handler(plugin_name)

    def thread_id(self) -> Any:
        return self._record("thread_id", self._connection.thread_id)

    def character_set_name(self) -> Any:
        return self._record("character_set_name", self._connection.character_set_name)

    def get_host_info(self) -> Any:
        return self._record("get_host_info", self._connection.host_info)

    def get_proto_info(self) -> Any:
        return self._record("get_proto_info", self._connection.get_proto_info)

    def _get_server_information(self) -> None:
        self._connection._get_server_information()

    def get_server_info(self) -> Any:
        return self._record("get_server_info", self._connection.get_server_info)

    Warning = err.Warning
    Error = err.Error
    InterfaceError = err.InterfaceError
    DatabaseError = err.DatabaseError
    DataError = err.DataError
    OperationalError = err.OperationalError
    IntegrityError = err.IntegrityError
    InternalError = err.InternalError
    ProgrammingError = err.ProgrammingError
    NotSupportedError = err.NotSupportedError


def _recording_mock_cursorclass(database_mock: DatabaseMock, cursorclass: Any) -> Any:
    def f(*args: Any, **kwargs: Any) -> Any:
        return _RecordingCursor(database_mock, cursorclass, *args, **kwargs)

    return f


def mock_connect(database_mock: DatabaseMock, real_connect: Any) -> Any:
    """
    Return a mock connect function.

    Depending on the mode, this function saves the database data to ``data`, uses the
    data from `data` instead of connecting to the database or just acts like PyMySQL's
    connect function (which must be passed as `real_connect`).

    Parameters
    ----------
    database_mock: `~pytest_pymysql_autorecord.util.DatabaseMockFixture`
        Database mock fixture.
    real_connect: function
        PyMySQL's connect function.

    Returns
    -------
    function
        A mock connect function.
    """

    def f(*args: Any, **kwargs: Any) -> Any:
        mode = database_mock.mode
        if mode == Mode.NORMAL:
            return real_connect(*args, **kwargs)
        elif mode == Mode.STORE_DATA:
            if "cursorclass" in kwargs:
                kwargs["cursorclass"] = _recording_mock_cursorclass(
                    database_mock, kwargs["cursorclass"]
                )
            else:
                kwargs["cursorclass"] = _recording_mock_cursorclass(
                    database_mock, pymysql.cursors.Cursor
                )
            c = real_connect(*args, **kwargs)
            return _RecordingConnection(
                database_mock=database_mock,
                connection=c,
                cursorclass=kwargs["cursorclass"],
            )
        elif mode == Mode.MOCK:
            return _MockConnection(database_mock=database_mock)

    return f
