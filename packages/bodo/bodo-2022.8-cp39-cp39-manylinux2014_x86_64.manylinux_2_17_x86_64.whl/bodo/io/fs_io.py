"""
S3 & Hadoop file system supports, and file system dependent calls
"""
import glob
import os
import warnings
from urllib.parse import urlparse
import llvmlite.binding as ll
import numba
import numpy as np
from fsspec.implementations.arrow import ArrowFile, ArrowFSWrapper, wrap_exceptions
from numba.core import types
from numba.extending import NativeValue, models, overload, register_model, unbox
import bodo
from bodo.io import csv_cpp
from bodo.libs.distributed_api import Reduce_Type
from bodo.libs.str_ext import unicode_to_utf8, unicode_to_utf8_and_len
from bodo.utils.typing import BodoError, BodoWarning, get_overload_constant_dict
from bodo.utils.utils import check_java_installation


def fsspec_arrowfswrapper__open(self, path, mode='rb', block_size=None, **
    kwargs):
    if mode == 'rb':
        try:
            azcr__mokvd = self.fs.open_input_file(path)
        except:
            azcr__mokvd = self.fs.open_input_stream(path)
    elif mode == 'wb':
        azcr__mokvd = self.fs.open_output_stream(path)
    else:
        raise ValueError(f'unsupported mode for Arrow filesystem: {mode!r}')
    return ArrowFile(self, azcr__mokvd, path, mode, block_size, **kwargs)


ArrowFSWrapper._open = wrap_exceptions(fsspec_arrowfswrapper__open)
_csv_write = types.ExternalFunction('csv_write', types.void(types.voidptr,
    types.voidptr, types.int64, types.int64, types.bool_, types.voidptr,
    types.voidptr))
ll.add_symbol('csv_write', csv_cpp.csv_write)
bodo_error_msg = """
    Some possible causes:
        (1) Incorrect path: Specified file/directory doesn't exist or is unreachable.
        (2) Missing credentials: You haven't provided S3 credentials, neither through 
            environment variables, nor through a local AWS setup 
            that makes the credentials available at ~/.aws/credentials.
        (3) Incorrect credentials: Your S3 credentials are incorrect or do not have
            the correct permissions.
        (4) Wrong bucket region is used. Set AWS_DEFAULT_REGION variable with correct bucket region.
    """


def get_proxy_uri_from_env_vars():
    return os.environ.get('http_proxy', None) or os.environ.get('https_proxy',
        None) or os.environ.get('HTTP_PROXY', None) or os.environ.get(
        'HTTPS_PROXY', None)


def get_s3_fs(region=None, storage_options=None):
    from pyarrow.fs import S3FileSystem
    uofq__fqs = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    wtfpx__jru = False
    hpy__uibl = get_proxy_uri_from_env_vars()
    if storage_options:
        wtfpx__jru = storage_options.get('anon', False)
    return S3FileSystem(anonymous=wtfpx__jru, region=region,
        endpoint_override=uofq__fqs, proxy_options=hpy__uibl)


def get_s3_subtree_fs(bucket_name, region=None, storage_options=None):
    from pyarrow._fs import SubTreeFileSystem
    from pyarrow._s3fs import S3FileSystem
    uofq__fqs = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    wtfpx__jru = False
    hpy__uibl = get_proxy_uri_from_env_vars()
    if storage_options:
        wtfpx__jru = storage_options.get('anon', False)
    fs = S3FileSystem(region=region, endpoint_override=uofq__fqs, anonymous
        =wtfpx__jru, proxy_options=hpy__uibl)
    return SubTreeFileSystem(bucket_name, fs)


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.fs import HadoopFileSystem as HdFS
    pceh__jix = urlparse(path)
    if pceh__jix.scheme in ('abfs', 'abfss'):
        bnkym__xqqp = path
        if pceh__jix.port is None:
            gbz__nmy = 0
        else:
            gbz__nmy = pceh__jix.port
        odkus__mfmd = None
    else:
        bnkym__xqqp = pceh__jix.hostname
        gbz__nmy = pceh__jix.port
        odkus__mfmd = pceh__jix.username
    try:
        fs = HdFS(host=bnkym__xqqp, port=gbz__nmy, user=odkus__mfmd)
    except Exception as fyxf__unt:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            fyxf__unt))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        knvdi__gjugh = fs.isdir(path)
    except gcsfs.utils.HttpError as fyxf__unt:
        raise BodoError(
            f'{fyxf__unt}. Make sure your google cloud credentials are set!')
    return knvdi__gjugh


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [gusd__eeyb.split('/')[-1] for gusd__eeyb in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        pceh__jix = urlparse(path)
        zvvw__ewmj = (pceh__jix.netloc + pceh__jix.path).rstrip('/')
        gpfx__kiocf = fs.get_file_info(zvvw__ewmj)
        if gpfx__kiocf.type in (pa_fs.FileType.NotFound, pa_fs.FileType.Unknown
            ):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if (not gpfx__kiocf.size and gpfx__kiocf.type == pa_fs.FileType.
            Directory):
            return True
        return False
    except (FileNotFoundError, OSError) as fyxf__unt:
        raise
    except BodoError as fxgue__nhmxm:
        raise
    except Exception as fyxf__unt:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(fyxf__unt).__name__}: {str(fyxf__unt)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    wmj__hrx = None
    try:
        if s3_is_directory(fs, path):
            pceh__jix = urlparse(path)
            zvvw__ewmj = (pceh__jix.netloc + pceh__jix.path).rstrip('/')
            pwqpl__xpwc = pa_fs.FileSelector(zvvw__ewmj, recursive=False)
            jroj__jivtk = fs.get_file_info(pwqpl__xpwc)
            if jroj__jivtk and jroj__jivtk[0].path in [zvvw__ewmj,
                f'{zvvw__ewmj}/'] and int(jroj__jivtk[0].size or 0) == 0:
                jroj__jivtk = jroj__jivtk[1:]
            wmj__hrx = [lqtsc__abl.base_name for lqtsc__abl in jroj__jivtk]
    except BodoError as fxgue__nhmxm:
        raise
    except Exception as fyxf__unt:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(fyxf__unt).__name__}: {str(fyxf__unt)}
{bodo_error_msg}"""
            )
    return wmj__hrx


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    pceh__jix = urlparse(path)
    txq__gru = pceh__jix.path
    try:
        txqz__ueld = HadoopFileSystem.from_uri(path)
    except Exception as fyxf__unt:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            fyxf__unt))
    txei__zzfjx = txqz__ueld.get_file_info([txq__gru])
    if txei__zzfjx[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not txei__zzfjx[0].size and txei__zzfjx[0].type == FileType.Directory:
        return txqz__ueld, True
    return txqz__ueld, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    wmj__hrx = None
    txqz__ueld, knvdi__gjugh = hdfs_is_directory(path)
    if knvdi__gjugh:
        pceh__jix = urlparse(path)
        txq__gru = pceh__jix.path
        pwqpl__xpwc = FileSelector(txq__gru, recursive=True)
        try:
            jroj__jivtk = txqz__ueld.get_file_info(pwqpl__xpwc)
        except Exception as fyxf__unt:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(txq__gru, fyxf__unt))
        wmj__hrx = [lqtsc__abl.base_name for lqtsc__abl in jroj__jivtk]
    return txqz__ueld, wmj__hrx


def abfs_is_directory(path):
    txqz__ueld = get_hdfs_fs(path)
    try:
        txei__zzfjx = txqz__ueld.info(path)
    except OSError as fxgue__nhmxm:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if txei__zzfjx['size'] == 0 and txei__zzfjx['kind'].lower() == 'directory':
        return txqz__ueld, True
    return txqz__ueld, False


def abfs_list_dir_fnames(path):
    wmj__hrx = None
    txqz__ueld, knvdi__gjugh = abfs_is_directory(path)
    if knvdi__gjugh:
        pceh__jix = urlparse(path)
        txq__gru = pceh__jix.path
        try:
            btzkf__ewzrg = txqz__ueld.ls(txq__gru)
        except Exception as fyxf__unt:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(txq__gru, fyxf__unt))
        wmj__hrx = [fname[fname.rindex('/') + 1:] for fname in btzkf__ewzrg]
    return txqz__ueld, wmj__hrx


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype, storage_options=None):
    from urllib.parse import urlparse
    xofaf__lsjb = urlparse(path)
    fname = path
    fs = None
    dix__uensx = 'read_json' if ftype == 'json' else 'read_csv'
    xstf__vbc = (
        f'pd.{dix__uensx}(): there is no {ftype} file in directory: {fname}')
    necwt__clg = directory_of_files_common_filter
    if xofaf__lsjb.scheme == 's3':
        bceq__yly = True
        fs = get_s3_fs_from_path(path, storage_options=storage_options)
        blpix__pxsbm = s3_list_dir_fnames(fs, path)
        zvvw__ewmj = (xofaf__lsjb.netloc + xofaf__lsjb.path).rstrip('/')
        fname = zvvw__ewmj
        if blpix__pxsbm:
            blpix__pxsbm = [(zvvw__ewmj + '/' + gusd__eeyb) for gusd__eeyb in
                sorted(filter(necwt__clg, blpix__pxsbm))]
            glp__nmik = [gusd__eeyb for gusd__eeyb in blpix__pxsbm if int(
                fs.get_file_info(gusd__eeyb).size or 0) > 0]
            if len(glp__nmik) == 0:
                raise BodoError(xstf__vbc)
            fname = glp__nmik[0]
        mqupd__mbx = int(fs.get_file_info(fname).size or 0)
        fs = ArrowFSWrapper(fs)
        zrx__fhm = fs._open(fname)
    elif xofaf__lsjb.scheme == 'hdfs':
        bceq__yly = True
        fs, blpix__pxsbm = hdfs_list_dir_fnames(path)
        mqupd__mbx = fs.get_file_info([xofaf__lsjb.path])[0].size
        if blpix__pxsbm:
            path = path.rstrip('/')
            blpix__pxsbm = [(path + '/' + gusd__eeyb) for gusd__eeyb in
                sorted(filter(necwt__clg, blpix__pxsbm))]
            glp__nmik = [gusd__eeyb for gusd__eeyb in blpix__pxsbm if fs.
                get_file_info([urlparse(gusd__eeyb).path])[0].size > 0]
            if len(glp__nmik) == 0:
                raise BodoError(xstf__vbc)
            fname = glp__nmik[0]
            fname = urlparse(fname).path
            mqupd__mbx = fs.get_file_info([fname])[0].size
        zrx__fhm = fs.open_input_file(fname)
    elif xofaf__lsjb.scheme in ('abfs', 'abfss'):
        bceq__yly = True
        fs, blpix__pxsbm = abfs_list_dir_fnames(path)
        mqupd__mbx = fs.info(fname)['size']
        if blpix__pxsbm:
            path = path.rstrip('/')
            blpix__pxsbm = [(path + '/' + gusd__eeyb) for gusd__eeyb in
                sorted(filter(necwt__clg, blpix__pxsbm))]
            glp__nmik = [gusd__eeyb for gusd__eeyb in blpix__pxsbm if fs.
                info(gusd__eeyb)['size'] > 0]
            if len(glp__nmik) == 0:
                raise BodoError(xstf__vbc)
            fname = glp__nmik[0]
            mqupd__mbx = fs.info(fname)['size']
            fname = urlparse(fname).path
        zrx__fhm = fs.open(fname, 'rb')
    else:
        if xofaf__lsjb.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {xofaf__lsjb.scheme}. Please refer to https://docs.bodo.ai/latest/file_io/.'
                )
        bceq__yly = False
        if os.path.isdir(path):
            btzkf__ewzrg = filter(necwt__clg, glob.glob(os.path.join(os.
                path.abspath(path), '*')))
            glp__nmik = [gusd__eeyb for gusd__eeyb in sorted(btzkf__ewzrg) if
                os.path.getsize(gusd__eeyb) > 0]
            if len(glp__nmik) == 0:
                raise BodoError(xstf__vbc)
            fname = glp__nmik[0]
        mqupd__mbx = os.path.getsize(fname)
        zrx__fhm = fname
    return bceq__yly, zrx__fhm, mqupd__mbx, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    pfmk__avx = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            gfawn__rig, dyw__eglpg = pa_fs.S3FileSystem.from_uri(s3_filepath)
            bucket_loc = gfawn__rig.region
        except Exception as fyxf__unt:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{fyxf__unt}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = pfmk__avx.bcast(bucket_loc)
    return bucket_loc


@numba.njit()
def get_s3_bucket_region_njit(s3_filepath, parallel):
    with numba.objmode(bucket_loc='unicode_type'):
        bucket_loc = ''
        if isinstance(s3_filepath, list):
            s3_filepath = s3_filepath[0]
        if s3_filepath.startswith('s3://'):
            bucket_loc = get_s3_bucket_region(s3_filepath, parallel)
    return bucket_loc


def csv_write(path_or_buf, D, filename_prefix, is_parallel=False):
    return None


@overload(csv_write, no_unliteral=True)
def csv_write_overload(path_or_buf, D, filename_prefix, is_parallel=False):

    def impl(path_or_buf, D, filename_prefix, is_parallel=False):
        fcdp__yjru = get_s3_bucket_region_njit(path_or_buf, parallel=
            is_parallel)
        gew__diatv, geh__qxfv = unicode_to_utf8_and_len(D)
        tyz__qyn = 0
        if is_parallel:
            tyz__qyn = bodo.libs.distributed_api.dist_exscan(geh__qxfv, np.
                int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), gew__diatv, tyz__qyn,
            geh__qxfv, is_parallel, unicode_to_utf8(fcdp__yjru),
            unicode_to_utf8(filename_prefix))
        bodo.utils.utils.check_and_propagate_cpp_exception()
    return impl


class StorageOptionsDictType(types.Opaque):

    def __init__(self):
        super(StorageOptionsDictType, self).__init__(name=
            'StorageOptionsDictType')


storage_options_dict_type = StorageOptionsDictType()
types.storage_options_dict_type = storage_options_dict_type
register_model(StorageOptionsDictType)(models.OpaqueModel)


@unbox(StorageOptionsDictType)
def unbox_storage_options_dict_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


def get_storage_options_pyobject(storage_options):
    pass


@overload(get_storage_options_pyobject, no_unliteral=True)
def overload_get_storage_options_pyobject(storage_options):
    pym__vnq = get_overload_constant_dict(storage_options)
    paow__ypkyl = 'def impl(storage_options):\n'
    paow__ypkyl += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    paow__ypkyl += f'    storage_options_py = {str(pym__vnq)}\n'
    paow__ypkyl += '  return storage_options_py\n'
    vpvv__spnw = {}
    exec(paow__ypkyl, globals(), vpvv__spnw)
    return vpvv__spnw['impl']
