"""
Support for Series.dt attributes and methods
"""
import datetime
import operator
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import intrinsic, make_attribute_wrapper, models, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_series_ext import SeriesType, get_series_data, get_series_index, get_series_name, init_series
from bodo.libs.pd_datetime_arr_ext import PandasDatetimeTZDtype
from bodo.utils.typing import BodoError, ColNamesMetaType, check_unsupported_args, create_unsupported_overload, raise_bodo_error
dt64_dtype = np.dtype('datetime64[ns]')
timedelta64_dtype = np.dtype('timedelta64[ns]')


class SeriesDatetimePropertiesType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        msxfk__axb = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(msxfk__axb)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        doh__zsxyl = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, doh__zsxyl)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        tspbi__lsl, = args
        szxn__qdof = signature.return_type
        qmii__alr = cgutils.create_struct_proxy(szxn__qdof)(context, builder)
        qmii__alr.obj = tspbi__lsl
        context.nrt.incref(builder, signature.args[0], tspbi__lsl)
        return qmii__alr._getvalue()
    return SeriesDatetimePropertiesType(obj)(obj), codegen


@overload_attribute(SeriesType, 'dt')
def overload_series_dt(s):
    if not (bodo.hiframes.pd_series_ext.is_dt64_series_typ(s) or bodo.
        hiframes.pd_series_ext.is_timedelta64_series_typ(s)):
        raise_bodo_error('Can only use .dt accessor with datetimelike values.')
    return lambda s: bodo.hiframes.series_dt_impl.init_series_dt_properties(s)


def create_date_field_overload(field):

    def overload_field(S_dt):
        if S_dt.stype.dtype != types.NPDatetime('ns') and not isinstance(S_dt
            .stype.dtype, PandasDatetimeTZDtype):
            return
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
            f'Series.dt.{field}')
        oxblv__gxbdm = 'def impl(S_dt):\n'
        oxblv__gxbdm += '    S = S_dt._obj\n'
        oxblv__gxbdm += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        oxblv__gxbdm += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        oxblv__gxbdm += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        oxblv__gxbdm += '    numba.parfors.parfor.init_prange()\n'
        oxblv__gxbdm += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            oxblv__gxbdm += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            oxblv__gxbdm += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        oxblv__gxbdm += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        oxblv__gxbdm += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        oxblv__gxbdm += (
            '            bodo.libs.array_kernels.setna(out_arr, i)\n')
        oxblv__gxbdm += '            continue\n'
        oxblv__gxbdm += (
            '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])\n'
            )
        if field in ('year', 'month', 'day'):
            oxblv__gxbdm += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            if field in ('month', 'day'):
                oxblv__gxbdm += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            oxblv__gxbdm += '        out_arr[i] = {}\n'.format(field)
        elif field in ('dayofyear', 'day_of_year', 'dayofweek',
            'day_of_week', 'weekday'):
            dixsl__lltvz = {'dayofyear': 'get_day_of_year', 'day_of_year':
                'get_day_of_year', 'dayofweek': 'get_day_of_week',
                'day_of_week': 'get_day_of_week', 'weekday': 'get_day_of_week'}
            oxblv__gxbdm += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            oxblv__gxbdm += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            oxblv__gxbdm += (
                """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month, day)
"""
                .format(dixsl__lltvz[field]))
        elif field == 'is_leap_year':
            oxblv__gxbdm += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            oxblv__gxbdm += """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(year)
"""
        elif field in ('daysinmonth', 'days_in_month'):
            dixsl__lltvz = {'days_in_month': 'get_days_in_month',
                'daysinmonth': 'get_days_in_month'}
            oxblv__gxbdm += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            oxblv__gxbdm += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            oxblv__gxbdm += (
                '        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month)\n'
                .format(dixsl__lltvz[field]))
        else:
            oxblv__gxbdm += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            oxblv__gxbdm += '        out_arr[i] = ts.' + field + '\n'
        oxblv__gxbdm += """    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
        omn__ptekx = {}
        exec(oxblv__gxbdm, {'bodo': bodo, 'numba': numba, 'np': np}, omn__ptekx
            )
        impl = omn__ptekx['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        nci__hapdz = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(nci__hapdz)


_install_date_fields()


def create_date_method_overload(method):
    bvvg__gyucn = method in ['day_name', 'month_name']
    if bvvg__gyucn:
        oxblv__gxbdm = 'def overload_method(S_dt, locale=None):\n'
        oxblv__gxbdm += '    unsupported_args = dict(locale=locale)\n'
        oxblv__gxbdm += '    arg_defaults = dict(locale=None)\n'
        oxblv__gxbdm += '    bodo.utils.typing.check_unsupported_args(\n'
        oxblv__gxbdm += f"        'Series.dt.{method}',\n"
        oxblv__gxbdm += '        unsupported_args,\n'
        oxblv__gxbdm += '        arg_defaults,\n'
        oxblv__gxbdm += "        package_name='pandas',\n"
        oxblv__gxbdm += "        module_name='Series',\n"
        oxblv__gxbdm += '    )\n'
    else:
        oxblv__gxbdm = 'def overload_method(S_dt):\n'
        oxblv__gxbdm += f"""    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt, 'Series.dt.{method}()')
"""
    oxblv__gxbdm += """    if not (S_dt.stype.dtype == bodo.datetime64ns or isinstance(S_dt.stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
"""
    oxblv__gxbdm += '        return\n'
    if bvvg__gyucn:
        oxblv__gxbdm += '    def impl(S_dt, locale=None):\n'
    else:
        oxblv__gxbdm += '    def impl(S_dt):\n'
    oxblv__gxbdm += '        S = S_dt._obj\n'
    oxblv__gxbdm += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    oxblv__gxbdm += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    oxblv__gxbdm += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    oxblv__gxbdm += '        numba.parfors.parfor.init_prange()\n'
    oxblv__gxbdm += '        n = len(arr)\n'
    if bvvg__gyucn:
        oxblv__gxbdm += """        out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
    else:
        oxblv__gxbdm += (
            "        out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
    oxblv__gxbdm += (
        '        for i in numba.parfors.parfor.internal_prange(n):\n')
    oxblv__gxbdm += '            if bodo.libs.array_kernels.isna(arr, i):\n'
    oxblv__gxbdm += (
        '                bodo.libs.array_kernels.setna(out_arr, i)\n')
    oxblv__gxbdm += '                continue\n'
    oxblv__gxbdm += (
        '            ts = bodo.utils.conversion.box_if_dt64(arr[i])\n')
    oxblv__gxbdm += f'            method_val = ts.{method}()\n'
    if bvvg__gyucn:
        oxblv__gxbdm += '            out_arr[i] = method_val\n'
    else:
        oxblv__gxbdm += """            out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
    oxblv__gxbdm += """        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    oxblv__gxbdm += '    return impl\n'
    omn__ptekx = {}
    exec(oxblv__gxbdm, {'bodo': bodo, 'numba': numba, 'np': np}, omn__ptekx)
    overload_method = omn__ptekx['overload_method']
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        nci__hapdz = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            nci__hapdz)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return

    def impl(S_dt):
        kwdph__kkovg = S_dt._obj
        afc__ysp = bodo.hiframes.pd_series_ext.get_series_data(kwdph__kkovg)
        betpe__caqj = bodo.hiframes.pd_series_ext.get_series_index(kwdph__kkovg
            )
        msxfk__axb = bodo.hiframes.pd_series_ext.get_series_name(kwdph__kkovg)
        numba.parfors.parfor.init_prange()
        hplqm__ibcsz = len(afc__ysp)
        wowqc__egh = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            hplqm__ibcsz)
        for woq__dxg in numba.parfors.parfor.internal_prange(hplqm__ibcsz):
            uqy__fcfx = afc__ysp[woq__dxg]
            hgxhb__axzm = bodo.utils.conversion.box_if_dt64(uqy__fcfx)
            wowqc__egh[woq__dxg] = datetime.date(hgxhb__axzm.year,
                hgxhb__axzm.month, hgxhb__axzm.day)
        return bodo.hiframes.pd_series_ext.init_series(wowqc__egh,
            betpe__caqj, msxfk__axb)
    return impl


def create_series_dt_df_output_overload(attr):

    def series_dt_df_output_overload(S_dt):
        if not (attr == 'components' and S_dt.stype.dtype == types.
            NPTimedelta('ns') or attr == 'isocalendar' and (S_dt.stype.
            dtype == types.NPDatetime('ns') or isinstance(S_dt.stype.dtype,
            PandasDatetimeTZDtype))):
            return
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
            f'Series.dt.{attr}')
        if attr == 'components':
            nmgv__kqw = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            bowys__bys = 'convert_numpy_timedelta64_to_pd_timedelta'
            eztmo__mhztl = 'np.empty(n, np.int64)'
            yglcg__yruh = attr
        elif attr == 'isocalendar':
            nmgv__kqw = ['year', 'week', 'day']
            bowys__bys = 'convert_datetime64_to_timestamp'
            eztmo__mhztl = (
                'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)')
            yglcg__yruh = attr + '()'
        oxblv__gxbdm = 'def impl(S_dt):\n'
        oxblv__gxbdm += '    S = S_dt._obj\n'
        oxblv__gxbdm += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        oxblv__gxbdm += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        oxblv__gxbdm += '    numba.parfors.parfor.init_prange()\n'
        oxblv__gxbdm += '    n = len(arr)\n'
        for field in nmgv__kqw:
            oxblv__gxbdm += '    {} = {}\n'.format(field, eztmo__mhztl)
        oxblv__gxbdm += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        oxblv__gxbdm += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in nmgv__kqw:
            oxblv__gxbdm += (
                '            bodo.libs.array_kernels.setna({}, i)\n'.format
                (field))
        oxblv__gxbdm += '            continue\n'
        isyov__qaea = '(' + '[i], '.join(nmgv__kqw) + '[i])'
        oxblv__gxbdm += (
            '        {} = bodo.hiframes.pd_timestamp_ext.{}(arr[i]).{}\n'.
            format(isyov__qaea, bowys__bys, yglcg__yruh))
        xmwsv__ajwle = '(' + ', '.join(nmgv__kqw) + ')'
        oxblv__gxbdm += (
            """    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, __col_name_meta_value_series_dt_df_output)
"""
            .format(xmwsv__ajwle))
        omn__ptekx = {}
        exec(oxblv__gxbdm, {'bodo': bodo, 'numba': numba, 'np': np,
            '__col_name_meta_value_series_dt_df_output': ColNamesMetaType(
            tuple(nmgv__kqw))}, omn__ptekx)
        impl = omn__ptekx['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    zike__stvs = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, jtkxh__ybhrj in zike__stvs:
        nci__hapdz = create_series_dt_df_output_overload(attr)
        jtkxh__ybhrj(SeriesDatetimePropertiesType, attr, inline='always')(
            nci__hapdz)


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        oxblv__gxbdm = 'def impl(S_dt):\n'
        oxblv__gxbdm += '    S = S_dt._obj\n'
        oxblv__gxbdm += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        oxblv__gxbdm += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        oxblv__gxbdm += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        oxblv__gxbdm += '    numba.parfors.parfor.init_prange()\n'
        oxblv__gxbdm += '    n = len(A)\n'
        oxblv__gxbdm += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        oxblv__gxbdm += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        oxblv__gxbdm += '        if bodo.libs.array_kernels.isna(A, i):\n'
        oxblv__gxbdm += '            bodo.libs.array_kernels.setna(B, i)\n'
        oxblv__gxbdm += '            continue\n'
        oxblv__gxbdm += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if field == 'nanoseconds':
            oxblv__gxbdm += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            oxblv__gxbdm += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            oxblv__gxbdm += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            oxblv__gxbdm += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        oxblv__gxbdm += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        omn__ptekx = {}
        exec(oxblv__gxbdm, {'numba': numba, 'np': np, 'bodo': bodo}, omn__ptekx
            )
        impl = omn__ptekx['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        oxblv__gxbdm = 'def impl(S_dt):\n'
        oxblv__gxbdm += '    S = S_dt._obj\n'
        oxblv__gxbdm += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        oxblv__gxbdm += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        oxblv__gxbdm += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        oxblv__gxbdm += '    numba.parfors.parfor.init_prange()\n'
        oxblv__gxbdm += '    n = len(A)\n'
        if method == 'total_seconds':
            oxblv__gxbdm += '    B = np.empty(n, np.float64)\n'
        else:
            oxblv__gxbdm += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        oxblv__gxbdm += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        oxblv__gxbdm += '        if bodo.libs.array_kernels.isna(A, i):\n'
        oxblv__gxbdm += '            bodo.libs.array_kernels.setna(B, i)\n'
        oxblv__gxbdm += '            continue\n'
        oxblv__gxbdm += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if method == 'total_seconds':
            oxblv__gxbdm += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            oxblv__gxbdm += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            oxblv__gxbdm += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            oxblv__gxbdm += '    return B\n'
        omn__ptekx = {}
        exec(oxblv__gxbdm, {'numba': numba, 'np': np, 'bodo': bodo,
            'datetime': datetime}, omn__ptekx)
        impl = omn__ptekx['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        nci__hapdz = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(nci__hapdz)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        nci__hapdz = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            nci__hapdz)


_install_S_dt_timedelta_methods()


@overload_method(SeriesDatetimePropertiesType, 'strftime', inline='always',
    no_unliteral=True)
def dt_strftime(S_dt, date_format):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return
    if types.unliteral(date_format) != types.unicode_type:
        raise BodoError(
            "Series.str.strftime(): 'date_format' argument must be a string")

    def impl(S_dt, date_format):
        kwdph__kkovg = S_dt._obj
        ofeud__icgm = bodo.hiframes.pd_series_ext.get_series_data(kwdph__kkovg)
        betpe__caqj = bodo.hiframes.pd_series_ext.get_series_index(kwdph__kkovg
            )
        msxfk__axb = bodo.hiframes.pd_series_ext.get_series_name(kwdph__kkovg)
        numba.parfors.parfor.init_prange()
        hplqm__ibcsz = len(ofeud__icgm)
        npped__ijmt = bodo.libs.str_arr_ext.pre_alloc_string_array(hplqm__ibcsz
            , -1)
        for hxu__grl in numba.parfors.parfor.internal_prange(hplqm__ibcsz):
            if bodo.libs.array_kernels.isna(ofeud__icgm, hxu__grl):
                bodo.libs.array_kernels.setna(npped__ijmt, hxu__grl)
                continue
            npped__ijmt[hxu__grl] = bodo.utils.conversion.box_if_dt64(
                ofeud__icgm[hxu__grl]).strftime(date_format)
        return bodo.hiframes.pd_series_ext.init_series(npped__ijmt,
            betpe__caqj, msxfk__axb)
    return impl


@overload_method(SeriesDatetimePropertiesType, 'tz_convert', inline=
    'always', no_unliteral=True)
def overload_dt_tz_convert(S_dt, tz):

    def impl(S_dt, tz):
        kwdph__kkovg = S_dt._obj
        jdc__yeoy = get_series_data(kwdph__kkovg).tz_convert(tz)
        betpe__caqj = get_series_index(kwdph__kkovg)
        msxfk__axb = get_series_name(kwdph__kkovg)
        return init_series(jdc__yeoy, betpe__caqj, msxfk__axb)
    return impl


def create_timedelta_freq_overload(method):

    def freq_overload(S_dt, freq, ambiguous='raise', nonexistent='raise'):
        if S_dt.stype.dtype != types.NPTimedelta('ns'
            ) and S_dt.stype.dtype != types.NPDatetime('ns'
            ) and not isinstance(S_dt.stype.dtype, bodo.libs.
            pd_datetime_arr_ext.PandasDatetimeTZDtype):
            return
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
            f'Series.dt.{method}()')
        rxce__ewfzs = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        pmovc__gju = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Series.dt.{method}', rxce__ewfzs,
            pmovc__gju, package_name='pandas', module_name='Series')
        oxblv__gxbdm = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        oxblv__gxbdm += '    S = S_dt._obj\n'
        oxblv__gxbdm += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        oxblv__gxbdm += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        oxblv__gxbdm += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        oxblv__gxbdm += '    numba.parfors.parfor.init_prange()\n'
        oxblv__gxbdm += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            oxblv__gxbdm += (
                "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n")
        else:
            oxblv__gxbdm += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        oxblv__gxbdm += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        oxblv__gxbdm += '        if bodo.libs.array_kernels.isna(A, i):\n'
        oxblv__gxbdm += '            bodo.libs.array_kernels.setna(B, i)\n'
        oxblv__gxbdm += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            ticc__rfbt = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            smiho__awrgf = (
                'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64')
        else:
            ticc__rfbt = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            smiho__awrgf = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        oxblv__gxbdm += '        B[i] = {}({}(A[i]).{}(freq).value)\n'.format(
            smiho__awrgf, ticc__rfbt, method)
        oxblv__gxbdm += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        omn__ptekx = {}
        exec(oxblv__gxbdm, {'numba': numba, 'np': np, 'bodo': bodo}, omn__ptekx
            )
        impl = omn__ptekx['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    zboe__qpks = ['ceil', 'floor', 'round']
    for method in zboe__qpks:
        nci__hapdz = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            nci__hapdz)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            hgke__njfd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                qpe__wjm = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                cksl__vam = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    qpe__wjm)
                betpe__caqj = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                msxfk__axb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                mdwz__xbom = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                smcbj__fctm = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    mdwz__xbom)
                hplqm__ibcsz = len(cksl__vam)
                kwdph__kkovg = np.empty(hplqm__ibcsz, timedelta64_dtype)
                wnf__hjd = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hgke__njfd)
                for woq__dxg in numba.parfors.parfor.internal_prange(
                    hplqm__ibcsz):
                    bsf__bsd = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        cksl__vam[woq__dxg])
                    ourq__naz = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        smcbj__fctm[woq__dxg])
                    if bsf__bsd == wnf__hjd or ourq__naz == wnf__hjd:
                        qyka__lnwq = wnf__hjd
                    else:
                        qyka__lnwq = op(bsf__bsd, ourq__naz)
                    kwdph__kkovg[woq__dxg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        qyka__lnwq)
                return bodo.hiframes.pd_series_ext.init_series(kwdph__kkovg,
                    betpe__caqj, msxfk__axb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            hgke__njfd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                qay__qvjd = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                afc__ysp = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    qay__qvjd)
                betpe__caqj = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                msxfk__axb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                smcbj__fctm = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                hplqm__ibcsz = len(afc__ysp)
                kwdph__kkovg = np.empty(hplqm__ibcsz, dt64_dtype)
                wnf__hjd = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hgke__njfd)
                for woq__dxg in numba.parfors.parfor.internal_prange(
                    hplqm__ibcsz):
                    awgwf__bear = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(afc__ysp[woq__dxg]))
                    aba__vkqj = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(smcbj__fctm[woq__dxg]))
                    if awgwf__bear == wnf__hjd or aba__vkqj == wnf__hjd:
                        qyka__lnwq = wnf__hjd
                    else:
                        qyka__lnwq = op(awgwf__bear, aba__vkqj)
                    kwdph__kkovg[woq__dxg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        qyka__lnwq)
                return bodo.hiframes.pd_series_ext.init_series(kwdph__kkovg,
                    betpe__caqj, msxfk__axb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            hgke__njfd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                qay__qvjd = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                afc__ysp = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    qay__qvjd)
                betpe__caqj = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                msxfk__axb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                smcbj__fctm = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                hplqm__ibcsz = len(afc__ysp)
                kwdph__kkovg = np.empty(hplqm__ibcsz, dt64_dtype)
                wnf__hjd = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hgke__njfd)
                for woq__dxg in numba.parfors.parfor.internal_prange(
                    hplqm__ibcsz):
                    awgwf__bear = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(afc__ysp[woq__dxg]))
                    aba__vkqj = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(smcbj__fctm[woq__dxg]))
                    if awgwf__bear == wnf__hjd or aba__vkqj == wnf__hjd:
                        qyka__lnwq = wnf__hjd
                    else:
                        qyka__lnwq = op(awgwf__bear, aba__vkqj)
                    kwdph__kkovg[woq__dxg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        qyka__lnwq)
                return bodo.hiframes.pd_series_ext.init_series(kwdph__kkovg,
                    betpe__caqj, msxfk__axb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            hgke__njfd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                qay__qvjd = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                afc__ysp = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    qay__qvjd)
                betpe__caqj = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                msxfk__axb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                hplqm__ibcsz = len(afc__ysp)
                kwdph__kkovg = np.empty(hplqm__ibcsz, timedelta64_dtype)
                wnf__hjd = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hgke__njfd)
                pczo__xpaay = rhs.value
                for woq__dxg in numba.parfors.parfor.internal_prange(
                    hplqm__ibcsz):
                    awgwf__bear = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(afc__ysp[woq__dxg]))
                    if awgwf__bear == wnf__hjd or pczo__xpaay == wnf__hjd:
                        qyka__lnwq = wnf__hjd
                    else:
                        qyka__lnwq = op(awgwf__bear, pczo__xpaay)
                    kwdph__kkovg[woq__dxg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        qyka__lnwq)
                return bodo.hiframes.pd_series_ext.init_series(kwdph__kkovg,
                    betpe__caqj, msxfk__axb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            hgke__njfd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                qay__qvjd = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                afc__ysp = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    qay__qvjd)
                betpe__caqj = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                msxfk__axb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                hplqm__ibcsz = len(afc__ysp)
                kwdph__kkovg = np.empty(hplqm__ibcsz, timedelta64_dtype)
                wnf__hjd = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hgke__njfd)
                pczo__xpaay = lhs.value
                for woq__dxg in numba.parfors.parfor.internal_prange(
                    hplqm__ibcsz):
                    awgwf__bear = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(afc__ysp[woq__dxg]))
                    if pczo__xpaay == wnf__hjd or awgwf__bear == wnf__hjd:
                        qyka__lnwq = wnf__hjd
                    else:
                        qyka__lnwq = op(pczo__xpaay, awgwf__bear)
                    kwdph__kkovg[woq__dxg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        qyka__lnwq)
                return bodo.hiframes.pd_series_ext.init_series(kwdph__kkovg,
                    betpe__caqj, msxfk__axb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            hgke__njfd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                qay__qvjd = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                afc__ysp = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    qay__qvjd)
                betpe__caqj = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                msxfk__axb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                hplqm__ibcsz = len(afc__ysp)
                kwdph__kkovg = np.empty(hplqm__ibcsz, dt64_dtype)
                wnf__hjd = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hgke__njfd)
                zkvyz__wur = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                aba__vkqj = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(zkvyz__wur))
                for woq__dxg in numba.parfors.parfor.internal_prange(
                    hplqm__ibcsz):
                    awgwf__bear = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(afc__ysp[woq__dxg]))
                    if awgwf__bear == wnf__hjd or aba__vkqj == wnf__hjd:
                        qyka__lnwq = wnf__hjd
                    else:
                        qyka__lnwq = op(awgwf__bear, aba__vkqj)
                    kwdph__kkovg[woq__dxg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        qyka__lnwq)
                return bodo.hiframes.pd_series_ext.init_series(kwdph__kkovg,
                    betpe__caqj, msxfk__axb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            hgke__njfd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                qay__qvjd = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                afc__ysp = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    qay__qvjd)
                betpe__caqj = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                msxfk__axb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                hplqm__ibcsz = len(afc__ysp)
                kwdph__kkovg = np.empty(hplqm__ibcsz, dt64_dtype)
                wnf__hjd = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hgke__njfd)
                zkvyz__wur = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                aba__vkqj = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(zkvyz__wur))
                for woq__dxg in numba.parfors.parfor.internal_prange(
                    hplqm__ibcsz):
                    awgwf__bear = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(afc__ysp[woq__dxg]))
                    if awgwf__bear == wnf__hjd or aba__vkqj == wnf__hjd:
                        qyka__lnwq = wnf__hjd
                    else:
                        qyka__lnwq = op(awgwf__bear, aba__vkqj)
                    kwdph__kkovg[woq__dxg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        qyka__lnwq)
                return bodo.hiframes.pd_series_ext.init_series(kwdph__kkovg,
                    betpe__caqj, msxfk__axb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            hgke__njfd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                qay__qvjd = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                afc__ysp = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    qay__qvjd)
                betpe__caqj = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                msxfk__axb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                hplqm__ibcsz = len(afc__ysp)
                kwdph__kkovg = np.empty(hplqm__ibcsz, timedelta64_dtype)
                wnf__hjd = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hgke__njfd)
                ftbw__jpwd = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                awgwf__bear = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ftbw__jpwd)
                for woq__dxg in numba.parfors.parfor.internal_prange(
                    hplqm__ibcsz):
                    usjmq__yutt = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(afc__ysp[woq__dxg]))
                    if usjmq__yutt == wnf__hjd or awgwf__bear == wnf__hjd:
                        qyka__lnwq = wnf__hjd
                    else:
                        qyka__lnwq = op(usjmq__yutt, awgwf__bear)
                    kwdph__kkovg[woq__dxg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        qyka__lnwq)
                return bodo.hiframes.pd_series_ext.init_series(kwdph__kkovg,
                    betpe__caqj, msxfk__axb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            hgke__njfd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                qay__qvjd = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                afc__ysp = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    qay__qvjd)
                betpe__caqj = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                msxfk__axb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                hplqm__ibcsz = len(afc__ysp)
                kwdph__kkovg = np.empty(hplqm__ibcsz, timedelta64_dtype)
                wnf__hjd = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hgke__njfd)
                ftbw__jpwd = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                awgwf__bear = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ftbw__jpwd)
                for woq__dxg in numba.parfors.parfor.internal_prange(
                    hplqm__ibcsz):
                    usjmq__yutt = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(afc__ysp[woq__dxg]))
                    if awgwf__bear == wnf__hjd or usjmq__yutt == wnf__hjd:
                        qyka__lnwq = wnf__hjd
                    else:
                        qyka__lnwq = op(awgwf__bear, usjmq__yutt)
                    kwdph__kkovg[woq__dxg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        qyka__lnwq)
                return bodo.hiframes.pd_series_ext.init_series(kwdph__kkovg,
                    betpe__caqj, msxfk__axb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            hgke__njfd = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                afc__ysp = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                betpe__caqj = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                msxfk__axb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                hplqm__ibcsz = len(afc__ysp)
                kwdph__kkovg = np.empty(hplqm__ibcsz, timedelta64_dtype)
                wnf__hjd = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(hgke__njfd))
                zkvyz__wur = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                aba__vkqj = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(zkvyz__wur))
                for woq__dxg in numba.parfors.parfor.internal_prange(
                    hplqm__ibcsz):
                    hqn__ohh = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(afc__ysp[woq__dxg]))
                    if aba__vkqj == wnf__hjd or hqn__ohh == wnf__hjd:
                        qyka__lnwq = wnf__hjd
                    else:
                        qyka__lnwq = op(hqn__ohh, aba__vkqj)
                    kwdph__kkovg[woq__dxg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        qyka__lnwq)
                return bodo.hiframes.pd_series_ext.init_series(kwdph__kkovg,
                    betpe__caqj, msxfk__axb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            hgke__njfd = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                afc__ysp = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                betpe__caqj = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                msxfk__axb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                hplqm__ibcsz = len(afc__ysp)
                kwdph__kkovg = np.empty(hplqm__ibcsz, timedelta64_dtype)
                wnf__hjd = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(hgke__njfd))
                zkvyz__wur = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                aba__vkqj = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(zkvyz__wur))
                for woq__dxg in numba.parfors.parfor.internal_prange(
                    hplqm__ibcsz):
                    hqn__ohh = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(afc__ysp[woq__dxg]))
                    if aba__vkqj == wnf__hjd or hqn__ohh == wnf__hjd:
                        qyka__lnwq = wnf__hjd
                    else:
                        qyka__lnwq = op(aba__vkqj, hqn__ohh)
                    kwdph__kkovg[woq__dxg
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        qyka__lnwq)
                return bodo.hiframes.pd_series_ext.init_series(kwdph__kkovg,
                    betpe__caqj, msxfk__axb)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            kkydt__enr = True
        else:
            kkydt__enr = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            hgke__njfd = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                afc__ysp = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                betpe__caqj = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                msxfk__axb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                hplqm__ibcsz = len(afc__ysp)
                wowqc__egh = bodo.libs.bool_arr_ext.alloc_bool_array(
                    hplqm__ibcsz)
                wnf__hjd = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(hgke__njfd))
                ygg__pewgn = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                lhmgj__lkdw = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ygg__pewgn))
                for woq__dxg in numba.parfors.parfor.internal_prange(
                    hplqm__ibcsz):
                    tkz__omt = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(afc__ysp[woq__dxg]))
                    if tkz__omt == wnf__hjd or lhmgj__lkdw == wnf__hjd:
                        qyka__lnwq = kkydt__enr
                    else:
                        qyka__lnwq = op(tkz__omt, lhmgj__lkdw)
                    wowqc__egh[woq__dxg] = qyka__lnwq
                return bodo.hiframes.pd_series_ext.init_series(wowqc__egh,
                    betpe__caqj, msxfk__axb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            hgke__njfd = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                afc__ysp = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                betpe__caqj = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                msxfk__axb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                hplqm__ibcsz = len(afc__ysp)
                wowqc__egh = bodo.libs.bool_arr_ext.alloc_bool_array(
                    hplqm__ibcsz)
                wnf__hjd = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(hgke__njfd))
                znox__xamx = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                tkz__omt = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(znox__xamx))
                for woq__dxg in numba.parfors.parfor.internal_prange(
                    hplqm__ibcsz):
                    lhmgj__lkdw = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(afc__ysp[woq__dxg]))
                    if tkz__omt == wnf__hjd or lhmgj__lkdw == wnf__hjd:
                        qyka__lnwq = kkydt__enr
                    else:
                        qyka__lnwq = op(tkz__omt, lhmgj__lkdw)
                    wowqc__egh[woq__dxg] = qyka__lnwq
                return bodo.hiframes.pd_series_ext.init_series(wowqc__egh,
                    betpe__caqj, msxfk__axb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            hgke__njfd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                qay__qvjd = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                afc__ysp = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    qay__qvjd)
                betpe__caqj = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                msxfk__axb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                hplqm__ibcsz = len(afc__ysp)
                wowqc__egh = bodo.libs.bool_arr_ext.alloc_bool_array(
                    hplqm__ibcsz)
                wnf__hjd = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hgke__njfd)
                for woq__dxg in numba.parfors.parfor.internal_prange(
                    hplqm__ibcsz):
                    tkz__omt = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        afc__ysp[woq__dxg])
                    if tkz__omt == wnf__hjd or rhs.value == wnf__hjd:
                        qyka__lnwq = kkydt__enr
                    else:
                        qyka__lnwq = op(tkz__omt, rhs.value)
                    wowqc__egh[woq__dxg] = qyka__lnwq
                return bodo.hiframes.pd_series_ext.init_series(wowqc__egh,
                    betpe__caqj, msxfk__axb)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type and
            bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs)):
            hgke__njfd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                qay__qvjd = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                afc__ysp = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    qay__qvjd)
                betpe__caqj = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                msxfk__axb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                hplqm__ibcsz = len(afc__ysp)
                wowqc__egh = bodo.libs.bool_arr_ext.alloc_bool_array(
                    hplqm__ibcsz)
                wnf__hjd = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hgke__njfd)
                for woq__dxg in numba.parfors.parfor.internal_prange(
                    hplqm__ibcsz):
                    lhmgj__lkdw = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(afc__ysp[woq__dxg]))
                    if lhmgj__lkdw == wnf__hjd or lhs.value == wnf__hjd:
                        qyka__lnwq = kkydt__enr
                    else:
                        qyka__lnwq = op(lhs.value, lhmgj__lkdw)
                    wowqc__egh[woq__dxg] = qyka__lnwq
                return bodo.hiframes.pd_series_ext.init_series(wowqc__egh,
                    betpe__caqj, msxfk__axb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            hgke__njfd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                qay__qvjd = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                afc__ysp = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    qay__qvjd)
                betpe__caqj = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                msxfk__axb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                hplqm__ibcsz = len(afc__ysp)
                wowqc__egh = bodo.libs.bool_arr_ext.alloc_bool_array(
                    hplqm__ibcsz)
                wnf__hjd = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hgke__njfd)
                ppdp__grxku = (bodo.hiframes.pd_timestamp_ext.
                    parse_datetime_str(rhs))
                axafl__rdr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ppdp__grxku)
                for woq__dxg in numba.parfors.parfor.internal_prange(
                    hplqm__ibcsz):
                    tkz__omt = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        afc__ysp[woq__dxg])
                    if tkz__omt == wnf__hjd or axafl__rdr == wnf__hjd:
                        qyka__lnwq = kkydt__enr
                    else:
                        qyka__lnwq = op(tkz__omt, axafl__rdr)
                    wowqc__egh[woq__dxg] = qyka__lnwq
                return bodo.hiframes.pd_series_ext.init_series(wowqc__egh,
                    betpe__caqj, msxfk__axb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            hgke__njfd = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                qay__qvjd = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                afc__ysp = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    qay__qvjd)
                betpe__caqj = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                msxfk__axb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                hplqm__ibcsz = len(afc__ysp)
                wowqc__egh = bodo.libs.bool_arr_ext.alloc_bool_array(
                    hplqm__ibcsz)
                wnf__hjd = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hgke__njfd)
                ppdp__grxku = (bodo.hiframes.pd_timestamp_ext.
                    parse_datetime_str(lhs))
                axafl__rdr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ppdp__grxku)
                for woq__dxg in numba.parfors.parfor.internal_prange(
                    hplqm__ibcsz):
                    ftbw__jpwd = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(afc__ysp[woq__dxg]))
                    if ftbw__jpwd == wnf__hjd or axafl__rdr == wnf__hjd:
                        qyka__lnwq = kkydt__enr
                    else:
                        qyka__lnwq = op(axafl__rdr, ftbw__jpwd)
                    wowqc__egh[woq__dxg] = qyka__lnwq
                return bodo.hiframes.pd_series_ext.init_series(wowqc__egh,
                    betpe__caqj, msxfk__axb)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'to_period', 'to_pydatetime',
    'tz_localize', 'asfreq', 'to_timestamp'}
series_dt_unsupported_attrs = {'time', 'timetz', 'tz', 'freq', 'qyear',
    'start_time', 'end_time'}


def _install_series_dt_unsupported():
    for iqb__njm in series_dt_unsupported_attrs:
        szv__khfpp = 'Series.dt.' + iqb__njm
        overload_attribute(SeriesDatetimePropertiesType, iqb__njm)(
            create_unsupported_overload(szv__khfpp))
    for ekgp__gma in series_dt_unsupported_methods:
        szv__khfpp = 'Series.dt.' + ekgp__gma
        overload_method(SeriesDatetimePropertiesType, ekgp__gma,
            no_unliteral=True)(create_unsupported_overload(szv__khfpp))


_install_series_dt_unsupported()
