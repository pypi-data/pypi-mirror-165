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
    for irjp__ygjdk in range(len(A)):
        if isinstance(A[irjp__ygjdk], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.coalesce',
                ['A'], irjp__ygjdk, container_length=len(A))

    def impl(A):
        return coalesce_util(A)
    return impl


def coalesce_util(A):
    return


@overload(coalesce_util, no_unliteral=True)
def overload_coalesce_util(A):
    if len(A) == 0:
        raise_bodo_error('Cannot coalesce 0 columns')
    mhr__hbzf = None
    zet__mwfjq = []
    for irjp__ygjdk in range(len(A)):
        if A[irjp__ygjdk] == bodo.none:
            zet__mwfjq.append(irjp__ygjdk)
        elif not bodo.utils.utils.is_array_typ(A[irjp__ygjdk]):
            for cqhzk__ysf in range(irjp__ygjdk + 1, len(A)):
                zet__mwfjq.append(cqhzk__ysf)
                if bodo.utils.utils.is_array_typ(A[cqhzk__ysf]):
                    mhr__hbzf = f'A[{cqhzk__ysf}]'
            break
    vsvzl__rdw = [f'A{irjp__ygjdk}' for irjp__ygjdk in range(len(A)) if 
        irjp__ygjdk not in zet__mwfjq]
    clo__wtj = [A[irjp__ygjdk] for irjp__ygjdk in range(len(A)) if 
        irjp__ygjdk not in zet__mwfjq]
    zbrfd__cjr = [False] * (len(A) - len(zet__mwfjq))
    nyed__mfer = ''
    zvv__pwf = True
    ylffo__lago = False
    wuxc__huait = 0
    for irjp__ygjdk in range(len(A)):
        if irjp__ygjdk in zet__mwfjq:
            wuxc__huait += 1
            continue
        elif bodo.utils.utils.is_array_typ(A[irjp__ygjdk]):
            ybvd__ychf = 'if' if zvv__pwf else 'elif'
            nyed__mfer += (
                f'{ybvd__ychf} not bodo.libs.array_kernels.isna(A{irjp__ygjdk}, i):\n'
                )
            nyed__mfer += f'   res[i] = arg{irjp__ygjdk - wuxc__huait}\n'
            zvv__pwf = False
        else:
            assert not ylffo__lago, 'should not encounter more than one scalar due to dead column pruning'
            if zvv__pwf:
                nyed__mfer += f'res[i] = arg{irjp__ygjdk - wuxc__huait}\n'
            else:
                nyed__mfer += 'else:\n'
                nyed__mfer += f'   res[i] = arg{irjp__ygjdk - wuxc__huait}\n'
            ylffo__lago = True
            break
    if not ylffo__lago:
        if not zvv__pwf:
            nyed__mfer += 'else:\n'
            nyed__mfer += '   bodo.libs.array_kernels.setna(res, i)'
        else:
            nyed__mfer += 'bodo.libs.array_kernels.setna(res, i)'
    bdsqh__nqgac = 'A'
    ksnx__rfrk = {f'A{irjp__ygjdk}': f'A[{irjp__ygjdk}]' for irjp__ygjdk in
        range(len(A)) if irjp__ygjdk not in zet__mwfjq}
    mcjal__hplbh = get_common_broadcasted_type(clo__wtj, 'COALESCE')
    return gen_vectorized(vsvzl__rdw, clo__wtj, zbrfd__cjr, nyed__mfer,
        mcjal__hplbh, bdsqh__nqgac, ksnx__rfrk, mhr__hbzf,
        support_dict_encoding=False)


@numba.generated_jit(nopython=True)
def decode(A):
    if not isinstance(A, (types.Tuple, types.UniTuple)):
        raise_bodo_error('Decode argument must be a tuple')
    for irjp__ygjdk in range(len(A)):
        if isinstance(A[irjp__ygjdk], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.decode',
                ['A'], irjp__ygjdk, container_length=len(A))

    def impl(A):
        return decode_util(A)
    return impl


@numba.generated_jit(nopython=True)
def decode_util(A):
    if len(A) < 3:
        raise_bodo_error('Need at least 3 arguments to DECODE')
    vsvzl__rdw = [f'A{irjp__ygjdk}' for irjp__ygjdk in range(len(A))]
    clo__wtj = [A[irjp__ygjdk] for irjp__ygjdk in range(len(A))]
    zbrfd__cjr = [False] * len(A)
    nyed__mfer = ''
    for irjp__ygjdk in range(1, len(A) - 1, 2):
        ybvd__ychf = 'if' if len(nyed__mfer) == 0 else 'elif'
        if A[irjp__ygjdk + 1] == bodo.none:
            jncr__tjvh = '   bodo.libs.array_kernels.setna(res, i)\n'
        elif bodo.utils.utils.is_array_typ(A[irjp__ygjdk + 1]):
            jncr__tjvh = (
                f'   if bodo.libs.array_kernels.isna({vsvzl__rdw[irjp__ygjdk + 1]}, i):\n'
                )
            jncr__tjvh += f'      bodo.libs.array_kernels.setna(res, i)\n'
            jncr__tjvh += f'   else:\n'
            jncr__tjvh += f'      res[i] = arg{irjp__ygjdk + 1}\n'
        else:
            jncr__tjvh = f'   res[i] = arg{irjp__ygjdk + 1}\n'
        if A[0] == bodo.none and (bodo.utils.utils.is_array_typ(A[
            irjp__ygjdk]) or A[irjp__ygjdk] == bodo.none):
            if A[irjp__ygjdk] == bodo.none:
                nyed__mfer += f'{ybvd__ychf} True:\n'
                nyed__mfer += jncr__tjvh
                break
            else:
                nyed__mfer += f"""{ybvd__ychf} bodo.libs.array_kernels.isna({vsvzl__rdw[irjp__ygjdk]}, i):
"""
                nyed__mfer += jncr__tjvh
        elif A[0] == bodo.none:
            pass
        elif bodo.utils.utils.is_array_typ(A[0]):
            if bodo.utils.utils.is_array_typ(A[irjp__ygjdk]):
                nyed__mfer += f"""{ybvd__ychf} (bodo.libs.array_kernels.isna({vsvzl__rdw[0]}, i) and bodo.libs.array_kernels.isna({vsvzl__rdw[irjp__ygjdk]}, i)) or (not bodo.libs.array_kernels.isna({vsvzl__rdw[0]}, i) and not bodo.libs.array_kernels.isna({vsvzl__rdw[irjp__ygjdk]}, i) and arg0 == arg{irjp__ygjdk}):
"""
                nyed__mfer += jncr__tjvh
            elif A[irjp__ygjdk] == bodo.none:
                nyed__mfer += (
                    f'{ybvd__ychf} bodo.libs.array_kernels.isna({vsvzl__rdw[0]}, i):\n'
                    )
                nyed__mfer += jncr__tjvh
            else:
                nyed__mfer += f"""{ybvd__ychf} (not bodo.libs.array_kernels.isna({vsvzl__rdw[0]}, i)) and arg0 == arg{irjp__ygjdk}:
"""
                nyed__mfer += jncr__tjvh
        elif A[irjp__ygjdk] == bodo.none:
            pass
        elif bodo.utils.utils.is_array_typ(A[irjp__ygjdk]):
            nyed__mfer += f"""{ybvd__ychf} (not bodo.libs.array_kernels.isna({vsvzl__rdw[irjp__ygjdk]}, i)) and arg0 == arg{irjp__ygjdk}:
"""
            nyed__mfer += jncr__tjvh
        else:
            nyed__mfer += f'{ybvd__ychf} arg0 == arg{irjp__ygjdk}:\n'
            nyed__mfer += jncr__tjvh
    if len(nyed__mfer) > 0:
        nyed__mfer += 'else:\n'
    if len(A) % 2 == 0 and A[-1] != bodo.none:
        if bodo.utils.utils.is_array_typ(A[-1]):
            nyed__mfer += (
                f'   if bodo.libs.array_kernels.isna({vsvzl__rdw[-1]}, i):\n')
            nyed__mfer += '      bodo.libs.array_kernels.setna(res, i)\n'
            nyed__mfer += '   else:\n'
        nyed__mfer += f'      res[i] = arg{len(A) - 1}'
    else:
        nyed__mfer += '   bodo.libs.array_kernels.setna(res, i)'
    bdsqh__nqgac = 'A'
    ksnx__rfrk = {f'A{irjp__ygjdk}': f'A[{irjp__ygjdk}]' for irjp__ygjdk in
        range(len(A))}
    if len(clo__wtj) % 2 == 0:
        vquzs__cnut = [clo__wtj[0]] + clo__wtj[1:-1:2]
        aewh__ktfl = clo__wtj[2::2] + [clo__wtj[-1]]
    else:
        vquzs__cnut = [clo__wtj[0]] + clo__wtj[1::2]
        aewh__ktfl = clo__wtj[2::2]
    uchli__egzn = get_common_broadcasted_type(vquzs__cnut, 'DECODE')
    mcjal__hplbh = get_common_broadcasted_type(aewh__ktfl, 'DECODE')
    if mcjal__hplbh == bodo.none:
        mcjal__hplbh = uchli__egzn
    vhbh__fga = bodo.utils.utils.is_array_typ(A[0]
        ) and bodo.none not in vquzs__cnut and len(clo__wtj) % 2 == 1
    return gen_vectorized(vsvzl__rdw, clo__wtj, zbrfd__cjr, nyed__mfer,
        mcjal__hplbh, bdsqh__nqgac, ksnx__rfrk, support_dict_encoding=vhbh__fga
        )
