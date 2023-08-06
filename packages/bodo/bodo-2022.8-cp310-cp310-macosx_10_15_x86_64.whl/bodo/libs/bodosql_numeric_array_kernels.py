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
    xbs__lhnaz = arr0.dtype if is_array_typ(arr0) else arr0
    zux__raq = arr1.dtype if is_array_typ(arr1) else arr1
    vboq__cep = bodo.float64
    if (arr0 is None or xbs__lhnaz == bodo.none
        ) or func_name in double_arg_funcs and (arr1 is None or zux__raq ==
        bodo.none):
        return types.Array(vboq__cep, 1, 'C')
    if isinstance(xbs__lhnaz, types.Float):
        if isinstance(zux__raq, types.Float):
            vboq__cep = _float[max(xbs__lhnaz.bitwidth, zux__raq.bitwidth)]
        else:
            vboq__cep = xbs__lhnaz
    if func_name == 'SIGN':
        if isinstance(xbs__lhnaz, types.Integer):
            vboq__cep = xbs__lhnaz
    elif func_name == 'MOD':
        if isinstance(xbs__lhnaz, types.Integer) and isinstance(zux__raq,
            types.Integer):
            if xbs__lhnaz.signed:
                if zux__raq.signed:
                    vboq__cep = zux__raq
                else:
                    vboq__cep = _int[min(64, zux__raq.bitwidth * 2)]
            else:
                vboq__cep = zux__raq
    elif func_name == 'ABS':
        if isinstance(xbs__lhnaz, types.Integer):
            if xbs__lhnaz.signed:
                vboq__cep = _uint[min(64, xbs__lhnaz.bitwidth * 2)]
            else:
                vboq__cep = xbs__lhnaz
    elif func_name == 'ROUND':
        if isinstance(xbs__lhnaz, (types.Float, types.Integer)):
            vboq__cep = xbs__lhnaz
    elif func_name == 'FACTORIAL':
        vboq__cep = bodo.int64
    if isinstance(vboq__cep, types.Integer):
        return bodo.libs.int_arr_ext.IntegerArrayType(vboq__cep)
    else:
        return types.Array(vboq__cep, 1, 'C')


def create_numeric_func_overload(func_name):
    if func_name not in double_arg_funcs:
        func_name = func_name.lower()

        def overload_func(arr):
            if isinstance(arr, types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.{func_name}', ['arr'], 0)
            mkqqu__iika = 'def impl(arr):\n'
            mkqqu__iika += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr)'
                )
            kvf__asb = {}
            exec(mkqqu__iika, {'bodo': bodo}, kvf__asb)
            return kvf__asb['impl']
    else:
        func_name = func_name.lower()

        def overload_func(arr0, arr1):
            args = [arr0, arr1]
            for agcc__beqpp in range(2):
                if isinstance(args[agcc__beqpp], types.optional):
                    return unopt_argument(
                        f'bodo.libs.bodosql_array_kernels.{func_name}', [
                        'arr0', 'arr1'], agcc__beqpp)
            mkqqu__iika = 'def impl(arr0, arr1):\n'
            mkqqu__iika += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr0, arr1)'
                )
            kvf__asb = {}
            exec(mkqqu__iika, {'bodo': bodo}, kvf__asb)
            return kvf__asb['impl']
    return overload_func


def create_numeric_util_overload(func_name):
    if func_name not in double_arg_funcs:

        def overload_numeric_util(arr):
            verify_int_float_arg(arr, func_name, 'arr')
            azw__aeh = ['arr']
            ldykt__itayn = [arr]
            xsssc__qtpt = [True]
            gwqr__kuuvg = ''
            if func_name in single_arg_funcs:
                if func_name == 'FACTORIAL':
                    gwqr__kuuvg += (
                        'if arg0 > 20 or np.abs(np.int64(arg0)) != arg0:\n')
                    gwqr__kuuvg += '  bodo.libs.array_kernels.setna(res, i)\n'
                    gwqr__kuuvg += 'else:\n'
                    gwqr__kuuvg += (
                        f'  res[i] = np.math.factorial(np.int64(arg0))')
                elif func_name == 'LN':
                    gwqr__kuuvg += f'res[i] = np.log(arg0)'
                else:
                    gwqr__kuuvg += f'res[i] = np.{func_name.lower()}(arg0)'
            else:
                ValueError(f'Unknown function name: {func_name}')
            vboq__cep = _get_numeric_output_dtype(func_name, arr)
            return gen_vectorized(azw__aeh, ldykt__itayn, xsssc__qtpt,
                gwqr__kuuvg, vboq__cep)
    else:

        def overload_numeric_util(arr0, arr1):
            verify_int_float_arg(arr0, func_name, 'arr0')
            verify_int_float_arg(arr0, func_name, 'arr1')
            azw__aeh = ['arr0', 'arr1']
            ldykt__itayn = [arr0, arr1]
            xsssc__qtpt = [True, True]
            gwqr__kuuvg = ''
            if func_name == 'MOD':
                gwqr__kuuvg += 'if arg1 == 0:\n'
                gwqr__kuuvg += '  bodo.libs.array_kernels.setna(res, i)\n'
                gwqr__kuuvg += 'val = np.mod(arg0, arg1)\n'
                gwqr__kuuvg += 'if val < 0 and arg0 > 0:\n'
                gwqr__kuuvg += '  res[i] = val + arg1\n'
                gwqr__kuuvg += 'elif val > 0 and arg0 < 0:\n'
                gwqr__kuuvg += '  res[i] = val - arg1\n'
                gwqr__kuuvg += 'else:\n'
                gwqr__kuuvg += '  res[i] = val'
            elif func_name == 'POWER':
                gwqr__kuuvg += 'res[i] = np.power(np.float64(arg0), arg1)'
            elif func_name == 'ROUND':
                gwqr__kuuvg += 'res[i] = np.round(arg0, arg1)'
            elif func_name == 'TRUNC':
                gwqr__kuuvg += 'if int(arg1) == arg1:\n'
                gwqr__kuuvg += (
                    '  res[i] = np.trunc(arg0 * (10.0 ** arg1)) * (10.0 ** -arg1)\n'
                    )
                gwqr__kuuvg += 'else:\n'
                gwqr__kuuvg += '  bodo.libs.array_kernels.setna(res, i)'
            else:
                raise ValueError(f'Unknown function name: {func_name}')
            vboq__cep = _get_numeric_output_dtype(func_name, arr0, arr1)
            return gen_vectorized(azw__aeh, ldykt__itayn, xsssc__qtpt,
                gwqr__kuuvg, vboq__cep)
    return overload_numeric_util


def _install_numeric_overload(funcs_utils_names):
    for yax__poguy, smh__njjbe, func_name in funcs_utils_names:
        guke__gotex = create_numeric_func_overload(func_name)
        overload(yax__poguy)(guke__gotex)
        waotn__yyue = create_numeric_util_overload(func_name)
        overload(smh__njjbe)(waotn__yyue)


_install_numeric_overload(funcs_utils_names)


@numba.generated_jit(nopython=True)
def bitand(A, B):
    args = [A, B]
    for agcc__beqpp in range(2):
        if isinstance(args[agcc__beqpp], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitand',
                ['A', 'B'], agcc__beqpp)

    def impl(A, B):
        return bitand_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitshiftleft(A, B):
    args = [A, B]
    for agcc__beqpp in range(2):
        if isinstance(args[agcc__beqpp], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.bitshiftleft', ['A', 'B'],
                agcc__beqpp)

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
    for agcc__beqpp in range(2):
        if isinstance(args[agcc__beqpp], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitor',
                ['A', 'B'], agcc__beqpp)

    def impl(A, B):
        return bitor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitshiftright(A, B):
    args = [A, B]
    for agcc__beqpp in range(2):
        if isinstance(args[agcc__beqpp], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.bitshiftright', ['A', 'B'],
                agcc__beqpp)

    def impl(A, B):
        return bitshiftright_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitxor(A, B):
    args = [A, B]
    for agcc__beqpp in range(2):
        if isinstance(args[agcc__beqpp], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitxor',
                ['A', 'B'], agcc__beqpp)

    def impl(A, B):
        return bitxor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def conv(arr, old_base, new_base):
    args = [arr, old_base, new_base]
    for agcc__beqpp in range(3):
        if isinstance(args[agcc__beqpp], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.conv', [
                'arr', 'old_base', 'new_base'], agcc__beqpp)

    def impl(arr, old_base, new_base):
        return conv_util(arr, old_base, new_base)
    return impl


@numba.generated_jit(nopython=True)
def getbit(A, B):
    args = [A, B]
    for agcc__beqpp in range(2):
        if isinstance(args[agcc__beqpp], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.getbit',
                ['A', 'B'], agcc__beqpp)

    def impl(A, B):
        return getbit_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def haversine(lat1, lon1, lat2, lon2):
    args = [lat1, lon1, lat2, lon2]
    for agcc__beqpp in range(4):
        if isinstance(args[agcc__beqpp], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.haversine',
                ['lat1', 'lon1', 'lat2', 'lon2'], agcc__beqpp)

    def impl(lat1, lon1, lat2, lon2):
        return haversine_util(lat1, lon1, lat2, lon2)
    return impl


@numba.generated_jit(nopython=True)
def div0(arr, divisor):
    args = [arr, divisor]
    for agcc__beqpp in range(2):
        if isinstance(args[agcc__beqpp], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.div0', [
                'arr', 'divisor'], agcc__beqpp)

    def impl(arr, divisor):
        return div0_util(arr, divisor)
    return impl


@numba.generated_jit(nopython=True)
def log(arr, base):
    args = [arr, base]
    for agcc__beqpp in range(2):
        if isinstance(args[agcc__beqpp], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.log', [
                'arr', 'base'], agcc__beqpp)

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
    for agcc__beqpp in range(4):
        if isinstance(args[agcc__beqpp], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.width_bucket', ['arr',
                'min_val', 'max_val', 'num_buckets'], agcc__beqpp)

    def impl(arr, min_val, max_val, num_buckets):
        return width_bucket_util(arr, min_val, max_val, num_buckets)
    return impl


@numba.generated_jit(nopython=True)
def bitand_util(A, B):
    verify_int_arg(A, 'bitand', 'A')
    verify_int_arg(B, 'bitand', 'B')
    azw__aeh = ['A', 'B']
    ldykt__itayn = [A, B]
    xsssc__qtpt = [True] * 2
    gwqr__kuuvg = 'res[i] = arg0 & arg1'
    vboq__cep = get_common_broadcasted_type([A, B], 'bitand')
    return gen_vectorized(azw__aeh, ldykt__itayn, xsssc__qtpt, gwqr__kuuvg,
        vboq__cep)


@numba.generated_jit(nopython=True)
def bitshiftleft_util(A, B):
    verify_int_arg(A, 'bitshiftleft', 'A')
    verify_int_arg(B, 'bitshiftleft', 'B')
    azw__aeh = ['A', 'B']
    ldykt__itayn = [A, B]
    xsssc__qtpt = [True] * 2
    gwqr__kuuvg = 'res[i] = arg0 << arg1'
    vboq__cep = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_vectorized(azw__aeh, ldykt__itayn, xsssc__qtpt, gwqr__kuuvg,
        vboq__cep)


@numba.generated_jit(nopython=True)
def bitnot_util(A):
    verify_int_arg(A, 'bitnot', 'A')
    azw__aeh = ['A']
    ldykt__itayn = [A]
    xsssc__qtpt = [True]
    gwqr__kuuvg = 'res[i] = ~arg0'
    if A == bodo.none:
        vboq__cep = bodo.none
    else:
        if bodo.utils.utils.is_array_typ(A, True):
            jwks__fjkxp = A.dtype
        else:
            jwks__fjkxp = A
        vboq__cep = bodo.libs.int_arr_ext.IntegerArrayType(jwks__fjkxp)
    return gen_vectorized(azw__aeh, ldykt__itayn, xsssc__qtpt, gwqr__kuuvg,
        vboq__cep)


@numba.generated_jit(nopython=True)
def bitor_util(A, B):
    verify_int_arg(A, 'bitor', 'A')
    verify_int_arg(B, 'bitor', 'B')
    azw__aeh = ['A', 'B']
    ldykt__itayn = [A, B]
    xsssc__qtpt = [True] * 2
    gwqr__kuuvg = 'res[i] = arg0 | arg1'
    vboq__cep = get_common_broadcasted_type([A, B], 'bitor')
    return gen_vectorized(azw__aeh, ldykt__itayn, xsssc__qtpt, gwqr__kuuvg,
        vboq__cep)


@numba.generated_jit(nopython=True)
def bitshiftright_util(A, B):
    verify_int_arg(A, 'bitshiftright', 'A')
    verify_int_arg(B, 'bitshiftright', 'B')
    azw__aeh = ['A', 'B']
    ldykt__itayn = [A, B]
    xsssc__qtpt = [True] * 2
    if A == bodo.none:
        jwks__fjkxp = vboq__cep = bodo.none
    else:
        if bodo.utils.utils.is_array_typ(A, True):
            jwks__fjkxp = A.dtype
        else:
            jwks__fjkxp = A
        vboq__cep = bodo.libs.int_arr_ext.IntegerArrayType(jwks__fjkxp)
    gwqr__kuuvg = f'res[i] = arg0 >> arg1\n'
    return gen_vectorized(azw__aeh, ldykt__itayn, xsssc__qtpt, gwqr__kuuvg,
        vboq__cep)


@numba.generated_jit(nopython=True)
def bitxor_util(A, B):
    verify_int_arg(A, 'bitxor', 'A')
    verify_int_arg(B, 'bitxor', 'B')
    azw__aeh = ['A', 'B']
    ldykt__itayn = [A, B]
    xsssc__qtpt = [True] * 2
    gwqr__kuuvg = 'res[i] = arg0 ^ arg1'
    vboq__cep = get_common_broadcasted_type([A, B], 'bitxor')
    return gen_vectorized(azw__aeh, ldykt__itayn, xsssc__qtpt, gwqr__kuuvg,
        vboq__cep)


@numba.generated_jit(nopython=True)
def conv_util(arr, old_base, new_base):
    verify_string_arg(arr, 'CONV', 'arr')
    verify_int_arg(old_base, 'CONV', 'old_base')
    verify_int_arg(new_base, 'CONV', 'new_base')
    azw__aeh = ['arr', 'old_base', 'new_base']
    ldykt__itayn = [arr, old_base, new_base]
    xsssc__qtpt = [True] * 3
    gwqr__kuuvg = 'old_val = int(arg0, arg1)\n'
    gwqr__kuuvg += 'if arg2 == 2:\n'
    gwqr__kuuvg += "   res[i] = format(old_val, 'b')\n"
    gwqr__kuuvg += 'elif arg2 == 8:\n'
    gwqr__kuuvg += "   res[i] = format(old_val, 'o')\n"
    gwqr__kuuvg += 'elif arg2 == 10:\n'
    gwqr__kuuvg += "   res[i] = format(old_val, 'd')\n"
    gwqr__kuuvg += 'elif arg2 == 16:\n'
    gwqr__kuuvg += "   res[i] = format(old_val, 'x')\n"
    gwqr__kuuvg += 'else:\n'
    gwqr__kuuvg += '   bodo.libs.array_kernels.setna(res, i)\n'
    vboq__cep = bodo.string_array_type
    return gen_vectorized(azw__aeh, ldykt__itayn, xsssc__qtpt, gwqr__kuuvg,
        vboq__cep)


@numba.generated_jit(nopython=True)
def getbit_util(A, B):
    verify_int_arg(A, 'bitshiftright', 'A')
    verify_int_arg(B, 'bitshiftright', 'B')
    azw__aeh = ['A', 'B']
    ldykt__itayn = [A, B]
    xsssc__qtpt = [True] * 2
    gwqr__kuuvg = 'res[i] = (arg0 >> arg1) & 1'
    vboq__cep = bodo.libs.int_arr_ext.IntegerArrayType(types.uint8)
    return gen_vectorized(azw__aeh, ldykt__itayn, xsssc__qtpt, gwqr__kuuvg,
        vboq__cep)


@numba.generated_jit(nopython=True)
def haversine_util(lat1, lon1, lat2, lon2):
    verify_int_float_arg(lat1, 'HAVERSINE', 'lat1')
    verify_int_float_arg(lon1, 'HAVERSINE', 'lon1')
    verify_int_float_arg(lat2, 'HAVERSINE', 'lat2')
    verify_int_float_arg(lon2, 'HAVERSINE', 'lon2')
    azw__aeh = ['lat1', 'lon1', 'lat2', 'lon2']
    ldykt__itayn = [lat1, lon1, lat2, lon2]
    cvf__gek = [True] * 4
    gwqr__kuuvg = (
        'arg0, arg1, arg2, arg3 = map(np.radians, (arg0, arg1, arg2, arg3))\n')
    onqtx__vhhto = '(arg2 - arg0) * 0.5'
    wpcb__owgpq = '(arg3 - arg1) * 0.5'
    dgf__nrv = (
        f'np.square(np.sin({onqtx__vhhto})) + (np.cos(arg0) * np.cos(arg2) * np.square(np.sin({wpcb__owgpq})))'
        )
    gwqr__kuuvg += f'res[i] = 12742.0 * np.arcsin(np.sqrt({dgf__nrv}))\n'
    vboq__cep = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(azw__aeh, ldykt__itayn, cvf__gek, gwqr__kuuvg,
        vboq__cep)


@numba.generated_jit(nopython=True)
def div0_util(arr, divisor):
    verify_int_float_arg(arr, 'DIV0', 'arr')
    verify_int_float_arg(divisor, 'DIV0', 'divisor')
    azw__aeh = ['arr', 'divisor']
    ldykt__itayn = [arr, divisor]
    cvf__gek = [True] * 2
    gwqr__kuuvg = 'res[i] = arg0 / arg1 if arg1 else 0\n'
    vboq__cep = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(azw__aeh, ldykt__itayn, cvf__gek, gwqr__kuuvg,
        vboq__cep)


@numba.generated_jit(nopython=True)
def log_util(arr, base):
    verify_int_float_arg(arr, 'log', 'arr')
    verify_int_float_arg(base, 'log', 'base')
    azw__aeh = ['arr', 'base']
    ldykt__itayn = [arr, base]
    xsssc__qtpt = [True] * 2
    gwqr__kuuvg = 'res[i] = np.log(arg0) / np.log(arg1)'
    vboq__cep = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(azw__aeh, ldykt__itayn, xsssc__qtpt, gwqr__kuuvg,
        vboq__cep)


@numba.generated_jit(nopython=True)
def negate_util(arr):
    verify_int_float_arg(arr, 'negate', 'arr')
    azw__aeh = ['arr']
    ldykt__itayn = [arr]
    xsssc__qtpt = [True]
    if arr == bodo.none:
        jwks__fjkxp = types.int32
    elif bodo.utils.utils.is_array_typ(arr, False):
        jwks__fjkxp = arr.dtype
    elif bodo.utils.utils.is_array_typ(arr, True):
        jwks__fjkxp = arr.data.dtype
    else:
        jwks__fjkxp = arr
    gwqr__kuuvg = {types.uint8: 'res[i] = -np.int16(arg0)', types.uint16:
        'res[i] = -np.int32(arg0)', types.uint32: 'res[i] = -np.int64(arg0)'
        }.get(jwks__fjkxp, 'res[i] = -arg0')
    jwks__fjkxp = {types.uint8: types.int16, types.uint16: types.int32,
        types.uint32: types.int64, types.uint64: types.int64}.get(jwks__fjkxp,
        jwks__fjkxp)
    vboq__cep = bodo.utils.typing.to_nullable_type(bodo.utils.typing.
        dtype_to_array_type(jwks__fjkxp))
    return gen_vectorized(azw__aeh, ldykt__itayn, xsssc__qtpt, gwqr__kuuvg,
        vboq__cep)


@numba.generated_jit(nopython=True)
def width_bucket_util(arr, min_val, max_val, num_buckets):
    verify_int_float_arg(arr, 'WIDTH_BUCKET', 'arr')
    verify_int_float_arg(min_val, 'WIDTH_BUCKET', 'min_val')
    verify_int_float_arg(max_val, 'WIDTH_BUCKET', 'max_val')
    verify_int_arg(num_buckets, 'WIDTH_BUCKET', 'num_buckets')
    azw__aeh = ['arr', 'min_val', 'max_val', 'num_buckets']
    ldykt__itayn = [arr, min_val, max_val, num_buckets]
    xsssc__qtpt = [True] * 4
    gwqr__kuuvg = (
        "if arg1 >= arg2: raise ValueError('min_val must be less than max_val')\n"
        )
    gwqr__kuuvg += (
        "if arg3 <= 0: raise ValueError('num_buckets must be a positive integer')\n"
        )
    gwqr__kuuvg += (
        'res[i] = min(max(-1.0, math.floor((arg0 - arg1) / ((arg2 - arg1) / arg3))), arg3) + 1.0'
        )
    vboq__cep = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_vectorized(azw__aeh, ldykt__itayn, xsssc__qtpt, gwqr__kuuvg,
        vboq__cep)
