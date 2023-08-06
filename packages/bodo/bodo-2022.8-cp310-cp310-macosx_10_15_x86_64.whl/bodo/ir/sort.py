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
            self.na_position_b = tuple([(True if nlej__tdbnz == 'last' else
                False) for nlej__tdbnz in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_inds)
        self.ascending_list = ascending_list
        self.loc = loc

    def get_live_in_vars(self):
        return [rlf__lpfu for rlf__lpfu in self.in_vars if rlf__lpfu is not
            None]

    def get_live_out_vars(self):
        return [rlf__lpfu for rlf__lpfu in self.out_vars if rlf__lpfu is not
            None]

    def __repr__(self):
        fgpbk__lqi = ', '.join(rlf__lpfu.name for rlf__lpfu in self.
            get_live_in_vars())
        ijq__fccsu = f'{self.df_in}{{{fgpbk__lqi}}}'
        fsdm__monc = ', '.join(rlf__lpfu.name for rlf__lpfu in self.
            get_live_out_vars())
        tthi__pqfii = f'{self.df_out}{{{fsdm__monc}}}'
        return f'Sort (keys: {self.key_inds}): {ijq__fccsu} {tthi__pqfii}'


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    hdfw__ehisn = []
    for amj__xzqn in sort_node.get_live_in_vars():
        hkfhd__gzbo = equiv_set.get_shape(amj__xzqn)
        if hkfhd__gzbo is not None:
            hdfw__ehisn.append(hkfhd__gzbo[0])
    if len(hdfw__ehisn) > 1:
        equiv_set.insert_equiv(*hdfw__ehisn)
    qkc__kfcl = []
    hdfw__ehisn = []
    for amj__xzqn in sort_node.get_live_out_vars():
        mzo__cvt = typemap[amj__xzqn.name]
        ghjw__qsved = array_analysis._gen_shape_call(equiv_set, amj__xzqn,
            mzo__cvt.ndim, None, qkc__kfcl)
        equiv_set.insert_equiv(amj__xzqn, ghjw__qsved)
        hdfw__ehisn.append(ghjw__qsved[0])
        equiv_set.define(amj__xzqn, set())
    if len(hdfw__ehisn) > 1:
        equiv_set.insert_equiv(*hdfw__ehisn)
    return [], qkc__kfcl


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    gmyq__yrohv = sort_node.get_live_in_vars()
    xmxj__oosiz = sort_node.get_live_out_vars()
    jnjj__acpn = Distribution.OneD
    for amj__xzqn in gmyq__yrohv:
        jnjj__acpn = Distribution(min(jnjj__acpn.value, array_dists[
            amj__xzqn.name].value))
    cxj__ojtlm = Distribution(min(jnjj__acpn.value, Distribution.OneD_Var.
        value))
    for amj__xzqn in xmxj__oosiz:
        if amj__xzqn.name in array_dists:
            cxj__ojtlm = Distribution(min(cxj__ojtlm.value, array_dists[
                amj__xzqn.name].value))
    if cxj__ojtlm != Distribution.OneD_Var:
        jnjj__acpn = cxj__ojtlm
    for amj__xzqn in gmyq__yrohv:
        array_dists[amj__xzqn.name] = jnjj__acpn
    for amj__xzqn in xmxj__oosiz:
        array_dists[amj__xzqn.name] = cxj__ojtlm


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for toclp__zelwl, biyvk__vdy in enumerate(sort_node.out_vars):
        soi__ffe = sort_node.in_vars[toclp__zelwl]
        if soi__ffe is not None and biyvk__vdy is not None:
            typeinferer.constraints.append(typeinfer.Propagate(dst=
                biyvk__vdy.name, src=soi__ffe.name, loc=sort_node.loc))


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for amj__xzqn in sort_node.get_live_out_vars():
            definitions[amj__xzqn.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    for toclp__zelwl in range(len(sort_node.in_vars)):
        if sort_node.in_vars[toclp__zelwl] is not None:
            sort_node.in_vars[toclp__zelwl] = visit_vars_inner(sort_node.
                in_vars[toclp__zelwl], callback, cbdata)
        if sort_node.out_vars[toclp__zelwl] is not None:
            sort_node.out_vars[toclp__zelwl] = visit_vars_inner(sort_node.
                out_vars[toclp__zelwl], callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if sort_node.is_table_format:
        nacs__tkq = sort_node.out_vars[0]
        if nacs__tkq is not None and nacs__tkq.name not in lives:
            sort_node.out_vars[0] = None
            dead_cols = set(range(sort_node.num_table_arrays))
            pbap__rjql = set(sort_node.key_inds)
            sort_node.dead_key_var_inds.update(dead_cols & pbap__rjql)
            sort_node.dead_var_inds.update(dead_cols - pbap__rjql)
            if len(pbap__rjql & dead_cols) == 0:
                sort_node.in_vars[0] = None
        for toclp__zelwl in range(1, len(sort_node.out_vars)):
            rlf__lpfu = sort_node.out_vars[toclp__zelwl]
            if rlf__lpfu is not None and rlf__lpfu.name not in lives:
                sort_node.out_vars[toclp__zelwl] = None
                yaspl__auyg = sort_node.num_table_arrays + toclp__zelwl - 1
                if yaspl__auyg in sort_node.key_inds:
                    sort_node.dead_key_var_inds.add(yaspl__auyg)
                else:
                    sort_node.dead_var_inds.add(yaspl__auyg)
                    sort_node.in_vars[toclp__zelwl] = None
    else:
        for toclp__zelwl in range(len(sort_node.out_vars)):
            rlf__lpfu = sort_node.out_vars[toclp__zelwl]
            if rlf__lpfu is not None and rlf__lpfu.name not in lives:
                sort_node.out_vars[toclp__zelwl] = None
                if toclp__zelwl in sort_node.key_inds:
                    sort_node.dead_key_var_inds.add(toclp__zelwl)
                else:
                    sort_node.dead_var_inds.add(toclp__zelwl)
                    sort_node.in_vars[toclp__zelwl] = None
    if all(rlf__lpfu is None for rlf__lpfu in sort_node.out_vars):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({rlf__lpfu.name for rlf__lpfu in sort_node.
        get_live_in_vars()})
    if not sort_node.inplace:
        def_set.update({rlf__lpfu.name for rlf__lpfu in sort_node.
            get_live_out_vars()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    upga__lrgsa = set()
    if not sort_node.inplace:
        upga__lrgsa.update({rlf__lpfu.name for rlf__lpfu in sort_node.
            get_live_out_vars()})
    return set(), upga__lrgsa


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for toclp__zelwl in range(len(sort_node.in_vars)):
        if sort_node.in_vars[toclp__zelwl] is not None:
            sort_node.in_vars[toclp__zelwl] = replace_vars_inner(sort_node.
                in_vars[toclp__zelwl], var_dict)
        if sort_node.out_vars[toclp__zelwl] is not None:
            sort_node.out_vars[toclp__zelwl] = replace_vars_inner(sort_node
                .out_vars[toclp__zelwl], var_dict)


ir_utils.apply_copy_propagate_extensions[Sort] = apply_copies_sort


def sort_distributed_run(sort_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    parallel = False
    in_vars = sort_node.get_live_in_vars()
    out_vars = sort_node.get_live_out_vars()
    if array_dists is not None:
        parallel = True
        for rlf__lpfu in (in_vars + out_vars):
            if array_dists[rlf__lpfu.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                rlf__lpfu.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    nodes = []
    if not sort_node.inplace:
        inpy__nwsy = []
        for rlf__lpfu in in_vars:
            pujs__jiakk = _copy_array_nodes(rlf__lpfu, nodes, typingctx,
                targetctx, typemap, calltypes, sort_node.dead_var_inds)
            inpy__nwsy.append(pujs__jiakk)
        in_vars = inpy__nwsy
    out_types = [(typemap[rlf__lpfu.name] if rlf__lpfu is not None else
        types.none) for rlf__lpfu in sort_node.out_vars]
    eectx__sgtw, jzrjn__qhpc = get_sort_cpp_section(sort_node, out_types,
        parallel)
    scvi__dgfi = {}
    exec(eectx__sgtw, {}, scvi__dgfi)
    uykw__dktt = scvi__dgfi['f']
    jzrjn__qhpc.update({'bodo': bodo, 'np': np, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'sort_values_table':
        sort_values_table, 'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info, 'py_data_to_cpp_table':
        py_data_to_cpp_table, 'cpp_table_to_py_data': cpp_table_to_py_data})
    jzrjn__qhpc.update({f'out_type{toclp__zelwl}': out_types[toclp__zelwl] for
        toclp__zelwl in range(len(out_types))})
    smpg__mwal = compile_to_numba_ir(uykw__dktt, jzrjn__qhpc, typingctx=
        typingctx, targetctx=targetctx, arg_typs=tuple(typemap[rlf__lpfu.
        name] for rlf__lpfu in in_vars), typemap=typemap, calltypes=calltypes
        ).blocks.popitem()[1]
    replace_arg_nodes(smpg__mwal, in_vars)
    jze__dfrpc = smpg__mwal.body[-2].value.value
    nodes += smpg__mwal.body[:-2]
    for toclp__zelwl, rlf__lpfu in enumerate(out_vars):
        gen_getitem(rlf__lpfu, jze__dfrpc, toclp__zelwl, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes,
    dead_cols):
    from bodo.hiframes.table import TableType
    ncq__zhz = lambda arr: arr.copy()
    zytm__jesec = None
    if isinstance(typemap[var.name], TableType):
        vmcp__cuy = len(typemap[var.name].arr_types)
        zytm__jesec = set(range(vmcp__cuy)) - dead_cols
        zytm__jesec = MetaType(tuple(sorted(zytm__jesec)))
        ncq__zhz = (lambda T: bodo.utils.table_utils.
            generate_mappable_table_func(T, 'copy', types.none, True,
            used_cols=_used_columns))
    smpg__mwal = compile_to_numba_ir(ncq__zhz, {'bodo': bodo, 'types':
        types, '_used_columns': zytm__jesec}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(smpg__mwal, [var])
    nodes += smpg__mwal.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(sort_node, out_types, parallel):
    yju__whjb = len(sort_node.key_inds)
    ivt__tauxa = len(sort_node.in_vars)
    jsi__clkg = len(sort_node.out_vars)
    n_cols = (sort_node.num_table_arrays + ivt__tauxa - 1 if sort_node.
        is_table_format else ivt__tauxa)
    iuf__lldfi, gphhw__ltaf, rogo__gzpi = _get_cpp_col_ind_mappings(sort_node
        .key_inds, sort_node.dead_var_inds, sort_node.dead_key_var_inds, n_cols
        )
    poeb__arf = []
    if sort_node.is_table_format:
        poeb__arf.append('arg0')
        for toclp__zelwl in range(1, ivt__tauxa):
            yaspl__auyg = sort_node.num_table_arrays + toclp__zelwl - 1
            if yaspl__auyg not in sort_node.dead_var_inds:
                poeb__arf.append(f'arg{yaspl__auyg}')
    else:
        for toclp__zelwl in range(n_cols):
            if toclp__zelwl not in sort_node.dead_var_inds:
                poeb__arf.append(f'arg{toclp__zelwl}')
    eectx__sgtw = f"def f({', '.join(poeb__arf)}):\n"
    if sort_node.is_table_format:
        eqqhw__tgs = ',' if ivt__tauxa - 1 == 1 else ''
        bevzl__kqxt = []
        for toclp__zelwl in range(sort_node.num_table_arrays, n_cols):
            if toclp__zelwl in sort_node.dead_var_inds:
                bevzl__kqxt.append('None')
            else:
                bevzl__kqxt.append(f'arg{toclp__zelwl}')
        eectx__sgtw += f"""  in_cpp_table = py_data_to_cpp_table(arg0, ({', '.join(bevzl__kqxt)}{eqqhw__tgs}), in_col_inds, {sort_node.num_table_arrays})
"""
    else:
        xobv__nouzu = {hwf__dsjfj: toclp__zelwl for toclp__zelwl,
            hwf__dsjfj in enumerate(iuf__lldfi)}
        buto__qvc = [None] * len(iuf__lldfi)
        for toclp__zelwl in range(n_cols):
            xeevz__txdnw = xobv__nouzu.get(toclp__zelwl, -1)
            if xeevz__txdnw != -1:
                buto__qvc[xeevz__txdnw] = f'array_to_info(arg{toclp__zelwl})'
        eectx__sgtw += '  info_list_total = [{}]\n'.format(','.join(buto__qvc))
        eectx__sgtw += (
            '  in_cpp_table = arr_info_list_to_table(info_list_total)\n')
    eectx__sgtw += '  vect_ascending = np.array([{}], np.int64)\n'.format(','
        .join('1' if pvx__zohtn else '0' for pvx__zohtn in sort_node.
        ascending_list))
    eectx__sgtw += '  na_position = np.array([{}], np.int64)\n'.format(','.
        join('1' if pvx__zohtn else '0' for pvx__zohtn in sort_node.
        na_position_b))
    eectx__sgtw += '  dead_keys = np.array([{}], np.int64)\n'.format(','.
        join('1' if toclp__zelwl in rogo__gzpi else '0' for toclp__zelwl in
        range(yju__whjb)))
    eectx__sgtw += f'  total_rows_np = np.array([0], dtype=np.int64)\n'
    eectx__sgtw += f"""  out_cpp_table = sort_values_table(in_cpp_table, {yju__whjb}, vect_ascending.ctypes, na_position.ctypes, dead_keys.ctypes, total_rows_np.ctypes, {parallel})
"""
    if sort_node.is_table_format:
        eqqhw__tgs = ',' if jsi__clkg == 1 else ''
        utydh__wybxj = (
            f"({', '.join(f'out_type{toclp__zelwl}' if not type_has_unknown_cats(out_types[toclp__zelwl]) else f'arg{toclp__zelwl}' for toclp__zelwl in range(jsi__clkg))}{eqqhw__tgs})"
            )
        eectx__sgtw += f"""  out_data = cpp_table_to_py_data(out_cpp_table, out_col_inds, {utydh__wybxj}, total_rows_np[0], {sort_node.num_table_arrays})
"""
    else:
        xobv__nouzu = {hwf__dsjfj: toclp__zelwl for toclp__zelwl,
            hwf__dsjfj in enumerate(gphhw__ltaf)}
        buto__qvc = []
        for toclp__zelwl in range(n_cols):
            xeevz__txdnw = xobv__nouzu.get(toclp__zelwl, -1)
            if xeevz__txdnw != -1:
                ozpw__tktq = (f'out_type{toclp__zelwl}' if not
                    type_has_unknown_cats(out_types[toclp__zelwl]) else
                    f'arg{toclp__zelwl}')
                eectx__sgtw += f"""  out{toclp__zelwl} = info_to_array(info_from_table(out_cpp_table, {xeevz__txdnw}), {ozpw__tktq})
"""
                buto__qvc.append(f'out{toclp__zelwl}')
        eqqhw__tgs = ',' if len(buto__qvc) == 1 else ''
        biso__scgc = f"({', '.join(buto__qvc)}{eqqhw__tgs})"
        eectx__sgtw += f'  out_data = {biso__scgc}\n'
    eectx__sgtw += '  delete_table(out_cpp_table)\n'
    eectx__sgtw += '  delete_table(in_cpp_table)\n'
    eectx__sgtw += f'  return out_data\n'
    return eectx__sgtw, {'in_col_inds': MetaType(tuple(iuf__lldfi)),
        'out_col_inds': MetaType(tuple(gphhw__ltaf))}


def _get_cpp_col_ind_mappings(key_inds, dead_var_inds, dead_key_var_inds,
    n_cols):
    iuf__lldfi = []
    gphhw__ltaf = []
    rogo__gzpi = []
    for hwf__dsjfj, toclp__zelwl in enumerate(key_inds):
        iuf__lldfi.append(toclp__zelwl)
        if toclp__zelwl in dead_key_var_inds:
            rogo__gzpi.append(hwf__dsjfj)
        else:
            gphhw__ltaf.append(toclp__zelwl)
    for toclp__zelwl in range(n_cols):
        if toclp__zelwl in dead_var_inds or toclp__zelwl in key_inds:
            continue
        iuf__lldfi.append(toclp__zelwl)
        gphhw__ltaf.append(toclp__zelwl)
    return iuf__lldfi, gphhw__ltaf, rogo__gzpi


def sort_table_column_use(sort_node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    if not sort_node.is_table_format or sort_node.in_vars[0
        ] is None or sort_node.out_vars[0] is None:
        return
    grxm__yoza = sort_node.in_vars[0].name
    gaebh__juikk = sort_node.out_vars[0].name
    mrhwz__hvfx, bom__eyd, yif__csy = block_use_map[grxm__yoza]
    if bom__eyd or yif__csy:
        return
    hxqxu__rsz, hwiv__qrevh, nnuj__xxw = _compute_table_column_uses(
        gaebh__juikk, table_col_use_map, equiv_vars)
    wdwyd__lzqsi = set(toclp__zelwl for toclp__zelwl in sort_node.key_inds if
        toclp__zelwl < sort_node.num_table_arrays)
    block_use_map[grxm__yoza] = (mrhwz__hvfx | hxqxu__rsz | wdwyd__lzqsi, 
        hwiv__qrevh or nnuj__xxw, False)


ir_extension_table_column_use[Sort] = sort_table_column_use


def sort_remove_dead_column(sort_node, column_live_map, equiv_vars, typemap):
    if not sort_node.is_table_format or sort_node.out_vars[0] is None:
        return False
    vmcp__cuy = sort_node.num_table_arrays
    gaebh__juikk = sort_node.out_vars[0].name
    zytm__jesec = _find_used_columns(gaebh__juikk, vmcp__cuy,
        column_live_map, equiv_vars)
    if zytm__jesec is None:
        return False
    uivjc__qyrge = set(range(vmcp__cuy)) - zytm__jesec
    wdwyd__lzqsi = set(toclp__zelwl for toclp__zelwl in sort_node.key_inds if
        toclp__zelwl < vmcp__cuy)
    pgk__uihfc = sort_node.dead_key_var_inds | uivjc__qyrge & wdwyd__lzqsi
    sde__petei = sort_node.dead_var_inds | uivjc__qyrge - wdwyd__lzqsi
    nsvf__szl = (pgk__uihfc != sort_node.dead_key_var_inds) | (sde__petei !=
        sort_node.dead_var_inds)
    sort_node.dead_key_var_inds = pgk__uihfc
    sort_node.dead_var_inds = sde__petei
    return nsvf__szl


remove_dead_column_extensions[Sort] = sort_remove_dead_column
