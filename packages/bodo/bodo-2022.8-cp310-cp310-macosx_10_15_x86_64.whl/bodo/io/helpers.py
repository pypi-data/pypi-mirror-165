"""
File that contains some IO related helpers.
"""
import os
import threading
import uuid
import numba
import pyarrow as pa
from mpi4py import MPI
from numba.core import types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, models, register_model, typeof_impl, unbox
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type, datetime_date_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.time_ext import TimeArrayType, TimeType
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils import tracing
from bodo.utils.typing import BodoError


class PyArrowTableSchemaType(types.Opaque):

    def __init__(self):
        super(PyArrowTableSchemaType, self).__init__(name=
            'PyArrowTableSchemaType')


pyarrow_table_schema_type = PyArrowTableSchemaType()
types.pyarrow_table_schema_type = pyarrow_table_schema_type
register_model(PyArrowTableSchemaType)(models.OpaqueModel)


@unbox(PyArrowTableSchemaType)
def unbox_pyarrow_table_schema_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


@box(PyArrowTableSchemaType)
def box_pyarrow_table_schema_type(typ, val, c):
    c.pyapi.incref(val)
    return val


@typeof_impl.register(pa.lib.Schema)
def typeof_pyarrow_table_schema(val, c):
    return pyarrow_table_schema_type


@lower_constant(PyArrowTableSchemaType)
def lower_pyarrow_table_schema(context, builder, ty, pyval):
    ttzub__glpa = context.get_python_api(builder)
    return ttzub__glpa.unserialize(ttzub__glpa.serialize_object(pyval))


def is_nullable(typ):
    return bodo.utils.utils.is_array_typ(typ, False) and (not isinstance(
        typ, types.Array) and not isinstance(typ, bodo.DatetimeArrayType))


def pa_schema_unify_reduction(schema_a, schema_b, unused):
    return pa.unify_schemas([schema_a, schema_b])


pa_schema_unify_mpi_op = MPI.Op.Create(pa_schema_unify_reduction, commute=True)
use_nullable_int_arr = True
_pyarrow_numba_type_map = {pa.bool_(): types.bool_, pa.int8(): types.int8,
    pa.int16(): types.int16, pa.int32(): types.int32, pa.int64(): types.
    int64, pa.uint8(): types.uint8, pa.uint16(): types.uint16, pa.uint32():
    types.uint32, pa.uint64(): types.uint64, pa.float32(): types.float32,
    pa.float64(): types.float64, pa.string(): string_type, pa.large_string(
    ): string_type, pa.binary(): bytes_type, pa.date32():
    datetime_date_type, pa.date64(): types.NPDatetime('ns'), pa.time32('s'):
    TimeType(0), pa.time32('ms'): TimeType(3), pa.time64('us'): TimeType(6),
    pa.time64('ns'): TimeType(9), pa.null(): string_type}


def get_arrow_timestamp_type(pa_ts_typ):
    fbr__emjch = 'ns', 'us', 'ms', 's'
    if pa_ts_typ.unit not in fbr__emjch:
        return types.Array(bodo.datetime64ns, 1, 'C'), False
    elif pa_ts_typ.tz is not None:
        xryyu__yhko = pa_ts_typ.to_pandas_dtype().tz
        fscpv__wne = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(
            xryyu__yhko)
        return bodo.DatetimeArrayType(fscpv__wne), True
    else:
        return types.Array(bodo.datetime64ns, 1, 'C'), True


def _get_numba_typ_from_pa_typ(pa_typ: pa.Field, is_index,
    nullable_from_metadata, category_info, str_as_dict=False):
    if isinstance(pa_typ.type, pa.ListType):
        ald__wfgf, ojg__dhfu = _get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info)
        return ArrayItemArrayType(ald__wfgf), ojg__dhfu
    if isinstance(pa_typ.type, pa.StructType):
        rwn__bkul = []
        snob__gum = []
        ojg__dhfu = True
        for hcee__hfd in pa_typ.flatten():
            snob__gum.append(hcee__hfd.name.split('.')[-1])
            edes__fzrj, espft__sig = _get_numba_typ_from_pa_typ(hcee__hfd,
                is_index, nullable_from_metadata, category_info)
            rwn__bkul.append(edes__fzrj)
            ojg__dhfu = ojg__dhfu and espft__sig
        return StructArrayType(tuple(rwn__bkul), tuple(snob__gum)), ojg__dhfu
    if isinstance(pa_typ.type, pa.Decimal128Type):
        return DecimalArrayType(pa_typ.type.precision, pa_typ.type.scale), True
    if str_as_dict:
        if pa_typ.type != pa.string():
            raise BodoError(
                f'Read as dictionary used for non-string column {pa_typ}')
        return dict_str_arr_type, True
    if isinstance(pa_typ.type, pa.DictionaryType):
        if pa_typ.type.value_type != pa.string():
            raise BodoError(
                f'Parquet Categorical data type should be string, not {pa_typ.type.value_type}'
                )
        zvpv__pek = _pyarrow_numba_type_map[pa_typ.type.index_type]
        anbk__rejjt = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=zvpv__pek)
        return CategoricalArrayType(anbk__rejjt), True
    if isinstance(pa_typ.type, pa.lib.TimestampType):
        return get_arrow_timestamp_type(pa_typ.type)
    elif pa_typ.type in _pyarrow_numba_type_map:
        mbbwu__pfnxa = _pyarrow_numba_type_map[pa_typ.type]
        ojg__dhfu = True
    else:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    if mbbwu__pfnxa == datetime_date_type:
        return datetime_date_array_type, ojg__dhfu
    if isinstance(mbbwu__pfnxa, TimeType):
        return TimeArrayType(mbbwu__pfnxa.precision), ojg__dhfu
    if mbbwu__pfnxa == bytes_type:
        return binary_array_type, ojg__dhfu
    ald__wfgf = (string_array_type if mbbwu__pfnxa == string_type else
        types.Array(mbbwu__pfnxa, 1, 'C'))
    if mbbwu__pfnxa == types.bool_:
        ald__wfgf = boolean_array
    huh__twub = (use_nullable_int_arr if nullable_from_metadata is None else
        nullable_from_metadata)
    if huh__twub and not is_index and isinstance(mbbwu__pfnxa, types.Integer
        ) and pa_typ.nullable:
        ald__wfgf = IntegerArrayType(mbbwu__pfnxa)
    return ald__wfgf, ojg__dhfu


def update_env_vars(env_vars):
    leg__nwtjs = {}
    for bfyqa__rfzdl, uzq__nkw in env_vars.items():
        if bfyqa__rfzdl in os.environ:
            leg__nwtjs[bfyqa__rfzdl] = os.environ[bfyqa__rfzdl]
        else:
            leg__nwtjs[bfyqa__rfzdl] = '__none__'
        if uzq__nkw == '__none__':
            del os.environ[bfyqa__rfzdl]
        else:
            os.environ[bfyqa__rfzdl] = uzq__nkw
    return leg__nwtjs


@numba.njit
def uuid4_helper():
    with numba.objmode(out='unicode_type'):
        out = str(uuid.uuid4())
    return out


class ExceptionPropagatingThread(threading.Thread):

    def run(self):
        self.exc = None
        try:
            self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as mbh__zbhk:
            self.exc = mbh__zbhk

    def join(self, timeout=None):
        super().join(timeout)
        if self.exc:
            raise self.exc
        return self.ret


class ExceptionPropagatingThreadType(types.Opaque):

    def __init__(self):
        super(ExceptionPropagatingThreadType, self).__init__(name=
            'ExceptionPropagatingThreadType')


exception_propagating_thread_type = ExceptionPropagatingThreadType()
types.exception_propagating_thread_type = exception_propagating_thread_type
register_model(ExceptionPropagatingThreadType)(models.OpaqueModel)


@unbox(ExceptionPropagatingThreadType)
def unbox_exception_propagating_thread_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


@box(ExceptionPropagatingThreadType)
def box_exception_propagating_thread_type(typ, val, c):
    c.pyapi.incref(val)
    return val


@typeof_impl.register(ExceptionPropagatingThread)
def typeof_exception_propagating_thread(val, c):
    return exception_propagating_thread_type


def join_all_threads(thread_list):
    pnvae__jgj = tracing.Event('join_all_threads', is_parallel=True)
    efsui__ckv = MPI.COMM_WORLD
    qht__fvc = None
    try:
        for prhqf__ukofb in thread_list:
            if isinstance(prhqf__ukofb, threading.Thread):
                prhqf__ukofb.join()
    except Exception as mbh__zbhk:
        qht__fvc = mbh__zbhk
    iijk__soei = int(qht__fvc is not None)
    avkjy__afh, mlivf__eckek = efsui__ckv.allreduce((iijk__soei, efsui__ckv
        .Get_rank()), op=MPI.MAXLOC)
    if avkjy__afh:
        if efsui__ckv.Get_rank() == mlivf__eckek:
            idy__tutjh = qht__fvc
        else:
            idy__tutjh = None
        idy__tutjh = efsui__ckv.bcast(idy__tutjh, root=mlivf__eckek)
        if iijk__soei:
            raise qht__fvc
        else:
            raise idy__tutjh
    pnvae__jgj.finalize()
