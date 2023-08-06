"""Array implementation for variable-size array items.
Corresponds to Spark's ArrayType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Variable-size List: https://arrow.apache.org/docs/format/Columnar.html

The values are stored in a contingous data array, while an offsets array marks the
individual arrays. For example:
value:             [[1, 2], [3], None, [5, 4, 6], []]
data:              [1, 2, 3, 5, 4, 6]
offsets:           [0, 2, 3, 3, 6, 6]
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import NativeValue, box, intrinsic, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs import array_ext
from bodo.utils.cg_helpers import gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit, to_arr_obj_if_list_obj
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, is_iterable_type, is_list_like_index_type
ll.add_symbol('count_total_elems_list_array', array_ext.
    count_total_elems_list_array)
ll.add_symbol('array_item_array_from_sequence', array_ext.
    array_item_array_from_sequence)
ll.add_symbol('np_array_from_array_item_array', array_ext.
    np_array_from_array_item_array)
offset_type = types.uint64
np_offset_type = numba.np.numpy_support.as_dtype(offset_type)


class ArrayItemArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        assert bodo.utils.utils.is_array_typ(dtype, False)
        self.dtype = dtype
        super(ArrayItemArrayType, self).__init__(name=
            'ArrayItemArrayType({})'.format(dtype))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return ArrayItemArrayType(self.dtype)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class ArrayItemArrayPayloadType(types.Type):

    def __init__(self, array_type):
        self.array_type = array_type
        super(ArrayItemArrayPayloadType, self).__init__(name=
            'ArrayItemArrayPayloadType({})'.format(array_type))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(ArrayItemArrayPayloadType)
class ArrayItemArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        llpm__ujy = [('n_arrays', types.int64), ('data', fe_type.array_type
            .dtype), ('offsets', types.Array(offset_type, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, llpm__ujy)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        llpm__ujy = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, llpm__ujy)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    usdzk__cmxbh = builder.module
    bml__ejqku = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    xau__gmeqq = cgutils.get_or_insert_function(usdzk__cmxbh, bml__ejqku,
        name='.dtor.array_item.{}'.format(array_item_type.dtype))
    if not xau__gmeqq.is_declaration:
        return xau__gmeqq
    xau__gmeqq.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(xau__gmeqq.append_basic_block())
    qhf__jie = xau__gmeqq.args[0]
    bjkq__hkr = context.get_value_type(payload_type).as_pointer()
    mwe__hsxk = builder.bitcast(qhf__jie, bjkq__hkr)
    gkhg__zav = context.make_helper(builder, payload_type, ref=mwe__hsxk)
    context.nrt.decref(builder, array_item_type.dtype, gkhg__zav.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'), gkhg__zav
        .offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'), gkhg__zav
        .null_bitmap)
    builder.ret_void()
    return xau__gmeqq


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    jxr__lcbdu = context.get_value_type(payload_type)
    vjao__vaq = context.get_abi_sizeof(jxr__lcbdu)
    doqlp__fplr = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    qkvdb__rdcol = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, vjao__vaq), doqlp__fplr)
    izq__ijmcg = context.nrt.meminfo_data(builder, qkvdb__rdcol)
    txft__ydjor = builder.bitcast(izq__ijmcg, jxr__lcbdu.as_pointer())
    gkhg__zav = cgutils.create_struct_proxy(payload_type)(context, builder)
    gkhg__zav.n_arrays = n_arrays
    hafb__tfii = n_elems.type.count
    pbe__most = builder.extract_value(n_elems, 0)
    tjsji__tprh = cgutils.alloca_once_value(builder, pbe__most)
    mggox__uab = builder.icmp_signed('==', pbe__most, lir.Constant(
        pbe__most.type, -1))
    with builder.if_then(mggox__uab):
        builder.store(n_arrays, tjsji__tprh)
    n_elems = cgutils.pack_array(builder, [builder.load(tjsji__tprh)] + [
        builder.extract_value(n_elems, ynwk__mghia) for ynwk__mghia in
        range(1, hafb__tfii)])
    gkhg__zav.data = gen_allocate_array(context, builder, array_item_type.
        dtype, n_elems, c)
    qjhm__khyo = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    ahb__rpa = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [qjhm__khyo])
    offsets_ptr = ahb__rpa.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    gkhg__zav.offsets = ahb__rpa._getvalue()
    ckwsp__fvod = builder.udiv(builder.add(n_arrays, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    ytbw__vdf = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [ckwsp__fvod])
    null_bitmap_ptr = ytbw__vdf.data
    gkhg__zav.null_bitmap = ytbw__vdf._getvalue()
    builder.store(gkhg__zav._getvalue(), txft__ydjor)
    return qkvdb__rdcol, gkhg__zav.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    vzqw__quwxr, odp__iccwm = c.pyapi.call_jit_code(copy_data, sig, [
        data_arr, item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    lns__zsdyb = context.insert_const_string(builder.module, 'pandas')
    bgxj__ugyp = c.pyapi.import_module_noblock(lns__zsdyb)
    kgybv__iylre = c.pyapi.object_getattr_string(bgxj__ugyp, 'NA')
    rtzb__sjvy = c.context.get_constant(offset_type, 0)
    builder.store(rtzb__sjvy, offsets_ptr)
    fkroe__sgmmj = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as icur__prwes:
        hlg__wxnei = icur__prwes.index
        item_ind = builder.load(fkroe__sgmmj)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [hlg__wxnei]))
        arr_obj = seq_getitem(builder, context, val, hlg__wxnei)
        set_bitmap_bit(builder, null_bitmap_ptr, hlg__wxnei, 0)
        chkbi__gys = is_na_value(builder, context, arr_obj, kgybv__iylre)
        wkm__uhx = builder.icmp_unsigned('!=', chkbi__gys, lir.Constant(
            chkbi__gys.type, 1))
        with builder.if_then(wkm__uhx):
            set_bitmap_bit(builder, null_bitmap_ptr, hlg__wxnei, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), fkroe__sgmmj)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(fkroe__sgmmj), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(bgxj__ugyp)
    c.pyapi.decref(kgybv__iylre)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    xaai__ppxhn = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if xaai__ppxhn:
        bml__ejqku = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        bqve__pwnlu = cgutils.get_or_insert_function(c.builder.module,
            bml__ejqku, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(bqve__pwnlu,
            [val])])
    else:
        xvcvt__dys = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            xvcvt__dys, ynwk__mghia) for ynwk__mghia in range(1, xvcvt__dys
            .type.count)])
    qkvdb__rdcol, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if xaai__ppxhn:
        gfuwv__tja = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        fino__tvd = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        bml__ejqku = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        xau__gmeqq = cgutils.get_or_insert_function(c.builder.module,
            bml__ejqku, name='array_item_array_from_sequence')
        c.builder.call(xau__gmeqq, [val, c.builder.bitcast(fino__tvd, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), gfuwv__tja)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    dyedk__bhd = c.context.make_helper(c.builder, typ)
    dyedk__bhd.meminfo = qkvdb__rdcol
    teqty__dtwt = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(dyedk__bhd._getvalue(), is_error=teqty__dtwt)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    dyedk__bhd = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    izq__ijmcg = context.nrt.meminfo_data(builder, dyedk__bhd.meminfo)
    txft__ydjor = builder.bitcast(izq__ijmcg, context.get_value_type(
        payload_type).as_pointer())
    gkhg__zav = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(txft__ydjor))
    return gkhg__zav


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    lns__zsdyb = context.insert_const_string(builder.module, 'numpy')
    dqpz__hyy = c.pyapi.import_module_noblock(lns__zsdyb)
    oycp__izk = c.pyapi.object_getattr_string(dqpz__hyy, 'object_')
    lct__mhebz = c.pyapi.long_from_longlong(n_arrays)
    ngdt__ltv = c.pyapi.call_method(dqpz__hyy, 'ndarray', (lct__mhebz,
        oycp__izk))
    trl__hyu = c.pyapi.object_getattr_string(dqpz__hyy, 'nan')
    fkroe__sgmmj = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_arrays) as icur__prwes:
        hlg__wxnei = icur__prwes.index
        pyarray_setitem(builder, context, ngdt__ltv, hlg__wxnei, trl__hyu)
        bglu__gtkn = get_bitmap_bit(builder, null_bitmap_ptr, hlg__wxnei)
        ooq__lfgeo = builder.icmp_unsigned('!=', bglu__gtkn, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(ooq__lfgeo):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(hlg__wxnei, lir.Constant(
                hlg__wxnei.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [hlg__wxnei]))), lir.IntType(64))
            item_ind = builder.load(fkroe__sgmmj)
            vzqw__quwxr, jhzn__swezk = c.pyapi.call_jit_code(lambda
                data_arr, item_ind, n_items: data_arr[item_ind:item_ind +
                n_items], typ.dtype(typ.dtype, types.int64, types.int64), [
                data_arr, item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), fkroe__sgmmj)
            arr_obj = c.pyapi.from_native_value(typ.dtype, jhzn__swezk, c.
                env_manager)
            pyarray_setitem(builder, context, ngdt__ltv, hlg__wxnei, arr_obj)
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(dqpz__hyy)
    c.pyapi.decref(oycp__izk)
    c.pyapi.decref(lct__mhebz)
    c.pyapi.decref(trl__hyu)
    return ngdt__ltv


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    gkhg__zav = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = gkhg__zav.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), gkhg__zav.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), gkhg__zav.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        gfuwv__tja = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        fino__tvd = c.context.make_helper(c.builder, typ.dtype, data_arr).data
        bml__ejqku = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        acd__kzpv = cgutils.get_or_insert_function(c.builder.module,
            bml__ejqku, name='np_array_from_array_item_array')
        arr = c.builder.call(acd__kzpv, [gkhg__zav.n_arrays, c.builder.
            bitcast(fino__tvd, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), gfuwv__tja)])
    else:
        arr = _box_array_item_array_generic(typ, c, gkhg__zav.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    tdn__pbs, zcmfp__xse, xnkx__lguj = args
    xuwh__qkq = bodo.utils.transform.get_type_alloc_counts(array_item_type.
        dtype)
    fbob__nqhe = sig.args[1]
    if not isinstance(fbob__nqhe, types.UniTuple):
        zcmfp__xse = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), -1) for xnkx__lguj in range(xuwh__qkq)])
    elif fbob__nqhe.count < xuwh__qkq:
        zcmfp__xse = cgutils.pack_array(builder, [builder.extract_value(
            zcmfp__xse, ynwk__mghia) for ynwk__mghia in range(fbob__nqhe.
            count)] + [lir.Constant(lir.IntType(64), -1) for xnkx__lguj in
            range(xuwh__qkq - fbob__nqhe.count)])
    qkvdb__rdcol, xnkx__lguj, xnkx__lguj, xnkx__lguj = (
        construct_array_item_array(context, builder, array_item_type,
        tdn__pbs, zcmfp__xse))
    dyedk__bhd = context.make_helper(builder, array_item_type)
    dyedk__bhd.meminfo = qkvdb__rdcol
    return dyedk__bhd._getvalue()


@intrinsic
def pre_alloc_array_item_array(typingctx, num_arrs_typ, num_values_typ,
    dtype_typ=None):
    assert isinstance(num_arrs_typ, types.Integer)
    array_item_type = ArrayItemArrayType(dtype_typ.instance_type)
    num_values_typ = types.unliteral(num_values_typ)
    return array_item_type(types.int64, num_values_typ, dtype_typ
        ), lower_pre_alloc_array_item_array


def pre_alloc_array_item_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_libs_array_item_arr_ext_pre_alloc_array_item_array
    ) = pre_alloc_array_item_array_equiv


def init_array_item_array_codegen(context, builder, signature, args):
    n_arrays, pqsgn__sbjqo, ahb__rpa, ytbw__vdf = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    jxr__lcbdu = context.get_value_type(payload_type)
    vjao__vaq = context.get_abi_sizeof(jxr__lcbdu)
    doqlp__fplr = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    qkvdb__rdcol = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, vjao__vaq), doqlp__fplr)
    izq__ijmcg = context.nrt.meminfo_data(builder, qkvdb__rdcol)
    txft__ydjor = builder.bitcast(izq__ijmcg, jxr__lcbdu.as_pointer())
    gkhg__zav = cgutils.create_struct_proxy(payload_type)(context, builder)
    gkhg__zav.n_arrays = n_arrays
    gkhg__zav.data = pqsgn__sbjqo
    gkhg__zav.offsets = ahb__rpa
    gkhg__zav.null_bitmap = ytbw__vdf
    builder.store(gkhg__zav._getvalue(), txft__ydjor)
    context.nrt.incref(builder, signature.args[1], pqsgn__sbjqo)
    context.nrt.incref(builder, signature.args[2], ahb__rpa)
    context.nrt.incref(builder, signature.args[3], ytbw__vdf)
    dyedk__bhd = context.make_helper(builder, array_item_type)
    dyedk__bhd.meminfo = qkvdb__rdcol
    return dyedk__bhd._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    dej__pyex = ArrayItemArrayType(data_type)
    sig = dej__pyex(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        gkhg__zav = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            gkhg__zav.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        gkhg__zav = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        fino__tvd = context.make_array(types.Array(offset_type, 1, 'C'))(
            context, builder, gkhg__zav.offsets).data
        ahb__rpa = builder.bitcast(fino__tvd, lir.IntType(offset_type.
            bitwidth).as_pointer())
        return builder.load(builder.gep(ahb__rpa, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        gkhg__zav = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            gkhg__zav.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        gkhg__zav = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            gkhg__zav.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


def alias_ext_single_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_offsets',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array
numba.core.ir_utils.alias_func_extensions['get_data',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array
numba.core.ir_utils.alias_func_extensions['get_null_bitmap',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array


@intrinsic
def get_n_arrays(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        gkhg__zav = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return gkhg__zav.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, uchx__yzzx = args
        dyedk__bhd = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        izq__ijmcg = context.nrt.meminfo_data(builder, dyedk__bhd.meminfo)
        txft__ydjor = builder.bitcast(izq__ijmcg, context.get_value_type(
            payload_type).as_pointer())
        gkhg__zav = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(txft__ydjor))
        context.nrt.decref(builder, data_typ, gkhg__zav.data)
        gkhg__zav.data = uchx__yzzx
        context.nrt.incref(builder, data_typ, uchx__yzzx)
        builder.store(gkhg__zav._getvalue(), txft__ydjor)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    pqsgn__sbjqo = get_data(arr)
    kghmf__zhj = len(pqsgn__sbjqo)
    if kghmf__zhj < new_size:
        drrw__mra = max(2 * kghmf__zhj, new_size)
        uchx__yzzx = bodo.libs.array_kernels.resize_and_copy(pqsgn__sbjqo,
            old_size, drrw__mra)
        replace_data_arr(arr, uchx__yzzx)


@numba.njit(no_cpython_wrapper=True)
def trim_excess_data(arr):
    pqsgn__sbjqo = get_data(arr)
    ahb__rpa = get_offsets(arr)
    jzp__wkwp = len(pqsgn__sbjqo)
    uce__zzzm = ahb__rpa[-1]
    if jzp__wkwp != uce__zzzm:
        uchx__yzzx = bodo.libs.array_kernels.resize_and_copy(pqsgn__sbjqo,
            uce__zzzm, uce__zzzm)
        replace_data_arr(arr, uchx__yzzx)


@overload(len, no_unliteral=True)
def overload_array_item_arr_len(A):
    if isinstance(A, ArrayItemArrayType):
        return lambda A: get_n_arrays(A)


@overload_attribute(ArrayItemArrayType, 'shape')
def overload_array_item_arr_shape(A):
    return lambda A: (get_n_arrays(A),)


@overload_attribute(ArrayItemArrayType, 'dtype')
def overload_array_item_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(ArrayItemArrayType, 'ndim')
def overload_array_item_arr_ndim(A):
    return lambda A: 1


@overload_attribute(ArrayItemArrayType, 'nbytes')
def overload_array_item_arr_nbytes(A):
    return lambda A: get_data(A).nbytes + get_offsets(A
        ).nbytes + get_null_bitmap(A).nbytes


@overload(operator.getitem, no_unliteral=True)
def array_item_arr_getitem_array(arr, ind):
    if not isinstance(arr, ArrayItemArrayType):
        return
    if isinstance(ind, types.Integer):

        def array_item_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            ahb__rpa = get_offsets(arr)
            pqsgn__sbjqo = get_data(arr)
            mlb__ybsma = ahb__rpa[ind]
            hwzhr__eifr = ahb__rpa[ind + 1]
            return pqsgn__sbjqo[mlb__ybsma:hwzhr__eifr]
        return array_item_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        pffm__nhjb = arr.dtype

        def impl_bool(arr, ind):
            fyjeq__gzdh = len(arr)
            if fyjeq__gzdh != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            ytbw__vdf = get_null_bitmap(arr)
            n_arrays = 0
            jzhs__okxj = init_nested_counts(pffm__nhjb)
            for ynwk__mghia in range(fyjeq__gzdh):
                if ind[ynwk__mghia]:
                    n_arrays += 1
                    ehbwb__cbc = arr[ynwk__mghia]
                    jzhs__okxj = add_nested_counts(jzhs__okxj, ehbwb__cbc)
            ngdt__ltv = pre_alloc_array_item_array(n_arrays, jzhs__okxj,
                pffm__nhjb)
            xyqr__oriit = get_null_bitmap(ngdt__ltv)
            laj__oxwj = 0
            for omfz__bqcq in range(fyjeq__gzdh):
                if ind[omfz__bqcq]:
                    ngdt__ltv[laj__oxwj] = arr[omfz__bqcq]
                    zotml__kbll = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        ytbw__vdf, omfz__bqcq)
                    bodo.libs.int_arr_ext.set_bit_to_arr(xyqr__oriit,
                        laj__oxwj, zotml__kbll)
                    laj__oxwj += 1
            return ngdt__ltv
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        pffm__nhjb = arr.dtype

        def impl_int(arr, ind):
            ytbw__vdf = get_null_bitmap(arr)
            fyjeq__gzdh = len(ind)
            n_arrays = fyjeq__gzdh
            jzhs__okxj = init_nested_counts(pffm__nhjb)
            for wezon__pympj in range(fyjeq__gzdh):
                ynwk__mghia = ind[wezon__pympj]
                ehbwb__cbc = arr[ynwk__mghia]
                jzhs__okxj = add_nested_counts(jzhs__okxj, ehbwb__cbc)
            ngdt__ltv = pre_alloc_array_item_array(n_arrays, jzhs__okxj,
                pffm__nhjb)
            xyqr__oriit = get_null_bitmap(ngdt__ltv)
            for gefwu__xkko in range(fyjeq__gzdh):
                omfz__bqcq = ind[gefwu__xkko]
                ngdt__ltv[gefwu__xkko] = arr[omfz__bqcq]
                zotml__kbll = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    ytbw__vdf, omfz__bqcq)
                bodo.libs.int_arr_ext.set_bit_to_arr(xyqr__oriit,
                    gefwu__xkko, zotml__kbll)
            return ngdt__ltv
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            fyjeq__gzdh = len(arr)
            kolyv__dymfs = numba.cpython.unicode._normalize_slice(ind,
                fyjeq__gzdh)
            tfsk__azzm = np.arange(kolyv__dymfs.start, kolyv__dymfs.stop,
                kolyv__dymfs.step)
            return arr[tfsk__azzm]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            ahb__rpa = get_offsets(A)
            ytbw__vdf = get_null_bitmap(A)
            if idx == 0:
                ahb__rpa[0] = 0
            n_items = len(val)
            ptelv__ysagx = ahb__rpa[idx] + n_items
            ensure_data_capacity(A, ahb__rpa[idx], ptelv__ysagx)
            pqsgn__sbjqo = get_data(A)
            ahb__rpa[idx + 1] = ahb__rpa[idx] + n_items
            pqsgn__sbjqo[ahb__rpa[idx]:ahb__rpa[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(ytbw__vdf, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            kolyv__dymfs = numba.cpython.unicode._normalize_slice(idx, len(A))
            for ynwk__mghia in range(kolyv__dymfs.start, kolyv__dymfs.stop,
                kolyv__dymfs.step):
                A[ynwk__mghia] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            ahb__rpa = get_offsets(A)
            ytbw__vdf = get_null_bitmap(A)
            sqwrc__jewj = get_offsets(val)
            oqmfq__acmp = get_data(val)
            fcr__pciwv = get_null_bitmap(val)
            fyjeq__gzdh = len(A)
            kolyv__dymfs = numba.cpython.unicode._normalize_slice(idx,
                fyjeq__gzdh)
            vswxe__cqe, xbnc__mni = kolyv__dymfs.start, kolyv__dymfs.stop
            assert kolyv__dymfs.step == 1
            if vswxe__cqe == 0:
                ahb__rpa[vswxe__cqe] = 0
            svty__upvz = ahb__rpa[vswxe__cqe]
            ptelv__ysagx = svty__upvz + len(oqmfq__acmp)
            ensure_data_capacity(A, svty__upvz, ptelv__ysagx)
            pqsgn__sbjqo = get_data(A)
            pqsgn__sbjqo[svty__upvz:svty__upvz + len(oqmfq__acmp)
                ] = oqmfq__acmp
            ahb__rpa[vswxe__cqe:xbnc__mni + 1] = sqwrc__jewj + svty__upvz
            bywvw__aifc = 0
            for ynwk__mghia in range(vswxe__cqe, xbnc__mni):
                zotml__kbll = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    fcr__pciwv, bywvw__aifc)
                bodo.libs.int_arr_ext.set_bit_to_arr(ytbw__vdf, ynwk__mghia,
                    zotml__kbll)
                bywvw__aifc += 1
        return impl_slice
    raise BodoError(
        'only setitem with scalar index is currently supported for list arrays'
        )


@overload_method(ArrayItemArrayType, 'copy', no_unliteral=True)
def overload_array_item_arr_copy(A):

    def copy_impl(A):
        return init_array_item_array(len(A), get_data(A).copy(),
            get_offsets(A).copy(), get_null_bitmap(A).copy())
    return copy_impl
