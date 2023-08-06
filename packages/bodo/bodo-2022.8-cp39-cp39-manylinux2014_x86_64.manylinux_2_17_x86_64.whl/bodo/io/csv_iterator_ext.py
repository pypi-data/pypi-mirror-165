"""
Class information for DataFrame iterators returned by pd.read_csv. This is used
to handle situations in which pd.read_csv is used to return chunks with separate
read calls instead of just a single read.
"""
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir_utils, types
from numba.core.imputils import RefType, impl_ret_borrowed, iternext_impl
from numba.core.typing.templates import signature
from numba.extending import intrinsic, lower_builtin, models, register_model
import bodo
import bodo.ir.connector
import bodo.ir.csv_ext
from bodo import objmode
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.table import Table, TableType
from bodo.io import csv_cpp
from bodo.ir.csv_ext import _gen_read_csv_objmode, astype
from bodo.utils.typing import ColNamesMetaType
from bodo.utils.utils import check_java_installation
from bodo.utils.utils import sanitize_varname
ll.add_symbol('update_csv_reader', csv_cpp.update_csv_reader)
ll.add_symbol('initialize_csv_reader', csv_cpp.initialize_csv_reader)


class CSVIteratorType(types.SimpleIteratorType):

    def __init__(self, df_type, out_colnames, out_types, usecols, sep,
        index_ind, index_arr_typ, index_name, escapechar, storage_options):
        assert isinstance(df_type, DataFrameType
            ), 'CSVIterator must return a DataFrame'
        jwmj__mdfo = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind}, {index_arr_typ}, {index_name}, {escapechar})'
            )
        super(types.SimpleIteratorType, self).__init__(jwmj__mdfo)
        self._yield_type = df_type
        self._out_colnames = out_colnames
        self._out_types = out_types
        self._usecols = usecols
        self._sep = sep
        self._index_ind = index_ind
        self._index_arr_typ = index_arr_typ
        self._index_name = index_name
        self._escapechar = escapechar
        self._storage_options = storage_options

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(CSVIteratorType)
class CSVIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nlmy__ack = [('csv_reader', types.stream_reader_type), ('index',
            types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, nlmy__ack)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    vsp__qwt = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    qly__lepe = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer()])
    uir__lvmhw = cgutils.get_or_insert_function(builder.module, qly__lepe,
        name='initialize_csv_reader')
    xgyld__gob = cgutils.create_struct_proxy(types.stream_reader_type)(context,
        builder, value=vsp__qwt.csv_reader)
    builder.call(uir__lvmhw, [xgyld__gob.pyobj])
    builder.store(context.get_constant(types.uint64, 0), vsp__qwt.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [kdlth__wmtl] = sig.args
    [xpivy__osobh] = args
    vsp__qwt = cgutils.create_struct_proxy(kdlth__wmtl)(context, builder,
        value=xpivy__osobh)
    qly__lepe = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer()])
    uir__lvmhw = cgutils.get_or_insert_function(builder.module, qly__lepe,
        name='update_csv_reader')
    xgyld__gob = cgutils.create_struct_proxy(types.stream_reader_type)(context,
        builder, value=vsp__qwt.csv_reader)
    ncc__lopb = builder.call(uir__lvmhw, [xgyld__gob.pyobj])
    result.set_valid(ncc__lopb)
    with builder.if_then(ncc__lopb):
        ftlsg__tqq = builder.load(vsp__qwt.index)
        joup__gyslh = types.Tuple([sig.return_type.first_type, types.int64])
        wjx__iwj = gen_read_csv_objmode(sig.args[0])
        nacri__bco = signature(joup__gyslh, types.stream_reader_type, types
            .int64)
        gixp__rifg = context.compile_internal(builder, wjx__iwj, nacri__bco,
            [vsp__qwt.csv_reader, ftlsg__tqq])
        iursa__knnpk, dkwee__gnt = cgutils.unpack_tuple(builder, gixp__rifg)
        lcd__wcjrb = builder.add(ftlsg__tqq, dkwee__gnt, flags=['nsw'])
        builder.store(lcd__wcjrb, vsp__qwt.index)
        result.yield_(iursa__knnpk)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        jbqc__tsiaa = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        context.nrt.incref(builder, signature.args[0], args[0])
        jbqc__tsiaa.csv_reader = args[0]
        yygu__qwn = context.get_constant(types.uintp, 0)
        jbqc__tsiaa.index = cgutils.alloca_once_value(builder, yygu__qwn)
        return jbqc__tsiaa._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    wkl__qtl = csv_iterator_typeref.instance_type
    sig = signature(wkl__qtl, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    zezrz__nan = 'def read_csv_objmode(f_reader):\n'
    lzts__wiwmq = [sanitize_varname(ptpzq__afvqp) for ptpzq__afvqp in
        csv_iterator_type._out_colnames]
    snol__nrajy = ir_utils.next_label()
    tlht__eyvp = globals()
    out_types = csv_iterator_type._out_types
    tlht__eyvp[f'table_type_{snol__nrajy}'] = TableType(tuple(out_types))
    tlht__eyvp[f'idx_array_typ'] = csv_iterator_type._index_arr_typ
    fshr__cip = list(range(len(csv_iterator_type._usecols)))
    zezrz__nan += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        lzts__wiwmq, out_types, csv_iterator_type._usecols, fshr__cip,
        csv_iterator_type._sep, csv_iterator_type._escapechar,
        csv_iterator_type._storage_options, snol__nrajy, tlht__eyvp,
        parallel=False, check_parallel_runtime=True, idx_col_index=
        csv_iterator_type._index_ind, idx_col_typ=csv_iterator_type.
        _index_arr_typ)
    byo__ohwr = bodo.ir.csv_ext._gen_parallel_flag_name(lzts__wiwmq)
    cot__zuond = ['T'] + (['idx_arr'] if csv_iterator_type._index_ind is not
        None else []) + [byo__ohwr]
    zezrz__nan += f"  return {', '.join(cot__zuond)}"
    tlht__eyvp = globals()
    fkhg__nxbpc = {}
    exec(zezrz__nan, tlht__eyvp, fkhg__nxbpc)
    moxno__xkol = fkhg__nxbpc['read_csv_objmode']
    ffra__evfay = numba.njit(moxno__xkol)
    bodo.ir.csv_ext.compiled_funcs.append(ffra__evfay)
    dxaa__wdpnj = 'def read_func(reader, local_start):\n'
    dxaa__wdpnj += f"  {', '.join(cot__zuond)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind is None:
        dxaa__wdpnj += f'  local_len = len(T)\n'
        dxaa__wdpnj += '  total_size = local_len\n'
        dxaa__wdpnj += f'  if ({byo__ohwr}):\n'
        dxaa__wdpnj += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        dxaa__wdpnj += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        hvoxa__hxqx = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
    else:
        dxaa__wdpnj += '  total_size = 0\n'
        hvoxa__hxqx = (
            f'bodo.utils.conversion.convert_to_index({cot__zuond[1]}, {csv_iterator_type._index_name!r})'
            )
    dxaa__wdpnj += f"""  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({cot__zuond[0]},), {hvoxa__hxqx}, __col_name_meta_value_read_csv_objmode), total_size)
"""
    exec(dxaa__wdpnj, {'bodo': bodo, 'objmode_func': ffra__evfay, '_op': np
        .int32(bodo.libs.distributed_api.Reduce_Type.Sum.value),
        '__col_name_meta_value_read_csv_objmode': ColNamesMetaType(
        csv_iterator_type.yield_type.columns)}, fkhg__nxbpc)
    return fkhg__nxbpc['read_func']
