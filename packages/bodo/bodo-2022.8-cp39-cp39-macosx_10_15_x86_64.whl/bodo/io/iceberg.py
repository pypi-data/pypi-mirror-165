"""
File that contains the main functionality for the Iceberg
integration within the Bodo repo. This does not contain the
main IR transformation.
"""
import os
import re
import sys
from typing import Any, Dict, List
from urllib.parse import urlparse
from uuid import uuid4
import numba
import numpy as np
import pyarrow as pa
from mpi4py import MPI
from numba.core import types
from numba.extending import intrinsic
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.io.fs_io import get_s3_bucket_region_njit
from bodo.io.helpers import is_nullable
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import unicode_to_utf8
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils import tracing
from bodo.utils.typing import BodoError, raise_bodo_error


def format_iceberg_conn(conn_str: str) ->str:
    rnso__redep = urlparse(conn_str)
    if not conn_str.startswith('iceberg+glue') and rnso__redep.scheme not in (
        'iceberg', 'iceberg+file', 'iceberg+s3', 'iceberg+thrift',
        'iceberg+http', 'iceberg+https'):
        raise BodoError(
            "'con' must start with one of the following: 'iceberg://', 'iceberg+file://', 'iceberg+s3://', 'iceberg+thrift://', 'iceberg+http://', 'iceberg+https://', 'iceberg+glue'"
            )
    if sys.version_info.minor < 9:
        if conn_str.startswith('iceberg+'):
            conn_str = conn_str[len('iceberg+'):]
        if conn_str.startswith('iceberg://'):
            conn_str = conn_str[len('iceberg://'):]
    else:
        conn_str = conn_str.removeprefix('iceberg+').removeprefix('iceberg://')
    return conn_str


@numba.njit
def format_iceberg_conn_njit(conn_str):
    with numba.objmode(conn_str='unicode_type'):
        conn_str = format_iceberg_conn(conn_str)
    return conn_str


def _clean_schema(schema: pa.Schema) ->pa.Schema:
    muq__ehy = schema
    for owtq__eoyj in range(len(schema)):
        inwk__xmg = schema.field(owtq__eoyj)
        if pa.types.is_floating(inwk__xmg.type):
            muq__ehy = muq__ehy.set(owtq__eoyj, inwk__xmg.with_nullable(False))
        elif pa.types.is_list(inwk__xmg.type):
            muq__ehy = muq__ehy.set(owtq__eoyj, inwk__xmg.with_type(pa.
                list_(pa.field('element', inwk__xmg.type.value_type))))
    return muq__ehy


def _schemas_equal(schema: pa.Schema, other: pa.Schema) ->bool:
    if schema.equals(other):
        return True
    hon__ngkzc = _clean_schema(schema)
    sxbb__xitny = _clean_schema(other)
    return hon__ngkzc.equals(sxbb__xitny)


def get_iceberg_type_info(table_name: str, con: str, database_schema: str):
    import bodo_iceberg_connector
    import numba.core
    from bodo.io.parquet_pio import _get_numba_typ_from_pa_typ
    kbp__hela = None
    tbrn__dkb = None
    pyarrow_schema = None
    if bodo.get_rank() == 0:
        try:
            kbp__hela, tbrn__dkb, pyarrow_schema = (bodo_iceberg_connector.
                get_iceberg_typing_schema(con, database_schema, table_name))
            if pyarrow_schema is None:
                raise BodoError('No such Iceberg table found')
        except bodo_iceberg_connector.IcebergError as qdbd__ntwcz:
            if isinstance(qdbd__ntwcz, bodo_iceberg_connector.IcebergJavaError
                ) and numba.core.config.DEVELOPER_MODE:
                kbp__hela = BodoError(
                    f'{qdbd__ntwcz.message}: {qdbd__ntwcz.java_error}')
            else:
                kbp__hela = BodoError(qdbd__ntwcz.message)
    poeme__uckz = MPI.COMM_WORLD
    kbp__hela = poeme__uckz.bcast(kbp__hela)
    if isinstance(kbp__hela, Exception):
        raise kbp__hela
    col_names = kbp__hela
    tbrn__dkb = poeme__uckz.bcast(tbrn__dkb)
    pyarrow_schema = poeme__uckz.bcast(pyarrow_schema)
    xuetr__yeq = [_get_numba_typ_from_pa_typ(roz__dohwl, False, True, None)
        [0] for roz__dohwl in tbrn__dkb]
    return col_names, xuetr__yeq, pyarrow_schema


def get_iceberg_file_list(table_name: str, conn: str, database_schema: str,
    filters) ->List[str]:
    import bodo_iceberg_connector
    import numba.core
    assert bodo.get_rank(
        ) == 0, 'get_iceberg_file_list should only ever be called on rank 0, as the operation requires access to the py4j server, which is only available on rank 0'
    try:
        krbt__tybua = (bodo_iceberg_connector.
            bodo_connector_get_parquet_file_list(conn, database_schema,
            table_name, filters))
    except bodo_iceberg_connector.IcebergError as qdbd__ntwcz:
        if isinstance(qdbd__ntwcz, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(f'{qdbd__ntwcz.message}:\n{qdbd__ntwcz.java_error}'
                )
        else:
            raise BodoError(qdbd__ntwcz.message)
    return krbt__tybua


class IcebergParquetDataset(object):

    def __init__(self, conn, database_schema, table_name, pa_table_schema,
        pq_dataset=None):
        self.pq_dataset = pq_dataset
        self.conn = conn
        self.database_schema = database_schema
        self.table_name = table_name
        self.schema = pa_table_schema
        self.pieces = []
        self._bodo_total_rows = 0
        self._prefix = ''
        self.filesystem = None
        if pq_dataset is not None:
            self.pieces = pq_dataset.pieces
            self._bodo_total_rows = pq_dataset._bodo_total_rows
            self._prefix = pq_dataset._prefix
            self.filesystem = pq_dataset.filesystem


def get_iceberg_pq_dataset(conn, database_schema, table_name,
    typing_pa_table_schema, dnf_filters=None, expr_filters=None,
    tot_rows_to_read=None, is_parallel=False):
    pmhdo__nbhtj = tracing.Event('get_iceberg_pq_dataset')
    poeme__uckz = MPI.COMM_WORLD
    ksv__dqlr = None
    if bodo.get_rank() == 0:
        jour__lri = tracing.Event('get_iceberg_file_list', is_parallel=False)
        try:
            ksv__dqlr = get_iceberg_file_list(table_name, conn,
                database_schema, dnf_filters)
            if tracing.is_tracing():
                bwt__qcnpj = int(os.environ.get(
                    'BODO_ICEBERG_TRACING_NUM_FILES_TO_LOG', '50'))
                jour__lri.add_attribute('num_files', len(ksv__dqlr))
                jour__lri.add_attribute(f'first_{bwt__qcnpj}_files', ', '.
                    join(ksv__dqlr[:bwt__qcnpj]))
        except Exception as qdbd__ntwcz:
            ksv__dqlr = qdbd__ntwcz
        jour__lri.finalize()
    ksv__dqlr = poeme__uckz.bcast(ksv__dqlr)
    if isinstance(ksv__dqlr, Exception):
        oup__yhop = ksv__dqlr
        raise BodoError(
            f"""Error reading Iceberg Table: {type(oup__yhop).__name__}: {str(oup__yhop)}
"""
            )
    yxbf__yyylp: List[str] = ksv__dqlr
    if len(yxbf__yyylp) == 0:
        pq_dataset = None
    else:
        try:
            pq_dataset = bodo.io.parquet_pio.get_parquet_dataset(yxbf__yyylp,
                get_row_counts=True, expr_filters=expr_filters, is_parallel
                =is_parallel, typing_pa_schema=typing_pa_table_schema,
                partitioning=None, tot_rows_to_read=tot_rows_to_read)
        except BodoError as qdbd__ntwcz:
            if re.search('Schema .* was different', str(qdbd__ntwcz), re.
                IGNORECASE):
                raise BodoError(
                    f"""Bodo currently doesn't support reading Iceberg tables with schema evolution.
{qdbd__ntwcz}"""
                    )
            else:
                raise
    qnj__clolo = IcebergParquetDataset(conn, database_schema, table_name,
        typing_pa_table_schema, pq_dataset)
    pmhdo__nbhtj.finalize()
    return qnj__clolo


_numba_pyarrow_type_map = {types.int8: pa.int8(), types.int16: pa.int16(),
    types.int32: pa.int32(), types.int64: pa.int64(), types.uint8: pa.uint8
    (), types.uint16: pa.uint16(), types.uint32: pa.uint32(), types.uint64:
    pa.uint64(), types.float32: pa.float32(), types.float64: pa.float64(),
    types.NPDatetime('ns'): pa.date64(), bodo.datetime64ns: pa.timestamp(
    'us', 'UTC')}


def _numba_to_pyarrow_type(numba_type: types.ArrayCompatible):
    if isinstance(numba_type, ArrayItemArrayType):
        mbz__vknhp = pa.list_(_numba_to_pyarrow_type(numba_type.dtype)[0])
    elif isinstance(numba_type, StructArrayType):
        vygf__dmna = []
        for tjwj__lrad, kaw__kvelo in zip(numba_type.names, numba_type.data):
            hiwd__lfxui, jdel__alm = _numba_to_pyarrow_type(kaw__kvelo)
            vygf__dmna.append(pa.field(tjwj__lrad, hiwd__lfxui, True))
        mbz__vknhp = pa.struct(vygf__dmna)
    elif isinstance(numba_type, DecimalArrayType):
        mbz__vknhp = pa.decimal128(numba_type.precision, numba_type.scale)
    elif isinstance(numba_type, CategoricalArrayType):
        ojo__paw: PDCategoricalDtype = numba_type.dtype
        mbz__vknhp = pa.dictionary(_numba_to_pyarrow_type(ojo__paw.int_type
            )[0], _numba_to_pyarrow_type(ojo__paw.elem_type)[0], ordered=
            False if ojo__paw.ordered is None else ojo__paw.ordered)
    elif numba_type == boolean_array:
        mbz__vknhp = pa.bool_()
    elif numba_type in (string_array_type, bodo.dict_str_arr_type):
        mbz__vknhp = pa.string()
    elif numba_type == binary_array_type:
        mbz__vknhp = pa.binary()
    elif numba_type == datetime_date_array_type:
        mbz__vknhp = pa.date32()
    elif isinstance(numba_type, bodo.DatetimeArrayType):
        mbz__vknhp = pa.timestamp('us', 'UTC')
    elif isinstance(numba_type, (types.Array, IntegerArrayType)
        ) and numba_type.dtype in _numba_pyarrow_type_map:
        mbz__vknhp = _numba_pyarrow_type_map[numba_type.dtype]
    else:
        raise BodoError(
            'Conversion from Bodo array type {} to PyArrow type not supported yet'
            .format(numba_type))
    return mbz__vknhp, is_nullable(numba_type)


def pyarrow_schema(df: DataFrameType) ->pa.Schema:
    vygf__dmna = []
    for tjwj__lrad, ocr__trf in zip(df.columns, df.data):
        try:
            osc__zkkbd, qqnq__yllf = _numba_to_pyarrow_type(ocr__trf)
        except BodoError as qdbd__ntwcz:
            raise_bodo_error(qdbd__ntwcz.msg, qdbd__ntwcz.loc)
        vygf__dmna.append(pa.field(tjwj__lrad, osc__zkkbd, qqnq__yllf))
    return pa.schema(vygf__dmna)


@numba.njit
def gen_iceberg_pq_fname():
    with numba.objmode(file_name='unicode_type'):
        poeme__uckz = MPI.COMM_WORLD
        bzy__rqy = poeme__uckz.Get_rank()
        file_name = f'{bzy__rqy:05}-{bzy__rqy}-{uuid4()}.parquet'
    return file_name


def get_table_details_before_write(table_name: str, conn: str,
    database_schema: str, df_pyarrow_schema, if_exists: str):
    import bodo_iceberg_connector as connector
    poeme__uckz = MPI.COMM_WORLD
    znuyy__rvkho = None
    iceberg_schema_id = None
    table_loc = ''
    partition_spec = ''
    sort_order = ''
    iceberg_schema_str = ''
    if poeme__uckz.Get_rank() == 0:
        try:
            (table_loc, iceberg_schema_id, pa_schema, iceberg_schema_str,
                partition_spec, sort_order) = (connector.get_typing_info(
                conn, database_schema, table_name))
            if (if_exists == 'append' and pa_schema is not None and not
                _schemas_equal(pa_schema, df_pyarrow_schema)):
                if numba.core.config.DEVELOPER_MODE:
                    raise BodoError(
                        f"""Iceberg Table and DataFrame Schemas Need to be Equal for Append

Iceberg:
{pa_schema}

DataFrame:
{df_pyarrow_schema}
"""
                        )
                else:
                    raise BodoError(
                        'Iceberg Table and DataFrame Schemas Need to be Equal for Append'
                        )
            if iceberg_schema_id is None:
                iceberg_schema_str = connector.pyarrow_to_iceberg_schema_str(
                    df_pyarrow_schema)
        except connector.IcebergError as qdbd__ntwcz:
            if isinstance(qdbd__ntwcz, connector.IcebergJavaError
                ) and numba.core.config.DEVELOPER_MODE:
                znuyy__rvkho = BodoError(
                    f'{qdbd__ntwcz.message}: {qdbd__ntwcz.java_error}')
            else:
                znuyy__rvkho = BodoError(qdbd__ntwcz.message)
        except Exception as qdbd__ntwcz:
            znuyy__rvkho = qdbd__ntwcz
    znuyy__rvkho = poeme__uckz.bcast(znuyy__rvkho)
    if isinstance(znuyy__rvkho, Exception):
        raise znuyy__rvkho
    table_loc = poeme__uckz.bcast(table_loc)
    iceberg_schema_id = poeme__uckz.bcast(iceberg_schema_id)
    partition_spec = poeme__uckz.bcast(partition_spec)
    sort_order = poeme__uckz.bcast(sort_order)
    iceberg_schema_str = poeme__uckz.bcast(iceberg_schema_str)
    if iceberg_schema_id is None:
        already_exists = False
        iceberg_schema_id = -1
    else:
        already_exists = True
    return (already_exists, table_loc, iceberg_schema_id, partition_spec,
        sort_order, iceberg_schema_str)


def register_table_write(conn_str: str, db_name: str, table_name: str,
    table_loc: str, fnames: List[str], all_metrics: Dict[str, List[Any]],
    iceberg_schema_id: int, pa_schema, partition_spec, sort_order, mode: str):
    import bodo_iceberg_connector
    poeme__uckz = MPI.COMM_WORLD
    success = False
    if poeme__uckz.Get_rank() == 0:
        kgpv__pnfh = None if iceberg_schema_id < 0 else iceberg_schema_id
        success = bodo_iceberg_connector.commit_write(conn_str, db_name,
            table_name, table_loc, fnames, all_metrics, kgpv__pnfh,
            pa_schema, partition_spec, sort_order, mode)
    success = poeme__uckz.bcast(success)
    return success


@numba.njit()
def iceberg_write(table_name, conn, database_schema, bodo_table, col_names,
    if_exists, is_parallel, df_pyarrow_schema):
    assert is_parallel, 'Iceberg Write only supported for distributed dataframes'
    with numba.objmode(already_exists='bool_', table_loc='unicode_type',
        iceberg_schema_id='i8', partition_spec='unicode_type', sort_order=
        'unicode_type', iceberg_schema_str='unicode_type'):
        (already_exists, table_loc, iceberg_schema_id, partition_spec,
            sort_order, iceberg_schema_str) = (get_table_details_before_write
            (table_name, conn, database_schema, df_pyarrow_schema, if_exists))
    if already_exists and if_exists == 'fail':
        raise ValueError(f'Table already exists.')
    if already_exists:
        mode = if_exists
    else:
        mode = 'create'
    egij__dnpe = gen_iceberg_pq_fname()
    bucket_region = get_s3_bucket_region_njit(table_loc, is_parallel)
    pyq__rvbvh = 'snappy'
    lpj__aqqy = -1
    bbsgu__iroi = np.zeros(1, dtype=np.int64)
    lmz__qple = np.zeros(1, dtype=np.int64)
    if not partition_spec and not sort_order:
        iceberg_pq_write_table_cpp(unicode_to_utf8(egij__dnpe),
            unicode_to_utf8(table_loc), bodo_table, col_names,
            unicode_to_utf8(pyq__rvbvh), is_parallel, unicode_to_utf8(
            bucket_region), lpj__aqqy, unicode_to_utf8(iceberg_schema_str),
            bbsgu__iroi.ctypes, lmz__qple.ctypes)
    else:
        raise Exception('Partition Spec and Sort Order not supported yet.')
    with numba.objmode(fnames='types.List(types.unicode_type)'):
        poeme__uckz = MPI.COMM_WORLD
        fnames = poeme__uckz.gather(egij__dnpe)
        if poeme__uckz.Get_rank() != 0:
            fnames = ['a', 'b']
    ivr__amib = bodo.gatherv(bbsgu__iroi)
    gri__xib = bodo.gatherv(lmz__qple)
    with numba.objmode(success='bool_'):
        success = register_table_write(conn, database_schema, table_name,
            table_loc, fnames, {'size': gri__xib.tolist(), 'record_count':
            ivr__amib.tolist()}, iceberg_schema_id, df_pyarrow_schema,
            partition_spec, sort_order, mode)
    if not success:
        raise BodoError('Iceberg write failed.')


import llvmlite.binding as ll
from llvmlite import ir as lir
from numba.core import cgutils, types
if bodo.utils.utils.has_pyarrow():
    from bodo.io import arrow_cpp
    ll.add_symbol('iceberg_pq_write', arrow_cpp.iceberg_pq_write)


@intrinsic
def iceberg_pq_write_table_cpp(typingctx, fname_t, path_name_t, table_t,
    col_names_t, compression_t, is_parallel_t, bucket_region,
    row_group_size, iceberg_metadata_t, record_count_t, file_size_in_bytes_t):

    def codegen(context, builder, sig, args):
        tyr__irnkn = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1), lir.IntType(8).as_pointer(), lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        ezz__onucm = cgutils.get_or_insert_function(builder.module,
            tyr__irnkn, name='iceberg_pq_write')
        builder.call(ezz__onucm, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, types.voidptr, table_t, col_names_t,
        types.voidptr, types.boolean, types.voidptr, types.int64, types.
        voidptr, types.voidptr, types.voidptr), codegen
