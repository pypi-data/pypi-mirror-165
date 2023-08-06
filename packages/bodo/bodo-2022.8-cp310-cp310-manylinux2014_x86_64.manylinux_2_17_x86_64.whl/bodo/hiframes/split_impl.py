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
        zzr__dtg = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, zzr__dtg)


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
    mnvu__byhxv = context.get_value_type(str_arr_split_view_payload_type)
    tkdu__qpi = context.get_abi_sizeof(mnvu__byhxv)
    fywx__wdri = context.get_value_type(types.voidptr)
    dkw__shrb = context.get_value_type(types.uintp)
    ctr__hhn = lir.FunctionType(lir.VoidType(), [fywx__wdri, dkw__shrb,
        fywx__wdri])
    wehj__bqnoa = cgutils.get_or_insert_function(builder.module, ctr__hhn,
        name='dtor_str_arr_split_view')
    qrie__mswpf = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, tkdu__qpi), wehj__bqnoa)
    jfc__qdgo = context.nrt.meminfo_data(builder, qrie__mswpf)
    ocfby__lmq = builder.bitcast(jfc__qdgo, mnvu__byhxv.as_pointer())
    return qrie__mswpf, ocfby__lmq


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        mtq__pydkf, lzygn__rkqz = args
        qrie__mswpf, ocfby__lmq = construct_str_arr_split_view(context, builder
            )
        spmg__ftd = _get_str_binary_arr_payload(context, builder,
            mtq__pydkf, string_array_type)
        kbgc__fkn = lir.FunctionType(lir.VoidType(), [ocfby__lmq.type, lir.
            IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        gnp__sne = cgutils.get_or_insert_function(builder.module, kbgc__fkn,
            name='str_arr_split_view_impl')
        hjyfm__dhlx = context.make_helper(builder, offset_arr_type,
            spmg__ftd.offsets).data
        vzs__aar = context.make_helper(builder, char_arr_type, spmg__ftd.data
            ).data
        bgk__asz = context.make_helper(builder, null_bitmap_arr_type,
            spmg__ftd.null_bitmap).data
        bfgxx__hxi = context.get_constant(types.int8, ord(sep_typ.
            literal_value))
        builder.call(gnp__sne, [ocfby__lmq, spmg__ftd.n_arrays, hjyfm__dhlx,
            vzs__aar, bgk__asz, bfgxx__hxi])
        aljpp__zmoog = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(ocfby__lmq))
        yaqvn__vzvr = context.make_helper(builder, string_array_split_view_type
            )
        yaqvn__vzvr.num_items = spmg__ftd.n_arrays
        yaqvn__vzvr.index_offsets = aljpp__zmoog.index_offsets
        yaqvn__vzvr.data_offsets = aljpp__zmoog.data_offsets
        yaqvn__vzvr.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [mtq__pydkf])
        yaqvn__vzvr.null_bitmap = aljpp__zmoog.null_bitmap
        yaqvn__vzvr.meminfo = qrie__mswpf
        qdh__vihbq = yaqvn__vzvr._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, qdh__vihbq)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    tuubi__gcb = context.make_helper(builder, string_array_split_view_type, val
        )
    ddns__vimol = context.insert_const_string(builder.module, 'numpy')
    slxa__all = c.pyapi.import_module_noblock(ddns__vimol)
    dtype = c.pyapi.object_getattr_string(slxa__all, 'object_')
    bhfbx__ujgix = builder.sext(tuubi__gcb.num_items, c.pyapi.longlong)
    uhp__amov = c.pyapi.long_from_longlong(bhfbx__ujgix)
    yandi__yeqx = c.pyapi.call_method(slxa__all, 'ndarray', (uhp__amov, dtype))
    wkr__taheo = lir.FunctionType(lir.IntType(8).as_pointer(), [c.pyapi.
        pyobj, c.pyapi.py_ssize_t])
    jqbjv__uvq = c.pyapi._get_function(wkr__taheo, name='array_getptr1')
    gbgm__uhn = lir.FunctionType(lir.VoidType(), [c.pyapi.pyobj, lir.
        IntType(8).as_pointer(), c.pyapi.pyobj])
    uwp__ort = c.pyapi._get_function(gbgm__uhn, name='array_setitem')
    ufsy__zsca = c.pyapi.object_getattr_string(slxa__all, 'nan')
    with cgutils.for_range(builder, tuubi__gcb.num_items) as fkux__zre:
        str_ind = fkux__zre.index
        mtru__efjmi = builder.sext(builder.load(builder.gep(tuubi__gcb.
            index_offsets, [str_ind])), lir.IntType(64))
        yod__mtbjd = builder.sext(builder.load(builder.gep(tuubi__gcb.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        vwhxk__octe = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        npnbe__fctoc = builder.gep(tuubi__gcb.null_bitmap, [vwhxk__octe])
        atts__cpno = builder.load(npnbe__fctoc)
        qywrh__evvjq = builder.trunc(builder.and_(str_ind, lir.Constant(lir
            .IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(atts__cpno, qywrh__evvjq), lir.
            Constant(lir.IntType(8), 1))
        dghdw__tfp = builder.sub(yod__mtbjd, mtru__efjmi)
        dghdw__tfp = builder.sub(dghdw__tfp, dghdw__tfp.type(1))
        lxee__vdeo = builder.call(jqbjv__uvq, [yandi__yeqx, str_ind])
        bbg__yhw = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(bbg__yhw) as (pfa__wixc, hrrnz__cflas):
            with pfa__wixc:
                nerq__hey = c.pyapi.list_new(dghdw__tfp)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    nerq__hey), likely=True):
                    with cgutils.for_range(c.builder, dghdw__tfp) as fkux__zre:
                        ola__zqag = builder.add(mtru__efjmi, fkux__zre.index)
                        data_start = builder.load(builder.gep(tuubi__gcb.
                            data_offsets, [ola__zqag]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        mtndb__lah = builder.load(builder.gep(tuubi__gcb.
                            data_offsets, [builder.add(ola__zqag, ola__zqag
                            .type(1))]))
                        aiuf__zjidb = builder.gep(builder.extract_value(
                            tuubi__gcb.data, 0), [data_start])
                        pxcl__iscs = builder.sext(builder.sub(mtndb__lah,
                            data_start), lir.IntType(64))
                        snkt__ecfm = c.pyapi.string_from_string_and_size(
                            aiuf__zjidb, pxcl__iscs)
                        c.pyapi.list_setitem(nerq__hey, fkux__zre.index,
                            snkt__ecfm)
                builder.call(uwp__ort, [yandi__yeqx, lxee__vdeo, nerq__hey])
            with hrrnz__cflas:
                builder.call(uwp__ort, [yandi__yeqx, lxee__vdeo, ufsy__zsca])
    c.pyapi.decref(slxa__all)
    c.pyapi.decref(dtype)
    c.pyapi.decref(ufsy__zsca)
    return yandi__yeqx


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        wsvq__uasm, hbtbx__eje, aiuf__zjidb = args
        qrie__mswpf, ocfby__lmq = construct_str_arr_split_view(context, builder
            )
        kbgc__fkn = lir.FunctionType(lir.VoidType(), [ocfby__lmq.type, lir.
            IntType(64), lir.IntType(64)])
        gnp__sne = cgutils.get_or_insert_function(builder.module, kbgc__fkn,
            name='str_arr_split_view_alloc')
        builder.call(gnp__sne, [ocfby__lmq, wsvq__uasm, hbtbx__eje])
        aljpp__zmoog = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(ocfby__lmq))
        yaqvn__vzvr = context.make_helper(builder, string_array_split_view_type
            )
        yaqvn__vzvr.num_items = wsvq__uasm
        yaqvn__vzvr.index_offsets = aljpp__zmoog.index_offsets
        yaqvn__vzvr.data_offsets = aljpp__zmoog.data_offsets
        yaqvn__vzvr.data = aiuf__zjidb
        yaqvn__vzvr.null_bitmap = aljpp__zmoog.null_bitmap
        context.nrt.incref(builder, data_t, aiuf__zjidb)
        yaqvn__vzvr.meminfo = qrie__mswpf
        qdh__vihbq = yaqvn__vzvr._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, qdh__vihbq)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        snni__ooq, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            snni__ooq = builder.extract_value(snni__ooq, 0)
        return builder.bitcast(builder.gep(snni__ooq, [ind]), lir.IntType(8
            ).as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        snni__ooq, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            snni__ooq = builder.extract_value(snni__ooq, 0)
        return builder.load(builder.gep(snni__ooq, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        snni__ooq, ind, uiit__kzrhv = args
        hfdx__fzj = builder.gep(snni__ooq, [ind])
        builder.store(uiit__kzrhv, hfdx__fzj)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        umvu__oea, ind = args
        dhyy__zovxy = context.make_helper(builder, arr_ctypes_t, umvu__oea)
        edc__moa = context.make_helper(builder, arr_ctypes_t)
        edc__moa.data = builder.gep(dhyy__zovxy.data, [ind])
        edc__moa.meminfo = dhyy__zovxy.meminfo
        gui__znmjl = edc__moa._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, gui__znmjl)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    rjhkh__wou = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr._null_bitmap,
        item_ind)
    if not rjhkh__wou:
        return 0, 0, 0
    ola__zqag = getitem_c_arr(arr._index_offsets, item_ind)
    jztlb__qxvgy = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    vxjh__afd = jztlb__qxvgy - ola__zqag
    if str_ind >= vxjh__afd:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, ola__zqag + str_ind)
    data_start += 1
    if ola__zqag + str_ind == 0:
        data_start = 0
    mtndb__lah = getitem_c_arr(arr._data_offsets, ola__zqag + str_ind + 1)
    ouit__qgpfp = mtndb__lah - data_start
    return 1, data_start, ouit__qgpfp


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
        yxs__mfi = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            ola__zqag = getitem_c_arr(A._index_offsets, ind)
            jztlb__qxvgy = getitem_c_arr(A._index_offsets, ind + 1)
            kmnr__kabry = jztlb__qxvgy - ola__zqag - 1
            mtq__pydkf = bodo.libs.str_arr_ext.pre_alloc_string_array(
                kmnr__kabry, -1)
            for ctu__rvfa in range(kmnr__kabry):
                data_start = getitem_c_arr(A._data_offsets, ola__zqag +
                    ctu__rvfa)
                data_start += 1
                if ola__zqag + ctu__rvfa == 0:
                    data_start = 0
                mtndb__lah = getitem_c_arr(A._data_offsets, ola__zqag +
                    ctu__rvfa + 1)
                ouit__qgpfp = mtndb__lah - data_start
                hfdx__fzj = get_array_ctypes_ptr(A._data, data_start)
                aichv__rjf = bodo.libs.str_arr_ext.decode_utf8(hfdx__fzj,
                    ouit__qgpfp)
                mtq__pydkf[ctu__rvfa] = aichv__rjf
            return mtq__pydkf
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        hfu__zkfru = offset_type.bitwidth // 8

        def _impl(A, ind):
            kmnr__kabry = len(A)
            if kmnr__kabry != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            wsvq__uasm = 0
            hbtbx__eje = 0
            for ctu__rvfa in range(kmnr__kabry):
                if ind[ctu__rvfa]:
                    wsvq__uasm += 1
                    ola__zqag = getitem_c_arr(A._index_offsets, ctu__rvfa)
                    jztlb__qxvgy = getitem_c_arr(A._index_offsets, 
                        ctu__rvfa + 1)
                    hbtbx__eje += jztlb__qxvgy - ola__zqag
            yandi__yeqx = pre_alloc_str_arr_view(wsvq__uasm, hbtbx__eje, A.
                _data)
            item_ind = 0
            xdp__qspmq = 0
            for ctu__rvfa in range(kmnr__kabry):
                if ind[ctu__rvfa]:
                    ola__zqag = getitem_c_arr(A._index_offsets, ctu__rvfa)
                    jztlb__qxvgy = getitem_c_arr(A._index_offsets, 
                        ctu__rvfa + 1)
                    kbj__bfgm = jztlb__qxvgy - ola__zqag
                    setitem_c_arr(yandi__yeqx._index_offsets, item_ind,
                        xdp__qspmq)
                    hfdx__fzj = get_c_arr_ptr(A._data_offsets, ola__zqag)
                    hkh__apxv = get_c_arr_ptr(yandi__yeqx._data_offsets,
                        xdp__qspmq)
                    _memcpy(hkh__apxv, hfdx__fzj, kbj__bfgm, hfu__zkfru)
                    rjhkh__wou = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, ctu__rvfa)
                    bodo.libs.int_arr_ext.set_bit_to_arr(yandi__yeqx.
                        _null_bitmap, item_ind, rjhkh__wou)
                    item_ind += 1
                    xdp__qspmq += kbj__bfgm
            setitem_c_arr(yandi__yeqx._index_offsets, item_ind, xdp__qspmq)
            return yandi__yeqx
        return _impl
