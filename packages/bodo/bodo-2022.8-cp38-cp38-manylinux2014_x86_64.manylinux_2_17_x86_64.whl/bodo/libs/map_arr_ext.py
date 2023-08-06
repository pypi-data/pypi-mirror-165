"""Array implementation for map values.
Corresponds to Spark's MapType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Map arrays: https://github.com/apache/arrow/blob/master/format/Schema.fbs

The implementation uses an array(struct) array underneath similar to Spark and Arrow.
For example: [{1: 2.1, 3: 1.1}, {5: -1.0}]
[[{"key": 1, "value" 2.1}, {"key": 3, "value": 1.1}], [{"key": 5, "value": -1.0}]]
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, _get_array_item_arr_payload, offset_type
from bodo.libs.struct_arr_ext import StructArrayType, _get_struct_arr_payload
from bodo.utils.cg_helpers import dict_keys, dict_merge_from_seq2, dict_values, gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit
from bodo.utils.typing import BodoError
from bodo.libs import array_ext, hdist
ll.add_symbol('count_total_elems_list_array', array_ext.
    count_total_elems_list_array)
ll.add_symbol('map_array_from_sequence', array_ext.map_array_from_sequence)
ll.add_symbol('np_array_from_map_array', array_ext.np_array_from_map_array)


class MapArrayType(types.ArrayCompatible):

    def __init__(self, key_arr_type, value_arr_type):
        self.key_arr_type = key_arr_type
        self.value_arr_type = value_arr_type
        super(MapArrayType, self).__init__(name='MapArrayType({}, {})'.
            format(key_arr_type, value_arr_type))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.DictType(self.key_arr_type.dtype, self.value_arr_type.
            dtype)

    def copy(self):
        return MapArrayType(self.key_arr_type, self.value_arr_type)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


def _get_map_arr_data_type(map_type):
    fcaue__koaft = StructArrayType((map_type.key_arr_type, map_type.
        value_arr_type), ('key', 'value'))
    return ArrayItemArrayType(fcaue__koaft)


@register_model(MapArrayType)
class MapArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        uiytw__pyijh = _get_map_arr_data_type(fe_type)
        ewu__wimhb = [('data', uiytw__pyijh)]
        models.StructModel.__init__(self, dmm, fe_type, ewu__wimhb)


make_attribute_wrapper(MapArrayType, 'data', '_data')


@unbox(MapArrayType)
def unbox_map_array(typ, val, c):
    n_maps = bodo.utils.utils.object_length(c, val)
    fclat__njho = all(isinstance(fvdkc__tzfmj, types.Array) and 
        fvdkc__tzfmj.dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for fvdkc__tzfmj in (typ.key_arr_type, typ.
        value_arr_type))
    if fclat__njho:
        qbcja__enbah = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        kgxy__ltxb = cgutils.get_or_insert_function(c.builder.module,
            qbcja__enbah, name='count_total_elems_list_array')
        pnf__zjry = cgutils.pack_array(c.builder, [n_maps, c.builder.call(
            kgxy__ltxb, [val])])
    else:
        pnf__zjry = get_array_elem_counts(c, c.builder, c.context, val, typ)
    uiytw__pyijh = _get_map_arr_data_type(typ)
    data_arr = gen_allocate_array(c.context, c.builder, uiytw__pyijh,
        pnf__zjry, c)
    lmiy__yxj = _get_array_item_arr_payload(c.context, c.builder,
        uiytw__pyijh, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, lmiy__yxj.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, lmiy__yxj.offsets).data
    atta__wkqeo = _get_struct_arr_payload(c.context, c.builder,
        uiytw__pyijh.dtype, lmiy__yxj.data)
    key_arr = c.builder.extract_value(atta__wkqeo.data, 0)
    value_arr = c.builder.extract_value(atta__wkqeo.data, 1)
    sig = types.none(types.Array(types.uint8, 1, 'C'))
    xplt__fmupe, rpl__tywie = c.pyapi.call_jit_code(lambda A: A.fill(255),
        sig, [atta__wkqeo.null_bitmap])
    if fclat__njho:
        xfjah__vgz = c.context.make_array(uiytw__pyijh.dtype.data[0])(c.
            context, c.builder, key_arr).data
        xyyl__ngwxl = c.context.make_array(uiytw__pyijh.dtype.data[1])(c.
            context, c.builder, value_arr).data
        qbcja__enbah = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
        nyqr__ynggb = cgutils.get_or_insert_function(c.builder.module,
            qbcja__enbah, name='map_array_from_sequence')
        zhj__gzp = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        hxusi__ubei = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype
            )
        c.builder.call(nyqr__ynggb, [val, c.builder.bitcast(xfjah__vgz, lir
            .IntType(8).as_pointer()), c.builder.bitcast(xyyl__ngwxl, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), zhj__gzp), lir.Constant(lir.IntType(
            32), hxusi__ubei)])
    else:
        _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
            offsets_ptr, null_bitmap_ptr)
    app__uvbv = c.context.make_helper(c.builder, typ)
    app__uvbv.data = data_arr
    kdis__fku = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(app__uvbv._getvalue(), is_error=kdis__fku)


def _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
    offsets_ptr, null_bitmap_ptr):
    from bodo.libs.array_item_arr_ext import _unbox_array_item_array_copy_data
    context = c.context
    builder = c.builder
    dey__qfonr = context.insert_const_string(builder.module, 'pandas')
    cmco__zre = c.pyapi.import_module_noblock(dey__qfonr)
    ldw__lbmll = c.pyapi.object_getattr_string(cmco__zre, 'NA')
    imxx__ecvc = c.context.get_constant(offset_type, 0)
    builder.store(imxx__ecvc, offsets_ptr)
    oltpp__knsha = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_maps) as wvns__eqs:
        eqbt__ckwqt = wvns__eqs.index
        item_ind = builder.load(oltpp__knsha)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [eqbt__ckwqt]))
        ajw__twnq = seq_getitem(builder, context, val, eqbt__ckwqt)
        set_bitmap_bit(builder, null_bitmap_ptr, eqbt__ckwqt, 0)
        gfbz__nihkd = is_na_value(builder, context, ajw__twnq, ldw__lbmll)
        qsr__nmk = builder.icmp_unsigned('!=', gfbz__nihkd, lir.Constant(
            gfbz__nihkd.type, 1))
        with builder.if_then(qsr__nmk):
            set_bitmap_bit(builder, null_bitmap_ptr, eqbt__ckwqt, 1)
            axn__mwy = dict_keys(builder, context, ajw__twnq)
            otwp__vkycj = dict_values(builder, context, ajw__twnq)
            n_items = bodo.utils.utils.object_length(c, axn__mwy)
            _unbox_array_item_array_copy_data(typ.key_arr_type, axn__mwy, c,
                key_arr, item_ind, n_items)
            _unbox_array_item_array_copy_data(typ.value_arr_type,
                otwp__vkycj, c, value_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), oltpp__knsha)
            c.pyapi.decref(axn__mwy)
            c.pyapi.decref(otwp__vkycj)
        c.pyapi.decref(ajw__twnq)
    builder.store(builder.trunc(builder.load(oltpp__knsha), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_maps]))
    c.pyapi.decref(cmco__zre)
    c.pyapi.decref(ldw__lbmll)


@box(MapArrayType)
def box_map_arr(typ, val, c):
    app__uvbv = c.context.make_helper(c.builder, typ, val)
    data_arr = app__uvbv.data
    uiytw__pyijh = _get_map_arr_data_type(typ)
    lmiy__yxj = _get_array_item_arr_payload(c.context, c.builder,
        uiytw__pyijh, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, lmiy__yxj.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, lmiy__yxj.offsets).data
    atta__wkqeo = _get_struct_arr_payload(c.context, c.builder,
        uiytw__pyijh.dtype, lmiy__yxj.data)
    key_arr = c.builder.extract_value(atta__wkqeo.data, 0)
    value_arr = c.builder.extract_value(atta__wkqeo.data, 1)
    if all(isinstance(fvdkc__tzfmj, types.Array) and fvdkc__tzfmj.dtype in
        (types.int64, types.float64, types.bool_, datetime_date_type) for
        fvdkc__tzfmj in (typ.key_arr_type, typ.value_arr_type)):
        xfjah__vgz = c.context.make_array(uiytw__pyijh.dtype.data[0])(c.
            context, c.builder, key_arr).data
        xyyl__ngwxl = c.context.make_array(uiytw__pyijh.dtype.data[1])(c.
            context, c.builder, value_arr).data
        qbcja__enbah = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(offset_type.bitwidth).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(32)])
        lba__hcem = cgutils.get_or_insert_function(c.builder.module,
            qbcja__enbah, name='np_array_from_map_array')
        zhj__gzp = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        hxusi__ubei = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype
            )
        arr = c.builder.call(lba__hcem, [lmiy__yxj.n_arrays, c.builder.
            bitcast(xfjah__vgz, lir.IntType(8).as_pointer()), c.builder.
            bitcast(xyyl__ngwxl, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), zhj__gzp), lir.
            Constant(lir.IntType(32), hxusi__ubei)])
    else:
        arr = _box_map_array_generic(typ, c, lmiy__yxj.n_arrays, key_arr,
            value_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_map_array_generic(typ, c, n_maps, key_arr, value_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    dey__qfonr = context.insert_const_string(builder.module, 'numpy')
    ojg__jfvzw = c.pyapi.import_module_noblock(dey__qfonr)
    rwj__khzv = c.pyapi.object_getattr_string(ojg__jfvzw, 'object_')
    zekp__iqzi = c.pyapi.long_from_longlong(n_maps)
    idza__gjewm = c.pyapi.call_method(ojg__jfvzw, 'ndarray', (zekp__iqzi,
        rwj__khzv))
    jjm__unayq = c.pyapi.object_getattr_string(ojg__jfvzw, 'nan')
    zlkmx__pvea = c.pyapi.unserialize(c.pyapi.serialize_object(zip))
    oltpp__knsha = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_maps) as wvns__eqs:
        adrd__cdzg = wvns__eqs.index
        pyarray_setitem(builder, context, idza__gjewm, adrd__cdzg, jjm__unayq)
        zuc__rqabm = get_bitmap_bit(builder, null_bitmap_ptr, adrd__cdzg)
        vyco__lyw = builder.icmp_unsigned('!=', zuc__rqabm, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(vyco__lyw):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(adrd__cdzg, lir.Constant(
                adrd__cdzg.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [adrd__cdzg]))), lir.IntType(64))
            item_ind = builder.load(oltpp__knsha)
            ajw__twnq = c.pyapi.dict_new()
            abtj__uwwkz = lambda data_arr, item_ind, n_items: data_arr[item_ind
                :item_ind + n_items]
            xplt__fmupe, wjjh__hjo = c.pyapi.call_jit_code(abtj__uwwkz, typ
                .key_arr_type(typ.key_arr_type, types.int64, types.int64),
                [key_arr, item_ind, n_items])
            xplt__fmupe, wgbbv__geaar = c.pyapi.call_jit_code(abtj__uwwkz,
                typ.value_arr_type(typ.value_arr_type, types.int64, types.
                int64), [value_arr, item_ind, n_items])
            jsc__fcsqx = c.pyapi.from_native_value(typ.key_arr_type,
                wjjh__hjo, c.env_manager)
            capy__jwkj = c.pyapi.from_native_value(typ.value_arr_type,
                wgbbv__geaar, c.env_manager)
            tsblt__vxlsp = c.pyapi.call_function_objargs(zlkmx__pvea, (
                jsc__fcsqx, capy__jwkj))
            dict_merge_from_seq2(builder, context, ajw__twnq, tsblt__vxlsp)
            builder.store(builder.add(item_ind, n_items), oltpp__knsha)
            pyarray_setitem(builder, context, idza__gjewm, adrd__cdzg,
                ajw__twnq)
            c.pyapi.decref(tsblt__vxlsp)
            c.pyapi.decref(jsc__fcsqx)
            c.pyapi.decref(capy__jwkj)
            c.pyapi.decref(ajw__twnq)
    c.pyapi.decref(zlkmx__pvea)
    c.pyapi.decref(ojg__jfvzw)
    c.pyapi.decref(rwj__khzv)
    c.pyapi.decref(zekp__iqzi)
    c.pyapi.decref(jjm__unayq)
    return idza__gjewm


def init_map_arr_codegen(context, builder, sig, args):
    data_arr, = args
    app__uvbv = context.make_helper(builder, sig.return_type)
    app__uvbv.data = data_arr
    context.nrt.incref(builder, sig.args[0], data_arr)
    return app__uvbv._getvalue()


@intrinsic
def init_map_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType) and isinstance(data_typ
        .dtype, StructArrayType)
    oyqzw__bnvfe = MapArrayType(data_typ.dtype.data[0], data_typ.dtype.data[1])
    return oyqzw__bnvfe(data_typ), init_map_arr_codegen


def alias_ext_init_map_arr(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_map_arr',
    'bodo.libs.map_arr_ext'] = alias_ext_init_map_arr


@numba.njit
def pre_alloc_map_array(num_maps, nested_counts, struct_typ):
    gimkx__ztu = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        num_maps, nested_counts, struct_typ)
    return init_map_arr(gimkx__ztu)


def pre_alloc_map_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_map_arr_ext_pre_alloc_map_array
    ) = pre_alloc_map_array_equiv


@overload(len, no_unliteral=True)
def overload_map_arr_len(A):
    if isinstance(A, MapArrayType):
        return lambda A: len(A._data)


@overload_attribute(MapArrayType, 'shape')
def overload_map_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(MapArrayType, 'dtype')
def overload_map_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(MapArrayType, 'ndim')
def overload_map_arr_ndim(A):
    return lambda A: 1


@overload_attribute(MapArrayType, 'nbytes')
def overload_map_arr_nbytes(A):
    return lambda A: A._data.nbytes


@overload_method(MapArrayType, 'copy')
def overload_map_arr_copy(A):
    return lambda A: init_map_arr(A._data.copy())


@overload(operator.setitem, no_unliteral=True)
def map_arr_setitem(arr, ind, val):
    if not isinstance(arr, MapArrayType):
        return
    wprc__ajf = arr.key_arr_type, arr.value_arr_type
    if isinstance(ind, types.Integer):

        def map_arr_setitem_impl(arr, ind, val):
            rys__mrbb = val.keys()
            bnz__pyhlz = bodo.libs.struct_arr_ext.pre_alloc_struct_array(len
                (val), (-1,), wprc__ajf, ('key', 'value'))
            for ayu__syss, ktgmr__yrvp in enumerate(rys__mrbb):
                bnz__pyhlz[ayu__syss] = bodo.libs.struct_arr_ext.init_struct((
                    ktgmr__yrvp, val[ktgmr__yrvp]), ('key', 'value'))
            arr._data[ind] = bnz__pyhlz
        return map_arr_setitem_impl
    raise BodoError(
        'operator.setitem with MapArrays is only supported with an integer index.'
        )


@overload(operator.getitem, no_unliteral=True)
def map_arr_getitem(arr, ind):
    if not isinstance(arr, MapArrayType):
        return
    if isinstance(ind, types.Integer):

        def map_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            edvjo__yhxqk = dict()
            svojr__iiade = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            bnz__pyhlz = bodo.libs.array_item_arr_ext.get_data(arr._data)
            dil__muf, laa__pxgi = bodo.libs.struct_arr_ext.get_data(bnz__pyhlz)
            lfn__akzj = svojr__iiade[ind]
            jqfl__dsyra = svojr__iiade[ind + 1]
            for ayu__syss in range(lfn__akzj, jqfl__dsyra):
                edvjo__yhxqk[dil__muf[ayu__syss]] = laa__pxgi[ayu__syss]
            return edvjo__yhxqk
        return map_arr_getitem_impl
    raise BodoError(
        'operator.getitem with MapArrays is only supported with an integer index.'
        )
