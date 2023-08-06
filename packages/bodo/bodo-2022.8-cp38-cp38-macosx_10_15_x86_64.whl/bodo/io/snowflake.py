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
    kdx__zrhdc = tracing.Event('snowflake_connect', is_parallel=is_parallel)
    isvx__dyzl = urlparse(conn_str)
    irvlu__gole = {}
    if isvx__dyzl.username:
        irvlu__gole['user'] = isvx__dyzl.username
    if isvx__dyzl.password:
        irvlu__gole['password'] = isvx__dyzl.password
    if isvx__dyzl.hostname:
        irvlu__gole['account'] = isvx__dyzl.hostname
    if isvx__dyzl.port:
        irvlu__gole['port'] = isvx__dyzl.port
    if isvx__dyzl.path:
        vthj__oqs = isvx__dyzl.path
        if vthj__oqs.startswith('/'):
            vthj__oqs = vthj__oqs[1:]
        strg__ownn = vthj__oqs.split('/')
        if len(strg__ownn) == 2:
            mzw__mqhr, schema = strg__ownn
        elif len(strg__ownn) == 1:
            mzw__mqhr = strg__ownn[0]
            schema = None
        else:
            raise BodoError(
                f'Unexpected Snowflake connection string {conn_str}. Path is expected to contain database name and possibly schema'
                )
        irvlu__gole['database'] = mzw__mqhr
        if schema:
            irvlu__gole['schema'] = schema
    if isvx__dyzl.query:
        for pvmka__vebq, sjswt__apvp in parse_qsl(isvx__dyzl.query):
            irvlu__gole[pvmka__vebq] = sjswt__apvp
            if pvmka__vebq == 'session_parameters':
                import json
                irvlu__gole[pvmka__vebq] = json.loads(sjswt__apvp)
    irvlu__gole['application'] = 'bodo'
    try:
        import snowflake.connector
    except ImportError as bspnh__jlc:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    conn = snowflake.connector.connect(**irvlu__gole)
    kdx__zrhdc.finalize()
    return conn


class SnowflakeDataset(object):

    def __init__(self, batches, schema, conn):
        self.pieces = batches
        self._bodo_total_rows = 0
        for lolk__rew in batches:
            lolk__rew._bodo_num_rows = lolk__rew.rowcount
            self._bodo_total_rows += lolk__rew._bodo_num_rows
        self.schema = schema
        self.conn = conn


def get_dataset(query, conn_str):
    kdx__zrhdc = tracing.Event('get_snowflake_dataset')
    zdcdo__dicdj = MPI.COMM_WORLD
    conn = snowflake_connect(conn_str)
    if bodo.get_rank() == 0:
        nxmpt__xgbz = conn.cursor()
        mpj__lufux = tracing.Event('get_schema', is_parallel=False)
        dlbjj__bttq = f'select * from ({query}) x LIMIT {100}'
        okmy__ffwkl = nxmpt__xgbz.execute(dlbjj__bttq).fetch_arrow_all()
        if okmy__ffwkl is None:
            txs__aoq = nxmpt__xgbz.describe(query)
            wvymk__ara = [pa.field(ncaw__ocheg.name, FIELD_TYPE_TO_PA_TYPE[
                ncaw__ocheg.type_code]) for ncaw__ocheg in txs__aoq]
            schema = pa.schema(wvymk__ara)
        else:
            schema = okmy__ffwkl.schema
        mpj__lufux.finalize()
        whfym__cct = tracing.Event('execute_query', is_parallel=False)
        nxmpt__xgbz.execute(query)
        whfym__cct.finalize()
        batches = nxmpt__xgbz.get_result_batches()
        zdcdo__dicdj.bcast((batches, schema))
    else:
        batches, schema = zdcdo__dicdj.bcast(None)
    djgn__mxp = SnowflakeDataset(batches, schema, conn)
    kdx__zrhdc.finalize()
    return djgn__mxp


def create_internal_stage(cursor, is_temporary=False):
    kdx__zrhdc = tracing.Event('create_internal_stage', is_parallel=False)
    try:
        import snowflake.connector
    except ImportError as bspnh__jlc:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    stage_name = None
    rxrw__sqrxg = None
    while True:
        try:
            stage_name = f'bodo_io_snowflake_{uuid4()}'
            if is_temporary:
                vyndz__qrud = 'CREATE TEMPORARY STAGE'
            else:
                vyndz__qrud = 'CREATE STAGE'
            ppcfb__rttv = (
                f'{vyndz__qrud} "{stage_name}" /* Python:bodo.io.snowflake.create_internal_stage() */ '
                )
            cursor.execute(ppcfb__rttv, _is_internal=True).fetchall()
            break
        except snowflake.connector.ProgrammingError as eolaf__erdq:
            if eolaf__erdq.msg.endswith('already exists.'):
                continue
            rxrw__sqrxg = eolaf__erdq.msg
            break
    kdx__zrhdc.finalize()
    if rxrw__sqrxg is not None:
        raise snowflake.connector.ProgrammingError(rxrw__sqrxg)
    return stage_name


def drop_internal_stage(cursor, stage_name):
    kdx__zrhdc = tracing.Event('drop_internal_stage', is_parallel=False)
    mcx__rqlda = (
        f'DROP STAGE "{stage_name}" /* Python:bodo.io.snowflake.drop_internal_stage() */ '
        )
    cursor.execute(mcx__rqlda, _is_internal=True)
    kdx__zrhdc.finalize()


def do_upload_and_cleanup(cursor, chunk_idx, chunk_path, stage_name):

    def upload_cleanup_thread_func(chunk_idx, chunk_path, stage_name):
        tolnz__mad = tracing.Event(f'upload_parquet_file{chunk_idx}',
            is_parallel=False)
        yom__pziqh = (
            f'PUT \'file://{chunk_path}\' @"{stage_name}" AUTO_COMPRESS=FALSE /* Python:bodo.io.snowflake.do_upload_and_cleanup() */'
            )
        cursor.execute(yom__pziqh, _is_internal=True).fetchall()
        tolnz__mad.finalize()
        os.remove(chunk_path)
    if SF_WRITE_OVERLAP_UPLOAD:
        qjqql__djl = ExceptionPropagatingThread(target=
            upload_cleanup_thread_func, args=(chunk_idx, chunk_path,
            stage_name))
        qjqql__djl.start()
    else:
        upload_cleanup_thread_func(chunk_idx, chunk_path, stage_name)
        qjqql__djl = None
    return qjqql__djl


def create_table_handle_exists(cursor, stage_name, location, df_columns,
    if_exists):
    kdx__zrhdc = tracing.Event('create_table_if_not_exists', is_parallel=False)
    try:
        import snowflake.connector
    except ImportError as bspnh__jlc:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    aprr__bukk = None
    bsvw__zhbc = None
    if if_exists == 'fail':
        puk__lkc = 'CREATE TABLE'
    elif if_exists == 'replace':
        puk__lkc = 'CREATE OR REPLACE TABLE'
    elif if_exists == 'append':
        puk__lkc = 'CREATE TABLE IF NOT EXISTS'
    else:
        raise ValueError(f"'{if_exists}' is not valid for if_exists")
    akts__ffy = tracing.Event('create_file_format', is_parallel=False)
    while True:
        try:
            aprr__bukk = f'bodo_io_snowflake_write_{uuid4()}'
            lrri__reoyv = (
                f'CREATE FILE FORMAT "{aprr__bukk}" TYPE=PARQUET COMPRESSION=AUTO /* Python:bodo.io.snowflake.create_table_if_not_exists() */'
                )
            cursor.execute(lrri__reoyv, _is_internal=True)
            break
        except snowflake.connector.ProgrammingError as eolaf__erdq:
            if eolaf__erdq.msg.endswith('already exists.'):
                continue
            bsvw__zhbc = eolaf__erdq.msg
            break
    akts__ffy.finalize()
    if bsvw__zhbc is not None:
        raise snowflake.connector.ProgrammingError(bsvw__zhbc)
    oyvv__rtxhm = tracing.Event('infer_schema', is_parallel=False)
    lmu__scb = (
        f'SELECT COLUMN_NAME, TYPE FROM table(infer_schema(location=>\'@"{stage_name}"\', file_format=>\'"{aprr__bukk}"\')) /* Python:bodo.io.snowflake.create_table_if_not_exists() */'
        )
    qbwpv__kjbgo = dict(cursor.execute(lmu__scb, _is_internal=True).fetchall())
    oyvv__rtxhm.finalize()
    jksto__ccscq = tracing.Event('create_table', is_parallel=False)
    uqk__tiek = ', '.join([f'"{xffdd__xpmw}" {qbwpv__kjbgo[xffdd__xpmw]}' for
        xffdd__xpmw in df_columns])
    wtobo__sha = (
        f'{puk__lkc} {location} ({uqk__tiek}) /* Python:bodo.io.snowflake.create_table_if_not_exists() */'
        )
    cursor.execute(wtobo__sha, _is_internal=True)
    jksto__ccscq.finalize()
    xiiva__buimo = tracing.Event('drop_file_format', is_parallel=False)
    lrvgp__urf = (
        f'DROP FILE FORMAT IF EXISTS "{aprr__bukk}" /* Python:bodo.io.snowflake.create_table_if_not_exists() */'
        )
    cursor.execute(lrvgp__urf, _is_internal=True)
    xiiva__buimo.finalize()
    kdx__zrhdc.finalize()


def execute_copy_into(cursor, stage_name, location, df_columns):
    kdx__zrhdc = tracing.Event('execute_copy_into', is_parallel=False)
    jng__qzbe = ','.join([f'"{xffdd__xpmw}"' for xffdd__xpmw in df_columns])
    wcjg__qzdx = ','.join([f'$1:"{xffdd__xpmw}"' for xffdd__xpmw in df_columns]
        )
    elr__pqtb = (
        f'COPY INTO {location} ({jng__qzbe}) FROM (SELECT {wcjg__qzdx} FROM @"{stage_name}") FILE_FORMAT=(TYPE=PARQUET COMPRESSION=AUTO) PURGE=TRUE ON_ERROR={SF_WRITE_COPY_INTO_ON_ERROR} /* Python:bodo.io.snowflake.execute_copy_into() */'
        )
    mcx__ebem = cursor.execute(elr__pqtb, _is_internal=True).fetchall()
    dgcp__nke = sum(1 if riqs__dcte[1] == 'LOADED' else 0 for riqs__dcte in
        mcx__ebem)
    jtcsn__hjhk = len(mcx__ebem)
    yldta__rdoj = sum(int(riqs__dcte[3]) for riqs__dcte in mcx__ebem)
    qwu__shui = dgcp__nke, jtcsn__hjhk, yldta__rdoj, mcx__ebem
    kdx__zrhdc.add_attribute('copy_into_nsuccess', dgcp__nke)
    kdx__zrhdc.add_attribute('copy_into_nchunks', jtcsn__hjhk)
    kdx__zrhdc.add_attribute('copy_into_nrows', yldta__rdoj)
    if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
        print(f'[Snowflake Write] copy_into results: {repr(mcx__ebem)}')
    kdx__zrhdc.finalize()
    return qwu__shui


try:
    import snowflake.connector
    snowflake_connector_cursor_python_type = (snowflake.connector.cursor.
        SnowflakeCursor)
except ImportError as bspnh__jlc:
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
    kdx__zrhdc = tracing.Event('get_snowflake_stage_info', is_parallel=False)
    nmgq__fxwg = os.path.join(tmp_folder.name,
        f'get_credentials_{uuid4()}.parquet')
    nmgq__fxwg = nmgq__fxwg.replace('\\', '\\\\').replace("'", "\\'")
    yom__pziqh = (
        f'PUT \'file://{nmgq__fxwg}\' @"{stage_name}" AUTO_COMPRESS=FALSE /* Python:bodo.io.snowflake.get_snowflake_stage_info() */'
        )
    zvmo__oynwa = cursor._execute_helper(yom__pziqh, is_internal=True)
    kdx__zrhdc.finalize()
    return zvmo__oynwa


def connect_and_get_upload_info(conn):
    kdx__zrhdc = tracing.Event('connect_and_get_upload_info')
    zdcdo__dicdj = MPI.COMM_WORLD
    fpw__stv = zdcdo__dicdj.Get_rank()
    tmp_folder = TemporaryDirectory()
    cursor = None
    stage_name = ''
    bhwnt__gbym = ''
    knckp__xfwu = {}
    old_creds = {}
    ezy__xgt = None
    if fpw__stv == 0:
        try:
            conn = snowflake_connect(conn)
            cursor = conn.cursor()
            is_temporary = not SF_WRITE_UPLOAD_USING_PUT
            stage_name = create_internal_stage(cursor, is_temporary=
                is_temporary)
            if SF_WRITE_UPLOAD_USING_PUT:
                bhwnt__gbym = ''
            else:
                zvmo__oynwa = get_snowflake_stage_info(cursor, stage_name,
                    tmp_folder)
                maz__mte = zvmo__oynwa['data']['uploadInfo']
                if maz__mte['locationType'] == 'S3':
                    urjs__mcefi, fin__qfac, vthj__oqs = maz__mte['location'
                        ].partition('/')
                    vthj__oqs = vthj__oqs.rstrip('/')
                    bhwnt__gbym = f's3://{urjs__mcefi}/{vthj__oqs}/'
                    knckp__xfwu = {'AWS_ACCESS_KEY_ID': maz__mte['creds'][
                        'AWS_KEY_ID'], 'AWS_SECRET_ACCESS_KEY': maz__mte[
                        'creds']['AWS_SECRET_KEY'], 'AWS_SESSION_TOKEN':
                        maz__mte['creds']['AWS_TOKEN'],
                        'AWS_DEFAULT_REGION': maz__mte['region']}
                else:
                    warnings.warn(BodoWarning(
                        f"Direct upload to stage is not supported for internal stage type '{maz__mte['locationType']}'. Falling back to PUT command for upload."
                        ))
                    drop_internal_stage(cursor, stage_name)
                    stage_name = create_internal_stage(cursor, is_temporary
                        =False)
        except Exception as riqs__dcte:
            ezy__xgt = riqs__dcte
    ezy__xgt = zdcdo__dicdj.bcast(ezy__xgt)
    if isinstance(ezy__xgt, Exception):
        raise ezy__xgt
    bhwnt__gbym = zdcdo__dicdj.bcast(bhwnt__gbym)
    if bhwnt__gbym == '':
        bsrke__vfpn = True
        bhwnt__gbym = tmp_folder.name + '/'
        if fpw__stv != 0:
            conn = snowflake_connect(conn)
            cursor = conn.cursor()
    else:
        bsrke__vfpn = False
        knckp__xfwu = zdcdo__dicdj.bcast(knckp__xfwu)
        old_creds = update_env_vars(knckp__xfwu)
    stage_name = zdcdo__dicdj.bcast(stage_name)
    kdx__zrhdc.finalize()
    return cursor, tmp_folder, stage_name, bhwnt__gbym, bsrke__vfpn, old_creds


def create_table_copy_into(cursor, stage_name, location, df_columns,
    if_exists, old_creds, tmp_folder):
    kdx__zrhdc = tracing.Event('create_table_copy_into', is_parallel=False)
    zdcdo__dicdj = MPI.COMM_WORLD
    fpw__stv = zdcdo__dicdj.Get_rank()
    ezy__xgt = None
    if fpw__stv == 0:
        try:
            pyp__wnr = (
                'BEGIN /* Python:bodo.io.snowflake.create_table_copy_into() */'
                )
            cursor.execute(pyp__wnr)
            create_table_handle_exists(cursor, stage_name, location,
                df_columns, if_exists)
            dgcp__nke, jtcsn__hjhk, yldta__rdoj, linqk__ydif = (
                execute_copy_into(cursor, stage_name, location, df_columns))
            if dgcp__nke != jtcsn__hjhk:
                raise BodoError(
                    f'Snowflake write copy_into failed: {linqk__ydif}')
            tku__bmt = (
                'COMMIT /* Python:bodo.io.snowflake.create_table_copy_into() */'
                )
            cursor.execute(tku__bmt)
            drop_internal_stage(cursor, stage_name)
            cursor.close()
        except Exception as riqs__dcte:
            ezy__xgt = riqs__dcte
    ezy__xgt = zdcdo__dicdj.bcast(ezy__xgt)
    if isinstance(ezy__xgt, Exception):
        raise ezy__xgt
    update_env_vars(old_creds)
    tmp_folder.cleanup()
    kdx__zrhdc.finalize()
