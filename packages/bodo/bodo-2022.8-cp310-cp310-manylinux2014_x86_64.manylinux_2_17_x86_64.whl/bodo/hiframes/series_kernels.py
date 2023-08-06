"""Some kernels for Series related functions. This is a legacy file that needs to be
refactored.
"""
import datetime
import numba
import numpy as np
from numba.core import types
from numba.extending import overload, register_jitable
import bodo
from bodo.libs.int_arr_ext import IntDtype
from bodo.utils.typing import decode_if_dict_array


def _column_filter_impl(B, ind):
    vxmws__lanh = bodo.hiframes.rolling.alloc_shift(len(B), B, (-1,))
    for zddwy__zpih in numba.parfors.parfor.internal_prange(len(vxmws__lanh)):
        if ind[zddwy__zpih]:
            vxmws__lanh[zddwy__zpih] = B[zddwy__zpih]
        else:
            bodo.libs.array_kernels.setna(vxmws__lanh, zddwy__zpih)
    return vxmws__lanh


@numba.njit(no_cpython_wrapper=True)
def _series_dropna_str_alloc_impl_inner(B):
    B = decode_if_dict_array(B)
    dtd__rog = len(B)
    ttpch__zagr = 0
    for zddwy__zpih in range(len(B)):
        if bodo.libs.str_arr_ext.str_arr_is_na(B, zddwy__zpih):
            ttpch__zagr += 1
    kfvm__xikw = dtd__rog - ttpch__zagr
    noxb__htovn = bodo.libs.str_arr_ext.num_total_chars(B)
    vxmws__lanh = bodo.libs.str_arr_ext.pre_alloc_string_array(kfvm__xikw,
        noxb__htovn)
    bodo.libs.str_arr_ext.copy_non_null_offsets(vxmws__lanh, B)
    bodo.libs.str_arr_ext.copy_data(vxmws__lanh, B)
    bodo.libs.str_arr_ext.set_null_bits_to_value(vxmws__lanh, -1)
    return vxmws__lanh


def _get_nan(val):
    return np.nan


@overload(_get_nan, no_unliteral=True)
def _get_nan_overload(val):
    if isinstance(val, (types.NPDatetime, types.NPTimedelta)):
        nat = val('NaT')
        return lambda val: nat
    if isinstance(val, types.Float):
        return lambda val: np.nan
    return lambda val: val


def _get_type_max_value(dtype):
    return 0


@overload(_get_type_max_value, inline='always', no_unliteral=True)
def _get_type_max_value_overload(dtype):
    if isinstance(dtype, (bodo.IntegerArrayType, IntDtype)):
        _dtype = dtype.dtype
        return lambda dtype: numba.cpython.builtins.get_type_max_value(_dtype)
    if dtype == bodo.datetime_date_array_type:
        return lambda dtype: _get_date_max_value()
    if isinstance(dtype.dtype, types.NPDatetime):
        return lambda dtype: bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
            numba.cpython.builtins.get_type_max_value(numba.core.types.int64))
    if isinstance(dtype.dtype, types.NPTimedelta):
        return (lambda dtype: bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(numba.cpython.builtins.
            get_type_max_value(numba.core.types.int64)))
    if dtype.dtype == types.bool_:
        return lambda dtype: True
    return lambda dtype: numba.cpython.builtins.get_type_max_value(dtype)


@register_jitable
def _get_date_max_value():
    return datetime.date(datetime.MAXYEAR, 12, 31)


def _get_type_min_value(dtype):
    return 0


@overload(_get_type_min_value, inline='always', no_unliteral=True)
def _get_type_min_value_overload(dtype):
    if isinstance(dtype, (bodo.IntegerArrayType, IntDtype)):
        _dtype = dtype.dtype
        return lambda dtype: numba.cpython.builtins.get_type_min_value(_dtype)
    if dtype == bodo.datetime_date_array_type:
        return lambda dtype: _get_date_min_value()
    if isinstance(dtype.dtype, types.NPDatetime):
        return lambda dtype: bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
            numba.cpython.builtins.get_type_min_value(numba.core.types.int64))
    if isinstance(dtype.dtype, types.NPTimedelta):
        return (lambda dtype: bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(numba.cpython.builtins.
            get_type_min_value(numba.core.types.uint64)))
    if dtype.dtype == types.bool_:
        return lambda dtype: False
    return lambda dtype: numba.cpython.builtins.get_type_min_value(dtype)


@register_jitable
def _get_date_min_value():
    return datetime.date(datetime.MINYEAR, 1, 1)


@overload(min)
def indval_min(a1, a2):
    if a1 == types.bool_ and a2 == types.bool_:

        def min_impl(a1, a2):
            if a1 > a2:
                return a2
            return a1
        return min_impl


@overload(max)
def indval_max(a1, a2):
    if a1 == types.bool_ and a2 == types.bool_:

        def max_impl(a1, a2):
            if a2 > a1:
                return a2
            return a1
        return max_impl


@numba.njit
def _sum_handle_nan(s, count):
    if not count:
        s = bodo.hiframes.series_kernels._get_nan(s)
    return s


@numba.njit
def _box_cat_val(s, cat_dtype, count):
    if s == -1 or count == 0:
        return bodo.hiframes.series_kernels._get_nan(cat_dtype.categories[0])
    return cat_dtype.categories[s]


@numba.generated_jit
def get_float_nan(s):
    nan = np.nan
    if s == types.float32:
        nan = np.float32('nan')
    return lambda s: nan


@numba.njit
def _mean_handle_nan(s, count):
    if not count:
        s = get_float_nan(s)
    else:
        s = s / count
    return s


@numba.njit
def _var_handle_mincount(s, count, min_count):
    if count < min_count:
        res = np.nan
    else:
        res = s
    return res


@numba.njit
def _compute_var_nan_count_ddof(first_moment, second_moment, count, ddof):
    if count == 0 or count <= ddof:
        s = np.nan
    else:
        s = second_moment - first_moment * first_moment / count
        s = s / (count - ddof)
    return s


@numba.njit
def _sem_handle_nan(res, count):
    if count < 1:
        nayb__qiuj = np.nan
    else:
        nayb__qiuj = (res / count) ** 0.5
    return nayb__qiuj


@numba.njit
def lt_f(a, b):
    return a < b


@numba.njit
def gt_f(a, b):
    return a > b


@numba.njit
def compute_skew(first_moment, second_moment, third_moment, count):
    if count < 3:
        return np.nan
    cjl__cxm = first_moment / count
    ojzap__pxkpx = (third_moment - 3 * second_moment * cjl__cxm + 2 * count *
        cjl__cxm ** 3)
    uudlz__zbkb = second_moment - cjl__cxm * first_moment
    s = count * (count - 1) ** 1.5 / (count - 2
        ) * ojzap__pxkpx / uudlz__zbkb ** 1.5
    s = s / (count - 1)
    return s


@numba.njit
def compute_kurt(first_moment, second_moment, third_moment, fourth_moment,
    count):
    if count < 4:
        return np.nan
    cjl__cxm = first_moment / count
    djqic__als = (fourth_moment - 4 * third_moment * cjl__cxm + 6 *
        second_moment * cjl__cxm ** 2 - 3 * count * cjl__cxm ** 4)
    lst__ioqdr = second_moment - cjl__cxm * first_moment
    fdi__lxxle = 3 * (count - 1) ** 2 / ((count - 2) * (count - 3))
    pfvus__prwe = count * (count + 1) * (count - 1) * djqic__als
    tei__lwvlt = (count - 2) * (count - 3) * lst__ioqdr ** 2
    s = (count - 1) * (pfvus__prwe / tei__lwvlt - fdi__lxxle)
    s = s / (count - 1)
    return s
