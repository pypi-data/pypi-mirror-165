"""Array implementation for binary (bytes) objects, which are usually immutable.
It is equivalent to string array, except that it stores a 'bytes' object for each
element instead of 'str'.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, overload, overload_attribute, overload_method
import bodo
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.utils.typing import BodoError, is_list_like_index_type
_bytes_fromhex = types.ExternalFunction('bytes_fromhex', types.int64(types.
    voidptr, types.voidptr, types.uint64))
ll.add_symbol('bytes_to_hex', hstr_ext.bytes_to_hex)
ll.add_symbol('bytes_fromhex', hstr_ext.bytes_fromhex)
bytes_type = types.Bytes(types.uint8, 1, 'C', readonly=True)


@overload(len)
def bytes_len_overload(bytes_obj):
    if isinstance(bytes_obj, types.Bytes):
        return lambda bytes_obj: bytes_obj._nitems


@overload(operator.getitem, no_unliteral=True)
def bytes_getitem(byte_obj, ind):
    if not isinstance(byte_obj, types.Bytes):
        return
    if isinstance(ind, types.SliceType):

        def impl(byte_obj, ind):
            arr = cast_bytes_uint8array(byte_obj)
            pbr__hsk = bodo.utils.conversion.ensure_contig_if_np(arr[ind])
            return cast_uint8array_bytes(pbr__hsk)
        return impl


class BinaryArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self):
        super(BinaryArrayType, self).__init__(name='BinaryArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return bytes_type

    def copy(self):
        return BinaryArrayType()

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)


binary_array_type = BinaryArrayType()


@overload(len, no_unliteral=True)
def bin_arr_len_overload(bin_arr):
    if bin_arr == binary_array_type:
        return lambda bin_arr: len(bin_arr._data)


make_attribute_wrapper(types.Bytes, 'nitems', '_nitems')


@overload_attribute(BinaryArrayType, 'size')
def bin_arr_size_overload(bin_arr):
    return lambda bin_arr: len(bin_arr._data)


@overload_attribute(BinaryArrayType, 'shape')
def bin_arr_shape_overload(bin_arr):
    return lambda bin_arr: (len(bin_arr._data),)


@overload_attribute(BinaryArrayType, 'nbytes')
def bin_arr_nbytes_overload(bin_arr):
    return lambda bin_arr: bin_arr._data.nbytes


@overload_attribute(BinaryArrayType, 'ndim')
def overload_bin_arr_ndim(A):
    return lambda A: 1


@overload_attribute(BinaryArrayType, 'dtype')
def overload_bool_arr_dtype(A):
    return lambda A: np.dtype('O')


@numba.njit
def pre_alloc_binary_array(n_bytestrs, n_chars):
    if n_chars is None:
        n_chars = -1
    bin_arr = init_binary_arr(bodo.libs.array_item_arr_ext.
        pre_alloc_array_item_array(np.int64(n_bytestrs), (np.int64(n_chars)
        ,), bodo.libs.str_arr_ext.char_arr_type))
    if n_chars == 0:
        bodo.libs.str_arr_ext.set_all_offsets_to_0(bin_arr)
    return bin_arr


@intrinsic
def init_binary_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, sig, args):
        iciej__mgmy, = args
        burl__eho = context.make_helper(builder, binary_array_type)
        burl__eho.data = iciej__mgmy
        context.nrt.incref(builder, data_typ, iciej__mgmy)
        return burl__eho._getvalue()
    return binary_array_type(data_typ), codegen


@intrinsic
def init_bytes_type(typingctx, data_typ, length_type):
    assert data_typ == types.Array(types.uint8, 1, 'C')
    assert length_type == types.int64

    def codegen(context, builder, sig, args):
        sft__hrw = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        uunj__scn = args[1]
        yck__zri = cgutils.create_struct_proxy(bytes_type)(context, builder)
        yck__zri.meminfo = context.nrt.meminfo_alloc(builder, uunj__scn)
        yck__zri.nitems = uunj__scn
        yck__zri.itemsize = lir.Constant(yck__zri.itemsize.type, 1)
        yck__zri.data = context.nrt.meminfo_data(builder, yck__zri.meminfo)
        yck__zri.parent = cgutils.get_null_value(yck__zri.parent.type)
        yck__zri.shape = cgutils.pack_array(builder, [uunj__scn], context.
            get_value_type(types.intp))
        yck__zri.strides = sft__hrw.strides
        cgutils.memcpy(builder, yck__zri.data, sft__hrw.data, uunj__scn)
        return yck__zri._getvalue()
    return bytes_type(data_typ, length_type), codegen


@intrinsic
def cast_bytes_uint8array(typingctx, data_typ):
    assert data_typ == bytes_type

    def codegen(context, builder, sig, args):
        return impl_ret_borrowed(context, builder, sig.return_type, args[0])
    return types.Array(types.uint8, 1, 'C')(data_typ), codegen


@intrinsic
def cast_uint8array_bytes(typingctx, data_typ):
    assert data_typ == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, sig, args):
        return impl_ret_borrowed(context, builder, sig.return_type, args[0])
    return bytes_type(data_typ), codegen


@overload_method(BinaryArrayType, 'copy', no_unliteral=True)
def binary_arr_copy_overload(arr):

    def copy_impl(arr):
        return init_binary_arr(arr._data.copy())
    return copy_impl


@overload_method(types.Bytes, 'hex')
def binary_arr_hex(arr):
    okyjp__zfpk = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def impl(arr):
        uunj__scn = len(arr) * 2
        output = numba.cpython.unicode._empty_string(okyjp__zfpk, uunj__scn, 1)
        bytes_to_hex(output, arr)
        return output
    return impl


@lower_cast(types.CPointer(types.uint8), types.voidptr)
def cast_uint8_array_to_voidptr(context, builder, fromty, toty, val):
    return val


make_attribute_wrapper(types.Bytes, 'data', '_data')


@overload_method(types.Bytes, '__hash__')
def bytes_hash(arr):

    def impl(arr):
        return numba.cpython.hashing._Py_HashBytes(arr._data, len(arr))
    return impl


@intrinsic
def bytes_to_hex(typingctx, output, arr):

    def codegen(context, builder, sig, args):
        vmbzi__gwiw = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        evxb__nkfa = cgutils.create_struct_proxy(sig.args[1])(context,
            builder, value=args[1])
        agv__fvl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(64)])
        dcqpm__boye = cgutils.get_or_insert_function(builder.module,
            agv__fvl, name='bytes_to_hex')
        builder.call(dcqpm__boye, (vmbzi__gwiw.data, evxb__nkfa.data,
            evxb__nkfa.nitems))
    return types.void(output, arr), codegen


@overload(operator.getitem, no_unliteral=True)
def binary_arr_getitem(arr, ind):
    if arr != binary_array_type:
        return
    if isinstance(ind, types.Integer):

        def impl(arr, ind):
            law__zwx = arr._data[ind]
            return init_bytes_type(law__zwx, len(law__zwx))
        return impl
    if is_list_like_index_type(ind) and (ind.dtype == types.bool_ or
        isinstance(ind.dtype, types.Integer)) or isinstance(ind, types.
        SliceType):
        return lambda arr, ind: init_binary_arr(arr._data[ind])
    raise BodoError(
        f'getitem for Binary Array with indexing type {ind} not supported.')


def bytes_fromhex(hex_str):
    pass


@overload(bytes_fromhex)
def overload_bytes_fromhex(hex_str):
    hex_str = types.unliteral(hex_str)
    if hex_str == bodo.string_type:
        okyjp__zfpk = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(hex_str):
            if not hex_str._is_ascii or hex_str._kind != okyjp__zfpk:
                raise TypeError(
                    'bytes.fromhex is only supported on ascii strings')
            iciej__mgmy = np.empty(len(hex_str) // 2, np.uint8)
            uunj__scn = _bytes_fromhex(iciej__mgmy.ctypes, hex_str._data,
                len(hex_str))
            lbgfh__jisv = init_bytes_type(iciej__mgmy, uunj__scn)
            return lbgfh__jisv
        return impl
    raise BodoError(f'bytes.fromhex not supported with argument type {hex_str}'
        )


@overload(operator.setitem)
def binary_arr_setitem(arr, ind, val):
    if arr != binary_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if val != bytes_type:
        raise BodoError(
            f'setitem for Binary Array only supported with bytes value and integer indexing'
            )
    if isinstance(ind, types.Integer):

        def impl(arr, ind, val):
            arr._data[ind] = cast_bytes_uint8array(val)
        return impl
    raise BodoError(
        f'setitem for Binary Array with indexing type {ind} not supported.')


def create_binary_cmp_op_overload(op):

    def overload_binary_cmp(lhs, rhs):
        wnxv__bhhz = lhs == binary_array_type
        sadfq__mat = rhs == binary_array_type
        lkvh__dgskc = 'lhs' if wnxv__bhhz else 'rhs'
        udfr__lwvy = 'def impl(lhs, rhs):\n'
        udfr__lwvy += '  numba.parfors.parfor.init_prange()\n'
        udfr__lwvy += f'  n = len({lkvh__dgskc})\n'
        udfr__lwvy += (
            '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(n)\n')
        udfr__lwvy += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        nzvrh__unf = []
        if wnxv__bhhz:
            nzvrh__unf.append('bodo.libs.array_kernels.isna(lhs, i)')
        if sadfq__mat:
            nzvrh__unf.append('bodo.libs.array_kernels.isna(rhs, i)')
        udfr__lwvy += f"    if {' or '.join(nzvrh__unf)}:\n"
        udfr__lwvy += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        udfr__lwvy += '      continue\n'
        cbvgz__geql = 'lhs[i]' if wnxv__bhhz else 'lhs'
        pfm__qwfqh = 'rhs[i]' if sadfq__mat else 'rhs'
        udfr__lwvy += f'    out_arr[i] = op({cbvgz__geql}, {pfm__qwfqh})\n'
        udfr__lwvy += '  return out_arr\n'
        lcvp__qjwu = {}
        exec(udfr__lwvy, {'bodo': bodo, 'numba': numba, 'op': op}, lcvp__qjwu)
        return lcvp__qjwu['impl']
    return overload_binary_cmp


lower_builtin('getiter', binary_array_type)(numba.np.arrayobj.getiter_array)


def pre_alloc_binary_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


from numba.parfors.array_analysis import ArrayAnalysis
(ArrayAnalysis._analyze_op_call_bodo_libs_binary_arr_ext_pre_alloc_binary_array
    ) = pre_alloc_binary_arr_equiv
