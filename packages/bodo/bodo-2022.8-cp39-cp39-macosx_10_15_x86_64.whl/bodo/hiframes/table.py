"""Table data type for storing dataframe column arrays. Supports storing many columns
(e.g. >10k) efficiently.
"""
import operator
from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.ir_utils import guard
from numba.core.typing.templates import signature
from numba.cpython.listobj import ListInstance
from numba.extending import NativeValue, box, infer_getattr, intrinsic, lower_builtin, lower_getattr, make_attribute_wrapper, models, overload, register_model, typeof_impl, unbox
from numba.np.arrayobj import _getitem_array_single_int
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.typing import BodoError, MetaType, decode_if_dict_array, get_overload_const_int, is_list_like_index_type, is_overload_constant_bool, is_overload_constant_int, is_overload_none, is_overload_true, raise_bodo_error, to_str_arr_if_dict_array, unwrap_typeref
from bodo.utils.utils import is_whole_slice


class Table:

    def __init__(self, arrs, usecols=None, num_arrs=-1):
        if usecols is not None:
            assert num_arrs != -1, 'num_arrs must be provided if usecols is not None'
            ubhmx__vic = 0
            acj__xdcs = []
            for i in range(usecols[-1] + 1):
                if i == usecols[ubhmx__vic]:
                    acj__xdcs.append(arrs[ubhmx__vic])
                    ubhmx__vic += 1
                else:
                    acj__xdcs.append(None)
            for sxrh__mex in range(usecols[-1] + 1, num_arrs):
                acj__xdcs.append(None)
            self.arrays = acj__xdcs
        else:
            self.arrays = arrs
        self.block_0 = arrs

    def __eq__(self, other):
        return isinstance(other, Table) and len(self.arrays) == len(other.
            arrays) and all((xrog__qjit == abh__nipww).all() for xrog__qjit,
            abh__nipww in zip(self.arrays, other.arrays))

    def __str__(self) ->str:
        return str(self.arrays)

    def to_pandas(self, index=None):
        jat__lakik = len(self.arrays)
        ylvl__tsg = dict(zip(range(jat__lakik), self.arrays))
        df = pd.DataFrame(ylvl__tsg, index)
        return df


class TableType(types.ArrayCompatible):

    def __init__(self, arr_types, has_runtime_cols=False):
        self.arr_types = arr_types
        self.has_runtime_cols = has_runtime_cols
        lcl__nlvyl = []
        ybc__jevf = []
        lwov__qabrf = {}
        twc__pbzpp = {}
        wuf__ehcij = defaultdict(int)
        lbsvh__vtpq = defaultdict(list)
        if not has_runtime_cols:
            for i, t in enumerate(arr_types):
                if t not in lwov__qabrf:
                    cwe__fab = len(lwov__qabrf)
                    lwov__qabrf[t] = cwe__fab
                    twc__pbzpp[cwe__fab] = t
                jlqi__jitai = lwov__qabrf[t]
                lcl__nlvyl.append(jlqi__jitai)
                ybc__jevf.append(wuf__ehcij[jlqi__jitai])
                wuf__ehcij[jlqi__jitai] += 1
                lbsvh__vtpq[jlqi__jitai].append(i)
        self.block_nums = lcl__nlvyl
        self.block_offsets = ybc__jevf
        self.type_to_blk = lwov__qabrf
        self.blk_to_type = twc__pbzpp
        self.block_to_arr_ind = lbsvh__vtpq
        super(TableType, self).__init__(name=
            f'TableType({arr_types}, {has_runtime_cols})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    @property
    def key(self):
        return self.arr_types, self.has_runtime_cols

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(Table)
def typeof_table(val, c):
    return TableType(tuple(numba.typeof(arr) for arr in val.arrays))


@register_model(TableType)
class TableTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        if fe_type.has_runtime_cols:
            zhn__nojrt = [(f'block_{i}', types.List(t)) for i, t in
                enumerate(fe_type.arr_types)]
        else:
            zhn__nojrt = [(f'block_{jlqi__jitai}', types.List(t)) for t,
                jlqi__jitai in fe_type.type_to_blk.items()]
        zhn__nojrt.append(('parent', types.pyobject))
        zhn__nojrt.append(('len', types.int64))
        super(TableTypeModel, self).__init__(dmm, fe_type, zhn__nojrt)


make_attribute_wrapper(TableType, 'block_0', 'block_0')
make_attribute_wrapper(TableType, 'len', '_len')


@infer_getattr
class TableTypeAttribute(OverloadedKeyAttributeTemplate):
    key = TableType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])


@unbox(TableType)
def unbox_table(typ, val, c):
    ygrnz__piu = c.pyapi.object_getattr_string(val, 'arrays')
    table = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    table.parent = cgutils.get_null_value(table.parent.type)
    zyv__fsuyd = c.pyapi.make_none()
    tqtq__hgofx = c.context.get_constant(types.int64, 0)
    eio__stwyd = cgutils.alloca_once_value(c.builder, tqtq__hgofx)
    for t, jlqi__jitai in typ.type_to_blk.items():
        shhp__uyh = c.context.get_constant(types.int64, len(typ.
            block_to_arr_ind[jlqi__jitai]))
        sxrh__mex, qte__swp = ListInstance.allocate_ex(c.context, c.builder,
            types.List(t), shhp__uyh)
        qte__swp.size = shhp__uyh
        mpmzj__nmtjr = c.context.make_constant_array(c.builder, types.Array
            (types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[
            jlqi__jitai], dtype=np.int64))
        jyut__ysfdi = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, mpmzj__nmtjr)
        with cgutils.for_range(c.builder, shhp__uyh) as zbij__ztd:
            i = zbij__ztd.index
            clxqt__vopi = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), jyut__ysfdi, i)
            das__rgua = c.pyapi.long_from_longlong(clxqt__vopi)
            kbv__mriq = c.pyapi.object_getitem(ygrnz__piu, das__rgua)
            taa__eosz = c.builder.icmp_unsigned('==', kbv__mriq, zyv__fsuyd)
            with c.builder.if_else(taa__eosz) as (yuun__nyiqs, dfpv__gryuy):
                with yuun__nyiqs:
                    lww__wkczr = c.context.get_constant_null(t)
                    qte__swp.inititem(i, lww__wkczr, incref=False)
                with dfpv__gryuy:
                    hjmue__exeu = c.pyapi.call_method(kbv__mriq, '__len__', ())
                    njx__cqj = c.pyapi.long_as_longlong(hjmue__exeu)
                    c.builder.store(njx__cqj, eio__stwyd)
                    c.pyapi.decref(hjmue__exeu)
                    arr = c.pyapi.to_native_value(t, kbv__mriq).value
                    qte__swp.inititem(i, arr, incref=False)
            c.pyapi.decref(kbv__mriq)
            c.pyapi.decref(das__rgua)
        setattr(table, f'block_{jlqi__jitai}', qte__swp.value)
    table.len = c.builder.load(eio__stwyd)
    c.pyapi.decref(ygrnz__piu)
    c.pyapi.decref(zyv__fsuyd)
    fshso__mpket = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(table._getvalue(), is_error=fshso__mpket)


@box(TableType)
def box_table(typ, val, c, ensure_unboxed=None):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    table = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ.has_runtime_cols:
        dthy__uxiu = c.context.get_constant(types.int64, 0)
        for i, t in enumerate(typ.arr_types):
            acj__xdcs = getattr(table, f'block_{i}')
            qfd__kvosh = ListInstance(c.context, c.builder, types.List(t),
                acj__xdcs)
            dthy__uxiu = c.builder.add(dthy__uxiu, qfd__kvosh.size)
        spt__ovkec = c.pyapi.list_new(dthy__uxiu)
        oqv__djrrt = c.context.get_constant(types.int64, 0)
        for i, t in enumerate(typ.arr_types):
            acj__xdcs = getattr(table, f'block_{i}')
            qfd__kvosh = ListInstance(c.context, c.builder, types.List(t),
                acj__xdcs)
            with cgutils.for_range(c.builder, qfd__kvosh.size) as zbij__ztd:
                i = zbij__ztd.index
                arr = qfd__kvosh.getitem(i)
                c.context.nrt.incref(c.builder, t, arr)
                idx = c.builder.add(oqv__djrrt, i)
                c.pyapi.list_setitem(spt__ovkec, idx, c.pyapi.
                    from_native_value(t, arr, c.env_manager))
            oqv__djrrt = c.builder.add(oqv__djrrt, qfd__kvosh.size)
        mceoj__ptvs = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
        ddn__eeqax = c.pyapi.call_function_objargs(mceoj__ptvs, (spt__ovkec,))
        c.pyapi.decref(mceoj__ptvs)
        c.pyapi.decref(spt__ovkec)
        c.context.nrt.decref(c.builder, typ, val)
        return ddn__eeqax
    spt__ovkec = c.pyapi.list_new(c.context.get_constant(types.int64, len(
        typ.arr_types)))
    ycn__pwwd = cgutils.is_not_null(c.builder, table.parent)
    if ensure_unboxed is None:
        ensure_unboxed = c.context.get_constant(types.bool_, False)
    for t, jlqi__jitai in typ.type_to_blk.items():
        acj__xdcs = getattr(table, f'block_{jlqi__jitai}')
        qfd__kvosh = ListInstance(c.context, c.builder, types.List(t),
            acj__xdcs)
        mpmzj__nmtjr = c.context.make_constant_array(c.builder, types.Array
            (types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[
            jlqi__jitai], dtype=np.int64))
        jyut__ysfdi = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, mpmzj__nmtjr)
        with cgutils.for_range(c.builder, qfd__kvosh.size) as zbij__ztd:
            i = zbij__ztd.index
            clxqt__vopi = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), jyut__ysfdi, i)
            arr = qfd__kvosh.getitem(i)
            tksn__zml = cgutils.alloca_once_value(c.builder, arr)
            gevl__musg = cgutils.alloca_once_value(c.builder, c.context.
                get_constant_null(t))
            is_null = is_ll_eq(c.builder, tksn__zml, gevl__musg)
            with c.builder.if_else(c.builder.and_(is_null, c.builder.not_(
                ensure_unboxed))) as (yuun__nyiqs, dfpv__gryuy):
                with yuun__nyiqs:
                    zyv__fsuyd = c.pyapi.make_none()
                    c.pyapi.list_setitem(spt__ovkec, clxqt__vopi, zyv__fsuyd)
                with dfpv__gryuy:
                    kbv__mriq = cgutils.alloca_once(c.builder, c.context.
                        get_value_type(types.pyobject))
                    with c.builder.if_else(c.builder.and_(is_null, ycn__pwwd)
                        ) as (wte__rzrcc, ttym__tbup):
                        with wte__rzrcc:
                            jwyi__sxv = get_df_obj_column_codegen(c.context,
                                c.builder, c.pyapi, table.parent,
                                clxqt__vopi, t)
                            c.builder.store(jwyi__sxv, kbv__mriq)
                        with ttym__tbup:
                            c.context.nrt.incref(c.builder, t, arr)
                            c.builder.store(c.pyapi.from_native_value(t,
                                arr, c.env_manager), kbv__mriq)
                    c.pyapi.list_setitem(spt__ovkec, clxqt__vopi, c.builder
                        .load(kbv__mriq))
    mceoj__ptvs = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
    ddn__eeqax = c.pyapi.call_function_objargs(mceoj__ptvs, (spt__ovkec,))
    c.pyapi.decref(mceoj__ptvs)
    c.pyapi.decref(spt__ovkec)
    c.context.nrt.decref(c.builder, typ, val)
    return ddn__eeqax


@lower_builtin(len, TableType)
def table_len_lower(context, builder, sig, args):
    impl = table_len_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def table_len_overload(T):
    if not isinstance(T, TableType):
        return

    def impl(T):
        return T._len
    return impl


@lower_getattr(TableType, 'shape')
def lower_table_shape(context, builder, typ, val):
    impl = table_shape_overload(typ)
    return context.compile_internal(builder, impl, types.Tuple([types.int64,
        types.int64])(typ), (val,))


def table_shape_overload(T):
    if T.has_runtime_cols:

        def impl(T):
            return T._len, compute_num_runtime_columns(T)
        return impl
    ncols = len(T.arr_types)
    return lambda T: (T._len, types.int64(ncols))


@intrinsic
def compute_num_runtime_columns(typingctx, table_type):
    assert isinstance(table_type, TableType)

    def codegen(context, builder, sig, args):
        table_arg, = args
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        rtlvy__ujtvk = context.get_constant(types.int64, 0)
        for i, t in enumerate(table_type.arr_types):
            acj__xdcs = getattr(table, f'block_{i}')
            qfd__kvosh = ListInstance(context, builder, types.List(t),
                acj__xdcs)
            rtlvy__ujtvk = builder.add(rtlvy__ujtvk, qfd__kvosh.size)
        return rtlvy__ujtvk
    sig = types.int64(table_type)
    return sig, codegen


def get_table_data_codegen(context, builder, table_arg, col_ind, table_type):
    arr_type = table_type.arr_types[col_ind]
    table = cgutils.create_struct_proxy(table_type)(context, builder, table_arg
        )
    jlqi__jitai = table_type.block_nums[col_ind]
    ronn__sjns = table_type.block_offsets[col_ind]
    acj__xdcs = getattr(table, f'block_{jlqi__jitai}')
    mvc__qnyro = types.none(table_type, types.List(arr_type), types.int64,
        types.int64)
    dmhz__hwypb = context.get_constant(types.int64, col_ind)
    jnsy__tzvn = context.get_constant(types.int64, ronn__sjns)
    yjch__zcfps = table_arg, acj__xdcs, jnsy__tzvn, dmhz__hwypb
    ensure_column_unboxed_codegen(context, builder, mvc__qnyro, yjch__zcfps)
    qfd__kvosh = ListInstance(context, builder, types.List(arr_type), acj__xdcs
        )
    arr = qfd__kvosh.getitem(ronn__sjns)
    return arr


@intrinsic
def get_table_data(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, sxrh__mex = args
        arr = get_table_data_codegen(context, builder, table_arg, col_ind,
            table_type)
        return impl_ret_borrowed(context, builder, arr_type, arr)
    sig = arr_type(table_type, ind_typ)
    return sig, codegen


@intrinsic
def del_column(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType
        ), 'Can only delete columns from a table'
    assert isinstance(ind_typ, types.TypeRef) and isinstance(ind_typ.
        instance_type, MetaType), 'ind_typ must be a typeref for a meta type'
    kgiu__yhcly = list(ind_typ.instance_type.meta)
    mee__ynau = defaultdict(list)
    for ind in kgiu__yhcly:
        mee__ynau[table_type.block_nums[ind]].append(table_type.
            block_offsets[ind])

    def codegen(context, builder, sig, args):
        table_arg, sxrh__mex = args
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        for jlqi__jitai, ljfex__ipox in mee__ynau.items():
            arr_type = table_type.blk_to_type[jlqi__jitai]
            acj__xdcs = getattr(table, f'block_{jlqi__jitai}')
            qfd__kvosh = ListInstance(context, builder, types.List(arr_type
                ), acj__xdcs)
            lww__wkczr = context.get_constant_null(arr_type)
            if len(ljfex__ipox) == 1:
                ronn__sjns = ljfex__ipox[0]
                arr = qfd__kvosh.getitem(ronn__sjns)
                context.nrt.decref(builder, arr_type, arr)
                qfd__kvosh.inititem(ronn__sjns, lww__wkczr, incref=False)
            else:
                shhp__uyh = context.get_constant(types.int64, len(ljfex__ipox))
                ndlf__bkjmh = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(ljfex__ipox, dtype
                    =np.int64))
                eyi__urure = context.make_array(types.Array(types.int64, 1,
                    'C'))(context, builder, ndlf__bkjmh)
                with cgutils.for_range(builder, shhp__uyh) as zbij__ztd:
                    i = zbij__ztd.index
                    ronn__sjns = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        eyi__urure, i)
                    arr = qfd__kvosh.getitem(ronn__sjns)
                    context.nrt.decref(builder, arr_type, arr)
                    qfd__kvosh.inititem(ronn__sjns, lww__wkczr, incref=False)
    sig = types.void(table_type, ind_typ)
    return sig, codegen


def set_table_data_codegen(context, builder, in_table_type, in_table,
    out_table_type, arr_type, arr_arg, col_ind, is_new_col):
    in_table = cgutils.create_struct_proxy(in_table_type)(context, builder,
        in_table)
    out_table = cgutils.create_struct_proxy(out_table_type)(context, builder)
    out_table.len = in_table.len
    out_table.parent = in_table.parent
    tqtq__hgofx = context.get_constant(types.int64, 0)
    xjeak__jxoqu = context.get_constant(types.int64, 1)
    fii__rymlq = arr_type not in in_table_type.type_to_blk
    for t, jlqi__jitai in out_table_type.type_to_blk.items():
        if t in in_table_type.type_to_blk:
            jxgt__koif = in_table_type.type_to_blk[t]
            qte__swp = ListInstance(context, builder, types.List(t),
                getattr(in_table, f'block_{jxgt__koif}'))
            context.nrt.incref(builder, types.List(t), qte__swp.value)
            setattr(out_table, f'block_{jlqi__jitai}', qte__swp.value)
    if fii__rymlq:
        sxrh__mex, qte__swp = ListInstance.allocate_ex(context, builder,
            types.List(arr_type), xjeak__jxoqu)
        qte__swp.size = xjeak__jxoqu
        qte__swp.inititem(tqtq__hgofx, arr_arg, incref=True)
        jlqi__jitai = out_table_type.type_to_blk[arr_type]
        setattr(out_table, f'block_{jlqi__jitai}', qte__swp.value)
        if not is_new_col:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
    else:
        jlqi__jitai = out_table_type.type_to_blk[arr_type]
        qte__swp = ListInstance(context, builder, types.List(arr_type),
            getattr(out_table, f'block_{jlqi__jitai}'))
        if is_new_col:
            n = qte__swp.size
            gtws__rxz = builder.add(n, xjeak__jxoqu)
            qte__swp.resize(gtws__rxz)
            qte__swp.inititem(n, arr_arg, incref=True)
        elif arr_type == in_table_type.arr_types[col_ind]:
            tcwt__lppow = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            qte__swp.setitem(tcwt__lppow, arr_arg, incref=True)
        else:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
            tcwt__lppow = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            n = qte__swp.size
            gtws__rxz = builder.add(n, xjeak__jxoqu)
            qte__swp.resize(gtws__rxz)
            context.nrt.incref(builder, arr_type, qte__swp.getitem(tcwt__lppow)
                )
            qte__swp.move(builder.add(tcwt__lppow, xjeak__jxoqu),
                tcwt__lppow, builder.sub(n, tcwt__lppow))
            qte__swp.setitem(tcwt__lppow, arr_arg, incref=True)
    return out_table._getvalue()


def _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
    context, builder):
    yzn__hsnc = in_table_type.arr_types[col_ind]
    if yzn__hsnc in out_table_type.type_to_blk:
        jlqi__jitai = out_table_type.type_to_blk[yzn__hsnc]
        beai__xml = getattr(out_table, f'block_{jlqi__jitai}')
        phhpo__aelp = types.List(yzn__hsnc)
        tcwt__lppow = context.get_constant(types.int64, in_table_type.
            block_offsets[col_ind])
        rrzt__saz = phhpo__aelp.dtype(phhpo__aelp, types.intp)
        vpypu__mbpx = context.compile_internal(builder, lambda lst, i: lst.
            pop(i), rrzt__saz, (beai__xml, tcwt__lppow))
        context.nrt.decref(builder, yzn__hsnc, vpypu__mbpx)


def generate_set_table_data_code(table, ind, arr_type, used_cols, is_null=False
    ):
    fyqlr__dsrar = list(table.arr_types)
    if ind == len(fyqlr__dsrar):
        gdt__isd = None
        fyqlr__dsrar.append(arr_type)
    else:
        gdt__isd = table.arr_types[ind]
        fyqlr__dsrar[ind] = arr_type
    tttne__mlil = TableType(tuple(fyqlr__dsrar))
    viyz__jwel = {'init_table': init_table, 'get_table_block':
        get_table_block, 'set_table_block': set_table_block,
        'set_table_len': set_table_len, 'set_table_parent':
        set_table_parent, 'alloc_list_like': alloc_list_like,
        'out_table_typ': tttne__mlil}
    xscx__rsox = 'def set_table_data(table, ind, arr, used_cols=None):\n'
    xscx__rsox += f'  T2 = init_table(out_table_typ, False)\n'
    xscx__rsox += f'  T2 = set_table_len(T2, len(table))\n'
    xscx__rsox += f'  T2 = set_table_parent(T2, table)\n'
    for typ, jlqi__jitai in tttne__mlil.type_to_blk.items():
        if typ in table.type_to_blk:
            khpfs__nxjq = table.type_to_blk[typ]
            xscx__rsox += (
                f'  arr_list_{jlqi__jitai} = get_table_block(table, {khpfs__nxjq})\n'
                )
            xscx__rsox += f"""  out_arr_list_{jlqi__jitai} = alloc_list_like(arr_list_{jlqi__jitai}, {len(tttne__mlil.block_to_arr_ind[jlqi__jitai])}, False)
"""
            if used_cols is None or set(table.block_to_arr_ind[khpfs__nxjq]
                ) & used_cols:
                xscx__rsox += (
                    f'  for i in range(len(arr_list_{jlqi__jitai})):\n')
                if typ not in (gdt__isd, arr_type):
                    xscx__rsox += (
                        f'    out_arr_list_{jlqi__jitai}[i] = arr_list_{jlqi__jitai}[i]\n'
                        )
                else:
                    wrq__loym = table.block_to_arr_ind[khpfs__nxjq]
                    ubome__iyom = np.empty(len(wrq__loym), np.int64)
                    fuk__fxqmp = False
                    for uervy__olwyq, clxqt__vopi in enumerate(wrq__loym):
                        if clxqt__vopi != ind:
                            ufkme__vcol = tttne__mlil.block_offsets[clxqt__vopi
                                ]
                        else:
                            ufkme__vcol = -1
                            fuk__fxqmp = True
                        ubome__iyom[uervy__olwyq] = ufkme__vcol
                    viyz__jwel[f'out_idxs_{jlqi__jitai}'] = np.array(
                        ubome__iyom, np.int64)
                    xscx__rsox += f'    out_idx = out_idxs_{jlqi__jitai}[i]\n'
                    if fuk__fxqmp:
                        xscx__rsox += f'    if out_idx == -1:\n'
                        xscx__rsox += f'      continue\n'
                    xscx__rsox += f"""    out_arr_list_{jlqi__jitai}[out_idx] = arr_list_{jlqi__jitai}[i]
"""
            if typ == arr_type and not is_null:
                xscx__rsox += f"""  out_arr_list_{jlqi__jitai}[{tttne__mlil.block_offsets[ind]}] = arr
"""
        else:
            viyz__jwel[f'arr_list_typ_{jlqi__jitai}'] = types.List(arr_type)
            xscx__rsox += f"""  out_arr_list_{jlqi__jitai} = alloc_list_like(arr_list_typ_{jlqi__jitai}, 1, False)
"""
            if not is_null:
                xscx__rsox += f'  out_arr_list_{jlqi__jitai}[0] = arr\n'
        xscx__rsox += (
            f'  T2 = set_table_block(T2, out_arr_list_{jlqi__jitai}, {jlqi__jitai})\n'
            )
    xscx__rsox += f'  return T2\n'
    xnv__ymkll = {}
    exec(xscx__rsox, viyz__jwel, xnv__ymkll)
    return xnv__ymkll['set_table_data']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def set_table_data(table, ind, arr, used_cols=None):
    if is_overload_none(used_cols):
        fesv__dds = None
    else:
        fesv__dds = set(used_cols.instance_type.meta)
    osckz__cjap = get_overload_const_int(ind)
    return generate_set_table_data_code(table, osckz__cjap, arr, fesv__dds)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def set_table_data_null(table, ind, arr, used_cols=None):
    osckz__cjap = get_overload_const_int(ind)
    arr_type = arr.instance_type
    if is_overload_none(used_cols):
        fesv__dds = None
    else:
        fesv__dds = set(used_cols.instance_type.meta)
    return generate_set_table_data_code(table, osckz__cjap, arr_type,
        fesv__dds, is_null=True)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_table_data',
    'bodo.hiframes.table'] = alias_ext_dummy_func


def get_table_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    jtu__iou = args[0]
    if equiv_set.has_shape(jtu__iou):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            jtu__iou)[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_get_table_data = (
    get_table_data_equiv)


@lower_constant(TableType)
def lower_constant_table(context, builder, table_type, pyval):
    hxu__aevb = []
    for t, jlqi__jitai in table_type.type_to_blk.items():
        qleq__ijed = len(table_type.block_to_arr_ind[jlqi__jitai])
        bfz__raogd = []
        for i in range(qleq__ijed):
            clxqt__vopi = table_type.block_to_arr_ind[jlqi__jitai][i]
            bfz__raogd.append(pyval.arrays[clxqt__vopi])
        hxu__aevb.append(context.get_constant_generic(builder, types.List(t
            ), bfz__raogd))
    hshe__tnx = context.get_constant_null(types.pyobject)
    prly__lrsts = context.get_constant(types.int64, 0 if len(pyval.arrays) ==
        0 else len(pyval.arrays[0]))
    return lir.Constant.literal_struct(hxu__aevb + [hshe__tnx, prly__lrsts])


@intrinsic
def init_table(typingctx, table_type, to_str_if_dict_t):
    out_table_type = table_type.instance_type if isinstance(table_type,
        types.TypeRef) else table_type
    assert isinstance(out_table_type, TableType
        ), 'table type or typeref expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    if is_overload_true(to_str_if_dict_t):
        out_table_type = to_str_arr_if_dict_array(out_table_type)

    def codegen(context, builder, sig, args):
        table = cgutils.create_struct_proxy(out_table_type)(context, builder)
        for t, jlqi__jitai in out_table_type.type_to_blk.items():
            dceq__llny = context.get_constant_null(types.List(t))
            setattr(table, f'block_{jlqi__jitai}', dceq__llny)
        return table._getvalue()
    sig = out_table_type(table_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def init_table_from_lists(typingctx, tuple_of_lists_type, table_type):
    assert isinstance(tuple_of_lists_type, types.BaseTuple
        ), 'Tuple of data expected'
    bzy__tmhss = {}
    for i, typ in enumerate(tuple_of_lists_type):
        assert isinstance(typ, types.List), 'Each tuple element must be a list'
        bzy__tmhss[typ.dtype] = i
    yxc__svv = table_type.instance_type if isinstance(table_type, types.TypeRef
        ) else table_type
    assert isinstance(yxc__svv, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        wfdv__rkp, sxrh__mex = args
        table = cgutils.create_struct_proxy(yxc__svv)(context, builder)
        for t, jlqi__jitai in yxc__svv.type_to_blk.items():
            idx = bzy__tmhss[t]
            gnt__zvt = signature(types.List(t), tuple_of_lists_type, types.
                literal(idx))
            vdn__vcq = wfdv__rkp, idx
            tgy__hhj = numba.cpython.tupleobj.static_getitem_tuple(context,
                builder, gnt__zvt, vdn__vcq)
            setattr(table, f'block_{jlqi__jitai}', tgy__hhj)
        return table._getvalue()
    sig = yxc__svv(tuple_of_lists_type, table_type)
    return sig, codegen


@intrinsic
def get_table_block(typingctx, table_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_int(blk_type)
    jlqi__jitai = get_overload_const_int(blk_type)
    arr_type = None
    for t, abh__nipww in table_type.type_to_blk.items():
        if abh__nipww == jlqi__jitai:
            arr_type = t
            break
    assert arr_type is not None, 'invalid table type block'
    cnpyb__uljy = types.List(arr_type)

    def codegen(context, builder, sig, args):
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            args[0])
        acj__xdcs = getattr(table, f'block_{jlqi__jitai}')
        return impl_ret_borrowed(context, builder, cnpyb__uljy, acj__xdcs)
    sig = cnpyb__uljy(table_type, blk_type)
    return sig, codegen


@intrinsic
def ensure_table_unboxed(typingctx, table_type, used_cols_typ):

    def codegen(context, builder, sig, args):
        table_arg, nuy__hbq = args
        yelw__zjo = context.get_python_api(builder)
        whyiw__aikub = used_cols_typ == types.none
        if not whyiw__aikub:
            lir__orghs = numba.cpython.setobj.SetInstance(context, builder,
                types.Set(types.int64), nuy__hbq)
        table = cgutils.create_struct_proxy(sig.args[0])(context, builder,
            table_arg)
        for t, jlqi__jitai in table_type.type_to_blk.items():
            shhp__uyh = context.get_constant(types.int64, len(table_type.
                block_to_arr_ind[jlqi__jitai]))
            mpmzj__nmtjr = context.make_constant_array(builder, types.Array
                (types.int64, 1, 'C'), np.array(table_type.block_to_arr_ind
                [jlqi__jitai], dtype=np.int64))
            jyut__ysfdi = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, mpmzj__nmtjr)
            acj__xdcs = getattr(table, f'block_{jlqi__jitai}')
            with cgutils.for_range(builder, shhp__uyh) as zbij__ztd:
                i = zbij__ztd.index
                clxqt__vopi = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    jyut__ysfdi, i)
                mvc__qnyro = types.none(table_type, types.List(t), types.
                    int64, types.int64)
                yjch__zcfps = table_arg, acj__xdcs, i, clxqt__vopi
                if whyiw__aikub:
                    ensure_column_unboxed_codegen(context, builder,
                        mvc__qnyro, yjch__zcfps)
                else:
                    dbl__see = lir__orghs.contains(clxqt__vopi)
                    with builder.if_then(dbl__see):
                        ensure_column_unboxed_codegen(context, builder,
                            mvc__qnyro, yjch__zcfps)
    assert isinstance(table_type, TableType), 'table type expected'
    sig = types.none(table_type, used_cols_typ)
    return sig, codegen


@intrinsic
def ensure_column_unboxed(typingctx, table_type, arr_list_t, ind_t, arr_ind_t):
    assert isinstance(table_type, TableType), 'table type expected'
    sig = types.none(table_type, arr_list_t, ind_t, arr_ind_t)
    return sig, ensure_column_unboxed_codegen


def ensure_column_unboxed_codegen(context, builder, sig, args):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    table_arg, yrntw__pfzf, gnjc__qts, kotkc__elors = args
    yelw__zjo = context.get_python_api(builder)
    table = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        table_arg)
    ycn__pwwd = cgutils.is_not_null(builder, table.parent)
    qfd__kvosh = ListInstance(context, builder, sig.args[1], yrntw__pfzf)
    npgq__fflq = qfd__kvosh.getitem(gnjc__qts)
    tksn__zml = cgutils.alloca_once_value(builder, npgq__fflq)
    gevl__musg = cgutils.alloca_once_value(builder, context.
        get_constant_null(sig.args[1].dtype))
    is_null = is_ll_eq(builder, tksn__zml, gevl__musg)
    with builder.if_then(is_null):
        with builder.if_else(ycn__pwwd) as (yuun__nyiqs, dfpv__gryuy):
            with yuun__nyiqs:
                kbv__mriq = get_df_obj_column_codegen(context, builder,
                    yelw__zjo, table.parent, kotkc__elors, sig.args[1].dtype)
                arr = yelw__zjo.to_native_value(sig.args[1].dtype, kbv__mriq
                    ).value
                qfd__kvosh.inititem(gnjc__qts, arr, incref=False)
                yelw__zjo.decref(kbv__mriq)
            with dfpv__gryuy:
                context.call_conv.return_user_exc(builder, BodoError, (
                    'unexpected null table column',))


@intrinsic
def set_table_block(typingctx, table_type, arr_list_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert isinstance(arr_list_type, types.List), 'list type expected'
    assert is_overload_constant_int(blk_type), 'blk should be const int'
    jlqi__jitai = get_overload_const_int(blk_type)

    def codegen(context, builder, sig, args):
        table_arg, tcayv__ukky, sxrh__mex = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        setattr(in_table, f'block_{jlqi__jitai}', tcayv__ukky)
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, arr_list_type, blk_type)
    return sig, codegen


@intrinsic
def set_table_len(typingctx, table_type, l_type):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        table_arg, hjzgb__sfk = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        in_table.len = hjzgb__sfk
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, l_type)
    return sig, codegen


@intrinsic
def set_table_parent(typingctx, out_table_type, in_table_type):
    assert isinstance(in_table_type, TableType), 'table type expected'
    assert isinstance(out_table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        okr__oky, qwdm__unaud = args
        in_table = cgutils.create_struct_proxy(in_table_type)(context,
            builder, qwdm__unaud)
        out_table = cgutils.create_struct_proxy(out_table_type)(context,
            builder, okr__oky)
        out_table.parent = in_table.parent
        context.nrt.incref(builder, types.pyobject, out_table.parent)
        return impl_ret_borrowed(context, builder, out_table_type,
            out_table._getvalue())
    sig = out_table_type(out_table_type, in_table_type)
    return sig, codegen


@intrinsic
def alloc_list_like(typingctx, list_type, len_type, to_str_if_dict_t):
    cnpyb__uljy = list_type.instance_type if isinstance(list_type, types.
        TypeRef) else list_type
    assert isinstance(cnpyb__uljy, types.List), 'list type or typeref expected'
    assert isinstance(len_type, types.Integer), 'integer type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    if is_overload_true(to_str_if_dict_t):
        cnpyb__uljy = types.List(to_str_arr_if_dict_array(cnpyb__uljy.dtype))

    def codegen(context, builder, sig, args):
        rli__cdtsv = args[1]
        sxrh__mex, qte__swp = ListInstance.allocate_ex(context, builder,
            cnpyb__uljy, rli__cdtsv)
        qte__swp.size = rli__cdtsv
        return qte__swp.value
    sig = cnpyb__uljy(list_type, len_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def alloc_empty_list_type(typingctx, size_typ, data_typ):
    assert isinstance(size_typ, types.Integer), 'Size must be an integer'
    urwn__xjwkz = data_typ.instance_type if isinstance(data_typ, types.TypeRef
        ) else data_typ
    list_type = types.List(urwn__xjwkz)

    def codegen(context, builder, sig, args):
        rli__cdtsv, sxrh__mex = args
        sxrh__mex, qte__swp = ListInstance.allocate_ex(context, builder,
            list_type, rli__cdtsv)
        qte__swp.size = rli__cdtsv
        return qte__swp.value
    sig = list_type(size_typ, data_typ)
    return sig, codegen


def _get_idx_length(idx):
    pass


@overload(_get_idx_length)
def overload_get_idx_length(idx, n):
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        return lambda idx, n: idx.sum()
    assert isinstance(idx, types.SliceType), 'slice index expected'

    def impl(idx, n):
        iprze__snf = numba.cpython.unicode._normalize_slice(idx, n)
        return numba.cpython.unicode._slice_span(iprze__snf)
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_filter(T, idx, used_cols=None):
    from bodo.utils.conversion import ensure_contig_if_np
    viyz__jwel = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, '_get_idx_length':
        _get_idx_length, 'ensure_contig_if_np': ensure_contig_if_np}
    if not is_overload_none(used_cols):
        efu__kflm = used_cols.instance_type
        zyi__gvxdf = np.array(efu__kflm.meta, dtype=np.int64)
        viyz__jwel['used_cols_vals'] = zyi__gvxdf
        cwezk__dvz = set([T.block_nums[i] for i in zyi__gvxdf])
    else:
        zyi__gvxdf = None
    xscx__rsox = 'def table_filter_func(T, idx, used_cols=None):\n'
    xscx__rsox += f'  T2 = init_table(T, False)\n'
    xscx__rsox += f'  l = 0\n'
    if zyi__gvxdf is not None and len(zyi__gvxdf) == 0:
        xscx__rsox += f'  l = _get_idx_length(idx, len(T))\n'
        xscx__rsox += f'  T2 = set_table_len(T2, l)\n'
        xscx__rsox += f'  return T2\n'
        xnv__ymkll = {}
        exec(xscx__rsox, viyz__jwel, xnv__ymkll)
        return xnv__ymkll['table_filter_func']
    if zyi__gvxdf is not None:
        xscx__rsox += f'  used_set = set(used_cols_vals)\n'
    for jlqi__jitai in T.type_to_blk.values():
        xscx__rsox += (
            f'  arr_list_{jlqi__jitai} = get_table_block(T, {jlqi__jitai})\n')
        xscx__rsox += f"""  out_arr_list_{jlqi__jitai} = alloc_list_like(arr_list_{jlqi__jitai}, len(arr_list_{jlqi__jitai}), False)
"""
        if zyi__gvxdf is None or jlqi__jitai in cwezk__dvz:
            viyz__jwel[f'arr_inds_{jlqi__jitai}'] = np.array(T.
                block_to_arr_ind[jlqi__jitai], dtype=np.int64)
            xscx__rsox += f'  for i in range(len(arr_list_{jlqi__jitai})):\n'
            xscx__rsox += (
                f'    arr_ind_{jlqi__jitai} = arr_inds_{jlqi__jitai}[i]\n')
            if zyi__gvxdf is not None:
                xscx__rsox += (
                    f'    if arr_ind_{jlqi__jitai} not in used_set: continue\n'
                    )
            xscx__rsox += f"""    ensure_column_unboxed(T, arr_list_{jlqi__jitai}, i, arr_ind_{jlqi__jitai})
"""
            xscx__rsox += f"""    out_arr_{jlqi__jitai} = ensure_contig_if_np(arr_list_{jlqi__jitai}[i][idx])
"""
            xscx__rsox += f'    l = len(out_arr_{jlqi__jitai})\n'
            xscx__rsox += (
                f'    out_arr_list_{jlqi__jitai}[i] = out_arr_{jlqi__jitai}\n')
        xscx__rsox += (
            f'  T2 = set_table_block(T2, out_arr_list_{jlqi__jitai}, {jlqi__jitai})\n'
            )
    xscx__rsox += f'  T2 = set_table_len(T2, l)\n'
    xscx__rsox += f'  return T2\n'
    xnv__ymkll = {}
    exec(xscx__rsox, viyz__jwel, xnv__ymkll)
    return xnv__ymkll['table_filter_func']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_subset(T, idx, copy_arrs, used_cols=None):
    zrih__samgh = list(idx.instance_type.meta)
    fyqlr__dsrar = tuple(np.array(T.arr_types, dtype=object)[zrih__samgh])
    tttne__mlil = TableType(fyqlr__dsrar)
    if not is_overload_constant_bool(copy_arrs):
        raise_bodo_error('table_subset(): copy_arrs must be a constant')
    rxlxx__yprk = is_overload_true(copy_arrs)
    viyz__jwel = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, 'out_table_typ': tttne__mlil}
    if not is_overload_none(used_cols):
        kept_cols = used_cols.instance_type.meta
        hvn__nakra = set(kept_cols)
        viyz__jwel['kept_cols'] = np.array(kept_cols, np.int64)
        gdcvc__wfyhp = True
    else:
        gdcvc__wfyhp = False
    rdsno__ajh = {i: c for i, c in enumerate(zrih__samgh)}
    xscx__rsox = 'def table_subset(T, idx, copy_arrs, used_cols=None):\n'
    xscx__rsox += f'  T2 = init_table(out_table_typ, False)\n'
    xscx__rsox += f'  T2 = set_table_len(T2, len(T))\n'
    if gdcvc__wfyhp and len(hvn__nakra) == 0:
        xscx__rsox += f'  return T2\n'
        xnv__ymkll = {}
        exec(xscx__rsox, viyz__jwel, xnv__ymkll)
        return xnv__ymkll['table_subset']
    if gdcvc__wfyhp:
        xscx__rsox += f'  kept_cols_set = set(kept_cols)\n'
    for typ, jlqi__jitai in tttne__mlil.type_to_blk.items():
        khpfs__nxjq = T.type_to_blk[typ]
        xscx__rsox += (
            f'  arr_list_{jlqi__jitai} = get_table_block(T, {khpfs__nxjq})\n')
        xscx__rsox += f"""  out_arr_list_{jlqi__jitai} = alloc_list_like(arr_list_{jlqi__jitai}, {len(tttne__mlil.block_to_arr_ind[jlqi__jitai])}, False)
"""
        ssblm__spln = True
        if gdcvc__wfyhp:
            zqwm__orq = set(tttne__mlil.block_to_arr_ind[jlqi__jitai])
            isx__grvr = zqwm__orq & hvn__nakra
            ssblm__spln = len(isx__grvr) > 0
        if ssblm__spln:
            viyz__jwel[f'out_arr_inds_{jlqi__jitai}'] = np.array(tttne__mlil
                .block_to_arr_ind[jlqi__jitai], dtype=np.int64)
            xscx__rsox += (
                f'  for i in range(len(out_arr_list_{jlqi__jitai})):\n')
            xscx__rsox += (
                f'    out_arr_ind_{jlqi__jitai} = out_arr_inds_{jlqi__jitai}[i]\n'
                )
            if gdcvc__wfyhp:
                xscx__rsox += (
                    f'    if out_arr_ind_{jlqi__jitai} not in kept_cols_set: continue\n'
                    )
            nfx__adxk = []
            zawkh__ysty = []
            for xpgt__lcgn in tttne__mlil.block_to_arr_ind[jlqi__jitai]:
                cghmt__xui = rdsno__ajh[xpgt__lcgn]
                nfx__adxk.append(cghmt__xui)
                daqhu__wees = T.block_offsets[cghmt__xui]
                zawkh__ysty.append(daqhu__wees)
            viyz__jwel[f'in_logical_idx_{jlqi__jitai}'] = np.array(nfx__adxk,
                dtype=np.int64)
            viyz__jwel[f'in_physical_idx_{jlqi__jitai}'] = np.array(zawkh__ysty
                , dtype=np.int64)
            xscx__rsox += (
                f'    logical_idx_{jlqi__jitai} = in_logical_idx_{jlqi__jitai}[i]\n'
                )
            xscx__rsox += (
                f'    physical_idx_{jlqi__jitai} = in_physical_idx_{jlqi__jitai}[i]\n'
                )
            xscx__rsox += f"""    ensure_column_unboxed(T, arr_list_{jlqi__jitai}, physical_idx_{jlqi__jitai}, logical_idx_{jlqi__jitai})
"""
            afvm__gco = '.copy()' if rxlxx__yprk else ''
            xscx__rsox += f"""    out_arr_list_{jlqi__jitai}[i] = arr_list_{jlqi__jitai}[physical_idx_{jlqi__jitai}]{afvm__gco}
"""
        xscx__rsox += (
            f'  T2 = set_table_block(T2, out_arr_list_{jlqi__jitai}, {jlqi__jitai})\n'
            )
    xscx__rsox += f'  return T2\n'
    xnv__ymkll = {}
    exec(xscx__rsox, viyz__jwel, xnv__ymkll)
    return xnv__ymkll['table_subset']


def table_filter_equiv(self, scope, equiv_set, loc, args, kws):
    jtu__iou = args[0]
    if equiv_set.has_shape(jtu__iou):
        if guard(is_whole_slice, self.typemap, self.func_ir, args[1]):
            return ArrayAnalysis.AnalyzeResult(shape=jtu__iou, pre=[])
        return ArrayAnalysis.AnalyzeResult(shape=(None, equiv_set.get_shape
            (jtu__iou)[1]), pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_table_filter = (
    table_filter_equiv)


def table_subset_equiv(self, scope, equiv_set, loc, args, kws):
    jtu__iou = args[0]
    if equiv_set.has_shape(jtu__iou):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            jtu__iou)[0], None), pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_table_subset = (
    table_subset_equiv)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def decode_if_dict_table(T):
    xscx__rsox = 'def impl(T):\n'
    xscx__rsox += f'  T2 = init_table(T, True)\n'
    xscx__rsox += f'  l = len(T)\n'
    viyz__jwel = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, 'decode_if_dict_array':
        decode_if_dict_array}
    for jlqi__jitai in T.type_to_blk.values():
        viyz__jwel[f'arr_inds_{jlqi__jitai}'] = np.array(T.block_to_arr_ind
            [jlqi__jitai], dtype=np.int64)
        xscx__rsox += (
            f'  arr_list_{jlqi__jitai} = get_table_block(T, {jlqi__jitai})\n')
        xscx__rsox += f"""  out_arr_list_{jlqi__jitai} = alloc_list_like(arr_list_{jlqi__jitai}, len(arr_list_{jlqi__jitai}), True)
"""
        xscx__rsox += f'  for i in range(len(arr_list_{jlqi__jitai})):\n'
        xscx__rsox += (
            f'    arr_ind_{jlqi__jitai} = arr_inds_{jlqi__jitai}[i]\n')
        xscx__rsox += f"""    ensure_column_unboxed(T, arr_list_{jlqi__jitai}, i, arr_ind_{jlqi__jitai})
"""
        xscx__rsox += f"""    out_arr_{jlqi__jitai} = decode_if_dict_array(arr_list_{jlqi__jitai}[i])
"""
        xscx__rsox += (
            f'    out_arr_list_{jlqi__jitai}[i] = out_arr_{jlqi__jitai}\n')
        xscx__rsox += (
            f'  T2 = set_table_block(T2, out_arr_list_{jlqi__jitai}, {jlqi__jitai})\n'
            )
    xscx__rsox += f'  T2 = set_table_len(T2, l)\n'
    xscx__rsox += f'  return T2\n'
    xnv__ymkll = {}
    exec(xscx__rsox, viyz__jwel, xnv__ymkll)
    return xnv__ymkll['impl']


@overload(operator.getitem, no_unliteral=True, inline='always')
def overload_table_getitem(T, idx):
    if not isinstance(T, TableType):
        return
    return lambda T, idx: table_filter(T, idx)


@intrinsic
def init_runtime_table_from_lists(typingctx, arr_list_tup_typ, nrows_typ=None):
    assert isinstance(arr_list_tup_typ, types.BaseTuple
        ), 'init_runtime_table_from_lists requires a tuple of list of arrays'
    if isinstance(arr_list_tup_typ, types.UniTuple):
        if arr_list_tup_typ.dtype.dtype == types.undefined:
            return
        fvmr__lxa = [arr_list_tup_typ.dtype.dtype] * len(arr_list_tup_typ)
    else:
        fvmr__lxa = []
        for typ in arr_list_tup_typ:
            if typ.dtype == types.undefined:
                return
            fvmr__lxa.append(typ.dtype)
    assert isinstance(nrows_typ, types.Integer
        ), 'init_runtime_table_from_lists requires an integer length'

    def codegen(context, builder, sig, args):
        uxymt__esec, dbcj__ghd = args
        table = cgutils.create_struct_proxy(table_type)(context, builder)
        table.len = dbcj__ghd
        hxu__aevb = cgutils.unpack_tuple(builder, uxymt__esec)
        for i, acj__xdcs in enumerate(hxu__aevb):
            setattr(table, f'block_{i}', acj__xdcs)
            context.nrt.incref(builder, types.List(fvmr__lxa[i]), acj__xdcs)
        return table._getvalue()
    table_type = TableType(tuple(fvmr__lxa), True)
    sig = table_type(arr_list_tup_typ, nrows_typ)
    return sig, codegen


def _to_arr_if_series(t):
    return t.data if isinstance(t, SeriesType) else t


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def logical_table_to_table(in_table_t, extra_arrs_t, in_col_inds_t,
    n_table_cols_t, out_table_type_t=None, used_cols=None):
    in_col_inds = in_col_inds_t.instance_type.meta
    assert isinstance(in_table_t, (TableType, types.BaseTuple, types.NoneType)
        ), 'logical_table_to_table: input table must be a TableType or tuple of arrays or None (for dead table)'
    viyz__jwel = {}
    if not is_overload_none(used_cols):
        kept_cols = set(used_cols.instance_type.meta)
        viyz__jwel['kept_cols'] = np.array(list(kept_cols), np.int64)
        gdcvc__wfyhp = True
    else:
        kept_cols = set(np.arange(len(in_col_inds)))
        gdcvc__wfyhp = False
    extra_arrs_no_series = ', '.join(f'get_series_data(extra_arrs_t[{i}])' if
        isinstance(extra_arrs_t[i], SeriesType) else f'extra_arrs_t[{i}]' for
        i in range(len(extra_arrs_t)))
    extra_arrs_no_series = (
        f"({extra_arrs_no_series}{',' if len(extra_arrs_t) == 1 else ''})")
    if isinstance(in_table_t, (types.BaseTuple, types.NoneType)):
        return _logical_tuple_table_to_table_codegen(in_table_t,
            extra_arrs_t, in_col_inds, kept_cols, n_table_cols_t,
            out_table_type_t, extra_arrs_no_series)
    rwldx__atjqk = len(in_table_t.arr_types)
    out_table_type = TableType(tuple(in_table_t.arr_types[i] if i <
        rwldx__atjqk else _to_arr_if_series(extra_arrs_t.types[i -
        rwldx__atjqk]) for i in in_col_inds)) if is_overload_none(
        out_table_type_t) else unwrap_typeref(out_table_type_t)
    xscx__rsox = """def impl(in_table_t, extra_arrs_t, in_col_inds_t, n_table_cols_t, out_table_type_t=None, used_cols=None):
"""
    if any(isinstance(t, SeriesType) for t in extra_arrs_t.types):
        xscx__rsox += f'  extra_arrs_t = {extra_arrs_no_series}\n'
    xscx__rsox += f'  T1 = in_table_t\n'
    xscx__rsox += f'  T2 = init_table(out_table_type, False)\n'
    xscx__rsox += f'  T2 = set_table_len(T2, len(T1))\n'
    if gdcvc__wfyhp and len(kept_cols) == 0:
        xscx__rsox += f'  return T2\n'
        xnv__ymkll = {}
        exec(xscx__rsox, viyz__jwel, xnv__ymkll)
        return xnv__ymkll['impl']
    if gdcvc__wfyhp:
        xscx__rsox += f'  kept_cols_set = set(kept_cols)\n'
    for typ, jlqi__jitai in out_table_type.type_to_blk.items():
        viyz__jwel[f'arr_list_typ_{jlqi__jitai}'] = types.List(typ)
        shhp__uyh = len(out_table_type.block_to_arr_ind[jlqi__jitai])
        xscx__rsox += f"""  out_arr_list_{jlqi__jitai} = alloc_list_like(arr_list_typ_{jlqi__jitai}, {shhp__uyh}, False)
"""
        if typ in in_table_t.type_to_blk:
            obtcf__kmbud = in_table_t.type_to_blk[typ]
            jqqv__cfhip = []
            mkr__papsq = []
            for fzafj__zcbbn in out_table_type.block_to_arr_ind[jlqi__jitai]:
                tov__ydx = in_col_inds[fzafj__zcbbn]
                if tov__ydx < rwldx__atjqk:
                    jqqv__cfhip.append(in_table_t.block_offsets[tov__ydx])
                    mkr__papsq.append(tov__ydx)
                else:
                    jqqv__cfhip.append(-1)
                    mkr__papsq.append(-1)
            viyz__jwel[f'in_idxs_{jlqi__jitai}'] = np.array(jqqv__cfhip, np
                .int64)
            viyz__jwel[f'in_arr_inds_{jlqi__jitai}'] = np.array(mkr__papsq,
                np.int64)
            if gdcvc__wfyhp:
                viyz__jwel[f'out_arr_inds_{jlqi__jitai}'] = np.array(
                    out_table_type.block_to_arr_ind[jlqi__jitai], dtype=np.
                    int64)
            xscx__rsox += (
                f'  in_arr_list_{jlqi__jitai} = get_table_block(T1, {obtcf__kmbud})\n'
                )
            xscx__rsox += (
                f'  for i in range(len(out_arr_list_{jlqi__jitai})):\n')
            xscx__rsox += (
                f'    in_offset_{jlqi__jitai} = in_idxs_{jlqi__jitai}[i]\n')
            xscx__rsox += f'    if in_offset_{jlqi__jitai} == -1:\n'
            xscx__rsox += f'      continue\n'
            xscx__rsox += (
                f'    in_arr_ind_{jlqi__jitai} = in_arr_inds_{jlqi__jitai}[i]\n'
                )
            if gdcvc__wfyhp:
                xscx__rsox += f"""    if out_arr_inds_{jlqi__jitai}[i] not in kept_cols_set: continue
"""
            xscx__rsox += f"""    ensure_column_unboxed(T1, in_arr_list_{jlqi__jitai}, in_offset_{jlqi__jitai}, in_arr_ind_{jlqi__jitai})
"""
            xscx__rsox += f"""    out_arr_list_{jlqi__jitai}[i] = in_arr_list_{jlqi__jitai}[in_offset_{jlqi__jitai}]
"""
        for i, fzafj__zcbbn in enumerate(out_table_type.block_to_arr_ind[
            jlqi__jitai]):
            if fzafj__zcbbn not in kept_cols:
                continue
            tov__ydx = in_col_inds[fzafj__zcbbn]
            if tov__ydx >= rwldx__atjqk:
                xscx__rsox += f"""  out_arr_list_{jlqi__jitai}[{i}] = extra_arrs_t[{tov__ydx - rwldx__atjqk}]
"""
        xscx__rsox += (
            f'  T2 = set_table_block(T2, out_arr_list_{jlqi__jitai}, {jlqi__jitai})\n'
            )
    xscx__rsox += f'  return T2\n'
    viyz__jwel.update({'init_table': init_table, 'alloc_list_like':
        alloc_list_like, 'set_table_block': set_table_block,
        'set_table_len': set_table_len, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'out_table_type':
        out_table_type, 'get_series_data': bodo.hiframes.pd_series_ext.
        get_series_data})
    xnv__ymkll = {}
    exec(xscx__rsox, viyz__jwel, xnv__ymkll)
    return xnv__ymkll['impl']


def _logical_tuple_table_to_table_codegen(in_table_t, extra_arrs_t,
    in_col_inds, kept_cols, n_table_cols_t, out_table_type_t,
    extra_arrs_no_series):
    rwldx__atjqk = get_overload_const_int(n_table_cols_t
        ) if is_overload_constant_int(n_table_cols_t) else len(in_table_t.types
        )
    out_table_type = TableType(tuple(in_table_t.types[i] if i <
        rwldx__atjqk else _to_arr_if_series(extra_arrs_t.types[i -
        rwldx__atjqk]) for i in in_col_inds)) if is_overload_none(
        out_table_type_t) else unwrap_typeref(out_table_type_t)
    uuw__vyt = None
    if not is_overload_none(in_table_t):
        for i, t in enumerate(in_table_t.types):
            if t != types.none:
                uuw__vyt = f'in_table_t[{i}]'
                break
    if uuw__vyt is None:
        for i, t in enumerate(extra_arrs_t.types):
            if t != types.none:
                uuw__vyt = f'extra_arrs_t[{i}]'
                break
    assert uuw__vyt is not None, 'no array found in input data'
    xscx__rsox = """def impl(in_table_t, extra_arrs_t, in_col_inds_t, n_table_cols_t, out_table_type_t=None, used_cols=None):
"""
    if any(isinstance(t, SeriesType) for t in extra_arrs_t.types):
        xscx__rsox += f'  extra_arrs_t = {extra_arrs_no_series}\n'
    xscx__rsox += f'  T1 = in_table_t\n'
    xscx__rsox += f'  T2 = init_table(out_table_type, False)\n'
    xscx__rsox += f'  T2 = set_table_len(T2, len({uuw__vyt}))\n'
    viyz__jwel = {}
    for typ, jlqi__jitai in out_table_type.type_to_blk.items():
        viyz__jwel[f'arr_list_typ_{jlqi__jitai}'] = types.List(typ)
        shhp__uyh = len(out_table_type.block_to_arr_ind[jlqi__jitai])
        xscx__rsox += f"""  out_arr_list_{jlqi__jitai} = alloc_list_like(arr_list_typ_{jlqi__jitai}, {shhp__uyh}, False)
"""
        for i, fzafj__zcbbn in enumerate(out_table_type.block_to_arr_ind[
            jlqi__jitai]):
            if fzafj__zcbbn not in kept_cols:
                continue
            tov__ydx = in_col_inds[fzafj__zcbbn]
            if tov__ydx < rwldx__atjqk:
                xscx__rsox += (
                    f'  out_arr_list_{jlqi__jitai}[{i}] = T1[{tov__ydx}]\n')
            else:
                xscx__rsox += f"""  out_arr_list_{jlqi__jitai}[{i}] = extra_arrs_t[{tov__ydx - rwldx__atjqk}]
"""
        xscx__rsox += (
            f'  T2 = set_table_block(T2, out_arr_list_{jlqi__jitai}, {jlqi__jitai})\n'
            )
    xscx__rsox += f'  return T2\n'
    viyz__jwel.update({'init_table': init_table, 'alloc_list_like':
        alloc_list_like, 'set_table_block': set_table_block,
        'set_table_len': set_table_len, 'out_table_type': out_table_type,
        'get_series_data': bodo.hiframes.pd_series_ext.get_series_data})
    xnv__ymkll = {}
    exec(xscx__rsox, viyz__jwel, xnv__ymkll)
    return xnv__ymkll['impl']


def logical_table_to_table_equiv(self, scope, equiv_set, loc, args, kws):
    rye__pul = args[0]
    zua__abzgq = args[1]
    if equiv_set.has_shape(rye__pul):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            rye__pul)[0], None), pre=[])
    if equiv_set.has_shape(zua__abzgq):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            zua__abzgq)[0], None), pre=[])


(ArrayAnalysis._analyze_op_call_bodo_hiframes_table_logical_table_to_table
    ) = logical_table_to_table_equiv


def alias_ext_logical_table_to_table(lhs_name, args, alias_map, arg_aliases):
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['logical_table_to_table',
    'bodo.hiframes.table'] = alias_ext_logical_table_to_table
