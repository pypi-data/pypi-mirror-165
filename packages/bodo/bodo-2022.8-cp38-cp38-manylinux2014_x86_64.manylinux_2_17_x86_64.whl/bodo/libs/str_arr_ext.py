"""Array implementation for string objects, which are usually immutable.
The characters are stored in a contingous data array, and an offsets array marks the
the individual strings. For example:
value:             ['a', 'bc', '', 'abc', None, 'bb']
data:              [a, b, c, a, b, c, b, b]
offsets:           [0, 1, 3, 3, 6, 6, 8]
"""
import glob
import operator
import numba
import numba.core.typing.typeof
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.unsafe.bytes import memcpy_region
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, type_callable, typeof_impl, unbox
import bodo
from bodo.libs.array_item_arr_ext import ArrayItemArrayPayloadType, ArrayItemArrayType, _get_array_item_arr_payload, np_offset_type, offset_type
from bodo.libs.binary_arr_ext import BinaryArrayType, binary_array_type, pre_alloc_binary_array
from bodo.libs.str_ext import memcmp, string_type, unicode_to_utf8_and_len
from bodo.utils.typing import BodoArrayIterator, BodoError, decode_if_dict_array, is_list_like_index_type, is_overload_constant_int, is_overload_none, is_overload_true, is_str_arr_type, parse_dtype, raise_bodo_error
use_pd_string_array = False
char_type = types.uint8
char_arr_type = types.Array(char_type, 1, 'C')
offset_arr_type = types.Array(offset_type, 1, 'C')
null_bitmap_arr_type = types.Array(types.uint8, 1, 'C')
data_ctypes_type = types.ArrayCTypes(char_arr_type)
offset_ctypes_type = types.ArrayCTypes(offset_arr_type)


class StringArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self):
        super(StringArrayType, self).__init__(name='StringArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_type

    @property
    def iterator_type(self):
        return BodoArrayIterator(self)

    def copy(self):
        return StringArrayType()


string_array_type = StringArrayType()


@typeof_impl.register(pd.arrays.StringArray)
def typeof_string_array(val, c):
    return string_array_type


@register_model(BinaryArrayType)
@register_model(StringArrayType)
class StringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        akz__rrhav = ArrayItemArrayType(char_arr_type)
        vxtt__aeiho = [('data', akz__rrhav)]
        models.StructModel.__init__(self, dmm, fe_type, vxtt__aeiho)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')
lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        bmsw__xoqb, = args
        ecucp__phjzp = context.make_helper(builder, string_array_type)
        ecucp__phjzp.data = bmsw__xoqb
        context.nrt.incref(builder, data_typ, bmsw__xoqb)
        return ecucp__phjzp._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    kwwh__scm = c.context.insert_const_string(c.builder.module, 'pandas')
    muuna__oucr = c.pyapi.import_module_noblock(kwwh__scm)
    mfl__vnvy = c.pyapi.call_method(muuna__oucr, 'StringDtype', ())
    c.pyapi.decref(muuna__oucr)
    return mfl__vnvy


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        tiq__dnxi = bodo.libs.dict_arr_ext.get_binary_op_overload(op, lhs, rhs)
        if tiq__dnxi is not None:
            return tiq__dnxi
        if is_str_arr_type(lhs) and is_str_arr_type(rhs):

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                kgda__banxu = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(kgda__banxu)
                for i in numba.parfors.parfor.internal_prange(kgda__banxu):
                    if bodo.libs.array_kernels.isna(lhs, i
                        ) or bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs[i], rhs[i])
                    out_arr[i] = val
                return out_arr
            return impl_both
        if is_str_arr_type(lhs) and types.unliteral(rhs) == string_type:

            def impl_left(lhs, rhs):
                numba.parfors.parfor.init_prange()
                kgda__banxu = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(kgda__banxu)
                for i in numba.parfors.parfor.internal_prange(kgda__banxu):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs[i], rhs)
                    out_arr[i] = val
                return out_arr
            return impl_left
        if types.unliteral(lhs) == string_type and is_str_arr_type(rhs):

            def impl_right(lhs, rhs):
                numba.parfors.parfor.init_prange()
                kgda__banxu = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(kgda__banxu)
                for i in numba.parfors.parfor.internal_prange(kgda__banxu):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs, rhs[i])
                    out_arr[i] = val
                return out_arr
            return impl_right
        raise_bodo_error(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_string_array_binary_op


def overload_add_operator_string_array(lhs, rhs):
    xdlgm__euv = is_str_arr_type(lhs) or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    kwi__hpbq = is_str_arr_type(rhs) or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if is_str_arr_type(lhs) and kwi__hpbq or xdlgm__euv and is_str_arr_type(rhs
        ):

        def impl_both(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j
                    ) or bodo.libs.array_kernels.isna(rhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] + rhs[j]
            return out_arr
        return impl_both
    if is_str_arr_type(lhs) and types.unliteral(rhs) == string_type:

        def impl_left(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] + rhs
            return out_arr
        return impl_left
    if types.unliteral(lhs) == string_type and is_str_arr_type(rhs):

        def impl_right(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(rhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(rhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs + rhs[j]
            return out_arr
        return impl_right


def overload_mul_operator_str_arr(lhs, rhs):
    if is_str_arr_type(lhs) and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] * rhs
            return out_arr
        return impl
    if isinstance(lhs, types.Integer) and is_str_arr_type(rhs):

        def impl(lhs, rhs):
            return rhs * lhs
        return impl


def _get_str_binary_arr_payload(context, builder, arr_value, arr_typ):
    assert arr_typ == string_array_type or arr_typ == binary_array_type
    ajs__xowx = context.make_helper(builder, arr_typ, arr_value)
    akz__rrhav = ArrayItemArrayType(char_arr_type)
    gwsn__tbyqr = _get_array_item_arr_payload(context, builder, akz__rrhav,
        ajs__xowx.data)
    return gwsn__tbyqr


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        gwsn__tbyqr = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        return gwsn__tbyqr.n_arrays
    return types.int64(string_array_type), codegen


def _get_num_total_chars(builder, offsets, num_strings):
    return builder.zext(builder.load(builder.gep(offsets, [num_strings])),
        lir.IntType(64))


@intrinsic
def num_total_chars(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        gwsn__tbyqr = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        gola__xwn = context.make_helper(builder, offset_arr_type,
            gwsn__tbyqr.offsets).data
        return _get_num_total_chars(builder, gola__xwn, gwsn__tbyqr.n_arrays)
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        gwsn__tbyqr = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        uxdv__aeo = context.make_helper(builder, offset_arr_type,
            gwsn__tbyqr.offsets)
        yhto__hil = context.make_helper(builder, offset_ctypes_type)
        yhto__hil.data = builder.bitcast(uxdv__aeo.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        yhto__hil.meminfo = uxdv__aeo.meminfo
        mfl__vnvy = yhto__hil._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            mfl__vnvy)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        gwsn__tbyqr = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        bmsw__xoqb = context.make_helper(builder, char_arr_type,
            gwsn__tbyqr.data)
        yhto__hil = context.make_helper(builder, data_ctypes_type)
        yhto__hil.data = bmsw__xoqb.data
        yhto__hil.meminfo = bmsw__xoqb.meminfo
        mfl__vnvy = yhto__hil._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, mfl__vnvy)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        bvivd__dxc, ind = args
        gwsn__tbyqr = _get_str_binary_arr_payload(context, builder,
            bvivd__dxc, sig.args[0])
        bmsw__xoqb = context.make_helper(builder, char_arr_type,
            gwsn__tbyqr.data)
        yhto__hil = context.make_helper(builder, data_ctypes_type)
        yhto__hil.data = builder.gep(bmsw__xoqb.data, [ind])
        yhto__hil.meminfo = bmsw__xoqb.meminfo
        mfl__vnvy = yhto__hil._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, mfl__vnvy)
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        qhafq__txcf, mgf__otx, vzsez__yrr, wzmjp__qhcx = args
        hfjaz__oon = builder.bitcast(builder.gep(qhafq__txcf, [mgf__otx]),
            lir.IntType(8).as_pointer())
        nqree__ffzs = builder.bitcast(builder.gep(vzsez__yrr, [wzmjp__qhcx]
            ), lir.IntType(8).as_pointer())
        ccen__vkn = builder.load(nqree__ffzs)
        builder.store(ccen__vkn, hfjaz__oon)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        gwsn__tbyqr = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        ssmpv__hxfdh = context.make_helper(builder, null_bitmap_arr_type,
            gwsn__tbyqr.null_bitmap)
        yhto__hil = context.make_helper(builder, data_ctypes_type)
        yhto__hil.data = ssmpv__hxfdh.data
        yhto__hil.meminfo = ssmpv__hxfdh.meminfo
        mfl__vnvy = yhto__hil._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, mfl__vnvy)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        gwsn__tbyqr = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        gola__xwn = context.make_helper(builder, offset_arr_type,
            gwsn__tbyqr.offsets).data
        return builder.load(builder.gep(gola__xwn, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        gwsn__tbyqr = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, gwsn__tbyqr
            .offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        kwz__twj, ind = args
        if in_bitmap_typ == data_ctypes_type:
            yhto__hil = context.make_helper(builder, data_ctypes_type, kwz__twj
                )
            kwz__twj = yhto__hil.data
        return builder.load(builder.gep(kwz__twj, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        kwz__twj, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            yhto__hil = context.make_helper(builder, data_ctypes_type, kwz__twj
                )
            kwz__twj = yhto__hil.data
        builder.store(val, builder.gep(kwz__twj, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        vuq__rdjx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        duzl__kwx = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        orpgi__zawra = context.make_helper(builder, offset_arr_type,
            vuq__rdjx.offsets).data
        cbov__andl = context.make_helper(builder, offset_arr_type,
            duzl__kwx.offsets).data
        csog__tvsbg = context.make_helper(builder, char_arr_type, vuq__rdjx
            .data).data
        cwy__pzoa = context.make_helper(builder, char_arr_type, duzl__kwx.data
            ).data
        szgf__tes = context.make_helper(builder, null_bitmap_arr_type,
            vuq__rdjx.null_bitmap).data
        oxvc__jrq = context.make_helper(builder, null_bitmap_arr_type,
            duzl__kwx.null_bitmap).data
        xvuc__kad = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, cbov__andl, orpgi__zawra, xvuc__kad)
        cgutils.memcpy(builder, cwy__pzoa, csog__tvsbg, builder.load(
            builder.gep(orpgi__zawra, [ind])))
        ouk__arizw = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        pcjmd__jzff = builder.lshr(ouk__arizw, lir.Constant(lir.IntType(64), 3)
            )
        cgutils.memcpy(builder, oxvc__jrq, szgf__tes, pcjmd__jzff)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        vuq__rdjx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        duzl__kwx = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        orpgi__zawra = context.make_helper(builder, offset_arr_type,
            vuq__rdjx.offsets).data
        csog__tvsbg = context.make_helper(builder, char_arr_type, vuq__rdjx
            .data).data
        cwy__pzoa = context.make_helper(builder, char_arr_type, duzl__kwx.data
            ).data
        num_total_chars = _get_num_total_chars(builder, orpgi__zawra,
            vuq__rdjx.n_arrays)
        cgutils.memcpy(builder, cwy__pzoa, csog__tvsbg, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        vuq__rdjx = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        duzl__kwx = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        orpgi__zawra = context.make_helper(builder, offset_arr_type,
            vuq__rdjx.offsets).data
        cbov__andl = context.make_helper(builder, offset_arr_type,
            duzl__kwx.offsets).data
        szgf__tes = context.make_helper(builder, null_bitmap_arr_type,
            vuq__rdjx.null_bitmap).data
        kgda__banxu = vuq__rdjx.n_arrays
        qcvkd__ytgz = context.get_constant(offset_type, 0)
        nkmk__lexn = cgutils.alloca_once_value(builder, qcvkd__ytgz)
        with cgutils.for_range(builder, kgda__banxu) as iqef__epjev:
            kohfx__irp = lower_is_na(context, builder, szgf__tes,
                iqef__epjev.index)
            with cgutils.if_likely(builder, builder.not_(kohfx__irp)):
                dpnm__stsjg = builder.load(builder.gep(orpgi__zawra, [
                    iqef__epjev.index]))
                ahlf__yceg = builder.load(nkmk__lexn)
                builder.store(dpnm__stsjg, builder.gep(cbov__andl, [
                    ahlf__yceg]))
                builder.store(builder.add(ahlf__yceg, lir.Constant(context.
                    get_value_type(offset_type), 1)), nkmk__lexn)
        ahlf__yceg = builder.load(nkmk__lexn)
        dpnm__stsjg = builder.load(builder.gep(orpgi__zawra, [kgda__banxu]))
        builder.store(dpnm__stsjg, builder.gep(cbov__andl, [ahlf__yceg]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        bnk__hhxrm, ind, str, nttrm__dzwd = args
        bnk__hhxrm = context.make_array(sig.args[0])(context, builder,
            bnk__hhxrm)
        xxwa__nuh = builder.gep(bnk__hhxrm.data, [ind])
        cgutils.raw_memcpy(builder, xxwa__nuh, str, nttrm__dzwd, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        xxwa__nuh, ind, hbtzh__lxmi, nttrm__dzwd = args
        xxwa__nuh = builder.gep(xxwa__nuh, [ind])
        cgutils.raw_memcpy(builder, xxwa__nuh, hbtzh__lxmi, nttrm__dzwd, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.generated_jit(nopython=True)
def get_str_arr_item_length(A, i):
    if A == bodo.dict_str_arr_type:

        def impl(A, i):
            idx = A._indices[i]
            jdi__lrfiy = A._data
            return np.int64(getitem_str_offset(jdi__lrfiy, idx + 1) -
                getitem_str_offset(jdi__lrfiy, idx))
        return impl
    else:
        return lambda A, i: np.int64(getitem_str_offset(A, i + 1) -
            getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_str_length(A, i):
    ctcxy__frnli = np.int64(getitem_str_offset(A, i))
    usjbo__thfkt = np.int64(getitem_str_offset(A, i + 1))
    l = usjbo__thfkt - ctcxy__frnli
    xywml__ixie = get_data_ptr_ind(A, ctcxy__frnli)
    for j in range(l):
        if bodo.hiframes.split_impl.getitem_c_arr(xywml__ixie, j) >= 128:
            return len(A[i])
    return l


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_ptr(A, i):
    return get_data_ptr_ind(A, getitem_str_offset(A, i))


@numba.generated_jit(no_cpython_wrapper=True, nopython=True)
def get_str_arr_item_copy(B, j, A, i):
    if B != string_array_type:
        raise BodoError(
            'get_str_arr_item_copy(): Output array must be a string array')
    if not is_str_arr_type(A):
        raise BodoError(
            'get_str_arr_item_copy(): Input array must be a string array or dictionary encoded array'
            )
    if A == bodo.dict_str_arr_type:
        xuxyb__tfxfi = 'in_str_arr = A._data'
        fix__nuwqb = 'input_index = A._indices[i]'
    else:
        xuxyb__tfxfi = 'in_str_arr = A'
        fix__nuwqb = 'input_index = i'
    tgsvi__qwv = f"""def impl(B, j, A, i):
        if j == 0:
            setitem_str_offset(B, 0, 0)

        {xuxyb__tfxfi}
        {fix__nuwqb}

        # set NA
        if bodo.libs.array_kernels.isna(A, i):
            str_arr_set_na(B, j)
            return
        else:
            str_arr_set_not_na(B, j)

        # get input array offsets
        in_start_offset = getitem_str_offset(in_str_arr, input_index)
        in_end_offset = getitem_str_offset(in_str_arr, input_index + 1)
        val_len = in_end_offset - in_start_offset

        # set output offset
        out_start_offset = getitem_str_offset(B, j)
        out_end_offset = out_start_offset + val_len
        setitem_str_offset(B, j + 1, out_end_offset)

        # copy data
        if val_len != 0:
            # ensure required space in output array
            data_arr = B._data
            bodo.libs.array_item_arr_ext.ensure_data_capacity(
                data_arr, np.int64(out_start_offset), np.int64(out_end_offset)
            )
            out_data_ptr = get_data_ptr(B).data
            in_data_ptr = get_data_ptr(in_str_arr).data
            memcpy_region(
                out_data_ptr,
                out_start_offset,
                in_data_ptr,
                in_start_offset,
                val_len,
                1,
            )"""
    vly__cgcx = {}
    exec(tgsvi__qwv, {'setitem_str_offset': setitem_str_offset,
        'memcpy_region': memcpy_region, 'getitem_str_offset':
        getitem_str_offset, 'str_arr_set_na': str_arr_set_na,
        'str_arr_set_not_na': str_arr_set_not_na, 'get_data_ptr':
        get_data_ptr, 'bodo': bodo, 'np': np}, vly__cgcx)
    impl = vly__cgcx['impl']
    return impl


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    kgda__banxu = len(str_arr)
    fwx__lmool = np.empty(kgda__banxu, np.bool_)
    for i in range(kgda__banxu):
        fwx__lmool[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return fwx__lmool


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if is_str_arr_type(data) or data == binary_array_type:

        def to_list_impl(data, str_null_bools=None):
            kgda__banxu = len(data)
            l = []
            for i in range(kgda__banxu):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        itshf__aizzw = data.count
        mquji__mevt = ['to_list_if_immutable_arr(data[{}])'.format(i) for i in
            range(itshf__aizzw)]
        if is_overload_true(str_null_bools):
            mquji__mevt += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(itshf__aizzw) if is_str_arr_type(data.types[i]) or 
                data.types[i] == binary_array_type]
        tgsvi__qwv = 'def f(data, str_null_bools=None):\n'
        tgsvi__qwv += '  return ({}{})\n'.format(', '.join(mquji__mevt), 
            ',' if itshf__aizzw == 1 else '')
        vly__cgcx = {}
        exec(tgsvi__qwv, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, vly__cgcx)
        esn__gngr = vly__cgcx['f']
        return esn__gngr
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                kgda__banxu = len(list_data)
                for i in range(kgda__banxu):
                    hbtzh__lxmi = list_data[i]
                    str_arr[i] = hbtzh__lxmi
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                kgda__banxu = len(list_data)
                for i in range(kgda__banxu):
                    hbtzh__lxmi = list_data[i]
                    str_arr[i] = hbtzh__lxmi
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        itshf__aizzw = str_arr.count
        geu__aghc = 0
        tgsvi__qwv = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(itshf__aizzw):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                tgsvi__qwv += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])\n'
                    .format(i, i, itshf__aizzw + geu__aghc))
                geu__aghc += 1
            else:
                tgsvi__qwv += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        tgsvi__qwv += '  return\n'
        vly__cgcx = {}
        exec(tgsvi__qwv, {'cp_str_list_to_array': cp_str_list_to_array},
            vly__cgcx)
        pdofh__hrof = vly__cgcx['f']
        return pdofh__hrof
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            kgda__banxu = len(str_list)
            str_arr = pre_alloc_string_array(kgda__banxu, -1)
            for i in range(kgda__banxu):
                hbtzh__lxmi = str_list[i]
                str_arr[i] = hbtzh__lxmi
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            kgda__banxu = len(A)
            ldx__nmfvx = 0
            for i in range(kgda__banxu):
                hbtzh__lxmi = A[i]
                ldx__nmfvx += get_utf8_size(hbtzh__lxmi)
            return ldx__nmfvx
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        kgda__banxu = len(arr)
        n_chars = num_total_chars(arr)
        rszwa__rdpx = pre_alloc_string_array(kgda__banxu, np.int64(n_chars))
        copy_str_arr_slice(rszwa__rdpx, arr, kgda__banxu)
        return rszwa__rdpx
    return copy_impl


@overload(len, no_unliteral=True)
def str_arr_len_overload(str_arr):
    if str_arr == string_array_type:

        def str_arr_len(str_arr):
            return str_arr.size
        return str_arr_len


@overload_attribute(StringArrayType, 'size')
def str_arr_size_overload(str_arr):
    return lambda str_arr: len(str_arr._data)


@overload_attribute(StringArrayType, 'shape')
def str_arr_shape_overload(str_arr):
    return lambda str_arr: (str_arr.size,)


@overload_attribute(StringArrayType, 'nbytes')
def str_arr_nbytes_overload(str_arr):
    return lambda str_arr: str_arr._data.nbytes


@overload_method(types.Array, 'tolist', no_unliteral=True)
@overload_method(StringArrayType, 'tolist', no_unliteral=True)
def overload_to_list(arr):
    return lambda arr: list(arr)


import llvmlite.binding as ll
from llvmlite import ir as lir
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('get_str_len', hstr_ext.get_str_len)
ll.add_symbol('setitem_string_array', hstr_ext.setitem_string_array)
ll.add_symbol('is_na', hstr_ext.is_na)
ll.add_symbol('string_array_from_sequence', array_ext.
    string_array_from_sequence)
ll.add_symbol('pd_array_from_string_array', hstr_ext.pd_array_from_string_array
    )
ll.add_symbol('np_array_from_string_array', hstr_ext.np_array_from_string_array
    )
ll.add_symbol('convert_len_arr_to_offset32', hstr_ext.
    convert_len_arr_to_offset32)
ll.add_symbol('convert_len_arr_to_offset', hstr_ext.convert_len_arr_to_offset)
ll.add_symbol('set_string_array_range', hstr_ext.set_string_array_range)
ll.add_symbol('str_arr_to_int64', hstr_ext.str_arr_to_int64)
ll.add_symbol('str_arr_to_float64', hstr_ext.str_arr_to_float64)
ll.add_symbol('get_utf8_size', hstr_ext.get_utf8_size)
ll.add_symbol('print_str_arr', hstr_ext.print_str_arr)
ll.add_symbol('inplace_int64_to_str', hstr_ext.inplace_int64_to_str)
inplace_int64_to_str = types.ExternalFunction('inplace_int64_to_str', types
    .void(types.voidptr, types.int64, types.int64))
convert_len_arr_to_offset32 = types.ExternalFunction(
    'convert_len_arr_to_offset32', types.void(types.voidptr, types.intp))
convert_len_arr_to_offset = types.ExternalFunction('convert_len_arr_to_offset',
    types.void(types.voidptr, types.voidptr, types.intp))
setitem_string_array = types.ExternalFunction('setitem_string_array', types
    .void(types.CPointer(offset_type), types.CPointer(char_type), types.
    uint64, types.voidptr, types.intp, offset_type, offset_type, types.intp))
_get_utf8_size = types.ExternalFunction('get_utf8_size', types.intp(types.
    voidptr, types.intp, offset_type))
_print_str_arr = types.ExternalFunction('print_str_arr', types.void(types.
    uint64, types.uint64, types.CPointer(offset_type), types.CPointer(
    char_type)))


@numba.generated_jit(nopython=True)
def empty_str_arr(in_seq):
    tgsvi__qwv = 'def f(in_seq):\n'
    tgsvi__qwv += '    n_strs = len(in_seq)\n'
    tgsvi__qwv += '    A = pre_alloc_string_array(n_strs, -1)\n'
    tgsvi__qwv += '    return A\n'
    vly__cgcx = {}
    exec(tgsvi__qwv, {'pre_alloc_string_array': pre_alloc_string_array},
        vly__cgcx)
    dxkj__lfk = vly__cgcx['f']
    return dxkj__lfk


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    in_seq = types.unliteral(in_seq)
    if in_seq.dtype == bodo.bytes_type:
        rai__jcf = 'pre_alloc_binary_array'
    else:
        rai__jcf = 'pre_alloc_string_array'
    tgsvi__qwv = 'def f(in_seq):\n'
    tgsvi__qwv += '    n_strs = len(in_seq)\n'
    tgsvi__qwv += f'    A = {rai__jcf}(n_strs, -1)\n'
    tgsvi__qwv += '    for i in range(n_strs):\n'
    tgsvi__qwv += '        A[i] = in_seq[i]\n'
    tgsvi__qwv += '    return A\n'
    vly__cgcx = {}
    exec(tgsvi__qwv, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, vly__cgcx)
    dxkj__lfk = vly__cgcx['f']
    return dxkj__lfk


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_all_offsets_to_0 requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        gwsn__tbyqr = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        ikxu__ecfv = builder.add(gwsn__tbyqr.n_arrays, lir.Constant(lir.
            IntType(64), 1))
        ttdp__hoieo = builder.lshr(lir.Constant(lir.IntType(64),
            offset_type.bitwidth), lir.Constant(lir.IntType(64), 3))
        pcjmd__jzff = builder.mul(ikxu__ecfv, ttdp__hoieo)
        gtiqx__nfkbt = context.make_array(offset_arr_type)(context, builder,
            gwsn__tbyqr.offsets).data
        cgutils.memset(builder, gtiqx__nfkbt, pcjmd__jzff, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@intrinsic
def set_bitmap_all_NA(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_bitmap_all_NA requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        gwsn__tbyqr = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        cofb__yrkv = gwsn__tbyqr.n_arrays
        pcjmd__jzff = builder.lshr(builder.add(cofb__yrkv, lir.Constant(lir
            .IntType(64), 7)), lir.Constant(lir.IntType(64), 3))
        wgwwu__kwnto = context.make_array(null_bitmap_arr_type)(context,
            builder, gwsn__tbyqr.null_bitmap).data
        cgutils.memset(builder, wgwwu__kwnto, pcjmd__jzff, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@numba.njit
def pre_alloc_string_array(n_strs, n_chars):
    if n_chars is None:
        n_chars = -1
    str_arr = init_str_arr(bodo.libs.array_item_arr_ext.
        pre_alloc_array_item_array(np.int64(n_strs), (np.int64(n_chars),),
        char_arr_type))
    if n_chars == 0:
        set_all_offsets_to_0(str_arr)
    return str_arr


@register_jitable
def gen_na_str_array_lens(n_strs, total_len, len_arr):
    str_arr = pre_alloc_string_array(n_strs, total_len)
    set_bitmap_all_NA(str_arr)
    offsets = bodo.libs.array_item_arr_ext.get_offsets(str_arr._data)
    qrja__rkek = 0
    if total_len == 0:
        for i in range(len(offsets)):
            offsets[i] = 0
    else:
        dplu__aspcz = len(len_arr)
        for i in range(dplu__aspcz):
            offsets[i] = qrja__rkek
            qrja__rkek += len_arr[i]
        offsets[dplu__aspcz] = qrja__rkek
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    twq__nqif = i // 8
    hrhm__ohxt = getitem_str_bitmap(bits, twq__nqif)
    hrhm__ohxt ^= np.uint8(-np.uint8(bit_is_set) ^ hrhm__ohxt) & kBitmask[i % 8
        ]
    setitem_str_bitmap(bits, twq__nqif, hrhm__ohxt)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    nbf__laz = get_null_bitmap_ptr(out_str_arr)
    mkl__alzgd = get_null_bitmap_ptr(in_str_arr)
    for j in range(len(in_str_arr)):
        jhv__zruv = get_bit_bitmap(mkl__alzgd, j)
        set_bit_to(nbf__laz, out_start + j, jhv__zruv)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type, 'set_string_array_range requires string or binary arrays'
    assert isinstance(curr_str_typ, types.Integer) and isinstance(
        curr_chars_typ, types.Integer
        ), 'set_string_array_range requires integer indices'

    def codegen(context, builder, sig, args):
        out_arr, bvivd__dxc, thozi__rlj, xhni__yef = args
        vuq__rdjx = _get_str_binary_arr_payload(context, builder,
            bvivd__dxc, string_array_type)
        duzl__kwx = _get_str_binary_arr_payload(context, builder, out_arr,
            string_array_type)
        orpgi__zawra = context.make_helper(builder, offset_arr_type,
            vuq__rdjx.offsets).data
        cbov__andl = context.make_helper(builder, offset_arr_type,
            duzl__kwx.offsets).data
        csog__tvsbg = context.make_helper(builder, char_arr_type, vuq__rdjx
            .data).data
        cwy__pzoa = context.make_helper(builder, char_arr_type, duzl__kwx.data
            ).data
        num_total_chars = _get_num_total_chars(builder, orpgi__zawra,
            vuq__rdjx.n_arrays)
        zteq__twibo = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        vugey__pae = cgutils.get_or_insert_function(builder.module,
            zteq__twibo, name='set_string_array_range')
        builder.call(vugey__pae, [cbov__andl, cwy__pzoa, orpgi__zawra,
            csog__tvsbg, thozi__rlj, xhni__yef, vuq__rdjx.n_arrays,
            num_total_chars])
        xxh__bdbk = context.typing_context.resolve_value_type(copy_nulls_range)
        lwamm__fbgn = xxh__bdbk.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        vts__eij = context.get_function(xxh__bdbk, lwamm__fbgn)
        vts__eij(builder, (out_arr, bvivd__dxc, thozi__rlj))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    grbs__qdczo = c.context.make_helper(c.builder, typ, val)
    akz__rrhav = ArrayItemArrayType(char_arr_type)
    gwsn__tbyqr = _get_array_item_arr_payload(c.context, c.builder,
        akz__rrhav, grbs__qdczo.data)
    vwp__pxd = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    qza__bclug = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        qza__bclug = 'pd_array_from_string_array'
    zteq__twibo = lir.FunctionType(c.context.get_argument_type(types.
        pyobject), [lir.IntType(64), lir.IntType(offset_type.bitwidth).
        as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
        as_pointer(), lir.IntType(32)])
    uvyrl__mqg = cgutils.get_or_insert_function(c.builder.module,
        zteq__twibo, name=qza__bclug)
    gola__xwn = c.context.make_array(offset_arr_type)(c.context, c.builder,
        gwsn__tbyqr.offsets).data
    xywml__ixie = c.context.make_array(char_arr_type)(c.context, c.builder,
        gwsn__tbyqr.data).data
    wgwwu__kwnto = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, gwsn__tbyqr.null_bitmap).data
    arr = c.builder.call(uvyrl__mqg, [gwsn__tbyqr.n_arrays, gola__xwn,
        xywml__ixie, wgwwu__kwnto, vwp__pxd])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        gwsn__tbyqr = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        wgwwu__kwnto = context.make_array(null_bitmap_arr_type)(context,
            builder, gwsn__tbyqr.null_bitmap).data
        utzuz__qvgim = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        mbtb__dezp = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        hrhm__ohxt = builder.load(builder.gep(wgwwu__kwnto, [utzuz__qvgim],
            inbounds=True))
        bnwt__ecvj = lir.ArrayType(lir.IntType(8), 8)
        sifl__htgo = cgutils.alloca_once_value(builder, lir.Constant(
            bnwt__ecvj, (1, 2, 4, 8, 16, 32, 64, 128)))
        xjp__selxo = builder.load(builder.gep(sifl__htgo, [lir.Constant(lir
            .IntType(64), 0), mbtb__dezp], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(hrhm__ohxt,
            xjp__selxo), lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        gwsn__tbyqr = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        utzuz__qvgim = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        mbtb__dezp = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        wgwwu__kwnto = context.make_array(null_bitmap_arr_type)(context,
            builder, gwsn__tbyqr.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type, gwsn__tbyqr
            .offsets).data
        xmjl__ial = builder.gep(wgwwu__kwnto, [utzuz__qvgim], inbounds=True)
        hrhm__ohxt = builder.load(xmjl__ial)
        bnwt__ecvj = lir.ArrayType(lir.IntType(8), 8)
        sifl__htgo = cgutils.alloca_once_value(builder, lir.Constant(
            bnwt__ecvj, (1, 2, 4, 8, 16, 32, 64, 128)))
        xjp__selxo = builder.load(builder.gep(sifl__htgo, [lir.Constant(lir
            .IntType(64), 0), mbtb__dezp], inbounds=True))
        xjp__selxo = builder.xor(xjp__selxo, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(hrhm__ohxt, xjp__selxo), xmjl__ial)
        if str_arr_typ == string_array_type:
            zboym__yqvd = builder.add(ind, lir.Constant(lir.IntType(64), 1))
            lkj__frcng = builder.icmp_unsigned('!=', zboym__yqvd,
                gwsn__tbyqr.n_arrays)
            with builder.if_then(lkj__frcng):
                builder.store(builder.load(builder.gep(offsets, [ind])),
                    builder.gep(offsets, [zboym__yqvd]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        gwsn__tbyqr = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        utzuz__qvgim = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        mbtb__dezp = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        wgwwu__kwnto = context.make_array(null_bitmap_arr_type)(context,
            builder, gwsn__tbyqr.null_bitmap).data
        xmjl__ial = builder.gep(wgwwu__kwnto, [utzuz__qvgim], inbounds=True)
        hrhm__ohxt = builder.load(xmjl__ial)
        bnwt__ecvj = lir.ArrayType(lir.IntType(8), 8)
        sifl__htgo = cgutils.alloca_once_value(builder, lir.Constant(
            bnwt__ecvj, (1, 2, 4, 8, 16, 32, 64, 128)))
        xjp__selxo = builder.load(builder.gep(sifl__htgo, [lir.Constant(lir
            .IntType(64), 0), mbtb__dezp], inbounds=True))
        builder.store(builder.or_(hrhm__ohxt, xjp__selxo), xmjl__ial)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        gwsn__tbyqr = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        pcjmd__jzff = builder.udiv(builder.add(gwsn__tbyqr.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        wgwwu__kwnto = context.make_array(null_bitmap_arr_type)(context,
            builder, gwsn__tbyqr.null_bitmap).data
        cgutils.memset(builder, wgwwu__kwnto, pcjmd__jzff, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    wvxc__lym = context.make_helper(builder, string_array_type, str_arr)
    akz__rrhav = ArrayItemArrayType(char_arr_type)
    npi__pyho = context.make_helper(builder, akz__rrhav, wvxc__lym.data)
    rzhk__zodvg = ArrayItemArrayPayloadType(akz__rrhav)
    ztfx__zwv = context.nrt.meminfo_data(builder, npi__pyho.meminfo)
    aeqwg__lqigf = builder.bitcast(ztfx__zwv, context.get_value_type(
        rzhk__zodvg).as_pointer())
    return aeqwg__lqigf


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        vrpmy__rzr, dfn__kjjra = args
        pve__lsi = _get_str_binary_arr_data_payload_ptr(context, builder,
            dfn__kjjra)
        mkbf__zlwsz = _get_str_binary_arr_data_payload_ptr(context, builder,
            vrpmy__rzr)
        cpupr__hpu = _get_str_binary_arr_payload(context, builder,
            dfn__kjjra, sig.args[1])
        jnw__vqey = _get_str_binary_arr_payload(context, builder,
            vrpmy__rzr, sig.args[0])
        context.nrt.incref(builder, char_arr_type, cpupr__hpu.data)
        context.nrt.incref(builder, offset_arr_type, cpupr__hpu.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, cpupr__hpu.
            null_bitmap)
        context.nrt.decref(builder, char_arr_type, jnw__vqey.data)
        context.nrt.decref(builder, offset_arr_type, jnw__vqey.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, jnw__vqey.null_bitmap
            )
        builder.store(builder.load(pve__lsi), mkbf__zlwsz)
        return context.get_dummy_value()
    return types.none(to_arr_typ, from_arr_typ), codegen


dummy_use = numba.njit(lambda a: None)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_utf8_size(s):
    if isinstance(s, types.StringLiteral):
        l = len(s.literal_value.encode())
        return lambda s: l

    def impl(s):
        if s is None:
            return 0
        s = bodo.utils.indexing.unoptional(s)
        if s._is_ascii == 1:
            return len(s)
        kgda__banxu = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return kgda__banxu
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, xxwa__nuh, jubbx__anrf = args
        gwsn__tbyqr = _get_str_binary_arr_payload(context, builder, arr,
            sig.args[0])
        offsets = context.make_helper(builder, offset_arr_type, gwsn__tbyqr
            .offsets).data
        data = context.make_helper(builder, char_arr_type, gwsn__tbyqr.data
            ).data
        zteq__twibo = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        cno__szuxo = cgutils.get_or_insert_function(builder.module,
            zteq__twibo, name='setitem_string_array')
        oqp__gle = context.get_constant(types.int32, -1)
        bndae__gtj = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets,
            gwsn__tbyqr.n_arrays)
        builder.call(cno__szuxo, [offsets, data, num_total_chars, builder.
            extract_value(xxwa__nuh, 0), jubbx__anrf, oqp__gle, bndae__gtj,
            ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    zteq__twibo = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64)])
    juytv__jkr = cgutils.get_or_insert_function(builder.module, zteq__twibo,
        name='is_na')
    return builder.call(juytv__jkr, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        hfjaz__oon, nqree__ffzs, itshf__aizzw, ichij__bxp = args
        cgutils.raw_memcpy(builder, hfjaz__oon, nqree__ffzs, itshf__aizzw,
            ichij__bxp)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.voidptr, types.intp, types.intp
        ), codegen


@numba.njit
def print_str_arr(arr):
    _print_str_arr(num_strings(arr), num_total_chars(arr), get_offset_ptr(
        arr), get_data_ptr(arr))


def inplace_eq(A, i, val):
    return A[i] == val


@overload(inplace_eq)
def inplace_eq_overload(A, ind, val):

    def impl(A, ind, val):
        wglb__pkdra, qhai__sol = unicode_to_utf8_and_len(val)
        mjtxd__mqp = getitem_str_offset(A, ind)
        kecsw__omps = getitem_str_offset(A, ind + 1)
        swaw__kxjci = kecsw__omps - mjtxd__mqp
        if swaw__kxjci != qhai__sol:
            return False
        xxwa__nuh = get_data_ptr_ind(A, mjtxd__mqp)
        return memcmp(xxwa__nuh, wglb__pkdra, qhai__sol) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        mjtxd__mqp = getitem_str_offset(A, ind)
        swaw__kxjci = bodo.libs.str_ext.int_to_str_len(val)
        ttkuk__vrnnu = mjtxd__mqp + swaw__kxjci
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            mjtxd__mqp, ttkuk__vrnnu)
        xxwa__nuh = get_data_ptr_ind(A, mjtxd__mqp)
        inplace_int64_to_str(xxwa__nuh, swaw__kxjci, val)
        setitem_str_offset(A, ind + 1, mjtxd__mqp + swaw__kxjci)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        xxwa__nuh, = args
        mrcge__svw = context.insert_const_string(builder.module, '<NA>')
        win__mnwcz = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, xxwa__nuh, mrcge__svw, win__mnwcz, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    dgct__jeu = len('<NA>')

    def impl(A, ind):
        mjtxd__mqp = getitem_str_offset(A, ind)
        ttkuk__vrnnu = mjtxd__mqp + dgct__jeu
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            mjtxd__mqp, ttkuk__vrnnu)
        xxwa__nuh = get_data_ptr_ind(A, mjtxd__mqp)
        inplace_set_NA_str(xxwa__nuh)
        setitem_str_offset(A, ind + 1, mjtxd__mqp + dgct__jeu)
        str_arr_set_not_na(A, ind)
    return impl


@overload(operator.getitem, no_unliteral=True)
def str_arr_getitem_int(A, ind):
    if A != string_array_type:
        return
    if isinstance(ind, types.Integer):

        def str_arr_getitem_impl(A, ind):
            if ind < 0:
                ind += A.size
            mjtxd__mqp = getitem_str_offset(A, ind)
            kecsw__omps = getitem_str_offset(A, ind + 1)
            jubbx__anrf = kecsw__omps - mjtxd__mqp
            xxwa__nuh = get_data_ptr_ind(A, mjtxd__mqp)
            ybpiv__cpmav = decode_utf8(xxwa__nuh, jubbx__anrf)
            return ybpiv__cpmav
        return str_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_ndarray(ind)
            kgda__banxu = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(kgda__banxu):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            zpijq__kgdj = get_data_ptr(out_arr).data
            xjxz__cavfe = get_data_ptr(A).data
            geu__aghc = 0
            ahlf__yceg = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(kgda__banxu):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    mpxdl__bwnvv = get_str_arr_item_length(A, i)
                    if mpxdl__bwnvv == 1:
                        copy_single_char(zpijq__kgdj, ahlf__yceg,
                            xjxz__cavfe, getitem_str_offset(A, i))
                    else:
                        memcpy_region(zpijq__kgdj, ahlf__yceg, xjxz__cavfe,
                            getitem_str_offset(A, i), mpxdl__bwnvv, 1)
                    ahlf__yceg += mpxdl__bwnvv
                    setitem_str_offset(out_arr, geu__aghc + 1, ahlf__yceg)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, geu__aghc)
                    else:
                        str_arr_set_not_na(out_arr, geu__aghc)
                    geu__aghc += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            kgda__banxu = len(ind)
            out_arr = pre_alloc_string_array(kgda__banxu, -1)
            geu__aghc = 0
            for i in range(kgda__banxu):
                hbtzh__lxmi = A[ind[i]]
                out_arr[geu__aghc] = hbtzh__lxmi
                if str_arr_is_na(A, ind[i]):
                    str_arr_set_na(out_arr, geu__aghc)
                geu__aghc += 1
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            kgda__banxu = len(A)
            neq__nvn = numba.cpython.unicode._normalize_slice(ind, kgda__banxu)
            lhzv__tbes = numba.cpython.unicode._slice_span(neq__nvn)
            if neq__nvn.step == 1:
                mjtxd__mqp = getitem_str_offset(A, neq__nvn.start)
                kecsw__omps = getitem_str_offset(A, neq__nvn.stop)
                n_chars = kecsw__omps - mjtxd__mqp
                rszwa__rdpx = pre_alloc_string_array(lhzv__tbes, np.int64(
                    n_chars))
                for i in range(lhzv__tbes):
                    rszwa__rdpx[i] = A[neq__nvn.start + i]
                    if str_arr_is_na(A, neq__nvn.start + i):
                        str_arr_set_na(rszwa__rdpx, i)
                return rszwa__rdpx
            else:
                rszwa__rdpx = pre_alloc_string_array(lhzv__tbes, -1)
                for i in range(lhzv__tbes):
                    rszwa__rdpx[i] = A[neq__nvn.start + i * neq__nvn.step]
                    if str_arr_is_na(A, neq__nvn.start + i * neq__nvn.step):
                        str_arr_set_na(rszwa__rdpx, i)
                return rszwa__rdpx
        return str_arr_slice_impl
    raise BodoError(
        f'getitem for StringArray with indexing type {ind} not supported.')


dummy_use = numba.njit(lambda a: None)


@overload(operator.setitem)
def str_arr_setitem(A, idx, val):
    if A != string_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    fbj__iiku = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(fbj__iiku)
        trq__jddik = 4

        def impl_scalar(A, idx, val):
            hou__ohufj = (val._length if val._is_ascii else trq__jddik *
                val._length)
            bmsw__xoqb = A._data
            mjtxd__mqp = np.int64(getitem_str_offset(A, idx))
            ttkuk__vrnnu = mjtxd__mqp + hou__ohufj
            bodo.libs.array_item_arr_ext.ensure_data_capacity(bmsw__xoqb,
                mjtxd__mqp, ttkuk__vrnnu)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                ttkuk__vrnnu, val._data, val._length, val._kind, val.
                _is_ascii, idx)
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                neq__nvn = numba.cpython.unicode._normalize_slice(idx, len(A))
                ctcxy__frnli = neq__nvn.start
                bmsw__xoqb = A._data
                mjtxd__mqp = np.int64(getitem_str_offset(A, ctcxy__frnli))
                ttkuk__vrnnu = mjtxd__mqp + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(bmsw__xoqb,
                    mjtxd__mqp, ttkuk__vrnnu)
                set_string_array_range(A, val, ctcxy__frnli, mjtxd__mqp)
                qbe__vxmp = 0
                for i in range(neq__nvn.start, neq__nvn.stop, neq__nvn.step):
                    if str_arr_is_na(val, qbe__vxmp):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    qbe__vxmp += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                bsaq__gazd = str_list_to_array(val)
                A[idx] = bsaq__gazd
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                neq__nvn = numba.cpython.unicode._normalize_slice(idx, len(A))
                for i in range(neq__nvn.start, neq__nvn.stop, neq__nvn.step):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(fbj__iiku)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                kgda__banxu = len(A)
                idx = bodo.utils.conversion.coerce_to_ndarray(idx)
                out_arr = pre_alloc_string_array(kgda__banxu, -1)
                for i in numba.parfors.parfor.internal_prange(kgda__banxu):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        out_arr[i] = val
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_scalar
        elif val == string_array_type or isinstance(val, types.Array
            ) and isinstance(val.dtype, types.UnicodeCharSeq):

            def impl_bool_arr(A, idx, val):
                kgda__banxu = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(kgda__banxu, -1)
                oaf__foibh = 0
                for i in numba.parfors.parfor.internal_prange(kgda__banxu):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, oaf__foibh):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, oaf__foibh)
                        else:
                            out_arr[i] = str(val[oaf__foibh])
                        oaf__foibh += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(fbj__iiku)
    raise BodoError(fbj__iiku)


@overload_attribute(StringArrayType, 'dtype')
def overload_str_arr_dtype(A):
    return lambda A: pd.StringDtype()


@overload_attribute(StringArrayType, 'ndim')
def overload_str_arr_ndim(A):
    return lambda A: 1


@overload_method(StringArrayType, 'astype', no_unliteral=True)
def overload_str_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "StringArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.Function) and dtype.key[0] == str:
        return lambda A, dtype, copy=True: A
    juh__lkj = parse_dtype(dtype, 'StringArray.astype')
    if not isinstance(juh__lkj, (types.Float, types.Integer)
        ) and juh__lkj not in (types.bool_, bodo.libs.bool_arr_ext.
        boolean_dtype):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(juh__lkj, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            kgda__banxu = len(A)
            B = np.empty(kgda__banxu, juh__lkj)
            for i in numba.parfors.parfor.internal_prange(kgda__banxu):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = np.nan
                else:
                    B[i] = float(A[i])
            return B
        return impl_float
    elif juh__lkj == types.bool_:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            kgda__banxu = len(A)
            B = np.empty(kgda__banxu, juh__lkj)
            for i in numba.parfors.parfor.internal_prange(kgda__banxu):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = False
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif juh__lkj == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            kgda__banxu = len(A)
            B = np.empty(kgda__banxu, juh__lkj)
            for i in numba.parfors.parfor.internal_prange(kgda__banxu):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(B, i)
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            kgda__banxu = len(A)
            B = np.empty(kgda__banxu, juh__lkj)
            for i in numba.parfors.parfor.internal_prange(kgda__banxu):
                B[i] = int(A[i])
            return B
        return impl_int


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        xxwa__nuh, jubbx__anrf = args
        bexm__sefdb = context.get_python_api(builder)
        wyhyr__fgu = bexm__sefdb.string_from_string_and_size(xxwa__nuh,
            jubbx__anrf)
        ztu__flea = bexm__sefdb.to_native_value(string_type, wyhyr__fgu).value
        ebk__ombs = cgutils.create_struct_proxy(string_type)(context,
            builder, ztu__flea)
        ebk__ombs.hash = ebk__ombs.hash.type(-1)
        bexm__sefdb.decref(wyhyr__fgu)
        return ebk__ombs._getvalue()
    return string_type(types.voidptr, types.intp), codegen


def get_arr_data_ptr(arr, ind):
    return arr


@overload(get_arr_data_ptr, no_unliteral=True)
def overload_get_arr_data_ptr(arr, ind):
    assert isinstance(types.unliteral(ind), types.Integer)
    if isinstance(arr, bodo.libs.int_arr_ext.IntegerArrayType):

        def impl_int(arr, ind):
            return bodo.hiframes.split_impl.get_c_arr_ptr(arr._data.ctypes, ind
                )
        return impl_int
    assert isinstance(arr, types.Array)

    def impl_np(arr, ind):
        return bodo.hiframes.split_impl.get_c_arr_ptr(arr.ctypes, ind)
    return impl_np


def set_to_numeric_out_na_err(out_arr, out_ind, err_code):
    pass


@overload(set_to_numeric_out_na_err)
def set_to_numeric_out_na_err_overload(out_arr, out_ind, err_code):
    if isinstance(out_arr, bodo.libs.int_arr_ext.IntegerArrayType):

        def impl_int(out_arr, out_ind, err_code):
            bodo.libs.int_arr_ext.set_bit_to_arr(out_arr._null_bitmap,
                out_ind, 0 if err_code == -1 else 1)
        return impl_int
    assert isinstance(out_arr, types.Array)
    if isinstance(out_arr.dtype, types.Float):

        def impl_np(out_arr, out_ind, err_code):
            if err_code == -1:
                out_arr[out_ind] = np.nan
        return impl_np
    return lambda out_arr, out_ind, err_code: None


@numba.njit(no_cpython_wrapper=True)
def str_arr_item_to_numeric(out_arr, out_ind, str_arr, ind):
    str_arr = decode_if_dict_array(str_arr)
    err_code = _str_arr_item_to_numeric(get_arr_data_ptr(out_arr, out_ind),
        str_arr, ind, out_arr.dtype)
    set_to_numeric_out_na_err(out_arr, out_ind, err_code)


@intrinsic
def _str_arr_item_to_numeric(typingctx, out_ptr_t, str_arr_t, ind_t,
    out_dtype_t=None):
    assert str_arr_t == string_array_type, '_str_arr_item_to_numeric: str arr expected'
    assert ind_t == types.int64, '_str_arr_item_to_numeric: integer index expected'

    def codegen(context, builder, sig, args):
        jtb__plc, arr, ind, vii__gnau = args
        gwsn__tbyqr = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, gwsn__tbyqr
            .offsets).data
        data = context.make_helper(builder, char_arr_type, gwsn__tbyqr.data
            ).data
        zteq__twibo = lir.FunctionType(lir.IntType(32), [jtb__plc.type, lir
            .IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        hpsw__iisc = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            hpsw__iisc = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        hlqgh__eem = cgutils.get_or_insert_function(builder.module,
            zteq__twibo, hpsw__iisc)
        return builder.call(hlqgh__eem, [jtb__plc, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    vwp__pxd = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    zteq__twibo = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer(), lir.IntType(32)])
    npck__xair = cgutils.get_or_insert_function(c.builder.module,
        zteq__twibo, name='string_array_from_sequence')
    ddy__buu = c.builder.call(npck__xair, [val, vwp__pxd])
    akz__rrhav = ArrayItemArrayType(char_arr_type)
    npi__pyho = c.context.make_helper(c.builder, akz__rrhav)
    npi__pyho.meminfo = ddy__buu
    wvxc__lym = c.context.make_helper(c.builder, typ)
    bmsw__xoqb = npi__pyho._getvalue()
    wvxc__lym.data = bmsw__xoqb
    xkoh__xyt = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(wvxc__lym._getvalue(), is_error=xkoh__xyt)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    kgda__banxu = len(pyval)
    ahlf__yceg = 0
    ayu__kluhx = np.empty(kgda__banxu + 1, np_offset_type)
    nvuyd__szb = []
    eozb__jvh = np.empty(kgda__banxu + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        ayu__kluhx[i] = ahlf__yceg
        nafl__brit = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(eozb__jvh, i, int(not nafl__brit))
        if nafl__brit:
            continue
        lpgri__skpe = list(s.encode()) if isinstance(s, str) else list(s)
        nvuyd__szb.extend(lpgri__skpe)
        ahlf__yceg += len(lpgri__skpe)
    ayu__kluhx[kgda__banxu] = ahlf__yceg
    dsmht__wsbm = np.array(nvuyd__szb, np.uint8)
    pbqd__vsdic = context.get_constant(types.int64, kgda__banxu)
    tivww__kqnqs = context.get_constant_generic(builder, char_arr_type,
        dsmht__wsbm)
    faxtl__ghtv = context.get_constant_generic(builder, offset_arr_type,
        ayu__kluhx)
    zgcai__rhgd = context.get_constant_generic(builder,
        null_bitmap_arr_type, eozb__jvh)
    gwsn__tbyqr = lir.Constant.literal_struct([pbqd__vsdic, tivww__kqnqs,
        faxtl__ghtv, zgcai__rhgd])
    gwsn__tbyqr = cgutils.global_constant(builder, '.const.payload',
        gwsn__tbyqr).bitcast(cgutils.voidptr_t)
    ukm__inf = context.get_constant(types.int64, -1)
    jooh__jgyb = context.get_constant_null(types.voidptr)
    gyd__bffud = lir.Constant.literal_struct([ukm__inf, jooh__jgyb,
        jooh__jgyb, gwsn__tbyqr, ukm__inf])
    gyd__bffud = cgutils.global_constant(builder, '.const.meminfo', gyd__bffud
        ).bitcast(cgutils.voidptr_t)
    bmsw__xoqb = lir.Constant.literal_struct([gyd__bffud])
    wvxc__lym = lir.Constant.literal_struct([bmsw__xoqb])
    return wvxc__lym


def pre_alloc_str_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


from numba.parfors.array_analysis import ArrayAnalysis
(ArrayAnalysis._analyze_op_call_bodo_libs_str_arr_ext_pre_alloc_string_array
    ) = pre_alloc_str_arr_equiv


@overload(glob.glob, no_unliteral=True)
def overload_glob_glob(pathname, recursive=False):

    def _glob_glob_impl(pathname, recursive=False):
        with numba.objmode(l='list_str_type'):
            l = glob.glob(pathname, recursive=recursive)
        return l
    return _glob_glob_impl
