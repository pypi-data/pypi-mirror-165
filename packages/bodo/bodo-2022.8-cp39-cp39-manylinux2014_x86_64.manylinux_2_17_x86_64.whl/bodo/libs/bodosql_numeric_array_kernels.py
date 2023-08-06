"""
Implements numerical array kernels that are specific to BodoSQL
"""
import numba
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.utils import is_array_typ


def cbrt(arr):
    return


def ceil(arr):
    return


def factorial(arr):
    return


def floor(arr):
    return


def mod(arr0, arr1):
    return


def sign(arr):
    return


def sqrt(arr):
    return


def round(arr0, arr1):
    return


def trunc(arr0, arr1):
    return


def abs(arr):
    return


def ln(arr):
    return


def log2(arr):
    return


def log10(arr):
    return


def exp(arr):
    return


def power(arr0, arr1):
    return


def sqrt_util(arr):
    return


def square(arr):
    return


def cbrt_util(arr):
    return


def ceil_util(arr):
    return


def factorial_util(arr):
    return


def floor_util(arr):
    return


def mod_util(arr0, arr1):
    return


def sign_util(arr):
    return


def round_util(arr0, arr1):
    return


def trunc_util(arr0, arr1):
    return


def abs_util(arr):
    return


def ln_util(arr):
    return


def log2_util(arr):
    return


def log10_util(arr):
    return


def exp_util(arr):
    return


def power_util(arr0, arr1):
    return


def square_util(arr):
    return


funcs_utils_names = (abs, abs_util, 'ABS'), (cbrt, cbrt_util, 'CBRT'), (ceil,
    ceil_util, 'CEIL'), (factorial, factorial_util, 'FACTORIAL'), (floor,
    floor_util, 'FLOOR'), (ln, ln_util, 'LN'), (log2, log2_util, 'LOG2'), (
    log10, log10_util, 'LOG10'), (mod, mod_util, 'MOD'), (sign, sign_util,
    'SIGN'), (round, round_util, 'ROUND'), (trunc, trunc_util, 'TRUNC'), (exp,
    exp_util, 'EXP'), (power, power_util, 'POWER'), (sqrt, sqrt_util, 'SQRT'
    ), (square, square_util, 'SQUARE')
double_arg_funcs = 'MOD', 'TRUNC', 'POWER', 'ROUND'
single_arg_funcs = set(a[2] for a in funcs_utils_names if a[2] not in
    double_arg_funcs)
_float = {(16): types.float16, (32): types.float32, (64): types.float64}
_int = {(8): types.int8, (16): types.int16, (32): types.int32, (64): types.
    int64}
_uint = {(8): types.uint8, (16): types.uint16, (32): types.uint32, (64):
    types.uint64}


def _get_numeric_output_dtype(func_name, arr0, arr1=None):
    lnyc__hcq = arr0.dtype if is_array_typ(arr0) else arr0
    uvkfs__ytyq = arr1.dtype if is_array_typ(arr1) else arr1
    uehe__abs = bodo.float64
    if (arr0 is None or lnyc__hcq == bodo.none
        ) or func_name in double_arg_funcs and (arr1 is None or uvkfs__ytyq ==
        bodo.none):
        return types.Array(uehe__abs, 1, 'C')
    if isinstance(lnyc__hcq, types.Float):
        if isinstance(uvkfs__ytyq, types.Float):
            uehe__abs = _float[max(lnyc__hcq.bitwidth, uvkfs__ytyq.bitwidth)]
        else:
            uehe__abs = lnyc__hcq
    if func_name == 'SIGN':
        if isinstance(lnyc__hcq, types.Integer):
            uehe__abs = lnyc__hcq
    elif func_name == 'MOD':
        if isinstance(lnyc__hcq, types.Integer) and isinstance(uvkfs__ytyq,
            types.Integer):
            if lnyc__hcq.signed:
                if uvkfs__ytyq.signed:
                    uehe__abs = uvkfs__ytyq
                else:
                    uehe__abs = _int[min(64, uvkfs__ytyq.bitwidth * 2)]
            else:
                uehe__abs = uvkfs__ytyq
    elif func_name == 'ABS':
        if isinstance(lnyc__hcq, types.Integer):
            if lnyc__hcq.signed:
                uehe__abs = _uint[min(64, lnyc__hcq.bitwidth * 2)]
            else:
                uehe__abs = lnyc__hcq
    elif func_name == 'ROUND':
        if isinstance(lnyc__hcq, (types.Float, types.Integer)):
            uehe__abs = lnyc__hcq
    elif func_name == 'FACTORIAL':
        uehe__abs = bodo.int64
    if isinstance(uehe__abs, types.Integer):
        return bodo.libs.int_arr_ext.IntegerArrayType(uehe__abs)
    else:
        return types.Array(uehe__abs, 1, 'C')


def create_numeric_func_overload(func_name):
    if func_name not in double_arg_funcs:
        func_name = func_name.lower()

        def overload_func(arr):
            if isinstance(arr, types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.{func_name}', ['arr'], 0)
            cdkq__xsacf = 'def impl(arr):\n'
            cdkq__xsacf += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr)'
                )
            shr__nbgl = {}
            exec(cdkq__xsacf, {'bodo': bodo}, shr__nbgl)
            return shr__nbgl['impl']
    else:
        func_name = func_name.lower()

        def overload_func(arr0, arr1):
            args = [arr0, arr1]
            for xcnsn__nldt in range(2):
                if isinstance(args[xcnsn__nldt], types.optional):
                    return unopt_argument(
                        f'bodo.libs.bodosql_array_kernels.{func_name}', [
                        'arr0', 'arr1'], xcnsn__nldt)
            cdkq__xsacf = 'def impl(arr0, arr1):\n'
            cdkq__xsacf += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr0, arr1)'
                )
            shr__nbgl = {}
            exec(cdkq__xsacf, {'bodo': bodo}, shr__nbgl)
            return shr__nbgl['impl']
    return overload_func


def create_numeric_util_overload(func_name):
    if func_name not in double_arg_funcs:

        def overload_numeric_util(arr):
            verify_int_float_arg(arr, func_name, 'arr')
            rlrm__sggm = ['arr']
            ppj__rrhsj = [arr]
            cynr__zbh = [True]
            xrj__znrl = ''
            if func_name in single_arg_funcs:
                if func_name == 'FACTORIAL':
                    xrj__znrl += (
                        'if arg0 > 20 or np.abs(np.int64(arg0)) != arg0:\n')
                    xrj__znrl += '  bodo.libs.array_kernels.setna(res, i)\n'
                    xrj__znrl += 'else:\n'
                    xrj__znrl += (
                        f'  res[i] = np.math.factorial(np.int64(arg0))')
                elif func_name == 'LN':
                    xrj__znrl += f'res[i] = np.log(arg0)'
                else:
                    xrj__znrl += f'res[i] = np.{func_name.lower()}(arg0)'
            else:
                ValueError(f'Unknown function name: {func_name}')
            uehe__abs = _get_numeric_output_dtype(func_name, arr)
            return gen_vectorized(rlrm__sggm, ppj__rrhsj, cynr__zbh,
                xrj__znrl, uehe__abs)
    else:

        def overload_numeric_util(arr0, arr1):
            verify_int_float_arg(arr0, func_name, 'arr0')
            verify_int_float_arg(arr0, func_name, 'arr1')
            rlrm__sggm = ['arr0', 'arr1']
            ppj__rrhsj = [arr0, arr1]
            cynr__zbh = [True, True]
            xrj__znrl = ''
            if func_name == 'MOD':
                xrj__znrl += 'if arg1 == 0:\n'
                xrj__znrl += '  bodo.libs.array_kernels.setna(res, i)\n'
                xrj__znrl += 'val = np.mod(arg0, arg1)\n'
                xrj__znrl += 'if val < 0 and arg0 > 0:\n'
                xrj__znrl += '  res[i] = val + arg1\n'
                xrj__znrl += 'elif val > 0 and arg0 < 0:\n'
                xrj__znrl += '  res[i] = val - arg1\n'
                xrj__znrl += 'else:\n'
                xrj__znrl += '  res[i] = val'
            elif func_name == 'POWER':
                xrj__znrl += 'res[i] = np.power(np.float64(arg0), arg1)'
            elif func_name == 'ROUND':
                xrj__znrl += 'res[i] = np.round(arg0, arg1)'
            elif func_name == 'TRUNC':
                xrj__znrl += 'if int(arg1) == arg1:\n'
                xrj__znrl += (
                    '  res[i] = np.trunc(arg0 * (10.0 ** arg1)) * (10.0 ** -arg1)\n'
                    )
                xrj__znrl += 'else:\n'
                xrj__znrl += '  bodo.libs.array_kernels.setna(res, i)'
            else:
                raise ValueError(f'Unknown function name: {func_name}')
            uehe__abs = _get_numeric_output_dtype(func_name, arr0, arr1)
            return gen_vectorized(rlrm__sggm, ppj__rrhsj, cynr__zbh,
                xrj__znrl, uehe__abs)
    return overload_numeric_util


def _install_numeric_overload(funcs_utils_names):
    for tia__tsyx, lyu__ngasa, func_name in funcs_utils_names:
        qsq__uxzpw = create_numeric_func_overload(func_name)
        overload(tia__tsyx)(qsq__uxzpw)
        uejz__rqn = create_numeric_util_overload(func_name)
        overload(lyu__ngasa)(uejz__rqn)


_install_numeric_overload(funcs_utils_names)


@numba.generated_jit(nopython=True)
def bitand(A, B):
    args = [A, B]
    for xcnsn__nldt in range(2):
        if isinstance(args[xcnsn__nldt], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitand',
                ['A', 'B'], xcnsn__nldt)

    def impl(A, B):
        return bitand_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitshiftleft(A, B):
    args = [A, B]
    for xcnsn__nldt in range(2):
        if isinstance(args[xcnsn__nldt], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.bitshiftleft', ['A', 'B'],
                xcnsn__nldt)

    def impl(A, B):
        return bitshiftleft_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitnot(A):
    if isinstance(A, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.bitnot_util',
            ['A'], 0)

    def impl(A):
        return bitnot_util(A)
    return impl


@numba.generated_jit(nopython=True)
def bitor(A, B):
    args = [A, B]
    for xcnsn__nldt in range(2):
        if isinstance(args[xcnsn__nldt], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitor',
                ['A', 'B'], xcnsn__nldt)

    def impl(A, B):
        return bitor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitshiftright(A, B):
    args = [A, B]
    for xcnsn__nldt in range(2):
        if isinstance(args[xcnsn__nldt], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.bitshiftright', ['A', 'B'],
                xcnsn__nldt)

    def impl(A, B):
        return bitshiftright_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitxor(A, B):
    args = [A, B]
    for xcnsn__nldt in range(2):
        if isinstance(args[xcnsn__nldt], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitxor',
                ['A', 'B'], xcnsn__nldt)

    def impl(A, B):
        return bitxor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def conv(arr, old_base, new_base):
    args = [arr, old_base, new_base]
    for xcnsn__nldt in range(3):
        if isinstance(args[xcnsn__nldt], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.conv', [
                'arr', 'old_base', 'new_base'], xcnsn__nldt)

    def impl(arr, old_base, new_base):
        return conv_util(arr, old_base, new_base)
    return impl


@numba.generated_jit(nopython=True)
def getbit(A, B):
    args = [A, B]
    for xcnsn__nldt in range(2):
        if isinstance(args[xcnsn__nldt], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.getbit',
                ['A', 'B'], xcnsn__nldt)

    def impl(A, B):
        return getbit_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def haversine(lat1, lon1, lat2, lon2):
    args = [lat1, lon1, lat2, lon2]
    for xcnsn__nldt in range(4):
        if isinstance(args[xcnsn__nldt], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.haversine',
                ['lat1', 'lon1', 'lat2', 'lon2'], xcnsn__nldt)

    def impl(lat1, lon1, lat2, lon2):
        return haversine_util(lat1, lon1, lat2, lon2)
    return impl


@numba.generated_jit(nopython=True)
def div0(arr, divisor):
    args = [arr, divisor]
    for xcnsn__nldt in range(2):
        if isinstance(args[xcnsn__nldt], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.div0', [
                'arr', 'divisor'], xcnsn__nldt)

    def impl(arr, divisor):
        return div0_util(arr, divisor)
    return impl


@numba.generated_jit(nopython=True)
def log(arr, base):
    args = [arr, base]
    for xcnsn__nldt in range(2):
        if isinstance(args[xcnsn__nldt], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.log', [
                'arr', 'base'], xcnsn__nldt)

    def impl(arr, base):
        return log_util(arr, base)
    return impl


@numba.generated_jit(nopython=True)
def negate(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.negate_util',
            ['arr'], 0)

    def impl(arr):
        return negate_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def width_bucket(arr, min_val, max_val, num_buckets):
    args = [arr, min_val, max_val, num_buckets]
    for xcnsn__nldt in range(4):
        if isinstance(args[xcnsn__nldt], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.width_bucket', ['arr',
                'min_val', 'max_val', 'num_buckets'], xcnsn__nldt)

    def impl(arr, min_val, max_val, num_buckets):
        return width_bucket_util(arr, min_val, max_val, num_buckets)
    return impl


@numba.generated_jit(nopython=True)
def bitand_util(A, B):
    verify_int_arg(A, 'bitand', 'A')
    verify_int_arg(B, 'bitand', 'B')
    rlrm__sggm = ['A', 'B']
    ppj__rrhsj = [A, B]
    cynr__zbh = [True] * 2
    xrj__znrl = 'res[i] = arg0 & arg1'
    uehe__abs = get_common_broadcasted_type([A, B], 'bitand')
    return gen_vectorized(rlrm__sggm, ppj__rrhsj, cynr__zbh, xrj__znrl,
        uehe__abs)


@numba.generated_jit(nopython=True)
def bitshiftleft_util(A, B):
    verify_int_arg(A, 'bitshiftleft', 'A')
    verify_int_arg(B, 'bitshiftleft', 'B')
    rlrm__sggm = ['A', 'B']
    ppj__rrhsj = [A, B]
    cynr__zbh = [True] * 2
    xrj__znrl = 'res[i] = arg0 << arg1'
    uehe__abs = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_vectorized(rlrm__sggm, ppj__rrhsj, cynr__zbh, xrj__znrl,
        uehe__abs)


@numba.generated_jit(nopython=True)
def bitnot_util(A):
    verify_int_arg(A, 'bitnot', 'A')
    rlrm__sggm = ['A']
    ppj__rrhsj = [A]
    cynr__zbh = [True]
    xrj__znrl = 'res[i] = ~arg0'
    if A == bodo.none:
        uehe__abs = bodo.none
    else:
        if bodo.utils.utils.is_array_typ(A, True):
            tevh__tixm = A.dtype
        else:
            tevh__tixm = A
        uehe__abs = bodo.libs.int_arr_ext.IntegerArrayType(tevh__tixm)
    return gen_vectorized(rlrm__sggm, ppj__rrhsj, cynr__zbh, xrj__znrl,
        uehe__abs)


@numba.generated_jit(nopython=True)
def bitor_util(A, B):
    verify_int_arg(A, 'bitor', 'A')
    verify_int_arg(B, 'bitor', 'B')
    rlrm__sggm = ['A', 'B']
    ppj__rrhsj = [A, B]
    cynr__zbh = [True] * 2
    xrj__znrl = 'res[i] = arg0 | arg1'
    uehe__abs = get_common_broadcasted_type([A, B], 'bitor')
    return gen_vectorized(rlrm__sggm, ppj__rrhsj, cynr__zbh, xrj__znrl,
        uehe__abs)


@numba.generated_jit(nopython=True)
def bitshiftright_util(A, B):
    verify_int_arg(A, 'bitshiftright', 'A')
    verify_int_arg(B, 'bitshiftright', 'B')
    rlrm__sggm = ['A', 'B']
    ppj__rrhsj = [A, B]
    cynr__zbh = [True] * 2
    if A == bodo.none:
        tevh__tixm = uehe__abs = bodo.none
    else:
        if bodo.utils.utils.is_array_typ(A, True):
            tevh__tixm = A.dtype
        else:
            tevh__tixm = A
        uehe__abs = bodo.libs.int_arr_ext.IntegerArrayType(tevh__tixm)
    xrj__znrl = f'res[i] = arg0 >> arg1\n'
    return gen_vectorized(rlrm__sggm, ppj__rrhsj, cynr__zbh, xrj__znrl,
        uehe__abs)


@numba.generated_jit(nopython=True)
def bitxor_util(A, B):
    verify_int_arg(A, 'bitxor', 'A')
    verify_int_arg(B, 'bitxor', 'B')
    rlrm__sggm = ['A', 'B']
    ppj__rrhsj = [A, B]
    cynr__zbh = [True] * 2
    xrj__znrl = 'res[i] = arg0 ^ arg1'
    uehe__abs = get_common_broadcasted_type([A, B], 'bitxor')
    return gen_vectorized(rlrm__sggm, ppj__rrhsj, cynr__zbh, xrj__znrl,
        uehe__abs)


@numba.generated_jit(nopython=True)
def conv_util(arr, old_base, new_base):
    verify_string_arg(arr, 'CONV', 'arr')
    verify_int_arg(old_base, 'CONV', 'old_base')
    verify_int_arg(new_base, 'CONV', 'new_base')
    rlrm__sggm = ['arr', 'old_base', 'new_base']
    ppj__rrhsj = [arr, old_base, new_base]
    cynr__zbh = [True] * 3
    xrj__znrl = 'old_val = int(arg0, arg1)\n'
    xrj__znrl += 'if arg2 == 2:\n'
    xrj__znrl += "   res[i] = format(old_val, 'b')\n"
    xrj__znrl += 'elif arg2 == 8:\n'
    xrj__znrl += "   res[i] = format(old_val, 'o')\n"
    xrj__znrl += 'elif arg2 == 10:\n'
    xrj__znrl += "   res[i] = format(old_val, 'd')\n"
    xrj__znrl += 'elif arg2 == 16:\n'
    xrj__znrl += "   res[i] = format(old_val, 'x')\n"
    xrj__znrl += 'else:\n'
    xrj__znrl += '   bodo.libs.array_kernels.setna(res, i)\n'
    uehe__abs = bodo.string_array_type
    return gen_vectorized(rlrm__sggm, ppj__rrhsj, cynr__zbh, xrj__znrl,
        uehe__abs)


@numba.generated_jit(nopython=True)
def getbit_util(A, B):
    verify_int_arg(A, 'bitshiftright', 'A')
    verify_int_arg(B, 'bitshiftright', 'B')
    rlrm__sggm = ['A', 'B']
    ppj__rrhsj = [A, B]
    cynr__zbh = [True] * 2
    xrj__znrl = 'res[i] = (arg0 >> arg1) & 1'
    uehe__abs = bodo.libs.int_arr_ext.IntegerArrayType(types.uint8)
    return gen_vectorized(rlrm__sggm, ppj__rrhsj, cynr__zbh, xrj__znrl,
        uehe__abs)


@numba.generated_jit(nopython=True)
def haversine_util(lat1, lon1, lat2, lon2):
    verify_int_float_arg(lat1, 'HAVERSINE', 'lat1')
    verify_int_float_arg(lon1, 'HAVERSINE', 'lon1')
    verify_int_float_arg(lat2, 'HAVERSINE', 'lat2')
    verify_int_float_arg(lon2, 'HAVERSINE', 'lon2')
    rlrm__sggm = ['lat1', 'lon1', 'lat2', 'lon2']
    ppj__rrhsj = [lat1, lon1, lat2, lon2]
    bloie__glph = [True] * 4
    xrj__znrl = (
        'arg0, arg1, arg2, arg3 = map(np.radians, (arg0, arg1, arg2, arg3))\n')
    fsj__kzhp = '(arg2 - arg0) * 0.5'
    vte__myr = '(arg3 - arg1) * 0.5'
    hmaz__dfy = (
        f'np.square(np.sin({fsj__kzhp})) + (np.cos(arg0) * np.cos(arg2) * np.square(np.sin({vte__myr})))'
        )
    xrj__znrl += f'res[i] = 12742.0 * np.arcsin(np.sqrt({hmaz__dfy}))\n'
    uehe__abs = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(rlrm__sggm, ppj__rrhsj, bloie__glph, xrj__znrl,
        uehe__abs)


@numba.generated_jit(nopython=True)
def div0_util(arr, divisor):
    verify_int_float_arg(arr, 'DIV0', 'arr')
    verify_int_float_arg(divisor, 'DIV0', 'divisor')
    rlrm__sggm = ['arr', 'divisor']
    ppj__rrhsj = [arr, divisor]
    bloie__glph = [True] * 2
    xrj__znrl = 'res[i] = arg0 / arg1 if arg1 else 0\n'
    uehe__abs = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(rlrm__sggm, ppj__rrhsj, bloie__glph, xrj__znrl,
        uehe__abs)


@numba.generated_jit(nopython=True)
def log_util(arr, base):
    verify_int_float_arg(arr, 'log', 'arr')
    verify_int_float_arg(base, 'log', 'base')
    rlrm__sggm = ['arr', 'base']
    ppj__rrhsj = [arr, base]
    cynr__zbh = [True] * 2
    xrj__znrl = 'res[i] = np.log(arg0) / np.log(arg1)'
    uehe__abs = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(rlrm__sggm, ppj__rrhsj, cynr__zbh, xrj__znrl,
        uehe__abs)


@numba.generated_jit(nopython=True)
def negate_util(arr):
    verify_int_float_arg(arr, 'negate', 'arr')
    rlrm__sggm = ['arr']
    ppj__rrhsj = [arr]
    cynr__zbh = [True]
    if arr == bodo.none:
        tevh__tixm = types.int32
    elif bodo.utils.utils.is_array_typ(arr, False):
        tevh__tixm = arr.dtype
    elif bodo.utils.utils.is_array_typ(arr, True):
        tevh__tixm = arr.data.dtype
    else:
        tevh__tixm = arr
    xrj__znrl = {types.uint8: 'res[i] = -np.int16(arg0)', types.uint16:
        'res[i] = -np.int32(arg0)', types.uint32: 'res[i] = -np.int64(arg0)'
        }.get(tevh__tixm, 'res[i] = -arg0')
    tevh__tixm = {types.uint8: types.int16, types.uint16: types.int32,
        types.uint32: types.int64, types.uint64: types.int64}.get(tevh__tixm,
        tevh__tixm)
    uehe__abs = bodo.utils.typing.to_nullable_type(bodo.utils.typing.
        dtype_to_array_type(tevh__tixm))
    return gen_vectorized(rlrm__sggm, ppj__rrhsj, cynr__zbh, xrj__znrl,
        uehe__abs)


@numba.generated_jit(nopython=True)
def width_bucket_util(arr, min_val, max_val, num_buckets):
    verify_int_float_arg(arr, 'WIDTH_BUCKET', 'arr')
    verify_int_float_arg(min_val, 'WIDTH_BUCKET', 'min_val')
    verify_int_float_arg(max_val, 'WIDTH_BUCKET', 'max_val')
    verify_int_arg(num_buckets, 'WIDTH_BUCKET', 'num_buckets')
    rlrm__sggm = ['arr', 'min_val', 'max_val', 'num_buckets']
    ppj__rrhsj = [arr, min_val, max_val, num_buckets]
    cynr__zbh = [True] * 4
    xrj__znrl = (
        "if arg1 >= arg2: raise ValueError('min_val must be less than max_val')\n"
        )
    xrj__znrl += (
        "if arg3 <= 0: raise ValueError('num_buckets must be a positive integer')\n"
        )
    xrj__znrl += (
        'res[i] = min(max(-1.0, math.floor((arg0 - arg1) / ((arg2 - arg1) / arg3))), arg3) + 1.0'
        )
    uehe__abs = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_vectorized(rlrm__sggm, ppj__rrhsj, cynr__zbh, xrj__znrl,
        uehe__abs)
