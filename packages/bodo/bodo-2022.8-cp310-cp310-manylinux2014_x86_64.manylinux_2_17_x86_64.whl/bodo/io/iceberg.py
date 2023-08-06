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
    igk__vogr = urlparse(conn_str)
    if not conn_str.startswith('iceberg+glue') and igk__vogr.scheme not in (
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
    cmlvc__npokt = schema
    for ruwjf__cmb in range(len(schema)):
        oowym__rqou = schema.field(ruwjf__cmb)
        if pa.types.is_floating(oowym__rqou.type):
            cmlvc__npokt = cmlvc__npokt.set(ruwjf__cmb, oowym__rqou.
                with_nullable(False))
        elif pa.types.is_list(oowym__rqou.type):
            cmlvc__npokt = cmlvc__npokt.set(ruwjf__cmb, oowym__rqou.
                with_type(pa.list_(pa.field('element', oowym__rqou.type.
                value_type))))
    return cmlvc__npokt


def _schemas_equal(schema: pa.Schema, other: pa.Schema) ->bool:
    if schema.equals(other):
        return True
    ibg__dtv = _clean_schema(schema)
    xnvwa__lqlse = _clean_schema(other)
    return ibg__dtv.equals(xnvwa__lqlse)


def get_iceberg_type_info(table_name: str, con: str, database_schema: str):
    import bodo_iceberg_connector
    import numba.core
    from bodo.io.parquet_pio import _get_numba_typ_from_pa_typ
    baiko__zogfs = None
    hpqx__hqrag = None
    pyarrow_schema = None
    if bodo.get_rank() == 0:
        try:
            baiko__zogfs, hpqx__hqrag, pyarrow_schema = (bodo_iceberg_connector
                .get_iceberg_typing_schema(con, database_schema, table_name))
            if pyarrow_schema is None:
                raise BodoError('No such Iceberg table found')
        except bodo_iceberg_connector.IcebergError as ynd__feui:
            if isinstance(ynd__feui, bodo_iceberg_connector.IcebergJavaError
                ) and numba.core.config.DEVELOPER_MODE:
                baiko__zogfs = BodoError(
                    f'{ynd__feui.message}: {ynd__feui.java_error}')
            else:
                baiko__zogfs = BodoError(ynd__feui.message)
    egpb__wxac = MPI.COMM_WORLD
    baiko__zogfs = egpb__wxac.bcast(baiko__zogfs)
    if isinstance(baiko__zogfs, Exception):
        raise baiko__zogfs
    col_names = baiko__zogfs
    hpqx__hqrag = egpb__wxac.bcast(hpqx__hqrag)
    pyarrow_schema = egpb__wxac.bcast(pyarrow_schema)
    xkpw__aon = [_get_numba_typ_from_pa_typ(zdyvi__vuj, False, True, None)[
        0] for zdyvi__vuj in hpqx__hqrag]
    return col_names, xkpw__aon, pyarrow_schema


def get_iceberg_file_list(table_name: str, conn: str, database_schema: str,
    filters) ->List[str]:
    import bodo_iceberg_connector
    import numba.core
    assert bodo.get_rank(
        ) == 0, 'get_iceberg_file_list should only ever be called on rank 0, as the operation requires access to the py4j server, which is only available on rank 0'
    try:
        wzlw__yrycv = (bodo_iceberg_connector.
            bodo_connector_get_parquet_file_list(conn, database_schema,
            table_name, filters))
    except bodo_iceberg_connector.IcebergError as ynd__feui:
        if isinstance(ynd__feui, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(f'{ynd__feui.message}:\n{ynd__feui.java_error}')
        else:
            raise BodoError(ynd__feui.message)
    return wzlw__yrycv


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
    rdp__rxw = tracing.Event('get_iceberg_pq_dataset')
    egpb__wxac = MPI.COMM_WORLD
    expvi__rax = None
    if bodo.get_rank() == 0:
        rpay__kxpy = tracing.Event('get_iceberg_file_list', is_parallel=False)
        try:
            expvi__rax = get_iceberg_file_list(table_name, conn,
                database_schema, dnf_filters)
            if tracing.is_tracing():
                wtuhr__dxkp = int(os.environ.get(
                    'BODO_ICEBERG_TRACING_NUM_FILES_TO_LOG', '50'))
                rpay__kxpy.add_attribute('num_files', len(expvi__rax))
                rpay__kxpy.add_attribute(f'first_{wtuhr__dxkp}_files', ', '
                    .join(expvi__rax[:wtuhr__dxkp]))
        except Exception as ynd__feui:
            expvi__rax = ynd__feui
        rpay__kxpy.finalize()
    expvi__rax = egpb__wxac.bcast(expvi__rax)
    if isinstance(expvi__rax, Exception):
        ytikz__sxom = expvi__rax
        raise BodoError(
            f"""Error reading Iceberg Table: {type(ytikz__sxom).__name__}: {str(ytikz__sxom)}
"""
            )
    zmk__pblgq: List[str] = expvi__rax
    if len(zmk__pblgq) == 0:
        pq_dataset = None
    else:
        try:
            pq_dataset = bodo.io.parquet_pio.get_parquet_dataset(zmk__pblgq,
                get_row_counts=True, expr_filters=expr_filters, is_parallel
                =is_parallel, typing_pa_schema=typing_pa_table_schema,
                partitioning=None, tot_rows_to_read=tot_rows_to_read)
        except BodoError as ynd__feui:
            if re.search('Schema .* was different', str(ynd__feui), re.
                IGNORECASE):
                raise BodoError(
                    f"""Bodo currently doesn't support reading Iceberg tables with schema evolution.
{ynd__feui}"""
                    )
            else:
                raise
    rweah__cbnqa = IcebergParquetDataset(conn, database_schema, table_name,
        typing_pa_table_schema, pq_dataset)
    rdp__rxw.finalize()
    return rweah__cbnqa


_numba_pyarrow_type_map = {types.int8: pa.int8(), types.int16: pa.int16(),
    types.int32: pa.int32(), types.int64: pa.int64(), types.uint8: pa.uint8
    (), types.uint16: pa.uint16(), types.uint32: pa.uint32(), types.uint64:
    pa.uint64(), types.float32: pa.float32(), types.float64: pa.float64(),
    types.NPDatetime('ns'): pa.date64(), bodo.datetime64ns: pa.timestamp(
    'us', 'UTC')}


def _numba_to_pyarrow_type(numba_type: types.ArrayCompatible):
    if isinstance(numba_type, ArrayItemArrayType):
        uwtk__qdq = pa.list_(_numba_to_pyarrow_type(numba_type.dtype)[0])
    elif isinstance(numba_type, StructArrayType):
        ijq__ykw = []
        for gxp__fczi, axkux__elhei in zip(numba_type.names, numba_type.data):
            uen__zck, lmhc__dtvhf = _numba_to_pyarrow_type(axkux__elhei)
            ijq__ykw.append(pa.field(gxp__fczi, uen__zck, True))
        uwtk__qdq = pa.struct(ijq__ykw)
    elif isinstance(numba_type, DecimalArrayType):
        uwtk__qdq = pa.decimal128(numba_type.precision, numba_type.scale)
    elif isinstance(numba_type, CategoricalArrayType):
        rouw__tuz: PDCategoricalDtype = numba_type.dtype
        uwtk__qdq = pa.dictionary(_numba_to_pyarrow_type(rouw__tuz.int_type
            )[0], _numba_to_pyarrow_type(rouw__tuz.elem_type)[0], ordered=
            False if rouw__tuz.ordered is None else rouw__tuz.ordered)
    elif numba_type == boolean_array:
        uwtk__qdq = pa.bool_()
    elif numba_type in (string_array_type, bodo.dict_str_arr_type):
        uwtk__qdq = pa.string()
    elif numba_type == binary_array_type:
        uwtk__qdq = pa.binary()
    elif numba_type == datetime_date_array_type:
        uwtk__qdq = pa.date32()
    elif isinstance(numba_type, bodo.DatetimeArrayType):
        uwtk__qdq = pa.timestamp('us', 'UTC')
    elif isinstance(numba_type, (types.Array, IntegerArrayType)
        ) and numba_type.dtype in _numba_pyarrow_type_map:
        uwtk__qdq = _numba_pyarrow_type_map[numba_type.dtype]
    else:
        raise BodoError(
            'Conversion from Bodo array type {} to PyArrow type not supported yet'
            .format(numba_type))
    return uwtk__qdq, is_nullable(numba_type)


def pyarrow_schema(df: DataFrameType) ->pa.Schema:
    ijq__ykw = []
    for gxp__fczi, bet__rti in zip(df.columns, df.data):
        try:
            zlyfj__enpx, zfx__xiw = _numba_to_pyarrow_type(bet__rti)
        except BodoError as ynd__feui:
            raise_bodo_error(ynd__feui.msg, ynd__feui.loc)
        ijq__ykw.append(pa.field(gxp__fczi, zlyfj__enpx, zfx__xiw))
    return pa.schema(ijq__ykw)


@numba.njit
def gen_iceberg_pq_fname():
    with numba.objmode(file_name='unicode_type'):
        egpb__wxac = MPI.COMM_WORLD
        poju__ukml = egpb__wxac.Get_rank()
        file_name = f'{poju__ukml:05}-{poju__ukml}-{uuid4()}.parquet'
    return file_name


def get_table_details_before_write(table_name: str, conn: str,
    database_schema: str, df_pyarrow_schema, if_exists: str):
    import bodo_iceberg_connector as connector
    egpb__wxac = MPI.COMM_WORLD
    ryplu__bjqc = None
    iceberg_schema_id = None
    table_loc = ''
    partition_spec = ''
    sort_order = ''
    iceberg_schema_str = ''
    if egpb__wxac.Get_rank() == 0:
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
        except connector.IcebergError as ynd__feui:
            if isinstance(ynd__feui, connector.IcebergJavaError
                ) and numba.core.config.DEVELOPER_MODE:
                ryplu__bjqc = BodoError(
                    f'{ynd__feui.message}: {ynd__feui.java_error}')
            else:
                ryplu__bjqc = BodoError(ynd__feui.message)
        except Exception as ynd__feui:
            ryplu__bjqc = ynd__feui
    ryplu__bjqc = egpb__wxac.bcast(ryplu__bjqc)
    if isinstance(ryplu__bjqc, Exception):
        raise ryplu__bjqc
    table_loc = egpb__wxac.bcast(table_loc)
    iceberg_schema_id = egpb__wxac.bcast(iceberg_schema_id)
    partition_spec = egpb__wxac.bcast(partition_spec)
    sort_order = egpb__wxac.bcast(sort_order)
    iceberg_schema_str = egpb__wxac.bcast(iceberg_schema_str)
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
    egpb__wxac = MPI.COMM_WORLD
    success = False
    if egpb__wxac.Get_rank() == 0:
        zpe__ibvma = None if iceberg_schema_id < 0 else iceberg_schema_id
        success = bodo_iceberg_connector.commit_write(conn_str, db_name,
            table_name, table_loc, fnames, all_metrics, zpe__ibvma,
            pa_schema, partition_spec, sort_order, mode)
    success = egpb__wxac.bcast(success)
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
    idcyk__pwbi = gen_iceberg_pq_fname()
    bucket_region = get_s3_bucket_region_njit(table_loc, is_parallel)
    qgonm__cypl = 'snappy'
    wwc__hdsaf = -1
    frfum__zby = np.zeros(1, dtype=np.int64)
    cigfl__pab = np.zeros(1, dtype=np.int64)
    if not partition_spec and not sort_order:
        iceberg_pq_write_table_cpp(unicode_to_utf8(idcyk__pwbi),
            unicode_to_utf8(table_loc), bodo_table, col_names,
            unicode_to_utf8(qgonm__cypl), is_parallel, unicode_to_utf8(
            bucket_region), wwc__hdsaf, unicode_to_utf8(iceberg_schema_str),
            frfum__zby.ctypes, cigfl__pab.ctypes)
    else:
        raise Exception('Partition Spec and Sort Order not supported yet.')
    with numba.objmode(fnames='types.List(types.unicode_type)'):
        egpb__wxac = MPI.COMM_WORLD
        fnames = egpb__wxac.gather(idcyk__pwbi)
        if egpb__wxac.Get_rank() != 0:
            fnames = ['a', 'b']
    qjwj__ufjqp = bodo.gatherv(frfum__zby)
    fty__cxbc = bodo.gatherv(cigfl__pab)
    with numba.objmode(success='bool_'):
        success = register_table_write(conn, database_schema, table_name,
            table_loc, fnames, {'size': fty__cxbc.tolist(), 'record_count':
            qjwj__ufjqp.tolist()}, iceberg_schema_id, df_pyarrow_schema,
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
        gfc__pjq = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1), lir.IntType(8).as_pointer(), lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        kzcx__rtv = cgutils.get_or_insert_function(builder.module, gfc__pjq,
            name='iceberg_pq_write')
        builder.call(kzcx__rtv, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, types.voidptr, table_t, col_names_t,
        types.voidptr, types.boolean, types.voidptr, types.int64, types.
        voidptr, types.voidptr, types.voidptr), codegen
