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
    wij__lddz = 'def impl(arr_tup, method="average", pct=False):\n'
    if method == 'first':
        wij__lddz += '  ret = np.arange(1, n + 1, 1, np.float64)\n'
    else:
        wij__lddz += (
            '  obs = bodo.libs.array_kernels._rank_detect_ties(arr_tup[0])\n')
        wij__lddz += '  for arr in arr_tup:\n'
        wij__lddz += (
            '    next_obs = bodo.libs.array_kernels._rank_detect_ties(arr)\n')
        wij__lddz += '    obs = obs | next_obs \n'
        wij__lddz += '  dense = obs.cumsum()\n'
        if method == 'dense':
            wij__lddz += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
            wij__lddz += '    dense,\n'
            wij__lddz += '    new_dtype=np.float64,\n'
            wij__lddz += '    copy=True,\n'
            wij__lddz += '    nan_to_str=False,\n'
            wij__lddz += '    from_series=True,\n'
            wij__lddz += '  )\n'
        else:
            wij__lddz += (
                '  count = np.concatenate((np.nonzero(obs)[0], np.array([len(obs)])))\n'
                )
            wij__lddz += """  count_float = bodo.utils.conversion.fix_arr_dtype(count, new_dtype=np.float64, copy=True, nan_to_str=False, from_series=True)
"""
            if method == 'max':
                wij__lddz += '  ret = count_float[dense]\n'
            elif method == 'min':
                wij__lddz += '  ret = count_float[dense - 1] + 1\n'
            else:
                wij__lddz += (
                    '  ret = 0.5 * (count_float[dense] + count_float[dense - 1] + 1)\n'
                    )
    if pct:
        if method == 'dense':
            wij__lddz += '  div_val = np.max(ret)\n'
        else:
            wij__lddz += '  div_val = arr.size\n'
        wij__lddz += '  for i in range(len(ret)):\n'
        wij__lddz += '    ret[i] = ret[i] / div_val\n'
    wij__lddz += '  return ret\n'
    eij__fpn = {}
    exec(wij__lddz, {'np': np, 'pd': pd, 'bodo': bodo}, eij__fpn)
    return eij__fpn['impl']


@numba.generated_jit(nopython=True)
def change_event(S):

    def impl(S):
        xnfca__gbqsk = bodo.hiframes.pd_series_ext.get_series_data(S)
        axiac__sek = len(xnfca__gbqsk)
        jazcz__egg = bodo.utils.utils.alloc_type(axiac__sek, types.uint64, -1)
        luw__khn = -1
        for yhp__xhe in range(axiac__sek):
            jazcz__egg[yhp__xhe] = 0
            if not bodo.libs.array_kernels.isna(xnfca__gbqsk, yhp__xhe):
                luw__khn = yhp__xhe
                break
        if luw__khn != -1:
            imqal__jlkp = xnfca__gbqsk[luw__khn]
            for yhp__xhe in range(luw__khn + 1, axiac__sek):
                if bodo.libs.array_kernels.isna(xnfca__gbqsk, yhp__xhe
                    ) or xnfca__gbqsk[yhp__xhe] == imqal__jlkp:
                    jazcz__egg[yhp__xhe] = jazcz__egg[yhp__xhe - 1]
                else:
                    imqal__jlkp = xnfca__gbqsk[yhp__xhe]
                    jazcz__egg[yhp__xhe] = jazcz__egg[yhp__xhe - 1] + 1
        return bodo.hiframes.pd_series_ext.init_series(jazcz__egg, bodo.
            hiframes.pd_index_ext.init_range_index(0, axiac__sek, 1), None)
    return impl


@numba.generated_jit(nopython=True)
def windowed_sum(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_sum', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    doj__qxh = 'res[i] = total'
    jrf__ulp = 'constant_value = S.sum()'
    wvmni__ubmn = 'total = 0'
    vhng__dbjqf = 'total += elem'
    zusn__uxpt = 'total -= elem'
    if isinstance(S.dtype, types.Integer):
        rziuo__cedv = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    else:
        rziuo__cedv = types.Array(bodo.float64, 1, 'C')
    return gen_windowed(doj__qxh, jrf__ulp, rziuo__cedv, setup_block=
        wvmni__ubmn, enter_block=vhng__dbjqf, exit_block=zusn__uxpt)


@numba.generated_jit(nopython=True)
def windowed_count(S, lower_bound, upper_bound):
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    doj__qxh = 'res[i] = in_window'
    jrf__ulp = 'constant_value = S.count()'
    czpxx__bvwdt = 'res[i] = 0'
    rziuo__cedv = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_windowed(doj__qxh, jrf__ulp, rziuo__cedv, empty_block=
        czpxx__bvwdt)


@numba.generated_jit(nopython=True)
def windowed_avg(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_avg', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    doj__qxh = 'res[i] = total / in_window'
    jrf__ulp = 'constant_value = S.mean()'
    rziuo__cedv = types.Array(bodo.float64, 1, 'C')
    wvmni__ubmn = 'total = 0'
    vhng__dbjqf = 'total += elem'
    zusn__uxpt = 'total -= elem'
    return gen_windowed(doj__qxh, jrf__ulp, rziuo__cedv, setup_block=
        wvmni__ubmn, enter_block=vhng__dbjqf, exit_block=zusn__uxpt)
