"""
Implements array kernels that are specific to BodoSQL which have a variable
number of arguments
"""
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import raise_bodo_error


def coalesce(A):
    return


@overload(coalesce)
def overload_coalesce(A):
    if not isinstance(A, (types.Tuple, types.UniTuple)):
        raise_bodo_error('Coalesce argument must be a tuple')
    for hrcw__xzhg in range(len(A)):
        if isinstance(A[hrcw__xzhg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.coalesce',
                ['A'], hrcw__xzhg, container_length=len(A))

    def impl(A):
        return coalesce_util(A)
    return impl


def coalesce_util(A):
    return


@overload(coalesce_util, no_unliteral=True)
def overload_coalesce_util(A):
    if len(A) == 0:
        raise_bodo_error('Cannot coalesce 0 columns')
    oxnso__wbm = None
    yicp__kdt = []
    for hrcw__xzhg in range(len(A)):
        if A[hrcw__xzhg] == bodo.none:
            yicp__kdt.append(hrcw__xzhg)
        elif not bodo.utils.utils.is_array_typ(A[hrcw__xzhg]):
            for ptwou__tmlwt in range(hrcw__xzhg + 1, len(A)):
                yicp__kdt.append(ptwou__tmlwt)
                if bodo.utils.utils.is_array_typ(A[ptwou__tmlwt]):
                    oxnso__wbm = f'A[{ptwou__tmlwt}]'
            break
    yki__yror = [f'A{hrcw__xzhg}' for hrcw__xzhg in range(len(A)) if 
        hrcw__xzhg not in yicp__kdt]
    wjili__vett = [A[hrcw__xzhg] for hrcw__xzhg in range(len(A)) if 
        hrcw__xzhg not in yicp__kdt]
    qxepg__vvlro = [False] * (len(A) - len(yicp__kdt))
    jefbq__ssr = ''
    srh__ucf = True
    vsdtl__ozibh = False
    hmnxm__nzfni = 0
    for hrcw__xzhg in range(len(A)):
        if hrcw__xzhg in yicp__kdt:
            hmnxm__nzfni += 1
            continue
        elif bodo.utils.utils.is_array_typ(A[hrcw__xzhg]):
            exkou__oqfkt = 'if' if srh__ucf else 'elif'
            jefbq__ssr += (
                f'{exkou__oqfkt} not bodo.libs.array_kernels.isna(A{hrcw__xzhg}, i):\n'
                )
            jefbq__ssr += f'   res[i] = arg{hrcw__xzhg - hmnxm__nzfni}\n'
            srh__ucf = False
        else:
            assert not vsdtl__ozibh, 'should not encounter more than one scalar due to dead column pruning'
            if srh__ucf:
                jefbq__ssr += f'res[i] = arg{hrcw__xzhg - hmnxm__nzfni}\n'
            else:
                jefbq__ssr += 'else:\n'
                jefbq__ssr += f'   res[i] = arg{hrcw__xzhg - hmnxm__nzfni}\n'
            vsdtl__ozibh = True
            break
    if not vsdtl__ozibh:
        if not srh__ucf:
            jefbq__ssr += 'else:\n'
            jefbq__ssr += '   bodo.libs.array_kernels.setna(res, i)'
        else:
            jefbq__ssr += 'bodo.libs.array_kernels.setna(res, i)'
    ybgc__ovqd = 'A'
    darw__jcqgl = {f'A{hrcw__xzhg}': f'A[{hrcw__xzhg}]' for hrcw__xzhg in
        range(len(A)) if hrcw__xzhg not in yicp__kdt}
    qqiab__hbq = get_common_broadcasted_type(wjili__vett, 'COALESCE')
    return gen_vectorized(yki__yror, wjili__vett, qxepg__vvlro, jefbq__ssr,
        qqiab__hbq, ybgc__ovqd, darw__jcqgl, oxnso__wbm,
        support_dict_encoding=False)


@numba.generated_jit(nopython=True)
def decode(A):
    if not isinstance(A, (types.Tuple, types.UniTuple)):
        raise_bodo_error('Decode argument must be a tuple')
    for hrcw__xzhg in range(len(A)):
        if isinstance(A[hrcw__xzhg], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.decode',
                ['A'], hrcw__xzhg, container_length=len(A))

    def impl(A):
        return decode_util(A)
    return impl


@numba.generated_jit(nopython=True)
def decode_util(A):
    if len(A) < 3:
        raise_bodo_error('Need at least 3 arguments to DECODE')
    yki__yror = [f'A{hrcw__xzhg}' for hrcw__xzhg in range(len(A))]
    wjili__vett = [A[hrcw__xzhg] for hrcw__xzhg in range(len(A))]
    qxepg__vvlro = [False] * len(A)
    jefbq__ssr = ''
    for hrcw__xzhg in range(1, len(A) - 1, 2):
        exkou__oqfkt = 'if' if len(jefbq__ssr) == 0 else 'elif'
        if A[hrcw__xzhg + 1] == bodo.none:
            ucqd__jzfwj = '   bodo.libs.array_kernels.setna(res, i)\n'
        elif bodo.utils.utils.is_array_typ(A[hrcw__xzhg + 1]):
            ucqd__jzfwj = (
                f'   if bodo.libs.array_kernels.isna({yki__yror[hrcw__xzhg + 1]}, i):\n'
                )
            ucqd__jzfwj += f'      bodo.libs.array_kernels.setna(res, i)\n'
            ucqd__jzfwj += f'   else:\n'
            ucqd__jzfwj += f'      res[i] = arg{hrcw__xzhg + 1}\n'
        else:
            ucqd__jzfwj = f'   res[i] = arg{hrcw__xzhg + 1}\n'
        if A[0] == bodo.none and (bodo.utils.utils.is_array_typ(A[
            hrcw__xzhg]) or A[hrcw__xzhg] == bodo.none):
            if A[hrcw__xzhg] == bodo.none:
                jefbq__ssr += f'{exkou__oqfkt} True:\n'
                jefbq__ssr += ucqd__jzfwj
                break
            else:
                jefbq__ssr += f"""{exkou__oqfkt} bodo.libs.array_kernels.isna({yki__yror[hrcw__xzhg]}, i):
"""
                jefbq__ssr += ucqd__jzfwj
        elif A[0] == bodo.none:
            pass
        elif bodo.utils.utils.is_array_typ(A[0]):
            if bodo.utils.utils.is_array_typ(A[hrcw__xzhg]):
                jefbq__ssr += f"""{exkou__oqfkt} (bodo.libs.array_kernels.isna({yki__yror[0]}, i) and bodo.libs.array_kernels.isna({yki__yror[hrcw__xzhg]}, i)) or (not bodo.libs.array_kernels.isna({yki__yror[0]}, i) and not bodo.libs.array_kernels.isna({yki__yror[hrcw__xzhg]}, i) and arg0 == arg{hrcw__xzhg}):
"""
                jefbq__ssr += ucqd__jzfwj
            elif A[hrcw__xzhg] == bodo.none:
                jefbq__ssr += (
                    f'{exkou__oqfkt} bodo.libs.array_kernels.isna({yki__yror[0]}, i):\n'
                    )
                jefbq__ssr += ucqd__jzfwj
            else:
                jefbq__ssr += f"""{exkou__oqfkt} (not bodo.libs.array_kernels.isna({yki__yror[0]}, i)) and arg0 == arg{hrcw__xzhg}:
"""
                jefbq__ssr += ucqd__jzfwj
        elif A[hrcw__xzhg] == bodo.none:
            pass
        elif bodo.utils.utils.is_array_typ(A[hrcw__xzhg]):
            jefbq__ssr += f"""{exkou__oqfkt} (not bodo.libs.array_kernels.isna({yki__yror[hrcw__xzhg]}, i)) and arg0 == arg{hrcw__xzhg}:
"""
            jefbq__ssr += ucqd__jzfwj
        else:
            jefbq__ssr += f'{exkou__oqfkt} arg0 == arg{hrcw__xzhg}:\n'
            jefbq__ssr += ucqd__jzfwj
    if len(jefbq__ssr) > 0:
        jefbq__ssr += 'else:\n'
    if len(A) % 2 == 0 and A[-1] != bodo.none:
        if bodo.utils.utils.is_array_typ(A[-1]):
            jefbq__ssr += (
                f'   if bodo.libs.array_kernels.isna({yki__yror[-1]}, i):\n')
            jefbq__ssr += '      bodo.libs.array_kernels.setna(res, i)\n'
            jefbq__ssr += '   else:\n'
        jefbq__ssr += f'      res[i] = arg{len(A) - 1}'
    else:
        jefbq__ssr += '   bodo.libs.array_kernels.setna(res, i)'
    ybgc__ovqd = 'A'
    darw__jcqgl = {f'A{hrcw__xzhg}': f'A[{hrcw__xzhg}]' for hrcw__xzhg in
        range(len(A))}
    if len(wjili__vett) % 2 == 0:
        upvfy__een = [wjili__vett[0]] + wjili__vett[1:-1:2]
        hsiw__vui = wjili__vett[2::2] + [wjili__vett[-1]]
    else:
        upvfy__een = [wjili__vett[0]] + wjili__vett[1::2]
        hsiw__vui = wjili__vett[2::2]
    hvu__dli = get_common_broadcasted_type(upvfy__een, 'DECODE')
    qqiab__hbq = get_common_broadcasted_type(hsiw__vui, 'DECODE')
    if qqiab__hbq == bodo.none:
        qqiab__hbq = hvu__dli
    noe__egej = bodo.utils.utils.is_array_typ(A[0]
        ) and bodo.none not in upvfy__een and len(wjili__vett) % 2 == 1
    return gen_vectorized(yki__yror, wjili__vett, qxepg__vvlro, jefbq__ssr,
        qqiab__hbq, ybgc__ovqd, darw__jcqgl, support_dict_encoding=noe__egej)
