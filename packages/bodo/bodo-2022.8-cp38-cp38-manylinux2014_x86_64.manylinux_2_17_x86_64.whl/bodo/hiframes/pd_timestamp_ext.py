"""Timestamp extension for Pandas Timestamp with timezone support."""
import calendar
import datetime
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pytz
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.core.typing.templates import ConcreteTemplate, infer_global, signature
from numba.extending import NativeValue, box, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
import bodo.libs.str_ext
import bodo.utils.utils
from bodo.hiframes.datetime_date_ext import DatetimeDateType, _ord2ymd, _ymd2ord, get_isocalendar
from bodo.hiframes.datetime_timedelta_ext import PDTimeDeltaType, _no_input, datetime_timedelta_type, pd_timedelta_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.libs import hdatetime_ext
from bodo.libs.pd_datetime_arr_ext import get_pytz_type_info
from bodo.libs.str_arr_ext import string_array_type
from bodo.utils.typing import BodoError, check_unsupported_args, get_overload_const_bool, get_overload_const_int, get_overload_const_str, is_iterable_type, is_overload_constant_int, is_overload_constant_str, is_overload_none, raise_bodo_error
ll.add_symbol('extract_year_days', hdatetime_ext.extract_year_days)
ll.add_symbol('get_month_day', hdatetime_ext.get_month_day)
ll.add_symbol('npy_datetimestruct_to_datetime', hdatetime_ext.
    npy_datetimestruct_to_datetime)
npy_datetimestruct_to_datetime = types.ExternalFunction(
    'npy_datetimestruct_to_datetime', types.int64(types.int64, types.int32,
    types.int32, types.int32, types.int32, types.int32, types.int32))
date_fields = ['year', 'month', 'day', 'hour', 'minute', 'second',
    'microsecond', 'nanosecond', 'quarter', 'dayofyear', 'day_of_year',
    'dayofweek', 'day_of_week', 'daysinmonth', 'days_in_month',
    'is_leap_year', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end', 'week', 'weekofyear',
    'weekday']
date_methods = ['normalize', 'day_name', 'month_name']
timedelta_fields = ['days', 'seconds', 'microseconds', 'nanoseconds']
timedelta_methods = ['total_seconds', 'to_pytimedelta']
iNaT = pd._libs.tslibs.iNaT


class PandasTimestampType(types.Type):

    def __init__(self, tz_val=None):
        self.tz = tz_val
        if tz_val is None:
            owgxj__ddn = 'PandasTimestampType()'
        else:
            owgxj__ddn = f'PandasTimestampType({tz_val})'
        super(PandasTimestampType, self).__init__(name=owgxj__ddn)


pd_timestamp_type = PandasTimestampType()


def check_tz_aware_unsupported(val, func_name):
    if isinstance(val, bodo.hiframes.series_dt_impl.
        SeriesDatetimePropertiesType):
        val = val.stype
    if isinstance(val, PandasTimestampType) and val.tz is not None:
        raise BodoError(
            f'{func_name} on Timezone-aware timestamp not yet supported. Please convert to timezone naive with ts.tz_convert(None)'
            )
    elif isinstance(val, bodo.DatetimeArrayType):
        raise BodoError(
            f'{func_name} on Timezone-aware array not yet supported. Please convert to timezone naive with arr.tz_convert(None)'
            )
    elif isinstance(val, bodo.DatetimeIndexType) and isinstance(val.data,
        bodo.DatetimeArrayType):
        raise BodoError(
            f'{func_name} on Timezone-aware index not yet supported. Please convert to timezone naive with index.tz_convert(None)'
            )
    elif isinstance(val, bodo.SeriesType) and isinstance(val.data, bodo.
        DatetimeArrayType):
        raise BodoError(
            f'{func_name} on Timezone-aware series not yet supported. Please convert to timezone naive with series.dt.tz_convert(None)'
            )
    elif isinstance(val, bodo.DataFrameType):
        for oxq__mvu in val.data:
            if isinstance(oxq__mvu, bodo.DatetimeArrayType):
                raise BodoError(
                    f'{func_name} on Timezone-aware columns not yet supported. Please convert each column to timezone naive with series.dt.tz_convert(None)'
                    )


@typeof_impl.register(pd.Timestamp)
def typeof_pd_timestamp(val, c):
    return PandasTimestampType(get_pytz_type_info(val.tz) if val.tz else None)


ts_field_typ = types.int64


@register_model(PandasTimestampType)
class PandasTimestampModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        dgtg__sfyka = [('year', ts_field_typ), ('month', ts_field_typ), (
            'day', ts_field_typ), ('hour', ts_field_typ), ('minute',
            ts_field_typ), ('second', ts_field_typ), ('microsecond',
            ts_field_typ), ('nanosecond', ts_field_typ), ('value',
            ts_field_typ)]
        models.StructModel.__init__(self, dmm, fe_type, dgtg__sfyka)


make_attribute_wrapper(PandasTimestampType, 'year', 'year')
make_attribute_wrapper(PandasTimestampType, 'month', 'month')
make_attribute_wrapper(PandasTimestampType, 'day', 'day')
make_attribute_wrapper(PandasTimestampType, 'hour', 'hour')
make_attribute_wrapper(PandasTimestampType, 'minute', 'minute')
make_attribute_wrapper(PandasTimestampType, 'second', 'second')
make_attribute_wrapper(PandasTimestampType, 'microsecond', 'microsecond')
make_attribute_wrapper(PandasTimestampType, 'nanosecond', 'nanosecond')
make_attribute_wrapper(PandasTimestampType, 'value', 'value')


@unbox(PandasTimestampType)
def unbox_pandas_timestamp(typ, val, c):
    wlzhy__dlc = c.pyapi.object_getattr_string(val, 'year')
    fasj__dykhr = c.pyapi.object_getattr_string(val, 'month')
    omstt__sqyn = c.pyapi.object_getattr_string(val, 'day')
    wjziy__vmwzr = c.pyapi.object_getattr_string(val, 'hour')
    cuv__ygh = c.pyapi.object_getattr_string(val, 'minute')
    ogkhf__owvxg = c.pyapi.object_getattr_string(val, 'second')
    vmgkm__auc = c.pyapi.object_getattr_string(val, 'microsecond')
    jnber__pzn = c.pyapi.object_getattr_string(val, 'nanosecond')
    tdyv__dze = c.pyapi.object_getattr_string(val, 'value')
    nyp__wrvjb = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    nyp__wrvjb.year = c.pyapi.long_as_longlong(wlzhy__dlc)
    nyp__wrvjb.month = c.pyapi.long_as_longlong(fasj__dykhr)
    nyp__wrvjb.day = c.pyapi.long_as_longlong(omstt__sqyn)
    nyp__wrvjb.hour = c.pyapi.long_as_longlong(wjziy__vmwzr)
    nyp__wrvjb.minute = c.pyapi.long_as_longlong(cuv__ygh)
    nyp__wrvjb.second = c.pyapi.long_as_longlong(ogkhf__owvxg)
    nyp__wrvjb.microsecond = c.pyapi.long_as_longlong(vmgkm__auc)
    nyp__wrvjb.nanosecond = c.pyapi.long_as_longlong(jnber__pzn)
    nyp__wrvjb.value = c.pyapi.long_as_longlong(tdyv__dze)
    c.pyapi.decref(wlzhy__dlc)
    c.pyapi.decref(fasj__dykhr)
    c.pyapi.decref(omstt__sqyn)
    c.pyapi.decref(wjziy__vmwzr)
    c.pyapi.decref(cuv__ygh)
    c.pyapi.decref(ogkhf__owvxg)
    c.pyapi.decref(vmgkm__auc)
    c.pyapi.decref(jnber__pzn)
    c.pyapi.decref(tdyv__dze)
    blb__cqpux = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(nyp__wrvjb._getvalue(), is_error=blb__cqpux)


@box(PandasTimestampType)
def box_pandas_timestamp(typ, val, c):
    yrjvd__xwigf = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    wlzhy__dlc = c.pyapi.long_from_longlong(yrjvd__xwigf.year)
    fasj__dykhr = c.pyapi.long_from_longlong(yrjvd__xwigf.month)
    omstt__sqyn = c.pyapi.long_from_longlong(yrjvd__xwigf.day)
    wjziy__vmwzr = c.pyapi.long_from_longlong(yrjvd__xwigf.hour)
    cuv__ygh = c.pyapi.long_from_longlong(yrjvd__xwigf.minute)
    ogkhf__owvxg = c.pyapi.long_from_longlong(yrjvd__xwigf.second)
    qhg__ftnfc = c.pyapi.long_from_longlong(yrjvd__xwigf.microsecond)
    ohu__gaf = c.pyapi.long_from_longlong(yrjvd__xwigf.nanosecond)
    eufo__xra = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timestamp))
    if typ.tz is None:
        res = c.pyapi.call_function_objargs(eufo__xra, (wlzhy__dlc,
            fasj__dykhr, omstt__sqyn, wjziy__vmwzr, cuv__ygh, ogkhf__owvxg,
            qhg__ftnfc, ohu__gaf))
    else:
        if isinstance(typ.tz, int):
            nxe__zmvbj = c.pyapi.long_from_longlong(lir.Constant(lir.
                IntType(64), typ.tz))
        else:
            dxvbh__szm = c.context.insert_const_string(c.builder.module,
                str(typ.tz))
            nxe__zmvbj = c.pyapi.string_from_string(dxvbh__szm)
        args = c.pyapi.tuple_pack(())
        kwargs = c.pyapi.dict_pack([('year', wlzhy__dlc), ('month',
            fasj__dykhr), ('day', omstt__sqyn), ('hour', wjziy__vmwzr), (
            'minute', cuv__ygh), ('second', ogkhf__owvxg), ('microsecond',
            qhg__ftnfc), ('nanosecond', ohu__gaf), ('tz', nxe__zmvbj)])
        res = c.pyapi.call(eufo__xra, args, kwargs)
        c.pyapi.decref(args)
        c.pyapi.decref(kwargs)
        c.pyapi.decref(nxe__zmvbj)
    c.pyapi.decref(wlzhy__dlc)
    c.pyapi.decref(fasj__dykhr)
    c.pyapi.decref(omstt__sqyn)
    c.pyapi.decref(wjziy__vmwzr)
    c.pyapi.decref(cuv__ygh)
    c.pyapi.decref(ogkhf__owvxg)
    c.pyapi.decref(qhg__ftnfc)
    c.pyapi.decref(ohu__gaf)
    return res


@intrinsic
def init_timestamp(typingctx, year, month, day, hour, minute, second,
    microsecond, nanosecond, value, tz):

    def codegen(context, builder, sig, args):
        (year, month, day, hour, minute, second, ispro__upx, kdig__vfqze,
            value, tpnqc__tuyw) = args
        ts = cgutils.create_struct_proxy(sig.return_type)(context, builder)
        ts.year = year
        ts.month = month
        ts.day = day
        ts.hour = hour
        ts.minute = minute
        ts.second = second
        ts.microsecond = ispro__upx
        ts.nanosecond = kdig__vfqze
        ts.value = value
        return ts._getvalue()
    if is_overload_none(tz):
        typ = pd_timestamp_type
    elif is_overload_constant_str(tz):
        typ = PandasTimestampType(get_overload_const_str(tz))
    elif is_overload_constant_int(tz):
        typ = PandasTimestampType(get_overload_const_int(tz))
    else:
        raise_bodo_error('tz must be a constant string, int, or None')
    return typ(types.int64, types.int64, types.int64, types.int64, types.
        int64, types.int64, types.int64, types.int64, types.int64, tz), codegen


@numba.generated_jit
def zero_if_none(value):
    if value == types.none:
        return lambda value: 0
    return lambda value: value


@lower_constant(PandasTimestampType)
def constant_timestamp(context, builder, ty, pyval):
    year = context.get_constant(types.int64, pyval.year)
    month = context.get_constant(types.int64, pyval.month)
    day = context.get_constant(types.int64, pyval.day)
    hour = context.get_constant(types.int64, pyval.hour)
    minute = context.get_constant(types.int64, pyval.minute)
    second = context.get_constant(types.int64, pyval.second)
    microsecond = context.get_constant(types.int64, pyval.microsecond)
    nanosecond = context.get_constant(types.int64, pyval.nanosecond)
    value = context.get_constant(types.int64, pyval.value)
    return lir.Constant.literal_struct((year, month, day, hour, minute,
        second, microsecond, nanosecond, value))


@overload(pd.Timestamp, no_unliteral=True)
def overload_pd_timestamp(ts_input=_no_input, freq=None, tz=None, unit=None,
    year=None, month=None, day=None, hour=None, minute=None, second=None,
    microsecond=None, nanosecond=None, tzinfo=None):
    if not is_overload_none(tz) and is_overload_constant_str(tz
        ) and get_overload_const_str(tz) not in pytz.all_timezones_set:
        raise BodoError(
            "pandas.Timestamp(): 'tz', if provided, must be constant string found in pytz.all_timezones"
            )
    if ts_input == _no_input or getattr(ts_input, 'value', None) == _no_input:

        def impl_kw(ts_input=_no_input, freq=None, tz=None, unit=None, year
            =None, month=None, day=None, hour=None, minute=None, second=
            None, microsecond=None, nanosecond=None, tzinfo=None):
            value = npy_datetimestruct_to_datetime(year, month, day,
                zero_if_none(hour), zero_if_none(minute), zero_if_none(
                second), zero_if_none(microsecond))
            value += zero_if_none(nanosecond)
            return init_timestamp(year, month, day, zero_if_none(hour),
                zero_if_none(minute), zero_if_none(second), zero_if_none(
                microsecond), zero_if_none(nanosecond), value, tz)
        return impl_kw
    if isinstance(types.unliteral(freq), types.Integer):

        def impl_pos(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            value = npy_datetimestruct_to_datetime(ts_input, freq, tz,
                zero_if_none(unit), zero_if_none(year), zero_if_none(month),
                zero_if_none(day))
            value += zero_if_none(hour)
            return init_timestamp(ts_input, freq, tz, zero_if_none(unit),
                zero_if_none(year), zero_if_none(month), zero_if_none(day),
                zero_if_none(hour), value, None)
        return impl_pos
    if isinstance(ts_input, types.Number):
        if is_overload_none(unit):
            unit = 'ns'
        if not is_overload_constant_str(unit):
            raise BodoError(
                'pandas.Timedelta(): unit argument must be a constant str')
        unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
            get_overload_const_str(unit))
        rbc__aol, precision = pd._libs.tslibs.conversion.precision_from_unit(
            unit)
        if isinstance(ts_input, types.Integer):

            def impl_int(ts_input=_no_input, freq=None, tz=None, unit=None,
                year=None, month=None, day=None, hour=None, minute=None,
                second=None, microsecond=None, nanosecond=None, tzinfo=None):
                value = ts_input * rbc__aol
                return convert_val_to_timestamp(value, tz)
            return impl_int

        def impl_float(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            jgwdj__sks = np.int64(ts_input)
            uloye__dtu = ts_input - jgwdj__sks
            if precision:
                uloye__dtu = np.round(uloye__dtu, precision)
            value = jgwdj__sks * rbc__aol + np.int64(uloye__dtu * rbc__aol)
            return convert_val_to_timestamp(value, tz)
        return impl_float
    if ts_input == bodo.string_type or is_overload_constant_str(ts_input):
        types.pd_timestamp_type = pd_timestamp_type
        if is_overload_none(tz):
            tz_val = None
        elif is_overload_constant_str(tz):
            tz_val = get_overload_const_str(tz)
        else:
            raise_bodo_error(
                'pandas.Timestamp(): tz argument must be a constant string or None'
                )
        typ = PandasTimestampType(tz_val)

        def impl_str(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            with numba.objmode(res=typ):
                res = pd.Timestamp(ts_input, tz=tz)
            return res
        return impl_str
    if ts_input == pd_timestamp_type:
        return (lambda ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None: ts_input)
    if ts_input == bodo.hiframes.datetime_datetime_ext.datetime_datetime_type:

        def impl_datetime(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            year = ts_input.year
            month = ts_input.month
            day = ts_input.day
            hour = ts_input.hour
            minute = ts_input.minute
            second = ts_input.second
            microsecond = ts_input.microsecond
            value = npy_datetimestruct_to_datetime(year, month, day,
                zero_if_none(hour), zero_if_none(minute), zero_if_none(
                second), zero_if_none(microsecond))
            value += zero_if_none(nanosecond)
            return init_timestamp(year, month, day, zero_if_none(hour),
                zero_if_none(minute), zero_if_none(second), zero_if_none(
                microsecond), zero_if_none(nanosecond), value, tz)
        return impl_datetime
    if ts_input == bodo.hiframes.datetime_date_ext.datetime_date_type:

        def impl_date(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            year = ts_input.year
            month = ts_input.month
            day = ts_input.day
            value = npy_datetimestruct_to_datetime(year, month, day,
                zero_if_none(hour), zero_if_none(minute), zero_if_none(
                second), zero_if_none(microsecond))
            value += zero_if_none(nanosecond)
            return init_timestamp(year, month, day, zero_if_none(hour),
                zero_if_none(minute), zero_if_none(second), zero_if_none(
                microsecond), zero_if_none(nanosecond), value, None)
        return impl_date
    if isinstance(ts_input, numba.core.types.scalars.NPDatetime):
        rbc__aol, precision = pd._libs.tslibs.conversion.precision_from_unit(
            ts_input.unit)

        def impl_date(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            value = np.int64(ts_input) * rbc__aol
            return convert_datetime64_to_timestamp(integer_to_dt64(value))
        return impl_date


@overload_attribute(PandasTimestampType, 'dayofyear')
@overload_attribute(PandasTimestampType, 'day_of_year')
def overload_pd_dayofyear(ptt):

    def pd_dayofyear(ptt):
        return get_day_of_year(ptt.year, ptt.month, ptt.day)
    return pd_dayofyear


@overload_method(PandasTimestampType, 'weekday')
@overload_attribute(PandasTimestampType, 'dayofweek')
@overload_attribute(PandasTimestampType, 'day_of_week')
def overload_pd_dayofweek(ptt):

    def pd_dayofweek(ptt):
        return get_day_of_week(ptt.year, ptt.month, ptt.day)
    return pd_dayofweek


@overload_attribute(PandasTimestampType, 'week')
@overload_attribute(PandasTimestampType, 'weekofyear')
def overload_week_number(ptt):

    def pd_week_number(ptt):
        tpnqc__tuyw, gqc__bxtgq, tpnqc__tuyw = get_isocalendar(ptt.year,
            ptt.month, ptt.day)
        return gqc__bxtgq
    return pd_week_number


@overload_method(PandasTimestampType, '__hash__', no_unliteral=True)
def dt64_hash(val):
    return lambda val: hash(val.value)


@overload_attribute(PandasTimestampType, 'days_in_month')
@overload_attribute(PandasTimestampType, 'daysinmonth')
def overload_pd_daysinmonth(ptt):

    def pd_daysinmonth(ptt):
        return get_days_in_month(ptt.year, ptt.month)
    return pd_daysinmonth


@overload_attribute(PandasTimestampType, 'is_leap_year')
def overload_pd_is_leap_year(ptt):

    def pd_is_leap_year(ptt):
        return is_leap_year(ptt.year)
    return pd_is_leap_year


@overload_attribute(PandasTimestampType, 'is_month_start')
def overload_pd_is_month_start(ptt):

    def pd_is_month_start(ptt):
        return ptt.day == 1
    return pd_is_month_start


@overload_attribute(PandasTimestampType, 'is_month_end')
def overload_pd_is_month_end(ptt):

    def pd_is_month_end(ptt):
        return ptt.day == get_days_in_month(ptt.year, ptt.month)
    return pd_is_month_end


@overload_attribute(PandasTimestampType, 'is_quarter_start')
def overload_pd_is_quarter_start(ptt):

    def pd_is_quarter_start(ptt):
        return ptt.day == 1 and ptt.month % 3 == 1
    return pd_is_quarter_start


@overload_attribute(PandasTimestampType, 'is_quarter_end')
def overload_pd_is_quarter_end(ptt):

    def pd_is_quarter_end(ptt):
        return ptt.month % 3 == 0 and ptt.day == get_days_in_month(ptt.year,
            ptt.month)
    return pd_is_quarter_end


@overload_attribute(PandasTimestampType, 'is_year_start')
def overload_pd_is_year_start(ptt):

    def pd_is_year_start(ptt):
        return ptt.day == 1 and ptt.month == 1
    return pd_is_year_start


@overload_attribute(PandasTimestampType, 'is_year_end')
def overload_pd_is_year_end(ptt):

    def pd_is_year_end(ptt):
        return ptt.day == 31 and ptt.month == 12
    return pd_is_year_end


@overload_attribute(PandasTimestampType, 'quarter')
def overload_quarter(ptt):

    def quarter(ptt):
        return (ptt.month - 1) // 3 + 1
    return quarter


@overload_method(PandasTimestampType, 'date', no_unliteral=True)
def overload_pd_timestamp_date(ptt):

    def pd_timestamp_date_impl(ptt):
        return datetime.date(ptt.year, ptt.month, ptt.day)
    return pd_timestamp_date_impl


@overload_method(PandasTimestampType, 'isocalendar', no_unliteral=True)
def overload_pd_timestamp_isocalendar(ptt):

    def impl(ptt):
        year, gqc__bxtgq, zzir__znrf = get_isocalendar(ptt.year, ptt.month,
            ptt.day)
        return year, gqc__bxtgq, zzir__znrf
    return impl


@overload_method(PandasTimestampType, 'isoformat', no_unliteral=True)
def overload_pd_timestamp_isoformat(ts, sep=None):
    if is_overload_none(sep):

        def timestamp_isoformat_impl(ts, sep=None):
            assert ts.nanosecond == 0
            ivev__rip = str_2d(ts.hour) + ':' + str_2d(ts.minute
                ) + ':' + str_2d(ts.second)
            res = str(ts.year) + '-' + str_2d(ts.month) + '-' + str_2d(ts.day
                ) + 'T' + ivev__rip
            return res
        return timestamp_isoformat_impl
    else:

        def timestamp_isoformat_impl(ts, sep=None):
            assert ts.nanosecond == 0
            ivev__rip = str_2d(ts.hour) + ':' + str_2d(ts.minute
                ) + ':' + str_2d(ts.second)
            res = str(ts.year) + '-' + str_2d(ts.month) + '-' + str_2d(ts.day
                ) + sep + ivev__rip
            return res
    return timestamp_isoformat_impl


@overload_method(PandasTimestampType, 'normalize', no_unliteral=True)
def overload_pd_timestamp_normalize(ptt):

    def impl(ptt):
        return pd.Timestamp(year=ptt.year, month=ptt.month, day=ptt.day)
    return impl


@overload_method(PandasTimestampType, 'day_name', no_unliteral=True)
def overload_pd_timestamp_day_name(ptt, locale=None):
    ohyrd__aqk = dict(locale=locale)
    oyok__ikqde = dict(locale=None)
    check_unsupported_args('Timestamp.day_name', ohyrd__aqk, oyok__ikqde,
        package_name='pandas', module_name='Timestamp')

    def impl(ptt, locale=None):
        thl__hda = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
            'Saturday', 'Sunday')
        tpnqc__tuyw, tpnqc__tuyw, exf__sajr = ptt.isocalendar()
        return thl__hda[exf__sajr - 1]
    return impl


@overload_method(PandasTimestampType, 'month_name', no_unliteral=True)
def overload_pd_timestamp_month_name(ptt, locale=None):
    ohyrd__aqk = dict(locale=locale)
    oyok__ikqde = dict(locale=None)
    check_unsupported_args('Timestamp.month_name', ohyrd__aqk, oyok__ikqde,
        package_name='pandas', module_name='Timestamp')

    def impl(ptt, locale=None):
        qpd__rlz = ('January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December')
        return qpd__rlz[ptt.month - 1]
    return impl


@overload_method(PandasTimestampType, 'tz_convert', no_unliteral=True)
def overload_pd_timestamp_tz_convert(ptt, tz):
    if ptt.tz is None:
        raise BodoError(
            'Cannot convert tz-naive Timestamp, use tz_localize to localize')
    if is_overload_none(tz):
        return lambda ptt, tz: convert_val_to_timestamp(ptt.value)
    elif is_overload_constant_str(tz):
        return lambda ptt, tz: convert_val_to_timestamp(ptt.value, tz=tz)


@overload_method(PandasTimestampType, 'tz_localize', no_unliteral=True)
def overload_pd_timestamp_tz_localize(ptt, tz, ambiguous='raise',
    nonexistent='raise'):
    if ptt.tz is not None and not is_overload_none(tz):
        raise BodoError(
            'Cannot localize tz-aware Timestamp, use tz_convert for conversions'
            )
    ohyrd__aqk = dict(ambiguous=ambiguous, nonexistent=nonexistent)
    fwjp__vuav = dict(ambiguous='raise', nonexistent='raise')
    check_unsupported_args('Timestamp.tz_localize', ohyrd__aqk, fwjp__vuav,
        package_name='pandas', module_name='Timestamp')
    if is_overload_none(tz):
        return (lambda ptt, tz, ambiguous='raise', nonexistent='raise':
            convert_val_to_timestamp(ptt.value, is_convert=False))
    elif is_overload_constant_str(tz):
        return (lambda ptt, tz, ambiguous='raise', nonexistent='raise':
            convert_val_to_timestamp(ptt.value, tz=tz, is_convert=False))


@numba.njit
def str_2d(a):
    res = str(a)
    if len(res) == 1:
        return '0' + res
    return res


@overload(str, no_unliteral=True)
def ts_str_overload(a):
    if a == pd_timestamp_type:
        return lambda a: a.isoformat(' ')


@intrinsic
def extract_year_days(typingctx, dt64_t=None):
    assert dt64_t in (types.int64, types.NPDatetime('ns'))

    def codegen(context, builder, sig, args):
        oio__krlof = cgutils.alloca_once(builder, lir.IntType(64))
        builder.store(args[0], oio__krlof)
        year = cgutils.alloca_once(builder, lir.IntType(64))
        bngi__nemv = cgutils.alloca_once(builder, lir.IntType(64))
        hskb__uszc = lir.FunctionType(lir.VoidType(), [lir.IntType(64).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer()])
        rey__vzqkd = cgutils.get_or_insert_function(builder.module,
            hskb__uszc, name='extract_year_days')
        builder.call(rey__vzqkd, [oio__krlof, year, bngi__nemv])
        return cgutils.pack_array(builder, [builder.load(oio__krlof),
            builder.load(year), builder.load(bngi__nemv)])
    return types.Tuple([types.int64, types.int64, types.int64])(dt64_t
        ), codegen


@intrinsic
def get_month_day(typingctx, year_t, days_t=None):
    assert year_t == types.int64
    assert days_t == types.int64

    def codegen(context, builder, sig, args):
        month = cgutils.alloca_once(builder, lir.IntType(64))
        day = cgutils.alloca_once(builder, lir.IntType(64))
        hskb__uszc = lir.FunctionType(lir.VoidType(), [lir.IntType(64), lir
            .IntType(64), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer()])
        rey__vzqkd = cgutils.get_or_insert_function(builder.module,
            hskb__uszc, name='get_month_day')
        builder.call(rey__vzqkd, [args[0], args[1], month, day])
        return cgutils.pack_array(builder, [builder.load(month), builder.
            load(day)])
    return types.Tuple([types.int64, types.int64])(types.int64, types.int64
        ), codegen


@register_jitable
def get_day_of_year(year, month, day):
    rez__rugz = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365,
        0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
    azxz__kir = is_leap_year(year)
    kkumz__euccr = rez__rugz[azxz__kir * 13 + month - 1]
    exkrh__cjs = kkumz__euccr + day
    return exkrh__cjs


@register_jitable
def get_day_of_week(y, m, d):
    rfgv__oivlx = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    y -= m < 3
    day = (y + y // 4 - y // 100 + y // 400 + rfgv__oivlx[m - 1] + d) % 7
    return (day + 6) % 7


@register_jitable
def get_days_in_month(year, month):
    is_leap_year = year & 3 == 0 and (year % 100 != 0 or year % 400 == 0)
    ydszt__wrae = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31, 29, 
        31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return ydszt__wrae[12 * is_leap_year + month - 1]


@register_jitable
def is_leap_year(year):
    return year & 3 == 0 and (year % 100 != 0 or year % 400 == 0)


@numba.generated_jit(nopython=True)
def convert_val_to_timestamp(ts_input, tz=None, is_convert=True):
    nwx__gyrno = ejfsd__xmpj = np.array([])
    hzqu__gsoyc = '0'
    if is_overload_constant_str(tz):
        dxvbh__szm = get_overload_const_str(tz)
        nxe__zmvbj = pytz.timezone(dxvbh__szm)
        if isinstance(nxe__zmvbj, pytz.tzinfo.DstTzInfo):
            nwx__gyrno = np.array(nxe__zmvbj._utc_transition_times, dtype=
                'M8[ns]').view('i8')
            ejfsd__xmpj = np.array(nxe__zmvbj._transition_info)[:, 0]
            ejfsd__xmpj = (pd.Series(ejfsd__xmpj).dt.total_seconds() * 
                1000000000).astype(np.int64).values
            hzqu__gsoyc = (
                "deltas[np.searchsorted(trans, ts_input, side='right') - 1]")
        else:
            ejfsd__xmpj = np.int64(nxe__zmvbj._utcoffset.total_seconds() * 
                1000000000)
            hzqu__gsoyc = 'deltas'
    elif is_overload_constant_int(tz):
        xew__mqy = get_overload_const_int(tz)
        hzqu__gsoyc = str(xew__mqy)
    elif not is_overload_none(tz):
        raise_bodo_error(
            'convert_val_to_timestamp(): tz value must be a constant string or None'
            )
    is_convert = get_overload_const_bool(is_convert)
    if is_convert:
        igz__jib = 'tz_ts_input'
        wvj__yctr = 'ts_input'
    else:
        igz__jib = 'ts_input'
        wvj__yctr = 'tz_ts_input'
    nbtid__bzxv = 'def impl(ts_input, tz=None, is_convert=True):\n'
    nbtid__bzxv += f'  tz_ts_input = ts_input + {hzqu__gsoyc}\n'
    nbtid__bzxv += (
        f'  dt, year, days = extract_year_days(integer_to_dt64({igz__jib}))\n')
    nbtid__bzxv += '  month, day = get_month_day(year, days)\n'
    nbtid__bzxv += '  return init_timestamp(\n'
    nbtid__bzxv += '    year=year,\n'
    nbtid__bzxv += '    month=month,\n'
    nbtid__bzxv += '    day=day,\n'
    nbtid__bzxv += '    hour=dt // (60 * 60 * 1_000_000_000),\n'
    nbtid__bzxv += '    minute=(dt // (60 * 1_000_000_000)) % 60,\n'
    nbtid__bzxv += '    second=(dt // 1_000_000_000) % 60,\n'
    nbtid__bzxv += '    microsecond=(dt // 1000) % 1_000_000,\n'
    nbtid__bzxv += '    nanosecond=dt % 1000,\n'
    nbtid__bzxv += f'    value={wvj__yctr},\n'
    nbtid__bzxv += '    tz=tz,\n'
    nbtid__bzxv += '  )\n'
    jss__wzf = {}
    exec(nbtid__bzxv, {'np': np, 'pd': pd, 'trans': nwx__gyrno, 'deltas':
        ejfsd__xmpj, 'integer_to_dt64': integer_to_dt64,
        'extract_year_days': extract_year_days, 'get_month_day':
        get_month_day, 'init_timestamp': init_timestamp, 'zero_if_none':
        zero_if_none}, jss__wzf)
    impl = jss__wzf['impl']
    return impl


@numba.njit(no_cpython_wrapper=True)
def convert_datetime64_to_timestamp(dt64):
    oio__krlof, year, bngi__nemv = extract_year_days(dt64)
    month, day = get_month_day(year, bngi__nemv)
    return init_timestamp(year=year, month=month, day=day, hour=oio__krlof //
        (60 * 60 * 1000000000), minute=oio__krlof // (60 * 1000000000) % 60,
        second=oio__krlof // 1000000000 % 60, microsecond=oio__krlof // 
        1000 % 1000000, nanosecond=oio__krlof % 1000, value=dt64, tz=None)


@numba.njit(no_cpython_wrapper=True)
def convert_numpy_timedelta64_to_datetime_timedelta(dt64):
    esv__uohd = (bodo.hiframes.datetime_timedelta_ext.
        cast_numpy_timedelta_to_int(dt64))
    hynuw__oip = esv__uohd // (86400 * 1000000000)
    rbsg__zhluj = esv__uohd - hynuw__oip * 86400 * 1000000000
    zdgfb__grck = rbsg__zhluj // 1000000000
    akvg__tlrl = rbsg__zhluj - zdgfb__grck * 1000000000
    guwra__mkq = akvg__tlrl // 1000
    return datetime.timedelta(hynuw__oip, zdgfb__grck, guwra__mkq)


@numba.njit(no_cpython_wrapper=True)
def convert_numpy_timedelta64_to_pd_timedelta(dt64):
    esv__uohd = (bodo.hiframes.datetime_timedelta_ext.
        cast_numpy_timedelta_to_int(dt64))
    return pd.Timedelta(esv__uohd)


@intrinsic
def integer_to_timedelta64(typingctx, val=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return types.NPTimedelta('ns')(val), codegen


@intrinsic
def integer_to_dt64(typingctx, val=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return types.NPDatetime('ns')(val), codegen


@intrinsic
def dt64_to_integer(typingctx, val=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return types.int64(val), codegen


@lower_cast(types.NPDatetime('ns'), types.int64)
def cast_dt64_to_integer(context, builder, fromty, toty, val):
    return val


@overload_method(types.NPDatetime, '__hash__', no_unliteral=True)
def dt64_hash(val):
    return lambda val: hash(dt64_to_integer(val))


@overload_method(types.NPTimedelta, '__hash__', no_unliteral=True)
def td64_hash(val):
    return lambda val: hash(dt64_to_integer(val))


@intrinsic
def timedelta64_to_integer(typingctx, val=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return types.int64(val), codegen


@lower_cast(bodo.timedelta64ns, types.int64)
def cast_td64_to_integer(context, builder, fromty, toty, val):
    return val


@numba.njit
def parse_datetime_str(val):
    with numba.objmode(res='int64'):
        res = pd.Timestamp(val).value
    return integer_to_dt64(res)


@numba.njit
def datetime_timedelta_to_timedelta64(val):
    with numba.objmode(res='NPTimedelta("ns")'):
        res = pd.to_timedelta(val)
        res = res.to_timedelta64()
    return res


@numba.njit
def series_str_dt64_astype(data):
    with numba.objmode(res="NPDatetime('ns')[::1]"):
        res = pd.Series(data).astype('datetime64[ns]').values
    return res


@numba.njit
def series_str_td64_astype(data):
    with numba.objmode(res="NPTimedelta('ns')[::1]"):
        res = data.astype('timedelta64[ns]')
    return res


@numba.njit
def datetime_datetime_to_dt64(val):
    with numba.objmode(res='NPDatetime("ns")'):
        res = np.datetime64(val).astype('datetime64[ns]')
    return res


@register_jitable
def datetime_date_arr_to_dt64_arr(arr):
    with numba.objmode(res='NPDatetime("ns")[::1]'):
        res = np.array(arr, dtype='datetime64[ns]')
    return res


types.pd_timestamp_type = pd_timestamp_type


@register_jitable
def to_datetime_scalar(a, errors='raise', dayfirst=False, yearfirst=False,
    utc=None, format=None, exact=True, unit=None, infer_datetime_format=
    False, origin='unix', cache=True):
    with numba.objmode(t='pd_timestamp_type'):
        t = pd.to_datetime(a, errors=errors, dayfirst=dayfirst, yearfirst=
            yearfirst, utc=utc, format=format, exact=exact, unit=unit,
            infer_datetime_format=infer_datetime_format, origin=origin,
            cache=cache)
    return t


@numba.njit
def pandas_string_array_to_datetime(arr, errors, dayfirst, yearfirst, utc,
    format, exact, unit, infer_datetime_format, origin, cache):
    with numba.objmode(result='datetime_index'):
        result = pd.to_datetime(arr, errors=errors, dayfirst=dayfirst,
            yearfirst=yearfirst, utc=utc, format=format, exact=exact, unit=
            unit, infer_datetime_format=infer_datetime_format, origin=
            origin, cache=cache)
    return result


@numba.njit
def pandas_dict_string_array_to_datetime(arr, errors, dayfirst, yearfirst,
    utc, format, exact, unit, infer_datetime_format, origin, cache):
    sjix__mouqu = len(arr)
    xems__sic = np.empty(sjix__mouqu, 'datetime64[ns]')
    kvyry__mar = arr._indices
    fjfq__obwu = pandas_string_array_to_datetime(arr._data, errors,
        dayfirst, yearfirst, utc, format, exact, unit,
        infer_datetime_format, origin, cache).values
    for kbjy__xyl in range(sjix__mouqu):
        if bodo.libs.array_kernels.isna(kvyry__mar, kbjy__xyl):
            bodo.libs.array_kernels.setna(xems__sic, kbjy__xyl)
            continue
        xems__sic[kbjy__xyl] = fjfq__obwu[kvyry__mar[kbjy__xyl]]
    return xems__sic


@overload(pd.to_datetime, inline='always', no_unliteral=True)
def overload_to_datetime(arg_a, errors='raise', dayfirst=False, yearfirst=
    False, utc=None, format=None, exact=True, unit=None,
    infer_datetime_format=False, origin='unix', cache=True):
    if arg_a == bodo.string_type or is_overload_constant_str(arg_a
        ) or is_overload_constant_int(arg_a) or isinstance(arg_a, types.Integer
        ):

        def pd_to_datetime_impl(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            return to_datetime_scalar(arg_a, errors=errors, dayfirst=
                dayfirst, yearfirst=yearfirst, utc=utc, format=format,
                exact=exact, unit=unit, infer_datetime_format=
                infer_datetime_format, origin=origin, cache=cache)
        return pd_to_datetime_impl
    if isinstance(arg_a, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            frn__dho = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            owgxj__ddn = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            gqr__ucnxy = bodo.utils.conversion.coerce_to_ndarray(pd.
                to_datetime(arr, errors=errors, dayfirst=dayfirst,
                yearfirst=yearfirst, utc=utc, format=format, exact=exact,
                unit=unit, infer_datetime_format=infer_datetime_format,
                origin=origin, cache=cache))
            return bodo.hiframes.pd_series_ext.init_series(gqr__ucnxy,
                frn__dho, owgxj__ddn)
        return impl_series
    if arg_a == bodo.hiframes.datetime_date_ext.datetime_date_array_type:
        sco__wig = np.dtype('datetime64[ns]')
        iNaT = pd._libs.tslibs.iNaT

        def impl_date_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            sjix__mouqu = len(arg_a)
            xems__sic = np.empty(sjix__mouqu, sco__wig)
            for kbjy__xyl in numba.parfors.parfor.internal_prange(sjix__mouqu):
                val = iNaT
                if not bodo.libs.array_kernels.isna(arg_a, kbjy__xyl):
                    data = arg_a[kbjy__xyl]
                    val = (bodo.hiframes.pd_timestamp_ext.
                        npy_datetimestruct_to_datetime(data.year, data.
                        month, data.day, 0, 0, 0, 0))
                xems__sic[kbjy__xyl
                    ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(val)
            return bodo.hiframes.pd_index_ext.init_datetime_index(xems__sic,
                None)
        return impl_date_arr
    if arg_a == types.Array(types.NPDatetime('ns'), 1, 'C'):
        return (lambda arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True: bodo.
            hiframes.pd_index_ext.init_datetime_index(arg_a, None))
    if arg_a == string_array_type:

        def impl_string_array(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            return pandas_string_array_to_datetime(arg_a, errors, dayfirst,
                yearfirst, utc, format, exact, unit, infer_datetime_format,
                origin, cache)
        return impl_string_array
    if isinstance(arg_a, types.Array) and isinstance(arg_a.dtype, types.Integer
        ):
        sco__wig = np.dtype('datetime64[ns]')

        def impl_date_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            sjix__mouqu = len(arg_a)
            xems__sic = np.empty(sjix__mouqu, sco__wig)
            for kbjy__xyl in numba.parfors.parfor.internal_prange(sjix__mouqu):
                data = arg_a[kbjy__xyl]
                val = to_datetime_scalar(data, errors=errors, dayfirst=
                    dayfirst, yearfirst=yearfirst, utc=utc, format=format,
                    exact=exact, unit=unit, infer_datetime_format=
                    infer_datetime_format, origin=origin, cache=cache)
                xems__sic[kbjy__xyl
                    ] = bodo.hiframes.pd_timestamp_ext.datetime_datetime_to_dt64(
                    val)
            return bodo.hiframes.pd_index_ext.init_datetime_index(xems__sic,
                None)
        return impl_date_arr
    if isinstance(arg_a, CategoricalArrayType
        ) and arg_a.dtype.elem_type == bodo.string_type:
        sco__wig = np.dtype('datetime64[ns]')

        def impl_cat_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            sjix__mouqu = len(arg_a)
            xems__sic = np.empty(sjix__mouqu, sco__wig)
            cezx__cjzep = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arg_a))
            fjfq__obwu = pandas_string_array_to_datetime(arg_a.dtype.
                categories.values, errors, dayfirst, yearfirst, utc, format,
                exact, unit, infer_datetime_format, origin, cache).values
            for kbjy__xyl in numba.parfors.parfor.internal_prange(sjix__mouqu):
                c = cezx__cjzep[kbjy__xyl]
                if c == -1:
                    bodo.libs.array_kernels.setna(xems__sic, kbjy__xyl)
                    continue
                xems__sic[kbjy__xyl] = fjfq__obwu[c]
            return bodo.hiframes.pd_index_ext.init_datetime_index(xems__sic,
                None)
        return impl_cat_arr
    if arg_a == bodo.dict_str_arr_type:

        def impl_dict_str_arr(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            xems__sic = pandas_dict_string_array_to_datetime(arg_a, errors,
                dayfirst, yearfirst, utc, format, exact, unit,
                infer_datetime_format, origin, cache)
            return bodo.hiframes.pd_index_ext.init_datetime_index(xems__sic,
                None)
        return impl_dict_str_arr
    if isinstance(arg_a, PandasTimestampType):

        def impl_timestamp(arg_a, errors='raise', dayfirst=False, yearfirst
            =False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            return arg_a
        return impl_timestamp
    raise_bodo_error(f'pd.to_datetime(): cannot convert date type {arg_a}')


@overload(pd.to_timedelta, inline='always', no_unliteral=True)
def overload_to_timedelta(arg_a, unit='ns', errors='raise'):
    if not is_overload_constant_str(unit):
        raise BodoError(
            'pandas.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    if isinstance(arg_a, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(arg_a, unit='ns', errors='raise'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            frn__dho = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            owgxj__ddn = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            gqr__ucnxy = bodo.utils.conversion.coerce_to_ndarray(pd.
                to_timedelta(arr, unit, errors))
            return bodo.hiframes.pd_series_ext.init_series(gqr__ucnxy,
                frn__dho, owgxj__ddn)
        return impl_series
    if is_overload_constant_str(arg_a) or arg_a in (pd_timedelta_type,
        datetime_timedelta_type, bodo.string_type):

        def impl_string(arg_a, unit='ns', errors='raise'):
            return pd.Timedelta(arg_a)
        return impl_string
    if isinstance(arg_a, types.Float):
        m, mwd__yvdgp = pd._libs.tslibs.conversion.precision_from_unit(unit)

        def impl_float_scalar(arg_a, unit='ns', errors='raise'):
            val = float_to_timedelta_val(arg_a, mwd__yvdgp, m)
            return pd.Timedelta(val)
        return impl_float_scalar
    if isinstance(arg_a, types.Integer):
        m, tpnqc__tuyw = pd._libs.tslibs.conversion.precision_from_unit(unit)

        def impl_integer_scalar(arg_a, unit='ns', errors='raise'):
            return pd.Timedelta(arg_a * m)
        return impl_integer_scalar
    if is_iterable_type(arg_a) and not isinstance(arg_a, types.BaseTuple):
        m, mwd__yvdgp = pd._libs.tslibs.conversion.precision_from_unit(unit)
        dlr__reehi = np.dtype('timedelta64[ns]')
        if isinstance(arg_a.dtype, types.Float):

            def impl_float(arg_a, unit='ns', errors='raise'):
                sjix__mouqu = len(arg_a)
                xems__sic = np.empty(sjix__mouqu, dlr__reehi)
                for kbjy__xyl in numba.parfors.parfor.internal_prange(
                    sjix__mouqu):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, kbjy__xyl):
                        val = float_to_timedelta_val(arg_a[kbjy__xyl],
                            mwd__yvdgp, m)
                    xems__sic[kbjy__xyl
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    xems__sic, None)
            return impl_float
        if isinstance(arg_a.dtype, types.Integer):

            def impl_int(arg_a, unit='ns', errors='raise'):
                sjix__mouqu = len(arg_a)
                xems__sic = np.empty(sjix__mouqu, dlr__reehi)
                for kbjy__xyl in numba.parfors.parfor.internal_prange(
                    sjix__mouqu):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, kbjy__xyl):
                        val = arg_a[kbjy__xyl] * m
                    xems__sic[kbjy__xyl
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    xems__sic, None)
            return impl_int
        if arg_a.dtype == bodo.timedelta64ns:

            def impl_td64(arg_a, unit='ns', errors='raise'):
                arr = bodo.utils.conversion.coerce_to_ndarray(arg_a)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(arr,
                    None)
            return impl_td64
        if arg_a.dtype == bodo.string_type or isinstance(arg_a.dtype, types
            .UnicodeCharSeq):

            def impl_str(arg_a, unit='ns', errors='raise'):
                return pandas_string_array_to_timedelta(arg_a, unit, errors)
            return impl_str
        if arg_a.dtype == datetime_timedelta_type:

            def impl_datetime_timedelta(arg_a, unit='ns', errors='raise'):
                sjix__mouqu = len(arg_a)
                xems__sic = np.empty(sjix__mouqu, dlr__reehi)
                for kbjy__xyl in numba.parfors.parfor.internal_prange(
                    sjix__mouqu):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, kbjy__xyl):
                        accn__evl = arg_a[kbjy__xyl]
                        val = (accn__evl.microseconds + 1000 * 1000 * (
                            accn__evl.seconds + 24 * 60 * 60 * accn__evl.days)
                            ) * 1000
                    xems__sic[kbjy__xyl
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    xems__sic, None)
            return impl_datetime_timedelta
    raise_bodo_error(
        f'pd.to_timedelta(): cannot convert date type {arg_a.dtype}')


@register_jitable
def float_to_timedelta_val(data, precision, multiplier):
    jgwdj__sks = np.int64(data)
    uloye__dtu = data - jgwdj__sks
    if precision:
        uloye__dtu = np.round(uloye__dtu, precision)
    return jgwdj__sks * multiplier + np.int64(uloye__dtu * multiplier)


@numba.njit
def pandas_string_array_to_timedelta(arg_a, unit='ns', errors='raise'):
    with numba.objmode(result='timedelta_index'):
        result = pd.to_timedelta(arg_a, errors=errors)
    return result


def create_timestamp_cmp_op_overload(op):

    def overload_date_timestamp_cmp(lhs, rhs):
        if (lhs == pd_timestamp_type and rhs == bodo.hiframes.
            datetime_date_ext.datetime_date_type):
            return lambda lhs, rhs: op(lhs.value, bodo.hiframes.
                pd_timestamp_ext.npy_datetimestruct_to_datetime(rhs.year,
                rhs.month, rhs.day, 0, 0, 0, 0))
        if (lhs == bodo.hiframes.datetime_date_ext.datetime_date_type and 
            rhs == pd_timestamp_type):
            return lambda lhs, rhs: op(bodo.hiframes.pd_timestamp_ext.
                npy_datetimestruct_to_datetime(lhs.year, lhs.month, lhs.day,
                0, 0, 0, 0), rhs.value)
        if lhs == pd_timestamp_type and rhs == pd_timestamp_type:
            return lambda lhs, rhs: op(lhs.value, rhs.value)
        if lhs == pd_timestamp_type and rhs == bodo.datetime64ns:
            return lambda lhs, rhs: op(bodo.hiframes.pd_timestamp_ext.
                integer_to_dt64(lhs.value), rhs)
        if lhs == bodo.datetime64ns and rhs == pd_timestamp_type:
            return lambda lhs, rhs: op(lhs, bodo.hiframes.pd_timestamp_ext.
                integer_to_dt64(rhs.value))
    return overload_date_timestamp_cmp


@overload_method(PandasTimestampType, 'toordinal', no_unliteral=True)
def toordinal(date):

    def impl(date):
        return _ymd2ord(date.year, date.month, date.day)
    return impl


def overload_freq_methods(method):

    def freq_overload(td, freq, ambiguous='raise', nonexistent='raise'):
        check_tz_aware_unsupported(td, f'Timestamp.{method}()')
        ohyrd__aqk = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        dgpuo__iuils = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Timestamp.{method}', ohyrd__aqk,
            dgpuo__iuils, package_name='pandas', module_name='Timestamp')
        rxwjm__aez = ["freq == 'D'", "freq == 'H'",
            "freq == 'min' or freq == 'T'", "freq == 'S'",
            "freq == 'ms' or freq == 'L'", "freq == 'U' or freq == 'us'",
            "freq == 'N'"]
        gbay__zpiso = [24 * 60 * 60 * 1000000 * 1000, 60 * 60 * 1000000 * 
            1000, 60 * 1000000 * 1000, 1000000 * 1000, 1000 * 1000, 1000, 1]
        nbtid__bzxv = (
            "def impl(td, freq, ambiguous='raise', nonexistent='raise'):\n")
        for kbjy__xyl, knnzj__uhg in enumerate(rxwjm__aez):
            tifmf__suv = 'if' if kbjy__xyl == 0 else 'elif'
            nbtid__bzxv += '    {} {}:\n'.format(tifmf__suv, knnzj__uhg)
            nbtid__bzxv += '        unit_value = {}\n'.format(gbay__zpiso[
                kbjy__xyl])
        nbtid__bzxv += '    else:\n'
        nbtid__bzxv += (
            "        raise ValueError('Incorrect Frequency specification')\n")
        if td == pd_timedelta_type:
            nbtid__bzxv += (
                """    return pd.Timedelta(unit_value * np.int64(np.{}(td.value / unit_value)))
"""
                .format(method))
        elif td == pd_timestamp_type:
            if method == 'ceil':
                nbtid__bzxv += (
                    '    value = td.value + np.remainder(-td.value, unit_value)\n'
                    )
            if method == 'floor':
                nbtid__bzxv += (
                    '    value = td.value - np.remainder(td.value, unit_value)\n'
                    )
            if method == 'round':
                nbtid__bzxv += '    if unit_value == 1:\n'
                nbtid__bzxv += '        value = td.value\n'
                nbtid__bzxv += '    else:\n'
                nbtid__bzxv += (
                    '        quotient, remainder = np.divmod(td.value, unit_value)\n'
                    )
                nbtid__bzxv += """        mask = np.logical_or(remainder > (unit_value // 2), np.logical_and(remainder == (unit_value // 2), quotient % 2))
"""
                nbtid__bzxv += '        if mask:\n'
                nbtid__bzxv += '            quotient = quotient + 1\n'
                nbtid__bzxv += '        value = quotient * unit_value\n'
            nbtid__bzxv += '    return pd.Timestamp(value)\n'
        jss__wzf = {}
        exec(nbtid__bzxv, {'np': np, 'pd': pd}, jss__wzf)
        impl = jss__wzf['impl']
        return impl
    return freq_overload


def _install_freq_methods():
    cqmub__bgkw = ['ceil', 'floor', 'round']
    for method in cqmub__bgkw:
        shee__big = overload_freq_methods(method)
        overload_method(PDTimeDeltaType, method, no_unliteral=True)(shee__big)
        overload_method(PandasTimestampType, method, no_unliteral=True)(
            shee__big)


_install_freq_methods()


@register_jitable
def compute_pd_timestamp(totmicrosec, nanosecond):
    microsecond = totmicrosec % 1000000
    suovo__uvghi = totmicrosec // 1000000
    second = suovo__uvghi % 60
    yvvy__reeq = suovo__uvghi // 60
    minute = yvvy__reeq % 60
    xhe__rxum = yvvy__reeq // 60
    hour = xhe__rxum % 24
    qoezs__aeh = xhe__rxum // 24
    year, month, day = _ord2ymd(qoezs__aeh)
    value = npy_datetimestruct_to_datetime(year, month, day, hour, minute,
        second, microsecond)
    value += zero_if_none(nanosecond)
    return init_timestamp(year, month, day, hour, minute, second,
        microsecond, nanosecond, value, None)


def overload_sub_operator_timestamp(lhs, rhs):
    if lhs == pd_timestamp_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            nvw__mzu = lhs.toordinal()
            xpm__azzb = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            ygx__fxhi = lhs.microsecond
            nanosecond = lhs.nanosecond
            nfcpr__xgm = rhs.days
            zovo__fbn = rhs.seconds
            ulxf__xijy = rhs.microseconds
            ujo__lfku = nvw__mzu - nfcpr__xgm
            jtc__ylnbp = xpm__azzb - zovo__fbn
            oia__zdrk = ygx__fxhi - ulxf__xijy
            totmicrosec = 1000000 * (ujo__lfku * 86400 + jtc__ylnbp
                ) + oia__zdrk
            return compute_pd_timestamp(totmicrosec, nanosecond)
        return impl
    if lhs == pd_timestamp_type and rhs == pd_timestamp_type:

        def impl_timestamp(lhs, rhs):
            return convert_numpy_timedelta64_to_pd_timedelta(lhs.value -
                rhs.value)
        return impl_timestamp
    if lhs == pd_timestamp_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl


def overload_add_operator_timestamp(lhs, rhs):
    if lhs == pd_timestamp_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            nvw__mzu = lhs.toordinal()
            xpm__azzb = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            ygx__fxhi = lhs.microsecond
            nanosecond = lhs.nanosecond
            nfcpr__xgm = rhs.days
            zovo__fbn = rhs.seconds
            ulxf__xijy = rhs.microseconds
            ujo__lfku = nvw__mzu + nfcpr__xgm
            jtc__ylnbp = xpm__azzb + zovo__fbn
            oia__zdrk = ygx__fxhi + ulxf__xijy
            totmicrosec = 1000000 * (ujo__lfku * 86400 + jtc__ylnbp
                ) + oia__zdrk
            return compute_pd_timestamp(totmicrosec, nanosecond)
        return impl
    if lhs == pd_timestamp_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            nvw__mzu = lhs.toordinal()
            xpm__azzb = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            ygx__fxhi = lhs.microsecond
            vgx__sok = lhs.nanosecond
            ulxf__xijy = rhs.value // 1000
            fqy__gbzx = rhs.nanoseconds
            oia__zdrk = ygx__fxhi + ulxf__xijy
            totmicrosec = 1000000 * (nvw__mzu * 86400 + xpm__azzb) + oia__zdrk
            smtr__tlhx = vgx__sok + fqy__gbzx
            return compute_pd_timestamp(totmicrosec, smtr__tlhx)
        return impl
    if (lhs == pd_timedelta_type and rhs == pd_timestamp_type or lhs ==
        datetime_timedelta_type and rhs == pd_timestamp_type):

        def impl(lhs, rhs):
            return rhs + lhs
        return impl


@overload(min, no_unliteral=True)
def timestamp_min(lhs, rhs):
    check_tz_aware_unsupported(lhs, f'Timestamp.min()')
    check_tz_aware_unsupported(rhs, f'Timestamp.min()')
    if lhs == pd_timestamp_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            return lhs if lhs < rhs else rhs
        return impl


@overload(max, no_unliteral=True)
def timestamp_max(lhs, rhs):
    check_tz_aware_unsupported(lhs, f'Timestamp.max()')
    check_tz_aware_unsupported(rhs, f'Timestamp.max()')
    if lhs == pd_timestamp_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            return lhs if lhs > rhs else rhs
        return impl


@overload_method(DatetimeDateType, 'strftime')
@overload_method(PandasTimestampType, 'strftime')
def strftime(ts, format):
    if isinstance(ts, DatetimeDateType):
        myx__fak = 'datetime.date'
    else:
        myx__fak = 'pandas.Timestamp'
    if types.unliteral(format) != types.unicode_type:
        raise BodoError(
            f"{myx__fak}.strftime(): 'strftime' argument must be a string")

    def impl(ts, format):
        with numba.objmode(res='unicode_type'):
            res = ts.strftime(format)
        return res
    return impl


@overload_method(PandasTimestampType, 'to_datetime64')
def to_datetime64(ts):

    def impl(ts):
        return integer_to_dt64(ts.value)
    return impl


@register_jitable
def now_impl():
    with numba.objmode(d='pd_timestamp_type'):
        d = pd.Timestamp.now()
    return d


class CompDT64(ConcreteTemplate):
    cases = [signature(types.boolean, types.NPDatetime('ns'), types.
        NPDatetime('ns'))]


@infer_global(operator.lt)
class CmpOpLt(CompDT64):
    key = operator.lt


@infer_global(operator.le)
class CmpOpLe(CompDT64):
    key = operator.le


@infer_global(operator.gt)
class CmpOpGt(CompDT64):
    key = operator.gt


@infer_global(operator.ge)
class CmpOpGe(CompDT64):
    key = operator.ge


@infer_global(operator.eq)
class CmpOpEq(CompDT64):
    key = operator.eq


@infer_global(operator.ne)
class CmpOpNe(CompDT64):
    key = operator.ne


@typeof_impl.register(calendar._localized_month)
def typeof_python_calendar(val, c):
    return types.Tuple([types.StringLiteral(tlcf__jzxk) for tlcf__jzxk in val])


@overload(str)
def overload_datetime64_str(val):
    if val == bodo.datetime64ns:

        def impl(val):
            return (bodo.hiframes.pd_timestamp_ext.
                convert_datetime64_to_timestamp(val).isoformat('T'))
        return impl


timestamp_unsupported_attrs = ['asm8', 'components', 'freqstr', 'tz',
    'fold', 'tzinfo', 'freq']
timestamp_unsupported_methods = ['astimezone', 'ctime', 'dst', 'isoweekday',
    'replace', 'strptime', 'time', 'timestamp', 'timetuple', 'timetz',
    'to_julian_date', 'to_numpy', 'to_period', 'to_pydatetime', 'tzname',
    'utcoffset', 'utctimetuple']


def _install_pd_timestamp_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for utbw__ikjwi in timestamp_unsupported_attrs:
        ihds__demg = 'pandas.Timestamp.' + utbw__ikjwi
        overload_attribute(PandasTimestampType, utbw__ikjwi)(
            create_unsupported_overload(ihds__demg))
    for cmzsp__wxul in timestamp_unsupported_methods:
        ihds__demg = 'pandas.Timestamp.' + cmzsp__wxul
        overload_method(PandasTimestampType, cmzsp__wxul)(
            create_unsupported_overload(ihds__demg + '()'))


_install_pd_timestamp_unsupported()


@lower_builtin(numba.core.types.functions.NumberClass, pd_timestamp_type,
    types.StringLiteral)
def datetime64_constructor(context, builder, sig, args):

    def datetime64_constructor_impl(a, b):
        return integer_to_dt64(a.value)
    return context.compile_internal(builder, datetime64_constructor_impl,
        sig, args)
