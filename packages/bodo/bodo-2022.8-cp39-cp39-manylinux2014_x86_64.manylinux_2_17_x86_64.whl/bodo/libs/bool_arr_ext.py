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
        urmp__jgm = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, urmp__jgm)


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
    wmmyo__moeih = c.context.insert_const_string(c.builder.module, 'pandas')
    drg__ogd = c.pyapi.import_module_noblock(wmmyo__moeih)
    dcfam__qzz = c.pyapi.call_method(drg__ogd, 'BooleanDtype', ())
    c.pyapi.decref(drg__ogd)
    return dcfam__qzz


@unbox(BooleanDtype)
def unbox_boolean_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.BooleanDtype)(lambda a, b: boolean_dtype)
type_callable(pd.BooleanDtype)(lambda c: lambda : boolean_dtype)
lower_builtin(pd.BooleanDtype)(lambda c, b, s, a: c.get_dummy_value())


@numba.njit
def gen_full_bitmap(n):
    bsmp__cligu = n + 7 >> 3
    return np.full(bsmp__cligu, 255, np.uint8)


def call_func_in_unbox(func, args, arg_typs, c):
    qzkd__lowbw = c.context.typing_context.resolve_value_type(func)
    rzjdu__uum = qzkd__lowbw.get_call_type(c.context.typing_context,
        arg_typs, {})
    kzz__bvo = c.context.get_function(qzkd__lowbw, rzjdu__uum)
    sjeg__hrp = c.context.call_conv.get_function_type(rzjdu__uum.
        return_type, rzjdu__uum.args)
    oofzp__izeae = c.builder.module
    tsoq__tuxb = lir.Function(oofzp__izeae, sjeg__hrp, name=oofzp__izeae.
        get_unique_name('.func_conv'))
    tsoq__tuxb.linkage = 'internal'
    whaq__qoamb = lir.IRBuilder(tsoq__tuxb.append_basic_block())
    ujj__vpr = c.context.call_conv.decode_arguments(whaq__qoamb, rzjdu__uum
        .args, tsoq__tuxb)
    wqjs__xplbw = kzz__bvo(whaq__qoamb, ujj__vpr)
    c.context.call_conv.return_value(whaq__qoamb, wqjs__xplbw)
    qwhj__vsch, quwx__wcsa = c.context.call_conv.call_function(c.builder,
        tsoq__tuxb, rzjdu__uum.return_type, rzjdu__uum.args, args)
    return quwx__wcsa


@unbox(BooleanArrayType)
def unbox_bool_array(typ, obj, c):
    tlc__emrdo = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(tlc__emrdo)
    c.pyapi.decref(tlc__emrdo)
    sjeg__hrp = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    diixh__fczwy = cgutils.get_or_insert_function(c.builder.module,
        sjeg__hrp, name='is_bool_array')
    sjeg__hrp = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    tsoq__tuxb = cgutils.get_or_insert_function(c.builder.module, sjeg__hrp,
        name='is_pd_boolean_array')
    xgav__choxx = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    xvh__kgdp = c.builder.call(tsoq__tuxb, [obj])
    dnmdz__fqn = c.builder.icmp_unsigned('!=', xvh__kgdp, xvh__kgdp.type(0))
    with c.builder.if_else(dnmdz__fqn) as (elq__mqdgx, zjk__bwfk):
        with elq__mqdgx:
            znmjp__osc = c.pyapi.object_getattr_string(obj, '_data')
            xgav__choxx.data = c.pyapi.to_native_value(types.Array(types.
                bool_, 1, 'C'), znmjp__osc).value
            siag__tvv = c.pyapi.object_getattr_string(obj, '_mask')
            oupf__eilzj = c.pyapi.to_native_value(types.Array(types.bool_, 
                1, 'C'), siag__tvv).value
            bsmp__cligu = c.builder.udiv(c.builder.add(n, lir.Constant(lir.
                IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
            crrju__fnxuh = c.context.make_array(types.Array(types.bool_, 1,
                'C'))(c.context, c.builder, oupf__eilzj)
            far__ueihb = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(types.uint8, 1, 'C'), [bsmp__cligu])
            sjeg__hrp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            tsoq__tuxb = cgutils.get_or_insert_function(c.builder.module,
                sjeg__hrp, name='mask_arr_to_bitmap')
            c.builder.call(tsoq__tuxb, [far__ueihb.data, crrju__fnxuh.data, n])
            xgav__choxx.null_bitmap = far__ueihb._getvalue()
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), oupf__eilzj)
            c.pyapi.decref(znmjp__osc)
            c.pyapi.decref(siag__tvv)
        with zjk__bwfk:
            xiwfb__tlpy = c.builder.call(diixh__fczwy, [obj])
            jarmp__dkxs = c.builder.icmp_unsigned('!=', xiwfb__tlpy,
                xiwfb__tlpy.type(0))
            with c.builder.if_else(jarmp__dkxs) as (mivh__jld, zeyz__vyl):
                with mivh__jld:
                    xgav__choxx.data = c.pyapi.to_native_value(types.Array(
                        types.bool_, 1, 'C'), obj).value
                    xgav__choxx.null_bitmap = call_func_in_unbox(
                        gen_full_bitmap, (n,), (types.int64,), c)
                with zeyz__vyl:
                    xgav__choxx.data = bodo.utils.utils._empty_nd_impl(c.
                        context, c.builder, types.Array(types.bool_, 1, 'C'
                        ), [n])._getvalue()
                    bsmp__cligu = c.builder.udiv(c.builder.add(n, lir.
                        Constant(lir.IntType(64), 7)), lir.Constant(lir.
                        IntType(64), 8))
                    xgav__choxx.null_bitmap = bodo.utils.utils._empty_nd_impl(c
                        .context, c.builder, types.Array(types.uint8, 1,
                        'C'), [bsmp__cligu])._getvalue()
                    wmfee__vit = c.context.make_array(types.Array(types.
                        bool_, 1, 'C'))(c.context, c.builder, xgav__choxx.data
                        ).data
                    nksis__vrvx = c.context.make_array(types.Array(types.
                        uint8, 1, 'C'))(c.context, c.builder, xgav__choxx.
                        null_bitmap).data
                    sjeg__hrp = lir.FunctionType(lir.VoidType(), [lir.
                        IntType(8).as_pointer(), lir.IntType(8).as_pointer(
                        ), lir.IntType(8).as_pointer(), lir.IntType(64)])
                    tsoq__tuxb = cgutils.get_or_insert_function(c.builder.
                        module, sjeg__hrp, name='unbox_bool_array_obj')
                    c.builder.call(tsoq__tuxb, [obj, wmfee__vit,
                        nksis__vrvx, n])
    return NativeValue(xgav__choxx._getvalue())


@box(BooleanArrayType)
def box_bool_arr(typ, val, c):
    xgav__choxx = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        xgav__choxx.data, c.env_manager)
    qfz__sjv = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, xgav__choxx.null_bitmap).data
    tlc__emrdo = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(tlc__emrdo)
    wmmyo__moeih = c.context.insert_const_string(c.builder.module, 'numpy')
    eddg__xpxkq = c.pyapi.import_module_noblock(wmmyo__moeih)
    pwygi__jnppg = c.pyapi.object_getattr_string(eddg__xpxkq, 'bool_')
    oupf__eilzj = c.pyapi.call_method(eddg__xpxkq, 'empty', (tlc__emrdo,
        pwygi__jnppg))
    qukr__xizpq = c.pyapi.object_getattr_string(oupf__eilzj, 'ctypes')
    kseni__tsw = c.pyapi.object_getattr_string(qukr__xizpq, 'data')
    ykoh__acom = c.builder.inttoptr(c.pyapi.long_as_longlong(kseni__tsw),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as gkf__dwizm:
        nxv__noji = gkf__dwizm.index
        etue__jlve = c.builder.lshr(nxv__noji, lir.Constant(lir.IntType(64), 3)
            )
        rqewi__icout = c.builder.load(cgutils.gep(c.builder, qfz__sjv,
            etue__jlve))
        bqjxc__far = c.builder.trunc(c.builder.and_(nxv__noji, lir.Constant
            (lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(rqewi__icout, bqjxc__far), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        ugjqa__vtg = cgutils.gep(c.builder, ykoh__acom, nxv__noji)
        c.builder.store(val, ugjqa__vtg)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        xgav__choxx.null_bitmap)
    wmmyo__moeih = c.context.insert_const_string(c.builder.module, 'pandas')
    drg__ogd = c.pyapi.import_module_noblock(wmmyo__moeih)
    mkv__tekl = c.pyapi.object_getattr_string(drg__ogd, 'arrays')
    dcfam__qzz = c.pyapi.call_method(mkv__tekl, 'BooleanArray', (data,
        oupf__eilzj))
    c.pyapi.decref(drg__ogd)
    c.pyapi.decref(tlc__emrdo)
    c.pyapi.decref(eddg__xpxkq)
    c.pyapi.decref(pwygi__jnppg)
    c.pyapi.decref(qukr__xizpq)
    c.pyapi.decref(kseni__tsw)
    c.pyapi.decref(mkv__tekl)
    c.pyapi.decref(data)
    c.pyapi.decref(oupf__eilzj)
    return dcfam__qzz


@lower_constant(BooleanArrayType)
def lower_constant_bool_arr(context, builder, typ, pyval):
    n = len(pyval)
    clete__piw = np.empty(n, np.bool_)
    yyth__rttk = np.empty(n + 7 >> 3, np.uint8)
    for nxv__noji, s in enumerate(pyval):
        omn__ibcvt = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(yyth__rttk, nxv__noji, int(not
            omn__ibcvt))
        if not omn__ibcvt:
            clete__piw[nxv__noji] = s
    bvpm__exeyj = context.get_constant_generic(builder, data_type, clete__piw)
    qxki__zmi = context.get_constant_generic(builder, nulls_type, yyth__rttk)
    return lir.Constant.literal_struct([bvpm__exeyj, qxki__zmi])


def lower_init_bool_array(context, builder, signature, args):
    yzwr__imfsp, ltloc__owe = args
    xgav__choxx = cgutils.create_struct_proxy(signature.return_type)(context,
        builder)
    xgav__choxx.data = yzwr__imfsp
    xgav__choxx.null_bitmap = ltloc__owe
    context.nrt.incref(builder, signature.args[0], yzwr__imfsp)
    context.nrt.incref(builder, signature.args[1], ltloc__owe)
    return xgav__choxx._getvalue()


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
    ytu__mwac = args[0]
    if equiv_set.has_shape(ytu__mwac):
        return ArrayAnalysis.AnalyzeResult(shape=ytu__mwac, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_get_bool_arr_data = (
    get_bool_arr_data_equiv)


def init_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    ytu__mwac = args[0]
    if equiv_set.has_shape(ytu__mwac):
        return ArrayAnalysis.AnalyzeResult(shape=ytu__mwac, pre=[])
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
    clete__piw = np.empty(n, dtype=np.bool_)
    ygcko__rncd = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_bool_array(clete__piw, ygcko__rncd)


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
            fadk__jbqqi, quu__gect = array_getitem_bool_index(A, ind)
            return init_bool_array(fadk__jbqqi, quu__gect)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            fadk__jbqqi, quu__gect = array_getitem_int_index(A, ind)
            return init_bool_array(fadk__jbqqi, quu__gect)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            fadk__jbqqi, quu__gect = array_getitem_slice_index(A, ind)
            return init_bool_array(fadk__jbqqi, quu__gect)
        return impl_slice
    raise BodoError(
        f'getitem for BooleanArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def bool_arr_setitem(A, idx, val):
    if A != boolean_array:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    yngu__atts = (
        f"setitem for BooleanArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == types.bool_:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(yngu__atts)
    if not (is_iterable_type(val) and val.dtype == types.bool_ or types.
        unliteral(val) == types.bool_):
        raise BodoError(yngu__atts)
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
        for nxv__noji in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, nxv__noji):
                val = A[nxv__noji]
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
            lxcrx__pgqu = np.empty(n, nb_dtype)
            for nxv__noji in numba.parfors.parfor.internal_prange(n):
                lxcrx__pgqu[nxv__noji] = data[nxv__noji]
                if bodo.libs.array_kernels.isna(A, nxv__noji):
                    lxcrx__pgqu[nxv__noji] = np.nan
            return lxcrx__pgqu
        return impl_float
    return (lambda A, dtype, copy=True: bodo.libs.bool_arr_ext.
        get_bool_arr_data(A).astype(nb_dtype))


@overload_method(BooleanArrayType, 'fillna', no_unliteral=True)
def overload_bool_fillna(A, value=None, method=None, limit=None):

    def impl(A, value=None, method=None, limit=None):
        data = bodo.libs.bool_arr_ext.get_bool_arr_data(A)
        n = len(data)
        lxcrx__pgqu = np.empty(n, dtype=np.bool_)
        for nxv__noji in numba.parfors.parfor.internal_prange(n):
            lxcrx__pgqu[nxv__noji] = data[nxv__noji]
            if bodo.libs.array_kernels.isna(A, nxv__noji):
                lxcrx__pgqu[nxv__noji] = value
        return lxcrx__pgqu
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
    zsfv__fsb = op.__name__
    zsfv__fsb = ufunc_aliases.get(zsfv__fsb, zsfv__fsb)
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
    for orxh__fcqze in numba.np.ufunc_db.get_ufuncs():
        qmco__lvl = create_op_overload(orxh__fcqze, orxh__fcqze.nin)
        overload(orxh__fcqze, no_unliteral=True)(qmco__lvl)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod, operator.or_, operator.and_]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        qmco__lvl = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(qmco__lvl)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        qmco__lvl = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(qmco__lvl)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        qmco__lvl = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(qmco__lvl)


_install_unary_ops()


@overload_method(BooleanArrayType, 'unique', no_unliteral=True)
def overload_unique(A):

    def impl_bool_arr(A):
        data = []
        bqjxc__far = []
        nuyf__alzcu = False
        wxjz__nrhcx = False
        fouj__brubu = False
        for nxv__noji in range(len(A)):
            if bodo.libs.array_kernels.isna(A, nxv__noji):
                if not nuyf__alzcu:
                    data.append(False)
                    bqjxc__far.append(False)
                    nuyf__alzcu = True
                continue
            val = A[nxv__noji]
            if val and not wxjz__nrhcx:
                data.append(True)
                bqjxc__far.append(True)
                wxjz__nrhcx = True
            if not val and not fouj__brubu:
                data.append(False)
                bqjxc__far.append(True)
                fouj__brubu = True
            if nuyf__alzcu and wxjz__nrhcx and fouj__brubu:
                break
        fadk__jbqqi = np.array(data)
        n = len(fadk__jbqqi)
        bsmp__cligu = 1
        quu__gect = np.empty(bsmp__cligu, np.uint8)
        for lqh__nhr in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(quu__gect, lqh__nhr,
                bqjxc__far[lqh__nhr])
        return init_bool_array(fadk__jbqqi, quu__gect)
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
    dcfam__qzz = context.compile_internal(builder, func, toty(fromty), [val])
    return impl_ret_borrowed(context, builder, toty, dcfam__qzz)


@overload(operator.setitem, no_unliteral=True)
def overload_np_array_setitem_bool_arr(A, idx, val):
    if isinstance(A, types.Array) and idx == boolean_array:

        def impl(A, idx, val):
            A[idx._data] = val
        return impl


def create_nullable_logical_op_overload(op):
    tvu__hrqi = op == operator.or_

    def bool_array_impl(val1, val2):
        if not is_valid_boolean_array_logical_op(val1, val2):
            return
        njnn__vgr = bodo.utils.utils.is_array_typ(val1, False)
        hft__yotk = bodo.utils.utils.is_array_typ(val2, False)
        ylsgl__einog = 'val1' if njnn__vgr else 'val2'
        buj__ejtqi = 'def impl(val1, val2):\n'
        buj__ejtqi += f'  n = len({ylsgl__einog})\n'
        buj__ejtqi += (
            '  out_arr = bodo.utils.utils.alloc_type(n, bodo.boolean_array, (-1,))\n'
            )
        buj__ejtqi += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if njnn__vgr:
            null1 = 'bodo.libs.array_kernels.isna(val1, i)\n'
            vehpx__ikrc = 'val1[i]'
        else:
            null1 = 'False\n'
            vehpx__ikrc = 'val1'
        if hft__yotk:
            null2 = 'bodo.libs.array_kernels.isna(val2, i)\n'
            wprk__nfcc = 'val2[i]'
        else:
            null2 = 'False\n'
            wprk__nfcc = 'val2'
        if tvu__hrqi:
            buj__ejtqi += f"""    result, isna_val = compute_or_body({null1}, {null2}, {vehpx__ikrc}, {wprk__nfcc})
"""
        else:
            buj__ejtqi += f"""    result, isna_val = compute_and_body({null1}, {null2}, {vehpx__ikrc}, {wprk__nfcc})
"""
        buj__ejtqi += '    out_arr[i] = result\n'
        buj__ejtqi += '    if isna_val:\n'
        buj__ejtqi += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        buj__ejtqi += '      continue\n'
        buj__ejtqi += '  return out_arr\n'
        qfupt__ago = {}
        exec(buj__ejtqi, {'bodo': bodo, 'numba': numba, 'compute_and_body':
            compute_and_body, 'compute_or_body': compute_or_body}, qfupt__ago)
        impl = qfupt__ago['impl']
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
        tgkvz__vicif = boolean_array
        return tgkvz__vicif(*args)


def is_valid_boolean_array_logical_op(typ1, typ2):
    hfry__jjxp = (typ1 == bodo.boolean_array or typ2 == bodo.boolean_array
        ) and (bodo.utils.utils.is_array_typ(typ1, False) and typ1.dtype ==
        types.bool_ or typ1 == types.bool_) and (bodo.utils.utils.
        is_array_typ(typ2, False) and typ2.dtype == types.bool_ or typ2 ==
        types.bool_)
    return hfry__jjxp


def _install_nullable_logical_lowering():
    for op in (operator.and_, operator.or_):
        lpgpr__acl = create_boolean_array_logical_lower_impl(op)
        infer_global(op)(BooleanArrayLogicalOperatorTemplate)
        for typ1, typ2 in [(boolean_array, boolean_array), (boolean_array,
            types.bool_), (boolean_array, types.Array(types.bool_, 1, 'C'))]:
            lower_builtin(op, typ1, typ2)(lpgpr__acl)
            if typ1 != typ2:
                lower_builtin(op, typ2, typ1)(lpgpr__acl)


_install_nullable_logical_lowering()
