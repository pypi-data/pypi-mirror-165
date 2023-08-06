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
        ufwik__aypeo = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(ufwik__aypeo)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ubcuy__udry = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, ubcuy__udry)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        batp__ryj, = args
        bggns__zxn = signature.return_type
        caj__whuwj = cgutils.create_struct_proxy(bggns__zxn)(context, builder)
        caj__whuwj.obj = batp__ryj
        context.nrt.incref(builder, signature.args[0], batp__ryj)
        return caj__whuwj._getvalue()
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
        ucwvf__qqcok = 'def impl(S_dt):\n'
        ucwvf__qqcok += '    S = S_dt._obj\n'
        ucwvf__qqcok += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        ucwvf__qqcok += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        ucwvf__qqcok += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        ucwvf__qqcok += '    numba.parfors.parfor.init_prange()\n'
        ucwvf__qqcok += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            ucwvf__qqcok += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            ucwvf__qqcok += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        ucwvf__qqcok += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        ucwvf__qqcok += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        ucwvf__qqcok += (
            '            bodo.libs.array_kernels.setna(out_arr, i)\n')
        ucwvf__qqcok += '            continue\n'
        ucwvf__qqcok += (
            '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])\n'
            )
        if field in ('year', 'month', 'day'):
            ucwvf__qqcok += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            if field in ('month', 'day'):
                ucwvf__qqcok += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            ucwvf__qqcok += '        out_arr[i] = {}\n'.format(field)
        elif field in ('dayofyear', 'day_of_year', 'dayofweek',
            'day_of_week', 'weekday'):
            gensw__vbczr = {'dayofyear': 'get_day_of_year', 'day_of_year':
                'get_day_of_year', 'dayofweek': 'get_day_of_week',
                'day_of_week': 'get_day_of_week', 'weekday': 'get_day_of_week'}
            ucwvf__qqcok += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            ucwvf__qqcok += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            ucwvf__qqcok += (
                """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month, day)
"""
                .format(gensw__vbczr[field]))
        elif field == 'is_leap_year':
            ucwvf__qqcok += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            ucwvf__qqcok += """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(year)
"""
        elif field in ('daysinmonth', 'days_in_month'):
            gensw__vbczr = {'days_in_month': 'get_days_in_month',
                'daysinmonth': 'get_days_in_month'}
            ucwvf__qqcok += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            ucwvf__qqcok += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            ucwvf__qqcok += (
                '        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month)\n'
                .format(gensw__vbczr[field]))
        else:
            ucwvf__qqcok += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            ucwvf__qqcok += '        out_arr[i] = ts.' + field + '\n'
        ucwvf__qqcok += """    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
        pjocz__xnlrs = {}
        exec(ucwvf__qqcok, {'bodo': bodo, 'numba': numba, 'np': np},
            pjocz__xnlrs)
        impl = pjocz__xnlrs['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        wdgin__vllj = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(wdgin__vllj)


_install_date_fields()


def create_date_method_overload(method):
    psgia__drx = method in ['day_name', 'month_name']
    if psgia__drx:
        ucwvf__qqcok = 'def overload_method(S_dt, locale=None):\n'
        ucwvf__qqcok += '    unsupported_args = dict(locale=locale)\n'
        ucwvf__qqcok += '    arg_defaults = dict(locale=None)\n'
        ucwvf__qqcok += '    bodo.utils.typing.check_unsupported_args(\n'
        ucwvf__qqcok += f"        'Series.dt.{method}',\n"
        ucwvf__qqcok += '        unsupported_args,\n'
        ucwvf__qqcok += '        arg_defaults,\n'
        ucwvf__qqcok += "        package_name='pandas',\n"
        ucwvf__qqcok += "        module_name='Series',\n"
        ucwvf__qqcok += '    )\n'
    else:
        ucwvf__qqcok = 'def overload_method(S_dt):\n'
        ucwvf__qqcok += f"""    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt, 'Series.dt.{method}()')
"""
    ucwvf__qqcok += """    if not (S_dt.stype.dtype == bodo.datetime64ns or isinstance(S_dt.stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
"""
    ucwvf__qqcok += '        return\n'
    if psgia__drx:
        ucwvf__qqcok += '    def impl(S_dt, locale=None):\n'
    else:
        ucwvf__qqcok += '    def impl(S_dt):\n'
    ucwvf__qqcok += '        S = S_dt._obj\n'
    ucwvf__qqcok += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    ucwvf__qqcok += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    ucwvf__qqcok += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    ucwvf__qqcok += '        numba.parfors.parfor.init_prange()\n'
    ucwvf__qqcok += '        n = len(arr)\n'
    if psgia__drx:
        ucwvf__qqcok += """        out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
    else:
        ucwvf__qqcok += (
            "        out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
    ucwvf__qqcok += (
        '        for i in numba.parfors.parfor.internal_prange(n):\n')
    ucwvf__qqcok += '            if bodo.libs.array_kernels.isna(arr, i):\n'
    ucwvf__qqcok += (
        '                bodo.libs.array_kernels.setna(out_arr, i)\n')
    ucwvf__qqcok += '                continue\n'
    ucwvf__qqcok += (
        '            ts = bodo.utils.conversion.box_if_dt64(arr[i])\n')
    ucwvf__qqcok += f'            method_val = ts.{method}()\n'
    if psgia__drx:
        ucwvf__qqcok += '            out_arr[i] = method_val\n'
    else:
        ucwvf__qqcok += """            out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
    ucwvf__qqcok += """        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    ucwvf__qqcok += '    return impl\n'
    pjocz__xnlrs = {}
    exec(ucwvf__qqcok, {'bodo': bodo, 'numba': numba, 'np': np}, pjocz__xnlrs)
    overload_method = pjocz__xnlrs['overload_method']
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        wdgin__vllj = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            wdgin__vllj)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return

    def impl(S_dt):
        ysrv__raxe = S_dt._obj
        luqaw__mdwj = bodo.hiframes.pd_series_ext.get_series_data(ysrv__raxe)
        mrk__ghjht = bodo.hiframes.pd_series_ext.get_series_index(ysrv__raxe)
        ufwik__aypeo = bodo.hiframes.pd_series_ext.get_series_name(ysrv__raxe)
        numba.parfors.parfor.init_prange()
        kch__hoh = len(luqaw__mdwj)
        omds__mhhsg = (bodo.hiframes.datetime_date_ext.
            alloc_datetime_date_array(kch__hoh))
        for gvm__gzy in numba.parfors.parfor.internal_prange(kch__hoh):
            kqih__zqcwb = luqaw__mdwj[gvm__gzy]
            rdst__sxi = bodo.utils.conversion.box_if_dt64(kqih__zqcwb)
            omds__mhhsg[gvm__gzy] = datetime.date(rdst__sxi.year, rdst__sxi
                .month, rdst__sxi.day)
        return bodo.hiframes.pd_series_ext.init_series(omds__mhhsg,
            mrk__ghjht, ufwik__aypeo)
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
            lnopn__bjcz = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            pvt__sfjsh = 'convert_numpy_timedelta64_to_pd_timedelta'
            zxhh__hfrkm = 'np.empty(n, np.int64)'
            wdqb__tywcu = attr
        elif attr == 'isocalendar':
            lnopn__bjcz = ['year', 'week', 'day']
            pvt__sfjsh = 'convert_datetime64_to_timestamp'
            zxhh__hfrkm = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)'
            wdqb__tywcu = attr + '()'
        ucwvf__qqcok = 'def impl(S_dt):\n'
        ucwvf__qqcok += '    S = S_dt._obj\n'
        ucwvf__qqcok += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        ucwvf__qqcok += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        ucwvf__qqcok += '    numba.parfors.parfor.init_prange()\n'
        ucwvf__qqcok += '    n = len(arr)\n'
        for field in lnopn__bjcz:
            ucwvf__qqcok += '    {} = {}\n'.format(field, zxhh__hfrkm)
        ucwvf__qqcok += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        ucwvf__qqcok += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in lnopn__bjcz:
            ucwvf__qqcok += (
                '            bodo.libs.array_kernels.setna({}, i)\n'.format
                (field))
        ucwvf__qqcok += '            continue\n'
        fsjcc__vlp = '(' + '[i], '.join(lnopn__bjcz) + '[i])'
        ucwvf__qqcok += (
            '        {} = bodo.hiframes.pd_timestamp_ext.{}(arr[i]).{}\n'.
            format(fsjcc__vlp, pvt__sfjsh, wdqb__tywcu))
        lit__zoldd = '(' + ', '.join(lnopn__bjcz) + ')'
        ucwvf__qqcok += (
            """    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, __col_name_meta_value_series_dt_df_output)
"""
            .format(lit__zoldd))
        pjocz__xnlrs = {}
        exec(ucwvf__qqcok, {'bodo': bodo, 'numba': numba, 'np': np,
            '__col_name_meta_value_series_dt_df_output': ColNamesMetaType(
            tuple(lnopn__bjcz))}, pjocz__xnlrs)
        impl = pjocz__xnlrs['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    qmfkg__dser = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, lwvbw__sid in qmfkg__dser:
        wdgin__vllj = create_series_dt_df_output_overload(attr)
        lwvbw__sid(SeriesDatetimePropertiesType, attr, inline='always')(
            wdgin__vllj)


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        ucwvf__qqcok = 'def impl(S_dt):\n'
        ucwvf__qqcok += '    S = S_dt._obj\n'
        ucwvf__qqcok += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        ucwvf__qqcok += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        ucwvf__qqcok += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        ucwvf__qqcok += '    numba.parfors.parfor.init_prange()\n'
        ucwvf__qqcok += '    n = len(A)\n'
        ucwvf__qqcok += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        ucwvf__qqcok += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        ucwvf__qqcok += '        if bodo.libs.array_kernels.isna(A, i):\n'
        ucwvf__qqcok += '            bodo.libs.array_kernels.setna(B, i)\n'
        ucwvf__qqcok += '            continue\n'
        ucwvf__qqcok += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if field == 'nanoseconds':
            ucwvf__qqcok += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            ucwvf__qqcok += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            ucwvf__qqcok += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            ucwvf__qqcok += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        ucwvf__qqcok += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        pjocz__xnlrs = {}
        exec(ucwvf__qqcok, {'numba': numba, 'np': np, 'bodo': bodo},
            pjocz__xnlrs)
        impl = pjocz__xnlrs['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        ucwvf__qqcok = 'def impl(S_dt):\n'
        ucwvf__qqcok += '    S = S_dt._obj\n'
        ucwvf__qqcok += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        ucwvf__qqcok += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        ucwvf__qqcok += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        ucwvf__qqcok += '    numba.parfors.parfor.init_prange()\n'
        ucwvf__qqcok += '    n = len(A)\n'
        if method == 'total_seconds':
            ucwvf__qqcok += '    B = np.empty(n, np.float64)\n'
        else:
            ucwvf__qqcok += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        ucwvf__qqcok += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        ucwvf__qqcok += '        if bodo.libs.array_kernels.isna(A, i):\n'
        ucwvf__qqcok += '            bodo.libs.array_kernels.setna(B, i)\n'
        ucwvf__qqcok += '            continue\n'
        ucwvf__qqcok += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if method == 'total_seconds':
            ucwvf__qqcok += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            ucwvf__qqcok += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            ucwvf__qqcok += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            ucwvf__qqcok += '    return B\n'
        pjocz__xnlrs = {}
        exec(ucwvf__qqcok, {'numba': numba, 'np': np, 'bodo': bodo,
            'datetime': datetime}, pjocz__xnlrs)
        impl = pjocz__xnlrs['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        wdgin__vllj = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(wdgin__vllj)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        wdgin__vllj = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            wdgin__vllj)


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
        ysrv__raxe = S_dt._obj
        bjoa__tgir = bodo.hiframes.pd_series_ext.get_series_data(ysrv__raxe)
        mrk__ghjht = bodo.hiframes.pd_series_ext.get_series_index(ysrv__raxe)
        ufwik__aypeo = bodo.hiframes.pd_series_ext.get_series_name(ysrv__raxe)
        numba.parfors.parfor.init_prange()
        kch__hoh = len(bjoa__tgir)
        ibxb__hpmn = bodo.libs.str_arr_ext.pre_alloc_string_array(kch__hoh, -1)
        for svy__iozh in numba.parfors.parfor.internal_prange(kch__hoh):
            if bodo.libs.array_kernels.isna(bjoa__tgir, svy__iozh):
                bodo.libs.array_kernels.setna(ibxb__hpmn, svy__iozh)
                continue
            ibxb__hpmn[svy__iozh] = bodo.utils.conversion.box_if_dt64(
                bjoa__tgir[svy__iozh]).strftime(date_format)
        return bodo.hiframes.pd_series_ext.init_series(ibxb__hpmn,
            mrk__ghjht, ufwik__aypeo)
    return impl


@overload_method(SeriesDatetimePropertiesType, 'tz_convert', inline=
    'always', no_unliteral=True)
def overload_dt_tz_convert(S_dt, tz):

    def impl(S_dt, tz):
        ysrv__raxe = S_dt._obj
        rimh__wby = get_series_data(ysrv__raxe).tz_convert(tz)
        mrk__ghjht = get_series_index(ysrv__raxe)
        ufwik__aypeo = get_series_name(ysrv__raxe)
        return init_series(rimh__wby, mrk__ghjht, ufwik__aypeo)
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
        hmfv__zoqx = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        vho__boong = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Series.dt.{method}', hmfv__zoqx,
            vho__boong, package_name='pandas', module_name='Series')
        ucwvf__qqcok = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        ucwvf__qqcok += '    S = S_dt._obj\n'
        ucwvf__qqcok += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        ucwvf__qqcok += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        ucwvf__qqcok += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        ucwvf__qqcok += '    numba.parfors.parfor.init_prange()\n'
        ucwvf__qqcok += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            ucwvf__qqcok += (
                "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n")
        else:
            ucwvf__qqcok += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        ucwvf__qqcok += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        ucwvf__qqcok += '        if bodo.libs.array_kernels.isna(A, i):\n'
        ucwvf__qqcok += '            bodo.libs.array_kernels.setna(B, i)\n'
        ucwvf__qqcok += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            peued__wxqgc = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            cfeo__oanym = (
                'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64')
        else:
            peued__wxqgc = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            cfeo__oanym = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        ucwvf__qqcok += '        B[i] = {}({}(A[i]).{}(freq).value)\n'.format(
            cfeo__oanym, peued__wxqgc, method)
        ucwvf__qqcok += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        pjocz__xnlrs = {}
        exec(ucwvf__qqcok, {'numba': numba, 'np': np, 'bodo': bodo},
            pjocz__xnlrs)
        impl = pjocz__xnlrs['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    oxhk__zbz = ['ceil', 'floor', 'round']
    for method in oxhk__zbz:
        wdgin__vllj = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            wdgin__vllj)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            zyl__ehyax = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                nflk__nhyg = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                jjzi__dydm = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    nflk__nhyg)
                mrk__ghjht = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ufwik__aypeo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                hrob__papi = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                sfgbk__fhr = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    hrob__papi)
                kch__hoh = len(jjzi__dydm)
                ysrv__raxe = np.empty(kch__hoh, timedelta64_dtype)
                nstaq__dbpzr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    zyl__ehyax)
                for gvm__gzy in numba.parfors.parfor.internal_prange(kch__hoh):
                    yzsiw__zuaty = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(jjzi__dydm[gvm__gzy]))
                    bav__moqc = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        sfgbk__fhr[gvm__gzy])
                    if (yzsiw__zuaty == nstaq__dbpzr or bav__moqc ==
                        nstaq__dbpzr):
                        ehozd__gmmnh = nstaq__dbpzr
                    else:
                        ehozd__gmmnh = op(yzsiw__zuaty, bav__moqc)
                    ysrv__raxe[gvm__gzy
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        ehozd__gmmnh)
                return bodo.hiframes.pd_series_ext.init_series(ysrv__raxe,
                    mrk__ghjht, ufwik__aypeo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            zyl__ehyax = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ibr__nno = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                luqaw__mdwj = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ibr__nno)
                mrk__ghjht = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ufwik__aypeo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                sfgbk__fhr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                kch__hoh = len(luqaw__mdwj)
                ysrv__raxe = np.empty(kch__hoh, dt64_dtype)
                nstaq__dbpzr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    zyl__ehyax)
                for gvm__gzy in numba.parfors.parfor.internal_prange(kch__hoh):
                    nlvut__igtq = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(luqaw__mdwj[gvm__gzy]))
                    zjs__sxi = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(sfgbk__fhr[gvm__gzy]))
                    if nlvut__igtq == nstaq__dbpzr or zjs__sxi == nstaq__dbpzr:
                        ehozd__gmmnh = nstaq__dbpzr
                    else:
                        ehozd__gmmnh = op(nlvut__igtq, zjs__sxi)
                    ysrv__raxe[gvm__gzy
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        ehozd__gmmnh)
                return bodo.hiframes.pd_series_ext.init_series(ysrv__raxe,
                    mrk__ghjht, ufwik__aypeo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            zyl__ehyax = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ibr__nno = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                luqaw__mdwj = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ibr__nno)
                mrk__ghjht = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ufwik__aypeo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                sfgbk__fhr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                kch__hoh = len(luqaw__mdwj)
                ysrv__raxe = np.empty(kch__hoh, dt64_dtype)
                nstaq__dbpzr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    zyl__ehyax)
                for gvm__gzy in numba.parfors.parfor.internal_prange(kch__hoh):
                    nlvut__igtq = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(luqaw__mdwj[gvm__gzy]))
                    zjs__sxi = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(sfgbk__fhr[gvm__gzy]))
                    if nlvut__igtq == nstaq__dbpzr or zjs__sxi == nstaq__dbpzr:
                        ehozd__gmmnh = nstaq__dbpzr
                    else:
                        ehozd__gmmnh = op(nlvut__igtq, zjs__sxi)
                    ysrv__raxe[gvm__gzy
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        ehozd__gmmnh)
                return bodo.hiframes.pd_series_ext.init_series(ysrv__raxe,
                    mrk__ghjht, ufwik__aypeo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            zyl__ehyax = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ibr__nno = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                luqaw__mdwj = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ibr__nno)
                mrk__ghjht = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ufwik__aypeo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                kch__hoh = len(luqaw__mdwj)
                ysrv__raxe = np.empty(kch__hoh, timedelta64_dtype)
                nstaq__dbpzr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    zyl__ehyax)
                tqgd__bjkn = rhs.value
                for gvm__gzy in numba.parfors.parfor.internal_prange(kch__hoh):
                    nlvut__igtq = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(luqaw__mdwj[gvm__gzy]))
                    if (nlvut__igtq == nstaq__dbpzr or tqgd__bjkn ==
                        nstaq__dbpzr):
                        ehozd__gmmnh = nstaq__dbpzr
                    else:
                        ehozd__gmmnh = op(nlvut__igtq, tqgd__bjkn)
                    ysrv__raxe[gvm__gzy
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        ehozd__gmmnh)
                return bodo.hiframes.pd_series_ext.init_series(ysrv__raxe,
                    mrk__ghjht, ufwik__aypeo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            zyl__ehyax = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ibr__nno = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                luqaw__mdwj = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ibr__nno)
                mrk__ghjht = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ufwik__aypeo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                kch__hoh = len(luqaw__mdwj)
                ysrv__raxe = np.empty(kch__hoh, timedelta64_dtype)
                nstaq__dbpzr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    zyl__ehyax)
                tqgd__bjkn = lhs.value
                for gvm__gzy in numba.parfors.parfor.internal_prange(kch__hoh):
                    nlvut__igtq = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(luqaw__mdwj[gvm__gzy]))
                    if (tqgd__bjkn == nstaq__dbpzr or nlvut__igtq ==
                        nstaq__dbpzr):
                        ehozd__gmmnh = nstaq__dbpzr
                    else:
                        ehozd__gmmnh = op(tqgd__bjkn, nlvut__igtq)
                    ysrv__raxe[gvm__gzy
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        ehozd__gmmnh)
                return bodo.hiframes.pd_series_ext.init_series(ysrv__raxe,
                    mrk__ghjht, ufwik__aypeo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            zyl__ehyax = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ibr__nno = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                luqaw__mdwj = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ibr__nno)
                mrk__ghjht = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ufwik__aypeo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                kch__hoh = len(luqaw__mdwj)
                ysrv__raxe = np.empty(kch__hoh, dt64_dtype)
                nstaq__dbpzr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    zyl__ehyax)
                cjz__rqe = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                zjs__sxi = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(cjz__rqe))
                for gvm__gzy in numba.parfors.parfor.internal_prange(kch__hoh):
                    nlvut__igtq = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(luqaw__mdwj[gvm__gzy]))
                    if nlvut__igtq == nstaq__dbpzr or zjs__sxi == nstaq__dbpzr:
                        ehozd__gmmnh = nstaq__dbpzr
                    else:
                        ehozd__gmmnh = op(nlvut__igtq, zjs__sxi)
                    ysrv__raxe[gvm__gzy
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        ehozd__gmmnh)
                return bodo.hiframes.pd_series_ext.init_series(ysrv__raxe,
                    mrk__ghjht, ufwik__aypeo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            zyl__ehyax = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ibr__nno = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                luqaw__mdwj = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ibr__nno)
                mrk__ghjht = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ufwik__aypeo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                kch__hoh = len(luqaw__mdwj)
                ysrv__raxe = np.empty(kch__hoh, dt64_dtype)
                nstaq__dbpzr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    zyl__ehyax)
                cjz__rqe = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                zjs__sxi = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(cjz__rqe))
                for gvm__gzy in numba.parfors.parfor.internal_prange(kch__hoh):
                    nlvut__igtq = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(luqaw__mdwj[gvm__gzy]))
                    if nlvut__igtq == nstaq__dbpzr or zjs__sxi == nstaq__dbpzr:
                        ehozd__gmmnh = nstaq__dbpzr
                    else:
                        ehozd__gmmnh = op(nlvut__igtq, zjs__sxi)
                    ysrv__raxe[gvm__gzy
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        ehozd__gmmnh)
                return bodo.hiframes.pd_series_ext.init_series(ysrv__raxe,
                    mrk__ghjht, ufwik__aypeo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            zyl__ehyax = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ibr__nno = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                luqaw__mdwj = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ibr__nno)
                mrk__ghjht = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ufwik__aypeo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                kch__hoh = len(luqaw__mdwj)
                ysrv__raxe = np.empty(kch__hoh, timedelta64_dtype)
                nstaq__dbpzr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    zyl__ehyax)
                rmk__mvxj = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                nlvut__igtq = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    rmk__mvxj)
                for gvm__gzy in numba.parfors.parfor.internal_prange(kch__hoh):
                    lawg__zdgfx = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(luqaw__mdwj[gvm__gzy]))
                    if (lawg__zdgfx == nstaq__dbpzr or nlvut__igtq ==
                        nstaq__dbpzr):
                        ehozd__gmmnh = nstaq__dbpzr
                    else:
                        ehozd__gmmnh = op(lawg__zdgfx, nlvut__igtq)
                    ysrv__raxe[gvm__gzy
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        ehozd__gmmnh)
                return bodo.hiframes.pd_series_ext.init_series(ysrv__raxe,
                    mrk__ghjht, ufwik__aypeo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            zyl__ehyax = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ibr__nno = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                luqaw__mdwj = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ibr__nno)
                mrk__ghjht = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ufwik__aypeo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                kch__hoh = len(luqaw__mdwj)
                ysrv__raxe = np.empty(kch__hoh, timedelta64_dtype)
                nstaq__dbpzr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    zyl__ehyax)
                rmk__mvxj = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                nlvut__igtq = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    rmk__mvxj)
                for gvm__gzy in numba.parfors.parfor.internal_prange(kch__hoh):
                    lawg__zdgfx = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(luqaw__mdwj[gvm__gzy]))
                    if (nlvut__igtq == nstaq__dbpzr or lawg__zdgfx ==
                        nstaq__dbpzr):
                        ehozd__gmmnh = nstaq__dbpzr
                    else:
                        ehozd__gmmnh = op(nlvut__igtq, lawg__zdgfx)
                    ysrv__raxe[gvm__gzy
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        ehozd__gmmnh)
                return bodo.hiframes.pd_series_ext.init_series(ysrv__raxe,
                    mrk__ghjht, ufwik__aypeo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            zyl__ehyax = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                luqaw__mdwj = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                mrk__ghjht = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ufwik__aypeo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                kch__hoh = len(luqaw__mdwj)
                ysrv__raxe = np.empty(kch__hoh, timedelta64_dtype)
                nstaq__dbpzr = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(zyl__ehyax))
                cjz__rqe = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                zjs__sxi = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(cjz__rqe))
                for gvm__gzy in numba.parfors.parfor.internal_prange(kch__hoh):
                    rofk__mexrv = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(luqaw__mdwj[gvm__gzy]))
                    if zjs__sxi == nstaq__dbpzr or rofk__mexrv == nstaq__dbpzr:
                        ehozd__gmmnh = nstaq__dbpzr
                    else:
                        ehozd__gmmnh = op(rofk__mexrv, zjs__sxi)
                    ysrv__raxe[gvm__gzy
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        ehozd__gmmnh)
                return bodo.hiframes.pd_series_ext.init_series(ysrv__raxe,
                    mrk__ghjht, ufwik__aypeo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            zyl__ehyax = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                luqaw__mdwj = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                mrk__ghjht = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ufwik__aypeo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                kch__hoh = len(luqaw__mdwj)
                ysrv__raxe = np.empty(kch__hoh, timedelta64_dtype)
                nstaq__dbpzr = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(zyl__ehyax))
                cjz__rqe = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                zjs__sxi = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(cjz__rqe))
                for gvm__gzy in numba.parfors.parfor.internal_prange(kch__hoh):
                    rofk__mexrv = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(luqaw__mdwj[gvm__gzy]))
                    if zjs__sxi == nstaq__dbpzr or rofk__mexrv == nstaq__dbpzr:
                        ehozd__gmmnh = nstaq__dbpzr
                    else:
                        ehozd__gmmnh = op(zjs__sxi, rofk__mexrv)
                    ysrv__raxe[gvm__gzy
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        ehozd__gmmnh)
                return bodo.hiframes.pd_series_ext.init_series(ysrv__raxe,
                    mrk__ghjht, ufwik__aypeo)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            rxmcq__msrww = True
        else:
            rxmcq__msrww = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            zyl__ehyax = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                luqaw__mdwj = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                mrk__ghjht = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ufwik__aypeo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                kch__hoh = len(luqaw__mdwj)
                omds__mhhsg = bodo.libs.bool_arr_ext.alloc_bool_array(kch__hoh)
                nstaq__dbpzr = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(zyl__ehyax))
                njalm__wyee = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                wluu__icvse = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(njalm__wyee))
                for gvm__gzy in numba.parfors.parfor.internal_prange(kch__hoh):
                    ieops__xvg = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(luqaw__mdwj[gvm__gzy]))
                    if (ieops__xvg == nstaq__dbpzr or wluu__icvse ==
                        nstaq__dbpzr):
                        ehozd__gmmnh = rxmcq__msrww
                    else:
                        ehozd__gmmnh = op(ieops__xvg, wluu__icvse)
                    omds__mhhsg[gvm__gzy] = ehozd__gmmnh
                return bodo.hiframes.pd_series_ext.init_series(omds__mhhsg,
                    mrk__ghjht, ufwik__aypeo)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            zyl__ehyax = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                luqaw__mdwj = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                mrk__ghjht = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ufwik__aypeo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                kch__hoh = len(luqaw__mdwj)
                omds__mhhsg = bodo.libs.bool_arr_ext.alloc_bool_array(kch__hoh)
                nstaq__dbpzr = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(zyl__ehyax))
                kczsm__abdea = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                ieops__xvg = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(kczsm__abdea))
                for gvm__gzy in numba.parfors.parfor.internal_prange(kch__hoh):
                    wluu__icvse = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(luqaw__mdwj[gvm__gzy]))
                    if (ieops__xvg == nstaq__dbpzr or wluu__icvse ==
                        nstaq__dbpzr):
                        ehozd__gmmnh = rxmcq__msrww
                    else:
                        ehozd__gmmnh = op(ieops__xvg, wluu__icvse)
                    omds__mhhsg[gvm__gzy] = ehozd__gmmnh
                return bodo.hiframes.pd_series_ext.init_series(omds__mhhsg,
                    mrk__ghjht, ufwik__aypeo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            zyl__ehyax = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ibr__nno = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                luqaw__mdwj = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ibr__nno)
                mrk__ghjht = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ufwik__aypeo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                kch__hoh = len(luqaw__mdwj)
                omds__mhhsg = bodo.libs.bool_arr_ext.alloc_bool_array(kch__hoh)
                nstaq__dbpzr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    zyl__ehyax)
                for gvm__gzy in numba.parfors.parfor.internal_prange(kch__hoh):
                    ieops__xvg = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(luqaw__mdwj[gvm__gzy]))
                    if ieops__xvg == nstaq__dbpzr or rhs.value == nstaq__dbpzr:
                        ehozd__gmmnh = rxmcq__msrww
                    else:
                        ehozd__gmmnh = op(ieops__xvg, rhs.value)
                    omds__mhhsg[gvm__gzy] = ehozd__gmmnh
                return bodo.hiframes.pd_series_ext.init_series(omds__mhhsg,
                    mrk__ghjht, ufwik__aypeo)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type and
            bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs)):
            zyl__ehyax = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ibr__nno = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                luqaw__mdwj = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ibr__nno)
                mrk__ghjht = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ufwik__aypeo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                kch__hoh = len(luqaw__mdwj)
                omds__mhhsg = bodo.libs.bool_arr_ext.alloc_bool_array(kch__hoh)
                nstaq__dbpzr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    zyl__ehyax)
                for gvm__gzy in numba.parfors.parfor.internal_prange(kch__hoh):
                    wluu__icvse = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(luqaw__mdwj[gvm__gzy]))
                    if (wluu__icvse == nstaq__dbpzr or lhs.value ==
                        nstaq__dbpzr):
                        ehozd__gmmnh = rxmcq__msrww
                    else:
                        ehozd__gmmnh = op(lhs.value, wluu__icvse)
                    omds__mhhsg[gvm__gzy] = ehozd__gmmnh
                return bodo.hiframes.pd_series_ext.init_series(omds__mhhsg,
                    mrk__ghjht, ufwik__aypeo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            zyl__ehyax = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                ibr__nno = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                luqaw__mdwj = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ibr__nno)
                mrk__ghjht = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                ufwik__aypeo = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                kch__hoh = len(luqaw__mdwj)
                omds__mhhsg = bodo.libs.bool_arr_ext.alloc_bool_array(kch__hoh)
                nstaq__dbpzr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    zyl__ehyax)
                brm__wltc = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    rhs)
                owquq__gzk = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    brm__wltc)
                for gvm__gzy in numba.parfors.parfor.internal_prange(kch__hoh):
                    ieops__xvg = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(luqaw__mdwj[gvm__gzy]))
                    if (ieops__xvg == nstaq__dbpzr or owquq__gzk ==
                        nstaq__dbpzr):
                        ehozd__gmmnh = rxmcq__msrww
                    else:
                        ehozd__gmmnh = op(ieops__xvg, owquq__gzk)
                    omds__mhhsg[gvm__gzy] = ehozd__gmmnh
                return bodo.hiframes.pd_series_ext.init_series(omds__mhhsg,
                    mrk__ghjht, ufwik__aypeo)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            zyl__ehyax = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                ibr__nno = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                luqaw__mdwj = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ibr__nno)
                mrk__ghjht = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                ufwik__aypeo = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                kch__hoh = len(luqaw__mdwj)
                omds__mhhsg = bodo.libs.bool_arr_ext.alloc_bool_array(kch__hoh)
                nstaq__dbpzr = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    zyl__ehyax)
                brm__wltc = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    lhs)
                owquq__gzk = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    brm__wltc)
                for gvm__gzy in numba.parfors.parfor.internal_prange(kch__hoh):
                    rmk__mvxj = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        luqaw__mdwj[gvm__gzy])
                    if rmk__mvxj == nstaq__dbpzr or owquq__gzk == nstaq__dbpzr:
                        ehozd__gmmnh = rxmcq__msrww
                    else:
                        ehozd__gmmnh = op(owquq__gzk, rmk__mvxj)
                    omds__mhhsg[gvm__gzy] = ehozd__gmmnh
                return bodo.hiframes.pd_series_ext.init_series(omds__mhhsg,
                    mrk__ghjht, ufwik__aypeo)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'to_period', 'to_pydatetime',
    'tz_localize', 'asfreq', 'to_timestamp'}
series_dt_unsupported_attrs = {'time', 'timetz', 'tz', 'freq', 'qyear',
    'start_time', 'end_time'}


def _install_series_dt_unsupported():
    for ohbh__nsi in series_dt_unsupported_attrs:
        sqm__vvtj = 'Series.dt.' + ohbh__nsi
        overload_attribute(SeriesDatetimePropertiesType, ohbh__nsi)(
            create_unsupported_overload(sqm__vvtj))
    for oiw__och in series_dt_unsupported_methods:
        sqm__vvtj = 'Series.dt.' + oiw__och
        overload_method(SeriesDatetimePropertiesType, oiw__och,
            no_unliteral=True)(create_unsupported_overload(sqm__vvtj))


_install_series_dt_unsupported()
