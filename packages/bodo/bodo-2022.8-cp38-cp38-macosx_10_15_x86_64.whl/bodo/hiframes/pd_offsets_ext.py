"""
Implement support for the various classes in pd.tseries.offsets.
"""
import operator
import llvmlite.binding as ll
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.hiframes.pd_timestamp_ext import get_days_in_month, pd_timestamp_type
from bodo.libs import hdatetime_ext
from bodo.utils.typing import BodoError, create_unsupported_overload, is_overload_none
ll.add_symbol('box_date_offset', hdatetime_ext.box_date_offset)
ll.add_symbol('unbox_date_offset', hdatetime_ext.unbox_date_offset)


class MonthBeginType(types.Type):

    def __init__(self):
        super(MonthBeginType, self).__init__(name='MonthBeginType()')


month_begin_type = MonthBeginType()


@typeof_impl.register(pd.tseries.offsets.MonthBegin)
def typeof_month_begin(val, c):
    return month_begin_type


@register_model(MonthBeginType)
class MonthBeginModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        grxy__dxebj = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, grxy__dxebj)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    uow__yedat = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    rfwlw__cznj = c.pyapi.long_from_longlong(uow__yedat.n)
    xustd__qepz = c.pyapi.from_native_value(types.boolean, uow__yedat.
        normalize, c.env_manager)
    tusrm__pbr = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    xvb__sdnn = c.pyapi.call_function_objargs(tusrm__pbr, (rfwlw__cznj,
        xustd__qepz))
    c.pyapi.decref(rfwlw__cznj)
    c.pyapi.decref(xustd__qepz)
    c.pyapi.decref(tusrm__pbr)
    return xvb__sdnn


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    rfwlw__cznj = c.pyapi.object_getattr_string(val, 'n')
    xustd__qepz = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(rfwlw__cznj)
    normalize = c.pyapi.to_native_value(types.bool_, xustd__qepz).value
    uow__yedat = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    uow__yedat.n = n
    uow__yedat.normalize = normalize
    c.pyapi.decref(rfwlw__cznj)
    c.pyapi.decref(xustd__qepz)
    xzw__qpl = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(uow__yedat._getvalue(), is_error=xzw__qpl)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        uow__yedat = cgutils.create_struct_proxy(typ)(context, builder)
        uow__yedat.n = args[0]
        uow__yedat.normalize = args[1]
        return uow__yedat._getvalue()
    return MonthBeginType()(n, normalize), codegen


make_attribute_wrapper(MonthBeginType, 'n', 'n')
make_attribute_wrapper(MonthBeginType, 'normalize', 'normalize')


@register_jitable
def calculate_month_begin_date(year, month, day, n):
    if n <= 0:
        if day > 1:
            n += 1
    month = month + n
    month -= 1
    year += month // 12
    month = month % 12 + 1
    day = 1
    return year, month, day


def overload_add_operator_month_begin_offset_type(lhs, rhs):
    if lhs == month_begin_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond)
        return impl
    if lhs == month_begin_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond)
        return impl
    if lhs == month_begin_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            return pd.Timestamp(year=year, month=month, day=day)
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == month_begin_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


class MonthEndType(types.Type):

    def __init__(self):
        super(MonthEndType, self).__init__(name='MonthEndType()')


month_end_type = MonthEndType()


@typeof_impl.register(pd.tseries.offsets.MonthEnd)
def typeof_month_end(val, c):
    return month_end_type


@register_model(MonthEndType)
class MonthEndModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        grxy__dxebj = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, grxy__dxebj)


@box(MonthEndType)
def box_month_end(typ, val, c):
    ldg__hdc = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val
        )
    rfwlw__cznj = c.pyapi.long_from_longlong(ldg__hdc.n)
    xustd__qepz = c.pyapi.from_native_value(types.boolean, ldg__hdc.
        normalize, c.env_manager)
    wocl__glhf = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    xvb__sdnn = c.pyapi.call_function_objargs(wocl__glhf, (rfwlw__cznj,
        xustd__qepz))
    c.pyapi.decref(rfwlw__cznj)
    c.pyapi.decref(xustd__qepz)
    c.pyapi.decref(wocl__glhf)
    return xvb__sdnn


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    rfwlw__cznj = c.pyapi.object_getattr_string(val, 'n')
    xustd__qepz = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(rfwlw__cznj)
    normalize = c.pyapi.to_native_value(types.bool_, xustd__qepz).value
    ldg__hdc = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ldg__hdc.n = n
    ldg__hdc.normalize = normalize
    c.pyapi.decref(rfwlw__cznj)
    c.pyapi.decref(xustd__qepz)
    xzw__qpl = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ldg__hdc._getvalue(), is_error=xzw__qpl)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        ldg__hdc = cgutils.create_struct_proxy(typ)(context, builder)
        ldg__hdc.n = args[0]
        ldg__hdc.normalize = args[1]
        return ldg__hdc._getvalue()
    return MonthEndType()(n, normalize), codegen


make_attribute_wrapper(MonthEndType, 'n', 'n')
make_attribute_wrapper(MonthEndType, 'normalize', 'normalize')


@lower_constant(MonthBeginType)
@lower_constant(MonthEndType)
def lower_constant_month_end(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    return lir.Constant.literal_struct([n, normalize])


@register_jitable
def calculate_month_end_date(year, month, day, n):
    if n > 0:
        ldg__hdc = get_days_in_month(year, month)
        if ldg__hdc > day:
            n -= 1
    month = month + n
    month -= 1
    year += month // 12
    month = month % 12 + 1
    day = get_days_in_month(year, month)
    return year, month, day


def overload_add_operator_month_end_offset_type(lhs, rhs):
    if lhs == month_end_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond)
        return impl
    if lhs == month_end_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond)
        return impl
    if lhs == month_end_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            return pd.Timestamp(year=year, month=month, day=day)
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == month_end_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def overload_mul_date_offset_types(lhs, rhs):
    if lhs == month_begin_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.MonthBegin(lhs.n * rhs, lhs.normalize)
    if lhs == month_end_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.MonthEnd(lhs.n * rhs, lhs.normalize)
    if lhs == week_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.Week(lhs.n * rhs, lhs.normalize, lhs.
                weekday)
    if lhs == date_offset_type:

        def impl(lhs, rhs):
            n = lhs.n * rhs
            normalize = lhs.normalize
            if lhs._has_kws:
                years = lhs._years
                months = lhs._months
                weeks = lhs._weeks
                days = lhs._days
                hours = lhs._hours
                minutes = lhs._minutes
                seconds = lhs._seconds
                microseconds = lhs._microseconds
                year = lhs._year
                month = lhs._month
                day = lhs._day
                weekday = lhs._weekday
                hour = lhs._hour
                minute = lhs._minute
                second = lhs._second
                microsecond = lhs._microsecond
                nanoseconds = lhs._nanoseconds
                nanosecond = lhs._nanosecond
                return pd.tseries.offsets.DateOffset(n, normalize, years,
                    months, weeks, days, hours, minutes, seconds,
                    microseconds, nanoseconds, year, month, day, weekday,
                    hour, minute, second, microsecond, nanosecond)
            else:
                return pd.tseries.offsets.DateOffset(n, normalize)
    if rhs in [week_type, month_end_type, month_begin_type, date_offset_type]:

        def impl(lhs, rhs):
            return rhs * lhs
        return impl
    return impl


class DateOffsetType(types.Type):

    def __init__(self):
        super(DateOffsetType, self).__init__(name='DateOffsetType()')


date_offset_type = DateOffsetType()
date_offset_fields = ['years', 'months', 'weeks', 'days', 'hours',
    'minutes', 'seconds', 'microseconds', 'nanoseconds', 'year', 'month',
    'day', 'weekday', 'hour', 'minute', 'second', 'microsecond', 'nanosecond']


@typeof_impl.register(pd.tseries.offsets.DateOffset)
def type_of_date_offset(val, c):
    return date_offset_type


@register_model(DateOffsetType)
class DateOffsetModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        grxy__dxebj = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, grxy__dxebj)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    cbfsz__frc = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    kyzq__ywd = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for ipo__dxvef, vhndr__rot in enumerate(date_offset_fields):
        c.builder.store(getattr(cbfsz__frc, vhndr__rot), c.builder.inttoptr
            (c.builder.add(c.builder.ptrtoint(kyzq__ywd, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * ipo__dxvef)), lir.IntType(64)
            .as_pointer()))
    voncm__kpyb = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    fjsub__qtaku = cgutils.get_or_insert_function(c.builder.module,
        voncm__kpyb, name='box_date_offset')
    nksi__mdop = c.builder.call(fjsub__qtaku, [cbfsz__frc.n, cbfsz__frc.
        normalize, kyzq__ywd, cbfsz__frc.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return nksi__mdop


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    rfwlw__cznj = c.pyapi.object_getattr_string(val, 'n')
    xustd__qepz = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(rfwlw__cznj)
    normalize = c.pyapi.to_native_value(types.bool_, xustd__qepz).value
    kyzq__ywd = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    voncm__kpyb = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer()])
    iky__vjbrg = cgutils.get_or_insert_function(c.builder.module,
        voncm__kpyb, name='unbox_date_offset')
    has_kws = c.builder.call(iky__vjbrg, [val, kyzq__ywd])
    cbfsz__frc = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    cbfsz__frc.n = n
    cbfsz__frc.normalize = normalize
    for ipo__dxvef, vhndr__rot in enumerate(date_offset_fields):
        setattr(cbfsz__frc, vhndr__rot, c.builder.load(c.builder.inttoptr(c
            .builder.add(c.builder.ptrtoint(kyzq__ywd, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * ipo__dxvef)), lir.IntType(64)
            .as_pointer())))
    cbfsz__frc.has_kws = has_kws
    c.pyapi.decref(rfwlw__cznj)
    c.pyapi.decref(xustd__qepz)
    xzw__qpl = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cbfsz__frc._getvalue(), is_error=xzw__qpl)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    bkh__kva = [n, normalize]
    has_kws = False
    ezbp__iccw = [0] * 9 + [-1] * 9
    for ipo__dxvef, vhndr__rot in enumerate(date_offset_fields):
        if hasattr(pyval, vhndr__rot):
            zfec__nvbm = context.get_constant(types.int64, getattr(pyval,
                vhndr__rot))
            has_kws = True
        else:
            zfec__nvbm = context.get_constant(types.int64, ezbp__iccw[
                ipo__dxvef])
        bkh__kva.append(zfec__nvbm)
    has_kws = context.get_constant(types.boolean, has_kws)
    bkh__kva.append(has_kws)
    return lir.Constant.literal_struct(bkh__kva)


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    wef__thiz = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for zjv__nxxjp in wef__thiz:
        if not is_overload_none(zjv__nxxjp):
            has_kws = True
            break

    def impl(n=1, normalize=False, years=None, months=None, weeks=None,
        days=None, hours=None, minutes=None, seconds=None, microseconds=
        None, nanoseconds=None, year=None, month=None, day=None, weekday=
        None, hour=None, minute=None, second=None, microsecond=None,
        nanosecond=None):
        years = 0 if years is None else years
        months = 0 if months is None else months
        weeks = 0 if weeks is None else weeks
        days = 0 if days is None else days
        hours = 0 if hours is None else hours
        minutes = 0 if minutes is None else minutes
        seconds = 0 if seconds is None else seconds
        microseconds = 0 if microseconds is None else microseconds
        nanoseconds = 0 if nanoseconds is None else nanoseconds
        year = -1 if year is None else year
        month = -1 if month is None else month
        weekday = -1 if weekday is None else weekday
        day = -1 if day is None else day
        hour = -1 if hour is None else hour
        minute = -1 if minute is None else minute
        second = -1 if second is None else second
        microsecond = -1 if microsecond is None else microsecond
        nanosecond = -1 if nanosecond is None else nanosecond
        return init_date_offset(n, normalize, years, months, weeks, days,
            hours, minutes, seconds, microseconds, nanoseconds, year, month,
            day, weekday, hour, minute, second, microsecond, nanosecond,
            has_kws)
    return impl


@intrinsic
def init_date_offset(typingctx, n, normalize, years, months, weeks, days,
    hours, minutes, seconds, microseconds, nanoseconds, year, month, day,
    weekday, hour, minute, second, microsecond, nanosecond, has_kws):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        cbfsz__frc = cgutils.create_struct_proxy(typ)(context, builder)
        cbfsz__frc.n = args[0]
        cbfsz__frc.normalize = args[1]
        cbfsz__frc.years = args[2]
        cbfsz__frc.months = args[3]
        cbfsz__frc.weeks = args[4]
        cbfsz__frc.days = args[5]
        cbfsz__frc.hours = args[6]
        cbfsz__frc.minutes = args[7]
        cbfsz__frc.seconds = args[8]
        cbfsz__frc.microseconds = args[9]
        cbfsz__frc.nanoseconds = args[10]
        cbfsz__frc.year = args[11]
        cbfsz__frc.month = args[12]
        cbfsz__frc.day = args[13]
        cbfsz__frc.weekday = args[14]
        cbfsz__frc.hour = args[15]
        cbfsz__frc.minute = args[16]
        cbfsz__frc.second = args[17]
        cbfsz__frc.microsecond = args[18]
        cbfsz__frc.nanosecond = args[19]
        cbfsz__frc.has_kws = args[20]
        return cbfsz__frc._getvalue()
    return DateOffsetType()(n, normalize, years, months, weeks, days, hours,
        minutes, seconds, microseconds, nanoseconds, year, month, day,
        weekday, hour, minute, second, microsecond, nanosecond, has_kws
        ), codegen


make_attribute_wrapper(DateOffsetType, 'n', 'n')
make_attribute_wrapper(DateOffsetType, 'normalize', 'normalize')
make_attribute_wrapper(DateOffsetType, 'years', '_years')
make_attribute_wrapper(DateOffsetType, 'months', '_months')
make_attribute_wrapper(DateOffsetType, 'weeks', '_weeks')
make_attribute_wrapper(DateOffsetType, 'days', '_days')
make_attribute_wrapper(DateOffsetType, 'hours', '_hours')
make_attribute_wrapper(DateOffsetType, 'minutes', '_minutes')
make_attribute_wrapper(DateOffsetType, 'seconds', '_seconds')
make_attribute_wrapper(DateOffsetType, 'microseconds', '_microseconds')
make_attribute_wrapper(DateOffsetType, 'nanoseconds', '_nanoseconds')
make_attribute_wrapper(DateOffsetType, 'year', '_year')
make_attribute_wrapper(DateOffsetType, 'month', '_month')
make_attribute_wrapper(DateOffsetType, 'weekday', '_weekday')
make_attribute_wrapper(DateOffsetType, 'day', '_day')
make_attribute_wrapper(DateOffsetType, 'hour', '_hour')
make_attribute_wrapper(DateOffsetType, 'minute', '_minute')
make_attribute_wrapper(DateOffsetType, 'second', '_second')
make_attribute_wrapper(DateOffsetType, 'microsecond', '_microsecond')
make_attribute_wrapper(DateOffsetType, 'nanosecond', '_nanosecond')
make_attribute_wrapper(DateOffsetType, 'has_kws', '_has_kws')


@register_jitable
def relative_delta_addition(dateoffset, ts):
    if dateoffset._has_kws:
        gsr__rly = -1 if dateoffset.n < 0 else 1
        for dwh__brkvt in range(np.abs(dateoffset.n)):
            year = ts.year
            month = ts.month
            day = ts.day
            hour = ts.hour
            minute = ts.minute
            second = ts.second
            microsecond = ts.microsecond
            nanosecond = ts.nanosecond
            if dateoffset._year != -1:
                year = dateoffset._year
            year += gsr__rly * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += gsr__rly * dateoffset._months
            year, month, vzlh__yxlcs = calculate_month_end_date(year, month,
                day, 0)
            if day > vzlh__yxlcs:
                day = vzlh__yxlcs
            if dateoffset._day != -1:
                day = dateoffset._day
            if dateoffset._hour != -1:
                hour = dateoffset._hour
            if dateoffset._minute != -1:
                minute = dateoffset._minute
            if dateoffset._second != -1:
                second = dateoffset._second
            if dateoffset._microsecond != -1:
                microsecond = dateoffset._microsecond
            if dateoffset._nanosecond != -1:
                nanosecond = dateoffset._nanosecond
            ts = pd.Timestamp(year=year, month=month, day=day, hour=hour,
                minute=minute, second=second, microsecond=microsecond,
                nanosecond=nanosecond)
            ufsh__juw = pd.Timedelta(days=dateoffset._days + 7 * dateoffset
                ._weeks, hours=dateoffset._hours, minutes=dateoffset.
                _minutes, seconds=dateoffset._seconds, microseconds=
                dateoffset._microseconds)
            ufsh__juw = ufsh__juw + pd.Timedelta(dateoffset._nanoseconds,
                unit='ns')
            if gsr__rly == -1:
                ufsh__juw = -ufsh__juw
            ts = ts + ufsh__juw
            if dateoffset._weekday != -1:
                opfm__htyqm = ts.weekday()
                hllfu__avxzw = (dateoffset._weekday - opfm__htyqm) % 7
                ts = ts + pd.Timedelta(days=hllfu__avxzw)
        return ts
    else:
        return pd.Timedelta(days=dateoffset.n) + ts


def overload_add_operator_date_offset_type(lhs, rhs):
    if lhs == date_offset_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            ts = relative_delta_addition(lhs, rhs)
            if lhs.normalize:
                return ts.normalize()
            return ts
        return impl
    if lhs == date_offset_type and rhs in [datetime_date_type,
        datetime_datetime_type]:

        def impl(lhs, rhs):
            ts = relative_delta_addition(lhs, pd.Timestamp(rhs))
            if lhs.normalize:
                return ts.normalize()
            return ts
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == date_offset_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def overload_sub_operator_offsets(lhs, rhs):
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs in [date_offset_type, month_begin_type, month_end_type,
        week_type]:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl


@overload(operator.neg, no_unliteral=True)
def overload_neg(lhs):
    if lhs == month_begin_type:

        def impl(lhs):
            return pd.tseries.offsets.MonthBegin(-lhs.n, lhs.normalize)
    elif lhs == month_end_type:

        def impl(lhs):
            return pd.tseries.offsets.MonthEnd(-lhs.n, lhs.normalize)
    elif lhs == week_type:

        def impl(lhs):
            return pd.tseries.offsets.Week(-lhs.n, lhs.normalize, lhs.weekday)
    elif lhs == date_offset_type:

        def impl(lhs):
            n = -lhs.n
            normalize = lhs.normalize
            if lhs._has_kws:
                years = lhs._years
                months = lhs._months
                weeks = lhs._weeks
                days = lhs._days
                hours = lhs._hours
                minutes = lhs._minutes
                seconds = lhs._seconds
                microseconds = lhs._microseconds
                year = lhs._year
                month = lhs._month
                day = lhs._day
                weekday = lhs._weekday
                hour = lhs._hour
                minute = lhs._minute
                second = lhs._second
                microsecond = lhs._microsecond
                nanoseconds = lhs._nanoseconds
                nanosecond = lhs._nanosecond
                return pd.tseries.offsets.DateOffset(n, normalize, years,
                    months, weeks, days, hours, minutes, seconds,
                    microseconds, nanoseconds, year, month, day, weekday,
                    hour, minute, second, microsecond, nanosecond)
            else:
                return pd.tseries.offsets.DateOffset(n, normalize)
    else:
        return
    return impl


def is_offsets_type(val):
    return val in [date_offset_type, month_begin_type, month_end_type,
        week_type]


class WeekType(types.Type):

    def __init__(self):
        super(WeekType, self).__init__(name='WeekType()')


week_type = WeekType()


@typeof_impl.register(pd.tseries.offsets.Week)
def typeof_week(val, c):
    return week_type


@register_model(WeekType)
class WeekModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        grxy__dxebj = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, grxy__dxebj)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        qnjsz__vheg = -1 if weekday is None else weekday
        return init_week(n, normalize, qnjsz__vheg)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        blmgv__ovwrg = cgutils.create_struct_proxy(typ)(context, builder)
        blmgv__ovwrg.n = args[0]
        blmgv__ovwrg.normalize = args[1]
        blmgv__ovwrg.weekday = args[2]
        return blmgv__ovwrg._getvalue()
    return WeekType()(n, normalize, weekday), codegen


@lower_constant(WeekType)
def lower_constant_week(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    if pyval.weekday is not None:
        weekday = context.get_constant(types.int64, pyval.weekday)
    else:
        weekday = context.get_constant(types.int64, -1)
    return lir.Constant.literal_struct([n, normalize, weekday])


@box(WeekType)
def box_week(typ, val, c):
    blmgv__ovwrg = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    rfwlw__cznj = c.pyapi.long_from_longlong(blmgv__ovwrg.n)
    xustd__qepz = c.pyapi.from_native_value(types.boolean, blmgv__ovwrg.
        normalize, c.env_manager)
    ngynt__kbaeq = c.pyapi.long_from_longlong(blmgv__ovwrg.weekday)
    joci__qudv = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    insii__wcdg = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64),
        -1), blmgv__ovwrg.weekday)
    with c.builder.if_else(insii__wcdg) as (jzo__eepw, dmr__nvzeq):
        with jzo__eepw:
            vdend__dwtnl = c.pyapi.call_function_objargs(joci__qudv, (
                rfwlw__cznj, xustd__qepz, ngynt__kbaeq))
            fsy__pmnuw = c.builder.block
        with dmr__nvzeq:
            sgpus__vqg = c.pyapi.call_function_objargs(joci__qudv, (
                rfwlw__cznj, xustd__qepz))
            cktnd__bqe = c.builder.block
    xvb__sdnn = c.builder.phi(vdend__dwtnl.type)
    xvb__sdnn.add_incoming(vdend__dwtnl, fsy__pmnuw)
    xvb__sdnn.add_incoming(sgpus__vqg, cktnd__bqe)
    c.pyapi.decref(ngynt__kbaeq)
    c.pyapi.decref(rfwlw__cznj)
    c.pyapi.decref(xustd__qepz)
    c.pyapi.decref(joci__qudv)
    return xvb__sdnn


@unbox(WeekType)
def unbox_week(typ, val, c):
    rfwlw__cznj = c.pyapi.object_getattr_string(val, 'n')
    xustd__qepz = c.pyapi.object_getattr_string(val, 'normalize')
    ngynt__kbaeq = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(rfwlw__cznj)
    normalize = c.pyapi.to_native_value(types.bool_, xustd__qepz).value
    txybk__mdlv = c.pyapi.make_none()
    ekus__oxkhw = c.builder.icmp_unsigned('==', ngynt__kbaeq, txybk__mdlv)
    with c.builder.if_else(ekus__oxkhw) as (dmr__nvzeq, jzo__eepw):
        with jzo__eepw:
            vdend__dwtnl = c.pyapi.long_as_longlong(ngynt__kbaeq)
            fsy__pmnuw = c.builder.block
        with dmr__nvzeq:
            sgpus__vqg = lir.Constant(lir.IntType(64), -1)
            cktnd__bqe = c.builder.block
    xvb__sdnn = c.builder.phi(vdend__dwtnl.type)
    xvb__sdnn.add_incoming(vdend__dwtnl, fsy__pmnuw)
    xvb__sdnn.add_incoming(sgpus__vqg, cktnd__bqe)
    blmgv__ovwrg = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    blmgv__ovwrg.n = n
    blmgv__ovwrg.normalize = normalize
    blmgv__ovwrg.weekday = xvb__sdnn
    c.pyapi.decref(rfwlw__cznj)
    c.pyapi.decref(xustd__qepz)
    c.pyapi.decref(ngynt__kbaeq)
    xzw__qpl = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(blmgv__ovwrg._getvalue(), is_error=xzw__qpl)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            ygkn__tdyqm = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday()
                )
            if lhs.normalize:
                eld__wzxuj = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                eld__wzxuj = rhs
            return eld__wzxuj + ygkn__tdyqm
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            ygkn__tdyqm = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday()
                )
            if lhs.normalize:
                eld__wzxuj = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                eld__wzxuj = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day, hour=rhs.hour, minute=rhs.minute, second=
                    rhs.second, microsecond=rhs.microsecond)
            return eld__wzxuj + ygkn__tdyqm
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            ygkn__tdyqm = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday()
                )
            return rhs + ygkn__tdyqm
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == week_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


@register_jitable
def calculate_week_date(n, weekday, other_weekday):
    if weekday == -1:
        return pd.Timedelta(weeks=n)
    if weekday != other_weekday:
        xars__nmyir = (weekday - other_weekday) % 7
        if n > 0:
            n = n - 1
    return pd.Timedelta(weeks=n, days=xars__nmyir)


date_offset_unsupported_attrs = {'base', 'freqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
date_offset_unsupported = {'__call__', 'rollback', 'rollforward',
    'is_month_start', 'is_month_end', 'apply', 'apply_index', 'copy',
    'isAnchored', 'onOffset', 'is_anchored', 'is_on_offset',
    'is_quarter_start', 'is_quarter_end', 'is_year_start', 'is_year_end'}
month_end_unsupported_attrs = {'base', 'freqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
month_end_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
month_begin_unsupported_attrs = {'basefreqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
month_begin_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
week_unsupported_attrs = {'basefreqstr', 'kwds', 'name', 'nanos', 'rule_code'}
week_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
offsets_unsupported = {pd.tseries.offsets.BusinessDay, pd.tseries.offsets.
    BDay, pd.tseries.offsets.BusinessHour, pd.tseries.offsets.
    CustomBusinessDay, pd.tseries.offsets.CDay, pd.tseries.offsets.
    CustomBusinessHour, pd.tseries.offsets.BusinessMonthEnd, pd.tseries.
    offsets.BMonthEnd, pd.tseries.offsets.BusinessMonthBegin, pd.tseries.
    offsets.BMonthBegin, pd.tseries.offsets.CustomBusinessMonthEnd, pd.
    tseries.offsets.CBMonthEnd, pd.tseries.offsets.CustomBusinessMonthBegin,
    pd.tseries.offsets.CBMonthBegin, pd.tseries.offsets.SemiMonthEnd, pd.
    tseries.offsets.SemiMonthBegin, pd.tseries.offsets.WeekOfMonth, pd.
    tseries.offsets.LastWeekOfMonth, pd.tseries.offsets.BQuarterEnd, pd.
    tseries.offsets.BQuarterBegin, pd.tseries.offsets.QuarterEnd, pd.
    tseries.offsets.QuarterBegin, pd.tseries.offsets.BYearEnd, pd.tseries.
    offsets.BYearBegin, pd.tseries.offsets.YearEnd, pd.tseries.offsets.
    YearBegin, pd.tseries.offsets.FY5253, pd.tseries.offsets.FY5253Quarter,
    pd.tseries.offsets.Easter, pd.tseries.offsets.Tick, pd.tseries.offsets.
    Day, pd.tseries.offsets.Hour, pd.tseries.offsets.Minute, pd.tseries.
    offsets.Second, pd.tseries.offsets.Milli, pd.tseries.offsets.Micro, pd.
    tseries.offsets.Nano}
frequencies_unsupported = {pd.tseries.frequencies.to_offset}


def _install_date_offsets_unsupported():
    for bfm__fyayk in date_offset_unsupported_attrs:
        yuaf__oditn = 'pandas.tseries.offsets.DateOffset.' + bfm__fyayk
        overload_attribute(DateOffsetType, bfm__fyayk)(
            create_unsupported_overload(yuaf__oditn))
    for bfm__fyayk in date_offset_unsupported:
        yuaf__oditn = 'pandas.tseries.offsets.DateOffset.' + bfm__fyayk
        overload_method(DateOffsetType, bfm__fyayk)(create_unsupported_overload
            (yuaf__oditn))


def _install_month_begin_unsupported():
    for bfm__fyayk in month_begin_unsupported_attrs:
        yuaf__oditn = 'pandas.tseries.offsets.MonthBegin.' + bfm__fyayk
        overload_attribute(MonthBeginType, bfm__fyayk)(
            create_unsupported_overload(yuaf__oditn))
    for bfm__fyayk in month_begin_unsupported:
        yuaf__oditn = 'pandas.tseries.offsets.MonthBegin.' + bfm__fyayk
        overload_method(MonthBeginType, bfm__fyayk)(create_unsupported_overload
            (yuaf__oditn))


def _install_month_end_unsupported():
    for bfm__fyayk in date_offset_unsupported_attrs:
        yuaf__oditn = 'pandas.tseries.offsets.MonthEnd.' + bfm__fyayk
        overload_attribute(MonthEndType, bfm__fyayk)(
            create_unsupported_overload(yuaf__oditn))
    for bfm__fyayk in date_offset_unsupported:
        yuaf__oditn = 'pandas.tseries.offsets.MonthEnd.' + bfm__fyayk
        overload_method(MonthEndType, bfm__fyayk)(create_unsupported_overload
            (yuaf__oditn))


def _install_week_unsupported():
    for bfm__fyayk in week_unsupported_attrs:
        yuaf__oditn = 'pandas.tseries.offsets.Week.' + bfm__fyayk
        overload_attribute(WeekType, bfm__fyayk)(create_unsupported_overload
            (yuaf__oditn))
    for bfm__fyayk in week_unsupported:
        yuaf__oditn = 'pandas.tseries.offsets.Week.' + bfm__fyayk
        overload_method(WeekType, bfm__fyayk)(create_unsupported_overload(
            yuaf__oditn))


def _install_offsets_unsupported():
    for zfec__nvbm in offsets_unsupported:
        yuaf__oditn = 'pandas.tseries.offsets.' + zfec__nvbm.__name__
        overload(zfec__nvbm)(create_unsupported_overload(yuaf__oditn))


def _install_frequencies_unsupported():
    for zfec__nvbm in frequencies_unsupported:
        yuaf__oditn = 'pandas.tseries.frequencies.' + zfec__nvbm.__name__
        overload(zfec__nvbm)(create_unsupported_overload(yuaf__oditn))


_install_date_offsets_unsupported()
_install_month_begin_unsupported()
_install_month_end_unsupported()
_install_week_unsupported()
_install_offsets_unsupported()
_install_frequencies_unsupported()
