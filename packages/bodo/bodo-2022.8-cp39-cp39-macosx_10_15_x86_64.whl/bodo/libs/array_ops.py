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
        bon__lolox = 0
    elif isinstance(A, bodo.libs.bool_arr_ext.BooleanArrayType) or isinstance(A
        , types.Array) and A.dtype == types.bool_:
        bon__lolox = False
    elif A == bodo.string_array_type:
        bon__lolox = ''
    elif A == bodo.binary_array_type:
        bon__lolox = b''
    else:
        raise bodo.utils.typing.BodoError(
            f'Cannot perform any with this array type: {A}')

    def impl(A, skipna=True):
        numba.parfors.parfor.init_prange()
        asg__rnvoq = 0
        for zbtbe__bagb in numba.parfors.parfor.internal_prange(len(A)):
            if not bodo.libs.array_kernels.isna(A, zbtbe__bagb):
                if A[zbtbe__bagb] != bon__lolox:
                    asg__rnvoq += 1
        return asg__rnvoq != 0
    return impl


def array_op_all(arr, skipna=True):
    pass


@overload(array_op_all)
def overload_array_op_all(A, skipna=True):
    if isinstance(A, types.Array) and isinstance(A.dtype, types.Integer
        ) or isinstance(A, bodo.libs.int_arr_ext.IntegerArrayType):
        bon__lolox = 0
    elif isinstance(A, bodo.libs.bool_arr_ext.BooleanArrayType) or isinstance(A
        , types.Array) and A.dtype == types.bool_:
        bon__lolox = False
    elif A == bodo.string_array_type:
        bon__lolox = ''
    elif A == bodo.binary_array_type:
        bon__lolox = b''
    else:
        raise bodo.utils.typing.BodoError(
            f'Cannot perform all with this array type: {A}')

    def impl(A, skipna=True):
        numba.parfors.parfor.init_prange()
        asg__rnvoq = 0
        for zbtbe__bagb in numba.parfors.parfor.internal_prange(len(A)):
            if not bodo.libs.array_kernels.isna(A, zbtbe__bagb):
                if A[zbtbe__bagb] == bon__lolox:
                    asg__rnvoq += 1
        return asg__rnvoq == 0
    return impl


@numba.njit
def array_op_median(arr, skipna=True, parallel=False):
    igi__aofn = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(igi__aofn.ctypes, arr,
        parallel, skipna)
    return igi__aofn[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        qidj__lyga = len(arr)
        ljlt__pkp = np.empty(qidj__lyga, np.bool_)
        for zbtbe__bagb in numba.parfors.parfor.internal_prange(qidj__lyga):
            ljlt__pkp[zbtbe__bagb] = bodo.libs.array_kernels.isna(arr,
                zbtbe__bagb)
        return ljlt__pkp
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        asg__rnvoq = 0
        for zbtbe__bagb in numba.parfors.parfor.internal_prange(len(arr)):
            xdu__axd = 0
            if not bodo.libs.array_kernels.isna(arr, zbtbe__bagb):
                xdu__axd = 1
            asg__rnvoq += xdu__axd
        igi__aofn = asg__rnvoq
        return igi__aofn
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    oqk__ovas = array_op_count(arr)
    yzxs__xpnan = array_op_min(arr)
    ykblh__lfexd = array_op_max(arr)
    uxrks__mctv = array_op_mean(arr)
    wwxr__sgna = array_op_std(arr)
    ivee__zgvzu = array_op_quantile(arr, 0.25)
    jrmkr__havv = array_op_quantile(arr, 0.5)
    rsoie__yvc = array_op_quantile(arr, 0.75)
    return (oqk__ovas, uxrks__mctv, wwxr__sgna, yzxs__xpnan, ivee__zgvzu,
        jrmkr__havv, rsoie__yvc, ykblh__lfexd)


def array_op_describe_dt_impl(arr):
    oqk__ovas = array_op_count(arr)
    yzxs__xpnan = array_op_min(arr)
    ykblh__lfexd = array_op_max(arr)
    uxrks__mctv = array_op_mean(arr)
    ivee__zgvzu = array_op_quantile(arr, 0.25)
    jrmkr__havv = array_op_quantile(arr, 0.5)
    rsoie__yvc = array_op_quantile(arr, 0.75)
    return (oqk__ovas, uxrks__mctv, yzxs__xpnan, ivee__zgvzu, jrmkr__havv,
        rsoie__yvc, ykblh__lfexd)


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
            sww__dvyzj = numba.cpython.builtins.get_type_max_value(np.int64)
            asg__rnvoq = 0
            for zbtbe__bagb in numba.parfors.parfor.internal_prange(len(arr)):
                upgb__lzg = sww__dvyzj
                xdu__axd = 0
                if not bodo.libs.array_kernels.isna(arr, zbtbe__bagb):
                    upgb__lzg = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[zbtbe__bagb]))
                    xdu__axd = 1
                sww__dvyzj = min(sww__dvyzj, upgb__lzg)
                asg__rnvoq += xdu__axd
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(sww__dvyzj,
                asg__rnvoq)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            sww__dvyzj = numba.cpython.builtins.get_type_max_value(np.int64)
            asg__rnvoq = 0
            for zbtbe__bagb in numba.parfors.parfor.internal_prange(len(arr)):
                upgb__lzg = sww__dvyzj
                xdu__axd = 0
                if not bodo.libs.array_kernels.isna(arr, zbtbe__bagb):
                    upgb__lzg = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        arr[zbtbe__bagb])
                    xdu__axd = 1
                sww__dvyzj = min(sww__dvyzj, upgb__lzg)
                asg__rnvoq += xdu__axd
            return bodo.hiframes.pd_index_ext._dti_val_finalize(sww__dvyzj,
                asg__rnvoq)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            lbuls__urwnk = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            sww__dvyzj = numba.cpython.builtins.get_type_max_value(np.int64)
            asg__rnvoq = 0
            for zbtbe__bagb in numba.parfors.parfor.internal_prange(len(
                lbuls__urwnk)):
                tows__lapy = lbuls__urwnk[zbtbe__bagb]
                if tows__lapy == -1:
                    continue
                sww__dvyzj = min(sww__dvyzj, tows__lapy)
                asg__rnvoq += 1
            igi__aofn = bodo.hiframes.series_kernels._box_cat_val(sww__dvyzj,
                arr.dtype, asg__rnvoq)
            return igi__aofn
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            sww__dvyzj = bodo.hiframes.series_kernels._get_date_max_value()
            asg__rnvoq = 0
            for zbtbe__bagb in numba.parfors.parfor.internal_prange(len(arr)):
                upgb__lzg = sww__dvyzj
                xdu__axd = 0
                if not bodo.libs.array_kernels.isna(arr, zbtbe__bagb):
                    upgb__lzg = arr[zbtbe__bagb]
                    xdu__axd = 1
                sww__dvyzj = min(sww__dvyzj, upgb__lzg)
                asg__rnvoq += xdu__axd
            igi__aofn = bodo.hiframes.series_kernels._sum_handle_nan(sww__dvyzj
                , asg__rnvoq)
            return igi__aofn
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        sww__dvyzj = bodo.hiframes.series_kernels._get_type_max_value(arr.dtype
            )
        asg__rnvoq = 0
        for zbtbe__bagb in numba.parfors.parfor.internal_prange(len(arr)):
            upgb__lzg = sww__dvyzj
            xdu__axd = 0
            if not bodo.libs.array_kernels.isna(arr, zbtbe__bagb):
                upgb__lzg = arr[zbtbe__bagb]
                xdu__axd = 1
            sww__dvyzj = min(sww__dvyzj, upgb__lzg)
            asg__rnvoq += xdu__axd
        igi__aofn = bodo.hiframes.series_kernels._sum_handle_nan(sww__dvyzj,
            asg__rnvoq)
        return igi__aofn
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            sww__dvyzj = numba.cpython.builtins.get_type_min_value(np.int64)
            asg__rnvoq = 0
            for zbtbe__bagb in numba.parfors.parfor.internal_prange(len(arr)):
                upgb__lzg = sww__dvyzj
                xdu__axd = 0
                if not bodo.libs.array_kernels.isna(arr, zbtbe__bagb):
                    upgb__lzg = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[zbtbe__bagb]))
                    xdu__axd = 1
                sww__dvyzj = max(sww__dvyzj, upgb__lzg)
                asg__rnvoq += xdu__axd
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(sww__dvyzj,
                asg__rnvoq)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            sww__dvyzj = numba.cpython.builtins.get_type_min_value(np.int64)
            asg__rnvoq = 0
            for zbtbe__bagb in numba.parfors.parfor.internal_prange(len(arr)):
                upgb__lzg = sww__dvyzj
                xdu__axd = 0
                if not bodo.libs.array_kernels.isna(arr, zbtbe__bagb):
                    upgb__lzg = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        arr[zbtbe__bagb])
                    xdu__axd = 1
                sww__dvyzj = max(sww__dvyzj, upgb__lzg)
                asg__rnvoq += xdu__axd
            return bodo.hiframes.pd_index_ext._dti_val_finalize(sww__dvyzj,
                asg__rnvoq)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            lbuls__urwnk = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            sww__dvyzj = -1
            for zbtbe__bagb in numba.parfors.parfor.internal_prange(len(
                lbuls__urwnk)):
                sww__dvyzj = max(sww__dvyzj, lbuls__urwnk[zbtbe__bagb])
            igi__aofn = bodo.hiframes.series_kernels._box_cat_val(sww__dvyzj,
                arr.dtype, 1)
            return igi__aofn
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            sww__dvyzj = bodo.hiframes.series_kernels._get_date_min_value()
            asg__rnvoq = 0
            for zbtbe__bagb in numba.parfors.parfor.internal_prange(len(arr)):
                upgb__lzg = sww__dvyzj
                xdu__axd = 0
                if not bodo.libs.array_kernels.isna(arr, zbtbe__bagb):
                    upgb__lzg = arr[zbtbe__bagb]
                    xdu__axd = 1
                sww__dvyzj = max(sww__dvyzj, upgb__lzg)
                asg__rnvoq += xdu__axd
            igi__aofn = bodo.hiframes.series_kernels._sum_handle_nan(sww__dvyzj
                , asg__rnvoq)
            return igi__aofn
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        sww__dvyzj = bodo.hiframes.series_kernels._get_type_min_value(arr.dtype
            )
        asg__rnvoq = 0
        for zbtbe__bagb in numba.parfors.parfor.internal_prange(len(arr)):
            upgb__lzg = sww__dvyzj
            xdu__axd = 0
            if not bodo.libs.array_kernels.isna(arr, zbtbe__bagb):
                upgb__lzg = arr[zbtbe__bagb]
                xdu__axd = 1
            sww__dvyzj = max(sww__dvyzj, upgb__lzg)
            asg__rnvoq += xdu__axd
        igi__aofn = bodo.hiframes.series_kernels._sum_handle_nan(sww__dvyzj,
            asg__rnvoq)
        return igi__aofn
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
    bwoi__pijd = types.float64
    arsaf__xvvh = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        bwoi__pijd = types.float32
        arsaf__xvvh = types.float32
    jjv__jqvfy = bwoi__pijd(0)
    wqjvj__qgrre = arsaf__xvvh(0)
    fbko__tpesu = arsaf__xvvh(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        sww__dvyzj = jjv__jqvfy
        asg__rnvoq = wqjvj__qgrre
        for zbtbe__bagb in numba.parfors.parfor.internal_prange(len(arr)):
            upgb__lzg = jjv__jqvfy
            xdu__axd = wqjvj__qgrre
            if not bodo.libs.array_kernels.isna(arr, zbtbe__bagb):
                upgb__lzg = arr[zbtbe__bagb]
                xdu__axd = fbko__tpesu
            sww__dvyzj += upgb__lzg
            asg__rnvoq += xdu__axd
        igi__aofn = bodo.hiframes.series_kernels._mean_handle_nan(sww__dvyzj,
            asg__rnvoq)
        return igi__aofn
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        gauf__bxxga = 0.0
        tlh__ttzdo = 0.0
        asg__rnvoq = 0
        for zbtbe__bagb in numba.parfors.parfor.internal_prange(len(arr)):
            upgb__lzg = 0.0
            xdu__axd = 0
            if not bodo.libs.array_kernels.isna(arr, zbtbe__bagb
                ) or not skipna:
                upgb__lzg = arr[zbtbe__bagb]
                xdu__axd = 1
            gauf__bxxga += upgb__lzg
            tlh__ttzdo += upgb__lzg * upgb__lzg
            asg__rnvoq += xdu__axd
        igi__aofn = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            gauf__bxxga, tlh__ttzdo, asg__rnvoq, ddof)
        return igi__aofn
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
                ljlt__pkp = np.empty(len(q), np.int64)
                for zbtbe__bagb in range(len(q)):
                    rqk__faa = np.float64(q[zbtbe__bagb])
                    ljlt__pkp[zbtbe__bagb] = bodo.libs.array_kernels.quantile(
                        arr.view(np.int64), rqk__faa)
                return ljlt__pkp.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            ljlt__pkp = np.empty(len(q), np.float64)
            for zbtbe__bagb in range(len(q)):
                rqk__faa = np.float64(q[zbtbe__bagb])
                ljlt__pkp[zbtbe__bagb] = bodo.libs.array_kernels.quantile(arr,
                    rqk__faa)
            return ljlt__pkp
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
        bhwbz__ljq = types.intp
    elif arr.dtype == types.bool_:
        bhwbz__ljq = np.int64
    else:
        bhwbz__ljq = arr.dtype
    mjoz__gdcll = bhwbz__ljq(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            sww__dvyzj = mjoz__gdcll
            qidj__lyga = len(arr)
            asg__rnvoq = 0
            for zbtbe__bagb in numba.parfors.parfor.internal_prange(qidj__lyga
                ):
                upgb__lzg = mjoz__gdcll
                xdu__axd = 0
                if not bodo.libs.array_kernels.isna(arr, zbtbe__bagb
                    ) or not skipna:
                    upgb__lzg = arr[zbtbe__bagb]
                    xdu__axd = 1
                sww__dvyzj += upgb__lzg
                asg__rnvoq += xdu__axd
            igi__aofn = bodo.hiframes.series_kernels._var_handle_mincount(
                sww__dvyzj, asg__rnvoq, min_count)
            return igi__aofn
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            sww__dvyzj = mjoz__gdcll
            qidj__lyga = len(arr)
            for zbtbe__bagb in numba.parfors.parfor.internal_prange(qidj__lyga
                ):
                upgb__lzg = mjoz__gdcll
                if not bodo.libs.array_kernels.isna(arr, zbtbe__bagb):
                    upgb__lzg = arr[zbtbe__bagb]
                sww__dvyzj += upgb__lzg
            return sww__dvyzj
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    msf__uzjui = arr.dtype(1)
    if arr.dtype == types.bool_:
        msf__uzjui = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            sww__dvyzj = msf__uzjui
            asg__rnvoq = 0
            for zbtbe__bagb in numba.parfors.parfor.internal_prange(len(arr)):
                upgb__lzg = msf__uzjui
                xdu__axd = 0
                if not bodo.libs.array_kernels.isna(arr, zbtbe__bagb
                    ) or not skipna:
                    upgb__lzg = arr[zbtbe__bagb]
                    xdu__axd = 1
                asg__rnvoq += xdu__axd
                sww__dvyzj *= upgb__lzg
            igi__aofn = bodo.hiframes.series_kernels._var_handle_mincount(
                sww__dvyzj, asg__rnvoq, min_count)
            return igi__aofn
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            sww__dvyzj = msf__uzjui
            for zbtbe__bagb in numba.parfors.parfor.internal_prange(len(arr)):
                upgb__lzg = msf__uzjui
                if not bodo.libs.array_kernels.isna(arr, zbtbe__bagb):
                    upgb__lzg = arr[zbtbe__bagb]
                sww__dvyzj *= upgb__lzg
            return sww__dvyzj
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        zbtbe__bagb = bodo.libs.array_kernels._nan_argmax(arr)
        return index[zbtbe__bagb]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        zbtbe__bagb = bodo.libs.array_kernels._nan_argmin(arr)
        return index[zbtbe__bagb]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            uvmjw__tpbci = {}
            for wzk__bub in values:
                uvmjw__tpbci[bodo.utils.conversion.box_if_dt64(wzk__bub)] = 0
            return uvmjw__tpbci
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
        qidj__lyga = len(arr)
        ljlt__pkp = np.empty(qidj__lyga, np.bool_)
        for zbtbe__bagb in numba.parfors.parfor.internal_prange(qidj__lyga):
            ljlt__pkp[zbtbe__bagb] = bodo.utils.conversion.box_if_dt64(arr[
                zbtbe__bagb]) in values
        return ljlt__pkp
    return impl


@generated_jit(nopython=True)
def array_unique_vector_map(in_arr_tup):
    jjqa__stqto = len(in_arr_tup) != 1
    ceumr__rwqyj = list(in_arr_tup.types)
    hmhsc__ntyzp = 'def impl(in_arr_tup):\n'
    hmhsc__ntyzp += (
        "  ev = tracing.Event('array_unique_vector_map', is_parallel=False)\n")
    hmhsc__ntyzp += '  n = len(in_arr_tup[0])\n'
    if jjqa__stqto:
        xbba__tastd = ', '.join([f'in_arr_tup[{zbtbe__bagb}][unused]' for
            zbtbe__bagb in range(len(in_arr_tup))])
        ffdb__ept = ', '.join(['False' for lqk__yzx in range(len(in_arr_tup))])
        hmhsc__ntyzp += f"""  arr_map = {{bodo.libs.nullable_tuple_ext.build_nullable_tuple(({xbba__tastd},), ({ffdb__ept},)): 0 for unused in range(0)}}
"""
        hmhsc__ntyzp += '  map_vector = np.empty(n, np.int64)\n'
        for zbtbe__bagb, xecio__nxc in enumerate(ceumr__rwqyj):
            hmhsc__ntyzp += f'  in_lst_{zbtbe__bagb} = []\n'
            if is_str_arr_type(xecio__nxc):
                hmhsc__ntyzp += f'  total_len_{zbtbe__bagb} = 0\n'
            hmhsc__ntyzp += f'  null_in_lst_{zbtbe__bagb} = []\n'
        hmhsc__ntyzp += '  for i in range(n):\n'
        fghxz__vbrx = ', '.join([f'in_arr_tup[{zbtbe__bagb}][i]' for
            zbtbe__bagb in range(len(ceumr__rwqyj))])
        rjt__aeib = ', '.join([
            f'bodo.libs.array_kernels.isna(in_arr_tup[{zbtbe__bagb}], i)' for
            zbtbe__bagb in range(len(ceumr__rwqyj))])
        hmhsc__ntyzp += f"""    data_val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({fghxz__vbrx},), ({rjt__aeib},))
"""
        hmhsc__ntyzp += '    if data_val not in arr_map:\n'
        hmhsc__ntyzp += '      set_val = len(arr_map)\n'
        hmhsc__ntyzp += '      values_tup = data_val._data\n'
        hmhsc__ntyzp += '      nulls_tup = data_val._null_values\n'
        for zbtbe__bagb, xecio__nxc in enumerate(ceumr__rwqyj):
            hmhsc__ntyzp += (
                f'      in_lst_{zbtbe__bagb}.append(values_tup[{zbtbe__bagb}])\n'
                )
            hmhsc__ntyzp += (
                f'      null_in_lst_{zbtbe__bagb}.append(nulls_tup[{zbtbe__bagb}])\n'
                )
            if is_str_arr_type(xecio__nxc):
                hmhsc__ntyzp += f"""      total_len_{zbtbe__bagb}  += nulls_tup[{zbtbe__bagb}] * bodo.libs.str_arr_ext.get_str_arr_item_length(in_arr_tup[{zbtbe__bagb}], i)
"""
        hmhsc__ntyzp += '      arr_map[data_val] = len(arr_map)\n'
        hmhsc__ntyzp += '    else:\n'
        hmhsc__ntyzp += '      set_val = arr_map[data_val]\n'
        hmhsc__ntyzp += '    map_vector[i] = set_val\n'
        hmhsc__ntyzp += '  n_rows = len(arr_map)\n'
        for zbtbe__bagb, xecio__nxc in enumerate(ceumr__rwqyj):
            if is_str_arr_type(xecio__nxc):
                hmhsc__ntyzp += f"""  out_arr_{zbtbe__bagb} = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len_{zbtbe__bagb})
"""
            else:
                hmhsc__ntyzp += f"""  out_arr_{zbtbe__bagb} = bodo.utils.utils.alloc_type(n_rows, in_arr_tup[{zbtbe__bagb}], (-1,))
"""
        hmhsc__ntyzp += '  for j in range(len(arr_map)):\n'
        for zbtbe__bagb in range(len(ceumr__rwqyj)):
            hmhsc__ntyzp += f'    if null_in_lst_{zbtbe__bagb}[j]:\n'
            hmhsc__ntyzp += (
                f'      bodo.libs.array_kernels.setna(out_arr_{zbtbe__bagb}, j)\n'
                )
            hmhsc__ntyzp += '    else:\n'
            hmhsc__ntyzp += (
                f'      out_arr_{zbtbe__bagb}[j] = in_lst_{zbtbe__bagb}[j]\n')
        txjp__xsbn = ', '.join([f'out_arr_{zbtbe__bagb}' for zbtbe__bagb in
            range(len(ceumr__rwqyj))])
        hmhsc__ntyzp += "  ev.add_attribute('n_map_entries', n_rows)\n"
        hmhsc__ntyzp += '  ev.finalize()\n'
        hmhsc__ntyzp += f'  return ({txjp__xsbn},), map_vector\n'
    else:
        hmhsc__ntyzp += '  in_arr = in_arr_tup[0]\n'
        hmhsc__ntyzp += (
            f'  arr_map = {{in_arr[unused]: 0 for unused in range(0)}}\n')
        hmhsc__ntyzp += '  map_vector = np.empty(n, np.int64)\n'
        hmhsc__ntyzp += '  is_na = 0\n'
        hmhsc__ntyzp += '  in_lst = []\n'
        hmhsc__ntyzp += '  na_idxs = []\n'
        if is_str_arr_type(ceumr__rwqyj[0]):
            hmhsc__ntyzp += '  total_len = 0\n'
        hmhsc__ntyzp += '  for i in range(n):\n'
        hmhsc__ntyzp += '    if bodo.libs.array_kernels.isna(in_arr, i):\n'
        hmhsc__ntyzp += '      is_na = 1\n'
        hmhsc__ntyzp += '      # Always put NA in the last location.\n'
        hmhsc__ntyzp += '      # We use -1 as a placeholder\n'
        hmhsc__ntyzp += '      set_val = -1\n'
        hmhsc__ntyzp += '      na_idxs.append(i)\n'
        hmhsc__ntyzp += '    else:\n'
        hmhsc__ntyzp += '      data_val = in_arr[i]\n'
        hmhsc__ntyzp += '      if data_val not in arr_map:\n'
        hmhsc__ntyzp += '        set_val = len(arr_map)\n'
        hmhsc__ntyzp += '        in_lst.append(data_val)\n'
        if is_str_arr_type(ceumr__rwqyj[0]):
            hmhsc__ntyzp += """        total_len += bodo.libs.str_arr_ext.get_str_arr_item_length(in_arr, i)
"""
        hmhsc__ntyzp += '        arr_map[data_val] = len(arr_map)\n'
        hmhsc__ntyzp += '      else:\n'
        hmhsc__ntyzp += '        set_val = arr_map[data_val]\n'
        hmhsc__ntyzp += '    map_vector[i] = set_val\n'
        hmhsc__ntyzp += '  map_vector[na_idxs] = len(arr_map)\n'
        hmhsc__ntyzp += '  n_rows = len(arr_map) + is_na\n'
        if is_str_arr_type(ceumr__rwqyj[0]):
            hmhsc__ntyzp += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len)
"""
        else:
            hmhsc__ntyzp += (
                '  out_arr = bodo.utils.utils.alloc_type(n_rows, in_arr, (-1,))\n'
                )
        hmhsc__ntyzp += '  for j in range(len(arr_map)):\n'
        hmhsc__ntyzp += '    out_arr[j] = in_lst[j]\n'
        hmhsc__ntyzp += '  if is_na:\n'
        hmhsc__ntyzp += (
            '    bodo.libs.array_kernels.setna(out_arr, n_rows - 1)\n')
        hmhsc__ntyzp += "  ev.add_attribute('n_map_entries', n_rows)\n"
        hmhsc__ntyzp += '  ev.finalize()\n'
        hmhsc__ntyzp += f'  return (out_arr,), map_vector\n'
    kzaj__rycqf = {}
    exec(hmhsc__ntyzp, {'bodo': bodo, 'np': np, 'tracing': tracing},
        kzaj__rycqf)
    impl = kzaj__rycqf['impl']
    return impl
