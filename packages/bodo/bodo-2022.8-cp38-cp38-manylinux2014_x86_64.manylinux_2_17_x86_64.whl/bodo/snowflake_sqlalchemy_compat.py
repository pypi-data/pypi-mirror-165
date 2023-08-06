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
    ytth__qfkw = {}
    ibxd__cpow, yup__bsrh = self._current_database_schema(connection, **kw)
    corw__gvqj = self._denormalize_quote_join(ibxd__cpow, schema)
    try:
        psesv__bcnow = self._get_schema_primary_keys(connection, corw__gvqj,
            **kw)
        bojm__nxx = connection.execute(text(
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
    except sa_exc.ProgrammingError as pdntc__vmofu:
        if pdntc__vmofu.orig.errno == 90030:
            return None
        raise
    for table_name, nluoz__ruu, seg__mig, uauo__ztrpk, tqxma__dux, iqi__cjh, aqr__vuck, sap__eejxn, fltbf__fra, this__icpmw in bojm__nxx:
        table_name = self.normalize_name(table_name)
        nluoz__ruu = self.normalize_name(nluoz__ruu)
        if table_name not in ytth__qfkw:
            ytth__qfkw[table_name] = list()
        if nluoz__ruu.startswith('sys_clustering_column'):
            continue
        votvd__awmwc = self.ischema_names.get(seg__mig, None)
        keoyt__tpu = {}
        if votvd__awmwc is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(seg__mig, nluoz__ruu))
            votvd__awmwc = sqltypes.NULLTYPE
        elif issubclass(votvd__awmwc, sqltypes.FLOAT):
            keoyt__tpu['precision'] = tqxma__dux
            keoyt__tpu['decimal_return_scale'] = iqi__cjh
        elif issubclass(votvd__awmwc, sqltypes.Numeric):
            keoyt__tpu['precision'] = tqxma__dux
            keoyt__tpu['scale'] = iqi__cjh
        elif issubclass(votvd__awmwc, (sqltypes.String, sqltypes.BINARY)):
            keoyt__tpu['length'] = uauo__ztrpk
        zberu__fgn = votvd__awmwc if isinstance(votvd__awmwc, sqltypes.NullType
            ) else votvd__awmwc(**keoyt__tpu)
        cryev__mbte = psesv__bcnow.get(table_name)
        ytth__qfkw[table_name].append({'name': nluoz__ruu, 'type':
            zberu__fgn, 'nullable': aqr__vuck == 'YES', 'default':
            sap__eejxn, 'autoincrement': fltbf__fra == 'YES', 'comment':
            this__icpmw, 'primary_key': nluoz__ruu in psesv__bcnow[
            table_name]['constrained_columns'] if cryev__mbte else False})
    return ytth__qfkw


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
    ytth__qfkw = []
    ibxd__cpow, yup__bsrh = self._current_database_schema(connection, **kw)
    corw__gvqj = self._denormalize_quote_join(ibxd__cpow, schema)
    psesv__bcnow = self._get_schema_primary_keys(connection, corw__gvqj, **kw)
    bojm__nxx = connection.execute(text(
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
    for table_name, nluoz__ruu, seg__mig, uauo__ztrpk, tqxma__dux, iqi__cjh, aqr__vuck, sap__eejxn, fltbf__fra, this__icpmw in bojm__nxx:
        table_name = self.normalize_name(table_name)
        nluoz__ruu = self.normalize_name(nluoz__ruu)
        if nluoz__ruu.startswith('sys_clustering_column'):
            continue
        votvd__awmwc = self.ischema_names.get(seg__mig, None)
        keoyt__tpu = {}
        if votvd__awmwc is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(seg__mig, nluoz__ruu))
            votvd__awmwc = sqltypes.NULLTYPE
        elif issubclass(votvd__awmwc, sqltypes.FLOAT):
            keoyt__tpu['precision'] = tqxma__dux
            keoyt__tpu['decimal_return_scale'] = iqi__cjh
        elif issubclass(votvd__awmwc, sqltypes.Numeric):
            keoyt__tpu['precision'] = tqxma__dux
            keoyt__tpu['scale'] = iqi__cjh
        elif issubclass(votvd__awmwc, (sqltypes.String, sqltypes.BINARY)):
            keoyt__tpu['length'] = uauo__ztrpk
        zberu__fgn = votvd__awmwc if isinstance(votvd__awmwc, sqltypes.NullType
            ) else votvd__awmwc(**keoyt__tpu)
        cryev__mbte = psesv__bcnow.get(table_name)
        ytth__qfkw.append({'name': nluoz__ruu, 'type': zberu__fgn,
            'nullable': aqr__vuck == 'YES', 'default': sap__eejxn,
            'autoincrement': fltbf__fra == 'YES', 'comment': this__icpmw if
            this__icpmw != '' else None, 'primary_key': nluoz__ruu in
            psesv__bcnow[table_name]['constrained_columns'] if cryev__mbte else
            False})
    return ytth__qfkw


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
