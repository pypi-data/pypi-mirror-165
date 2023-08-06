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
        okkx__hotx = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = okkx__hotx
        return _setnan_impl
    if isinstance(arr, DatetimeArrayType):
        okkx__hotx = bodo.datetime64ns('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr._data[ind] = okkx__hotx
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
            umsnc__tmkuw = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            umsnc__tmkuw[ind + 1] = umsnc__tmkuw[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            umsnc__tmkuw = bodo.libs.array_item_arr_ext.get_offsets(arr)
            umsnc__tmkuw[ind + 1] = umsnc__tmkuw[ind]
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
    dgsm__mpdtu = arr_tup.count
    zqkn__hjd = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(dgsm__mpdtu):
        zqkn__hjd += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    zqkn__hjd += '  return\n'
    oiyau__erul = {}
    exec(zqkn__hjd, {'setna': setna}, oiyau__erul)
    impl = oiyau__erul['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        ohus__sfz = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(ohus__sfz.start, ohus__sfz.stop, ohus__sfz.step):
            setna(arr, i)
    return impl


@numba.generated_jit
def first_last_valid_index(arr, index_arr, is_first=True, parallel=False):
    is_first = get_overload_const_bool(is_first)
    if is_first:
        svvl__gjda = 'n'
        mump__bmji = 'n_pes'
        obfn__oynqn = 'min_op'
    else:
        svvl__gjda = 'n-1, -1, -1'
        mump__bmji = '-1'
        obfn__oynqn = 'max_op'
    zqkn__hjd = f"""def impl(arr, index_arr, is_first=True, parallel=False):
    n = len(arr)
    index_value = index_arr[0]
    has_valid = False
    loc_valid_rank = -1
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        loc_valid_rank = {mump__bmji}
    for i in range({svvl__gjda}):
        if not isna(arr, i):
            if parallel:
                loc_valid_rank = rank
            index_value = index_arr[i]
            has_valid = True
            break
    if parallel:
        possible_valid_rank = np.int32(bodo.libs.distributed_api.dist_reduce(loc_valid_rank, {obfn__oynqn}))
        if possible_valid_rank != {mump__bmji}:
            has_valid = True
            index_value = bodo.libs.distributed_api.bcast_scalar(index_value, possible_valid_rank)
    return has_valid, box_if_dt64(index_value)

    """
    oiyau__erul = {}
    exec(zqkn__hjd, {'np': np, 'bodo': bodo, 'isna': isna, 'max_op': max_op,
        'min_op': min_op, 'box_if_dt64': bodo.utils.conversion.box_if_dt64},
        oiyau__erul)
    impl = oiyau__erul['impl']
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    hwdsd__ybsd = array_to_info(arr)
    _median_series_computation(res, hwdsd__ybsd, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(hwdsd__ybsd)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    hwdsd__ybsd = array_to_info(arr)
    _autocorr_series_computation(res, hwdsd__ybsd, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(hwdsd__ybsd)


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
    hwdsd__ybsd = array_to_info(arr)
    _compute_series_monotonicity(res, hwdsd__ybsd, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(hwdsd__ybsd)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    xrn__jwfzq = res[0] > 0.5
    return xrn__jwfzq


@numba.generated_jit(nopython=True)
def get_valid_entries_from_date_offset(index_arr, offset, initial_date,
    is_last, is_parallel=False):
    if get_overload_const_bool(is_last):
        jslde__atzif = '-'
        ylwrm__ylk = 'index_arr[0] > threshhold_date'
        svvl__gjda = '1, n+1'
        gwe__osvlx = 'index_arr[-i] <= threshhold_date'
        dneu__sjmwd = 'i - 1'
    else:
        jslde__atzif = '+'
        ylwrm__ylk = 'index_arr[-1] < threshhold_date'
        svvl__gjda = 'n'
        gwe__osvlx = 'index_arr[i] >= threshhold_date'
        dneu__sjmwd = 'i'
    zqkn__hjd = (
        'def impl(index_arr, offset, initial_date, is_last, is_parallel=False):\n'
        )
    if types.unliteral(offset) == types.unicode_type:
        zqkn__hjd += (
            '  with numba.objmode(threshhold_date=bodo.pd_timestamp_type):\n')
        zqkn__hjd += (
            '    date_offset = pd.tseries.frequencies.to_offset(offset)\n')
        if not get_overload_const_bool(is_last):
            zqkn__hjd += """    if not isinstance(date_offset, pd._libs.tslibs.Tick) and date_offset.is_on_offset(index_arr[0]):
"""
            zqkn__hjd += (
                '      threshhold_date = initial_date - date_offset.base + date_offset\n'
                )
            zqkn__hjd += '    else:\n'
            zqkn__hjd += '      threshhold_date = initial_date + date_offset\n'
        else:
            zqkn__hjd += (
                f'    threshhold_date = initial_date {jslde__atzif} date_offset\n'
                )
    else:
        zqkn__hjd += (
            f'  threshhold_date = initial_date {jslde__atzif} offset\n')
    zqkn__hjd += '  local_valid = 0\n'
    zqkn__hjd += f'  n = len(index_arr)\n'
    zqkn__hjd += f'  if n:\n'
    zqkn__hjd += f'    if {ylwrm__ylk}:\n'
    zqkn__hjd += '      loc_valid = n\n'
    zqkn__hjd += '    else:\n'
    zqkn__hjd += f'      for i in range({svvl__gjda}):\n'
    zqkn__hjd += f'        if {gwe__osvlx}:\n'
    zqkn__hjd += f'          loc_valid = {dneu__sjmwd}\n'
    zqkn__hjd += '          break\n'
    zqkn__hjd += '  if is_parallel:\n'
    zqkn__hjd += (
        '    total_valid = bodo.libs.distributed_api.dist_reduce(loc_valid, sum_op)\n'
        )
    zqkn__hjd += '    return total_valid\n'
    zqkn__hjd += '  else:\n'
    zqkn__hjd += '    return loc_valid\n'
    oiyau__erul = {}
    exec(zqkn__hjd, {'bodo': bodo, 'pd': pd, 'numba': numba, 'sum_op':
        sum_op}, oiyau__erul)
    return oiyau__erul['impl']


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
    kzdl__gzhh = numba_to_c_type(sig.args[0].dtype)
    cbl__zqj = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType(
        32), kzdl__gzhh))
    paxt__uxu = args[0]
    bxkj__axner = sig.args[0]
    if isinstance(bxkj__axner, (IntegerArrayType, BooleanArrayType)):
        paxt__uxu = cgutils.create_struct_proxy(bxkj__axner)(context,
            builder, paxt__uxu).data
        bxkj__axner = types.Array(bxkj__axner.dtype, 1, 'C')
    assert bxkj__axner.ndim == 1
    arr = make_array(bxkj__axner)(context, builder, paxt__uxu)
    trruf__qkms = builder.extract_value(arr.shape, 0)
    mbta__udeo = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        trruf__qkms, args[1], builder.load(cbl__zqj)]
    jkwcg__mtx = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    arxp__wfw = lir.FunctionType(lir.DoubleType(), jkwcg__mtx)
    rzt__tvj = cgutils.get_or_insert_function(builder.module, arxp__wfw,
        name='quantile_sequential')
    uspru__eaea = builder.call(rzt__tvj, mbta__udeo)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return uspru__eaea


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    kzdl__gzhh = numba_to_c_type(sig.args[0].dtype)
    cbl__zqj = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType(
        32), kzdl__gzhh))
    paxt__uxu = args[0]
    bxkj__axner = sig.args[0]
    if isinstance(bxkj__axner, (IntegerArrayType, BooleanArrayType)):
        paxt__uxu = cgutils.create_struct_proxy(bxkj__axner)(context,
            builder, paxt__uxu).data
        bxkj__axner = types.Array(bxkj__axner.dtype, 1, 'C')
    assert bxkj__axner.ndim == 1
    arr = make_array(bxkj__axner)(context, builder, paxt__uxu)
    trruf__qkms = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        rkrww__zkt = args[2]
    else:
        rkrww__zkt = trruf__qkms
    mbta__udeo = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        trruf__qkms, rkrww__zkt, args[1], builder.load(cbl__zqj)]
    jkwcg__mtx = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.IntType
        (64), lir.DoubleType(), lir.IntType(32)]
    arxp__wfw = lir.FunctionType(lir.DoubleType(), jkwcg__mtx)
    rzt__tvj = cgutils.get_or_insert_function(builder.module, arxp__wfw,
        name='quantile_parallel')
    uspru__eaea = builder.call(rzt__tvj, mbta__udeo)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return uspru__eaea


@numba.generated_jit(nopython=True)
def _rank_detect_ties(arr):

    def impl(arr):
        mylbd__ojhzd = np.nonzero(pd.isna(arr))[0]
        qrmeg__ffp = arr[1:] != arr[:-1]
        qrmeg__ffp[pd.isna(qrmeg__ffp)] = False
        kcd__ksgra = qrmeg__ffp.astype(np.bool_)
        pmq__lgbk = np.concatenate((np.array([True]), kcd__ksgra))
        if mylbd__ojhzd.size:
            yxucq__ltplb, jjqu__ehtx = mylbd__ojhzd[0], mylbd__ojhzd[1:]
            pmq__lgbk[yxucq__ltplb] = True
            if jjqu__ehtx.size:
                pmq__lgbk[jjqu__ehtx] = False
                if jjqu__ehtx[-1] + 1 < pmq__lgbk.size:
                    pmq__lgbk[jjqu__ehtx[-1] + 1] = True
            elif yxucq__ltplb + 1 < pmq__lgbk.size:
                pmq__lgbk[yxucq__ltplb + 1] = True
        return pmq__lgbk
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
    zqkn__hjd = (
        "def impl(arr, method='average', na_option='keep', ascending=True, pct=False):\n"
        )
    zqkn__hjd += '  na_idxs = pd.isna(arr)\n'
    zqkn__hjd += '  sorter = bodo.hiframes.series_impl.argsort(arr)\n'
    zqkn__hjd += '  nas = sum(na_idxs)\n'
    if not ascending:
        zqkn__hjd += '  if nas and nas < (sorter.size - 1):\n'
        zqkn__hjd += '    sorter[:-nas] = sorter[-(nas + 1)::-1]\n'
        zqkn__hjd += '  else:\n'
        zqkn__hjd += '    sorter = sorter[::-1]\n'
    if na_option == 'top':
        zqkn__hjd += (
            '  sorter = np.concatenate((sorter[-nas:], sorter[:-nas]))\n')
    zqkn__hjd += '  inv = np.empty(sorter.size, dtype=np.intp)\n'
    zqkn__hjd += '  inv[sorter] = np.arange(sorter.size)\n'
    if method == 'first':
        zqkn__hjd += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
        zqkn__hjd += '    inv,\n'
        zqkn__hjd += '    new_dtype=np.float64,\n'
        zqkn__hjd += '    copy=True,\n'
        zqkn__hjd += '    nan_to_str=False,\n'
        zqkn__hjd += '    from_series=True,\n'
        zqkn__hjd += '    ) + 1\n'
    else:
        zqkn__hjd += '  arr = arr[sorter]\n'
        zqkn__hjd += '  obs = bodo.libs.array_kernels._rank_detect_ties(arr)\n'
        zqkn__hjd += '  dense = obs.cumsum()[inv]\n'
        if method == 'dense':
            zqkn__hjd += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
            zqkn__hjd += '    dense,\n'
            zqkn__hjd += '    new_dtype=np.float64,\n'
            zqkn__hjd += '    copy=True,\n'
            zqkn__hjd += '    nan_to_str=False,\n'
            zqkn__hjd += '    from_series=True,\n'
            zqkn__hjd += '  )\n'
        else:
            zqkn__hjd += (
                '  count = np.concatenate((np.nonzero(obs)[0], np.array([len(obs)])))\n'
                )
            zqkn__hjd += """  count_float = bodo.utils.conversion.fix_arr_dtype(count, new_dtype=np.float64, copy=True, nan_to_str=False, from_series=True)
"""
            if method == 'max':
                zqkn__hjd += '  ret = count_float[dense]\n'
            elif method == 'min':
                zqkn__hjd += '  ret = count_float[dense - 1] + 1\n'
            else:
                zqkn__hjd += (
                    '  ret = 0.5 * (count_float[dense] + count_float[dense - 1] + 1)\n'
                    )
    if pct:
        if method == 'dense':
            if na_option == 'keep':
                zqkn__hjd += '  ret[na_idxs] = -1\n'
            zqkn__hjd += '  div_val = np.max(ret)\n'
        elif na_option == 'keep':
            zqkn__hjd += '  div_val = arr.size - nas\n'
        else:
            zqkn__hjd += '  div_val = arr.size\n'
        zqkn__hjd += '  for i in range(len(ret)):\n'
        zqkn__hjd += '    ret[i] = ret[i] / div_val\n'
    if na_option == 'keep':
        zqkn__hjd += '  ret[na_idxs] = np.nan\n'
    zqkn__hjd += '  return ret\n'
    oiyau__erul = {}
    exec(zqkn__hjd, {'np': np, 'pd': pd, 'bodo': bodo}, oiyau__erul)
    return oiyau__erul['impl']


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    pbipc__lcequ = start
    pis__mqs = 2 * start + 1
    ulwtn__sfela = 2 * start + 2
    if pis__mqs < n and not cmp_f(arr[pis__mqs], arr[pbipc__lcequ]):
        pbipc__lcequ = pis__mqs
    if ulwtn__sfela < n and not cmp_f(arr[ulwtn__sfela], arr[pbipc__lcequ]):
        pbipc__lcequ = ulwtn__sfela
    if pbipc__lcequ != start:
        arr[start], arr[pbipc__lcequ] = arr[pbipc__lcequ], arr[start]
        ind_arr[start], ind_arr[pbipc__lcequ] = ind_arr[pbipc__lcequ], ind_arr[
            start]
        min_heapify(arr, ind_arr, n, pbipc__lcequ, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        zsb__srmq = np.empty(k, A.dtype)
        jqp__chq = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                zsb__srmq[ind] = A[i]
                jqp__chq[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            zsb__srmq = zsb__srmq[:ind]
            jqp__chq = jqp__chq[:ind]
        return zsb__srmq, jqp__chq, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        zaca__eszoe = np.sort(A)
        octzy__chlyk = index_arr[np.argsort(A)]
        ppaos__mdr = pd.Series(zaca__eszoe).notna().values
        zaca__eszoe = zaca__eszoe[ppaos__mdr]
        octzy__chlyk = octzy__chlyk[ppaos__mdr]
        if is_largest:
            zaca__eszoe = zaca__eszoe[::-1]
            octzy__chlyk = octzy__chlyk[::-1]
        return np.ascontiguousarray(zaca__eszoe), np.ascontiguousarray(
            octzy__chlyk)
    zsb__srmq, jqp__chq, start = select_k_nonan(A, index_arr, m, k)
    jqp__chq = jqp__chq[zsb__srmq.argsort()]
    zsb__srmq.sort()
    if not is_largest:
        zsb__srmq = np.ascontiguousarray(zsb__srmq[::-1])
        jqp__chq = np.ascontiguousarray(jqp__chq[::-1])
    for i in range(start, m):
        if cmp_f(A[i], zsb__srmq[0]):
            zsb__srmq[0] = A[i]
            jqp__chq[0] = index_arr[i]
            min_heapify(zsb__srmq, jqp__chq, k, 0, cmp_f)
    jqp__chq = jqp__chq[zsb__srmq.argsort()]
    zsb__srmq.sort()
    if is_largest:
        zsb__srmq = zsb__srmq[::-1]
        jqp__chq = jqp__chq[::-1]
    return np.ascontiguousarray(zsb__srmq), np.ascontiguousarray(jqp__chq)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    ialhz__lezc = bodo.libs.distributed_api.get_rank()
    jigvr__cro, odxog__yaz = nlargest(A, I, k, is_largest, cmp_f)
    tfkcz__nimqc = bodo.libs.distributed_api.gatherv(jigvr__cro)
    cbi__mcj = bodo.libs.distributed_api.gatherv(odxog__yaz)
    if ialhz__lezc == MPI_ROOT:
        res, mkfw__ebbp = nlargest(tfkcz__nimqc, cbi__mcj, k, is_largest, cmp_f
            )
    else:
        res = np.empty(k, A.dtype)
        mkfw__ebbp = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(mkfw__ebbp)
    return res, mkfw__ebbp


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    xpnes__xjk, ymcuk__olo = mat.shape
    uff__jdru = np.empty((ymcuk__olo, ymcuk__olo), dtype=np.float64)
    for psm__okqe in range(ymcuk__olo):
        for kqv__vdi in range(psm__okqe + 1):
            orc__ootp = 0
            adb__iwuae = dck__ckd = ywz__uxi = dyjan__rfbz = 0.0
            for i in range(xpnes__xjk):
                if np.isfinite(mat[i, psm__okqe]) and np.isfinite(mat[i,
                    kqv__vdi]):
                    savwe__nwp = mat[i, psm__okqe]
                    nfsij__typ = mat[i, kqv__vdi]
                    orc__ootp += 1
                    ywz__uxi += savwe__nwp
                    dyjan__rfbz += nfsij__typ
            if parallel:
                orc__ootp = bodo.libs.distributed_api.dist_reduce(orc__ootp,
                    sum_op)
                ywz__uxi = bodo.libs.distributed_api.dist_reduce(ywz__uxi,
                    sum_op)
                dyjan__rfbz = bodo.libs.distributed_api.dist_reduce(dyjan__rfbz
                    , sum_op)
            if orc__ootp < minpv:
                uff__jdru[psm__okqe, kqv__vdi] = uff__jdru[kqv__vdi, psm__okqe
                    ] = np.nan
            else:
                tfrgi__sct = ywz__uxi / orc__ootp
                sglv__pbdga = dyjan__rfbz / orc__ootp
                ywz__uxi = 0.0
                for i in range(xpnes__xjk):
                    if np.isfinite(mat[i, psm__okqe]) and np.isfinite(mat[i,
                        kqv__vdi]):
                        savwe__nwp = mat[i, psm__okqe] - tfrgi__sct
                        nfsij__typ = mat[i, kqv__vdi] - sglv__pbdga
                        ywz__uxi += savwe__nwp * nfsij__typ
                        adb__iwuae += savwe__nwp * savwe__nwp
                        dck__ckd += nfsij__typ * nfsij__typ
                if parallel:
                    ywz__uxi = bodo.libs.distributed_api.dist_reduce(ywz__uxi,
                        sum_op)
                    adb__iwuae = bodo.libs.distributed_api.dist_reduce(
                        adb__iwuae, sum_op)
                    dck__ckd = bodo.libs.distributed_api.dist_reduce(dck__ckd,
                        sum_op)
                wae__ogziu = orc__ootp - 1.0 if cov else sqrt(adb__iwuae *
                    dck__ckd)
                if wae__ogziu != 0.0:
                    uff__jdru[psm__okqe, kqv__vdi] = uff__jdru[kqv__vdi,
                        psm__okqe] = ywz__uxi / wae__ogziu
                else:
                    uff__jdru[psm__okqe, kqv__vdi] = uff__jdru[kqv__vdi,
                        psm__okqe] = np.nan
    return uff__jdru


@numba.generated_jit(nopython=True)
def duplicated(data, parallel=False):
    n = len(data)
    if n == 0:
        return lambda data, parallel=False: np.empty(0, dtype=np.bool_)
    hrrxk__xhpu = n != 1
    zqkn__hjd = 'def impl(data, parallel=False):\n'
    zqkn__hjd += '  if parallel:\n'
    edxk__quqsf = ', '.join(f'array_to_info(data[{i}])' for i in range(n))
    zqkn__hjd += f'    cpp_table = arr_info_list_to_table([{edxk__quqsf}])\n'
    zqkn__hjd += (
        f'    out_cpp_table = bodo.libs.array.shuffle_table(cpp_table, {n}, parallel, 1)\n'
        )
    watjn__yykx = ', '.join(
        f'info_to_array(info_from_table(out_cpp_table, {i}), data[{i}])' for
        i in range(n))
    zqkn__hjd += f'    data = ({watjn__yykx},)\n'
    zqkn__hjd += (
        '    shuffle_info = bodo.libs.array.get_shuffle_info(out_cpp_table)\n')
    zqkn__hjd += '    bodo.libs.array.delete_table(out_cpp_table)\n'
    zqkn__hjd += '    bodo.libs.array.delete_table(cpp_table)\n'
    zqkn__hjd += '  n = len(data[0])\n'
    zqkn__hjd += '  out = np.empty(n, np.bool_)\n'
    zqkn__hjd += '  uniqs = dict()\n'
    if hrrxk__xhpu:
        zqkn__hjd += '  for i in range(n):\n'
        cgq__peh = ', '.join(f'data[{i}][i]' for i in range(n))
        bfcwl__mjt = ',  '.join(
            f'bodo.libs.array_kernels.isna(data[{i}], i)' for i in range(n))
        zqkn__hjd += f"""    val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({cgq__peh},), ({bfcwl__mjt},))
"""
        zqkn__hjd += '    if val in uniqs:\n'
        zqkn__hjd += '      out[i] = True\n'
        zqkn__hjd += '    else:\n'
        zqkn__hjd += '      out[i] = False\n'
        zqkn__hjd += '      uniqs[val] = 0\n'
    else:
        zqkn__hjd += '  data = data[0]\n'
        zqkn__hjd += '  hasna = False\n'
        zqkn__hjd += '  for i in range(n):\n'
        zqkn__hjd += '    if bodo.libs.array_kernels.isna(data, i):\n'
        zqkn__hjd += '      out[i] = hasna\n'
        zqkn__hjd += '      hasna = True\n'
        zqkn__hjd += '    else:\n'
        zqkn__hjd += '      val = data[i]\n'
        zqkn__hjd += '      if val in uniqs:\n'
        zqkn__hjd += '        out[i] = True\n'
        zqkn__hjd += '      else:\n'
        zqkn__hjd += '        out[i] = False\n'
        zqkn__hjd += '        uniqs[val] = 0\n'
    zqkn__hjd += '  if parallel:\n'
    zqkn__hjd += (
        '    out = bodo.hiframes.pd_groupby_ext.reverse_shuffle(out, shuffle_info)\n'
        )
    zqkn__hjd += '  return out\n'
    oiyau__erul = {}
    exec(zqkn__hjd, {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table}, oiyau__erul)
    impl = oiyau__erul['impl']
    return impl


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    return data, ind_arr


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    dgsm__mpdtu = len(data)
    zqkn__hjd = 'def impl(data, ind_arr, n, frac, replace, parallel=False):\n'
    zqkn__hjd += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        dgsm__mpdtu)))
    zqkn__hjd += '  table_total = arr_info_list_to_table(info_list_total)\n'
    zqkn__hjd += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(dgsm__mpdtu))
    for pibx__nsqpg in range(dgsm__mpdtu):
        zqkn__hjd += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(pibx__nsqpg, pibx__nsqpg, pibx__nsqpg))
    zqkn__hjd += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(dgsm__mpdtu))
    zqkn__hjd += '  delete_table(out_table)\n'
    zqkn__hjd += '  delete_table(table_total)\n'
    zqkn__hjd += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(dgsm__mpdtu)))
    oiyau__erul = {}
    exec(zqkn__hjd, {'np': np, 'bodo': bodo, 'array_to_info': array_to_info,
        'sample_table': sample_table, 'arr_info_list_to_table':
        arr_info_list_to_table, 'info_from_table': info_from_table,
        'info_to_array': info_to_array, 'delete_table': delete_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, oiyau__erul)
    impl = oiyau__erul['impl']
    return impl


def drop_duplicates(data, ind_arr, ncols, parallel=False):
    return data, ind_arr


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, ncols, parallel=False):
    dgsm__mpdtu = len(data)
    zqkn__hjd = 'def impl(data, ind_arr, ncols, parallel=False):\n'
    zqkn__hjd += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        dgsm__mpdtu)))
    zqkn__hjd += '  table_total = arr_info_list_to_table(info_list_total)\n'
    zqkn__hjd += '  keep_i = 0\n'
    zqkn__hjd += """  out_table = drop_duplicates_table(table_total, parallel, ncols, keep_i, False, True)
"""
    for pibx__nsqpg in range(dgsm__mpdtu):
        zqkn__hjd += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(pibx__nsqpg, pibx__nsqpg, pibx__nsqpg))
    zqkn__hjd += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(dgsm__mpdtu))
    zqkn__hjd += '  delete_table(out_table)\n'
    zqkn__hjd += '  delete_table(table_total)\n'
    zqkn__hjd += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(dgsm__mpdtu)))
    oiyau__erul = {}
    exec(zqkn__hjd, {'np': np, 'bodo': bodo, 'array_to_info': array_to_info,
        'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, oiyau__erul)
    impl = oiyau__erul['impl']
    return impl


def drop_duplicates_array(data_arr, parallel=False):
    return data_arr


@overload(drop_duplicates_array, no_unliteral=True)
def overload_drop_duplicates_array(data_arr, parallel=False):

    def impl(data_arr, parallel=False):
        bqneg__pxbwc = [array_to_info(data_arr)]
        rbxn__gao = arr_info_list_to_table(bqneg__pxbwc)
        rlf__klhxu = 0
        jjnl__qlzs = drop_duplicates_table(rbxn__gao, parallel, 1,
            rlf__klhxu, False, True)
        vkwc__otd = info_to_array(info_from_table(jjnl__qlzs, 0), data_arr)
        delete_table(jjnl__qlzs)
        delete_table(rbxn__gao)
        return vkwc__otd
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    return data


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.dropna()')
    ctz__wywp = len(data.types)
    acw__hdb = [('out' + str(i)) for i in range(ctz__wywp)]
    gdp__emo = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    sbii__sla = ['isna(data[{}], i)'.format(i) for i in gdp__emo]
    dbah__qpwx = 'not ({})'.format(' or '.join(sbii__sla))
    if not is_overload_none(thresh):
        dbah__qpwx = '(({}) <= ({}) - thresh)'.format(' + '.join(sbii__sla),
            ctz__wywp - 1)
    elif how == 'all':
        dbah__qpwx = 'not ({})'.format(' and '.join(sbii__sla))
    zqkn__hjd = 'def _dropna_imp(data, how, thresh, subset):\n'
    zqkn__hjd += '  old_len = len(data[0])\n'
    zqkn__hjd += '  new_len = 0\n'
    zqkn__hjd += '  for i in range(old_len):\n'
    zqkn__hjd += '    if {}:\n'.format(dbah__qpwx)
    zqkn__hjd += '      new_len += 1\n'
    for i, out in enumerate(acw__hdb):
        if isinstance(data[i], bodo.CategoricalArrayType):
            zqkn__hjd += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            zqkn__hjd += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    zqkn__hjd += '  curr_ind = 0\n'
    zqkn__hjd += '  for i in range(old_len):\n'
    zqkn__hjd += '    if {}:\n'.format(dbah__qpwx)
    for i in range(ctz__wywp):
        zqkn__hjd += '      if isna(data[{}], i):\n'.format(i)
        zqkn__hjd += '        setna({}, curr_ind)\n'.format(acw__hdb[i])
        zqkn__hjd += '      else:\n'
        zqkn__hjd += '        {}[curr_ind] = data[{}][i]\n'.format(acw__hdb
            [i], i)
    zqkn__hjd += '      curr_ind += 1\n'
    zqkn__hjd += '  return {}\n'.format(', '.join(acw__hdb))
    oiyau__erul = {}
    qbd__lxezd = {'t{}'.format(i): iutip__bwni for i, iutip__bwni in
        enumerate(data.types)}
    qbd__lxezd.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(zqkn__hjd, qbd__lxezd, oiyau__erul)
    uaxu__lre = oiyau__erul['_dropna_imp']
    return uaxu__lre


def get(arr, ind):
    return pd.Series(arr).str.get(ind)


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        bxkj__axner = arr.dtype
        hgkma__wjsf = bxkj__axner.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            coit__awaf = init_nested_counts(hgkma__wjsf)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                coit__awaf = add_nested_counts(coit__awaf, val[ind])
            vkwc__otd = bodo.utils.utils.alloc_type(n, bxkj__axner, coit__awaf)
            for qacr__dcunm in range(n):
                if bodo.libs.array_kernels.isna(arr, qacr__dcunm):
                    setna(vkwc__otd, qacr__dcunm)
                    continue
                val = arr[qacr__dcunm]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(vkwc__otd, qacr__dcunm)
                    continue
                vkwc__otd[qacr__dcunm] = val[ind]
            return vkwc__otd
        return get_arr_item


def _is_same_categorical_array_type(arr_types):
    from bodo.hiframes.pd_categorical_ext import _to_readonly
    if not isinstance(arr_types, types.BaseTuple) or len(arr_types) == 0:
        return False
    raodj__hdans = _to_readonly(arr_types.types[0])
    return all(isinstance(iutip__bwni, CategoricalArrayType) and 
        _to_readonly(iutip__bwni) == raodj__hdans for iutip__bwni in
        arr_types.types)


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
        gjlf__ucj = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            dju__nwbye = 0
            bozf__alk = []
            for A in arr_list:
                pmw__rrza = len(A)
                bodo.libs.array_item_arr_ext.trim_excess_data(A)
                bozf__alk.append(bodo.libs.array_item_arr_ext.get_data(A))
                dju__nwbye += pmw__rrza
            ghem__gfc = np.empty(dju__nwbye + 1, offset_type)
            heyy__gqv = bodo.libs.array_kernels.concat(bozf__alk)
            uhjz__illqa = np.empty(dju__nwbye + 7 >> 3, np.uint8)
            ejia__txk = 0
            zzz__pujic = 0
            for A in arr_list:
                fusp__rmvji = bodo.libs.array_item_arr_ext.get_offsets(A)
                eepow__otfmn = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                pmw__rrza = len(A)
                evl__uxu = fusp__rmvji[pmw__rrza]
                for i in range(pmw__rrza):
                    ghem__gfc[i + ejia__txk] = fusp__rmvji[i] + zzz__pujic
                    ahy__xlooy = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        eepow__otfmn, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(uhjz__illqa, i +
                        ejia__txk, ahy__xlooy)
                ejia__txk += pmw__rrza
                zzz__pujic += evl__uxu
            ghem__gfc[ejia__txk] = zzz__pujic
            vkwc__otd = bodo.libs.array_item_arr_ext.init_array_item_array(
                dju__nwbye, heyy__gqv, ghem__gfc, uhjz__illqa)
            return vkwc__otd
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.StructArrayType):
        cey__oyxii = arr_list.dtype.names
        zqkn__hjd = 'def struct_array_concat_impl(arr_list):\n'
        zqkn__hjd += f'    n_all = 0\n'
        for i in range(len(cey__oyxii)):
            zqkn__hjd += f'    concat_list{i} = []\n'
        zqkn__hjd += '    for A in arr_list:\n'
        zqkn__hjd += (
            '        data_tuple = bodo.libs.struct_arr_ext.get_data(A)\n')
        for i in range(len(cey__oyxii)):
            zqkn__hjd += f'        concat_list{i}.append(data_tuple[{i}])\n'
        zqkn__hjd += '        n_all += len(A)\n'
        zqkn__hjd += '    n_bytes = (n_all + 7) >> 3\n'
        zqkn__hjd += '    new_mask = np.empty(n_bytes, np.uint8)\n'
        zqkn__hjd += '    curr_bit = 0\n'
        zqkn__hjd += '    for A in arr_list:\n'
        zqkn__hjd += (
            '        old_mask = bodo.libs.struct_arr_ext.get_null_bitmap(A)\n')
        zqkn__hjd += '        for j in range(len(A)):\n'
        zqkn__hjd += (
            '            bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        zqkn__hjd += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        zqkn__hjd += '            curr_bit += 1\n'
        zqkn__hjd += '    return bodo.libs.struct_arr_ext.init_struct_arr(\n'
        asx__dagw = ', '.join([
            f'bodo.libs.array_kernels.concat(concat_list{i})' for i in
            range(len(cey__oyxii))])
        zqkn__hjd += f'        ({asx__dagw},),\n'
        zqkn__hjd += '        new_mask,\n'
        zqkn__hjd += f'        {cey__oyxii},\n'
        zqkn__hjd += '    )\n'
        oiyau__erul = {}
        exec(zqkn__hjd, {'bodo': bodo, 'np': np}, oiyau__erul)
        return oiyau__erul['struct_array_concat_impl']
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            bwqi__cqxr = 0
            for A in arr_list:
                bwqi__cqxr += len(A)
            brat__fcej = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(bwqi__cqxr))
            wegp__tfo = 0
            for A in arr_list:
                for i in range(len(A)):
                    brat__fcej._data[i + wegp__tfo] = A._data[i]
                    ahy__xlooy = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(brat__fcej.
                        _null_bitmap, i + wegp__tfo, ahy__xlooy)
                wegp__tfo += len(A)
            return brat__fcej
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            bwqi__cqxr = 0
            for A in arr_list:
                bwqi__cqxr += len(A)
            brat__fcej = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(bwqi__cqxr))
            wegp__tfo = 0
            for A in arr_list:
                for i in range(len(A)):
                    brat__fcej._days_data[i + wegp__tfo] = A._days_data[i]
                    brat__fcej._seconds_data[i + wegp__tfo] = A._seconds_data[i
                        ]
                    brat__fcej._microseconds_data[i + wegp__tfo
                        ] = A._microseconds_data[i]
                    ahy__xlooy = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(brat__fcej.
                        _null_bitmap, i + wegp__tfo, ahy__xlooy)
                wegp__tfo += len(A)
            return brat__fcej
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        nlqx__gyzsq = arr_list.dtype.precision
        ybu__yac = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            bwqi__cqxr = 0
            for A in arr_list:
                bwqi__cqxr += len(A)
            brat__fcej = bodo.libs.decimal_arr_ext.alloc_decimal_array(
                bwqi__cqxr, nlqx__gyzsq, ybu__yac)
            wegp__tfo = 0
            for A in arr_list:
                for i in range(len(A)):
                    brat__fcej._data[i + wegp__tfo] = A._data[i]
                    ahy__xlooy = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(brat__fcej.
                        _null_bitmap, i + wegp__tfo, ahy__xlooy)
                wegp__tfo += len(A)
            return brat__fcej
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and (is_str_arr_type
        (arr_list.dtype) or arr_list.dtype == bodo.binary_array_type
        ) or isinstance(arr_list, types.BaseTuple) and all(is_str_arr_type(
        iutip__bwni) for iutip__bwni in arr_list.types):
        if isinstance(arr_list, types.BaseTuple):
            ffnh__uyw = arr_list.types[0]
            for i in range(len(arr_list)):
                if arr_list.types[i] != bodo.dict_str_arr_type:
                    ffnh__uyw = arr_list.types[i]
                    break
        else:
            ffnh__uyw = arr_list.dtype
        if ffnh__uyw == bodo.dict_str_arr_type:

            def impl_dict_arr(arr_list):
                vrzyh__dznpj = 0
                hlrpc__uqtj = 0
                qpg__dqy = 0
                for A in arr_list:
                    data_arr = A._data
                    qax__aeqss = A._indices
                    qpg__dqy += len(qax__aeqss)
                    vrzyh__dznpj += len(data_arr)
                    hlrpc__uqtj += bodo.libs.str_arr_ext.num_total_chars(
                        data_arr)
                efq__aeq = pre_alloc_string_array(vrzyh__dznpj, hlrpc__uqtj)
                jin__fpnh = bodo.libs.int_arr_ext.alloc_int_array(qpg__dqy,
                    np.int32)
                bodo.libs.str_arr_ext.set_null_bits_to_value(efq__aeq, -1)
                vpt__ticp = 0
                ehcf__zci = 0
                sznu__pofcl = 0
                for A in arr_list:
                    data_arr = A._data
                    qax__aeqss = A._indices
                    qpg__dqy = len(qax__aeqss)
                    bodo.libs.str_arr_ext.set_string_array_range(efq__aeq,
                        data_arr, vpt__ticp, ehcf__zci)
                    for i in range(qpg__dqy):
                        if bodo.libs.array_kernels.isna(qax__aeqss, i
                            ) or bodo.libs.array_kernels.isna(data_arr,
                            qax__aeqss[i]):
                            bodo.libs.array_kernels.setna(jin__fpnh, 
                                sznu__pofcl + i)
                        else:
                            jin__fpnh[sznu__pofcl + i
                                ] = vpt__ticp + qax__aeqss[i]
                    vpt__ticp += len(data_arr)
                    ehcf__zci += bodo.libs.str_arr_ext.num_total_chars(data_arr
                        )
                    sznu__pofcl += qpg__dqy
                vkwc__otd = init_dict_arr(efq__aeq, jin__fpnh, False)
                fpank__qfms = convert_local_dictionary_to_global(vkwc__otd,
                    False)
                return fpank__qfms
            return impl_dict_arr

        def impl_str(arr_list):
            arr_list = decode_if_dict_array(arr_list)
            vrzyh__dznpj = 0
            hlrpc__uqtj = 0
            for A in arr_list:
                arr = A
                vrzyh__dznpj += len(arr)
                hlrpc__uqtj += bodo.libs.str_arr_ext.num_total_chars(arr)
            vkwc__otd = bodo.utils.utils.alloc_type(vrzyh__dznpj, ffnh__uyw,
                (hlrpc__uqtj,))
            bodo.libs.str_arr_ext.set_null_bits_to_value(vkwc__otd, -1)
            vpt__ticp = 0
            ehcf__zci = 0
            for A in arr_list:
                arr = A
                bodo.libs.str_arr_ext.set_string_array_range(vkwc__otd, arr,
                    vpt__ticp, ehcf__zci)
                vpt__ticp += len(arr)
                ehcf__zci += bodo.libs.str_arr_ext.num_total_chars(arr)
            return vkwc__otd
        return impl_str
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(iutip__bwni.dtype, types.Integer) for
        iutip__bwni in arr_list.types) and any(isinstance(iutip__bwni,
        IntegerArrayType) for iutip__bwni in arr_list.types):

        def impl_int_arr_list(arr_list):
            jlscm__kvku = convert_to_nullable_tup(arr_list)
            kbjcu__hucnd = []
            ucj__kuwkz = 0
            for A in jlscm__kvku:
                kbjcu__hucnd.append(A._data)
                ucj__kuwkz += len(A)
            heyy__gqv = bodo.libs.array_kernels.concat(kbjcu__hucnd)
            iszy__autoo = ucj__kuwkz + 7 >> 3
            iur__tbbh = np.empty(iszy__autoo, np.uint8)
            quri__hniqw = 0
            for A in jlscm__kvku:
                jtu__lgr = A._null_bitmap
                for qacr__dcunm in range(len(A)):
                    ahy__xlooy = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        jtu__lgr, qacr__dcunm)
                    bodo.libs.int_arr_ext.set_bit_to_arr(iur__tbbh,
                        quri__hniqw, ahy__xlooy)
                    quri__hniqw += 1
            return bodo.libs.int_arr_ext.init_integer_array(heyy__gqv,
                iur__tbbh)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(iutip__bwni.dtype == types.bool_ for
        iutip__bwni in arr_list.types) and any(iutip__bwni == boolean_array for
        iutip__bwni in arr_list.types):

        def impl_bool_arr_list(arr_list):
            jlscm__kvku = convert_to_nullable_tup(arr_list)
            kbjcu__hucnd = []
            ucj__kuwkz = 0
            for A in jlscm__kvku:
                kbjcu__hucnd.append(A._data)
                ucj__kuwkz += len(A)
            heyy__gqv = bodo.libs.array_kernels.concat(kbjcu__hucnd)
            iszy__autoo = ucj__kuwkz + 7 >> 3
            iur__tbbh = np.empty(iszy__autoo, np.uint8)
            quri__hniqw = 0
            for A in jlscm__kvku:
                jtu__lgr = A._null_bitmap
                for qacr__dcunm in range(len(A)):
                    ahy__xlooy = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        jtu__lgr, qacr__dcunm)
                    bodo.libs.int_arr_ext.set_bit_to_arr(iur__tbbh,
                        quri__hniqw, ahy__xlooy)
                    quri__hniqw += 1
            return bodo.libs.bool_arr_ext.init_bool_array(heyy__gqv, iur__tbbh)
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            mif__uzl = []
            for A in arr_list:
                mif__uzl.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                mif__uzl), arr_list[0].dtype)
        return cat_array_concat_impl
    if _is_same_categorical_array_type(arr_list):
        zowpk__cug = ', '.join(f'arr_list[{i}].codes' for i in range(len(
            arr_list)))
        zqkn__hjd = 'def impl(arr_list):\n'
        zqkn__hjd += f"""    return init_categorical_array(bodo.libs.array_kernels.concat(({zowpk__cug},)), arr_list[0].dtype)
"""
        ubii__emsx = {}
        exec(zqkn__hjd, {'bodo': bodo, 'init_categorical_array':
            init_categorical_array}, ubii__emsx)
        return ubii__emsx['impl']
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            ucj__kuwkz = 0
            for A in arr_list:
                ucj__kuwkz += len(A)
            vkwc__otd = np.empty(ucj__kuwkz, dtype)
            pbnn__llsy = 0
            for A in arr_list:
                n = len(A)
                vkwc__otd[pbnn__llsy:pbnn__llsy + n] = A
                pbnn__llsy += n
            return vkwc__otd
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(iutip__bwni,
        (types.Array, IntegerArrayType)) and isinstance(iutip__bwni.dtype,
        types.Integer) for iutip__bwni in arr_list.types) and any(
        isinstance(iutip__bwni, types.Array) and isinstance(iutip__bwni.
        dtype, types.Float) for iutip__bwni in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.MapArrayType):

        def impl_map_arr_list(arr_list):
            mytc__qlf = []
            for A in arr_list:
                mytc__qlf.append(A._data)
            fldei__rowbk = bodo.libs.array_kernels.concat(mytc__qlf)
            uff__jdru = bodo.libs.map_arr_ext.init_map_arr(fldei__rowbk)
            return uff__jdru
        return impl_map_arr_list
    for oybb__cuwsl in arr_list:
        if not isinstance(oybb__cuwsl, types.Array):
            raise_bodo_error(f'concat of array types {arr_list} not supported')
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(iutip__bwni.astype(np.float64) for iutip__bwni in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    dgsm__mpdtu = len(arr_tup.types)
    zqkn__hjd = 'def f(arr_tup):\n'
    zqkn__hjd += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(
        dgsm__mpdtu)), ',' if dgsm__mpdtu == 1 else '')
    oiyau__erul = {}
    exec(zqkn__hjd, {'np': np}, oiyau__erul)
    kmh__altri = oiyau__erul['f']
    return kmh__altri


def convert_to_nullable_tup(arr_tup):
    return arr_tup


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple)
    dgsm__mpdtu = len(arr_tup.types)
    dny__utmb = find_common_np_dtype(arr_tup.types)
    hgkma__wjsf = None
    wbwi__nme = ''
    if isinstance(dny__utmb, types.Integer):
        hgkma__wjsf = bodo.libs.int_arr_ext.IntDtype(dny__utmb)
        wbwi__nme = '.astype(out_dtype, False)'
    zqkn__hjd = 'def f(arr_tup):\n'
    zqkn__hjd += '  return ({}{})\n'.format(','.join(
        'bodo.utils.conversion.coerce_to_array(arr_tup[{}], use_nullable_array=True){}'
        .format(i, wbwi__nme) for i in range(dgsm__mpdtu)), ',' if 
        dgsm__mpdtu == 1 else '')
    oiyau__erul = {}
    exec(zqkn__hjd, {'bodo': bodo, 'out_dtype': hgkma__wjsf}, oiyau__erul)
    wfqb__hfvu = oiyau__erul['f']
    return wfqb__hfvu


def nunique(A, dropna):
    return len(set(A))


def nunique_parallel(A, dropna):
    return len(set(A))


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, bsku__kbv = build_set_seen_na(A)
        return len(s) + int(not dropna and bsku__kbv)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        xce__fou = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        pim__xbts = len(xce__fou)
        return bodo.libs.distributed_api.dist_reduce(pim__xbts, np.int32(
            sum_op))
    return nunique_par


def unique(A, dropna=False, parallel=False):
    return np.array([fkdko__mxzm for fkdko__mxzm in set(A)]).astype(A.dtype)


def cummin(A):
    return A


@overload(cummin, no_unliteral=True)
def cummin_overload(A):
    if isinstance(A.dtype, types.Float):
        bgr__ngce = np.finfo(A.dtype(1).dtype).max
    else:
        bgr__ngce = np.iinfo(A.dtype(1).dtype).max

    def impl(A):
        n = len(A)
        vkwc__otd = np.empty(n, A.dtype)
        ucume__agwec = bgr__ngce
        for i in range(n):
            ucume__agwec = min(ucume__agwec, A[i])
            vkwc__otd[i] = ucume__agwec
        return vkwc__otd
    return impl


def cummax(A):
    return A


@overload(cummax, no_unliteral=True)
def cummax_overload(A):
    if isinstance(A.dtype, types.Float):
        bgr__ngce = np.finfo(A.dtype(1).dtype).min
    else:
        bgr__ngce = np.iinfo(A.dtype(1).dtype).min

    def impl(A):
        n = len(A)
        vkwc__otd = np.empty(n, A.dtype)
        ucume__agwec = bgr__ngce
        for i in range(n):
            ucume__agwec = max(ucume__agwec, A[i])
            vkwc__otd[i] = ucume__agwec
        return vkwc__otd
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        wepi__znmup = arr_info_list_to_table([array_to_info(A)])
        zcp__mmykq = 1
        rlf__klhxu = 0
        jjnl__qlzs = drop_duplicates_table(wepi__znmup, parallel,
            zcp__mmykq, rlf__klhxu, dropna, True)
        vkwc__otd = info_to_array(info_from_table(jjnl__qlzs, 0), A)
        delete_table(wepi__znmup)
        delete_table(jjnl__qlzs)
        return vkwc__otd
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    gjlf__ucj = bodo.utils.typing.to_nullable_type(arr.dtype)
    ztsv__lun = index_arr
    yjru__kno = ztsv__lun.dtype

    def impl(arr, index_arr):
        n = len(arr)
        coit__awaf = init_nested_counts(gjlf__ucj)
        wmf__waqo = init_nested_counts(yjru__kno)
        for i in range(n):
            shp__xsz = index_arr[i]
            if isna(arr, i):
                coit__awaf = (coit__awaf[0] + 1,) + coit__awaf[1:]
                wmf__waqo = add_nested_counts(wmf__waqo, shp__xsz)
                continue
            hipmx__rzkqf = arr[i]
            if len(hipmx__rzkqf) == 0:
                coit__awaf = (coit__awaf[0] + 1,) + coit__awaf[1:]
                wmf__waqo = add_nested_counts(wmf__waqo, shp__xsz)
                continue
            coit__awaf = add_nested_counts(coit__awaf, hipmx__rzkqf)
            for loaet__kqiw in range(len(hipmx__rzkqf)):
                wmf__waqo = add_nested_counts(wmf__waqo, shp__xsz)
        vkwc__otd = bodo.utils.utils.alloc_type(coit__awaf[0], gjlf__ucj,
            coit__awaf[1:])
        qlqe__dbgr = bodo.utils.utils.alloc_type(coit__awaf[0], ztsv__lun,
            wmf__waqo)
        zzz__pujic = 0
        for i in range(n):
            if isna(arr, i):
                setna(vkwc__otd, zzz__pujic)
                qlqe__dbgr[zzz__pujic] = index_arr[i]
                zzz__pujic += 1
                continue
            hipmx__rzkqf = arr[i]
            evl__uxu = len(hipmx__rzkqf)
            if evl__uxu == 0:
                setna(vkwc__otd, zzz__pujic)
                qlqe__dbgr[zzz__pujic] = index_arr[i]
                zzz__pujic += 1
                continue
            vkwc__otd[zzz__pujic:zzz__pujic + evl__uxu] = hipmx__rzkqf
            qlqe__dbgr[zzz__pujic:zzz__pujic + evl__uxu] = index_arr[i]
            zzz__pujic += evl__uxu
        return vkwc__otd, qlqe__dbgr
    return impl


def explode_no_index(arr):
    return pd.Series(arr).explode()


@overload(explode_no_index, no_unliteral=True)
def overload_explode_no_index(arr, counts):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    gjlf__ucj = bodo.utils.typing.to_nullable_type(arr.dtype)

    def impl(arr, counts):
        n = len(arr)
        coit__awaf = init_nested_counts(gjlf__ucj)
        for i in range(n):
            if isna(arr, i):
                coit__awaf = (coit__awaf[0] + 1,) + coit__awaf[1:]
                lbfw__taw = 1
            else:
                hipmx__rzkqf = arr[i]
                zvh__izzpv = len(hipmx__rzkqf)
                if zvh__izzpv == 0:
                    coit__awaf = (coit__awaf[0] + 1,) + coit__awaf[1:]
                    lbfw__taw = 1
                    continue
                else:
                    coit__awaf = add_nested_counts(coit__awaf, hipmx__rzkqf)
                    lbfw__taw = zvh__izzpv
            if counts[i] != lbfw__taw:
                raise ValueError(
                    'DataFrame.explode(): columns must have matching element counts'
                    )
        vkwc__otd = bodo.utils.utils.alloc_type(coit__awaf[0], gjlf__ucj,
            coit__awaf[1:])
        zzz__pujic = 0
        for i in range(n):
            if isna(arr, i):
                setna(vkwc__otd, zzz__pujic)
                zzz__pujic += 1
                continue
            hipmx__rzkqf = arr[i]
            evl__uxu = len(hipmx__rzkqf)
            if evl__uxu == 0:
                setna(vkwc__otd, zzz__pujic)
                zzz__pujic += 1
                continue
            vkwc__otd[zzz__pujic:zzz__pujic + evl__uxu] = hipmx__rzkqf
            zzz__pujic += evl__uxu
        return vkwc__otd
    return impl


def get_arr_lens(arr, na_empty_as_one=True):
    return [len(duqt__wmns) for duqt__wmns in arr]


@overload(get_arr_lens, inline='always', no_unliteral=True)
def overload_get_arr_lens(arr, na_empty_as_one=True):
    na_empty_as_one = get_overload_const_bool(na_empty_as_one)
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type or is_str_arr_type(arr
        ) and not na_empty_as_one or is_bin_arr_type(arr
        ) and not na_empty_as_one, f'get_arr_lens: invalid input array type {arr}'
    if na_empty_as_one:
        qbst__zvv = 'np.empty(n, np.int64)'
        dndv__euv = 'out_arr[i] = 1'
        cfhs__wefc = 'max(len(arr[i]), 1)'
    else:
        qbst__zvv = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)'
        dndv__euv = 'bodo.libs.array_kernels.setna(out_arr, i)'
        cfhs__wefc = 'len(arr[i])'
    zqkn__hjd = f"""def impl(arr, na_empty_as_one=True):
    numba.parfors.parfor.init_prange()
    n = len(arr)
    out_arr = {qbst__zvv}
    for i in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(arr, i):
            {dndv__euv}
        else:
            out_arr[i] = {cfhs__wefc}
    return out_arr
    """
    oiyau__erul = {}
    exec(zqkn__hjd, {'bodo': bodo, 'numba': numba, 'np': np}, oiyau__erul)
    impl = oiyau__erul['impl']
    return impl


def explode_str_split(arr, pat, n, index_arr):
    return pd.Series(arr, index_arr).str.split(pat, n).explode()


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert is_str_arr_type(arr
        ), f'explode_str_split: string array expected, not {arr}'
    ztsv__lun = index_arr
    yjru__kno = ztsv__lun.dtype

    def impl(arr, pat, n, index_arr):
        asd__mahtx = pat is not None and len(pat) > 1
        if asd__mahtx:
            clpp__zwunt = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        jjx__rsgyg = len(arr)
        vrzyh__dznpj = 0
        hlrpc__uqtj = 0
        wmf__waqo = init_nested_counts(yjru__kno)
        for i in range(jjx__rsgyg):
            shp__xsz = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                vrzyh__dznpj += 1
                wmf__waqo = add_nested_counts(wmf__waqo, shp__xsz)
                continue
            if asd__mahtx:
                medf__kbac = clpp__zwunt.split(arr[i], maxsplit=n)
            else:
                medf__kbac = arr[i].split(pat, n)
            vrzyh__dznpj += len(medf__kbac)
            for s in medf__kbac:
                wmf__waqo = add_nested_counts(wmf__waqo, shp__xsz)
                hlrpc__uqtj += bodo.libs.str_arr_ext.get_utf8_size(s)
        vkwc__otd = bodo.libs.str_arr_ext.pre_alloc_string_array(vrzyh__dznpj,
            hlrpc__uqtj)
        qlqe__dbgr = bodo.utils.utils.alloc_type(vrzyh__dznpj, ztsv__lun,
            wmf__waqo)
        zntsf__kjkgs = 0
        for qacr__dcunm in range(jjx__rsgyg):
            if isna(arr, qacr__dcunm):
                vkwc__otd[zntsf__kjkgs] = ''
                bodo.libs.array_kernels.setna(vkwc__otd, zntsf__kjkgs)
                qlqe__dbgr[zntsf__kjkgs] = index_arr[qacr__dcunm]
                zntsf__kjkgs += 1
                continue
            if asd__mahtx:
                medf__kbac = clpp__zwunt.split(arr[qacr__dcunm], maxsplit=n)
            else:
                medf__kbac = arr[qacr__dcunm].split(pat, n)
            rrtj__vbqj = len(medf__kbac)
            vkwc__otd[zntsf__kjkgs:zntsf__kjkgs + rrtj__vbqj] = medf__kbac
            qlqe__dbgr[zntsf__kjkgs:zntsf__kjkgs + rrtj__vbqj] = index_arr[
                qacr__dcunm]
            zntsf__kjkgs += rrtj__vbqj
        return vkwc__otd, qlqe__dbgr
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
            vkwc__otd = np.empty(n, dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                vkwc__otd[i] = np.nan
            return vkwc__otd
        return impl_float
    if arr == bodo.dict_str_arr_type and is_overload_true(use_dict_arr):

        def impl_dict(n, arr, use_dict_arr=False):
            zja__obfd = bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0)
            moypb__kbeu = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)
            numba.parfors.parfor.init_prange()
            for i in numba.parfors.parfor.internal_prange(n):
                setna(moypb__kbeu, i)
            return bodo.libs.dict_arr_ext.init_dict_arr(zja__obfd,
                moypb__kbeu, True)
        return impl_dict
    yadg__tquwq = to_str_arr_if_dict_array(arr)

    def impl(n, arr, use_dict_arr=False):
        numba.parfors.parfor.init_prange()
        vkwc__otd = bodo.utils.utils.alloc_type(n, yadg__tquwq, (0,))
        for i in numba.parfors.parfor.internal_prange(n):
            setna(vkwc__otd, i)
        return vkwc__otd
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
    mfhhi__jjl = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            vkwc__otd = bodo.utils.utils.alloc_type(new_len, mfhhi__jjl)
            bodo.libs.str_arr_ext.str_copy_ptr(vkwc__otd.ctypes, 0, A.
                ctypes, old_size)
            return vkwc__otd
        return impl_char

    def impl(A, old_size, new_len):
        vkwc__otd = bodo.utils.utils.alloc_type(new_len, mfhhi__jjl, (-1,))
        vkwc__otd[:old_size] = A[:old_size]
        return vkwc__otd
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    fjyub__lxjne = math.ceil((stop - start) / step)
    return int(max(fjyub__lxjne, 0))


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
    if any(isinstance(fkdko__mxzm, types.Complex) for fkdko__mxzm in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            wxp__vvp = (stop - start) / step
            fjyub__lxjne = math.ceil(wxp__vvp.real)
            lajdj__eka = math.ceil(wxp__vvp.imag)
            shgiy__xck = int(max(min(lajdj__eka, fjyub__lxjne), 0))
            arr = np.empty(shgiy__xck, dtype)
            for i in numba.parfors.parfor.internal_prange(shgiy__xck):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            shgiy__xck = bodo.libs.array_kernels.calc_nitems(start, stop, step)
            arr = np.empty(shgiy__xck, dtype)
            for i in numba.parfors.parfor.internal_prange(shgiy__xck):
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
        ihxh__pjr = arr,
        if not inplace:
            ihxh__pjr = arr.copy(),
        kbod__nfmg = bodo.libs.str_arr_ext.to_list_if_immutable_arr(ihxh__pjr)
        jup__dujl = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data, True)
        bodo.libs.timsort.sort(kbod__nfmg, 0, n, jup__dujl)
        if not ascending:
            bodo.libs.timsort.reverseRange(kbod__nfmg, 0, n, jup__dujl)
        bodo.libs.str_arr_ext.cp_str_list_to_array(ihxh__pjr, kbod__nfmg)
        return ihxh__pjr[0]
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
        uff__jdru = []
        for i in range(n):
            if A[i]:
                uff__jdru.append(i + offset)
        return np.array(uff__jdru, np.int64),
    return impl


def ffill_bfill_arr(arr):
    return arr


@overload(ffill_bfill_arr, no_unliteral=True)
def ffill_bfill_overload(A, method, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.ffill_bfill_arr()')
    mfhhi__jjl = element_type(A)
    if mfhhi__jjl == types.unicode_type:
        null_value = '""'
    elif mfhhi__jjl == types.bool_:
        null_value = 'False'
    elif mfhhi__jjl == bodo.datetime64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_datetime(0))')
    elif mfhhi__jjl == bodo.timedelta64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_timedelta(0))')
    else:
        null_value = '0'
    zntsf__kjkgs = 'i'
    illkk__hbgva = False
    emd__smhu = get_overload_const_str(method)
    if emd__smhu in ('ffill', 'pad'):
        zfq__zooi = 'n'
        send_right = True
    elif emd__smhu in ('backfill', 'bfill'):
        zfq__zooi = 'n-1, -1, -1'
        send_right = False
        if mfhhi__jjl == types.unicode_type:
            zntsf__kjkgs = '(n - 1) - i'
            illkk__hbgva = True
    zqkn__hjd = 'def impl(A, method, parallel=False):\n'
    zqkn__hjd += '  A = decode_if_dict_array(A)\n'
    zqkn__hjd += '  has_last_value = False\n'
    zqkn__hjd += f'  last_value = {null_value}\n'
    zqkn__hjd += '  if parallel:\n'
    zqkn__hjd += '    rank = bodo.libs.distributed_api.get_rank()\n'
    zqkn__hjd += '    n_pes = bodo.libs.distributed_api.get_size()\n'
    zqkn__hjd += f"""    has_last_value, last_value = null_border_icomm(A, rank, n_pes, {null_value}, {send_right})
"""
    zqkn__hjd += '  n = len(A)\n'
    zqkn__hjd += '  out_arr = bodo.utils.utils.alloc_type(n, A, (-1,))\n'
    zqkn__hjd += f'  for i in range({zfq__zooi}):\n'
    zqkn__hjd += (
        '    if (bodo.libs.array_kernels.isna(A, i) and not has_last_value):\n'
        )
    zqkn__hjd += (
        f'      bodo.libs.array_kernels.setna(out_arr, {zntsf__kjkgs})\n')
    zqkn__hjd += '      continue\n'
    zqkn__hjd += '    s = A[i]\n'
    zqkn__hjd += '    if bodo.libs.array_kernels.isna(A, i):\n'
    zqkn__hjd += '      s = last_value\n'
    zqkn__hjd += f'    out_arr[{zntsf__kjkgs}] = s\n'
    zqkn__hjd += '    last_value = s\n'
    zqkn__hjd += '    has_last_value = True\n'
    if illkk__hbgva:
        zqkn__hjd += '  return out_arr[::-1]\n'
    else:
        zqkn__hjd += '  return out_arr\n'
    gvwds__doqlh = {}
    exec(zqkn__hjd, {'bodo': bodo, 'numba': numba, 'pd': pd,
        'null_border_icomm': null_border_icomm, 'decode_if_dict_array':
        decode_if_dict_array}, gvwds__doqlh)
    impl = gvwds__doqlh['impl']
    return impl


@register_jitable(cache=True)
def null_border_icomm(in_arr, rank, n_pes, null_value, send_right=True):
    if send_right:
        trwki__whc = 0
        mpoo__ctvmi = n_pes - 1
        acfvh__puuhg = np.int32(rank + 1)
        hadze__fdmoa = np.int32(rank - 1)
        upb__iisn = len(in_arr) - 1
        fng__yoqya = -1
        yzope__uwvhy = -1
    else:
        trwki__whc = n_pes - 1
        mpoo__ctvmi = 0
        acfvh__puuhg = np.int32(rank - 1)
        hadze__fdmoa = np.int32(rank + 1)
        upb__iisn = 0
        fng__yoqya = len(in_arr)
        yzope__uwvhy = 1
    zrwd__pek = np.int32(bodo.hiframes.rolling.comm_border_tag)
    fsk__uje = np.empty(1, dtype=np.bool_)
    kxu__sjka = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    gejbx__odmn = np.empty(1, dtype=np.bool_)
    mbqs__lfg = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    yqalb__hthvj = False
    grc__yaq = null_value
    for i in range(upb__iisn, fng__yoqya, yzope__uwvhy):
        if not isna(in_arr, i):
            yqalb__hthvj = True
            grc__yaq = in_arr[i]
            break
    if rank != trwki__whc:
        kyeek__doq = bodo.libs.distributed_api.irecv(fsk__uje, 1,
            hadze__fdmoa, zrwd__pek, True)
        bodo.libs.distributed_api.wait(kyeek__doq, True)
        qllh__ztl = bodo.libs.distributed_api.irecv(kxu__sjka, 1,
            hadze__fdmoa, zrwd__pek, True)
        bodo.libs.distributed_api.wait(qllh__ztl, True)
        xpp__uogy = fsk__uje[0]
        xtuqj__gqip = kxu__sjka[0]
    else:
        xpp__uogy = False
        xtuqj__gqip = null_value
    if yqalb__hthvj:
        gejbx__odmn[0] = yqalb__hthvj
        mbqs__lfg[0] = grc__yaq
    else:
        gejbx__odmn[0] = xpp__uogy
        mbqs__lfg[0] = xtuqj__gqip
    if rank != mpoo__ctvmi:
        iazjc__rnj = bodo.libs.distributed_api.isend(gejbx__odmn, 1,
            acfvh__puuhg, zrwd__pek, True)
        ijj__tem = bodo.libs.distributed_api.isend(mbqs__lfg, 1,
            acfvh__puuhg, zrwd__pek, True)
    return xpp__uogy, xtuqj__gqip


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    ziun__rmmpn = {'axis': axis, 'kind': kind, 'order': order}
    xyup__qfb = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', ziun__rmmpn, xyup__qfb, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    return A


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'Series.repeat()')
    mfhhi__jjl = to_str_arr_if_dict_array(A)
    if isinstance(repeats, types.Integer):
        if A == bodo.dict_str_arr_type:

            def impl_dict_int(A, repeats):
                data_arr = A._data.copy()
                qax__aeqss = A._indices
                jjx__rsgyg = len(qax__aeqss)
                jin__fpnh = alloc_int_array(jjx__rsgyg * repeats, np.int32)
                for i in range(jjx__rsgyg):
                    zntsf__kjkgs = i * repeats
                    if bodo.libs.array_kernels.isna(qax__aeqss, i):
                        for qacr__dcunm in range(repeats):
                            bodo.libs.array_kernels.setna(jin__fpnh, 
                                zntsf__kjkgs + qacr__dcunm)
                    else:
                        jin__fpnh[zntsf__kjkgs:zntsf__kjkgs + repeats
                            ] = qax__aeqss[i]
                return init_dict_arr(data_arr, jin__fpnh, A.
                    _has_global_dictionary)
            return impl_dict_int

        def impl_int(A, repeats):
            jjx__rsgyg = len(A)
            vkwc__otd = bodo.utils.utils.alloc_type(jjx__rsgyg * repeats,
                mfhhi__jjl, (-1,))
            for i in range(jjx__rsgyg):
                zntsf__kjkgs = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for qacr__dcunm in range(repeats):
                        bodo.libs.array_kernels.setna(vkwc__otd, 
                            zntsf__kjkgs + qacr__dcunm)
                else:
                    vkwc__otd[zntsf__kjkgs:zntsf__kjkgs + repeats] = A[i]
            return vkwc__otd
        return impl_int
    if A == bodo.dict_str_arr_type:

        def impl_dict_arr(A, repeats):
            data_arr = A._data.copy()
            qax__aeqss = A._indices
            jjx__rsgyg = len(qax__aeqss)
            jin__fpnh = alloc_int_array(repeats.sum(), np.int32)
            zntsf__kjkgs = 0
            for i in range(jjx__rsgyg):
                yky__wgy = repeats[i]
                if yky__wgy < 0:
                    raise ValueError('repeats may not contain negative values.'
                        )
                if bodo.libs.array_kernels.isna(qax__aeqss, i):
                    for qacr__dcunm in range(yky__wgy):
                        bodo.libs.array_kernels.setna(jin__fpnh, 
                            zntsf__kjkgs + qacr__dcunm)
                else:
                    jin__fpnh[zntsf__kjkgs:zntsf__kjkgs + yky__wgy
                        ] = qax__aeqss[i]
                zntsf__kjkgs += yky__wgy
            return init_dict_arr(data_arr, jin__fpnh, A._has_global_dictionary)
        return impl_dict_arr

    def impl_arr(A, repeats):
        jjx__rsgyg = len(A)
        vkwc__otd = bodo.utils.utils.alloc_type(repeats.sum(), mfhhi__jjl,
            (-1,))
        zntsf__kjkgs = 0
        for i in range(jjx__rsgyg):
            yky__wgy = repeats[i]
            if yky__wgy < 0:
                raise ValueError('repeats may not contain negative values.')
            if bodo.libs.array_kernels.isna(A, i):
                for qacr__dcunm in range(yky__wgy):
                    bodo.libs.array_kernels.setna(vkwc__otd, zntsf__kjkgs +
                        qacr__dcunm)
            else:
                vkwc__otd[zntsf__kjkgs:zntsf__kjkgs + yky__wgy] = A[i]
            zntsf__kjkgs += yky__wgy
        return vkwc__otd
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
        yib__yhst = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(yib__yhst, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        hud__itj = bodo.libs.array_kernels.concat([A1, A2])
        wgzuw__rwcxk = bodo.libs.array_kernels.unique(hud__itj)
        return pd.Series(wgzuw__rwcxk).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    ziun__rmmpn = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    xyup__qfb = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', ziun__rmmpn, xyup__qfb, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        odg__pmqg = bodo.libs.array_kernels.unique(A1)
        aii__qvxtk = bodo.libs.array_kernels.unique(A2)
        hud__itj = bodo.libs.array_kernels.concat([odg__pmqg, aii__qvxtk])
        help__npbb = pd.Series(hud__itj).sort_values().values
        return slice_array_intersect1d(help__npbb)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    ppaos__mdr = arr[1:] == arr[:-1]
    return arr[:-1][ppaos__mdr]


@register_jitable(cache=True)
def intersection_mask_comm(arr, rank, n_pes):
    zrwd__pek = np.int32(bodo.hiframes.rolling.comm_border_tag)
    kvs__ttv = bodo.utils.utils.alloc_type(1, arr, (-1,))
    if rank != 0:
        evjp__hoo = bodo.libs.distributed_api.isend(arr[:1], 1, np.int32(
            rank - 1), zrwd__pek, True)
        bodo.libs.distributed_api.wait(evjp__hoo, True)
    if rank == n_pes - 1:
        return None
    else:
        rgsva__omw = bodo.libs.distributed_api.irecv(kvs__ttv, 1, np.int32(
            rank + 1), zrwd__pek, True)
        bodo.libs.distributed_api.wait(rgsva__omw, True)
        return kvs__ttv[0]


@register_jitable(cache=True)
def intersection_mask(arr, parallel=False):
    n = len(arr)
    ppaos__mdr = np.full(n, False)
    for i in range(n - 1):
        if arr[i] == arr[i + 1]:
            ppaos__mdr[i] = True
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        jbx__ags = intersection_mask_comm(arr, rank, n_pes)
        if rank != n_pes - 1 and arr[n - 1] == jbx__ags:
            ppaos__mdr[n - 1] = True
    return ppaos__mdr


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    ziun__rmmpn = {'assume_unique': assume_unique}
    xyup__qfb = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', ziun__rmmpn, xyup__qfb, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        odg__pmqg = bodo.libs.array_kernels.unique(A1)
        aii__qvxtk = bodo.libs.array_kernels.unique(A2)
        ppaos__mdr = calculate_mask_setdiff1d(odg__pmqg, aii__qvxtk)
        return pd.Series(odg__pmqg[ppaos__mdr]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    ppaos__mdr = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        ppaos__mdr &= A1 != A2[i]
    return ppaos__mdr


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    ziun__rmmpn = {'retstep': retstep, 'axis': axis}
    xyup__qfb = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', ziun__rmmpn, xyup__qfb, 'numpy')
    enlxd__vtnyv = False
    if is_overload_none(dtype):
        mfhhi__jjl = np.promote_types(np.promote_types(numba.np.
            numpy_support.as_dtype(start), numba.np.numpy_support.as_dtype(
            stop)), numba.np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            enlxd__vtnyv = True
        mfhhi__jjl = numba.np.numpy_support.as_dtype(dtype).type
    if enlxd__vtnyv:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            hbb__atey = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            vkwc__otd = np.empty(num, mfhhi__jjl)
            for i in numba.parfors.parfor.internal_prange(num):
                vkwc__otd[i] = mfhhi__jjl(np.floor(start + i * hbb__atey))
            return vkwc__otd
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            hbb__atey = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            vkwc__otd = np.empty(num, mfhhi__jjl)
            for i in numba.parfors.parfor.internal_prange(num):
                vkwc__otd[i] = mfhhi__jjl(start + i * hbb__atey)
            return vkwc__otd
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
        dgsm__mpdtu = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                dgsm__mpdtu += A[i] == val
        return dgsm__mpdtu > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.any()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    ziun__rmmpn = {'axis': axis, 'out': out, 'keepdims': keepdims}
    xyup__qfb = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', ziun__rmmpn, xyup__qfb, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        dgsm__mpdtu = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                dgsm__mpdtu += int(bool(A[i]))
        return dgsm__mpdtu > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.all()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    ziun__rmmpn = {'axis': axis, 'out': out, 'keepdims': keepdims}
    xyup__qfb = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', ziun__rmmpn, xyup__qfb, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        dgsm__mpdtu = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                dgsm__mpdtu += int(bool(A[i]))
        return dgsm__mpdtu == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    ziun__rmmpn = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    xyup__qfb = {'out': None, 'where': True, 'casting': 'same_kind',
        'order': 'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', ziun__rmmpn, xyup__qfb, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        khpk__ppv = np.promote_types(numba.np.numpy_support.as_dtype(A.
            dtype), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            vkwc__otd = np.empty(n, khpk__ppv)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(vkwc__otd, i)
                    continue
                vkwc__otd[i] = np_cbrt_scalar(A[i], khpk__ppv)
            return vkwc__otd
        return impl_arr
    khpk__ppv = np.promote_types(numba.np.numpy_support.as_dtype(A), numba.
        np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, khpk__ppv)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    ykaz__eylj = x < 0
    if ykaz__eylj:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if ykaz__eylj:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    hesn__ktxv = isinstance(tup, (types.BaseTuple, types.List))
    xalmf__gyxi = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List, bodo.NullableTupleType))
    if isinstance(tup, types.BaseTuple):
        for oybb__cuwsl in tup.types:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                oybb__cuwsl, 'numpy.hstack()')
            hesn__ktxv = hesn__ktxv and bodo.utils.utils.is_array_typ(
                oybb__cuwsl, False)
    elif isinstance(tup, types.List):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup.dtype,
            'numpy.hstack()')
        hesn__ktxv = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif xalmf__gyxi:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup,
            'numpy.hstack()')
        kcus__crqds = tup.data.tuple_typ if isinstance(tup.data, bodo.
            NullableTupleType) else tup.data
        for oybb__cuwsl in kcus__crqds.types:
            xalmf__gyxi = xalmf__gyxi and bodo.utils.utils.is_array_typ(
                oybb__cuwsl, False)
    if not (hesn__ktxv or xalmf__gyxi):
        return
    if xalmf__gyxi:

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
    ziun__rmmpn = {'check_valid': check_valid, 'tol': tol}
    xyup__qfb = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', ziun__rmmpn,
        xyup__qfb, 'numpy')
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
        xpnes__xjk = mean.shape[0]
        xamhj__cnyt = size, xpnes__xjk
        wbzjh__vpqgf = np.random.standard_normal(xamhj__cnyt)
        cov = cov.astype(np.float64)
        wdy__kmfw, s, aneg__qgfd = np.linalg.svd(cov)
        res = np.dot(wbzjh__vpqgf, np.sqrt(s).reshape(xpnes__xjk, 1) *
            aneg__qgfd)
        dgxie__zmt = res + mean
        return dgxie__zmt
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
            mump__bmji = bodo.hiframes.series_kernels._get_type_max_value(arr)
            birc__nvz = typing.builtins.IndexValue(-1, mump__bmji)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                hiupn__wps = typing.builtins.IndexValue(i, arr[i])
                birc__nvz = min(birc__nvz, hiupn__wps)
            return birc__nvz.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        ejak__chtyn = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            cyspv__xlrww = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            mump__bmji = ejak__chtyn(len(arr.dtype.categories) + 1)
            birc__nvz = typing.builtins.IndexValue(-1, mump__bmji)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                hiupn__wps = typing.builtins.IndexValue(i, cyspv__xlrww[i])
                birc__nvz = min(birc__nvz, hiupn__wps)
            return birc__nvz.index
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
            mump__bmji = bodo.hiframes.series_kernels._get_type_min_value(arr)
            birc__nvz = typing.builtins.IndexValue(-1, mump__bmji)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                hiupn__wps = typing.builtins.IndexValue(i, arr[i])
                birc__nvz = max(birc__nvz, hiupn__wps)
            return birc__nvz.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        ejak__chtyn = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            n = len(arr)
            cyspv__xlrww = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            mump__bmji = ejak__chtyn(-1)
            birc__nvz = typing.builtins.IndexValue(-1, mump__bmji)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                hiupn__wps = typing.builtins.IndexValue(i, cyspv__xlrww[i])
                birc__nvz = max(birc__nvz, hiupn__wps)
            return birc__nvz.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
