import operator
import llvmlite.binding as ll
import numba
import numba.core.typing.typeof
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, impl_ret_new_ref
from numba.extending import box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, register_model
import bodo
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import offset_type
from bodo.libs.str_arr_ext import _get_str_binary_arr_payload, _memcpy, char_arr_type, get_data_ptr, null_bitmap_arr_type, offset_arr_type, string_array_type
ll.add_symbol('array_setitem', hstr_ext.array_setitem)
ll.add_symbol('array_getptr1', hstr_ext.array_getptr1)
ll.add_symbol('dtor_str_arr_split_view', hstr_ext.dtor_str_arr_split_view)
ll.add_symbol('str_arr_split_view_impl', hstr_ext.str_arr_split_view_impl)
ll.add_symbol('str_arr_split_view_alloc', hstr_ext.str_arr_split_view_alloc)
char_typ = types.uint8
data_ctypes_type = types.ArrayCTypes(types.Array(char_typ, 1, 'C'))
offset_ctypes_type = types.ArrayCTypes(types.Array(offset_type, 1, 'C'))


class StringArraySplitViewType(types.ArrayCompatible):

    def __init__(self):
        super(StringArraySplitViewType, self).__init__(name=
            'StringArraySplitViewType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_array_type

    def copy(self):
        return StringArraySplitViewType()


string_array_split_view_type = StringArraySplitViewType()


class StringArraySplitViewPayloadType(types.Type):

    def __init__(self):
        super(StringArraySplitViewPayloadType, self).__init__(name=
            'StringArraySplitViewPayloadType()')


str_arr_split_view_payload_type = StringArraySplitViewPayloadType()


@register_model(StringArraySplitViewPayloadType)
class StringArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nvdq__bkfl = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, nvdq__bkfl)


str_arr_model_members = [('num_items', types.uint64), ('index_offsets',
    types.CPointer(offset_type)), ('data_offsets', types.CPointer(
    offset_type)), ('data', data_ctypes_type), ('null_bitmap', types.
    CPointer(char_typ)), ('meminfo', types.MemInfoPointer(
    str_arr_split_view_payload_type))]


@register_model(StringArraySplitViewType)
class StringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        models.StructModel.__init__(self, dmm, fe_type, str_arr_model_members)


make_attribute_wrapper(StringArraySplitViewType, 'num_items', '_num_items')
make_attribute_wrapper(StringArraySplitViewType, 'index_offsets',
    '_index_offsets')
make_attribute_wrapper(StringArraySplitViewType, 'data_offsets',
    '_data_offsets')
make_attribute_wrapper(StringArraySplitViewType, 'data', '_data')
make_attribute_wrapper(StringArraySplitViewType, 'null_bitmap', '_null_bitmap')


def construct_str_arr_split_view(context, builder):
    yvr__lwl = context.get_value_type(str_arr_split_view_payload_type)
    mojh__yeq = context.get_abi_sizeof(yvr__lwl)
    zspe__gyxv = context.get_value_type(types.voidptr)
    gbs__yre = context.get_value_type(types.uintp)
    ihver__vop = lir.FunctionType(lir.VoidType(), [zspe__gyxv, gbs__yre,
        zspe__gyxv])
    aaxq__ovhnv = cgutils.get_or_insert_function(builder.module, ihver__vop,
        name='dtor_str_arr_split_view')
    daveu__cgu = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, mojh__yeq), aaxq__ovhnv)
    awpxw__qosy = context.nrt.meminfo_data(builder, daveu__cgu)
    hluvr__awaui = builder.bitcast(awpxw__qosy, yvr__lwl.as_pointer())
    return daveu__cgu, hluvr__awaui


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        wozd__cvh, sptgj__puwbj = args
        daveu__cgu, hluvr__awaui = construct_str_arr_split_view(context,
            builder)
        pha__teslo = _get_str_binary_arr_payload(context, builder,
            wozd__cvh, string_array_type)
        tar__pgy = lir.FunctionType(lir.VoidType(), [hluvr__awaui.type, lir
            .IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        vgp__crpo = cgutils.get_or_insert_function(builder.module, tar__pgy,
            name='str_arr_split_view_impl')
        whvi__qimdn = context.make_helper(builder, offset_arr_type,
            pha__teslo.offsets).data
        swvm__qtj = context.make_helper(builder, char_arr_type, pha__teslo.data
            ).data
        jusnt__ofmb = context.make_helper(builder, null_bitmap_arr_type,
            pha__teslo.null_bitmap).data
        fdba__gxf = context.get_constant(types.int8, ord(sep_typ.literal_value)
            )
        builder.call(vgp__crpo, [hluvr__awaui, pha__teslo.n_arrays,
            whvi__qimdn, swvm__qtj, jusnt__ofmb, fdba__gxf])
        kou__wdbl = cgutils.create_struct_proxy(str_arr_split_view_payload_type
            )(context, builder, value=builder.load(hluvr__awaui))
        ykrv__agca = context.make_helper(builder, string_array_split_view_type)
        ykrv__agca.num_items = pha__teslo.n_arrays
        ykrv__agca.index_offsets = kou__wdbl.index_offsets
        ykrv__agca.data_offsets = kou__wdbl.data_offsets
        ykrv__agca.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [wozd__cvh])
        ykrv__agca.null_bitmap = kou__wdbl.null_bitmap
        ykrv__agca.meminfo = daveu__cgu
        zek__foiy = ykrv__agca._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, zek__foiy)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    gabk__rjgt = context.make_helper(builder, string_array_split_view_type, val
        )
    ipg__jbid = context.insert_const_string(builder.module, 'numpy')
    cnpfp__owi = c.pyapi.import_module_noblock(ipg__jbid)
    dtype = c.pyapi.object_getattr_string(cnpfp__owi, 'object_')
    fiwi__gcwqb = builder.sext(gabk__rjgt.num_items, c.pyapi.longlong)
    eoe__bnrom = c.pyapi.long_from_longlong(fiwi__gcwqb)
    fvyn__disd = c.pyapi.call_method(cnpfp__owi, 'ndarray', (eoe__bnrom, dtype)
        )
    zjlcu__ayek = lir.FunctionType(lir.IntType(8).as_pointer(), [c.pyapi.
        pyobj, c.pyapi.py_ssize_t])
    jttm__rtr = c.pyapi._get_function(zjlcu__ayek, name='array_getptr1')
    akml__igtu = lir.FunctionType(lir.VoidType(), [c.pyapi.pyobj, lir.
        IntType(8).as_pointer(), c.pyapi.pyobj])
    gkgc__ubcd = c.pyapi._get_function(akml__igtu, name='array_setitem')
    hakgf__lpmx = c.pyapi.object_getattr_string(cnpfp__owi, 'nan')
    with cgutils.for_range(builder, gabk__rjgt.num_items) as xgkai__yxvz:
        str_ind = xgkai__yxvz.index
        itg__yyml = builder.sext(builder.load(builder.gep(gabk__rjgt.
            index_offsets, [str_ind])), lir.IntType(64))
        fvf__jedqg = builder.sext(builder.load(builder.gep(gabk__rjgt.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        uhhw__alubd = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        ftpk__vsjzl = builder.gep(gabk__rjgt.null_bitmap, [uhhw__alubd])
        rfyj__okqt = builder.load(ftpk__vsjzl)
        gckxa__wijfm = builder.trunc(builder.and_(str_ind, lir.Constant(lir
            .IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(rfyj__okqt, gckxa__wijfm), lir.
            Constant(lir.IntType(8), 1))
        wvf__bxsxs = builder.sub(fvf__jedqg, itg__yyml)
        wvf__bxsxs = builder.sub(wvf__bxsxs, wvf__bxsxs.type(1))
        yduw__qhmjw = builder.call(jttm__rtr, [fvyn__disd, str_ind])
        mrsb__eqc = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(mrsb__eqc) as (huy__fwo, iiboq__qox):
            with huy__fwo:
                ctr__xjvnu = c.pyapi.list_new(wvf__bxsxs)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    ctr__xjvnu), likely=True):
                    with cgutils.for_range(c.builder, wvf__bxsxs
                        ) as xgkai__yxvz:
                        cwyq__skwff = builder.add(itg__yyml, xgkai__yxvz.index)
                        data_start = builder.load(builder.gep(gabk__rjgt.
                            data_offsets, [cwyq__skwff]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        qgas__hgshd = builder.load(builder.gep(gabk__rjgt.
                            data_offsets, [builder.add(cwyq__skwff,
                            cwyq__skwff.type(1))]))
                        vqlb__gjn = builder.gep(builder.extract_value(
                            gabk__rjgt.data, 0), [data_start])
                        hkc__mdy = builder.sext(builder.sub(qgas__hgshd,
                            data_start), lir.IntType(64))
                        uspyk__fqspj = c.pyapi.string_from_string_and_size(
                            vqlb__gjn, hkc__mdy)
                        c.pyapi.list_setitem(ctr__xjvnu, xgkai__yxvz.index,
                            uspyk__fqspj)
                builder.call(gkgc__ubcd, [fvyn__disd, yduw__qhmjw, ctr__xjvnu])
            with iiboq__qox:
                builder.call(gkgc__ubcd, [fvyn__disd, yduw__qhmjw, hakgf__lpmx]
                    )
    c.pyapi.decref(cnpfp__owi)
    c.pyapi.decref(dtype)
    c.pyapi.decref(hakgf__lpmx)
    return fvyn__disd


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        vbiyj__gku, cgk__elw, vqlb__gjn = args
        daveu__cgu, hluvr__awaui = construct_str_arr_split_view(context,
            builder)
        tar__pgy = lir.FunctionType(lir.VoidType(), [hluvr__awaui.type, lir
            .IntType(64), lir.IntType(64)])
        vgp__crpo = cgutils.get_or_insert_function(builder.module, tar__pgy,
            name='str_arr_split_view_alloc')
        builder.call(vgp__crpo, [hluvr__awaui, vbiyj__gku, cgk__elw])
        kou__wdbl = cgutils.create_struct_proxy(str_arr_split_view_payload_type
            )(context, builder, value=builder.load(hluvr__awaui))
        ykrv__agca = context.make_helper(builder, string_array_split_view_type)
        ykrv__agca.num_items = vbiyj__gku
        ykrv__agca.index_offsets = kou__wdbl.index_offsets
        ykrv__agca.data_offsets = kou__wdbl.data_offsets
        ykrv__agca.data = vqlb__gjn
        ykrv__agca.null_bitmap = kou__wdbl.null_bitmap
        context.nrt.incref(builder, data_t, vqlb__gjn)
        ykrv__agca.meminfo = daveu__cgu
        zek__foiy = ykrv__agca._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, zek__foiy)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        sax__bowak, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            sax__bowak = builder.extract_value(sax__bowak, 0)
        return builder.bitcast(builder.gep(sax__bowak, [ind]), lir.IntType(
            8).as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        sax__bowak, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            sax__bowak = builder.extract_value(sax__bowak, 0)
        return builder.load(builder.gep(sax__bowak, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        sax__bowak, ind, pamga__dfv = args
        hzz__hvn = builder.gep(sax__bowak, [ind])
        builder.store(pamga__dfv, hzz__hvn)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        uzzi__zncqj, ind = args
        rpjji__ntatg = context.make_helper(builder, arr_ctypes_t, uzzi__zncqj)
        wfwcp__gthdq = context.make_helper(builder, arr_ctypes_t)
        wfwcp__gthdq.data = builder.gep(rpjji__ntatg.data, [ind])
        wfwcp__gthdq.meminfo = rpjji__ntatg.meminfo
        nrlt__uyji = wfwcp__gthdq._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, nrlt__uyji)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    olgs__mrsvl = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr._null_bitmap,
        item_ind)
    if not olgs__mrsvl:
        return 0, 0, 0
    cwyq__skwff = getitem_c_arr(arr._index_offsets, item_ind)
    lwida__zaur = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    worb__xppzn = lwida__zaur - cwyq__skwff
    if str_ind >= worb__xppzn:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, cwyq__skwff + str_ind)
    data_start += 1
    if cwyq__skwff + str_ind == 0:
        data_start = 0
    qgas__hgshd = getitem_c_arr(arr._data_offsets, cwyq__skwff + str_ind + 1)
    mcyj__gjbdf = qgas__hgshd - data_start
    return 1, data_start, mcyj__gjbdf


@numba.njit(no_cpython_wrapper=True)
def get_split_view_data_ptr(arr, data_start):
    return get_array_ctypes_ptr(arr._data, data_start)


@overload(len, no_unliteral=True)
def str_arr_split_view_len_overload(arr):
    if arr == string_array_split_view_type:
        return lambda arr: np.int64(arr._num_items)


@overload_attribute(StringArraySplitViewType, 'shape')
def overload_split_view_arr_shape(A):
    return lambda A: (np.int64(A._num_items),)


@overload(operator.getitem, no_unliteral=True)
def str_arr_split_view_getitem_overload(A, ind):
    if A != string_array_split_view_type:
        return
    if A == string_array_split_view_type and isinstance(ind, types.Integer):
        ukqf__kjy = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            cwyq__skwff = getitem_c_arr(A._index_offsets, ind)
            lwida__zaur = getitem_c_arr(A._index_offsets, ind + 1)
            urh__wwd = lwida__zaur - cwyq__skwff - 1
            wozd__cvh = bodo.libs.str_arr_ext.pre_alloc_string_array(urh__wwd,
                -1)
            for xsavp__lefho in range(urh__wwd):
                data_start = getitem_c_arr(A._data_offsets, cwyq__skwff +
                    xsavp__lefho)
                data_start += 1
                if cwyq__skwff + xsavp__lefho == 0:
                    data_start = 0
                qgas__hgshd = getitem_c_arr(A._data_offsets, cwyq__skwff +
                    xsavp__lefho + 1)
                mcyj__gjbdf = qgas__hgshd - data_start
                hzz__hvn = get_array_ctypes_ptr(A._data, data_start)
                egixm__iwwvr = bodo.libs.str_arr_ext.decode_utf8(hzz__hvn,
                    mcyj__gjbdf)
                wozd__cvh[xsavp__lefho] = egixm__iwwvr
            return wozd__cvh
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        wfyqc__dpau = offset_type.bitwidth // 8

        def _impl(A, ind):
            urh__wwd = len(A)
            if urh__wwd != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            vbiyj__gku = 0
            cgk__elw = 0
            for xsavp__lefho in range(urh__wwd):
                if ind[xsavp__lefho]:
                    vbiyj__gku += 1
                    cwyq__skwff = getitem_c_arr(A._index_offsets, xsavp__lefho)
                    lwida__zaur = getitem_c_arr(A._index_offsets, 
                        xsavp__lefho + 1)
                    cgk__elw += lwida__zaur - cwyq__skwff
            fvyn__disd = pre_alloc_str_arr_view(vbiyj__gku, cgk__elw, A._data)
            item_ind = 0
            psyti__ckod = 0
            for xsavp__lefho in range(urh__wwd):
                if ind[xsavp__lefho]:
                    cwyq__skwff = getitem_c_arr(A._index_offsets, xsavp__lefho)
                    lwida__zaur = getitem_c_arr(A._index_offsets, 
                        xsavp__lefho + 1)
                    iina__bbh = lwida__zaur - cwyq__skwff
                    setitem_c_arr(fvyn__disd._index_offsets, item_ind,
                        psyti__ckod)
                    hzz__hvn = get_c_arr_ptr(A._data_offsets, cwyq__skwff)
                    diola__uql = get_c_arr_ptr(fvyn__disd._data_offsets,
                        psyti__ckod)
                    _memcpy(diola__uql, hzz__hvn, iina__bbh, wfyqc__dpau)
                    olgs__mrsvl = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, xsavp__lefho)
                    bodo.libs.int_arr_ext.set_bit_to_arr(fvyn__disd.
                        _null_bitmap, item_ind, olgs__mrsvl)
                    item_ind += 1
                    psyti__ckod += iina__bbh
            setitem_c_arr(fvyn__disd._index_offsets, item_ind, psyti__ckod)
            return fvyn__disd
        return _impl
