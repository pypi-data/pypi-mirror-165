"""
Implements string array kernels that are specific to BodoSQL
"""
import numba
import numpy as np
from numba.core import types
from numba.extending import overload, register_jitable
import bodo
from bodo.libs.bodosql_array_kernel_utils import *


@numba.generated_jit(nopython=True)
def char(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.char_util',
            ['arr'], 0)

    def impl(arr):
        return char_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def editdistance_no_max(s, t):
    args = [s, t]
    for mhukf__xfzl in range(2):
        if isinstance(args[mhukf__xfzl], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.editdistance_no_max', ['s',
                't'], mhukf__xfzl)

    def impl(s, t):
        return editdistance_no_max_util(s, t)
    return impl


@numba.generated_jit(nopython=True)
def editdistance_with_max(s, t, maxDistance):
    args = [s, t, maxDistance]
    for mhukf__xfzl in range(3):
        if isinstance(args[mhukf__xfzl], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.editdistance_with_max', [
                's', 't', 'maxDistance'], mhukf__xfzl)

    def impl(s, t, maxDistance):
        return editdistance_with_max_util(s, t, maxDistance)
    return impl


@numba.generated_jit(nopython=True)
def format(arr, places):
    args = [arr, places]
    for mhukf__xfzl in range(2):
        if isinstance(args[mhukf__xfzl], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.format',
                ['arr', 'places'], mhukf__xfzl)

    def impl(arr, places):
        return format_util(arr, places)
    return impl


@numba.generated_jit(nopython=True)
def initcap(arr, delim):
    args = [arr, delim]
    for mhukf__xfzl in range(2):
        if isinstance(args[mhukf__xfzl], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.initcap',
                ['arr', 'delim'], mhukf__xfzl)

    def impl(arr, delim):
        return initcap_util(arr, delim)
    return impl


@numba.generated_jit(nopython=True)
def instr(arr, target):
    args = [arr, target]
    for mhukf__xfzl in range(2):
        if isinstance(args[mhukf__xfzl], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.instr',
                ['arr', 'target'], mhukf__xfzl)

    def impl(arr, target):
        return instr_util(arr, target)
    return impl


def left(arr, n_chars):
    return


@overload(left)
def overload_left(arr, n_chars):
    args = [arr, n_chars]
    for mhukf__xfzl in range(2):
        if isinstance(args[mhukf__xfzl], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.left', [
                'arr', 'n_chars'], mhukf__xfzl)

    def impl(arr, n_chars):
        return left_util(arr, n_chars)
    return impl


def lpad(arr, length, padstr):
    return


@overload(lpad)
def overload_lpad(arr, length, padstr):
    args = [arr, length, padstr]
    for mhukf__xfzl in range(3):
        if isinstance(args[mhukf__xfzl], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.lpad', [
                'arr', 'length', 'padstr'], mhukf__xfzl)

    def impl(arr, length, padstr):
        return lpad_util(arr, length, padstr)
    return impl


@numba.generated_jit(nopython=True)
def ord_ascii(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.ord_ascii_util',
            ['arr'], 0)

    def impl(arr):
        return ord_ascii_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def repeat(arr, repeats):
    args = [arr, repeats]
    for mhukf__xfzl in range(2):
        if isinstance(args[mhukf__xfzl], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.repeat',
                ['arr', 'repeats'], mhukf__xfzl)

    def impl(arr, repeats):
        return repeat_util(arr, repeats)
    return impl


@numba.generated_jit(nopython=True)
def replace(arr, to_replace, replace_with):
    args = [arr, to_replace, replace_with]
    for mhukf__xfzl in range(3):
        if isinstance(args[mhukf__xfzl], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.replace',
                ['arr', 'to_replace', 'replace_with'], mhukf__xfzl)

    def impl(arr, to_replace, replace_with):
        return replace_util(arr, to_replace, replace_with)
    return impl


@numba.generated_jit(nopython=True)
def reverse(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.reverse_util',
            ['arr'], 0)

    def impl(arr):
        return reverse_util(arr)
    return impl


def right(arr, n_chars):
    return


@overload(right)
def overload_right(arr, n_chars):
    args = [arr, n_chars]
    for mhukf__xfzl in range(2):
        if isinstance(args[mhukf__xfzl], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.right',
                ['arr', 'n_chars'], mhukf__xfzl)

    def impl(arr, n_chars):
        return right_util(arr, n_chars)
    return impl


def rpad(arr, length, padstr):
    return


@overload(rpad)
def overload_rpad(arr, length, padstr):
    args = [arr, length, padstr]
    for mhukf__xfzl in range(3):
        if isinstance(args[mhukf__xfzl], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.rpad', [
                'arr', 'length', 'padstr'], mhukf__xfzl)

    def impl(arr, length, padstr):
        return rpad_util(arr, length, padstr)
    return impl


@numba.generated_jit(nopython=True)
def space(n_chars):
    if isinstance(n_chars, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.space_util',
            ['n_chars'], 0)

    def impl(n_chars):
        return space_util(n_chars)
    return impl


@numba.generated_jit(nopython=True)
def split_part(source, delim, part):
    args = [source, delim, part]
    for mhukf__xfzl in range(3):
        if isinstance(args[mhukf__xfzl], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.split_part',
                ['source', 'delim', 'part'], mhukf__xfzl)

    def impl(source, delim, part):
        return split_part_util(source, delim, part)
    return impl


@numba.generated_jit(nopython=True)
def strcmp(arr0, arr1):
    args = [arr0, arr1]
    for mhukf__xfzl in range(2):
        if isinstance(args[mhukf__xfzl], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.strcmp',
                ['arr0', 'arr1'], mhukf__xfzl)

    def impl(arr0, arr1):
        return strcmp_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def strtok(source, delim, part):
    args = [source, delim, part]
    for mhukf__xfzl in range(3):
        if isinstance(args[mhukf__xfzl], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.strtok',
                ['source', 'delim', 'part'], mhukf__xfzl)

    def impl(source, delim, part):
        return strtok_util(source, delim, part)
    return impl


@numba.generated_jit(nopython=True)
def substring(arr, start, length):
    args = [arr, start, length]
    for mhukf__xfzl in range(3):
        if isinstance(args[mhukf__xfzl], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.substring',
                ['arr', 'start', 'length'], mhukf__xfzl)

    def impl(arr, start, length):
        return substring_util(arr, start, length)
    return impl


@numba.generated_jit(nopython=True)
def substring_index(arr, delimiter, occurrences):
    args = [arr, delimiter, occurrences]
    for mhukf__xfzl in range(3):
        if isinstance(args[mhukf__xfzl], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.substring_index', ['arr',
                'delimiter', 'occurrences'], mhukf__xfzl)

    def impl(arr, delimiter, occurrences):
        return substring_index_util(arr, delimiter, occurrences)
    return impl


@numba.generated_jit(nopython=True)
def translate(arr, source, target):
    args = [arr, source, target]
    for mhukf__xfzl in range(3):
        if isinstance(args[mhukf__xfzl], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.translate',
                ['arr', 'source', 'target'], mhukf__xfzl)

    def impl(arr, source, target):
        return translate_util(arr, source, target)
    return impl


@numba.generated_jit(nopython=True)
def char_util(arr):
    verify_int_arg(arr, 'CHAR', 'arr')
    nfirb__sua = ['arr']
    xtanw__zzoc = [arr]
    scsmb__lns = [True]
    cye__unxp = 'if 0 <= arg0 <= 127:\n'
    cye__unxp += '   res[i] = chr(arg0)\n'
    cye__unxp += 'else:\n'
    cye__unxp += '   bodo.libs.array_kernels.setna(res, i)\n'
    bbr__arb = bodo.string_array_type
    return gen_vectorized(nfirb__sua, xtanw__zzoc, scsmb__lns, cye__unxp,
        bbr__arb)


@numba.generated_jit(nopython=True)
def initcap_util(arr, delim):
    verify_string_arg(arr, 'INITCAP', 'arr')
    verify_string_arg(delim, 'INITCAP', 'delim')
    nfirb__sua = ['arr', 'delim']
    xtanw__zzoc = [arr, delim]
    scsmb__lns = [True] * 2
    cye__unxp = 'capitalized = arg0[:1].upper()\n'
    cye__unxp += 'for j in range(1, len(arg0)):\n'
    cye__unxp += '   if arg0[j-1] in arg1:\n'
    cye__unxp += '      capitalized += arg0[j].upper()\n'
    cye__unxp += '   else:\n'
    cye__unxp += '      capitalized += arg0[j].lower()\n'
    cye__unxp += 'res[i] = capitalized'
    bbr__arb = bodo.string_array_type
    return gen_vectorized(nfirb__sua, xtanw__zzoc, scsmb__lns, cye__unxp,
        bbr__arb)


@numba.generated_jit(nopython=True)
def instr_util(arr, target):
    verify_string_arg(arr, 'instr', 'arr')
    verify_string_arg(target, 'instr', 'target')
    nfirb__sua = ['arr', 'target']
    xtanw__zzoc = [arr, target]
    scsmb__lns = [True] * 2
    cye__unxp = 'res[i] = arg0.find(arg1) + 1'
    bbr__arb = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(nfirb__sua, xtanw__zzoc, scsmb__lns, cye__unxp,
        bbr__arb)


@register_jitable
def min_edit_distance(s, t):
    if len(s) > len(t):
        s, t = t, s
    nya__rehpd, hpus__lmg = len(s), len(t)
    ykn__tkqhq, aoqx__jyahz = 1, 0
    arr = np.zeros((2, nya__rehpd + 1), dtype=np.uint32)
    arr[0, :] = np.arange(nya__rehpd + 1)
    for mhukf__xfzl in range(1, hpus__lmg + 1):
        arr[ykn__tkqhq, 0] = mhukf__xfzl
        for fdzo__xmjm in range(1, nya__rehpd + 1):
            if s[fdzo__xmjm - 1] == t[mhukf__xfzl - 1]:
                arr[ykn__tkqhq, fdzo__xmjm] = arr[aoqx__jyahz, fdzo__xmjm - 1]
            else:
                arr[ykn__tkqhq, fdzo__xmjm] = 1 + min(arr[ykn__tkqhq, 
                    fdzo__xmjm - 1], arr[aoqx__jyahz, fdzo__xmjm], arr[
                    aoqx__jyahz, fdzo__xmjm - 1])
        ykn__tkqhq, aoqx__jyahz = aoqx__jyahz, ykn__tkqhq
    return arr[hpus__lmg % 2, nya__rehpd]


@register_jitable
def min_edit_distance_with_max(s, t, maxDistance):
    if maxDistance < 0:
        return 0
    if len(s) > len(t):
        s, t = t, s
    nya__rehpd, hpus__lmg = len(s), len(t)
    if nya__rehpd <= maxDistance and hpus__lmg <= maxDistance:
        return min_edit_distance(s, t)
    ykn__tkqhq, aoqx__jyahz = 1, 0
    arr = np.zeros((2, nya__rehpd + 1), dtype=np.uint32)
    arr[0, :] = np.arange(nya__rehpd + 1)
    for mhukf__xfzl in range(1, hpus__lmg + 1):
        arr[ykn__tkqhq, 0] = mhukf__xfzl
        for fdzo__xmjm in range(1, nya__rehpd + 1):
            if s[fdzo__xmjm - 1] == t[mhukf__xfzl - 1]:
                arr[ykn__tkqhq, fdzo__xmjm] = arr[aoqx__jyahz, fdzo__xmjm - 1]
            else:
                arr[ykn__tkqhq, fdzo__xmjm] = 1 + min(arr[ykn__tkqhq, 
                    fdzo__xmjm - 1], arr[aoqx__jyahz, fdzo__xmjm], arr[
                    aoqx__jyahz, fdzo__xmjm - 1])
        if (arr[ykn__tkqhq] >= maxDistance).all():
            return maxDistance
        ykn__tkqhq, aoqx__jyahz = aoqx__jyahz, ykn__tkqhq
    return min(arr[hpus__lmg % 2, nya__rehpd], maxDistance)


@numba.generated_jit(nopython=True)
def editdistance_no_max_util(s, t):
    verify_string_arg(s, 'editdistance_no_max', 's')
    verify_string_arg(t, 'editdistance_no_max', 't')
    nfirb__sua = ['s', 't']
    xtanw__zzoc = [s, t]
    scsmb__lns = [True] * 2
    cye__unxp = (
        'res[i] = bodo.libs.bodosql_array_kernels.min_edit_distance(arg0, arg1)'
        )
    bbr__arb = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(nfirb__sua, xtanw__zzoc, scsmb__lns, cye__unxp,
        bbr__arb)


@numba.generated_jit(nopython=True)
def editdistance_with_max_util(s, t, maxDistance):
    verify_string_arg(s, 'editdistance_no_max', 's')
    verify_string_arg(t, 'editdistance_no_max', 't')
    verify_int_arg(maxDistance, 'editdistance_no_max', 't')
    nfirb__sua = ['s', 't', 'maxDistance']
    xtanw__zzoc = [s, t, maxDistance]
    scsmb__lns = [True] * 3
    cye__unxp = (
        'res[i] = bodo.libs.bodosql_array_kernels.min_edit_distance_with_max(arg0, arg1, arg2)'
        )
    bbr__arb = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(nfirb__sua, xtanw__zzoc, scsmb__lns, cye__unxp,
        bbr__arb)


@numba.generated_jit(nopython=True)
def format_util(arr, places):
    verify_int_float_arg(arr, 'FORMAT', 'arr')
    verify_int_arg(places, 'FORMAT', 'places')
    nfirb__sua = ['arr', 'places']
    xtanw__zzoc = [arr, places]
    scsmb__lns = [True] * 2
    cye__unxp = 'prec = max(arg1, 0)\n'
    cye__unxp += "res[i] = format(arg0, f',.{prec}f')"
    bbr__arb = bodo.string_array_type
    return gen_vectorized(nfirb__sua, xtanw__zzoc, scsmb__lns, cye__unxp,
        bbr__arb)


def left_util(arr, n_chars):
    return


def right_util(arr, n_chars):
    return


def create_left_right_util_overload(func_name):

    def overload_left_right_util(arr, n_chars):
        zzebx__pco = verify_string_binary_arg(arr, func_name, 'arr')
        verify_int_arg(n_chars, func_name, 'n_chars')
        nsp__vbk = "''" if zzebx__pco else "b''"
        nfirb__sua = ['arr', 'n_chars']
        xtanw__zzoc = [arr, n_chars]
        scsmb__lns = [True] * 2
        cye__unxp = 'if arg1 <= 0:\n'
        cye__unxp += f'   res[i] = {nsp__vbk}\n'
        cye__unxp += 'else:\n'
        if func_name == 'LEFT':
            cye__unxp += '   res[i] = arg0[:arg1]'
        elif func_name == 'RIGHT':
            cye__unxp += '   res[i] = arg0[-arg1:]'
        bbr__arb = (bodo.string_array_type if zzebx__pco else bodo.
            binary_array_type)
        return gen_vectorized(nfirb__sua, xtanw__zzoc, scsmb__lns,
            cye__unxp, bbr__arb)
    return overload_left_right_util


def _install_left_right_overload():
    for qga__teihe, func_name in zip((left_util, right_util), ('LEFT', 'RIGHT')
        ):
        ygosa__qlby = create_left_right_util_overload(func_name)
        overload(qga__teihe)(ygosa__qlby)


_install_left_right_overload()


def lpad_util(arr, length, padstr):
    return


def rpad_util(arr, length, padstr):
    return


def create_lpad_rpad_util_overload(func_name):

    def overload_lpad_rpad_util(arr, length, pad_string):
        nkh__kcm = verify_string_binary_arg(pad_string, func_name, 'pad_string'
            )
        zzebx__pco = verify_string_binary_arg(arr, func_name, 'arr')
        if zzebx__pco != nkh__kcm:
            raise bodo.utils.typing.BodoError(
                'Pad string and arr must be the same type!')
        bbr__arb = (bodo.string_array_type if zzebx__pco else bodo.
            binary_array_type)
        verify_int_arg(length, func_name, 'length')
        verify_string_binary_arg(pad_string, func_name,
            f'{func_name.lower()}_string')
        if func_name == 'LPAD':
            znjzr__tufb = f'(arg2 * quotient) + arg2[:remainder] + arg0'
        elif func_name == 'RPAD':
            znjzr__tufb = f'arg0 + (arg2 * quotient) + arg2[:remainder]'
        nfirb__sua = ['arr', 'length', 'pad_string']
        xtanw__zzoc = [arr, length, pad_string]
        scsmb__lns = [True] * 3
        nsp__vbk = "''" if zzebx__pco else "b''"
        cye__unxp = f"""                if arg1 <= 0:
                    res[i] = {nsp__vbk}
                elif len(arg2) == 0:
                    res[i] = arg0
                elif len(arg0) >= arg1:
                    res[i] = arg0[:arg1]
                else:
                    quotient = (arg1 - len(arg0)) // len(arg2)
                    remainder = (arg1 - len(arg0)) % len(arg2)
                    res[i] = {znjzr__tufb}"""
        return gen_vectorized(nfirb__sua, xtanw__zzoc, scsmb__lns,
            cye__unxp, bbr__arb)
    return overload_lpad_rpad_util


def _install_lpad_rpad_overload():
    for qga__teihe, func_name in zip((lpad_util, rpad_util), ('LPAD', 'RPAD')):
        ygosa__qlby = create_lpad_rpad_util_overload(func_name)
        overload(qga__teihe)(ygosa__qlby)


_install_lpad_rpad_overload()


@numba.generated_jit(nopython=True)
def ord_ascii_util(arr):
    verify_string_arg(arr, 'ORD', 'arr')
    nfirb__sua = ['arr']
    xtanw__zzoc = [arr]
    scsmb__lns = [True]
    cye__unxp = 'if len(arg0) == 0:\n'
    cye__unxp += '   bodo.libs.array_kernels.setna(res, i)\n'
    cye__unxp += 'else:\n'
    cye__unxp += '   res[i] = ord(arg0[0])'
    bbr__arb = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(nfirb__sua, xtanw__zzoc, scsmb__lns, cye__unxp,
        bbr__arb)


@numba.generated_jit(nopython=True)
def repeat_util(arr, repeats):
    verify_string_arg(arr, 'REPEAT', 'arr')
    verify_int_arg(repeats, 'REPEAT', 'repeats')
    nfirb__sua = ['arr', 'repeats']
    xtanw__zzoc = [arr, repeats]
    scsmb__lns = [True] * 2
    cye__unxp = 'if arg1 <= 0:\n'
    cye__unxp += "   res[i] = ''\n"
    cye__unxp += 'else:\n'
    cye__unxp += '   res[i] = arg0 * arg1'
    bbr__arb = bodo.string_array_type
    return gen_vectorized(nfirb__sua, xtanw__zzoc, scsmb__lns, cye__unxp,
        bbr__arb)


@numba.generated_jit(nopython=True)
def replace_util(arr, to_replace, replace_with):
    verify_string_arg(arr, 'REPLACE', 'arr')
    verify_string_arg(to_replace, 'REPLACE', 'to_replace')
    verify_string_arg(replace_with, 'REPLACE', 'replace_with')
    nfirb__sua = ['arr', 'to_replace', 'replace_with']
    xtanw__zzoc = [arr, to_replace, replace_with]
    scsmb__lns = [True] * 3
    cye__unxp = "if arg1 == '':\n"
    cye__unxp += '   res[i] = arg0\n'
    cye__unxp += 'else:\n'
    cye__unxp += '   res[i] = arg0.replace(arg1, arg2)'
    bbr__arb = bodo.string_array_type
    return gen_vectorized(nfirb__sua, xtanw__zzoc, scsmb__lns, cye__unxp,
        bbr__arb)


@numba.generated_jit(nopython=True)
def reverse_util(arr):
    zzebx__pco = verify_string_binary_arg(arr, 'REVERSE', 'arr')
    nfirb__sua = ['arr']
    xtanw__zzoc = [arr]
    scsmb__lns = [True]
    cye__unxp = 'res[i] = arg0[::-1]'
    bbr__arb = bodo.string_array_type
    bbr__arb = bodo.string_array_type if zzebx__pco else bodo.binary_array_type
    return gen_vectorized(nfirb__sua, xtanw__zzoc, scsmb__lns, cye__unxp,
        bbr__arb)


@numba.generated_jit(nopython=True)
def space_util(n_chars):
    verify_int_arg(n_chars, 'SPACE', 'n_chars')
    nfirb__sua = ['n_chars']
    xtanw__zzoc = [n_chars]
    scsmb__lns = [True]
    cye__unxp = 'if arg0 <= 0:\n'
    cye__unxp += "   res[i] = ''\n"
    cye__unxp += 'else:\n'
    cye__unxp += "   res[i] = ' ' * arg0"
    bbr__arb = bodo.string_array_type
    return gen_vectorized(nfirb__sua, xtanw__zzoc, scsmb__lns, cye__unxp,
        bbr__arb)


@numba.generated_jit(nopython=True)
def split_part_util(source, delim, part):
    verify_string_arg(source, 'SPLIT_PART', 'source')
    verify_string_arg(delim, 'SPLIT_PART', 'delim')
    verify_int_arg(part, 'SPLIT_PART', 'part')
    nfirb__sua = ['source', 'delim', 'part']
    xtanw__zzoc = [source, delim, part]
    scsmb__lns = [True] * 3
    cye__unxp = "tokens = arg0.split(arg1) if arg1 != '' else [arg0]\n"
    cye__unxp += 'if abs(arg2) > len(tokens):\n'
    cye__unxp += "    res[i] = ''\n"
    cye__unxp += 'else:\n'
    cye__unxp += '    res[i] = tokens[arg2 if arg2 <= 0 else arg2-1]\n'
    bbr__arb = bodo.string_array_type
    return gen_vectorized(nfirb__sua, xtanw__zzoc, scsmb__lns, cye__unxp,
        bbr__arb)


@numba.generated_jit(nopython=True)
def strcmp_util(arr0, arr1):
    verify_string_arg(arr0, 'strcmp', 'arr0')
    verify_string_arg(arr1, 'strcmp', 'arr1')
    nfirb__sua = ['arr0', 'arr1']
    xtanw__zzoc = [arr0, arr1]
    scsmb__lns = [True] * 2
    cye__unxp = 'if arg0 < arg1:\n'
    cye__unxp += '   res[i] = -1\n'
    cye__unxp += 'elif arg0 > arg1:\n'
    cye__unxp += '   res[i] = 1\n'
    cye__unxp += 'else:\n'
    cye__unxp += '   res[i] = 0\n'
    bbr__arb = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(nfirb__sua, xtanw__zzoc, scsmb__lns, cye__unxp,
        bbr__arb)


@numba.generated_jit(nopython=True)
def strtok_util(source, delim, part):
    verify_string_arg(source, 'STRTOK', 'source')
    verify_string_arg(delim, 'STRTOK', 'delim')
    verify_int_arg(part, 'STRTOK', 'part')
    nfirb__sua = ['source', 'delim', 'part']
    xtanw__zzoc = [source, delim, part]
    scsmb__lns = [True] * 3
    cye__unxp = "if (arg0 == '' and arg1 == '') or arg2 <= 0:\n"
    cye__unxp += '   bodo.libs.array_kernels.setna(res, i)\n'
    cye__unxp += 'else:\n'
    cye__unxp += '   tokens = []\n'
    cye__unxp += "   buffer = ''\n"
    cye__unxp += '   for j in range(len(arg0)):\n'
    cye__unxp += '      if arg0[j] in arg1:\n'
    cye__unxp += "         if buffer != '':"
    cye__unxp += '            tokens.append(buffer)\n'
    cye__unxp += "         buffer = ''\n"
    cye__unxp += '      else:\n'
    cye__unxp += '         buffer += arg0[j]\n'
    cye__unxp += "   if buffer != '':\n"
    cye__unxp += '      tokens.append(buffer)\n'
    cye__unxp += '   if arg2 > len(tokens):\n'
    cye__unxp += '      bodo.libs.array_kernels.setna(res, i)\n'
    cye__unxp += '   else:\n'
    cye__unxp += '      res[i] = tokens[arg2-1]\n'
    bbr__arb = bodo.string_array_type
    return gen_vectorized(nfirb__sua, xtanw__zzoc, scsmb__lns, cye__unxp,
        bbr__arb)


@numba.generated_jit(nopython=True)
def substring_util(arr, start, length):
    zzebx__pco = verify_string_binary_arg(arr, 'SUBSTRING', 'arr')
    verify_int_arg(start, 'SUBSTRING', 'start')
    verify_int_arg(length, 'SUBSTRING', 'length')
    bbr__arb = bodo.string_array_type if zzebx__pco else bodo.binary_array_type
    nfirb__sua = ['arr', 'start', 'length']
    xtanw__zzoc = [arr, start, length]
    scsmb__lns = [True] * 3
    cye__unxp = 'if arg2 <= 0:\n'
    cye__unxp += "   res[i] = ''\n" if zzebx__pco else "   res[i] = b''\n"
    cye__unxp += 'elif arg1 < 0 and arg1 + arg2 >= 0:\n'
    cye__unxp += '   res[i] = arg0[arg1:]\n'
    cye__unxp += 'else:\n'
    cye__unxp += '   if arg1 > 0: arg1 -= 1\n'
    cye__unxp += '   res[i] = arg0[arg1:arg1+arg2]\n'
    return gen_vectorized(nfirb__sua, xtanw__zzoc, scsmb__lns, cye__unxp,
        bbr__arb)


@numba.generated_jit(nopython=True)
def substring_index_util(arr, delimiter, occurrences):
    verify_string_arg(arr, 'SUBSTRING_INDEX', 'arr')
    verify_string_arg(delimiter, 'SUBSTRING_INDEX', 'delimiter')
    verify_int_arg(occurrences, 'SUBSTRING_INDEX', 'occurrences')
    nfirb__sua = ['arr', 'delimiter', 'occurrences']
    xtanw__zzoc = [arr, delimiter, occurrences]
    scsmb__lns = [True] * 3
    cye__unxp = "if arg1 == '' or arg2 == 0:\n"
    cye__unxp += "   res[i] = ''\n"
    cye__unxp += 'elif arg2 >= 0:\n'
    cye__unxp += '   res[i] = arg1.join(arg0.split(arg1, arg2+1)[:arg2])\n'
    cye__unxp += 'else:\n'
    cye__unxp += '   res[i] = arg1.join(arg0.split(arg1)[arg2:])\n'
    bbr__arb = bodo.string_array_type
    return gen_vectorized(nfirb__sua, xtanw__zzoc, scsmb__lns, cye__unxp,
        bbr__arb)


@numba.generated_jit(nopython=True)
def translate_util(arr, source, target):
    verify_string_arg(arr, 'translate', 'arr')
    verify_string_arg(source, 'translate', 'source')
    verify_string_arg(target, 'translate', 'target')
    nfirb__sua = ['arr', 'source', 'target']
    xtanw__zzoc = [arr, source, target]
    scsmb__lns = [True] * 3
    cye__unxp = "translated = ''\n"
    cye__unxp += 'for char in arg0:\n'
    cye__unxp += '   index = arg1.find(char)\n'
    cye__unxp += '   if index == -1:\n'
    cye__unxp += '      translated += char\n'
    cye__unxp += '   elif index < len(arg2):\n'
    cye__unxp += '      translated += arg2[index]\n'
    cye__unxp += 'res[i] = translated'
    bbr__arb = bodo.string_array_type
    return gen_vectorized(nfirb__sua, xtanw__zzoc, scsmb__lns, cye__unxp,
        bbr__arb)
