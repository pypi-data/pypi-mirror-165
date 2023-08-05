from dataclasses import asdict
from typing import Optional, Any, List, Callable, TypeVar

from psycopg2 import connect, DatabaseError
from zpy.utils.funcs import safely_exec

from zdb.commons import show_info, DBTypes, get_map_type, ZDatabase, ZDBConfig, build_params, process_exception

T = TypeVar("T")


def __fn_extract_data(result_set, rows, column_names, ret_type: DBTypes, model, jsonfy=False) -> Any:
    """
        Inner Data Builder
    """
    if ret_type == DBTypes.cursor:
        if model is not None:
            return [model(**dict(zip(column_names, r))) for r in rows]
        if jsonfy is True:
            return [dict(zip(column_names, r)) for r in rows]
        return rows
    else:
        if len(rows) > 0:
            parser = get_map_type(ret_type)
            if model is not None:
                return model(**dict(zip(column_names, rows[0])))
            if jsonfy is True:
                return dict(zip(column_names, rows[0]))
            return parser(rows[0][0])
    return result_set


def extract_data(result_set, ret_type: DBTypes, cursor, model, jsonfy=False) -> Any:
    """
        Data Builder for custom stored procedures
    """
    # for result in cursor.stored_results():
    #     colum_names = result.column_names
    colum_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    if not ret_type:
        return rows
    return __fn_extract_data(result_set, rows, colum_names, ret_type, model, jsonfy)


def fn_extract_data(result_set, ret_type: DBTypes, cursor, model, jsonfy=False) -> Any:
    """
        Data Builder for custom functions
    """
    colum_names = cursor.column_names
    rows = cursor.fetchall()
    if not ret_type:
        return rows
    return __fn_extract_data(result_set, rows, colum_names, ret_type, model, jsonfy)


class ZPostgres(ZDatabase):

    def __init__(self, dict_config: Optional[dict] = None, config: Optional[ZDBConfig] = None,
                 verbose: bool = False):
        self.dict_config = dict_config
        self.config = config
        self.verbose = verbose

    @classmethod
    def setup(cls, config: dict, verbose: bool = False):
        return cls(config, config=None, verbose=verbose)

    @classmethod
    def setup_of(cls, config: ZDBConfig, verbose: bool = False):
        return cls(config=config, verbose=verbose)

    @classmethod
    def from_dict(cls, config: dict, verbose: bool = False, **kwargs):
        """
            dict should be contain the next keys:
            dbname=
            user=
            password=
            host=
            port=
        """
        config.update(kwargs)
        return cls(config, verbose=verbose)

    @classmethod
    def from_of(cls, user: str, password: str, host: str, db_name: str, verbose: bool = False):
        return cls({
            'user': user,
            'password': password,
            'host': host,
            'database': db_name,
            'raise_on_warnings': False
        }, verbose=verbose)

    def new_connect(self) -> Any:
        final_config = self.__validate_config()
        if final_config is None:
            raise ValueError("The value of db configuration can not be null.")
        return connect(**final_config)

    def call(self, name: str, ret_type: Optional[DBTypes] = None, params: Optional[dict] = None,
             list_params: Optional[List[Any]] = None,
             model: Optional[Any] = None,
             connection=None, jsonfy: bool = False, throw: bool = True) -> Any:
        """Stored procedure caller

        Args:
            name (str): Stored procedure name
            ret_type (DBTypes): Type of data returned from stored procedure
            params (dict, optional): params for the procedure. Defaults to None.
            list_params (List[Any], optional): positional list params to the procedure. Defaults to None.
            model (Any, optional): model for build returned data. Defaults to None.
            connection ([type], optional): connection database. Defaults to None.
            jsonfy (bool, optional): return data in dict format if model is null. Defaults to False.
            throw (bool, optional): raise exceptions

        Returns:
            Any: processed data
        """
        return self.__call(lambda c, fn, p: c.callproc(fn, p), extract_data, name, ret_type, params, list_params, model,
                           connection, jsonfy, throw)

    def __call(self, runner: Callable, extractor: Callable, name: str, ret_type: DBTypes, params: dict = None,
               list_params: List[Any] = None,
               model: Any = None,
               connection=None, jsonfy: bool = False, throw: bool = True) -> Any:
        cn = connection
        connection_passed = True
        if connection is None:
            connection_passed = False
            cn = self.new_connect()

        cursor = None
        if cn is not None:
            cursor = cn.cursor()

        if cn is None or cursor is None:
            raise Exception("Can't get db connection")
        if self.verbose:
            show_info(name, params, ret_type, model)
        try:
            result_set = runner(cursor, name, build_params(dict_params=params, list_params=list_params))
            return extractor(result_set, ret_type, cursor, model, jsonfy)
        except DatabaseError as error:
            process_exception(throw, error)
        except Exception as e:
            process_exception(throw, e)
        finally:
            if not connection_passed:
                safely_exec(lambda c: c.close(), args=[cursor])
                if cn.closed == 0:
                    safely_exec(lambda c: c.commit(), args=[cn])
                    safely_exec(lambda c: c.close(), args=[cn])
        return None

    def exec(self, fn_name: str, ret_type: DBTypes = None, params: dict = None, list_params: List[Any] = None,
             model: Any = None,
             connection=None, jsonfy: bool = False, throw: bool = True) -> Any:
        """Function executor

        Args:
            fn_name (str): Stored procedure name
            ret_type (DBTypes): Type of data returned from stored procedure
            params (dict, optional): params for the procedure. Defaults to None.
            list_params (List[Any], optional): positional list params to the procedure. Defaults to None.
            model (Any, optional): model for build returned data. Defaults to None.
            connection ([type], optional): connection database. Defaults to None.
            jsonfy (bool, optional): return data in dict format if model is null. Defaults to False.
            throw: (bool, optional): raise exceptions

        Returns:
            Any: processed data
        """
        return self.__call(lambda c, fn, p: c.execute(f'SELECT {fn}', p), fn_extract_data, fn_name, ret_type, params,
                           list_params, model,
                           connection, jsonfy, throw)

    def __validate_config(self) -> dict:
        if self.config is not None:
            return asdict(self.config)
        return self.dict_config

    def init_local_client(self, path: str):
        raise NotImplementedError("Not implemented for MySQL!")

    def connect(self):
        raise NotImplementedError("Not implemented for MySQL!")

    def close(self) -> None:
        raise NotImplementedError("Not implemented for MySQL!")

    def is_connected(self) -> bool:
        raise NotImplementedError("Not implemented for MySQL!")

    def get_connection(self) -> Any:
        raise NotImplementedError("Not implemented for MySQL!")
