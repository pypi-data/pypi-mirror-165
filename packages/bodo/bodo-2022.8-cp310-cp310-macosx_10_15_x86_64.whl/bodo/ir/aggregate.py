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
        jnnb__mejtk = func.signature
        if jnnb__mejtk == types.none(types.voidptr):
            gof__wevvh = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer()])
            dtcep__hmt = cgutils.get_or_insert_function(builder.module,
                gof__wevvh, sym._literal_value)
            builder.call(dtcep__hmt, [context.get_constant_null(jnnb__mejtk
                .args[0])])
        elif jnnb__mejtk == types.none(types.int64, types.voidptr, types.
            voidptr):
            gof__wevvh = lir.FunctionType(lir.VoidType(), [lir.IntType(64),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            dtcep__hmt = cgutils.get_or_insert_function(builder.module,
                gof__wevvh, sym._literal_value)
            builder.call(dtcep__hmt, [context.get_constant(types.int64, 0),
                context.get_constant_null(jnnb__mejtk.args[1]), context.
                get_constant_null(jnnb__mejtk.args[2])])
        else:
            gof__wevvh = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64).
                as_pointer()])
            dtcep__hmt = cgutils.get_or_insert_function(builder.module,
                gof__wevvh, sym._literal_value)
            builder.call(dtcep__hmt, [context.get_constant_null(jnnb__mejtk
                .args[0]), context.get_constant_null(jnnb__mejtk.args[1]),
                context.get_constant_null(jnnb__mejtk.args[2])])
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
        cef__gtw = True
        stpf__swcs = 1
        qymk__bbm = -1
        if isinstance(rhs, ir.Expr):
            for vlk__lci in rhs.kws:
                if func_name in list_cumulative:
                    if vlk__lci[0] == 'skipna':
                        cef__gtw = guard(find_const, func_ir, vlk__lci[1])
                        if not isinstance(cef__gtw, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if vlk__lci[0] == 'dropna':
                        cef__gtw = guard(find_const, func_ir, vlk__lci[1])
                        if not isinstance(cef__gtw, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            stpf__swcs = get_call_expr_arg('shift', rhs.args, dict(rhs.kws),
                0, 'periods', stpf__swcs)
            stpf__swcs = guard(find_const, func_ir, stpf__swcs)
        if func_name == 'head':
            qymk__bbm = get_call_expr_arg('head', rhs.args, dict(rhs.kws), 
                0, 'n', 5)
            if not isinstance(qymk__bbm, int):
                qymk__bbm = guard(find_const, func_ir, qymk__bbm)
            if qymk__bbm < 0:
                raise BodoError(
                    f'groupby.{func_name} does not work with negative values.')
        func.skipdropna = cef__gtw
        func.periods = stpf__swcs
        func.head_n = qymk__bbm
        if func_name == 'transform':
            kws = dict(rhs.kws)
            fahu__hcta = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            gnbe__nuu = typemap[fahu__hcta.name]
            miqai__qoeez = None
            if isinstance(gnbe__nuu, str):
                miqai__qoeez = gnbe__nuu
            elif is_overload_constant_str(gnbe__nuu):
                miqai__qoeez = get_overload_const_str(gnbe__nuu)
            elif bodo.utils.typing.is_builtin_function(gnbe__nuu):
                miqai__qoeez = bodo.utils.typing.get_builtin_function_name(
                    gnbe__nuu)
            if miqai__qoeez not in bodo.ir.aggregate.supported_transform_funcs[
                :]:
                raise BodoError(
                    f'unsupported transform function {miqai__qoeez}')
            func.transform_func = supported_agg_funcs.index(miqai__qoeez)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    fahu__hcta = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if fahu__hcta == '':
        gnbe__nuu = types.none
    else:
        gnbe__nuu = typemap[fahu__hcta.name]
    if is_overload_constant_dict(gnbe__nuu):
        chr__ngvh = get_overload_constant_dict(gnbe__nuu)
        usts__cjed = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in chr__ngvh.values()]
        return usts__cjed
    if gnbe__nuu == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(gnbe__nuu, types.BaseTuple) or is_overload_constant_list(
        gnbe__nuu):
        usts__cjed = []
        idimu__agnd = 0
        if is_overload_constant_list(gnbe__nuu):
            uswrq__vsyi = get_overload_const_list(gnbe__nuu)
        else:
            uswrq__vsyi = gnbe__nuu.types
        for t in uswrq__vsyi:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                usts__cjed.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>' and len(uswrq__vsyi) > 1:
                    func.fname = '<lambda_' + str(idimu__agnd) + '>'
                    idimu__agnd += 1
                usts__cjed.append(func)
        return [usts__cjed]
    if is_overload_constant_str(gnbe__nuu):
        func_name = get_overload_const_str(gnbe__nuu)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(gnbe__nuu):
        func_name = bodo.utils.typing.get_builtin_function_name(gnbe__nuu)
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
        idimu__agnd = 0
        tdn__dxhu = []
        for omu__dswx in f_val:
            func = get_agg_func_udf(func_ir, omu__dswx, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{idimu__agnd}>'
                idimu__agnd += 1
            tdn__dxhu.append(func)
        return tdn__dxhu
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
    miqai__qoeez = code.co_name
    return miqai__qoeez


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
            lhcxs__ygwnv = types.DType(args[0])
            return signature(lhcxs__ygwnv, *args)


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
        return [kymr__anoi for kymr__anoi in self.in_vars if kymr__anoi is not
            None]

    def get_live_out_vars(self):
        return [kymr__anoi for kymr__anoi in self.out_vars if kymr__anoi is not
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
        qes__dqnd = [self.out_type.data] if isinstance(self.out_type,
            SeriesType) else list(self.out_type.table_type.arr_types)
        helbu__bvow = list(get_index_data_arr_types(self.out_type.index))
        return qes__dqnd + helbu__bvow

    def update_dead_col_info(self):
        for yxln__uav in self.dead_out_inds:
            self.gb_info_out.pop(yxln__uav, None)
        if not self.input_has_index:
            self.dead_in_inds.add(self.n_in_cols - 1)
            self.dead_out_inds.add(self.n_out_cols - 1)
        for pizj__yta, nghz__izt in self.gb_info_in.copy().items():
            hfmdy__khol = []
            for omu__dswx, xhzgm__abul in nghz__izt:
                if xhzgm__abul not in self.dead_out_inds:
                    hfmdy__khol.append((omu__dswx, xhzgm__abul))
            if not hfmdy__khol:
                if pizj__yta is not None and pizj__yta not in self.in_key_inds:
                    self.dead_in_inds.add(pizj__yta)
                self.gb_info_in.pop(pizj__yta)
            else:
                self.gb_info_in[pizj__yta] = hfmdy__khol
        if self.is_in_table_format:
            if not set(range(self.n_in_table_arrays)) - self.dead_in_inds:
                self.in_vars[0] = None
            for bhcf__kzj in range(1, len(self.in_vars)):
                yxln__uav = self.n_in_table_arrays + bhcf__kzj - 1
                if yxln__uav in self.dead_in_inds:
                    self.in_vars[bhcf__kzj] = None
        else:
            for bhcf__kzj in range(len(self.in_vars)):
                if bhcf__kzj in self.dead_in_inds:
                    self.in_vars[bhcf__kzj] = None

    def __repr__(self):
        wyb__ukecw = ', '.join(kymr__anoi.name for kymr__anoi in self.
            get_live_in_vars())
        wll__dieo = f'{self.df_in}{{{wyb__ukecw}}}'
        xcsvv__kij = ', '.join(kymr__anoi.name for kymr__anoi in self.
            get_live_out_vars())
        tmnui__ysl = f'{self.df_out}{{{xcsvv__kij}}}'
        return (
            f'Groupby (keys: {self.key_names} {self.in_key_inds}): {wll__dieo} {tmnui__ysl}'
            )


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({kymr__anoi.name for kymr__anoi in aggregate_node.
        get_live_in_vars()})
    def_set.update({kymr__anoi.name for kymr__anoi in aggregate_node.
        get_live_out_vars()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(agg_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    vlg__yjq = agg_node.out_vars[0]
    if vlg__yjq is not None and vlg__yjq.name not in lives:
        agg_node.out_vars[0] = None
        if agg_node.is_output_table:
            hndqm__tpd = set(range(agg_node.n_out_table_arrays))
            agg_node.dead_out_inds.update(hndqm__tpd)
        else:
            agg_node.dead_out_inds.add(0)
    for bhcf__kzj in range(1, len(agg_node.out_vars)):
        kymr__anoi = agg_node.out_vars[bhcf__kzj]
        if kymr__anoi is not None and kymr__anoi.name not in lives:
            agg_node.out_vars[bhcf__kzj] = None
            yxln__uav = agg_node.n_out_table_arrays + bhcf__kzj - 1
            agg_node.dead_out_inds.add(yxln__uav)
    if all(kymr__anoi is None for kymr__anoi in agg_node.out_vars):
        return None
    agg_node.update_dead_col_info()
    return agg_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    gmbm__klff = {kymr__anoi.name for kymr__anoi in aggregate_node.
        get_live_out_vars()}
    return set(), gmbm__klff


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for bhcf__kzj in range(len(aggregate_node.in_vars)):
        if aggregate_node.in_vars[bhcf__kzj] is not None:
            aggregate_node.in_vars[bhcf__kzj] = replace_vars_inner(
                aggregate_node.in_vars[bhcf__kzj], var_dict)
    for bhcf__kzj in range(len(aggregate_node.out_vars)):
        if aggregate_node.out_vars[bhcf__kzj] is not None:
            aggregate_node.out_vars[bhcf__kzj] = replace_vars_inner(
                aggregate_node.out_vars[bhcf__kzj], var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    for bhcf__kzj in range(len(aggregate_node.in_vars)):
        if aggregate_node.in_vars[bhcf__kzj] is not None:
            aggregate_node.in_vars[bhcf__kzj] = visit_vars_inner(aggregate_node
                .in_vars[bhcf__kzj], callback, cbdata)
    for bhcf__kzj in range(len(aggregate_node.out_vars)):
        if aggregate_node.out_vars[bhcf__kzj] is not None:
            aggregate_node.out_vars[bhcf__kzj] = visit_vars_inner(
                aggregate_node.out_vars[bhcf__kzj], callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    khn__uechj = []
    for fkdz__fjgi in aggregate_node.get_live_in_vars():
        ctnhm__jqqta = equiv_set.get_shape(fkdz__fjgi)
        if ctnhm__jqqta is not None:
            khn__uechj.append(ctnhm__jqqta[0])
    if len(khn__uechj) > 1:
        equiv_set.insert_equiv(*khn__uechj)
    hde__bzix = []
    khn__uechj = []
    for fkdz__fjgi in aggregate_node.get_live_out_vars():
        rpa__krdq = typemap[fkdz__fjgi.name]
        tpcmz__qtit = array_analysis._gen_shape_call(equiv_set, fkdz__fjgi,
            rpa__krdq.ndim, None, hde__bzix)
        equiv_set.insert_equiv(fkdz__fjgi, tpcmz__qtit)
        khn__uechj.append(tpcmz__qtit[0])
        equiv_set.define(fkdz__fjgi, set())
    if len(khn__uechj) > 1:
        equiv_set.insert_equiv(*khn__uechj)
    return [], hde__bzix


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    mvov__jraiz = aggregate_node.get_live_in_vars()
    pra__jep = aggregate_node.get_live_out_vars()
    efis__urt = Distribution.OneD
    for fkdz__fjgi in mvov__jraiz:
        efis__urt = Distribution(min(efis__urt.value, array_dists[
            fkdz__fjgi.name].value))
    ztgb__acoa = Distribution(min(efis__urt.value, Distribution.OneD_Var.value)
        )
    for fkdz__fjgi in pra__jep:
        if fkdz__fjgi.name in array_dists:
            ztgb__acoa = Distribution(min(ztgb__acoa.value, array_dists[
                fkdz__fjgi.name].value))
    if ztgb__acoa != Distribution.OneD_Var:
        efis__urt = ztgb__acoa
    for fkdz__fjgi in mvov__jraiz:
        array_dists[fkdz__fjgi.name] = efis__urt
    for fkdz__fjgi in pra__jep:
        array_dists[fkdz__fjgi.name] = ztgb__acoa


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for fkdz__fjgi in agg_node.get_live_out_vars():
        definitions[fkdz__fjgi.name].append(agg_node)
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
    isyas__wyx = agg_node.get_live_in_vars()
    hdun__xytr = agg_node.get_live_out_vars()
    if array_dists is not None:
        parallel = True
        for kymr__anoi in (isyas__wyx + hdun__xytr):
            if array_dists[kymr__anoi.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                kymr__anoi.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    out_col_typs = agg_node.out_col_types
    in_col_typs = []
    usts__cjed = []
    func_out_types = []
    for xhzgm__abul, (pizj__yta, func) in agg_node.gb_info_out.items():
        if pizj__yta is not None:
            t = agg_node.in_col_types[pizj__yta]
            in_col_typs.append(t)
        usts__cjed.append(func)
        func_out_types.append(out_col_typs[xhzgm__abul])
    mxxr__swc = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for bhcf__kzj, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            mxxr__swc.update({f'in_cat_dtype_{bhcf__kzj}': in_col_typ})
    for bhcf__kzj, pcmzr__effwo in enumerate(out_col_typs):
        if isinstance(pcmzr__effwo, bodo.CategoricalArrayType):
            mxxr__swc.update({f'out_cat_dtype_{bhcf__kzj}': pcmzr__effwo})
    udf_func_struct = get_udf_func_struct(usts__cjed, in_col_typs,
        typingctx, targetctx)
    out_var_types = [(typemap[kymr__anoi.name] if kymr__anoi is not None else
        types.none) for kymr__anoi in agg_node.out_vars]
    alp__iwurj, klb__lzg = gen_top_level_agg_func(agg_node, in_col_typs,
        out_col_typs, func_out_types, parallel, udf_func_struct,
        out_var_types, typemap)
    mxxr__swc.update(klb__lzg)
    mxxr__swc.update({'pd': pd, 'pre_alloc_string_array':
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
            mxxr__swc.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            mxxr__swc.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    kubd__njl = {}
    exec(alp__iwurj, {}, kubd__njl)
    uta__jwea = kubd__njl['agg_top']
    hib__cobw = compile_to_numba_ir(uta__jwea, mxxr__swc, typingctx=
        typingctx, targetctx=targetctx, arg_typs=tuple(typemap[kymr__anoi.
        name] for kymr__anoi in isyas__wyx), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(hib__cobw, isyas__wyx)
    wggif__udz = hib__cobw.body[-2].value.value
    cquc__wlyfq = hib__cobw.body[:-2]
    for bhcf__kzj, kymr__anoi in enumerate(hdun__xytr):
        gen_getitem(kymr__anoi, wggif__udz, bhcf__kzj, calltypes, cquc__wlyfq)
    return cquc__wlyfq


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        nyhiv__gwfwx = IntDtype(t.dtype).name
        assert nyhiv__gwfwx.endswith('Dtype()')
        nyhiv__gwfwx = nyhiv__gwfwx[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{nyhiv__gwfwx}'))"
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
        uxxpy__dipi = 'in' if is_input else 'out'
        return (
            f'bodo.utils.utils.alloc_type(1, {uxxpy__dipi}_cat_dtype_{colnum})'
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
    dptj__epvy = udf_func_struct.var_typs
    aefvm__kvft = len(dptj__epvy)
    alp__iwurj = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    alp__iwurj += '    if is_null_pointer(in_table):\n'
    alp__iwurj += '        return\n'
    alp__iwurj += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in dptj__epvy]), 
        ',' if len(dptj__epvy) == 1 else '')
    azn__mqj = n_keys
    xzier__gwn = []
    redvar_offsets = []
    ibl__ote = []
    if do_combine:
        for bhcf__kzj, omu__dswx in enumerate(allfuncs):
            if omu__dswx.ftype != 'udf':
                azn__mqj += omu__dswx.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(azn__mqj, azn__mqj + omu__dswx
                    .n_redvars))
                azn__mqj += omu__dswx.n_redvars
                ibl__ote.append(data_in_typs_[func_idx_to_in_col[bhcf__kzj]])
                xzier__gwn.append(func_idx_to_in_col[bhcf__kzj] + n_keys)
    else:
        for bhcf__kzj, omu__dswx in enumerate(allfuncs):
            if omu__dswx.ftype != 'udf':
                azn__mqj += omu__dswx.ncols_post_shuffle
            else:
                redvar_offsets += list(range(azn__mqj + 1, azn__mqj + 1 +
                    omu__dswx.n_redvars))
                azn__mqj += omu__dswx.n_redvars + 1
                ibl__ote.append(data_in_typs_[func_idx_to_in_col[bhcf__kzj]])
                xzier__gwn.append(func_idx_to_in_col[bhcf__kzj] + n_keys)
    assert len(redvar_offsets) == aefvm__kvft
    cexv__gjyb = len(ibl__ote)
    ppqx__vdleb = []
    for bhcf__kzj, t in enumerate(ibl__ote):
        ppqx__vdleb.append(_gen_dummy_alloc(t, bhcf__kzj, True))
    alp__iwurj += '    data_in_dummy = ({}{})\n'.format(','.join(
        ppqx__vdleb), ',' if len(ibl__ote) == 1 else '')
    alp__iwurj += """
    # initialize redvar cols
"""
    alp__iwurj += '    init_vals = __init_func()\n'
    for bhcf__kzj in range(aefvm__kvft):
        alp__iwurj += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(bhcf__kzj, redvar_offsets[bhcf__kzj], bhcf__kzj))
        alp__iwurj += '    incref(redvar_arr_{})\n'.format(bhcf__kzj)
        alp__iwurj += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            bhcf__kzj, bhcf__kzj)
    alp__iwurj += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(bhcf__kzj) for bhcf__kzj in range(aefvm__kvft)]), ',' if 
        aefvm__kvft == 1 else '')
    alp__iwurj += '\n'
    for bhcf__kzj in range(cexv__gjyb):
        alp__iwurj += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(bhcf__kzj, xzier__gwn[bhcf__kzj], bhcf__kzj))
        alp__iwurj += '    incref(data_in_{})\n'.format(bhcf__kzj)
    alp__iwurj += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(bhcf__kzj) for bhcf__kzj in range(cexv__gjyb)]), ',' if 
        cexv__gjyb == 1 else '')
    alp__iwurj += '\n'
    alp__iwurj += '    for i in range(len(data_in_0)):\n'
    alp__iwurj += '        w_ind = row_to_group[i]\n'
    alp__iwurj += '        if w_ind != -1:\n'
    alp__iwurj += '            __update_redvars(redvars, data_in, w_ind, i)\n'
    kubd__njl = {}
    exec(alp__iwurj, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, kubd__njl)
    return kubd__njl['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, label_suffix):
    dptj__epvy = udf_func_struct.var_typs
    aefvm__kvft = len(dptj__epvy)
    alp__iwurj = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    alp__iwurj += '    if is_null_pointer(in_table):\n'
    alp__iwurj += '        return\n'
    alp__iwurj += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in dptj__epvy]), 
        ',' if len(dptj__epvy) == 1 else '')
    ucz__jify = n_keys
    izh__bsuy = n_keys
    acjm__orlx = []
    kezma__wahv = []
    for omu__dswx in allfuncs:
        if omu__dswx.ftype != 'udf':
            ucz__jify += omu__dswx.ncols_pre_shuffle
            izh__bsuy += omu__dswx.ncols_post_shuffle
        else:
            acjm__orlx += list(range(ucz__jify, ucz__jify + omu__dswx.
                n_redvars))
            kezma__wahv += list(range(izh__bsuy + 1, izh__bsuy + 1 +
                omu__dswx.n_redvars))
            ucz__jify += omu__dswx.n_redvars
            izh__bsuy += 1 + omu__dswx.n_redvars
    assert len(acjm__orlx) == aefvm__kvft
    alp__iwurj += """
    # initialize redvar cols
"""
    alp__iwurj += '    init_vals = __init_func()\n'
    for bhcf__kzj in range(aefvm__kvft):
        alp__iwurj += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(bhcf__kzj, kezma__wahv[bhcf__kzj], bhcf__kzj))
        alp__iwurj += '    incref(redvar_arr_{})\n'.format(bhcf__kzj)
        alp__iwurj += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            bhcf__kzj, bhcf__kzj)
    alp__iwurj += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(bhcf__kzj) for bhcf__kzj in range(aefvm__kvft)]), ',' if 
        aefvm__kvft == 1 else '')
    alp__iwurj += '\n'
    for bhcf__kzj in range(aefvm__kvft):
        alp__iwurj += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(bhcf__kzj, acjm__orlx[bhcf__kzj], bhcf__kzj))
        alp__iwurj += '    incref(recv_redvar_arr_{})\n'.format(bhcf__kzj)
    alp__iwurj += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(bhcf__kzj) for bhcf__kzj in range(
        aefvm__kvft)]), ',' if aefvm__kvft == 1 else '')
    alp__iwurj += '\n'
    if aefvm__kvft:
        alp__iwurj += '    for i in range(len(recv_redvar_arr_0)):\n'
        alp__iwurj += '        w_ind = row_to_group[i]\n'
        alp__iwurj += (
            '        __combine_redvars(redvars, recv_redvars, w_ind, i)\n')
    kubd__njl = {}
    exec(alp__iwurj, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, kubd__njl)
    return kubd__njl['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    dptj__epvy = udf_func_struct.var_typs
    aefvm__kvft = len(dptj__epvy)
    azn__mqj = n_keys
    redvar_offsets = []
    nhg__xslv = []
    sop__gle = []
    for bhcf__kzj, omu__dswx in enumerate(allfuncs):
        if omu__dswx.ftype != 'udf':
            azn__mqj += omu__dswx.ncols_post_shuffle
        else:
            nhg__xslv.append(azn__mqj)
            redvar_offsets += list(range(azn__mqj + 1, azn__mqj + 1 +
                omu__dswx.n_redvars))
            azn__mqj += 1 + omu__dswx.n_redvars
            sop__gle.append(out_data_typs_[bhcf__kzj])
    assert len(redvar_offsets) == aefvm__kvft
    cexv__gjyb = len(sop__gle)
    alp__iwurj = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    alp__iwurj += '    if is_null_pointer(table):\n'
    alp__iwurj += '        return\n'
    alp__iwurj += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in dptj__epvy]), 
        ',' if len(dptj__epvy) == 1 else '')
    alp__iwurj += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in sop__gle]
        ), ',' if len(sop__gle) == 1 else '')
    for bhcf__kzj in range(aefvm__kvft):
        alp__iwurj += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(bhcf__kzj, redvar_offsets[bhcf__kzj], bhcf__kzj))
        alp__iwurj += '    incref(redvar_arr_{})\n'.format(bhcf__kzj)
    alp__iwurj += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(bhcf__kzj) for bhcf__kzj in range(aefvm__kvft)]), ',' if 
        aefvm__kvft == 1 else '')
    alp__iwurj += '\n'
    for bhcf__kzj in range(cexv__gjyb):
        alp__iwurj += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(bhcf__kzj, nhg__xslv[bhcf__kzj], bhcf__kzj))
        alp__iwurj += '    incref(data_out_{})\n'.format(bhcf__kzj)
    alp__iwurj += '    data_out = ({}{})\n'.format(','.join(['data_out_{}'.
        format(bhcf__kzj) for bhcf__kzj in range(cexv__gjyb)]), ',' if 
        cexv__gjyb == 1 else '')
    alp__iwurj += '\n'
    alp__iwurj += '    for i in range(len(data_out_0)):\n'
    alp__iwurj += '        __eval_res(redvars, data_out, i)\n'
    kubd__njl = {}
    exec(alp__iwurj, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, kubd__njl)
    return kubd__njl['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    azn__mqj = n_keys
    arwf__zar = []
    for bhcf__kzj, omu__dswx in enumerate(allfuncs):
        if omu__dswx.ftype == 'gen_udf':
            arwf__zar.append(azn__mqj)
            azn__mqj += 1
        elif omu__dswx.ftype != 'udf':
            azn__mqj += omu__dswx.ncols_post_shuffle
        else:
            azn__mqj += omu__dswx.n_redvars + 1
    alp__iwurj = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    alp__iwurj += '    if num_groups == 0:\n'
    alp__iwurj += '        return\n'
    for bhcf__kzj, func in enumerate(udf_func_struct.general_udf_funcs):
        alp__iwurj += '    # col {}\n'.format(bhcf__kzj)
        alp__iwurj += (
            """    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)
"""
            .format(arwf__zar[bhcf__kzj], bhcf__kzj))
        alp__iwurj += '    incref(out_col)\n'
        alp__iwurj += '    for j in range(num_groups):\n'
        alp__iwurj += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(bhcf__kzj, bhcf__kzj))
        alp__iwurj += '        incref(in_col)\n'
        alp__iwurj += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(bhcf__kzj))
    mxxr__swc = {'pd': pd, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref}
    fxprh__vsctc = 0
    for bhcf__kzj, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[fxprh__vsctc]
        mxxr__swc['func_{}'.format(fxprh__vsctc)] = func
        mxxr__swc['in_col_{}_typ'.format(fxprh__vsctc)] = in_col_typs[
            func_idx_to_in_col[bhcf__kzj]]
        mxxr__swc['out_col_{}_typ'.format(fxprh__vsctc)] = out_col_typs[
            bhcf__kzj]
        fxprh__vsctc += 1
    kubd__njl = {}
    exec(alp__iwurj, mxxr__swc, kubd__njl)
    omu__dswx = kubd__njl['bodo_gb_apply_general_udfs{}'.format(label_suffix)]
    diqsb__ulmi = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(diqsb__ulmi, nopython=True)(omu__dswx)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs,
    func_out_types, parallel, udf_func_struct, out_var_types, typemap):
    n_keys = len(agg_node.in_key_inds)
    giqn__muirg = len(agg_node.out_vars)
    if agg_node.same_index:
        assert agg_node.input_has_index, 'agg codegen: input_has_index=True required for same_index=True'
    if agg_node.is_in_table_format:
        vyd__cpkl = []
        if agg_node.in_vars[0] is not None:
            vyd__cpkl.append('arg0')
        for bhcf__kzj in range(agg_node.n_in_table_arrays, agg_node.n_in_cols):
            if bhcf__kzj not in agg_node.dead_in_inds:
                vyd__cpkl.append(f'arg{bhcf__kzj}')
    else:
        vyd__cpkl = [f'arg{bhcf__kzj}' for bhcf__kzj, kymr__anoi in
            enumerate(agg_node.in_vars) if kymr__anoi is not None]
    alp__iwurj = f"def agg_top({', '.join(vyd__cpkl)}):\n"
    hytep__mdh = []
    if agg_node.is_in_table_format:
        hytep__mdh = agg_node.in_key_inds + [pizj__yta for pizj__yta,
            awyh__drctf in agg_node.gb_info_out.values() if pizj__yta is not
            None]
        if agg_node.input_has_index:
            hytep__mdh.append(agg_node.n_in_cols - 1)
        vdls__vwo = ',' if len(agg_node.in_vars) - 1 == 1 else ''
        fxhl__tmgh = []
        for bhcf__kzj in range(agg_node.n_in_table_arrays, agg_node.n_in_cols):
            if bhcf__kzj in agg_node.dead_in_inds:
                fxhl__tmgh.append('None')
            else:
                fxhl__tmgh.append(f'arg{bhcf__kzj}')
        wtnu__ucgnw = 'arg0' if agg_node.in_vars[0] is not None else 'None'
        alp__iwurj += f"""    table = py_data_to_cpp_table({wtnu__ucgnw}, ({', '.join(fxhl__tmgh)}{vdls__vwo}), in_col_inds, {agg_node.n_in_table_arrays})
"""
    else:
        ynlms__wshez = [f'arg{bhcf__kzj}' for bhcf__kzj in agg_node.in_key_inds
            ]
        jjvkt__egnfp = [f'arg{pizj__yta}' for pizj__yta, awyh__drctf in
            agg_node.gb_info_out.values() if pizj__yta is not None]
        fbn__febp = ynlms__wshez + jjvkt__egnfp
        if agg_node.input_has_index:
            fbn__febp.append(f'arg{len(agg_node.in_vars) - 1}')
        alp__iwurj += '    info_list = [{}]\n'.format(', '.join(
            f'array_to_info({tcy__sslh})' for tcy__sslh in fbn__febp))
        alp__iwurj += '    table = arr_info_list_to_table(info_list)\n'
    do_combine = parallel
    allfuncs = []
    brffb__brnt = []
    func_idx_to_in_col = []
    vgw__pipt = []
    cef__gtw = False
    dsifc__qlk = 1
    qymk__bbm = -1
    rhany__gselu = 0
    ndppb__wpp = 0
    usts__cjed = [func for awyh__drctf, func in agg_node.gb_info_out.values()]
    for pdqza__idw, func in enumerate(usts__cjed):
        brffb__brnt.append(len(allfuncs))
        if func.ftype in {'median', 'nunique', 'ngroup'}:
            do_combine = False
        if func.ftype in list_cumulative:
            rhany__gselu += 1
        if hasattr(func, 'skipdropna'):
            cef__gtw = func.skipdropna
        if func.ftype == 'shift':
            dsifc__qlk = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            ndppb__wpp = func.transform_func
            do_combine = False
        if func.ftype == 'head':
            qymk__bbm = func.head_n
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(pdqza__idw)
        if func.ftype == 'udf':
            vgw__pipt.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            vgw__pipt.append(0)
            do_combine = False
    brffb__brnt.append(len(allfuncs))
    assert len(agg_node.gb_info_out) == len(allfuncs
        ), 'invalid number of groupby outputs'
    if rhany__gselu > 0:
        if rhany__gselu != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    lxjra__pkqkp = []
    if udf_func_struct is not None:
        difkb__sqes = next_label()
        if udf_func_struct.regular_udfs:
            diqsb__ulmi = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            aak__yzwb = numba.cfunc(diqsb__ulmi, nopython=True)(gen_update_cb
                (udf_func_struct, allfuncs, n_keys, in_col_typs, do_combine,
                func_idx_to_in_col, difkb__sqes))
            trvg__vwz = numba.cfunc(diqsb__ulmi, nopython=True)(gen_combine_cb
                (udf_func_struct, allfuncs, n_keys, difkb__sqes))
            vtkat__esaqj = numba.cfunc('void(voidptr)', nopython=True)(
                gen_eval_cb(udf_func_struct, allfuncs, n_keys,
                func_out_types, difkb__sqes))
            udf_func_struct.set_regular_cfuncs(aak__yzwb, trvg__vwz,
                vtkat__esaqj)
            for injg__qvyw in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[injg__qvyw.native_name] = injg__qvyw
                gb_agg_cfunc_addr[injg__qvyw.native_name] = injg__qvyw.address
        if udf_func_struct.general_udfs:
            jhb__qau = gen_general_udf_cb(udf_func_struct, allfuncs, n_keys,
                in_col_typs, func_out_types, func_idx_to_in_col, difkb__sqes)
            udf_func_struct.set_general_cfunc(jhb__qau)
        dptj__epvy = (udf_func_struct.var_typs if udf_func_struct.
            regular_udfs else None)
        znj__wdiep = 0
        bhcf__kzj = 0
        for kmcjp__ayz, omu__dswx in zip(agg_node.gb_info_out.keys(), allfuncs
            ):
            if omu__dswx.ftype in ('udf', 'gen_udf'):
                lxjra__pkqkp.append(out_col_typs[kmcjp__ayz])
                for hwq__vjoh in range(znj__wdiep, znj__wdiep + vgw__pipt[
                    bhcf__kzj]):
                    lxjra__pkqkp.append(dtype_to_array_type(dptj__epvy[
                        hwq__vjoh]))
                znj__wdiep += vgw__pipt[bhcf__kzj]
                bhcf__kzj += 1
        alp__iwurj += f"""    dummy_table = create_dummy_table(({', '.join(f'udf_type{bhcf__kzj}' for bhcf__kzj in range(len(lxjra__pkqkp)))}{',' if len(lxjra__pkqkp) == 1 else ''}))
"""
        alp__iwurj += f"""    udf_table_dummy = py_data_to_cpp_table(dummy_table, (), udf_dummy_col_inds, {len(lxjra__pkqkp)})
"""
        if udf_func_struct.regular_udfs:
            alp__iwurj += (
                f"    add_agg_cfunc_sym(cpp_cb_update, '{aak__yzwb.native_name}')\n"
                )
            alp__iwurj += (
                f"    add_agg_cfunc_sym(cpp_cb_combine, '{trvg__vwz.native_name}')\n"
                )
            alp__iwurj += (
                f"    add_agg_cfunc_sym(cpp_cb_eval, '{vtkat__esaqj.native_name}')\n"
                )
            alp__iwurj += (
                f"    cpp_cb_update_addr = get_agg_udf_addr('{aak__yzwb.native_name}')\n"
                )
            alp__iwurj += (
                f"    cpp_cb_combine_addr = get_agg_udf_addr('{trvg__vwz.native_name}')\n"
                )
            alp__iwurj += (
                f"    cpp_cb_eval_addr = get_agg_udf_addr('{vtkat__esaqj.native_name}')\n"
                )
        else:
            alp__iwurj += '    cpp_cb_update_addr = 0\n'
            alp__iwurj += '    cpp_cb_combine_addr = 0\n'
            alp__iwurj += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            injg__qvyw = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[injg__qvyw.native_name] = injg__qvyw
            gb_agg_cfunc_addr[injg__qvyw.native_name] = injg__qvyw.address
            alp__iwurj += (
                f"    add_agg_cfunc_sym(cpp_cb_general, '{injg__qvyw.native_name}')\n"
                )
            alp__iwurj += f"""    cpp_cb_general_addr = get_agg_udf_addr('{injg__qvyw.native_name}')
"""
        else:
            alp__iwurj += '    cpp_cb_general_addr = 0\n'
    else:
        alp__iwurj += """    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])
"""
        alp__iwurj += '    cpp_cb_update_addr = 0\n'
        alp__iwurj += '    cpp_cb_combine_addr = 0\n'
        alp__iwurj += '    cpp_cb_eval_addr = 0\n'
        alp__iwurj += '    cpp_cb_general_addr = 0\n'
    alp__iwurj += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(
        ', '.join([str(supported_agg_funcs.index(omu__dswx.ftype)) for
        omu__dswx in allfuncs] + ['0']))
    alp__iwurj += (
        f'    func_offsets = np.array({str(brffb__brnt)}, dtype=np.int32)\n')
    if len(vgw__pipt) > 0:
        alp__iwurj += (
            f'    udf_ncols = np.array({str(vgw__pipt)}, dtype=np.int32)\n')
    else:
        alp__iwurj += '    udf_ncols = np.array([0], np.int32)\n'
    alp__iwurj += '    total_rows_np = np.array([0], dtype=np.int64)\n'
    ibugn__fmu = (agg_node._num_shuffle_keys if agg_node._num_shuffle_keys !=
        -1 else n_keys)
    alp__iwurj += f"""    out_table = groupby_and_aggregate(table, {n_keys}, {agg_node.input_has_index}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {parallel}, {cef__gtw}, {dsifc__qlk}, {ndppb__wpp}, {qymk__bbm}, {agg_node.return_key}, {agg_node.same_index}, {agg_node.dropna}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy, total_rows_np.ctypes, {ibugn__fmu})
"""
    quvsm__rukp = []
    erq__uchr = 0
    if agg_node.return_key:
        eehx__pvyc = 0 if isinstance(agg_node.out_type.index, bodo.
            RangeIndexType) else agg_node.n_out_cols - len(agg_node.in_key_inds
            ) - 1
        for bhcf__kzj in range(n_keys):
            yxln__uav = eehx__pvyc + bhcf__kzj
            quvsm__rukp.append(yxln__uav if yxln__uav not in agg_node.
                dead_out_inds else -1)
            erq__uchr += 1
    for kmcjp__ayz in agg_node.gb_info_out.keys():
        quvsm__rukp.append(kmcjp__ayz)
        erq__uchr += 1
    rzp__mmq = False
    if agg_node.same_index:
        if agg_node.out_vars[-1] is not None:
            quvsm__rukp.append(agg_node.n_out_cols - 1)
        else:
            rzp__mmq = True
    vdls__vwo = ',' if giqn__muirg == 1 else ''
    mvn__aury = (
        f"({', '.join(f'out_type{bhcf__kzj}' for bhcf__kzj in range(giqn__muirg))}{vdls__vwo})"
        )
    hsg__ybr = []
    djtu__nsbam = []
    for bhcf__kzj, t in enumerate(out_col_typs):
        if bhcf__kzj not in agg_node.dead_out_inds and type_has_unknown_cats(t
            ):
            if bhcf__kzj in agg_node.gb_info_out:
                pizj__yta = agg_node.gb_info_out[bhcf__kzj][0]
            else:
                assert agg_node.return_key, 'Internal error: groupby key output with unknown categoricals detected, but return_key is False'
                ttxb__mqm = bhcf__kzj - eehx__pvyc
                pizj__yta = agg_node.in_key_inds[ttxb__mqm]
            djtu__nsbam.append(bhcf__kzj)
            if (agg_node.is_in_table_format and pizj__yta < agg_node.
                n_in_table_arrays):
                hsg__ybr.append(f'get_table_data(arg0, {pizj__yta})')
            else:
                hsg__ybr.append(f'arg{pizj__yta}')
    vdls__vwo = ',' if len(hsg__ybr) == 1 else ''
    alp__iwurj += f"""    out_data = cpp_table_to_py_data(out_table, out_col_inds, {mvn__aury}, total_rows_np[0], {agg_node.n_out_table_arrays}, ({', '.join(hsg__ybr)}{vdls__vwo}), unknown_cat_out_inds)
"""
    alp__iwurj += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    alp__iwurj += '    delete_table_decref_arrays(table)\n'
    alp__iwurj += '    delete_table_decref_arrays(udf_table_dummy)\n'
    if agg_node.return_key:
        for bhcf__kzj in range(n_keys):
            if quvsm__rukp[bhcf__kzj] == -1:
                alp__iwurj += (
                    f'    decref_table_array(out_table, {bhcf__kzj})\n')
    if rzp__mmq:
        wvfg__dbxa = len(agg_node.gb_info_out) + (n_keys if agg_node.
            return_key else 0)
        alp__iwurj += f'    decref_table_array(out_table, {wvfg__dbxa})\n'
    alp__iwurj += '    delete_table(out_table)\n'
    alp__iwurj += '    ev_clean.finalize()\n'
    alp__iwurj += '    return out_data\n'
    goi__qblu = {f'out_type{bhcf__kzj}': out_var_types[bhcf__kzj] for
        bhcf__kzj in range(giqn__muirg)}
    goi__qblu['out_col_inds'] = MetaType(tuple(quvsm__rukp))
    goi__qblu['in_col_inds'] = MetaType(tuple(hytep__mdh))
    goi__qblu['cpp_table_to_py_data'] = cpp_table_to_py_data
    goi__qblu['py_data_to_cpp_table'] = py_data_to_cpp_table
    goi__qblu.update({f'udf_type{bhcf__kzj}': t for bhcf__kzj, t in
        enumerate(lxjra__pkqkp)})
    goi__qblu['udf_dummy_col_inds'] = MetaType(tuple(range(len(lxjra__pkqkp))))
    goi__qblu['create_dummy_table'] = create_dummy_table
    goi__qblu['unknown_cat_out_inds'] = MetaType(tuple(djtu__nsbam))
    goi__qblu['get_table_data'] = bodo.hiframes.table.get_table_data
    return alp__iwurj, goi__qblu


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def create_dummy_table(data_types):
    bhu__qdtpi = tuple(unwrap_typeref(data_types.types[bhcf__kzj]) for
        bhcf__kzj in range(len(data_types.types)))
    wux__kux = bodo.TableType(bhu__qdtpi)
    goi__qblu = {'table_type': wux__kux}
    alp__iwurj = 'def impl(data_types):\n'
    alp__iwurj += '  py_table = init_table(table_type, False)\n'
    alp__iwurj += '  py_table = set_table_len(py_table, 1)\n'
    for rpa__krdq, ckj__fhori in wux__kux.type_to_blk.items():
        goi__qblu[f'typ_list_{ckj__fhori}'] = types.List(rpa__krdq)
        goi__qblu[f'typ_{ckj__fhori}'] = rpa__krdq
        jzpgb__rwbm = len(wux__kux.block_to_arr_ind[ckj__fhori])
        alp__iwurj += f"""  arr_list_{ckj__fhori} = alloc_list_like(typ_list_{ckj__fhori}, {jzpgb__rwbm}, False)
"""
        alp__iwurj += f'  for i in range(len(arr_list_{ckj__fhori})):\n'
        alp__iwurj += (
            f'    arr_list_{ckj__fhori}[i] = alloc_type(1, typ_{ckj__fhori}, (-1,))\n'
            )
        alp__iwurj += f"""  py_table = set_table_block(py_table, arr_list_{ckj__fhori}, {ckj__fhori})
"""
    alp__iwurj += '  return py_table\n'
    goi__qblu.update({'init_table': bodo.hiframes.table.init_table,
        'alloc_list_like': bodo.hiframes.table.alloc_list_like,
        'set_table_block': bodo.hiframes.table.set_table_block,
        'set_table_len': bodo.hiframes.table.set_table_len, 'alloc_type':
        bodo.utils.utils.alloc_type})
    kubd__njl = {}
    exec(alp__iwurj, goi__qblu, kubd__njl)
    return kubd__njl['impl']


def agg_table_column_use(agg_node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    if not agg_node.is_in_table_format or agg_node.in_vars[0] is None:
        return
    rtd__sqx = agg_node.in_vars[0].name
    djszu__ckm, mzqi__rwmm, wxoe__uazhk = block_use_map[rtd__sqx]
    if mzqi__rwmm or wxoe__uazhk:
        return
    if agg_node.is_output_table and agg_node.out_vars[0] is not None:
        tai__ywmw, rirac__krbp, rpr__asf = _compute_table_column_uses(agg_node
            .out_vars[0].name, table_col_use_map, equiv_vars)
        if rirac__krbp or rpr__asf:
            tai__ywmw = set(range(agg_node.n_out_table_arrays))
    else:
        tai__ywmw = {}
        if agg_node.out_vars[0
            ] is not None and 0 not in agg_node.dead_out_inds:
            tai__ywmw = {0}
    fez__dhiux = set(bhcf__kzj for bhcf__kzj in agg_node.in_key_inds if 
        bhcf__kzj < agg_node.n_in_table_arrays)
    uyt__aewh = set(agg_node.gb_info_out[bhcf__kzj][0] for bhcf__kzj in
        tai__ywmw if bhcf__kzj in agg_node.gb_info_out and agg_node.
        gb_info_out[bhcf__kzj][0] is not None)
    uyt__aewh |= fez__dhiux | djszu__ckm
    eszw__eqpqd = len(set(range(agg_node.n_in_table_arrays)) - uyt__aewh) == 0
    block_use_map[rtd__sqx] = uyt__aewh, eszw__eqpqd, False


ir_extension_table_column_use[Aggregate] = agg_table_column_use


def agg_remove_dead_column(agg_node, column_live_map, equiv_vars, typemap):
    if not agg_node.is_output_table or agg_node.out_vars[0] is None:
        return False
    rqf__jvacj = agg_node.n_out_table_arrays
    aqicl__dblbv = agg_node.out_vars[0].name
    mwzkn__kakf = _find_used_columns(aqicl__dblbv, rqf__jvacj,
        column_live_map, equiv_vars)
    if mwzkn__kakf is None:
        return False
    ear__zin = set(range(rqf__jvacj)) - mwzkn__kakf
    kgj__hjpl = len(ear__zin - agg_node.dead_out_inds) != 0
    if kgj__hjpl:
        agg_node.dead_out_inds.update(ear__zin)
        agg_node.update_dead_col_info()
    return kgj__hjpl


remove_dead_column_extensions[Aggregate] = agg_remove_dead_column


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for yrjzx__ccmam in block.body:
            if is_call_assign(yrjzx__ccmam) and find_callname(f_ir,
                yrjzx__ccmam.value) == ('len', 'builtins'
                ) and yrjzx__ccmam.value.args[0].name == f_ir.arg_names[0]:
                cqd__puld = get_definition(f_ir, yrjzx__ccmam.value.func)
                cqd__puld.name = 'dummy_agg_count'
                cqd__puld.value = dummy_agg_count
    uhl__knyv = get_name_var_table(f_ir.blocks)
    jczo__hnklw = {}
    for name, awyh__drctf in uhl__knyv.items():
        jczo__hnklw[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, jczo__hnklw)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    mcta__dbyme = numba.core.compiler.Flags()
    mcta__dbyme.nrt = True
    vrqqp__pmfo = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, mcta__dbyme)
    vrqqp__pmfo.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, umlh__urj, calltypes, awyh__drctf = (numba.core.typed_passes.
        type_inference_stage(typingctx, targetctx, f_ir, arg_typs, None))
    hunxd__gsgf = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    rjpt__gqc = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    qiy__sva = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    kpg__btpc = qiy__sva(typemap, calltypes)
    pm = rjpt__gqc(typingctx, targetctx, None, f_ir, typemap, umlh__urj,
        calltypes, kpg__btpc, {}, mcta__dbyme, None)
    shn__ote = numba.core.compiler.DefaultPassBuilder.define_untyped_pipeline(
        pm)
    pm = rjpt__gqc(typingctx, targetctx, None, f_ir, typemap, umlh__urj,
        calltypes, kpg__btpc, {}, mcta__dbyme, shn__ote)
    xuqbp__pbepd = numba.core.typed_passes.InlineOverloads()
    xuqbp__pbepd.run_pass(pm)
    ezpp__brpk = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    ezpp__brpk.run()
    for block in f_ir.blocks.values():
        for yrjzx__ccmam in block.body:
            if is_assign(yrjzx__ccmam) and isinstance(yrjzx__ccmam.value, (
                ir.Arg, ir.Var)) and isinstance(typemap[yrjzx__ccmam.target
                .name], SeriesType):
                rpa__krdq = typemap.pop(yrjzx__ccmam.target.name)
                typemap[yrjzx__ccmam.target.name] = rpa__krdq.data
            if is_call_assign(yrjzx__ccmam) and find_callname(f_ir,
                yrjzx__ccmam.value) == ('get_series_data',
                'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[yrjzx__ccmam.target.name].remove(yrjzx__ccmam
                    .value)
                yrjzx__ccmam.value = yrjzx__ccmam.value.args[0]
                f_ir._definitions[yrjzx__ccmam.target.name].append(yrjzx__ccmam
                    .value)
            if is_call_assign(yrjzx__ccmam) and find_callname(f_ir,
                yrjzx__ccmam.value) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[yrjzx__ccmam.target.name].remove(yrjzx__ccmam
                    .value)
                yrjzx__ccmam.value = ir.Const(False, yrjzx__ccmam.loc)
                f_ir._definitions[yrjzx__ccmam.target.name].append(yrjzx__ccmam
                    .value)
            if is_call_assign(yrjzx__ccmam) and find_callname(f_ir,
                yrjzx__ccmam.value) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[yrjzx__ccmam.target.name].remove(yrjzx__ccmam
                    .value)
                yrjzx__ccmam.value = ir.Const(False, yrjzx__ccmam.loc)
                f_ir._definitions[yrjzx__ccmam.target.name].append(yrjzx__ccmam
                    .value)
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    ddk__szoea = numba.parfors.parfor.PreParforPass(f_ir, typemap,
        calltypes, typingctx, targetctx, hunxd__gsgf)
    ddk__szoea.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    iwi__fvc = numba.core.compiler.StateDict()
    iwi__fvc.func_ir = f_ir
    iwi__fvc.typemap = typemap
    iwi__fvc.calltypes = calltypes
    iwi__fvc.typingctx = typingctx
    iwi__fvc.targetctx = targetctx
    iwi__fvc.return_type = umlh__urj
    numba.core.rewrites.rewrite_registry.apply('after-inference', iwi__fvc)
    iqzb__hey = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        umlh__urj, typingctx, targetctx, hunxd__gsgf, mcta__dbyme, {})
    iqzb__hey.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            bwab__hde = ctypes.pythonapi.PyCell_Get
            bwab__hde.restype = ctypes.py_object
            bwab__hde.argtypes = ctypes.py_object,
            chr__ngvh = tuple(bwab__hde(zfiwq__xtgfy) for zfiwq__xtgfy in
                closure)
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            chr__ngvh = closure.items
        assert len(code.co_freevars) == len(chr__ngvh)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks, chr__ngvh)


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
        pgr__ovd = SeriesType(in_col_typ.dtype, to_str_arr_if_dict_array(
            in_col_typ), None, string_type)
        f_ir, pm = compile_to_optimized_ir(func, (pgr__ovd,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        ztu__ehm, arr_var = _rm_arg_agg_block(block, pm.typemap)
        eqt__gek = -1
        for bhcf__kzj, yrjzx__ccmam in enumerate(ztu__ehm):
            if isinstance(yrjzx__ccmam, numba.parfors.parfor.Parfor):
                assert eqt__gek == -1, 'only one parfor for aggregation function'
                eqt__gek = bhcf__kzj
        parfor = None
        if eqt__gek != -1:
            parfor = ztu__ehm[eqt__gek]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = ztu__ehm[:eqt__gek] + parfor.init_block.body
        eval_nodes = ztu__ehm[eqt__gek + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for yrjzx__ccmam in init_nodes:
            if is_assign(yrjzx__ccmam) and yrjzx__ccmam.target.name in redvars:
                ind = redvars.index(yrjzx__ccmam.target.name)
                reduce_vars[ind] = yrjzx__ccmam.target
        var_types = [pm.typemap[kymr__anoi] for kymr__anoi in redvars]
        lmqw__cvph = gen_combine_func(f_ir, parfor, redvars, var_to_redvar,
            var_types, arr_var, pm, self.typingctx, self.targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        qaka__khfs = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        pqmyr__pnt = gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types,
            pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(pqmyr__pnt)
        self.all_update_funcs.append(qaka__khfs)
        self.all_combine_funcs.append(lmqw__cvph)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        dsxz__xwik = gen_init_func(self.all_init_nodes, self.
            all_reduce_vars, self.all_vartypes, self.typingctx, self.targetctx)
        haq__hency = gen_all_update_func(self.all_update_funcs, self.
            in_col_types, self.redvar_offsets)
        xnxeh__sbif = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.targetctx)
        bmxl__ufiqo = gen_all_eval_func(self.all_eval_funcs, self.
            redvar_offsets)
        return (self.all_vartypes, dsxz__xwik, haq__hency, xnxeh__sbif,
            bmxl__ufiqo)


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
    xky__afvs = []
    for t, omu__dswx in zip(in_col_types, agg_func):
        xky__afvs.append((t, omu__dswx))
    jxb__jxu = RegularUDFGenerator(in_col_types, typingctx, targetctx)
    mtcnp__etx = GeneralUDFGenerator()
    for in_col_typ, func in xky__afvs:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            jxb__jxu.add_udf(in_col_typ, func)
        except:
            mtcnp__etx.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = jxb__jxu.gen_all_func()
    general_udf_funcs = mtcnp__etx.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    uil__vfvpt = compute_use_defs(parfor.loop_body)
    yib__hcbn = set()
    for yoa__joon in uil__vfvpt.usemap.values():
        yib__hcbn |= yoa__joon
    tsrcf__szta = set()
    for yoa__joon in uil__vfvpt.defmap.values():
        tsrcf__szta |= yoa__joon
    wxq__earyr = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    wxq__earyr.body = eval_nodes
    akmej__ygzd = compute_use_defs({(0): wxq__earyr})
    mcjbj__wswob = akmej__ygzd.usemap[0]
    tsl__pzouv = set()
    ydbkp__lye = []
    wun__ovyv = []
    for yrjzx__ccmam in reversed(init_nodes):
        wjrkm__qcda = {kymr__anoi.name for kymr__anoi in yrjzx__ccmam.
            list_vars()}
        if is_assign(yrjzx__ccmam):
            kymr__anoi = yrjzx__ccmam.target.name
            wjrkm__qcda.remove(kymr__anoi)
            if (kymr__anoi in yib__hcbn and kymr__anoi not in tsl__pzouv and
                kymr__anoi not in mcjbj__wswob and kymr__anoi not in
                tsrcf__szta):
                wun__ovyv.append(yrjzx__ccmam)
                yib__hcbn |= wjrkm__qcda
                tsrcf__szta.add(kymr__anoi)
                continue
        tsl__pzouv |= wjrkm__qcda
        ydbkp__lye.append(yrjzx__ccmam)
    wun__ovyv.reverse()
    ydbkp__lye.reverse()
    aim__urknp = min(parfor.loop_body.keys())
    tujs__dli = parfor.loop_body[aim__urknp]
    tujs__dli.body = wun__ovyv + tujs__dli.body
    return ydbkp__lye


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    qmd__cbrv = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    dlm__apbl = set()
    werjj__hddji = []
    for yrjzx__ccmam in init_nodes:
        if is_assign(yrjzx__ccmam) and isinstance(yrjzx__ccmam.value, ir.Global
            ) and isinstance(yrjzx__ccmam.value.value, pytypes.FunctionType
            ) and yrjzx__ccmam.value.value in qmd__cbrv:
            dlm__apbl.add(yrjzx__ccmam.target.name)
        elif is_call_assign(yrjzx__ccmam
            ) and yrjzx__ccmam.value.func.name in dlm__apbl:
            pass
        else:
            werjj__hddji.append(yrjzx__ccmam)
    init_nodes = werjj__hddji
    okfm__jtdip = types.Tuple(var_types)
    liosl__tmnb = lambda : None
    f_ir = compile_to_numba_ir(liosl__tmnb, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    rilz__wprr = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    yith__jai = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc), rilz__wprr,
        loc)
    block.body = block.body[-2:]
    block.body = init_nodes + [yith__jai] + block.body
    block.body[-2].value.value = rilz__wprr
    kopoi__wwe = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        okfm__jtdip, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    jfwex__csz = numba.core.target_extension.dispatcher_registry[cpu_target](
        liosl__tmnb)
    jfwex__csz.add_overload(kopoi__wwe)
    return jfwex__csz


def gen_all_update_func(update_funcs, in_col_types, redvar_offsets):
    rai__xip = len(update_funcs)
    rdb__jewi = len(in_col_types)
    alp__iwurj = 'def update_all_f(redvar_arrs, data_in, w_ind, i):\n'
    for hwq__vjoh in range(rai__xip):
        hed__fee = ', '.join(['redvar_arrs[{}][w_ind]'.format(bhcf__kzj) for
            bhcf__kzj in range(redvar_offsets[hwq__vjoh], redvar_offsets[
            hwq__vjoh + 1])])
        if hed__fee:
            alp__iwurj += ('  {} = update_vars_{}({},  data_in[{}][i])\n'.
                format(hed__fee, hwq__vjoh, hed__fee, 0 if rdb__jewi == 1 else
                hwq__vjoh))
    alp__iwurj += '  return\n'
    mxxr__swc = {}
    for bhcf__kzj, omu__dswx in enumerate(update_funcs):
        mxxr__swc['update_vars_{}'.format(bhcf__kzj)] = omu__dswx
    kubd__njl = {}
    exec(alp__iwurj, mxxr__swc, kubd__njl)
    imzi__bmzu = kubd__njl['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(imzi__bmzu)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx):
    zsev__edzj = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types]
        )
    arg_typs = zsev__edzj, zsev__edzj, types.intp, types.intp
    bap__dfg = len(redvar_offsets) - 1
    alp__iwurj = 'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i):\n'
    for hwq__vjoh in range(bap__dfg):
        hed__fee = ', '.join(['redvar_arrs[{}][w_ind]'.format(bhcf__kzj) for
            bhcf__kzj in range(redvar_offsets[hwq__vjoh], redvar_offsets[
            hwq__vjoh + 1])])
        ebs__bxfy = ', '.join(['recv_arrs[{}][i]'.format(bhcf__kzj) for
            bhcf__kzj in range(redvar_offsets[hwq__vjoh], redvar_offsets[
            hwq__vjoh + 1])])
        if ebs__bxfy:
            alp__iwurj += '  {} = combine_vars_{}({}, {})\n'.format(hed__fee,
                hwq__vjoh, hed__fee, ebs__bxfy)
    alp__iwurj += '  return\n'
    mxxr__swc = {}
    for bhcf__kzj, omu__dswx in enumerate(combine_funcs):
        mxxr__swc['combine_vars_{}'.format(bhcf__kzj)] = omu__dswx
    kubd__njl = {}
    exec(alp__iwurj, mxxr__swc, kubd__njl)
    nopcq__lqhx = kubd__njl['combine_all_f']
    f_ir = compile_to_numba_ir(nopcq__lqhx, mxxr__swc)
    xnxeh__sbif = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    jfwex__csz = numba.core.target_extension.dispatcher_registry[cpu_target](
        nopcq__lqhx)
    jfwex__csz.add_overload(xnxeh__sbif)
    return jfwex__csz


def gen_all_eval_func(eval_funcs, redvar_offsets):
    bap__dfg = len(redvar_offsets) - 1
    alp__iwurj = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    for hwq__vjoh in range(bap__dfg):
        hed__fee = ', '.join(['redvar_arrs[{}][j]'.format(bhcf__kzj) for
            bhcf__kzj in range(redvar_offsets[hwq__vjoh], redvar_offsets[
            hwq__vjoh + 1])])
        alp__iwurj += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(hwq__vjoh
            , hwq__vjoh, hed__fee)
    alp__iwurj += '  return\n'
    mxxr__swc = {}
    for bhcf__kzj, omu__dswx in enumerate(eval_funcs):
        mxxr__swc['eval_vars_{}'.format(bhcf__kzj)] = omu__dswx
    kubd__njl = {}
    exec(alp__iwurj, mxxr__swc, kubd__njl)
    sgva__szy = kubd__njl['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(sgva__szy)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    xhyul__zffdi = len(var_types)
    tropp__ankma = [f'in{bhcf__kzj}' for bhcf__kzj in range(xhyul__zffdi)]
    okfm__jtdip = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    nppt__fnzhm = okfm__jtdip(0)
    alp__iwurj = 'def agg_eval({}):\n return _zero\n'.format(', '.join(
        tropp__ankma))
    kubd__njl = {}
    exec(alp__iwurj, {'_zero': nppt__fnzhm}, kubd__njl)
    wwkma__hhwu = kubd__njl['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(wwkma__hhwu, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': nppt__fnzhm}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    kocq__prk = []
    for bhcf__kzj, kymr__anoi in enumerate(reduce_vars):
        kocq__prk.append(ir.Assign(block.body[bhcf__kzj].target, kymr__anoi,
            kymr__anoi.loc))
        for pvn__gwzzt in kymr__anoi.versioned_names:
            kocq__prk.append(ir.Assign(kymr__anoi, ir.Var(kymr__anoi.scope,
                pvn__gwzzt, kymr__anoi.loc), kymr__anoi.loc))
    block.body = block.body[:xhyul__zffdi] + kocq__prk + eval_nodes
    pqmyr__pnt = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        okfm__jtdip, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    jfwex__csz = numba.core.target_extension.dispatcher_registry[cpu_target](
        wwkma__hhwu)
    jfwex__csz.add_overload(pqmyr__pnt)
    return jfwex__csz


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    xhyul__zffdi = len(redvars)
    ljzlg__jvpq = [f'v{bhcf__kzj}' for bhcf__kzj in range(xhyul__zffdi)]
    tropp__ankma = [f'in{bhcf__kzj}' for bhcf__kzj in range(xhyul__zffdi)]
    alp__iwurj = 'def agg_combine({}):\n'.format(', '.join(ljzlg__jvpq +
        tropp__ankma))
    yupj__vrptc = wrap_parfor_blocks(parfor)
    luox__lgn = find_topo_order(yupj__vrptc)
    luox__lgn = luox__lgn[1:]
    unwrap_parfor_blocks(parfor)
    ovewy__bve = {}
    pypdg__haqf = []
    for cfmai__eoisi in luox__lgn:
        ggsen__qxv = parfor.loop_body[cfmai__eoisi]
        for yrjzx__ccmam in ggsen__qxv.body:
            if is_assign(yrjzx__ccmam) and yrjzx__ccmam.target.name in redvars:
                jpd__foa = yrjzx__ccmam.target.name
                ind = redvars.index(jpd__foa)
                if ind in pypdg__haqf:
                    continue
                if len(f_ir._definitions[jpd__foa]) == 2:
                    var_def = f_ir._definitions[jpd__foa][0]
                    alp__iwurj += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[jpd__foa][1]
                    alp__iwurj += _match_reduce_def(var_def, f_ir, ind)
    alp__iwurj += '    return {}'.format(', '.join(['v{}'.format(bhcf__kzj) for
        bhcf__kzj in range(xhyul__zffdi)]))
    kubd__njl = {}
    exec(alp__iwurj, {}, kubd__njl)
    ibz__cxs = kubd__njl['agg_combine']
    arg_typs = tuple(2 * var_types)
    mxxr__swc = {'numba': numba, 'bodo': bodo, 'np': np}
    mxxr__swc.update(ovewy__bve)
    f_ir = compile_to_numba_ir(ibz__cxs, mxxr__swc, typingctx=typingctx,
        targetctx=targetctx, arg_typs=arg_typs, typemap=pm.typemap,
        calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    okfm__jtdip = pm.typemap[block.body[-1].value.name]
    lmqw__cvph = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        okfm__jtdip, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    jfwex__csz = numba.core.target_extension.dispatcher_registry[cpu_target](
        ibz__cxs)
    jfwex__csz.add_overload(lmqw__cvph)
    return jfwex__csz


def _match_reduce_def(var_def, f_ir, ind):
    alp__iwurj = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        alp__iwurj = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        uujp__gtrck = guard(find_callname, f_ir, var_def)
        if uujp__gtrck == ('min', 'builtins'):
            alp__iwurj = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if uujp__gtrck == ('max', 'builtins'):
            alp__iwurj = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return alp__iwurj


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    xhyul__zffdi = len(redvars)
    fcyw__tzh = 1
    in_vars = []
    for bhcf__kzj in range(fcyw__tzh):
        nji__xduy = ir.Var(arr_var.scope, f'$input{bhcf__kzj}', arr_var.loc)
        in_vars.append(nji__xduy)
    caak__aan = parfor.loop_nests[0].index_variable
    wkb__eujfw = [0] * xhyul__zffdi
    for ggsen__qxv in parfor.loop_body.values():
        yak__wif = []
        for yrjzx__ccmam in ggsen__qxv.body:
            if is_var_assign(yrjzx__ccmam
                ) and yrjzx__ccmam.value.name == caak__aan.name:
                continue
            if is_getitem(yrjzx__ccmam
                ) and yrjzx__ccmam.value.value.name == arr_var.name:
                yrjzx__ccmam.value = in_vars[0]
            if is_call_assign(yrjzx__ccmam) and guard(find_callname, pm.
                func_ir, yrjzx__ccmam.value) == ('isna',
                'bodo.libs.array_kernels') and yrjzx__ccmam.value.args[0
                ].name == arr_var.name:
                yrjzx__ccmam.value = ir.Const(False, yrjzx__ccmam.target.loc)
            if is_assign(yrjzx__ccmam) and yrjzx__ccmam.target.name in redvars:
                ind = redvars.index(yrjzx__ccmam.target.name)
                wkb__eujfw[ind] = yrjzx__ccmam.target
            yak__wif.append(yrjzx__ccmam)
        ggsen__qxv.body = yak__wif
    ljzlg__jvpq = ['v{}'.format(bhcf__kzj) for bhcf__kzj in range(xhyul__zffdi)
        ]
    tropp__ankma = ['in{}'.format(bhcf__kzj) for bhcf__kzj in range(fcyw__tzh)]
    alp__iwurj = 'def agg_update({}):\n'.format(', '.join(ljzlg__jvpq +
        tropp__ankma))
    alp__iwurj += '    __update_redvars()\n'
    alp__iwurj += '    return {}'.format(', '.join(['v{}'.format(bhcf__kzj) for
        bhcf__kzj in range(xhyul__zffdi)]))
    kubd__njl = {}
    exec(alp__iwurj, {}, kubd__njl)
    jyq__pitpr = kubd__njl['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * fcyw__tzh)
    f_ir = compile_to_numba_ir(jyq__pitpr, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    xatqg__jalje = f_ir.blocks.popitem()[1].body
    okfm__jtdip = pm.typemap[xatqg__jalje[-1].value.name]
    yupj__vrptc = wrap_parfor_blocks(parfor)
    luox__lgn = find_topo_order(yupj__vrptc)
    luox__lgn = luox__lgn[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    tujs__dli = f_ir.blocks[luox__lgn[0]]
    xeef__uaun = f_ir.blocks[luox__lgn[-1]]
    pokp__mpndv = xatqg__jalje[:xhyul__zffdi + fcyw__tzh]
    if xhyul__zffdi > 1:
        nkku__iyw = xatqg__jalje[-3:]
        assert is_assign(nkku__iyw[0]) and isinstance(nkku__iyw[0].value,
            ir.Expr) and nkku__iyw[0].value.op == 'build_tuple'
    else:
        nkku__iyw = xatqg__jalje[-2:]
    for bhcf__kzj in range(xhyul__zffdi):
        seizo__zpu = xatqg__jalje[bhcf__kzj].target
        lghx__cmlsg = ir.Assign(seizo__zpu, wkb__eujfw[bhcf__kzj],
            seizo__zpu.loc)
        pokp__mpndv.append(lghx__cmlsg)
    for bhcf__kzj in range(xhyul__zffdi, xhyul__zffdi + fcyw__tzh):
        seizo__zpu = xatqg__jalje[bhcf__kzj].target
        lghx__cmlsg = ir.Assign(seizo__zpu, in_vars[bhcf__kzj -
            xhyul__zffdi], seizo__zpu.loc)
        pokp__mpndv.append(lghx__cmlsg)
    tujs__dli.body = pokp__mpndv + tujs__dli.body
    olef__cml = []
    for bhcf__kzj in range(xhyul__zffdi):
        seizo__zpu = xatqg__jalje[bhcf__kzj].target
        lghx__cmlsg = ir.Assign(wkb__eujfw[bhcf__kzj], seizo__zpu,
            seizo__zpu.loc)
        olef__cml.append(lghx__cmlsg)
    xeef__uaun.body += olef__cml + nkku__iyw
    jafbh__uqyum = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        okfm__jtdip, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    jfwex__csz = numba.core.target_extension.dispatcher_registry[cpu_target](
        jyq__pitpr)
    jfwex__csz.add_overload(jafbh__uqyum)
    return jfwex__csz


def _rm_arg_agg_block(block, typemap):
    ztu__ehm = []
    arr_var = None
    for bhcf__kzj, yrjzx__ccmam in enumerate(block.body):
        if is_assign(yrjzx__ccmam) and isinstance(yrjzx__ccmam.value, ir.Arg):
            arr_var = yrjzx__ccmam.target
            str__gurfm = typemap[arr_var.name]
            if not isinstance(str__gurfm, types.ArrayCompatible):
                ztu__ehm += block.body[bhcf__kzj + 1:]
                break
            vegh__ljox = block.body[bhcf__kzj + 1]
            assert is_assign(vegh__ljox) and isinstance(vegh__ljox.value,
                ir.Expr
                ) and vegh__ljox.value.op == 'getattr' and vegh__ljox.value.attr == 'shape' and vegh__ljox.value.value.name == arr_var.name
            drqf__rnz = vegh__ljox.target
            pvac__tadb = block.body[bhcf__kzj + 2]
            assert is_assign(pvac__tadb) and isinstance(pvac__tadb.value,
                ir.Expr
                ) and pvac__tadb.value.op == 'static_getitem' and pvac__tadb.value.value.name == drqf__rnz.name
            ztu__ehm += block.body[bhcf__kzj + 3:]
            break
        ztu__ehm.append(yrjzx__ccmam)
    return ztu__ehm, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    yupj__vrptc = wrap_parfor_blocks(parfor)
    luox__lgn = find_topo_order(yupj__vrptc)
    luox__lgn = luox__lgn[1:]
    unwrap_parfor_blocks(parfor)
    for cfmai__eoisi in reversed(luox__lgn):
        for yrjzx__ccmam in reversed(parfor.loop_body[cfmai__eoisi].body):
            if isinstance(yrjzx__ccmam, ir.Assign) and (yrjzx__ccmam.target
                .name in parfor_params or yrjzx__ccmam.target.name in
                var_to_param):
                jqnwd__dqbvn = yrjzx__ccmam.target.name
                rhs = yrjzx__ccmam.value
                avkh__omxwy = (jqnwd__dqbvn if jqnwd__dqbvn in
                    parfor_params else var_to_param[jqnwd__dqbvn])
                yyum__mghx = []
                if isinstance(rhs, ir.Var):
                    yyum__mghx = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    yyum__mghx = [kymr__anoi.name for kymr__anoi in
                        yrjzx__ccmam.value.list_vars()]
                param_uses[avkh__omxwy].extend(yyum__mghx)
                for kymr__anoi in yyum__mghx:
                    var_to_param[kymr__anoi] = avkh__omxwy
            if isinstance(yrjzx__ccmam, Parfor):
                get_parfor_reductions(yrjzx__ccmam, parfor_params,
                    calltypes, reduce_varnames, param_uses, var_to_param)
    for orhkt__xyvr, yyum__mghx in param_uses.items():
        if orhkt__xyvr in yyum__mghx and orhkt__xyvr not in reduce_varnames:
            reduce_varnames.append(orhkt__xyvr)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
