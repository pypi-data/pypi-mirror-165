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
    for kqa__hgw in range(2):
        if isinstance(args[kqa__hgw], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.editdistance_no_max', ['s',
                't'], kqa__hgw)

    def impl(s, t):
        return editdistance_no_max_util(s, t)
    return impl


@numba.generated_jit(nopython=True)
def editdistance_with_max(s, t, maxDistance):
    args = [s, t, maxDistance]
    for kqa__hgw in range(3):
        if isinstance(args[kqa__hgw], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.editdistance_with_max', [
                's', 't', 'maxDistance'], kqa__hgw)

    def impl(s, t, maxDistance):
        return editdistance_with_max_util(s, t, maxDistance)
    return impl


@numba.generated_jit(nopython=True)
def format(arr, places):
    args = [arr, places]
    for kqa__hgw in range(2):
        if isinstance(args[kqa__hgw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.format',
                ['arr', 'places'], kqa__hgw)

    def impl(arr, places):
        return format_util(arr, places)
    return impl


@numba.generated_jit(nopython=True)
def initcap(arr, delim):
    args = [arr, delim]
    for kqa__hgw in range(2):
        if isinstance(args[kqa__hgw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.initcap',
                ['arr', 'delim'], kqa__hgw)

    def impl(arr, delim):
        return initcap_util(arr, delim)
    return impl


@numba.generated_jit(nopython=True)
def instr(arr, target):
    args = [arr, target]
    for kqa__hgw in range(2):
        if isinstance(args[kqa__hgw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.instr',
                ['arr', 'target'], kqa__hgw)

    def impl(arr, target):
        return instr_util(arr, target)
    return impl


def left(arr, n_chars):
    return


@overload(left)
def overload_left(arr, n_chars):
    args = [arr, n_chars]
    for kqa__hgw in range(2):
        if isinstance(args[kqa__hgw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.left', [
                'arr', 'n_chars'], kqa__hgw)

    def impl(arr, n_chars):
        return left_util(arr, n_chars)
    return impl


def lpad(arr, length, padstr):
    return


@overload(lpad)
def overload_lpad(arr, length, padstr):
    args = [arr, length, padstr]
    for kqa__hgw in range(3):
        if isinstance(args[kqa__hgw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.lpad', [
                'arr', 'length', 'padstr'], kqa__hgw)

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
    for kqa__hgw in range(2):
        if isinstance(args[kqa__hgw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.repeat',
                ['arr', 'repeats'], kqa__hgw)

    def impl(arr, repeats):
        return repeat_util(arr, repeats)
    return impl


@numba.generated_jit(nopython=True)
def replace(arr, to_replace, replace_with):
    args = [arr, to_replace, replace_with]
    for kqa__hgw in range(3):
        if isinstance(args[kqa__hgw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.replace',
                ['arr', 'to_replace', 'replace_with'], kqa__hgw)

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
    for kqa__hgw in range(2):
        if isinstance(args[kqa__hgw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.right',
                ['arr', 'n_chars'], kqa__hgw)

    def impl(arr, n_chars):
        return right_util(arr, n_chars)
    return impl


def rpad(arr, length, padstr):
    return


@overload(rpad)
def overload_rpad(arr, length, padstr):
    args = [arr, length, padstr]
    for kqa__hgw in range(3):
        if isinstance(args[kqa__hgw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.rpad', [
                'arr', 'length', 'padstr'], kqa__hgw)

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
    for kqa__hgw in range(3):
        if isinstance(args[kqa__hgw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.split_part',
                ['source', 'delim', 'part'], kqa__hgw)

    def impl(source, delim, part):
        return split_part_util(source, delim, part)
    return impl


@numba.generated_jit(nopython=True)
def strcmp(arr0, arr1):
    args = [arr0, arr1]
    for kqa__hgw in range(2):
        if isinstance(args[kqa__hgw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.strcmp',
                ['arr0', 'arr1'], kqa__hgw)

    def impl(arr0, arr1):
        return strcmp_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def strtok(source, delim, part):
    args = [source, delim, part]
    for kqa__hgw in range(3):
        if isinstance(args[kqa__hgw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.strtok',
                ['source', 'delim', 'part'], kqa__hgw)

    def impl(source, delim, part):
        return strtok_util(source, delim, part)
    return impl


@numba.generated_jit(nopython=True)
def substring(arr, start, length):
    args = [arr, start, length]
    for kqa__hgw in range(3):
        if isinstance(args[kqa__hgw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.substring',
                ['arr', 'start', 'length'], kqa__hgw)

    def impl(arr, start, length):
        return substring_util(arr, start, length)
    return impl


@numba.generated_jit(nopython=True)
def substring_index(arr, delimiter, occurrences):
    args = [arr, delimiter, occurrences]
    for kqa__hgw in range(3):
        if isinstance(args[kqa__hgw], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.substring_index', ['arr',
                'delimiter', 'occurrences'], kqa__hgw)

    def impl(arr, delimiter, occurrences):
        return substring_index_util(arr, delimiter, occurrences)
    return impl


@numba.generated_jit(nopython=True)
def translate(arr, source, target):
    args = [arr, source, target]
    for kqa__hgw in range(3):
        if isinstance(args[kqa__hgw], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.translate',
                ['arr', 'source', 'target'], kqa__hgw)

    def impl(arr, source, target):
        return translate_util(arr, source, target)
    return impl


@numba.generated_jit(nopython=True)
def char_util(arr):
    verify_int_arg(arr, 'CHAR', 'arr')
    qulw__coflt = ['arr']
    xif__rnukb = [arr]
    gvj__imhug = [True]
    dvlc__wsyye = 'if 0 <= arg0 <= 127:\n'
    dvlc__wsyye += '   res[i] = chr(arg0)\n'
    dvlc__wsyye += 'else:\n'
    dvlc__wsyye += '   bodo.libs.array_kernels.setna(res, i)\n'
    lbp__qvhae = bodo.string_array_type
    return gen_vectorized(qulw__coflt, xif__rnukb, gvj__imhug, dvlc__wsyye,
        lbp__qvhae)


@numba.generated_jit(nopython=True)
def initcap_util(arr, delim):
    verify_string_arg(arr, 'INITCAP', 'arr')
    verify_string_arg(delim, 'INITCAP', 'delim')
    qulw__coflt = ['arr', 'delim']
    xif__rnukb = [arr, delim]
    gvj__imhug = [True] * 2
    dvlc__wsyye = 'capitalized = arg0[:1].upper()\n'
    dvlc__wsyye += 'for j in range(1, len(arg0)):\n'
    dvlc__wsyye += '   if arg0[j-1] in arg1:\n'
    dvlc__wsyye += '      capitalized += arg0[j].upper()\n'
    dvlc__wsyye += '   else:\n'
    dvlc__wsyye += '      capitalized += arg0[j].lower()\n'
    dvlc__wsyye += 'res[i] = capitalized'
    lbp__qvhae = bodo.string_array_type
    return gen_vectorized(qulw__coflt, xif__rnukb, gvj__imhug, dvlc__wsyye,
        lbp__qvhae)


@numba.generated_jit(nopython=True)
def instr_util(arr, target):
    verify_string_arg(arr, 'instr', 'arr')
    verify_string_arg(target, 'instr', 'target')
    qulw__coflt = ['arr', 'target']
    xif__rnukb = [arr, target]
    gvj__imhug = [True] * 2
    dvlc__wsyye = 'res[i] = arg0.find(arg1) + 1'
    lbp__qvhae = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(qulw__coflt, xif__rnukb, gvj__imhug, dvlc__wsyye,
        lbp__qvhae)


@register_jitable
def min_edit_distance(s, t):
    if len(s) > len(t):
        s, t = t, s
    dcy__tenlq, iyi__iumi = len(s), len(t)
    xqc__euagz, vzz__vue = 1, 0
    arr = np.zeros((2, dcy__tenlq + 1), dtype=np.uint32)
    arr[0, :] = np.arange(dcy__tenlq + 1)
    for kqa__hgw in range(1, iyi__iumi + 1):
        arr[xqc__euagz, 0] = kqa__hgw
        for gnejo__wsutg in range(1, dcy__tenlq + 1):
            if s[gnejo__wsutg - 1] == t[kqa__hgw - 1]:
                arr[xqc__euagz, gnejo__wsutg] = arr[vzz__vue, gnejo__wsutg - 1]
            else:
                arr[xqc__euagz, gnejo__wsutg] = 1 + min(arr[xqc__euagz, 
                    gnejo__wsutg - 1], arr[vzz__vue, gnejo__wsutg], arr[
                    vzz__vue, gnejo__wsutg - 1])
        xqc__euagz, vzz__vue = vzz__vue, xqc__euagz
    return arr[iyi__iumi % 2, dcy__tenlq]


@register_jitable
def min_edit_distance_with_max(s, t, maxDistance):
    if maxDistance < 0:
        return 0
    if len(s) > len(t):
        s, t = t, s
    dcy__tenlq, iyi__iumi = len(s), len(t)
    if dcy__tenlq <= maxDistance and iyi__iumi <= maxDistance:
        return min_edit_distance(s, t)
    xqc__euagz, vzz__vue = 1, 0
    arr = np.zeros((2, dcy__tenlq + 1), dtype=np.uint32)
    arr[0, :] = np.arange(dcy__tenlq + 1)
    for kqa__hgw in range(1, iyi__iumi + 1):
        arr[xqc__euagz, 0] = kqa__hgw
        for gnejo__wsutg in range(1, dcy__tenlq + 1):
            if s[gnejo__wsutg - 1] == t[kqa__hgw - 1]:
                arr[xqc__euagz, gnejo__wsutg] = arr[vzz__vue, gnejo__wsutg - 1]
            else:
                arr[xqc__euagz, gnejo__wsutg] = 1 + min(arr[xqc__euagz, 
                    gnejo__wsutg - 1], arr[vzz__vue, gnejo__wsutg], arr[
                    vzz__vue, gnejo__wsutg - 1])
        if (arr[xqc__euagz] >= maxDistance).all():
            return maxDistance
        xqc__euagz, vzz__vue = vzz__vue, xqc__euagz
    return min(arr[iyi__iumi % 2, dcy__tenlq], maxDistance)


@numba.generated_jit(nopython=True)
def editdistance_no_max_util(s, t):
    verify_string_arg(s, 'editdistance_no_max', 's')
    verify_string_arg(t, 'editdistance_no_max', 't')
    qulw__coflt = ['s', 't']
    xif__rnukb = [s, t]
    gvj__imhug = [True] * 2
    dvlc__wsyye = (
        'res[i] = bodo.libs.bodosql_array_kernels.min_edit_distance(arg0, arg1)'
        )
    lbp__qvhae = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(qulw__coflt, xif__rnukb, gvj__imhug, dvlc__wsyye,
        lbp__qvhae)


@numba.generated_jit(nopython=True)
def editdistance_with_max_util(s, t, maxDistance):
    verify_string_arg(s, 'editdistance_no_max', 's')
    verify_string_arg(t, 'editdistance_no_max', 't')
    verify_int_arg(maxDistance, 'editdistance_no_max', 't')
    qulw__coflt = ['s', 't', 'maxDistance']
    xif__rnukb = [s, t, maxDistance]
    gvj__imhug = [True] * 3
    dvlc__wsyye = (
        'res[i] = bodo.libs.bodosql_array_kernels.min_edit_distance_with_max(arg0, arg1, arg2)'
        )
    lbp__qvhae = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(qulw__coflt, xif__rnukb, gvj__imhug, dvlc__wsyye,
        lbp__qvhae)


@numba.generated_jit(nopython=True)
def format_util(arr, places):
    verify_int_float_arg(arr, 'FORMAT', 'arr')
    verify_int_arg(places, 'FORMAT', 'places')
    qulw__coflt = ['arr', 'places']
    xif__rnukb = [arr, places]
    gvj__imhug = [True] * 2
    dvlc__wsyye = 'prec = max(arg1, 0)\n'
    dvlc__wsyye += "res[i] = format(arg0, f',.{prec}f')"
    lbp__qvhae = bodo.string_array_type
    return gen_vectorized(qulw__coflt, xif__rnukb, gvj__imhug, dvlc__wsyye,
        lbp__qvhae)


def left_util(arr, n_chars):
    return


def right_util(arr, n_chars):
    return


def create_left_right_util_overload(func_name):

    def overload_left_right_util(arr, n_chars):
        rlvua__nwevb = verify_string_binary_arg(arr, func_name, 'arr')
        verify_int_arg(n_chars, func_name, 'n_chars')
        oam__azkf = "''" if rlvua__nwevb else "b''"
        qulw__coflt = ['arr', 'n_chars']
        xif__rnukb = [arr, n_chars]
        gvj__imhug = [True] * 2
        dvlc__wsyye = 'if arg1 <= 0:\n'
        dvlc__wsyye += f'   res[i] = {oam__azkf}\n'
        dvlc__wsyye += 'else:\n'
        if func_name == 'LEFT':
            dvlc__wsyye += '   res[i] = arg0[:arg1]'
        elif func_name == 'RIGHT':
            dvlc__wsyye += '   res[i] = arg0[-arg1:]'
        lbp__qvhae = (bodo.string_array_type if rlvua__nwevb else bodo.
            binary_array_type)
        return gen_vectorized(qulw__coflt, xif__rnukb, gvj__imhug,
            dvlc__wsyye, lbp__qvhae)
    return overload_left_right_util


def _install_left_right_overload():
    for ryox__lvm, func_name in zip((left_util, right_util), ('LEFT', 'RIGHT')
        ):
        rep__ptbuh = create_left_right_util_overload(func_name)
        overload(ryox__lvm)(rep__ptbuh)


_install_left_right_overload()


def lpad_util(arr, length, padstr):
    return


def rpad_util(arr, length, padstr):
    return


def create_lpad_rpad_util_overload(func_name):

    def overload_lpad_rpad_util(arr, length, pad_string):
        fep__hbj = verify_string_binary_arg(pad_string, func_name, 'pad_string'
            )
        rlvua__nwevb = verify_string_binary_arg(arr, func_name, 'arr')
        if rlvua__nwevb != fep__hbj:
            raise bodo.utils.typing.BodoError(
                'Pad string and arr must be the same type!')
        lbp__qvhae = (bodo.string_array_type if rlvua__nwevb else bodo.
            binary_array_type)
        verify_int_arg(length, func_name, 'length')
        verify_string_binary_arg(pad_string, func_name,
            f'{func_name.lower()}_string')
        if func_name == 'LPAD':
            fdtf__awwmb = f'(arg2 * quotient) + arg2[:remainder] + arg0'
        elif func_name == 'RPAD':
            fdtf__awwmb = f'arg0 + (arg2 * quotient) + arg2[:remainder]'
        qulw__coflt = ['arr', 'length', 'pad_string']
        xif__rnukb = [arr, length, pad_string]
        gvj__imhug = [True] * 3
        oam__azkf = "''" if rlvua__nwevb else "b''"
        dvlc__wsyye = f"""                if arg1 <= 0:
                    res[i] = {oam__azkf}
                elif len(arg2) == 0:
                    res[i] = arg0
                elif len(arg0) >= arg1:
                    res[i] = arg0[:arg1]
                else:
                    quotient = (arg1 - len(arg0)) // len(arg2)
                    remainder = (arg1 - len(arg0)) % len(arg2)
                    res[i] = {fdtf__awwmb}"""
        return gen_vectorized(qulw__coflt, xif__rnukb, gvj__imhug,
            dvlc__wsyye, lbp__qvhae)
    return overload_lpad_rpad_util


def _install_lpad_rpad_overload():
    for ryox__lvm, func_name in zip((lpad_util, rpad_util), ('LPAD', 'RPAD')):
        rep__ptbuh = create_lpad_rpad_util_overload(func_name)
        overload(ryox__lvm)(rep__ptbuh)


_install_lpad_rpad_overload()


@numba.generated_jit(nopython=True)
def ord_ascii_util(arr):
    verify_string_arg(arr, 'ORD', 'arr')
    qulw__coflt = ['arr']
    xif__rnukb = [arr]
    gvj__imhug = [True]
    dvlc__wsyye = 'if len(arg0) == 0:\n'
    dvlc__wsyye += '   bodo.libs.array_kernels.setna(res, i)\n'
    dvlc__wsyye += 'else:\n'
    dvlc__wsyye += '   res[i] = ord(arg0[0])'
    lbp__qvhae = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(qulw__coflt, xif__rnukb, gvj__imhug, dvlc__wsyye,
        lbp__qvhae)


@numba.generated_jit(nopython=True)
def repeat_util(arr, repeats):
    verify_string_arg(arr, 'REPEAT', 'arr')
    verify_int_arg(repeats, 'REPEAT', 'repeats')
    qulw__coflt = ['arr', 'repeats']
    xif__rnukb = [arr, repeats]
    gvj__imhug = [True] * 2
    dvlc__wsyye = 'if arg1 <= 0:\n'
    dvlc__wsyye += "   res[i] = ''\n"
    dvlc__wsyye += 'else:\n'
    dvlc__wsyye += '   res[i] = arg0 * arg1'
    lbp__qvhae = bodo.string_array_type
    return gen_vectorized(qulw__coflt, xif__rnukb, gvj__imhug, dvlc__wsyye,
        lbp__qvhae)


@numba.generated_jit(nopython=True)
def replace_util(arr, to_replace, replace_with):
    verify_string_arg(arr, 'REPLACE', 'arr')
    verify_string_arg(to_replace, 'REPLACE', 'to_replace')
    verify_string_arg(replace_with, 'REPLACE', 'replace_with')
    qulw__coflt = ['arr', 'to_replace', 'replace_with']
    xif__rnukb = [arr, to_replace, replace_with]
    gvj__imhug = [True] * 3
    dvlc__wsyye = "if arg1 == '':\n"
    dvlc__wsyye += '   res[i] = arg0\n'
    dvlc__wsyye += 'else:\n'
    dvlc__wsyye += '   res[i] = arg0.replace(arg1, arg2)'
    lbp__qvhae = bodo.string_array_type
    return gen_vectorized(qulw__coflt, xif__rnukb, gvj__imhug, dvlc__wsyye,
        lbp__qvhae)


@numba.generated_jit(nopython=True)
def reverse_util(arr):
    rlvua__nwevb = verify_string_binary_arg(arr, 'REVERSE', 'arr')
    qulw__coflt = ['arr']
    xif__rnukb = [arr]
    gvj__imhug = [True]
    dvlc__wsyye = 'res[i] = arg0[::-1]'
    lbp__qvhae = bodo.string_array_type
    lbp__qvhae = (bodo.string_array_type if rlvua__nwevb else bodo.
        binary_array_type)
    return gen_vectorized(qulw__coflt, xif__rnukb, gvj__imhug, dvlc__wsyye,
        lbp__qvhae)


@numba.generated_jit(nopython=True)
def space_util(n_chars):
    verify_int_arg(n_chars, 'SPACE', 'n_chars')
    qulw__coflt = ['n_chars']
    xif__rnukb = [n_chars]
    gvj__imhug = [True]
    dvlc__wsyye = 'if arg0 <= 0:\n'
    dvlc__wsyye += "   res[i] = ''\n"
    dvlc__wsyye += 'else:\n'
    dvlc__wsyye += "   res[i] = ' ' * arg0"
    lbp__qvhae = bodo.string_array_type
    return gen_vectorized(qulw__coflt, xif__rnukb, gvj__imhug, dvlc__wsyye,
        lbp__qvhae)


@numba.generated_jit(nopython=True)
def split_part_util(source, delim, part):
    verify_string_arg(source, 'SPLIT_PART', 'source')
    verify_string_arg(delim, 'SPLIT_PART', 'delim')
    verify_int_arg(part, 'SPLIT_PART', 'part')
    qulw__coflt = ['source', 'delim', 'part']
    xif__rnukb = [source, delim, part]
    gvj__imhug = [True] * 3
    dvlc__wsyye = "tokens = arg0.split(arg1) if arg1 != '' else [arg0]\n"
    dvlc__wsyye += 'if abs(arg2) > len(tokens):\n'
    dvlc__wsyye += "    res[i] = ''\n"
    dvlc__wsyye += 'else:\n'
    dvlc__wsyye += '    res[i] = tokens[arg2 if arg2 <= 0 else arg2-1]\n'
    lbp__qvhae = bodo.string_array_type
    return gen_vectorized(qulw__coflt, xif__rnukb, gvj__imhug, dvlc__wsyye,
        lbp__qvhae)


@numba.generated_jit(nopython=True)
def strcmp_util(arr0, arr1):
    verify_string_arg(arr0, 'strcmp', 'arr0')
    verify_string_arg(arr1, 'strcmp', 'arr1')
    qulw__coflt = ['arr0', 'arr1']
    xif__rnukb = [arr0, arr1]
    gvj__imhug = [True] * 2
    dvlc__wsyye = 'if arg0 < arg1:\n'
    dvlc__wsyye += '   res[i] = -1\n'
    dvlc__wsyye += 'elif arg0 > arg1:\n'
    dvlc__wsyye += '   res[i] = 1\n'
    dvlc__wsyye += 'else:\n'
    dvlc__wsyye += '   res[i] = 0\n'
    lbp__qvhae = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(qulw__coflt, xif__rnukb, gvj__imhug, dvlc__wsyye,
        lbp__qvhae)


@numba.generated_jit(nopython=True)
def strtok_util(source, delim, part):
    verify_string_arg(source, 'STRTOK', 'source')
    verify_string_arg(delim, 'STRTOK', 'delim')
    verify_int_arg(part, 'STRTOK', 'part')
    qulw__coflt = ['source', 'delim', 'part']
    xif__rnukb = [source, delim, part]
    gvj__imhug = [True] * 3
    dvlc__wsyye = "if (arg0 == '' and arg1 == '') or arg2 <= 0:\n"
    dvlc__wsyye += '   bodo.libs.array_kernels.setna(res, i)\n'
    dvlc__wsyye += 'else:\n'
    dvlc__wsyye += '   tokens = []\n'
    dvlc__wsyye += "   buffer = ''\n"
    dvlc__wsyye += '   for j in range(len(arg0)):\n'
    dvlc__wsyye += '      if arg0[j] in arg1:\n'
    dvlc__wsyye += "         if buffer != '':"
    dvlc__wsyye += '            tokens.append(buffer)\n'
    dvlc__wsyye += "         buffer = ''\n"
    dvlc__wsyye += '      else:\n'
    dvlc__wsyye += '         buffer += arg0[j]\n'
    dvlc__wsyye += "   if buffer != '':\n"
    dvlc__wsyye += '      tokens.append(buffer)\n'
    dvlc__wsyye += '   if arg2 > len(tokens):\n'
    dvlc__wsyye += '      bodo.libs.array_kernels.setna(res, i)\n'
    dvlc__wsyye += '   else:\n'
    dvlc__wsyye += '      res[i] = tokens[arg2-1]\n'
    lbp__qvhae = bodo.string_array_type
    return gen_vectorized(qulw__coflt, xif__rnukb, gvj__imhug, dvlc__wsyye,
        lbp__qvhae)


@numba.generated_jit(nopython=True)
def substring_util(arr, start, length):
    rlvua__nwevb = verify_string_binary_arg(arr, 'SUBSTRING', 'arr')
    verify_int_arg(start, 'SUBSTRING', 'start')
    verify_int_arg(length, 'SUBSTRING', 'length')
    lbp__qvhae = (bodo.string_array_type if rlvua__nwevb else bodo.
        binary_array_type)
    qulw__coflt = ['arr', 'start', 'length']
    xif__rnukb = [arr, start, length]
    gvj__imhug = [True] * 3
    dvlc__wsyye = 'if arg2 <= 0:\n'
    dvlc__wsyye += "   res[i] = ''\n" if rlvua__nwevb else "   res[i] = b''\n"
    dvlc__wsyye += 'elif arg1 < 0 and arg1 + arg2 >= 0:\n'
    dvlc__wsyye += '   res[i] = arg0[arg1:]\n'
    dvlc__wsyye += 'else:\n'
    dvlc__wsyye += '   if arg1 > 0: arg1 -= 1\n'
    dvlc__wsyye += '   res[i] = arg0[arg1:arg1+arg2]\n'
    return gen_vectorized(qulw__coflt, xif__rnukb, gvj__imhug, dvlc__wsyye,
        lbp__qvhae)


@numba.generated_jit(nopython=True)
def substring_index_util(arr, delimiter, occurrences):
    verify_string_arg(arr, 'SUBSTRING_INDEX', 'arr')
    verify_string_arg(delimiter, 'SUBSTRING_INDEX', 'delimiter')
    verify_int_arg(occurrences, 'SUBSTRING_INDEX', 'occurrences')
    qulw__coflt = ['arr', 'delimiter', 'occurrences']
    xif__rnukb = [arr, delimiter, occurrences]
    gvj__imhug = [True] * 3
    dvlc__wsyye = "if arg1 == '' or arg2 == 0:\n"
    dvlc__wsyye += "   res[i] = ''\n"
    dvlc__wsyye += 'elif arg2 >= 0:\n'
    dvlc__wsyye += '   res[i] = arg1.join(arg0.split(arg1, arg2+1)[:arg2])\n'
    dvlc__wsyye += 'else:\n'
    dvlc__wsyye += '   res[i] = arg1.join(arg0.split(arg1)[arg2:])\n'
    lbp__qvhae = bodo.string_array_type
    return gen_vectorized(qulw__coflt, xif__rnukb, gvj__imhug, dvlc__wsyye,
        lbp__qvhae)


@numba.generated_jit(nopython=True)
def translate_util(arr, source, target):
    verify_string_arg(arr, 'translate', 'arr')
    verify_string_arg(source, 'translate', 'source')
    verify_string_arg(target, 'translate', 'target')
    qulw__coflt = ['arr', 'source', 'target']
    xif__rnukb = [arr, source, target]
    gvj__imhug = [True] * 3
    dvlc__wsyye = "translated = ''\n"
    dvlc__wsyye += 'for char in arg0:\n'
    dvlc__wsyye += '   index = arg1.find(char)\n'
    dvlc__wsyye += '   if index == -1:\n'
    dvlc__wsyye += '      translated += char\n'
    dvlc__wsyye += '   elif index < len(arg2):\n'
    dvlc__wsyye += '      translated += arg2[index]\n'
    dvlc__wsyye += 'res[i] = translated'
    lbp__qvhae = bodo.string_array_type
    return gen_vectorized(qulw__coflt, xif__rnukb, gvj__imhug, dvlc__wsyye,
        lbp__qvhae)
