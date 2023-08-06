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
    siyuz__qga = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    xai__diy = []
    for ezo__hxprw in node.out_vars:
        fmy__poqi = typemap[ezo__hxprw.name]
        if fmy__poqi == types.none:
            continue
        ufvi__lwua = array_analysis._gen_shape_call(equiv_set, ezo__hxprw,
            fmy__poqi.ndim, None, siyuz__qga)
        equiv_set.insert_equiv(ezo__hxprw, ufvi__lwua)
        xai__diy.append(ufvi__lwua[0])
        equiv_set.define(ezo__hxprw, set())
    if len(xai__diy) > 1:
        equiv_set.insert_equiv(*xai__diy)
    return [], siyuz__qga


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and not node.is_select_query:
        evn__dkaxs = Distribution.REP
    elif isinstance(node, SqlReader) and node.limit is not None:
        evn__dkaxs = Distribution.OneD_Var
    else:
        evn__dkaxs = Distribution.OneD
    for xvpi__jjbt in node.out_vars:
        if xvpi__jjbt.name in array_dists:
            evn__dkaxs = Distribution(min(evn__dkaxs.value, array_dists[
                xvpi__jjbt.name].value))
    for xvpi__jjbt in node.out_vars:
        array_dists[xvpi__jjbt.name] = evn__dkaxs


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
    for ezo__hxprw, fmy__poqi in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(ezo__hxprw.name, fmy__poqi, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    onzr__bcy = []
    for ezo__hxprw in node.out_vars:
        syz__tofvn = visit_vars_inner(ezo__hxprw, callback, cbdata)
        onzr__bcy.append(syz__tofvn)
    node.out_vars = onzr__bcy
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for xtkt__hrfvr in node.filters:
            for eufk__vmfq in range(len(xtkt__hrfvr)):
                hefrt__rsw = xtkt__hrfvr[eufk__vmfq]
                xtkt__hrfvr[eufk__vmfq] = hefrt__rsw[0], hefrt__rsw[1
                    ], visit_vars_inner(hefrt__rsw[2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({xvpi__jjbt.name for xvpi__jjbt in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for pbah__uax in node.filters:
            for xvpi__jjbt in pbah__uax:
                if isinstance(xvpi__jjbt[2], ir.Var):
                    use_set.add(xvpi__jjbt[2].name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    xzx__gfjc = set(xvpi__jjbt.name for xvpi__jjbt in node.out_vars)
    return set(), xzx__gfjc


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    onzr__bcy = []
    for ezo__hxprw in node.out_vars:
        syz__tofvn = replace_vars_inner(ezo__hxprw, var_dict)
        onzr__bcy.append(syz__tofvn)
    node.out_vars = onzr__bcy
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for xtkt__hrfvr in node.filters:
            for eufk__vmfq in range(len(xtkt__hrfvr)):
                hefrt__rsw = xtkt__hrfvr[eufk__vmfq]
                xtkt__hrfvr[eufk__vmfq] = hefrt__rsw[0], hefrt__rsw[1
                    ], replace_vars_inner(hefrt__rsw[2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for ezo__hxprw in node.out_vars:
        kyvvu__ewc = definitions[ezo__hxprw.name]
        if node not in kyvvu__ewc:
            kyvvu__ewc.append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        filter_vars = []
        hengb__jxzu = [xvpi__jjbt[2] for pbah__uax in filters for
            xvpi__jjbt in pbah__uax]
        quqv__hhvel = set()
        for bol__rivwx in hengb__jxzu:
            if isinstance(bol__rivwx, ir.Var):
                if bol__rivwx.name not in quqv__hhvel:
                    filter_vars.append(bol__rivwx)
                quqv__hhvel.add(bol__rivwx.name)
        return {xvpi__jjbt.name: f'f{eufk__vmfq}' for eufk__vmfq,
            xvpi__jjbt in enumerate(filter_vars)}, filter_vars
    else:
        return {}, []


this_module = sys.modules[__name__]
StreamReaderType = install_py_obj_class(types_name='stream_reader_type',
    module=this_module, class_name='StreamReaderType', model_name=
    'StreamReaderModel')


def trim_extra_used_columns(used_columns: Set, num_columns: int):
    return {eufk__vmfq for eufk__vmfq in used_columns if eufk__vmfq <
        num_columns}


def cast_float_to_nullable(df, df_type):
    import bodo
    oxf__izn = {}
    for eufk__vmfq, twod__rds in enumerate(df_type.data):
        if isinstance(twod__rds, bodo.IntegerArrayType):
            htr__yvpxl = twod__rds.get_pandas_scalar_type_instance
            if htr__yvpxl not in oxf__izn:
                oxf__izn[htr__yvpxl] = []
            oxf__izn[htr__yvpxl].append(df.columns[eufk__vmfq])
    for fmy__poqi, plb__mij in oxf__izn.items():
        df[plb__mij] = df[plb__mij].astype(fmy__poqi)


def connector_table_column_use(node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    return


def base_connector_remove_dead_columns(node, column_live_map, equiv_vars,
    typemap, nodename, possible_cols, require_one_column=True):
    assert len(node.out_vars) == 2, f'invalid {nodename} node'
    wfxk__gqh = node.out_vars[0].name
    assert isinstance(typemap[wfxk__gqh], TableType
        ), f'{nodename} Node Table must be a TableType'
    if possible_cols:
        used_columns, jxe__igyne, efrum__kzhun = get_live_column_nums_block(
            column_live_map, equiv_vars, wfxk__gqh)
        if not (jxe__igyne or efrum__kzhun):
            used_columns = trim_extra_used_columns(used_columns, len(
                possible_cols))
            if not used_columns and require_one_column:
                used_columns = {0}
            if len(used_columns) != len(node.out_used_cols):
                node.out_used_cols = list(sorted(used_columns))
    """We return flase in all cases, as no changes performed in the file will allow for dead code elimination to do work."""
    return False


def is_connector_table_parallel(node, array_dists, typemap, node_name):
    fdsb__brifl = False
    if array_dists is not None:
        nwngx__yvz = node.out_vars[0].name
        fdsb__brifl = array_dists[nwngx__yvz] in (Distribution.OneD,
            Distribution.OneD_Var)
        cvq__alvyz = node.out_vars[1].name
        assert typemap[cvq__alvyz
            ] == types.none or not fdsb__brifl or array_dists[cvq__alvyz] in (
            Distribution.OneD, Distribution.OneD_Var
            ), f'{node_name} data/index parallelization does not match'
    return fdsb__brifl


def generate_arrow_filters(filters, filter_map, filter_vars, col_names,
    partition_names, original_out_types, typemap, source: Literal['parquet',
    'iceberg'], output_dnf=True) ->Tuple[str, str]:
    aehi__kcvxg = 'None'
    xmug__wfco = 'None'
    if filters:
        sddxw__tgpiy = []
        erhxn__ogkul = []
        tlaj__rzsx = False
        orig_colname_map = {qzdzt__pavz: eufk__vmfq for eufk__vmfq,
            qzdzt__pavz in enumerate(col_names)}
        for xtkt__hrfvr in filters:
            dawh__wzsbc = []
            dyp__quae = []
            for xvpi__jjbt in xtkt__hrfvr:
                if isinstance(xvpi__jjbt[2], ir.Var):
                    ubohr__cexbu, fdze__arxbb = determine_filter_cast(
                        original_out_types, typemap, xvpi__jjbt,
                        orig_colname_map, partition_names, source)
                    if xvpi__jjbt[1] == 'in':
                        fmym__aebq = (
                            f"(ds.field('{xvpi__jjbt[0]}').isin({filter_map[xvpi__jjbt[2].name]}))"
                            )
                    else:
                        fmym__aebq = (
                            f"(ds.field('{xvpi__jjbt[0]}'){ubohr__cexbu} {xvpi__jjbt[1]} ds.scalar({filter_map[xvpi__jjbt[2].name]}){fdze__arxbb})"
                            )
                else:
                    assert xvpi__jjbt[2
                        ] == 'NULL', 'unsupport constant used in filter pushdown'
                    if xvpi__jjbt[1] == 'is not':
                        wmww__ekjcj = '~'
                    else:
                        wmww__ekjcj = ''
                    fmym__aebq = (
                        f"({wmww__ekjcj}ds.field('{xvpi__jjbt[0]}').is_null())"
                        )
                dyp__quae.append(fmym__aebq)
                if not tlaj__rzsx:
                    if xvpi__jjbt[0] in partition_names and isinstance(
                        xvpi__jjbt[2], ir.Var):
                        if output_dnf:
                            qhjh__hcfkp = (
                                f"('{xvpi__jjbt[0]}', '{xvpi__jjbt[1]}', {filter_map[xvpi__jjbt[2].name]})"
                                )
                        else:
                            qhjh__hcfkp = fmym__aebq
                        dawh__wzsbc.append(qhjh__hcfkp)
                    elif xvpi__jjbt[0] in partition_names and not isinstance(
                        xvpi__jjbt[2], ir.Var) and source == 'iceberg':
                        if output_dnf:
                            qhjh__hcfkp = (
                                f"('{xvpi__jjbt[0]}', '{xvpi__jjbt[1]}', '{xvpi__jjbt[2]}')"
                                )
                        else:
                            qhjh__hcfkp = fmym__aebq
                        dawh__wzsbc.append(qhjh__hcfkp)
            anav__xcx = ''
            if dawh__wzsbc:
                if output_dnf:
                    anav__xcx = ', '.join(dawh__wzsbc)
                else:
                    anav__xcx = ' & '.join(dawh__wzsbc)
            else:
                tlaj__rzsx = True
            jyxk__wugs = ' & '.join(dyp__quae)
            if anav__xcx:
                if output_dnf:
                    sddxw__tgpiy.append(f'[{anav__xcx}]')
                else:
                    sddxw__tgpiy.append(f'({anav__xcx})')
            erhxn__ogkul.append(f'({jyxk__wugs})')
        if output_dnf:
            llp__eqito = ', '.join(sddxw__tgpiy)
        else:
            llp__eqito = ' | '.join(sddxw__tgpiy)
        edac__ufz = ' | '.join(erhxn__ogkul)
        if llp__eqito and not tlaj__rzsx:
            if output_dnf:
                aehi__kcvxg = f'[{llp__eqito}]'
            else:
                aehi__kcvxg = f'({llp__eqito})'
        xmug__wfco = f'({edac__ufz})'
    return aehi__kcvxg, xmug__wfco


def determine_filter_cast(col_types, typemap, filter_val, orig_colname_map,
    partition_names, source):
    import bodo
    blysm__eyp = filter_val[0]
    tyw__vwtk = col_types[orig_colname_map[blysm__eyp]]
    aqx__fbzt = bodo.utils.typing.element_type(tyw__vwtk)
    if source == 'parquet' and blysm__eyp in partition_names:
        if aqx__fbzt == types.unicode_type:
            wxd__wsu = '.cast(pyarrow.string(), safe=False)'
        elif isinstance(aqx__fbzt, types.Integer):
            wxd__wsu = f'.cast(pyarrow.{aqx__fbzt.name}(), safe=False)'
        else:
            wxd__wsu = ''
    else:
        wxd__wsu = ''
    utv__ydm = typemap[filter_val[2].name]
    if isinstance(utv__ydm, (types.List, types.Set)):
        pwp__tsu = utv__ydm.dtype
    else:
        pwp__tsu = utv__ydm
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(aqx__fbzt,
        'Filter pushdown')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(pwp__tsu,
        'Filter pushdown')
    if not bodo.utils.typing.is_common_scalar_dtype([aqx__fbzt, pwp__tsu]):
        if not bodo.utils.typing.is_safe_arrow_cast(aqx__fbzt, pwp__tsu):
            raise BodoError(
                f'Unsupported Arrow cast from {aqx__fbzt} to {pwp__tsu} in filter pushdown. Please try a comparison that avoids casting the column.'
                )
        if aqx__fbzt == types.unicode_type and pwp__tsu in (bodo.
            datetime64ns, bodo.pd_timestamp_type):
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif pwp__tsu == types.unicode_type and aqx__fbzt in (bodo.
            datetime64ns, bodo.pd_timestamp_type):
            if isinstance(utv__ydm, (types.List, types.Set)):
                fuw__fmzly = 'list' if isinstance(utv__ydm, types.List
                    ) else 'tuple'
                raise BodoError(
                    f'Cannot cast {fuw__fmzly} values with isin filter pushdown.'
                    )
            return wxd__wsu, ".cast(pyarrow.timestamp('ns'), safe=False)"
        elif aqx__fbzt == bodo.datetime_date_type and pwp__tsu in (bodo.
            datetime64ns, bodo.pd_timestamp_type):
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif pwp__tsu == bodo.datetime_date_type and aqx__fbzt in (bodo.
            datetime64ns, bodo.pd_timestamp_type):
            return wxd__wsu, ".cast(pyarrow.timestamp('ns'), safe=False)"
    return wxd__wsu, ''
