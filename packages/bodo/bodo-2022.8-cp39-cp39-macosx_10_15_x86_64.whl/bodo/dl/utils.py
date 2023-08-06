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
    qzsrn__ltpck = MPI.COMM_WORLD
    jesdl__smxcw = qzsrn__ltpck.Get_rank()
    pgs__mnc = get_host_ranks()
    kum__vqdbb = get_nodes_first_ranks()
    if jesdl__smxcw in kum__vqdbb:
        try:
            ncrhe__inlx = get_num_gpus(framework)
        except Exception as msld__jrvj:
            ncrhe__inlx = msld__jrvj
        thir__orks = create_subcomm_mpi4py(kum__vqdbb)
        gwczo__ujsx = thir__orks.gather(ncrhe__inlx)
        if jesdl__smxcw == 0:
            gpu_ranks = []
            cdq__qyvmo = None
            for eswu__jetne, ozsg__pcqb in enumerate(pgs__mnc.values()):
                dead__vwki = gwczo__ujsx[eswu__jetne]
                if isinstance(dead__vwki, Exception):
                    cdq__qyvmo = dead__vwki
                    break
                if dead__vwki == 0:
                    continue
                nsyb__lxa = len(ozsg__pcqb) // dead__vwki
                for wfmv__balnk, fmjo__ixt in enumerate(ozsg__pcqb):
                    if wfmv__balnk % nsyb__lxa == 0:
                        yqkp__sjqs = wfmv__balnk / nsyb__lxa
                        if yqkp__sjqs < dead__vwki:
                            gpu_ranks.append(fmjo__ixt)
            if cdq__qyvmo:
                qzsrn__ltpck.bcast(cdq__qyvmo)
                raise cdq__qyvmo
            else:
                qzsrn__ltpck.bcast(gpu_ranks)
    if jesdl__smxcw != 0:
        gpu_ranks = qzsrn__ltpck.bcast(None)
        if isinstance(gpu_ranks, Exception):
            msld__jrvj = gpu_ranks
            raise msld__jrvj
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
    qwdg__rxft = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        thir__orks = MPI.COMM_WORLD.Split(color=0 if qwdg__rxft in
            gpu_ranks else MPI.UNDEFINED, key=qwdg__rxft)
        if thir__orks != MPI.COMM_NULL:
            hvd.init(comm=thir__orks)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                sueh__tijj = tf.config.experimental.list_physical_devices('GPU'
                    )
                for bqpgh__wlnbr in sueh__tijj:
                    tf.config.experimental.set_memory_growth(bqpgh__wlnbr, True
                        )
                tf.config.experimental.set_visible_devices(sueh__tijj[hvd.
                    local_rank()], 'GPU')
    else:
        if qwdg__rxft == 0:
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
        ysz__yujje = 17
        qzsrn__ltpck = MPI.COMM_WORLD
        npf__rpgfk = MPI.Get_processor_name()
        ylk__qxqf = get_host_ranks()[npf__rpgfk]
        assert_dl_initialized()
        if bodo.get_rank() == ylk__qxqf[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for jesdl__smxcw in ylk__qxqf[1:]:
                qzsrn__ltpck.isend(1, dest=jesdl__smxcw, tag=ysz__yujje)
        else:
            while True:
                dddy__xqqr = MPI.Status()
                odd__myg = qzsrn__ltpck.Iprobe(MPI.ANY_SOURCE, MPI.ANY_TAG,
                    dddy__xqqr)
                if odd__myg:
                    assert dddy__xqqr.source == ylk__qxqf[0]
                    assert dddy__xqqr.tag == ysz__yujje
                    qzsrn__ltpck.recv(source=0, tag=ysz__yujje)
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
