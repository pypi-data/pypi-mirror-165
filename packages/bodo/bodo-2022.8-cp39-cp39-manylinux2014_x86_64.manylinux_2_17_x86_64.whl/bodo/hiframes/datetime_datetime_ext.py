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
        nefxy__qpu = [('year', types.int64), ('month', types.int64), ('day',
            types.int64), ('hour', types.int64), ('minute', types.int64), (
            'second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, nefxy__qpu)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    tka__hlt = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val
        )
    cwgd__wgv = c.pyapi.long_from_longlong(tka__hlt.year)
    zha__doywn = c.pyapi.long_from_longlong(tka__hlt.month)
    jbsmt__rfm = c.pyapi.long_from_longlong(tka__hlt.day)
    iqzw__uak = c.pyapi.long_from_longlong(tka__hlt.hour)
    buyf__rtyes = c.pyapi.long_from_longlong(tka__hlt.minute)
    zryt__snoc = c.pyapi.long_from_longlong(tka__hlt.second)
    xcigr__xeva = c.pyapi.long_from_longlong(tka__hlt.microsecond)
    kpdgs__btbfa = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        datetime))
    junja__trb = c.pyapi.call_function_objargs(kpdgs__btbfa, (cwgd__wgv,
        zha__doywn, jbsmt__rfm, iqzw__uak, buyf__rtyes, zryt__snoc,
        xcigr__xeva))
    c.pyapi.decref(cwgd__wgv)
    c.pyapi.decref(zha__doywn)
    c.pyapi.decref(jbsmt__rfm)
    c.pyapi.decref(iqzw__uak)
    c.pyapi.decref(buyf__rtyes)
    c.pyapi.decref(zryt__snoc)
    c.pyapi.decref(xcigr__xeva)
    c.pyapi.decref(kpdgs__btbfa)
    return junja__trb


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    cwgd__wgv = c.pyapi.object_getattr_string(val, 'year')
    zha__doywn = c.pyapi.object_getattr_string(val, 'month')
    jbsmt__rfm = c.pyapi.object_getattr_string(val, 'day')
    iqzw__uak = c.pyapi.object_getattr_string(val, 'hour')
    buyf__rtyes = c.pyapi.object_getattr_string(val, 'minute')
    zryt__snoc = c.pyapi.object_getattr_string(val, 'second')
    xcigr__xeva = c.pyapi.object_getattr_string(val, 'microsecond')
    tka__hlt = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    tka__hlt.year = c.pyapi.long_as_longlong(cwgd__wgv)
    tka__hlt.month = c.pyapi.long_as_longlong(zha__doywn)
    tka__hlt.day = c.pyapi.long_as_longlong(jbsmt__rfm)
    tka__hlt.hour = c.pyapi.long_as_longlong(iqzw__uak)
    tka__hlt.minute = c.pyapi.long_as_longlong(buyf__rtyes)
    tka__hlt.second = c.pyapi.long_as_longlong(zryt__snoc)
    tka__hlt.microsecond = c.pyapi.long_as_longlong(xcigr__xeva)
    c.pyapi.decref(cwgd__wgv)
    c.pyapi.decref(zha__doywn)
    c.pyapi.decref(jbsmt__rfm)
    c.pyapi.decref(iqzw__uak)
    c.pyapi.decref(buyf__rtyes)
    c.pyapi.decref(zryt__snoc)
    c.pyapi.decref(xcigr__xeva)
    uml__zmthe = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(tka__hlt._getvalue(), is_error=uml__zmthe)


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
        tka__hlt = cgutils.create_struct_proxy(typ)(context, builder)
        tka__hlt.year = args[0]
        tka__hlt.month = args[1]
        tka__hlt.day = args[2]
        tka__hlt.hour = args[3]
        tka__hlt.minute = args[4]
        tka__hlt.second = args[5]
        tka__hlt.microsecond = args[6]
        return tka__hlt._getvalue()
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
                y, wrs__sizo = lhs.year, rhs.year
                zjvl__gsebr, oty__xpfm = lhs.month, rhs.month
                d, eoal__lgp = lhs.day, rhs.day
                rqg__ctqsa, uayrx__omn = lhs.hour, rhs.hour
                kry__dkob, jni__uoj = lhs.minute, rhs.minute
                clodm__yzy, guesk__nmv = lhs.second, rhs.second
                szbbx__bkyav, llqei__gsjuo = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, zjvl__gsebr, d, rqg__ctqsa, kry__dkob,
                    clodm__yzy, szbbx__bkyav), (wrs__sizo, oty__xpfm,
                    eoal__lgp, uayrx__omn, jni__uoj, guesk__nmv,
                    llqei__gsjuo)), 0)
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            wzjvr__hdzxe = lhs.toordinal()
            sidys__dyf = rhs.toordinal()
            dvkxe__ehou = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            lwwza__ate = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            mucs__uuj = datetime.timedelta(wzjvr__hdzxe - sidys__dyf, 
                dvkxe__ehou - lwwza__ate, lhs.microsecond - rhs.microsecond)
            return mucs__uuj
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    klb__bkt = context.make_helper(builder, fromty, value=val)
    lvzmg__jczfm = cgutils.as_bool_bit(builder, klb__bkt.valid)
    with builder.if_else(lvzmg__jczfm) as (bbgnb__mkmvv, jue__lzbfp):
        with bbgnb__mkmvv:
            atbi__urml = context.cast(builder, klb__bkt.data, fromty.type, toty
                )
            edrs__bvz = builder.block
        with jue__lzbfp:
            zse__iluw = numba.np.npdatetime.NAT
            pxlkj__xgs = builder.block
    junja__trb = builder.phi(atbi__urml.type)
    junja__trb.add_incoming(atbi__urml, edrs__bvz)
    junja__trb.add_incoming(zse__iluw, pxlkj__xgs)
    return junja__trb
