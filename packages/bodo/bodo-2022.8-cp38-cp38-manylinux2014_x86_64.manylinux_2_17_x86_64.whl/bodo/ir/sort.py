"""IR node for the data sorting"""
from collections import defaultdict
from typing import List, Set, Tuple, Union
import numba
import numpy as np
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes, replace_vars_inner, visit_vars_inner
import bodo
from bodo.libs.array import arr_info_list_to_table, array_to_info, cpp_table_to_py_data, delete_table, delete_table_decref_arrays, info_from_table, info_to_array, py_data_to_cpp_table, sort_values_table
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.transforms.table_column_del_pass import _compute_table_column_uses, _find_used_columns, ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import MetaType, type_has_unknown_cats
from bodo.utils.utils import gen_getitem


class Sort(ir.Stmt):

    def __init__(self, df_in: str, df_out: str, in_vars: List[ir.Var],
        out_vars: List[ir.Var], key_inds: Tuple[int], inplace: bool, loc:
        ir.Loc, ascending_list: Union[List[bool], bool]=True, na_position:
        Union[List[str], str]='last', is_table_format: bool=False,
        num_table_arrays: int=0):
        self.df_in = df_in
        self.df_out = df_out
        self.in_vars = in_vars
        self.out_vars = out_vars
        self.key_inds = key_inds
        self.inplace = inplace
        self.is_table_format = is_table_format
        self.num_table_arrays = num_table_arrays
        self.dead_var_inds: Set[int] = set()
        self.dead_key_var_inds: Set[int] = set()
        if isinstance(na_position, str):
            if na_position == 'last':
                self.na_position_b = (True,) * len(key_inds)
            else:
                self.na_position_b = (False,) * len(key_inds)
        else:
            self.na_position_b = tuple([(True if gqzhg__hno == 'last' else 
                False) for gqzhg__hno in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_inds)
        self.ascending_list = ascending_list
        self.loc = loc

    def get_live_in_vars(self):
        return [iuwyz__pkw for iuwyz__pkw in self.in_vars if iuwyz__pkw is not
            None]

    def get_live_out_vars(self):
        return [iuwyz__pkw for iuwyz__pkw in self.out_vars if iuwyz__pkw is not
            None]

    def __repr__(self):
        klpoo__hacvb = ', '.join(iuwyz__pkw.name for iuwyz__pkw in self.
            get_live_in_vars())
        vryrw__fbl = f'{self.df_in}{{{klpoo__hacvb}}}'
        xjcb__ciuto = ', '.join(iuwyz__pkw.name for iuwyz__pkw in self.
            get_live_out_vars())
        pwuc__gtx = f'{self.df_out}{{{xjcb__ciuto}}}'
        return f'Sort (keys: {self.key_inds}): {vryrw__fbl} {pwuc__gtx}'


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    qtf__ihme = []
    for sbfbm__qgzg in sort_node.get_live_in_vars():
        qdhx__jbz = equiv_set.get_shape(sbfbm__qgzg)
        if qdhx__jbz is not None:
            qtf__ihme.append(qdhx__jbz[0])
    if len(qtf__ihme) > 1:
        equiv_set.insert_equiv(*qtf__ihme)
    jqjbv__ujxur = []
    qtf__ihme = []
    for sbfbm__qgzg in sort_node.get_live_out_vars():
        chie__bmkg = typemap[sbfbm__qgzg.name]
        lzvuv__pdok = array_analysis._gen_shape_call(equiv_set, sbfbm__qgzg,
            chie__bmkg.ndim, None, jqjbv__ujxur)
        equiv_set.insert_equiv(sbfbm__qgzg, lzvuv__pdok)
        qtf__ihme.append(lzvuv__pdok[0])
        equiv_set.define(sbfbm__qgzg, set())
    if len(qtf__ihme) > 1:
        equiv_set.insert_equiv(*qtf__ihme)
    return [], jqjbv__ujxur


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    rotwy__nmwsn = sort_node.get_live_in_vars()
    pkisw__mxu = sort_node.get_live_out_vars()
    sify__eykkt = Distribution.OneD
    for sbfbm__qgzg in rotwy__nmwsn:
        sify__eykkt = Distribution(min(sify__eykkt.value, array_dists[
            sbfbm__qgzg.name].value))
    tvo__vxh = Distribution(min(sify__eykkt.value, Distribution.OneD_Var.value)
        )
    for sbfbm__qgzg in pkisw__mxu:
        if sbfbm__qgzg.name in array_dists:
            tvo__vxh = Distribution(min(tvo__vxh.value, array_dists[
                sbfbm__qgzg.name].value))
    if tvo__vxh != Distribution.OneD_Var:
        sify__eykkt = tvo__vxh
    for sbfbm__qgzg in rotwy__nmwsn:
        array_dists[sbfbm__qgzg.name] = sify__eykkt
    for sbfbm__qgzg in pkisw__mxu:
        array_dists[sbfbm__qgzg.name] = tvo__vxh


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for nofh__fnmsw, vhi__jwf in enumerate(sort_node.out_vars):
        sggka__sslep = sort_node.in_vars[nofh__fnmsw]
        if sggka__sslep is not None and vhi__jwf is not None:
            typeinferer.constraints.append(typeinfer.Propagate(dst=vhi__jwf
                .name, src=sggka__sslep.name, loc=sort_node.loc))


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for sbfbm__qgzg in sort_node.get_live_out_vars():
            definitions[sbfbm__qgzg.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    for nofh__fnmsw in range(len(sort_node.in_vars)):
        if sort_node.in_vars[nofh__fnmsw] is not None:
            sort_node.in_vars[nofh__fnmsw] = visit_vars_inner(sort_node.
                in_vars[nofh__fnmsw], callback, cbdata)
        if sort_node.out_vars[nofh__fnmsw] is not None:
            sort_node.out_vars[nofh__fnmsw] = visit_vars_inner(sort_node.
                out_vars[nofh__fnmsw], callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if sort_node.is_table_format:
        dyff__qdot = sort_node.out_vars[0]
        if dyff__qdot is not None and dyff__qdot.name not in lives:
            sort_node.out_vars[0] = None
            dead_cols = set(range(sort_node.num_table_arrays))
            ffrx__hiso = set(sort_node.key_inds)
            sort_node.dead_key_var_inds.update(dead_cols & ffrx__hiso)
            sort_node.dead_var_inds.update(dead_cols - ffrx__hiso)
            if len(ffrx__hiso & dead_cols) == 0:
                sort_node.in_vars[0] = None
        for nofh__fnmsw in range(1, len(sort_node.out_vars)):
            iuwyz__pkw = sort_node.out_vars[nofh__fnmsw]
            if iuwyz__pkw is not None and iuwyz__pkw.name not in lives:
                sort_node.out_vars[nofh__fnmsw] = None
                uzmjf__fdymh = sort_node.num_table_arrays + nofh__fnmsw - 1
                if uzmjf__fdymh in sort_node.key_inds:
                    sort_node.dead_key_var_inds.add(uzmjf__fdymh)
                else:
                    sort_node.dead_var_inds.add(uzmjf__fdymh)
                    sort_node.in_vars[nofh__fnmsw] = None
    else:
        for nofh__fnmsw in range(len(sort_node.out_vars)):
            iuwyz__pkw = sort_node.out_vars[nofh__fnmsw]
            if iuwyz__pkw is not None and iuwyz__pkw.name not in lives:
                sort_node.out_vars[nofh__fnmsw] = None
                if nofh__fnmsw in sort_node.key_inds:
                    sort_node.dead_key_var_inds.add(nofh__fnmsw)
                else:
                    sort_node.dead_var_inds.add(nofh__fnmsw)
                    sort_node.in_vars[nofh__fnmsw] = None
    if all(iuwyz__pkw is None for iuwyz__pkw in sort_node.out_vars):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({iuwyz__pkw.name for iuwyz__pkw in sort_node.
        get_live_in_vars()})
    if not sort_node.inplace:
        def_set.update({iuwyz__pkw.name for iuwyz__pkw in sort_node.
            get_live_out_vars()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    rss__xndd = set()
    if not sort_node.inplace:
        rss__xndd.update({iuwyz__pkw.name for iuwyz__pkw in sort_node.
            get_live_out_vars()})
    return set(), rss__xndd


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for nofh__fnmsw in range(len(sort_node.in_vars)):
        if sort_node.in_vars[nofh__fnmsw] is not None:
            sort_node.in_vars[nofh__fnmsw] = replace_vars_inner(sort_node.
                in_vars[nofh__fnmsw], var_dict)
        if sort_node.out_vars[nofh__fnmsw] is not None:
            sort_node.out_vars[nofh__fnmsw] = replace_vars_inner(sort_node.
                out_vars[nofh__fnmsw], var_dict)


ir_utils.apply_copy_propagate_extensions[Sort] = apply_copies_sort


def sort_distributed_run(sort_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    parallel = False
    in_vars = sort_node.get_live_in_vars()
    out_vars = sort_node.get_live_out_vars()
    if array_dists is not None:
        parallel = True
        for iuwyz__pkw in (in_vars + out_vars):
            if array_dists[iuwyz__pkw.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                iuwyz__pkw.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    nodes = []
    if not sort_node.inplace:
        tqzy__lobw = []
        for iuwyz__pkw in in_vars:
            jzwf__nwnc = _copy_array_nodes(iuwyz__pkw, nodes, typingctx,
                targetctx, typemap, calltypes, sort_node.dead_var_inds)
            tqzy__lobw.append(jzwf__nwnc)
        in_vars = tqzy__lobw
    out_types = [(typemap[iuwyz__pkw.name] if iuwyz__pkw is not None else
        types.none) for iuwyz__pkw in sort_node.out_vars]
    ifi__ptly, qlwdj__ueqn = get_sort_cpp_section(sort_node, out_types,
        parallel)
    iez__zfj = {}
    exec(ifi__ptly, {}, iez__zfj)
    jkc__dbgu = iez__zfj['f']
    qlwdj__ueqn.update({'bodo': bodo, 'np': np, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'sort_values_table':
        sort_values_table, 'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info, 'py_data_to_cpp_table':
        py_data_to_cpp_table, 'cpp_table_to_py_data': cpp_table_to_py_data})
    qlwdj__ueqn.update({f'out_type{nofh__fnmsw}': out_types[nofh__fnmsw] for
        nofh__fnmsw in range(len(out_types))})
    rwji__xpy = compile_to_numba_ir(jkc__dbgu, qlwdj__ueqn, typingctx=
        typingctx, targetctx=targetctx, arg_typs=tuple(typemap[iuwyz__pkw.
        name] for iuwyz__pkw in in_vars), typemap=typemap, calltypes=calltypes
        ).blocks.popitem()[1]
    replace_arg_nodes(rwji__xpy, in_vars)
    tfn__khb = rwji__xpy.body[-2].value.value
    nodes += rwji__xpy.body[:-2]
    for nofh__fnmsw, iuwyz__pkw in enumerate(out_vars):
        gen_getitem(iuwyz__pkw, tfn__khb, nofh__fnmsw, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes,
    dead_cols):
    from bodo.hiframes.table import TableType
    mwwdo__qse = lambda arr: arr.copy()
    idz__wfegk = None
    if isinstance(typemap[var.name], TableType):
        lvm__wddoj = len(typemap[var.name].arr_types)
        idz__wfegk = set(range(lvm__wddoj)) - dead_cols
        idz__wfegk = MetaType(tuple(sorted(idz__wfegk)))
        mwwdo__qse = (lambda T: bodo.utils.table_utils.
            generate_mappable_table_func(T, 'copy', types.none, True,
            used_cols=_used_columns))
    rwji__xpy = compile_to_numba_ir(mwwdo__qse, {'bodo': bodo, 'types':
        types, '_used_columns': idz__wfegk}, typingctx=typingctx, targetctx
        =targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(rwji__xpy, [var])
    nodes += rwji__xpy.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(sort_node, out_types, parallel):
    mmpx__pgbo = len(sort_node.key_inds)
    lvbod__drda = len(sort_node.in_vars)
    ldj__wun = len(sort_node.out_vars)
    n_cols = (sort_node.num_table_arrays + lvbod__drda - 1 if sort_node.
        is_table_format else lvbod__drda)
    yoqbv__wgvh, fljoj__wisxb, gfydk__iwe = _get_cpp_col_ind_mappings(sort_node
        .key_inds, sort_node.dead_var_inds, sort_node.dead_key_var_inds, n_cols
        )
    fet__qqsvi = []
    if sort_node.is_table_format:
        fet__qqsvi.append('arg0')
        for nofh__fnmsw in range(1, lvbod__drda):
            uzmjf__fdymh = sort_node.num_table_arrays + nofh__fnmsw - 1
            if uzmjf__fdymh not in sort_node.dead_var_inds:
                fet__qqsvi.append(f'arg{uzmjf__fdymh}')
    else:
        for nofh__fnmsw in range(n_cols):
            if nofh__fnmsw not in sort_node.dead_var_inds:
                fet__qqsvi.append(f'arg{nofh__fnmsw}')
    ifi__ptly = f"def f({', '.join(fet__qqsvi)}):\n"
    if sort_node.is_table_format:
        ilzpr__vxcta = ',' if lvbod__drda - 1 == 1 else ''
        scud__ibg = []
        for nofh__fnmsw in range(sort_node.num_table_arrays, n_cols):
            if nofh__fnmsw in sort_node.dead_var_inds:
                scud__ibg.append('None')
            else:
                scud__ibg.append(f'arg{nofh__fnmsw}')
        ifi__ptly += f"""  in_cpp_table = py_data_to_cpp_table(arg0, ({', '.join(scud__ibg)}{ilzpr__vxcta}), in_col_inds, {sort_node.num_table_arrays})
"""
    else:
        krndr__rxcrn = {yfok__xmd: nofh__fnmsw for nofh__fnmsw, yfok__xmd in
            enumerate(yoqbv__wgvh)}
        tftsd__zdpeg = [None] * len(yoqbv__wgvh)
        for nofh__fnmsw in range(n_cols):
            vwu__mkyc = krndr__rxcrn.get(nofh__fnmsw, -1)
            if vwu__mkyc != -1:
                tftsd__zdpeg[vwu__mkyc] = f'array_to_info(arg{nofh__fnmsw})'
        ifi__ptly += '  info_list_total = [{}]\n'.format(','.join(tftsd__zdpeg)
            )
        ifi__ptly += (
            '  in_cpp_table = arr_info_list_to_table(info_list_total)\n')
    ifi__ptly += '  vect_ascending = np.array([{}], np.int64)\n'.format(','
        .join('1' if zcdn__tdueg else '0' for zcdn__tdueg in sort_node.
        ascending_list))
    ifi__ptly += '  na_position = np.array([{}], np.int64)\n'.format(','.
        join('1' if zcdn__tdueg else '0' for zcdn__tdueg in sort_node.
        na_position_b))
    ifi__ptly += '  dead_keys = np.array([{}], np.int64)\n'.format(','.join
        ('1' if nofh__fnmsw in gfydk__iwe else '0' for nofh__fnmsw in range
        (mmpx__pgbo)))
    ifi__ptly += f'  total_rows_np = np.array([0], dtype=np.int64)\n'
    ifi__ptly += f"""  out_cpp_table = sort_values_table(in_cpp_table, {mmpx__pgbo}, vect_ascending.ctypes, na_position.ctypes, dead_keys.ctypes, total_rows_np.ctypes, {parallel})
"""
    if sort_node.is_table_format:
        ilzpr__vxcta = ',' if ldj__wun == 1 else ''
        isj__jqlp = (
            f"({', '.join(f'out_type{nofh__fnmsw}' if not type_has_unknown_cats(out_types[nofh__fnmsw]) else f'arg{nofh__fnmsw}' for nofh__fnmsw in range(ldj__wun))}{ilzpr__vxcta})"
            )
        ifi__ptly += f"""  out_data = cpp_table_to_py_data(out_cpp_table, out_col_inds, {isj__jqlp}, total_rows_np[0], {sort_node.num_table_arrays})
"""
    else:
        krndr__rxcrn = {yfok__xmd: nofh__fnmsw for nofh__fnmsw, yfok__xmd in
            enumerate(fljoj__wisxb)}
        tftsd__zdpeg = []
        for nofh__fnmsw in range(n_cols):
            vwu__mkyc = krndr__rxcrn.get(nofh__fnmsw, -1)
            if vwu__mkyc != -1:
                vplx__ddt = (f'out_type{nofh__fnmsw}' if not
                    type_has_unknown_cats(out_types[nofh__fnmsw]) else
                    f'arg{nofh__fnmsw}')
                ifi__ptly += f"""  out{nofh__fnmsw} = info_to_array(info_from_table(out_cpp_table, {vwu__mkyc}), {vplx__ddt})
"""
                tftsd__zdpeg.append(f'out{nofh__fnmsw}')
        ilzpr__vxcta = ',' if len(tftsd__zdpeg) == 1 else ''
        czx__wtqt = f"({', '.join(tftsd__zdpeg)}{ilzpr__vxcta})"
        ifi__ptly += f'  out_data = {czx__wtqt}\n'
    ifi__ptly += '  delete_table(out_cpp_table)\n'
    ifi__ptly += '  delete_table(in_cpp_table)\n'
    ifi__ptly += f'  return out_data\n'
    return ifi__ptly, {'in_col_inds': MetaType(tuple(yoqbv__wgvh)),
        'out_col_inds': MetaType(tuple(fljoj__wisxb))}


def _get_cpp_col_ind_mappings(key_inds, dead_var_inds, dead_key_var_inds,
    n_cols):
    yoqbv__wgvh = []
    fljoj__wisxb = []
    gfydk__iwe = []
    for yfok__xmd, nofh__fnmsw in enumerate(key_inds):
        yoqbv__wgvh.append(nofh__fnmsw)
        if nofh__fnmsw in dead_key_var_inds:
            gfydk__iwe.append(yfok__xmd)
        else:
            fljoj__wisxb.append(nofh__fnmsw)
    for nofh__fnmsw in range(n_cols):
        if nofh__fnmsw in dead_var_inds or nofh__fnmsw in key_inds:
            continue
        yoqbv__wgvh.append(nofh__fnmsw)
        fljoj__wisxb.append(nofh__fnmsw)
    return yoqbv__wgvh, fljoj__wisxb, gfydk__iwe


def sort_table_column_use(sort_node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    if not sort_node.is_table_format or sort_node.in_vars[0
        ] is None or sort_node.out_vars[0] is None:
        return
    wrcw__zpgf = sort_node.in_vars[0].name
    inbte__ett = sort_node.out_vars[0].name
    qbjp__nuwbd, qpa__trfug, bcs__xtj = block_use_map[wrcw__zpgf]
    if qpa__trfug or bcs__xtj:
        return
    car__aznb, ikdlc__twic, uwrj__uxe = _compute_table_column_uses(inbte__ett,
        table_col_use_map, equiv_vars)
    fpj__jdzu = set(nofh__fnmsw for nofh__fnmsw in sort_node.key_inds if 
        nofh__fnmsw < sort_node.num_table_arrays)
    block_use_map[wrcw__zpgf
        ] = qbjp__nuwbd | car__aznb | fpj__jdzu, ikdlc__twic or uwrj__uxe, False


ir_extension_table_column_use[Sort] = sort_table_column_use


def sort_remove_dead_column(sort_node, column_live_map, equiv_vars, typemap):
    if not sort_node.is_table_format or sort_node.out_vars[0] is None:
        return False
    lvm__wddoj = sort_node.num_table_arrays
    inbte__ett = sort_node.out_vars[0].name
    idz__wfegk = _find_used_columns(inbte__ett, lvm__wddoj, column_live_map,
        equiv_vars)
    if idz__wfegk is None:
        return False
    ffbjm__vxgh = set(range(lvm__wddoj)) - idz__wfegk
    fpj__jdzu = set(nofh__fnmsw for nofh__fnmsw in sort_node.key_inds if 
        nofh__fnmsw < lvm__wddoj)
    vywfo__txgb = sort_node.dead_key_var_inds | ffbjm__vxgh & fpj__jdzu
    hbrer__igvl = sort_node.dead_var_inds | ffbjm__vxgh - fpj__jdzu
    aqv__bjgya = (vywfo__txgb != sort_node.dead_key_var_inds) | (hbrer__igvl !=
        sort_node.dead_var_inds)
    sort_node.dead_key_var_inds = vywfo__txgb
    sort_node.dead_var_inds = hbrer__igvl
    return aqv__bjgya


remove_dead_column_extensions[Sort] = sort_remove_dead_column
