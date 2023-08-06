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
    htw__phmch = tuple(val.columns.to_list())
    dazqr__aqczg = get_hiframes_dtypes(val)
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and len(val._bodo_meta['type_metadata'
        ][1]) == len(val.columns) and val._bodo_meta['type_metadata'][0] is not
        None):
        ivy__lsz = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        ivy__lsz = numba.typeof(val.index)
    vclxj__ugaev = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    ebb__nimo = len(dazqr__aqczg) >= TABLE_FORMAT_THRESHOLD
    return DataFrameType(dazqr__aqczg, ivy__lsz, htw__phmch, vclxj__ugaev,
        is_table_format=ebb__nimo)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    vclxj__ugaev = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and val._bodo_meta['type_metadata'][0]
         is not None):
        edo__wtbdi = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        edo__wtbdi = numba.typeof(val.index)
    dtype = _infer_series_dtype(val)
    bdo__ppxym = dtype_to_array_type(dtype)
    if _use_dict_str_type and bdo__ppxym == string_array_type:
        bdo__ppxym = bodo.dict_str_arr_type
    return SeriesType(dtype, data=bdo__ppxym, index=edo__wtbdi, name_typ=
        numba.typeof(val.name), dist=vclxj__ugaev)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    check_runtime_cols_unsupported(typ, 'Unboxing')
    iaq__yiyx = c.pyapi.object_getattr_string(val, 'index')
    aie__szl = c.pyapi.to_native_value(typ.index, iaq__yiyx).value
    c.pyapi.decref(iaq__yiyx)
    if typ.is_table_format:
        hfehy__kujt = cgutils.create_struct_proxy(typ.table_type)(c.context,
            c.builder)
        hfehy__kujt.parent = val
        for fbiq__mmd, tnb__bpt in typ.table_type.type_to_blk.items():
            lsea__ywe = c.context.get_constant(types.int64, len(typ.
                table_type.block_to_arr_ind[tnb__bpt]))
            cdljw__rgfw, zuj__yjzdz = ListInstance.allocate_ex(c.context, c
                .builder, types.List(fbiq__mmd), lsea__ywe)
            zuj__yjzdz.size = lsea__ywe
            setattr(hfehy__kujt, f'block_{tnb__bpt}', zuj__yjzdz.value)
        onu__ilzpn = c.pyapi.call_method(val, '__len__', ())
        hsq__eclv = c.pyapi.long_as_longlong(onu__ilzpn)
        c.pyapi.decref(onu__ilzpn)
        hfehy__kujt.len = hsq__eclv
        kiq__mprz = c.context.make_tuple(c.builder, types.Tuple([typ.
            table_type]), [hfehy__kujt._getvalue()])
    else:
        xbmk__okuq = [c.context.get_constant_null(fbiq__mmd) for fbiq__mmd in
            typ.data]
        kiq__mprz = c.context.make_tuple(c.builder, types.Tuple(typ.data),
            xbmk__okuq)
    titb__nbvk = construct_dataframe(c.context, c.builder, typ, kiq__mprz,
        aie__szl, val, None)
    return NativeValue(titb__nbvk)


def get_hiframes_dtypes(df):
    if (hasattr(df, '_bodo_meta') and df._bodo_meta is not None and 
        'type_metadata' in df._bodo_meta and df._bodo_meta['type_metadata']
         is not None and len(df._bodo_meta['type_metadata'][1]) == len(df.
        columns)):
        kba__uqi = df._bodo_meta['type_metadata'][1]
    else:
        kba__uqi = [None] * len(df.columns)
    zdwua__lwpa = [dtype_to_array_type(_infer_series_dtype(df.iloc[:, i],
        array_metadata=kba__uqi[i])) for i in range(len(df.columns))]
    zdwua__lwpa = [(bodo.dict_str_arr_type if _use_dict_str_type and 
        fbiq__mmd == string_array_type else fbiq__mmd) for fbiq__mmd in
        zdwua__lwpa]
    return tuple(zdwua__lwpa)


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
    zjy__fqc, typ = _dtype_from_type_enum_list_recursor(typ_enum_list)
    if len(zjy__fqc) != 0:
        raise_bodo_error(
            f"""Unexpected Internal Error while converting typing metadata: Dtype list was not fully consumed.
 Input typ_enum_list: {typ_enum_list}.
Remainder: {zjy__fqc}. Please file the error here: https://github.com/Bodo-inc/Feedback"""
            )
    return typ


def _dtype_from_type_enum_list_recursor(typ_enum_list):
    if len(typ_enum_list) == 0:
        raise_bodo_error('Unable to infer dtype from empty typ_enum_list')
    elif typ_enum_list[0] in _one_to_one_enum_to_type_map:
        return typ_enum_list[1:], _one_to_one_enum_to_type_map[typ_enum_list[0]
            ]
    elif typ_enum_list[0] == SeriesDtypeEnum.IntegerArray.value:
        shfod__qtkz, typ = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        return shfod__qtkz, IntegerArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.ARRAY.value:
        shfod__qtkz, typ = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        return shfod__qtkz, dtype_to_array_type(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.Decimal.value:
        njpx__obqo = typ_enum_list[1]
        ztdhf__sbyjq = typ_enum_list[2]
        return typ_enum_list[3:], Decimal128Type(njpx__obqo, ztdhf__sbyjq)
    elif typ_enum_list[0] == SeriesDtypeEnum.STRUCT.value:
        qxdd__gehfl = typ_enum_list[1]
        vtpkk__mcs = tuple(typ_enum_list[2:2 + qxdd__gehfl])
        iqbh__kpt = typ_enum_list[2 + qxdd__gehfl:]
        ybz__kyuo = []
        for i in range(qxdd__gehfl):
            iqbh__kpt, hnc__rxyf = _dtype_from_type_enum_list_recursor(
                iqbh__kpt)
            ybz__kyuo.append(hnc__rxyf)
        return iqbh__kpt, StructType(tuple(ybz__kyuo), vtpkk__mcs)
    elif typ_enum_list[0] == SeriesDtypeEnum.Literal.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'Literal' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        wkb__kqi = typ_enum_list[1]
        iqbh__kpt = typ_enum_list[2:]
        return iqbh__kpt, wkb__kqi
    elif typ_enum_list[0] == SeriesDtypeEnum.LiteralType.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'LiteralType' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        wkb__kqi = typ_enum_list[1]
        iqbh__kpt = typ_enum_list[2:]
        return iqbh__kpt, numba.types.literal(wkb__kqi)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalType.value:
        iqbh__kpt, rcv__wpqkx = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        iqbh__kpt, yin__phm = _dtype_from_type_enum_list_recursor(iqbh__kpt)
        iqbh__kpt, lih__yoca = _dtype_from_type_enum_list_recursor(iqbh__kpt)
        iqbh__kpt, wmh__qdmfq = _dtype_from_type_enum_list_recursor(iqbh__kpt)
        iqbh__kpt, kcjqw__yfahw = _dtype_from_type_enum_list_recursor(iqbh__kpt
            )
        return iqbh__kpt, PDCategoricalDtype(rcv__wpqkx, yin__phm,
            lih__yoca, wmh__qdmfq, kcjqw__yfahw)
    elif typ_enum_list[0] == SeriesDtypeEnum.DatetimeIndexType.value:
        iqbh__kpt, ibxn__cxy = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return iqbh__kpt, DatetimeIndexType(ibxn__cxy)
    elif typ_enum_list[0] == SeriesDtypeEnum.NumericIndexType.value:
        iqbh__kpt, dtype = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        iqbh__kpt, ibxn__cxy = _dtype_from_type_enum_list_recursor(iqbh__kpt)
        iqbh__kpt, wmh__qdmfq = _dtype_from_type_enum_list_recursor(iqbh__kpt)
        return iqbh__kpt, NumericIndexType(dtype, ibxn__cxy, wmh__qdmfq)
    elif typ_enum_list[0] == SeriesDtypeEnum.PeriodIndexType.value:
        iqbh__kpt, ipb__ancfq = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        iqbh__kpt, ibxn__cxy = _dtype_from_type_enum_list_recursor(iqbh__kpt)
        return iqbh__kpt, PeriodIndexType(ipb__ancfq, ibxn__cxy)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalIndexType.value:
        iqbh__kpt, wmh__qdmfq = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        iqbh__kpt, ibxn__cxy = _dtype_from_type_enum_list_recursor(iqbh__kpt)
        return iqbh__kpt, CategoricalIndexType(wmh__qdmfq, ibxn__cxy)
    elif typ_enum_list[0] == SeriesDtypeEnum.RangeIndexType.value:
        iqbh__kpt, ibxn__cxy = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return iqbh__kpt, RangeIndexType(ibxn__cxy)
    elif typ_enum_list[0] == SeriesDtypeEnum.StringIndexType.value:
        iqbh__kpt, ibxn__cxy = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return iqbh__kpt, StringIndexType(ibxn__cxy)
    elif typ_enum_list[0] == SeriesDtypeEnum.BinaryIndexType.value:
        iqbh__kpt, ibxn__cxy = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return iqbh__kpt, BinaryIndexType(ibxn__cxy)
    elif typ_enum_list[0] == SeriesDtypeEnum.TimedeltaIndexType.value:
        iqbh__kpt, ibxn__cxy = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return iqbh__kpt, TimedeltaIndexType(ibxn__cxy)
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
        fiish__civi = get_overload_const_int(typ)
        if numba.types.maybe_literal(fiish__civi) == typ:
            return [SeriesDtypeEnum.LiteralType.value, fiish__civi]
    elif is_overload_constant_str(typ):
        fiish__civi = get_overload_const_str(typ)
        if numba.types.maybe_literal(fiish__civi) == typ:
            return [SeriesDtypeEnum.LiteralType.value, fiish__civi]
    elif is_overload_constant_bool(typ):
        fiish__civi = get_overload_const_bool(typ)
        if numba.types.maybe_literal(fiish__civi) == typ:
            return [SeriesDtypeEnum.LiteralType.value, fiish__civi]
    elif isinstance(typ, IntegerArrayType):
        return [SeriesDtypeEnum.IntegerArray.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif bodo.utils.utils.is_array_typ(typ, False):
        return [SeriesDtypeEnum.ARRAY.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif isinstance(typ, StructType):
        errig__pxngf = [SeriesDtypeEnum.STRUCT.value, len(typ.names)]
        for xcn__zbcqw in typ.names:
            errig__pxngf.append(xcn__zbcqw)
        for hks__txds in typ.data:
            errig__pxngf += _dtype_to_type_enum_list_recursor(hks__txds)
        return errig__pxngf
    elif isinstance(typ, bodo.libs.decimal_arr_ext.Decimal128Type):
        return [SeriesDtypeEnum.Decimal.value, typ.precision, typ.scale]
    elif isinstance(typ, PDCategoricalDtype):
        vya__etxpj = _dtype_to_type_enum_list_recursor(typ.categories)
        yisl__ath = _dtype_to_type_enum_list_recursor(typ.elem_type)
        podqj__els = _dtype_to_type_enum_list_recursor(typ.ordered)
        kcnbz__jjz = _dtype_to_type_enum_list_recursor(typ.data)
        vktn__iphyp = _dtype_to_type_enum_list_recursor(typ.int_type)
        return [SeriesDtypeEnum.CategoricalType.value
            ] + vya__etxpj + yisl__ath + podqj__els + kcnbz__jjz + vktn__iphyp
    elif isinstance(typ, DatetimeIndexType):
        return [SeriesDtypeEnum.DatetimeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, NumericIndexType):
        if upcast_numeric_index:
            if isinstance(typ.dtype, types.Float):
                xnj__apr = types.float64
                uvza__lfg = types.Array(xnj__apr, 1, 'C')
            elif typ.dtype in {types.int8, types.int16, types.int32, types.
                int64}:
                xnj__apr = types.int64
                if isinstance(typ.data, IntegerArrayType):
                    uvza__lfg = IntegerArrayType(xnj__apr)
                else:
                    uvza__lfg = types.Array(xnj__apr, 1, 'C')
            elif typ.dtype in {types.uint8, types.uint16, types.uint32,
                types.uint64}:
                xnj__apr = types.uint64
                if isinstance(typ.data, IntegerArrayType):
                    uvza__lfg = IntegerArrayType(xnj__apr)
                else:
                    uvza__lfg = types.Array(xnj__apr, 1, 'C')
            elif typ.dtype == types.bool_:
                xnj__apr = typ.dtype
                uvza__lfg = typ.data
            else:
                raise GuardException('Unable to convert type')
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(xnj__apr
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(uvza__lfg)
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
                tzcpw__lpzc = S._bodo_meta['type_metadata'][1]
                return _dtype_from_type_enum_list(tzcpw__lpzc)
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
        jekqy__lvdwz = S.dtype.unit
        if jekqy__lvdwz != 'ns':
            raise BodoError("Timezone-aware datetime data requires 'ns' units")
        jkpxo__unyq = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(S.
            dtype.tz)
        return PandasDatetimeTZDtype(jkpxo__unyq)
    try:
        return numpy_support.from_dtype(S.dtype)
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


def _get_use_df_parent_obj_flag(builder, context, pyapi, parent_obj, n_cols):
    if n_cols is None:
        return context.get_constant(types.bool_, False)
    nqwkt__akg = cgutils.is_not_null(builder, parent_obj)
    xwpc__bnm = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with builder.if_then(nqwkt__akg):
        yhd__ieb = pyapi.object_getattr_string(parent_obj, 'columns')
        onu__ilzpn = pyapi.call_method(yhd__ieb, '__len__', ())
        builder.store(pyapi.long_as_longlong(onu__ilzpn), xwpc__bnm)
        pyapi.decref(onu__ilzpn)
        pyapi.decref(yhd__ieb)
    use_parent_obj = builder.and_(nqwkt__akg, builder.icmp_unsigned('==',
        builder.load(xwpc__bnm), context.get_constant(types.int64, n_cols)))
    return use_parent_obj


def _get_df_columns_obj(c, builder, context, pyapi, df_typ, dataframe_payload):
    if df_typ.has_runtime_cols:
        frmbe__raywv = df_typ.runtime_colname_typ
        context.nrt.incref(builder, frmbe__raywv, dataframe_payload.columns)
        return pyapi.from_native_value(frmbe__raywv, dataframe_payload.
            columns, c.env_manager)
    if all(isinstance(c, str) for c in df_typ.columns):
        wbxy__wfzb = pd.array(df_typ.columns, 'string')
    elif all(isinstance(c, int) for c in df_typ.columns):
        wbxy__wfzb = np.array(df_typ.columns, 'int64')
    else:
        wbxy__wfzb = df_typ.columns
    zjm__rpx = numba.typeof(wbxy__wfzb)
    nlz__vqqp = context.get_constant_generic(builder, zjm__rpx, wbxy__wfzb)
    bqhh__tyunm = pyapi.from_native_value(zjm__rpx, nlz__vqqp, c.env_manager)
    return bqhh__tyunm


def _create_initial_df_object(builder, context, pyapi, c, df_typ, obj,
    dataframe_payload, res, use_parent_obj):
    with c.builder.if_else(use_parent_obj) as (jdlk__zfsw, jzvu__ies):
        with jdlk__zfsw:
            pyapi.incref(obj)
            eqtx__gmyqv = context.insert_const_string(c.builder.module, 'numpy'
                )
            vtkr__rkwfr = pyapi.import_module_noblock(eqtx__gmyqv)
            if df_typ.has_runtime_cols:
                yth__xmejy = 0
            else:
                yth__xmejy = len(df_typ.columns)
            ajrc__ofs = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), yth__xmejy))
            bdsef__hsnlx = pyapi.call_method(vtkr__rkwfr, 'arange', (
                ajrc__ofs,))
            pyapi.object_setattr_string(obj, 'columns', bdsef__hsnlx)
            pyapi.decref(vtkr__rkwfr)
            pyapi.decref(bdsef__hsnlx)
            pyapi.decref(ajrc__ofs)
        with jzvu__ies:
            context.nrt.incref(builder, df_typ.index, dataframe_payload.index)
            eyi__mjyjd = c.pyapi.from_native_value(df_typ.index,
                dataframe_payload.index, c.env_manager)
            eqtx__gmyqv = context.insert_const_string(c.builder.module,
                'pandas')
            vtkr__rkwfr = pyapi.import_module_noblock(eqtx__gmyqv)
            df_obj = pyapi.call_method(vtkr__rkwfr, 'DataFrame', (pyapi.
                borrow_none(), eyi__mjyjd))
            pyapi.decref(vtkr__rkwfr)
            pyapi.decref(eyi__mjyjd)
            builder.store(df_obj, res)


@box(DataFrameType)
def box_dataframe(typ, val, c):
    from bodo.hiframes.table import box_table
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    dataframe_payload = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
        .context, c.builder, typ, val)
    uglf__hkdn = cgutils.create_struct_proxy(typ)(context, builder, value=val)
    n_cols = len(typ.columns) if not typ.has_runtime_cols else None
    obj = uglf__hkdn.parent
    res = cgutils.alloca_once_value(builder, obj)
    use_parent_obj = _get_use_df_parent_obj_flag(builder, context, pyapi,
        obj, n_cols)
    _create_initial_df_object(builder, context, pyapi, c, typ, obj,
        dataframe_payload, res, use_parent_obj)
    if typ.is_table_format:
        atcq__jmvil = typ.table_type
        hfehy__kujt = builder.extract_value(dataframe_payload.data, 0)
        context.nrt.incref(builder, atcq__jmvil, hfehy__kujt)
        vkz__qyfk = box_table(atcq__jmvil, hfehy__kujt, c, builder.not_(
            use_parent_obj))
        with builder.if_else(use_parent_obj) as (aay__adfxx, son__tvosh):
            with aay__adfxx:
                zsiym__ffrom = pyapi.object_getattr_string(vkz__qyfk, 'arrays')
                abta__rrjzy = c.pyapi.make_none()
                if n_cols is None:
                    onu__ilzpn = pyapi.call_method(zsiym__ffrom, '__len__', ())
                    lsea__ywe = pyapi.long_as_longlong(onu__ilzpn)
                    pyapi.decref(onu__ilzpn)
                else:
                    lsea__ywe = context.get_constant(types.int64, n_cols)
                with cgutils.for_range(builder, lsea__ywe) as jbe__hevoi:
                    i = jbe__hevoi.index
                    lruvt__vkwo = pyapi.list_getitem(zsiym__ffrom, i)
                    iuny__zoj = c.builder.icmp_unsigned('!=', lruvt__vkwo,
                        abta__rrjzy)
                    with builder.if_then(iuny__zoj):
                        zen__jvlu = pyapi.long_from_longlong(i)
                        df_obj = builder.load(res)
                        pyapi.object_setitem(df_obj, zen__jvlu, lruvt__vkwo)
                        pyapi.decref(zen__jvlu)
                pyapi.decref(zsiym__ffrom)
                pyapi.decref(abta__rrjzy)
            with son__tvosh:
                df_obj = builder.load(res)
                eyi__mjyjd = pyapi.object_getattr_string(df_obj, 'index')
                hzn__wzzm = c.pyapi.call_method(vkz__qyfk, 'to_pandas', (
                    eyi__mjyjd,))
                builder.store(hzn__wzzm, res)
                pyapi.decref(df_obj)
                pyapi.decref(eyi__mjyjd)
        pyapi.decref(vkz__qyfk)
    else:
        tllet__bhivb = [builder.extract_value(dataframe_payload.data, i) for
            i in range(n_cols)]
        hml__rsr = typ.data
        for i, xfu__rjads, bdo__ppxym in zip(range(n_cols), tllet__bhivb,
            hml__rsr):
            yeii__udoav = cgutils.alloca_once_value(builder, xfu__rjads)
            onlac__ibf = cgutils.alloca_once_value(builder, context.
                get_constant_null(bdo__ppxym))
            iuny__zoj = builder.not_(is_ll_eq(builder, yeii__udoav, onlac__ibf)
                )
            oca__nce = builder.or_(builder.not_(use_parent_obj), builder.
                and_(use_parent_obj, iuny__zoj))
            with builder.if_then(oca__nce):
                zen__jvlu = pyapi.long_from_longlong(context.get_constant(
                    types.int64, i))
                context.nrt.incref(builder, bdo__ppxym, xfu__rjads)
                arr_obj = pyapi.from_native_value(bdo__ppxym, xfu__rjads, c
                    .env_manager)
                df_obj = builder.load(res)
                pyapi.object_setitem(df_obj, zen__jvlu, arr_obj)
                pyapi.decref(arr_obj)
                pyapi.decref(zen__jvlu)
    df_obj = builder.load(res)
    bqhh__tyunm = _get_df_columns_obj(c, builder, context, pyapi, typ,
        dataframe_payload)
    pyapi.object_setattr_string(df_obj, 'columns', bqhh__tyunm)
    pyapi.decref(bqhh__tyunm)
    _set_bodo_meta_dataframe(c, df_obj, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return df_obj


def get_df_obj_column_codegen(context, builder, pyapi, df_obj, col_ind,
    data_typ):
    abta__rrjzy = pyapi.borrow_none()
    gsw__fgdys = pyapi.unserialize(pyapi.serialize_object(slice))
    xigu__uzhd = pyapi.call_function_objargs(gsw__fgdys, [abta__rrjzy])
    mun__fqzt = pyapi.long_from_longlong(col_ind)
    tnkcs__vfk = pyapi.tuple_pack([xigu__uzhd, mun__fqzt])
    xvr__fuu = pyapi.object_getattr_string(df_obj, 'iloc')
    lwgkn__mcm = pyapi.object_getitem(xvr__fuu, tnkcs__vfk)
    if isinstance(data_typ, bodo.DatetimeArrayType):
        bboli__vvcs = pyapi.object_getattr_string(lwgkn__mcm, 'array')
    else:
        bboli__vvcs = pyapi.object_getattr_string(lwgkn__mcm, 'values')
    if isinstance(data_typ, types.Array):
        sqey__xwb = context.insert_const_string(builder.module, 'numpy')
        yuv__cdd = pyapi.import_module_noblock(sqey__xwb)
        arr_obj = pyapi.call_method(yuv__cdd, 'ascontiguousarray', (
            bboli__vvcs,))
        pyapi.decref(bboli__vvcs)
        pyapi.decref(yuv__cdd)
    else:
        arr_obj = bboli__vvcs
    pyapi.decref(gsw__fgdys)
    pyapi.decref(xigu__uzhd)
    pyapi.decref(mun__fqzt)
    pyapi.decref(tnkcs__vfk)
    pyapi.decref(xvr__fuu)
    pyapi.decref(lwgkn__mcm)
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
        uglf__hkdn = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        arr_obj = get_df_obj_column_codegen(context, builder, pyapi,
            uglf__hkdn.parent, args[1], data_typ)
        qktm__cfs = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(arr_obj)
        dataframe_payload = (bodo.hiframes.pd_dataframe_ext.
            get_dataframe_payload(c.context, c.builder, df_typ, args[0]))
        if df_typ.is_table_format:
            hfehy__kujt = cgutils.create_struct_proxy(df_typ.table_type)(c.
                context, c.builder, builder.extract_value(dataframe_payload
                .data, 0))
            tnb__bpt = df_typ.table_type.type_to_blk[data_typ]
            fipj__fnq = getattr(hfehy__kujt, f'block_{tnb__bpt}')
            qnr__kplf = ListInstance(c.context, c.builder, types.List(
                data_typ), fipj__fnq)
            blsfd__qoqq = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[col_ind])
            qnr__kplf.inititem(blsfd__qoqq, qktm__cfs.value, incref=False)
        else:
            dataframe_payload.data = builder.insert_value(dataframe_payload
                .data, qktm__cfs.value, col_ind)
        iru__xklli = DataFramePayloadType(df_typ)
        gjoch__qarpx = context.nrt.meminfo_data(builder, uglf__hkdn.meminfo)
        isrn__xiy = context.get_value_type(iru__xklli).as_pointer()
        gjoch__qarpx = builder.bitcast(gjoch__qarpx, isrn__xiy)
        builder.store(dataframe_payload._getvalue(), gjoch__qarpx)
    return signature(types.none, df, i), codegen


@numba.njit
def unbox_col_if_needed(df, i):
    if bodo.hiframes.pd_dataframe_ext.has_parent(df
        ) and bodo.hiframes.pd_dataframe_ext._column_needs_unboxing(df, i):
        bodo.hiframes.boxing.unbox_dataframe_column(df, i)


@unbox(SeriesType)
def unbox_series(typ, val, c):
    if isinstance(typ.data, DatetimeArrayType):
        bboli__vvcs = c.pyapi.object_getattr_string(val, 'array')
    else:
        bboli__vvcs = c.pyapi.object_getattr_string(val, 'values')
    if isinstance(typ.data, types.Array):
        sqey__xwb = c.context.insert_const_string(c.builder.module, 'numpy')
        yuv__cdd = c.pyapi.import_module_noblock(sqey__xwb)
        arr_obj = c.pyapi.call_method(yuv__cdd, 'ascontiguousarray', (
            bboli__vvcs,))
        c.pyapi.decref(bboli__vvcs)
        c.pyapi.decref(yuv__cdd)
    else:
        arr_obj = bboli__vvcs
    ddtv__czfq = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    eyi__mjyjd = c.pyapi.object_getattr_string(val, 'index')
    aie__szl = c.pyapi.to_native_value(typ.index, eyi__mjyjd).value
    pkgf__jkr = c.pyapi.object_getattr_string(val, 'name')
    ctsd__smla = c.pyapi.to_native_value(typ.name_typ, pkgf__jkr).value
    pqn__bcddy = bodo.hiframes.pd_series_ext.construct_series(c.context, c.
        builder, typ, ddtv__czfq, aie__szl, ctsd__smla)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(eyi__mjyjd)
    c.pyapi.decref(pkgf__jkr)
    return NativeValue(pqn__bcddy)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        hwljz__mqe = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(hwljz__mqe._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    eqtx__gmyqv = c.context.insert_const_string(c.builder.module, 'pandas')
    qme__grl = c.pyapi.import_module_noblock(eqtx__gmyqv)
    tnw__veeo = bodo.hiframes.pd_series_ext.get_series_payload(c.context, c
        .builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, tnw__veeo.data)
    c.context.nrt.incref(c.builder, typ.index, tnw__veeo.index)
    c.context.nrt.incref(c.builder, typ.name_typ, tnw__veeo.name)
    arr_obj = c.pyapi.from_native_value(typ.data, tnw__veeo.data, c.env_manager
        )
    eyi__mjyjd = c.pyapi.from_native_value(typ.index, tnw__veeo.index, c.
        env_manager)
    pkgf__jkr = c.pyapi.from_native_value(typ.name_typ, tnw__veeo.name, c.
        env_manager)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        dtype = c.pyapi.unserialize(c.pyapi.serialize_object(object))
    else:
        dtype = c.pyapi.make_none()
    res = c.pyapi.call_method(qme__grl, 'Series', (arr_obj, eyi__mjyjd,
        dtype, pkgf__jkr))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(eyi__mjyjd)
    c.pyapi.decref(pkgf__jkr)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        c.pyapi.decref(dtype)
    _set_bodo_meta_series(res, c, typ)
    c.pyapi.decref(qme__grl)
    c.context.nrt.decref(c.builder, typ, val)
    return res


def type_enum_list_to_py_list_obj(pyapi, context, builder, env_manager,
    typ_list):
    vxlfc__mzg = []
    for xvo__ucfr in typ_list:
        if isinstance(xvo__ucfr, int) and not isinstance(xvo__ucfr, bool):
            bmwd__axfll = pyapi.long_from_longlong(lir.Constant(lir.IntType
                (64), xvo__ucfr))
        else:
            utv__epz = numba.typeof(xvo__ucfr)
            qleg__bklhd = context.get_constant_generic(builder, utv__epz,
                xvo__ucfr)
            bmwd__axfll = pyapi.from_native_value(utv__epz, qleg__bklhd,
                env_manager)
        vxlfc__mzg.append(bmwd__axfll)
    akc__odgo = pyapi.list_pack(vxlfc__mzg)
    for val in vxlfc__mzg:
        pyapi.decref(val)
    return akc__odgo


def _set_bodo_meta_dataframe(c, obj, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    gtnkd__vmd = not typ.has_runtime_cols
    nijgg__lbz = 2 if gtnkd__vmd else 1
    hcsgk__gpabw = pyapi.dict_new(nijgg__lbz)
    egr__nyl = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    pyapi.dict_setitem_string(hcsgk__gpabw, 'dist', egr__nyl)
    pyapi.decref(egr__nyl)
    if gtnkd__vmd:
        nxhi__gdbzh = _dtype_to_type_enum_list(typ.index)
        if nxhi__gdbzh != None:
            qxz__degm = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, nxhi__gdbzh)
        else:
            qxz__degm = pyapi.make_none()
        if typ.is_table_format:
            fbiq__mmd = typ.table_type
            hmdh__lwqhp = pyapi.list_new(lir.Constant(lir.IntType(64), len(
                typ.data)))
            for tnb__bpt, dtype in fbiq__mmd.blk_to_type.items():
                typ_list = _dtype_to_type_enum_list(dtype)
                if typ_list != None:
                    typ_list = type_enum_list_to_py_list_obj(pyapi, context,
                        builder, c.env_manager, typ_list)
                else:
                    typ_list = pyapi.make_none()
                lsea__ywe = c.context.get_constant(types.int64, len(
                    fbiq__mmd.block_to_arr_ind[tnb__bpt]))
                lujyj__vwans = c.context.make_constant_array(c.builder,
                    types.Array(types.int64, 1, 'C'), np.array(fbiq__mmd.
                    block_to_arr_ind[tnb__bpt], dtype=np.int64))
                hne__wpaem = c.context.make_array(types.Array(types.int64, 
                    1, 'C'))(c.context, c.builder, lujyj__vwans)
                with cgutils.for_range(c.builder, lsea__ywe) as jbe__hevoi:
                    i = jbe__hevoi.index
                    solul__lmdju = _getitem_array_single_int(c.context, c.
                        builder, types.int64, types.Array(types.int64, 1,
                        'C'), hne__wpaem, i)
                    c.context.nrt.incref(builder, types.pyobject, typ_list)
                    pyapi.list_setitem(hmdh__lwqhp, solul__lmdju, typ_list)
                c.context.nrt.decref(builder, types.pyobject, typ_list)
        else:
            dha__fhtqh = []
            for dtype in typ.data:
                typ_list = _dtype_to_type_enum_list(dtype)
                if typ_list != None:
                    akc__odgo = type_enum_list_to_py_list_obj(pyapi,
                        context, builder, c.env_manager, typ_list)
                else:
                    akc__odgo = pyapi.make_none()
                dha__fhtqh.append(akc__odgo)
            hmdh__lwqhp = pyapi.list_pack(dha__fhtqh)
            for val in dha__fhtqh:
                pyapi.decref(val)
        inepi__pfuc = pyapi.list_pack([qxz__degm, hmdh__lwqhp])
        pyapi.dict_setitem_string(hcsgk__gpabw, 'type_metadata', inepi__pfuc)
    pyapi.object_setattr_string(obj, '_bodo_meta', hcsgk__gpabw)
    pyapi.decref(hcsgk__gpabw)


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
    hcsgk__gpabw = pyapi.dict_new(2)
    egr__nyl = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    nxhi__gdbzh = _dtype_to_type_enum_list(typ.index)
    if nxhi__gdbzh != None:
        qxz__degm = type_enum_list_to_py_list_obj(pyapi, context, builder,
            c.env_manager, nxhi__gdbzh)
    else:
        qxz__degm = pyapi.make_none()
    dtype = get_series_dtype_handle_null_int_and_hetrogenous(typ)
    if dtype != None:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            ngm__melu = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            ngm__melu = pyapi.make_none()
    else:
        ngm__melu = pyapi.make_none()
    jfwc__ewvoe = pyapi.list_pack([qxz__degm, ngm__melu])
    pyapi.dict_setitem_string(hcsgk__gpabw, 'type_metadata', jfwc__ewvoe)
    pyapi.decref(jfwc__ewvoe)
    pyapi.dict_setitem_string(hcsgk__gpabw, 'dist', egr__nyl)
    pyapi.object_setattr_string(obj, '_bodo_meta', hcsgk__gpabw)
    pyapi.decref(hcsgk__gpabw)
    pyapi.decref(egr__nyl)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as nri__lcihe:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    xfih__eod = numba.np.numpy_support.map_layout(val)
    xtf__oti = not val.flags.writeable
    return types.Array(dtype, val.ndim, xfih__eod, readonly=xtf__oti)


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
    myf__ato = val[i]
    if isinstance(myf__ato, str):
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    elif isinstance(myf__ato, bytes):
        return binary_array_type
    elif isinstance(myf__ato, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(myf__ato, (int, np.int8, np.int16, np.int32, np.int64,
        np.uint8, np.uint16, np.uint32, np.uint64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(myf__ato))
    elif isinstance(myf__ato, (dict, Dict)) and all(isinstance(tzjd__ffvwc,
        str) for tzjd__ffvwc in myf__ato.keys()):
        vtpkk__mcs = tuple(myf__ato.keys())
        rhzwz__ocdtx = tuple(_get_struct_value_arr_type(v) for v in
            myf__ato.values())
        return StructArrayType(rhzwz__ocdtx, vtpkk__mcs)
    elif isinstance(myf__ato, (dict, Dict)):
        hecz__myxb = numba.typeof(_value_to_array(list(myf__ato.keys())))
        atpi__cnty = numba.typeof(_value_to_array(list(myf__ato.values())))
        hecz__myxb = to_str_arr_if_dict_array(hecz__myxb)
        atpi__cnty = to_str_arr_if_dict_array(atpi__cnty)
        return MapArrayType(hecz__myxb, atpi__cnty)
    elif isinstance(myf__ato, tuple):
        rhzwz__ocdtx = tuple(_get_struct_value_arr_type(v) for v in myf__ato)
        return TupleArrayType(rhzwz__ocdtx)
    if isinstance(myf__ato, (list, np.ndarray, pd.arrays.BooleanArray, pd.
        arrays.IntegerArray, pd.arrays.StringArray)):
        if isinstance(myf__ato, list):
            myf__ato = _value_to_array(myf__ato)
        aufry__ebd = numba.typeof(myf__ato)
        aufry__ebd = to_str_arr_if_dict_array(aufry__ebd)
        return ArrayItemArrayType(aufry__ebd)
    if isinstance(myf__ato, datetime.date):
        return datetime_date_array_type
    if isinstance(myf__ato, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(myf__ato, bodo.Time):
        return TimeArrayType(myf__ato.precision)
    if isinstance(myf__ato, decimal.Decimal):
        return DecimalArrayType(38, 18)
    if isinstance(myf__ato, pd._libs.interval.Interval):
        return bodo.libs.interval_arr_ext.IntervalArrayType
    raise BodoError(f'Unsupported object array with first value: {myf__ato}')


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    xgnp__agpq = val.copy()
    xgnp__agpq.append(None)
    xfu__rjads = np.array(xgnp__agpq, np.object_)
    if len(val) and isinstance(val[0], float):
        xfu__rjads = np.array(val, np.float64)
    return xfu__rjads


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
    bdo__ppxym = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        bdo__ppxym = to_nullable_type(bdo__ppxym)
    return bdo__ppxym
