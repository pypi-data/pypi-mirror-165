import gc
import inspect
import sys
import types as pytypes
import bodo
master_mode_on = False
MASTER_RANK = 0


class MasterModeDispatcher(object):

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def __call__(self, *args, **kwargs):
        assert bodo.get_rank() == MASTER_RANK
        return master_wrapper(self.dispatcher, *args, **kwargs)

    def __getstate__(self):
        assert bodo.get_rank() == MASTER_RANK
        return self.dispatcher.py_func

    def __setstate__(self, state):
        assert bodo.get_rank() != MASTER_RANK
        ajw__gwb = state
        apsr__gtbub = inspect.getsourcelines(ajw__gwb)[0][0]
        assert apsr__gtbub.startswith('@bodo.jit') or apsr__gtbub.startswith(
            '@jit')
        ofo__zhe = eval(apsr__gtbub[1:])
        self.dispatcher = ofo__zhe(ajw__gwb)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    lnv__frev = MPI.COMM_WORLD
    while True:
        ope__mkp = lnv__frev.bcast(None, root=MASTER_RANK)
        if ope__mkp[0] == 'exec':
            ajw__gwb = pickle.loads(ope__mkp[1])
            for lgh__dsjdm, koti__vkdx in list(ajw__gwb.__globals__.items()):
                if isinstance(koti__vkdx, MasterModeDispatcher):
                    ajw__gwb.__globals__[lgh__dsjdm] = koti__vkdx.dispatcher
            if ajw__gwb.__module__ not in sys.modules:
                sys.modules[ajw__gwb.__module__] = pytypes.ModuleType(ajw__gwb
                    .__module__)
            apsr__gtbub = inspect.getsourcelines(ajw__gwb)[0][0]
            assert apsr__gtbub.startswith('@bodo.jit'
                ) or apsr__gtbub.startswith('@jit')
            ofo__zhe = eval(apsr__gtbub[1:])
            func = ofo__zhe(ajw__gwb)
            fukxb__eeac = ope__mkp[2]
            pjlp__admnd = ope__mkp[3]
            rmas__npja = []
            for hboc__uwl in fukxb__eeac:
                if hboc__uwl == 'scatter':
                    rmas__npja.append(bodo.scatterv(None))
                elif hboc__uwl == 'bcast':
                    rmas__npja.append(lnv__frev.bcast(None, root=MASTER_RANK))
            tqq__qaa = {}
            for argname, hboc__uwl in pjlp__admnd.items():
                if hboc__uwl == 'scatter':
                    tqq__qaa[argname] = bodo.scatterv(None)
                elif hboc__uwl == 'bcast':
                    tqq__qaa[argname] = lnv__frev.bcast(None, root=MASTER_RANK)
            lhomb__lzkt = func(*rmas__npja, **tqq__qaa)
            if lhomb__lzkt is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(lhomb__lzkt)
            del (ope__mkp, ajw__gwb, func, ofo__zhe, fukxb__eeac,
                pjlp__admnd, rmas__npja, tqq__qaa, lhomb__lzkt)
            gc.collect()
        elif ope__mkp[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    lnv__frev = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        fukxb__eeac = ['scatter' for mzyxi__ndv in range(len(args))]
        pjlp__admnd = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        taf__sww = func.py_func.__code__.co_varnames
        yjh__pfrf = func.targetoptions

        def get_distribution(argname):
            if argname in yjh__pfrf.get('distributed', []
                ) or argname in yjh__pfrf.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        fukxb__eeac = [get_distribution(argname) for argname in taf__sww[:
            len(args)]]
        pjlp__admnd = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    qowth__lolv = pickle.dumps(func.py_func)
    lnv__frev.bcast(['exec', qowth__lolv, fukxb__eeac, pjlp__admnd])
    rmas__npja = []
    for mlo__mzyg, hboc__uwl in zip(args, fukxb__eeac):
        if hboc__uwl == 'scatter':
            rmas__npja.append(bodo.scatterv(mlo__mzyg))
        elif hboc__uwl == 'bcast':
            lnv__frev.bcast(mlo__mzyg)
            rmas__npja.append(mlo__mzyg)
    tqq__qaa = {}
    for argname, mlo__mzyg in kwargs.items():
        hboc__uwl = pjlp__admnd[argname]
        if hboc__uwl == 'scatter':
            tqq__qaa[argname] = bodo.scatterv(mlo__mzyg)
        elif hboc__uwl == 'bcast':
            lnv__frev.bcast(mlo__mzyg)
            tqq__qaa[argname] = mlo__mzyg
    dhdyh__zcoh = []
    for lgh__dsjdm, koti__vkdx in list(func.py_func.__globals__.items()):
        if isinstance(koti__vkdx, MasterModeDispatcher):
            dhdyh__zcoh.append((func.py_func.__globals__, lgh__dsjdm, func.
                py_func.__globals__[lgh__dsjdm]))
            func.py_func.__globals__[lgh__dsjdm] = koti__vkdx.dispatcher
    lhomb__lzkt = func(*rmas__npja, **tqq__qaa)
    for vbud__hypr, lgh__dsjdm, koti__vkdx in dhdyh__zcoh:
        vbud__hypr[lgh__dsjdm] = koti__vkdx
    if lhomb__lzkt is not None and func.overloads[func.signatures[0]].metadata[
        'is_return_distributed']:
        lhomb__lzkt = bodo.gatherv(lhomb__lzkt)
    return lhomb__lzkt


def init_master_mode():
    if bodo.get_size() == 1:
        return
    global master_mode_on
    assert master_mode_on is False, 'init_master_mode can only be called once on each process'
    master_mode_on = True
    assert sys.version_info[:2] >= (3, 8
        ), 'Python 3.8+ required for master mode'
    from bodo import jit
    globals()['jit'] = jit
    import cloudpickle
    from mpi4py import MPI
    globals()['pickle'] = cloudpickle
    globals()['MPI'] = MPI

    def master_exit():
        MPI.COMM_WORLD.bcast(['exit'])
    if bodo.get_rank() == MASTER_RANK:
        import atexit
        atexit.register(master_exit)
    else:
        worker_loop()
