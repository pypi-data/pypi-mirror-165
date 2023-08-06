import operator
import re
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, bound_function, infer_getattr, infer_global, signature
from numba.extending import intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, register_jitable, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs import hstr_ext
from bodo.utils.typing import BodoError, get_overload_const_int, get_overload_const_str, is_overload_constant_int, is_overload_constant_str


def unliteral_all(args):
    return tuple(types.unliteral(a) for a in args)


ll.add_symbol('del_str', hstr_ext.del_str)
ll.add_symbol('unicode_to_utf8', hstr_ext.unicode_to_utf8)
ll.add_symbol('memcmp', hstr_ext.memcmp)
ll.add_symbol('int_to_hex', hstr_ext.int_to_hex)
string_type = types.unicode_type


@numba.njit
def contains_regex(e, in_str):
    with numba.objmode(res='bool_'):
        res = bool(e.search(in_str))
    return res


@numba.generated_jit
def str_findall_count(regex, in_str):

    def _str_findall_count_impl(regex, in_str):
        with numba.objmode(res='int64'):
            res = len(regex.findall(in_str))
        return res
    return _str_findall_count_impl


utf8_str_type = types.ArrayCTypes(types.Array(types.uint8, 1, 'C'))


@intrinsic
def unicode_to_utf8_and_len(typingctx, str_typ):
    assert str_typ in (string_type, types.Optional(string_type)) or isinstance(
        str_typ, types.StringLiteral)
    oxkh__xjghm = types.Tuple([utf8_str_type, types.int64])

    def codegen(context, builder, sig, args):
        ulp__woe, = args
        jmiuq__lztx = cgutils.create_struct_proxy(string_type)(context,
            builder, value=ulp__woe)
        izox__yhf = cgutils.create_struct_proxy(utf8_str_type)(context, builder
            )
        qcclb__eot = cgutils.create_struct_proxy(oxkh__xjghm)(context, builder)
        is_ascii = builder.icmp_unsigned('==', jmiuq__lztx.is_ascii, lir.
            Constant(jmiuq__lztx.is_ascii.type, 1))
        with builder.if_else(is_ascii) as (uyl__ibg, luep__vjhs):
            with uyl__ibg:
                context.nrt.incref(builder, string_type, ulp__woe)
                izox__yhf.data = jmiuq__lztx.data
                izox__yhf.meminfo = jmiuq__lztx.meminfo
                qcclb__eot.f1 = jmiuq__lztx.length
            with luep__vjhs:
                ptew__adhn = lir.FunctionType(lir.IntType(64), [lir.IntType
                    (8).as_pointer(), lir.IntType(8).as_pointer(), lir.
                    IntType(64), lir.IntType(32)])
                pomeh__craxo = cgutils.get_or_insert_function(builder.
                    module, ptew__adhn, name='unicode_to_utf8')
                kjmzf__ulnaf = context.get_constant_null(types.voidptr)
                nccw__zobm = builder.call(pomeh__craxo, [kjmzf__ulnaf,
                    jmiuq__lztx.data, jmiuq__lztx.length, jmiuq__lztx.kind])
                qcclb__eot.f1 = nccw__zobm
                ruf__eiihr = builder.add(nccw__zobm, lir.Constant(lir.
                    IntType(64), 1))
                izox__yhf.meminfo = context.nrt.meminfo_alloc_aligned(builder,
                    size=ruf__eiihr, align=32)
                izox__yhf.data = context.nrt.meminfo_data(builder,
                    izox__yhf.meminfo)
                builder.call(pomeh__craxo, [izox__yhf.data, jmiuq__lztx.
                    data, jmiuq__lztx.length, jmiuq__lztx.kind])
                builder.store(lir.Constant(lir.IntType(8), 0), builder.gep(
                    izox__yhf.data, [nccw__zobm]))
        qcclb__eot.f0 = izox__yhf._getvalue()
        return qcclb__eot._getvalue()
    return oxkh__xjghm(string_type), codegen


def unicode_to_utf8(s):
    return s


@overload(unicode_to_utf8)
def overload_unicode_to_utf8(s):
    return lambda s: unicode_to_utf8_and_len(s)[0]


@overload(max)
def overload_builtin_max(lhs, rhs):
    if lhs == types.unicode_type and rhs == types.unicode_type:

        def impl(lhs, rhs):
            return lhs if lhs > rhs else rhs
        return impl


@overload(min)
def overload_builtin_min(lhs, rhs):
    if lhs == types.unicode_type and rhs == types.unicode_type:

        def impl(lhs, rhs):
            return lhs if lhs < rhs else rhs
        return impl


@intrinsic
def memcmp(typingctx, dest_t, src_t, count_t=None):

    def codegen(context, builder, sig, args):
        ptew__adhn = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
        czl__hfe = cgutils.get_or_insert_function(builder.module,
            ptew__adhn, name='memcmp')
        return builder.call(czl__hfe, args)
    return types.int32(types.voidptr, types.voidptr, types.intp), codegen


def int_to_str_len(n):
    return len(str(n))


@overload(int_to_str_len)
def overload_int_to_str_len(n):
    levq__kkf = n(10)

    def impl(n):
        if n == 0:
            return 1
        pnp__ztxy = 0
        if n < 0:
            n = -n
            pnp__ztxy += 1
        while n > 0:
            n = n // levq__kkf
            pnp__ztxy += 1
        return pnp__ztxy
    return impl


class StdStringType(types.Opaque):

    def __init__(self):
        super(StdStringType, self).__init__(name='StdStringType')


std_str_type = StdStringType()
register_model(StdStringType)(models.OpaqueModel)
del_str = types.ExternalFunction('del_str', types.void(std_str_type))
get_c_str = types.ExternalFunction('get_c_str', types.voidptr(std_str_type))
dummy_use = numba.njit(lambda a: None)


@overload(int)
def int_str_overload(in_str, base=10):
    if in_str == string_type:
        if is_overload_constant_int(base) and get_overload_const_int(base
            ) == 10:

            def _str_to_int_impl(in_str, base=10):
                val = _str_to_int64(in_str._data, in_str._length)
                dummy_use(in_str)
                return val
            return _str_to_int_impl

        def _str_to_int_base_impl(in_str, base=10):
            val = _str_to_int64_base(in_str._data, in_str._length, base)
            dummy_use(in_str)
            return val
        return _str_to_int_base_impl


@infer_global(float)
class StrToFloat(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        [ducw__uxmig] = args
        if isinstance(ducw__uxmig, StdStringType):
            return signature(types.float64, ducw__uxmig)
        if ducw__uxmig == string_type:
            return signature(types.float64, ducw__uxmig)


ll.add_symbol('init_string_const', hstr_ext.init_string_const)
ll.add_symbol('get_c_str', hstr_ext.get_c_str)
ll.add_symbol('str_to_int64', hstr_ext.str_to_int64)
ll.add_symbol('str_to_uint64', hstr_ext.str_to_uint64)
ll.add_symbol('str_to_int64_base', hstr_ext.str_to_int64_base)
ll.add_symbol('str_to_float64', hstr_ext.str_to_float64)
ll.add_symbol('str_to_float32', hstr_ext.str_to_float32)
ll.add_symbol('get_str_len', hstr_ext.get_str_len)
ll.add_symbol('str_from_float32', hstr_ext.str_from_float32)
ll.add_symbol('str_from_float64', hstr_ext.str_from_float64)
get_std_str_len = types.ExternalFunction('get_str_len', signature(types.
    intp, std_str_type))
init_string_from_chars = types.ExternalFunction('init_string_const',
    std_str_type(types.voidptr, types.intp))
_str_to_int64 = types.ExternalFunction('str_to_int64', signature(types.
    int64, types.voidptr, types.int64))
_str_to_uint64 = types.ExternalFunction('str_to_uint64', signature(types.
    uint64, types.voidptr, types.int64))
_str_to_int64_base = types.ExternalFunction('str_to_int64_base', signature(
    types.int64, types.voidptr, types.int64, types.int64))


def gen_unicode_to_std_str(context, builder, unicode_val):
    jmiuq__lztx = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    ptew__adhn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType
        (8).as_pointer(), lir.IntType(64)])
    bab__bjimg = cgutils.get_or_insert_function(builder.module, ptew__adhn,
        name='init_string_const')
    return builder.call(bab__bjimg, [jmiuq__lztx.data, jmiuq__lztx.length])


def gen_std_str_to_unicode(context, builder, std_str_val, del_str=False):
    kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def _std_str_to_unicode(std_str):
        length = bodo.libs.str_ext.get_std_str_len(std_str)
        tmvsy__eub = numba.cpython.unicode._empty_string(kind, length, 1)
        bodo.libs.str_arr_ext._memcpy(tmvsy__eub._data, bodo.libs.str_ext.
            get_c_str(std_str), length, 1)
        if del_str:
            bodo.libs.str_ext.del_str(std_str)
        return tmvsy__eub
    val = context.compile_internal(builder, _std_str_to_unicode,
        string_type(bodo.libs.str_ext.std_str_type), [std_str_val])
    return val


def gen_get_unicode_chars(context, builder, unicode_val):
    jmiuq__lztx = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    return jmiuq__lztx.data


@intrinsic
def unicode_to_std_str(typingctx, unicode_t=None):

    def codegen(context, builder, sig, args):
        return gen_unicode_to_std_str(context, builder, args[0])
    return std_str_type(string_type), codegen


@intrinsic
def std_str_to_unicode(typingctx, unicode_t=None):

    def codegen(context, builder, sig, args):
        return gen_std_str_to_unicode(context, builder, args[0], True)
    return string_type(std_str_type), codegen


class RandomAccessStringArrayType(types.ArrayCompatible):

    def __init__(self):
        super(RandomAccessStringArrayType, self).__init__(name=
            'RandomAccessStringArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_type

    def copy(self):
        RandomAccessStringArrayType()


random_access_string_array = RandomAccessStringArrayType()


@register_model(RandomAccessStringArrayType)
class RandomAccessStringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        mrutq__iqjqv = [('data', types.List(string_type))]
        models.StructModel.__init__(self, dmm, fe_type, mrutq__iqjqv)


make_attribute_wrapper(RandomAccessStringArrayType, 'data', '_data')


@intrinsic
def alloc_random_access_string_array(typingctx, n_t=None):

    def codegen(context, builder, sig, args):
        oireq__ecwt, = args
        utf__kkyyn = types.List(string_type)
        ifihv__sdv = numba.cpython.listobj.ListInstance.allocate(context,
            builder, utf__kkyyn, oireq__ecwt)
        ifihv__sdv.size = oireq__ecwt
        yzzw__dldm = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        yzzw__dldm.data = ifihv__sdv.value
        return yzzw__dldm._getvalue()
    return random_access_string_array(types.intp), codegen


@overload(operator.getitem, no_unliteral=True)
def random_access_str_arr_getitem(A, ind):
    if A != random_access_string_array:
        return
    if isinstance(ind, types.Integer):
        return lambda A, ind: A._data[ind]


@overload(operator.setitem)
def random_access_str_arr_setitem(A, idx, val):
    if A != random_access_string_array:
        return
    if isinstance(idx, types.Integer):
        assert val == string_type

        def impl_scalar(A, idx, val):
            A._data[idx] = val
        return impl_scalar


@overload(len, no_unliteral=True)
def overload_str_arr_len(A):
    if A == random_access_string_array:
        return lambda A: len(A._data)


@overload_attribute(RandomAccessStringArrayType, 'shape')
def overload_str_arr_shape(A):
    return lambda A: (len(A._data),)


def alloc_random_access_str_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_libs_str_ext_alloc_random_access_string_array
    ) = alloc_random_access_str_arr_equiv
str_from_float32 = types.ExternalFunction('str_from_float32', types.void(
    types.voidptr, types.float32))
str_from_float64 = types.ExternalFunction('str_from_float64', types.void(
    types.voidptr, types.float64))


def float_to_str(s, v):
    pass


@overload(float_to_str)
def float_to_str_overload(s, v):
    assert isinstance(v, types.Float)
    if v == types.float32:
        return lambda s, v: str_from_float32(s._data, v)
    return lambda s, v: str_from_float64(s._data, v)


@overload(str)
def float_str_overload(v):
    if isinstance(v, types.Float):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(v):
            if v == 0:
                return '0.0'
            wbe__ivaz = 0
            hbcw__ghsi = v
            if hbcw__ghsi < 0:
                wbe__ivaz = 1
                hbcw__ghsi = -hbcw__ghsi
            if hbcw__ghsi < 1:
                lcrda__qzvr = 1
            else:
                lcrda__qzvr = 1 + int(np.floor(np.log10(hbcw__ghsi)))
            length = wbe__ivaz + lcrda__qzvr + 1 + 6
            s = numba.cpython.unicode._malloc_string(kind, 1, length, True)
            float_to_str(s, v)
            return s
        return impl


@overload(format, no_unliteral=True)
def overload_format(value, format_spec=''):
    if is_overload_constant_str(format_spec) and get_overload_const_str(
        format_spec) == '':

        def impl_fast(value, format_spec=''):
            return str(value)
        return impl_fast

    def impl(value, format_spec=''):
        with numba.objmode(res='string'):
            res = format(value, format_spec)
        return res
    return impl


@lower_cast(StdStringType, types.float64)
def cast_str_to_float64(context, builder, fromty, toty, val):
    ptew__adhn = lir.FunctionType(lir.DoubleType(), [lir.IntType(8).
        as_pointer()])
    bab__bjimg = cgutils.get_or_insert_function(builder.module, ptew__adhn,
        name='str_to_float64')
    res = builder.call(bab__bjimg, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(StdStringType, types.float32)
def cast_str_to_float32(context, builder, fromty, toty, val):
    ptew__adhn = lir.FunctionType(lir.FloatType(), [lir.IntType(8).
        as_pointer()])
    bab__bjimg = cgutils.get_or_insert_function(builder.module, ptew__adhn,
        name='str_to_float32')
    res = builder.call(bab__bjimg, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.float64)
def cast_unicode_str_to_float64(context, builder, fromty, toty, val):
    std_str = gen_unicode_to_std_str(context, builder, val)
    return cast_str_to_float64(context, builder, std_str_type, toty, std_str)


@lower_cast(string_type, types.float32)
def cast_unicode_str_to_float32(context, builder, fromty, toty, val):
    std_str = gen_unicode_to_std_str(context, builder, val)
    return cast_str_to_float32(context, builder, std_str_type, toty, std_str)


@lower_cast(string_type, types.int64)
@lower_cast(string_type, types.int32)
@lower_cast(string_type, types.int16)
@lower_cast(string_type, types.int8)
def cast_unicode_str_to_int64(context, builder, fromty, toty, val):
    jmiuq__lztx = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    ptew__adhn = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(
        8).as_pointer(), lir.IntType(64)])
    bab__bjimg = cgutils.get_or_insert_function(builder.module, ptew__adhn,
        name='str_to_int64')
    res = builder.call(bab__bjimg, (jmiuq__lztx.data, jmiuq__lztx.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.uint64)
@lower_cast(string_type, types.uint32)
@lower_cast(string_type, types.uint16)
@lower_cast(string_type, types.uint8)
def cast_unicode_str_to_uint64(context, builder, fromty, toty, val):
    jmiuq__lztx = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    ptew__adhn = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(
        8).as_pointer(), lir.IntType(64)])
    bab__bjimg = cgutils.get_or_insert_function(builder.module, ptew__adhn,
        name='str_to_uint64')
    res = builder.call(bab__bjimg, (jmiuq__lztx.data, jmiuq__lztx.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@infer_getattr
class StringAttribute(AttributeTemplate):
    key = types.UnicodeType

    @bound_function('str.format', no_unliteral=True)
    def resolve_format(self, string_typ, args, kws):
        kws = dict(kws)
        coemx__okja = ', '.join('e{}'.format(wtggk__sai) for wtggk__sai in
            range(len(args)))
        if coemx__okja:
            coemx__okja += ', '
        yvcr__gsx = ', '.join("{} = ''".format(a) for a in kws.keys())
        hlla__pgi = f'def format_stub(string, {coemx__okja} {yvcr__gsx}):\n'
        hlla__pgi += '    pass\n'
        zxbw__cqj = {}
        exec(hlla__pgi, {}, zxbw__cqj)
        okjr__eusk = zxbw__cqj['format_stub']
        zez__ybww = numba.core.utils.pysignature(okjr__eusk)
        vrvzu__kskgc = (string_typ,) + args + tuple(kws.values())
        return signature(string_typ, vrvzu__kskgc).replace(pysig=zez__ybww)


@numba.njit(cache=True)
def str_split(arr, pat, n):
    vyjw__cmqpp = pat is not None and len(pat) > 1
    if vyjw__cmqpp:
        xgmm__chxab = re.compile(pat)
        if n == -1:
            n = 0
    elif n == 0:
        n = -1
    ifihv__sdv = len(arr)
    luqu__gdz = 0
    jwovn__zyl = 0
    for wtggk__sai in numba.parfors.parfor.internal_prange(ifihv__sdv):
        if bodo.libs.array_kernels.isna(arr, wtggk__sai):
            continue
        if vyjw__cmqpp:
            vxi__jbaga = xgmm__chxab.split(arr[wtggk__sai], maxsplit=n)
        elif pat == '':
            vxi__jbaga = [''] + list(arr[wtggk__sai]) + ['']
        else:
            vxi__jbaga = arr[wtggk__sai].split(pat, n)
        luqu__gdz += len(vxi__jbaga)
        for s in vxi__jbaga:
            jwovn__zyl += bodo.libs.str_arr_ext.get_utf8_size(s)
    srwag__qsqdl = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        ifihv__sdv, (luqu__gdz, jwovn__zyl), bodo.libs.str_arr_ext.
        string_array_type)
    fpxn__fdpw = bodo.libs.array_item_arr_ext.get_offsets(srwag__qsqdl)
    fghh__utxg = bodo.libs.array_item_arr_ext.get_null_bitmap(srwag__qsqdl)
    omwlo__ljevk = bodo.libs.array_item_arr_ext.get_data(srwag__qsqdl)
    ndyuh__jcm = 0
    for nauw__glj in numba.parfors.parfor.internal_prange(ifihv__sdv):
        fpxn__fdpw[nauw__glj] = ndyuh__jcm
        if bodo.libs.array_kernels.isna(arr, nauw__glj):
            bodo.libs.int_arr_ext.set_bit_to_arr(fghh__utxg, nauw__glj, 0)
            continue
        bodo.libs.int_arr_ext.set_bit_to_arr(fghh__utxg, nauw__glj, 1)
        if vyjw__cmqpp:
            vxi__jbaga = xgmm__chxab.split(arr[nauw__glj], maxsplit=n)
        elif pat == '':
            vxi__jbaga = [''] + list(arr[nauw__glj]) + ['']
        else:
            vxi__jbaga = arr[nauw__glj].split(pat, n)
        wrqa__wvczt = len(vxi__jbaga)
        for tauz__xfioj in range(wrqa__wvczt):
            s = vxi__jbaga[tauz__xfioj]
            omwlo__ljevk[ndyuh__jcm] = s
            ndyuh__jcm += 1
    fpxn__fdpw[ifihv__sdv] = ndyuh__jcm
    return srwag__qsqdl


@overload(hex)
def overload_hex(x):
    if isinstance(x, types.Integer):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(x):
            x = np.int64(x)
            if x < 0:
                gdh__nmb = '-0x'
                x = x * -1
            else:
                gdh__nmb = '0x'
            x = np.uint64(x)
            if x == 0:
                hry__tdhek = 1
            else:
                hry__tdhek = fast_ceil_log2(x + 1)
                hry__tdhek = (hry__tdhek + 3) // 4
            length = len(gdh__nmb) + hry__tdhek
            output = numba.cpython.unicode._empty_string(kind, length, 1)
            bodo.libs.str_arr_ext._memcpy(output._data, gdh__nmb._data, len
                (gdh__nmb), 1)
            int_to_hex(output, hry__tdhek, len(gdh__nmb), x)
            return output
        return impl


@register_jitable
def fast_ceil_log2(x):
    otrf__zvtj = 0 if x & x - 1 == 0 else 1
    qfw__ihdd = [np.uint64(18446744069414584320), np.uint64(4294901760), np
        .uint64(65280), np.uint64(240), np.uint64(12), np.uint64(2)]
    tmvqt__cnsx = 32
    for wtggk__sai in range(len(qfw__ihdd)):
        esg__rnll = 0 if x & qfw__ihdd[wtggk__sai] == 0 else tmvqt__cnsx
        otrf__zvtj = otrf__zvtj + esg__rnll
        x = x >> esg__rnll
        tmvqt__cnsx = tmvqt__cnsx >> 1
    return otrf__zvtj


@intrinsic
def int_to_hex(typingctx, output, out_len, header_len, int_val):

    def codegen(context, builder, sig, args):
        output, out_len, header_len, int_val = args
        ghjc__vevum = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=output)
        ptew__adhn = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(64)])
        pmji__hyqw = cgutils.get_or_insert_function(builder.module,
            ptew__adhn, name='int_to_hex')
        smo__csfw = builder.inttoptr(builder.add(builder.ptrtoint(
            ghjc__vevum.data, lir.IntType(64)), header_len), lir.IntType(8)
            .as_pointer())
        builder.call(pmji__hyqw, (smo__csfw, out_len, int_val))
    return types.void(output, out_len, header_len, int_val), codegen


def alloc_empty_bytes_or_string_data(typ, kind, length, is_ascii=0):
    pass


@overload(alloc_empty_bytes_or_string_data)
def overload_alloc_empty_bytes_or_string_data(typ, kind, length, is_ascii=0):
    typ = typ.instance_type if isinstance(typ, types.TypeRef) else typ
    if typ == bodo.bytes_type:
        return lambda typ, kind, length, is_ascii=0: np.empty(length, np.uint8)
    if typ == string_type:
        return (lambda typ, kind, length, is_ascii=0: numba.cpython.unicode
            ._empty_string(kind, length, is_ascii))
    raise BodoError(
        f'Internal Error: Expected Bytes or String type, found {typ}')


def get_unicode_or_numpy_data(val):
    pass


@overload(get_unicode_or_numpy_data)
def overload_get_unicode_or_numpy_data(val):
    if val == string_type:
        return lambda val: val._data
    if isinstance(val, types.Array):
        return lambda val: val.ctypes
    raise BodoError(
        f'Internal Error: Expected String or Numpy Array, found {val}')
