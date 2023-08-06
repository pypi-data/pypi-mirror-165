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
        ephbw__xhhd = typemap[call_expr.args[1].name].literal_value
        return {ephbw__xhhd}
    elif fdef in {('table_filter', 'bodo.hiframes.table'), ('table_astype',
        'bodo.utils.table_utils'), ('generate_mappable_table_func',
        'bodo.utils.table_utils'), ('set_table_data', 'bodo.hiframes.table'
        ), ('set_table_data_null', 'bodo.hiframes.table')}:
        pty__tfmr = dict(call_expr.kws)
        if 'used_cols' in pty__tfmr:
            rav__yjn = pty__tfmr['used_cols']
            omm__exa = typemap[rav__yjn.name]
            omm__exa = omm__exa.instance_type
            return set(omm__exa.meta)
    elif fdef == ('table_concat', 'bodo.utils.table_utils'):
        rav__yjn = call_expr.args[1]
        omm__exa = typemap[rav__yjn.name]
        omm__exa = omm__exa.instance_type
        return set(omm__exa.meta)
    elif fdef == ('table_subset', 'bodo.hiframes.table'):
        mzqhi__hkf = call_expr.args[1]
        vpc__dvud = typemap[mzqhi__hkf.name]
        vpc__dvud = vpc__dvud.instance_type
        jdfc__qlpyj = vpc__dvud.meta
        pty__tfmr = dict(call_expr.kws)
        if 'used_cols' in pty__tfmr:
            rav__yjn = pty__tfmr['used_cols']
            omm__exa = typemap[rav__yjn.name]
            omm__exa = omm__exa.instance_type
            njhxd__pacjv = set(omm__exa.meta)
            xvjc__nrmmx = set()
            for yossg__tmk, achfv__cnab in enumerate(jdfc__qlpyj):
                if yossg__tmk in njhxd__pacjv:
                    xvjc__nrmmx.add(achfv__cnab)
            return xvjc__nrmmx
        else:
            return set(jdfc__qlpyj)
    elif fdef == ('py_data_to_cpp_table', 'bodo.libs.array'):
        kxytl__cypig = typemap[call_expr.args[2].name].instance_type.meta
        edn__znieu = len(typemap[call_expr.args[0].name].arr_types)
        return set(yossg__tmk for yossg__tmk in kxytl__cypig if yossg__tmk <
            edn__znieu)
    elif fdef == ('logical_table_to_table', 'bodo.hiframes.table'):
        czkk__oqima = typemap[call_expr.args[2].name].instance_type.meta
        zvgzx__vln = len(typemap[call_expr.args[0].name].arr_types)
        pty__tfmr = dict(call_expr.kws)
        if 'used_cols' in pty__tfmr:
            njhxd__pacjv = set(typemap[pty__tfmr['used_cols'].name].
                instance_type.meta)
            kwerh__fpw = set()
            for jyud__oyu, miw__gkk in enumerate(czkk__oqima):
                if jyud__oyu in njhxd__pacjv and miw__gkk < zvgzx__vln:
                    kwerh__fpw.add(miw__gkk)
            return kwerh__fpw
        else:
            return set(yossg__tmk for yossg__tmk in czkk__oqima if 
                yossg__tmk < zvgzx__vln)
    return None
