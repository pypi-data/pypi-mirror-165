"""
Implements regexp array kernels that are specific to BodoSQL
"""
import re
import numba
from numba.core import types
import bodo
from bodo.libs.bodosql_array_kernel_utils import *


def posix_to_re(pattern):
    jnq__thr = {'[:alnum:]': 'A-Za-z0-9', '[:alpha:]': 'A-Za-z',
        '[:ascii:]': '\x01-\x7f', '[:blank:]': ' \t', '[:cntrl:]':
        '\x01-\x1f\x7f', '[:digit:]': '0-9', '[:graph:]': '!-~',
        '[:lower:]': 'a-z', '[:print:]': ' -~', '[:punct:]':
        '\\]\\[!"#$%&\'()*+,./:;<=>?@\\^_`{|}~-', '[:space:]':
        ' \t\r\n\x0b\x0c', '[:upper:]': 'A-Z', '[:word:]': 'A-Za-z0-9_',
        '[:xdigit:]': 'A-Fa-f0-9'}
    for igs__mmqx in jnq__thr:
        pattern = pattern.replace(igs__mmqx, jnq__thr[igs__mmqx])
    return pattern


def make_flag_bitvector(flags):
    tzqe__ogkk = 0
    if 'i' in flags:
        if 'c' not in flags or flags.rindex('i') > flags.rindex('c'):
            tzqe__ogkk = tzqe__ogkk | re.I
    if 'm' in flags:
        tzqe__ogkk = tzqe__ogkk | re.M
    if 's' in flags:
        tzqe__ogkk = tzqe__ogkk | re.S
    return tzqe__ogkk


@numba.generated_jit(nopython=True)
def regexp_count(arr, pattern, position, flags):
    args = [arr, pattern, position, flags]
    for jwbl__bnhcd in range(4):
        if isinstance(args[jwbl__bnhcd], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_count', ['arr',
                'pattern', 'position', 'flags'], jwbl__bnhcd)

    def impl(arr, pattern, position, flags):
        return regexp_count_util(arr, numba.literally(pattern), position,
            numba.literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_instr(arr, pattern, position, occurrence, option, flags, group):
    args = [arr, pattern, position, occurrence, option, flags, group]
    for jwbl__bnhcd in range(7):
        if isinstance(args[jwbl__bnhcd], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_instr', ['arr',
                'pattern', 'position', 'occurrence', 'option', 'flags',
                'group'], jwbl__bnhcd)

    def impl(arr, pattern, position, occurrence, option, flags, group):
        return regexp_instr_util(arr, numba.literally(pattern), position,
            occurrence, option, numba.literally(flags), group)
    return impl


@numba.generated_jit(nopython=True)
def regexp_like(arr, pattern, flags):
    args = [arr, pattern, flags]
    for jwbl__bnhcd in range(3):
        if isinstance(args[jwbl__bnhcd], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regexp_like'
                , ['arr', 'pattern', 'flags'], jwbl__bnhcd)

    def impl(arr, pattern, flags):
        return regexp_like_util(arr, numba.literally(pattern), numba.
            literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_replace(arr, pattern, replacement, position, occurrence, flags):
    args = [arr, pattern, replacement, position, occurrence, flags]
    for jwbl__bnhcd in range(6):
        if isinstance(args[jwbl__bnhcd], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_replace', ['arr',
                'pattern', 'replacement', 'position', 'occurrence', 'flags'
                ], jwbl__bnhcd)

    def impl(arr, pattern, replacement, position, occurrence, flags):
        return regexp_replace_util(arr, numba.literally(pattern),
            replacement, position, occurrence, numba.literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_substr(arr, pattern, position, occurrence, flags, group):
    args = [arr, pattern, position, occurrence, flags, group]
    for jwbl__bnhcd in range(6):
        if isinstance(args[jwbl__bnhcd], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_substr', ['arr',
                'pattern', 'position', 'occurrence', 'flags', 'group'],
                jwbl__bnhcd)

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
    cjy__yqof = ['arr', 'pattern', 'position', 'flags']
    upsx__xefi = [arr, pattern, position, flags]
    ejnvx__mjb = [True] * 4
    zimp__ifgek = bodo.utils.typing.get_overload_const_str(pattern)
    wayo__fgm = posix_to_re(zimp__ifgek)
    cyd__nkvg = bodo.utils.typing.get_overload_const_str(flags)
    uhcjc__qtp = make_flag_bitvector(cyd__nkvg)
    ystu__zyoe = '\n'
    ycm__sqraz = ''
    if bodo.utils.utils.is_array_typ(position, True):
        ycm__sqraz += """if arg2 <= 0: raise ValueError('REGEXP_COUNT requires a positive position')
"""
    else:
        ystu__zyoe += """if position <= 0: raise ValueError('REGEXP_COUNT requires a positive position')
"""
    if wayo__fgm == '':
        ycm__sqraz += 'res[i] = 0'
    else:
        ystu__zyoe += f'r = re.compile({repr(wayo__fgm)}, {uhcjc__qtp})'
        ycm__sqraz += 'res[i] = len(r.findall(arg0[arg2-1:]))'
    iys__rvq = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(cjy__yqof, upsx__xefi, ejnvx__mjb, ycm__sqraz,
        iys__rvq, prefix_code=ystu__zyoe)


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
    cjy__yqof = ['arr', 'pattern', 'position', 'occurrence', 'option',
        'flags', 'group']
    upsx__xefi = [arr, pattern, position, occurrence, option, flags, group]
    ejnvx__mjb = [True] * 7
    zimp__ifgek = bodo.utils.typing.get_overload_const_str(pattern)
    wayo__fgm = posix_to_re(zimp__ifgek)
    pqxt__jbdu = re.compile(zimp__ifgek).groups
    cyd__nkvg = bodo.utils.typing.get_overload_const_str(flags)
    uhcjc__qtp = make_flag_bitvector(cyd__nkvg)
    ystu__zyoe = '\n'
    ycm__sqraz = ''
    if bodo.utils.utils.is_array_typ(position, True):
        ycm__sqraz += """if arg2 <= 0: raise ValueError('REGEXP_INSTR requires a positive position')
"""
    else:
        ystu__zyoe += """if position <= 0: raise ValueError('REGEXP_INSTR requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        ycm__sqraz += """if arg3 <= 0: raise ValueError('REGEXP_INSTR requires a positive occurrence')
"""
    else:
        ystu__zyoe += """if occurrence <= 0: raise ValueError('REGEXP_INSTR requires a positive occurrence')
"""
    if bodo.utils.utils.is_array_typ(option, True):
        ycm__sqraz += """if arg4 != 0 and arg4 != 1: raise ValueError('REGEXP_INSTR requires option to be 0 or 1')
"""
    else:
        ystu__zyoe += """if option != 0 and option != 1: raise ValueError('REGEXP_INSTR requires option to be 0 or 1')
"""
    if 'e' in cyd__nkvg:
        if bodo.utils.utils.is_array_typ(group, True):
            ycm__sqraz += f"""if not (1 <= arg6 <= {pqxt__jbdu}): raise ValueError('REGEXP_INSTR requires a valid group number')
"""
        else:
            ystu__zyoe += f"""if not (1 <= group <= {pqxt__jbdu}): raise ValueError('REGEXP_INSTR requires a valid group number')
"""
    if wayo__fgm == '':
        ycm__sqraz += 'res[i] = 0'
    else:
        ystu__zyoe += f'r = re.compile({repr(wayo__fgm)}, {uhcjc__qtp})'
        ycm__sqraz += 'arg0 = arg0[arg2-1:]\n'
        ycm__sqraz += 'res[i] = 0\n'
        ycm__sqraz += 'offset = arg2\n'
        ycm__sqraz += 'for j in range(arg3):\n'
        ycm__sqraz += '   match = r.search(arg0)\n'
        ycm__sqraz += '   if match is None:\n'
        ycm__sqraz += '      res[i] = 0\n'
        ycm__sqraz += '      break\n'
        ycm__sqraz += '   start, end = match.span()\n'
        ycm__sqraz += '   if j == arg3 - 1:\n'
        if 'e' in cyd__nkvg:
            ycm__sqraz += '      res[i] = offset + match.span(arg6)[arg4]\n'
        else:
            ycm__sqraz += '      res[i] = offset + match.span()[arg4]\n'
        ycm__sqraz += '   else:\n'
        ycm__sqraz += '      offset += end\n'
        ycm__sqraz += '      arg0 = arg0[end:]\n'
    iys__rvq = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(cjy__yqof, upsx__xefi, ejnvx__mjb, ycm__sqraz,
        iys__rvq, prefix_code=ystu__zyoe)


@numba.generated_jit(nopython=True)
def regexp_like_util(arr, pattern, flags):
    verify_string_arg(arr, 'REGEXP_LIKE', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_LIKE', 'pattern')
    verify_scalar_string_arg(flags, 'REGEXP_LIKE', 'flags')
    cjy__yqof = ['arr', 'pattern', 'flags']
    upsx__xefi = [arr, pattern, flags]
    ejnvx__mjb = [True] * 3
    zimp__ifgek = bodo.utils.typing.get_overload_const_str(pattern)
    wayo__fgm = posix_to_re(zimp__ifgek)
    cyd__nkvg = bodo.utils.typing.get_overload_const_str(flags)
    uhcjc__qtp = make_flag_bitvector(cyd__nkvg)
    if wayo__fgm == '':
        ystu__zyoe = None
        ycm__sqraz = 'res[i] = len(arg0) == 0'
    else:
        ystu__zyoe = f'r = re.compile({repr(wayo__fgm)}, {uhcjc__qtp})'
        ycm__sqraz = 'if r.fullmatch(arg0) is None:\n'
        ycm__sqraz += '   res[i] = False\n'
        ycm__sqraz += 'else:\n'
        ycm__sqraz += '   res[i] = True\n'
    iys__rvq = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(cjy__yqof, upsx__xefi, ejnvx__mjb, ycm__sqraz,
        iys__rvq, prefix_code=ystu__zyoe)


@numba.generated_jit(nopython=True)
def regexp_replace_util(arr, pattern, replacement, position, occurrence, flags
    ):
    verify_string_arg(arr, 'REGEXP_REPLACE', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_REPLACE', 'pattern')
    verify_string_arg(replacement, 'REGEXP_REPLACE', 'replacement')
    verify_int_arg(position, 'REGEXP_REPLACE', 'position')
    verify_int_arg(occurrence, 'REGEXP_REPLACE', 'occurrence')
    verify_scalar_string_arg(flags, 'REGEXP_REPLACE', 'flags')
    cjy__yqof = ['arr', 'pattern', 'replacement', 'position', 'occurrence',
        'flags']
    upsx__xefi = [arr, pattern, replacement, position, occurrence, flags]
    ejnvx__mjb = [True] * 6
    zimp__ifgek = bodo.utils.typing.get_overload_const_str(pattern)
    wayo__fgm = posix_to_re(zimp__ifgek)
    cyd__nkvg = bodo.utils.typing.get_overload_const_str(flags)
    uhcjc__qtp = make_flag_bitvector(cyd__nkvg)
    ystu__zyoe = '\n'
    ycm__sqraz = ''
    if bodo.utils.utils.is_array_typ(position, True):
        ycm__sqraz += """if arg3 <= 0: raise ValueError('REGEXP_REPLACE requires a positive position')
"""
    else:
        ystu__zyoe += """if position <= 0: raise ValueError('REGEXP_REPLACE requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        ycm__sqraz += """if arg4 < 0: raise ValueError('REGEXP_REPLACE requires a non-negative occurrence')
"""
    else:
        ystu__zyoe += """if occurrence < 0: raise ValueError('REGEXP_REPLACE requires a non-negative occurrence')
"""
    if wayo__fgm == '':
        ycm__sqraz += 'res[i] = arg0'
    else:
        ystu__zyoe += f'r = re.compile({repr(wayo__fgm)}, {uhcjc__qtp})'
        ycm__sqraz += 'result = arg0[:arg3-1]\n'
        ycm__sqraz += 'arg0 = arg0[arg3-1:]\n'
        ycm__sqraz += 'if arg4 == 0:\n'
        ycm__sqraz += '   res[i] = result + r.sub(arg2, arg0)\n'
        ycm__sqraz += 'else:\n'
        ycm__sqraz += '   nomatch = False\n'
        ycm__sqraz += '   for j in range(arg4 - 1):\n'
        ycm__sqraz += '      match = r.search(arg0)\n'
        ycm__sqraz += '      if match is None:\n'
        ycm__sqraz += '         res[i] = result + arg0\n'
        ycm__sqraz += '         nomatch = True\n'
        ycm__sqraz += '         break\n'
        ycm__sqraz += '      _, end = match.span()\n'
        ycm__sqraz += '      result += arg0[:end]\n'
        ycm__sqraz += '      arg0 = arg0[end:]\n'
        ycm__sqraz += '   if nomatch == False:\n'
        ycm__sqraz += '      result += r.sub(arg2, arg0, count=1)\n'
        ycm__sqraz += '      res[i] = result'
    iys__rvq = bodo.string_array_type
    return gen_vectorized(cjy__yqof, upsx__xefi, ejnvx__mjb, ycm__sqraz,
        iys__rvq, prefix_code=ystu__zyoe)


@numba.generated_jit(nopython=True)
def regexp_substr_util(arr, pattern, position, occurrence, flags, group):
    verify_string_arg(arr, 'REGEXP_SUBSTR', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_SUBSTR', 'pattern')
    verify_int_arg(position, 'REGEXP_SUBSTR', 'position')
    verify_int_arg(occurrence, 'REGEXP_SUBSTR', 'occurrence')
    verify_scalar_string_arg(flags, 'REGEXP_SUBSTR', 'flags')
    verify_int_arg(group, 'REGEXP_SUBSTR', 'group')
    cjy__yqof = ['arr', 'pattern', 'position', 'occurrence', 'flags', 'group']
    upsx__xefi = [arr, pattern, position, occurrence, flags, group]
    ejnvx__mjb = [True] * 6
    zimp__ifgek = bodo.utils.typing.get_overload_const_str(pattern)
    wayo__fgm = posix_to_re(zimp__ifgek)
    pqxt__jbdu = re.compile(zimp__ifgek).groups
    cyd__nkvg = bodo.utils.typing.get_overload_const_str(flags)
    uhcjc__qtp = make_flag_bitvector(cyd__nkvg)
    ystu__zyoe = '\n'
    ycm__sqraz = ''
    if bodo.utils.utils.is_array_typ(position, True):
        ycm__sqraz += """if arg2 <= 0: raise ValueError('REGEXP_SUBSTR requires a positive position')
"""
    else:
        ystu__zyoe += """if position <= 0: raise ValueError('REGEXP_SUBSTR requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        ycm__sqraz += """if arg3 <= 0: raise ValueError('REGEXP_SUBSTR requires a positive occurrence')
"""
    else:
        ystu__zyoe += """if occurrence <= 0: raise ValueError('REGEXP_SUBSTR requires a positive occurrence')
"""
    if 'e' in cyd__nkvg:
        if bodo.utils.utils.is_array_typ(group, True):
            ycm__sqraz += f"""if not (1 <= arg5 <= {pqxt__jbdu}): raise ValueError('REGEXP_SUBSTR requires a valid group number')
"""
        else:
            ystu__zyoe += f"""if not (1 <= group <= {pqxt__jbdu}): raise ValueError('REGEXP_SUBSTR requires a valid group number')
"""
    if wayo__fgm == '':
        ycm__sqraz += 'bodo.libs.array_kernels.setna(res, i)'
    else:
        ystu__zyoe += f'r = re.compile({repr(wayo__fgm)}, {uhcjc__qtp})'
        if 'e' in cyd__nkvg:
            ycm__sqraz += 'matches = r.findall(arg0[arg2-1:])\n'
            ycm__sqraz += f'if len(matches) < arg3:\n'
            ycm__sqraz += '   bodo.libs.array_kernels.setna(res, i)\n'
            ycm__sqraz += 'else:\n'
            if pqxt__jbdu == 1:
                ycm__sqraz += '   res[i] = matches[arg3-1]\n'
            else:
                ycm__sqraz += '   res[i] = matches[arg3-1][arg5-1]\n'
        else:
            ycm__sqraz += 'arg0 = str(arg0)[arg2-1:]\n'
            ycm__sqraz += 'for j in range(arg3):\n'
            ycm__sqraz += '   match = r.search(arg0)\n'
            ycm__sqraz += '   if match is None:\n'
            ycm__sqraz += '      bodo.libs.array_kernels.setna(res, i)\n'
            ycm__sqraz += '      break\n'
            ycm__sqraz += '   start, end = match.span()\n'
            ycm__sqraz += '   if j == arg3 - 1:\n'
            ycm__sqraz += '      res[i] = arg0[start:end]\n'
            ycm__sqraz += '   else:\n'
            ycm__sqraz += '      arg0 = arg0[end:]\n'
    iys__rvq = bodo.string_array_type
    return gen_vectorized(cjy__yqof, upsx__xefi, ejnvx__mjb, ycm__sqraz,
        iys__rvq, prefix_code=ystu__zyoe)
