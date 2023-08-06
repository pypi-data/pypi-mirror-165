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
    pyf__ovg = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, pyf__ovg, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    pyf__ovg = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, pyf__ovg, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            pyf__ovg = get_type_enum(arr)
            return _isend(arr.ctypes, size, pyf__ovg, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        pyf__ovg = np.int32(numba_to_c_type(arr.dtype))
        awg__wzn = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            iewp__sqtj = size + 7 >> 3
            bpcqh__tdco = _isend(arr._data.ctypes, size, pyf__ovg, pe, tag,
                cond)
            ewyka__ooq = _isend(arr._null_bitmap.ctypes, iewp__sqtj,
                awg__wzn, pe, tag, cond)
            return bpcqh__tdco, ewyka__ooq
        return impl_nullable
    if is_str_arr_type(arr) or arr == binary_array_type:
        dns__qwgz = np.int32(numba_to_c_type(offset_type))
        awg__wzn = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            arr = decode_if_dict_array(arr)
            vik__azs = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(vik__azs, pe, tag - 1)
            iewp__sqtj = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                dns__qwgz, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), vik__azs,
                awg__wzn, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr),
                iewp__sqtj, awg__wzn, pe, tag)
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
            pyf__ovg = get_type_enum(arr)
            return _irecv(arr.ctypes, size, pyf__ovg, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        pyf__ovg = np.int32(numba_to_c_type(arr.dtype))
        awg__wzn = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            iewp__sqtj = size + 7 >> 3
            bpcqh__tdco = _irecv(arr._data.ctypes, size, pyf__ovg, pe, tag,
                cond)
            ewyka__ooq = _irecv(arr._null_bitmap.ctypes, iewp__sqtj,
                awg__wzn, pe, tag, cond)
            return bpcqh__tdco, ewyka__ooq
        return impl_nullable
    if arr in [binary_array_type, string_array_type]:
        dns__qwgz = np.int32(numba_to_c_type(offset_type))
        awg__wzn = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            muwtg__uqc = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            muwtg__uqc = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        bijkv__kkuv = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {muwtg__uqc}(size, n_chars)
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
        bufh__hcd = dict()
        exec(bijkv__kkuv, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            dns__qwgz, 'char_typ_enum': awg__wzn}, bufh__hcd)
        impl = bufh__hcd['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    pyf__ovg = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), pyf__ovg)


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
        qaqt__fqbs = n_pes if rank == root or allgather else 0
        utbo__isoe = np.empty(qaqt__fqbs, dtype)
        c_gather_scalar(send.ctypes, utbo__isoe.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return utbo__isoe
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
        zos__rwp = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], zos__rwp)
        return builder.bitcast(zos__rwp, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        zos__rwp = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(zos__rwp)
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
    mzok__jpr = types.unliteral(value)
    if isinstance(mzok__jpr, IndexValueType):
        mzok__jpr = mzok__jpr.val_typ
        qzhu__qsf = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            qzhu__qsf.append(types.int64)
            qzhu__qsf.append(bodo.datetime64ns)
            qzhu__qsf.append(bodo.timedelta64ns)
            qzhu__qsf.append(bodo.datetime_date_type)
            qzhu__qsf.append(bodo.TimeType)
        if mzok__jpr not in qzhu__qsf:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(mzok__jpr))
    typ_enum = np.int32(numba_to_c_type(mzok__jpr))

    def impl(value, reduce_op):
        vdl__kkh = value_to_ptr(value)
        hkckl__unwg = value_to_ptr(value)
        _dist_reduce(vdl__kkh, hkckl__unwg, reduce_op, typ_enum)
        return load_val_ptr(hkckl__unwg, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    mzok__jpr = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(mzok__jpr))
    ozdgd__abip = mzok__jpr(0)

    def impl(value, reduce_op):
        vdl__kkh = value_to_ptr(value)
        hkckl__unwg = value_to_ptr(ozdgd__abip)
        _dist_exscan(vdl__kkh, hkckl__unwg, reduce_op, typ_enum)
        return load_val_ptr(hkckl__unwg, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    vtsb__pmb = 0
    xac__ldn = 0
    for i in range(len(recv_counts)):
        xye__qdffm = recv_counts[i]
        iewp__sqtj = recv_counts_nulls[i]
        omfk__kmpen = tmp_null_bytes[vtsb__pmb:vtsb__pmb + iewp__sqtj]
        for xafha__vwr in range(xye__qdffm):
            set_bit_to(null_bitmap_ptr, xac__ldn, get_bit(omfk__kmpen,
                xafha__vwr))
            xac__ldn += 1
        vtsb__pmb += iewp__sqtj


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.gatherv()')
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            cgs__nvo = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                cgs__nvo, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            blh__jqolo = data.size
            recv_counts = gather_scalar(np.int32(blh__jqolo), allgather,
                root=root)
            bsnd__ctpoq = recv_counts.sum()
            imm__bxwb = empty_like_type(bsnd__ctpoq, data)
            sdama__nyl = np.empty(1, np.int32)
            if rank == root or allgather:
                sdama__nyl = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(blh__jqolo), imm__bxwb.ctypes,
                recv_counts.ctypes, sdama__nyl.ctypes, np.int32(typ_val),
                allgather, np.int32(root))
            return imm__bxwb.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if is_str_arr_type(data):

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            data = decode_if_dict_array(data)
            imm__bxwb = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.str_arr_ext.init_str_arr(imm__bxwb)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            imm__bxwb = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(imm__bxwb)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        awg__wzn = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            blh__jqolo = len(data)
            iewp__sqtj = blh__jqolo + 7 >> 3
            recv_counts = gather_scalar(np.int32(blh__jqolo), allgather,
                root=root)
            bsnd__ctpoq = recv_counts.sum()
            imm__bxwb = empty_like_type(bsnd__ctpoq, data)
            sdama__nyl = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            lzntb__qzrkq = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                sdama__nyl = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                lzntb__qzrkq = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(blh__jqolo),
                imm__bxwb._days_data.ctypes, recv_counts.ctypes, sdama__nyl
                .ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._seconds_data.ctypes, np.int32(blh__jqolo),
                imm__bxwb._seconds_data.ctypes, recv_counts.ctypes,
                sdama__nyl.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._microseconds_data.ctypes, np.int32(blh__jqolo),
                imm__bxwb._microseconds_data.ctypes, recv_counts.ctypes,
                sdama__nyl.ctypes, np.int32(typ_val), allgather, np.int32(root)
                )
            c_gatherv(data._null_bitmap.ctypes, np.int32(iewp__sqtj),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                lzntb__qzrkq.ctypes, awg__wzn, allgather, np.int32(root))
            copy_gathered_null_bytes(imm__bxwb._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return imm__bxwb
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        awg__wzn = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            blh__jqolo = len(data)
            iewp__sqtj = blh__jqolo + 7 >> 3
            recv_counts = gather_scalar(np.int32(blh__jqolo), allgather,
                root=root)
            bsnd__ctpoq = recv_counts.sum()
            imm__bxwb = empty_like_type(bsnd__ctpoq, data)
            sdama__nyl = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            lzntb__qzrkq = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                sdama__nyl = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                lzntb__qzrkq = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(blh__jqolo), imm__bxwb.
                _data.ctypes, recv_counts.ctypes, sdama__nyl.ctypes, np.
                int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(iewp__sqtj),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                lzntb__qzrkq.ctypes, awg__wzn, allgather, np.int32(root))
            copy_gathered_null_bytes(imm__bxwb._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return imm__bxwb
        return gatherv_impl_int_arr
    if isinstance(data, DatetimeArrayType):
        krzw__rhv = data.tz

        def impl_pd_datetime_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            kafs__fzanb = bodo.gatherv(data._data, allgather, warn_if_rep, root
                )
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(
                kafs__fzanb, krzw__rhv)
        return impl_pd_datetime_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            tlph__ika = bodo.gatherv(data._left, allgather, warn_if_rep, root)
            lmibw__kvkb = bodo.gatherv(data._right, allgather, warn_if_rep,
                root)
            return bodo.libs.interval_arr_ext.init_interval_array(tlph__ika,
                lmibw__kvkb)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            qzjje__sufh = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            swur__zapf = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                swur__zapf, qzjje__sufh)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        qgtod__xirx = np.iinfo(np.int64).max
        upl__maaeq = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            axqz__eichr = data._start
            niv__rws = data._stop
            if len(data) == 0:
                axqz__eichr = qgtod__xirx
                niv__rws = upl__maaeq
            axqz__eichr = bodo.libs.distributed_api.dist_reduce(axqz__eichr,
                np.int32(Reduce_Type.Min.value))
            niv__rws = bodo.libs.distributed_api.dist_reduce(niv__rws, np.
                int32(Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if axqz__eichr == qgtod__xirx and niv__rws == upl__maaeq:
                axqz__eichr = 0
                niv__rws = 0
            lul__ess = max(0, -(-(niv__rws - axqz__eichr) // data._step))
            if lul__ess < total_len:
                niv__rws = axqz__eichr + data._step * total_len
            if bodo.get_rank() != root and not allgather:
                axqz__eichr = 0
                niv__rws = 0
            return bodo.hiframes.pd_index_ext.init_range_index(axqz__eichr,
                niv__rws, data._step, data._name)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        from bodo.hiframes.pd_index_ext import PeriodIndexType
        if isinstance(data, PeriodIndexType):
            wanv__zrb = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, wanv__zrb)
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
            imm__bxwb = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(imm__bxwb,
                data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.table.TableType):
        dtf__pzcu = {'bodo': bodo, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like, 'init_table': bodo.hiframes.table.init_table}
        bijkv__kkuv = (
            f'def impl_table(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):\n'
            )
        bijkv__kkuv += '  T = data\n'
        bijkv__kkuv += '  T2 = init_table(T, True)\n'
        for chnnj__obrzr in data.type_to_blk.values():
            dtf__pzcu[f'arr_inds_{chnnj__obrzr}'] = np.array(data.
                block_to_arr_ind[chnnj__obrzr], dtype=np.int64)
            bijkv__kkuv += (
                f'  arr_list_{chnnj__obrzr} = get_table_block(T, {chnnj__obrzr})\n'
                )
            bijkv__kkuv += f"""  out_arr_list_{chnnj__obrzr} = alloc_list_like(arr_list_{chnnj__obrzr}, len(arr_list_{chnnj__obrzr}), True)
"""
            bijkv__kkuv += f'  for i in range(len(arr_list_{chnnj__obrzr})):\n'
            bijkv__kkuv += (
                f'    arr_ind_{chnnj__obrzr} = arr_inds_{chnnj__obrzr}[i]\n')
            bijkv__kkuv += f"""    ensure_column_unboxed(T, arr_list_{chnnj__obrzr}, i, arr_ind_{chnnj__obrzr})
"""
            bijkv__kkuv += f"""    out_arr_{chnnj__obrzr} = bodo.gatherv(arr_list_{chnnj__obrzr}[i], allgather, warn_if_rep, root)
"""
            bijkv__kkuv += (
                f'    out_arr_list_{chnnj__obrzr}[i] = out_arr_{chnnj__obrzr}\n'
                )
            bijkv__kkuv += f"""  T2 = set_table_block(T2, out_arr_list_{chnnj__obrzr}, {chnnj__obrzr})
"""
        bijkv__kkuv += (
            f'  length = T._len if bodo.get_rank() == root or allgather else 0\n'
            )
        bijkv__kkuv += f'  T2 = set_table_len(T2, length)\n'
        bijkv__kkuv += f'  return T2\n'
        bufh__hcd = {}
        exec(bijkv__kkuv, dtf__pzcu, bufh__hcd)
        khd__wqn = bufh__hcd['impl_table']
        return khd__wqn
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        tjif__fyxwf = len(data.columns)
        if tjif__fyxwf == 0:
            qvoqj__xwjj = ColNamesMetaType(())

            def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
                index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data
                    )
                wcbs__ioch = bodo.gatherv(index, allgather, warn_if_rep, root)
                return bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                    wcbs__ioch, qvoqj__xwjj)
            return impl
        mnsx__ytgex = ', '.join(f'g_data_{i}' for i in range(tjif__fyxwf))
        bijkv__kkuv = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        if data.is_table_format:
            from bodo.transforms.distributed_analysis import Distribution
            zhd__dgjti = bodo.hiframes.pd_dataframe_ext.DataFrameType(data.
                data, data.index, data.columns, Distribution.REP, True)
            mnsx__ytgex = 'T2'
            bijkv__kkuv += (
                '  T = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            bijkv__kkuv += (
                '  T2 = bodo.gatherv(T, allgather, warn_if_rep, root)\n')
        else:
            for i in range(tjif__fyxwf):
                bijkv__kkuv += (
                    """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                    .format(i, i))
                bijkv__kkuv += (
                    """  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)
"""
                    .format(i, i))
        bijkv__kkuv += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        bijkv__kkuv += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        bijkv__kkuv += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, __col_name_meta_value_gatherv_with_cols)
"""
            .format(mnsx__ytgex))
        bufh__hcd = {}
        dtf__pzcu = {'bodo': bodo,
            '__col_name_meta_value_gatherv_with_cols': ColNamesMetaType(
            data.columns)}
        exec(bijkv__kkuv, dtf__pzcu, bufh__hcd)
        aky__axzn = bufh__hcd['impl_df']
        return aky__axzn
    if isinstance(data, ArrayItemArrayType):
        ignin__wyxrf = np.int32(numba_to_c_type(types.int32))
        awg__wzn = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            kzihi__qtoko = bodo.libs.array_item_arr_ext.get_offsets(data)
            wfrds__codrs = bodo.libs.array_item_arr_ext.get_data(data)
            wfrds__codrs = wfrds__codrs[:kzihi__qtoko[-1]]
            pwhbk__kmhre = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            blh__jqolo = len(data)
            siyat__ixzd = np.empty(blh__jqolo, np.uint32)
            iewp__sqtj = blh__jqolo + 7 >> 3
            for i in range(blh__jqolo):
                siyat__ixzd[i] = kzihi__qtoko[i + 1] - kzihi__qtoko[i]
            recv_counts = gather_scalar(np.int32(blh__jqolo), allgather,
                root=root)
            bsnd__ctpoq = recv_counts.sum()
            sdama__nyl = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            lzntb__qzrkq = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                sdama__nyl = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for joj__naag in range(len(recv_counts)):
                    recv_counts_nulls[joj__naag] = recv_counts[joj__naag
                        ] + 7 >> 3
                lzntb__qzrkq = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            jlkkn__fpy = np.empty(bsnd__ctpoq + 1, np.uint32)
            vmcc__tmec = bodo.gatherv(wfrds__codrs, allgather, warn_if_rep,
                root)
            gef__tzpco = np.empty(bsnd__ctpoq + 7 >> 3, np.uint8)
            c_gatherv(siyat__ixzd.ctypes, np.int32(blh__jqolo), jlkkn__fpy.
                ctypes, recv_counts.ctypes, sdama__nyl.ctypes, ignin__wyxrf,
                allgather, np.int32(root))
            c_gatherv(pwhbk__kmhre.ctypes, np.int32(iewp__sqtj),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                lzntb__qzrkq.ctypes, awg__wzn, allgather, np.int32(root))
            dummy_use(data)
            ujbmw__bksff = np.empty(bsnd__ctpoq + 1, np.uint64)
            convert_len_arr_to_offset(jlkkn__fpy.ctypes, ujbmw__bksff.
                ctypes, bsnd__ctpoq)
            copy_gathered_null_bytes(gef__tzpco.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                bsnd__ctpoq, vmcc__tmec, ujbmw__bksff, gef__tzpco)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        vvyu__gdjc = data.names
        awg__wzn = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            mpny__iat = bodo.libs.struct_arr_ext.get_data(data)
            ctdq__egifm = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            iwccd__ngbz = bodo.gatherv(mpny__iat, allgather=allgather, root
                =root)
            rank = bodo.libs.distributed_api.get_rank()
            blh__jqolo = len(data)
            iewp__sqtj = blh__jqolo + 7 >> 3
            recv_counts = gather_scalar(np.int32(blh__jqolo), allgather,
                root=root)
            bsnd__ctpoq = recv_counts.sum()
            bzx__hyu = np.empty(bsnd__ctpoq + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            lzntb__qzrkq = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                lzntb__qzrkq = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(ctdq__egifm.ctypes, np.int32(iewp__sqtj),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes,
                lzntb__qzrkq.ctypes, awg__wzn, allgather, np.int32(root))
            copy_gathered_null_bytes(bzx__hyu.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(iwccd__ngbz,
                bzx__hyu, vvyu__gdjc)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            imm__bxwb = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(imm__bxwb)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            imm__bxwb = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.tuple_arr_ext.init_tuple_arr(imm__bxwb)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            imm__bxwb = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.map_arr_ext.init_map_arr(imm__bxwb)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            imm__bxwb = bodo.gatherv(data.data, allgather, warn_if_rep, root)
            cfcj__vaje = bodo.gatherv(data.indices, allgather, warn_if_rep,
                root)
            pkv__cwevv = bodo.gatherv(data.indptr, allgather, warn_if_rep, root
                )
            pvszz__kutgc = gather_scalar(data.shape[0], allgather, root=root)
            sdpu__nlsve = pvszz__kutgc.sum()
            tjif__fyxwf = bodo.libs.distributed_api.dist_reduce(data.shape[
                1], np.int32(Reduce_Type.Max.value))
            ggqhb__tvxg = np.empty(sdpu__nlsve + 1, np.int64)
            cfcj__vaje = cfcj__vaje.astype(np.int64)
            ggqhb__tvxg[0] = 0
            vitxf__dkp = 1
            oolm__vgp = 0
            for xomd__bcx in pvszz__kutgc:
                for zqd__ikmzr in range(xomd__bcx):
                    mmgsb__ndevs = pkv__cwevv[oolm__vgp + 1] - pkv__cwevv[
                        oolm__vgp]
                    ggqhb__tvxg[vitxf__dkp] = ggqhb__tvxg[vitxf__dkp - 1
                        ] + mmgsb__ndevs
                    vitxf__dkp += 1
                    oolm__vgp += 1
                oolm__vgp += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(imm__bxwb,
                cfcj__vaje, ggqhb__tvxg, (sdpu__nlsve, tjif__fyxwf))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        bijkv__kkuv = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        bijkv__kkuv += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        bufh__hcd = {}
        exec(bijkv__kkuv, {'bodo': bodo}, bufh__hcd)
        vgvy__cyyp = bufh__hcd['impl_tuple']
        return vgvy__cyyp
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    try:
        import bodosql
        from bodosql.context_ext import BodoSQLContextType
    except ImportError as jaq__qsyy:
        BodoSQLContextType = None
    if BodoSQLContextType is not None and isinstance(data, BodoSQLContextType):
        bijkv__kkuv = f"""def impl_bodosql_context(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):
"""
        vyu__mew = ', '.join([f"'{qzjje__sufh}'" for qzjje__sufh in data.names]
            )
        ics__jmlds = ', '.join([
            f'bodo.gatherv(data.dataframes[{i}], allgather, warn_if_rep, root)'
             for i in range(len(data.dataframes))])
        bijkv__kkuv += f"""  return bodosql.context_ext.init_sql_context(({vyu__mew}, ), ({ics__jmlds}, ), data.catalog)
"""
        bufh__hcd = {}
        exec(bijkv__kkuv, {'bodo': bodo, 'bodosql': bodosql}, bufh__hcd)
        kwq__bjce = bufh__hcd['impl_bodosql_context']
        return kwq__bjce
    try:
        import bodosql
        from bodosql import TablePathType
    except ImportError as jaq__qsyy:
        TablePathType = None
    if TablePathType is not None and isinstance(data, TablePathType):
        bijkv__kkuv = f"""def impl_table_path(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):
"""
        bijkv__kkuv += f'  return data\n'
        bufh__hcd = {}
        exec(bijkv__kkuv, {}, bufh__hcd)
        jsg__ncp = bufh__hcd['impl_table_path']
        return jsg__ncp
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.rebalance()')
    bijkv__kkuv = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    bijkv__kkuv += '    if random:\n'
    bijkv__kkuv += '        if random_seed is None:\n'
    bijkv__kkuv += '            random = 1\n'
    bijkv__kkuv += '        else:\n'
    bijkv__kkuv += '            random = 2\n'
    bijkv__kkuv += '    if random_seed is None:\n'
    bijkv__kkuv += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        iabr__hsgac = data
        tjif__fyxwf = len(iabr__hsgac.columns)
        for i in range(tjif__fyxwf):
            bijkv__kkuv += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        bijkv__kkuv += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        mnsx__ytgex = ', '.join(f'data_{i}' for i in range(tjif__fyxwf))
        bijkv__kkuv += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(tztv__nlxt) for
            tztv__nlxt in range(tjif__fyxwf))))
        bijkv__kkuv += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        bijkv__kkuv += '    if dests is None:\n'
        bijkv__kkuv += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        bijkv__kkuv += '    else:\n'
        bijkv__kkuv += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for cbi__cnxtm in range(tjif__fyxwf):
            bijkv__kkuv += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(cbi__cnxtm))
        bijkv__kkuv += (
            """    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)
"""
            .format(tjif__fyxwf))
        bijkv__kkuv += '    delete_table(out_table)\n'
        bijkv__kkuv += '    if parallel:\n'
        bijkv__kkuv += '        delete_table(table_total)\n'
        mnsx__ytgex = ', '.join('out_arr_{}'.format(i) for i in range(
            tjif__fyxwf))
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        bijkv__kkuv += (
            """    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, __col_name_meta_value_rebalance)
"""
            .format(mnsx__ytgex, index))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        bijkv__kkuv += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        bijkv__kkuv += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        bijkv__kkuv += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        bijkv__kkuv += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        bijkv__kkuv += '    if dests is None:\n'
        bijkv__kkuv += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        bijkv__kkuv += '    else:\n'
        bijkv__kkuv += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        bijkv__kkuv += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        bijkv__kkuv += """    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)
"""
        bijkv__kkuv += '    delete_table(out_table)\n'
        bijkv__kkuv += '    if parallel:\n'
        bijkv__kkuv += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        bijkv__kkuv += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        bijkv__kkuv += '    if not parallel:\n'
        bijkv__kkuv += '        return data\n'
        bijkv__kkuv += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        bijkv__kkuv += '    if dests is None:\n'
        bijkv__kkuv += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        bijkv__kkuv += '    elif bodo.get_rank() not in dests:\n'
        bijkv__kkuv += '        dim0_local_size = 0\n'
        bijkv__kkuv += '    else:\n'
        bijkv__kkuv += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        bijkv__kkuv += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        bijkv__kkuv += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        bijkv__kkuv += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        bijkv__kkuv += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        bijkv__kkuv += '    if dests is None:\n'
        bijkv__kkuv += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        bijkv__kkuv += '    else:\n'
        bijkv__kkuv += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        bijkv__kkuv += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        bijkv__kkuv += '    delete_table(out_table)\n'
        bijkv__kkuv += '    if parallel:\n'
        bijkv__kkuv += '        delete_table(table_total)\n'
        bijkv__kkuv += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    bufh__hcd = {}
    dtf__pzcu = {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.array.
        array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table}
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        dtf__pzcu.update({'__col_name_meta_value_rebalance':
            ColNamesMetaType(iabr__hsgac.columns)})
    exec(bijkv__kkuv, dtf__pzcu, bufh__hcd)
    impl = bufh__hcd['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, n_samples=None, parallel=False
    ):
    bijkv__kkuv = (
        'def impl(data, seed=None, dests=None, n_samples=None, parallel=False):\n'
        )
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        bijkv__kkuv += '    if seed is None:\n'
        bijkv__kkuv += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        bijkv__kkuv += '    np.random.seed(seed)\n'
        bijkv__kkuv += '    if not parallel:\n'
        bijkv__kkuv += '        data = data.copy()\n'
        bijkv__kkuv += '        np.random.shuffle(data)\n'
        if not is_overload_none(n_samples):
            bijkv__kkuv += '        data = data[:n_samples]\n'
        bijkv__kkuv += '        return data\n'
        bijkv__kkuv += '    else:\n'
        bijkv__kkuv += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        bijkv__kkuv += '        permutation = np.arange(dim0_global_size)\n'
        bijkv__kkuv += '        np.random.shuffle(permutation)\n'
        if not is_overload_none(n_samples):
            bijkv__kkuv += (
                '        n_samples = max(0, min(dim0_global_size, n_samples))\n'
                )
        else:
            bijkv__kkuv += '        n_samples = dim0_global_size\n'
        bijkv__kkuv += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        bijkv__kkuv += """        dim0_output_size = bodo.libs.distributed_api.get_node_portion(n_samples, bodo.get_size(), bodo.get_rank())
"""
        bijkv__kkuv += """        output = np.empty((dim0_output_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        bijkv__kkuv += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        bijkv__kkuv += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation), n_samples)
"""
        bijkv__kkuv += '        return output\n'
    else:
        bijkv__kkuv += """    output = bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
        if not is_overload_none(n_samples):
            bijkv__kkuv += """    local_n_samples = bodo.libs.distributed_api.get_node_portion(n_samples, bodo.get_size(), bodo.get_rank())
"""
            bijkv__kkuv += '    output = output[:local_n_samples]\n'
        bijkv__kkuv += '    return output\n'
    bufh__hcd = {}
    exec(bijkv__kkuv, {'np': np, 'bodo': bodo}, bufh__hcd)
    impl = bufh__hcd['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    hlk__qxhop = np.empty(sendcounts_nulls.sum(), np.uint8)
    vtsb__pmb = 0
    xac__ldn = 0
    for cjjg__spf in range(len(sendcounts)):
        xye__qdffm = sendcounts[cjjg__spf]
        iewp__sqtj = sendcounts_nulls[cjjg__spf]
        omfk__kmpen = hlk__qxhop[vtsb__pmb:vtsb__pmb + iewp__sqtj]
        for xafha__vwr in range(xye__qdffm):
            set_bit_to_arr(omfk__kmpen, xafha__vwr, get_bit_bitmap(
                null_bitmap_ptr, xac__ldn))
            xac__ldn += 1
        vtsb__pmb += iewp__sqtj
    return hlk__qxhop


def _bcast_dtype(data, root=MPI_ROOT):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    vghgh__zbjj = MPI.COMM_WORLD
    data = vghgh__zbjj.bcast(data, root)
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
    vgs__kra = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    jfo__luo = (0,) * vgs__kra

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        ejlwl__xaqzf = np.ascontiguousarray(data)
        elj__nhzr = data.ctypes
        qbtlz__dksah = jfo__luo
        if rank == MPI_ROOT:
            qbtlz__dksah = ejlwl__xaqzf.shape
        qbtlz__dksah = bcast_tuple(qbtlz__dksah)
        txios__fflqk = get_tuple_prod(qbtlz__dksah[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes,
            qbtlz__dksah[0])
        send_counts *= txios__fflqk
        blh__jqolo = send_counts[rank]
        bwtdh__qrgua = np.empty(blh__jqolo, dtype)
        sdama__nyl = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(elj__nhzr, send_counts.ctypes, sdama__nyl.ctypes,
            bwtdh__qrgua.ctypes, np.int32(blh__jqolo), np.int32(typ_val))
        return bwtdh__qrgua.reshape((-1,) + qbtlz__dksah[1:])
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
        gwy__nik = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], gwy__nik)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        qzjje__sufh = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=qzjje__sufh)
        lnfjz__ykhk = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(lnfjz__ykhk)
        return pd.Index(arr, name=qzjje__sufh)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        import pyarrow as pa
        qzjje__sufh = _get_name_value_for_type(dtype.name_typ)
        vvyu__gdjc = tuple(_get_name_value_for_type(t) for t in dtype.names_typ
            )
        zzfnr__idgy = tuple(get_value_for_type(t) for t in dtype.array_types)
        zzfnr__idgy = tuple(a.to_numpy(False) if isinstance(a, pa.Array) else
            a for a in zzfnr__idgy)
        val = pd.MultiIndex.from_arrays(zzfnr__idgy, names=vvyu__gdjc)
        val.name = qzjje__sufh
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        qzjje__sufh = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=qzjje__sufh)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        zzfnr__idgy = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({qzjje__sufh: arr for qzjje__sufh, arr in zip(
            dtype.columns, zzfnr__idgy)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    if isinstance(dtype, IntervalArrayType):
        lnfjz__ykhk = get_value_for_type(dtype.arr_type)
        return pd.arrays.IntervalArray([pd.Interval(lnfjz__ykhk[0],
            lnfjz__ykhk[0])])
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
        ignin__wyxrf = np.int32(numba_to_c_type(types.int32))
        awg__wzn = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            muwtg__uqc = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            muwtg__uqc = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        bijkv__kkuv = f"""def impl(
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
            recv_arr = {muwtg__uqc}(n_loc, n_loc_char)

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
        bufh__hcd = dict()
        exec(bijkv__kkuv, {'bodo': bodo, 'np': np, 'int32_typ_enum':
            ignin__wyxrf, 'char_typ_enum': awg__wzn, 'decode_if_dict_array':
            decode_if_dict_array}, bufh__hcd)
        impl = bufh__hcd['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        ignin__wyxrf = np.int32(numba_to_c_type(types.int32))
        awg__wzn = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            haj__ridr = bodo.libs.array_item_arr_ext.get_offsets(data)
            mrv__vre = bodo.libs.array_item_arr_ext.get_data(data)
            mrv__vre = mrv__vre[:haj__ridr[-1]]
            oieg__hpfzm = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            pelt__prik = bcast_scalar(len(data))
            vtxdv__mhnxs = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                vtxdv__mhnxs[i] = haj__ridr[i + 1] - haj__ridr[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                pelt__prik)
            sdama__nyl = bodo.ir.join.calc_disp(send_counts)
            fpj__tetsl = np.empty(n_pes, np.int32)
            if rank == 0:
                ngjsa__atyub = 0
                for i in range(n_pes):
                    vvyd__nvvp = 0
                    for zqd__ikmzr in range(send_counts[i]):
                        vvyd__nvvp += vtxdv__mhnxs[ngjsa__atyub]
                        ngjsa__atyub += 1
                    fpj__tetsl[i] = vvyd__nvvp
            bcast(fpj__tetsl)
            udey__nlbsc = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                udey__nlbsc[i] = send_counts[i] + 7 >> 3
            lzntb__qzrkq = bodo.ir.join.calc_disp(udey__nlbsc)
            blh__jqolo = send_counts[rank]
            unvx__mxqf = np.empty(blh__jqolo + 1, np_offset_type)
            bvd__hiir = bodo.libs.distributed_api.scatterv_impl(mrv__vre,
                fpj__tetsl)
            kdxg__xpn = blh__jqolo + 7 >> 3
            sjep__gvt = np.empty(kdxg__xpn, np.uint8)
            rub__vcjkk = np.empty(blh__jqolo, np.uint32)
            c_scatterv(vtxdv__mhnxs.ctypes, send_counts.ctypes, sdama__nyl.
                ctypes, rub__vcjkk.ctypes, np.int32(blh__jqolo), ignin__wyxrf)
            convert_len_arr_to_offset(rub__vcjkk.ctypes, unvx__mxqf.ctypes,
                blh__jqolo)
            oypkz__bfc = get_scatter_null_bytes_buff(oieg__hpfzm.ctypes,
                send_counts, udey__nlbsc)
            c_scatterv(oypkz__bfc.ctypes, udey__nlbsc.ctypes, lzntb__qzrkq.
                ctypes, sjep__gvt.ctypes, np.int32(kdxg__xpn), awg__wzn)
            return bodo.libs.array_item_arr_ext.init_array_item_array(
                blh__jqolo, bvd__hiir, unvx__mxqf, sjep__gvt)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        awg__wzn = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            ziag__xuqo = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            ziag__xuqo = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            ziag__xuqo = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            ziag__xuqo = (bodo.hiframes.datetime_date_ext.
                init_datetime_date_array)

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            ejlwl__xaqzf = data._data
            ctdq__egifm = data._null_bitmap
            zul__tksvr = len(ejlwl__xaqzf)
            wny__dtpop = _scatterv_np(ejlwl__xaqzf, send_counts)
            pelt__prik = bcast_scalar(zul__tksvr)
            xnk__asqzq = len(wny__dtpop) + 7 >> 3
            dfalj__mkl = np.empty(xnk__asqzq, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                pelt__prik)
            udey__nlbsc = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                udey__nlbsc[i] = send_counts[i] + 7 >> 3
            lzntb__qzrkq = bodo.ir.join.calc_disp(udey__nlbsc)
            oypkz__bfc = get_scatter_null_bytes_buff(ctdq__egifm.ctypes,
                send_counts, udey__nlbsc)
            c_scatterv(oypkz__bfc.ctypes, udey__nlbsc.ctypes, lzntb__qzrkq.
                ctypes, dfalj__mkl.ctypes, np.int32(xnk__asqzq), awg__wzn)
            return ziag__xuqo(wny__dtpop, dfalj__mkl)
        return scatterv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, send_counts=None, warn_if_dist=True):
            ale__mzjp = bodo.libs.distributed_api.scatterv_impl(data._left,
                send_counts)
            gmpw__qce = bodo.libs.distributed_api.scatterv_impl(data._right,
                send_counts)
            return bodo.libs.interval_arr_ext.init_interval_array(ale__mzjp,
                gmpw__qce)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            axqz__eichr = data._start
            niv__rws = data._stop
            gct__dlyxw = data._step
            qzjje__sufh = data._name
            qzjje__sufh = bcast_scalar(qzjje__sufh)
            axqz__eichr = bcast_scalar(axqz__eichr)
            niv__rws = bcast_scalar(niv__rws)
            gct__dlyxw = bcast_scalar(gct__dlyxw)
            upmg__oiqzz = bodo.libs.array_kernels.calc_nitems(axqz__eichr,
                niv__rws, gct__dlyxw)
            chunk_start = bodo.libs.distributed_api.get_start(upmg__oiqzz,
                n_pes, rank)
            hwfvr__zrpk = bodo.libs.distributed_api.get_node_portion(
                upmg__oiqzz, n_pes, rank)
            ksq__pnl = axqz__eichr + gct__dlyxw * chunk_start
            roo__esxnd = axqz__eichr + gct__dlyxw * (chunk_start + hwfvr__zrpk)
            roo__esxnd = min(roo__esxnd, niv__rws)
            return bodo.hiframes.pd_index_ext.init_range_index(ksq__pnl,
                roo__esxnd, gct__dlyxw, qzjje__sufh)
        return impl_range_index
    if isinstance(data, bodo.hiframes.pd_index_ext.PeriodIndexType):
        wanv__zrb = data.freq

        def impl_period_index(data, send_counts=None, warn_if_dist=True):
            ejlwl__xaqzf = data._data
            qzjje__sufh = data._name
            qzjje__sufh = bcast_scalar(qzjje__sufh)
            arr = bodo.libs.distributed_api.scatterv_impl(ejlwl__xaqzf,
                send_counts)
            return bodo.hiframes.pd_index_ext.init_period_index(arr,
                qzjje__sufh, wanv__zrb)
        return impl_period_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            ejlwl__xaqzf = data._data
            qzjje__sufh = data._name
            qzjje__sufh = bcast_scalar(qzjje__sufh)
            arr = bodo.libs.distributed_api.scatterv_impl(ejlwl__xaqzf,
                send_counts)
            return bodo.utils.conversion.index_from_array(arr, qzjje__sufh)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            imm__bxwb = bodo.libs.distributed_api.scatterv_impl(data._data,
                send_counts)
            qzjje__sufh = bcast_scalar(data._name)
            vvyu__gdjc = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(imm__bxwb,
                vvyu__gdjc, qzjje__sufh)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            qzjje__sufh = bodo.hiframes.pd_series_ext.get_series_name(data)
            jiky__svi = bcast_scalar(qzjje__sufh)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            swur__zapf = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                swur__zapf, jiky__svi)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        tjif__fyxwf = len(data.columns)
        iqzq__mxqm = ColNamesMetaType(data.columns)
        bijkv__kkuv = (
            'def impl_df(data, send_counts=None, warn_if_dist=True):\n')
        if data.is_table_format:
            bijkv__kkuv += (
                '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            bijkv__kkuv += """  g_table = bodo.libs.distributed_api.scatterv_impl(table, send_counts)
"""
            mnsx__ytgex = 'g_table'
        else:
            for i in range(tjif__fyxwf):
                bijkv__kkuv += f"""  data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
                bijkv__kkuv += f"""  g_data_{i} = bodo.libs.distributed_api.scatterv_impl(data_{i}, send_counts)
"""
            mnsx__ytgex = ', '.join(f'g_data_{i}' for i in range(tjif__fyxwf))
        bijkv__kkuv += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        bijkv__kkuv += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        bijkv__kkuv += f"""  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({mnsx__ytgex},), g_index, __col_name_meta_scaterv_impl)
"""
        bufh__hcd = {}
        exec(bijkv__kkuv, {'bodo': bodo, '__col_name_meta_scaterv_impl':
            iqzq__mxqm}, bufh__hcd)
        aky__axzn = bufh__hcd['impl_df']
        return aky__axzn
    if isinstance(data, bodo.TableType):
        bijkv__kkuv = (
            'def impl_table(data, send_counts=None, warn_if_dist=True):\n')
        bijkv__kkuv += '  T = data\n'
        bijkv__kkuv += '  T2 = init_table(T, False)\n'
        bijkv__kkuv += '  l = 0\n'
        dtf__pzcu = {}
        for chnnj__obrzr in data.type_to_blk.values():
            dtf__pzcu[f'arr_inds_{chnnj__obrzr}'] = np.array(data.
                block_to_arr_ind[chnnj__obrzr], dtype=np.int64)
            bijkv__kkuv += (
                f'  arr_list_{chnnj__obrzr} = get_table_block(T, {chnnj__obrzr})\n'
                )
            bijkv__kkuv += f"""  out_arr_list_{chnnj__obrzr} = alloc_list_like(arr_list_{chnnj__obrzr}, len(arr_list_{chnnj__obrzr}), False)
"""
            bijkv__kkuv += f'  for i in range(len(arr_list_{chnnj__obrzr})):\n'
            bijkv__kkuv += (
                f'    arr_ind_{chnnj__obrzr} = arr_inds_{chnnj__obrzr}[i]\n')
            bijkv__kkuv += f"""    ensure_column_unboxed(T, arr_list_{chnnj__obrzr}, i, arr_ind_{chnnj__obrzr})
"""
            bijkv__kkuv += f"""    out_arr_{chnnj__obrzr} = bodo.libs.distributed_api.scatterv_impl(arr_list_{chnnj__obrzr}[i], send_counts)
"""
            bijkv__kkuv += (
                f'    out_arr_list_{chnnj__obrzr}[i] = out_arr_{chnnj__obrzr}\n'
                )
            bijkv__kkuv += f'    l = len(out_arr_{chnnj__obrzr})\n'
            bijkv__kkuv += f"""  T2 = set_table_block(T2, out_arr_list_{chnnj__obrzr}, {chnnj__obrzr})
"""
        bijkv__kkuv += f'  T2 = set_table_len(T2, l)\n'
        bijkv__kkuv += f'  return T2\n'
        dtf__pzcu.update({'bodo': bodo, 'init_table': bodo.hiframes.table.
            init_table, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like})
        bufh__hcd = {}
        exec(bijkv__kkuv, dtf__pzcu, bufh__hcd)
        return bufh__hcd['impl_table']
    if data == bodo.dict_str_arr_type:

        def impl_dict_arr(data, send_counts=None, warn_if_dist=True):
            if bodo.get_rank() == 0:
                udmfh__cnml = data._data
                bodo.libs.distributed_api.bcast_scalar(len(udmfh__cnml))
                bodo.libs.distributed_api.bcast_scalar(np.int64(bodo.libs.
                    str_arr_ext.num_total_chars(udmfh__cnml)))
            else:
                lul__ess = bodo.libs.distributed_api.bcast_scalar(0)
                vik__azs = bodo.libs.distributed_api.bcast_scalar(0)
                udmfh__cnml = bodo.libs.str_arr_ext.pre_alloc_string_array(
                    lul__ess, vik__azs)
            bodo.libs.distributed_api.bcast(udmfh__cnml)
            trgvj__dim = bodo.libs.distributed_api.scatterv_impl(data.
                _indices, send_counts)
            return bodo.libs.dict_arr_ext.init_dict_arr(udmfh__cnml,
                trgvj__dim, True)
        return impl_dict_arr
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            cgs__nvo = bodo.libs.distributed_api.scatterv_impl(data.codes,
                send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                cgs__nvo, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        bijkv__kkuv = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        bijkv__kkuv += '  return ({}{})\n'.format(', '.join(
            f'bodo.libs.distributed_api.scatterv_impl(data[{i}], send_counts)'
             for i in range(len(data))), ',' if len(data) > 0 else '')
        bufh__hcd = {}
        exec(bijkv__kkuv, {'bodo': bodo}, bufh__hcd)
        vgvy__cyyp = bufh__hcd['impl_tuple']
        return vgvy__cyyp
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
        dns__qwgz = np.int32(numba_to_c_type(offset_type))
        awg__wzn = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data, root=MPI_ROOT):
            data = decode_if_dict_array(data)
            blh__jqolo = len(data)
            shazh__ubt = num_total_chars(data)
            assert blh__jqolo < INT_MAX
            assert shazh__ubt < INT_MAX
            jvtab__wxe = get_offset_ptr(data)
            elj__nhzr = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            iewp__sqtj = blh__jqolo + 7 >> 3
            c_bcast(jvtab__wxe, np.int32(blh__jqolo + 1), dns__qwgz, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(elj__nhzr, np.int32(shazh__ubt), awg__wzn, np.array([-1
                ]).ctypes, 0, np.int32(root))
            c_bcast(null_bitmap_ptr, np.int32(iewp__sqtj), awg__wzn, np.
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
        awg__wzn = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != root:
                ufu__voi = 0
                wjqva__nox = np.empty(0, np.uint8).ctypes
            else:
                wjqva__nox, ufu__voi = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            ufu__voi = bodo.libs.distributed_api.bcast_scalar(ufu__voi, root)
            if rank != root:
                lnkxp__zmq = np.empty(ufu__voi + 1, np.uint8)
                lnkxp__zmq[ufu__voi] = 0
                wjqva__nox = lnkxp__zmq.ctypes
            c_bcast(wjqva__nox, np.int32(ufu__voi), awg__wzn, np.array([-1]
                ).ctypes, 0, np.int32(root))
            return bodo.libs.str_arr_ext.decode_utf8(wjqva__nox, ufu__voi)
        return impl_str
    typ_val = numba_to_c_type(val)
    bijkv__kkuv = f"""def bcast_scalar_impl(val, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({typ_val}), np.array([-1]).ctypes, 0, np.int32(root))
  return send[0]
"""
    dtype = numba.np.numpy_support.as_dtype(val)
    bufh__hcd = {}
    exec(bijkv__kkuv, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, bufh__hcd)
    hrz__fqb = bufh__hcd['bcast_scalar_impl']
    return hrz__fqb


@numba.generated_jit(nopython=True)
def bcast_tuple(val, root=MPI_ROOT):
    assert isinstance(val, types.BaseTuple)
    lau__fvq = len(val)
    bijkv__kkuv = f'def bcast_tuple_impl(val, root={MPI_ROOT}):\n'
    bijkv__kkuv += '  return ({}{})'.format(','.join(
        'bcast_scalar(val[{}], root)'.format(i) for i in range(lau__fvq)), 
        ',' if lau__fvq else '')
    bufh__hcd = {}
    exec(bijkv__kkuv, {'bcast_scalar': bcast_scalar}, bufh__hcd)
    utxdw__leyxq = bufh__hcd['bcast_tuple_impl']
    return utxdw__leyxq


def prealloc_str_for_bcast(arr, root=MPI_ROOT):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr, root=MPI_ROOT):
    if arr == string_array_type:

        def prealloc_impl(arr, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            blh__jqolo = bcast_scalar(len(arr), root)
            nscxe__amcqt = bcast_scalar(np.int64(num_total_chars(arr)), root)
            if rank != root:
                arr = pre_alloc_string_array(blh__jqolo, nscxe__amcqt)
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
            ksq__pnl = max(arr_start, slice_index.start) - arr_start
            roo__esxnd = max(slice_index.stop - arr_start, 0)
            return slice(ksq__pnl, roo__esxnd)
    else:

        def impl(idx, arr_start, total_len):
            slice_index = numba.cpython.unicode._normalize_slice(idx, total_len
                )
            axqz__eichr = slice_index.start
            gct__dlyxw = slice_index.step
            swxj__dad = (0 if gct__dlyxw == 1 or axqz__eichr > arr_start else
                abs(gct__dlyxw - arr_start % gct__dlyxw) % gct__dlyxw)
            ksq__pnl = max(arr_start, slice_index.start
                ) - arr_start + swxj__dad
            roo__esxnd = max(slice_index.stop - arr_start, 0)
            return slice(ksq__pnl, roo__esxnd, gct__dlyxw)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        dvd__hzq = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[dvd__hzq])
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
        lemv__rxxhg = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        awg__wzn = np.int32(numba_to_c_type(types.uint8))
        tkal__avvew = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            arr = decode_if_dict_array(arr)
            ind = ind % total_len
            root = np.int32(0)
            mushh__eijv = np.int32(10)
            tag = np.int32(11)
            cdz__hplh = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                wfrds__codrs = arr._data
                ajqrg__lwprm = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    wfrds__codrs, ind)
                doqcx__vuplp = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    wfrds__codrs, ind + 1)
                length = doqcx__vuplp - ajqrg__lwprm
                zos__rwp = wfrds__codrs[ind]
                cdz__hplh[0] = length
                isend(cdz__hplh, np.int32(1), root, mushh__eijv, True)
                isend(zos__rwp, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                tkal__avvew, lemv__rxxhg, 0, 1)
            lul__ess = 0
            if rank == root:
                lul__ess = recv(np.int64, ANY_SOURCE, mushh__eijv)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    tkal__avvew, lemv__rxxhg, lul__ess, 1)
                elj__nhzr = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(elj__nhzr, np.int32(lul__ess), awg__wzn, ANY_SOURCE, tag)
            dummy_use(cdz__hplh)
            lul__ess = bcast_scalar(lul__ess)
            dummy_use(arr)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    tkal__avvew, lemv__rxxhg, lul__ess, 1)
            elj__nhzr = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(elj__nhzr, np.int32(lul__ess), awg__wzn, np.array([-1])
                .ctypes, 0, np.int32(root))
            val = transform_str_getitem_output(val, lul__ess)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        zwt__ojqa = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, zwt__ojqa)
            if arr_start <= ind < arr_start + len(arr):
                cgs__nvo = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = cgs__nvo[ind - arr_start]
                send_arr = np.full(1, data, zwt__ojqa)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = zwt__ojqa(-1)
            if rank == root:
                val = recv(zwt__ojqa, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            wtt__xzes = arr.dtype.categories[max(val, 0)]
            return wtt__xzes
        return cat_getitem_impl
    khz__huw = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, khz__huw)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, khz__huw)[0]
        if rank == root:
            val = recv(khz__huw, ANY_SOURCE, tag)
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
    hywl__nqyx = get_type_enum(out_data)
    assert typ_enum == hywl__nqyx
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
    bijkv__kkuv = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        bijkv__kkuv += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    bijkv__kkuv += '  return\n'
    bufh__hcd = {}
    exec(bijkv__kkuv, {'alltoallv': alltoallv}, bufh__hcd)
    jdb__pmtg = bufh__hcd['f']
    return jdb__pmtg


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    axqz__eichr = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return axqz__eichr, count


@numba.njit
def get_start(total_size, pes, rank):
    utbo__isoe = total_size % pes
    umpld__ocza = (total_size - utbo__isoe) // pes
    return rank * umpld__ocza + min(rank, utbo__isoe)


@numba.njit
def get_end(total_size, pes, rank):
    utbo__isoe = total_size % pes
    umpld__ocza = (total_size - utbo__isoe) // pes
    return (rank + 1) * umpld__ocza + min(rank + 1, utbo__isoe)


@numba.njit
def get_node_portion(total_size, pes, rank):
    utbo__isoe = total_size % pes
    umpld__ocza = (total_size - utbo__isoe) // pes
    if rank < utbo__isoe:
        return umpld__ocza + 1
    else:
        return umpld__ocza


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    ozdgd__abip = in_arr.dtype(0)
    rhay__lzrg = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        vvyd__nvvp = ozdgd__abip
        for tti__foo in np.nditer(in_arr):
            vvyd__nvvp += tti__foo.item()
        ypqh__uvxax = dist_exscan(vvyd__nvvp, rhay__lzrg)
        for i in range(in_arr.size):
            ypqh__uvxax += in_arr[i]
            out_arr[i] = ypqh__uvxax
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    aqsam__zoi = in_arr.dtype(1)
    rhay__lzrg = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        vvyd__nvvp = aqsam__zoi
        for tti__foo in np.nditer(in_arr):
            vvyd__nvvp *= tti__foo.item()
        ypqh__uvxax = dist_exscan(vvyd__nvvp, rhay__lzrg)
        if get_rank() == 0:
            ypqh__uvxax = aqsam__zoi
        for i in range(in_arr.size):
            ypqh__uvxax *= in_arr[i]
            out_arr[i] = ypqh__uvxax
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        aqsam__zoi = np.finfo(in_arr.dtype(1).dtype).max
    else:
        aqsam__zoi = np.iinfo(in_arr.dtype(1).dtype).max
    rhay__lzrg = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        vvyd__nvvp = aqsam__zoi
        for tti__foo in np.nditer(in_arr):
            vvyd__nvvp = min(vvyd__nvvp, tti__foo.item())
        ypqh__uvxax = dist_exscan(vvyd__nvvp, rhay__lzrg)
        if get_rank() == 0:
            ypqh__uvxax = aqsam__zoi
        for i in range(in_arr.size):
            ypqh__uvxax = min(ypqh__uvxax, in_arr[i])
            out_arr[i] = ypqh__uvxax
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        aqsam__zoi = np.finfo(in_arr.dtype(1).dtype).min
    else:
        aqsam__zoi = np.iinfo(in_arr.dtype(1).dtype).min
    aqsam__zoi = in_arr.dtype(1)
    rhay__lzrg = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        vvyd__nvvp = aqsam__zoi
        for tti__foo in np.nditer(in_arr):
            vvyd__nvvp = max(vvyd__nvvp, tti__foo.item())
        ypqh__uvxax = dist_exscan(vvyd__nvvp, rhay__lzrg)
        if get_rank() == 0:
            ypqh__uvxax = aqsam__zoi
        for i in range(in_arr.size):
            ypqh__uvxax = max(ypqh__uvxax, in_arr[i])
            out_arr[i] = ypqh__uvxax
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    pyf__ovg = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), pyf__ovg)


def dist_return(A):
    return A


def rep_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    ftm__knvva = args[0]
    if equiv_set.has_shape(ftm__knvva):
        return ArrayAnalysis.AnalyzeResult(shape=ftm__knvva, pre=[])
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
    dfg__joq = '(' + ' or '.join(['False'] + [f'len(args[{i}]) != 0' for i,
        utqn__gllt in enumerate(args) if is_array_typ(utqn__gllt) or
        isinstance(utqn__gllt, bodo.hiframes.pd_dataframe_ext.DataFrameType)]
        ) + ')'
    bijkv__kkuv = f"""def impl(*args):
    if {dfg__joq} or bodo.get_rank() == 0:
        print(*args)"""
    bufh__hcd = {}
    exec(bijkv__kkuv, globals(), bufh__hcd)
    impl = bufh__hcd['impl']
    return impl


_wait = types.ExternalFunction('dist_wait', types.void(mpi_req_numba_type,
    types.bool_))


@numba.generated_jit(nopython=True)
def wait(req, cond=True):
    if isinstance(req, types.BaseTuple):
        count = len(req.types)
        sfku__qvc = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        bijkv__kkuv = 'def f(req, cond=True):\n'
        bijkv__kkuv += f'  return {sfku__qvc}\n'
        bufh__hcd = {}
        exec(bijkv__kkuv, {'_wait': _wait}, bufh__hcd)
        impl = bufh__hcd['f']
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
        utbo__isoe = 1
        for a in t:
            utbo__isoe *= a
        return utbo__isoe
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    glze__oljj = np.ascontiguousarray(in_arr)
    abq__obg = get_tuple_prod(glze__oljj.shape[1:])
    sch__lqfz = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        axh__wlxx = np.array(dest_ranks, dtype=np.int32)
    else:
        axh__wlxx = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, glze__oljj.ctypes, new_dim0_global_len,
        len(in_arr), dtype_size * sch__lqfz, dtype_size * abq__obg, len(
        axh__wlxx), axh__wlxx.ctypes)
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
    vxal__qjly = np.ascontiguousarray(rhs)
    uhjvk__vlte = get_tuple_prod(vxal__qjly.shape[1:])
    wwi__chkp = dtype_size * uhjvk__vlte
    permutation_array_index(lhs.ctypes, lhs_len, wwi__chkp, vxal__qjly.
        ctypes, vxal__qjly.shape[0], p.ctypes, p_len, n_samples)
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
        bijkv__kkuv = (
            f"""def bcast_scalar_impl(data, comm_ranks, nranks, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({{}}), comm_ranks,ctypes, np.int32({{}}), np.int32(root))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        bufh__hcd = {}
        exec(bijkv__kkuv, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast,
            'dtype': dtype}, bufh__hcd)
        hrz__fqb = bufh__hcd['bcast_scalar_impl']
        return hrz__fqb
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: _bcast_np(data,
            comm_ranks, nranks, root)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        tjif__fyxwf = len(data.columns)
        mnsx__ytgex = ', '.join('g_data_{}'.format(i) for i in range(
            tjif__fyxwf))
        bywil__stxid = ColNamesMetaType(data.columns)
        bijkv__kkuv = (
            f'def impl_df(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        for i in range(tjif__fyxwf):
            bijkv__kkuv += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            bijkv__kkuv += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks, root)
"""
                .format(i, i))
        bijkv__kkuv += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        bijkv__kkuv += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks, root)
"""
        bijkv__kkuv += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, __col_name_meta_value_bcast_comm)
"""
            .format(mnsx__ytgex))
        bufh__hcd = {}
        exec(bijkv__kkuv, {'bodo': bodo, '__col_name_meta_value_bcast_comm':
            bywil__stxid}, bufh__hcd)
        aky__axzn = bufh__hcd['impl_df']
        return aky__axzn
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            axqz__eichr = data._start
            niv__rws = data._stop
            gct__dlyxw = data._step
            qzjje__sufh = data._name
            qzjje__sufh = bcast_scalar(qzjje__sufh, root)
            axqz__eichr = bcast_scalar(axqz__eichr, root)
            niv__rws = bcast_scalar(niv__rws, root)
            gct__dlyxw = bcast_scalar(gct__dlyxw, root)
            upmg__oiqzz = bodo.libs.array_kernels.calc_nitems(axqz__eichr,
                niv__rws, gct__dlyxw)
            chunk_start = bodo.libs.distributed_api.get_start(upmg__oiqzz,
                n_pes, rank)
            hwfvr__zrpk = bodo.libs.distributed_api.get_node_portion(
                upmg__oiqzz, n_pes, rank)
            ksq__pnl = axqz__eichr + gct__dlyxw * chunk_start
            roo__esxnd = axqz__eichr + gct__dlyxw * (chunk_start + hwfvr__zrpk)
            roo__esxnd = min(roo__esxnd, niv__rws)
            return bodo.hiframes.pd_index_ext.init_range_index(ksq__pnl,
                roo__esxnd, gct__dlyxw, qzjje__sufh)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks, root=MPI_ROOT):
            ejlwl__xaqzf = data._data
            qzjje__sufh = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(ejlwl__xaqzf,
                comm_ranks, nranks, root)
            return bodo.utils.conversion.index_from_array(arr, qzjje__sufh)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            qzjje__sufh = bodo.hiframes.pd_series_ext.get_series_name(data)
            jiky__svi = bodo.libs.distributed_api.bcast_comm_impl(qzjje__sufh,
                comm_ranks, nranks, root)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks, root)
            swur__zapf = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                swur__zapf, jiky__svi)
        return impl_series
    if isinstance(data, types.BaseTuple):
        bijkv__kkuv = (
            f'def impl_tuple(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        bijkv__kkuv += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks, root)'.format(i) for
            i in range(len(data))), ',' if len(data) > 0 else '')
        bufh__hcd = {}
        exec(bijkv__kkuv, {'bcast_comm_impl': bcast_comm_impl}, bufh__hcd)
        vgvy__cyyp = bufh__hcd['impl_tuple']
        return vgvy__cyyp
    if data is types.none:
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks, root=MPI_ROOT):
    typ_val = numba_to_c_type(data.dtype)
    vgs__kra = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    jfo__luo = (0,) * vgs__kra

    def bcast_arr_impl(data, comm_ranks, nranks, root=MPI_ROOT):
        rank = bodo.libs.distributed_api.get_rank()
        ejlwl__xaqzf = np.ascontiguousarray(data)
        elj__nhzr = data.ctypes
        qbtlz__dksah = jfo__luo
        if rank == root:
            qbtlz__dksah = ejlwl__xaqzf.shape
        qbtlz__dksah = bcast_tuple(qbtlz__dksah, root)
        txios__fflqk = get_tuple_prod(qbtlz__dksah[1:])
        send_counts = qbtlz__dksah[0] * txios__fflqk
        bwtdh__qrgua = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(elj__nhzr, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return data
        else:
            c_bcast(bwtdh__qrgua.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return bwtdh__qrgua.reshape((-1,) + qbtlz__dksah[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        vghgh__zbjj = MPI.COMM_WORLD
        rhdz__hpuz = MPI.Get_processor_name()
        mukm__fgej = vghgh__zbjj.allgather(rhdz__hpuz)
        node_ranks = defaultdict(list)
        for i, zrm__sse in enumerate(mukm__fgej):
            node_ranks[zrm__sse].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    vghgh__zbjj = MPI.COMM_WORLD
    xrzn__dzwnv = vghgh__zbjj.Get_group()
    utvl__iydzy = xrzn__dzwnv.Incl(comm_ranks)
    apuk__biiyz = vghgh__zbjj.Create_group(utvl__iydzy)
    return apuk__biiyz


def get_nodes_first_ranks():
    nwof__nhs = get_host_ranks()
    return np.array([kef__ifvdb[0] for kef__ifvdb in nwof__nhs.values()],
        dtype='int32')


def get_num_nodes():
    return len(get_host_ranks())
