from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from mpi4py import MPI
from numba.core import cgutils, ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes
from numba.extending import intrinsic
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.table import Table, TableType
from bodo.io.fs_io import get_storage_options_pyobject, storage_options_dict_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, string_array_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.table_column_del_pass import ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import BodoError
from bodo.utils.utils import check_java_installation
from bodo.utils.utils import check_and_propagate_cpp_exception, sanitize_varname


class CsvReader(ir.Stmt):

    def __init__(self, file_name, df_out, sep, df_colnames, out_vars,
        out_types, usecols, loc, header, compression, nrows, skiprows,
        chunksize, is_skiprows_list, low_memory, escapechar,
        storage_options=None, index_column_index=None, index_column_typ=
        types.none):
        self.connector_typ = 'csv'
        self.file_name = file_name
        self.df_out = df_out
        self.sep = sep
        self.df_colnames = df_colnames
        self.out_vars = out_vars
        self.out_types = out_types
        self.usecols = usecols
        self.loc = loc
        self.skiprows = skiprows
        self.nrows = nrows
        self.header = header
        self.compression = compression
        self.chunksize = chunksize
        self.is_skiprows_list = is_skiprows_list
        self.pd_low_memory = low_memory
        self.escapechar = escapechar
        self.storage_options = storage_options
        self.index_column_index = index_column_index
        self.index_column_typ = index_column_typ
        self.out_used_cols = list(range(len(usecols)))

    def __repr__(self):
        return (
            '{} = ReadCsv(file={}, col_names={}, types={}, vars={}, nrows={}, skiprows={}, chunksize={}, is_skiprows_list={}, pd_low_memory={}, escapechar={}, storage_options={}, index_column_index={}, index_colum_typ = {}, out_used_colss={})'
            .format(self.df_out, self.file_name, self.df_colnames, self.
            out_types, self.out_vars, self.nrows, self.skiprows, self.
            chunksize, self.is_skiprows_list, self.pd_low_memory, self.
            escapechar, self.storage_options, self.index_column_index, self
            .index_column_typ, self.out_used_cols))


def check_node_typing(node, typemap):
    rkq__gkknn = typemap[node.file_name.name]
    if types.unliteral(rkq__gkknn) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {rkq__gkknn}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        wgjcg__ily = typemap[node.skiprows.name]
        if isinstance(wgjcg__ily, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(wgjcg__ily, types.Integer) and not (isinstance(
            wgjcg__ily, (types.List, types.Tuple)) and isinstance(
            wgjcg__ily.dtype, types.Integer)) and not isinstance(wgjcg__ily,
            (types.LiteralList, bodo.utils.typing.ListLiteral)):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer or list of integers. Found type {wgjcg__ily}."
                , loc=node.skiprows.loc)
        elif isinstance(wgjcg__ily, (types.List, types.Tuple)):
            node.is_skiprows_list = True
    if not isinstance(node.nrows, ir.Const):
        lqhdk__zrbvz = typemap[node.nrows.name]
        if not isinstance(lqhdk__zrbvz, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {lqhdk__zrbvz}."
                , loc=node.nrows.loc)


import llvmlite.binding as ll
from bodo.io import csv_cpp
ll.add_symbol('csv_file_chunk_reader', csv_cpp.csv_file_chunk_reader)


@intrinsic
def csv_file_chunk_reader(typingctx, fname_t, is_parallel_t, skiprows_t,
    nrows_t, header_t, compression_t, bucket_region_t, storage_options_t,
    chunksize_t, is_skiprows_list_t, skiprows_list_len_t, pd_low_memory_t):
    assert storage_options_t == storage_options_dict_type, "Storage options don't match expected type"

    def codegen(context, builder, sig, args):
        smr__kmyf = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(1), lir.IntType(64),
            lir.IntType(1)])
        cuwhv__cqhp = cgutils.get_or_insert_function(builder.module,
            smr__kmyf, name='csv_file_chunk_reader')
        uksb__rmo = builder.call(cuwhv__cqhp, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        gtep__buyi = cgutils.create_struct_proxy(types.stream_reader_type)(
            context, builder)
        sfxg__pna = context.get_python_api(builder)
        gtep__buyi.meminfo = sfxg__pna.nrt_meminfo_new_from_pyobject(context
            .get_constant_null(types.voidptr), uksb__rmo)
        gtep__buyi.pyobj = uksb__rmo
        sfxg__pna.decref(uksb__rmo)
        return gtep__buyi._getvalue()
    return types.stream_reader_type(types.voidptr, types.bool_, types.
        voidptr, types.int64, types.bool_, types.voidptr, types.voidptr,
        storage_options_dict_type, types.int64, types.bool_, types.int64,
        types.bool_), codegen


def remove_dead_csv(csv_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if csv_node.chunksize is not None:
        rpusv__vca = csv_node.out_vars[0]
        if rpusv__vca.name not in lives:
            return None
    else:
        puh__nkco = csv_node.out_vars[0]
        vxikn__jnh = csv_node.out_vars[1]
        if puh__nkco.name not in lives and vxikn__jnh.name not in lives:
            return None
        elif vxikn__jnh.name not in lives:
            csv_node.index_column_index = None
            csv_node.index_column_typ = types.none
        elif puh__nkco.name not in lives:
            csv_node.usecols = []
            csv_node.out_types = []
            csv_node.out_used_cols = []
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    wgjcg__ily = types.int64 if isinstance(csv_node.skiprows, ir.Const
        ) else types.unliteral(typemap[csv_node.skiprows.name])
    if csv_node.chunksize is not None:
        parallel = False
        if bodo.user_logging.get_verbose_level() >= 1:
            olw__pkd = (
                'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n'
                )
            lzed__eafq = csv_node.loc.strformat()
            wkg__vtoje = csv_node.df_colnames
            bodo.user_logging.log_message('Column Pruning', olw__pkd,
                lzed__eafq, wkg__vtoje)
            pdkle__yxmhm = csv_node.out_types[0].yield_type.data
            irlz__qwr = [abtmw__utdm for umhs__tshzw, abtmw__utdm in
                enumerate(csv_node.df_colnames) if isinstance(pdkle__yxmhm[
                umhs__tshzw], bodo.libs.dict_arr_ext.DictionaryArrayType)]
            if irlz__qwr:
                hqs__vcltb = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
                bodo.user_logging.log_message('Dictionary Encoding',
                    hqs__vcltb, lzed__eafq, irlz__qwr)
        if array_dists is not None:
            utzyi__iigf = csv_node.out_vars[0].name
            parallel = array_dists[utzyi__iigf] in (distributed_pass.
                Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        vlqq__yqa = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        vlqq__yqa += f'    reader = _csv_reader_init(fname, nrows, skiprows)\n'
        vlqq__yqa += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        und__juimv = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(vlqq__yqa, {}, und__juimv)
        tbc__blbue = und__juimv['csv_iterator_impl']
        iymn__qfp = 'def csv_reader_init(fname, nrows, skiprows):\n'
        iymn__qfp += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize, csv_node.
            is_skiprows_list, csv_node.pd_low_memory, csv_node.storage_options)
        iymn__qfp += '  return f_reader\n'
        exec(iymn__qfp, globals(), und__juimv)
        rfdx__yar = und__juimv['csv_reader_init']
        voras__nlx = numba.njit(rfdx__yar)
        compiled_funcs.append(voras__nlx)
        tdsz__nzesq = compile_to_numba_ir(tbc__blbue, {'_csv_reader_init':
            voras__nlx, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, wgjcg__ily), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(tdsz__nzesq, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        daqf__amlkz = tdsz__nzesq.body[:-3]
        daqf__amlkz[-1].target = csv_node.out_vars[0]
        return daqf__amlkz
    parallel = bodo.ir.connector.is_connector_table_parallel(csv_node,
        array_dists, typemap, 'CSVReader')
    vlqq__yqa = 'def csv_impl(fname, nrows, skiprows):\n'
    vlqq__yqa += (
        f'    (table_val, idx_col) = _csv_reader_py(fname, nrows, skiprows)\n')
    und__juimv = {}
    exec(vlqq__yqa, {}, und__juimv)
    dsn__dirbz = und__juimv['csv_impl']
    rqvvu__cof = csv_node.usecols
    if rqvvu__cof:
        rqvvu__cof = [csv_node.usecols[umhs__tshzw] for umhs__tshzw in
            csv_node.out_used_cols]
    if bodo.user_logging.get_verbose_level() >= 1:
        olw__pkd = (
            'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n')
        lzed__eafq = csv_node.loc.strformat()
        wkg__vtoje = []
        irlz__qwr = []
        if rqvvu__cof:
            for umhs__tshzw in csv_node.out_used_cols:
                kfo__ylq = csv_node.df_colnames[umhs__tshzw]
                wkg__vtoje.append(kfo__ylq)
                if isinstance(csv_node.out_types[umhs__tshzw], bodo.libs.
                    dict_arr_ext.DictionaryArrayType):
                    irlz__qwr.append(kfo__ylq)
        bodo.user_logging.log_message('Column Pruning', olw__pkd,
            lzed__eafq, wkg__vtoje)
        if irlz__qwr:
            hqs__vcltb = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', hqs__vcltb,
                lzed__eafq, irlz__qwr)
    pdpct__sirw = _gen_csv_reader_py(csv_node.df_colnames, csv_node.
        out_types, rqvvu__cof, csv_node.out_used_cols, csv_node.sep,
        parallel, csv_node.header, csv_node.compression, csv_node.
        is_skiprows_list, csv_node.pd_low_memory, csv_node.escapechar,
        csv_node.storage_options, idx_col_index=csv_node.index_column_index,
        idx_col_typ=csv_node.index_column_typ)
    tdsz__nzesq = compile_to_numba_ir(dsn__dirbz, {'_csv_reader_py':
        pdpct__sirw}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type, types.int64, wgjcg__ily), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(tdsz__nzesq, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows, csv_node.is_skiprows_list])
    daqf__amlkz = tdsz__nzesq.body[:-3]
    daqf__amlkz[-1].target = csv_node.out_vars[1]
    daqf__amlkz[-2].target = csv_node.out_vars[0]
    assert not (csv_node.index_column_index is None and not rqvvu__cof
        ), 'At most one of table and index should be dead if the CSV IR node is live'
    if csv_node.index_column_index is None:
        daqf__amlkz.pop(-1)
    elif not rqvvu__cof:
        daqf__amlkz.pop(-2)
    return daqf__amlkz


def csv_remove_dead_column(csv_node, column_live_map, equiv_vars, typemap):
    if csv_node.chunksize is not None:
        return False
    return bodo.ir.connector.base_connector_remove_dead_columns(csv_node,
        column_live_map, equiv_vars, typemap, 'CSVReader', csv_node.usecols)


numba.parfors.array_analysis.array_analysis_extensions[CsvReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[CsvReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[CsvReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[CsvReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[CsvReader] = remove_dead_csv
numba.core.analysis.ir_extension_usedefs[CsvReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[CsvReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[CsvReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[CsvReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[CsvReader] = csv_distributed_run
remove_dead_column_extensions[CsvReader] = csv_remove_dead_column
ir_extension_table_column_use[CsvReader
    ] = bodo.ir.connector.connector_table_column_use


def _get_dtype_str(t):
    vozju__ikukh = t.dtype
    if isinstance(vozju__ikukh, PDCategoricalDtype):
        evsrp__mdwg = CategoricalArrayType(vozju__ikukh)
        xyuvq__ojr = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, xyuvq__ojr, evsrp__mdwg)
        return xyuvq__ojr
    if vozju__ikukh == types.NPDatetime('ns'):
        vozju__ikukh = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        acxv__cqqmc = 'int_arr_{}'.format(vozju__ikukh)
        setattr(types, acxv__cqqmc, t)
        return acxv__cqqmc
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if vozju__ikukh == types.bool_:
        vozju__ikukh = 'bool_'
    if vozju__ikukh == datetime_date_type:
        return 'datetime_date_array_type'
    if isinstance(t, ArrayItemArrayType) and isinstance(vozju__ikukh, (
        StringArrayType, ArrayItemArrayType)):
        ksw__lby = f'ArrayItemArrayType{str(ir_utils.next_label())}'
        setattr(types, ksw__lby, t)
        return ksw__lby
    return '{}[::1]'.format(vozju__ikukh)


def _get_pd_dtype_str(t):
    vozju__ikukh = t.dtype
    if isinstance(vozju__ikukh, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(vozju__ikukh.categories)
    if vozju__ikukh == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if vozju__ikukh.signed else 'U',
            vozju__ikukh.bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    if isinstance(t, ArrayItemArrayType) and isinstance(vozju__ikukh, (
        StringArrayType, ArrayItemArrayType)):
        return 'object'
    return 'np.{}'.format(vozju__ikukh)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows[0] < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    ylwud__dsy = ''
    from collections import defaultdict
    zam__qhlj = defaultdict(list)
    for crcgk__sxhbl, qrvmu__kiipg in typemap.items():
        zam__qhlj[qrvmu__kiipg].append(crcgk__sxhbl)
    ibp__eebd = df.columns.to_list()
    qjn__zkvwq = []
    for qrvmu__kiipg, yak__uninq in zam__qhlj.items():
        try:
            qjn__zkvwq.append(df.loc[:, yak__uninq].astype(qrvmu__kiipg,
                copy=False))
            df = df.drop(yak__uninq, axis=1)
        except (ValueError, TypeError) as xyue__mwui:
            ylwud__dsy = (
                f"Caught the runtime error '{xyue__mwui}' on columns {yak__uninq}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    hqism__gkh = bool(ylwud__dsy)
    if parallel:
        kna__gkfaj = MPI.COMM_WORLD
        hqism__gkh = kna__gkfaj.allreduce(hqism__gkh, op=MPI.LOR)
    if hqism__gkh:
        bqfj__dvhzl = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if ylwud__dsy:
            raise TypeError(f'{bqfj__dvhzl}\n{ylwud__dsy}')
        else:
            raise TypeError(
                f'{bqfj__dvhzl}\nPlease refer to errors on other ranks.')
    df = pd.concat(qjn__zkvwq + [df], axis=1)
    tsmll__vzvo = df.loc[:, ibp__eebd]
    return tsmll__vzvo


def _gen_csv_file_reader_init(parallel, header, compression, chunksize,
    is_skiprows_list, pd_low_memory, storage_options):
    cddvr__izltc = header == 0
    if compression is None:
        compression = 'uncompressed'
    if is_skiprows_list:
        vlqq__yqa = '  skiprows = sorted(set(skiprows))\n'
    else:
        vlqq__yqa = '  skiprows = [skiprows]\n'
    vlqq__yqa += '  skiprows_list_len = len(skiprows)\n'
    vlqq__yqa += '  check_nrows_skiprows_value(nrows, skiprows)\n'
    vlqq__yqa += '  check_java_installation(fname)\n'
    vlqq__yqa += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    vlqq__yqa += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    vlqq__yqa += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    vlqq__yqa += (
        """    {}, bodo.utils.conversion.coerce_to_ndarray(skiprows, scalar_to_arr_len=1).ctypes, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py, {}, {}, skiprows_list_len, {})
"""
        .format(parallel, cddvr__izltc, compression, chunksize,
        is_skiprows_list, pd_low_memory))
    vlqq__yqa += '  if bodo.utils.utils.is_null_pointer(f_reader._pyobj):\n'
    vlqq__yqa += "      raise FileNotFoundError('File does not exist')\n"
    return vlqq__yqa


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    out_used_cols, sep, escapechar, storage_options, call_id, glbs,
    parallel, check_parallel_runtime, idx_col_index, idx_col_typ):
    rtazf__dphid = [str(umhs__tshzw) for umhs__tshzw, vdpm__xnlfu in
        enumerate(usecols) if col_typs[out_used_cols[umhs__tshzw]].dtype ==
        types.NPDatetime('ns')]
    if idx_col_typ == types.NPDatetime('ns'):
        assert not idx_col_index is None
        rtazf__dphid.append(str(idx_col_index))
    hiy__cbgd = ', '.join(rtazf__dphid)
    jfwcl__uinkt = _gen_parallel_flag_name(sanitized_cnames)
    lczlw__osxnn = f"{jfwcl__uinkt}='bool_'" if check_parallel_runtime else ''
    cdw__aglm = [_get_pd_dtype_str(col_typs[out_used_cols[umhs__tshzw]]) for
        umhs__tshzw in range(len(usecols))]
    qgz__hgim = None if idx_col_index is None else _get_pd_dtype_str(
        idx_col_typ)
    lzglm__poxr = [vdpm__xnlfu for umhs__tshzw, vdpm__xnlfu in enumerate(
        usecols) if cdw__aglm[umhs__tshzw] == 'str']
    if idx_col_index is not None and qgz__hgim == 'str':
        lzglm__poxr.append(idx_col_index)
    uqw__czi = np.array(lzglm__poxr, dtype=np.int64)
    glbs[f'str_col_nums_{call_id}'] = uqw__czi
    vlqq__yqa = f'  str_col_nums_{call_id}_2 = str_col_nums_{call_id}\n'
    mlvz__aqhey = np.array(usecols + ([idx_col_index] if idx_col_index is not
        None else []), dtype=np.int64)
    glbs[f'usecols_arr_{call_id}'] = mlvz__aqhey
    vlqq__yqa += f'  usecols_arr_{call_id}_2 = usecols_arr_{call_id}\n'
    ohra__fmyqb = np.array(out_used_cols, dtype=np.int64)
    if usecols:
        glbs[f'type_usecols_offsets_arr_{call_id}'] = ohra__fmyqb
        vlqq__yqa += f"""  type_usecols_offsets_arr_{call_id}_2 = type_usecols_offsets_arr_{call_id}
"""
    iyjvr__xcmw = defaultdict(list)
    for umhs__tshzw, vdpm__xnlfu in enumerate(usecols):
        if cdw__aglm[umhs__tshzw] == 'str':
            continue
        iyjvr__xcmw[cdw__aglm[umhs__tshzw]].append(vdpm__xnlfu)
    if idx_col_index is not None and qgz__hgim != 'str':
        iyjvr__xcmw[qgz__hgim].append(idx_col_index)
    for umhs__tshzw, edvh__aijd in enumerate(iyjvr__xcmw.values()):
        glbs[f't_arr_{umhs__tshzw}_{call_id}'] = np.asarray(edvh__aijd)
        vlqq__yqa += (
            f'  t_arr_{umhs__tshzw}_{call_id}_2 = t_arr_{umhs__tshzw}_{call_id}\n'
            )
    if idx_col_index != None:
        vlqq__yqa += f"""  with objmode(T=table_type_{call_id}, idx_arr=idx_array_typ, {lczlw__osxnn}):
"""
    else:
        vlqq__yqa += (
            f'  with objmode(T=table_type_{call_id}, {lczlw__osxnn}):\n')
    vlqq__yqa += f'    typemap = {{}}\n'
    for umhs__tshzw, kcf__xxpv in enumerate(iyjvr__xcmw.keys()):
        vlqq__yqa += f"""    typemap.update({{i:{kcf__xxpv} for i in t_arr_{umhs__tshzw}_{call_id}_2}})
"""
    vlqq__yqa += '    if f_reader.get_chunk_size() == 0:\n'
    vlqq__yqa += (
        f'      df = pd.DataFrame(columns=usecols_arr_{call_id}_2, dtype=str)\n'
        )
    vlqq__yqa += '    else:\n'
    vlqq__yqa += '      df = pd.read_csv(f_reader,\n'
    vlqq__yqa += '        header=None,\n'
    vlqq__yqa += '        parse_dates=[{}],\n'.format(hiy__cbgd)
    vlqq__yqa += (
        f'        dtype={{i:str for i in str_col_nums_{call_id}_2}},\n')
    vlqq__yqa += f"""        usecols=usecols_arr_{call_id}_2, sep={sep!r}, low_memory=False, escapechar={escapechar!r})
"""
    if check_parallel_runtime:
        vlqq__yqa += f'    {jfwcl__uinkt} = f_reader.is_parallel()\n'
    else:
        vlqq__yqa += f'    {jfwcl__uinkt} = {parallel}\n'
    vlqq__yqa += f'    df = astype(df, typemap, {jfwcl__uinkt})\n'
    if idx_col_index != None:
        mqdy__cbpub = sorted(mlvz__aqhey).index(idx_col_index)
        vlqq__yqa += f'    idx_arr = df.iloc[:, {mqdy__cbpub}].values\n'
        vlqq__yqa += (
            f'    df.drop(columns=df.columns[{mqdy__cbpub}], inplace=True)\n')
    if len(usecols) == 0:
        vlqq__yqa += f'    T = None\n'
    else:
        vlqq__yqa += f'    arrs = []\n'
        vlqq__yqa += f'    for i in range(df.shape[1]):\n'
        vlqq__yqa += f'      arrs.append(df.iloc[:, i].values)\n'
        vlqq__yqa += f"""    T = Table(arrs, type_usecols_offsets_arr_{call_id}_2, {len(col_names)})
"""
    return vlqq__yqa


def _gen_parallel_flag_name(sanitized_cnames):
    jfwcl__uinkt = '_parallel_value'
    while jfwcl__uinkt in sanitized_cnames:
        jfwcl__uinkt = '_' + jfwcl__uinkt
    return jfwcl__uinkt


def _gen_csv_reader_py(col_names, col_typs, usecols, out_used_cols, sep,
    parallel, header, compression, is_skiprows_list, pd_low_memory,
    escapechar, storage_options, idx_col_index=None, idx_col_typ=types.none):
    sanitized_cnames = [sanitize_varname(abtmw__utdm) for abtmw__utdm in
        col_names]
    vlqq__yqa = 'def csv_reader_py(fname, nrows, skiprows):\n'
    vlqq__yqa += _gen_csv_file_reader_init(parallel, header, compression, -
        1, is_skiprows_list, pd_low_memory, storage_options)
    call_id = ir_utils.next_label()
    olkc__yefo = globals()
    if idx_col_typ != types.none:
        olkc__yefo[f'idx_array_typ'] = idx_col_typ
    if len(usecols) == 0:
        olkc__yefo[f'table_type_{call_id}'] = types.none
    else:
        olkc__yefo[f'table_type_{call_id}'] = TableType(tuple(col_typs))
    vlqq__yqa += _gen_read_csv_objmode(col_names, sanitized_cnames,
        col_typs, usecols, out_used_cols, sep, escapechar, storage_options,
        call_id, olkc__yefo, parallel=parallel, check_parallel_runtime=
        False, idx_col_index=idx_col_index, idx_col_typ=idx_col_typ)
    if idx_col_index != None:
        vlqq__yqa += '  return (T, idx_arr)\n'
    else:
        vlqq__yqa += '  return (T, None)\n'
    und__juimv = {}
    olkc__yefo['get_storage_options_pyobject'] = get_storage_options_pyobject
    exec(vlqq__yqa, olkc__yefo, und__juimv)
    pdpct__sirw = und__juimv['csv_reader_py']
    voras__nlx = numba.njit(pdpct__sirw)
    compiled_funcs.append(voras__nlx)
    return voras__nlx
