"""
Implements array operations for usage by DataFrames and Series
such as count and max.
"""
import numba
import numpy as np
import pandas as pd
from numba import generated_jit
from numba.core import types
from numba.extending import overload
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.utils import tracing
from bodo.utils.typing import element_type, is_hashable_type, is_iterable_type, is_overload_true, is_overload_zero, is_str_arr_type


def array_op_any(arr, skipna=True):
    pass


@overload(array_op_any)
def overload_array_op_any(A, skipna=True):
    if isinstance(A, types.Array) and isinstance(A.dtype, types.Integer
        ) or isinstance(A, bodo.libs.int_arr_ext.IntegerArrayType):
        fxzuo__pnykk = 0
    elif isinstance(A, bodo.libs.bool_arr_ext.BooleanArrayType) or isinstance(A
        , types.Array) and A.dtype == types.bool_:
        fxzuo__pnykk = False
    elif A == bodo.string_array_type:
        fxzuo__pnykk = ''
    elif A == bodo.binary_array_type:
        fxzuo__pnykk = b''
    else:
        raise bodo.utils.typing.BodoError(
            f'Cannot perform any with this array type: {A}')

    def impl(A, skipna=True):
        numba.parfors.parfor.init_prange()
        mdurr__jkb = 0
        for ldl__dia in numba.parfors.parfor.internal_prange(len(A)):
            if not bodo.libs.array_kernels.isna(A, ldl__dia):
                if A[ldl__dia] != fxzuo__pnykk:
                    mdurr__jkb += 1
        return mdurr__jkb != 0
    return impl


def array_op_all(arr, skipna=True):
    pass


@overload(array_op_all)
def overload_array_op_all(A, skipna=True):
    if isinstance(A, types.Array) and isinstance(A.dtype, types.Integer
        ) or isinstance(A, bodo.libs.int_arr_ext.IntegerArrayType):
        fxzuo__pnykk = 0
    elif isinstance(A, bodo.libs.bool_arr_ext.BooleanArrayType) or isinstance(A
        , types.Array) and A.dtype == types.bool_:
        fxzuo__pnykk = False
    elif A == bodo.string_array_type:
        fxzuo__pnykk = ''
    elif A == bodo.binary_array_type:
        fxzuo__pnykk = b''
    else:
        raise bodo.utils.typing.BodoError(
            f'Cannot perform all with this array type: {A}')

    def impl(A, skipna=True):
        numba.parfors.parfor.init_prange()
        mdurr__jkb = 0
        for ldl__dia in numba.parfors.parfor.internal_prange(len(A)):
            if not bodo.libs.array_kernels.isna(A, ldl__dia):
                if A[ldl__dia] == fxzuo__pnykk:
                    mdurr__jkb += 1
        return mdurr__jkb == 0
    return impl


@numba.njit
def array_op_median(arr, skipna=True, parallel=False):
    vjpd__arss = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(vjpd__arss.ctypes,
        arr, parallel, skipna)
    return vjpd__arss[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        bpiht__hab = len(arr)
        ywnc__wssan = np.empty(bpiht__hab, np.bool_)
        for ldl__dia in numba.parfors.parfor.internal_prange(bpiht__hab):
            ywnc__wssan[ldl__dia] = bodo.libs.array_kernels.isna(arr, ldl__dia)
        return ywnc__wssan
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        mdurr__jkb = 0
        for ldl__dia in numba.parfors.parfor.internal_prange(len(arr)):
            wgjdf__mnfx = 0
            if not bodo.libs.array_kernels.isna(arr, ldl__dia):
                wgjdf__mnfx = 1
            mdurr__jkb += wgjdf__mnfx
        vjpd__arss = mdurr__jkb
        return vjpd__arss
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    dkmf__fhfj = array_op_count(arr)
    swogk__svl = array_op_min(arr)
    mvr__wbdbr = array_op_max(arr)
    hnaaw__nzma = array_op_mean(arr)
    ozda__ucprl = array_op_std(arr)
    zep__rtamq = array_op_quantile(arr, 0.25)
    tkwmu__zpy = array_op_quantile(arr, 0.5)
    dwqs__jmauv = array_op_quantile(arr, 0.75)
    return (dkmf__fhfj, hnaaw__nzma, ozda__ucprl, swogk__svl, zep__rtamq,
        tkwmu__zpy, dwqs__jmauv, mvr__wbdbr)


def array_op_describe_dt_impl(arr):
    dkmf__fhfj = array_op_count(arr)
    swogk__svl = array_op_min(arr)
    mvr__wbdbr = array_op_max(arr)
    hnaaw__nzma = array_op_mean(arr)
    zep__rtamq = array_op_quantile(arr, 0.25)
    tkwmu__zpy = array_op_quantile(arr, 0.5)
    dwqs__jmauv = array_op_quantile(arr, 0.75)
    return (dkmf__fhfj, hnaaw__nzma, swogk__svl, zep__rtamq, tkwmu__zpy,
        dwqs__jmauv, mvr__wbdbr)


@overload(array_op_describe)
def overload_array_op_describe(arr):
    if arr.dtype == bodo.datetime64ns:
        return array_op_describe_dt_impl
    return array_op_describe_impl


@generated_jit(nopython=True)
def array_op_nbytes(arr):
    return array_op_nbytes_impl


def array_op_nbytes_impl(arr):
    return arr.nbytes


def array_op_min(arr):
    pass


@overload(array_op_min)
def overload_array_op_min(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            coy__purnf = numba.cpython.builtins.get_type_max_value(np.int64)
            mdurr__jkb = 0
            for ldl__dia in numba.parfors.parfor.internal_prange(len(arr)):
                ucuk__gtjmu = coy__purnf
                wgjdf__mnfx = 0
                if not bodo.libs.array_kernels.isna(arr, ldl__dia):
                    ucuk__gtjmu = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[ldl__dia]))
                    wgjdf__mnfx = 1
                coy__purnf = min(coy__purnf, ucuk__gtjmu)
                mdurr__jkb += wgjdf__mnfx
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(coy__purnf,
                mdurr__jkb)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            coy__purnf = numba.cpython.builtins.get_type_max_value(np.int64)
            mdurr__jkb = 0
            for ldl__dia in numba.parfors.parfor.internal_prange(len(arr)):
                ucuk__gtjmu = coy__purnf
                wgjdf__mnfx = 0
                if not bodo.libs.array_kernels.isna(arr, ldl__dia):
                    ucuk__gtjmu = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[ldl__dia]))
                    wgjdf__mnfx = 1
                coy__purnf = min(coy__purnf, ucuk__gtjmu)
                mdurr__jkb += wgjdf__mnfx
            return bodo.hiframes.pd_index_ext._dti_val_finalize(coy__purnf,
                mdurr__jkb)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            opsc__nbv = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            coy__purnf = numba.cpython.builtins.get_type_max_value(np.int64)
            mdurr__jkb = 0
            for ldl__dia in numba.parfors.parfor.internal_prange(len(opsc__nbv)
                ):
                zvejm__egqjh = opsc__nbv[ldl__dia]
                if zvejm__egqjh == -1:
                    continue
                coy__purnf = min(coy__purnf, zvejm__egqjh)
                mdurr__jkb += 1
            vjpd__arss = bodo.hiframes.series_kernels._box_cat_val(coy__purnf,
                arr.dtype, mdurr__jkb)
            return vjpd__arss
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            coy__purnf = bodo.hiframes.series_kernels._get_date_max_value()
            mdurr__jkb = 0
            for ldl__dia in numba.parfors.parfor.internal_prange(len(arr)):
                ucuk__gtjmu = coy__purnf
                wgjdf__mnfx = 0
                if not bodo.libs.array_kernels.isna(arr, ldl__dia):
                    ucuk__gtjmu = arr[ldl__dia]
                    wgjdf__mnfx = 1
                coy__purnf = min(coy__purnf, ucuk__gtjmu)
                mdurr__jkb += wgjdf__mnfx
            vjpd__arss = bodo.hiframes.series_kernels._sum_handle_nan(
                coy__purnf, mdurr__jkb)
            return vjpd__arss
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        coy__purnf = bodo.hiframes.series_kernels._get_type_max_value(arr.dtype
            )
        mdurr__jkb = 0
        for ldl__dia in numba.parfors.parfor.internal_prange(len(arr)):
            ucuk__gtjmu = coy__purnf
            wgjdf__mnfx = 0
            if not bodo.libs.array_kernels.isna(arr, ldl__dia):
                ucuk__gtjmu = arr[ldl__dia]
                wgjdf__mnfx = 1
            coy__purnf = min(coy__purnf, ucuk__gtjmu)
            mdurr__jkb += wgjdf__mnfx
        vjpd__arss = bodo.hiframes.series_kernels._sum_handle_nan(coy__purnf,
            mdurr__jkb)
        return vjpd__arss
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            coy__purnf = numba.cpython.builtins.get_type_min_value(np.int64)
            mdurr__jkb = 0
            for ldl__dia in numba.parfors.parfor.internal_prange(len(arr)):
                ucuk__gtjmu = coy__purnf
                wgjdf__mnfx = 0
                if not bodo.libs.array_kernels.isna(arr, ldl__dia):
                    ucuk__gtjmu = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[ldl__dia]))
                    wgjdf__mnfx = 1
                coy__purnf = max(coy__purnf, ucuk__gtjmu)
                mdurr__jkb += wgjdf__mnfx
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(coy__purnf,
                mdurr__jkb)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            coy__purnf = numba.cpython.builtins.get_type_min_value(np.int64)
            mdurr__jkb = 0
            for ldl__dia in numba.parfors.parfor.internal_prange(len(arr)):
                ucuk__gtjmu = coy__purnf
                wgjdf__mnfx = 0
                if not bodo.libs.array_kernels.isna(arr, ldl__dia):
                    ucuk__gtjmu = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[ldl__dia]))
                    wgjdf__mnfx = 1
                coy__purnf = max(coy__purnf, ucuk__gtjmu)
                mdurr__jkb += wgjdf__mnfx
            return bodo.hiframes.pd_index_ext._dti_val_finalize(coy__purnf,
                mdurr__jkb)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            opsc__nbv = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            coy__purnf = -1
            for ldl__dia in numba.parfors.parfor.internal_prange(len(opsc__nbv)
                ):
                coy__purnf = max(coy__purnf, opsc__nbv[ldl__dia])
            vjpd__arss = bodo.hiframes.series_kernels._box_cat_val(coy__purnf,
                arr.dtype, 1)
            return vjpd__arss
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            coy__purnf = bodo.hiframes.series_kernels._get_date_min_value()
            mdurr__jkb = 0
            for ldl__dia in numba.parfors.parfor.internal_prange(len(arr)):
                ucuk__gtjmu = coy__purnf
                wgjdf__mnfx = 0
                if not bodo.libs.array_kernels.isna(arr, ldl__dia):
                    ucuk__gtjmu = arr[ldl__dia]
                    wgjdf__mnfx = 1
                coy__purnf = max(coy__purnf, ucuk__gtjmu)
                mdurr__jkb += wgjdf__mnfx
            vjpd__arss = bodo.hiframes.series_kernels._sum_handle_nan(
                coy__purnf, mdurr__jkb)
            return vjpd__arss
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        coy__purnf = bodo.hiframes.series_kernels._get_type_min_value(arr.dtype
            )
        mdurr__jkb = 0
        for ldl__dia in numba.parfors.parfor.internal_prange(len(arr)):
            ucuk__gtjmu = coy__purnf
            wgjdf__mnfx = 0
            if not bodo.libs.array_kernels.isna(arr, ldl__dia):
                ucuk__gtjmu = arr[ldl__dia]
                wgjdf__mnfx = 1
            coy__purnf = max(coy__purnf, ucuk__gtjmu)
            mdurr__jkb += wgjdf__mnfx
        vjpd__arss = bodo.hiframes.series_kernels._sum_handle_nan(coy__purnf,
            mdurr__jkb)
        return vjpd__arss
    return impl


def array_op_mean(arr):
    pass


@overload(array_op_mean)
def overload_array_op_mean(arr):
    if arr.dtype == bodo.datetime64ns:

        def impl(arr):
            return pd.Timestamp(types.int64(bodo.libs.array_ops.
                array_op_mean(arr.view(np.int64))))
        return impl
    zxz__fpdv = types.float64
    bfhy__uzy = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        zxz__fpdv = types.float32
        bfhy__uzy = types.float32
    mxka__hkn = zxz__fpdv(0)
    bmf__jpq = bfhy__uzy(0)
    bciy__ilst = bfhy__uzy(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        coy__purnf = mxka__hkn
        mdurr__jkb = bmf__jpq
        for ldl__dia in numba.parfors.parfor.internal_prange(len(arr)):
            ucuk__gtjmu = mxka__hkn
            wgjdf__mnfx = bmf__jpq
            if not bodo.libs.array_kernels.isna(arr, ldl__dia):
                ucuk__gtjmu = arr[ldl__dia]
                wgjdf__mnfx = bciy__ilst
            coy__purnf += ucuk__gtjmu
            mdurr__jkb += wgjdf__mnfx
        vjpd__arss = bodo.hiframes.series_kernels._mean_handle_nan(coy__purnf,
            mdurr__jkb)
        return vjpd__arss
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        nob__bkbr = 0.0
        udjy__bpz = 0.0
        mdurr__jkb = 0
        for ldl__dia in numba.parfors.parfor.internal_prange(len(arr)):
            ucuk__gtjmu = 0.0
            wgjdf__mnfx = 0
            if not bodo.libs.array_kernels.isna(arr, ldl__dia) or not skipna:
                ucuk__gtjmu = arr[ldl__dia]
                wgjdf__mnfx = 1
            nob__bkbr += ucuk__gtjmu
            udjy__bpz += ucuk__gtjmu * ucuk__gtjmu
            mdurr__jkb += wgjdf__mnfx
        vjpd__arss = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            nob__bkbr, udjy__bpz, mdurr__jkb, ddof)
        return vjpd__arss
    return impl


def array_op_std(arr, skipna=True, ddof=1):
    pass


@overload(array_op_std)
def overload_array_op_std(arr, skipna=True, ddof=1):
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr, skipna=True, ddof=1):
            return pd.Timedelta(types.int64(array_op_var(arr.view(np.int64),
                skipna, ddof) ** 0.5))
        return impl_dt64
    return lambda arr, skipna=True, ddof=1: array_op_var(arr, skipna, ddof
        ) ** 0.5


def array_op_quantile(arr, q):
    pass


@overload(array_op_quantile)
def overload_array_op_quantile(arr, q):
    if is_iterable_type(q):
        if arr.dtype == bodo.datetime64ns:

            def _impl_list_dt(arr, q):
                ywnc__wssan = np.empty(len(q), np.int64)
                for ldl__dia in range(len(q)):
                    jfib__sgdcz = np.float64(q[ldl__dia])
                    ywnc__wssan[ldl__dia] = bodo.libs.array_kernels.quantile(
                        arr.view(np.int64), jfib__sgdcz)
                return ywnc__wssan.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            ywnc__wssan = np.empty(len(q), np.float64)
            for ldl__dia in range(len(q)):
                jfib__sgdcz = np.float64(q[ldl__dia])
                ywnc__wssan[ldl__dia] = bodo.libs.array_kernels.quantile(arr,
                    jfib__sgdcz)
            return ywnc__wssan
        return impl_list
    if arr.dtype == bodo.datetime64ns:

        def _impl_dt(arr, q):
            return pd.Timestamp(bodo.libs.array_kernels.quantile(arr.view(
                np.int64), np.float64(q)))
        return _impl_dt

    def impl(arr, q):
        return bodo.libs.array_kernels.quantile(arr, np.float64(q))
    return impl


def array_op_sum(arr, skipna, min_count):
    pass


@overload(array_op_sum, no_unliteral=True)
def overload_array_op_sum(arr, skipna, min_count):
    if isinstance(arr.dtype, types.Integer):
        wdu__krw = types.intp
    elif arr.dtype == types.bool_:
        wdu__krw = np.int64
    else:
        wdu__krw = arr.dtype
    stgis__jcxa = wdu__krw(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            coy__purnf = stgis__jcxa
            bpiht__hab = len(arr)
            mdurr__jkb = 0
            for ldl__dia in numba.parfors.parfor.internal_prange(bpiht__hab):
                ucuk__gtjmu = stgis__jcxa
                wgjdf__mnfx = 0
                if not bodo.libs.array_kernels.isna(arr, ldl__dia
                    ) or not skipna:
                    ucuk__gtjmu = arr[ldl__dia]
                    wgjdf__mnfx = 1
                coy__purnf += ucuk__gtjmu
                mdurr__jkb += wgjdf__mnfx
            vjpd__arss = bodo.hiframes.series_kernels._var_handle_mincount(
                coy__purnf, mdurr__jkb, min_count)
            return vjpd__arss
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            coy__purnf = stgis__jcxa
            bpiht__hab = len(arr)
            for ldl__dia in numba.parfors.parfor.internal_prange(bpiht__hab):
                ucuk__gtjmu = stgis__jcxa
                if not bodo.libs.array_kernels.isna(arr, ldl__dia):
                    ucuk__gtjmu = arr[ldl__dia]
                coy__purnf += ucuk__gtjmu
            return coy__purnf
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    cos__eeqf = arr.dtype(1)
    if arr.dtype == types.bool_:
        cos__eeqf = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            coy__purnf = cos__eeqf
            mdurr__jkb = 0
            for ldl__dia in numba.parfors.parfor.internal_prange(len(arr)):
                ucuk__gtjmu = cos__eeqf
                wgjdf__mnfx = 0
                if not bodo.libs.array_kernels.isna(arr, ldl__dia
                    ) or not skipna:
                    ucuk__gtjmu = arr[ldl__dia]
                    wgjdf__mnfx = 1
                mdurr__jkb += wgjdf__mnfx
                coy__purnf *= ucuk__gtjmu
            vjpd__arss = bodo.hiframes.series_kernels._var_handle_mincount(
                coy__purnf, mdurr__jkb, min_count)
            return vjpd__arss
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            coy__purnf = cos__eeqf
            for ldl__dia in numba.parfors.parfor.internal_prange(len(arr)):
                ucuk__gtjmu = cos__eeqf
                if not bodo.libs.array_kernels.isna(arr, ldl__dia):
                    ucuk__gtjmu = arr[ldl__dia]
                coy__purnf *= ucuk__gtjmu
            return coy__purnf
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        ldl__dia = bodo.libs.array_kernels._nan_argmax(arr)
        return index[ldl__dia]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        ldl__dia = bodo.libs.array_kernels._nan_argmin(arr)
        return index[ldl__dia]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            zlyct__ntzwx = {}
            for ctqi__dbdef in values:
                zlyct__ntzwx[bodo.utils.conversion.box_if_dt64(ctqi__dbdef)
                    ] = 0
            return zlyct__ntzwx
        return impl
    else:

        def impl(values, use_hash_impl):
            return values
        return impl


def array_op_isin(arr, values):
    pass


@overload(array_op_isin, inline='always')
def overload_array_op_isin(arr, values):
    use_hash_impl = element_type(values) == element_type(arr
        ) and is_hashable_type(element_type(values))

    def impl(arr, values):
        values = bodo.libs.array_ops._convert_isin_values(values, use_hash_impl
            )
        numba.parfors.parfor.init_prange()
        bpiht__hab = len(arr)
        ywnc__wssan = np.empty(bpiht__hab, np.bool_)
        for ldl__dia in numba.parfors.parfor.internal_prange(bpiht__hab):
            ywnc__wssan[ldl__dia] = bodo.utils.conversion.box_if_dt64(arr[
                ldl__dia]) in values
        return ywnc__wssan
    return impl


@generated_jit(nopython=True)
def array_unique_vector_map(in_arr_tup):
    yacyy__wndu = len(in_arr_tup) != 1
    pfpi__vlb = list(in_arr_tup.types)
    rjins__rxn = 'def impl(in_arr_tup):\n'
    rjins__rxn += (
        "  ev = tracing.Event('array_unique_vector_map', is_parallel=False)\n")
    rjins__rxn += '  n = len(in_arr_tup[0])\n'
    if yacyy__wndu:
        nza__stf = ', '.join([f'in_arr_tup[{ldl__dia}][unused]' for
            ldl__dia in range(len(in_arr_tup))])
        bypw__ttcfg = ', '.join(['False' for csht__ksjc in range(len(
            in_arr_tup))])
        rjins__rxn += f"""  arr_map = {{bodo.libs.nullable_tuple_ext.build_nullable_tuple(({nza__stf},), ({bypw__ttcfg},)): 0 for unused in range(0)}}
"""
        rjins__rxn += '  map_vector = np.empty(n, np.int64)\n'
        for ldl__dia, ltwnh__tyds in enumerate(pfpi__vlb):
            rjins__rxn += f'  in_lst_{ldl__dia} = []\n'
            if is_str_arr_type(ltwnh__tyds):
                rjins__rxn += f'  total_len_{ldl__dia} = 0\n'
            rjins__rxn += f'  null_in_lst_{ldl__dia} = []\n'
        rjins__rxn += '  for i in range(n):\n'
        cffjy__adi = ', '.join([f'in_arr_tup[{ldl__dia}][i]' for ldl__dia in
            range(len(pfpi__vlb))])
        xunp__comn = ', '.join([
            f'bodo.libs.array_kernels.isna(in_arr_tup[{ldl__dia}], i)' for
            ldl__dia in range(len(pfpi__vlb))])
        rjins__rxn += f"""    data_val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({cffjy__adi},), ({xunp__comn},))
"""
        rjins__rxn += '    if data_val not in arr_map:\n'
        rjins__rxn += '      set_val = len(arr_map)\n'
        rjins__rxn += '      values_tup = data_val._data\n'
        rjins__rxn += '      nulls_tup = data_val._null_values\n'
        for ldl__dia, ltwnh__tyds in enumerate(pfpi__vlb):
            rjins__rxn += (
                f'      in_lst_{ldl__dia}.append(values_tup[{ldl__dia}])\n')
            rjins__rxn += (
                f'      null_in_lst_{ldl__dia}.append(nulls_tup[{ldl__dia}])\n'
                )
            if is_str_arr_type(ltwnh__tyds):
                rjins__rxn += f"""      total_len_{ldl__dia}  += nulls_tup[{ldl__dia}] * bodo.libs.str_arr_ext.get_str_arr_item_length(in_arr_tup[{ldl__dia}], i)
"""
        rjins__rxn += '      arr_map[data_val] = len(arr_map)\n'
        rjins__rxn += '    else:\n'
        rjins__rxn += '      set_val = arr_map[data_val]\n'
        rjins__rxn += '    map_vector[i] = set_val\n'
        rjins__rxn += '  n_rows = len(arr_map)\n'
        for ldl__dia, ltwnh__tyds in enumerate(pfpi__vlb):
            if is_str_arr_type(ltwnh__tyds):
                rjins__rxn += f"""  out_arr_{ldl__dia} = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len_{ldl__dia})
"""
            else:
                rjins__rxn += f"""  out_arr_{ldl__dia} = bodo.utils.utils.alloc_type(n_rows, in_arr_tup[{ldl__dia}], (-1,))
"""
        rjins__rxn += '  for j in range(len(arr_map)):\n'
        for ldl__dia in range(len(pfpi__vlb)):
            rjins__rxn += f'    if null_in_lst_{ldl__dia}[j]:\n'
            rjins__rxn += (
                f'      bodo.libs.array_kernels.setna(out_arr_{ldl__dia}, j)\n'
                )
            rjins__rxn += '    else:\n'
            rjins__rxn += (
                f'      out_arr_{ldl__dia}[j] = in_lst_{ldl__dia}[j]\n')
        bjjlj__jmcld = ', '.join([f'out_arr_{ldl__dia}' for ldl__dia in
            range(len(pfpi__vlb))])
        rjins__rxn += "  ev.add_attribute('n_map_entries', n_rows)\n"
        rjins__rxn += '  ev.finalize()\n'
        rjins__rxn += f'  return ({bjjlj__jmcld},), map_vector\n'
    else:
        rjins__rxn += '  in_arr = in_arr_tup[0]\n'
        rjins__rxn += (
            f'  arr_map = {{in_arr[unused]: 0 for unused in range(0)}}\n')
        rjins__rxn += '  map_vector = np.empty(n, np.int64)\n'
        rjins__rxn += '  is_na = 0\n'
        rjins__rxn += '  in_lst = []\n'
        rjins__rxn += '  na_idxs = []\n'
        if is_str_arr_type(pfpi__vlb[0]):
            rjins__rxn += '  total_len = 0\n'
        rjins__rxn += '  for i in range(n):\n'
        rjins__rxn += '    if bodo.libs.array_kernels.isna(in_arr, i):\n'
        rjins__rxn += '      is_na = 1\n'
        rjins__rxn += '      # Always put NA in the last location.\n'
        rjins__rxn += '      # We use -1 as a placeholder\n'
        rjins__rxn += '      set_val = -1\n'
        rjins__rxn += '      na_idxs.append(i)\n'
        rjins__rxn += '    else:\n'
        rjins__rxn += '      data_val = in_arr[i]\n'
        rjins__rxn += '      if data_val not in arr_map:\n'
        rjins__rxn += '        set_val = len(arr_map)\n'
        rjins__rxn += '        in_lst.append(data_val)\n'
        if is_str_arr_type(pfpi__vlb[0]):
            rjins__rxn += """        total_len += bodo.libs.str_arr_ext.get_str_arr_item_length(in_arr, i)
"""
        rjins__rxn += '        arr_map[data_val] = len(arr_map)\n'
        rjins__rxn += '      else:\n'
        rjins__rxn += '        set_val = arr_map[data_val]\n'
        rjins__rxn += '    map_vector[i] = set_val\n'
        rjins__rxn += '  map_vector[na_idxs] = len(arr_map)\n'
        rjins__rxn += '  n_rows = len(arr_map) + is_na\n'
        if is_str_arr_type(pfpi__vlb[0]):
            rjins__rxn += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len)
"""
        else:
            rjins__rxn += (
                '  out_arr = bodo.utils.utils.alloc_type(n_rows, in_arr, (-1,))\n'
                )
        rjins__rxn += '  for j in range(len(arr_map)):\n'
        rjins__rxn += '    out_arr[j] = in_lst[j]\n'
        rjins__rxn += '  if is_na:\n'
        rjins__rxn += (
            '    bodo.libs.array_kernels.setna(out_arr, n_rows - 1)\n')
        rjins__rxn += "  ev.add_attribute('n_map_entries', n_rows)\n"
        rjins__rxn += '  ev.finalize()\n'
        rjins__rxn += f'  return (out_arr,), map_vector\n'
    nmcci__vqmbu = {}
    exec(rjins__rxn, {'bodo': bodo, 'np': np, 'tracing': tracing}, nmcci__vqmbu
        )
    impl = nmcci__vqmbu['impl']
    return impl
