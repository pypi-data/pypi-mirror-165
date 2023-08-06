"""
Implementation of pd.read_sql in BODO.
We piggyback on the pandas implementation. Future plan is to have a faster
version for this task.
"""
from typing import List, Optional
from urllib.parse import urlparse
import numba
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, next_label, replace_arg_nodes
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.hiframes.table import Table, TableType
from bodo.io.helpers import PyArrowTableSchemaType, is_nullable
from bodo.io.parquet_pio import ParquetPredicateType
from bodo.libs.array import cpp_table_to_py_table, delete_table, info_from_table, info_to_array, table_type
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.distributed_api import bcast, bcast_scalar
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.table_column_del_pass import ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import BodoError
from bodo.utils.utils import check_and_propagate_cpp_exception
MPI_ROOT = 0


class SqlReader(ir.Stmt):

    def __init__(self, sql_request, connection, df_out, df_colnames,
        out_vars, out_types, converted_colnames, db_type, loc,
        unsupported_columns, unsupported_arrow_types, is_select_query,
        index_column_name, index_column_type, database_schema,
        pyarrow_table_schema=None):
        self.connector_typ = 'sql'
        self.sql_request = sql_request
        self.connection = connection
        self.df_out = df_out
        self.df_colnames = df_colnames
        self.out_vars = out_vars
        self.out_types = out_types
        self.converted_colnames = converted_colnames
        self.loc = loc
        self.limit = req_limit(sql_request)
        self.db_type = db_type
        self.filters = None
        self.unsupported_columns = unsupported_columns
        self.unsupported_arrow_types = unsupported_arrow_types
        self.is_select_query = is_select_query
        self.index_column_name = index_column_name
        self.index_column_type = index_column_type
        self.out_used_cols = list(range(len(df_colnames)))
        self.database_schema = database_schema
        self.pyarrow_table_schema = pyarrow_table_schema

    def __repr__(self):
        cqfzj__xdkb = tuple(kkf__wczoo.name for kkf__wczoo in self.out_vars)
        return (
            f'{cqfzj__xdkb} = ReadSql(sql_request={self.sql_request}, connection={self.connection}, col_names={self.df_colnames}, types={self.out_types}, df_out={self.df_out}, limit={self.limit}, unsupported_columns={self.unsupported_columns}, unsupported_arrow_types={self.unsupported_arrow_types}, is_select_query={self.is_select_query}, index_column_name={self.index_column_name}, index_column_type={self.index_column_type}, out_used_cols={self.out_used_cols}, database_schema={self.database_schema}, pyarrow_table_schema={self.pyarrow_table_schema})'
            )


def parse_dbtype(con_str):
    hlqzq__munwp = urlparse(con_str)
    db_type = hlqzq__munwp.scheme
    fvsrr__cklr = hlqzq__munwp.password
    if con_str.startswith('oracle+cx_oracle://'):
        return 'oracle', fvsrr__cklr
    if db_type == 'mysql+pymysql':
        return 'mysql', fvsrr__cklr
    if con_str == 'iceberg+glue' or hlqzq__munwp.scheme in ('iceberg',
        'iceberg+file', 'iceberg+s3', 'iceberg+thrift', 'iceberg+http',
        'iceberg+https'):
        return 'iceberg', fvsrr__cklr
    return db_type, fvsrr__cklr


def remove_iceberg_prefix(con):
    import sys
    if sys.version_info.minor < 9:
        if con.startswith('iceberg+'):
            con = con[len('iceberg+'):]
        if con.startswith('iceberg://'):
            con = con[len('iceberg://'):]
    else:
        con = con.removeprefix('iceberg+').removeprefix('iceberg://')
    return con


def remove_dead_sql(sql_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    fmg__kbzz = sql_node.out_vars[0].name
    aue__fonz = sql_node.out_vars[1].name
    if fmg__kbzz not in lives and aue__fonz not in lives:
        return None
    elif fmg__kbzz not in lives:
        sql_node.out_types = []
        sql_node.df_colnames = []
        sql_node.out_used_cols = []
    elif aue__fonz not in lives:
        sql_node.index_column_name = None
        sql_node.index_arr_typ = types.none
    return sql_node


def sql_distributed_run(sql_node, array_dists, typemap, calltypes,
    typingctx, targetctx, meta_head_only_info=None):
    if bodo.user_logging.get_verbose_level() >= 1:
        aub__tlzx = (
            'Finish column pruning on read_sql node:\n%s\nColumns loaded %s\n')
        chx__ouh = []
        agnap__mtp = []
        for tsljg__hsya in sql_node.out_used_cols:
            jfkt__nrwz = sql_node.df_colnames[tsljg__hsya]
            chx__ouh.append(jfkt__nrwz)
            if isinstance(sql_node.out_types[tsljg__hsya], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                agnap__mtp.append(jfkt__nrwz)
        if sql_node.index_column_name:
            chx__ouh.append(sql_node.index_column_name)
            if isinstance(sql_node.index_column_type, bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                agnap__mtp.append(sql_node.index_column_name)
        uviq__dtz = sql_node.loc.strformat()
        bodo.user_logging.log_message('Column Pruning', aub__tlzx,
            uviq__dtz, chx__ouh)
        if agnap__mtp:
            ptxn__dumla = """Finished optimized encoding on read_sql node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                ptxn__dumla, uviq__dtz, agnap__mtp)
    parallel = bodo.ir.connector.is_connector_table_parallel(sql_node,
        array_dists, typemap, 'SQLReader')
    if sql_node.unsupported_columns:
        oyums__rrcu = set(sql_node.unsupported_columns)
        asa__uwwt = set(sql_node.out_used_cols)
        qsw__vjq = asa__uwwt & oyums__rrcu
        if qsw__vjq:
            jsqvz__dmr = sorted(qsw__vjq)
            piio__nbdu = [
                f'pandas.read_sql(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                'Please manually remove these columns from your sql query by specifying the columns you need in your SELECT statement. If these '
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            uhwau__lnup = 0
            for mruud__cuu in jsqvz__dmr:
                while sql_node.unsupported_columns[uhwau__lnup] != mruud__cuu:
                    uhwau__lnup += 1
                piio__nbdu.append(
                    f"Column '{sql_node.original_df_colnames[mruud__cuu]}' with unsupported arrow type {sql_node.unsupported_arrow_types[uhwau__lnup]}"
                    )
                uhwau__lnup += 1
            ico__kuqpc = '\n'.join(piio__nbdu)
            raise BodoError(ico__kuqpc, loc=sql_node.loc)
    nchb__imda, icb__ovcf = bodo.ir.connector.generate_filter_map(sql_node.
        filters)
    gzp__fyhyf = ', '.join(nchb__imda.values())
    ihrm__pax = (
        f'def sql_impl(sql_request, conn, database_schema, {gzp__fyhyf}):\n')
    if sql_node.filters and sql_node.db_type != 'iceberg':
        jht__icfj = []
        for varth__xjln in sql_node.filters:
            rcsro__famqe = []
            for inah__vsi in varth__xjln:
                ceqcr__wmkh = '{' + nchb__imda[inah__vsi[2].name
                    ] + '}' if isinstance(inah__vsi[2], ir.Var) else inah__vsi[
                    2]
                if inah__vsi[1] in ('startswith', 'endswith'):
                    rocqx__gzh = ['(', inah__vsi[1], '(', inah__vsi[0], ',',
                        ceqcr__wmkh, ')', ')']
                else:
                    rocqx__gzh = ['(', inah__vsi[0], inah__vsi[1],
                        ceqcr__wmkh, ')']
                rcsro__famqe.append(' '.join(rocqx__gzh))
            jht__icfj.append(' ( ' + ' AND '.join(rcsro__famqe) + ' ) ')
        ichi__asoh = ' WHERE ' + ' OR '.join(jht__icfj)
        for tsljg__hsya, iiqu__ykhx in enumerate(nchb__imda.values()):
            ihrm__pax += f'    {iiqu__ykhx} = get_sql_literal({iiqu__ykhx})\n'
        ihrm__pax += f'    sql_request = f"{{sql_request}} {ichi__asoh}"\n'
    jlod__qpne = ''
    if sql_node.db_type == 'iceberg':
        jlod__qpne = gzp__fyhyf
    ihrm__pax += f"""    (total_rows, table_var, index_var) = _sql_reader_py(sql_request, conn, database_schema, {jlod__qpne})
"""
    fntb__aqnu = {}
    exec(ihrm__pax, {}, fntb__aqnu)
    aqx__kpx = fntb__aqnu['sql_impl']
    if sql_node.limit is not None:
        limit = sql_node.limit
    elif meta_head_only_info and meta_head_only_info[0] is not None:
        limit = meta_head_only_info[0]
    else:
        limit = None
    fhq__mhqo = _gen_sql_reader_py(sql_node.df_colnames, sql_node.out_types,
        sql_node.index_column_name, sql_node.index_column_type, sql_node.
        out_used_cols, typingctx, targetctx, sql_node.db_type, limit,
        parallel, typemap, sql_node.filters, sql_node.pyarrow_table_schema)
    asf__mijm = types.none if sql_node.database_schema is None else string_type
    yhcsa__tpp = compile_to_numba_ir(aqx__kpx, {'_sql_reader_py': fhq__mhqo,
        'bcast_scalar': bcast_scalar, 'bcast': bcast, 'get_sql_literal':
        _get_snowflake_sql_literal}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=(string_type, string_type, asf__mijm) + tuple(
        typemap[kkf__wczoo.name] for kkf__wczoo in icb__ovcf), typemap=
        typemap, calltypes=calltypes).blocks.popitem()[1]
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        ysuav__pksj = [sql_node.df_colnames[tsljg__hsya] for tsljg__hsya in
            sql_node.out_used_cols]
        if sql_node.index_column_name:
            ysuav__pksj.append(sql_node.index_column_name)
        vhs__bht = escape_column_names(ysuav__pksj, sql_node.db_type,
            sql_node.converted_colnames)
        if sql_node.db_type == 'oracle':
            tvx__kdpva = ('SELECT ' + vhs__bht + ' FROM (' + sql_node.
                sql_request + ') TEMP')
        else:
            tvx__kdpva = ('SELECT ' + vhs__bht + ' FROM (' + sql_node.
                sql_request + ') as TEMP')
    else:
        tvx__kdpva = sql_node.sql_request
    replace_arg_nodes(yhcsa__tpp, [ir.Const(tvx__kdpva, sql_node.loc), ir.
        Const(sql_node.connection, sql_node.loc), ir.Const(sql_node.
        database_schema, sql_node.loc)] + icb__ovcf)
    qnp__feon = yhcsa__tpp.body[:-3]
    if meta_head_only_info:
        qnp__feon[-3].target = meta_head_only_info[1]
    qnp__feon[-2].target = sql_node.out_vars[0]
    qnp__feon[-1].target = sql_node.out_vars[1]
    assert not (sql_node.index_column_name is None and not sql_node.
        out_used_cols
        ), 'At most one of table and index should be dead if the SQL IR node is live'
    if sql_node.index_column_name is None:
        qnp__feon.pop(-1)
    elif not sql_node.out_used_cols:
        qnp__feon.pop(-2)
    return qnp__feon


def escape_column_names(col_names, db_type, converted_colnames):
    if db_type in ('snowflake', 'oracle'):
        ysuav__pksj = [(ncel__irthb.upper() if ncel__irthb in
            converted_colnames else ncel__irthb) for ncel__irthb in col_names]
        vhs__bht = ', '.join([f'"{ncel__irthb}"' for ncel__irthb in
            ysuav__pksj])
    elif db_type == 'mysql':
        vhs__bht = ', '.join([f'`{ncel__irthb}`' for ncel__irthb in col_names])
    else:
        vhs__bht = ', '.join([f'"{ncel__irthb}"' for ncel__irthb in col_names])
    return vhs__bht


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal_scalar(filter_value):
    setc__kemc = types.unliteral(filter_value)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(setc__kemc,
        'Filter pushdown')
    if setc__kemc == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(setc__kemc, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif setc__kemc == bodo.pd_timestamp_type:

        def impl(filter_value):
            dhue__hzaew = filter_value.nanosecond
            ikme__lbl = ''
            if dhue__hzaew < 10:
                ikme__lbl = '00'
            elif dhue__hzaew < 100:
                ikme__lbl = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{ikme__lbl}{dhue__hzaew}'"
                )
        return impl
    elif setc__kemc == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported scalar type {setc__kemc} used in filter pushdown.'
            )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    scalar_isinstance = types.Integer, types.Float
    mlme__kwi = (bodo.datetime_date_type, bodo.pd_timestamp_type, types.
        unicode_type, types.bool_)
    setc__kemc = types.unliteral(filter_value)
    if isinstance(setc__kemc, types.List) and (isinstance(setc__kemc.dtype,
        scalar_isinstance) or setc__kemc.dtype in mlme__kwi):

        def impl(filter_value):
            qufc__zxe = ', '.join([_get_snowflake_sql_literal_scalar(
                ncel__irthb) for ncel__irthb in filter_value])
            return f'({qufc__zxe})'
        return impl
    elif isinstance(setc__kemc, scalar_isinstance) or setc__kemc in mlme__kwi:
        return lambda filter_value: _get_snowflake_sql_literal_scalar(
            filter_value)
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {setc__kemc} used in filter pushdown.'
            )


def sql_remove_dead_column(sql_node, column_live_map, equiv_vars, typemap):
    return bodo.ir.connector.base_connector_remove_dead_columns(sql_node,
        column_live_map, equiv_vars, typemap, 'SQLReader', sql_node.df_colnames
        )


numba.parfors.array_analysis.array_analysis_extensions[SqlReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[SqlReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[SqlReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[SqlReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[SqlReader] = remove_dead_sql
numba.core.analysis.ir_extension_usedefs[SqlReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[SqlReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[SqlReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[SqlReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[SqlReader] = sql_distributed_run
remove_dead_column_extensions[SqlReader] = sql_remove_dead_column
ir_extension_table_column_use[SqlReader
    ] = bodo.ir.connector.connector_table_column_use
compiled_funcs = []


@numba.njit
def sqlalchemy_check():
    with numba.objmode():
        sqlalchemy_check_()


def sqlalchemy_check_():
    try:
        import sqlalchemy
    except ImportError as owb__cwp:
        hmsv__kkcil = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(hmsv__kkcil)


@numba.njit
def pymysql_check():
    with numba.objmode():
        pymysql_check_()


def pymysql_check_():
    try:
        import pymysql
    except ImportError as owb__cwp:
        hmsv__kkcil = (
            "Using MySQL URI string requires pymsql to be installed. It can be installed by calling 'conda install -c conda-forge pymysql' or 'pip install PyMySQL'."
            )
        raise BodoError(hmsv__kkcil)


@numba.njit
def cx_oracle_check():
    with numba.objmode():
        cx_oracle_check_()


def cx_oracle_check_():
    try:
        import cx_Oracle
    except ImportError as owb__cwp:
        hmsv__kkcil = (
            "Using Oracle URI string requires cx_oracle to be installed. It can be installed by calling 'conda install -c conda-forge cx_oracle' or 'pip install cx-Oracle'."
            )
        raise BodoError(hmsv__kkcil)


@numba.njit
def psycopg2_check():
    with numba.objmode():
        psycopg2_check_()


def psycopg2_check_():
    try:
        import psycopg2
    except ImportError as owb__cwp:
        hmsv__kkcil = (
            "Using PostgreSQL URI string requires psycopg2 to be installed. It can be installed by calling 'conda install -c conda-forge psycopg2' or 'pip install psycopg2'."
            )
        raise BodoError(hmsv__kkcil)


def req_limit(sql_request):
    import re
    frp__squx = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    cmjz__aqd = frp__squx.search(sql_request)
    if cmjz__aqd:
        return int(cmjz__aqd.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names: List[str], col_typs, index_column_name:
    str, index_column_type, out_used_cols: List[int], typingctx, targetctx,
    db_type: str, limit: Optional[int], parallel, typemap, filters,
    pyarrow_table_schema: 'Optional[pyarrow.Schema]'):
    jpanj__wpqos = next_label()
    ysuav__pksj = [col_names[tsljg__hsya] for tsljg__hsya in out_used_cols]
    phg__mspj = [col_typs[tsljg__hsya] for tsljg__hsya in out_used_cols]
    if index_column_name:
        ysuav__pksj.append(index_column_name)
        phg__mspj.append(index_column_type)
    upm__sng = None
    fxbs__uyq = None
    avia__cjyvw = TableType(tuple(col_typs)) if out_used_cols else types.none
    jlod__qpne = ''
    nchb__imda = {}
    icb__ovcf = []
    if filters and db_type == 'iceberg':
        nchb__imda, icb__ovcf = bodo.ir.connector.generate_filter_map(filters)
        jlod__qpne = ', '.join(nchb__imda.values())
    ihrm__pax = (
        f'def sql_reader_py(sql_request, conn, database_schema, {jlod__qpne}):\n'
        )
    if db_type == 'iceberg':
        assert pyarrow_table_schema is not None, 'SQLNode must contain a pyarrow_table_schema if reading from an Iceberg database'
        bea__qpr, zhyqm__duzm = bodo.ir.connector.generate_arrow_filters(
            filters, nchb__imda, icb__ovcf, col_names, col_names, col_typs,
            typemap, 'iceberg')
        tiesv__sfusy: List[int] = [pyarrow_table_schema.get_field_index(
            col_names[tsljg__hsya]) for tsljg__hsya in out_used_cols]
        oyc__peoj = {ygi__otjko: tsljg__hsya for tsljg__hsya, ygi__otjko in
            enumerate(tiesv__sfusy)}
        fde__qhxn = [int(is_nullable(col_typs[tsljg__hsya])) for
            tsljg__hsya in tiesv__sfusy]
        jwmd__yvfg = ',' if jlod__qpne else ''
        ihrm__pax += f"""  ev = bodo.utils.tracing.Event('read_iceberg', {parallel})
  dnf_filters, expr_filters = get_filters_pyobject("{bea__qpr}", "{zhyqm__duzm}", ({jlod__qpne}{jwmd__yvfg}))
  total_rows_np = np.array([0], dtype=np.int64)
  out_table = iceberg_read(
    unicode_to_utf8(conn),
    unicode_to_utf8(database_schema),
    unicode_to_utf8(sql_request),
    {parallel},
    {-1 if limit is None else limit},
    dnf_filters,
    expr_filters,
    selected_cols_arr_{jpanj__wpqos}.ctypes,
    {len(tiesv__sfusy)},
    nullable_cols_arr_{jpanj__wpqos}.ctypes,
    pyarrow_table_schema_{jpanj__wpqos},
    total_rows_np.ctypes,
  )
  check_and_propagate_cpp_exception()
"""
        ihrm__pax += f'  total_rows = total_rows_np[0]\n'
        if parallel:
            ihrm__pax += f"""  local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
        else:
            ihrm__pax += f'  local_rows = total_rows\n'
        tzxg__lqpd = not out_used_cols
        avia__cjyvw = TableType(tuple(col_typs))
        if tzxg__lqpd:
            avia__cjyvw = types.none
        upm__sng = None
        if not tzxg__lqpd:
            upm__sng = []
            fltk__fumzc = 0
            for tsljg__hsya in range(len(col_names)):
                if fltk__fumzc < len(out_used_cols
                    ) and tsljg__hsya == out_used_cols[fltk__fumzc]:
                    upm__sng.append(oyc__peoj[tsljg__hsya])
                    fltk__fumzc += 1
                else:
                    upm__sng.append(-1)
            upm__sng = np.array(upm__sng, dtype=np.int64)
        if tzxg__lqpd:
            ihrm__pax += '  table_var = None\n'
        else:
            ihrm__pax += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{jpanj__wpqos}, py_table_type_{jpanj__wpqos})
"""
            if len(out_used_cols) == 0:
                ihrm__pax += (
                    f'  table_var = set_table_len(table_var, local_rows)\n')
        aue__fonz = 'None'
        if index_column_name is not None:
            mgp__gbmff = len(out_used_cols) + 1 if not tzxg__lqpd else 0
            aue__fonz = (
                f'info_to_array(info_from_table(out_table, {mgp__gbmff}), index_col_typ)'
                )
        ihrm__pax += f'  index_var = {aue__fonz}\n'
        ihrm__pax += f'  delete_table(out_table)\n'
        ihrm__pax += f'  ev.finalize()\n'
        ihrm__pax += '  return (total_rows, table_var, index_var)\n'
    elif db_type == 'snowflake':
        sazso__lspi = {ygi__otjko: tsljg__hsya for tsljg__hsya, ygi__otjko in
            enumerate(out_used_cols)}
        vjk__rcv = [sazso__lspi[tsljg__hsya] for tsljg__hsya in
            out_used_cols if col_typs[tsljg__hsya] == dict_str_arr_type]
        ihrm__pax += (
            f"  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})\n")
        fde__qhxn = [int(is_nullable(col_typs[tsljg__hsya])) for
            tsljg__hsya in out_used_cols]
        if index_column_name:
            fde__qhxn.append(int(is_nullable(index_column_type)))
        ihrm__pax += f"""  out_table = snowflake_read(unicode_to_utf8(sql_request), unicode_to_utf8(conn), {parallel}, {len(fde__qhxn)}, np.array({fde__qhxn}, dtype=np.int32).ctypes,
"""
        if len(vjk__rcv) > 0:
            ihrm__pax += (
                f'        np.array({vjk__rcv}, dtype=np.int32).ctypes, {len(vjk__rcv)})\n'
                )
        else:
            ihrm__pax += f'        0, 0)\n'
        ihrm__pax += '  check_and_propagate_cpp_exception()\n'
        if index_column_name:
            ihrm__pax += f"""  index_var = info_to_array(info_from_table(out_table, {len(out_used_cols)}), index_col_typ)
"""
        else:
            ihrm__pax += '  index_var = None\n'
        if out_used_cols:
            uhwau__lnup = []
            fltk__fumzc = 0
            for tsljg__hsya in range(len(col_names)):
                if fltk__fumzc < len(out_used_cols
                    ) and tsljg__hsya == out_used_cols[fltk__fumzc]:
                    uhwau__lnup.append(fltk__fumzc)
                    fltk__fumzc += 1
                else:
                    uhwau__lnup.append(-1)
            upm__sng = np.array(uhwau__lnup, dtype=np.int64)
            ihrm__pax += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{jpanj__wpqos}, py_table_type_{jpanj__wpqos})
"""
        else:
            ihrm__pax += '  table_var = None\n'
        ihrm__pax += '  delete_table(out_table)\n'
        ihrm__pax += f'  ev.finalize()\n'
        ihrm__pax += '  return (-1, table_var, index_var)\n'
    else:
        if out_used_cols:
            ihrm__pax += f"""  type_usecols_offsets_arr_{jpanj__wpqos}_2 = type_usecols_offsets_arr_{jpanj__wpqos}
"""
            fxbs__uyq = np.array(out_used_cols, dtype=np.int64)
        ihrm__pax += '  df_typeref_2 = df_typeref\n'
        ihrm__pax += '  sqlalchemy_check()\n'
        if db_type == 'mysql':
            ihrm__pax += '  pymysql_check()\n'
        elif db_type == 'oracle':
            ihrm__pax += '  cx_oracle_check()\n'
        elif db_type == 'postgresql' or db_type == 'postgresql+psycopg2':
            ihrm__pax += '  psycopg2_check()\n'
        if parallel:
            ihrm__pax += '  rank = bodo.libs.distributed_api.get_rank()\n'
            if limit is not None:
                ihrm__pax += f'  nb_row = {limit}\n'
            else:
                ihrm__pax += '  with objmode(nb_row="int64"):\n'
                ihrm__pax += f'     if rank == {MPI_ROOT}:\n'
                ihrm__pax += (
                    "         sql_cons = 'select count(*) from (' + sql_request + ') x'\n"
                    )
                ihrm__pax += '         frame = pd.read_sql(sql_cons, conn)\n'
                ihrm__pax += '         nb_row = frame.iat[0,0]\n'
                ihrm__pax += '     else:\n'
                ihrm__pax += '         nb_row = 0\n'
                ihrm__pax += '  nb_row = bcast_scalar(nb_row)\n'
            ihrm__pax += f"""  with objmode(table_var=py_table_type_{jpanj__wpqos}, index_var=index_col_typ):
"""
            ihrm__pax += (
                '    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)\n'
                )
            if db_type == 'oracle':
                ihrm__pax += f"""    sql_cons = 'select * from (' + sql_request + ') OFFSET ' + str(offset) + ' ROWS FETCH NEXT ' + str(limit) + ' ROWS ONLY'
"""
            else:
                ihrm__pax += f"""    sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
            ihrm__pax += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            ihrm__pax += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        else:
            ihrm__pax += f"""  with objmode(table_var=py_table_type_{jpanj__wpqos}, index_var=index_col_typ):
"""
            ihrm__pax += '    df_ret = pd.read_sql(sql_request, conn)\n'
            ihrm__pax += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        if index_column_name:
            ihrm__pax += (
                f'    index_var = df_ret.iloc[:, {len(out_used_cols)}].values\n'
                )
            ihrm__pax += f"""    df_ret.drop(columns=df_ret.columns[{len(out_used_cols)}], inplace=True)
"""
        else:
            ihrm__pax += '    index_var = None\n'
        if out_used_cols:
            ihrm__pax += f'    arrs = []\n'
            ihrm__pax += f'    for i in range(df_ret.shape[1]):\n'
            ihrm__pax += f'      arrs.append(df_ret.iloc[:, i].values)\n'
            ihrm__pax += f"""    table_var = Table(arrs, type_usecols_offsets_arr_{jpanj__wpqos}_2, {len(col_names)})
"""
        else:
            ihrm__pax += '    table_var = None\n'
        ihrm__pax += '  return (-1, table_var, index_var)\n'
    fvp__lnym = globals()
    fvp__lnym.update({'bodo': bodo, f'py_table_type_{jpanj__wpqos}':
        avia__cjyvw, 'index_col_typ': index_column_type})
    if db_type in ('iceberg', 'snowflake'):
        fvp__lnym.update({'unicode_to_utf8': unicode_to_utf8,
            'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'info_to_array':
            info_to_array, 'info_from_table': info_from_table,
            'delete_table': delete_table, 'cpp_table_to_py_table':
            cpp_table_to_py_table, f'table_idx_{jpanj__wpqos}': upm__sng})
    if db_type == 'iceberg':
        fvp__lnym.update({f'selected_cols_arr_{jpanj__wpqos}': np.array(
            tiesv__sfusy, np.int32), f'nullable_cols_arr_{jpanj__wpqos}':
            np.array(fde__qhxn, np.int32), f'py_table_type_{jpanj__wpqos}':
            avia__cjyvw, f'pyarrow_table_schema_{jpanj__wpqos}':
            pyarrow_table_schema, 'get_filters_pyobject': bodo.io.
            parquet_pio.get_filters_pyobject, 'iceberg_read': _iceberg_read,
            'get_node_portion': bodo.libs.distributed_api.get_node_portion,
            'set_table_len': bodo.hiframes.table.set_table_len})
    elif db_type == 'snowflake':
        fvp__lnym.update({'np': np, 'snowflake_read': _snowflake_read})
    else:
        fvp__lnym.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar,
            'pymysql_check': pymysql_check, 'cx_oracle_check':
            cx_oracle_check, 'psycopg2_check': psycopg2_check, 'df_typeref':
            bodo.DataFrameType(tuple(phg__mspj), bodo.RangeIndexType(None),
            tuple(ysuav__pksj)), 'Table': Table,
            f'type_usecols_offsets_arr_{jpanj__wpqos}': fxbs__uyq})
    fntb__aqnu = {}
    exec(ihrm__pax, fvp__lnym, fntb__aqnu)
    fhq__mhqo = fntb__aqnu['sql_reader_py']
    lgu__kihdz = numba.njit(fhq__mhqo)
    compiled_funcs.append(lgu__kihdz)
    return lgu__kihdz


_snowflake_read = types.ExternalFunction('snowflake_read', table_type(types
    .voidptr, types.voidptr, types.boolean, types.int64, types.voidptr,
    types.voidptr, types.int32))
parquet_predicate_type = ParquetPredicateType()
pyarrow_table_schema_type = PyArrowTableSchemaType()
_iceberg_read = types.ExternalFunction('iceberg_pq_read', table_type(types.
    voidptr, types.voidptr, types.voidptr, types.boolean, types.int64,
    parquet_predicate_type, parquet_predicate_type, types.voidptr, types.
    int32, types.voidptr, pyarrow_table_schema_type, types.voidptr))
import llvmlite.binding as ll
from bodo.io import arrow_cpp
ll.add_symbol('snowflake_read', arrow_cpp.snowflake_read)
ll.add_symbol('iceberg_pq_read', arrow_cpp.iceberg_pq_read)
