import llvmlite.binding as ll
import numba
from numba.core import types
from bodo.io import arrow_cpp
from bodo.libs import array_ext, decimal_ext, quantile_alg
ll.add_symbol('get_stats_alloc_arr', array_ext.get_stats_alloc)
ll.add_symbol('get_stats_free_arr', array_ext.get_stats_free)
ll.add_symbol('get_stats_mi_alloc_arr', array_ext.get_stats_mi_alloc)
ll.add_symbol('get_stats_mi_free_arr', array_ext.get_stats_mi_free)
ll.add_symbol('get_stats_alloc_dec', decimal_ext.get_stats_alloc)
ll.add_symbol('get_stats_free_dec', decimal_ext.get_stats_free)
ll.add_symbol('get_stats_mi_alloc_dec', decimal_ext.get_stats_mi_alloc)
ll.add_symbol('get_stats_mi_free_dec', decimal_ext.get_stats_mi_free)
ll.add_symbol('get_stats_alloc_qa', quantile_alg.get_stats_alloc)
ll.add_symbol('get_stats_free_qa', quantile_alg.get_stats_free)
ll.add_symbol('get_stats_alloc_pq', arrow_cpp.get_stats_alloc)
ll.add_symbol('get_stats_free_pq', arrow_cpp.get_stats_free)
ll.add_symbol('get_stats_mi_alloc_pq', arrow_cpp.get_stats_mi_alloc)
ll.add_symbol('get_stats_mi_free_pq', arrow_cpp.get_stats_mi_free)
ll.add_symbol('get_stats_mi_alloc_qa', quantile_alg.get_stats_mi_alloc)
ll.add_symbol('get_stats_mi_free_qa', quantile_alg.get_stats_mi_free)
get_stats_alloc_arr = types.ExternalFunction('get_stats_alloc_arr', types.
    uint64())
get_stats_free_arr = types.ExternalFunction('get_stats_free_arr', types.
    uint64())
get_stats_mi_alloc_arr = types.ExternalFunction('get_stats_mi_alloc_arr',
    types.uint64())
get_stats_mi_free_arr = types.ExternalFunction('get_stats_mi_free_arr',
    types.uint64())
get_stats_alloc_dec = types.ExternalFunction('get_stats_alloc_dec', types.
    uint64())
get_stats_free_dec = types.ExternalFunction('get_stats_free_dec', types.
    uint64())
get_stats_mi_alloc_dec = types.ExternalFunction('get_stats_mi_alloc_dec',
    types.uint64())
get_stats_mi_free_dec = types.ExternalFunction('get_stats_mi_free_dec',
    types.uint64())
get_stats_alloc_pq = types.ExternalFunction('get_stats_alloc_pq', types.
    uint64())
get_stats_free_pq = types.ExternalFunction('get_stats_free_pq', types.uint64())
get_stats_mi_alloc_pq = types.ExternalFunction('get_stats_mi_alloc_pq',
    types.uint64())
get_stats_mi_free_pq = types.ExternalFunction('get_stats_mi_free_pq', types
    .uint64())
get_stats_alloc_qa = types.ExternalFunction('get_stats_alloc_qa', types.
    uint64())
get_stats_free_qa = types.ExternalFunction('get_stats_free_qa', types.uint64())
get_stats_mi_alloc_qa = types.ExternalFunction('get_stats_mi_alloc_qa',
    types.uint64())
get_stats_mi_free_qa = types.ExternalFunction('get_stats_mi_free_qa', types
    .uint64())


@numba.njit
def get_allocation_stats():
    gapm__tkni = get_allocation_stats_arr(), get_allocation_stats_dec(
        ), get_allocation_stats_pq(), get_allocation_stats_qa()
    bzg__rndlh, rch__rca, oyzb__bfcml, csu__hyj = 0, 0, 0, 0
    for hyuv__opd in gapm__tkni:
        bzg__rndlh += hyuv__opd[0]
        rch__rca += hyuv__opd[1]
        oyzb__bfcml += hyuv__opd[2]
        csu__hyj += hyuv__opd[3]
    return bzg__rndlh, rch__rca, oyzb__bfcml, csu__hyj


@numba.njit
def get_allocation_stats_arr():
    return get_stats_alloc_arr(), get_stats_free_arr(), get_stats_mi_alloc_arr(
        ), get_stats_mi_free_arr()


@numba.njit
def get_allocation_stats_dec():
    return get_stats_alloc_dec(), get_stats_free_dec(), get_stats_mi_alloc_dec(
        ), get_stats_mi_free_dec()


@numba.njit
def get_allocation_stats_pq():
    return get_stats_alloc_pq(), get_stats_free_pq(), get_stats_mi_alloc_pq(
        ), get_stats_mi_free_pq()


@numba.njit
def get_allocation_stats_qa():
    return get_stats_alloc_qa(), get_stats_free_qa(), get_stats_mi_alloc_qa(
        ), get_stats_mi_free_qa()
