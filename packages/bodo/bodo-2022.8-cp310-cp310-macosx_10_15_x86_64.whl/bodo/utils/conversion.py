"""
Utility functions for conversion of data such as list to array.
Need to be inlined for better optimization.
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.extending import overload
import bodo
from bodo.hiframes.time_ext import TimeArrayType, cast_time_to_int
from bodo.libs.binary_arr_ext import bytes_type
from bodo.libs.bool_arr_ext import boolean_dtype
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.nullable_tuple_ext import NullableTupleType
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, dtype_to_array_type, get_overload_const_list, get_overload_const_str, is_heterogeneous_tuple_type, is_np_arr_typ, is_overload_constant_list, is_overload_constant_str, is_overload_none, is_overload_true, is_str_arr_type, to_nullable_type, unwrap_typeref
NS_DTYPE = np.dtype('M8[ns]')
TD_DTYPE = np.dtype('m8[ns]')


def coerce_to_ndarray(data, error_on_nonarray=True, use_nullable_array=None,
    scalar_to_arr_len=None):
    return data


@overload(coerce_to_ndarray)
def overload_coerce_to_ndarray(data, error_on_nonarray=True,
    use_nullable_array=None, scalar_to_arr_len=None):
    from bodo.hiframes.pd_index_ext import DatetimeIndexType, NumericIndexType, RangeIndexType, TimedeltaIndexType
    from bodo.hiframes.pd_series_ext import SeriesType
    data = types.unliteral(data)
    if isinstance(data, types.Optional) and bodo.utils.typing.is_scalar_type(
        data.type):
        data = data.type
        use_nullable_array = True
    if isinstance(data, bodo.libs.int_arr_ext.IntegerArrayType
        ) and not is_overload_none(use_nullable_array):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.int_arr_ext.
            get_int_arr_data(data))
    if data == bodo.libs.bool_arr_ext.boolean_array and not is_overload_none(
        use_nullable_array):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.bool_arr_ext.
            get_bool_arr_data(data))
    if isinstance(data, types.Array):
        if not is_overload_none(use_nullable_array) and isinstance(data.
            dtype, (types.Boolean, types.Integer)):
            if data.dtype == types.bool_:
                if data.layout != 'C':
                    return (lambda data, error_on_nonarray=True,
                        use_nullable_array=None, scalar_to_arr_len=None:
                        bodo.libs.bool_arr_ext.init_bool_array(np.
                        ascontiguousarray(data), np.full(len(data) + 7 >> 3,
                        255, np.uint8)))
                else:
                    return (lambda data, error_on_nonarray=True,
                        use_nullable_array=None, scalar_to_arr_len=None:
                        bodo.libs.bool_arr_ext.init_bool_array(data, np.
                        full(len(data) + 7 >> 3, 255, np.uint8)))
            elif data.layout != 'C':
                return (lambda data, error_on_nonarray=True,
                    use_nullable_array=None, scalar_to_arr_len=None: bodo.
                    libs.int_arr_ext.init_integer_array(np.
                    ascontiguousarray(data), np.full(len(data) + 7 >> 3, 
                    255, np.uint8)))
            else:
                return (lambda data, error_on_nonarray=True,
                    use_nullable_array=None, scalar_to_arr_len=None: bodo.
                    libs.int_arr_ext.init_integer_array(data, np.full(len(
                    data) + 7 >> 3, 255, np.uint8)))
        if data.layout != 'C':
            return (lambda data, error_on_nonarray=True, use_nullable_array
                =None, scalar_to_arr_len=None: np.ascontiguousarray(data))
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: data)
    if isinstance(data, (types.List, types.UniTuple)):
        edhr__qgc = data.dtype
        if isinstance(edhr__qgc, types.Optional):
            edhr__qgc = edhr__qgc.type
            if bodo.utils.typing.is_scalar_type(edhr__qgc):
                use_nullable_array = True
        if isinstance(edhr__qgc, (types.Boolean, types.Integer, Decimal128Type)
            ) or edhr__qgc in [bodo.hiframes.pd_timestamp_ext.
            pd_timestamp_type, bodo.hiframes.datetime_date_ext.
            datetime_date_type, bodo.hiframes.datetime_timedelta_ext.
            datetime_timedelta_type]:
            rjr__qoh = dtype_to_array_type(edhr__qgc)
            if not is_overload_none(use_nullable_array):
                rjr__qoh = to_nullable_type(rjr__qoh)

            def impl(data, error_on_nonarray=True, use_nullable_array=None,
                scalar_to_arr_len=None):
                zqsg__tzzpc = len(data)
                A = bodo.utils.utils.alloc_type(zqsg__tzzpc, rjr__qoh, (-1,))
                bodo.utils.utils.tuple_list_to_array(A, data, edhr__qgc)
                return A
            return impl
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.asarray(data))
    if isinstance(data, SeriesType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_series_ext.
            get_series_data(data))
    if isinstance(data, (NumericIndexType, DatetimeIndexType,
        TimedeltaIndexType)):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_index_ext.
            get_index_data(data))
    if isinstance(data, RangeIndexType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.arange(data._start, data._stop,
            data._step))
    if isinstance(data, types.RangeType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.arange(data.start, data.stop,
            data.step))
    if not is_overload_none(scalar_to_arr_len):
        if isinstance(data, Decimal128Type):
            dtipw__zazz = data.precision
            bckhk__xzstb = data.scale

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                zqsg__tzzpc = scalar_to_arr_len
                A = bodo.libs.decimal_arr_ext.alloc_decimal_array(zqsg__tzzpc,
                    dtipw__zazz, bckhk__xzstb)
                for rgv__vuza in numba.parfors.parfor.internal_prange(
                    zqsg__tzzpc):
                    A[rgv__vuza] = data
                return A
            return impl_ts
        if data == bodo.hiframes.datetime_datetime_ext.datetime_datetime_type:
            jcgm__coe = np.dtype('datetime64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                zqsg__tzzpc = scalar_to_arr_len
                A = np.empty(zqsg__tzzpc, jcgm__coe)
                dpsih__ymrj = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(data))
                fdqwk__ldwou = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    dpsih__ymrj)
                for rgv__vuza in numba.parfors.parfor.internal_prange(
                    zqsg__tzzpc):
                    A[rgv__vuza] = fdqwk__ldwou
                return A
            return impl_ts
        if (data == bodo.hiframes.datetime_timedelta_ext.
            datetime_timedelta_type):
            vce__evxo = np.dtype('timedelta64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                zqsg__tzzpc = scalar_to_arr_len
                A = np.empty(zqsg__tzzpc, vce__evxo)
                iacm__kbyaa = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(data))
                for rgv__vuza in numba.parfors.parfor.internal_prange(
                    zqsg__tzzpc):
                    A[rgv__vuza] = iacm__kbyaa
                return A
            return impl_ts
        if data == bodo.hiframes.datetime_date_ext.datetime_date_type:

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                zqsg__tzzpc = scalar_to_arr_len
                A = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
                    zqsg__tzzpc)
                for rgv__vuza in numba.parfors.parfor.internal_prange(
                    zqsg__tzzpc):
                    A[rgv__vuza] = data
                return A
            return impl_ts
        if isinstance(data, bodo.hiframes.time_ext.TimeType):

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                zqsg__tzzpc = scalar_to_arr_len
                A = bodo.hiframes.time_ext.alloc_time_array(zqsg__tzzpc)
                for rgv__vuza in numba.parfors.parfor.internal_prange(
                    zqsg__tzzpc):
                    A[rgv__vuza] = data
                return A
            return impl_ts
        if data == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            jcgm__coe = np.dtype('datetime64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                zqsg__tzzpc = scalar_to_arr_len
                A = np.empty(scalar_to_arr_len, jcgm__coe)
                dpsih__ymrj = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    data.value)
                for rgv__vuza in numba.parfors.parfor.internal_prange(
                    zqsg__tzzpc):
                    A[rgv__vuza] = dpsih__ymrj
                return A
            return impl_ts
        dtype = types.unliteral(data)
        if not is_overload_none(use_nullable_array) and isinstance(dtype,
            types.Integer):

            def impl_null_integer(data, error_on_nonarray=True,
                use_nullable_array=None, scalar_to_arr_len=None):
                numba.parfors.parfor.init_prange()
                zqsg__tzzpc = scalar_to_arr_len
                mukf__hgxw = bodo.libs.int_arr_ext.alloc_int_array(zqsg__tzzpc,
                    dtype)
                for rgv__vuza in numba.parfors.parfor.internal_prange(
                    zqsg__tzzpc):
                    mukf__hgxw[rgv__vuza] = data
                return mukf__hgxw
            return impl_null_integer
        if not is_overload_none(use_nullable_array) and dtype == types.bool_:

            def impl_null_bool(data, error_on_nonarray=True,
                use_nullable_array=None, scalar_to_arr_len=None):
                numba.parfors.parfor.init_prange()
                zqsg__tzzpc = scalar_to_arr_len
                mukf__hgxw = bodo.libs.bool_arr_ext.alloc_bool_array(
                    zqsg__tzzpc)
                for rgv__vuza in numba.parfors.parfor.internal_prange(
                    zqsg__tzzpc):
                    mukf__hgxw[rgv__vuza] = data
                return mukf__hgxw
            return impl_null_bool

        def impl_num(data, error_on_nonarray=True, use_nullable_array=None,
            scalar_to_arr_len=None):
            numba.parfors.parfor.init_prange()
            zqsg__tzzpc = scalar_to_arr_len
            mukf__hgxw = np.empty(zqsg__tzzpc, dtype)
            for rgv__vuza in numba.parfors.parfor.internal_prange(zqsg__tzzpc):
                mukf__hgxw[rgv__vuza] = data
            return mukf__hgxw
        return impl_num
    if isinstance(data, types.BaseTuple) and all(isinstance(ixzc__rbuf, (
        types.Float, types.Integer)) for ixzc__rbuf in data.types):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.array(data))
    if bodo.utils.utils.is_array_typ(data, False):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: data)
    if is_overload_true(error_on_nonarray):
        raise BodoError(f'cannot coerce {data} to array')
    return (lambda data, error_on_nonarray=True, use_nullable_array=None,
        scalar_to_arr_len=None: data)


def coerce_scalar_to_array(scalar, length, arr_type):
    pass


@overload(coerce_scalar_to_array)
def overload_coerce_scalar_to_array(scalar, length, arr_type):
    nhtpo__ajalx = to_nullable_type(unwrap_typeref(arr_type))
    if scalar == types.none:

        def impl(scalar, length, arr_type):
            return bodo.libs.array_kernels.gen_na_array(length,
                nhtpo__ajalx, True)
    elif isinstance(scalar, types.Optional):

        def impl(scalar, length, arr_type):
            if scalar is None:
                return bodo.libs.array_kernels.gen_na_array(length,
                    nhtpo__ajalx, True)
            else:
                return bodo.utils.conversion.coerce_to_array(bodo.utils.
                    indexing.unoptional(scalar), True, True, length)
    else:

        def impl(scalar, length, arr_type):
            return bodo.utils.conversion.coerce_to_array(scalar, True, None,
                length)
    return impl


def coerce_to_array(data, error_on_nonarray=True, use_nullable_array=None,
    scalar_to_arr_len=None):
    return data


@overload(coerce_to_array, no_unliteral=True)
def overload_coerce_to_array(data, error_on_nonarray=True,
    use_nullable_array=None, scalar_to_arr_len=None):
    from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, StringIndexType
    from bodo.hiframes.pd_series_ext import SeriesType
    data = types.unliteral(data)
    if isinstance(data, types.Optional) and bodo.utils.typing.is_scalar_type(
        data.type):
        data = data.type
        use_nullable_array = True
    if isinstance(data, SeriesType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_series_ext.
            get_series_data(data))
    if isinstance(data, (StringIndexType, BinaryIndexType,
        CategoricalIndexType)):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_index_ext.
            get_index_data(data))
    if isinstance(data, types.List) and data.dtype in (bodo.string_type,
        bodo.bytes_type):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.str_arr_ext.
            str_arr_from_sequence(data))
    if isinstance(data, types.BaseTuple) and data.count == 0:
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.str_arr_ext.
            empty_str_arr(data))
    if isinstance(data, types.UniTuple) and isinstance(data.dtype, (types.
        UnicodeType, types.StringLiteral)) or isinstance(data, types.BaseTuple
        ) and all(isinstance(ixzc__rbuf, types.StringLiteral) for
        ixzc__rbuf in data.types):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.str_arr_ext.
            str_arr_from_sequence(data))
    if data in (bodo.string_array_type, bodo.dict_str_arr_type, bodo.
        binary_array_type, bodo.libs.bool_arr_ext.boolean_array, bodo.
        hiframes.datetime_date_ext.datetime_date_array_type, bodo.hiframes.
        datetime_timedelta_ext.datetime_timedelta_array_type, bodo.hiframes
        .split_impl.string_array_split_view_type) or isinstance(data, (bodo
        .libs.int_arr_ext.IntegerArrayType, DecimalArrayType, bodo.libs.
        interval_arr_ext.IntervalArrayType, bodo.libs.tuple_arr_ext.
        TupleArrayType, bodo.libs.struct_arr_ext.StructArrayType, bodo.
        hiframes.pd_categorical_ext.CategoricalArrayType, bodo.libs.
        csr_matrix_ext.CSRMatrixType, bodo.DatetimeArrayType, TimeArrayType)):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: data)
    if isinstance(data, (types.List, types.UniTuple)) and isinstance(data.
        dtype, types.BaseTuple):
        ent__vyj = tuple(dtype_to_array_type(ixzc__rbuf) for ixzc__rbuf in
            data.dtype.types)

        def impl_tuple_list(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            zqsg__tzzpc = len(data)
            arr = bodo.libs.tuple_arr_ext.pre_alloc_tuple_array(zqsg__tzzpc,
                (-1,), ent__vyj)
            for rgv__vuza in range(zqsg__tzzpc):
                arr[rgv__vuza] = data[rgv__vuza]
            return arr
        return impl_tuple_list
    if isinstance(data, types.List) and (bodo.utils.utils.is_array_typ(data
        .dtype, False) or isinstance(data.dtype, types.List)):
        smzj__pcth = dtype_to_array_type(data.dtype.dtype)

        def impl_array_item_arr(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            zqsg__tzzpc = len(data)
            ywmoa__poj = init_nested_counts(smzj__pcth)
            for rgv__vuza in range(zqsg__tzzpc):
                cuj__pqxw = bodo.utils.conversion.coerce_to_array(data[
                    rgv__vuza], use_nullable_array=True)
                ywmoa__poj = add_nested_counts(ywmoa__poj, cuj__pqxw)
            mukf__hgxw = (bodo.libs.array_item_arr_ext.
                pre_alloc_array_item_array(zqsg__tzzpc, ywmoa__poj, smzj__pcth)
                )
            vgtr__ghhpg = bodo.libs.array_item_arr_ext.get_null_bitmap(
                mukf__hgxw)
            for shqv__pwwy in range(zqsg__tzzpc):
                cuj__pqxw = bodo.utils.conversion.coerce_to_array(data[
                    shqv__pwwy], use_nullable_array=True)
                mukf__hgxw[shqv__pwwy] = cuj__pqxw
                bodo.libs.int_arr_ext.set_bit_to_arr(vgtr__ghhpg, shqv__pwwy, 1
                    )
            return mukf__hgxw
        return impl_array_item_arr
    if not is_overload_none(scalar_to_arr_len) and isinstance(data, (types.
        UnicodeType, types.StringLiteral)):

        def impl_str(data, error_on_nonarray=True, use_nullable_array=None,
            scalar_to_arr_len=None):
            zqsg__tzzpc = scalar_to_arr_len
            ohkn__gix = bodo.libs.str_arr_ext.str_arr_from_sequence([data])
            zhda__xzgp = bodo.libs.int_arr_ext.alloc_int_array(zqsg__tzzpc,
                np.int32)
            numba.parfors.parfor.init_prange()
            for rgv__vuza in numba.parfors.parfor.internal_prange(zqsg__tzzpc):
                zhda__xzgp[rgv__vuza] = 0
            A = bodo.libs.dict_arr_ext.init_dict_arr(ohkn__gix, zhda__xzgp,
                True)
            return A
        return impl_str
    if isinstance(data, types.List) and isinstance(data.dtype, bodo.
        hiframes.pd_timestamp_ext.PandasTimestampType):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
            'coerce_to_array()')

        def impl_list_timestamp(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            zqsg__tzzpc = len(data)
            A = np.empty(zqsg__tzzpc, np.dtype('datetime64[ns]'))
            for rgv__vuza in range(zqsg__tzzpc):
                A[rgv__vuza] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    data[rgv__vuza].value)
            return A
        return impl_list_timestamp
    if isinstance(data, types.List) and data.dtype == bodo.pd_timedelta_type:

        def impl_list_timedelta(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            zqsg__tzzpc = len(data)
            A = np.empty(zqsg__tzzpc, np.dtype('timedelta64[ns]'))
            for rgv__vuza in range(zqsg__tzzpc):
                A[rgv__vuza
                    ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    data[rgv__vuza].value)
            return A
        return impl_list_timedelta
    if isinstance(data, bodo.hiframes.pd_timestamp_ext.PandasTimestampType):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
            'coerce_to_array()')
    if not is_overload_none(scalar_to_arr_len) and data in [bodo.
        pd_timestamp_type, bodo.pd_timedelta_type]:
        jbcvi__xgao = ('datetime64[ns]' if data == bodo.pd_timestamp_type else
            'timedelta64[ns]')

        def impl_timestamp(data, error_on_nonarray=True, use_nullable_array
            =None, scalar_to_arr_len=None):
            zqsg__tzzpc = scalar_to_arr_len
            A = np.empty(zqsg__tzzpc, jbcvi__xgao)
            data = bodo.utils.conversion.unbox_if_timestamp(data)
            for rgv__vuza in numba.parfors.parfor.internal_prange(zqsg__tzzpc):
                A[rgv__vuza] = data
            return A
        return impl_timestamp
    return (lambda data, error_on_nonarray=True, use_nullable_array=None,
        scalar_to_arr_len=None: bodo.utils.conversion.coerce_to_ndarray(
        data, error_on_nonarray, use_nullable_array, scalar_to_arr_len))


def _is_str_dtype(dtype):
    return isinstance(dtype, bodo.libs.str_arr_ext.StringDtype) or isinstance(
        dtype, types.Function) and dtype.key[0
        ] == str or is_overload_constant_str(dtype) and get_overload_const_str(
        dtype) == 'str' or isinstance(dtype, types.TypeRef
        ) and dtype.instance_type == types.unicode_type


def fix_arr_dtype(data, new_dtype, copy=None, nan_to_str=True, from_series=
    False):
    return data


@overload(fix_arr_dtype, no_unliteral=True)
def overload_fix_arr_dtype(data, new_dtype, copy=None, nan_to_str=True,
    from_series=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'fix_arr_dtype()')
    pjy__rnw = is_overload_true(copy)
    cwgu__xdfxn = is_overload_constant_str(new_dtype
        ) and get_overload_const_str(new_dtype) == 'object'
    if is_overload_none(new_dtype) or cwgu__xdfxn:
        if pjy__rnw:
            return (lambda data, new_dtype, copy=None, nan_to_str=True,
                from_series=False: data.copy())
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data)
    if isinstance(data, NullableTupleType):
        nb_dtype = bodo.utils.typing.parse_dtype(new_dtype)
        if isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype):
            nb_dtype = nb_dtype.dtype
        yjf__ccy = {types.unicode_type: '', boolean_dtype: False, types.
            bool_: False, types.int8: np.int8(0), types.int16: np.int16(0),
            types.int32: np.int32(0), types.int64: np.int64(0), types.uint8:
            np.uint8(0), types.uint16: np.uint16(0), types.uint32: np.
            uint32(0), types.uint64: np.uint64(0), types.float32: np.
            float32(0), types.float64: np.float64(0), bodo.datetime64ns: pd
            .Timestamp(0), bodo.timedelta64ns: pd.Timedelta(0)}
        odkef__aotvd = {types.unicode_type: str, types.bool_: bool,
            boolean_dtype: bool, types.int8: np.int8, types.int16: np.int16,
            types.int32: np.int32, types.int64: np.int64, types.uint8: np.
            uint8, types.uint16: np.uint16, types.uint32: np.uint32, types.
            uint64: np.uint64, types.float32: np.float32, types.float64: np
            .float64, bodo.datetime64ns: pd.to_datetime, bodo.timedelta64ns:
            pd.to_timedelta}
        qmra__cafmz = yjf__ccy.keys()
        frnwo__gykr = list(data._tuple_typ.types)
        if nb_dtype not in qmra__cafmz:
            raise BodoError(f'type conversion to {nb_dtype} types unsupported.'
                )
        for ngha__rcx in frnwo__gykr:
            if ngha__rcx == bodo.datetime64ns:
                if nb_dtype not in (types.unicode_type, types.int64, types.
                    uint64, bodo.datetime64ns):
                    raise BodoError(
                        f'invalid type conversion from {ngha__rcx} to {nb_dtype}.'
                        )
            elif ngha__rcx == bodo.timedelta64ns:
                if nb_dtype not in (types.unicode_type, types.int64, types.
                    uint64, bodo.timedelta64ns):
                    raise BodoError(
                        f'invalid type conversion from {ngha__rcx} to {nb_dtype}.'
                        )
        jck__vcz = (
            'def impl(data, new_dtype, copy=None, nan_to_str=True, from_series=False):\n'
            )
        jck__vcz += '  data_tup = data._data\n'
        jck__vcz += '  null_tup = data._null_values\n'
        for rgv__vuza in range(len(frnwo__gykr)):
            jck__vcz += f'  val_{rgv__vuza} = convert_func(default_value)\n'
            jck__vcz += f'  if not null_tup[{rgv__vuza}]:\n'
            jck__vcz += (
                f'    val_{rgv__vuza} = convert_func(data_tup[{rgv__vuza}])\n')
        nveu__huym = ', '.join(f'val_{rgv__vuza}' for rgv__vuza in range(
            len(frnwo__gykr)))
        jck__vcz += f'  vals_tup = ({nveu__huym},)\n'
        jck__vcz += """  res_tup = bodo.libs.nullable_tuple_ext.build_nullable_tuple(vals_tup, null_tup)
"""
        jck__vcz += '  return res_tup\n'
        uaqj__iospw = {}
        wsacl__gmzrc = odkef__aotvd[nb_dtype]
        dpwah__oyxjz = yjf__ccy[nb_dtype]
        exec(jck__vcz, {'bodo': bodo, 'np': np, 'pd': pd, 'default_value':
            dpwah__oyxjz, 'convert_func': wsacl__gmzrc}, uaqj__iospw)
        impl = uaqj__iospw['impl']
        return impl
    if _is_str_dtype(new_dtype):
        if isinstance(data.dtype, types.Integer):

            def impl_int_str(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                zqsg__tzzpc = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(zqsg__tzzpc,
                    -1)
                for icw__qagns in numba.parfors.parfor.internal_prange(
                    zqsg__tzzpc):
                    if bodo.libs.array_kernels.isna(data, icw__qagns):
                        if nan_to_str:
                            bodo.libs.str_arr_ext.str_arr_setitem_NA_str(A,
                                icw__qagns)
                        else:
                            bodo.libs.array_kernels.setna(A, icw__qagns)
                    else:
                        bodo.libs.str_arr_ext.str_arr_setitem_int_to_str(A,
                            icw__qagns, data[icw__qagns])
                return A
            return impl_int_str
        if data.dtype == bytes_type:

            def impl_binary(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                zqsg__tzzpc = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(zqsg__tzzpc,
                    -1)
                for icw__qagns in numba.parfors.parfor.internal_prange(
                    zqsg__tzzpc):
                    if bodo.libs.array_kernels.isna(data, icw__qagns):
                        bodo.libs.array_kernels.setna(A, icw__qagns)
                    else:
                        A[icw__qagns] = ''.join([chr(onej__rqtw) for
                            onej__rqtw in data[icw__qagns]])
                return A
            return impl_binary
        if is_overload_true(from_series) and data.dtype in (bodo.
            datetime64ns, bodo.timedelta64ns):

            def impl_str_dt_series(data, new_dtype, copy=None, nan_to_str=
                True, from_series=False):
                numba.parfors.parfor.init_prange()
                zqsg__tzzpc = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(zqsg__tzzpc,
                    -1)
                for icw__qagns in numba.parfors.parfor.internal_prange(
                    zqsg__tzzpc):
                    if bodo.libs.array_kernels.isna(data, icw__qagns):
                        if nan_to_str:
                            A[icw__qagns] = 'NaT'
                        else:
                            bodo.libs.array_kernels.setna(A, icw__qagns)
                        continue
                    A[icw__qagns] = str(box_if_dt64(data[icw__qagns]))
                return A
            return impl_str_dt_series
        else:

            def impl_str_array(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                zqsg__tzzpc = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(zqsg__tzzpc,
                    -1)
                for icw__qagns in numba.parfors.parfor.internal_prange(
                    zqsg__tzzpc):
                    if bodo.libs.array_kernels.isna(data, icw__qagns):
                        if nan_to_str:
                            A[icw__qagns] = 'nan'
                        else:
                            bodo.libs.array_kernels.setna(A, icw__qagns)
                        continue
                    A[icw__qagns] = str(data[icw__qagns])
                return A
            return impl_str_array
    if isinstance(new_dtype, bodo.hiframes.pd_categorical_ext.
        PDCategoricalDtype):

        def impl_cat_dtype(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            zqsg__tzzpc = len(data)
            numba.parfors.parfor.init_prange()
            bbne__jdsf = (bodo.hiframes.pd_categorical_ext.
                get_label_dict_from_categories(new_dtype.categories.values))
            A = bodo.hiframes.pd_categorical_ext.alloc_categorical_array(
                zqsg__tzzpc, new_dtype)
            boh__xsqpg = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A))
            for rgv__vuza in numba.parfors.parfor.internal_prange(zqsg__tzzpc):
                if bodo.libs.array_kernels.isna(data, rgv__vuza):
                    bodo.libs.array_kernels.setna(A, rgv__vuza)
                    continue
                val = data[rgv__vuza]
                if val not in bbne__jdsf:
                    bodo.libs.array_kernels.setna(A, rgv__vuza)
                    continue
                boh__xsqpg[rgv__vuza] = bbne__jdsf[val]
            return A
        return impl_cat_dtype
    if is_overload_constant_str(new_dtype) and get_overload_const_str(new_dtype
        ) == 'category':

        def impl_category(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            aobhz__yoiy = bodo.libs.array_kernels.unique(data, dropna=True)
            aobhz__yoiy = pd.Series(aobhz__yoiy).sort_values().values
            aobhz__yoiy = bodo.allgatherv(aobhz__yoiy, False)
            agck__pgayh = bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo
                .utils.conversion.index_from_array(aobhz__yoiy, None), 
                False, None, None)
            zqsg__tzzpc = len(data)
            numba.parfors.parfor.init_prange()
            bbne__jdsf = (bodo.hiframes.pd_categorical_ext.
                get_label_dict_from_categories_no_duplicates(aobhz__yoiy))
            A = bodo.hiframes.pd_categorical_ext.alloc_categorical_array(
                zqsg__tzzpc, agck__pgayh)
            boh__xsqpg = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A))
            for rgv__vuza in numba.parfors.parfor.internal_prange(zqsg__tzzpc):
                if bodo.libs.array_kernels.isna(data, rgv__vuza):
                    bodo.libs.array_kernels.setna(A, rgv__vuza)
                    continue
                val = data[rgv__vuza]
                boh__xsqpg[rgv__vuza] = bbne__jdsf[val]
            return A
        return impl_category
    nb_dtype = bodo.utils.typing.parse_dtype(new_dtype)
    if isinstance(data, bodo.libs.int_arr_ext.IntegerArrayType):
        aurtk__fdca = isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype
            ) and data.dtype == nb_dtype.dtype
    else:
        aurtk__fdca = data.dtype == nb_dtype
    if pjy__rnw and aurtk__fdca:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data.copy())
    if aurtk__fdca:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data)
    if isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype):
        if isinstance(nb_dtype, types.Integer):
            jbcvi__xgao = nb_dtype
        else:
            jbcvi__xgao = nb_dtype.dtype
        if isinstance(data.dtype, types.Float):

            def impl_float(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                zqsg__tzzpc = len(data)
                numba.parfors.parfor.init_prange()
                rdjjq__oiedx = bodo.libs.int_arr_ext.alloc_int_array(
                    zqsg__tzzpc, jbcvi__xgao)
                for rgv__vuza in numba.parfors.parfor.internal_prange(
                    zqsg__tzzpc):
                    if bodo.libs.array_kernels.isna(data, rgv__vuza):
                        bodo.libs.array_kernels.setna(rdjjq__oiedx, rgv__vuza)
                    else:
                        rdjjq__oiedx[rgv__vuza] = int(data[rgv__vuza])
                return rdjjq__oiedx
            return impl_float
        else:
            if data == bodo.dict_str_arr_type:

                def impl_dict(data, new_dtype, copy=None, nan_to_str=True,
                    from_series=False):
                    return bodo.libs.dict_arr_ext.convert_dict_arr_to_int(data,
                        jbcvi__xgao)
                return impl_dict
            if isinstance(data, bodo.hiframes.time_ext.TimeArrayType):

                def impl(data, new_dtype, copy=None, nan_to_str=True,
                    from_series=False):
                    zqsg__tzzpc = len(data)
                    numba.parfors.parfor.init_prange()
                    rdjjq__oiedx = bodo.libs.int_arr_ext.alloc_int_array(
                        zqsg__tzzpc, jbcvi__xgao)
                    for rgv__vuza in numba.parfors.parfor.internal_prange(
                        zqsg__tzzpc):
                        if bodo.libs.array_kernels.isna(data, rgv__vuza):
                            bodo.libs.array_kernels.setna(rdjjq__oiedx,
                                rgv__vuza)
                        else:
                            rdjjq__oiedx[rgv__vuza] = cast_time_to_int(data
                                [rgv__vuza])
                    return rdjjq__oiedx
                return impl

            def impl(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                zqsg__tzzpc = len(data)
                numba.parfors.parfor.init_prange()
                rdjjq__oiedx = bodo.libs.int_arr_ext.alloc_int_array(
                    zqsg__tzzpc, jbcvi__xgao)
                for rgv__vuza in numba.parfors.parfor.internal_prange(
                    zqsg__tzzpc):
                    if bodo.libs.array_kernels.isna(data, rgv__vuza):
                        bodo.libs.array_kernels.setna(rdjjq__oiedx, rgv__vuza)
                    else:
                        rdjjq__oiedx[rgv__vuza] = np.int64(data[rgv__vuza])
                return rdjjq__oiedx
            return impl
    if isinstance(nb_dtype, types.Integer) and isinstance(data.dtype, types
        .Integer):

        def impl(data, new_dtype, copy=None, nan_to_str=True, from_series=False
            ):
            return data.astype(nb_dtype)
        return impl
    if nb_dtype == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            zqsg__tzzpc = len(data)
            numba.parfors.parfor.init_prange()
            rdjjq__oiedx = bodo.libs.bool_arr_ext.alloc_bool_array(zqsg__tzzpc)
            for rgv__vuza in numba.parfors.parfor.internal_prange(zqsg__tzzpc):
                if bodo.libs.array_kernels.isna(data, rgv__vuza):
                    bodo.libs.array_kernels.setna(rdjjq__oiedx, rgv__vuza)
                else:
                    rdjjq__oiedx[rgv__vuza] = bool(data[rgv__vuza])
            return rdjjq__oiedx
        return impl_bool
    if nb_dtype == bodo.datetime_date_type:
        if data.dtype == bodo.datetime64ns:

            def impl_date(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                zqsg__tzzpc = len(data)
                mukf__hgxw = (bodo.hiframes.datetime_date_ext.
                    alloc_datetime_date_array(zqsg__tzzpc))
                for rgv__vuza in numba.parfors.parfor.internal_prange(
                    zqsg__tzzpc):
                    if bodo.libs.array_kernels.isna(data, rgv__vuza):
                        bodo.libs.array_kernels.setna(mukf__hgxw, rgv__vuza)
                    else:
                        mukf__hgxw[rgv__vuza
                            ] = bodo.utils.conversion.box_if_dt64(data[
                            rgv__vuza]).date()
                return mukf__hgxw
            return impl_date
    if nb_dtype == bodo.datetime64ns:
        if data.dtype == bodo.string_type:

            def impl_str(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                return bodo.hiframes.pd_timestamp_ext.series_str_dt64_astype(
                    data)
            return impl_str
        if data == bodo.datetime_date_array_type:

            def impl_date(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                return (bodo.hiframes.pd_timestamp_ext.
                    datetime_date_arr_to_dt64_arr(data))
            return impl_date
        if isinstance(data.dtype, types.Number) or data.dtype in [bodo.
            timedelta64ns, types.bool_]:

            def impl_numeric(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                zqsg__tzzpc = len(data)
                numba.parfors.parfor.init_prange()
                mukf__hgxw = np.empty(zqsg__tzzpc, dtype=np.dtype(
                    'datetime64[ns]'))
                for rgv__vuza in numba.parfors.parfor.internal_prange(
                    zqsg__tzzpc):
                    if bodo.libs.array_kernels.isna(data, rgv__vuza):
                        bodo.libs.array_kernels.setna(mukf__hgxw, rgv__vuza)
                    else:
                        mukf__hgxw[rgv__vuza
                            ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                            np.int64(data[rgv__vuza]))
                return mukf__hgxw
            return impl_numeric
    if nb_dtype == bodo.timedelta64ns:
        if data.dtype == bodo.string_type:

            def impl_str(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                return bodo.hiframes.pd_timestamp_ext.series_str_td64_astype(
                    data)
            return impl_str
        if isinstance(data.dtype, types.Number) or data.dtype in [bodo.
            datetime64ns, types.bool_]:
            if pjy__rnw:

                def impl_numeric(data, new_dtype, copy=None, nan_to_str=
                    True, from_series=False):
                    zqsg__tzzpc = len(data)
                    numba.parfors.parfor.init_prange()
                    mukf__hgxw = np.empty(zqsg__tzzpc, dtype=np.dtype(
                        'timedelta64[ns]'))
                    for rgv__vuza in numba.parfors.parfor.internal_prange(
                        zqsg__tzzpc):
                        if bodo.libs.array_kernels.isna(data, rgv__vuza):
                            bodo.libs.array_kernels.setna(mukf__hgxw, rgv__vuza
                                )
                        else:
                            mukf__hgxw[rgv__vuza] = (bodo.hiframes.
                                pd_timestamp_ext.integer_to_timedelta64(np.
                                int64(data[rgv__vuza])))
                    return mukf__hgxw
                return impl_numeric
            else:
                return (lambda data, new_dtype, copy=None, nan_to_str=True,
                    from_series=False: data.view('int64'))
    if nb_dtype == types.int64 and data.dtype in [bodo.datetime64ns, bodo.
        timedelta64ns]:

        def impl_datelike_to_integer(data, new_dtype, copy=None, nan_to_str
            =True, from_series=False):
            zqsg__tzzpc = len(data)
            numba.parfors.parfor.init_prange()
            A = np.empty(zqsg__tzzpc, types.int64)
            for rgv__vuza in numba.parfors.parfor.internal_prange(zqsg__tzzpc):
                if bodo.libs.array_kernels.isna(data, rgv__vuza):
                    bodo.libs.array_kernels.setna(A, rgv__vuza)
                else:
                    A[rgv__vuza] = np.int64(data[rgv__vuza])
            return A
        return impl_datelike_to_integer
    if data.dtype != nb_dtype:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data.astype(nb_dtype))
    raise BodoError(f'Conversion from {data} to {new_dtype} not supported yet')


def array_type_from_dtype(dtype):
    return dtype_to_array_type(bodo.utils.typing.parse_dtype(dtype))


@overload(array_type_from_dtype)
def overload_array_type_from_dtype(dtype):
    arr_type = dtype_to_array_type(bodo.utils.typing.parse_dtype(dtype))
    return lambda dtype: arr_type


@numba.jit
def flatten_array(A):
    prtj__npq = []
    zqsg__tzzpc = len(A)
    for rgv__vuza in range(zqsg__tzzpc):
        tad__wpbma = A[rgv__vuza]
        for mxxq__qae in tad__wpbma:
            prtj__npq.append(mxxq__qae)
    return bodo.utils.conversion.coerce_to_array(prtj__npq)


def parse_datetimes_from_strings(data):
    return data


@overload(parse_datetimes_from_strings, no_unliteral=True)
def overload_parse_datetimes_from_strings(data):
    assert is_str_arr_type(data
        ), 'parse_datetimes_from_strings: string array expected'

    def parse_impl(data):
        numba.parfors.parfor.init_prange()
        zqsg__tzzpc = len(data)
        ehzpl__gtdp = np.empty(zqsg__tzzpc, bodo.utils.conversion.NS_DTYPE)
        for rgv__vuza in numba.parfors.parfor.internal_prange(zqsg__tzzpc):
            ehzpl__gtdp[rgv__vuza
                ] = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(data[
                rgv__vuza])
        return ehzpl__gtdp
    return parse_impl


def convert_to_dt64ns(data):
    return data


@overload(convert_to_dt64ns, no_unliteral=True)
def overload_convert_to_dt64ns(data):
    if data == bodo.hiframes.datetime_date_ext.datetime_date_array_type:
        return (lambda data: bodo.hiframes.pd_timestamp_ext.
            datetime_date_arr_to_dt64_arr(data))
    if is_np_arr_typ(data, types.int64):
        return lambda data: data.view(bodo.utils.conversion.NS_DTYPE)
    if is_np_arr_typ(data, types.NPDatetime('ns')):
        return lambda data: data
    if is_str_arr_type(data):
        return lambda data: bodo.utils.conversion.parse_datetimes_from_strings(
            data)
    raise BodoError(f'invalid data type {data} for dt64 conversion')


def convert_to_td64ns(data):
    return data


@overload(convert_to_td64ns, no_unliteral=True)
def overload_convert_to_td64ns(data):
    if is_np_arr_typ(data, types.int64):
        return lambda data: data.view(bodo.utils.conversion.TD_DTYPE)
    if is_np_arr_typ(data, types.NPTimedelta('ns')):
        return lambda data: data
    if is_str_arr_type(data):
        raise BodoError('conversion to timedelta from string not supported yet'
            )
    raise BodoError(f'invalid data type {data} for timedelta64 conversion')


def convert_to_index(data, name=None):
    return data


@overload(convert_to_index, no_unliteral=True)
def overload_convert_to_index(data, name=None):
    from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, DatetimeIndexType, NumericIndexType, PeriodIndexType, RangeIndexType, StringIndexType, TimedeltaIndexType
    if isinstance(data, (RangeIndexType, NumericIndexType,
        DatetimeIndexType, TimedeltaIndexType, StringIndexType,
        BinaryIndexType, CategoricalIndexType, PeriodIndexType, types.NoneType)
        ):
        return lambda data, name=None: data

    def impl(data, name=None):
        bohp__biz = bodo.utils.conversion.coerce_to_array(data)
        return bodo.utils.conversion.index_from_array(bohp__biz, name)
    return impl


def force_convert_index(I1, I2):
    return I2


@overload(force_convert_index, no_unliteral=True)
def overload_force_convert_index(I1, I2):
    from bodo.hiframes.pd_index_ext import RangeIndexType
    if isinstance(I2, RangeIndexType):
        return lambda I1, I2: pd.RangeIndex(len(I1._data))
    return lambda I1, I2: I1


def index_from_array(data, name=None):
    return data


@overload(index_from_array, no_unliteral=True)
def overload_index_from_array(data, name=None):
    if data in [bodo.string_array_type, bodo.binary_array_type, bodo.
        dict_str_arr_type]:
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_binary_str_index(data, name))
    if (data == bodo.hiframes.datetime_date_ext.datetime_date_array_type or
        data.dtype == types.NPDatetime('ns')):
        return lambda data, name=None: pd.DatetimeIndex(data, name=name)
    if data.dtype == types.NPTimedelta('ns'):
        return lambda data, name=None: pd.TimedeltaIndex(data, name=name)
    if isinstance(data.dtype, (types.Integer, types.Float, types.Boolean)):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_numeric_index(data, name))
    if isinstance(data, bodo.libs.interval_arr_ext.IntervalArrayType):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_interval_index(data, name))
    if isinstance(data, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_categorical_index(data, name))
    if isinstance(data, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_datetime_index(data, name))
    raise BodoError(f'cannot convert {data} to Index')


def index_to_array(data):
    return data


@overload(index_to_array, no_unliteral=True)
def overload_index_to_array(I):
    from bodo.hiframes.pd_index_ext import RangeIndexType
    if isinstance(I, RangeIndexType):
        return lambda I: np.arange(I._start, I._stop, I._step)
    return lambda I: bodo.hiframes.pd_index_ext.get_index_data(I)


def false_if_none(val):
    return False if val is None else val


@overload(false_if_none, no_unliteral=True)
def overload_false_if_none(val):
    if is_overload_none(val):
        return lambda val: False
    return lambda val: val


def extract_name_if_none(data, name):
    return name


@overload(extract_name_if_none, no_unliteral=True)
def overload_extract_name_if_none(data, name):
    from bodo.hiframes.pd_index_ext import CategoricalIndexType, DatetimeIndexType, NumericIndexType, PeriodIndexType, TimedeltaIndexType
    from bodo.hiframes.pd_series_ext import SeriesType
    if not is_overload_none(name):
        return lambda data, name: name
    if isinstance(data, (NumericIndexType, DatetimeIndexType,
        TimedeltaIndexType, PeriodIndexType, CategoricalIndexType)):
        return lambda data, name: bodo.hiframes.pd_index_ext.get_index_name(
            data)
    if isinstance(data, SeriesType):
        return lambda data, name: bodo.hiframes.pd_series_ext.get_series_name(
            data)
    return lambda data, name: name


def extract_index_if_none(data, index):
    return index


@overload(extract_index_if_none, no_unliteral=True)
def overload_extract_index_if_none(data, index):
    from bodo.hiframes.pd_series_ext import SeriesType
    if not is_overload_none(index):
        return lambda data, index: index
    if isinstance(data, SeriesType):
        return (lambda data, index: bodo.hiframes.pd_series_ext.
            get_series_index(data))
    return lambda data, index: bodo.hiframes.pd_index_ext.init_range_index(
        0, len(data), 1, None)


def box_if_dt64(val):
    return val


@overload(box_if_dt64, no_unliteral=True)
def overload_box_if_dt64(val):
    if val == types.NPDatetime('ns'):
        return (lambda val: bodo.hiframes.pd_timestamp_ext.
            convert_datetime64_to_timestamp(val))
    if val == types.NPTimedelta('ns'):
        return (lambda val: bodo.hiframes.pd_timestamp_ext.
            convert_numpy_timedelta64_to_pd_timedelta(val))
    return lambda val: val


def unbox_if_timestamp(val):
    return val


@overload(unbox_if_timestamp, no_unliteral=True)
def overload_unbox_if_timestamp(val):
    if val == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        return lambda val: bodo.hiframes.pd_timestamp_ext.integer_to_dt64(val
            .value)
    if val == bodo.hiframes.datetime_datetime_ext.datetime_datetime_type:
        return lambda val: bodo.hiframes.pd_timestamp_ext.integer_to_dt64(pd
            .Timestamp(val).value)
    if val == bodo.hiframes.datetime_timedelta_ext.pd_timedelta_type:
        return (lambda val: bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(val.value))
    if val == types.Optional(bodo.hiframes.pd_timestamp_ext.pd_timestamp_type):

        def impl_optional(val):
            if val is None:
                puqr__egi = None
            else:
                puqr__egi = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(bodo
                    .utils.indexing.unoptional(val).value)
            return puqr__egi
        return impl_optional
    if val == types.Optional(bodo.hiframes.datetime_timedelta_ext.
        pd_timedelta_type):

        def impl_optional_td(val):
            if val is None:
                puqr__egi = None
            else:
                puqr__egi = (bodo.hiframes.pd_timestamp_ext.
                    integer_to_timedelta64(bodo.utils.indexing.unoptional(
                    val).value))
            return puqr__egi
        return impl_optional_td
    return lambda val: val


def to_tuple(val):
    return val


@overload(to_tuple, no_unliteral=True)
def overload_to_tuple(val):
    if not isinstance(val, types.BaseTuple) and is_overload_constant_list(val):
        ajcv__vjdpl = len(val.types if isinstance(val, types.LiteralList) else
            get_overload_const_list(val))
        jck__vcz = 'def f(val):\n'
        ipkyl__hktzx = ','.join(f'val[{rgv__vuza}]' for rgv__vuza in range(
            ajcv__vjdpl))
        jck__vcz += f'  return ({ipkyl__hktzx},)\n'
        uaqj__iospw = {}
        exec(jck__vcz, {}, uaqj__iospw)
        impl = uaqj__iospw['f']
        return impl
    assert isinstance(val, types.BaseTuple), 'tuple type expected'
    return lambda val: val


def get_array_if_series_or_index(data):
    return data


@overload(get_array_if_series_or_index)
def overload_get_array_if_series_or_index(data):
    from bodo.hiframes.pd_series_ext import SeriesType
    if isinstance(data, SeriesType):
        return lambda data: bodo.hiframes.pd_series_ext.get_series_data(data)
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        return lambda data: bodo.utils.conversion.coerce_to_array(data)
    if isinstance(data, bodo.hiframes.pd_index_ext.HeterogeneousIndexType):
        if not is_heterogeneous_tuple_type(data.data):

            def impl(data):
                eeewm__dabo = bodo.hiframes.pd_index_ext.get_index_data(data)
                return bodo.utils.conversion.coerce_to_array(eeewm__dabo)
            return impl

        def impl(data):
            return bodo.hiframes.pd_index_ext.get_index_data(data)
        return impl
    return lambda data: data


def extract_index_array(A):
    return np.arange(len(A))


@overload(extract_index_array, no_unliteral=True)
def overload_extract_index_array(A):
    from bodo.hiframes.pd_series_ext import SeriesType
    if isinstance(A, SeriesType):

        def impl(A):
            index = bodo.hiframes.pd_series_ext.get_series_index(A)
            smdz__tupl = bodo.utils.conversion.coerce_to_array(index)
            return smdz__tupl
        return impl
    return lambda A: np.arange(len(A))


def ensure_contig_if_np(arr):
    return np.ascontiguousarray(arr)


@overload(ensure_contig_if_np, no_unliteral=True)
def overload_ensure_contig_if_np(arr):
    if isinstance(arr, types.Array):
        return lambda arr: np.ascontiguousarray(arr)
    return lambda arr: arr


def struct_if_heter_dict(values, names):
    return {efthg__cdg: dpsih__ymrj for efthg__cdg, dpsih__ymrj in zip(
        names, values)}


@overload(struct_if_heter_dict, no_unliteral=True)
def overload_struct_if_heter_dict(values, names):
    if not types.is_homogeneous(*values.types):
        return lambda values, names: bodo.libs.struct_arr_ext.init_struct(
            values, names)
    vdbch__lkon = len(values.types)
    jck__vcz = 'def f(values, names):\n'
    ipkyl__hktzx = ','.join("'{}': values[{}]".format(
        get_overload_const_str(names.types[rgv__vuza]), rgv__vuza) for
        rgv__vuza in range(vdbch__lkon))
    jck__vcz += '  return {{{}}}\n'.format(ipkyl__hktzx)
    uaqj__iospw = {}
    exec(jck__vcz, {}, uaqj__iospw)
    impl = uaqj__iospw['f']
    return impl
