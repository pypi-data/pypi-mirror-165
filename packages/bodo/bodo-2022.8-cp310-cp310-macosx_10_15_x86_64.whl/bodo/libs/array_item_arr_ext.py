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
        hng__lotkm = [('n_arrays', types.int64), ('data', fe_type.
            array_type.dtype), ('offsets', types.Array(offset_type, 1, 'C')
            ), ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, hng__lotkm)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        hng__lotkm = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, hng__lotkm)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    kmz__sdlok = builder.module
    hkzd__xrzj = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    dzh__glizi = cgutils.get_or_insert_function(kmz__sdlok, hkzd__xrzj,
        name='.dtor.array_item.{}'.format(array_item_type.dtype))
    if not dzh__glizi.is_declaration:
        return dzh__glizi
    dzh__glizi.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(dzh__glizi.append_basic_block())
    wyge__fqeef = dzh__glizi.args[0]
    fux__tpf = context.get_value_type(payload_type).as_pointer()
    aob__nkfc = builder.bitcast(wyge__fqeef, fux__tpf)
    lbiw__vzym = context.make_helper(builder, payload_type, ref=aob__nkfc)
    context.nrt.decref(builder, array_item_type.dtype, lbiw__vzym.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'),
        lbiw__vzym.offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        lbiw__vzym.null_bitmap)
    builder.ret_void()
    return dzh__glizi


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    lwpf__ezl = context.get_value_type(payload_type)
    sln__dxgvz = context.get_abi_sizeof(lwpf__ezl)
    hros__zadre = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    phnq__rpks = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, sln__dxgvz), hros__zadre)
    qzwd__rzarz = context.nrt.meminfo_data(builder, phnq__rpks)
    eikiv__xlopg = builder.bitcast(qzwd__rzarz, lwpf__ezl.as_pointer())
    lbiw__vzym = cgutils.create_struct_proxy(payload_type)(context, builder)
    lbiw__vzym.n_arrays = n_arrays
    wnypg__ztz = n_elems.type.count
    bobkp__bsw = builder.extract_value(n_elems, 0)
    oebna__gtb = cgutils.alloca_once_value(builder, bobkp__bsw)
    bjgod__rzxw = builder.icmp_signed('==', bobkp__bsw, lir.Constant(
        bobkp__bsw.type, -1))
    with builder.if_then(bjgod__rzxw):
        builder.store(n_arrays, oebna__gtb)
    n_elems = cgutils.pack_array(builder, [builder.load(oebna__gtb)] + [
        builder.extract_value(n_elems, rgm__duwmb) for rgm__duwmb in range(
        1, wnypg__ztz)])
    lbiw__vzym.data = gen_allocate_array(context, builder, array_item_type.
        dtype, n_elems, c)
    mph__qufpa = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    guf__nfu = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [mph__qufpa])
    offsets_ptr = guf__nfu.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    lbiw__vzym.offsets = guf__nfu._getvalue()
    rmsuc__urwb = builder.udiv(builder.add(n_arrays, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    enhda__ljm = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [rmsuc__urwb])
    null_bitmap_ptr = enhda__ljm.data
    lbiw__vzym.null_bitmap = enhda__ljm._getvalue()
    builder.store(lbiw__vzym._getvalue(), eikiv__xlopg)
    return phnq__rpks, lbiw__vzym.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    eqb__mljd, prya__ryib = c.pyapi.call_jit_code(copy_data, sig, [data_arr,
        item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    zhuji__ijet = context.insert_const_string(builder.module, 'pandas')
    fkxl__embuz = c.pyapi.import_module_noblock(zhuji__ijet)
    xmd__klz = c.pyapi.object_getattr_string(fkxl__embuz, 'NA')
    ddab__xpbt = c.context.get_constant(offset_type, 0)
    builder.store(ddab__xpbt, offsets_ptr)
    drf__srezx = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as kporu__bmvv:
        xpc__vvqno = kporu__bmvv.index
        item_ind = builder.load(drf__srezx)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [xpc__vvqno]))
        arr_obj = seq_getitem(builder, context, val, xpc__vvqno)
        set_bitmap_bit(builder, null_bitmap_ptr, xpc__vvqno, 0)
        chun__exu = is_na_value(builder, context, arr_obj, xmd__klz)
        iqtme__qtcx = builder.icmp_unsigned('!=', chun__exu, lir.Constant(
            chun__exu.type, 1))
        with builder.if_then(iqtme__qtcx):
            set_bitmap_bit(builder, null_bitmap_ptr, xpc__vvqno, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), drf__srezx)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(drf__srezx), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(fkxl__embuz)
    c.pyapi.decref(xmd__klz)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    bptp__gtooh = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if bptp__gtooh:
        hkzd__xrzj = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        kcb__cjfou = cgutils.get_or_insert_function(c.builder.module,
            hkzd__xrzj, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(kcb__cjfou,
            [val])])
    else:
        lfxa__gsfg = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            lfxa__gsfg, rgm__duwmb) for rgm__duwmb in range(1, lfxa__gsfg.
            type.count)])
    phnq__rpks, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if bptp__gtooh:
        bid__walkq = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        nzebc__ktat = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        hkzd__xrzj = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        dzh__glizi = cgutils.get_or_insert_function(c.builder.module,
            hkzd__xrzj, name='array_item_array_from_sequence')
        c.builder.call(dzh__glizi, [val, c.builder.bitcast(nzebc__ktat, lir
            .IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), bid__walkq)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    rebfi__izkr = c.context.make_helper(c.builder, typ)
    rebfi__izkr.meminfo = phnq__rpks
    wsc__uga = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(rebfi__izkr._getvalue(), is_error=wsc__uga)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    rebfi__izkr = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    qzwd__rzarz = context.nrt.meminfo_data(builder, rebfi__izkr.meminfo)
    eikiv__xlopg = builder.bitcast(qzwd__rzarz, context.get_value_type(
        payload_type).as_pointer())
    lbiw__vzym = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(eikiv__xlopg))
    return lbiw__vzym


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    zhuji__ijet = context.insert_const_string(builder.module, 'numpy')
    ztcx__fleof = c.pyapi.import_module_noblock(zhuji__ijet)
    badx__zvj = c.pyapi.object_getattr_string(ztcx__fleof, 'object_')
    sifve__bzgrm = c.pyapi.long_from_longlong(n_arrays)
    yyd__syn = c.pyapi.call_method(ztcx__fleof, 'ndarray', (sifve__bzgrm,
        badx__zvj))
    jpilg__fdax = c.pyapi.object_getattr_string(ztcx__fleof, 'nan')
    drf__srezx = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_arrays) as kporu__bmvv:
        xpc__vvqno = kporu__bmvv.index
        pyarray_setitem(builder, context, yyd__syn, xpc__vvqno, jpilg__fdax)
        njrry__fthkh = get_bitmap_bit(builder, null_bitmap_ptr, xpc__vvqno)
        qby__vspfj = builder.icmp_unsigned('!=', njrry__fthkh, lir.Constant
            (lir.IntType(8), 0))
        with builder.if_then(qby__vspfj):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(xpc__vvqno, lir.Constant(
                xpc__vvqno.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [xpc__vvqno]))), lir.IntType(64))
            item_ind = builder.load(drf__srezx)
            eqb__mljd, ymbj__xot = c.pyapi.call_jit_code(lambda data_arr,
                item_ind, n_items: data_arr[item_ind:item_ind + n_items],
                typ.dtype(typ.dtype, types.int64, types.int64), [data_arr,
                item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), drf__srezx)
            arr_obj = c.pyapi.from_native_value(typ.dtype, ymbj__xot, c.
                env_manager)
            pyarray_setitem(builder, context, yyd__syn, xpc__vvqno, arr_obj)
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(ztcx__fleof)
    c.pyapi.decref(badx__zvj)
    c.pyapi.decref(sifve__bzgrm)
    c.pyapi.decref(jpilg__fdax)
    return yyd__syn


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    lbiw__vzym = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = lbiw__vzym.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), lbiw__vzym.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), lbiw__vzym.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        bid__walkq = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        nzebc__ktat = c.context.make_helper(c.builder, typ.dtype, data_arr
            ).data
        hkzd__xrzj = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        fruaw__xxlz = cgutils.get_or_insert_function(c.builder.module,
            hkzd__xrzj, name='np_array_from_array_item_array')
        arr = c.builder.call(fruaw__xxlz, [lbiw__vzym.n_arrays, c.builder.
            bitcast(nzebc__ktat, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), bid__walkq)])
    else:
        arr = _box_array_item_array_generic(typ, c, lbiw__vzym.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    gfy__ymxh, ebu__auzgb, jyafl__vjxtt = args
    sthk__jqfs = bodo.utils.transform.get_type_alloc_counts(array_item_type
        .dtype)
    ugaar__zzwz = sig.args[1]
    if not isinstance(ugaar__zzwz, types.UniTuple):
        ebu__auzgb = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), -1) for jyafl__vjxtt in range(sthk__jqfs)])
    elif ugaar__zzwz.count < sthk__jqfs:
        ebu__auzgb = cgutils.pack_array(builder, [builder.extract_value(
            ebu__auzgb, rgm__duwmb) for rgm__duwmb in range(ugaar__zzwz.
            count)] + [lir.Constant(lir.IntType(64), -1) for jyafl__vjxtt in
            range(sthk__jqfs - ugaar__zzwz.count)])
    phnq__rpks, jyafl__vjxtt, jyafl__vjxtt, jyafl__vjxtt = (
        construct_array_item_array(context, builder, array_item_type,
        gfy__ymxh, ebu__auzgb))
    rebfi__izkr = context.make_helper(builder, array_item_type)
    rebfi__izkr.meminfo = phnq__rpks
    return rebfi__izkr._getvalue()


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
    n_arrays, mtu__srkz, guf__nfu, enhda__ljm = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    lwpf__ezl = context.get_value_type(payload_type)
    sln__dxgvz = context.get_abi_sizeof(lwpf__ezl)
    hros__zadre = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    phnq__rpks = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, sln__dxgvz), hros__zadre)
    qzwd__rzarz = context.nrt.meminfo_data(builder, phnq__rpks)
    eikiv__xlopg = builder.bitcast(qzwd__rzarz, lwpf__ezl.as_pointer())
    lbiw__vzym = cgutils.create_struct_proxy(payload_type)(context, builder)
    lbiw__vzym.n_arrays = n_arrays
    lbiw__vzym.data = mtu__srkz
    lbiw__vzym.offsets = guf__nfu
    lbiw__vzym.null_bitmap = enhda__ljm
    builder.store(lbiw__vzym._getvalue(), eikiv__xlopg)
    context.nrt.incref(builder, signature.args[1], mtu__srkz)
    context.nrt.incref(builder, signature.args[2], guf__nfu)
    context.nrt.incref(builder, signature.args[3], enhda__ljm)
    rebfi__izkr = context.make_helper(builder, array_item_type)
    rebfi__izkr.meminfo = phnq__rpks
    return rebfi__izkr._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    lavfe__llb = ArrayItemArrayType(data_type)
    sig = lavfe__llb(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        lbiw__vzym = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return impl_ret_borrowed(context, builder, sig.return_type,
            lbiw__vzym.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        lbiw__vzym = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        nzebc__ktat = context.make_array(types.Array(offset_type, 1, 'C'))(
            context, builder, lbiw__vzym.offsets).data
        guf__nfu = builder.bitcast(nzebc__ktat, lir.IntType(offset_type.
            bitwidth).as_pointer())
        return builder.load(builder.gep(guf__nfu, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        lbiw__vzym = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return impl_ret_borrowed(context, builder, sig.return_type,
            lbiw__vzym.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        lbiw__vzym = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return impl_ret_borrowed(context, builder, sig.return_type,
            lbiw__vzym.null_bitmap)
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
        lbiw__vzym = _get_array_item_arr_payload(context, builder, arr_typ, arr
            )
        return lbiw__vzym.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, pyqh__togos = args
        rebfi__izkr = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        qzwd__rzarz = context.nrt.meminfo_data(builder, rebfi__izkr.meminfo)
        eikiv__xlopg = builder.bitcast(qzwd__rzarz, context.get_value_type(
            payload_type).as_pointer())
        lbiw__vzym = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(eikiv__xlopg))
        context.nrt.decref(builder, data_typ, lbiw__vzym.data)
        lbiw__vzym.data = pyqh__togos
        context.nrt.incref(builder, data_typ, pyqh__togos)
        builder.store(lbiw__vzym._getvalue(), eikiv__xlopg)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    mtu__srkz = get_data(arr)
    kmr__nburf = len(mtu__srkz)
    if kmr__nburf < new_size:
        shkhr__fuwn = max(2 * kmr__nburf, new_size)
        pyqh__togos = bodo.libs.array_kernels.resize_and_copy(mtu__srkz,
            old_size, shkhr__fuwn)
        replace_data_arr(arr, pyqh__togos)


@numba.njit(no_cpython_wrapper=True)
def trim_excess_data(arr):
    mtu__srkz = get_data(arr)
    guf__nfu = get_offsets(arr)
    jto__qornu = len(mtu__srkz)
    ptq__ajr = guf__nfu[-1]
    if jto__qornu != ptq__ajr:
        pyqh__togos = bodo.libs.array_kernels.resize_and_copy(mtu__srkz,
            ptq__ajr, ptq__ajr)
        replace_data_arr(arr, pyqh__togos)


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
            guf__nfu = get_offsets(arr)
            mtu__srkz = get_data(arr)
            too__zqd = guf__nfu[ind]
            plvyf__fytoc = guf__nfu[ind + 1]
            return mtu__srkz[too__zqd:plvyf__fytoc]
        return array_item_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        qqc__tkks = arr.dtype

        def impl_bool(arr, ind):
            mlchz__jhmhd = len(arr)
            if mlchz__jhmhd != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            enhda__ljm = get_null_bitmap(arr)
            n_arrays = 0
            ccba__aty = init_nested_counts(qqc__tkks)
            for rgm__duwmb in range(mlchz__jhmhd):
                if ind[rgm__duwmb]:
                    n_arrays += 1
                    xgsmz__luf = arr[rgm__duwmb]
                    ccba__aty = add_nested_counts(ccba__aty, xgsmz__luf)
            yyd__syn = pre_alloc_array_item_array(n_arrays, ccba__aty,
                qqc__tkks)
            orygh__jhmo = get_null_bitmap(yyd__syn)
            svc__ggjx = 0
            for nbuce__bwuj in range(mlchz__jhmhd):
                if ind[nbuce__bwuj]:
                    yyd__syn[svc__ggjx] = arr[nbuce__bwuj]
                    gevyl__ncbu = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        enhda__ljm, nbuce__bwuj)
                    bodo.libs.int_arr_ext.set_bit_to_arr(orygh__jhmo,
                        svc__ggjx, gevyl__ncbu)
                    svc__ggjx += 1
            return yyd__syn
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        qqc__tkks = arr.dtype

        def impl_int(arr, ind):
            enhda__ljm = get_null_bitmap(arr)
            mlchz__jhmhd = len(ind)
            n_arrays = mlchz__jhmhd
            ccba__aty = init_nested_counts(qqc__tkks)
            for svy__ectgr in range(mlchz__jhmhd):
                rgm__duwmb = ind[svy__ectgr]
                xgsmz__luf = arr[rgm__duwmb]
                ccba__aty = add_nested_counts(ccba__aty, xgsmz__luf)
            yyd__syn = pre_alloc_array_item_array(n_arrays, ccba__aty,
                qqc__tkks)
            orygh__jhmo = get_null_bitmap(yyd__syn)
            for nvslc__njxb in range(mlchz__jhmhd):
                nbuce__bwuj = ind[nvslc__njxb]
                yyd__syn[nvslc__njxb] = arr[nbuce__bwuj]
                gevyl__ncbu = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    enhda__ljm, nbuce__bwuj)
                bodo.libs.int_arr_ext.set_bit_to_arr(orygh__jhmo,
                    nvslc__njxb, gevyl__ncbu)
            return yyd__syn
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            mlchz__jhmhd = len(arr)
            ytbj__iaj = numba.cpython.unicode._normalize_slice(ind,
                mlchz__jhmhd)
            ylei__kgu = np.arange(ytbj__iaj.start, ytbj__iaj.stop,
                ytbj__iaj.step)
            return arr[ylei__kgu]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            guf__nfu = get_offsets(A)
            enhda__ljm = get_null_bitmap(A)
            if idx == 0:
                guf__nfu[0] = 0
            n_items = len(val)
            ejjo__gnlz = guf__nfu[idx] + n_items
            ensure_data_capacity(A, guf__nfu[idx], ejjo__gnlz)
            mtu__srkz = get_data(A)
            guf__nfu[idx + 1] = guf__nfu[idx] + n_items
            mtu__srkz[guf__nfu[idx]:guf__nfu[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(enhda__ljm, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            ytbj__iaj = numba.cpython.unicode._normalize_slice(idx, len(A))
            for rgm__duwmb in range(ytbj__iaj.start, ytbj__iaj.stop,
                ytbj__iaj.step):
                A[rgm__duwmb] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            guf__nfu = get_offsets(A)
            enhda__ljm = get_null_bitmap(A)
            zyzf__aya = get_offsets(val)
            dgirt__bli = get_data(val)
            reb__pdih = get_null_bitmap(val)
            mlchz__jhmhd = len(A)
            ytbj__iaj = numba.cpython.unicode._normalize_slice(idx,
                mlchz__jhmhd)
            egm__lvkl, cce__zrew = ytbj__iaj.start, ytbj__iaj.stop
            assert ytbj__iaj.step == 1
            if egm__lvkl == 0:
                guf__nfu[egm__lvkl] = 0
            iyes__avcgt = guf__nfu[egm__lvkl]
            ejjo__gnlz = iyes__avcgt + len(dgirt__bli)
            ensure_data_capacity(A, iyes__avcgt, ejjo__gnlz)
            mtu__srkz = get_data(A)
            mtu__srkz[iyes__avcgt:iyes__avcgt + len(dgirt__bli)] = dgirt__bli
            guf__nfu[egm__lvkl:cce__zrew + 1] = zyzf__aya + iyes__avcgt
            bdzok__mpk = 0
            for rgm__duwmb in range(egm__lvkl, cce__zrew):
                gevyl__ncbu = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    reb__pdih, bdzok__mpk)
                bodo.libs.int_arr_ext.set_bit_to_arr(enhda__ljm, rgm__duwmb,
                    gevyl__ncbu)
                bdzok__mpk += 1
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
