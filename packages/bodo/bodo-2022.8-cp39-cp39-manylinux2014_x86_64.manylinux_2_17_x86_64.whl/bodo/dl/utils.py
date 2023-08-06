"""Support distributed deep learning with Horovod
"""
import time
import numba
import numpy as np
from mpi4py import MPI
import bodo
from bodo.libs.distributed_api import create_subcomm_mpi4py, get_host_ranks, get_nodes_first_ranks
dl_status = None


def assert_dl_initialized():
    assert dl_status is not None, 'Horovod has not been initialized. Call bodo.dl.start() first'


class DLStatus(object):

    def __init__(self, framework, gpu_ranks):
        self.framework = framework
        self.gpu_ranks = gpu_ranks


def get_num_gpus(framework):
    if framework == 'torch':
        import torch
        return torch.cuda.device_count()
    elif framework == 'tensorflow':
        import tensorflow as tf
        return len(tf.config.experimental.list_physical_devices('GPU'))
    else:
        raise RuntimeError('Framework {} not recognized'.format(framework))


def get_gpu_ranks(framework):
    ulqbq__ycnu = MPI.COMM_WORLD
    ewl__usagb = ulqbq__ycnu.Get_rank()
    szhn__xdj = get_host_ranks()
    yjk__vsl = get_nodes_first_ranks()
    if ewl__usagb in yjk__vsl:
        try:
            mkuly__gdwti = get_num_gpus(framework)
        except Exception as vxhu__ceio:
            mkuly__gdwti = vxhu__ceio
        pxqb__iwsc = create_subcomm_mpi4py(yjk__vsl)
        axcx__rbn = pxqb__iwsc.gather(mkuly__gdwti)
        if ewl__usagb == 0:
            gpu_ranks = []
            jqua__irern = None
            for uffh__mhk, ihy__mrmw in enumerate(szhn__xdj.values()):
                nrccg__ozbx = axcx__rbn[uffh__mhk]
                if isinstance(nrccg__ozbx, Exception):
                    jqua__irern = nrccg__ozbx
                    break
                if nrccg__ozbx == 0:
                    continue
                xanb__dpmjh = len(ihy__mrmw) // nrccg__ozbx
                for agzx__yepri, gfdn__zcp in enumerate(ihy__mrmw):
                    if agzx__yepri % xanb__dpmjh == 0:
                        oytgt__hwee = agzx__yepri / xanb__dpmjh
                        if oytgt__hwee < nrccg__ozbx:
                            gpu_ranks.append(gfdn__zcp)
            if jqua__irern:
                ulqbq__ycnu.bcast(jqua__irern)
                raise jqua__irern
            else:
                ulqbq__ycnu.bcast(gpu_ranks)
    if ewl__usagb != 0:
        gpu_ranks = ulqbq__ycnu.bcast(None)
        if isinstance(gpu_ranks, Exception):
            vxhu__ceio = gpu_ranks
            raise vxhu__ceio
    return gpu_ranks


def is_cuda_available():
    assert_dl_initialized()
    return len(dl_status.gpu_ranks) > 0


def initialize_horovod(framework):
    global dl_status
    if dl_status is not None:
        assert dl_status.framework == framework, 'Attempted to initialize Horovod with different DL frameworks'
        return np.array(dl_status.gpu_ranks, dtype=np.int32)
    gpu_ranks = get_gpu_ranks(framework)
    if framework == 'torch':
        import horovod.torch as hvd
        import torch
        torch.set_num_threads(1)
    elif framework == 'tensorflow':
        import horovod.tensorflow as hvd
        import tensorflow as tf
    else:
        raise RuntimeError('Framework {} not recognized'.format(framework))
    wmisg__bmgly = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        pxqb__iwsc = MPI.COMM_WORLD.Split(color=0 if wmisg__bmgly in
            gpu_ranks else MPI.UNDEFINED, key=wmisg__bmgly)
        if pxqb__iwsc != MPI.COMM_NULL:
            hvd.init(comm=pxqb__iwsc)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                ovri__suuki = tf.config.experimental.list_physical_devices(
                    'GPU')
                for jhov__lisp in ovri__suuki:
                    tf.config.experimental.set_memory_growth(jhov__lisp, True)
                tf.config.experimental.set_visible_devices(ovri__suuki[hvd.
                    local_rank()], 'GPU')
    else:
        if wmisg__bmgly == 0:
            print('[BODO-DL]: No GPUs found in cluster. Using CPUs')
        hvd.init()
    dl_status = DLStatus(framework, np.array(gpu_ranks, dtype=np.int32))


@numba.njit
def start(framework):
    with numba.objmode:
        initialize_horovod(framework)


@numba.njit
def end():
    with numba.objmode:
        end_py()


def end_py():
    if is_cuda_available():
        ryhyw__xamob = 17
        ulqbq__ycnu = MPI.COMM_WORLD
        xotv__oroq = MPI.Get_processor_name()
        vzf__gossc = get_host_ranks()[xotv__oroq]
        assert_dl_initialized()
        if bodo.get_rank() == vzf__gossc[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for ewl__usagb in vzf__gossc[1:]:
                ulqbq__ycnu.isend(1, dest=ewl__usagb, tag=ryhyw__xamob)
        else:
            while True:
                smhgh__vsoef = MPI.Status()
                tamw__hxgvn = ulqbq__ycnu.Iprobe(MPI.ANY_SOURCE, MPI.
                    ANY_TAG, smhgh__vsoef)
                if tamw__hxgvn:
                    assert smhgh__vsoef.source == vzf__gossc[0]
                    assert smhgh__vsoef.tag == ryhyw__xamob
                    ulqbq__ycnu.recv(source=0, tag=ryhyw__xamob)
                    break
                time.sleep(1.0)
    else:
        bodo.barrier()


def _prepare_data_get_gpu_ranks():
    assert_dl_initialized()
    return dl_status.gpu_ranks


@numba.njit
def prepare_data(data):
    with numba.objmode(gpu_ranks='int32[:]'):
        gpu_ranks = _prepare_data_get_gpu_ranks()
    if len(gpu_ranks) > 0:
        data = bodo.rebalance(data, dests=list(gpu_ranks), parallel=True)
    else:
        data = bodo.rebalance(data, parallel=True)
    return data
