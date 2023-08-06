"""Nullable integer array corresponding to Pandas IntegerArray.
However, nulls are stored in bit arrays similar to Arrow's arrays.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs.str_arr_ext import kBitmask
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('mask_arr_to_bitmap', hstr_ext.mask_arr_to_bitmap)
ll.add_symbol('is_pd_int_array', array_ext.is_pd_int_array)
ll.add_symbol('int_array_from_sequence', array_ext.int_array_from_sequence)
from bodo.hiframes.datetime_timedelta_ext import pd_timedelta_type
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, check_unsupported_args, is_iterable_type, is_list_like_index_type, is_overload_false, is_overload_none, is_overload_true, parse_dtype, raise_bodo_error, to_nullable_type


class IntegerArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(IntegerArrayType, self).__init__(name=
            f'IntegerArrayType({dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return IntegerArrayType(self.dtype)

    @property
    def get_pandas_scalar_type_instance(self):
        pmhus__ckc = int(np.log2(self.dtype.bitwidth // 8))
        qgti__cuzta = 0 if self.dtype.signed else 4
        idx = pmhus__ckc + qgti__cuzta
        return pd_int_dtype_classes[idx]()


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        idvgs__frs = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, idvgs__frs)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    bpbg__wvbzx = 8 * val.dtype.itemsize
    zjz__yxmkq = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(zjz__yxmkq, bpbg__wvbzx))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        fds__bii = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(fds__bii)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    ajvd__zon = c.context.insert_const_string(c.builder.module, 'pandas')
    grw__yyaww = c.pyapi.import_module_noblock(ajvd__zon)
    vbe__cnigr = c.pyapi.call_method(grw__yyaww, str(typ)[:-2], ())
    c.pyapi.decref(grw__yyaww)
    return vbe__cnigr


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    bpbg__wvbzx = 8 * val.itemsize
    zjz__yxmkq = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(zjz__yxmkq, bpbg__wvbzx))
    return IntDtype(dtype)


def _register_int_dtype(t):
    typeof_impl.register(t)(typeof_pd_int_dtype)
    int_dtype = typeof_pd_int_dtype(t(), None)
    type_callable(t)(lambda c: lambda : int_dtype)
    lower_builtin(t)(lambda c, b, s, a: c.get_dummy_value())


pd_int_dtype_classes = (pd.Int8Dtype, pd.Int16Dtype, pd.Int32Dtype, pd.
    Int64Dtype, pd.UInt8Dtype, pd.UInt16Dtype, pd.UInt32Dtype, pd.UInt64Dtype)
for t in pd_int_dtype_classes:
    _register_int_dtype(t)


@numba.extending.register_jitable
def mask_arr_to_bitmap(mask_arr):
    n = len(mask_arr)
    gxb__qth = n + 7 >> 3
    vrclz__jvuo = np.empty(gxb__qth, np.uint8)
    for i in range(n):
        cxzti__dfsq = i // 8
        vrclz__jvuo[cxzti__dfsq] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            vrclz__jvuo[cxzti__dfsq]) & kBitmask[i % 8]
    return vrclz__jvuo


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    ogcp__ywjsf = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(ogcp__ywjsf)
    c.pyapi.decref(ogcp__ywjsf)
    droyd__gwwm = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    gxb__qth = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(64),
        7)), lir.Constant(lir.IntType(64), 8))
    mfjeh__wzn = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [gxb__qth])
    rxjo__smg = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    xfbuj__qvv = cgutils.get_or_insert_function(c.builder.module, rxjo__smg,
        name='is_pd_int_array')
    gwl__bqu = c.builder.call(xfbuj__qvv, [obj])
    ablgh__tyg = c.builder.icmp_unsigned('!=', gwl__bqu, gwl__bqu.type(0))
    with c.builder.if_else(ablgh__tyg) as (hwk__wolib, plx__evl):
        with hwk__wolib:
            zka__shby = c.pyapi.object_getattr_string(obj, '_data')
            droyd__gwwm.data = c.pyapi.to_native_value(types.Array(typ.
                dtype, 1, 'C'), zka__shby).value
            yjtv__ikpvv = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), yjtv__ikpvv).value
            c.pyapi.decref(zka__shby)
            c.pyapi.decref(yjtv__ikpvv)
            upon__qtxm = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, mask_arr)
            rxjo__smg = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            xfbuj__qvv = cgutils.get_or_insert_function(c.builder.module,
                rxjo__smg, name='mask_arr_to_bitmap')
            c.builder.call(xfbuj__qvv, [mfjeh__wzn.data, upon__qtxm.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with plx__evl:
            rudl__aqir = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            rxjo__smg = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            jraa__ltio = cgutils.get_or_insert_function(c.builder.module,
                rxjo__smg, name='int_array_from_sequence')
            c.builder.call(jraa__ltio, [obj, c.builder.bitcast(rudl__aqir.
                data, lir.IntType(8).as_pointer()), mfjeh__wzn.data])
            droyd__gwwm.data = rudl__aqir._getvalue()
    droyd__gwwm.null_bitmap = mfjeh__wzn._getvalue()
    lqym__nqrkb = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(droyd__gwwm._getvalue(), is_error=lqym__nqrkb)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    droyd__gwwm = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        droyd__gwwm.data, c.env_manager)
    nltgc__yknqa = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, droyd__gwwm.null_bitmap).data
    ogcp__ywjsf = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(ogcp__ywjsf)
    ajvd__zon = c.context.insert_const_string(c.builder.module, 'numpy')
    xhqhu__luuh = c.pyapi.import_module_noblock(ajvd__zon)
    jfyhp__tganv = c.pyapi.object_getattr_string(xhqhu__luuh, 'bool_')
    mask_arr = c.pyapi.call_method(xhqhu__luuh, 'empty', (ogcp__ywjsf,
        jfyhp__tganv))
    xgi__nswv = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    sfuqo__imd = c.pyapi.object_getattr_string(xgi__nswv, 'data')
    llpii__oyfh = c.builder.inttoptr(c.pyapi.long_as_longlong(sfuqo__imd),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as hijy__mxaac:
        i = hijy__mxaac.index
        bdjpm__ninu = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        tjtt__msgw = c.builder.load(cgutils.gep(c.builder, nltgc__yknqa,
            bdjpm__ninu))
        colt__sdavb = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(tjtt__msgw, colt__sdavb), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        fhznu__tjdas = cgutils.gep(c.builder, llpii__oyfh, i)
        c.builder.store(val, fhznu__tjdas)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        droyd__gwwm.null_bitmap)
    ajvd__zon = c.context.insert_const_string(c.builder.module, 'pandas')
    grw__yyaww = c.pyapi.import_module_noblock(ajvd__zon)
    qfp__ckd = c.pyapi.object_getattr_string(grw__yyaww, 'arrays')
    vbe__cnigr = c.pyapi.call_method(qfp__ckd, 'IntegerArray', (data, mask_arr)
        )
    c.pyapi.decref(grw__yyaww)
    c.pyapi.decref(ogcp__ywjsf)
    c.pyapi.decref(xhqhu__luuh)
    c.pyapi.decref(jfyhp__tganv)
    c.pyapi.decref(xgi__nswv)
    c.pyapi.decref(sfuqo__imd)
    c.pyapi.decref(qfp__ckd)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return vbe__cnigr


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        dlxmv__ralbz, zrae__cth = args
        droyd__gwwm = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        droyd__gwwm.data = dlxmv__ralbz
        droyd__gwwm.null_bitmap = zrae__cth
        context.nrt.incref(builder, signature.args[0], dlxmv__ralbz)
        context.nrt.incref(builder, signature.args[1], zrae__cth)
        return droyd__gwwm._getvalue()
    vfwva__tmvu = IntegerArrayType(data.dtype)
    tgsoz__pqo = vfwva__tmvu(data, null_bitmap)
    return tgsoz__pqo, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    tyjzw__nyqeu = np.empty(n, pyval.dtype.type)
    wnuoa__bdc = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        pocie__qxm = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(wnuoa__bdc, i, int(not pocie__qxm)
            )
        if not pocie__qxm:
            tyjzw__nyqeu[i] = s
    jvocw__bilw = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), tyjzw__nyqeu)
    oxqbt__shjxo = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), wnuoa__bdc)
    return lir.Constant.literal_struct([jvocw__bilw, oxqbt__shjxo])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    rdvxx__rhn = args[0]
    if equiv_set.has_shape(rdvxx__rhn):
        return ArrayAnalysis.AnalyzeResult(shape=rdvxx__rhn, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    rdvxx__rhn = args[0]
    if equiv_set.has_shape(rdvxx__rhn):
        return ArrayAnalysis.AnalyzeResult(shape=rdvxx__rhn, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_init_integer_array = (
    init_integer_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_integer_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_integer_array',
    'bodo.libs.int_arr_ext'] = alias_ext_init_integer_array
numba.core.ir_utils.alias_func_extensions['get_int_arr_data',
    'bodo.libs.int_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_int_arr_bitmap',
    'bodo.libs.int_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_int_array(n, dtype):
    tyjzw__nyqeu = np.empty(n, dtype)
    yoyhc__skw = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(tyjzw__nyqeu, yoyhc__skw)


def alloc_int_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_alloc_int_array = (
    alloc_int_array_equiv)


@numba.extending.register_jitable
def set_bit_to_arr(bits, i, bit_is_set):
    bits[i // 8] ^= np.uint8(-np.uint8(bit_is_set) ^ bits[i // 8]) & kBitmask[
        i % 8]


@numba.extending.register_jitable
def get_bit_bitmap_arr(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@overload(operator.getitem, no_unliteral=True)
def int_arr_getitem(A, ind):
    if not isinstance(A, IntegerArrayType):
        return
    if isinstance(ind, types.Integer):
        return lambda A, ind: A._data[ind]
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            tlhpa__cufq, wujj__qptp = array_getitem_bool_index(A, ind)
            return init_integer_array(tlhpa__cufq, wujj__qptp)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            tlhpa__cufq, wujj__qptp = array_getitem_int_index(A, ind)
            return init_integer_array(tlhpa__cufq, wujj__qptp)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            tlhpa__cufq, wujj__qptp = array_getitem_slice_index(A, ind)
            return init_integer_array(tlhpa__cufq, wujj__qptp)
        return impl_slice
    raise BodoError(
        f'getitem for IntegerArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def int_arr_setitem(A, idx, val):
    if not isinstance(A, IntegerArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    cdtp__zhl = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    crns__weg = isinstance(val, (types.Integer, types.Boolean, types.Float))
    if isinstance(idx, types.Integer):
        if crns__weg:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(cdtp__zhl)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or crns__weg):
        raise BodoError(cdtp__zhl)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, types.Integer):

        def impl_arr_ind_mask(A, idx, val):
            array_setitem_int_index(A, idx, val)
        return impl_arr_ind_mask
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:

        def impl_bool_ind_mask(A, idx, val):
            array_setitem_bool_index(A, idx, val)
        return impl_bool_ind_mask
    if isinstance(idx, types.SliceType):

        def impl_slice_mask(A, idx, val):
            array_setitem_slice_index(A, idx, val)
        return impl_slice_mask
    raise BodoError(
        f'setitem for IntegerArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_int_arr_len(A):
    if isinstance(A, IntegerArrayType):
        return lambda A: len(A._data)


@overload_attribute(IntegerArrayType, 'shape')
def overload_int_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(IntegerArrayType, 'dtype')
def overload_int_arr_dtype(A):
    dtype_class = getattr(pd, '{}Int{}Dtype'.format('' if A.dtype.signed else
        'U', A.dtype.bitwidth))
    return lambda A: dtype_class()


@overload_attribute(IntegerArrayType, 'ndim')
def overload_int_arr_ndim(A):
    return lambda A: 1


@overload_attribute(IntegerArrayType, 'nbytes')
def int_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(IntegerArrayType, 'copy', no_unliteral=True)
def overload_int_arr_copy(A, dtype=None):
    if not is_overload_none(dtype):
        return lambda A, dtype=None: A.astype(dtype, copy=True)
    else:
        return lambda A, dtype=None: bodo.libs.int_arr_ext.init_integer_array(
            bodo.libs.int_arr_ext.get_int_arr_data(A).copy(), bodo.libs.
            int_arr_ext.get_int_arr_bitmap(A).copy())


@overload_method(IntegerArrayType, 'astype', no_unliteral=True)
def overload_int_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "IntegerArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.NumberClass):
        dtype = dtype.dtype
    if isinstance(dtype, IntDtype) and A.dtype == dtype.dtype:
        if is_overload_false(copy):
            return lambda A, dtype, copy=True: A
        elif is_overload_true(copy):
            return lambda A, dtype, copy=True: A.copy()
        else:

            def impl(A, dtype, copy=True):
                if copy:
                    return A.copy()
                else:
                    return A
            return impl
    if isinstance(dtype, IntDtype):
        np_dtype = dtype.dtype
        return (lambda A, dtype, copy=True: bodo.libs.int_arr_ext.
            init_integer_array(bodo.libs.int_arr_ext.get_int_arr_data(A).
            astype(np_dtype), bodo.libs.int_arr_ext.get_int_arr_bitmap(A).
            copy()))
    nb_dtype = parse_dtype(dtype, 'IntegerArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.int_arr_ext.get_int_arr_data(A)
            n = len(data)
            lfhht__nhn = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                lfhht__nhn[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    lfhht__nhn[i] = np.nan
            return lfhht__nhn
        return impl_float
    return lambda A, dtype, copy=True: bodo.libs.int_arr_ext.get_int_arr_data(A
        ).astype(nb_dtype)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def apply_null_mask(arr, bitmap, mask_fill, inplace):
    assert isinstance(arr, types.Array)
    if isinstance(arr.dtype, types.Integer):
        if is_overload_none(inplace):
            return (lambda arr, bitmap, mask_fill, inplace: bodo.libs.
                int_arr_ext.init_integer_array(arr, bitmap.copy()))
        else:
            return (lambda arr, bitmap, mask_fill, inplace: bodo.libs.
                int_arr_ext.init_integer_array(arr, bitmap))
    if isinstance(arr.dtype, types.Float):

        def impl(arr, bitmap, mask_fill, inplace):
            n = len(arr)
            for i in numba.parfors.parfor.internal_prange(n):
                if not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bitmap, i):
                    arr[i] = np.nan
            return arr
        return impl
    if arr.dtype == types.bool_:

        def impl_bool(arr, bitmap, mask_fill, inplace):
            n = len(arr)
            for i in numba.parfors.parfor.internal_prange(n):
                if not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bitmap, i):
                    arr[i] = mask_fill
            return arr
        return impl_bool
    return lambda arr, bitmap, mask_fill, inplace: arr


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def merge_bitmaps(B1, B2, n, inplace):
    assert B1 == types.Array(types.uint8, 1, 'C')
    assert B2 == types.Array(types.uint8, 1, 'C')
    if not is_overload_none(inplace):

        def impl_inplace(B1, B2, n, inplace):
            for i in numba.parfors.parfor.internal_prange(n):
                iglqh__aebql = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
                pqwsn__dipnz = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
                etdx__ncj = iglqh__aebql & pqwsn__dipnz
                bodo.libs.int_arr_ext.set_bit_to_arr(B1, i, etdx__ncj)
            return B1
        return impl_inplace

    def impl(B1, B2, n, inplace):
        numba.parfors.parfor.init_prange()
        gxb__qth = n + 7 >> 3
        lfhht__nhn = np.empty(gxb__qth, np.uint8)
        for i in numba.parfors.parfor.internal_prange(n):
            iglqh__aebql = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
            pqwsn__dipnz = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
            etdx__ncj = iglqh__aebql & pqwsn__dipnz
            bodo.libs.int_arr_ext.set_bit_to_arr(lfhht__nhn, i, etdx__ncj)
        return lfhht__nhn
    return impl


ufunc_aliases = {'subtract': 'sub', 'multiply': 'mul', 'floor_divide':
    'floordiv', 'true_divide': 'truediv', 'power': 'pow', 'remainder':
    'mod', 'divide': 'div', 'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    if n_inputs == 1:

        def overload_int_arr_op_nin_1(A):
            if isinstance(A, IntegerArrayType):
                return get_nullable_array_unary_impl(op, A)
        return overload_int_arr_op_nin_1
    elif n_inputs == 2:

        def overload_series_op_nin_2(lhs, rhs):
            if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
                IntegerArrayType):
                return get_nullable_array_binary_impl(op, lhs, rhs)
        return overload_series_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for qbwxd__eeas in numba.np.ufunc_db.get_ufuncs():
        idmm__czi = create_op_overload(qbwxd__eeas, qbwxd__eeas.nin)
        overload(qbwxd__eeas, no_unliteral=True)(idmm__czi)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        idmm__czi = create_op_overload(op, 2)
        overload(op)(idmm__czi)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        idmm__czi = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(idmm__czi)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        idmm__czi = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(idmm__czi)


_install_unary_ops()


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data_tup(arrs):
    jnj__dvelt = len(arrs.types)
    tntv__liefo = 'def f(arrs):\n'
    vbe__cnigr = ', '.join('arrs[{}]._data'.format(i) for i in range(
        jnj__dvelt))
    tntv__liefo += '  return ({}{})\n'.format(vbe__cnigr, ',' if jnj__dvelt ==
        1 else '')
    yxcfz__fse = {}
    exec(tntv__liefo, {}, yxcfz__fse)
    impl = yxcfz__fse['f']
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def concat_bitmap_tup(arrs):
    jnj__dvelt = len(arrs.types)
    zsxz__xme = '+'.join('len(arrs[{}]._data)'.format(i) for i in range(
        jnj__dvelt))
    tntv__liefo = 'def f(arrs):\n'
    tntv__liefo += '  n = {}\n'.format(zsxz__xme)
    tntv__liefo += '  n_bytes = (n + 7) >> 3\n'
    tntv__liefo += '  new_mask = np.empty(n_bytes, np.uint8)\n'
    tntv__liefo += '  curr_bit = 0\n'
    for i in range(jnj__dvelt):
        tntv__liefo += '  old_mask = arrs[{}]._null_bitmap\n'.format(i)
        tntv__liefo += '  for j in range(len(arrs[{}])):\n'.format(i)
        tntv__liefo += (
            '    bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        tntv__liefo += (
            '    bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        tntv__liefo += '    curr_bit += 1\n'
    tntv__liefo += '  return new_mask\n'
    yxcfz__fse = {}
    exec(tntv__liefo, {'np': np, 'bodo': bodo}, yxcfz__fse)
    impl = yxcfz__fse['f']
    return impl


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    yibn__rkrr = dict(skipna=skipna, min_count=min_count)
    sgih__nrmv = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', yibn__rkrr, sgih__nrmv)

    def impl(A, skipna=True, min_count=0):
        numba.parfors.parfor.init_prange()
        s = 0
        for i in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, i):
                val = A[i]
            s += val
        return s
    return impl


@overload_method(IntegerArrayType, 'unique', no_unliteral=True)
def overload_unique(A):
    dtype = A.dtype

    def impl_int_arr(A):
        data = []
        colt__sdavb = []
        zoiwk__nsakl = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not zoiwk__nsakl:
                    data.append(dtype(1))
                    colt__sdavb.append(False)
                    zoiwk__nsakl = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                colt__sdavb.append(True)
        tlhpa__cufq = np.array(data)
        n = len(tlhpa__cufq)
        gxb__qth = n + 7 >> 3
        wujj__qptp = np.empty(gxb__qth, np.uint8)
        for bdl__mcn in range(n):
            set_bit_to_arr(wujj__qptp, bdl__mcn, colt__sdavb[bdl__mcn])
        return init_integer_array(tlhpa__cufq, wujj__qptp)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    zxlz__odf = numba.core.registry.cpu_target.typing_context
    xdrks__nktn = zxlz__odf.resolve_function_type(op, (types.Array(A.dtype,
        1, 'C'),), {}).return_type
    xdrks__nktn = to_nullable_type(xdrks__nktn)

    def impl(A):
        n = len(A)
        fkj__mzwn = bodo.utils.utils.alloc_type(n, xdrks__nktn, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(fkj__mzwn, i)
                continue
            fkj__mzwn[i] = op(A[i])
        return fkj__mzwn
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    inplace = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    lft__oyvsr = isinstance(lhs, (types.Number, types.Boolean))
    tys__czpoc = isinstance(rhs, (types.Number, types.Boolean))
    bag__ukie = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    xiud__efm = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    zxlz__odf = numba.core.registry.cpu_target.typing_context
    xdrks__nktn = zxlz__odf.resolve_function_type(op, (bag__ukie, xiud__efm
        ), {}).return_type
    xdrks__nktn = to_nullable_type(xdrks__nktn)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    xhjx__lmagk = 'lhs' if lft__oyvsr else 'lhs[i]'
    wxmsb__ncby = 'rhs' if tys__czpoc else 'rhs[i]'
    giwq__kcutr = ('False' if lft__oyvsr else
        'bodo.libs.array_kernels.isna(lhs, i)')
    mxwlv__qlm = ('False' if tys__czpoc else
        'bodo.libs.array_kernels.isna(rhs, i)')
    tntv__liefo = 'def impl(lhs, rhs):\n'
    tntv__liefo += '  n = len({})\n'.format('lhs' if not lft__oyvsr else 'rhs')
    if inplace:
        tntv__liefo += '  out_arr = {}\n'.format('lhs' if not lft__oyvsr else
            'rhs')
    else:
        tntv__liefo += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    tntv__liefo += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    tntv__liefo += '    if ({}\n'.format(giwq__kcutr)
    tntv__liefo += '        or {}):\n'.format(mxwlv__qlm)
    tntv__liefo += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    tntv__liefo += '      continue\n'
    tntv__liefo += (
        '    out_arr[i] = bodo.utils.conversion.unbox_if_timestamp(op({}, {}))\n'
        .format(xhjx__lmagk, wxmsb__ncby))
    tntv__liefo += '  return out_arr\n'
    yxcfz__fse = {}
    exec(tntv__liefo, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        xdrks__nktn, 'op': op}, yxcfz__fse)
    impl = yxcfz__fse['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        lft__oyvsr = lhs in [pd_timedelta_type]
        tys__czpoc = rhs in [pd_timedelta_type]
        if lft__oyvsr:

            def impl(lhs, rhs):
                n = len(rhs)
                fkj__mzwn = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(fkj__mzwn, i)
                        continue
                    fkj__mzwn[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs, rhs[i]))
                return fkj__mzwn
            return impl
        elif tys__czpoc:

            def impl(lhs, rhs):
                n = len(lhs)
                fkj__mzwn = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(fkj__mzwn, i)
                        continue
                    fkj__mzwn[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs[i], rhs))
                return fkj__mzwn
            return impl
    return impl
