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
    wdy__yyok = tuple(call_list)
    if wdy__yyok in no_side_effect_call_tuples:
        return True
    if wdy__yyok == (bodo.hiframes.pd_index_ext.init_range_index,):
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
    if len(wdy__yyok) == 1 and tuple in getattr(wdy__yyok[0], '__mro__', ()):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=False, add_default_globals=True):
    if replace_globals:
        cmkq__hekwz = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd,
            'math': math}
    else:
        cmkq__hekwz = func.__globals__
    if extra_globals is not None:
        cmkq__hekwz.update(extra_globals)
    if add_default_globals:
        cmkq__hekwz.update({'numba': numba, 'np': np, 'bodo': bodo, 'pd':
            pd, 'math': math})
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, cmkq__hekwz, typingctx=typing_info
            .typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[dcma__vbvz.name] for dcma__vbvz in args),
            typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, cmkq__hekwz)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        tdk__efd = tuple(typing_info.typemap[dcma__vbvz.name] for
            dcma__vbvz in args)
        oel__tdy = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, tdk__efd, {}, {}, flags)
        oel__tdy.run()
    rve__boan = f_ir.blocks.popitem()[1]
    replace_arg_nodes(rve__boan, args)
    eyze__zmj = rve__boan.body[:-2]
    update_locs(eyze__zmj[len(args):], loc)
    for stmt in eyze__zmj[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        gbmnp__ztw = rve__boan.body[-2]
        assert is_assign(gbmnp__ztw) and is_expr(gbmnp__ztw.value, 'cast')
        ehlwg__pmsxg = gbmnp__ztw.value.value
        eyze__zmj.append(ir.Assign(ehlwg__pmsxg, ret_var, loc))
    return eyze__zmj


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for axzsi__bcuem in stmt.list_vars():
            axzsi__bcuem.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        qiohr__enncn = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        olgzw__nvx, wariq__uito = qiohr__enncn(stmt)
        return wariq__uito
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        nzosn__tzel = get_const_value_inner(func_ir, var, arg_types,
            typemap, file_info=file_info)
        if isinstance(nzosn__tzel, ir.UndefinedType):
            sjraa__xkol = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{sjraa__xkol}' is not defined", loc=loc)
    except GuardException as xkyyd__yqdjl:
        raise BodoError(err_msg, loc=loc)
    return nzosn__tzel


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False,
    literalize_args=True):
    require(isinstance(var, ir.Var))
    oxkd__jbu = get_definition(func_ir, var)
    xkw__wgzjk = None
    if typemap is not None:
        xkw__wgzjk = typemap.get(var.name, None)
    if isinstance(oxkd__jbu, ir.Arg) and arg_types is not None:
        xkw__wgzjk = arg_types[oxkd__jbu.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(xkw__wgzjk):
        return get_literal_value(xkw__wgzjk)
    if isinstance(oxkd__jbu, (ir.Const, ir.Global, ir.FreeVar)):
        nzosn__tzel = oxkd__jbu.value
        return nzosn__tzel
    if literalize_args and isinstance(oxkd__jbu, ir.Arg
        ) and can_literalize_type(xkw__wgzjk, pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({oxkd__jbu.index}, loc=var.
            loc, file_infos={oxkd__jbu.index: file_info} if file_info is not
            None else None)
    if is_expr(oxkd__jbu, 'binop'):
        if file_info and oxkd__jbu.fn == operator.add:
            try:
                aclrb__zyl = get_const_value_inner(func_ir, oxkd__jbu.lhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(aclrb__zyl, True)
                tohj__qet = get_const_value_inner(func_ir, oxkd__jbu.rhs,
                    arg_types, typemap, updated_containers, file_info)
                return oxkd__jbu.fn(aclrb__zyl, tohj__qet)
            except (GuardException, BodoConstUpdatedError) as xkyyd__yqdjl:
                pass
            try:
                tohj__qet = get_const_value_inner(func_ir, oxkd__jbu.rhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(tohj__qet, False)
                aclrb__zyl = get_const_value_inner(func_ir, oxkd__jbu.lhs,
                    arg_types, typemap, updated_containers, file_info)
                return oxkd__jbu.fn(aclrb__zyl, tohj__qet)
            except (GuardException, BodoConstUpdatedError) as xkyyd__yqdjl:
                pass
        aclrb__zyl = get_const_value_inner(func_ir, oxkd__jbu.lhs,
            arg_types, typemap, updated_containers)
        tohj__qet = get_const_value_inner(func_ir, oxkd__jbu.rhs, arg_types,
            typemap, updated_containers)
        return oxkd__jbu.fn(aclrb__zyl, tohj__qet)
    if is_expr(oxkd__jbu, 'unary'):
        nzosn__tzel = get_const_value_inner(func_ir, oxkd__jbu.value,
            arg_types, typemap, updated_containers)
        return oxkd__jbu.fn(nzosn__tzel)
    if is_expr(oxkd__jbu, 'getattr') and typemap:
        poat__jku = typemap.get(oxkd__jbu.value.name, None)
        if isinstance(poat__jku, bodo.hiframes.pd_dataframe_ext.DataFrameType
            ) and oxkd__jbu.attr == 'columns':
            return pd.Index(poat__jku.columns)
        if isinstance(poat__jku, types.SliceType):
            cehxm__ugon = get_definition(func_ir, oxkd__jbu.value)
            require(is_call(cehxm__ugon))
            waa__wzcvu = find_callname(func_ir, cehxm__ugon)
            andu__syunq = False
            if waa__wzcvu == ('_normalize_slice', 'numba.cpython.unicode'):
                require(oxkd__jbu.attr in ('start', 'step'))
                cehxm__ugon = get_definition(func_ir, cehxm__ugon.args[0])
                andu__syunq = True
            require(find_callname(func_ir, cehxm__ugon) == ('slice',
                'builtins'))
            if len(cehxm__ugon.args) == 1:
                if oxkd__jbu.attr == 'start':
                    return 0
                if oxkd__jbu.attr == 'step':
                    return 1
                require(oxkd__jbu.attr == 'stop')
                return get_const_value_inner(func_ir, cehxm__ugon.args[0],
                    arg_types, typemap, updated_containers)
            if oxkd__jbu.attr == 'start':
                nzosn__tzel = get_const_value_inner(func_ir, cehxm__ugon.
                    args[0], arg_types, typemap, updated_containers)
                if nzosn__tzel is None:
                    nzosn__tzel = 0
                if andu__syunq:
                    require(nzosn__tzel == 0)
                return nzosn__tzel
            if oxkd__jbu.attr == 'stop':
                assert not andu__syunq
                return get_const_value_inner(func_ir, cehxm__ugon.args[1],
                    arg_types, typemap, updated_containers)
            require(oxkd__jbu.attr == 'step')
            if len(cehxm__ugon.args) == 2:
                return 1
            else:
                nzosn__tzel = get_const_value_inner(func_ir, cehxm__ugon.
                    args[2], arg_types, typemap, updated_containers)
                if nzosn__tzel is None:
                    nzosn__tzel = 1
                if andu__syunq:
                    require(nzosn__tzel == 1)
                return nzosn__tzel
    if is_expr(oxkd__jbu, 'getattr'):
        return getattr(get_const_value_inner(func_ir, oxkd__jbu.value,
            arg_types, typemap, updated_containers), oxkd__jbu.attr)
    if is_expr(oxkd__jbu, 'getitem'):
        value = get_const_value_inner(func_ir, oxkd__jbu.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, oxkd__jbu.index, arg_types,
            typemap, updated_containers)
        return value[index]
    usvzt__aqof = guard(find_callname, func_ir, oxkd__jbu, typemap)
    if usvzt__aqof is not None and len(usvzt__aqof) == 2 and usvzt__aqof[0
        ] == 'keys' and isinstance(usvzt__aqof[1], ir.Var):
        dhi__xinvv = oxkd__jbu.func
        oxkd__jbu = get_definition(func_ir, usvzt__aqof[1])
        suvlz__vxyef = usvzt__aqof[1].name
        if updated_containers and suvlz__vxyef in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                suvlz__vxyef, updated_containers[suvlz__vxyef]))
        require(is_expr(oxkd__jbu, 'build_map'))
        vals = [axzsi__bcuem[0] for axzsi__bcuem in oxkd__jbu.items]
        cilw__jygmt = guard(get_definition, func_ir, dhi__xinvv)
        assert isinstance(cilw__jygmt, ir.Expr) and cilw__jygmt.attr == 'keys'
        cilw__jygmt.attr = 'copy'
        return [get_const_value_inner(func_ir, axzsi__bcuem, arg_types,
            typemap, updated_containers) for axzsi__bcuem in vals]
    if is_expr(oxkd__jbu, 'build_map'):
        return {get_const_value_inner(func_ir, axzsi__bcuem[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            axzsi__bcuem[1], arg_types, typemap, updated_containers) for
            axzsi__bcuem in oxkd__jbu.items}
    if is_expr(oxkd__jbu, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, axzsi__bcuem, arg_types,
            typemap, updated_containers) for axzsi__bcuem in oxkd__jbu.items)
    if is_expr(oxkd__jbu, 'build_list'):
        return [get_const_value_inner(func_ir, axzsi__bcuem, arg_types,
            typemap, updated_containers) for axzsi__bcuem in oxkd__jbu.items]
    if is_expr(oxkd__jbu, 'build_set'):
        return {get_const_value_inner(func_ir, axzsi__bcuem, arg_types,
            typemap, updated_containers) for axzsi__bcuem in oxkd__jbu.items}
    if usvzt__aqof == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, oxkd__jbu.args[0],
            arg_types, typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if usvzt__aqof == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, oxkd__jbu.args[0],
            arg_types, typemap, updated_containers))
    if usvzt__aqof == ('range', 'builtins') and len(oxkd__jbu.args) == 1:
        return range(get_const_value_inner(func_ir, oxkd__jbu.args[0],
            arg_types, typemap, updated_containers))
    if usvzt__aqof == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, axzsi__bcuem,
            arg_types, typemap, updated_containers) for axzsi__bcuem in
            oxkd__jbu.args))
    if usvzt__aqof == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, oxkd__jbu.args[0],
            arg_types, typemap, updated_containers))
    if usvzt__aqof == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, oxkd__jbu.args[0],
            arg_types, typemap, updated_containers))
    if usvzt__aqof == ('format', 'builtins'):
        dcma__vbvz = get_const_value_inner(func_ir, oxkd__jbu.args[0],
            arg_types, typemap, updated_containers)
        atq__dfv = get_const_value_inner(func_ir, oxkd__jbu.args[1],
            arg_types, typemap, updated_containers) if len(oxkd__jbu.args
            ) > 1 else ''
        return format(dcma__vbvz, atq__dfv)
    if usvzt__aqof in (('init_binary_str_index',
        'bodo.hiframes.pd_index_ext'), ('init_numeric_index',
        'bodo.hiframes.pd_index_ext'), ('init_categorical_index',
        'bodo.hiframes.pd_index_ext'), ('init_datetime_index',
        'bodo.hiframes.pd_index_ext'), ('init_timedelta_index',
        'bodo.hiframes.pd_index_ext'), ('init_heter_index',
        'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, oxkd__jbu.args[0],
            arg_types, typemap, updated_containers))
    if usvzt__aqof == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, oxkd__jbu.args[0],
            arg_types, typemap, updated_containers))
    if usvzt__aqof == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, oxkd__jbu.args[
            0], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, oxkd__jbu.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            oxkd__jbu.args[2], arg_types, typemap, updated_containers))
    if usvzt__aqof == ('len', 'builtins') and typemap and isinstance(typemap
        .get(oxkd__jbu.args[0].name, None), types.BaseTuple):
        return len(typemap[oxkd__jbu.args[0].name])
    if usvzt__aqof == ('len', 'builtins'):
        ikgwl__irsjs = guard(get_definition, func_ir, oxkd__jbu.args[0])
        if isinstance(ikgwl__irsjs, ir.Expr) and ikgwl__irsjs.op in (
            'build_tuple', 'build_list', 'build_set', 'build_map'):
            return len(ikgwl__irsjs.items)
        return len(get_const_value_inner(func_ir, oxkd__jbu.args[0],
            arg_types, typemap, updated_containers))
    if usvzt__aqof == ('CategoricalDtype', 'pandas'):
        kws = dict(oxkd__jbu.kws)
        aajq__ztlws = get_call_expr_arg('CategoricalDtype', oxkd__jbu.args,
            kws, 0, 'categories', '')
        ilvo__dgfl = get_call_expr_arg('CategoricalDtype', oxkd__jbu.args,
            kws, 1, 'ordered', False)
        if ilvo__dgfl is not False:
            ilvo__dgfl = get_const_value_inner(func_ir, ilvo__dgfl,
                arg_types, typemap, updated_containers)
        if aajq__ztlws == '':
            aajq__ztlws = None
        else:
            aajq__ztlws = get_const_value_inner(func_ir, aajq__ztlws,
                arg_types, typemap, updated_containers)
        return pd.CategoricalDtype(aajq__ztlws, ilvo__dgfl)
    if usvzt__aqof == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, oxkd__jbu.args[0],
            arg_types, typemap, updated_containers))
    if usvzt__aqof is not None and usvzt__aqof[1] == 'numpy' and usvzt__aqof[0
        ] in _np_type_names:
        return getattr(np, usvzt__aqof[0])(get_const_value_inner(func_ir,
            oxkd__jbu.args[0], arg_types, typemap, updated_containers))
    if usvzt__aqof is not None and len(usvzt__aqof) == 2 and usvzt__aqof[1
        ] == 'pandas' and usvzt__aqof[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, usvzt__aqof[0])()
    if usvzt__aqof is not None and len(usvzt__aqof) == 2 and isinstance(
        usvzt__aqof[1], ir.Var):
        nzosn__tzel = get_const_value_inner(func_ir, usvzt__aqof[1],
            arg_types, typemap, updated_containers)
        args = [get_const_value_inner(func_ir, axzsi__bcuem, arg_types,
            typemap, updated_containers) for axzsi__bcuem in oxkd__jbu.args]
        kws = {kwv__pbqfk[0]: get_const_value_inner(func_ir, kwv__pbqfk[1],
            arg_types, typemap, updated_containers) for kwv__pbqfk in
            oxkd__jbu.kws}
        return getattr(nzosn__tzel, usvzt__aqof[0])(*args, **kws)
    if usvzt__aqof is not None and len(usvzt__aqof) == 2 and usvzt__aqof[1
        ] == 'bodo' and usvzt__aqof[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, axzsi__bcuem, arg_types,
            typemap, updated_containers) for axzsi__bcuem in oxkd__jbu.args)
        kwargs = {sjraa__xkol: get_const_value_inner(func_ir, axzsi__bcuem,
            arg_types, typemap, updated_containers) for sjraa__xkol,
            axzsi__bcuem in dict(oxkd__jbu.kws).items()}
        return getattr(bodo, usvzt__aqof[0])(*args, **kwargs)
    if is_call(oxkd__jbu) and typemap and isinstance(typemap.get(oxkd__jbu.
        func.name, None), types.Dispatcher):
        py_func = typemap[oxkd__jbu.func.name].dispatcher.py_func
        require(oxkd__jbu.vararg is None)
        args = tuple(get_const_value_inner(func_ir, axzsi__bcuem, arg_types,
            typemap, updated_containers) for axzsi__bcuem in oxkd__jbu.args)
        kwargs = {sjraa__xkol: get_const_value_inner(func_ir, axzsi__bcuem,
            arg_types, typemap, updated_containers) for sjraa__xkol,
            axzsi__bcuem in dict(oxkd__jbu.kws).items()}
        arg_types = tuple(bodo.typeof(axzsi__bcuem) for axzsi__bcuem in args)
        kw_types = {xdi__dvs: bodo.typeof(axzsi__bcuem) for xdi__dvs,
            axzsi__bcuem in kwargs.items()}
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
    f_ir, typemap, nxr__isyk, nxr__isyk = bodo.compiler.get_func_type_info(
        py_func, arg_types, kw_types)
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
                    vkxed__lpewb = guard(get_definition, f_ir, rhs.func)
                    if isinstance(vkxed__lpewb, ir.Const) and isinstance(
                        vkxed__lpewb.value, numba.core.dispatcher.
                        ObjModeLiftedWith):
                        return False
                    lmpu__rtsh = guard(find_callname, f_ir, rhs)
                    if lmpu__rtsh is None:
                        return False
                    func_name, gfhrb__pccu = lmpu__rtsh
                    if gfhrb__pccu == 'pandas' and func_name.startswith('read_'
                        ):
                        return False
                    if lmpu__rtsh in (('fromfile', 'numpy'), ('file_read',
                        'bodo.io.np_io')):
                        return False
                    if lmpu__rtsh == ('File', 'h5py'):
                        return False
                    if isinstance(gfhrb__pccu, ir.Var):
                        xkw__wgzjk = typemap[gfhrb__pccu.name]
                        if isinstance(xkw__wgzjk, (DataFrameType, SeriesType)
                            ) and func_name in ('to_csv', 'to_excel',
                            'to_json', 'to_sql', 'to_pickle', 'to_parquet',
                            'info'):
                            return False
                        if isinstance(xkw__wgzjk, types.Array
                            ) and func_name == 'tofile':
                            return False
                        if isinstance(xkw__wgzjk, bodo.LoggingLoggerType):
                            return False
                        if str(xkw__wgzjk).startswith('Mpl'):
                            return False
                        if (func_name in container_update_method_names and
                            isinstance(guard(get_definition, f_ir,
                            gfhrb__pccu), ir.Arg)):
                            return False
                    if gfhrb__pccu in ('numpy.random', 'time', 'logging',
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
        sffhh__bfwal = func.literal_value.code
        yrkxd__vlxz = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            yrkxd__vlxz = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(yrkxd__vlxz, sffhh__bfwal)
        fix_struct_return(f_ir)
        typemap, zurg__fwq, zogh__jokkm, nxr__isyk = (numba.core.
            typed_passes.type_inference_stage(typing_context,
            target_context, f_ir, arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, zogh__jokkm, zurg__fwq = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, zogh__jokkm, zurg__fwq = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, zogh__jokkm, zurg__fwq = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    if is_udf and isinstance(zurg__fwq, types.DictType):
        npip__tfnp = guard(get_struct_keynames, f_ir, typemap)
        if npip__tfnp is not None:
            zurg__fwq = StructType((zurg__fwq.value_type,) * len(npip__tfnp
                ), npip__tfnp)
    if is_udf and isinstance(zurg__fwq, (SeriesType, HeterogeneousSeriesType)):
        eqioo__ecd = numba.core.registry.cpu_target.typing_context
        noas__fnux = numba.core.registry.cpu_target.target_context
        yzi__zwo = bodo.transforms.series_pass.SeriesPass(f_ir, eqioo__ecd,
            noas__fnux, typemap, zogh__jokkm, {})
        yzi__zwo.run()
        yzi__zwo.run()
        yzi__zwo.run()
        ofex__sshuk = compute_cfg_from_blocks(f_ir.blocks)
        vfnaa__zixe = [guard(_get_const_series_info, f_ir.blocks[kgu__kqito
            ], f_ir, typemap) for kgu__kqito in ofex__sshuk.exit_points() if
            isinstance(f_ir.blocks[kgu__kqito].body[-1], ir.Return)]
        if None in vfnaa__zixe or len(pd.Series(vfnaa__zixe).unique()) != 1:
            zurg__fwq.const_info = None
        else:
            zurg__fwq.const_info = vfnaa__zixe[0]
    return zurg__fwq


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    jgkq__mct = block.body[-1].value
    cjmks__mdfms = get_definition(f_ir, jgkq__mct)
    require(is_expr(cjmks__mdfms, 'cast'))
    cjmks__mdfms = get_definition(f_ir, cjmks__mdfms.value)
    require(is_call(cjmks__mdfms) and find_callname(f_ir, cjmks__mdfms) ==
        ('init_series', 'bodo.hiframes.pd_series_ext'))
    ztunj__mzav = cjmks__mdfms.args[1]
    algfl__kboxh = tuple(get_const_value_inner(f_ir, ztunj__mzav, typemap=
        typemap))
    if isinstance(typemap[jgkq__mct.name], HeterogeneousSeriesType):
        return len(typemap[jgkq__mct.name].data), algfl__kboxh
    tesbw__vbqh = cjmks__mdfms.args[0]
    lhb__jheh = get_definition(f_ir, tesbw__vbqh)
    func_name, voyr__mmxmd = find_callname(f_ir, lhb__jheh)
    if is_call(lhb__jheh) and bodo.utils.utils.is_alloc_callname(func_name,
        voyr__mmxmd):
        sfhxo__mev = lhb__jheh.args[0]
        fcm__babt = get_const_value_inner(f_ir, sfhxo__mev, typemap=typemap)
        return fcm__babt, algfl__kboxh
    if is_call(lhb__jheh) and find_callname(f_ir, lhb__jheh) in [('asarray',
        'numpy'), ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'), (
        'build_nullable_tuple', 'bodo.libs.nullable_tuple_ext')]:
        tesbw__vbqh = lhb__jheh.args[0]
        lhb__jheh = get_definition(f_ir, tesbw__vbqh)
    require(is_expr(lhb__jheh, 'build_tuple') or is_expr(lhb__jheh,
        'build_list'))
    return len(lhb__jheh.items), algfl__kboxh


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    hyor__btan = []
    ywca__uwbla = []
    values = []
    for xdi__dvs, axzsi__bcuem in build_map.items:
        nzr__hffr = find_const(f_ir, xdi__dvs)
        require(isinstance(nzr__hffr, str))
        ywca__uwbla.append(nzr__hffr)
        hyor__btan.append(xdi__dvs)
        values.append(axzsi__bcuem)
    ixwqy__hpst = ir.Var(scope, mk_unique_var('val_tup'), loc)
    wkqby__befof = ir.Assign(ir.Expr.build_tuple(values, loc), ixwqy__hpst, loc
        )
    f_ir._definitions[ixwqy__hpst.name] = [wkqby__befof.value]
    wzchi__fgr = ir.Var(scope, mk_unique_var('key_tup'), loc)
    kzf__krihq = ir.Assign(ir.Expr.build_tuple(hyor__btan, loc), wzchi__fgr,
        loc)
    f_ir._definitions[wzchi__fgr.name] = [kzf__krihq.value]
    if typemap is not None:
        typemap[ixwqy__hpst.name] = types.Tuple([typemap[axzsi__bcuem.name] for
            axzsi__bcuem in values])
        typemap[wzchi__fgr.name] = types.Tuple([typemap[axzsi__bcuem.name] for
            axzsi__bcuem in hyor__btan])
    return ywca__uwbla, ixwqy__hpst, wkqby__befof, wzchi__fgr, kzf__krihq


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    iys__yyypb = block.body[-1].value
    sadam__fejy = guard(get_definition, f_ir, iys__yyypb)
    require(is_expr(sadam__fejy, 'cast'))
    cjmks__mdfms = guard(get_definition, f_ir, sadam__fejy.value)
    require(is_expr(cjmks__mdfms, 'build_map'))
    require(len(cjmks__mdfms.items) > 0)
    loc = block.loc
    scope = block.scope
    ywca__uwbla, ixwqy__hpst, wkqby__befof, wzchi__fgr, kzf__krihq = (
        extract_keyvals_from_struct_map(f_ir, cjmks__mdfms, loc, scope))
    scr__mhcbv = ir.Var(scope, mk_unique_var('conv_call'), loc)
    nkcr__kqcw = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), scr__mhcbv, loc)
    f_ir._definitions[scr__mhcbv.name] = [nkcr__kqcw.value]
    bua__ttnz = ir.Var(scope, mk_unique_var('struct_val'), loc)
    teed__cpj = ir.Assign(ir.Expr.call(scr__mhcbv, [ixwqy__hpst, wzchi__fgr
        ], {}, loc), bua__ttnz, loc)
    f_ir._definitions[bua__ttnz.name] = [teed__cpj.value]
    sadam__fejy.value = bua__ttnz
    cjmks__mdfms.items = [(xdi__dvs, xdi__dvs) for xdi__dvs, nxr__isyk in
        cjmks__mdfms.items]
    block.body = block.body[:-2] + [wkqby__befof, kzf__krihq, nkcr__kqcw,
        teed__cpj] + block.body[-2:]
    return tuple(ywca__uwbla)


def get_struct_keynames(f_ir, typemap):
    ofex__sshuk = compute_cfg_from_blocks(f_ir.blocks)
    byyil__ghg = list(ofex__sshuk.exit_points())[0]
    block = f_ir.blocks[byyil__ghg]
    require(isinstance(block.body[-1], ir.Return))
    iys__yyypb = block.body[-1].value
    sadam__fejy = guard(get_definition, f_ir, iys__yyypb)
    require(is_expr(sadam__fejy, 'cast'))
    cjmks__mdfms = guard(get_definition, f_ir, sadam__fejy.value)
    require(is_call(cjmks__mdfms) and find_callname(f_ir, cjmks__mdfms) ==
        ('struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[cjmks__mdfms.args[1].name])


def fix_struct_return(f_ir):
    txbpi__xzol = None
    ofex__sshuk = compute_cfg_from_blocks(f_ir.blocks)
    for byyil__ghg in ofex__sshuk.exit_points():
        txbpi__xzol = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            byyil__ghg], byyil__ghg)
    return txbpi__xzol


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    kdvo__pjr = ir.Block(ir.Scope(None, loc), loc)
    kdvo__pjr.body = node_list
    build_definitions({(0): kdvo__pjr}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(axzsi__bcuem) for axzsi__bcuem in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    jcw__rvzyf = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(jcw__rvzyf, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for kam__wtqgl in range(len(vals) - 1, -1, -1):
        axzsi__bcuem = vals[kam__wtqgl]
        if isinstance(axzsi__bcuem, str) and axzsi__bcuem.startswith(
            NESTED_TUP_SENTINEL):
            bbypw__rrtaw = int(axzsi__bcuem[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:kam__wtqgl]) + (
                tuple(vals[kam__wtqgl + 1:kam__wtqgl + bbypw__rrtaw + 1]),) +
                tuple(vals[kam__wtqgl + bbypw__rrtaw + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    dcma__vbvz = None
    if len(args) > arg_no and arg_no >= 0:
        dcma__vbvz = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        dcma__vbvz = kws[arg_name]
    if dcma__vbvz is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return dcma__vbvz


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
    cmkq__hekwz = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        cmkq__hekwz.update(extra_globals)
    func.__globals__.update(cmkq__hekwz)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            hsdzj__elgs = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[hsdzj__elgs.name] = types.literal(default)
            except:
                pass_info.typemap[hsdzj__elgs.name] = numba.typeof(default)
            oqgtq__ikr = ir.Assign(ir.Const(default, loc), hsdzj__elgs, loc)
            pre_nodes.append(oqgtq__ikr)
            return hsdzj__elgs
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    tdk__efd = tuple(pass_info.typemap[axzsi__bcuem.name] for axzsi__bcuem in
        args)
    if const:
        yulnb__poul = []
        for kam__wtqgl, dcma__vbvz in enumerate(args):
            nzosn__tzel = guard(find_const, pass_info.func_ir, dcma__vbvz)
            if nzosn__tzel:
                yulnb__poul.append(types.literal(nzosn__tzel))
            else:
                yulnb__poul.append(tdk__efd[kam__wtqgl])
        tdk__efd = tuple(yulnb__poul)
    return ReplaceFunc(func, tdk__efd, args, cmkq__hekwz, inline_bodo_calls,
        run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(ybelh__qrlwb) for ybelh__qrlwb in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        hscqa__ezrv = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {hscqa__ezrv} = 0\n', (hscqa__ezrv,)
    if isinstance(t, ArrayItemArrayType):
        lww__jgqn, vpdo__rstt = gen_init_varsize_alloc_sizes(t.dtype)
        hscqa__ezrv = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {hscqa__ezrv} = 0\n' + lww__jgqn, (hscqa__ezrv,
            ) + vpdo__rstt
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
        return 1 + sum(get_type_alloc_counts(ybelh__qrlwb.dtype) for
            ybelh__qrlwb in t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(ybelh__qrlwb) for ybelh__qrlwb in
            t.data)
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(ybelh__qrlwb) for ybelh__qrlwb in
            t.types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    cyl__qmvsa = typing_context.resolve_getattr(obj_dtype, func_name)
    if cyl__qmvsa is None:
        vke__aqqoe = types.misc.Module(np)
        try:
            cyl__qmvsa = typing_context.resolve_getattr(vke__aqqoe, func_name)
        except AttributeError as xkyyd__yqdjl:
            cyl__qmvsa = None
        if cyl__qmvsa is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return cyl__qmvsa


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    cyl__qmvsa = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(cyl__qmvsa, types.BoundFunction):
        if axis is not None:
            hxqjo__vkjd = cyl__qmvsa.get_call_type(typing_context, (), {
                'axis': axis})
        else:
            hxqjo__vkjd = cyl__qmvsa.get_call_type(typing_context, (), {})
        return hxqjo__vkjd.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(cyl__qmvsa):
            hxqjo__vkjd = cyl__qmvsa.get_call_type(typing_context, (
                obj_dtype,), {})
            return hxqjo__vkjd.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    cyl__qmvsa = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(cyl__qmvsa, types.BoundFunction):
        ide__cxjyh = cyl__qmvsa.template
        if axis is not None:
            return ide__cxjyh._overload_func(obj_dtype, axis=axis)
        else:
            return ide__cxjyh._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    mvpau__vzot = get_definition(func_ir, dict_var)
    require(isinstance(mvpau__vzot, ir.Expr))
    require(mvpau__vzot.op == 'build_map')
    swkx__bredi = mvpau__vzot.items
    hyor__btan = []
    values = []
    cnxs__wloi = False
    for kam__wtqgl in range(len(swkx__bredi)):
        adg__ntjxv, value = swkx__bredi[kam__wtqgl]
        try:
            patqg__abr = get_const_value_inner(func_ir, adg__ntjxv,
                arg_types, typemap, updated_containers)
            hyor__btan.append(patqg__abr)
            values.append(value)
        except GuardException as xkyyd__yqdjl:
            require_const_map[adg__ntjxv] = label
            cnxs__wloi = True
    if cnxs__wloi:
        raise GuardException
    return hyor__btan, values


def _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc):
    try:
        hyor__btan = tuple(get_const_value_inner(func_ir, t[0], args) for t in
            build_map.items)
    except GuardException as xkyyd__yqdjl:
        raise BodoError(err_msg, loc)
    if not all(isinstance(c, (str, int)) for c in hyor__btan):
        raise BodoError(err_msg, loc)
    return hyor__btan


def _convert_const_key_dict(args, func_ir, build_map, err_msg, scope, loc,
    output_sentinel_tuple=False):
    hyor__btan = _get_const_keys_from_dict(args, func_ir, build_map,
        err_msg, loc)
    wvwh__bvhyh = []
    rpj__gbmb = [bodo.transforms.typing_pass._create_const_var(xdi__dvs,
        'dict_key', scope, loc, wvwh__bvhyh) for xdi__dvs in hyor__btan]
    jjqdj__svkur = [t[1] for t in build_map.items]
    if output_sentinel_tuple:
        eoclp__hwq = ir.Var(scope, mk_unique_var('sentinel'), loc)
        qmt__hjdt = ir.Var(scope, mk_unique_var('dict_tup'), loc)
        wvwh__bvhyh.append(ir.Assign(ir.Const('__bodo_tup', loc),
            eoclp__hwq, loc))
        kvxj__qjb = [eoclp__hwq] + rpj__gbmb + jjqdj__svkur
        wvwh__bvhyh.append(ir.Assign(ir.Expr.build_tuple(kvxj__qjb, loc),
            qmt__hjdt, loc))
        return (qmt__hjdt,), wvwh__bvhyh
    else:
        kfj__qanw = ir.Var(scope, mk_unique_var('values_tup'), loc)
        mkur__sbuig = ir.Var(scope, mk_unique_var('idx_tup'), loc)
        wvwh__bvhyh.append(ir.Assign(ir.Expr.build_tuple(jjqdj__svkur, loc),
            kfj__qanw, loc))
        wvwh__bvhyh.append(ir.Assign(ir.Expr.build_tuple(rpj__gbmb, loc),
            mkur__sbuig, loc))
        return (kfj__qanw, mkur__sbuig), wvwh__bvhyh
