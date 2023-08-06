"""IR node for the join and merge"""
from collections import defaultdict
from typing import Dict, List, Literal, Optional, Set, Tuple, Union
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir, ir_utils, types
from numba.core.ir_utils import compile_to_numba_ir, next_label, replace_arg_nodes, replace_vars_inner, visit_vars_inner
from numba.extending import intrinsic
import bodo
from bodo.hiframes.table import TableType
from bodo.ir.connector import trim_extra_used_columns
from bodo.libs.array import arr_info_list_to_table, array_to_info, cpp_table_to_py_data, delete_table, hash_join_table, py_data_to_cpp_table
from bodo.libs.timsort import getitem_arr_tup, setitem_arr_tup
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.transforms.table_column_del_pass import _compute_table_column_uses, get_live_column_nums_block, ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import INDEX_SENTINEL, BodoError, MetaType, dtype_to_array_type, find_common_np_dtype, is_dtype_nullable, is_nullable_type, is_str_arr_type, to_nullable_type
from bodo.utils.utils import alloc_arr_tup, is_null_pointer
join_gen_cond_cfunc = {}
join_gen_cond_cfunc_addr = {}


@intrinsic
def add_join_gen_cond_cfunc_sym(typingctx, func, sym):

    def codegen(context, builder, signature, args):
        tyx__hjzq = func.signature
        gwlvc__pfw = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        siu__bja = cgutils.get_or_insert_function(builder.module,
            gwlvc__pfw, sym._literal_value)
        builder.call(siu__bja, [context.get_constant_null(tyx__hjzq.args[0]
            ), context.get_constant_null(tyx__hjzq.args[1]), context.
            get_constant_null(tyx__hjzq.args[2]), context.get_constant_null
            (tyx__hjzq.args[3]), context.get_constant_null(tyx__hjzq.args[4
            ]), context.get_constant_null(tyx__hjzq.args[5]), context.
            get_constant(types.int64, 0), context.get_constant(types.int64, 0)]
            )
        context.add_linking_libs([join_gen_cond_cfunc[sym._literal_value].
            _library])
        return
    return types.none(func, sym), codegen


@numba.jit
def get_join_cond_addr(name):
    with numba.objmode(addr='int64'):
        addr = join_gen_cond_cfunc_addr[name]
    return addr


HOW_OPTIONS = Literal['inner', 'left', 'right', 'outer', 'asof']


class Join(ir.Stmt):

    def __init__(self, left_keys: Union[List[str], str], right_keys: Union[
        List[str], str], out_data_vars: List[ir.Var], out_df_type: bodo.
        DataFrameType, left_vars: List[ir.Var], left_df_type: bodo.
        DataFrameType, right_vars: List[ir.Var], right_df_type: bodo.
        DataFrameType, how: HOW_OPTIONS, suffix_left: str, suffix_right:
        str, loc: ir.Loc, is_left: bool, is_right: bool, is_join: bool,
        left_index: bool, right_index: bool, indicator_col_num: int,
        is_na_equal: bool, gen_cond_expr: str):
        self.left_keys = left_keys
        self.right_keys = right_keys
        self.out_data_vars = out_data_vars
        self.out_col_names = out_df_type.columns
        self.left_vars = left_vars
        self.right_vars = right_vars
        self.how = how
        self.loc = loc
        self.is_left = is_left
        self.is_right = is_right
        self.is_join = is_join
        self.left_index = left_index
        self.right_index = right_index
        self.indicator_col_num = indicator_col_num
        self.is_na_equal = is_na_equal
        self.gen_cond_expr = gen_cond_expr
        self.n_out_table_cols = len(self.out_col_names)
        self.out_used_cols = set(range(self.n_out_table_cols))
        if self.out_data_vars[1] is not None:
            self.out_used_cols.add(self.n_out_table_cols)
        ulqc__rtn = left_df_type.columns
        amk__ktq = right_df_type.columns
        self.left_col_names = ulqc__rtn
        self.right_col_names = amk__ktq
        self.is_left_table = left_df_type.is_table_format
        self.is_right_table = right_df_type.is_table_format
        self.n_left_table_cols = len(ulqc__rtn) if self.is_left_table else 0
        self.n_right_table_cols = len(amk__ktq) if self.is_right_table else 0
        yyvpo__cju = self.n_left_table_cols if self.is_left_table else len(
            left_vars) - 1
        kcfy__onh = self.n_right_table_cols if self.is_right_table else len(
            right_vars) - 1
        self.left_dead_var_inds = set()
        self.right_dead_var_inds = set()
        if self.left_vars[-1] is None:
            self.left_dead_var_inds.add(yyvpo__cju)
        if self.right_vars[-1] is None:
            self.right_dead_var_inds.add(kcfy__onh)
        self.left_var_map = {wgawe__oclj: jhhmw__zuz for jhhmw__zuz,
            wgawe__oclj in enumerate(ulqc__rtn)}
        self.right_var_map = {wgawe__oclj: jhhmw__zuz for jhhmw__zuz,
            wgawe__oclj in enumerate(amk__ktq)}
        if self.left_vars[-1] is not None:
            self.left_var_map[INDEX_SENTINEL] = yyvpo__cju
        if self.right_vars[-1] is not None:
            self.right_var_map[INDEX_SENTINEL] = kcfy__onh
        self.left_key_set = set(self.left_var_map[wgawe__oclj] for
            wgawe__oclj in left_keys)
        self.right_key_set = set(self.right_var_map[wgawe__oclj] for
            wgawe__oclj in right_keys)
        if gen_cond_expr:
            self.left_cond_cols = set(self.left_var_map[wgawe__oclj] for
                wgawe__oclj in ulqc__rtn if f'(left.{wgawe__oclj})' in
                gen_cond_expr)
            self.right_cond_cols = set(self.right_var_map[wgawe__oclj] for
                wgawe__oclj in amk__ktq if f'(right.{wgawe__oclj})' in
                gen_cond_expr)
        else:
            self.left_cond_cols = set()
            self.right_cond_cols = set()
        ovqb__nudzm: int = -1
        tzdxk__fmem = set(left_keys) & set(right_keys)
        ias__yjuxs = set(ulqc__rtn) & set(amk__ktq)
        ulpqf__hydq = ias__yjuxs - tzdxk__fmem
        sgcn__ulm: Dict[int, (Literal['left', 'right'], int)] = {}
        aojey__irjr: Dict[int, int] = {}
        tivj__qtfge: Dict[int, int] = {}
        for jhhmw__zuz, wgawe__oclj in enumerate(ulqc__rtn):
            if wgawe__oclj in ulpqf__hydq:
                nxohd__yhi = str(wgawe__oclj) + suffix_left
                qtdta__hwrbv = out_df_type.column_index[nxohd__yhi]
                if (right_index and not left_index and jhhmw__zuz in self.
                    left_key_set):
                    ovqb__nudzm = out_df_type.column_index[wgawe__oclj]
                    sgcn__ulm[ovqb__nudzm] = 'left', jhhmw__zuz
            else:
                qtdta__hwrbv = out_df_type.column_index[wgawe__oclj]
            sgcn__ulm[qtdta__hwrbv] = 'left', jhhmw__zuz
            aojey__irjr[jhhmw__zuz] = qtdta__hwrbv
        for jhhmw__zuz, wgawe__oclj in enumerate(amk__ktq):
            if wgawe__oclj not in tzdxk__fmem:
                if wgawe__oclj in ulpqf__hydq:
                    rgxli__tjq = str(wgawe__oclj) + suffix_right
                    qtdta__hwrbv = out_df_type.column_index[rgxli__tjq]
                    if (left_index and not right_index and jhhmw__zuz in
                        self.right_key_set):
                        ovqb__nudzm = out_df_type.column_index[wgawe__oclj]
                        sgcn__ulm[ovqb__nudzm] = 'right', jhhmw__zuz
                else:
                    qtdta__hwrbv = out_df_type.column_index[wgawe__oclj]
                sgcn__ulm[qtdta__hwrbv] = 'right', jhhmw__zuz
                tivj__qtfge[jhhmw__zuz] = qtdta__hwrbv
        if self.left_vars[-1] is not None:
            aojey__irjr[yyvpo__cju] = self.n_out_table_cols
        if self.right_vars[-1] is not None:
            tivj__qtfge[kcfy__onh] = self.n_out_table_cols
        self.out_to_input_col_map = sgcn__ulm
        self.left_to_output_map = aojey__irjr
        self.right_to_output_map = tivj__qtfge
        self.extra_data_col_num = ovqb__nudzm
        if len(out_data_vars) > 1:
            vjgj__peoa = 'left' if right_index else 'right'
            if vjgj__peoa == 'left':
                pgo__iqlz = yyvpo__cju
            elif vjgj__peoa == 'right':
                pgo__iqlz = kcfy__onh
        else:
            vjgj__peoa = None
            pgo__iqlz = -1
        self.index_source = vjgj__peoa
        self.index_col_num = pgo__iqlz
        bdjof__ncd = []
        ejs__zte = len(left_keys)
        for qzr__tys in range(ejs__zte):
            obm__gdc = left_keys[qzr__tys]
            gejqn__obyeo = right_keys[qzr__tys]
            bdjof__ncd.append(obm__gdc == gejqn__obyeo)
        self.vect_same_key = bdjof__ncd

    @property
    def has_live_left_table_var(self):
        return self.is_left_table and self.left_vars[0] is not None

    @property
    def has_live_right_table_var(self):
        return self.is_right_table and self.right_vars[0] is not None

    @property
    def has_live_out_table_var(self):
        return self.out_data_vars[0] is not None

    @property
    def has_live_out_index_var(self):
        return self.out_data_vars[1] is not None

    def get_out_table_var(self):
        return self.out_data_vars[0]

    def get_out_index_var(self):
        return self.out_data_vars[1]

    def get_live_left_vars(self):
        vars = []
        for hpies__rzjzm in self.left_vars:
            if hpies__rzjzm is not None:
                vars.append(hpies__rzjzm)
        return vars

    def get_live_right_vars(self):
        vars = []
        for hpies__rzjzm in self.right_vars:
            if hpies__rzjzm is not None:
                vars.append(hpies__rzjzm)
        return vars

    def get_live_out_vars(self):
        vars = []
        for hpies__rzjzm in self.out_data_vars:
            if hpies__rzjzm is not None:
                vars.append(hpies__rzjzm)
        return vars

    def set_live_left_vars(self, live_data_vars):
        left_vars = []
        manj__ydvw = 0
        start = 0
        if self.is_left_table:
            if self.has_live_left_table_var:
                left_vars.append(live_data_vars[manj__ydvw])
                manj__ydvw += 1
            else:
                left_vars.append(None)
            start = 1
        umy__llbtv = max(self.n_left_table_cols - 1, 0)
        for jhhmw__zuz in range(start, len(self.left_vars)):
            if jhhmw__zuz + umy__llbtv in self.left_dead_var_inds:
                left_vars.append(None)
            else:
                left_vars.append(live_data_vars[manj__ydvw])
                manj__ydvw += 1
        self.left_vars = left_vars

    def set_live_right_vars(self, live_data_vars):
        right_vars = []
        manj__ydvw = 0
        start = 0
        if self.is_right_table:
            if self.has_live_right_table_var:
                right_vars.append(live_data_vars[manj__ydvw])
                manj__ydvw += 1
            else:
                right_vars.append(None)
            start = 1
        umy__llbtv = max(self.n_right_table_cols - 1, 0)
        for jhhmw__zuz in range(start, len(self.right_vars)):
            if jhhmw__zuz + umy__llbtv in self.right_dead_var_inds:
                right_vars.append(None)
            else:
                right_vars.append(live_data_vars[manj__ydvw])
                manj__ydvw += 1
        self.right_vars = right_vars

    def set_live_out_data_vars(self, live_data_vars):
        out_data_vars = []
        spise__mrdk = [self.has_live_out_table_var, self.has_live_out_index_var
            ]
        manj__ydvw = 0
        for jhhmw__zuz in range(len(self.out_data_vars)):
            if not spise__mrdk[jhhmw__zuz]:
                out_data_vars.append(None)
            else:
                out_data_vars.append(live_data_vars[manj__ydvw])
                manj__ydvw += 1
        self.out_data_vars = out_data_vars

    def get_out_table_used_cols(self):
        return {jhhmw__zuz for jhhmw__zuz in self.out_used_cols if 
            jhhmw__zuz < self.n_out_table_cols}

    def __repr__(self):
        rwasr__xioe = ', '.join([f'{wgawe__oclj}' for wgawe__oclj in self.
            left_col_names])
        uytpa__zjkbf = f'left={{{rwasr__xioe}}}'
        rwasr__xioe = ', '.join([f'{wgawe__oclj}' for wgawe__oclj in self.
            right_col_names])
        ldva__muk = f'right={{{rwasr__xioe}}}'
        return 'join [{}={}]: {}, {}'.format(self.left_keys, self.
            right_keys, uytpa__zjkbf, ldva__muk)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    qcq__ravn = []
    assert len(join_node.get_live_out_vars()
        ) > 0, 'empty join in array analysis'
    hkf__jxzf = []
    axj__xqg = join_node.get_live_left_vars()
    for mdjsf__pcs in axj__xqg:
        yadq__yicdo = typemap[mdjsf__pcs.name]
        qzsav__xyt = equiv_set.get_shape(mdjsf__pcs)
        if qzsav__xyt:
            hkf__jxzf.append(qzsav__xyt[0])
    if len(hkf__jxzf) > 1:
        equiv_set.insert_equiv(*hkf__jxzf)
    hkf__jxzf = []
    axj__xqg = list(join_node.get_live_right_vars())
    for mdjsf__pcs in axj__xqg:
        yadq__yicdo = typemap[mdjsf__pcs.name]
        qzsav__xyt = equiv_set.get_shape(mdjsf__pcs)
        if qzsav__xyt:
            hkf__jxzf.append(qzsav__xyt[0])
    if len(hkf__jxzf) > 1:
        equiv_set.insert_equiv(*hkf__jxzf)
    hkf__jxzf = []
    for jzbz__igm in join_node.get_live_out_vars():
        yadq__yicdo = typemap[jzbz__igm.name]
        vzweh__bavit = array_analysis._gen_shape_call(equiv_set, jzbz__igm,
            yadq__yicdo.ndim, None, qcq__ravn)
        equiv_set.insert_equiv(jzbz__igm, vzweh__bavit)
        hkf__jxzf.append(vzweh__bavit[0])
        equiv_set.define(jzbz__igm, set())
    if len(hkf__jxzf) > 1:
        equiv_set.insert_equiv(*hkf__jxzf)
    return [], qcq__ravn


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    uppf__grv = Distribution.OneD
    ugq__fgyn = Distribution.OneD
    for mdjsf__pcs in join_node.get_live_left_vars():
        uppf__grv = Distribution(min(uppf__grv.value, array_dists[
            mdjsf__pcs.name].value))
    for mdjsf__pcs in join_node.get_live_right_vars():
        ugq__fgyn = Distribution(min(ugq__fgyn.value, array_dists[
            mdjsf__pcs.name].value))
    xbq__poos = Distribution.OneD_Var
    for jzbz__igm in join_node.get_live_out_vars():
        if jzbz__igm.name in array_dists:
            xbq__poos = Distribution(min(xbq__poos.value, array_dists[
                jzbz__igm.name].value))
    uxqe__ymir = Distribution(min(xbq__poos.value, uppf__grv.value))
    pmy__lzcsx = Distribution(min(xbq__poos.value, ugq__fgyn.value))
    xbq__poos = Distribution(max(uxqe__ymir.value, pmy__lzcsx.value))
    for jzbz__igm in join_node.get_live_out_vars():
        array_dists[jzbz__igm.name] = xbq__poos
    if xbq__poos != Distribution.OneD_Var:
        uppf__grv = xbq__poos
        ugq__fgyn = xbq__poos
    for mdjsf__pcs in join_node.get_live_left_vars():
        array_dists[mdjsf__pcs.name] = uppf__grv
    for mdjsf__pcs in join_node.get_live_right_vars():
        array_dists[mdjsf__pcs.name] = ugq__fgyn
    return


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def visit_vars_join(join_node, callback, cbdata):
    join_node.set_live_left_vars([visit_vars_inner(hpies__rzjzm, callback,
        cbdata) for hpies__rzjzm in join_node.get_live_left_vars()])
    join_node.set_live_right_vars([visit_vars_inner(hpies__rzjzm, callback,
        cbdata) for hpies__rzjzm in join_node.get_live_right_vars()])
    join_node.set_live_out_data_vars([visit_vars_inner(hpies__rzjzm,
        callback, cbdata) for hpies__rzjzm in join_node.get_live_out_vars()])


ir_utils.visit_vars_extensions[Join] = visit_vars_join


def remove_dead_join(join_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if join_node.has_live_out_table_var:
        ngcog__ilu = []
        dema__yxfq = join_node.get_out_table_var()
        if dema__yxfq.name not in lives:
            join_node.out_data_vars[0] = None
            join_node.out_used_cols.difference_update(join_node.
                get_out_table_used_cols())
        for rost__zulir in join_node.out_to_input_col_map.keys():
            if rost__zulir in join_node.out_used_cols:
                continue
            ngcog__ilu.append(rost__zulir)
            if join_node.indicator_col_num == rost__zulir:
                join_node.indicator_col_num = -1
                continue
            if rost__zulir == join_node.extra_data_col_num:
                join_node.extra_data_col_num = -1
                continue
            pybq__kcj, rost__zulir = join_node.out_to_input_col_map[rost__zulir
                ]
            if pybq__kcj == 'left':
                if (rost__zulir not in join_node.left_key_set and 
                    rost__zulir not in join_node.left_cond_cols):
                    join_node.left_dead_var_inds.add(rost__zulir)
                    if not join_node.is_left_table:
                        join_node.left_vars[rost__zulir] = None
            elif pybq__kcj == 'right':
                if (rost__zulir not in join_node.right_key_set and 
                    rost__zulir not in join_node.right_cond_cols):
                    join_node.right_dead_var_inds.add(rost__zulir)
                    if not join_node.is_right_table:
                        join_node.right_vars[rost__zulir] = None
        for jhhmw__zuz in ngcog__ilu:
            del join_node.out_to_input_col_map[jhhmw__zuz]
        if join_node.is_left_table:
            zhrb__jxbce = set(range(join_node.n_left_table_cols))
            qlutu__lwiq = not bool(zhrb__jxbce - join_node.left_dead_var_inds)
            if qlutu__lwiq:
                join_node.left_vars[0] = None
        if join_node.is_right_table:
            zhrb__jxbce = set(range(join_node.n_right_table_cols))
            qlutu__lwiq = not bool(zhrb__jxbce - join_node.right_dead_var_inds)
            if qlutu__lwiq:
                join_node.right_vars[0] = None
    if join_node.has_live_out_index_var:
        hhlbg__chdai = join_node.get_out_index_var()
        if hhlbg__chdai.name not in lives:
            join_node.out_data_vars[1] = None
            join_node.out_used_cols.remove(join_node.n_out_table_cols)
            if join_node.index_source == 'left':
                if (join_node.index_col_num not in join_node.left_key_set and
                    join_node.index_col_num not in join_node.left_cond_cols):
                    join_node.left_dead_var_inds.add(join_node.index_col_num)
                    join_node.left_vars[-1] = None
            elif join_node.index_col_num not in join_node.right_key_set and join_node.index_col_num not in join_node.right_cond_cols:
                join_node.right_dead_var_inds.add(join_node.index_col_num)
                join_node.right_vars[-1] = None
    if not (join_node.has_live_out_table_var or join_node.
        has_live_out_index_var):
        return None
    return join_node


ir_utils.remove_dead_extensions[Join] = remove_dead_join


def join_remove_dead_column(join_node, column_live_map, equiv_vars, typemap):
    kpax__qgs = False
    if join_node.has_live_out_table_var:
        xtwq__qvlg = join_node.get_out_table_var().name
        efhv__cqg, lcmcl__qxnpm, uaame__gdc = get_live_column_nums_block(
            column_live_map, equiv_vars, xtwq__qvlg)
        if not (lcmcl__qxnpm or uaame__gdc):
            efhv__cqg = trim_extra_used_columns(efhv__cqg, join_node.
                n_out_table_cols)
            cvvfs__kzi = join_node.get_out_table_used_cols()
            if len(efhv__cqg) != len(cvvfs__kzi):
                kpax__qgs = not (join_node.is_left_table and join_node.
                    is_right_table)
                zgfkw__lpu = cvvfs__kzi - efhv__cqg
                join_node.out_used_cols = join_node.out_used_cols - zgfkw__lpu
    return kpax__qgs


remove_dead_column_extensions[Join] = join_remove_dead_column


def join_table_column_use(join_node: Join, block_use_map: Dict[str, Tuple[
    Set[int], bool, bool]], equiv_vars: Dict[str, Set[str]], typemap: Dict[
    str, types.Type], table_col_use_map: Dict[int, Dict[str, Tuple[Set[int],
    bool, bool]]]):
    if not (join_node.is_left_table or join_node.is_right_table):
        return
    if join_node.has_live_out_table_var:
        hwjmq__dndop = join_node.get_out_table_var()
        xvyqo__yfes, lcmcl__qxnpm, uaame__gdc = _compute_table_column_uses(
            hwjmq__dndop.name, table_col_use_map, equiv_vars)
    else:
        xvyqo__yfes, lcmcl__qxnpm, uaame__gdc = set(), False, False
    if join_node.has_live_left_table_var:
        ybjn__tmsp = join_node.left_vars[0].name
        qogf__nnysy, mmqu__ivxni, iwlyd__ncqab = block_use_map[ybjn__tmsp]
        if not (mmqu__ivxni or iwlyd__ncqab):
            gvwdf__pazo = set([join_node.out_to_input_col_map[jhhmw__zuz][1
                ] for jhhmw__zuz in xvyqo__yfes if join_node.
                out_to_input_col_map[jhhmw__zuz][0] == 'left'])
            owdfg__byq = set(jhhmw__zuz for jhhmw__zuz in join_node.
                left_key_set | join_node.left_cond_cols if jhhmw__zuz <
                join_node.n_left_table_cols)
            if not (lcmcl__qxnpm or uaame__gdc):
                join_node.left_dead_var_inds |= set(range(join_node.
                    n_left_table_cols)) - (gvwdf__pazo | owdfg__byq)
            block_use_map[ybjn__tmsp] = (qogf__nnysy | gvwdf__pazo |
                owdfg__byq, lcmcl__qxnpm or uaame__gdc, False)
    if join_node.has_live_right_table_var:
        wqy__euv = join_node.right_vars[0].name
        qogf__nnysy, mmqu__ivxni, iwlyd__ncqab = block_use_map[wqy__euv]
        if not (mmqu__ivxni or iwlyd__ncqab):
            zyiod__fdvf = set([join_node.out_to_input_col_map[jhhmw__zuz][1
                ] for jhhmw__zuz in xvyqo__yfes if join_node.
                out_to_input_col_map[jhhmw__zuz][0] == 'right'])
            vzps__ikrmw = set(jhhmw__zuz for jhhmw__zuz in join_node.
                right_key_set | join_node.right_cond_cols if jhhmw__zuz <
                join_node.n_right_table_cols)
            if not (lcmcl__qxnpm or uaame__gdc):
                join_node.right_dead_var_inds |= set(range(join_node.
                    n_right_table_cols)) - (zyiod__fdvf | vzps__ikrmw)
            block_use_map[wqy__euv] = (qogf__nnysy | zyiod__fdvf |
                vzps__ikrmw, lcmcl__qxnpm or uaame__gdc, False)


ir_extension_table_column_use[Join] = join_table_column_use


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({wnsuz__gkee.name for wnsuz__gkee in join_node.
        get_live_left_vars()})
    use_set.update({wnsuz__gkee.name for wnsuz__gkee in join_node.
        get_live_right_vars()})
    def_set.update({wnsuz__gkee.name for wnsuz__gkee in join_node.
        get_live_out_vars()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    qwzfu__dpha = set(wnsuz__gkee.name for wnsuz__gkee in join_node.
        get_live_out_vars())
    return set(), qwzfu__dpha


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    join_node.set_live_left_vars([replace_vars_inner(hpies__rzjzm, var_dict
        ) for hpies__rzjzm in join_node.get_live_left_vars()])
    join_node.set_live_right_vars([replace_vars_inner(hpies__rzjzm,
        var_dict) for hpies__rzjzm in join_node.get_live_right_vars()])
    join_node.set_live_out_data_vars([replace_vars_inner(hpies__rzjzm,
        var_dict) for hpies__rzjzm in join_node.get_live_out_vars()])


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for mdjsf__pcs in join_node.get_live_out_vars():
        definitions[mdjsf__pcs.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 2:
        htcga__pikd = join_node.loc.strformat()
        jxv__gzt = [join_node.left_col_names[jhhmw__zuz] for jhhmw__zuz in
            sorted(set(range(len(join_node.left_col_names))) - join_node.
            left_dead_var_inds)]
        dmdr__djvib = """Finished column elimination on join's left input:
%s
Left input columns: %s
"""
        bodo.user_logging.log_message('Column Pruning', dmdr__djvib,
            htcga__pikd, jxv__gzt)
        lst__pvw = [join_node.right_col_names[jhhmw__zuz] for jhhmw__zuz in
            sorted(set(range(len(join_node.right_col_names))) - join_node.
            right_dead_var_inds)]
        dmdr__djvib = """Finished column elimination on join's right input:
%s
Right input columns: %s
"""
        bodo.user_logging.log_message('Column Pruning', dmdr__djvib,
            htcga__pikd, lst__pvw)
        zjnex__gml = [join_node.out_col_names[jhhmw__zuz] for jhhmw__zuz in
            sorted(join_node.get_out_table_used_cols())]
        dmdr__djvib = (
            'Finished column pruning on join node:\n%s\nOutput columns: %s\n')
        bodo.user_logging.log_message('Column Pruning', dmdr__djvib,
            htcga__pikd, zjnex__gml)
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    ejs__zte = len(join_node.left_keys)
    out_physical_to_logical_list = []
    if join_node.has_live_out_table_var:
        out_table_type = typemap[join_node.get_out_table_var().name]
    else:
        out_table_type = types.none
    if join_node.has_live_out_index_var:
        index_col_type = typemap[join_node.get_out_index_var().name]
    else:
        index_col_type = types.none
    if join_node.extra_data_col_num != -1:
        out_physical_to_logical_list.append(join_node.extra_data_col_num)
    left_key_in_output = []
    right_key_in_output = []
    left_used_key_nums = set()
    right_used_key_nums = set()
    left_logical_physical_map = {}
    right_logical_physical_map = {}
    left_physical_to_logical_list = []
    right_physical_to_logical_list = []
    ysa__ayjjw = 0
    irs__iacgu = 0
    gmk__xtvij = []
    for wgawe__oclj in join_node.left_keys:
        skxsb__siy = join_node.left_var_map[wgawe__oclj]
        if not join_node.is_left_table:
            gmk__xtvij.append(join_node.left_vars[skxsb__siy])
        spise__mrdk = 1
        qtdta__hwrbv = join_node.left_to_output_map[skxsb__siy]
        if wgawe__oclj == INDEX_SENTINEL:
            if (join_node.has_live_out_index_var and join_node.index_source ==
                'left' and join_node.index_col_num == skxsb__siy):
                out_physical_to_logical_list.append(qtdta__hwrbv)
                left_used_key_nums.add(skxsb__siy)
            else:
                spise__mrdk = 0
        elif qtdta__hwrbv not in join_node.out_used_cols:
            spise__mrdk = 0
        elif skxsb__siy in left_used_key_nums:
            spise__mrdk = 0
        else:
            left_used_key_nums.add(skxsb__siy)
            out_physical_to_logical_list.append(qtdta__hwrbv)
        left_physical_to_logical_list.append(skxsb__siy)
        left_logical_physical_map[skxsb__siy] = ysa__ayjjw
        ysa__ayjjw += 1
        left_key_in_output.append(spise__mrdk)
    gmk__xtvij = tuple(gmk__xtvij)
    ttx__cvm = []
    for jhhmw__zuz in range(len(join_node.left_col_names)):
        if (jhhmw__zuz not in join_node.left_dead_var_inds and jhhmw__zuz
             not in join_node.left_key_set):
            if not join_node.is_left_table:
                wnsuz__gkee = join_node.left_vars[jhhmw__zuz]
                ttx__cvm.append(wnsuz__gkee)
            uns__jvx = 1
            wghy__smbee = 1
            qtdta__hwrbv = join_node.left_to_output_map[jhhmw__zuz]
            if jhhmw__zuz in join_node.left_cond_cols:
                if qtdta__hwrbv not in join_node.out_used_cols:
                    uns__jvx = 0
                left_key_in_output.append(uns__jvx)
            elif jhhmw__zuz in join_node.left_dead_var_inds:
                uns__jvx = 0
                wghy__smbee = 0
            if uns__jvx:
                out_physical_to_logical_list.append(qtdta__hwrbv)
            if wghy__smbee:
                left_physical_to_logical_list.append(jhhmw__zuz)
                left_logical_physical_map[jhhmw__zuz] = ysa__ayjjw
                ysa__ayjjw += 1
    if (join_node.has_live_out_index_var and join_node.index_source ==
        'left' and join_node.index_col_num not in join_node.left_key_set):
        if not join_node.is_left_table:
            ttx__cvm.append(join_node.left_vars[join_node.index_col_num])
        qtdta__hwrbv = join_node.left_to_output_map[join_node.index_col_num]
        out_physical_to_logical_list.append(qtdta__hwrbv)
        left_physical_to_logical_list.append(join_node.index_col_num)
    ttx__cvm = tuple(ttx__cvm)
    if join_node.is_left_table:
        ttx__cvm = tuple(join_node.get_live_left_vars())
    udn__qjso = []
    for jhhmw__zuz, wgawe__oclj in enumerate(join_node.right_keys):
        skxsb__siy = join_node.right_var_map[wgawe__oclj]
        if not join_node.is_right_table:
            udn__qjso.append(join_node.right_vars[skxsb__siy])
        if not join_node.vect_same_key[jhhmw__zuz] and not join_node.is_join:
            spise__mrdk = 1
            if skxsb__siy not in join_node.right_to_output_map:
                spise__mrdk = 0
            else:
                qtdta__hwrbv = join_node.right_to_output_map[skxsb__siy]
                if wgawe__oclj == INDEX_SENTINEL:
                    if (join_node.has_live_out_index_var and join_node.
                        index_source == 'right' and join_node.index_col_num ==
                        skxsb__siy):
                        out_physical_to_logical_list.append(qtdta__hwrbv)
                        right_used_key_nums.add(skxsb__siy)
                    else:
                        spise__mrdk = 0
                elif qtdta__hwrbv not in join_node.out_used_cols:
                    spise__mrdk = 0
                elif skxsb__siy in right_used_key_nums:
                    spise__mrdk = 0
                else:
                    right_used_key_nums.add(skxsb__siy)
                    out_physical_to_logical_list.append(qtdta__hwrbv)
            right_key_in_output.append(spise__mrdk)
        right_physical_to_logical_list.append(skxsb__siy)
        right_logical_physical_map[skxsb__siy] = irs__iacgu
        irs__iacgu += 1
    udn__qjso = tuple(udn__qjso)
    wdxn__pjy = []
    for jhhmw__zuz in range(len(join_node.right_col_names)):
        if (jhhmw__zuz not in join_node.right_dead_var_inds and jhhmw__zuz
             not in join_node.right_key_set):
            if not join_node.is_right_table:
                wdxn__pjy.append(join_node.right_vars[jhhmw__zuz])
            uns__jvx = 1
            wghy__smbee = 1
            qtdta__hwrbv = join_node.right_to_output_map[jhhmw__zuz]
            if jhhmw__zuz in join_node.right_cond_cols:
                if qtdta__hwrbv not in join_node.out_used_cols:
                    uns__jvx = 0
                right_key_in_output.append(uns__jvx)
            elif jhhmw__zuz in join_node.right_dead_var_inds:
                uns__jvx = 0
                wghy__smbee = 0
            if uns__jvx:
                out_physical_to_logical_list.append(qtdta__hwrbv)
            if wghy__smbee:
                right_physical_to_logical_list.append(jhhmw__zuz)
                right_logical_physical_map[jhhmw__zuz] = irs__iacgu
                irs__iacgu += 1
    if (join_node.has_live_out_index_var and join_node.index_source ==
        'right' and join_node.index_col_num not in join_node.right_key_set):
        if not join_node.is_right_table:
            wdxn__pjy.append(join_node.right_vars[join_node.index_col_num])
        qtdta__hwrbv = join_node.right_to_output_map[join_node.index_col_num]
        out_physical_to_logical_list.append(qtdta__hwrbv)
        right_physical_to_logical_list.append(join_node.index_col_num)
    wdxn__pjy = tuple(wdxn__pjy)
    if join_node.is_right_table:
        wdxn__pjy = tuple(join_node.get_live_right_vars())
    if join_node.indicator_col_num != -1:
        out_physical_to_logical_list.append(join_node.indicator_col_num)
    qvh__iykas = gmk__xtvij + udn__qjso + ttx__cvm + wdxn__pjy
    msko__rakit = tuple(typemap[wnsuz__gkee.name] for wnsuz__gkee in qvh__iykas
        )
    left_other_names = tuple('t1_c' + str(jhhmw__zuz) for jhhmw__zuz in
        range(len(ttx__cvm)))
    right_other_names = tuple('t2_c' + str(jhhmw__zuz) for jhhmw__zuz in
        range(len(wdxn__pjy)))
    if join_node.is_left_table:
        srrr__cuwug = ()
    else:
        srrr__cuwug = tuple('t1_key' + str(jhhmw__zuz) for jhhmw__zuz in
            range(ejs__zte))
    if join_node.is_right_table:
        retl__pkjrw = ()
    else:
        retl__pkjrw = tuple('t2_key' + str(jhhmw__zuz) for jhhmw__zuz in
            range(ejs__zte))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}):\n'.format(','.join(srrr__cuwug + retl__pkjrw +
        left_other_names + right_other_names))
    if join_node.is_left_table:
        left_key_types = []
        left_other_types = []
        if join_node.has_live_left_table_var:
            wnrk__qwbg = typemap[join_node.left_vars[0].name]
        else:
            wnrk__qwbg = types.none
        for mapig__etqk in left_physical_to_logical_list:
            if mapig__etqk < join_node.n_left_table_cols:
                assert join_node.has_live_left_table_var, 'No logical columns should refer to a dead table'
                yadq__yicdo = wnrk__qwbg.arr_types[mapig__etqk]
            else:
                yadq__yicdo = typemap[join_node.left_vars[-1].name]
            if mapig__etqk in join_node.left_key_set:
                left_key_types.append(yadq__yicdo)
            else:
                left_other_types.append(yadq__yicdo)
        left_key_types = tuple(left_key_types)
        left_other_types = tuple(left_other_types)
    else:
        left_key_types = tuple(typemap[wnsuz__gkee.name] for wnsuz__gkee in
            gmk__xtvij)
        left_other_types = tuple([typemap[wgawe__oclj.name] for wgawe__oclj in
            ttx__cvm])
    if join_node.is_right_table:
        right_key_types = []
        right_other_types = []
        if join_node.has_live_right_table_var:
            wnrk__qwbg = typemap[join_node.right_vars[0].name]
        else:
            wnrk__qwbg = types.none
        for mapig__etqk in right_physical_to_logical_list:
            if mapig__etqk < join_node.n_right_table_cols:
                assert join_node.has_live_right_table_var, 'No logical columns should refer to a dead table'
                yadq__yicdo = wnrk__qwbg.arr_types[mapig__etqk]
            else:
                yadq__yicdo = typemap[join_node.right_vars[-1].name]
            if mapig__etqk in join_node.right_key_set:
                right_key_types.append(yadq__yicdo)
            else:
                right_other_types.append(yadq__yicdo)
        right_key_types = tuple(right_key_types)
        right_other_types = tuple(right_other_types)
    else:
        right_key_types = tuple(typemap[wnsuz__gkee.name] for wnsuz__gkee in
            udn__qjso)
        right_other_types = tuple([typemap[wgawe__oclj.name] for
            wgawe__oclj in wdxn__pjy])
    matched_key_types = []
    for jhhmw__zuz in range(ejs__zte):
        vfvqi__sxpb = _match_join_key_types(left_key_types[jhhmw__zuz],
            right_key_types[jhhmw__zuz], loc)
        glbs[f'key_type_{jhhmw__zuz}'] = vfvqi__sxpb
        matched_key_types.append(vfvqi__sxpb)
    if join_node.is_left_table:
        qle__xzeib = determine_table_cast_map(matched_key_types,
            left_key_types, None, {jhhmw__zuz: join_node.left_var_map[
            adnma__ntl] for jhhmw__zuz, adnma__ntl in enumerate(join_node.
            left_keys)}, True)
        if qle__xzeib:
            vqj__basnr = False
            okt__krw = False
            kzyv__vayoe = None
            if join_node.has_live_left_table_var:
                wbpp__ozcy = list(typemap[join_node.left_vars[0].name].
                    arr_types)
            else:
                wbpp__ozcy = None
            for rost__zulir, yadq__yicdo in qle__xzeib.items():
                if rost__zulir < join_node.n_left_table_cols:
                    assert join_node.has_live_left_table_var, 'Casting columns for a dead table should not occur'
                    wbpp__ozcy[rost__zulir] = yadq__yicdo
                    vqj__basnr = True
                else:
                    kzyv__vayoe = yadq__yicdo
                    okt__krw = True
            if vqj__basnr:
                func_text += f"""    {left_other_names[0]} = bodo.utils.table_utils.table_astype({left_other_names[0]}, left_cast_table_type, False, _bodo_nan_to_str=False, used_cols=left_used_cols)
"""
                glbs['left_cast_table_type'] = TableType(tuple(wbpp__ozcy))
                glbs['left_used_cols'] = MetaType(tuple(sorted(set(range(
                    join_node.n_left_table_cols)) - join_node.
                    left_dead_var_inds)))
            if okt__krw:
                func_text += f"""    {left_other_names[1]} = bodo.utils.utils.astype({left_other_names[1]}, left_cast_index_type)
"""
                glbs['left_cast_index_type'] = kzyv__vayoe
    else:
        func_text += '    t1_keys = ({},)\n'.format(', '.join(
            f'bodo.utils.utils.astype({srrr__cuwug[jhhmw__zuz]}, key_type_{jhhmw__zuz})'
             if left_key_types[jhhmw__zuz] != matched_key_types[jhhmw__zuz]
             else f'{srrr__cuwug[jhhmw__zuz]}' for jhhmw__zuz in range(
            ejs__zte)))
        func_text += '    data_left = ({}{})\n'.format(','.join(
            left_other_names), ',' if len(left_other_names) != 0 else '')
    if join_node.is_right_table:
        qle__xzeib = determine_table_cast_map(matched_key_types,
            right_key_types, None, {jhhmw__zuz: join_node.right_var_map[
            adnma__ntl] for jhhmw__zuz, adnma__ntl in enumerate(join_node.
            right_keys)}, True)
        if qle__xzeib:
            vqj__basnr = False
            okt__krw = False
            kzyv__vayoe = None
            if join_node.has_live_right_table_var:
                wbpp__ozcy = list(typemap[join_node.right_vars[0].name].
                    arr_types)
            else:
                wbpp__ozcy = None
            for rost__zulir, yadq__yicdo in qle__xzeib.items():
                if rost__zulir < join_node.n_right_table_cols:
                    assert join_node.has_live_right_table_var, 'Casting columns for a dead table should not occur'
                    wbpp__ozcy[rost__zulir] = yadq__yicdo
                    vqj__basnr = True
                else:
                    kzyv__vayoe = yadq__yicdo
                    okt__krw = True
            if vqj__basnr:
                func_text += f"""    {right_other_names[0]} = bodo.utils.table_utils.table_astype({right_other_names[0]}, right_cast_table_type, False, _bodo_nan_to_str=False, used_cols=right_used_cols)
"""
                glbs['right_cast_table_type'] = TableType(tuple(wbpp__ozcy))
                glbs['right_used_cols'] = MetaType(tuple(sorted(set(range(
                    join_node.n_right_table_cols)) - join_node.
                    right_dead_var_inds)))
            if okt__krw:
                func_text += f"""    {right_other_names[1]} = bodo.utils.utils.astype({right_other_names[1]}, left_cast_index_type)
"""
                glbs['right_cast_index_type'] = kzyv__vayoe
    else:
        func_text += '    t2_keys = ({},)\n'.format(', '.join(
            f'bodo.utils.utils.astype({retl__pkjrw[jhhmw__zuz]}, key_type_{jhhmw__zuz})'
             if right_key_types[jhhmw__zuz] != matched_key_types[jhhmw__zuz
            ] else f'{retl__pkjrw[jhhmw__zuz]}' for jhhmw__zuz in range(
            ejs__zte)))
        func_text += '    data_right = ({}{})\n'.format(','.join(
            right_other_names), ',' if len(right_other_names) != 0 else '')
    general_cond_cfunc, left_col_nums, right_col_nums = (
        _gen_general_cond_cfunc(join_node, typemap,
        left_logical_physical_map, right_logical_physical_map))
    if join_node.how == 'asof':
        if left_parallel or right_parallel:
            assert left_parallel and right_parallel, 'pd.merge_asof requires both left and right to be replicated or distributed'
            func_text += """    t2_keys, data_right = parallel_asof_comm(t1_keys, t2_keys, data_right)
"""
        func_text += """    out_t1_keys, out_t2_keys, out_data_left, out_data_right = bodo.ir.join.local_merge_asof(t1_keys, t2_keys, data_left, data_right)
"""
    else:
        func_text += _gen_local_hash_join(join_node, left_key_types,
            right_key_types, matched_key_types, left_other_names,
            right_other_names, left_other_types, right_other_types,
            left_key_in_output, right_key_in_output, left_parallel,
            right_parallel, glbs, out_physical_to_logical_list,
            out_table_type, index_col_type, join_node.
            get_out_table_used_cols(), left_used_key_nums,
            right_used_key_nums, general_cond_cfunc, left_col_nums,
            right_col_nums, left_physical_to_logical_list,
            right_physical_to_logical_list)
    if join_node.how == 'asof':
        for jhhmw__zuz in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(jhhmw__zuz,
                jhhmw__zuz)
        for jhhmw__zuz in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(
                jhhmw__zuz, jhhmw__zuz)
        for jhhmw__zuz in range(ejs__zte):
            func_text += (
                f'    t1_keys_{jhhmw__zuz} = out_t1_keys[{jhhmw__zuz}]\n')
        for jhhmw__zuz in range(ejs__zte):
            func_text += (
                f'    t2_keys_{jhhmw__zuz} = out_t2_keys[{jhhmw__zuz}]\n')
    hmj__xfk = {}
    exec(func_text, {}, hmj__xfk)
    udm__ptc = hmj__xfk['f']
    glbs.update({'bodo': bodo, 'np': np, 'pd': pd, 'parallel_asof_comm':
        parallel_asof_comm, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'hash_join_table':
        hash_join_table, 'delete_table': delete_table,
        'add_join_gen_cond_cfunc_sym': add_join_gen_cond_cfunc_sym,
        'get_join_cond_addr': get_join_cond_addr, 'key_in_output': np.array
        (left_key_in_output + right_key_in_output, dtype=np.bool_),
        'py_data_to_cpp_table': py_data_to_cpp_table,
        'cpp_table_to_py_data': cpp_table_to_py_data})
    if general_cond_cfunc:
        glbs.update({'general_cond_cfunc': general_cond_cfunc})
    hlfgz__whh = compile_to_numba_ir(udm__ptc, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=msko__rakit, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(hlfgz__whh, qvh__iykas)
    gdw__yamx = hlfgz__whh.body[:-3]
    if join_node.has_live_out_index_var:
        gdw__yamx[-1].target = join_node.out_data_vars[1]
    if join_node.has_live_out_table_var:
        gdw__yamx[-2].target = join_node.out_data_vars[0]
    assert join_node.has_live_out_index_var or join_node.has_live_out_table_var, 'At most one of table and index should be dead if the Join IR node is live'
    if not join_node.has_live_out_index_var:
        gdw__yamx.pop(-1)
    elif not join_node.has_live_out_table_var:
        gdw__yamx.pop(-2)
    return gdw__yamx


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap, left_logical_physical_map,
    right_logical_physical_map):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    ynye__rplz = next_label()
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{ynye__rplz}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
"""
    func_text += '  if is_null_pointer(left_table):\n'
    func_text += '    return False\n'
    expr, func_text, left_col_nums = _replace_column_accesses(expr,
        left_logical_physical_map, join_node.left_var_map, typemap,
        join_node.left_vars, table_getitem_funcs, func_text, 'left',
        join_node.left_key_set, na_check_name, join_node.is_left_table)
    expr, func_text, right_col_nums = _replace_column_accesses(expr,
        right_logical_physical_map, join_node.right_var_map, typemap,
        join_node.right_vars, table_getitem_funcs, func_text, 'right',
        join_node.right_key_set, na_check_name, join_node.is_right_table)
    func_text += f'  return {expr}'
    hmj__xfk = {}
    exec(func_text, table_getitem_funcs, hmj__xfk)
    hybu__exsmf = hmj__xfk[f'bodo_join_gen_cond{ynye__rplz}']
    uvwfq__xlrl = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    ahrtg__olnh = numba.cfunc(uvwfq__xlrl, nopython=True)(hybu__exsmf)
    join_gen_cond_cfunc[ahrtg__olnh.native_name] = ahrtg__olnh
    join_gen_cond_cfunc_addr[ahrtg__olnh.native_name] = ahrtg__olnh.address
    return ahrtg__olnh, left_col_nums, right_col_nums


def _replace_column_accesses(expr, logical_to_physical_ind, name_to_var_map,
    typemap, col_vars, table_getitem_funcs, func_text, table_name, key_set,
    na_check_name, is_table_var):
    hud__fbwo = []
    for wgawe__oclj, slou__iip in name_to_var_map.items():
        izud__dwty = f'({table_name}.{wgawe__oclj})'
        if izud__dwty not in expr:
            continue
        rfj__ovgn = f'getitem_{table_name}_val_{slou__iip}'
        bzza__xrlv = f'_bodo_{table_name}_val_{slou__iip}'
        if is_table_var:
            bhb__ovgtz = typemap[col_vars[0].name].arr_types[slou__iip]
        else:
            bhb__ovgtz = typemap[col_vars[slou__iip].name]
        if is_str_arr_type(bhb__ovgtz) or bhb__ovgtz == bodo.binary_array_type:
            func_text += f"""  {bzza__xrlv}, {bzza__xrlv}_size = {rfj__ovgn}({table_name}_table, {table_name}_ind)
"""
            func_text += f"""  {bzza__xrlv} = bodo.libs.str_arr_ext.decode_utf8({bzza__xrlv}, {bzza__xrlv}_size)
"""
        else:
            func_text += (
                f'  {bzza__xrlv} = {rfj__ovgn}({table_name}_data1, {table_name}_ind)\n'
                )
        adghd__mda = logical_to_physical_ind[slou__iip]
        table_getitem_funcs[rfj__ovgn
            ] = bodo.libs.array._gen_row_access_intrinsic(bhb__ovgtz,
            adghd__mda)
        expr = expr.replace(izud__dwty, bzza__xrlv)
        bst__uck = f'({na_check_name}.{table_name}.{wgawe__oclj})'
        if bst__uck in expr:
            pubj__kqi = f'nacheck_{table_name}_val_{slou__iip}'
            hgvd__iag = f'_bodo_isna_{table_name}_val_{slou__iip}'
            if isinstance(bhb__ovgtz, bodo.libs.int_arr_ext.IntegerArrayType
                ) or bhb__ovgtz in (bodo.libs.bool_arr_ext.boolean_array,
                bodo.binary_array_type) or is_str_arr_type(bhb__ovgtz):
                func_text += f"""  {hgvd__iag} = {pubj__kqi}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += (
                    f'  {hgvd__iag} = {pubj__kqi}({table_name}_data1, {table_name}_ind)\n'
                    )
            table_getitem_funcs[pubj__kqi
                ] = bodo.libs.array._gen_row_na_check_intrinsic(bhb__ovgtz,
                adghd__mda)
            expr = expr.replace(bst__uck, hgvd__iag)
        if slou__iip not in key_set:
            hud__fbwo.append(adghd__mda)
    return expr, func_text, hud__fbwo


def _match_join_key_types(t1, t2, loc):
    if t1 == t2:
        return t1
    if is_str_arr_type(t1) and is_str_arr_type(t2):
        return bodo.string_array_type
    try:
        arr = dtype_to_array_type(find_common_np_dtype([t1, t2]))
        return to_nullable_type(arr) if is_nullable_type(t1
            ) or is_nullable_type(t2) else arr
    except Exception as hqrh__ggwk:
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    fll__jjxim = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[wnsuz__gkee.name] in fll__jjxim for
        wnsuz__gkee in join_node.get_live_left_vars())
    right_parallel = all(array_dists[wnsuz__gkee.name] in fll__jjxim for
        wnsuz__gkee in join_node.get_live_right_vars())
    if not left_parallel:
        assert not any(array_dists[wnsuz__gkee.name] in fll__jjxim for
            wnsuz__gkee in join_node.get_live_left_vars())
    if not right_parallel:
        assert not any(array_dists[wnsuz__gkee.name] in fll__jjxim for
            wnsuz__gkee in join_node.get_live_right_vars())
    if left_parallel or right_parallel:
        assert all(array_dists[wnsuz__gkee.name] in fll__jjxim for
            wnsuz__gkee in join_node.get_live_out_vars())
    return left_parallel, right_parallel


def _gen_local_hash_join(join_node, left_key_types, right_key_types,
    matched_key_types, left_other_names, right_other_names,
    left_other_types, right_other_types, left_key_in_output,
    right_key_in_output, left_parallel, right_parallel, glbs,
    out_physical_to_logical_list, out_table_type, index_col_type,
    out_table_used_cols, left_used_key_nums, right_used_key_nums,
    general_cond_cfunc, left_col_nums, right_col_nums,
    left_physical_to_logical_list, right_physical_to_logical_list):

    def needs_typechange(in_type, need_nullable, is_same_key):
        return isinstance(in_type, types.Array) and not is_dtype_nullable(
            in_type.dtype) and need_nullable and not is_same_key
    nxoh__wrwg = set(left_col_nums)
    dyba__aml = set(right_col_nums)
    bdjof__ncd = join_node.vect_same_key
    ait__qoe = []
    for jhhmw__zuz in range(len(left_key_types)):
        if left_key_in_output[jhhmw__zuz]:
            ait__qoe.append(needs_typechange(matched_key_types[jhhmw__zuz],
                join_node.is_right, bdjof__ncd[jhhmw__zuz]))
    nvo__tqoqg = len(left_key_types)
    bzpuy__lpob = 0
    vcfpu__yyslu = left_physical_to_logical_list[len(left_key_types):]
    for jhhmw__zuz, mapig__etqk in enumerate(vcfpu__yyslu):
        xgp__ooxwe = True
        if mapig__etqk in nxoh__wrwg:
            xgp__ooxwe = left_key_in_output[nvo__tqoqg]
            nvo__tqoqg += 1
        if xgp__ooxwe:
            ait__qoe.append(needs_typechange(left_other_types[jhhmw__zuz],
                join_node.is_right, False))
    for jhhmw__zuz in range(len(right_key_types)):
        if not bdjof__ncd[jhhmw__zuz] and not join_node.is_join:
            if right_key_in_output[bzpuy__lpob]:
                ait__qoe.append(needs_typechange(matched_key_types[
                    jhhmw__zuz], join_node.is_left, False))
            bzpuy__lpob += 1
    fhzk__hilrf = right_physical_to_logical_list[len(right_key_types):]
    for jhhmw__zuz, mapig__etqk in enumerate(fhzk__hilrf):
        xgp__ooxwe = True
        if mapig__etqk in dyba__aml:
            xgp__ooxwe = right_key_in_output[bzpuy__lpob]
            bzpuy__lpob += 1
        if xgp__ooxwe:
            ait__qoe.append(needs_typechange(right_other_types[jhhmw__zuz],
                join_node.is_left, False))
    ejs__zte = len(left_key_types)
    func_text = '    # beginning of _gen_local_hash_join\n'
    if join_node.is_left_table:
        if join_node.has_live_left_table_var:
            skqz__oom = left_other_names[1:]
            dema__yxfq = left_other_names[0]
        else:
            skqz__oom = left_other_names
            dema__yxfq = None
        ijddm__kub = '()' if len(skqz__oom) == 0 else f'({skqz__oom[0]},)'
        func_text += f"""    table_left = py_data_to_cpp_table({dema__yxfq}, {ijddm__kub}, left_in_cols, {join_node.n_left_table_cols})
"""
        glbs['left_in_cols'] = MetaType(tuple(left_physical_to_logical_list))
    else:
        hogr__pyr = []
        for jhhmw__zuz in range(ejs__zte):
            hogr__pyr.append('t1_keys[{}]'.format(jhhmw__zuz))
        for jhhmw__zuz in range(len(left_other_names)):
            hogr__pyr.append('data_left[{}]'.format(jhhmw__zuz))
        func_text += '    info_list_total_l = [{}]\n'.format(','.join(
            'array_to_info({})'.format(yugf__lcm) for yugf__lcm in hogr__pyr))
        func_text += (
            '    table_left = arr_info_list_to_table(info_list_total_l)\n')
    if join_node.is_right_table:
        if join_node.has_live_right_table_var:
            dkbg__wfqvx = right_other_names[1:]
            dema__yxfq = right_other_names[0]
        else:
            dkbg__wfqvx = right_other_names
            dema__yxfq = None
        ijddm__kub = '()' if len(dkbg__wfqvx) == 0 else f'({dkbg__wfqvx[0]},)'
        func_text += f"""    table_right = py_data_to_cpp_table({dema__yxfq}, {ijddm__kub}, right_in_cols, {join_node.n_right_table_cols})
"""
        glbs['right_in_cols'] = MetaType(tuple(right_physical_to_logical_list))
    else:
        rolmc__yqs = []
        for jhhmw__zuz in range(ejs__zte):
            rolmc__yqs.append('t2_keys[{}]'.format(jhhmw__zuz))
        for jhhmw__zuz in range(len(right_other_names)):
            rolmc__yqs.append('data_right[{}]'.format(jhhmw__zuz))
        func_text += '    info_list_total_r = [{}]\n'.format(','.join(
            'array_to_info({})'.format(yugf__lcm) for yugf__lcm in rolmc__yqs))
        func_text += (
            '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    glbs['vect_same_key'] = np.array(bdjof__ncd, dtype=np.int64)
    glbs['vect_need_typechange'] = np.array(ait__qoe, dtype=np.int64)
    glbs['left_table_cond_columns'] = np.array(left_col_nums if len(
        left_col_nums) > 0 else [-1], dtype=np.int64)
    glbs['right_table_cond_columns'] = np.array(right_col_nums if len(
        right_col_nums) > 0 else [-1], dtype=np.int64)
    if general_cond_cfunc:
        func_text += f"""    cfunc_cond = add_join_gen_cond_cfunc_sym(general_cond_cfunc, '{general_cond_cfunc.native_name}')
"""
        func_text += (
            f"    cfunc_cond = get_join_cond_addr('{general_cond_cfunc.native_name}')\n"
            )
    else:
        func_text += '    cfunc_cond = 0\n'
    func_text += f'    total_rows_np = np.array([0], dtype=np.int64)\n'
    func_text += (
        """    out_table = hash_join_table(table_left, table_right, {}, {}, {}, {}, {}, vect_same_key.ctypes, key_in_output.ctypes, vect_need_typechange.ctypes, {}, {}, {}, {}, {}, {}, cfunc_cond, left_table_cond_columns.ctypes, {}, right_table_cond_columns.ctypes, {}, total_rows_np.ctypes)
"""
        .format(left_parallel, right_parallel, ejs__zte, len(vcfpu__yyslu),
        len(fhzk__hilrf), join_node.is_left, join_node.is_right, join_node.
        is_join, join_node.extra_data_col_num != -1, join_node.
        indicator_col_num != -1, join_node.is_na_equal, len(left_col_nums),
        len(right_col_nums)))
    func_text += '    delete_table(table_left)\n'
    func_text += '    delete_table(table_right)\n'
    tlf__xsk = '(py_table_type, index_col_type)'
    func_text += f"""    out_data = cpp_table_to_py_data(out_table, out_col_inds, {tlf__xsk}, total_rows_np[0], {join_node.n_out_table_cols})
"""
    if join_node.has_live_out_table_var:
        func_text += f'    T = out_data[0]\n'
    else:
        func_text += f'    T = None\n'
    if join_node.has_live_out_index_var:
        manj__ydvw = 1 if join_node.has_live_out_table_var else 0
        func_text += f'    index_var = out_data[{manj__ydvw}]\n'
    else:
        func_text += f'    index_var = None\n'
    glbs['py_table_type'] = out_table_type
    glbs['index_col_type'] = index_col_type
    glbs['out_col_inds'] = MetaType(tuple(out_physical_to_logical_list))
    if bool(join_node.out_used_cols) or index_col_type != types.none:
        func_text += '    delete_table(out_table)\n'
    if out_table_type != types.none:
        qle__xzeib = determine_table_cast_map(matched_key_types,
            left_key_types, left_used_key_nums, join_node.
            left_to_output_map, False)
        qle__xzeib.update(determine_table_cast_map(matched_key_types,
            right_key_types, right_used_key_nums, join_node.
            right_to_output_map, False))
        vqj__basnr = False
        okt__krw = False
        if join_node.has_live_out_table_var:
            wbpp__ozcy = list(out_table_type.arr_types)
        else:
            wbpp__ozcy = None
        for rost__zulir, yadq__yicdo in qle__xzeib.items():
            if rost__zulir < join_node.n_out_table_cols:
                assert join_node.has_live_out_table_var, 'Casting columns for a dead table should not occur'
                wbpp__ozcy[rost__zulir] = yadq__yicdo
                vqj__basnr = True
            else:
                kzyv__vayoe = yadq__yicdo
                okt__krw = True
        if vqj__basnr:
            func_text += f"""    T = bodo.utils.table_utils.table_astype(T, cast_table_type, False, _bodo_nan_to_str=False, used_cols=used_cols)
"""
            vwu__xbt = bodo.TableType(tuple(wbpp__ozcy))
            glbs['py_table_type'] = vwu__xbt
            glbs['cast_table_type'] = out_table_type
            glbs['used_cols'] = MetaType(tuple(out_table_used_cols))
        if okt__krw:
            glbs['index_col_type'] = kzyv__vayoe
            glbs['index_cast_type'] = index_col_type
            func_text += (
                f'    index_var = bodo.utils.utils.astype(index_var, index_cast_type)\n'
                )
    func_text += f'    out_table = T\n'
    func_text += f'    out_index = index_var\n'
    return func_text


def determine_table_cast_map(matched_key_types: List[types.Type], key_types:
    List[types.Type], used_key_nums: Optional[Set[int]], output_map: Dict[
    int, int], convert_dict_col: bool):
    qle__xzeib: Dict[int, types.Type] = {}
    ejs__zte = len(matched_key_types)
    for jhhmw__zuz in range(ejs__zte):
        if used_key_nums is None or jhhmw__zuz in used_key_nums:
            if matched_key_types[jhhmw__zuz] != key_types[jhhmw__zuz] and (
                convert_dict_col or key_types[jhhmw__zuz] != bodo.
                dict_str_arr_type):
                manj__ydvw = output_map[jhhmw__zuz]
                qle__xzeib[manj__ydvw] = matched_key_types[jhhmw__zuz]
    return qle__xzeib


@numba.njit
def parallel_asof_comm(left_key_arrs, right_key_arrs, right_data):
    otev__qafz = bodo.libs.distributed_api.get_size()
    kbrtn__cvqx = np.empty(otev__qafz, left_key_arrs[0].dtype)
    rdum__dleu = np.empty(otev__qafz, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(kbrtn__cvqx, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(rdum__dleu, left_key_arrs[0][-1])
    sjls__irjsv = np.zeros(otev__qafz, np.int32)
    agsg__prdru = np.zeros(otev__qafz, np.int32)
    ogvap__phm = np.zeros(otev__qafz, np.int32)
    rezhk__ecec = right_key_arrs[0][0]
    zwxv__iqv = right_key_arrs[0][-1]
    umy__llbtv = -1
    jhhmw__zuz = 0
    while jhhmw__zuz < otev__qafz - 1 and rdum__dleu[jhhmw__zuz] < rezhk__ecec:
        jhhmw__zuz += 1
    while jhhmw__zuz < otev__qafz and kbrtn__cvqx[jhhmw__zuz] <= zwxv__iqv:
        umy__llbtv, wkxoj__vzfgp = _count_overlap(right_key_arrs[0],
            kbrtn__cvqx[jhhmw__zuz], rdum__dleu[jhhmw__zuz])
        if umy__llbtv != 0:
            umy__llbtv -= 1
            wkxoj__vzfgp += 1
        sjls__irjsv[jhhmw__zuz] = wkxoj__vzfgp
        agsg__prdru[jhhmw__zuz] = umy__llbtv
        jhhmw__zuz += 1
    while jhhmw__zuz < otev__qafz:
        sjls__irjsv[jhhmw__zuz] = 1
        agsg__prdru[jhhmw__zuz] = len(right_key_arrs[0]) - 1
        jhhmw__zuz += 1
    bodo.libs.distributed_api.alltoall(sjls__irjsv, ogvap__phm, 1)
    mpj__ujb = ogvap__phm.sum()
    irj__iwk = np.empty(mpj__ujb, right_key_arrs[0].dtype)
    lyo__fmi = alloc_arr_tup(mpj__ujb, right_data)
    rzpji__wxtml = bodo.ir.join.calc_disp(ogvap__phm)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], irj__iwk,
        sjls__irjsv, ogvap__phm, agsg__prdru, rzpji__wxtml)
    bodo.libs.distributed_api.alltoallv_tup(right_data, lyo__fmi,
        sjls__irjsv, ogvap__phm, agsg__prdru, rzpji__wxtml)
    return (irj__iwk,), lyo__fmi


@numba.njit
def _count_overlap(r_key_arr, start, end):
    wkxoj__vzfgp = 0
    umy__llbtv = 0
    fzrf__oiu = 0
    while fzrf__oiu < len(r_key_arr) and r_key_arr[fzrf__oiu] < start:
        umy__llbtv += 1
        fzrf__oiu += 1
    while fzrf__oiu < len(r_key_arr) and start <= r_key_arr[fzrf__oiu] <= end:
        fzrf__oiu += 1
        wkxoj__vzfgp += 1
    return umy__llbtv, wkxoj__vzfgp


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    sytt__gzqa = np.empty_like(arr)
    sytt__gzqa[0] = 0
    for jhhmw__zuz in range(1, len(arr)):
        sytt__gzqa[jhhmw__zuz] = sytt__gzqa[jhhmw__zuz - 1] + arr[
            jhhmw__zuz - 1]
    return sytt__gzqa


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    bih__uge = len(left_keys[0])
    mtndb__mffh = len(right_keys[0])
    hkypt__kwqu = alloc_arr_tup(bih__uge, left_keys)
    lfdyy__otn = alloc_arr_tup(bih__uge, right_keys)
    mzrtj__faez = alloc_arr_tup(bih__uge, data_left)
    twve__gpjm = alloc_arr_tup(bih__uge, data_right)
    ixdqe__rmwtd = 0
    ehjvw__egq = 0
    for ixdqe__rmwtd in range(bih__uge):
        if ehjvw__egq < 0:
            ehjvw__egq = 0
        while ehjvw__egq < mtndb__mffh and getitem_arr_tup(right_keys,
            ehjvw__egq) <= getitem_arr_tup(left_keys, ixdqe__rmwtd):
            ehjvw__egq += 1
        ehjvw__egq -= 1
        setitem_arr_tup(hkypt__kwqu, ixdqe__rmwtd, getitem_arr_tup(
            left_keys, ixdqe__rmwtd))
        setitem_arr_tup(mzrtj__faez, ixdqe__rmwtd, getitem_arr_tup(
            data_left, ixdqe__rmwtd))
        if ehjvw__egq >= 0:
            setitem_arr_tup(lfdyy__otn, ixdqe__rmwtd, getitem_arr_tup(
                right_keys, ehjvw__egq))
            setitem_arr_tup(twve__gpjm, ixdqe__rmwtd, getitem_arr_tup(
                data_right, ehjvw__egq))
        else:
            bodo.libs.array_kernels.setna_tup(lfdyy__otn, ixdqe__rmwtd)
            bodo.libs.array_kernels.setna_tup(twve__gpjm, ixdqe__rmwtd)
    return hkypt__kwqu, lfdyy__otn, mzrtj__faez, twve__gpjm
