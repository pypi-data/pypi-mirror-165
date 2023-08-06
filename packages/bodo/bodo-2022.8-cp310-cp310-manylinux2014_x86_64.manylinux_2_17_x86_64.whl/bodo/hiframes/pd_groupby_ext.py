"""Support for Pandas Groupby operations
"""
import operator
from enum import Enum
import numba
import numpy as np
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.core.registry import CPUDispatcher
from numba.core.typing.templates import AbstractTemplate, bound_function, infer_global, signature
from numba.extending import infer, infer_getattr, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import NumericIndexType, RangeIndexType
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_table, delete_table_decref_arrays, get_groupby_labels, get_null_shuffle_info, get_shuffle_info, info_from_table, info_to_array, reverse_shuffle_table, shuffle_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.decimal_arr_ext import Decimal128Type
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.transform import get_call_expr_arg, get_const_func_output_type
from bodo.utils.typing import BodoError, ColNamesMetaType, check_unsupported_args, create_unsupported_overload, dtype_to_array_type, get_index_data_arr_types, get_index_name_types, get_literal_value, get_overload_const_bool, get_overload_const_func, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_constant_dict, get_udf_error_msg, get_udf_out_arr_type, is_dtype_nullable, is_literal_type, is_overload_constant_bool, is_overload_constant_dict, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true, list_cumulative, raise_bodo_error, to_nullable_type, to_numeric_index_if_range_index, to_str_arr_if_dict_array
from bodo.utils.utils import dt_err, is_expr


class DataFrameGroupByType(types.Type):

    def __init__(self, df_type, keys, selection, as_index, dropna=True,
        explicit_select=False, series_select=False, _num_shuffle_keys=-1):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df_type,
            'pandas.groupby()')
        self.df_type = df_type
        self.keys = keys
        self.selection = selection
        self.as_index = as_index
        self.dropna = dropna
        self.explicit_select = explicit_select
        self.series_select = series_select
        self._num_shuffle_keys = _num_shuffle_keys
        super(DataFrameGroupByType, self).__init__(name=
            f'DataFrameGroupBy({df_type}, {keys}, {selection}, {as_index}, {dropna}, {explicit_select}, {series_select}, {_num_shuffle_keys})'
            )

    def copy(self):
        return DataFrameGroupByType(self.df_type, self.keys, self.selection,
            self.as_index, self.dropna, self.explicit_select, self.
            series_select, self._num_shuffle_keys)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(DataFrameGroupByType)
class GroupbyModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        adlg__ltbyi = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, adlg__ltbyi)


make_attribute_wrapper(DataFrameGroupByType, 'obj', 'obj')


def validate_udf(func_name, func):
    if not isinstance(func, (types.functions.MakeFunctionLiteral, bodo.
        utils.typing.FunctionLiteral, types.Dispatcher, CPUDispatcher)):
        raise_bodo_error(
            f"Groupby.{func_name}: 'func' must be user defined function")


@intrinsic
def init_groupby(typingctx, obj_type, by_type, as_index_type, dropna_type,
    _num_shuffle_keys):

    def codegen(context, builder, signature, args):
        zhld__lhx = args[0]
        ckztn__vkwm = signature.return_type
        mzm__fppel = cgutils.create_struct_proxy(ckztn__vkwm)(context, builder)
        mzm__fppel.obj = zhld__lhx
        context.nrt.incref(builder, signature.args[0], zhld__lhx)
        return mzm__fppel._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for gld__xzyr in keys:
        selection.remove(gld__xzyr)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    if is_overload_constant_int(_num_shuffle_keys):
        wsr__dzbyn = get_overload_const_int(_num_shuffle_keys)
    else:
        wsr__dzbyn = -1
    ckztn__vkwm = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False, _num_shuffle_keys=wsr__dzbyn)
    return ckztn__vkwm(obj_type, by_type, as_index_type, dropna_type,
        _num_shuffle_keys), codegen


@lower_builtin('groupby.count', types.VarArg(types.Any))
@lower_builtin('groupby.size', types.VarArg(types.Any))
@lower_builtin('groupby.apply', types.VarArg(types.Any))
@lower_builtin('groupby.agg', types.VarArg(types.Any))
def lower_groupby_count_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


@infer
class StaticGetItemDataFrameGroupBy(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        grpby, mkbv__tnn = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(mkbv__tnn, (tuple, list)):
                if len(set(mkbv__tnn).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(mkbv__tnn).difference(set(grpby.df_type
                        .columns))))
                selection = mkbv__tnn
            else:
                if mkbv__tnn not in grpby.df_type.columns:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(mkbv__tnn))
                selection = mkbv__tnn,
                series_select = True
            ctk__jneul = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True,
                series_select, _num_shuffle_keys=grpby._num_shuffle_keys)
            return signature(ctk__jneul, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, mkbv__tnn = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(
            mkbv__tnn):
            ctk__jneul = StaticGetItemDataFrameGroupBy.generic(self, (grpby,
                get_literal_value(mkbv__tnn)), {}).return_type
            return signature(ctk__jneul, *args)


GetItemDataFrameGroupBy.prefer_literal = True


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    muf__fzs = arr_type == ArrayItemArrayType(string_array_type)
    rjd__ejbu = arr_type.dtype
    if isinstance(rjd__ejbu, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {rjd__ejbu} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(rjd__ejbu, (Decimal128Type,
        types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    if func_name in ('first', 'last', 'sum', 'prod', 'min', 'max', 'count',
        'nunique', 'head') and isinstance(arr_type, (TupleArrayType,
        ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {rjd__ejbu} is not supported in groupby built-in function {func_name}'
            )
    if func_name in {'median', 'mean', 'var', 'std'} and isinstance(rjd__ejbu,
        (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    if not isinstance(rjd__ejbu, (types.Integer, types.Float, types.Boolean)):
        if muf__fzs or rjd__ejbu == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last', 'head'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(rjd__ejbu, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not rjd__ejbu.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last', 'head'}:
                return (None,
                    f'column type of {rjd__ejbu} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(rjd__ejbu, types.Boolean) and func_name in {'cumsum',
        'mean', 'sum', 'std', 'var'}:
        if func_name in {'sum'}:
            return to_nullable_type(dtype_to_array_type(types.int64)), 'ok'
        return (None,
            f'groupby built-in functions {func_name} does not support boolean column'
            )
    if func_name in {'idxmin', 'idxmax'}:
        return dtype_to_array_type(get_index_data_arr_types(index_type)[0].
            dtype), 'ok'
    elif func_name in {'count', 'nunique'}:
        return dtype_to_array_type(types.int64), 'ok'
    else:
        return arr_type, 'ok'


def get_pivot_output_dtype(arr_type, func_name, index_type=None):
    rjd__ejbu = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(rjd__ejbu, (
            types.Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(rjd__ejbu, types.Integer):
            return IntDtype(rjd__ejbu)
        return rjd__ejbu
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        jlbv__ehyy = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{jlbv__ehyy}'."
            )
    elif len(args) > len_args:
        raise BodoError(
            f'Groupby.{func_name}() takes {len_args + 1} positional argument but {len(args)} were given.'
            )


class ColumnType(Enum):
    KeyColumn = 0
    NumericalColumn = 1
    NonNumericalColumn = 2


def get_keys_not_as_index(grp, out_columns, out_data, out_column_type,
    multi_level_names=False):
    for gld__xzyr in grp.keys:
        if multi_level_names:
            jwwfc__phqp = gld__xzyr, ''
        else:
            jwwfc__phqp = gld__xzyr
        wsr__yeqkg = grp.df_type.column_index[gld__xzyr]
        data = grp.df_type.data[wsr__yeqkg]
        out_columns.append(jwwfc__phqp)
        out_data.append(data)
        out_column_type.append(ColumnType.KeyColumn.value)


def get_agg_typ(grp, args, func_name, typing_context, target_context, func=
    None, kws=None):
    index = RangeIndexType(types.none)
    out_data = []
    out_columns = []
    out_column_type = []
    if func_name in ('head', 'ngroup'):
        grp.as_index = True
    if not grp.as_index:
        get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
    elif func_name in ('head', 'ngroup'):
        if grp.df_type.index == index:
            index = NumericIndexType(types.int64, types.none)
        else:
            index = grp.df_type.index
    elif len(grp.keys) > 1:
        voeh__dvpx = tuple(grp.df_type.column_index[grp.keys[pqptt__lasty]] for
            pqptt__lasty in range(len(grp.keys)))
        bgrmx__fdbaw = tuple(grp.df_type.data[wsr__yeqkg] for wsr__yeqkg in
            voeh__dvpx)
        index = MultiIndexType(bgrmx__fdbaw, tuple(types.StringLiteral(
            gld__xzyr) for gld__xzyr in grp.keys))
    else:
        wsr__yeqkg = grp.df_type.column_index[grp.keys[0]]
        lztk__rkdb = grp.df_type.data[wsr__yeqkg]
        index = bodo.hiframes.pd_index_ext.array_type_to_index(lztk__rkdb,
            types.StringLiteral(grp.keys[0]))
    goddb__jdxy = {}
    cxtl__puhjc = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        goddb__jdxy[None, 'size'] = 'size'
    elif func_name == 'ngroup':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('ngroup')
        goddb__jdxy[None, 'ngroup'] = 'ngroup'
        kws = dict(kws) if kws else {}
        ascending = args[0] if len(args) > 0 else kws.pop('ascending', True)
        pzds__dqfnr = dict(ascending=ascending)
        wqgfj__cnir = dict(ascending=True)
        check_unsupported_args(f'Groupby.{func_name}', pzds__dqfnr,
            wqgfj__cnir, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(func_name, 1, args, kws)
    else:
        columns = (grp.selection if func_name != 'head' or grp.
            explicit_select else grp.df_type.columns)
        for wktqh__ktnuh in columns:
            wsr__yeqkg = grp.df_type.column_index[wktqh__ktnuh]
            data = grp.df_type.data[wsr__yeqkg]
            if func_name in ('sum', 'cumsum'):
                data = to_str_arr_if_dict_array(data)
            jzmu__jnzmy = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType)
                ) and isinstance(data.dtype, (types.Integer, types.Float)):
                jzmu__jnzmy = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    wdg__gio = SeriesType(data.dtype, data, None, string_type)
                    oyl__tfww = get_const_func_output_type(func, (wdg__gio,
                        ), {}, typing_context, target_context)
                    if oyl__tfww != ArrayItemArrayType(string_array_type):
                        oyl__tfww = dtype_to_array_type(oyl__tfww)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=wktqh__ktnuh, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    ubkl__szvg = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    hpfn__fczdj = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    pzds__dqfnr = dict(numeric_only=ubkl__szvg, min_count=
                        hpfn__fczdj)
                    wqgfj__cnir = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        pzds__dqfnr, wqgfj__cnir, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    ubkl__szvg = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    hpfn__fczdj = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    pzds__dqfnr = dict(numeric_only=ubkl__szvg, min_count=
                        hpfn__fczdj)
                    wqgfj__cnir = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}',
                        pzds__dqfnr, wqgfj__cnir, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    ubkl__szvg = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    pzds__dqfnr = dict(numeric_only=ubkl__szvg)
                    wqgfj__cnir = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        pzds__dqfnr, wqgfj__cnir, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    wmwq__sirj = args[0] if len(args) > 0 else kws.pop('axis',
                        0)
                    dmwm__aqnw = args[1] if len(args) > 1 else kws.pop('skipna'
                        , True)
                    pzds__dqfnr = dict(axis=wmwq__sirj, skipna=dmwm__aqnw)
                    wqgfj__cnir = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        pzds__dqfnr, wqgfj__cnir, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    dxoo__xwqce = args[0] if len(args) > 0 else kws.pop('ddof',
                        1)
                    pzds__dqfnr = dict(ddof=dxoo__xwqce)
                    wqgfj__cnir = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        pzds__dqfnr, wqgfj__cnir, package_name='pandas',
                        module_name='GroupBy')
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                elif func_name == 'head':
                    if len(args) == 0:
                        kws.pop('n', None)
                oyl__tfww, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                oyl__tfww = to_str_arr_if_dict_array(oyl__tfww
                    ) if func_name in ('sum', 'cumsum') else oyl__tfww
                out_data.append(oyl__tfww)
                out_columns.append(wktqh__ktnuh)
                if func_name == 'agg':
                    cxp__gqi = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    goddb__jdxy[wktqh__ktnuh, cxp__gqi] = wktqh__ktnuh
                else:
                    goddb__jdxy[wktqh__ktnuh, func_name] = wktqh__ktnuh
                out_column_type.append(jzmu__jnzmy)
            else:
                cxtl__puhjc.append(err_msg)
    if func_name == 'sum':
        gyrk__knxn = any([(blytf__tmj == ColumnType.NumericalColumn.value) for
            blytf__tmj in out_column_type])
        if gyrk__knxn:
            out_data = [blytf__tmj for blytf__tmj, efpou__yhi in zip(
                out_data, out_column_type) if efpou__yhi != ColumnType.
                NonNumericalColumn.value]
            out_columns = [blytf__tmj for blytf__tmj, efpou__yhi in zip(
                out_columns, out_column_type) if efpou__yhi != ColumnType.
                NonNumericalColumn.value]
            goddb__jdxy = {}
            for wktqh__ktnuh in out_columns:
                if grp.as_index is False and wktqh__ktnuh in grp.keys:
                    continue
                goddb__jdxy[wktqh__ktnuh, func_name] = wktqh__ktnuh
    lel__urhl = len(cxtl__puhjc)
    if len(out_data) == 0:
        if lel__urhl == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(lel__urhl, ' was' if lel__urhl == 1 else 's were',
                ','.join(cxtl__puhjc)))
    pifff__eoce = DataFrameType(tuple(out_data), index, tuple(out_columns),
        is_table_format=True)
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index or func_name == 'ngroup'):
        if isinstance(out_data[0], IntegerArrayType):
            sbg__glkwn = IntDtype(out_data[0].dtype)
        else:
            sbg__glkwn = out_data[0].dtype
        xkgc__omrvy = types.none if func_name in ('size', 'ngroup'
            ) else types.StringLiteral(grp.selection[0])
        pifff__eoce = SeriesType(sbg__glkwn, data=out_data[0], index=index,
            name_typ=xkgc__omrvy)
    return signature(pifff__eoce, *args), goddb__jdxy


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context, target_context
    ):
    kyvxn__kybk = True
    if isinstance(f_val, str):
        kyvxn__kybk = False
        jcnl__lie = f_val
    elif is_overload_constant_str(f_val):
        kyvxn__kybk = False
        jcnl__lie = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        kyvxn__kybk = False
        jcnl__lie = bodo.utils.typing.get_builtin_function_name(f_val)
    if not kyvxn__kybk:
        if jcnl__lie not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {jcnl__lie}')
        ctk__jneul = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True, _num_shuffle_keys=grp.
            _num_shuffle_keys)
        out_tp = get_agg_typ(ctk__jneul, (), jcnl__lie, typing_context,
            target_context)[0].return_type
    else:
        if is_expr(f_val, 'make_function'):
            bes__yssm = types.functions.MakeFunctionLiteral(f_val)
        else:
            bes__yssm = f_val
        validate_udf('agg', bes__yssm)
        func = get_overload_const_func(bes__yssm, None)
        ezqgv__fhey = func.code if hasattr(func, 'code') else func.__code__
        jcnl__lie = ezqgv__fhey.co_name
        ctk__jneul = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True, _num_shuffle_keys=grp.
            _num_shuffle_keys)
        out_tp = get_agg_typ(ctk__jneul, (), 'agg', typing_context,
            target_context, bes__yssm)[0].return_type
    return jcnl__lie, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    niush__jcpf = kws and all(isinstance(pfnhr__kbiex, types.Tuple) and len
        (pfnhr__kbiex) == 2 for pfnhr__kbiex in kws.values())
    if is_overload_none(func) and not niush__jcpf:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not niush__jcpf:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    pvgfi__cfmk = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if niush__jcpf or is_overload_constant_dict(func):
        if niush__jcpf:
            clrfh__twiqb = [get_literal_value(ett__gie) for ett__gie,
                jhww__eauar in kws.values()]
            bjz__nfbbj = [get_literal_value(jzgd__zyae) for jhww__eauar,
                jzgd__zyae in kws.values()]
        else:
            viuze__fnou = get_overload_constant_dict(func)
            clrfh__twiqb = tuple(viuze__fnou.keys())
            bjz__nfbbj = tuple(viuze__fnou.values())
        for aero__yac in ('head', 'ngroup'):
            if aero__yac in bjz__nfbbj:
                raise BodoError(
                    f'Groupby.agg()/aggregate(): {aero__yac} cannot be mixed with other groupby operations.'
                    )
        if any(wktqh__ktnuh not in grp.selection and wktqh__ktnuh not in
            grp.keys for wktqh__ktnuh in clrfh__twiqb):
            raise_bodo_error(
                f'Selected column names {clrfh__twiqb} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            bjz__nfbbj)
        if niush__jcpf and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        goddb__jdxy = {}
        out_columns = []
        out_data = []
        out_column_type = []
        ogs__gcu = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for mvt__qfuf, f_val in zip(clrfh__twiqb, bjz__nfbbj):
            if isinstance(f_val, (tuple, list)):
                qqd__fcg = 0
                for bes__yssm in f_val:
                    jcnl__lie, out_tp = get_agg_funcname_and_outtyp(grp,
                        mvt__qfuf, bes__yssm, typing_context, target_context)
                    pvgfi__cfmk = jcnl__lie in list_cumulative
                    if jcnl__lie == '<lambda>' and len(f_val) > 1:
                        jcnl__lie = '<lambda_' + str(qqd__fcg) + '>'
                        qqd__fcg += 1
                    out_columns.append((mvt__qfuf, jcnl__lie))
                    goddb__jdxy[mvt__qfuf, jcnl__lie] = mvt__qfuf, jcnl__lie
                    _append_out_type(grp, out_data, out_tp)
            else:
                jcnl__lie, out_tp = get_agg_funcname_and_outtyp(grp,
                    mvt__qfuf, f_val, typing_context, target_context)
                pvgfi__cfmk = jcnl__lie in list_cumulative
                if multi_level_names:
                    out_columns.append((mvt__qfuf, jcnl__lie))
                    goddb__jdxy[mvt__qfuf, jcnl__lie] = mvt__qfuf, jcnl__lie
                elif not niush__jcpf:
                    out_columns.append(mvt__qfuf)
                    goddb__jdxy[mvt__qfuf, jcnl__lie] = mvt__qfuf
                elif niush__jcpf:
                    ogs__gcu.append(jcnl__lie)
                _append_out_type(grp, out_data, out_tp)
        if niush__jcpf:
            for pqptt__lasty, kcmfp__hcsk in enumerate(kws.keys()):
                out_columns.append(kcmfp__hcsk)
                goddb__jdxy[clrfh__twiqb[pqptt__lasty], ogs__gcu[pqptt__lasty]
                    ] = kcmfp__hcsk
        if pvgfi__cfmk:
            index = grp.df_type.index
        else:
            index = out_tp.index
        pifff__eoce = DataFrameType(tuple(out_data), index, tuple(
            out_columns), is_table_format=True)
        return signature(pifff__eoce, *args), goddb__jdxy
    if isinstance(func, types.BaseTuple) and not isinstance(func, types.
        LiteralStrKeyDict) or is_overload_constant_list(func):
        if not (len(grp.selection) == 1 and grp.explicit_select):
            raise_bodo_error(
                'Groupby.agg()/aggregate(): must select exactly one column when more than one function is supplied'
                )
        if is_overload_constant_list(func):
            pmma__cnit = get_overload_const_list(func)
        else:
            pmma__cnit = func.types
        if len(pmma__cnit) == 0:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): List of functions must contain at least 1 function'
                )
        out_data = []
        out_columns = []
        out_column_type = []
        qqd__fcg = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        goddb__jdxy = {}
        zjyh__mejem = grp.selection[0]
        for f_val in pmma__cnit:
            jcnl__lie, out_tp = get_agg_funcname_and_outtyp(grp,
                zjyh__mejem, f_val, typing_context, target_context)
            pvgfi__cfmk = jcnl__lie in list_cumulative
            if jcnl__lie == '<lambda>' and len(pmma__cnit) > 1:
                jcnl__lie = '<lambda_' + str(qqd__fcg) + '>'
                qqd__fcg += 1
            out_columns.append(jcnl__lie)
            goddb__jdxy[zjyh__mejem, jcnl__lie] = jcnl__lie
            _append_out_type(grp, out_data, out_tp)
        if pvgfi__cfmk:
            index = grp.df_type.index
        else:
            index = out_tp.index
        pifff__eoce = DataFrameType(tuple(out_data), index, tuple(
            out_columns), is_table_format=True)
        return signature(pifff__eoce, *args), goddb__jdxy
    jcnl__lie = ''
    if types.unliteral(func) == types.unicode_type:
        jcnl__lie = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        jcnl__lie = bodo.utils.typing.get_builtin_function_name(func)
    if jcnl__lie:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, jcnl__lie, typing_context, kws)
    validate_udf('agg', func)
    return get_agg_typ(grp, args, 'agg', typing_context, target_context, func)


def resolve_transformative(grp, args, kws, msg, name_operation):
    index = to_numeric_index_if_range_index(grp.df_type.index)
    if isinstance(index, MultiIndexType):
        raise_bodo_error(
            f'Groupby.{name_operation}: MultiIndex input not supported for groupby operations that use input Index'
            )
    out_columns = []
    out_data = []
    if name_operation in list_cumulative:
        kws = dict(kws) if kws else {}
        wmwq__sirj = args[0] if len(args) > 0 else kws.pop('axis', 0)
        ubkl__szvg = args[1] if len(args) > 1 else kws.pop('numeric_only', 
            False)
        dmwm__aqnw = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        pzds__dqfnr = dict(axis=wmwq__sirj, numeric_only=ubkl__szvg)
        wqgfj__cnir = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', pzds__dqfnr,
            wqgfj__cnir, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        pmfy__lxat = args[0] if len(args) > 0 else kws.pop('periods', 1)
        pgyh__dvsf = args[1] if len(args) > 1 else kws.pop('freq', None)
        wmwq__sirj = args[2] if len(args) > 2 else kws.pop('axis', 0)
        thh__mjkhf = args[3] if len(args) > 3 else kws.pop('fill_value', None)
        pzds__dqfnr = dict(freq=pgyh__dvsf, axis=wmwq__sirj, fill_value=
            thh__mjkhf)
        wqgfj__cnir = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', pzds__dqfnr,
            wqgfj__cnir, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        lwfd__jwsvh = args[0] if len(args) > 0 else kws.pop('func', None)
        wokvc__qsbf = kws.pop('engine', None)
        dgd__xapao = kws.pop('engine_kwargs', None)
        pzds__dqfnr = dict(engine=wokvc__qsbf, engine_kwargs=dgd__xapao)
        wqgfj__cnir = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', pzds__dqfnr,
            wqgfj__cnir, package_name='pandas', module_name='GroupBy')
    goddb__jdxy = {}
    for wktqh__ktnuh in grp.selection:
        out_columns.append(wktqh__ktnuh)
        goddb__jdxy[wktqh__ktnuh, name_operation] = wktqh__ktnuh
        wsr__yeqkg = grp.df_type.column_index[wktqh__ktnuh]
        data = grp.df_type.data[wsr__yeqkg]
        nfy__roji = (name_operation if name_operation != 'transform' else
            get_literal_value(lwfd__jwsvh))
        if nfy__roji in ('sum', 'cumsum'):
            data = to_str_arr_if_dict_array(data)
        if name_operation == 'cumprod':
            if not isinstance(data.dtype, (types.Integer, types.Float)):
                raise BodoError(msg)
        if name_operation == 'cumsum':
            if data.dtype != types.unicode_type and data != ArrayItemArrayType(
                string_array_type) and not isinstance(data.dtype, (types.
                Integer, types.Float)):
                raise BodoError(msg)
        if name_operation in ('cummin', 'cummax'):
            if not isinstance(data.dtype, types.Integer
                ) and not is_dtype_nullable(data.dtype):
                raise BodoError(msg)
        if name_operation == 'shift':
            if isinstance(data, (TupleArrayType, ArrayItemArrayType)):
                raise BodoError(msg)
            if isinstance(data.dtype, bodo.hiframes.datetime_timedelta_ext.
                DatetimeTimeDeltaType):
                raise BodoError(
                    f"""column type of {data.dtype} is not supported in groupby built-in function shift.
{dt_err}"""
                    )
        if name_operation == 'transform':
            oyl__tfww, err_msg = get_groupby_output_dtype(data,
                get_literal_value(lwfd__jwsvh), grp.df_type.index)
            if err_msg == 'ok':
                data = oyl__tfww
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    pifff__eoce = DataFrameType(tuple(out_data), index, tuple(out_columns),
        is_table_format=True)
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        pifff__eoce = SeriesType(out_data[0].dtype, data=out_data[0], index
            =index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(pifff__eoce, *args), goddb__jdxy


def resolve_gb(grp, args, kws, func_name, typing_context, target_context,
    err_msg=''):
    if func_name in set(list_cumulative) | {'shift', 'transform'}:
        return resolve_transformative(grp, args, kws, err_msg, func_name)
    elif func_name in {'agg', 'aggregate'}:
        return resolve_agg(grp, args, kws, typing_context, target_context)
    else:
        return get_agg_typ(grp, args, func_name, typing_context,
            target_context, kws=kws)


@infer_getattr
class DataframeGroupByAttribute(OverloadedKeyAttributeTemplate):
    key = DataFrameGroupByType
    _attr_set = None

    @bound_function('groupby.agg', no_unliteral=True)
    def resolve_agg(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'agg', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.aggregate', no_unliteral=True)
    def resolve_aggregate(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'agg', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.sum', no_unliteral=True)
    def resolve_sum(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'sum', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.count', no_unliteral=True)
    def resolve_count(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'count', self.context, numba.core
            .registry.cpu_target.target_context)[0]

    @bound_function('groupby.nunique', no_unliteral=True)
    def resolve_nunique(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'nunique', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.median', no_unliteral=True)
    def resolve_median(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'median', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.mean', no_unliteral=True)
    def resolve_mean(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'mean', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.min', no_unliteral=True)
    def resolve_min(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'min', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.max', no_unliteral=True)
    def resolve_max(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'max', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.prod', no_unliteral=True)
    def resolve_prod(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'prod', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.var', no_unliteral=True)
    def resolve_var(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'var', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.std', no_unliteral=True)
    def resolve_std(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'std', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.first', no_unliteral=True)
    def resolve_first(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'first', self.context, numba.core
            .registry.cpu_target.target_context)[0]

    @bound_function('groupby.last', no_unliteral=True)
    def resolve_last(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'last', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.idxmin', no_unliteral=True)
    def resolve_idxmin(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'idxmin', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.idxmax', no_unliteral=True)
    def resolve_idxmax(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'idxmax', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.size', no_unliteral=True)
    def resolve_size(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'size', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.cumsum', no_unliteral=True)
    def resolve_cumsum(self, grp, args, kws):
        msg = (
            'Groupby.cumsum() only supports columns of types integer, float, string or liststring'
            )
        return resolve_gb(grp, args, kws, 'cumsum', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cumprod', no_unliteral=True)
    def resolve_cumprod(self, grp, args, kws):
        msg = (
            'Groupby.cumprod() only supports columns of types integer and float'
            )
        return resolve_gb(grp, args, kws, 'cumprod', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cummin', no_unliteral=True)
    def resolve_cummin(self, grp, args, kws):
        msg = (
            'Groupby.cummin() only supports columns of types integer, float, string, liststring, date, datetime or timedelta'
            )
        return resolve_gb(grp, args, kws, 'cummin', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cummax', no_unliteral=True)
    def resolve_cummax(self, grp, args, kws):
        msg = (
            'Groupby.cummax() only supports columns of types integer, float, string, liststring, date, datetime or timedelta'
            )
        return resolve_gb(grp, args, kws, 'cummax', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.shift', no_unliteral=True)
    def resolve_shift(self, grp, args, kws):
        msg = (
            'Column type of list/tuple is not supported in groupby built-in function shift'
            )
        return resolve_gb(grp, args, kws, 'shift', self.context, numba.core
            .registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.pipe', no_unliteral=True)
    def resolve_pipe(self, grp, args, kws):
        return resolve_obj_pipe(self, grp, args, kws, 'GroupBy')

    @bound_function('groupby.transform', no_unliteral=True)
    def resolve_transform(self, grp, args, kws):
        msg = (
            'Groupby.transform() only supports sum, count, min, max, mean, and std operations'
            )
        return resolve_gb(grp, args, kws, 'transform', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.head', no_unliteral=True)
    def resolve_head(self, grp, args, kws):
        msg = 'Unsupported Gropupby head operation.\n'
        return resolve_gb(grp, args, kws, 'head', self.context, numba.core.
            registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.ngroup', no_unliteral=True)
    def resolve_ngroup(self, grp, args, kws):
        msg = 'Unsupported Gropupby head operation.\n'
        return resolve_gb(grp, args, kws, 'ngroup', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.apply', no_unliteral=True)
    def resolve_apply(self, grp, args, kws):
        kws = dict(kws)
        func = args[0] if len(args) > 0 else kws.pop('func', None)
        f_args = tuple(args[1:]) if len(args) > 0 else ()
        syef__tgisq = _get_groupby_apply_udf_out_type(func, grp, f_args,
            kws, self.context, numba.core.registry.cpu_target.target_context)
        sld__ewsj = isinstance(syef__tgisq, (SeriesType,
            HeterogeneousSeriesType)
            ) and syef__tgisq.const_info is not None or not isinstance(
            syef__tgisq, (SeriesType, DataFrameType))
        if sld__ewsj:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                lpvg__mjodg = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                voeh__dvpx = tuple(grp.df_type.column_index[grp.keys[
                    pqptt__lasty]] for pqptt__lasty in range(len(grp.keys)))
                bgrmx__fdbaw = tuple(grp.df_type.data[wsr__yeqkg] for
                    wsr__yeqkg in voeh__dvpx)
                lpvg__mjodg = MultiIndexType(bgrmx__fdbaw, tuple(types.
                    literal(gld__xzyr) for gld__xzyr in grp.keys))
            else:
                wsr__yeqkg = grp.df_type.column_index[grp.keys[0]]
                lztk__rkdb = grp.df_type.data[wsr__yeqkg]
                lpvg__mjodg = bodo.hiframes.pd_index_ext.array_type_to_index(
                    lztk__rkdb, types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            hwq__miah = tuple(grp.df_type.data[grp.df_type.column_index[
                wktqh__ktnuh]] for wktqh__ktnuh in grp.keys)
            moklf__xbxn = tuple(types.literal(pfnhr__kbiex) for
                pfnhr__kbiex in grp.keys) + get_index_name_types(syef__tgisq
                .index)
            if not grp.as_index:
                hwq__miah = types.Array(types.int64, 1, 'C'),
                moklf__xbxn = (types.none,) + get_index_name_types(syef__tgisq
                    .index)
            lpvg__mjodg = MultiIndexType(hwq__miah +
                get_index_data_arr_types(syef__tgisq.index), moklf__xbxn)
        if sld__ewsj:
            if isinstance(syef__tgisq, HeterogeneousSeriesType):
                jhww__eauar, vukaw__bykt = syef__tgisq.const_info
                if isinstance(syef__tgisq.data, bodo.libs.
                    nullable_tuple_ext.NullableTupleType):
                    prgm__hbon = syef__tgisq.data.tuple_typ.types
                elif isinstance(syef__tgisq.data, types.Tuple):
                    prgm__hbon = syef__tgisq.data.types
                ibn__ttq = tuple(to_nullable_type(dtype_to_array_type(
                    akjo__iidzs)) for akjo__iidzs in prgm__hbon)
                irvlr__uqvus = DataFrameType(out_data + ibn__ttq,
                    lpvg__mjodg, out_columns + vukaw__bykt)
            elif isinstance(syef__tgisq, SeriesType):
                pwvh__sumhs, vukaw__bykt = syef__tgisq.const_info
                ibn__ttq = tuple(to_nullable_type(dtype_to_array_type(
                    syef__tgisq.dtype)) for jhww__eauar in range(pwvh__sumhs))
                irvlr__uqvus = DataFrameType(out_data + ibn__ttq,
                    lpvg__mjodg, out_columns + vukaw__bykt)
            else:
                gqf__fjp = get_udf_out_arr_type(syef__tgisq)
                if not grp.as_index:
                    irvlr__uqvus = DataFrameType(out_data + (gqf__fjp,),
                        lpvg__mjodg, out_columns + ('',))
                else:
                    irvlr__uqvus = SeriesType(gqf__fjp.dtype, gqf__fjp,
                        lpvg__mjodg, None)
        elif isinstance(syef__tgisq, SeriesType):
            irvlr__uqvus = SeriesType(syef__tgisq.dtype, syef__tgisq.data,
                lpvg__mjodg, syef__tgisq.name_typ)
        else:
            irvlr__uqvus = DataFrameType(syef__tgisq.data, lpvg__mjodg,
                syef__tgisq.columns)
        aibfk__ugc = gen_apply_pysig(len(f_args), kws.keys())
        rahl__kzt = (func, *f_args) + tuple(kws.values())
        return signature(irvlr__uqvus, *rahl__kzt).replace(pysig=aibfk__ugc)

    def generic_resolve(self, grpby, attr):
        if self._is_existing_attr(attr):
            return
        if attr not in grpby.df_type.columns:
            raise_bodo_error(
                f'groupby: invalid attribute {attr} (column not found in dataframe or unsupported function)'
                )
        return DataFrameGroupByType(grpby.df_type, grpby.keys, (attr,),
            grpby.as_index, grpby.dropna, True, True, _num_shuffle_keys=
            grpby._num_shuffle_keys)


def _get_groupby_apply_udf_out_type(func, grp, f_args, kws, typing_context,
    target_context):
    llo__mrgrg = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            mvt__qfuf = grp.selection[0]
            gqf__fjp = llo__mrgrg.data[llo__mrgrg.column_index[mvt__qfuf]]
            pvxf__gnkb = SeriesType(gqf__fjp.dtype, gqf__fjp, llo__mrgrg.
                index, types.literal(mvt__qfuf))
        else:
            nhu__ubu = tuple(llo__mrgrg.data[llo__mrgrg.column_index[
                wktqh__ktnuh]] for wktqh__ktnuh in grp.selection)
            pvxf__gnkb = DataFrameType(nhu__ubu, llo__mrgrg.index, tuple(
                grp.selection))
    else:
        pvxf__gnkb = llo__mrgrg
    uitm__dtp = pvxf__gnkb,
    uitm__dtp += tuple(f_args)
    try:
        syef__tgisq = get_const_func_output_type(func, uitm__dtp, kws,
            typing_context, target_context)
    except Exception as oxqsd__wqoc:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', oxqsd__wqoc),
            getattr(oxqsd__wqoc, 'loc', None))
    return syef__tgisq


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    uitm__dtp = (grp,) + f_args
    try:
        syef__tgisq = get_const_func_output_type(func, uitm__dtp, kws, self
            .context, numba.core.registry.cpu_target.target_context, False)
    except Exception as oxqsd__wqoc:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()',
            oxqsd__wqoc), getattr(oxqsd__wqoc, 'loc', None))
    aibfk__ugc = gen_apply_pysig(len(f_args), kws.keys())
    rahl__kzt = (func, *f_args) + tuple(kws.values())
    return signature(syef__tgisq, *rahl__kzt).replace(pysig=aibfk__ugc)


def gen_apply_pysig(n_args, kws):
    idn__tkfq = ', '.join(f'arg{pqptt__lasty}' for pqptt__lasty in range(
        n_args))
    idn__tkfq = idn__tkfq + ', ' if idn__tkfq else ''
    fiv__bhyd = ', '.join(f"{mnhsu__yfi} = ''" for mnhsu__yfi in kws)
    yldhv__ubfh = f'def apply_stub(func, {idn__tkfq}{fiv__bhyd}):\n'
    yldhv__ubfh += '    pass\n'
    qqxqt__ceg = {}
    exec(yldhv__ubfh, {}, qqxqt__ceg)
    nqryg__yxdbb = qqxqt__ceg['apply_stub']
    return numba.core.utils.pysignature(nqryg__yxdbb)


def crosstab_dummy(index, columns, _pivot_values):
    return 0


@infer_global(crosstab_dummy)
class CrossTabTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        index, columns, _pivot_values = args
        rrv__lpgf = types.Array(types.int64, 1, 'C')
        wkyuz__xcr = _pivot_values.meta
        frutl__llz = len(wkyuz__xcr)
        thkk__ddb = bodo.hiframes.pd_index_ext.array_type_to_index(index.
            data, types.StringLiteral('index'))
        zfpk__zbiw = DataFrameType((rrv__lpgf,) * frutl__llz, thkk__ddb,
            tuple(wkyuz__xcr))
        return signature(zfpk__zbiw, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    yldhv__ubfh = 'def impl(keys, dropna, _is_parallel):\n'
    yldhv__ubfh += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    yldhv__ubfh += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{pqptt__lasty}])' for pqptt__lasty in range(
        len(keys.types))))
    yldhv__ubfh += '    table = arr_info_list_to_table(info_list)\n'
    yldhv__ubfh += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    yldhv__ubfh += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    yldhv__ubfh += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    yldhv__ubfh += '    delete_table_decref_arrays(table)\n'
    yldhv__ubfh += '    ev.finalize()\n'
    yldhv__ubfh += '    return sort_idx, group_labels, ngroups\n'
    qqxqt__ceg = {}
    exec(yldhv__ubfh, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, qqxqt__ceg)
    ttd__eytcu = qqxqt__ceg['impl']
    return ttd__eytcu


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    ixka__eupu = len(labels)
    ppn__kvmzf = np.zeros(ngroups, dtype=np.int64)
    vnhzx__rdyp = np.zeros(ngroups, dtype=np.int64)
    gllur__vxe = 0
    hcfw__qup = 0
    for pqptt__lasty in range(ixka__eupu):
        brtv__fgtzt = labels[pqptt__lasty]
        if brtv__fgtzt < 0:
            gllur__vxe += 1
        else:
            hcfw__qup += 1
            if pqptt__lasty == ixka__eupu - 1 or brtv__fgtzt != labels[
                pqptt__lasty + 1]:
                ppn__kvmzf[brtv__fgtzt] = gllur__vxe
                vnhzx__rdyp[brtv__fgtzt] = gllur__vxe + hcfw__qup
                gllur__vxe += hcfw__qup
                hcfw__qup = 0
    return ppn__kvmzf, vnhzx__rdyp


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe, prefer_literal=True)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    ttd__eytcu, jhww__eauar = gen_shuffle_dataframe(df, keys, _is_parallel)
    return ttd__eytcu


def gen_shuffle_dataframe(df, keys, _is_parallel):
    pwvh__sumhs = len(df.columns)
    vtnv__daivg = len(keys.types)
    assert is_overload_constant_bool(_is_parallel
        ), 'shuffle_dataframe: _is_parallel is not a constant'
    yldhv__ubfh = 'def impl(df, keys, _is_parallel):\n'
    if is_overload_false(_is_parallel):
        yldhv__ubfh += '  return df, keys, get_null_shuffle_info()\n'
        qqxqt__ceg = {}
        exec(yldhv__ubfh, {'get_null_shuffle_info': get_null_shuffle_info},
            qqxqt__ceg)
        ttd__eytcu = qqxqt__ceg['impl']
        return ttd__eytcu
    for pqptt__lasty in range(pwvh__sumhs):
        yldhv__ubfh += f"""  in_arr{pqptt__lasty} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {pqptt__lasty})
"""
    yldhv__ubfh += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    yldhv__ubfh += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{pqptt__lasty}])' for pqptt__lasty in range(
        vtnv__daivg)), ', '.join(f'array_to_info(in_arr{pqptt__lasty})' for
        pqptt__lasty in range(pwvh__sumhs)), 'array_to_info(in_index_arr)')
    yldhv__ubfh += '  table = arr_info_list_to_table(info_list)\n'
    yldhv__ubfh += (
        f'  out_table = shuffle_table(table, {vtnv__daivg}, _is_parallel, 1)\n'
        )
    for pqptt__lasty in range(vtnv__daivg):
        yldhv__ubfh += f"""  out_key{pqptt__lasty} = info_to_array(info_from_table(out_table, {pqptt__lasty}), keys{pqptt__lasty}_typ)
"""
    for pqptt__lasty in range(pwvh__sumhs):
        yldhv__ubfh += f"""  out_arr{pqptt__lasty} = info_to_array(info_from_table(out_table, {pqptt__lasty + vtnv__daivg}), in_arr{pqptt__lasty}_typ)
"""
    yldhv__ubfh += f"""  out_arr_index = info_to_array(info_from_table(out_table, {vtnv__daivg + pwvh__sumhs}), ind_arr_typ)
"""
    yldhv__ubfh += '  shuffle_info = get_shuffle_info(out_table)\n'
    yldhv__ubfh += '  delete_table(out_table)\n'
    yldhv__ubfh += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{pqptt__lasty}' for pqptt__lasty in range
        (pwvh__sumhs))
    yldhv__ubfh += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    yldhv__ubfh += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, __col_name_meta_value_df_shuffle)
"""
    yldhv__ubfh += '  return out_df, ({},), shuffle_info\n'.format(', '.
        join(f'out_key{pqptt__lasty}' for pqptt__lasty in range(vtnv__daivg)))
    cbier__jryv = {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info, '__col_name_meta_value_df_shuffle':
        ColNamesMetaType(df.columns), 'ind_arr_typ': types.Array(types.
        int64, 1, 'C') if isinstance(df.index, RangeIndexType) else df.
        index.data}
    cbier__jryv.update({f'keys{pqptt__lasty}_typ': keys.types[pqptt__lasty] for
        pqptt__lasty in range(vtnv__daivg)})
    cbier__jryv.update({f'in_arr{pqptt__lasty}_typ': df.data[pqptt__lasty] for
        pqptt__lasty in range(pwvh__sumhs)})
    qqxqt__ceg = {}
    exec(yldhv__ubfh, cbier__jryv, qqxqt__ceg)
    ttd__eytcu = qqxqt__ceg['impl']
    return ttd__eytcu, cbier__jryv


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        cnrjg__cjp = len(data.array_types)
        yldhv__ubfh = 'def impl(data, shuffle_info):\n'
        yldhv__ubfh += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{pqptt__lasty}])' for pqptt__lasty in
            range(cnrjg__cjp)))
        yldhv__ubfh += '  table = arr_info_list_to_table(info_list)\n'
        yldhv__ubfh += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for pqptt__lasty in range(cnrjg__cjp):
            yldhv__ubfh += f"""  out_arr{pqptt__lasty} = info_to_array(info_from_table(out_table, {pqptt__lasty}), data._data[{pqptt__lasty}])
"""
        yldhv__ubfh += '  delete_table(out_table)\n'
        yldhv__ubfh += '  delete_table(table)\n'
        yldhv__ubfh += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{pqptt__lasty}' for pqptt__lasty in
            range(cnrjg__cjp))))
        qqxqt__ceg = {}
        exec(yldhv__ubfh, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, qqxqt__ceg)
        ttd__eytcu = qqxqt__ceg['impl']
        return ttd__eytcu
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            tbo__men = bodo.utils.conversion.index_to_array(data)
            adbb__lroi = reverse_shuffle(tbo__men, shuffle_info)
            return bodo.utils.conversion.index_from_array(adbb__lroi)
        return impl_index

    def impl_arr(data, shuffle_info):
        xpzdr__rwzrk = [array_to_info(data)]
        iswg__drv = arr_info_list_to_table(xpzdr__rwzrk)
        dbr__wggoh = reverse_shuffle_table(iswg__drv, shuffle_info)
        adbb__lroi = info_to_array(info_from_table(dbr__wggoh, 0), data)
        delete_table(dbr__wggoh)
        delete_table(iswg__drv)
        return adbb__lroi
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    pzds__dqfnr = dict(normalize=normalize, sort=sort, bins=bins, dropna=dropna
        )
    wqgfj__cnir = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', pzds__dqfnr, wqgfj__cnir,
        package_name='pandas', module_name='GroupBy')
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    if not is_overload_constant_bool(ascending):
        raise BodoError(
            'Groupby.value_counts() ascending must be a constant boolean')
    ixvef__rkt = get_overload_const_bool(ascending)
    pzv__wnfe = grp.selection[0]
    yldhv__ubfh = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    zknz__oeeh = (
        f"lambda S: S.value_counts(ascending={ixvef__rkt}, _index_name='{pzv__wnfe}')"
        )
    yldhv__ubfh += f'    return grp.apply({zknz__oeeh})\n'
    qqxqt__ceg = {}
    exec(yldhv__ubfh, {'bodo': bodo}, qqxqt__ceg)
    ttd__eytcu = qqxqt__ceg['impl']
    return ttd__eytcu


groupby_unsupported_attr = {'groups', 'indices'}
groupby_unsupported = {'__iter__', 'get_group', 'all', 'any', 'bfill',
    'backfill', 'cumcount', 'cummax', 'cummin', 'cumprod', 'ffill', 'nth',
    'ohlc', 'pad', 'rank', 'pct_change', 'sem', 'tail', 'corr', 'cov',
    'describe', 'diff', 'fillna', 'filter', 'hist', 'mad', 'plot',
    'quantile', 'resample', 'sample', 'skew', 'take', 'tshift'}
series_only_unsupported_attrs = {'is_monotonic_increasing',
    'is_monotonic_decreasing'}
series_only_unsupported = {'nlargest', 'nsmallest', 'unique'}
dataframe_only_unsupported = {'corrwith', 'boxplot'}


def _install_groupby_unsupported():
    for fum__gsr in groupby_unsupported_attr:
        overload_attribute(DataFrameGroupByType, fum__gsr, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{fum__gsr}'))
    for fum__gsr in groupby_unsupported:
        overload_method(DataFrameGroupByType, fum__gsr, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{fum__gsr}'))
    for fum__gsr in series_only_unsupported_attrs:
        overload_attribute(DataFrameGroupByType, fum__gsr, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{fum__gsr}'))
    for fum__gsr in series_only_unsupported:
        overload_method(DataFrameGroupByType, fum__gsr, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{fum__gsr}'))
    for fum__gsr in dataframe_only_unsupported:
        overload_method(DataFrameGroupByType, fum__gsr, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{fum__gsr}'))


_install_groupby_unsupported()
