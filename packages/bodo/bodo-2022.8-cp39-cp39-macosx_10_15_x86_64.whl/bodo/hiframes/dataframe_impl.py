"""
Implementation of DataFrame attributes and methods using overload.
"""
import operator
import re
import warnings
from collections import namedtuple
from typing import Tuple
import numba
import numpy as np
import pandas as pd
from numba.core import cgutils, ir, types
from numba.core.imputils import RefType, impl_ret_borrowed, impl_ret_new_ref, iternext_impl, lower_builtin
from numba.core.ir_utils import mk_unique_var, next_label
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_getattr, models, overload, overload_attribute, overload_method, register_model, type_callable
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import _no_input, datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported, handle_inplace_df_type_change
from bodo.hiframes.pd_index_ext import DatetimeIndexType, RangeIndexType, StringIndexType, is_pd_index_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import SeriesType, if_series_to_array_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_type
from bodo.hiframes.rolling import is_supported_shift_array_type
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.hiframes.time_ext import TimeArrayType
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array, boolean_dtype
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils import tracing
from bodo.utils.transform import bodo_types_with_params, gen_const_tup, no_side_effect_call_tuples
from bodo.utils.typing import BodoError, BodoWarning, ColNamesMetaType, check_unsupported_args, dtype_to_array_type, ensure_constant_arg, ensure_constant_values, get_index_data_arr_types, get_index_names, get_literal_value, get_nullable_and_non_nullable_types, get_overload_const_bool, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_tuple, get_overload_constant_dict, get_overload_constant_series, is_common_scalar_dtype, is_literal_type, is_overload_bool, is_overload_bool_list, is_overload_constant_bool, is_overload_constant_dict, is_overload_constant_int, is_overload_constant_list, is_overload_constant_series, is_overload_constant_str, is_overload_constant_tuple, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_overload_zero, is_scalar_type, parse_dtype, raise_bodo_error, unliteral_val
from bodo.utils.utils import is_array_typ


@overload_attribute(DataFrameType, 'index', inline='always')
def overload_dataframe_index(df):
    return lambda df: bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)


def generate_col_to_index_func_text(col_names: Tuple):
    if all(isinstance(a, str) for a in col_names) or all(isinstance(a,
        bytes) for a in col_names):
        jzm__ajd = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return (
            f'bodo.hiframes.pd_index_ext.init_binary_str_index({jzm__ajd})\n')
    elif all(isinstance(a, (int, float)) for a in col_names):
        arr = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return f'bodo.hiframes.pd_index_ext.init_numeric_index({arr})\n'
    else:
        return f'bodo.hiframes.pd_index_ext.init_heter_index({col_names})\n'


@overload_attribute(DataFrameType, 'columns', inline='always')
def overload_dataframe_columns(df):
    pqp__oegav = 'def impl(df):\n'
    if df.has_runtime_cols:
        pqp__oegav += (
            '  return bodo.hiframes.pd_dataframe_ext.get_dataframe_column_names(df)\n'
            )
    else:
        vhf__nkezg = (bodo.hiframes.dataframe_impl.
            generate_col_to_index_func_text(df.columns))
        pqp__oegav += f'  return {vhf__nkezg}'
    xdkv__qiwz = {}
    exec(pqp__oegav, {'bodo': bodo}, xdkv__qiwz)
    impl = xdkv__qiwz['impl']
    return impl


@overload_attribute(DataFrameType, 'values')
def overload_dataframe_values(df):
    check_runtime_cols_unsupported(df, 'DataFrame.values')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.values')
    if not is_df_values_numpy_supported_dftyp(df):
        raise_bodo_error(
            'DataFrame.values: only supported for dataframes containing numeric values'
            )
    xhvv__qmpga = len(df.columns)
    ptd__tdzfa = set(i for i in range(xhvv__qmpga) if isinstance(df.data[i],
        IntegerArrayType))
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(i, '.astype(float)' if i in ptd__tdzfa else '') for i in
        range(xhvv__qmpga))
    pqp__oegav = 'def f(df):\n'.format()
    pqp__oegav += '    return np.stack(({},), 1)\n'.format(data_args)
    xdkv__qiwz = {}
    exec(pqp__oegav, {'bodo': bodo, 'np': np}, xdkv__qiwz)
    hjbyz__hqno = xdkv__qiwz['f']
    return hjbyz__hqno


@overload_method(DataFrameType, 'to_numpy', inline='always', no_unliteral=True)
def overload_dataframe_to_numpy(df, dtype=None, copy=False, na_value=_no_input
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.to_numpy()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.to_numpy()')
    if not is_df_values_numpy_supported_dftyp(df):
        raise_bodo_error(
            'DataFrame.to_numpy(): only supported for dataframes containing numeric values'
            )
    lzvl__ztj = {'dtype': dtype, 'na_value': na_value}
    iuc__bisq = {'dtype': None, 'na_value': _no_input}
    check_unsupported_args('DataFrame.to_numpy', lzvl__ztj, iuc__bisq,
        package_name='pandas', module_name='DataFrame')

    def impl(df, dtype=None, copy=False, na_value=_no_input):
        return df.values
    return impl


@overload_attribute(DataFrameType, 'ndim', inline='always')
def overload_dataframe_ndim(df):
    return lambda df: 2


@overload_attribute(DataFrameType, 'size')
def overload_dataframe_size(df):
    if df.has_runtime_cols:

        def impl(df):
            t = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            yuuzl__ppeib = bodo.hiframes.table.compute_num_runtime_columns(t)
            return yuuzl__ppeib * len(t)
        return impl
    ncols = len(df.columns)
    return lambda df: ncols * len(df)


@lower_getattr(DataFrameType, 'shape')
def lower_dataframe_shape(context, builder, typ, val):
    impl = overload_dataframe_shape(typ)
    return context.compile_internal(builder, impl, types.Tuple([types.int64,
        types.int64])(typ), (val,))


def overload_dataframe_shape(df):
    if df.has_runtime_cols:

        def impl(df):
            t = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            yuuzl__ppeib = bodo.hiframes.table.compute_num_runtime_columns(t)
            return len(t), yuuzl__ppeib
        return impl
    ncols = len(df.columns)
    return lambda df: (len(df), ncols)


@overload_attribute(DataFrameType, 'dtypes')
def overload_dataframe_dtypes(df):
    check_runtime_cols_unsupported(df, 'DataFrame.dtypes')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.dtypes')
    pqp__oegav = 'def impl(df):\n'
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype\n'
         for i in range(len(df.columns)))
    bbtc__gcgh = ',' if len(df.columns) == 1 else ''
    index = f'bodo.hiframes.pd_index_ext.init_heter_index({df.columns})'
    pqp__oegav += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}{bbtc__gcgh}), {index}, None)
"""
    xdkv__qiwz = {}
    exec(pqp__oegav, {'bodo': bodo}, xdkv__qiwz)
    impl = xdkv__qiwz['impl']
    return impl


@overload_attribute(DataFrameType, 'empty')
def overload_dataframe_empty(df):
    check_runtime_cols_unsupported(df, 'DataFrame.empty')
    if len(df.columns) == 0:
        return lambda df: True
    return lambda df: len(df) == 0


@overload_method(DataFrameType, 'assign', no_unliteral=True)
def overload_dataframe_assign(df, **kwargs):
    check_runtime_cols_unsupported(df, 'DataFrame.assign()')
    raise_bodo_error('Invalid df.assign() call')


@overload_method(DataFrameType, 'insert', no_unliteral=True)
def overload_dataframe_insert(df, loc, column, value, allow_duplicates=False):
    check_runtime_cols_unsupported(df, 'DataFrame.insert()')
    raise_bodo_error('Invalid df.insert() call')


def _get_dtype_str(dtype):
    if isinstance(dtype, types.Function):
        if dtype.key[0] == str:
            return "'str'"
        elif dtype.key[0] == float:
            return 'float'
        elif dtype.key[0] == int:
            return 'int'
        elif dtype.key[0] == bool:
            return 'bool'
        else:
            raise BodoError(f'invalid dtype: {dtype}')
    if type(dtype) in bodo.libs.int_arr_ext.pd_int_dtype_classes:
        return dtype.name
    if isinstance(dtype, types.DTypeSpec):
        dtype = dtype.dtype
    if isinstance(dtype, types.functions.NumberClass):
        return f"'{dtype.key}'"
    if isinstance(dtype, types.PyObject) or dtype in (object, 'object'):
        return "'object'"
    if dtype in (bodo.libs.str_arr_ext.string_dtype, pd.StringDtype()):
        return 'str'
    return f"'{dtype}'"


@overload_method(DataFrameType, 'astype', inline='always', no_unliteral=True)
def overload_dataframe_astype(df, dtype, copy=True, errors='raise',
    _bodo_nan_to_str=True, _bodo_object_typeref=None):
    check_runtime_cols_unsupported(df, 'DataFrame.astype()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.astype()')
    lzvl__ztj = {'copy': copy, 'errors': errors}
    iuc__bisq = {'copy': True, 'errors': 'raise'}
    check_unsupported_args('df.astype', lzvl__ztj, iuc__bisq, package_name=
        'pandas', module_name='DataFrame')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "DataFrame.astype(): 'dtype' when passed as string must be a constant value"
            )
    extra_globals = None
    header = """def impl(df, dtype, copy=True, errors='raise', _bodo_nan_to_str=True, _bodo_object_typeref=None):
"""
    if df.is_table_format:
        extra_globals = {}
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        dhh__ulow = []
    if _bodo_object_typeref is not None:
        assert isinstance(_bodo_object_typeref, types.TypeRef
            ), 'Bodo schema used in DataFrame.astype should be a TypeRef'
        ohh__tdyo = _bodo_object_typeref.instance_type
        assert isinstance(ohh__tdyo, DataFrameType
            ), 'Bodo schema used in DataFrame.astype is only supported for DataFrame schemas'
        if df.is_table_format:
            for i, name in enumerate(df.columns):
                if name in ohh__tdyo.column_index:
                    idx = ohh__tdyo.column_index[name]
                    arr_typ = ohh__tdyo.data[idx]
                else:
                    arr_typ = df.data[i]
                dhh__ulow.append(arr_typ)
        else:
            extra_globals = {}
            vrpek__ipa = {}
            for i, name in enumerate(ohh__tdyo.columns):
                arr_typ = ohh__tdyo.data[i]
                if isinstance(arr_typ, IntegerArrayType):
                    edqfy__fbek = bodo.libs.int_arr_ext.IntDtype(arr_typ.dtype)
                elif arr_typ == boolean_array:
                    edqfy__fbek = boolean_dtype
                else:
                    edqfy__fbek = arr_typ.dtype
                extra_globals[f'_bodo_schema{i}'] = edqfy__fbek
                vrpek__ipa[name] = f'_bodo_schema{i}'
            data_args = ', '.join(
                f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {vrpek__ipa[doowf__rqn]}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
                 if doowf__rqn in vrpek__ipa else
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
                 for i, doowf__rqn in enumerate(df.columns))
    elif is_overload_constant_dict(dtype) or is_overload_constant_series(dtype
        ):
        nbo__kjy = get_overload_constant_dict(dtype
            ) if is_overload_constant_dict(dtype) else dict(
            get_overload_constant_series(dtype))
        if df.is_table_format:
            nbo__kjy = {name: dtype_to_array_type(parse_dtype(dtype)) for 
                name, dtype in nbo__kjy.items()}
            for i, name in enumerate(df.columns):
                if name in nbo__kjy:
                    arr_typ = nbo__kjy[name]
                else:
                    arr_typ = df.data[i]
                dhh__ulow.append(arr_typ)
        else:
            data_args = ', '.join(
                f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {_get_dtype_str(nbo__kjy[doowf__rqn])}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
                 if doowf__rqn in nbo__kjy else
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
                 for i, doowf__rqn in enumerate(df.columns))
    elif df.is_table_format:
        arr_typ = dtype_to_array_type(parse_dtype(dtype))
        dhh__ulow = [arr_typ] * len(df.columns)
    else:
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dtype, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             for i in range(len(df.columns)))
    if df.is_table_format:
        dniln__axxju = bodo.TableType(tuple(dhh__ulow))
        extra_globals['out_table_typ'] = dniln__axxju
        data_args = (
            'bodo.utils.table_utils.table_astype(table, out_table_typ, copy, _bodo_nan_to_str)'
            )
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'copy', inline='always', no_unliteral=True)
def overload_dataframe_copy(df, deep=True):
    check_runtime_cols_unsupported(df, 'DataFrame.copy()')
    header = 'def impl(df, deep=True):\n'
    extra_globals = None
    if df.is_table_format:
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        tgwb__koitb = types.none
        extra_globals = {'output_arr_typ': tgwb__koitb}
        if is_overload_false(deep):
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + 'None, ' + 'output_arr_typ, ' + 'True)')
        elif is_overload_true(deep):
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + "'copy', " + 'output_arr_typ, ' + 'True)')
        else:
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + "'copy', " + 'output_arr_typ, ' +
                'True) if deep else bodo.utils.table_utils.generate_mappable_table_func('
                 + 'table, ' + 'None, ' + 'output_arr_typ, ' + 'True)')
    else:
        htzw__bmcah = []
        for i in range(len(df.columns)):
            arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
            if is_overload_true(deep):
                htzw__bmcah.append(arr + '.copy()')
            elif is_overload_false(deep):
                htzw__bmcah.append(arr)
            else:
                htzw__bmcah.append(f'{arr}.copy() if deep else {arr}')
        data_args = ', '.join(htzw__bmcah)
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'rename', inline='always', no_unliteral=True)
def overload_dataframe_rename(df, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False, level=None, errors='ignore',
    _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.rename()')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'rename')
    lzvl__ztj = {'index': index, 'level': level, 'errors': errors}
    iuc__bisq = {'index': None, 'level': None, 'errors': 'ignore'}
    check_unsupported_args('DataFrame.rename', lzvl__ztj, iuc__bisq,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_constant_bool(inplace):
        raise BodoError(
            "DataFrame.rename(): 'inplace' keyword only supports boolean constant assignment"
            )
    if not is_overload_none(mapper):
        if not is_overload_none(columns):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'mapper' and 'columns'"
                )
        if not (is_overload_constant_int(axis) and get_overload_const_int(
            axis) == 1):
            raise BodoError(
                "DataFrame.rename(): 'mapper' only supported with axis=1")
        if not is_overload_constant_dict(mapper):
            raise_bodo_error(
                "'mapper' argument to DataFrame.rename() should be a constant dictionary"
                )
        clayw__tvv = get_overload_constant_dict(mapper)
    elif not is_overload_none(columns):
        if not is_overload_none(axis):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'axis' and 'columns'")
        if not is_overload_constant_dict(columns):
            raise_bodo_error(
                "'columns' argument to DataFrame.rename() should be a constant dictionary"
                )
        clayw__tvv = get_overload_constant_dict(columns)
    else:
        raise_bodo_error(
            "DataFrame.rename(): must pass columns either via 'mapper' and 'axis'=1 or 'columns'"
            )
    cpp__birwo = tuple([clayw__tvv.get(df.columns[i], df.columns[i]) for i in
        range(len(df.columns))])
    header = """def impl(df, mapper=None, index=None, columns=None, axis=None, copy=True, inplace=False, level=None, errors='ignore', _bodo_transformed=False):
"""
    extra_globals = None
    fxs__xycvy = None
    if df.is_table_format:
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        fxs__xycvy = df.copy(columns=cpp__birwo)
        tgwb__koitb = types.none
        extra_globals = {'output_arr_typ': tgwb__koitb}
        if is_overload_false(copy):
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + 'None, ' + 'output_arr_typ, ' + 'True)')
        elif is_overload_true(copy):
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + "'copy', " + 'output_arr_typ, ' + 'True)')
        else:
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + "'copy', " + 'output_arr_typ, ' +
                'True) if copy else bodo.utils.table_utils.generate_mappable_table_func('
                 + 'table, ' + 'None, ' + 'output_arr_typ, ' + 'True)')
    else:
        htzw__bmcah = []
        for i in range(len(df.columns)):
            arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
            if is_overload_true(copy):
                htzw__bmcah.append(arr + '.copy()')
            elif is_overload_false(copy):
                htzw__bmcah.append(arr)
            else:
                htzw__bmcah.append(f'{arr}.copy() if copy else {arr}')
        data_args = ', '.join(htzw__bmcah)
    return _gen_init_df(header, cpp__birwo, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'filter', no_unliteral=True)
def overload_dataframe_filter(df, items=None, like=None, regex=None, axis=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.filter()')
    agnl__yxxj = not is_overload_none(items)
    tcki__wgxe = not is_overload_none(like)
    lbsb__irqm = not is_overload_none(regex)
    amso__naok = agnl__yxxj ^ tcki__wgxe ^ lbsb__irqm
    rvls__pgm = not (agnl__yxxj or tcki__wgxe or lbsb__irqm)
    if rvls__pgm:
        raise BodoError(
            'DataFrame.filter(): one of keyword arguments `items`, `like`, and `regex` must be supplied'
            )
    if not amso__naok:
        raise BodoError(
            'DataFrame.filter(): keyword arguments `items`, `like`, and `regex` are mutually exclusive'
            )
    if is_overload_none(axis):
        axis = 'columns'
    if is_overload_constant_str(axis):
        axis = get_overload_const_str(axis)
        if axis not in {'index', 'columns'}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either "index" or "columns" if string'
                )
        vxnw__ajt = 0 if axis == 'index' else 1
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
        if axis not in {0, 1}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either 0 or 1 if integer'
                )
        vxnw__ajt = axis
    else:
        raise_bodo_error(
            'DataFrame.filter(): keyword arguments `axis` must be constant string or integer'
            )
    assert vxnw__ajt in {0, 1}
    pqp__oegav = (
        'def impl(df, items=None, like=None, regex=None, axis=None):\n')
    if vxnw__ajt == 0:
        raise BodoError(
            'DataFrame.filter(): filtering based on index is not supported.')
    if vxnw__ajt == 1:
        vdvf__djfaf = []
        labcu__ygd = []
        sydj__rgiyp = []
        if agnl__yxxj:
            if is_overload_constant_list(items):
                eqat__dvr = get_overload_const_list(items)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'items' must be a list of constant strings."
                    )
        if tcki__wgxe:
            if is_overload_constant_str(like):
                trtnd__ptrn = get_overload_const_str(like)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'like' must be a constant string."
                    )
        if lbsb__irqm:
            if is_overload_constant_str(regex):
                ilz__erh = get_overload_const_str(regex)
                bet__lguyz = re.compile(ilz__erh)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'regex' must be a constant string."
                    )
        for i, doowf__rqn in enumerate(df.columns):
            if not is_overload_none(items
                ) and doowf__rqn in eqat__dvr or not is_overload_none(like
                ) and trtnd__ptrn in str(doowf__rqn) or not is_overload_none(
                regex) and bet__lguyz.search(str(doowf__rqn)):
                labcu__ygd.append(doowf__rqn)
                sydj__rgiyp.append(i)
        for i in sydj__rgiyp:
            var_name = f'data_{i}'
            vdvf__djfaf.append(var_name)
            pqp__oegav += f"""  {var_name} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})
"""
        data_args = ', '.join(vdvf__djfaf)
        return _gen_init_df(pqp__oegav, labcu__ygd, data_args)


@overload_method(DataFrameType, 'isna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'isnull', inline='always', no_unliteral=True)
def overload_dataframe_isna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.isna()')
    header = 'def impl(df):\n'
    extra_globals = None
    fxs__xycvy = None
    if df.is_table_format:
        tgwb__koitb = types.Array(types.bool_, 1, 'C')
        fxs__xycvy = DataFrameType(tuple([tgwb__koitb] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': tgwb__koitb}
        data_args = ('bodo.utils.table_utils.generate_mappable_table_func(' +
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), ' +
            "'bodo.libs.array_ops.array_op_isna', " + 'output_arr_typ, ' +
            'False)')
    else:
        data_args = ', '.join(
            f'bodo.libs.array_ops.array_op_isna(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'select_dtypes', inline='always',
    no_unliteral=True)
def overload_dataframe_select_dtypes(df, include=None, exclude=None):
    check_runtime_cols_unsupported(df, 'DataFrame.select_dtypes')
    hqmp__jbs = is_overload_none(include)
    ydbyh__msabq = is_overload_none(exclude)
    juz__exnpk = 'DataFrame.select_dtypes'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.select_dtypes()')
    if hqmp__jbs and ydbyh__msabq:
        raise_bodo_error(
            'DataFrame.select_dtypes() At least one of include or exclude must not be none'
            )

    def is_legal_input(elem):
        return is_overload_constant_str(elem) or isinstance(elem, types.
            DTypeSpec) or isinstance(elem, types.Function)
    if not hqmp__jbs:
        if is_overload_constant_list(include):
            include = get_overload_const_list(include)
            ofsec__pqltc = [dtype_to_array_type(parse_dtype(elem,
                juz__exnpk)) for elem in include]
        elif is_legal_input(include):
            ofsec__pqltc = [dtype_to_array_type(parse_dtype(include,
                juz__exnpk))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        ofsec__pqltc = get_nullable_and_non_nullable_types(ofsec__pqltc)
        qjjyw__btemz = tuple(doowf__rqn for i, doowf__rqn in enumerate(df.
            columns) if df.data[i] in ofsec__pqltc)
    else:
        qjjyw__btemz = df.columns
    if not ydbyh__msabq:
        if is_overload_constant_list(exclude):
            exclude = get_overload_const_list(exclude)
            jumz__ecrdz = [dtype_to_array_type(parse_dtype(elem, juz__exnpk
                )) for elem in exclude]
        elif is_legal_input(exclude):
            jumz__ecrdz = [dtype_to_array_type(parse_dtype(exclude,
                juz__exnpk))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        jumz__ecrdz = get_nullable_and_non_nullable_types(jumz__ecrdz)
        qjjyw__btemz = tuple(doowf__rqn for doowf__rqn in qjjyw__btemz if 
            df.data[df.column_index[doowf__rqn]] not in jumz__ecrdz)
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[doowf__rqn]})'
         for doowf__rqn in qjjyw__btemz)
    header = 'def impl(df, include=None, exclude=None):\n'
    return _gen_init_df(header, qjjyw__btemz, data_args)


@overload_method(DataFrameType, 'notna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'notnull', inline='always', no_unliteral=True)
def overload_dataframe_notna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.notna()')
    header = 'def impl(df):\n'
    extra_globals = None
    fxs__xycvy = None
    if df.is_table_format:
        tgwb__koitb = types.Array(types.bool_, 1, 'C')
        fxs__xycvy = DataFrameType(tuple([tgwb__koitb] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': tgwb__koitb}
        data_args = ('bodo.utils.table_utils.generate_mappable_table_func(' +
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), ' +
            "'~bodo.libs.array_ops.array_op_isna', " + 'output_arr_typ, ' +
            'False)')
    else:
        data_args = ', '.join(
            f'bodo.libs.array_ops.array_op_isna(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})) == False'
             for i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


def overload_dataframe_head(df, n=5):
    if df.is_table_format:
        data_args = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[:n]')
    else:
        data_args = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[:n]'
             for i in range(len(df.columns)))
    header = 'def impl(df, n=5):\n'
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[:n]'
    return _gen_init_df(header, df.columns, data_args, index)


@lower_builtin('df.head', DataFrameType, types.Integer)
@lower_builtin('df.head', DataFrameType, types.Omitted)
def dataframe_head_lower(context, builder, sig, args):
    impl = overload_dataframe_head(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'tail', inline='always', no_unliteral=True)
def overload_dataframe_tail(df, n=5):
    check_runtime_cols_unsupported(df, 'DataFrame.tail()')
    if not is_overload_int(n):
        raise BodoError("Dataframe.tail(): 'n' must be an Integer")
    if df.is_table_format:
        data_args = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[m:]')
    else:
        data_args = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[m:]'
             for i in range(len(df.columns)))
    header = 'def impl(df, n=5):\n'
    header += '  m = bodo.hiframes.series_impl.tail_slice(len(df), n)\n'
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[m:]'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'first', inline='always', no_unliteral=True)
def overload_dataframe_first(df, offset):
    check_runtime_cols_unsupported(df, 'DataFrame.first()')
    tza__iyaoo = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError(
            'DataFrame.first(): only supports a DatetimeIndex index')
    if types.unliteral(offset) not in tza__iyaoo:
        raise BodoError(
            "DataFrame.first(): 'offset' must be an string or DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.first()')
    index = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[:valid_entries]'
        )
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[:valid_entries]'
         for i in range(len(df.columns)))
    header = 'def impl(df, offset):\n'
    header += (
        '  df_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
        )
    header += '  if len(df_index):\n'
    header += '    start_date = df_index[0]\n'
    header += """    valid_entries = bodo.libs.array_kernels.get_valid_entries_from_date_offset(df_index, offset, start_date, False)
"""
    header += '  else:\n'
    header += '    valid_entries = 0\n'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'last', inline='always', no_unliteral=True)
def overload_dataframe_last(df, offset):
    check_runtime_cols_unsupported(df, 'DataFrame.last()')
    tza__iyaoo = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError('DataFrame.last(): only supports a DatetimeIndex index'
            )
    if types.unliteral(offset) not in tza__iyaoo:
        raise BodoError(
            "DataFrame.last(): 'offset' must be an string or DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.last()')
    index = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[len(df)-valid_entries:]'
        )
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[len(df)-valid_entries:]'
         for i in range(len(df.columns)))
    header = 'def impl(df, offset):\n'
    header += (
        '  df_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
        )
    header += '  if len(df_index):\n'
    header += '    final_date = df_index[-1]\n'
    header += """    valid_entries = bodo.libs.array_kernels.get_valid_entries_from_date_offset(df_index, offset, final_date, True)
"""
    header += '  else:\n'
    header += '    valid_entries = 0\n'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'to_string', no_unliteral=True)
def to_string_overload(df, buf=None, columns=None, col_space=None, header=
    True, index=True, na_rep='NaN', formatters=None, float_format=None,
    sparsify=None, index_names=True, justify=None, max_rows=None, min_rows=
    None, max_cols=None, show_dimensions=False, decimal='.', line_width=
    None, max_colwidth=None, encoding=None):
    check_runtime_cols_unsupported(df, 'DataFrame.to_string()')

    def impl(df, buf=None, columns=None, col_space=None, header=True, index
        =True, na_rep='NaN', formatters=None, float_format=None, sparsify=
        None, index_names=True, justify=None, max_rows=None, min_rows=None,
        max_cols=None, show_dimensions=False, decimal='.', line_width=None,
        max_colwidth=None, encoding=None):
        with numba.objmode(res='string'):
            res = df.to_string(buf=buf, columns=columns, col_space=
                col_space, header=header, index=index, na_rep=na_rep,
                formatters=formatters, float_format=float_format, sparsify=
                sparsify, index_names=index_names, justify=justify,
                max_rows=max_rows, min_rows=min_rows, max_cols=max_cols,
                show_dimensions=show_dimensions, decimal=decimal,
                line_width=line_width, max_colwidth=max_colwidth, encoding=
                encoding)
        return res
    return impl


@overload_method(DataFrameType, 'isin', inline='always', no_unliteral=True)
def overload_dataframe_isin(df, values):
    check_runtime_cols_unsupported(df, 'DataFrame.isin()')
    from bodo.utils.typing import is_iterable_type
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.isin()')
    pqp__oegav = 'def impl(df, values):\n'
    cphzn__qnk = {}
    ycjq__qnqlk = False
    if isinstance(values, DataFrameType):
        ycjq__qnqlk = True
        for i, doowf__rqn in enumerate(df.columns):
            if doowf__rqn in values.column_index:
                gqdrw__qctcr = 'val{}'.format(i)
                pqp__oegav += f"""  {gqdrw__qctcr} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(values, {values.column_index[doowf__rqn]})
"""
                cphzn__qnk[doowf__rqn] = gqdrw__qctcr
    elif is_iterable_type(values) and not isinstance(values, SeriesType):
        cphzn__qnk = {doowf__rqn: 'values' for doowf__rqn in df.columns}
    else:
        raise_bodo_error(f'pd.isin(): not supported for type {values}')
    data = []
    for i in range(len(df.columns)):
        gqdrw__qctcr = 'data{}'.format(i)
        pqp__oegav += (
            '  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})\n'
            .format(gqdrw__qctcr, i))
        data.append(gqdrw__qctcr)
    zbzw__fsew = ['out{}'.format(i) for i in range(len(df.columns))]
    hsy__gfd = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  m = len({1})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] == {1}[i] if i < m else False
"""
    rgt__hll = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] in {1}
"""
    dzrl__iolo = '  {} = np.zeros(len(df), np.bool_)\n'
    for i, (cname, htc__wnkgb) in enumerate(zip(df.columns, data)):
        if cname in cphzn__qnk:
            srqp__spuj = cphzn__qnk[cname]
            if ycjq__qnqlk:
                pqp__oegav += hsy__gfd.format(htc__wnkgb, srqp__spuj,
                    zbzw__fsew[i])
            else:
                pqp__oegav += rgt__hll.format(htc__wnkgb, srqp__spuj,
                    zbzw__fsew[i])
        else:
            pqp__oegav += dzrl__iolo.format(zbzw__fsew[i])
    return _gen_init_df(pqp__oegav, df.columns, ','.join(zbzw__fsew))


@overload_method(DataFrameType, 'abs', inline='always', no_unliteral=True)
def overload_dataframe_abs(df):
    check_runtime_cols_unsupported(df, 'DataFrame.abs()')
    for arr_typ in df.data:
        if not (isinstance(arr_typ.dtype, types.Number) or arr_typ.dtype ==
            bodo.timedelta64ns):
            raise_bodo_error(
                f'DataFrame.abs(): Only supported for numeric and Timedelta. Encountered array with dtype {arr_typ.dtype}'
                )
    xhvv__qmpga = len(df.columns)
    data_args = ', '.join(
        'np.abs(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
        .format(i) for i in range(xhvv__qmpga))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


def overload_dataframe_corr(df, method='pearson', min_periods=1):
    zwryx__tvat = [doowf__rqn for doowf__rqn, kucr__difwy in zip(df.columns,
        df.data) if bodo.utils.typing._is_pandas_numeric_dtype(kucr__difwy.
        dtype)]
    assert len(zwryx__tvat) != 0
    kuw__pav = ''
    if not any(kucr__difwy == types.float64 for kucr__difwy in df.data):
        kuw__pav = '.astype(np.float64)'
    tds__fmlu = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[doowf__rqn], '.astype(np.float64)' if 
        isinstance(df.data[df.column_index[doowf__rqn]], IntegerArrayType) or
        df.data[df.column_index[doowf__rqn]] == boolean_array else '') for
        doowf__rqn in zwryx__tvat)
    abdka__dflsk = 'np.stack(({},), 1){}'.format(tds__fmlu, kuw__pav)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(
        zwryx__tvat)))
    index = f'{generate_col_to_index_func_text(zwryx__tvat)}\n'
    header = "def impl(df, method='pearson', min_periods=1):\n"
    header += '  mat = {}\n'.format(abdka__dflsk)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 0, min_periods)\n'
    return _gen_init_df(header, zwryx__tvat, data_args, index)


@lower_builtin('df.corr', DataFrameType, types.VarArg(types.Any))
def dataframe_corr_lower(context, builder, sig, args):
    impl = overload_dataframe_corr(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'cov', inline='always', no_unliteral=True)
def overload_dataframe_cov(df, min_periods=None, ddof=1):
    check_runtime_cols_unsupported(df, 'DataFrame.cov()')
    fppl__hshwq = dict(ddof=ddof)
    eza__kshz = dict(ddof=1)
    check_unsupported_args('DataFrame.cov', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    vhy__svj = '1' if is_overload_none(min_periods) else 'min_periods'
    zwryx__tvat = [doowf__rqn for doowf__rqn, kucr__difwy in zip(df.columns,
        df.data) if bodo.utils.typing._is_pandas_numeric_dtype(kucr__difwy.
        dtype)]
    if len(zwryx__tvat) == 0:
        raise_bodo_error('DataFrame.cov(): requires non-empty dataframe')
    kuw__pav = ''
    if not any(kucr__difwy == types.float64 for kucr__difwy in df.data):
        kuw__pav = '.astype(np.float64)'
    tds__fmlu = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[doowf__rqn], '.astype(np.float64)' if 
        isinstance(df.data[df.column_index[doowf__rqn]], IntegerArrayType) or
        df.data[df.column_index[doowf__rqn]] == boolean_array else '') for
        doowf__rqn in zwryx__tvat)
    abdka__dflsk = 'np.stack(({},), 1){}'.format(tds__fmlu, kuw__pav)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(
        zwryx__tvat)))
    index = f'pd.Index({zwryx__tvat})\n'
    header = 'def impl(df, min_periods=None, ddof=1):\n'
    header += '  mat = {}\n'.format(abdka__dflsk)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 1, {})\n'.format(
        vhy__svj)
    return _gen_init_df(header, zwryx__tvat, data_args, index)


@overload_method(DataFrameType, 'count', inline='always', no_unliteral=True)
def overload_dataframe_count(df, axis=0, level=None, numeric_only=False):
    check_runtime_cols_unsupported(df, 'DataFrame.count()')
    fppl__hshwq = dict(axis=axis, level=level, numeric_only=numeric_only)
    eza__kshz = dict(axis=0, level=None, numeric_only=False)
    check_unsupported_args('DataFrame.count', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
         for i in range(len(df.columns)))
    pqp__oegav = 'def impl(df, axis=0, level=None, numeric_only=False):\n'
    pqp__oegav += '  data = np.array([{}])\n'.format(data_args)
    vhf__nkezg = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    pqp__oegav += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {vhf__nkezg})\n'
        )
    xdkv__qiwz = {}
    exec(pqp__oegav, {'bodo': bodo, 'np': np}, xdkv__qiwz)
    impl = xdkv__qiwz['impl']
    return impl


@overload_method(DataFrameType, 'nunique', inline='always', no_unliteral=True)
def overload_dataframe_nunique(df, axis=0, dropna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.unique()')
    fppl__hshwq = dict(axis=axis)
    eza__kshz = dict(axis=0)
    if not is_overload_bool(dropna):
        raise BodoError('DataFrame.nunique: dropna must be a boolean value')
    check_unsupported_args('DataFrame.nunique', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_kernels.nunique(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dropna)'
         for i in range(len(df.columns)))
    pqp__oegav = 'def impl(df, axis=0, dropna=True):\n'
    pqp__oegav += '  data = np.asarray(({},))\n'.format(data_args)
    vhf__nkezg = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    pqp__oegav += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {vhf__nkezg})\n'
        )
    xdkv__qiwz = {}
    exec(pqp__oegav, {'bodo': bodo, 'np': np}, xdkv__qiwz)
    impl = xdkv__qiwz['impl']
    return impl


@overload_method(DataFrameType, 'prod', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'product', inline='always', no_unliteral=True)
def overload_dataframe_prod(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.prod()')
    fppl__hshwq = dict(skipna=skipna, level=level, numeric_only=
        numeric_only, min_count=min_count)
    eza__kshz = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.prod', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.product()')
    return _gen_reduce_impl(df, 'prod', axis=axis)


@overload_method(DataFrameType, 'sum', inline='always', no_unliteral=True)
def overload_dataframe_sum(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.sum()')
    fppl__hshwq = dict(skipna=skipna, level=level, numeric_only=
        numeric_only, min_count=min_count)
    eza__kshz = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.sum', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sum()')
    return _gen_reduce_impl(df, 'sum', axis=axis)


@overload_method(DataFrameType, 'max', inline='always', no_unliteral=True)
def overload_dataframe_max(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.max()')
    fppl__hshwq = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    eza__kshz = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.max', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.max()')
    return _gen_reduce_impl(df, 'max', axis=axis)


@overload_method(DataFrameType, 'min', inline='always', no_unliteral=True)
def overload_dataframe_min(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.min()')
    fppl__hshwq = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    eza__kshz = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.min', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.min()')
    return _gen_reduce_impl(df, 'min', axis=axis)


@overload_method(DataFrameType, 'mean', inline='always', no_unliteral=True)
def overload_dataframe_mean(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.mean()')
    fppl__hshwq = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    eza__kshz = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.mean', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.mean()')
    return _gen_reduce_impl(df, 'mean', axis=axis)


@overload_method(DataFrameType, 'var', inline='always', no_unliteral=True)
def overload_dataframe_var(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.var()')
    fppl__hshwq = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    eza__kshz = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.var', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.var()')
    return _gen_reduce_impl(df, 'var', axis=axis)


@overload_method(DataFrameType, 'std', inline='always', no_unliteral=True)
def overload_dataframe_std(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.std()')
    fppl__hshwq = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    eza__kshz = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.std', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.std()')
    return _gen_reduce_impl(df, 'std', axis=axis)


@overload_method(DataFrameType, 'median', inline='always', no_unliteral=True)
def overload_dataframe_median(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.median()')
    fppl__hshwq = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    eza__kshz = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.median', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.median()')
    return _gen_reduce_impl(df, 'median', axis=axis)


@overload_method(DataFrameType, 'quantile', inline='always', no_unliteral=True)
def overload_dataframe_quantile(df, q=0.5, axis=0, numeric_only=True,
    interpolation='linear'):
    check_runtime_cols_unsupported(df, 'DataFrame.quantile()')
    fppl__hshwq = dict(numeric_only=numeric_only, interpolation=interpolation)
    eza__kshz = dict(numeric_only=True, interpolation='linear')
    check_unsupported_args('DataFrame.quantile', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.quantile()')
    return _gen_reduce_impl(df, 'quantile', 'q', axis=axis)


@overload_method(DataFrameType, 'idxmax', inline='always', no_unliteral=True)
def overload_dataframe_idxmax(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmax()')
    fppl__hshwq = dict(axis=axis, skipna=skipna)
    eza__kshz = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmax', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmax()')
    for ifg__ifvli in df.data:
        if not (bodo.utils.utils.is_np_array_typ(ifg__ifvli) and (
            ifg__ifvli.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(ifg__ifvli.dtype, (types.Number, types.Boolean))) or
            isinstance(ifg__ifvli, (bodo.IntegerArrayType, bodo.
            CategoricalArrayType)) or ifg__ifvli in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmax() only supported for numeric column types. Column type: {ifg__ifvli} not supported.'
                )
        if isinstance(ifg__ifvli, bodo.CategoricalArrayType
            ) and not ifg__ifvli.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmax(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmax', axis=axis)


@overload_method(DataFrameType, 'idxmin', inline='always', no_unliteral=True)
def overload_dataframe_idxmin(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmin()')
    fppl__hshwq = dict(axis=axis, skipna=skipna)
    eza__kshz = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmin', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmin()')
    for ifg__ifvli in df.data:
        if not (bodo.utils.utils.is_np_array_typ(ifg__ifvli) and (
            ifg__ifvli.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(ifg__ifvli.dtype, (types.Number, types.Boolean))) or
            isinstance(ifg__ifvli, (bodo.IntegerArrayType, bodo.
            CategoricalArrayType)) or ifg__ifvli in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmin() only supported for numeric column types. Column type: {ifg__ifvli} not supported.'
                )
        if isinstance(ifg__ifvli, bodo.CategoricalArrayType
            ) and not ifg__ifvli.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmin(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmin', axis=axis)


@overload_method(DataFrameType, 'infer_objects', inline='always')
def overload_dataframe_infer_objects(df):
    check_runtime_cols_unsupported(df, 'DataFrame.infer_objects()')
    return lambda df: df.copy()


def _gen_reduce_impl(df, func_name, args=None, axis=None):
    args = '' if is_overload_none(args) else args
    if is_overload_none(axis):
        axis = 0
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
    else:
        raise_bodo_error(
            f'DataFrame.{func_name}: axis must be a constant Integer')
    assert axis in (0, 1), f'invalid axis argument for DataFrame.{func_name}'
    if func_name in ('idxmax', 'idxmin'):
        out_colnames = df.columns
    else:
        zwryx__tvat = tuple(doowf__rqn for doowf__rqn, kucr__difwy in zip(
            df.columns, df.data) if bodo.utils.typing.
            _is_pandas_numeric_dtype(kucr__difwy.dtype))
        out_colnames = zwryx__tvat
    assert len(out_colnames) != 0
    try:
        if func_name in ('idxmax', 'idxmin') and axis == 0:
            comm_dtype = None
        else:
            jhq__swvkm = [numba.np.numpy_support.as_dtype(df.data[df.
                column_index[doowf__rqn]].dtype) for doowf__rqn in out_colnames
                ]
            comm_dtype = numba.np.numpy_support.from_dtype(np.
                find_common_type(jhq__swvkm, []))
    except NotImplementedError as lnz__oijj:
        raise BodoError(
            f'Dataframe.{func_name}() with column types: {df.data} could not be merged to a common type.'
            )
    nxp__nvsem = ''
    if func_name in ('sum', 'prod'):
        nxp__nvsem = ', min_count=0'
    ddof = ''
    if func_name in ('var', 'std'):
        ddof = 'ddof=1, '
    pqp__oegav = (
        'def impl(df, axis=None, skipna=None, level=None,{} numeric_only=None{}):\n'
        .format(ddof, nxp__nvsem))
    if func_name == 'quantile':
        pqp__oegav = (
            "def impl(df, q=0.5, axis=0, numeric_only=True, interpolation='linear'):\n"
            )
    if func_name in ('idxmax', 'idxmin'):
        pqp__oegav = 'def impl(df, axis=0, skipna=True):\n'
    if axis == 0:
        pqp__oegav += _gen_reduce_impl_axis0(df, func_name, out_colnames,
            comm_dtype, args)
    else:
        pqp__oegav += _gen_reduce_impl_axis1(func_name, out_colnames,
            comm_dtype, df)
    xdkv__qiwz = {}
    exec(pqp__oegav, {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba},
        xdkv__qiwz)
    impl = xdkv__qiwz['impl']
    return impl


def _gen_reduce_impl_axis0(df, func_name, out_colnames, comm_dtype, args):
    nycak__bhl = ''
    if func_name in ('min', 'max'):
        nycak__bhl = ', dtype=np.{}'.format(comm_dtype)
    if comm_dtype == types.float32 and func_name in ('sum', 'prod', 'mean',
        'var', 'std', 'median'):
        nycak__bhl = ', dtype=np.float32'
    rzjar__fnbi = f'bodo.libs.array_ops.array_op_{func_name}'
    cjsk__tmbh = ''
    if func_name in ['sum', 'prod']:
        cjsk__tmbh = 'True, min_count'
    elif func_name in ['idxmax', 'idxmin']:
        cjsk__tmbh = 'index'
    elif func_name == 'quantile':
        cjsk__tmbh = 'q'
    elif func_name in ['std', 'var']:
        cjsk__tmbh = 'True, ddof'
    elif func_name == 'median':
        cjsk__tmbh = 'True'
    data_args = ', '.join(
        f'{rzjar__fnbi}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[doowf__rqn]}), {cjsk__tmbh})'
         for doowf__rqn in out_colnames)
    pqp__oegav = ''
    if func_name in ('idxmax', 'idxmin'):
        pqp__oegav += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        pqp__oegav += (
            '  data = bodo.utils.conversion.coerce_to_array(({},))\n'.
            format(data_args))
    else:
        pqp__oegav += '  data = np.asarray(({},){})\n'.format(data_args,
            nycak__bhl)
    pqp__oegav += f"""  return bodo.hiframes.pd_series_ext.init_series(data, pd.Index({out_colnames}))
"""
    return pqp__oegav


def _gen_reduce_impl_axis1(func_name, out_colnames, comm_dtype, df_type):
    cioac__taf = [df_type.column_index[doowf__rqn] for doowf__rqn in
        out_colnames]
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    data_args = '\n    '.join(
        'arr_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
        .format(i) for i in cioac__taf)
    tjy__gjj = '\n        '.join(f'row[{i}] = arr_{cioac__taf[i]}[i]' for i in
        range(len(out_colnames)))
    assert len(data_args) > 0, f'empty dataframe in DataFrame.{func_name}()'
    cgq__rlcb = f'len(arr_{cioac__taf[0]})'
    midz__erp = {'max': 'np.nanmax', 'min': 'np.nanmin', 'sum': 'np.nansum',
        'prod': 'np.nanprod', 'mean': 'np.nanmean', 'median':
        'np.nanmedian', 'var': 'bodo.utils.utils.nanvar_ddof1', 'std':
        'bodo.utils.utils.nanstd_ddof1'}
    if func_name in midz__erp:
        omons__obe = midz__erp[func_name]
        zyhp__gxj = 'float64' if func_name in ['mean', 'median', 'std', 'var'
            ] else comm_dtype
        pqp__oegav = f"""
    {data_args}
    numba.parfors.parfor.init_prange()
    n = {cgq__rlcb}
    row = np.empty({len(out_colnames)}, np.{comm_dtype})
    A = np.empty(n, np.{zyhp__gxj})
    for i in numba.parfors.parfor.internal_prange(n):
        {tjy__gjj}
        A[i] = {omons__obe}(row)
    return bodo.hiframes.pd_series_ext.init_series(A, {index})
"""
        return pqp__oegav
    else:
        raise BodoError(f'DataFrame.{func_name}(): Not supported for axis=1')


@overload_method(DataFrameType, 'pct_change', inline='always', no_unliteral
    =True)
def overload_dataframe_pct_change(df, periods=1, fill_method='pad', limit=
    None, freq=None):
    check_runtime_cols_unsupported(df, 'DataFrame.pct_change()')
    fppl__hshwq = dict(fill_method=fill_method, limit=limit, freq=freq)
    eza__kshz = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('DataFrame.pct_change', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.pct_change()')
    data_args = ', '.join(
        f'bodo.hiframes.rolling.pct_change(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), periods, False)'
         for i in range(len(df.columns)))
    header = (
        "def impl(df, periods=1, fill_method='pad', limit=None, freq=None):\n")
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'cumprod', inline='always', no_unliteral=True)
def overload_dataframe_cumprod(df, axis=None, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.cumprod()')
    fppl__hshwq = dict(axis=axis, skipna=skipna)
    eza__kshz = dict(axis=None, skipna=True)
    check_unsupported_args('DataFrame.cumprod', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.cumprod()')
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).cumprod()'
         for i in range(len(df.columns)))
    header = 'def impl(df, axis=None, skipna=True):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'cumsum', inline='always', no_unliteral=True)
def overload_dataframe_cumsum(df, axis=None, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.cumsum()')
    fppl__hshwq = dict(skipna=skipna)
    eza__kshz = dict(skipna=True)
    check_unsupported_args('DataFrame.cumsum', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.cumsum()')
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).cumsum()'
         for i in range(len(df.columns)))
    header = 'def impl(df, axis=None, skipna=True):\n'
    return _gen_init_df(header, df.columns, data_args)


def _is_describe_type(data):
    return isinstance(data, IntegerArrayType) or isinstance(data, types.Array
        ) and isinstance(data.dtype, types.Number
        ) or data.dtype == bodo.datetime64ns


@overload_method(DataFrameType, 'describe', inline='always', no_unliteral=True)
def overload_dataframe_describe(df, percentiles=None, include=None, exclude
    =None, datetime_is_numeric=True):
    check_runtime_cols_unsupported(df, 'DataFrame.describe()')
    fppl__hshwq = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    eza__kshz = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('DataFrame.describe', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.describe()')
    zwryx__tvat = [doowf__rqn for doowf__rqn, kucr__difwy in zip(df.columns,
        df.data) if _is_describe_type(kucr__difwy)]
    if len(zwryx__tvat) == 0:
        raise BodoError('df.describe() only supports numeric columns')
    quq__jnkai = sum(df.data[df.column_index[doowf__rqn]].dtype == bodo.
        datetime64ns for doowf__rqn in zwryx__tvat)

    def _get_describe(col_ind):
        ubt__waphl = df.data[col_ind].dtype == bodo.datetime64ns
        if quq__jnkai and quq__jnkai != len(zwryx__tvat):
            if ubt__waphl:
                return f'des_{col_ind} + (np.nan,)'
            return (
                f'des_{col_ind}[:2] + des_{col_ind}[3:] + (des_{col_ind}[2],)')
        return f'des_{col_ind}'
    header = """def impl(df, percentiles=None, include=None, exclude=None, datetime_is_numeric=True):
"""
    for doowf__rqn in zwryx__tvat:
        col_ind = df.column_index[doowf__rqn]
        header += f"""  des_{col_ind} = bodo.libs.array_ops.array_op_describe(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {col_ind}))
"""
    data_args = ', '.join(_get_describe(df.column_index[doowf__rqn]) for
        doowf__rqn in zwryx__tvat)
    woajx__yfm = "['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']"
    if quq__jnkai == len(zwryx__tvat):
        woajx__yfm = "['count', 'mean', 'min', '25%', '50%', '75%', 'max']"
    elif quq__jnkai:
        woajx__yfm = (
            "['count', 'mean', 'min', '25%', '50%', '75%', 'max', 'std']")
    index = f'bodo.utils.conversion.convert_to_index({woajx__yfm})'
    return _gen_init_df(header, zwryx__tvat, data_args, index)


@overload_method(DataFrameType, 'take', inline='always', no_unliteral=True)
def overload_dataframe_take(df, indices, axis=0, convert=None, is_copy=True):
    check_runtime_cols_unsupported(df, 'DataFrame.take()')
    fppl__hshwq = dict(axis=axis, convert=convert, is_copy=is_copy)
    eza__kshz = dict(axis=0, convert=None, is_copy=True)
    check_unsupported_args('DataFrame.take', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[indices_t]'
        .format(i) for i in range(len(df.columns)))
    header = 'def impl(df, indices, axis=0, convert=None, is_copy=True):\n'
    header += (
        '  indices_t = bodo.utils.conversion.coerce_to_ndarray(indices)\n')
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[indices_t]'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'shift', inline='always', no_unliteral=True)
def overload_dataframe_shift(df, periods=1, freq=None, axis=0, fill_value=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.shift()')
    fppl__hshwq = dict(freq=freq, axis=axis, fill_value=fill_value)
    eza__kshz = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('DataFrame.shift', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.shift()')
    for idnl__ckkn in df.data:
        if not is_supported_shift_array_type(idnl__ckkn):
            raise BodoError(
                f'Dataframe.shift() column input type {idnl__ckkn.dtype} not supported yet.'
                )
    if not is_overload_int(periods):
        raise BodoError(
            "DataFrame.shift(): 'periods' input must be an integer.")
    data_args = ', '.join(
        f'bodo.hiframes.rolling.shift(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), periods, False)'
         for i in range(len(df.columns)))
    header = 'def impl(df, periods=1, freq=None, axis=0, fill_value=None):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'diff', inline='always', no_unliteral=True)
def overload_dataframe_diff(df, periods=1, axis=0):
    check_runtime_cols_unsupported(df, 'DataFrame.diff()')
    fppl__hshwq = dict(axis=axis)
    eza__kshz = dict(axis=0)
    check_unsupported_args('DataFrame.diff', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.diff()')
    for idnl__ckkn in df.data:
        if not (isinstance(idnl__ckkn, types.Array) and (isinstance(
            idnl__ckkn.dtype, types.Number) or idnl__ckkn.dtype == bodo.
            datetime64ns)):
            raise BodoError(
                f'DataFrame.diff() column input type {idnl__ckkn.dtype} not supported.'
                )
    if not is_overload_int(periods):
        raise BodoError("DataFrame.diff(): 'periods' input must be an integer."
            )
    header = 'def impl(df, periods=1, axis= 0):\n'
    for i in range(len(df.columns)):
        header += (
            f'  data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})\n'
            )
    data_args = ', '.join(
        f'bodo.hiframes.series_impl.dt64_arr_sub(data_{i}, bodo.hiframes.rolling.shift(data_{i}, periods, False))'
         if df.data[i] == types.Array(bodo.datetime64ns, 1, 'C') else
        f'data_{i} - bodo.hiframes.rolling.shift(data_{i}, periods, False)' for
        i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'explode', inline='always', no_unliteral=True)
def overload_dataframe_explode(df, column, ignore_index=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.explode()')
    uiahe__hsg = (
        "DataFrame.explode(): 'column' must a constant label or list of labels"
        )
    if not is_literal_type(column):
        raise_bodo_error(uiahe__hsg)
    if is_overload_constant_list(column) or is_overload_constant_tuple(column):
        vef__kra = get_overload_const_list(column)
    else:
        vef__kra = [get_literal_value(column)]
    jyvf__uno = [df.column_index[doowf__rqn] for doowf__rqn in vef__kra]
    for i in jyvf__uno:
        if not isinstance(df.data[i], ArrayItemArrayType) and df.data[i
            ].dtype != string_array_split_view_type:
            raise BodoError(
                f'DataFrame.explode(): columns must have array-like entries')
    n = len(df.columns)
    header = 'def impl(df, column, ignore_index=False):\n'
    header += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    header += '  index_arr = bodo.utils.conversion.index_to_array(index)\n'
    for i in range(n):
        header += (
            f'  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})\n'
            )
    header += (
        f'  counts = bodo.libs.array_kernels.get_arr_lens(data{jyvf__uno[0]})\n'
        )
    for i in range(n):
        if i in jyvf__uno:
            header += (
                f'  out_data{i} = bodo.libs.array_kernels.explode_no_index(data{i}, counts)\n'
                )
        else:
            header += (
                f'  out_data{i} = bodo.libs.array_kernels.repeat_kernel(data{i}, counts)\n'
                )
    header += (
        '  new_index = bodo.libs.array_kernels.repeat_kernel(index_arr, counts)\n'
        )
    data_args = ', '.join(f'out_data{i}' for i in range(n))
    index = 'bodo.utils.conversion.convert_to_index(new_index)'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'set_index', inline='always', no_unliteral=True
    )
def overload_dataframe_set_index(df, keys, drop=True, append=False, inplace
    =False, verify_integrity=False):
    check_runtime_cols_unsupported(df, 'DataFrame.set_index()')
    lzvl__ztj = {'inplace': inplace, 'append': append, 'verify_integrity':
        verify_integrity}
    iuc__bisq = {'inplace': False, 'append': False, 'verify_integrity': False}
    check_unsupported_args('DataFrame.set_index', lzvl__ztj, iuc__bisq,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_constant_str(keys):
        raise_bodo_error(
            "DataFrame.set_index(): 'keys' must be a constant string")
    col_name = get_overload_const_str(keys)
    col_ind = df.columns.index(col_name)
    header = """def impl(df, keys, drop=True, append=False, inplace=False, verify_integrity=False):
"""
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'.format(
        i) for i in range(len(df.columns)) if i != col_ind)
    columns = tuple(doowf__rqn for doowf__rqn in df.columns if doowf__rqn !=
        col_name)
    index = (
        'bodo.utils.conversion.index_from_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}), {})'
        .format(col_ind, f"'{col_name}'" if isinstance(col_name, str) else
        col_name))
    return _gen_init_df(header, columns, data_args, index)


@overload_method(DataFrameType, 'query', no_unliteral=True)
def overload_dataframe_query(df, expr, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.query()')
    lzvl__ztj = {'inplace': inplace}
    iuc__bisq = {'inplace': False}
    check_unsupported_args('query', lzvl__ztj, iuc__bisq, package_name=
        'pandas', module_name='DataFrame')
    if not isinstance(expr, (types.StringLiteral, types.UnicodeType)):
        raise BodoError('query(): expr argument should be a string')

    def impl(df, expr, inplace=False):
        vnx__hje = bodo.hiframes.pd_dataframe_ext.query_dummy(df, expr)
        return df[vnx__hje]
    return impl


@overload_method(DataFrameType, 'duplicated', inline='always', no_unliteral
    =True)
def overload_dataframe_duplicated(df, subset=None, keep='first'):
    check_runtime_cols_unsupported(df, 'DataFrame.duplicated()')
    lzvl__ztj = {'subset': subset, 'keep': keep}
    iuc__bisq = {'subset': None, 'keep': 'first'}
    check_unsupported_args('DataFrame.duplicated', lzvl__ztj, iuc__bisq,
        package_name='pandas', module_name='DataFrame')
    xhvv__qmpga = len(df.columns)
    pqp__oegav = "def impl(df, subset=None, keep='first'):\n"
    for i in range(xhvv__qmpga):
        pqp__oegav += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    sbvl__lbjtn = ', '.join(f'data_{i}' for i in range(xhvv__qmpga))
    sbvl__lbjtn += ',' if xhvv__qmpga == 1 else ''
    pqp__oegav += (
        f'  duplicated = bodo.libs.array_kernels.duplicated(({sbvl__lbjtn}))\n'
        )
    pqp__oegav += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    pqp__oegav += (
        '  return bodo.hiframes.pd_series_ext.init_series(duplicated, index)\n'
        )
    xdkv__qiwz = {}
    exec(pqp__oegav, {'bodo': bodo}, xdkv__qiwz)
    impl = xdkv__qiwz['impl']
    return impl


@overload_method(DataFrameType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_dataframe_drop_duplicates(df, subset=None, keep='first',
    inplace=False, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop_duplicates()')
    lzvl__ztj = {'keep': keep, 'inplace': inplace, 'ignore_index': ignore_index
        }
    iuc__bisq = {'keep': 'first', 'inplace': False, 'ignore_index': False}
    avve__mrv = []
    if is_overload_constant_list(subset):
        avve__mrv = get_overload_const_list(subset)
    elif is_overload_constant_str(subset):
        avve__mrv = [get_overload_const_str(subset)]
    elif is_overload_constant_int(subset):
        avve__mrv = [get_overload_const_int(subset)]
    elif not is_overload_none(subset):
        raise_bodo_error(
            'DataFrame.drop_duplicates(): subset must be a constant column name, constant list of column names or None'
            )
    xln__xzrzx = []
    for col_name in avve__mrv:
        if col_name not in df.column_index:
            raise BodoError(
                'DataFrame.drop_duplicates(): All subset columns must be found in the DataFrame.'
                 +
                f'Column {col_name} not found in DataFrame columns {df.columns}'
                )
        xln__xzrzx.append(df.column_index[col_name])
    check_unsupported_args('DataFrame.drop_duplicates', lzvl__ztj,
        iuc__bisq, package_name='pandas', module_name='DataFrame')
    npb__kvbjo = []
    if xln__xzrzx:
        for fydm__bww in xln__xzrzx:
            if isinstance(df.data[fydm__bww], bodo.MapArrayType):
                npb__kvbjo.append(df.columns[fydm__bww])
    else:
        for i, col_name in enumerate(df.columns):
            if isinstance(df.data[i], bodo.MapArrayType):
                npb__kvbjo.append(col_name)
    if npb__kvbjo:
        raise BodoError(
            f'DataFrame.drop_duplicates(): Columns {npb__kvbjo} ' +
            f'have dictionary types which cannot be used to drop duplicates. '
             +
            "Please consider using the 'subset' argument to skip these columns."
            )
    xhvv__qmpga = len(df.columns)
    rpz__yjebe = ['data_{}'.format(i) for i in xln__xzrzx]
    vmv__hkes = ['data_{}'.format(i) for i in range(xhvv__qmpga) if i not in
        xln__xzrzx]
    if rpz__yjebe:
        nkwdn__gauas = len(rpz__yjebe)
    else:
        nkwdn__gauas = xhvv__qmpga
    cciky__jvshb = ', '.join(rpz__yjebe + vmv__hkes)
    data_args = ', '.join('data_{}'.format(i) for i in range(xhvv__qmpga))
    pqp__oegav = (
        "def impl(df, subset=None, keep='first', inplace=False, ignore_index=False):\n"
        )
    for i in range(xhvv__qmpga):
        pqp__oegav += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    pqp__oegav += (
        """  ({0},), index_arr = bodo.libs.array_kernels.drop_duplicates(({0},), {1}, {2})
"""
        .format(cciky__jvshb, index, nkwdn__gauas))
    pqp__oegav += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(pqp__oegav, df.columns, data_args, 'index')


def create_dataframe_mask_where_overload(func_name):

    def overload_dataframe_mask_where(df, cond, other=np.nan, inplace=False,
        axis=None, level=None, errors='raise', try_cast=False):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
            f'DataFrame.{func_name}()')
        _validate_arguments_mask_where(f'DataFrame.{func_name}', df, cond,
            other, inplace, axis, level, errors, try_cast)
        header = """def impl(df, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise', try_cast=False):
"""
        if func_name == 'mask':
            header += '  cond = ~cond\n'
        gen_all_false = [False]
        if cond.ndim == 1:
            cond_str = lambda i, _: 'cond'
        elif cond.ndim == 2:
            if isinstance(cond, DataFrameType):

                def cond_str(i, gen_all_false):
                    if df.columns[i] in cond.column_index:
                        return (
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(cond, {cond.column_index[df.columns[i]]})'
                            )
                    else:
                        gen_all_false[0] = True
                        return 'all_false'
            elif isinstance(cond, types.Array):
                cond_str = lambda i, _: f'cond[:,{i}]'
        if not hasattr(other, 'ndim') or other.ndim == 1:
            ydynd__hwj = lambda i: 'other'
        elif other.ndim == 2:
            if isinstance(other, DataFrameType):
                ydynd__hwj = (lambda i: 
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {other.column_index[df.columns[i]]})'
                     if df.columns[i] in other.column_index else 'None')
            elif isinstance(other, types.Array):
                ydynd__hwj = lambda i: f'other[:,{i}]'
        xhvv__qmpga = len(df.columns)
        data_args = ', '.join(
            f'bodo.hiframes.series_impl.where_impl({cond_str(i, gen_all_false)}, bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {ydynd__hwj(i)})'
             for i in range(xhvv__qmpga))
        if gen_all_false[0]:
            header += '  all_false = np.zeros(len(df), dtype=bool)\n'
        return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_mask_where


def _install_dataframe_mask_where_overload():
    for func_name in ('mask', 'where'):
        ahyu__ucxc = create_dataframe_mask_where_overload(func_name)
        overload_method(DataFrameType, func_name, no_unliteral=True)(ahyu__ucxc
            )


_install_dataframe_mask_where_overload()


def _validate_arguments_mask_where(func_name, df, cond, other, inplace,
    axis, level, errors, try_cast):
    fppl__hshwq = dict(inplace=inplace, level=level, errors=errors,
        try_cast=try_cast)
    eza__kshz = dict(inplace=False, level=None, errors='raise', try_cast=False)
    check_unsupported_args(f'{func_name}', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error(f'{func_name}(): axis argument not supported')
    if not (isinstance(cond, (SeriesType, types.Array, BooleanArrayType)) and
        (cond.ndim == 1 or cond.ndim == 2) and cond.dtype == types.bool_
        ) and not (isinstance(cond, DataFrameType) and cond.ndim == 2 and
        all(cond.data[i].dtype == types.bool_ for i in range(len(df.columns)))
        ):
        raise BodoError(
            f"{func_name}(): 'cond' argument must be a DataFrame, Series, 1- or 2-dimensional array of booleans"
            )
    xhvv__qmpga = len(df.columns)
    if hasattr(other, 'ndim') and (other.ndim != 1 or other.ndim != 2):
        if other.ndim == 2:
            if not isinstance(other, (DataFrameType, types.Array)):
                raise BodoError(
                    f"{func_name}(): 'other', if 2-dimensional, must be a DataFrame or array."
                    )
        elif other.ndim != 1:
            raise BodoError(
                f"{func_name}(): 'other' must be either 1 or 2-dimensional")
    if isinstance(other, DataFrameType):
        for i in range(xhvv__qmpga):
            if df.columns[i] in other.column_index:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, 'Series', df.data[i], other.data[other.
                    column_index[df.columns[i]]])
            else:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, 'Series', df.data[i], None, is_default=True)
    elif isinstance(other, SeriesType):
        for i in range(xhvv__qmpga):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , 'Series', df.data[i], other.data)
    else:
        for i in range(xhvv__qmpga):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , 'Series', df.data[i], other, max_ndim=2)


def _gen_init_df(header, columns, data_args, index=None, extra_globals=None):
    if index is None:
        index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    if extra_globals is None:
        extra_globals = {}
    bpwmz__cgw = ColNamesMetaType(tuple(columns))
    data_args = '({}{})'.format(data_args, ',' if data_args else '')
    pqp__oegav = f"""{header}  return bodo.hiframes.pd_dataframe_ext.init_dataframe({data_args}, {index}, __col_name_meta_value_gen_init_df)
"""
    xdkv__qiwz = {}
    enaw__yjmy = {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba,
        '__col_name_meta_value_gen_init_df': bpwmz__cgw}
    enaw__yjmy.update(extra_globals)
    exec(pqp__oegav, enaw__yjmy, xdkv__qiwz)
    impl = xdkv__qiwz['impl']
    return impl


def _get_binop_columns(lhs, rhs, is_inplace=False):
    if lhs.columns != rhs.columns:
        hmkw__ukvo = pd.Index(lhs.columns)
        mkb__wryd = pd.Index(rhs.columns)
        tbbsd__rxqtx, nevc__srget, gwc__zgfx = hmkw__ukvo.join(mkb__wryd,
            how='left' if is_inplace else 'outer', level=None,
            return_indexers=True)
        return tuple(tbbsd__rxqtx), nevc__srget, gwc__zgfx
    return lhs.columns, range(len(lhs.columns)), range(len(lhs.columns))


def create_binary_op_overload(op):

    def overload_dataframe_binary_op(lhs, rhs):
        nkb__mvs = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        uwng__nyn = operator.eq, operator.ne
        check_runtime_cols_unsupported(lhs, nkb__mvs)
        check_runtime_cols_unsupported(rhs, nkb__mvs)
        if isinstance(lhs, DataFrameType):
            if isinstance(rhs, DataFrameType):
                tbbsd__rxqtx, nevc__srget, gwc__zgfx = _get_binop_columns(lhs,
                    rhs)
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {kihtd__awri}) {nkb__mvs}bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {goq__zjb})'
                     if kihtd__awri != -1 and goq__zjb != -1 else
                    f'bodo.libs.array_kernels.gen_na_array(len(lhs), float64_arr_type)'
                     for kihtd__awri, goq__zjb in zip(nevc__srget, gwc__zgfx))
                header = 'def impl(lhs, rhs):\n'
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)')
                return _gen_init_df(header, tbbsd__rxqtx, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            elif isinstance(rhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            rmh__kfql = []
            zgnz__rtt = []
            if op in uwng__nyn:
                for i, aypp__veh in enumerate(lhs.data):
                    if is_common_scalar_dtype([aypp__veh.dtype, rhs]):
                        rmh__kfql.append(
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {nkb__mvs} rhs'
                            )
                    else:
                        gyoff__sjfy = f'arr{i}'
                        zgnz__rtt.append(gyoff__sjfy)
                        rmh__kfql.append(gyoff__sjfy)
                data_args = ', '.join(rmh__kfql)
            else:
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {nkb__mvs} rhs'
                     for i in range(len(lhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(zgnz__rtt) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(lhs)\n'
                header += ''.join(
                    f'  {gyoff__sjfy} = np.empty(n, dtype=np.bool_)\n' for
                    gyoff__sjfy in zgnz__rtt)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(gyoff__sjfy, 
                    op == operator.ne) for gyoff__sjfy in zgnz__rtt)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)'
            return _gen_init_df(header, lhs.columns, data_args, index)
        if isinstance(rhs, DataFrameType):
            if isinstance(lhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            rmh__kfql = []
            zgnz__rtt = []
            if op in uwng__nyn:
                for i, aypp__veh in enumerate(rhs.data):
                    if is_common_scalar_dtype([lhs, aypp__veh.dtype]):
                        rmh__kfql.append(
                            f'lhs {nkb__mvs} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {i})'
                            )
                    else:
                        gyoff__sjfy = f'arr{i}'
                        zgnz__rtt.append(gyoff__sjfy)
                        rmh__kfql.append(gyoff__sjfy)
                data_args = ', '.join(rmh__kfql)
            else:
                data_args = ', '.join(
                    'lhs {1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {0})'
                    .format(i, nkb__mvs) for i in range(len(rhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(zgnz__rtt) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(rhs)\n'
                header += ''.join('  {0} = np.empty(n, dtype=np.bool_)\n'.
                    format(gyoff__sjfy) for gyoff__sjfy in zgnz__rtt)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(gyoff__sjfy, 
                    op == operator.ne) for gyoff__sjfy in zgnz__rtt)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(rhs)'
            return _gen_init_df(header, rhs.columns, data_args, index)
    return overload_dataframe_binary_op


skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        ahyu__ucxc = create_binary_op_overload(op)
        overload(op)(ahyu__ucxc)


_install_binary_ops()


def create_inplace_binary_op_overload(op):

    def overload_dataframe_inplace_binary_op(left, right):
        nkb__mvs = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        check_runtime_cols_unsupported(left, nkb__mvs)
        check_runtime_cols_unsupported(right, nkb__mvs)
        if isinstance(left, DataFrameType):
            if isinstance(right, DataFrameType):
                tbbsd__rxqtx, _, gwc__zgfx = _get_binop_columns(left, right,
                    True)
                pqp__oegav = 'def impl(left, right):\n'
                for i, goq__zjb in enumerate(gwc__zgfx):
                    if goq__zjb == -1:
                        pqp__oegav += f"""  df_arr{i} = bodo.libs.array_kernels.gen_na_array(len(left), float64_arr_type)
"""
                        continue
                    pqp__oegav += f"""  df_arr{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {i})
"""
                    pqp__oegav += f"""  df_arr{i} {nkb__mvs} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(right, {goq__zjb})
"""
                data_args = ', '.join(f'df_arr{i}' for i in range(len(
                    tbbsd__rxqtx)))
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)')
                return _gen_init_df(pqp__oegav, tbbsd__rxqtx, data_args,
                    index, extra_globals={'float64_arr_type': types.Array(
                    types.float64, 1, 'C')})
            pqp__oegav = 'def impl(left, right):\n'
            for i in range(len(left.columns)):
                pqp__oegav += (
                    """  df_arr{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {0})
"""
                    .format(i))
                pqp__oegav += '  df_arr{0} {1} right\n'.format(i, nkb__mvs)
            data_args = ', '.join('df_arr{}'.format(i) for i in range(len(
                left.columns)))
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)'
            return _gen_init_df(pqp__oegav, left.columns, data_args, index)
    return overload_dataframe_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        ahyu__ucxc = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(ahyu__ucxc)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_dataframe_unary_op(df):
        if isinstance(df, DataFrameType):
            nkb__mvs = numba.core.utils.OPERATORS_TO_BUILTINS[op]
            check_runtime_cols_unsupported(df, nkb__mvs)
            data_args = ', '.join(
                '{1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
                .format(i, nkb__mvs) for i in range(len(df.columns)))
            header = 'def impl(df):\n'
            return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        ahyu__ucxc = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(ahyu__ucxc)


_install_unary_ops()


def overload_isna(obj):
    check_runtime_cols_unsupported(obj, 'pd.isna()')
    if isinstance(obj, (DataFrameType, SeriesType)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj):
        return lambda obj: obj.isna()
    if is_array_typ(obj):

        def impl(obj):
            numba.parfors.parfor.init_prange()
            n = len(obj)
            apnyc__teeh = np.empty(n, np.bool_)
            for i in numba.parfors.parfor.internal_prange(n):
                apnyc__teeh[i] = bodo.libs.array_kernels.isna(obj, i)
            return apnyc__teeh
        return impl


overload(pd.isna, inline='always')(overload_isna)
overload(pd.isnull, inline='always')(overload_isna)


@overload(pd.isna)
@overload(pd.isnull)
def overload_isna_scalar(obj):
    if isinstance(obj, (DataFrameType, SeriesType)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj) or is_array_typ(
        obj):
        return
    if isinstance(obj, (types.List, types.UniTuple)):

        def impl(obj):
            n = len(obj)
            apnyc__teeh = np.empty(n, np.bool_)
            for i in range(n):
                apnyc__teeh[i] = pd.isna(obj[i])
            return apnyc__teeh
        return impl
    obj = types.unliteral(obj)
    if obj == bodo.string_type:
        return lambda obj: unliteral_val(False)
    if isinstance(obj, types.Integer):
        return lambda obj: unliteral_val(False)
    if isinstance(obj, types.Float):
        return lambda obj: np.isnan(obj)
    if isinstance(obj, (types.NPDatetime, types.NPTimedelta)):
        return lambda obj: np.isnat(obj)
    if obj == types.none:
        return lambda obj: unliteral_val(True)
    if isinstance(obj, bodo.hiframes.pd_timestamp_ext.PandasTimestampType):
        return lambda obj: np.isnat(bodo.hiframes.pd_timestamp_ext.
            integer_to_dt64(obj.value))
    if obj == bodo.hiframes.datetime_timedelta_ext.pd_timedelta_type:
        return lambda obj: np.isnat(bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(obj.value))
    if isinstance(obj, types.Optional):
        return lambda obj: obj is None
    return lambda obj: unliteral_val(False)


@overload(operator.setitem, no_unliteral=True)
def overload_setitem_arr_none(A, idx, val):
    if is_array_typ(A, False) and isinstance(idx, types.Integer
        ) and val == types.none:
        return lambda A, idx, val: bodo.libs.array_kernels.setna(A, idx)


def overload_notna(obj):
    check_runtime_cols_unsupported(obj, 'pd.notna()')
    if isinstance(obj, (DataFrameType, SeriesType)):
        return lambda obj: obj.notna()
    if isinstance(obj, (types.List, types.UniTuple)) or is_array_typ(obj,
        include_index_series=True):
        return lambda obj: ~pd.isna(obj)
    return lambda obj: not pd.isna(obj)


overload(pd.notna, inline='always', no_unliteral=True)(overload_notna)
overload(pd.notnull, inline='always', no_unliteral=True)(overload_notna)


def _get_pd_dtype_str(t):
    if t.dtype == types.NPDatetime('ns'):
        return "'datetime64[ns]'"
    return bodo.ir.csv_ext._get_pd_dtype_str(t)


@overload_method(DataFrameType, 'replace', inline='always', no_unliteral=True)
def overload_dataframe_replace(df, to_replace=None, value=None, inplace=
    False, limit=None, regex=False, method='pad'):
    check_runtime_cols_unsupported(df, 'DataFrame.replace()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.replace()')
    if is_overload_none(to_replace):
        raise BodoError('replace(): to_replace value of None is not supported')
    lzvl__ztj = {'inplace': inplace, 'limit': limit, 'regex': regex,
        'method': method}
    iuc__bisq = {'inplace': False, 'limit': None, 'regex': False, 'method':
        'pad'}
    check_unsupported_args('replace', lzvl__ztj, iuc__bisq, package_name=
        'pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'df.iloc[:, {i}].replace(to_replace, value).values' for i in range
        (len(df.columns)))
    header = """def impl(df, to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad'):
"""
    return _gen_init_df(header, df.columns, data_args)


def _is_col_access(expr_node):
    seb__mfx = str(expr_node)
    return seb__mfx.startswith('left.') or seb__mfx.startswith('right.')


def _insert_NA_cond(expr_node, left_columns, left_data, right_columns,
    right_data):
    sjeqs__zrk = {'left': 0, 'right': 0, 'NOT_NA': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (sjeqs__zrk,))
    kyn__nser = pd.core.computation.parsing.clean_column_name

    def append_null_checks(expr_node, null_set):
        if not null_set:
            return expr_node
        bipu__lxs = ' & '.join([('NOT_NA.`' + x + '`') for x in null_set])
        joq__tdjgt = {('NOT_NA', kyn__nser(aypp__veh)): aypp__veh for
            aypp__veh in null_set}
        jwwpw__iocd, _, _ = _parse_query_expr(bipu__lxs, env, [], [], None,
            join_cleaned_cols=joq__tdjgt)
        cpieb__fagf = (pd.core.computation.ops.BinOp.
            _disallow_scalar_only_bool_ops)
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        try:
            ochn__cyjs = pd.core.computation.ops.BinOp('&', jwwpw__iocd,
                expr_node)
        finally:
            (pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
                ) = cpieb__fagf
        return ochn__cyjs

    def _insert_NA_cond_body(expr_node, null_set):
        if isinstance(expr_node, pd.core.computation.ops.BinOp):
            if expr_node.op == '|':
                ywgmp__hpyiw = set()
                tgsg__xjqpi = set()
                fmf__bjjki = _insert_NA_cond_body(expr_node.lhs, ywgmp__hpyiw)
                zev__cdi = _insert_NA_cond_body(expr_node.rhs, tgsg__xjqpi)
                vjg__sri = ywgmp__hpyiw.intersection(tgsg__xjqpi)
                ywgmp__hpyiw.difference_update(vjg__sri)
                tgsg__xjqpi.difference_update(vjg__sri)
                null_set.update(vjg__sri)
                expr_node.lhs = append_null_checks(fmf__bjjki, ywgmp__hpyiw)
                expr_node.rhs = append_null_checks(zev__cdi, tgsg__xjqpi)
                expr_node.operands = expr_node.lhs, expr_node.rhs
            else:
                expr_node.lhs = _insert_NA_cond_body(expr_node.lhs, null_set)
                expr_node.rhs = _insert_NA_cond_body(expr_node.rhs, null_set)
        elif _is_col_access(expr_node):
            ziacf__zsdok = expr_node.name
            kng__tdo, col_name = ziacf__zsdok.split('.')
            if kng__tdo == 'left':
                phwr__rjbn = left_columns
                data = left_data
            else:
                phwr__rjbn = right_columns
                data = right_data
            vtc__bqhr = data[phwr__rjbn.index(col_name)]
            if bodo.utils.typing.is_nullable(vtc__bqhr):
                null_set.add(expr_node.name)
        return expr_node
    null_set = set()
    pyv__bkcx = _insert_NA_cond_body(expr_node, null_set)
    return append_null_checks(expr_node, null_set)


def _extract_equal_conds(expr_node):
    if not hasattr(expr_node, 'op'):
        return [], [], expr_node
    if expr_node.op == '==' and _is_col_access(expr_node.lhs
        ) and _is_col_access(expr_node.rhs):
        egvk__hnxxh = str(expr_node.lhs)
        gpuxg__htz = str(expr_node.rhs)
        if egvk__hnxxh.startswith('left.') and gpuxg__htz.startswith('left.'
            ) or egvk__hnxxh.startswith('right.') and gpuxg__htz.startswith(
            'right.'):
            return [], [], expr_node
        left_on = [egvk__hnxxh.split('.')[1]]
        right_on = [gpuxg__htz.split('.')[1]]
        if egvk__hnxxh.startswith('right.'):
            return right_on, left_on, None
        return left_on, right_on, None
    if expr_node.op == '&':
        mnhk__dvkz, mofcr__laby, gcmg__vtsbv = _extract_equal_conds(expr_node
            .lhs)
        kbts__rbegn, hnq__uxs, lgqxg__wpawv = _extract_equal_conds(expr_node
            .rhs)
        left_on = mnhk__dvkz + kbts__rbegn
        right_on = mofcr__laby + hnq__uxs
        if gcmg__vtsbv is None:
            return left_on, right_on, lgqxg__wpawv
        if lgqxg__wpawv is None:
            return left_on, right_on, gcmg__vtsbv
        expr_node.lhs = gcmg__vtsbv
        expr_node.rhs = lgqxg__wpawv
        expr_node.operands = expr_node.lhs, expr_node.rhs
        return left_on, right_on, expr_node
    return [], [], expr_node


def _parse_merge_cond(on_str, left_columns, left_data, right_columns,
    right_data):
    sjeqs__zrk = {'left': 0, 'right': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (sjeqs__zrk,))
    clayw__tvv = dict()
    kyn__nser = pd.core.computation.parsing.clean_column_name
    for name, eepn__shozk in (('left', left_columns), ('right', right_columns)
        ):
        for aypp__veh in eepn__shozk:
            fzfb__alh = kyn__nser(aypp__veh)
            xgv__xqd = name, fzfb__alh
            if xgv__xqd in clayw__tvv:
                raise_bodo_error(
                    f"pd.merge(): {name} table contains two columns that are escaped to the same Python identifier '{aypp__veh}' and '{clayw__tvv[fzfb__alh]}' Please rename one of these columns. To avoid this issue, please use names that are valid Python identifiers."
                    )
            clayw__tvv[xgv__xqd] = aypp__veh
    fhnnd__lxl, _, _ = _parse_query_expr(on_str, env, [], [], None,
        join_cleaned_cols=clayw__tvv)
    left_on, right_on, jwego__vxxcm = _extract_equal_conds(fhnnd__lxl.terms)
    return left_on, right_on, _insert_NA_cond(jwego__vxxcm, left_columns,
        left_data, right_columns, right_data)


@overload_method(DataFrameType, 'merge', inline='always', no_unliteral=True)
@overload(pd.merge, inline='always', no_unliteral=True)
def overload_dataframe_merge(left, right, how='inner', on=None, left_on=
    None, right_on=None, left_index=False, right_index=False, sort=False,
    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None,
    _bodo_na_equal=True):
    check_runtime_cols_unsupported(left, 'DataFrame.merge()')
    check_runtime_cols_unsupported(right, 'DataFrame.merge()')
    fppl__hshwq = dict(sort=sort, copy=copy, validate=validate)
    eza__kshz = dict(sort=False, copy=True, validate=None)
    check_unsupported_args('DataFrame.merge', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
        right_index, sort, suffixes, copy, indicator, validate)
    how = get_overload_const_str(how)
    vkrwa__xvcpz = tuple(sorted(set(left.columns) & set(right.columns), key
        =lambda k: str(k)))
    txg__ogr = ''
    if not is_overload_none(on):
        left_on = right_on = on
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            if on_str not in vkrwa__xvcpz and ('left.' in on_str or 
                'right.' in on_str):
                left_on, right_on, rhwv__zsmqt = _parse_merge_cond(on_str,
                    left.columns, left.data, right.columns, right.data)
                if rhwv__zsmqt is None:
                    txg__ogr = ''
                else:
                    txg__ogr = str(rhwv__zsmqt)
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = vkrwa__xvcpz
        right_keys = vkrwa__xvcpz
    else:
        if is_overload_true(left_index):
            left_keys = ['$_bodo_index_']
        else:
            left_keys = get_overload_const_list(left_on)
            validate_keys(left_keys, left)
        if is_overload_true(right_index):
            right_keys = ['$_bodo_index_']
        else:
            right_keys = get_overload_const_list(right_on)
            validate_keys(right_keys, right)
    if (not left_on or not right_on) and not is_overload_none(on):
        raise BodoError(
            f"DataFrame.merge(): Merge condition '{get_overload_const_str(on)}' requires a cross join to implement, but cross join is not supported."
            )
    if not is_overload_bool(indicator):
        raise_bodo_error(
            'DataFrame.merge(): indicator must be a constant boolean')
    indicator_val = get_overload_const_bool(indicator)
    if not is_overload_bool(_bodo_na_equal):
        raise_bodo_error(
            'DataFrame.merge(): bodo extension _bodo_na_equal must be a constant boolean'
            )
    xfo__whs = get_overload_const_bool(_bodo_na_equal)
    validate_keys_length(left_index, right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    if is_overload_constant_tuple(suffixes):
        bjzat__mang = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        bjzat__mang = list(get_overload_const_list(suffixes))
    suffix_x = bjzat__mang[0]
    suffix_y = bjzat__mang[1]
    validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
        right_keys, left.columns, right.columns, indicator_val)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    pqp__oegav = "def _impl(left, right, how='inner', on=None, left_on=None,\n"
    pqp__oegav += (
        '    right_on=None, left_index=False, right_index=False, sort=False,\n'
        )
    pqp__oegav += """    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None, _bodo_na_equal=True):
"""
    pqp__oegav += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, '{}', '{}', '{}', False, {}, {}, '{}')
"""
        .format(left_keys, right_keys, how, suffix_x, suffix_y,
        indicator_val, xfo__whs, txg__ogr))
    xdkv__qiwz = {}
    exec(pqp__oegav, {'bodo': bodo}, xdkv__qiwz)
    _impl = xdkv__qiwz['_impl']
    return _impl


def common_validate_merge_merge_asof_spec(name_func, left, right, on,
    left_on, right_on, left_index, right_index, suffixes):
    if not isinstance(left, DataFrameType) or not isinstance(right,
        DataFrameType):
        raise BodoError(name_func + '() requires dataframe inputs')
    valid_dataframe_column_types = (ArrayItemArrayType, MapArrayType,
        StructArrayType, CategoricalArrayType, types.Array,
        IntegerArrayType, DecimalArrayType, IntervalArrayType, bodo.
        DatetimeArrayType, TimeArrayType)
    xnqub__sjpuj = {string_array_type, dict_str_arr_type, binary_array_type,
        datetime_date_array_type, datetime_timedelta_array_type, boolean_array}
    yxxvu__thp = {get_overload_const_str(gem__jgcst) for gem__jgcst in (
        left_on, right_on, on) if is_overload_constant_str(gem__jgcst)}
    for df in (left, right):
        for i, aypp__veh in enumerate(df.data):
            if not isinstance(aypp__veh, valid_dataframe_column_types
                ) and aypp__veh not in xnqub__sjpuj:
                raise BodoError(
                    f'{name_func}(): use of column with {type(aypp__veh)} in merge unsupported'
                    )
            if df.columns[i] in yxxvu__thp and isinstance(aypp__veh,
                MapArrayType):
                raise BodoError(
                    f'{name_func}(): merge on MapArrayType unsupported')
    ensure_constant_arg(name_func, 'left_index', left_index, bool)
    ensure_constant_arg(name_func, 'right_index', right_index, bool)
    if not is_overload_constant_tuple(suffixes
        ) and not is_overload_constant_list(suffixes):
        raise_bodo_error(name_func +
            "(): suffixes parameters should be ['_left', '_right']")
    if is_overload_constant_tuple(suffixes):
        bjzat__mang = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        bjzat__mang = list(get_overload_const_list(suffixes))
    if len(bjzat__mang) != 2:
        raise BodoError(name_func +
            '(): The number of suffixes should be exactly 2')
    vkrwa__xvcpz = tuple(set(left.columns) & set(right.columns))
    if not is_overload_none(on):
        knvrj__ymh = False
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            knvrj__ymh = on_str not in vkrwa__xvcpz and ('left.' in on_str or
                'right.' in on_str)
        if len(vkrwa__xvcpz) == 0 and not knvrj__ymh:
            raise_bodo_error(name_func +
                '(): No common columns to perform merge on. Merge options: left_on={lon}, right_on={ron}, left_index={lidx}, right_index={ridx}'
                .format(lon=is_overload_true(left_on), ron=is_overload_true
                (right_on), lidx=is_overload_true(left_index), ridx=
                is_overload_true(right_index)))
        if not is_overload_none(left_on) or not is_overload_none(right_on):
            raise BodoError(name_func +
                '(): Can only pass argument "on" OR "left_on" and "right_on", not a combination of both.'
                )
    if (is_overload_true(left_index) or not is_overload_none(left_on)
        ) and is_overload_none(right_on) and not is_overload_true(right_index):
        raise BodoError(name_func +
            '(): Must pass right_on or right_index=True')
    if (is_overload_true(right_index) or not is_overload_none(right_on)
        ) and is_overload_none(left_on) and not is_overload_true(left_index):
        raise BodoError(name_func + '(): Must pass left_on or left_index=True')


def validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
    right_index, sort, suffixes, copy, indicator, validate):
    common_validate_merge_merge_asof_spec('merge', left, right, on, left_on,
        right_on, left_index, right_index, suffixes)
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))


def validate_merge_asof_spec(left, right, on, left_on, right_on, left_index,
    right_index, by, left_by, right_by, suffixes, tolerance,
    allow_exact_matches, direction):
    common_validate_merge_merge_asof_spec('merge_asof', left, right, on,
        left_on, right_on, left_index, right_index, suffixes)
    if not is_overload_true(allow_exact_matches):
        raise BodoError(
            'merge_asof(): allow_exact_matches parameter only supports default value True'
            )
    if not is_overload_none(tolerance):
        raise BodoError(
            'merge_asof(): tolerance parameter only supports default value None'
            )
    if not is_overload_none(by):
        raise BodoError(
            'merge_asof(): by parameter only supports default value None')
    if not is_overload_none(left_by):
        raise BodoError(
            'merge_asof(): left_by parameter only supports default value None')
    if not is_overload_none(right_by):
        raise BodoError(
            'merge_asof(): right_by parameter only supports default value None'
            )
    if not is_overload_constant_str(direction):
        raise BodoError(
            'merge_asof(): direction parameter should be of type str')
    else:
        direction = get_overload_const_str(direction)
        if direction != 'backward':
            raise BodoError(
                "merge_asof(): direction parameter only supports default value 'backward'"
                )


def validate_merge_asof_keys_length(left_on, right_on, left_index,
    right_index, left_keys, right_keys):
    if not is_overload_true(left_index) and not is_overload_true(right_index):
        if len(right_keys) != len(left_keys):
            raise BodoError('merge(): len(right_on) must equal len(left_on)')
    if not is_overload_none(left_on) and is_overload_true(right_index):
        raise BodoError(
            'merge(): right_index = True and specifying left_on is not suppported yet.'
            )
    if not is_overload_none(right_on) and is_overload_true(left_index):
        raise BodoError(
            'merge(): left_index = True and specifying right_on is not suppported yet.'
            )


def validate_keys_length(left_index, right_index, left_keys, right_keys):
    if not is_overload_true(left_index) and not is_overload_true(right_index):
        if len(right_keys) != len(left_keys):
            raise BodoError('merge(): len(right_on) must equal len(left_on)')
    if is_overload_true(right_index):
        if len(left_keys) != 1:
            raise BodoError(
                'merge(): len(left_on) must equal the number of levels in the index of "right", which is 1'
                )
    if is_overload_true(left_index):
        if len(right_keys) != 1:
            raise BodoError(
                'merge(): len(right_on) must equal the number of levels in the index of "left", which is 1'
                )


def validate_keys_dtypes(left, right, left_index, right_index, left_keys,
    right_keys):
    kfog__zkoc = numba.core.registry.cpu_target.typing_context
    if is_overload_true(left_index) or is_overload_true(right_index):
        if is_overload_true(left_index) and is_overload_true(right_index):
            uyrpc__hgyjg = left.index
            fph__adcy = isinstance(uyrpc__hgyjg, StringIndexType)
            bppe__ayg = right.index
            kzn__gtq = isinstance(bppe__ayg, StringIndexType)
        elif is_overload_true(left_index):
            uyrpc__hgyjg = left.index
            fph__adcy = isinstance(uyrpc__hgyjg, StringIndexType)
            bppe__ayg = right.data[right.columns.index(right_keys[0])]
            kzn__gtq = bppe__ayg.dtype == string_type
        elif is_overload_true(right_index):
            uyrpc__hgyjg = left.data[left.columns.index(left_keys[0])]
            fph__adcy = uyrpc__hgyjg.dtype == string_type
            bppe__ayg = right.index
            kzn__gtq = isinstance(bppe__ayg, StringIndexType)
        if fph__adcy and kzn__gtq:
            return
        uyrpc__hgyjg = uyrpc__hgyjg.dtype
        bppe__ayg = bppe__ayg.dtype
        try:
            lrjpe__zlyrl = kfog__zkoc.resolve_function_type(operator.eq, (
                uyrpc__hgyjg, bppe__ayg), {})
        except:
            raise_bodo_error(
                'merge: You are trying to merge on {lk_dtype} and {rk_dtype} columns. If you wish to proceed you should use pd.concat'
                .format(lk_dtype=uyrpc__hgyjg, rk_dtype=bppe__ayg))
    else:
        for eri__qgwc, knfg__eehm in zip(left_keys, right_keys):
            uyrpc__hgyjg = left.data[left.columns.index(eri__qgwc)].dtype
            msnp__adxda = left.data[left.columns.index(eri__qgwc)]
            bppe__ayg = right.data[right.columns.index(knfg__eehm)].dtype
            gdyjm__uefk = right.data[right.columns.index(knfg__eehm)]
            if msnp__adxda == gdyjm__uefk:
                continue
            amahd__ecav = (
                'merge: You are trying to merge on column {lk} of {lk_dtype} and column {rk} of {rk_dtype}. If you wish to proceed you should use pd.concat'
                .format(lk=eri__qgwc, lk_dtype=uyrpc__hgyjg, rk=knfg__eehm,
                rk_dtype=bppe__ayg))
            hxwjd__aoew = uyrpc__hgyjg == string_type
            cniox__wynp = bppe__ayg == string_type
            if hxwjd__aoew ^ cniox__wynp:
                raise_bodo_error(amahd__ecav)
            try:
                lrjpe__zlyrl = kfog__zkoc.resolve_function_type(operator.eq,
                    (uyrpc__hgyjg, bppe__ayg), {})
            except:
                raise_bodo_error(amahd__ecav)


def validate_keys(keys, df):
    bqt__kxe = set(keys).difference(set(df.columns))
    if len(bqt__kxe) > 0:
        if is_overload_constant_str(df.index.name_typ
            ) and get_overload_const_str(df.index.name_typ) in bqt__kxe:
            raise_bodo_error(
                f'merge(): use of index {df.index.name_typ} as key for on/left_on/right_on is unsupported'
                )
        raise_bodo_error(
            f"""merge(): invalid key {bqt__kxe} for on/left_on/right_on
merge supports only valid column names {df.columns}"""
            )


@overload_method(DataFrameType, 'join', inline='always', no_unliteral=True)
def overload_dataframe_join(left, other, on=None, how='left', lsuffix='',
    rsuffix='', sort=False):
    check_runtime_cols_unsupported(left, 'DataFrame.join()')
    check_runtime_cols_unsupported(other, 'DataFrame.join()')
    fppl__hshwq = dict(lsuffix=lsuffix, rsuffix=rsuffix)
    eza__kshz = dict(lsuffix='', rsuffix='')
    check_unsupported_args('DataFrame.join', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort)
    how = get_overload_const_str(how)
    if not is_overload_none(on):
        left_keys = get_overload_const_list(on)
    else:
        left_keys = ['$_bodo_index_']
    right_keys = ['$_bodo_index_']
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    pqp__oegav = "def _impl(left, other, on=None, how='left',\n"
    pqp__oegav += "    lsuffix='', rsuffix='', sort=False):\n"
    pqp__oegav += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, other, {}, {}, '{}', '{}', '{}', True, False, True, '')
"""
        .format(left_keys, right_keys, how, lsuffix, rsuffix))
    xdkv__qiwz = {}
    exec(pqp__oegav, {'bodo': bodo}, xdkv__qiwz)
    _impl = xdkv__qiwz['_impl']
    return _impl


def validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort):
    if not isinstance(other, DataFrameType):
        raise BodoError('join() requires dataframe inputs')
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))
    if not is_overload_none(on) and len(get_overload_const_list(on)) != 1:
        raise BodoError('join(): len(on) must equals to 1 when specified.')
    if not is_overload_none(on):
        otgn__qlro = get_overload_const_list(on)
        validate_keys(otgn__qlro, left)
    if not is_overload_false(sort):
        raise BodoError(
            'join(): sort parameter only supports default value False')
    vkrwa__xvcpz = tuple(set(left.columns) & set(other.columns))
    if len(vkrwa__xvcpz) > 0:
        raise_bodo_error(
            'join(): not supporting joining on overlapping columns:{cols} Use DataFrame.merge() instead.'
            .format(cols=vkrwa__xvcpz))


def validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
    right_keys, left_columns, right_columns, indicator_val):
    asia__sgb = set(left_keys) & set(right_keys)
    srgjt__puvyl = set(left_columns) & set(right_columns)
    wdya__wmwe = srgjt__puvyl - asia__sgb
    gckom__fsg = set(left_columns) - srgjt__puvyl
    ohv__ftrqq = set(right_columns) - srgjt__puvyl
    ujnu__fiei = {}

    def insertOutColumn(col_name):
        if col_name in ujnu__fiei:
            raise_bodo_error(
                'join(): two columns happen to have the same name : {}'.
                format(col_name))
        ujnu__fiei[col_name] = 0
    for clovz__aljv in asia__sgb:
        insertOutColumn(clovz__aljv)
    for clovz__aljv in wdya__wmwe:
        xcvc__izo = str(clovz__aljv) + suffix_x
        njl__qga = str(clovz__aljv) + suffix_y
        insertOutColumn(xcvc__izo)
        insertOutColumn(njl__qga)
    for clovz__aljv in gckom__fsg:
        insertOutColumn(clovz__aljv)
    for clovz__aljv in ohv__ftrqq:
        insertOutColumn(clovz__aljv)
    if indicator_val:
        insertOutColumn('_merge')


@overload(pd.merge_asof, inline='always', no_unliteral=True)
def overload_dataframe_merge_asof(left, right, on=None, left_on=None,
    right_on=None, left_index=False, right_index=False, by=None, left_by=
    None, right_by=None, suffixes=('_x', '_y'), tolerance=None,
    allow_exact_matches=True, direction='backward'):
    raise BodoError('pandas.merge_asof() not support yet')
    validate_merge_asof_spec(left, right, on, left_on, right_on, left_index,
        right_index, by, left_by, right_by, suffixes, tolerance,
        allow_exact_matches, direction)
    if not isinstance(left, DataFrameType) or not isinstance(right,
        DataFrameType):
        raise BodoError('merge_asof() requires dataframe inputs')
    vkrwa__xvcpz = tuple(sorted(set(left.columns) & set(right.columns), key
        =lambda k: str(k)))
    if not is_overload_none(on):
        left_on = right_on = on
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = vkrwa__xvcpz
        right_keys = vkrwa__xvcpz
    else:
        if is_overload_true(left_index):
            left_keys = ['$_bodo_index_']
        else:
            left_keys = get_overload_const_list(left_on)
            validate_keys(left_keys, left)
        if is_overload_true(right_index):
            right_keys = ['$_bodo_index_']
        else:
            right_keys = get_overload_const_list(right_on)
            validate_keys(right_keys, right)
    validate_merge_asof_keys_length(left_on, right_on, left_index,
        right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    if isinstance(suffixes, tuple):
        bjzat__mang = suffixes
    if is_overload_constant_list(suffixes):
        bjzat__mang = list(get_overload_const_list(suffixes))
    if isinstance(suffixes, types.Omitted):
        bjzat__mang = suffixes.value
    suffix_x = bjzat__mang[0]
    suffix_y = bjzat__mang[1]
    pqp__oegav = (
        'def _impl(left, right, on=None, left_on=None, right_on=None,\n')
    pqp__oegav += (
        '    left_index=False, right_index=False, by=None, left_by=None,\n')
    pqp__oegav += "    right_by=None, suffixes=('_x', '_y'), tolerance=None,\n"
    pqp__oegav += "    allow_exact_matches=True, direction='backward'):\n"
    pqp__oegav += '  suffix_x = suffixes[0]\n'
    pqp__oegav += '  suffix_y = suffixes[1]\n'
    pqp__oegav += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, 'asof', '{}', '{}', False, False, True, '')
"""
        .format(left_keys, right_keys, suffix_x, suffix_y))
    xdkv__qiwz = {}
    exec(pqp__oegav, {'bodo': bodo}, xdkv__qiwz)
    _impl = xdkv__qiwz['_impl']
    return _impl


@overload_method(DataFrameType, 'groupby', inline='always', no_unliteral=True)
def overload_dataframe_groupby(df, by=None, axis=0, level=None, as_index=
    True, sort=False, group_keys=True, squeeze=False, observed=True, dropna
    =True, _bodo_num_shuffle_keys=-1):
    check_runtime_cols_unsupported(df, 'DataFrame.groupby()')
    validate_groupby_spec(df, by, axis, level, as_index, sort, group_keys,
        squeeze, observed, dropna, _bodo_num_shuffle_keys)

    def _impl(df, by=None, axis=0, level=None, as_index=True, sort=False,
        group_keys=True, squeeze=False, observed=True, dropna=True,
        _bodo_num_shuffle_keys=-1):
        return bodo.hiframes.pd_groupby_ext.init_groupby(df, by, as_index,
            dropna, _bodo_num_shuffle_keys)
    return _impl


def validate_groupby_spec(df, by, axis, level, as_index, sort, group_keys,
    squeeze, observed, dropna, _num_shuffle_keys):
    if is_overload_none(by):
        raise BodoError("groupby(): 'by' must be supplied.")
    if not is_overload_zero(axis):
        raise BodoError(
            "groupby(): 'axis' parameter only supports integer value 0.")
    if not is_overload_none(level):
        raise BodoError(
            "groupby(): 'level' is not supported since MultiIndex is not supported."
            )
    if not is_literal_type(by) and not is_overload_constant_list(by):
        raise_bodo_error(
            f"groupby(): 'by' parameter only supports a constant column label or column labels, not {by}."
            )
    if len(set(get_overload_const_list(by)).difference(set(df.columns))) > 0:
        raise_bodo_error(
            "groupby(): invalid key {} for 'by' (not available in columns {})."
            .format(get_overload_const_list(by), df.columns))
    if not is_overload_constant_bool(as_index):
        raise_bodo_error(
            "groupby(): 'as_index' parameter must be a constant bool, not {}."
            .format(as_index))
    if not is_overload_constant_bool(dropna):
        raise_bodo_error(
            "groupby(): 'dropna' parameter must be a constant bool, not {}."
            .format(dropna))
    if not is_overload_constant_int(_num_shuffle_keys):
        raise_bodo_error(
            f"groupby(): '_num_shuffle_keys' parameter must be a constant integer, not {_num_shuffle_keys}."
            )
    fppl__hshwq = dict(sort=sort, group_keys=group_keys, squeeze=squeeze,
        observed=observed)
    wfh__iorph = dict(sort=False, group_keys=True, squeeze=False, observed=True
        )
    check_unsupported_args('Dataframe.groupby', fppl__hshwq, wfh__iorph,
        package_name='pandas', module_name='GroupBy')


def pivot_error_checking(df, index, columns, values, func_name):
    wdm__yvy = func_name == 'DataFrame.pivot_table'
    if wdm__yvy:
        if is_overload_none(index) or not is_literal_type(index):
            raise_bodo_error(
                f"DataFrame.pivot_table(): 'index' argument is required and must be constant column labels"
                )
    elif not is_overload_none(index) and not is_literal_type(index):
        raise_bodo_error(
            f"{func_name}(): if 'index' argument is provided it must be constant column labels"
            )
    if is_overload_none(columns) or not is_literal_type(columns):
        raise_bodo_error(
            f"{func_name}(): 'columns' argument is required and must be a constant column label"
            )
    if not is_overload_none(values) and not is_literal_type(values):
        raise_bodo_error(
            f"{func_name}(): if 'values' argument is provided it must be constant column labels"
            )
    xpo__wjwn = get_literal_value(columns)
    if isinstance(xpo__wjwn, (list, tuple)):
        if len(xpo__wjwn) > 1:
            raise BodoError(
                f"{func_name}(): 'columns' argument must be a constant column label not a {xpo__wjwn}"
                )
        xpo__wjwn = xpo__wjwn[0]
    if xpo__wjwn not in df.columns:
        raise BodoError(
            f"{func_name}(): 'columns' column {xpo__wjwn} not found in DataFrame {df}."
            )
    iltfh__xjnfv = df.column_index[xpo__wjwn]
    if is_overload_none(index):
        zdzf__luenx = []
        hnmt__fxiag = []
    else:
        hnmt__fxiag = get_literal_value(index)
        if not isinstance(hnmt__fxiag, (list, tuple)):
            hnmt__fxiag = [hnmt__fxiag]
        zdzf__luenx = []
        for index in hnmt__fxiag:
            if index not in df.column_index:
                raise BodoError(
                    f"{func_name}(): 'index' column {index} not found in DataFrame {df}."
                    )
            zdzf__luenx.append(df.column_index[index])
    if not (all(isinstance(doowf__rqn, int) for doowf__rqn in hnmt__fxiag) or
        all(isinstance(doowf__rqn, str) for doowf__rqn in hnmt__fxiag)):
        raise BodoError(
            f"{func_name}(): column names selected for 'index' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    if is_overload_none(values):
        atco__gftso = []
        fxsc__skbkc = []
        gsyoo__zxij = zdzf__luenx + [iltfh__xjnfv]
        for i, doowf__rqn in enumerate(df.columns):
            if i not in gsyoo__zxij:
                atco__gftso.append(i)
                fxsc__skbkc.append(doowf__rqn)
    else:
        fxsc__skbkc = get_literal_value(values)
        if not isinstance(fxsc__skbkc, (list, tuple)):
            fxsc__skbkc = [fxsc__skbkc]
        atco__gftso = []
        for val in fxsc__skbkc:
            if val not in df.column_index:
                raise BodoError(
                    f"{func_name}(): 'values' column {val} not found in DataFrame {df}."
                    )
            atco__gftso.append(df.column_index[val])
    fubll__jsmd = set(atco__gftso) | set(zdzf__luenx) | {iltfh__xjnfv}
    if len(fubll__jsmd) != len(atco__gftso) + len(zdzf__luenx) + 1:
        raise BodoError(
            f"{func_name}(): 'index', 'columns', and 'values' must all refer to different columns"
            )

    def check_valid_index_typ(index_column):
        if isinstance(index_column, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType, bodo.
            IntervalArrayType)):
            raise BodoError(
                f"{func_name}(): 'index' DataFrame column must have scalar rows"
                )
        if isinstance(index_column, bodo.CategoricalArrayType):
            raise BodoError(
                f"{func_name}(): 'index' DataFrame column does not support categorical data"
                )
    if len(zdzf__luenx) == 0:
        index = df.index
        if isinstance(index, MultiIndexType):
            raise BodoError(
                f"{func_name}(): 'index' cannot be None with a DataFrame with a multi-index"
                )
        if not isinstance(index, RangeIndexType):
            check_valid_index_typ(index.data)
        if not is_literal_type(df.index.name_typ):
            raise BodoError(
                f"{func_name}(): If 'index' is None, the name of the DataFrame's Index must be constant at compile-time"
                )
    else:
        for ipqf__hsr in zdzf__luenx:
            index_column = df.data[ipqf__hsr]
            check_valid_index_typ(index_column)
    klh__grl = df.data[iltfh__xjnfv]
    if isinstance(klh__grl, (bodo.ArrayItemArrayType, bodo.MapArrayType,
        bodo.StructArrayType, bodo.TupleArrayType, bodo.IntervalArrayType)):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column must have scalar rows")
    if isinstance(klh__grl, bodo.CategoricalArrayType):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column does not support categorical data"
            )
    for aare__iksf in atco__gftso:
        mwl__okl = df.data[aare__iksf]
        if isinstance(mwl__okl, (bodo.ArrayItemArrayType, bodo.MapArrayType,
            bodo.StructArrayType, bodo.TupleArrayType)
            ) or mwl__okl == bodo.binary_array_type:
            raise BodoError(
                f"{func_name}(): 'values' DataFrame column must have scalar rows"
                )
    return (hnmt__fxiag, xpo__wjwn, fxsc__skbkc, zdzf__luenx, iltfh__xjnfv,
        atco__gftso)


@overload(pd.pivot, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot', inline='always', no_unliteral=True)
def overload_dataframe_pivot(data, index=None, columns=None, values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot()')
    if not isinstance(data, DataFrameType):
        raise BodoError("pandas.pivot(): 'data' argument must be a DataFrame")
    (hnmt__fxiag, xpo__wjwn, fxsc__skbkc, ipqf__hsr, iltfh__xjnfv, rrqo__rog
        ) = (pivot_error_checking(data, index, columns, values,
        'DataFrame.pivot'))
    if len(hnmt__fxiag) == 0:
        if is_overload_none(data.index.name_typ):
            yiio__ahfgw = None,
        else:
            yiio__ahfgw = get_literal_value(data.index.name_typ),
    else:
        yiio__ahfgw = tuple(hnmt__fxiag)
    hnmt__fxiag = ColNamesMetaType(yiio__ahfgw)
    fxsc__skbkc = ColNamesMetaType(tuple(fxsc__skbkc))
    xpo__wjwn = ColNamesMetaType((xpo__wjwn,))
    pqp__oegav = 'def impl(data, index=None, columns=None, values=None):\n'
    pqp__oegav += "    ev = tracing.Event('df.pivot')\n"
    pqp__oegav += f'    pivot_values = data.iloc[:, {iltfh__xjnfv}].unique()\n'
    pqp__oegav += '    result = bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    if len(ipqf__hsr) == 0:
        pqp__oegav += f"""        (bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)),),
"""
    else:
        pqp__oegav += '        (\n'
        for edpjb__tpyjw in ipqf__hsr:
            pqp__oegav += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {edpjb__tpyjw}),
"""
        pqp__oegav += '        ),\n'
    pqp__oegav += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {iltfh__xjnfv}),),
"""
    pqp__oegav += '        (\n'
    for aare__iksf in rrqo__rog:
        pqp__oegav += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {aare__iksf}),
"""
    pqp__oegav += '        ),\n'
    pqp__oegav += '        pivot_values,\n'
    pqp__oegav += '        index_lit,\n'
    pqp__oegav += '        columns_lit,\n'
    pqp__oegav += '        values_lit,\n'
    pqp__oegav += '    )\n'
    pqp__oegav += '    ev.finalize()\n'
    pqp__oegav += '    return result\n'
    xdkv__qiwz = {}
    exec(pqp__oegav, {'bodo': bodo, 'index_lit': hnmt__fxiag, 'columns_lit':
        xpo__wjwn, 'values_lit': fxsc__skbkc, 'tracing': tracing}, xdkv__qiwz)
    impl = xdkv__qiwz['impl']
    return impl


@overload(pd.pivot_table, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot_table', inline='always',
    no_unliteral=True)
def overload_dataframe_pivot_table(data, values=None, index=None, columns=
    None, aggfunc='mean', fill_value=None, margins=False, dropna=True,
    margins_name='All', observed=False, sort=True, _pivot_values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot_table()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot_table()')
    fppl__hshwq = dict(fill_value=fill_value, margins=margins, dropna=
        dropna, margins_name=margins_name, observed=observed, sort=sort)
    eza__kshz = dict(fill_value=None, margins=False, dropna=True,
        margins_name='All', observed=False, sort=True)
    check_unsupported_args('DataFrame.pivot_table', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(data, DataFrameType):
        raise BodoError(
            "pandas.pivot_table(): 'data' argument must be a DataFrame")
    (hnmt__fxiag, xpo__wjwn, fxsc__skbkc, ipqf__hsr, iltfh__xjnfv, rrqo__rog
        ) = (pivot_error_checking(data, index, columns, values,
        'DataFrame.pivot_table'))
    lwyf__ita = hnmt__fxiag
    hnmt__fxiag = ColNamesMetaType(tuple(hnmt__fxiag))
    fxsc__skbkc = ColNamesMetaType(tuple(fxsc__skbkc))
    bikef__bwg = xpo__wjwn
    xpo__wjwn = ColNamesMetaType((xpo__wjwn,))
    pqp__oegav = 'def impl(\n'
    pqp__oegav += '    data,\n'
    pqp__oegav += '    values=None,\n'
    pqp__oegav += '    index=None,\n'
    pqp__oegav += '    columns=None,\n'
    pqp__oegav += '    aggfunc="mean",\n'
    pqp__oegav += '    fill_value=None,\n'
    pqp__oegav += '    margins=False,\n'
    pqp__oegav += '    dropna=True,\n'
    pqp__oegav += '    margins_name="All",\n'
    pqp__oegav += '    observed=False,\n'
    pqp__oegav += '    sort=True,\n'
    pqp__oegav += '    _pivot_values=None,\n'
    pqp__oegav += '):\n'
    pqp__oegav += "    ev = tracing.Event('df.pivot_table')\n"
    imku__qrjx = ipqf__hsr + [iltfh__xjnfv] + rrqo__rog
    pqp__oegav += f'    data = data.iloc[:, {imku__qrjx}]\n'
    zfxd__zpgp = lwyf__ita + [bikef__bwg]
    if not is_overload_none(_pivot_values):
        zpc__vgnh = tuple(sorted(_pivot_values.meta))
        _pivot_values = ColNamesMetaType(zpc__vgnh)
        pqp__oegav += '    pivot_values = _pivot_values_arr\n'
        pqp__oegav += (
            f'    data = data[data.iloc[:, {len(ipqf__hsr)}].isin(pivot_values)]\n'
            )
        if all(isinstance(doowf__rqn, str) for doowf__rqn in zpc__vgnh):
            pmxni__svgy = pd.array(zpc__vgnh, 'string')
        elif all(isinstance(doowf__rqn, int) for doowf__rqn in zpc__vgnh):
            pmxni__svgy = np.array(zpc__vgnh, 'int64')
        else:
            raise BodoError(
                f'pivot(): pivot values selcected via pivot JIT argument must all share a common int or string type.'
                )
    else:
        pmxni__svgy = None
    mzjc__nvmdy = is_overload_constant_str(aggfunc) and get_overload_const_str(
        aggfunc) == 'nunique'
    dbw__tiz = len(zfxd__zpgp) if mzjc__nvmdy else len(lwyf__ita)
    pqp__oegav += f"""    data = data.groupby({zfxd__zpgp!r}, as_index=False, _bodo_num_shuffle_keys={dbw__tiz}).agg(aggfunc)
"""
    if is_overload_none(_pivot_values):
        pqp__oegav += (
            f'    pivot_values = data.iloc[:, {len(ipqf__hsr)}].unique()\n')
    pqp__oegav += '    result = bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    pqp__oegav += '        (\n'
    for i in range(0, len(ipqf__hsr)):
        pqp__oegav += (
            f'            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),\n'
            )
    pqp__oegav += '        ),\n'
    pqp__oegav += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {len(ipqf__hsr)}),),
"""
    pqp__oegav += '        (\n'
    for i in range(len(ipqf__hsr) + 1, len(rrqo__rog) + len(ipqf__hsr) + 1):
        pqp__oegav += (
            f'            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),\n'
            )
    pqp__oegav += '        ),\n'
    pqp__oegav += '        pivot_values,\n'
    pqp__oegav += '        index_lit,\n'
    pqp__oegav += '        columns_lit,\n'
    pqp__oegav += '        values_lit,\n'
    pqp__oegav += '        check_duplicates=False,\n'
    pqp__oegav += f'        is_already_shuffled={not mzjc__nvmdy},\n'
    pqp__oegav += '        _constant_pivot_values=_constant_pivot_values,\n'
    pqp__oegav += '    )\n'
    pqp__oegav += '    ev.finalize()\n'
    pqp__oegav += '    return result\n'
    xdkv__qiwz = {}
    exec(pqp__oegav, {'bodo': bodo, 'numba': numba, 'index_lit':
        hnmt__fxiag, 'columns_lit': xpo__wjwn, 'values_lit': fxsc__skbkc,
        '_pivot_values_arr': pmxni__svgy, '_constant_pivot_values':
        _pivot_values, 'tracing': tracing}, xdkv__qiwz)
    impl = xdkv__qiwz['impl']
    return impl


@overload(pd.melt, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'melt', inline='always', no_unliteral=True)
def overload_dataframe_melt(frame, id_vars=None, value_vars=None, var_name=
    None, value_name='value', col_level=None, ignore_index=True):
    fppl__hshwq = dict(col_level=col_level, ignore_index=ignore_index)
    eza__kshz = dict(col_level=None, ignore_index=True)
    check_unsupported_args('DataFrame.melt', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(frame, DataFrameType):
        raise BodoError("pandas.melt(): 'frame' argument must be a DataFrame.")
    if not is_overload_none(id_vars) and not is_literal_type(id_vars):
        raise_bodo_error(
            "DataFrame.melt(): 'id_vars', if specified, must be a literal.")
    if not is_overload_none(value_vars) and not is_literal_type(value_vars):
        raise_bodo_error(
            "DataFrame.melt(): 'value_vars', if specified, must be a literal.")
    if not is_overload_none(var_name) and not (is_literal_type(var_name) and
        (is_scalar_type(var_name) or isinstance(value_name, types.Omitted))):
        raise_bodo_error(
            "DataFrame.melt(): 'var_name', if specified, must be a literal.")
    if value_name != 'value' and not (is_literal_type(value_name) and (
        is_scalar_type(value_name) or isinstance(value_name, types.Omitted))):
        raise_bodo_error(
            "DataFrame.melt(): 'value_name', if specified, must be a literal.")
    var_name = get_literal_value(var_name) if not is_overload_none(var_name
        ) else 'variable'
    value_name = get_literal_value(value_name
        ) if value_name != 'value' else 'value'
    vxvgd__kgcdu = get_literal_value(id_vars) if not is_overload_none(id_vars
        ) else []
    if not isinstance(vxvgd__kgcdu, (list, tuple)):
        vxvgd__kgcdu = [vxvgd__kgcdu]
    for doowf__rqn in vxvgd__kgcdu:
        if doowf__rqn not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'id_vars' column {doowf__rqn} not found in {frame}."
                )
    xbgic__hzx = [frame.column_index[i] for i in vxvgd__kgcdu]
    if is_overload_none(value_vars):
        phc__wzvy = []
        bjjb__lkxp = []
        for i, doowf__rqn in enumerate(frame.columns):
            if i not in xbgic__hzx:
                phc__wzvy.append(i)
                bjjb__lkxp.append(doowf__rqn)
    else:
        bjjb__lkxp = get_literal_value(value_vars)
        if not isinstance(bjjb__lkxp, (list, tuple)):
            bjjb__lkxp = [bjjb__lkxp]
        bjjb__lkxp = [v for v in bjjb__lkxp if v not in vxvgd__kgcdu]
        if not bjjb__lkxp:
            raise BodoError(
                "DataFrame.melt(): currently empty 'value_vars' is unsupported."
                )
        phc__wzvy = []
        for val in bjjb__lkxp:
            if val not in frame.column_index:
                raise BodoError(
                    f"DataFrame.melt(): 'value_vars' column {val} not found in DataFrame {frame}."
                    )
            phc__wzvy.append(frame.column_index[val])
    for doowf__rqn in bjjb__lkxp:
        if doowf__rqn not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'value_vars' column {doowf__rqn} not found in {frame}."
                )
    if not (all(isinstance(doowf__rqn, int) for doowf__rqn in bjjb__lkxp) or
        all(isinstance(doowf__rqn, str) for doowf__rqn in bjjb__lkxp)):
        raise BodoError(
            f"DataFrame.melt(): column names selected for 'value_vars' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    ydv__tcb = frame.data[phc__wzvy[0]]
    vzdk__gkau = [frame.data[i].dtype for i in phc__wzvy]
    phc__wzvy = np.array(phc__wzvy, dtype=np.int64)
    xbgic__hzx = np.array(xbgic__hzx, dtype=np.int64)
    _, cbkt__waf = bodo.utils.typing.get_common_scalar_dtype(vzdk__gkau)
    if not cbkt__waf:
        raise BodoError(
            "DataFrame.melt(): columns selected in 'value_vars' must have a unifiable type."
            )
    extra_globals = {'np': np, 'value_lit': bjjb__lkxp, 'val_type': ydv__tcb}
    header = 'def impl(\n'
    header += '  frame,\n'
    header += '  id_vars=None,\n'
    header += '  value_vars=None,\n'
    header += '  var_name=None,\n'
    header += "  value_name='value',\n"
    header += '  col_level=None,\n'
    header += '  ignore_index=True,\n'
    header += '):\n'
    header += (
        '  dummy_id = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, 0)\n'
        )
    if frame.is_table_format and all(v == ydv__tcb.dtype for v in vzdk__gkau):
        extra_globals['value_idxs'] = bodo.utils.typing.MetaType(tuple(
            phc__wzvy))
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(frame)\n'
            )
        header += (
            '  val_col = bodo.utils.table_utils.table_concat(table, value_idxs, val_type)\n'
            )
    elif len(bjjb__lkxp) == 1:
        header += f"""  val_col = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {phc__wzvy[0]})
"""
    else:
        mtma__qjo = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})'
             for i in phc__wzvy)
        header += (
            f'  val_col = bodo.libs.array_kernels.concat(({mtma__qjo},))\n')
    header += """  var_col = bodo.libs.array_kernels.repeat_like(bodo.utils.conversion.coerce_to_array(value_lit), dummy_id)
"""
    for i in xbgic__hzx:
        header += (
            f'  id{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})\n'
            )
        header += (
            f'  out_id{i} = bodo.libs.array_kernels.concat([id{i}] * {len(bjjb__lkxp)})\n'
            )
    zfli__nfrre = ', '.join(f'out_id{i}' for i in xbgic__hzx) + (', ' if 
        len(xbgic__hzx) > 0 else '')
    data_args = zfli__nfrre + 'var_col, val_col'
    columns = tuple(vxvgd__kgcdu + [var_name, value_name])
    index = (
        f'bodo.hiframes.pd_index_ext.init_range_index(0, len(frame) * {len(bjjb__lkxp)}, 1, None)'
        )
    return _gen_init_df(header, columns, data_args, index, extra_globals)


@overload(pd.crosstab, inline='always', no_unliteral=True)
def crosstab_overload(index, columns, values=None, rownames=None, colnames=
    None, aggfunc=None, margins=False, margins_name='All', dropna=True,
    normalize=False, _pivot_values=None):
    raise BodoError(f'pandas.crosstab() not supported yet')
    fppl__hshwq = dict(values=values, rownames=rownames, colnames=colnames,
        aggfunc=aggfunc, margins=margins, margins_name=margins_name, dropna
        =dropna, normalize=normalize)
    eza__kshz = dict(values=None, rownames=None, colnames=None, aggfunc=
        None, margins=False, margins_name='All', dropna=True, normalize=False)
    check_unsupported_args('pandas.crosstab', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(index,
        'pandas.crosstab()')
    if not isinstance(index, SeriesType):
        raise BodoError(
            f"pandas.crosstab(): 'index' argument only supported for Series types, found {index}"
            )
    if not isinstance(columns, SeriesType):
        raise BodoError(
            f"pandas.crosstab(): 'columns' argument only supported for Series types, found {columns}"
            )

    def _impl(index, columns, values=None, rownames=None, colnames=None,
        aggfunc=None, margins=False, margins_name='All', dropna=True,
        normalize=False, _pivot_values=None):
        return bodo.hiframes.pd_groupby_ext.crosstab_dummy(index, columns,
            _pivot_values)
    return _impl


@overload_method(DataFrameType, 'sort_values', inline='always',
    no_unliteral=True)
def overload_dataframe_sort_values(df, by, axis=0, ascending=True, inplace=
    False, kind='quicksort', na_position='last', ignore_index=False, key=
    None, _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.sort_values()')
    fppl__hshwq = dict(ignore_index=ignore_index, key=key)
    eza__kshz = dict(ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_values', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'sort_values')
    validate_sort_values_spec(df, by, axis, ascending, inplace, kind,
        na_position)

    def _impl(df, by, axis=0, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', ignore_index=False, key=None,
        _bodo_transformed=False):
        return bodo.hiframes.pd_dataframe_ext.sort_values_dummy(df, by,
            ascending, inplace, na_position)
    return _impl


def validate_sort_values_spec(df, by, axis, ascending, inplace, kind,
    na_position):
    if is_overload_none(by) or not is_literal_type(by
        ) and not is_overload_constant_list(by):
        raise_bodo_error(
            "sort_values(): 'by' parameter only supports a constant column label or column labels. by={}"
            .format(by))
    gah__hhvyv = set(df.columns)
    if is_overload_constant_str(df.index.name_typ):
        gah__hhvyv.add(get_overload_const_str(df.index.name_typ))
    if is_overload_constant_tuple(by):
        cvoj__zqv = [get_overload_const_tuple(by)]
    else:
        cvoj__zqv = get_overload_const_list(by)
    cvoj__zqv = set((k, '') if (k, '') in gah__hhvyv else k for k in cvoj__zqv)
    if len(cvoj__zqv.difference(gah__hhvyv)) > 0:
        lmrhb__zgsaj = list(set(get_overload_const_list(by)).difference(
            gah__hhvyv))
        raise_bodo_error(f'sort_values(): invalid keys {lmrhb__zgsaj} for by.')
    if not is_overload_zero(axis):
        raise_bodo_error(
            "sort_values(): 'axis' parameter only supports integer value 0.")
    if not is_overload_bool(ascending) and not is_overload_bool_list(ascending
        ):
        raise_bodo_error(
            "sort_values(): 'ascending' parameter must be of type bool or list of bool, not {}."
            .format(ascending))
    if not is_overload_bool(inplace):
        raise_bodo_error(
            "sort_values(): 'inplace' parameter must be of type bool, not {}."
            .format(inplace))
    if kind != 'quicksort' and not isinstance(kind, types.Omitted):
        warnings.warn(BodoWarning(
            'sort_values(): specifying sorting algorithm is not supported in Bodo. Bodo uses stable sort.'
            ))
    if is_overload_constant_str(na_position):
        na_position = get_overload_const_str(na_position)
        if na_position not in ('first', 'last'):
            raise BodoError(
                "sort_values(): na_position should either be 'first' or 'last'"
                )
    elif is_overload_constant_list(na_position):
        mxhs__ayd = get_overload_const_list(na_position)
        for na_position in mxhs__ayd:
            if na_position not in ('first', 'last'):
                raise BodoError(
                    "sort_values(): Every value in na_position should either be 'first' or 'last'"
                    )
    else:
        raise_bodo_error(
            f'sort_values(): na_position parameter must be a literal constant of type str or a constant list of str with 1 entry per key column, not {na_position}'
            )
    na_position = get_overload_const_str(na_position)
    if na_position not in ['first', 'last']:
        raise BodoError(
            "sort_values(): na_position should either be 'first' or 'last'")


@overload_method(DataFrameType, 'sort_index', inline='always', no_unliteral
    =True)
def overload_dataframe_sort_index(df, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    check_runtime_cols_unsupported(df, 'DataFrame.sort_index()')
    fppl__hshwq = dict(axis=axis, level=level, kind=kind, sort_remaining=
        sort_remaining, ignore_index=ignore_index, key=key)
    eza__kshz = dict(axis=0, level=None, kind='quicksort', sort_remaining=
        True, ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_index', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_bool(ascending):
        raise BodoError(
            "DataFrame.sort_index(): 'ascending' parameter must be of type bool"
            )
    if not is_overload_bool(inplace):
        raise BodoError(
            "DataFrame.sort_index(): 'inplace' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "DataFrame.sort_index(): 'na_position' should either be 'first' or 'last'"
            )

    def _impl(df, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        return bodo.hiframes.pd_dataframe_ext.sort_values_dummy(df,
            '$_bodo_index_', ascending, inplace, na_position)
    return _impl


@overload_method(DataFrameType, 'rank', inline='always', no_unliteral=True)
def overload_dataframe_rank(df, axis=0, method='average', numeric_only=None,
    na_option='keep', ascending=True, pct=False):
    pqp__oegav = """def impl(df, axis=0, method='average', numeric_only=None, na_option='keep', ascending=True, pct=False):
"""
    xhvv__qmpga = len(df.columns)
    data_args = ', '.join(
        'bodo.libs.array_kernels.rank(data_{}, method=method, na_option=na_option, ascending=ascending, pct=pct)'
        .format(i) for i in range(xhvv__qmpga))
    for i in range(xhvv__qmpga):
        pqp__oegav += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(pqp__oegav, df.columns, data_args, index)


@overload_method(DataFrameType, 'fillna', inline='always', no_unliteral=True)
def overload_dataframe_fillna(df, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    check_runtime_cols_unsupported(df, 'DataFrame.fillna()')
    fppl__hshwq = dict(limit=limit, downcast=downcast)
    eza__kshz = dict(limit=None, downcast=None)
    check_unsupported_args('DataFrame.fillna', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.fillna()')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError("DataFrame.fillna(): 'axis' argument not supported.")
    pxj__kqksf = not is_overload_none(value)
    ymyzc__egs = not is_overload_none(method)
    if pxj__kqksf and ymyzc__egs:
        raise BodoError(
            "DataFrame.fillna(): Cannot specify both 'value' and 'method'.")
    if not pxj__kqksf and not ymyzc__egs:
        raise BodoError(
            "DataFrame.fillna(): Must specify one of 'value' and 'method'.")
    if pxj__kqksf:
        neo__lws = 'value=value'
    else:
        neo__lws = 'method=method'
    data_args = [(f"df['{doowf__rqn}'].fillna({neo__lws}, inplace=inplace)" if
        isinstance(doowf__rqn, str) else
        f'df[{doowf__rqn}].fillna({neo__lws}, inplace=inplace)') for
        doowf__rqn in df.columns]
    pqp__oegav = """def impl(df, value=None, method=None, axis=None, inplace=False, limit=None, downcast=None):
"""
    if is_overload_true(inplace):
        pqp__oegav += '  ' + '  \n'.join(data_args) + '\n'
        xdkv__qiwz = {}
        exec(pqp__oegav, {}, xdkv__qiwz)
        impl = xdkv__qiwz['impl']
        return impl
    else:
        return _gen_init_df(pqp__oegav, df.columns, ', '.join(kucr__difwy +
            '.values' for kucr__difwy in data_args))


@overload_method(DataFrameType, 'reset_index', inline='always',
    no_unliteral=True)
def overload_dataframe_reset_index(df, level=None, drop=False, inplace=
    False, col_level=0, col_fill='', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.reset_index()')
    fppl__hshwq = dict(col_level=col_level, col_fill=col_fill)
    eza__kshz = dict(col_level=0, col_fill='')
    check_unsupported_args('DataFrame.reset_index', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'reset_index')
    if not _is_all_levels(df, level):
        raise_bodo_error(
            'DataFrame.reset_index(): only dropping all index levels supported'
            )
    if not is_overload_constant_bool(drop):
        raise BodoError(
            "DataFrame.reset_index(): 'drop' parameter should be a constant boolean value"
            )
    if not is_overload_constant_bool(inplace):
        raise BodoError(
            "DataFrame.reset_index(): 'inplace' parameter should be a constant boolean value"
            )
    pqp__oegav = """def impl(df, level=None, drop=False, inplace=False, col_level=0, col_fill='', _bodo_transformed=False,):
"""
    pqp__oegav += (
        '  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(df), 1, None)\n'
        )
    drop = is_overload_true(drop)
    inplace = is_overload_true(inplace)
    columns = df.columns
    data_args = [
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}\n'.
        format(i, '' if inplace else '.copy()') for i in range(len(df.columns))
        ]
    if not drop:
        lezei__fxykf = 'index' if 'index' not in columns else 'level_0'
        index_names = get_index_names(df.index, 'DataFrame.reset_index()',
            lezei__fxykf)
        columns = index_names + columns
        if isinstance(df.index, MultiIndexType):
            pqp__oegav += """  m_index = bodo.hiframes.pd_index_ext.get_index_data(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
            wtoej__venab = ['m_index[{}]'.format(i) for i in range(df.index
                .nlevels)]
            data_args = wtoej__venab + data_args
        else:
            vtby__gxu = (
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
                )
            data_args = [vtby__gxu] + data_args
    return _gen_init_df(pqp__oegav, columns, ', '.join(data_args), 'index')


def _is_all_levels(df, level):
    gslbq__lkr = len(get_index_data_arr_types(df.index))
    return is_overload_none(level) or is_overload_constant_int(level
        ) and get_overload_const_int(level
        ) == 0 and gslbq__lkr == 1 or is_overload_constant_list(level
        ) and list(get_overload_const_list(level)) == list(range(gslbq__lkr))


@overload_method(DataFrameType, 'dropna', inline='always', no_unliteral=True)
def overload_dataframe_dropna(df, axis=0, how='any', thresh=None, subset=
    None, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.dropna()')
    if not is_overload_constant_bool(inplace) or is_overload_true(inplace):
        raise BodoError('DataFrame.dropna(): inplace=True is not supported')
    if not is_overload_zero(axis):
        raise_bodo_error(f'df.dropna(): only axis=0 supported')
    ensure_constant_values('dropna', 'how', how, ('any', 'all'))
    if is_overload_none(subset):
        vszle__zly = list(range(len(df.columns)))
    elif not is_overload_constant_list(subset):
        raise_bodo_error(
            f'df.dropna(): subset argument should a constant list, not {subset}'
            )
    else:
        mkj__nul = get_overload_const_list(subset)
        vszle__zly = []
        for xkrms__clcky in mkj__nul:
            if xkrms__clcky not in df.column_index:
                raise_bodo_error(
                    f"df.dropna(): column '{xkrms__clcky}' not in data frame columns {df}"
                    )
            vszle__zly.append(df.column_index[xkrms__clcky])
    xhvv__qmpga = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(xhvv__qmpga))
    pqp__oegav = (
        "def impl(df, axis=0, how='any', thresh=None, subset=None, inplace=False):\n"
        )
    for i in range(xhvv__qmpga):
        pqp__oegav += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    pqp__oegav += (
        """  ({0}, index_arr) = bodo.libs.array_kernels.dropna(({0}, {1}), how, thresh, ({2},))
"""
        .format(data_args, index, ', '.join(str(a) for a in vszle__zly)))
    pqp__oegav += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(pqp__oegav, df.columns, data_args, 'index')


@overload_method(DataFrameType, 'drop', inline='always', no_unliteral=True)
def overload_dataframe_drop(df, labels=None, axis=0, index=None, columns=
    None, level=None, inplace=False, errors='raise', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop()')
    fppl__hshwq = dict(index=index, level=level, errors=errors)
    eza__kshz = dict(index=None, level=None, errors='raise')
    check_unsupported_args('DataFrame.drop', fppl__hshwq, eza__kshz,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'drop')
    if not is_overload_constant_bool(inplace):
        raise_bodo_error(
            "DataFrame.drop(): 'inplace' parameter should be a constant bool")
    if not is_overload_none(labels):
        if not is_overload_none(columns):
            raise BodoError(
                "Dataframe.drop(): Cannot specify both 'labels' and 'columns'")
        if not is_overload_constant_int(axis) or get_overload_const_int(axis
            ) != 1:
            raise_bodo_error('DataFrame.drop(): only axis=1 supported')
        if is_overload_constant_str(labels):
            ggrgw__wmkmv = get_overload_const_str(labels),
        elif is_overload_constant_list(labels):
            ggrgw__wmkmv = get_overload_const_list(labels)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    else:
        if is_overload_none(columns):
            raise BodoError(
                "DataFrame.drop(): Need to specify at least one of 'labels' or 'columns'"
                )
        if is_overload_constant_str(columns):
            ggrgw__wmkmv = get_overload_const_str(columns),
        elif is_overload_constant_list(columns):
            ggrgw__wmkmv = get_overload_const_list(columns)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    for doowf__rqn in ggrgw__wmkmv:
        if doowf__rqn not in df.columns:
            raise_bodo_error(
                'DataFrame.drop(): column {} not in DataFrame columns {}'.
                format(doowf__rqn, df.columns))
    if len(set(ggrgw__wmkmv)) == len(df.columns):
        raise BodoError('DataFrame.drop(): Dropping all columns not supported.'
            )
    inplace = is_overload_true(inplace)
    cpp__birwo = tuple(doowf__rqn for doowf__rqn in df.columns if 
        doowf__rqn not in ggrgw__wmkmv)
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[doowf__rqn], '.copy()' if not inplace else
        '') for doowf__rqn in cpp__birwo)
    pqp__oegav = (
        'def impl(df, labels=None, axis=0, index=None, columns=None,\n')
    pqp__oegav += (
        "     level=None, inplace=False, errors='raise', _bodo_transformed=False):\n"
        )
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(pqp__oegav, cpp__birwo, data_args, index)


@overload_method(DataFrameType, 'append', inline='always', no_unliteral=True)
def overload_dataframe_append(df, other, ignore_index=False,
    verify_integrity=False, sort=None):
    check_runtime_cols_unsupported(df, 'DataFrame.append()')
    check_runtime_cols_unsupported(other, 'DataFrame.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'DataFrame.append()')
    if isinstance(other, DataFrameType):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat((df, other), ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    if isinstance(other, types.BaseTuple):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat((df,) + other, ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    if isinstance(other, types.List) and isinstance(other.dtype, DataFrameType
        ):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat([df] + other, ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    raise BodoError(
        'invalid df.append() input. Only dataframe and list/tuple of dataframes supported'
        )


@overload_method(DataFrameType, 'sample', inline='always', no_unliteral=True)
def overload_dataframe_sample(df, n=None, frac=None, replace=False, weights
    =None, random_state=None, axis=None, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.sample()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sample()')
    fppl__hshwq = dict(random_state=random_state, weights=weights, axis=
        axis, ignore_index=ignore_index)
    hwaq__qez = dict(random_state=None, weights=None, axis=None,
        ignore_index=False)
    check_unsupported_args('DataFrame.sample', fppl__hshwq, hwaq__qez,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_none(n) and not is_overload_none(frac):
        raise BodoError(
            'DataFrame.sample(): only one of n and frac option can be selected'
            )
    xhvv__qmpga = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(xhvv__qmpga))
    epld__mvc = ', '.join('rhs_data_{}'.format(i) for i in range(xhvv__qmpga))
    pqp__oegav = """def impl(df, n=None, frac=None, replace=False, weights=None, random_state=None, axis=None, ignore_index=False):
"""
    pqp__oegav += '  if (frac == 1 or n == len(df)) and not replace:\n'
    pqp__oegav += (
        '    return bodo.allgatherv(bodo.random_shuffle(df), False)\n')
    for i in range(xhvv__qmpga):
        pqp__oegav += (
            """  rhs_data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})
"""
            .format(i))
    pqp__oegav += '  if frac is None:\n'
    pqp__oegav += '    frac_d = -1.0\n'
    pqp__oegav += '  else:\n'
    pqp__oegav += '    frac_d = frac\n'
    pqp__oegav += '  if n is None:\n'
    pqp__oegav += '    n_i = 0\n'
    pqp__oegav += '  else:\n'
    pqp__oegav += '    n_i = n\n'
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    pqp__oegav += f"""  ({data_args},), index_arr = bodo.libs.array_kernels.sample_table_operation(({epld__mvc},), {index}, n_i, frac_d, replace)
"""
    pqp__oegav += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return bodo.hiframes.dataframe_impl._gen_init_df(pqp__oegav, df.columns,
        data_args, 'index')


@numba.njit
def _sizeof_fmt(num, size_qualifier=''):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f'{num:3.1f}{size_qualifier} {x}'
        num /= 1024.0
    return f'{num:3.1f}{size_qualifier} PB'


@overload_method(DataFrameType, 'info', no_unliteral=True)
def overload_dataframe_info(df, verbose=None, buf=None, max_cols=None,
    memory_usage=None, show_counts=None, null_counts=None):
    check_runtime_cols_unsupported(df, 'DataFrame.info()')
    lzvl__ztj = {'verbose': verbose, 'buf': buf, 'max_cols': max_cols,
        'memory_usage': memory_usage, 'show_counts': show_counts,
        'null_counts': null_counts}
    iuc__bisq = {'verbose': None, 'buf': None, 'max_cols': None,
        'memory_usage': None, 'show_counts': None, 'null_counts': None}
    check_unsupported_args('DataFrame.info', lzvl__ztj, iuc__bisq,
        package_name='pandas', module_name='DataFrame')
    qjk__yegoe = f"<class '{str(type(df)).split('.')[-1]}"
    if len(df.columns) == 0:

        def _info_impl(df, verbose=None, buf=None, max_cols=None,
            memory_usage=None, show_counts=None, null_counts=None):
            phm__iwfki = qjk__yegoe + '\n'
            phm__iwfki += 'Index: 0 entries\n'
            phm__iwfki += 'Empty DataFrame'
            print(phm__iwfki)
        return _info_impl
    else:
        pqp__oegav = """def _info_impl(df, verbose=None, buf=None, max_cols=None, memory_usage=None, show_counts=None, null_counts=None): #pragma: no cover
"""
        pqp__oegav += '    ncols = df.shape[1]\n'
        pqp__oegav += f'    lines = "{qjk__yegoe}\\n"\n'
        pqp__oegav += f'    lines += "{df.index}: "\n'
        pqp__oegav += (
            '    index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        if isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType):
            pqp__oegav += """    lines += f"{len(index)} entries, {index.start} to {index.stop-1}\\n\"
"""
        elif isinstance(df.index, bodo.hiframes.pd_index_ext.StringIndexType):
            pqp__oegav += """    lines += f"{len(index)} entries, {index[0]} to {index[len(index)-1]}\\n\"
"""
        else:
            pqp__oegav += (
                '    lines += f"{len(index)} entries, {index[0]} to {index[-1]}\\n"\n'
                )
        pqp__oegav += (
            '    lines += f"Data columns (total {ncols} columns):\\n"\n')
        pqp__oegav += (
            f'    space = {max(len(str(k)) for k in df.columns) + 1}\n')
        pqp__oegav += '    column_width = max(space, 7)\n'
        pqp__oegav += '    column= "Column"\n'
        pqp__oegav += '    underl= "------"\n'
        pqp__oegav += (
            '    lines += f"#   {column:<{column_width}} Non-Null Count  Dtype\\n"\n'
            )
        pqp__oegav += (
            '    lines += f"--- {underl:<{column_width}} --------------  -----\\n"\n'
            )
        pqp__oegav += '    mem_size = 0\n'
        pqp__oegav += (
            '    col_name = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        pqp__oegav += """    non_null_count = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)
"""
        pqp__oegav += (
            '    col_dtype = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        jccov__fyx = dict()
        for i in range(len(df.columns)):
            pqp__oegav += f"""    non_null_count[{i}] = str(bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})))
"""
            hgs__elc = f'{df.data[i].dtype}'
            if isinstance(df.data[i], bodo.CategoricalArrayType):
                hgs__elc = 'category'
            elif isinstance(df.data[i], bodo.IntegerArrayType):
                rrk__xsn = bodo.libs.int_arr_ext.IntDtype(df.data[i].dtype
                    ).name
                hgs__elc = f'{rrk__xsn[:-7]}'
            pqp__oegav += f'    col_dtype[{i}] = "{hgs__elc}"\n'
            if hgs__elc in jccov__fyx:
                jccov__fyx[hgs__elc] += 1
            else:
                jccov__fyx[hgs__elc] = 1
            pqp__oegav += f'    col_name[{i}] = "{df.columns[i]}"\n'
            pqp__oegav += f"""    mem_size += bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).nbytes
"""
        pqp__oegav += """    column_info = [f'{i:^3} {name:<{column_width}} {count} non-null      {dtype}' for i, (name, count, dtype) in enumerate(zip(col_name, non_null_count, col_dtype))]
"""
        pqp__oegav += '    for i in column_info:\n'
        pqp__oegav += "        lines += f'{i}\\n'\n"
        kmb__lzw = ', '.join(f'{k}({jccov__fyx[k]})' for k in sorted(
            jccov__fyx))
        pqp__oegav += f"    lines += 'dtypes: {kmb__lzw}\\n'\n"
        pqp__oegav += '    mem_size += df.index.nbytes\n'
        pqp__oegav += '    total_size = _sizeof_fmt(mem_size)\n'
        pqp__oegav += "    lines += f'memory usage: {total_size}'\n"
        pqp__oegav += '    print(lines)\n'
        xdkv__qiwz = {}
        exec(pqp__oegav, {'_sizeof_fmt': _sizeof_fmt, 'pd': pd, 'bodo':
            bodo, 'np': np}, xdkv__qiwz)
        _info_impl = xdkv__qiwz['_info_impl']
        return _info_impl


@overload_method(DataFrameType, 'memory_usage', inline='always',
    no_unliteral=True)
def overload_dataframe_memory_usage(df, index=True, deep=False):
    check_runtime_cols_unsupported(df, 'DataFrame.memory_usage()')
    pqp__oegav = 'def impl(df, index=True, deep=False):\n'
    igoxb__ztb = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df).nbytes')
    ygm__plxk = is_overload_true(index)
    columns = df.columns
    if ygm__plxk:
        columns = ('Index',) + columns
    if len(columns) == 0:
        nmt__ziuh = ()
    elif all(isinstance(doowf__rqn, int) for doowf__rqn in columns):
        nmt__ziuh = np.array(columns, 'int64')
    elif all(isinstance(doowf__rqn, str) for doowf__rqn in columns):
        nmt__ziuh = pd.array(columns, 'string')
    else:
        nmt__ziuh = columns
    if df.is_table_format and len(df.columns) > 0:
        mpusg__tptm = int(ygm__plxk)
        yuuzl__ppeib = len(columns)
        pqp__oegav += f'  nbytes_arr = np.empty({yuuzl__ppeib}, np.int64)\n'
        pqp__oegav += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        pqp__oegav += f"""  bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, {mpusg__tptm})
"""
        if ygm__plxk:
            pqp__oegav += f'  nbytes_arr[0] = {igoxb__ztb}\n'
        pqp__oegav += f"""  return bodo.hiframes.pd_series_ext.init_series(nbytes_arr, pd.Index(column_vals), None)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        if ygm__plxk:
            data = f'{igoxb__ztb},{data}'
        else:
            bbtc__gcgh = ',' if len(columns) == 1 else ''
            data = f'{data}{bbtc__gcgh}'
        pqp__oegav += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}), pd.Index(column_vals), None)
"""
    xdkv__qiwz = {}
    exec(pqp__oegav, {'bodo': bodo, 'np': np, 'pd': pd, 'column_vals':
        nmt__ziuh}, xdkv__qiwz)
    impl = xdkv__qiwz['impl']
    return impl


@overload(pd.read_excel, no_unliteral=True)
def overload_read_excel(io, sheet_name=0, header=0, names=None, index_col=
    None, usecols=None, squeeze=False, dtype=None, engine=None, converters=
    None, true_values=None, false_values=None, skiprows=None, nrows=None,
    na_values=None, keep_default_na=True, na_filter=True, verbose=False,
    parse_dates=False, date_parser=None, thousands=None, comment=None,
    skipfooter=0, convert_float=True, mangle_dupe_cols=True, _bodo_df_type=None
    ):
    df_type = _bodo_df_type.instance_type
    cxrrt__xavl = 'read_excel_df{}'.format(next_label())
    setattr(types, cxrrt__xavl, df_type)
    lkaqp__dpg = False
    if is_overload_constant_list(parse_dates):
        lkaqp__dpg = get_overload_const_list(parse_dates)
    hjd__tdzo = ', '.join(["'{}':{}".format(cname, _get_pd_dtype_str(t)) for
        cname, t in zip(df_type.columns, df_type.data)])
    pqp__oegav = f"""
def impl(
    io,
    sheet_name=0,
    header=0,
    names=None,
    index_col=None,
    usecols=None,
    squeeze=False,
    dtype=None,
    engine=None,
    converters=None,
    true_values=None,
    false_values=None,
    skiprows=None,
    nrows=None,
    na_values=None,
    keep_default_na=True,
    na_filter=True,
    verbose=False,
    parse_dates=False,
    date_parser=None,
    thousands=None,
    comment=None,
    skipfooter=0,
    convert_float=True,
    mangle_dupe_cols=True,
    _bodo_df_type=None,
):
    with numba.objmode(df="{cxrrt__xavl}"):
        df = pd.read_excel(
            io=io,
            sheet_name=sheet_name,
            header=header,
            names={list(df_type.columns)},
            index_col=index_col,
            usecols=usecols,
            squeeze=squeeze,
            dtype={{{hjd__tdzo}}},
            engine=engine,
            converters=converters,
            true_values=true_values,
            false_values=false_values,
            skiprows=skiprows,
            nrows=nrows,
            na_values=na_values,
            keep_default_na=keep_default_na,
            na_filter=na_filter,
            verbose=verbose,
            parse_dates={lkaqp__dpg},
            date_parser=date_parser,
            thousands=thousands,
            comment=comment,
            skipfooter=skipfooter,
            convert_float=convert_float,
            mangle_dupe_cols=mangle_dupe_cols,
        )
    return df
"""
    xdkv__qiwz = {}
    exec(pqp__oegav, globals(), xdkv__qiwz)
    impl = xdkv__qiwz['impl']
    return impl


def overload_dataframe_plot(df, x=None, y=None, kind='line', figsize=None,
    xlabel=None, ylabel=None, title=None, legend=True, fontsize=None,
    xticks=None, yticks=None, ax=None):
    try:
        import matplotlib.pyplot as plt
    except ImportError as lnz__oijj:
        raise BodoError('df.plot needs matplotllib which is not installed.')
    pqp__oegav = (
        "def impl(df, x=None, y=None, kind='line', figsize=None, xlabel=None, \n"
        )
    pqp__oegav += '    ylabel=None, title=None, legend=True, fontsize=None, \n'
    pqp__oegav += '    xticks=None, yticks=None, ax=None):\n'
    if is_overload_none(ax):
        pqp__oegav += '   fig, ax = plt.subplots()\n'
    else:
        pqp__oegav += '   fig = ax.get_figure()\n'
    if not is_overload_none(figsize):
        pqp__oegav += '   fig.set_figwidth(figsize[0])\n'
        pqp__oegav += '   fig.set_figheight(figsize[1])\n'
    if is_overload_none(xlabel):
        pqp__oegav += '   xlabel = x\n'
    pqp__oegav += '   ax.set_xlabel(xlabel)\n'
    if is_overload_none(ylabel):
        pqp__oegav += '   ylabel = y\n'
    else:
        pqp__oegav += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(title):
        pqp__oegav += '   ax.set_title(title)\n'
    if not is_overload_none(fontsize):
        pqp__oegav += '   ax.tick_params(labelsize=fontsize)\n'
    kind = get_overload_const_str(kind)
    if kind == 'line':
        if is_overload_none(x) and is_overload_none(y):
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    pqp__oegav += (
                        f'   ax.plot(df.iloc[:, {i}], label=df.columns[{i}])\n'
                        )
        elif is_overload_none(x):
            pqp__oegav += '   ax.plot(df[y], label=y)\n'
        elif is_overload_none(y):
            gao__zlbsi = get_overload_const_str(x)
            zvavt__bsgju = df.columns.index(gao__zlbsi)
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    if zvavt__bsgju != i:
                        pqp__oegav += (
                            f'   ax.plot(df[x], df.iloc[:, {i}], label=df.columns[{i}])\n'
                            )
        else:
            pqp__oegav += '   ax.plot(df[x], df[y], label=y)\n'
    elif kind == 'scatter':
        legend = False
        pqp__oegav += '   ax.scatter(df[x], df[y], s=20)\n'
        pqp__oegav += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(xticks):
        pqp__oegav += '   ax.set_xticks(xticks)\n'
    if not is_overload_none(yticks):
        pqp__oegav += '   ax.set_yticks(yticks)\n'
    if is_overload_true(legend):
        pqp__oegav += '   ax.legend()\n'
    pqp__oegav += '   return ax\n'
    xdkv__qiwz = {}
    exec(pqp__oegav, {'bodo': bodo, 'plt': plt}, xdkv__qiwz)
    impl = xdkv__qiwz['impl']
    return impl


@lower_builtin('df.plot', DataFrameType, types.VarArg(types.Any))
def dataframe_plot_low(context, builder, sig, args):
    impl = overload_dataframe_plot(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def is_df_values_numpy_supported_dftyp(df_typ):
    for qhz__wqo in df_typ.data:
        if not (isinstance(qhz__wqo, IntegerArrayType) or isinstance(
            qhz__wqo.dtype, types.Number) or qhz__wqo.dtype in (bodo.
            datetime64ns, bodo.timedelta64ns)):
            return False
    return True


def typeref_to_type(v):
    if isinstance(v, types.BaseTuple):
        return types.BaseTuple.from_types(tuple(typeref_to_type(a) for a in v))
    return v.instance_type if isinstance(v, (types.TypeRef, types.NumberClass)
        ) else v


def _install_typer_for_type(type_name, typ):

    @type_callable(typ)
    def type_call_type(context):

        def typer(*args, **kws):
            args = tuple(typeref_to_type(v) for v in args)
            kws = {name: typeref_to_type(v) for name, v in kws.items()}
            return types.TypeRef(typ(*args, **kws))
        return typer
    no_side_effect_call_tuples.add((type_name, bodo))
    no_side_effect_call_tuples.add((typ,))


def _install_type_call_typers():
    for type_name in bodo_types_with_params:
        typ = getattr(bodo, type_name)
        _install_typer_for_type(type_name, typ)


_install_type_call_typers()


def set_df_col(df, cname, arr, inplace):
    df[cname] = arr


@infer_global(set_df_col)
class SetDfColInfer(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        assert not kws
        assert len(args) == 4
        assert isinstance(args[1], types.Literal)
        lxlm__eqx = args[0]
        uxqc__ipst = args[1].literal_value
        val = args[2]
        assert val != types.unknown
        thk__upn = lxlm__eqx
        check_runtime_cols_unsupported(lxlm__eqx, 'set_df_col()')
        if isinstance(lxlm__eqx, DataFrameType):
            index = lxlm__eqx.index
            if len(lxlm__eqx.columns) == 0:
                index = bodo.hiframes.pd_index_ext.RangeIndexType(types.none)
            if isinstance(val, SeriesType):
                if len(lxlm__eqx.columns) == 0:
                    index = val.index
                val = val.data
            if is_pd_index_type(val):
                val = bodo.utils.typing.get_index_data_arr_types(val)[0]
            if isinstance(val, types.List):
                val = dtype_to_array_type(val.dtype)
            if is_overload_constant_str(val) or val == types.unicode_type:
                val = bodo.dict_str_arr_type
            elif not is_array_typ(val):
                val = dtype_to_array_type(val)
            if uxqc__ipst in lxlm__eqx.columns:
                cpp__birwo = lxlm__eqx.columns
                blwo__pfr = lxlm__eqx.columns.index(uxqc__ipst)
                nksmi__gke = list(lxlm__eqx.data)
                nksmi__gke[blwo__pfr] = val
                nksmi__gke = tuple(nksmi__gke)
            else:
                cpp__birwo = lxlm__eqx.columns + (uxqc__ipst,)
                nksmi__gke = lxlm__eqx.data + (val,)
            thk__upn = DataFrameType(nksmi__gke, index, cpp__birwo,
                lxlm__eqx.dist, lxlm__eqx.is_table_format)
        return thk__upn(*args)


SetDfColInfer.prefer_literal = True


def __bodosql_replace_columns_dummy(df, col_names_to_replace,
    cols_to_replace_with):
    for i in range(len(col_names_to_replace)):
        df[col_names_to_replace[i]] = cols_to_replace_with[i]


@infer_global(__bodosql_replace_columns_dummy)
class BodoSQLReplaceColsInfer(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        assert not kws
        assert len(args) == 3
        assert is_overload_constant_tuple(args[1])
        assert isinstance(args[2], types.BaseTuple)
        dfwy__yrfr = args[0]
        assert isinstance(dfwy__yrfr, DataFrameType) and len(dfwy__yrfr.columns
            ) > 0, 'Error while typechecking __bodosql_replace_columns_dummy: we should only generate a call __bodosql_replace_columns_dummy if the input dataframe'
        col_names_to_replace = get_overload_const_tuple(args[1])
        jvuk__nndk = args[2]
        assert len(col_names_to_replace) == len(jvuk__nndk
            ), 'Error while typechecking __bodosql_replace_columns_dummy: the tuple of column indicies to replace should be equal to the number of columns to replace them with'
        assert len(col_names_to_replace) <= len(dfwy__yrfr.columns
            ), 'Error while typechecking __bodosql_replace_columns_dummy: The number of indicies provided should be less than or equal to the number of columns in the input dataframe'
        for col_name in col_names_to_replace:
            assert col_name in dfwy__yrfr.columns, 'Error while typechecking __bodosql_replace_columns_dummy: All columns specified to be replaced should already be present in input dataframe'
        check_runtime_cols_unsupported(dfwy__yrfr,
            '__bodosql_replace_columns_dummy()')
        index = dfwy__yrfr.index
        cpp__birwo = dfwy__yrfr.columns
        nksmi__gke = list(dfwy__yrfr.data)
        for i in range(len(col_names_to_replace)):
            col_name = col_names_to_replace[i]
            msxqn__fqf = jvuk__nndk[i]
            assert isinstance(msxqn__fqf, SeriesType
                ), 'Error while typechecking __bodosql_replace_columns_dummy: the values to replace the columns with are expected to be series'
            if isinstance(msxqn__fqf, SeriesType):
                msxqn__fqf = msxqn__fqf.data
            fydm__bww = dfwy__yrfr.column_index[col_name]
            nksmi__gke[fydm__bww] = msxqn__fqf
        nksmi__gke = tuple(nksmi__gke)
        thk__upn = DataFrameType(nksmi__gke, index, cpp__birwo, dfwy__yrfr.
            dist, dfwy__yrfr.is_table_format)
        return thk__upn(*args)


BodoSQLReplaceColsInfer.prefer_literal = True


def _parse_query_expr(expr, env, columns, cleaned_columns, index_name=None,
    join_cleaned_cols=()):
    rlq__iqnu = {}

    def _rewrite_membership_op(self, node, left, right):
        uuwn__ylnwz = node.op
        op = self.visit(uuwn__ylnwz)
        return op, uuwn__ylnwz, left, right

    def _maybe_evaluate_binop(self, op, op_class, lhs, rhs, eval_in_python=
        ('in', 'not in'), maybe_eval_in_python=('==', '!=', '<', '>', '<=',
        '>=')):
        res = op(lhs, rhs)
        return res
    pfqbn__xevg = []


    class NewFuncNode(pd.core.computation.ops.FuncNode):

        def __init__(self, name):
            if (name not in pd.core.computation.ops.MATHOPS or pd.core.
                computation.check._NUMEXPR_INSTALLED and pd.core.
                computation.check_NUMEXPR_VERSION < pd.core.computation.ops
                .LooseVersion('2.6.9') and name in ('floor', 'ceil')):
                if name not in pfqbn__xevg:
                    raise BodoError('"{0}" is not a supported function'.
                        format(name))
            self.name = name
            if name in pfqbn__xevg:
                self.func = name
            else:
                self.func = getattr(np, name)

        def __call__(self, *args):
            return pd.core.computation.ops.MathCall(self, args)

        def __repr__(self):
            return pd.io.formats.printing.pprint_thing(self.name)

    def visit_Attribute(self, node, **kwargs):
        ymk__laog = node.attr
        value = node.value
        tynix__bbl = pd.core.computation.ops.LOCAL_TAG
        if ymk__laog in ('str', 'dt'):
            try:
                mqzbv__jks = str(self.visit(value))
            except pd.core.computation.ops.UndefinedVariableError as janzy__rdhan:
                col_name = janzy__rdhan.args[0].split("'")[1]
                raise BodoError(
                    'df.query(): column {} is not found in dataframe columns {}'
                    .format(col_name, columns))
        else:
            mqzbv__jks = str(self.visit(value))
        xgv__xqd = mqzbv__jks, ymk__laog
        if xgv__xqd in join_cleaned_cols:
            ymk__laog = join_cleaned_cols[xgv__xqd]
        name = mqzbv__jks + '.' + ymk__laog
        if name.startswith(tynix__bbl):
            name = name[len(tynix__bbl):]
        if ymk__laog in ('str', 'dt'):
            nzesl__ycioq = columns[cleaned_columns.index(mqzbv__jks)]
            rlq__iqnu[nzesl__ycioq] = mqzbv__jks
            self.env.scope[name] = 0
            return self.term_type(tynix__bbl + name, self.env)
        pfqbn__xevg.append(name)
        return NewFuncNode(name)

    def __str__(self):
        if isinstance(self.value, list):
            return '{}'.format(self.value)
        if isinstance(self.value, str):
            return "'{}'".format(self.value)
        return pd.io.formats.printing.pprint_thing(self.name)

    def math__str__(self):
        if self.op in pfqbn__xevg:
            return pd.io.formats.printing.pprint_thing('{0}({1})'.format(
                self.op, ','.join(map(str, self.operands))))
        hji__otujp = map(lambda a:
            'bodo.hiframes.pd_series_ext.get_series_data({})'.format(str(a)
            ), self.operands)
        op = 'np.{}'.format(self.op)
        uxqc__ipst = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len({}), 1, None)'
            .format(str(self.operands[0])))
        return pd.io.formats.printing.pprint_thing(
            'bodo.hiframes.pd_series_ext.init_series({0}({1}), {2})'.format
            (op, ','.join(hji__otujp), uxqc__ipst))

    def op__str__(self):
        brjos__eypg = ('({0})'.format(pd.io.formats.printing.pprint_thing(
            gwtp__lpe)) for gwtp__lpe in self.operands)
        if self.op == 'in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_isin_dummy({})'.format(
                ', '.join(brjos__eypg)))
        if self.op == 'not in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_notin_dummy({})'.format
                (', '.join(brjos__eypg)))
        return pd.io.formats.printing.pprint_thing(' {0} '.format(self.op).
            join(brjos__eypg))
    fmlf__yob = pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op
    vlkuh__xirkv = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_evaluate_binop)
    gasre__hqpc = pd.core.computation.expr.BaseExprVisitor.visit_Attribute
    hfdnj__fbhy = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_downcast_constants)
    ajwmu__ahy = pd.core.computation.ops.Term.__str__
    aler__snq = pd.core.computation.ops.MathCall.__str__
    uupv__usbk = pd.core.computation.ops.Op.__str__
    cpieb__fagf = pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
    try:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            _rewrite_membership_op)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            _maybe_evaluate_binop)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = (
            visit_Attribute)
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = lambda self, left, right: (left, right)
        pd.core.computation.ops.Term.__str__ = __str__
        pd.core.computation.ops.MathCall.__str__ = math__str__
        pd.core.computation.ops.Op.__str__ = op__str__
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        fhnnd__lxl = pd.core.computation.expr.Expr(expr, env=env)
        mzxi__mpt = str(fhnnd__lxl)
    except pd.core.computation.ops.UndefinedVariableError as janzy__rdhan:
        if not is_overload_none(index_name) and get_overload_const_str(
            index_name) == janzy__rdhan.args[0].split("'")[1]:
            raise BodoError(
                "df.query(): Refering to named index ('{}') by name is not supported"
                .format(get_overload_const_str(index_name)))
        else:
            raise BodoError(f'df.query(): undefined variable, {janzy__rdhan}')
    finally:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            fmlf__yob)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            vlkuh__xirkv)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = gasre__hqpc
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = hfdnj__fbhy
        pd.core.computation.ops.Term.__str__ = ajwmu__ahy
        pd.core.computation.ops.MathCall.__str__ = aler__snq
        pd.core.computation.ops.Op.__str__ = uupv__usbk
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (
            cpieb__fagf)
    hyiq__imoq = pd.core.computation.parsing.clean_column_name
    rlq__iqnu.update({doowf__rqn: hyiq__imoq(doowf__rqn) for doowf__rqn in
        columns if hyiq__imoq(doowf__rqn) in fhnnd__lxl.names})
    return fhnnd__lxl, mzxi__mpt, rlq__iqnu


class DataFrameTupleIterator(types.SimpleIteratorType):

    def __init__(self, col_names, arr_typs):
        self.array_types = arr_typs
        self.col_names = col_names
        vfbc__fjkp = ['{}={}'.format(col_names[i], arr_typs[i]) for i in
            range(len(col_names))]
        name = 'itertuples({})'.format(','.join(vfbc__fjkp))
        lcj__pnohj = namedtuple('Pandas', col_names)
        wnsfn__gpv = types.NamedTuple([_get_series_dtype(a) for a in
            arr_typs], lcj__pnohj)
        super(DataFrameTupleIterator, self).__init__(name, wnsfn__gpv)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


def _get_series_dtype(arr_typ):
    if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
        return pd_timestamp_type
    return arr_typ.dtype


def get_itertuples():
    pass


@infer_global(get_itertuples)
class TypeIterTuples(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) % 2 == 0, 'name and column pairs expected'
        col_names = [a.literal_value for a in args[:len(args) // 2]]
        xyfz__hkzni = [if_series_to_array_type(a) for a in args[len(args) //
            2:]]
        assert 'Index' not in col_names[0]
        col_names = ['Index'] + col_names
        xyfz__hkzni = [types.Array(types.int64, 1, 'C')] + xyfz__hkzni
        ftww__admb = DataFrameTupleIterator(col_names, xyfz__hkzni)
        return ftww__admb(*args)


TypeIterTuples.prefer_literal = True


@register_model(DataFrameTupleIterator)
class DataFrameTupleIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        kvdk__mkz = [('index', types.EphemeralPointer(types.uintp))] + [(
            'array{}'.format(i), arr) for i, arr in enumerate(fe_type.
            array_types[1:])]
        super(DataFrameTupleIteratorModel, self).__init__(dmm, fe_type,
            kvdk__mkz)

    def from_return(self, builder, value):
        return value


@lower_builtin(get_itertuples, types.VarArg(types.Any))
def get_itertuples_impl(context, builder, sig, args):
    evay__mdxtb = args[len(args) // 2:]
    xtauj__zzxh = sig.args[len(sig.args) // 2:]
    rkhv__weus = context.make_helper(builder, sig.return_type)
    wzt__gfgry = context.get_constant(types.intp, 0)
    udb__yzkn = cgutils.alloca_once_value(builder, wzt__gfgry)
    rkhv__weus.index = udb__yzkn
    for i, arr in enumerate(evay__mdxtb):
        setattr(rkhv__weus, 'array{}'.format(i), arr)
    for arr, arr_typ in zip(evay__mdxtb, xtauj__zzxh):
        context.nrt.incref(builder, arr_typ, arr)
    res = rkhv__weus._getvalue()
    return impl_ret_new_ref(context, builder, sig.return_type, res)


@lower_builtin('getiter', DataFrameTupleIterator)
def getiter_itertuples(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', DataFrameTupleIterator)
@iternext_impl(RefType.UNTRACKED)
def iternext_itertuples(context, builder, sig, args, result):
    wgv__papq, = sig.args
    ksd__qsbwz, = args
    rkhv__weus = context.make_helper(builder, wgv__papq, value=ksd__qsbwz)
    efhds__gavjx = signature(types.intp, wgv__papq.array_types[1])
    tjgo__dds = context.compile_internal(builder, lambda a: len(a),
        efhds__gavjx, [rkhv__weus.array0])
    index = builder.load(rkhv__weus.index)
    uwtlp__yajk = builder.icmp_signed('<', index, tjgo__dds)
    result.set_valid(uwtlp__yajk)
    with builder.if_then(uwtlp__yajk):
        values = [index]
        for i, arr_typ in enumerate(wgv__papq.array_types[1:]):
            hrvjs__zdosw = getattr(rkhv__weus, 'array{}'.format(i))
            if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
                nnvgg__ipwoj = signature(pd_timestamp_type, arr_typ, types.intp
                    )
                val = context.compile_internal(builder, lambda a, i: bodo.
                    hiframes.pd_timestamp_ext.
                    convert_datetime64_to_timestamp(np.int64(a[i])),
                    nnvgg__ipwoj, [hrvjs__zdosw, index])
            else:
                nnvgg__ipwoj = signature(arr_typ.dtype, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: a[i],
                    nnvgg__ipwoj, [hrvjs__zdosw, index])
            values.append(val)
        value = context.make_tuple(builder, wgv__papq.yield_type, values)
        result.yield_(value)
        lqi__uavya = cgutils.increment_index(builder, index)
        builder.store(lqi__uavya, rkhv__weus.index)


def _analyze_op_pair_first(self, scope, equiv_set, expr, lhs):
    typ = self.typemap[expr.value.name].first_type
    if not isinstance(typ, types.NamedTuple):
        return None
    lhs = ir.Var(scope, mk_unique_var('tuple_var'), expr.loc)
    self.typemap[lhs.name] = typ
    rhs = ir.Expr.pair_first(expr.value, expr.loc)
    jgrm__jvj = ir.Assign(rhs, lhs, expr.loc)
    hrvt__dka = lhs
    ikuzu__kvr = []
    gkvu__rci = []
    zpcp__axwa = typ.count
    for i in range(zpcp__axwa):
        zjnk__chbf = ir.Var(hrvt__dka.scope, mk_unique_var('{}_size{}'.
            format(hrvt__dka.name, i)), hrvt__dka.loc)
        tegjs__zldb = ir.Expr.static_getitem(lhs, i, None, hrvt__dka.loc)
        self.calltypes[tegjs__zldb] = None
        ikuzu__kvr.append(ir.Assign(tegjs__zldb, zjnk__chbf, hrvt__dka.loc))
        self._define(equiv_set, zjnk__chbf, types.intp, tegjs__zldb)
        gkvu__rci.append(zjnk__chbf)
    ltvoy__edekn = tuple(gkvu__rci)
    return numba.parfors.array_analysis.ArrayAnalysis.AnalyzeResult(shape=
        ltvoy__edekn, pre=[jgrm__jvj] + ikuzu__kvr)


numba.parfors.array_analysis.ArrayAnalysis._analyze_op_pair_first = (
    _analyze_op_pair_first)
