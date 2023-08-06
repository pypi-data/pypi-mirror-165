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
    ejaje__jgmwg = typemap[node.file_name.name]
    if types.unliteral(ejaje__jgmwg) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {ejaje__jgmwg}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        vbcni__nlhu = typemap[node.skiprows.name]
        if isinstance(vbcni__nlhu, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(vbcni__nlhu, types.Integer) and not (isinstance
            (vbcni__nlhu, (types.List, types.Tuple)) and isinstance(
            vbcni__nlhu.dtype, types.Integer)) and not isinstance(vbcni__nlhu,
            (types.LiteralList, bodo.utils.typing.ListLiteral)):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer or list of integers. Found type {vbcni__nlhu}."
                , loc=node.skiprows.loc)
        elif isinstance(vbcni__nlhu, (types.List, types.Tuple)):
            node.is_skiprows_list = True
    if not isinstance(node.nrows, ir.Const):
        hjfqp__raap = typemap[node.nrows.name]
        if not isinstance(hjfqp__raap, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {hjfqp__raap}."
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
        zfegr__csx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(1), lir.IntType(64),
            lir.IntType(1)])
        hdew__ulev = cgutils.get_or_insert_function(builder.module,
            zfegr__csx, name='csv_file_chunk_reader')
        qnjrg__ztc = builder.call(hdew__ulev, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        zhrn__brbrz = cgutils.create_struct_proxy(types.stream_reader_type)(
            context, builder)
        inow__axmg = context.get_python_api(builder)
        zhrn__brbrz.meminfo = inow__axmg.nrt_meminfo_new_from_pyobject(context
            .get_constant_null(types.voidptr), qnjrg__ztc)
        zhrn__brbrz.pyobj = qnjrg__ztc
        inow__axmg.decref(qnjrg__ztc)
        return zhrn__brbrz._getvalue()
    return types.stream_reader_type(types.voidptr, types.bool_, types.
        voidptr, types.int64, types.bool_, types.voidptr, types.voidptr,
        storage_options_dict_type, types.int64, types.bool_, types.int64,
        types.bool_), codegen


def remove_dead_csv(csv_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if csv_node.chunksize is not None:
        ercu__twgy = csv_node.out_vars[0]
        if ercu__twgy.name not in lives:
            return None
    else:
        szgo__olm = csv_node.out_vars[0]
        hyff__gif = csv_node.out_vars[1]
        if szgo__olm.name not in lives and hyff__gif.name not in lives:
            return None
        elif hyff__gif.name not in lives:
            csv_node.index_column_index = None
            csv_node.index_column_typ = types.none
        elif szgo__olm.name not in lives:
            csv_node.usecols = []
            csv_node.out_types = []
            csv_node.out_used_cols = []
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    vbcni__nlhu = types.int64 if isinstance(csv_node.skiprows, ir.Const
        ) else types.unliteral(typemap[csv_node.skiprows.name])
    if csv_node.chunksize is not None:
        parallel = False
        if bodo.user_logging.get_verbose_level() >= 1:
            qzzw__gpx = (
                'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n'
                )
            vxg__xlwh = csv_node.loc.strformat()
            bjg__erc = csv_node.df_colnames
            bodo.user_logging.log_message('Column Pruning', qzzw__gpx,
                vxg__xlwh, bjg__erc)
            vddek__yfcmg = csv_node.out_types[0].yield_type.data
            dtqh__zhshu = [wxpga__qvws for yiqvc__cgr, wxpga__qvws in
                enumerate(csv_node.df_colnames) if isinstance(vddek__yfcmg[
                yiqvc__cgr], bodo.libs.dict_arr_ext.DictionaryArrayType)]
            if dtqh__zhshu:
                aamqz__qqfkz = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
                bodo.user_logging.log_message('Dictionary Encoding',
                    aamqz__qqfkz, vxg__xlwh, dtqh__zhshu)
        if array_dists is not None:
            ake__ceydj = csv_node.out_vars[0].name
            parallel = array_dists[ake__ceydj] in (distributed_pass.
                Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        rwdsa__sua = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        rwdsa__sua += (
            f'    reader = _csv_reader_init(fname, nrows, skiprows)\n')
        rwdsa__sua += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        rmel__gkfh = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(rwdsa__sua, {}, rmel__gkfh)
        zzu__hnvqg = rmel__gkfh['csv_iterator_impl']
        pzm__qwxn = 'def csv_reader_init(fname, nrows, skiprows):\n'
        pzm__qwxn += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize, csv_node.
            is_skiprows_list, csv_node.pd_low_memory, csv_node.storage_options)
        pzm__qwxn += '  return f_reader\n'
        exec(pzm__qwxn, globals(), rmel__gkfh)
        etyig__fjhz = rmel__gkfh['csv_reader_init']
        aub__khbc = numba.njit(etyig__fjhz)
        compiled_funcs.append(aub__khbc)
        hcw__lfxks = compile_to_numba_ir(zzu__hnvqg, {'_csv_reader_init':
            aub__khbc, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, vbcni__nlhu), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(hcw__lfxks, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        fpp__hxyek = hcw__lfxks.body[:-3]
        fpp__hxyek[-1].target = csv_node.out_vars[0]
        return fpp__hxyek
    parallel = bodo.ir.connector.is_connector_table_parallel(csv_node,
        array_dists, typemap, 'CSVReader')
    rwdsa__sua = 'def csv_impl(fname, nrows, skiprows):\n'
    rwdsa__sua += (
        f'    (table_val, idx_col) = _csv_reader_py(fname, nrows, skiprows)\n')
    rmel__gkfh = {}
    exec(rwdsa__sua, {}, rmel__gkfh)
    ikui__nekri = rmel__gkfh['csv_impl']
    atb__uofb = csv_node.usecols
    if atb__uofb:
        atb__uofb = [csv_node.usecols[yiqvc__cgr] for yiqvc__cgr in
            csv_node.out_used_cols]
    if bodo.user_logging.get_verbose_level() >= 1:
        qzzw__gpx = (
            'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n')
        vxg__xlwh = csv_node.loc.strformat()
        bjg__erc = []
        dtqh__zhshu = []
        if atb__uofb:
            for yiqvc__cgr in csv_node.out_used_cols:
                kzs__bax = csv_node.df_colnames[yiqvc__cgr]
                bjg__erc.append(kzs__bax)
                if isinstance(csv_node.out_types[yiqvc__cgr], bodo.libs.
                    dict_arr_ext.DictionaryArrayType):
                    dtqh__zhshu.append(kzs__bax)
        bodo.user_logging.log_message('Column Pruning', qzzw__gpx,
            vxg__xlwh, bjg__erc)
        if dtqh__zhshu:
            aamqz__qqfkz = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                aamqz__qqfkz, vxg__xlwh, dtqh__zhshu)
    kxy__ibf = _gen_csv_reader_py(csv_node.df_colnames, csv_node.out_types,
        atb__uofb, csv_node.out_used_cols, csv_node.sep, parallel, csv_node
        .header, csv_node.compression, csv_node.is_skiprows_list, csv_node.
        pd_low_memory, csv_node.escapechar, csv_node.storage_options,
        idx_col_index=csv_node.index_column_index, idx_col_typ=csv_node.
        index_column_typ)
    hcw__lfxks = compile_to_numba_ir(ikui__nekri, {'_csv_reader_py':
        kxy__ibf}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type, types.int64, vbcni__nlhu), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(hcw__lfxks, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows, csv_node.is_skiprows_list])
    fpp__hxyek = hcw__lfxks.body[:-3]
    fpp__hxyek[-1].target = csv_node.out_vars[1]
    fpp__hxyek[-2].target = csv_node.out_vars[0]
    assert not (csv_node.index_column_index is None and not atb__uofb
        ), 'At most one of table and index should be dead if the CSV IR node is live'
    if csv_node.index_column_index is None:
        fpp__hxyek.pop(-1)
    elif not atb__uofb:
        fpp__hxyek.pop(-2)
    return fpp__hxyek


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
    favgc__mrf = t.dtype
    if isinstance(favgc__mrf, PDCategoricalDtype):
        flufl__avk = CategoricalArrayType(favgc__mrf)
        mguad__lcck = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, mguad__lcck, flufl__avk)
        return mguad__lcck
    if favgc__mrf == types.NPDatetime('ns'):
        favgc__mrf = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        bdzjd__hysgv = 'int_arr_{}'.format(favgc__mrf)
        setattr(types, bdzjd__hysgv, t)
        return bdzjd__hysgv
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if favgc__mrf == types.bool_:
        favgc__mrf = 'bool_'
    if favgc__mrf == datetime_date_type:
        return 'datetime_date_array_type'
    if isinstance(t, ArrayItemArrayType) and isinstance(favgc__mrf, (
        StringArrayType, ArrayItemArrayType)):
        cnx__wvz = f'ArrayItemArrayType{str(ir_utils.next_label())}'
        setattr(types, cnx__wvz, t)
        return cnx__wvz
    return '{}[::1]'.format(favgc__mrf)


def _get_pd_dtype_str(t):
    favgc__mrf = t.dtype
    if isinstance(favgc__mrf, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(favgc__mrf.categories)
    if favgc__mrf == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if favgc__mrf.signed else 'U',
            favgc__mrf.bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    if isinstance(t, ArrayItemArrayType) and isinstance(favgc__mrf, (
        StringArrayType, ArrayItemArrayType)):
        return 'object'
    return 'np.{}'.format(favgc__mrf)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows[0] < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    epho__sjuw = ''
    from collections import defaultdict
    ihmr__zuotf = defaultdict(list)
    for cuklz__hfp, ivfkc__gyznt in typemap.items():
        ihmr__zuotf[ivfkc__gyznt].append(cuklz__hfp)
    aqqgd__ylzu = df.columns.to_list()
    qzzqk__qzna = []
    for ivfkc__gyznt, zqd__wfch in ihmr__zuotf.items():
        try:
            qzzqk__qzna.append(df.loc[:, zqd__wfch].astype(ivfkc__gyznt,
                copy=False))
            df = df.drop(zqd__wfch, axis=1)
        except (ValueError, TypeError) as luw__ilqyk:
            epho__sjuw = (
                f"Caught the runtime error '{luw__ilqyk}' on columns {zqd__wfch}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    dnorz__ushxs = bool(epho__sjuw)
    if parallel:
        nil__jjqus = MPI.COMM_WORLD
        dnorz__ushxs = nil__jjqus.allreduce(dnorz__ushxs, op=MPI.LOR)
    if dnorz__ushxs:
        bep__wdm = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if epho__sjuw:
            raise TypeError(f'{bep__wdm}\n{epho__sjuw}')
        else:
            raise TypeError(
                f'{bep__wdm}\nPlease refer to errors on other ranks.')
    df = pd.concat(qzzqk__qzna + [df], axis=1)
    ybw__mmbr = df.loc[:, aqqgd__ylzu]
    return ybw__mmbr


def _gen_csv_file_reader_init(parallel, header, compression, chunksize,
    is_skiprows_list, pd_low_memory, storage_options):
    akkx__pfd = header == 0
    if compression is None:
        compression = 'uncompressed'
    if is_skiprows_list:
        rwdsa__sua = '  skiprows = sorted(set(skiprows))\n'
    else:
        rwdsa__sua = '  skiprows = [skiprows]\n'
    rwdsa__sua += '  skiprows_list_len = len(skiprows)\n'
    rwdsa__sua += '  check_nrows_skiprows_value(nrows, skiprows)\n'
    rwdsa__sua += '  check_java_installation(fname)\n'
    rwdsa__sua += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    rwdsa__sua += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    rwdsa__sua += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    rwdsa__sua += (
        """    {}, bodo.utils.conversion.coerce_to_ndarray(skiprows, scalar_to_arr_len=1).ctypes, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py, {}, {}, skiprows_list_len, {})
"""
        .format(parallel, akkx__pfd, compression, chunksize,
        is_skiprows_list, pd_low_memory))
    rwdsa__sua += '  if bodo.utils.utils.is_null_pointer(f_reader._pyobj):\n'
    rwdsa__sua += "      raise FileNotFoundError('File does not exist')\n"
    return rwdsa__sua


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    out_used_cols, sep, escapechar, storage_options, call_id, glbs,
    parallel, check_parallel_runtime, idx_col_index, idx_col_typ):
    dujys__quom = [str(yiqvc__cgr) for yiqvc__cgr, gusgb__emt in enumerate(
        usecols) if col_typs[out_used_cols[yiqvc__cgr]].dtype == types.
        NPDatetime('ns')]
    if idx_col_typ == types.NPDatetime('ns'):
        assert not idx_col_index is None
        dujys__quom.append(str(idx_col_index))
    shwse__oocc = ', '.join(dujys__quom)
    ouafz__pvqnd = _gen_parallel_flag_name(sanitized_cnames)
    oupxm__fsac = f"{ouafz__pvqnd}='bool_'" if check_parallel_runtime else ''
    xxae__goxj = [_get_pd_dtype_str(col_typs[out_used_cols[yiqvc__cgr]]) for
        yiqvc__cgr in range(len(usecols))]
    mef__ldz = None if idx_col_index is None else _get_pd_dtype_str(idx_col_typ
        )
    ckmmi__afc = [gusgb__emt for yiqvc__cgr, gusgb__emt in enumerate(
        usecols) if xxae__goxj[yiqvc__cgr] == 'str']
    if idx_col_index is not None and mef__ldz == 'str':
        ckmmi__afc.append(idx_col_index)
    kbo__gmtu = np.array(ckmmi__afc, dtype=np.int64)
    glbs[f'str_col_nums_{call_id}'] = kbo__gmtu
    rwdsa__sua = f'  str_col_nums_{call_id}_2 = str_col_nums_{call_id}\n'
    dxovg__fbtb = np.array(usecols + ([idx_col_index] if idx_col_index is not
        None else []), dtype=np.int64)
    glbs[f'usecols_arr_{call_id}'] = dxovg__fbtb
    rwdsa__sua += f'  usecols_arr_{call_id}_2 = usecols_arr_{call_id}\n'
    zccq__gmq = np.array(out_used_cols, dtype=np.int64)
    if usecols:
        glbs[f'type_usecols_offsets_arr_{call_id}'] = zccq__gmq
        rwdsa__sua += f"""  type_usecols_offsets_arr_{call_id}_2 = type_usecols_offsets_arr_{call_id}
"""
    lkrsy__lztf = defaultdict(list)
    for yiqvc__cgr, gusgb__emt in enumerate(usecols):
        if xxae__goxj[yiqvc__cgr] == 'str':
            continue
        lkrsy__lztf[xxae__goxj[yiqvc__cgr]].append(gusgb__emt)
    if idx_col_index is not None and mef__ldz != 'str':
        lkrsy__lztf[mef__ldz].append(idx_col_index)
    for yiqvc__cgr, jrqw__vofri in enumerate(lkrsy__lztf.values()):
        glbs[f't_arr_{yiqvc__cgr}_{call_id}'] = np.asarray(jrqw__vofri)
        rwdsa__sua += (
            f'  t_arr_{yiqvc__cgr}_{call_id}_2 = t_arr_{yiqvc__cgr}_{call_id}\n'
            )
    if idx_col_index != None:
        rwdsa__sua += f"""  with objmode(T=table_type_{call_id}, idx_arr=idx_array_typ, {oupxm__fsac}):
"""
    else:
        rwdsa__sua += (
            f'  with objmode(T=table_type_{call_id}, {oupxm__fsac}):\n')
    rwdsa__sua += f'    typemap = {{}}\n'
    for yiqvc__cgr, rgxc__feqyf in enumerate(lkrsy__lztf.keys()):
        rwdsa__sua += f"""    typemap.update({{i:{rgxc__feqyf} for i in t_arr_{yiqvc__cgr}_{call_id}_2}})
"""
    rwdsa__sua += '    if f_reader.get_chunk_size() == 0:\n'
    rwdsa__sua += (
        f'      df = pd.DataFrame(columns=usecols_arr_{call_id}_2, dtype=str)\n'
        )
    rwdsa__sua += '    else:\n'
    rwdsa__sua += '      df = pd.read_csv(f_reader,\n'
    rwdsa__sua += '        header=None,\n'
    rwdsa__sua += '        parse_dates=[{}],\n'.format(shwse__oocc)
    rwdsa__sua += (
        f'        dtype={{i:str for i in str_col_nums_{call_id}_2}},\n')
    rwdsa__sua += f"""        usecols=usecols_arr_{call_id}_2, sep={sep!r}, low_memory=False, escapechar={escapechar!r})
"""
    if check_parallel_runtime:
        rwdsa__sua += f'    {ouafz__pvqnd} = f_reader.is_parallel()\n'
    else:
        rwdsa__sua += f'    {ouafz__pvqnd} = {parallel}\n'
    rwdsa__sua += f'    df = astype(df, typemap, {ouafz__pvqnd})\n'
    if idx_col_index != None:
        kms__cgi = sorted(dxovg__fbtb).index(idx_col_index)
        rwdsa__sua += f'    idx_arr = df.iloc[:, {kms__cgi}].values\n'
        rwdsa__sua += (
            f'    df.drop(columns=df.columns[{kms__cgi}], inplace=True)\n')
    if len(usecols) == 0:
        rwdsa__sua += f'    T = None\n'
    else:
        rwdsa__sua += f'    arrs = []\n'
        rwdsa__sua += f'    for i in range(df.shape[1]):\n'
        rwdsa__sua += f'      arrs.append(df.iloc[:, i].values)\n'
        rwdsa__sua += f"""    T = Table(arrs, type_usecols_offsets_arr_{call_id}_2, {len(col_names)})
"""
    return rwdsa__sua


def _gen_parallel_flag_name(sanitized_cnames):
    ouafz__pvqnd = '_parallel_value'
    while ouafz__pvqnd in sanitized_cnames:
        ouafz__pvqnd = '_' + ouafz__pvqnd
    return ouafz__pvqnd


def _gen_csv_reader_py(col_names, col_typs, usecols, out_used_cols, sep,
    parallel, header, compression, is_skiprows_list, pd_low_memory,
    escapechar, storage_options, idx_col_index=None, idx_col_typ=types.none):
    sanitized_cnames = [sanitize_varname(wxpga__qvws) for wxpga__qvws in
        col_names]
    rwdsa__sua = 'def csv_reader_py(fname, nrows, skiprows):\n'
    rwdsa__sua += _gen_csv_file_reader_init(parallel, header, compression, 
        -1, is_skiprows_list, pd_low_memory, storage_options)
    call_id = ir_utils.next_label()
    aln__dcdla = globals()
    if idx_col_typ != types.none:
        aln__dcdla[f'idx_array_typ'] = idx_col_typ
    if len(usecols) == 0:
        aln__dcdla[f'table_type_{call_id}'] = types.none
    else:
        aln__dcdla[f'table_type_{call_id}'] = TableType(tuple(col_typs))
    rwdsa__sua += _gen_read_csv_objmode(col_names, sanitized_cnames,
        col_typs, usecols, out_used_cols, sep, escapechar, storage_options,
        call_id, aln__dcdla, parallel=parallel, check_parallel_runtime=
        False, idx_col_index=idx_col_index, idx_col_typ=idx_col_typ)
    if idx_col_index != None:
        rwdsa__sua += '  return (T, idx_arr)\n'
    else:
        rwdsa__sua += '  return (T, None)\n'
    rmel__gkfh = {}
    aln__dcdla['get_storage_options_pyobject'] = get_storage_options_pyobject
    exec(rwdsa__sua, aln__dcdla, rmel__gkfh)
    kxy__ibf = rmel__gkfh['csv_reader_py']
    aub__khbc = numba.njit(kxy__ibf)
    compiled_funcs.append(aub__khbc)
    return aub__khbc
