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
        except Exception as zcugk__dylz:
            print('Exception on removing file: {error}'.format(error=
                zcugk__dylz))


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
        except Exception as zcugk__dylz:
            print('Exception on removing directory: {error}'.format(error=
                zcugk__dylz))


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
            except Exception as zcugk__dylz:
                print('Exception on removing file: {error}'.format(error=
                    zcugk__dylz))
            try:
                if os.path.exists(pathname) and os.path.isdir(pathname):
                    shutil.rmtree(pathname)
            except Exception as zcugk__dylz:
                print('Exception on removing directory: {error}'.format(
                    error=zcugk__dylz))


@contextmanager
def ensure_clean_mysql_psql_table(conn, table_name_prefix='test_small_table'):
    import uuid
    from mpi4py import MPI
    from sqlalchemy import create_engine
    utu__vaofz = MPI.COMM_WORLD
    try:
        rvvn__vmb = None
        if bodo.get_rank() == 0:
            rvvn__vmb = f'{table_name_prefix}_{uuid.uuid4()}'
        rvvn__vmb = utu__vaofz.bcast(rvvn__vmb)
        yield rvvn__vmb
    finally:
        bodo.barrier()
        rikyb__dhls = None
        if bodo.get_rank() == 0:
            try:
                egv__nek = create_engine(conn)
                caugf__pzri = egv__nek.connect()
                caugf__pzri.execute(f'drop table if exists `{rvvn__vmb}`')
            except Exception as zcugk__dylz:
                rikyb__dhls = zcugk__dylz
        rikyb__dhls = utu__vaofz.bcast(rikyb__dhls)
        if isinstance(rikyb__dhls, Exception):
            raise rikyb__dhls
