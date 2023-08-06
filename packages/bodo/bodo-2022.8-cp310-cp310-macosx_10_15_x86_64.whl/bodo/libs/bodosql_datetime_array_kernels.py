"""
Implements datetime array kernels that are specific to BodoSQL
"""
import numba
import numpy as np
from numba.core import types
import bodo
from bodo.libs.bodosql_array_kernel_utils import *


@numba.generated_jit(nopython=True)
def dayname(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.dayname_util',
            ['arr'], 0)

    def impl(arr):
        return dayname_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def day_timestamp(arr):
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.day_timestamp_util', ['arr'], 0)

    def impl(arr):
        return day_timestamp_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def int_to_days(arr):
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.int_to_days_util', ['arr'], 0)

    def impl(arr):
        return int_to_days_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def last_day(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.last_day_util',
            ['arr'], 0)

    def impl(arr):
        return last_day_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def makedate(year, day):
    args = [year, day]
    for wyypd__oqzli in range(2):
        if isinstance(args[wyypd__oqzli], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.makedate',
                ['year', 'day'], wyypd__oqzli)

    def impl(year, day):
        return makedate_util(year, day)
    return impl


@numba.generated_jit(nopython=True)
def monthname(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.monthname_util',
            ['arr'], 0)

    def impl(arr):
        return monthname_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def month_diff(arr0, arr1):
    args = [arr0, arr1]
    for wyypd__oqzli in range(2):
        if isinstance(args[wyypd__oqzli], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.month_diff',
                ['arr0', 'arr1'], wyypd__oqzli)

    def impl(arr0, arr1):
        return month_diff_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def second_timestamp(arr):
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.second_timestamp_util', ['arr'], 0
            )

    def impl(arr):
        return second_timestamp_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def weekday(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.weekday_util',
            ['arr'], 0)

    def impl(arr):
        return weekday_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def yearofweekiso(arr):
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.yearofweekiso_util', ['arr'], 0)

    def impl(arr):
        return yearofweekiso_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def dayname_util(arr):
    verify_datetime_arg(arr, 'DAYNAME', 'arr')
    lndi__fbdir = ['arr']
    uqck__raoa = [arr]
    xmz__itak = [True]
    ytlo__anpf = 'res[i] = pd.Timestamp(arg0).day_name()'
    ioc__rnjp = bodo.string_array_type
    return gen_vectorized(lndi__fbdir, uqck__raoa, xmz__itak, ytlo__anpf,
        ioc__rnjp)


@numba.generated_jit(nopython=True)
def day_timestamp_util(arr):
    verify_int_arg(arr, 'day_timestamp', 'arr')
    lndi__fbdir = ['arr']
    uqck__raoa = [arr]
    xmz__itak = [True]
    ytlo__anpf = (
        "res[i] = bodo.utils.conversion.unbox_if_timestamp(pd.Timestamp(arg0, unit='D'))"
        )
    ioc__rnjp = np.dtype('datetime64[ns]')
    return gen_vectorized(lndi__fbdir, uqck__raoa, xmz__itak, ytlo__anpf,
        ioc__rnjp)


@numba.generated_jit(nopython=True)
def int_to_days_util(arr):
    verify_int_arg(arr, 'int_to_days', 'arr')
    lndi__fbdir = ['arr']
    uqck__raoa = [arr]
    xmz__itak = [True]
    ytlo__anpf = (
        'res[i] = bodo.utils.conversion.unbox_if_timestamp(pd.Timedelta(days=arg0))'
        )
    ioc__rnjp = np.dtype('timedelta64[ns]')
    return gen_vectorized(lndi__fbdir, uqck__raoa, xmz__itak, ytlo__anpf,
        ioc__rnjp)


@numba.generated_jit(nopython=True)
def last_day_util(arr):
    verify_datetime_arg(arr, 'LAST_DAY', 'arr')
    lndi__fbdir = ['arr']
    uqck__raoa = [arr]
    xmz__itak = [True]
    ytlo__anpf = (
        'res[i] = bodo.utils.conversion.unbox_if_timestamp(pd.Timestamp(arg0) + pd.tseries.offsets.MonthEnd(n=0, normalize=True))'
        )
    ioc__rnjp = np.dtype('datetime64[ns]')
    return gen_vectorized(lndi__fbdir, uqck__raoa, xmz__itak, ytlo__anpf,
        ioc__rnjp)


@numba.generated_jit(nopython=True)
def makedate_util(year, day):
    verify_int_arg(year, 'MAKEDATE', 'year')
    verify_int_arg(day, 'MAKEDATE', 'day')
    lndi__fbdir = ['year', 'day']
    uqck__raoa = [year, day]
    xmz__itak = [True] * 2
    ytlo__anpf = (
        'res[i] = bodo.utils.conversion.unbox_if_timestamp(pd.Timestamp(year=arg0, month=1, day=1) + pd.Timedelta(days=arg1-1))'
        )
    ioc__rnjp = np.dtype('datetime64[ns]')
    return gen_vectorized(lndi__fbdir, uqck__raoa, xmz__itak, ytlo__anpf,
        ioc__rnjp)


@numba.generated_jit(nopython=True)
def monthname_util(arr):
    verify_datetime_arg(arr, 'MONTHNAME', 'arr')
    lndi__fbdir = ['arr']
    uqck__raoa = [arr]
    xmz__itak = [True]
    ytlo__anpf = 'res[i] = pd.Timestamp(arg0).month_name()'
    ioc__rnjp = bodo.string_array_type
    return gen_vectorized(lndi__fbdir, uqck__raoa, xmz__itak, ytlo__anpf,
        ioc__rnjp)


@numba.generated_jit(nopython=True)
def month_diff_util(arr0, arr1):
    verify_datetime_arg(arr0, 'month_diff', 'arr0')
    verify_datetime_arg(arr1, 'month_diff', 'arr1')
    lndi__fbdir = ['arr0', 'arr1']
    uqck__raoa = [arr0, arr1]
    xmz__itak = [True] * 2
    ytlo__anpf = 'A0 = bodo.utils.conversion.box_if_dt64(arg0)\n'
    ytlo__anpf += 'A1 = bodo.utils.conversion.box_if_dt64(arg1)\n'
    ytlo__anpf += 'delta = 12 * (A0.year - A1.year) + (A0.month - A1.month)\n'
    ytlo__anpf += (
        'remainder = ((A0 - pd.DateOffset(months=delta)) - A1).value\n')
    ytlo__anpf += 'if delta > 0 and remainder < 0:\n'
    ytlo__anpf += '   res[i] = -(delta - 1)\n'
    ytlo__anpf += 'elif delta < 0 and remainder > 0:\n'
    ytlo__anpf += '   res[i] = -(delta + 1)\n'
    ytlo__anpf += 'else:\n'
    ytlo__anpf += '   res[i] = -delta'
    ioc__rnjp = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(lndi__fbdir, uqck__raoa, xmz__itak, ytlo__anpf,
        ioc__rnjp)


@numba.generated_jit(nopython=True)
def second_timestamp_util(arr):
    verify_int_arg(arr, 'second_timestamp', 'arr')
    lndi__fbdir = ['arr']
    uqck__raoa = [arr]
    xmz__itak = [True]
    ytlo__anpf = (
        "res[i] = bodo.utils.conversion.unbox_if_timestamp(pd.Timestamp(arg0, unit='s'))"
        )
    ioc__rnjp = np.dtype('datetime64[ns]')
    return gen_vectorized(lndi__fbdir, uqck__raoa, xmz__itak, ytlo__anpf,
        ioc__rnjp)


@numba.generated_jit(nopython=True)
def weekday_util(arr):
    verify_datetime_arg(arr, 'WEEKDAY', 'arr')
    lndi__fbdir = ['arr']
    uqck__raoa = [arr]
    xmz__itak = [True]
    ytlo__anpf = 'dt = pd.Timestamp(arg0)\n'
    ytlo__anpf += (
        'res[i] = bodo.hiframes.pd_timestamp_ext.get_day_of_week(dt.year, dt.month, dt.day)'
        )
    ioc__rnjp = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(lndi__fbdir, uqck__raoa, xmz__itak, ytlo__anpf,
        ioc__rnjp)


@numba.generated_jit(nopython=True)
def yearofweekiso_util(arr):
    verify_datetime_arg(arr, 'YEAROFWEEKISO', 'arr')
    lndi__fbdir = ['arr']
    uqck__raoa = [arr]
    xmz__itak = [True]
    ytlo__anpf = 'dt = pd.Timestamp(arg0)\n'
    ytlo__anpf += 'res[i] = dt.isocalendar()[0]'
    ioc__rnjp = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(lndi__fbdir, uqck__raoa, xmz__itak, ytlo__anpf,
        ioc__rnjp)
