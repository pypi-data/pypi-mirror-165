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
        eerg__oudb = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, eerg__oudb)


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
        zxp__xyrk = args[0]
        dvu__aljs = signature.return_type
        kgr__lbij = cgutils.create_struct_proxy(dvu__aljs)(context, builder)
        kgr__lbij.obj = zxp__xyrk
        context.nrt.incref(builder, signature.args[0], zxp__xyrk)
        return kgr__lbij._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for bjayx__pvut in keys:
        selection.remove(bjayx__pvut)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    if is_overload_constant_int(_num_shuffle_keys):
        jgfa__qtpmi = get_overload_const_int(_num_shuffle_keys)
    else:
        jgfa__qtpmi = -1
    dvu__aljs = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False, _num_shuffle_keys=jgfa__qtpmi)
    return dvu__aljs(obj_type, by_type, as_index_type, dropna_type,
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
        grpby, kleq__sqbdv = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(kleq__sqbdv, (tuple, list)):
                if len(set(kleq__sqbdv).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(kleq__sqbdv).difference(set(grpby.
                        df_type.columns))))
                selection = kleq__sqbdv
            else:
                if kleq__sqbdv not in grpby.df_type.columns:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(kleq__sqbdv))
                selection = kleq__sqbdv,
                series_select = True
            nfko__qdb = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True,
                series_select, _num_shuffle_keys=grpby._num_shuffle_keys)
            return signature(nfko__qdb, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, kleq__sqbdv = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(
            kleq__sqbdv):
            nfko__qdb = StaticGetItemDataFrameGroupBy.generic(self, (grpby,
                get_literal_value(kleq__sqbdv)), {}).return_type
            return signature(nfko__qdb, *args)


GetItemDataFrameGroupBy.prefer_literal = True


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    boxv__dgdk = arr_type == ArrayItemArrayType(string_array_type)
    xbsu__tihl = arr_type.dtype
    if isinstance(xbsu__tihl, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {xbsu__tihl} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(xbsu__tihl, (Decimal128Type,
        types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    if func_name in ('first', 'last', 'sum', 'prod', 'min', 'max', 'count',
        'nunique', 'head') and isinstance(arr_type, (TupleArrayType,
        ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {xbsu__tihl} is not supported in groupby built-in function {func_name}'
            )
    if func_name in {'median', 'mean', 'var', 'std'} and isinstance(xbsu__tihl,
        (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    if not isinstance(xbsu__tihl, (types.Integer, types.Float, types.Boolean)):
        if boxv__dgdk or xbsu__tihl == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last', 'head'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(xbsu__tihl, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not xbsu__tihl.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last', 'head'}:
                return (None,
                    f'column type of {xbsu__tihl} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(xbsu__tihl, types.Boolean) and func_name in {'cumsum',
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
    xbsu__tihl = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(xbsu__tihl, (
            types.Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(xbsu__tihl, types.Integer):
            return IntDtype(xbsu__tihl)
        return xbsu__tihl
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        fjj__abhnm = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{fjj__abhnm}'."
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
    for bjayx__pvut in grp.keys:
        if multi_level_names:
            fuve__ahx = bjayx__pvut, ''
        else:
            fuve__ahx = bjayx__pvut
        abm__utma = grp.df_type.column_index[bjayx__pvut]
        data = grp.df_type.data[abm__utma]
        out_columns.append(fuve__ahx)
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
        rvj__ndhlk = tuple(grp.df_type.column_index[grp.keys[jvz__grk]] for
            jvz__grk in range(len(grp.keys)))
        fhht__jiqf = tuple(grp.df_type.data[abm__utma] for abm__utma in
            rvj__ndhlk)
        index = MultiIndexType(fhht__jiqf, tuple(types.StringLiteral(
            bjayx__pvut) for bjayx__pvut in grp.keys))
    else:
        abm__utma = grp.df_type.column_index[grp.keys[0]]
        huyt__zhs = grp.df_type.data[abm__utma]
        index = bodo.hiframes.pd_index_ext.array_type_to_index(huyt__zhs,
            types.StringLiteral(grp.keys[0]))
    inhgz__yergh = {}
    wxfec__qcxs = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        inhgz__yergh[None, 'size'] = 'size'
    elif func_name == 'ngroup':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('ngroup')
        inhgz__yergh[None, 'ngroup'] = 'ngroup'
        kws = dict(kws) if kws else {}
        ascending = args[0] if len(args) > 0 else kws.pop('ascending', True)
        yje__ukp = dict(ascending=ascending)
        brzkp__wfswu = dict(ascending=True)
        check_unsupported_args(f'Groupby.{func_name}', yje__ukp,
            brzkp__wfswu, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(func_name, 1, args, kws)
    else:
        columns = (grp.selection if func_name != 'head' or grp.
            explicit_select else grp.df_type.columns)
        for gvhys__hvadc in columns:
            abm__utma = grp.df_type.column_index[gvhys__hvadc]
            data = grp.df_type.data[abm__utma]
            if func_name in ('sum', 'cumsum'):
                data = to_str_arr_if_dict_array(data)
            nsdsa__aloww = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType)
                ) and isinstance(data.dtype, (types.Integer, types.Float)):
                nsdsa__aloww = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    cylzp__mbt = SeriesType(data.dtype, data, None, string_type
                        )
                    xzl__srom = get_const_func_output_type(func, (
                        cylzp__mbt,), {}, typing_context, target_context)
                    if xzl__srom != ArrayItemArrayType(string_array_type):
                        xzl__srom = dtype_to_array_type(xzl__srom)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=gvhys__hvadc, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    qhyba__jave = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    gpaaj__gjhx = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    yje__ukp = dict(numeric_only=qhyba__jave, min_count=
                        gpaaj__gjhx)
                    brzkp__wfswu = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}', yje__ukp,
                        brzkp__wfswu, package_name='pandas', module_name=
                        'GroupBy')
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    qhyba__jave = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    gpaaj__gjhx = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    yje__ukp = dict(numeric_only=qhyba__jave, min_count=
                        gpaaj__gjhx)
                    brzkp__wfswu = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}', yje__ukp,
                        brzkp__wfswu, package_name='pandas', module_name=
                        'GroupBy')
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    qhyba__jave = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    yje__ukp = dict(numeric_only=qhyba__jave)
                    brzkp__wfswu = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}', yje__ukp,
                        brzkp__wfswu, package_name='pandas', module_name=
                        'GroupBy')
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    pqpb__ycgl = args[0] if len(args) > 0 else kws.pop('axis',
                        0)
                    ihht__erg = args[1] if len(args) > 1 else kws.pop('skipna',
                        True)
                    yje__ukp = dict(axis=pqpb__ycgl, skipna=ihht__erg)
                    brzkp__wfswu = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}', yje__ukp,
                        brzkp__wfswu, package_name='pandas', module_name=
                        'GroupBy')
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    euyct__hxsaa = args[0] if len(args) > 0 else kws.pop('ddof'
                        , 1)
                    yje__ukp = dict(ddof=euyct__hxsaa)
                    brzkp__wfswu = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}', yje__ukp,
                        brzkp__wfswu, package_name='pandas', module_name=
                        'GroupBy')
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                elif func_name == 'head':
                    if len(args) == 0:
                        kws.pop('n', None)
                xzl__srom, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                xzl__srom = to_str_arr_if_dict_array(xzl__srom
                    ) if func_name in ('sum', 'cumsum') else xzl__srom
                out_data.append(xzl__srom)
                out_columns.append(gvhys__hvadc)
                if func_name == 'agg':
                    jxoyy__auxa = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    inhgz__yergh[gvhys__hvadc, jxoyy__auxa] = gvhys__hvadc
                else:
                    inhgz__yergh[gvhys__hvadc, func_name] = gvhys__hvadc
                out_column_type.append(nsdsa__aloww)
            else:
                wxfec__qcxs.append(err_msg)
    if func_name == 'sum':
        womn__fgw = any([(dir__hxs == ColumnType.NumericalColumn.value) for
            dir__hxs in out_column_type])
        if womn__fgw:
            out_data = [dir__hxs for dir__hxs, jsoo__mel in zip(out_data,
                out_column_type) if jsoo__mel != ColumnType.
                NonNumericalColumn.value]
            out_columns = [dir__hxs for dir__hxs, jsoo__mel in zip(
                out_columns, out_column_type) if jsoo__mel != ColumnType.
                NonNumericalColumn.value]
            inhgz__yergh = {}
            for gvhys__hvadc in out_columns:
                if grp.as_index is False and gvhys__hvadc in grp.keys:
                    continue
                inhgz__yergh[gvhys__hvadc, func_name] = gvhys__hvadc
    hrsx__kjyv = len(wxfec__qcxs)
    if len(out_data) == 0:
        if hrsx__kjyv == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(hrsx__kjyv, ' was' if hrsx__kjyv == 1 else 's were',
                ','.join(wxfec__qcxs)))
    xrkgg__neur = DataFrameType(tuple(out_data), index, tuple(out_columns),
        is_table_format=True)
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index or func_name == 'ngroup'):
        if isinstance(out_data[0], IntegerArrayType):
            urxhv__gntcw = IntDtype(out_data[0].dtype)
        else:
            urxhv__gntcw = out_data[0].dtype
        lebz__epq = types.none if func_name in ('size', 'ngroup'
            ) else types.StringLiteral(grp.selection[0])
        xrkgg__neur = SeriesType(urxhv__gntcw, data=out_data[0], index=
            index, name_typ=lebz__epq)
    return signature(xrkgg__neur, *args), inhgz__yergh


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context, target_context
    ):
    uyata__nrjsz = True
    if isinstance(f_val, str):
        uyata__nrjsz = False
        lgw__modzq = f_val
    elif is_overload_constant_str(f_val):
        uyata__nrjsz = False
        lgw__modzq = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        uyata__nrjsz = False
        lgw__modzq = bodo.utils.typing.get_builtin_function_name(f_val)
    if not uyata__nrjsz:
        if lgw__modzq not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {lgw__modzq}')
        nfko__qdb = DataFrameGroupByType(grp.df_type, grp.keys, (col,), grp
            .as_index, grp.dropna, True, True, _num_shuffle_keys=grp.
            _num_shuffle_keys)
        out_tp = get_agg_typ(nfko__qdb, (), lgw__modzq, typing_context,
            target_context)[0].return_type
    else:
        if is_expr(f_val, 'make_function'):
            jgts__ohy = types.functions.MakeFunctionLiteral(f_val)
        else:
            jgts__ohy = f_val
        validate_udf('agg', jgts__ohy)
        func = get_overload_const_func(jgts__ohy, None)
        cmhd__ndmp = func.code if hasattr(func, 'code') else func.__code__
        lgw__modzq = cmhd__ndmp.co_name
        nfko__qdb = DataFrameGroupByType(grp.df_type, grp.keys, (col,), grp
            .as_index, grp.dropna, True, True, _num_shuffle_keys=grp.
            _num_shuffle_keys)
        out_tp = get_agg_typ(nfko__qdb, (), 'agg', typing_context,
            target_context, jgts__ohy)[0].return_type
    return lgw__modzq, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    jfbgh__mkkw = kws and all(isinstance(wst__zau, types.Tuple) and len(
        wst__zau) == 2 for wst__zau in kws.values())
    if is_overload_none(func) and not jfbgh__mkkw:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not jfbgh__mkkw:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    elz__wiauq = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if jfbgh__mkkw or is_overload_constant_dict(func):
        if jfbgh__mkkw:
            tls__fyt = [get_literal_value(pxnfk__sgh) for pxnfk__sgh,
                wajyq__vnk in kws.values()]
            wkncp__wttvn = [get_literal_value(iel__ovg) for wajyq__vnk,
                iel__ovg in kws.values()]
        else:
            wxbxz__qipyl = get_overload_constant_dict(func)
            tls__fyt = tuple(wxbxz__qipyl.keys())
            wkncp__wttvn = tuple(wxbxz__qipyl.values())
        for nqy__oqw in ('head', 'ngroup'):
            if nqy__oqw in wkncp__wttvn:
                raise BodoError(
                    f'Groupby.agg()/aggregate(): {nqy__oqw} cannot be mixed with other groupby operations.'
                    )
        if any(gvhys__hvadc not in grp.selection and gvhys__hvadc not in
            grp.keys for gvhys__hvadc in tls__fyt):
            raise_bodo_error(
                f'Selected column names {tls__fyt} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            wkncp__wttvn)
        if jfbgh__mkkw and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        inhgz__yergh = {}
        out_columns = []
        out_data = []
        out_column_type = []
        pqc__qtnfp = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for zldc__srh, f_val in zip(tls__fyt, wkncp__wttvn):
            if isinstance(f_val, (tuple, list)):
                wfleb__fqhpc = 0
                for jgts__ohy in f_val:
                    lgw__modzq, out_tp = get_agg_funcname_and_outtyp(grp,
                        zldc__srh, jgts__ohy, typing_context, target_context)
                    elz__wiauq = lgw__modzq in list_cumulative
                    if lgw__modzq == '<lambda>' and len(f_val) > 1:
                        lgw__modzq = '<lambda_' + str(wfleb__fqhpc) + '>'
                        wfleb__fqhpc += 1
                    out_columns.append((zldc__srh, lgw__modzq))
                    inhgz__yergh[zldc__srh, lgw__modzq] = zldc__srh, lgw__modzq
                    _append_out_type(grp, out_data, out_tp)
            else:
                lgw__modzq, out_tp = get_agg_funcname_and_outtyp(grp,
                    zldc__srh, f_val, typing_context, target_context)
                elz__wiauq = lgw__modzq in list_cumulative
                if multi_level_names:
                    out_columns.append((zldc__srh, lgw__modzq))
                    inhgz__yergh[zldc__srh, lgw__modzq] = zldc__srh, lgw__modzq
                elif not jfbgh__mkkw:
                    out_columns.append(zldc__srh)
                    inhgz__yergh[zldc__srh, lgw__modzq] = zldc__srh
                elif jfbgh__mkkw:
                    pqc__qtnfp.append(lgw__modzq)
                _append_out_type(grp, out_data, out_tp)
        if jfbgh__mkkw:
            for jvz__grk, lgrh__kcx in enumerate(kws.keys()):
                out_columns.append(lgrh__kcx)
                inhgz__yergh[tls__fyt[jvz__grk], pqc__qtnfp[jvz__grk]
                    ] = lgrh__kcx
        if elz__wiauq:
            index = grp.df_type.index
        else:
            index = out_tp.index
        xrkgg__neur = DataFrameType(tuple(out_data), index, tuple(
            out_columns), is_table_format=True)
        return signature(xrkgg__neur, *args), inhgz__yergh
    if isinstance(func, types.BaseTuple) and not isinstance(func, types.
        LiteralStrKeyDict) or is_overload_constant_list(func):
        if not (len(grp.selection) == 1 and grp.explicit_select):
            raise_bodo_error(
                'Groupby.agg()/aggregate(): must select exactly one column when more than one function is supplied'
                )
        if is_overload_constant_list(func):
            pbdm__csrv = get_overload_const_list(func)
        else:
            pbdm__csrv = func.types
        if len(pbdm__csrv) == 0:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): List of functions must contain at least 1 function'
                )
        out_data = []
        out_columns = []
        out_column_type = []
        wfleb__fqhpc = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        inhgz__yergh = {}
        sexu__ofnwc = grp.selection[0]
        for f_val in pbdm__csrv:
            lgw__modzq, out_tp = get_agg_funcname_and_outtyp(grp,
                sexu__ofnwc, f_val, typing_context, target_context)
            elz__wiauq = lgw__modzq in list_cumulative
            if lgw__modzq == '<lambda>' and len(pbdm__csrv) > 1:
                lgw__modzq = '<lambda_' + str(wfleb__fqhpc) + '>'
                wfleb__fqhpc += 1
            out_columns.append(lgw__modzq)
            inhgz__yergh[sexu__ofnwc, lgw__modzq] = lgw__modzq
            _append_out_type(grp, out_data, out_tp)
        if elz__wiauq:
            index = grp.df_type.index
        else:
            index = out_tp.index
        xrkgg__neur = DataFrameType(tuple(out_data), index, tuple(
            out_columns), is_table_format=True)
        return signature(xrkgg__neur, *args), inhgz__yergh
    lgw__modzq = ''
    if types.unliteral(func) == types.unicode_type:
        lgw__modzq = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        lgw__modzq = bodo.utils.typing.get_builtin_function_name(func)
    if lgw__modzq:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, lgw__modzq, typing_context, kws)
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
        pqpb__ycgl = args[0] if len(args) > 0 else kws.pop('axis', 0)
        qhyba__jave = args[1] if len(args) > 1 else kws.pop('numeric_only',
            False)
        ihht__erg = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        yje__ukp = dict(axis=pqpb__ycgl, numeric_only=qhyba__jave)
        brzkp__wfswu = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', yje__ukp,
            brzkp__wfswu, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        ecm__krofc = args[0] if len(args) > 0 else kws.pop('periods', 1)
        jwv__ddtm = args[1] if len(args) > 1 else kws.pop('freq', None)
        pqpb__ycgl = args[2] if len(args) > 2 else kws.pop('axis', 0)
        etkd__mcdh = args[3] if len(args) > 3 else kws.pop('fill_value', None)
        yje__ukp = dict(freq=jwv__ddtm, axis=pqpb__ycgl, fill_value=etkd__mcdh)
        brzkp__wfswu = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', yje__ukp,
            brzkp__wfswu, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        sltrc__henv = args[0] if len(args) > 0 else kws.pop('func', None)
        qli__lqx = kws.pop('engine', None)
        skyc__jhrlj = kws.pop('engine_kwargs', None)
        yje__ukp = dict(engine=qli__lqx, engine_kwargs=skyc__jhrlj)
        brzkp__wfswu = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', yje__ukp, brzkp__wfswu,
            package_name='pandas', module_name='GroupBy')
    inhgz__yergh = {}
    for gvhys__hvadc in grp.selection:
        out_columns.append(gvhys__hvadc)
        inhgz__yergh[gvhys__hvadc, name_operation] = gvhys__hvadc
        abm__utma = grp.df_type.column_index[gvhys__hvadc]
        data = grp.df_type.data[abm__utma]
        bvrqs__bebkc = (name_operation if name_operation != 'transform' else
            get_literal_value(sltrc__henv))
        if bvrqs__bebkc in ('sum', 'cumsum'):
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
            xzl__srom, err_msg = get_groupby_output_dtype(data,
                get_literal_value(sltrc__henv), grp.df_type.index)
            if err_msg == 'ok':
                data = xzl__srom
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    xrkgg__neur = DataFrameType(tuple(out_data), index, tuple(out_columns),
        is_table_format=True)
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        xrkgg__neur = SeriesType(out_data[0].dtype, data=out_data[0], index
            =index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(xrkgg__neur, *args), inhgz__yergh


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
        wtrg__cxir = _get_groupby_apply_udf_out_type(func, grp, f_args, kws,
            self.context, numba.core.registry.cpu_target.target_context)
        yjrcm__xby = isinstance(wtrg__cxir, (SeriesType,
            HeterogeneousSeriesType)
            ) and wtrg__cxir.const_info is not None or not isinstance(
            wtrg__cxir, (SeriesType, DataFrameType))
        if yjrcm__xby:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                bze__kdp = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                rvj__ndhlk = tuple(grp.df_type.column_index[grp.keys[
                    jvz__grk]] for jvz__grk in range(len(grp.keys)))
                fhht__jiqf = tuple(grp.df_type.data[abm__utma] for
                    abm__utma in rvj__ndhlk)
                bze__kdp = MultiIndexType(fhht__jiqf, tuple(types.literal(
                    bjayx__pvut) for bjayx__pvut in grp.keys))
            else:
                abm__utma = grp.df_type.column_index[grp.keys[0]]
                huyt__zhs = grp.df_type.data[abm__utma]
                bze__kdp = bodo.hiframes.pd_index_ext.array_type_to_index(
                    huyt__zhs, types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            bmop__qtuck = tuple(grp.df_type.data[grp.df_type.column_index[
                gvhys__hvadc]] for gvhys__hvadc in grp.keys)
            rreaw__qzf = tuple(types.literal(wst__zau) for wst__zau in grp.keys
                ) + get_index_name_types(wtrg__cxir.index)
            if not grp.as_index:
                bmop__qtuck = types.Array(types.int64, 1, 'C'),
                rreaw__qzf = (types.none,) + get_index_name_types(wtrg__cxir
                    .index)
            bze__kdp = MultiIndexType(bmop__qtuck +
                get_index_data_arr_types(wtrg__cxir.index), rreaw__qzf)
        if yjrcm__xby:
            if isinstance(wtrg__cxir, HeterogeneousSeriesType):
                wajyq__vnk, izv__pov = wtrg__cxir.const_info
                if isinstance(wtrg__cxir.data, bodo.libs.nullable_tuple_ext
                    .NullableTupleType):
                    otsln__txkl = wtrg__cxir.data.tuple_typ.types
                elif isinstance(wtrg__cxir.data, types.Tuple):
                    otsln__txkl = wtrg__cxir.data.types
                ztcg__bujf = tuple(to_nullable_type(dtype_to_array_type(
                    flckt__sye)) for flckt__sye in otsln__txkl)
                rkm__reez = DataFrameType(out_data + ztcg__bujf, bze__kdp, 
                    out_columns + izv__pov)
            elif isinstance(wtrg__cxir, SeriesType):
                eubb__phj, izv__pov = wtrg__cxir.const_info
                ztcg__bujf = tuple(to_nullable_type(dtype_to_array_type(
                    wtrg__cxir.dtype)) for wajyq__vnk in range(eubb__phj))
                rkm__reez = DataFrameType(out_data + ztcg__bujf, bze__kdp, 
                    out_columns + izv__pov)
            else:
                beb__ndw = get_udf_out_arr_type(wtrg__cxir)
                if not grp.as_index:
                    rkm__reez = DataFrameType(out_data + (beb__ndw,),
                        bze__kdp, out_columns + ('',))
                else:
                    rkm__reez = SeriesType(beb__ndw.dtype, beb__ndw,
                        bze__kdp, None)
        elif isinstance(wtrg__cxir, SeriesType):
            rkm__reez = SeriesType(wtrg__cxir.dtype, wtrg__cxir.data,
                bze__kdp, wtrg__cxir.name_typ)
        else:
            rkm__reez = DataFrameType(wtrg__cxir.data, bze__kdp, wtrg__cxir
                .columns)
        jlta__urjfw = gen_apply_pysig(len(f_args), kws.keys())
        uib__ergi = (func, *f_args) + tuple(kws.values())
        return signature(rkm__reez, *uib__ergi).replace(pysig=jlta__urjfw)

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
    rphq__aadae = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            zldc__srh = grp.selection[0]
            beb__ndw = rphq__aadae.data[rphq__aadae.column_index[zldc__srh]]
            ijzx__mjk = SeriesType(beb__ndw.dtype, beb__ndw, rphq__aadae.
                index, types.literal(zldc__srh))
        else:
            rss__wvqn = tuple(rphq__aadae.data[rphq__aadae.column_index[
                gvhys__hvadc]] for gvhys__hvadc in grp.selection)
            ijzx__mjk = DataFrameType(rss__wvqn, rphq__aadae.index, tuple(
                grp.selection))
    else:
        ijzx__mjk = rphq__aadae
    jur__cpjiz = ijzx__mjk,
    jur__cpjiz += tuple(f_args)
    try:
        wtrg__cxir = get_const_func_output_type(func, jur__cpjiz, kws,
            typing_context, target_context)
    except Exception as xtddi__xgtfu:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', xtddi__xgtfu),
            getattr(xtddi__xgtfu, 'loc', None))
    return wtrg__cxir


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    jur__cpjiz = (grp,) + f_args
    try:
        wtrg__cxir = get_const_func_output_type(func, jur__cpjiz, kws, self
            .context, numba.core.registry.cpu_target.target_context, False)
    except Exception as xtddi__xgtfu:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()',
            xtddi__xgtfu), getattr(xtddi__xgtfu, 'loc', None))
    jlta__urjfw = gen_apply_pysig(len(f_args), kws.keys())
    uib__ergi = (func, *f_args) + tuple(kws.values())
    return signature(wtrg__cxir, *uib__ergi).replace(pysig=jlta__urjfw)


def gen_apply_pysig(n_args, kws):
    tco__iyjb = ', '.join(f'arg{jvz__grk}' for jvz__grk in range(n_args))
    tco__iyjb = tco__iyjb + ', ' if tco__iyjb else ''
    fzf__gevm = ', '.join(f"{iyhg__arsja} = ''" for iyhg__arsja in kws)
    seksf__jbe = f'def apply_stub(func, {tco__iyjb}{fzf__gevm}):\n'
    seksf__jbe += '    pass\n'
    fyj__djg = {}
    exec(seksf__jbe, {}, fyj__djg)
    msb__nmkve = fyj__djg['apply_stub']
    return numba.core.utils.pysignature(msb__nmkve)


def crosstab_dummy(index, columns, _pivot_values):
    return 0


@infer_global(crosstab_dummy)
class CrossTabTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        index, columns, _pivot_values = args
        qkf__ntrg = types.Array(types.int64, 1, 'C')
        ofchr__lgx = _pivot_values.meta
        wxm__esk = len(ofchr__lgx)
        nykv__hebt = bodo.hiframes.pd_index_ext.array_type_to_index(index.
            data, types.StringLiteral('index'))
        rxiyg__aiuq = DataFrameType((qkf__ntrg,) * wxm__esk, nykv__hebt,
            tuple(ofchr__lgx))
        return signature(rxiyg__aiuq, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    seksf__jbe = 'def impl(keys, dropna, _is_parallel):\n'
    seksf__jbe += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    seksf__jbe += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{jvz__grk}])' for jvz__grk in range(len(keys.
        types))))
    seksf__jbe += '    table = arr_info_list_to_table(info_list)\n'
    seksf__jbe += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    seksf__jbe += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    seksf__jbe += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    seksf__jbe += '    delete_table_decref_arrays(table)\n'
    seksf__jbe += '    ev.finalize()\n'
    seksf__jbe += '    return sort_idx, group_labels, ngroups\n'
    fyj__djg = {}
    exec(seksf__jbe, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, fyj__djg)
    evgp__aps = fyj__djg['impl']
    return evgp__aps


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    lzq__rwsto = len(labels)
    nwx__eps = np.zeros(ngroups, dtype=np.int64)
    xon__oxn = np.zeros(ngroups, dtype=np.int64)
    twdk__yvdmh = 0
    ahbx__jrho = 0
    for jvz__grk in range(lzq__rwsto):
        kkvwq__hkgco = labels[jvz__grk]
        if kkvwq__hkgco < 0:
            twdk__yvdmh += 1
        else:
            ahbx__jrho += 1
            if jvz__grk == lzq__rwsto - 1 or kkvwq__hkgco != labels[
                jvz__grk + 1]:
                nwx__eps[kkvwq__hkgco] = twdk__yvdmh
                xon__oxn[kkvwq__hkgco] = twdk__yvdmh + ahbx__jrho
                twdk__yvdmh += ahbx__jrho
                ahbx__jrho = 0
    return nwx__eps, xon__oxn


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe, prefer_literal=True)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    evgp__aps, wajyq__vnk = gen_shuffle_dataframe(df, keys, _is_parallel)
    return evgp__aps


def gen_shuffle_dataframe(df, keys, _is_parallel):
    eubb__phj = len(df.columns)
    ohj__agb = len(keys.types)
    assert is_overload_constant_bool(_is_parallel
        ), 'shuffle_dataframe: _is_parallel is not a constant'
    seksf__jbe = 'def impl(df, keys, _is_parallel):\n'
    if is_overload_false(_is_parallel):
        seksf__jbe += '  return df, keys, get_null_shuffle_info()\n'
        fyj__djg = {}
        exec(seksf__jbe, {'get_null_shuffle_info': get_null_shuffle_info},
            fyj__djg)
        evgp__aps = fyj__djg['impl']
        return evgp__aps
    for jvz__grk in range(eubb__phj):
        seksf__jbe += f"""  in_arr{jvz__grk} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {jvz__grk})
"""
    seksf__jbe += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    seksf__jbe += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{jvz__grk}])' for jvz__grk in range(ohj__agb)),
        ', '.join(f'array_to_info(in_arr{jvz__grk})' for jvz__grk in range(
        eubb__phj)), 'array_to_info(in_index_arr)')
    seksf__jbe += '  table = arr_info_list_to_table(info_list)\n'
    seksf__jbe += (
        f'  out_table = shuffle_table(table, {ohj__agb}, _is_parallel, 1)\n')
    for jvz__grk in range(ohj__agb):
        seksf__jbe += f"""  out_key{jvz__grk} = info_to_array(info_from_table(out_table, {jvz__grk}), keys{jvz__grk}_typ)
"""
    for jvz__grk in range(eubb__phj):
        seksf__jbe += f"""  out_arr{jvz__grk} = info_to_array(info_from_table(out_table, {jvz__grk + ohj__agb}), in_arr{jvz__grk}_typ)
"""
    seksf__jbe += f"""  out_arr_index = info_to_array(info_from_table(out_table, {ohj__agb + eubb__phj}), ind_arr_typ)
"""
    seksf__jbe += '  shuffle_info = get_shuffle_info(out_table)\n'
    seksf__jbe += '  delete_table(out_table)\n'
    seksf__jbe += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{jvz__grk}' for jvz__grk in range(eubb__phj))
    seksf__jbe += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    seksf__jbe += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, __col_name_meta_value_df_shuffle)
"""
    seksf__jbe += '  return out_df, ({},), shuffle_info\n'.format(', '.join
        (f'out_key{jvz__grk}' for jvz__grk in range(ohj__agb)))
    mkla__kzh = {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info, '__col_name_meta_value_df_shuffle':
        ColNamesMetaType(df.columns), 'ind_arr_typ': types.Array(types.
        int64, 1, 'C') if isinstance(df.index, RangeIndexType) else df.
        index.data}
    mkla__kzh.update({f'keys{jvz__grk}_typ': keys.types[jvz__grk] for
        jvz__grk in range(ohj__agb)})
    mkla__kzh.update({f'in_arr{jvz__grk}_typ': df.data[jvz__grk] for
        jvz__grk in range(eubb__phj)})
    fyj__djg = {}
    exec(seksf__jbe, mkla__kzh, fyj__djg)
    evgp__aps = fyj__djg['impl']
    return evgp__aps, mkla__kzh


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        onjx__ysu = len(data.array_types)
        seksf__jbe = 'def impl(data, shuffle_info):\n'
        seksf__jbe += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{jvz__grk}])' for jvz__grk in range(
            onjx__ysu)))
        seksf__jbe += '  table = arr_info_list_to_table(info_list)\n'
        seksf__jbe += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for jvz__grk in range(onjx__ysu):
            seksf__jbe += f"""  out_arr{jvz__grk} = info_to_array(info_from_table(out_table, {jvz__grk}), data._data[{jvz__grk}])
"""
        seksf__jbe += '  delete_table(out_table)\n'
        seksf__jbe += '  delete_table(table)\n'
        seksf__jbe += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{jvz__grk}' for jvz__grk in range(
            onjx__ysu))))
        fyj__djg = {}
        exec(seksf__jbe, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, fyj__djg)
        evgp__aps = fyj__djg['impl']
        return evgp__aps
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            dazsx__gho = bodo.utils.conversion.index_to_array(data)
            fbvtv__slikm = reverse_shuffle(dazsx__gho, shuffle_info)
            return bodo.utils.conversion.index_from_array(fbvtv__slikm)
        return impl_index

    def impl_arr(data, shuffle_info):
        egrju__fth = [array_to_info(data)]
        trpj__fmxkv = arr_info_list_to_table(egrju__fth)
        ycugd__youvk = reverse_shuffle_table(trpj__fmxkv, shuffle_info)
        fbvtv__slikm = info_to_array(info_from_table(ycugd__youvk, 0), data)
        delete_table(ycugd__youvk)
        delete_table(trpj__fmxkv)
        return fbvtv__slikm
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    yje__ukp = dict(normalize=normalize, sort=sort, bins=bins, dropna=dropna)
    brzkp__wfswu = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', yje__ukp, brzkp__wfswu,
        package_name='pandas', module_name='GroupBy')
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    if not is_overload_constant_bool(ascending):
        raise BodoError(
            'Groupby.value_counts() ascending must be a constant boolean')
    ngym__uwo = get_overload_const_bool(ascending)
    pxf__lak = grp.selection[0]
    seksf__jbe = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    txln__apb = (
        f"lambda S: S.value_counts(ascending={ngym__uwo}, _index_name='{pxf__lak}')"
        )
    seksf__jbe += f'    return grp.apply({txln__apb})\n'
    fyj__djg = {}
    exec(seksf__jbe, {'bodo': bodo}, fyj__djg)
    evgp__aps = fyj__djg['impl']
    return evgp__aps


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
    for rwy__qqhxj in groupby_unsupported_attr:
        overload_attribute(DataFrameGroupByType, rwy__qqhxj, no_unliteral=True
            )(create_unsupported_overload(f'DataFrameGroupBy.{rwy__qqhxj}'))
    for rwy__qqhxj in groupby_unsupported:
        overload_method(DataFrameGroupByType, rwy__qqhxj, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{rwy__qqhxj}'))
    for rwy__qqhxj in series_only_unsupported_attrs:
        overload_attribute(DataFrameGroupByType, rwy__qqhxj, no_unliteral=True
            )(create_unsupported_overload(f'SeriesGroupBy.{rwy__qqhxj}'))
    for rwy__qqhxj in series_only_unsupported:
        overload_method(DataFrameGroupByType, rwy__qqhxj, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{rwy__qqhxj}'))
    for rwy__qqhxj in dataframe_only_unsupported:
        overload_method(DataFrameGroupByType, rwy__qqhxj, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{rwy__qqhxj}'))


_install_groupby_unsupported()
