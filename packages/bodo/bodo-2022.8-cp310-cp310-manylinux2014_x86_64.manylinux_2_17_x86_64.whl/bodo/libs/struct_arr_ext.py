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
            .utils.is_array_typ(rcxk__evmdo, False) for rcxk__evmdo in data)
        if names is not None:
            assert isinstance(names, tuple) and all(isinstance(rcxk__evmdo,
                str) for rcxk__evmdo in names) and len(names) == len(data)
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
        return StructType(tuple(mxu__rvrv.dtype for mxu__rvrv in self.data),
            self.names)

    @classmethod
    def from_dict(cls, d):
        assert isinstance(d, dict)
        names = tuple(str(rcxk__evmdo) for rcxk__evmdo in d.keys())
        data = tuple(dtype_to_array_type(mxu__rvrv) for mxu__rvrv in d.values()
            )
        return StructArrayType(data, names)

    def copy(self):
        return StructArrayType(self.data, self.names)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class StructArrayPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple) and all(bodo.utils.utils.
            is_array_typ(rcxk__evmdo, False) for rcxk__evmdo in data)
        self.data = data
        super(StructArrayPayloadType, self).__init__(name=
            'StructArrayPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructArrayPayloadType)
class StructArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yme__dzy = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, yme__dzy)


@register_model(StructArrayType)
class StructArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructArrayPayloadType(fe_type.data)
        yme__dzy = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, yme__dzy)


def define_struct_arr_dtor(context, builder, struct_arr_type, payload_type):
    zro__auq = builder.module
    xgy__qvs = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    zlyzc__vsoeo = cgutils.get_or_insert_function(zro__auq, xgy__qvs, name=
        '.dtor.struct_arr.{}.{}.'.format(struct_arr_type.data,
        struct_arr_type.names))
    if not zlyzc__vsoeo.is_declaration:
        return zlyzc__vsoeo
    zlyzc__vsoeo.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(zlyzc__vsoeo.append_basic_block())
    cwtjv__lna = zlyzc__vsoeo.args[0]
    miyv__hoyqm = context.get_value_type(payload_type).as_pointer()
    gzpwc__ztnj = builder.bitcast(cwtjv__lna, miyv__hoyqm)
    tty__urnye = context.make_helper(builder, payload_type, ref=gzpwc__ztnj)
    context.nrt.decref(builder, types.BaseTuple.from_types(struct_arr_type.
        data), tty__urnye.data)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        tty__urnye.null_bitmap)
    builder.ret_void()
    return zlyzc__vsoeo


def construct_struct_array(context, builder, struct_arr_type, n_structs,
    n_elems, c=None):
    payload_type = StructArrayPayloadType(struct_arr_type.data)
    uawg__vwxvd = context.get_value_type(payload_type)
    ihhd__rvle = context.get_abi_sizeof(uawg__vwxvd)
    ungvi__hsrv = define_struct_arr_dtor(context, builder, struct_arr_type,
        payload_type)
    vexo__whgzb = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, ihhd__rvle), ungvi__hsrv)
    trn__wlf = context.nrt.meminfo_data(builder, vexo__whgzb)
    tgfw__ohjcv = builder.bitcast(trn__wlf, uawg__vwxvd.as_pointer())
    tty__urnye = cgutils.create_struct_proxy(payload_type)(context, builder)
    arrs = []
    sfxi__bjokm = 0
    for arr_typ in struct_arr_type.data:
        rztga__fzka = bodo.utils.transform.get_type_alloc_counts(arr_typ.dtype)
        xogvj__aeef = cgutils.pack_array(builder, [n_structs] + [builder.
            extract_value(n_elems, i) for i in range(sfxi__bjokm, 
            sfxi__bjokm + rztga__fzka)])
        arr = gen_allocate_array(context, builder, arr_typ, xogvj__aeef, c)
        arrs.append(arr)
        sfxi__bjokm += rztga__fzka
    tty__urnye.data = cgutils.pack_array(builder, arrs
        ) if types.is_homogeneous(*struct_arr_type.data
        ) else cgutils.pack_struct(builder, arrs)
    yze__payl = builder.udiv(builder.add(n_structs, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    vefwm__ycxbf = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [yze__payl])
    null_bitmap_ptr = vefwm__ycxbf.data
    tty__urnye.null_bitmap = vefwm__ycxbf._getvalue()
    builder.store(tty__urnye._getvalue(), tgfw__ohjcv)
    return vexo__whgzb, tty__urnye.data, null_bitmap_ptr


def _get_C_API_ptrs(c, data_tup, data_typ, names):
    bozl__nylwt = []
    assert len(data_typ) > 0
    for i, arr_typ in enumerate(data_typ):
        uyttb__cap = c.builder.extract_value(data_tup, i)
        arr = c.context.make_array(arr_typ)(c.context, c.builder, value=
            uyttb__cap)
        bozl__nylwt.append(arr.data)
    qfcv__rvvbt = cgutils.pack_array(c.builder, bozl__nylwt
        ) if types.is_homogeneous(*data_typ) else cgutils.pack_struct(c.
        builder, bozl__nylwt)
    ddusd__evx = cgutils.alloca_once_value(c.builder, qfcv__rvvbt)
    lta__rggtx = [c.context.get_constant(types.int32, bodo.utils.utils.
        numba_to_c_type(rcxk__evmdo.dtype)) for rcxk__evmdo in data_typ]
    nylbr__bnih = cgutils.alloca_once_value(c.builder, cgutils.pack_array(c
        .builder, lta__rggtx))
    sfn__deh = cgutils.pack_array(c.builder, [c.context.insert_const_string
        (c.builder.module, rcxk__evmdo) for rcxk__evmdo in names])
    klfs__hvaz = cgutils.alloca_once_value(c.builder, sfn__deh)
    return ddusd__evx, nylbr__bnih, klfs__hvaz


@unbox(StructArrayType)
def unbox_struct_array(typ, val, c, is_tuple_array=False):
    from bodo.libs.tuple_arr_ext import TupleArrayType
    n_structs = bodo.utils.utils.object_length(c, val)
    jzh__yqs = all(isinstance(mxu__rvrv, types.Array) and (mxu__rvrv.dtype in
        (types.int64, types.float64, types.bool_, datetime_date_type) or
        isinstance(mxu__rvrv.dtype, TimeType)) for mxu__rvrv in typ.data)
    if jzh__yqs:
        n_elems = cgutils.pack_array(c.builder, [], lir.IntType(64))
    else:
        jqi__uxve = get_array_elem_counts(c, c.builder, c.context, val, 
            TupleArrayType(typ.data) if is_tuple_array else typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            jqi__uxve, i) for i in range(1, jqi__uxve.type.count)], lir.
            IntType(64))
    vexo__whgzb, data_tup, null_bitmap_ptr = construct_struct_array(c.
        context, c.builder, typ, n_structs, n_elems, c)
    if jzh__yqs:
        ddusd__evx, nylbr__bnih, klfs__hvaz = _get_C_API_ptrs(c, data_tup,
            typ.data, typ.names)
        xgy__qvs = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1)])
        zlyzc__vsoeo = cgutils.get_or_insert_function(c.builder.module,
            xgy__qvs, name='struct_array_from_sequence')
        c.builder.call(zlyzc__vsoeo, [val, c.context.get_constant(types.
            int32, len(typ.data)), c.builder.bitcast(ddusd__evx, lir.
            IntType(8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            nylbr__bnih, lir.IntType(8).as_pointer()), c.builder.bitcast(
            klfs__hvaz, lir.IntType(8).as_pointer()), c.context.
            get_constant(types.bool_, is_tuple_array)])
    else:
        _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
            null_bitmap_ptr, is_tuple_array)
    dka__hrcno = c.context.make_helper(c.builder, typ)
    dka__hrcno.meminfo = vexo__whgzb
    vvgk__nifhn = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(dka__hrcno._getvalue(), is_error=vvgk__nifhn)


def _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    lcpi__ezin = context.insert_const_string(builder.module, 'pandas')
    pjhs__jhws = c.pyapi.import_module_noblock(lcpi__ezin)
    ckq__ofb = c.pyapi.object_getattr_string(pjhs__jhws, 'NA')
    with cgutils.for_range(builder, n_structs) as gwise__crv:
        aboj__oyl = gwise__crv.index
        elppx__jbz = seq_getitem(builder, context, val, aboj__oyl)
        set_bitmap_bit(builder, null_bitmap_ptr, aboj__oyl, 0)
        for xynlr__alt in range(len(typ.data)):
            arr_typ = typ.data[xynlr__alt]
            data_arr = builder.extract_value(data_tup, xynlr__alt)

            def set_na(data_arr, i):
                bodo.libs.array_kernels.setna(data_arr, i)
            sig = types.none(arr_typ, types.int64)
            nqsdn__ttm, fyyn__dyuxz = c.pyapi.call_jit_code(set_na, sig, [
                data_arr, aboj__oyl])
        msqb__xgp = is_na_value(builder, context, elppx__jbz, ckq__ofb)
        hdsq__ednf = builder.icmp_unsigned('!=', msqb__xgp, lir.Constant(
            msqb__xgp.type, 1))
        with builder.if_then(hdsq__ednf):
            set_bitmap_bit(builder, null_bitmap_ptr, aboj__oyl, 1)
            for xynlr__alt in range(len(typ.data)):
                arr_typ = typ.data[xynlr__alt]
                if is_tuple_array:
                    ezntv__fcrif = c.pyapi.tuple_getitem(elppx__jbz, xynlr__alt
                        )
                else:
                    ezntv__fcrif = c.pyapi.dict_getitem_string(elppx__jbz,
                        typ.names[xynlr__alt])
                msqb__xgp = is_na_value(builder, context, ezntv__fcrif,
                    ckq__ofb)
                hdsq__ednf = builder.icmp_unsigned('!=', msqb__xgp, lir.
                    Constant(msqb__xgp.type, 1))
                with builder.if_then(hdsq__ednf):
                    ezntv__fcrif = to_arr_obj_if_list_obj(c, context,
                        builder, ezntv__fcrif, arr_typ.dtype)
                    field_val = c.pyapi.to_native_value(arr_typ.dtype,
                        ezntv__fcrif).value
                    data_arr = builder.extract_value(data_tup, xynlr__alt)

                    def set_data(data_arr, i, field_val):
                        data_arr[i] = field_val
                    sig = types.none(arr_typ, types.int64, arr_typ.dtype)
                    nqsdn__ttm, fyyn__dyuxz = c.pyapi.call_jit_code(set_data,
                        sig, [data_arr, aboj__oyl, field_val])
                    c.context.nrt.decref(builder, arr_typ.dtype, field_val)
        c.pyapi.decref(elppx__jbz)
    c.pyapi.decref(pjhs__jhws)
    c.pyapi.decref(ckq__ofb)


def _get_struct_arr_payload(context, builder, arr_typ, arr):
    dka__hrcno = context.make_helper(builder, arr_typ, arr)
    payload_type = StructArrayPayloadType(arr_typ.data)
    trn__wlf = context.nrt.meminfo_data(builder, dka__hrcno.meminfo)
    tgfw__ohjcv = builder.bitcast(trn__wlf, context.get_value_type(
        payload_type).as_pointer())
    tty__urnye = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(tgfw__ohjcv))
    return tty__urnye


@box(StructArrayType)
def box_struct_arr(typ, val, c, is_tuple_array=False):
    tty__urnye = _get_struct_arr_payload(c.context, c.builder, typ, val)
    nqsdn__ttm, length = c.pyapi.call_jit_code(lambda A: len(A), types.
        int64(typ), [val])
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), tty__urnye.null_bitmap).data
    jzh__yqs = all(isinstance(mxu__rvrv, types.Array) and (mxu__rvrv.dtype in
        (types.int64, types.float64, types.bool_, datetime_date_type) or
        isinstance(mxu__rvrv.dtype, TimeType)) for mxu__rvrv in typ.data)
    if jzh__yqs:
        ddusd__evx, nylbr__bnih, klfs__hvaz = _get_C_API_ptrs(c, tty__urnye
            .data, typ.data, typ.names)
        xgy__qvs = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        kox__sicb = cgutils.get_or_insert_function(c.builder.module,
            xgy__qvs, name='np_array_from_struct_array')
        arr = c.builder.call(kox__sicb, [length, c.context.get_constant(
            types.int32, len(typ.data)), c.builder.bitcast(ddusd__evx, lir.
            IntType(8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            nylbr__bnih, lir.IntType(8).as_pointer()), c.builder.bitcast(
            klfs__hvaz, lir.IntType(8).as_pointer()), c.context.
            get_constant(types.bool_, is_tuple_array)])
    else:
        arr = _box_struct_array_generic(typ, c, length, tty__urnye.data,
            null_bitmap_ptr, is_tuple_array)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_struct_array_generic(typ, c, length, data_arrs_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    lcpi__ezin = context.insert_const_string(builder.module, 'numpy')
    xnxb__pkde = c.pyapi.import_module_noblock(lcpi__ezin)
    rjkkk__sgve = c.pyapi.object_getattr_string(xnxb__pkde, 'object_')
    nebz__wdmrs = c.pyapi.long_from_longlong(length)
    karns__jcdpj = c.pyapi.call_method(xnxb__pkde, 'ndarray', (nebz__wdmrs,
        rjkkk__sgve))
    aqcf__gwepg = c.pyapi.object_getattr_string(xnxb__pkde, 'nan')
    with cgutils.for_range(builder, length) as gwise__crv:
        aboj__oyl = gwise__crv.index
        pyarray_setitem(builder, context, karns__jcdpj, aboj__oyl, aqcf__gwepg)
        beak__wmmvy = get_bitmap_bit(builder, null_bitmap_ptr, aboj__oyl)
        bsv__wkgm = builder.icmp_unsigned('!=', beak__wmmvy, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(bsv__wkgm):
            if is_tuple_array:
                elppx__jbz = c.pyapi.tuple_new(len(typ.data))
            else:
                elppx__jbz = c.pyapi.dict_new(len(typ.data))
            for i, arr_typ in enumerate(typ.data):
                if is_tuple_array:
                    c.pyapi.incref(aqcf__gwepg)
                    c.pyapi.tuple_setitem(elppx__jbz, i, aqcf__gwepg)
                else:
                    c.pyapi.dict_setitem_string(elppx__jbz, typ.names[i],
                        aqcf__gwepg)
                data_arr = c.builder.extract_value(data_arrs_tup, i)
                nqsdn__ttm, bkfxc__eseed = c.pyapi.call_jit_code(lambda
                    data_arr, ind: not bodo.libs.array_kernels.isna(
                    data_arr, ind), types.bool_(arr_typ, types.int64), [
                    data_arr, aboj__oyl])
                with builder.if_then(bkfxc__eseed):
                    nqsdn__ttm, field_val = c.pyapi.call_jit_code(lambda
                        data_arr, ind: data_arr[ind], arr_typ.dtype(arr_typ,
                        types.int64), [data_arr, aboj__oyl])
                    iusy__auxq = c.pyapi.from_native_value(arr_typ.dtype,
                        field_val, c.env_manager)
                    if is_tuple_array:
                        c.pyapi.tuple_setitem(elppx__jbz, i, iusy__auxq)
                    else:
                        c.pyapi.dict_setitem_string(elppx__jbz, typ.names[i
                            ], iusy__auxq)
                        c.pyapi.decref(iusy__auxq)
            pyarray_setitem(builder, context, karns__jcdpj, aboj__oyl,
                elppx__jbz)
            c.pyapi.decref(elppx__jbz)
    c.pyapi.decref(xnxb__pkde)
    c.pyapi.decref(rjkkk__sgve)
    c.pyapi.decref(nebz__wdmrs)
    c.pyapi.decref(aqcf__gwepg)
    return karns__jcdpj


def _fix_nested_counts(nested_counts, struct_arr_type, nested_counts_type,
    builder):
    uhtik__xpg = bodo.utils.transform.get_type_alloc_counts(struct_arr_type
        ) - 1
    if uhtik__xpg == 0:
        return nested_counts
    if not isinstance(nested_counts_type, types.UniTuple):
        nested_counts = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), -1) for kfv__ptf in range(uhtik__xpg)])
    elif nested_counts_type.count < uhtik__xpg:
        nested_counts = cgutils.pack_array(builder, [builder.extract_value(
            nested_counts, i) for i in range(nested_counts_type.count)] + [
            lir.Constant(lir.IntType(64), -1) for kfv__ptf in range(
            uhtik__xpg - nested_counts_type.count)])
    return nested_counts


@intrinsic
def pre_alloc_struct_array(typingctx, num_structs_typ, nested_counts_typ,
    dtypes_typ, names_typ=None):
    assert isinstance(num_structs_typ, types.Integer) and isinstance(dtypes_typ
        , types.BaseTuple)
    if is_overload_none(names_typ):
        names = tuple(f'f{i}' for i in range(len(dtypes_typ)))
    else:
        names = tuple(get_overload_const_str(mxu__rvrv) for mxu__rvrv in
            names_typ.types)
    aanb__suj = tuple(mxu__rvrv.instance_type for mxu__rvrv in dtypes_typ.types
        )
    struct_arr_type = StructArrayType(aanb__suj, names)

    def codegen(context, builder, sig, args):
        vdo__qjoff, nested_counts, kfv__ptf, kfv__ptf = args
        nested_counts_type = sig.args[1]
        nested_counts = _fix_nested_counts(nested_counts, struct_arr_type,
            nested_counts_type, builder)
        vexo__whgzb, kfv__ptf, kfv__ptf = construct_struct_array(context,
            builder, struct_arr_type, vdo__qjoff, nested_counts)
        dka__hrcno = context.make_helper(builder, struct_arr_type)
        dka__hrcno.meminfo = vexo__whgzb
        return dka__hrcno._getvalue()
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
        assert isinstance(names, tuple) and all(isinstance(rcxk__evmdo, str
            ) for rcxk__evmdo in names) and len(names) == len(data)
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
        yme__dzy = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.UniTuple(types.int8, len(fe_type.data)))]
        models.StructModel.__init__(self, dmm, fe_type, yme__dzy)


@register_model(StructType)
class StructModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructPayloadType(fe_type.data)
        yme__dzy = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, yme__dzy)


def define_struct_dtor(context, builder, struct_type, payload_type):
    zro__auq = builder.module
    xgy__qvs = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    zlyzc__vsoeo = cgutils.get_or_insert_function(zro__auq, xgy__qvs, name=
        '.dtor.struct.{}.{}.'.format(struct_type.data, struct_type.names))
    if not zlyzc__vsoeo.is_declaration:
        return zlyzc__vsoeo
    zlyzc__vsoeo.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(zlyzc__vsoeo.append_basic_block())
    cwtjv__lna = zlyzc__vsoeo.args[0]
    miyv__hoyqm = context.get_value_type(payload_type).as_pointer()
    gzpwc__ztnj = builder.bitcast(cwtjv__lna, miyv__hoyqm)
    tty__urnye = context.make_helper(builder, payload_type, ref=gzpwc__ztnj)
    for i in range(len(struct_type.data)):
        huuq__ple = builder.extract_value(tty__urnye.null_bitmap, i)
        bsv__wkgm = builder.icmp_unsigned('==', huuq__ple, lir.Constant(
            huuq__ple.type, 1))
        with builder.if_then(bsv__wkgm):
            val = builder.extract_value(tty__urnye.data, i)
            context.nrt.decref(builder, struct_type.data[i], val)
    builder.ret_void()
    return zlyzc__vsoeo


def _get_struct_payload(context, builder, typ, struct):
    struct = context.make_helper(builder, typ, struct)
    payload_type = StructPayloadType(typ.data)
    trn__wlf = context.nrt.meminfo_data(builder, struct.meminfo)
    tgfw__ohjcv = builder.bitcast(trn__wlf, context.get_value_type(
        payload_type).as_pointer())
    tty__urnye = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(tgfw__ohjcv))
    return tty__urnye, tgfw__ohjcv


@unbox(StructType)
def unbox_struct(typ, val, c):
    context = c.context
    builder = c.builder
    lcpi__ezin = context.insert_const_string(builder.module, 'pandas')
    pjhs__jhws = c.pyapi.import_module_noblock(lcpi__ezin)
    ckq__ofb = c.pyapi.object_getattr_string(pjhs__jhws, 'NA')
    xzn__nwk = []
    nulls = []
    for i, mxu__rvrv in enumerate(typ.data):
        iusy__auxq = c.pyapi.dict_getitem_string(val, typ.names[i])
        xek__ddtt = cgutils.alloca_once_value(c.builder, context.
            get_constant(types.uint8, 0))
        vovy__ypl = cgutils.alloca_once_value(c.builder, cgutils.
            get_null_value(context.get_value_type(mxu__rvrv)))
        msqb__xgp = is_na_value(builder, context, iusy__auxq, ckq__ofb)
        bsv__wkgm = builder.icmp_unsigned('!=', msqb__xgp, lir.Constant(
            msqb__xgp.type, 1))
        with builder.if_then(bsv__wkgm):
            builder.store(context.get_constant(types.uint8, 1), xek__ddtt)
            field_val = c.pyapi.to_native_value(mxu__rvrv, iusy__auxq).value
            builder.store(field_val, vovy__ypl)
        xzn__nwk.append(builder.load(vovy__ypl))
        nulls.append(builder.load(xek__ddtt))
    c.pyapi.decref(pjhs__jhws)
    c.pyapi.decref(ckq__ofb)
    vexo__whgzb = construct_struct(context, builder, typ, xzn__nwk, nulls)
    struct = context.make_helper(builder, typ)
    struct.meminfo = vexo__whgzb
    vvgk__nifhn = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(struct._getvalue(), is_error=vvgk__nifhn)


@box(StructType)
def box_struct(typ, val, c):
    masr__ksdn = c.pyapi.dict_new(len(typ.data))
    tty__urnye, kfv__ptf = _get_struct_payload(c.context, c.builder, typ, val)
    assert len(typ.data) > 0
    for i, val_typ in enumerate(typ.data):
        c.pyapi.dict_setitem_string(masr__ksdn, typ.names[i], c.pyapi.
            borrow_none())
        huuq__ple = c.builder.extract_value(tty__urnye.null_bitmap, i)
        bsv__wkgm = c.builder.icmp_unsigned('==', huuq__ple, lir.Constant(
            huuq__ple.type, 1))
        with c.builder.if_then(bsv__wkgm):
            krmd__jxg = c.builder.extract_value(tty__urnye.data, i)
            c.context.nrt.incref(c.builder, val_typ, krmd__jxg)
            ezntv__fcrif = c.pyapi.from_native_value(val_typ, krmd__jxg, c.
                env_manager)
            c.pyapi.dict_setitem_string(masr__ksdn, typ.names[i], ezntv__fcrif)
            c.pyapi.decref(ezntv__fcrif)
    c.context.nrt.decref(c.builder, typ, val)
    return masr__ksdn


@intrinsic
def init_struct(typingctx, data_typ, names_typ=None):
    names = tuple(get_overload_const_str(mxu__rvrv) for mxu__rvrv in
        names_typ.types)
    struct_type = StructType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, wjg__ylmbf = args
        payload_type = StructPayloadType(struct_type.data)
        uawg__vwxvd = context.get_value_type(payload_type)
        ihhd__rvle = context.get_abi_sizeof(uawg__vwxvd)
        ungvi__hsrv = define_struct_dtor(context, builder, struct_type,
            payload_type)
        vexo__whgzb = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, ihhd__rvle), ungvi__hsrv)
        trn__wlf = context.nrt.meminfo_data(builder, vexo__whgzb)
        tgfw__ohjcv = builder.bitcast(trn__wlf, uawg__vwxvd.as_pointer())
        tty__urnye = cgutils.create_struct_proxy(payload_type)(context, builder
            )
        tty__urnye.data = data
        tty__urnye.null_bitmap = cgutils.pack_array(builder, [context.
            get_constant(types.uint8, 1) for kfv__ptf in range(len(data_typ
            .types))])
        builder.store(tty__urnye._getvalue(), tgfw__ohjcv)
        context.nrt.incref(builder, data_typ, data)
        struct = context.make_helper(builder, struct_type)
        struct.meminfo = vexo__whgzb
        return struct._getvalue()
    return struct_type(data_typ, names_typ), codegen


@intrinsic
def get_struct_data(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        tty__urnye, kfv__ptf = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            tty__urnye.data)
    return types.BaseTuple.from_types(struct_typ.data)(struct_typ), codegen


@intrinsic
def get_struct_null_bitmap(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        tty__urnye, kfv__ptf = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            tty__urnye.null_bitmap)
    gtif__esme = types.UniTuple(types.int8, len(struct_typ.data))
    return gtif__esme(struct_typ), codegen


@intrinsic
def set_struct_data(typingctx, struct_typ, field_ind_typ, val_typ=None):
    assert isinstance(struct_typ, StructType) and is_overload_constant_int(
        field_ind_typ)
    field_ind = get_overload_const_int(field_ind_typ)

    def codegen(context, builder, sig, args):
        struct, kfv__ptf, val = args
        tty__urnye, tgfw__ohjcv = _get_struct_payload(context, builder,
            struct_typ, struct)
        prjhj__yzcm = tty__urnye.data
        grgo__djz = builder.insert_value(prjhj__yzcm, val, field_ind)
        wsbqf__xwa = types.BaseTuple.from_types(struct_typ.data)
        context.nrt.decref(builder, wsbqf__xwa, prjhj__yzcm)
        context.nrt.incref(builder, wsbqf__xwa, grgo__djz)
        tty__urnye.data = grgo__djz
        builder.store(tty__urnye._getvalue(), tgfw__ohjcv)
        return context.get_dummy_value()
    return types.none(struct_typ, field_ind_typ, val_typ), codegen


def _get_struct_field_ind(struct, ind, op):
    if not is_overload_constant_str(ind):
        raise BodoError(
            'structs (from struct array) only support constant strings for {}, not {}'
            .format(op, ind))
    ehll__ghwie = get_overload_const_str(ind)
    if ehll__ghwie not in struct.names:
        raise BodoError('Field {} does not exist in struct {}'.format(
            ehll__ghwie, struct))
    return struct.names.index(ehll__ghwie)


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
    uawg__vwxvd = context.get_value_type(payload_type)
    ihhd__rvle = context.get_abi_sizeof(uawg__vwxvd)
    ungvi__hsrv = define_struct_dtor(context, builder, struct_type,
        payload_type)
    vexo__whgzb = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, ihhd__rvle), ungvi__hsrv)
    trn__wlf = context.nrt.meminfo_data(builder, vexo__whgzb)
    tgfw__ohjcv = builder.bitcast(trn__wlf, uawg__vwxvd.as_pointer())
    tty__urnye = cgutils.create_struct_proxy(payload_type)(context, builder)
    tty__urnye.data = cgutils.pack_array(builder, values
        ) if types.is_homogeneous(*struct_type.data) else cgutils.pack_struct(
        builder, values)
    tty__urnye.null_bitmap = cgutils.pack_array(builder, nulls)
    builder.store(tty__urnye._getvalue(), tgfw__ohjcv)
    return vexo__whgzb


@intrinsic
def struct_array_get_struct(typingctx, struct_arr_typ, ind_typ=None):
    assert isinstance(struct_arr_typ, StructArrayType) and isinstance(ind_typ,
        types.Integer)
    geyq__ssu = tuple(d.dtype for d in struct_arr_typ.data)
    bxp__frsi = StructType(geyq__ssu, struct_arr_typ.names)

    def codegen(context, builder, sig, args):
        bmz__nqe, ind = args
        tty__urnye = _get_struct_arr_payload(context, builder,
            struct_arr_typ, bmz__nqe)
        xzn__nwk = []
        ykr__eqv = []
        for i, arr_typ in enumerate(struct_arr_typ.data):
            uyttb__cap = builder.extract_value(tty__urnye.data, i)
            fbpy__glajo = context.compile_internal(builder, lambda arr, ind:
                np.uint8(0) if bodo.libs.array_kernels.isna(arr, ind) else
                np.uint8(1), types.uint8(arr_typ, types.int64), [uyttb__cap,
                ind])
            ykr__eqv.append(fbpy__glajo)
            cbp__rkhx = cgutils.alloca_once_value(builder, context.
                get_constant_null(arr_typ.dtype))
            bsv__wkgm = builder.icmp_unsigned('==', fbpy__glajo, lir.
                Constant(fbpy__glajo.type, 1))
            with builder.if_then(bsv__wkgm):
                ymjek__tcbj = context.compile_internal(builder, lambda arr,
                    ind: arr[ind], arr_typ.dtype(arr_typ, types.int64), [
                    uyttb__cap, ind])
                builder.store(ymjek__tcbj, cbp__rkhx)
            xzn__nwk.append(builder.load(cbp__rkhx))
        if isinstance(bxp__frsi, types.DictType):
            qrro__whcp = [context.insert_const_string(builder.module,
                ncjj__ayplc) for ncjj__ayplc in struct_arr_typ.names]
            mxfvz__wmv = cgutils.pack_array(builder, xzn__nwk)
            vck__ptlk = cgutils.pack_array(builder, qrro__whcp)

            def impl(names, vals):
                d = {}
                for i, ncjj__ayplc in enumerate(names):
                    d[ncjj__ayplc] = vals[i]
                return d
            dodj__ozt = context.compile_internal(builder, impl, bxp__frsi(
                types.Tuple(tuple(types.StringLiteral(ncjj__ayplc) for
                ncjj__ayplc in struct_arr_typ.names)), types.Tuple(
                geyq__ssu)), [vck__ptlk, mxfvz__wmv])
            context.nrt.decref(builder, types.BaseTuple.from_types(
                geyq__ssu), mxfvz__wmv)
            return dodj__ozt
        vexo__whgzb = construct_struct(context, builder, bxp__frsi,
            xzn__nwk, ykr__eqv)
        struct = context.make_helper(builder, bxp__frsi)
        struct.meminfo = vexo__whgzb
        return struct._getvalue()
    return bxp__frsi(struct_arr_typ, ind_typ), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        tty__urnye = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            tty__urnye.data)
    return types.BaseTuple.from_types(arr_typ.data)(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        tty__urnye = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            tty__urnye.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


@intrinsic
def init_struct_arr(typingctx, data_typ, null_bitmap_typ, names_typ=None):
    names = tuple(get_overload_const_str(mxu__rvrv) for mxu__rvrv in
        names_typ.types)
    struct_arr_type = StructArrayType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, vefwm__ycxbf, wjg__ylmbf = args
        payload_type = StructArrayPayloadType(struct_arr_type.data)
        uawg__vwxvd = context.get_value_type(payload_type)
        ihhd__rvle = context.get_abi_sizeof(uawg__vwxvd)
        ungvi__hsrv = define_struct_arr_dtor(context, builder,
            struct_arr_type, payload_type)
        vexo__whgzb = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, ihhd__rvle), ungvi__hsrv)
        trn__wlf = context.nrt.meminfo_data(builder, vexo__whgzb)
        tgfw__ohjcv = builder.bitcast(trn__wlf, uawg__vwxvd.as_pointer())
        tty__urnye = cgutils.create_struct_proxy(payload_type)(context, builder
            )
        tty__urnye.data = data
        tty__urnye.null_bitmap = vefwm__ycxbf
        builder.store(tty__urnye._getvalue(), tgfw__ohjcv)
        context.nrt.incref(builder, data_typ, data)
        context.nrt.incref(builder, null_bitmap_typ, vefwm__ycxbf)
        dka__hrcno = context.make_helper(builder, struct_arr_type)
        dka__hrcno.meminfo = vexo__whgzb
        return dka__hrcno._getvalue()
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
    drf__vmx = len(arr.data)
    sqmz__ubs = 'def impl(arr, ind):\n'
    sqmz__ubs += '  data = get_data(arr)\n'
    sqmz__ubs += '  null_bitmap = get_null_bitmap(arr)\n'
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        sqmz__ubs += """  out_null_bitmap = get_new_null_mask_bool_index(null_bitmap, ind, len(data[0]))
"""
    elif is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        sqmz__ubs += """  out_null_bitmap = get_new_null_mask_int_index(null_bitmap, ind, len(data[0]))
"""
    elif isinstance(ind, types.SliceType):
        sqmz__ubs += """  out_null_bitmap = get_new_null_mask_slice_index(null_bitmap, ind, len(data[0]))
"""
    else:
        raise BodoError('invalid index {} in struct array indexing'.format(ind)
            )
    sqmz__ubs += ('  return init_struct_arr(({},), out_null_bitmap, ({},))\n'
        .format(', '.join('ensure_contig_if_np(data[{}][ind])'.format(i) for
        i in range(drf__vmx)), ', '.join("'{}'".format(ncjj__ayplc) for
        ncjj__ayplc in arr.names)))
    grg__tjz = {}
    exec(sqmz__ubs, {'init_struct_arr': init_struct_arr, 'get_data':
        get_data, 'get_null_bitmap': get_null_bitmap, 'ensure_contig_if_np':
        bodo.utils.conversion.ensure_contig_if_np,
        'get_new_null_mask_bool_index': bodo.utils.indexing.
        get_new_null_mask_bool_index, 'get_new_null_mask_int_index': bodo.
        utils.indexing.get_new_null_mask_int_index,
        'get_new_null_mask_slice_index': bodo.utils.indexing.
        get_new_null_mask_slice_index}, grg__tjz)
    impl = grg__tjz['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def struct_arr_setitem(arr, ind, val):
    if not isinstance(arr, StructArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        drf__vmx = len(arr.data)
        sqmz__ubs = 'def impl(arr, ind, val):\n'
        sqmz__ubs += '  data = get_data(arr)\n'
        sqmz__ubs += '  null_bitmap = get_null_bitmap(arr)\n'
        sqmz__ubs += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for i in range(drf__vmx):
            if isinstance(val, StructType):
                sqmz__ubs += "  if is_field_value_null(val, '{}'):\n".format(
                    arr.names[i])
                sqmz__ubs += (
                    '    bodo.libs.array_kernels.setna(data[{}], ind)\n'.
                    format(i))
                sqmz__ubs += '  else:\n'
                sqmz__ubs += "    data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
            else:
                sqmz__ubs += "  data[{}][ind] = val['{}']\n".format(i, arr.
                    names[i])
        grg__tjz = {}
        exec(sqmz__ubs, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'is_field_value_null':
            is_field_value_null}, grg__tjz)
        impl = grg__tjz['impl']
        return impl
    if isinstance(ind, types.SliceType):
        drf__vmx = len(arr.data)
        sqmz__ubs = 'def impl(arr, ind, val):\n'
        sqmz__ubs += '  data = get_data(arr)\n'
        sqmz__ubs += '  null_bitmap = get_null_bitmap(arr)\n'
        sqmz__ubs += '  val_data = get_data(val)\n'
        sqmz__ubs += '  val_null_bitmap = get_null_bitmap(val)\n'
        sqmz__ubs += """  setitem_slice_index_null_bits(null_bitmap, val_null_bitmap, ind, len(arr))
"""
        for i in range(drf__vmx):
            sqmz__ubs += '  data[{0}][ind] = val_data[{0}]\n'.format(i)
        grg__tjz = {}
        exec(sqmz__ubs, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'setitem_slice_index_null_bits':
            bodo.utils.indexing.setitem_slice_index_null_bits}, grg__tjz)
        impl = grg__tjz['impl']
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
    sqmz__ubs = 'def impl(A):\n'
    sqmz__ubs += '  total_nbytes = 0\n'
    sqmz__ubs += '  data = get_data(A)\n'
    for i in range(len(A.data)):
        sqmz__ubs += f'  total_nbytes += data[{i}].nbytes\n'
    sqmz__ubs += '  total_nbytes += get_null_bitmap(A).nbytes\n'
    sqmz__ubs += '  return total_nbytes\n'
    grg__tjz = {}
    exec(sqmz__ubs, {'get_data': get_data, 'get_null_bitmap':
        get_null_bitmap}, grg__tjz)
    impl = grg__tjz['impl']
    return impl


@overload_method(StructArrayType, 'copy', no_unliteral=True)
def overload_struct_arr_copy(A):
    names = A.names

    def copy_impl(A):
        data = get_data(A)
        vefwm__ycxbf = get_null_bitmap(A)
        hcvz__bir = bodo.libs.struct_arr_ext.copy_arr_tup(data)
        pall__sem = vefwm__ycxbf.copy()
        return init_struct_arr(hcvz__bir, pall__sem, names)
    return copy_impl


def copy_arr_tup(arrs):
    return tuple(rcxk__evmdo.copy() for rcxk__evmdo in arrs)


@overload(copy_arr_tup, no_unliteral=True)
def copy_arr_tup_overload(arrs):
    zck__gfgip = arrs.count
    sqmz__ubs = 'def f(arrs):\n'
    sqmz__ubs += '  return ({},)\n'.format(','.join('arrs[{}].copy()'.
        format(i) for i in range(zck__gfgip)))
    grg__tjz = {}
    exec(sqmz__ubs, {}, grg__tjz)
    impl = grg__tjz['f']
    return impl
