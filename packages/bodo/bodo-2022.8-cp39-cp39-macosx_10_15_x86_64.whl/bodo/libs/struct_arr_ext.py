"""Array implementation for structs of values.
Corresponds to Spark's StructType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Struct arrays: https://arrow.apache.org/docs/format/Columnar.html

The values are stored in contiguous data arrays; one array per field. For example:
A:             ["AA", "B", "C"]
B:             [1, 2, 4]
"""
import operator
import llvmlite.binding as ll
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import NativeValue, box, intrinsic, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
from numba.typed.typedobjectutils import _cast
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.time_ext import TimeType
from bodo.libs import array_ext
from bodo.utils.cg_helpers import gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit, to_arr_obj_if_list_obj
from bodo.utils.typing import BodoError, dtype_to_array_type, get_overload_const_int, get_overload_const_str, is_list_like_index_type, is_overload_constant_int, is_overload_constant_str, is_overload_none
ll.add_symbol('struct_array_from_sequence', array_ext.
    struct_array_from_sequence)
ll.add_symbol('np_array_from_struct_array', array_ext.
    np_array_from_struct_array)


class StructArrayType(types.ArrayCompatible):

    def __init__(self, data, names=None):
        assert isinstance(data, tuple) and len(data) > 0 and all(bodo.utils
            .utils.is_array_typ(ydnr__uycv, False) for ydnr__uycv in data)
        if names is not None:
            assert isinstance(names, tuple) and all(isinstance(ydnr__uycv,
                str) for ydnr__uycv in names) and len(names) == len(data)
        else:
            names = tuple('f{}'.format(i) for i in range(len(data)))
        self.data = data
        self.names = names
        super(StructArrayType, self).__init__(name=
            'StructArrayType({}, {})'.format(data, names))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return StructType(tuple(sdhin__pwjs.dtype for sdhin__pwjs in self.
            data), self.names)

    @classmethod
    def from_dict(cls, d):
        assert isinstance(d, dict)
        names = tuple(str(ydnr__uycv) for ydnr__uycv in d.keys())
        data = tuple(dtype_to_array_type(sdhin__pwjs) for sdhin__pwjs in d.
            values())
        return StructArrayType(data, names)

    def copy(self):
        return StructArrayType(self.data, self.names)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class StructArrayPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple) and all(bodo.utils.utils.
            is_array_typ(ydnr__uycv, False) for ydnr__uycv in data)
        self.data = data
        super(StructArrayPayloadType, self).__init__(name=
            'StructArrayPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructArrayPayloadType)
class StructArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        msw__ibb = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, msw__ibb)


@register_model(StructArrayType)
class StructArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructArrayPayloadType(fe_type.data)
        msw__ibb = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, msw__ibb)


def define_struct_arr_dtor(context, builder, struct_arr_type, payload_type):
    uyotc__slcrx = builder.module
    xoj__hiog = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    twd__yvqzf = cgutils.get_or_insert_function(uyotc__slcrx, xoj__hiog,
        name='.dtor.struct_arr.{}.{}.'.format(struct_arr_type.data,
        struct_arr_type.names))
    if not twd__yvqzf.is_declaration:
        return twd__yvqzf
    twd__yvqzf.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(twd__yvqzf.append_basic_block())
    pwjzo__hfe = twd__yvqzf.args[0]
    npuxc__jhcx = context.get_value_type(payload_type).as_pointer()
    flzxl__uqaw = builder.bitcast(pwjzo__hfe, npuxc__jhcx)
    xhfr__odhoy = context.make_helper(builder, payload_type, ref=flzxl__uqaw)
    context.nrt.decref(builder, types.BaseTuple.from_types(struct_arr_type.
        data), xhfr__odhoy.data)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        xhfr__odhoy.null_bitmap)
    builder.ret_void()
    return twd__yvqzf


def construct_struct_array(context, builder, struct_arr_type, n_structs,
    n_elems, c=None):
    payload_type = StructArrayPayloadType(struct_arr_type.data)
    zxa__awjj = context.get_value_type(payload_type)
    pcu__skgr = context.get_abi_sizeof(zxa__awjj)
    akcah__ubz = define_struct_arr_dtor(context, builder, struct_arr_type,
        payload_type)
    pvxuh__wjk = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, pcu__skgr), akcah__ubz)
    bttl__rkknc = context.nrt.meminfo_data(builder, pvxuh__wjk)
    wql__ifyfz = builder.bitcast(bttl__rkknc, zxa__awjj.as_pointer())
    xhfr__odhoy = cgutils.create_struct_proxy(payload_type)(context, builder)
    arrs = []
    utnqu__dcal = 0
    for arr_typ in struct_arr_type.data:
        uxcnq__ppii = bodo.utils.transform.get_type_alloc_counts(arr_typ.dtype)
        gbdd__zedi = cgutils.pack_array(builder, [n_structs] + [builder.
            extract_value(n_elems, i) for i in range(utnqu__dcal, 
            utnqu__dcal + uxcnq__ppii)])
        arr = gen_allocate_array(context, builder, arr_typ, gbdd__zedi, c)
        arrs.append(arr)
        utnqu__dcal += uxcnq__ppii
    xhfr__odhoy.data = cgutils.pack_array(builder, arrs
        ) if types.is_homogeneous(*struct_arr_type.data
        ) else cgutils.pack_struct(builder, arrs)
    emsnb__swwb = builder.udiv(builder.add(n_structs, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    afid__eqkrh = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [emsnb__swwb])
    null_bitmap_ptr = afid__eqkrh.data
    xhfr__odhoy.null_bitmap = afid__eqkrh._getvalue()
    builder.store(xhfr__odhoy._getvalue(), wql__ifyfz)
    return pvxuh__wjk, xhfr__odhoy.data, null_bitmap_ptr


def _get_C_API_ptrs(c, data_tup, data_typ, names):
    acyqi__rprfs = []
    assert len(data_typ) > 0
    for i, arr_typ in enumerate(data_typ):
        wikz__mdg = c.builder.extract_value(data_tup, i)
        arr = c.context.make_array(arr_typ)(c.context, c.builder, value=
            wikz__mdg)
        acyqi__rprfs.append(arr.data)
    ktjm__iljun = cgutils.pack_array(c.builder, acyqi__rprfs
        ) if types.is_homogeneous(*data_typ) else cgutils.pack_struct(c.
        builder, acyqi__rprfs)
    rrdu__ieyu = cgutils.alloca_once_value(c.builder, ktjm__iljun)
    fif__ticgr = [c.context.get_constant(types.int32, bodo.utils.utils.
        numba_to_c_type(ydnr__uycv.dtype)) for ydnr__uycv in data_typ]
    bvk__kmmj = cgutils.alloca_once_value(c.builder, cgutils.pack_array(c.
        builder, fif__ticgr))
    pzk__bvxm = cgutils.pack_array(c.builder, [c.context.
        insert_const_string(c.builder.module, ydnr__uycv) for ydnr__uycv in
        names])
    vzed__acls = cgutils.alloca_once_value(c.builder, pzk__bvxm)
    return rrdu__ieyu, bvk__kmmj, vzed__acls


@unbox(StructArrayType)
def unbox_struct_array(typ, val, c, is_tuple_array=False):
    from bodo.libs.tuple_arr_ext import TupleArrayType
    n_structs = bodo.utils.utils.object_length(c, val)
    frevt__jmr = all(isinstance(sdhin__pwjs, types.Array) and (sdhin__pwjs.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) or isinstance(sdhin__pwjs.dtype, TimeType)) for
        sdhin__pwjs in typ.data)
    if frevt__jmr:
        n_elems = cgutils.pack_array(c.builder, [], lir.IntType(64))
    else:
        mti__zqmn = get_array_elem_counts(c, c.builder, c.context, val, 
            TupleArrayType(typ.data) if is_tuple_array else typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            mti__zqmn, i) for i in range(1, mti__zqmn.type.count)], lir.
            IntType(64))
    pvxuh__wjk, data_tup, null_bitmap_ptr = construct_struct_array(c.
        context, c.builder, typ, n_structs, n_elems, c)
    if frevt__jmr:
        rrdu__ieyu, bvk__kmmj, vzed__acls = _get_C_API_ptrs(c, data_tup,
            typ.data, typ.names)
        xoj__hiog = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1)])
        twd__yvqzf = cgutils.get_or_insert_function(c.builder.module,
            xoj__hiog, name='struct_array_from_sequence')
        c.builder.call(twd__yvqzf, [val, c.context.get_constant(types.int32,
            len(typ.data)), c.builder.bitcast(rrdu__ieyu, lir.IntType(8).
            as_pointer()), null_bitmap_ptr, c.builder.bitcast(bvk__kmmj,
            lir.IntType(8).as_pointer()), c.builder.bitcast(vzed__acls, lir
            .IntType(8).as_pointer()), c.context.get_constant(types.bool_,
            is_tuple_array)])
    else:
        _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
            null_bitmap_ptr, is_tuple_array)
    hct__znt = c.context.make_helper(c.builder, typ)
    hct__znt.meminfo = pvxuh__wjk
    wmr__fdh = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(hct__znt._getvalue(), is_error=wmr__fdh)


def _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    tehk__bdsy = context.insert_const_string(builder.module, 'pandas')
    fzpip__ote = c.pyapi.import_module_noblock(tehk__bdsy)
    mabg__app = c.pyapi.object_getattr_string(fzpip__ote, 'NA')
    with cgutils.for_range(builder, n_structs) as mwk__pkya:
        mxhdb__cidfv = mwk__pkya.index
        box__hgqt = seq_getitem(builder, context, val, mxhdb__cidfv)
        set_bitmap_bit(builder, null_bitmap_ptr, mxhdb__cidfv, 0)
        for ufwam__abf in range(len(typ.data)):
            arr_typ = typ.data[ufwam__abf]
            data_arr = builder.extract_value(data_tup, ufwam__abf)

            def set_na(data_arr, i):
                bodo.libs.array_kernels.setna(data_arr, i)
            sig = types.none(arr_typ, types.int64)
            gbfi__hndrp, kidt__jah = c.pyapi.call_jit_code(set_na, sig, [
                data_arr, mxhdb__cidfv])
        qqejh__nli = is_na_value(builder, context, box__hgqt, mabg__app)
        kqog__chxb = builder.icmp_unsigned('!=', qqejh__nli, lir.Constant(
            qqejh__nli.type, 1))
        with builder.if_then(kqog__chxb):
            set_bitmap_bit(builder, null_bitmap_ptr, mxhdb__cidfv, 1)
            for ufwam__abf in range(len(typ.data)):
                arr_typ = typ.data[ufwam__abf]
                if is_tuple_array:
                    gmn__hdh = c.pyapi.tuple_getitem(box__hgqt, ufwam__abf)
                else:
                    gmn__hdh = c.pyapi.dict_getitem_string(box__hgqt, typ.
                        names[ufwam__abf])
                qqejh__nli = is_na_value(builder, context, gmn__hdh, mabg__app)
                kqog__chxb = builder.icmp_unsigned('!=', qqejh__nli, lir.
                    Constant(qqejh__nli.type, 1))
                with builder.if_then(kqog__chxb):
                    gmn__hdh = to_arr_obj_if_list_obj(c, context, builder,
                        gmn__hdh, arr_typ.dtype)
                    field_val = c.pyapi.to_native_value(arr_typ.dtype, gmn__hdh
                        ).value
                    data_arr = builder.extract_value(data_tup, ufwam__abf)

                    def set_data(data_arr, i, field_val):
                        data_arr[i] = field_val
                    sig = types.none(arr_typ, types.int64, arr_typ.dtype)
                    gbfi__hndrp, kidt__jah = c.pyapi.call_jit_code(set_data,
                        sig, [data_arr, mxhdb__cidfv, field_val])
                    c.context.nrt.decref(builder, arr_typ.dtype, field_val)
        c.pyapi.decref(box__hgqt)
    c.pyapi.decref(fzpip__ote)
    c.pyapi.decref(mabg__app)


def _get_struct_arr_payload(context, builder, arr_typ, arr):
    hct__znt = context.make_helper(builder, arr_typ, arr)
    payload_type = StructArrayPayloadType(arr_typ.data)
    bttl__rkknc = context.nrt.meminfo_data(builder, hct__znt.meminfo)
    wql__ifyfz = builder.bitcast(bttl__rkknc, context.get_value_type(
        payload_type).as_pointer())
    xhfr__odhoy = cgutils.create_struct_proxy(payload_type)(context,
        builder, builder.load(wql__ifyfz))
    return xhfr__odhoy


@box(StructArrayType)
def box_struct_arr(typ, val, c, is_tuple_array=False):
    xhfr__odhoy = _get_struct_arr_payload(c.context, c.builder, typ, val)
    gbfi__hndrp, length = c.pyapi.call_jit_code(lambda A: len(A), types.
        int64(typ), [val])
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), xhfr__odhoy.null_bitmap).data
    frevt__jmr = all(isinstance(sdhin__pwjs, types.Array) and (sdhin__pwjs.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) or isinstance(sdhin__pwjs.dtype, TimeType)) for
        sdhin__pwjs in typ.data)
    if frevt__jmr:
        rrdu__ieyu, bvk__kmmj, vzed__acls = _get_C_API_ptrs(c, xhfr__odhoy.
            data, typ.data, typ.names)
        xoj__hiog = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        kozjj__ecn = cgutils.get_or_insert_function(c.builder.module,
            xoj__hiog, name='np_array_from_struct_array')
        arr = c.builder.call(kozjj__ecn, [length, c.context.get_constant(
            types.int32, len(typ.data)), c.builder.bitcast(rrdu__ieyu, lir.
            IntType(8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            bvk__kmmj, lir.IntType(8).as_pointer()), c.builder.bitcast(
            vzed__acls, lir.IntType(8).as_pointer()), c.context.
            get_constant(types.bool_, is_tuple_array)])
    else:
        arr = _box_struct_array_generic(typ, c, length, xhfr__odhoy.data,
            null_bitmap_ptr, is_tuple_array)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_struct_array_generic(typ, c, length, data_arrs_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    tehk__bdsy = context.insert_const_string(builder.module, 'numpy')
    rucqj__womlg = c.pyapi.import_module_noblock(tehk__bdsy)
    sug__pdez = c.pyapi.object_getattr_string(rucqj__womlg, 'object_')
    lccz__ohdux = c.pyapi.long_from_longlong(length)
    igfiw__esymu = c.pyapi.call_method(rucqj__womlg, 'ndarray', (
        lccz__ohdux, sug__pdez))
    cwvg__ofnd = c.pyapi.object_getattr_string(rucqj__womlg, 'nan')
    with cgutils.for_range(builder, length) as mwk__pkya:
        mxhdb__cidfv = mwk__pkya.index
        pyarray_setitem(builder, context, igfiw__esymu, mxhdb__cidfv,
            cwvg__ofnd)
        remdc__mnxp = get_bitmap_bit(builder, null_bitmap_ptr, mxhdb__cidfv)
        imerj__bcarg = builder.icmp_unsigned('!=', remdc__mnxp, lir.
            Constant(lir.IntType(8), 0))
        with builder.if_then(imerj__bcarg):
            if is_tuple_array:
                box__hgqt = c.pyapi.tuple_new(len(typ.data))
            else:
                box__hgqt = c.pyapi.dict_new(len(typ.data))
            for i, arr_typ in enumerate(typ.data):
                if is_tuple_array:
                    c.pyapi.incref(cwvg__ofnd)
                    c.pyapi.tuple_setitem(box__hgqt, i, cwvg__ofnd)
                else:
                    c.pyapi.dict_setitem_string(box__hgqt, typ.names[i],
                        cwvg__ofnd)
                data_arr = c.builder.extract_value(data_arrs_tup, i)
                gbfi__hndrp, elp__smo = c.pyapi.call_jit_code(lambda
                    data_arr, ind: not bodo.libs.array_kernels.isna(
                    data_arr, ind), types.bool_(arr_typ, types.int64), [
                    data_arr, mxhdb__cidfv])
                with builder.if_then(elp__smo):
                    gbfi__hndrp, field_val = c.pyapi.call_jit_code(lambda
                        data_arr, ind: data_arr[ind], arr_typ.dtype(arr_typ,
                        types.int64), [data_arr, mxhdb__cidfv])
                    brlw__tlmur = c.pyapi.from_native_value(arr_typ.dtype,
                        field_val, c.env_manager)
                    if is_tuple_array:
                        c.pyapi.tuple_setitem(box__hgqt, i, brlw__tlmur)
                    else:
                        c.pyapi.dict_setitem_string(box__hgqt, typ.names[i],
                            brlw__tlmur)
                        c.pyapi.decref(brlw__tlmur)
            pyarray_setitem(builder, context, igfiw__esymu, mxhdb__cidfv,
                box__hgqt)
            c.pyapi.decref(box__hgqt)
    c.pyapi.decref(rucqj__womlg)
    c.pyapi.decref(sug__pdez)
    c.pyapi.decref(lccz__ohdux)
    c.pyapi.decref(cwvg__ofnd)
    return igfiw__esymu


def _fix_nested_counts(nested_counts, struct_arr_type, nested_counts_type,
    builder):
    tzhes__vdm = bodo.utils.transform.get_type_alloc_counts(struct_arr_type
        ) - 1
    if tzhes__vdm == 0:
        return nested_counts
    if not isinstance(nested_counts_type, types.UniTuple):
        nested_counts = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), -1) for hbrwl__ycv in range(tzhes__vdm)])
    elif nested_counts_type.count < tzhes__vdm:
        nested_counts = cgutils.pack_array(builder, [builder.extract_value(
            nested_counts, i) for i in range(nested_counts_type.count)] + [
            lir.Constant(lir.IntType(64), -1) for hbrwl__ycv in range(
            tzhes__vdm - nested_counts_type.count)])
    return nested_counts


@intrinsic
def pre_alloc_struct_array(typingctx, num_structs_typ, nested_counts_typ,
    dtypes_typ, names_typ=None):
    assert isinstance(num_structs_typ, types.Integer) and isinstance(dtypes_typ
        , types.BaseTuple)
    if is_overload_none(names_typ):
        names = tuple(f'f{i}' for i in range(len(dtypes_typ)))
    else:
        names = tuple(get_overload_const_str(sdhin__pwjs) for sdhin__pwjs in
            names_typ.types)
    gsje__gutsi = tuple(sdhin__pwjs.instance_type for sdhin__pwjs in
        dtypes_typ.types)
    struct_arr_type = StructArrayType(gsje__gutsi, names)

    def codegen(context, builder, sig, args):
        aazg__tyox, nested_counts, hbrwl__ycv, hbrwl__ycv = args
        nested_counts_type = sig.args[1]
        nested_counts = _fix_nested_counts(nested_counts, struct_arr_type,
            nested_counts_type, builder)
        pvxuh__wjk, hbrwl__ycv, hbrwl__ycv = construct_struct_array(context,
            builder, struct_arr_type, aazg__tyox, nested_counts)
        hct__znt = context.make_helper(builder, struct_arr_type)
        hct__znt.meminfo = pvxuh__wjk
        return hct__znt._getvalue()
    return struct_arr_type(num_structs_typ, nested_counts_typ, dtypes_typ,
        names_typ), codegen


def pre_alloc_struct_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 4 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_struct_arr_ext_pre_alloc_struct_array
    ) = pre_alloc_struct_array_equiv


class StructType(types.Type):

    def __init__(self, data, names):
        assert isinstance(data, tuple) and len(data) > 0
        assert isinstance(names, tuple) and all(isinstance(ydnr__uycv, str) for
            ydnr__uycv in names) and len(names) == len(data)
        self.data = data
        self.names = names
        super(StructType, self).__init__(name='StructType({}, {})'.format(
            data, names))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class StructPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple)
        self.data = data
        super(StructPayloadType, self).__init__(name=
            'StructPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructPayloadType)
class StructPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        msw__ibb = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.UniTuple(types.int8, len(fe_type.data)))]
        models.StructModel.__init__(self, dmm, fe_type, msw__ibb)


@register_model(StructType)
class StructModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructPayloadType(fe_type.data)
        msw__ibb = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, msw__ibb)


def define_struct_dtor(context, builder, struct_type, payload_type):
    uyotc__slcrx = builder.module
    xoj__hiog = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    twd__yvqzf = cgutils.get_or_insert_function(uyotc__slcrx, xoj__hiog,
        name='.dtor.struct.{}.{}.'.format(struct_type.data, struct_type.names))
    if not twd__yvqzf.is_declaration:
        return twd__yvqzf
    twd__yvqzf.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(twd__yvqzf.append_basic_block())
    pwjzo__hfe = twd__yvqzf.args[0]
    npuxc__jhcx = context.get_value_type(payload_type).as_pointer()
    flzxl__uqaw = builder.bitcast(pwjzo__hfe, npuxc__jhcx)
    xhfr__odhoy = context.make_helper(builder, payload_type, ref=flzxl__uqaw)
    for i in range(len(struct_type.data)):
        asqy__ppiov = builder.extract_value(xhfr__odhoy.null_bitmap, i)
        imerj__bcarg = builder.icmp_unsigned('==', asqy__ppiov, lir.
            Constant(asqy__ppiov.type, 1))
        with builder.if_then(imerj__bcarg):
            val = builder.extract_value(xhfr__odhoy.data, i)
            context.nrt.decref(builder, struct_type.data[i], val)
    builder.ret_void()
    return twd__yvqzf


def _get_struct_payload(context, builder, typ, struct):
    struct = context.make_helper(builder, typ, struct)
    payload_type = StructPayloadType(typ.data)
    bttl__rkknc = context.nrt.meminfo_data(builder, struct.meminfo)
    wql__ifyfz = builder.bitcast(bttl__rkknc, context.get_value_type(
        payload_type).as_pointer())
    xhfr__odhoy = cgutils.create_struct_proxy(payload_type)(context,
        builder, builder.load(wql__ifyfz))
    return xhfr__odhoy, wql__ifyfz


@unbox(StructType)
def unbox_struct(typ, val, c):
    context = c.context
    builder = c.builder
    tehk__bdsy = context.insert_const_string(builder.module, 'pandas')
    fzpip__ote = c.pyapi.import_module_noblock(tehk__bdsy)
    mabg__app = c.pyapi.object_getattr_string(fzpip__ote, 'NA')
    jpei__ghlp = []
    nulls = []
    for i, sdhin__pwjs in enumerate(typ.data):
        brlw__tlmur = c.pyapi.dict_getitem_string(val, typ.names[i])
        nexp__gqvl = cgutils.alloca_once_value(c.builder, context.
            get_constant(types.uint8, 0))
        pth__bobg = cgutils.alloca_once_value(c.builder, cgutils.
            get_null_value(context.get_value_type(sdhin__pwjs)))
        qqejh__nli = is_na_value(builder, context, brlw__tlmur, mabg__app)
        imerj__bcarg = builder.icmp_unsigned('!=', qqejh__nli, lir.Constant
            (qqejh__nli.type, 1))
        with builder.if_then(imerj__bcarg):
            builder.store(context.get_constant(types.uint8, 1), nexp__gqvl)
            field_val = c.pyapi.to_native_value(sdhin__pwjs, brlw__tlmur).value
            builder.store(field_val, pth__bobg)
        jpei__ghlp.append(builder.load(pth__bobg))
        nulls.append(builder.load(nexp__gqvl))
    c.pyapi.decref(fzpip__ote)
    c.pyapi.decref(mabg__app)
    pvxuh__wjk = construct_struct(context, builder, typ, jpei__ghlp, nulls)
    struct = context.make_helper(builder, typ)
    struct.meminfo = pvxuh__wjk
    wmr__fdh = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(struct._getvalue(), is_error=wmr__fdh)


@box(StructType)
def box_struct(typ, val, c):
    upvs__tkt = c.pyapi.dict_new(len(typ.data))
    xhfr__odhoy, hbrwl__ycv = _get_struct_payload(c.context, c.builder, typ,
        val)
    assert len(typ.data) > 0
    for i, val_typ in enumerate(typ.data):
        c.pyapi.dict_setitem_string(upvs__tkt, typ.names[i], c.pyapi.
            borrow_none())
        asqy__ppiov = c.builder.extract_value(xhfr__odhoy.null_bitmap, i)
        imerj__bcarg = c.builder.icmp_unsigned('==', asqy__ppiov, lir.
            Constant(asqy__ppiov.type, 1))
        with c.builder.if_then(imerj__bcarg):
            zjiq__gwnpg = c.builder.extract_value(xhfr__odhoy.data, i)
            c.context.nrt.incref(c.builder, val_typ, zjiq__gwnpg)
            gmn__hdh = c.pyapi.from_native_value(val_typ, zjiq__gwnpg, c.
                env_manager)
            c.pyapi.dict_setitem_string(upvs__tkt, typ.names[i], gmn__hdh)
            c.pyapi.decref(gmn__hdh)
    c.context.nrt.decref(c.builder, typ, val)
    return upvs__tkt


@intrinsic
def init_struct(typingctx, data_typ, names_typ=None):
    names = tuple(get_overload_const_str(sdhin__pwjs) for sdhin__pwjs in
        names_typ.types)
    struct_type = StructType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, kmgj__bmfh = args
        payload_type = StructPayloadType(struct_type.data)
        zxa__awjj = context.get_value_type(payload_type)
        pcu__skgr = context.get_abi_sizeof(zxa__awjj)
        akcah__ubz = define_struct_dtor(context, builder, struct_type,
            payload_type)
        pvxuh__wjk = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, pcu__skgr), akcah__ubz)
        bttl__rkknc = context.nrt.meminfo_data(builder, pvxuh__wjk)
        wql__ifyfz = builder.bitcast(bttl__rkknc, zxa__awjj.as_pointer())
        xhfr__odhoy = cgutils.create_struct_proxy(payload_type)(context,
            builder)
        xhfr__odhoy.data = data
        xhfr__odhoy.null_bitmap = cgutils.pack_array(builder, [context.
            get_constant(types.uint8, 1) for hbrwl__ycv in range(len(
            data_typ.types))])
        builder.store(xhfr__odhoy._getvalue(), wql__ifyfz)
        context.nrt.incref(builder, data_typ, data)
        struct = context.make_helper(builder, struct_type)
        struct.meminfo = pvxuh__wjk
        return struct._getvalue()
    return struct_type(data_typ, names_typ), codegen


@intrinsic
def get_struct_data(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        xhfr__odhoy, hbrwl__ycv = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            xhfr__odhoy.data)
    return types.BaseTuple.from_types(struct_typ.data)(struct_typ), codegen


@intrinsic
def get_struct_null_bitmap(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        xhfr__odhoy, hbrwl__ycv = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            xhfr__odhoy.null_bitmap)
    lzrr__zxugp = types.UniTuple(types.int8, len(struct_typ.data))
    return lzrr__zxugp(struct_typ), codegen


@intrinsic
def set_struct_data(typingctx, struct_typ, field_ind_typ, val_typ=None):
    assert isinstance(struct_typ, StructType) and is_overload_constant_int(
        field_ind_typ)
    field_ind = get_overload_const_int(field_ind_typ)

    def codegen(context, builder, sig, args):
        struct, hbrwl__ycv, val = args
        xhfr__odhoy, wql__ifyfz = _get_struct_payload(context, builder,
            struct_typ, struct)
        eibqy__ifl = xhfr__odhoy.data
        ynx__rzmxw = builder.insert_value(eibqy__ifl, val, field_ind)
        ughvn__nnpef = types.BaseTuple.from_types(struct_typ.data)
        context.nrt.decref(builder, ughvn__nnpef, eibqy__ifl)
        context.nrt.incref(builder, ughvn__nnpef, ynx__rzmxw)
        xhfr__odhoy.data = ynx__rzmxw
        builder.store(xhfr__odhoy._getvalue(), wql__ifyfz)
        return context.get_dummy_value()
    return types.none(struct_typ, field_ind_typ, val_typ), codegen


def _get_struct_field_ind(struct, ind, op):
    if not is_overload_constant_str(ind):
        raise BodoError(
            'structs (from struct array) only support constant strings for {}, not {}'
            .format(op, ind))
    jar__ter = get_overload_const_str(ind)
    if jar__ter not in struct.names:
        raise BodoError('Field {} does not exist in struct {}'.format(
            jar__ter, struct))
    return struct.names.index(jar__ter)


def is_field_value_null(s, field_name):
    pass


@overload(is_field_value_null, no_unliteral=True)
def overload_is_field_value_null(s, field_name):
    field_ind = _get_struct_field_ind(s, field_name, 'element access (getitem)'
        )
    return lambda s, field_name: get_struct_null_bitmap(s)[field_ind] == 0


@overload(operator.getitem, no_unliteral=True)
def struct_getitem(struct, ind):
    if not isinstance(struct, StructType):
        return
    field_ind = _get_struct_field_ind(struct, ind, 'element access (getitem)')
    return lambda struct, ind: get_struct_data(struct)[field_ind]


@overload(operator.setitem, no_unliteral=True)
def struct_setitem(struct, ind, val):
    if not isinstance(struct, StructType):
        return
    field_ind = _get_struct_field_ind(struct, ind, 'item assignment (setitem)')
    field_typ = struct.data[field_ind]
    return lambda struct, ind, val: set_struct_data(struct, field_ind,
        _cast(val, field_typ))


@overload(len, no_unliteral=True)
def overload_struct_arr_len(struct):
    if isinstance(struct, StructType):
        num_fields = len(struct.data)
        return lambda struct: num_fields


def construct_struct(context, builder, struct_type, values, nulls):
    payload_type = StructPayloadType(struct_type.data)
    zxa__awjj = context.get_value_type(payload_type)
    pcu__skgr = context.get_abi_sizeof(zxa__awjj)
    akcah__ubz = define_struct_dtor(context, builder, struct_type, payload_type
        )
    pvxuh__wjk = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, pcu__skgr), akcah__ubz)
    bttl__rkknc = context.nrt.meminfo_data(builder, pvxuh__wjk)
    wql__ifyfz = builder.bitcast(bttl__rkknc, zxa__awjj.as_pointer())
    xhfr__odhoy = cgutils.create_struct_proxy(payload_type)(context, builder)
    xhfr__odhoy.data = cgutils.pack_array(builder, values
        ) if types.is_homogeneous(*struct_type.data) else cgutils.pack_struct(
        builder, values)
    xhfr__odhoy.null_bitmap = cgutils.pack_array(builder, nulls)
    builder.store(xhfr__odhoy._getvalue(), wql__ifyfz)
    return pvxuh__wjk


@intrinsic
def struct_array_get_struct(typingctx, struct_arr_typ, ind_typ=None):
    assert isinstance(struct_arr_typ, StructArrayType) and isinstance(ind_typ,
        types.Integer)
    bho__gfdi = tuple(d.dtype for d in struct_arr_typ.data)
    hwcy__xuwh = StructType(bho__gfdi, struct_arr_typ.names)

    def codegen(context, builder, sig, args):
        tsz__bdcc, ind = args
        xhfr__odhoy = _get_struct_arr_payload(context, builder,
            struct_arr_typ, tsz__bdcc)
        jpei__ghlp = []
        gbov__leukr = []
        for i, arr_typ in enumerate(struct_arr_typ.data):
            wikz__mdg = builder.extract_value(xhfr__odhoy.data, i)
            gkdt__ram = context.compile_internal(builder, lambda arr, ind: 
                np.uint8(0) if bodo.libs.array_kernels.isna(arr, ind) else
                np.uint8(1), types.uint8(arr_typ, types.int64), [wikz__mdg,
                ind])
            gbov__leukr.append(gkdt__ram)
            vjhz__gzi = cgutils.alloca_once_value(builder, context.
                get_constant_null(arr_typ.dtype))
            imerj__bcarg = builder.icmp_unsigned('==', gkdt__ram, lir.
                Constant(gkdt__ram.type, 1))
            with builder.if_then(imerj__bcarg):
                omygv__rlof = context.compile_internal(builder, lambda arr,
                    ind: arr[ind], arr_typ.dtype(arr_typ, types.int64), [
                    wikz__mdg, ind])
                builder.store(omygv__rlof, vjhz__gzi)
            jpei__ghlp.append(builder.load(vjhz__gzi))
        if isinstance(hwcy__xuwh, types.DictType):
            gwrks__xtwfv = [context.insert_const_string(builder.module,
                exop__zdlnw) for exop__zdlnw in struct_arr_typ.names]
            rac__ccg = cgutils.pack_array(builder, jpei__ghlp)
            ncyz__lzoqy = cgutils.pack_array(builder, gwrks__xtwfv)

            def impl(names, vals):
                d = {}
                for i, exop__zdlnw in enumerate(names):
                    d[exop__zdlnw] = vals[i]
                return d
            ztgf__nfkgb = context.compile_internal(builder, impl,
                hwcy__xuwh(types.Tuple(tuple(types.StringLiteral(
                exop__zdlnw) for exop__zdlnw in struct_arr_typ.names)),
                types.Tuple(bho__gfdi)), [ncyz__lzoqy, rac__ccg])
            context.nrt.decref(builder, types.BaseTuple.from_types(
                bho__gfdi), rac__ccg)
            return ztgf__nfkgb
        pvxuh__wjk = construct_struct(context, builder, hwcy__xuwh,
            jpei__ghlp, gbov__leukr)
        struct = context.make_helper(builder, hwcy__xuwh)
        struct.meminfo = pvxuh__wjk
        return struct._getvalue()
    return hwcy__xuwh(struct_arr_typ, ind_typ), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        xhfr__odhoy = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            xhfr__odhoy.data)
    return types.BaseTuple.from_types(arr_typ.data)(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        xhfr__odhoy = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            xhfr__odhoy.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


@intrinsic
def init_struct_arr(typingctx, data_typ, null_bitmap_typ, names_typ=None):
    names = tuple(get_overload_const_str(sdhin__pwjs) for sdhin__pwjs in
        names_typ.types)
    struct_arr_type = StructArrayType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, afid__eqkrh, kmgj__bmfh = args
        payload_type = StructArrayPayloadType(struct_arr_type.data)
        zxa__awjj = context.get_value_type(payload_type)
        pcu__skgr = context.get_abi_sizeof(zxa__awjj)
        akcah__ubz = define_struct_arr_dtor(context, builder,
            struct_arr_type, payload_type)
        pvxuh__wjk = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, pcu__skgr), akcah__ubz)
        bttl__rkknc = context.nrt.meminfo_data(builder, pvxuh__wjk)
        wql__ifyfz = builder.bitcast(bttl__rkknc, zxa__awjj.as_pointer())
        xhfr__odhoy = cgutils.create_struct_proxy(payload_type)(context,
            builder)
        xhfr__odhoy.data = data
        xhfr__odhoy.null_bitmap = afid__eqkrh
        builder.store(xhfr__odhoy._getvalue(), wql__ifyfz)
        context.nrt.incref(builder, data_typ, data)
        context.nrt.incref(builder, null_bitmap_typ, afid__eqkrh)
        hct__znt = context.make_helper(builder, struct_arr_type)
        hct__znt.meminfo = pvxuh__wjk
        return hct__znt._getvalue()
    return struct_arr_type(data_typ, null_bitmap_typ, names_typ), codegen


@overload(operator.getitem, no_unliteral=True)
def struct_arr_getitem(arr, ind):
    if not isinstance(arr, StructArrayType):
        return
    if isinstance(ind, types.Integer):

        def struct_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            return struct_array_get_struct(arr, ind)
        return struct_arr_getitem_impl
    hsay__ctlqn = len(arr.data)
    vkw__onna = 'def impl(arr, ind):\n'
    vkw__onna += '  data = get_data(arr)\n'
    vkw__onna += '  null_bitmap = get_null_bitmap(arr)\n'
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        vkw__onna += """  out_null_bitmap = get_new_null_mask_bool_index(null_bitmap, ind, len(data[0]))
"""
    elif is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        vkw__onna += """  out_null_bitmap = get_new_null_mask_int_index(null_bitmap, ind, len(data[0]))
"""
    elif isinstance(ind, types.SliceType):
        vkw__onna += """  out_null_bitmap = get_new_null_mask_slice_index(null_bitmap, ind, len(data[0]))
"""
    else:
        raise BodoError('invalid index {} in struct array indexing'.format(ind)
            )
    vkw__onna += ('  return init_struct_arr(({},), out_null_bitmap, ({},))\n'
        .format(', '.join('ensure_contig_if_np(data[{}][ind])'.format(i) for
        i in range(hsay__ctlqn)), ', '.join("'{}'".format(exop__zdlnw) for
        exop__zdlnw in arr.names)))
    shb__yget = {}
    exec(vkw__onna, {'init_struct_arr': init_struct_arr, 'get_data':
        get_data, 'get_null_bitmap': get_null_bitmap, 'ensure_contig_if_np':
        bodo.utils.conversion.ensure_contig_if_np,
        'get_new_null_mask_bool_index': bodo.utils.indexing.
        get_new_null_mask_bool_index, 'get_new_null_mask_int_index': bodo.
        utils.indexing.get_new_null_mask_int_index,
        'get_new_null_mask_slice_index': bodo.utils.indexing.
        get_new_null_mask_slice_index}, shb__yget)
    impl = shb__yget['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def struct_arr_setitem(arr, ind, val):
    if not isinstance(arr, StructArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        hsay__ctlqn = len(arr.data)
        vkw__onna = 'def impl(arr, ind, val):\n'
        vkw__onna += '  data = get_data(arr)\n'
        vkw__onna += '  null_bitmap = get_null_bitmap(arr)\n'
        vkw__onna += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for i in range(hsay__ctlqn):
            if isinstance(val, StructType):
                vkw__onna += "  if is_field_value_null(val, '{}'):\n".format(
                    arr.names[i])
                vkw__onna += (
                    '    bodo.libs.array_kernels.setna(data[{}], ind)\n'.
                    format(i))
                vkw__onna += '  else:\n'
                vkw__onna += "    data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
            else:
                vkw__onna += "  data[{}][ind] = val['{}']\n".format(i, arr.
                    names[i])
        shb__yget = {}
        exec(vkw__onna, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'is_field_value_null':
            is_field_value_null}, shb__yget)
        impl = shb__yget['impl']
        return impl
    if isinstance(ind, types.SliceType):
        hsay__ctlqn = len(arr.data)
        vkw__onna = 'def impl(arr, ind, val):\n'
        vkw__onna += '  data = get_data(arr)\n'
        vkw__onna += '  null_bitmap = get_null_bitmap(arr)\n'
        vkw__onna += '  val_data = get_data(val)\n'
        vkw__onna += '  val_null_bitmap = get_null_bitmap(val)\n'
        vkw__onna += """  setitem_slice_index_null_bits(null_bitmap, val_null_bitmap, ind, len(arr))
"""
        for i in range(hsay__ctlqn):
            vkw__onna += '  data[{0}][ind] = val_data[{0}]\n'.format(i)
        shb__yget = {}
        exec(vkw__onna, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'setitem_slice_index_null_bits':
            bodo.utils.indexing.setitem_slice_index_null_bits}, shb__yget)
        impl = shb__yget['impl']
        return impl
    raise BodoError(
        'only setitem with scalar/slice index is currently supported for struct arrays'
        )


@overload(len, no_unliteral=True)
def overload_struct_arr_len(A):
    if isinstance(A, StructArrayType):
        return lambda A: len(get_data(A)[0])


@overload_attribute(StructArrayType, 'shape')
def overload_struct_arr_shape(A):
    return lambda A: (len(get_data(A)[0]),)


@overload_attribute(StructArrayType, 'dtype')
def overload_struct_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(StructArrayType, 'ndim')
def overload_struct_arr_ndim(A):
    return lambda A: 1


@overload_attribute(StructArrayType, 'nbytes')
def overload_struct_arr_nbytes(A):
    vkw__onna = 'def impl(A):\n'
    vkw__onna += '  total_nbytes = 0\n'
    vkw__onna += '  data = get_data(A)\n'
    for i in range(len(A.data)):
        vkw__onna += f'  total_nbytes += data[{i}].nbytes\n'
    vkw__onna += '  total_nbytes += get_null_bitmap(A).nbytes\n'
    vkw__onna += '  return total_nbytes\n'
    shb__yget = {}
    exec(vkw__onna, {'get_data': get_data, 'get_null_bitmap':
        get_null_bitmap}, shb__yget)
    impl = shb__yget['impl']
    return impl


@overload_method(StructArrayType, 'copy', no_unliteral=True)
def overload_struct_arr_copy(A):
    names = A.names

    def copy_impl(A):
        data = get_data(A)
        afid__eqkrh = get_null_bitmap(A)
        ooo__cooo = bodo.libs.struct_arr_ext.copy_arr_tup(data)
        epv__lnsi = afid__eqkrh.copy()
        return init_struct_arr(ooo__cooo, epv__lnsi, names)
    return copy_impl


def copy_arr_tup(arrs):
    return tuple(ydnr__uycv.copy() for ydnr__uycv in arrs)


@overload(copy_arr_tup, no_unliteral=True)
def copy_arr_tup_overload(arrs):
    plrxd__mvdn = arrs.count
    vkw__onna = 'def f(arrs):\n'
    vkw__onna += '  return ({},)\n'.format(','.join('arrs[{}].copy()'.
        format(i) for i in range(plrxd__mvdn)))
    shb__yget = {}
    exec(vkw__onna, {}, shb__yget)
    impl = shb__yget['f']
    return impl
