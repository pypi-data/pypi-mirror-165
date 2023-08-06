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
            haaz__phlel = self.fs.open_input_file(path)
        except:
            haaz__phlel = self.fs.open_input_stream(path)
    elif mode == 'wb':
        haaz__phlel = self.fs.open_output_stream(path)
    else:
        raise ValueError(f'unsupported mode for Arrow filesystem: {mode!r}')
    return ArrowFile(self, haaz__phlel, path, mode, block_size, **kwargs)


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
    mld__khqa = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    nsdkp__rsqxe = False
    fmbg__dspa = get_proxy_uri_from_env_vars()
    if storage_options:
        nsdkp__rsqxe = storage_options.get('anon', False)
    return S3FileSystem(anonymous=nsdkp__rsqxe, region=region,
        endpoint_override=mld__khqa, proxy_options=fmbg__dspa)


def get_s3_subtree_fs(bucket_name, region=None, storage_options=None):
    from pyarrow._fs import SubTreeFileSystem
    from pyarrow._s3fs import S3FileSystem
    mld__khqa = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    nsdkp__rsqxe = False
    fmbg__dspa = get_proxy_uri_from_env_vars()
    if storage_options:
        nsdkp__rsqxe = storage_options.get('anon', False)
    fs = S3FileSystem(region=region, endpoint_override=mld__khqa, anonymous
        =nsdkp__rsqxe, proxy_options=fmbg__dspa)
    return SubTreeFileSystem(bucket_name, fs)


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.fs import HadoopFileSystem as HdFS
    hrmbj__gyf = urlparse(path)
    if hrmbj__gyf.scheme in ('abfs', 'abfss'):
        lpv__gokp = path
        if hrmbj__gyf.port is None:
            fkb__sbqw = 0
        else:
            fkb__sbqw = hrmbj__gyf.port
        anc__ajrnw = None
    else:
        lpv__gokp = hrmbj__gyf.hostname
        fkb__sbqw = hrmbj__gyf.port
        anc__ajrnw = hrmbj__gyf.username
    try:
        fs = HdFS(host=lpv__gokp, port=fkb__sbqw, user=anc__ajrnw)
    except Exception as vkoh__zmsm:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            vkoh__zmsm))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        yqbn__sgo = fs.isdir(path)
    except gcsfs.utils.HttpError as vkoh__zmsm:
        raise BodoError(
            f'{vkoh__zmsm}. Make sure your google cloud credentials are set!')
    return yqbn__sgo


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [lpg__odqx.split('/')[-1] for lpg__odqx in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        hrmbj__gyf = urlparse(path)
        rxjxh__zwcdg = (hrmbj__gyf.netloc + hrmbj__gyf.path).rstrip('/')
        vhp__wscog = fs.get_file_info(rxjxh__zwcdg)
        if vhp__wscog.type in (pa_fs.FileType.NotFound, pa_fs.FileType.Unknown
            ):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if not vhp__wscog.size and vhp__wscog.type == pa_fs.FileType.Directory:
            return True
        return False
    except (FileNotFoundError, OSError) as vkoh__zmsm:
        raise
    except BodoError as ygv__hjllj:
        raise
    except Exception as vkoh__zmsm:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(vkoh__zmsm).__name__}: {str(vkoh__zmsm)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    kwbzg__punlp = None
    try:
        if s3_is_directory(fs, path):
            hrmbj__gyf = urlparse(path)
            rxjxh__zwcdg = (hrmbj__gyf.netloc + hrmbj__gyf.path).rstrip('/')
            xpp__igtkr = pa_fs.FileSelector(rxjxh__zwcdg, recursive=False)
            fpr__jsp = fs.get_file_info(xpp__igtkr)
            if fpr__jsp and fpr__jsp[0].path in [rxjxh__zwcdg,
                f'{rxjxh__zwcdg}/'] and int(fpr__jsp[0].size or 0) == 0:
                fpr__jsp = fpr__jsp[1:]
            kwbzg__punlp = [fwhrc__unx.base_name for fwhrc__unx in fpr__jsp]
    except BodoError as ygv__hjllj:
        raise
    except Exception as vkoh__zmsm:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(vkoh__zmsm).__name__}: {str(vkoh__zmsm)}
{bodo_error_msg}"""
            )
    return kwbzg__punlp


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    hrmbj__gyf = urlparse(path)
    zpij__aow = hrmbj__gyf.path
    try:
        ihn__ifmca = HadoopFileSystem.from_uri(path)
    except Exception as vkoh__zmsm:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            vkoh__zmsm))
    myn__jonoz = ihn__ifmca.get_file_info([zpij__aow])
    if myn__jonoz[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not myn__jonoz[0].size and myn__jonoz[0].type == FileType.Directory:
        return ihn__ifmca, True
    return ihn__ifmca, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    kwbzg__punlp = None
    ihn__ifmca, yqbn__sgo = hdfs_is_directory(path)
    if yqbn__sgo:
        hrmbj__gyf = urlparse(path)
        zpij__aow = hrmbj__gyf.path
        xpp__igtkr = FileSelector(zpij__aow, recursive=True)
        try:
            fpr__jsp = ihn__ifmca.get_file_info(xpp__igtkr)
        except Exception as vkoh__zmsm:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(zpij__aow, vkoh__zmsm))
        kwbzg__punlp = [fwhrc__unx.base_name for fwhrc__unx in fpr__jsp]
    return ihn__ifmca, kwbzg__punlp


def abfs_is_directory(path):
    ihn__ifmca = get_hdfs_fs(path)
    try:
        myn__jonoz = ihn__ifmca.info(path)
    except OSError as ygv__hjllj:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if myn__jonoz['size'] == 0 and myn__jonoz['kind'].lower() == 'directory':
        return ihn__ifmca, True
    return ihn__ifmca, False


def abfs_list_dir_fnames(path):
    kwbzg__punlp = None
    ihn__ifmca, yqbn__sgo = abfs_is_directory(path)
    if yqbn__sgo:
        hrmbj__gyf = urlparse(path)
        zpij__aow = hrmbj__gyf.path
        try:
            rmh__axhm = ihn__ifmca.ls(zpij__aow)
        except Exception as vkoh__zmsm:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(zpij__aow, vkoh__zmsm))
        kwbzg__punlp = [fname[fname.rindex('/') + 1:] for fname in rmh__axhm]
    return ihn__ifmca, kwbzg__punlp


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype, storage_options=None):
    from urllib.parse import urlparse
    ubz__ebo = urlparse(path)
    fname = path
    fs = None
    apx__jwggl = 'read_json' if ftype == 'json' else 'read_csv'
    zui__dcek = (
        f'pd.{apx__jwggl}(): there is no {ftype} file in directory: {fname}')
    kfdfy__djyem = directory_of_files_common_filter
    if ubz__ebo.scheme == 's3':
        cfmrt__couzv = True
        fs = get_s3_fs_from_path(path, storage_options=storage_options)
        otc__rlfa = s3_list_dir_fnames(fs, path)
        rxjxh__zwcdg = (ubz__ebo.netloc + ubz__ebo.path).rstrip('/')
        fname = rxjxh__zwcdg
        if otc__rlfa:
            otc__rlfa = [(rxjxh__zwcdg + '/' + lpg__odqx) for lpg__odqx in
                sorted(filter(kfdfy__djyem, otc__rlfa))]
            gvqbz__lstz = [lpg__odqx for lpg__odqx in otc__rlfa if int(fs.
                get_file_info(lpg__odqx).size or 0) > 0]
            if len(gvqbz__lstz) == 0:
                raise BodoError(zui__dcek)
            fname = gvqbz__lstz[0]
        oyd__zzh = int(fs.get_file_info(fname).size or 0)
        fs = ArrowFSWrapper(fs)
        ssye__jly = fs._open(fname)
    elif ubz__ebo.scheme == 'hdfs':
        cfmrt__couzv = True
        fs, otc__rlfa = hdfs_list_dir_fnames(path)
        oyd__zzh = fs.get_file_info([ubz__ebo.path])[0].size
        if otc__rlfa:
            path = path.rstrip('/')
            otc__rlfa = [(path + '/' + lpg__odqx) for lpg__odqx in sorted(
                filter(kfdfy__djyem, otc__rlfa))]
            gvqbz__lstz = [lpg__odqx for lpg__odqx in otc__rlfa if fs.
                get_file_info([urlparse(lpg__odqx).path])[0].size > 0]
            if len(gvqbz__lstz) == 0:
                raise BodoError(zui__dcek)
            fname = gvqbz__lstz[0]
            fname = urlparse(fname).path
            oyd__zzh = fs.get_file_info([fname])[0].size
        ssye__jly = fs.open_input_file(fname)
    elif ubz__ebo.scheme in ('abfs', 'abfss'):
        cfmrt__couzv = True
        fs, otc__rlfa = abfs_list_dir_fnames(path)
        oyd__zzh = fs.info(fname)['size']
        if otc__rlfa:
            path = path.rstrip('/')
            otc__rlfa = [(path + '/' + lpg__odqx) for lpg__odqx in sorted(
                filter(kfdfy__djyem, otc__rlfa))]
            gvqbz__lstz = [lpg__odqx for lpg__odqx in otc__rlfa if fs.info(
                lpg__odqx)['size'] > 0]
            if len(gvqbz__lstz) == 0:
                raise BodoError(zui__dcek)
            fname = gvqbz__lstz[0]
            oyd__zzh = fs.info(fname)['size']
            fname = urlparse(fname).path
        ssye__jly = fs.open(fname, 'rb')
    else:
        if ubz__ebo.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {ubz__ebo.scheme}. Please refer to https://docs.bodo.ai/latest/file_io/.'
                )
        cfmrt__couzv = False
        if os.path.isdir(path):
            rmh__axhm = filter(kfdfy__djyem, glob.glob(os.path.join(os.path
                .abspath(path), '*')))
            gvqbz__lstz = [lpg__odqx for lpg__odqx in sorted(rmh__axhm) if 
                os.path.getsize(lpg__odqx) > 0]
            if len(gvqbz__lstz) == 0:
                raise BodoError(zui__dcek)
            fname = gvqbz__lstz[0]
        oyd__zzh = os.path.getsize(fname)
        ssye__jly = fname
    return cfmrt__couzv, ssye__jly, oyd__zzh, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    mogl__bzr = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            aemhl__quwhr, qgbp__zqazb = pa_fs.S3FileSystem.from_uri(s3_filepath
                )
            bucket_loc = aemhl__quwhr.region
        except Exception as vkoh__zmsm:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{vkoh__zmsm}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = mogl__bzr.bcast(bucket_loc)
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
        cdiy__chh = get_s3_bucket_region_njit(path_or_buf, parallel=is_parallel
            )
        lfso__smf, riin__tfyxs = unicode_to_utf8_and_len(D)
        rinxh__syo = 0
        if is_parallel:
            rinxh__syo = bodo.libs.distributed_api.dist_exscan(riin__tfyxs,
                np.int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), lfso__smf, rinxh__syo,
            riin__tfyxs, is_parallel, unicode_to_utf8(cdiy__chh),
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
    gcevd__eissg = get_overload_constant_dict(storage_options)
    ipj__swr = 'def impl(storage_options):\n'
    ipj__swr += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    ipj__swr += f'    storage_options_py = {str(gcevd__eissg)}\n'
    ipj__swr += '  return storage_options_py\n'
    oavj__byes = {}
    exec(ipj__swr, globals(), oavj__byes)
    return oavj__byes['impl']
