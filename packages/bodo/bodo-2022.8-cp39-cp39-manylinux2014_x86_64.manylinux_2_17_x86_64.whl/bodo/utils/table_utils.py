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
    npah__zowc = not is_overload_none(func_name)
    if npah__zowc:
        func_name = get_overload_const_str(func_name)
        rayrq__euzh = get_overload_const_bool(is_method)
    kpib__jqsn = out_arr_typ.instance_type if isinstance(out_arr_typ, types
        .TypeRef) else out_arr_typ
    tqui__tjw = kpib__jqsn == types.none
    bvid__yrswt = len(table.arr_types)
    if tqui__tjw:
        nmzs__izohw = table
    else:
        ama__nmri = tuple([kpib__jqsn] * bvid__yrswt)
        nmzs__izohw = TableType(ama__nmri)
    zfr__mxyaz = {'bodo': bodo, 'lst_dtype': kpib__jqsn, 'table_typ':
        nmzs__izohw}
    mlh__mdsm = (
        'def impl(table, func_name, out_arr_typ, is_method, used_cols=None):\n'
        )
    if tqui__tjw:
        mlh__mdsm += (
            f'  out_table = bodo.hiframes.table.init_table(table, False)\n')
        mlh__mdsm += f'  l = len(table)\n'
    else:
        mlh__mdsm += f"""  out_list = bodo.hiframes.table.alloc_empty_list_type({bvid__yrswt}, lst_dtype)
"""
    if not is_overload_none(used_cols):
        yicq__zqpx = used_cols.instance_type
        qwpsj__tdn = np.array(yicq__zqpx.meta, dtype=np.int64)
        zfr__mxyaz['used_cols_glbl'] = qwpsj__tdn
        qhei__jsy = set([table.block_nums[mitb__msb] for mitb__msb in
            qwpsj__tdn])
        mlh__mdsm += f'  used_cols_set = set(used_cols_glbl)\n'
    else:
        mlh__mdsm += f'  used_cols_set = None\n'
        qwpsj__tdn = None
    mlh__mdsm += (
        f'  bodo.hiframes.table.ensure_table_unboxed(table, used_cols_set)\n')
    for cfbbf__jmvc in table.type_to_blk.values():
        mlh__mdsm += f"""  blk_{cfbbf__jmvc} = bodo.hiframes.table.get_table_block(table, {cfbbf__jmvc})
"""
        if tqui__tjw:
            mlh__mdsm += f"""  out_list_{cfbbf__jmvc} = bodo.hiframes.table.alloc_list_like(blk_{cfbbf__jmvc}, len(blk_{cfbbf__jmvc}), False)
"""
            qysei__ecojl = f'out_list_{cfbbf__jmvc}'
        else:
            qysei__ecojl = 'out_list'
        if qwpsj__tdn is None or cfbbf__jmvc in qhei__jsy:
            mlh__mdsm += f'  for i in range(len(blk_{cfbbf__jmvc})):\n'
            zfr__mxyaz[f'col_indices_{cfbbf__jmvc}'] = np.array(table.
                block_to_arr_ind[cfbbf__jmvc], dtype=np.int64)
            mlh__mdsm += f'    col_loc = col_indices_{cfbbf__jmvc}[i]\n'
            if qwpsj__tdn is not None:
                mlh__mdsm += f'    if col_loc not in used_cols_set:\n'
                mlh__mdsm += f'        continue\n'
            if tqui__tjw:
                pamlf__sxuw = 'i'
            else:
                pamlf__sxuw = 'col_loc'
            if not npah__zowc:
                mlh__mdsm += (
                    f'    {qysei__ecojl}[{pamlf__sxuw}] = blk_{cfbbf__jmvc}[i]\n'
                    )
            elif rayrq__euzh:
                mlh__mdsm += f"""    {qysei__ecojl}[{pamlf__sxuw}] = blk_{cfbbf__jmvc}[i].{func_name}()
"""
            else:
                mlh__mdsm += f"""    {qysei__ecojl}[{pamlf__sxuw}] = {func_name}(blk_{cfbbf__jmvc}[i])
"""
        if tqui__tjw:
            mlh__mdsm += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, {qysei__ecojl}, {cfbbf__jmvc})
"""
    if tqui__tjw:
        mlh__mdsm += (
            f'  out_table = bodo.hiframes.table.set_table_len(out_table, l)\n')
        mlh__mdsm += '  return out_table\n'
    else:
        mlh__mdsm += (
            '  return bodo.hiframes.table.init_table_from_lists((out_list,), table_typ)\n'
            )
    euh__spxkh = {}
    exec(mlh__mdsm, zfr__mxyaz, euh__spxkh)
    return euh__spxkh['impl']


def generate_mappable_table_func_equiv(self, scope, equiv_set, loc, args, kws):
    ognig__azblv = args[0]
    if equiv_set.has_shape(ognig__azblv):
        return ArrayAnalysis.AnalyzeResult(shape=ognig__azblv, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_utils_table_utils_generate_mappable_table_func
    ) = generate_mappable_table_func_equiv


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_table_nbytes(table, out_arr, start_offset, parallel=False):
    zfr__mxyaz = {'bodo': bodo, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value)}
    mlh__mdsm = 'def impl(table, out_arr, start_offset, parallel=False):\n'
    mlh__mdsm += '  bodo.hiframes.table.ensure_table_unboxed(table, None)\n'
    for cfbbf__jmvc in table.type_to_blk.values():
        mlh__mdsm += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {cfbbf__jmvc})\n'
            )
        zfr__mxyaz[f'col_indices_{cfbbf__jmvc}'] = np.array(table.
            block_to_arr_ind[cfbbf__jmvc], dtype=np.int64)
        mlh__mdsm += '  for i in range(len(blk)):\n'
        mlh__mdsm += f'    col_loc = col_indices_{cfbbf__jmvc}[i]\n'
        mlh__mdsm += '    out_arr[col_loc + start_offset] = blk[i].nbytes\n'
    mlh__mdsm += '  if parallel:\n'
    mlh__mdsm += '    for i in range(start_offset, len(out_arr)):\n'
    mlh__mdsm += (
        '      out_arr[i] = bodo.libs.distributed_api.dist_reduce(out_arr[i], sum_op)\n'
        )
    euh__spxkh = {}
    exec(mlh__mdsm, zfr__mxyaz, euh__spxkh)
    return euh__spxkh['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_concat(table, col_nums_meta, arr_type):
    arr_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type
    sgij__gidju = table.type_to_blk[arr_type]
    zfr__mxyaz = {'bodo': bodo}
    zfr__mxyaz['col_indices'] = np.array(table.block_to_arr_ind[sgij__gidju
        ], dtype=np.int64)
    xegi__yjaq = col_nums_meta.instance_type
    zfr__mxyaz['col_nums'] = np.array(xegi__yjaq.meta, np.int64)
    mlh__mdsm = 'def impl(table, col_nums_meta, arr_type):\n'
    mlh__mdsm += (
        f'  blk = bodo.hiframes.table.get_table_block(table, {sgij__gidju})\n')
    mlh__mdsm += (
        '  col_num_to_ind_in_blk = {c : i for i, c in enumerate(col_indices)}\n'
        )
    mlh__mdsm += '  n = len(table)\n'
    zhe__kxtq = arr_type == bodo.string_array_type
    if zhe__kxtq:
        mlh__mdsm += '  total_chars = 0\n'
        mlh__mdsm += '  for c in col_nums:\n'
        mlh__mdsm += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
        mlh__mdsm += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
        mlh__mdsm += (
            '    total_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n')
        mlh__mdsm += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n * len(col_nums), total_chars)
"""
    else:
        mlh__mdsm += """  out_arr = bodo.utils.utils.alloc_type(n * len(col_nums), arr_type, (-1,))
"""
    mlh__mdsm += '  for i in range(len(col_nums)):\n'
    mlh__mdsm += '    c = col_nums[i]\n'
    if not zhe__kxtq:
        mlh__mdsm += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
    mlh__mdsm += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
    mlh__mdsm += '    off = i * n\n'
    mlh__mdsm += '    for j in range(len(arr)):\n'
    mlh__mdsm += '      if bodo.libs.array_kernels.isna(arr, j):\n'
    mlh__mdsm += '        bodo.libs.array_kernels.setna(out_arr, off+j)\n'
    mlh__mdsm += '      else:\n'
    mlh__mdsm += '        out_arr[off+j] = arr[j]\n'
    mlh__mdsm += '  return out_arr\n'
    cyvzj__phihc = {}
    exec(mlh__mdsm, zfr__mxyaz, cyvzj__phihc)
    uihgy__lxw = cyvzj__phihc['impl']
    return uihgy__lxw


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_astype(table, new_table_typ, copy, _bodo_nan_to_str, used_cols=None):
    new_table_typ = new_table_typ.instance_type
    nviv__wtlbg = not is_overload_false(copy)
    vcgoc__uywww = is_overload_true(copy)
    zfr__mxyaz = {'bodo': bodo}
    frbr__kpme = table.arr_types
    dodp__hbgl = new_table_typ.arr_types
    dddjb__udq: Set[int] = set()
    cpgf__lvbxf: Dict[types.Type, Set[types.Type]] = defaultdict(set)
    cdvml__hgih: Set[types.Type] = set()
    for mitb__msb, llqbq__junvo in enumerate(frbr__kpme):
        kbyoh__rdq = dodp__hbgl[mitb__msb]
        if llqbq__junvo == kbyoh__rdq:
            cdvml__hgih.add(llqbq__junvo)
        else:
            dddjb__udq.add(mitb__msb)
            cpgf__lvbxf[kbyoh__rdq].add(llqbq__junvo)
    mlh__mdsm = (
        'def impl(table, new_table_typ, copy, _bodo_nan_to_str, used_cols=None):\n'
        )
    mlh__mdsm += (
        f'  out_table = bodo.hiframes.table.init_table(new_table_typ, False)\n'
        )
    mlh__mdsm += (
        f'  out_table = bodo.hiframes.table.set_table_len(out_table, len(table))\n'
        )
    mpbj__njzbp = set(range(len(frbr__kpme)))
    hoe__arki = mpbj__njzbp - dddjb__udq
    if not is_overload_none(used_cols):
        yicq__zqpx = used_cols.instance_type
        knnx__qtmj = set(yicq__zqpx.meta)
        dddjb__udq = dddjb__udq & knnx__qtmj
        hoe__arki = hoe__arki & knnx__qtmj
        qhei__jsy = set([table.block_nums[mitb__msb] for mitb__msb in
            knnx__qtmj])
    else:
        knnx__qtmj = None
    zfr__mxyaz['cast_cols'] = np.array(list(dddjb__udq), dtype=np.int64)
    zfr__mxyaz['copied_cols'] = np.array(list(hoe__arki), dtype=np.int64)
    mlh__mdsm += f'  copied_cols_set = set(copied_cols)\n'
    mlh__mdsm += f'  cast_cols_set = set(cast_cols)\n'
    for bmnqq__pws, cfbbf__jmvc in new_table_typ.type_to_blk.items():
        zfr__mxyaz[f'typ_list_{cfbbf__jmvc}'] = types.List(bmnqq__pws)
        mlh__mdsm += f"""  out_arr_list_{cfbbf__jmvc} = bodo.hiframes.table.alloc_list_like(typ_list_{cfbbf__jmvc}, {len(new_table_typ.block_to_arr_ind[cfbbf__jmvc])}, False)
"""
        if bmnqq__pws in cdvml__hgih:
            gjr__nsax = table.type_to_blk[bmnqq__pws]
            if knnx__qtmj is None or gjr__nsax in qhei__jsy:
                ezq__zvrb = table.block_to_arr_ind[gjr__nsax]
                kcwbg__gsugn = [new_table_typ.block_offsets[qeic__cbvj] for
                    qeic__cbvj in ezq__zvrb]
                zfr__mxyaz[f'new_idx_{gjr__nsax}'] = np.array(kcwbg__gsugn,
                    np.int64)
                zfr__mxyaz[f'orig_arr_inds_{gjr__nsax}'] = np.array(ezq__zvrb,
                    np.int64)
                mlh__mdsm += f"""  arr_list_{gjr__nsax} = bodo.hiframes.table.get_table_block(table, {gjr__nsax})
"""
                mlh__mdsm += f'  for i in range(len(arr_list_{gjr__nsax})):\n'
                mlh__mdsm += (
                    f'    arr_ind_{gjr__nsax} = orig_arr_inds_{gjr__nsax}[i]\n'
                    )
                mlh__mdsm += (
                    f'    if arr_ind_{gjr__nsax} not in copied_cols_set:\n')
                mlh__mdsm += f'      continue\n'
                mlh__mdsm += f"""    bodo.hiframes.table.ensure_column_unboxed(table, arr_list_{gjr__nsax}, i, arr_ind_{gjr__nsax})
"""
                mlh__mdsm += (
                    f'    out_idx_{cfbbf__jmvc}_{gjr__nsax} = new_idx_{gjr__nsax}[i]\n'
                    )
                mlh__mdsm += (
                    f'    arr_val_{gjr__nsax} = arr_list_{gjr__nsax}[i]\n')
                if vcgoc__uywww:
                    mlh__mdsm += (
                        f'    arr_val_{gjr__nsax} = arr_val_{gjr__nsax}.copy()\n'
                        )
                elif nviv__wtlbg:
                    mlh__mdsm += f"""    arr_val_{gjr__nsax} = arr_val_{gjr__nsax}.copy() if copy else arr_val_{cfbbf__jmvc}
"""
                mlh__mdsm += f"""    out_arr_list_{cfbbf__jmvc}[out_idx_{cfbbf__jmvc}_{gjr__nsax}] = arr_val_{gjr__nsax}
"""
    ksjbr__ehe = set()
    for bmnqq__pws, cfbbf__jmvc in new_table_typ.type_to_blk.items():
        if bmnqq__pws in cpgf__lvbxf:
            if isinstance(bmnqq__pws, bodo.IntegerArrayType):
                ibck__hbxj = bmnqq__pws.get_pandas_scalar_type_instance.name
            else:
                ibck__hbxj = bmnqq__pws.dtype
            zfr__mxyaz[f'typ_{cfbbf__jmvc}'] = ibck__hbxj
            ivrr__khi = cpgf__lvbxf[bmnqq__pws]
            for krj__akte in ivrr__khi:
                gjr__nsax = table.type_to_blk[krj__akte]
                if knnx__qtmj is None or gjr__nsax in qhei__jsy:
                    if (krj__akte not in cdvml__hgih and krj__akte not in
                        ksjbr__ehe):
                        ezq__zvrb = table.block_to_arr_ind[gjr__nsax]
                        kcwbg__gsugn = [new_table_typ.block_offsets[
                            qeic__cbvj] for qeic__cbvj in ezq__zvrb]
                        zfr__mxyaz[f'new_idx_{gjr__nsax}'] = np.array(
                            kcwbg__gsugn, np.int64)
                        zfr__mxyaz[f'orig_arr_inds_{gjr__nsax}'] = np.array(
                            ezq__zvrb, np.int64)
                        mlh__mdsm += f"""  arr_list_{gjr__nsax} = bodo.hiframes.table.get_table_block(table, {gjr__nsax})
"""
                    ksjbr__ehe.add(krj__akte)
                    mlh__mdsm += (
                        f'  for i in range(len(arr_list_{gjr__nsax})):\n')
                    mlh__mdsm += (
                        f'    arr_ind_{gjr__nsax} = orig_arr_inds_{gjr__nsax}[i]\n'
                        )
                    mlh__mdsm += (
                        f'    if arr_ind_{gjr__nsax} not in cast_cols_set:\n')
                    mlh__mdsm += f'      continue\n'
                    mlh__mdsm += f"""    bodo.hiframes.table.ensure_column_unboxed(table, arr_list_{gjr__nsax}, i, arr_ind_{gjr__nsax})
"""
                    mlh__mdsm += (
                        f'    out_idx_{cfbbf__jmvc}_{gjr__nsax} = new_idx_{gjr__nsax}[i]\n'
                        )
                    mlh__mdsm += f"""    arr_val_{cfbbf__jmvc} =  bodo.utils.conversion.fix_arr_dtype(arr_list_{gjr__nsax}[i], typ_{cfbbf__jmvc}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)
"""
                    mlh__mdsm += f"""    out_arr_list_{cfbbf__jmvc}[out_idx_{cfbbf__jmvc}_{gjr__nsax}] = arr_val_{cfbbf__jmvc}
"""
        mlh__mdsm += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, out_arr_list_{cfbbf__jmvc}, {cfbbf__jmvc})
"""
    mlh__mdsm += '  return out_table\n'
    euh__spxkh = {}
    exec(mlh__mdsm, zfr__mxyaz, euh__spxkh)
    return euh__spxkh['impl']


def table_astype_equiv(self, scope, equiv_set, loc, args, kws):
    ognig__azblv = args[0]
    if equiv_set.has_shape(ognig__azblv):
        return ArrayAnalysis.AnalyzeResult(shape=ognig__azblv, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_utils_table_utils_table_astype = (
    table_astype_equiv)
