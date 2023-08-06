import hashlib
import inspect
import warnings
import snowflake.sqlalchemy
import sqlalchemy.types as sqltypes
from sqlalchemy import exc as sa_exc
from sqlalchemy import util as sa_util
from sqlalchemy.sql import text
_check_snowflake_sqlalchemy_change = True


def _get_schema_columns(self, connection, schema, **kw):
    any__ravq = {}
    qzhqd__txd, qme__qjhve = self._current_database_schema(connection, **kw)
    wlq__iex = self._denormalize_quote_join(qzhqd__txd, schema)
    try:
        lgn__xde = self._get_schema_primary_keys(connection, wlq__iex, **kw)
        kstah__mtrhn = connection.execute(text(
            """
        SELECT /* sqlalchemy:_get_schema_columns */
                ic.table_name,
                ic.column_name,
                ic.data_type,
                ic.character_maximum_length,
                ic.numeric_precision,
                ic.numeric_scale,
                ic.is_nullable,
                ic.column_default,
                ic.is_identity,
                ic.comment
            FROM information_schema.columns ic
            WHERE ic.table_schema=:table_schema
            ORDER BY ic.ordinal_position"""
            ), {'table_schema': self.denormalize_name(schema)})
    except sa_exc.ProgrammingError as xjkq__cdyei:
        if xjkq__cdyei.orig.errno == 90030:
            return None
        raise
    for table_name, quohq__vgwk, etp__ljjab, kysbv__wjxve, livkp__ytnlo, yda__pkl, gmqq__tzdwl, dghtf__idjpx, erplw__blhou, ecny__vgxjt in kstah__mtrhn:
        table_name = self.normalize_name(table_name)
        quohq__vgwk = self.normalize_name(quohq__vgwk)
        if table_name not in any__ravq:
            any__ravq[table_name] = list()
        if quohq__vgwk.startswith('sys_clustering_column'):
            continue
        qms__mtx = self.ischema_names.get(etp__ljjab, None)
        kpoq__knxy = {}
        if qms__mtx is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(etp__ljjab, quohq__vgwk))
            qms__mtx = sqltypes.NULLTYPE
        elif issubclass(qms__mtx, sqltypes.FLOAT):
            kpoq__knxy['precision'] = livkp__ytnlo
            kpoq__knxy['decimal_return_scale'] = yda__pkl
        elif issubclass(qms__mtx, sqltypes.Numeric):
            kpoq__knxy['precision'] = livkp__ytnlo
            kpoq__knxy['scale'] = yda__pkl
        elif issubclass(qms__mtx, (sqltypes.String, sqltypes.BINARY)):
            kpoq__knxy['length'] = kysbv__wjxve
        efisc__idgsw = qms__mtx if isinstance(qms__mtx, sqltypes.NullType
            ) else qms__mtx(**kpoq__knxy)
        paqxk__mdway = lgn__xde.get(table_name)
        any__ravq[table_name].append({'name': quohq__vgwk, 'type':
            efisc__idgsw, 'nullable': gmqq__tzdwl == 'YES', 'default':
            dghtf__idjpx, 'autoincrement': erplw__blhou == 'YES', 'comment':
            ecny__vgxjt, 'primary_key': quohq__vgwk in lgn__xde[table_name]
            ['constrained_columns'] if paqxk__mdway else False})
    return any__ravq


if _check_snowflake_sqlalchemy_change:
    lines = inspect.getsource(snowflake.sqlalchemy.snowdialect.
        SnowflakeDialect._get_schema_columns)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'fdf39af1ac165319d3b6074e8cf9296a090a21f0e2c05b644ff8ec0e56e2d769':
        warnings.warn(
            'snowflake.sqlalchemy.snowdialect.SnowflakeDialect._get_schema_columns has changed'
            )
snowflake.sqlalchemy.snowdialect.SnowflakeDialect._get_schema_columns = (
    _get_schema_columns)


def _get_table_columns(self, connection, table_name, schema=None, **kw):
    any__ravq = []
    qzhqd__txd, qme__qjhve = self._current_database_schema(connection, **kw)
    wlq__iex = self._denormalize_quote_join(qzhqd__txd, schema)
    lgn__xde = self._get_schema_primary_keys(connection, wlq__iex, **kw)
    kstah__mtrhn = connection.execute(text(
        """
    SELECT /* sqlalchemy:get_table_columns */
            ic.table_name,
            ic.column_name,
            ic.data_type,
            ic.character_maximum_length,
            ic.numeric_precision,
            ic.numeric_scale,
            ic.is_nullable,
            ic.column_default,
            ic.is_identity,
            ic.comment
        FROM information_schema.columns ic
        WHERE ic.table_schema=:table_schema
        AND ic.table_name=:table_name
        ORDER BY ic.ordinal_position"""
        ), {'table_schema': self.denormalize_name(schema), 'table_name':
        self.denormalize_name(table_name)})
    for table_name, quohq__vgwk, etp__ljjab, kysbv__wjxve, livkp__ytnlo, yda__pkl, gmqq__tzdwl, dghtf__idjpx, erplw__blhou, ecny__vgxjt in kstah__mtrhn:
        table_name = self.normalize_name(table_name)
        quohq__vgwk = self.normalize_name(quohq__vgwk)
        if quohq__vgwk.startswith('sys_clustering_column'):
            continue
        qms__mtx = self.ischema_names.get(etp__ljjab, None)
        kpoq__knxy = {}
        if qms__mtx is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(etp__ljjab, quohq__vgwk))
            qms__mtx = sqltypes.NULLTYPE
        elif issubclass(qms__mtx, sqltypes.FLOAT):
            kpoq__knxy['precision'] = livkp__ytnlo
            kpoq__knxy['decimal_return_scale'] = yda__pkl
        elif issubclass(qms__mtx, sqltypes.Numeric):
            kpoq__knxy['precision'] = livkp__ytnlo
            kpoq__knxy['scale'] = yda__pkl
        elif issubclass(qms__mtx, (sqltypes.String, sqltypes.BINARY)):
            kpoq__knxy['length'] = kysbv__wjxve
        efisc__idgsw = qms__mtx if isinstance(qms__mtx, sqltypes.NullType
            ) else qms__mtx(**kpoq__knxy)
        paqxk__mdway = lgn__xde.get(table_name)
        any__ravq.append({'name': quohq__vgwk, 'type': efisc__idgsw,
            'nullable': gmqq__tzdwl == 'YES', 'default': dghtf__idjpx,
            'autoincrement': erplw__blhou == 'YES', 'comment': ecny__vgxjt if
            ecny__vgxjt != '' else None, 'primary_key': quohq__vgwk in
            lgn__xde[table_name]['constrained_columns'] if paqxk__mdway else
            False})
    return any__ravq


if _check_snowflake_sqlalchemy_change:
    lines = inspect.getsource(snowflake.sqlalchemy.snowdialect.
        SnowflakeDialect._get_table_columns)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '9ecc8a2425c655836ade4008b1b98a8fd1819f3be43ba77b0fbbfc1f8740e2be':
        warnings.warn(
            'snowflake.sqlalchemy.snowdialect.SnowflakeDialect._get_table_columns has changed'
            )
snowflake.sqlalchemy.snowdialect.SnowflakeDialect._get_table_columns = (
    _get_table_columns)
