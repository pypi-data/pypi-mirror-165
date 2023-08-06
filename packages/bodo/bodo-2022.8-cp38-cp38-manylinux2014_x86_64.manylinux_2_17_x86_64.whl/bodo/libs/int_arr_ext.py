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
        dwiyq__vtpkh = int(np.log2(self.dtype.bitwidth // 8))
        runy__yzyx = 0 if self.dtype.signed else 4
        idx = dwiyq__vtpkh + runy__yzyx
        return pd_int_dtype_classes[idx]()


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wpa__vmvmw = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, wpa__vmvmw)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    oxtoz__pyzt = 8 * val.dtype.itemsize
    iaq__agzp = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(iaq__agzp, oxtoz__pyzt))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        vacx__qomka = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(vacx__qomka)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    dwmjo__hdkwz = c.context.insert_const_string(c.builder.module, 'pandas')
    jvk__svo = c.pyapi.import_module_noblock(dwmjo__hdkwz)
    mpb__vjvax = c.pyapi.call_method(jvk__svo, str(typ)[:-2], ())
    c.pyapi.decref(jvk__svo)
    return mpb__vjvax


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    oxtoz__pyzt = 8 * val.itemsize
    iaq__agzp = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(iaq__agzp, oxtoz__pyzt))
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
    cxl__sff = n + 7 >> 3
    rjepg__att = np.empty(cxl__sff, np.uint8)
    for i in range(n):
        eaeyb__xyrh = i // 8
        rjepg__att[eaeyb__xyrh] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            rjepg__att[eaeyb__xyrh]) & kBitmask[i % 8]
    return rjepg__att


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    rdpz__sqke = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(rdpz__sqke)
    c.pyapi.decref(rdpz__sqke)
    sie__kxelf = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    cxl__sff = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(64),
        7)), lir.Constant(lir.IntType(64), 8))
    ydxe__jwing = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [cxl__sff])
    iaoi__lblws = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    qld__apwh = cgutils.get_or_insert_function(c.builder.module,
        iaoi__lblws, name='is_pd_int_array')
    jio__ehtln = c.builder.call(qld__apwh, [obj])
    eay__xgqjh = c.builder.icmp_unsigned('!=', jio__ehtln, jio__ehtln.type(0))
    with c.builder.if_else(eay__xgqjh) as (vmk__zyoao, rrj__zkyt):
        with vmk__zyoao:
            vjdj__sbqux = c.pyapi.object_getattr_string(obj, '_data')
            sie__kxelf.data = c.pyapi.to_native_value(types.Array(typ.dtype,
                1, 'C'), vjdj__sbqux).value
            jhpo__sumyf = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), jhpo__sumyf).value
            c.pyapi.decref(vjdj__sbqux)
            c.pyapi.decref(jhpo__sumyf)
            yfzmg__wuqsa = c.context.make_array(types.Array(types.bool_, 1,
                'C'))(c.context, c.builder, mask_arr)
            iaoi__lblws = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            qld__apwh = cgutils.get_or_insert_function(c.builder.module,
                iaoi__lblws, name='mask_arr_to_bitmap')
            c.builder.call(qld__apwh, [ydxe__jwing.data, yfzmg__wuqsa.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with rrj__zkyt:
            chpbt__bmy = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            iaoi__lblws = lir.FunctionType(lir.IntType(32), [lir.IntType(8)
                .as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            ylkld__ske = cgutils.get_or_insert_function(c.builder.module,
                iaoi__lblws, name='int_array_from_sequence')
            c.builder.call(ylkld__ske, [obj, c.builder.bitcast(chpbt__bmy.
                data, lir.IntType(8).as_pointer()), ydxe__jwing.data])
            sie__kxelf.data = chpbt__bmy._getvalue()
    sie__kxelf.null_bitmap = ydxe__jwing._getvalue()
    rfrqd__kgzce = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(sie__kxelf._getvalue(), is_error=rfrqd__kgzce)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    sie__kxelf = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        sie__kxelf.data, c.env_manager)
    xppf__tjii = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, sie__kxelf.null_bitmap).data
    rdpz__sqke = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(rdpz__sqke)
    dwmjo__hdkwz = c.context.insert_const_string(c.builder.module, 'numpy')
    loyl__qsbu = c.pyapi.import_module_noblock(dwmjo__hdkwz)
    ldnzg__untt = c.pyapi.object_getattr_string(loyl__qsbu, 'bool_')
    mask_arr = c.pyapi.call_method(loyl__qsbu, 'empty', (rdpz__sqke,
        ldnzg__untt))
    hydrb__hpur = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    yya__hpt = c.pyapi.object_getattr_string(hydrb__hpur, 'data')
    eqp__kcw = c.builder.inttoptr(c.pyapi.long_as_longlong(yya__hpt), lir.
        IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as tpgu__vkk:
        i = tpgu__vkk.index
        kecec__jhst = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        axuab__dpi = c.builder.load(cgutils.gep(c.builder, xppf__tjii,
            kecec__jhst))
        jkq__ayuxt = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(axuab__dpi, jkq__ayuxt), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        yag__fnw = cgutils.gep(c.builder, eqp__kcw, i)
        c.builder.store(val, yag__fnw)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        sie__kxelf.null_bitmap)
    dwmjo__hdkwz = c.context.insert_const_string(c.builder.module, 'pandas')
    jvk__svo = c.pyapi.import_module_noblock(dwmjo__hdkwz)
    okxg__wmr = c.pyapi.object_getattr_string(jvk__svo, 'arrays')
    mpb__vjvax = c.pyapi.call_method(okxg__wmr, 'IntegerArray', (data,
        mask_arr))
    c.pyapi.decref(jvk__svo)
    c.pyapi.decref(rdpz__sqke)
    c.pyapi.decref(loyl__qsbu)
    c.pyapi.decref(ldnzg__untt)
    c.pyapi.decref(hydrb__hpur)
    c.pyapi.decref(yya__hpt)
    c.pyapi.decref(okxg__wmr)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return mpb__vjvax


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        zur__khbw, ptnfd__qfo = args
        sie__kxelf = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        sie__kxelf.data = zur__khbw
        sie__kxelf.null_bitmap = ptnfd__qfo
        context.nrt.incref(builder, signature.args[0], zur__khbw)
        context.nrt.incref(builder, signature.args[1], ptnfd__qfo)
        return sie__kxelf._getvalue()
    tqz__nlyzd = IntegerArrayType(data.dtype)
    fvcf__emf = tqz__nlyzd(data, null_bitmap)
    return fvcf__emf, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    tpcd__kavw = np.empty(n, pyval.dtype.type)
    soccj__dhng = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        fuib__soht = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(soccj__dhng, i, int(not
            fuib__soht))
        if not fuib__soht:
            tpcd__kavw[i] = s
    hmi__mpizc = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), tpcd__kavw)
    jek__aewhn = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), soccj__dhng)
    return lir.Constant.literal_struct([hmi__mpizc, jek__aewhn])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    dzoov__tmohg = args[0]
    if equiv_set.has_shape(dzoov__tmohg):
        return ArrayAnalysis.AnalyzeResult(shape=dzoov__tmohg, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    dzoov__tmohg = args[0]
    if equiv_set.has_shape(dzoov__tmohg):
        return ArrayAnalysis.AnalyzeResult(shape=dzoov__tmohg, pre=[])
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
    tpcd__kavw = np.empty(n, dtype)
    tomr__flaf = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(tpcd__kavw, tomr__flaf)


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
            tflfk__ajccs, mpx__gnyl = array_getitem_bool_index(A, ind)
            return init_integer_array(tflfk__ajccs, mpx__gnyl)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            tflfk__ajccs, mpx__gnyl = array_getitem_int_index(A, ind)
            return init_integer_array(tflfk__ajccs, mpx__gnyl)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            tflfk__ajccs, mpx__gnyl = array_getitem_slice_index(A, ind)
            return init_integer_array(tflfk__ajccs, mpx__gnyl)
        return impl_slice
    raise BodoError(
        f'getitem for IntegerArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def int_arr_setitem(A, idx, val):
    if not isinstance(A, IntegerArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    dylj__femb = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    takbi__vjnr = isinstance(val, (types.Integer, types.Boolean, types.Float))
    if isinstance(idx, types.Integer):
        if takbi__vjnr:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(dylj__femb)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or takbi__vjnr):
        raise BodoError(dylj__femb)
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
            owwj__kbu = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                owwj__kbu[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    owwj__kbu[i] = np.nan
            return owwj__kbu
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
                hpjgp__mbqr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
                uurm__rvkz = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
                qeh__levd = hpjgp__mbqr & uurm__rvkz
                bodo.libs.int_arr_ext.set_bit_to_arr(B1, i, qeh__levd)
            return B1
        return impl_inplace

    def impl(B1, B2, n, inplace):
        numba.parfors.parfor.init_prange()
        cxl__sff = n + 7 >> 3
        owwj__kbu = np.empty(cxl__sff, np.uint8)
        for i in numba.parfors.parfor.internal_prange(n):
            hpjgp__mbqr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
            uurm__rvkz = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
            qeh__levd = hpjgp__mbqr & uurm__rvkz
            bodo.libs.int_arr_ext.set_bit_to_arr(owwj__kbu, i, qeh__levd)
        return owwj__kbu
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
    for sab__nbjr in numba.np.ufunc_db.get_ufuncs():
        lcqw__guu = create_op_overload(sab__nbjr, sab__nbjr.nin)
        overload(sab__nbjr, no_unliteral=True)(lcqw__guu)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        lcqw__guu = create_op_overload(op, 2)
        overload(op)(lcqw__guu)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        lcqw__guu = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(lcqw__guu)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        lcqw__guu = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(lcqw__guu)


_install_unary_ops()


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data_tup(arrs):
    wlfyp__npsk = len(arrs.types)
    qetry__mbhb = 'def f(arrs):\n'
    mpb__vjvax = ', '.join('arrs[{}]._data'.format(i) for i in range(
        wlfyp__npsk))
    qetry__mbhb += '  return ({}{})\n'.format(mpb__vjvax, ',' if 
        wlfyp__npsk == 1 else '')
    wahk__eqaiv = {}
    exec(qetry__mbhb, {}, wahk__eqaiv)
    impl = wahk__eqaiv['f']
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def concat_bitmap_tup(arrs):
    wlfyp__npsk = len(arrs.types)
    lzp__lwg = '+'.join('len(arrs[{}]._data)'.format(i) for i in range(
        wlfyp__npsk))
    qetry__mbhb = 'def f(arrs):\n'
    qetry__mbhb += '  n = {}\n'.format(lzp__lwg)
    qetry__mbhb += '  n_bytes = (n + 7) >> 3\n'
    qetry__mbhb += '  new_mask = np.empty(n_bytes, np.uint8)\n'
    qetry__mbhb += '  curr_bit = 0\n'
    for i in range(wlfyp__npsk):
        qetry__mbhb += '  old_mask = arrs[{}]._null_bitmap\n'.format(i)
        qetry__mbhb += '  for j in range(len(arrs[{}])):\n'.format(i)
        qetry__mbhb += (
            '    bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        qetry__mbhb += (
            '    bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        qetry__mbhb += '    curr_bit += 1\n'
    qetry__mbhb += '  return new_mask\n'
    wahk__eqaiv = {}
    exec(qetry__mbhb, {'np': np, 'bodo': bodo}, wahk__eqaiv)
    impl = wahk__eqaiv['f']
    return impl


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    ldsld__exr = dict(skipna=skipna, min_count=min_count)
    qsts__fhqco = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', ldsld__exr, qsts__fhqco)

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
        jkq__ayuxt = []
        fqv__gtt = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not fqv__gtt:
                    data.append(dtype(1))
                    jkq__ayuxt.append(False)
                    fqv__gtt = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                jkq__ayuxt.append(True)
        tflfk__ajccs = np.array(data)
        n = len(tflfk__ajccs)
        cxl__sff = n + 7 >> 3
        mpx__gnyl = np.empty(cxl__sff, np.uint8)
        for kyx__rgw in range(n):
            set_bit_to_arr(mpx__gnyl, kyx__rgw, jkq__ayuxt[kyx__rgw])
        return init_integer_array(tflfk__ajccs, mpx__gnyl)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    kygtg__bkkj = numba.core.registry.cpu_target.typing_context
    gygis__uds = kygtg__bkkj.resolve_function_type(op, (types.Array(A.dtype,
        1, 'C'),), {}).return_type
    gygis__uds = to_nullable_type(gygis__uds)

    def impl(A):
        n = len(A)
        mypf__aows = bodo.utils.utils.alloc_type(n, gygis__uds, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(mypf__aows, i)
                continue
            mypf__aows[i] = op(A[i])
        return mypf__aows
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    inplace = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    xujga__djzq = isinstance(lhs, (types.Number, types.Boolean))
    ubs__paj = isinstance(rhs, (types.Number, types.Boolean))
    tgknw__amcku = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    qenl__rwwqq = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    kygtg__bkkj = numba.core.registry.cpu_target.typing_context
    gygis__uds = kygtg__bkkj.resolve_function_type(op, (tgknw__amcku,
        qenl__rwwqq), {}).return_type
    gygis__uds = to_nullable_type(gygis__uds)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    vlkyu__sufpg = 'lhs' if xujga__djzq else 'lhs[i]'
    djpqk__tld = 'rhs' if ubs__paj else 'rhs[i]'
    ebt__jxy = ('False' if xujga__djzq else
        'bodo.libs.array_kernels.isna(lhs, i)')
    lmc__ypln = 'False' if ubs__paj else 'bodo.libs.array_kernels.isna(rhs, i)'
    qetry__mbhb = 'def impl(lhs, rhs):\n'
    qetry__mbhb += '  n = len({})\n'.format('lhs' if not xujga__djzq else 'rhs'
        )
    if inplace:
        qetry__mbhb += '  out_arr = {}\n'.format('lhs' if not xujga__djzq else
            'rhs')
    else:
        qetry__mbhb += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    qetry__mbhb += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    qetry__mbhb += '    if ({}\n'.format(ebt__jxy)
    qetry__mbhb += '        or {}):\n'.format(lmc__ypln)
    qetry__mbhb += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    qetry__mbhb += '      continue\n'
    qetry__mbhb += (
        '    out_arr[i] = bodo.utils.conversion.unbox_if_timestamp(op({}, {}))\n'
        .format(vlkyu__sufpg, djpqk__tld))
    qetry__mbhb += '  return out_arr\n'
    wahk__eqaiv = {}
    exec(qetry__mbhb, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        gygis__uds, 'op': op}, wahk__eqaiv)
    impl = wahk__eqaiv['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        xujga__djzq = lhs in [pd_timedelta_type]
        ubs__paj = rhs in [pd_timedelta_type]
        if xujga__djzq:

            def impl(lhs, rhs):
                n = len(rhs)
                mypf__aows = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(mypf__aows, i)
                        continue
                    mypf__aows[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs, rhs[i]))
                return mypf__aows
            return impl
        elif ubs__paj:

            def impl(lhs, rhs):
                n = len(lhs)
                mypf__aows = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(mypf__aows, i)
                        continue
                    mypf__aows[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs[i], rhs))
                return mypf__aows
            return impl
    return impl
