from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.bodosql_array_kernel_utils import *


def acos(arr):
    return


def acosh(arr):
    return


def asin(arr):
    return


def asinh(arr):
    return


def atan(arr):
    return


def atanh(arr):
    return


def atan2(arr0, arr1):
    return


def cos(arr):
    return


def cosh(arr):
    return


def sin(arr):
    return


def sinh(arr):
    return


def tan(arr):
    return


def tanh(arr):
    return


def radians(arr):
    return


def degrees(arr):
    return


def acos_util(arr):
    return


def acosh_util(arr):
    return


def asin_util(arr):
    return


def asinh_util(arr):
    return


def atan_util(arr):
    return


def atanh_util(arr):
    return


def atan2_util(arr0, arr1):
    return


def cos_util(arr):
    return


def cosh_util(arr):
    return


def sin_util(arr):
    return


def sinh_util(arr):
    return


def tan_util(arr):
    return


def tanh_util(arr):
    return


def radians_util(arr):
    return


def degrees_util(arr):
    return


funcs_utils_names = (acos, acos_util, 'ACOS'), (acosh, acosh_util, 'ACOSH'), (
    asin, asin_util, 'ASIN'), (asinh, asinh_util, 'ASINH'), (atan,
    atan_util, 'ATAN'), (atanh, atanh_util, 'ATANH'), (atan2, atan2_util,
    'ATAN2'), (cos, cos_util, 'COS'), (cosh, cosh_util, 'COSH'), (sin,
    sin_util, 'SIN'), (sinh, sinh_util, 'SINH'), (tan, tan_util, 'TAN'), (tanh,
    tanh_util, 'TANH'), (radians, radians_util, 'RADIANS'), (degrees,
    degrees_util, 'DEGREES')
double_arg_funcs = 'ATAN2',


def create_trig_func_overload(func_name):
    if func_name not in double_arg_funcs:
        func_name = func_name.lower()

        def overload_func(arr):
            if isinstance(arr, types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.{func_name}', ['arr'], 0)
            glnoc__lpm = 'def impl(arr):\n'
            glnoc__lpm += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr)'
                )
            xmaf__ltdc = {}
            exec(glnoc__lpm, {'bodo': bodo}, xmaf__ltdc)
            return xmaf__ltdc['impl']
    else:
        func_name = func_name.lower()

        def overload_func(arr0, arr1):
            args = [arr0, arr1]
            for flbhr__abm in range(2):
                if isinstance(args[flbhr__abm], types.optional):
                    return unopt_argument(
                        f'bodo.libs.bodosql_array_kernels.{func_name}', [
                        'arr0', 'arr1'], flbhr__abm)
            glnoc__lpm = 'def impl(arr0, arr1):\n'
            glnoc__lpm += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr0, arr1)'
                )
            xmaf__ltdc = {}
            exec(glnoc__lpm, {'bodo': bodo}, xmaf__ltdc)
            return xmaf__ltdc['impl']
    return overload_func


def create_trig_util_overload(func_name):
    if func_name not in double_arg_funcs:

        def overload_trig_util(arr):
            verify_int_float_arg(arr, func_name, 'arr')
            fihfc__bom = ['arr']
            hyccp__hault = [arr]
            suz__kyoh = [True]
            wxz__hhdcm = ''
            if func_name == 'ACOS':
                wxz__hhdcm += 'res[i] = np.arccos(arg0)'
            elif func_name == 'ACOSH':
                wxz__hhdcm += 'res[i] = np.arccosh(arg0)'
            elif func_name == 'ASIN':
                wxz__hhdcm += 'res[i] = np.arcsin(arg0)'
            elif func_name == 'ASINH':
                wxz__hhdcm += 'res[i] = np.arcsinh(arg0)'
            elif func_name == 'ATAN':
                wxz__hhdcm += 'res[i] = np.arctan(arg0)'
            elif func_name == 'ATANH':
                wxz__hhdcm += 'res[i] = np.arctanh(arg0)'
            elif func_name == 'COS':
                wxz__hhdcm += 'res[i] = np.cos(arg0)'
            elif func_name == 'COSH':
                wxz__hhdcm += 'res[i] = np.cosh(arg0)'
            elif func_name == 'SIN':
                wxz__hhdcm += 'res[i] = np.sin(arg0)'
            elif func_name == 'SINH':
                wxz__hhdcm += 'res[i] = np.sinh(arg0)'
            elif func_name == 'TAN':
                wxz__hhdcm += 'res[i] = np.tan(arg0)'
            elif func_name == 'TANH':
                wxz__hhdcm += 'res[i] = np.tanh(arg0)'
            elif func_name == 'RADIANS':
                wxz__hhdcm += 'res[i] = np.radians(arg0)'
            elif func_name == 'DEGREES':
                wxz__hhdcm += 'res[i] = np.degrees(arg0)'
            else:
                raise ValueError(f'Unknown function name: {func_name}')
            udvbk__skar = types.Array(bodo.float64, 1, 'C')
            return gen_vectorized(fihfc__bom, hyccp__hault, suz__kyoh,
                wxz__hhdcm, udvbk__skar)
    else:

        def overload_trig_util(arr0, arr1):
            verify_int_float_arg(arr0, func_name, 'arr0')
            verify_int_float_arg(arr1, func_name, 'arr1')
            fihfc__bom = ['arr0', 'arr1']
            hyccp__hault = [arr0, arr1]
            suz__kyoh = [True, True]
            wxz__hhdcm = ''
            if func_name == 'ATAN2':
                wxz__hhdcm += 'res[i] = np.arctan2(arg0, arg1)\n'
            else:
                raise ValueError(f'Unknown function name: {func_name}')
            udvbk__skar = types.Array(bodo.float64, 1, 'C')
            return gen_vectorized(fihfc__bom, hyccp__hault, suz__kyoh,
                wxz__hhdcm, udvbk__skar)
    return overload_trig_util


def _install_trig_overload(funcs_utils_names):
    for zocg__ijp, epu__cma, func_name in funcs_utils_names:
        pnt__qishh = create_trig_func_overload(func_name)
        overload(zocg__ijp)(pnt__qishh)
        znrq__ftigf = create_trig_util_overload(func_name)
        overload(epu__cma)(znrq__ftigf)


_install_trig_overload(funcs_utils_names)
