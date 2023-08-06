"""Nullable boolean array that stores data in Numpy format (1 byte per value)
but nulls are stored in bit arrays (1 bit per value) similar to Arrow's nulls.
Pandas converts boolean array to object when NAs are introduced.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import NativeValue, box, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs import hstr_ext
from bodo.libs.str_arr_ext import string_array_type
from bodo.utils.typing import is_list_like_index_type
ll.add_symbol('is_bool_array', hstr_ext.is_bool_array)
ll.add_symbol('is_pd_boolean_array', hstr_ext.is_pd_boolean_array)
ll.add_symbol('unbox_bool_array_obj', hstr_ext.unbox_bool_array_obj)
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, is_iterable_type, is_overload_false, is_overload_true, parse_dtype, raise_bodo_error


class BooleanArrayType(types.ArrayCompatible):

    def __init__(self):
        super(BooleanArrayType, self).__init__(name='BooleanArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.bool_

    def copy(self):
        return BooleanArrayType()


boolean_array = BooleanArrayType()


@typeof_impl.register(pd.arrays.BooleanArray)
def typeof_boolean_array(val, c):
    return boolean_array


data_type = types.Array(types.bool_, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(BooleanArrayType)
class BooleanArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        mjg__xlp = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, mjg__xlp)


make_attribute_wrapper(BooleanArrayType, 'data', '_data')
make_attribute_wrapper(BooleanArrayType, 'null_bitmap', '_null_bitmap')


class BooleanDtype(types.Number):

    def __init__(self):
        self.dtype = types.bool_
        super(BooleanDtype, self).__init__('BooleanDtype')


boolean_dtype = BooleanDtype()
register_model(BooleanDtype)(models.OpaqueModel)


@box(BooleanDtype)
def box_boolean_dtype(typ, val, c):
    rtogv__waqd = c.context.insert_const_string(c.builder.module, 'pandas')
    exed__nqt = c.pyapi.import_module_noblock(rtogv__waqd)
    mtfd__ict = c.pyapi.call_method(exed__nqt, 'BooleanDtype', ())
    c.pyapi.decref(exed__nqt)
    return mtfd__ict


@unbox(BooleanDtype)
def unbox_boolean_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.BooleanDtype)(lambda a, b: boolean_dtype)
type_callable(pd.BooleanDtype)(lambda c: lambda : boolean_dtype)
lower_builtin(pd.BooleanDtype)(lambda c, b, s, a: c.get_dummy_value())


@numba.njit
def gen_full_bitmap(n):
    askk__kcu = n + 7 >> 3
    return np.full(askk__kcu, 255, np.uint8)


def call_func_in_unbox(func, args, arg_typs, c):
    ltcam__smy = c.context.typing_context.resolve_value_type(func)
    qsyrb__zmirc = ltcam__smy.get_call_type(c.context.typing_context,
        arg_typs, {})
    nppe__lnz = c.context.get_function(ltcam__smy, qsyrb__zmirc)
    rbs__nxcic = c.context.call_conv.get_function_type(qsyrb__zmirc.
        return_type, qsyrb__zmirc.args)
    ruu__qfqaw = c.builder.module
    khel__pyudx = lir.Function(ruu__qfqaw, rbs__nxcic, name=ruu__qfqaw.
        get_unique_name('.func_conv'))
    khel__pyudx.linkage = 'internal'
    clwxa__eavz = lir.IRBuilder(khel__pyudx.append_basic_block())
    ltit__dvo = c.context.call_conv.decode_arguments(clwxa__eavz,
        qsyrb__zmirc.args, khel__pyudx)
    ygppv__hgtc = nppe__lnz(clwxa__eavz, ltit__dvo)
    c.context.call_conv.return_value(clwxa__eavz, ygppv__hgtc)
    xdkoj__cjqa, livyq__dlcw = c.context.call_conv.call_function(c.builder,
        khel__pyudx, qsyrb__zmirc.return_type, qsyrb__zmirc.args, args)
    return livyq__dlcw


@unbox(BooleanArrayType)
def unbox_bool_array(typ, obj, c):
    ylmm__mbpbi = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(ylmm__mbpbi)
    c.pyapi.decref(ylmm__mbpbi)
    rbs__nxcic = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    rlz__ihixb = cgutils.get_or_insert_function(c.builder.module,
        rbs__nxcic, name='is_bool_array')
    rbs__nxcic = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    khel__pyudx = cgutils.get_or_insert_function(c.builder.module,
        rbs__nxcic, name='is_pd_boolean_array')
    azf__pksy = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mrhmf__cmqma = c.builder.call(khel__pyudx, [obj])
    jmhn__dtq = c.builder.icmp_unsigned('!=', mrhmf__cmqma, mrhmf__cmqma.
        type(0))
    with c.builder.if_else(jmhn__dtq) as (ukm__jlxs, dnlqp__eoac):
        with ukm__jlxs:
            ejciu__uuv = c.pyapi.object_getattr_string(obj, '_data')
            azf__pksy.data = c.pyapi.to_native_value(types.Array(types.
                bool_, 1, 'C'), ejciu__uuv).value
            oskwx__wfzhx = c.pyapi.object_getattr_string(obj, '_mask')
            nkklg__utdu = c.pyapi.to_native_value(types.Array(types.bool_, 
                1, 'C'), oskwx__wfzhx).value
            askk__kcu = c.builder.udiv(c.builder.add(n, lir.Constant(lir.
                IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
            dfizt__vwsq = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, nkklg__utdu)
            zohi__nvge = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(types.uint8, 1, 'C'), [askk__kcu])
            rbs__nxcic = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            khel__pyudx = cgutils.get_or_insert_function(c.builder.module,
                rbs__nxcic, name='mask_arr_to_bitmap')
            c.builder.call(khel__pyudx, [zohi__nvge.data, dfizt__vwsq.data, n])
            azf__pksy.null_bitmap = zohi__nvge._getvalue()
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), nkklg__utdu)
            c.pyapi.decref(ejciu__uuv)
            c.pyapi.decref(oskwx__wfzhx)
        with dnlqp__eoac:
            ewd__imu = c.builder.call(rlz__ihixb, [obj])
            bvguy__svhn = c.builder.icmp_unsigned('!=', ewd__imu, ewd__imu.
                type(0))
            with c.builder.if_else(bvguy__svhn) as (gdd__sogp, guce__laj):
                with gdd__sogp:
                    azf__pksy.data = c.pyapi.to_native_value(types.Array(
                        types.bool_, 1, 'C'), obj).value
                    azf__pksy.null_bitmap = call_func_in_unbox(gen_full_bitmap,
                        (n,), (types.int64,), c)
                with guce__laj:
                    azf__pksy.data = bodo.utils.utils._empty_nd_impl(c.
                        context, c.builder, types.Array(types.bool_, 1, 'C'
                        ), [n])._getvalue()
                    askk__kcu = c.builder.udiv(c.builder.add(n, lir.
                        Constant(lir.IntType(64), 7)), lir.Constant(lir.
                        IntType(64), 8))
                    azf__pksy.null_bitmap = bodo.utils.utils._empty_nd_impl(c
                        .context, c.builder, types.Array(types.uint8, 1,
                        'C'), [askk__kcu])._getvalue()
                    uhr__veatm = c.context.make_array(types.Array(types.
                        bool_, 1, 'C'))(c.context, c.builder, azf__pksy.data
                        ).data
                    taapb__bjf = c.context.make_array(types.Array(types.
                        uint8, 1, 'C'))(c.context, c.builder, azf__pksy.
                        null_bitmap).data
                    rbs__nxcic = lir.FunctionType(lir.VoidType(), [lir.
                        IntType(8).as_pointer(), lir.IntType(8).as_pointer(
                        ), lir.IntType(8).as_pointer(), lir.IntType(64)])
                    khel__pyudx = cgutils.get_or_insert_function(c.builder.
                        module, rbs__nxcic, name='unbox_bool_array_obj')
                    c.builder.call(khel__pyudx, [obj, uhr__veatm,
                        taapb__bjf, n])
    return NativeValue(azf__pksy._getvalue())


@box(BooleanArrayType)
def box_bool_arr(typ, val, c):
    azf__pksy = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        azf__pksy.data, c.env_manager)
    aez__zneh = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, azf__pksy.null_bitmap).data
    ylmm__mbpbi = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(ylmm__mbpbi)
    rtogv__waqd = c.context.insert_const_string(c.builder.module, 'numpy')
    yhvi__mculf = c.pyapi.import_module_noblock(rtogv__waqd)
    jlt__ghsmh = c.pyapi.object_getattr_string(yhvi__mculf, 'bool_')
    nkklg__utdu = c.pyapi.call_method(yhvi__mculf, 'empty', (ylmm__mbpbi,
        jlt__ghsmh))
    noqc__cbls = c.pyapi.object_getattr_string(nkklg__utdu, 'ctypes')
    hppm__czwi = c.pyapi.object_getattr_string(noqc__cbls, 'data')
    trn__wuux = c.builder.inttoptr(c.pyapi.long_as_longlong(hppm__czwi),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as ksdh__zpmt:
        ipty__kwd = ksdh__zpmt.index
        ajrd__flsp = c.builder.lshr(ipty__kwd, lir.Constant(lir.IntType(64), 3)
            )
        aga__hctjq = c.builder.load(cgutils.gep(c.builder, aez__zneh,
            ajrd__flsp))
        htob__pkvd = c.builder.trunc(c.builder.and_(ipty__kwd, lir.Constant
            (lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(aga__hctjq, htob__pkvd), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        cqops__nmlx = cgutils.gep(c.builder, trn__wuux, ipty__kwd)
        c.builder.store(val, cqops__nmlx)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        azf__pksy.null_bitmap)
    rtogv__waqd = c.context.insert_const_string(c.builder.module, 'pandas')
    exed__nqt = c.pyapi.import_module_noblock(rtogv__waqd)
    ldry__gpoky = c.pyapi.object_getattr_string(exed__nqt, 'arrays')
    mtfd__ict = c.pyapi.call_method(ldry__gpoky, 'BooleanArray', (data,
        nkklg__utdu))
    c.pyapi.decref(exed__nqt)
    c.pyapi.decref(ylmm__mbpbi)
    c.pyapi.decref(yhvi__mculf)
    c.pyapi.decref(jlt__ghsmh)
    c.pyapi.decref(noqc__cbls)
    c.pyapi.decref(hppm__czwi)
    c.pyapi.decref(ldry__gpoky)
    c.pyapi.decref(data)
    c.pyapi.decref(nkklg__utdu)
    return mtfd__ict


@lower_constant(BooleanArrayType)
def lower_constant_bool_arr(context, builder, typ, pyval):
    n = len(pyval)
    wtzc__kgnaa = np.empty(n, np.bool_)
    yfcjw__fcsik = np.empty(n + 7 >> 3, np.uint8)
    for ipty__kwd, s in enumerate(pyval):
        wuatr__jwmt = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(yfcjw__fcsik, ipty__kwd, int(
            not wuatr__jwmt))
        if not wuatr__jwmt:
            wtzc__kgnaa[ipty__kwd] = s
    hqwbn__qycz = context.get_constant_generic(builder, data_type, wtzc__kgnaa)
    lpve__pep = context.get_constant_generic(builder, nulls_type, yfcjw__fcsik)
    return lir.Constant.literal_struct([hqwbn__qycz, lpve__pep])


def lower_init_bool_array(context, builder, signature, args):
    dbflc__pld, obv__yuyb = args
    azf__pksy = cgutils.create_struct_proxy(signature.return_type)(context,
        builder)
    azf__pksy.data = dbflc__pld
    azf__pksy.null_bitmap = obv__yuyb
    context.nrt.incref(builder, signature.args[0], dbflc__pld)
    context.nrt.incref(builder, signature.args[1], obv__yuyb)
    return azf__pksy._getvalue()


@intrinsic
def init_bool_array(typingctx, data, null_bitmap=None):
    assert data == types.Array(types.bool_, 1, 'C')
    assert null_bitmap == types.Array(types.uint8, 1, 'C')
    sig = boolean_array(data, null_bitmap)
    return sig, lower_init_bool_array


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_bool_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_bool_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_bool_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    vbvtx__iibsx = args[0]
    if equiv_set.has_shape(vbvtx__iibsx):
        return ArrayAnalysis.AnalyzeResult(shape=vbvtx__iibsx, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_get_bool_arr_data = (
    get_bool_arr_data_equiv)


def init_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    vbvtx__iibsx = args[0]
    if equiv_set.has_shape(vbvtx__iibsx):
        return ArrayAnalysis.AnalyzeResult(shape=vbvtx__iibsx, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_init_bool_array = (
    init_bool_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_bool_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_bool_array',
    'bodo.libs.bool_arr_ext'] = alias_ext_init_bool_array
numba.core.ir_utils.alias_func_extensions['get_bool_arr_data',
    'bodo.libs.bool_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_bool_arr_bitmap',
    'bodo.libs.bool_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_bool_array(n):
    wtzc__kgnaa = np.empty(n, dtype=np.bool_)
    okag__fmqj = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_bool_array(wtzc__kgnaa, okag__fmqj)


def alloc_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_alloc_bool_array = (
    alloc_bool_array_equiv)


@overload(operator.getitem, no_unliteral=True)
def bool_arr_getitem(A, ind):
    if A != boolean_array:
        return
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda A, ind: A._data[ind]
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            wfioo__cfyhg, ufh__amwop = array_getitem_bool_index(A, ind)
            return init_bool_array(wfioo__cfyhg, ufh__amwop)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            wfioo__cfyhg, ufh__amwop = array_getitem_int_index(A, ind)
            return init_bool_array(wfioo__cfyhg, ufh__amwop)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            wfioo__cfyhg, ufh__amwop = array_getitem_slice_index(A, ind)
            return init_bool_array(wfioo__cfyhg, ufh__amwop)
        return impl_slice
    raise BodoError(
        f'getitem for BooleanArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def bool_arr_setitem(A, idx, val):
    if A != boolean_array:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    lwik__ngq = (
        f"setitem for BooleanArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == types.bool_:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(lwik__ngq)
    if not (is_iterable_type(val) and val.dtype == types.bool_ or types.
        unliteral(val) == types.bool_):
        raise BodoError(lwik__ngq)
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
        f'setitem for BooleanArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_bool_arr_len(A):
    if A == boolean_array:
        return lambda A: len(A._data)


@overload_attribute(BooleanArrayType, 'size')
def overload_bool_arr_size(A):
    return lambda A: len(A._data)


@overload_attribute(BooleanArrayType, 'shape')
def overload_bool_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(BooleanArrayType, 'dtype')
def overload_bool_arr_dtype(A):
    return lambda A: pd.BooleanDtype()


@overload_attribute(BooleanArrayType, 'ndim')
def overload_bool_arr_ndim(A):
    return lambda A: 1


@overload_attribute(BooleanArrayType, 'nbytes')
def bool_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(BooleanArrayType, 'copy', no_unliteral=True)
def overload_bool_arr_copy(A):
    return lambda A: bodo.libs.bool_arr_ext.init_bool_array(bodo.libs.
        bool_arr_ext.get_bool_arr_data(A).copy(), bodo.libs.bool_arr_ext.
        get_bool_arr_bitmap(A).copy())


@overload_method(BooleanArrayType, 'sum', no_unliteral=True, inline='always')
def overload_bool_sum(A):

    def impl(A):
        numba.parfors.parfor.init_prange()
        s = 0
        for ipty__kwd in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, ipty__kwd):
                val = A[ipty__kwd]
            s += val
        return s
    return impl


@overload_method(BooleanArrayType, 'astype', no_unliteral=True)
def overload_bool_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "BooleanArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if dtype == types.bool_:
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
    nb_dtype = parse_dtype(dtype, 'BooleanArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.bool_arr_ext.get_bool_arr_data(A)
            n = len(data)
            ufa__evo = np.empty(n, nb_dtype)
            for ipty__kwd in numba.parfors.parfor.internal_prange(n):
                ufa__evo[ipty__kwd] = data[ipty__kwd]
                if bodo.libs.array_kernels.isna(A, ipty__kwd):
                    ufa__evo[ipty__kwd] = np.nan
            return ufa__evo
        return impl_float
    return (lambda A, dtype, copy=True: bodo.libs.bool_arr_ext.
        get_bool_arr_data(A).astype(nb_dtype))


@overload_method(BooleanArrayType, 'fillna', no_unliteral=True)
def overload_bool_fillna(A, value=None, method=None, limit=None):

    def impl(A, value=None, method=None, limit=None):
        data = bodo.libs.bool_arr_ext.get_bool_arr_data(A)
        n = len(data)
        ufa__evo = np.empty(n, dtype=np.bool_)
        for ipty__kwd in numba.parfors.parfor.internal_prange(n):
            ufa__evo[ipty__kwd] = data[ipty__kwd]
            if bodo.libs.array_kernels.isna(A, ipty__kwd):
                ufa__evo[ipty__kwd] = value
        return ufa__evo
    return impl


@overload(str, no_unliteral=True)
def overload_str_bool(val):
    if val == types.bool_:

        def impl(val):
            if val:
                return 'True'
            return 'False'
        return impl


ufunc_aliases = {'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    fstq__gxa = op.__name__
    fstq__gxa = ufunc_aliases.get(fstq__gxa, fstq__gxa)
    if n_inputs == 1:

        def overload_bool_arr_op_nin_1(A):
            if isinstance(A, BooleanArrayType):
                return bodo.libs.int_arr_ext.get_nullable_array_unary_impl(op,
                    A)
        return overload_bool_arr_op_nin_1
    elif n_inputs == 2:

        def overload_bool_arr_op_nin_2(lhs, rhs):
            if lhs == boolean_array or rhs == boolean_array:
                return bodo.libs.int_arr_ext.get_nullable_array_binary_impl(op,
                    lhs, rhs)
        return overload_bool_arr_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ardnm__erjhg in numba.np.ufunc_db.get_ufuncs():
        olqg__ylam = create_op_overload(ardnm__erjhg, ardnm__erjhg.nin)
        overload(ardnm__erjhg, no_unliteral=True)(olqg__ylam)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod, operator.or_, operator.and_]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        olqg__ylam = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(olqg__ylam)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        olqg__ylam = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(olqg__ylam)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        olqg__ylam = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(olqg__ylam)


_install_unary_ops()


@overload_method(BooleanArrayType, 'unique', no_unliteral=True)
def overload_unique(A):

    def impl_bool_arr(A):
        data = []
        htob__pkvd = []
        wyj__guuo = False
        ahjtk__vtnmn = False
        ljmt__mxip = False
        for ipty__kwd in range(len(A)):
            if bodo.libs.array_kernels.isna(A, ipty__kwd):
                if not wyj__guuo:
                    data.append(False)
                    htob__pkvd.append(False)
                    wyj__guuo = True
                continue
            val = A[ipty__kwd]
            if val and not ahjtk__vtnmn:
                data.append(True)
                htob__pkvd.append(True)
                ahjtk__vtnmn = True
            if not val and not ljmt__mxip:
                data.append(False)
                htob__pkvd.append(True)
                ljmt__mxip = True
            if wyj__guuo and ahjtk__vtnmn and ljmt__mxip:
                break
        wfioo__cfyhg = np.array(data)
        n = len(wfioo__cfyhg)
        askk__kcu = 1
        ufh__amwop = np.empty(askk__kcu, np.uint8)
        for qrlol__aaca in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(ufh__amwop, qrlol__aaca,
                htob__pkvd[qrlol__aaca])
        return init_bool_array(wfioo__cfyhg, ufh__amwop)
    return impl_bool_arr


@overload(operator.getitem, no_unliteral=True)
def bool_arr_ind_getitem(A, ind):
    if ind == boolean_array and (isinstance(A, (types.Array, bodo.libs.
        int_arr_ext.IntegerArrayType)) or isinstance(A, bodo.libs.
        struct_arr_ext.StructArrayType) or isinstance(A, bodo.libs.
        array_item_arr_ext.ArrayItemArrayType) or isinstance(A, bodo.libs.
        map_arr_ext.MapArrayType) or A in (string_array_type, bodo.hiframes
        .split_impl.string_array_split_view_type, boolean_array)):
        return lambda A, ind: A[ind._data]


@lower_cast(types.Array(types.bool_, 1, 'C'), boolean_array)
def cast_np_bool_arr_to_bool_arr(context, builder, fromty, toty, val):
    func = lambda A: bodo.libs.bool_arr_ext.init_bool_array(A, np.full(len(
        A) + 7 >> 3, 255, np.uint8))
    mtfd__ict = context.compile_internal(builder, func, toty(fromty), [val])
    return impl_ret_borrowed(context, builder, toty, mtfd__ict)


@overload(operator.setitem, no_unliteral=True)
def overload_np_array_setitem_bool_arr(A, idx, val):
    if isinstance(A, types.Array) and idx == boolean_array:

        def impl(A, idx, val):
            A[idx._data] = val
        return impl


def create_nullable_logical_op_overload(op):
    npq__trxs = op == operator.or_

    def bool_array_impl(val1, val2):
        if not is_valid_boolean_array_logical_op(val1, val2):
            return
        town__zpj = bodo.utils.utils.is_array_typ(val1, False)
        kaj__egs = bodo.utils.utils.is_array_typ(val2, False)
        sql__bdvf = 'val1' if town__zpj else 'val2'
        gmynw__wwgp = 'def impl(val1, val2):\n'
        gmynw__wwgp += f'  n = len({sql__bdvf})\n'
        gmynw__wwgp += (
            '  out_arr = bodo.utils.utils.alloc_type(n, bodo.boolean_array, (-1,))\n'
            )
        gmynw__wwgp += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if town__zpj:
            null1 = 'bodo.libs.array_kernels.isna(val1, i)\n'
            wad__xdg = 'val1[i]'
        else:
            null1 = 'False\n'
            wad__xdg = 'val1'
        if kaj__egs:
            null2 = 'bodo.libs.array_kernels.isna(val2, i)\n'
            vqbp__exrc = 'val2[i]'
        else:
            null2 = 'False\n'
            vqbp__exrc = 'val2'
        if npq__trxs:
            gmynw__wwgp += f"""    result, isna_val = compute_or_body({null1}, {null2}, {wad__xdg}, {vqbp__exrc})
"""
        else:
            gmynw__wwgp += f"""    result, isna_val = compute_and_body({null1}, {null2}, {wad__xdg}, {vqbp__exrc})
"""
        gmynw__wwgp += '    out_arr[i] = result\n'
        gmynw__wwgp += '    if isna_val:\n'
        gmynw__wwgp += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        gmynw__wwgp += '      continue\n'
        gmynw__wwgp += '  return out_arr\n'
        fmkh__rpwx = {}
        exec(gmynw__wwgp, {'bodo': bodo, 'numba': numba, 'compute_and_body':
            compute_and_body, 'compute_or_body': compute_or_body}, fmkh__rpwx)
        impl = fmkh__rpwx['impl']
        return impl
    return bool_array_impl


def compute_or_body(null1, null2, val1, val2):
    pass


@overload(compute_or_body)
def overload_compute_or_body(null1, null2, val1, val2):

    def impl(null1, null2, val1, val2):
        if null1 and null2:
            return False, True
        elif null1:
            return val2, val2 == False
        elif null2:
            return val1, val1 == False
        else:
            return val1 | val2, False
    return impl


def compute_and_body(null1, null2, val1, val2):
    pass


@overload(compute_and_body)
def overload_compute_and_body(null1, null2, val1, val2):

    def impl(null1, null2, val1, val2):
        if null1 and null2:
            return False, True
        elif null1:
            return val2, val2 == True
        elif null2:
            return val1, val1 == True
        else:
            return val1 & val2, False
    return impl


def create_boolean_array_logical_lower_impl(op):

    def logical_lower_impl(context, builder, sig, args):
        impl = create_nullable_logical_op_overload(op)(*sig.args)
        return context.compile_internal(builder, impl, sig, args)
    return logical_lower_impl


class BooleanArrayLogicalOperatorTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        if not is_valid_boolean_array_logical_op(args[0], args[1]):
            return
        qmwa__ncsk = boolean_array
        return qmwa__ncsk(*args)


def is_valid_boolean_array_logical_op(typ1, typ2):
    hkxk__bztj = (typ1 == bodo.boolean_array or typ2 == bodo.boolean_array
        ) and (bodo.utils.utils.is_array_typ(typ1, False) and typ1.dtype ==
        types.bool_ or typ1 == types.bool_) and (bodo.utils.utils.
        is_array_typ(typ2, False) and typ2.dtype == types.bool_ or typ2 ==
        types.bool_)
    return hkxk__bztj


def _install_nullable_logical_lowering():
    for op in (operator.and_, operator.or_):
        atzs__elkw = create_boolean_array_logical_lower_impl(op)
        infer_global(op)(BooleanArrayLogicalOperatorTemplate)
        for typ1, typ2 in [(boolean_array, boolean_array), (boolean_array,
            types.bool_), (boolean_array, types.Array(types.bool_, 1, 'C'))]:
            lower_builtin(op, typ1, typ2)(atzs__elkw)
            if typ1 != typ2:
                lower_builtin(op, typ2, typ1)(atzs__elkw)


_install_nullable_logical_lowering()
