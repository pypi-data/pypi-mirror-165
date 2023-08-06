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
            qirp__xvdh = 0
            odua__xhwtm = []
            for i in range(usecols[-1] + 1):
                if i == usecols[qirp__xvdh]:
                    odua__xhwtm.append(arrs[qirp__xvdh])
                    qirp__xvdh += 1
                else:
                    odua__xhwtm.append(None)
            for ijri__cluxe in range(usecols[-1] + 1, num_arrs):
                odua__xhwtm.append(None)
            self.arrays = odua__xhwtm
        else:
            self.arrays = arrs
        self.block_0 = arrs

    def __eq__(self, other):
        return isinstance(other, Table) and len(self.arrays) == len(other.
            arrays) and all((nuae__bpql == sjh__nebs).all() for nuae__bpql,
            sjh__nebs in zip(self.arrays, other.arrays))

    def __str__(self) ->str:
        return str(self.arrays)

    def to_pandas(self, index=None):
        bccp__obmy = len(self.arrays)
        vroc__sbw = dict(zip(range(bccp__obmy), self.arrays))
        df = pd.DataFrame(vroc__sbw, index)
        return df


class TableType(types.ArrayCompatible):

    def __init__(self, arr_types, has_runtime_cols=False):
        self.arr_types = arr_types
        self.has_runtime_cols = has_runtime_cols
        hfcd__rhqs = []
        ugnjc__ebfp = []
        tzl__njqoy = {}
        uhis__zndlf = {}
        ufkhs__hsea = defaultdict(int)
        dawfk__hwqs = defaultdict(list)
        if not has_runtime_cols:
            for i, t in enumerate(arr_types):
                if t not in tzl__njqoy:
                    pvnbn__wcqg = len(tzl__njqoy)
                    tzl__njqoy[t] = pvnbn__wcqg
                    uhis__zndlf[pvnbn__wcqg] = t
                jnhw__rgebh = tzl__njqoy[t]
                hfcd__rhqs.append(jnhw__rgebh)
                ugnjc__ebfp.append(ufkhs__hsea[jnhw__rgebh])
                ufkhs__hsea[jnhw__rgebh] += 1
                dawfk__hwqs[jnhw__rgebh].append(i)
        self.block_nums = hfcd__rhqs
        self.block_offsets = ugnjc__ebfp
        self.type_to_blk = tzl__njqoy
        self.blk_to_type = uhis__zndlf
        self.block_to_arr_ind = dawfk__hwqs
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
            udfd__aak = [(f'block_{i}', types.List(t)) for i, t in
                enumerate(fe_type.arr_types)]
        else:
            udfd__aak = [(f'block_{jnhw__rgebh}', types.List(t)) for t,
                jnhw__rgebh in fe_type.type_to_blk.items()]
        udfd__aak.append(('parent', types.pyobject))
        udfd__aak.append(('len', types.int64))
        super(TableTypeModel, self).__init__(dmm, fe_type, udfd__aak)


make_attribute_wrapper(TableType, 'block_0', 'block_0')
make_attribute_wrapper(TableType, 'len', '_len')


@infer_getattr
class TableTypeAttribute(OverloadedKeyAttributeTemplate):
    key = TableType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])


@unbox(TableType)
def unbox_table(typ, val, c):
    jwfu__wscww = c.pyapi.object_getattr_string(val, 'arrays')
    table = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    table.parent = cgutils.get_null_value(table.parent.type)
    zlv__urzb = c.pyapi.make_none()
    moycm__jqb = c.context.get_constant(types.int64, 0)
    nlwk__gracf = cgutils.alloca_once_value(c.builder, moycm__jqb)
    for t, jnhw__rgebh in typ.type_to_blk.items():
        ult__lqt = c.context.get_constant(types.int64, len(typ.
            block_to_arr_ind[jnhw__rgebh]))
        ijri__cluxe, akb__svx = ListInstance.allocate_ex(c.context, c.
            builder, types.List(t), ult__lqt)
        akb__svx.size = ult__lqt
        xeli__kcfq = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[jnhw__rgebh
            ], dtype=np.int64))
        pov__lveq = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, xeli__kcfq)
        with cgutils.for_range(c.builder, ult__lqt) as ouqf__xymy:
            i = ouqf__xymy.index
            jtg__egt = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), pov__lveq, i)
            pgnr__fax = c.pyapi.long_from_longlong(jtg__egt)
            rverj__vwi = c.pyapi.object_getitem(jwfu__wscww, pgnr__fax)
            nqafm__knd = c.builder.icmp_unsigned('==', rverj__vwi, zlv__urzb)
            with c.builder.if_else(nqafm__knd) as (bwr__ghoze, zlqs__lglrt):
                with bwr__ghoze:
                    yve__xbof = c.context.get_constant_null(t)
                    akb__svx.inititem(i, yve__xbof, incref=False)
                with zlqs__lglrt:
                    szqli__hswrw = c.pyapi.call_method(rverj__vwi,
                        '__len__', ())
                    hsewd__zlqx = c.pyapi.long_as_longlong(szqli__hswrw)
                    c.builder.store(hsewd__zlqx, nlwk__gracf)
                    c.pyapi.decref(szqli__hswrw)
                    arr = c.pyapi.to_native_value(t, rverj__vwi).value
                    akb__svx.inititem(i, arr, incref=False)
            c.pyapi.decref(rverj__vwi)
            c.pyapi.decref(pgnr__fax)
        setattr(table, f'block_{jnhw__rgebh}', akb__svx.value)
    table.len = c.builder.load(nlwk__gracf)
    c.pyapi.decref(jwfu__wscww)
    c.pyapi.decref(zlv__urzb)
    ncul__otq = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(table._getvalue(), is_error=ncul__otq)


@box(TableType)
def box_table(typ, val, c, ensure_unboxed=None):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    table = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ.has_runtime_cols:
        dkc__qlyw = c.context.get_constant(types.int64, 0)
        for i, t in enumerate(typ.arr_types):
            odua__xhwtm = getattr(table, f'block_{i}')
            cqx__tlfe = ListInstance(c.context, c.builder, types.List(t),
                odua__xhwtm)
            dkc__qlyw = c.builder.add(dkc__qlyw, cqx__tlfe.size)
        pmxm__sybio = c.pyapi.list_new(dkc__qlyw)
        vlwch__nwjla = c.context.get_constant(types.int64, 0)
        for i, t in enumerate(typ.arr_types):
            odua__xhwtm = getattr(table, f'block_{i}')
            cqx__tlfe = ListInstance(c.context, c.builder, types.List(t),
                odua__xhwtm)
            with cgutils.for_range(c.builder, cqx__tlfe.size) as ouqf__xymy:
                i = ouqf__xymy.index
                arr = cqx__tlfe.getitem(i)
                c.context.nrt.incref(c.builder, t, arr)
                idx = c.builder.add(vlwch__nwjla, i)
                c.pyapi.list_setitem(pmxm__sybio, idx, c.pyapi.
                    from_native_value(t, arr, c.env_manager))
            vlwch__nwjla = c.builder.add(vlwch__nwjla, cqx__tlfe.size)
        fuipp__gcydi = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
        zdt__mjrx = c.pyapi.call_function_objargs(fuipp__gcydi, (pmxm__sybio,))
        c.pyapi.decref(fuipp__gcydi)
        c.pyapi.decref(pmxm__sybio)
        c.context.nrt.decref(c.builder, typ, val)
        return zdt__mjrx
    pmxm__sybio = c.pyapi.list_new(c.context.get_constant(types.int64, len(
        typ.arr_types)))
    kpwc__kivm = cgutils.is_not_null(c.builder, table.parent)
    if ensure_unboxed is None:
        ensure_unboxed = c.context.get_constant(types.bool_, False)
    for t, jnhw__rgebh in typ.type_to_blk.items():
        odua__xhwtm = getattr(table, f'block_{jnhw__rgebh}')
        cqx__tlfe = ListInstance(c.context, c.builder, types.List(t),
            odua__xhwtm)
        xeli__kcfq = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[jnhw__rgebh
            ], dtype=np.int64))
        pov__lveq = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, xeli__kcfq)
        with cgutils.for_range(c.builder, cqx__tlfe.size) as ouqf__xymy:
            i = ouqf__xymy.index
            jtg__egt = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), pov__lveq, i)
            arr = cqx__tlfe.getitem(i)
            fbxr__ivgd = cgutils.alloca_once_value(c.builder, arr)
            zbjs__nuaq = cgutils.alloca_once_value(c.builder, c.context.
                get_constant_null(t))
            is_null = is_ll_eq(c.builder, fbxr__ivgd, zbjs__nuaq)
            with c.builder.if_else(c.builder.and_(is_null, c.builder.not_(
                ensure_unboxed))) as (bwr__ghoze, zlqs__lglrt):
                with bwr__ghoze:
                    zlv__urzb = c.pyapi.make_none()
                    c.pyapi.list_setitem(pmxm__sybio, jtg__egt, zlv__urzb)
                with zlqs__lglrt:
                    rverj__vwi = cgutils.alloca_once(c.builder, c.context.
                        get_value_type(types.pyobject))
                    with c.builder.if_else(c.builder.and_(is_null, kpwc__kivm)
                        ) as (ukpnt__jaolf, yepxe__xedql):
                        with ukpnt__jaolf:
                            wcz__pks = get_df_obj_column_codegen(c.context,
                                c.builder, c.pyapi, table.parent, jtg__egt, t)
                            c.builder.store(wcz__pks, rverj__vwi)
                        with yepxe__xedql:
                            c.context.nrt.incref(c.builder, t, arr)
                            c.builder.store(c.pyapi.from_native_value(t,
                                arr, c.env_manager), rverj__vwi)
                    c.pyapi.list_setitem(pmxm__sybio, jtg__egt, c.builder.
                        load(rverj__vwi))
    fuipp__gcydi = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
    zdt__mjrx = c.pyapi.call_function_objargs(fuipp__gcydi, (pmxm__sybio,))
    c.pyapi.decref(fuipp__gcydi)
    c.pyapi.decref(pmxm__sybio)
    c.context.nrt.decref(c.builder, typ, val)
    return zdt__mjrx


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
        tov__egune = context.get_constant(types.int64, 0)
        for i, t in enumerate(table_type.arr_types):
            odua__xhwtm = getattr(table, f'block_{i}')
            cqx__tlfe = ListInstance(context, builder, types.List(t),
                odua__xhwtm)
            tov__egune = builder.add(tov__egune, cqx__tlfe.size)
        return tov__egune
    sig = types.int64(table_type)
    return sig, codegen


def get_table_data_codegen(context, builder, table_arg, col_ind, table_type):
    arr_type = table_type.arr_types[col_ind]
    table = cgutils.create_struct_proxy(table_type)(context, builder, table_arg
        )
    jnhw__rgebh = table_type.block_nums[col_ind]
    bha__reog = table_type.block_offsets[col_ind]
    odua__xhwtm = getattr(table, f'block_{jnhw__rgebh}')
    nkw__znn = types.none(table_type, types.List(arr_type), types.int64,
        types.int64)
    zrewt__gcrv = context.get_constant(types.int64, col_ind)
    guex__vsos = context.get_constant(types.int64, bha__reog)
    sscsa__csvr = table_arg, odua__xhwtm, guex__vsos, zrewt__gcrv
    ensure_column_unboxed_codegen(context, builder, nkw__znn, sscsa__csvr)
    cqx__tlfe = ListInstance(context, builder, types.List(arr_type),
        odua__xhwtm)
    arr = cqx__tlfe.getitem(bha__reog)
    return arr


@intrinsic
def get_table_data(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, ijri__cluxe = args
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
    fih__lql = list(ind_typ.instance_type.meta)
    vhpdi__ggnq = defaultdict(list)
    for ind in fih__lql:
        vhpdi__ggnq[table_type.block_nums[ind]].append(table_type.
            block_offsets[ind])

    def codegen(context, builder, sig, args):
        table_arg, ijri__cluxe = args
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        for jnhw__rgebh, ejd__mrrd in vhpdi__ggnq.items():
            arr_type = table_type.blk_to_type[jnhw__rgebh]
            odua__xhwtm = getattr(table, f'block_{jnhw__rgebh}')
            cqx__tlfe = ListInstance(context, builder, types.List(arr_type),
                odua__xhwtm)
            yve__xbof = context.get_constant_null(arr_type)
            if len(ejd__mrrd) == 1:
                bha__reog = ejd__mrrd[0]
                arr = cqx__tlfe.getitem(bha__reog)
                context.nrt.decref(builder, arr_type, arr)
                cqx__tlfe.inititem(bha__reog, yve__xbof, incref=False)
            else:
                ult__lqt = context.get_constant(types.int64, len(ejd__mrrd))
                eja__xxaoi = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(ejd__mrrd, dtype=
                    np.int64))
                csh__egvyc = context.make_array(types.Array(types.int64, 1,
                    'C'))(context, builder, eja__xxaoi)
                with cgutils.for_range(builder, ult__lqt) as ouqf__xymy:
                    i = ouqf__xymy.index
                    bha__reog = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        csh__egvyc, i)
                    arr = cqx__tlfe.getitem(bha__reog)
                    context.nrt.decref(builder, arr_type, arr)
                    cqx__tlfe.inititem(bha__reog, yve__xbof, incref=False)
    sig = types.void(table_type, ind_typ)
    return sig, codegen


def set_table_data_codegen(context, builder, in_table_type, in_table,
    out_table_type, arr_type, arr_arg, col_ind, is_new_col):
    in_table = cgutils.create_struct_proxy(in_table_type)(context, builder,
        in_table)
    out_table = cgutils.create_struct_proxy(out_table_type)(context, builder)
    out_table.len = in_table.len
    out_table.parent = in_table.parent
    moycm__jqb = context.get_constant(types.int64, 0)
    wci__fpl = context.get_constant(types.int64, 1)
    wdj__lgkc = arr_type not in in_table_type.type_to_blk
    for t, jnhw__rgebh in out_table_type.type_to_blk.items():
        if t in in_table_type.type_to_blk:
            ern__sjzb = in_table_type.type_to_blk[t]
            akb__svx = ListInstance(context, builder, types.List(t),
                getattr(in_table, f'block_{ern__sjzb}'))
            context.nrt.incref(builder, types.List(t), akb__svx.value)
            setattr(out_table, f'block_{jnhw__rgebh}', akb__svx.value)
    if wdj__lgkc:
        ijri__cluxe, akb__svx = ListInstance.allocate_ex(context, builder,
            types.List(arr_type), wci__fpl)
        akb__svx.size = wci__fpl
        akb__svx.inititem(moycm__jqb, arr_arg, incref=True)
        jnhw__rgebh = out_table_type.type_to_blk[arr_type]
        setattr(out_table, f'block_{jnhw__rgebh}', akb__svx.value)
        if not is_new_col:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
    else:
        jnhw__rgebh = out_table_type.type_to_blk[arr_type]
        akb__svx = ListInstance(context, builder, types.List(arr_type),
            getattr(out_table, f'block_{jnhw__rgebh}'))
        if is_new_col:
            n = akb__svx.size
            sda__bpr = builder.add(n, wci__fpl)
            akb__svx.resize(sda__bpr)
            akb__svx.inititem(n, arr_arg, incref=True)
        elif arr_type == in_table_type.arr_types[col_ind]:
            cic__ops = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            akb__svx.setitem(cic__ops, arr_arg, incref=True)
        else:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
            cic__ops = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            n = akb__svx.size
            sda__bpr = builder.add(n, wci__fpl)
            akb__svx.resize(sda__bpr)
            context.nrt.incref(builder, arr_type, akb__svx.getitem(cic__ops))
            akb__svx.move(builder.add(cic__ops, wci__fpl), cic__ops,
                builder.sub(n, cic__ops))
            akb__svx.setitem(cic__ops, arr_arg, incref=True)
    return out_table._getvalue()


def _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
    context, builder):
    vpj__spa = in_table_type.arr_types[col_ind]
    if vpj__spa in out_table_type.type_to_blk:
        jnhw__rgebh = out_table_type.type_to_blk[vpj__spa]
        geswk__itig = getattr(out_table, f'block_{jnhw__rgebh}')
        pprr__oti = types.List(vpj__spa)
        cic__ops = context.get_constant(types.int64, in_table_type.
            block_offsets[col_ind])
        tgqe__jyi = pprr__oti.dtype(pprr__oti, types.intp)
        rtsk__xagbt = context.compile_internal(builder, lambda lst, i: lst.
            pop(i), tgqe__jyi, (geswk__itig, cic__ops))
        context.nrt.decref(builder, vpj__spa, rtsk__xagbt)


def generate_set_table_data_code(table, ind, arr_type, used_cols, is_null=False
    ):
    skeu__gtwhg = list(table.arr_types)
    if ind == len(skeu__gtwhg):
        jdwgw__wfir = None
        skeu__gtwhg.append(arr_type)
    else:
        jdwgw__wfir = table.arr_types[ind]
        skeu__gtwhg[ind] = arr_type
    wicmv__evqc = TableType(tuple(skeu__gtwhg))
    lrdk__eiyl = {'init_table': init_table, 'get_table_block':
        get_table_block, 'set_table_block': set_table_block,
        'set_table_len': set_table_len, 'set_table_parent':
        set_table_parent, 'alloc_list_like': alloc_list_like,
        'out_table_typ': wicmv__evqc}
    mso__cgr = 'def set_table_data(table, ind, arr, used_cols=None):\n'
    mso__cgr += f'  T2 = init_table(out_table_typ, False)\n'
    mso__cgr += f'  T2 = set_table_len(T2, len(table))\n'
    mso__cgr += f'  T2 = set_table_parent(T2, table)\n'
    for typ, jnhw__rgebh in wicmv__evqc.type_to_blk.items():
        if typ in table.type_to_blk:
            ukr__nlfom = table.type_to_blk[typ]
            mso__cgr += (
                f'  arr_list_{jnhw__rgebh} = get_table_block(table, {ukr__nlfom})\n'
                )
            mso__cgr += f"""  out_arr_list_{jnhw__rgebh} = alloc_list_like(arr_list_{jnhw__rgebh}, {len(wicmv__evqc.block_to_arr_ind[jnhw__rgebh])}, False)
"""
            if used_cols is None or set(table.block_to_arr_ind[ukr__nlfom]
                ) & used_cols:
                mso__cgr += f'  for i in range(len(arr_list_{jnhw__rgebh})):\n'
                if typ not in (jdwgw__wfir, arr_type):
                    mso__cgr += (
                        f'    out_arr_list_{jnhw__rgebh}[i] = arr_list_{jnhw__rgebh}[i]\n'
                        )
                else:
                    nttpk__sxcn = table.block_to_arr_ind[ukr__nlfom]
                    zsq__cgnt = np.empty(len(nttpk__sxcn), np.int64)
                    uecat__nnod = False
                    for hbu__rnnrt, jtg__egt in enumerate(nttpk__sxcn):
                        if jtg__egt != ind:
                            xhj__ljqz = wicmv__evqc.block_offsets[jtg__egt]
                        else:
                            xhj__ljqz = -1
                            uecat__nnod = True
                        zsq__cgnt[hbu__rnnrt] = xhj__ljqz
                    lrdk__eiyl[f'out_idxs_{jnhw__rgebh}'] = np.array(zsq__cgnt,
                        np.int64)
                    mso__cgr += f'    out_idx = out_idxs_{jnhw__rgebh}[i]\n'
                    if uecat__nnod:
                        mso__cgr += f'    if out_idx == -1:\n'
                        mso__cgr += f'      continue\n'
                    mso__cgr += f"""    out_arr_list_{jnhw__rgebh}[out_idx] = arr_list_{jnhw__rgebh}[i]
"""
            if typ == arr_type and not is_null:
                mso__cgr += f"""  out_arr_list_{jnhw__rgebh}[{wicmv__evqc.block_offsets[ind]}] = arr
"""
        else:
            lrdk__eiyl[f'arr_list_typ_{jnhw__rgebh}'] = types.List(arr_type)
            mso__cgr += f"""  out_arr_list_{jnhw__rgebh} = alloc_list_like(arr_list_typ_{jnhw__rgebh}, 1, False)
"""
            if not is_null:
                mso__cgr += f'  out_arr_list_{jnhw__rgebh}[0] = arr\n'
        mso__cgr += (
            f'  T2 = set_table_block(T2, out_arr_list_{jnhw__rgebh}, {jnhw__rgebh})\n'
            )
    mso__cgr += f'  return T2\n'
    eeoh__yyz = {}
    exec(mso__cgr, lrdk__eiyl, eeoh__yyz)
    return eeoh__yyz['set_table_data']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def set_table_data(table, ind, arr, used_cols=None):
    if is_overload_none(used_cols):
        vnkx__hrj = None
    else:
        vnkx__hrj = set(used_cols.instance_type.meta)
    hlax__toxaj = get_overload_const_int(ind)
    return generate_set_table_data_code(table, hlax__toxaj, arr, vnkx__hrj)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def set_table_data_null(table, ind, arr, used_cols=None):
    hlax__toxaj = get_overload_const_int(ind)
    arr_type = arr.instance_type
    if is_overload_none(used_cols):
        vnkx__hrj = None
    else:
        vnkx__hrj = set(used_cols.instance_type.meta)
    return generate_set_table_data_code(table, hlax__toxaj, arr_type,
        vnkx__hrj, is_null=True)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_table_data',
    'bodo.hiframes.table'] = alias_ext_dummy_func


def get_table_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    gjt__dwx = args[0]
    if equiv_set.has_shape(gjt__dwx):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            gjt__dwx)[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_get_table_data = (
    get_table_data_equiv)


@lower_constant(TableType)
def lower_constant_table(context, builder, table_type, pyval):
    wytow__lofn = []
    for t, jnhw__rgebh in table_type.type_to_blk.items():
        ywh__nwcf = len(table_type.block_to_arr_ind[jnhw__rgebh])
        dkur__ylt = []
        for i in range(ywh__nwcf):
            jtg__egt = table_type.block_to_arr_ind[jnhw__rgebh][i]
            dkur__ylt.append(pyval.arrays[jtg__egt])
        wytow__lofn.append(context.get_constant_generic(builder, types.List
            (t), dkur__ylt))
    mmpy__bigig = context.get_constant_null(types.pyobject)
    gujl__jvh = context.get_constant(types.int64, 0 if len(pyval.arrays) ==
        0 else len(pyval.arrays[0]))
    return lir.Constant.literal_struct(wytow__lofn + [mmpy__bigig, gujl__jvh])


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
        for t, jnhw__rgebh in out_table_type.type_to_blk.items():
            igz__kgp = context.get_constant_null(types.List(t))
            setattr(table, f'block_{jnhw__rgebh}', igz__kgp)
        return table._getvalue()
    sig = out_table_type(table_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def init_table_from_lists(typingctx, tuple_of_lists_type, table_type):
    assert isinstance(tuple_of_lists_type, types.BaseTuple
        ), 'Tuple of data expected'
    ykpj__gxjsu = {}
    for i, typ in enumerate(tuple_of_lists_type):
        assert isinstance(typ, types.List), 'Each tuple element must be a list'
        ykpj__gxjsu[typ.dtype] = i
    ijjl__dradl = table_type.instance_type if isinstance(table_type, types.
        TypeRef) else table_type
    assert isinstance(ijjl__dradl, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        wqhjc__wxvbu, ijri__cluxe = args
        table = cgutils.create_struct_proxy(ijjl__dradl)(context, builder)
        for t, jnhw__rgebh in ijjl__dradl.type_to_blk.items():
            idx = ykpj__gxjsu[t]
            jgtv__xmg = signature(types.List(t), tuple_of_lists_type, types
                .literal(idx))
            rdxgm__btcsf = wqhjc__wxvbu, idx
            hgh__vei = numba.cpython.tupleobj.static_getitem_tuple(context,
                builder, jgtv__xmg, rdxgm__btcsf)
            setattr(table, f'block_{jnhw__rgebh}', hgh__vei)
        return table._getvalue()
    sig = ijjl__dradl(tuple_of_lists_type, table_type)
    return sig, codegen


@intrinsic
def get_table_block(typingctx, table_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_int(blk_type)
    jnhw__rgebh = get_overload_const_int(blk_type)
    arr_type = None
    for t, sjh__nebs in table_type.type_to_blk.items():
        if sjh__nebs == jnhw__rgebh:
            arr_type = t
            break
    assert arr_type is not None, 'invalid table type block'
    qkyqm__hop = types.List(arr_type)

    def codegen(context, builder, sig, args):
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            args[0])
        odua__xhwtm = getattr(table, f'block_{jnhw__rgebh}')
        return impl_ret_borrowed(context, builder, qkyqm__hop, odua__xhwtm)
    sig = qkyqm__hop(table_type, blk_type)
    return sig, codegen


@intrinsic
def ensure_table_unboxed(typingctx, table_type, used_cols_typ):

    def codegen(context, builder, sig, args):
        table_arg, bxlfv__fflq = args
        xtoms__sek = context.get_python_api(builder)
        zra__fkiw = used_cols_typ == types.none
        if not zra__fkiw:
            wjdwz__eactk = numba.cpython.setobj.SetInstance(context,
                builder, types.Set(types.int64), bxlfv__fflq)
        table = cgutils.create_struct_proxy(sig.args[0])(context, builder,
            table_arg)
        for t, jnhw__rgebh in table_type.type_to_blk.items():
            ult__lqt = context.get_constant(types.int64, len(table_type.
                block_to_arr_ind[jnhw__rgebh]))
            xeli__kcfq = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(table_type.block_to_arr_ind[
                jnhw__rgebh], dtype=np.int64))
            pov__lveq = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, xeli__kcfq)
            odua__xhwtm = getattr(table, f'block_{jnhw__rgebh}')
            with cgutils.for_range(builder, ult__lqt) as ouqf__xymy:
                i = ouqf__xymy.index
                jtg__egt = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'), pov__lveq, i
                    )
                nkw__znn = types.none(table_type, types.List(t), types.
                    int64, types.int64)
                sscsa__csvr = table_arg, odua__xhwtm, i, jtg__egt
                if zra__fkiw:
                    ensure_column_unboxed_codegen(context, builder,
                        nkw__znn, sscsa__csvr)
                else:
                    mzb__qumm = wjdwz__eactk.contains(jtg__egt)
                    with builder.if_then(mzb__qumm):
                        ensure_column_unboxed_codegen(context, builder,
                            nkw__znn, sscsa__csvr)
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
    table_arg, zhqo__usq, pyjyd__zavhs, xte__fcqb = args
    xtoms__sek = context.get_python_api(builder)
    table = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        table_arg)
    kpwc__kivm = cgutils.is_not_null(builder, table.parent)
    cqx__tlfe = ListInstance(context, builder, sig.args[1], zhqo__usq)
    xpafp__awnt = cqx__tlfe.getitem(pyjyd__zavhs)
    fbxr__ivgd = cgutils.alloca_once_value(builder, xpafp__awnt)
    zbjs__nuaq = cgutils.alloca_once_value(builder, context.
        get_constant_null(sig.args[1].dtype))
    is_null = is_ll_eq(builder, fbxr__ivgd, zbjs__nuaq)
    with builder.if_then(is_null):
        with builder.if_else(kpwc__kivm) as (bwr__ghoze, zlqs__lglrt):
            with bwr__ghoze:
                rverj__vwi = get_df_obj_column_codegen(context, builder,
                    xtoms__sek, table.parent, xte__fcqb, sig.args[1].dtype)
                arr = xtoms__sek.to_native_value(sig.args[1].dtype, rverj__vwi
                    ).value
                cqx__tlfe.inititem(pyjyd__zavhs, arr, incref=False)
                xtoms__sek.decref(rverj__vwi)
            with zlqs__lglrt:
                context.call_conv.return_user_exc(builder, BodoError, (
                    'unexpected null table column',))


@intrinsic
def set_table_block(typingctx, table_type, arr_list_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert isinstance(arr_list_type, types.List), 'list type expected'
    assert is_overload_constant_int(blk_type), 'blk should be const int'
    jnhw__rgebh = get_overload_const_int(blk_type)

    def codegen(context, builder, sig, args):
        table_arg, ndd__lxgil, ijri__cluxe = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        setattr(in_table, f'block_{jnhw__rgebh}', ndd__lxgil)
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, arr_list_type, blk_type)
    return sig, codegen


@intrinsic
def set_table_len(typingctx, table_type, l_type):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        table_arg, sjf__pkoy = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        in_table.len = sjf__pkoy
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, l_type)
    return sig, codegen


@intrinsic
def set_table_parent(typingctx, out_table_type, in_table_type):
    assert isinstance(in_table_type, TableType), 'table type expected'
    assert isinstance(out_table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        jgek__bep, awh__ccoy = args
        in_table = cgutils.create_struct_proxy(in_table_type)(context,
            builder, awh__ccoy)
        out_table = cgutils.create_struct_proxy(out_table_type)(context,
            builder, jgek__bep)
        out_table.parent = in_table.parent
        context.nrt.incref(builder, types.pyobject, out_table.parent)
        return impl_ret_borrowed(context, builder, out_table_type,
            out_table._getvalue())
    sig = out_table_type(out_table_type, in_table_type)
    return sig, codegen


@intrinsic
def alloc_list_like(typingctx, list_type, len_type, to_str_if_dict_t):
    qkyqm__hop = list_type.instance_type if isinstance(list_type, types.TypeRef
        ) else list_type
    assert isinstance(qkyqm__hop, types.List), 'list type or typeref expected'
    assert isinstance(len_type, types.Integer), 'integer type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    if is_overload_true(to_str_if_dict_t):
        qkyqm__hop = types.List(to_str_arr_if_dict_array(qkyqm__hop.dtype))

    def codegen(context, builder, sig, args):
        cjl__btcxx = args[1]
        ijri__cluxe, akb__svx = ListInstance.allocate_ex(context, builder,
            qkyqm__hop, cjl__btcxx)
        akb__svx.size = cjl__btcxx
        return akb__svx.value
    sig = qkyqm__hop(list_type, len_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def alloc_empty_list_type(typingctx, size_typ, data_typ):
    assert isinstance(size_typ, types.Integer), 'Size must be an integer'
    swd__rqti = data_typ.instance_type if isinstance(data_typ, types.TypeRef
        ) else data_typ
    list_type = types.List(swd__rqti)

    def codegen(context, builder, sig, args):
        cjl__btcxx, ijri__cluxe = args
        ijri__cluxe, akb__svx = ListInstance.allocate_ex(context, builder,
            list_type, cjl__btcxx)
        akb__svx.size = cjl__btcxx
        return akb__svx.value
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
        qik__tmjey = numba.cpython.unicode._normalize_slice(idx, n)
        return numba.cpython.unicode._slice_span(qik__tmjey)
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_filter(T, idx, used_cols=None):
    from bodo.utils.conversion import ensure_contig_if_np
    lrdk__eiyl = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, '_get_idx_length':
        _get_idx_length, 'ensure_contig_if_np': ensure_contig_if_np}
    if not is_overload_none(used_cols):
        drp__dxqs = used_cols.instance_type
        buvxg__phxgr = np.array(drp__dxqs.meta, dtype=np.int64)
        lrdk__eiyl['used_cols_vals'] = buvxg__phxgr
        ebs__pidqp = set([T.block_nums[i] for i in buvxg__phxgr])
    else:
        buvxg__phxgr = None
    mso__cgr = 'def table_filter_func(T, idx, used_cols=None):\n'
    mso__cgr += f'  T2 = init_table(T, False)\n'
    mso__cgr += f'  l = 0\n'
    if buvxg__phxgr is not None and len(buvxg__phxgr) == 0:
        mso__cgr += f'  l = _get_idx_length(idx, len(T))\n'
        mso__cgr += f'  T2 = set_table_len(T2, l)\n'
        mso__cgr += f'  return T2\n'
        eeoh__yyz = {}
        exec(mso__cgr, lrdk__eiyl, eeoh__yyz)
        return eeoh__yyz['table_filter_func']
    if buvxg__phxgr is not None:
        mso__cgr += f'  used_set = set(used_cols_vals)\n'
    for jnhw__rgebh in T.type_to_blk.values():
        mso__cgr += (
            f'  arr_list_{jnhw__rgebh} = get_table_block(T, {jnhw__rgebh})\n')
        mso__cgr += f"""  out_arr_list_{jnhw__rgebh} = alloc_list_like(arr_list_{jnhw__rgebh}, len(arr_list_{jnhw__rgebh}), False)
"""
        if buvxg__phxgr is None or jnhw__rgebh in ebs__pidqp:
            lrdk__eiyl[f'arr_inds_{jnhw__rgebh}'] = np.array(T.
                block_to_arr_ind[jnhw__rgebh], dtype=np.int64)
            mso__cgr += f'  for i in range(len(arr_list_{jnhw__rgebh})):\n'
            mso__cgr += (
                f'    arr_ind_{jnhw__rgebh} = arr_inds_{jnhw__rgebh}[i]\n')
            if buvxg__phxgr is not None:
                mso__cgr += (
                    f'    if arr_ind_{jnhw__rgebh} not in used_set: continue\n'
                    )
            mso__cgr += f"""    ensure_column_unboxed(T, arr_list_{jnhw__rgebh}, i, arr_ind_{jnhw__rgebh})
"""
            mso__cgr += f"""    out_arr_{jnhw__rgebh} = ensure_contig_if_np(arr_list_{jnhw__rgebh}[i][idx])
"""
            mso__cgr += f'    l = len(out_arr_{jnhw__rgebh})\n'
            mso__cgr += (
                f'    out_arr_list_{jnhw__rgebh}[i] = out_arr_{jnhw__rgebh}\n')
        mso__cgr += (
            f'  T2 = set_table_block(T2, out_arr_list_{jnhw__rgebh}, {jnhw__rgebh})\n'
            )
    mso__cgr += f'  T2 = set_table_len(T2, l)\n'
    mso__cgr += f'  return T2\n'
    eeoh__yyz = {}
    exec(mso__cgr, lrdk__eiyl, eeoh__yyz)
    return eeoh__yyz['table_filter_func']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_subset(T, idx, copy_arrs, used_cols=None):
    mqse__mktw = list(idx.instance_type.meta)
    skeu__gtwhg = tuple(np.array(T.arr_types, dtype=object)[mqse__mktw])
    wicmv__evqc = TableType(skeu__gtwhg)
    if not is_overload_constant_bool(copy_arrs):
        raise_bodo_error('table_subset(): copy_arrs must be a constant')
    lhd__qyov = is_overload_true(copy_arrs)
    lrdk__eiyl = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, 'out_table_typ': wicmv__evqc}
    if not is_overload_none(used_cols):
        kept_cols = used_cols.instance_type.meta
        pbx__eniba = set(kept_cols)
        lrdk__eiyl['kept_cols'] = np.array(kept_cols, np.int64)
        blyw__kte = True
    else:
        blyw__kte = False
    zoc__hnn = {i: c for i, c in enumerate(mqse__mktw)}
    mso__cgr = 'def table_subset(T, idx, copy_arrs, used_cols=None):\n'
    mso__cgr += f'  T2 = init_table(out_table_typ, False)\n'
    mso__cgr += f'  T2 = set_table_len(T2, len(T))\n'
    if blyw__kte and len(pbx__eniba) == 0:
        mso__cgr += f'  return T2\n'
        eeoh__yyz = {}
        exec(mso__cgr, lrdk__eiyl, eeoh__yyz)
        return eeoh__yyz['table_subset']
    if blyw__kte:
        mso__cgr += f'  kept_cols_set = set(kept_cols)\n'
    for typ, jnhw__rgebh in wicmv__evqc.type_to_blk.items():
        ukr__nlfom = T.type_to_blk[typ]
        mso__cgr += (
            f'  arr_list_{jnhw__rgebh} = get_table_block(T, {ukr__nlfom})\n')
        mso__cgr += f"""  out_arr_list_{jnhw__rgebh} = alloc_list_like(arr_list_{jnhw__rgebh}, {len(wicmv__evqc.block_to_arr_ind[jnhw__rgebh])}, False)
"""
        zkhc__ikj = True
        if blyw__kte:
            hxiwj__hmya = set(wicmv__evqc.block_to_arr_ind[jnhw__rgebh])
            uwr__bwj = hxiwj__hmya & pbx__eniba
            zkhc__ikj = len(uwr__bwj) > 0
        if zkhc__ikj:
            lrdk__eiyl[f'out_arr_inds_{jnhw__rgebh}'] = np.array(wicmv__evqc
                .block_to_arr_ind[jnhw__rgebh], dtype=np.int64)
            mso__cgr += f'  for i in range(len(out_arr_list_{jnhw__rgebh})):\n'
            mso__cgr += (
                f'    out_arr_ind_{jnhw__rgebh} = out_arr_inds_{jnhw__rgebh}[i]\n'
                )
            if blyw__kte:
                mso__cgr += (
                    f'    if out_arr_ind_{jnhw__rgebh} not in kept_cols_set: continue\n'
                    )
            iempy__boitl = []
            lxq__prksn = []
            for wkxm__edm in wicmv__evqc.block_to_arr_ind[jnhw__rgebh]:
                nhcm__rehh = zoc__hnn[wkxm__edm]
                iempy__boitl.append(nhcm__rehh)
                mofcp__zrw = T.block_offsets[nhcm__rehh]
                lxq__prksn.append(mofcp__zrw)
            lrdk__eiyl[f'in_logical_idx_{jnhw__rgebh}'] = np.array(iempy__boitl
                , dtype=np.int64)
            lrdk__eiyl[f'in_physical_idx_{jnhw__rgebh}'] = np.array(lxq__prksn,
                dtype=np.int64)
            mso__cgr += (
                f'    logical_idx_{jnhw__rgebh} = in_logical_idx_{jnhw__rgebh}[i]\n'
                )
            mso__cgr += (
                f'    physical_idx_{jnhw__rgebh} = in_physical_idx_{jnhw__rgebh}[i]\n'
                )
            mso__cgr += f"""    ensure_column_unboxed(T, arr_list_{jnhw__rgebh}, physical_idx_{jnhw__rgebh}, logical_idx_{jnhw__rgebh})
"""
            wlo__cqyp = '.copy()' if lhd__qyov else ''
            mso__cgr += f"""    out_arr_list_{jnhw__rgebh}[i] = arr_list_{jnhw__rgebh}[physical_idx_{jnhw__rgebh}]{wlo__cqyp}
"""
        mso__cgr += (
            f'  T2 = set_table_block(T2, out_arr_list_{jnhw__rgebh}, {jnhw__rgebh})\n'
            )
    mso__cgr += f'  return T2\n'
    eeoh__yyz = {}
    exec(mso__cgr, lrdk__eiyl, eeoh__yyz)
    return eeoh__yyz['table_subset']


def table_filter_equiv(self, scope, equiv_set, loc, args, kws):
    gjt__dwx = args[0]
    if equiv_set.has_shape(gjt__dwx):
        if guard(is_whole_slice, self.typemap, self.func_ir, args[1]):
            return ArrayAnalysis.AnalyzeResult(shape=gjt__dwx, pre=[])
        return ArrayAnalysis.AnalyzeResult(shape=(None, equiv_set.get_shape
            (gjt__dwx)[1]), pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_table_filter = (
    table_filter_equiv)


def table_subset_equiv(self, scope, equiv_set, loc, args, kws):
    gjt__dwx = args[0]
    if equiv_set.has_shape(gjt__dwx):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            gjt__dwx)[0], None), pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_table_subset = (
    table_subset_equiv)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def decode_if_dict_table(T):
    mso__cgr = 'def impl(T):\n'
    mso__cgr += f'  T2 = init_table(T, True)\n'
    mso__cgr += f'  l = len(T)\n'
    lrdk__eiyl = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, 'decode_if_dict_array':
        decode_if_dict_array}
    for jnhw__rgebh in T.type_to_blk.values():
        lrdk__eiyl[f'arr_inds_{jnhw__rgebh}'] = np.array(T.block_to_arr_ind
            [jnhw__rgebh], dtype=np.int64)
        mso__cgr += (
            f'  arr_list_{jnhw__rgebh} = get_table_block(T, {jnhw__rgebh})\n')
        mso__cgr += f"""  out_arr_list_{jnhw__rgebh} = alloc_list_like(arr_list_{jnhw__rgebh}, len(arr_list_{jnhw__rgebh}), True)
"""
        mso__cgr += f'  for i in range(len(arr_list_{jnhw__rgebh})):\n'
        mso__cgr += f'    arr_ind_{jnhw__rgebh} = arr_inds_{jnhw__rgebh}[i]\n'
        mso__cgr += f"""    ensure_column_unboxed(T, arr_list_{jnhw__rgebh}, i, arr_ind_{jnhw__rgebh})
"""
        mso__cgr += (
            f'    out_arr_{jnhw__rgebh} = decode_if_dict_array(arr_list_{jnhw__rgebh}[i])\n'
            )
        mso__cgr += (
            f'    out_arr_list_{jnhw__rgebh}[i] = out_arr_{jnhw__rgebh}\n')
        mso__cgr += (
            f'  T2 = set_table_block(T2, out_arr_list_{jnhw__rgebh}, {jnhw__rgebh})\n'
            )
    mso__cgr += f'  T2 = set_table_len(T2, l)\n'
    mso__cgr += f'  return T2\n'
    eeoh__yyz = {}
    exec(mso__cgr, lrdk__eiyl, eeoh__yyz)
    return eeoh__yyz['impl']


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
        ltal__mlms = [arr_list_tup_typ.dtype.dtype] * len(arr_list_tup_typ)
    else:
        ltal__mlms = []
        for typ in arr_list_tup_typ:
            if typ.dtype == types.undefined:
                return
            ltal__mlms.append(typ.dtype)
    assert isinstance(nrows_typ, types.Integer
        ), 'init_runtime_table_from_lists requires an integer length'

    def codegen(context, builder, sig, args):
        ewxn__qgwfk, ewwux__ucw = args
        table = cgutils.create_struct_proxy(table_type)(context, builder)
        table.len = ewwux__ucw
        wytow__lofn = cgutils.unpack_tuple(builder, ewxn__qgwfk)
        for i, odua__xhwtm in enumerate(wytow__lofn):
            setattr(table, f'block_{i}', odua__xhwtm)
            context.nrt.incref(builder, types.List(ltal__mlms[i]), odua__xhwtm)
        return table._getvalue()
    table_type = TableType(tuple(ltal__mlms), True)
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
    lrdk__eiyl = {}
    if not is_overload_none(used_cols):
        kept_cols = set(used_cols.instance_type.meta)
        lrdk__eiyl['kept_cols'] = np.array(list(kept_cols), np.int64)
        blyw__kte = True
    else:
        kept_cols = set(np.arange(len(in_col_inds)))
        blyw__kte = False
    extra_arrs_no_series = ', '.join(f'get_series_data(extra_arrs_t[{i}])' if
        isinstance(extra_arrs_t[i], SeriesType) else f'extra_arrs_t[{i}]' for
        i in range(len(extra_arrs_t)))
    extra_arrs_no_series = (
        f"({extra_arrs_no_series}{',' if len(extra_arrs_t) == 1 else ''})")
    if isinstance(in_table_t, (types.BaseTuple, types.NoneType)):
        return _logical_tuple_table_to_table_codegen(in_table_t,
            extra_arrs_t, in_col_inds, kept_cols, n_table_cols_t,
            out_table_type_t, extra_arrs_no_series)
    ayfjc__ymt = len(in_table_t.arr_types)
    out_table_type = TableType(tuple(in_table_t.arr_types[i] if i <
        ayfjc__ymt else _to_arr_if_series(extra_arrs_t.types[i - ayfjc__ymt
        ]) for i in in_col_inds)) if is_overload_none(out_table_type_t
        ) else unwrap_typeref(out_table_type_t)
    mso__cgr = """def impl(in_table_t, extra_arrs_t, in_col_inds_t, n_table_cols_t, out_table_type_t=None, used_cols=None):
"""
    if any(isinstance(t, SeriesType) for t in extra_arrs_t.types):
        mso__cgr += f'  extra_arrs_t = {extra_arrs_no_series}\n'
    mso__cgr += f'  T1 = in_table_t\n'
    mso__cgr += f'  T2 = init_table(out_table_type, False)\n'
    mso__cgr += f'  T2 = set_table_len(T2, len(T1))\n'
    if blyw__kte and len(kept_cols) == 0:
        mso__cgr += f'  return T2\n'
        eeoh__yyz = {}
        exec(mso__cgr, lrdk__eiyl, eeoh__yyz)
        return eeoh__yyz['impl']
    if blyw__kte:
        mso__cgr += f'  kept_cols_set = set(kept_cols)\n'
    for typ, jnhw__rgebh in out_table_type.type_to_blk.items():
        lrdk__eiyl[f'arr_list_typ_{jnhw__rgebh}'] = types.List(typ)
        ult__lqt = len(out_table_type.block_to_arr_ind[jnhw__rgebh])
        mso__cgr += f"""  out_arr_list_{jnhw__rgebh} = alloc_list_like(arr_list_typ_{jnhw__rgebh}, {ult__lqt}, False)
"""
        if typ in in_table_t.type_to_blk:
            wntu__wtl = in_table_t.type_to_blk[typ]
            heyv__pht = []
            kjb__tuahs = []
            for dyzfx__jploh in out_table_type.block_to_arr_ind[jnhw__rgebh]:
                cixig__kmp = in_col_inds[dyzfx__jploh]
                if cixig__kmp < ayfjc__ymt:
                    heyv__pht.append(in_table_t.block_offsets[cixig__kmp])
                    kjb__tuahs.append(cixig__kmp)
                else:
                    heyv__pht.append(-1)
                    kjb__tuahs.append(-1)
            lrdk__eiyl[f'in_idxs_{jnhw__rgebh}'] = np.array(heyv__pht, np.int64
                )
            lrdk__eiyl[f'in_arr_inds_{jnhw__rgebh}'] = np.array(kjb__tuahs,
                np.int64)
            if blyw__kte:
                lrdk__eiyl[f'out_arr_inds_{jnhw__rgebh}'] = np.array(
                    out_table_type.block_to_arr_ind[jnhw__rgebh], dtype=np.
                    int64)
            mso__cgr += (
                f'  in_arr_list_{jnhw__rgebh} = get_table_block(T1, {wntu__wtl})\n'
                )
            mso__cgr += f'  for i in range(len(out_arr_list_{jnhw__rgebh})):\n'
            mso__cgr += (
                f'    in_offset_{jnhw__rgebh} = in_idxs_{jnhw__rgebh}[i]\n')
            mso__cgr += f'    if in_offset_{jnhw__rgebh} == -1:\n'
            mso__cgr += f'      continue\n'
            mso__cgr += (
                f'    in_arr_ind_{jnhw__rgebh} = in_arr_inds_{jnhw__rgebh}[i]\n'
                )
            if blyw__kte:
                mso__cgr += (
                    f'    if out_arr_inds_{jnhw__rgebh}[i] not in kept_cols_set: continue\n'
                    )
            mso__cgr += f"""    ensure_column_unboxed(T1, in_arr_list_{jnhw__rgebh}, in_offset_{jnhw__rgebh}, in_arr_ind_{jnhw__rgebh})
"""
            mso__cgr += f"""    out_arr_list_{jnhw__rgebh}[i] = in_arr_list_{jnhw__rgebh}[in_offset_{jnhw__rgebh}]
"""
        for i, dyzfx__jploh in enumerate(out_table_type.block_to_arr_ind[
            jnhw__rgebh]):
            if dyzfx__jploh not in kept_cols:
                continue
            cixig__kmp = in_col_inds[dyzfx__jploh]
            if cixig__kmp >= ayfjc__ymt:
                mso__cgr += f"""  out_arr_list_{jnhw__rgebh}[{i}] = extra_arrs_t[{cixig__kmp - ayfjc__ymt}]
"""
        mso__cgr += (
            f'  T2 = set_table_block(T2, out_arr_list_{jnhw__rgebh}, {jnhw__rgebh})\n'
            )
    mso__cgr += f'  return T2\n'
    lrdk__eiyl.update({'init_table': init_table, 'alloc_list_like':
        alloc_list_like, 'set_table_block': set_table_block,
        'set_table_len': set_table_len, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'out_table_type':
        out_table_type, 'get_series_data': bodo.hiframes.pd_series_ext.
        get_series_data})
    eeoh__yyz = {}
    exec(mso__cgr, lrdk__eiyl, eeoh__yyz)
    return eeoh__yyz['impl']


def _logical_tuple_table_to_table_codegen(in_table_t, extra_arrs_t,
    in_col_inds, kept_cols, n_table_cols_t, out_table_type_t,
    extra_arrs_no_series):
    ayfjc__ymt = get_overload_const_int(n_table_cols_t
        ) if is_overload_constant_int(n_table_cols_t) else len(in_table_t.types
        )
    out_table_type = TableType(tuple(in_table_t.types[i] if i < ayfjc__ymt else
        _to_arr_if_series(extra_arrs_t.types[i - ayfjc__ymt]) for i in
        in_col_inds)) if is_overload_none(out_table_type_t
        ) else unwrap_typeref(out_table_type_t)
    lcd__qgq = None
    if not is_overload_none(in_table_t):
        for i, t in enumerate(in_table_t.types):
            if t != types.none:
                lcd__qgq = f'in_table_t[{i}]'
                break
    if lcd__qgq is None:
        for i, t in enumerate(extra_arrs_t.types):
            if t != types.none:
                lcd__qgq = f'extra_arrs_t[{i}]'
                break
    assert lcd__qgq is not None, 'no array found in input data'
    mso__cgr = """def impl(in_table_t, extra_arrs_t, in_col_inds_t, n_table_cols_t, out_table_type_t=None, used_cols=None):
"""
    if any(isinstance(t, SeriesType) for t in extra_arrs_t.types):
        mso__cgr += f'  extra_arrs_t = {extra_arrs_no_series}\n'
    mso__cgr += f'  T1 = in_table_t\n'
    mso__cgr += f'  T2 = init_table(out_table_type, False)\n'
    mso__cgr += f'  T2 = set_table_len(T2, len({lcd__qgq}))\n'
    lrdk__eiyl = {}
    for typ, jnhw__rgebh in out_table_type.type_to_blk.items():
        lrdk__eiyl[f'arr_list_typ_{jnhw__rgebh}'] = types.List(typ)
        ult__lqt = len(out_table_type.block_to_arr_ind[jnhw__rgebh])
        mso__cgr += f"""  out_arr_list_{jnhw__rgebh} = alloc_list_like(arr_list_typ_{jnhw__rgebh}, {ult__lqt}, False)
"""
        for i, dyzfx__jploh in enumerate(out_table_type.block_to_arr_ind[
            jnhw__rgebh]):
            if dyzfx__jploh not in kept_cols:
                continue
            cixig__kmp = in_col_inds[dyzfx__jploh]
            if cixig__kmp < ayfjc__ymt:
                mso__cgr += (
                    f'  out_arr_list_{jnhw__rgebh}[{i}] = T1[{cixig__kmp}]\n')
            else:
                mso__cgr += f"""  out_arr_list_{jnhw__rgebh}[{i}] = extra_arrs_t[{cixig__kmp - ayfjc__ymt}]
"""
        mso__cgr += (
            f'  T2 = set_table_block(T2, out_arr_list_{jnhw__rgebh}, {jnhw__rgebh})\n'
            )
    mso__cgr += f'  return T2\n'
    lrdk__eiyl.update({'init_table': init_table, 'alloc_list_like':
        alloc_list_like, 'set_table_block': set_table_block,
        'set_table_len': set_table_len, 'out_table_type': out_table_type,
        'get_series_data': bodo.hiframes.pd_series_ext.get_series_data})
    eeoh__yyz = {}
    exec(mso__cgr, lrdk__eiyl, eeoh__yyz)
    return eeoh__yyz['impl']


def logical_table_to_table_equiv(self, scope, equiv_set, loc, args, kws):
    dzpw__rtis = args[0]
    ruxkw__wxfa = args[1]
    if equiv_set.has_shape(dzpw__rtis):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            dzpw__rtis)[0], None), pre=[])
    if equiv_set.has_shape(ruxkw__wxfa):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            ruxkw__wxfa)[0], None), pre=[])


(ArrayAnalysis._analyze_op_call_bodo_hiframes_table_logical_table_to_table
    ) = logical_table_to_table_equiv


def alias_ext_logical_table_to_table(lhs_name, args, alias_map, arg_aliases):
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['logical_table_to_table',
    'bodo.hiframes.table'] = alias_ext_logical_table_to_table
