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
    nlp__jmfl = StructArrayType((map_type.key_arr_type, map_type.
        value_arr_type), ('key', 'value'))
    return ArrayItemArrayType(nlp__jmfl)


@register_model(MapArrayType)
class MapArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        rweac__ggr = _get_map_arr_data_type(fe_type)
        ivq__xcu = [('data', rweac__ggr)]
        models.StructModel.__init__(self, dmm, fe_type, ivq__xcu)


make_attribute_wrapper(MapArrayType, 'data', '_data')


@unbox(MapArrayType)
def unbox_map_array(typ, val, c):
    n_maps = bodo.utils.utils.object_length(c, val)
    ayqdx__njl = all(isinstance(tjj__qinl, types.Array) and tjj__qinl.dtype in
        (types.int64, types.float64, types.bool_, datetime_date_type) for
        tjj__qinl in (typ.key_arr_type, typ.value_arr_type))
    if ayqdx__njl:
        xpubu__mch = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        qks__tpse = cgutils.get_or_insert_function(c.builder.module,
            xpubu__mch, name='count_total_elems_list_array')
        wlb__ryaat = cgutils.pack_array(c.builder, [n_maps, c.builder.call(
            qks__tpse, [val])])
    else:
        wlb__ryaat = get_array_elem_counts(c, c.builder, c.context, val, typ)
    rweac__ggr = _get_map_arr_data_type(typ)
    data_arr = gen_allocate_array(c.context, c.builder, rweac__ggr,
        wlb__ryaat, c)
    eacns__stcgc = _get_array_item_arr_payload(c.context, c.builder,
        rweac__ggr, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, eacns__stcgc.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, eacns__stcgc.offsets).data
    piwcz__rie = _get_struct_arr_payload(c.context, c.builder, rweac__ggr.
        dtype, eacns__stcgc.data)
    key_arr = c.builder.extract_value(piwcz__rie.data, 0)
    value_arr = c.builder.extract_value(piwcz__rie.data, 1)
    sig = types.none(types.Array(types.uint8, 1, 'C'))
    yjdjj__vlf, kye__esy = c.pyapi.call_jit_code(lambda A: A.fill(255), sig,
        [piwcz__rie.null_bitmap])
    if ayqdx__njl:
        ageov__gfzg = c.context.make_array(rweac__ggr.dtype.data[0])(c.
            context, c.builder, key_arr).data
        eahzj__jbpe = c.context.make_array(rweac__ggr.dtype.data[1])(c.
            context, c.builder, value_arr).data
        xpubu__mch = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
        hpnc__fdmt = cgutils.get_or_insert_function(c.builder.module,
            xpubu__mch, name='map_array_from_sequence')
        qda__pqeds = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        vgo__opqex = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        c.builder.call(hpnc__fdmt, [val, c.builder.bitcast(ageov__gfzg, lir
            .IntType(8).as_pointer()), c.builder.bitcast(eahzj__jbpe, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), qda__pqeds), lir.Constant(lir.IntType
            (32), vgo__opqex)])
    else:
        _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
            offsets_ptr, null_bitmap_ptr)
    yscxk__ydzg = c.context.make_helper(c.builder, typ)
    yscxk__ydzg.data = data_arr
    axb__aid = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(yscxk__ydzg._getvalue(), is_error=axb__aid)


def _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
    offsets_ptr, null_bitmap_ptr):
    from bodo.libs.array_item_arr_ext import _unbox_array_item_array_copy_data
    context = c.context
    builder = c.builder
    ygje__sagky = context.insert_const_string(builder.module, 'pandas')
    rsy__jfysk = c.pyapi.import_module_noblock(ygje__sagky)
    sydg__fxu = c.pyapi.object_getattr_string(rsy__jfysk, 'NA')
    sjcfj__jzw = c.context.get_constant(offset_type, 0)
    builder.store(sjcfj__jzw, offsets_ptr)
    lvz__doiq = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_maps) as tdj__uas:
        bhe__dwvoj = tdj__uas.index
        item_ind = builder.load(lvz__doiq)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [bhe__dwvoj]))
        kwbbg__hzghz = seq_getitem(builder, context, val, bhe__dwvoj)
        set_bitmap_bit(builder, null_bitmap_ptr, bhe__dwvoj, 0)
        cqmb__tld = is_na_value(builder, context, kwbbg__hzghz, sydg__fxu)
        echf__jkjyn = builder.icmp_unsigned('!=', cqmb__tld, lir.Constant(
            cqmb__tld.type, 1))
        with builder.if_then(echf__jkjyn):
            set_bitmap_bit(builder, null_bitmap_ptr, bhe__dwvoj, 1)
            woa__fpk = dict_keys(builder, context, kwbbg__hzghz)
            kpk__athl = dict_values(builder, context, kwbbg__hzghz)
            n_items = bodo.utils.utils.object_length(c, woa__fpk)
            _unbox_array_item_array_copy_data(typ.key_arr_type, woa__fpk, c,
                key_arr, item_ind, n_items)
            _unbox_array_item_array_copy_data(typ.value_arr_type, kpk__athl,
                c, value_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), lvz__doiq)
            c.pyapi.decref(woa__fpk)
            c.pyapi.decref(kpk__athl)
        c.pyapi.decref(kwbbg__hzghz)
    builder.store(builder.trunc(builder.load(lvz__doiq), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_maps]))
    c.pyapi.decref(rsy__jfysk)
    c.pyapi.decref(sydg__fxu)


@box(MapArrayType)
def box_map_arr(typ, val, c):
    yscxk__ydzg = c.context.make_helper(c.builder, typ, val)
    data_arr = yscxk__ydzg.data
    rweac__ggr = _get_map_arr_data_type(typ)
    eacns__stcgc = _get_array_item_arr_payload(c.context, c.builder,
        rweac__ggr, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, eacns__stcgc.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, eacns__stcgc.offsets).data
    piwcz__rie = _get_struct_arr_payload(c.context, c.builder, rweac__ggr.
        dtype, eacns__stcgc.data)
    key_arr = c.builder.extract_value(piwcz__rie.data, 0)
    value_arr = c.builder.extract_value(piwcz__rie.data, 1)
    if all(isinstance(tjj__qinl, types.Array) and tjj__qinl.dtype in (types
        .int64, types.float64, types.bool_, datetime_date_type) for
        tjj__qinl in (typ.key_arr_type, typ.value_arr_type)):
        ageov__gfzg = c.context.make_array(rweac__ggr.dtype.data[0])(c.
            context, c.builder, key_arr).data
        eahzj__jbpe = c.context.make_array(rweac__ggr.dtype.data[1])(c.
            context, c.builder, value_arr).data
        xpubu__mch = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(offset_type.bitwidth).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(32)])
        apu__lxxiv = cgutils.get_or_insert_function(c.builder.module,
            xpubu__mch, name='np_array_from_map_array')
        qda__pqeds = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        vgo__opqex = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        arr = c.builder.call(apu__lxxiv, [eacns__stcgc.n_arrays, c.builder.
            bitcast(ageov__gfzg, lir.IntType(8).as_pointer()), c.builder.
            bitcast(eahzj__jbpe, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), qda__pqeds), lir
            .Constant(lir.IntType(32), vgo__opqex)])
    else:
        arr = _box_map_array_generic(typ, c, eacns__stcgc.n_arrays, key_arr,
            value_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_map_array_generic(typ, c, n_maps, key_arr, value_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    ygje__sagky = context.insert_const_string(builder.module, 'numpy')
    eav__hgda = c.pyapi.import_module_noblock(ygje__sagky)
    eomfy__munx = c.pyapi.object_getattr_string(eav__hgda, 'object_')
    kycyk__rpilc = c.pyapi.long_from_longlong(n_maps)
    ecvow__dsax = c.pyapi.call_method(eav__hgda, 'ndarray', (kycyk__rpilc,
        eomfy__munx))
    ailns__gqgf = c.pyapi.object_getattr_string(eav__hgda, 'nan')
    fekfl__cvdah = c.pyapi.unserialize(c.pyapi.serialize_object(zip))
    lvz__doiq = cgutils.alloca_once_value(builder, lir.Constant(lir.IntType
        (64), 0))
    with cgutils.for_range(builder, n_maps) as tdj__uas:
        sed__ecahp = tdj__uas.index
        pyarray_setitem(builder, context, ecvow__dsax, sed__ecahp, ailns__gqgf)
        wja__fzo = get_bitmap_bit(builder, null_bitmap_ptr, sed__ecahp)
        eupde__qic = builder.icmp_unsigned('!=', wja__fzo, lir.Constant(lir
            .IntType(8), 0))
        with builder.if_then(eupde__qic):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(sed__ecahp, lir.Constant(
                sed__ecahp.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [sed__ecahp]))), lir.IntType(64))
            item_ind = builder.load(lvz__doiq)
            kwbbg__hzghz = c.pyapi.dict_new()
            vay__bbqmz = lambda data_arr, item_ind, n_items: data_arr[item_ind
                :item_ind + n_items]
            yjdjj__vlf, ukra__hkig = c.pyapi.call_jit_code(vay__bbqmz, typ.
                key_arr_type(typ.key_arr_type, types.int64, types.int64), [
                key_arr, item_ind, n_items])
            yjdjj__vlf, deyds__bmkc = c.pyapi.call_jit_code(vay__bbqmz, typ
                .value_arr_type(typ.value_arr_type, types.int64, types.
                int64), [value_arr, item_ind, n_items])
            ged__lyvxz = c.pyapi.from_native_value(typ.key_arr_type,
                ukra__hkig, c.env_manager)
            pjd__apej = c.pyapi.from_native_value(typ.value_arr_type,
                deyds__bmkc, c.env_manager)
            ueeom__wyrai = c.pyapi.call_function_objargs(fekfl__cvdah, (
                ged__lyvxz, pjd__apej))
            dict_merge_from_seq2(builder, context, kwbbg__hzghz, ueeom__wyrai)
            builder.store(builder.add(item_ind, n_items), lvz__doiq)
            pyarray_setitem(builder, context, ecvow__dsax, sed__ecahp,
                kwbbg__hzghz)
            c.pyapi.decref(ueeom__wyrai)
            c.pyapi.decref(ged__lyvxz)
            c.pyapi.decref(pjd__apej)
            c.pyapi.decref(kwbbg__hzghz)
    c.pyapi.decref(fekfl__cvdah)
    c.pyapi.decref(eav__hgda)
    c.pyapi.decref(eomfy__munx)
    c.pyapi.decref(kycyk__rpilc)
    c.pyapi.decref(ailns__gqgf)
    return ecvow__dsax


def init_map_arr_codegen(context, builder, sig, args):
    data_arr, = args
    yscxk__ydzg = context.make_helper(builder, sig.return_type)
    yscxk__ydzg.data = data_arr
    context.nrt.incref(builder, sig.args[0], data_arr)
    return yscxk__ydzg._getvalue()


@intrinsic
def init_map_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType) and isinstance(data_typ
        .dtype, StructArrayType)
    gglm__kpm = MapArrayType(data_typ.dtype.data[0], data_typ.dtype.data[1])
    return gglm__kpm(data_typ), init_map_arr_codegen


def alias_ext_init_map_arr(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_map_arr',
    'bodo.libs.map_arr_ext'] = alias_ext_init_map_arr


@numba.njit
def pre_alloc_map_array(num_maps, nested_counts, struct_typ):
    eght__wux = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        num_maps, nested_counts, struct_typ)
    return init_map_arr(eght__wux)


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
    ego__mryak = arr.key_arr_type, arr.value_arr_type
    if isinstance(ind, types.Integer):

        def map_arr_setitem_impl(arr, ind, val):
            xmts__stfm = val.keys()
            ojq__jyof = bodo.libs.struct_arr_ext.pre_alloc_struct_array(len
                (val), (-1,), ego__mryak, ('key', 'value'))
            for mdphy__pjvbd, lduo__wswr in enumerate(xmts__stfm):
                ojq__jyof[mdphy__pjvbd] = bodo.libs.struct_arr_ext.init_struct(
                    (lduo__wswr, val[lduo__wswr]), ('key', 'value'))
            arr._data[ind] = ojq__jyof
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
            hfg__lkzm = dict()
            tynz__qnoo = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            ojq__jyof = bodo.libs.array_item_arr_ext.get_data(arr._data)
            syawy__wized, erlqf__iwxg = bodo.libs.struct_arr_ext.get_data(
                ojq__jyof)
            dqf__vix = tynz__qnoo[ind]
            dvdyl__tcm = tynz__qnoo[ind + 1]
            for mdphy__pjvbd in range(dqf__vix, dvdyl__tcm):
                hfg__lkzm[syawy__wized[mdphy__pjvbd]] = erlqf__iwxg[
                    mdphy__pjvbd]
            return hfg__lkzm
        return map_arr_getitem_impl
    raise BodoError(
        'operator.getitem with MapArrays is only supported with an integer index.'
        )
