import os
import warnings
from collections import defaultdict
from glob import has_magic
from urllib.parse import urlparse
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow
import pyarrow as pa
import pyarrow.dataset as ds
from numba.core import ir, types
from numba.core.ir_utils import compile_to_numba_ir, get_definition, guard, mk_unique_var, next_label, replace_arg_nodes
from numba.extending import NativeValue, box, intrinsic, models, overload, register_model, unbox
from pyarrow._fs import PyFileSystem
from pyarrow.fs import FSSpecHandler
import bodo
import bodo.ir.parquet_ext
import bodo.utils.tracing as tracing
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.table import TableType
from bodo.io.fs_io import get_hdfs_fs, get_s3_fs_from_path, get_storage_options_pyobject, storage_options_dict_type
from bodo.io.helpers import _get_numba_typ_from_pa_typ, is_nullable
from bodo.libs.array import cpp_table_to_py_table, delete_table, info_from_table, info_to_array, table_type
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.distributed_api import get_end, get_start
from bodo.libs.str_ext import unicode_to_utf8
from bodo.transforms import distributed_pass
from bodo.utils.transform import get_const_value
from bodo.utils.typing import BodoError, BodoWarning, FileInfo, get_overload_const_str
from bodo.utils.utils import check_and_propagate_cpp_exception, numba_to_c_type, sanitize_varname
REMOTE_FILESYSTEMS = {'s3', 'gcs', 'gs', 'http', 'hdfs', 'abfs', 'abfss'}
READ_STR_AS_DICT_THRESHOLD = 1.0
list_of_files_error_msg = (
    '. Make sure the list/glob passed to read_parquet() only contains paths to files (no directories)'
    )


class ParquetPredicateType(types.Type):

    def __init__(self):
        super(ParquetPredicateType, self).__init__(name=
            'ParquetPredicateType()')


parquet_predicate_type = ParquetPredicateType()
types.parquet_predicate_type = parquet_predicate_type
register_model(ParquetPredicateType)(models.OpaqueModel)


@unbox(ParquetPredicateType)
def unbox_parquet_predicate_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


@box(ParquetPredicateType)
def box_parquet_predicate_type(typ, val, c):
    c.pyapi.incref(val)
    return val


class ReadParquetFilepathType(types.Opaque):

    def __init__(self):
        super(ReadParquetFilepathType, self).__init__(name=
            'ReadParquetFilepathType')


read_parquet_fpath_type = ReadParquetFilepathType()
types.read_parquet_fpath_type = read_parquet_fpath_type
register_model(ReadParquetFilepathType)(models.OpaqueModel)


@unbox(ReadParquetFilepathType)
def unbox_read_parquet_fpath_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


class ParquetFileInfo(FileInfo):

    def __init__(self, columns, storage_options=None, input_file_name_col=
        None, read_as_dict_cols=None):
        self.columns = columns
        self.storage_options = storage_options
        self.input_file_name_col = input_file_name_col
        self.read_as_dict_cols = read_as_dict_cols
        super().__init__()

    def _get_schema(self, fname):
        try:
            return parquet_file_schema(fname, selected_columns=self.columns,
                storage_options=self.storage_options, input_file_name_col=
                self.input_file_name_col, read_as_dict_cols=self.
                read_as_dict_cols)
        except OSError as hzox__akr:
            if 'non-file path' in str(hzox__akr):
                raise FileNotFoundError(str(hzox__akr))
            raise


class ParquetHandler:

    def __init__(self, func_ir, typingctx, args, _locals):
        self.func_ir = func_ir
        self.typingctx = typingctx
        self.args = args
        self.locals = _locals

    def gen_parquet_read(self, file_name, lhs, columns, storage_options=
        None, input_file_name_col=None, read_as_dict_cols=None):
        zsr__pyq = lhs.scope
        uxl__ubw = lhs.loc
        lwh__ukci = None
        if lhs.name in self.locals:
            lwh__ukci = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        senn__lqc = {}
        if lhs.name + ':convert' in self.locals:
            senn__lqc = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if lwh__ukci is None:
            huar__upj = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/file_io/#parquet-section.'
                )
            quu__ipvk = get_const_value(file_name, self.func_ir, huar__upj,
                arg_types=self.args, file_info=ParquetFileInfo(columns,
                storage_options=storage_options, input_file_name_col=
                input_file_name_col, read_as_dict_cols=read_as_dict_cols))
            ztl__jea = False
            gkc__gjlge = guard(get_definition, self.func_ir, file_name)
            if isinstance(gkc__gjlge, ir.Arg):
                typ = self.args[gkc__gjlge.index]
                if isinstance(typ, types.FilenameType):
                    (col_names, fph__xsh, esta__yjw, col_indices,
                        partition_names, ycxyc__wxn, ojhj__kfudx) = typ.schema
                    ztl__jea = True
            if not ztl__jea:
                (col_names, fph__xsh, esta__yjw, col_indices,
                    partition_names, ycxyc__wxn, ojhj__kfudx) = (
                    parquet_file_schema(quu__ipvk, columns, storage_options
                    =storage_options, input_file_name_col=
                    input_file_name_col, read_as_dict_cols=read_as_dict_cols))
        else:
            zfr__edzdt = list(lwh__ukci.keys())
            jxwbs__nfvkl = {c: ibaxa__uaekj for ibaxa__uaekj, c in
                enumerate(zfr__edzdt)}
            wnmqb__pgh = [qxr__taaoh for qxr__taaoh in lwh__ukci.values()]
            esta__yjw = 'index' if 'index' in jxwbs__nfvkl else None
            if columns is None:
                selected_columns = zfr__edzdt
            else:
                selected_columns = columns
            col_indices = [jxwbs__nfvkl[c] for c in selected_columns]
            fph__xsh = [wnmqb__pgh[jxwbs__nfvkl[c]] for c in selected_columns]
            col_names = selected_columns
            esta__yjw = esta__yjw if esta__yjw in col_names else None
            partition_names = []
            ycxyc__wxn = []
            ojhj__kfudx = []
        fnztw__jhk = None if isinstance(esta__yjw, dict
            ) or esta__yjw is None else esta__yjw
        index_column_index = None
        index_column_type = types.none
        if fnztw__jhk:
            jjpr__begr = col_names.index(fnztw__jhk)
            index_column_index = col_indices.pop(jjpr__begr)
            index_column_type = fph__xsh.pop(jjpr__begr)
            col_names.pop(jjpr__begr)
        for ibaxa__uaekj, c in enumerate(col_names):
            if c in senn__lqc:
                fph__xsh[ibaxa__uaekj] = senn__lqc[c]
        zsqw__cschy = [ir.Var(zsr__pyq, mk_unique_var('pq_table'), uxl__ubw
            ), ir.Var(zsr__pyq, mk_unique_var('pq_index'), uxl__ubw)]
        szizc__tgy = [bodo.ir.parquet_ext.ParquetReader(file_name, lhs.name,
            col_names, col_indices, fph__xsh, zsqw__cschy, uxl__ubw,
            partition_names, storage_options, index_column_index,
            index_column_type, input_file_name_col, ycxyc__wxn, ojhj__kfudx)]
        return (col_names, zsqw__cschy, esta__yjw, szizc__tgy, fph__xsh,
            index_column_type)


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, meta_head_only_info=None):
    vdgk__bqmhg = len(pq_node.out_vars)
    dnf_filter_str = 'None'
    expr_filter_str = 'None'
    ulcg__owj, tmmn__isji = bodo.ir.connector.generate_filter_map(pq_node.
        filters)
    extra_args = ', '.join(ulcg__owj.values())
    dnf_filter_str, expr_filter_str = bodo.ir.connector.generate_arrow_filters(
        pq_node.filters, ulcg__owj, tmmn__isji, pq_node.
        original_df_colnames, pq_node.partition_names, pq_node.
        original_out_types, typemap, 'parquet', output_dnf=False)
    kniqh__fhme = ', '.join(f'out{ibaxa__uaekj}' for ibaxa__uaekj in range(
        vdgk__bqmhg))
    kocxk__xxj = f'def pq_impl(fname, {extra_args}):\n'
    kocxk__xxj += (
        f'    (total_rows, {kniqh__fhme},) = _pq_reader_py(fname, {extra_args})\n'
        )
    mdkyp__wxiwc = {}
    exec(kocxk__xxj, {}, mdkyp__wxiwc)
    enqsg__bbir = mdkyp__wxiwc['pq_impl']
    if bodo.user_logging.get_verbose_level() >= 1:
        wex__vqi = pq_node.loc.strformat()
        zvifu__knizg = []
        xhk__gyik = []
        for ibaxa__uaekj in pq_node.out_used_cols:
            ozcy__cfn = pq_node.df_colnames[ibaxa__uaekj]
            zvifu__knizg.append(ozcy__cfn)
            if isinstance(pq_node.out_types[ibaxa__uaekj], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                xhk__gyik.append(ozcy__cfn)
        mckyt__cvq = (
            'Finish column pruning on read_parquet node:\n%s\nColumns loaded %s\n'
            )
        bodo.user_logging.log_message('Column Pruning', mckyt__cvq,
            wex__vqi, zvifu__knizg)
        if xhk__gyik:
            fbkv__lsaee = """Finished optimized encoding on read_parquet node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                fbkv__lsaee, wex__vqi, xhk__gyik)
    parallel = bodo.ir.connector.is_connector_table_parallel(pq_node,
        array_dists, typemap, 'ParquetReader')
    if pq_node.unsupported_columns:
        lqpa__sil = set(pq_node.out_used_cols)
        ikkl__mvbxp = set(pq_node.unsupported_columns)
        qvyi__ompsc = lqpa__sil & ikkl__mvbxp
        if qvyi__ompsc:
            xgi__dfbjc = sorted(qvyi__ompsc)
            zomsu__kqvrn = [
                f'pandas.read_parquet(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                "Please manually remove these columns from your read_parquet with the 'columns' argument. If these "
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            yzjn__bszkn = 0
            for qcx__tqqu in xgi__dfbjc:
                while pq_node.unsupported_columns[yzjn__bszkn] != qcx__tqqu:
                    yzjn__bszkn += 1
                zomsu__kqvrn.append(
                    f"Column '{pq_node.df_colnames[qcx__tqqu]}' with unsupported arrow type {pq_node.unsupported_arrow_types[yzjn__bszkn]}"
                    )
                yzjn__bszkn += 1
            oue__mtt = '\n'.join(zomsu__kqvrn)
            raise BodoError(oue__mtt, loc=pq_node.loc)
    xcggh__fxbq = _gen_pq_reader_py(pq_node.df_colnames, pq_node.
        col_indices, pq_node.out_used_cols, pq_node.out_types, pq_node.
        storage_options, pq_node.partition_names, dnf_filter_str,
        expr_filter_str, extra_args, parallel, meta_head_only_info, pq_node
        .index_column_index, pq_node.index_column_type, pq_node.
        input_file_name_col, not pq_node.is_live_table)
    idm__zupni = typemap[pq_node.file_name.name]
    xpmu__pkdg = (idm__zupni,) + tuple(typemap[dum__erxo.name] for
        dum__erxo in tmmn__isji)
    cfqgn__orsf = compile_to_numba_ir(enqsg__bbir, {'_pq_reader_py':
        xcggh__fxbq}, typingctx=typingctx, targetctx=targetctx, arg_typs=
        xpmu__pkdg, typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(cfqgn__orsf, [pq_node.file_name] + tmmn__isji)
    szizc__tgy = cfqgn__orsf.body[:-3]
    if meta_head_only_info:
        szizc__tgy[-3].target = meta_head_only_info[1]
    szizc__tgy[-2].target = pq_node.out_vars[0]
    szizc__tgy[-1].target = pq_node.out_vars[1]
    assert not (pq_node.index_column_index is None and not pq_node.
        is_live_table
        ), 'At most one of table and index should be dead if the Parquet IR node is live'
    if pq_node.index_column_index is None:
        szizc__tgy.pop(-1)
    elif not pq_node.is_live_table:
        szizc__tgy.pop(-2)
    return szizc__tgy


distributed_pass.distributed_run_extensions[bodo.ir.parquet_ext.ParquetReader
    ] = pq_distributed_run


def get_filters_pyobject(dnf_filter_str, expr_filter_str, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(dnf_filter_str, expr_filter_str, var_tup):
    djkxy__hahp = get_overload_const_str(dnf_filter_str)
    srjt__rdw = get_overload_const_str(expr_filter_str)
    vlf__nhjk = ', '.join(f'f{ibaxa__uaekj}' for ibaxa__uaekj in range(len(
        var_tup)))
    kocxk__xxj = 'def impl(dnf_filter_str, expr_filter_str, var_tup):\n'
    if len(var_tup):
        kocxk__xxj += f'  {vlf__nhjk}, = var_tup\n'
    kocxk__xxj += """  with numba.objmode(dnf_filters_py='parquet_predicate_type', expr_filters_py='parquet_predicate_type'):
"""
    kocxk__xxj += f'    dnf_filters_py = {djkxy__hahp}\n'
    kocxk__xxj += f'    expr_filters_py = {srjt__rdw}\n'
    kocxk__xxj += '  return (dnf_filters_py, expr_filters_py)\n'
    mdkyp__wxiwc = {}
    exec(kocxk__xxj, globals(), mdkyp__wxiwc)
    return mdkyp__wxiwc['impl']


@numba.njit
def get_fname_pyobject(fname):
    with numba.objmode(fname_py='read_parquet_fpath_type'):
        fname_py = fname
    return fname_py


def _gen_pq_reader_py(col_names, col_indices, out_used_cols, out_types,
    storage_options, partition_names, dnf_filter_str, expr_filter_str,
    extra_args, is_parallel, meta_head_only_info, index_column_index,
    index_column_type, input_file_name_col, is_dead_table):
    wbi__ryto = next_label()
    kjq__uysd = ',' if extra_args else ''
    kocxk__xxj = f'def pq_reader_py(fname,{extra_args}):\n'
    kocxk__xxj += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    kocxk__xxj += f"    ev.add_attribute('g_fname', fname)\n"
    kocxk__xxj += f"""    dnf_filters, expr_filters = get_filters_pyobject("{dnf_filter_str}", "{expr_filter_str}", ({extra_args}{kjq__uysd}))
"""
    kocxk__xxj += '    fname_py = get_fname_pyobject(fname)\n'
    storage_options['bodo_dummy'] = 'dummy'
    kocxk__xxj += (
        f'    storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    tot_rows_to_read = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        tot_rows_to_read = meta_head_only_info[0]
    amv__iammz = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    input_file_name_col = sanitize_varname(input_file_name_col
        ) if input_file_name_col is not None and col_names.index(
        input_file_name_col) in out_used_cols else None
    xvi__doku = {c: ibaxa__uaekj for ibaxa__uaekj, c in enumerate(col_indices)}
    bnite__vdm = {c: ibaxa__uaekj for ibaxa__uaekj, c in enumerate(amv__iammz)}
    xdy__uulpk = []
    iva__otrsp = set()
    nexoc__pbvad = partition_names + [input_file_name_col]
    for ibaxa__uaekj in out_used_cols:
        if amv__iammz[ibaxa__uaekj] not in nexoc__pbvad:
            xdy__uulpk.append(col_indices[ibaxa__uaekj])
        elif not input_file_name_col or amv__iammz[ibaxa__uaekj
            ] != input_file_name_col:
            iva__otrsp.add(col_indices[ibaxa__uaekj])
    if index_column_index is not None:
        xdy__uulpk.append(index_column_index)
    xdy__uulpk = sorted(xdy__uulpk)
    ioeak__jvt = {c: ibaxa__uaekj for ibaxa__uaekj, c in enumerate(xdy__uulpk)}
    hsgq__dih = [(int(is_nullable(out_types[xvi__doku[kbulh__snpnq]])) if 
        kbulh__snpnq != index_column_index else int(is_nullable(
        index_column_type))) for kbulh__snpnq in xdy__uulpk]
    str_as_dict_cols = []
    for kbulh__snpnq in xdy__uulpk:
        if kbulh__snpnq == index_column_index:
            qxr__taaoh = index_column_type
        else:
            qxr__taaoh = out_types[xvi__doku[kbulh__snpnq]]
        if qxr__taaoh == dict_str_arr_type:
            str_as_dict_cols.append(kbulh__snpnq)
    uujqn__wae = []
    nkf__ejd = {}
    nwy__cpth = []
    lcc__dzkw = []
    for ibaxa__uaekj, mkma__mzip in enumerate(partition_names):
        try:
            zndyx__mst = bnite__vdm[mkma__mzip]
            if col_indices[zndyx__mst] not in iva__otrsp:
                continue
        except (KeyError, ValueError) as wlu__oad:
            continue
        nkf__ejd[mkma__mzip] = len(uujqn__wae)
        uujqn__wae.append(mkma__mzip)
        nwy__cpth.append(ibaxa__uaekj)
        lcx__ojk = out_types[zndyx__mst].dtype
        ief__uef = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            lcx__ojk)
        lcc__dzkw.append(numba_to_c_type(ief__uef))
    kocxk__xxj += f'    total_rows_np = np.array([0], dtype=np.int64)\n'
    kocxk__xxj += f'    out_table = pq_read(\n'
    kocxk__xxj += f'        fname_py, {is_parallel},\n'
    kocxk__xxj += f'        dnf_filters, expr_filters,\n'
    kocxk__xxj += f"""        storage_options_py, {tot_rows_to_read}, selected_cols_arr_{wbi__ryto}.ctypes,
"""
    kocxk__xxj += f'        {len(xdy__uulpk)},\n'
    kocxk__xxj += f'        nullable_cols_arr_{wbi__ryto}.ctypes,\n'
    if len(nwy__cpth) > 0:
        kocxk__xxj += (
            f'        np.array({nwy__cpth}, dtype=np.int32).ctypes,\n')
        kocxk__xxj += (
            f'        np.array({lcc__dzkw}, dtype=np.int32).ctypes,\n')
        kocxk__xxj += f'        {len(nwy__cpth)},\n'
    else:
        kocxk__xxj += f'        0, 0, 0,\n'
    if len(str_as_dict_cols) > 0:
        kocxk__xxj += f"""        np.array({str_as_dict_cols}, dtype=np.int32).ctypes, {len(str_as_dict_cols)},
"""
    else:
        kocxk__xxj += f'        0, 0,\n'
    kocxk__xxj += f'        total_rows_np.ctypes,\n'
    kocxk__xxj += f'        {input_file_name_col is not None},\n'
    kocxk__xxj += f'    )\n'
    kocxk__xxj += f'    check_and_propagate_cpp_exception()\n'
    kocxk__xxj += f'    total_rows = total_rows_np[0]\n'
    if is_parallel:
        kocxk__xxj += f"""    local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
    else:
        kocxk__xxj += f'    local_rows = total_rows\n'
    cfyg__jijmp = index_column_type
    sywt__pxbwh = TableType(tuple(out_types))
    if is_dead_table:
        sywt__pxbwh = types.none
    if is_dead_table:
        cevx__xjn = None
    else:
        cevx__xjn = []
        qcvgd__jkeqt = 0
        upcs__tkxi = col_indices[col_names.index(input_file_name_col)
            ] if input_file_name_col is not None else None
        for ibaxa__uaekj, qcx__tqqu in enumerate(col_indices):
            if qcvgd__jkeqt < len(out_used_cols
                ) and ibaxa__uaekj == out_used_cols[qcvgd__jkeqt]:
                jjkcs__wdc = col_indices[ibaxa__uaekj]
                if upcs__tkxi and jjkcs__wdc == upcs__tkxi:
                    cevx__xjn.append(len(xdy__uulpk) + len(uujqn__wae))
                elif jjkcs__wdc in iva__otrsp:
                    uabyh__iwm = amv__iammz[ibaxa__uaekj]
                    cevx__xjn.append(len(xdy__uulpk) + nkf__ejd[uabyh__iwm])
                else:
                    cevx__xjn.append(ioeak__jvt[qcx__tqqu])
                qcvgd__jkeqt += 1
            else:
                cevx__xjn.append(-1)
        cevx__xjn = np.array(cevx__xjn, dtype=np.int64)
    if is_dead_table:
        kocxk__xxj += '    T = None\n'
    else:
        kocxk__xxj += f"""    T = cpp_table_to_py_table(out_table, table_idx_{wbi__ryto}, py_table_type_{wbi__ryto})
"""
        if len(out_used_cols) == 0:
            kocxk__xxj += f'    T = set_table_len(T, local_rows)\n'
    if index_column_index is None:
        kocxk__xxj += '    index_arr = None\n'
    else:
        aali__eyrqv = ioeak__jvt[index_column_index]
        kocxk__xxj += f"""    index_arr = info_to_array(info_from_table(out_table, {aali__eyrqv}), index_arr_type)
"""
    kocxk__xxj += f'    delete_table(out_table)\n'
    kocxk__xxj += f'    ev.finalize()\n'
    kocxk__xxj += f'    return (total_rows, T, index_arr)\n'
    mdkyp__wxiwc = {}
    dyg__puz = {f'py_table_type_{wbi__ryto}': sywt__pxbwh,
        f'table_idx_{wbi__ryto}': cevx__xjn,
        f'selected_cols_arr_{wbi__ryto}': np.array(xdy__uulpk, np.int32),
        f'nullable_cols_arr_{wbi__ryto}': np.array(hsgq__dih, np.int32),
        'index_arr_type': cfyg__jijmp, 'cpp_table_to_py_table':
        cpp_table_to_py_table, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'delete_table': delete_table,
        'check_and_propagate_cpp_exception':
        check_and_propagate_cpp_exception, 'pq_read': _pq_read,
        'unicode_to_utf8': unicode_to_utf8, 'get_filters_pyobject':
        get_filters_pyobject, 'get_storage_options_pyobject':
        get_storage_options_pyobject, 'get_fname_pyobject':
        get_fname_pyobject, 'np': np, 'pd': pd, 'bodo': bodo,
        'get_node_portion': bodo.libs.distributed_api.get_node_portion,
        'set_table_len': bodo.hiframes.table.set_table_len}
    exec(kocxk__xxj, dyg__puz, mdkyp__wxiwc)
    xcggh__fxbq = mdkyp__wxiwc['pq_reader_py']
    zcmka__spszr = numba.njit(xcggh__fxbq, no_cpython_wrapper=True)
    return zcmka__spszr


def unify_schemas(schemas):
    zjbd__hkmej = []
    for schema in schemas:
        for ibaxa__uaekj in range(len(schema)):
            pfuow__hqkcu = schema.field(ibaxa__uaekj)
            if pfuow__hqkcu.type == pa.large_string():
                schema = schema.set(ibaxa__uaekj, pfuow__hqkcu.with_type(pa
                    .string()))
            elif pfuow__hqkcu.type == pa.large_binary():
                schema = schema.set(ibaxa__uaekj, pfuow__hqkcu.with_type(pa
                    .binary()))
            elif isinstance(pfuow__hqkcu.type, (pa.ListType, pa.LargeListType)
                ) and pfuow__hqkcu.type.value_type in (pa.string(), pa.
                large_string()):
                schema = schema.set(ibaxa__uaekj, pfuow__hqkcu.with_type(pa
                    .list_(pa.field(pfuow__hqkcu.type.value_field.name, pa.
                    string()))))
            elif isinstance(pfuow__hqkcu.type, pa.LargeListType):
                schema = schema.set(ibaxa__uaekj, pfuow__hqkcu.with_type(pa
                    .list_(pa.field(pfuow__hqkcu.type.value_field.name,
                    pfuow__hqkcu.type.value_type))))
        zjbd__hkmej.append(schema)
    return pa.unify_schemas(zjbd__hkmej)


class ParquetDataset(object):

    def __init__(self, pa_pq_dataset, prefix=''):
        self.schema = pa_pq_dataset.schema
        self.filesystem = None
        self._bodo_total_rows = 0
        self._prefix = prefix
        self.partitioning = None
        partitioning = pa_pq_dataset.partitioning
        self.partition_names = ([] if partitioning is None or partitioning.
            schema == pa_pq_dataset.schema else list(partitioning.schema.names)
            )
        if self.partition_names:
            self.partitioning_dictionaries = partitioning.dictionaries
            self.partitioning_cls = partitioning.__class__
            self.partitioning_schema = partitioning.schema
        else:
            self.partitioning_dictionaries = {}
        for ibaxa__uaekj in range(len(self.schema)):
            pfuow__hqkcu = self.schema.field(ibaxa__uaekj)
            if pfuow__hqkcu.type == pa.large_string():
                self.schema = self.schema.set(ibaxa__uaekj, pfuow__hqkcu.
                    with_type(pa.string()))
        self.pieces = [ParquetPiece(frag, partitioning, self.
            partition_names) for frag in pa_pq_dataset._dataset.
            get_fragments(filter=pa_pq_dataset._filter_expression)]

    def set_fs(self, fs):
        self.filesystem = fs
        for rjivg__gyij in self.pieces:
            rjivg__gyij.filesystem = fs

    def __setstate__(self, state):
        self.__dict__ = state
        if self.partition_names:
            zkysr__pwrj = {rjivg__gyij: self.partitioning_dictionaries[
                ibaxa__uaekj] for ibaxa__uaekj, rjivg__gyij in enumerate(
                self.partition_names)}
            self.partitioning = self.partitioning_cls(self.
                partitioning_schema, zkysr__pwrj)


class ParquetPiece(object):

    def __init__(self, frag, partitioning, partition_names):
        self._frag = None
        self.format = frag.format
        self.path = frag.path
        self._bodo_num_rows = 0
        self.partition_keys = []
        if partitioning is not None:
            self.partition_keys = ds._get_partition_keys(frag.
                partition_expression)
            self.partition_keys = [(mkma__mzip, partitioning.dictionaries[
                ibaxa__uaekj].index(self.partition_keys[mkma__mzip]).as_py(
                )) for ibaxa__uaekj, mkma__mzip in enumerate(partition_names)]

    @property
    def frag(self):
        if self._frag is None:
            self._frag = self.format.make_fragment(self.path, self.filesystem)
            del self.format
        return self._frag

    @property
    def metadata(self):
        return self.frag.metadata

    @property
    def num_row_groups(self):
        return self.frag.num_row_groups


def get_parquet_dataset(fpath, get_row_counts=True, dnf_filters=None,
    expr_filters=None, storage_options=None, read_categories=False,
    is_parallel=False, tot_rows_to_read=None, typing_pa_schema=None,
    partitioning='hive'):
    if get_row_counts:
        uopf__sky = tracing.Event('get_parquet_dataset')
    import time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    jsa__bsnz = MPI.COMM_WORLD
    if isinstance(fpath, list):
        mwq__gzbt = urlparse(fpath[0])
        protocol = mwq__gzbt.scheme
        owd__qqvnt = mwq__gzbt.netloc
        for ibaxa__uaekj in range(len(fpath)):
            pfuow__hqkcu = fpath[ibaxa__uaekj]
            fgde__vrm = urlparse(pfuow__hqkcu)
            if fgde__vrm.scheme != protocol:
                raise BodoError(
                    'All parquet files must use the same filesystem protocol')
            if fgde__vrm.netloc != owd__qqvnt:
                raise BodoError(
                    'All parquet files must be in the same S3 bucket')
            fpath[ibaxa__uaekj] = pfuow__hqkcu.rstrip('/')
    else:
        mwq__gzbt = urlparse(fpath)
        protocol = mwq__gzbt.scheme
        fpath = fpath.rstrip('/')
    if protocol in {'gcs', 'gs'}:
        try:
            import gcsfs
        except ImportError as wlu__oad:
            fpsgd__gxpm = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(fpsgd__gxpm)
    if protocol == 'http':
        try:
            import fsspec
        except ImportError as wlu__oad:
            fpsgd__gxpm = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
"""
    fs = []

    def getfs(parallel=False):
        if len(fs) == 1:
            return fs[0]
        if protocol == 's3':
            fs.append(get_s3_fs_from_path(fpath, parallel=parallel,
                storage_options=storage_options) if not isinstance(fpath,
                list) else get_s3_fs_from_path(fpath[0], parallel=parallel,
                storage_options=storage_options))
        elif protocol in {'gcs', 'gs'}:
            lsbgf__aqhu = gcsfs.GCSFileSystem(token=None)
            fs.append(PyFileSystem(FSSpecHandler(lsbgf__aqhu)))
        elif protocol == 'http':
            fs.append(PyFileSystem(FSSpecHandler(fsspec.filesystem('http'))))
        elif protocol in {'hdfs', 'abfs', 'abfss'}:
            fs.append(get_hdfs_fs(fpath) if not isinstance(fpath, list) else
                get_hdfs_fs(fpath[0]))
        else:
            fs.append(pa.fs.LocalFileSystem())
        return fs[0]

    def glob(protocol, fs, path):
        if not protocol and fs is None:
            from fsspec.implementations.local import LocalFileSystem
            fs = LocalFileSystem()
        if isinstance(fs, pa.fs.FileSystem):
            from fsspec.implementations.arrow import ArrowFSWrapper
            fs = ArrowFSWrapper(fs)
        try:
            mvvip__qxx = fs.glob(path)
        except:
            raise BodoError(
                f'glob pattern expansion not supported for {protocol}')
        if len(mvvip__qxx) == 0:
            raise BodoError('No files found matching glob pattern')
        return mvvip__qxx
    ran__sbtox = False
    if get_row_counts:
        ldn__wcqyi = getfs(parallel=True)
        ran__sbtox = bodo.parquet_validate_schema
    if bodo.get_rank() == 0:
        vucr__oawrb = 1
        tgzt__xesln = os.cpu_count()
        if tgzt__xesln is not None and tgzt__xesln > 1:
            vucr__oawrb = tgzt__xesln // 2
        try:
            if get_row_counts:
                qwj__vpww = tracing.Event('pq.ParquetDataset', is_parallel=
                    False)
                if tracing.is_tracing():
                    qwj__vpww.add_attribute('g_dnf_filter', str(dnf_filters))
            gfy__wvmpv = pa.io_thread_count()
            pa.set_io_thread_count(vucr__oawrb)
            prefix = ''
            if protocol == 's3':
                prefix = 's3://'
            elif protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{mwq__gzbt.netloc}'
            if prefix:
                if isinstance(fpath, list):
                    fsef__cndex = [pfuow__hqkcu[len(prefix):] for
                        pfuow__hqkcu in fpath]
                else:
                    fsef__cndex = fpath[len(prefix):]
            else:
                fsef__cndex = fpath
            if isinstance(fsef__cndex, list):
                gno__qhrls = []
                for rjivg__gyij in fsef__cndex:
                    if has_magic(rjivg__gyij):
                        gno__qhrls += glob(protocol, getfs(), rjivg__gyij)
                    else:
                        gno__qhrls.append(rjivg__gyij)
                fsef__cndex = gno__qhrls
            elif has_magic(fsef__cndex):
                fsef__cndex = glob(protocol, getfs(), fsef__cndex)
            zdm__hyd = pq.ParquetDataset(fsef__cndex, filesystem=getfs(),
                filters=None, use_legacy_dataset=False, partitioning=
                partitioning)
            if dnf_filters is not None:
                zdm__hyd._filters = dnf_filters
                zdm__hyd._filter_expression = pq._filters_to_expression(
                    dnf_filters)
            pgp__hxbk = len(zdm__hyd.files)
            zdm__hyd = ParquetDataset(zdm__hyd, prefix)
            pa.set_io_thread_count(gfy__wvmpv)
            if typing_pa_schema:
                zdm__hyd.schema = typing_pa_schema
            if get_row_counts:
                if dnf_filters is not None:
                    qwj__vpww.add_attribute('num_pieces_before_filter',
                        pgp__hxbk)
                    qwj__vpww.add_attribute('num_pieces_after_filter', len(
                        zdm__hyd.pieces))
                qwj__vpww.finalize()
        except Exception as hzox__akr:
            if isinstance(hzox__akr, IsADirectoryError):
                hzox__akr = BodoError(list_of_files_error_msg)
            elif isinstance(fpath, list) and isinstance(hzox__akr, (OSError,
                FileNotFoundError)):
                hzox__akr = BodoError(str(hzox__akr) + list_of_files_error_msg)
            else:
                hzox__akr = BodoError(
                    f"""error from pyarrow: {type(hzox__akr).__name__}: {str(hzox__akr)}
"""
                    )
            jsa__bsnz.bcast(hzox__akr)
            raise hzox__akr
        if get_row_counts:
            mzukc__oir = tracing.Event('bcast dataset')
        zdm__hyd = jsa__bsnz.bcast(zdm__hyd)
    else:
        if get_row_counts:
            mzukc__oir = tracing.Event('bcast dataset')
        zdm__hyd = jsa__bsnz.bcast(None)
        if isinstance(zdm__hyd, Exception):
            rth__fvy = zdm__hyd
            raise rth__fvy
    zdm__hyd.set_fs(getfs())
    if get_row_counts:
        mzukc__oir.finalize()
    if get_row_counts and tot_rows_to_read == 0:
        get_row_counts = ran__sbtox = False
    if get_row_counts or ran__sbtox:
        if get_row_counts and tracing.is_tracing():
            mflxg__omnol = tracing.Event('get_row_counts')
            mflxg__omnol.add_attribute('g_num_pieces', len(zdm__hyd.pieces))
            mflxg__omnol.add_attribute('g_expr_filters', str(expr_filters))
        nobf__faczs = 0.0
        num_pieces = len(zdm__hyd.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        ucos__xmfsy = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        fbcde__gwm = 0
        gjsgc__tbe = 0
        hsbh__ula = 0
        dto__zzf = True
        if expr_filters is not None:
            import random
            random.seed(37)
            hgibj__mwuv = random.sample(zdm__hyd.pieces, k=len(zdm__hyd.pieces)
                )
        else:
            hgibj__mwuv = zdm__hyd.pieces
        fpaths = [rjivg__gyij.path for rjivg__gyij in hgibj__mwuv[start:
            ucos__xmfsy]]
        vucr__oawrb = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), 4)
        pa.set_io_thread_count(vucr__oawrb)
        pa.set_cpu_count(vucr__oawrb)
        rth__fvy = None
        try:
            fwzmu__rnn = ds.dataset(fpaths, filesystem=zdm__hyd.filesystem,
                partitioning=zdm__hyd.partitioning)
            for cmd__hwz, frag in zip(hgibj__mwuv[start:ucos__xmfsy],
                fwzmu__rnn.get_fragments()):
                if ran__sbtox:
                    ert__cacgy = frag.metadata.schema.to_arrow_schema()
                    lwh__wozdo = set(ert__cacgy.names)
                    vkd__pjtp = set(zdm__hyd.schema.names) - set(zdm__hyd.
                        partition_names)
                    if vkd__pjtp != lwh__wozdo:
                        kdn__hrb = lwh__wozdo - vkd__pjtp
                        txzwo__ynev = vkd__pjtp - lwh__wozdo
                        huar__upj = f'Schema in {cmd__hwz} was different.\n'
                        if kdn__hrb:
                            huar__upj += f"""File contains column(s) {kdn__hrb} not found in other files in the dataset.
"""
                        if txzwo__ynev:
                            huar__upj += f"""File missing column(s) {txzwo__ynev} found in other files in the dataset.
"""
                        raise BodoError(huar__upj)
                    try:
                        zdm__hyd.schema = unify_schemas([zdm__hyd.schema,
                            ert__cacgy])
                    except Exception as hzox__akr:
                        huar__upj = (
                            f'Schema in {cmd__hwz} was different.\n' + str(
                            hzox__akr))
                        raise BodoError(huar__upj)
                kkd__leagj = time.time()
                hne__jnu = frag.scanner(schema=fwzmu__rnn.schema, filter=
                    expr_filters, use_threads=True).count_rows()
                nobf__faczs += time.time() - kkd__leagj
                cmd__hwz._bodo_num_rows = hne__jnu
                fbcde__gwm += hne__jnu
                gjsgc__tbe += frag.num_row_groups
                hsbh__ula += sum(uzek__tgkv.total_byte_size for uzek__tgkv in
                    frag.row_groups)
        except Exception as hzox__akr:
            rth__fvy = hzox__akr
        if jsa__bsnz.allreduce(rth__fvy is not None, op=MPI.LOR):
            for rth__fvy in jsa__bsnz.allgather(rth__fvy):
                if rth__fvy:
                    if isinstance(fpath, list) and isinstance(rth__fvy, (
                        OSError, FileNotFoundError)):
                        raise BodoError(str(rth__fvy) + list_of_files_error_msg
                            )
                    raise rth__fvy
        if ran__sbtox:
            dto__zzf = jsa__bsnz.allreduce(dto__zzf, op=MPI.LAND)
            if not dto__zzf:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            zdm__hyd._bodo_total_rows = jsa__bsnz.allreduce(fbcde__gwm, op=
                MPI.SUM)
            svcx__scel = jsa__bsnz.allreduce(gjsgc__tbe, op=MPI.SUM)
            omth__dmluu = jsa__bsnz.allreduce(hsbh__ula, op=MPI.SUM)
            zsy__npec = np.array([rjivg__gyij._bodo_num_rows for
                rjivg__gyij in zdm__hyd.pieces])
            zsy__npec = jsa__bsnz.allreduce(zsy__npec, op=MPI.SUM)
            for rjivg__gyij, cota__dhzb in zip(zdm__hyd.pieces, zsy__npec):
                rjivg__gyij._bodo_num_rows = cota__dhzb
            if is_parallel and bodo.get_rank(
                ) == 0 and svcx__scel < bodo.get_size() and svcx__scel != 0:
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({svcx__scel}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()}). For more details, refer to
https://docs.bodo.ai/latest/file_io/#parquet-section.
"""
                    ))
            if svcx__scel == 0:
                dfdu__dffub = 0
            else:
                dfdu__dffub = omth__dmluu // svcx__scel
            if (bodo.get_rank() == 0 and omth__dmluu >= 20 * 1048576 and 
                dfdu__dffub < 1048576 and protocol in REMOTE_FILESYSTEMS):
                warnings.warn(BodoWarning(
                    f'Parquet average row group size is small ({dfdu__dffub} bytes) and can have negative impact on performance when reading from remote sources'
                    ))
            if tracing.is_tracing():
                mflxg__omnol.add_attribute('g_total_num_row_groups', svcx__scel
                    )
                mflxg__omnol.add_attribute('total_scan_time', nobf__faczs)
                gcz__blr = np.array([rjivg__gyij._bodo_num_rows for
                    rjivg__gyij in zdm__hyd.pieces])
                zesl__bczc = np.percentile(gcz__blr, [25, 50, 75])
                mflxg__omnol.add_attribute('g_row_counts_min', gcz__blr.min())
                mflxg__omnol.add_attribute('g_row_counts_Q1', zesl__bczc[0])
                mflxg__omnol.add_attribute('g_row_counts_median', zesl__bczc[1]
                    )
                mflxg__omnol.add_attribute('g_row_counts_Q3', zesl__bczc[2])
                mflxg__omnol.add_attribute('g_row_counts_max', gcz__blr.max())
                mflxg__omnol.add_attribute('g_row_counts_mean', gcz__blr.mean()
                    )
                mflxg__omnol.add_attribute('g_row_counts_std', gcz__blr.std())
                mflxg__omnol.add_attribute('g_row_counts_sum', gcz__blr.sum())
                mflxg__omnol.finalize()
    if read_categories:
        _add_categories_to_pq_dataset(zdm__hyd)
    if get_row_counts:
        uopf__sky.finalize()
    if ran__sbtox and is_parallel:
        if tracing.is_tracing():
            fmvjb__cueu = tracing.Event('unify_schemas_across_ranks')
        rth__fvy = None
        try:
            zdm__hyd.schema = jsa__bsnz.allreduce(zdm__hyd.schema, bodo.io.
                helpers.pa_schema_unify_mpi_op)
        except Exception as hzox__akr:
            rth__fvy = hzox__akr
        if tracing.is_tracing():
            fmvjb__cueu.finalize()
        if jsa__bsnz.allreduce(rth__fvy is not None, op=MPI.LOR):
            for rth__fvy in jsa__bsnz.allgather(rth__fvy):
                if rth__fvy:
                    huar__upj = (f'Schema in some files were different.\n' +
                        str(rth__fvy))
                    raise BodoError(huar__upj)
    return zdm__hyd


def get_scanner_batches(fpaths, expr_filters, selected_fields,
    avg_num_pieces, is_parallel, filesystem, str_as_dict_cols, start_offset,
    rows_to_read, partitioning, schema):
    import pyarrow as pa
    tgzt__xesln = os.cpu_count()
    if tgzt__xesln is None or tgzt__xesln == 0:
        tgzt__xesln = 2
    fkm__exh = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), tgzt__xesln)
    mle__jpawb = min(int(os.environ.get('BODO_MAX_IO_THREADS', 16)),
        tgzt__xesln)
    if is_parallel and len(fpaths) > mle__jpawb and len(fpaths
        ) / avg_num_pieces >= 2.0:
        pa.set_io_thread_count(mle__jpawb)
        pa.set_cpu_count(mle__jpawb)
    else:
        pa.set_io_thread_count(fkm__exh)
        pa.set_cpu_count(fkm__exh)
    lnex__zcm = ds.ParquetFileFormat(dictionary_columns=str_as_dict_cols)
    ilwzj__omxuh = set(str_as_dict_cols)
    for ibaxa__uaekj, name in enumerate(schema.names):
        if name in ilwzj__omxuh:
            yvtjt__vzm = schema.field(ibaxa__uaekj)
            nytiy__wvuc = pa.field(name, pa.dictionary(pa.int32(),
                yvtjt__vzm.type), yvtjt__vzm.nullable)
            schema = schema.remove(ibaxa__uaekj).insert(ibaxa__uaekj,
                nytiy__wvuc)
    zdm__hyd = ds.dataset(fpaths, filesystem=filesystem, partitioning=
        partitioning, schema=schema, format=lnex__zcm)
    col_names = zdm__hyd.schema.names
    qqei__yfips = [col_names[kvzt__tzuz] for kvzt__tzuz in selected_fields]
    cojyn__ygfod = len(fpaths) <= 3 or start_offset > 0 and len(fpaths) <= 10
    if cojyn__ygfod and expr_filters is None:
        doqby__fbc = []
        zqr__liw = 0
        sbomv__mhmbo = 0
        for frag in zdm__hyd.get_fragments():
            imj__nczd = []
            for uzek__tgkv in frag.row_groups:
                lwbnn__rqfi = uzek__tgkv.num_rows
                if start_offset < zqr__liw + lwbnn__rqfi:
                    if sbomv__mhmbo == 0:
                        mduov__wnsd = start_offset - zqr__liw
                        ofsor__ifl = min(lwbnn__rqfi - mduov__wnsd,
                            rows_to_read)
                    else:
                        ofsor__ifl = min(lwbnn__rqfi, rows_to_read -
                            sbomv__mhmbo)
                    sbomv__mhmbo += ofsor__ifl
                    imj__nczd.append(uzek__tgkv.id)
                zqr__liw += lwbnn__rqfi
                if sbomv__mhmbo == rows_to_read:
                    break
            doqby__fbc.append(frag.subset(row_group_ids=imj__nczd))
            if sbomv__mhmbo == rows_to_read:
                break
        zdm__hyd = ds.FileSystemDataset(doqby__fbc, zdm__hyd.schema,
            lnex__zcm, filesystem=zdm__hyd.filesystem)
        start_offset = mduov__wnsd
    vwrxe__csg = zdm__hyd.scanner(columns=qqei__yfips, filter=expr_filters,
        use_threads=True).to_reader()
    return zdm__hyd, vwrxe__csg, start_offset


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    pa_schema = pq_dataset.schema
    twbo__ziwqu = [c for c in pa_schema.names if isinstance(pa_schema.field
        (c).type, pa.DictionaryType) and c not in pq_dataset.partition_names]
    if len(twbo__ziwqu) == 0:
        pq_dataset._category_info = {}
        return
    jsa__bsnz = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            ald__ggw = pq_dataset.pieces[0].frag.head(100, columns=twbo__ziwqu)
            lywld__gud = {c: tuple(ald__ggw.column(c).chunk(0).dictionary.
                to_pylist()) for c in twbo__ziwqu}
            del ald__ggw
        except Exception as hzox__akr:
            jsa__bsnz.bcast(hzox__akr)
            raise hzox__akr
        jsa__bsnz.bcast(lywld__gud)
    else:
        lywld__gud = jsa__bsnz.bcast(None)
        if isinstance(lywld__gud, Exception):
            rth__fvy = lywld__gud
            raise rth__fvy
    pq_dataset._category_info = lywld__gud


def get_pandas_metadata(schema, num_pieces):
    esta__yjw = None
    tfxs__rnob = defaultdict(lambda : None)
    bae__rmq = b'pandas'
    if schema.metadata is not None and bae__rmq in schema.metadata:
        import json
        bpvsk__reud = json.loads(schema.metadata[bae__rmq].decode('utf8'))
        sxt__kvd = len(bpvsk__reud['index_columns'])
        if sxt__kvd > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        esta__yjw = bpvsk__reud['index_columns'][0] if sxt__kvd else None
        if not isinstance(esta__yjw, str) and not isinstance(esta__yjw, dict):
            esta__yjw = None
        for djsxb__udse in bpvsk__reud['columns']:
            qpf__ehl = djsxb__udse['name']
            if djsxb__udse['pandas_type'].startswith('int'
                ) and qpf__ehl is not None:
                if djsxb__udse['numpy_type'].startswith('Int'):
                    tfxs__rnob[qpf__ehl] = True
                else:
                    tfxs__rnob[qpf__ehl] = False
    return esta__yjw, tfxs__rnob


def get_str_columns_from_pa_schema(pa_schema):
    str_columns = []
    for qpf__ehl in pa_schema.names:
        tbmgr__odipz = pa_schema.field(qpf__ehl)
        if tbmgr__odipz.type in (pa.string(), pa.large_string()):
            str_columns.append(qpf__ehl)
    return str_columns


def determine_str_as_dict_columns(pq_dataset, pa_schema, str_columns):
    from mpi4py import MPI
    jsa__bsnz = MPI.COMM_WORLD
    if len(str_columns) == 0:
        return set()
    if len(pq_dataset.pieces) > bodo.get_size():
        import random
        random.seed(37)
        hgibj__mwuv = random.sample(pq_dataset.pieces, bodo.get_size())
    else:
        hgibj__mwuv = pq_dataset.pieces
    wrauc__rsdy = np.zeros(len(str_columns), dtype=np.int64)
    qguzf__jece = np.zeros(len(str_columns), dtype=np.int64)
    if bodo.get_rank() < len(hgibj__mwuv):
        cmd__hwz = hgibj__mwuv[bodo.get_rank()]
        try:
            metadata = cmd__hwz.metadata
            for ibaxa__uaekj in range(cmd__hwz.num_row_groups):
                for qcvgd__jkeqt, qpf__ehl in enumerate(str_columns):
                    yzjn__bszkn = pa_schema.get_field_index(qpf__ehl)
                    wrauc__rsdy[qcvgd__jkeqt] += metadata.row_group(
                        ibaxa__uaekj).column(yzjn__bszkn
                        ).total_uncompressed_size
            bchm__bmi = metadata.num_rows
        except Exception as hzox__akr:
            if isinstance(hzox__akr, (OSError, FileNotFoundError)):
                bchm__bmi = 0
            else:
                raise
    else:
        bchm__bmi = 0
    rxr__tng = jsa__bsnz.allreduce(bchm__bmi, op=MPI.SUM)
    if rxr__tng == 0:
        return set()
    jsa__bsnz.Allreduce(wrauc__rsdy, qguzf__jece, op=MPI.SUM)
    imits__wkw = qguzf__jece / rxr__tng
    pfke__nyytg = set()
    for ibaxa__uaekj, ell__duyd in enumerate(imits__wkw):
        if ell__duyd < READ_STR_AS_DICT_THRESHOLD:
            qpf__ehl = str_columns[ibaxa__uaekj][0]
            pfke__nyytg.add(qpf__ehl)
    return pfke__nyytg


def parquet_file_schema(file_name, selected_columns, storage_options=None,
    input_file_name_col=None, read_as_dict_cols=None):
    col_names = []
    fph__xsh = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True)
    partition_names = pq_dataset.partition_names
    pa_schema = pq_dataset.schema
    num_pieces = len(pq_dataset.pieces)
    str_columns = get_str_columns_from_pa_schema(pa_schema)
    zcb__evqjw = set(str_columns)
    if read_as_dict_cols is None:
        read_as_dict_cols = []
    read_as_dict_cols = set(read_as_dict_cols)
    owj__vispe = read_as_dict_cols - zcb__evqjw
    if len(owj__vispe) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {owj__vispe}'
                , bodo.utils.typing.BodoWarning)
    read_as_dict_cols.intersection_update(zcb__evqjw)
    zcb__evqjw = zcb__evqjw - read_as_dict_cols
    str_columns = [cgb__wlba for cgb__wlba in str_columns if cgb__wlba in
        zcb__evqjw]
    pfke__nyytg: set = determine_str_as_dict_columns(pq_dataset, pa_schema,
        str_columns)
    pfke__nyytg.update(read_as_dict_cols)
    col_names = pa_schema.names
    esta__yjw, tfxs__rnob = get_pandas_metadata(pa_schema, num_pieces)
    wnmqb__pgh = []
    nlxov__thgdj = []
    qoych__arj = []
    for ibaxa__uaekj, c in enumerate(col_names):
        if c in partition_names:
            continue
        tbmgr__odipz = pa_schema.field(c)
        oxqp__mfsxm, iuwjh__sqtc = _get_numba_typ_from_pa_typ(tbmgr__odipz,
            c == esta__yjw, tfxs__rnob[c], pq_dataset._category_info,
            str_as_dict=c in pfke__nyytg)
        wnmqb__pgh.append(oxqp__mfsxm)
        nlxov__thgdj.append(iuwjh__sqtc)
        qoych__arj.append(tbmgr__odipz.type)
    if partition_names:
        wnmqb__pgh += [_get_partition_cat_dtype(pq_dataset.
            partitioning_dictionaries[ibaxa__uaekj]) for ibaxa__uaekj in
            range(len(partition_names))]
        nlxov__thgdj.extend([True] * len(partition_names))
        qoych__arj.extend([None] * len(partition_names))
    if input_file_name_col is not None:
        col_names += [input_file_name_col]
        wnmqb__pgh += [dict_str_arr_type]
        nlxov__thgdj.append(True)
        qoych__arj.append(None)
    avif__cpez = {c: ibaxa__uaekj for ibaxa__uaekj, c in enumerate(col_names)}
    if selected_columns is None:
        selected_columns = col_names
    for c in selected_columns:
        if c not in avif__cpez:
            raise BodoError(f'Selected column {c} not in Parquet file schema')
    if esta__yjw and not isinstance(esta__yjw, dict
        ) and esta__yjw not in selected_columns:
        selected_columns.append(esta__yjw)
    col_names = selected_columns
    col_indices = []
    fph__xsh = []
    ycxyc__wxn = []
    ojhj__kfudx = []
    for ibaxa__uaekj, c in enumerate(col_names):
        jjkcs__wdc = avif__cpez[c]
        col_indices.append(jjkcs__wdc)
        fph__xsh.append(wnmqb__pgh[jjkcs__wdc])
        if not nlxov__thgdj[jjkcs__wdc]:
            ycxyc__wxn.append(ibaxa__uaekj)
            ojhj__kfudx.append(qoych__arj[jjkcs__wdc])
    return (col_names, fph__xsh, esta__yjw, col_indices, partition_names,
        ycxyc__wxn, ojhj__kfudx)


def _get_partition_cat_dtype(dictionary):
    assert dictionary is not None
    yzq__yig = dictionary.to_pandas()
    guc__fwnb = bodo.typeof(yzq__yig).dtype
    if isinstance(guc__fwnb, types.Integer):
        gtn__zja = PDCategoricalDtype(tuple(yzq__yig), guc__fwnb, False,
            int_type=guc__fwnb)
    else:
        gtn__zja = PDCategoricalDtype(tuple(yzq__yig), guc__fwnb, False)
    return CategoricalArrayType(gtn__zja)


_pq_read = types.ExternalFunction('pq_read', table_type(
    read_parquet_fpath_type, types.boolean, parquet_predicate_type,
    parquet_predicate_type, storage_options_dict_type, types.int64, types.
    voidptr, types.int32, types.voidptr, types.voidptr, types.voidptr,
    types.int32, types.voidptr, types.int32, types.voidptr, types.boolean))
from llvmlite import ir as lir
from numba.core import cgutils
if bodo.utils.utils.has_pyarrow():
    from bodo.io import arrow_cpp
    ll.add_symbol('pq_read', arrow_cpp.pq_read)
    ll.add_symbol('pq_write', arrow_cpp.pq_write)
    ll.add_symbol('pq_write_partitioned', arrow_cpp.pq_write_partitioned)


@intrinsic
def parquet_write_table_cpp(typingctx, filename_t, table_t, col_names_t,
    index_t, write_index, metadata_t, compression_t, is_parallel_t,
    write_range_index, start, stop, step, name, bucket_region,
    row_group_size, file_prefix, timestamp_tz):

    def codegen(context, builder, sig, args):
        jng__isawx = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        onizz__cqd = cgutils.get_or_insert_function(builder.module,
            jng__isawx, name='pq_write')
        kqmnq__xbter = builder.call(onizz__cqd, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return kqmnq__xbter
    return types.int64(types.voidptr, table_t, col_names_t, index_t, types.
        boolean, types.voidptr, types.voidptr, types.boolean, types.boolean,
        types.int32, types.int32, types.int32, types.voidptr, types.voidptr,
        types.int64, types.voidptr, types.voidptr), codegen


@intrinsic
def parquet_write_table_partitioned_cpp(typingctx, filename_t, data_table_t,
    col_names_t, col_names_no_partitions_t, cat_table_t, part_col_idxs_t,
    num_part_col_t, compression_t, is_parallel_t, bucket_region,
    row_group_size, file_prefix):

    def codegen(context, builder, sig, args):
        jng__isawx = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer()])
        onizz__cqd = cgutils.get_or_insert_function(builder.module,
            jng__isawx, name='pq_write_partitioned')
        builder.call(onizz__cqd, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr, types.int64, types.voidptr
        ), codegen
