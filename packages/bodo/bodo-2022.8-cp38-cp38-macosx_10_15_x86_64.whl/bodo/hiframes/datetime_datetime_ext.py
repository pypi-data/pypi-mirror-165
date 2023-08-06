import datetime
import numba
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
"""
Implementation is based on
https://github.com/python/cpython/blob/39a5c889d30d03a88102e56f03ee0c95db198fb3/Lib/datetime.py
"""


class DatetimeDatetimeType(types.Type):

    def __init__(self):
        super(DatetimeDatetimeType, self).__init__(name=
            'DatetimeDatetimeType()')


datetime_datetime_type = DatetimeDatetimeType()
types.datetime_datetime_type = datetime_datetime_type


@typeof_impl.register(datetime.datetime)
def typeof_datetime_datetime(val, c):
    return datetime_datetime_type


@register_model(DatetimeDatetimeType)
class DatetimeDateTimeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        salt__cuyq = [('year', types.int64), ('month', types.int64), ('day',
            types.int64), ('hour', types.int64), ('minute', types.int64), (
            'second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, salt__cuyq)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    oeqmg__wtzqv = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    oecwj__bedlv = c.pyapi.long_from_longlong(oeqmg__wtzqv.year)
    jjk__ijxks = c.pyapi.long_from_longlong(oeqmg__wtzqv.month)
    kipno__okg = c.pyapi.long_from_longlong(oeqmg__wtzqv.day)
    njjhv__xhjgo = c.pyapi.long_from_longlong(oeqmg__wtzqv.hour)
    bho__gjvbn = c.pyapi.long_from_longlong(oeqmg__wtzqv.minute)
    ydox__cxzri = c.pyapi.long_from_longlong(oeqmg__wtzqv.second)
    awgck__praib = c.pyapi.long_from_longlong(oeqmg__wtzqv.microsecond)
    rjl__nhh = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.datetime))
    mgv__guj = c.pyapi.call_function_objargs(rjl__nhh, (oecwj__bedlv,
        jjk__ijxks, kipno__okg, njjhv__xhjgo, bho__gjvbn, ydox__cxzri,
        awgck__praib))
    c.pyapi.decref(oecwj__bedlv)
    c.pyapi.decref(jjk__ijxks)
    c.pyapi.decref(kipno__okg)
    c.pyapi.decref(njjhv__xhjgo)
    c.pyapi.decref(bho__gjvbn)
    c.pyapi.decref(ydox__cxzri)
    c.pyapi.decref(awgck__praib)
    c.pyapi.decref(rjl__nhh)
    return mgv__guj


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    oecwj__bedlv = c.pyapi.object_getattr_string(val, 'year')
    jjk__ijxks = c.pyapi.object_getattr_string(val, 'month')
    kipno__okg = c.pyapi.object_getattr_string(val, 'day')
    njjhv__xhjgo = c.pyapi.object_getattr_string(val, 'hour')
    bho__gjvbn = c.pyapi.object_getattr_string(val, 'minute')
    ydox__cxzri = c.pyapi.object_getattr_string(val, 'second')
    awgck__praib = c.pyapi.object_getattr_string(val, 'microsecond')
    oeqmg__wtzqv = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    oeqmg__wtzqv.year = c.pyapi.long_as_longlong(oecwj__bedlv)
    oeqmg__wtzqv.month = c.pyapi.long_as_longlong(jjk__ijxks)
    oeqmg__wtzqv.day = c.pyapi.long_as_longlong(kipno__okg)
    oeqmg__wtzqv.hour = c.pyapi.long_as_longlong(njjhv__xhjgo)
    oeqmg__wtzqv.minute = c.pyapi.long_as_longlong(bho__gjvbn)
    oeqmg__wtzqv.second = c.pyapi.long_as_longlong(ydox__cxzri)
    oeqmg__wtzqv.microsecond = c.pyapi.long_as_longlong(awgck__praib)
    c.pyapi.decref(oecwj__bedlv)
    c.pyapi.decref(jjk__ijxks)
    c.pyapi.decref(kipno__okg)
    c.pyapi.decref(njjhv__xhjgo)
    c.pyapi.decref(bho__gjvbn)
    c.pyapi.decref(ydox__cxzri)
    c.pyapi.decref(awgck__praib)
    atir__tfzp = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(oeqmg__wtzqv._getvalue(), is_error=atir__tfzp)


@lower_constant(DatetimeDatetimeType)
def constant_datetime(context, builder, ty, pyval):
    year = context.get_constant(types.int64, pyval.year)
    month = context.get_constant(types.int64, pyval.month)
    day = context.get_constant(types.int64, pyval.day)
    hour = context.get_constant(types.int64, pyval.hour)
    minute = context.get_constant(types.int64, pyval.minute)
    second = context.get_constant(types.int64, pyval.second)
    microsecond = context.get_constant(types.int64, pyval.microsecond)
    return lir.Constant.literal_struct([year, month, day, hour, minute,
        second, microsecond])


@overload(datetime.datetime, no_unliteral=True)
def datetime_datetime(year, month, day, hour=0, minute=0, second=0,
    microsecond=0):

    def impl_datetime(year, month, day, hour=0, minute=0, second=0,
        microsecond=0):
        return init_datetime(year, month, day, hour, minute, second,
            microsecond)
    return impl_datetime


@intrinsic
def init_datetime(typingctx, year, month, day, hour, minute, second,
    microsecond):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        oeqmg__wtzqv = cgutils.create_struct_proxy(typ)(context, builder)
        oeqmg__wtzqv.year = args[0]
        oeqmg__wtzqv.month = args[1]
        oeqmg__wtzqv.day = args[2]
        oeqmg__wtzqv.hour = args[3]
        oeqmg__wtzqv.minute = args[4]
        oeqmg__wtzqv.second = args[5]
        oeqmg__wtzqv.microsecond = args[6]
        return oeqmg__wtzqv._getvalue()
    return DatetimeDatetimeType()(year, month, day, hour, minute, second,
        microsecond), codegen


make_attribute_wrapper(DatetimeDatetimeType, 'year', '_year')
make_attribute_wrapper(DatetimeDatetimeType, 'month', '_month')
make_attribute_wrapper(DatetimeDatetimeType, 'day', '_day')
make_attribute_wrapper(DatetimeDatetimeType, 'hour', '_hour')
make_attribute_wrapper(DatetimeDatetimeType, 'minute', '_minute')
make_attribute_wrapper(DatetimeDatetimeType, 'second', '_second')
make_attribute_wrapper(DatetimeDatetimeType, 'microsecond', '_microsecond')


@overload_attribute(DatetimeDatetimeType, 'year')
def datetime_get_year(dt):

    def impl(dt):
        return dt._year
    return impl


@overload_attribute(DatetimeDatetimeType, 'month')
def datetime_get_month(dt):

    def impl(dt):
        return dt._month
    return impl


@overload_attribute(DatetimeDatetimeType, 'day')
def datetime_get_day(dt):

    def impl(dt):
        return dt._day
    return impl


@overload_attribute(DatetimeDatetimeType, 'hour')
def datetime_get_hour(dt):

    def impl(dt):
        return dt._hour
    return impl


@overload_attribute(DatetimeDatetimeType, 'minute')
def datetime_get_minute(dt):

    def impl(dt):
        return dt._minute
    return impl


@overload_attribute(DatetimeDatetimeType, 'second')
def datetime_get_second(dt):

    def impl(dt):
        return dt._second
    return impl


@overload_attribute(DatetimeDatetimeType, 'microsecond')
def datetime_get_microsecond(dt):

    def impl(dt):
        return dt._microsecond
    return impl


@overload_method(DatetimeDatetimeType, 'date', no_unliteral=True)
def date(dt):

    def impl(dt):
        return datetime.date(dt.year, dt.month, dt.day)
    return impl


@register_jitable
def now_impl():
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.now()
    return d


@register_jitable
def today_impl():
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.today()
    return d


@register_jitable
def strptime_impl(date_string, dtformat):
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.strptime(date_string, dtformat)
    return d


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


def create_cmp_op_overload(op):

    def overload_datetime_cmp(lhs, rhs):
        if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

            def impl(lhs, rhs):
                y, iar__tizxo = lhs.year, rhs.year
                kafe__bkju, lomhh__jwwg = lhs.month, rhs.month
                d, wiqnr__ilvmy = lhs.day, rhs.day
                szpk__hfrhv, kmskc__imfw = lhs.hour, rhs.hour
                qdj__xqnb, oajv__aama = lhs.minute, rhs.minute
                cps__vvlpn, ybeuc__shg = lhs.second, rhs.second
                eok__tiy, snta__yhwk = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, kafe__bkju, d, szpk__hfrhv, qdj__xqnb,
                    cps__vvlpn, eok__tiy), (iar__tizxo, lomhh__jwwg,
                    wiqnr__ilvmy, kmskc__imfw, oajv__aama, ybeuc__shg,
                    snta__yhwk)), 0)
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            dgdl__demm = lhs.toordinal()
            zhowu__drt = rhs.toordinal()
            yai__hkfkm = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            cmcbu__qeeov = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            sjm__svqq = datetime.timedelta(dgdl__demm - zhowu__drt, 
                yai__hkfkm - cmcbu__qeeov, lhs.microsecond - rhs.microsecond)
            return sjm__svqq
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    gtli__ell = context.make_helper(builder, fromty, value=val)
    czdkj__efd = cgutils.as_bool_bit(builder, gtli__ell.valid)
    with builder.if_else(czdkj__efd) as (mhs__qczkr, znz__bty):
        with mhs__qczkr:
            ojgf__abxb = context.cast(builder, gtli__ell.data, fromty.type,
                toty)
            rha__hitae = builder.block
        with znz__bty:
            sof__wwol = numba.np.npdatetime.NAT
            undin__dgq = builder.block
    mgv__guj = builder.phi(ojgf__abxb.type)
    mgv__guj.add_incoming(ojgf__abxb, rha__hitae)
    mgv__guj.add_incoming(sof__wwol, undin__dgq)
    return mgv__guj
