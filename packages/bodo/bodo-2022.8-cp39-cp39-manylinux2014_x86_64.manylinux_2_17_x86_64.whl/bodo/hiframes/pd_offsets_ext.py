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
        jln__uwd = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, jln__uwd)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    chz__tkng = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    zkvwa__txxh = c.pyapi.long_from_longlong(chz__tkng.n)
    xrkij__aecoe = c.pyapi.from_native_value(types.boolean, chz__tkng.
        normalize, c.env_manager)
    eucby__zrs = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    rvefv__ypxo = c.pyapi.call_function_objargs(eucby__zrs, (zkvwa__txxh,
        xrkij__aecoe))
    c.pyapi.decref(zkvwa__txxh)
    c.pyapi.decref(xrkij__aecoe)
    c.pyapi.decref(eucby__zrs)
    return rvefv__ypxo


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    zkvwa__txxh = c.pyapi.object_getattr_string(val, 'n')
    xrkij__aecoe = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(zkvwa__txxh)
    normalize = c.pyapi.to_native_value(types.bool_, xrkij__aecoe).value
    chz__tkng = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    chz__tkng.n = n
    chz__tkng.normalize = normalize
    c.pyapi.decref(zkvwa__txxh)
    c.pyapi.decref(xrkij__aecoe)
    bvce__vtgju = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(chz__tkng._getvalue(), is_error=bvce__vtgju)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        chz__tkng = cgutils.create_struct_proxy(typ)(context, builder)
        chz__tkng.n = args[0]
        chz__tkng.normalize = args[1]
        return chz__tkng._getvalue()
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
        jln__uwd = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, jln__uwd)


@box(MonthEndType)
def box_month_end(typ, val, c):
    fco__qnwrl = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    zkvwa__txxh = c.pyapi.long_from_longlong(fco__qnwrl.n)
    xrkij__aecoe = c.pyapi.from_native_value(types.boolean, fco__qnwrl.
        normalize, c.env_manager)
    nxo__zfb = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    rvefv__ypxo = c.pyapi.call_function_objargs(nxo__zfb, (zkvwa__txxh,
        xrkij__aecoe))
    c.pyapi.decref(zkvwa__txxh)
    c.pyapi.decref(xrkij__aecoe)
    c.pyapi.decref(nxo__zfb)
    return rvefv__ypxo


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    zkvwa__txxh = c.pyapi.object_getattr_string(val, 'n')
    xrkij__aecoe = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(zkvwa__txxh)
    normalize = c.pyapi.to_native_value(types.bool_, xrkij__aecoe).value
    fco__qnwrl = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    fco__qnwrl.n = n
    fco__qnwrl.normalize = normalize
    c.pyapi.decref(zkvwa__txxh)
    c.pyapi.decref(xrkij__aecoe)
    bvce__vtgju = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(fco__qnwrl._getvalue(), is_error=bvce__vtgju)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        fco__qnwrl = cgutils.create_struct_proxy(typ)(context, builder)
        fco__qnwrl.n = args[0]
        fco__qnwrl.normalize = args[1]
        return fco__qnwrl._getvalue()
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
        fco__qnwrl = get_days_in_month(year, month)
        if fco__qnwrl > day:
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
        jln__uwd = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, jln__uwd)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    noy__uypxi = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    yedw__fsm = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for lok__srxwz, hjy__wqjjq in enumerate(date_offset_fields):
        c.builder.store(getattr(noy__uypxi, hjy__wqjjq), c.builder.inttoptr
            (c.builder.add(c.builder.ptrtoint(yedw__fsm, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * lok__srxwz)), lir.IntType(64)
            .as_pointer()))
    enoa__iwl = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    ohz__leqnq = cgutils.get_or_insert_function(c.builder.module, enoa__iwl,
        name='box_date_offset')
    mfats__bllz = c.builder.call(ohz__leqnq, [noy__uypxi.n, noy__uypxi.
        normalize, yedw__fsm, noy__uypxi.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return mfats__bllz


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    zkvwa__txxh = c.pyapi.object_getattr_string(val, 'n')
    xrkij__aecoe = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(zkvwa__txxh)
    normalize = c.pyapi.to_native_value(types.bool_, xrkij__aecoe).value
    yedw__fsm = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    enoa__iwl = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer
        (), lir.IntType(64).as_pointer()])
    tphk__aajza = cgutils.get_or_insert_function(c.builder.module,
        enoa__iwl, name='unbox_date_offset')
    has_kws = c.builder.call(tphk__aajza, [val, yedw__fsm])
    noy__uypxi = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    noy__uypxi.n = n
    noy__uypxi.normalize = normalize
    for lok__srxwz, hjy__wqjjq in enumerate(date_offset_fields):
        setattr(noy__uypxi, hjy__wqjjq, c.builder.load(c.builder.inttoptr(c
            .builder.add(c.builder.ptrtoint(yedw__fsm, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * lok__srxwz)), lir.IntType(64)
            .as_pointer())))
    noy__uypxi.has_kws = has_kws
    c.pyapi.decref(zkvwa__txxh)
    c.pyapi.decref(xrkij__aecoe)
    bvce__vtgju = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(noy__uypxi._getvalue(), is_error=bvce__vtgju)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    kxm__ufwk = [n, normalize]
    has_kws = False
    vome__hjo = [0] * 9 + [-1] * 9
    for lok__srxwz, hjy__wqjjq in enumerate(date_offset_fields):
        if hasattr(pyval, hjy__wqjjq):
            zgkki__gzc = context.get_constant(types.int64, getattr(pyval,
                hjy__wqjjq))
            has_kws = True
        else:
            zgkki__gzc = context.get_constant(types.int64, vome__hjo[
                lok__srxwz])
        kxm__ufwk.append(zgkki__gzc)
    has_kws = context.get_constant(types.boolean, has_kws)
    kxm__ufwk.append(has_kws)
    return lir.Constant.literal_struct(kxm__ufwk)


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    fycl__ohh = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for nbj__iumq in fycl__ohh:
        if not is_overload_none(nbj__iumq):
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
        noy__uypxi = cgutils.create_struct_proxy(typ)(context, builder)
        noy__uypxi.n = args[0]
        noy__uypxi.normalize = args[1]
        noy__uypxi.years = args[2]
        noy__uypxi.months = args[3]
        noy__uypxi.weeks = args[4]
        noy__uypxi.days = args[5]
        noy__uypxi.hours = args[6]
        noy__uypxi.minutes = args[7]
        noy__uypxi.seconds = args[8]
        noy__uypxi.microseconds = args[9]
        noy__uypxi.nanoseconds = args[10]
        noy__uypxi.year = args[11]
        noy__uypxi.month = args[12]
        noy__uypxi.day = args[13]
        noy__uypxi.weekday = args[14]
        noy__uypxi.hour = args[15]
        noy__uypxi.minute = args[16]
        noy__uypxi.second = args[17]
        noy__uypxi.microsecond = args[18]
        noy__uypxi.nanosecond = args[19]
        noy__uypxi.has_kws = args[20]
        return noy__uypxi._getvalue()
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
        idse__fde = -1 if dateoffset.n < 0 else 1
        for jny__hiuk in range(np.abs(dateoffset.n)):
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
            year += idse__fde * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += idse__fde * dateoffset._months
            year, month, mcuo__osxu = calculate_month_end_date(year, month,
                day, 0)
            if day > mcuo__osxu:
                day = mcuo__osxu
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
            foiy__kzqe = pd.Timedelta(days=dateoffset._days + 7 *
                dateoffset._weeks, hours=dateoffset._hours, minutes=
                dateoffset._minutes, seconds=dateoffset._seconds,
                microseconds=dateoffset._microseconds)
            foiy__kzqe = foiy__kzqe + pd.Timedelta(dateoffset._nanoseconds,
                unit='ns')
            if idse__fde == -1:
                foiy__kzqe = -foiy__kzqe
            ts = ts + foiy__kzqe
            if dateoffset._weekday != -1:
                fbar__jwn = ts.weekday()
                awbf__wotm = (dateoffset._weekday - fbar__jwn) % 7
                ts = ts + pd.Timedelta(days=awbf__wotm)
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
        jln__uwd = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, jln__uwd)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        bat__opcmp = -1 if weekday is None else weekday
        return init_week(n, normalize, bat__opcmp)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        ixbuk__pmsm = cgutils.create_struct_proxy(typ)(context, builder)
        ixbuk__pmsm.n = args[0]
        ixbuk__pmsm.normalize = args[1]
        ixbuk__pmsm.weekday = args[2]
        return ixbuk__pmsm._getvalue()
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
    ixbuk__pmsm = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    zkvwa__txxh = c.pyapi.long_from_longlong(ixbuk__pmsm.n)
    xrkij__aecoe = c.pyapi.from_native_value(types.boolean, ixbuk__pmsm.
        normalize, c.env_manager)
    ukwj__qgu = c.pyapi.long_from_longlong(ixbuk__pmsm.weekday)
    oiwo__qbvf = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    zdup__asnf = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64), 
        -1), ixbuk__pmsm.weekday)
    with c.builder.if_else(zdup__asnf) as (whfzx__ottj, mfyzi__tjxk):
        with whfzx__ottj:
            jly__xieuf = c.pyapi.call_function_objargs(oiwo__qbvf, (
                zkvwa__txxh, xrkij__aecoe, ukwj__qgu))
            uydcz__xnjkj = c.builder.block
        with mfyzi__tjxk:
            rqhjh__hwmnz = c.pyapi.call_function_objargs(oiwo__qbvf, (
                zkvwa__txxh, xrkij__aecoe))
            gww__zygat = c.builder.block
    rvefv__ypxo = c.builder.phi(jly__xieuf.type)
    rvefv__ypxo.add_incoming(jly__xieuf, uydcz__xnjkj)
    rvefv__ypxo.add_incoming(rqhjh__hwmnz, gww__zygat)
    c.pyapi.decref(ukwj__qgu)
    c.pyapi.decref(zkvwa__txxh)
    c.pyapi.decref(xrkij__aecoe)
    c.pyapi.decref(oiwo__qbvf)
    return rvefv__ypxo


@unbox(WeekType)
def unbox_week(typ, val, c):
    zkvwa__txxh = c.pyapi.object_getattr_string(val, 'n')
    xrkij__aecoe = c.pyapi.object_getattr_string(val, 'normalize')
    ukwj__qgu = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(zkvwa__txxh)
    normalize = c.pyapi.to_native_value(types.bool_, xrkij__aecoe).value
    fwnv__bqj = c.pyapi.make_none()
    jzu__odywc = c.builder.icmp_unsigned('==', ukwj__qgu, fwnv__bqj)
    with c.builder.if_else(jzu__odywc) as (mfyzi__tjxk, whfzx__ottj):
        with whfzx__ottj:
            jly__xieuf = c.pyapi.long_as_longlong(ukwj__qgu)
            uydcz__xnjkj = c.builder.block
        with mfyzi__tjxk:
            rqhjh__hwmnz = lir.Constant(lir.IntType(64), -1)
            gww__zygat = c.builder.block
    rvefv__ypxo = c.builder.phi(jly__xieuf.type)
    rvefv__ypxo.add_incoming(jly__xieuf, uydcz__xnjkj)
    rvefv__ypxo.add_incoming(rqhjh__hwmnz, gww__zygat)
    ixbuk__pmsm = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ixbuk__pmsm.n = n
    ixbuk__pmsm.normalize = normalize
    ixbuk__pmsm.weekday = rvefv__ypxo
    c.pyapi.decref(zkvwa__txxh)
    c.pyapi.decref(xrkij__aecoe)
    c.pyapi.decref(ukwj__qgu)
    bvce__vtgju = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ixbuk__pmsm._getvalue(), is_error=bvce__vtgju)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            css__bcyhu = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            if lhs.normalize:
                nfm__qzn = pd.Timestamp(year=rhs.year, month=rhs.month, day
                    =rhs.day)
            else:
                nfm__qzn = rhs
            return nfm__qzn + css__bcyhu
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            css__bcyhu = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            if lhs.normalize:
                nfm__qzn = pd.Timestamp(year=rhs.year, month=rhs.month, day
                    =rhs.day)
            else:
                nfm__qzn = pd.Timestamp(year=rhs.year, month=rhs.month, day
                    =rhs.day, hour=rhs.hour, minute=rhs.minute, second=rhs.
                    second, microsecond=rhs.microsecond)
            return nfm__qzn + css__bcyhu
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            css__bcyhu = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            return rhs + css__bcyhu
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
        fjvkq__dvif = (weekday - other_weekday) % 7
        if n > 0:
            n = n - 1
    return pd.Timedelta(weeks=n, days=fjvkq__dvif)


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
    for skig__nelm in date_offset_unsupported_attrs:
        bmx__pjuu = 'pandas.tseries.offsets.DateOffset.' + skig__nelm
        overload_attribute(DateOffsetType, skig__nelm)(
            create_unsupported_overload(bmx__pjuu))
    for skig__nelm in date_offset_unsupported:
        bmx__pjuu = 'pandas.tseries.offsets.DateOffset.' + skig__nelm
        overload_method(DateOffsetType, skig__nelm)(create_unsupported_overload
            (bmx__pjuu))


def _install_month_begin_unsupported():
    for skig__nelm in month_begin_unsupported_attrs:
        bmx__pjuu = 'pandas.tseries.offsets.MonthBegin.' + skig__nelm
        overload_attribute(MonthBeginType, skig__nelm)(
            create_unsupported_overload(bmx__pjuu))
    for skig__nelm in month_begin_unsupported:
        bmx__pjuu = 'pandas.tseries.offsets.MonthBegin.' + skig__nelm
        overload_method(MonthBeginType, skig__nelm)(create_unsupported_overload
            (bmx__pjuu))


def _install_month_end_unsupported():
    for skig__nelm in date_offset_unsupported_attrs:
        bmx__pjuu = 'pandas.tseries.offsets.MonthEnd.' + skig__nelm
        overload_attribute(MonthEndType, skig__nelm)(
            create_unsupported_overload(bmx__pjuu))
    for skig__nelm in date_offset_unsupported:
        bmx__pjuu = 'pandas.tseries.offsets.MonthEnd.' + skig__nelm
        overload_method(MonthEndType, skig__nelm)(create_unsupported_overload
            (bmx__pjuu))


def _install_week_unsupported():
    for skig__nelm in week_unsupported_attrs:
        bmx__pjuu = 'pandas.tseries.offsets.Week.' + skig__nelm
        overload_attribute(WeekType, skig__nelm)(create_unsupported_overload
            (bmx__pjuu))
    for skig__nelm in week_unsupported:
        bmx__pjuu = 'pandas.tseries.offsets.Week.' + skig__nelm
        overload_method(WeekType, skig__nelm)(create_unsupported_overload(
            bmx__pjuu))


def _install_offsets_unsupported():
    for zgkki__gzc in offsets_unsupported:
        bmx__pjuu = 'pandas.tseries.offsets.' + zgkki__gzc.__name__
        overload(zgkki__gzc)(create_unsupported_overload(bmx__pjuu))


def _install_frequencies_unsupported():
    for zgkki__gzc in frequencies_unsupported:
        bmx__pjuu = 'pandas.tseries.frequencies.' + zgkki__gzc.__name__
        overload(zgkki__gzc)(create_unsupported_overload(bmx__pjuu))


_install_date_offsets_unsupported()
_install_month_begin_unsupported()
_install_month_end_unsupported()
_install_week_unsupported()
_install_offsets_unsupported()
_install_frequencies_unsupported()
