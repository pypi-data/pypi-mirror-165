"""implementations of rolling window functions (sequential and parallel)
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.core.imputils import impl_ret_borrowed
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_builtin, overload, register_jitable
import bodo
from bodo.libs.distributed_api import Reduce_Type
from bodo.utils.typing import BodoError, decode_if_dict_array, get_overload_const_func, get_overload_const_str, is_const_func_type, is_overload_constant_bool, is_overload_constant_str, is_overload_none, is_overload_true
from bodo.utils.utils import unliteral_all
supported_rolling_funcs = ('sum', 'mean', 'var', 'std', 'count', 'median',
    'min', 'max', 'cov', 'corr', 'apply')
unsupported_rolling_methods = ['skew', 'kurt', 'aggregate', 'quantile', 'sem']


def rolling_fixed(arr, win):
    return arr


def rolling_variable(arr, on_arr, win):
    return arr


def rolling_cov(arr, arr2, win):
    return arr


def rolling_corr(arr, arr2, win):
    return arr


@infer_global(rolling_cov)
@infer_global(rolling_corr)
class RollingCovType(AbstractTemplate):

    def generic(self, args, kws):
        arr = args[0]
        farsn__xwdiy = arr.copy(dtype=types.float64)
        return signature(farsn__xwdiy, *unliteral_all(args))


@lower_builtin(rolling_corr, types.VarArg(types.Any))
@lower_builtin(rolling_cov, types.VarArg(types.Any))
def lower_rolling_corr_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


@overload(rolling_fixed, no_unliteral=True)
def overload_rolling_fixed(arr, index_arr, win, minp, center, fname, raw=
    True, parallel=False):
    assert is_overload_constant_bool(raw
        ), 'raw argument should be constant bool'
    if is_const_func_type(fname):
        func = _get_apply_func(fname)
        return (lambda arr, index_arr, win, minp, center, fname, raw=True,
            parallel=False: roll_fixed_apply(arr, index_arr, win, minp,
            center, parallel, func, raw))
    assert is_overload_constant_str(fname)
    vyzu__bylzh = get_overload_const_str(fname)
    if vyzu__bylzh not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (fixed window) function {}'.format
            (vyzu__bylzh))
    if vyzu__bylzh in ('median', 'min', 'max'):
        hbyz__japel = 'def kernel_func(A):\n'
        hbyz__japel += '  if np.isnan(A).sum() != 0: return np.nan\n'
        hbyz__japel += '  return np.{}(A)\n'.format(vyzu__bylzh)
        blh__dfzto = {}
        exec(hbyz__japel, {'np': np}, blh__dfzto)
        kernel_func = register_jitable(blh__dfzto['kernel_func'])
        return (lambda arr, index_arr, win, minp, center, fname, raw=True,
            parallel=False: roll_fixed_apply(arr, index_arr, win, minp,
            center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        vyzu__bylzh]
    return (lambda arr, index_arr, win, minp, center, fname, raw=True,
        parallel=False: roll_fixed_linear_generic(arr, win, minp, center,
        parallel, init_kernel, add_kernel, remove_kernel, calc_kernel))


@overload(rolling_variable, no_unliteral=True)
def overload_rolling_variable(arr, on_arr, index_arr, win, minp, center,
    fname, raw=True, parallel=False):
    assert is_overload_constant_bool(raw)
    if is_const_func_type(fname):
        func = _get_apply_func(fname)
        return (lambda arr, on_arr, index_arr, win, minp, center, fname,
            raw=True, parallel=False: roll_variable_apply(arr, on_arr,
            index_arr, win, minp, center, parallel, func, raw))
    assert is_overload_constant_str(fname)
    vyzu__bylzh = get_overload_const_str(fname)
    if vyzu__bylzh not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (variable window) function {}'.
            format(vyzu__bylzh))
    if vyzu__bylzh in ('median', 'min', 'max'):
        hbyz__japel = 'def kernel_func(A):\n'
        hbyz__japel += '  arr  = dropna(A)\n'
        hbyz__japel += '  if len(arr) == 0: return np.nan\n'
        hbyz__japel += '  return np.{}(arr)\n'.format(vyzu__bylzh)
        blh__dfzto = {}
        exec(hbyz__japel, {'np': np, 'dropna': _dropna}, blh__dfzto)
        kernel_func = register_jitable(blh__dfzto['kernel_func'])
        return (lambda arr, on_arr, index_arr, win, minp, center, fname,
            raw=True, parallel=False: roll_variable_apply(arr, on_arr,
            index_arr, win, minp, center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        vyzu__bylzh]
    return (lambda arr, on_arr, index_arr, win, minp, center, fname, raw=
        True, parallel=False: roll_var_linear_generic(arr, on_arr, win,
        minp, center, parallel, init_kernel, add_kernel, remove_kernel,
        calc_kernel))


def _get_apply_func(f_type):
    func = get_overload_const_func(f_type, None)
    return bodo.compiler.udf_jit(func)


comm_border_tag = 22


@register_jitable
def roll_fixed_linear_generic(in_arr, win, minp, center, parallel,
    init_data, add_obs, remove_obs, calc_out):
    _validate_roll_fixed_args(win, minp)
    in_arr = prep_values(in_arr)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    if parallel:
        halo_size = np.int32(win // 2) if center else np.int32(win - 1)
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data(in_arr, win, minp, center, rank,
                n_pes, init_data, add_obs, remove_obs, calc_out)
        xckc__kzyjp = _border_icomm(in_arr, rank, n_pes, halo_size, True,
            center)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            bziue__obj) = xckc__kzyjp
    output, data = roll_fixed_linear_generic_seq(in_arr, win, minp, center,
        init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(bziue__obj, True)
            for jxz__jhp in range(0, halo_size):
                data = add_obs(r_recv_buff[jxz__jhp], *data)
                fdg__gbss = in_arr[N + jxz__jhp - win]
                data = remove_obs(fdg__gbss, *data)
                output[N + jxz__jhp - offset] = calc_out(minp, *data)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            data = init_data()
            for jxz__jhp in range(0, halo_size):
                data = add_obs(l_recv_buff[jxz__jhp], *data)
            for jxz__jhp in range(0, win - 1):
                data = add_obs(in_arr[jxz__jhp], *data)
                if jxz__jhp > offset:
                    fdg__gbss = l_recv_buff[jxz__jhp - offset - 1]
                    data = remove_obs(fdg__gbss, *data)
                if jxz__jhp >= offset:
                    output[jxz__jhp - offset] = calc_out(minp, *data)
    return output


@register_jitable
def roll_fixed_linear_generic_seq(in_arr, win, minp, center, init_data,
    add_obs, remove_obs, calc_out):
    data = init_data()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    output = np.empty(N, dtype=np.float64)
    tzee__sor = max(minp, 1) - 1
    tzee__sor = min(tzee__sor, N)
    for jxz__jhp in range(0, tzee__sor):
        data = add_obs(in_arr[jxz__jhp], *data)
        if jxz__jhp >= offset:
            output[jxz__jhp - offset] = calc_out(minp, *data)
    for jxz__jhp in range(tzee__sor, N):
        val = in_arr[jxz__jhp]
        data = add_obs(val, *data)
        if jxz__jhp > win - 1:
            fdg__gbss = in_arr[jxz__jhp - win]
            data = remove_obs(fdg__gbss, *data)
        output[jxz__jhp - offset] = calc_out(minp, *data)
    ilu__tgdno = data
    for jxz__jhp in range(N, N + offset):
        if jxz__jhp > win - 1:
            fdg__gbss = in_arr[jxz__jhp - win]
            data = remove_obs(fdg__gbss, *data)
        output[jxz__jhp - offset] = calc_out(minp, *data)
    return output, ilu__tgdno


def roll_fixed_apply(in_arr, index_arr, win, minp, center, parallel,
    kernel_func, raw=True):
    pass


@overload(roll_fixed_apply, no_unliteral=True)
def overload_roll_fixed_apply(in_arr, index_arr, win, minp, center,
    parallel, kernel_func, raw=True):
    assert is_overload_constant_bool(raw)
    return roll_fixed_apply_impl


def roll_fixed_apply_impl(in_arr, index_arr, win, minp, center, parallel,
    kernel_func, raw=True):
    _validate_roll_fixed_args(win, minp)
    in_arr = prep_values(in_arr)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    index_arr = fix_index_arr(index_arr)
    if parallel:
        halo_size = np.int32(win // 2) if center else np.int32(win - 1)
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_apply(in_arr, index_arr, win, minp,
                center, rank, n_pes, kernel_func, raw)
        xckc__kzyjp = _border_icomm(in_arr, rank, n_pes, halo_size, True,
            center)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            bziue__obj) = xckc__kzyjp
        if raw == False:
            srknb__ayq = _border_icomm(index_arr, rank, n_pes, halo_size, 
                True, center)
            (l_recv_buff_idx, r_recv_buff_idx, hzmt__lft, ypwwn__ysdpo,
                rucpf__jdv, syba__eeiu) = srknb__ayq
    output = roll_fixed_apply_seq(in_arr, index_arr, win, minp, center,
        kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if raw == False:
            _border_send_wait(ypwwn__ysdpo, hzmt__lft, rank, n_pes, True,
                center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(bziue__obj, True)
            if raw == False:
                bodo.libs.distributed_api.wait(syba__eeiu, True)
            recv_right_compute(output, in_arr, index_arr, N, win, minp,
                offset, r_recv_buff, r_recv_buff_idx, kernel_func, raw)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            if raw == False:
                bodo.libs.distributed_api.wait(rucpf__jdv, True)
            recv_left_compute(output, in_arr, index_arr, win, minp, offset,
                l_recv_buff, l_recv_buff_idx, kernel_func, raw)
    return output


def recv_right_compute(output, in_arr, index_arr, N, win, minp, offset,
    r_recv_buff, r_recv_buff_idx, kernel_func, raw):
    pass


@overload(recv_right_compute, no_unliteral=True)
def overload_recv_right_compute(output, in_arr, index_arr, N, win, minp,
    offset, r_recv_buff, r_recv_buff_idx, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, N, win, minp, offset,
            r_recv_buff, r_recv_buff_idx, kernel_func, raw):
            ilu__tgdno = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
            pns__zgbu = 0
            for jxz__jhp in range(max(N - offset, 0), N):
                data = ilu__tgdno[pns__zgbu:pns__zgbu + win]
                if win - np.isnan(data).sum() < minp:
                    output[jxz__jhp] = np.nan
                else:
                    output[jxz__jhp] = kernel_func(data)
                pns__zgbu += 1
        return impl

    def impl_series(output, in_arr, index_arr, N, win, minp, offset,
        r_recv_buff, r_recv_buff_idx, kernel_func, raw):
        ilu__tgdno = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
        qxrec__qmqw = np.concatenate((index_arr[N - win + 1:], r_recv_buff_idx)
            )
        pns__zgbu = 0
        for jxz__jhp in range(max(N - offset, 0), N):
            data = ilu__tgdno[pns__zgbu:pns__zgbu + win]
            if win - np.isnan(data).sum() < minp:
                output[jxz__jhp] = np.nan
            else:
                output[jxz__jhp] = kernel_func(pd.Series(data, qxrec__qmqw[
                    pns__zgbu:pns__zgbu + win]))
            pns__zgbu += 1
    return impl_series


def recv_left_compute(output, in_arr, index_arr, win, minp, offset,
    l_recv_buff, l_recv_buff_idx, kernel_func, raw):
    pass


@overload(recv_left_compute, no_unliteral=True)
def overload_recv_left_compute(output, in_arr, index_arr, win, minp, offset,
    l_recv_buff, l_recv_buff_idx, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, win, minp, offset, l_recv_buff,
            l_recv_buff_idx, kernel_func, raw):
            ilu__tgdno = np.concatenate((l_recv_buff, in_arr[:win - 1]))
            for jxz__jhp in range(0, win - offset - 1):
                data = ilu__tgdno[jxz__jhp:jxz__jhp + win]
                if win - np.isnan(data).sum() < minp:
                    output[jxz__jhp] = np.nan
                else:
                    output[jxz__jhp] = kernel_func(data)
        return impl

    def impl_series(output, in_arr, index_arr, win, minp, offset,
        l_recv_buff, l_recv_buff_idx, kernel_func, raw):
        ilu__tgdno = np.concatenate((l_recv_buff, in_arr[:win - 1]))
        qxrec__qmqw = np.concatenate((l_recv_buff_idx, index_arr[:win - 1]))
        for jxz__jhp in range(0, win - offset - 1):
            data = ilu__tgdno[jxz__jhp:jxz__jhp + win]
            if win - np.isnan(data).sum() < minp:
                output[jxz__jhp] = np.nan
            else:
                output[jxz__jhp] = kernel_func(pd.Series(data, qxrec__qmqw[
                    jxz__jhp:jxz__jhp + win]))
    return impl_series


def roll_fixed_apply_seq(in_arr, index_arr, win, minp, center, kernel_func,
    raw=True):
    pass


@overload(roll_fixed_apply_seq, no_unliteral=True)
def overload_roll_fixed_apply_seq(in_arr, index_arr, win, minp, center,
    kernel_func, raw=True):
    assert is_overload_constant_bool(raw), "'raw' should be constant bool"

    def roll_fixed_apply_seq_impl(in_arr, index_arr, win, minp, center,
        kernel_func, raw=True):
        N = len(in_arr)
        output = np.empty(N, dtype=np.float64)
        offset = (win - 1) // 2 if center else 0
        for jxz__jhp in range(0, N):
            start = max(jxz__jhp - win + 1 + offset, 0)
            end = min(jxz__jhp + 1 + offset, N)
            data = in_arr[start:end]
            if end - start - np.isnan(data).sum() < minp:
                output[jxz__jhp] = np.nan
            else:
                output[jxz__jhp] = apply_func(kernel_func, data, index_arr,
                    start, end, raw)
        return output
    return roll_fixed_apply_seq_impl


def apply_func(kernel_func, data, index_arr, start, end, raw):
    return kernel_func(data)


@overload(apply_func, no_unliteral=True)
def overload_apply_func(kernel_func, data, index_arr, start, end, raw):
    assert is_overload_constant_bool(raw), "'raw' should be constant bool"
    if is_overload_true(raw):
        return (lambda kernel_func, data, index_arr, start, end, raw:
            kernel_func(data))
    return lambda kernel_func, data, index_arr, start, end, raw: kernel_func(pd
        .Series(data, index_arr[start:end]))


def fix_index_arr(A):
    return A


@overload(fix_index_arr)
def overload_fix_index_arr(A):
    if is_overload_none(A):
        return lambda A: np.zeros(3)
    return lambda A: A


def get_offset_nanos(w):
    out = status = 0
    try:
        out = pd.tseries.frequencies.to_offset(w).nanos
    except:
        status = 1
    return out, status


def offset_to_nanos(w):
    return w


@overload(offset_to_nanos)
def overload_offset_to_nanos(w):
    if isinstance(w, types.Integer):
        return lambda w: w

    def impl(w):
        with numba.objmode(out='int64', status='int64'):
            out, status = get_offset_nanos(w)
        if status != 0:
            raise ValueError('Invalid offset value')
        return out
    return impl


@register_jitable
def roll_var_linear_generic(in_arr, on_arr_dt, win, minp, center, parallel,
    init_data, add_obs, remove_obs, calc_out):
    _validate_roll_var_args(minp, center)
    in_arr = prep_values(in_arr)
    win = offset_to_nanos(win)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    on_arr = cast_dt64_arr_to_int(on_arr_dt)
    N = len(in_arr)
    left_closed = False
    right_closed = True
    if parallel:
        if _is_small_for_parallel_variable(on_arr, win):
            return _handle_small_data_variable(in_arr, on_arr, win, minp,
                rank, n_pes, init_data, add_obs, remove_obs, calc_out)
        xckc__kzyjp = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, ovvbv__xii, l_recv_req,
            rmsl__urpt) = xckc__kzyjp
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start,
        end, init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(ovvbv__xii, ovvbv__xii, rank, n_pes, True, False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(rmsl__urpt, True)
            num_zero_starts = 0
            for jxz__jhp in range(0, N):
                if start[jxz__jhp] != 0:
                    break
                num_zero_starts += 1
            if num_zero_starts == 0:
                return output
            recv_starts = _get_var_recv_starts(on_arr, l_recv_t_buff,
                num_zero_starts, win)
            data = init_data()
            for yvqtt__iezrz in range(recv_starts[0], len(l_recv_t_buff)):
                data = add_obs(l_recv_buff[yvqtt__iezrz], *data)
            if right_closed:
                data = add_obs(in_arr[0], *data)
            output[0] = calc_out(minp, *data)
            for jxz__jhp in range(1, num_zero_starts):
                s = recv_starts[jxz__jhp]
                ygbdk__mfc = end[jxz__jhp]
                for yvqtt__iezrz in range(recv_starts[jxz__jhp - 1], s):
                    data = remove_obs(l_recv_buff[yvqtt__iezrz], *data)
                for yvqtt__iezrz in range(end[jxz__jhp - 1], ygbdk__mfc):
                    data = add_obs(in_arr[yvqtt__iezrz], *data)
                output[jxz__jhp] = calc_out(minp, *data)
    return output


@register_jitable(cache=True)
def _get_var_recv_starts(on_arr, l_recv_t_buff, num_zero_starts, win):
    recv_starts = np.zeros(num_zero_starts, np.int64)
    halo_size = len(l_recv_t_buff)
    fhw__uiuig = cast_dt64_arr_to_int(on_arr)
    left_closed = False
    rwo__rhm = fhw__uiuig[0] - win
    if left_closed:
        rwo__rhm -= 1
    recv_starts[0] = halo_size
    for yvqtt__iezrz in range(0, halo_size):
        if l_recv_t_buff[yvqtt__iezrz] > rwo__rhm:
            recv_starts[0] = yvqtt__iezrz
            break
    for jxz__jhp in range(1, num_zero_starts):
        rwo__rhm = fhw__uiuig[jxz__jhp] - win
        if left_closed:
            rwo__rhm -= 1
        recv_starts[jxz__jhp] = halo_size
        for yvqtt__iezrz in range(recv_starts[jxz__jhp - 1], halo_size):
            if l_recv_t_buff[yvqtt__iezrz] > rwo__rhm:
                recv_starts[jxz__jhp] = yvqtt__iezrz
                break
    return recv_starts


@register_jitable
def roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start, end,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    output = np.empty(N, np.float64)
    data = init_data()
    for yvqtt__iezrz in range(start[0], end[0]):
        data = add_obs(in_arr[yvqtt__iezrz], *data)
    output[0] = calc_out(minp, *data)
    for jxz__jhp in range(1, N):
        s = start[jxz__jhp]
        ygbdk__mfc = end[jxz__jhp]
        for yvqtt__iezrz in range(start[jxz__jhp - 1], s):
            data = remove_obs(in_arr[yvqtt__iezrz], *data)
        for yvqtt__iezrz in range(end[jxz__jhp - 1], ygbdk__mfc):
            data = add_obs(in_arr[yvqtt__iezrz], *data)
        output[jxz__jhp] = calc_out(minp, *data)
    return output


def roll_variable_apply(in_arr, on_arr_dt, index_arr, win, minp, center,
    parallel, kernel_func, raw=True):
    pass


@overload(roll_variable_apply, no_unliteral=True)
def overload_roll_variable_apply(in_arr, on_arr_dt, index_arr, win, minp,
    center, parallel, kernel_func, raw=True):
    assert is_overload_constant_bool(raw)
    return roll_variable_apply_impl


def roll_variable_apply_impl(in_arr, on_arr_dt, index_arr, win, minp,
    center, parallel, kernel_func, raw=True):
    _validate_roll_var_args(minp, center)
    in_arr = prep_values(in_arr)
    win = offset_to_nanos(win)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    on_arr = cast_dt64_arr_to_int(on_arr_dt)
    index_arr = fix_index_arr(index_arr)
    N = len(in_arr)
    left_closed = False
    right_closed = True
    if parallel:
        if _is_small_for_parallel_variable(on_arr, win):
            return _handle_small_data_variable_apply(in_arr, on_arr,
                index_arr, win, minp, rank, n_pes, kernel_func, raw)
        xckc__kzyjp = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, ovvbv__xii, l_recv_req,
            rmsl__urpt) = xckc__kzyjp
        if raw == False:
            srknb__ayq = _border_icomm_var(index_arr, on_arr, rank, n_pes, win)
            (l_recv_buff_idx, sxpk__mizri, ypwwn__ysdpo, uaism__vor,
                rucpf__jdv, qlk__lfc) = srknb__ayq
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp,
        start, end, kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(ovvbv__xii, ovvbv__xii, rank, n_pes, True, False)
        if raw == False:
            _border_send_wait(ypwwn__ysdpo, ypwwn__ysdpo, rank, n_pes, True,
                False)
            _border_send_wait(uaism__vor, uaism__vor, rank, n_pes, True, False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(rmsl__urpt, True)
            if raw == False:
                bodo.libs.distributed_api.wait(rucpf__jdv, True)
                bodo.libs.distributed_api.wait(qlk__lfc, True)
            num_zero_starts = 0
            for jxz__jhp in range(0, N):
                if start[jxz__jhp] != 0:
                    break
                num_zero_starts += 1
            if num_zero_starts == 0:
                return output
            recv_starts = _get_var_recv_starts(on_arr, l_recv_t_buff,
                num_zero_starts, win)
            recv_left_var_compute(output, in_arr, index_arr,
                num_zero_starts, recv_starts, l_recv_buff, l_recv_buff_idx,
                minp, kernel_func, raw)
    return output


def recv_left_var_compute(output, in_arr, index_arr, num_zero_starts,
    recv_starts, l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
    pass


@overload(recv_left_var_compute)
def overload_recv_left_var_compute(output, in_arr, index_arr,
    num_zero_starts, recv_starts, l_recv_buff, l_recv_buff_idx, minp,
    kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, num_zero_starts, recv_starts,
            l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
            for jxz__jhp in range(0, num_zero_starts):
                wnwc__pyvp = recv_starts[jxz__jhp]
                tam__rgd = np.concatenate((l_recv_buff[wnwc__pyvp:], in_arr
                    [:jxz__jhp + 1]))
                if len(tam__rgd) - np.isnan(tam__rgd).sum() >= minp:
                    output[jxz__jhp] = kernel_func(tam__rgd)
                else:
                    output[jxz__jhp] = np.nan
        return impl

    def impl_series(output, in_arr, index_arr, num_zero_starts, recv_starts,
        l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
        for jxz__jhp in range(0, num_zero_starts):
            wnwc__pyvp = recv_starts[jxz__jhp]
            tam__rgd = np.concatenate((l_recv_buff[wnwc__pyvp:], in_arr[:
                jxz__jhp + 1]))
            pfd__alyu = np.concatenate((l_recv_buff_idx[wnwc__pyvp:],
                index_arr[:jxz__jhp + 1]))
            if len(tam__rgd) - np.isnan(tam__rgd).sum() >= minp:
                output[jxz__jhp] = kernel_func(pd.Series(tam__rgd, pfd__alyu))
            else:
                output[jxz__jhp] = np.nan
    return impl_series


def roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp, start,
    end, kernel_func, raw):
    pass


@overload(roll_variable_apply_seq)
def overload_roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp,
    start, end, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):
        return roll_variable_apply_seq_impl
    return roll_variable_apply_seq_impl_series


def roll_variable_apply_seq_impl(in_arr, on_arr, index_arr, win, minp,
    start, end, kernel_func, raw):
    N = len(in_arr)
    output = np.empty(N, dtype=np.float64)
    for jxz__jhp in range(0, N):
        s = start[jxz__jhp]
        ygbdk__mfc = end[jxz__jhp]
        data = in_arr[s:ygbdk__mfc]
        if ygbdk__mfc - s - np.isnan(data).sum() >= minp:
            output[jxz__jhp] = kernel_func(data)
        else:
            output[jxz__jhp] = np.nan
    return output


def roll_variable_apply_seq_impl_series(in_arr, on_arr, index_arr, win,
    minp, start, end, kernel_func, raw):
    N = len(in_arr)
    output = np.empty(N, dtype=np.float64)
    for jxz__jhp in range(0, N):
        s = start[jxz__jhp]
        ygbdk__mfc = end[jxz__jhp]
        data = in_arr[s:ygbdk__mfc]
        if ygbdk__mfc - s - np.isnan(data).sum() >= minp:
            output[jxz__jhp] = kernel_func(pd.Series(data, index_arr[s:
                ygbdk__mfc]))
        else:
            output[jxz__jhp] = np.nan
    return output


@register_jitable(cache=True)
def _build_indexer(on_arr, N, win, left_closed, right_closed):
    fhw__uiuig = cast_dt64_arr_to_int(on_arr)
    start = np.empty(N, np.int64)
    end = np.empty(N, np.int64)
    start[0] = 0
    if right_closed:
        end[0] = 1
    else:
        end[0] = 0
    for jxz__jhp in range(1, N):
        mitur__gnr = fhw__uiuig[jxz__jhp]
        rwo__rhm = fhw__uiuig[jxz__jhp] - win
        if left_closed:
            rwo__rhm -= 1
        start[jxz__jhp] = jxz__jhp
        for yvqtt__iezrz in range(start[jxz__jhp - 1], jxz__jhp):
            if fhw__uiuig[yvqtt__iezrz] > rwo__rhm:
                start[jxz__jhp] = yvqtt__iezrz
                break
        if fhw__uiuig[end[jxz__jhp - 1]] <= mitur__gnr:
            end[jxz__jhp] = jxz__jhp + 1
        else:
            end[jxz__jhp] = end[jxz__jhp - 1]
        if not right_closed:
            end[jxz__jhp] -= 1
    return start, end


@register_jitable
def init_data_sum():
    return 0, 0.0


@register_jitable
def add_sum(val, nobs, sum_x):
    if not np.isnan(val):
        nobs += 1
        sum_x += val
    return nobs, sum_x


@register_jitable
def remove_sum(val, nobs, sum_x):
    if not np.isnan(val):
        nobs -= 1
        sum_x -= val
    return nobs, sum_x


@register_jitable
def calc_sum(minp, nobs, sum_x):
    return sum_x if nobs >= minp else np.nan


@register_jitable
def init_data_mean():
    return 0, 0.0, 0


@register_jitable
def add_mean(val, nobs, sum_x, neg_ct):
    if not np.isnan(val):
        nobs += 1
        sum_x += val
        if val < 0:
            neg_ct += 1
    return nobs, sum_x, neg_ct


@register_jitable
def remove_mean(val, nobs, sum_x, neg_ct):
    if not np.isnan(val):
        nobs -= 1
        sum_x -= val
        if val < 0:
            neg_ct -= 1
    return nobs, sum_x, neg_ct


@register_jitable
def calc_mean(minp, nobs, sum_x, neg_ct):
    if nobs >= minp:
        jeoc__zycb = sum_x / nobs
        if neg_ct == 0 and jeoc__zycb < 0.0:
            jeoc__zycb = 0
        elif neg_ct == nobs and jeoc__zycb > 0.0:
            jeoc__zycb = 0
    else:
        jeoc__zycb = np.nan
    return jeoc__zycb


@register_jitable
def init_data_var():
    return 0, 0.0, 0.0


@register_jitable
def add_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs += 1
        rie__xmtg = val - mean_x
        mean_x += rie__xmtg / nobs
        ssqdm_x += (nobs - 1) * rie__xmtg ** 2 / nobs
    return nobs, mean_x, ssqdm_x


@register_jitable
def remove_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs -= 1
        if nobs != 0:
            rie__xmtg = val - mean_x
            mean_x -= rie__xmtg / nobs
            ssqdm_x -= (nobs + 1) * rie__xmtg ** 2 / nobs
        else:
            mean_x = 0.0
            ssqdm_x = 0.0
    return nobs, mean_x, ssqdm_x


@register_jitable
def calc_var(minp, nobs, mean_x, ssqdm_x):
    pzy__pjmv = 1.0
    jeoc__zycb = np.nan
    if nobs >= minp and nobs > pzy__pjmv:
        if nobs == 1:
            jeoc__zycb = 0.0
        else:
            jeoc__zycb = ssqdm_x / (nobs - pzy__pjmv)
            if jeoc__zycb < 0.0:
                jeoc__zycb = 0.0
    return jeoc__zycb


@register_jitable
def calc_std(minp, nobs, mean_x, ssqdm_x):
    ozhts__fixn = calc_var(minp, nobs, mean_x, ssqdm_x)
    return np.sqrt(ozhts__fixn)


@register_jitable
def init_data_count():
    return 0.0,


@register_jitable
def add_count(val, count_x):
    if not np.isnan(val):
        count_x += 1.0
    return count_x,


@register_jitable
def remove_count(val, count_x):
    if not np.isnan(val):
        count_x -= 1.0
    return count_x,


@register_jitable
def calc_count(minp, count_x):
    return count_x


@register_jitable
def calc_count_var(minp, count_x):
    return count_x if count_x >= minp else np.nan


linear_kernels = {'sum': (init_data_sum, add_sum, remove_sum, calc_sum),
    'mean': (init_data_mean, add_mean, remove_mean, calc_mean), 'var': (
    init_data_var, add_var, remove_var, calc_var), 'std': (init_data_var,
    add_var, remove_var, calc_std), 'count': (init_data_count, add_count,
    remove_count, calc_count)}


def shift():
    return


@overload(shift, jit_options={'cache': True})
def shift_overload(in_arr, shift, parallel):
    if not isinstance(parallel, types.Literal):
        return shift_impl


def shift_impl(in_arr, shift, parallel):
    N = len(in_arr)
    in_arr = decode_if_dict_array(in_arr)
    output = alloc_shift(N, in_arr, (-1,))
    send_right = shift > 0
    send_left = shift <= 0
    is_parallel_str = False
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        halo_size = np.int32(abs(shift))
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_shift(in_arr, shift, rank, n_pes)
        xckc__kzyjp = _border_icomm(in_arr, rank, n_pes, halo_size,
            send_right, send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            bziue__obj) = xckc__kzyjp
        if send_right and is_str_binary_array(in_arr):
            is_parallel_str = True
            shift_left_recv(r_send_req, l_send_req, rank, n_pes, halo_size,
                l_recv_req, l_recv_buff, output)
    shift_seq(in_arr, shift, output, is_parallel_str)
    if parallel:
        if send_right:
            if not is_str_binary_array(in_arr):
                shift_left_recv(r_send_req, l_send_req, rank, n_pes,
                    halo_size, l_recv_req, l_recv_buff, output)
        else:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, False, True)
            if rank != n_pes - 1:
                bodo.libs.distributed_api.wait(bziue__obj, True)
                for jxz__jhp in range(0, halo_size):
                    if bodo.libs.array_kernels.isna(r_recv_buff, jxz__jhp):
                        bodo.libs.array_kernels.setna(output, N - halo_size +
                            jxz__jhp)
                        continue
                    output[N - halo_size + jxz__jhp] = r_recv_buff[jxz__jhp]
    return output


@register_jitable(cache=True)
def shift_seq(in_arr, shift, output, is_parallel_str=False):
    N = len(in_arr)
    zen__qcr = 1 if shift > 0 else -1
    shift = zen__qcr * min(abs(shift), N)
    if shift > 0 and (not is_parallel_str or bodo.get_rank() == 0):
        bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
    start = max(shift, 0)
    end = min(N, N + shift)
    for jxz__jhp in range(start, end):
        if bodo.libs.array_kernels.isna(in_arr, jxz__jhp - shift):
            bodo.libs.array_kernels.setna(output, jxz__jhp)
            continue
        output[jxz__jhp] = in_arr[jxz__jhp - shift]
    if shift < 0:
        bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
    return output


@register_jitable
def shift_left_recv(r_send_req, l_send_req, rank, n_pes, halo_size,
    l_recv_req, l_recv_buff, output):
    _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
    if rank != 0:
        bodo.libs.distributed_api.wait(l_recv_req, True)
        for jxz__jhp in range(0, halo_size):
            if bodo.libs.array_kernels.isna(l_recv_buff, jxz__jhp):
                bodo.libs.array_kernels.setna(output, jxz__jhp)
                continue
            output[jxz__jhp] = l_recv_buff[jxz__jhp]


def is_str_binary_array(arr):
    return False


@overload(is_str_binary_array)
def overload_is_str_binary_array(arr):
    if arr in [bodo.string_array_type, bodo.binary_array_type]:
        return lambda arr: True
    return lambda arr: False


def is_supported_shift_array_type(arr_type):
    return isinstance(arr_type, types.Array) and (isinstance(arr_type.dtype,
        types.Number) or arr_type.dtype in [bodo.datetime64ns, bodo.
        timedelta64ns]) or isinstance(arr_type, (bodo.IntegerArrayType,
        bodo.DecimalArrayType)) or arr_type in (bodo.boolean_array, bodo.
        datetime_date_array_type, bodo.string_array_type, bodo.
        binary_array_type, bodo.dict_str_arr_type)


def pct_change():
    return


@overload(pct_change, jit_options={'cache': True})
def pct_change_overload(in_arr, shift, parallel):
    if not isinstance(parallel, types.Literal):
        return pct_change_impl


def pct_change_impl(in_arr, shift, parallel):
    N = len(in_arr)
    send_right = shift > 0
    send_left = shift <= 0
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        halo_size = np.int32(abs(shift))
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_pct_change(in_arr, shift, rank, n_pes)
        xckc__kzyjp = _border_icomm(in_arr, rank, n_pes, halo_size,
            send_right, send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            bziue__obj) = xckc__kzyjp
    output = pct_change_seq(in_arr, shift)
    if parallel:
        if send_right:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
            if rank != 0:
                bodo.libs.distributed_api.wait(l_recv_req, True)
                for jxz__jhp in range(0, halo_size):
                    vyi__vcop = l_recv_buff[jxz__jhp]
                    output[jxz__jhp] = (in_arr[jxz__jhp] - vyi__vcop
                        ) / vyi__vcop
        else:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, False, True)
            if rank != n_pes - 1:
                bodo.libs.distributed_api.wait(bziue__obj, True)
                for jxz__jhp in range(0, halo_size):
                    vyi__vcop = r_recv_buff[jxz__jhp]
                    output[N - halo_size + jxz__jhp] = (in_arr[N -
                        halo_size + jxz__jhp] - vyi__vcop) / vyi__vcop
    return output


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_first_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[0]
    assert isinstance(arr.dtype, types.Float)
    rgsyq__jbohi = np.nan
    if arr.dtype == types.float32:
        rgsyq__jbohi = np.float32('nan')

    def impl(arr):
        for jxz__jhp in range(len(arr)):
            if not bodo.libs.array_kernels.isna(arr, jxz__jhp):
                return arr[jxz__jhp]
        return rgsyq__jbohi
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_last_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[-1]
    assert isinstance(arr.dtype, types.Float)
    rgsyq__jbohi = np.nan
    if arr.dtype == types.float32:
        rgsyq__jbohi = np.float32('nan')

    def impl(arr):
        znxbe__pexco = len(arr)
        for jxz__jhp in range(len(arr)):
            pns__zgbu = znxbe__pexco - jxz__jhp - 1
            if not bodo.libs.array_kernels.isna(arr, pns__zgbu):
                return arr[pns__zgbu]
        return rgsyq__jbohi
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_one_from_arr_dtype(arr):
    one = arr.dtype(1)
    return lambda arr: one


@register_jitable(cache=True)
def pct_change_seq(in_arr, shift):
    N = len(in_arr)
    output = alloc_pct_change(N, in_arr)
    zen__qcr = 1 if shift > 0 else -1
    shift = zen__qcr * min(abs(shift), N)
    if shift > 0:
        bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
    else:
        bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
    if shift > 0:
        ckpn__siw = get_first_non_na(in_arr[:shift])
        xxp__ppr = get_last_non_na(in_arr[:shift])
    else:
        ckpn__siw = get_last_non_na(in_arr[:-shift])
        xxp__ppr = get_first_non_na(in_arr[:-shift])
    one = get_one_from_arr_dtype(output)
    start = max(shift, 0)
    end = min(N, N + shift)
    for jxz__jhp in range(start, end):
        vyi__vcop = in_arr[jxz__jhp - shift]
        if np.isnan(vyi__vcop):
            vyi__vcop = ckpn__siw
        else:
            ckpn__siw = vyi__vcop
        val = in_arr[jxz__jhp]
        if np.isnan(val):
            val = xxp__ppr
        else:
            xxp__ppr = val
        output[jxz__jhp] = val / vyi__vcop - one
    return output


@register_jitable(cache=True)
def _border_icomm(in_arr, rank, n_pes, halo_size, send_right=True,
    send_left=False):
    ovvpm__aed = np.int32(comm_border_tag)
    l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    r_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    if send_right and rank != n_pes - 1:
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            halo_size, np.int32(rank + 1), ovvpm__aed, True)
    if send_right and rank != 0:
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, halo_size,
            np.int32(rank - 1), ovvpm__aed, True)
    if send_left and rank != 0:
        l_send_req = bodo.libs.distributed_api.isend(in_arr[:halo_size],
            halo_size, np.int32(rank - 1), ovvpm__aed, True)
    if send_left and rank != n_pes - 1:
        bziue__obj = bodo.libs.distributed_api.irecv(r_recv_buff, halo_size,
            np.int32(rank + 1), ovvpm__aed, True)
    return (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
        bziue__obj)


@register_jitable(cache=True)
def _border_icomm_var(in_arr, on_arr, rank, n_pes, win_size):
    ovvpm__aed = np.int32(comm_border_tag)
    N = len(on_arr)
    halo_size = N
    end = on_arr[-1]
    for yvqtt__iezrz in range(-2, -N, -1):
        qhpe__sxuf = on_arr[yvqtt__iezrz]
        if end - qhpe__sxuf >= win_size:
            halo_size = -yvqtt__iezrz
            break
    if rank != n_pes - 1:
        bodo.libs.distributed_api.send(halo_size, np.int32(rank + 1),
            ovvpm__aed)
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            np.int32(halo_size), np.int32(rank + 1), ovvpm__aed, True)
        ovvbv__xii = bodo.libs.distributed_api.isend(on_arr[-halo_size:],
            np.int32(halo_size), np.int32(rank + 1), ovvpm__aed, True)
    if rank != 0:
        halo_size = bodo.libs.distributed_api.recv(np.int64, np.int32(rank -
            1), ovvpm__aed)
        l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr)
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, np.int32(
            halo_size), np.int32(rank - 1), ovvpm__aed, True)
        l_recv_t_buff = np.empty(halo_size, np.int64)
        rmsl__urpt = bodo.libs.distributed_api.irecv(l_recv_t_buff, np.
            int32(halo_size), np.int32(rank - 1), ovvpm__aed, True)
    return (l_recv_buff, l_recv_t_buff, r_send_req, ovvbv__xii, l_recv_req,
        rmsl__urpt)


@register_jitable
def _border_send_wait(r_send_req, l_send_req, rank, n_pes, right, left):
    if right and rank != n_pes - 1:
        bodo.libs.distributed_api.wait(r_send_req, True)
    if left and rank != 0:
        bodo.libs.distributed_api.wait(l_send_req, True)


@register_jitable
def _is_small_for_parallel(N, halo_size):
    vnyab__tnnp = bodo.libs.distributed_api.dist_reduce(int(N <= 2 *
        halo_size + 1), np.int32(Reduce_Type.Sum.value))
    return vnyab__tnnp != 0


@register_jitable
def _handle_small_data(in_arr, win, minp, center, rank, n_pes, init_data,
    add_obs, remove_obs, calc_out):
    N = len(in_arr)
    jcbvz__uij = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    ksqt__yuvrr = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        xwdu__gikv, xowb__syu = roll_fixed_linear_generic_seq(ksqt__yuvrr,
            win, minp, center, init_data, add_obs, remove_obs, calc_out)
    else:
        xwdu__gikv = np.empty(jcbvz__uij, np.float64)
    bodo.libs.distributed_api.bcast(xwdu__gikv)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return xwdu__gikv[start:end]


@register_jitable
def _handle_small_data_apply(in_arr, index_arr, win, minp, center, rank,
    n_pes, kernel_func, raw=True):
    N = len(in_arr)
    jcbvz__uij = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    ksqt__yuvrr = bodo.libs.distributed_api.gatherv(in_arr)
    qsyrl__gnou = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        xwdu__gikv = roll_fixed_apply_seq(ksqt__yuvrr, qsyrl__gnou, win,
            minp, center, kernel_func, raw)
    else:
        xwdu__gikv = np.empty(jcbvz__uij, np.float64)
    bodo.libs.distributed_api.bcast(xwdu__gikv)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return xwdu__gikv[start:end]


def bcast_n_chars_if_str_binary_arr(arr):
    pass


@overload(bcast_n_chars_if_str_binary_arr)
def overload_bcast_n_chars_if_str_binary_arr(arr):
    if arr in [bodo.binary_array_type, bodo.string_array_type]:

        def impl(arr):
            return bodo.libs.distributed_api.bcast_scalar(np.int64(bodo.
                libs.str_arr_ext.num_total_chars(arr)))
        return impl
    return lambda arr: -1


@register_jitable
def _handle_small_data_shift(in_arr, shift, rank, n_pes):
    N = len(in_arr)
    jcbvz__uij = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.
        int32(Reduce_Type.Sum.value))
    ksqt__yuvrr = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        xwdu__gikv = alloc_shift(len(ksqt__yuvrr), ksqt__yuvrr, (-1,))
        shift_seq(ksqt__yuvrr, shift, xwdu__gikv)
        gqh__qxy = bcast_n_chars_if_str_binary_arr(xwdu__gikv)
    else:
        gqh__qxy = bcast_n_chars_if_str_binary_arr(in_arr)
        xwdu__gikv = alloc_shift(jcbvz__uij, in_arr, (gqh__qxy,))
    bodo.libs.distributed_api.bcast(xwdu__gikv)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return xwdu__gikv[start:end]


@register_jitable
def _handle_small_data_pct_change(in_arr, shift, rank, n_pes):
    N = len(in_arr)
    jcbvz__uij = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    ksqt__yuvrr = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        xwdu__gikv = pct_change_seq(ksqt__yuvrr, shift)
    else:
        xwdu__gikv = alloc_pct_change(jcbvz__uij, in_arr)
    bodo.libs.distributed_api.bcast(xwdu__gikv)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return xwdu__gikv[start:end]


def cast_dt64_arr_to_int(arr):
    return arr


@infer_global(cast_dt64_arr_to_int)
class DtArrToIntType(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        assert args[0] == types.Array(types.NPDatetime('ns'), 1, 'C') or args[0
            ] == types.Array(types.int64, 1, 'C')
        return signature(types.Array(types.int64, 1, 'C'), *args)


@lower_builtin(cast_dt64_arr_to_int, types.Array(types.NPDatetime('ns'), 1,
    'C'))
@lower_builtin(cast_dt64_arr_to_int, types.Array(types.int64, 1, 'C'))
def lower_cast_dt64_arr_to_int(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@register_jitable
def _is_small_for_parallel_variable(on_arr, win_size):
    if len(on_arr) < 2:
        zpdzw__wfs = 1
    else:
        start = on_arr[0]
        end = on_arr[-1]
        hkrp__ece = end - start
        zpdzw__wfs = int(hkrp__ece <= win_size)
    vnyab__tnnp = bodo.libs.distributed_api.dist_reduce(zpdzw__wfs, np.
        int32(Reduce_Type.Sum.value))
    return vnyab__tnnp != 0


@register_jitable
def _handle_small_data_variable(in_arr, on_arr, win, minp, rank, n_pes,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    jcbvz__uij = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    ksqt__yuvrr = bodo.libs.distributed_api.gatherv(in_arr)
    axnbz__cad = bodo.libs.distributed_api.gatherv(on_arr)
    if rank == 0:
        start, end = _build_indexer(axnbz__cad, jcbvz__uij, win, False, True)
        xwdu__gikv = roll_var_linear_generic_seq(ksqt__yuvrr, axnbz__cad,
            win, minp, start, end, init_data, add_obs, remove_obs, calc_out)
    else:
        xwdu__gikv = np.empty(jcbvz__uij, np.float64)
    bodo.libs.distributed_api.bcast(xwdu__gikv)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return xwdu__gikv[start:end]


@register_jitable
def _handle_small_data_variable_apply(in_arr, on_arr, index_arr, win, minp,
    rank, n_pes, kernel_func, raw):
    N = len(in_arr)
    jcbvz__uij = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    ksqt__yuvrr = bodo.libs.distributed_api.gatherv(in_arr)
    axnbz__cad = bodo.libs.distributed_api.gatherv(on_arr)
    qsyrl__gnou = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        start, end = _build_indexer(axnbz__cad, jcbvz__uij, win, False, True)
        xwdu__gikv = roll_variable_apply_seq(ksqt__yuvrr, axnbz__cad,
            qsyrl__gnou, win, minp, start, end, kernel_func, raw)
    else:
        xwdu__gikv = np.empty(jcbvz__uij, np.float64)
    bodo.libs.distributed_api.bcast(xwdu__gikv)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return xwdu__gikv[start:end]


@register_jitable(cache=True)
def _dropna(arr):
    oif__zpesz = len(arr)
    awrb__udmm = oif__zpesz - np.isnan(arr).sum()
    A = np.empty(awrb__udmm, arr.dtype)
    owjqa__ypy = 0
    for jxz__jhp in range(oif__zpesz):
        val = arr[jxz__jhp]
        if not np.isnan(val):
            A[owjqa__ypy] = val
            owjqa__ypy += 1
    return A


def alloc_shift(n, A, s=None):
    return np.empty(n, A.dtype)


@overload(alloc_shift, no_unliteral=True)
def alloc_shift_overload(n, A, s=None):
    if not isinstance(A, types.Array):
        return lambda n, A, s=None: bodo.utils.utils.alloc_type(n, A, s)
    if isinstance(A.dtype, types.Integer):
        return lambda n, A, s=None: np.empty(n, np.float64)
    return lambda n, A, s=None: np.empty(n, A.dtype)


def alloc_pct_change(n, A):
    return np.empty(n, A.dtype)


@overload(alloc_pct_change, no_unliteral=True)
def alloc_pct_change_overload(n, A):
    if isinstance(A.dtype, types.Integer):
        return lambda n, A: np.empty(n, np.float64)
    return lambda n, A: np.empty(n, A.dtype)


def prep_values(A):
    return A.astype('float64')


@overload(prep_values, no_unliteral=True)
def prep_values_overload(A):
    if A == types.Array(types.float64, 1, 'C'):
        return lambda A: A
    return lambda A: A.astype(np.float64)


@register_jitable
def _validate_roll_fixed_args(win, minp):
    if win < 0:
        raise ValueError('window must be non-negative')
    if minp < 0:
        raise ValueError('min_periods must be >= 0')
    if minp > win:
        raise ValueError('min_periods must be <= window')


@register_jitable
def _validate_roll_var_args(minp, center):
    if minp < 0:
        raise ValueError('min_periods must be >= 0')
    if center:
        raise NotImplementedError(
            'rolling: center is not implemented for datetimelike and offset based windows'
            )
