"""
Implements window/aggregation array kernels that are specific to BodoSQL.
Specifically, window/aggregation array kernels that do not concern window
frames.
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import get_overload_const_bool, get_overload_const_str, is_overload_constant_bool, is_overload_constant_str, raise_bodo_error


def rank_sql(arr_tup, method='average', pct=False):
    return


@overload(rank_sql, no_unliteral=True)
def overload_rank_sql(arr_tup, method='average', pct=False):
    if not is_overload_constant_str(method):
        raise_bodo_error(
            "Series.rank(): 'method' argument must be a constant string")
    method = get_overload_const_str(method)
    if not is_overload_constant_bool(pct):
        raise_bodo_error(
            "Series.rank(): 'pct' argument must be a constant boolean")
    pct = get_overload_const_bool(pct)
    oia__bsksw = 'def impl(arr_tup, method="average", pct=False):\n'
    if method == 'first':
        oia__bsksw += '  ret = np.arange(1, n + 1, 1, np.float64)\n'
    else:
        oia__bsksw += (
            '  obs = bodo.libs.array_kernels._rank_detect_ties(arr_tup[0])\n')
        oia__bsksw += '  for arr in arr_tup:\n'
        oia__bsksw += (
            '    next_obs = bodo.libs.array_kernels._rank_detect_ties(arr)\n')
        oia__bsksw += '    obs = obs | next_obs \n'
        oia__bsksw += '  dense = obs.cumsum()\n'
        if method == 'dense':
            oia__bsksw += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
            oia__bsksw += '    dense,\n'
            oia__bsksw += '    new_dtype=np.float64,\n'
            oia__bsksw += '    copy=True,\n'
            oia__bsksw += '    nan_to_str=False,\n'
            oia__bsksw += '    from_series=True,\n'
            oia__bsksw += '  )\n'
        else:
            oia__bsksw += (
                '  count = np.concatenate((np.nonzero(obs)[0], np.array([len(obs)])))\n'
                )
            oia__bsksw += """  count_float = bodo.utils.conversion.fix_arr_dtype(count, new_dtype=np.float64, copy=True, nan_to_str=False, from_series=True)
"""
            if method == 'max':
                oia__bsksw += '  ret = count_float[dense]\n'
            elif method == 'min':
                oia__bsksw += '  ret = count_float[dense - 1] + 1\n'
            else:
                oia__bsksw += (
                    '  ret = 0.5 * (count_float[dense] + count_float[dense - 1] + 1)\n'
                    )
    if pct:
        if method == 'dense':
            oia__bsksw += '  div_val = np.max(ret)\n'
        else:
            oia__bsksw += '  div_val = arr.size\n'
        oia__bsksw += '  for i in range(len(ret)):\n'
        oia__bsksw += '    ret[i] = ret[i] / div_val\n'
    oia__bsksw += '  return ret\n'
    pvbi__csnrt = {}
    exec(oia__bsksw, {'np': np, 'pd': pd, 'bodo': bodo}, pvbi__csnrt)
    return pvbi__csnrt['impl']


@numba.generated_jit(nopython=True)
def change_event(S):

    def impl(S):
        wsnz__lycz = bodo.hiframes.pd_series_ext.get_series_data(S)
        yyi__bfhp = len(wsnz__lycz)
        abauz__ypyiw = bodo.utils.utils.alloc_type(yyi__bfhp, types.uint64, -1)
        zvja__pmndo = -1
        for wzjxy__zhjb in range(yyi__bfhp):
            abauz__ypyiw[wzjxy__zhjb] = 0
            if not bodo.libs.array_kernels.isna(wsnz__lycz, wzjxy__zhjb):
                zvja__pmndo = wzjxy__zhjb
                break
        if zvja__pmndo != -1:
            qqlcw__yqdsg = wsnz__lycz[zvja__pmndo]
            for wzjxy__zhjb in range(zvja__pmndo + 1, yyi__bfhp):
                if bodo.libs.array_kernels.isna(wsnz__lycz, wzjxy__zhjb
                    ) or wsnz__lycz[wzjxy__zhjb] == qqlcw__yqdsg:
                    abauz__ypyiw[wzjxy__zhjb] = abauz__ypyiw[wzjxy__zhjb - 1]
                else:
                    qqlcw__yqdsg = wsnz__lycz[wzjxy__zhjb]
                    abauz__ypyiw[wzjxy__zhjb] = abauz__ypyiw[wzjxy__zhjb - 1
                        ] + 1
        return bodo.hiframes.pd_series_ext.init_series(abauz__ypyiw, bodo.
            hiframes.pd_index_ext.init_range_index(0, yyi__bfhp, 1), None)
    return impl


@numba.generated_jit(nopython=True)
def windowed_sum(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_sum', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    yjxo__fht = 'res[i] = total'
    xzt__hbko = 'constant_value = S.sum()'
    selq__woe = 'total = 0'
    opw__qnf = 'total += elem'
    mrs__ajno = 'total -= elem'
    if isinstance(S.dtype, types.Integer):
        tuax__hzhtm = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    else:
        tuax__hzhtm = types.Array(bodo.float64, 1, 'C')
    return gen_windowed(yjxo__fht, xzt__hbko, tuax__hzhtm, setup_block=
        selq__woe, enter_block=opw__qnf, exit_block=mrs__ajno)


@numba.generated_jit(nopython=True)
def windowed_count(S, lower_bound, upper_bound):
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    yjxo__fht = 'res[i] = in_window'
    xzt__hbko = 'constant_value = S.count()'
    ihvk__leel = 'res[i] = 0'
    tuax__hzhtm = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_windowed(yjxo__fht, xzt__hbko, tuax__hzhtm, empty_block=
        ihvk__leel)


@numba.generated_jit(nopython=True)
def windowed_avg(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_avg', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    yjxo__fht = 'res[i] = total / in_window'
    xzt__hbko = 'constant_value = S.mean()'
    tuax__hzhtm = types.Array(bodo.float64, 1, 'C')
    selq__woe = 'total = 0'
    opw__qnf = 'total += elem'
    mrs__ajno = 'total -= elem'
    return gen_windowed(yjxo__fht, xzt__hbko, tuax__hzhtm, setup_block=
        selq__woe, enter_block=opw__qnf, exit_block=mrs__ajno)
