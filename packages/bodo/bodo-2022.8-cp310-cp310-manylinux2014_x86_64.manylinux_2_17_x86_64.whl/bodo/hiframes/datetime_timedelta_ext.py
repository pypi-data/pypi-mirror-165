"""Numba extension support for datetime.timedelta objects and their arrays.
"""
import datetime
import operator
from collections import namedtuple
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.libs import hdatetime_ext
from bodo.utils.indexing import get_new_null_mask_bool_index, get_new_null_mask_int_index, get_new_null_mask_slice_index, setitem_slice_index_null_bits
from bodo.utils.typing import BodoError, get_overload_const_str, is_iterable_type, is_list_like_index_type, is_overload_constant_str
ll.add_symbol('box_datetime_timedelta_array', hdatetime_ext.
    box_datetime_timedelta_array)
ll.add_symbol('unbox_datetime_timedelta_array', hdatetime_ext.
    unbox_datetime_timedelta_array)


class NoInput:
    pass


_no_input = NoInput()


class NoInputType(types.Type):

    def __init__(self):
        super(NoInputType, self).__init__(name='NoInput')


register_model(NoInputType)(models.OpaqueModel)


@typeof_impl.register(NoInput)
def _typ_no_input(val, c):
    return NoInputType()


@lower_constant(NoInputType)
def constant_no_input(context, builder, ty, pyval):
    return context.get_dummy_value()


class PDTimeDeltaType(types.Type):

    def __init__(self):
        super(PDTimeDeltaType, self).__init__(name='PDTimeDeltaType()')


pd_timedelta_type = PDTimeDeltaType()
types.pd_timedelta_type = pd_timedelta_type


@typeof_impl.register(pd.Timedelta)
def typeof_pd_timedelta(val, c):
    return pd_timedelta_type


@register_model(PDTimeDeltaType)
class PDTimeDeltaModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        dpe__dxz = [('value', types.int64)]
        super(PDTimeDeltaModel, self).__init__(dmm, fe_type, dpe__dxz)


@box(PDTimeDeltaType)
def box_pd_timedelta(typ, val, c):
    qxb__aal = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val
        )
    mfl__nvje = c.pyapi.long_from_longlong(qxb__aal.value)
    ygsvk__kah = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timedelta))
    res = c.pyapi.call_function_objargs(ygsvk__kah, (mfl__nvje,))
    c.pyapi.decref(mfl__nvje)
    c.pyapi.decref(ygsvk__kah)
    return res


@unbox(PDTimeDeltaType)
def unbox_pd_timedelta(typ, val, c):
    mfl__nvje = c.pyapi.object_getattr_string(val, 'value')
    gibpe__kjo = c.pyapi.long_as_longlong(mfl__nvje)
    qxb__aal = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qxb__aal.value = gibpe__kjo
    c.pyapi.decref(mfl__nvje)
    rgzuk__ktrbs = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(qxb__aal._getvalue(), is_error=rgzuk__ktrbs)


@lower_constant(PDTimeDeltaType)
def lower_constant_pd_timedelta(context, builder, ty, pyval):
    value = context.get_constant(types.int64, pyval.value)
    return lir.Constant.literal_struct([value])


@overload(pd.Timedelta, no_unliteral=True)
def pd_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
    microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    if value == _no_input:

        def impl_timedelta_kw(value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
            days += weeks * 7
            hours += days * 24
            minutes += 60 * hours
            seconds += 60 * minutes
            milliseconds += 1000 * seconds
            microseconds += 1000 * milliseconds
            xbw__kgeb = 1000 * microseconds
            return init_pd_timedelta(xbw__kgeb)
        return impl_timedelta_kw
    if value == bodo.string_type or is_overload_constant_str(value):

        def impl_str(value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
            with numba.objmode(res='pd_timedelta_type'):
                res = pd.Timedelta(value)
            return res
        return impl_str
    if value == pd_timedelta_type:
        return (lambda value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0: value)
    if value == datetime_timedelta_type:

        def impl_timedelta_datetime(value=_no_input, unit='ns', days=0,
            seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0,
            weeks=0):
            days = value.days
            seconds = 60 * 60 * 24 * days + value.seconds
            microseconds = 1000 * 1000 * seconds + value.microseconds
            xbw__kgeb = 1000 * microseconds
            return init_pd_timedelta(xbw__kgeb)
        return impl_timedelta_datetime
    if not is_overload_constant_str(unit):
        raise BodoError('pd.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    sdf__usaj, bfvn__qiw = pd._libs.tslibs.conversion.precision_from_unit(unit)

    def impl_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
        microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return init_pd_timedelta(value * sdf__usaj)
    return impl_timedelta


@intrinsic
def init_pd_timedelta(typingctx, value):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        timedelta = cgutils.create_struct_proxy(typ)(context, builder)
        timedelta.value = args[0]
        return timedelta._getvalue()
    return PDTimeDeltaType()(value), codegen


make_attribute_wrapper(PDTimeDeltaType, 'value', '_value')


@overload_attribute(PDTimeDeltaType, 'value')
@overload_attribute(PDTimeDeltaType, 'delta')
def pd_timedelta_get_value(td):

    def impl(td):
        return td._value
    return impl


@overload_attribute(PDTimeDeltaType, 'days')
def pd_timedelta_get_days(td):

    def impl(td):
        return td._value // (1000 * 1000 * 1000 * 60 * 60 * 24)
    return impl


@overload_attribute(PDTimeDeltaType, 'seconds')
def pd_timedelta_get_seconds(td):

    def impl(td):
        return td._value // (1000 * 1000 * 1000) % (60 * 60 * 24)
    return impl


@overload_attribute(PDTimeDeltaType, 'microseconds')
def pd_timedelta_get_microseconds(td):

    def impl(td):
        return td._value // 1000 % 1000000
    return impl


@overload_attribute(PDTimeDeltaType, 'nanoseconds')
def pd_timedelta_get_nanoseconds(td):

    def impl(td):
        return td._value % 1000
    return impl


@register_jitable
def _to_hours_pd_td(td):
    return td._value // (1000 * 1000 * 1000 * 60 * 60) % 24


@register_jitable
def _to_minutes_pd_td(td):
    return td._value // (1000 * 1000 * 1000 * 60) % 60


@register_jitable
def _to_seconds_pd_td(td):
    return td._value // (1000 * 1000 * 1000) % 60


@register_jitable
def _to_milliseconds_pd_td(td):
    return td._value // (1000 * 1000) % 1000


@register_jitable
def _to_microseconds_pd_td(td):
    return td._value // 1000 % 1000


Components = namedtuple('Components', ['days', 'hours', 'minutes',
    'seconds', 'milliseconds', 'microseconds', 'nanoseconds'], defaults=[0,
    0, 0, 0, 0, 0, 0])


@overload_attribute(PDTimeDeltaType, 'components', no_unliteral=True)
def pd_timedelta_get_components(td):

    def impl(td):
        a = Components(td.days, _to_hours_pd_td(td), _to_minutes_pd_td(td),
            _to_seconds_pd_td(td), _to_milliseconds_pd_td(td),
            _to_microseconds_pd_td(td), td.nanoseconds)
        return a
    return impl


@overload_method(PDTimeDeltaType, '__hash__', no_unliteral=True)
def pd_td___hash__(td):

    def impl(td):
        return hash(td._value)
    return impl


@overload_method(PDTimeDeltaType, 'to_numpy', no_unliteral=True)
@overload_method(PDTimeDeltaType, 'to_timedelta64', no_unliteral=True)
def pd_td_to_numpy(td):
    from bodo.hiframes.pd_timestamp_ext import integer_to_timedelta64

    def impl(td):
        return integer_to_timedelta64(td.value)
    return impl


@overload_method(PDTimeDeltaType, 'to_pytimedelta', no_unliteral=True)
def pd_td_to_pytimedelta(td):

    def impl(td):
        return datetime.timedelta(microseconds=np.int64(td._value / 1000))
    return impl


@overload_method(PDTimeDeltaType, 'total_seconds', no_unliteral=True)
def pd_td_total_seconds(td):

    def impl(td):
        return td._value // 1000 / 10 ** 6
    return impl


def overload_add_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            val = lhs.value + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            vomb__zzx = (rhs.microseconds + (rhs.seconds + rhs.days * 60 * 
                60 * 24) * 1000 * 1000) * 1000
            val = lhs.value + vomb__zzx
            return pd.Timedelta(val)
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            tnfod__prq = (lhs.microseconds + (lhs.seconds + lhs.days * 60 *
                60 * 24) * 1000 * 1000) * 1000
            val = tnfod__prq + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_datetime_type:
        from bodo.hiframes.pd_timestamp_ext import compute_pd_timestamp

        def impl(lhs, rhs):
            ncscr__kwo = rhs.toordinal()
            jzlbw__msqi = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            phie__qzuf = rhs.microsecond
            dix__xgh = lhs.value // 1000
            ejfrr__bayye = lhs.nanoseconds
            rzwk__xxkgn = phie__qzuf + dix__xgh
            ddkn__vwdfn = 1000000 * (ncscr__kwo * 86400 + jzlbw__msqi
                ) + rzwk__xxkgn
            vbmh__hyrkq = ejfrr__bayye
            return compute_pd_timestamp(ddkn__vwdfn, vbmh__hyrkq)
        return impl
    if lhs == datetime_datetime_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + rhs.to_pytimedelta()
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs.days + rhs.days
            s = lhs.seconds + rhs.seconds
            us = lhs.microseconds + rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            uir__utrxp = datetime.timedelta(rhs.toordinal(), hours=rhs.hour,
                minutes=rhs.minute, seconds=rhs.second, microseconds=rhs.
                microsecond)
            uir__utrxp = uir__utrxp + lhs
            zkd__njsf, rzmvo__ylqu = divmod(uir__utrxp.seconds, 3600)
            qrq__svk, kdcm__yim = divmod(rzmvo__ylqu, 60)
            if 0 < uir__utrxp.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(uir__utrxp
                    .days)
                return datetime.datetime(d.year, d.month, d.day, zkd__njsf,
                    qrq__svk, kdcm__yim, uir__utrxp.microseconds)
            raise OverflowError('result out of range')
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            uir__utrxp = datetime.timedelta(lhs.toordinal(), hours=lhs.hour,
                minutes=lhs.minute, seconds=lhs.second, microseconds=lhs.
                microsecond)
            uir__utrxp = uir__utrxp + rhs
            zkd__njsf, rzmvo__ylqu = divmod(uir__utrxp.seconds, 3600)
            qrq__svk, kdcm__yim = divmod(rzmvo__ylqu, 60)
            if 0 < uir__utrxp.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(uir__utrxp
                    .days)
                return datetime.datetime(d.year, d.month, d.day, zkd__njsf,
                    qrq__svk, kdcm__yim, uir__utrxp.microseconds)
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            wjof__fch = lhs.value - rhs.value
            return pd.Timedelta(wjof__fch)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_datetime_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs.days - rhs.days
            s = lhs.seconds - rhs.seconds
            us = lhs.microseconds - rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_array_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            uaq__zyqro = lhs
            numba.parfors.parfor.init_prange()
            n = len(uaq__zyqro)
            A = alloc_datetime_timedelta_array(n)
            for etd__ffgu in numba.parfors.parfor.internal_prange(n):
                A[etd__ffgu] = uaq__zyqro[etd__ffgu] - rhs
            return A
        return impl


def overload_mul_operator_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value * rhs)
        return impl
    elif isinstance(lhs, types.Integer) and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return pd.Timedelta(rhs.value * lhs)
        return impl
    if lhs == datetime_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            d = lhs.days * rhs
            s = lhs.seconds * rhs
            us = lhs.microseconds * rhs
            return datetime.timedelta(d, s, us)
        return impl
    elif isinstance(lhs, types.Integer) and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs * rhs.days
            s = lhs * rhs.seconds
            us = lhs * rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl


def overload_floordiv_operator_pd_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs.value // rhs.value
        return impl
    elif lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value // rhs)
        return impl


def overload_truediv_operator_pd_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs.value / rhs.value
        return impl
    elif lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(int(lhs.value / rhs))
        return impl


def overload_mod_operator_timedeltas(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value % rhs.value)
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            gomp__uqbl = _to_microseconds(lhs) % _to_microseconds(rhs)
            return datetime.timedelta(0, 0, gomp__uqbl)
        return impl


def pd_create_cmp_op_overload(op):

    def overload_pd_timedelta_cmp(lhs, rhs):
        if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

            def impl(lhs, rhs):
                return op(lhs.value, rhs.value)
            return impl
        if lhs == pd_timedelta_type and rhs == bodo.timedelta64ns:
            return lambda lhs, rhs: op(bodo.hiframes.pd_timestamp_ext.
                integer_to_timedelta64(lhs.value), rhs)
        if lhs == bodo.timedelta64ns and rhs == pd_timedelta_type:
            return lambda lhs, rhs: op(lhs, bodo.hiframes.pd_timestamp_ext.
                integer_to_timedelta64(rhs.value))
    return overload_pd_timedelta_cmp


@overload(operator.neg, no_unliteral=True)
def pd_timedelta_neg(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            return pd.Timedelta(-lhs.value)
        return impl


@overload(operator.pos, no_unliteral=True)
def pd_timedelta_pos(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            return lhs
        return impl


@overload(divmod, no_unliteral=True)
def pd_timedelta_divmod(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            oowtd__eeon, gomp__uqbl = divmod(lhs.value, rhs.value)
            return oowtd__eeon, pd.Timedelta(gomp__uqbl)
        return impl


@overload(abs, no_unliteral=True)
def pd_timedelta_abs(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            if lhs.value < 0:
                return -lhs
            else:
                return lhs
        return impl


class DatetimeTimeDeltaType(types.Type):

    def __init__(self):
        super(DatetimeTimeDeltaType, self).__init__(name=
            'DatetimeTimeDeltaType()')


datetime_timedelta_type = DatetimeTimeDeltaType()


@typeof_impl.register(datetime.timedelta)
def typeof_datetime_timedelta(val, c):
    return datetime_timedelta_type


@register_model(DatetimeTimeDeltaType)
class DatetimeTimeDeltaModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        dpe__dxz = [('days', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64)]
        super(DatetimeTimeDeltaModel, self).__init__(dmm, fe_type, dpe__dxz)


@box(DatetimeTimeDeltaType)
def box_datetime_timedelta(typ, val, c):
    qxb__aal = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val
        )
    tms__araa = c.pyapi.long_from_longlong(qxb__aal.days)
    uxbc__ols = c.pyapi.long_from_longlong(qxb__aal.seconds)
    kdqeg__jen = c.pyapi.long_from_longlong(qxb__aal.microseconds)
    ygsvk__kah = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        timedelta))
    res = c.pyapi.call_function_objargs(ygsvk__kah, (tms__araa, uxbc__ols,
        kdqeg__jen))
    c.pyapi.decref(tms__araa)
    c.pyapi.decref(uxbc__ols)
    c.pyapi.decref(kdqeg__jen)
    c.pyapi.decref(ygsvk__kah)
    return res


@unbox(DatetimeTimeDeltaType)
def unbox_datetime_timedelta(typ, val, c):
    tms__araa = c.pyapi.object_getattr_string(val, 'days')
    uxbc__ols = c.pyapi.object_getattr_string(val, 'seconds')
    kdqeg__jen = c.pyapi.object_getattr_string(val, 'microseconds')
    rmsq__ijlt = c.pyapi.long_as_longlong(tms__araa)
    zjkxj__vlht = c.pyapi.long_as_longlong(uxbc__ols)
    vzi__hpq = c.pyapi.long_as_longlong(kdqeg__jen)
    qxb__aal = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qxb__aal.days = rmsq__ijlt
    qxb__aal.seconds = zjkxj__vlht
    qxb__aal.microseconds = vzi__hpq
    c.pyapi.decref(tms__araa)
    c.pyapi.decref(uxbc__ols)
    c.pyapi.decref(kdqeg__jen)
    rgzuk__ktrbs = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(qxb__aal._getvalue(), is_error=rgzuk__ktrbs)


@lower_constant(DatetimeTimeDeltaType)
def lower_constant_datetime_timedelta(context, builder, ty, pyval):
    days = context.get_constant(types.int64, pyval.days)
    seconds = context.get_constant(types.int64, pyval.seconds)
    microseconds = context.get_constant(types.int64, pyval.microseconds)
    return lir.Constant.literal_struct([days, seconds, microseconds])


@overload(datetime.timedelta, no_unliteral=True)
def datetime_timedelta(days=0, seconds=0, microseconds=0, milliseconds=0,
    minutes=0, hours=0, weeks=0):

    def impl_timedelta(days=0, seconds=0, microseconds=0, milliseconds=0,
        minutes=0, hours=0, weeks=0):
        d = s = us = 0
        days += weeks * 7
        seconds += minutes * 60 + hours * 3600
        microseconds += milliseconds * 1000
        d = days
        days, seconds = divmod(seconds, 24 * 3600)
        d += days
        s += int(seconds)
        seconds, us = divmod(microseconds, 1000000)
        days, seconds = divmod(seconds, 24 * 3600)
        d += days
        s += seconds
        return init_timedelta(d, s, us)
    return impl_timedelta


@intrinsic
def init_timedelta(typingctx, d, s, us):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        timedelta = cgutils.create_struct_proxy(typ)(context, builder)
        timedelta.days = args[0]
        timedelta.seconds = args[1]
        timedelta.microseconds = args[2]
        return timedelta._getvalue()
    return DatetimeTimeDeltaType()(d, s, us), codegen


make_attribute_wrapper(DatetimeTimeDeltaType, 'days', '_days')
make_attribute_wrapper(DatetimeTimeDeltaType, 'seconds', '_seconds')
make_attribute_wrapper(DatetimeTimeDeltaType, 'microseconds', '_microseconds')


@overload_attribute(DatetimeTimeDeltaType, 'days')
def timedelta_get_days(td):

    def impl(td):
        return td._days
    return impl


@overload_attribute(DatetimeTimeDeltaType, 'seconds')
def timedelta_get_seconds(td):

    def impl(td):
        return td._seconds
    return impl


@overload_attribute(DatetimeTimeDeltaType, 'microseconds')
def timedelta_get_microseconds(td):

    def impl(td):
        return td._microseconds
    return impl


@overload_method(DatetimeTimeDeltaType, 'total_seconds', no_unliteral=True)
def total_seconds(td):

    def impl(td):
        return ((td._days * 86400 + td._seconds) * 10 ** 6 + td._microseconds
            ) / 10 ** 6
    return impl


@overload_method(DatetimeTimeDeltaType, '__hash__', no_unliteral=True)
def __hash__(td):

    def impl(td):
        return hash((td._days, td._seconds, td._microseconds))
    return impl


@register_jitable
def _to_nanoseconds(td):
    return np.int64(((td._days * 86400 + td._seconds) * 1000000 + td.
        _microseconds) * 1000)


@register_jitable
def _to_microseconds(td):
    return (td._days * (24 * 3600) + td._seconds) * 1000000 + td._microseconds


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


@register_jitable
def _getstate(td):
    return td._days, td._seconds, td._microseconds


@register_jitable
def _divide_and_round(a, b):
    oowtd__eeon, gomp__uqbl = divmod(a, b)
    gomp__uqbl *= 2
    joir__duovt = gomp__uqbl > b if b > 0 else gomp__uqbl < b
    if joir__duovt or gomp__uqbl == b and oowtd__eeon % 2 == 1:
        oowtd__eeon += 1
    return oowtd__eeon


_MAXORDINAL = 3652059


def overload_floordiv_operator_dt_timedelta(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return us // _to_microseconds(rhs)
        return impl
    elif lhs == datetime_timedelta_type and rhs == types.int64:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return datetime.timedelta(0, 0, us // rhs)
        return impl


def overload_truediv_operator_dt_timedelta(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return us / _to_microseconds(rhs)
        return impl
    elif lhs == datetime_timedelta_type and rhs == types.int64:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return datetime.timedelta(0, 0, _divide_and_round(us, rhs))
        return impl


def create_cmp_op_overload(op):

    def overload_timedelta_cmp(lhs, rhs):
        if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

            def impl(lhs, rhs):
                tdm__jsdwa = _cmp(_getstate(lhs), _getstate(rhs))
                return op(tdm__jsdwa, 0)
            return impl
    return overload_timedelta_cmp


@overload(operator.neg, no_unliteral=True)
def timedelta_neg(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            return datetime.timedelta(-lhs.days, -lhs.seconds, -lhs.
                microseconds)
        return impl


@overload(operator.pos, no_unliteral=True)
def timedelta_pos(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            return lhs
        return impl


@overload(divmod, no_unliteral=True)
def timedelta_divmod(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            oowtd__eeon, gomp__uqbl = divmod(_to_microseconds(lhs),
                _to_microseconds(rhs))
            return oowtd__eeon, datetime.timedelta(0, 0, gomp__uqbl)
        return impl


@overload(abs, no_unliteral=True)
def timedelta_abs(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            if lhs.days < 0:
                return -lhs
            else:
                return lhs
        return impl


@intrinsic
def cast_numpy_timedelta_to_int(typingctx, val=None):
    assert val in (types.NPTimedelta('ns'), types.int64)

    def codegen(context, builder, signature, args):
        return args[0]
    return types.int64(val), codegen


@overload(bool, no_unliteral=True)
def timedelta_to_bool(timedelta):
    if timedelta != datetime_timedelta_type:
        return
    san__dzgwm = datetime.timedelta(0)

    def impl(timedelta):
        return timedelta != san__dzgwm
    return impl


class DatetimeTimeDeltaArrayType(types.ArrayCompatible):

    def __init__(self):
        super(DatetimeTimeDeltaArrayType, self).__init__(name=
            'DatetimeTimeDeltaArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return datetime_timedelta_type

    def copy(self):
        return DatetimeTimeDeltaArrayType()


datetime_timedelta_array_type = DatetimeTimeDeltaArrayType()
types.datetime_timedelta_array_type = datetime_timedelta_array_type
days_data_type = types.Array(types.int64, 1, 'C')
seconds_data_type = types.Array(types.int64, 1, 'C')
microseconds_data_type = types.Array(types.int64, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(DatetimeTimeDeltaArrayType)
class DatetimeTimeDeltaArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        dpe__dxz = [('days_data', days_data_type), ('seconds_data',
            seconds_data_type), ('microseconds_data',
            microseconds_data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, dpe__dxz)


make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'days_data', '_days_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'seconds_data',
    '_seconds_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'microseconds_data',
    '_microseconds_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'null_bitmap',
    '_null_bitmap')


@overload_method(DatetimeTimeDeltaArrayType, 'copy', no_unliteral=True)
def overload_datetime_timedelta_arr_copy(A):
    return (lambda A: bodo.hiframes.datetime_timedelta_ext.
        init_datetime_timedelta_array(A._days_data.copy(), A._seconds_data.
        copy(), A._microseconds_data.copy(), A._null_bitmap.copy()))


@unbox(DatetimeTimeDeltaArrayType)
def unbox_datetime_timedelta_array(typ, val, c):
    n = bodo.utils.utils.object_length(c, val)
    kxonz__vzsbs = types.Array(types.intp, 1, 'C')
    cei__qmp = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        kxonz__vzsbs, [n])
    nwzec__rsjtg = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        kxonz__vzsbs, [n])
    uxr__qhbwg = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        kxonz__vzsbs, [n])
    fwo__vmvau = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    alrj__vtz = bodo.utils.utils._empty_nd_impl(c.context, c.builder, types
        .Array(types.uint8, 1, 'C'), [fwo__vmvau])
    mch__nbihg = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64), lir.IntType(64).as_pointer(), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (8).as_pointer()])
    ere__pyy = cgutils.get_or_insert_function(c.builder.module, mch__nbihg,
        name='unbox_datetime_timedelta_array')
    c.builder.call(ere__pyy, [val, n, cei__qmp.data, nwzec__rsjtg.data,
        uxr__qhbwg.data, alrj__vtz.data])
    zhjna__hjth = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    zhjna__hjth.days_data = cei__qmp._getvalue()
    zhjna__hjth.seconds_data = nwzec__rsjtg._getvalue()
    zhjna__hjth.microseconds_data = uxr__qhbwg._getvalue()
    zhjna__hjth.null_bitmap = alrj__vtz._getvalue()
    rgzuk__ktrbs = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(zhjna__hjth._getvalue(), is_error=rgzuk__ktrbs)


@box(DatetimeTimeDeltaArrayType)
def box_datetime_timedelta_array(typ, val, c):
    uaq__zyqro = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    cei__qmp = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, uaq__zyqro.days_data)
    nwzec__rsjtg = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
        .context, c.builder, uaq__zyqro.seconds_data).data
    uxr__qhbwg = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, uaq__zyqro.microseconds_data).data
    dzr__bll = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, uaq__zyqro.null_bitmap).data
    n = c.builder.extract_value(cei__qmp.shape, 0)
    mch__nbihg = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (64).as_pointer(), lir.IntType(8).as_pointer()])
    nxd__qjx = cgutils.get_or_insert_function(c.builder.module, mch__nbihg,
        name='box_datetime_timedelta_array')
    xskra__hfqpd = c.builder.call(nxd__qjx, [n, cei__qmp.data, nwzec__rsjtg,
        uxr__qhbwg, dzr__bll])
    c.context.nrt.decref(c.builder, typ, val)
    return xskra__hfqpd


@intrinsic
def init_datetime_timedelta_array(typingctx, days_data, seconds_data,
    microseconds_data, nulls=None):
    assert days_data == types.Array(types.int64, 1, 'C')
    assert seconds_data == types.Array(types.int64, 1, 'C')
    assert microseconds_data == types.Array(types.int64, 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        vpohr__flwhg, ila__xul, yan__tih, ubhwq__wvolb = args
        ulbux__nloqy = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        ulbux__nloqy.days_data = vpohr__flwhg
        ulbux__nloqy.seconds_data = ila__xul
        ulbux__nloqy.microseconds_data = yan__tih
        ulbux__nloqy.null_bitmap = ubhwq__wvolb
        context.nrt.incref(builder, signature.args[0], vpohr__flwhg)
        context.nrt.incref(builder, signature.args[1], ila__xul)
        context.nrt.incref(builder, signature.args[2], yan__tih)
        context.nrt.incref(builder, signature.args[3], ubhwq__wvolb)
        return ulbux__nloqy._getvalue()
    rros__idb = datetime_timedelta_array_type(days_data, seconds_data,
        microseconds_data, nulls)
    return rros__idb, codegen


@lower_constant(DatetimeTimeDeltaArrayType)
def lower_constant_datetime_timedelta_arr(context, builder, typ, pyval):
    n = len(pyval)
    cei__qmp = np.empty(n, np.int64)
    nwzec__rsjtg = np.empty(n, np.int64)
    uxr__qhbwg = np.empty(n, np.int64)
    tddp__fparw = np.empty(n + 7 >> 3, np.uint8)
    for etd__ffgu, s in enumerate(pyval):
        xieyc__bac = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(tddp__fparw, etd__ffgu, int(
            not xieyc__bac))
        if not xieyc__bac:
            cei__qmp[etd__ffgu] = s.days
            nwzec__rsjtg[etd__ffgu] = s.seconds
            uxr__qhbwg[etd__ffgu] = s.microseconds
    pcdnq__amquu = context.get_constant_generic(builder, days_data_type,
        cei__qmp)
    ebn__cov = context.get_constant_generic(builder, seconds_data_type,
        nwzec__rsjtg)
    tbhl__rhbjd = context.get_constant_generic(builder,
        microseconds_data_type, uxr__qhbwg)
    paut__vlvd = context.get_constant_generic(builder, nulls_type, tddp__fparw)
    return lir.Constant.literal_struct([pcdnq__amquu, ebn__cov, tbhl__rhbjd,
        paut__vlvd])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_timedelta_array(n):
    cei__qmp = np.empty(n, dtype=np.int64)
    nwzec__rsjtg = np.empty(n, dtype=np.int64)
    uxr__qhbwg = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_timedelta_array(cei__qmp, nwzec__rsjtg, uxr__qhbwg,
        nulls)


def alloc_datetime_timedelta_array_equiv(self, scope, equiv_set, loc, args, kws
    ):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_datetime_timedelta_ext_alloc_datetime_timedelta_array
    ) = alloc_datetime_timedelta_array_equiv


@overload(operator.getitem, no_unliteral=True)
def dt_timedelta_arr_getitem(A, ind):
    if A != datetime_timedelta_array_type:
        return
    if isinstance(ind, types.Integer):

        def impl_int(A, ind):
            return datetime.timedelta(days=A._days_data[ind], seconds=A.
                _seconds_data[ind], microseconds=A._microseconds_data[ind])
        return impl_int
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            arhqt__zffdx = bodo.utils.conversion.coerce_to_ndarray(ind)
            tbs__toy = A._null_bitmap
            fggm__yalve = A._days_data[arhqt__zffdx]
            emzn__uqh = A._seconds_data[arhqt__zffdx]
            qhm__zweux = A._microseconds_data[arhqt__zffdx]
            n = len(fggm__yalve)
            qme__eyw = get_new_null_mask_bool_index(tbs__toy, ind, n)
            return init_datetime_timedelta_array(fggm__yalve, emzn__uqh,
                qhm__zweux, qme__eyw)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            arhqt__zffdx = bodo.utils.conversion.coerce_to_ndarray(ind)
            tbs__toy = A._null_bitmap
            fggm__yalve = A._days_data[arhqt__zffdx]
            emzn__uqh = A._seconds_data[arhqt__zffdx]
            qhm__zweux = A._microseconds_data[arhqt__zffdx]
            n = len(fggm__yalve)
            qme__eyw = get_new_null_mask_int_index(tbs__toy, arhqt__zffdx, n)
            return init_datetime_timedelta_array(fggm__yalve, emzn__uqh,
                qhm__zweux, qme__eyw)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            n = len(A._days_data)
            tbs__toy = A._null_bitmap
            fggm__yalve = np.ascontiguousarray(A._days_data[ind])
            emzn__uqh = np.ascontiguousarray(A._seconds_data[ind])
            qhm__zweux = np.ascontiguousarray(A._microseconds_data[ind])
            qme__eyw = get_new_null_mask_slice_index(tbs__toy, ind, n)
            return init_datetime_timedelta_array(fggm__yalve, emzn__uqh,
                qhm__zweux, qme__eyw)
        return impl_slice
    raise BodoError(
        f'getitem for DatetimeTimedeltaArray with indexing type {ind} not supported.'
        )


@overload(operator.setitem, no_unliteral=True)
def dt_timedelta_arr_setitem(A, ind, val):
    if A != datetime_timedelta_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    dxqz__bfoya = (
        f"setitem for DatetimeTimedeltaArray with indexing type {ind} received an incorrect 'value' type {val}."
        )
    if isinstance(ind, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl(A, ind, val):
                A._days_data[ind] = val._days
                A._seconds_data[ind] = val._seconds
                A._microseconds_data[ind] = val._microseconds
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, ind, 1)
            return impl
        else:
            raise BodoError(dxqz__bfoya)
    if not (is_iterable_type(val) and val.dtype == bodo.
        datetime_timedelta_type or types.unliteral(val) ==
        datetime_timedelta_type):
        raise BodoError(dxqz__bfoya)
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_arr_ind_scalar(A, ind, val):
                n = len(A)
                for etd__ffgu in range(n):
                    A._days_data[ind[etd__ffgu]] = val._days
                    A._seconds_data[ind[etd__ffgu]] = val._seconds
                    A._microseconds_data[ind[etd__ffgu]] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[etd__ffgu], 1)
            return impl_arr_ind_scalar
        else:

            def impl_arr_ind(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(val._days_data)
                for etd__ffgu in range(n):
                    A._days_data[ind[etd__ffgu]] = val._days_data[etd__ffgu]
                    A._seconds_data[ind[etd__ffgu]] = val._seconds_data[
                        etd__ffgu]
                    A._microseconds_data[ind[etd__ffgu]
                        ] = val._microseconds_data[etd__ffgu]
                    blp__twil = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                        ._null_bitmap, etd__ffgu)
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[etd__ffgu], blp__twil)
            return impl_arr_ind
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_bool_ind_mask_scalar(A, ind, val):
                n = len(ind)
                for etd__ffgu in range(n):
                    if not bodo.libs.array_kernels.isna(ind, etd__ffgu
                        ) and ind[etd__ffgu]:
                        A._days_data[etd__ffgu] = val._days
                        A._seconds_data[etd__ffgu] = val._seconds
                        A._microseconds_data[etd__ffgu] = val._microseconds
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            etd__ffgu, 1)
            return impl_bool_ind_mask_scalar
        else:

            def impl_bool_ind_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(ind)
                imn__gmdze = 0
                for etd__ffgu in range(n):
                    if not bodo.libs.array_kernels.isna(ind, etd__ffgu
                        ) and ind[etd__ffgu]:
                        A._days_data[etd__ffgu] = val._days_data[imn__gmdze]
                        A._seconds_data[etd__ffgu] = val._seconds_data[
                            imn__gmdze]
                        A._microseconds_data[etd__ffgu
                            ] = val._microseconds_data[imn__gmdze]
                        blp__twil = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                            val._null_bitmap, imn__gmdze)
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            etd__ffgu, blp__twil)
                        imn__gmdze += 1
            return impl_bool_ind_mask
    if isinstance(ind, types.SliceType):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_slice_scalar(A, ind, val):
                cbeah__tfssi = numba.cpython.unicode._normalize_slice(ind,
                    len(A))
                for etd__ffgu in range(cbeah__tfssi.start, cbeah__tfssi.
                    stop, cbeah__tfssi.step):
                    A._days_data[etd__ffgu] = val._days
                    A._seconds_data[etd__ffgu] = val._seconds
                    A._microseconds_data[etd__ffgu] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        etd__ffgu, 1)
            return impl_slice_scalar
        else:

            def impl_slice_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(A._days_data)
                A._days_data[ind] = val._days_data
                A._seconds_data[ind] = val._seconds_data
                A._microseconds_data[ind] = val._microseconds_data
                agm__zvqc = val._null_bitmap.copy()
                setitem_slice_index_null_bits(A._null_bitmap, agm__zvqc, ind, n
                    )
            return impl_slice_mask
    raise BodoError(
        f'setitem for DatetimeTimedeltaArray with indexing type {ind} not supported.'
        )


@overload(len, no_unliteral=True)
def overload_len_datetime_timedelta_arr(A):
    if A == datetime_timedelta_array_type:
        return lambda A: len(A._days_data)


@overload_attribute(DatetimeTimeDeltaArrayType, 'shape')
def overload_datetime_timedelta_arr_shape(A):
    return lambda A: (len(A._days_data),)


@overload_attribute(DatetimeTimeDeltaArrayType, 'nbytes')
def timedelta_arr_nbytes_overload(A):
    return (lambda A: A._days_data.nbytes + A._seconds_data.nbytes + A.
        _microseconds_data.nbytes + A._null_bitmap.nbytes)


def overload_datetime_timedelta_arr_sub(arg1, arg2):
    if (arg1 == datetime_timedelta_array_type and arg2 ==
        datetime_timedelta_type):

        def impl(arg1, arg2):
            uaq__zyqro = arg1
            numba.parfors.parfor.init_prange()
            n = len(uaq__zyqro)
            A = alloc_datetime_timedelta_array(n)
            for etd__ffgu in numba.parfors.parfor.internal_prange(n):
                A[etd__ffgu] = uaq__zyqro[etd__ffgu] - arg2
            return A
        return impl


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            jsmm__neg = True
        else:
            jsmm__neg = False
        if (lhs == datetime_timedelta_array_type and rhs ==
            datetime_timedelta_array_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                qtta__zui = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for etd__ffgu in numba.parfors.parfor.internal_prange(n):
                    akh__xpo = bodo.libs.array_kernels.isna(lhs, etd__ffgu)
                    opak__ldjz = bodo.libs.array_kernels.isna(rhs, etd__ffgu)
                    if akh__xpo or opak__ldjz:
                        vhpp__blb = jsmm__neg
                    else:
                        vhpp__blb = op(lhs[etd__ffgu], rhs[etd__ffgu])
                    qtta__zui[etd__ffgu] = vhpp__blb
                return qtta__zui
            return impl
        elif lhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                qtta__zui = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for etd__ffgu in numba.parfors.parfor.internal_prange(n):
                    blp__twil = bodo.libs.array_kernels.isna(lhs, etd__ffgu)
                    if blp__twil:
                        vhpp__blb = jsmm__neg
                    else:
                        vhpp__blb = op(lhs[etd__ffgu], rhs)
                    qtta__zui[etd__ffgu] = vhpp__blb
                return qtta__zui
            return impl
        elif rhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                qtta__zui = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for etd__ffgu in numba.parfors.parfor.internal_prange(n):
                    blp__twil = bodo.libs.array_kernels.isna(rhs, etd__ffgu)
                    if blp__twil:
                        vhpp__blb = jsmm__neg
                    else:
                        vhpp__blb = op(lhs, rhs[etd__ffgu])
                    qtta__zui[etd__ffgu] = vhpp__blb
                return qtta__zui
            return impl
    return overload_date_arr_cmp


timedelta_unsupported_attrs = ['asm8', 'resolution_string', 'freq',
    'is_populated']
timedelta_unsupported_methods = ['isoformat']


def _intstall_pd_timedelta_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for unk__vfawi in timedelta_unsupported_attrs:
        zin__dsae = 'pandas.Timedelta.' + unk__vfawi
        overload_attribute(PDTimeDeltaType, unk__vfawi)(
            create_unsupported_overload(zin__dsae))
    for pwk__mdsex in timedelta_unsupported_methods:
        zin__dsae = 'pandas.Timedelta.' + pwk__mdsex
        overload_method(PDTimeDeltaType, pwk__mdsex)(
            create_unsupported_overload(zin__dsae + '()'))


_intstall_pd_timedelta_unsupported()
