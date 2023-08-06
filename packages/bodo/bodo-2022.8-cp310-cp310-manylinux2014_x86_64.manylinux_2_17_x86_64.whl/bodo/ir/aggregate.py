"""IR node for the groupby"""
import ctypes
import operator
import types as pytypes
from collections import defaultdict, namedtuple
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, compiler, ir, ir_utils, types
from numba.core.analysis import compute_use_defs
from numba.core.ir_utils import build_definitions, compile_to_numba_ir, find_callname, find_const, find_topo_order, get_definition, get_ir_of_code, get_name_var_table, guard, is_getitem, mk_unique_var, next_label, remove_dels, replace_arg_nodes, replace_var_names, replace_vars_inner, visit_vars_inner
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic
from numba.parfors.parfor import Parfor, unwrap_parfor_blocks, wrap_parfor_blocks
import bodo
from bodo.hiframes.datetime_date_ext import DatetimeDateArrayType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.libs.array import arr_info_list_to_table, array_to_info, cpp_table_to_py_data, decref_table_array, delete_info_decref_array, delete_table, delete_table_decref_arrays, groupby_and_aggregate, info_from_table, info_to_array, py_data_to_cpp_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, pre_alloc_array_item_array
from bodo.libs.binary_arr_ext import BinaryArrayType, pre_alloc_binary_array
from bodo.libs.bool_arr_ext import BooleanArrayType
from bodo.libs.decimal_arr_ext import DecimalArrayType, alloc_decimal_array
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.transforms.table_column_del_pass import _compute_table_column_uses, _find_used_columns, ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.transform import get_call_expr_arg
from bodo.utils.typing import BodoError, MetaType, decode_if_dict_array, dtype_to_array_type, get_index_data_arr_types, get_literal_value, get_overload_const_func, get_overload_const_list, get_overload_const_str, get_overload_constant_dict, is_overload_constant_dict, is_overload_constant_list, is_overload_constant_str, list_cumulative, to_str_arr_if_dict_array, type_has_unknown_cats, unwrap_typeref
from bodo.utils.utils import gen_getitem, incref, is_assign, is_call_assign, is_expr, is_null_pointer, is_var_assign
gb_agg_cfunc = {}
gb_agg_cfunc_addr = {}


@intrinsic
def add_agg_cfunc_sym(typingctx, func, sym):

    def codegen(context, builder, signature, args):
        gbqj__agpqp = func.signature
        if gbqj__agpqp == types.none(types.voidptr):
            vucmx__ztzy = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer()])
            xpbub__kkou = cgutils.get_or_insert_function(builder.module,
                vucmx__ztzy, sym._literal_value)
            builder.call(xpbub__kkou, [context.get_constant_null(
                gbqj__agpqp.args[0])])
        elif gbqj__agpqp == types.none(types.int64, types.voidptr, types.
            voidptr):
            vucmx__ztzy = lir.FunctionType(lir.VoidType(), [lir.IntType(64),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            xpbub__kkou = cgutils.get_or_insert_function(builder.module,
                vucmx__ztzy, sym._literal_value)
            builder.call(xpbub__kkou, [context.get_constant(types.int64, 0),
                context.get_constant_null(gbqj__agpqp.args[1]), context.
                get_constant_null(gbqj__agpqp.args[2])])
        else:
            vucmx__ztzy = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64).
                as_pointer()])
            xpbub__kkou = cgutils.get_or_insert_function(builder.module,
                vucmx__ztzy, sym._literal_value)
            builder.call(xpbub__kkou, [context.get_constant_null(
                gbqj__agpqp.args[0]), context.get_constant_null(gbqj__agpqp
                .args[1]), context.get_constant_null(gbqj__agpqp.args[2])])
        context.add_linking_libs([gb_agg_cfunc[sym._literal_value]._library])
        return
    return types.none(func, sym), codegen


@numba.jit
def get_agg_udf_addr(name):
    with numba.objmode(addr='int64'):
        addr = gb_agg_cfunc_addr[name]
    return addr


class AggUDFStruct(object):

    def __init__(self, regular_udf_funcs=None, general_udf_funcs=None):
        assert regular_udf_funcs is not None or general_udf_funcs is not None
        self.regular_udfs = False
        self.general_udfs = False
        self.regular_udf_cfuncs = None
        self.general_udf_cfunc = None
        if regular_udf_funcs is not None:
            (self.var_typs, self.init_func, self.update_all_func, self.
                combine_all_func, self.eval_all_func) = regular_udf_funcs
            self.regular_udfs = True
        if general_udf_funcs is not None:
            self.general_udf_funcs = general_udf_funcs
            self.general_udfs = True

    def set_regular_cfuncs(self, update_cb, combine_cb, eval_cb):
        assert self.regular_udfs and self.regular_udf_cfuncs is None
        self.regular_udf_cfuncs = [update_cb, combine_cb, eval_cb]

    def set_general_cfunc(self, general_udf_cb):
        assert self.general_udfs and self.general_udf_cfunc is None
        self.general_udf_cfunc = general_udf_cb


AggFuncStruct = namedtuple('AggFuncStruct', ['func', 'ftype'])
supported_agg_funcs = ['no_op', 'ngroup', 'head', 'transform', 'size',
    'shift', 'sum', 'count', 'nunique', 'median', 'cumsum', 'cumprod',
    'cummin', 'cummax', 'mean', 'min', 'max', 'prod', 'first', 'last',
    'idxmin', 'idxmax', 'var', 'std', 'udf', 'gen_udf']
supported_transform_funcs = ['no_op', 'sum', 'count', 'nunique', 'median',
    'mean', 'min', 'max', 'prod', 'first', 'last', 'var', 'std']


def get_agg_func(func_ir, func_name, rhs, series_type=None, typemap=None):
    if func_name == 'no_op':
        raise BodoError('Unknown aggregation function used in groupby.')
    if series_type is None:
        series_type = SeriesType(types.float64)
    if func_name in {'var', 'std'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 3
        func.ncols_post_shuffle = 4
        return func
    if func_name in {'first', 'last'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        return func
    if func_name in {'idxmin', 'idxmax'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 2
        func.ncols_post_shuffle = 2
        return func
    if func_name in supported_agg_funcs[:-8]:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        dcq__sfkkv = True
        wqrr__yuv = 1
        rebz__wtcol = -1
        if isinstance(rhs, ir.Expr):
            for jsd__nspik in rhs.kws:
                if func_name in list_cumulative:
                    if jsd__nspik[0] == 'skipna':
                        dcq__sfkkv = guard(find_const, func_ir, jsd__nspik[1])
                        if not isinstance(dcq__sfkkv, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if jsd__nspik[0] == 'dropna':
                        dcq__sfkkv = guard(find_const, func_ir, jsd__nspik[1])
                        if not isinstance(dcq__sfkkv, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            wqrr__yuv = get_call_expr_arg('shift', rhs.args, dict(rhs.kws),
                0, 'periods', wqrr__yuv)
            wqrr__yuv = guard(find_const, func_ir, wqrr__yuv)
        if func_name == 'head':
            rebz__wtcol = get_call_expr_arg('head', rhs.args, dict(rhs.kws),
                0, 'n', 5)
            if not isinstance(rebz__wtcol, int):
                rebz__wtcol = guard(find_const, func_ir, rebz__wtcol)
            if rebz__wtcol < 0:
                raise BodoError(
                    f'groupby.{func_name} does not work with negative values.')
        func.skipdropna = dcq__sfkkv
        func.periods = wqrr__yuv
        func.head_n = rebz__wtcol
        if func_name == 'transform':
            kws = dict(rhs.kws)
            zyk__vekot = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            luhy__qiqlo = typemap[zyk__vekot.name]
            chrrj__bjyup = None
            if isinstance(luhy__qiqlo, str):
                chrrj__bjyup = luhy__qiqlo
            elif is_overload_constant_str(luhy__qiqlo):
                chrrj__bjyup = get_overload_const_str(luhy__qiqlo)
            elif bodo.utils.typing.is_builtin_function(luhy__qiqlo):
                chrrj__bjyup = bodo.utils.typing.get_builtin_function_name(
                    luhy__qiqlo)
            if chrrj__bjyup not in bodo.ir.aggregate.supported_transform_funcs[
                :]:
                raise BodoError(
                    f'unsupported transform function {chrrj__bjyup}')
            func.transform_func = supported_agg_funcs.index(chrrj__bjyup)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    zyk__vekot = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if zyk__vekot == '':
        luhy__qiqlo = types.none
    else:
        luhy__qiqlo = typemap[zyk__vekot.name]
    if is_overload_constant_dict(luhy__qiqlo):
        ttct__evswk = get_overload_constant_dict(luhy__qiqlo)
        ebael__ptvzo = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in ttct__evswk.values()]
        return ebael__ptvzo
    if luhy__qiqlo == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(luhy__qiqlo, types.BaseTuple) or is_overload_constant_list(
        luhy__qiqlo):
        ebael__ptvzo = []
        qpz__llzf = 0
        if is_overload_constant_list(luhy__qiqlo):
            ojmth__rriej = get_overload_const_list(luhy__qiqlo)
        else:
            ojmth__rriej = luhy__qiqlo.types
        for t in ojmth__rriej:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                ebael__ptvzo.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>' and len(ojmth__rriej) > 1:
                    func.fname = '<lambda_' + str(qpz__llzf) + '>'
                    qpz__llzf += 1
                ebael__ptvzo.append(func)
        return [ebael__ptvzo]
    if is_overload_constant_str(luhy__qiqlo):
        func_name = get_overload_const_str(luhy__qiqlo)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(luhy__qiqlo):
        func_name = bodo.utils.typing.get_builtin_function_name(luhy__qiqlo)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    assert typemap is not None, 'typemap is required for agg UDF handling'
    func = _get_const_agg_func(typemap[rhs.args[0].name], func_ir)
    func.ftype = 'udf'
    func.fname = _get_udf_name(func)
    return func


def get_agg_func_udf(func_ir, f_val, rhs, series_type, typemap):
    if isinstance(f_val, str):
        return get_agg_func(func_ir, f_val, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(f_val):
        func_name = bodo.utils.typing.get_builtin_function_name(f_val)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if isinstance(f_val, (tuple, list)):
        qpz__llzf = 0
        olozw__snf = []
        for xpcfc__ntnl in f_val:
            func = get_agg_func_udf(func_ir, xpcfc__ntnl, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{qpz__llzf}>'
                qpz__llzf += 1
            olozw__snf.append(func)
        return olozw__snf
    else:
        assert is_expr(f_val, 'make_function') or isinstance(f_val, (numba.
            core.registry.CPUDispatcher, types.Dispatcher))
        assert typemap is not None, 'typemap is required for agg UDF handling'
        func = _get_const_agg_func(f_val, func_ir)
        func.ftype = 'udf'
        func.fname = _get_udf_name(func)
        return func


def _get_udf_name(func):
    code = func.code if hasattr(func, 'code') else func.__code__
    chrrj__bjyup = code.co_name
    return chrrj__bjyup


def _get_const_agg_func(func_typ, func_ir):
    agg_func = get_overload_const_func(func_typ, func_ir)
    if is_expr(agg_func, 'make_function'):

        def agg_func_wrapper(A):
            return A
        agg_func_wrapper.__code__ = agg_func.code
        agg_func = agg_func_wrapper
        return agg_func
    return agg_func


@infer_global(type)
class TypeDt64(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if len(args) == 1 and isinstance(args[0], (types.NPDatetime, types.
            NPTimedelta)):
            obs__aphwx = types.DType(args[0])
            return signature(obs__aphwx, *args)


class Aggregate(ir.Stmt):

    def __init__(self, df_out, df_in, key_names, gb_info_in, gb_info_out,
        out_vars, in_vars, in_key_inds, df_in_type, out_type,
        input_has_index, same_index, return_key, loc, func_name, dropna,
        _num_shuffle_keys):
        self.df_out = df_out
        self.df_in = df_in
        self.key_names = key_names
        self.gb_info_in = gb_info_in
        self.gb_info_out = gb_info_out
        self.out_vars = out_vars
        self.in_vars = in_vars
        self.in_key_inds = in_key_inds
        self.df_in_type = df_in_type
        self.out_type = out_type
        self.input_has_index = input_has_index
        self.same_index = same_index
        self.return_key = return_key
        self.loc = loc
        self.func_name = func_name
        self.dropna = dropna
        self._num_shuffle_keys = _num_shuffle_keys
        self.dead_in_inds = set()
        self.dead_out_inds = set()

    def get_live_in_vars(self):
        return [nrzwi__dyb for nrzwi__dyb in self.in_vars if nrzwi__dyb is not
            None]

    def get_live_out_vars(self):
        return [nrzwi__dyb for nrzwi__dyb in self.out_vars if nrzwi__dyb is not
            None]

    @property
    def is_in_table_format(self):
        return self.df_in_type.is_table_format

    @property
    def n_in_table_arrays(self):
        return len(self.df_in_type.columns
            ) if self.df_in_type.is_table_format else 1

    @property
    def n_in_cols(self):
        return self.n_in_table_arrays + len(self.in_vars) - 1

    @property
    def in_col_types(self):
        return list(self.df_in_type.data) + list(get_index_data_arr_types(
            self.df_in_type.index))

    @property
    def is_output_table(self):
        return not isinstance(self.out_type, SeriesType)

    @property
    def n_out_table_arrays(self):
        return len(self.out_type.table_type.arr_types) if not isinstance(self
            .out_type, SeriesType) else 1

    @property
    def n_out_cols(self):
        return self.n_out_table_arrays + len(self.out_vars) - 1

    @property
    def out_col_types(self):
        awyn__bapdj = [self.out_type.data] if isinstance(self.out_type,
            SeriesType) else list(self.out_type.table_type.arr_types)
        nsc__qave = list(get_index_data_arr_types(self.out_type.index))
        return awyn__bapdj + nsc__qave

    def update_dead_col_info(self):
        for jqlj__oimuh in self.dead_out_inds:
            self.gb_info_out.pop(jqlj__oimuh, None)
        if not self.input_has_index:
            self.dead_in_inds.add(self.n_in_cols - 1)
            self.dead_out_inds.add(self.n_out_cols - 1)
        for egcjx__iwvv, tyzvb__qtr in self.gb_info_in.copy().items():
            kjbo__ndz = []
            for xpcfc__ntnl, zsi__iiei in tyzvb__qtr:
                if zsi__iiei not in self.dead_out_inds:
                    kjbo__ndz.append((xpcfc__ntnl, zsi__iiei))
            if not kjbo__ndz:
                if (egcjx__iwvv is not None and egcjx__iwvv not in self.
                    in_key_inds):
                    self.dead_in_inds.add(egcjx__iwvv)
                self.gb_info_in.pop(egcjx__iwvv)
            else:
                self.gb_info_in[egcjx__iwvv] = kjbo__ndz
        if self.is_in_table_format:
            if not set(range(self.n_in_table_arrays)) - self.dead_in_inds:
                self.in_vars[0] = None
            for ghw__jfcd in range(1, len(self.in_vars)):
                jqlj__oimuh = self.n_in_table_arrays + ghw__jfcd - 1
                if jqlj__oimuh in self.dead_in_inds:
                    self.in_vars[ghw__jfcd] = None
        else:
            for ghw__jfcd in range(len(self.in_vars)):
                if ghw__jfcd in self.dead_in_inds:
                    self.in_vars[ghw__jfcd] = None

    def __repr__(self):
        bbglx__ndoma = ', '.join(nrzwi__dyb.name for nrzwi__dyb in self.
            get_live_in_vars())
        sapu__bpin = f'{self.df_in}{{{bbglx__ndoma}}}'
        dtec__zfsms = ', '.join(nrzwi__dyb.name for nrzwi__dyb in self.
            get_live_out_vars())
        tkcpb__xnx = f'{self.df_out}{{{dtec__zfsms}}}'
        return (
            f'Groupby (keys: {self.key_names} {self.in_key_inds}): {sapu__bpin} {tkcpb__xnx}'
            )


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({nrzwi__dyb.name for nrzwi__dyb in aggregate_node.
        get_live_in_vars()})
    def_set.update({nrzwi__dyb.name for nrzwi__dyb in aggregate_node.
        get_live_out_vars()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(agg_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    utj__hthw = agg_node.out_vars[0]
    if utj__hthw is not None and utj__hthw.name not in lives:
        agg_node.out_vars[0] = None
        if agg_node.is_output_table:
            qfez__zrhzn = set(range(agg_node.n_out_table_arrays))
            agg_node.dead_out_inds.update(qfez__zrhzn)
        else:
            agg_node.dead_out_inds.add(0)
    for ghw__jfcd in range(1, len(agg_node.out_vars)):
        nrzwi__dyb = agg_node.out_vars[ghw__jfcd]
        if nrzwi__dyb is not None and nrzwi__dyb.name not in lives:
            agg_node.out_vars[ghw__jfcd] = None
            jqlj__oimuh = agg_node.n_out_table_arrays + ghw__jfcd - 1
            agg_node.dead_out_inds.add(jqlj__oimuh)
    if all(nrzwi__dyb is None for nrzwi__dyb in agg_node.out_vars):
        return None
    agg_node.update_dead_col_info()
    return agg_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    uqynp__ufwi = {nrzwi__dyb.name for nrzwi__dyb in aggregate_node.
        get_live_out_vars()}
    return set(), uqynp__ufwi


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for ghw__jfcd in range(len(aggregate_node.in_vars)):
        if aggregate_node.in_vars[ghw__jfcd] is not None:
            aggregate_node.in_vars[ghw__jfcd] = replace_vars_inner(
                aggregate_node.in_vars[ghw__jfcd], var_dict)
    for ghw__jfcd in range(len(aggregate_node.out_vars)):
        if aggregate_node.out_vars[ghw__jfcd] is not None:
            aggregate_node.out_vars[ghw__jfcd] = replace_vars_inner(
                aggregate_node.out_vars[ghw__jfcd], var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    for ghw__jfcd in range(len(aggregate_node.in_vars)):
        if aggregate_node.in_vars[ghw__jfcd] is not None:
            aggregate_node.in_vars[ghw__jfcd] = visit_vars_inner(aggregate_node
                .in_vars[ghw__jfcd], callback, cbdata)
    for ghw__jfcd in range(len(aggregate_node.out_vars)):
        if aggregate_node.out_vars[ghw__jfcd] is not None:
            aggregate_node.out_vars[ghw__jfcd] = visit_vars_inner(
                aggregate_node.out_vars[ghw__jfcd], callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    vngs__bzir = []
    for smngq__tibtz in aggregate_node.get_live_in_vars():
        nfisr__dolox = equiv_set.get_shape(smngq__tibtz)
        if nfisr__dolox is not None:
            vngs__bzir.append(nfisr__dolox[0])
    if len(vngs__bzir) > 1:
        equiv_set.insert_equiv(*vngs__bzir)
    gvecv__ubngs = []
    vngs__bzir = []
    for smngq__tibtz in aggregate_node.get_live_out_vars():
        ybze__bnm = typemap[smngq__tibtz.name]
        mxjn__dfr = array_analysis._gen_shape_call(equiv_set, smngq__tibtz,
            ybze__bnm.ndim, None, gvecv__ubngs)
        equiv_set.insert_equiv(smngq__tibtz, mxjn__dfr)
        vngs__bzir.append(mxjn__dfr[0])
        equiv_set.define(smngq__tibtz, set())
    if len(vngs__bzir) > 1:
        equiv_set.insert_equiv(*vngs__bzir)
    return [], gvecv__ubngs


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    iue__ioh = aggregate_node.get_live_in_vars()
    tmm__kunz = aggregate_node.get_live_out_vars()
    jrsm__ykl = Distribution.OneD
    for smngq__tibtz in iue__ioh:
        jrsm__ykl = Distribution(min(jrsm__ykl.value, array_dists[
            smngq__tibtz.name].value))
    kulr__tixvo = Distribution(min(jrsm__ykl.value, Distribution.OneD_Var.
        value))
    for smngq__tibtz in tmm__kunz:
        if smngq__tibtz.name in array_dists:
            kulr__tixvo = Distribution(min(kulr__tixvo.value, array_dists[
                smngq__tibtz.name].value))
    if kulr__tixvo != Distribution.OneD_Var:
        jrsm__ykl = kulr__tixvo
    for smngq__tibtz in iue__ioh:
        array_dists[smngq__tibtz.name] = jrsm__ykl
    for smngq__tibtz in tmm__kunz:
        array_dists[smngq__tibtz.name] = kulr__tixvo


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for smngq__tibtz in agg_node.get_live_out_vars():
        definitions[smngq__tibtz.name].append(agg_node)
    return definitions


ir_utils.build_defs_extensions[Aggregate] = build_agg_definitions


def __update_redvars():
    pass


@infer_global(__update_redvars)
class UpdateDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *args)


def __combine_redvars():
    pass


@infer_global(__combine_redvars)
class CombineDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *args)


def __eval_res():
    pass


@infer_global(__eval_res)
class EvalDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(args[0].dtype, *args)


def agg_distributed_run(agg_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    parallel = False
    mapd__ynxby = agg_node.get_live_in_vars()
    mmyz__gevix = agg_node.get_live_out_vars()
    if array_dists is not None:
        parallel = True
        for nrzwi__dyb in (mapd__ynxby + mmyz__gevix):
            if array_dists[nrzwi__dyb.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                nrzwi__dyb.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    out_col_typs = agg_node.out_col_types
    in_col_typs = []
    ebael__ptvzo = []
    func_out_types = []
    for zsi__iiei, (egcjx__iwvv, func) in agg_node.gb_info_out.items():
        if egcjx__iwvv is not None:
            t = agg_node.in_col_types[egcjx__iwvv]
            in_col_typs.append(t)
        ebael__ptvzo.append(func)
        func_out_types.append(out_col_typs[zsi__iiei])
    mcsvs__feg = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for ghw__jfcd, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            mcsvs__feg.update({f'in_cat_dtype_{ghw__jfcd}': in_col_typ})
    for ghw__jfcd, tntc__muq in enumerate(out_col_typs):
        if isinstance(tntc__muq, bodo.CategoricalArrayType):
            mcsvs__feg.update({f'out_cat_dtype_{ghw__jfcd}': tntc__muq})
    udf_func_struct = get_udf_func_struct(ebael__ptvzo, in_col_typs,
        typingctx, targetctx)
    out_var_types = [(typemap[nrzwi__dyb.name] if nrzwi__dyb is not None else
        types.none) for nrzwi__dyb in agg_node.out_vars]
    ngnzf__acqgh, mfg__chdxr = gen_top_level_agg_func(agg_node, in_col_typs,
        out_col_typs, func_out_types, parallel, udf_func_struct,
        out_var_types, typemap)
    mcsvs__feg.update(mfg__chdxr)
    mcsvs__feg.update({'pd': pd, 'pre_alloc_string_array':
        pre_alloc_string_array, 'pre_alloc_binary_array':
        pre_alloc_binary_array, 'pre_alloc_array_item_array':
        pre_alloc_array_item_array, 'string_array_type': string_array_type,
        'alloc_decimal_array': alloc_decimal_array, 'array_to_info':
        array_to_info, 'arr_info_list_to_table': arr_info_list_to_table,
        'coerce_to_array': bodo.utils.conversion.coerce_to_array,
        'groupby_and_aggregate': groupby_and_aggregate, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array,
        'delete_info_decref_array': delete_info_decref_array,
        'delete_table': delete_table, 'add_agg_cfunc_sym':
        add_agg_cfunc_sym, 'get_agg_udf_addr': get_agg_udf_addr,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'decref_table_array': decref_table_array, 'decode_if_dict_array':
        decode_if_dict_array, 'set_table_data': bodo.hiframes.table.
        set_table_data, 'get_table_data': bodo.hiframes.table.
        get_table_data, 'out_typs': out_col_typs})
    if udf_func_struct is not None:
        if udf_func_struct.regular_udfs:
            mcsvs__feg.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            mcsvs__feg.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    wwq__thbyo = {}
    exec(ngnzf__acqgh, {}, wwq__thbyo)
    gnl__ouzlb = wwq__thbyo['agg_top']
    luqox__cgafc = compile_to_numba_ir(gnl__ouzlb, mcsvs__feg, typingctx=
        typingctx, targetctx=targetctx, arg_typs=tuple(typemap[nrzwi__dyb.
        name] for nrzwi__dyb in mapd__ynxby), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(luqox__cgafc, mapd__ynxby)
    eciw__hkutu = luqox__cgafc.body[-2].value.value
    fulc__kkcy = luqox__cgafc.body[:-2]
    for ghw__jfcd, nrzwi__dyb in enumerate(mmyz__gevix):
        gen_getitem(nrzwi__dyb, eciw__hkutu, ghw__jfcd, calltypes, fulc__kkcy)
    return fulc__kkcy


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        aebd__nyu = IntDtype(t.dtype).name
        assert aebd__nyu.endswith('Dtype()')
        aebd__nyu = aebd__nyu[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{aebd__nyu}'))"
            )
    elif isinstance(t, BooleanArrayType):
        return (
            'bodo.libs.bool_arr_ext.init_bool_array(np.empty(0, np.bool_), np.empty(0, np.uint8))'
            )
    elif isinstance(t, StringArrayType):
        return 'pre_alloc_string_array(1, 1)'
    elif t == bodo.dict_str_arr_type:
        return (
            'bodo.libs.dict_arr_ext.init_dict_arr(pre_alloc_string_array(1, 1), bodo.libs.int_arr_ext.alloc_int_array(1, np.int32), False)'
            )
    elif isinstance(t, BinaryArrayType):
        return 'pre_alloc_binary_array(1, 1)'
    elif t == ArrayItemArrayType(string_array_type):
        return 'pre_alloc_array_item_array(1, (1, 1), string_array_type)'
    elif isinstance(t, DecimalArrayType):
        return 'alloc_decimal_array(1, {}, {})'.format(t.precision, t.scale)
    elif isinstance(t, DatetimeDateArrayType):
        return (
            'bodo.hiframes.datetime_date_ext.init_datetime_date_array(np.empty(1, np.int64), np.empty(1, np.uint8))'
            )
    elif isinstance(t, bodo.CategoricalArrayType):
        if t.dtype.categories is None:
            raise BodoError(
                'Groupby agg operations on Categorical types require constant categories'
                )
        ccioo__iotcg = 'in' if is_input else 'out'
        return (
            f'bodo.utils.utils.alloc_type(1, {ccioo__iotcg}_cat_dtype_{colnum})'
            )
    else:
        return 'np.empty(1, {})'.format(_get_np_dtype(t.dtype))


def _get_np_dtype(t):
    if t == types.bool_:
        return 'np.bool_'
    if t == types.NPDatetime('ns'):
        return 'dt64_dtype'
    if t == types.NPTimedelta('ns'):
        return 'td64_dtype'
    return 'np.{}'.format(t)


def gen_update_cb(udf_func_struct, allfuncs, n_keys, data_in_typs_,
    do_combine, func_idx_to_in_col, label_suffix):
    mapi__lbgz = udf_func_struct.var_typs
    dycj__hduz = len(mapi__lbgz)
    ngnzf__acqgh = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    ngnzf__acqgh += '    if is_null_pointer(in_table):\n'
    ngnzf__acqgh += '        return\n'
    ngnzf__acqgh += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in mapi__lbgz]), 
        ',' if len(mapi__lbgz) == 1 else '')
    zoibg__eqm = n_keys
    foalg__pckp = []
    redvar_offsets = []
    hjs__wgu = []
    if do_combine:
        for ghw__jfcd, xpcfc__ntnl in enumerate(allfuncs):
            if xpcfc__ntnl.ftype != 'udf':
                zoibg__eqm += xpcfc__ntnl.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(zoibg__eqm, zoibg__eqm +
                    xpcfc__ntnl.n_redvars))
                zoibg__eqm += xpcfc__ntnl.n_redvars
                hjs__wgu.append(data_in_typs_[func_idx_to_in_col[ghw__jfcd]])
                foalg__pckp.append(func_idx_to_in_col[ghw__jfcd] + n_keys)
    else:
        for ghw__jfcd, xpcfc__ntnl in enumerate(allfuncs):
            if xpcfc__ntnl.ftype != 'udf':
                zoibg__eqm += xpcfc__ntnl.ncols_post_shuffle
            else:
                redvar_offsets += list(range(zoibg__eqm + 1, zoibg__eqm + 1 +
                    xpcfc__ntnl.n_redvars))
                zoibg__eqm += xpcfc__ntnl.n_redvars + 1
                hjs__wgu.append(data_in_typs_[func_idx_to_in_col[ghw__jfcd]])
                foalg__pckp.append(func_idx_to_in_col[ghw__jfcd] + n_keys)
    assert len(redvar_offsets) == dycj__hduz
    suqf__ktv = len(hjs__wgu)
    cdxjs__aeg = []
    for ghw__jfcd, t in enumerate(hjs__wgu):
        cdxjs__aeg.append(_gen_dummy_alloc(t, ghw__jfcd, True))
    ngnzf__acqgh += '    data_in_dummy = ({}{})\n'.format(','.join(
        cdxjs__aeg), ',' if len(hjs__wgu) == 1 else '')
    ngnzf__acqgh += """
    # initialize redvar cols
"""
    ngnzf__acqgh += '    init_vals = __init_func()\n'
    for ghw__jfcd in range(dycj__hduz):
        ngnzf__acqgh += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(ghw__jfcd, redvar_offsets[ghw__jfcd], ghw__jfcd))
        ngnzf__acqgh += '    incref(redvar_arr_{})\n'.format(ghw__jfcd)
        ngnzf__acqgh += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            ghw__jfcd, ghw__jfcd)
    ngnzf__acqgh += '    redvars = ({}{})\n'.format(','.join([
        'redvar_arr_{}'.format(ghw__jfcd) for ghw__jfcd in range(dycj__hduz
        )]), ',' if dycj__hduz == 1 else '')
    ngnzf__acqgh += '\n'
    for ghw__jfcd in range(suqf__ktv):
        ngnzf__acqgh += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(ghw__jfcd, foalg__pckp[ghw__jfcd], ghw__jfcd))
        ngnzf__acqgh += '    incref(data_in_{})\n'.format(ghw__jfcd)
    ngnzf__acqgh += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(ghw__jfcd) for ghw__jfcd in range(suqf__ktv)]), ',' if 
        suqf__ktv == 1 else '')
    ngnzf__acqgh += '\n'
    ngnzf__acqgh += '    for i in range(len(data_in_0)):\n'
    ngnzf__acqgh += '        w_ind = row_to_group[i]\n'
    ngnzf__acqgh += '        if w_ind != -1:\n'
    ngnzf__acqgh += (
        '            __update_redvars(redvars, data_in, w_ind, i)\n')
    wwq__thbyo = {}
    exec(ngnzf__acqgh, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, wwq__thbyo)
    return wwq__thbyo['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, label_suffix):
    mapi__lbgz = udf_func_struct.var_typs
    dycj__hduz = len(mapi__lbgz)
    ngnzf__acqgh = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    ngnzf__acqgh += '    if is_null_pointer(in_table):\n'
    ngnzf__acqgh += '        return\n'
    ngnzf__acqgh += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in mapi__lbgz]), 
        ',' if len(mapi__lbgz) == 1 else '')
    bcn__klb = n_keys
    gup__oaqe = n_keys
    npm__ycw = []
    zjcic__uumon = []
    for xpcfc__ntnl in allfuncs:
        if xpcfc__ntnl.ftype != 'udf':
            bcn__klb += xpcfc__ntnl.ncols_pre_shuffle
            gup__oaqe += xpcfc__ntnl.ncols_post_shuffle
        else:
            npm__ycw += list(range(bcn__klb, bcn__klb + xpcfc__ntnl.n_redvars))
            zjcic__uumon += list(range(gup__oaqe + 1, gup__oaqe + 1 +
                xpcfc__ntnl.n_redvars))
            bcn__klb += xpcfc__ntnl.n_redvars
            gup__oaqe += 1 + xpcfc__ntnl.n_redvars
    assert len(npm__ycw) == dycj__hduz
    ngnzf__acqgh += """
    # initialize redvar cols
"""
    ngnzf__acqgh += '    init_vals = __init_func()\n'
    for ghw__jfcd in range(dycj__hduz):
        ngnzf__acqgh += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(ghw__jfcd, zjcic__uumon[ghw__jfcd], ghw__jfcd))
        ngnzf__acqgh += '    incref(redvar_arr_{})\n'.format(ghw__jfcd)
        ngnzf__acqgh += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            ghw__jfcd, ghw__jfcd)
    ngnzf__acqgh += '    redvars = ({}{})\n'.format(','.join([
        'redvar_arr_{}'.format(ghw__jfcd) for ghw__jfcd in range(dycj__hduz
        )]), ',' if dycj__hduz == 1 else '')
    ngnzf__acqgh += '\n'
    for ghw__jfcd in range(dycj__hduz):
        ngnzf__acqgh += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(ghw__jfcd, npm__ycw[ghw__jfcd], ghw__jfcd))
        ngnzf__acqgh += '    incref(recv_redvar_arr_{})\n'.format(ghw__jfcd)
    ngnzf__acqgh += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(ghw__jfcd) for ghw__jfcd in range(
        dycj__hduz)]), ',' if dycj__hduz == 1 else '')
    ngnzf__acqgh += '\n'
    if dycj__hduz:
        ngnzf__acqgh += '    for i in range(len(recv_redvar_arr_0)):\n'
        ngnzf__acqgh += '        w_ind = row_to_group[i]\n'
        ngnzf__acqgh += (
            '        __combine_redvars(redvars, recv_redvars, w_ind, i)\n')
    wwq__thbyo = {}
    exec(ngnzf__acqgh, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, wwq__thbyo)
    return wwq__thbyo['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    mapi__lbgz = udf_func_struct.var_typs
    dycj__hduz = len(mapi__lbgz)
    zoibg__eqm = n_keys
    redvar_offsets = []
    uxm__emfiz = []
    xkz__mrok = []
    for ghw__jfcd, xpcfc__ntnl in enumerate(allfuncs):
        if xpcfc__ntnl.ftype != 'udf':
            zoibg__eqm += xpcfc__ntnl.ncols_post_shuffle
        else:
            uxm__emfiz.append(zoibg__eqm)
            redvar_offsets += list(range(zoibg__eqm + 1, zoibg__eqm + 1 +
                xpcfc__ntnl.n_redvars))
            zoibg__eqm += 1 + xpcfc__ntnl.n_redvars
            xkz__mrok.append(out_data_typs_[ghw__jfcd])
    assert len(redvar_offsets) == dycj__hduz
    suqf__ktv = len(xkz__mrok)
    ngnzf__acqgh = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    ngnzf__acqgh += '    if is_null_pointer(table):\n'
    ngnzf__acqgh += '        return\n'
    ngnzf__acqgh += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in mapi__lbgz]), 
        ',' if len(mapi__lbgz) == 1 else '')
    ngnzf__acqgh += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in xkz__mrok
        ]), ',' if len(xkz__mrok) == 1 else '')
    for ghw__jfcd in range(dycj__hduz):
        ngnzf__acqgh += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(ghw__jfcd, redvar_offsets[ghw__jfcd], ghw__jfcd))
        ngnzf__acqgh += '    incref(redvar_arr_{})\n'.format(ghw__jfcd)
    ngnzf__acqgh += '    redvars = ({}{})\n'.format(','.join([
        'redvar_arr_{}'.format(ghw__jfcd) for ghw__jfcd in range(dycj__hduz
        )]), ',' if dycj__hduz == 1 else '')
    ngnzf__acqgh += '\n'
    for ghw__jfcd in range(suqf__ktv):
        ngnzf__acqgh += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(ghw__jfcd, uxm__emfiz[ghw__jfcd], ghw__jfcd))
        ngnzf__acqgh += '    incref(data_out_{})\n'.format(ghw__jfcd)
    ngnzf__acqgh += '    data_out = ({}{})\n'.format(','.join([
        'data_out_{}'.format(ghw__jfcd) for ghw__jfcd in range(suqf__ktv)]),
        ',' if suqf__ktv == 1 else '')
    ngnzf__acqgh += '\n'
    ngnzf__acqgh += '    for i in range(len(data_out_0)):\n'
    ngnzf__acqgh += '        __eval_res(redvars, data_out, i)\n'
    wwq__thbyo = {}
    exec(ngnzf__acqgh, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, wwq__thbyo)
    return wwq__thbyo['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    zoibg__eqm = n_keys
    aswb__rmml = []
    for ghw__jfcd, xpcfc__ntnl in enumerate(allfuncs):
        if xpcfc__ntnl.ftype == 'gen_udf':
            aswb__rmml.append(zoibg__eqm)
            zoibg__eqm += 1
        elif xpcfc__ntnl.ftype != 'udf':
            zoibg__eqm += xpcfc__ntnl.ncols_post_shuffle
        else:
            zoibg__eqm += xpcfc__ntnl.n_redvars + 1
    ngnzf__acqgh = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    ngnzf__acqgh += '    if num_groups == 0:\n'
    ngnzf__acqgh += '        return\n'
    for ghw__jfcd, func in enumerate(udf_func_struct.general_udf_funcs):
        ngnzf__acqgh += '    # col {}\n'.format(ghw__jfcd)
        ngnzf__acqgh += (
            """    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)
"""
            .format(aswb__rmml[ghw__jfcd], ghw__jfcd))
        ngnzf__acqgh += '    incref(out_col)\n'
        ngnzf__acqgh += '    for j in range(num_groups):\n'
        ngnzf__acqgh += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(ghw__jfcd, ghw__jfcd))
        ngnzf__acqgh += '        incref(in_col)\n'
        ngnzf__acqgh += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(ghw__jfcd))
    mcsvs__feg = {'pd': pd, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref}
    roy__pqnxi = 0
    for ghw__jfcd, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[roy__pqnxi]
        mcsvs__feg['func_{}'.format(roy__pqnxi)] = func
        mcsvs__feg['in_col_{}_typ'.format(roy__pqnxi)] = in_col_typs[
            func_idx_to_in_col[ghw__jfcd]]
        mcsvs__feg['out_col_{}_typ'.format(roy__pqnxi)] = out_col_typs[
            ghw__jfcd]
        roy__pqnxi += 1
    wwq__thbyo = {}
    exec(ngnzf__acqgh, mcsvs__feg, wwq__thbyo)
    xpcfc__ntnl = wwq__thbyo['bodo_gb_apply_general_udfs{}'.format(
        label_suffix)]
    ucv__ewxq = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(ucv__ewxq, nopython=True)(xpcfc__ntnl)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs,
    func_out_types, parallel, udf_func_struct, out_var_types, typemap):
    n_keys = len(agg_node.in_key_inds)
    iklj__opwa = len(agg_node.out_vars)
    if agg_node.same_index:
        assert agg_node.input_has_index, 'agg codegen: input_has_index=True required for same_index=True'
    if agg_node.is_in_table_format:
        urm__mgwj = []
        if agg_node.in_vars[0] is not None:
            urm__mgwj.append('arg0')
        for ghw__jfcd in range(agg_node.n_in_table_arrays, agg_node.n_in_cols):
            if ghw__jfcd not in agg_node.dead_in_inds:
                urm__mgwj.append(f'arg{ghw__jfcd}')
    else:
        urm__mgwj = [f'arg{ghw__jfcd}' for ghw__jfcd, nrzwi__dyb in
            enumerate(agg_node.in_vars) if nrzwi__dyb is not None]
    ngnzf__acqgh = f"def agg_top({', '.join(urm__mgwj)}):\n"
    tehi__iomag = []
    if agg_node.is_in_table_format:
        tehi__iomag = agg_node.in_key_inds + [egcjx__iwvv for egcjx__iwvv,
            zan__jnghk in agg_node.gb_info_out.values() if egcjx__iwvv is not
            None]
        if agg_node.input_has_index:
            tehi__iomag.append(agg_node.n_in_cols - 1)
        mhva__wzjof = ',' if len(agg_node.in_vars) - 1 == 1 else ''
        ffl__khuro = []
        for ghw__jfcd in range(agg_node.n_in_table_arrays, agg_node.n_in_cols):
            if ghw__jfcd in agg_node.dead_in_inds:
                ffl__khuro.append('None')
            else:
                ffl__khuro.append(f'arg{ghw__jfcd}')
        xzimg__jxq = 'arg0' if agg_node.in_vars[0] is not None else 'None'
        ngnzf__acqgh += f"""    table = py_data_to_cpp_table({xzimg__jxq}, ({', '.join(ffl__khuro)}{mhva__wzjof}), in_col_inds, {agg_node.n_in_table_arrays})
"""
    else:
        xzqe__irf = [f'arg{ghw__jfcd}' for ghw__jfcd in agg_node.in_key_inds]
        uyh__dtcdq = [f'arg{egcjx__iwvv}' for egcjx__iwvv, zan__jnghk in
            agg_node.gb_info_out.values() if egcjx__iwvv is not None]
        ybmop__ivwc = xzqe__irf + uyh__dtcdq
        if agg_node.input_has_index:
            ybmop__ivwc.append(f'arg{len(agg_node.in_vars) - 1}')
        ngnzf__acqgh += '    info_list = [{}]\n'.format(', '.join(
            f'array_to_info({spl__glh})' for spl__glh in ybmop__ivwc))
        ngnzf__acqgh += '    table = arr_info_list_to_table(info_list)\n'
    do_combine = parallel
    allfuncs = []
    gotz__mwm = []
    func_idx_to_in_col = []
    tyhz__xlkbl = []
    dcq__sfkkv = False
    tmiu__uboy = 1
    rebz__wtcol = -1
    jqhmo__vygzb = 0
    anqn__nhi = 0
    ebael__ptvzo = [func for zan__jnghk, func in agg_node.gb_info_out.values()]
    for gxnwe__ktzoi, func in enumerate(ebael__ptvzo):
        gotz__mwm.append(len(allfuncs))
        if func.ftype in {'median', 'nunique', 'ngroup'}:
            do_combine = False
        if func.ftype in list_cumulative:
            jqhmo__vygzb += 1
        if hasattr(func, 'skipdropna'):
            dcq__sfkkv = func.skipdropna
        if func.ftype == 'shift':
            tmiu__uboy = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            anqn__nhi = func.transform_func
            do_combine = False
        if func.ftype == 'head':
            rebz__wtcol = func.head_n
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(gxnwe__ktzoi)
        if func.ftype == 'udf':
            tyhz__xlkbl.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            tyhz__xlkbl.append(0)
            do_combine = False
    gotz__mwm.append(len(allfuncs))
    assert len(agg_node.gb_info_out) == len(allfuncs
        ), 'invalid number of groupby outputs'
    if jqhmo__vygzb > 0:
        if jqhmo__vygzb != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    lxr__bqdcf = []
    if udf_func_struct is not None:
        nrvd__uoyl = next_label()
        if udf_func_struct.regular_udfs:
            ucv__ewxq = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            ufk__tdk = numba.cfunc(ucv__ewxq, nopython=True)(gen_update_cb(
                udf_func_struct, allfuncs, n_keys, in_col_typs, do_combine,
                func_idx_to_in_col, nrvd__uoyl))
            zrctv__ejqp = numba.cfunc(ucv__ewxq, nopython=True)(gen_combine_cb
                (udf_func_struct, allfuncs, n_keys, nrvd__uoyl))
            ualft__dqdp = numba.cfunc('void(voidptr)', nopython=True)(
                gen_eval_cb(udf_func_struct, allfuncs, n_keys,
                func_out_types, nrvd__uoyl))
            udf_func_struct.set_regular_cfuncs(ufk__tdk, zrctv__ejqp,
                ualft__dqdp)
            for rujx__irjj in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[rujx__irjj.native_name] = rujx__irjj
                gb_agg_cfunc_addr[rujx__irjj.native_name] = rujx__irjj.address
        if udf_func_struct.general_udfs:
            gwm__bkzxf = gen_general_udf_cb(udf_func_struct, allfuncs,
                n_keys, in_col_typs, func_out_types, func_idx_to_in_col,
                nrvd__uoyl)
            udf_func_struct.set_general_cfunc(gwm__bkzxf)
        mapi__lbgz = (udf_func_struct.var_typs if udf_func_struct.
            regular_udfs else None)
        yzr__kppae = 0
        ghw__jfcd = 0
        for binl__btyw, xpcfc__ntnl in zip(agg_node.gb_info_out.keys(),
            allfuncs):
            if xpcfc__ntnl.ftype in ('udf', 'gen_udf'):
                lxr__bqdcf.append(out_col_typs[binl__btyw])
                for omvwo__wzh in range(yzr__kppae, yzr__kppae +
                    tyhz__xlkbl[ghw__jfcd]):
                    lxr__bqdcf.append(dtype_to_array_type(mapi__lbgz[
                        omvwo__wzh]))
                yzr__kppae += tyhz__xlkbl[ghw__jfcd]
                ghw__jfcd += 1
        ngnzf__acqgh += f"""    dummy_table = create_dummy_table(({', '.join(f'udf_type{ghw__jfcd}' for ghw__jfcd in range(len(lxr__bqdcf)))}{',' if len(lxr__bqdcf) == 1 else ''}))
"""
        ngnzf__acqgh += f"""    udf_table_dummy = py_data_to_cpp_table(dummy_table, (), udf_dummy_col_inds, {len(lxr__bqdcf)})
"""
        if udf_func_struct.regular_udfs:
            ngnzf__acqgh += (
                f"    add_agg_cfunc_sym(cpp_cb_update, '{ufk__tdk.native_name}')\n"
                )
            ngnzf__acqgh += (
                f"    add_agg_cfunc_sym(cpp_cb_combine, '{zrctv__ejqp.native_name}')\n"
                )
            ngnzf__acqgh += (
                f"    add_agg_cfunc_sym(cpp_cb_eval, '{ualft__dqdp.native_name}')\n"
                )
            ngnzf__acqgh += (
                f"    cpp_cb_update_addr = get_agg_udf_addr('{ufk__tdk.native_name}')\n"
                )
            ngnzf__acqgh += f"""    cpp_cb_combine_addr = get_agg_udf_addr('{zrctv__ejqp.native_name}')
"""
            ngnzf__acqgh += f"""    cpp_cb_eval_addr = get_agg_udf_addr('{ualft__dqdp.native_name}')
"""
        else:
            ngnzf__acqgh += '    cpp_cb_update_addr = 0\n'
            ngnzf__acqgh += '    cpp_cb_combine_addr = 0\n'
            ngnzf__acqgh += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            rujx__irjj = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[rujx__irjj.native_name] = rujx__irjj
            gb_agg_cfunc_addr[rujx__irjj.native_name] = rujx__irjj.address
            ngnzf__acqgh += (
                f"    add_agg_cfunc_sym(cpp_cb_general, '{rujx__irjj.native_name}')\n"
                )
            ngnzf__acqgh += f"""    cpp_cb_general_addr = get_agg_udf_addr('{rujx__irjj.native_name}')
"""
        else:
            ngnzf__acqgh += '    cpp_cb_general_addr = 0\n'
    else:
        ngnzf__acqgh += """    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])
"""
        ngnzf__acqgh += '    cpp_cb_update_addr = 0\n'
        ngnzf__acqgh += '    cpp_cb_combine_addr = 0\n'
        ngnzf__acqgh += '    cpp_cb_eval_addr = 0\n'
        ngnzf__acqgh += '    cpp_cb_general_addr = 0\n'
    ngnzf__acqgh += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(
        ', '.join([str(supported_agg_funcs.index(xpcfc__ntnl.ftype)) for
        xpcfc__ntnl in allfuncs] + ['0']))
    ngnzf__acqgh += (
        f'    func_offsets = np.array({str(gotz__mwm)}, dtype=np.int32)\n')
    if len(tyhz__xlkbl) > 0:
        ngnzf__acqgh += (
            f'    udf_ncols = np.array({str(tyhz__xlkbl)}, dtype=np.int32)\n')
    else:
        ngnzf__acqgh += '    udf_ncols = np.array([0], np.int32)\n'
    ngnzf__acqgh += '    total_rows_np = np.array([0], dtype=np.int64)\n'
    ccdpq__wdf = (agg_node._num_shuffle_keys if agg_node._num_shuffle_keys !=
        -1 else n_keys)
    ngnzf__acqgh += f"""    out_table = groupby_and_aggregate(table, {n_keys}, {agg_node.input_has_index}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {parallel}, {dcq__sfkkv}, {tmiu__uboy}, {anqn__nhi}, {rebz__wtcol}, {agg_node.return_key}, {agg_node.same_index}, {agg_node.dropna}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy, total_rows_np.ctypes, {ccdpq__wdf})
"""
    kjdcl__ysqts = []
    ibdwp__elbcf = 0
    if agg_node.return_key:
        aukbo__ugc = 0 if isinstance(agg_node.out_type.index, bodo.
            RangeIndexType) else agg_node.n_out_cols - len(agg_node.in_key_inds
            ) - 1
        for ghw__jfcd in range(n_keys):
            jqlj__oimuh = aukbo__ugc + ghw__jfcd
            kjdcl__ysqts.append(jqlj__oimuh if jqlj__oimuh not in agg_node.
                dead_out_inds else -1)
            ibdwp__elbcf += 1
    for binl__btyw in agg_node.gb_info_out.keys():
        kjdcl__ysqts.append(binl__btyw)
        ibdwp__elbcf += 1
    jvii__cfqtr = False
    if agg_node.same_index:
        if agg_node.out_vars[-1] is not None:
            kjdcl__ysqts.append(agg_node.n_out_cols - 1)
        else:
            jvii__cfqtr = True
    mhva__wzjof = ',' if iklj__opwa == 1 else ''
    iouxz__kwwh = (
        f"({', '.join(f'out_type{ghw__jfcd}' for ghw__jfcd in range(iklj__opwa))}{mhva__wzjof})"
        )
    pic__gzsfa = []
    dwfd__rejf = []
    for ghw__jfcd, t in enumerate(out_col_typs):
        if ghw__jfcd not in agg_node.dead_out_inds and type_has_unknown_cats(t
            ):
            if ghw__jfcd in agg_node.gb_info_out:
                egcjx__iwvv = agg_node.gb_info_out[ghw__jfcd][0]
            else:
                assert agg_node.return_key, 'Internal error: groupby key output with unknown categoricals detected, but return_key is False'
                sidac__jndve = ghw__jfcd - aukbo__ugc
                egcjx__iwvv = agg_node.in_key_inds[sidac__jndve]
            dwfd__rejf.append(ghw__jfcd)
            if (agg_node.is_in_table_format and egcjx__iwvv < agg_node.
                n_in_table_arrays):
                pic__gzsfa.append(f'get_table_data(arg0, {egcjx__iwvv})')
            else:
                pic__gzsfa.append(f'arg{egcjx__iwvv}')
    mhva__wzjof = ',' if len(pic__gzsfa) == 1 else ''
    ngnzf__acqgh += f"""    out_data = cpp_table_to_py_data(out_table, out_col_inds, {iouxz__kwwh}, total_rows_np[0], {agg_node.n_out_table_arrays}, ({', '.join(pic__gzsfa)}{mhva__wzjof}), unknown_cat_out_inds)
"""
    ngnzf__acqgh += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    ngnzf__acqgh += '    delete_table_decref_arrays(table)\n'
    ngnzf__acqgh += '    delete_table_decref_arrays(udf_table_dummy)\n'
    if agg_node.return_key:
        for ghw__jfcd in range(n_keys):
            if kjdcl__ysqts[ghw__jfcd] == -1:
                ngnzf__acqgh += (
                    f'    decref_table_array(out_table, {ghw__jfcd})\n')
    if jvii__cfqtr:
        otuzt__mxiz = len(agg_node.gb_info_out) + (n_keys if agg_node.
            return_key else 0)
        ngnzf__acqgh += f'    decref_table_array(out_table, {otuzt__mxiz})\n'
    ngnzf__acqgh += '    delete_table(out_table)\n'
    ngnzf__acqgh += '    ev_clean.finalize()\n'
    ngnzf__acqgh += '    return out_data\n'
    wtnar__nspg = {f'out_type{ghw__jfcd}': out_var_types[ghw__jfcd] for
        ghw__jfcd in range(iklj__opwa)}
    wtnar__nspg['out_col_inds'] = MetaType(tuple(kjdcl__ysqts))
    wtnar__nspg['in_col_inds'] = MetaType(tuple(tehi__iomag))
    wtnar__nspg['cpp_table_to_py_data'] = cpp_table_to_py_data
    wtnar__nspg['py_data_to_cpp_table'] = py_data_to_cpp_table
    wtnar__nspg.update({f'udf_type{ghw__jfcd}': t for ghw__jfcd, t in
        enumerate(lxr__bqdcf)})
    wtnar__nspg['udf_dummy_col_inds'] = MetaType(tuple(range(len(lxr__bqdcf))))
    wtnar__nspg['create_dummy_table'] = create_dummy_table
    wtnar__nspg['unknown_cat_out_inds'] = MetaType(tuple(dwfd__rejf))
    wtnar__nspg['get_table_data'] = bodo.hiframes.table.get_table_data
    return ngnzf__acqgh, wtnar__nspg


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def create_dummy_table(data_types):
    acr__qxoj = tuple(unwrap_typeref(data_types.types[ghw__jfcd]) for
        ghw__jfcd in range(len(data_types.types)))
    edohx__pdvue = bodo.TableType(acr__qxoj)
    wtnar__nspg = {'table_type': edohx__pdvue}
    ngnzf__acqgh = 'def impl(data_types):\n'
    ngnzf__acqgh += '  py_table = init_table(table_type, False)\n'
    ngnzf__acqgh += '  py_table = set_table_len(py_table, 1)\n'
    for ybze__bnm, sipv__vseas in edohx__pdvue.type_to_blk.items():
        wtnar__nspg[f'typ_list_{sipv__vseas}'] = types.List(ybze__bnm)
        wtnar__nspg[f'typ_{sipv__vseas}'] = ybze__bnm
        qnt__ygxbh = len(edohx__pdvue.block_to_arr_ind[sipv__vseas])
        ngnzf__acqgh += f"""  arr_list_{sipv__vseas} = alloc_list_like(typ_list_{sipv__vseas}, {qnt__ygxbh}, False)
"""
        ngnzf__acqgh += f'  for i in range(len(arr_list_{sipv__vseas})):\n'
        ngnzf__acqgh += (
            f'    arr_list_{sipv__vseas}[i] = alloc_type(1, typ_{sipv__vseas}, (-1,))\n'
            )
        ngnzf__acqgh += f"""  py_table = set_table_block(py_table, arr_list_{sipv__vseas}, {sipv__vseas})
"""
    ngnzf__acqgh += '  return py_table\n'
    wtnar__nspg.update({'init_table': bodo.hiframes.table.init_table,
        'alloc_list_like': bodo.hiframes.table.alloc_list_like,
        'set_table_block': bodo.hiframes.table.set_table_block,
        'set_table_len': bodo.hiframes.table.set_table_len, 'alloc_type':
        bodo.utils.utils.alloc_type})
    wwq__thbyo = {}
    exec(ngnzf__acqgh, wtnar__nspg, wwq__thbyo)
    return wwq__thbyo['impl']


def agg_table_column_use(agg_node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    if not agg_node.is_in_table_format or agg_node.in_vars[0] is None:
        return
    dzjj__mqcd = agg_node.in_vars[0].name
    wss__ajkpr, cejc__njybv, fmqy__uhj = block_use_map[dzjj__mqcd]
    if cejc__njybv or fmqy__uhj:
        return
    if agg_node.is_output_table and agg_node.out_vars[0] is not None:
        jrie__hqzpx, ftba__hmf, igxp__ljxcr = _compute_table_column_uses(
            agg_node.out_vars[0].name, table_col_use_map, equiv_vars)
        if ftba__hmf or igxp__ljxcr:
            jrie__hqzpx = set(range(agg_node.n_out_table_arrays))
    else:
        jrie__hqzpx = {}
        if agg_node.out_vars[0
            ] is not None and 0 not in agg_node.dead_out_inds:
            jrie__hqzpx = {0}
    clve__erxz = set(ghw__jfcd for ghw__jfcd in agg_node.in_key_inds if 
        ghw__jfcd < agg_node.n_in_table_arrays)
    aks__fxy = set(agg_node.gb_info_out[ghw__jfcd][0] for ghw__jfcd in
        jrie__hqzpx if ghw__jfcd in agg_node.gb_info_out and agg_node.
        gb_info_out[ghw__jfcd][0] is not None)
    aks__fxy |= clve__erxz | wss__ajkpr
    vdruo__mae = len(set(range(agg_node.n_in_table_arrays)) - aks__fxy) == 0
    block_use_map[dzjj__mqcd] = aks__fxy, vdruo__mae, False


ir_extension_table_column_use[Aggregate] = agg_table_column_use


def agg_remove_dead_column(agg_node, column_live_map, equiv_vars, typemap):
    if not agg_node.is_output_table or agg_node.out_vars[0] is None:
        return False
    nkzl__hmk = agg_node.n_out_table_arrays
    fkon__ctzme = agg_node.out_vars[0].name
    bxqg__lyiu = _find_used_columns(fkon__ctzme, nkzl__hmk, column_live_map,
        equiv_vars)
    if bxqg__lyiu is None:
        return False
    rvuqi__hgfv = set(range(nkzl__hmk)) - bxqg__lyiu
    dwey__let = len(rvuqi__hgfv - agg_node.dead_out_inds) != 0
    if dwey__let:
        agg_node.dead_out_inds.update(rvuqi__hgfv)
        agg_node.update_dead_col_info()
    return dwey__let


remove_dead_column_extensions[Aggregate] = agg_remove_dead_column


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for vqhy__zgatg in block.body:
            if is_call_assign(vqhy__zgatg) and find_callname(f_ir,
                vqhy__zgatg.value) == ('len', 'builtins'
                ) and vqhy__zgatg.value.args[0].name == f_ir.arg_names[0]:
                vdc__efnf = get_definition(f_ir, vqhy__zgatg.value.func)
                vdc__efnf.name = 'dummy_agg_count'
                vdc__efnf.value = dummy_agg_count
    zjqlq__jxcq = get_name_var_table(f_ir.blocks)
    mkpao__ggzrs = {}
    for name, zan__jnghk in zjqlq__jxcq.items():
        mkpao__ggzrs[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, mkpao__ggzrs)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    suq__yqem = numba.core.compiler.Flags()
    suq__yqem.nrt = True
    qlzt__quc = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, suq__yqem)
    qlzt__quc.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, ugmk__eeaq, calltypes, zan__jnghk = (numba.core.typed_passes.
        type_inference_stage(typingctx, targetctx, f_ir, arg_typs, None))
    cks__vyyr = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    touwz__qexpr = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    lkiqt__dyol = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    ylk__jawh = lkiqt__dyol(typemap, calltypes)
    pm = touwz__qexpr(typingctx, targetctx, None, f_ir, typemap, ugmk__eeaq,
        calltypes, ylk__jawh, {}, suq__yqem, None)
    avi__gmqcn = (numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline(pm))
    pm = touwz__qexpr(typingctx, targetctx, None, f_ir, typemap, ugmk__eeaq,
        calltypes, ylk__jawh, {}, suq__yqem, avi__gmqcn)
    ypmp__iqkt = numba.core.typed_passes.InlineOverloads()
    ypmp__iqkt.run_pass(pm)
    cqoml__phmdc = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    cqoml__phmdc.run()
    for block in f_ir.blocks.values():
        for vqhy__zgatg in block.body:
            if is_assign(vqhy__zgatg) and isinstance(vqhy__zgatg.value, (ir
                .Arg, ir.Var)) and isinstance(typemap[vqhy__zgatg.target.
                name], SeriesType):
                ybze__bnm = typemap.pop(vqhy__zgatg.target.name)
                typemap[vqhy__zgatg.target.name] = ybze__bnm.data
            if is_call_assign(vqhy__zgatg) and find_callname(f_ir,
                vqhy__zgatg.value) == ('get_series_data',
                'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[vqhy__zgatg.target.name].remove(vqhy__zgatg
                    .value)
                vqhy__zgatg.value = vqhy__zgatg.value.args[0]
                f_ir._definitions[vqhy__zgatg.target.name].append(vqhy__zgatg
                    .value)
            if is_call_assign(vqhy__zgatg) and find_callname(f_ir,
                vqhy__zgatg.value) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[vqhy__zgatg.target.name].remove(vqhy__zgatg
                    .value)
                vqhy__zgatg.value = ir.Const(False, vqhy__zgatg.loc)
                f_ir._definitions[vqhy__zgatg.target.name].append(vqhy__zgatg
                    .value)
            if is_call_assign(vqhy__zgatg) and find_callname(f_ir,
                vqhy__zgatg.value) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[vqhy__zgatg.target.name].remove(vqhy__zgatg
                    .value)
                vqhy__zgatg.value = ir.Const(False, vqhy__zgatg.loc)
                f_ir._definitions[vqhy__zgatg.target.name].append(vqhy__zgatg
                    .value)
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    plfuz__ayb = numba.parfors.parfor.PreParforPass(f_ir, typemap,
        calltypes, typingctx, targetctx, cks__vyyr)
    plfuz__ayb.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    fqbi__kyml = numba.core.compiler.StateDict()
    fqbi__kyml.func_ir = f_ir
    fqbi__kyml.typemap = typemap
    fqbi__kyml.calltypes = calltypes
    fqbi__kyml.typingctx = typingctx
    fqbi__kyml.targetctx = targetctx
    fqbi__kyml.return_type = ugmk__eeaq
    numba.core.rewrites.rewrite_registry.apply('after-inference', fqbi__kyml)
    lvdvb__zlrvz = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        ugmk__eeaq, typingctx, targetctx, cks__vyyr, suq__yqem, {})
    lvdvb__zlrvz.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            mas__dlwul = ctypes.pythonapi.PyCell_Get
            mas__dlwul.restype = ctypes.py_object
            mas__dlwul.argtypes = ctypes.py_object,
            ttct__evswk = tuple(mas__dlwul(spt__vzld) for spt__vzld in closure)
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            ttct__evswk = closure.items
        assert len(code.co_freevars) == len(ttct__evswk)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks,
            ttct__evswk)


class RegularUDFGenerator:

    def __init__(self, in_col_types, typingctx, targetctx):
        self.in_col_types = in_col_types
        self.typingctx = typingctx
        self.targetctx = targetctx
        self.all_reduce_vars = []
        self.all_vartypes = []
        self.all_init_nodes = []
        self.all_eval_funcs = []
        self.all_update_funcs = []
        self.all_combine_funcs = []
        self.curr_offset = 0
        self.redvar_offsets = [0]

    def add_udf(self, in_col_typ, func):
        eghge__dbffc = SeriesType(in_col_typ.dtype,
            to_str_arr_if_dict_array(in_col_typ), None, string_type)
        f_ir, pm = compile_to_optimized_ir(func, (eghge__dbffc,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        dsmy__cnqw, arr_var = _rm_arg_agg_block(block, pm.typemap)
        obdgr__cuppx = -1
        for ghw__jfcd, vqhy__zgatg in enumerate(dsmy__cnqw):
            if isinstance(vqhy__zgatg, numba.parfors.parfor.Parfor):
                assert obdgr__cuppx == -1, 'only one parfor for aggregation function'
                obdgr__cuppx = ghw__jfcd
        parfor = None
        if obdgr__cuppx != -1:
            parfor = dsmy__cnqw[obdgr__cuppx]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = dsmy__cnqw[:obdgr__cuppx] + parfor.init_block.body
        eval_nodes = dsmy__cnqw[obdgr__cuppx + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for vqhy__zgatg in init_nodes:
            if is_assign(vqhy__zgatg) and vqhy__zgatg.target.name in redvars:
                ind = redvars.index(vqhy__zgatg.target.name)
                reduce_vars[ind] = vqhy__zgatg.target
        var_types = [pm.typemap[nrzwi__dyb] for nrzwi__dyb in redvars]
        ion__mtifk = gen_combine_func(f_ir, parfor, redvars, var_to_redvar,
            var_types, arr_var, pm, self.typingctx, self.targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        ekdw__qai = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        emsk__ocsr = gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types,
            pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(emsk__ocsr)
        self.all_update_funcs.append(ekdw__qai)
        self.all_combine_funcs.append(ion__mtifk)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        lje__cfs = gen_init_func(self.all_init_nodes, self.all_reduce_vars,
            self.all_vartypes, self.typingctx, self.targetctx)
        xth__zmnl = gen_all_update_func(self.all_update_funcs, self.
            in_col_types, self.redvar_offsets)
        sssw__avxp = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.targetctx)
        amnj__obwa = gen_all_eval_func(self.all_eval_funcs, self.redvar_offsets
            )
        return self.all_vartypes, lje__cfs, xth__zmnl, sssw__avxp, amnj__obwa


class GeneralUDFGenerator(object):

    def __init__(self):
        self.funcs = []

    def add_udf(self, func):
        self.funcs.append(bodo.jit(distributed=False)(func))
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        func.n_redvars = 0

    def gen_all_func(self):
        if len(self.funcs) > 0:
            return self.funcs
        else:
            return None


def get_udf_func_struct(agg_func, in_col_types, typingctx, targetctx):
    phg__dqtce = []
    for t, xpcfc__ntnl in zip(in_col_types, agg_func):
        phg__dqtce.append((t, xpcfc__ntnl))
    ebuy__ubyqz = RegularUDFGenerator(in_col_types, typingctx, targetctx)
    znmix__lshk = GeneralUDFGenerator()
    for in_col_typ, func in phg__dqtce:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            ebuy__ubyqz.add_udf(in_col_typ, func)
        except:
            znmix__lshk.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = ebuy__ubyqz.gen_all_func()
    general_udf_funcs = znmix__lshk.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    ojyc__kice = compute_use_defs(parfor.loop_body)
    qtd__vbfho = set()
    for eyuuv__bfxg in ojyc__kice.usemap.values():
        qtd__vbfho |= eyuuv__bfxg
    rvztu__nwyuy = set()
    for eyuuv__bfxg in ojyc__kice.defmap.values():
        rvztu__nwyuy |= eyuuv__bfxg
    cfd__rsy = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    cfd__rsy.body = eval_nodes
    nqrwd__jfgio = compute_use_defs({(0): cfd__rsy})
    qjpch__xryq = nqrwd__jfgio.usemap[0]
    swton__pgyxn = set()
    pehq__war = []
    dqu__ickz = []
    for vqhy__zgatg in reversed(init_nodes):
        gzzkj__dby = {nrzwi__dyb.name for nrzwi__dyb in vqhy__zgatg.list_vars()
            }
        if is_assign(vqhy__zgatg):
            nrzwi__dyb = vqhy__zgatg.target.name
            gzzkj__dby.remove(nrzwi__dyb)
            if (nrzwi__dyb in qtd__vbfho and nrzwi__dyb not in swton__pgyxn and
                nrzwi__dyb not in qjpch__xryq and nrzwi__dyb not in
                rvztu__nwyuy):
                dqu__ickz.append(vqhy__zgatg)
                qtd__vbfho |= gzzkj__dby
                rvztu__nwyuy.add(nrzwi__dyb)
                continue
        swton__pgyxn |= gzzkj__dby
        pehq__war.append(vqhy__zgatg)
    dqu__ickz.reverse()
    pehq__war.reverse()
    vtp__xyjg = min(parfor.loop_body.keys())
    hze__gvi = parfor.loop_body[vtp__xyjg]
    hze__gvi.body = dqu__ickz + hze__gvi.body
    return pehq__war


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    wvwxo__sayp = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    ffek__bheiy = set()
    uprkz__gnaoh = []
    for vqhy__zgatg in init_nodes:
        if is_assign(vqhy__zgatg) and isinstance(vqhy__zgatg.value, ir.Global
            ) and isinstance(vqhy__zgatg.value.value, pytypes.FunctionType
            ) and vqhy__zgatg.value.value in wvwxo__sayp:
            ffek__bheiy.add(vqhy__zgatg.target.name)
        elif is_call_assign(vqhy__zgatg
            ) and vqhy__zgatg.value.func.name in ffek__bheiy:
            pass
        else:
            uprkz__gnaoh.append(vqhy__zgatg)
    init_nodes = uprkz__gnaoh
    ppr__ytdje = types.Tuple(var_types)
    zrz__qdrg = lambda : None
    f_ir = compile_to_numba_ir(zrz__qdrg, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    zwx__pfjw = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    vrgjg__ecg = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc), zwx__pfjw,
        loc)
    block.body = block.body[-2:]
    block.body = init_nodes + [vrgjg__ecg] + block.body
    block.body[-2].value.value = zwx__pfjw
    pdbri__vprtz = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        ppr__ytdje, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    glf__gknic = numba.core.target_extension.dispatcher_registry[cpu_target](
        zrz__qdrg)
    glf__gknic.add_overload(pdbri__vprtz)
    return glf__gknic


def gen_all_update_func(update_funcs, in_col_types, redvar_offsets):
    upccf__bkk = len(update_funcs)
    zakwd__vwq = len(in_col_types)
    ngnzf__acqgh = 'def update_all_f(redvar_arrs, data_in, w_ind, i):\n'
    for omvwo__wzh in range(upccf__bkk):
        ejz__jdwm = ', '.join(['redvar_arrs[{}][w_ind]'.format(ghw__jfcd) for
            ghw__jfcd in range(redvar_offsets[omvwo__wzh], redvar_offsets[
            omvwo__wzh + 1])])
        if ejz__jdwm:
            ngnzf__acqgh += ('  {} = update_vars_{}({},  data_in[{}][i])\n'
                .format(ejz__jdwm, omvwo__wzh, ejz__jdwm, 0 if zakwd__vwq ==
                1 else omvwo__wzh))
    ngnzf__acqgh += '  return\n'
    mcsvs__feg = {}
    for ghw__jfcd, xpcfc__ntnl in enumerate(update_funcs):
        mcsvs__feg['update_vars_{}'.format(ghw__jfcd)] = xpcfc__ntnl
    wwq__thbyo = {}
    exec(ngnzf__acqgh, mcsvs__feg, wwq__thbyo)
    why__dsgds = wwq__thbyo['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(why__dsgds)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx):
    gew__zsyb = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types])
    arg_typs = gew__zsyb, gew__zsyb, types.intp, types.intp
    npvy__yssrv = len(redvar_offsets) - 1
    ngnzf__acqgh = 'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i):\n'
    for omvwo__wzh in range(npvy__yssrv):
        ejz__jdwm = ', '.join(['redvar_arrs[{}][w_ind]'.format(ghw__jfcd) for
            ghw__jfcd in range(redvar_offsets[omvwo__wzh], redvar_offsets[
            omvwo__wzh + 1])])
        qtlx__mzr = ', '.join(['recv_arrs[{}][i]'.format(ghw__jfcd) for
            ghw__jfcd in range(redvar_offsets[omvwo__wzh], redvar_offsets[
            omvwo__wzh + 1])])
        if qtlx__mzr:
            ngnzf__acqgh += '  {} = combine_vars_{}({}, {})\n'.format(ejz__jdwm
                , omvwo__wzh, ejz__jdwm, qtlx__mzr)
    ngnzf__acqgh += '  return\n'
    mcsvs__feg = {}
    for ghw__jfcd, xpcfc__ntnl in enumerate(combine_funcs):
        mcsvs__feg['combine_vars_{}'.format(ghw__jfcd)] = xpcfc__ntnl
    wwq__thbyo = {}
    exec(ngnzf__acqgh, mcsvs__feg, wwq__thbyo)
    nqtvs__iegxy = wwq__thbyo['combine_all_f']
    f_ir = compile_to_numba_ir(nqtvs__iegxy, mcsvs__feg)
    sssw__avxp = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    glf__gknic = numba.core.target_extension.dispatcher_registry[cpu_target](
        nqtvs__iegxy)
    glf__gknic.add_overload(sssw__avxp)
    return glf__gknic


def gen_all_eval_func(eval_funcs, redvar_offsets):
    npvy__yssrv = len(redvar_offsets) - 1
    ngnzf__acqgh = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    for omvwo__wzh in range(npvy__yssrv):
        ejz__jdwm = ', '.join(['redvar_arrs[{}][j]'.format(ghw__jfcd) for
            ghw__jfcd in range(redvar_offsets[omvwo__wzh], redvar_offsets[
            omvwo__wzh + 1])])
        ngnzf__acqgh += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(
            omvwo__wzh, omvwo__wzh, ejz__jdwm)
    ngnzf__acqgh += '  return\n'
    mcsvs__feg = {}
    for ghw__jfcd, xpcfc__ntnl in enumerate(eval_funcs):
        mcsvs__feg['eval_vars_{}'.format(ghw__jfcd)] = xpcfc__ntnl
    wwq__thbyo = {}
    exec(ngnzf__acqgh, mcsvs__feg, wwq__thbyo)
    gcxc__npw = wwq__thbyo['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(gcxc__npw)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    olrrw__ywza = len(var_types)
    ljwu__ppl = [f'in{ghw__jfcd}' for ghw__jfcd in range(olrrw__ywza)]
    ppr__ytdje = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    jvjz__ygup = ppr__ytdje(0)
    ngnzf__acqgh = 'def agg_eval({}):\n return _zero\n'.format(', '.join(
        ljwu__ppl))
    wwq__thbyo = {}
    exec(ngnzf__acqgh, {'_zero': jvjz__ygup}, wwq__thbyo)
    rsyfc__lwvlh = wwq__thbyo['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(rsyfc__lwvlh, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': jvjz__ygup}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    tojb__ixwhu = []
    for ghw__jfcd, nrzwi__dyb in enumerate(reduce_vars):
        tojb__ixwhu.append(ir.Assign(block.body[ghw__jfcd].target,
            nrzwi__dyb, nrzwi__dyb.loc))
        for tpj__vlk in nrzwi__dyb.versioned_names:
            tojb__ixwhu.append(ir.Assign(nrzwi__dyb, ir.Var(nrzwi__dyb.
                scope, tpj__vlk, nrzwi__dyb.loc), nrzwi__dyb.loc))
    block.body = block.body[:olrrw__ywza] + tojb__ixwhu + eval_nodes
    emsk__ocsr = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        ppr__ytdje, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    glf__gknic = numba.core.target_extension.dispatcher_registry[cpu_target](
        rsyfc__lwvlh)
    glf__gknic.add_overload(emsk__ocsr)
    return glf__gknic


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    olrrw__ywza = len(redvars)
    alvuu__mytz = [f'v{ghw__jfcd}' for ghw__jfcd in range(olrrw__ywza)]
    ljwu__ppl = [f'in{ghw__jfcd}' for ghw__jfcd in range(olrrw__ywza)]
    ngnzf__acqgh = 'def agg_combine({}):\n'.format(', '.join(alvuu__mytz +
        ljwu__ppl))
    gkr__bawu = wrap_parfor_blocks(parfor)
    svcj__rsk = find_topo_order(gkr__bawu)
    svcj__rsk = svcj__rsk[1:]
    unwrap_parfor_blocks(parfor)
    elru__oswjd = {}
    gppe__abffh = []
    for nmn__jpkqp in svcj__rsk:
        hvxyo__mph = parfor.loop_body[nmn__jpkqp]
        for vqhy__zgatg in hvxyo__mph.body:
            if is_assign(vqhy__zgatg) and vqhy__zgatg.target.name in redvars:
                biohx__ogc = vqhy__zgatg.target.name
                ind = redvars.index(biohx__ogc)
                if ind in gppe__abffh:
                    continue
                if len(f_ir._definitions[biohx__ogc]) == 2:
                    var_def = f_ir._definitions[biohx__ogc][0]
                    ngnzf__acqgh += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[biohx__ogc][1]
                    ngnzf__acqgh += _match_reduce_def(var_def, f_ir, ind)
    ngnzf__acqgh += '    return {}'.format(', '.join(['v{}'.format(
        ghw__jfcd) for ghw__jfcd in range(olrrw__ywza)]))
    wwq__thbyo = {}
    exec(ngnzf__acqgh, {}, wwq__thbyo)
    shqht__qotyc = wwq__thbyo['agg_combine']
    arg_typs = tuple(2 * var_types)
    mcsvs__feg = {'numba': numba, 'bodo': bodo, 'np': np}
    mcsvs__feg.update(elru__oswjd)
    f_ir = compile_to_numba_ir(shqht__qotyc, mcsvs__feg, typingctx=
        typingctx, targetctx=targetctx, arg_typs=arg_typs, typemap=pm.
        typemap, calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    ppr__ytdje = pm.typemap[block.body[-1].value.name]
    ion__mtifk = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        ppr__ytdje, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    glf__gknic = numba.core.target_extension.dispatcher_registry[cpu_target](
        shqht__qotyc)
    glf__gknic.add_overload(ion__mtifk)
    return glf__gknic


def _match_reduce_def(var_def, f_ir, ind):
    ngnzf__acqgh = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        ngnzf__acqgh = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        cgyr__qcvag = guard(find_callname, f_ir, var_def)
        if cgyr__qcvag == ('min', 'builtins'):
            ngnzf__acqgh = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if cgyr__qcvag == ('max', 'builtins'):
            ngnzf__acqgh = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return ngnzf__acqgh


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    olrrw__ywza = len(redvars)
    nxkq__fbt = 1
    in_vars = []
    for ghw__jfcd in range(nxkq__fbt):
        gvztj__qxd = ir.Var(arr_var.scope, f'$input{ghw__jfcd}', arr_var.loc)
        in_vars.append(gvztj__qxd)
    pdrlb__rvmaw = parfor.loop_nests[0].index_variable
    agsww__mndga = [0] * olrrw__ywza
    for hvxyo__mph in parfor.loop_body.values():
        jfp__irz = []
        for vqhy__zgatg in hvxyo__mph.body:
            if is_var_assign(vqhy__zgatg
                ) and vqhy__zgatg.value.name == pdrlb__rvmaw.name:
                continue
            if is_getitem(vqhy__zgatg
                ) and vqhy__zgatg.value.value.name == arr_var.name:
                vqhy__zgatg.value = in_vars[0]
            if is_call_assign(vqhy__zgatg) and guard(find_callname, pm.
                func_ir, vqhy__zgatg.value) == ('isna',
                'bodo.libs.array_kernels') and vqhy__zgatg.value.args[0
                ].name == arr_var.name:
                vqhy__zgatg.value = ir.Const(False, vqhy__zgatg.target.loc)
            if is_assign(vqhy__zgatg) and vqhy__zgatg.target.name in redvars:
                ind = redvars.index(vqhy__zgatg.target.name)
                agsww__mndga[ind] = vqhy__zgatg.target
            jfp__irz.append(vqhy__zgatg)
        hvxyo__mph.body = jfp__irz
    alvuu__mytz = ['v{}'.format(ghw__jfcd) for ghw__jfcd in range(olrrw__ywza)]
    ljwu__ppl = ['in{}'.format(ghw__jfcd) for ghw__jfcd in range(nxkq__fbt)]
    ngnzf__acqgh = 'def agg_update({}):\n'.format(', '.join(alvuu__mytz +
        ljwu__ppl))
    ngnzf__acqgh += '    __update_redvars()\n'
    ngnzf__acqgh += '    return {}'.format(', '.join(['v{}'.format(
        ghw__jfcd) for ghw__jfcd in range(olrrw__ywza)]))
    wwq__thbyo = {}
    exec(ngnzf__acqgh, {}, wwq__thbyo)
    tpsyu__lmf = wwq__thbyo['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * nxkq__fbt)
    f_ir = compile_to_numba_ir(tpsyu__lmf, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    upm__pfcog = f_ir.blocks.popitem()[1].body
    ppr__ytdje = pm.typemap[upm__pfcog[-1].value.name]
    gkr__bawu = wrap_parfor_blocks(parfor)
    svcj__rsk = find_topo_order(gkr__bawu)
    svcj__rsk = svcj__rsk[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    hze__gvi = f_ir.blocks[svcj__rsk[0]]
    qbq__pjsrg = f_ir.blocks[svcj__rsk[-1]]
    vyk__xtaht = upm__pfcog[:olrrw__ywza + nxkq__fbt]
    if olrrw__ywza > 1:
        mcvjn__snv = upm__pfcog[-3:]
        assert is_assign(mcvjn__snv[0]) and isinstance(mcvjn__snv[0].value,
            ir.Expr) and mcvjn__snv[0].value.op == 'build_tuple'
    else:
        mcvjn__snv = upm__pfcog[-2:]
    for ghw__jfcd in range(olrrw__ywza):
        zsr__qvyg = upm__pfcog[ghw__jfcd].target
        wdhpt__jcq = ir.Assign(zsr__qvyg, agsww__mndga[ghw__jfcd],
            zsr__qvyg.loc)
        vyk__xtaht.append(wdhpt__jcq)
    for ghw__jfcd in range(olrrw__ywza, olrrw__ywza + nxkq__fbt):
        zsr__qvyg = upm__pfcog[ghw__jfcd].target
        wdhpt__jcq = ir.Assign(zsr__qvyg, in_vars[ghw__jfcd - olrrw__ywza],
            zsr__qvyg.loc)
        vyk__xtaht.append(wdhpt__jcq)
    hze__gvi.body = vyk__xtaht + hze__gvi.body
    dtnpp__qen = []
    for ghw__jfcd in range(olrrw__ywza):
        zsr__qvyg = upm__pfcog[ghw__jfcd].target
        wdhpt__jcq = ir.Assign(agsww__mndga[ghw__jfcd], zsr__qvyg,
            zsr__qvyg.loc)
        dtnpp__qen.append(wdhpt__jcq)
    qbq__pjsrg.body += dtnpp__qen + mcvjn__snv
    ltg__tbr = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        ppr__ytdje, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    glf__gknic = numba.core.target_extension.dispatcher_registry[cpu_target](
        tpsyu__lmf)
    glf__gknic.add_overload(ltg__tbr)
    return glf__gknic


def _rm_arg_agg_block(block, typemap):
    dsmy__cnqw = []
    arr_var = None
    for ghw__jfcd, vqhy__zgatg in enumerate(block.body):
        if is_assign(vqhy__zgatg) and isinstance(vqhy__zgatg.value, ir.Arg):
            arr_var = vqhy__zgatg.target
            euodm__jpugy = typemap[arr_var.name]
            if not isinstance(euodm__jpugy, types.ArrayCompatible):
                dsmy__cnqw += block.body[ghw__jfcd + 1:]
                break
            tlvs__brjzt = block.body[ghw__jfcd + 1]
            assert is_assign(tlvs__brjzt) and isinstance(tlvs__brjzt.value,
                ir.Expr
                ) and tlvs__brjzt.value.op == 'getattr' and tlvs__brjzt.value.attr == 'shape' and tlvs__brjzt.value.value.name == arr_var.name
            awa__gepiq = tlvs__brjzt.target
            mlb__gcz = block.body[ghw__jfcd + 2]
            assert is_assign(mlb__gcz) and isinstance(mlb__gcz.value, ir.Expr
                ) and mlb__gcz.value.op == 'static_getitem' and mlb__gcz.value.value.name == awa__gepiq.name
            dsmy__cnqw += block.body[ghw__jfcd + 3:]
            break
        dsmy__cnqw.append(vqhy__zgatg)
    return dsmy__cnqw, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    gkr__bawu = wrap_parfor_blocks(parfor)
    svcj__rsk = find_topo_order(gkr__bawu)
    svcj__rsk = svcj__rsk[1:]
    unwrap_parfor_blocks(parfor)
    for nmn__jpkqp in reversed(svcj__rsk):
        for vqhy__zgatg in reversed(parfor.loop_body[nmn__jpkqp].body):
            if isinstance(vqhy__zgatg, ir.Assign) and (vqhy__zgatg.target.
                name in parfor_params or vqhy__zgatg.target.name in
                var_to_param):
                bhw__tapwf = vqhy__zgatg.target.name
                rhs = vqhy__zgatg.value
                kgyu__qdd = (bhw__tapwf if bhw__tapwf in parfor_params else
                    var_to_param[bhw__tapwf])
                ffpm__rmgo = []
                if isinstance(rhs, ir.Var):
                    ffpm__rmgo = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    ffpm__rmgo = [nrzwi__dyb.name for nrzwi__dyb in
                        vqhy__zgatg.value.list_vars()]
                param_uses[kgyu__qdd].extend(ffpm__rmgo)
                for nrzwi__dyb in ffpm__rmgo:
                    var_to_param[nrzwi__dyb] = kgyu__qdd
            if isinstance(vqhy__zgatg, Parfor):
                get_parfor_reductions(vqhy__zgatg, parfor_params, calltypes,
                    reduce_varnames, param_uses, var_to_param)
    for lmdbr__ezohf, ffpm__rmgo in param_uses.items():
        if lmdbr__ezohf in ffpm__rmgo and lmdbr__ezohf not in reduce_varnames:
            reduce_varnames.append(lmdbr__ezohf)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
