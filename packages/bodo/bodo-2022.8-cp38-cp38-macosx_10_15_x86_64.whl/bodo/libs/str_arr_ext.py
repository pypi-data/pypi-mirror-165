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
        ppjzv__jbdv = ArrayItemArrayType(char_arr_type)
        ltmn__zilm = [('data', ppjzv__jbdv)]
        models.StructModel.__init__(self, dmm, fe_type, ltmn__zilm)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')
lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        nxmcg__ryy, = args
        xoir__tcom = context.make_helper(builder, string_array_type)
        xoir__tcom.data = nxmcg__ryy
        context.nrt.incref(builder, data_typ, nxmcg__ryy)
        return xoir__tcom._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    gwj__gudv = c.context.insert_const_string(c.builder.module, 'pandas')
    urrft__kuxvz = c.pyapi.import_module_noblock(gwj__gudv)
    msrq__mhrg = c.pyapi.call_method(urrft__kuxvz, 'StringDtype', ())
    c.pyapi.decref(urrft__kuxvz)
    return msrq__mhrg


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        dfzl__nuflw = bodo.libs.dict_arr_ext.get_binary_op_overload(op, lhs,
            rhs)
        if dfzl__nuflw is not None:
            return dfzl__nuflw
        if is_str_arr_type(lhs) and is_str_arr_type(rhs):

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                prhm__wetp = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(prhm__wetp)
                for i in numba.parfors.parfor.internal_prange(prhm__wetp):
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
                prhm__wetp = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(prhm__wetp)
                for i in numba.parfors.parfor.internal_prange(prhm__wetp):
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
                prhm__wetp = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(prhm__wetp)
                for i in numba.parfors.parfor.internal_prange(prhm__wetp):
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
    jfnba__jph = is_str_arr_type(lhs) or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    jok__uieu = is_str_arr_type(rhs) or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if is_str_arr_type(lhs) and jok__uieu or jfnba__jph and is_str_arr_type(rhs
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
    rxss__fglei = context.make_helper(builder, arr_typ, arr_value)
    ppjzv__jbdv = ArrayItemArrayType(char_arr_type)
    zth__bqv = _get_array_item_arr_payload(context, builder, ppjzv__jbdv,
        rxss__fglei.data)
    return zth__bqv


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        zth__bqv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        return zth__bqv.n_arrays
    return types.int64(string_array_type), codegen


def _get_num_total_chars(builder, offsets, num_strings):
    return builder.zext(builder.load(builder.gep(offsets, [num_strings])),
        lir.IntType(64))


@intrinsic
def num_total_chars(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        zth__bqv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        kinad__okl = context.make_helper(builder, offset_arr_type, zth__bqv
            .offsets).data
        return _get_num_total_chars(builder, kinad__okl, zth__bqv.n_arrays)
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        zth__bqv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        fjboa__mlrkb = context.make_helper(builder, offset_arr_type,
            zth__bqv.offsets)
        kryj__ira = context.make_helper(builder, offset_ctypes_type)
        kryj__ira.data = builder.bitcast(fjboa__mlrkb.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        kryj__ira.meminfo = fjboa__mlrkb.meminfo
        msrq__mhrg = kryj__ira._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            msrq__mhrg)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        zth__bqv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        nxmcg__ryy = context.make_helper(builder, char_arr_type, zth__bqv.data)
        kryj__ira = context.make_helper(builder, data_ctypes_type)
        kryj__ira.data = nxmcg__ryy.data
        kryj__ira.meminfo = nxmcg__ryy.meminfo
        msrq__mhrg = kryj__ira._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, msrq__mhrg
            )
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        gqf__hvy, ind = args
        zth__bqv = _get_str_binary_arr_payload(context, builder, gqf__hvy,
            sig.args[0])
        nxmcg__ryy = context.make_helper(builder, char_arr_type, zth__bqv.data)
        kryj__ira = context.make_helper(builder, data_ctypes_type)
        kryj__ira.data = builder.gep(nxmcg__ryy.data, [ind])
        kryj__ira.meminfo = nxmcg__ryy.meminfo
        msrq__mhrg = kryj__ira._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, msrq__mhrg
            )
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        euv__vebx, kan__pozn, ukigo__zxfi, ngeqk__tqsxl = args
        jpzmz__avej = builder.bitcast(builder.gep(euv__vebx, [kan__pozn]),
            lir.IntType(8).as_pointer())
        rpo__snu = builder.bitcast(builder.gep(ukigo__zxfi, [ngeqk__tqsxl]),
            lir.IntType(8).as_pointer())
        cbf__bbn = builder.load(rpo__snu)
        builder.store(cbf__bbn, jpzmz__avej)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        zth__bqv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        jyzs__nbm = context.make_helper(builder, null_bitmap_arr_type,
            zth__bqv.null_bitmap)
        kryj__ira = context.make_helper(builder, data_ctypes_type)
        kryj__ira.data = jyzs__nbm.data
        kryj__ira.meminfo = jyzs__nbm.meminfo
        msrq__mhrg = kryj__ira._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, msrq__mhrg
            )
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        zth__bqv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        kinad__okl = context.make_helper(builder, offset_arr_type, zth__bqv
            .offsets).data
        return builder.load(builder.gep(kinad__okl, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        zth__bqv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, zth__bqv.
            offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        wmvxk__tvrr, ind = args
        if in_bitmap_typ == data_ctypes_type:
            kryj__ira = context.make_helper(builder, data_ctypes_type,
                wmvxk__tvrr)
            wmvxk__tvrr = kryj__ira.data
        return builder.load(builder.gep(wmvxk__tvrr, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        wmvxk__tvrr, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            kryj__ira = context.make_helper(builder, data_ctypes_type,
                wmvxk__tvrr)
            wmvxk__tvrr = kryj__ira.data
        builder.store(val, builder.gep(wmvxk__tvrr, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        yrrb__upjhe = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        nuo__mec = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        aph__ttsc = context.make_helper(builder, offset_arr_type,
            yrrb__upjhe.offsets).data
        qkylr__ybp = context.make_helper(builder, offset_arr_type, nuo__mec
            .offsets).data
        bcyoy__vcb = context.make_helper(builder, char_arr_type,
            yrrb__upjhe.data).data
        ifj__mcm = context.make_helper(builder, char_arr_type, nuo__mec.data
            ).data
        swgox__bwa = context.make_helper(builder, null_bitmap_arr_type,
            yrrb__upjhe.null_bitmap).data
        zrwc__hwycb = context.make_helper(builder, null_bitmap_arr_type,
            nuo__mec.null_bitmap).data
        sriex__cbg = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, qkylr__ybp, aph__ttsc, sriex__cbg)
        cgutils.memcpy(builder, ifj__mcm, bcyoy__vcb, builder.load(builder.
            gep(aph__ttsc, [ind])))
        gjj__pci = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        yopp__hhnc = builder.lshr(gjj__pci, lir.Constant(lir.IntType(64), 3))
        cgutils.memcpy(builder, zrwc__hwycb, swgox__bwa, yopp__hhnc)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        yrrb__upjhe = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        nuo__mec = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        aph__ttsc = context.make_helper(builder, offset_arr_type,
            yrrb__upjhe.offsets).data
        bcyoy__vcb = context.make_helper(builder, char_arr_type,
            yrrb__upjhe.data).data
        ifj__mcm = context.make_helper(builder, char_arr_type, nuo__mec.data
            ).data
        num_total_chars = _get_num_total_chars(builder, aph__ttsc,
            yrrb__upjhe.n_arrays)
        cgutils.memcpy(builder, ifj__mcm, bcyoy__vcb, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        yrrb__upjhe = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        nuo__mec = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        aph__ttsc = context.make_helper(builder, offset_arr_type,
            yrrb__upjhe.offsets).data
        qkylr__ybp = context.make_helper(builder, offset_arr_type, nuo__mec
            .offsets).data
        swgox__bwa = context.make_helper(builder, null_bitmap_arr_type,
            yrrb__upjhe.null_bitmap).data
        prhm__wetp = yrrb__upjhe.n_arrays
        pyh__kai = context.get_constant(offset_type, 0)
        rzlu__lewh = cgutils.alloca_once_value(builder, pyh__kai)
        with cgutils.for_range(builder, prhm__wetp) as qqfh__mej:
            urjz__mdnn = lower_is_na(context, builder, swgox__bwa,
                qqfh__mej.index)
            with cgutils.if_likely(builder, builder.not_(urjz__mdnn)):
                pmtr__iai = builder.load(builder.gep(aph__ttsc, [qqfh__mej.
                    index]))
                yov__tble = builder.load(rzlu__lewh)
                builder.store(pmtr__iai, builder.gep(qkylr__ybp, [yov__tble]))
                builder.store(builder.add(yov__tble, lir.Constant(context.
                    get_value_type(offset_type), 1)), rzlu__lewh)
        yov__tble = builder.load(rzlu__lewh)
        pmtr__iai = builder.load(builder.gep(aph__ttsc, [prhm__wetp]))
        builder.store(pmtr__iai, builder.gep(qkylr__ybp, [yov__tble]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        fjatj__mrm, ind, str, inuw__qdi = args
        fjatj__mrm = context.make_array(sig.args[0])(context, builder,
            fjatj__mrm)
        xrh__rpg = builder.gep(fjatj__mrm.data, [ind])
        cgutils.raw_memcpy(builder, xrh__rpg, str, inuw__qdi, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        xrh__rpg, ind, kydny__wtl, inuw__qdi = args
        xrh__rpg = builder.gep(xrh__rpg, [ind])
        cgutils.raw_memcpy(builder, xrh__rpg, kydny__wtl, inuw__qdi, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.generated_jit(nopython=True)
def get_str_arr_item_length(A, i):
    if A == bodo.dict_str_arr_type:

        def impl(A, i):
            idx = A._indices[i]
            yft__aaqg = A._data
            return np.int64(getitem_str_offset(yft__aaqg, idx + 1) -
                getitem_str_offset(yft__aaqg, idx))
        return impl
    else:
        return lambda A, i: np.int64(getitem_str_offset(A, i + 1) -
            getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_str_length(A, i):
    dlues__kuk = np.int64(getitem_str_offset(A, i))
    kaslk__aygk = np.int64(getitem_str_offset(A, i + 1))
    l = kaslk__aygk - dlues__kuk
    qjx__aszy = get_data_ptr_ind(A, dlues__kuk)
    for j in range(l):
        if bodo.hiframes.split_impl.getitem_c_arr(qjx__aszy, j) >= 128:
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
        wobza__vqa = 'in_str_arr = A._data'
        fweh__xfcg = 'input_index = A._indices[i]'
    else:
        wobza__vqa = 'in_str_arr = A'
        fweh__xfcg = 'input_index = i'
    ycae__gmbqd = f"""def impl(B, j, A, i):
        if j == 0:
            setitem_str_offset(B, 0, 0)

        {wobza__vqa}
        {fweh__xfcg}

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
    xor__jpoyj = {}
    exec(ycae__gmbqd, {'setitem_str_offset': setitem_str_offset,
        'memcpy_region': memcpy_region, 'getitem_str_offset':
        getitem_str_offset, 'str_arr_set_na': str_arr_set_na,
        'str_arr_set_not_na': str_arr_set_not_na, 'get_data_ptr':
        get_data_ptr, 'bodo': bodo, 'np': np}, xor__jpoyj)
    impl = xor__jpoyj['impl']
    return impl


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    prhm__wetp = len(str_arr)
    gns__rgh = np.empty(prhm__wetp, np.bool_)
    for i in range(prhm__wetp):
        gns__rgh[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return gns__rgh


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if is_str_arr_type(data) or data == binary_array_type:

        def to_list_impl(data, str_null_bools=None):
            prhm__wetp = len(data)
            l = []
            for i in range(prhm__wetp):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        qsa__qpnwn = data.count
        dolo__jvz = ['to_list_if_immutable_arr(data[{}])'.format(i) for i in
            range(qsa__qpnwn)]
        if is_overload_true(str_null_bools):
            dolo__jvz += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(qsa__qpnwn) if is_str_arr_type(data.types[i]) or data
                .types[i] == binary_array_type]
        ycae__gmbqd = 'def f(data, str_null_bools=None):\n'
        ycae__gmbqd += '  return ({}{})\n'.format(', '.join(dolo__jvz), ',' if
            qsa__qpnwn == 1 else '')
        xor__jpoyj = {}
        exec(ycae__gmbqd, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, xor__jpoyj)
        peok__dnj = xor__jpoyj['f']
        return peok__dnj
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                prhm__wetp = len(list_data)
                for i in range(prhm__wetp):
                    kydny__wtl = list_data[i]
                    str_arr[i] = kydny__wtl
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                prhm__wetp = len(list_data)
                for i in range(prhm__wetp):
                    kydny__wtl = list_data[i]
                    str_arr[i] = kydny__wtl
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        qsa__qpnwn = str_arr.count
        yxaw__hdj = 0
        ycae__gmbqd = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(qsa__qpnwn):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                ycae__gmbqd += (
                    """  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])
"""
                    .format(i, i, qsa__qpnwn + yxaw__hdj))
                yxaw__hdj += 1
            else:
                ycae__gmbqd += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        ycae__gmbqd += '  return\n'
        xor__jpoyj = {}
        exec(ycae__gmbqd, {'cp_str_list_to_array': cp_str_list_to_array},
            xor__jpoyj)
        jgnnh__lxxzy = xor__jpoyj['f']
        return jgnnh__lxxzy
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            prhm__wetp = len(str_list)
            str_arr = pre_alloc_string_array(prhm__wetp, -1)
            for i in range(prhm__wetp):
                kydny__wtl = str_list[i]
                str_arr[i] = kydny__wtl
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            prhm__wetp = len(A)
            leb__dmcjg = 0
            for i in range(prhm__wetp):
                kydny__wtl = A[i]
                leb__dmcjg += get_utf8_size(kydny__wtl)
            return leb__dmcjg
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        prhm__wetp = len(arr)
        n_chars = num_total_chars(arr)
        dxpcf__qlzw = pre_alloc_string_array(prhm__wetp, np.int64(n_chars))
        copy_str_arr_slice(dxpcf__qlzw, arr, prhm__wetp)
        return dxpcf__qlzw
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
    ycae__gmbqd = 'def f(in_seq):\n'
    ycae__gmbqd += '    n_strs = len(in_seq)\n'
    ycae__gmbqd += '    A = pre_alloc_string_array(n_strs, -1)\n'
    ycae__gmbqd += '    return A\n'
    xor__jpoyj = {}
    exec(ycae__gmbqd, {'pre_alloc_string_array': pre_alloc_string_array},
        xor__jpoyj)
    ppumx__ncxg = xor__jpoyj['f']
    return ppumx__ncxg


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    in_seq = types.unliteral(in_seq)
    if in_seq.dtype == bodo.bytes_type:
        drux__prlxg = 'pre_alloc_binary_array'
    else:
        drux__prlxg = 'pre_alloc_string_array'
    ycae__gmbqd = 'def f(in_seq):\n'
    ycae__gmbqd += '    n_strs = len(in_seq)\n'
    ycae__gmbqd += f'    A = {drux__prlxg}(n_strs, -1)\n'
    ycae__gmbqd += '    for i in range(n_strs):\n'
    ycae__gmbqd += '        A[i] = in_seq[i]\n'
    ycae__gmbqd += '    return A\n'
    xor__jpoyj = {}
    exec(ycae__gmbqd, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, xor__jpoyj)
    ppumx__ncxg = xor__jpoyj['f']
    return ppumx__ncxg


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_all_offsets_to_0 requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        zth__bqv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        ogfql__yjzlc = builder.add(zth__bqv.n_arrays, lir.Constant(lir.
            IntType(64), 1))
        zpyfz__uzl = builder.lshr(lir.Constant(lir.IntType(64), offset_type
            .bitwidth), lir.Constant(lir.IntType(64), 3))
        yopp__hhnc = builder.mul(ogfql__yjzlc, zpyfz__uzl)
        kye__jahb = context.make_array(offset_arr_type)(context, builder,
            zth__bqv.offsets).data
        cgutils.memset(builder, kye__jahb, yopp__hhnc, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@intrinsic
def set_bitmap_all_NA(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_bitmap_all_NA requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        zth__bqv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            sig.args[0])
        rmw__ebw = zth__bqv.n_arrays
        yopp__hhnc = builder.lshr(builder.add(rmw__ebw, lir.Constant(lir.
            IntType(64), 7)), lir.Constant(lir.IntType(64), 3))
        ljpe__kis = context.make_array(null_bitmap_arr_type)(context,
            builder, zth__bqv.null_bitmap).data
        cgutils.memset(builder, ljpe__kis, yopp__hhnc, 0)
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
    jwuc__xhtid = 0
    if total_len == 0:
        for i in range(len(offsets)):
            offsets[i] = 0
    else:
        yhw__upv = len(len_arr)
        for i in range(yhw__upv):
            offsets[i] = jwuc__xhtid
            jwuc__xhtid += len_arr[i]
        offsets[yhw__upv] = jwuc__xhtid
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    hpi__xqhwr = i // 8
    gaa__uncp = getitem_str_bitmap(bits, hpi__xqhwr)
    gaa__uncp ^= np.uint8(-np.uint8(bit_is_set) ^ gaa__uncp) & kBitmask[i % 8]
    setitem_str_bitmap(bits, hpi__xqhwr, gaa__uncp)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    ypoz__odiur = get_null_bitmap_ptr(out_str_arr)
    pwlue__tpnh = get_null_bitmap_ptr(in_str_arr)
    for j in range(len(in_str_arr)):
        xzkjq__tmz = get_bit_bitmap(pwlue__tpnh, j)
        set_bit_to(ypoz__odiur, out_start + j, xzkjq__tmz)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type, 'set_string_array_range requires string or binary arrays'
    assert isinstance(curr_str_typ, types.Integer) and isinstance(
        curr_chars_typ, types.Integer
        ), 'set_string_array_range requires integer indices'

    def codegen(context, builder, sig, args):
        out_arr, gqf__hvy, shbun__vref, brk__wslld = args
        yrrb__upjhe = _get_str_binary_arr_payload(context, builder,
            gqf__hvy, string_array_type)
        nuo__mec = _get_str_binary_arr_payload(context, builder, out_arr,
            string_array_type)
        aph__ttsc = context.make_helper(builder, offset_arr_type,
            yrrb__upjhe.offsets).data
        qkylr__ybp = context.make_helper(builder, offset_arr_type, nuo__mec
            .offsets).data
        bcyoy__vcb = context.make_helper(builder, char_arr_type,
            yrrb__upjhe.data).data
        ifj__mcm = context.make_helper(builder, char_arr_type, nuo__mec.data
            ).data
        num_total_chars = _get_num_total_chars(builder, aph__ttsc,
            yrrb__upjhe.n_arrays)
        wek__utdh = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        sgnv__usq = cgutils.get_or_insert_function(builder.module,
            wek__utdh, name='set_string_array_range')
        builder.call(sgnv__usq, [qkylr__ybp, ifj__mcm, aph__ttsc,
            bcyoy__vcb, shbun__vref, brk__wslld, yrrb__upjhe.n_arrays,
            num_total_chars])
        qjpyx__xgzmh = context.typing_context.resolve_value_type(
            copy_nulls_range)
        cuwuw__iyvn = qjpyx__xgzmh.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        kxcnp__eenuk = context.get_function(qjpyx__xgzmh, cuwuw__iyvn)
        kxcnp__eenuk(builder, (out_arr, gqf__hvy, shbun__vref))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    uxyo__qoss = c.context.make_helper(c.builder, typ, val)
    ppjzv__jbdv = ArrayItemArrayType(char_arr_type)
    zth__bqv = _get_array_item_arr_payload(c.context, c.builder,
        ppjzv__jbdv, uxyo__qoss.data)
    jvusi__mex = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    hwk__ykzvb = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        hwk__ykzvb = 'pd_array_from_string_array'
    wek__utdh = lir.FunctionType(c.context.get_argument_type(types.pyobject
        ), [lir.IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
        lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
        IntType(32)])
    voj__kbs = cgutils.get_or_insert_function(c.builder.module, wek__utdh,
        name=hwk__ykzvb)
    kinad__okl = c.context.make_array(offset_arr_type)(c.context, c.builder,
        zth__bqv.offsets).data
    qjx__aszy = c.context.make_array(char_arr_type)(c.context, c.builder,
        zth__bqv.data).data
    ljpe__kis = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, zth__bqv.null_bitmap).data
    arr = c.builder.call(voj__kbs, [zth__bqv.n_arrays, kinad__okl,
        qjx__aszy, ljpe__kis, jvusi__mex])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        zth__bqv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        ljpe__kis = context.make_array(null_bitmap_arr_type)(context,
            builder, zth__bqv.null_bitmap).data
        ocivl__bkxek = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        vafur__kazc = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        gaa__uncp = builder.load(builder.gep(ljpe__kis, [ocivl__bkxek],
            inbounds=True))
        kte__rwld = lir.ArrayType(lir.IntType(8), 8)
        tyliz__ipgnm = cgutils.alloca_once_value(builder, lir.Constant(
            kte__rwld, (1, 2, 4, 8, 16, 32, 64, 128)))
        enmg__fqu = builder.load(builder.gep(tyliz__ipgnm, [lir.Constant(
            lir.IntType(64), 0), vafur__kazc], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(gaa__uncp,
            enmg__fqu), lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        zth__bqv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        ocivl__bkxek = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        vafur__kazc = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        ljpe__kis = context.make_array(null_bitmap_arr_type)(context,
            builder, zth__bqv.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type, zth__bqv.
            offsets).data
        omvx__zbc = builder.gep(ljpe__kis, [ocivl__bkxek], inbounds=True)
        gaa__uncp = builder.load(omvx__zbc)
        kte__rwld = lir.ArrayType(lir.IntType(8), 8)
        tyliz__ipgnm = cgutils.alloca_once_value(builder, lir.Constant(
            kte__rwld, (1, 2, 4, 8, 16, 32, 64, 128)))
        enmg__fqu = builder.load(builder.gep(tyliz__ipgnm, [lir.Constant(
            lir.IntType(64), 0), vafur__kazc], inbounds=True))
        enmg__fqu = builder.xor(enmg__fqu, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(gaa__uncp, enmg__fqu), omvx__zbc)
        if str_arr_typ == string_array_type:
            nbcmf__kqo = builder.add(ind, lir.Constant(lir.IntType(64), 1))
            ohdr__yzpk = builder.icmp_unsigned('!=', nbcmf__kqo, zth__bqv.
                n_arrays)
            with builder.if_then(ohdr__yzpk):
                builder.store(builder.load(builder.gep(offsets, [ind])),
                    builder.gep(offsets, [nbcmf__kqo]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        zth__bqv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        ocivl__bkxek = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        vafur__kazc = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        ljpe__kis = context.make_array(null_bitmap_arr_type)(context,
            builder, zth__bqv.null_bitmap).data
        omvx__zbc = builder.gep(ljpe__kis, [ocivl__bkxek], inbounds=True)
        gaa__uncp = builder.load(omvx__zbc)
        kte__rwld = lir.ArrayType(lir.IntType(8), 8)
        tyliz__ipgnm = cgutils.alloca_once_value(builder, lir.Constant(
            kte__rwld, (1, 2, 4, 8, 16, 32, 64, 128)))
        enmg__fqu = builder.load(builder.gep(tyliz__ipgnm, [lir.Constant(
            lir.IntType(64), 0), vafur__kazc], inbounds=True))
        builder.store(builder.or_(gaa__uncp, enmg__fqu), omvx__zbc)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        zth__bqv = _get_str_binary_arr_payload(context, builder, in_str_arr,
            string_array_type)
        yopp__hhnc = builder.udiv(builder.add(zth__bqv.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        ljpe__kis = context.make_array(null_bitmap_arr_type)(context,
            builder, zth__bqv.null_bitmap).data
        cgutils.memset(builder, ljpe__kis, yopp__hhnc, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    ciri__rmts = context.make_helper(builder, string_array_type, str_arr)
    ppjzv__jbdv = ArrayItemArrayType(char_arr_type)
    xuvu__pmbew = context.make_helper(builder, ppjzv__jbdv, ciri__rmts.data)
    moh__nupr = ArrayItemArrayPayloadType(ppjzv__jbdv)
    plwo__qap = context.nrt.meminfo_data(builder, xuvu__pmbew.meminfo)
    imj__fjl = builder.bitcast(plwo__qap, context.get_value_type(moh__nupr)
        .as_pointer())
    return imj__fjl


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        lsdd__aixp, wntbz__szdp = args
        kgs__vpw = _get_str_binary_arr_data_payload_ptr(context, builder,
            wntbz__szdp)
        pyba__jmqrc = _get_str_binary_arr_data_payload_ptr(context, builder,
            lsdd__aixp)
        gqhvt__weh = _get_str_binary_arr_payload(context, builder,
            wntbz__szdp, sig.args[1])
        vkaw__ndgx = _get_str_binary_arr_payload(context, builder,
            lsdd__aixp, sig.args[0])
        context.nrt.incref(builder, char_arr_type, gqhvt__weh.data)
        context.nrt.incref(builder, offset_arr_type, gqhvt__weh.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, gqhvt__weh.
            null_bitmap)
        context.nrt.decref(builder, char_arr_type, vkaw__ndgx.data)
        context.nrt.decref(builder, offset_arr_type, vkaw__ndgx.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, vkaw__ndgx.
            null_bitmap)
        builder.store(builder.load(kgs__vpw), pyba__jmqrc)
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
        prhm__wetp = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return prhm__wetp
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, xrh__rpg, trh__rng = args
        zth__bqv = _get_str_binary_arr_payload(context, builder, arr, sig.
            args[0])
        offsets = context.make_helper(builder, offset_arr_type, zth__bqv.
            offsets).data
        data = context.make_helper(builder, char_arr_type, zth__bqv.data).data
        wek__utdh = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        cckpv__mztf = cgutils.get_or_insert_function(builder.module,
            wek__utdh, name='setitem_string_array')
        wtz__jtfy = context.get_constant(types.int32, -1)
        rti__twpg = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets, zth__bqv.
            n_arrays)
        builder.call(cckpv__mztf, [offsets, data, num_total_chars, builder.
            extract_value(xrh__rpg, 0), trh__rng, wtz__jtfy, rti__twpg, ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    wek__utdh = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer
        (), lir.IntType(64)])
    mptk__qydto = cgutils.get_or_insert_function(builder.module, wek__utdh,
        name='is_na')
    return builder.call(mptk__qydto, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        jpzmz__avej, rpo__snu, qsa__qpnwn, juku__dxue = args
        cgutils.raw_memcpy(builder, jpzmz__avej, rpo__snu, qsa__qpnwn,
            juku__dxue)
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
        ktzy__plbdp, geaf__wamw = unicode_to_utf8_and_len(val)
        vvm__srgsr = getitem_str_offset(A, ind)
        rpyug__emkep = getitem_str_offset(A, ind + 1)
        jiuim__mkq = rpyug__emkep - vvm__srgsr
        if jiuim__mkq != geaf__wamw:
            return False
        xrh__rpg = get_data_ptr_ind(A, vvm__srgsr)
        return memcmp(xrh__rpg, ktzy__plbdp, geaf__wamw) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        vvm__srgsr = getitem_str_offset(A, ind)
        jiuim__mkq = bodo.libs.str_ext.int_to_str_len(val)
        ofpki__gns = vvm__srgsr + jiuim__mkq
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            vvm__srgsr, ofpki__gns)
        xrh__rpg = get_data_ptr_ind(A, vvm__srgsr)
        inplace_int64_to_str(xrh__rpg, jiuim__mkq, val)
        setitem_str_offset(A, ind + 1, vvm__srgsr + jiuim__mkq)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        xrh__rpg, = args
        zkafv__acjj = context.insert_const_string(builder.module, '<NA>')
        tskyq__dtbq = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, xrh__rpg, zkafv__acjj, tskyq__dtbq, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    silmg__uww = len('<NA>')

    def impl(A, ind):
        vvm__srgsr = getitem_str_offset(A, ind)
        ofpki__gns = vvm__srgsr + silmg__uww
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            vvm__srgsr, ofpki__gns)
        xrh__rpg = get_data_ptr_ind(A, vvm__srgsr)
        inplace_set_NA_str(xrh__rpg)
        setitem_str_offset(A, ind + 1, vvm__srgsr + silmg__uww)
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
            vvm__srgsr = getitem_str_offset(A, ind)
            rpyug__emkep = getitem_str_offset(A, ind + 1)
            trh__rng = rpyug__emkep - vvm__srgsr
            xrh__rpg = get_data_ptr_ind(A, vvm__srgsr)
            hcpy__rpnd = decode_utf8(xrh__rpg, trh__rng)
            return hcpy__rpnd
        return str_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_ndarray(ind)
            prhm__wetp = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(prhm__wetp):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            kdblp__ebwpm = get_data_ptr(out_arr).data
            lxki__maloj = get_data_ptr(A).data
            yxaw__hdj = 0
            yov__tble = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(prhm__wetp):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    eeu__cbvba = get_str_arr_item_length(A, i)
                    if eeu__cbvba == 1:
                        copy_single_char(kdblp__ebwpm, yov__tble,
                            lxki__maloj, getitem_str_offset(A, i))
                    else:
                        memcpy_region(kdblp__ebwpm, yov__tble, lxki__maloj,
                            getitem_str_offset(A, i), eeu__cbvba, 1)
                    yov__tble += eeu__cbvba
                    setitem_str_offset(out_arr, yxaw__hdj + 1, yov__tble)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, yxaw__hdj)
                    else:
                        str_arr_set_not_na(out_arr, yxaw__hdj)
                    yxaw__hdj += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            prhm__wetp = len(ind)
            out_arr = pre_alloc_string_array(prhm__wetp, -1)
            yxaw__hdj = 0
            for i in range(prhm__wetp):
                kydny__wtl = A[ind[i]]
                out_arr[yxaw__hdj] = kydny__wtl
                if str_arr_is_na(A, ind[i]):
                    str_arr_set_na(out_arr, yxaw__hdj)
                yxaw__hdj += 1
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            prhm__wetp = len(A)
            crvcn__lwl = numba.cpython.unicode._normalize_slice(ind, prhm__wetp
                )
            bjy__qtlxk = numba.cpython.unicode._slice_span(crvcn__lwl)
            if crvcn__lwl.step == 1:
                vvm__srgsr = getitem_str_offset(A, crvcn__lwl.start)
                rpyug__emkep = getitem_str_offset(A, crvcn__lwl.stop)
                n_chars = rpyug__emkep - vvm__srgsr
                dxpcf__qlzw = pre_alloc_string_array(bjy__qtlxk, np.int64(
                    n_chars))
                for i in range(bjy__qtlxk):
                    dxpcf__qlzw[i] = A[crvcn__lwl.start + i]
                    if str_arr_is_na(A, crvcn__lwl.start + i):
                        str_arr_set_na(dxpcf__qlzw, i)
                return dxpcf__qlzw
            else:
                dxpcf__qlzw = pre_alloc_string_array(bjy__qtlxk, -1)
                for i in range(bjy__qtlxk):
                    dxpcf__qlzw[i] = A[crvcn__lwl.start + i * crvcn__lwl.step]
                    if str_arr_is_na(A, crvcn__lwl.start + i * crvcn__lwl.step
                        ):
                        str_arr_set_na(dxpcf__qlzw, i)
                return dxpcf__qlzw
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
    mcv__zvslv = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(mcv__zvslv)
        wzr__fsdi = 4

        def impl_scalar(A, idx, val):
            plk__kuyej = (val._length if val._is_ascii else wzr__fsdi * val
                ._length)
            nxmcg__ryy = A._data
            vvm__srgsr = np.int64(getitem_str_offset(A, idx))
            ofpki__gns = vvm__srgsr + plk__kuyej
            bodo.libs.array_item_arr_ext.ensure_data_capacity(nxmcg__ryy,
                vvm__srgsr, ofpki__gns)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                ofpki__gns, val._data, val._length, val._kind, val.
                _is_ascii, idx)
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                crvcn__lwl = numba.cpython.unicode._normalize_slice(idx, len(A)
                    )
                dlues__kuk = crvcn__lwl.start
                nxmcg__ryy = A._data
                vvm__srgsr = np.int64(getitem_str_offset(A, dlues__kuk))
                ofpki__gns = vvm__srgsr + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(nxmcg__ryy,
                    vvm__srgsr, ofpki__gns)
                set_string_array_range(A, val, dlues__kuk, vvm__srgsr)
                koh__fsn = 0
                for i in range(crvcn__lwl.start, crvcn__lwl.stop,
                    crvcn__lwl.step):
                    if str_arr_is_na(val, koh__fsn):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    koh__fsn += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                ngg__acfw = str_list_to_array(val)
                A[idx] = ngg__acfw
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                crvcn__lwl = numba.cpython.unicode._normalize_slice(idx, len(A)
                    )
                for i in range(crvcn__lwl.start, crvcn__lwl.stop,
                    crvcn__lwl.step):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(mcv__zvslv)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                prhm__wetp = len(A)
                idx = bodo.utils.conversion.coerce_to_ndarray(idx)
                out_arr = pre_alloc_string_array(prhm__wetp, -1)
                for i in numba.parfors.parfor.internal_prange(prhm__wetp):
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
                prhm__wetp = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(prhm__wetp, -1)
                twv__vfjq = 0
                for i in numba.parfors.parfor.internal_prange(prhm__wetp):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, twv__vfjq):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, twv__vfjq)
                        else:
                            out_arr[i] = str(val[twv__vfjq])
                        twv__vfjq += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(mcv__zvslv)
    raise BodoError(mcv__zvslv)


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
    azh__hha = parse_dtype(dtype, 'StringArray.astype')
    if not isinstance(azh__hha, (types.Float, types.Integer)
        ) and azh__hha not in (types.bool_, bodo.libs.bool_arr_ext.
        boolean_dtype):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(azh__hha, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            prhm__wetp = len(A)
            B = np.empty(prhm__wetp, azh__hha)
            for i in numba.parfors.parfor.internal_prange(prhm__wetp):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = np.nan
                else:
                    B[i] = float(A[i])
            return B
        return impl_float
    elif azh__hha == types.bool_:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            prhm__wetp = len(A)
            B = np.empty(prhm__wetp, azh__hha)
            for i in numba.parfors.parfor.internal_prange(prhm__wetp):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = False
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif azh__hha == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            prhm__wetp = len(A)
            B = np.empty(prhm__wetp, azh__hha)
            for i in numba.parfors.parfor.internal_prange(prhm__wetp):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(B, i)
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            prhm__wetp = len(A)
            B = np.empty(prhm__wetp, azh__hha)
            for i in numba.parfors.parfor.internal_prange(prhm__wetp):
                B[i] = int(A[i])
            return B
        return impl_int


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        xrh__rpg, trh__rng = args
        wmjwn__glrs = context.get_python_api(builder)
        lpauw__umxy = wmjwn__glrs.string_from_string_and_size(xrh__rpg,
            trh__rng)
        kwcsv__mcffs = wmjwn__glrs.to_native_value(string_type, lpauw__umxy
            ).value
        dxgcn__uihhs = cgutils.create_struct_proxy(string_type)(context,
            builder, kwcsv__mcffs)
        dxgcn__uihhs.hash = dxgcn__uihhs.hash.type(-1)
        wmjwn__glrs.decref(lpauw__umxy)
        return dxgcn__uihhs._getvalue()
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
        efasm__jiupv, arr, ind, vyxxg__bbid = args
        zth__bqv = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, zth__bqv.
            offsets).data
        data = context.make_helper(builder, char_arr_type, zth__bqv.data).data
        wek__utdh = lir.FunctionType(lir.IntType(32), [efasm__jiupv.type,
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        ovl__awxb = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            ovl__awxb = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        vmmn__bpcrl = cgutils.get_or_insert_function(builder.module,
            wek__utdh, ovl__awxb)
        return builder.call(vmmn__bpcrl, [efasm__jiupv, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    jvusi__mex = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    wek__utdh = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(
        8).as_pointer(), lir.IntType(32)])
    aziij__fpf = cgutils.get_or_insert_function(c.builder.module, wek__utdh,
        name='string_array_from_sequence')
    uail__bjpjt = c.builder.call(aziij__fpf, [val, jvusi__mex])
    ppjzv__jbdv = ArrayItemArrayType(char_arr_type)
    xuvu__pmbew = c.context.make_helper(c.builder, ppjzv__jbdv)
    xuvu__pmbew.meminfo = uail__bjpjt
    ciri__rmts = c.context.make_helper(c.builder, typ)
    nxmcg__ryy = xuvu__pmbew._getvalue()
    ciri__rmts.data = nxmcg__ryy
    tous__vraf = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ciri__rmts._getvalue(), is_error=tous__vraf)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    prhm__wetp = len(pyval)
    yov__tble = 0
    tpdkc__klrj = np.empty(prhm__wetp + 1, np_offset_type)
    xqgrz__knu = []
    ropc__zkdz = np.empty(prhm__wetp + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        tpdkc__klrj[i] = yov__tble
        vvjmx__ablvu = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(ropc__zkdz, i, int(not
            vvjmx__ablvu))
        if vvjmx__ablvu:
            continue
        ircor__mmhx = list(s.encode()) if isinstance(s, str) else list(s)
        xqgrz__knu.extend(ircor__mmhx)
        yov__tble += len(ircor__mmhx)
    tpdkc__klrj[prhm__wetp] = yov__tble
    bpyxq__txcos = np.array(xqgrz__knu, np.uint8)
    qqlna__nbc = context.get_constant(types.int64, prhm__wetp)
    tgai__tvl = context.get_constant_generic(builder, char_arr_type,
        bpyxq__txcos)
    ywsq__tphoh = context.get_constant_generic(builder, offset_arr_type,
        tpdkc__klrj)
    bsyg__cbzh = context.get_constant_generic(builder, null_bitmap_arr_type,
        ropc__zkdz)
    zth__bqv = lir.Constant.literal_struct([qqlna__nbc, tgai__tvl,
        ywsq__tphoh, bsyg__cbzh])
    zth__bqv = cgutils.global_constant(builder, '.const.payload', zth__bqv
        ).bitcast(cgutils.voidptr_t)
    tkyu__jjx = context.get_constant(types.int64, -1)
    hcq__nppw = context.get_constant_null(types.voidptr)
    siw__zccd = lir.Constant.literal_struct([tkyu__jjx, hcq__nppw,
        hcq__nppw, zth__bqv, tkyu__jjx])
    siw__zccd = cgutils.global_constant(builder, '.const.meminfo', siw__zccd
        ).bitcast(cgutils.voidptr_t)
    nxmcg__ryy = lir.Constant.literal_struct([siw__zccd])
    ciri__rmts = lir.Constant.literal_struct([nxmcg__ryy])
    return ciri__rmts


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
