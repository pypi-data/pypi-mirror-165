import os
import shutil
from contextlib import contextmanager
from pathlib import Path
import bodo
cwd = Path(__file__).resolve().parent
datadir = cwd.parent / 'tests' / 'data'


@bodo.jit
def get_rank():
    return bodo.libs.distributed_api.get_rank()


@bodo.jit
def barrier():
    return bodo.libs.distributed_api.barrier()


@contextmanager
def ensure_clean(filename):
    try:
        yield
    finally:
        try:
            barrier()
            if get_rank() == 0 and os.path.exists(filename) and os.path.isfile(
                filename):
                os.remove(filename)
        except Exception as fyrz__dxdh:
            print('Exception on removing file: {error}'.format(error=
                fyrz__dxdh))


@contextmanager
def ensure_clean_dir(dirname):
    try:
        yield
    finally:
        try:
            barrier()
            if get_rank() == 0 and os.path.exists(dirname) and os.path.isdir(
                dirname):
                shutil.rmtree(dirname)
        except Exception as fyrz__dxdh:
            print('Exception on removing directory: {error}'.format(error=
                fyrz__dxdh))


@contextmanager
def ensure_clean2(pathname):
    try:
        yield
    finally:
        barrier()
        if get_rank() == 0:
            try:
                if os.path.exists(pathname) and os.path.isfile(pathname):
                    os.remove(pathname)
            except Exception as fyrz__dxdh:
                print('Exception on removing file: {error}'.format(error=
                    fyrz__dxdh))
            try:
                if os.path.exists(pathname) and os.path.isdir(pathname):
                    shutil.rmtree(pathname)
            except Exception as fyrz__dxdh:
                print('Exception on removing directory: {error}'.format(
                    error=fyrz__dxdh))


@contextmanager
def ensure_clean_mysql_psql_table(conn, table_name_prefix='test_small_table'):
    import uuid
    from mpi4py import MPI
    from sqlalchemy import create_engine
    chrc__vcbnn = MPI.COMM_WORLD
    try:
        nvap__evuh = None
        if bodo.get_rank() == 0:
            nvap__evuh = f'{table_name_prefix}_{uuid.uuid4()}'
        nvap__evuh = chrc__vcbnn.bcast(nvap__evuh)
        yield nvap__evuh
    finally:
        bodo.barrier()
        wardj__wmfa = None
        if bodo.get_rank() == 0:
            try:
                vnko__gba = create_engine(conn)
                hgdor__vchd = vnko__gba.connect()
                hgdor__vchd.execute(f'drop table if exists `{nvap__evuh}`')
            except Exception as fyrz__dxdh:
                wardj__wmfa = fyrz__dxdh
        wardj__wmfa = chrc__vcbnn.bcast(wardj__wmfa)
        if isinstance(wardj__wmfa, Exception):
            raise wardj__wmfa
