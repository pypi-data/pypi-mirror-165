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
    lbezx__zctv = context.get_python_api(builder)
    return lbezx__zctv.unserialize(lbezx__zctv.serialize_object(pyval))


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
    fviot__eije = 'ns', 'us', 'ms', 's'
    if pa_ts_typ.unit not in fviot__eije:
        return types.Array(bodo.datetime64ns, 1, 'C'), False
    elif pa_ts_typ.tz is not None:
        sgdw__pxkhw = pa_ts_typ.to_pandas_dtype().tz
        oysrj__qyl = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(
            sgdw__pxkhw)
        return bodo.DatetimeArrayType(oysrj__qyl), True
    else:
        return types.Array(bodo.datetime64ns, 1, 'C'), True


def _get_numba_typ_from_pa_typ(pa_typ: pa.Field, is_index,
    nullable_from_metadata, category_info, str_as_dict=False):
    if isinstance(pa_typ.type, pa.ListType):
        xtxb__vpfo, yfsdv__lnfmi = _get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info)
        return ArrayItemArrayType(xtxb__vpfo), yfsdv__lnfmi
    if isinstance(pa_typ.type, pa.StructType):
        gykt__ptmq = []
        krz__zunnm = []
        yfsdv__lnfmi = True
        for zgqqa__viyh in pa_typ.flatten():
            krz__zunnm.append(zgqqa__viyh.name.split('.')[-1])
            pysd__zzfc, ktwh__seqs = _get_numba_typ_from_pa_typ(zgqqa__viyh,
                is_index, nullable_from_metadata, category_info)
            gykt__ptmq.append(pysd__zzfc)
            yfsdv__lnfmi = yfsdv__lnfmi and ktwh__seqs
        return StructArrayType(tuple(gykt__ptmq), tuple(krz__zunnm)
            ), yfsdv__lnfmi
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
        gnyoj__ldqh = _pyarrow_numba_type_map[pa_typ.type.index_type]
        jdowe__jts = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=gnyoj__ldqh)
        return CategoricalArrayType(jdowe__jts), True
    if isinstance(pa_typ.type, pa.lib.TimestampType):
        return get_arrow_timestamp_type(pa_typ.type)
    elif pa_typ.type in _pyarrow_numba_type_map:
        hgyaq__efa = _pyarrow_numba_type_map[pa_typ.type]
        yfsdv__lnfmi = True
    else:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    if hgyaq__efa == datetime_date_type:
        return datetime_date_array_type, yfsdv__lnfmi
    if isinstance(hgyaq__efa, TimeType):
        return TimeArrayType(hgyaq__efa.precision), yfsdv__lnfmi
    if hgyaq__efa == bytes_type:
        return binary_array_type, yfsdv__lnfmi
    xtxb__vpfo = (string_array_type if hgyaq__efa == string_type else types
        .Array(hgyaq__efa, 1, 'C'))
    if hgyaq__efa == types.bool_:
        xtxb__vpfo = boolean_array
    gsjr__nyov = (use_nullable_int_arr if nullable_from_metadata is None else
        nullable_from_metadata)
    if gsjr__nyov and not is_index and isinstance(hgyaq__efa, types.Integer
        ) and pa_typ.nullable:
        xtxb__vpfo = IntegerArrayType(hgyaq__efa)
    return xtxb__vpfo, yfsdv__lnfmi


def update_env_vars(env_vars):
    olfxb__elwl = {}
    for urz__azo, ujagi__lha in env_vars.items():
        if urz__azo in os.environ:
            olfxb__elwl[urz__azo] = os.environ[urz__azo]
        else:
            olfxb__elwl[urz__azo] = '__none__'
        if ujagi__lha == '__none__':
            del os.environ[urz__azo]
        else:
            os.environ[urz__azo] = ujagi__lha
    return olfxb__elwl


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
        except BaseException as zwej__gguop:
            self.exc = zwej__gguop

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
    oxkn__vxcym = tracing.Event('join_all_threads', is_parallel=True)
    voo__hcshx = MPI.COMM_WORLD
    gwnb__vnf = None
    try:
        for hgj__kuhg in thread_list:
            if isinstance(hgj__kuhg, threading.Thread):
                hgj__kuhg.join()
    except Exception as zwej__gguop:
        gwnb__vnf = zwej__gguop
    bclx__kygxi = int(gwnb__vnf is not None)
    ztd__yqo, cgb__sxug = voo__hcshx.allreduce((bclx__kygxi, voo__hcshx.
        Get_rank()), op=MPI.MAXLOC)
    if ztd__yqo:
        if voo__hcshx.Get_rank() == cgb__sxug:
            gzso__yxh = gwnb__vnf
        else:
            gzso__yxh = None
        gzso__yxh = voo__hcshx.bcast(gzso__yxh, root=cgb__sxug)
        if bclx__kygxi:
            raise gwnb__vnf
        else:
            raise gzso__yxh
    oxkn__vxcym.finalize()
