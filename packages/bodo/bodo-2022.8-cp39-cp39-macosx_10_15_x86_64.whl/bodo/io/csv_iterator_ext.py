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
        utjx__gsasw = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind}, {index_arr_typ}, {index_name}, {escapechar})'
            )
        super(types.SimpleIteratorType, self).__init__(utjx__gsasw)
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
        lykoe__wyxvz = [('csv_reader', types.stream_reader_type), ('index',
            types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, lykoe__wyxvz)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    jgzv__rtnp = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    jox__rdr = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer()])
    ihvz__rdzf = cgutils.get_or_insert_function(builder.module, jox__rdr,
        name='initialize_csv_reader')
    peetx__tnrxy = cgutils.create_struct_proxy(types.stream_reader_type)(
        context, builder, value=jgzv__rtnp.csv_reader)
    builder.call(ihvz__rdzf, [peetx__tnrxy.pyobj])
    builder.store(context.get_constant(types.uint64, 0), jgzv__rtnp.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [ikx__tlfx] = sig.args
    [oqww__vnyjv] = args
    jgzv__rtnp = cgutils.create_struct_proxy(ikx__tlfx)(context, builder,
        value=oqww__vnyjv)
    jox__rdr = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer()])
    ihvz__rdzf = cgutils.get_or_insert_function(builder.module, jox__rdr,
        name='update_csv_reader')
    peetx__tnrxy = cgutils.create_struct_proxy(types.stream_reader_type)(
        context, builder, value=jgzv__rtnp.csv_reader)
    lsk__wxnfi = builder.call(ihvz__rdzf, [peetx__tnrxy.pyobj])
    result.set_valid(lsk__wxnfi)
    with builder.if_then(lsk__wxnfi):
        nlbdr__dtcqd = builder.load(jgzv__rtnp.index)
        nhz__tfusx = types.Tuple([sig.return_type.first_type, types.int64])
        werl__wfj = gen_read_csv_objmode(sig.args[0])
        hpy__ruz = signature(nhz__tfusx, types.stream_reader_type, types.int64)
        ykwc__vsy = context.compile_internal(builder, werl__wfj, hpy__ruz,
            [jgzv__rtnp.csv_reader, nlbdr__dtcqd])
        gip__fiv, txmdb__zayp = cgutils.unpack_tuple(builder, ykwc__vsy)
        xzpul__ozxzv = builder.add(nlbdr__dtcqd, txmdb__zayp, flags=['nsw'])
        builder.store(xzpul__ozxzv, jgzv__rtnp.index)
        result.yield_(gip__fiv)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        eznkm__bxci = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        context.nrt.incref(builder, signature.args[0], args[0])
        eznkm__bxci.csv_reader = args[0]
        xai__iwef = context.get_constant(types.uintp, 0)
        eznkm__bxci.index = cgutils.alloca_once_value(builder, xai__iwef)
        return eznkm__bxci._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    hggd__wdht = csv_iterator_typeref.instance_type
    sig = signature(hggd__wdht, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    povts__qbofg = 'def read_csv_objmode(f_reader):\n'
    hikcq__qyzf = [sanitize_varname(dmbm__pvk) for dmbm__pvk in
        csv_iterator_type._out_colnames]
    qqj__kyjsy = ir_utils.next_label()
    uejs__kuy = globals()
    out_types = csv_iterator_type._out_types
    uejs__kuy[f'table_type_{qqj__kyjsy}'] = TableType(tuple(out_types))
    uejs__kuy[f'idx_array_typ'] = csv_iterator_type._index_arr_typ
    mqrjm__hfpzj = list(range(len(csv_iterator_type._usecols)))
    povts__qbofg += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        hikcq__qyzf, out_types, csv_iterator_type._usecols, mqrjm__hfpzj,
        csv_iterator_type._sep, csv_iterator_type._escapechar,
        csv_iterator_type._storage_options, qqj__kyjsy, uejs__kuy, parallel
        =False, check_parallel_runtime=True, idx_col_index=
        csv_iterator_type._index_ind, idx_col_typ=csv_iterator_type.
        _index_arr_typ)
    uomm__aid = bodo.ir.csv_ext._gen_parallel_flag_name(hikcq__qyzf)
    xrisw__pra = ['T'] + (['idx_arr'] if csv_iterator_type._index_ind is not
        None else []) + [uomm__aid]
    povts__qbofg += f"  return {', '.join(xrisw__pra)}"
    uejs__kuy = globals()
    yhyb__fjl = {}
    exec(povts__qbofg, uejs__kuy, yhyb__fjl)
    qyir__znfn = yhyb__fjl['read_csv_objmode']
    csg__ojiq = numba.njit(qyir__znfn)
    bodo.ir.csv_ext.compiled_funcs.append(csg__ojiq)
    qylev__onxtn = 'def read_func(reader, local_start):\n'
    qylev__onxtn += f"  {', '.join(xrisw__pra)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind is None:
        qylev__onxtn += f'  local_len = len(T)\n'
        qylev__onxtn += '  total_size = local_len\n'
        qylev__onxtn += f'  if ({uomm__aid}):\n'
        qylev__onxtn += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        qylev__onxtn += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        vqeh__wfq = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
    else:
        qylev__onxtn += '  total_size = 0\n'
        vqeh__wfq = (
            f'bodo.utils.conversion.convert_to_index({xrisw__pra[1]}, {csv_iterator_type._index_name!r})'
            )
    qylev__onxtn += f"""  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({xrisw__pra[0]},), {vqeh__wfq}, __col_name_meta_value_read_csv_objmode), total_size)
"""
    exec(qylev__onxtn, {'bodo': bodo, 'objmode_func': csg__ojiq, '_op': np.
        int32(bodo.libs.distributed_api.Reduce_Type.Sum.value),
        '__col_name_meta_value_read_csv_objmode': ColNamesMetaType(
        csv_iterator_type.yield_type.columns)}, yhyb__fjl)
    return yhyb__fjl['read_func']
