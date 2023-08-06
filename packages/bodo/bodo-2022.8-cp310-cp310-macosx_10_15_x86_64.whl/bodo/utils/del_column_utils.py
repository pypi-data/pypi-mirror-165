"""Helper information to keep table column deletion
pass organized. This contains information about all
table operations for optimizations.
"""
from typing import Dict, Tuple
from numba.core import ir, types
from bodo.hiframes.table import TableType
table_usecol_funcs = {('get_table_data', 'bodo.hiframes.table'), (
    'table_filter', 'bodo.hiframes.table'), ('table_subset',
    'bodo.hiframes.table'), ('set_table_data', 'bodo.hiframes.table'), (
    'set_table_data_null', 'bodo.hiframes.table'), (
    'generate_mappable_table_func', 'bodo.utils.table_utils'), (
    'table_astype', 'bodo.utils.table_utils'), ('generate_table_nbytes',
    'bodo.utils.table_utils'), ('table_concat', 'bodo.utils.table_utils'),
    ('py_data_to_cpp_table', 'bodo.libs.array'), ('logical_table_to_table',
    'bodo.hiframes.table')}


def is_table_use_column_ops(fdef: Tuple[str, str], args, typemap):
    return fdef in table_usecol_funcs and len(args) > 0 and isinstance(typemap
        [args[0].name], TableType)


def get_table_used_columns(fdef: Tuple[str, str], call_expr: ir.Expr,
    typemap: Dict[str, types.Type]):
    if fdef == ('get_table_data', 'bodo.hiframes.table'):
        yba__jibq = typemap[call_expr.args[1].name].literal_value
        return {yba__jibq}
    elif fdef in {('table_filter', 'bodo.hiframes.table'), ('table_astype',
        'bodo.utils.table_utils'), ('generate_mappable_table_func',
        'bodo.utils.table_utils'), ('set_table_data', 'bodo.hiframes.table'
        ), ('set_table_data_null', 'bodo.hiframes.table')}:
        ealzo__wgzuf = dict(call_expr.kws)
        if 'used_cols' in ealzo__wgzuf:
            jgohp__uck = ealzo__wgzuf['used_cols']
            uxg__qhb = typemap[jgohp__uck.name]
            uxg__qhb = uxg__qhb.instance_type
            return set(uxg__qhb.meta)
    elif fdef == ('table_concat', 'bodo.utils.table_utils'):
        jgohp__uck = call_expr.args[1]
        uxg__qhb = typemap[jgohp__uck.name]
        uxg__qhb = uxg__qhb.instance_type
        return set(uxg__qhb.meta)
    elif fdef == ('table_subset', 'bodo.hiframes.table'):
        lto__bejux = call_expr.args[1]
        wpw__kisyk = typemap[lto__bejux.name]
        wpw__kisyk = wpw__kisyk.instance_type
        ydd__hlcer = wpw__kisyk.meta
        ealzo__wgzuf = dict(call_expr.kws)
        if 'used_cols' in ealzo__wgzuf:
            jgohp__uck = ealzo__wgzuf['used_cols']
            uxg__qhb = typemap[jgohp__uck.name]
            uxg__qhb = uxg__qhb.instance_type
            zzba__mdrgf = set(uxg__qhb.meta)
            lhyim__sqv = set()
            for oigbk__mqxdf, rnmls__aer in enumerate(ydd__hlcer):
                if oigbk__mqxdf in zzba__mdrgf:
                    lhyim__sqv.add(rnmls__aer)
            return lhyim__sqv
        else:
            return set(ydd__hlcer)
    elif fdef == ('py_data_to_cpp_table', 'bodo.libs.array'):
        dif__dpti = typemap[call_expr.args[2].name].instance_type.meta
        cwi__lkgp = len(typemap[call_expr.args[0].name].arr_types)
        return set(oigbk__mqxdf for oigbk__mqxdf in dif__dpti if 
            oigbk__mqxdf < cwi__lkgp)
    elif fdef == ('logical_table_to_table', 'bodo.hiframes.table'):
        jej__yqyn = typemap[call_expr.args[2].name].instance_type.meta
        jspa__kxpf = len(typemap[call_expr.args[0].name].arr_types)
        ealzo__wgzuf = dict(call_expr.kws)
        if 'used_cols' in ealzo__wgzuf:
            zzba__mdrgf = set(typemap[ealzo__wgzuf['used_cols'].name].
                instance_type.meta)
            ybfwi__gxcvj = set()
            for mitb__abz, cgpo__gzzk in enumerate(jej__yqyn):
                if mitb__abz in zzba__mdrgf and cgpo__gzzk < jspa__kxpf:
                    ybfwi__gxcvj.add(cgpo__gzzk)
            return ybfwi__gxcvj
        else:
            return set(oigbk__mqxdf for oigbk__mqxdf in jej__yqyn if 
                oigbk__mqxdf < jspa__kxpf)
    return None
