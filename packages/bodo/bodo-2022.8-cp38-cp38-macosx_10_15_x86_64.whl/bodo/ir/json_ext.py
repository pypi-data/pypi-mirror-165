import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes
from numba.extending import intrinsic
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.io.fs_io import get_storage_options_pyobject, storage_options_dict_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.utils.utils import check_and_propagate_cpp_exception, check_java_installation, sanitize_varname


class JsonReader(ir.Stmt):

    def __init__(self, df_out, loc, out_vars, out_types, file_name,
        df_colnames, orient, convert_dates, precise_float, lines,
        compression, storage_options):
        self.connector_typ = 'json'
        self.df_out = df_out
        self.loc = loc
        self.out_vars = out_vars
        self.out_types = out_types
        self.file_name = file_name
        self.df_colnames = df_colnames
        self.orient = orient
        self.convert_dates = convert_dates
        self.precise_float = precise_float
        self.lines = lines
        self.compression = compression
        self.storage_options = storage_options

    def __repr__(self):
        return ('{} = ReadJson(file={}, col_names={}, types={}, vars={})'.
            format(self.df_out, self.file_name, self.df_colnames, self.
            out_types, self.out_vars))


import llvmlite.binding as ll
from bodo.io import json_cpp
ll.add_symbol('json_file_chunk_reader', json_cpp.json_file_chunk_reader)


@intrinsic
def json_file_chunk_reader(typingctx, fname_t, lines_t, is_parallel_t,
    nrows_t, compression_t, bucket_region_t, storage_options_t):
    assert storage_options_t == storage_options_dict_type, "Storage options don't match expected type"

    def codegen(context, builder, sig, args):
        kxu__tgz = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        pzu__zxw = cgutils.get_or_insert_function(builder.module, kxu__tgz,
            name='json_file_chunk_reader')
        szy__alx = builder.call(pzu__zxw, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        jadc__sfvwg = cgutils.create_struct_proxy(types.stream_reader_type)(
            context, builder)
        puitl__pog = context.get_python_api(builder)
        jadc__sfvwg.meminfo = puitl__pog.nrt_meminfo_new_from_pyobject(context
            .get_constant_null(types.voidptr), szy__alx)
        jadc__sfvwg.pyobj = szy__alx
        puitl__pog.decref(szy__alx)
        return jadc__sfvwg._getvalue()
    return types.stream_reader_type(types.voidptr, types.bool_, types.bool_,
        types.int64, types.voidptr, types.voidptr, storage_options_dict_type
        ), codegen


def remove_dead_json(json_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    lhdz__bmy = []
    utpnv__uhmx = []
    akm__dhy = []
    for ftxq__zyo, mwxw__utx in enumerate(json_node.out_vars):
        if mwxw__utx.name in lives:
            lhdz__bmy.append(json_node.df_colnames[ftxq__zyo])
            utpnv__uhmx.append(json_node.out_vars[ftxq__zyo])
            akm__dhy.append(json_node.out_types[ftxq__zyo])
    json_node.df_colnames = lhdz__bmy
    json_node.out_vars = utpnv__uhmx
    json_node.out_types = akm__dhy
    if len(json_node.out_vars) == 0:
        return None
    return json_node


def json_distributed_run(json_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        nargn__gzgbk = (
            'Finish column pruning on read_json node:\n%s\nColumns loaded %s\n'
            )
        zphcc__sgm = json_node.loc.strformat()
        yne__wal = json_node.df_colnames
        bodo.user_logging.log_message('Column Pruning', nargn__gzgbk,
            zphcc__sgm, yne__wal)
        ffm__ppst = [pxeb__fqsfw for ftxq__zyo, pxeb__fqsfw in enumerate(
            json_node.df_colnames) if isinstance(json_node.out_types[
            ftxq__zyo], bodo.libs.dict_arr_ext.DictionaryArrayType)]
        if ffm__ppst:
            dhvt__fge = """Finished optimized encoding on read_json node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', dhvt__fge,
                zphcc__sgm, ffm__ppst)
    parallel = False
    if array_dists is not None:
        parallel = True
        for vegr__jfrg in json_node.out_vars:
            if array_dists[vegr__jfrg.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                vegr__jfrg.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    zbatu__eie = len(json_node.out_vars)
    pum__dpj = ', '.join('arr' + str(ftxq__zyo) for ftxq__zyo in range(
        zbatu__eie))
    con__uee = 'def json_impl(fname):\n'
    con__uee += '    ({},) = _json_reader_py(fname)\n'.format(pum__dpj)
    nicwo__mkce = {}
    exec(con__uee, {}, nicwo__mkce)
    klbd__cbjnn = nicwo__mkce['json_impl']
    xnjs__uzpu = _gen_json_reader_py(json_node.df_colnames, json_node.
        out_types, typingctx, targetctx, parallel, json_node.orient,
        json_node.convert_dates, json_node.precise_float, json_node.lines,
        json_node.compression, json_node.storage_options)
    tqxpx__bglye = compile_to_numba_ir(klbd__cbjnn, {'_json_reader_py':
        xnjs__uzpu}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type,), typemap=typemap, calltypes=calltypes).blocks.popitem()[1
        ]
    replace_arg_nodes(tqxpx__bglye, [json_node.file_name])
    wxo__xhni = tqxpx__bglye.body[:-3]
    for ftxq__zyo in range(len(json_node.out_vars)):
        wxo__xhni[-len(json_node.out_vars) + ftxq__zyo
            ].target = json_node.out_vars[ftxq__zyo]
    return wxo__xhni


numba.parfors.array_analysis.array_analysis_extensions[JsonReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[JsonReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[JsonReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[JsonReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[JsonReader] = remove_dead_json
numba.core.analysis.ir_extension_usedefs[JsonReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[JsonReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[JsonReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[JsonReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[JsonReader] = json_distributed_run
compiled_funcs = []


def _gen_json_reader_py(col_names, col_typs, typingctx, targetctx, parallel,
    orient, convert_dates, precise_float, lines, compression, storage_options):
    hsrar__akkzf = [sanitize_varname(pxeb__fqsfw) for pxeb__fqsfw in col_names]
    jcbb__mfuoi = ', '.join(str(ftxq__zyo) for ftxq__zyo, bbr__osa in
        enumerate(col_typs) if bbr__osa.dtype == types.NPDatetime('ns'))
    wyr__sedkl = ', '.join(["{}='{}'".format(gabre__emygp, bodo.ir.csv_ext.
        _get_dtype_str(bbr__osa)) for gabre__emygp, bbr__osa in zip(
        hsrar__akkzf, col_typs)])
    nxi__suh = ', '.join(["'{}':{}".format(ycmww__nok, bodo.ir.csv_ext.
        _get_pd_dtype_str(bbr__osa)) for ycmww__nok, bbr__osa in zip(
        col_names, col_typs)])
    if compression is None:
        compression = 'uncompressed'
    con__uee = 'def json_reader_py(fname):\n'
    con__uee += '  df_typeref_2 = df_typeref\n'
    con__uee += '  check_java_installation(fname)\n'
    con__uee += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    con__uee += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    con__uee += (
        '  f_reader = bodo.ir.json_ext.json_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    con__uee += (
        """    {}, {}, -1, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py )
"""
        .format(lines, parallel, compression))
    con__uee += '  if bodo.utils.utils.is_null_pointer(f_reader._pyobj):\n'
    con__uee += "      raise FileNotFoundError('File does not exist')\n"
    con__uee += f'  with objmode({wyr__sedkl}):\n'
    con__uee += f"    df = pd.read_json(f_reader, orient='{orient}',\n"
    con__uee += f'       convert_dates = {convert_dates}, \n'
    con__uee += f'       precise_float={precise_float}, \n'
    con__uee += f'       lines={lines}, \n'
    con__uee += '       dtype={{{}}},\n'.format(nxi__suh)
    con__uee += '       )\n'
    con__uee += (
        '    bodo.ir.connector.cast_float_to_nullable(df, df_typeref_2)\n')
    for gabre__emygp, ycmww__nok in zip(hsrar__akkzf, col_names):
        con__uee += '    if len(df) > 0:\n'
        con__uee += "        {} = df['{}'].values\n".format(gabre__emygp,
            ycmww__nok)
        con__uee += '    else:\n'
        con__uee += '        {} = np.array([])\n'.format(gabre__emygp)
    con__uee += '  return ({},)\n'.format(', '.join(lbuuo__agncs for
        lbuuo__agncs in hsrar__akkzf))
    kkvx__snou = globals()
    kkvx__snou.update({'bodo': bodo, 'pd': pd, 'np': np, 'objmode': objmode,
        'check_java_installation': check_java_installation, 'df_typeref':
        bodo.DataFrameType(tuple(col_typs), bodo.RangeIndexType(None),
        tuple(col_names)), 'get_storage_options_pyobject':
        get_storage_options_pyobject})
    nicwo__mkce = {}
    exec(con__uee, kkvx__snou, nicwo__mkce)
    xnjs__uzpu = nicwo__mkce['json_reader_py']
    kwuxq__akyg = numba.njit(xnjs__uzpu)
    compiled_funcs.append(kwuxq__akyg)
    return kwuxq__akyg
