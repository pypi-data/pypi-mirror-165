"""Numba extension support for time objects and their arrays.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_builtin, lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs import hdatetime_ext
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, is_iterable_type, is_list_like_index_type
_nanos_per_micro = 1000
_nanos_per_milli = 1000 * _nanos_per_micro
_nanos_per_second = 1000 * _nanos_per_milli
_nanos_per_minute = 60 * _nanos_per_second
_nanos_per_hour = 60 * _nanos_per_minute


class Time:

    def __init__(self, hour=0, minute=0, second=0, millisecond=0,
        microsecond=0, nanosecond=0, precision=9):
        self.precision = precision
        self.value = np.int64(hour * _nanos_per_hour + minute *
            _nanos_per_minute + second * _nanos_per_second + millisecond *
            _nanos_per_milli + microsecond * _nanos_per_micro + nanosecond)

    def __repr__(self):
        return (
            f'Time({self.hour}, {self.minute}, {self.second}, {self.millisecond}, {self.microsecond}, {self.nanosecond}, precision={self.precision})'
            )

    def __eq__(self, other):
        if not isinstance(other, Time):
            return False
        return self.value == other.value and self.precision == other.precision

    def _check_can_compare(self, other):
        if self.precision != other.precision:
            raise BodoError(
                f'Cannot compare times with different precisions: {self} and {other}'
                )

    def __lt__(self, other):
        self._check_can_compare(other)
        return self.value < other.value

    def __le__(self, other):
        self._check_can_compare(other)
        return self.value <= other.value

    def __int__(self):
        if self.precision == 9:
            return self.value
        if self.precision == 6:
            return self.value // _nanos_per_micro
        if self.precision == 3:
            return self.value // _nanos_per_milli
        if self.precision == 0:
            return self.value // _nanos_per_second
        raise BodoError(f'Unsupported precision: {self.precision}')

    def __hash__(self):
        return hash((self.value, self.precision))

    @property
    def hour(self):
        return self.value // _nanos_per_hour

    @property
    def minute(self):
        return self.value % _nanos_per_hour // _nanos_per_minute

    @property
    def second(self):
        return self.value % _nanos_per_minute // _nanos_per_second

    @property
    def millisecond(self):
        return self.value % _nanos_per_second // _nanos_per_milli

    @property
    def microsecond(self):
        return self.value % _nanos_per_milli // _nanos_per_micro

    @property
    def nanosecond(self):
        return self.value % _nanos_per_micro


ll.add_symbol('box_time_array', hdatetime_ext.box_time_array)
ll.add_symbol('unbox_time_array', hdatetime_ext.unbox_time_array)


class TimeType(types.Type):

    def __init__(self, precision):
        assert isinstance(precision, int
            ) and precision >= 0 and precision <= 9, 'precision must be an integer between 0 and 9'
        self.precision = precision
        super(TimeType, self).__init__(name=f'TimeType({precision})')
        self.bitwidth = 64


@typeof_impl.register(Time)
def typeof_time(val, c):
    return TimeType(val.precision)


@overload(Time)
def overload_time(hour=0, min=0, second=0, millisecond=0, microsecond=0,
    nanosecond=0, precision=9):

    def impl(hour=0, min=0, second=0, millisecond=0, microsecond=0,
        nanosecond=0, precision=9):
        return cast_int_to_time(_nanos_per_hour * hour + _nanos_per_minute *
            min + _nanos_per_second * second + _nanos_per_milli *
            millisecond + _nanos_per_micro * microsecond + nanosecond,
            precision)
    return impl


register_model(TimeType)(models.IntegerModel)


@overload_attribute(TimeType, 'hour')
def time_hour_attribute(val):
    return lambda val: cast_time_to_int(val) // _nanos_per_hour


@overload_attribute(TimeType, 'minute')
def time_minute_attribute(val):
    return lambda val: cast_time_to_int(val
        ) % _nanos_per_hour // _nanos_per_minute


@overload_attribute(TimeType, 'second')
def time_second_attribute(val):
    return lambda val: cast_time_to_int(val
        ) % _nanos_per_minute // _nanos_per_second


@overload_attribute(TimeType, 'millisecond')
def time_millisecond_attribute(val):
    return lambda val: cast_time_to_int(val
        ) % _nanos_per_second // _nanos_per_milli


@overload_attribute(TimeType, 'microsecond')
def time_microsecond_attribute(val):
    return lambda val: cast_time_to_int(val
        ) % _nanos_per_milli // _nanos_per_micro


@overload_attribute(TimeType, 'nanosecond')
def time_nanosecond_attribute(val):
    return lambda val: cast_time_to_int(val) % _nanos_per_micro


def _to_nanos_codegen(c, hour_ll, minute_ll, second_ll, millisecond_ll,
    microsecond_ll, nanosecond_ll):
    return c.builder.add(nanosecond_ll, c.builder.add(c.builder.mul(
        microsecond_ll, lir.Constant(lir.IntType(64), _nanos_per_micro)), c
        .builder.add(c.builder.mul(millisecond_ll, lir.Constant(lir.IntType
        (64), _nanos_per_milli)), c.builder.add(c.builder.mul(second_ll,
        lir.Constant(lir.IntType(64), _nanos_per_second)), c.builder.add(c.
        builder.mul(minute_ll, lir.Constant(lir.IntType(64),
        _nanos_per_minute)), c.builder.mul(hour_ll, lir.Constant(lir.
        IntType(64), _nanos_per_hour)))))))


def _from_nanos_codegen(c, val):
    vwa__dwe = c.pyapi.long_from_longlong(c.builder.udiv(val, lir.Constant(
        lir.IntType(64), _nanos_per_hour)))
    ika__nznbq = c.pyapi.long_from_longlong(c.builder.udiv(c.builder.urem(
        val, lir.Constant(lir.IntType(64), _nanos_per_hour)), lir.Constant(
        lir.IntType(64), _nanos_per_minute)))
    kyy__kzu = c.pyapi.long_from_longlong(c.builder.udiv(c.builder.urem(val,
        lir.Constant(lir.IntType(64), _nanos_per_minute)), lir.Constant(lir
        .IntType(64), _nanos_per_second)))
    jzwd__hyoh = c.pyapi.long_from_longlong(c.builder.udiv(c.builder.urem(
        val, lir.Constant(lir.IntType(64), _nanos_per_second)), lir.
        Constant(lir.IntType(64), _nanos_per_milli)))
    brlzs__dofs = c.pyapi.long_from_longlong(c.builder.udiv(c.builder.urem(
        val, lir.Constant(lir.IntType(64), _nanos_per_milli)), lir.Constant
        (lir.IntType(64), _nanos_per_micro)))
    yjpsm__vhwdw = c.pyapi.long_from_longlong(c.builder.urem(val, lir.
        Constant(lir.IntType(64), _nanos_per_micro)))
    return (vwa__dwe, ika__nznbq, kyy__kzu, jzwd__hyoh, brlzs__dofs,
        yjpsm__vhwdw)


@unbox(TimeType)
def unbox_time(typ, val, c):
    vwa__dwe = c.pyapi.object_getattr_string(val, 'hour')
    ika__nznbq = c.pyapi.object_getattr_string(val, 'minute')
    kyy__kzu = c.pyapi.object_getattr_string(val, 'second')
    jzwd__hyoh = c.pyapi.object_getattr_string(val, 'millisecond')
    brlzs__dofs = c.pyapi.object_getattr_string(val, 'microsecond')
    yjpsm__vhwdw = c.pyapi.object_getattr_string(val, 'nanosecond')
    hour_ll = c.pyapi.long_as_longlong(vwa__dwe)
    minute_ll = c.pyapi.long_as_longlong(ika__nznbq)
    second_ll = c.pyapi.long_as_longlong(kyy__kzu)
    millisecond_ll = c.pyapi.long_as_longlong(jzwd__hyoh)
    microsecond_ll = c.pyapi.long_as_longlong(brlzs__dofs)
    nanosecond_ll = c.pyapi.long_as_longlong(yjpsm__vhwdw)
    sge__mzzoo = _to_nanos_codegen(c, hour_ll, minute_ll, second_ll,
        millisecond_ll, microsecond_ll, nanosecond_ll)
    c.pyapi.decref(vwa__dwe)
    c.pyapi.decref(ika__nznbq)
    c.pyapi.decref(kyy__kzu)
    c.pyapi.decref(jzwd__hyoh)
    c.pyapi.decref(brlzs__dofs)
    c.pyapi.decref(yjpsm__vhwdw)
    aku__sznb = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(sge__mzzoo, is_error=aku__sznb)


@lower_constant(TimeType)
def lower_constant_time(context, builder, ty, pyval):
    hour_ll = context.get_constant(types.int64, pyval.hour)
    minute_ll = context.get_constant(types.int64, pyval.minute)
    second_ll = context.get_constant(types.int64, pyval.second)
    millisecond_ll = context.get_constant(types.int64, pyval.millisecond)
    microsecond_ll = context.get_constant(types.int64, pyval.microsecond)
    nanosecond_ll = context.get_constant(types.int64, pyval.nanosecond)
    sge__mzzoo = _to_nanos_codegen(context, hour_ll, minute_ll, second_ll,
        millisecond_ll, microsecond_ll, nanosecond_ll)
    return sge__mzzoo


@box(TimeType)
def box_time(typ, val, c):
    (vwa__dwe, ika__nznbq, kyy__kzu, jzwd__hyoh, brlzs__dofs, yjpsm__vhwdw
        ) = _from_nanos_codegen(c, val)
    cwp__jtdte = c.pyapi.unserialize(c.pyapi.serialize_object(Time))
    hkry__rgg = c.pyapi.call_function_objargs(cwp__jtdte, (vwa__dwe,
        ika__nznbq, kyy__kzu, jzwd__hyoh, brlzs__dofs, yjpsm__vhwdw, c.
        pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.precision)))
        )
    c.pyapi.decref(vwa__dwe)
    c.pyapi.decref(ika__nznbq)
    c.pyapi.decref(kyy__kzu)
    c.pyapi.decref(jzwd__hyoh)
    c.pyapi.decref(brlzs__dofs)
    c.pyapi.decref(yjpsm__vhwdw)
    c.pyapi.decref(cwp__jtdte)
    return hkry__rgg


@lower_builtin(Time, types.int64, types.int64, types.int64, types.int64,
    types.int64, types.int64)
def impl_ctor_time(context, builder, sig, args):
    (hour_ll, minute_ll, second_ll, millisecond_ll, microsecond_ll,
        nanosecond_ll) = args
    sge__mzzoo = _to_nanos_codegen(context, hour_ll, minute_ll, second_ll,
        millisecond_ll, microsecond_ll, nanosecond_ll)
    return sge__mzzoo


@intrinsic
def cast_int_to_time(typingctx, val, precision):
    assert val == types.int64, 'val must be int64'
    assert isinstance(precision, types.IntegerLiteral
        ), 'precision must be an integer literal'

    def codegen(context, builder, signature, args):
        return args[0]
    return TimeType(precision.literal_value)(types.int64, types.int64), codegen


@intrinsic
def cast_time_to_int(typingctx, val):
    assert isinstance(val, TimeType), 'val must be Time'

    def codegen(context, builder, signature, args):
        return args[0]
    return types.int64(val), codegen


class TimeArrayType(types.ArrayCompatible):

    def __init__(self, precision):
        assert isinstance(precision, int
            ) and precision >= 0 and precision <= 9, 'precision must be an integer between 0 and 9'
        self.precision = precision
        super(TimeArrayType, self).__init__(name=f'TimeArrayType({precision})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return TimeType(self.precision)

    def copy(self):
        return TimeArrayType(self.precision)


data_type = types.Array(types.int64, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(TimeArrayType)
class TimeArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        jbeo__vqx = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, jbeo__vqx)


make_attribute_wrapper(TimeArrayType, 'data', '_data')
make_attribute_wrapper(TimeArrayType, 'null_bitmap', '_null_bitmap')


@overload_method(TimeArrayType, 'copy', no_unliteral=True)
def overload_time_arr_copy(A):
    return lambda A: bodo.hiframes.time_ext.init_time_array(A._data.copy(),
        A._null_bitmap.copy())


@overload_attribute(TimeArrayType, 'dtype')
def overload_time_arr_dtype(A):
    return lambda A: np.object_


@unbox(TimeArrayType)
def unbox_time_array(typ, val, c):
    n = bodo.utils.utils.object_length(c, val)
    ogmx__mry = types.Array(types.intp, 1, 'C')
    hou__sgbhr = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        ogmx__mry, [n])
    mlqt__yiupp = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    zrux__cqltw = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [mlqt__yiupp])
    swsbq__gsm = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64), lir.IntType(64).as_pointer(), lir.
        IntType(8).as_pointer()])
    cwmvu__mxu = cgutils.get_or_insert_function(c.builder.module,
        swsbq__gsm, name='unbox_time_array')
    c.builder.call(cwmvu__mxu, [val, n, hou__sgbhr.data, zrux__cqltw.data])
    xwza__ont = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    xwza__ont.data = hou__sgbhr._getvalue()
    xwza__ont.null_bitmap = zrux__cqltw._getvalue()
    aku__sznb = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(xwza__ont._getvalue(), is_error=aku__sznb)


@box(TimeArrayType)
def box_time_array(typ, val, c):
    rbm__naa = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    hou__sgbhr = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, rbm__naa.data)
    vchys__lbr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, rbm__naa.null_bitmap).data
    n = c.builder.extract_value(hou__sgbhr.shape, 0)
    swsbq__gsm = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8)])
    fsbp__jibmi = cgutils.get_or_insert_function(c.builder.module,
        swsbq__gsm, name='box_time_array')
    kyds__lswn = c.builder.call(fsbp__jibmi, [n, hou__sgbhr.data,
        vchys__lbr, lir.Constant(lir.IntType(8), typ.precision)])
    c.context.nrt.decref(c.builder, typ, val)
    return kyds__lswn


@intrinsic
def init_time_array(typingctx, data, nulls, precision):
    assert data == types.Array(types.int64, 1, 'C'
        ), 'data must be an array of int64'
    assert nulls == types.Array(types.uint8, 1, 'C'
        ), 'nulls must be an array of uint8'
    assert isinstance(precision, types.IntegerLiteral
        ), 'precision must be an integer literal'

    def codegen(context, builder, signature, args):
        bwpdh__isw, rzt__vybm, snzxt__byv = args
        cjdjo__atkzn = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        cjdjo__atkzn.data = bwpdh__isw
        cjdjo__atkzn.null_bitmap = rzt__vybm
        context.nrt.incref(builder, signature.args[0], bwpdh__isw)
        context.nrt.incref(builder, signature.args[1], rzt__vybm)
        return cjdjo__atkzn._getvalue()
    sig = TimeArrayType(precision.literal_value)(data, nulls, precision)
    return sig, codegen


@lower_constant(TimeArrayType)
def lower_constant_time_arr(context, builder, typ, pyval):
    n = len(pyval)
    hou__sgbhr = np.full(n, 0, np.int64)
    pfxvm__ixne = np.empty(n + 7 >> 3, np.uint8)
    for frj__ict, eayz__zdw in enumerate(pyval):
        knjql__xwp = pd.isna(eayz__zdw)
        bodo.libs.int_arr_ext.set_bit_to_arr(pfxvm__ixne, frj__ict, int(not
            knjql__xwp))
        if not knjql__xwp:
            hou__sgbhr[frj__ict] = (eayz__zdw.hour * _nanos_per_hour + 
                eayz__zdw.minute * _nanos_per_minute + eayz__zdw.second *
                _nanos_per_second + eayz__zdw.millisecond *
                _nanos_per_milli + eayz__zdw.microsecond * _nanos_per_micro +
                eayz__zdw.nanosecond)
    unj__gsgi = context.get_constant_generic(builder, data_type, hou__sgbhr)
    ybcz__qmck = context.get_constant_generic(builder, nulls_type, pfxvm__ixne)
    return lir.Constant.literal_struct([unj__gsgi, ybcz__qmck])


@numba.njit(no_cpython_wrapper=True)
def alloc_time_array(n):
    hou__sgbhr = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_time_array(hou__sgbhr, nulls)


def alloc_time_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws, 'Only one argument allowed'
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_time_ext_alloc_time_array = (
    alloc_time_array_equiv)


@overload(operator.getitem, no_unliteral=True)
def time_arr_getitem(A, ind):
    if not isinstance(A, TimeArrayType):
        return
    precision = A.precision
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda A, ind: cast_int_to_time(A._data[ind], precision)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            bum__fhkp, wyw__jbut = array_getitem_bool_index(A, ind)
            return init_time_array(bum__fhkp, wyw__jbut, precision)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            bum__fhkp, wyw__jbut = array_getitem_int_index(A, ind)
            return init_time_array(bum__fhkp, wyw__jbut, precision)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            bum__fhkp, wyw__jbut = array_getitem_slice_index(A, ind)
            return init_time_array(bum__fhkp, wyw__jbut, precision)
        return impl_slice
    raise BodoError(
        f'getitem for TimeArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def time_arr_setitem(A, idx, val):
    if not isinstance(A, TimeArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    rwuxq__lao = (
        f"setitem for TimeArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if isinstance(types.unliteral(val), TimeType):

            def impl(A, idx, val):
                A._data[idx] = cast_time_to_int(val)
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl
        else:
            raise BodoError(rwuxq__lao)
    if not (is_iterable_type(val) and isinstance(val.dtype, TimeType) or
        isinstance(types.unliteral(val), TimeType)):
        raise BodoError(rwuxq__lao)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, types.Integer):
        if isinstance(types.unliteral(val), TimeType):
            return lambda A, idx, val: array_setitem_int_index(A, idx,
                cast_time_to_int(val))

        def impl_arr_ind(A, idx, val):
            array_setitem_int_index(A, idx, val)
        return impl_arr_ind
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if isinstance(types.unliteral(val), TimeType):
            return lambda A, idx, val: array_setitem_bool_index(A, idx,
                cast_time_to_int(val))

        def impl_bool_ind_mask(A, idx, val):
            array_setitem_bool_index(A, idx, val)
        return impl_bool_ind_mask
    if isinstance(idx, types.SliceType):
        if isinstance(types.unliteral(val), TimeType):
            return lambda A, idx, val: array_setitem_slice_index(A, idx,
                cast_time_to_int(val))

        def impl_slice_mask(A, idx, val):
            array_setitem_slice_index(A, idx, val)
        return impl_slice_mask
    raise BodoError(
        f'setitem for TimeArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_len_time_arr(A):
    if isinstance(A, TimeArrayType):
        return lambda A: len(A._data)


@overload_attribute(TimeArrayType, 'shape')
def overload_time_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(TimeArrayType, 'nbytes')
def time_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


def create_cmp_op_overload(op):

    def overload_time_cmp(lhs, rhs):
        if isinstance(lhs, TimeType) and isinstance(rhs, TimeType):

            def impl(lhs, rhs):
                ytnw__oescs = cast_time_to_int(lhs)
                jem__hur = cast_time_to_int(rhs)
                return op(0 if ytnw__oescs == jem__hur else 1 if 
                    ytnw__oescs > jem__hur else -1, 0)
            return impl
    return overload_time_cmp
