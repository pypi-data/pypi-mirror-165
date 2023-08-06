import atexit
import datetime
import sys
import time
import warnings
from collections import defaultdict
from decimal import Decimal
from enum import Enum
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from mpi4py import MPI
from numba.core import cgutils, ir_utils, types
from numba.core.typing import signature
from numba.core.typing.builtins import IndexValueType
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, overload, register_jitable
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.libs import hdist
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, np_offset_type, offset_type
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType, set_bit_to_arr
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType
from bodo.libs.str_arr_ext import convert_len_arr_to_offset, get_bit_bitmap, get_data_ptr, get_null_bitmap_ptr, get_offset_ptr, num_total_chars, pre_alloc_string_array, set_bit_to, string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoError, BodoWarning, ColNamesMetaType, decode_if_dict_array, is_overload_false, is_overload_none, is_str_arr_type
from bodo.utils.utils import CTypeEnum, check_and_propagate_cpp_exception, empty_like_type, is_array_typ, numba_to_c_type
ll.add_symbol('dist_get_time', hdist.dist_get_time)
ll.add_symbol('get_time', hdist.get_time)
ll.add_symbol('dist_reduce', hdist.dist_reduce)
ll.add_symbol('dist_arr_reduce', hdist.dist_arr_reduce)
ll.add_symbol('dist_exscan', hdist.dist_exscan)
ll.add_symbol('dist_irecv', hdist.dist_irecv)
ll.add_symbol('dist_isend', hdist.dist_isend)
ll.add_symbol('dist_wait', hdist.dist_wait)
ll.add_symbol('dist_get_item_pointer', hdist.dist_get_item_pointer)
ll.add_symbol('get_dummy_ptr', hdist.get_dummy_ptr)
ll.add_symbol('allgather', hdist.allgather)
ll.add_symbol('oneD_reshape_shuffle', hdist.oneD_reshape_shuffle)
ll.add_symbol('permutation_int', hdist.permutation_int)
ll.add_symbol('permutation_array_index', hdist.permutation_array_index)
ll.add_symbol('c_get_rank', hdist.dist_get_rank)
ll.add_symbol('c_get_size', hdist.dist_get_size)
ll.add_symbol('c_barrier', hdist.barrier)
ll.add_symbol('c_alltoall', hdist.c_alltoall)
ll.add_symbol('c_gather_scalar', hdist.c_gather_scalar)
ll.add_symbol('c_gatherv', hdist.c_gatherv)
ll.add_symbol('c_scatterv', hdist.c_scatterv)
ll.add_symbol('c_allgatherv', hdist.c_allgatherv)
ll.add_symbol('c_bcast', hdist.c_bcast)
ll.add_symbol('c_recv', hdist.dist_recv)
ll.add_symbol('c_send', hdist.dist_send)
mpi_req_numba_type = getattr(types, 'int' + str(8 * hdist.mpi_req_num_bytes))
MPI_ROOT = 0
ANY_SOURCE = np.int32(hdist.ANY_SOURCE)


class Reduce_Type(Enum):
    Sum = 0
    Prod = 1
    Min = 2
    Max = 3
    Argmin = 4
    Argmax = 5
    Or = 6
    Concat = 7
    No_Op = 8


_get_rank = types.ExternalFunction('c_get_rank', types.int32())
_get_size = types.ExternalFunction('c_get_size', types.int32())
_barrier = types.ExternalFunction('c_barrier', types.int32())


@numba.njit
def get_rank():
    return _get_rank()


@numba.njit
def get_size():
    return _get_size()


@numba.njit
def barrier():
    _barrier()


_get_time = types.ExternalFunction('get_time', types.float64())
dist_time = types.ExternalFunction('dist_get_time', types.float64())


@overload(time.time, no_unliteral=True)
def overload_time_time():
    return lambda : _get_time()


@numba.generated_jit(nopython=True)
def get_type_enum(arr):
    arr = arr.instance_type if isinstance(arr, types.TypeRef) else arr
    dtype = arr.dtype
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):
        dtype = bodo.hiframes.pd_categorical_ext.get_categories_int_type(dtype)
    typ_val = numba_to_c_type(dtype)
    return lambda arr: np.int32(typ_val)


INT_MAX = np.iinfo(np.int32).max
_send = types.ExternalFunction('c_send', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def send(val, rank, tag):
    send_arr = np.full(1, val)
    lvkzc__tuhu = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, lvkzc__tuhu, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    lvkzc__tuhu = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, lvkzc__tuhu, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            lvkzc__tuhu = get_type_enum(arr)
            return _isend(arr.ctypes, size, lvkzc__tuhu, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        lvkzc__tuhu = np.int32(numba_to_c_type(arr.dtype))
        ttmx__puo = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            xefj__eva = size + 7 >> 3
            yyzd__kbni = _isend(arr._data.ctypes, size, lvkzc__tuhu, pe,
                tag, cond)
            pvs__uiwgz = _isend(arr._null_bitmap.ctypes, xefj__eva,
                ttmx__puo, pe, tag, cond)
            return yyzd__kbni, pvs__uiwgz
        return impl_nullable
    if is_str_arr_type(arr) or arr == binary_array_type:
        vlpw__wuzz = np.int32(numba_to_c_type(offset_type))
        ttmx__puo = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            arr = decode_if_dict_array(arr)
            cnx__wls = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(cnx__wls, pe, tag - 1)
            xefj__eva = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                vlpw__wuzz, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), cnx__wls,
                ttmx__puo, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr), xefj__eva,
                ttmx__puo, pe, tag)
            return None
        return impl_str_arr
    typ_enum = numba_to_c_type(types.uint8)

    def impl_voidptr(arr, size, pe, tag, cond=True):
        return _isend(arr, size, typ_enum, pe, tag, cond)
    return impl_voidptr


_irecv = types.ExternalFunction('dist_irecv', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def irecv(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            lvkzc__tuhu = get_type_enum(arr)
            return _irecv(arr.ctypes, size, lvkzc__tuhu, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        lvkzc__tuhu = np.int32(numba_to_c_type(arr.dtype))
        ttmx__puo = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            xefj__eva = size + 7 >> 3
            yyzd__kbni = _irecv(arr._data.ctypes, size, lvkzc__tuhu, pe,
                tag, cond)
            pvs__uiwgz = _irecv(arr._null_bitmap.ctypes, xefj__eva,
                ttmx__puo, pe, tag, cond)
            return yyzd__kbni, pvs__uiwgz
        return impl_nullable
    if arr in [binary_array_type, string_array_type]:
        vlpw__wuzz = np.int32(numba_to_c_type(offset_type))
        ttmx__puo = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            xgp__fghtc = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            xgp__fghtc = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        qes__ugu = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {xgp__fghtc}(size, n_chars)
            bodo.libs.str_arr_ext.move_str_binary_arr_payload(arr, new_arr)

            n_bytes = (size + 7) >> 3
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_offset_ptr(arr),
                size + 1,
                offset_typ_enum,
                pe,
                tag,
            )
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_data_ptr(arr), n_chars, char_typ_enum, pe, tag
            )
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr),
                n_bytes,
                char_typ_enum,
                pe,
                tag,
            )
            return None"""
        ntqz__kgsw = dict()
        exec(qes__ugu, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            vlpw__wuzz, 'char_typ_enum': ttmx__puo}, ntqz__kgsw)
        impl = ntqz__kgsw['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    lvkzc__tuhu = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), lvkzc__tuhu)


@numba.generated_jit(nopython=True)
def gather_scalar(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    data = types.unliteral(data)
    typ_val = numba_to_c_type(data)
    dtype = data

    def gather_scalar_impl(data, allgather=False, warn_if_rep=True, root=
        MPI_ROOT):
        n_pes = bodo.libs.distributed_api.get_size()
        rank = bodo.libs.distributed_api.get_rank()
        send = np.full(1, data, dtype)
        aumbs__tkx = n_pes if rank == root or allgather else 0
        xxis__ykbw = np.empty(aumbs__tkx, dtype)
        c_gather_scalar(send.ctypes, xxis__ykbw.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return xxis__ykbw
    return gather_scalar_impl


c_gather_scalar = types.ExternalFunction('c_gather_scalar', types.void(
    types.voidptr, types.voidptr, types.int32, types.bool_, types.int32))
c_gatherv = types.ExternalFunction('c_gatherv', types.void(types.voidptr,
    types.int32, types.voidptr, types.voidptr, types.voidptr, types.int32,
    types.bool_, types.int32))
c_scatterv = types.ExternalFunction('c_scatterv', types.void(types.voidptr,
    types.voidptr, types.voidptr, types.voidptr, types.int32, types.int32))


@intrinsic
def value_to_ptr(typingctx, val_tp=None):

    def codegen(context, builder, sig, args):
        fvr__mdey = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], fvr__mdey)
        return builder.bitcast(fvr__mdey, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        fvr__mdey = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(fvr__mdey)
    return val_tp(ptr_tp, val_tp), codegen


_dist_reduce = types.ExternalFunction('dist_reduce', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))
_dist_arr_reduce = types.ExternalFunction('dist_arr_reduce', types.void(
    types.voidptr, types.int64, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_reduce(value, reduce_op):
    if isinstance(value, types.Array):
        typ_enum = np.int32(numba_to_c_type(value.dtype))

        def impl_arr(value, reduce_op):
            A = np.ascontiguousarray(value)
            _dist_arr_reduce(A.ctypes, A.size, reduce_op, typ_enum)
            return A
        return impl_arr
    fqksq__wspd = types.unliteral(value)
    if isinstance(fqksq__wspd, IndexValueType):
        fqksq__wspd = fqksq__wspd.val_typ
        tns__qgznw = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            tns__qgznw.append(types.int64)
            tns__qgznw.append(bodo.datetime64ns)
            tns__qgznw.append(bodo.timedelta64ns)
            tns__qgznw.append(bodo.datetime_date_type)
            tns__qgznw.append(bodo.TimeType)
        if fqksq__wspd not in tns__qgznw:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(fqksq__wspd))
    typ_enum = np.int32(numba_to_c_type(fqksq__wspd))

    def impl(value, reduce_op):
        uqdc__igk = value_to_ptr(value)
        khc__fre = value_to_ptr(value)
        _dist_reduce(uqdc__igk, khc__fre, reduce_op, typ_enum)
        return load_val_ptr(khc__fre, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    fqksq__wspd = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(fqksq__wspd))
    zkl__hnlql = fqksq__wspd(0)

    def impl(value, reduce_op):
        uqdc__igk = value_to_ptr(value)
        khc__fre = value_to_ptr(zkl__hnlql)
        _dist_exscan(uqdc__igk, khc__fre, reduce_op, typ_enum)
        return load_val_ptr(khc__fre, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    vckw__ahg = 0
    sag__pfe = 0
    for i in range(len(recv_counts)):
        jsa__hns = recv_counts[i]
        xefj__eva = recv_counts_nulls[i]
        zfyri__yhn = tmp_null_bytes[vckw__ahg:vckw__ahg + xefj__eva]
        for fvaoz__kwn in range(jsa__hns):
            set_bit_to(null_bitmap_ptr, sag__pfe, get_bit(zfyri__yhn,
                fvaoz__kwn))
            sag__pfe += 1
        vckw__ahg += xefj__eva


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.gatherv()')
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            zslj__sby = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                zslj__sby, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            gtgf__ezm = data.size
            recv_counts = gather_scalar(np.int32(gtgf__ezm), allgather,
                root=root)
            jrb__hsww = recv_counts.sum()
            bas__fbjv = empty_like_type(jrb__hsww, data)
            miq__ksvl = np.empty(1, np.int32)
            if rank == root or allgather:
                miq__ksvl = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(gtgf__ezm), bas__fbjv.ctypes,
                recv_counts.ctypes, miq__ksvl.ctypes, np.int32(typ_val),
                allgather, np.int32(root))
            return bas__fbjv.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if is_str_arr_type(data):

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            data = decode_if_dict_array(data)
            bas__fbjv = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.str_arr_ext.init_str_arr(bas__fbjv)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            bas__fbjv = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(bas__fbjv)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        ttmx__puo = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            gtgf__ezm = len(data)
            xefj__eva = gtgf__ezm + 7 >> 3
            recv_counts = gather_scalar(np.int32(gtgf__ezm), allgather,
                root=root)
            jrb__hsww = recv_counts.sum()
            bas__fbjv = empty_like_type(jrb__hsww, data)
            miq__ksvl = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            ask__ossml = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                miq__ksvl = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                ask__ossml = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(gtgf__ezm),
                bas__fbjv._days_data.ctypes, recv_counts.ctypes, miq__ksvl.
                ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._seconds_data.ctypes, np.int32(gtgf__ezm),
                bas__fbjv._seconds_data.ctypes, recv_counts.ctypes,
                miq__ksvl.ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._microseconds_data.ctypes, np.int32(gtgf__ezm),
                bas__fbjv._microseconds_data.ctypes, recv_counts.ctypes,
                miq__ksvl.ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(xefj__eva),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, ask__ossml
                .ctypes, ttmx__puo, allgather, np.int32(root))
            copy_gathered_null_bytes(bas__fbjv._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return bas__fbjv
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        ttmx__puo = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            gtgf__ezm = len(data)
            xefj__eva = gtgf__ezm + 7 >> 3
            recv_counts = gather_scalar(np.int32(gtgf__ezm), allgather,
                root=root)
            jrb__hsww = recv_counts.sum()
            bas__fbjv = empty_like_type(jrb__hsww, data)
            miq__ksvl = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            ask__ossml = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                miq__ksvl = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                ask__ossml = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(gtgf__ezm), bas__fbjv.
                _data.ctypes, recv_counts.ctypes, miq__ksvl.ctypes, np.
                int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(xefj__eva),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, ask__ossml
                .ctypes, ttmx__puo, allgather, np.int32(root))
            copy_gathered_null_bytes(bas__fbjv._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return bas__fbjv
        return gatherv_impl_int_arr
    if isinstance(data, DatetimeArrayType):
        dbgx__tyjl = data.tz

        def impl_pd_datetime_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            mqk__amg = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(
                mqk__amg, dbgx__tyjl)
        return impl_pd_datetime_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            gysgd__ndedb = bodo.gatherv(data._left, allgather, warn_if_rep,
                root)
            spyod__qal = bodo.gatherv(data._right, allgather, warn_if_rep, root
                )
            return bodo.libs.interval_arr_ext.init_interval_array(gysgd__ndedb,
                spyod__qal)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            noc__duvl = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            mjnd__dfb = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                mjnd__dfb, noc__duvl)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        axlpt__pmr = np.iinfo(np.int64).max
        uez__skfwf = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            wjmv__xvfmf = data._start
            zrsxx__ycg = data._stop
            if len(data) == 0:
                wjmv__xvfmf = axlpt__pmr
                zrsxx__ycg = uez__skfwf
            wjmv__xvfmf = bodo.libs.distributed_api.dist_reduce(wjmv__xvfmf,
                np.int32(Reduce_Type.Min.value))
            zrsxx__ycg = bodo.libs.distributed_api.dist_reduce(zrsxx__ycg,
                np.int32(Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if wjmv__xvfmf == axlpt__pmr and zrsxx__ycg == uez__skfwf:
                wjmv__xvfmf = 0
                zrsxx__ycg = 0
            ojsof__izte = max(0, -(-(zrsxx__ycg - wjmv__xvfmf) // data._step))
            if ojsof__izte < total_len:
                zrsxx__ycg = wjmv__xvfmf + data._step * total_len
            if bodo.get_rank() != root and not allgather:
                wjmv__xvfmf = 0
                zrsxx__ycg = 0
            return bodo.hiframes.pd_index_ext.init_range_index(wjmv__xvfmf,
                zrsxx__ycg, data._step, data._name)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        from bodo.hiframes.pd_index_ext import PeriodIndexType
        if isinstance(data, PeriodIndexType):
            rsnkj__mmir = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, rsnkj__mmir)
        else:

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.utils.conversion.index_from_array(arr, data._name)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            bas__fbjv = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(bas__fbjv,
                data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.table.TableType):
        fewei__umvj = {'bodo': bodo, 'get_table_block': bodo.hiframes.table
            .get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like, 'init_table': bodo.hiframes.table.init_table}
        qes__ugu = (
            f'def impl_table(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):\n'
            )
        qes__ugu += '  T = data\n'
        qes__ugu += '  T2 = init_table(T, True)\n'
        for muu__efdv in data.type_to_blk.values():
            fewei__umvj[f'arr_inds_{muu__efdv}'] = np.array(data.
                block_to_arr_ind[muu__efdv], dtype=np.int64)
            qes__ugu += (
                f'  arr_list_{muu__efdv} = get_table_block(T, {muu__efdv})\n')
            qes__ugu += f"""  out_arr_list_{muu__efdv} = alloc_list_like(arr_list_{muu__efdv}, len(arr_list_{muu__efdv}), True)
"""
            qes__ugu += f'  for i in range(len(arr_list_{muu__efdv})):\n'
            qes__ugu += f'    arr_ind_{muu__efdv} = arr_inds_{muu__efdv}[i]\n'
            qes__ugu += f"""    ensure_column_unboxed(T, arr_list_{muu__efdv}, i, arr_ind_{muu__efdv})
"""
            qes__ugu += f"""    out_arr_{muu__efdv} = bodo.gatherv(arr_list_{muu__efdv}[i], allgather, warn_if_rep, root)
"""
            qes__ugu += (
                f'    out_arr_list_{muu__efdv}[i] = out_arr_{muu__efdv}\n')
            qes__ugu += (
                f'  T2 = set_table_block(T2, out_arr_list_{muu__efdv}, {muu__efdv})\n'
                )
        qes__ugu += (
            f'  length = T._len if bodo.get_rank() == root or allgather else 0\n'
            )
        qes__ugu += f'  T2 = set_table_len(T2, length)\n'
        qes__ugu += f'  return T2\n'
        ntqz__kgsw = {}
        exec(qes__ugu, fewei__umvj, ntqz__kgsw)
        ymiye__wurv = ntqz__kgsw['impl_table']
        return ymiye__wurv
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        paj__mpjjq = len(data.columns)
        if paj__mpjjq == 0:
            rva__utkk = ColNamesMetaType(())

            def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
                index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data
                    )
                acf__zvpa = bodo.gatherv(index, allgather, warn_if_rep, root)
                return bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                    acf__zvpa, rva__utkk)
            return impl
        jyfjl__enl = ', '.join(f'g_data_{i}' for i in range(paj__mpjjq))
        qes__ugu = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        if data.is_table_format:
            from bodo.transforms.distributed_analysis import Distribution
            ffjdp__ymmz = bodo.hiframes.pd_dataframe_ext.DataFrameType(data
                .data, data.index, data.columns, Distribution.REP, True)
            jyfjl__enl = 'T2'
            qes__ugu += (
                '  T = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            qes__ugu += (
                '  T2 = bodo.gatherv(T, allgather, warn_if_rep, root)\n')
        else:
            for i in range(paj__mpjjq):
                qes__ugu += (
                    """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                    .format(i, i))
                qes__ugu += (
                    '  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)\n'
                    .format(i, i))
        qes__ugu += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        qes__ugu += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        qes__ugu += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, __col_name_meta_value_gatherv_with_cols)
"""
            .format(jyfjl__enl))
        ntqz__kgsw = {}
        fewei__umvj = {'bodo': bodo,
            '__col_name_meta_value_gatherv_with_cols': ColNamesMetaType(
            data.columns)}
        exec(qes__ugu, fewei__umvj, ntqz__kgsw)
        lib__kmsfb = ntqz__kgsw['impl_df']
        return lib__kmsfb
    if isinstance(data, ArrayItemArrayType):
        ijs__gwpb = np.int32(numba_to_c_type(types.int32))
        ttmx__puo = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            rmll__iazh = bodo.libs.array_item_arr_ext.get_offsets(data)
            tmyab__ayai = bodo.libs.array_item_arr_ext.get_data(data)
            tmyab__ayai = tmyab__ayai[:rmll__iazh[-1]]
            gep__ekg = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            gtgf__ezm = len(data)
            mfy__iqs = np.empty(gtgf__ezm, np.uint32)
            xefj__eva = gtgf__ezm + 7 >> 3
            for i in range(gtgf__ezm):
                mfy__iqs[i] = rmll__iazh[i + 1] - rmll__iazh[i]
            recv_counts = gather_scalar(np.int32(gtgf__ezm), allgather,
                root=root)
            jrb__hsww = recv_counts.sum()
            miq__ksvl = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            ask__ossml = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                miq__ksvl = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for vev__yqr in range(len(recv_counts)):
                    recv_counts_nulls[vev__yqr] = recv_counts[vev__yqr
                        ] + 7 >> 3
                ask__ossml = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            srx__sxd = np.empty(jrb__hsww + 1, np.uint32)
            qcr__plvu = bodo.gatherv(tmyab__ayai, allgather, warn_if_rep, root)
            jaeku__zzzq = np.empty(jrb__hsww + 7 >> 3, np.uint8)
            c_gatherv(mfy__iqs.ctypes, np.int32(gtgf__ezm), srx__sxd.ctypes,
                recv_counts.ctypes, miq__ksvl.ctypes, ijs__gwpb, allgather,
                np.int32(root))
            c_gatherv(gep__ekg.ctypes, np.int32(xefj__eva), tmp_null_bytes.
                ctypes, recv_counts_nulls.ctypes, ask__ossml.ctypes,
                ttmx__puo, allgather, np.int32(root))
            dummy_use(data)
            lfs__lzzoe = np.empty(jrb__hsww + 1, np.uint64)
            convert_len_arr_to_offset(srx__sxd.ctypes, lfs__lzzoe.ctypes,
                jrb__hsww)
            copy_gathered_null_bytes(jaeku__zzzq.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                jrb__hsww, qcr__plvu, lfs__lzzoe, jaeku__zzzq)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        lcp__lilij = data.names
        ttmx__puo = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            roa__kjm = bodo.libs.struct_arr_ext.get_data(data)
            tjrvu__zxiv = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            sxi__wrtwd = bodo.gatherv(roa__kjm, allgather=allgather, root=root)
            rank = bodo.libs.distributed_api.get_rank()
            gtgf__ezm = len(data)
            xefj__eva = gtgf__ezm + 7 >> 3
            recv_counts = gather_scalar(np.int32(gtgf__ezm), allgather,
                root=root)
            jrb__hsww = recv_counts.sum()
            djo__wgxi = np.empty(jrb__hsww + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            ask__ossml = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                ask__ossml = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(tjrvu__zxiv.ctypes, np.int32(xefj__eva),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, ask__ossml
                .ctypes, ttmx__puo, allgather, np.int32(root))
            copy_gathered_null_bytes(djo__wgxi.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(sxi__wrtwd,
                djo__wgxi, lcp__lilij)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            bas__fbjv = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(bas__fbjv)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            bas__fbjv = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.tuple_arr_ext.init_tuple_arr(bas__fbjv)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            bas__fbjv = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.map_arr_ext.init_map_arr(bas__fbjv)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            bas__fbjv = bodo.gatherv(data.data, allgather, warn_if_rep, root)
            vrxbi__shq = bodo.gatherv(data.indices, allgather, warn_if_rep,
                root)
            mtw__kmw = bodo.gatherv(data.indptr, allgather, warn_if_rep, root)
            vzlbk__cqneu = gather_scalar(data.shape[0], allgather, root=root)
            cty__nias = vzlbk__cqneu.sum()
            paj__mpjjq = bodo.libs.distributed_api.dist_reduce(data.shape[1
                ], np.int32(Reduce_Type.Max.value))
            auaxi__ekmzo = np.empty(cty__nias + 1, np.int64)
            vrxbi__shq = vrxbi__shq.astype(np.int64)
            auaxi__ekmzo[0] = 0
            goe__ezc = 1
            tzqc__nbo = 0
            for lsqdz__xcgl in vzlbk__cqneu:
                for ygiki__bel in range(lsqdz__xcgl):
                    xkx__vtbs = mtw__kmw[tzqc__nbo + 1] - mtw__kmw[tzqc__nbo]
                    auaxi__ekmzo[goe__ezc] = auaxi__ekmzo[goe__ezc - 1
                        ] + xkx__vtbs
                    goe__ezc += 1
                    tzqc__nbo += 1
                tzqc__nbo += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(bas__fbjv,
                vrxbi__shq, auaxi__ekmzo, (cty__nias, paj__mpjjq))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        qes__ugu = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        qes__ugu += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        ntqz__kgsw = {}
        exec(qes__ugu, {'bodo': bodo}, ntqz__kgsw)
        nla__grbxw = ntqz__kgsw['impl_tuple']
        return nla__grbxw
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    try:
        import bodosql
        from bodosql.context_ext import BodoSQLContextType
    except ImportError as ysq__khekn:
        BodoSQLContextType = None
    if BodoSQLContextType is not None and isinstance(data, BodoSQLContextType):
        qes__ugu = f"""def impl_bodosql_context(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):
"""
        sgp__xehbh = ', '.join([f"'{noc__duvl}'" for noc__duvl in data.names])
        wzpk__wknh = ', '.join([
            f'bodo.gatherv(data.dataframes[{i}], allgather, warn_if_rep, root)'
             for i in range(len(data.dataframes))])
        qes__ugu += f"""  return bodosql.context_ext.init_sql_context(({sgp__xehbh}, ), ({wzpk__wknh}, ), data.catalog)
"""
        ntqz__kgsw = {}
        exec(qes__ugu, {'bodo': bodo, 'bodosql': bodosql}, ntqz__kgsw)
        cgjn__riov = ntqz__kgsw['impl_bodosql_context']
        return cgjn__riov
    try:
        import bodosql
        from bodosql import TablePathType
    except ImportError as ysq__khekn:
        TablePathType = None
    if TablePathType is not None and isinstance(data, TablePathType):
        qes__ugu = f"""def impl_table_path(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):
"""
        qes__ugu += f'  return data\n'
        ntqz__kgsw = {}
        exec(qes__ugu, {}, ntqz__kgsw)
        tsiax__mrzw = ntqz__kgsw['impl_table_path']
        return tsiax__mrzw
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.rebalance()')
    qes__ugu = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    qes__ugu += '    if random:\n'
    qes__ugu += '        if random_seed is None:\n'
    qes__ugu += '            random = 1\n'
    qes__ugu += '        else:\n'
    qes__ugu += '            random = 2\n'
    qes__ugu += '    if random_seed is None:\n'
    qes__ugu += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        efqv__twa = data
        paj__mpjjq = len(efqv__twa.columns)
        for i in range(paj__mpjjq):
            qes__ugu += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        qes__ugu += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        jyfjl__enl = ', '.join(f'data_{i}' for i in range(paj__mpjjq))
        qes__ugu += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(ynok__hbia) for
            ynok__hbia in range(paj__mpjjq))))
        qes__ugu += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        qes__ugu += '    if dests is None:\n'
        qes__ugu += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        qes__ugu += '    else:\n'
        qes__ugu += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for rywcs__xll in range(paj__mpjjq):
            qes__ugu += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(rywcs__xll))
        qes__ugu += (
            '    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
            .format(paj__mpjjq))
        qes__ugu += '    delete_table(out_table)\n'
        qes__ugu += '    if parallel:\n'
        qes__ugu += '        delete_table(table_total)\n'
        jyfjl__enl = ', '.join('out_arr_{}'.format(i) for i in range(
            paj__mpjjq))
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        qes__ugu += (
            """    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, __col_name_meta_value_rebalance)
"""
            .format(jyfjl__enl, index))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        qes__ugu += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        qes__ugu += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        qes__ugu += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        qes__ugu += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        qes__ugu += '    if dests is None:\n'
        qes__ugu += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        qes__ugu += '    else:\n'
        qes__ugu += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        qes__ugu += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        qes__ugu += (
            '    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)\n'
            )
        qes__ugu += '    delete_table(out_table)\n'
        qes__ugu += '    if parallel:\n'
        qes__ugu += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        qes__ugu += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        qes__ugu += '    if not parallel:\n'
        qes__ugu += '        return data\n'
        qes__ugu += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        qes__ugu += '    if dests is None:\n'
        qes__ugu += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        qes__ugu += '    elif bodo.get_rank() not in dests:\n'
        qes__ugu += '        dim0_local_size = 0\n'
        qes__ugu += '    else:\n'
        qes__ugu += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        qes__ugu += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        qes__ugu += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        qes__ugu += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        qes__ugu += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        qes__ugu += '    if dests is None:\n'
        qes__ugu += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        qes__ugu += '    else:\n'
        qes__ugu += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        qes__ugu += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        qes__ugu += '    delete_table(out_table)\n'
        qes__ugu += '    if parallel:\n'
        qes__ugu += '        delete_table(table_total)\n'
        qes__ugu += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    ntqz__kgsw = {}
    fewei__umvj = {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.array
        .array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table}
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        fewei__umvj.update({'__col_name_meta_value_rebalance':
            ColNamesMetaType(efqv__twa.columns)})
    exec(qes__ugu, fewei__umvj, ntqz__kgsw)
    impl = ntqz__kgsw['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, n_samples=None, parallel=False
    ):
    qes__ugu = (
        'def impl(data, seed=None, dests=None, n_samples=None, parallel=False):\n'
        )
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        qes__ugu += '    if seed is None:\n'
        qes__ugu += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        qes__ugu += '    np.random.seed(seed)\n'
        qes__ugu += '    if not parallel:\n'
        qes__ugu += '        data = data.copy()\n'
        qes__ugu += '        np.random.shuffle(data)\n'
        if not is_overload_none(n_samples):
            qes__ugu += '        data = data[:n_samples]\n'
        qes__ugu += '        return data\n'
        qes__ugu += '    else:\n'
        qes__ugu += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        qes__ugu += '        permutation = np.arange(dim0_global_size)\n'
        qes__ugu += '        np.random.shuffle(permutation)\n'
        if not is_overload_none(n_samples):
            qes__ugu += (
                '        n_samples = max(0, min(dim0_global_size, n_samples))\n'
                )
        else:
            qes__ugu += '        n_samples = dim0_global_size\n'
        qes__ugu += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        qes__ugu += """        dim0_output_size = bodo.libs.distributed_api.get_node_portion(n_samples, bodo.get_size(), bodo.get_rank())
"""
        qes__ugu += """        output = np.empty((dim0_output_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        qes__ugu += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        qes__ugu += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation), n_samples)
"""
        qes__ugu += '        return output\n'
    else:
        qes__ugu += """    output = bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
        if not is_overload_none(n_samples):
            qes__ugu += """    local_n_samples = bodo.libs.distributed_api.get_node_portion(n_samples, bodo.get_size(), bodo.get_rank())
"""
            qes__ugu += '    output = output[:local_n_samples]\n'
        qes__ugu += '    return output\n'
    ntqz__kgsw = {}
    exec(qes__ugu, {'np': np, 'bodo': bodo}, ntqz__kgsw)
    impl = ntqz__kgsw['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    pfvd__ncg = np.empty(sendcounts_nulls.sum(), np.uint8)
    vckw__ahg = 0
    sag__pfe = 0
    for mcd__vmg in range(len(sendcounts)):
        jsa__hns = sendcounts[mcd__vmg]
        xefj__eva = sendcounts_nulls[mcd__vmg]
        zfyri__yhn = pfvd__ncg[vckw__ahg:vckw__ahg + xefj__eva]
        for fvaoz__kwn in range(jsa__hns):
            set_bit_to_arr(zfyri__yhn, fvaoz__kwn, get_bit_bitmap(
                null_bitmap_ptr, sag__pfe))
            sag__pfe += 1
        vckw__ahg += xefj__eva
    return pfvd__ncg


def _bcast_dtype(data, root=MPI_ROOT):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    ydw__edck = MPI.COMM_WORLD
    data = ydw__edck.bcast(data, root)
    return data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_scatterv_send_counts(send_counts, n_pes, n):
    if not is_overload_none(send_counts):
        return lambda send_counts, n_pes, n: send_counts

    def impl(send_counts, n_pes, n):
        send_counts = np.empty(n_pes, np.int32)
        for i in range(n_pes):
            send_counts[i] = get_node_portion(n, n_pes, i)
        return send_counts
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _scatterv_np(data, send_counts=None, warn_if_dist=True):
    typ_val = numba_to_c_type(data.dtype)
    grk__udn = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    zve__akbab = (0,) * grk__udn

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        kess__mvo = np.ascontiguousarray(data)
        cye__bfxq = data.ctypes
        ejwh__ygvf = zve__akbab
        if rank == MPI_ROOT:
            ejwh__ygvf = kess__mvo.shape
        ejwh__ygvf = bcast_tuple(ejwh__ygvf)
        aeysv__tigh = get_tuple_prod(ejwh__ygvf[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes,
            ejwh__ygvf[0])
        send_counts *= aeysv__tigh
        gtgf__ezm = send_counts[rank]
        cat__vnzx = np.empty(gtgf__ezm, dtype)
        miq__ksvl = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(cye__bfxq, send_counts.ctypes, miq__ksvl.ctypes,
            cat__vnzx.ctypes, np.int32(gtgf__ezm), np.int32(typ_val))
        return cat__vnzx.reshape((-1,) + ejwh__ygvf[1:])
    return scatterv_arr_impl


def _get_name_value_for_type(name_typ):
    assert isinstance(name_typ, (types.UnicodeType, types.StringLiteral)
        ) or name_typ == types.none
    return None if name_typ == types.none else '_' + str(ir_utils.next_label())


def get_value_for_type(dtype):
    if isinstance(dtype, types.Array):
        return np.zeros((1,) * dtype.ndim, numba.np.numpy_support.as_dtype(
            dtype.dtype))
    if dtype == string_array_type:
        return pd.array(['A'], 'string')
    if dtype == bodo.dict_str_arr_type:
        import pyarrow as pa
        return pa.array(['a'], type=pa.dictionary(pa.int32(), pa.string()))
    if dtype == binary_array_type:
        return np.array([b'A'], dtype=object)
    if isinstance(dtype, IntegerArrayType):
        fow__jseym = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], fow__jseym)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        noc__duvl = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=noc__duvl)
        sodnx__rmgm = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(sodnx__rmgm)
        return pd.Index(arr, name=noc__duvl)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        import pyarrow as pa
        noc__duvl = _get_name_value_for_type(dtype.name_typ)
        lcp__lilij = tuple(_get_name_value_for_type(t) for t in dtype.names_typ
            )
        qokp__hxbmz = tuple(get_value_for_type(t) for t in dtype.array_types)
        qokp__hxbmz = tuple(a.to_numpy(False) if isinstance(a, pa.Array) else
            a for a in qokp__hxbmz)
        val = pd.MultiIndex.from_arrays(qokp__hxbmz, names=lcp__lilij)
        val.name = noc__duvl
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        noc__duvl = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=noc__duvl)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        qokp__hxbmz = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({noc__duvl: arr for noc__duvl, arr in zip(dtype
            .columns, qokp__hxbmz)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    if isinstance(dtype, IntervalArrayType):
        sodnx__rmgm = get_value_for_type(dtype.arr_type)
        return pd.arrays.IntervalArray([pd.Interval(sodnx__rmgm[0],
            sodnx__rmgm[0])])
    raise BodoError(f'get_value_for_type(dtype): Missing data type {dtype}')


def scatterv(data, send_counts=None, warn_if_dist=True):
    rank = bodo.libs.distributed_api.get_rank()
    if rank != MPI_ROOT and data is not None:
        warnings.warn(BodoWarning(
            "bodo.scatterv(): A non-None value for 'data' was found on a rank other than the root. This data won't be sent to any other ranks and will be overwritten with data from rank 0."
            ))
    dtype = bodo.typeof(data)
    dtype = _bcast_dtype(dtype)
    if rank != MPI_ROOT:
        data = get_value_for_type(dtype)
    return scatterv_impl(data, send_counts)


@overload(scatterv)
def scatterv_overload(data, send_counts=None, warn_if_dist=True):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.scatterv()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.scatterv()')
    return lambda data, send_counts=None, warn_if_dist=True: scatterv_impl(data
        , send_counts)


@numba.generated_jit(nopython=True)
def scatterv_impl(data, send_counts=None, warn_if_dist=True):
    if isinstance(data, types.Array):
        return lambda data, send_counts=None, warn_if_dist=True: _scatterv_np(
            data, send_counts)
    if data in (string_array_type, binary_array_type):
        ijs__gwpb = np.int32(numba_to_c_type(types.int32))
        ttmx__puo = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            xgp__fghtc = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            xgp__fghtc = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        qes__ugu = f"""def impl(
            data, send_counts=None, warn_if_dist=True
        ):  # pragma: no cover
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            n_all = bodo.libs.distributed_api.bcast_scalar(len(data))

            # convert offsets to lengths of strings
            send_arr_lens = np.empty(
                len(data), np.uint32
            )  # XXX offset type is offset_type, lengths for comm are uint32
            for i in range(len(data)):
                send_arr_lens[i] = bodo.libs.str_arr_ext.get_str_arr_item_length(
                    data, i
                )

            # ------- calculate buffer counts -------

            send_counts = bodo.libs.distributed_api._get_scatterv_send_counts(send_counts, n_pes, n_all)

            # displacements
            displs = bodo.ir.join.calc_disp(send_counts)

            # compute send counts for characters
            send_counts_char = np.empty(n_pes, np.int32)
            if rank == 0:
                curr_str = 0
                for i in range(n_pes):
                    c = 0
                    for _ in range(send_counts[i]):
                        c += send_arr_lens[curr_str]
                        curr_str += 1
                    send_counts_char[i] = c

            bodo.libs.distributed_api.bcast(send_counts_char)

            # displacements for characters
            displs_char = bodo.ir.join.calc_disp(send_counts_char)

            # compute send counts for nulls
            send_counts_nulls = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                send_counts_nulls[i] = (send_counts[i] + 7) >> 3

            # displacements for nulls
            displs_nulls = bodo.ir.join.calc_disp(send_counts_nulls)

            # alloc output array
            n_loc = send_counts[rank]  # total number of elements on this PE
            n_loc_char = send_counts_char[rank]
            recv_arr = {xgp__fghtc}(n_loc, n_loc_char)

            # ----- string lengths -----------

            recv_lens = np.empty(n_loc, np.uint32)
            bodo.libs.distributed_api.c_scatterv(
                send_arr_lens.ctypes,
                send_counts.ctypes,
                displs.ctypes,
                recv_lens.ctypes,
                np.int32(n_loc),
                int32_typ_enum,
            )

            # TODO: don't hardcode offset type. Also, if offset is 32 bit we can
            # use the same buffer
            bodo.libs.str_arr_ext.convert_len_arr_to_offset(recv_lens.ctypes, bodo.libs.str_arr_ext.get_offset_ptr(recv_arr), n_loc)

            # ----- string characters -----------

            bodo.libs.distributed_api.c_scatterv(
                bodo.libs.str_arr_ext.get_data_ptr(data),
                send_counts_char.ctypes,
                displs_char.ctypes,
                bodo.libs.str_arr_ext.get_data_ptr(recv_arr),
                np.int32(n_loc_char),
                char_typ_enum,
            )

            # ----------- null bitmap -------------

            n_recv_bytes = (n_loc + 7) >> 3

            send_null_bitmap = bodo.libs.distributed_api.get_scatter_null_bytes_buff(
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(data), send_counts, send_counts_nulls
            )

            bodo.libs.distributed_api.c_scatterv(
                send_null_bitmap.ctypes,
                send_counts_nulls.ctypes,
                displs_nulls.ctypes,
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(recv_arr),
                np.int32(n_recv_bytes),
                char_typ_enum,
            )

            return recv_arr"""
        ntqz__kgsw = dict()
        exec(qes__ugu, {'bodo': bodo, 'np': np, 'int32_typ_enum': ijs__gwpb,
            'char_typ_enum': ttmx__puo, 'decode_if_dict_array':
            decode_if_dict_array}, ntqz__kgsw)
        impl = ntqz__kgsw['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        ijs__gwpb = np.int32(numba_to_c_type(types.int32))
        ttmx__puo = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            mthpd__mbfy = bodo.libs.array_item_arr_ext.get_offsets(data)
            hvfa__dmns = bodo.libs.array_item_arr_ext.get_data(data)
            hvfa__dmns = hvfa__dmns[:mthpd__mbfy[-1]]
            tsf__nwt = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            ewgwj__cwpb = bcast_scalar(len(data))
            ecbmw__bsw = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                ecbmw__bsw[i] = mthpd__mbfy[i + 1] - mthpd__mbfy[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                ewgwj__cwpb)
            miq__ksvl = bodo.ir.join.calc_disp(send_counts)
            qhg__jjx = np.empty(n_pes, np.int32)
            if rank == 0:
                htf__tbzr = 0
                for i in range(n_pes):
                    gpmuo__mrb = 0
                    for ygiki__bel in range(send_counts[i]):
                        gpmuo__mrb += ecbmw__bsw[htf__tbzr]
                        htf__tbzr += 1
                    qhg__jjx[i] = gpmuo__mrb
            bcast(qhg__jjx)
            rfkn__wpapa = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                rfkn__wpapa[i] = send_counts[i] + 7 >> 3
            ask__ossml = bodo.ir.join.calc_disp(rfkn__wpapa)
            gtgf__ezm = send_counts[rank]
            tukna__aqg = np.empty(gtgf__ezm + 1, np_offset_type)
            gdw__bivj = bodo.libs.distributed_api.scatterv_impl(hvfa__dmns,
                qhg__jjx)
            njyqe__rbi = gtgf__ezm + 7 >> 3
            zrbt__krj = np.empty(njyqe__rbi, np.uint8)
            isbb__lvg = np.empty(gtgf__ezm, np.uint32)
            c_scatterv(ecbmw__bsw.ctypes, send_counts.ctypes, miq__ksvl.
                ctypes, isbb__lvg.ctypes, np.int32(gtgf__ezm), ijs__gwpb)
            convert_len_arr_to_offset(isbb__lvg.ctypes, tukna__aqg.ctypes,
                gtgf__ezm)
            mzj__fqh = get_scatter_null_bytes_buff(tsf__nwt.ctypes,
                send_counts, rfkn__wpapa)
            c_scatterv(mzj__fqh.ctypes, rfkn__wpapa.ctypes, ask__ossml.
                ctypes, zrbt__krj.ctypes, np.int32(njyqe__rbi), ttmx__puo)
            return bodo.libs.array_item_arr_ext.init_array_item_array(gtgf__ezm
                , gdw__bivj, tukna__aqg, zrbt__krj)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        ttmx__puo = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            xly__csrg = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            xly__csrg = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            xly__csrg = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            xly__csrg = (bodo.hiframes.datetime_date_ext.
                init_datetime_date_array)

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            kess__mvo = data._data
            tjrvu__zxiv = data._null_bitmap
            uygdn__yowdk = len(kess__mvo)
            qfzig__mjzwq = _scatterv_np(kess__mvo, send_counts)
            ewgwj__cwpb = bcast_scalar(uygdn__yowdk)
            lxe__wuch = len(qfzig__mjzwq) + 7 >> 3
            znblj__uwpz = np.empty(lxe__wuch, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                ewgwj__cwpb)
            rfkn__wpapa = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                rfkn__wpapa[i] = send_counts[i] + 7 >> 3
            ask__ossml = bodo.ir.join.calc_disp(rfkn__wpapa)
            mzj__fqh = get_scatter_null_bytes_buff(tjrvu__zxiv.ctypes,
                send_counts, rfkn__wpapa)
            c_scatterv(mzj__fqh.ctypes, rfkn__wpapa.ctypes, ask__ossml.
                ctypes, znblj__uwpz.ctypes, np.int32(lxe__wuch), ttmx__puo)
            return xly__csrg(qfzig__mjzwq, znblj__uwpz)
        return scatterv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, send_counts=None, warn_if_dist=True):
            dvpg__xvl = bodo.libs.distributed_api.scatterv_impl(data._left,
                send_counts)
            itl__tomp = bodo.libs.distributed_api.scatterv_impl(data._right,
                send_counts)
            return bodo.libs.interval_arr_ext.init_interval_array(dvpg__xvl,
                itl__tomp)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            wjmv__xvfmf = data._start
            zrsxx__ycg = data._stop
            swzzu__bfwuc = data._step
            noc__duvl = data._name
            noc__duvl = bcast_scalar(noc__duvl)
            wjmv__xvfmf = bcast_scalar(wjmv__xvfmf)
            zrsxx__ycg = bcast_scalar(zrsxx__ycg)
            swzzu__bfwuc = bcast_scalar(swzzu__bfwuc)
            jetu__qsyj = bodo.libs.array_kernels.calc_nitems(wjmv__xvfmf,
                zrsxx__ycg, swzzu__bfwuc)
            chunk_start = bodo.libs.distributed_api.get_start(jetu__qsyj,
                n_pes, rank)
            goj__cguwg = bodo.libs.distributed_api.get_node_portion(jetu__qsyj,
                n_pes, rank)
            nnk__biou = wjmv__xvfmf + swzzu__bfwuc * chunk_start
            vfe__uswv = wjmv__xvfmf + swzzu__bfwuc * (chunk_start + goj__cguwg)
            vfe__uswv = min(vfe__uswv, zrsxx__ycg)
            return bodo.hiframes.pd_index_ext.init_range_index(nnk__biou,
                vfe__uswv, swzzu__bfwuc, noc__duvl)
        return impl_range_index
    if isinstance(data, bodo.hiframes.pd_index_ext.PeriodIndexType):
        rsnkj__mmir = data.freq

        def impl_period_index(data, send_counts=None, warn_if_dist=True):
            kess__mvo = data._data
            noc__duvl = data._name
            noc__duvl = bcast_scalar(noc__duvl)
            arr = bodo.libs.distributed_api.scatterv_impl(kess__mvo,
                send_counts)
            return bodo.hiframes.pd_index_ext.init_period_index(arr,
                noc__duvl, rsnkj__mmir)
        return impl_period_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            kess__mvo = data._data
            noc__duvl = data._name
            noc__duvl = bcast_scalar(noc__duvl)
            arr = bodo.libs.distributed_api.scatterv_impl(kess__mvo,
                send_counts)
            return bodo.utils.conversion.index_from_array(arr, noc__duvl)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            bas__fbjv = bodo.libs.distributed_api.scatterv_impl(data._data,
                send_counts)
            noc__duvl = bcast_scalar(data._name)
            lcp__lilij = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(bas__fbjv,
                lcp__lilij, noc__duvl)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            noc__duvl = bodo.hiframes.pd_series_ext.get_series_name(data)
            mqbgf__mac = bcast_scalar(noc__duvl)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            mjnd__dfb = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                mjnd__dfb, mqbgf__mac)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        paj__mpjjq = len(data.columns)
        guz__zhpu = ColNamesMetaType(data.columns)
        qes__ugu = 'def impl_df(data, send_counts=None, warn_if_dist=True):\n'
        if data.is_table_format:
            qes__ugu += (
                '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            qes__ugu += (
                '  g_table = bodo.libs.distributed_api.scatterv_impl(table, send_counts)\n'
                )
            jyfjl__enl = 'g_table'
        else:
            for i in range(paj__mpjjq):
                qes__ugu += f"""  data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
                qes__ugu += f"""  g_data_{i} = bodo.libs.distributed_api.scatterv_impl(data_{i}, send_counts)
"""
            jyfjl__enl = ', '.join(f'g_data_{i}' for i in range(paj__mpjjq))
        qes__ugu += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        qes__ugu += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        qes__ugu += f"""  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({jyfjl__enl},), g_index, __col_name_meta_scaterv_impl)
"""
        ntqz__kgsw = {}
        exec(qes__ugu, {'bodo': bodo, '__col_name_meta_scaterv_impl':
            guz__zhpu}, ntqz__kgsw)
        lib__kmsfb = ntqz__kgsw['impl_df']
        return lib__kmsfb
    if isinstance(data, bodo.TableType):
        qes__ugu = (
            'def impl_table(data, send_counts=None, warn_if_dist=True):\n')
        qes__ugu += '  T = data\n'
        qes__ugu += '  T2 = init_table(T, False)\n'
        qes__ugu += '  l = 0\n'
        fewei__umvj = {}
        for muu__efdv in data.type_to_blk.values():
            fewei__umvj[f'arr_inds_{muu__efdv}'] = np.array(data.
                block_to_arr_ind[muu__efdv], dtype=np.int64)
            qes__ugu += (
                f'  arr_list_{muu__efdv} = get_table_block(T, {muu__efdv})\n')
            qes__ugu += f"""  out_arr_list_{muu__efdv} = alloc_list_like(arr_list_{muu__efdv}, len(arr_list_{muu__efdv}), False)
"""
            qes__ugu += f'  for i in range(len(arr_list_{muu__efdv})):\n'
            qes__ugu += f'    arr_ind_{muu__efdv} = arr_inds_{muu__efdv}[i]\n'
            qes__ugu += f"""    ensure_column_unboxed(T, arr_list_{muu__efdv}, i, arr_ind_{muu__efdv})
"""
            qes__ugu += f"""    out_arr_{muu__efdv} = bodo.libs.distributed_api.scatterv_impl(arr_list_{muu__efdv}[i], send_counts)
"""
            qes__ugu += (
                f'    out_arr_list_{muu__efdv}[i] = out_arr_{muu__efdv}\n')
            qes__ugu += f'    l = len(out_arr_{muu__efdv})\n'
            qes__ugu += (
                f'  T2 = set_table_block(T2, out_arr_list_{muu__efdv}, {muu__efdv})\n'
                )
        qes__ugu += f'  T2 = set_table_len(T2, l)\n'
        qes__ugu += f'  return T2\n'
        fewei__umvj.update({'bodo': bodo, 'init_table': bodo.hiframes.table
            .init_table, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like})
        ntqz__kgsw = {}
        exec(qes__ugu, fewei__umvj, ntqz__kgsw)
        return ntqz__kgsw['impl_table']
    if data == bodo.dict_str_arr_type:

        def impl_dict_arr(data, send_counts=None, warn_if_dist=True):
            if bodo.get_rank() == 0:
                thv__fzr = data._data
                bodo.libs.distributed_api.bcast_scalar(len(thv__fzr))
                bodo.libs.distributed_api.bcast_scalar(np.int64(bodo.libs.
                    str_arr_ext.num_total_chars(thv__fzr)))
            else:
                ojsof__izte = bodo.libs.distributed_api.bcast_scalar(0)
                cnx__wls = bodo.libs.distributed_api.bcast_scalar(0)
                thv__fzr = bodo.libs.str_arr_ext.pre_alloc_string_array(
                    ojsof__izte, cnx__wls)
            bodo.libs.distributed_api.bcast(thv__fzr)
            ljxvm__brut = bodo.libs.distributed_api.scatterv_impl(data.
                _indices, send_counts)
            return bodo.libs.dict_arr_ext.init_dict_arr(thv__fzr,
                ljxvm__brut, True)
        return impl_dict_arr
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            zslj__sby = bodo.libs.distributed_api.scatterv_impl(data.codes,
                send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                zslj__sby, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        qes__ugu = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        qes__ugu += '  return ({}{})\n'.format(', '.join(
            f'bodo.libs.distributed_api.scatterv_impl(data[{i}], send_counts)'
             for i in range(len(data))), ',' if len(data) > 0 else '')
        ntqz__kgsw = {}
        exec(qes__ugu, {'bodo': bodo}, ntqz__kgsw)
        nla__grbxw = ntqz__kgsw['impl_tuple']
        return nla__grbxw
    if data is types.none:
        return lambda data, send_counts=None, warn_if_dist=True: None
    raise BodoError('scatterv() not available for {}'.format(data))


@intrinsic
def cptr_to_voidptr(typingctx, cptr_tp=None):

    def codegen(context, builder, sig, args):
        return builder.bitcast(args[0], lir.IntType(8).as_pointer())
    return types.voidptr(cptr_tp), codegen


def bcast(data, root=MPI_ROOT):
    return


@overload(bcast, no_unliteral=True)
def bcast_overload(data, root=MPI_ROOT):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.bcast()')
    if isinstance(data, types.Array):

        def bcast_impl(data, root=MPI_ROOT):
            typ_enum = get_type_enum(data)
            count = data.size
            assert count < INT_MAX
            c_bcast(data.ctypes, np.int32(count), typ_enum, np.array([-1]).
                ctypes, 0, np.int32(root))
            return
        return bcast_impl
    if isinstance(data, DecimalArrayType):

        def bcast_decimal_arr(data, root=MPI_ROOT):
            count = data._data.size
            assert count < INT_MAX
            c_bcast(data._data.ctypes, np.int32(count), CTypeEnum.Int128.
                value, np.array([-1]).ctypes, 0, np.int32(root))
            bcast(data._null_bitmap, root)
            return
        return bcast_decimal_arr
    if isinstance(data, IntegerArrayType) or data in (boolean_array,
        datetime_date_array_type):

        def bcast_impl_int_arr(data, root=MPI_ROOT):
            bcast(data._data, root)
            bcast(data._null_bitmap, root)
            return
        return bcast_impl_int_arr
    if is_str_arr_type(data) or data == binary_array_type:
        vlpw__wuzz = np.int32(numba_to_c_type(offset_type))
        ttmx__puo = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data, root=MPI_ROOT):
            data = decode_if_dict_array(data)
            gtgf__ezm = len(data)
            ihphv__czf = num_total_chars(data)
            assert gtgf__ezm < INT_MAX
            assert ihphv__czf < INT_MAX
            okqy__eky = get_offset_ptr(data)
            cye__bfxq = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            xefj__eva = gtgf__ezm + 7 >> 3
            c_bcast(okqy__eky, np.int32(gtgf__ezm + 1), vlpw__wuzz, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(cye__bfxq, np.int32(ihphv__czf), ttmx__puo, np.array([-
                1]).ctypes, 0, np.int32(root))
            c_bcast(null_bitmap_ptr, np.int32(xefj__eva), ttmx__puo, np.
                array([-1]).ctypes, 0, np.int32(root))
        return bcast_str_impl


c_bcast = types.ExternalFunction('c_bcast', types.void(types.voidptr, types
    .int32, types.int32, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def bcast_scalar(val, root=MPI_ROOT):
    val = types.unliteral(val)
    if not (isinstance(val, (types.Integer, types.Float)) or val in [bodo.
        datetime64ns, bodo.timedelta64ns, bodo.string_type, types.none,
        types.bool_]):
        raise BodoError(
            f'bcast_scalar requires an argument of type Integer, Float, datetime64ns, timedelta64ns, string, None, or Bool. Found type {val}'
            )
    if val == types.none:
        return lambda val, root=MPI_ROOT: None
    if val == bodo.string_type:
        ttmx__puo = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != root:
                kvzq__cdp = 0
                rqc__gll = np.empty(0, np.uint8).ctypes
            else:
                rqc__gll, kvzq__cdp = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            kvzq__cdp = bodo.libs.distributed_api.bcast_scalar(kvzq__cdp, root)
            if rank != root:
                mbuvb__aoccd = np.empty(kvzq__cdp + 1, np.uint8)
                mbuvb__aoccd[kvzq__cdp] = 0
                rqc__gll = mbuvb__aoccd.ctypes
            c_bcast(rqc__gll, np.int32(kvzq__cdp), ttmx__puo, np.array([-1]
                ).ctypes, 0, np.int32(root))
            return bodo.libs.str_arr_ext.decode_utf8(rqc__gll, kvzq__cdp)
        return impl_str
    typ_val = numba_to_c_type(val)
    qes__ugu = f"""def bcast_scalar_impl(val, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({typ_val}), np.array([-1]).ctypes, 0, np.int32(root))
  return send[0]
"""
    dtype = numba.np.numpy_support.as_dtype(val)
    ntqz__kgsw = {}
    exec(qes__ugu, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, ntqz__kgsw)
    mqu__cvlvn = ntqz__kgsw['bcast_scalar_impl']
    return mqu__cvlvn


@numba.generated_jit(nopython=True)
def bcast_tuple(val, root=MPI_ROOT):
    assert isinstance(val, types.BaseTuple)
    ucmc__qsssh = len(val)
    qes__ugu = f'def bcast_tuple_impl(val, root={MPI_ROOT}):\n'
    qes__ugu += '  return ({}{})'.format(','.join(
        'bcast_scalar(val[{}], root)'.format(i) for i in range(ucmc__qsssh)
        ), ',' if ucmc__qsssh else '')
    ntqz__kgsw = {}
    exec(qes__ugu, {'bcast_scalar': bcast_scalar}, ntqz__kgsw)
    urdwr__bxw = ntqz__kgsw['bcast_tuple_impl']
    return urdwr__bxw


def prealloc_str_for_bcast(arr, root=MPI_ROOT):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr, root=MPI_ROOT):
    if arr == string_array_type:

        def prealloc_impl(arr, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            gtgf__ezm = bcast_scalar(len(arr), root)
            xgsob__lun = bcast_scalar(np.int64(num_total_chars(arr)), root)
            if rank != root:
                arr = pre_alloc_string_array(gtgf__ezm, xgsob__lun)
            return arr
        return prealloc_impl
    return lambda arr, root=MPI_ROOT: arr


def get_local_slice(idx, arr_start, total_len):
    return idx


@overload(get_local_slice, no_unliteral=True, jit_options={'cache': True,
    'no_cpython_wrapper': True})
def get_local_slice_overload(idx, arr_start, total_len):
    if not idx.has_step:

        def impl(idx, arr_start, total_len):
            slice_index = numba.cpython.unicode._normalize_slice(idx, total_len
                )
            nnk__biou = max(arr_start, slice_index.start) - arr_start
            vfe__uswv = max(slice_index.stop - arr_start, 0)
            return slice(nnk__biou, vfe__uswv)
    else:

        def impl(idx, arr_start, total_len):
            slice_index = numba.cpython.unicode._normalize_slice(idx, total_len
                )
            wjmv__xvfmf = slice_index.start
            swzzu__bfwuc = slice_index.step
            dnxzz__wje = (0 if swzzu__bfwuc == 1 or wjmv__xvfmf > arr_start
                 else abs(swzzu__bfwuc - arr_start % swzzu__bfwuc) %
                swzzu__bfwuc)
            nnk__biou = max(arr_start, slice_index.start
                ) - arr_start + dnxzz__wje
            vfe__uswv = max(slice_index.stop - arr_start, 0)
            return slice(nnk__biou, vfe__uswv, swzzu__bfwuc)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        gyag__kyvzg = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[gyag__kyvzg])
    return getitem_impl


dummy_use = numba.njit(lambda a: None)


def int_getitem(arr, ind, arr_start, total_len, is_1D):
    return arr[ind]


def transform_str_getitem_output(data, length):
    pass


@overload(transform_str_getitem_output)
def overload_transform_str_getitem_output(data, length):
    if data == bodo.string_type:
        return lambda data, length: bodo.libs.str_arr_ext.decode_utf8(data.
            _data, length)
    if data == types.Array(types.uint8, 1, 'C'):
        return lambda data, length: bodo.libs.binary_arr_ext.init_bytes_type(
            data, length)
    raise BodoError(
        f'Internal Error: Expected String or Uint8 Array, found {data}')


@overload(int_getitem, no_unliteral=True)
def int_getitem_overload(arr, ind, arr_start, total_len, is_1D):
    if is_str_arr_type(arr) or arr == bodo.binary_array_type:
        qewh__xaxtk = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        ttmx__puo = np.int32(numba_to_c_type(types.uint8))
        fpmb__vzym = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            arr = decode_if_dict_array(arr)
            ind = ind % total_len
            root = np.int32(0)
            zbhqn__bwfrz = np.int32(10)
            tag = np.int32(11)
            kffh__chsqf = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                tmyab__ayai = arr._data
                sfxd__aah = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    tmyab__ayai, ind)
                quza__iesxc = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    tmyab__ayai, ind + 1)
                length = quza__iesxc - sfxd__aah
                fvr__mdey = tmyab__ayai[ind]
                kffh__chsqf[0] = length
                isend(kffh__chsqf, np.int32(1), root, zbhqn__bwfrz, True)
                isend(fvr__mdey, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(fpmb__vzym
                , qewh__xaxtk, 0, 1)
            ojsof__izte = 0
            if rank == root:
                ojsof__izte = recv(np.int64, ANY_SOURCE, zbhqn__bwfrz)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    fpmb__vzym, qewh__xaxtk, ojsof__izte, 1)
                cye__bfxq = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(cye__bfxq, np.int32(ojsof__izte), ttmx__puo,
                    ANY_SOURCE, tag)
            dummy_use(kffh__chsqf)
            ojsof__izte = bcast_scalar(ojsof__izte)
            dummy_use(arr)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    fpmb__vzym, qewh__xaxtk, ojsof__izte, 1)
            cye__bfxq = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(cye__bfxq, np.int32(ojsof__izte), ttmx__puo, np.array([
                -1]).ctypes, 0, np.int32(root))
            val = transform_str_getitem_output(val, ojsof__izte)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        jqgx__jvsc = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, jqgx__jvsc)
            if arr_start <= ind < arr_start + len(arr):
                zslj__sby = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = zslj__sby[ind - arr_start]
                send_arr = np.full(1, data, jqgx__jvsc)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = jqgx__jvsc(-1)
            if rank == root:
                val = recv(jqgx__jvsc, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            yvq__jtdw = arr.dtype.categories[max(val, 0)]
            return yvq__jtdw
        return cat_getitem_impl
    iccm__lnoe = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, iccm__lnoe)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, iccm__lnoe)[0]
        if rank == root:
            val = recv(iccm__lnoe, ANY_SOURCE, tag)
        dummy_use(send_arr)
        val = bcast_scalar(val)
        return val
    return getitem_impl


c_alltoallv = types.ExternalFunction('c_alltoallv', types.void(types.
    voidptr, types.voidptr, types.voidptr, types.voidptr, types.voidptr,
    types.voidptr, types.int32))


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def alltoallv(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    typ_enum = get_type_enum(send_data)
    qqizl__vrj = get_type_enum(out_data)
    assert typ_enum == qqizl__vrj
    if isinstance(send_data, (IntegerArrayType, DecimalArrayType)
        ) or send_data in (boolean_array, datetime_date_array_type):
        return (lambda send_data, out_data, send_counts, recv_counts,
            send_disp, recv_disp: c_alltoallv(send_data._data.ctypes,
            out_data._data.ctypes, send_counts.ctypes, recv_counts.ctypes,
            send_disp.ctypes, recv_disp.ctypes, typ_enum))
    if isinstance(send_data, bodo.CategoricalArrayType):
        return (lambda send_data, out_data, send_counts, recv_counts,
            send_disp, recv_disp: c_alltoallv(send_data.codes.ctypes,
            out_data.codes.ctypes, send_counts.ctypes, recv_counts.ctypes,
            send_disp.ctypes, recv_disp.ctypes, typ_enum))
    return (lambda send_data, out_data, send_counts, recv_counts, send_disp,
        recv_disp: c_alltoallv(send_data.ctypes, out_data.ctypes,
        send_counts.ctypes, recv_counts.ctypes, send_disp.ctypes, recv_disp
        .ctypes, typ_enum))


def alltoallv_tup(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    return


@overload(alltoallv_tup, no_unliteral=True)
def alltoallv_tup_overload(send_data, out_data, send_counts, recv_counts,
    send_disp, recv_disp):
    count = send_data.count
    assert out_data.count == count
    qes__ugu = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        qes__ugu += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    qes__ugu += '  return\n'
    ntqz__kgsw = {}
    exec(qes__ugu, {'alltoallv': alltoallv}, ntqz__kgsw)
    fykm__txbo = ntqz__kgsw['f']
    return fykm__txbo


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    wjmv__xvfmf = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return wjmv__xvfmf, count


@numba.njit
def get_start(total_size, pes, rank):
    xxis__ykbw = total_size % pes
    ebstq__lizxr = (total_size - xxis__ykbw) // pes
    return rank * ebstq__lizxr + min(rank, xxis__ykbw)


@numba.njit
def get_end(total_size, pes, rank):
    xxis__ykbw = total_size % pes
    ebstq__lizxr = (total_size - xxis__ykbw) // pes
    return (rank + 1) * ebstq__lizxr + min(rank + 1, xxis__ykbw)


@numba.njit
def get_node_portion(total_size, pes, rank):
    xxis__ykbw = total_size % pes
    ebstq__lizxr = (total_size - xxis__ykbw) // pes
    if rank < xxis__ykbw:
        return ebstq__lizxr + 1
    else:
        return ebstq__lizxr


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    zkl__hnlql = in_arr.dtype(0)
    ttsal__mpy = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        gpmuo__mrb = zkl__hnlql
        for kevi__vcghw in np.nditer(in_arr):
            gpmuo__mrb += kevi__vcghw.item()
        uvvux__rwvb = dist_exscan(gpmuo__mrb, ttsal__mpy)
        for i in range(in_arr.size):
            uvvux__rwvb += in_arr[i]
            out_arr[i] = uvvux__rwvb
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    atv__ooeea = in_arr.dtype(1)
    ttsal__mpy = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        gpmuo__mrb = atv__ooeea
        for kevi__vcghw in np.nditer(in_arr):
            gpmuo__mrb *= kevi__vcghw.item()
        uvvux__rwvb = dist_exscan(gpmuo__mrb, ttsal__mpy)
        if get_rank() == 0:
            uvvux__rwvb = atv__ooeea
        for i in range(in_arr.size):
            uvvux__rwvb *= in_arr[i]
            out_arr[i] = uvvux__rwvb
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        atv__ooeea = np.finfo(in_arr.dtype(1).dtype).max
    else:
        atv__ooeea = np.iinfo(in_arr.dtype(1).dtype).max
    ttsal__mpy = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        gpmuo__mrb = atv__ooeea
        for kevi__vcghw in np.nditer(in_arr):
            gpmuo__mrb = min(gpmuo__mrb, kevi__vcghw.item())
        uvvux__rwvb = dist_exscan(gpmuo__mrb, ttsal__mpy)
        if get_rank() == 0:
            uvvux__rwvb = atv__ooeea
        for i in range(in_arr.size):
            uvvux__rwvb = min(uvvux__rwvb, in_arr[i])
            out_arr[i] = uvvux__rwvb
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        atv__ooeea = np.finfo(in_arr.dtype(1).dtype).min
    else:
        atv__ooeea = np.iinfo(in_arr.dtype(1).dtype).min
    atv__ooeea = in_arr.dtype(1)
    ttsal__mpy = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        gpmuo__mrb = atv__ooeea
        for kevi__vcghw in np.nditer(in_arr):
            gpmuo__mrb = max(gpmuo__mrb, kevi__vcghw.item())
        uvvux__rwvb = dist_exscan(gpmuo__mrb, ttsal__mpy)
        if get_rank() == 0:
            uvvux__rwvb = atv__ooeea
        for i in range(in_arr.size):
            uvvux__rwvb = max(uvvux__rwvb, in_arr[i])
            out_arr[i] = uvvux__rwvb
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    lvkzc__tuhu = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), lvkzc__tuhu)


def dist_return(A):
    return A


def rep_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    uyfc__fgvqp = args[0]
    if equiv_set.has_shape(uyfc__fgvqp):
        return ArrayAnalysis.AnalyzeResult(shape=uyfc__fgvqp, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_distributed_api_dist_return = (
    dist_return_equiv)
ArrayAnalysis._analyze_op_call_bodo_libs_distributed_api_rep_return = (
    dist_return_equiv)


def threaded_return(A):
    return A


@numba.njit
def set_arr_local(arr, ind, val):
    arr[ind] = val


@numba.njit
def local_alloc_size(n, in_arr):
    return n


@infer_global(threaded_return)
@infer_global(dist_return)
@infer_global(rep_return)
class ThreadedRetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        return signature(args[0], *args)


@numba.njit
def parallel_print(*args):
    print(*args)


@numba.njit
def single_print(*args):
    if bodo.libs.distributed_api.get_rank() == 0:
        print(*args)


def print_if_not_empty(args):
    pass


@overload(print_if_not_empty)
def overload_print_if_not_empty(*args):
    ngne__dofcs = '(' + ' or '.join(['False'] + [f'len(args[{i}]) != 0' for
        i, hsrj__vrib in enumerate(args) if is_array_typ(hsrj__vrib) or
        isinstance(hsrj__vrib, bodo.hiframes.pd_dataframe_ext.DataFrameType)]
        ) + ')'
    qes__ugu = f"""def impl(*args):
    if {ngne__dofcs} or bodo.get_rank() == 0:
        print(*args)"""
    ntqz__kgsw = {}
    exec(qes__ugu, globals(), ntqz__kgsw)
    impl = ntqz__kgsw['impl']
    return impl


_wait = types.ExternalFunction('dist_wait', types.void(mpi_req_numba_type,
    types.bool_))


@numba.generated_jit(nopython=True)
def wait(req, cond=True):
    if isinstance(req, types.BaseTuple):
        count = len(req.types)
        aqm__oaahk = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        qes__ugu = 'def f(req, cond=True):\n'
        qes__ugu += f'  return {aqm__oaahk}\n'
        ntqz__kgsw = {}
        exec(qes__ugu, {'_wait': _wait}, ntqz__kgsw)
        impl = ntqz__kgsw['f']
        return impl
    if is_overload_none(req):
        return lambda req, cond=True: None
    return lambda req, cond=True: _wait(req, cond)


@register_jitable
def _set_if_in_range(A, val, index, chunk_start):
    if index >= chunk_start and index < chunk_start + len(A):
        A[index - chunk_start] = val


@register_jitable
def _root_rank_select(old_val, new_val):
    if get_rank() == 0:
        return old_val
    return new_val


def get_tuple_prod(t):
    return np.prod(t)


@overload(get_tuple_prod, no_unliteral=True)
def get_tuple_prod_overload(t):
    if t == numba.core.types.containers.Tuple(()):
        return lambda t: 1

    def get_tuple_prod_impl(t):
        xxis__ykbw = 1
        for a in t:
            xxis__ykbw *= a
        return xxis__ykbw
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    nit__gawuh = np.ascontiguousarray(in_arr)
    ubs__kmo = get_tuple_prod(nit__gawuh.shape[1:])
    txpay__wpusz = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        forh__wbuwg = np.array(dest_ranks, dtype=np.int32)
    else:
        forh__wbuwg = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, nit__gawuh.ctypes, new_dim0_global_len,
        len(in_arr), dtype_size * txpay__wpusz, dtype_size * ubs__kmo, len(
        forh__wbuwg), forh__wbuwg.ctypes)
    check_and_propagate_cpp_exception()


permutation_int = types.ExternalFunction('permutation_int', types.void(
    types.voidptr, types.intp))


@numba.njit
def dist_permutation_int(lhs, n):
    permutation_int(lhs.ctypes, n)


permutation_array_index = types.ExternalFunction('permutation_array_index',
    types.void(types.voidptr, types.intp, types.intp, types.voidptr, types.
    int64, types.voidptr, types.intp, types.int64))


@numba.njit
def dist_permutation_array_index(lhs, lhs_len, dtype_size, rhs, p, p_len,
    n_samples):
    fmkfb__mtcw = np.ascontiguousarray(rhs)
    dem__iamdg = get_tuple_prod(fmkfb__mtcw.shape[1:])
    spl__rqm = dtype_size * dem__iamdg
    permutation_array_index(lhs.ctypes, lhs_len, spl__rqm, fmkfb__mtcw.
        ctypes, fmkfb__mtcw.shape[0], p.ctypes, p_len, n_samples)
    check_and_propagate_cpp_exception()


from bodo.io import fsspec_reader, hdfs_reader, s3_reader
ll.add_symbol('finalize', hdist.finalize)
finalize = types.ExternalFunction('finalize', types.int32())
ll.add_symbol('finalize_s3', s3_reader.finalize_s3)
finalize_s3 = types.ExternalFunction('finalize_s3', types.int32())
ll.add_symbol('finalize_fsspec', fsspec_reader.finalize_fsspec)
finalize_fsspec = types.ExternalFunction('finalize_fsspec', types.int32())
ll.add_symbol('disconnect_hdfs', hdfs_reader.disconnect_hdfs)
disconnect_hdfs = types.ExternalFunction('disconnect_hdfs', types.int32())


def _check_for_cpp_errors():
    pass


@overload(_check_for_cpp_errors)
def overload_check_for_cpp_errors():
    return lambda : check_and_propagate_cpp_exception()


@numba.njit
def call_finalize():
    finalize()
    finalize_s3()
    finalize_fsspec()
    _check_for_cpp_errors()
    disconnect_hdfs()


def flush_stdout():
    if not sys.stdout.closed:
        sys.stdout.flush()


atexit.register(call_finalize)
atexit.register(flush_stdout)


def bcast_comm(data, comm_ranks, nranks, root=MPI_ROOT):
    rank = bodo.libs.distributed_api.get_rank()
    dtype = bodo.typeof(data)
    dtype = _bcast_dtype(dtype, root)
    if rank != MPI_ROOT:
        data = get_value_for_type(dtype)
    return bcast_comm_impl(data, comm_ranks, nranks, root)


@overload(bcast_comm)
def bcast_comm_overload(data, comm_ranks, nranks, root=MPI_ROOT):
    return lambda data, comm_ranks, nranks, root=MPI_ROOT: bcast_comm_impl(data
        , comm_ranks, nranks, root)


@numba.generated_jit(nopython=True)
def bcast_comm_impl(data, comm_ranks, nranks, root=MPI_ROOT):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.bcast_comm()')
    if isinstance(data, (types.Integer, types.Float)):
        typ_val = numba_to_c_type(data)
        qes__ugu = (
            f"""def bcast_scalar_impl(data, comm_ranks, nranks, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({{}}), comm_ranks,ctypes, np.int32({{}}), np.int32(root))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        ntqz__kgsw = {}
        exec(qes__ugu, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
            dtype}, ntqz__kgsw)
        mqu__cvlvn = ntqz__kgsw['bcast_scalar_impl']
        return mqu__cvlvn
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: _bcast_np(data,
            comm_ranks, nranks, root)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        paj__mpjjq = len(data.columns)
        jyfjl__enl = ', '.join('g_data_{}'.format(i) for i in range(paj__mpjjq)
            )
        kox__tiwcr = ColNamesMetaType(data.columns)
        qes__ugu = f'def impl_df(data, comm_ranks, nranks, root={MPI_ROOT}):\n'
        for i in range(paj__mpjjq):
            qes__ugu += (
                '  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})\n'
                .format(i, i))
            qes__ugu += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks, root)
"""
                .format(i, i))
        qes__ugu += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        qes__ugu += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks, root)
"""
        qes__ugu += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, __col_name_meta_value_bcast_comm)
"""
            .format(jyfjl__enl))
        ntqz__kgsw = {}
        exec(qes__ugu, {'bodo': bodo, '__col_name_meta_value_bcast_comm':
            kox__tiwcr}, ntqz__kgsw)
        lib__kmsfb = ntqz__kgsw['impl_df']
        return lib__kmsfb
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            wjmv__xvfmf = data._start
            zrsxx__ycg = data._stop
            swzzu__bfwuc = data._step
            noc__duvl = data._name
            noc__duvl = bcast_scalar(noc__duvl, root)
            wjmv__xvfmf = bcast_scalar(wjmv__xvfmf, root)
            zrsxx__ycg = bcast_scalar(zrsxx__ycg, root)
            swzzu__bfwuc = bcast_scalar(swzzu__bfwuc, root)
            jetu__qsyj = bodo.libs.array_kernels.calc_nitems(wjmv__xvfmf,
                zrsxx__ycg, swzzu__bfwuc)
            chunk_start = bodo.libs.distributed_api.get_start(jetu__qsyj,
                n_pes, rank)
            goj__cguwg = bodo.libs.distributed_api.get_node_portion(jetu__qsyj,
                n_pes, rank)
            nnk__biou = wjmv__xvfmf + swzzu__bfwuc * chunk_start
            vfe__uswv = wjmv__xvfmf + swzzu__bfwuc * (chunk_start + goj__cguwg)
            vfe__uswv = min(vfe__uswv, zrsxx__ycg)
            return bodo.hiframes.pd_index_ext.init_range_index(nnk__biou,
                vfe__uswv, swzzu__bfwuc, noc__duvl)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks, root=MPI_ROOT):
            kess__mvo = data._data
            noc__duvl = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(kess__mvo,
                comm_ranks, nranks, root)
            return bodo.utils.conversion.index_from_array(arr, noc__duvl)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            noc__duvl = bodo.hiframes.pd_series_ext.get_series_name(data)
            mqbgf__mac = bodo.libs.distributed_api.bcast_comm_impl(noc__duvl,
                comm_ranks, nranks, root)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks, root)
            mjnd__dfb = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                mjnd__dfb, mqbgf__mac)
        return impl_series
    if isinstance(data, types.BaseTuple):
        qes__ugu = (
            f'def impl_tuple(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        qes__ugu += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks, root)'.format(i) for
            i in range(len(data))), ',' if len(data) > 0 else '')
        ntqz__kgsw = {}
        exec(qes__ugu, {'bcast_comm_impl': bcast_comm_impl}, ntqz__kgsw)
        nla__grbxw = ntqz__kgsw['impl_tuple']
        return nla__grbxw
    if data is types.none:
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks, root=MPI_ROOT):
    typ_val = numba_to_c_type(data.dtype)
    grk__udn = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    zve__akbab = (0,) * grk__udn

    def bcast_arr_impl(data, comm_ranks, nranks, root=MPI_ROOT):
        rank = bodo.libs.distributed_api.get_rank()
        kess__mvo = np.ascontiguousarray(data)
        cye__bfxq = data.ctypes
        ejwh__ygvf = zve__akbab
        if rank == root:
            ejwh__ygvf = kess__mvo.shape
        ejwh__ygvf = bcast_tuple(ejwh__ygvf, root)
        aeysv__tigh = get_tuple_prod(ejwh__ygvf[1:])
        send_counts = ejwh__ygvf[0] * aeysv__tigh
        cat__vnzx = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(cye__bfxq, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return data
        else:
            c_bcast(cat__vnzx.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return cat__vnzx.reshape((-1,) + ejwh__ygvf[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        ydw__edck = MPI.COMM_WORLD
        beuly__fzy = MPI.Get_processor_name()
        roeq__jtl = ydw__edck.allgather(beuly__fzy)
        node_ranks = defaultdict(list)
        for i, oxrg__iqm in enumerate(roeq__jtl):
            node_ranks[oxrg__iqm].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    ydw__edck = MPI.COMM_WORLD
    nrd__gcs = ydw__edck.Get_group()
    xpbw__slxag = nrd__gcs.Incl(comm_ranks)
    ztck__xhp = ydw__edck.Create_group(xpbw__slxag)
    return ztck__xhp


def get_nodes_first_ranks():
    zntje__enyl = get_host_ranks()
    return np.array([fpjx__fws[0] for fpjx__fws in zntje__enyl.values()],
        dtype='int32')


def get_num_nodes():
    return len(get_host_ranks())
