"""File containing utility functions for supporting DataFrame operations with Table Format."""
from collections import defaultdict
from typing import Dict, Set
import numba
import numpy as np
from numba.core import types
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.table import TableType
from bodo.utils.typing import get_overload_const_bool, get_overload_const_str, is_overload_constant_bool, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true, raise_bodo_error


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_mappable_table_func(table, func_name, out_arr_typ, is_method,
    used_cols=None):
    if not is_overload_constant_str(func_name) and not is_overload_none(
        func_name):
        raise_bodo_error(
            'generate_mappable_table_func(): func_name must be a constant string'
            )
    if not is_overload_constant_bool(is_method):
        raise_bodo_error(
            'generate_mappable_table_func(): is_method must be a constant boolean'
            )
    eog__ixw = not is_overload_none(func_name)
    if eog__ixw:
        func_name = get_overload_const_str(func_name)
        kaulh__vdr = get_overload_const_bool(is_method)
    gbwz__xuxmq = out_arr_typ.instance_type if isinstance(out_arr_typ,
        types.TypeRef) else out_arr_typ
    xulk__clb = gbwz__xuxmq == types.none
    lrqj__tsue = len(table.arr_types)
    if xulk__clb:
        yde__mqa = table
    else:
        xocbj__cylga = tuple([gbwz__xuxmq] * lrqj__tsue)
        yde__mqa = TableType(xocbj__cylga)
    qgoxf__wll = {'bodo': bodo, 'lst_dtype': gbwz__xuxmq, 'table_typ': yde__mqa
        }
    axchx__tgwwe = (
        'def impl(table, func_name, out_arr_typ, is_method, used_cols=None):\n'
        )
    if xulk__clb:
        axchx__tgwwe += (
            f'  out_table = bodo.hiframes.table.init_table(table, False)\n')
        axchx__tgwwe += f'  l = len(table)\n'
    else:
        axchx__tgwwe += f"""  out_list = bodo.hiframes.table.alloc_empty_list_type({lrqj__tsue}, lst_dtype)
"""
    if not is_overload_none(used_cols):
        czcga__jrhnw = used_cols.instance_type
        qeb__ltn = np.array(czcga__jrhnw.meta, dtype=np.int64)
        qgoxf__wll['used_cols_glbl'] = qeb__ltn
        nzqka__fbwdg = set([table.block_nums[nypfk__xjwat] for nypfk__xjwat in
            qeb__ltn])
        axchx__tgwwe += f'  used_cols_set = set(used_cols_glbl)\n'
    else:
        axchx__tgwwe += f'  used_cols_set = None\n'
        qeb__ltn = None
    axchx__tgwwe += (
        f'  bodo.hiframes.table.ensure_table_unboxed(table, used_cols_set)\n')
    for itxfh__fuj in table.type_to_blk.values():
        axchx__tgwwe += f"""  blk_{itxfh__fuj} = bodo.hiframes.table.get_table_block(table, {itxfh__fuj})
"""
        if xulk__clb:
            axchx__tgwwe += f"""  out_list_{itxfh__fuj} = bodo.hiframes.table.alloc_list_like(blk_{itxfh__fuj}, len(blk_{itxfh__fuj}), False)
"""
            pwyz__onct = f'out_list_{itxfh__fuj}'
        else:
            pwyz__onct = 'out_list'
        if qeb__ltn is None or itxfh__fuj in nzqka__fbwdg:
            axchx__tgwwe += f'  for i in range(len(blk_{itxfh__fuj})):\n'
            qgoxf__wll[f'col_indices_{itxfh__fuj}'] = np.array(table.
                block_to_arr_ind[itxfh__fuj], dtype=np.int64)
            axchx__tgwwe += f'    col_loc = col_indices_{itxfh__fuj}[i]\n'
            if qeb__ltn is not None:
                axchx__tgwwe += f'    if col_loc not in used_cols_set:\n'
                axchx__tgwwe += f'        continue\n'
            if xulk__clb:
                olqm__xkk = 'i'
            else:
                olqm__xkk = 'col_loc'
            if not eog__ixw:
                axchx__tgwwe += (
                    f'    {pwyz__onct}[{olqm__xkk}] = blk_{itxfh__fuj}[i]\n')
            elif kaulh__vdr:
                axchx__tgwwe += f"""    {pwyz__onct}[{olqm__xkk}] = blk_{itxfh__fuj}[i].{func_name}()
"""
            else:
                axchx__tgwwe += f"""    {pwyz__onct}[{olqm__xkk}] = {func_name}(blk_{itxfh__fuj}[i])
"""
        if xulk__clb:
            axchx__tgwwe += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, {pwyz__onct}, {itxfh__fuj})
"""
    if xulk__clb:
        axchx__tgwwe += (
            f'  out_table = bodo.hiframes.table.set_table_len(out_table, l)\n')
        axchx__tgwwe += '  return out_table\n'
    else:
        axchx__tgwwe += """  return bodo.hiframes.table.init_table_from_lists((out_list,), table_typ)
"""
    hmqid__ash = {}
    exec(axchx__tgwwe, qgoxf__wll, hmqid__ash)
    return hmqid__ash['impl']


def generate_mappable_table_func_equiv(self, scope, equiv_set, loc, args, kws):
    pejg__rhtok = args[0]
    if equiv_set.has_shape(pejg__rhtok):
        return ArrayAnalysis.AnalyzeResult(shape=pejg__rhtok, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_utils_table_utils_generate_mappable_table_func
    ) = generate_mappable_table_func_equiv


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_table_nbytes(table, out_arr, start_offset, parallel=False):
    qgoxf__wll = {'bodo': bodo, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value)}
    axchx__tgwwe = 'def impl(table, out_arr, start_offset, parallel=False):\n'
    axchx__tgwwe += '  bodo.hiframes.table.ensure_table_unboxed(table, None)\n'
    for itxfh__fuj in table.type_to_blk.values():
        axchx__tgwwe += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {itxfh__fuj})\n'
            )
        qgoxf__wll[f'col_indices_{itxfh__fuj}'] = np.array(table.
            block_to_arr_ind[itxfh__fuj], dtype=np.int64)
        axchx__tgwwe += '  for i in range(len(blk)):\n'
        axchx__tgwwe += f'    col_loc = col_indices_{itxfh__fuj}[i]\n'
        axchx__tgwwe += '    out_arr[col_loc + start_offset] = blk[i].nbytes\n'
    axchx__tgwwe += '  if parallel:\n'
    axchx__tgwwe += '    for i in range(start_offset, len(out_arr)):\n'
    axchx__tgwwe += """      out_arr[i] = bodo.libs.distributed_api.dist_reduce(out_arr[i], sum_op)
"""
    hmqid__ash = {}
    exec(axchx__tgwwe, qgoxf__wll, hmqid__ash)
    return hmqid__ash['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_concat(table, col_nums_meta, arr_type):
    arr_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type
    jzbh__ttap = table.type_to_blk[arr_type]
    qgoxf__wll = {'bodo': bodo}
    qgoxf__wll['col_indices'] = np.array(table.block_to_arr_ind[jzbh__ttap],
        dtype=np.int64)
    oinb__cbvv = col_nums_meta.instance_type
    qgoxf__wll['col_nums'] = np.array(oinb__cbvv.meta, np.int64)
    axchx__tgwwe = 'def impl(table, col_nums_meta, arr_type):\n'
    axchx__tgwwe += (
        f'  blk = bodo.hiframes.table.get_table_block(table, {jzbh__ttap})\n')
    axchx__tgwwe += (
        '  col_num_to_ind_in_blk = {c : i for i, c in enumerate(col_indices)}\n'
        )
    axchx__tgwwe += '  n = len(table)\n'
    voqj__zjo = arr_type == bodo.string_array_type
    if voqj__zjo:
        axchx__tgwwe += '  total_chars = 0\n'
        axchx__tgwwe += '  for c in col_nums:\n'
        axchx__tgwwe += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
        axchx__tgwwe += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
        axchx__tgwwe += (
            '    total_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n')
        axchx__tgwwe += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n * len(col_nums), total_chars)
"""
    else:
        axchx__tgwwe += """  out_arr = bodo.utils.utils.alloc_type(n * len(col_nums), arr_type, (-1,))
"""
    axchx__tgwwe += '  for i in range(len(col_nums)):\n'
    axchx__tgwwe += '    c = col_nums[i]\n'
    if not voqj__zjo:
        axchx__tgwwe += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
    axchx__tgwwe += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
    axchx__tgwwe += '    off = i * n\n'
    axchx__tgwwe += '    for j in range(len(arr)):\n'
    axchx__tgwwe += '      if bodo.libs.array_kernels.isna(arr, j):\n'
    axchx__tgwwe += '        bodo.libs.array_kernels.setna(out_arr, off+j)\n'
    axchx__tgwwe += '      else:\n'
    axchx__tgwwe += '        out_arr[off+j] = arr[j]\n'
    axchx__tgwwe += '  return out_arr\n'
    kgx__iqvlo = {}
    exec(axchx__tgwwe, qgoxf__wll, kgx__iqvlo)
    erx__rzjxb = kgx__iqvlo['impl']
    return erx__rzjxb


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_astype(table, new_table_typ, copy, _bodo_nan_to_str, used_cols=None):
    new_table_typ = new_table_typ.instance_type
    nqnmk__aomla = not is_overload_false(copy)
    agvqo__mztub = is_overload_true(copy)
    qgoxf__wll = {'bodo': bodo}
    hdw__gsu = table.arr_types
    oadax__gdx = new_table_typ.arr_types
    qqz__dzebb: Set[int] = set()
    vthjj__aam: Dict[types.Type, Set[types.Type]] = defaultdict(set)
    gmpx__tvla: Set[types.Type] = set()
    for nypfk__xjwat, jyjjy__hfe in enumerate(hdw__gsu):
        jmt__rqjb = oadax__gdx[nypfk__xjwat]
        if jyjjy__hfe == jmt__rqjb:
            gmpx__tvla.add(jyjjy__hfe)
        else:
            qqz__dzebb.add(nypfk__xjwat)
            vthjj__aam[jmt__rqjb].add(jyjjy__hfe)
    axchx__tgwwe = (
        'def impl(table, new_table_typ, copy, _bodo_nan_to_str, used_cols=None):\n'
        )
    axchx__tgwwe += (
        f'  out_table = bodo.hiframes.table.init_table(new_table_typ, False)\n'
        )
    axchx__tgwwe += (
        f'  out_table = bodo.hiframes.table.set_table_len(out_table, len(table))\n'
        )
    netat__kqnnu = set(range(len(hdw__gsu)))
    svxt__xqrne = netat__kqnnu - qqz__dzebb
    if not is_overload_none(used_cols):
        czcga__jrhnw = used_cols.instance_type
        ccf__wrjs = set(czcga__jrhnw.meta)
        qqz__dzebb = qqz__dzebb & ccf__wrjs
        svxt__xqrne = svxt__xqrne & ccf__wrjs
        nzqka__fbwdg = set([table.block_nums[nypfk__xjwat] for nypfk__xjwat in
            ccf__wrjs])
    else:
        ccf__wrjs = None
    qgoxf__wll['cast_cols'] = np.array(list(qqz__dzebb), dtype=np.int64)
    qgoxf__wll['copied_cols'] = np.array(list(svxt__xqrne), dtype=np.int64)
    axchx__tgwwe += f'  copied_cols_set = set(copied_cols)\n'
    axchx__tgwwe += f'  cast_cols_set = set(cast_cols)\n'
    for yis__gsu, itxfh__fuj in new_table_typ.type_to_blk.items():
        qgoxf__wll[f'typ_list_{itxfh__fuj}'] = types.List(yis__gsu)
        axchx__tgwwe += f"""  out_arr_list_{itxfh__fuj} = bodo.hiframes.table.alloc_list_like(typ_list_{itxfh__fuj}, {len(new_table_typ.block_to_arr_ind[itxfh__fuj])}, False)
"""
        if yis__gsu in gmpx__tvla:
            dod__jwu = table.type_to_blk[yis__gsu]
            if ccf__wrjs is None or dod__jwu in nzqka__fbwdg:
                jfyl__plado = table.block_to_arr_ind[dod__jwu]
                yodv__oadoe = [new_table_typ.block_offsets[foqu__icim] for
                    foqu__icim in jfyl__plado]
                qgoxf__wll[f'new_idx_{dod__jwu}'] = np.array(yodv__oadoe,
                    np.int64)
                qgoxf__wll[f'orig_arr_inds_{dod__jwu}'] = np.array(jfyl__plado,
                    np.int64)
                axchx__tgwwe += f"""  arr_list_{dod__jwu} = bodo.hiframes.table.get_table_block(table, {dod__jwu})
"""
                axchx__tgwwe += (
                    f'  for i in range(len(arr_list_{dod__jwu})):\n')
                axchx__tgwwe += (
                    f'    arr_ind_{dod__jwu} = orig_arr_inds_{dod__jwu}[i]\n')
                axchx__tgwwe += (
                    f'    if arr_ind_{dod__jwu} not in copied_cols_set:\n')
                axchx__tgwwe += f'      continue\n'
                axchx__tgwwe += f"""    bodo.hiframes.table.ensure_column_unboxed(table, arr_list_{dod__jwu}, i, arr_ind_{dod__jwu})
"""
                axchx__tgwwe += (
                    f'    out_idx_{itxfh__fuj}_{dod__jwu} = new_idx_{dod__jwu}[i]\n'
                    )
                axchx__tgwwe += (
                    f'    arr_val_{dod__jwu} = arr_list_{dod__jwu}[i]\n')
                if agvqo__mztub:
                    axchx__tgwwe += (
                        f'    arr_val_{dod__jwu} = arr_val_{dod__jwu}.copy()\n'
                        )
                elif nqnmk__aomla:
                    axchx__tgwwe += f"""    arr_val_{dod__jwu} = arr_val_{dod__jwu}.copy() if copy else arr_val_{itxfh__fuj}
"""
                axchx__tgwwe += f"""    out_arr_list_{itxfh__fuj}[out_idx_{itxfh__fuj}_{dod__jwu}] = arr_val_{dod__jwu}
"""
    kwgit__yxe = set()
    for yis__gsu, itxfh__fuj in new_table_typ.type_to_blk.items():
        if yis__gsu in vthjj__aam:
            if isinstance(yis__gsu, bodo.IntegerArrayType):
                yfga__aqnoh = yis__gsu.get_pandas_scalar_type_instance.name
            else:
                yfga__aqnoh = yis__gsu.dtype
            qgoxf__wll[f'typ_{itxfh__fuj}'] = yfga__aqnoh
            vlndx__apo = vthjj__aam[yis__gsu]
            for ynksa__kze in vlndx__apo:
                dod__jwu = table.type_to_blk[ynksa__kze]
                if ccf__wrjs is None or dod__jwu in nzqka__fbwdg:
                    if (ynksa__kze not in gmpx__tvla and ynksa__kze not in
                        kwgit__yxe):
                        jfyl__plado = table.block_to_arr_ind[dod__jwu]
                        yodv__oadoe = [new_table_typ.block_offsets[
                            foqu__icim] for foqu__icim in jfyl__plado]
                        qgoxf__wll[f'new_idx_{dod__jwu}'] = np.array(
                            yodv__oadoe, np.int64)
                        qgoxf__wll[f'orig_arr_inds_{dod__jwu}'] = np.array(
                            jfyl__plado, np.int64)
                        axchx__tgwwe += f"""  arr_list_{dod__jwu} = bodo.hiframes.table.get_table_block(table, {dod__jwu})
"""
                    kwgit__yxe.add(ynksa__kze)
                    axchx__tgwwe += (
                        f'  for i in range(len(arr_list_{dod__jwu})):\n')
                    axchx__tgwwe += (
                        f'    arr_ind_{dod__jwu} = orig_arr_inds_{dod__jwu}[i]\n'
                        )
                    axchx__tgwwe += (
                        f'    if arr_ind_{dod__jwu} not in cast_cols_set:\n')
                    axchx__tgwwe += f'      continue\n'
                    axchx__tgwwe += f"""    bodo.hiframes.table.ensure_column_unboxed(table, arr_list_{dod__jwu}, i, arr_ind_{dod__jwu})
"""
                    axchx__tgwwe += (
                        f'    out_idx_{itxfh__fuj}_{dod__jwu} = new_idx_{dod__jwu}[i]\n'
                        )
                    axchx__tgwwe += f"""    arr_val_{itxfh__fuj} =  bodo.utils.conversion.fix_arr_dtype(arr_list_{dod__jwu}[i], typ_{itxfh__fuj}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)
"""
                    axchx__tgwwe += f"""    out_arr_list_{itxfh__fuj}[out_idx_{itxfh__fuj}_{dod__jwu}] = arr_val_{itxfh__fuj}
"""
        axchx__tgwwe += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, out_arr_list_{itxfh__fuj}, {itxfh__fuj})
"""
    axchx__tgwwe += '  return out_table\n'
    hmqid__ash = {}
    exec(axchx__tgwwe, qgoxf__wll, hmqid__ash)
    return hmqid__ash['impl']


def table_astype_equiv(self, scope, equiv_set, loc, args, kws):
    pejg__rhtok = args[0]
    if equiv_set.has_shape(pejg__rhtok):
        return ArrayAnalysis.AnalyzeResult(shape=pejg__rhtok, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_utils_table_utils_table_astype = (
    table_astype_equiv)
