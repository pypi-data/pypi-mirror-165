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
        lhjds__ovkun = func.signature
        wrk__xls = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        jnatl__zoqjn = cgutils.get_or_insert_function(builder.module,
            wrk__xls, sym._literal_value)
        builder.call(jnatl__zoqjn, [context.get_constant_null(lhjds__ovkun.
            args[0]), context.get_constant_null(lhjds__ovkun.args[1]),
            context.get_constant_null(lhjds__ovkun.args[2]), context.
            get_constant_null(lhjds__ovkun.args[3]), context.
            get_constant_null(lhjds__ovkun.args[4]), context.
            get_constant_null(lhjds__ovkun.args[5]), context.get_constant(
            types.int64, 0), context.get_constant(types.int64, 0)])
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
        yttzh__gtdh = left_df_type.columns
        slq__mmulq = right_df_type.columns
        self.left_col_names = yttzh__gtdh
        self.right_col_names = slq__mmulq
        self.is_left_table = left_df_type.is_table_format
        self.is_right_table = right_df_type.is_table_format
        self.n_left_table_cols = len(yttzh__gtdh) if self.is_left_table else 0
        self.n_right_table_cols = len(slq__mmulq) if self.is_right_table else 0
        wer__eyt = self.n_left_table_cols if self.is_left_table else len(
            left_vars) - 1
        xozgv__nhm = self.n_right_table_cols if self.is_right_table else len(
            right_vars) - 1
        self.left_dead_var_inds = set()
        self.right_dead_var_inds = set()
        if self.left_vars[-1] is None:
            self.left_dead_var_inds.add(wer__eyt)
        if self.right_vars[-1] is None:
            self.right_dead_var_inds.add(xozgv__nhm)
        self.left_var_map = {ltun__przzl: bzpg__pffh for bzpg__pffh,
            ltun__przzl in enumerate(yttzh__gtdh)}
        self.right_var_map = {ltun__przzl: bzpg__pffh for bzpg__pffh,
            ltun__przzl in enumerate(slq__mmulq)}
        if self.left_vars[-1] is not None:
            self.left_var_map[INDEX_SENTINEL] = wer__eyt
        if self.right_vars[-1] is not None:
            self.right_var_map[INDEX_SENTINEL] = xozgv__nhm
        self.left_key_set = set(self.left_var_map[ltun__przzl] for
            ltun__przzl in left_keys)
        self.right_key_set = set(self.right_var_map[ltun__przzl] for
            ltun__przzl in right_keys)
        if gen_cond_expr:
            self.left_cond_cols = set(self.left_var_map[ltun__przzl] for
                ltun__przzl in yttzh__gtdh if f'(left.{ltun__przzl})' in
                gen_cond_expr)
            self.right_cond_cols = set(self.right_var_map[ltun__przzl] for
                ltun__przzl in slq__mmulq if f'(right.{ltun__przzl})' in
                gen_cond_expr)
        else:
            self.left_cond_cols = set()
            self.right_cond_cols = set()
        zrihz__rbuw: int = -1
        cvpcv__qei = set(left_keys) & set(right_keys)
        szila__obe = set(yttzh__gtdh) & set(slq__mmulq)
        loo__jdh = szila__obe - cvpcv__qei
        qwtop__xfxfy: Dict[int, (Literal['left', 'right'], int)] = {}
        gswpb__bvkit: Dict[int, int] = {}
        fncxd__unu: Dict[int, int] = {}
        for bzpg__pffh, ltun__przzl in enumerate(yttzh__gtdh):
            if ltun__przzl in loo__jdh:
                clfn__zkhw = str(ltun__przzl) + suffix_left
                xqsea__ymmr = out_df_type.column_index[clfn__zkhw]
                if (right_index and not left_index and bzpg__pffh in self.
                    left_key_set):
                    zrihz__rbuw = out_df_type.column_index[ltun__przzl]
                    qwtop__xfxfy[zrihz__rbuw] = 'left', bzpg__pffh
            else:
                xqsea__ymmr = out_df_type.column_index[ltun__przzl]
            qwtop__xfxfy[xqsea__ymmr] = 'left', bzpg__pffh
            gswpb__bvkit[bzpg__pffh] = xqsea__ymmr
        for bzpg__pffh, ltun__przzl in enumerate(slq__mmulq):
            if ltun__przzl not in cvpcv__qei:
                if ltun__przzl in loo__jdh:
                    dbow__dnffs = str(ltun__przzl) + suffix_right
                    xqsea__ymmr = out_df_type.column_index[dbow__dnffs]
                    if (left_index and not right_index and bzpg__pffh in
                        self.right_key_set):
                        zrihz__rbuw = out_df_type.column_index[ltun__przzl]
                        qwtop__xfxfy[zrihz__rbuw] = 'right', bzpg__pffh
                else:
                    xqsea__ymmr = out_df_type.column_index[ltun__przzl]
                qwtop__xfxfy[xqsea__ymmr] = 'right', bzpg__pffh
                fncxd__unu[bzpg__pffh] = xqsea__ymmr
        if self.left_vars[-1] is not None:
            gswpb__bvkit[wer__eyt] = self.n_out_table_cols
        if self.right_vars[-1] is not None:
            fncxd__unu[xozgv__nhm] = self.n_out_table_cols
        self.out_to_input_col_map = qwtop__xfxfy
        self.left_to_output_map = gswpb__bvkit
        self.right_to_output_map = fncxd__unu
        self.extra_data_col_num = zrihz__rbuw
        if len(out_data_vars) > 1:
            akeyf__nveyt = 'left' if right_index else 'right'
            if akeyf__nveyt == 'left':
                uxef__tbl = wer__eyt
            elif akeyf__nveyt == 'right':
                uxef__tbl = xozgv__nhm
        else:
            akeyf__nveyt = None
            uxef__tbl = -1
        self.index_source = akeyf__nveyt
        self.index_col_num = uxef__tbl
        scp__zocau = []
        hyd__phf = len(left_keys)
        for lqkk__lfy in range(hyd__phf):
            flne__qerb = left_keys[lqkk__lfy]
            jmcx__snlig = right_keys[lqkk__lfy]
            scp__zocau.append(flne__qerb == jmcx__snlig)
        self.vect_same_key = scp__zocau

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
        for nlwj__uiog in self.left_vars:
            if nlwj__uiog is not None:
                vars.append(nlwj__uiog)
        return vars

    def get_live_right_vars(self):
        vars = []
        for nlwj__uiog in self.right_vars:
            if nlwj__uiog is not None:
                vars.append(nlwj__uiog)
        return vars

    def get_live_out_vars(self):
        vars = []
        for nlwj__uiog in self.out_data_vars:
            if nlwj__uiog is not None:
                vars.append(nlwj__uiog)
        return vars

    def set_live_left_vars(self, live_data_vars):
        left_vars = []
        koqy__ooyz = 0
        start = 0
        if self.is_left_table:
            if self.has_live_left_table_var:
                left_vars.append(live_data_vars[koqy__ooyz])
                koqy__ooyz += 1
            else:
                left_vars.append(None)
            start = 1
        muzxn__vbdy = max(self.n_left_table_cols - 1, 0)
        for bzpg__pffh in range(start, len(self.left_vars)):
            if bzpg__pffh + muzxn__vbdy in self.left_dead_var_inds:
                left_vars.append(None)
            else:
                left_vars.append(live_data_vars[koqy__ooyz])
                koqy__ooyz += 1
        self.left_vars = left_vars

    def set_live_right_vars(self, live_data_vars):
        right_vars = []
        koqy__ooyz = 0
        start = 0
        if self.is_right_table:
            if self.has_live_right_table_var:
                right_vars.append(live_data_vars[koqy__ooyz])
                koqy__ooyz += 1
            else:
                right_vars.append(None)
            start = 1
        muzxn__vbdy = max(self.n_right_table_cols - 1, 0)
        for bzpg__pffh in range(start, len(self.right_vars)):
            if bzpg__pffh + muzxn__vbdy in self.right_dead_var_inds:
                right_vars.append(None)
            else:
                right_vars.append(live_data_vars[koqy__ooyz])
                koqy__ooyz += 1
        self.right_vars = right_vars

    def set_live_out_data_vars(self, live_data_vars):
        out_data_vars = []
        fkfl__sri = [self.has_live_out_table_var, self.has_live_out_index_var]
        koqy__ooyz = 0
        for bzpg__pffh in range(len(self.out_data_vars)):
            if not fkfl__sri[bzpg__pffh]:
                out_data_vars.append(None)
            else:
                out_data_vars.append(live_data_vars[koqy__ooyz])
                koqy__ooyz += 1
        self.out_data_vars = out_data_vars

    def get_out_table_used_cols(self):
        return {bzpg__pffh for bzpg__pffh in self.out_used_cols if 
            bzpg__pffh < self.n_out_table_cols}

    def __repr__(self):
        hdhi__cpss = ', '.join([f'{ltun__przzl}' for ltun__przzl in self.
            left_col_names])
        sfph__qbot = f'left={{{hdhi__cpss}}}'
        hdhi__cpss = ', '.join([f'{ltun__przzl}' for ltun__przzl in self.
            right_col_names])
        xln__ccktm = f'right={{{hdhi__cpss}}}'
        return 'join [{}={}]: {}, {}'.format(self.left_keys, self.
            right_keys, sfph__qbot, xln__ccktm)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    ttt__cmnz = []
    assert len(join_node.get_live_out_vars()
        ) > 0, 'empty join in array analysis'
    tat__hjk = []
    xpo__gizam = join_node.get_live_left_vars()
    for lcutj__iury in xpo__gizam:
        msldp__yvx = typemap[lcutj__iury.name]
        dxz__vfsl = equiv_set.get_shape(lcutj__iury)
        if dxz__vfsl:
            tat__hjk.append(dxz__vfsl[0])
    if len(tat__hjk) > 1:
        equiv_set.insert_equiv(*tat__hjk)
    tat__hjk = []
    xpo__gizam = list(join_node.get_live_right_vars())
    for lcutj__iury in xpo__gizam:
        msldp__yvx = typemap[lcutj__iury.name]
        dxz__vfsl = equiv_set.get_shape(lcutj__iury)
        if dxz__vfsl:
            tat__hjk.append(dxz__vfsl[0])
    if len(tat__hjk) > 1:
        equiv_set.insert_equiv(*tat__hjk)
    tat__hjk = []
    for urql__ahg in join_node.get_live_out_vars():
        msldp__yvx = typemap[urql__ahg.name]
        ijhk__vjhu = array_analysis._gen_shape_call(equiv_set, urql__ahg,
            msldp__yvx.ndim, None, ttt__cmnz)
        equiv_set.insert_equiv(urql__ahg, ijhk__vjhu)
        tat__hjk.append(ijhk__vjhu[0])
        equiv_set.define(urql__ahg, set())
    if len(tat__hjk) > 1:
        equiv_set.insert_equiv(*tat__hjk)
    return [], ttt__cmnz


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    mdr__gbrc = Distribution.OneD
    okmpy__xprw = Distribution.OneD
    for lcutj__iury in join_node.get_live_left_vars():
        mdr__gbrc = Distribution(min(mdr__gbrc.value, array_dists[
            lcutj__iury.name].value))
    for lcutj__iury in join_node.get_live_right_vars():
        okmpy__xprw = Distribution(min(okmpy__xprw.value, array_dists[
            lcutj__iury.name].value))
    ebhi__wgj = Distribution.OneD_Var
    for urql__ahg in join_node.get_live_out_vars():
        if urql__ahg.name in array_dists:
            ebhi__wgj = Distribution(min(ebhi__wgj.value, array_dists[
                urql__ahg.name].value))
    kbgp__cwvb = Distribution(min(ebhi__wgj.value, mdr__gbrc.value))
    dhr__fjrqn = Distribution(min(ebhi__wgj.value, okmpy__xprw.value))
    ebhi__wgj = Distribution(max(kbgp__cwvb.value, dhr__fjrqn.value))
    for urql__ahg in join_node.get_live_out_vars():
        array_dists[urql__ahg.name] = ebhi__wgj
    if ebhi__wgj != Distribution.OneD_Var:
        mdr__gbrc = ebhi__wgj
        okmpy__xprw = ebhi__wgj
    for lcutj__iury in join_node.get_live_left_vars():
        array_dists[lcutj__iury.name] = mdr__gbrc
    for lcutj__iury in join_node.get_live_right_vars():
        array_dists[lcutj__iury.name] = okmpy__xprw
    return


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def visit_vars_join(join_node, callback, cbdata):
    join_node.set_live_left_vars([visit_vars_inner(nlwj__uiog, callback,
        cbdata) for nlwj__uiog in join_node.get_live_left_vars()])
    join_node.set_live_right_vars([visit_vars_inner(nlwj__uiog, callback,
        cbdata) for nlwj__uiog in join_node.get_live_right_vars()])
    join_node.set_live_out_data_vars([visit_vars_inner(nlwj__uiog, callback,
        cbdata) for nlwj__uiog in join_node.get_live_out_vars()])


ir_utils.visit_vars_extensions[Join] = visit_vars_join


def remove_dead_join(join_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if join_node.has_live_out_table_var:
        uptee__ogzrm = []
        xmdn__tyg = join_node.get_out_table_var()
        if xmdn__tyg.name not in lives:
            join_node.out_data_vars[0] = None
            join_node.out_used_cols.difference_update(join_node.
                get_out_table_used_cols())
        for evnzt__xoyy in join_node.out_to_input_col_map.keys():
            if evnzt__xoyy in join_node.out_used_cols:
                continue
            uptee__ogzrm.append(evnzt__xoyy)
            if join_node.indicator_col_num == evnzt__xoyy:
                join_node.indicator_col_num = -1
                continue
            if evnzt__xoyy == join_node.extra_data_col_num:
                join_node.extra_data_col_num = -1
                continue
            walv__kcjh, evnzt__xoyy = join_node.out_to_input_col_map[
                evnzt__xoyy]
            if walv__kcjh == 'left':
                if (evnzt__xoyy not in join_node.left_key_set and 
                    evnzt__xoyy not in join_node.left_cond_cols):
                    join_node.left_dead_var_inds.add(evnzt__xoyy)
                    if not join_node.is_left_table:
                        join_node.left_vars[evnzt__xoyy] = None
            elif walv__kcjh == 'right':
                if (evnzt__xoyy not in join_node.right_key_set and 
                    evnzt__xoyy not in join_node.right_cond_cols):
                    join_node.right_dead_var_inds.add(evnzt__xoyy)
                    if not join_node.is_right_table:
                        join_node.right_vars[evnzt__xoyy] = None
        for bzpg__pffh in uptee__ogzrm:
            del join_node.out_to_input_col_map[bzpg__pffh]
        if join_node.is_left_table:
            hzyux__cktz = set(range(join_node.n_left_table_cols))
            vvkyh__qfr = not bool(hzyux__cktz - join_node.left_dead_var_inds)
            if vvkyh__qfr:
                join_node.left_vars[0] = None
        if join_node.is_right_table:
            hzyux__cktz = set(range(join_node.n_right_table_cols))
            vvkyh__qfr = not bool(hzyux__cktz - join_node.right_dead_var_inds)
            if vvkyh__qfr:
                join_node.right_vars[0] = None
    if join_node.has_live_out_index_var:
        jijt__wnaso = join_node.get_out_index_var()
        if jijt__wnaso.name not in lives:
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
    wleoz__yithr = False
    if join_node.has_live_out_table_var:
        wtrc__hjme = join_node.get_out_table_var().name
        vlpw__qitr, mxi__mcc, xpq__gxki = get_live_column_nums_block(
            column_live_map, equiv_vars, wtrc__hjme)
        if not (mxi__mcc or xpq__gxki):
            vlpw__qitr = trim_extra_used_columns(vlpw__qitr, join_node.
                n_out_table_cols)
            arfqs__qixi = join_node.get_out_table_used_cols()
            if len(vlpw__qitr) != len(arfqs__qixi):
                wleoz__yithr = not (join_node.is_left_table and join_node.
                    is_right_table)
                vvj__aslgk = arfqs__qixi - vlpw__qitr
                join_node.out_used_cols = join_node.out_used_cols - vvj__aslgk
    return wleoz__yithr


remove_dead_column_extensions[Join] = join_remove_dead_column


def join_table_column_use(join_node: Join, block_use_map: Dict[str, Tuple[
    Set[int], bool, bool]], equiv_vars: Dict[str, Set[str]], typemap: Dict[
    str, types.Type], table_col_use_map: Dict[int, Dict[str, Tuple[Set[int],
    bool, bool]]]):
    if not (join_node.is_left_table or join_node.is_right_table):
        return
    if join_node.has_live_out_table_var:
        rdj__ubj = join_node.get_out_table_var()
        utht__wbp, mxi__mcc, xpq__gxki = _compute_table_column_uses(rdj__ubj
            .name, table_col_use_map, equiv_vars)
    else:
        utht__wbp, mxi__mcc, xpq__gxki = set(), False, False
    if join_node.has_live_left_table_var:
        boxvf__dlnx = join_node.left_vars[0].name
        sanwr__znjb, ysh__zymno, rnc__lmltm = block_use_map[boxvf__dlnx]
        if not (ysh__zymno or rnc__lmltm):
            wngty__mmih = set([join_node.out_to_input_col_map[bzpg__pffh][1
                ] for bzpg__pffh in utht__wbp if join_node.
                out_to_input_col_map[bzpg__pffh][0] == 'left'])
            zwzbx__tyd = set(bzpg__pffh for bzpg__pffh in join_node.
                left_key_set | join_node.left_cond_cols if bzpg__pffh <
                join_node.n_left_table_cols)
            if not (mxi__mcc or xpq__gxki):
                join_node.left_dead_var_inds |= set(range(join_node.
                    n_left_table_cols)) - (wngty__mmih | zwzbx__tyd)
            block_use_map[boxvf__dlnx] = (sanwr__znjb | wngty__mmih |
                zwzbx__tyd, mxi__mcc or xpq__gxki, False)
    if join_node.has_live_right_table_var:
        kdxf__ydwb = join_node.right_vars[0].name
        sanwr__znjb, ysh__zymno, rnc__lmltm = block_use_map[kdxf__ydwb]
        if not (ysh__zymno or rnc__lmltm):
            kpyy__niaj = set([join_node.out_to_input_col_map[bzpg__pffh][1] for
                bzpg__pffh in utht__wbp if join_node.out_to_input_col_map[
                bzpg__pffh][0] == 'right'])
            vlr__bpmk = set(bzpg__pffh for bzpg__pffh in join_node.
                right_key_set | join_node.right_cond_cols if bzpg__pffh <
                join_node.n_right_table_cols)
            if not (mxi__mcc or xpq__gxki):
                join_node.right_dead_var_inds |= set(range(join_node.
                    n_right_table_cols)) - (kpyy__niaj | vlr__bpmk)
            block_use_map[kdxf__ydwb] = (sanwr__znjb | kpyy__niaj |
                vlr__bpmk, mxi__mcc or xpq__gxki, False)


ir_extension_table_column_use[Join] = join_table_column_use


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({dsj__eqxmd.name for dsj__eqxmd in join_node.
        get_live_left_vars()})
    use_set.update({dsj__eqxmd.name for dsj__eqxmd in join_node.
        get_live_right_vars()})
    def_set.update({dsj__eqxmd.name for dsj__eqxmd in join_node.
        get_live_out_vars()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    pexk__mruf = set(dsj__eqxmd.name for dsj__eqxmd in join_node.
        get_live_out_vars())
    return set(), pexk__mruf


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    join_node.set_live_left_vars([replace_vars_inner(nlwj__uiog, var_dict) for
        nlwj__uiog in join_node.get_live_left_vars()])
    join_node.set_live_right_vars([replace_vars_inner(nlwj__uiog, var_dict) for
        nlwj__uiog in join_node.get_live_right_vars()])
    join_node.set_live_out_data_vars([replace_vars_inner(nlwj__uiog,
        var_dict) for nlwj__uiog in join_node.get_live_out_vars()])


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for lcutj__iury in join_node.get_live_out_vars():
        definitions[lcutj__iury.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 2:
        uhvr__fsim = join_node.loc.strformat()
        jmy__holf = [join_node.left_col_names[bzpg__pffh] for bzpg__pffh in
            sorted(set(range(len(join_node.left_col_names))) - join_node.
            left_dead_var_inds)]
        dfpz__yakw = """Finished column elimination on join's left input:
%s
Left input columns: %s
"""
        bodo.user_logging.log_message('Column Pruning', dfpz__yakw,
            uhvr__fsim, jmy__holf)
        fmksv__xeo = [join_node.right_col_names[bzpg__pffh] for bzpg__pffh in
            sorted(set(range(len(join_node.right_col_names))) - join_node.
            right_dead_var_inds)]
        dfpz__yakw = """Finished column elimination on join's right input:
%s
Right input columns: %s
"""
        bodo.user_logging.log_message('Column Pruning', dfpz__yakw,
            uhvr__fsim, fmksv__xeo)
        cow__gczxs = [join_node.out_col_names[bzpg__pffh] for bzpg__pffh in
            sorted(join_node.get_out_table_used_cols())]
        dfpz__yakw = (
            'Finished column pruning on join node:\n%s\nOutput columns: %s\n')
        bodo.user_logging.log_message('Column Pruning', dfpz__yakw,
            uhvr__fsim, cow__gczxs)
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    hyd__phf = len(join_node.left_keys)
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
    wzok__bfyny = 0
    ogi__qcjv = 0
    lwk__nhyva = []
    for ltun__przzl in join_node.left_keys:
        qjeh__owtw = join_node.left_var_map[ltun__przzl]
        if not join_node.is_left_table:
            lwk__nhyva.append(join_node.left_vars[qjeh__owtw])
        fkfl__sri = 1
        xqsea__ymmr = join_node.left_to_output_map[qjeh__owtw]
        if ltun__przzl == INDEX_SENTINEL:
            if (join_node.has_live_out_index_var and join_node.index_source ==
                'left' and join_node.index_col_num == qjeh__owtw):
                out_physical_to_logical_list.append(xqsea__ymmr)
                left_used_key_nums.add(qjeh__owtw)
            else:
                fkfl__sri = 0
        elif xqsea__ymmr not in join_node.out_used_cols:
            fkfl__sri = 0
        elif qjeh__owtw in left_used_key_nums:
            fkfl__sri = 0
        else:
            left_used_key_nums.add(qjeh__owtw)
            out_physical_to_logical_list.append(xqsea__ymmr)
        left_physical_to_logical_list.append(qjeh__owtw)
        left_logical_physical_map[qjeh__owtw] = wzok__bfyny
        wzok__bfyny += 1
        left_key_in_output.append(fkfl__sri)
    lwk__nhyva = tuple(lwk__nhyva)
    nassn__cjqms = []
    for bzpg__pffh in range(len(join_node.left_col_names)):
        if (bzpg__pffh not in join_node.left_dead_var_inds and bzpg__pffh
             not in join_node.left_key_set):
            if not join_node.is_left_table:
                dsj__eqxmd = join_node.left_vars[bzpg__pffh]
                nassn__cjqms.append(dsj__eqxmd)
            mwp__wtyk = 1
            nwa__oqtx = 1
            xqsea__ymmr = join_node.left_to_output_map[bzpg__pffh]
            if bzpg__pffh in join_node.left_cond_cols:
                if xqsea__ymmr not in join_node.out_used_cols:
                    mwp__wtyk = 0
                left_key_in_output.append(mwp__wtyk)
            elif bzpg__pffh in join_node.left_dead_var_inds:
                mwp__wtyk = 0
                nwa__oqtx = 0
            if mwp__wtyk:
                out_physical_to_logical_list.append(xqsea__ymmr)
            if nwa__oqtx:
                left_physical_to_logical_list.append(bzpg__pffh)
                left_logical_physical_map[bzpg__pffh] = wzok__bfyny
                wzok__bfyny += 1
    if (join_node.has_live_out_index_var and join_node.index_source ==
        'left' and join_node.index_col_num not in join_node.left_key_set):
        if not join_node.is_left_table:
            nassn__cjqms.append(join_node.left_vars[join_node.index_col_num])
        xqsea__ymmr = join_node.left_to_output_map[join_node.index_col_num]
        out_physical_to_logical_list.append(xqsea__ymmr)
        left_physical_to_logical_list.append(join_node.index_col_num)
    nassn__cjqms = tuple(nassn__cjqms)
    if join_node.is_left_table:
        nassn__cjqms = tuple(join_node.get_live_left_vars())
    bufh__nqyzg = []
    for bzpg__pffh, ltun__przzl in enumerate(join_node.right_keys):
        qjeh__owtw = join_node.right_var_map[ltun__przzl]
        if not join_node.is_right_table:
            bufh__nqyzg.append(join_node.right_vars[qjeh__owtw])
        if not join_node.vect_same_key[bzpg__pffh] and not join_node.is_join:
            fkfl__sri = 1
            if qjeh__owtw not in join_node.right_to_output_map:
                fkfl__sri = 0
            else:
                xqsea__ymmr = join_node.right_to_output_map[qjeh__owtw]
                if ltun__przzl == INDEX_SENTINEL:
                    if (join_node.has_live_out_index_var and join_node.
                        index_source == 'right' and join_node.index_col_num ==
                        qjeh__owtw):
                        out_physical_to_logical_list.append(xqsea__ymmr)
                        right_used_key_nums.add(qjeh__owtw)
                    else:
                        fkfl__sri = 0
                elif xqsea__ymmr not in join_node.out_used_cols:
                    fkfl__sri = 0
                elif qjeh__owtw in right_used_key_nums:
                    fkfl__sri = 0
                else:
                    right_used_key_nums.add(qjeh__owtw)
                    out_physical_to_logical_list.append(xqsea__ymmr)
            right_key_in_output.append(fkfl__sri)
        right_physical_to_logical_list.append(qjeh__owtw)
        right_logical_physical_map[qjeh__owtw] = ogi__qcjv
        ogi__qcjv += 1
    bufh__nqyzg = tuple(bufh__nqyzg)
    vfqx__jlam = []
    for bzpg__pffh in range(len(join_node.right_col_names)):
        if (bzpg__pffh not in join_node.right_dead_var_inds and bzpg__pffh
             not in join_node.right_key_set):
            if not join_node.is_right_table:
                vfqx__jlam.append(join_node.right_vars[bzpg__pffh])
            mwp__wtyk = 1
            nwa__oqtx = 1
            xqsea__ymmr = join_node.right_to_output_map[bzpg__pffh]
            if bzpg__pffh in join_node.right_cond_cols:
                if xqsea__ymmr not in join_node.out_used_cols:
                    mwp__wtyk = 0
                right_key_in_output.append(mwp__wtyk)
            elif bzpg__pffh in join_node.right_dead_var_inds:
                mwp__wtyk = 0
                nwa__oqtx = 0
            if mwp__wtyk:
                out_physical_to_logical_list.append(xqsea__ymmr)
            if nwa__oqtx:
                right_physical_to_logical_list.append(bzpg__pffh)
                right_logical_physical_map[bzpg__pffh] = ogi__qcjv
                ogi__qcjv += 1
    if (join_node.has_live_out_index_var and join_node.index_source ==
        'right' and join_node.index_col_num not in join_node.right_key_set):
        if not join_node.is_right_table:
            vfqx__jlam.append(join_node.right_vars[join_node.index_col_num])
        xqsea__ymmr = join_node.right_to_output_map[join_node.index_col_num]
        out_physical_to_logical_list.append(xqsea__ymmr)
        right_physical_to_logical_list.append(join_node.index_col_num)
    vfqx__jlam = tuple(vfqx__jlam)
    if join_node.is_right_table:
        vfqx__jlam = tuple(join_node.get_live_right_vars())
    if join_node.indicator_col_num != -1:
        out_physical_to_logical_list.append(join_node.indicator_col_num)
    hihgo__qusn = lwk__nhyva + bufh__nqyzg + nassn__cjqms + vfqx__jlam
    iyevw__oklz = tuple(typemap[dsj__eqxmd.name] for dsj__eqxmd in hihgo__qusn)
    left_other_names = tuple('t1_c' + str(bzpg__pffh) for bzpg__pffh in
        range(len(nassn__cjqms)))
    right_other_names = tuple('t2_c' + str(bzpg__pffh) for bzpg__pffh in
        range(len(vfqx__jlam)))
    if join_node.is_left_table:
        mcund__ybdp = ()
    else:
        mcund__ybdp = tuple('t1_key' + str(bzpg__pffh) for bzpg__pffh in
            range(hyd__phf))
    if join_node.is_right_table:
        exkur__rftj = ()
    else:
        exkur__rftj = tuple('t2_key' + str(bzpg__pffh) for bzpg__pffh in
            range(hyd__phf))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}):\n'.format(','.join(mcund__ybdp + exkur__rftj +
        left_other_names + right_other_names))
    if join_node.is_left_table:
        left_key_types = []
        left_other_types = []
        if join_node.has_live_left_table_var:
            pvvnx__wbii = typemap[join_node.left_vars[0].name]
        else:
            pvvnx__wbii = types.none
        for snr__ekngb in left_physical_to_logical_list:
            if snr__ekngb < join_node.n_left_table_cols:
                assert join_node.has_live_left_table_var, 'No logical columns should refer to a dead table'
                msldp__yvx = pvvnx__wbii.arr_types[snr__ekngb]
            else:
                msldp__yvx = typemap[join_node.left_vars[-1].name]
            if snr__ekngb in join_node.left_key_set:
                left_key_types.append(msldp__yvx)
            else:
                left_other_types.append(msldp__yvx)
        left_key_types = tuple(left_key_types)
        left_other_types = tuple(left_other_types)
    else:
        left_key_types = tuple(typemap[dsj__eqxmd.name] for dsj__eqxmd in
            lwk__nhyva)
        left_other_types = tuple([typemap[ltun__przzl.name] for ltun__przzl in
            nassn__cjqms])
    if join_node.is_right_table:
        right_key_types = []
        right_other_types = []
        if join_node.has_live_right_table_var:
            pvvnx__wbii = typemap[join_node.right_vars[0].name]
        else:
            pvvnx__wbii = types.none
        for snr__ekngb in right_physical_to_logical_list:
            if snr__ekngb < join_node.n_right_table_cols:
                assert join_node.has_live_right_table_var, 'No logical columns should refer to a dead table'
                msldp__yvx = pvvnx__wbii.arr_types[snr__ekngb]
            else:
                msldp__yvx = typemap[join_node.right_vars[-1].name]
            if snr__ekngb in join_node.right_key_set:
                right_key_types.append(msldp__yvx)
            else:
                right_other_types.append(msldp__yvx)
        right_key_types = tuple(right_key_types)
        right_other_types = tuple(right_other_types)
    else:
        right_key_types = tuple(typemap[dsj__eqxmd.name] for dsj__eqxmd in
            bufh__nqyzg)
        right_other_types = tuple([typemap[ltun__przzl.name] for
            ltun__przzl in vfqx__jlam])
    matched_key_types = []
    for bzpg__pffh in range(hyd__phf):
        hapsc__pbhkm = _match_join_key_types(left_key_types[bzpg__pffh],
            right_key_types[bzpg__pffh], loc)
        glbs[f'key_type_{bzpg__pffh}'] = hapsc__pbhkm
        matched_key_types.append(hapsc__pbhkm)
    if join_node.is_left_table:
        ndk__eiktw = determine_table_cast_map(matched_key_types,
            left_key_types, None, {bzpg__pffh: join_node.left_var_map[
            fjip__brjfz] for bzpg__pffh, fjip__brjfz in enumerate(join_node
            .left_keys)}, True)
        if ndk__eiktw:
            emw__birtu = False
            pfg__xki = False
            vqsd__vad = None
            if join_node.has_live_left_table_var:
                znok__tgq = list(typemap[join_node.left_vars[0].name].arr_types
                    )
            else:
                znok__tgq = None
            for evnzt__xoyy, msldp__yvx in ndk__eiktw.items():
                if evnzt__xoyy < join_node.n_left_table_cols:
                    assert join_node.has_live_left_table_var, 'Casting columns for a dead table should not occur'
                    znok__tgq[evnzt__xoyy] = msldp__yvx
                    emw__birtu = True
                else:
                    vqsd__vad = msldp__yvx
                    pfg__xki = True
            if emw__birtu:
                func_text += f"""    {left_other_names[0]} = bodo.utils.table_utils.table_astype({left_other_names[0]}, left_cast_table_type, False, _bodo_nan_to_str=False, used_cols=left_used_cols)
"""
                glbs['left_cast_table_type'] = TableType(tuple(znok__tgq))
                glbs['left_used_cols'] = MetaType(tuple(sorted(set(range(
                    join_node.n_left_table_cols)) - join_node.
                    left_dead_var_inds)))
            if pfg__xki:
                func_text += f"""    {left_other_names[1]} = bodo.utils.utils.astype({left_other_names[1]}, left_cast_index_type)
"""
                glbs['left_cast_index_type'] = vqsd__vad
    else:
        func_text += '    t1_keys = ({},)\n'.format(', '.join(
            f'bodo.utils.utils.astype({mcund__ybdp[bzpg__pffh]}, key_type_{bzpg__pffh})'
             if left_key_types[bzpg__pffh] != matched_key_types[bzpg__pffh]
             else f'{mcund__ybdp[bzpg__pffh]}' for bzpg__pffh in range(
            hyd__phf)))
        func_text += '    data_left = ({}{})\n'.format(','.join(
            left_other_names), ',' if len(left_other_names) != 0 else '')
    if join_node.is_right_table:
        ndk__eiktw = determine_table_cast_map(matched_key_types,
            right_key_types, None, {bzpg__pffh: join_node.right_var_map[
            fjip__brjfz] for bzpg__pffh, fjip__brjfz in enumerate(join_node
            .right_keys)}, True)
        if ndk__eiktw:
            emw__birtu = False
            pfg__xki = False
            vqsd__vad = None
            if join_node.has_live_right_table_var:
                znok__tgq = list(typemap[join_node.right_vars[0].name].
                    arr_types)
            else:
                znok__tgq = None
            for evnzt__xoyy, msldp__yvx in ndk__eiktw.items():
                if evnzt__xoyy < join_node.n_right_table_cols:
                    assert join_node.has_live_right_table_var, 'Casting columns for a dead table should not occur'
                    znok__tgq[evnzt__xoyy] = msldp__yvx
                    emw__birtu = True
                else:
                    vqsd__vad = msldp__yvx
                    pfg__xki = True
            if emw__birtu:
                func_text += f"""    {right_other_names[0]} = bodo.utils.table_utils.table_astype({right_other_names[0]}, right_cast_table_type, False, _bodo_nan_to_str=False, used_cols=right_used_cols)
"""
                glbs['right_cast_table_type'] = TableType(tuple(znok__tgq))
                glbs['right_used_cols'] = MetaType(tuple(sorted(set(range(
                    join_node.n_right_table_cols)) - join_node.
                    right_dead_var_inds)))
            if pfg__xki:
                func_text += f"""    {right_other_names[1]} = bodo.utils.utils.astype({right_other_names[1]}, left_cast_index_type)
"""
                glbs['right_cast_index_type'] = vqsd__vad
    else:
        func_text += '    t2_keys = ({},)\n'.format(', '.join(
            f'bodo.utils.utils.astype({exkur__rftj[bzpg__pffh]}, key_type_{bzpg__pffh})'
             if right_key_types[bzpg__pffh] != matched_key_types[bzpg__pffh
            ] else f'{exkur__rftj[bzpg__pffh]}' for bzpg__pffh in range(
            hyd__phf)))
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
        for bzpg__pffh in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(bzpg__pffh,
                bzpg__pffh)
        for bzpg__pffh in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(
                bzpg__pffh, bzpg__pffh)
        for bzpg__pffh in range(hyd__phf):
            func_text += (
                f'    t1_keys_{bzpg__pffh} = out_t1_keys[{bzpg__pffh}]\n')
        for bzpg__pffh in range(hyd__phf):
            func_text += (
                f'    t2_keys_{bzpg__pffh} = out_t2_keys[{bzpg__pffh}]\n')
    lzvay__bpikz = {}
    exec(func_text, {}, lzvay__bpikz)
    hyyeu__psgpy = lzvay__bpikz['f']
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
    zjm__esarv = compile_to_numba_ir(hyyeu__psgpy, glbs, typingctx=
        typingctx, targetctx=targetctx, arg_typs=iyevw__oklz, typemap=
        typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(zjm__esarv, hihgo__qusn)
    gbqfm__slx = zjm__esarv.body[:-3]
    if join_node.has_live_out_index_var:
        gbqfm__slx[-1].target = join_node.out_data_vars[1]
    if join_node.has_live_out_table_var:
        gbqfm__slx[-2].target = join_node.out_data_vars[0]
    assert join_node.has_live_out_index_var or join_node.has_live_out_table_var, 'At most one of table and index should be dead if the Join IR node is live'
    if not join_node.has_live_out_index_var:
        gbqfm__slx.pop(-1)
    elif not join_node.has_live_out_table_var:
        gbqfm__slx.pop(-2)
    return gbqfm__slx


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap, left_logical_physical_map,
    right_logical_physical_map):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    xuts__xffl = next_label()
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{xuts__xffl}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
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
    lzvay__bpikz = {}
    exec(func_text, table_getitem_funcs, lzvay__bpikz)
    aonwx__wzvl = lzvay__bpikz[f'bodo_join_gen_cond{xuts__xffl}']
    fsz__iwntw = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    rlix__tbx = numba.cfunc(fsz__iwntw, nopython=True)(aonwx__wzvl)
    join_gen_cond_cfunc[rlix__tbx.native_name] = rlix__tbx
    join_gen_cond_cfunc_addr[rlix__tbx.native_name] = rlix__tbx.address
    return rlix__tbx, left_col_nums, right_col_nums


def _replace_column_accesses(expr, logical_to_physical_ind, name_to_var_map,
    typemap, col_vars, table_getitem_funcs, func_text, table_name, key_set,
    na_check_name, is_table_var):
    xde__vkg = []
    for ltun__przzl, ocjx__ldlxk in name_to_var_map.items():
        egjcx__llrps = f'({table_name}.{ltun__przzl})'
        if egjcx__llrps not in expr:
            continue
        hio__hjk = f'getitem_{table_name}_val_{ocjx__ldlxk}'
        pllf__eozrq = f'_bodo_{table_name}_val_{ocjx__ldlxk}'
        if is_table_var:
            uaf__fty = typemap[col_vars[0].name].arr_types[ocjx__ldlxk]
        else:
            uaf__fty = typemap[col_vars[ocjx__ldlxk].name]
        if is_str_arr_type(uaf__fty) or uaf__fty == bodo.binary_array_type:
            func_text += f"""  {pllf__eozrq}, {pllf__eozrq}_size = {hio__hjk}({table_name}_table, {table_name}_ind)
"""
            func_text += f"""  {pllf__eozrq} = bodo.libs.str_arr_ext.decode_utf8({pllf__eozrq}, {pllf__eozrq}_size)
"""
        else:
            func_text += (
                f'  {pllf__eozrq} = {hio__hjk}({table_name}_data1, {table_name}_ind)\n'
                )
        aob__ytsfw = logical_to_physical_ind[ocjx__ldlxk]
        table_getitem_funcs[hio__hjk
            ] = bodo.libs.array._gen_row_access_intrinsic(uaf__fty, aob__ytsfw)
        expr = expr.replace(egjcx__llrps, pllf__eozrq)
        bvoq__buhb = f'({na_check_name}.{table_name}.{ltun__przzl})'
        if bvoq__buhb in expr:
            qglm__rbnmu = f'nacheck_{table_name}_val_{ocjx__ldlxk}'
            rco__ruyb = f'_bodo_isna_{table_name}_val_{ocjx__ldlxk}'
            if isinstance(uaf__fty, bodo.libs.int_arr_ext.IntegerArrayType
                ) or uaf__fty in (bodo.libs.bool_arr_ext.boolean_array,
                bodo.binary_array_type) or is_str_arr_type(uaf__fty):
                func_text += f"""  {rco__ruyb} = {qglm__rbnmu}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += f"""  {rco__ruyb} = {qglm__rbnmu}({table_name}_data1, {table_name}_ind)
"""
            table_getitem_funcs[qglm__rbnmu
                ] = bodo.libs.array._gen_row_na_check_intrinsic(uaf__fty,
                aob__ytsfw)
            expr = expr.replace(bvoq__buhb, rco__ruyb)
        if ocjx__ldlxk not in key_set:
            xde__vkg.append(aob__ytsfw)
    return expr, func_text, xde__vkg


def _match_join_key_types(t1, t2, loc):
    if t1 == t2:
        return t1
    if is_str_arr_type(t1) and is_str_arr_type(t2):
        return bodo.string_array_type
    try:
        arr = dtype_to_array_type(find_common_np_dtype([t1, t2]))
        return to_nullable_type(arr) if is_nullable_type(t1
            ) or is_nullable_type(t2) else arr
    except Exception as gktw__mnv:
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    fukz__aivk = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[dsj__eqxmd.name] in fukz__aivk for
        dsj__eqxmd in join_node.get_live_left_vars())
    right_parallel = all(array_dists[dsj__eqxmd.name] in fukz__aivk for
        dsj__eqxmd in join_node.get_live_right_vars())
    if not left_parallel:
        assert not any(array_dists[dsj__eqxmd.name] in fukz__aivk for
            dsj__eqxmd in join_node.get_live_left_vars())
    if not right_parallel:
        assert not any(array_dists[dsj__eqxmd.name] in fukz__aivk for
            dsj__eqxmd in join_node.get_live_right_vars())
    if left_parallel or right_parallel:
        assert all(array_dists[dsj__eqxmd.name] in fukz__aivk for
            dsj__eqxmd in join_node.get_live_out_vars())
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
    ysn__imhmv = set(left_col_nums)
    gnzf__jsjan = set(right_col_nums)
    scp__zocau = join_node.vect_same_key
    etz__ing = []
    for bzpg__pffh in range(len(left_key_types)):
        if left_key_in_output[bzpg__pffh]:
            etz__ing.append(needs_typechange(matched_key_types[bzpg__pffh],
                join_node.is_right, scp__zocau[bzpg__pffh]))
    vwt__rtw = len(left_key_types)
    dggbj__iloln = 0
    iufgf__qrt = left_physical_to_logical_list[len(left_key_types):]
    for bzpg__pffh, snr__ekngb in enumerate(iufgf__qrt):
        azxt__jvqx = True
        if snr__ekngb in ysn__imhmv:
            azxt__jvqx = left_key_in_output[vwt__rtw]
            vwt__rtw += 1
        if azxt__jvqx:
            etz__ing.append(needs_typechange(left_other_types[bzpg__pffh],
                join_node.is_right, False))
    for bzpg__pffh in range(len(right_key_types)):
        if not scp__zocau[bzpg__pffh] and not join_node.is_join:
            if right_key_in_output[dggbj__iloln]:
                etz__ing.append(needs_typechange(matched_key_types[
                    bzpg__pffh], join_node.is_left, False))
            dggbj__iloln += 1
    juudb__sprsp = right_physical_to_logical_list[len(right_key_types):]
    for bzpg__pffh, snr__ekngb in enumerate(juudb__sprsp):
        azxt__jvqx = True
        if snr__ekngb in gnzf__jsjan:
            azxt__jvqx = right_key_in_output[dggbj__iloln]
            dggbj__iloln += 1
        if azxt__jvqx:
            etz__ing.append(needs_typechange(right_other_types[bzpg__pffh],
                join_node.is_left, False))
    hyd__phf = len(left_key_types)
    func_text = '    # beginning of _gen_local_hash_join\n'
    if join_node.is_left_table:
        if join_node.has_live_left_table_var:
            iqu__ezue = left_other_names[1:]
            xmdn__tyg = left_other_names[0]
        else:
            iqu__ezue = left_other_names
            xmdn__tyg = None
        exz__ssht = '()' if len(iqu__ezue) == 0 else f'({iqu__ezue[0]},)'
        func_text += f"""    table_left = py_data_to_cpp_table({xmdn__tyg}, {exz__ssht}, left_in_cols, {join_node.n_left_table_cols})
"""
        glbs['left_in_cols'] = MetaType(tuple(left_physical_to_logical_list))
    else:
        epbx__ala = []
        for bzpg__pffh in range(hyd__phf):
            epbx__ala.append('t1_keys[{}]'.format(bzpg__pffh))
        for bzpg__pffh in range(len(left_other_names)):
            epbx__ala.append('data_left[{}]'.format(bzpg__pffh))
        func_text += '    info_list_total_l = [{}]\n'.format(','.join(
            'array_to_info({})'.format(bbv__has) for bbv__has in epbx__ala))
        func_text += (
            '    table_left = arr_info_list_to_table(info_list_total_l)\n')
    if join_node.is_right_table:
        if join_node.has_live_right_table_var:
            efw__kmnqu = right_other_names[1:]
            xmdn__tyg = right_other_names[0]
        else:
            efw__kmnqu = right_other_names
            xmdn__tyg = None
        exz__ssht = '()' if len(efw__kmnqu) == 0 else f'({efw__kmnqu[0]},)'
        func_text += f"""    table_right = py_data_to_cpp_table({xmdn__tyg}, {exz__ssht}, right_in_cols, {join_node.n_right_table_cols})
"""
        glbs['right_in_cols'] = MetaType(tuple(right_physical_to_logical_list))
    else:
        zowog__bfwj = []
        for bzpg__pffh in range(hyd__phf):
            zowog__bfwj.append('t2_keys[{}]'.format(bzpg__pffh))
        for bzpg__pffh in range(len(right_other_names)):
            zowog__bfwj.append('data_right[{}]'.format(bzpg__pffh))
        func_text += '    info_list_total_r = [{}]\n'.format(','.join(
            'array_to_info({})'.format(bbv__has) for bbv__has in zowog__bfwj))
        func_text += (
            '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    glbs['vect_same_key'] = np.array(scp__zocau, dtype=np.int64)
    glbs['vect_need_typechange'] = np.array(etz__ing, dtype=np.int64)
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
        .format(left_parallel, right_parallel, hyd__phf, len(iufgf__qrt),
        len(juudb__sprsp), join_node.is_left, join_node.is_right, join_node
        .is_join, join_node.extra_data_col_num != -1, join_node.
        indicator_col_num != -1, join_node.is_na_equal, len(left_col_nums),
        len(right_col_nums)))
    func_text += '    delete_table(table_left)\n'
    func_text += '    delete_table(table_right)\n'
    jkexq__batf = '(py_table_type, index_col_type)'
    func_text += f"""    out_data = cpp_table_to_py_data(out_table, out_col_inds, {jkexq__batf}, total_rows_np[0], {join_node.n_out_table_cols})
"""
    if join_node.has_live_out_table_var:
        func_text += f'    T = out_data[0]\n'
    else:
        func_text += f'    T = None\n'
    if join_node.has_live_out_index_var:
        koqy__ooyz = 1 if join_node.has_live_out_table_var else 0
        func_text += f'    index_var = out_data[{koqy__ooyz}]\n'
    else:
        func_text += f'    index_var = None\n'
    glbs['py_table_type'] = out_table_type
    glbs['index_col_type'] = index_col_type
    glbs['out_col_inds'] = MetaType(tuple(out_physical_to_logical_list))
    if bool(join_node.out_used_cols) or index_col_type != types.none:
        func_text += '    delete_table(out_table)\n'
    if out_table_type != types.none:
        ndk__eiktw = determine_table_cast_map(matched_key_types,
            left_key_types, left_used_key_nums, join_node.
            left_to_output_map, False)
        ndk__eiktw.update(determine_table_cast_map(matched_key_types,
            right_key_types, right_used_key_nums, join_node.
            right_to_output_map, False))
        emw__birtu = False
        pfg__xki = False
        if join_node.has_live_out_table_var:
            znok__tgq = list(out_table_type.arr_types)
        else:
            znok__tgq = None
        for evnzt__xoyy, msldp__yvx in ndk__eiktw.items():
            if evnzt__xoyy < join_node.n_out_table_cols:
                assert join_node.has_live_out_table_var, 'Casting columns for a dead table should not occur'
                znok__tgq[evnzt__xoyy] = msldp__yvx
                emw__birtu = True
            else:
                vqsd__vad = msldp__yvx
                pfg__xki = True
        if emw__birtu:
            func_text += f"""    T = bodo.utils.table_utils.table_astype(T, cast_table_type, False, _bodo_nan_to_str=False, used_cols=used_cols)
"""
            ixzv__ldb = bodo.TableType(tuple(znok__tgq))
            glbs['py_table_type'] = ixzv__ldb
            glbs['cast_table_type'] = out_table_type
            glbs['used_cols'] = MetaType(tuple(out_table_used_cols))
        if pfg__xki:
            glbs['index_col_type'] = vqsd__vad
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
    ndk__eiktw: Dict[int, types.Type] = {}
    hyd__phf = len(matched_key_types)
    for bzpg__pffh in range(hyd__phf):
        if used_key_nums is None or bzpg__pffh in used_key_nums:
            if matched_key_types[bzpg__pffh] != key_types[bzpg__pffh] and (
                convert_dict_col or key_types[bzpg__pffh] != bodo.
                dict_str_arr_type):
                koqy__ooyz = output_map[bzpg__pffh]
                ndk__eiktw[koqy__ooyz] = matched_key_types[bzpg__pffh]
    return ndk__eiktw


@numba.njit
def parallel_asof_comm(left_key_arrs, right_key_arrs, right_data):
    etuwd__jrmj = bodo.libs.distributed_api.get_size()
    dwr__jwb = np.empty(etuwd__jrmj, left_key_arrs[0].dtype)
    bft__xdv = np.empty(etuwd__jrmj, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(dwr__jwb, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(bft__xdv, left_key_arrs[0][-1])
    csr__ibt = np.zeros(etuwd__jrmj, np.int32)
    qoafu__kaydf = np.zeros(etuwd__jrmj, np.int32)
    gfq__cuovf = np.zeros(etuwd__jrmj, np.int32)
    rsvpd__xggoq = right_key_arrs[0][0]
    rua__ycrp = right_key_arrs[0][-1]
    muzxn__vbdy = -1
    bzpg__pffh = 0
    while bzpg__pffh < etuwd__jrmj - 1 and bft__xdv[bzpg__pffh] < rsvpd__xggoq:
        bzpg__pffh += 1
    while bzpg__pffh < etuwd__jrmj and dwr__jwb[bzpg__pffh] <= rua__ycrp:
        muzxn__vbdy, rwwva__remyw = _count_overlap(right_key_arrs[0],
            dwr__jwb[bzpg__pffh], bft__xdv[bzpg__pffh])
        if muzxn__vbdy != 0:
            muzxn__vbdy -= 1
            rwwva__remyw += 1
        csr__ibt[bzpg__pffh] = rwwva__remyw
        qoafu__kaydf[bzpg__pffh] = muzxn__vbdy
        bzpg__pffh += 1
    while bzpg__pffh < etuwd__jrmj:
        csr__ibt[bzpg__pffh] = 1
        qoafu__kaydf[bzpg__pffh] = len(right_key_arrs[0]) - 1
        bzpg__pffh += 1
    bodo.libs.distributed_api.alltoall(csr__ibt, gfq__cuovf, 1)
    jxgpo__teu = gfq__cuovf.sum()
    kzo__zftp = np.empty(jxgpo__teu, right_key_arrs[0].dtype)
    uov__ysrg = alloc_arr_tup(jxgpo__teu, right_data)
    rwy__lrt = bodo.ir.join.calc_disp(gfq__cuovf)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], kzo__zftp,
        csr__ibt, gfq__cuovf, qoafu__kaydf, rwy__lrt)
    bodo.libs.distributed_api.alltoallv_tup(right_data, uov__ysrg, csr__ibt,
        gfq__cuovf, qoafu__kaydf, rwy__lrt)
    return (kzo__zftp,), uov__ysrg


@numba.njit
def _count_overlap(r_key_arr, start, end):
    rwwva__remyw = 0
    muzxn__vbdy = 0
    cqhsa__diitp = 0
    while cqhsa__diitp < len(r_key_arr) and r_key_arr[cqhsa__diitp] < start:
        muzxn__vbdy += 1
        cqhsa__diitp += 1
    while cqhsa__diitp < len(r_key_arr) and start <= r_key_arr[cqhsa__diitp
        ] <= end:
        cqhsa__diitp += 1
        rwwva__remyw += 1
    return muzxn__vbdy, rwwva__remyw


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    ydan__sgc = np.empty_like(arr)
    ydan__sgc[0] = 0
    for bzpg__pffh in range(1, len(arr)):
        ydan__sgc[bzpg__pffh] = ydan__sgc[bzpg__pffh - 1] + arr[bzpg__pffh - 1]
    return ydan__sgc


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    rgw__jbczi = len(left_keys[0])
    nljre__eynu = len(right_keys[0])
    wgytk__pnrl = alloc_arr_tup(rgw__jbczi, left_keys)
    xvth__xkiyl = alloc_arr_tup(rgw__jbczi, right_keys)
    gxh__tnbmq = alloc_arr_tup(rgw__jbczi, data_left)
    aooeh__jgi = alloc_arr_tup(rgw__jbczi, data_right)
    kds__xyy = 0
    jojqn__muyq = 0
    for kds__xyy in range(rgw__jbczi):
        if jojqn__muyq < 0:
            jojqn__muyq = 0
        while jojqn__muyq < nljre__eynu and getitem_arr_tup(right_keys,
            jojqn__muyq) <= getitem_arr_tup(left_keys, kds__xyy):
            jojqn__muyq += 1
        jojqn__muyq -= 1
        setitem_arr_tup(wgytk__pnrl, kds__xyy, getitem_arr_tup(left_keys,
            kds__xyy))
        setitem_arr_tup(gxh__tnbmq, kds__xyy, getitem_arr_tup(data_left,
            kds__xyy))
        if jojqn__muyq >= 0:
            setitem_arr_tup(xvth__xkiyl, kds__xyy, getitem_arr_tup(
                right_keys, jojqn__muyq))
            setitem_arr_tup(aooeh__jgi, kds__xyy, getitem_arr_tup(
                data_right, jojqn__muyq))
        else:
            bodo.libs.array_kernels.setna_tup(xvth__xkiyl, kds__xyy)
            bodo.libs.array_kernels.setna_tup(aooeh__jgi, kds__xyy)
    return wgytk__pnrl, xvth__xkiyl, gxh__tnbmq, aooeh__jgi
