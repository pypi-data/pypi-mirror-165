"""
Implements regexp array kernels that are specific to BodoSQL
"""
import re
import numba
from numba.core import types
import bodo
from bodo.libs.bodosql_array_kernel_utils import *


def posix_to_re(pattern):
    psn__qzn = {'[:alnum:]': 'A-Za-z0-9', '[:alpha:]': 'A-Za-z',
        '[:ascii:]': '\x01-\x7f', '[:blank:]': ' \t', '[:cntrl:]':
        '\x01-\x1f\x7f', '[:digit:]': '0-9', '[:graph:]': '!-~',
        '[:lower:]': 'a-z', '[:print:]': ' -~', '[:punct:]':
        '\\]\\[!"#$%&\'()*+,./:;<=>?@\\^_`{|}~-', '[:space:]':
        ' \t\r\n\x0b\x0c', '[:upper:]': 'A-Z', '[:word:]': 'A-Za-z0-9_',
        '[:xdigit:]': 'A-Fa-f0-9'}
    for swq__abkde in psn__qzn:
        pattern = pattern.replace(swq__abkde, psn__qzn[swq__abkde])
    return pattern


def make_flag_bitvector(flags):
    ijxc__qsjd = 0
    if 'i' in flags:
        if 'c' not in flags or flags.rindex('i') > flags.rindex('c'):
            ijxc__qsjd = ijxc__qsjd | re.I
    if 'm' in flags:
        ijxc__qsjd = ijxc__qsjd | re.M
    if 's' in flags:
        ijxc__qsjd = ijxc__qsjd | re.S
    return ijxc__qsjd


@numba.generated_jit(nopython=True)
def regexp_count(arr, pattern, position, flags):
    args = [arr, pattern, position, flags]
    for mndp__vgml in range(4):
        if isinstance(args[mndp__vgml], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_count', ['arr',
                'pattern', 'position', 'flags'], mndp__vgml)

    def impl(arr, pattern, position, flags):
        return regexp_count_util(arr, numba.literally(pattern), position,
            numba.literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_instr(arr, pattern, position, occurrence, option, flags, group):
    args = [arr, pattern, position, occurrence, option, flags, group]
    for mndp__vgml in range(7):
        if isinstance(args[mndp__vgml], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_instr', ['arr',
                'pattern', 'position', 'occurrence', 'option', 'flags',
                'group'], mndp__vgml)

    def impl(arr, pattern, position, occurrence, option, flags, group):
        return regexp_instr_util(arr, numba.literally(pattern), position,
            occurrence, option, numba.literally(flags), group)
    return impl


@numba.generated_jit(nopython=True)
def regexp_like(arr, pattern, flags):
    args = [arr, pattern, flags]
    for mndp__vgml in range(3):
        if isinstance(args[mndp__vgml], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regexp_like'
                , ['arr', 'pattern', 'flags'], mndp__vgml)

    def impl(arr, pattern, flags):
        return regexp_like_util(arr, numba.literally(pattern), numba.
            literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_replace(arr, pattern, replacement, position, occurrence, flags):
    args = [arr, pattern, replacement, position, occurrence, flags]
    for mndp__vgml in range(6):
        if isinstance(args[mndp__vgml], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_replace', ['arr',
                'pattern', 'replacement', 'position', 'occurrence', 'flags'
                ], mndp__vgml)

    def impl(arr, pattern, replacement, position, occurrence, flags):
        return regexp_replace_util(arr, numba.literally(pattern),
            replacement, position, occurrence, numba.literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_substr(arr, pattern, position, occurrence, flags, group):
    args = [arr, pattern, position, occurrence, flags, group]
    for mndp__vgml in range(6):
        if isinstance(args[mndp__vgml], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_substr', ['arr',
                'pattern', 'position', 'occurrence', 'flags', 'group'],
                mndp__vgml)

    def impl(arr, pattern, position, occurrence, flags, group):
        return regexp_substr_util(arr, numba.literally(pattern), position,
            occurrence, numba.literally(flags), group)
    return impl


@numba.generated_jit(nopython=True)
def regexp_count_util(arr, pattern, position, flags):
    verify_string_arg(arr, 'REGEXP_COUNT', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_COUNT', 'pattern')
    verify_int_arg(position, 'REGEXP_COUNT', 'position')
    verify_scalar_string_arg(flags, 'REGEXP_COUNT', 'flags')
    fhm__jbap = ['arr', 'pattern', 'position', 'flags']
    eleby__xfrr = [arr, pattern, position, flags]
    jlk__xmy = [True] * 4
    fgbua__vfmc = bodo.utils.typing.get_overload_const_str(pattern)
    rwyng__nbvws = posix_to_re(fgbua__vfmc)
    enlv__qygrm = bodo.utils.typing.get_overload_const_str(flags)
    owx__kca = make_flag_bitvector(enlv__qygrm)
    zlj__erdi = '\n'
    xyzc__ewia = ''
    if bodo.utils.utils.is_array_typ(position, True):
        xyzc__ewia += """if arg2 <= 0: raise ValueError('REGEXP_COUNT requires a positive position')
"""
    else:
        zlj__erdi += """if position <= 0: raise ValueError('REGEXP_COUNT requires a positive position')
"""
    if rwyng__nbvws == '':
        xyzc__ewia += 'res[i] = 0'
    else:
        zlj__erdi += f'r = re.compile({repr(rwyng__nbvws)}, {owx__kca})'
        xyzc__ewia += 'res[i] = len(r.findall(arg0[arg2-1:]))'
    vdd__ewfh = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(fhm__jbap, eleby__xfrr, jlk__xmy, xyzc__ewia,
        vdd__ewfh, prefix_code=zlj__erdi)


@numba.generated_jit(nopython=True)
def regexp_instr_util(arr, pattern, position, occurrence, option, flags, group
    ):
    verify_string_arg(arr, 'REGEXP_INSTR', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_INSTR', 'pattern')
    verify_int_arg(position, 'REGEXP_INSTR', 'position')
    verify_int_arg(occurrence, 'REGEXP_INSTR', 'occurrence')
    verify_int_arg(option, 'REGEXP_INSTR', 'option')
    verify_scalar_string_arg(flags, 'REGEXP_INSTR', 'flags')
    verify_int_arg(group, 'REGEXP_INSTR', 'group')
    fhm__jbap = ['arr', 'pattern', 'position', 'occurrence', 'option',
        'flags', 'group']
    eleby__xfrr = [arr, pattern, position, occurrence, option, flags, group]
    jlk__xmy = [True] * 7
    fgbua__vfmc = bodo.utils.typing.get_overload_const_str(pattern)
    rwyng__nbvws = posix_to_re(fgbua__vfmc)
    cwei__zmni = re.compile(fgbua__vfmc).groups
    enlv__qygrm = bodo.utils.typing.get_overload_const_str(flags)
    owx__kca = make_flag_bitvector(enlv__qygrm)
    zlj__erdi = '\n'
    xyzc__ewia = ''
    if bodo.utils.utils.is_array_typ(position, True):
        xyzc__ewia += """if arg2 <= 0: raise ValueError('REGEXP_INSTR requires a positive position')
"""
    else:
        zlj__erdi += """if position <= 0: raise ValueError('REGEXP_INSTR requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        xyzc__ewia += """if arg3 <= 0: raise ValueError('REGEXP_INSTR requires a positive occurrence')
"""
    else:
        zlj__erdi += """if occurrence <= 0: raise ValueError('REGEXP_INSTR requires a positive occurrence')
"""
    if bodo.utils.utils.is_array_typ(option, True):
        xyzc__ewia += """if arg4 != 0 and arg4 != 1: raise ValueError('REGEXP_INSTR requires option to be 0 or 1')
"""
    else:
        zlj__erdi += """if option != 0 and option != 1: raise ValueError('REGEXP_INSTR requires option to be 0 or 1')
"""
    if 'e' in enlv__qygrm:
        if bodo.utils.utils.is_array_typ(group, True):
            xyzc__ewia += f"""if not (1 <= arg6 <= {cwei__zmni}): raise ValueError('REGEXP_INSTR requires a valid group number')
"""
        else:
            zlj__erdi += f"""if not (1 <= group <= {cwei__zmni}): raise ValueError('REGEXP_INSTR requires a valid group number')
"""
    if rwyng__nbvws == '':
        xyzc__ewia += 'res[i] = 0'
    else:
        zlj__erdi += f'r = re.compile({repr(rwyng__nbvws)}, {owx__kca})'
        xyzc__ewia += 'arg0 = arg0[arg2-1:]\n'
        xyzc__ewia += 'res[i] = 0\n'
        xyzc__ewia += 'offset = arg2\n'
        xyzc__ewia += 'for j in range(arg3):\n'
        xyzc__ewia += '   match = r.search(arg0)\n'
        xyzc__ewia += '   if match is None:\n'
        xyzc__ewia += '      res[i] = 0\n'
        xyzc__ewia += '      break\n'
        xyzc__ewia += '   start, end = match.span()\n'
        xyzc__ewia += '   if j == arg3 - 1:\n'
        if 'e' in enlv__qygrm:
            xyzc__ewia += '      res[i] = offset + match.span(arg6)[arg4]\n'
        else:
            xyzc__ewia += '      res[i] = offset + match.span()[arg4]\n'
        xyzc__ewia += '   else:\n'
        xyzc__ewia += '      offset += end\n'
        xyzc__ewia += '      arg0 = arg0[end:]\n'
    vdd__ewfh = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(fhm__jbap, eleby__xfrr, jlk__xmy, xyzc__ewia,
        vdd__ewfh, prefix_code=zlj__erdi)


@numba.generated_jit(nopython=True)
def regexp_like_util(arr, pattern, flags):
    verify_string_arg(arr, 'REGEXP_LIKE', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_LIKE', 'pattern')
    verify_scalar_string_arg(flags, 'REGEXP_LIKE', 'flags')
    fhm__jbap = ['arr', 'pattern', 'flags']
    eleby__xfrr = [arr, pattern, flags]
    jlk__xmy = [True] * 3
    fgbua__vfmc = bodo.utils.typing.get_overload_const_str(pattern)
    rwyng__nbvws = posix_to_re(fgbua__vfmc)
    enlv__qygrm = bodo.utils.typing.get_overload_const_str(flags)
    owx__kca = make_flag_bitvector(enlv__qygrm)
    if rwyng__nbvws == '':
        zlj__erdi = None
        xyzc__ewia = 'res[i] = len(arg0) == 0'
    else:
        zlj__erdi = f'r = re.compile({repr(rwyng__nbvws)}, {owx__kca})'
        xyzc__ewia = 'if r.fullmatch(arg0) is None:\n'
        xyzc__ewia += '   res[i] = False\n'
        xyzc__ewia += 'else:\n'
        xyzc__ewia += '   res[i] = True\n'
    vdd__ewfh = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(fhm__jbap, eleby__xfrr, jlk__xmy, xyzc__ewia,
        vdd__ewfh, prefix_code=zlj__erdi)


@numba.generated_jit(nopython=True)
def regexp_replace_util(arr, pattern, replacement, position, occurrence, flags
    ):
    verify_string_arg(arr, 'REGEXP_REPLACE', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_REPLACE', 'pattern')
    verify_string_arg(replacement, 'REGEXP_REPLACE', 'replacement')
    verify_int_arg(position, 'REGEXP_REPLACE', 'position')
    verify_int_arg(occurrence, 'REGEXP_REPLACE', 'occurrence')
    verify_scalar_string_arg(flags, 'REGEXP_REPLACE', 'flags')
    fhm__jbap = ['arr', 'pattern', 'replacement', 'position', 'occurrence',
        'flags']
    eleby__xfrr = [arr, pattern, replacement, position, occurrence, flags]
    jlk__xmy = [True] * 6
    fgbua__vfmc = bodo.utils.typing.get_overload_const_str(pattern)
    rwyng__nbvws = posix_to_re(fgbua__vfmc)
    enlv__qygrm = bodo.utils.typing.get_overload_const_str(flags)
    owx__kca = make_flag_bitvector(enlv__qygrm)
    zlj__erdi = '\n'
    xyzc__ewia = ''
    if bodo.utils.utils.is_array_typ(position, True):
        xyzc__ewia += """if arg3 <= 0: raise ValueError('REGEXP_REPLACE requires a positive position')
"""
    else:
        zlj__erdi += """if position <= 0: raise ValueError('REGEXP_REPLACE requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        xyzc__ewia += """if arg4 < 0: raise ValueError('REGEXP_REPLACE requires a non-negative occurrence')
"""
    else:
        zlj__erdi += """if occurrence < 0: raise ValueError('REGEXP_REPLACE requires a non-negative occurrence')
"""
    if rwyng__nbvws == '':
        xyzc__ewia += 'res[i] = arg0'
    else:
        zlj__erdi += f'r = re.compile({repr(rwyng__nbvws)}, {owx__kca})'
        xyzc__ewia += 'result = arg0[:arg3-1]\n'
        xyzc__ewia += 'arg0 = arg0[arg3-1:]\n'
        xyzc__ewia += 'if arg4 == 0:\n'
        xyzc__ewia += '   res[i] = result + r.sub(arg2, arg0)\n'
        xyzc__ewia += 'else:\n'
        xyzc__ewia += '   nomatch = False\n'
        xyzc__ewia += '   for j in range(arg4 - 1):\n'
        xyzc__ewia += '      match = r.search(arg0)\n'
        xyzc__ewia += '      if match is None:\n'
        xyzc__ewia += '         res[i] = result + arg0\n'
        xyzc__ewia += '         nomatch = True\n'
        xyzc__ewia += '         break\n'
        xyzc__ewia += '      _, end = match.span()\n'
        xyzc__ewia += '      result += arg0[:end]\n'
        xyzc__ewia += '      arg0 = arg0[end:]\n'
        xyzc__ewia += '   if nomatch == False:\n'
        xyzc__ewia += '      result += r.sub(arg2, arg0, count=1)\n'
        xyzc__ewia += '      res[i] = result'
    vdd__ewfh = bodo.string_array_type
    return gen_vectorized(fhm__jbap, eleby__xfrr, jlk__xmy, xyzc__ewia,
        vdd__ewfh, prefix_code=zlj__erdi)


@numba.generated_jit(nopython=True)
def regexp_substr_util(arr, pattern, position, occurrence, flags, group):
    verify_string_arg(arr, 'REGEXP_SUBSTR', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_SUBSTR', 'pattern')
    verify_int_arg(position, 'REGEXP_SUBSTR', 'position')
    verify_int_arg(occurrence, 'REGEXP_SUBSTR', 'occurrence')
    verify_scalar_string_arg(flags, 'REGEXP_SUBSTR', 'flags')
    verify_int_arg(group, 'REGEXP_SUBSTR', 'group')
    fhm__jbap = ['arr', 'pattern', 'position', 'occurrence', 'flags', 'group']
    eleby__xfrr = [arr, pattern, position, occurrence, flags, group]
    jlk__xmy = [True] * 6
    fgbua__vfmc = bodo.utils.typing.get_overload_const_str(pattern)
    rwyng__nbvws = posix_to_re(fgbua__vfmc)
    cwei__zmni = re.compile(fgbua__vfmc).groups
    enlv__qygrm = bodo.utils.typing.get_overload_const_str(flags)
    owx__kca = make_flag_bitvector(enlv__qygrm)
    zlj__erdi = '\n'
    xyzc__ewia = ''
    if bodo.utils.utils.is_array_typ(position, True):
        xyzc__ewia += """if arg2 <= 0: raise ValueError('REGEXP_SUBSTR requires a positive position')
"""
    else:
        zlj__erdi += """if position <= 0: raise ValueError('REGEXP_SUBSTR requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        xyzc__ewia += """if arg3 <= 0: raise ValueError('REGEXP_SUBSTR requires a positive occurrence')
"""
    else:
        zlj__erdi += """if occurrence <= 0: raise ValueError('REGEXP_SUBSTR requires a positive occurrence')
"""
    if 'e' in enlv__qygrm:
        if bodo.utils.utils.is_array_typ(group, True):
            xyzc__ewia += f"""if not (1 <= arg5 <= {cwei__zmni}): raise ValueError('REGEXP_SUBSTR requires a valid group number')
"""
        else:
            zlj__erdi += f"""if not (1 <= group <= {cwei__zmni}): raise ValueError('REGEXP_SUBSTR requires a valid group number')
"""
    if rwyng__nbvws == '':
        xyzc__ewia += 'bodo.libs.array_kernels.setna(res, i)'
    else:
        zlj__erdi += f'r = re.compile({repr(rwyng__nbvws)}, {owx__kca})'
        if 'e' in enlv__qygrm:
            xyzc__ewia += 'matches = r.findall(arg0[arg2-1:])\n'
            xyzc__ewia += f'if len(matches) < arg3:\n'
            xyzc__ewia += '   bodo.libs.array_kernels.setna(res, i)\n'
            xyzc__ewia += 'else:\n'
            if cwei__zmni == 1:
                xyzc__ewia += '   res[i] = matches[arg3-1]\n'
            else:
                xyzc__ewia += '   res[i] = matches[arg3-1][arg5-1]\n'
        else:
            xyzc__ewia += 'arg0 = str(arg0)[arg2-1:]\n'
            xyzc__ewia += 'for j in range(arg3):\n'
            xyzc__ewia += '   match = r.search(arg0)\n'
            xyzc__ewia += '   if match is None:\n'
            xyzc__ewia += '      bodo.libs.array_kernels.setna(res, i)\n'
            xyzc__ewia += '      break\n'
            xyzc__ewia += '   start, end = match.span()\n'
            xyzc__ewia += '   if j == arg3 - 1:\n'
            xyzc__ewia += '      res[i] = arg0[start:end]\n'
            xyzc__ewia += '   else:\n'
            xyzc__ewia += '      arg0 = arg0[end:]\n'
    vdd__ewfh = bodo.string_array_type
    return gen_vectorized(fhm__jbap, eleby__xfrr, jlk__xmy, xyzc__ewia,
        vdd__ewfh, prefix_code=zlj__erdi)
