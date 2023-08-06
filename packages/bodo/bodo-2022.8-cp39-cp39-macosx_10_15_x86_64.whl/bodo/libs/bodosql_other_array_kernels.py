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
    for imlox__dxdaz in range(2):
        if isinstance(args[imlox__dxdaz], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.booland',
                ['A', 'B'], imlox__dxdaz)

    def impl(A, B):
        return booland_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def boolor(A, B):
    args = [A, B]
    for imlox__dxdaz in range(2):
        if isinstance(args[imlox__dxdaz], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.boolor',
                ['A', 'B'], imlox__dxdaz)

    def impl(A, B):
        return boolor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def boolxor(A, B):
    args = [A, B]
    for imlox__dxdaz in range(2):
        if isinstance(args[imlox__dxdaz], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.boolxor',
                ['A', 'B'], imlox__dxdaz)

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
    for imlox__dxdaz in range(3):
        if isinstance(args[imlox__dxdaz], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.cond', [
                'arr', 'ifbranch', 'elsebranch'], imlox__dxdaz)

    def impl(arr, ifbranch, elsebranch):
        return cond_util(arr, ifbranch, elsebranch)
    return impl


@numba.generated_jit(nopython=True)
def equal_null(A, B):
    args = [A, B]
    for imlox__dxdaz in range(2):
        if isinstance(args[imlox__dxdaz], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.equal_null',
                ['A', 'B'], imlox__dxdaz)

    def impl(A, B):
        return equal_null_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def booland_util(A, B):
    verify_int_float_arg(A, 'BOOLAND', 'A')
    verify_int_float_arg(B, 'BOOLAND', 'B')
    bxuu__gyjj = ['A', 'B']
    shrss__oyuxc = [A, B]
    pbda__fls = [False] * 2
    if A == bodo.none:
        pbda__fls = [False, True]
        kmg__ojl = 'if arg1 != 0:\n'
        kmg__ojl += '   bodo.libs.array_kernels.setna(res, i)\n'
        kmg__ojl += 'else:\n'
        kmg__ojl += '   res[i] = False\n'
    elif B == bodo.none:
        pbda__fls = [True, False]
        kmg__ojl = 'if arg0 != 0:\n'
        kmg__ojl += '   bodo.libs.array_kernels.setna(res, i)\n'
        kmg__ojl += 'else:\n'
        kmg__ojl += '   res[i] = False\n'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            kmg__ojl = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            kmg__ojl += '   bodo.libs.array_kernels.setna(res, i)\n'
            kmg__ojl += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            kmg__ojl += '   bodo.libs.array_kernels.setna(res, i)\n'
            kmg__ojl += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n')
            kmg__ojl += '   bodo.libs.array_kernels.setna(res, i)\n'
            kmg__ojl += 'else:\n'
            kmg__ojl += '   res[i] = (arg0 != 0) and (arg1 != 0)'
        else:
            kmg__ojl = 'if bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n'
            kmg__ojl += '   bodo.libs.array_kernels.setna(res, i)\n'
            kmg__ojl += 'else:\n'
            kmg__ojl += '   res[i] = (arg0 != 0) and (arg1 != 0)'
    elif bodo.utils.utils.is_array_typ(B, True):
        kmg__ojl = 'if bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n'
        kmg__ojl += '   bodo.libs.array_kernels.setna(res, i)\n'
        kmg__ojl += 'else:\n'
        kmg__ojl += '   res[i] = (arg0 != 0) and (arg1 != 0)'
    else:
        kmg__ojl = 'res[i] = (arg0 != 0) and (arg1 != 0)'
    dnvk__kpus = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(bxuu__gyjj, shrss__oyuxc, pbda__fls, kmg__ojl,
        dnvk__kpus)


@numba.generated_jit(nopython=True)
def boolor_util(A, B):
    verify_int_float_arg(A, 'BOOLOR', 'A')
    verify_int_float_arg(B, 'BOOLOR', 'B')
    bxuu__gyjj = ['A', 'B']
    shrss__oyuxc = [A, B]
    pbda__fls = [False] * 2
    if A == bodo.none:
        pbda__fls = [False, True]
        kmg__ojl = 'if arg1 == 0:\n'
        kmg__ojl += '   bodo.libs.array_kernels.setna(res, i)\n'
        kmg__ojl += 'else:\n'
        kmg__ojl += '   res[i] = True\n'
    elif B == bodo.none:
        pbda__fls = [True, False]
        kmg__ojl = 'if arg0 == 0:\n'
        kmg__ojl += '   bodo.libs.array_kernels.setna(res, i)\n'
        kmg__ojl += 'else:\n'
        kmg__ojl += '   res[i] = True\n'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            kmg__ojl = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            kmg__ojl += '   bodo.libs.array_kernels.setna(res, i)\n'
            kmg__ojl += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n')
            kmg__ojl += '   res[i] = True\n'
            kmg__ojl += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 == 0:\n')
            kmg__ojl += '   bodo.libs.array_kernels.setna(res, i)\n'
            kmg__ojl += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n')
            kmg__ojl += '   res[i] = True\n'
            kmg__ojl += (
                'elif bodo.libs.array_kernels.isna(B, i) and arg0 == 0:\n')
            kmg__ojl += '   bodo.libs.array_kernels.setna(res, i)\n'
            kmg__ojl += 'else:\n'
            kmg__ojl += '   res[i] = (arg0 != 0) or (arg1 != 0)'
        else:
            kmg__ojl = 'if bodo.libs.array_kernels.isna(A, i) and arg1 != 0:\n'
            kmg__ojl += '   res[i] = True\n'
            kmg__ojl += (
                'elif bodo.libs.array_kernels.isna(A, i) and arg1 == 0:\n')
            kmg__ojl += '   bodo.libs.array_kernels.setna(res, i)\n'
            kmg__ojl += 'else:\n'
            kmg__ojl += '   res[i] = (arg0 != 0) or (arg1 != 0)'
    elif bodo.utils.utils.is_array_typ(B, True):
        kmg__ojl = 'if bodo.libs.array_kernels.isna(B, i) and arg0 != 0:\n'
        kmg__ojl += '   res[i] = True\n'
        kmg__ojl += 'elif bodo.libs.array_kernels.isna(B, i) and arg0 == 0:\n'
        kmg__ojl += '   bodo.libs.array_kernels.setna(res, i)\n'
        kmg__ojl += 'else:\n'
        kmg__ojl += '   res[i] = (arg0 != 0) or (arg1 != 0)'
    else:
        kmg__ojl = 'res[i] = (arg0 != 0) or (arg1 != 0)'
    dnvk__kpus = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(bxuu__gyjj, shrss__oyuxc, pbda__fls, kmg__ojl,
        dnvk__kpus)


@numba.generated_jit(nopython=True)
def boolxor_util(A, B):
    verify_int_float_arg(A, 'BOOLXOR', 'A')
    verify_int_float_arg(B, 'BOOLXOR', 'B')
    bxuu__gyjj = ['A', 'B']
    shrss__oyuxc = [A, B]
    pbda__fls = [True] * 2
    kmg__ojl = 'res[i] = (arg0 == 0) != (arg1 == 0)'
    dnvk__kpus = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(bxuu__gyjj, shrss__oyuxc, pbda__fls, kmg__ojl,
        dnvk__kpus)


@numba.generated_jit(nopython=True)
def boolnot_util(A):
    verify_int_float_arg(A, 'BOOLNOT', 'A')
    bxuu__gyjj = ['A']
    shrss__oyuxc = [A]
    pbda__fls = [True]
    kmg__ojl = 'res[i] = arg0 == 0'
    dnvk__kpus = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(bxuu__gyjj, shrss__oyuxc, pbda__fls, kmg__ojl,
        dnvk__kpus)


@numba.generated_jit(nopython=True)
def nullif(arr0, arr1):
    args = [arr0, arr1]
    for imlox__dxdaz in range(2):
        if isinstance(args[imlox__dxdaz], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.nullif',
                ['arr0', 'arr1'], imlox__dxdaz)

    def impl(arr0, arr1):
        return nullif_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def regr_valx(y, x):
    args = [y, x]
    for imlox__dxdaz in range(2):
        if isinstance(args[imlox__dxdaz], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regr_valx',
                ['y', 'x'], imlox__dxdaz)

    def impl(y, x):
        return regr_valx_util(y, x)
    return impl


@numba.generated_jit(nopython=True)
def regr_valy(y, x):
    args = [y, x]
    for imlox__dxdaz in range(2):
        if isinstance(args[imlox__dxdaz], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regr_valy',
                ['y', 'x'], imlox__dxdaz)

    def impl(y, x):
        return regr_valx(x, y)
    return impl


@numba.generated_jit(nopython=True)
def cond_util(arr, ifbranch, elsebranch):
    verify_boolean_arg(arr, 'cond', 'arr')
    if bodo.utils.utils.is_array_typ(arr, True
        ) and ifbranch == bodo.none and elsebranch == bodo.none:
        raise_bodo_error('Both branches of IF() cannot be scalar NULL')
    bxuu__gyjj = ['arr', 'ifbranch', 'elsebranch']
    shrss__oyuxc = [arr, ifbranch, elsebranch]
    pbda__fls = [False] * 3
    if bodo.utils.utils.is_array_typ(arr, True):
        kmg__ojl = 'if (not bodo.libs.array_kernels.isna(arr, i)) and arg0:\n'
    elif arr != bodo.none:
        kmg__ojl = 'if arg0:\n'
    else:
        kmg__ojl = ''
    if arr != bodo.none:
        if bodo.utils.utils.is_array_typ(ifbranch, True):
            kmg__ojl += '   if bodo.libs.array_kernels.isna(ifbranch, i):\n'
            kmg__ojl += '      bodo.libs.array_kernels.setna(res, i)\n'
            kmg__ojl += '   else:\n'
            kmg__ojl += '      res[i] = arg1\n'
        elif ifbranch == bodo.none:
            kmg__ojl += '   bodo.libs.array_kernels.setna(res, i)\n'
        else:
            kmg__ojl += '   res[i] = arg1\n'
        kmg__ojl += 'else:\n'
    if bodo.utils.utils.is_array_typ(elsebranch, True):
        kmg__ojl += '   if bodo.libs.array_kernels.isna(elsebranch, i):\n'
        kmg__ojl += '      bodo.libs.array_kernels.setna(res, i)\n'
        kmg__ojl += '   else:\n'
        kmg__ojl += '      res[i] = arg2\n'
    elif elsebranch == bodo.none:
        kmg__ojl += '   bodo.libs.array_kernels.setna(res, i)\n'
    else:
        kmg__ojl += '   res[i] = arg2\n'
    dnvk__kpus = get_common_broadcasted_type([ifbranch, elsebranch], 'IF')
    return gen_vectorized(bxuu__gyjj, shrss__oyuxc, pbda__fls, kmg__ojl,
        dnvk__kpus)


@numba.generated_jit(nopython=True)
def equal_null_util(A, B):
    get_common_broadcasted_type([A, B], 'EQUAL_NULL')
    bxuu__gyjj = ['A', 'B']
    shrss__oyuxc = [A, B]
    pbda__fls = [False] * 2
    if A == bodo.none:
        if B == bodo.none:
            kmg__ojl = 'res[i] = True'
        elif bodo.utils.utils.is_array_typ(B, True):
            kmg__ojl = 'res[i] = bodo.libs.array_kernels.isna(B, i)'
        else:
            kmg__ojl = 'res[i] = False'
    elif B == bodo.none:
        if bodo.utils.utils.is_array_typ(A, True):
            kmg__ojl = 'res[i] = bodo.libs.array_kernels.isna(A, i)'
        else:
            kmg__ojl = 'res[i] = False'
    elif bodo.utils.utils.is_array_typ(A, True):
        if bodo.utils.utils.is_array_typ(B, True):
            kmg__ojl = """if bodo.libs.array_kernels.isna(A, i) and bodo.libs.array_kernels.isna(B, i):
"""
            kmg__ojl += '   res[i] = True\n'
            kmg__ojl += """elif bodo.libs.array_kernels.isna(A, i) or bodo.libs.array_kernels.isna(B, i):
"""
            kmg__ojl += '   res[i] = False\n'
            kmg__ojl += 'else:\n'
            kmg__ojl += '   res[i] = arg0 == arg1'
        else:
            kmg__ojl = (
                'res[i] = (not bodo.libs.array_kernels.isna(A, i)) and arg0 == arg1'
                )
    elif bodo.utils.utils.is_array_typ(B, True):
        kmg__ojl = (
            'res[i] = (not bodo.libs.array_kernels.isna(B, i)) and arg0 == arg1'
            )
    else:
        kmg__ojl = 'res[i] = arg0 == arg1'
    dnvk__kpus = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(bxuu__gyjj, shrss__oyuxc, pbda__fls, kmg__ojl,
        dnvk__kpus)


@numba.generated_jit(nopython=True)
def nullif_util(arr0, arr1):
    bxuu__gyjj = ['arr0', 'arr1']
    shrss__oyuxc = [arr0, arr1]
    pbda__fls = [True, False]
    if arr1 == bodo.none:
        kmg__ojl = 'res[i] = arg0\n'
    elif bodo.utils.utils.is_array_typ(arr1, True):
        kmg__ojl = (
            'if bodo.libs.array_kernels.isna(arr1, i) or arg0 != arg1:\n')
        kmg__ojl += '   res[i] = arg0\n'
        kmg__ojl += 'else:\n'
        kmg__ojl += '   bodo.libs.array_kernels.setna(res, i)'
    else:
        kmg__ojl = 'if arg0 != arg1:\n'
        kmg__ojl += '   res[i] = arg0\n'
        kmg__ojl += 'else:\n'
        kmg__ojl += '   bodo.libs.array_kernels.setna(res, i)'
    dnvk__kpus = get_common_broadcasted_type([arr0, arr1], 'NULLIF')
    return gen_vectorized(bxuu__gyjj, shrss__oyuxc, pbda__fls, kmg__ojl,
        dnvk__kpus)


@numba.generated_jit(nopython=True)
def regr_valx_util(y, x):
    verify_int_float_arg(y, 'regr_valx', 'y')
    verify_int_float_arg(x, 'regr_valx', 'x')
    bxuu__gyjj = ['y', 'x']
    shrss__oyuxc = [y, x]
    sjgmd__eqow = [True] * 2
    kmg__ojl = 'res[i] = arg1'
    dnvk__kpus = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(bxuu__gyjj, shrss__oyuxc, sjgmd__eqow, kmg__ojl,
        dnvk__kpus)
