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
        czist__qwovf = arr.copy(dtype=types.float64)
        return signature(czist__qwovf, *unliteral_all(args))


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
    cmeld__whh = get_overload_const_str(fname)
    if cmeld__whh not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (fixed window) function {}'.format
            (cmeld__whh))
    if cmeld__whh in ('median', 'min', 'max'):
        maxoa__gjzua = 'def kernel_func(A):\n'
        maxoa__gjzua += '  if np.isnan(A).sum() != 0: return np.nan\n'
        maxoa__gjzua += '  return np.{}(A)\n'.format(cmeld__whh)
        lxvmy__tcrb = {}
        exec(maxoa__gjzua, {'np': np}, lxvmy__tcrb)
        kernel_func = register_jitable(lxvmy__tcrb['kernel_func'])
        return (lambda arr, index_arr, win, minp, center, fname, raw=True,
            parallel=False: roll_fixed_apply(arr, index_arr, win, minp,
            center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        cmeld__whh]
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
    cmeld__whh = get_overload_const_str(fname)
    if cmeld__whh not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (variable window) function {}'.
            format(cmeld__whh))
    if cmeld__whh in ('median', 'min', 'max'):
        maxoa__gjzua = 'def kernel_func(A):\n'
        maxoa__gjzua += '  arr  = dropna(A)\n'
        maxoa__gjzua += '  if len(arr) == 0: return np.nan\n'
        maxoa__gjzua += '  return np.{}(arr)\n'.format(cmeld__whh)
        lxvmy__tcrb = {}
        exec(maxoa__gjzua, {'np': np, 'dropna': _dropna}, lxvmy__tcrb)
        kernel_func = register_jitable(lxvmy__tcrb['kernel_func'])
        return (lambda arr, on_arr, index_arr, win, minp, center, fname,
            raw=True, parallel=False: roll_variable_apply(arr, on_arr,
            index_arr, win, minp, center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        cmeld__whh]
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
        xhia__wbc = _border_icomm(in_arr, rank, n_pes, halo_size, True, center)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            mtjcx__jof) = xhia__wbc
    output, data = roll_fixed_linear_generic_seq(in_arr, win, minp, center,
        init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(mtjcx__jof, True)
            for vhq__fnyq in range(0, halo_size):
                data = add_obs(r_recv_buff[vhq__fnyq], *data)
                huiq__mygxr = in_arr[N + vhq__fnyq - win]
                data = remove_obs(huiq__mygxr, *data)
                output[N + vhq__fnyq - offset] = calc_out(minp, *data)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            data = init_data()
            for vhq__fnyq in range(0, halo_size):
                data = add_obs(l_recv_buff[vhq__fnyq], *data)
            for vhq__fnyq in range(0, win - 1):
                data = add_obs(in_arr[vhq__fnyq], *data)
                if vhq__fnyq > offset:
                    huiq__mygxr = l_recv_buff[vhq__fnyq - offset - 1]
                    data = remove_obs(huiq__mygxr, *data)
                if vhq__fnyq >= offset:
                    output[vhq__fnyq - offset] = calc_out(minp, *data)
    return output


@register_jitable
def roll_fixed_linear_generic_seq(in_arr, win, minp, center, init_data,
    add_obs, remove_obs, calc_out):
    data = init_data()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    output = np.empty(N, dtype=np.float64)
    wgoo__moy = max(minp, 1) - 1
    wgoo__moy = min(wgoo__moy, N)
    for vhq__fnyq in range(0, wgoo__moy):
        data = add_obs(in_arr[vhq__fnyq], *data)
        if vhq__fnyq >= offset:
            output[vhq__fnyq - offset] = calc_out(minp, *data)
    for vhq__fnyq in range(wgoo__moy, N):
        val = in_arr[vhq__fnyq]
        data = add_obs(val, *data)
        if vhq__fnyq > win - 1:
            huiq__mygxr = in_arr[vhq__fnyq - win]
            data = remove_obs(huiq__mygxr, *data)
        output[vhq__fnyq - offset] = calc_out(minp, *data)
    grnr__ojf = data
    for vhq__fnyq in range(N, N + offset):
        if vhq__fnyq > win - 1:
            huiq__mygxr = in_arr[vhq__fnyq - win]
            data = remove_obs(huiq__mygxr, *data)
        output[vhq__fnyq - offset] = calc_out(minp, *data)
    return output, grnr__ojf


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
        xhia__wbc = _border_icomm(in_arr, rank, n_pes, halo_size, True, center)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            mtjcx__jof) = xhia__wbc
        if raw == False:
            wuv__fwoz = _border_icomm(index_arr, rank, n_pes, halo_size, 
                True, center)
            (l_recv_buff_idx, r_recv_buff_idx, joju__wwj, pejb__kjml,
                wquw__eqxbo, oics__urb) = wuv__fwoz
    output = roll_fixed_apply_seq(in_arr, index_arr, win, minp, center,
        kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if raw == False:
            _border_send_wait(pejb__kjml, joju__wwj, rank, n_pes, True, center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(mtjcx__jof, True)
            if raw == False:
                bodo.libs.distributed_api.wait(oics__urb, True)
            recv_right_compute(output, in_arr, index_arr, N, win, minp,
                offset, r_recv_buff, r_recv_buff_idx, kernel_func, raw)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            if raw == False:
                bodo.libs.distributed_api.wait(wquw__eqxbo, True)
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
            grnr__ojf = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
            hpkur__ywwy = 0
            for vhq__fnyq in range(max(N - offset, 0), N):
                data = grnr__ojf[hpkur__ywwy:hpkur__ywwy + win]
                if win - np.isnan(data).sum() < minp:
                    output[vhq__fnyq] = np.nan
                else:
                    output[vhq__fnyq] = kernel_func(data)
                hpkur__ywwy += 1
        return impl

    def impl_series(output, in_arr, index_arr, N, win, minp, offset,
        r_recv_buff, r_recv_buff_idx, kernel_func, raw):
        grnr__ojf = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
        ivv__idln = np.concatenate((index_arr[N - win + 1:], r_recv_buff_idx))
        hpkur__ywwy = 0
        for vhq__fnyq in range(max(N - offset, 0), N):
            data = grnr__ojf[hpkur__ywwy:hpkur__ywwy + win]
            if win - np.isnan(data).sum() < minp:
                output[vhq__fnyq] = np.nan
            else:
                output[vhq__fnyq] = kernel_func(pd.Series(data, ivv__idln[
                    hpkur__ywwy:hpkur__ywwy + win]))
            hpkur__ywwy += 1
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
            grnr__ojf = np.concatenate((l_recv_buff, in_arr[:win - 1]))
            for vhq__fnyq in range(0, win - offset - 1):
                data = grnr__ojf[vhq__fnyq:vhq__fnyq + win]
                if win - np.isnan(data).sum() < minp:
                    output[vhq__fnyq] = np.nan
                else:
                    output[vhq__fnyq] = kernel_func(data)
        return impl

    def impl_series(output, in_arr, index_arr, win, minp, offset,
        l_recv_buff, l_recv_buff_idx, kernel_func, raw):
        grnr__ojf = np.concatenate((l_recv_buff, in_arr[:win - 1]))
        ivv__idln = np.concatenate((l_recv_buff_idx, index_arr[:win - 1]))
        for vhq__fnyq in range(0, win - offset - 1):
            data = grnr__ojf[vhq__fnyq:vhq__fnyq + win]
            if win - np.isnan(data).sum() < minp:
                output[vhq__fnyq] = np.nan
            else:
                output[vhq__fnyq] = kernel_func(pd.Series(data, ivv__idln[
                    vhq__fnyq:vhq__fnyq + win]))
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
        for vhq__fnyq in range(0, N):
            start = max(vhq__fnyq - win + 1 + offset, 0)
            end = min(vhq__fnyq + 1 + offset, N)
            data = in_arr[start:end]
            if end - start - np.isnan(data).sum() < minp:
                output[vhq__fnyq] = np.nan
            else:
                output[vhq__fnyq] = apply_func(kernel_func, data, index_arr,
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
        xhia__wbc = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, watn__acwp, l_recv_req,
            ptji__jgsvx) = xhia__wbc
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start,
        end, init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(watn__acwp, watn__acwp, rank, n_pes, True, False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(ptji__jgsvx, True)
            num_zero_starts = 0
            for vhq__fnyq in range(0, N):
                if start[vhq__fnyq] != 0:
                    break
                num_zero_starts += 1
            if num_zero_starts == 0:
                return output
            recv_starts = _get_var_recv_starts(on_arr, l_recv_t_buff,
                num_zero_starts, win)
            data = init_data()
            for onyn__qwzgg in range(recv_starts[0], len(l_recv_t_buff)):
                data = add_obs(l_recv_buff[onyn__qwzgg], *data)
            if right_closed:
                data = add_obs(in_arr[0], *data)
            output[0] = calc_out(minp, *data)
            for vhq__fnyq in range(1, num_zero_starts):
                s = recv_starts[vhq__fnyq]
                kfo__xdruv = end[vhq__fnyq]
                for onyn__qwzgg in range(recv_starts[vhq__fnyq - 1], s):
                    data = remove_obs(l_recv_buff[onyn__qwzgg], *data)
                for onyn__qwzgg in range(end[vhq__fnyq - 1], kfo__xdruv):
                    data = add_obs(in_arr[onyn__qwzgg], *data)
                output[vhq__fnyq] = calc_out(minp, *data)
    return output


@register_jitable(cache=True)
def _get_var_recv_starts(on_arr, l_recv_t_buff, num_zero_starts, win):
    recv_starts = np.zeros(num_zero_starts, np.int64)
    halo_size = len(l_recv_t_buff)
    donlw__yrsnd = cast_dt64_arr_to_int(on_arr)
    left_closed = False
    tgszq__gvrqu = donlw__yrsnd[0] - win
    if left_closed:
        tgszq__gvrqu -= 1
    recv_starts[0] = halo_size
    for onyn__qwzgg in range(0, halo_size):
        if l_recv_t_buff[onyn__qwzgg] > tgszq__gvrqu:
            recv_starts[0] = onyn__qwzgg
            break
    for vhq__fnyq in range(1, num_zero_starts):
        tgszq__gvrqu = donlw__yrsnd[vhq__fnyq] - win
        if left_closed:
            tgszq__gvrqu -= 1
        recv_starts[vhq__fnyq] = halo_size
        for onyn__qwzgg in range(recv_starts[vhq__fnyq - 1], halo_size):
            if l_recv_t_buff[onyn__qwzgg] > tgszq__gvrqu:
                recv_starts[vhq__fnyq] = onyn__qwzgg
                break
    return recv_starts


@register_jitable
def roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start, end,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    output = np.empty(N, np.float64)
    data = init_data()
    for onyn__qwzgg in range(start[0], end[0]):
        data = add_obs(in_arr[onyn__qwzgg], *data)
    output[0] = calc_out(minp, *data)
    for vhq__fnyq in range(1, N):
        s = start[vhq__fnyq]
        kfo__xdruv = end[vhq__fnyq]
        for onyn__qwzgg in range(start[vhq__fnyq - 1], s):
            data = remove_obs(in_arr[onyn__qwzgg], *data)
        for onyn__qwzgg in range(end[vhq__fnyq - 1], kfo__xdruv):
            data = add_obs(in_arr[onyn__qwzgg], *data)
        output[vhq__fnyq] = calc_out(minp, *data)
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
        xhia__wbc = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, watn__acwp, l_recv_req,
            ptji__jgsvx) = xhia__wbc
        if raw == False:
            wuv__fwoz = _border_icomm_var(index_arr, on_arr, rank, n_pes, win)
            (l_recv_buff_idx, esaw__cet, pejb__kjml, bqlf__jqcn,
                wquw__eqxbo, yrju__nouy) = wuv__fwoz
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp,
        start, end, kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(watn__acwp, watn__acwp, rank, n_pes, True, False)
        if raw == False:
            _border_send_wait(pejb__kjml, pejb__kjml, rank, n_pes, True, False)
            _border_send_wait(bqlf__jqcn, bqlf__jqcn, rank, n_pes, True, False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(ptji__jgsvx, True)
            if raw == False:
                bodo.libs.distributed_api.wait(wquw__eqxbo, True)
                bodo.libs.distributed_api.wait(yrju__nouy, True)
            num_zero_starts = 0
            for vhq__fnyq in range(0, N):
                if start[vhq__fnyq] != 0:
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
            for vhq__fnyq in range(0, num_zero_starts):
                nmv__sut = recv_starts[vhq__fnyq]
                ecd__bbh = np.concatenate((l_recv_buff[nmv__sut:], in_arr[:
                    vhq__fnyq + 1]))
                if len(ecd__bbh) - np.isnan(ecd__bbh).sum() >= minp:
                    output[vhq__fnyq] = kernel_func(ecd__bbh)
                else:
                    output[vhq__fnyq] = np.nan
        return impl

    def impl_series(output, in_arr, index_arr, num_zero_starts, recv_starts,
        l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
        for vhq__fnyq in range(0, num_zero_starts):
            nmv__sut = recv_starts[vhq__fnyq]
            ecd__bbh = np.concatenate((l_recv_buff[nmv__sut:], in_arr[:
                vhq__fnyq + 1]))
            jgbxi__uwkjh = np.concatenate((l_recv_buff_idx[nmv__sut:],
                index_arr[:vhq__fnyq + 1]))
            if len(ecd__bbh) - np.isnan(ecd__bbh).sum() >= minp:
                output[vhq__fnyq] = kernel_func(pd.Series(ecd__bbh,
                    jgbxi__uwkjh))
            else:
                output[vhq__fnyq] = np.nan
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
    for vhq__fnyq in range(0, N):
        s = start[vhq__fnyq]
        kfo__xdruv = end[vhq__fnyq]
        data = in_arr[s:kfo__xdruv]
        if kfo__xdruv - s - np.isnan(data).sum() >= minp:
            output[vhq__fnyq] = kernel_func(data)
        else:
            output[vhq__fnyq] = np.nan
    return output


def roll_variable_apply_seq_impl_series(in_arr, on_arr, index_arr, win,
    minp, start, end, kernel_func, raw):
    N = len(in_arr)
    output = np.empty(N, dtype=np.float64)
    for vhq__fnyq in range(0, N):
        s = start[vhq__fnyq]
        kfo__xdruv = end[vhq__fnyq]
        data = in_arr[s:kfo__xdruv]
        if kfo__xdruv - s - np.isnan(data).sum() >= minp:
            output[vhq__fnyq] = kernel_func(pd.Series(data, index_arr[s:
                kfo__xdruv]))
        else:
            output[vhq__fnyq] = np.nan
    return output


@register_jitable(cache=True)
def _build_indexer(on_arr, N, win, left_closed, right_closed):
    donlw__yrsnd = cast_dt64_arr_to_int(on_arr)
    start = np.empty(N, np.int64)
    end = np.empty(N, np.int64)
    start[0] = 0
    if right_closed:
        end[0] = 1
    else:
        end[0] = 0
    for vhq__fnyq in range(1, N):
        abmzi__kij = donlw__yrsnd[vhq__fnyq]
        tgszq__gvrqu = donlw__yrsnd[vhq__fnyq] - win
        if left_closed:
            tgszq__gvrqu -= 1
        start[vhq__fnyq] = vhq__fnyq
        for onyn__qwzgg in range(start[vhq__fnyq - 1], vhq__fnyq):
            if donlw__yrsnd[onyn__qwzgg] > tgszq__gvrqu:
                start[vhq__fnyq] = onyn__qwzgg
                break
        if donlw__yrsnd[end[vhq__fnyq - 1]] <= abmzi__kij:
            end[vhq__fnyq] = vhq__fnyq + 1
        else:
            end[vhq__fnyq] = end[vhq__fnyq - 1]
        if not right_closed:
            end[vhq__fnyq] -= 1
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
        iaw__qgqkt = sum_x / nobs
        if neg_ct == 0 and iaw__qgqkt < 0.0:
            iaw__qgqkt = 0
        elif neg_ct == nobs and iaw__qgqkt > 0.0:
            iaw__qgqkt = 0
    else:
        iaw__qgqkt = np.nan
    return iaw__qgqkt


@register_jitable
def init_data_var():
    return 0, 0.0, 0.0


@register_jitable
def add_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs += 1
        skka__eqfs = val - mean_x
        mean_x += skka__eqfs / nobs
        ssqdm_x += (nobs - 1) * skka__eqfs ** 2 / nobs
    return nobs, mean_x, ssqdm_x


@register_jitable
def remove_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs -= 1
        if nobs != 0:
            skka__eqfs = val - mean_x
            mean_x -= skka__eqfs / nobs
            ssqdm_x -= (nobs + 1) * skka__eqfs ** 2 / nobs
        else:
            mean_x = 0.0
            ssqdm_x = 0.0
    return nobs, mean_x, ssqdm_x


@register_jitable
def calc_var(minp, nobs, mean_x, ssqdm_x):
    bcsbi__sigr = 1.0
    iaw__qgqkt = np.nan
    if nobs >= minp and nobs > bcsbi__sigr:
        if nobs == 1:
            iaw__qgqkt = 0.0
        else:
            iaw__qgqkt = ssqdm_x / (nobs - bcsbi__sigr)
            if iaw__qgqkt < 0.0:
                iaw__qgqkt = 0.0
    return iaw__qgqkt


@register_jitable
def calc_std(minp, nobs, mean_x, ssqdm_x):
    jibjk__jitv = calc_var(minp, nobs, mean_x, ssqdm_x)
    return np.sqrt(jibjk__jitv)


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
        xhia__wbc = _border_icomm(in_arr, rank, n_pes, halo_size,
            send_right, send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            mtjcx__jof) = xhia__wbc
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
                bodo.libs.distributed_api.wait(mtjcx__jof, True)
                for vhq__fnyq in range(0, halo_size):
                    if bodo.libs.array_kernels.isna(r_recv_buff, vhq__fnyq):
                        bodo.libs.array_kernels.setna(output, N - halo_size +
                            vhq__fnyq)
                        continue
                    output[N - halo_size + vhq__fnyq] = r_recv_buff[vhq__fnyq]
    return output


@register_jitable(cache=True)
def shift_seq(in_arr, shift, output, is_parallel_str=False):
    N = len(in_arr)
    cob__cii = 1 if shift > 0 else -1
    shift = cob__cii * min(abs(shift), N)
    if shift > 0 and (not is_parallel_str or bodo.get_rank() == 0):
        bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
    start = max(shift, 0)
    end = min(N, N + shift)
    for vhq__fnyq in range(start, end):
        if bodo.libs.array_kernels.isna(in_arr, vhq__fnyq - shift):
            bodo.libs.array_kernels.setna(output, vhq__fnyq)
            continue
        output[vhq__fnyq] = in_arr[vhq__fnyq - shift]
    if shift < 0:
        bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
    return output


@register_jitable
def shift_left_recv(r_send_req, l_send_req, rank, n_pes, halo_size,
    l_recv_req, l_recv_buff, output):
    _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
    if rank != 0:
        bodo.libs.distributed_api.wait(l_recv_req, True)
        for vhq__fnyq in range(0, halo_size):
            if bodo.libs.array_kernels.isna(l_recv_buff, vhq__fnyq):
                bodo.libs.array_kernels.setna(output, vhq__fnyq)
                continue
            output[vhq__fnyq] = l_recv_buff[vhq__fnyq]


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
        xhia__wbc = _border_icomm(in_arr, rank, n_pes, halo_size,
            send_right, send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            mtjcx__jof) = xhia__wbc
    output = pct_change_seq(in_arr, shift)
    if parallel:
        if send_right:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
            if rank != 0:
                bodo.libs.distributed_api.wait(l_recv_req, True)
                for vhq__fnyq in range(0, halo_size):
                    knu__cou = l_recv_buff[vhq__fnyq]
                    output[vhq__fnyq] = (in_arr[vhq__fnyq] - knu__cou
                        ) / knu__cou
        else:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, False, True)
            if rank != n_pes - 1:
                bodo.libs.distributed_api.wait(mtjcx__jof, True)
                for vhq__fnyq in range(0, halo_size):
                    knu__cou = r_recv_buff[vhq__fnyq]
                    output[N - halo_size + vhq__fnyq] = (in_arr[N -
                        halo_size + vhq__fnyq] - knu__cou) / knu__cou
    return output


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_first_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[0]
    assert isinstance(arr.dtype, types.Float)
    kjg__ocosb = np.nan
    if arr.dtype == types.float32:
        kjg__ocosb = np.float32('nan')

    def impl(arr):
        for vhq__fnyq in range(len(arr)):
            if not bodo.libs.array_kernels.isna(arr, vhq__fnyq):
                return arr[vhq__fnyq]
        return kjg__ocosb
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_last_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[-1]
    assert isinstance(arr.dtype, types.Float)
    kjg__ocosb = np.nan
    if arr.dtype == types.float32:
        kjg__ocosb = np.float32('nan')

    def impl(arr):
        jdjg__epk = len(arr)
        for vhq__fnyq in range(len(arr)):
            hpkur__ywwy = jdjg__epk - vhq__fnyq - 1
            if not bodo.libs.array_kernels.isna(arr, hpkur__ywwy):
                return arr[hpkur__ywwy]
        return kjg__ocosb
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_one_from_arr_dtype(arr):
    one = arr.dtype(1)
    return lambda arr: one


@register_jitable(cache=True)
def pct_change_seq(in_arr, shift):
    N = len(in_arr)
    output = alloc_pct_change(N, in_arr)
    cob__cii = 1 if shift > 0 else -1
    shift = cob__cii * min(abs(shift), N)
    if shift > 0:
        bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
    else:
        bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
    if shift > 0:
        mop__lxv = get_first_non_na(in_arr[:shift])
        edtz__hov = get_last_non_na(in_arr[:shift])
    else:
        mop__lxv = get_last_non_na(in_arr[:-shift])
        edtz__hov = get_first_non_na(in_arr[:-shift])
    one = get_one_from_arr_dtype(output)
    start = max(shift, 0)
    end = min(N, N + shift)
    for vhq__fnyq in range(start, end):
        knu__cou = in_arr[vhq__fnyq - shift]
        if np.isnan(knu__cou):
            knu__cou = mop__lxv
        else:
            mop__lxv = knu__cou
        val = in_arr[vhq__fnyq]
        if np.isnan(val):
            val = edtz__hov
        else:
            edtz__hov = val
        output[vhq__fnyq] = val / knu__cou - one
    return output


@register_jitable(cache=True)
def _border_icomm(in_arr, rank, n_pes, halo_size, send_right=True,
    send_left=False):
    eaxr__nau = np.int32(comm_border_tag)
    l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    r_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    if send_right and rank != n_pes - 1:
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            halo_size, np.int32(rank + 1), eaxr__nau, True)
    if send_right and rank != 0:
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, halo_size,
            np.int32(rank - 1), eaxr__nau, True)
    if send_left and rank != 0:
        l_send_req = bodo.libs.distributed_api.isend(in_arr[:halo_size],
            halo_size, np.int32(rank - 1), eaxr__nau, True)
    if send_left and rank != n_pes - 1:
        mtjcx__jof = bodo.libs.distributed_api.irecv(r_recv_buff, halo_size,
            np.int32(rank + 1), eaxr__nau, True)
    return (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
        mtjcx__jof)


@register_jitable(cache=True)
def _border_icomm_var(in_arr, on_arr, rank, n_pes, win_size):
    eaxr__nau = np.int32(comm_border_tag)
    N = len(on_arr)
    halo_size = N
    end = on_arr[-1]
    for onyn__qwzgg in range(-2, -N, -1):
        euv__szej = on_arr[onyn__qwzgg]
        if end - euv__szej >= win_size:
            halo_size = -onyn__qwzgg
            break
    if rank != n_pes - 1:
        bodo.libs.distributed_api.send(halo_size, np.int32(rank + 1), eaxr__nau
            )
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            np.int32(halo_size), np.int32(rank + 1), eaxr__nau, True)
        watn__acwp = bodo.libs.distributed_api.isend(on_arr[-halo_size:],
            np.int32(halo_size), np.int32(rank + 1), eaxr__nau, True)
    if rank != 0:
        halo_size = bodo.libs.distributed_api.recv(np.int64, np.int32(rank -
            1), eaxr__nau)
        l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr)
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, np.int32(
            halo_size), np.int32(rank - 1), eaxr__nau, True)
        l_recv_t_buff = np.empty(halo_size, np.int64)
        ptji__jgsvx = bodo.libs.distributed_api.irecv(l_recv_t_buff, np.
            int32(halo_size), np.int32(rank - 1), eaxr__nau, True)
    return (l_recv_buff, l_recv_t_buff, r_send_req, watn__acwp, l_recv_req,
        ptji__jgsvx)


@register_jitable
def _border_send_wait(r_send_req, l_send_req, rank, n_pes, right, left):
    if right and rank != n_pes - 1:
        bodo.libs.distributed_api.wait(r_send_req, True)
    if left and rank != 0:
        bodo.libs.distributed_api.wait(l_send_req, True)


@register_jitable
def _is_small_for_parallel(N, halo_size):
    sejqp__xwelv = bodo.libs.distributed_api.dist_reduce(int(N <= 2 *
        halo_size + 1), np.int32(Reduce_Type.Sum.value))
    return sejqp__xwelv != 0


@register_jitable
def _handle_small_data(in_arr, win, minp, center, rank, n_pes, init_data,
    add_obs, remove_obs, calc_out):
    N = len(in_arr)
    mnpb__lvq = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.int32
        (Reduce_Type.Sum.value))
    woti__liq = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        lcmgs__yfoo, nlkix__ycqq = roll_fixed_linear_generic_seq(woti__liq,
            win, minp, center, init_data, add_obs, remove_obs, calc_out)
    else:
        lcmgs__yfoo = np.empty(mnpb__lvq, np.float64)
    bodo.libs.distributed_api.bcast(lcmgs__yfoo)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return lcmgs__yfoo[start:end]


@register_jitable
def _handle_small_data_apply(in_arr, index_arr, win, minp, center, rank,
    n_pes, kernel_func, raw=True):
    N = len(in_arr)
    mnpb__lvq = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.int32
        (Reduce_Type.Sum.value))
    woti__liq = bodo.libs.distributed_api.gatherv(in_arr)
    efio__tboc = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        lcmgs__yfoo = roll_fixed_apply_seq(woti__liq, efio__tboc, win, minp,
            center, kernel_func, raw)
    else:
        lcmgs__yfoo = np.empty(mnpb__lvq, np.float64)
    bodo.libs.distributed_api.bcast(lcmgs__yfoo)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return lcmgs__yfoo[start:end]


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
    mnpb__lvq = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.int32
        (Reduce_Type.Sum.value))
    woti__liq = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        lcmgs__yfoo = alloc_shift(len(woti__liq), woti__liq, (-1,))
        shift_seq(woti__liq, shift, lcmgs__yfoo)
        ikuwm__xhobj = bcast_n_chars_if_str_binary_arr(lcmgs__yfoo)
    else:
        ikuwm__xhobj = bcast_n_chars_if_str_binary_arr(in_arr)
        lcmgs__yfoo = alloc_shift(mnpb__lvq, in_arr, (ikuwm__xhobj,))
    bodo.libs.distributed_api.bcast(lcmgs__yfoo)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return lcmgs__yfoo[start:end]


@register_jitable
def _handle_small_data_pct_change(in_arr, shift, rank, n_pes):
    N = len(in_arr)
    mnpb__lvq = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    woti__liq = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        lcmgs__yfoo = pct_change_seq(woti__liq, shift)
    else:
        lcmgs__yfoo = alloc_pct_change(mnpb__lvq, in_arr)
    bodo.libs.distributed_api.bcast(lcmgs__yfoo)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return lcmgs__yfoo[start:end]


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
        svyg__lgxi = 1
    else:
        start = on_arr[0]
        end = on_arr[-1]
        jvznl__vsab = end - start
        svyg__lgxi = int(jvznl__vsab <= win_size)
    sejqp__xwelv = bodo.libs.distributed_api.dist_reduce(svyg__lgxi, np.
        int32(Reduce_Type.Sum.value))
    return sejqp__xwelv != 0


@register_jitable
def _handle_small_data_variable(in_arr, on_arr, win, minp, rank, n_pes,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    mnpb__lvq = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    woti__liq = bodo.libs.distributed_api.gatherv(in_arr)
    nyt__yeyu = bodo.libs.distributed_api.gatherv(on_arr)
    if rank == 0:
        start, end = _build_indexer(nyt__yeyu, mnpb__lvq, win, False, True)
        lcmgs__yfoo = roll_var_linear_generic_seq(woti__liq, nyt__yeyu, win,
            minp, start, end, init_data, add_obs, remove_obs, calc_out)
    else:
        lcmgs__yfoo = np.empty(mnpb__lvq, np.float64)
    bodo.libs.distributed_api.bcast(lcmgs__yfoo)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return lcmgs__yfoo[start:end]


@register_jitable
def _handle_small_data_variable_apply(in_arr, on_arr, index_arr, win, minp,
    rank, n_pes, kernel_func, raw):
    N = len(in_arr)
    mnpb__lvq = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    woti__liq = bodo.libs.distributed_api.gatherv(in_arr)
    nyt__yeyu = bodo.libs.distributed_api.gatherv(on_arr)
    efio__tboc = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        start, end = _build_indexer(nyt__yeyu, mnpb__lvq, win, False, True)
        lcmgs__yfoo = roll_variable_apply_seq(woti__liq, nyt__yeyu,
            efio__tboc, win, minp, start, end, kernel_func, raw)
    else:
        lcmgs__yfoo = np.empty(mnpb__lvq, np.float64)
    bodo.libs.distributed_api.bcast(lcmgs__yfoo)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return lcmgs__yfoo[start:end]


@register_jitable(cache=True)
def _dropna(arr):
    xdvj__vli = len(arr)
    hwpt__trxj = xdvj__vli - np.isnan(arr).sum()
    A = np.empty(hwpt__trxj, arr.dtype)
    dfi__fnzp = 0
    for vhq__fnyq in range(xdvj__vli):
        val = arr[vhq__fnyq]
        if not np.isnan(val):
            A[dfi__fnzp] = val
            dfi__fnzp += 1
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
