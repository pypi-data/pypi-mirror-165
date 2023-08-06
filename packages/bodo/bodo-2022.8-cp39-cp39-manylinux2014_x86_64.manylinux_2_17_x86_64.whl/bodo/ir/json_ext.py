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
        xcmm__hxavr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        dho__yonn = cgutils.get_or_insert_function(builder.module,
            xcmm__hxavr, name='json_file_chunk_reader')
        rgzze__yevmt = builder.call(dho__yonn, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        nhrk__krgr = cgutils.create_struct_proxy(types.stream_reader_type)(
            context, builder)
        oad__anik = context.get_python_api(builder)
        nhrk__krgr.meminfo = oad__anik.nrt_meminfo_new_from_pyobject(context
            .get_constant_null(types.voidptr), rgzze__yevmt)
        nhrk__krgr.pyobj = rgzze__yevmt
        oad__anik.decref(rgzze__yevmt)
        return nhrk__krgr._getvalue()
    return types.stream_reader_type(types.voidptr, types.bool_, types.bool_,
        types.int64, types.voidptr, types.voidptr, storage_options_dict_type
        ), codegen


def remove_dead_json(json_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    qbox__ylu = []
    vwnf__qezq = []
    gzti__akf = []
    for zvc__wmptf, aiv__buwuw in enumerate(json_node.out_vars):
        if aiv__buwuw.name in lives:
            qbox__ylu.append(json_node.df_colnames[zvc__wmptf])
            vwnf__qezq.append(json_node.out_vars[zvc__wmptf])
            gzti__akf.append(json_node.out_types[zvc__wmptf])
    json_node.df_colnames = qbox__ylu
    json_node.out_vars = vwnf__qezq
    json_node.out_types = gzti__akf
    if len(json_node.out_vars) == 0:
        return None
    return json_node


def json_distributed_run(json_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        isru__aaaul = (
            'Finish column pruning on read_json node:\n%s\nColumns loaded %s\n'
            )
        dhls__nmv = json_node.loc.strformat()
        yfr__atzr = json_node.df_colnames
        bodo.user_logging.log_message('Column Pruning', isru__aaaul,
            dhls__nmv, yfr__atzr)
        zupmd__ayj = [efby__gyi for zvc__wmptf, efby__gyi in enumerate(
            json_node.df_colnames) if isinstance(json_node.out_types[
            zvc__wmptf], bodo.libs.dict_arr_ext.DictionaryArrayType)]
        if zupmd__ayj:
            arpjr__yyze = """Finished optimized encoding on read_json node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                arpjr__yyze, dhls__nmv, zupmd__ayj)
    parallel = False
    if array_dists is not None:
        parallel = True
        for gjz__rpyh in json_node.out_vars:
            if array_dists[gjz__rpyh.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                gjz__rpyh.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    mua__stbam = len(json_node.out_vars)
    gsil__qog = ', '.join('arr' + str(zvc__wmptf) for zvc__wmptf in range(
        mua__stbam))
    yqxk__yieh = 'def json_impl(fname):\n'
    yqxk__yieh += '    ({},) = _json_reader_py(fname)\n'.format(gsil__qog)
    nsxzp__dpam = {}
    exec(yqxk__yieh, {}, nsxzp__dpam)
    clbey__tkv = nsxzp__dpam['json_impl']
    qnpgv__ncy = _gen_json_reader_py(json_node.df_colnames, json_node.
        out_types, typingctx, targetctx, parallel, json_node.orient,
        json_node.convert_dates, json_node.precise_float, json_node.lines,
        json_node.compression, json_node.storage_options)
    vvnq__bxf = compile_to_numba_ir(clbey__tkv, {'_json_reader_py':
        qnpgv__ncy}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type,), typemap=typemap, calltypes=calltypes).blocks.popitem()[1
        ]
    replace_arg_nodes(vvnq__bxf, [json_node.file_name])
    kcgex__suih = vvnq__bxf.body[:-3]
    for zvc__wmptf in range(len(json_node.out_vars)):
        kcgex__suih[-len(json_node.out_vars) + zvc__wmptf
            ].target = json_node.out_vars[zvc__wmptf]
    return kcgex__suih


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
    agkoy__nonba = [sanitize_varname(efby__gyi) for efby__gyi in col_names]
    bzfjs__nuq = ', '.join(str(zvc__wmptf) for zvc__wmptf, cwodf__visi in
        enumerate(col_typs) if cwodf__visi.dtype == types.NPDatetime('ns'))
    adks__iydwm = ', '.join(["{}='{}'".format(bgvst__okhq, bodo.ir.csv_ext.
        _get_dtype_str(cwodf__visi)) for bgvst__okhq, cwodf__visi in zip(
        agkoy__nonba, col_typs)])
    men__nwsp = ', '.join(["'{}':{}".format(mmzh__hjt, bodo.ir.csv_ext.
        _get_pd_dtype_str(cwodf__visi)) for mmzh__hjt, cwodf__visi in zip(
        col_names, col_typs)])
    if compression is None:
        compression = 'uncompressed'
    yqxk__yieh = 'def json_reader_py(fname):\n'
    yqxk__yieh += '  df_typeref_2 = df_typeref\n'
    yqxk__yieh += '  check_java_installation(fname)\n'
    yqxk__yieh += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    yqxk__yieh += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    yqxk__yieh += (
        '  f_reader = bodo.ir.json_ext.json_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    yqxk__yieh += (
        """    {}, {}, -1, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py )
"""
        .format(lines, parallel, compression))
    yqxk__yieh += '  if bodo.utils.utils.is_null_pointer(f_reader._pyobj):\n'
    yqxk__yieh += "      raise FileNotFoundError('File does not exist')\n"
    yqxk__yieh += f'  with objmode({adks__iydwm}):\n'
    yqxk__yieh += f"    df = pd.read_json(f_reader, orient='{orient}',\n"
    yqxk__yieh += f'       convert_dates = {convert_dates}, \n'
    yqxk__yieh += f'       precise_float={precise_float}, \n'
    yqxk__yieh += f'       lines={lines}, \n'
    yqxk__yieh += '       dtype={{{}}},\n'.format(men__nwsp)
    yqxk__yieh += '       )\n'
    yqxk__yieh += (
        '    bodo.ir.connector.cast_float_to_nullable(df, df_typeref_2)\n')
    for bgvst__okhq, mmzh__hjt in zip(agkoy__nonba, col_names):
        yqxk__yieh += '    if len(df) > 0:\n'
        yqxk__yieh += "        {} = df['{}'].values\n".format(bgvst__okhq,
            mmzh__hjt)
        yqxk__yieh += '    else:\n'
        yqxk__yieh += '        {} = np.array([])\n'.format(bgvst__okhq)
    yqxk__yieh += '  return ({},)\n'.format(', '.join(gacn__vbd for
        gacn__vbd in agkoy__nonba))
    wvs__cpuh = globals()
    wvs__cpuh.update({'bodo': bodo, 'pd': pd, 'np': np, 'objmode': objmode,
        'check_java_installation': check_java_installation, 'df_typeref':
        bodo.DataFrameType(tuple(col_typs), bodo.RangeIndexType(None),
        tuple(col_names)), 'get_storage_options_pyobject':
        get_storage_options_pyobject})
    nsxzp__dpam = {}
    exec(yqxk__yieh, wvs__cpuh, nsxzp__dpam)
    qnpgv__ncy = nsxzp__dpam['json_reader_py']
    zjwqg__hmrwg = numba.njit(qnpgv__ncy)
    compiled_funcs.append(zjwqg__hmrwg)
    return zjwqg__hmrwg
