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
            gduce__bqh = bodo.hiframes.pd_series_ext.get_series_data(s)
            shvsw__qaqf = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                gduce__bqh)
            return shvsw__qaqf
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
            kzbk__fptah = list()
            for muw__dug in range(len(S)):
                kzbk__fptah.append(S.iat[muw__dug])
            return kzbk__fptah
        return impl_float

    def impl(S):
        kzbk__fptah = list()
        for muw__dug in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, muw__dug):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            kzbk__fptah.append(S.iat[muw__dug])
        return kzbk__fptah
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    jsha__lkjoa = dict(dtype=dtype, copy=copy, na_value=na_value)
    kyar__oicjx = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', jsha__lkjoa, kyar__oicjx,
        package_name='pandas', module_name='Series')

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    jsha__lkjoa = dict(name=name, inplace=inplace)
    kyar__oicjx = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', jsha__lkjoa, kyar__oicjx,
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
        zde__xzs = ', '.join(['index_arrs[{}]'.format(muw__dug) for
            muw__dug in range(S.index.nlevels)])
    else:
        zde__xzs = '    bodo.utils.conversion.index_to_array(index)\n'
    lar__ksmr = 'index' if 'index' != series_name else 'level_0'
    ygd__aihz = get_index_names(S.index, 'Series.reset_index()', lar__ksmr)
    columns = [name for name in ygd__aihz]
    columns.append(series_name)
    bjif__ckcn = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    bjif__ckcn += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    bjif__ckcn += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    if isinstance(S.index, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        bjif__ckcn += (
            '    index_arrs = bodo.hiframes.pd_index_ext.get_index_data(index)\n'
            )
    bjif__ckcn += """    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)
"""
    bjif__ckcn += f"""    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({zde__xzs}, arr), df_index, __col_name_meta_value_series_reset_index)
"""
    lyyah__edntv = {}
    exec(bjif__ckcn, {'bodo': bodo,
        '__col_name_meta_value_series_reset_index': ColNamesMetaType(tuple(
        columns))}, lyyah__edntv)
    xctbc__cypm = lyyah__edntv['_impl']
    return xctbc__cypm


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        hbeqo__fbr = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr, index, name)
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
        hbeqo__fbr = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for muw__dug in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[muw__dug]):
                bodo.libs.array_kernels.setna(hbeqo__fbr, muw__dug)
            else:
                hbeqo__fbr[muw__dug] = np.round(arr[muw__dug], decimals)
        return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr, index, name)
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    jsha__lkjoa = dict(level=level, numeric_only=numeric_only)
    kyar__oicjx = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', jsha__lkjoa, kyar__oicjx,
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
    jsha__lkjoa = dict(level=level, numeric_only=numeric_only)
    kyar__oicjx = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', jsha__lkjoa, kyar__oicjx,
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
    jsha__lkjoa = dict(axis=axis, bool_only=bool_only, skipna=skipna, level
        =level)
    kyar__oicjx = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', jsha__lkjoa, kyar__oicjx,
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
        aiblf__hat = bodo.hiframes.pd_series_ext.get_series_data(S)
        dbbqs__wsl = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        guw__fjjct = 0
        for muw__dug in numba.parfors.parfor.internal_prange(len(aiblf__hat)):
            ied__xbla = 0
            omy__jggr = bodo.libs.array_kernels.isna(aiblf__hat, muw__dug)
            enim__jvg = bodo.libs.array_kernels.isna(dbbqs__wsl, muw__dug)
            if omy__jggr and not enim__jvg or not omy__jggr and enim__jvg:
                ied__xbla = 1
            elif not omy__jggr:
                if aiblf__hat[muw__dug] != dbbqs__wsl[muw__dug]:
                    ied__xbla = 1
            guw__fjjct += ied__xbla
        return guw__fjjct == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    jsha__lkjoa = dict(axis=axis, bool_only=bool_only, skipna=skipna, level
        =level)
    kyar__oicjx = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', jsha__lkjoa, kyar__oicjx,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.all()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_all(A)
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    jsha__lkjoa = dict(level=level)
    kyar__oicjx = dict(level=None)
    check_unsupported_args('Series.mad', jsha__lkjoa, kyar__oicjx,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(skipna):
        raise BodoError("Series.mad(): 'skipna' argument must be a boolean")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mad(): axis argument not supported')
    qrpum__hwjyo = types.float64
    boe__qff = types.float64
    if S.dtype == types.float32:
        qrpum__hwjyo = types.float32
        boe__qff = types.float32
    fvpj__elck = qrpum__hwjyo(0)
    kgp__eoak = boe__qff(0)
    yauqy__ifyd = boe__qff(1)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.mad()'
        )

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        ityi__jinf = fvpj__elck
        guw__fjjct = kgp__eoak
        for muw__dug in numba.parfors.parfor.internal_prange(len(A)):
            ied__xbla = fvpj__elck
            xqin__btkyq = kgp__eoak
            if not bodo.libs.array_kernels.isna(A, muw__dug) or not skipna:
                ied__xbla = A[muw__dug]
                xqin__btkyq = yauqy__ifyd
            ityi__jinf += ied__xbla
            guw__fjjct += xqin__btkyq
        qyns__ycp = bodo.hiframes.series_kernels._mean_handle_nan(ityi__jinf,
            guw__fjjct)
        mlsoz__kxfk = fvpj__elck
        for muw__dug in numba.parfors.parfor.internal_prange(len(A)):
            ied__xbla = fvpj__elck
            if not bodo.libs.array_kernels.isna(A, muw__dug) or not skipna:
                ied__xbla = abs(A[muw__dug] - qyns__ycp)
            mlsoz__kxfk += ied__xbla
        gvgt__oaiqa = bodo.hiframes.series_kernels._mean_handle_nan(mlsoz__kxfk
            , guw__fjjct)
        return gvgt__oaiqa
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    jsha__lkjoa = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    kyar__oicjx = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', jsha__lkjoa, kyar__oicjx,
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
    jsha__lkjoa = dict(level=level, numeric_only=numeric_only)
    kyar__oicjx = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', jsha__lkjoa, kyar__oicjx,
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
        jidn__jxvr = 0
        wegia__tqqky = 0
        guw__fjjct = 0
        for muw__dug in numba.parfors.parfor.internal_prange(len(A)):
            ied__xbla = 0
            xqin__btkyq = 0
            if not bodo.libs.array_kernels.isna(A, muw__dug) or not skipna:
                ied__xbla = A[muw__dug]
                xqin__btkyq = 1
            jidn__jxvr += ied__xbla
            wegia__tqqky += ied__xbla * ied__xbla
            guw__fjjct += xqin__btkyq
        bhk__okfh = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            jidn__jxvr, wegia__tqqky, guw__fjjct, ddof)
        bvt__ils = bodo.hiframes.series_kernels._sem_handle_nan(bhk__okfh,
            guw__fjjct)
        return bvt__ils
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    jsha__lkjoa = dict(level=level, numeric_only=numeric_only)
    kyar__oicjx = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', jsha__lkjoa, kyar__oicjx,
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
        jidn__jxvr = 0.0
        wegia__tqqky = 0.0
        tcou__esu = 0.0
        tsgcr__blpl = 0.0
        guw__fjjct = 0
        for muw__dug in numba.parfors.parfor.internal_prange(len(A)):
            ied__xbla = 0.0
            xqin__btkyq = 0
            if not bodo.libs.array_kernels.isna(A, muw__dug) or not skipna:
                ied__xbla = np.float64(A[muw__dug])
                xqin__btkyq = 1
            jidn__jxvr += ied__xbla
            wegia__tqqky += ied__xbla ** 2
            tcou__esu += ied__xbla ** 3
            tsgcr__blpl += ied__xbla ** 4
            guw__fjjct += xqin__btkyq
        bhk__okfh = bodo.hiframes.series_kernels.compute_kurt(jidn__jxvr,
            wegia__tqqky, tcou__esu, tsgcr__blpl, guw__fjjct)
        return bhk__okfh
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    jsha__lkjoa = dict(level=level, numeric_only=numeric_only)
    kyar__oicjx = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', jsha__lkjoa, kyar__oicjx,
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
        jidn__jxvr = 0.0
        wegia__tqqky = 0.0
        tcou__esu = 0.0
        guw__fjjct = 0
        for muw__dug in numba.parfors.parfor.internal_prange(len(A)):
            ied__xbla = 0.0
            xqin__btkyq = 0
            if not bodo.libs.array_kernels.isna(A, muw__dug) or not skipna:
                ied__xbla = np.float64(A[muw__dug])
                xqin__btkyq = 1
            jidn__jxvr += ied__xbla
            wegia__tqqky += ied__xbla ** 2
            tcou__esu += ied__xbla ** 3
            guw__fjjct += xqin__btkyq
        bhk__okfh = bodo.hiframes.series_kernels.compute_skew(jidn__jxvr,
            wegia__tqqky, tcou__esu, guw__fjjct)
        return bhk__okfh
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    jsha__lkjoa = dict(level=level, numeric_only=numeric_only)
    kyar__oicjx = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', jsha__lkjoa, kyar__oicjx,
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
    jsha__lkjoa = dict(level=level, numeric_only=numeric_only)
    kyar__oicjx = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', jsha__lkjoa, kyar__oicjx,
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
        aiblf__hat = bodo.hiframes.pd_series_ext.get_series_data(S)
        dbbqs__wsl = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        rykw__err = 0
        for muw__dug in numba.parfors.parfor.internal_prange(len(aiblf__hat)):
            nutwh__amj = aiblf__hat[muw__dug]
            olyrq__fdlib = dbbqs__wsl[muw__dug]
            rykw__err += nutwh__amj * olyrq__fdlib
        return rykw__err
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=None, skipna=True):
    jsha__lkjoa = dict(skipna=skipna)
    kyar__oicjx = dict(skipna=True)
    check_unsupported_args('Series.cumsum', jsha__lkjoa, kyar__oicjx,
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
    jsha__lkjoa = dict(skipna=skipna)
    kyar__oicjx = dict(skipna=True)
    check_unsupported_args('Series.cumprod', jsha__lkjoa, kyar__oicjx,
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
    jsha__lkjoa = dict(skipna=skipna)
    kyar__oicjx = dict(skipna=True)
    check_unsupported_args('Series.cummin', jsha__lkjoa, kyar__oicjx,
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
    jsha__lkjoa = dict(skipna=skipna)
    kyar__oicjx = dict(skipna=True)
    check_unsupported_args('Series.cummax', jsha__lkjoa, kyar__oicjx,
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
    jsha__lkjoa = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    kyar__oicjx = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', jsha__lkjoa, kyar__oicjx,
        package_name='pandas', module_name='Series')

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        wzsq__iedz = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, wzsq__iedz, index)
    return impl


@overload_method(SeriesType, 'rename_axis', inline='always', no_unliteral=True)
def overload_series_rename_axis(S, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False):
    jsha__lkjoa = dict(index=index, columns=columns, axis=axis, copy=copy,
        inplace=inplace)
    kyar__oicjx = dict(index=None, columns=None, axis=None, copy=True,
        inplace=False)
    check_unsupported_args('Series.rename_axis', jsha__lkjoa, kyar__oicjx,
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
    jsha__lkjoa = dict(level=level)
    kyar__oicjx = dict(level=None)
    check_unsupported_args('Series.count', jsha__lkjoa, kyar__oicjx,
        package_name='pandas', module_name='Series')

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    jsha__lkjoa = dict(method=method, min_periods=min_periods)
    kyar__oicjx = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', jsha__lkjoa, kyar__oicjx,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.corr()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.corr()')

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        akya__unis = S.sum()
        aqiv__repfs = other.sum()
        a = n * (S * other).sum() - akya__unis * aqiv__repfs
        ardxx__sgdfi = n * (S ** 2).sum() - akya__unis ** 2
        icojg__neeu = n * (other ** 2).sum() - aqiv__repfs ** 2
        return a / np.sqrt(ardxx__sgdfi * icojg__neeu)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    jsha__lkjoa = dict(min_periods=min_periods)
    kyar__oicjx = dict(min_periods=None)
    check_unsupported_args('Series.cov', jsha__lkjoa, kyar__oicjx,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.cov()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.cov()')

    def impl(S, other, min_periods=None, ddof=1):
        akya__unis = S.mean()
        aqiv__repfs = other.mean()
        uhbwq__brhtx = ((S - akya__unis) * (other - aqiv__repfs)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(uhbwq__brhtx, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            aowe__mgcs = np.sign(sum_val)
            return np.inf * aowe__mgcs
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    jsha__lkjoa = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    kyar__oicjx = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', jsha__lkjoa, kyar__oicjx,
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
    jsha__lkjoa = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    kyar__oicjx = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', jsha__lkjoa, kyar__oicjx,
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
    jsha__lkjoa = dict(axis=axis, skipna=skipna)
    kyar__oicjx = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', jsha__lkjoa, kyar__oicjx,
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
    jsha__lkjoa = dict(axis=axis, skipna=skipna)
    kyar__oicjx = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', jsha__lkjoa, kyar__oicjx,
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
    jsha__lkjoa = dict(level=level, numeric_only=numeric_only)
    kyar__oicjx = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', jsha__lkjoa, kyar__oicjx,
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
        rwr__qwef = arr[:n]
        qlip__uuu = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(rwr__qwef, qlip__uuu,
            name)
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
        ypf__ooeq = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        rwr__qwef = arr[ypf__ooeq:]
        qlip__uuu = index[ypf__ooeq:]
        return bodo.hiframes.pd_series_ext.init_series(rwr__qwef, qlip__uuu,
            name)
    return impl


@overload_method(SeriesType, 'first', inline='always', no_unliteral=True)
def overload_series_first(S, offset):
    bzf__wda = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in bzf__wda:
        raise BodoError(
            "Series.first(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.first()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            vztat__cmh = index[0]
            lsoe__ievi = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                vztat__cmh, False))
        else:
            lsoe__ievi = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        rwr__qwef = arr[:lsoe__ievi]
        qlip__uuu = index[:lsoe__ievi]
        return bodo.hiframes.pd_series_ext.init_series(rwr__qwef, qlip__uuu,
            name)
    return impl


@overload_method(SeriesType, 'last', inline='always', no_unliteral=True)
def overload_series_last(S, offset):
    bzf__wda = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in bzf__wda:
        raise BodoError(
            "Series.last(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.last()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            bbks__srghw = index[-1]
            lsoe__ievi = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                bbks__srghw, True))
        else:
            lsoe__ievi = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        rwr__qwef = arr[len(arr) - lsoe__ievi:]
        qlip__uuu = index[len(arr) - lsoe__ievi:]
        return bodo.hiframes.pd_series_ext.init_series(rwr__qwef, qlip__uuu,
            name)
    return impl


@overload_method(SeriesType, 'first_valid_index', inline='always',
    no_unliteral=True)
def overload_series_first_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        pztd__uivek = bodo.utils.conversion.index_to_array(index)
        lbh__ihen, ieoiy__quz = bodo.libs.array_kernels.first_last_valid_index(
            arr, pztd__uivek)
        return ieoiy__quz if lbh__ihen else None
    return impl


@overload_method(SeriesType, 'last_valid_index', inline='always',
    no_unliteral=True)
def overload_series_last_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        pztd__uivek = bodo.utils.conversion.index_to_array(index)
        lbh__ihen, ieoiy__quz = bodo.libs.array_kernels.first_last_valid_index(
            arr, pztd__uivek, False)
        return ieoiy__quz if lbh__ihen else None
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    jsha__lkjoa = dict(keep=keep)
    kyar__oicjx = dict(keep='first')
    check_unsupported_args('Series.nlargest', jsha__lkjoa, kyar__oicjx,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nlargest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nlargest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        pztd__uivek = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        hbeqo__fbr, wlo__npq = bodo.libs.array_kernels.nlargest(arr,
            pztd__uivek, n, True, bodo.hiframes.series_kernels.gt_f)
        wnwjp__yap = bodo.utils.conversion.convert_to_index(wlo__npq)
        return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
            wnwjp__yap, name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    jsha__lkjoa = dict(keep=keep)
    kyar__oicjx = dict(keep='first')
    check_unsupported_args('Series.nsmallest', jsha__lkjoa, kyar__oicjx,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nsmallest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nsmallest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        pztd__uivek = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        hbeqo__fbr, wlo__npq = bodo.libs.array_kernels.nlargest(arr,
            pztd__uivek, n, False, bodo.hiframes.series_kernels.lt_f)
        wnwjp__yap = bodo.utils.conversion.convert_to_index(wlo__npq)
        return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
            wnwjp__yap, name)
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
    jsha__lkjoa = dict(errors=errors)
    kyar__oicjx = dict(errors='raise')
    check_unsupported_args('Series.astype', jsha__lkjoa, kyar__oicjx,
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
        hbeqo__fbr = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr, index, name)
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    jsha__lkjoa = dict(axis=axis, is_copy=is_copy)
    kyar__oicjx = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', jsha__lkjoa, kyar__oicjx,
        package_name='pandas', module_name='Series')
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        exvj__tyocl = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[exvj__tyocl],
            index[exvj__tyocl], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    jsha__lkjoa = dict(axis=axis, kind=kind, order=order)
    kyar__oicjx = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', jsha__lkjoa, kyar__oicjx,
        package_name='pandas', module_name='Series')

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        csr__gob = S.notna().values
        if not csr__gob.all():
            hbeqo__fbr = np.full(n, -1, np.int64)
            hbeqo__fbr[csr__gob] = argsort(arr[csr__gob])
        else:
            hbeqo__fbr = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr, index, name)
    return impl


@overload_method(SeriesType, 'rank', inline='always', no_unliteral=True)
def overload_series_rank(S, axis=0, method='average', numeric_only=None,
    na_option='keep', ascending=True, pct=False):
    jsha__lkjoa = dict(axis=axis, numeric_only=numeric_only)
    kyar__oicjx = dict(axis=0, numeric_only=None)
    check_unsupported_args('Series.rank', jsha__lkjoa, kyar__oicjx,
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
        hbeqo__fbr = bodo.libs.array_kernels.rank(arr, method=method,
            na_option=na_option, ascending=ascending, pct=pct)
        return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr, index, name)
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    jsha__lkjoa = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    kyar__oicjx = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', jsha__lkjoa, kyar__oicjx,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_index(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_index(): 'na_position' should either be 'first' or 'last'"
            )
    ofche__pmigr = ColNamesMetaType(('$_bodo_col3_',))

    def impl(S, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        sjpsp__uliwg = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ofche__pmigr)
        ntm__emup = sjpsp__uliwg.sort_index(ascending=ascending, inplace=
            inplace, na_position=na_position)
        hbeqo__fbr = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            ntm__emup, 0)
        wnwjp__yap = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            ntm__emup)
        return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
            wnwjp__yap, name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    jsha__lkjoa = dict(axis=axis, inplace=inplace, kind=kind, ignore_index=
        ignore_index, key=key)
    kyar__oicjx = dict(axis=0, inplace=False, kind='quicksort',
        ignore_index=False, key=None)
    check_unsupported_args('Series.sort_values', jsha__lkjoa, kyar__oicjx,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_values(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_values(): 'na_position' should either be 'first' or 'last'"
            )
    csog__pmyx = ColNamesMetaType(('$_bodo_col_',))

    def impl(S, axis=0, ascending=True, inplace=False, kind='quicksort',
        na_position='last', ignore_index=False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        sjpsp__uliwg = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, csog__pmyx)
        ntm__emup = sjpsp__uliwg.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        hbeqo__fbr = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            ntm__emup, 0)
        wnwjp__yap = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            ntm__emup)
        return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
            wnwjp__yap, name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    zmsb__yvbs = is_overload_true(is_nullable)
    bjif__ckcn = (
        'def impl(bins, arr, is_nullable=True, include_lowest=True):\n')
    bjif__ckcn += '  numba.parfors.parfor.init_prange()\n'
    bjif__ckcn += '  n = len(arr)\n'
    if zmsb__yvbs:
        bjif__ckcn += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        bjif__ckcn += '  out_arr = np.empty(n, np.int64)\n'
    bjif__ckcn += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    bjif__ckcn += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if zmsb__yvbs:
        bjif__ckcn += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        bjif__ckcn += '      out_arr[i] = -1\n'
    bjif__ckcn += '      continue\n'
    bjif__ckcn += '    val = arr[i]\n'
    bjif__ckcn += '    if include_lowest and val == bins[0]:\n'
    bjif__ckcn += '      ind = 1\n'
    bjif__ckcn += '    else:\n'
    bjif__ckcn += '      ind = np.searchsorted(bins, val)\n'
    bjif__ckcn += '    if ind == 0 or ind == len(bins):\n'
    if zmsb__yvbs:
        bjif__ckcn += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        bjif__ckcn += '      out_arr[i] = -1\n'
    bjif__ckcn += '    else:\n'
    bjif__ckcn += '      out_arr[i] = ind - 1\n'
    bjif__ckcn += '  return out_arr\n'
    lyyah__edntv = {}
    exec(bjif__ckcn, {'bodo': bodo, 'np': np, 'numba': numba}, lyyah__edntv)
    impl = lyyah__edntv['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        kyq__jpg, btn__ljiw = np.divmod(x, 1)
        if kyq__jpg == 0:
            vdi__pvv = -int(np.floor(np.log10(abs(btn__ljiw)))) - 1 + precision
        else:
            vdi__pvv = precision
        return np.around(x, vdi__pvv)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        iey__arbfi = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(iey__arbfi)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        lenqs__znyao = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            ukcmt__ypeg = bins.copy()
            if right and include_lowest:
                ukcmt__ypeg[0] = ukcmt__ypeg[0] - lenqs__znyao
            dzh__ztd = bodo.libs.interval_arr_ext.init_interval_array(
                ukcmt__ypeg[:-1], ukcmt__ypeg[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(dzh__ztd,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        ukcmt__ypeg = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            ukcmt__ypeg[0] = ukcmt__ypeg[0] - 10.0 ** -precision
        dzh__ztd = bodo.libs.interval_arr_ext.init_interval_array(ukcmt__ypeg
            [:-1], ukcmt__ypeg[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(dzh__ztd, None)
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        pturh__pkwfd = bodo.hiframes.pd_series_ext.get_series_data(count_series
            )
        vbuqd__tfsb = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        hbeqo__fbr = np.zeros(nbins, np.int64)
        for muw__dug in range(len(pturh__pkwfd)):
            hbeqo__fbr[vbuqd__tfsb[muw__dug]] = pturh__pkwfd[muw__dug]
        return hbeqo__fbr
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
            xfn__iln = (max_val - min_val) * 0.001
            if right:
                bins[0] -= xfn__iln
            else:
                bins[-1] += xfn__iln
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    jsha__lkjoa = dict(dropna=dropna)
    kyar__oicjx = dict(dropna=True)
    check_unsupported_args('Series.value_counts', jsha__lkjoa, kyar__oicjx,
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
    wbhn__tbz = not is_overload_none(bins)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.value_counts()')
    bjif__ckcn = 'def impl(\n'
    bjif__ckcn += '    S,\n'
    bjif__ckcn += '    normalize=False,\n'
    bjif__ckcn += '    sort=True,\n'
    bjif__ckcn += '    ascending=False,\n'
    bjif__ckcn += '    bins=None,\n'
    bjif__ckcn += '    dropna=True,\n'
    bjif__ckcn += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    bjif__ckcn += '):\n'
    bjif__ckcn += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    bjif__ckcn += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    bjif__ckcn += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    if wbhn__tbz:
        bjif__ckcn += '    right = True\n'
        bjif__ckcn += _gen_bins_handling(bins, S.dtype)
        bjif__ckcn += '    arr = get_bin_inds(bins, arr)\n'
    bjif__ckcn += (
        '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
    bjif__ckcn += (
        '        (arr,), index, __col_name_meta_value_series_value_counts\n')
    bjif__ckcn += '    )\n'
    bjif__ckcn += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if wbhn__tbz:
        bjif__ckcn += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        bjif__ckcn += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        bjif__ckcn += '    index = get_bin_labels(bins)\n'
    else:
        bjif__ckcn += (
            '    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)\n'
            )
        bjif__ckcn += '    ind_arr = bodo.utils.conversion.coerce_to_array(\n'
        bjif__ckcn += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        bjif__ckcn += '    )\n'
        bjif__ckcn += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    bjif__ckcn += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        bjif__ckcn += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        njw__fylbc = 'len(S)' if wbhn__tbz else 'count_arr.sum()'
        bjif__ckcn += f'    res = res / float({njw__fylbc})\n'
    bjif__ckcn += '    return res\n'
    lyyah__edntv = {}
    exec(bjif__ckcn, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins, '__col_name_meta_value_series_value_counts':
        ColNamesMetaType(('$_bodo_col2_',))}, lyyah__edntv)
    impl = lyyah__edntv['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    bjif__ckcn = ''
    if isinstance(bins, types.Integer):
        bjif__ckcn += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        bjif__ckcn += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            bjif__ckcn += '    min_val = min_val.value\n'
            bjif__ckcn += '    max_val = max_val.value\n'
        bjif__ckcn += (
            '    bins = compute_bins(bins, min_val, max_val, right)\n')
        if dtype == bodo.datetime64ns:
            bjif__ckcn += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        bjif__ckcn += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return bjif__ckcn


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    jsha__lkjoa = dict(right=right, labels=labels, retbins=retbins,
        precision=precision, duplicates=duplicates, ordered=ordered)
    kyar__oicjx = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pandas.cut', jsha__lkjoa, kyar__oicjx,
        package_name='pandas', module_name='General')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x, 'pandas.cut()'
        )
    bjif__ckcn = 'def impl(\n'
    bjif__ckcn += '    x,\n'
    bjif__ckcn += '    bins,\n'
    bjif__ckcn += '    right=True,\n'
    bjif__ckcn += '    labels=None,\n'
    bjif__ckcn += '    retbins=False,\n'
    bjif__ckcn += '    precision=3,\n'
    bjif__ckcn += '    include_lowest=False,\n'
    bjif__ckcn += "    duplicates='raise',\n"
    bjif__ckcn += '    ordered=True\n'
    bjif__ckcn += '):\n'
    if isinstance(x, SeriesType):
        bjif__ckcn += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        bjif__ckcn += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        bjif__ckcn += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        bjif__ckcn += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    bjif__ckcn += _gen_bins_handling(bins, x.dtype)
    bjif__ckcn += '    arr = get_bin_inds(bins, arr, False, include_lowest)\n'
    bjif__ckcn += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    bjif__ckcn += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None, None)
"""
    bjif__ckcn += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        bjif__ckcn += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        bjif__ckcn += '    return res\n'
    else:
        bjif__ckcn += '    return out_arr\n'
    lyyah__edntv = {}
    exec(bjif__ckcn, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, lyyah__edntv)
    impl = lyyah__edntv['impl']
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
    jsha__lkjoa = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    kyar__oicjx = dict(labels=None, retbins=False, precision=3, duplicates=
        'raise')
    check_unsupported_args('pandas.qcut', jsha__lkjoa, kyar__oicjx,
        package_name='pandas', module_name='General')
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'pandas.qcut()')

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        kdwkh__tgare = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, kdwkh__tgare)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    jsha__lkjoa = dict(axis=axis, sort=sort, group_keys=group_keys, squeeze
        =squeeze, observed=observed, dropna=dropna)
    kyar__oicjx = dict(axis=0, sort=True, group_keys=True, squeeze=False,
        observed=True, dropna=True)
    check_unsupported_args('Series.groupby', jsha__lkjoa, kyar__oicjx,
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
        cszrj__wtw = ColNamesMetaType((' ', ''))

        def impl_index(S, by=None, axis=0, level=None, as_index=True, sort=
            True, group_keys=True, squeeze=False, observed=True, dropna=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            kviq__uxo = bodo.utils.conversion.coerce_to_array(index)
            sjpsp__uliwg = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                kviq__uxo, arr), index, cszrj__wtw)
            return sjpsp__uliwg.groupby(' ')['']
        return impl_index
    slsob__ypu = by
    if isinstance(by, SeriesType):
        slsob__ypu = by.data
    if isinstance(slsob__ypu, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )
    ldyk__vhpg = ColNamesMetaType((' ', ''))

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        kviq__uxo = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        sjpsp__uliwg = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            kviq__uxo, arr), index, ldyk__vhpg)
        return sjpsp__uliwg.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    jsha__lkjoa = dict(verify_integrity=verify_integrity)
    kyar__oicjx = dict(verify_integrity=False)
    check_unsupported_args('Series.append', jsha__lkjoa, kyar__oicjx,
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
            igwb__nyts = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            hbeqo__fbr = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(hbeqo__fbr, A, igwb__nyts, False)
            return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
                index, name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        hbeqo__fbr = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr, index, name)
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    jsha__lkjoa = dict(interpolation=interpolation)
    kyar__oicjx = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', jsha__lkjoa, kyar__oicjx,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.quantile()')
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            hbeqo__fbr = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
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
        hvhd__lbi = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(hvhd__lbi, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    jsha__lkjoa = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    kyar__oicjx = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', jsha__lkjoa, kyar__oicjx,
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
        hvb__ddvl = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        hvb__ddvl = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    bjif__ckcn = '\n'.join(('def impl(', '    S,', '    value=None,',
        '    method=None,', '    axis=None,', '    inplace=False,',
        '    limit=None,', '    downcast=None,', '):',
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)',
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)',
        '    n = len(in_arr)', '    nf = len(fill_arr)',
        "    assert n == nf, 'fillna() requires same length arrays'",
        f'    out_arr = {hvb__ddvl}(n, -1)',
        '    for j in numba.parfors.parfor.internal_prange(n):',
        '        s = in_arr[j]',
        '        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna('
        , '            fill_arr, j', '        ):',
        '            s = fill_arr[j]', '        out_arr[j] = s',
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)'
        ))
    vku__lhei = dict()
    exec(bjif__ckcn, {'bodo': bodo, 'numba': numba}, vku__lhei)
    yrdo__uiga = vku__lhei['impl']
    return yrdo__uiga


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        hvb__ddvl = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        hvb__ddvl = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    bjif__ckcn = 'def impl(S,\n'
    bjif__ckcn += '     value=None,\n'
    bjif__ckcn += '    method=None,\n'
    bjif__ckcn += '    axis=None,\n'
    bjif__ckcn += '    inplace=False,\n'
    bjif__ckcn += '    limit=None,\n'
    bjif__ckcn += '   downcast=None,\n'
    bjif__ckcn += '):\n'
    bjif__ckcn += (
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    bjif__ckcn += '    n = len(in_arr)\n'
    bjif__ckcn += f'    out_arr = {hvb__ddvl}(n, -1)\n'
    bjif__ckcn += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    bjif__ckcn += '        s = in_arr[j]\n'
    bjif__ckcn += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    bjif__ckcn += '            s = value\n'
    bjif__ckcn += '        out_arr[j] = s\n'
    bjif__ckcn += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    vku__lhei = dict()
    exec(bjif__ckcn, {'bodo': bodo, 'numba': numba}, vku__lhei)
    yrdo__uiga = vku__lhei['impl']
    return yrdo__uiga


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    cfq__odk = bodo.hiframes.pd_series_ext.get_series_data(S)
    ubby__uujj = bodo.hiframes.pd_series_ext.get_series_data(value)
    for muw__dug in numba.parfors.parfor.internal_prange(len(cfq__odk)):
        s = cfq__odk[muw__dug]
        if bodo.libs.array_kernels.isna(cfq__odk, muw__dug
            ) and not bodo.libs.array_kernels.isna(ubby__uujj, muw__dug):
            s = ubby__uujj[muw__dug]
        cfq__odk[muw__dug] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    cfq__odk = bodo.hiframes.pd_series_ext.get_series_data(S)
    for muw__dug in numba.parfors.parfor.internal_prange(len(cfq__odk)):
        s = cfq__odk[muw__dug]
        if bodo.libs.array_kernels.isna(cfq__odk, muw__dug):
            s = value
        cfq__odk[muw__dug] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    cfq__odk = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    ubby__uujj = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(cfq__odk)
    hbeqo__fbr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for yirv__zfve in numba.parfors.parfor.internal_prange(n):
        s = cfq__odk[yirv__zfve]
        if bodo.libs.array_kernels.isna(cfq__odk, yirv__zfve
            ) and not bodo.libs.array_kernels.isna(ubby__uujj, yirv__zfve):
            s = ubby__uujj[yirv__zfve]
        hbeqo__fbr[yirv__zfve] = s
        if bodo.libs.array_kernels.isna(cfq__odk, yirv__zfve
            ) and bodo.libs.array_kernels.isna(ubby__uujj, yirv__zfve):
            bodo.libs.array_kernels.setna(hbeqo__fbr, yirv__zfve)
    return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    cfq__odk = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    ubby__uujj = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(cfq__odk)
    hbeqo__fbr = bodo.utils.utils.alloc_type(n, cfq__odk.dtype, (-1,))
    for muw__dug in numba.parfors.parfor.internal_prange(n):
        s = cfq__odk[muw__dug]
        if bodo.libs.array_kernels.isna(cfq__odk, muw__dug
            ) and not bodo.libs.array_kernels.isna(ubby__uujj, muw__dug):
            s = ubby__uujj[muw__dug]
        hbeqo__fbr[muw__dug] = s
    return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    jsha__lkjoa = dict(limit=limit, downcast=downcast)
    kyar__oicjx = dict(limit=None, downcast=None)
    check_unsupported_args('Series.fillna', jsha__lkjoa, kyar__oicjx,
        package_name='pandas', module_name='Series')
    qxjd__yyezd = not is_overload_none(value)
    qshq__tzgob = not is_overload_none(method)
    if qxjd__yyezd and qshq__tzgob:
        raise BodoError(
            "Series.fillna(): Cannot specify both 'value' and 'method'.")
    if not qxjd__yyezd and not qshq__tzgob:
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
    if qshq__tzgob:
        if is_overload_true(inplace):
            raise BodoError(
                "Series.fillna() with inplace=True not supported with 'method' argument yet."
                )
        yadw__vpqh = (
            "Series.fillna(): 'method' argument if provided must be a constant string and one of ('backfill', 'bfill', 'pad' 'ffill')."
            )
        if not is_overload_constant_str(method):
            raise_bodo_error(yadw__vpqh)
        elif get_overload_const_str(method) not in ('backfill', 'bfill',
            'pad', 'ffill'):
            raise BodoError(yadw__vpqh)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.fillna()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'Series.fillna()')
    payh__qlxln = element_type(S.data)
    jara__nhgd = None
    if qxjd__yyezd:
        jara__nhgd = element_type(types.unliteral(value))
    if jara__nhgd and not can_replace(payh__qlxln, jara__nhgd):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {jara__nhgd} with series type {payh__qlxln}'
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
        qjl__bghp = to_str_arr_if_dict_array(S.data)
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                cfq__odk = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                ubby__uujj = bodo.hiframes.pd_series_ext.get_series_data(value)
                n = len(cfq__odk)
                hbeqo__fbr = bodo.utils.utils.alloc_type(n, qjl__bghp, (-1,))
                for muw__dug in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(cfq__odk, muw__dug
                        ) and bodo.libs.array_kernels.isna(ubby__uujj, muw__dug
                        ):
                        bodo.libs.array_kernels.setna(hbeqo__fbr, muw__dug)
                        continue
                    if bodo.libs.array_kernels.isna(cfq__odk, muw__dug):
                        hbeqo__fbr[muw__dug
                            ] = bodo.utils.conversion.unbox_if_timestamp(
                            ubby__uujj[muw__dug])
                        continue
                    hbeqo__fbr[muw__dug
                        ] = bodo.utils.conversion.unbox_if_timestamp(cfq__odk
                        [muw__dug])
                return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
                    index, name)
            return fillna_series_impl
        if qshq__tzgob:
            cyg__qlb = (types.unicode_type, types.bool_, bodo.datetime64ns,
                bodo.timedelta64ns)
            if not isinstance(payh__qlxln, (types.Integer, types.Float)
                ) and payh__qlxln not in cyg__qlb:
                raise BodoError(
                    f"Series.fillna(): series of type {payh__qlxln} are not supported with 'method' argument."
                    )

            def fillna_method_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                cfq__odk = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                hbeqo__fbr = bodo.libs.array_kernels.ffill_bfill_arr(cfq__odk,
                    method)
                return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
                    index, name)
            return fillna_method_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_timestamp(value)
            cfq__odk = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(cfq__odk)
            hbeqo__fbr = bodo.utils.utils.alloc_type(n, qjl__bghp, (-1,))
            for muw__dug in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_timestamp(cfq__odk[muw__dug]
                    )
                if bodo.libs.array_kernels.isna(cfq__odk, muw__dug):
                    s = value
                hbeqo__fbr[muw__dug] = s
            return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
                index, name)
        return fillna_impl


def create_fillna_specific_method_overload(overload_name):

    def overload_series_fillna_specific_method(S, axis=None, inplace=False,
        limit=None, downcast=None):
        bjc__ugvme = {'ffill': 'ffill', 'bfill': 'bfill', 'pad': 'ffill',
            'backfill': 'bfill'}[overload_name]
        jsha__lkjoa = dict(limit=limit, downcast=downcast)
        kyar__oicjx = dict(limit=None, downcast=None)
        check_unsupported_args(f'Series.{overload_name}', jsha__lkjoa,
            kyar__oicjx, package_name='pandas', module_name='Series')
        if not (is_overload_none(axis) or is_overload_zero(axis)):
            raise BodoError(
                f'Series.{overload_name}(): axis argument not supported')
        payh__qlxln = element_type(S.data)
        cyg__qlb = (types.unicode_type, types.bool_, bodo.datetime64ns,
            bodo.timedelta64ns)
        if not isinstance(payh__qlxln, (types.Integer, types.Float)
            ) and payh__qlxln not in cyg__qlb:
            raise BodoError(
                f'Series.{overload_name}(): series of type {payh__qlxln} are not supported.'
                )

        def impl(S, axis=None, inplace=False, limit=None, downcast=None):
            cfq__odk = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            hbeqo__fbr = bodo.libs.array_kernels.ffill_bfill_arr(cfq__odk,
                bjc__ugvme)
            return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
                index, name)
        return impl
    return overload_series_fillna_specific_method


fillna_specific_methods = 'ffill', 'bfill', 'pad', 'backfill'


def _install_fillna_specific_methods():
    for overload_name in fillna_specific_methods:
        djm__eci = create_fillna_specific_method_overload(overload_name)
        overload_method(SeriesType, overload_name, no_unliteral=True)(djm__eci)


_install_fillna_specific_methods()


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        hgtt__eucx = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(hgtt__eucx)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        hgtt__eucx = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(hgtt__eucx)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        hgtt__eucx = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(hgtt__eucx)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    jsha__lkjoa = dict(inplace=inplace, limit=limit, regex=regex, method=method
        )
    eqyit__rhzq = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', jsha__lkjoa, eqyit__rhzq,
        package_name='pandas', module_name='Series')
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.replace()')
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    payh__qlxln = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        ftflv__xepsz = element_type(to_replace.key_type)
        jara__nhgd = element_type(to_replace.value_type)
    else:
        ftflv__xepsz = element_type(to_replace)
        jara__nhgd = element_type(value)
    vvwnt__bsjf = None
    if payh__qlxln != types.unliteral(ftflv__xepsz):
        if bodo.utils.typing.equality_always_false(payh__qlxln, types.
            unliteral(ftflv__xepsz)
            ) or not bodo.utils.typing.types_equality_exists(payh__qlxln,
            ftflv__xepsz):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(payh__qlxln, (types.Float, types.Integer)
            ) or payh__qlxln == np.bool_:
            vvwnt__bsjf = payh__qlxln
    if not can_replace(payh__qlxln, types.unliteral(jara__nhgd)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    lqb__tuslc = to_str_arr_if_dict_array(S.data)
    if isinstance(lqb__tuslc, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            cfq__odk = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(cfq__odk.replace
                (to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        cfq__odk = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(cfq__odk)
        hbeqo__fbr = bodo.utils.utils.alloc_type(n, lqb__tuslc, (-1,))
        mrd__bleru = build_replace_dict(to_replace, value, vvwnt__bsjf)
        for muw__dug in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(cfq__odk, muw__dug):
                bodo.libs.array_kernels.setna(hbeqo__fbr, muw__dug)
                continue
            s = cfq__odk[muw__dug]
            if s in mrd__bleru:
                s = mrd__bleru[s]
            hbeqo__fbr[muw__dug] = s
        return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr, index, name)
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    redg__jryno = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    aek__xwkh = is_iterable_type(to_replace)
    fxvg__hgdgq = isinstance(value, (types.Number, Decimal128Type)
        ) or value in [bodo.string_type, bodo.bytes_type, types.boolean]
    kru__tcb = is_iterable_type(value)
    if redg__jryno and fxvg__hgdgq:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                mrd__bleru = {}
                mrd__bleru[key_dtype_conv(to_replace)] = value
                return mrd__bleru
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            mrd__bleru = {}
            mrd__bleru[to_replace] = value
            return mrd__bleru
        return impl
    if aek__xwkh and fxvg__hgdgq:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                mrd__bleru = {}
                for chs__fsqxr in to_replace:
                    mrd__bleru[key_dtype_conv(chs__fsqxr)] = value
                return mrd__bleru
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            mrd__bleru = {}
            for chs__fsqxr in to_replace:
                mrd__bleru[chs__fsqxr] = value
            return mrd__bleru
        return impl
    if aek__xwkh and kru__tcb:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                mrd__bleru = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for muw__dug in range(len(to_replace)):
                    mrd__bleru[key_dtype_conv(to_replace[muw__dug])] = value[
                        muw__dug]
                return mrd__bleru
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            mrd__bleru = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for muw__dug in range(len(to_replace)):
                mrd__bleru[to_replace[muw__dug]] = value[muw__dug]
            return mrd__bleru
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
            hbeqo__fbr = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo.
                hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
                index, name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        hbeqo__fbr = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr, index, name)
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    jsha__lkjoa = dict(ignore_index=ignore_index)
    cfqz__pxkq = dict(ignore_index=False)
    check_unsupported_args('Series.explode', jsha__lkjoa, cfqz__pxkq,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        pztd__uivek = bodo.utils.conversion.index_to_array(index)
        hbeqo__fbr, vldm__lhre = bodo.libs.array_kernels.explode(arr,
            pztd__uivek)
        wnwjp__yap = bodo.utils.conversion.index_from_array(vldm__lhre)
        return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
            wnwjp__yap, name)
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
            hhim__yrss = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for muw__dug in numba.parfors.parfor.internal_prange(n):
                hhim__yrss[muw__dug] = np.argmax(a[muw__dug])
            return hhim__yrss
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            njrt__vat = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for muw__dug in numba.parfors.parfor.internal_prange(n):
                njrt__vat[muw__dug] = np.argmin(a[muw__dug])
            return njrt__vat
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
    jsha__lkjoa = dict(axis=axis, inplace=inplace, how=how)
    ezrc__hzf = dict(axis=0, inplace=False, how=None)
    check_unsupported_args('Series.dropna', jsha__lkjoa, ezrc__hzf,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.dropna()')
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False, how=None):
            cfq__odk = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            csr__gob = S.notna().values
            pztd__uivek = bodo.utils.conversion.extract_index_array(S)
            wnwjp__yap = bodo.utils.conversion.convert_to_index(pztd__uivek
                [csr__gob])
            hbeqo__fbr = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(cfq__odk))
            return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
                wnwjp__yap, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False, how=None):
            cfq__odk = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            pztd__uivek = bodo.utils.conversion.extract_index_array(S)
            csr__gob = S.notna().values
            wnwjp__yap = bodo.utils.conversion.convert_to_index(pztd__uivek
                [csr__gob])
            hbeqo__fbr = cfq__odk[csr__gob]
            return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
                wnwjp__yap, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    jsha__lkjoa = dict(freq=freq, axis=axis, fill_value=fill_value)
    kyar__oicjx = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('Series.shift', jsha__lkjoa, kyar__oicjx,
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
        hbeqo__fbr = bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr, index, name)
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    jsha__lkjoa = dict(fill_method=fill_method, limit=limit, freq=freq)
    kyar__oicjx = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', jsha__lkjoa, kyar__oicjx,
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
        hbeqo__fbr = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr, index, name)
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
            wxlrz__gyrkf = 'None'
        else:
            wxlrz__gyrkf = 'other'
        bjif__ckcn = """def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise',try_cast=False):
"""
        if func_name == 'mask':
            bjif__ckcn += '  cond = ~cond\n'
        bjif__ckcn += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        bjif__ckcn += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        bjif__ckcn += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        bjif__ckcn += f"""  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {wxlrz__gyrkf})
"""
        bjif__ckcn += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        lyyah__edntv = {}
        exec(bjif__ckcn, {'bodo': bodo, 'np': np}, lyyah__edntv)
        impl = lyyah__edntv['impl']
        return impl
    return overload_series_mask_where


def _install_series_mask_where_overload():
    for func_name in ('mask', 'where'):
        djm__eci = create_series_mask_where_overload(func_name)
        overload_method(SeriesType, func_name, no_unliteral=True)(djm__eci)


_install_series_mask_where_overload()


def _validate_arguments_mask_where(func_name, module_name, S, cond, other,
    inplace, axis, level, errors, try_cast):
    jsha__lkjoa = dict(inplace=inplace, level=level, errors=errors,
        try_cast=try_cast)
    kyar__oicjx = dict(inplace=False, level=None, errors='raise', try_cast=
        False)
    check_unsupported_args(f'{func_name}', jsha__lkjoa, kyar__oicjx,
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
    gkyw__elq = is_overload_constant_nan(other)
    if not (is_default or gkyw__elq or is_scalar_type(other) or isinstance(
        other, types.Array) and other.ndim >= 1 and other.ndim <= max_ndim or
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
            mat__rfnck = arr.dtype.elem_type
        else:
            mat__rfnck = arr.dtype
        if is_iterable_type(other):
            plz__nydym = other.dtype
        elif gkyw__elq:
            plz__nydym = types.float64
        else:
            plz__nydym = types.unliteral(other)
        if not gkyw__elq and not is_common_scalar_dtype([mat__rfnck,
            plz__nydym]):
            raise BodoError(
                f"{func_name}() {module_name.lower()} and 'other' must share a common type."
                )


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        jsha__lkjoa = dict(level=level, axis=axis)
        kyar__oicjx = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__), jsha__lkjoa,
            kyar__oicjx, package_name='pandas', module_name='Series')
        ejw__ruo = other == string_type or is_overload_constant_str(other)
        cds__gufon = is_iterable_type(other) and other.dtype == string_type
        jqqog__zemma = S.dtype == string_type and (op == operator.add and (
            ejw__ruo or cds__gufon) or op == operator.mul and isinstance(
            other, types.Integer))
        svnd__pei = S.dtype == bodo.timedelta64ns
        aav__xheaw = S.dtype == bodo.datetime64ns
        bjalg__rut = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        mtpes__smrye = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype == pd_timestamp_type or 
            other.dtype == bodo.datetime64ns)
        cpguz__agxw = svnd__pei and (bjalg__rut or mtpes__smrye
            ) or aav__xheaw and bjalg__rut
        cpguz__agxw = cpguz__agxw and op == operator.add
        if not (isinstance(S.dtype, types.Number) or jqqog__zemma or
            cpguz__agxw):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        epjj__agu = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            lqb__tuslc = epjj__agu.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and lqb__tuslc == types.Array(types.bool_, 1, 'C'):
                lqb__tuslc = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_timestamp(other)
                n = len(arr)
                hbeqo__fbr = bodo.utils.utils.alloc_type(n, lqb__tuslc, (-1,))
                for muw__dug in numba.parfors.parfor.internal_prange(n):
                    puykr__riscj = bodo.libs.array_kernels.isna(arr, muw__dug)
                    if puykr__riscj:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(hbeqo__fbr, muw__dug)
                        else:
                            hbeqo__fbr[muw__dug] = op(fill_value, other)
                    else:
                        hbeqo__fbr[muw__dug] = op(arr[muw__dug], other)
                return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        lqb__tuslc = epjj__agu.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, IntegerArrayType) and lqb__tuslc == types.Array(
            types.bool_, 1, 'C'):
            lqb__tuslc = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            tavus__hcta = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            hbeqo__fbr = bodo.utils.utils.alloc_type(n, lqb__tuslc, (-1,))
            for muw__dug in numba.parfors.parfor.internal_prange(n):
                puykr__riscj = bodo.libs.array_kernels.isna(arr, muw__dug)
                uoigs__yry = bodo.libs.array_kernels.isna(tavus__hcta, muw__dug
                    )
                if puykr__riscj and uoigs__yry:
                    bodo.libs.array_kernels.setna(hbeqo__fbr, muw__dug)
                elif puykr__riscj:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(hbeqo__fbr, muw__dug)
                    else:
                        hbeqo__fbr[muw__dug] = op(fill_value, tavus__hcta[
                            muw__dug])
                elif uoigs__yry:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(hbeqo__fbr, muw__dug)
                    else:
                        hbeqo__fbr[muw__dug] = op(arr[muw__dug], fill_value)
                else:
                    hbeqo__fbr[muw__dug] = op(arr[muw__dug], tavus__hcta[
                        muw__dug])
            return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
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
        epjj__agu = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            lqb__tuslc = epjj__agu.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and lqb__tuslc == types.Array(types.bool_, 1, 'C'):
                lqb__tuslc = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                hbeqo__fbr = bodo.utils.utils.alloc_type(n, lqb__tuslc, None)
                for muw__dug in numba.parfors.parfor.internal_prange(n):
                    puykr__riscj = bodo.libs.array_kernels.isna(arr, muw__dug)
                    if puykr__riscj:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(hbeqo__fbr, muw__dug)
                        else:
                            hbeqo__fbr[muw__dug] = op(other, fill_value)
                    else:
                        hbeqo__fbr[muw__dug] = op(other, arr[muw__dug])
                return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        lqb__tuslc = epjj__agu.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, IntegerArrayType) and lqb__tuslc == types.Array(
            types.bool_, 1, 'C'):
            lqb__tuslc = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            tavus__hcta = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            hbeqo__fbr = bodo.utils.utils.alloc_type(n, lqb__tuslc, None)
            for muw__dug in numba.parfors.parfor.internal_prange(n):
                puykr__riscj = bodo.libs.array_kernels.isna(arr, muw__dug)
                uoigs__yry = bodo.libs.array_kernels.isna(tavus__hcta, muw__dug
                    )
                hbeqo__fbr[muw__dug] = op(tavus__hcta[muw__dug], arr[muw__dug])
                if puykr__riscj and uoigs__yry:
                    bodo.libs.array_kernels.setna(hbeqo__fbr, muw__dug)
                elif puykr__riscj:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(hbeqo__fbr, muw__dug)
                    else:
                        hbeqo__fbr[muw__dug] = op(tavus__hcta[muw__dug],
                            fill_value)
                elif uoigs__yry:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(hbeqo__fbr, muw__dug)
                    else:
                        hbeqo__fbr[muw__dug] = op(fill_value, arr[muw__dug])
                else:
                    hbeqo__fbr[muw__dug] = op(tavus__hcta[muw__dug], arr[
                        muw__dug])
            return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
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
    for op, keddr__knh in explicit_binop_funcs_two_ways.items():
        for name in keddr__knh:
            djm__eci = create_explicit_binary_op_overload(op)
            yogo__zso = create_explicit_binary_reverse_op_overload(op)
            zyqi__naebr = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(djm__eci)
            overload_method(SeriesType, zyqi__naebr, no_unliteral=True)(
                yogo__zso)
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        djm__eci = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(djm__eci)
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
                zdzq__fxxse = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                hbeqo__fbr = dt64_arr_sub(arr, zdzq__fxxse)
                return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
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
                hbeqo__fbr = np.empty(n, np.dtype('datetime64[ns]'))
                for muw__dug in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, muw__dug):
                        bodo.libs.array_kernels.setna(hbeqo__fbr, muw__dug)
                        continue
                    ywstm__phrzy = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[muw__dug]))
                    nwj__nrce = op(ywstm__phrzy, rhs)
                    hbeqo__fbr[muw__dug
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        nwj__nrce.value)
                return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
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
                    zdzq__fxxse = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    hbeqo__fbr = op(arr, bodo.utils.conversion.
                        unbox_if_timestamp(zdzq__fxxse))
                    return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                zdzq__fxxse = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                hbeqo__fbr = op(arr, zdzq__fxxse)
                return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    ejun__ycfzd = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    hbeqo__fbr = op(bodo.utils.conversion.
                        unbox_if_timestamp(ejun__ycfzd), arr)
                    return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                ejun__ycfzd = (bodo.utils.conversion.
                    get_array_if_series_or_index(lhs))
                hbeqo__fbr = op(ejun__ycfzd, arr)
                return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        djm__eci = create_binary_op_overload(op)
        overload(op)(djm__eci)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    zibs__zymle = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, zibs__zymle)
        for muw__dug in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, muw__dug
                ) or bodo.libs.array_kernels.isna(arg2, muw__dug):
                bodo.libs.array_kernels.setna(S, muw__dug)
                continue
            S[muw__dug
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                muw__dug]) - bodo.hiframes.pd_timestamp_ext.dt64_to_integer
                (arg2[muw__dug]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                tavus__hcta = (bodo.utils.conversion.
                    get_array_if_series_or_index(other))
                op(arr, tavus__hcta)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        djm__eci = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(djm__eci)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                hbeqo__fbr = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        djm__eci = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(djm__eci)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    hbeqo__fbr = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
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
                    tavus__hcta = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    hbeqo__fbr = ufunc(arr, tavus__hcta)
                    return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
                        index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    tavus__hcta = bodo.hiframes.pd_series_ext.get_series_data(
                        S2)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    hbeqo__fbr = ufunc(arr, tavus__hcta)
                    return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
                        index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        djm__eci = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(djm__eci)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        zuurj__amks = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.
            copy(),))
        gduce__bqh = np.arange(n),
        bodo.libs.timsort.sort(zuurj__amks, 0, n, gduce__bqh)
        return gduce__bqh[0]
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
        ymoa__kbl = get_overload_const_str(downcast)
        if ymoa__kbl in ('integer', 'signed'):
            out_dtype = types.int64
        elif ymoa__kbl == 'unsigned':
            out_dtype = types.uint64
        else:
            assert ymoa__kbl == 'float'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arg_a,
        'pandas.to_numeric()')
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            cfq__odk = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            hbeqo__fbr = pd.to_numeric(cfq__odk, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
                index, name)
        return impl_series
    if not is_str_arr_type(arg_a):
        raise BodoError(f'pd.to_numeric(): invalid argument type {arg_a}')
    if out_dtype == types.float64:

        def to_numeric_float_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            sdjk__xcd = np.empty(n, np.float64)
            for muw__dug in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, muw__dug):
                    bodo.libs.array_kernels.setna(sdjk__xcd, muw__dug)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(sdjk__xcd,
                        muw__dug, arg_a, muw__dug)
            return sdjk__xcd
        return to_numeric_float_impl
    else:

        def to_numeric_int_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            sdjk__xcd = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)
            for muw__dug in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, muw__dug):
                    bodo.libs.array_kernels.setna(sdjk__xcd, muw__dug)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(sdjk__xcd,
                        muw__dug, arg_a, muw__dug)
            return sdjk__xcd
        return to_numeric_int_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        nvvvm__gpyfc = if_series_to_array_type(args[0])
        if isinstance(nvvvm__gpyfc, types.Array) and isinstance(nvvvm__gpyfc
            .dtype, types.Integer):
            nvvvm__gpyfc = types.Array(types.float64, 1, 'C')
        return nvvvm__gpyfc(*args)


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
    bjluf__pli = bodo.utils.utils.is_array_typ(x, True)
    bpp__spe = bodo.utils.utils.is_array_typ(y, True)
    bjif__ckcn = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        bjif__ckcn += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if bjluf__pli and not bodo.utils.utils.is_array_typ(x, False):
        bjif__ckcn += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if bpp__spe and not bodo.utils.utils.is_array_typ(y, False):
        bjif__ckcn += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    bjif__ckcn += '  n = len(condition)\n'
    hiloa__jws = x.dtype if bjluf__pli else types.unliteral(x)
    fufts__volz = y.dtype if bpp__spe else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        hiloa__jws = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        fufts__volz = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    ztft__plx = get_data(x)
    ezx__mign = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(gduce__bqh) for
        gduce__bqh in [ztft__plx, ezx__mign])
    if ezx__mign == types.none:
        if isinstance(hiloa__jws, types.Number):
            out_dtype = types.Array(types.float64, 1, 'C')
        else:
            out_dtype = to_nullable_type(x)
    elif ztft__plx == ezx__mign and not is_nullable:
        out_dtype = dtype_to_array_type(hiloa__jws)
    elif hiloa__jws == string_type or fufts__volz == string_type:
        out_dtype = bodo.string_array_type
    elif ztft__plx == bytes_type or (bjluf__pli and hiloa__jws == bytes_type
        ) and (ezx__mign == bytes_type or bpp__spe and fufts__volz ==
        bytes_type):
        out_dtype = binary_array_type
    elif isinstance(hiloa__jws, bodo.PDCategoricalDtype):
        out_dtype = None
    elif hiloa__jws in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(hiloa__jws, 1, 'C')
    elif fufts__volz in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(fufts__volz, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(hiloa__jws), numba.np.numpy_support.
            as_dtype(fufts__volz)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(hiloa__jws, bodo.PDCategoricalDtype):
        gahin__bspc = 'x'
    else:
        gahin__bspc = 'out_dtype'
    bjif__ckcn += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {gahin__bspc}, (-1,))\n')
    if isinstance(hiloa__jws, bodo.PDCategoricalDtype):
        bjif__ckcn += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        bjif__ckcn += (
            '  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)\n'
            )
    bjif__ckcn += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    bjif__ckcn += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if bjluf__pli:
        bjif__ckcn += '      if bodo.libs.array_kernels.isna(x, j):\n'
        bjif__ckcn += '        setna(out_arr, j)\n'
        bjif__ckcn += '        continue\n'
    if isinstance(hiloa__jws, bodo.PDCategoricalDtype):
        bjif__ckcn += '      out_codes[j] = x_codes[j]\n'
    else:
        bjif__ckcn += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('x[j]' if bjluf__pli else 'x'))
    bjif__ckcn += '    else:\n'
    if bpp__spe:
        bjif__ckcn += '      if bodo.libs.array_kernels.isna(y, j):\n'
        bjif__ckcn += '        setna(out_arr, j)\n'
        bjif__ckcn += '        continue\n'
    if ezx__mign == types.none:
        if isinstance(hiloa__jws, bodo.PDCategoricalDtype):
            bjif__ckcn += '      out_codes[j] = -1\n'
        else:
            bjif__ckcn += '      setna(out_arr, j)\n'
    else:
        bjif__ckcn += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('y[j]' if bpp__spe else 'y'))
    bjif__ckcn += '  return out_arr\n'
    lyyah__edntv = {}
    exec(bjif__ckcn, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, lyyah__edntv)
    xctbc__cypm = lyyah__edntv['_impl']
    return xctbc__cypm


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
        jafe__vcw = choicelist.dtype
        if not bodo.utils.utils.is_array_typ(jafe__vcw, True):
            raise BodoError(
                "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                )
        if is_series_type(jafe__vcw):
            bpgg__ycskp = jafe__vcw.data.dtype
        else:
            bpgg__ycskp = jafe__vcw.dtype
        if isinstance(bpgg__ycskp, bodo.PDCategoricalDtype):
            raise BodoError(
                'np.select(): data with choicelist of type Categorical not yet supported'
                )
        tnvie__nnbip = jafe__vcw
    else:
        pzvih__vlapr = []
        for jafe__vcw in choicelist:
            if not bodo.utils.utils.is_array_typ(jafe__vcw, True):
                raise BodoError(
                    "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                    )
            if is_series_type(jafe__vcw):
                bpgg__ycskp = jafe__vcw.data.dtype
            else:
                bpgg__ycskp = jafe__vcw.dtype
            if isinstance(bpgg__ycskp, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            pzvih__vlapr.append(bpgg__ycskp)
        if not is_common_scalar_dtype(pzvih__vlapr):
            raise BodoError(
                f"np.select(): 'choicelist' items must be arrays with a commmon data type. Found a tuple with the following data types {choicelist}."
                )
        tnvie__nnbip = choicelist[0]
    if is_series_type(tnvie__nnbip):
        tnvie__nnbip = tnvie__nnbip.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pass
    else:
        if not is_scalar_type(default):
            raise BodoError(
                "np.select(): 'default' argument must be scalar type")
        if not (is_common_scalar_dtype([default, tnvie__nnbip.dtype]) or 
            default == types.none or is_overload_constant_nan(default)):
            raise BodoError(
                f"np.select(): 'default' is not type compatible with the array types in choicelist. Choicelist type: {choicelist}, Default type: {default}"
                )
    if not (isinstance(tnvie__nnbip, types.Array) or isinstance(
        tnvie__nnbip, BooleanArrayType) or isinstance(tnvie__nnbip,
        IntegerArrayType) or bodo.utils.utils.is_array_typ(tnvie__nnbip, 
        False) and tnvie__nnbip.dtype in [bodo.string_type, bodo.bytes_type]):
        raise BodoError(
            f'np.select(): data with choicelist of type {tnvie__nnbip} not yet supported'
            )


@overload(np.select)
def overload_np_select(condlist, choicelist, default=0):
    _verify_np_select_arg_typs(condlist, choicelist, default)
    hehh__mmk = isinstance(choicelist, (types.List, types.UniTuple)
        ) and isinstance(condlist, (types.List, types.UniTuple))
    if isinstance(choicelist, (types.List, types.UniTuple)):
        xrd__vlq = choicelist.dtype
    else:
        tkgnm__msiq = False
        pzvih__vlapr = []
        for jafe__vcw in choicelist:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(jafe__vcw
                , 'numpy.select()')
            if is_nullable_type(jafe__vcw):
                tkgnm__msiq = True
            if is_series_type(jafe__vcw):
                bpgg__ycskp = jafe__vcw.data.dtype
            else:
                bpgg__ycskp = jafe__vcw.dtype
            if isinstance(bpgg__ycskp, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            pzvih__vlapr.append(bpgg__ycskp)
        mujk__hqs, wol__kwn = get_common_scalar_dtype(pzvih__vlapr)
        if not wol__kwn:
            raise BodoError('Internal error in overload_np_select')
        fdrcb__jtphb = dtype_to_array_type(mujk__hqs)
        if tkgnm__msiq:
            fdrcb__jtphb = to_nullable_type(fdrcb__jtphb)
        xrd__vlq = fdrcb__jtphb
    if isinstance(xrd__vlq, SeriesType):
        xrd__vlq = xrd__vlq.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        rszjl__qyfw = True
    else:
        rszjl__qyfw = False
    jezmz__wgm = False
    bcnh__eucby = False
    if rszjl__qyfw:
        if isinstance(xrd__vlq.dtype, types.Number):
            pass
        elif xrd__vlq.dtype == types.bool_:
            bcnh__eucby = True
        else:
            jezmz__wgm = True
            xrd__vlq = to_nullable_type(xrd__vlq)
    elif default == types.none or is_overload_constant_nan(default):
        jezmz__wgm = True
        xrd__vlq = to_nullable_type(xrd__vlq)
    bjif__ckcn = 'def np_select_impl(condlist, choicelist, default=0):\n'
    bjif__ckcn += '  if len(condlist) != len(choicelist):\n'
    bjif__ckcn += """    raise ValueError('list of cases must be same length as list of conditions')
"""
    bjif__ckcn += '  output_len = len(choicelist[0])\n'
    bjif__ckcn += (
        '  out = bodo.utils.utils.alloc_type(output_len, alloc_typ, (-1,))\n')
    bjif__ckcn += '  for i in range(output_len):\n'
    if jezmz__wgm:
        bjif__ckcn += '    bodo.libs.array_kernels.setna(out, i)\n'
    elif bcnh__eucby:
        bjif__ckcn += '    out[i] = False\n'
    else:
        bjif__ckcn += '    out[i] = default\n'
    if hehh__mmk:
        bjif__ckcn += '  for i in range(len(condlist) - 1, -1, -1):\n'
        bjif__ckcn += '    cond = condlist[i]\n'
        bjif__ckcn += '    choice = choicelist[i]\n'
        bjif__ckcn += '    out = np.where(cond, choice, out)\n'
    else:
        for muw__dug in range(len(choicelist) - 1, -1, -1):
            bjif__ckcn += f'  cond = condlist[{muw__dug}]\n'
            bjif__ckcn += f'  choice = choicelist[{muw__dug}]\n'
            bjif__ckcn += f'  out = np.where(cond, choice, out)\n'
    bjif__ckcn += '  return out'
    lyyah__edntv = dict()
    exec(bjif__ckcn, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'alloc_typ': xrd__vlq}, lyyah__edntv)
    impl = lyyah__edntv['np_select_impl']
    return impl


@overload_method(SeriesType, 'duplicated', inline='always', no_unliteral=True)
def overload_series_duplicated(S, keep='first'):

    def impl(S, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        hbeqo__fbr = bodo.libs.array_kernels.duplicated((arr,))
        return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr, index, name)
    return impl


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    jsha__lkjoa = dict(subset=subset, keep=keep, inplace=inplace)
    kyar__oicjx = dict(subset=None, keep='first', inplace=False)
    check_unsupported_args('Series.drop_duplicates', jsha__lkjoa,
        kyar__oicjx, package_name='pandas', module_name='Series')

    def impl(S, subset=None, keep='first', inplace=False):
        xlpeq__otei = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (xlpeq__otei,), pztd__uivek = bodo.libs.array_kernels.drop_duplicates((
            xlpeq__otei,), index, 1)
        index = bodo.utils.conversion.index_from_array(pztd__uivek)
        return bodo.hiframes.pd_series_ext.init_series(xlpeq__otei, index, name
            )
    return impl


@overload_method(SeriesType, 'between', inline='always', no_unliteral=True)
def overload_series_between(S, left, right, inclusive='both'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(left,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(right,
        'Series.between()')
    pesx__zntww = element_type(S.data)
    if not is_common_scalar_dtype([pesx__zntww, left]):
        raise_bodo_error(
            "Series.between(): 'left' must be compariable with the Series data"
            )
    if not is_common_scalar_dtype([pesx__zntww, right]):
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
        hbeqo__fbr = np.empty(n, np.bool_)
        for muw__dug in numba.parfors.parfor.internal_prange(n):
            ied__xbla = bodo.utils.conversion.box_if_dt64(arr[muw__dug])
            if inclusive == 'both':
                hbeqo__fbr[muw__dug] = ied__xbla <= right and ied__xbla >= left
            else:
                hbeqo__fbr[muw__dug] = ied__xbla < right and ied__xbla > left
        return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr, index, name)
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    jsha__lkjoa = dict(axis=axis)
    kyar__oicjx = dict(axis=None)
    check_unsupported_args('Series.repeat', jsha__lkjoa, kyar__oicjx,
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
            pztd__uivek = bodo.utils.conversion.index_to_array(index)
            hbeqo__fbr = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            vldm__lhre = bodo.libs.array_kernels.repeat_kernel(pztd__uivek,
                repeats)
            wnwjp__yap = bodo.utils.conversion.index_from_array(vldm__lhre)
            return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
                wnwjp__yap, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        pztd__uivek = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        hbeqo__fbr = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        vldm__lhre = bodo.libs.array_kernels.repeat_kernel(pztd__uivek, repeats
            )
        wnwjp__yap = bodo.utils.conversion.index_from_array(vldm__lhre)
        return bodo.hiframes.pd_series_ext.init_series(hbeqo__fbr,
            wnwjp__yap, name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        gduce__bqh = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(gduce__bqh)
        riq__zfyxb = {}
        for muw__dug in range(n):
            ied__xbla = bodo.utils.conversion.box_if_dt64(gduce__bqh[muw__dug])
            riq__zfyxb[index[muw__dug]] = ied__xbla
        return riq__zfyxb
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    yadw__vpqh = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            rlg__xtgo = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(yadw__vpqh)
    elif is_literal_type(name):
        rlg__xtgo = get_literal_value(name)
    else:
        raise_bodo_error(yadw__vpqh)
    rlg__xtgo = 0 if rlg__xtgo is None else rlg__xtgo
    nvqdv__jlgon = ColNamesMetaType((rlg__xtgo,))

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            nvqdv__jlgon)
    return impl


@overload_method(SeriesType, 'keys', inline='always', no_unliteral=True)
def overload_series_keys(S):

    def impl(S):
        return bodo.hiframes.pd_series_ext.get_series_index(S)
    return impl
