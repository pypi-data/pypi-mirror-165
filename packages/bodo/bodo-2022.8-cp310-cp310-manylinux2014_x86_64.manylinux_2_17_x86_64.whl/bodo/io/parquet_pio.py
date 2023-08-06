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
        except OSError as sqsys__asnd:
            if 'non-file path' in str(sqsys__asnd):
                raise FileNotFoundError(str(sqsys__asnd))
            raise


class ParquetHandler:

    def __init__(self, func_ir, typingctx, args, _locals):
        self.func_ir = func_ir
        self.typingctx = typingctx
        self.args = args
        self.locals = _locals

    def gen_parquet_read(self, file_name, lhs, columns, storage_options=
        None, input_file_name_col=None, read_as_dict_cols=None):
        cfdc__tcd = lhs.scope
        zei__wzoh = lhs.loc
        bqm__zuonm = None
        if lhs.name in self.locals:
            bqm__zuonm = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        tcj__lbql = {}
        if lhs.name + ':convert' in self.locals:
            tcj__lbql = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if bqm__zuonm is None:
            vyky__fzj = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/file_io/#parquet-section.'
                )
            dcen__qzly = get_const_value(file_name, self.func_ir, vyky__fzj,
                arg_types=self.args, file_info=ParquetFileInfo(columns,
                storage_options=storage_options, input_file_name_col=
                input_file_name_col, read_as_dict_cols=read_as_dict_cols))
            ory__olcfk = False
            qbyo__qhtr = guard(get_definition, self.func_ir, file_name)
            if isinstance(qbyo__qhtr, ir.Arg):
                typ = self.args[qbyo__qhtr.index]
                if isinstance(typ, types.FilenameType):
                    (col_names, xhmke__fefp, vto__jpxze, col_indices,
                        partition_names, rte__uboly, kko__oih) = typ.schema
                    ory__olcfk = True
            if not ory__olcfk:
                (col_names, xhmke__fefp, vto__jpxze, col_indices,
                    partition_names, rte__uboly, kko__oih) = (
                    parquet_file_schema(dcen__qzly, columns,
                    storage_options=storage_options, input_file_name_col=
                    input_file_name_col, read_as_dict_cols=read_as_dict_cols))
        else:
            cpoeo__qelzu = list(bqm__zuonm.keys())
            nyc__wbwwk = {c: fydgh__vyet for fydgh__vyet, c in enumerate(
                cpoeo__qelzu)}
            elii__fyx = [zoajq__snrml for zoajq__snrml in bqm__zuonm.values()]
            vto__jpxze = 'index' if 'index' in nyc__wbwwk else None
            if columns is None:
                selected_columns = cpoeo__qelzu
            else:
                selected_columns = columns
            col_indices = [nyc__wbwwk[c] for c in selected_columns]
            xhmke__fefp = [elii__fyx[nyc__wbwwk[c]] for c in selected_columns]
            col_names = selected_columns
            vto__jpxze = vto__jpxze if vto__jpxze in col_names else None
            partition_names = []
            rte__uboly = []
            kko__oih = []
        xjpd__ktfcj = None if isinstance(vto__jpxze, dict
            ) or vto__jpxze is None else vto__jpxze
        index_column_index = None
        index_column_type = types.none
        if xjpd__ktfcj:
            eda__ywg = col_names.index(xjpd__ktfcj)
            index_column_index = col_indices.pop(eda__ywg)
            index_column_type = xhmke__fefp.pop(eda__ywg)
            col_names.pop(eda__ywg)
        for fydgh__vyet, c in enumerate(col_names):
            if c in tcj__lbql:
                xhmke__fefp[fydgh__vyet] = tcj__lbql[c]
        oeo__caa = [ir.Var(cfdc__tcd, mk_unique_var('pq_table'), zei__wzoh),
            ir.Var(cfdc__tcd, mk_unique_var('pq_index'), zei__wzoh)]
        kglx__urrr = [bodo.ir.parquet_ext.ParquetReader(file_name, lhs.name,
            col_names, col_indices, xhmke__fefp, oeo__caa, zei__wzoh,
            partition_names, storage_options, index_column_index,
            index_column_type, input_file_name_col, rte__uboly, kko__oih)]
        return (col_names, oeo__caa, vto__jpxze, kglx__urrr, xhmke__fefp,
            index_column_type)


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, meta_head_only_info=None):
    uqy__hcc = len(pq_node.out_vars)
    dnf_filter_str = 'None'
    expr_filter_str = 'None'
    rhm__xgcd, owkib__thmv = bodo.ir.connector.generate_filter_map(pq_node.
        filters)
    extra_args = ', '.join(rhm__xgcd.values())
    dnf_filter_str, expr_filter_str = bodo.ir.connector.generate_arrow_filters(
        pq_node.filters, rhm__xgcd, owkib__thmv, pq_node.
        original_df_colnames, pq_node.partition_names, pq_node.
        original_out_types, typemap, 'parquet', output_dnf=False)
    svg__vjnvn = ', '.join(f'out{fydgh__vyet}' for fydgh__vyet in range(
        uqy__hcc))
    rvwja__uteb = f'def pq_impl(fname, {extra_args}):\n'
    rvwja__uteb += (
        f'    (total_rows, {svg__vjnvn},) = _pq_reader_py(fname, {extra_args})\n'
        )
    snvwy__tyk = {}
    exec(rvwja__uteb, {}, snvwy__tyk)
    dee__itd = snvwy__tyk['pq_impl']
    if bodo.user_logging.get_verbose_level() >= 1:
        jhxcn__tiq = pq_node.loc.strformat()
        ovr__leeb = []
        pqlut__pkfa = []
        for fydgh__vyet in pq_node.out_used_cols:
            cwtxb__ydz = pq_node.df_colnames[fydgh__vyet]
            ovr__leeb.append(cwtxb__ydz)
            if isinstance(pq_node.out_types[fydgh__vyet], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                pqlut__pkfa.append(cwtxb__ydz)
        cxf__oucog = (
            'Finish column pruning on read_parquet node:\n%s\nColumns loaded %s\n'
            )
        bodo.user_logging.log_message('Column Pruning', cxf__oucog,
            jhxcn__tiq, ovr__leeb)
        if pqlut__pkfa:
            vue__lskz = """Finished optimized encoding on read_parquet node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', vue__lskz,
                jhxcn__tiq, pqlut__pkfa)
    parallel = bodo.ir.connector.is_connector_table_parallel(pq_node,
        array_dists, typemap, 'ParquetReader')
    if pq_node.unsupported_columns:
        aggiu__vkqu = set(pq_node.out_used_cols)
        ssh__oetr = set(pq_node.unsupported_columns)
        qyfd__amoa = aggiu__vkqu & ssh__oetr
        if qyfd__amoa:
            jylx__zzc = sorted(qyfd__amoa)
            txoe__enj = [
                f'pandas.read_parquet(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                "Please manually remove these columns from your read_parquet with the 'columns' argument. If these "
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            kuj__jqf = 0
            for pbs__axdxu in jylx__zzc:
                while pq_node.unsupported_columns[kuj__jqf] != pbs__axdxu:
                    kuj__jqf += 1
                txoe__enj.append(
                    f"Column '{pq_node.df_colnames[pbs__axdxu]}' with unsupported arrow type {pq_node.unsupported_arrow_types[kuj__jqf]}"
                    )
                kuj__jqf += 1
            ejq__xafyi = '\n'.join(txoe__enj)
            raise BodoError(ejq__xafyi, loc=pq_node.loc)
    rwsw__gaycc = _gen_pq_reader_py(pq_node.df_colnames, pq_node.
        col_indices, pq_node.out_used_cols, pq_node.out_types, pq_node.
        storage_options, pq_node.partition_names, dnf_filter_str,
        expr_filter_str, extra_args, parallel, meta_head_only_info, pq_node
        .index_column_index, pq_node.index_column_type, pq_node.
        input_file_name_col, not pq_node.is_live_table)
    pxnj__dfqv = typemap[pq_node.file_name.name]
    jngs__tdu = (pxnj__dfqv,) + tuple(typemap[lzlp__obji.name] for
        lzlp__obji in owkib__thmv)
    cqw__uyhp = compile_to_numba_ir(dee__itd, {'_pq_reader_py': rwsw__gaycc
        }, typingctx=typingctx, targetctx=targetctx, arg_typs=jngs__tdu,
        typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(cqw__uyhp, [pq_node.file_name] + owkib__thmv)
    kglx__urrr = cqw__uyhp.body[:-3]
    if meta_head_only_info:
        kglx__urrr[-3].target = meta_head_only_info[1]
    kglx__urrr[-2].target = pq_node.out_vars[0]
    kglx__urrr[-1].target = pq_node.out_vars[1]
    assert not (pq_node.index_column_index is None and not pq_node.
        is_live_table
        ), 'At most one of table and index should be dead if the Parquet IR node is live'
    if pq_node.index_column_index is None:
        kglx__urrr.pop(-1)
    elif not pq_node.is_live_table:
        kglx__urrr.pop(-2)
    return kglx__urrr


distributed_pass.distributed_run_extensions[bodo.ir.parquet_ext.ParquetReader
    ] = pq_distributed_run


def get_filters_pyobject(dnf_filter_str, expr_filter_str, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(dnf_filter_str, expr_filter_str, var_tup):
    vgo__lqz = get_overload_const_str(dnf_filter_str)
    jhqv__jhlfu = get_overload_const_str(expr_filter_str)
    qmlu__wkne = ', '.join(f'f{fydgh__vyet}' for fydgh__vyet in range(len(
        var_tup)))
    rvwja__uteb = 'def impl(dnf_filter_str, expr_filter_str, var_tup):\n'
    if len(var_tup):
        rvwja__uteb += f'  {qmlu__wkne}, = var_tup\n'
    rvwja__uteb += """  with numba.objmode(dnf_filters_py='parquet_predicate_type', expr_filters_py='parquet_predicate_type'):
"""
    rvwja__uteb += f'    dnf_filters_py = {vgo__lqz}\n'
    rvwja__uteb += f'    expr_filters_py = {jhqv__jhlfu}\n'
    rvwja__uteb += '  return (dnf_filters_py, expr_filters_py)\n'
    snvwy__tyk = {}
    exec(rvwja__uteb, globals(), snvwy__tyk)
    return snvwy__tyk['impl']


@numba.njit
def get_fname_pyobject(fname):
    with numba.objmode(fname_py='read_parquet_fpath_type'):
        fname_py = fname
    return fname_py


def _gen_pq_reader_py(col_names, col_indices, out_used_cols, out_types,
    storage_options, partition_names, dnf_filter_str, expr_filter_str,
    extra_args, is_parallel, meta_head_only_info, index_column_index,
    index_column_type, input_file_name_col, is_dead_table):
    zjual__lsd = next_label()
    rjlmu__bzv = ',' if extra_args else ''
    rvwja__uteb = f'def pq_reader_py(fname,{extra_args}):\n'
    rvwja__uteb += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    rvwja__uteb += f"    ev.add_attribute('g_fname', fname)\n"
    rvwja__uteb += f"""    dnf_filters, expr_filters = get_filters_pyobject("{dnf_filter_str}", "{expr_filter_str}", ({extra_args}{rjlmu__bzv}))
"""
    rvwja__uteb += '    fname_py = get_fname_pyobject(fname)\n'
    storage_options['bodo_dummy'] = 'dummy'
    rvwja__uteb += f"""    storage_options_py = get_storage_options_pyobject({str(storage_options)})
"""
    tot_rows_to_read = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        tot_rows_to_read = meta_head_only_info[0]
    xbb__grx = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    input_file_name_col = sanitize_varname(input_file_name_col
        ) if input_file_name_col is not None and col_names.index(
        input_file_name_col) in out_used_cols else None
    yaj__nzqie = {c: fydgh__vyet for fydgh__vyet, c in enumerate(col_indices)}
    yumqz__pxpwd = {c: fydgh__vyet for fydgh__vyet, c in enumerate(xbb__grx)}
    ajfj__ijnzk = []
    rmpi__hzss = set()
    ints__jia = partition_names + [input_file_name_col]
    for fydgh__vyet in out_used_cols:
        if xbb__grx[fydgh__vyet] not in ints__jia:
            ajfj__ijnzk.append(col_indices[fydgh__vyet])
        elif not input_file_name_col or xbb__grx[fydgh__vyet
            ] != input_file_name_col:
            rmpi__hzss.add(col_indices[fydgh__vyet])
    if index_column_index is not None:
        ajfj__ijnzk.append(index_column_index)
    ajfj__ijnzk = sorted(ajfj__ijnzk)
    eyro__jahj = {c: fydgh__vyet for fydgh__vyet, c in enumerate(ajfj__ijnzk)}
    vaal__hlh = [(int(is_nullable(out_types[yaj__nzqie[kcviq__pkoy]])) if 
        kcviq__pkoy != index_column_index else int(is_nullable(
        index_column_type))) for kcviq__pkoy in ajfj__ijnzk]
    str_as_dict_cols = []
    for kcviq__pkoy in ajfj__ijnzk:
        if kcviq__pkoy == index_column_index:
            zoajq__snrml = index_column_type
        else:
            zoajq__snrml = out_types[yaj__nzqie[kcviq__pkoy]]
        if zoajq__snrml == dict_str_arr_type:
            str_as_dict_cols.append(kcviq__pkoy)
    afm__mbrn = []
    qxml__egyx = {}
    rorr__dzaim = []
    ikovn__rnv = []
    for fydgh__vyet, kxzb__mzd in enumerate(partition_names):
        try:
            djbon__guc = yumqz__pxpwd[kxzb__mzd]
            if col_indices[djbon__guc] not in rmpi__hzss:
                continue
        except (KeyError, ValueError) as ijc__fsvf:
            continue
        qxml__egyx[kxzb__mzd] = len(afm__mbrn)
        afm__mbrn.append(kxzb__mzd)
        rorr__dzaim.append(fydgh__vyet)
        pcq__lzncd = out_types[djbon__guc].dtype
        sfx__gqv = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            pcq__lzncd)
        ikovn__rnv.append(numba_to_c_type(sfx__gqv))
    rvwja__uteb += f'    total_rows_np = np.array([0], dtype=np.int64)\n'
    rvwja__uteb += f'    out_table = pq_read(\n'
    rvwja__uteb += f'        fname_py, {is_parallel},\n'
    rvwja__uteb += f'        dnf_filters, expr_filters,\n'
    rvwja__uteb += f"""        storage_options_py, {tot_rows_to_read}, selected_cols_arr_{zjual__lsd}.ctypes,
"""
    rvwja__uteb += f'        {len(ajfj__ijnzk)},\n'
    rvwja__uteb += f'        nullable_cols_arr_{zjual__lsd}.ctypes,\n'
    if len(rorr__dzaim) > 0:
        rvwja__uteb += (
            f'        np.array({rorr__dzaim}, dtype=np.int32).ctypes,\n')
        rvwja__uteb += (
            f'        np.array({ikovn__rnv}, dtype=np.int32).ctypes,\n')
        rvwja__uteb += f'        {len(rorr__dzaim)},\n'
    else:
        rvwja__uteb += f'        0, 0, 0,\n'
    if len(str_as_dict_cols) > 0:
        rvwja__uteb += f"""        np.array({str_as_dict_cols}, dtype=np.int32).ctypes, {len(str_as_dict_cols)},
"""
    else:
        rvwja__uteb += f'        0, 0,\n'
    rvwja__uteb += f'        total_rows_np.ctypes,\n'
    rvwja__uteb += f'        {input_file_name_col is not None},\n'
    rvwja__uteb += f'    )\n'
    rvwja__uteb += f'    check_and_propagate_cpp_exception()\n'
    rvwja__uteb += f'    total_rows = total_rows_np[0]\n'
    if is_parallel:
        rvwja__uteb += f"""    local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
    else:
        rvwja__uteb += f'    local_rows = total_rows\n'
    bbku__dskq = index_column_type
    jwpw__dby = TableType(tuple(out_types))
    if is_dead_table:
        jwpw__dby = types.none
    if is_dead_table:
        fkc__stde = None
    else:
        fkc__stde = []
        gpd__uof = 0
        eljzu__tro = col_indices[col_names.index(input_file_name_col)
            ] if input_file_name_col is not None else None
        for fydgh__vyet, pbs__axdxu in enumerate(col_indices):
            if gpd__uof < len(out_used_cols) and fydgh__vyet == out_used_cols[
                gpd__uof]:
                tpdq__ynq = col_indices[fydgh__vyet]
                if eljzu__tro and tpdq__ynq == eljzu__tro:
                    fkc__stde.append(len(ajfj__ijnzk) + len(afm__mbrn))
                elif tpdq__ynq in rmpi__hzss:
                    nzde__eidd = xbb__grx[fydgh__vyet]
                    fkc__stde.append(len(ajfj__ijnzk) + qxml__egyx[nzde__eidd])
                else:
                    fkc__stde.append(eyro__jahj[pbs__axdxu])
                gpd__uof += 1
            else:
                fkc__stde.append(-1)
        fkc__stde = np.array(fkc__stde, dtype=np.int64)
    if is_dead_table:
        rvwja__uteb += '    T = None\n'
    else:
        rvwja__uteb += f"""    T = cpp_table_to_py_table(out_table, table_idx_{zjual__lsd}, py_table_type_{zjual__lsd})
"""
        if len(out_used_cols) == 0:
            rvwja__uteb += f'    T = set_table_len(T, local_rows)\n'
    if index_column_index is None:
        rvwja__uteb += '    index_arr = None\n'
    else:
        ogpop__ejbk = eyro__jahj[index_column_index]
        rvwja__uteb += f"""    index_arr = info_to_array(info_from_table(out_table, {ogpop__ejbk}), index_arr_type)
"""
    rvwja__uteb += f'    delete_table(out_table)\n'
    rvwja__uteb += f'    ev.finalize()\n'
    rvwja__uteb += f'    return (total_rows, T, index_arr)\n'
    snvwy__tyk = {}
    tnpxw__emvb = {f'py_table_type_{zjual__lsd}': jwpw__dby,
        f'table_idx_{zjual__lsd}': fkc__stde,
        f'selected_cols_arr_{zjual__lsd}': np.array(ajfj__ijnzk, np.int32),
        f'nullable_cols_arr_{zjual__lsd}': np.array(vaal__hlh, np.int32),
        'index_arr_type': bbku__dskq, 'cpp_table_to_py_table':
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
    exec(rvwja__uteb, tnpxw__emvb, snvwy__tyk)
    rwsw__gaycc = snvwy__tyk['pq_reader_py']
    qyelk__dalf = numba.njit(rwsw__gaycc, no_cpython_wrapper=True)
    return qyelk__dalf


def unify_schemas(schemas):
    vgiv__jsx = []
    for schema in schemas:
        for fydgh__vyet in range(len(schema)):
            xze__hrpk = schema.field(fydgh__vyet)
            if xze__hrpk.type == pa.large_string():
                schema = schema.set(fydgh__vyet, xze__hrpk.with_type(pa.
                    string()))
            elif xze__hrpk.type == pa.large_binary():
                schema = schema.set(fydgh__vyet, xze__hrpk.with_type(pa.
                    binary()))
            elif isinstance(xze__hrpk.type, (pa.ListType, pa.LargeListType)
                ) and xze__hrpk.type.value_type in (pa.string(), pa.
                large_string()):
                schema = schema.set(fydgh__vyet, xze__hrpk.with_type(pa.
                    list_(pa.field(xze__hrpk.type.value_field.name, pa.
                    string()))))
            elif isinstance(xze__hrpk.type, pa.LargeListType):
                schema = schema.set(fydgh__vyet, xze__hrpk.with_type(pa.
                    list_(pa.field(xze__hrpk.type.value_field.name,
                    xze__hrpk.type.value_type))))
        vgiv__jsx.append(schema)
    return pa.unify_schemas(vgiv__jsx)


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
        for fydgh__vyet in range(len(self.schema)):
            xze__hrpk = self.schema.field(fydgh__vyet)
            if xze__hrpk.type == pa.large_string():
                self.schema = self.schema.set(fydgh__vyet, xze__hrpk.
                    with_type(pa.string()))
        self.pieces = [ParquetPiece(frag, partitioning, self.
            partition_names) for frag in pa_pq_dataset._dataset.
            get_fragments(filter=pa_pq_dataset._filter_expression)]

    def set_fs(self, fs):
        self.filesystem = fs
        for vfon__azkus in self.pieces:
            vfon__azkus.filesystem = fs

    def __setstate__(self, state):
        self.__dict__ = state
        if self.partition_names:
            ttfy__bymjk = {vfon__azkus: self.partitioning_dictionaries[
                fydgh__vyet] for fydgh__vyet, vfon__azkus in enumerate(self
                .partition_names)}
            self.partitioning = self.partitioning_cls(self.
                partitioning_schema, ttfy__bymjk)


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
            self.partition_keys = [(kxzb__mzd, partitioning.dictionaries[
                fydgh__vyet].index(self.partition_keys[kxzb__mzd]).as_py()) for
                fydgh__vyet, kxzb__mzd in enumerate(partition_names)]

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
        yufv__nsr = tracing.Event('get_parquet_dataset')
    import time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    khv__tzmz = MPI.COMM_WORLD
    if isinstance(fpath, list):
        cmy__hfunw = urlparse(fpath[0])
        protocol = cmy__hfunw.scheme
        yeuwa__ynmg = cmy__hfunw.netloc
        for fydgh__vyet in range(len(fpath)):
            xze__hrpk = fpath[fydgh__vyet]
            nlosp__wqzoq = urlparse(xze__hrpk)
            if nlosp__wqzoq.scheme != protocol:
                raise BodoError(
                    'All parquet files must use the same filesystem protocol')
            if nlosp__wqzoq.netloc != yeuwa__ynmg:
                raise BodoError(
                    'All parquet files must be in the same S3 bucket')
            fpath[fydgh__vyet] = xze__hrpk.rstrip('/')
    else:
        cmy__hfunw = urlparse(fpath)
        protocol = cmy__hfunw.scheme
        fpath = fpath.rstrip('/')
    if protocol in {'gcs', 'gs'}:
        try:
            import gcsfs
        except ImportError as ijc__fsvf:
            bhidx__uefv = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(bhidx__uefv)
    if protocol == 'http':
        try:
            import fsspec
        except ImportError as ijc__fsvf:
            bhidx__uefv = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
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
            vbi__mumb = gcsfs.GCSFileSystem(token=None)
            fs.append(PyFileSystem(FSSpecHandler(vbi__mumb)))
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
            aan__qnequ = fs.glob(path)
        except:
            raise BodoError(
                f'glob pattern expansion not supported for {protocol}')
        if len(aan__qnequ) == 0:
            raise BodoError('No files found matching glob pattern')
        return aan__qnequ
    unk__jfa = False
    if get_row_counts:
        uhe__jhyqb = getfs(parallel=True)
        unk__jfa = bodo.parquet_validate_schema
    if bodo.get_rank() == 0:
        lth__yyaav = 1
        ugan__rol = os.cpu_count()
        if ugan__rol is not None and ugan__rol > 1:
            lth__yyaav = ugan__rol // 2
        try:
            if get_row_counts:
                hwggm__rydf = tracing.Event('pq.ParquetDataset',
                    is_parallel=False)
                if tracing.is_tracing():
                    hwggm__rydf.add_attribute('g_dnf_filter', str(dnf_filters))
            tbxxj__jwwo = pa.io_thread_count()
            pa.set_io_thread_count(lth__yyaav)
            prefix = ''
            if protocol == 's3':
                prefix = 's3://'
            elif protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{cmy__hfunw.netloc}'
            if prefix:
                if isinstance(fpath, list):
                    xook__idswz = [xze__hrpk[len(prefix):] for xze__hrpk in
                        fpath]
                else:
                    xook__idswz = fpath[len(prefix):]
            else:
                xook__idswz = fpath
            if isinstance(xook__idswz, list):
                ibr__zds = []
                for vfon__azkus in xook__idswz:
                    if has_magic(vfon__azkus):
                        ibr__zds += glob(protocol, getfs(), vfon__azkus)
                    else:
                        ibr__zds.append(vfon__azkus)
                xook__idswz = ibr__zds
            elif has_magic(xook__idswz):
                xook__idswz = glob(protocol, getfs(), xook__idswz)
            notjt__jlk = pq.ParquetDataset(xook__idswz, filesystem=getfs(),
                filters=None, use_legacy_dataset=False, partitioning=
                partitioning)
            if dnf_filters is not None:
                notjt__jlk._filters = dnf_filters
                notjt__jlk._filter_expression = pq._filters_to_expression(
                    dnf_filters)
            snsh__uafg = len(notjt__jlk.files)
            notjt__jlk = ParquetDataset(notjt__jlk, prefix)
            pa.set_io_thread_count(tbxxj__jwwo)
            if typing_pa_schema:
                notjt__jlk.schema = typing_pa_schema
            if get_row_counts:
                if dnf_filters is not None:
                    hwggm__rydf.add_attribute('num_pieces_before_filter',
                        snsh__uafg)
                    hwggm__rydf.add_attribute('num_pieces_after_filter',
                        len(notjt__jlk.pieces))
                hwggm__rydf.finalize()
        except Exception as sqsys__asnd:
            if isinstance(sqsys__asnd, IsADirectoryError):
                sqsys__asnd = BodoError(list_of_files_error_msg)
            elif isinstance(fpath, list) and isinstance(sqsys__asnd, (
                OSError, FileNotFoundError)):
                sqsys__asnd = BodoError(str(sqsys__asnd) +
                    list_of_files_error_msg)
            else:
                sqsys__asnd = BodoError(
                    f"""error from pyarrow: {type(sqsys__asnd).__name__}: {str(sqsys__asnd)}
"""
                    )
            khv__tzmz.bcast(sqsys__asnd)
            raise sqsys__asnd
        if get_row_counts:
            nbcle__gfmsy = tracing.Event('bcast dataset')
        notjt__jlk = khv__tzmz.bcast(notjt__jlk)
    else:
        if get_row_counts:
            nbcle__gfmsy = tracing.Event('bcast dataset')
        notjt__jlk = khv__tzmz.bcast(None)
        if isinstance(notjt__jlk, Exception):
            awcmb__jxj = notjt__jlk
            raise awcmb__jxj
    notjt__jlk.set_fs(getfs())
    if get_row_counts:
        nbcle__gfmsy.finalize()
    if get_row_counts and tot_rows_to_read == 0:
        get_row_counts = unk__jfa = False
    if get_row_counts or unk__jfa:
        if get_row_counts and tracing.is_tracing():
            cbh__qvqxj = tracing.Event('get_row_counts')
            cbh__qvqxj.add_attribute('g_num_pieces', len(notjt__jlk.pieces))
            cbh__qvqxj.add_attribute('g_expr_filters', str(expr_filters))
        beb__ubn = 0.0
        num_pieces = len(notjt__jlk.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        euthh__rkrzn = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        arsqk__atayg = 0
        rmdh__dzmm = 0
        jtzt__xcc = 0
        gdj__txde = True
        if expr_filters is not None:
            import random
            random.seed(37)
            zju__afotm = random.sample(notjt__jlk.pieces, k=len(notjt__jlk.
                pieces))
        else:
            zju__afotm = notjt__jlk.pieces
        fpaths = [vfon__azkus.path for vfon__azkus in zju__afotm[start:
            euthh__rkrzn]]
        lth__yyaav = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), 4)
        pa.set_io_thread_count(lth__yyaav)
        pa.set_cpu_count(lth__yyaav)
        awcmb__jxj = None
        try:
            wpb__skts = ds.dataset(fpaths, filesystem=notjt__jlk.filesystem,
                partitioning=notjt__jlk.partitioning)
            for mifc__fiu, frag in zip(zju__afotm[start:euthh__rkrzn],
                wpb__skts.get_fragments()):
                if unk__jfa:
                    iut__aoz = frag.metadata.schema.to_arrow_schema()
                    uhcxi__hss = set(iut__aoz.names)
                    xhqs__oxtp = set(notjt__jlk.schema.names) - set(notjt__jlk
                        .partition_names)
                    if xhqs__oxtp != uhcxi__hss:
                        edmov__vro = uhcxi__hss - xhqs__oxtp
                        wot__dmxam = xhqs__oxtp - uhcxi__hss
                        vyky__fzj = f'Schema in {mifc__fiu} was different.\n'
                        if edmov__vro:
                            vyky__fzj += f"""File contains column(s) {edmov__vro} not found in other files in the dataset.
"""
                        if wot__dmxam:
                            vyky__fzj += f"""File missing column(s) {wot__dmxam} found in other files in the dataset.
"""
                        raise BodoError(vyky__fzj)
                    try:
                        notjt__jlk.schema = unify_schemas([notjt__jlk.
                            schema, iut__aoz])
                    except Exception as sqsys__asnd:
                        vyky__fzj = (
                            f'Schema in {mifc__fiu} was different.\n' + str
                            (sqsys__asnd))
                        raise BodoError(vyky__fzj)
                agfcr__vcfkp = time.time()
                mdfld__pyo = frag.scanner(schema=wpb__skts.schema, filter=
                    expr_filters, use_threads=True).count_rows()
                beb__ubn += time.time() - agfcr__vcfkp
                mifc__fiu._bodo_num_rows = mdfld__pyo
                arsqk__atayg += mdfld__pyo
                rmdh__dzmm += frag.num_row_groups
                jtzt__xcc += sum(rdcf__voc.total_byte_size for rdcf__voc in
                    frag.row_groups)
        except Exception as sqsys__asnd:
            awcmb__jxj = sqsys__asnd
        if khv__tzmz.allreduce(awcmb__jxj is not None, op=MPI.LOR):
            for awcmb__jxj in khv__tzmz.allgather(awcmb__jxj):
                if awcmb__jxj:
                    if isinstance(fpath, list) and isinstance(awcmb__jxj, (
                        OSError, FileNotFoundError)):
                        raise BodoError(str(awcmb__jxj) +
                            list_of_files_error_msg)
                    raise awcmb__jxj
        if unk__jfa:
            gdj__txde = khv__tzmz.allreduce(gdj__txde, op=MPI.LAND)
            if not gdj__txde:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            notjt__jlk._bodo_total_rows = khv__tzmz.allreduce(arsqk__atayg,
                op=MPI.SUM)
            bwn__qku = khv__tzmz.allreduce(rmdh__dzmm, op=MPI.SUM)
            tvt__ban = khv__tzmz.allreduce(jtzt__xcc, op=MPI.SUM)
            fbant__owzj = np.array([vfon__azkus._bodo_num_rows for
                vfon__azkus in notjt__jlk.pieces])
            fbant__owzj = khv__tzmz.allreduce(fbant__owzj, op=MPI.SUM)
            for vfon__azkus, kuhvw__xml in zip(notjt__jlk.pieces, fbant__owzj):
                vfon__azkus._bodo_num_rows = kuhvw__xml
            if is_parallel and bodo.get_rank(
                ) == 0 and bwn__qku < bodo.get_size() and bwn__qku != 0:
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({bwn__qku}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()}). For more details, refer to
https://docs.bodo.ai/latest/file_io/#parquet-section.
"""
                    ))
            if bwn__qku == 0:
                hsgxd__yoegb = 0
            else:
                hsgxd__yoegb = tvt__ban // bwn__qku
            if (bodo.get_rank() == 0 and tvt__ban >= 20 * 1048576 and 
                hsgxd__yoegb < 1048576 and protocol in REMOTE_FILESYSTEMS):
                warnings.warn(BodoWarning(
                    f'Parquet average row group size is small ({hsgxd__yoegb} bytes) and can have negative impact on performance when reading from remote sources'
                    ))
            if tracing.is_tracing():
                cbh__qvqxj.add_attribute('g_total_num_row_groups', bwn__qku)
                cbh__qvqxj.add_attribute('total_scan_time', beb__ubn)
                nboe__jtrhm = np.array([vfon__azkus._bodo_num_rows for
                    vfon__azkus in notjt__jlk.pieces])
                kxzzf__nqh = np.percentile(nboe__jtrhm, [25, 50, 75])
                cbh__qvqxj.add_attribute('g_row_counts_min', nboe__jtrhm.min())
                cbh__qvqxj.add_attribute('g_row_counts_Q1', kxzzf__nqh[0])
                cbh__qvqxj.add_attribute('g_row_counts_median', kxzzf__nqh[1])
                cbh__qvqxj.add_attribute('g_row_counts_Q3', kxzzf__nqh[2])
                cbh__qvqxj.add_attribute('g_row_counts_max', nboe__jtrhm.max())
                cbh__qvqxj.add_attribute('g_row_counts_mean', nboe__jtrhm.
                    mean())
                cbh__qvqxj.add_attribute('g_row_counts_std', nboe__jtrhm.std())
                cbh__qvqxj.add_attribute('g_row_counts_sum', nboe__jtrhm.sum())
                cbh__qvqxj.finalize()
    if read_categories:
        _add_categories_to_pq_dataset(notjt__jlk)
    if get_row_counts:
        yufv__nsr.finalize()
    if unk__jfa and is_parallel:
        if tracing.is_tracing():
            qhl__nqza = tracing.Event('unify_schemas_across_ranks')
        awcmb__jxj = None
        try:
            notjt__jlk.schema = khv__tzmz.allreduce(notjt__jlk.schema, bodo
                .io.helpers.pa_schema_unify_mpi_op)
        except Exception as sqsys__asnd:
            awcmb__jxj = sqsys__asnd
        if tracing.is_tracing():
            qhl__nqza.finalize()
        if khv__tzmz.allreduce(awcmb__jxj is not None, op=MPI.LOR):
            for awcmb__jxj in khv__tzmz.allgather(awcmb__jxj):
                if awcmb__jxj:
                    vyky__fzj = (f'Schema in some files were different.\n' +
                        str(awcmb__jxj))
                    raise BodoError(vyky__fzj)
    return notjt__jlk


def get_scanner_batches(fpaths, expr_filters, selected_fields,
    avg_num_pieces, is_parallel, filesystem, str_as_dict_cols, start_offset,
    rows_to_read, partitioning, schema):
    import pyarrow as pa
    ugan__rol = os.cpu_count()
    if ugan__rol is None or ugan__rol == 0:
        ugan__rol = 2
    zplw__zyx = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), ugan__rol)
    rlueh__jrsn = min(int(os.environ.get('BODO_MAX_IO_THREADS', 16)), ugan__rol
        )
    if is_parallel and len(fpaths) > rlueh__jrsn and len(fpaths
        ) / avg_num_pieces >= 2.0:
        pa.set_io_thread_count(rlueh__jrsn)
        pa.set_cpu_count(rlueh__jrsn)
    else:
        pa.set_io_thread_count(zplw__zyx)
        pa.set_cpu_count(zplw__zyx)
    vekk__qwle = ds.ParquetFileFormat(dictionary_columns=str_as_dict_cols)
    qmec__chjoc = set(str_as_dict_cols)
    for fydgh__vyet, name in enumerate(schema.names):
        if name in qmec__chjoc:
            zxyec__xye = schema.field(fydgh__vyet)
            nvsv__ptpt = pa.field(name, pa.dictionary(pa.int32(),
                zxyec__xye.type), zxyec__xye.nullable)
            schema = schema.remove(fydgh__vyet).insert(fydgh__vyet, nvsv__ptpt)
    notjt__jlk = ds.dataset(fpaths, filesystem=filesystem, partitioning=
        partitioning, schema=schema, format=vekk__qwle)
    col_names = notjt__jlk.schema.names
    ujzgn__zzmb = [col_names[ukf__qauze] for ukf__qauze in selected_fields]
    pfx__dxj = len(fpaths) <= 3 or start_offset > 0 and len(fpaths) <= 10
    if pfx__dxj and expr_filters is None:
        vnie__nbung = []
        gcxxm__lzf = 0
        fnuux__gzote = 0
        for frag in notjt__jlk.get_fragments():
            hdc__wzbm = []
            for rdcf__voc in frag.row_groups:
                njkl__fiq = rdcf__voc.num_rows
                if start_offset < gcxxm__lzf + njkl__fiq:
                    if fnuux__gzote == 0:
                        iygkj__qixvj = start_offset - gcxxm__lzf
                        fhl__eznfq = min(njkl__fiq - iygkj__qixvj, rows_to_read
                            )
                    else:
                        fhl__eznfq = min(njkl__fiq, rows_to_read - fnuux__gzote
                            )
                    fnuux__gzote += fhl__eznfq
                    hdc__wzbm.append(rdcf__voc.id)
                gcxxm__lzf += njkl__fiq
                if fnuux__gzote == rows_to_read:
                    break
            vnie__nbung.append(frag.subset(row_group_ids=hdc__wzbm))
            if fnuux__gzote == rows_to_read:
                break
        notjt__jlk = ds.FileSystemDataset(vnie__nbung, notjt__jlk.schema,
            vekk__qwle, filesystem=notjt__jlk.filesystem)
        start_offset = iygkj__qixvj
    mgu__arzx = notjt__jlk.scanner(columns=ujzgn__zzmb, filter=expr_filters,
        use_threads=True).to_reader()
    return notjt__jlk, mgu__arzx, start_offset


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    pa_schema = pq_dataset.schema
    rvfw__csv = [c for c in pa_schema.names if isinstance(pa_schema.field(c
        ).type, pa.DictionaryType) and c not in pq_dataset.partition_names]
    if len(rvfw__csv) == 0:
        pq_dataset._category_info = {}
        return
    khv__tzmz = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            mquvv__bqras = pq_dataset.pieces[0].frag.head(100, columns=
                rvfw__csv)
            ryn__eqxht = {c: tuple(mquvv__bqras.column(c).chunk(0).
                dictionary.to_pylist()) for c in rvfw__csv}
            del mquvv__bqras
        except Exception as sqsys__asnd:
            khv__tzmz.bcast(sqsys__asnd)
            raise sqsys__asnd
        khv__tzmz.bcast(ryn__eqxht)
    else:
        ryn__eqxht = khv__tzmz.bcast(None)
        if isinstance(ryn__eqxht, Exception):
            awcmb__jxj = ryn__eqxht
            raise awcmb__jxj
    pq_dataset._category_info = ryn__eqxht


def get_pandas_metadata(schema, num_pieces):
    vto__jpxze = None
    yepst__ckle = defaultdict(lambda : None)
    xrgox__okh = b'pandas'
    if schema.metadata is not None and xrgox__okh in schema.metadata:
        import json
        nhmkv__fdrt = json.loads(schema.metadata[xrgox__okh].decode('utf8'))
        crbm__wyjz = len(nhmkv__fdrt['index_columns'])
        if crbm__wyjz > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        vto__jpxze = nhmkv__fdrt['index_columns'][0] if crbm__wyjz else None
        if not isinstance(vto__jpxze, str) and not isinstance(vto__jpxze, dict
            ):
            vto__jpxze = None
        for tinpr__fedg in nhmkv__fdrt['columns']:
            yqguu__hwcj = tinpr__fedg['name']
            if tinpr__fedg['pandas_type'].startswith('int'
                ) and yqguu__hwcj is not None:
                if tinpr__fedg['numpy_type'].startswith('Int'):
                    yepst__ckle[yqguu__hwcj] = True
                else:
                    yepst__ckle[yqguu__hwcj] = False
    return vto__jpxze, yepst__ckle


def get_str_columns_from_pa_schema(pa_schema):
    str_columns = []
    for yqguu__hwcj in pa_schema.names:
        qkyun__tahp = pa_schema.field(yqguu__hwcj)
        if qkyun__tahp.type in (pa.string(), pa.large_string()):
            str_columns.append(yqguu__hwcj)
    return str_columns


def determine_str_as_dict_columns(pq_dataset, pa_schema, str_columns):
    from mpi4py import MPI
    khv__tzmz = MPI.COMM_WORLD
    if len(str_columns) == 0:
        return set()
    if len(pq_dataset.pieces) > bodo.get_size():
        import random
        random.seed(37)
        zju__afotm = random.sample(pq_dataset.pieces, bodo.get_size())
    else:
        zju__afotm = pq_dataset.pieces
    afh__vxdf = np.zeros(len(str_columns), dtype=np.int64)
    ejdw__ktfkp = np.zeros(len(str_columns), dtype=np.int64)
    if bodo.get_rank() < len(zju__afotm):
        mifc__fiu = zju__afotm[bodo.get_rank()]
        try:
            metadata = mifc__fiu.metadata
            for fydgh__vyet in range(mifc__fiu.num_row_groups):
                for gpd__uof, yqguu__hwcj in enumerate(str_columns):
                    kuj__jqf = pa_schema.get_field_index(yqguu__hwcj)
                    afh__vxdf[gpd__uof] += metadata.row_group(fydgh__vyet
                        ).column(kuj__jqf).total_uncompressed_size
            emy__ulz = metadata.num_rows
        except Exception as sqsys__asnd:
            if isinstance(sqsys__asnd, (OSError, FileNotFoundError)):
                emy__ulz = 0
            else:
                raise
    else:
        emy__ulz = 0
    ita__xgqf = khv__tzmz.allreduce(emy__ulz, op=MPI.SUM)
    if ita__xgqf == 0:
        return set()
    khv__tzmz.Allreduce(afh__vxdf, ejdw__ktfkp, op=MPI.SUM)
    oyen__siy = ejdw__ktfkp / ita__xgqf
    poq__vwnor = set()
    for fydgh__vyet, sjf__dtwdn in enumerate(oyen__siy):
        if sjf__dtwdn < READ_STR_AS_DICT_THRESHOLD:
            yqguu__hwcj = str_columns[fydgh__vyet][0]
            poq__vwnor.add(yqguu__hwcj)
    return poq__vwnor


def parquet_file_schema(file_name, selected_columns, storage_options=None,
    input_file_name_col=None, read_as_dict_cols=None):
    col_names = []
    xhmke__fefp = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True)
    partition_names = pq_dataset.partition_names
    pa_schema = pq_dataset.schema
    num_pieces = len(pq_dataset.pieces)
    str_columns = get_str_columns_from_pa_schema(pa_schema)
    vmn__exv = set(str_columns)
    if read_as_dict_cols is None:
        read_as_dict_cols = []
    read_as_dict_cols = set(read_as_dict_cols)
    okm__yev = read_as_dict_cols - vmn__exv
    if len(okm__yev) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {okm__yev}'
                , bodo.utils.typing.BodoWarning)
    read_as_dict_cols.intersection_update(vmn__exv)
    vmn__exv = vmn__exv - read_as_dict_cols
    str_columns = [qqx__mzqq for qqx__mzqq in str_columns if qqx__mzqq in
        vmn__exv]
    poq__vwnor: set = determine_str_as_dict_columns(pq_dataset, pa_schema,
        str_columns)
    poq__vwnor.update(read_as_dict_cols)
    col_names = pa_schema.names
    vto__jpxze, yepst__ckle = get_pandas_metadata(pa_schema, num_pieces)
    elii__fyx = []
    rrev__qgon = []
    nnl__ubjt = []
    for fydgh__vyet, c in enumerate(col_names):
        if c in partition_names:
            continue
        qkyun__tahp = pa_schema.field(c)
        rdq__udc, lagr__xjqd = _get_numba_typ_from_pa_typ(qkyun__tahp, c ==
            vto__jpxze, yepst__ckle[c], pq_dataset._category_info,
            str_as_dict=c in poq__vwnor)
        elii__fyx.append(rdq__udc)
        rrev__qgon.append(lagr__xjqd)
        nnl__ubjt.append(qkyun__tahp.type)
    if partition_names:
        elii__fyx += [_get_partition_cat_dtype(pq_dataset.
            partitioning_dictionaries[fydgh__vyet]) for fydgh__vyet in
            range(len(partition_names))]
        rrev__qgon.extend([True] * len(partition_names))
        nnl__ubjt.extend([None] * len(partition_names))
    if input_file_name_col is not None:
        col_names += [input_file_name_col]
        elii__fyx += [dict_str_arr_type]
        rrev__qgon.append(True)
        nnl__ubjt.append(None)
    rkj__evf = {c: fydgh__vyet for fydgh__vyet, c in enumerate(col_names)}
    if selected_columns is None:
        selected_columns = col_names
    for c in selected_columns:
        if c not in rkj__evf:
            raise BodoError(f'Selected column {c} not in Parquet file schema')
    if vto__jpxze and not isinstance(vto__jpxze, dict
        ) and vto__jpxze not in selected_columns:
        selected_columns.append(vto__jpxze)
    col_names = selected_columns
    col_indices = []
    xhmke__fefp = []
    rte__uboly = []
    kko__oih = []
    for fydgh__vyet, c in enumerate(col_names):
        tpdq__ynq = rkj__evf[c]
        col_indices.append(tpdq__ynq)
        xhmke__fefp.append(elii__fyx[tpdq__ynq])
        if not rrev__qgon[tpdq__ynq]:
            rte__uboly.append(fydgh__vyet)
            kko__oih.append(nnl__ubjt[tpdq__ynq])
    return (col_names, xhmke__fefp, vto__jpxze, col_indices,
        partition_names, rte__uboly, kko__oih)


def _get_partition_cat_dtype(dictionary):
    assert dictionary is not None
    xjxhe__jtz = dictionary.to_pandas()
    qnxd__mwzt = bodo.typeof(xjxhe__jtz).dtype
    if isinstance(qnxd__mwzt, types.Integer):
        rzgdx__wsru = PDCategoricalDtype(tuple(xjxhe__jtz), qnxd__mwzt, 
            False, int_type=qnxd__mwzt)
    else:
        rzgdx__wsru = PDCategoricalDtype(tuple(xjxhe__jtz), qnxd__mwzt, False)
    return CategoricalArrayType(rzgdx__wsru)


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
        wlgvw__wtndl = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        tns__suudg = cgutils.get_or_insert_function(builder.module,
            wlgvw__wtndl, name='pq_write')
        xfpm__cij = builder.call(tns__suudg, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return xfpm__cij
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
        wlgvw__wtndl = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer()])
        tns__suudg = cgutils.get_or_insert_function(builder.module,
            wlgvw__wtndl, name='pq_write_partitioned')
        builder.call(tns__suudg, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr, types.int64, types.voidptr
        ), codegen
