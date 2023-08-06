"""
Common utilities for all BodoSQL array kernels
"""
import math
import re
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from numba.core import types
import bodo
from bodo.utils.typing import is_overload_bool, is_overload_constant_bytes, is_overload_constant_number, is_overload_constant_str, is_overload_int, raise_bodo_error


def gen_vectorized(arg_names, arg_types, propagate_null, scalar_text,
    out_dtype, arg_string=None, arg_sources=None, array_override=None,
    support_dict_encoding=True, prefix_code=None):
    yhqiq__ljr = [bodo.utils.utils.is_array_typ(gco__hqzl, True) for
        gco__hqzl in arg_types]
    ecmuz__ofh = not any(yhqiq__ljr)
    qnqpp__gae = any([propagate_null[i] for i in range(len(arg_types)) if 
        arg_types[i] == bodo.none])
    yyjzy__izgx = 0
    bno__rpta = -1
    for i in range(len(arg_types)):
        if bodo.utils.utils.is_array_typ(arg_types[i], False):
            yyjzy__izgx += 1
            if arg_types[i] == bodo.dict_str_arr_type:
                bno__rpta = i
        elif bodo.utils.utils.is_array_typ(arg_types[i], True):
            yyjzy__izgx += 1
            if arg_types[i].dtype == bodo.dict_str_arr_type:
                bno__rpta = i
    ocfd__zvt = support_dict_encoding and yyjzy__izgx == 1 and bno__rpta >= 0
    uuy__bbicg = ocfd__zvt and out_dtype == bodo.string_array_type and (any
        (arg_types[i] == bodo.none and propagate_null[i] for i in range(len
        (arg_types))) or 'bodo.libs.array_kernels.setna' in scalar_text)
    if prefix_code is not None:
        fdzo__mcs = prefix_code.splitlines()[0]
        cql__deha = len(fdzo__mcs) - len(fdzo__mcs.lstrip())
    equr__nkr = scalar_text.splitlines()[0]
    aemuy__mjfw = len(equr__nkr) - len(equr__nkr.lstrip())
    if arg_string is None:
        arg_string = ', '.join(arg_names)
    jxy__emyxo = f'def impl({arg_string}):\n'
    if arg_sources is not None:
        for sqnl__hwkrt, mcppp__wdd in arg_sources.items():
            jxy__emyxo += f'   {sqnl__hwkrt} = {mcppp__wdd}\n'
    if prefix_code is not None and not qnqpp__gae:
        for jmr__dfal in prefix_code.splitlines():
            jxy__emyxo += ' ' * 3 + jmr__dfal[cql__deha:] + '\n'
    if ecmuz__ofh and array_override == None:
        if qnqpp__gae:
            jxy__emyxo += '   return None'
        else:
            for i in range(len(arg_names)):
                jxy__emyxo += f'   arg{i} = {arg_names[i]}\n'
            for jmr__dfal in scalar_text.splitlines():
                jxy__emyxo += ' ' * 3 + jmr__dfal[aemuy__mjfw:].replace(
                    'res[i] =', 'answer =').replace(
                    'bodo.libs.array_kernels.setna(res, i)', 'return None'
                    ) + '\n'
            jxy__emyxo += '   return answer'
    else:
        for i in range(len(arg_names)):
            if bodo.hiframes.pd_series_ext.is_series_type(arg_types[i]):
                jxy__emyxo += f"""   {arg_names[i]} = bodo.hiframes.pd_series_ext.get_series_data({arg_names[i]})
"""
        if array_override != None:
            cago__mmnj = f'len({array_override})'
        else:
            for i in range(len(arg_names)):
                if yhqiq__ljr[i]:
                    cago__mmnj = f'len({arg_names[i]})'
                    break
        if ocfd__zvt:
            if out_dtype == bodo.string_array_type:
                jxy__emyxo += (
                    f'   indices = {arg_names[bno__rpta]}._indices.copy()\n')
                jxy__emyxo += (
                    f'   has_global = {arg_names[bno__rpta]}._has_global_dictionary\n'
                    )
                jxy__emyxo += (
                    f'   {arg_names[i]} = {arg_names[bno__rpta]}._data\n')
            else:
                jxy__emyxo += f'   indices = {arg_names[bno__rpta]}._indices\n'
                jxy__emyxo += (
                    f'   {arg_names[i]} = {arg_names[bno__rpta]}._data\n')
        jxy__emyxo += f'   n = {cago__mmnj}\n'
        if ocfd__zvt:
            lijm__mzgl = 'n' if propagate_null[bno__rpta] else '(n + 1)'
            if not propagate_null[bno__rpta]:
                njgb__aowxi = arg_names[bno__rpta]
                jxy__emyxo += f"""   {njgb__aowxi} = bodo.libs.array_kernels.concat([{njgb__aowxi}, bodo.libs.array_kernels.gen_na_array(1, {njgb__aowxi})])
"""
            if out_dtype == bodo.string_array_type:
                jxy__emyxo += f"""   res = bodo.libs.str_arr_ext.pre_alloc_string_array({lijm__mzgl}, -1)
"""
            else:
                jxy__emyxo += f"""   res = bodo.utils.utils.alloc_type({lijm__mzgl}, out_dtype, (-1,))
"""
            jxy__emyxo += f'   for i in range({lijm__mzgl}):\n'
        else:
            jxy__emyxo += (
                '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n')
            jxy__emyxo += '   numba.parfors.parfor.init_prange()\n'
            jxy__emyxo += (
                '   for i in numba.parfors.parfor.internal_prange(n):\n')
        if qnqpp__gae:
            jxy__emyxo += f'      bodo.libs.array_kernels.setna(res, i)\n'
        else:
            for i in range(len(arg_names)):
                if yhqiq__ljr[i]:
                    if propagate_null[i]:
                        jxy__emyxo += (
                            f'      if bodo.libs.array_kernels.isna({arg_names[i]}, i):\n'
                            )
                        jxy__emyxo += (
                            '         bodo.libs.array_kernels.setna(res, i)\n')
                        jxy__emyxo += '         continue\n'
            for i in range(len(arg_names)):
                if yhqiq__ljr[i]:
                    jxy__emyxo += f'      arg{i} = {arg_names[i]}[i]\n'
                else:
                    jxy__emyxo += f'      arg{i} = {arg_names[i]}\n'
            for jmr__dfal in scalar_text.splitlines():
                jxy__emyxo += ' ' * 6 + jmr__dfal[aemuy__mjfw:] + '\n'
        if ocfd__zvt:
            if uuy__bbicg:
                jxy__emyxo += '   numba.parfors.parfor.init_prange()\n'
                jxy__emyxo += (
                    '   for i in numba.parfors.parfor.internal_prange(len(indices)):\n'
                    )
                jxy__emyxo += (
                    '      if not bodo.libs.array_kernels.isna(indices, i):\n')
                jxy__emyxo += '         loc = indices[i]\n'
                jxy__emyxo += (
                    '         if bodo.libs.array_kernels.isna(res, loc):\n')
                jxy__emyxo += (
                    '            bodo.libs.array_kernels.setna(indices, i)\n')
            if out_dtype == bodo.string_array_type:
                jxy__emyxo += """   res = bodo.libs.dict_arr_ext.init_dict_arr(res, indices, has_global)
"""
            else:
                jxy__emyxo += """   res2 = bodo.utils.utils.alloc_type(len(indices), out_dtype, (-1,))
"""
                jxy__emyxo += '   numba.parfors.parfor.init_prange()\n'
                jxy__emyxo += (
                    '   for i in numba.parfors.parfor.internal_prange(len(indices)):\n'
                    )
                if propagate_null[bno__rpta]:
                    jxy__emyxo += (
                        '      if bodo.libs.array_kernels.isna(indices, i):\n')
                    jxy__emyxo += (
                        '         bodo.libs.array_kernels.setna(res2, i)\n')
                    jxy__emyxo += '         continue\n'
                    jxy__emyxo += '      loc = indices[i]\n'
                else:
                    jxy__emyxo += """      loc = n if bodo.libs.array_kernels.isna(indices, i) else indices[i]
"""
                jxy__emyxo += (
                    '      if bodo.libs.array_kernels.isna(res, loc):\n')
                jxy__emyxo += (
                    '         bodo.libs.array_kernels.setna(res2, i)\n')
                jxy__emyxo += '      else:\n'
                jxy__emyxo += '         res2[i] = res[loc]\n'
                jxy__emyxo += '   res = res2\n'
        jxy__emyxo += '   return res'
    pps__baeox = {}
    exec(jxy__emyxo, {'bodo': bodo, 'math': math, 'numba': numba, 're': re,
        'np': np, 'out_dtype': out_dtype, 'pd': pd}, pps__baeox)
    bdy__fdot = pps__baeox['impl']
    return bdy__fdot


def unopt_argument(func_name, arg_names, i, container_length=None):
    if container_length != None:
        hjytg__nyl = [(f'{arg_names[0]}{[gdz__xyt]}' if gdz__xyt != i else
            'None') for gdz__xyt in range(container_length)]
        qbb__bhy = [(f'{arg_names[0]}{[gdz__xyt]}' if gdz__xyt != i else
            f'bodo.utils.indexing.unoptional({arg_names[0]}[{gdz__xyt}])') for
            gdz__xyt in range(container_length)]
        jxy__emyxo = f"def impl({', '.join(arg_names)}):\n"
        jxy__emyxo += f'   if {arg_names[0]}[{i}] is None:\n'
        jxy__emyxo += f"      return {func_name}(({', '.join(hjytg__nyl)}))\n"
        jxy__emyxo += f'   else:\n'
        jxy__emyxo += f"      return {func_name}(({', '.join(qbb__bhy)}))"
    else:
        hjytg__nyl = [(arg_names[gdz__xyt] if gdz__xyt != i else 'None') for
            gdz__xyt in range(len(arg_names))]
        qbb__bhy = [(arg_names[gdz__xyt] if gdz__xyt != i else
            f'bodo.utils.indexing.unoptional({arg_names[gdz__xyt]})') for
            gdz__xyt in range(len(arg_names))]
        jxy__emyxo = f"def impl({', '.join(arg_names)}):\n"
        jxy__emyxo += f'   if {arg_names[i]} is None:\n'
        jxy__emyxo += f"      return {func_name}({', '.join(hjytg__nyl)})\n"
        jxy__emyxo += f'   else:\n'
        jxy__emyxo += f"      return {func_name}({', '.join(qbb__bhy)})"
    pps__baeox = {}
    exec(jxy__emyxo, {'bodo': bodo, 'numba': numba}, pps__baeox)
    bdy__fdot = pps__baeox['impl']
    return bdy__fdot


def verify_int_arg(arg, f_name, a_name):
    if arg != types.none and not isinstance(arg, types.Integer) and not (bodo
        .utils.utils.is_array_typ(arg, True) and isinstance(arg.dtype,
        types.Integer)) and not is_overload_int(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be an integer, integer column, or null'
            )


def verify_int_float_arg(arg, f_name, a_name):
    if arg != types.none and not isinstance(arg, (types.Integer, types.
        Float, types.Boolean)) and not (bodo.utils.utils.is_array_typ(arg, 
        True) and isinstance(arg.dtype, (types.Integer, types.Float, types.
        Boolean))) and not is_overload_constant_number(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a numeric, numeric column, or null'
            )


def is_valid_string_arg(arg):
    return not (arg not in (types.none, types.unicode_type) and not
        isinstance(arg, types.StringLiteral) and not (bodo.utils.utils.
        is_array_typ(arg, True) and arg.dtype == types.unicode_type) and 
        not is_overload_constant_str(arg))


def is_valid_binary_arg(arg):
    return not (arg != bodo.bytes_type and not (bodo.utils.utils.
        is_array_typ(arg, True) and arg.dtype == bodo.bytes_type) and not
        is_overload_constant_bytes(arg) and not isinstance(arg, types.Bytes))


def verify_string_arg(arg, f_name, a_name):
    if not is_valid_string_arg(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a string, string column, or null'
            )


def verify_scalar_string_arg(arg, f_name, a_name):
    if arg not in (types.unicode_type, bodo.none) and not isinstance(arg,
        types.StringLiteral):
        raise_bodo_error(f'{f_name} {a_name} argument must be a scalar string')


def verify_binary_arg(arg, f_name, a_name):
    if not is_valid_binary_arg(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be binary data or null')


def verify_string_binary_arg(arg, f_name, a_name):
    mde__eayq = is_valid_string_arg(arg)
    klsmm__qzezs = is_valid_binary_arg(arg)
    if mde__eayq or klsmm__qzezs:
        return mde__eayq
    else:
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a binary data, string, string column, or null'
            )


def verify_boolean_arg(arg, f_name, a_name):
    if arg not in (types.none, types.boolean) and not (bodo.utils.utils.
        is_array_typ(arg, True) and arg.dtype == types.boolean
        ) and not is_overload_bool(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a boolean, boolean column, or null'
            )


def verify_datetime_arg(arg, f_name, a_name):
    if arg not in (types.none, bodo.datetime64ns, bodo.pd_timestamp_type,
        bodo.hiframes.datetime_date_ext.DatetimeDateType()) and not (bodo.
        utils.utils.is_array_typ(arg, True) and arg.dtype in (bodo.
        datetime64ns, bodo.hiframes.datetime_date_ext.DatetimeDateType())):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a datetime, datetime column, or null'
            )


def get_common_broadcasted_type(arg_types, func_name):
    lihup__oqk = []
    for i in range(len(arg_types)):
        if bodo.utils.utils.is_array_typ(arg_types[i], False):
            lihup__oqk.append(arg_types[i])
        elif bodo.utils.utils.is_array_typ(arg_types[i], True):
            lihup__oqk.append(arg_types[i].data)
        else:
            lihup__oqk.append(arg_types[i])
    if len(lihup__oqk) == 0:
        return bodo.none
    elif len(lihup__oqk) == 1:
        if bodo.utils.utils.is_array_typ(lihup__oqk[0]):
            return bodo.utils.typing.to_nullable_type(lihup__oqk[0])
        elif lihup__oqk[0] == bodo.none:
            return bodo.none
        else:
            return bodo.utils.typing.to_nullable_type(bodo.utils.typing.
                dtype_to_array_type(lihup__oqk[0]))
    else:
        gsy__bpda = []
        for i in range(len(arg_types)):
            if bodo.utils.utils.is_array_typ(arg_types[i]):
                gsy__bpda.append(lihup__oqk[i].dtype)
            elif lihup__oqk[i] == bodo.none:
                pass
            else:
                gsy__bpda.append(lihup__oqk[i])
        if len(gsy__bpda) == 0:
            return bodo.none
        xbkzm__adpmo, maqub__wbd = bodo.utils.typing.get_common_scalar_dtype(
            gsy__bpda)
        if not maqub__wbd:
            raise_bodo_error(
                f'Cannot call {func_name} on columns with different dtypes')
        return bodo.utils.typing.to_nullable_type(bodo.utils.typing.
            dtype_to_array_type(xbkzm__adpmo))


def vectorized_sol(args, scalar_fn, dtype, manual_coercion=False):
    nigrk__ograk = -1
    for arg in args:
        if isinstance(arg, (pd.core.arrays.base.ExtensionArray, pd.Series,
            np.ndarray, pa.Array)):
            nigrk__ograk = len(arg)
            break
    if nigrk__ograk == -1:
        return dtype(scalar_fn(*args)) if manual_coercion else scalar_fn(*args)
    wde__nhu = []
    for arg in args:
        if isinstance(arg, (pd.core.arrays.base.ExtensionArray, pd.Series,
            np.ndarray, pa.Array)):
            wde__nhu.append(arg)
        else:
            wde__nhu.append([arg] * nigrk__ograk)
    if manual_coercion:
        return pd.Series([dtype(scalar_fn(*fgt__yhm)) for fgt__yhm in zip(*
            wde__nhu)])
    else:
        return pd.Series([scalar_fn(*fgt__yhm) for fgt__yhm in zip(*
            wde__nhu)], dtype=dtype)


def gen_windowed(calculate_block, constant_block, out_dtype, setup_block=
    None, enter_block=None, exit_block=None, empty_block=None):
    lvi__drygv = calculate_block.splitlines()
    zmpli__nux = len(lvi__drygv[0]) - len(lvi__drygv[0].lstrip())
    kij__qbluu = constant_block.splitlines()
    vps__mzjrw = len(kij__qbluu[0]) - len(kij__qbluu[0].lstrip())
    if setup_block != None:
        wkv__zlln = setup_block.splitlines()
        nehdp__bbaao = len(wkv__zlln[0]) - len(wkv__zlln[0].lstrip())
    if enter_block != None:
        hqs__idcy = enter_block.splitlines()
        ect__dad = len(hqs__idcy[0]) - len(hqs__idcy[0].lstrip())
    if exit_block != None:
        xvlo__rwmyd = exit_block.splitlines()
        ujvfx__qye = len(xvlo__rwmyd[0]) - len(xvlo__rwmyd[0].lstrip())
    if empty_block == None:
        empty_block = 'bodo.libs.array_kernels.setna(res, i)'
    ogvt__bqsb = empty_block.splitlines()
    yrkls__nmb = len(ogvt__bqsb[0]) - len(ogvt__bqsb[0].lstrip())
    jxy__emyxo = 'def impl(S, lower_bound, upper_bound):\n'
    jxy__emyxo += '   n = len(S)\n'
    jxy__emyxo += '   arr = bodo.utils.conversion.coerce_to_array(S)\n'
    jxy__emyxo += '   res = bodo.utils.utils.alloc_type(n, out_dtype, -1)\n'
    jxy__emyxo += '   if upper_bound < lower_bound:\n'
    jxy__emyxo += '      for i in range(n):\n'
    jxy__emyxo += '         bodo.libs.array_kernels.setna(res, i)\n'
    jxy__emyxo += '   elif lower_bound <= -n+1 and n-1 <= upper_bound:\n'
    jxy__emyxo += '\n'.join([(' ' * 6 + jmr__dfal[vps__mzjrw:]) for
        jmr__dfal in kij__qbluu]) + '\n'
    jxy__emyxo += '      for i in range(n):\n'
    jxy__emyxo += '         res[i] = constant_value\n'
    jxy__emyxo += '   else:\n'
    jxy__emyxo += '      exiting = lower_bound\n'
    jxy__emyxo += '      entering = upper_bound\n'
    jxy__emyxo += '      in_window = 0\n'
    if setup_block != None:
        jxy__emyxo += '\n'.join([(' ' * 6 + jmr__dfal[nehdp__bbaao:]) for
            jmr__dfal in wkv__zlln]) + '\n'
    jxy__emyxo += (
        '      for i in range(min(max(0, exiting), n), min(max(0, entering + 1), n)):\n'
        )
    jxy__emyxo += '         if not bodo.libs.array_kernels.isna(arr, i):\n'
    jxy__emyxo += '            in_window += 1\n'
    if enter_block != None:
        if 'elem' in enter_block:
            jxy__emyxo += '            elem = arr[i]\n'
        jxy__emyxo += '\n'.join([(' ' * 12 + jmr__dfal[ect__dad:]) for
            jmr__dfal in hqs__idcy]) + '\n'
    jxy__emyxo += '      for i in range(n):\n'
    jxy__emyxo += '         if in_window == 0:\n'
    jxy__emyxo += '\n'.join([(' ' * 12 + jmr__dfal[yrkls__nmb:]) for
        jmr__dfal in ogvt__bqsb]) + '\n'
    jxy__emyxo += '         else:\n'
    jxy__emyxo += '\n'.join([(' ' * 12 + jmr__dfal[zmpli__nux:]) for
        jmr__dfal in lvi__drygv]) + '\n'
    jxy__emyxo += '         if 0 <= exiting < n:\n'
    jxy__emyxo += (
        '            if not bodo.libs.array_kernels.isna(arr, exiting):\n')
    jxy__emyxo += '               in_window -= 1\n'
    if exit_block != None:
        if 'elem' in exit_block:
            jxy__emyxo += '               elem = arr[exiting]\n'
        jxy__emyxo += '\n'.join([(' ' * 15 + jmr__dfal[ujvfx__qye:]) for
            jmr__dfal in xvlo__rwmyd]) + '\n'
    jxy__emyxo += '         exiting += 1\n'
    jxy__emyxo += '         entering += 1\n'
    jxy__emyxo += '         if 0 <= entering < n:\n'
    jxy__emyxo += (
        '            if not bodo.libs.array_kernels.isna(arr, entering):\n')
    jxy__emyxo += '               in_window += 1\n'
    if enter_block != None:
        if 'elem' in enter_block:
            jxy__emyxo += '               elem = arr[entering]\n'
        jxy__emyxo += '\n'.join([(' ' * 15 + jmr__dfal[ect__dad:]) for
            jmr__dfal in hqs__idcy]) + '\n'
    jxy__emyxo += '   return res'
    pps__baeox = {}
    exec(jxy__emyxo, {'bodo': bodo, 'numba': numba, 'np': np, 'out_dtype':
        out_dtype, 'pd': pd}, pps__baeox)
    bdy__fdot = pps__baeox['impl']
    return bdy__fdot
