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
        bbsxh__xpna = state
        bzmoi__lihdo = inspect.getsourcelines(bbsxh__xpna)[0][0]
        assert bzmoi__lihdo.startswith('@bodo.jit') or bzmoi__lihdo.startswith(
            '@jit')
        sfyex__dai = eval(bzmoi__lihdo[1:])
        self.dispatcher = sfyex__dai(bbsxh__xpna)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    mez__uuj = MPI.COMM_WORLD
    while True:
        mszfy__ylmkf = mez__uuj.bcast(None, root=MASTER_RANK)
        if mszfy__ylmkf[0] == 'exec':
            bbsxh__xpna = pickle.loads(mszfy__ylmkf[1])
            for czyj__kzq, fubi__kbs in list(bbsxh__xpna.__globals__.items()):
                if isinstance(fubi__kbs, MasterModeDispatcher):
                    bbsxh__xpna.__globals__[czyj__kzq] = fubi__kbs.dispatcher
            if bbsxh__xpna.__module__ not in sys.modules:
                sys.modules[bbsxh__xpna.__module__] = pytypes.ModuleType(
                    bbsxh__xpna.__module__)
            bzmoi__lihdo = inspect.getsourcelines(bbsxh__xpna)[0][0]
            assert bzmoi__lihdo.startswith('@bodo.jit'
                ) or bzmoi__lihdo.startswith('@jit')
            sfyex__dai = eval(bzmoi__lihdo[1:])
            func = sfyex__dai(bbsxh__xpna)
            nlwj__iftuy = mszfy__ylmkf[2]
            bol__uzb = mszfy__ylmkf[3]
            vnii__mbrpf = []
            for lbuul__nyspw in nlwj__iftuy:
                if lbuul__nyspw == 'scatter':
                    vnii__mbrpf.append(bodo.scatterv(None))
                elif lbuul__nyspw == 'bcast':
                    vnii__mbrpf.append(mez__uuj.bcast(None, root=MASTER_RANK))
            yxn__zyd = {}
            for argname, lbuul__nyspw in bol__uzb.items():
                if lbuul__nyspw == 'scatter':
                    yxn__zyd[argname] = bodo.scatterv(None)
                elif lbuul__nyspw == 'bcast':
                    yxn__zyd[argname] = mez__uuj.bcast(None, root=MASTER_RANK)
            ndjyc__qzcbd = func(*vnii__mbrpf, **yxn__zyd)
            if ndjyc__qzcbd is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(ndjyc__qzcbd)
            del (mszfy__ylmkf, bbsxh__xpna, func, sfyex__dai, nlwj__iftuy,
                bol__uzb, vnii__mbrpf, yxn__zyd, ndjyc__qzcbd)
            gc.collect()
        elif mszfy__ylmkf[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    mez__uuj = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        nlwj__iftuy = ['scatter' for ukrc__ziqy in range(len(args))]
        bol__uzb = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        yilaw__qdvm = func.py_func.__code__.co_varnames
        zjp__tdlc = func.targetoptions

        def get_distribution(argname):
            if argname in zjp__tdlc.get('distributed', []
                ) or argname in zjp__tdlc.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        nlwj__iftuy = [get_distribution(argname) for argname in yilaw__qdvm
            [:len(args)]]
        bol__uzb = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    gpbk__ajisq = pickle.dumps(func.py_func)
    mez__uuj.bcast(['exec', gpbk__ajisq, nlwj__iftuy, bol__uzb])
    vnii__mbrpf = []
    for rtta__thx, lbuul__nyspw in zip(args, nlwj__iftuy):
        if lbuul__nyspw == 'scatter':
            vnii__mbrpf.append(bodo.scatterv(rtta__thx))
        elif lbuul__nyspw == 'bcast':
            mez__uuj.bcast(rtta__thx)
            vnii__mbrpf.append(rtta__thx)
    yxn__zyd = {}
    for argname, rtta__thx in kwargs.items():
        lbuul__nyspw = bol__uzb[argname]
        if lbuul__nyspw == 'scatter':
            yxn__zyd[argname] = bodo.scatterv(rtta__thx)
        elif lbuul__nyspw == 'bcast':
            mez__uuj.bcast(rtta__thx)
            yxn__zyd[argname] = rtta__thx
    jnvq__xxbm = []
    for czyj__kzq, fubi__kbs in list(func.py_func.__globals__.items()):
        if isinstance(fubi__kbs, MasterModeDispatcher):
            jnvq__xxbm.append((func.py_func.__globals__, czyj__kzq, func.
                py_func.__globals__[czyj__kzq]))
            func.py_func.__globals__[czyj__kzq] = fubi__kbs.dispatcher
    ndjyc__qzcbd = func(*vnii__mbrpf, **yxn__zyd)
    for xjxmi__xbeyc, czyj__kzq, fubi__kbs in jnvq__xxbm:
        xjxmi__xbeyc[czyj__kzq] = fubi__kbs
    if ndjyc__qzcbd is not None and func.overloads[func.signatures[0]
        ].metadata['is_return_distributed']:
        ndjyc__qzcbd = bodo.gatherv(ndjyc__qzcbd)
    return ndjyc__qzcbd


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
