import os
import sys
import warnings
from tempfile import TemporaryDirectory
from urllib.parse import parse_qsl, urlparse
from uuid import uuid4
import pyarrow as pa
from mpi4py import MPI
import bodo
from bodo.io.helpers import ExceptionPropagatingThread, update_env_vars
from bodo.utils import tracing
from bodo.utils.py_objs import install_py_obj_class
from bodo.utils.typing import BodoError, BodoWarning
DICT_ENCODE_CRITERION = 0.5
FIELD_TYPE_TO_PA_TYPE = [pa.int64(), pa.float64(), pa.string(), pa.date32(),
    pa.timestamp('ns'), pa.string(), pa.timestamp('ns'), pa.timestamp('ns'),
    pa.timestamp('ns'), pa.string(), pa.string(), pa.binary(), pa.time64(
    'ns'), pa.bool_()]
SF_WRITE_COPY_INTO_ON_ERROR = 'abort_statement'
SF_WRITE_OVERLAP_UPLOAD = True
SF_WRITE_PARQUET_CHUNK_SIZE = int(256000000.0)
SF_WRITE_PARQUET_COMPRESSION = 'snappy'
SF_WRITE_UPLOAD_USING_PUT = False


def snowflake_connect(conn_str, is_parallel=False):
    onc__obck = tracing.Event('snowflake_connect', is_parallel=is_parallel)
    wdara__hxe = urlparse(conn_str)
    eos__qdoz = {}
    if wdara__hxe.username:
        eos__qdoz['user'] = wdara__hxe.username
    if wdara__hxe.password:
        eos__qdoz['password'] = wdara__hxe.password
    if wdara__hxe.hostname:
        eos__qdoz['account'] = wdara__hxe.hostname
    if wdara__hxe.port:
        eos__qdoz['port'] = wdara__hxe.port
    if wdara__hxe.path:
        ezjq__swjl = wdara__hxe.path
        if ezjq__swjl.startswith('/'):
            ezjq__swjl = ezjq__swjl[1:]
        spqb__xyll = ezjq__swjl.split('/')
        if len(spqb__xyll) == 2:
            ywaup__vrg, schema = spqb__xyll
        elif len(spqb__xyll) == 1:
            ywaup__vrg = spqb__xyll[0]
            schema = None
        else:
            raise BodoError(
                f'Unexpected Snowflake connection string {conn_str}. Path is expected to contain database name and possibly schema'
                )
        eos__qdoz['database'] = ywaup__vrg
        if schema:
            eos__qdoz['schema'] = schema
    if wdara__hxe.query:
        for adhc__kvzic, kcoy__itza in parse_qsl(wdara__hxe.query):
            eos__qdoz[adhc__kvzic] = kcoy__itza
            if adhc__kvzic == 'session_parameters':
                import json
                eos__qdoz[adhc__kvzic] = json.loads(kcoy__itza)
    eos__qdoz['application'] = 'bodo'
    try:
        import snowflake.connector
    except ImportError as szfs__rbeg:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    conn = snowflake.connector.connect(**eos__qdoz)
    onc__obck.finalize()
    return conn


class SnowflakeDataset(object):

    def __init__(self, batches, schema, conn):
        self.pieces = batches
        self._bodo_total_rows = 0
        for nhclk__drmno in batches:
            nhclk__drmno._bodo_num_rows = nhclk__drmno.rowcount
            self._bodo_total_rows += nhclk__drmno._bodo_num_rows
        self.schema = schema
        self.conn = conn


def get_dataset(query, conn_str):
    onc__obck = tracing.Event('get_snowflake_dataset')
    ypwe__wore = MPI.COMM_WORLD
    conn = snowflake_connect(conn_str)
    if bodo.get_rank() == 0:
        qdfqm__czixj = conn.cursor()
        fbyk__mwlb = tracing.Event('get_schema', is_parallel=False)
        edn__pdi = f'select * from ({query}) x LIMIT {100}'
        edob__ofi = qdfqm__czixj.execute(edn__pdi).fetch_arrow_all()
        if edob__ofi is None:
            tkfpq__pnwf = qdfqm__czixj.describe(query)
            slx__yefp = [pa.field(mov__umb.name, FIELD_TYPE_TO_PA_TYPE[
                mov__umb.type_code]) for mov__umb in tkfpq__pnwf]
            schema = pa.schema(slx__yefp)
        else:
            schema = edob__ofi.schema
        fbyk__mwlb.finalize()
        ysqqg__pkt = tracing.Event('execute_query', is_parallel=False)
        qdfqm__czixj.execute(query)
        ysqqg__pkt.finalize()
        batches = qdfqm__czixj.get_result_batches()
        ypwe__wore.bcast((batches, schema))
    else:
        batches, schema = ypwe__wore.bcast(None)
    glrmv__tewp = SnowflakeDataset(batches, schema, conn)
    onc__obck.finalize()
    return glrmv__tewp


def create_internal_stage(cursor, is_temporary=False):
    onc__obck = tracing.Event('create_internal_stage', is_parallel=False)
    try:
        import snowflake.connector
    except ImportError as szfs__rbeg:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    stage_name = None
    thl__kxk = None
    while True:
        try:
            stage_name = f'bodo_io_snowflake_{uuid4()}'
            if is_temporary:
                qztpz__rck = 'CREATE TEMPORARY STAGE'
            else:
                qztpz__rck = 'CREATE STAGE'
            jxgc__xibz = (
                f'{qztpz__rck} "{stage_name}" /* Python:bodo.io.snowflake.create_internal_stage() */ '
                )
            cursor.execute(jxgc__xibz, _is_internal=True).fetchall()
            break
        except snowflake.connector.ProgrammingError as gpoyp__egh:
            if gpoyp__egh.msg.endswith('already exists.'):
                continue
            thl__kxk = gpoyp__egh.msg
            break
    onc__obck.finalize()
    if thl__kxk is not None:
        raise snowflake.connector.ProgrammingError(thl__kxk)
    return stage_name


def drop_internal_stage(cursor, stage_name):
    onc__obck = tracing.Event('drop_internal_stage', is_parallel=False)
    mntkk__nxzfl = (
        f'DROP STAGE "{stage_name}" /* Python:bodo.io.snowflake.drop_internal_stage() */ '
        )
    cursor.execute(mntkk__nxzfl, _is_internal=True)
    onc__obck.finalize()


def do_upload_and_cleanup(cursor, chunk_idx, chunk_path, stage_name):

    def upload_cleanup_thread_func(chunk_idx, chunk_path, stage_name):
        xcbhr__nhs = tracing.Event(f'upload_parquet_file{chunk_idx}',
            is_parallel=False)
        wngzf__bydf = (
            f'PUT \'file://{chunk_path}\' @"{stage_name}" AUTO_COMPRESS=FALSE /* Python:bodo.io.snowflake.do_upload_and_cleanup() */'
            )
        cursor.execute(wngzf__bydf, _is_internal=True).fetchall()
        xcbhr__nhs.finalize()
        os.remove(chunk_path)
    if SF_WRITE_OVERLAP_UPLOAD:
        zhg__kbxx = ExceptionPropagatingThread(target=
            upload_cleanup_thread_func, args=(chunk_idx, chunk_path,
            stage_name))
        zhg__kbxx.start()
    else:
        upload_cleanup_thread_func(chunk_idx, chunk_path, stage_name)
        zhg__kbxx = None
    return zhg__kbxx


def create_table_handle_exists(cursor, stage_name, location, df_columns,
    if_exists):
    onc__obck = tracing.Event('create_table_if_not_exists', is_parallel=False)
    try:
        import snowflake.connector
    except ImportError as szfs__rbeg:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    fmy__urvsz = None
    xzg__lhbdv = None
    if if_exists == 'fail':
        aaw__qijxv = 'CREATE TABLE'
    elif if_exists == 'replace':
        aaw__qijxv = 'CREATE OR REPLACE TABLE'
    elif if_exists == 'append':
        aaw__qijxv = 'CREATE TABLE IF NOT EXISTS'
    else:
        raise ValueError(f"'{if_exists}' is not valid for if_exists")
    bdn__ecwak = tracing.Event('create_file_format', is_parallel=False)
    while True:
        try:
            fmy__urvsz = f'bodo_io_snowflake_write_{uuid4()}'
            ayu__sder = (
                f'CREATE FILE FORMAT "{fmy__urvsz}" TYPE=PARQUET COMPRESSION=AUTO /* Python:bodo.io.snowflake.create_table_if_not_exists() */'
                )
            cursor.execute(ayu__sder, _is_internal=True)
            break
        except snowflake.connector.ProgrammingError as gpoyp__egh:
            if gpoyp__egh.msg.endswith('already exists.'):
                continue
            xzg__lhbdv = gpoyp__egh.msg
            break
    bdn__ecwak.finalize()
    if xzg__lhbdv is not None:
        raise snowflake.connector.ProgrammingError(xzg__lhbdv)
    lmix__rvir = tracing.Event('infer_schema', is_parallel=False)
    sqt__ujtaf = (
        f'SELECT COLUMN_NAME, TYPE FROM table(infer_schema(location=>\'@"{stage_name}"\', file_format=>\'"{fmy__urvsz}"\')) /* Python:bodo.io.snowflake.create_table_if_not_exists() */'
        )
    grnhv__xsek = dict(cursor.execute(sqt__ujtaf, _is_internal=True).fetchall()
        )
    lmix__rvir.finalize()
    vqkk__klb = tracing.Event('create_table', is_parallel=False)
    yjvt__vqfg = ', '.join([f'"{iczoj__brilb}" {grnhv__xsek[iczoj__brilb]}' for
        iczoj__brilb in df_columns])
    ztqn__exw = (
        f'{aaw__qijxv} {location} ({yjvt__vqfg}) /* Python:bodo.io.snowflake.create_table_if_not_exists() */'
        )
    cursor.execute(ztqn__exw, _is_internal=True)
    vqkk__klb.finalize()
    sin__vpb = tracing.Event('drop_file_format', is_parallel=False)
    ogtho__rvnps = (
        f'DROP FILE FORMAT IF EXISTS "{fmy__urvsz}" /* Python:bodo.io.snowflake.create_table_if_not_exists() */'
        )
    cursor.execute(ogtho__rvnps, _is_internal=True)
    sin__vpb.finalize()
    onc__obck.finalize()


def execute_copy_into(cursor, stage_name, location, df_columns):
    onc__obck = tracing.Event('execute_copy_into', is_parallel=False)
    xqvd__bejob = ','.join([f'"{iczoj__brilb}"' for iczoj__brilb in df_columns]
        )
    tjdgd__zrtnw = ','.join([f'$1:"{iczoj__brilb}"' for iczoj__brilb in
        df_columns])
    awvo__qfcvq = (
        f'COPY INTO {location} ({xqvd__bejob}) FROM (SELECT {tjdgd__zrtnw} FROM @"{stage_name}") FILE_FORMAT=(TYPE=PARQUET COMPRESSION=AUTO) PURGE=TRUE ON_ERROR={SF_WRITE_COPY_INTO_ON_ERROR} /* Python:bodo.io.snowflake.execute_copy_into() */'
        )
    qxa__wndy = cursor.execute(awvo__qfcvq, _is_internal=True).fetchall()
    skgjr__bghah = sum(1 if kkisp__aoqte[1] == 'LOADED' else 0 for
        kkisp__aoqte in qxa__wndy)
    rbbsl__mmhd = len(qxa__wndy)
    subu__wcfie = sum(int(kkisp__aoqte[3]) for kkisp__aoqte in qxa__wndy)
    xxq__clj = skgjr__bghah, rbbsl__mmhd, subu__wcfie, qxa__wndy
    onc__obck.add_attribute('copy_into_nsuccess', skgjr__bghah)
    onc__obck.add_attribute('copy_into_nchunks', rbbsl__mmhd)
    onc__obck.add_attribute('copy_into_nrows', subu__wcfie)
    if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
        print(f'[Snowflake Write] copy_into results: {repr(qxa__wndy)}')
    onc__obck.finalize()
    return xxq__clj


try:
    import snowflake.connector
    snowflake_connector_cursor_python_type = (snowflake.connector.cursor.
        SnowflakeCursor)
except ImportError as szfs__rbeg:
    snowflake_connector_cursor_python_type = None
SnowflakeConnectorCursorType = install_py_obj_class(types_name=
    'snowflake_connector_cursor_type', python_type=
    snowflake_connector_cursor_python_type, module=sys.modules[__name__],
    class_name='SnowflakeConnectorCursorType', model_name=
    'SnowflakeConnectorCursorModel')
TemporaryDirectoryType = install_py_obj_class(types_name=
    'temporary_directory_type', python_type=TemporaryDirectory, module=sys.
    modules[__name__], class_name='TemporaryDirectoryType', model_name=
    'TemporaryDirectoryModel')


def get_snowflake_stage_info(cursor, stage_name, tmp_folder):
    onc__obck = tracing.Event('get_snowflake_stage_info', is_parallel=False)
    ssu__dnur = os.path.join(tmp_folder.name,
        f'get_credentials_{uuid4()}.parquet')
    ssu__dnur = ssu__dnur.replace('\\', '\\\\').replace("'", "\\'")
    wngzf__bydf = (
        f'PUT \'file://{ssu__dnur}\' @"{stage_name}" AUTO_COMPRESS=FALSE /* Python:bodo.io.snowflake.get_snowflake_stage_info() */'
        )
    bkx__badc = cursor._execute_helper(wngzf__bydf, is_internal=True)
    onc__obck.finalize()
    return bkx__badc


def connect_and_get_upload_info(conn):
    onc__obck = tracing.Event('connect_and_get_upload_info')
    ypwe__wore = MPI.COMM_WORLD
    keg__xby = ypwe__wore.Get_rank()
    tmp_folder = TemporaryDirectory()
    cursor = None
    stage_name = ''
    cgzg__ckz = ''
    pdp__oxa = {}
    old_creds = {}
    oteif__ged = None
    if keg__xby == 0:
        try:
            conn = snowflake_connect(conn)
            cursor = conn.cursor()
            is_temporary = not SF_WRITE_UPLOAD_USING_PUT
            stage_name = create_internal_stage(cursor, is_temporary=
                is_temporary)
            if SF_WRITE_UPLOAD_USING_PUT:
                cgzg__ckz = ''
            else:
                bkx__badc = get_snowflake_stage_info(cursor, stage_name,
                    tmp_folder)
                fatfe__hmqw = bkx__badc['data']['uploadInfo']
                if fatfe__hmqw['locationType'] == 'S3':
                    cwrkk__lcrim, kegji__lshm, ezjq__swjl = fatfe__hmqw[
                        'location'].partition('/')
                    ezjq__swjl = ezjq__swjl.rstrip('/')
                    cgzg__ckz = f's3://{cwrkk__lcrim}/{ezjq__swjl}/'
                    pdp__oxa = {'AWS_ACCESS_KEY_ID': fatfe__hmqw['creds'][
                        'AWS_KEY_ID'], 'AWS_SECRET_ACCESS_KEY': fatfe__hmqw
                        ['creds']['AWS_SECRET_KEY'], 'AWS_SESSION_TOKEN':
                        fatfe__hmqw['creds']['AWS_TOKEN'],
                        'AWS_DEFAULT_REGION': fatfe__hmqw['region']}
                else:
                    warnings.warn(BodoWarning(
                        f"Direct upload to stage is not supported for internal stage type '{fatfe__hmqw['locationType']}'. Falling back to PUT command for upload."
                        ))
                    drop_internal_stage(cursor, stage_name)
                    stage_name = create_internal_stage(cursor, is_temporary
                        =False)
        except Exception as kkisp__aoqte:
            oteif__ged = kkisp__aoqte
    oteif__ged = ypwe__wore.bcast(oteif__ged)
    if isinstance(oteif__ged, Exception):
        raise oteif__ged
    cgzg__ckz = ypwe__wore.bcast(cgzg__ckz)
    if cgzg__ckz == '':
        sxp__cnl = True
        cgzg__ckz = tmp_folder.name + '/'
        if keg__xby != 0:
            conn = snowflake_connect(conn)
            cursor = conn.cursor()
    else:
        sxp__cnl = False
        pdp__oxa = ypwe__wore.bcast(pdp__oxa)
        old_creds = update_env_vars(pdp__oxa)
    stage_name = ypwe__wore.bcast(stage_name)
    onc__obck.finalize()
    return cursor, tmp_folder, stage_name, cgzg__ckz, sxp__cnl, old_creds


def create_table_copy_into(cursor, stage_name, location, df_columns,
    if_exists, old_creds, tmp_folder):
    onc__obck = tracing.Event('create_table_copy_into', is_parallel=False)
    ypwe__wore = MPI.COMM_WORLD
    keg__xby = ypwe__wore.Get_rank()
    oteif__ged = None
    if keg__xby == 0:
        try:
            oze__yfvjv = (
                'BEGIN /* Python:bodo.io.snowflake.create_table_copy_into() */'
                )
            cursor.execute(oze__yfvjv)
            create_table_handle_exists(cursor, stage_name, location,
                df_columns, if_exists)
            skgjr__bghah, rbbsl__mmhd, subu__wcfie, qzl__xbu = (
                execute_copy_into(cursor, stage_name, location, df_columns))
            if skgjr__bghah != rbbsl__mmhd:
                raise BodoError(f'Snowflake write copy_into failed: {qzl__xbu}'
                    )
            bvq__ted = (
                'COMMIT /* Python:bodo.io.snowflake.create_table_copy_into() */'
                )
            cursor.execute(bvq__ted)
            drop_internal_stage(cursor, stage_name)
            cursor.close()
        except Exception as kkisp__aoqte:
            oteif__ged = kkisp__aoqte
    oteif__ged = ypwe__wore.bcast(oteif__ged)
    if isinstance(oteif__ged, Exception):
        raise oteif__ged
    update_env_vars(old_creds)
    tmp_folder.cleanup()
    onc__obck.finalize()
