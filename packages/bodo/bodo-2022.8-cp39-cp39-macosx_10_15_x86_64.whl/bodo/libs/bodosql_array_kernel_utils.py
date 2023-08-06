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
    kgzt__hzd = [bodo.utils.utils.is_array_typ(ovw__mwnc, True) for
        ovw__mwnc in arg_types]
    riu__cvzh = not any(kgzt__hzd)
    yujw__ipzc = any([propagate_null[i] for i in range(len(arg_types)) if 
        arg_types[i] == bodo.none])
    uhuv__gmkvu = 0
    ivqzz__bnzua = -1
    for i in range(len(arg_types)):
        if bodo.utils.utils.is_array_typ(arg_types[i], False):
            uhuv__gmkvu += 1
            if arg_types[i] == bodo.dict_str_arr_type:
                ivqzz__bnzua = i
        elif bodo.utils.utils.is_array_typ(arg_types[i], True):
            uhuv__gmkvu += 1
            if arg_types[i].dtype == bodo.dict_str_arr_type:
                ivqzz__bnzua = i
    onzoz__hpw = (support_dict_encoding and uhuv__gmkvu == 1 and 
        ivqzz__bnzua >= 0)
    banhr__zbtlx = onzoz__hpw and out_dtype == bodo.string_array_type and (any
        (arg_types[i] == bodo.none and propagate_null[i] for i in range(len
        (arg_types))) or 'bodo.libs.array_kernels.setna' in scalar_text)
    if prefix_code is not None:
        lfv__bdszj = prefix_code.splitlines()[0]
        sfwpm__glpmm = len(lfv__bdszj) - len(lfv__bdszj.lstrip())
    ssewv__eeueh = scalar_text.splitlines()[0]
    tqdc__fkud = len(ssewv__eeueh) - len(ssewv__eeueh.lstrip())
    if arg_string is None:
        arg_string = ', '.join(arg_names)
    tmrpy__fma = f'def impl({arg_string}):\n'
    if arg_sources is not None:
        for ika__bwao, aam__dzohz in arg_sources.items():
            tmrpy__fma += f'   {ika__bwao} = {aam__dzohz}\n'
    if prefix_code is not None and not yujw__ipzc:
        for ovldm__qbc in prefix_code.splitlines():
            tmrpy__fma += ' ' * 3 + ovldm__qbc[sfwpm__glpmm:] + '\n'
    if riu__cvzh and array_override == None:
        if yujw__ipzc:
            tmrpy__fma += '   return None'
        else:
            for i in range(len(arg_names)):
                tmrpy__fma += f'   arg{i} = {arg_names[i]}\n'
            for ovldm__qbc in scalar_text.splitlines():
                tmrpy__fma += ' ' * 3 + ovldm__qbc[tqdc__fkud:].replace(
                    'res[i] =', 'answer =').replace(
                    'bodo.libs.array_kernels.setna(res, i)', 'return None'
                    ) + '\n'
            tmrpy__fma += '   return answer'
    else:
        for i in range(len(arg_names)):
            if bodo.hiframes.pd_series_ext.is_series_type(arg_types[i]):
                tmrpy__fma += f"""   {arg_names[i]} = bodo.hiframes.pd_series_ext.get_series_data({arg_names[i]})
"""
        if array_override != None:
            yslpl__hfutv = f'len({array_override})'
        else:
            for i in range(len(arg_names)):
                if kgzt__hzd[i]:
                    yslpl__hfutv = f'len({arg_names[i]})'
                    break
        if onzoz__hpw:
            if out_dtype == bodo.string_array_type:
                tmrpy__fma += (
                    f'   indices = {arg_names[ivqzz__bnzua]}._indices.copy()\n'
                    )
                tmrpy__fma += (
                    f'   has_global = {arg_names[ivqzz__bnzua]}._has_global_dictionary\n'
                    )
                tmrpy__fma += (
                    f'   {arg_names[i]} = {arg_names[ivqzz__bnzua]}._data\n')
            else:
                tmrpy__fma += (
                    f'   indices = {arg_names[ivqzz__bnzua]}._indices\n')
                tmrpy__fma += (
                    f'   {arg_names[i]} = {arg_names[ivqzz__bnzua]}._data\n')
        tmrpy__fma += f'   n = {yslpl__hfutv}\n'
        if onzoz__hpw:
            hacuy__qof = 'n' if propagate_null[ivqzz__bnzua] else '(n + 1)'
            if not propagate_null[ivqzz__bnzua]:
                qkbxp__azso = arg_names[ivqzz__bnzua]
                tmrpy__fma += f"""   {qkbxp__azso} = bodo.libs.array_kernels.concat([{qkbxp__azso}, bodo.libs.array_kernels.gen_na_array(1, {qkbxp__azso})])
"""
            if out_dtype == bodo.string_array_type:
                tmrpy__fma += f"""   res = bodo.libs.str_arr_ext.pre_alloc_string_array({hacuy__qof}, -1)
"""
            else:
                tmrpy__fma += f"""   res = bodo.utils.utils.alloc_type({hacuy__qof}, out_dtype, (-1,))
"""
            tmrpy__fma += f'   for i in range({hacuy__qof}):\n'
        else:
            tmrpy__fma += (
                '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n')
            tmrpy__fma += '   numba.parfors.parfor.init_prange()\n'
            tmrpy__fma += (
                '   for i in numba.parfors.parfor.internal_prange(n):\n')
        if yujw__ipzc:
            tmrpy__fma += f'      bodo.libs.array_kernels.setna(res, i)\n'
        else:
            for i in range(len(arg_names)):
                if kgzt__hzd[i]:
                    if propagate_null[i]:
                        tmrpy__fma += (
                            f'      if bodo.libs.array_kernels.isna({arg_names[i]}, i):\n'
                            )
                        tmrpy__fma += (
                            '         bodo.libs.array_kernels.setna(res, i)\n')
                        tmrpy__fma += '         continue\n'
            for i in range(len(arg_names)):
                if kgzt__hzd[i]:
                    tmrpy__fma += f'      arg{i} = {arg_names[i]}[i]\n'
                else:
                    tmrpy__fma += f'      arg{i} = {arg_names[i]}\n'
            for ovldm__qbc in scalar_text.splitlines():
                tmrpy__fma += ' ' * 6 + ovldm__qbc[tqdc__fkud:] + '\n'
        if onzoz__hpw:
            if banhr__zbtlx:
                tmrpy__fma += '   numba.parfors.parfor.init_prange()\n'
                tmrpy__fma += (
                    '   for i in numba.parfors.parfor.internal_prange(len(indices)):\n'
                    )
                tmrpy__fma += (
                    '      if not bodo.libs.array_kernels.isna(indices, i):\n')
                tmrpy__fma += '         loc = indices[i]\n'
                tmrpy__fma += (
                    '         if bodo.libs.array_kernels.isna(res, loc):\n')
                tmrpy__fma += (
                    '            bodo.libs.array_kernels.setna(indices, i)\n')
            if out_dtype == bodo.string_array_type:
                tmrpy__fma += """   res = bodo.libs.dict_arr_ext.init_dict_arr(res, indices, has_global)
"""
            else:
                tmrpy__fma += """   res2 = bodo.utils.utils.alloc_type(len(indices), out_dtype, (-1,))
"""
                tmrpy__fma += '   numba.parfors.parfor.init_prange()\n'
                tmrpy__fma += (
                    '   for i in numba.parfors.parfor.internal_prange(len(indices)):\n'
                    )
                if propagate_null[ivqzz__bnzua]:
                    tmrpy__fma += (
                        '      if bodo.libs.array_kernels.isna(indices, i):\n')
                    tmrpy__fma += (
                        '         bodo.libs.array_kernels.setna(res2, i)\n')
                    tmrpy__fma += '         continue\n'
                    tmrpy__fma += '      loc = indices[i]\n'
                else:
                    tmrpy__fma += """      loc = n if bodo.libs.array_kernels.isna(indices, i) else indices[i]
"""
                tmrpy__fma += (
                    '      if bodo.libs.array_kernels.isna(res, loc):\n')
                tmrpy__fma += (
                    '         bodo.libs.array_kernels.setna(res2, i)\n')
                tmrpy__fma += '      else:\n'
                tmrpy__fma += '         res2[i] = res[loc]\n'
                tmrpy__fma += '   res = res2\n'
        tmrpy__fma += '   return res'
    bnd__ufgqa = {}
    exec(tmrpy__fma, {'bodo': bodo, 'math': math, 'numba': numba, 're': re,
        'np': np, 'out_dtype': out_dtype, 'pd': pd}, bnd__ufgqa)
    ulnav__lcx = bnd__ufgqa['impl']
    return ulnav__lcx


def unopt_argument(func_name, arg_names, i, container_length=None):
    if container_length != None:
        qudbm__xwtw = [(f'{arg_names[0]}{[wni__mcrot]}' if wni__mcrot != i else
            'None') for wni__mcrot in range(container_length)]
        pwu__gqhqm = [(f'{arg_names[0]}{[wni__mcrot]}' if wni__mcrot != i else
            f'bodo.utils.indexing.unoptional({arg_names[0]}[{wni__mcrot}])'
            ) for wni__mcrot in range(container_length)]
        tmrpy__fma = f"def impl({', '.join(arg_names)}):\n"
        tmrpy__fma += f'   if {arg_names[0]}[{i}] is None:\n'
        tmrpy__fma += f"      return {func_name}(({', '.join(qudbm__xwtw)}))\n"
        tmrpy__fma += f'   else:\n'
        tmrpy__fma += f"      return {func_name}(({', '.join(pwu__gqhqm)}))"
    else:
        qudbm__xwtw = [(arg_names[wni__mcrot] if wni__mcrot != i else
            'None') for wni__mcrot in range(len(arg_names))]
        pwu__gqhqm = [(arg_names[wni__mcrot] if wni__mcrot != i else
            f'bodo.utils.indexing.unoptional({arg_names[wni__mcrot]})') for
            wni__mcrot in range(len(arg_names))]
        tmrpy__fma = f"def impl({', '.join(arg_names)}):\n"
        tmrpy__fma += f'   if {arg_names[i]} is None:\n'
        tmrpy__fma += f"      return {func_name}({', '.join(qudbm__xwtw)})\n"
        tmrpy__fma += f'   else:\n'
        tmrpy__fma += f"      return {func_name}({', '.join(pwu__gqhqm)})"
    bnd__ufgqa = {}
    exec(tmrpy__fma, {'bodo': bodo, 'numba': numba}, bnd__ufgqa)
    ulnav__lcx = bnd__ufgqa['impl']
    return ulnav__lcx


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
    keuu__okbq = is_valid_string_arg(arg)
    mqu__usm = is_valid_binary_arg(arg)
    if keuu__okbq or mqu__usm:
        return keuu__okbq
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
    uala__itt = []
    for i in range(len(arg_types)):
        if bodo.utils.utils.is_array_typ(arg_types[i], False):
            uala__itt.append(arg_types[i])
        elif bodo.utils.utils.is_array_typ(arg_types[i], True):
            uala__itt.append(arg_types[i].data)
        else:
            uala__itt.append(arg_types[i])
    if len(uala__itt) == 0:
        return bodo.none
    elif len(uala__itt) == 1:
        if bodo.utils.utils.is_array_typ(uala__itt[0]):
            return bodo.utils.typing.to_nullable_type(uala__itt[0])
        elif uala__itt[0] == bodo.none:
            return bodo.none
        else:
            return bodo.utils.typing.to_nullable_type(bodo.utils.typing.
                dtype_to_array_type(uala__itt[0]))
    else:
        gfw__lcjux = []
        for i in range(len(arg_types)):
            if bodo.utils.utils.is_array_typ(arg_types[i]):
                gfw__lcjux.append(uala__itt[i].dtype)
            elif uala__itt[i] == bodo.none:
                pass
            else:
                gfw__lcjux.append(uala__itt[i])
        if len(gfw__lcjux) == 0:
            return bodo.none
        gqxx__jcwep, qjcxl__lfuc = bodo.utils.typing.get_common_scalar_dtype(
            gfw__lcjux)
        if not qjcxl__lfuc:
            raise_bodo_error(
                f'Cannot call {func_name} on columns with different dtypes')
        return bodo.utils.typing.to_nullable_type(bodo.utils.typing.
            dtype_to_array_type(gqxx__jcwep))


def vectorized_sol(args, scalar_fn, dtype, manual_coercion=False):
    izo__aqkyh = -1
    for arg in args:
        if isinstance(arg, (pd.core.arrays.base.ExtensionArray, pd.Series,
            np.ndarray, pa.Array)):
            izo__aqkyh = len(arg)
            break
    if izo__aqkyh == -1:
        return dtype(scalar_fn(*args)) if manual_coercion else scalar_fn(*args)
    jzfly__eak = []
    for arg in args:
        if isinstance(arg, (pd.core.arrays.base.ExtensionArray, pd.Series,
            np.ndarray, pa.Array)):
            jzfly__eak.append(arg)
        else:
            jzfly__eak.append([arg] * izo__aqkyh)
    if manual_coercion:
        return pd.Series([dtype(scalar_fn(*hpa__gtuvm)) for hpa__gtuvm in
            zip(*jzfly__eak)])
    else:
        return pd.Series([scalar_fn(*hpa__gtuvm) for hpa__gtuvm in zip(*
            jzfly__eak)], dtype=dtype)


def gen_windowed(calculate_block, constant_block, out_dtype, setup_block=
    None, enter_block=None, exit_block=None, empty_block=None):
    wflyf__wsmjh = calculate_block.splitlines()
    rsw__zsatf = len(wflyf__wsmjh[0]) - len(wflyf__wsmjh[0].lstrip())
    kalac__reut = constant_block.splitlines()
    gpxj__ers = len(kalac__reut[0]) - len(kalac__reut[0].lstrip())
    if setup_block != None:
        hpg__vzdav = setup_block.splitlines()
        omctb__tchu = len(hpg__vzdav[0]) - len(hpg__vzdav[0].lstrip())
    if enter_block != None:
        kbh__ntqv = enter_block.splitlines()
        nzuno__nrvn = len(kbh__ntqv[0]) - len(kbh__ntqv[0].lstrip())
    if exit_block != None:
        ztf__wjwl = exit_block.splitlines()
        pbzxj__itx = len(ztf__wjwl[0]) - len(ztf__wjwl[0].lstrip())
    if empty_block == None:
        empty_block = 'bodo.libs.array_kernels.setna(res, i)'
    krdvh__ufx = empty_block.splitlines()
    bhha__fpp = len(krdvh__ufx[0]) - len(krdvh__ufx[0].lstrip())
    tmrpy__fma = 'def impl(S, lower_bound, upper_bound):\n'
    tmrpy__fma += '   n = len(S)\n'
    tmrpy__fma += '   arr = bodo.utils.conversion.coerce_to_array(S)\n'
    tmrpy__fma += '   res = bodo.utils.utils.alloc_type(n, out_dtype, -1)\n'
    tmrpy__fma += '   if upper_bound < lower_bound:\n'
    tmrpy__fma += '      for i in range(n):\n'
    tmrpy__fma += '         bodo.libs.array_kernels.setna(res, i)\n'
    tmrpy__fma += '   elif lower_bound <= -n+1 and n-1 <= upper_bound:\n'
    tmrpy__fma += '\n'.join([(' ' * 6 + ovldm__qbc[gpxj__ers:]) for
        ovldm__qbc in kalac__reut]) + '\n'
    tmrpy__fma += '      for i in range(n):\n'
    tmrpy__fma += '         res[i] = constant_value\n'
    tmrpy__fma += '   else:\n'
    tmrpy__fma += '      exiting = lower_bound\n'
    tmrpy__fma += '      entering = upper_bound\n'
    tmrpy__fma += '      in_window = 0\n'
    if setup_block != None:
        tmrpy__fma += '\n'.join([(' ' * 6 + ovldm__qbc[omctb__tchu:]) for
            ovldm__qbc in hpg__vzdav]) + '\n'
    tmrpy__fma += (
        '      for i in range(min(max(0, exiting), n), min(max(0, entering + 1), n)):\n'
        )
    tmrpy__fma += '         if not bodo.libs.array_kernels.isna(arr, i):\n'
    tmrpy__fma += '            in_window += 1\n'
    if enter_block != None:
        if 'elem' in enter_block:
            tmrpy__fma += '            elem = arr[i]\n'
        tmrpy__fma += '\n'.join([(' ' * 12 + ovldm__qbc[nzuno__nrvn:]) for
            ovldm__qbc in kbh__ntqv]) + '\n'
    tmrpy__fma += '      for i in range(n):\n'
    tmrpy__fma += '         if in_window == 0:\n'
    tmrpy__fma += '\n'.join([(' ' * 12 + ovldm__qbc[bhha__fpp:]) for
        ovldm__qbc in krdvh__ufx]) + '\n'
    tmrpy__fma += '         else:\n'
    tmrpy__fma += '\n'.join([(' ' * 12 + ovldm__qbc[rsw__zsatf:]) for
        ovldm__qbc in wflyf__wsmjh]) + '\n'
    tmrpy__fma += '         if 0 <= exiting < n:\n'
    tmrpy__fma += (
        '            if not bodo.libs.array_kernels.isna(arr, exiting):\n')
    tmrpy__fma += '               in_window -= 1\n'
    if exit_block != None:
        if 'elem' in exit_block:
            tmrpy__fma += '               elem = arr[exiting]\n'
        tmrpy__fma += '\n'.join([(' ' * 15 + ovldm__qbc[pbzxj__itx:]) for
            ovldm__qbc in ztf__wjwl]) + '\n'
    tmrpy__fma += '         exiting += 1\n'
    tmrpy__fma += '         entering += 1\n'
    tmrpy__fma += '         if 0 <= entering < n:\n'
    tmrpy__fma += (
        '            if not bodo.libs.array_kernels.isna(arr, entering):\n')
    tmrpy__fma += '               in_window += 1\n'
    if enter_block != None:
        if 'elem' in enter_block:
            tmrpy__fma += '               elem = arr[entering]\n'
        tmrpy__fma += '\n'.join([(' ' * 15 + ovldm__qbc[nzuno__nrvn:]) for
            ovldm__qbc in kbh__ntqv]) + '\n'
    tmrpy__fma += '   return res'
    bnd__ufgqa = {}
    exec(tmrpy__fma, {'bodo': bodo, 'numba': numba, 'np': np, 'out_dtype':
        out_dtype, 'pd': pd}, bnd__ufgqa)
    ulnav__lcx = bnd__ufgqa['impl']
    return ulnav__lcx
