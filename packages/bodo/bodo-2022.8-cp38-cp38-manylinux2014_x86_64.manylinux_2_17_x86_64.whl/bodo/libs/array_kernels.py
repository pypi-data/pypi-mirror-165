"""
Implements array kernels such as median and quantile.
"""
import hashlib
import inspect
import math
import operator
import re
import warnings
from math import sqrt
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types, typing
from numba.core.imputils import lower_builtin
from numba.core.ir_utils import find_const, guard
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import overload, overload_attribute, register_jitable
from numba.np.arrayobj import make_array
from numba.np.numpy_support import as_dtype
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, init_categorical_array
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.hiframes.time_ext import TimeArrayType
from bodo.libs import quantile_alg
from bodo.libs.array import arr_info_list_to_table, array_to_info, convert_local_dictionary_to_global, delete_info_decref_array, delete_table, delete_table_decref_arrays, drop_duplicates_table, info_from_table, info_to_array, sample_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, offset_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import DictionaryArrayType, init_dict_arr
from bodo.libs.distributed_api import Reduce_Type
from bodo.libs.int_arr_ext import IntegerArrayType, alloc_int_array
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType
from bodo.libs.str_arr_ext import pre_alloc_string_array, str_arr_set_na, string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, check_unsupported_args, decode_if_dict_array, element_type, find_common_np_dtype, get_overload_const_bool, get_overload_const_list, get_overload_const_str, is_bin_arr_type, is_overload_constant_bool, is_overload_constant_str, is_overload_none, is_overload_true, is_str_arr_type, raise_bodo_error, to_str_arr_if_dict_array
from bodo.utils.utils import build_set_seen_na, check_and_propagate_cpp_exception, numba_to_c_type, unliteral_all
ll.add_symbol('quantile_sequential', quantile_alg.quantile_sequential)
ll.add_symbol('quantile_parallel', quantile_alg.quantile_parallel)
MPI_ROOT = 0
sum_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value)
max_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Max.value)
min_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Min.value)


def isna(arr, i):
    return False


@overload(isna)
def overload_isna(arr, i):
    i = types.unliteral(i)
    if arr == string_array_type:
        return lambda arr, i: bodo.libs.str_arr_ext.str_arr_is_na(arr, i)
    if isinstance(arr, (IntegerArrayType, DecimalArrayType, TimeArrayType)
        ) or arr in (boolean_array, datetime_date_array_type,
        datetime_timedelta_array_type, string_array_split_view_type):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr
            ._null_bitmap, i)
    if isinstance(arr, ArrayItemArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr), i)
    if isinstance(arr, StructArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.struct_arr_ext.get_null_bitmap(arr), i)
    if isinstance(arr, TupleArrayType):
        return lambda arr, i: bodo.libs.array_kernels.isna(arr._data, i)
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return lambda arr, i: arr.codes[i] == -1
    if arr == bodo.binary_array_type:
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr._data), i)
    if isinstance(arr, types.List):
        if arr.dtype == types.none:
            return lambda arr, i: True
        elif isinstance(arr.dtype, types.optional):
            return lambda arr, i: arr[i] is None
        else:
            return lambda arr, i: False
    if isinstance(arr, bodo.NullableTupleType):
        return lambda arr, i: arr._null_values[i]
    if isinstance(arr, DictionaryArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr
            ._indices._null_bitmap, i) or bodo.libs.array_kernels.isna(arr.
            _data, arr._indices[i])
    if isinstance(arr, DatetimeArrayType):
        return lambda arr, i: np.isnat(arr._data[i])
    assert isinstance(arr, types.Array), f'Invalid array type in isna(): {arr}'
    dtype = arr.dtype
    if isinstance(dtype, types.Float):
        return lambda arr, i: np.isnan(arr[i])
    if isinstance(dtype, (types.NPDatetime, types.NPTimedelta)):
        return lambda arr, i: np.isnat(arr[i])
    return lambda arr, i: False


def setna(arr, ind, int_nan_const=0):
    arr[ind] = np.nan


@overload(setna, no_unliteral=True)
def setna_overload(arr, ind, int_nan_const=0):
    if isinstance(arr.dtype, types.Float):
        return setna
    if isinstance(arr.dtype, (types.NPDatetime, types.NPTimedelta)):
        qxvqk__rbgkz = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = qxvqk__rbgkz
        return _setnan_impl
    if isinstance(arr, DatetimeArrayType):
        qxvqk__rbgkz = bodo.datetime64ns('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr._data[ind] = qxvqk__rbgkz
        return _setnan_impl
    if arr == string_array_type:

        def impl(arr, ind, int_nan_const=0):
            arr[ind] = ''
            str_arr_set_na(arr, ind)
        return impl
    if isinstance(arr, DictionaryArrayType):
        return lambda arr, ind, int_nan_const=0: bodo.libs.array_kernels.setna(
            arr._indices, ind)
    if arr == boolean_array:

        def impl(arr, ind, int_nan_const=0):
            arr[ind] = False
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)):
        return (lambda arr, ind, int_nan_const=0: bodo.libs.int_arr_ext.
            set_bit_to_arr(arr._null_bitmap, ind, 0))
    if arr == bodo.binary_array_type:

        def impl_binary_arr(arr, ind, int_nan_const=0):
            tcvn__upol = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            tcvn__upol[ind + 1] = tcvn__upol[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            tcvn__upol = bodo.libs.array_item_arr_ext.get_offsets(arr)
            tcvn__upol[ind + 1] = tcvn__upol[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr), ind, 0)
        return impl_arr_item
    if isinstance(arr, bodo.libs.struct_arr_ext.StructArrayType):

        def impl(arr, ind, int_nan_const=0):
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.struct_arr_ext.
                get_null_bitmap(arr), ind, 0)
            data = bodo.libs.struct_arr_ext.get_data(arr)
            setna_tup(data, ind)
        return impl
    if isinstance(arr, TupleArrayType):

        def impl(arr, ind, int_nan_const=0):
            bodo.libs.array_kernels.setna(arr._data, ind)
        return impl
    if arr.dtype == types.bool_:

        def b_set(arr, ind, int_nan_const=0):
            arr[ind] = False
        return b_set
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):

        def setna_cat(arr, ind, int_nan_const=0):
            arr.codes[ind] = -1
        return setna_cat
    if isinstance(arr.dtype, types.Integer):

        def setna_int(arr, ind, int_nan_const=0):
            arr[ind] = int_nan_const
        return setna_int
    if arr == datetime_date_array_type:

        def setna_datetime_date(arr, ind, int_nan_const=0):
            arr._data[ind] = (1970 << 32) + (1 << 16) + 1
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_datetime_date
    if arr == datetime_timedelta_array_type:

        def setna_datetime_timedelta(arr, ind, int_nan_const=0):
            bodo.libs.array_kernels.setna(arr._days_data, ind)
            bodo.libs.array_kernels.setna(arr._seconds_data, ind)
            bodo.libs.array_kernels.setna(arr._microseconds_data, ind)
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_datetime_timedelta
    return lambda arr, ind, int_nan_const=0: None


def setna_tup(arr_tup, ind, int_nan_const=0):
    for arr in arr_tup:
        arr[ind] = np.nan


@overload(setna_tup, no_unliteral=True)
def overload_setna_tup(arr_tup, ind, int_nan_const=0):
    ccran__kkuml = arr_tup.count
    dkuc__ksmky = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(ccran__kkuml):
        dkuc__ksmky += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    dkuc__ksmky += '  return\n'
    tpxxu__nsdw = {}
    exec(dkuc__ksmky, {'setna': setna}, tpxxu__nsdw)
    impl = tpxxu__nsdw['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        etqfc__hmcc = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(etqfc__hmcc.start, etqfc__hmcc.stop, etqfc__hmcc.step):
            setna(arr, i)
    return impl


@numba.generated_jit
def first_last_valid_index(arr, index_arr, is_first=True, parallel=False):
    is_first = get_overload_const_bool(is_first)
    if is_first:
        dmv__tfeo = 'n'
        ejaq__gng = 'n_pes'
        ctf__rpfo = 'min_op'
    else:
        dmv__tfeo = 'n-1, -1, -1'
        ejaq__gng = '-1'
        ctf__rpfo = 'max_op'
    dkuc__ksmky = f"""def impl(arr, index_arr, is_first=True, parallel=False):
    n = len(arr)
    index_value = index_arr[0]
    has_valid = False
    loc_valid_rank = -1
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        loc_valid_rank = {ejaq__gng}
    for i in range({dmv__tfeo}):
        if not isna(arr, i):
            if parallel:
                loc_valid_rank = rank
            index_value = index_arr[i]
            has_valid = True
            break
    if parallel:
        possible_valid_rank = np.int32(bodo.libs.distributed_api.dist_reduce(loc_valid_rank, {ctf__rpfo}))
        if possible_valid_rank != {ejaq__gng}:
            has_valid = True
            index_value = bodo.libs.distributed_api.bcast_scalar(index_value, possible_valid_rank)
    return has_valid, box_if_dt64(index_value)

    """
    tpxxu__nsdw = {}
    exec(dkuc__ksmky, {'np': np, 'bodo': bodo, 'isna': isna, 'max_op':
        max_op, 'min_op': min_op, 'box_if_dt64': bodo.utils.conversion.
        box_if_dt64}, tpxxu__nsdw)
    impl = tpxxu__nsdw['impl']
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    ryohp__lmx = array_to_info(arr)
    _median_series_computation(res, ryohp__lmx, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(ryohp__lmx)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    ryohp__lmx = array_to_info(arr)
    _autocorr_series_computation(res, ryohp__lmx, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(ryohp__lmx)


@numba.njit
def autocorr(arr, lag=1, parallel=False):
    res = np.empty(1, types.float64)
    autocorr_series_computation(res.ctypes, arr, lag, parallel)
    return res[0]


ll.add_symbol('compute_series_monotonicity', quantile_alg.
    compute_series_monotonicity)
_compute_series_monotonicity = types.ExternalFunction(
    'compute_series_monotonicity', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def series_monotonicity_call(res, arr, inc_dec, is_parallel):
    ryohp__lmx = array_to_info(arr)
    _compute_series_monotonicity(res, ryohp__lmx, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(ryohp__lmx)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    mookd__zbijc = res[0] > 0.5
    return mookd__zbijc


@numba.generated_jit(nopython=True)
def get_valid_entries_from_date_offset(index_arr, offset, initial_date,
    is_last, is_parallel=False):
    if get_overload_const_bool(is_last):
        efh__deeg = '-'
        bmam__nsnbv = 'index_arr[0] > threshhold_date'
        dmv__tfeo = '1, n+1'
        hrvyt__jlxxw = 'index_arr[-i] <= threshhold_date'
        scjm__dclwv = 'i - 1'
    else:
        efh__deeg = '+'
        bmam__nsnbv = 'index_arr[-1] < threshhold_date'
        dmv__tfeo = 'n'
        hrvyt__jlxxw = 'index_arr[i] >= threshhold_date'
        scjm__dclwv = 'i'
    dkuc__ksmky = (
        'def impl(index_arr, offset, initial_date, is_last, is_parallel=False):\n'
        )
    if types.unliteral(offset) == types.unicode_type:
        dkuc__ksmky += (
            '  with numba.objmode(threshhold_date=bodo.pd_timestamp_type):\n')
        dkuc__ksmky += (
            '    date_offset = pd.tseries.frequencies.to_offset(offset)\n')
        if not get_overload_const_bool(is_last):
            dkuc__ksmky += """    if not isinstance(date_offset, pd._libs.tslibs.Tick) and date_offset.is_on_offset(index_arr[0]):
"""
            dkuc__ksmky += """      threshhold_date = initial_date - date_offset.base + date_offset
"""
            dkuc__ksmky += '    else:\n'
            dkuc__ksmky += (
                '      threshhold_date = initial_date + date_offset\n')
        else:
            dkuc__ksmky += (
                f'    threshhold_date = initial_date {efh__deeg} date_offset\n'
                )
    else:
        dkuc__ksmky += f'  threshhold_date = initial_date {efh__deeg} offset\n'
    dkuc__ksmky += '  local_valid = 0\n'
    dkuc__ksmky += f'  n = len(index_arr)\n'
    dkuc__ksmky += f'  if n:\n'
    dkuc__ksmky += f'    if {bmam__nsnbv}:\n'
    dkuc__ksmky += '      loc_valid = n\n'
    dkuc__ksmky += '    else:\n'
    dkuc__ksmky += f'      for i in range({dmv__tfeo}):\n'
    dkuc__ksmky += f'        if {hrvyt__jlxxw}:\n'
    dkuc__ksmky += f'          loc_valid = {scjm__dclwv}\n'
    dkuc__ksmky += '          break\n'
    dkuc__ksmky += '  if is_parallel:\n'
    dkuc__ksmky += (
        '    total_valid = bodo.libs.distributed_api.dist_reduce(loc_valid, sum_op)\n'
        )
    dkuc__ksmky += '    return total_valid\n'
    dkuc__ksmky += '  else:\n'
    dkuc__ksmky += '    return loc_valid\n'
    tpxxu__nsdw = {}
    exec(dkuc__ksmky, {'bodo': bodo, 'pd': pd, 'numba': numba, 'sum_op':
        sum_op}, tpxxu__nsdw)
    return tpxxu__nsdw['impl']


def quantile(A, q):
    return 0


def quantile_parallel(A, q):
    return 0


@infer_global(quantile)
@infer_global(quantile_parallel)
class QuantileType(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) in [2, 3]
        return signature(types.float64, *unliteral_all(args))


@lower_builtin(quantile, types.Array, types.float64)
@lower_builtin(quantile, IntegerArrayType, types.float64)
@lower_builtin(quantile, BooleanArrayType, types.float64)
def lower_dist_quantile_seq(context, builder, sig, args):
    gcen__nsp = numba_to_c_type(sig.args[0].dtype)
    qwl__tbsa = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (32), gcen__nsp))
    tpms__tav = args[0]
    gsgbx__ophg = sig.args[0]
    if isinstance(gsgbx__ophg, (IntegerArrayType, BooleanArrayType)):
        tpms__tav = cgutils.create_struct_proxy(gsgbx__ophg)(context,
            builder, tpms__tav).data
        gsgbx__ophg = types.Array(gsgbx__ophg.dtype, 1, 'C')
    assert gsgbx__ophg.ndim == 1
    arr = make_array(gsgbx__ophg)(context, builder, tpms__tav)
    nyie__yreu = builder.extract_value(arr.shape, 0)
    meapi__lyb = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        nyie__yreu, args[1], builder.load(qwl__tbsa)]
    vsy__ykkr = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    bopi__dan = lir.FunctionType(lir.DoubleType(), vsy__ykkr)
    lzb__yihq = cgutils.get_or_insert_function(builder.module, bopi__dan,
        name='quantile_sequential')
    lmhl__xwnnv = builder.call(lzb__yihq, meapi__lyb)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return lmhl__xwnnv


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    gcen__nsp = numba_to_c_type(sig.args[0].dtype)
    qwl__tbsa = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (32), gcen__nsp))
    tpms__tav = args[0]
    gsgbx__ophg = sig.args[0]
    if isinstance(gsgbx__ophg, (IntegerArrayType, BooleanArrayType)):
        tpms__tav = cgutils.create_struct_proxy(gsgbx__ophg)(context,
            builder, tpms__tav).data
        gsgbx__ophg = types.Array(gsgbx__ophg.dtype, 1, 'C')
    assert gsgbx__ophg.ndim == 1
    arr = make_array(gsgbx__ophg)(context, builder, tpms__tav)
    nyie__yreu = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        kixh__mynzt = args[2]
    else:
        kixh__mynzt = nyie__yreu
    meapi__lyb = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        nyie__yreu, kixh__mynzt, args[1], builder.load(qwl__tbsa)]
    vsy__ykkr = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.IntType(
        64), lir.DoubleType(), lir.IntType(32)]
    bopi__dan = lir.FunctionType(lir.DoubleType(), vsy__ykkr)
    lzb__yihq = cgutils.get_or_insert_function(builder.module, bopi__dan,
        name='quantile_parallel')
    lmhl__xwnnv = builder.call(lzb__yihq, meapi__lyb)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return lmhl__xwnnv


@numba.generated_jit(nopython=True)
def _rank_detect_ties(arr):

    def impl(arr):
        zmwgb__kmodh = np.nonzero(pd.isna(arr))[0]
        gykw__eaier = arr[1:] != arr[:-1]
        gykw__eaier[pd.isna(gykw__eaier)] = False
        wyyfn__zhj = gykw__eaier.astype(np.bool_)
        rcme__wnxu = np.concatenate((np.array([True]), wyyfn__zhj))
        if zmwgb__kmodh.size:
            qiz__sykw, bll__ayg = zmwgb__kmodh[0], zmwgb__kmodh[1:]
            rcme__wnxu[qiz__sykw] = True
            if bll__ayg.size:
                rcme__wnxu[bll__ayg] = False
                if bll__ayg[-1] + 1 < rcme__wnxu.size:
                    rcme__wnxu[bll__ayg[-1] + 1] = True
            elif qiz__sykw + 1 < rcme__wnxu.size:
                rcme__wnxu[qiz__sykw + 1] = True
        return rcme__wnxu
    return impl


def rank(arr, method='average', na_option='keep', ascending=True, pct=False):
    return arr


@overload(rank, no_unliteral=True, inline='always')
def overload_rank(arr, method='average', na_option='keep', ascending=True,
    pct=False):
    if not is_overload_constant_str(method):
        raise_bodo_error(
            "Series.rank(): 'method' argument must be a constant string")
    method = get_overload_const_str(method)
    if not is_overload_constant_str(na_option):
        raise_bodo_error(
            "Series.rank(): 'na_option' argument must be a constant string")
    na_option = get_overload_const_str(na_option)
    if not is_overload_constant_bool(ascending):
        raise_bodo_error(
            "Series.rank(): 'ascending' argument must be a constant boolean")
    ascending = get_overload_const_bool(ascending)
    if not is_overload_constant_bool(pct):
        raise_bodo_error(
            "Series.rank(): 'pct' argument must be a constant boolean")
    pct = get_overload_const_bool(pct)
    if method == 'first' and not ascending:
        raise BodoError(
            "Series.rank(): method='first' with ascending=False is currently unsupported."
            )
    dkuc__ksmky = (
        "def impl(arr, method='average', na_option='keep', ascending=True, pct=False):\n"
        )
    dkuc__ksmky += '  na_idxs = pd.isna(arr)\n'
    dkuc__ksmky += '  sorter = bodo.hiframes.series_impl.argsort(arr)\n'
    dkuc__ksmky += '  nas = sum(na_idxs)\n'
    if not ascending:
        dkuc__ksmky += '  if nas and nas < (sorter.size - 1):\n'
        dkuc__ksmky += '    sorter[:-nas] = sorter[-(nas + 1)::-1]\n'
        dkuc__ksmky += '  else:\n'
        dkuc__ksmky += '    sorter = sorter[::-1]\n'
    if na_option == 'top':
        dkuc__ksmky += (
            '  sorter = np.concatenate((sorter[-nas:], sorter[:-nas]))\n')
    dkuc__ksmky += '  inv = np.empty(sorter.size, dtype=np.intp)\n'
    dkuc__ksmky += '  inv[sorter] = np.arange(sorter.size)\n'
    if method == 'first':
        dkuc__ksmky += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
        dkuc__ksmky += '    inv,\n'
        dkuc__ksmky += '    new_dtype=np.float64,\n'
        dkuc__ksmky += '    copy=True,\n'
        dkuc__ksmky += '    nan_to_str=False,\n'
        dkuc__ksmky += '    from_series=True,\n'
        dkuc__ksmky += '    ) + 1\n'
    else:
        dkuc__ksmky += '  arr = arr[sorter]\n'
        dkuc__ksmky += (
            '  obs = bodo.libs.array_kernels._rank_detect_ties(arr)\n')
        dkuc__ksmky += '  dense = obs.cumsum()[inv]\n'
        if method == 'dense':
            dkuc__ksmky += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
            dkuc__ksmky += '    dense,\n'
            dkuc__ksmky += '    new_dtype=np.float64,\n'
            dkuc__ksmky += '    copy=True,\n'
            dkuc__ksmky += '    nan_to_str=False,\n'
            dkuc__ksmky += '    from_series=True,\n'
            dkuc__ksmky += '  )\n'
        else:
            dkuc__ksmky += (
                '  count = np.concatenate((np.nonzero(obs)[0], np.array([len(obs)])))\n'
                )
            dkuc__ksmky += """  count_float = bodo.utils.conversion.fix_arr_dtype(count, new_dtype=np.float64, copy=True, nan_to_str=False, from_series=True)
"""
            if method == 'max':
                dkuc__ksmky += '  ret = count_float[dense]\n'
            elif method == 'min':
                dkuc__ksmky += '  ret = count_float[dense - 1] + 1\n'
            else:
                dkuc__ksmky += (
                    '  ret = 0.5 * (count_float[dense] + count_float[dense - 1] + 1)\n'
                    )
    if pct:
        if method == 'dense':
            if na_option == 'keep':
                dkuc__ksmky += '  ret[na_idxs] = -1\n'
            dkuc__ksmky += '  div_val = np.max(ret)\n'
        elif na_option == 'keep':
            dkuc__ksmky += '  div_val = arr.size - nas\n'
        else:
            dkuc__ksmky += '  div_val = arr.size\n'
        dkuc__ksmky += '  for i in range(len(ret)):\n'
        dkuc__ksmky += '    ret[i] = ret[i] / div_val\n'
    if na_option == 'keep':
        dkuc__ksmky += '  ret[na_idxs] = np.nan\n'
    dkuc__ksmky += '  return ret\n'
    tpxxu__nsdw = {}
    exec(dkuc__ksmky, {'np': np, 'pd': pd, 'bodo': bodo}, tpxxu__nsdw)
    return tpxxu__nsdw['impl']


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    ezn__gln = start
    fcfoh__knvy = 2 * start + 1
    cvqu__fwxq = 2 * start + 2
    if fcfoh__knvy < n and not cmp_f(arr[fcfoh__knvy], arr[ezn__gln]):
        ezn__gln = fcfoh__knvy
    if cvqu__fwxq < n and not cmp_f(arr[cvqu__fwxq], arr[ezn__gln]):
        ezn__gln = cvqu__fwxq
    if ezn__gln != start:
        arr[start], arr[ezn__gln] = arr[ezn__gln], arr[start]
        ind_arr[start], ind_arr[ezn__gln] = ind_arr[ezn__gln], ind_arr[start]
        min_heapify(arr, ind_arr, n, ezn__gln, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        rrgr__acxvr = np.empty(k, A.dtype)
        zcs__cptnz = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                rrgr__acxvr[ind] = A[i]
                zcs__cptnz[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            rrgr__acxvr = rrgr__acxvr[:ind]
            zcs__cptnz = zcs__cptnz[:ind]
        return rrgr__acxvr, zcs__cptnz, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        okqhi__llokl = np.sort(A)
        ysj__fovp = index_arr[np.argsort(A)]
        tddz__caw = pd.Series(okqhi__llokl).notna().values
        okqhi__llokl = okqhi__llokl[tddz__caw]
        ysj__fovp = ysj__fovp[tddz__caw]
        if is_largest:
            okqhi__llokl = okqhi__llokl[::-1]
            ysj__fovp = ysj__fovp[::-1]
        return np.ascontiguousarray(okqhi__llokl), np.ascontiguousarray(
            ysj__fovp)
    rrgr__acxvr, zcs__cptnz, start = select_k_nonan(A, index_arr, m, k)
    zcs__cptnz = zcs__cptnz[rrgr__acxvr.argsort()]
    rrgr__acxvr.sort()
    if not is_largest:
        rrgr__acxvr = np.ascontiguousarray(rrgr__acxvr[::-1])
        zcs__cptnz = np.ascontiguousarray(zcs__cptnz[::-1])
    for i in range(start, m):
        if cmp_f(A[i], rrgr__acxvr[0]):
            rrgr__acxvr[0] = A[i]
            zcs__cptnz[0] = index_arr[i]
            min_heapify(rrgr__acxvr, zcs__cptnz, k, 0, cmp_f)
    zcs__cptnz = zcs__cptnz[rrgr__acxvr.argsort()]
    rrgr__acxvr.sort()
    if is_largest:
        rrgr__acxvr = rrgr__acxvr[::-1]
        zcs__cptnz = zcs__cptnz[::-1]
    return np.ascontiguousarray(rrgr__acxvr), np.ascontiguousarray(zcs__cptnz)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    moeeq__lofaq = bodo.libs.distributed_api.get_rank()
    oiwnu__cphm, offzu__xryes = nlargest(A, I, k, is_largest, cmp_f)
    lszq__dtcn = bodo.libs.distributed_api.gatherv(oiwnu__cphm)
    qyg__ryjsb = bodo.libs.distributed_api.gatherv(offzu__xryes)
    if moeeq__lofaq == MPI_ROOT:
        res, fak__wlo = nlargest(lszq__dtcn, qyg__ryjsb, k, is_largest, cmp_f)
    else:
        res = np.empty(k, A.dtype)
        fak__wlo = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(fak__wlo)
    return res, fak__wlo


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    heo__byr, rez__lhk = mat.shape
    uwm__yjo = np.empty((rez__lhk, rez__lhk), dtype=np.float64)
    for vvgb__lqx in range(rez__lhk):
        for wkav__lhbh in range(vvgb__lqx + 1):
            yqm__bssg = 0
            qokl__udfwx = emxq__bazxb = tkudq__cxuhe = xom__hripf = 0.0
            for i in range(heo__byr):
                if np.isfinite(mat[i, vvgb__lqx]) and np.isfinite(mat[i,
                    wkav__lhbh]):
                    bzm__ctom = mat[i, vvgb__lqx]
                    psh__bnjil = mat[i, wkav__lhbh]
                    yqm__bssg += 1
                    tkudq__cxuhe += bzm__ctom
                    xom__hripf += psh__bnjil
            if parallel:
                yqm__bssg = bodo.libs.distributed_api.dist_reduce(yqm__bssg,
                    sum_op)
                tkudq__cxuhe = bodo.libs.distributed_api.dist_reduce(
                    tkudq__cxuhe, sum_op)
                xom__hripf = bodo.libs.distributed_api.dist_reduce(xom__hripf,
                    sum_op)
            if yqm__bssg < minpv:
                uwm__yjo[vvgb__lqx, wkav__lhbh] = uwm__yjo[wkav__lhbh,
                    vvgb__lqx] = np.nan
            else:
                ivk__bbq = tkudq__cxuhe / yqm__bssg
                kddod__gfuwh = xom__hripf / yqm__bssg
                tkudq__cxuhe = 0.0
                for i in range(heo__byr):
                    if np.isfinite(mat[i, vvgb__lqx]) and np.isfinite(mat[i,
                        wkav__lhbh]):
                        bzm__ctom = mat[i, vvgb__lqx] - ivk__bbq
                        psh__bnjil = mat[i, wkav__lhbh] - kddod__gfuwh
                        tkudq__cxuhe += bzm__ctom * psh__bnjil
                        qokl__udfwx += bzm__ctom * bzm__ctom
                        emxq__bazxb += psh__bnjil * psh__bnjil
                if parallel:
                    tkudq__cxuhe = bodo.libs.distributed_api.dist_reduce(
                        tkudq__cxuhe, sum_op)
                    qokl__udfwx = bodo.libs.distributed_api.dist_reduce(
                        qokl__udfwx, sum_op)
                    emxq__bazxb = bodo.libs.distributed_api.dist_reduce(
                        emxq__bazxb, sum_op)
                hpqbn__qko = yqm__bssg - 1.0 if cov else sqrt(qokl__udfwx *
                    emxq__bazxb)
                if hpqbn__qko != 0.0:
                    uwm__yjo[vvgb__lqx, wkav__lhbh] = uwm__yjo[wkav__lhbh,
                        vvgb__lqx] = tkudq__cxuhe / hpqbn__qko
                else:
                    uwm__yjo[vvgb__lqx, wkav__lhbh] = uwm__yjo[wkav__lhbh,
                        vvgb__lqx] = np.nan
    return uwm__yjo


@numba.generated_jit(nopython=True)
def duplicated(data, parallel=False):
    n = len(data)
    if n == 0:
        return lambda data, parallel=False: np.empty(0, dtype=np.bool_)
    liee__qnk = n != 1
    dkuc__ksmky = 'def impl(data, parallel=False):\n'
    dkuc__ksmky += '  if parallel:\n'
    txlk__tqrgq = ', '.join(f'array_to_info(data[{i}])' for i in range(n))
    dkuc__ksmky += f'    cpp_table = arr_info_list_to_table([{txlk__tqrgq}])\n'
    dkuc__ksmky += f"""    out_cpp_table = bodo.libs.array.shuffle_table(cpp_table, {n}, parallel, 1)
"""
    rcmt__txfy = ', '.join(
        f'info_to_array(info_from_table(out_cpp_table, {i}), data[{i}])' for
        i in range(n))
    dkuc__ksmky += f'    data = ({rcmt__txfy},)\n'
    dkuc__ksmky += (
        '    shuffle_info = bodo.libs.array.get_shuffle_info(out_cpp_table)\n')
    dkuc__ksmky += '    bodo.libs.array.delete_table(out_cpp_table)\n'
    dkuc__ksmky += '    bodo.libs.array.delete_table(cpp_table)\n'
    dkuc__ksmky += '  n = len(data[0])\n'
    dkuc__ksmky += '  out = np.empty(n, np.bool_)\n'
    dkuc__ksmky += '  uniqs = dict()\n'
    if liee__qnk:
        dkuc__ksmky += '  for i in range(n):\n'
        eaxy__dure = ', '.join(f'data[{i}][i]' for i in range(n))
        tpslw__ylxw = ',  '.join(
            f'bodo.libs.array_kernels.isna(data[{i}], i)' for i in range(n))
        dkuc__ksmky += f"""    val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({eaxy__dure},), ({tpslw__ylxw},))
"""
        dkuc__ksmky += '    if val in uniqs:\n'
        dkuc__ksmky += '      out[i] = True\n'
        dkuc__ksmky += '    else:\n'
        dkuc__ksmky += '      out[i] = False\n'
        dkuc__ksmky += '      uniqs[val] = 0\n'
    else:
        dkuc__ksmky += '  data = data[0]\n'
        dkuc__ksmky += '  hasna = False\n'
        dkuc__ksmky += '  for i in range(n):\n'
        dkuc__ksmky += '    if bodo.libs.array_kernels.isna(data, i):\n'
        dkuc__ksmky += '      out[i] = hasna\n'
        dkuc__ksmky += '      hasna = True\n'
        dkuc__ksmky += '    else:\n'
        dkuc__ksmky += '      val = data[i]\n'
        dkuc__ksmky += '      if val in uniqs:\n'
        dkuc__ksmky += '        out[i] = True\n'
        dkuc__ksmky += '      else:\n'
        dkuc__ksmky += '        out[i] = False\n'
        dkuc__ksmky += '        uniqs[val] = 0\n'
    dkuc__ksmky += '  if parallel:\n'
    dkuc__ksmky += (
        '    out = bodo.hiframes.pd_groupby_ext.reverse_shuffle(out, shuffle_info)\n'
        )
    dkuc__ksmky += '  return out\n'
    tpxxu__nsdw = {}
    exec(dkuc__ksmky, {'bodo': bodo, 'np': np, 'array_to_info':
        array_to_info, 'arr_info_list_to_table': arr_info_list_to_table,
        'info_to_array': info_to_array, 'info_from_table': info_from_table},
        tpxxu__nsdw)
    impl = tpxxu__nsdw['impl']
    return impl


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    return data, ind_arr


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    ccran__kkuml = len(data)
    dkuc__ksmky = (
        'def impl(data, ind_arr, n, frac, replace, parallel=False):\n')
    dkuc__ksmky += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        ccran__kkuml)))
    dkuc__ksmky += '  table_total = arr_info_list_to_table(info_list_total)\n'
    dkuc__ksmky += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(ccran__kkuml))
    for lsgvh__pmkmd in range(ccran__kkuml):
        dkuc__ksmky += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(lsgvh__pmkmd, lsgvh__pmkmd, lsgvh__pmkmd))
    dkuc__ksmky += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(ccran__kkuml))
    dkuc__ksmky += '  delete_table(out_table)\n'
    dkuc__ksmky += '  delete_table(table_total)\n'
    dkuc__ksmky += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(ccran__kkuml)))
    tpxxu__nsdw = {}
    exec(dkuc__ksmky, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'sample_table': sample_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, tpxxu__nsdw)
    impl = tpxxu__nsdw['impl']
    return impl


def drop_duplicates(data, ind_arr, ncols, parallel=False):
    return data, ind_arr


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, ncols, parallel=False):
    ccran__kkuml = len(data)
    dkuc__ksmky = 'def impl(data, ind_arr, ncols, parallel=False):\n'
    dkuc__ksmky += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        ccran__kkuml)))
    dkuc__ksmky += '  table_total = arr_info_list_to_table(info_list_total)\n'
    dkuc__ksmky += '  keep_i = 0\n'
    dkuc__ksmky += """  out_table = drop_duplicates_table(table_total, parallel, ncols, keep_i, False, True)
"""
    for lsgvh__pmkmd in range(ccran__kkuml):
        dkuc__ksmky += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(lsgvh__pmkmd, lsgvh__pmkmd, lsgvh__pmkmd))
    dkuc__ksmky += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(ccran__kkuml))
    dkuc__ksmky += '  delete_table(out_table)\n'
    dkuc__ksmky += '  delete_table(table_total)\n'
    dkuc__ksmky += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(ccran__kkuml)))
    tpxxu__nsdw = {}
    exec(dkuc__ksmky, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, tpxxu__nsdw)
    impl = tpxxu__nsdw['impl']
    return impl


def drop_duplicates_array(data_arr, parallel=False):
    return data_arr


@overload(drop_duplicates_array, no_unliteral=True)
def overload_drop_duplicates_array(data_arr, parallel=False):

    def impl(data_arr, parallel=False):
        kdzy__aid = [array_to_info(data_arr)]
        ucdn__xdh = arr_info_list_to_table(kdzy__aid)
        edpbe__gqgvn = 0
        nyaux__lvxy = drop_duplicates_table(ucdn__xdh, parallel, 1,
            edpbe__gqgvn, False, True)
        fkhxi__mvlxe = info_to_array(info_from_table(nyaux__lvxy, 0), data_arr)
        delete_table(nyaux__lvxy)
        delete_table(ucdn__xdh)
        return fkhxi__mvlxe
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    return data


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.dropna()')
    lxp__dxvid = len(data.types)
    fng__zxt = [('out' + str(i)) for i in range(lxp__dxvid)]
    gdcb__yraj = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    fcd__opj = ['isna(data[{}], i)'.format(i) for i in gdcb__yraj]
    myujm__kbm = 'not ({})'.format(' or '.join(fcd__opj))
    if not is_overload_none(thresh):
        myujm__kbm = '(({}) <= ({}) - thresh)'.format(' + '.join(fcd__opj),
            lxp__dxvid - 1)
    elif how == 'all':
        myujm__kbm = 'not ({})'.format(' and '.join(fcd__opj))
    dkuc__ksmky = 'def _dropna_imp(data, how, thresh, subset):\n'
    dkuc__ksmky += '  old_len = len(data[0])\n'
    dkuc__ksmky += '  new_len = 0\n'
    dkuc__ksmky += '  for i in range(old_len):\n'
    dkuc__ksmky += '    if {}:\n'.format(myujm__kbm)
    dkuc__ksmky += '      new_len += 1\n'
    for i, out in enumerate(fng__zxt):
        if isinstance(data[i], bodo.CategoricalArrayType):
            dkuc__ksmky += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            dkuc__ksmky += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    dkuc__ksmky += '  curr_ind = 0\n'
    dkuc__ksmky += '  for i in range(old_len):\n'
    dkuc__ksmky += '    if {}:\n'.format(myujm__kbm)
    for i in range(lxp__dxvid):
        dkuc__ksmky += '      if isna(data[{}], i):\n'.format(i)
        dkuc__ksmky += '        setna({}, curr_ind)\n'.format(fng__zxt[i])
        dkuc__ksmky += '      else:\n'
        dkuc__ksmky += '        {}[curr_ind] = data[{}][i]\n'.format(fng__zxt
            [i], i)
    dkuc__ksmky += '      curr_ind += 1\n'
    dkuc__ksmky += '  return {}\n'.format(', '.join(fng__zxt))
    tpxxu__nsdw = {}
    tmn__dyfox = {'t{}'.format(i): tgje__tys for i, tgje__tys in enumerate(
        data.types)}
    tmn__dyfox.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(dkuc__ksmky, tmn__dyfox, tpxxu__nsdw)
    rndz__abgre = tpxxu__nsdw['_dropna_imp']
    return rndz__abgre


def get(arr, ind):
    return pd.Series(arr).str.get(ind)


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        gsgbx__ophg = arr.dtype
        jko__eiqmr = gsgbx__ophg.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            cajg__fru = init_nested_counts(jko__eiqmr)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                cajg__fru = add_nested_counts(cajg__fru, val[ind])
            fkhxi__mvlxe = bodo.utils.utils.alloc_type(n, gsgbx__ophg,
                cajg__fru)
            for werm__yhl in range(n):
                if bodo.libs.array_kernels.isna(arr, werm__yhl):
                    setna(fkhxi__mvlxe, werm__yhl)
                    continue
                val = arr[werm__yhl]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(fkhxi__mvlxe, werm__yhl)
                    continue
                fkhxi__mvlxe[werm__yhl] = val[ind]
            return fkhxi__mvlxe
        return get_arr_item


def _is_same_categorical_array_type(arr_types):
    from bodo.hiframes.pd_categorical_ext import _to_readonly
    if not isinstance(arr_types, types.BaseTuple) or len(arr_types) == 0:
        return False
    bqfyv__ekqm = _to_readonly(arr_types.types[0])
    return all(isinstance(tgje__tys, CategoricalArrayType) and _to_readonly
        (tgje__tys) == bqfyv__ekqm for tgje__tys in arr_types.types)


def concat(arr_list):
    return pd.concat(arr_list)


@overload(concat, no_unliteral=True)
def concat_overload(arr_list):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arr_list.
        dtype, 'bodo.concat()')
    if isinstance(arr_list, bodo.NullableTupleType):
        return lambda arr_list: bodo.libs.array_kernels.concat(arr_list._data)
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, ArrayItemArrayType):
        jcvcs__brxbl = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            ybdxs__wnihm = 0
            mvnxn__lyq = []
            for A in arr_list:
                qug__yvt = len(A)
                bodo.libs.array_item_arr_ext.trim_excess_data(A)
                mvnxn__lyq.append(bodo.libs.array_item_arr_ext.get_data(A))
                ybdxs__wnihm += qug__yvt
            rzik__dkwr = np.empty(ybdxs__wnihm + 1, offset_type)
            iwydx__own = bodo.libs.array_kernels.concat(mvnxn__lyq)
            vofa__zltkq = np.empty(ybdxs__wnihm + 7 >> 3, np.uint8)
            neeh__zhpq = 0
            mtc__oaq = 0
            for A in arr_list:
                okdlg__lcovz = bodo.libs.array_item_arr_ext.get_offsets(A)
                awpez__iggu = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                qug__yvt = len(A)
                lgkx__ekrgv = okdlg__lcovz[qug__yvt]
                for i in range(qug__yvt):
                    rzik__dkwr[i + neeh__zhpq] = okdlg__lcovz[i] + mtc__oaq
                    xhcms__hnto = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        awpez__iggu, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(vofa__zltkq, i +
                        neeh__zhpq, xhcms__hnto)
                neeh__zhpq += qug__yvt
                mtc__oaq += lgkx__ekrgv
            rzik__dkwr[neeh__zhpq] = mtc__oaq
            fkhxi__mvlxe = bodo.libs.array_item_arr_ext.init_array_item_array(
                ybdxs__wnihm, iwydx__own, rzik__dkwr, vofa__zltkq)
            return fkhxi__mvlxe
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.StructArrayType):
        rkc__midwr = arr_list.dtype.names
        dkuc__ksmky = 'def struct_array_concat_impl(arr_list):\n'
        dkuc__ksmky += f'    n_all = 0\n'
        for i in range(len(rkc__midwr)):
            dkuc__ksmky += f'    concat_list{i} = []\n'
        dkuc__ksmky += '    for A in arr_list:\n'
        dkuc__ksmky += (
            '        data_tuple = bodo.libs.struct_arr_ext.get_data(A)\n')
        for i in range(len(rkc__midwr)):
            dkuc__ksmky += f'        concat_list{i}.append(data_tuple[{i}])\n'
        dkuc__ksmky += '        n_all += len(A)\n'
        dkuc__ksmky += '    n_bytes = (n_all + 7) >> 3\n'
        dkuc__ksmky += '    new_mask = np.empty(n_bytes, np.uint8)\n'
        dkuc__ksmky += '    curr_bit = 0\n'
        dkuc__ksmky += '    for A in arr_list:\n'
        dkuc__ksmky += (
            '        old_mask = bodo.libs.struct_arr_ext.get_null_bitmap(A)\n')
        dkuc__ksmky += '        for j in range(len(A)):\n'
        dkuc__ksmky += (
            '            bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        dkuc__ksmky += """            bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)
"""
        dkuc__ksmky += '            curr_bit += 1\n'
        dkuc__ksmky += '    return bodo.libs.struct_arr_ext.init_struct_arr(\n'
        jygzh__vsxwc = ', '.join([
            f'bodo.libs.array_kernels.concat(concat_list{i})' for i in
            range(len(rkc__midwr))])
        dkuc__ksmky += f'        ({jygzh__vsxwc},),\n'
        dkuc__ksmky += '        new_mask,\n'
        dkuc__ksmky += f'        {rkc__midwr},\n'
        dkuc__ksmky += '    )\n'
        tpxxu__nsdw = {}
        exec(dkuc__ksmky, {'bodo': bodo, 'np': np}, tpxxu__nsdw)
        return tpxxu__nsdw['struct_array_concat_impl']
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            uybs__isuf = 0
            for A in arr_list:
                uybs__isuf += len(A)
            agvj__sscpc = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(uybs__isuf))
            upn__jacgo = 0
            for A in arr_list:
                for i in range(len(A)):
                    agvj__sscpc._data[i + upn__jacgo] = A._data[i]
                    xhcms__hnto = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(agvj__sscpc.
                        _null_bitmap, i + upn__jacgo, xhcms__hnto)
                upn__jacgo += len(A)
            return agvj__sscpc
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            uybs__isuf = 0
            for A in arr_list:
                uybs__isuf += len(A)
            agvj__sscpc = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(uybs__isuf))
            upn__jacgo = 0
            for A in arr_list:
                for i in range(len(A)):
                    agvj__sscpc._days_data[i + upn__jacgo] = A._days_data[i]
                    agvj__sscpc._seconds_data[i + upn__jacgo
                        ] = A._seconds_data[i]
                    agvj__sscpc._microseconds_data[i + upn__jacgo
                        ] = A._microseconds_data[i]
                    xhcms__hnto = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(agvj__sscpc.
                        _null_bitmap, i + upn__jacgo, xhcms__hnto)
                upn__jacgo += len(A)
            return agvj__sscpc
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        ksuw__kcrm = arr_list.dtype.precision
        fxrhw__dob = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            uybs__isuf = 0
            for A in arr_list:
                uybs__isuf += len(A)
            agvj__sscpc = bodo.libs.decimal_arr_ext.alloc_decimal_array(
                uybs__isuf, ksuw__kcrm, fxrhw__dob)
            upn__jacgo = 0
            for A in arr_list:
                for i in range(len(A)):
                    agvj__sscpc._data[i + upn__jacgo] = A._data[i]
                    xhcms__hnto = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(agvj__sscpc.
                        _null_bitmap, i + upn__jacgo, xhcms__hnto)
                upn__jacgo += len(A)
            return agvj__sscpc
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and (is_str_arr_type
        (arr_list.dtype) or arr_list.dtype == bodo.binary_array_type
        ) or isinstance(arr_list, types.BaseTuple) and all(is_str_arr_type(
        tgje__tys) for tgje__tys in arr_list.types):
        if isinstance(arr_list, types.BaseTuple):
            qkxs__vamls = arr_list.types[0]
            for i in range(len(arr_list)):
                if arr_list.types[i] != bodo.dict_str_arr_type:
                    qkxs__vamls = arr_list.types[i]
                    break
        else:
            qkxs__vamls = arr_list.dtype
        if qkxs__vamls == bodo.dict_str_arr_type:

            def impl_dict_arr(arr_list):
                qzli__nltxm = 0
                ocp__bgq = 0
                pvnda__yyyoz = 0
                for A in arr_list:
                    data_arr = A._data
                    yeu__aoq = A._indices
                    pvnda__yyyoz += len(yeu__aoq)
                    qzli__nltxm += len(data_arr)
                    ocp__bgq += bodo.libs.str_arr_ext.num_total_chars(data_arr)
                cmrwl__pjvqw = pre_alloc_string_array(qzli__nltxm, ocp__bgq)
                xhgf__lfdw = bodo.libs.int_arr_ext.alloc_int_array(pvnda__yyyoz
                    , np.int32)
                bodo.libs.str_arr_ext.set_null_bits_to_value(cmrwl__pjvqw, -1)
                uerxc__pqohl = 0
                fisit__jshbk = 0
                rrgi__ozywh = 0
                for A in arr_list:
                    data_arr = A._data
                    yeu__aoq = A._indices
                    pvnda__yyyoz = len(yeu__aoq)
                    bodo.libs.str_arr_ext.set_string_array_range(cmrwl__pjvqw,
                        data_arr, uerxc__pqohl, fisit__jshbk)
                    for i in range(pvnda__yyyoz):
                        if bodo.libs.array_kernels.isna(yeu__aoq, i
                            ) or bodo.libs.array_kernels.isna(data_arr,
                            yeu__aoq[i]):
                            bodo.libs.array_kernels.setna(xhgf__lfdw, 
                                rrgi__ozywh + i)
                        else:
                            xhgf__lfdw[rrgi__ozywh + i
                                ] = uerxc__pqohl + yeu__aoq[i]
                    uerxc__pqohl += len(data_arr)
                    fisit__jshbk += bodo.libs.str_arr_ext.num_total_chars(
                        data_arr)
                    rrgi__ozywh += pvnda__yyyoz
                fkhxi__mvlxe = init_dict_arr(cmrwl__pjvqw, xhgf__lfdw, False)
                oep__cqwza = convert_local_dictionary_to_global(fkhxi__mvlxe,
                    False)
                return oep__cqwza
            return impl_dict_arr

        def impl_str(arr_list):
            arr_list = decode_if_dict_array(arr_list)
            qzli__nltxm = 0
            ocp__bgq = 0
            for A in arr_list:
                arr = A
                qzli__nltxm += len(arr)
                ocp__bgq += bodo.libs.str_arr_ext.num_total_chars(arr)
            fkhxi__mvlxe = bodo.utils.utils.alloc_type(qzli__nltxm,
                qkxs__vamls, (ocp__bgq,))
            bodo.libs.str_arr_ext.set_null_bits_to_value(fkhxi__mvlxe, -1)
            uerxc__pqohl = 0
            fisit__jshbk = 0
            for A in arr_list:
                arr = A
                bodo.libs.str_arr_ext.set_string_array_range(fkhxi__mvlxe,
                    arr, uerxc__pqohl, fisit__jshbk)
                uerxc__pqohl += len(arr)
                fisit__jshbk += bodo.libs.str_arr_ext.num_total_chars(arr)
            return fkhxi__mvlxe
        return impl_str
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(tgje__tys.dtype, types.Integer) for
        tgje__tys in arr_list.types) and any(isinstance(tgje__tys,
        IntegerArrayType) for tgje__tys in arr_list.types):

        def impl_int_arr_list(arr_list):
            izmth__dqz = convert_to_nullable_tup(arr_list)
            fpfm__punfj = []
            vhq__ksv = 0
            for A in izmth__dqz:
                fpfm__punfj.append(A._data)
                vhq__ksv += len(A)
            iwydx__own = bodo.libs.array_kernels.concat(fpfm__punfj)
            mour__priqk = vhq__ksv + 7 >> 3
            ihiv__aqi = np.empty(mour__priqk, np.uint8)
            kvvq__xqgxh = 0
            for A in izmth__dqz:
                kqazl__npowf = A._null_bitmap
                for werm__yhl in range(len(A)):
                    xhcms__hnto = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        kqazl__npowf, werm__yhl)
                    bodo.libs.int_arr_ext.set_bit_to_arr(ihiv__aqi,
                        kvvq__xqgxh, xhcms__hnto)
                    kvvq__xqgxh += 1
            return bodo.libs.int_arr_ext.init_integer_array(iwydx__own,
                ihiv__aqi)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(tgje__tys.dtype == types.bool_ for tgje__tys in
        arr_list.types) and any(tgje__tys == boolean_array for tgje__tys in
        arr_list.types):

        def impl_bool_arr_list(arr_list):
            izmth__dqz = convert_to_nullable_tup(arr_list)
            fpfm__punfj = []
            vhq__ksv = 0
            for A in izmth__dqz:
                fpfm__punfj.append(A._data)
                vhq__ksv += len(A)
            iwydx__own = bodo.libs.array_kernels.concat(fpfm__punfj)
            mour__priqk = vhq__ksv + 7 >> 3
            ihiv__aqi = np.empty(mour__priqk, np.uint8)
            kvvq__xqgxh = 0
            for A in izmth__dqz:
                kqazl__npowf = A._null_bitmap
                for werm__yhl in range(len(A)):
                    xhcms__hnto = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        kqazl__npowf, werm__yhl)
                    bodo.libs.int_arr_ext.set_bit_to_arr(ihiv__aqi,
                        kvvq__xqgxh, xhcms__hnto)
                    kvvq__xqgxh += 1
            return bodo.libs.bool_arr_ext.init_bool_array(iwydx__own, ihiv__aqi
                )
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            gwkix__yri = []
            for A in arr_list:
                gwkix__yri.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                gwkix__yri), arr_list[0].dtype)
        return cat_array_concat_impl
    if _is_same_categorical_array_type(arr_list):
        bhgis__wjfsf = ', '.join(f'arr_list[{i}].codes' for i in range(len(
            arr_list)))
        dkuc__ksmky = 'def impl(arr_list):\n'
        dkuc__ksmky += f"""    return init_categorical_array(bodo.libs.array_kernels.concat(({bhgis__wjfsf},)), arr_list[0].dtype)
"""
        zim__abgv = {}
        exec(dkuc__ksmky, {'bodo': bodo, 'init_categorical_array':
            init_categorical_array}, zim__abgv)
        return zim__abgv['impl']
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            vhq__ksv = 0
            for A in arr_list:
                vhq__ksv += len(A)
            fkhxi__mvlxe = np.empty(vhq__ksv, dtype)
            cxdn__fawsl = 0
            for A in arr_list:
                n = len(A)
                fkhxi__mvlxe[cxdn__fawsl:cxdn__fawsl + n] = A
                cxdn__fawsl += n
            return fkhxi__mvlxe
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(tgje__tys,
        (types.Array, IntegerArrayType)) and isinstance(tgje__tys.dtype,
        types.Integer) for tgje__tys in arr_list.types) and any(isinstance(
        tgje__tys, types.Array) and isinstance(tgje__tys.dtype, types.Float
        ) for tgje__tys in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.MapArrayType):

        def impl_map_arr_list(arr_list):
            pfk__ppbn = []
            for A in arr_list:
                pfk__ppbn.append(A._data)
            ihldc__eysxh = bodo.libs.array_kernels.concat(pfk__ppbn)
            uwm__yjo = bodo.libs.map_arr_ext.init_map_arr(ihldc__eysxh)
            return uwm__yjo
        return impl_map_arr_list
    for iuzq__zyhrc in arr_list:
        if not isinstance(iuzq__zyhrc, types.Array):
            raise_bodo_error(f'concat of array types {arr_list} not supported')
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(tgje__tys.astype(np.float64) for tgje__tys in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    ccran__kkuml = len(arr_tup.types)
    dkuc__ksmky = 'def f(arr_tup):\n'
    dkuc__ksmky += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(
        ccran__kkuml)), ',' if ccran__kkuml == 1 else '')
    tpxxu__nsdw = {}
    exec(dkuc__ksmky, {'np': np}, tpxxu__nsdw)
    jbkzb__wxw = tpxxu__nsdw['f']
    return jbkzb__wxw


def convert_to_nullable_tup(arr_tup):
    return arr_tup


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple)
    ccran__kkuml = len(arr_tup.types)
    mcrzc__cum = find_common_np_dtype(arr_tup.types)
    jko__eiqmr = None
    qzkbf__oyzn = ''
    if isinstance(mcrzc__cum, types.Integer):
        jko__eiqmr = bodo.libs.int_arr_ext.IntDtype(mcrzc__cum)
        qzkbf__oyzn = '.astype(out_dtype, False)'
    dkuc__ksmky = 'def f(arr_tup):\n'
    dkuc__ksmky += '  return ({}{})\n'.format(','.join(
        'bodo.utils.conversion.coerce_to_array(arr_tup[{}], use_nullable_array=True){}'
        .format(i, qzkbf__oyzn) for i in range(ccran__kkuml)), ',' if 
        ccran__kkuml == 1 else '')
    tpxxu__nsdw = {}
    exec(dkuc__ksmky, {'bodo': bodo, 'out_dtype': jko__eiqmr}, tpxxu__nsdw)
    ooc__bgey = tpxxu__nsdw['f']
    return ooc__bgey


def nunique(A, dropna):
    return len(set(A))


def nunique_parallel(A, dropna):
    return len(set(A))


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, xonj__bftlg = build_set_seen_na(A)
        return len(s) + int(not dropna and xonj__bftlg)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        ybol__ggqxd = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        leixq__zcq = len(ybol__ggqxd)
        return bodo.libs.distributed_api.dist_reduce(leixq__zcq, np.int32(
            sum_op))
    return nunique_par


def unique(A, dropna=False, parallel=False):
    return np.array([sxls__rkki for sxls__rkki in set(A)]).astype(A.dtype)


def cummin(A):
    return A


@overload(cummin, no_unliteral=True)
def cummin_overload(A):
    if isinstance(A.dtype, types.Float):
        pyd__dmkrc = np.finfo(A.dtype(1).dtype).max
    else:
        pyd__dmkrc = np.iinfo(A.dtype(1).dtype).max

    def impl(A):
        n = len(A)
        fkhxi__mvlxe = np.empty(n, A.dtype)
        exdgb__abi = pyd__dmkrc
        for i in range(n):
            exdgb__abi = min(exdgb__abi, A[i])
            fkhxi__mvlxe[i] = exdgb__abi
        return fkhxi__mvlxe
    return impl


def cummax(A):
    return A


@overload(cummax, no_unliteral=True)
def cummax_overload(A):
    if isinstance(A.dtype, types.Float):
        pyd__dmkrc = np.finfo(A.dtype(1).dtype).min
    else:
        pyd__dmkrc = np.iinfo(A.dtype(1).dtype).min

    def impl(A):
        n = len(A)
        fkhxi__mvlxe = np.empty(n, A.dtype)
        exdgb__abi = pyd__dmkrc
        for i in range(n):
            exdgb__abi = max(exdgb__abi, A[i])
            fkhxi__mvlxe[i] = exdgb__abi
        return fkhxi__mvlxe
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        svddx__wbt = arr_info_list_to_table([array_to_info(A)])
        uqhfv__cie = 1
        edpbe__gqgvn = 0
        nyaux__lvxy = drop_duplicates_table(svddx__wbt, parallel,
            uqhfv__cie, edpbe__gqgvn, dropna, True)
        fkhxi__mvlxe = info_to_array(info_from_table(nyaux__lvxy, 0), A)
        delete_table(svddx__wbt)
        delete_table(nyaux__lvxy)
        return fkhxi__mvlxe
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    jcvcs__brxbl = bodo.utils.typing.to_nullable_type(arr.dtype)
    bip__sbc = index_arr
    rzgfg__rhmi = bip__sbc.dtype

    def impl(arr, index_arr):
        n = len(arr)
        cajg__fru = init_nested_counts(jcvcs__brxbl)
        rlcri__ihoqa = init_nested_counts(rzgfg__rhmi)
        for i in range(n):
            xszhs__ebt = index_arr[i]
            if isna(arr, i):
                cajg__fru = (cajg__fru[0] + 1,) + cajg__fru[1:]
                rlcri__ihoqa = add_nested_counts(rlcri__ihoqa, xszhs__ebt)
                continue
            zyvs__icol = arr[i]
            if len(zyvs__icol) == 0:
                cajg__fru = (cajg__fru[0] + 1,) + cajg__fru[1:]
                rlcri__ihoqa = add_nested_counts(rlcri__ihoqa, xszhs__ebt)
                continue
            cajg__fru = add_nested_counts(cajg__fru, zyvs__icol)
            for hvwba__dwanl in range(len(zyvs__icol)):
                rlcri__ihoqa = add_nested_counts(rlcri__ihoqa, xszhs__ebt)
        fkhxi__mvlxe = bodo.utils.utils.alloc_type(cajg__fru[0],
            jcvcs__brxbl, cajg__fru[1:])
        fmof__iez = bodo.utils.utils.alloc_type(cajg__fru[0], bip__sbc,
            rlcri__ihoqa)
        mtc__oaq = 0
        for i in range(n):
            if isna(arr, i):
                setna(fkhxi__mvlxe, mtc__oaq)
                fmof__iez[mtc__oaq] = index_arr[i]
                mtc__oaq += 1
                continue
            zyvs__icol = arr[i]
            lgkx__ekrgv = len(zyvs__icol)
            if lgkx__ekrgv == 0:
                setna(fkhxi__mvlxe, mtc__oaq)
                fmof__iez[mtc__oaq] = index_arr[i]
                mtc__oaq += 1
                continue
            fkhxi__mvlxe[mtc__oaq:mtc__oaq + lgkx__ekrgv] = zyvs__icol
            fmof__iez[mtc__oaq:mtc__oaq + lgkx__ekrgv] = index_arr[i]
            mtc__oaq += lgkx__ekrgv
        return fkhxi__mvlxe, fmof__iez
    return impl


def explode_no_index(arr):
    return pd.Series(arr).explode()


@overload(explode_no_index, no_unliteral=True)
def overload_explode_no_index(arr, counts):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    jcvcs__brxbl = bodo.utils.typing.to_nullable_type(arr.dtype)

    def impl(arr, counts):
        n = len(arr)
        cajg__fru = init_nested_counts(jcvcs__brxbl)
        for i in range(n):
            if isna(arr, i):
                cajg__fru = (cajg__fru[0] + 1,) + cajg__fru[1:]
                gds__knigg = 1
            else:
                zyvs__icol = arr[i]
                woy__lbmpy = len(zyvs__icol)
                if woy__lbmpy == 0:
                    cajg__fru = (cajg__fru[0] + 1,) + cajg__fru[1:]
                    gds__knigg = 1
                    continue
                else:
                    cajg__fru = add_nested_counts(cajg__fru, zyvs__icol)
                    gds__knigg = woy__lbmpy
            if counts[i] != gds__knigg:
                raise ValueError(
                    'DataFrame.explode(): columns must have matching element counts'
                    )
        fkhxi__mvlxe = bodo.utils.utils.alloc_type(cajg__fru[0],
            jcvcs__brxbl, cajg__fru[1:])
        mtc__oaq = 0
        for i in range(n):
            if isna(arr, i):
                setna(fkhxi__mvlxe, mtc__oaq)
                mtc__oaq += 1
                continue
            zyvs__icol = arr[i]
            lgkx__ekrgv = len(zyvs__icol)
            if lgkx__ekrgv == 0:
                setna(fkhxi__mvlxe, mtc__oaq)
                mtc__oaq += 1
                continue
            fkhxi__mvlxe[mtc__oaq:mtc__oaq + lgkx__ekrgv] = zyvs__icol
            mtc__oaq += lgkx__ekrgv
        return fkhxi__mvlxe
    return impl


def get_arr_lens(arr, na_empty_as_one=True):
    return [len(cznf__cvr) for cznf__cvr in arr]


@overload(get_arr_lens, inline='always', no_unliteral=True)
def overload_get_arr_lens(arr, na_empty_as_one=True):
    na_empty_as_one = get_overload_const_bool(na_empty_as_one)
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type or is_str_arr_type(arr
        ) and not na_empty_as_one or is_bin_arr_type(arr
        ) and not na_empty_as_one, f'get_arr_lens: invalid input array type {arr}'
    if na_empty_as_one:
        dwes__egd = 'np.empty(n, np.int64)'
        lwwi__ajanw = 'out_arr[i] = 1'
        ihnd__fbfk = 'max(len(arr[i]), 1)'
    else:
        dwes__egd = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)'
        lwwi__ajanw = 'bodo.libs.array_kernels.setna(out_arr, i)'
        ihnd__fbfk = 'len(arr[i])'
    dkuc__ksmky = f"""def impl(arr, na_empty_as_one=True):
    numba.parfors.parfor.init_prange()
    n = len(arr)
    out_arr = {dwes__egd}
    for i in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(arr, i):
            {lwwi__ajanw}
        else:
            out_arr[i] = {ihnd__fbfk}
    return out_arr
    """
    tpxxu__nsdw = {}
    exec(dkuc__ksmky, {'bodo': bodo, 'numba': numba, 'np': np}, tpxxu__nsdw)
    impl = tpxxu__nsdw['impl']
    return impl


def explode_str_split(arr, pat, n, index_arr):
    return pd.Series(arr, index_arr).str.split(pat, n).explode()


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert is_str_arr_type(arr
        ), f'explode_str_split: string array expected, not {arr}'
    bip__sbc = index_arr
    rzgfg__rhmi = bip__sbc.dtype

    def impl(arr, pat, n, index_arr):
        yuf__qls = pat is not None and len(pat) > 1
        if yuf__qls:
            ible__pcd = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        iwb__ppej = len(arr)
        qzli__nltxm = 0
        ocp__bgq = 0
        rlcri__ihoqa = init_nested_counts(rzgfg__rhmi)
        for i in range(iwb__ppej):
            xszhs__ebt = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                qzli__nltxm += 1
                rlcri__ihoqa = add_nested_counts(rlcri__ihoqa, xszhs__ebt)
                continue
            if yuf__qls:
                kkjg__bev = ible__pcd.split(arr[i], maxsplit=n)
            else:
                kkjg__bev = arr[i].split(pat, n)
            qzli__nltxm += len(kkjg__bev)
            for s in kkjg__bev:
                rlcri__ihoqa = add_nested_counts(rlcri__ihoqa, xszhs__ebt)
                ocp__bgq += bodo.libs.str_arr_ext.get_utf8_size(s)
        fkhxi__mvlxe = bodo.libs.str_arr_ext.pre_alloc_string_array(qzli__nltxm
            , ocp__bgq)
        fmof__iez = bodo.utils.utils.alloc_type(qzli__nltxm, bip__sbc,
            rlcri__ihoqa)
        muoyk__tkvpb = 0
        for werm__yhl in range(iwb__ppej):
            if isna(arr, werm__yhl):
                fkhxi__mvlxe[muoyk__tkvpb] = ''
                bodo.libs.array_kernels.setna(fkhxi__mvlxe, muoyk__tkvpb)
                fmof__iez[muoyk__tkvpb] = index_arr[werm__yhl]
                muoyk__tkvpb += 1
                continue
            if yuf__qls:
                kkjg__bev = ible__pcd.split(arr[werm__yhl], maxsplit=n)
            else:
                kkjg__bev = arr[werm__yhl].split(pat, n)
            vzwx__nrjq = len(kkjg__bev)
            fkhxi__mvlxe[muoyk__tkvpb:muoyk__tkvpb + vzwx__nrjq] = kkjg__bev
            fmof__iez[muoyk__tkvpb:muoyk__tkvpb + vzwx__nrjq] = index_arr[
                werm__yhl]
            muoyk__tkvpb += vzwx__nrjq
        return fkhxi__mvlxe, fmof__iez
    return impl


def gen_na_array(n, arr):
    return np.full(n, np.nan)


@overload(gen_na_array, no_unliteral=True)
def overload_gen_na_array(n, arr, use_dict_arr=False):
    if isinstance(arr, types.TypeRef):
        arr = arr.instance_type
    dtype = arr.dtype
    if not isinstance(arr, IntegerArrayType) and isinstance(dtype, (types.
        Integer, types.Float)):
        dtype = dtype if isinstance(dtype, types.Float) else types.float64

        def impl_float(n, arr, use_dict_arr=False):
            numba.parfors.parfor.init_prange()
            fkhxi__mvlxe = np.empty(n, dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                fkhxi__mvlxe[i] = np.nan
            return fkhxi__mvlxe
        return impl_float
    if arr == bodo.dict_str_arr_type and is_overload_true(use_dict_arr):

        def impl_dict(n, arr, use_dict_arr=False):
            fqp__kss = bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0)
            fren__usz = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)
            numba.parfors.parfor.init_prange()
            for i in numba.parfors.parfor.internal_prange(n):
                setna(fren__usz, i)
            return bodo.libs.dict_arr_ext.init_dict_arr(fqp__kss, fren__usz,
                True)
        return impl_dict
    hmnxn__ezf = to_str_arr_if_dict_array(arr)

    def impl(n, arr, use_dict_arr=False):
        numba.parfors.parfor.init_prange()
        fkhxi__mvlxe = bodo.utils.utils.alloc_type(n, hmnxn__ezf, (0,))
        for i in numba.parfors.parfor.internal_prange(n):
            setna(fkhxi__mvlxe, i)
        return fkhxi__mvlxe
    return impl


def gen_na_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_array_kernels_gen_na_array = (
    gen_na_array_equiv)


def resize_and_copy(A, new_len):
    return A


@overload(resize_and_copy, no_unliteral=True)
def overload_resize_and_copy(A, old_size, new_len):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.resize_and_copy()')
    dgi__gmhkg = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            fkhxi__mvlxe = bodo.utils.utils.alloc_type(new_len, dgi__gmhkg)
            bodo.libs.str_arr_ext.str_copy_ptr(fkhxi__mvlxe.ctypes, 0, A.
                ctypes, old_size)
            return fkhxi__mvlxe
        return impl_char

    def impl(A, old_size, new_len):
        fkhxi__mvlxe = bodo.utils.utils.alloc_type(new_len, dgi__gmhkg, (-1,))
        fkhxi__mvlxe[:old_size] = A[:old_size]
        return fkhxi__mvlxe
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    ssqx__skq = math.ceil((stop - start) / step)
    return int(max(ssqx__skq, 0))


def calc_nitems_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    if guard(find_const, self.func_ir, args[0]) == 0 and guard(find_const,
        self.func_ir, args[2]) == 1:
        return ArrayAnalysis.AnalyzeResult(shape=args[1], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_array_kernels_calc_nitems = (
    calc_nitems_equiv)


def arange_parallel_impl(return_type, *args):
    dtype = as_dtype(return_type.dtype)

    def arange_1(stop):
        return np.arange(0, stop, 1, dtype)

    def arange_2(start, stop):
        return np.arange(start, stop, 1, dtype)

    def arange_3(start, stop, step):
        return np.arange(start, stop, step, dtype)
    if any(isinstance(sxls__rkki, types.Complex) for sxls__rkki in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            kayss__afer = (stop - start) / step
            ssqx__skq = math.ceil(kayss__afer.real)
            ngavq__tfm = math.ceil(kayss__afer.imag)
            hwot__ffi = int(max(min(ngavq__tfm, ssqx__skq), 0))
            arr = np.empty(hwot__ffi, dtype)
            for i in numba.parfors.parfor.internal_prange(hwot__ffi):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            hwot__ffi = bodo.libs.array_kernels.calc_nitems(start, stop, step)
            arr = np.empty(hwot__ffi, dtype)
            for i in numba.parfors.parfor.internal_prange(hwot__ffi):
                arr[i] = start + i * step
            return arr
    if len(args) == 1:
        return arange_1
    elif len(args) == 2:
        return arange_2
    elif len(args) == 3:
        return arange_3
    elif len(args) == 4:
        return arange_4
    else:
        raise BodoError('parallel arange with types {}'.format(args))


if bodo.numba_compat._check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.arange_parallel_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c72b0390b4f3e52dcc5426bd42c6b55ff96bae5a425381900985d36e7527a4bd':
        warnings.warn('numba.parfors.parfor.arange_parallel_impl has changed')
numba.parfors.parfor.swap_functions_map['arange', 'numpy'
    ] = arange_parallel_impl


def sort(arr, ascending, inplace):
    return np.sort(arr)


@overload(sort, no_unliteral=True)
def overload_sort(arr, ascending, inplace):

    def impl(arr, ascending, inplace):
        n = len(arr)
        data = np.arange(n),
        jdzq__wbj = arr,
        if not inplace:
            jdzq__wbj = arr.copy(),
        ynimz__phpg = bodo.libs.str_arr_ext.to_list_if_immutable_arr(jdzq__wbj)
        eje__kyjo = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data, True)
        bodo.libs.timsort.sort(ynimz__phpg, 0, n, eje__kyjo)
        if not ascending:
            bodo.libs.timsort.reverseRange(ynimz__phpg, 0, n, eje__kyjo)
        bodo.libs.str_arr_ext.cp_str_list_to_array(jdzq__wbj, ynimz__phpg)
        return jdzq__wbj[0]
    return impl


def overload_array_max(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).max()
        return impl


overload(np.max, inline='always', no_unliteral=True)(overload_array_max)
overload(max, inline='always', no_unliteral=True)(overload_array_max)


def overload_array_min(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).min()
        return impl


overload(np.min, inline='always', no_unliteral=True)(overload_array_min)
overload(min, inline='always', no_unliteral=True)(overload_array_min)


def overload_array_sum(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).sum()
    return impl


overload(np.sum, inline='always', no_unliteral=True)(overload_array_sum)
overload(sum, inline='always', no_unliteral=True)(overload_array_sum)


@overload(np.prod, inline='always', no_unliteral=True)
def overload_array_prod(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).prod()
    return impl


def nonzero(arr):
    return arr,


@overload(nonzero, no_unliteral=True)
def nonzero_overload(A, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.nonzero()')
    if not bodo.utils.utils.is_array_typ(A, False):
        return

    def impl(A, parallel=False):
        n = len(A)
        if parallel:
            offset = bodo.libs.distributed_api.dist_exscan(n, Reduce_Type.
                Sum.value)
        else:
            offset = 0
        uwm__yjo = []
        for i in range(n):
            if A[i]:
                uwm__yjo.append(i + offset)
        return np.array(uwm__yjo, np.int64),
    return impl


def ffill_bfill_arr(arr):
    return arr


@overload(ffill_bfill_arr, no_unliteral=True)
def ffill_bfill_overload(A, method, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.ffill_bfill_arr()')
    dgi__gmhkg = element_type(A)
    if dgi__gmhkg == types.unicode_type:
        null_value = '""'
    elif dgi__gmhkg == types.bool_:
        null_value = 'False'
    elif dgi__gmhkg == bodo.datetime64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_datetime(0))')
    elif dgi__gmhkg == bodo.timedelta64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_timedelta(0))')
    else:
        null_value = '0'
    muoyk__tkvpb = 'i'
    nxfov__fcmwd = False
    bwhd__ufvm = get_overload_const_str(method)
    if bwhd__ufvm in ('ffill', 'pad'):
        loosa__eydy = 'n'
        send_right = True
    elif bwhd__ufvm in ('backfill', 'bfill'):
        loosa__eydy = 'n-1, -1, -1'
        send_right = False
        if dgi__gmhkg == types.unicode_type:
            muoyk__tkvpb = '(n - 1) - i'
            nxfov__fcmwd = True
    dkuc__ksmky = 'def impl(A, method, parallel=False):\n'
    dkuc__ksmky += '  A = decode_if_dict_array(A)\n'
    dkuc__ksmky += '  has_last_value = False\n'
    dkuc__ksmky += f'  last_value = {null_value}\n'
    dkuc__ksmky += '  if parallel:\n'
    dkuc__ksmky += '    rank = bodo.libs.distributed_api.get_rank()\n'
    dkuc__ksmky += '    n_pes = bodo.libs.distributed_api.get_size()\n'
    dkuc__ksmky += f"""    has_last_value, last_value = null_border_icomm(A, rank, n_pes, {null_value}, {send_right})
"""
    dkuc__ksmky += '  n = len(A)\n'
    dkuc__ksmky += '  out_arr = bodo.utils.utils.alloc_type(n, A, (-1,))\n'
    dkuc__ksmky += f'  for i in range({loosa__eydy}):\n'
    dkuc__ksmky += (
        '    if (bodo.libs.array_kernels.isna(A, i) and not has_last_value):\n'
        )
    dkuc__ksmky += (
        f'      bodo.libs.array_kernels.setna(out_arr, {muoyk__tkvpb})\n')
    dkuc__ksmky += '      continue\n'
    dkuc__ksmky += '    s = A[i]\n'
    dkuc__ksmky += '    if bodo.libs.array_kernels.isna(A, i):\n'
    dkuc__ksmky += '      s = last_value\n'
    dkuc__ksmky += f'    out_arr[{muoyk__tkvpb}] = s\n'
    dkuc__ksmky += '    last_value = s\n'
    dkuc__ksmky += '    has_last_value = True\n'
    if nxfov__fcmwd:
        dkuc__ksmky += '  return out_arr[::-1]\n'
    else:
        dkuc__ksmky += '  return out_arr\n'
    kezn__vsw = {}
    exec(dkuc__ksmky, {'bodo': bodo, 'numba': numba, 'pd': pd,
        'null_border_icomm': null_border_icomm, 'decode_if_dict_array':
        decode_if_dict_array}, kezn__vsw)
    impl = kezn__vsw['impl']
    return impl


@register_jitable(cache=True)
def null_border_icomm(in_arr, rank, n_pes, null_value, send_right=True):
    if send_right:
        pvrwl__vkjgq = 0
        kcd__vfn = n_pes - 1
        jsg__bmapi = np.int32(rank + 1)
        pfnxi__yecyq = np.int32(rank - 1)
        uabh__mja = len(in_arr) - 1
        geh__rrhrs = -1
        zqt__wodnv = -1
    else:
        pvrwl__vkjgq = n_pes - 1
        kcd__vfn = 0
        jsg__bmapi = np.int32(rank - 1)
        pfnxi__yecyq = np.int32(rank + 1)
        uabh__mja = 0
        geh__rrhrs = len(in_arr)
        zqt__wodnv = 1
    mhm__swgk = np.int32(bodo.hiframes.rolling.comm_border_tag)
    qezcx__zwpe = np.empty(1, dtype=np.bool_)
    err__upt = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    yparq__upy = np.empty(1, dtype=np.bool_)
    mjvfh__oza = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    thwdy__ooa = False
    lpwfy__mkww = null_value
    for i in range(uabh__mja, geh__rrhrs, zqt__wodnv):
        if not isna(in_arr, i):
            thwdy__ooa = True
            lpwfy__mkww = in_arr[i]
            break
    if rank != pvrwl__vkjgq:
        myu__fsur = bodo.libs.distributed_api.irecv(qezcx__zwpe, 1,
            pfnxi__yecyq, mhm__swgk, True)
        bodo.libs.distributed_api.wait(myu__fsur, True)
        kgoyf__soy = bodo.libs.distributed_api.irecv(err__upt, 1,
            pfnxi__yecyq, mhm__swgk, True)
        bodo.libs.distributed_api.wait(kgoyf__soy, True)
        rgluz__agh = qezcx__zwpe[0]
        dtrmv__xctb = err__upt[0]
    else:
        rgluz__agh = False
        dtrmv__xctb = null_value
    if thwdy__ooa:
        yparq__upy[0] = thwdy__ooa
        mjvfh__oza[0] = lpwfy__mkww
    else:
        yparq__upy[0] = rgluz__agh
        mjvfh__oza[0] = dtrmv__xctb
    if rank != kcd__vfn:
        cpc__llv = bodo.libs.distributed_api.isend(yparq__upy, 1,
            jsg__bmapi, mhm__swgk, True)
        dnov__psnvr = bodo.libs.distributed_api.isend(mjvfh__oza, 1,
            jsg__bmapi, mhm__swgk, True)
    return rgluz__agh, dtrmv__xctb


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    bsmuo__cfkq = {'axis': axis, 'kind': kind, 'order': order}
    ubn__evu = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', bsmuo__cfkq, ubn__evu, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    return A


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'Series.repeat()')
    dgi__gmhkg = to_str_arr_if_dict_array(A)
    if isinstance(repeats, types.Integer):
        if A == bodo.dict_str_arr_type:

            def impl_dict_int(A, repeats):
                data_arr = A._data.copy()
                yeu__aoq = A._indices
                iwb__ppej = len(yeu__aoq)
                xhgf__lfdw = alloc_int_array(iwb__ppej * repeats, np.int32)
                for i in range(iwb__ppej):
                    muoyk__tkvpb = i * repeats
                    if bodo.libs.array_kernels.isna(yeu__aoq, i):
                        for werm__yhl in range(repeats):
                            bodo.libs.array_kernels.setna(xhgf__lfdw, 
                                muoyk__tkvpb + werm__yhl)
                    else:
                        xhgf__lfdw[muoyk__tkvpb:muoyk__tkvpb + repeats
                            ] = yeu__aoq[i]
                return init_dict_arr(data_arr, xhgf__lfdw, A.
                    _has_global_dictionary)
            return impl_dict_int

        def impl_int(A, repeats):
            iwb__ppej = len(A)
            fkhxi__mvlxe = bodo.utils.utils.alloc_type(iwb__ppej * repeats,
                dgi__gmhkg, (-1,))
            for i in range(iwb__ppej):
                muoyk__tkvpb = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for werm__yhl in range(repeats):
                        bodo.libs.array_kernels.setna(fkhxi__mvlxe, 
                            muoyk__tkvpb + werm__yhl)
                else:
                    fkhxi__mvlxe[muoyk__tkvpb:muoyk__tkvpb + repeats] = A[i]
            return fkhxi__mvlxe
        return impl_int
    if A == bodo.dict_str_arr_type:

        def impl_dict_arr(A, repeats):
            data_arr = A._data.copy()
            yeu__aoq = A._indices
            iwb__ppej = len(yeu__aoq)
            xhgf__lfdw = alloc_int_array(repeats.sum(), np.int32)
            muoyk__tkvpb = 0
            for i in range(iwb__ppej):
                aqyqz__jnb = repeats[i]
                if aqyqz__jnb < 0:
                    raise ValueError('repeats may not contain negative values.'
                        )
                if bodo.libs.array_kernels.isna(yeu__aoq, i):
                    for werm__yhl in range(aqyqz__jnb):
                        bodo.libs.array_kernels.setna(xhgf__lfdw, 
                            muoyk__tkvpb + werm__yhl)
                else:
                    xhgf__lfdw[muoyk__tkvpb:muoyk__tkvpb + aqyqz__jnb
                        ] = yeu__aoq[i]
                muoyk__tkvpb += aqyqz__jnb
            return init_dict_arr(data_arr, xhgf__lfdw, A._has_global_dictionary
                )
        return impl_dict_arr

    def impl_arr(A, repeats):
        iwb__ppej = len(A)
        fkhxi__mvlxe = bodo.utils.utils.alloc_type(repeats.sum(),
            dgi__gmhkg, (-1,))
        muoyk__tkvpb = 0
        for i in range(iwb__ppej):
            aqyqz__jnb = repeats[i]
            if aqyqz__jnb < 0:
                raise ValueError('repeats may not contain negative values.')
            if bodo.libs.array_kernels.isna(A, i):
                for werm__yhl in range(aqyqz__jnb):
                    bodo.libs.array_kernels.setna(fkhxi__mvlxe, 
                        muoyk__tkvpb + werm__yhl)
            else:
                fkhxi__mvlxe[muoyk__tkvpb:muoyk__tkvpb + aqyqz__jnb] = A[i]
            muoyk__tkvpb += aqyqz__jnb
        return fkhxi__mvlxe
    return impl_arr


@overload(np.repeat, inline='always', no_unliteral=True)
def np_repeat(A, repeats):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    if not isinstance(repeats, types.Integer):
        raise BodoError(
            'Only integer type supported for repeats in np.repeat()')

    def impl(A, repeats):
        return bodo.libs.array_kernels.repeat_kernel(A, repeats)
    return impl


@numba.generated_jit
def repeat_like(A, dist_like_arr):
    if not bodo.utils.utils.is_array_typ(A, False
        ) or not bodo.utils.utils.is_array_typ(dist_like_arr, False):
        raise BodoError('Both A and dist_like_arr must be array-like.')

    def impl(A, dist_like_arr):
        return bodo.libs.array_kernels.repeat_kernel(A, len(dist_like_arr))
    return impl


@overload(np.unique, inline='always', no_unliteral=True)
def np_unique(A):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return

    def impl(A):
        tcrp__tkue = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(tcrp__tkue, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        pnh__lyydb = bodo.libs.array_kernels.concat([A1, A2])
        qpdjq__cnbfp = bodo.libs.array_kernels.unique(pnh__lyydb)
        return pd.Series(qpdjq__cnbfp).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    bsmuo__cfkq = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    ubn__evu = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', bsmuo__cfkq, ubn__evu, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        zkcst__urmms = bodo.libs.array_kernels.unique(A1)
        jnjr__czh = bodo.libs.array_kernels.unique(A2)
        pnh__lyydb = bodo.libs.array_kernels.concat([zkcst__urmms, jnjr__czh])
        wzvv__pucej = pd.Series(pnh__lyydb).sort_values().values
        return slice_array_intersect1d(wzvv__pucej)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    tddz__caw = arr[1:] == arr[:-1]
    return arr[:-1][tddz__caw]


@register_jitable(cache=True)
def intersection_mask_comm(arr, rank, n_pes):
    mhm__swgk = np.int32(bodo.hiframes.rolling.comm_border_tag)
    vots__muj = bodo.utils.utils.alloc_type(1, arr, (-1,))
    if rank != 0:
        lhplc__ibxms = bodo.libs.distributed_api.isend(arr[:1], 1, np.int32
            (rank - 1), mhm__swgk, True)
        bodo.libs.distributed_api.wait(lhplc__ibxms, True)
    if rank == n_pes - 1:
        return None
    else:
        sdszg__dsp = bodo.libs.distributed_api.irecv(vots__muj, 1, np.int32
            (rank + 1), mhm__swgk, True)
        bodo.libs.distributed_api.wait(sdszg__dsp, True)
        return vots__muj[0]


@register_jitable(cache=True)
def intersection_mask(arr, parallel=False):
    n = len(arr)
    tddz__caw = np.full(n, False)
    for i in range(n - 1):
        if arr[i] == arr[i + 1]:
            tddz__caw[i] = True
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        mlitn__joncg = intersection_mask_comm(arr, rank, n_pes)
        if rank != n_pes - 1 and arr[n - 1] == mlitn__joncg:
            tddz__caw[n - 1] = True
    return tddz__caw


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    bsmuo__cfkq = {'assume_unique': assume_unique}
    ubn__evu = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', bsmuo__cfkq, ubn__evu, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        zkcst__urmms = bodo.libs.array_kernels.unique(A1)
        jnjr__czh = bodo.libs.array_kernels.unique(A2)
        tddz__caw = calculate_mask_setdiff1d(zkcst__urmms, jnjr__czh)
        return pd.Series(zkcst__urmms[tddz__caw]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    tddz__caw = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        tddz__caw &= A1 != A2[i]
    return tddz__caw


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    bsmuo__cfkq = {'retstep': retstep, 'axis': axis}
    ubn__evu = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', bsmuo__cfkq, ubn__evu, 'numpy')
    kxlqc__mjxpd = False
    if is_overload_none(dtype):
        dgi__gmhkg = np.promote_types(np.promote_types(numba.np.
            numpy_support.as_dtype(start), numba.np.numpy_support.as_dtype(
            stop)), numba.np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            kxlqc__mjxpd = True
        dgi__gmhkg = numba.np.numpy_support.as_dtype(dtype).type
    if kxlqc__mjxpd:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            aeiu__gwm = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            fkhxi__mvlxe = np.empty(num, dgi__gmhkg)
            for i in numba.parfors.parfor.internal_prange(num):
                fkhxi__mvlxe[i] = dgi__gmhkg(np.floor(start + i * aeiu__gwm))
            return fkhxi__mvlxe
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            aeiu__gwm = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            fkhxi__mvlxe = np.empty(num, dgi__gmhkg)
            for i in numba.parfors.parfor.internal_prange(num):
                fkhxi__mvlxe[i] = dgi__gmhkg(start + i * aeiu__gwm)
            return fkhxi__mvlxe
        return impl


def np_linspace_get_stepsize(start, stop, num, endpoint):
    return 0


@overload(np_linspace_get_stepsize, no_unliteral=True)
def overload_np_linspace_get_stepsize(start, stop, num, endpoint):

    def impl(start, stop, num, endpoint):
        if num < 0:
            raise ValueError('np.linspace() Num must be >= 0')
        if endpoint:
            num -= 1
        if num > 1:
            return (stop - start) / num
        return 0
    return impl


@overload(operator.contains, no_unliteral=True)
def arr_contains(A, val):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'np.contains()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.dtype == types.
        unliteral(val)):
        return

    def impl(A, val):
        numba.parfors.parfor.init_prange()
        ccran__kkuml = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                ccran__kkuml += A[i] == val
        return ccran__kkuml > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.any()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    bsmuo__cfkq = {'axis': axis, 'out': out, 'keepdims': keepdims}
    ubn__evu = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', bsmuo__cfkq, ubn__evu, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        ccran__kkuml = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                ccran__kkuml += int(bool(A[i]))
        return ccran__kkuml > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.all()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    bsmuo__cfkq = {'axis': axis, 'out': out, 'keepdims': keepdims}
    ubn__evu = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', bsmuo__cfkq, ubn__evu, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        ccran__kkuml = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                ccran__kkuml += int(bool(A[i]))
        return ccran__kkuml == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    bsmuo__cfkq = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    ubn__evu = {'out': None, 'where': True, 'casting': 'same_kind', 'order':
        'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', bsmuo__cfkq, ubn__evu, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        kepa__gvpsx = np.promote_types(numba.np.numpy_support.as_dtype(A.
            dtype), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            fkhxi__mvlxe = np.empty(n, kepa__gvpsx)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(fkhxi__mvlxe, i)
                    continue
                fkhxi__mvlxe[i] = np_cbrt_scalar(A[i], kepa__gvpsx)
            return fkhxi__mvlxe
        return impl_arr
    kepa__gvpsx = np.promote_types(numba.np.numpy_support.as_dtype(A),
        numba.np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, kepa__gvpsx)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    sgot__ccil = x < 0
    if sgot__ccil:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if sgot__ccil:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    srt__urj = isinstance(tup, (types.BaseTuple, types.List))
    enbh__zve = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List, bodo.NullableTupleType))
    if isinstance(tup, types.BaseTuple):
        for iuzq__zyhrc in tup.types:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                iuzq__zyhrc, 'numpy.hstack()')
            srt__urj = srt__urj and bodo.utils.utils.is_array_typ(iuzq__zyhrc,
                False)
    elif isinstance(tup, types.List):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup.dtype,
            'numpy.hstack()')
        srt__urj = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif enbh__zve:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup,
            'numpy.hstack()')
        myc__yfjn = tup.data.tuple_typ if isinstance(tup.data, bodo.
            NullableTupleType) else tup.data
        for iuzq__zyhrc in myc__yfjn.types:
            enbh__zve = enbh__zve and bodo.utils.utils.is_array_typ(iuzq__zyhrc
                , False)
    if not (srt__urj or enbh__zve):
        return
    if enbh__zve:

        def impl_series(tup):
            arr_tup = bodo.hiframes.pd_series_ext.get_series_data(tup)
            return bodo.libs.array_kernels.concat(arr_tup)
        return impl_series

    def impl(tup):
        return bodo.libs.array_kernels.concat(tup)
    return impl


@overload(np.random.multivariate_normal, inline='always', no_unliteral=True)
def np_random_multivariate_normal(mean, cov, size=None, check_valid='warn',
    tol=1e-08):
    bsmuo__cfkq = {'check_valid': check_valid, 'tol': tol}
    ubn__evu = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', bsmuo__cfkq,
        ubn__evu, 'numpy')
    if not isinstance(size, types.Integer):
        raise BodoError(
            'np.random.multivariate_normal() size argument is required and must be an integer'
            )
    if not (bodo.utils.utils.is_array_typ(mean, False) and mean.ndim == 1):
        raise BodoError(
            'np.random.multivariate_normal() mean must be a 1 dimensional numpy array'
            )
    if not (bodo.utils.utils.is_array_typ(cov, False) and cov.ndim == 2):
        raise BodoError(
            'np.random.multivariate_normal() cov must be a 2 dimensional square, numpy array'
            )

    def impl(mean, cov, size=None, check_valid='warn', tol=1e-08):
        _validate_multivar_norm(cov)
        heo__byr = mean.shape[0]
        vjk__jhnuw = size, heo__byr
        wsg__vhkd = np.random.standard_normal(vjk__jhnuw)
        cov = cov.astype(np.float64)
        wgnt__cek, s, tsil__eksa = np.linalg.svd(cov)
        res = np.dot(wsg__vhkd, np.sqrt(s).reshape(heo__byr, 1) * tsil__eksa)
        oimc__ogp = res + mean
        return oimc__ogp
    return impl


def _validate_multivar_norm(cov):
    return


@overload(_validate_multivar_norm, no_unliteral=True)
def _overload_validate_multivar_norm(cov):

    def impl(cov):
        if cov.shape[0] != cov.shape[1]:
            raise ValueError(
                'np.random.multivariate_normal() cov must be a 2 dimensional square, numpy array'
                )
    return impl


def _nan_argmin(arr):
    return


@overload(_nan_argmin, no_unliteral=True)
def _overload_nan_argmin(arr):
    if isinstance(arr, IntegerArrayType) or arr in [boolean_array,
        datetime_date_array_type] or arr.dtype == bodo.timedelta64ns:

        def impl_bodo_arr(arr):
            numba.parfors.parfor.init_prange()
            ejaq__gng = bodo.hiframes.series_kernels._get_type_max_value(arr)
            rmr__haeo = typing.builtins.IndexValue(-1, ejaq__gng)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                ispxt__jenxq = typing.builtins.IndexValue(i, arr[i])
                rmr__haeo = min(rmr__haeo, ispxt__jenxq)
            return rmr__haeo.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        bzg__wlnm = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            ore__yahs = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            ejaq__gng = bzg__wlnm(len(arr.dtype.categories) + 1)
            rmr__haeo = typing.builtins.IndexValue(-1, ejaq__gng)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                ispxt__jenxq = typing.builtins.IndexValue(i, ore__yahs[i])
                rmr__haeo = min(rmr__haeo, ispxt__jenxq)
            return rmr__haeo.index
        return impl_cat_arr
    return lambda arr: arr.argmin()


def _nan_argmax(arr):
    return


@overload(_nan_argmax, no_unliteral=True)
def _overload_nan_argmax(arr):
    if isinstance(arr, IntegerArrayType) or arr in [boolean_array,
        datetime_date_array_type] or arr.dtype == bodo.timedelta64ns:

        def impl_bodo_arr(arr):
            n = len(arr)
            numba.parfors.parfor.init_prange()
            ejaq__gng = bodo.hiframes.series_kernels._get_type_min_value(arr)
            rmr__haeo = typing.builtins.IndexValue(-1, ejaq__gng)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                ispxt__jenxq = typing.builtins.IndexValue(i, arr[i])
                rmr__haeo = max(rmr__haeo, ispxt__jenxq)
            return rmr__haeo.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        bzg__wlnm = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            n = len(arr)
            ore__yahs = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            ejaq__gng = bzg__wlnm(-1)
            rmr__haeo = typing.builtins.IndexValue(-1, ejaq__gng)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                ispxt__jenxq = typing.builtins.IndexValue(i, ore__yahs[i])
                rmr__haeo = max(rmr__haeo, ispxt__jenxq)
            return rmr__haeo.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
