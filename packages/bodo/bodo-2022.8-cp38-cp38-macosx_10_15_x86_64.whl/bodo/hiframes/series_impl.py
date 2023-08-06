"""
Implementation of Series attributes and methods using overload.
"""
import operator
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_builtin, overload, overload_attribute, overload_method, register_jitable
import bodo
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.hiframes.datetime_timedelta_ext import PDTimeDeltaType, datetime_timedelta_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.pd_offsets_ext import is_offsets_type
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType, if_series_to_array_type, is_series_type
from bodo.hiframes.pd_timestamp_ext import PandasTimestampType, pd_timestamp_type
from bodo.hiframes.rolling import is_supported_shift_array_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import BinaryArrayType, binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType
from bodo.libs.str_ext import string_type
from bodo.utils.transform import is_var_size_item_array_type
from bodo.utils.typing import BodoError, ColNamesMetaType, can_replace, check_unsupported_args, dtype_to_array_type, element_type, get_common_scalar_dtype, get_index_names, get_literal_value, get_overload_const_bytes, get_overload_const_int, get_overload_const_str, is_common_scalar_dtype, is_iterable_type, is_literal_type, is_nullable_type, is_overload_bool, is_overload_constant_bool, is_overload_constant_bytes, is_overload_constant_int, is_overload_constant_nan, is_overload_constant_str, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_overload_zero, is_scalar_type, is_str_arr_type, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array


@overload_attribute(HeterogeneousSeriesType, 'index', inline='always')
@overload_attribute(SeriesType, 'index', inline='always')
def overload_series_index(s):
    return lambda s: bodo.hiframes.pd_series_ext.get_series_index(s)


@overload_attribute(HeterogeneousSeriesType, 'values', inline='always')
@overload_attribute(SeriesType, 'values', inline='always')
def overload_series_values(s):
    if isinstance(s.data, bodo.DatetimeArrayType):

        def impl(s):
            dtgcp__ctr = bodo.hiframes.pd_series_ext.get_series_data(s)
            rpry__bgfxv = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                dtgcp__ctr)
            return rpry__bgfxv
        return impl
    return lambda s: bodo.hiframes.pd_series_ext.get_series_data(s)


@overload_attribute(SeriesType, 'dtype', inline='always')
def overload_series_dtype(s):
    if s.dtype == bodo.string_type:
        raise BodoError('Series.dtype not supported for string Series yet')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(s, 'Series.dtype'
        )
    return lambda s: bodo.hiframes.pd_series_ext.get_series_data(s).dtype


@overload_attribute(HeterogeneousSeriesType, 'shape')
@overload_attribute(SeriesType, 'shape')
def overload_series_shape(s):
    return lambda s: (len(bodo.hiframes.pd_series_ext.get_series_data(s)),)


@overload_attribute(HeterogeneousSeriesType, 'ndim', inline='always')
@overload_attribute(SeriesType, 'ndim', inline='always')
def overload_series_ndim(s):
    return lambda s: 1


@overload_attribute(HeterogeneousSeriesType, 'size')
@overload_attribute(SeriesType, 'size')
def overload_series_size(s):
    return lambda s: len(bodo.hiframes.pd_series_ext.get_series_data(s))


@overload_attribute(HeterogeneousSeriesType, 'T', inline='always')
@overload_attribute(SeriesType, 'T', inline='always')
def overload_series_T(s):
    return lambda s: s


@overload_attribute(SeriesType, 'hasnans', inline='always')
def overload_series_hasnans(s):
    return lambda s: s.isna().sum() != 0


@overload_attribute(HeterogeneousSeriesType, 'empty')
@overload_attribute(SeriesType, 'empty')
def overload_series_empty(s):
    return lambda s: len(bodo.hiframes.pd_series_ext.get_series_data(s)) == 0


@overload_attribute(SeriesType, 'dtypes', inline='always')
def overload_series_dtypes(s):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(s,
        'Series.dtypes')
    return lambda s: s.dtype


@overload_attribute(HeterogeneousSeriesType, 'name', inline='always')
@overload_attribute(SeriesType, 'name', inline='always')
def overload_series_name(s):
    return lambda s: bodo.hiframes.pd_series_ext.get_series_name(s)


@overload(len, no_unliteral=True)
def overload_series_len(S):
    if isinstance(S, (SeriesType, HeterogeneousSeriesType)):
        return lambda S: len(bodo.hiframes.pd_series_ext.get_series_data(S))


@overload_method(SeriesType, 'copy', inline='always', no_unliteral=True)
def overload_series_copy(S, deep=True):
    if is_overload_true(deep):

        def impl1(S, deep=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr.copy(),
                index, name)
        return impl1
    if is_overload_false(deep):

        def impl2(S, deep=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
        return impl2

    def impl(S, deep=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        if deep:
            arr = arr.copy()
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
    return impl


@overload_method(SeriesType, 'to_list', no_unliteral=True)
@overload_method(SeriesType, 'tolist', no_unliteral=True)
def overload_series_to_list(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.tolist()')
    if isinstance(S.dtype, types.Float):

        def impl_float(S):
            bjj__uhy = list()
            for uek__gymrr in range(len(S)):
                bjj__uhy.append(S.iat[uek__gymrr])
            return bjj__uhy
        return impl_float

    def impl(S):
        bjj__uhy = list()
        for uek__gymrr in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, uek__gymrr):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            bjj__uhy.append(S.iat[uek__gymrr])
        return bjj__uhy
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    nmlga__svejm = dict(dtype=dtype, copy=copy, na_value=na_value)
    zjkg__vpkwi = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    nmlga__svejm = dict(name=name, inplace=inplace)
    zjkg__vpkwi = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not bodo.hiframes.dataframe_impl._is_all_levels(S, level):
        raise_bodo_error(
            'Series.reset_index(): only dropping all index levels supported')
    if not is_overload_constant_bool(drop):
        raise_bodo_error(
            "Series.reset_index(): 'drop' parameter should be a constant boolean value"
            )
    if is_overload_true(drop):

        def impl_drop(S, level=None, drop=False, name=None, inplace=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_index_ext.init_range_index(0, len(arr),
                1, None)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
        return impl_drop

    def get_name_literal(name_typ, is_index=False, series_name=None):
        if is_overload_none(name_typ):
            if is_index:
                return 'index' if series_name != 'index' else 'level_0'
            return 0
        if is_literal_type(name_typ):
            return get_literal_value(name_typ)
        else:
            raise BodoError(
                'Series.reset_index() not supported for non-literal series names'
                )
    series_name = get_name_literal(S.name_typ)
    if isinstance(S.index, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        uaqv__nyb = ', '.join(['index_arrs[{}]'.format(uek__gymrr) for
            uek__gymrr in range(S.index.nlevels)])
    else:
        uaqv__nyb = '    bodo.utils.conversion.index_to_array(index)\n'
    nku__bnpc = 'index' if 'index' != series_name else 'level_0'
    ztqn__rwtkg = get_index_names(S.index, 'Series.reset_index()', nku__bnpc)
    columns = [name for name in ztqn__rwtkg]
    columns.append(series_name)
    dct__vba = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    dct__vba += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    dct__vba += '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    if isinstance(S.index, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        dct__vba += (
            '    index_arrs = bodo.hiframes.pd_index_ext.get_index_data(index)\n'
            )
    dct__vba += (
        '    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)\n'
        )
    dct__vba += f"""    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({uaqv__nyb}, arr), df_index, __col_name_meta_value_series_reset_index)
"""
    fertk__qecdz = {}
    exec(dct__vba, {'bodo': bodo,
        '__col_name_meta_value_series_reset_index': ColNamesMetaType(tuple(
        columns))}, fertk__qecdz)
    kylv__vnci = fertk__qecdz['_impl']
    return kylv__vnci


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mqtlv__emc = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc, index, name)
    return impl


@overload_method(SeriesType, 'round', inline='always', no_unliteral=True)
def overload_series_round(S, decimals=0):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.round()')

    def impl(S, decimals=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(arr)
        mqtlv__emc = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for uek__gymrr in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[uek__gymrr]):
                bodo.libs.array_kernels.setna(mqtlv__emc, uek__gymrr)
            else:
                mqtlv__emc[uek__gymrr] = np.round(arr[uek__gymrr], decimals)
        return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc, index, name)
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    nmlga__svejm = dict(level=level, numeric_only=numeric_only)
    zjkg__vpkwi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.sum(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.sum(): skipna argument must be a boolean')
    if not is_overload_int(min_count):
        raise BodoError('Series.sum(): min_count argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.sum()'
        )

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None,
        min_count=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_sum(arr, skipna, min_count)
    return impl


@overload_method(SeriesType, 'prod', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'product', inline='always', no_unliteral=True)
def overload_series_prod(S, axis=None, skipna=True, level=None,
    numeric_only=None, min_count=0):
    nmlga__svejm = dict(level=level, numeric_only=numeric_only)
    zjkg__vpkwi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.product(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.product(): skipna argument must be a boolean')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.product()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None,
        min_count=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_prod(arr, skipna, min_count)
    return impl


@overload_method(SeriesType, 'any', inline='always', no_unliteral=True)
def overload_series_any(S, axis=0, bool_only=None, skipna=True, level=None):
    nmlga__svejm = dict(axis=axis, bool_only=bool_only, skipna=skipna,
        level=level)
    zjkg__vpkwi = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.any()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_any(A)
    return impl


@overload_method(SeriesType, 'equals', inline='always', no_unliteral=True)
def overload_series_equals(S, other):
    if not isinstance(other, SeriesType):
        raise BodoError("Series.equals() 'other' must be a Series")
    if isinstance(S.data, bodo.ArrayItemArrayType):
        raise BodoError(
            'Series.equals() not supported for Series where each element is an array or list'
            )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.equals()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.equals()')
    if S.data != other.data:
        return lambda S, other: False

    def impl(S, other):
        atxy__yrqp = bodo.hiframes.pd_series_ext.get_series_data(S)
        eelv__ibr = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        mckvh__pht = 0
        for uek__gymrr in numba.parfors.parfor.internal_prange(len(atxy__yrqp)
            ):
            yekp__crft = 0
            zmhi__tfxz = bodo.libs.array_kernels.isna(atxy__yrqp, uek__gymrr)
            zus__dwlyh = bodo.libs.array_kernels.isna(eelv__ibr, uek__gymrr)
            if zmhi__tfxz and not zus__dwlyh or not zmhi__tfxz and zus__dwlyh:
                yekp__crft = 1
            elif not zmhi__tfxz:
                if atxy__yrqp[uek__gymrr] != eelv__ibr[uek__gymrr]:
                    yekp__crft = 1
            mckvh__pht += yekp__crft
        return mckvh__pht == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    nmlga__svejm = dict(axis=axis, bool_only=bool_only, skipna=skipna,
        level=level)
    zjkg__vpkwi = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.all()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_all(A)
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    nmlga__svejm = dict(level=level)
    zjkg__vpkwi = dict(level=None)
    check_unsupported_args('Series.mad', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(skipna):
        raise BodoError("Series.mad(): 'skipna' argument must be a boolean")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mad(): axis argument not supported')
    gow__pyad = types.float64
    uwuil__yle = types.float64
    if S.dtype == types.float32:
        gow__pyad = types.float32
        uwuil__yle = types.float32
    exwrd__fpjnm = gow__pyad(0)
    uyh__bdorw = uwuil__yle(0)
    dkd__jszif = uwuil__yle(1)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.mad()'
        )

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        wlnft__kllu = exwrd__fpjnm
        mckvh__pht = uyh__bdorw
        for uek__gymrr in numba.parfors.parfor.internal_prange(len(A)):
            yekp__crft = exwrd__fpjnm
            mbqn__lbsp = uyh__bdorw
            if not bodo.libs.array_kernels.isna(A, uek__gymrr) or not skipna:
                yekp__crft = A[uek__gymrr]
                mbqn__lbsp = dkd__jszif
            wlnft__kllu += yekp__crft
            mckvh__pht += mbqn__lbsp
        fphln__hjnd = bodo.hiframes.series_kernels._mean_handle_nan(wlnft__kllu
            , mckvh__pht)
        knlvn__tzw = exwrd__fpjnm
        for uek__gymrr in numba.parfors.parfor.internal_prange(len(A)):
            yekp__crft = exwrd__fpjnm
            if not bodo.libs.array_kernels.isna(A, uek__gymrr) or not skipna:
                yekp__crft = abs(A[uek__gymrr] - fphln__hjnd)
            knlvn__tzw += yekp__crft
        zokzi__zkqy = bodo.hiframes.series_kernels._mean_handle_nan(knlvn__tzw,
            mckvh__pht)
        return zokzi__zkqy
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    nmlga__svejm = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    zjkg__vpkwi = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mean(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.mean()')

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_mean(arr)
    return impl


@overload_method(SeriesType, 'sem', inline='always', no_unliteral=True)
def overload_series_sem(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    nmlga__svejm = dict(level=level, numeric_only=numeric_only)
    zjkg__vpkwi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.sem(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.sem(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.sem(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.sem()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        xiu__kukbz = 0
        dbkn__mdqll = 0
        mckvh__pht = 0
        for uek__gymrr in numba.parfors.parfor.internal_prange(len(A)):
            yekp__crft = 0
            mbqn__lbsp = 0
            if not bodo.libs.array_kernels.isna(A, uek__gymrr) or not skipna:
                yekp__crft = A[uek__gymrr]
                mbqn__lbsp = 1
            xiu__kukbz += yekp__crft
            dbkn__mdqll += yekp__crft * yekp__crft
            mckvh__pht += mbqn__lbsp
        tmt__opo = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            xiu__kukbz, dbkn__mdqll, mckvh__pht, ddof)
        umxu__mqw = bodo.hiframes.series_kernels._sem_handle_nan(tmt__opo,
            mckvh__pht)
        return umxu__mqw
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    nmlga__svejm = dict(level=level, numeric_only=numeric_only)
    zjkg__vpkwi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.kurtosis(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError(
            "Series.kurtosis(): 'skipna' argument must be a boolean")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.kurtosis()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        xiu__kukbz = 0.0
        dbkn__mdqll = 0.0
        vct__ieu = 0.0
        bzcko__qlft = 0.0
        mckvh__pht = 0
        for uek__gymrr in numba.parfors.parfor.internal_prange(len(A)):
            yekp__crft = 0.0
            mbqn__lbsp = 0
            if not bodo.libs.array_kernels.isna(A, uek__gymrr) or not skipna:
                yekp__crft = np.float64(A[uek__gymrr])
                mbqn__lbsp = 1
            xiu__kukbz += yekp__crft
            dbkn__mdqll += yekp__crft ** 2
            vct__ieu += yekp__crft ** 3
            bzcko__qlft += yekp__crft ** 4
            mckvh__pht += mbqn__lbsp
        tmt__opo = bodo.hiframes.series_kernels.compute_kurt(xiu__kukbz,
            dbkn__mdqll, vct__ieu, bzcko__qlft, mckvh__pht)
        return tmt__opo
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    nmlga__svejm = dict(level=level, numeric_only=numeric_only)
    zjkg__vpkwi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.skew(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.skew(): skipna argument must be a boolean')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.skew()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        xiu__kukbz = 0.0
        dbkn__mdqll = 0.0
        vct__ieu = 0.0
        mckvh__pht = 0
        for uek__gymrr in numba.parfors.parfor.internal_prange(len(A)):
            yekp__crft = 0.0
            mbqn__lbsp = 0
            if not bodo.libs.array_kernels.isna(A, uek__gymrr) or not skipna:
                yekp__crft = np.float64(A[uek__gymrr])
                mbqn__lbsp = 1
            xiu__kukbz += yekp__crft
            dbkn__mdqll += yekp__crft ** 2
            vct__ieu += yekp__crft ** 3
            mckvh__pht += mbqn__lbsp
        tmt__opo = bodo.hiframes.series_kernels.compute_skew(xiu__kukbz,
            dbkn__mdqll, vct__ieu, mckvh__pht)
        return tmt__opo
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    nmlga__svejm = dict(level=level, numeric_only=numeric_only)
    zjkg__vpkwi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.var(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.var(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.var(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.var()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_var(arr, skipna, ddof)
    return impl


@overload_method(SeriesType, 'std', inline='always', no_unliteral=True)
def overload_series_std(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    nmlga__svejm = dict(level=level, numeric_only=numeric_only)
    zjkg__vpkwi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.std(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.std(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.std(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.std()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_std(arr, skipna, ddof)
    return impl


@overload_method(SeriesType, 'dot', inline='always', no_unliteral=True)
def overload_series_dot(S, other):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.dot()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.dot()')

    def impl(S, other):
        atxy__yrqp = bodo.hiframes.pd_series_ext.get_series_data(S)
        eelv__ibr = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        vhy__ono = 0
        for uek__gymrr in numba.parfors.parfor.internal_prange(len(atxy__yrqp)
            ):
            sjsq__myfd = atxy__yrqp[uek__gymrr]
            fwpw__xgea = eelv__ibr[uek__gymrr]
            vhy__ono += sjsq__myfd * fwpw__xgea
        return vhy__ono
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=None, skipna=True):
    nmlga__svejm = dict(skipna=skipna)
    zjkg__vpkwi = dict(skipna=True)
    check_unsupported_args('Series.cumsum', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cumsum(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cumsum()')

    def impl(S, axis=None, skipna=True):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(A.cumsum(), index, name)
    return impl


@overload_method(SeriesType, 'cumprod', inline='always', no_unliteral=True)
def overload_series_cumprod(S, axis=None, skipna=True):
    nmlga__svejm = dict(skipna=skipna)
    zjkg__vpkwi = dict(skipna=True)
    check_unsupported_args('Series.cumprod', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cumprod(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cumprod()')

    def impl(S, axis=None, skipna=True):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(A.cumprod(), index, name
            )
    return impl


@overload_method(SeriesType, 'cummin', inline='always', no_unliteral=True)
def overload_series_cummin(S, axis=None, skipna=True):
    nmlga__svejm = dict(skipna=skipna)
    zjkg__vpkwi = dict(skipna=True)
    check_unsupported_args('Series.cummin', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cummin(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cummin()')

    def impl(S, axis=None, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.cummin(arr), index, name)
    return impl


@overload_method(SeriesType, 'cummax', inline='always', no_unliteral=True)
def overload_series_cummax(S, axis=None, skipna=True):
    nmlga__svejm = dict(skipna=skipna)
    zjkg__vpkwi = dict(skipna=True)
    check_unsupported_args('Series.cummax', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cummax(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cummax()')

    def impl(S, axis=None, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.cummax(arr), index, name)
    return impl


@overload_method(SeriesType, 'rename', inline='always', no_unliteral=True)
def overload_series_rename(S, index=None, axis=None, copy=True, inplace=
    False, level=None, errors='ignore'):
    if not (index == bodo.string_type or isinstance(index, types.StringLiteral)
        ):
        raise BodoError("Series.rename() 'index' can only be a string")
    nmlga__svejm = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    zjkg__vpkwi = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        spfrr__yfxq = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, spfrr__yfxq, index)
    return impl


@overload_method(SeriesType, 'rename_axis', inline='always', no_unliteral=True)
def overload_series_rename_axis(S, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False):
    nmlga__svejm = dict(index=index, columns=columns, axis=axis, copy=copy,
        inplace=inplace)
    zjkg__vpkwi = dict(index=None, columns=None, axis=None, copy=True,
        inplace=False)
    check_unsupported_args('Series.rename_axis', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if is_overload_none(mapper) or not is_scalar_type(mapper):
        raise BodoError(
            "Series.rename_axis(): 'mapper' is required and must be a scalar type."
            )

    def impl(S, mapper=None, index=None, columns=None, axis=None, copy=True,
        inplace=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        index = index.rename(mapper)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
    return impl


@overload_method(SeriesType, 'abs', inline='always', no_unliteral=True)
def overload_series_abs(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.abs()'
        )

    def impl(S):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(np.abs(A), index, name)
    return impl


@overload_method(SeriesType, 'count', no_unliteral=True)
def overload_series_count(S, level=None):
    nmlga__svejm = dict(level=level)
    zjkg__vpkwi = dict(level=None)
    check_unsupported_args('Series.count', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    nmlga__svejm = dict(method=method, min_periods=min_periods)
    zjkg__vpkwi = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.corr()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.corr()')

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        hem__pxxoc = S.sum()
        gxfr__icjy = other.sum()
        a = n * (S * other).sum() - hem__pxxoc * gxfr__icjy
        nipo__wlmjj = n * (S ** 2).sum() - hem__pxxoc ** 2
        hnpeg__dzrg = n * (other ** 2).sum() - gxfr__icjy ** 2
        return a / np.sqrt(nipo__wlmjj * hnpeg__dzrg)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    nmlga__svejm = dict(min_periods=min_periods)
    zjkg__vpkwi = dict(min_periods=None)
    check_unsupported_args('Series.cov', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.cov()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.cov()')

    def impl(S, other, min_periods=None, ddof=1):
        hem__pxxoc = S.mean()
        gxfr__icjy = other.mean()
        eeijh__lucmv = ((S - hem__pxxoc) * (other - gxfr__icjy)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(eeijh__lucmv, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            zih__rqeot = np.sign(sum_val)
            return np.inf * zih__rqeot
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    nmlga__svejm = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    zjkg__vpkwi = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.min(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.min(): only ordered categoricals are possible')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.min()'
        )

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_min(arr)
    return impl


@overload(max, no_unliteral=True)
def overload_series_builtins_max(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.max()
        return impl


@overload(min, no_unliteral=True)
def overload_series_builtins_min(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.min()
        return impl


@overload(sum, no_unliteral=True)
def overload_series_builtins_sum(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.sum()
        return impl


@overload(np.prod, inline='always', no_unliteral=True)
def overload_series_np_prod(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.prod()
        return impl


@overload_method(SeriesType, 'max', inline='always', no_unliteral=True)
def overload_series_max(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    nmlga__svejm = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    zjkg__vpkwi = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.max(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.max(): only ordered categoricals are possible')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.max()'
        )

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_max(arr)
    return impl


@overload_method(SeriesType, 'idxmin', inline='always', no_unliteral=True)
def overload_series_idxmin(S, axis=0, skipna=True):
    nmlga__svejm = dict(axis=axis, skipna=skipna)
    zjkg__vpkwi = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.idxmin()')
    if not (S.dtype == types.none or bodo.utils.utils.is_np_array_typ(S.
        data) and (S.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
        isinstance(S.dtype, (types.Number, types.Boolean))) or isinstance(S
        .data, (bodo.IntegerArrayType, bodo.CategoricalArrayType)) or S.
        data in [bodo.boolean_array, bodo.datetime_date_array_type]):
        raise BodoError(
            f'Series.idxmin() only supported for numeric array types. Array type: {S.data} not supported.'
            )
    if isinstance(S.data, bodo.CategoricalArrayType) and not S.dtype.ordered:
        raise BodoError(
            'Series.idxmin(): only ordered categoricals are possible')

    def impl(S, axis=0, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.libs.array_ops.array_op_idxmin(arr, index)
    return impl


@overload_method(SeriesType, 'idxmax', inline='always', no_unliteral=True)
def overload_series_idxmax(S, axis=0, skipna=True):
    nmlga__svejm = dict(axis=axis, skipna=skipna)
    zjkg__vpkwi = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.idxmax()')
    if not (S.dtype == types.none or bodo.utils.utils.is_np_array_typ(S.
        data) and (S.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
        isinstance(S.dtype, (types.Number, types.Boolean))) or isinstance(S
        .data, (bodo.IntegerArrayType, bodo.CategoricalArrayType)) or S.
        data in [bodo.boolean_array, bodo.datetime_date_array_type]):
        raise BodoError(
            f'Series.idxmax() only supported for numeric array types. Array type: {S.data} not supported.'
            )
    if isinstance(S.data, bodo.CategoricalArrayType) and not S.dtype.ordered:
        raise BodoError(
            'Series.idxmax(): only ordered categoricals are possible')

    def impl(S, axis=0, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.libs.array_ops.array_op_idxmax(arr, index)
    return impl


@overload_method(SeriesType, 'infer_objects', inline='always')
def overload_series_infer_objects(S):
    return lambda S: S.copy()


@overload_attribute(SeriesType, 'is_monotonic', inline='always')
@overload_attribute(SeriesType, 'is_monotonic_increasing', inline='always')
def overload_series_is_monotonic_increasing(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.is_monotonic_increasing')
    return lambda S: bodo.libs.array_kernels.series_monotonicity(bodo.
        hiframes.pd_series_ext.get_series_data(S), 1)


@overload_attribute(SeriesType, 'is_monotonic_decreasing', inline='always')
def overload_series_is_monotonic_decreasing(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.is_monotonic_decreasing')
    return lambda S: bodo.libs.array_kernels.series_monotonicity(bodo.
        hiframes.pd_series_ext.get_series_data(S), 2)


@overload_attribute(SeriesType, 'nbytes', inline='always')
def overload_series_nbytes(S):
    return lambda S: bodo.hiframes.pd_series_ext.get_series_data(S).nbytes


@overload_method(SeriesType, 'autocorr', inline='always', no_unliteral=True)
def overload_series_autocorr(S, lag=1):
    return lambda S, lag=1: bodo.libs.array_kernels.autocorr(bodo.hiframes.
        pd_series_ext.get_series_data(S), lag)


@overload_method(SeriesType, 'median', inline='always', no_unliteral=True)
def overload_series_median(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    nmlga__svejm = dict(level=level, numeric_only=numeric_only)
    zjkg__vpkwi = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.median(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.median(): skipna argument must be a boolean')
    return (lambda S, axis=None, skipna=True, level=None, numeric_only=None:
        bodo.libs.array_ops.array_op_median(bodo.hiframes.pd_series_ext.
        get_series_data(S), skipna))


def overload_series_head(S, n=5):

    def impl(S, n=5):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        kif__wzgk = arr[:n]
        mrow__xdlq = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(kif__wzgk,
            mrow__xdlq, name)
    return impl


@lower_builtin('series.head', SeriesType, types.Integer)
@lower_builtin('series.head', SeriesType, types.Omitted)
def series_head_lower(context, builder, sig, args):
    impl = overload_series_head(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@numba.extending.register_jitable
def tail_slice(k, n):
    if n == 0:
        return k
    return -n


@overload_method(SeriesType, 'tail', inline='always', no_unliteral=True)
def overload_series_tail(S, n=5):
    if not is_overload_int(n):
        raise BodoError("Series.tail(): 'n' must be an Integer")

    def impl(S, n=5):
        rkt__xpz = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        kif__wzgk = arr[rkt__xpz:]
        mrow__xdlq = index[rkt__xpz:]
        return bodo.hiframes.pd_series_ext.init_series(kif__wzgk,
            mrow__xdlq, name)
    return impl


@overload_method(SeriesType, 'first', inline='always', no_unliteral=True)
def overload_series_first(S, offset):
    ltdq__kah = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in ltdq__kah:
        raise BodoError(
            "Series.first(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.first()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            sydj__ncuhk = index[0]
            ataoc__kduci = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                sydj__ncuhk, False))
        else:
            ataoc__kduci = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        kif__wzgk = arr[:ataoc__kduci]
        mrow__xdlq = index[:ataoc__kduci]
        return bodo.hiframes.pd_series_ext.init_series(kif__wzgk,
            mrow__xdlq, name)
    return impl


@overload_method(SeriesType, 'last', inline='always', no_unliteral=True)
def overload_series_last(S, offset):
    ltdq__kah = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in ltdq__kah:
        raise BodoError(
            "Series.last(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.last()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            mubs__ghogy = index[-1]
            ataoc__kduci = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                mubs__ghogy, True))
        else:
            ataoc__kduci = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        kif__wzgk = arr[len(arr) - ataoc__kduci:]
        mrow__xdlq = index[len(arr) - ataoc__kduci:]
        return bodo.hiframes.pd_series_ext.init_series(kif__wzgk,
            mrow__xdlq, name)
    return impl


@overload_method(SeriesType, 'first_valid_index', inline='always',
    no_unliteral=True)
def overload_series_first_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        pptyo__lfqai = bodo.utils.conversion.index_to_array(index)
        nifj__fixrd, uoke__agve = (bodo.libs.array_kernels.
            first_last_valid_index(arr, pptyo__lfqai))
        return uoke__agve if nifj__fixrd else None
    return impl


@overload_method(SeriesType, 'last_valid_index', inline='always',
    no_unliteral=True)
def overload_series_last_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        pptyo__lfqai = bodo.utils.conversion.index_to_array(index)
        nifj__fixrd, uoke__agve = (bodo.libs.array_kernels.
            first_last_valid_index(arr, pptyo__lfqai, False))
        return uoke__agve if nifj__fixrd else None
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    nmlga__svejm = dict(keep=keep)
    zjkg__vpkwi = dict(keep='first')
    check_unsupported_args('Series.nlargest', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nlargest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nlargest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        pptyo__lfqai = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mqtlv__emc, lepd__mzfb = bodo.libs.array_kernels.nlargest(arr,
            pptyo__lfqai, n, True, bodo.hiframes.series_kernels.gt_f)
        kbrnu__dibm = bodo.utils.conversion.convert_to_index(lepd__mzfb)
        return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
            kbrnu__dibm, name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    nmlga__svejm = dict(keep=keep)
    zjkg__vpkwi = dict(keep='first')
    check_unsupported_args('Series.nsmallest', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nsmallest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nsmallest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        pptyo__lfqai = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mqtlv__emc, lepd__mzfb = bodo.libs.array_kernels.nlargest(arr,
            pptyo__lfqai, n, False, bodo.hiframes.series_kernels.lt_f)
        kbrnu__dibm = bodo.utils.conversion.convert_to_index(lepd__mzfb)
        return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
            kbrnu__dibm, name)
    return impl


@overload_method(SeriesType, 'notnull', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'notna', inline='always', no_unliteral=True)
def overload_series_notna(S):
    return lambda S: S.isna() == False


@overload_method(SeriesType, 'astype', inline='always', no_unliteral=True)
@overload_method(HeterogeneousSeriesType, 'astype', inline='always',
    no_unliteral=True)
def overload_series_astype(S, dtype, copy=True, errors='raise',
    _bodo_nan_to_str=True):
    nmlga__svejm = dict(errors=errors)
    zjkg__vpkwi = dict(errors='raise')
    check_unsupported_args('Series.astype', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "Series.astype(): 'dtype' when passed as string must be a constant value"
            )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.astype()')

    def impl(S, dtype, copy=True, errors='raise', _bodo_nan_to_str=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mqtlv__emc = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc, index, name)
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    nmlga__svejm = dict(axis=axis, is_copy=is_copy)
    zjkg__vpkwi = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        rmyo__myimt = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[rmyo__myimt],
            index[rmyo__myimt], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    nmlga__svejm = dict(axis=axis, kind=kind, order=order)
    zjkg__vpkwi = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ranwc__kgwdo = S.notna().values
        if not ranwc__kgwdo.all():
            mqtlv__emc = np.full(n, -1, np.int64)
            mqtlv__emc[ranwc__kgwdo] = argsort(arr[ranwc__kgwdo])
        else:
            mqtlv__emc = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc, index, name)
    return impl


@overload_method(SeriesType, 'rank', inline='always', no_unliteral=True)
def overload_series_rank(S, axis=0, method='average', numeric_only=None,
    na_option='keep', ascending=True, pct=False):
    nmlga__svejm = dict(axis=axis, numeric_only=numeric_only)
    zjkg__vpkwi = dict(axis=0, numeric_only=None)
    check_unsupported_args('Series.rank', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not is_overload_constant_str(method):
        raise BodoError(
            "Series.rank(): 'method' argument must be a constant string")
    if not is_overload_constant_str(na_option):
        raise BodoError(
            "Series.rank(): 'na_option' argument must be a constant string")

    def impl(S, axis=0, method='average', numeric_only=None, na_option=
        'keep', ascending=True, pct=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mqtlv__emc = bodo.libs.array_kernels.rank(arr, method=method,
            na_option=na_option, ascending=ascending, pct=pct)
        return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc, index, name)
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    nmlga__svejm = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    zjkg__vpkwi = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_index(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_index(): 'na_position' should either be 'first' or 'last'"
            )
    xvhh__bzrt = ColNamesMetaType(('$_bodo_col3_',))

    def impl(S, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ctk__rkfsk = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, xvhh__bzrt)
        vaeob__veaw = ctk__rkfsk.sort_index(ascending=ascending, inplace=
            inplace, na_position=na_position)
        mqtlv__emc = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            vaeob__veaw, 0)
        kbrnu__dibm = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            vaeob__veaw)
        return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
            kbrnu__dibm, name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    nmlga__svejm = dict(axis=axis, inplace=inplace, kind=kind, ignore_index
        =ignore_index, key=key)
    zjkg__vpkwi = dict(axis=0, inplace=False, kind='quicksort',
        ignore_index=False, key=None)
    check_unsupported_args('Series.sort_values', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_values(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_values(): 'na_position' should either be 'first' or 'last'"
            )
    pplk__nyb = ColNamesMetaType(('$_bodo_col_',))

    def impl(S, axis=0, ascending=True, inplace=False, kind='quicksort',
        na_position='last', ignore_index=False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ctk__rkfsk = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, pplk__nyb)
        vaeob__veaw = ctk__rkfsk.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        mqtlv__emc = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            vaeob__veaw, 0)
        kbrnu__dibm = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            vaeob__veaw)
        return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
            kbrnu__dibm, name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    pqr__mju = is_overload_true(is_nullable)
    dct__vba = 'def impl(bins, arr, is_nullable=True, include_lowest=True):\n'
    dct__vba += '  numba.parfors.parfor.init_prange()\n'
    dct__vba += '  n = len(arr)\n'
    if pqr__mju:
        dct__vba += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        dct__vba += '  out_arr = np.empty(n, np.int64)\n'
    dct__vba += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    dct__vba += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if pqr__mju:
        dct__vba += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        dct__vba += '      out_arr[i] = -1\n'
    dct__vba += '      continue\n'
    dct__vba += '    val = arr[i]\n'
    dct__vba += '    if include_lowest and val == bins[0]:\n'
    dct__vba += '      ind = 1\n'
    dct__vba += '    else:\n'
    dct__vba += '      ind = np.searchsorted(bins, val)\n'
    dct__vba += '    if ind == 0 or ind == len(bins):\n'
    if pqr__mju:
        dct__vba += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        dct__vba += '      out_arr[i] = -1\n'
    dct__vba += '    else:\n'
    dct__vba += '      out_arr[i] = ind - 1\n'
    dct__vba += '  return out_arr\n'
    fertk__qecdz = {}
    exec(dct__vba, {'bodo': bodo, 'np': np, 'numba': numba}, fertk__qecdz)
    impl = fertk__qecdz['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        jtz__gnn, kfqdh__icz = np.divmod(x, 1)
        if jtz__gnn == 0:
            ivnql__dksqi = -int(np.floor(np.log10(abs(kfqdh__icz)))
                ) - 1 + precision
        else:
            ivnql__dksqi = precision
        return np.around(x, ivnql__dksqi)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        owo__kev = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(owo__kev)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        bia__okgn = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            xdyk__gcu = bins.copy()
            if right and include_lowest:
                xdyk__gcu[0] = xdyk__gcu[0] - bia__okgn
            tzouh__nlwz = bodo.libs.interval_arr_ext.init_interval_array(
                xdyk__gcu[:-1], xdyk__gcu[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(tzouh__nlwz,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        xdyk__gcu = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            xdyk__gcu[0] = xdyk__gcu[0] - 10.0 ** -precision
        tzouh__nlwz = bodo.libs.interval_arr_ext.init_interval_array(xdyk__gcu
            [:-1], xdyk__gcu[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(tzouh__nlwz, None
            )
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        cea__bmc = bodo.hiframes.pd_series_ext.get_series_data(count_series)
        gcgp__ptuvp = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        mqtlv__emc = np.zeros(nbins, np.int64)
        for uek__gymrr in range(len(cea__bmc)):
            mqtlv__emc[gcgp__ptuvp[uek__gymrr]] = cea__bmc[uek__gymrr]
        return mqtlv__emc
    return impl


def compute_bins(nbins, min_val, max_val):
    pass


@overload(compute_bins, no_unliteral=True)
def overload_compute_bins(nbins, min_val, max_val, right=True):

    def impl(nbins, min_val, max_val, right=True):
        if nbins < 1:
            raise ValueError('`bins` should be a positive integer.')
        min_val = min_val + 0.0
        max_val = max_val + 0.0
        if np.isinf(min_val) or np.isinf(max_val):
            raise ValueError(
                'cannot specify integer `bins` when input data contains infinity'
                )
        elif min_val == max_val:
            min_val -= 0.001 * abs(min_val) if min_val != 0 else 0.001
            max_val += 0.001 * abs(max_val) if max_val != 0 else 0.001
            bins = np.linspace(min_val, max_val, nbins + 1, endpoint=True)
        else:
            bins = np.linspace(min_val, max_val, nbins + 1, endpoint=True)
            eef__gqyxd = (max_val - min_val) * 0.001
            if right:
                bins[0] -= eef__gqyxd
            else:
                bins[-1] += eef__gqyxd
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    nmlga__svejm = dict(dropna=dropna)
    zjkg__vpkwi = dict(dropna=True)
    check_unsupported_args('Series.value_counts', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not is_overload_constant_bool(normalize):
        raise_bodo_error(
            'Series.value_counts(): normalize argument must be a constant boolean'
            )
    if not is_overload_constant_bool(sort):
        raise_bodo_error(
            'Series.value_counts(): sort argument must be a constant boolean')
    if not is_overload_bool(ascending):
        raise_bodo_error(
            'Series.value_counts(): ascending argument must be a constant boolean'
            )
    ffh__scfl = not is_overload_none(bins)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.value_counts()')
    dct__vba = 'def impl(\n'
    dct__vba += '    S,\n'
    dct__vba += '    normalize=False,\n'
    dct__vba += '    sort=True,\n'
    dct__vba += '    ascending=False,\n'
    dct__vba += '    bins=None,\n'
    dct__vba += '    dropna=True,\n'
    dct__vba += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    dct__vba += '):\n'
    dct__vba += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    dct__vba += '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    dct__vba += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    if ffh__scfl:
        dct__vba += '    right = True\n'
        dct__vba += _gen_bins_handling(bins, S.dtype)
        dct__vba += '    arr = get_bin_inds(bins, arr)\n'
    dct__vba += '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n'
    dct__vba += (
        '        (arr,), index, __col_name_meta_value_series_value_counts\n')
    dct__vba += '    )\n'
    dct__vba += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if ffh__scfl:
        dct__vba += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        dct__vba += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        dct__vba += '    index = get_bin_labels(bins)\n'
    else:
        dct__vba += (
            '    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)\n'
            )
        dct__vba += '    ind_arr = bodo.utils.conversion.coerce_to_array(\n'
        dct__vba += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        dct__vba += '    )\n'
        dct__vba += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    dct__vba += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        dct__vba += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        zfr__knfl = 'len(S)' if ffh__scfl else 'count_arr.sum()'
        dct__vba += f'    res = res / float({zfr__knfl})\n'
    dct__vba += '    return res\n'
    fertk__qecdz = {}
    exec(dct__vba, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins, '__col_name_meta_value_series_value_counts':
        ColNamesMetaType(('$_bodo_col2_',))}, fertk__qecdz)
    impl = fertk__qecdz['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    dct__vba = ''
    if isinstance(bins, types.Integer):
        dct__vba += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        dct__vba += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            dct__vba += '    min_val = min_val.value\n'
            dct__vba += '    max_val = max_val.value\n'
        dct__vba += '    bins = compute_bins(bins, min_val, max_val, right)\n'
        if dtype == bodo.datetime64ns:
            dct__vba += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        dct__vba += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return dct__vba


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    nmlga__svejm = dict(right=right, labels=labels, retbins=retbins,
        precision=precision, duplicates=duplicates, ordered=ordered)
    zjkg__vpkwi = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pandas.cut', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='General')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x, 'pandas.cut()'
        )
    dct__vba = 'def impl(\n'
    dct__vba += '    x,\n'
    dct__vba += '    bins,\n'
    dct__vba += '    right=True,\n'
    dct__vba += '    labels=None,\n'
    dct__vba += '    retbins=False,\n'
    dct__vba += '    precision=3,\n'
    dct__vba += '    include_lowest=False,\n'
    dct__vba += "    duplicates='raise',\n"
    dct__vba += '    ordered=True\n'
    dct__vba += '):\n'
    if isinstance(x, SeriesType):
        dct__vba += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        dct__vba += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        dct__vba += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        dct__vba += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    dct__vba += _gen_bins_handling(bins, x.dtype)
    dct__vba += '    arr = get_bin_inds(bins, arr, False, include_lowest)\n'
    dct__vba += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    dct__vba += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None, None)
"""
    dct__vba += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        dct__vba += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        dct__vba += '    return res\n'
    else:
        dct__vba += '    return out_arr\n'
    fertk__qecdz = {}
    exec(dct__vba, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, fertk__qecdz)
    impl = fertk__qecdz['impl']
    return impl


def _get_q_list(q):
    return q


@overload(_get_q_list, no_unliteral=True)
def get_q_list_overload(q):
    if is_overload_int(q):
        return lambda q: np.linspace(0, 1, q + 1)
    return lambda q: q


@overload(pd.unique, inline='always', no_unliteral=True)
def overload_unique(values):
    if not is_series_type(values) and not (bodo.utils.utils.is_array_typ(
        values, False) and values.ndim == 1):
        raise BodoError(
            "pd.unique(): 'values' must be either a Series or a 1-d array")
    if is_series_type(values):

        def impl(values):
            arr = bodo.hiframes.pd_series_ext.get_series_data(values)
            return bodo.allgatherv(bodo.libs.array_kernels.unique(arr), False)
        return impl
    else:
        return lambda values: bodo.allgatherv(bodo.libs.array_kernels.
            unique(values), False)


@overload(pd.qcut, inline='always', no_unliteral=True)
def overload_qcut(x, q, labels=None, retbins=False, precision=3, duplicates
    ='raise'):
    nmlga__svejm = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    zjkg__vpkwi = dict(labels=None, retbins=False, precision=3, duplicates=
        'raise')
    check_unsupported_args('pandas.qcut', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='General')
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'pandas.qcut()')

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        bsny__eohta = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, bsny__eohta)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    nmlga__svejm = dict(axis=axis, sort=sort, group_keys=group_keys,
        squeeze=squeeze, observed=observed, dropna=dropna)
    zjkg__vpkwi = dict(axis=0, sort=True, group_keys=True, squeeze=False,
        observed=True, dropna=True)
    check_unsupported_args('Series.groupby', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='GroupBy')
    if not is_overload_true(as_index):
        raise BodoError('as_index=False only valid with DataFrame')
    if is_overload_none(by) and is_overload_none(level):
        raise BodoError("You have to supply one of 'by' and 'level'")
    if not is_overload_none(by) and not is_overload_none(level):
        raise BodoError(
            "Series.groupby(): 'level' argument should be None if 'by' is not None"
            )
    if not is_overload_none(level):
        if not (is_overload_constant_int(level) and get_overload_const_int(
            level) == 0) or isinstance(S.index, bodo.hiframes.
            pd_multi_index_ext.MultiIndexType):
            raise BodoError(
                "Series.groupby(): MultiIndex case or 'level' other than 0 not supported yet"
                )
        vzjj__hfjmf = ColNamesMetaType((' ', ''))

        def impl_index(S, by=None, axis=0, level=None, as_index=True, sort=
            True, group_keys=True, squeeze=False, observed=True, dropna=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            cla__yoizf = bodo.utils.conversion.coerce_to_array(index)
            ctk__rkfsk = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                cla__yoizf, arr), index, vzjj__hfjmf)
            return ctk__rkfsk.groupby(' ')['']
        return impl_index
    gdj__xhi = by
    if isinstance(by, SeriesType):
        gdj__xhi = by.data
    if isinstance(gdj__xhi, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )
    nbw__xbuv = ColNamesMetaType((' ', ''))

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        cla__yoizf = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        ctk__rkfsk = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            cla__yoizf, arr), index, nbw__xbuv)
        return ctk__rkfsk.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    nmlga__svejm = dict(verify_integrity=verify_integrity)
    zjkg__vpkwi = dict(verify_integrity=False)
    check_unsupported_args('Series.append', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(to_append,
        'Series.append()')
    if isinstance(to_append, SeriesType):
        return (lambda S, to_append, ignore_index=False, verify_integrity=
            False: pd.concat((S, to_append), ignore_index=ignore_index,
            verify_integrity=verify_integrity))
    if isinstance(to_append, types.BaseTuple):
        return (lambda S, to_append, ignore_index=False, verify_integrity=
            False: pd.concat((S,) + to_append, ignore_index=ignore_index,
            verify_integrity=verify_integrity))
    return (lambda S, to_append, ignore_index=False, verify_integrity=False:
        pd.concat([S] + to_append, ignore_index=ignore_index,
        verify_integrity=verify_integrity))


@overload_method(SeriesType, 'isin', inline='always', no_unliteral=True)
def overload_series_isin(S, values):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.isin()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(values,
        'Series.isin()')
    if bodo.utils.utils.is_array_typ(values):

        def impl_arr(S, values):
            ycslj__tuatf = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            mqtlv__emc = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(mqtlv__emc, A, ycslj__tuatf, False)
            return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                index, name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mqtlv__emc = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc, index, name)
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    nmlga__svejm = dict(interpolation=interpolation)
    zjkg__vpkwi = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.quantile()')
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            mqtlv__emc = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                index, name)
        return impl_list
    elif isinstance(q, (float, types.Number)) or is_overload_constant_int(q):

        def impl(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            return bodo.libs.array_ops.array_op_quantile(arr, q)
        return impl
    else:
        raise BodoError(
            f'Series.quantile() q type must be float or iterable of floats only.'
            )


@overload_method(SeriesType, 'nunique', inline='always', no_unliteral=True)
def overload_series_nunique(S, dropna=True):
    if not is_overload_bool(dropna):
        raise BodoError('Series.nunique: dropna must be a boolean value')

    def impl(S, dropna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_kernels.nunique(arr, dropna)
    return impl


@overload_method(SeriesType, 'unique', inline='always', no_unliteral=True)
def overload_series_unique(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        sqpc__lffnn = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(sqpc__lffnn, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    nmlga__svejm = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    zjkg__vpkwi = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.describe()')
    if not (isinstance(S.data, types.Array) and (isinstance(S.data.dtype,
        types.Number) or S.data.dtype == bodo.datetime64ns)
        ) and not isinstance(S.data, IntegerArrayType):
        raise BodoError(f'describe() column input type {S.data} not supported.'
            )
    if S.data.dtype == bodo.datetime64ns:

        def impl_dt(S, percentiles=None, include=None, exclude=None,
            datetime_is_numeric=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
                array_ops.array_op_describe(arr), bodo.utils.conversion.
                convert_to_index(['count', 'mean', 'min', '25%', '50%',
                '75%', 'max']), name)
        return impl_dt

    def impl(S, percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.array_ops.
            array_op_describe(arr), bodo.utils.conversion.convert_to_index(
            ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']), name)
    return impl


@overload_method(SeriesType, 'memory_usage', inline='always', no_unliteral=True
    )
def overload_series_memory_usage(S, index=True, deep=False):
    if is_overload_true(index):

        def impl(S, index=True, deep=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            return arr.nbytes + index.nbytes
        return impl
    else:

        def impl(S, index=True, deep=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            return arr.nbytes
        return impl


def binary_str_fillna_inplace_series_impl(is_binary=False):
    if is_binary:
        nytk__gjznx = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        nytk__gjznx = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    dct__vba = '\n'.join(('def impl(', '    S,', '    value=None,',
        '    method=None,', '    axis=None,', '    inplace=False,',
        '    limit=None,', '    downcast=None,', '):',
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)',
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)',
        '    n = len(in_arr)', '    nf = len(fill_arr)',
        "    assert n == nf, 'fillna() requires same length arrays'",
        f'    out_arr = {nytk__gjznx}(n, -1)',
        '    for j in numba.parfors.parfor.internal_prange(n):',
        '        s = in_arr[j]',
        '        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna('
        , '            fill_arr, j', '        ):',
        '            s = fill_arr[j]', '        out_arr[j] = s',
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)'
        ))
    zzc__elk = dict()
    exec(dct__vba, {'bodo': bodo, 'numba': numba}, zzc__elk)
    iybfm__zcqey = zzc__elk['impl']
    return iybfm__zcqey


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        nytk__gjznx = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        nytk__gjznx = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    dct__vba = 'def impl(S,\n'
    dct__vba += '     value=None,\n'
    dct__vba += '    method=None,\n'
    dct__vba += '    axis=None,\n'
    dct__vba += '    inplace=False,\n'
    dct__vba += '    limit=None,\n'
    dct__vba += '   downcast=None,\n'
    dct__vba += '):\n'
    dct__vba += '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    dct__vba += '    n = len(in_arr)\n'
    dct__vba += f'    out_arr = {nytk__gjznx}(n, -1)\n'
    dct__vba += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    dct__vba += '        s = in_arr[j]\n'
    dct__vba += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    dct__vba += '            s = value\n'
    dct__vba += '        out_arr[j] = s\n'
    dct__vba += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    zzc__elk = dict()
    exec(dct__vba, {'bodo': bodo, 'numba': numba}, zzc__elk)
    iybfm__zcqey = zzc__elk['impl']
    return iybfm__zcqey


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    syl__fxss = bodo.hiframes.pd_series_ext.get_series_data(S)
    kgsrm__ydl = bodo.hiframes.pd_series_ext.get_series_data(value)
    for uek__gymrr in numba.parfors.parfor.internal_prange(len(syl__fxss)):
        s = syl__fxss[uek__gymrr]
        if bodo.libs.array_kernels.isna(syl__fxss, uek__gymrr
            ) and not bodo.libs.array_kernels.isna(kgsrm__ydl, uek__gymrr):
            s = kgsrm__ydl[uek__gymrr]
        syl__fxss[uek__gymrr] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    syl__fxss = bodo.hiframes.pd_series_ext.get_series_data(S)
    for uek__gymrr in numba.parfors.parfor.internal_prange(len(syl__fxss)):
        s = syl__fxss[uek__gymrr]
        if bodo.libs.array_kernels.isna(syl__fxss, uek__gymrr):
            s = value
        syl__fxss[uek__gymrr] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    syl__fxss = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    kgsrm__ydl = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(syl__fxss)
    mqtlv__emc = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for vsjt__afsv in numba.parfors.parfor.internal_prange(n):
        s = syl__fxss[vsjt__afsv]
        if bodo.libs.array_kernels.isna(syl__fxss, vsjt__afsv
            ) and not bodo.libs.array_kernels.isna(kgsrm__ydl, vsjt__afsv):
            s = kgsrm__ydl[vsjt__afsv]
        mqtlv__emc[vsjt__afsv] = s
        if bodo.libs.array_kernels.isna(syl__fxss, vsjt__afsv
            ) and bodo.libs.array_kernels.isna(kgsrm__ydl, vsjt__afsv):
            bodo.libs.array_kernels.setna(mqtlv__emc, vsjt__afsv)
    return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    syl__fxss = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    kgsrm__ydl = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(syl__fxss)
    mqtlv__emc = bodo.utils.utils.alloc_type(n, syl__fxss.dtype, (-1,))
    for uek__gymrr in numba.parfors.parfor.internal_prange(n):
        s = syl__fxss[uek__gymrr]
        if bodo.libs.array_kernels.isna(syl__fxss, uek__gymrr
            ) and not bodo.libs.array_kernels.isna(kgsrm__ydl, uek__gymrr):
            s = kgsrm__ydl[uek__gymrr]
        mqtlv__emc[uek__gymrr] = s
    return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    nmlga__svejm = dict(limit=limit, downcast=downcast)
    zjkg__vpkwi = dict(limit=None, downcast=None)
    check_unsupported_args('Series.fillna', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    bamm__wxq = not is_overload_none(value)
    bebkp__ntdx = not is_overload_none(method)
    if bamm__wxq and bebkp__ntdx:
        raise BodoError(
            "Series.fillna(): Cannot specify both 'value' and 'method'.")
    if not bamm__wxq and not bebkp__ntdx:
        raise BodoError(
            "Series.fillna(): Must specify one of 'value' and 'method'.")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.fillna(): axis argument not supported')
    elif is_iterable_type(value) and not isinstance(value, SeriesType):
        raise BodoError('Series.fillna(): "value" parameter cannot be a list')
    elif is_var_size_item_array_type(S.data
        ) and not S.dtype == bodo.string_type:
        raise BodoError(
            f'Series.fillna() with inplace=True not supported for {S.dtype} values yet.'
            )
    if not is_overload_constant_bool(inplace):
        raise_bodo_error(
            "Series.fillna(): 'inplace' argument must be a constant boolean")
    if bebkp__ntdx:
        if is_overload_true(inplace):
            raise BodoError(
                "Series.fillna() with inplace=True not supported with 'method' argument yet."
                )
        jzggc__trcla = (
            "Series.fillna(): 'method' argument if provided must be a constant string and one of ('backfill', 'bfill', 'pad' 'ffill')."
            )
        if not is_overload_constant_str(method):
            raise_bodo_error(jzggc__trcla)
        elif get_overload_const_str(method) not in ('backfill', 'bfill',
            'pad', 'ffill'):
            raise BodoError(jzggc__trcla)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.fillna()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'Series.fillna()')
    jubnf__wrt = element_type(S.data)
    bygyn__tybd = None
    if bamm__wxq:
        bygyn__tybd = element_type(types.unliteral(value))
    if bygyn__tybd and not can_replace(jubnf__wrt, bygyn__tybd):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {bygyn__tybd} with series type {jubnf__wrt}'
            )
    if is_overload_true(inplace):
        if S.dtype == bodo.string_type:
            if S.data == bodo.dict_str_arr_type:
                raise_bodo_error(
                    "Series.fillna(): 'inplace' not supported for dictionary-encoded string arrays yet."
                    )
            if is_overload_constant_str(value) and get_overload_const_str(value
                ) == '':
                return (lambda S, value=None, method=None, axis=None,
                    inplace=False, limit=None, downcast=None: bodo.libs.
                    str_arr_ext.set_null_bits_to_value(bodo.hiframes.
                    pd_series_ext.get_series_data(S), -1))
            if isinstance(value, SeriesType):
                return binary_str_fillna_inplace_series_impl(is_binary=False)
            return binary_str_fillna_inplace_impl(is_binary=False)
        if S.dtype == bodo.bytes_type:
            if is_overload_constant_bytes(value) and get_overload_const_bytes(
                value) == b'':
                return (lambda S, value=None, method=None, axis=None,
                    inplace=False, limit=None, downcast=None: bodo.libs.
                    str_arr_ext.set_null_bits_to_value(bodo.hiframes.
                    pd_series_ext.get_series_data(S), -1))
            if isinstance(value, SeriesType):
                return binary_str_fillna_inplace_series_impl(is_binary=True)
            return binary_str_fillna_inplace_impl(is_binary=True)
        else:
            if isinstance(value, SeriesType):
                return fillna_inplace_series_impl
            return fillna_inplace_impl
    else:
        yffbj__bgkim = to_str_arr_if_dict_array(S.data)
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                syl__fxss = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                kgsrm__ydl = bodo.hiframes.pd_series_ext.get_series_data(value)
                n = len(syl__fxss)
                mqtlv__emc = bodo.utils.utils.alloc_type(n, yffbj__bgkim, (-1,)
                    )
                for uek__gymrr in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(syl__fxss, uek__gymrr
                        ) and bodo.libs.array_kernels.isna(kgsrm__ydl,
                        uek__gymrr):
                        bodo.libs.array_kernels.setna(mqtlv__emc, uek__gymrr)
                        continue
                    if bodo.libs.array_kernels.isna(syl__fxss, uek__gymrr):
                        mqtlv__emc[uek__gymrr
                            ] = bodo.utils.conversion.unbox_if_timestamp(
                            kgsrm__ydl[uek__gymrr])
                        continue
                    mqtlv__emc[uek__gymrr
                        ] = bodo.utils.conversion.unbox_if_timestamp(syl__fxss
                        [uek__gymrr])
                return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                    index, name)
            return fillna_series_impl
        if bebkp__ntdx:
            rsovy__tsbtu = (types.unicode_type, types.bool_, bodo.
                datetime64ns, bodo.timedelta64ns)
            if not isinstance(jubnf__wrt, (types.Integer, types.Float)
                ) and jubnf__wrt not in rsovy__tsbtu:
                raise BodoError(
                    f"Series.fillna(): series of type {jubnf__wrt} are not supported with 'method' argument."
                    )

            def fillna_method_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                syl__fxss = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                mqtlv__emc = bodo.libs.array_kernels.ffill_bfill_arr(syl__fxss,
                    method)
                return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                    index, name)
            return fillna_method_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_timestamp(value)
            syl__fxss = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(syl__fxss)
            mqtlv__emc = bodo.utils.utils.alloc_type(n, yffbj__bgkim, (-1,))
            for uek__gymrr in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_timestamp(syl__fxss[
                    uek__gymrr])
                if bodo.libs.array_kernels.isna(syl__fxss, uek__gymrr):
                    s = value
                mqtlv__emc[uek__gymrr] = s
            return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                index, name)
        return fillna_impl


def create_fillna_specific_method_overload(overload_name):

    def overload_series_fillna_specific_method(S, axis=None, inplace=False,
        limit=None, downcast=None):
        thb__bgd = {'ffill': 'ffill', 'bfill': 'bfill', 'pad': 'ffill',
            'backfill': 'bfill'}[overload_name]
        nmlga__svejm = dict(limit=limit, downcast=downcast)
        zjkg__vpkwi = dict(limit=None, downcast=None)
        check_unsupported_args(f'Series.{overload_name}', nmlga__svejm,
            zjkg__vpkwi, package_name='pandas', module_name='Series')
        if not (is_overload_none(axis) or is_overload_zero(axis)):
            raise BodoError(
                f'Series.{overload_name}(): axis argument not supported')
        jubnf__wrt = element_type(S.data)
        rsovy__tsbtu = (types.unicode_type, types.bool_, bodo.datetime64ns,
            bodo.timedelta64ns)
        if not isinstance(jubnf__wrt, (types.Integer, types.Float)
            ) and jubnf__wrt not in rsovy__tsbtu:
            raise BodoError(
                f'Series.{overload_name}(): series of type {jubnf__wrt} are not supported.'
                )

        def impl(S, axis=None, inplace=False, limit=None, downcast=None):
            syl__fxss = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            mqtlv__emc = bodo.libs.array_kernels.ffill_bfill_arr(syl__fxss,
                thb__bgd)
            return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                index, name)
        return impl
    return overload_series_fillna_specific_method


fillna_specific_methods = 'ffill', 'bfill', 'pad', 'backfill'


def _install_fillna_specific_methods():
    for overload_name in fillna_specific_methods:
        ytx__yjh = create_fillna_specific_method_overload(overload_name)
        overload_method(SeriesType, overload_name, no_unliteral=True)(ytx__yjh)


_install_fillna_specific_methods()


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        aiozt__iai = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(aiozt__iai)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        aiozt__iai = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(aiozt__iai)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        aiozt__iai = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(aiozt__iai)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    nmlga__svejm = dict(inplace=inplace, limit=limit, regex=regex, method=
        method)
    ryu__dpk = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', nmlga__svejm, ryu__dpk,
        package_name='pandas', module_name='Series')
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.replace()')
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    jubnf__wrt = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        yyu__rlp = element_type(to_replace.key_type)
        bygyn__tybd = element_type(to_replace.value_type)
    else:
        yyu__rlp = element_type(to_replace)
        bygyn__tybd = element_type(value)
    elybt__gxmq = None
    if jubnf__wrt != types.unliteral(yyu__rlp):
        if bodo.utils.typing.equality_always_false(jubnf__wrt, types.
            unliteral(yyu__rlp)
            ) or not bodo.utils.typing.types_equality_exists(jubnf__wrt,
            yyu__rlp):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(jubnf__wrt, (types.Float, types.Integer)
            ) or jubnf__wrt == np.bool_:
            elybt__gxmq = jubnf__wrt
    if not can_replace(jubnf__wrt, types.unliteral(bygyn__tybd)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    vfjv__npf = to_str_arr_if_dict_array(S.data)
    if isinstance(vfjv__npf, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            syl__fxss = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(syl__fxss.
                replace(to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        syl__fxss = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(syl__fxss)
        mqtlv__emc = bodo.utils.utils.alloc_type(n, vfjv__npf, (-1,))
        sue__nmq = build_replace_dict(to_replace, value, elybt__gxmq)
        for uek__gymrr in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(syl__fxss, uek__gymrr):
                bodo.libs.array_kernels.setna(mqtlv__emc, uek__gymrr)
                continue
            s = syl__fxss[uek__gymrr]
            if s in sue__nmq:
                s = sue__nmq[s]
            mqtlv__emc[uek__gymrr] = s
        return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc, index, name)
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    qsp__nvzm = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    clp__qlck = is_iterable_type(to_replace)
    ddl__smmb = isinstance(value, (types.Number, Decimal128Type)) or value in [
        bodo.string_type, bodo.bytes_type, types.boolean]
    kqm__wlxy = is_iterable_type(value)
    if qsp__nvzm and ddl__smmb:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                sue__nmq = {}
                sue__nmq[key_dtype_conv(to_replace)] = value
                return sue__nmq
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            sue__nmq = {}
            sue__nmq[to_replace] = value
            return sue__nmq
        return impl
    if clp__qlck and ddl__smmb:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                sue__nmq = {}
                for gdglg__clpec in to_replace:
                    sue__nmq[key_dtype_conv(gdglg__clpec)] = value
                return sue__nmq
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            sue__nmq = {}
            for gdglg__clpec in to_replace:
                sue__nmq[gdglg__clpec] = value
            return sue__nmq
        return impl
    if clp__qlck and kqm__wlxy:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                sue__nmq = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for uek__gymrr in range(len(to_replace)):
                    sue__nmq[key_dtype_conv(to_replace[uek__gymrr])] = value[
                        uek__gymrr]
                return sue__nmq
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            sue__nmq = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for uek__gymrr in range(len(to_replace)):
                sue__nmq[to_replace[uek__gymrr]] = value[uek__gymrr]
            return sue__nmq
        return impl
    if isinstance(to_replace, numba.types.DictType) and is_overload_none(value
        ):
        return lambda to_replace, value, key_dtype_conv: to_replace
    raise BodoError(
        'Series.replace(): Not supported for types to_replace={} and value={}'
        .format(to_replace, value))


@overload_method(SeriesType, 'diff', inline='always', no_unliteral=True)
def overload_series_diff(S, periods=1):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.diff()')
    if not (isinstance(S.data, types.Array) and (isinstance(S.data.dtype,
        types.Number) or S.data.dtype == bodo.datetime64ns)):
        raise BodoError(
            f'Series.diff() column input type {S.data} not supported.')
    if not is_overload_int(periods):
        raise BodoError("Series.diff(): 'periods' input must be an integer.")
    if S.data == types.Array(bodo.datetime64ns, 1, 'C'):

        def impl_datetime(S, periods=1):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            mqtlv__emc = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo.
                hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                index, name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mqtlv__emc = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc, index, name)
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    nmlga__svejm = dict(ignore_index=ignore_index)
    wsb__fhqv = dict(ignore_index=False)
    check_unsupported_args('Series.explode', nmlga__svejm, wsb__fhqv,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        pptyo__lfqai = bodo.utils.conversion.index_to_array(index)
        mqtlv__emc, vfs__jacqh = bodo.libs.array_kernels.explode(arr,
            pptyo__lfqai)
        kbrnu__dibm = bodo.utils.conversion.index_from_array(vfs__jacqh)
        return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
            kbrnu__dibm, name)
    return impl


@overload(np.digitize, inline='always', no_unliteral=True)
def overload_series_np_digitize(x, bins, right=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'numpy.digitize()')
    if isinstance(x, SeriesType):

        def impl(x, bins, right=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(x)
            return np.digitize(arr, bins, right)
        return impl


@overload(np.argmax, inline='always', no_unliteral=True)
def argmax_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            xelz__jcs = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for uek__gymrr in numba.parfors.parfor.internal_prange(n):
                xelz__jcs[uek__gymrr] = np.argmax(a[uek__gymrr])
            return xelz__jcs
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            jcud__yay = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for uek__gymrr in numba.parfors.parfor.internal_prange(n):
                jcud__yay[uek__gymrr] = np.argmin(a[uek__gymrr])
            return jcud__yay
        return impl


def overload_series_np_dot(a, b, out=None):
    if (isinstance(a, SeriesType) or isinstance(b, SeriesType)
        ) and not is_overload_none(out):
        raise BodoError("np.dot(): 'out' parameter not supported yet")
    if isinstance(a, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(a)
            return np.dot(arr, b)
        return impl
    if isinstance(b, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(b)
            return np.dot(a, arr)
        return impl


overload(np.dot, inline='always', no_unliteral=True)(overload_series_np_dot)
overload(operator.matmul, inline='always', no_unliteral=True)(
    overload_series_np_dot)


@overload_method(SeriesType, 'dropna', inline='always', no_unliteral=True)
def overload_series_dropna(S, axis=0, inplace=False, how=None):
    nmlga__svejm = dict(axis=axis, inplace=inplace, how=how)
    jcxk__griml = dict(axis=0, inplace=False, how=None)
    check_unsupported_args('Series.dropna', nmlga__svejm, jcxk__griml,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.dropna()')
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False, how=None):
            syl__fxss = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            ranwc__kgwdo = S.notna().values
            pptyo__lfqai = bodo.utils.conversion.extract_index_array(S)
            kbrnu__dibm = bodo.utils.conversion.convert_to_index(pptyo__lfqai
                [ranwc__kgwdo])
            mqtlv__emc = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(syl__fxss))
            return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                kbrnu__dibm, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False, how=None):
            syl__fxss = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            pptyo__lfqai = bodo.utils.conversion.extract_index_array(S)
            ranwc__kgwdo = S.notna().values
            kbrnu__dibm = bodo.utils.conversion.convert_to_index(pptyo__lfqai
                [ranwc__kgwdo])
            mqtlv__emc = syl__fxss[ranwc__kgwdo]
            return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                kbrnu__dibm, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    nmlga__svejm = dict(freq=freq, axis=axis, fill_value=fill_value)
    zjkg__vpkwi = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('Series.shift', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.shift()')
    if not is_supported_shift_array_type(S.data):
        raise BodoError(
            f"Series.shift(): Series input type '{S.data.dtype}' not supported yet."
            )
    if not is_overload_int(periods):
        raise BodoError("Series.shift(): 'periods' input must be an integer.")

    def impl(S, periods=1, freq=None, axis=0, fill_value=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mqtlv__emc = bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc, index, name)
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    nmlga__svejm = dict(fill_method=fill_method, limit=limit, freq=freq)
    zjkg__vpkwi = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    if not is_overload_int(periods):
        raise BodoError(
            'Series.pct_change(): periods argument must be an Integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.pct_change()')

    def impl(S, periods=1, fill_method='pad', limit=None, freq=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mqtlv__emc = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc, index, name)
    return impl


def create_series_mask_where_overload(func_name):

    def overload_series_mask_where(S, cond, other=np.nan, inplace=False,
        axis=None, level=None, errors='raise', try_cast=False):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
            f'Series.{func_name}()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
            f'Series.{func_name}()')
        _validate_arguments_mask_where(f'Series.{func_name}', 'Series', S,
            cond, other, inplace, axis, level, errors, try_cast)
        if is_overload_constant_nan(other):
            acimu__beg = 'None'
        else:
            acimu__beg = 'other'
        dct__vba = """def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise',try_cast=False):
"""
        if func_name == 'mask':
            dct__vba += '  cond = ~cond\n'
        dct__vba += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        dct__vba += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        dct__vba += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
        dct__vba += (
            f'  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {acimu__beg})\n'
            )
        dct__vba += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        fertk__qecdz = {}
        exec(dct__vba, {'bodo': bodo, 'np': np}, fertk__qecdz)
        impl = fertk__qecdz['impl']
        return impl
    return overload_series_mask_where


def _install_series_mask_where_overload():
    for func_name in ('mask', 'where'):
        ytx__yjh = create_series_mask_where_overload(func_name)
        overload_method(SeriesType, func_name, no_unliteral=True)(ytx__yjh)


_install_series_mask_where_overload()


def _validate_arguments_mask_where(func_name, module_name, S, cond, other,
    inplace, axis, level, errors, try_cast):
    nmlga__svejm = dict(inplace=inplace, level=level, errors=errors,
        try_cast=try_cast)
    zjkg__vpkwi = dict(inplace=False, level=None, errors='raise', try_cast=
        False)
    check_unsupported_args(f'{func_name}', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name=module_name)
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error(f'{func_name}(): axis argument not supported')
    if isinstance(S, bodo.hiframes.pd_index_ext.RangeIndexType):
        arr = types.Array(types.int64, 1, 'C')
    else:
        arr = S.data
    if isinstance(other, SeriesType):
        _validate_self_other_mask_where(func_name, module_name, arr, other.data
            )
    else:
        _validate_self_other_mask_where(func_name, module_name, arr, other)
    if not (isinstance(cond, (SeriesType, types.Array, BooleanArrayType)) and
        cond.ndim == 1 and cond.dtype == types.bool_):
        raise BodoError(
            f"{func_name}() 'cond' argument must be a Series or 1-dim array of booleans"
            )


def _validate_self_other_mask_where(func_name, module_name, arr, other,
    max_ndim=1, is_default=False):
    if not (isinstance(arr, types.Array) or isinstance(arr,
        BooleanArrayType) or isinstance(arr, IntegerArrayType) or bodo.
        utils.utils.is_array_typ(arr, False) and arr.dtype in [bodo.
        string_type, bodo.bytes_type] or isinstance(arr, bodo.
        CategoricalArrayType) and arr.dtype.elem_type not in [bodo.
        datetime64ns, bodo.timedelta64ns, bodo.pd_timestamp_type, bodo.
        pd_timedelta_type]):
        raise BodoError(
            f'{func_name}() {module_name} data with type {arr} not yet supported'
            )
    ifpx__muky = is_overload_constant_nan(other)
    if not (is_default or ifpx__muky or is_scalar_type(other) or isinstance
        (other, types.Array) and other.ndim >= 1 and other.ndim <= max_ndim or
        isinstance(other, SeriesType) and (isinstance(arr, types.Array) or 
        arr.dtype in [bodo.string_type, bodo.bytes_type]) or 
        is_str_arr_type(other) and (arr.dtype == bodo.string_type or 
        isinstance(arr, bodo.CategoricalArrayType) and arr.dtype.elem_type ==
        bodo.string_type) or isinstance(other, BinaryArrayType) and (arr.
        dtype == bodo.bytes_type or isinstance(arr, bodo.
        CategoricalArrayType) and arr.dtype.elem_type == bodo.bytes_type) or
        (not (isinstance(other, (StringArrayType, BinaryArrayType)) or 
        other == bodo.dict_str_arr_type) and (isinstance(arr.dtype, types.
        Integer) and (bodo.utils.utils.is_array_typ(other) and isinstance(
        other.dtype, types.Integer) or is_series_type(other) and isinstance
        (other.dtype, types.Integer))) or (bodo.utils.utils.is_array_typ(
        other) and arr.dtype == other.dtype or is_series_type(other) and 
        arr.dtype == other.dtype)) and (isinstance(arr, BooleanArrayType) or
        isinstance(arr, IntegerArrayType))):
        raise BodoError(
            f"{func_name}() 'other' must be a scalar, non-categorical series, 1-dim numpy array or StringArray with a matching type for {module_name}."
            )
    if not is_default:
        if isinstance(arr.dtype, bodo.PDCategoricalDtype):
            kmdoa__zvp = arr.dtype.elem_type
        else:
            kmdoa__zvp = arr.dtype
        if is_iterable_type(other):
            dqnha__clqt = other.dtype
        elif ifpx__muky:
            dqnha__clqt = types.float64
        else:
            dqnha__clqt = types.unliteral(other)
        if not ifpx__muky and not is_common_scalar_dtype([kmdoa__zvp,
            dqnha__clqt]):
            raise BodoError(
                f"{func_name}() {module_name.lower()} and 'other' must share a common type."
                )


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        nmlga__svejm = dict(level=level, axis=axis)
        zjkg__vpkwi = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__),
            nmlga__svejm, zjkg__vpkwi, package_name='pandas', module_name=
            'Series')
        vjn__dbru = other == string_type or is_overload_constant_str(other)
        tzabw__qfl = is_iterable_type(other) and other.dtype == string_type
        hucki__ijwg = S.dtype == string_type and (op == operator.add and (
            vjn__dbru or tzabw__qfl) or op == operator.mul and isinstance(
            other, types.Integer))
        fdh__fgvg = S.dtype == bodo.timedelta64ns
        hbjl__gzp = S.dtype == bodo.datetime64ns
        isyu__arwww = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        jnul__wtook = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype == pd_timestamp_type or 
            other.dtype == bodo.datetime64ns)
        lpujd__aav = fdh__fgvg and (isyu__arwww or jnul__wtook
            ) or hbjl__gzp and isyu__arwww
        lpujd__aav = lpujd__aav and op == operator.add
        if not (isinstance(S.dtype, types.Number) or hucki__ijwg or lpujd__aav
            ):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        sxyu__zxabt = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            vfjv__npf = sxyu__zxabt.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and vfjv__npf == types.Array(types.bool_, 1, 'C'):
                vfjv__npf = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_timestamp(other)
                n = len(arr)
                mqtlv__emc = bodo.utils.utils.alloc_type(n, vfjv__npf, (-1,))
                for uek__gymrr in numba.parfors.parfor.internal_prange(n):
                    tpll__rlzu = bodo.libs.array_kernels.isna(arr, uek__gymrr)
                    if tpll__rlzu:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(mqtlv__emc,
                                uek__gymrr)
                        else:
                            mqtlv__emc[uek__gymrr] = op(fill_value, other)
                    else:
                        mqtlv__emc[uek__gymrr] = op(arr[uek__gymrr], other)
                return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        vfjv__npf = sxyu__zxabt.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, IntegerArrayType) and vfjv__npf == types.Array(
            types.bool_, 1, 'C'):
            vfjv__npf = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            oxmkw__eck = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            mqtlv__emc = bodo.utils.utils.alloc_type(n, vfjv__npf, (-1,))
            for uek__gymrr in numba.parfors.parfor.internal_prange(n):
                tpll__rlzu = bodo.libs.array_kernels.isna(arr, uek__gymrr)
                qnoq__oxr = bodo.libs.array_kernels.isna(oxmkw__eck, uek__gymrr
                    )
                if tpll__rlzu and qnoq__oxr:
                    bodo.libs.array_kernels.setna(mqtlv__emc, uek__gymrr)
                elif tpll__rlzu:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(mqtlv__emc, uek__gymrr)
                    else:
                        mqtlv__emc[uek__gymrr] = op(fill_value, oxmkw__eck[
                            uek__gymrr])
                elif qnoq__oxr:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(mqtlv__emc, uek__gymrr)
                    else:
                        mqtlv__emc[uek__gymrr] = op(arr[uek__gymrr], fill_value
                            )
                else:
                    mqtlv__emc[uek__gymrr] = op(arr[uek__gymrr], oxmkw__eck
                        [uek__gymrr])
            return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                index, name)
        return impl
    return overload_series_explicit_binary_op


def create_explicit_binary_reverse_op_overload(op):

    def overload_series_explicit_binary_reverse_op(S, other, level=None,
        fill_value=None, axis=0):
        if not is_overload_none(level):
            raise BodoError('level argument not supported')
        if not is_overload_zero(axis):
            raise BodoError('axis argument not supported')
        if not isinstance(S.dtype, types.Number):
            raise BodoError('only numeric values supported')
        sxyu__zxabt = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            vfjv__npf = sxyu__zxabt.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and vfjv__npf == types.Array(types.bool_, 1, 'C'):
                vfjv__npf = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                mqtlv__emc = bodo.utils.utils.alloc_type(n, vfjv__npf, None)
                for uek__gymrr in numba.parfors.parfor.internal_prange(n):
                    tpll__rlzu = bodo.libs.array_kernels.isna(arr, uek__gymrr)
                    if tpll__rlzu:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(mqtlv__emc,
                                uek__gymrr)
                        else:
                            mqtlv__emc[uek__gymrr] = op(other, fill_value)
                    else:
                        mqtlv__emc[uek__gymrr] = op(other, arr[uek__gymrr])
                return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        vfjv__npf = sxyu__zxabt.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, IntegerArrayType) and vfjv__npf == types.Array(
            types.bool_, 1, 'C'):
            vfjv__npf = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            oxmkw__eck = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            mqtlv__emc = bodo.utils.utils.alloc_type(n, vfjv__npf, None)
            for uek__gymrr in numba.parfors.parfor.internal_prange(n):
                tpll__rlzu = bodo.libs.array_kernels.isna(arr, uek__gymrr)
                qnoq__oxr = bodo.libs.array_kernels.isna(oxmkw__eck, uek__gymrr
                    )
                mqtlv__emc[uek__gymrr] = op(oxmkw__eck[uek__gymrr], arr[
                    uek__gymrr])
                if tpll__rlzu and qnoq__oxr:
                    bodo.libs.array_kernels.setna(mqtlv__emc, uek__gymrr)
                elif tpll__rlzu:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(mqtlv__emc, uek__gymrr)
                    else:
                        mqtlv__emc[uek__gymrr] = op(oxmkw__eck[uek__gymrr],
                            fill_value)
                elif qnoq__oxr:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(mqtlv__emc, uek__gymrr)
                    else:
                        mqtlv__emc[uek__gymrr] = op(fill_value, arr[uek__gymrr]
                            )
                else:
                    mqtlv__emc[uek__gymrr] = op(oxmkw__eck[uek__gymrr], arr
                        [uek__gymrr])
            return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                index, name)
        return impl
    return overload_series_explicit_binary_reverse_op


explicit_binop_funcs_two_ways = {operator.add: {'add'}, operator.sub: {
    'sub'}, operator.mul: {'mul'}, operator.truediv: {'div', 'truediv'},
    operator.floordiv: {'floordiv'}, operator.mod: {'mod'}, operator.pow: {
    'pow'}}
explicit_binop_funcs_single = {operator.lt: 'lt', operator.gt: 'gt',
    operator.le: 'le', operator.ge: 'ge', operator.ne: 'ne', operator.eq: 'eq'}
explicit_binop_funcs = set()
split_logical_binops_funcs = [operator.or_, operator.and_]


def _install_explicit_binary_ops():
    for op, sxc__zcmt in explicit_binop_funcs_two_ways.items():
        for name in sxc__zcmt:
            ytx__yjh = create_explicit_binary_op_overload(op)
            far__fjcsf = create_explicit_binary_reverse_op_overload(op)
            axyxa__shm = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(ytx__yjh)
            overload_method(SeriesType, axyxa__shm, no_unliteral=True)(
                far__fjcsf)
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        ytx__yjh = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(ytx__yjh)
        explicit_binop_funcs.add(name)


_install_explicit_binary_ops()


def create_binary_op_overload(op):

    def overload_series_binary_op(lhs, rhs):
        if (isinstance(lhs, SeriesType) and isinstance(rhs, SeriesType) and
            lhs.dtype == bodo.datetime64ns and rhs.dtype == bodo.
            datetime64ns and op == operator.sub):

            def impl_dt64(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                xyb__nelne = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                mqtlv__emc = dt64_arr_sub(arr, xyb__nelne)
                return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                    index, name)
            return impl_dt64
        if op in [operator.add, operator.sub] and isinstance(lhs, SeriesType
            ) and lhs.dtype == bodo.datetime64ns and is_offsets_type(rhs):

            def impl_offsets(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                mqtlv__emc = np.empty(n, np.dtype('datetime64[ns]'))
                for uek__gymrr in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, uek__gymrr):
                        bodo.libs.array_kernels.setna(mqtlv__emc, uek__gymrr)
                        continue
                    dpla__xlxpv = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[uek__gymrr]))
                    djcdi__azo = op(dpla__xlxpv, rhs)
                    mqtlv__emc[uek__gymrr
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        djcdi__azo.value)
                return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                    index, name)
            return impl_offsets
        if op == operator.add and is_offsets_type(lhs) and isinstance(rhs,
            SeriesType) and rhs.dtype == bodo.datetime64ns:

            def impl(lhs, rhs):
                return op(rhs, lhs)
            return impl
        if isinstance(lhs, SeriesType):
            if lhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                    xyb__nelne = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    mqtlv__emc = op(arr, bodo.utils.conversion.
                        unbox_if_timestamp(xyb__nelne))
                    return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                xyb__nelne = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                mqtlv__emc = op(arr, xyb__nelne)
                return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    qfeab__lpsis = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    mqtlv__emc = op(bodo.utils.conversion.
                        unbox_if_timestamp(qfeab__lpsis), arr)
                    return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                qfeab__lpsis = (bodo.utils.conversion.
                    get_array_if_series_or_index(lhs))
                mqtlv__emc = op(qfeab__lpsis, arr)
                return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        ytx__yjh = create_binary_op_overload(op)
        overload(op)(ytx__yjh)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    lgbb__jrhfa = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, lgbb__jrhfa)
        for uek__gymrr in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, uek__gymrr
                ) or bodo.libs.array_kernels.isna(arg2, uek__gymrr):
                bodo.libs.array_kernels.setna(S, uek__gymrr)
                continue
            S[uek__gymrr
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                uek__gymrr]) - bodo.hiframes.pd_timestamp_ext.
                dt64_to_integer(arg2[uek__gymrr]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                oxmkw__eck = (bodo.utils.conversion.
                    get_array_if_series_or_index(other))
                op(arr, oxmkw__eck)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        ytx__yjh = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(ytx__yjh)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                mqtlv__emc = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        ytx__yjh = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(ytx__yjh)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    mqtlv__emc = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                        index, name)
                return impl
        return overload_series_ufunc_nin_1
    elif ufunc.nin == 2:

        def overload_series_ufunc_nin_2(S1, S2):
            if isinstance(S1, SeriesType):

                def impl(S1, S2):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S1)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S1)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S1)
                    oxmkw__eck = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    mqtlv__emc = ufunc(arr, oxmkw__eck)
                    return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                        index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    oxmkw__eck = bodo.hiframes.pd_series_ext.get_series_data(S2
                        )
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    mqtlv__emc = ufunc(arr, oxmkw__eck)
                    return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                        index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        ytx__yjh = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(ytx__yjh)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        gcpu__ewssa = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.
            copy(),))
        dtgcp__ctr = np.arange(n),
        bodo.libs.timsort.sort(gcpu__ewssa, 0, n, dtgcp__ctr)
        return dtgcp__ctr[0]
    return impl


@overload(pd.to_numeric, inline='always', no_unliteral=True)
def overload_to_numeric(arg_a, errors='raise', downcast=None):
    if not is_overload_none(downcast) and not (is_overload_constant_str(
        downcast) and get_overload_const_str(downcast) in ('integer',
        'signed', 'unsigned', 'float')):
        raise BodoError(
            'pd.to_numeric(): invalid downcasting method provided {}'.
            format(downcast))
    out_dtype = types.float64
    if not is_overload_none(downcast):
        pld__uytk = get_overload_const_str(downcast)
        if pld__uytk in ('integer', 'signed'):
            out_dtype = types.int64
        elif pld__uytk == 'unsigned':
            out_dtype = types.uint64
        else:
            assert pld__uytk == 'float'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arg_a,
        'pandas.to_numeric()')
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            syl__fxss = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            mqtlv__emc = pd.to_numeric(syl__fxss, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                index, name)
        return impl_series
    if not is_str_arr_type(arg_a):
        raise BodoError(f'pd.to_numeric(): invalid argument type {arg_a}')
    if out_dtype == types.float64:

        def to_numeric_float_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            iye__iwj = np.empty(n, np.float64)
            for uek__gymrr in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, uek__gymrr):
                    bodo.libs.array_kernels.setna(iye__iwj, uek__gymrr)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(iye__iwj,
                        uek__gymrr, arg_a, uek__gymrr)
            return iye__iwj
        return to_numeric_float_impl
    else:

        def to_numeric_int_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            iye__iwj = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)
            for uek__gymrr in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, uek__gymrr):
                    bodo.libs.array_kernels.setna(iye__iwj, uek__gymrr)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(iye__iwj,
                        uek__gymrr, arg_a, uek__gymrr)
            return iye__iwj
        return to_numeric_int_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        sdp__oqdz = if_series_to_array_type(args[0])
        if isinstance(sdp__oqdz, types.Array) and isinstance(sdp__oqdz.
            dtype, types.Integer):
            sdp__oqdz = types.Array(types.float64, 1, 'C')
        return sdp__oqdz(*args)


def where_impl_one_arg(c):
    return np.where(c)


@overload(where_impl_one_arg, no_unliteral=True)
def overload_where_unsupported_one_arg(condition):
    if isinstance(condition, SeriesType) or bodo.utils.utils.is_array_typ(
        condition, False):
        return lambda condition: np.where(condition)


def overload_np_where_one_arg(condition):
    if isinstance(condition, SeriesType):

        def impl_series(condition):
            condition = bodo.hiframes.pd_series_ext.get_series_data(condition)
            return bodo.libs.array_kernels.nonzero(condition)
        return impl_series
    elif bodo.utils.utils.is_array_typ(condition, False):

        def impl(condition):
            return bodo.libs.array_kernels.nonzero(condition)
        return impl


overload(np.where, inline='always', no_unliteral=True)(
    overload_np_where_one_arg)
overload(where_impl_one_arg, inline='always', no_unliteral=True)(
    overload_np_where_one_arg)


def where_impl(c, x, y):
    return np.where(c, x, y)


@overload(where_impl, no_unliteral=True)
def overload_where_unsupported(condition, x, y):
    if not isinstance(condition, (SeriesType, types.Array, BooleanArrayType)
        ) or condition.ndim != 1:
        return lambda condition, x, y: np.where(condition, x, y)


@overload(where_impl, no_unliteral=True)
@overload(np.where, no_unliteral=True)
def overload_np_where(condition, x, y):
    if not isinstance(condition, (SeriesType, types.Array, BooleanArrayType)
        ) or condition.ndim != 1:
        return
    assert condition.dtype == types.bool_, 'invalid condition dtype'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'numpy.where()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(y,
        'numpy.where()')
    xkwb__nac = bodo.utils.utils.is_array_typ(x, True)
    jhjq__ruk = bodo.utils.utils.is_array_typ(y, True)
    dct__vba = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        dct__vba += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if xkwb__nac and not bodo.utils.utils.is_array_typ(x, False):
        dct__vba += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if jhjq__ruk and not bodo.utils.utils.is_array_typ(y, False):
        dct__vba += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    dct__vba += '  n = len(condition)\n'
    gsbdi__tewsd = x.dtype if xkwb__nac else types.unliteral(x)
    tvxmx__sknw = y.dtype if jhjq__ruk else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        gsbdi__tewsd = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        tvxmx__sknw = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    axt__cgrk = get_data(x)
    dpyh__zvjsa = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(dtgcp__ctr) for
        dtgcp__ctr in [axt__cgrk, dpyh__zvjsa])
    if dpyh__zvjsa == types.none:
        if isinstance(gsbdi__tewsd, types.Number):
            out_dtype = types.Array(types.float64, 1, 'C')
        else:
            out_dtype = to_nullable_type(x)
    elif axt__cgrk == dpyh__zvjsa and not is_nullable:
        out_dtype = dtype_to_array_type(gsbdi__tewsd)
    elif gsbdi__tewsd == string_type or tvxmx__sknw == string_type:
        out_dtype = bodo.string_array_type
    elif axt__cgrk == bytes_type or (xkwb__nac and gsbdi__tewsd == bytes_type
        ) and (dpyh__zvjsa == bytes_type or jhjq__ruk and tvxmx__sknw ==
        bytes_type):
        out_dtype = binary_array_type
    elif isinstance(gsbdi__tewsd, bodo.PDCategoricalDtype):
        out_dtype = None
    elif gsbdi__tewsd in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(gsbdi__tewsd, 1, 'C')
    elif tvxmx__sknw in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(tvxmx__sknw, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(gsbdi__tewsd), numba.np.numpy_support.
            as_dtype(tvxmx__sknw)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(gsbdi__tewsd, bodo.PDCategoricalDtype):
        cmrax__izb = 'x'
    else:
        cmrax__izb = 'out_dtype'
    dct__vba += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {cmrax__izb}, (-1,))\n')
    if isinstance(gsbdi__tewsd, bodo.PDCategoricalDtype):
        dct__vba += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        dct__vba += (
            '  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)\n'
            )
    dct__vba += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    dct__vba += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if xkwb__nac:
        dct__vba += '      if bodo.libs.array_kernels.isna(x, j):\n'
        dct__vba += '        setna(out_arr, j)\n'
        dct__vba += '        continue\n'
    if isinstance(gsbdi__tewsd, bodo.PDCategoricalDtype):
        dct__vba += '      out_codes[j] = x_codes[j]\n'
    else:
        dct__vba += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('x[j]' if xkwb__nac else 'x'))
    dct__vba += '    else:\n'
    if jhjq__ruk:
        dct__vba += '      if bodo.libs.array_kernels.isna(y, j):\n'
        dct__vba += '        setna(out_arr, j)\n'
        dct__vba += '        continue\n'
    if dpyh__zvjsa == types.none:
        if isinstance(gsbdi__tewsd, bodo.PDCategoricalDtype):
            dct__vba += '      out_codes[j] = -1\n'
        else:
            dct__vba += '      setna(out_arr, j)\n'
    else:
        dct__vba += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('y[j]' if jhjq__ruk else 'y'))
    dct__vba += '  return out_arr\n'
    fertk__qecdz = {}
    exec(dct__vba, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, fertk__qecdz)
    kylv__vnci = fertk__qecdz['_impl']
    return kylv__vnci


def _verify_np_select_arg_typs(condlist, choicelist, default):
    if isinstance(condlist, (types.List, types.UniTuple)):
        if not (bodo.utils.utils.is_np_array_typ(condlist.dtype) and 
            condlist.dtype.dtype == types.bool_):
            raise BodoError(
                "np.select(): 'condlist' argument must be list or tuple of boolean ndarrays. If passing a Series, please convert with pd.Series.to_numpy()."
                )
    else:
        raise BodoError(
            "np.select(): 'condlist' argument must be list or tuple of boolean ndarrays. If passing a Series, please convert with pd.Series.to_numpy()."
            )
    if not isinstance(choicelist, (types.List, types.UniTuple, types.BaseTuple)
        ):
        raise BodoError(
            "np.select(): 'choicelist' argument must be list or tuple type")
    if isinstance(choicelist, (types.List, types.UniTuple)):
        wjbir__rcjk = choicelist.dtype
        if not bodo.utils.utils.is_array_typ(wjbir__rcjk, True):
            raise BodoError(
                "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                )
        if is_series_type(wjbir__rcjk):
            fuyev__lzja = wjbir__rcjk.data.dtype
        else:
            fuyev__lzja = wjbir__rcjk.dtype
        if isinstance(fuyev__lzja, bodo.PDCategoricalDtype):
            raise BodoError(
                'np.select(): data with choicelist of type Categorical not yet supported'
                )
        mflco__mxl = wjbir__rcjk
    else:
        duc__gudoi = []
        for wjbir__rcjk in choicelist:
            if not bodo.utils.utils.is_array_typ(wjbir__rcjk, True):
                raise BodoError(
                    "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                    )
            if is_series_type(wjbir__rcjk):
                fuyev__lzja = wjbir__rcjk.data.dtype
            else:
                fuyev__lzja = wjbir__rcjk.dtype
            if isinstance(fuyev__lzja, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            duc__gudoi.append(fuyev__lzja)
        if not is_common_scalar_dtype(duc__gudoi):
            raise BodoError(
                f"np.select(): 'choicelist' items must be arrays with a commmon data type. Found a tuple with the following data types {choicelist}."
                )
        mflco__mxl = choicelist[0]
    if is_series_type(mflco__mxl):
        mflco__mxl = mflco__mxl.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pass
    else:
        if not is_scalar_type(default):
            raise BodoError(
                "np.select(): 'default' argument must be scalar type")
        if not (is_common_scalar_dtype([default, mflco__mxl.dtype]) or 
            default == types.none or is_overload_constant_nan(default)):
            raise BodoError(
                f"np.select(): 'default' is not type compatible with the array types in choicelist. Choicelist type: {choicelist}, Default type: {default}"
                )
    if not (isinstance(mflco__mxl, types.Array) or isinstance(mflco__mxl,
        BooleanArrayType) or isinstance(mflco__mxl, IntegerArrayType) or 
        bodo.utils.utils.is_array_typ(mflco__mxl, False) and mflco__mxl.
        dtype in [bodo.string_type, bodo.bytes_type]):
        raise BodoError(
            f'np.select(): data with choicelist of type {mflco__mxl} not yet supported'
            )


@overload(np.select)
def overload_np_select(condlist, choicelist, default=0):
    _verify_np_select_arg_typs(condlist, choicelist, default)
    kwgb__bax = isinstance(choicelist, (types.List, types.UniTuple)
        ) and isinstance(condlist, (types.List, types.UniTuple))
    if isinstance(choicelist, (types.List, types.UniTuple)):
        mdbbp__koyg = choicelist.dtype
    else:
        keeo__wtj = False
        duc__gudoi = []
        for wjbir__rcjk in choicelist:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                wjbir__rcjk, 'numpy.select()')
            if is_nullable_type(wjbir__rcjk):
                keeo__wtj = True
            if is_series_type(wjbir__rcjk):
                fuyev__lzja = wjbir__rcjk.data.dtype
            else:
                fuyev__lzja = wjbir__rcjk.dtype
            if isinstance(fuyev__lzja, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            duc__gudoi.append(fuyev__lzja)
        vssut__enamf, smb__vbpgc = get_common_scalar_dtype(duc__gudoi)
        if not smb__vbpgc:
            raise BodoError('Internal error in overload_np_select')
        otg__ucbge = dtype_to_array_type(vssut__enamf)
        if keeo__wtj:
            otg__ucbge = to_nullable_type(otg__ucbge)
        mdbbp__koyg = otg__ucbge
    if isinstance(mdbbp__koyg, SeriesType):
        mdbbp__koyg = mdbbp__koyg.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        egm__uydx = True
    else:
        egm__uydx = False
    ite__ueedx = False
    jcj__sgdi = False
    if egm__uydx:
        if isinstance(mdbbp__koyg.dtype, types.Number):
            pass
        elif mdbbp__koyg.dtype == types.bool_:
            jcj__sgdi = True
        else:
            ite__ueedx = True
            mdbbp__koyg = to_nullable_type(mdbbp__koyg)
    elif default == types.none or is_overload_constant_nan(default):
        ite__ueedx = True
        mdbbp__koyg = to_nullable_type(mdbbp__koyg)
    dct__vba = 'def np_select_impl(condlist, choicelist, default=0):\n'
    dct__vba += '  if len(condlist) != len(choicelist):\n'
    dct__vba += (
        "    raise ValueError('list of cases must be same length as list of conditions')\n"
        )
    dct__vba += '  output_len = len(choicelist[0])\n'
    dct__vba += (
        '  out = bodo.utils.utils.alloc_type(output_len, alloc_typ, (-1,))\n')
    dct__vba += '  for i in range(output_len):\n'
    if ite__ueedx:
        dct__vba += '    bodo.libs.array_kernels.setna(out, i)\n'
    elif jcj__sgdi:
        dct__vba += '    out[i] = False\n'
    else:
        dct__vba += '    out[i] = default\n'
    if kwgb__bax:
        dct__vba += '  for i in range(len(condlist) - 1, -1, -1):\n'
        dct__vba += '    cond = condlist[i]\n'
        dct__vba += '    choice = choicelist[i]\n'
        dct__vba += '    out = np.where(cond, choice, out)\n'
    else:
        for uek__gymrr in range(len(choicelist) - 1, -1, -1):
            dct__vba += f'  cond = condlist[{uek__gymrr}]\n'
            dct__vba += f'  choice = choicelist[{uek__gymrr}]\n'
            dct__vba += f'  out = np.where(cond, choice, out)\n'
    dct__vba += '  return out'
    fertk__qecdz = dict()
    exec(dct__vba, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'alloc_typ': mdbbp__koyg}, fertk__qecdz)
    impl = fertk__qecdz['np_select_impl']
    return impl


@overload_method(SeriesType, 'duplicated', inline='always', no_unliteral=True)
def overload_series_duplicated(S, keep='first'):

    def impl(S, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mqtlv__emc = bodo.libs.array_kernels.duplicated((arr,))
        return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc, index, name)
    return impl


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    nmlga__svejm = dict(subset=subset, keep=keep, inplace=inplace)
    zjkg__vpkwi = dict(subset=None, keep='first', inplace=False)
    check_unsupported_args('Series.drop_duplicates', nmlga__svejm,
        zjkg__vpkwi, package_name='pandas', module_name='Series')

    def impl(S, subset=None, keep='first', inplace=False):
        mtmie__xmv = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (mtmie__xmv,), pptyo__lfqai = bodo.libs.array_kernels.drop_duplicates((
            mtmie__xmv,), index, 1)
        index = bodo.utils.conversion.index_from_array(pptyo__lfqai)
        return bodo.hiframes.pd_series_ext.init_series(mtmie__xmv, index, name)
    return impl


@overload_method(SeriesType, 'between', inline='always', no_unliteral=True)
def overload_series_between(S, left, right, inclusive='both'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(left,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(right,
        'Series.between()')
    rjdy__bzc = element_type(S.data)
    if not is_common_scalar_dtype([rjdy__bzc, left]):
        raise_bodo_error(
            "Series.between(): 'left' must be compariable with the Series data"
            )
    if not is_common_scalar_dtype([rjdy__bzc, right]):
        raise_bodo_error(
            "Series.between(): 'right' must be compariable with the Series data"
            )
    if not is_overload_constant_str(inclusive) or get_overload_const_str(
        inclusive) not in ('both', 'neither'):
        raise_bodo_error(
            "Series.between(): 'inclusive' must be a constant string and one of ('both', 'neither')"
            )

    def impl(S, left, right, inclusive='both'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(arr)
        mqtlv__emc = np.empty(n, np.bool_)
        for uek__gymrr in numba.parfors.parfor.internal_prange(n):
            yekp__crft = bodo.utils.conversion.box_if_dt64(arr[uek__gymrr])
            if inclusive == 'both':
                mqtlv__emc[uek__gymrr
                    ] = yekp__crft <= right and yekp__crft >= left
            else:
                mqtlv__emc[uek__gymrr
                    ] = yekp__crft < right and yekp__crft > left
        return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc, index, name)
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    nmlga__svejm = dict(axis=axis)
    zjkg__vpkwi = dict(axis=None)
    check_unsupported_args('Series.repeat', nmlga__svejm, zjkg__vpkwi,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.repeat()')
    if not (isinstance(repeats, types.Integer) or is_iterable_type(repeats) and
        isinstance(repeats.dtype, types.Integer)):
        raise BodoError(
            "Series.repeat(): 'repeats' should be an integer or array of integers"
            )
    if isinstance(repeats, types.Integer):

        def impl_int(S, repeats, axis=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            pptyo__lfqai = bodo.utils.conversion.index_to_array(index)
            mqtlv__emc = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            vfs__jacqh = bodo.libs.array_kernels.repeat_kernel(pptyo__lfqai,
                repeats)
            kbrnu__dibm = bodo.utils.conversion.index_from_array(vfs__jacqh)
            return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
                kbrnu__dibm, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        pptyo__lfqai = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        mqtlv__emc = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        vfs__jacqh = bodo.libs.array_kernels.repeat_kernel(pptyo__lfqai,
            repeats)
        kbrnu__dibm = bodo.utils.conversion.index_from_array(vfs__jacqh)
        return bodo.hiframes.pd_series_ext.init_series(mqtlv__emc,
            kbrnu__dibm, name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        dtgcp__ctr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(dtgcp__ctr)
        sulvd__lzey = {}
        for uek__gymrr in range(n):
            yekp__crft = bodo.utils.conversion.box_if_dt64(dtgcp__ctr[
                uek__gymrr])
            sulvd__lzey[index[uek__gymrr]] = yekp__crft
        return sulvd__lzey
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    jzggc__trcla = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            gbw__nyfsh = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(jzggc__trcla)
    elif is_literal_type(name):
        gbw__nyfsh = get_literal_value(name)
    else:
        raise_bodo_error(jzggc__trcla)
    gbw__nyfsh = 0 if gbw__nyfsh is None else gbw__nyfsh
    yjzmc__jci = ColNamesMetaType((gbw__nyfsh,))

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            yjzmc__jci)
    return impl


@overload_method(SeriesType, 'keys', inline='always', no_unliteral=True)
def overload_series_keys(S):

    def impl(S):
        return bodo.hiframes.pd_series_ext.get_series_index(S)
    return impl
