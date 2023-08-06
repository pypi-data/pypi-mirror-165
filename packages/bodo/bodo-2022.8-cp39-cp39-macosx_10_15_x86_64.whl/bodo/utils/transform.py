"""
Helper functions for transformations.
"""
import itertools
import math
import operator
import types as pytypes
from collections import namedtuple
import numba
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, types
from numba.core.ir_utils import GuardException, build_definitions, compile_to_numba_ir, compute_cfg_from_blocks, find_callname, find_const, get_definition, guard, is_setitem, mk_unique_var, replace_arg_nodes, require
from numba.core.registry import CPUDispatcher
from numba.core.typing.templates import fold_arguments
import bodo
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.struct_arr_ext import StructArrayType, StructType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoConstUpdatedError, BodoError, can_literalize_type, get_literal_value, get_overload_const_bool, get_overload_const_list, is_literal_type, is_overload_constant_bool
from bodo.utils.utils import is_array_typ, is_assign, is_call, is_expr
ReplaceFunc = namedtuple('ReplaceFunc', ['func', 'arg_types', 'args',
    'glbls', 'inline_bodo_calls', 'run_full_pipeline', 'pre_nodes'])
bodo_types_with_params = {'ArrayItemArrayType', 'CSRMatrixType',
    'CategoricalArrayType', 'CategoricalIndexType', 'DataFrameType',
    'DatetimeIndexType', 'Decimal128Type', 'DecimalArrayType',
    'IntegerArrayType', 'IntervalArrayType', 'IntervalIndexType', 'List',
    'MapArrayType', 'NumericIndexType', 'PDCategoricalDtype',
    'PeriodIndexType', 'RangeIndexType', 'SeriesType', 'StringIndexType',
    'BinaryIndexType', 'StructArrayType', 'TimedeltaIndexType',
    'TupleArrayType'}
container_update_method_names = ('clear', 'pop', 'popitem', 'update', 'add',
    'difference_update', 'discard', 'intersection_update', 'remove',
    'symmetric_difference_update', 'append', 'extend', 'insert', 'reverse',
    'sort')
no_side_effect_call_tuples = {(int,), (list,), (set,), (dict,), (min,), (
    max,), (abs,), (len,), (bool,), (str,), ('ceil', math), ('init_series',
    'pd_series_ext', 'hiframes', bodo), ('get_series_data', 'pd_series_ext',
    'hiframes', bodo), ('get_series_index', 'pd_series_ext', 'hiframes',
    bodo), ('get_series_name', 'pd_series_ext', 'hiframes', bodo), (
    'get_index_data', 'pd_index_ext', 'hiframes', bodo), ('get_index_name',
    'pd_index_ext', 'hiframes', bodo), ('init_binary_str_index',
    'pd_index_ext', 'hiframes', bodo), ('init_numeric_index',
    'pd_index_ext', 'hiframes', bodo), ('init_categorical_index',
    'pd_index_ext', 'hiframes', bodo), ('_dti_val_finalize', 'pd_index_ext',
    'hiframes', bodo), ('init_datetime_index', 'pd_index_ext', 'hiframes',
    bodo), ('init_timedelta_index', 'pd_index_ext', 'hiframes', bodo), (
    'init_range_index', 'pd_index_ext', 'hiframes', bodo), (
    'init_heter_index', 'pd_index_ext', 'hiframes', bodo), (
    'get_int_arr_data', 'int_arr_ext', 'libs', bodo), ('get_int_arr_bitmap',
    'int_arr_ext', 'libs', bodo), ('init_integer_array', 'int_arr_ext',
    'libs', bodo), ('alloc_int_array', 'int_arr_ext', 'libs', bodo), (
    'inplace_eq', 'str_arr_ext', 'libs', bodo), ('get_bool_arr_data',
    'bool_arr_ext', 'libs', bodo), ('get_bool_arr_bitmap', 'bool_arr_ext',
    'libs', bodo), ('init_bool_array', 'bool_arr_ext', 'libs', bodo), (
    'alloc_bool_array', 'bool_arr_ext', 'libs', bodo), (
    'datetime_date_arr_to_dt64_arr', 'pd_timestamp_ext', 'hiframes', bodo),
    (bodo.libs.bool_arr_ext.compute_or_body,), (bodo.libs.bool_arr_ext.
    compute_and_body,), ('alloc_datetime_date_array', 'datetime_date_ext',
    'hiframes', bodo), ('alloc_datetime_timedelta_array',
    'datetime_timedelta_ext', 'hiframes', bodo), ('cat_replace',
    'pd_categorical_ext', 'hiframes', bodo), ('init_categorical_array',
    'pd_categorical_ext', 'hiframes', bodo), ('alloc_categorical_array',
    'pd_categorical_ext', 'hiframes', bodo), ('get_categorical_arr_codes',
    'pd_categorical_ext', 'hiframes', bodo), ('_sum_handle_nan',
    'series_kernels', 'hiframes', bodo), ('_box_cat_val', 'series_kernels',
    'hiframes', bodo), ('_mean_handle_nan', 'series_kernels', 'hiframes',
    bodo), ('_var_handle_mincount', 'series_kernels', 'hiframes', bodo), (
    '_compute_var_nan_count_ddof', 'series_kernels', 'hiframes', bodo), (
    '_sem_handle_nan', 'series_kernels', 'hiframes', bodo), ('dist_return',
    'distributed_api', 'libs', bodo), ('rep_return', 'distributed_api',
    'libs', bodo), ('init_dataframe', 'pd_dataframe_ext', 'hiframes', bodo),
    ('get_dataframe_data', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_all_data', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_table', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_column_names', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_table_data', 'table', 'hiframes', bodo), ('get_dataframe_index',
    'pd_dataframe_ext', 'hiframes', bodo), ('init_rolling',
    'pd_rolling_ext', 'hiframes', bodo), ('init_groupby', 'pd_groupby_ext',
    'hiframes', bodo), ('calc_nitems', 'array_kernels', 'libs', bodo), (
    'concat', 'array_kernels', 'libs', bodo), ('unique', 'array_kernels',
    'libs', bodo), ('nunique', 'array_kernels', 'libs', bodo), ('quantile',
    'array_kernels', 'libs', bodo), ('explode', 'array_kernels', 'libs',
    bodo), ('explode_no_index', 'array_kernels', 'libs', bodo), (
    'get_arr_lens', 'array_kernels', 'libs', bodo), (
    'str_arr_from_sequence', 'str_arr_ext', 'libs', bodo), (
    'get_str_arr_str_length', 'str_arr_ext', 'libs', bodo), (
    'parse_datetime_str', 'pd_timestamp_ext', 'hiframes', bodo), (
    'integer_to_dt64', 'pd_timestamp_ext', 'hiframes', bodo), (
    'dt64_to_integer', 'pd_timestamp_ext', 'hiframes', bodo), (
    'timedelta64_to_integer', 'pd_timestamp_ext', 'hiframes', bodo), (
    'integer_to_timedelta64', 'pd_timestamp_ext', 'hiframes', bodo), (
    'npy_datetimestruct_to_datetime', 'pd_timestamp_ext', 'hiframes', bodo),
    ('isna', 'array_kernels', 'libs', bodo), (bodo.libs.str_arr_ext.
    num_total_chars,), ('num_total_chars', 'str_arr_ext', 'libs', bodo), (
    'copy',), ('from_iterable_impl', 'typing', 'utils', bodo), ('chain',
    itertools), ('groupby',), ('rolling',), (pd.CategoricalDtype,), (bodo.
    hiframes.pd_categorical_ext.get_code_for_value,), ('asarray', np), (
    'int32', np), ('int64', np), ('float64', np), ('float32', np), ('bool_',
    np), ('full', np), ('round', np), ('isnan', np), ('isnat', np), (
    'arange', np), ('internal_prange', 'parfor', numba), ('internal_prange',
    'parfor', 'parfors', numba), ('empty_inferred', 'ndarray', 'unsafe',
    numba), ('_slice_span', 'unicode', numba), ('_normalize_slice',
    'unicode', numba), ('init_session_builder', 'pyspark_ext', 'libs', bodo
    ), ('init_session', 'pyspark_ext', 'libs', bodo), ('init_spark_df',
    'pyspark_ext', 'libs', bodo), ('h5size', 'h5_api', 'io', bodo), (
    'pre_alloc_struct_array', 'struct_arr_ext', 'libs', bodo), (bodo.libs.
    struct_arr_ext.pre_alloc_struct_array,), ('pre_alloc_tuple_array',
    'tuple_arr_ext', 'libs', bodo), (bodo.libs.tuple_arr_ext.
    pre_alloc_tuple_array,), ('pre_alloc_array_item_array',
    'array_item_arr_ext', 'libs', bodo), (bodo.libs.array_item_arr_ext.
    pre_alloc_array_item_array,), ('dist_reduce', 'distributed_api', 'libs',
    bodo), (bodo.libs.distributed_api.dist_reduce,), (
    'pre_alloc_string_array', 'str_arr_ext', 'libs', bodo), (bodo.libs.
    str_arr_ext.pre_alloc_string_array,), ('pre_alloc_binary_array',
    'binary_arr_ext', 'libs', bodo), (bodo.libs.binary_arr_ext.
    pre_alloc_binary_array,), ('pre_alloc_map_array', 'map_arr_ext', 'libs',
    bodo), (bodo.libs.map_arr_ext.pre_alloc_map_array,), (
    'convert_dict_arr_to_int', 'dict_arr_ext', 'libs', bodo), (
    'cat_dict_str', 'dict_arr_ext', 'libs', bodo), ('str_replace',
    'dict_arr_ext', 'libs', bodo), ('dict_arr_eq', 'dict_arr_ext', 'libs',
    bodo), ('dict_arr_ne', 'dict_arr_ext', 'libs', bodo), ('str_startswith',
    'dict_arr_ext', 'libs', bodo), ('str_endswith', 'dict_arr_ext', 'libs',
    bodo), ('str_contains_non_regex', 'dict_arr_ext', 'libs', bodo), (
    'str_series_contains_regex', 'dict_arr_ext', 'libs', bodo), (
    'str_capitalize', 'dict_arr_ext', 'libs', bodo), ('str_lower',
    'dict_arr_ext', 'libs', bodo), ('str_swapcase', 'dict_arr_ext', 'libs',
    bodo), ('str_title', 'dict_arr_ext', 'libs', bodo), ('str_upper',
    'dict_arr_ext', 'libs', bodo), ('str_center', 'dict_arr_ext', 'libs',
    bodo), ('str_get', 'dict_arr_ext', 'libs', bodo), ('str_repeat_int',
    'dict_arr_ext', 'libs', bodo), ('str_lstrip', 'dict_arr_ext', 'libs',
    bodo), ('str_rstrip', 'dict_arr_ext', 'libs', bodo), ('str_strip',
    'dict_arr_ext', 'libs', bodo), ('str_zfill', 'dict_arr_ext', 'libs',
    bodo), ('str_ljust', 'dict_arr_ext', 'libs', bodo), ('str_rjust',
    'dict_arr_ext', 'libs', bodo), ('str_find', 'dict_arr_ext', 'libs',
    bodo), ('str_rfind', 'dict_arr_ext', 'libs', bodo), ('str_index',
    'dict_arr_ext', 'libs', bodo), ('str_rindex', 'dict_arr_ext', 'libs',
    bodo), ('str_slice', 'dict_arr_ext', 'libs', bodo), ('str_extract',
    'dict_arr_ext', 'libs', bodo), ('str_extractall', 'dict_arr_ext',
    'libs', bodo), ('str_extractall_multi', 'dict_arr_ext', 'libs', bodo),
    ('str_len', 'dict_arr_ext', 'libs', bodo), ('str_count', 'dict_arr_ext',
    'libs', bodo), ('str_isalnum', 'dict_arr_ext', 'libs', bodo), (
    'str_isalpha', 'dict_arr_ext', 'libs', bodo), ('str_isdigit',
    'dict_arr_ext', 'libs', bodo), ('str_isspace', 'dict_arr_ext', 'libs',
    bodo), ('str_islower', 'dict_arr_ext', 'libs', bodo), ('str_isupper',
    'dict_arr_ext', 'libs', bodo), ('str_istitle', 'dict_arr_ext', 'libs',
    bodo), ('str_isnumeric', 'dict_arr_ext', 'libs', bodo), (
    'str_isdecimal', 'dict_arr_ext', 'libs', bodo), ('str_match',
    'dict_arr_ext', 'libs', bodo), ('prange', bodo), (bodo.prange,), (
    'objmode', bodo), (bodo.objmode,), ('get_label_dict_from_categories',
    'pd_categorial_ext', 'hiframes', bodo), (
    'get_label_dict_from_categories_no_duplicates', 'pd_categorial_ext',
    'hiframes', bodo), ('build_nullable_tuple', 'nullable_tuple_ext',
    'libs', bodo), ('generate_mappable_table_func', 'table_utils', 'utils',
    bodo), ('table_astype', 'table_utils', 'utils', bodo), ('table_concat',
    'table_utils', 'utils', bodo), ('table_filter', 'table', 'hiframes',
    bodo), ('table_subset', 'table', 'hiframes', bodo), (
    'logical_table_to_table', 'table', 'hiframes', bodo), ('startswith',),
    ('endswith',), ('upper',), ('lower',)}
_np_type_names = {'int8', 'int16', 'int32', 'int64', 'uint8', 'uint16',
    'uint32', 'uint64', 'float32', 'float64', 'bool_'}


def remove_hiframes(rhs, lives, call_list):
    kbx__goqrq = tuple(call_list)
    if kbx__goqrq in no_side_effect_call_tuples:
        return True
    if kbx__goqrq == (bodo.hiframes.pd_index_ext.init_range_index,):
        return True
    if len(call_list) == 4 and call_list[1:] == ['conversion', 'utils', bodo]:
        return True
    if isinstance(call_list[-1], pytypes.ModuleType) and call_list[-1
        ].__name__ == 'bodosql':
        return True
    if len(call_list) == 2 and call_list[0] == 'copy':
        return True
    if call_list == ['h5read', 'h5_api', 'io', bodo] and rhs.args[5
        ].name not in lives:
        return True
    if call_list == ['move_str_binary_arr_payload', 'str_arr_ext', 'libs', bodo
        ] and rhs.args[0].name not in lives:
        return True
    if call_list == ['setna', 'array_kernels', 'libs', bodo] and rhs.args[0
        ].name not in lives:
        return True
    if call_list == ['set_table_data', 'table', 'hiframes', bodo] and rhs.args[
        0].name not in lives:
        return True
    if call_list == ['set_table_data_null', 'table', 'hiframes', bodo
        ] and rhs.args[0].name not in lives:
        return True
    if call_list == ['ensure_column_unboxed', 'table', 'hiframes', bodo
        ] and rhs.args[0].name not in lives and rhs.args[1].name not in lives:
        return True
    if call_list == ['generate_table_nbytes', 'table_utils', 'utils', bodo
        ] and rhs.args[1].name not in lives:
        return True
    if len(kbx__goqrq) == 1 and tuple in getattr(kbx__goqrq[0], '__mro__', ()):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=False, add_default_globals=True):
    if replace_globals:
        nlpk__pok = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd,
            'math': math}
    else:
        nlpk__pok = func.__globals__
    if extra_globals is not None:
        nlpk__pok.update(extra_globals)
    if add_default_globals:
        nlpk__pok.update({'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd,
            'math': math})
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, nlpk__pok, typingctx=typing_info.
            typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[ifijc__hqxup.name] for ifijc__hqxup in args
            ), typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, nlpk__pok)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        asv__vhg = tuple(typing_info.typemap[ifijc__hqxup.name] for
            ifijc__hqxup in args)
        ocnch__kmbe = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, asv__vhg, {}, {}, flags)
        ocnch__kmbe.run()
    opm__pki = f_ir.blocks.popitem()[1]
    replace_arg_nodes(opm__pki, args)
    hefy__fywcc = opm__pki.body[:-2]
    update_locs(hefy__fywcc[len(args):], loc)
    for stmt in hefy__fywcc[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        qit__empc = opm__pki.body[-2]
        assert is_assign(qit__empc) and is_expr(qit__empc.value, 'cast')
        ysneq__iblt = qit__empc.value.value
        hefy__fywcc.append(ir.Assign(ysneq__iblt, ret_var, loc))
    return hefy__fywcc


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for ksquq__wmu in stmt.list_vars():
            ksquq__wmu.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        ndxft__bqp = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        rpol__kkyc, mlooa__nku = ndxft__bqp(stmt)
        return mlooa__nku
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        mfub__lwvbl = get_const_value_inner(func_ir, var, arg_types,
            typemap, file_info=file_info)
        if isinstance(mfub__lwvbl, ir.UndefinedType):
            vilyi__erus = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{vilyi__erus}' is not defined", loc=loc)
    except GuardException as sbhp__qvl:
        raise BodoError(err_msg, loc=loc)
    return mfub__lwvbl


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False,
    literalize_args=True):
    require(isinstance(var, ir.Var))
    zsmlc__dqj = get_definition(func_ir, var)
    mqr__txr = None
    if typemap is not None:
        mqr__txr = typemap.get(var.name, None)
    if isinstance(zsmlc__dqj, ir.Arg) and arg_types is not None:
        mqr__txr = arg_types[zsmlc__dqj.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(mqr__txr):
        return get_literal_value(mqr__txr)
    if isinstance(zsmlc__dqj, (ir.Const, ir.Global, ir.FreeVar)):
        mfub__lwvbl = zsmlc__dqj.value
        return mfub__lwvbl
    if literalize_args and isinstance(zsmlc__dqj, ir.Arg
        ) and can_literalize_type(mqr__txr, pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({zsmlc__dqj.index}, loc=var
            .loc, file_infos={zsmlc__dqj.index: file_info} if file_info is not
            None else None)
    if is_expr(zsmlc__dqj, 'binop'):
        if file_info and zsmlc__dqj.fn == operator.add:
            try:
                ypml__gksk = get_const_value_inner(func_ir, zsmlc__dqj.lhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(ypml__gksk, True)
                iny__wwm = get_const_value_inner(func_ir, zsmlc__dqj.rhs,
                    arg_types, typemap, updated_containers, file_info)
                return zsmlc__dqj.fn(ypml__gksk, iny__wwm)
            except (GuardException, BodoConstUpdatedError) as sbhp__qvl:
                pass
            try:
                iny__wwm = get_const_value_inner(func_ir, zsmlc__dqj.rhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(iny__wwm, False)
                ypml__gksk = get_const_value_inner(func_ir, zsmlc__dqj.lhs,
                    arg_types, typemap, updated_containers, file_info)
                return zsmlc__dqj.fn(ypml__gksk, iny__wwm)
            except (GuardException, BodoConstUpdatedError) as sbhp__qvl:
                pass
        ypml__gksk = get_const_value_inner(func_ir, zsmlc__dqj.lhs,
            arg_types, typemap, updated_containers)
        iny__wwm = get_const_value_inner(func_ir, zsmlc__dqj.rhs, arg_types,
            typemap, updated_containers)
        return zsmlc__dqj.fn(ypml__gksk, iny__wwm)
    if is_expr(zsmlc__dqj, 'unary'):
        mfub__lwvbl = get_const_value_inner(func_ir, zsmlc__dqj.value,
            arg_types, typemap, updated_containers)
        return zsmlc__dqj.fn(mfub__lwvbl)
    if is_expr(zsmlc__dqj, 'getattr') and typemap:
        efkhi__zsque = typemap.get(zsmlc__dqj.value.name, None)
        if isinstance(efkhi__zsque, bodo.hiframes.pd_dataframe_ext.
            DataFrameType) and zsmlc__dqj.attr == 'columns':
            return pd.Index(efkhi__zsque.columns)
        if isinstance(efkhi__zsque, types.SliceType):
            mlov__awi = get_definition(func_ir, zsmlc__dqj.value)
            require(is_call(mlov__awi))
            xdxm__bfpp = find_callname(func_ir, mlov__awi)
            rckoe__lzei = False
            if xdxm__bfpp == ('_normalize_slice', 'numba.cpython.unicode'):
                require(zsmlc__dqj.attr in ('start', 'step'))
                mlov__awi = get_definition(func_ir, mlov__awi.args[0])
                rckoe__lzei = True
            require(find_callname(func_ir, mlov__awi) == ('slice', 'builtins'))
            if len(mlov__awi.args) == 1:
                if zsmlc__dqj.attr == 'start':
                    return 0
                if zsmlc__dqj.attr == 'step':
                    return 1
                require(zsmlc__dqj.attr == 'stop')
                return get_const_value_inner(func_ir, mlov__awi.args[0],
                    arg_types, typemap, updated_containers)
            if zsmlc__dqj.attr == 'start':
                mfub__lwvbl = get_const_value_inner(func_ir, mlov__awi.args
                    [0], arg_types, typemap, updated_containers)
                if mfub__lwvbl is None:
                    mfub__lwvbl = 0
                if rckoe__lzei:
                    require(mfub__lwvbl == 0)
                return mfub__lwvbl
            if zsmlc__dqj.attr == 'stop':
                assert not rckoe__lzei
                return get_const_value_inner(func_ir, mlov__awi.args[1],
                    arg_types, typemap, updated_containers)
            require(zsmlc__dqj.attr == 'step')
            if len(mlov__awi.args) == 2:
                return 1
            else:
                mfub__lwvbl = get_const_value_inner(func_ir, mlov__awi.args
                    [2], arg_types, typemap, updated_containers)
                if mfub__lwvbl is None:
                    mfub__lwvbl = 1
                if rckoe__lzei:
                    require(mfub__lwvbl == 1)
                return mfub__lwvbl
    if is_expr(zsmlc__dqj, 'getattr'):
        return getattr(get_const_value_inner(func_ir, zsmlc__dqj.value,
            arg_types, typemap, updated_containers), zsmlc__dqj.attr)
    if is_expr(zsmlc__dqj, 'getitem'):
        value = get_const_value_inner(func_ir, zsmlc__dqj.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, zsmlc__dqj.index, arg_types,
            typemap, updated_containers)
        return value[index]
    gzzaa__kfw = guard(find_callname, func_ir, zsmlc__dqj, typemap)
    if gzzaa__kfw is not None and len(gzzaa__kfw) == 2 and gzzaa__kfw[0
        ] == 'keys' and isinstance(gzzaa__kfw[1], ir.Var):
        ihdl__osuq = zsmlc__dqj.func
        zsmlc__dqj = get_definition(func_ir, gzzaa__kfw[1])
        cei__btqs = gzzaa__kfw[1].name
        if updated_containers and cei__btqs in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                cei__btqs, updated_containers[cei__btqs]))
        require(is_expr(zsmlc__dqj, 'build_map'))
        vals = [ksquq__wmu[0] for ksquq__wmu in zsmlc__dqj.items]
        cvx__dmb = guard(get_definition, func_ir, ihdl__osuq)
        assert isinstance(cvx__dmb, ir.Expr) and cvx__dmb.attr == 'keys'
        cvx__dmb.attr = 'copy'
        return [get_const_value_inner(func_ir, ksquq__wmu, arg_types,
            typemap, updated_containers) for ksquq__wmu in vals]
    if is_expr(zsmlc__dqj, 'build_map'):
        return {get_const_value_inner(func_ir, ksquq__wmu[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            ksquq__wmu[1], arg_types, typemap, updated_containers) for
            ksquq__wmu in zsmlc__dqj.items}
    if is_expr(zsmlc__dqj, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, ksquq__wmu, arg_types,
            typemap, updated_containers) for ksquq__wmu in zsmlc__dqj.items)
    if is_expr(zsmlc__dqj, 'build_list'):
        return [get_const_value_inner(func_ir, ksquq__wmu, arg_types,
            typemap, updated_containers) for ksquq__wmu in zsmlc__dqj.items]
    if is_expr(zsmlc__dqj, 'build_set'):
        return {get_const_value_inner(func_ir, ksquq__wmu, arg_types,
            typemap, updated_containers) for ksquq__wmu in zsmlc__dqj.items}
    if gzzaa__kfw == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, zsmlc__dqj.args[0],
            arg_types, typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if gzzaa__kfw == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, zsmlc__dqj.args[0],
            arg_types, typemap, updated_containers))
    if gzzaa__kfw == ('range', 'builtins') and len(zsmlc__dqj.args) == 1:
        return range(get_const_value_inner(func_ir, zsmlc__dqj.args[0],
            arg_types, typemap, updated_containers))
    if gzzaa__kfw == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, ksquq__wmu,
            arg_types, typemap, updated_containers) for ksquq__wmu in
            zsmlc__dqj.args))
    if gzzaa__kfw == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, zsmlc__dqj.args[0],
            arg_types, typemap, updated_containers))
    if gzzaa__kfw == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, zsmlc__dqj.args[0],
            arg_types, typemap, updated_containers))
    if gzzaa__kfw == ('format', 'builtins'):
        ifijc__hqxup = get_const_value_inner(func_ir, zsmlc__dqj.args[0],
            arg_types, typemap, updated_containers)
        whj__yfegr = get_const_value_inner(func_ir, zsmlc__dqj.args[1],
            arg_types, typemap, updated_containers) if len(zsmlc__dqj.args
            ) > 1 else ''
        return format(ifijc__hqxup, whj__yfegr)
    if gzzaa__kfw in (('init_binary_str_index',
        'bodo.hiframes.pd_index_ext'), ('init_numeric_index',
        'bodo.hiframes.pd_index_ext'), ('init_categorical_index',
        'bodo.hiframes.pd_index_ext'), ('init_datetime_index',
        'bodo.hiframes.pd_index_ext'), ('init_timedelta_index',
        'bodo.hiframes.pd_index_ext'), ('init_heter_index',
        'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, zsmlc__dqj.args[0],
            arg_types, typemap, updated_containers))
    if gzzaa__kfw == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, zsmlc__dqj.args[0],
            arg_types, typemap, updated_containers))
    if gzzaa__kfw == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, zsmlc__dqj.args
            [0], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, zsmlc__dqj.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            zsmlc__dqj.args[2], arg_types, typemap, updated_containers))
    if gzzaa__kfw == ('len', 'builtins') and typemap and isinstance(typemap
        .get(zsmlc__dqj.args[0].name, None), types.BaseTuple):
        return len(typemap[zsmlc__dqj.args[0].name])
    if gzzaa__kfw == ('len', 'builtins'):
        joji__surh = guard(get_definition, func_ir, zsmlc__dqj.args[0])
        if isinstance(joji__surh, ir.Expr) and joji__surh.op in ('build_tuple',
            'build_list', 'build_set', 'build_map'):
            return len(joji__surh.items)
        return len(get_const_value_inner(func_ir, zsmlc__dqj.args[0],
            arg_types, typemap, updated_containers))
    if gzzaa__kfw == ('CategoricalDtype', 'pandas'):
        kws = dict(zsmlc__dqj.kws)
        est__grwg = get_call_expr_arg('CategoricalDtype', zsmlc__dqj.args,
            kws, 0, 'categories', '')
        ugago__gxgkn = get_call_expr_arg('CategoricalDtype', zsmlc__dqj.
            args, kws, 1, 'ordered', False)
        if ugago__gxgkn is not False:
            ugago__gxgkn = get_const_value_inner(func_ir, ugago__gxgkn,
                arg_types, typemap, updated_containers)
        if est__grwg == '':
            est__grwg = None
        else:
            est__grwg = get_const_value_inner(func_ir, est__grwg, arg_types,
                typemap, updated_containers)
        return pd.CategoricalDtype(est__grwg, ugago__gxgkn)
    if gzzaa__kfw == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, zsmlc__dqj.args[0],
            arg_types, typemap, updated_containers))
    if gzzaa__kfw is not None and gzzaa__kfw[1] == 'numpy' and gzzaa__kfw[0
        ] in _np_type_names:
        return getattr(np, gzzaa__kfw[0])(get_const_value_inner(func_ir,
            zsmlc__dqj.args[0], arg_types, typemap, updated_containers))
    if gzzaa__kfw is not None and len(gzzaa__kfw) == 2 and gzzaa__kfw[1
        ] == 'pandas' and gzzaa__kfw[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, gzzaa__kfw[0])()
    if gzzaa__kfw is not None and len(gzzaa__kfw) == 2 and isinstance(
        gzzaa__kfw[1], ir.Var):
        mfub__lwvbl = get_const_value_inner(func_ir, gzzaa__kfw[1],
            arg_types, typemap, updated_containers)
        args = [get_const_value_inner(func_ir, ksquq__wmu, arg_types,
            typemap, updated_containers) for ksquq__wmu in zsmlc__dqj.args]
        kws = {aoju__prqj[0]: get_const_value_inner(func_ir, aoju__prqj[1],
            arg_types, typemap, updated_containers) for aoju__prqj in
            zsmlc__dqj.kws}
        return getattr(mfub__lwvbl, gzzaa__kfw[0])(*args, **kws)
    if gzzaa__kfw is not None and len(gzzaa__kfw) == 2 and gzzaa__kfw[1
        ] == 'bodo' and gzzaa__kfw[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, ksquq__wmu, arg_types,
            typemap, updated_containers) for ksquq__wmu in zsmlc__dqj.args)
        kwargs = {vilyi__erus: get_const_value_inner(func_ir, ksquq__wmu,
            arg_types, typemap, updated_containers) for vilyi__erus,
            ksquq__wmu in dict(zsmlc__dqj.kws).items()}
        return getattr(bodo, gzzaa__kfw[0])(*args, **kwargs)
    if is_call(zsmlc__dqj) and typemap and isinstance(typemap.get(
        zsmlc__dqj.func.name, None), types.Dispatcher):
        py_func = typemap[zsmlc__dqj.func.name].dispatcher.py_func
        require(zsmlc__dqj.vararg is None)
        args = tuple(get_const_value_inner(func_ir, ksquq__wmu, arg_types,
            typemap, updated_containers) for ksquq__wmu in zsmlc__dqj.args)
        kwargs = {vilyi__erus: get_const_value_inner(func_ir, ksquq__wmu,
            arg_types, typemap, updated_containers) for vilyi__erus,
            ksquq__wmu in dict(zsmlc__dqj.kws).items()}
        arg_types = tuple(bodo.typeof(ksquq__wmu) for ksquq__wmu in args)
        kw_types = {drzc__ftk: bodo.typeof(ksquq__wmu) for drzc__ftk,
            ksquq__wmu in kwargs.items()}
        require(_func_is_pure(py_func, arg_types, kw_types))
        return py_func(*args, **kwargs)
    raise GuardException('Constant value not found')


def _func_is_pure(py_func, arg_types, kw_types):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.ir.csv_ext import CsvReader
    from bodo.ir.json_ext import JsonReader
    from bodo.ir.parquet_ext import ParquetReader
    from bodo.ir.sql_ext import SqlReader
    f_ir, typemap, qvmce__tsqzo, qvmce__tsqzo = (bodo.compiler.
        get_func_type_info(py_func, arg_types, kw_types))
    for block in f_ir.blocks.values():
        for stmt in block.body:
            if isinstance(stmt, ir.Print):
                return False
            if isinstance(stmt, (CsvReader, JsonReader, ParquetReader,
                SqlReader)):
                return False
            if is_setitem(stmt) and isinstance(guard(get_definition, f_ir,
                stmt.target), ir.Arg):
                return False
            if is_assign(stmt):
                rhs = stmt.value
                if isinstance(rhs, ir.Yield):
                    return False
                if is_call(rhs):
                    iimsd__vdmn = guard(get_definition, f_ir, rhs.func)
                    if isinstance(iimsd__vdmn, ir.Const) and isinstance(
                        iimsd__vdmn.value, numba.core.dispatcher.
                        ObjModeLiftedWith):
                        return False
                    knfwf__jfspf = guard(find_callname, f_ir, rhs)
                    if knfwf__jfspf is None:
                        return False
                    func_name, agkve__ntfq = knfwf__jfspf
                    if agkve__ntfq == 'pandas' and func_name.startswith('read_'
                        ):
                        return False
                    if knfwf__jfspf in (('fromfile', 'numpy'), ('file_read',
                        'bodo.io.np_io')):
                        return False
                    if knfwf__jfspf == ('File', 'h5py'):
                        return False
                    if isinstance(agkve__ntfq, ir.Var):
                        mqr__txr = typemap[agkve__ntfq.name]
                        if isinstance(mqr__txr, (DataFrameType, SeriesType)
                            ) and func_name in ('to_csv', 'to_excel',
                            'to_json', 'to_sql', 'to_pickle', 'to_parquet',
                            'info'):
                            return False
                        if isinstance(mqr__txr, types.Array
                            ) and func_name == 'tofile':
                            return False
                        if isinstance(mqr__txr, bodo.LoggingLoggerType):
                            return False
                        if str(mqr__txr).startswith('Mpl'):
                            return False
                        if (func_name in container_update_method_names and
                            isinstance(guard(get_definition, f_ir,
                            agkve__ntfq), ir.Arg)):
                            return False
                    if agkve__ntfq in ('numpy.random', 'time', 'logging',
                        'matplotlib.pyplot'):
                        return False
    return True


def fold_argument_types(pysig, args, kws):

    def normal_handler(index, param, value):
        return value

    def default_handler(index, param, default):
        return types.Omitted(default)

    def stararg_handler(index, param, values):
        return types.StarArgTuple(values)
    args = fold_arguments(pysig, args, kws, normal_handler, default_handler,
        stararg_handler)
    return args


def get_const_func_output_type(func, arg_types, kw_types, typing_context,
    target_context, is_udf=True):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
    py_func = None
    if isinstance(func, types.MakeFunctionLiteral):
        fmiv__tsvs = func.literal_value.code
        itra__xldqb = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            itra__xldqb = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(itra__xldqb, fmiv__tsvs)
        fix_struct_return(f_ir)
        typemap, yak__fxkzn, ulpe__eerxw, qvmce__tsqzo = (numba.core.
            typed_passes.type_inference_stage(typing_context,
            target_context, f_ir, arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, ulpe__eerxw, yak__fxkzn = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, ulpe__eerxw, yak__fxkzn = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, ulpe__eerxw, yak__fxkzn = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    if is_udf and isinstance(yak__fxkzn, types.DictType):
        vahp__gsvtd = guard(get_struct_keynames, f_ir, typemap)
        if vahp__gsvtd is not None:
            yak__fxkzn = StructType((yak__fxkzn.value_type,) * len(
                vahp__gsvtd), vahp__gsvtd)
    if is_udf and isinstance(yak__fxkzn, (SeriesType, HeterogeneousSeriesType)
        ):
        npuwq__fvnz = numba.core.registry.cpu_target.typing_context
        hexc__acls = numba.core.registry.cpu_target.target_context
        xkele__udyy = bodo.transforms.series_pass.SeriesPass(f_ir,
            npuwq__fvnz, hexc__acls, typemap, ulpe__eerxw, {})
        xkele__udyy.run()
        xkele__udyy.run()
        xkele__udyy.run()
        bqvgo__xwk = compute_cfg_from_blocks(f_ir.blocks)
        mvfuz__ppt = [guard(_get_const_series_info, f_ir.blocks[rnz__zmuts],
            f_ir, typemap) for rnz__zmuts in bqvgo__xwk.exit_points() if
            isinstance(f_ir.blocks[rnz__zmuts].body[-1], ir.Return)]
        if None in mvfuz__ppt or len(pd.Series(mvfuz__ppt).unique()) != 1:
            yak__fxkzn.const_info = None
        else:
            yak__fxkzn.const_info = mvfuz__ppt[0]
    return yak__fxkzn


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    qmlhr__lmxe = block.body[-1].value
    owm__vwtdf = get_definition(f_ir, qmlhr__lmxe)
    require(is_expr(owm__vwtdf, 'cast'))
    owm__vwtdf = get_definition(f_ir, owm__vwtdf.value)
    require(is_call(owm__vwtdf) and find_callname(f_ir, owm__vwtdf) == (
        'init_series', 'bodo.hiframes.pd_series_ext'))
    gwdn__mzzw = owm__vwtdf.args[1]
    gad__qjtx = tuple(get_const_value_inner(f_ir, gwdn__mzzw, typemap=typemap))
    if isinstance(typemap[qmlhr__lmxe.name], HeterogeneousSeriesType):
        return len(typemap[qmlhr__lmxe.name].data), gad__qjtx
    ewjx__ual = owm__vwtdf.args[0]
    qap__rfyx = get_definition(f_ir, ewjx__ual)
    func_name, rgtj__vlq = find_callname(f_ir, qap__rfyx)
    if is_call(qap__rfyx) and bodo.utils.utils.is_alloc_callname(func_name,
        rgtj__vlq):
        muysc__ccy = qap__rfyx.args[0]
        tskr__mieh = get_const_value_inner(f_ir, muysc__ccy, typemap=typemap)
        return tskr__mieh, gad__qjtx
    if is_call(qap__rfyx) and find_callname(f_ir, qap__rfyx) in [('asarray',
        'numpy'), ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'), (
        'build_nullable_tuple', 'bodo.libs.nullable_tuple_ext')]:
        ewjx__ual = qap__rfyx.args[0]
        qap__rfyx = get_definition(f_ir, ewjx__ual)
    require(is_expr(qap__rfyx, 'build_tuple') or is_expr(qap__rfyx,
        'build_list'))
    return len(qap__rfyx.items), gad__qjtx


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    mqpl__hfkoj = []
    cums__oihz = []
    values = []
    for drzc__ftk, ksquq__wmu in build_map.items:
        vwq__ffh = find_const(f_ir, drzc__ftk)
        require(isinstance(vwq__ffh, str))
        cums__oihz.append(vwq__ffh)
        mqpl__hfkoj.append(drzc__ftk)
        values.append(ksquq__wmu)
    zgigh__tqxad = ir.Var(scope, mk_unique_var('val_tup'), loc)
    qxfv__vccuo = ir.Assign(ir.Expr.build_tuple(values, loc), zgigh__tqxad, loc
        )
    f_ir._definitions[zgigh__tqxad.name] = [qxfv__vccuo.value]
    nxp__yyaa = ir.Var(scope, mk_unique_var('key_tup'), loc)
    hxmy__zwvbq = ir.Assign(ir.Expr.build_tuple(mqpl__hfkoj, loc),
        nxp__yyaa, loc)
    f_ir._definitions[nxp__yyaa.name] = [hxmy__zwvbq.value]
    if typemap is not None:
        typemap[zgigh__tqxad.name] = types.Tuple([typemap[ksquq__wmu.name] for
            ksquq__wmu in values])
        typemap[nxp__yyaa.name] = types.Tuple([typemap[ksquq__wmu.name] for
            ksquq__wmu in mqpl__hfkoj])
    return cums__oihz, zgigh__tqxad, qxfv__vccuo, nxp__yyaa, hxmy__zwvbq


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    wxfza__rmlv = block.body[-1].value
    zjcmf__iqw = guard(get_definition, f_ir, wxfza__rmlv)
    require(is_expr(zjcmf__iqw, 'cast'))
    owm__vwtdf = guard(get_definition, f_ir, zjcmf__iqw.value)
    require(is_expr(owm__vwtdf, 'build_map'))
    require(len(owm__vwtdf.items) > 0)
    loc = block.loc
    scope = block.scope
    cums__oihz, zgigh__tqxad, qxfv__vccuo, nxp__yyaa, hxmy__zwvbq = (
        extract_keyvals_from_struct_map(f_ir, owm__vwtdf, loc, scope))
    kepk__aagtx = ir.Var(scope, mk_unique_var('conv_call'), loc)
    jde__zgzho = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), kepk__aagtx, loc)
    f_ir._definitions[kepk__aagtx.name] = [jde__zgzho.value]
    eqsn__zeh = ir.Var(scope, mk_unique_var('struct_val'), loc)
    xkqnh__nuee = ir.Assign(ir.Expr.call(kepk__aagtx, [zgigh__tqxad,
        nxp__yyaa], {}, loc), eqsn__zeh, loc)
    f_ir._definitions[eqsn__zeh.name] = [xkqnh__nuee.value]
    zjcmf__iqw.value = eqsn__zeh
    owm__vwtdf.items = [(drzc__ftk, drzc__ftk) for drzc__ftk, qvmce__tsqzo in
        owm__vwtdf.items]
    block.body = block.body[:-2] + [qxfv__vccuo, hxmy__zwvbq, jde__zgzho,
        xkqnh__nuee] + block.body[-2:]
    return tuple(cums__oihz)


def get_struct_keynames(f_ir, typemap):
    bqvgo__xwk = compute_cfg_from_blocks(f_ir.blocks)
    dov__ayug = list(bqvgo__xwk.exit_points())[0]
    block = f_ir.blocks[dov__ayug]
    require(isinstance(block.body[-1], ir.Return))
    wxfza__rmlv = block.body[-1].value
    zjcmf__iqw = guard(get_definition, f_ir, wxfza__rmlv)
    require(is_expr(zjcmf__iqw, 'cast'))
    owm__vwtdf = guard(get_definition, f_ir, zjcmf__iqw.value)
    require(is_call(owm__vwtdf) and find_callname(f_ir, owm__vwtdf) == (
        'struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[owm__vwtdf.args[1].name])


def fix_struct_return(f_ir):
    rvdps__tuq = None
    bqvgo__xwk = compute_cfg_from_blocks(f_ir.blocks)
    for dov__ayug in bqvgo__xwk.exit_points():
        rvdps__tuq = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            dov__ayug], dov__ayug)
    return rvdps__tuq


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    gcn__wbj = ir.Block(ir.Scope(None, loc), loc)
    gcn__wbj.body = node_list
    build_definitions({(0): gcn__wbj}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(ksquq__wmu) for ksquq__wmu in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    metrl__bcrem = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(metrl__bcrem, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for alec__yqh in range(len(vals) - 1, -1, -1):
        ksquq__wmu = vals[alec__yqh]
        if isinstance(ksquq__wmu, str) and ksquq__wmu.startswith(
            NESTED_TUP_SENTINEL):
            aqek__guly = int(ksquq__wmu[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:alec__yqh]) + (
                tuple(vals[alec__yqh + 1:alec__yqh + aqek__guly + 1]),) +
                tuple(vals[alec__yqh + aqek__guly + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    ifijc__hqxup = None
    if len(args) > arg_no and arg_no >= 0:
        ifijc__hqxup = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        ifijc__hqxup = kws[arg_name]
    if ifijc__hqxup is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return ifijc__hqxup


def set_call_expr_arg(var, args, kws, arg_no, arg_name, add_if_missing=False):
    if len(args) > arg_no:
        args[arg_no] = var
    elif add_if_missing or arg_name in kws:
        kws[arg_name] = var
    else:
        raise BodoError('cannot set call argument since does not exist')


def avoid_udf_inline(py_func, arg_types, kw_types):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    f_ir = numba.core.compiler.run_frontend(py_func, inline_closures=True)
    if '_bodo_inline' in kw_types and is_overload_constant_bool(kw_types[
        '_bodo_inline']):
        return not get_overload_const_bool(kw_types['_bodo_inline'])
    if any(isinstance(t, DataFrameType) for t in arg_types + tuple(kw_types
        .values())):
        return True
    for block in f_ir.blocks.values():
        if isinstance(block.body[-1], (ir.Raise, ir.StaticRaise)):
            return True
        for stmt in block.body:
            if isinstance(stmt, ir.EnterWith):
                return True
    return False


def replace_func(pass_info, func, args, const=False, pre_nodes=None,
    extra_globals=None, pysig=None, kws=None, inline_bodo_calls=False,
    run_full_pipeline=False):
    nlpk__pok = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        nlpk__pok.update(extra_globals)
    func.__globals__.update(nlpk__pok)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            xmdp__skdqe = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[xmdp__skdqe.name] = types.literal(default)
            except:
                pass_info.typemap[xmdp__skdqe.name] = numba.typeof(default)
            dqx__pbjw = ir.Assign(ir.Const(default, loc), xmdp__skdqe, loc)
            pre_nodes.append(dqx__pbjw)
            return xmdp__skdqe
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    asv__vhg = tuple(pass_info.typemap[ksquq__wmu.name] for ksquq__wmu in args)
    if const:
        rmvuw__hau = []
        for alec__yqh, ifijc__hqxup in enumerate(args):
            mfub__lwvbl = guard(find_const, pass_info.func_ir, ifijc__hqxup)
            if mfub__lwvbl:
                rmvuw__hau.append(types.literal(mfub__lwvbl))
            else:
                rmvuw__hau.append(asv__vhg[alec__yqh])
        asv__vhg = tuple(rmvuw__hau)
    return ReplaceFunc(func, asv__vhg, args, nlpk__pok, inline_bodo_calls,
        run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(qvvyn__nhyqs) for qvvyn__nhyqs in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        cxygw__neax = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {cxygw__neax} = 0\n', (cxygw__neax,)
    if isinstance(t, ArrayItemArrayType):
        hlim__jfn, frrj__dxxuh = gen_init_varsize_alloc_sizes(t.dtype)
        cxygw__neax = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {cxygw__neax} = 0\n' + hlim__jfn, (cxygw__neax,
            ) + frrj__dxxuh
    return '', ()


def gen_varsize_item_sizes(t, item, var_names):
    if t == string_array_type:
        return '    {} += bodo.libs.str_arr_ext.get_utf8_size({})\n'.format(
            var_names[0], item)
    if isinstance(t, ArrayItemArrayType):
        return '    {} += len({})\n'.format(var_names[0], item
            ) + gen_varsize_array_counts(t.dtype, item, var_names[1:])
    return ''


def gen_varsize_array_counts(t, item, var_names):
    if t == string_array_type:
        return ('    {} += bodo.libs.str_arr_ext.get_num_total_chars({})\n'
            .format(var_names[0], item))
    return ''


def get_type_alloc_counts(t):
    if isinstance(t, (StructArrayType, TupleArrayType)):
        return 1 + sum(get_type_alloc_counts(qvvyn__nhyqs.dtype) for
            qvvyn__nhyqs in t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(qvvyn__nhyqs) for qvvyn__nhyqs in
            t.data)
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(qvvyn__nhyqs) for qvvyn__nhyqs in
            t.types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    crrn__rwhk = typing_context.resolve_getattr(obj_dtype, func_name)
    if crrn__rwhk is None:
        betm__agzo = types.misc.Module(np)
        try:
            crrn__rwhk = typing_context.resolve_getattr(betm__agzo, func_name)
        except AttributeError as sbhp__qvl:
            crrn__rwhk = None
        if crrn__rwhk is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return crrn__rwhk


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    crrn__rwhk = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(crrn__rwhk, types.BoundFunction):
        if axis is not None:
            jeqak__szfn = crrn__rwhk.get_call_type(typing_context, (), {
                'axis': axis})
        else:
            jeqak__szfn = crrn__rwhk.get_call_type(typing_context, (), {})
        return jeqak__szfn.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(crrn__rwhk):
            jeqak__szfn = crrn__rwhk.get_call_type(typing_context, (
                obj_dtype,), {})
            return jeqak__szfn.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    crrn__rwhk = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(crrn__rwhk, types.BoundFunction):
        wjlc__vxaum = crrn__rwhk.template
        if axis is not None:
            return wjlc__vxaum._overload_func(obj_dtype, axis=axis)
        else:
            return wjlc__vxaum._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    argj__uof = get_definition(func_ir, dict_var)
    require(isinstance(argj__uof, ir.Expr))
    require(argj__uof.op == 'build_map')
    sqw__qxmtt = argj__uof.items
    mqpl__hfkoj = []
    values = []
    wwtsd__llaw = False
    for alec__yqh in range(len(sqw__qxmtt)):
        xqqwc__mvpw, value = sqw__qxmtt[alec__yqh]
        try:
            uzky__nydfk = get_const_value_inner(func_ir, xqqwc__mvpw,
                arg_types, typemap, updated_containers)
            mqpl__hfkoj.append(uzky__nydfk)
            values.append(value)
        except GuardException as sbhp__qvl:
            require_const_map[xqqwc__mvpw] = label
            wwtsd__llaw = True
    if wwtsd__llaw:
        raise GuardException
    return mqpl__hfkoj, values


def _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc):
    try:
        mqpl__hfkoj = tuple(get_const_value_inner(func_ir, t[0], args) for
            t in build_map.items)
    except GuardException as sbhp__qvl:
        raise BodoError(err_msg, loc)
    if not all(isinstance(c, (str, int)) for c in mqpl__hfkoj):
        raise BodoError(err_msg, loc)
    return mqpl__hfkoj


def _convert_const_key_dict(args, func_ir, build_map, err_msg, scope, loc,
    output_sentinel_tuple=False):
    mqpl__hfkoj = _get_const_keys_from_dict(args, func_ir, build_map,
        err_msg, loc)
    zgfpl__enpn = []
    kyi__jxagk = [bodo.transforms.typing_pass._create_const_var(drzc__ftk,
        'dict_key', scope, loc, zgfpl__enpn) for drzc__ftk in mqpl__hfkoj]
    uvhpe__eguqf = [t[1] for t in build_map.items]
    if output_sentinel_tuple:
        xzrxu__vjx = ir.Var(scope, mk_unique_var('sentinel'), loc)
        ggy__ftz = ir.Var(scope, mk_unique_var('dict_tup'), loc)
        zgfpl__enpn.append(ir.Assign(ir.Const('__bodo_tup', loc),
            xzrxu__vjx, loc))
        fday__mkumr = [xzrxu__vjx] + kyi__jxagk + uvhpe__eguqf
        zgfpl__enpn.append(ir.Assign(ir.Expr.build_tuple(fday__mkumr, loc),
            ggy__ftz, loc))
        return (ggy__ftz,), zgfpl__enpn
    else:
        eohxf__mzglz = ir.Var(scope, mk_unique_var('values_tup'), loc)
        iift__fsfik = ir.Var(scope, mk_unique_var('idx_tup'), loc)
        zgfpl__enpn.append(ir.Assign(ir.Expr.build_tuple(uvhpe__eguqf, loc),
            eohxf__mzglz, loc))
        zgfpl__enpn.append(ir.Assign(ir.Expr.build_tuple(kyi__jxagk, loc),
            iift__fsfik, loc))
        return (eohxf__mzglz, iift__fsfik), zgfpl__enpn
