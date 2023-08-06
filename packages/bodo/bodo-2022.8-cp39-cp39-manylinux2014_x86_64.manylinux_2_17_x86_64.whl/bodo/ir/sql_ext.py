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
        atf__zvxgg = tuple(fwxcg__voxv.name for fwxcg__voxv in self.out_vars)
        return (
            f'{atf__zvxgg} = ReadSql(sql_request={self.sql_request}, connection={self.connection}, col_names={self.df_colnames}, types={self.out_types}, df_out={self.df_out}, limit={self.limit}, unsupported_columns={self.unsupported_columns}, unsupported_arrow_types={self.unsupported_arrow_types}, is_select_query={self.is_select_query}, index_column_name={self.index_column_name}, index_column_type={self.index_column_type}, out_used_cols={self.out_used_cols}, database_schema={self.database_schema}, pyarrow_table_schema={self.pyarrow_table_schema})'
            )


def parse_dbtype(con_str):
    wtdcr__yhby = urlparse(con_str)
    db_type = wtdcr__yhby.scheme
    iyg__zjen = wtdcr__yhby.password
    if con_str.startswith('oracle+cx_oracle://'):
        return 'oracle', iyg__zjen
    if db_type == 'mysql+pymysql':
        return 'mysql', iyg__zjen
    if con_str == 'iceberg+glue' or wtdcr__yhby.scheme in ('iceberg',
        'iceberg+file', 'iceberg+s3', 'iceberg+thrift', 'iceberg+http',
        'iceberg+https'):
        return 'iceberg', iyg__zjen
    return db_type, iyg__zjen


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
    ardu__ced = sql_node.out_vars[0].name
    vxguk__aqju = sql_node.out_vars[1].name
    if ardu__ced not in lives and vxguk__aqju not in lives:
        return None
    elif ardu__ced not in lives:
        sql_node.out_types = []
        sql_node.df_colnames = []
        sql_node.out_used_cols = []
    elif vxguk__aqju not in lives:
        sql_node.index_column_name = None
        sql_node.index_arr_typ = types.none
    return sql_node


def sql_distributed_run(sql_node, array_dists, typemap, calltypes,
    typingctx, targetctx, meta_head_only_info=None):
    if bodo.user_logging.get_verbose_level() >= 1:
        qwq__dcklb = (
            'Finish column pruning on read_sql node:\n%s\nColumns loaded %s\n')
        tyv__nexgk = []
        nstij__lybcd = []
        for lwsve__yow in sql_node.out_used_cols:
            smdcg__wgua = sql_node.df_colnames[lwsve__yow]
            tyv__nexgk.append(smdcg__wgua)
            if isinstance(sql_node.out_types[lwsve__yow], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                nstij__lybcd.append(smdcg__wgua)
        if sql_node.index_column_name:
            tyv__nexgk.append(sql_node.index_column_name)
            if isinstance(sql_node.index_column_type, bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                nstij__lybcd.append(sql_node.index_column_name)
        tiqn__wlejh = sql_node.loc.strformat()
        bodo.user_logging.log_message('Column Pruning', qwq__dcklb,
            tiqn__wlejh, tyv__nexgk)
        if nstij__lybcd:
            pyt__wtci = """Finished optimized encoding on read_sql node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', pyt__wtci,
                tiqn__wlejh, nstij__lybcd)
    parallel = bodo.ir.connector.is_connector_table_parallel(sql_node,
        array_dists, typemap, 'SQLReader')
    if sql_node.unsupported_columns:
        evs__djm = set(sql_node.unsupported_columns)
        otzp__xln = set(sql_node.out_used_cols)
        tgyd__vwqz = otzp__xln & evs__djm
        if tgyd__vwqz:
            wtwa__fjn = sorted(tgyd__vwqz)
            jerc__dykw = [
                f'pandas.read_sql(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                'Please manually remove these columns from your sql query by specifying the columns you need in your SELECT statement. If these '
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            sfls__wqbf = 0
            for kyita__zzea in wtwa__fjn:
                while sql_node.unsupported_columns[sfls__wqbf] != kyita__zzea:
                    sfls__wqbf += 1
                jerc__dykw.append(
                    f"Column '{sql_node.original_df_colnames[kyita__zzea]}' with unsupported arrow type {sql_node.unsupported_arrow_types[sfls__wqbf]}"
                    )
                sfls__wqbf += 1
            sjiq__nadt = '\n'.join(jerc__dykw)
            raise BodoError(sjiq__nadt, loc=sql_node.loc)
    qhxhq__mlzk, tgkik__zjrjd = bodo.ir.connector.generate_filter_map(sql_node
        .filters)
    wbajo__mrozy = ', '.join(qhxhq__mlzk.values())
    rxhou__nxhdf = (
        f'def sql_impl(sql_request, conn, database_schema, {wbajo__mrozy}):\n')
    if sql_node.filters and sql_node.db_type != 'iceberg':
        ulfjs__wuf = []
        for jtsxy__kxk in sql_node.filters:
            akuum__nhwt = []
            for mspl__zdt in jtsxy__kxk:
                zzde__jqmsi = '{' + qhxhq__mlzk[mspl__zdt[2].name
                    ] + '}' if isinstance(mspl__zdt[2], ir.Var) else mspl__zdt[
                    2]
                if mspl__zdt[1] in ('startswith', 'endswith'):
                    dyp__wnzu = ['(', mspl__zdt[1], '(', mspl__zdt[0], ',',
                        zzde__jqmsi, ')', ')']
                else:
                    dyp__wnzu = ['(', mspl__zdt[0], mspl__zdt[1],
                        zzde__jqmsi, ')']
                akuum__nhwt.append(' '.join(dyp__wnzu))
            ulfjs__wuf.append(' ( ' + ' AND '.join(akuum__nhwt) + ' ) ')
        jyygl__efrsc = ' WHERE ' + ' OR '.join(ulfjs__wuf)
        for lwsve__yow, aro__dyvo in enumerate(qhxhq__mlzk.values()):
            rxhou__nxhdf += f'    {aro__dyvo} = get_sql_literal({aro__dyvo})\n'
        rxhou__nxhdf += (
            f'    sql_request = f"{{sql_request}} {jyygl__efrsc}"\n')
    ttd__xyv = ''
    if sql_node.db_type == 'iceberg':
        ttd__xyv = wbajo__mrozy
    rxhou__nxhdf += f"""    (total_rows, table_var, index_var) = _sql_reader_py(sql_request, conn, database_schema, {ttd__xyv})
"""
    cbyy__kldak = {}
    exec(rxhou__nxhdf, {}, cbyy__kldak)
    cspyh__vmt = cbyy__kldak['sql_impl']
    if sql_node.limit is not None:
        limit = sql_node.limit
    elif meta_head_only_info and meta_head_only_info[0] is not None:
        limit = meta_head_only_info[0]
    else:
        limit = None
    job__uzh = _gen_sql_reader_py(sql_node.df_colnames, sql_node.out_types,
        sql_node.index_column_name, sql_node.index_column_type, sql_node.
        out_used_cols, typingctx, targetctx, sql_node.db_type, limit,
        parallel, typemap, sql_node.filters, sql_node.pyarrow_table_schema)
    ootxc__qsvx = (types.none if sql_node.database_schema is None else
        string_type)
    dtzpt__hfjha = compile_to_numba_ir(cspyh__vmt, {'_sql_reader_py':
        job__uzh, 'bcast_scalar': bcast_scalar, 'bcast': bcast,
        'get_sql_literal': _get_snowflake_sql_literal}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(string_type, string_type,
        ootxc__qsvx) + tuple(typemap[fwxcg__voxv.name] for fwxcg__voxv in
        tgkik__zjrjd), typemap=typemap, calltypes=calltypes).blocks.popitem()[1
        ]
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        gmxqf__lshzp = [sql_node.df_colnames[lwsve__yow] for lwsve__yow in
            sql_node.out_used_cols]
        if sql_node.index_column_name:
            gmxqf__lshzp.append(sql_node.index_column_name)
        qajyr__fguo = escape_column_names(gmxqf__lshzp, sql_node.db_type,
            sql_node.converted_colnames)
        if sql_node.db_type == 'oracle':
            jxd__qonz = ('SELECT ' + qajyr__fguo + ' FROM (' + sql_node.
                sql_request + ') TEMP')
        else:
            jxd__qonz = ('SELECT ' + qajyr__fguo + ' FROM (' + sql_node.
                sql_request + ') as TEMP')
    else:
        jxd__qonz = sql_node.sql_request
    replace_arg_nodes(dtzpt__hfjha, [ir.Const(jxd__qonz, sql_node.loc), ir.
        Const(sql_node.connection, sql_node.loc), ir.Const(sql_node.
        database_schema, sql_node.loc)] + tgkik__zjrjd)
    mpj__coijb = dtzpt__hfjha.body[:-3]
    if meta_head_only_info:
        mpj__coijb[-3].target = meta_head_only_info[1]
    mpj__coijb[-2].target = sql_node.out_vars[0]
    mpj__coijb[-1].target = sql_node.out_vars[1]
    assert not (sql_node.index_column_name is None and not sql_node.
        out_used_cols
        ), 'At most one of table and index should be dead if the SQL IR node is live'
    if sql_node.index_column_name is None:
        mpj__coijb.pop(-1)
    elif not sql_node.out_used_cols:
        mpj__coijb.pop(-2)
    return mpj__coijb


def escape_column_names(col_names, db_type, converted_colnames):
    if db_type in ('snowflake', 'oracle'):
        gmxqf__lshzp = [(bjkce__cso.upper() if bjkce__cso in
            converted_colnames else bjkce__cso) for bjkce__cso in col_names]
        qajyr__fguo = ', '.join([f'"{bjkce__cso}"' for bjkce__cso in
            gmxqf__lshzp])
    elif db_type == 'mysql':
        qajyr__fguo = ', '.join([f'`{bjkce__cso}`' for bjkce__cso in col_names]
            )
    else:
        qajyr__fguo = ', '.join([f'"{bjkce__cso}"' for bjkce__cso in col_names]
            )
    return qajyr__fguo


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal_scalar(filter_value):
    tqvh__pgs = types.unliteral(filter_value)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tqvh__pgs,
        'Filter pushdown')
    if tqvh__pgs == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(tqvh__pgs, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif tqvh__pgs == bodo.pd_timestamp_type:

        def impl(filter_value):
            zom__tcsk = filter_value.nanosecond
            vitor__ndc = ''
            if zom__tcsk < 10:
                vitor__ndc = '00'
            elif zom__tcsk < 100:
                vitor__ndc = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{vitor__ndc}{zom__tcsk}'"
                )
        return impl
    elif tqvh__pgs == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported scalar type {tqvh__pgs} used in filter pushdown.'
            )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    scalar_isinstance = types.Integer, types.Float
    eqy__peu = (bodo.datetime_date_type, bodo.pd_timestamp_type, types.
        unicode_type, types.bool_)
    tqvh__pgs = types.unliteral(filter_value)
    if isinstance(tqvh__pgs, types.List) and (isinstance(tqvh__pgs.dtype,
        scalar_isinstance) or tqvh__pgs.dtype in eqy__peu):

        def impl(filter_value):
            feco__kie = ', '.join([_get_snowflake_sql_literal_scalar(
                bjkce__cso) for bjkce__cso in filter_value])
            return f'({feco__kie})'
        return impl
    elif isinstance(tqvh__pgs, scalar_isinstance) or tqvh__pgs in eqy__peu:
        return lambda filter_value: _get_snowflake_sql_literal_scalar(
            filter_value)
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {tqvh__pgs} used in filter pushdown.'
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
    except ImportError as ahzx__fty:
        mvyyq__rcy = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(mvyyq__rcy)


@numba.njit
def pymysql_check():
    with numba.objmode():
        pymysql_check_()


def pymysql_check_():
    try:
        import pymysql
    except ImportError as ahzx__fty:
        mvyyq__rcy = (
            "Using MySQL URI string requires pymsql to be installed. It can be installed by calling 'conda install -c conda-forge pymysql' or 'pip install PyMySQL'."
            )
        raise BodoError(mvyyq__rcy)


@numba.njit
def cx_oracle_check():
    with numba.objmode():
        cx_oracle_check_()


def cx_oracle_check_():
    try:
        import cx_Oracle
    except ImportError as ahzx__fty:
        mvyyq__rcy = (
            "Using Oracle URI string requires cx_oracle to be installed. It can be installed by calling 'conda install -c conda-forge cx_oracle' or 'pip install cx-Oracle'."
            )
        raise BodoError(mvyyq__rcy)


@numba.njit
def psycopg2_check():
    with numba.objmode():
        psycopg2_check_()


def psycopg2_check_():
    try:
        import psycopg2
    except ImportError as ahzx__fty:
        mvyyq__rcy = (
            "Using PostgreSQL URI string requires psycopg2 to be installed. It can be installed by calling 'conda install -c conda-forge psycopg2' or 'pip install psycopg2'."
            )
        raise BodoError(mvyyq__rcy)


def req_limit(sql_request):
    import re
    jnn__vhqh = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    olopz__qgdqv = jnn__vhqh.search(sql_request)
    if olopz__qgdqv:
        return int(olopz__qgdqv.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names: List[str], col_typs, index_column_name:
    str, index_column_type, out_used_cols: List[int], typingctx, targetctx,
    db_type: str, limit: Optional[int], parallel, typemap, filters,
    pyarrow_table_schema: 'Optional[pyarrow.Schema]'):
    rdi__neg = next_label()
    gmxqf__lshzp = [col_names[lwsve__yow] for lwsve__yow in out_used_cols]
    zmnhc__rclp = [col_typs[lwsve__yow] for lwsve__yow in out_used_cols]
    if index_column_name:
        gmxqf__lshzp.append(index_column_name)
        zmnhc__rclp.append(index_column_type)
    axery__fklli = None
    hyizo__lun = None
    ezu__orpnw = TableType(tuple(col_typs)) if out_used_cols else types.none
    ttd__xyv = ''
    qhxhq__mlzk = {}
    tgkik__zjrjd = []
    if filters and db_type == 'iceberg':
        qhxhq__mlzk, tgkik__zjrjd = bodo.ir.connector.generate_filter_map(
            filters)
        ttd__xyv = ', '.join(qhxhq__mlzk.values())
    rxhou__nxhdf = (
        f'def sql_reader_py(sql_request, conn, database_schema, {ttd__xyv}):\n'
        )
    if db_type == 'iceberg':
        assert pyarrow_table_schema is not None, 'SQLNode must contain a pyarrow_table_schema if reading from an Iceberg database'
        ins__cuai, tfllo__jdpp = bodo.ir.connector.generate_arrow_filters(
            filters, qhxhq__mlzk, tgkik__zjrjd, col_names, col_names,
            col_typs, typemap, 'iceberg')
        qgnv__nuhwf: List[int] = [pyarrow_table_schema.get_field_index(
            col_names[lwsve__yow]) for lwsve__yow in out_used_cols]
        suhsu__jbdkv = {rbnq__uqb: lwsve__yow for lwsve__yow, rbnq__uqb in
            enumerate(qgnv__nuhwf)}
        gxew__bgp = [int(is_nullable(col_typs[lwsve__yow])) for lwsve__yow in
            qgnv__nuhwf]
        jcfq__fsaav = ',' if ttd__xyv else ''
        rxhou__nxhdf += f"""  ev = bodo.utils.tracing.Event('read_iceberg', {parallel})
  dnf_filters, expr_filters = get_filters_pyobject("{ins__cuai}", "{tfllo__jdpp}", ({ttd__xyv}{jcfq__fsaav}))
  total_rows_np = np.array([0], dtype=np.int64)
  out_table = iceberg_read(
    unicode_to_utf8(conn),
    unicode_to_utf8(database_schema),
    unicode_to_utf8(sql_request),
    {parallel},
    {-1 if limit is None else limit},
    dnf_filters,
    expr_filters,
    selected_cols_arr_{rdi__neg}.ctypes,
    {len(qgnv__nuhwf)},
    nullable_cols_arr_{rdi__neg}.ctypes,
    pyarrow_table_schema_{rdi__neg},
    total_rows_np.ctypes,
  )
  check_and_propagate_cpp_exception()
"""
        rxhou__nxhdf += f'  total_rows = total_rows_np[0]\n'
        if parallel:
            rxhou__nxhdf += f"""  local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
        else:
            rxhou__nxhdf += f'  local_rows = total_rows\n'
        ukp__sghwl = not out_used_cols
        ezu__orpnw = TableType(tuple(col_typs))
        if ukp__sghwl:
            ezu__orpnw = types.none
        axery__fklli = None
        if not ukp__sghwl:
            axery__fklli = []
            mnt__zvcr = 0
            for lwsve__yow in range(len(col_names)):
                if mnt__zvcr < len(out_used_cols
                    ) and lwsve__yow == out_used_cols[mnt__zvcr]:
                    axery__fklli.append(suhsu__jbdkv[lwsve__yow])
                    mnt__zvcr += 1
                else:
                    axery__fklli.append(-1)
            axery__fklli = np.array(axery__fklli, dtype=np.int64)
        if ukp__sghwl:
            rxhou__nxhdf += '  table_var = None\n'
        else:
            rxhou__nxhdf += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{rdi__neg}, py_table_type_{rdi__neg})
"""
            if len(out_used_cols) == 0:
                rxhou__nxhdf += (
                    f'  table_var = set_table_len(table_var, local_rows)\n')
        vxguk__aqju = 'None'
        if index_column_name is not None:
            fjhpc__feqg = len(out_used_cols) + 1 if not ukp__sghwl else 0
            vxguk__aqju = (
                f'info_to_array(info_from_table(out_table, {fjhpc__feqg}), index_col_typ)'
                )
        rxhou__nxhdf += f'  index_var = {vxguk__aqju}\n'
        rxhou__nxhdf += f'  delete_table(out_table)\n'
        rxhou__nxhdf += f'  ev.finalize()\n'
        rxhou__nxhdf += '  return (total_rows, table_var, index_var)\n'
    elif db_type == 'snowflake':
        tic__psg = {rbnq__uqb: lwsve__yow for lwsve__yow, rbnq__uqb in
            enumerate(out_used_cols)}
        bwinq__denh = [tic__psg[lwsve__yow] for lwsve__yow in out_used_cols if
            col_typs[lwsve__yow] == dict_str_arr_type]
        rxhou__nxhdf += (
            f"  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})\n")
        gxew__bgp = [int(is_nullable(col_typs[lwsve__yow])) for lwsve__yow in
            out_used_cols]
        if index_column_name:
            gxew__bgp.append(int(is_nullable(index_column_type)))
        rxhou__nxhdf += f"""  out_table = snowflake_read(unicode_to_utf8(sql_request), unicode_to_utf8(conn), {parallel}, {len(gxew__bgp)}, np.array({gxew__bgp}, dtype=np.int32).ctypes,
"""
        if len(bwinq__denh) > 0:
            rxhou__nxhdf += f"""        np.array({bwinq__denh}, dtype=np.int32).ctypes, {len(bwinq__denh)})
"""
        else:
            rxhou__nxhdf += f'        0, 0)\n'
        rxhou__nxhdf += '  check_and_propagate_cpp_exception()\n'
        if index_column_name:
            rxhou__nxhdf += f"""  index_var = info_to_array(info_from_table(out_table, {len(out_used_cols)}), index_col_typ)
"""
        else:
            rxhou__nxhdf += '  index_var = None\n'
        if out_used_cols:
            sfls__wqbf = []
            mnt__zvcr = 0
            for lwsve__yow in range(len(col_names)):
                if mnt__zvcr < len(out_used_cols
                    ) and lwsve__yow == out_used_cols[mnt__zvcr]:
                    sfls__wqbf.append(mnt__zvcr)
                    mnt__zvcr += 1
                else:
                    sfls__wqbf.append(-1)
            axery__fklli = np.array(sfls__wqbf, dtype=np.int64)
            rxhou__nxhdf += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{rdi__neg}, py_table_type_{rdi__neg})
"""
        else:
            rxhou__nxhdf += '  table_var = None\n'
        rxhou__nxhdf += '  delete_table(out_table)\n'
        rxhou__nxhdf += f'  ev.finalize()\n'
        rxhou__nxhdf += '  return (-1, table_var, index_var)\n'
    else:
        if out_used_cols:
            rxhou__nxhdf += f"""  type_usecols_offsets_arr_{rdi__neg}_2 = type_usecols_offsets_arr_{rdi__neg}
"""
            hyizo__lun = np.array(out_used_cols, dtype=np.int64)
        rxhou__nxhdf += '  df_typeref_2 = df_typeref\n'
        rxhou__nxhdf += '  sqlalchemy_check()\n'
        if db_type == 'mysql':
            rxhou__nxhdf += '  pymysql_check()\n'
        elif db_type == 'oracle':
            rxhou__nxhdf += '  cx_oracle_check()\n'
        elif db_type == 'postgresql' or db_type == 'postgresql+psycopg2':
            rxhou__nxhdf += '  psycopg2_check()\n'
        if parallel:
            rxhou__nxhdf += '  rank = bodo.libs.distributed_api.get_rank()\n'
            if limit is not None:
                rxhou__nxhdf += f'  nb_row = {limit}\n'
            else:
                rxhou__nxhdf += '  with objmode(nb_row="int64"):\n'
                rxhou__nxhdf += f'     if rank == {MPI_ROOT}:\n'
                rxhou__nxhdf += """         sql_cons = 'select count(*) from (' + sql_request + ') x'
"""
                rxhou__nxhdf += (
                    '         frame = pd.read_sql(sql_cons, conn)\n')
                rxhou__nxhdf += '         nb_row = frame.iat[0,0]\n'
                rxhou__nxhdf += '     else:\n'
                rxhou__nxhdf += '         nb_row = 0\n'
                rxhou__nxhdf += '  nb_row = bcast_scalar(nb_row)\n'
            rxhou__nxhdf += f"""  with objmode(table_var=py_table_type_{rdi__neg}, index_var=index_col_typ):
"""
            rxhou__nxhdf += """    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)
"""
            if db_type == 'oracle':
                rxhou__nxhdf += f"""    sql_cons = 'select * from (' + sql_request + ') OFFSET ' + str(offset) + ' ROWS FETCH NEXT ' + str(limit) + ' ROWS ONLY'
"""
            else:
                rxhou__nxhdf += f"""    sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
            rxhou__nxhdf += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            rxhou__nxhdf += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        else:
            rxhou__nxhdf += f"""  with objmode(table_var=py_table_type_{rdi__neg}, index_var=index_col_typ):
"""
            rxhou__nxhdf += '    df_ret = pd.read_sql(sql_request, conn)\n'
            rxhou__nxhdf += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        if index_column_name:
            rxhou__nxhdf += (
                f'    index_var = df_ret.iloc[:, {len(out_used_cols)}].values\n'
                )
            rxhou__nxhdf += f"""    df_ret.drop(columns=df_ret.columns[{len(out_used_cols)}], inplace=True)
"""
        else:
            rxhou__nxhdf += '    index_var = None\n'
        if out_used_cols:
            rxhou__nxhdf += f'    arrs = []\n'
            rxhou__nxhdf += f'    for i in range(df_ret.shape[1]):\n'
            rxhou__nxhdf += f'      arrs.append(df_ret.iloc[:, i].values)\n'
            rxhou__nxhdf += f"""    table_var = Table(arrs, type_usecols_offsets_arr_{rdi__neg}_2, {len(col_names)})
"""
        else:
            rxhou__nxhdf += '    table_var = None\n'
        rxhou__nxhdf += '  return (-1, table_var, index_var)\n'
    lte__xfj = globals()
    lte__xfj.update({'bodo': bodo, f'py_table_type_{rdi__neg}': ezu__orpnw,
        'index_col_typ': index_column_type})
    if db_type in ('iceberg', 'snowflake'):
        lte__xfj.update({'unicode_to_utf8': unicode_to_utf8,
            'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'info_to_array':
            info_to_array, 'info_from_table': info_from_table,
            'delete_table': delete_table, 'cpp_table_to_py_table':
            cpp_table_to_py_table, f'table_idx_{rdi__neg}': axery__fklli})
    if db_type == 'iceberg':
        lte__xfj.update({f'selected_cols_arr_{rdi__neg}': np.array(
            qgnv__nuhwf, np.int32), f'nullable_cols_arr_{rdi__neg}': np.
            array(gxew__bgp, np.int32), f'py_table_type_{rdi__neg}':
            ezu__orpnw, f'pyarrow_table_schema_{rdi__neg}':
            pyarrow_table_schema, 'get_filters_pyobject': bodo.io.
            parquet_pio.get_filters_pyobject, 'iceberg_read': _iceberg_read,
            'get_node_portion': bodo.libs.distributed_api.get_node_portion,
            'set_table_len': bodo.hiframes.table.set_table_len})
    elif db_type == 'snowflake':
        lte__xfj.update({'np': np, 'snowflake_read': _snowflake_read})
    else:
        lte__xfj.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar,
            'pymysql_check': pymysql_check, 'cx_oracle_check':
            cx_oracle_check, 'psycopg2_check': psycopg2_check, 'df_typeref':
            bodo.DataFrameType(tuple(zmnhc__rclp), bodo.RangeIndexType(None
            ), tuple(gmxqf__lshzp)), 'Table': Table,
            f'type_usecols_offsets_arr_{rdi__neg}': hyizo__lun})
    cbyy__kldak = {}
    exec(rxhou__nxhdf, lte__xfj, cbyy__kldak)
    job__uzh = cbyy__kldak['sql_reader_py']
    trn__oik = numba.njit(job__uzh)
    compiled_funcs.append(trn__oik)
    return trn__oik


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
