"""
Common IR extension functions for connectors such as CSV, Parquet and JSON readers.
"""
import sys
from collections import defaultdict
from typing import Literal, Set, Tuple
import numba
from numba.core import ir, types
from numba.core.ir_utils import replace_vars_inner, visit_vars_inner
from bodo.hiframes.table import TableType
from bodo.transforms.distributed_analysis import Distribution
from bodo.transforms.table_column_del_pass import get_live_column_nums_block
from bodo.utils.py_objs import install_py_obj_class
from bodo.utils.typing import BodoError
from bodo.utils.utils import debug_prints


def connector_array_analysis(node, equiv_set, typemap, array_analysis):
    ogtw__eqfn = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    ohsl__kbcy = []
    for ohw__kjm in node.out_vars:
        dii__ycor = typemap[ohw__kjm.name]
        if dii__ycor == types.none:
            continue
        cojvh__nidcp = array_analysis._gen_shape_call(equiv_set, ohw__kjm,
            dii__ycor.ndim, None, ogtw__eqfn)
        equiv_set.insert_equiv(ohw__kjm, cojvh__nidcp)
        ohsl__kbcy.append(cojvh__nidcp[0])
        equiv_set.define(ohw__kjm, set())
    if len(ohsl__kbcy) > 1:
        equiv_set.insert_equiv(*ohsl__kbcy)
    return [], ogtw__eqfn


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and not node.is_select_query:
        wkpkf__dbpdf = Distribution.REP
    elif isinstance(node, SqlReader) and node.limit is not None:
        wkpkf__dbpdf = Distribution.OneD_Var
    else:
        wkpkf__dbpdf = Distribution.OneD
    for jcd__ymnqk in node.out_vars:
        if jcd__ymnqk.name in array_dists:
            wkpkf__dbpdf = Distribution(min(wkpkf__dbpdf.value, array_dists
                [jcd__ymnqk.name].value))
    for jcd__ymnqk in node.out_vars:
        array_dists[jcd__ymnqk.name] = wkpkf__dbpdf


def connector_typeinfer(node, typeinferer):
    if node.connector_typ == 'csv':
        if node.chunksize is not None:
            typeinferer.lock_type(node.out_vars[0].name, node.out_types[0],
                loc=node.loc)
        else:
            typeinferer.lock_type(node.out_vars[0].name, TableType(tuple(
                node.out_types)), loc=node.loc)
            typeinferer.lock_type(node.out_vars[1].name, node.
                index_column_typ, loc=node.loc)
        return
    if node.connector_typ in ('parquet', 'sql'):
        typeinferer.lock_type(node.out_vars[0].name, TableType(tuple(node.
            out_types)), loc=node.loc)
        typeinferer.lock_type(node.out_vars[1].name, node.index_column_type,
            loc=node.loc)
        return
    for ohw__kjm, dii__ycor in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(ohw__kjm.name, dii__ycor, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    ojuos__aiun = []
    for ohw__kjm in node.out_vars:
        sfka__dnl = visit_vars_inner(ohw__kjm, callback, cbdata)
        ojuos__aiun.append(sfka__dnl)
    node.out_vars = ojuos__aiun
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for fdl__utjs in node.filters:
            for fsex__bnlv in range(len(fdl__utjs)):
                twn__iee = fdl__utjs[fsex__bnlv]
                fdl__utjs[fsex__bnlv] = twn__iee[0], twn__iee[1
                    ], visit_vars_inner(twn__iee[2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({jcd__ymnqk.name for jcd__ymnqk in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for aepx__tvhxz in node.filters:
            for jcd__ymnqk in aepx__tvhxz:
                if isinstance(jcd__ymnqk[2], ir.Var):
                    use_set.add(jcd__ymnqk[2].name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    tffp__gkpv = set(jcd__ymnqk.name for jcd__ymnqk in node.out_vars)
    return set(), tffp__gkpv


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    ojuos__aiun = []
    for ohw__kjm in node.out_vars:
        sfka__dnl = replace_vars_inner(ohw__kjm, var_dict)
        ojuos__aiun.append(sfka__dnl)
    node.out_vars = ojuos__aiun
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for fdl__utjs in node.filters:
            for fsex__bnlv in range(len(fdl__utjs)):
                twn__iee = fdl__utjs[fsex__bnlv]
                fdl__utjs[fsex__bnlv] = twn__iee[0], twn__iee[1
                    ], replace_vars_inner(twn__iee[2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for ohw__kjm in node.out_vars:
        ubtr__lvp = definitions[ohw__kjm.name]
        if node not in ubtr__lvp:
            ubtr__lvp.append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        filter_vars = []
        ykok__dcnb = [jcd__ymnqk[2] for aepx__tvhxz in filters for
            jcd__ymnqk in aepx__tvhxz]
        zvbe__jqsn = set()
        for cxx__nwld in ykok__dcnb:
            if isinstance(cxx__nwld, ir.Var):
                if cxx__nwld.name not in zvbe__jqsn:
                    filter_vars.append(cxx__nwld)
                zvbe__jqsn.add(cxx__nwld.name)
        return {jcd__ymnqk.name: f'f{fsex__bnlv}' for fsex__bnlv,
            jcd__ymnqk in enumerate(filter_vars)}, filter_vars
    else:
        return {}, []


this_module = sys.modules[__name__]
StreamReaderType = install_py_obj_class(types_name='stream_reader_type',
    module=this_module, class_name='StreamReaderType', model_name=
    'StreamReaderModel')


def trim_extra_used_columns(used_columns: Set, num_columns: int):
    return {fsex__bnlv for fsex__bnlv in used_columns if fsex__bnlv <
        num_columns}


def cast_float_to_nullable(df, df_type):
    import bodo
    fnnp__eybz = {}
    for fsex__bnlv, afe__hdz in enumerate(df_type.data):
        if isinstance(afe__hdz, bodo.IntegerArrayType):
            jirko__qnsf = afe__hdz.get_pandas_scalar_type_instance
            if jirko__qnsf not in fnnp__eybz:
                fnnp__eybz[jirko__qnsf] = []
            fnnp__eybz[jirko__qnsf].append(df.columns[fsex__bnlv])
    for dii__ycor, qmbf__vgki in fnnp__eybz.items():
        df[qmbf__vgki] = df[qmbf__vgki].astype(dii__ycor)


def connector_table_column_use(node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    return


def base_connector_remove_dead_columns(node, column_live_map, equiv_vars,
    typemap, nodename, possible_cols, require_one_column=True):
    assert len(node.out_vars) == 2, f'invalid {nodename} node'
    wwder__uuz = node.out_vars[0].name
    assert isinstance(typemap[wwder__uuz], TableType
        ), f'{nodename} Node Table must be a TableType'
    if possible_cols:
        used_columns, vdiun__kzwv, kmn__yxg = get_live_column_nums_block(
            column_live_map, equiv_vars, wwder__uuz)
        if not (vdiun__kzwv or kmn__yxg):
            used_columns = trim_extra_used_columns(used_columns, len(
                possible_cols))
            if not used_columns and require_one_column:
                used_columns = {0}
            if len(used_columns) != len(node.out_used_cols):
                node.out_used_cols = list(sorted(used_columns))
    """We return flase in all cases, as no changes performed in the file will allow for dead code elimination to do work."""
    return False


def is_connector_table_parallel(node, array_dists, typemap, node_name):
    rqzq__ceocq = False
    if array_dists is not None:
        aynaz__iults = node.out_vars[0].name
        rqzq__ceocq = array_dists[aynaz__iults] in (Distribution.OneD,
            Distribution.OneD_Var)
        grcr__slpny = node.out_vars[1].name
        assert typemap[grcr__slpny
            ] == types.none or not rqzq__ceocq or array_dists[grcr__slpny] in (
            Distribution.OneD, Distribution.OneD_Var
            ), f'{node_name} data/index parallelization does not match'
    return rqzq__ceocq


def generate_arrow_filters(filters, filter_map, filter_vars, col_names,
    partition_names, original_out_types, typemap, source: Literal['parquet',
    'iceberg'], output_dnf=True) ->Tuple[str, str]:
    guves__exh = 'None'
    lvmg__csw = 'None'
    if filters:
        chmeh__fwgk = []
        dwx__lje = []
        uwlw__uqkru = False
        orig_colname_map = {bdms__lydc: fsex__bnlv for fsex__bnlv,
            bdms__lydc in enumerate(col_names)}
        for fdl__utjs in filters:
            wgafa__mdwlk = []
            zdo__tvi = []
            for jcd__ymnqk in fdl__utjs:
                if isinstance(jcd__ymnqk[2], ir.Var):
                    rsnek__ezma, iqpjp__xzxq = determine_filter_cast(
                        original_out_types, typemap, jcd__ymnqk,
                        orig_colname_map, partition_names, source)
                    if jcd__ymnqk[1] == 'in':
                        smma__lrz = (
                            f"(ds.field('{jcd__ymnqk[0]}').isin({filter_map[jcd__ymnqk[2].name]}))"
                            )
                    else:
                        smma__lrz = (
                            f"(ds.field('{jcd__ymnqk[0]}'){rsnek__ezma} {jcd__ymnqk[1]} ds.scalar({filter_map[jcd__ymnqk[2].name]}){iqpjp__xzxq})"
                            )
                else:
                    assert jcd__ymnqk[2
                        ] == 'NULL', 'unsupport constant used in filter pushdown'
                    if jcd__ymnqk[1] == 'is not':
                        wrm__cyif = '~'
                    else:
                        wrm__cyif = ''
                    smma__lrz = (
                        f"({wrm__cyif}ds.field('{jcd__ymnqk[0]}').is_null())")
                zdo__tvi.append(smma__lrz)
                if not uwlw__uqkru:
                    if jcd__ymnqk[0] in partition_names and isinstance(
                        jcd__ymnqk[2], ir.Var):
                        if output_dnf:
                            uah__arwdw = (
                                f"('{jcd__ymnqk[0]}', '{jcd__ymnqk[1]}', {filter_map[jcd__ymnqk[2].name]})"
                                )
                        else:
                            uah__arwdw = smma__lrz
                        wgafa__mdwlk.append(uah__arwdw)
                    elif jcd__ymnqk[0] in partition_names and not isinstance(
                        jcd__ymnqk[2], ir.Var) and source == 'iceberg':
                        if output_dnf:
                            uah__arwdw = (
                                f"('{jcd__ymnqk[0]}', '{jcd__ymnqk[1]}', '{jcd__ymnqk[2]}')"
                                )
                        else:
                            uah__arwdw = smma__lrz
                        wgafa__mdwlk.append(uah__arwdw)
            gff__rcs = ''
            if wgafa__mdwlk:
                if output_dnf:
                    gff__rcs = ', '.join(wgafa__mdwlk)
                else:
                    gff__rcs = ' & '.join(wgafa__mdwlk)
            else:
                uwlw__uqkru = True
            wtb__cloa = ' & '.join(zdo__tvi)
            if gff__rcs:
                if output_dnf:
                    chmeh__fwgk.append(f'[{gff__rcs}]')
                else:
                    chmeh__fwgk.append(f'({gff__rcs})')
            dwx__lje.append(f'({wtb__cloa})')
        if output_dnf:
            qdre__cncwl = ', '.join(chmeh__fwgk)
        else:
            qdre__cncwl = ' | '.join(chmeh__fwgk)
        bzg__aszg = ' | '.join(dwx__lje)
        if qdre__cncwl and not uwlw__uqkru:
            if output_dnf:
                guves__exh = f'[{qdre__cncwl}]'
            else:
                guves__exh = f'({qdre__cncwl})'
        lvmg__csw = f'({bzg__aszg})'
    return guves__exh, lvmg__csw


def determine_filter_cast(col_types, typemap, filter_val, orig_colname_map,
    partition_names, source):
    import bodo
    hfiuj__zdg = filter_val[0]
    oghx__efb = col_types[orig_colname_map[hfiuj__zdg]]
    ehdop__avvm = bodo.utils.typing.element_type(oghx__efb)
    if source == 'parquet' and hfiuj__zdg in partition_names:
        if ehdop__avvm == types.unicode_type:
            thx__bxykv = '.cast(pyarrow.string(), safe=False)'
        elif isinstance(ehdop__avvm, types.Integer):
            thx__bxykv = f'.cast(pyarrow.{ehdop__avvm.name}(), safe=False)'
        else:
            thx__bxykv = ''
    else:
        thx__bxykv = ''
    crh__veto = typemap[filter_val[2].name]
    if isinstance(crh__veto, (types.List, types.Set)):
        ipc__ventd = crh__veto.dtype
    else:
        ipc__ventd = crh__veto
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(ehdop__avvm,
        'Filter pushdown')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(ipc__ventd,
        'Filter pushdown')
    if not bodo.utils.typing.is_common_scalar_dtype([ehdop__avvm, ipc__ventd]):
        if not bodo.utils.typing.is_safe_arrow_cast(ehdop__avvm, ipc__ventd):
            raise BodoError(
                f'Unsupported Arrow cast from {ehdop__avvm} to {ipc__ventd} in filter pushdown. Please try a comparison that avoids casting the column.'
                )
        if ehdop__avvm == types.unicode_type and ipc__ventd in (bodo.
            datetime64ns, bodo.pd_timestamp_type):
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif ipc__ventd == types.unicode_type and ehdop__avvm in (bodo.
            datetime64ns, bodo.pd_timestamp_type):
            if isinstance(crh__veto, (types.List, types.Set)):
                ekswg__ykv = 'list' if isinstance(crh__veto, types.List
                    ) else 'tuple'
                raise BodoError(
                    f'Cannot cast {ekswg__ykv} values with isin filter pushdown.'
                    )
            return thx__bxykv, ".cast(pyarrow.timestamp('ns'), safe=False)"
        elif ehdop__avvm == bodo.datetime_date_type and ipc__ventd in (bodo
            .datetime64ns, bodo.pd_timestamp_type):
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif ipc__ventd == bodo.datetime_date_type and ehdop__avvm in (bodo
            .datetime64ns, bodo.pd_timestamp_type):
            return thx__bxykv, ".cast(pyarrow.timestamp('ns'), safe=False)"
    return thx__bxykv, ''
