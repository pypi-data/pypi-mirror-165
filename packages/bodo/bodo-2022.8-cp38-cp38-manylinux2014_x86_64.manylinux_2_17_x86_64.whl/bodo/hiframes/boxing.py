"""
Boxing and unboxing support for DataFrame, Series, etc.
"""
import datetime
import decimal
import warnings
from enum import Enum
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.ir_utils import GuardException, guard
from numba.core.typing import signature
from numba.cpython.listobj import ListInstance
from numba.extending import NativeValue, box, intrinsic, typeof_impl, unbox
from numba.np import numpy_support
from numba.np.arrayobj import _getitem_array_single_int
from numba.typed.typeddict import Dict
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import PDCategoricalDtype
from bodo.hiframes.pd_dataframe_ext import DataFramePayloadType, DataFrameType, check_runtime_cols_unsupported, construct_dataframe
from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, DatetimeIndexType, NumericIndexType, PeriodIndexType, RangeIndexType, StringIndexType, TimedeltaIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.hiframes.time_ext import TimeArrayType
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType, typeof_pd_int_dtype
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType, PandasDatetimeTZDtype
from bodo.libs.str_arr_ext import string_array_type, string_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType, StructType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.typing import BodoError, BodoWarning, dtype_to_array_type, get_overload_const_bool, get_overload_const_int, get_overload_const_str, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_str, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array
ll.add_symbol('is_np_array', hstr_ext.is_np_array)
ll.add_symbol('array_size', hstr_ext.array_size)
ll.add_symbol('array_getptr1', hstr_ext.array_getptr1)
TABLE_FORMAT_THRESHOLD = 20
_use_dict_str_type = False


def _set_bodo_meta_in_pandas():
    if '_bodo_meta' not in pd.Series._metadata:
        pd.Series._metadata.append('_bodo_meta')
    if '_bodo_meta' not in pd.DataFrame._metadata:
        pd.DataFrame._metadata.append('_bodo_meta')


_set_bodo_meta_in_pandas()


@typeof_impl.register(pd.DataFrame)
def typeof_pd_dataframe(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    qfrx__khq = tuple(val.columns.to_list())
    ahkqc__yvuc = get_hiframes_dtypes(val)
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and len(val._bodo_meta['type_metadata'
        ][1]) == len(val.columns) and val._bodo_meta['type_metadata'][0] is not
        None):
        vvc__hin = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        vvc__hin = numba.typeof(val.index)
    rfkkw__kwt = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    osoya__isg = len(ahkqc__yvuc) >= TABLE_FORMAT_THRESHOLD
    return DataFrameType(ahkqc__yvuc, vvc__hin, qfrx__khq, rfkkw__kwt,
        is_table_format=osoya__isg)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    rfkkw__kwt = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and val._bodo_meta['type_metadata'][0]
         is not None):
        dil__keqz = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        dil__keqz = numba.typeof(val.index)
    dtype = _infer_series_dtype(val)
    xgzgb__cbkqi = dtype_to_array_type(dtype)
    if _use_dict_str_type and xgzgb__cbkqi == string_array_type:
        xgzgb__cbkqi = bodo.dict_str_arr_type
    return SeriesType(dtype, data=xgzgb__cbkqi, index=dil__keqz, name_typ=
        numba.typeof(val.name), dist=rfkkw__kwt)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    check_runtime_cols_unsupported(typ, 'Unboxing')
    kyc__dubt = c.pyapi.object_getattr_string(val, 'index')
    zpyp__iouv = c.pyapi.to_native_value(typ.index, kyc__dubt).value
    c.pyapi.decref(kyc__dubt)
    if typ.is_table_format:
        ork__xsqs = cgutils.create_struct_proxy(typ.table_type)(c.context,
            c.builder)
        ork__xsqs.parent = val
        for nnz__nsmp, gsu__qtt in typ.table_type.type_to_blk.items():
            uuyh__arrd = c.context.get_constant(types.int64, len(typ.
                table_type.block_to_arr_ind[gsu__qtt]))
            jflq__lgplp, hizxb__qxs = ListInstance.allocate_ex(c.context, c
                .builder, types.List(nnz__nsmp), uuyh__arrd)
            hizxb__qxs.size = uuyh__arrd
            setattr(ork__xsqs, f'block_{gsu__qtt}', hizxb__qxs.value)
        lnpix__oahla = c.pyapi.call_method(val, '__len__', ())
        txu__cctn = c.pyapi.long_as_longlong(lnpix__oahla)
        c.pyapi.decref(lnpix__oahla)
        ork__xsqs.len = txu__cctn
        rvmbu__bcdkd = c.context.make_tuple(c.builder, types.Tuple([typ.
            table_type]), [ork__xsqs._getvalue()])
    else:
        rbgux__rhs = [c.context.get_constant_null(nnz__nsmp) for nnz__nsmp in
            typ.data]
        rvmbu__bcdkd = c.context.make_tuple(c.builder, types.Tuple(typ.data
            ), rbgux__rhs)
    espal__tma = construct_dataframe(c.context, c.builder, typ,
        rvmbu__bcdkd, zpyp__iouv, val, None)
    return NativeValue(espal__tma)


def get_hiframes_dtypes(df):
    if (hasattr(df, '_bodo_meta') and df._bodo_meta is not None and 
        'type_metadata' in df._bodo_meta and df._bodo_meta['type_metadata']
         is not None and len(df._bodo_meta['type_metadata'][1]) == len(df.
        columns)):
        xvdry__micvl = df._bodo_meta['type_metadata'][1]
    else:
        xvdry__micvl = [None] * len(df.columns)
    byl__lqcg = [dtype_to_array_type(_infer_series_dtype(df.iloc[:, i],
        array_metadata=xvdry__micvl[i])) for i in range(len(df.columns))]
    byl__lqcg = [(bodo.dict_str_arr_type if _use_dict_str_type and 
        nnz__nsmp == string_array_type else nnz__nsmp) for nnz__nsmp in
        byl__lqcg]
    return tuple(byl__lqcg)


class SeriesDtypeEnum(Enum):
    Int8 = 0
    UInt8 = 1
    Int32 = 2
    UInt32 = 3
    Int64 = 4
    UInt64 = 7
    Float32 = 5
    Float64 = 6
    Int16 = 8
    UInt16 = 9
    STRING = 10
    Bool = 11
    Decimal = 12
    Datime_Date = 13
    NP_Datetime64ns = 14
    NP_Timedelta64ns = 15
    Int128 = 16
    LIST = 18
    STRUCT = 19
    BINARY = 21
    ARRAY = 22
    PD_nullable_Int8 = 23
    PD_nullable_UInt8 = 24
    PD_nullable_Int16 = 25
    PD_nullable_UInt16 = 26
    PD_nullable_Int32 = 27
    PD_nullable_UInt32 = 28
    PD_nullable_Int64 = 29
    PD_nullable_UInt64 = 30
    PD_nullable_bool = 31
    CategoricalType = 32
    NoneType = 33
    Literal = 34
    IntegerArray = 35
    RangeIndexType = 36
    DatetimeIndexType = 37
    NumericIndexType = 38
    PeriodIndexType = 39
    IntervalIndexType = 40
    CategoricalIndexType = 41
    StringIndexType = 42
    BinaryIndexType = 43
    TimedeltaIndexType = 44
    LiteralType = 45


_one_to_one_type_to_enum_map = {types.int8: SeriesDtypeEnum.Int8.value,
    types.uint8: SeriesDtypeEnum.UInt8.value, types.int32: SeriesDtypeEnum.
    Int32.value, types.uint32: SeriesDtypeEnum.UInt32.value, types.int64:
    SeriesDtypeEnum.Int64.value, types.uint64: SeriesDtypeEnum.UInt64.value,
    types.float32: SeriesDtypeEnum.Float32.value, types.float64:
    SeriesDtypeEnum.Float64.value, types.NPDatetime('ns'): SeriesDtypeEnum.
    NP_Datetime64ns.value, types.NPTimedelta('ns'): SeriesDtypeEnum.
    NP_Timedelta64ns.value, types.bool_: SeriesDtypeEnum.Bool.value, types.
    int16: SeriesDtypeEnum.Int16.value, types.uint16: SeriesDtypeEnum.
    UInt16.value, types.Integer('int128', 128): SeriesDtypeEnum.Int128.
    value, bodo.hiframes.datetime_date_ext.datetime_date_type:
    SeriesDtypeEnum.Datime_Date.value, IntDtype(types.int8):
    SeriesDtypeEnum.PD_nullable_Int8.value, IntDtype(types.uint8):
    SeriesDtypeEnum.PD_nullable_UInt8.value, IntDtype(types.int16):
    SeriesDtypeEnum.PD_nullable_Int16.value, IntDtype(types.uint16):
    SeriesDtypeEnum.PD_nullable_UInt16.value, IntDtype(types.int32):
    SeriesDtypeEnum.PD_nullable_Int32.value, IntDtype(types.uint32):
    SeriesDtypeEnum.PD_nullable_UInt32.value, IntDtype(types.int64):
    SeriesDtypeEnum.PD_nullable_Int64.value, IntDtype(types.uint64):
    SeriesDtypeEnum.PD_nullable_UInt64.value, bytes_type: SeriesDtypeEnum.
    BINARY.value, string_type: SeriesDtypeEnum.STRING.value, bodo.bool_:
    SeriesDtypeEnum.Bool.value, types.none: SeriesDtypeEnum.NoneType.value}
_one_to_one_enum_to_type_map = {SeriesDtypeEnum.Int8.value: types.int8,
    SeriesDtypeEnum.UInt8.value: types.uint8, SeriesDtypeEnum.Int32.value:
    types.int32, SeriesDtypeEnum.UInt32.value: types.uint32,
    SeriesDtypeEnum.Int64.value: types.int64, SeriesDtypeEnum.UInt64.value:
    types.uint64, SeriesDtypeEnum.Float32.value: types.float32,
    SeriesDtypeEnum.Float64.value: types.float64, SeriesDtypeEnum.
    NP_Datetime64ns.value: types.NPDatetime('ns'), SeriesDtypeEnum.
    NP_Timedelta64ns.value: types.NPTimedelta('ns'), SeriesDtypeEnum.Int16.
    value: types.int16, SeriesDtypeEnum.UInt16.value: types.uint16,
    SeriesDtypeEnum.Int128.value: types.Integer('int128', 128),
    SeriesDtypeEnum.Datime_Date.value: bodo.hiframes.datetime_date_ext.
    datetime_date_type, SeriesDtypeEnum.PD_nullable_Int8.value: IntDtype(
    types.int8), SeriesDtypeEnum.PD_nullable_UInt8.value: IntDtype(types.
    uint8), SeriesDtypeEnum.PD_nullable_Int16.value: IntDtype(types.int16),
    SeriesDtypeEnum.PD_nullable_UInt16.value: IntDtype(types.uint16),
    SeriesDtypeEnum.PD_nullable_Int32.value: IntDtype(types.int32),
    SeriesDtypeEnum.PD_nullable_UInt32.value: IntDtype(types.uint32),
    SeriesDtypeEnum.PD_nullable_Int64.value: IntDtype(types.int64),
    SeriesDtypeEnum.PD_nullable_UInt64.value: IntDtype(types.uint64),
    SeriesDtypeEnum.BINARY.value: bytes_type, SeriesDtypeEnum.STRING.value:
    string_type, SeriesDtypeEnum.Bool.value: bodo.bool_, SeriesDtypeEnum.
    NoneType.value: types.none}


def _dtype_from_type_enum_list(typ_enum_list):
    byo__zzn, typ = _dtype_from_type_enum_list_recursor(typ_enum_list)
    if len(byo__zzn) != 0:
        raise_bodo_error(
            f"""Unexpected Internal Error while converting typing metadata: Dtype list was not fully consumed.
 Input typ_enum_list: {typ_enum_list}.
Remainder: {byo__zzn}. Please file the error here: https://github.com/Bodo-inc/Feedback"""
            )
    return typ


def _dtype_from_type_enum_list_recursor(typ_enum_list):
    if len(typ_enum_list) == 0:
        raise_bodo_error('Unable to infer dtype from empty typ_enum_list')
    elif typ_enum_list[0] in _one_to_one_enum_to_type_map:
        return typ_enum_list[1:], _one_to_one_enum_to_type_map[typ_enum_list[0]
            ]
    elif typ_enum_list[0] == SeriesDtypeEnum.IntegerArray.value:
        qft__dkts, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:])
        return qft__dkts, IntegerArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.ARRAY.value:
        qft__dkts, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:])
        return qft__dkts, dtype_to_array_type(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.Decimal.value:
        ised__hfbb = typ_enum_list[1]
        xvgos__iwga = typ_enum_list[2]
        return typ_enum_list[3:], Decimal128Type(ised__hfbb, xvgos__iwga)
    elif typ_enum_list[0] == SeriesDtypeEnum.STRUCT.value:
        jgrov__cxy = typ_enum_list[1]
        jmn__mci = tuple(typ_enum_list[2:2 + jgrov__cxy])
        rtov__ugl = typ_enum_list[2 + jgrov__cxy:]
        xsn__rcau = []
        for i in range(jgrov__cxy):
            rtov__ugl, enpsr__ezn = _dtype_from_type_enum_list_recursor(
                rtov__ugl)
            xsn__rcau.append(enpsr__ezn)
        return rtov__ugl, StructType(tuple(xsn__rcau), jmn__mci)
    elif typ_enum_list[0] == SeriesDtypeEnum.Literal.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'Literal' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        dyr__vaoj = typ_enum_list[1]
        rtov__ugl = typ_enum_list[2:]
        return rtov__ugl, dyr__vaoj
    elif typ_enum_list[0] == SeriesDtypeEnum.LiteralType.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'LiteralType' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        dyr__vaoj = typ_enum_list[1]
        rtov__ugl = typ_enum_list[2:]
        return rtov__ugl, numba.types.literal(dyr__vaoj)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalType.value:
        rtov__ugl, vxqmv__fvyy = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        rtov__ugl, djo__fcc = _dtype_from_type_enum_list_recursor(rtov__ugl)
        rtov__ugl, xcrrz__had = _dtype_from_type_enum_list_recursor(rtov__ugl)
        rtov__ugl, ndaw__ivaj = _dtype_from_type_enum_list_recursor(rtov__ugl)
        rtov__ugl, myxw__jtzh = _dtype_from_type_enum_list_recursor(rtov__ugl)
        return rtov__ugl, PDCategoricalDtype(vxqmv__fvyy, djo__fcc,
            xcrrz__had, ndaw__ivaj, myxw__jtzh)
    elif typ_enum_list[0] == SeriesDtypeEnum.DatetimeIndexType.value:
        rtov__ugl, ooqd__omkno = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return rtov__ugl, DatetimeIndexType(ooqd__omkno)
    elif typ_enum_list[0] == SeriesDtypeEnum.NumericIndexType.value:
        rtov__ugl, dtype = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        rtov__ugl, ooqd__omkno = _dtype_from_type_enum_list_recursor(rtov__ugl)
        rtov__ugl, ndaw__ivaj = _dtype_from_type_enum_list_recursor(rtov__ugl)
        return rtov__ugl, NumericIndexType(dtype, ooqd__omkno, ndaw__ivaj)
    elif typ_enum_list[0] == SeriesDtypeEnum.PeriodIndexType.value:
        rtov__ugl, gvttl__wtlo = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        rtov__ugl, ooqd__omkno = _dtype_from_type_enum_list_recursor(rtov__ugl)
        return rtov__ugl, PeriodIndexType(gvttl__wtlo, ooqd__omkno)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalIndexType.value:
        rtov__ugl, ndaw__ivaj = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        rtov__ugl, ooqd__omkno = _dtype_from_type_enum_list_recursor(rtov__ugl)
        return rtov__ugl, CategoricalIndexType(ndaw__ivaj, ooqd__omkno)
    elif typ_enum_list[0] == SeriesDtypeEnum.RangeIndexType.value:
        rtov__ugl, ooqd__omkno = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return rtov__ugl, RangeIndexType(ooqd__omkno)
    elif typ_enum_list[0] == SeriesDtypeEnum.StringIndexType.value:
        rtov__ugl, ooqd__omkno = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return rtov__ugl, StringIndexType(ooqd__omkno)
    elif typ_enum_list[0] == SeriesDtypeEnum.BinaryIndexType.value:
        rtov__ugl, ooqd__omkno = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return rtov__ugl, BinaryIndexType(ooqd__omkno)
    elif typ_enum_list[0] == SeriesDtypeEnum.TimedeltaIndexType.value:
        rtov__ugl, ooqd__omkno = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return rtov__ugl, TimedeltaIndexType(ooqd__omkno)
    else:
        raise_bodo_error(
            f'Unexpected Internal Error while converting typing metadata: unable to infer dtype for type enum {typ_enum_list[0]}. Please file the error here: https://github.com/Bodo-inc/Feedback'
            )


def _dtype_to_type_enum_list(typ):
    return guard(_dtype_to_type_enum_list_recursor, typ)


def _dtype_to_type_enum_list_recursor(typ, upcast_numeric_index=True):
    if typ.__hash__ and typ in _one_to_one_type_to_enum_map:
        return [_one_to_one_type_to_enum_map[typ]]
    if isinstance(typ, (dict, int, list, tuple, str, bool, bytes, float)):
        return [SeriesDtypeEnum.Literal.value, typ]
    elif typ is None:
        return [SeriesDtypeEnum.Literal.value, typ]
    elif is_overload_constant_int(typ):
        qtuzm__vfjqe = get_overload_const_int(typ)
        if numba.types.maybe_literal(qtuzm__vfjqe) == typ:
            return [SeriesDtypeEnum.LiteralType.value, qtuzm__vfjqe]
    elif is_overload_constant_str(typ):
        qtuzm__vfjqe = get_overload_const_str(typ)
        if numba.types.maybe_literal(qtuzm__vfjqe) == typ:
            return [SeriesDtypeEnum.LiteralType.value, qtuzm__vfjqe]
    elif is_overload_constant_bool(typ):
        qtuzm__vfjqe = get_overload_const_bool(typ)
        if numba.types.maybe_literal(qtuzm__vfjqe) == typ:
            return [SeriesDtypeEnum.LiteralType.value, qtuzm__vfjqe]
    elif isinstance(typ, IntegerArrayType):
        return [SeriesDtypeEnum.IntegerArray.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif bodo.utils.utils.is_array_typ(typ, False):
        return [SeriesDtypeEnum.ARRAY.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif isinstance(typ, StructType):
        jidt__sjdpj = [SeriesDtypeEnum.STRUCT.value, len(typ.names)]
        for fxmrl__iyzkr in typ.names:
            jidt__sjdpj.append(fxmrl__iyzkr)
        for cnatw__snc in typ.data:
            jidt__sjdpj += _dtype_to_type_enum_list_recursor(cnatw__snc)
        return jidt__sjdpj
    elif isinstance(typ, bodo.libs.decimal_arr_ext.Decimal128Type):
        return [SeriesDtypeEnum.Decimal.value, typ.precision, typ.scale]
    elif isinstance(typ, PDCategoricalDtype):
        psdrr__zvn = _dtype_to_type_enum_list_recursor(typ.categories)
        lnsz__xnu = _dtype_to_type_enum_list_recursor(typ.elem_type)
        tra__jra = _dtype_to_type_enum_list_recursor(typ.ordered)
        yky__mwgmy = _dtype_to_type_enum_list_recursor(typ.data)
        hxqp__dvwzx = _dtype_to_type_enum_list_recursor(typ.int_type)
        return [SeriesDtypeEnum.CategoricalType.value
            ] + psdrr__zvn + lnsz__xnu + tra__jra + yky__mwgmy + hxqp__dvwzx
    elif isinstance(typ, DatetimeIndexType):
        return [SeriesDtypeEnum.DatetimeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, NumericIndexType):
        if upcast_numeric_index:
            if isinstance(typ.dtype, types.Float):
                byurt__aigu = types.float64
                cyzy__xsvu = types.Array(byurt__aigu, 1, 'C')
            elif typ.dtype in {types.int8, types.int16, types.int32, types.
                int64}:
                byurt__aigu = types.int64
                if isinstance(typ.data, IntegerArrayType):
                    cyzy__xsvu = IntegerArrayType(byurt__aigu)
                else:
                    cyzy__xsvu = types.Array(byurt__aigu, 1, 'C')
            elif typ.dtype in {types.uint8, types.uint16, types.uint32,
                types.uint64}:
                byurt__aigu = types.uint64
                if isinstance(typ.data, IntegerArrayType):
                    cyzy__xsvu = IntegerArrayType(byurt__aigu)
                else:
                    cyzy__xsvu = types.Array(byurt__aigu, 1, 'C')
            elif typ.dtype == types.bool_:
                byurt__aigu = typ.dtype
                cyzy__xsvu = typ.data
            else:
                raise GuardException('Unable to convert type')
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(byurt__aigu
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(cyzy__xsvu)
        else:
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(typ.dtype
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(typ.data)
    elif isinstance(typ, PeriodIndexType):
        return [SeriesDtypeEnum.PeriodIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.freq
            ) + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, CategoricalIndexType):
        return [SeriesDtypeEnum.CategoricalIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.data
            ) + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, RangeIndexType):
        return [SeriesDtypeEnum.RangeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, StringIndexType):
        return [SeriesDtypeEnum.StringIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, BinaryIndexType):
        return [SeriesDtypeEnum.BinaryIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, TimedeltaIndexType):
        return [SeriesDtypeEnum.TimedeltaIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    else:
        raise GuardException('Unable to convert type')


def _infer_series_dtype(S, array_metadata=None):
    if S.dtype == np.dtype('O'):
        if len(S.values) == 0 or S.isna().sum() == len(S):
            if array_metadata != None:
                return _dtype_from_type_enum_list(array_metadata).dtype
            elif hasattr(S, '_bodo_meta'
                ) and S._bodo_meta is not None and 'type_metadata' in S._bodo_meta and S._bodo_meta[
                'type_metadata'][1] is not None:
                sjqzc__lauir = S._bodo_meta['type_metadata'][1]
                return _dtype_from_type_enum_list(sjqzc__lauir)
        return numba.typeof(S.values).dtype
    if isinstance(S.dtype, pd.core.arrays.floating.FloatingDtype):
        raise BodoError(
            """Bodo does not currently support Series constructed with Pandas FloatingArray.
Please use Series.astype() to convert any input Series input to Bodo JIT functions."""
            )
    if isinstance(S.dtype, pd.core.arrays.integer._IntegerDtype):
        return typeof_pd_int_dtype(S.dtype, None)
    elif isinstance(S.dtype, pd.CategoricalDtype):
        return bodo.typeof(S.dtype)
    elif isinstance(S.dtype, pd.StringDtype):
        return string_type
    elif isinstance(S.dtype, pd.BooleanDtype):
        return types.bool_
    if isinstance(S.dtype, pd.DatetimeTZDtype):
        bwe__fzztw = S.dtype.unit
        if bwe__fzztw != 'ns':
            raise BodoError("Timezone-aware datetime data requires 'ns' units")
        vvqhx__xpiu = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(S.
            dtype.tz)
        return PandasDatetimeTZDtype(vvqhx__xpiu)
    try:
        return numpy_support.from_dtype(S.dtype)
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


def _get_use_df_parent_obj_flag(builder, context, pyapi, parent_obj, n_cols):
    if n_cols is None:
        return context.get_constant(types.bool_, False)
    dtpsy__epunu = cgutils.is_not_null(builder, parent_obj)
    rfqcy__uexu = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with builder.if_then(dtpsy__epunu):
        ggd__pdf = pyapi.object_getattr_string(parent_obj, 'columns')
        lnpix__oahla = pyapi.call_method(ggd__pdf, '__len__', ())
        builder.store(pyapi.long_as_longlong(lnpix__oahla), rfqcy__uexu)
        pyapi.decref(lnpix__oahla)
        pyapi.decref(ggd__pdf)
    use_parent_obj = builder.and_(dtpsy__epunu, builder.icmp_unsigned('==',
        builder.load(rfqcy__uexu), context.get_constant(types.int64, n_cols)))
    return use_parent_obj


def _get_df_columns_obj(c, builder, context, pyapi, df_typ, dataframe_payload):
    if df_typ.has_runtime_cols:
        iplk__rxad = df_typ.runtime_colname_typ
        context.nrt.incref(builder, iplk__rxad, dataframe_payload.columns)
        return pyapi.from_native_value(iplk__rxad, dataframe_payload.
            columns, c.env_manager)
    if all(isinstance(c, str) for c in df_typ.columns):
        dhxgs__buu = pd.array(df_typ.columns, 'string')
    elif all(isinstance(c, int) for c in df_typ.columns):
        dhxgs__buu = np.array(df_typ.columns, 'int64')
    else:
        dhxgs__buu = df_typ.columns
    rhams__zja = numba.typeof(dhxgs__buu)
    swu__uhqx = context.get_constant_generic(builder, rhams__zja, dhxgs__buu)
    fjypk__nar = pyapi.from_native_value(rhams__zja, swu__uhqx, c.env_manager)
    return fjypk__nar


def _create_initial_df_object(builder, context, pyapi, c, df_typ, obj,
    dataframe_payload, res, use_parent_obj):
    with c.builder.if_else(use_parent_obj) as (psuhd__jyg, znea__lmtzh):
        with psuhd__jyg:
            pyapi.incref(obj)
            fdfa__fpjv = context.insert_const_string(c.builder.module, 'numpy')
            ydybg__xczf = pyapi.import_module_noblock(fdfa__fpjv)
            if df_typ.has_runtime_cols:
                hxr__tpxv = 0
            else:
                hxr__tpxv = len(df_typ.columns)
            xor__txgzc = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), hxr__tpxv))
            kaj__utb = pyapi.call_method(ydybg__xczf, 'arange', (xor__txgzc,))
            pyapi.object_setattr_string(obj, 'columns', kaj__utb)
            pyapi.decref(ydybg__xczf)
            pyapi.decref(kaj__utb)
            pyapi.decref(xor__txgzc)
        with znea__lmtzh:
            context.nrt.incref(builder, df_typ.index, dataframe_payload.index)
            kbrii__sgxq = c.pyapi.from_native_value(df_typ.index,
                dataframe_payload.index, c.env_manager)
            fdfa__fpjv = context.insert_const_string(c.builder.module, 'pandas'
                )
            ydybg__xczf = pyapi.import_module_noblock(fdfa__fpjv)
            df_obj = pyapi.call_method(ydybg__xczf, 'DataFrame', (pyapi.
                borrow_none(), kbrii__sgxq))
            pyapi.decref(ydybg__xczf)
            pyapi.decref(kbrii__sgxq)
            builder.store(df_obj, res)


@box(DataFrameType)
def box_dataframe(typ, val, c):
    from bodo.hiframes.table import box_table
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    dataframe_payload = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
        .context, c.builder, typ, val)
    sipva__cuysc = cgutils.create_struct_proxy(typ)(context, builder, value=val
        )
    n_cols = len(typ.columns) if not typ.has_runtime_cols else None
    obj = sipva__cuysc.parent
    res = cgutils.alloca_once_value(builder, obj)
    use_parent_obj = _get_use_df_parent_obj_flag(builder, context, pyapi,
        obj, n_cols)
    _create_initial_df_object(builder, context, pyapi, c, typ, obj,
        dataframe_payload, res, use_parent_obj)
    if typ.is_table_format:
        oje__xra = typ.table_type
        ork__xsqs = builder.extract_value(dataframe_payload.data, 0)
        context.nrt.incref(builder, oje__xra, ork__xsqs)
        adwf__ota = box_table(oje__xra, ork__xsqs, c, builder.not_(
            use_parent_obj))
        with builder.if_else(use_parent_obj) as (hyj__fppz, fxtuj__abx):
            with hyj__fppz:
                nyn__ajy = pyapi.object_getattr_string(adwf__ota, 'arrays')
                deg__vxyml = c.pyapi.make_none()
                if n_cols is None:
                    lnpix__oahla = pyapi.call_method(nyn__ajy, '__len__', ())
                    uuyh__arrd = pyapi.long_as_longlong(lnpix__oahla)
                    pyapi.decref(lnpix__oahla)
                else:
                    uuyh__arrd = context.get_constant(types.int64, n_cols)
                with cgutils.for_range(builder, uuyh__arrd) as dhxu__ntzoy:
                    i = dhxu__ntzoy.index
                    xldex__fol = pyapi.list_getitem(nyn__ajy, i)
                    ddlvr__nin = c.builder.icmp_unsigned('!=', xldex__fol,
                        deg__vxyml)
                    with builder.if_then(ddlvr__nin):
                        hkodr__rzn = pyapi.long_from_longlong(i)
                        df_obj = builder.load(res)
                        pyapi.object_setitem(df_obj, hkodr__rzn, xldex__fol)
                        pyapi.decref(hkodr__rzn)
                pyapi.decref(nyn__ajy)
                pyapi.decref(deg__vxyml)
            with fxtuj__abx:
                df_obj = builder.load(res)
                kbrii__sgxq = pyapi.object_getattr_string(df_obj, 'index')
                vcbp__qkneb = c.pyapi.call_method(adwf__ota, 'to_pandas', (
                    kbrii__sgxq,))
                builder.store(vcbp__qkneb, res)
                pyapi.decref(df_obj)
                pyapi.decref(kbrii__sgxq)
        pyapi.decref(adwf__ota)
    else:
        qxwep__dab = [builder.extract_value(dataframe_payload.data, i) for
            i in range(n_cols)]
        xok__rzn = typ.data
        for i, qjtou__apb, xgzgb__cbkqi in zip(range(n_cols), qxwep__dab,
            xok__rzn):
            ebvw__jwx = cgutils.alloca_once_value(builder, qjtou__apb)
            tra__kow = cgutils.alloca_once_value(builder, context.
                get_constant_null(xgzgb__cbkqi))
            ddlvr__nin = builder.not_(is_ll_eq(builder, ebvw__jwx, tra__kow))
            tcbf__rfqmb = builder.or_(builder.not_(use_parent_obj), builder
                .and_(use_parent_obj, ddlvr__nin))
            with builder.if_then(tcbf__rfqmb):
                hkodr__rzn = pyapi.long_from_longlong(context.get_constant(
                    types.int64, i))
                context.nrt.incref(builder, xgzgb__cbkqi, qjtou__apb)
                arr_obj = pyapi.from_native_value(xgzgb__cbkqi, qjtou__apb,
                    c.env_manager)
                df_obj = builder.load(res)
                pyapi.object_setitem(df_obj, hkodr__rzn, arr_obj)
                pyapi.decref(arr_obj)
                pyapi.decref(hkodr__rzn)
    df_obj = builder.load(res)
    fjypk__nar = _get_df_columns_obj(c, builder, context, pyapi, typ,
        dataframe_payload)
    pyapi.object_setattr_string(df_obj, 'columns', fjypk__nar)
    pyapi.decref(fjypk__nar)
    _set_bodo_meta_dataframe(c, df_obj, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return df_obj


def get_df_obj_column_codegen(context, builder, pyapi, df_obj, col_ind,
    data_typ):
    deg__vxyml = pyapi.borrow_none()
    ihsv__mnqds = pyapi.unserialize(pyapi.serialize_object(slice))
    lrgxv__zfn = pyapi.call_function_objargs(ihsv__mnqds, [deg__vxyml])
    nruo__rmfgv = pyapi.long_from_longlong(col_ind)
    gfo__lta = pyapi.tuple_pack([lrgxv__zfn, nruo__rmfgv])
    ebhv__dyh = pyapi.object_getattr_string(df_obj, 'iloc')
    mjmqj__vmtwl = pyapi.object_getitem(ebhv__dyh, gfo__lta)
    if isinstance(data_typ, bodo.DatetimeArrayType):
        uvmmq__soff = pyapi.object_getattr_string(mjmqj__vmtwl, 'array')
    else:
        uvmmq__soff = pyapi.object_getattr_string(mjmqj__vmtwl, 'values')
    if isinstance(data_typ, types.Array):
        xxuv__lzfd = context.insert_const_string(builder.module, 'numpy')
        ahrk__kpd = pyapi.import_module_noblock(xxuv__lzfd)
        arr_obj = pyapi.call_method(ahrk__kpd, 'ascontiguousarray', (
            uvmmq__soff,))
        pyapi.decref(uvmmq__soff)
        pyapi.decref(ahrk__kpd)
    else:
        arr_obj = uvmmq__soff
    pyapi.decref(ihsv__mnqds)
    pyapi.decref(lrgxv__zfn)
    pyapi.decref(nruo__rmfgv)
    pyapi.decref(gfo__lta)
    pyapi.decref(ebhv__dyh)
    pyapi.decref(mjmqj__vmtwl)
    return arr_obj


@intrinsic
def unbox_dataframe_column(typingctx, df, i=None):
    assert isinstance(df, DataFrameType) and is_overload_constant_int(i)

    def codegen(context, builder, sig, args):
        pyapi = context.get_python_api(builder)
        c = numba.core.pythonapi._UnboxContext(context, builder, pyapi)
        df_typ = sig.args[0]
        col_ind = get_overload_const_int(sig.args[1])
        data_typ = df_typ.data[col_ind]
        sipva__cuysc = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        arr_obj = get_df_obj_column_codegen(context, builder, pyapi,
            sipva__cuysc.parent, args[1], data_typ)
        thlv__gksp = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(arr_obj)
        dataframe_payload = (bodo.hiframes.pd_dataframe_ext.
            get_dataframe_payload(c.context, c.builder, df_typ, args[0]))
        if df_typ.is_table_format:
            ork__xsqs = cgutils.create_struct_proxy(df_typ.table_type)(c.
                context, c.builder, builder.extract_value(dataframe_payload
                .data, 0))
            gsu__qtt = df_typ.table_type.type_to_blk[data_typ]
            bcd__yraz = getattr(ork__xsqs, f'block_{gsu__qtt}')
            tsjm__gpz = ListInstance(c.context, c.builder, types.List(
                data_typ), bcd__yraz)
            itin__qeurl = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[col_ind])
            tsjm__gpz.inititem(itin__qeurl, thlv__gksp.value, incref=False)
        else:
            dataframe_payload.data = builder.insert_value(dataframe_payload
                .data, thlv__gksp.value, col_ind)
        psotp__ubgy = DataFramePayloadType(df_typ)
        nbxxk__tsbhs = context.nrt.meminfo_data(builder, sipva__cuysc.meminfo)
        czis__zkan = context.get_value_type(psotp__ubgy).as_pointer()
        nbxxk__tsbhs = builder.bitcast(nbxxk__tsbhs, czis__zkan)
        builder.store(dataframe_payload._getvalue(), nbxxk__tsbhs)
    return signature(types.none, df, i), codegen


@numba.njit
def unbox_col_if_needed(df, i):
    if bodo.hiframes.pd_dataframe_ext.has_parent(df
        ) and bodo.hiframes.pd_dataframe_ext._column_needs_unboxing(df, i):
        bodo.hiframes.boxing.unbox_dataframe_column(df, i)


@unbox(SeriesType)
def unbox_series(typ, val, c):
    if isinstance(typ.data, DatetimeArrayType):
        uvmmq__soff = c.pyapi.object_getattr_string(val, 'array')
    else:
        uvmmq__soff = c.pyapi.object_getattr_string(val, 'values')
    if isinstance(typ.data, types.Array):
        xxuv__lzfd = c.context.insert_const_string(c.builder.module, 'numpy')
        ahrk__kpd = c.pyapi.import_module_noblock(xxuv__lzfd)
        arr_obj = c.pyapi.call_method(ahrk__kpd, 'ascontiguousarray', (
            uvmmq__soff,))
        c.pyapi.decref(uvmmq__soff)
        c.pyapi.decref(ahrk__kpd)
    else:
        arr_obj = uvmmq__soff
    chc__lqhu = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    kbrii__sgxq = c.pyapi.object_getattr_string(val, 'index')
    zpyp__iouv = c.pyapi.to_native_value(typ.index, kbrii__sgxq).value
    dzkqc__ivuwe = c.pyapi.object_getattr_string(val, 'name')
    idpci__vzsfh = c.pyapi.to_native_value(typ.name_typ, dzkqc__ivuwe).value
    cfqel__mln = bodo.hiframes.pd_series_ext.construct_series(c.context, c.
        builder, typ, chc__lqhu, zpyp__iouv, idpci__vzsfh)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(kbrii__sgxq)
    c.pyapi.decref(dzkqc__ivuwe)
    return NativeValue(cfqel__mln)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        ryul__nxci = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(ryul__nxci._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    fdfa__fpjv = c.context.insert_const_string(c.builder.module, 'pandas')
    mxgg__oiw = c.pyapi.import_module_noblock(fdfa__fpjv)
    qycef__lnczo = bodo.hiframes.pd_series_ext.get_series_payload(c.context,
        c.builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, qycef__lnczo.data)
    c.context.nrt.incref(c.builder, typ.index, qycef__lnczo.index)
    c.context.nrt.incref(c.builder, typ.name_typ, qycef__lnczo.name)
    arr_obj = c.pyapi.from_native_value(typ.data, qycef__lnczo.data, c.
        env_manager)
    kbrii__sgxq = c.pyapi.from_native_value(typ.index, qycef__lnczo.index,
        c.env_manager)
    dzkqc__ivuwe = c.pyapi.from_native_value(typ.name_typ, qycef__lnczo.
        name, c.env_manager)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        dtype = c.pyapi.unserialize(c.pyapi.serialize_object(object))
    else:
        dtype = c.pyapi.make_none()
    res = c.pyapi.call_method(mxgg__oiw, 'Series', (arr_obj, kbrii__sgxq,
        dtype, dzkqc__ivuwe))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(kbrii__sgxq)
    c.pyapi.decref(dzkqc__ivuwe)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        c.pyapi.decref(dtype)
    _set_bodo_meta_series(res, c, typ)
    c.pyapi.decref(mxgg__oiw)
    c.context.nrt.decref(c.builder, typ, val)
    return res


def type_enum_list_to_py_list_obj(pyapi, context, builder, env_manager,
    typ_list):
    vvbej__yqf = []
    for qthqm__zdfs in typ_list:
        if isinstance(qthqm__zdfs, int) and not isinstance(qthqm__zdfs, bool):
            eulod__angga = pyapi.long_from_longlong(lir.Constant(lir.
                IntType(64), qthqm__zdfs))
        else:
            fbqu__wlf = numba.typeof(qthqm__zdfs)
            tfoo__vtp = context.get_constant_generic(builder, fbqu__wlf,
                qthqm__zdfs)
            eulod__angga = pyapi.from_native_value(fbqu__wlf, tfoo__vtp,
                env_manager)
        vvbej__yqf.append(eulod__angga)
    rjb__inya = pyapi.list_pack(vvbej__yqf)
    for val in vvbej__yqf:
        pyapi.decref(val)
    return rjb__inya


def _set_bodo_meta_dataframe(c, obj, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    vwozf__rrp = not typ.has_runtime_cols
    jxr__gfmgm = 2 if vwozf__rrp else 1
    nasl__hbs = pyapi.dict_new(jxr__gfmgm)
    hbidn__vos = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ
        .dist.value))
    pyapi.dict_setitem_string(nasl__hbs, 'dist', hbidn__vos)
    pyapi.decref(hbidn__vos)
    if vwozf__rrp:
        zxwnb__dejx = _dtype_to_type_enum_list(typ.index)
        if zxwnb__dejx != None:
            ietve__ovgsc = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, zxwnb__dejx)
        else:
            ietve__ovgsc = pyapi.make_none()
        if typ.is_table_format:
            nnz__nsmp = typ.table_type
            thq__qmqak = pyapi.list_new(lir.Constant(lir.IntType(64), len(
                typ.data)))
            for gsu__qtt, dtype in nnz__nsmp.blk_to_type.items():
                typ_list = _dtype_to_type_enum_list(dtype)
                if typ_list != None:
                    typ_list = type_enum_list_to_py_list_obj(pyapi, context,
                        builder, c.env_manager, typ_list)
                else:
                    typ_list = pyapi.make_none()
                uuyh__arrd = c.context.get_constant(types.int64, len(
                    nnz__nsmp.block_to_arr_ind[gsu__qtt]))
                tma__oenr = c.context.make_constant_array(c.builder, types.
                    Array(types.int64, 1, 'C'), np.array(nnz__nsmp.
                    block_to_arr_ind[gsu__qtt], dtype=np.int64))
                mck__tmlg = c.context.make_array(types.Array(types.int64, 1,
                    'C'))(c.context, c.builder, tma__oenr)
                with cgutils.for_range(c.builder, uuyh__arrd) as dhxu__ntzoy:
                    i = dhxu__ntzoy.index
                    ukuwd__cpgr = _getitem_array_single_int(c.context, c.
                        builder, types.int64, types.Array(types.int64, 1,
                        'C'), mck__tmlg, i)
                    c.context.nrt.incref(builder, types.pyobject, typ_list)
                    pyapi.list_setitem(thq__qmqak, ukuwd__cpgr, typ_list)
                c.context.nrt.decref(builder, types.pyobject, typ_list)
        else:
            kgga__spmc = []
            for dtype in typ.data:
                typ_list = _dtype_to_type_enum_list(dtype)
                if typ_list != None:
                    rjb__inya = type_enum_list_to_py_list_obj(pyapi,
                        context, builder, c.env_manager, typ_list)
                else:
                    rjb__inya = pyapi.make_none()
                kgga__spmc.append(rjb__inya)
            thq__qmqak = pyapi.list_pack(kgga__spmc)
            for val in kgga__spmc:
                pyapi.decref(val)
        ddh__unl = pyapi.list_pack([ietve__ovgsc, thq__qmqak])
        pyapi.dict_setitem_string(nasl__hbs, 'type_metadata', ddh__unl)
    pyapi.object_setattr_string(obj, '_bodo_meta', nasl__hbs)
    pyapi.decref(nasl__hbs)


def get_series_dtype_handle_null_int_and_hetrogenous(series_typ):
    if isinstance(series_typ, HeterogeneousSeriesType):
        return None
    if isinstance(series_typ.dtype, types.Number) and isinstance(series_typ
        .data, IntegerArrayType):
        return IntDtype(series_typ.dtype)
    return series_typ.dtype


def _set_bodo_meta_series(obj, c, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    nasl__hbs = pyapi.dict_new(2)
    hbidn__vos = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ
        .dist.value))
    zxwnb__dejx = _dtype_to_type_enum_list(typ.index)
    if zxwnb__dejx != None:
        ietve__ovgsc = type_enum_list_to_py_list_obj(pyapi, context,
            builder, c.env_manager, zxwnb__dejx)
    else:
        ietve__ovgsc = pyapi.make_none()
    dtype = get_series_dtype_handle_null_int_and_hetrogenous(typ)
    if dtype != None:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            wzjf__wmkom = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            wzjf__wmkom = pyapi.make_none()
    else:
        wzjf__wmkom = pyapi.make_none()
    qat__fbo = pyapi.list_pack([ietve__ovgsc, wzjf__wmkom])
    pyapi.dict_setitem_string(nasl__hbs, 'type_metadata', qat__fbo)
    pyapi.decref(qat__fbo)
    pyapi.dict_setitem_string(nasl__hbs, 'dist', hbidn__vos)
    pyapi.object_setattr_string(obj, '_bodo_meta', nasl__hbs)
    pyapi.decref(nasl__hbs)
    pyapi.decref(hbidn__vos)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as vugq__xeyej:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    paaw__rvao = numba.np.numpy_support.map_layout(val)
    osw__qfxss = not val.flags.writeable
    return types.Array(dtype, val.ndim, paaw__rvao, readonly=osw__qfxss)


def _infer_ndarray_obj_dtype(val):
    if not val.dtype == np.dtype('O'):
        raise BodoError('Unsupported array dtype: {}'.format(val.dtype))
    i = 0
    while i < len(val) and (pd.api.types.is_scalar(val[i]) and pd.isna(val[
        i]) or not pd.api.types.is_scalar(val[i]) and len(val[i]) == 0):
        i += 1
    if i == len(val):
        warnings.warn(BodoWarning(
            'Empty object array passed to Bodo, which causes ambiguity in typing. This can cause errors in parallel execution.'
            ))
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    cim__rycs = val[i]
    if isinstance(cim__rycs, str):
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    elif isinstance(cim__rycs, bytes):
        return binary_array_type
    elif isinstance(cim__rycs, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(cim__rycs, (int, np.int8, np.int16, np.int32, np.int64,
        np.uint8, np.uint16, np.uint32, np.uint64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(cim__rycs))
    elif isinstance(cim__rycs, (dict, Dict)) and all(isinstance(ttiun__upam,
        str) for ttiun__upam in cim__rycs.keys()):
        jmn__mci = tuple(cim__rycs.keys())
        vakl__nggv = tuple(_get_struct_value_arr_type(v) for v in cim__rycs
            .values())
        return StructArrayType(vakl__nggv, jmn__mci)
    elif isinstance(cim__rycs, (dict, Dict)):
        prsb__jcdl = numba.typeof(_value_to_array(list(cim__rycs.keys())))
        hnh__ept = numba.typeof(_value_to_array(list(cim__rycs.values())))
        prsb__jcdl = to_str_arr_if_dict_array(prsb__jcdl)
        hnh__ept = to_str_arr_if_dict_array(hnh__ept)
        return MapArrayType(prsb__jcdl, hnh__ept)
    elif isinstance(cim__rycs, tuple):
        vakl__nggv = tuple(_get_struct_value_arr_type(v) for v in cim__rycs)
        return TupleArrayType(vakl__nggv)
    if isinstance(cim__rycs, (list, np.ndarray, pd.arrays.BooleanArray, pd.
        arrays.IntegerArray, pd.arrays.StringArray)):
        if isinstance(cim__rycs, list):
            cim__rycs = _value_to_array(cim__rycs)
        itne__wubqi = numba.typeof(cim__rycs)
        itne__wubqi = to_str_arr_if_dict_array(itne__wubqi)
        return ArrayItemArrayType(itne__wubqi)
    if isinstance(cim__rycs, datetime.date):
        return datetime_date_array_type
    if isinstance(cim__rycs, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(cim__rycs, bodo.Time):
        return TimeArrayType(cim__rycs.precision)
    if isinstance(cim__rycs, decimal.Decimal):
        return DecimalArrayType(38, 18)
    if isinstance(cim__rycs, pd._libs.interval.Interval):
        return bodo.libs.interval_arr_ext.IntervalArrayType
    raise BodoError(f'Unsupported object array with first value: {cim__rycs}')


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    nlyxm__xagd = val.copy()
    nlyxm__xagd.append(None)
    qjtou__apb = np.array(nlyxm__xagd, np.object_)
    if len(val) and isinstance(val[0], float):
        qjtou__apb = np.array(val, np.float64)
    return qjtou__apb


def _get_struct_value_arr_type(v):
    if isinstance(v, (dict, Dict)):
        return numba.typeof(_value_to_array(v))
    if isinstance(v, list):
        return dtype_to_array_type(numba.typeof(_value_to_array(v)))
    if pd.api.types.is_scalar(v) and pd.isna(v):
        warnings.warn(BodoWarning(
            'Field value in struct array is NA, which causes ambiguity in typing. This can cause errors in parallel execution.'
            ))
        return string_array_type
    xgzgb__cbkqi = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        xgzgb__cbkqi = to_nullable_type(xgzgb__cbkqi)
    return xgzgb__cbkqi
