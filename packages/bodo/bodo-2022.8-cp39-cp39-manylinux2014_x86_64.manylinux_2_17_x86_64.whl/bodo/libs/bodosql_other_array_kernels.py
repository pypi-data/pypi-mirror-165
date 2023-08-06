"""
Implements miscellaneous array kernels that are specific to BodoSQL
"""
import numba
from numba.core import types
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import raise_bodo_error


@numba.generated_jit(nopython=True)
def booland(A, B):
    args = [A, B]
    for eilq__nuo in range(2):
        if isinstance(args[eilq__nuo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.booland',
                ['A', 'B'], eilq__nuo)

    def impl(A, B):
        return booland_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def boolor(A, B):
    args = [A, B]
    for eilq__nuo in range(2):
        if isinstance(args[eilq__nuo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.boolor',
                ['A', 'B'], eilq__nuo)

    def impl(A, B):
        return boolor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def boolxor(A, B):
    args = [A, B]
    for eilq__nuo in range(2):
        if isinstance(args[eilq__nuo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.boolxor',
                ['A', 'B'], eilq__nuo)

    def impl(A, B):
        return boolxor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def boolnot(A):
    if isinstance(A, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.boolnot_util',
            ['A'], 0)

    def impl(A):
        return boolnot_util(A)
    return impl


@numba.generated_jit(nopython=True)
def cond(arr, ifbranch, elsebranch):
    args = [arr, ifbranch, elsebranch]
    for eilq__nuo in range(3):
        if isinstance(args[eilq__nuo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.cond', [
                'arr', 'ifbranch', 'elsebranch'], eilq__nuo)

    def impl(arr, ifbranch, elsebranch):
        return cond_util(arr, ifbranch, elsebranch)
    return impl


@numba.generated_jit(nopython=True)
def equal_null(A, B):
    args = [A, B]
    for eilq__nuo in range(2):
        if isinstance(args[eilq__nuo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.equal_null',
                ['A', 'B'], eilq__nuo)

    def impl(A, B):
        return equal_null_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def booland_util(A, B):
    verify_int_float_arg(A, 'BOOLAND', 'A')
    verify_int_float_arg(B, 'BOOLAND', 'B')
    edkf__ztc = ['A', 'B']
    bizuh__lxgih = [A, B]
    ddwz__pqjla = [False] * 2
    if A == bodo.none:
        ddwz__pqjla = [False, True]
        mkvg__olvv = 'if arg1 != 0:\n'
        mkvg__olvv += '   bodo.libs.array_kernels.setna(res, i)\n'
        mkvg__olvv += 'else:\n'
        mkvg__olvv += '   res[i] = False\n'
    elif B == bodo.none:
        ddwz__pqjla = [True, False]
        mkvg__olvv = 'if arg0 != 0:\n'
        mkvg__olvv += '   bodo.libs.array_kernels.setna(res, i)\n'
        mkvg__olvv += 'else:\n'
        mkvg__olvv += '   res[i] = False\n'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            mkvg__olvv = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            mkvg__olvv += '   bodo.libs.array_kernels.setna(res, i)\n'
            mkvg__olvv += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            mkvg__olvv += '   bodo.libs.array_kernels.setna(res, i)\n'
            mkvg__olvv += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n')
            mkvg__olvv += '   bodo.libs.array_kernels.setna(res, i)\n'
            mkvg__olvv += 'else:\n'
            mkvg__olvv += '   res[i] = (arg0 != 0) and (arg1 != 0)'
        else:
            mkvg__olvv = (
                'if bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            mkvg__olvv += '   bodo.libs.array_kernels.setna(res, i)\n'
            mkvg__olvv += 'else:\n'
            mkvg__olvv += '   res[i] = (arg0 != 0) and (arg1 != 0)'
    elif bodo.utils.utils.is_array_typ(B, True):
        mkvg__olvv = 'if bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n'
        mkvg__olvv += '   bodo.libs.array_kernels.setna(res, i)\n'
        mkvg__olvv += 'else:\n'
        mkvg__olvv += '   res[i] = (arg0 != 0) and (arg1 != 0)'
    else:
        mkvg__olvv = 'res[i] = (arg0 != 0) and (arg1 != 0)'
    dve__vkelk = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(edkf__ztc, bizuh__lxgih, ddwz__pqjla, mkvg__olvv,
        dve__vkelk)


@numba.generated_jit(nopython=True)
def boolor_util(A, B):
    verify_int_float_arg(A, 'BOOLOR', 'A')
    verify_int_float_arg(B, 'BOOLOR', 'B')
    edkf__ztc = ['A', 'B']
    bizuh__lxgih = [A, B]
    ddwz__pqjla = [False] * 2
    if A == bodo.none:
        ddwz__pqjla = [False, True]
        mkvg__olvv = 'if arg1 == 0:\n'
        mkvg__olvv += '   bodo.libs.array_kernels.setna(res, i)\n'
        mkvg__olvv += 'else:\n'
        mkvg__olvv += '   res[i] = True\n'
    elif B == bodo.none:
        ddwz__pqjla = [True, False]
        mkvg__olvv = 'if arg0 == 0:\n'
        mkvg__olvv += '   bodo.libs.array_kernels.setna(res, i)\n'
        mkvg__olvv += 'else:\n'
        mkvg__olvv += '   res[i] = True\n'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            mkvg__olvv = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            mkvg__olvv += '   bodo.libs.array_kernels.setna(res, i)\n'
            mkvg__olvv += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            mkvg__olvv += '   res[i] = True\n'
            mkvg__olvv += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 == 0:\n')
            mkvg__olvv += '   bodo.libs.array_kernels.setna(res, i)\n'
            mkvg__olvv += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n')
            mkvg__olvv += '   res[i] = True\n'
            mkvg__olvv += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 == 0:\n')
            mkvg__olvv += '   bodo.libs.array_kernels.setna(res, i)\n'
            mkvg__olvv += 'else:\n'
            mkvg__olvv += '   res[i] = (arg0 != 0) or (arg1 != 0)'
        else:
            mkvg__olvv = (
                'if bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            mkvg__olvv += '   res[i] = True\n'
            mkvg__olvv += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 == 0:\n')
            mkvg__olvv += '   bodo.libs.array_kernels.setna(res, i)\n'
            mkvg__olvv += 'else:\n'
            mkvg__olvv += '   res[i] = (arg0 != 0) or (arg1 != 0)'
    elif bodo.utils.utils.is_array_typ(B, True):
        mkvg__olvv = 'if bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n'
        mkvg__olvv += '   res[i] = True\n'
        mkvg__olvv += (
            'elif bodo.libs.array_kernels.isna(B, i) and arg0 == 0:\n')
        mkvg__olvv += '   bodo.libs.array_kernels.setna(res, i)\n'
        mkvg__olvv += 'else:\n'
        mkvg__olvv += '   res[i] = (arg0 != 0) or (arg1 != 0)'
    else:
        mkvg__olvv = 'res[i] = (arg0 != 0) or (arg1 != 0)'
    dve__vkelk = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(edkf__ztc, bizuh__lxgih, ddwz__pqjla, mkvg__olvv,
        dve__vkelk)


@numba.generated_jit(nopython=True)
def boolxor_util(A, B):
    verify_int_float_arg(A, 'BOOLXOR', 'A')
    verify_int_float_arg(B, 'BOOLXOR', 'B')
    edkf__ztc = ['A', 'B']
    bizuh__lxgih = [A, B]
    ddwz__pqjla = [True] * 2
    mkvg__olvv = 'res[i] = (arg0 == 0) != (arg1 == 0)'
    dve__vkelk = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(edkf__ztc, bizuh__lxgih, ddwz__pqjla, mkvg__olvv,
        dve__vkelk)


@numba.generated_jit(nopython=True)
def boolnot_util(A):
    verify_int_float_arg(A, 'BOOLNOT', 'A')
    edkf__ztc = ['A']
    bizuh__lxgih = [A]
    ddwz__pqjla = [True]
    mkvg__olvv = 'res[i] = arg0 == 0'
    dve__vkelk = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(edkf__ztc, bizuh__lxgih, ddwz__pqjla, mkvg__olvv,
        dve__vkelk)


@numba.generated_jit(nopython=True)
def nullif(arr0, arr1):
    args = [arr0, arr1]
    for eilq__nuo in range(2):
        if isinstance(args[eilq__nuo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.nullif',
                ['arr0', 'arr1'], eilq__nuo)

    def impl(arr0, arr1):
        return nullif_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def regr_valx(y, x):
    args = [y, x]
    for eilq__nuo in range(2):
        if isinstance(args[eilq__nuo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regr_valx',
                ['y', 'x'], eilq__nuo)

    def impl(y, x):
        return regr_valx_util(y, x)
    return impl


@numba.generated_jit(nopython=True)
def regr_valy(y, x):
    args = [y, x]
    for eilq__nuo in range(2):
        if isinstance(args[eilq__nuo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regr_valy',
                ['y', 'x'], eilq__nuo)

    def impl(y, x):
        return regr_valx(x, y)
    return impl


@numba.generated_jit(nopython=True)
def cond_util(arr, ifbranch, elsebranch):
    verify_boolean_arg(arr, 'cond', 'arr')
    if bodo.utils.utils.is_array_typ(arr, True
        ) and ifbranch == bodo.none and elsebranch == bodo.none:
        raise_bodo_error('Both branches of IF() cannot be scalar NULL')
    edkf__ztc = ['arr', 'ifbranch', 'elsebranch']
    bizuh__lxgih = [arr, ifbranch, elsebranch]
    ddwz__pqjla = [False] * 3
    if bodo.utils.utils.is_array_typ(arr, True):
        mkvg__olvv = (
            'if (not bodo.libs.array_kernels.isna(arr, i)) and arg0:\n')
    elif arr != bodo.none:
        mkvg__olvv = 'if arg0:\n'
    else:
        mkvg__olvv = ''
    if arr != bodo.none:
        if bodo.utils.utils.is_array_typ(ifbranch, True):
            mkvg__olvv += '   if bodo.libs.array_kernels.isna(ifbranch, i):\n'
            mkvg__olvv += '      bodo.libs.array_kernels.setna(res, i)\n'
            mkvg__olvv += '   else:\n'
            mkvg__olvv += '      res[i] = arg1\n'
        elif ifbranch == bodo.none:
            mkvg__olvv += '   bodo.libs.array_kernels.setna(res, i)\n'
        else:
            mkvg__olvv += '   res[i] = arg1\n'
        mkvg__olvv += 'else:\n'
    if bodo.utils.utils.is_array_typ(elsebranch, True):
        mkvg__olvv += '   if bodo.libs.array_kernels.isna(elsebranch, i):\n'
        mkvg__olvv += '      bodo.libs.array_kernels.setna(res, i)\n'
        mkvg__olvv += '   else:\n'
        mkvg__olvv += '      res[i] = arg2\n'
    elif elsebranch == bodo.none:
        mkvg__olvv += '   bodo.libs.array_kernels.setna(res, i)\n'
    else:
        mkvg__olvv += '   res[i] = arg2\n'
    dve__vkelk = get_common_broadcasted_type([ifbranch, elsebranch], 'IF')
    return gen_vectorized(edkf__ztc, bizuh__lxgih, ddwz__pqjla, mkvg__olvv,
        dve__vkelk)


@numba.generated_jit(nopython=True)
def equal_null_util(A, B):
    get_common_broadcasted_type([A, B], 'EQUAL_NULL')
    edkf__ztc = ['A', 'B']
    bizuh__lxgih = [A, B]
    ddwz__pqjla = [False] * 2
    if A == bodo.none:
        if B == bodo.none:
            mkvg__olvv = 'res[i] = True'
        elif bodo.utils.utils.is_array_typ(B, True):
            mkvg__olvv = 'res[i] = bodo.libs.array_kernels.isna(B, i)'
        else:
            mkvg__olvv = 'res[i] = False'
    elif B == bodo.none:
        if bodo.utils.utils.is_array_typ(A, True):
            mkvg__olvv = 'res[i] = bodo.libs.array_kernels.isna(A, i)'
        else:
            mkvg__olvv = 'res[i] = False'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            mkvg__olvv = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            mkvg__olvv += '   res[i] = True\n'
            mkvg__olvv += """elif bodo.libs.array_kernels.isna(A, i) or bodo.libs.array_kernels.isna(B, i):
"""
            mkvg__olvv += '   res[i] = False\n'
            mkvg__olvv += 'else:\n'
            mkvg__olvv += '   res[i] = arg0 == arg1'
        else:
            mkvg__olvv = (
                'res[i] = (not bodo.libs.array_kernels.isna(A, i)) and arg0 == arg1'
                )
    elif bodo.utils.utils.is_array_typ(B, True):
        mkvg__olvv = (
            'res[i] = (not bodo.libs.array_kernels.isna(B, i)) and arg0 == arg1'
            )
    else:
        mkvg__olvv = 'res[i] = arg0 == arg1'
    dve__vkelk = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(edkf__ztc, bizuh__lxgih, ddwz__pqjla, mkvg__olvv,
        dve__vkelk)


@numba.generated_jit(nopython=True)
def nullif_util(arr0, arr1):
    edkf__ztc = ['arr0', 'arr1']
    bizuh__lxgih = [arr0, arr1]
    ddwz__pqjla = [True, False]
    if arr1 == bodo.none:
        mkvg__olvv = 'res[i] = arg0\n'
    elif bodo.utils.utils.is_array_typ(arr1, True):
        mkvg__olvv = (
            'if bodo.libs.array_kernels.isna(arr1, i) or arg0 != arg1:\n')
        mkvg__olvv += '   res[i] = arg0\n'
        mkvg__olvv += 'else:\n'
        mkvg__olvv += '   bodo.libs.array_kernels.setna(res, i)'
    else:
        mkvg__olvv = 'if arg0 != arg1:\n'
        mkvg__olvv += '   res[i] = arg0\n'
        mkvg__olvv += 'else:\n'
        mkvg__olvv += '   bodo.libs.array_kernels.setna(res, i)'
    dve__vkelk = get_common_broadcasted_type([arr0, arr1], 'NULLIF')
    return gen_vectorized(edkf__ztc, bizuh__lxgih, ddwz__pqjla, mkvg__olvv,
        dve__vkelk)


@numba.generated_jit(nopython=True)
def regr_valx_util(y, x):
    verify_int_float_arg(y, 'regr_valx', 'y')
    verify_int_float_arg(x, 'regr_valx', 'x')
    edkf__ztc = ['y', 'x']
    bizuh__lxgih = [y, x]
    hhib__kwkx = [True] * 2
    mkvg__olvv = 'res[i] = arg1'
    dve__vkelk = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(edkf__ztc, bizuh__lxgih, hhib__kwkx, mkvg__olvv,
        dve__vkelk)
