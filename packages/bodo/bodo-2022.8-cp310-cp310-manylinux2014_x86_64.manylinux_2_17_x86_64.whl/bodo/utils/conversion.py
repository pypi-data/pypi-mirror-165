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
        vlom__jhsqr = data.dtype
        if isinstance(vlom__jhsqr, types.Optional):
            vlom__jhsqr = vlom__jhsqr.type
            if bodo.utils.typing.is_scalar_type(vlom__jhsqr):
                use_nullable_array = True
        if isinstance(vlom__jhsqr, (types.Boolean, types.Integer,
            Decimal128Type)) or vlom__jhsqr in [bodo.hiframes.
            pd_timestamp_ext.pd_timestamp_type, bodo.hiframes.
            datetime_date_ext.datetime_date_type, bodo.hiframes.
            datetime_timedelta_ext.datetime_timedelta_type]:
            vjcm__fcpg = dtype_to_array_type(vlom__jhsqr)
            if not is_overload_none(use_nullable_array):
                vjcm__fcpg = to_nullable_type(vjcm__fcpg)

            def impl(data, error_on_nonarray=True, use_nullable_array=None,
                scalar_to_arr_len=None):
                zqkxe__yrro = len(data)
                A = bodo.utils.utils.alloc_type(zqkxe__yrro, vjcm__fcpg, (-1,))
                bodo.utils.utils.tuple_list_to_array(A, data, vlom__jhsqr)
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
            ojofa__owh = data.precision
            hdw__kqmec = data.scale

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                zqkxe__yrro = scalar_to_arr_len
                A = bodo.libs.decimal_arr_ext.alloc_decimal_array(zqkxe__yrro,
                    ojofa__owh, hdw__kqmec)
                for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                    zqkxe__yrro):
                    A[gwbat__vvnlf] = data
                return A
            return impl_ts
        if data == bodo.hiframes.datetime_datetime_ext.datetime_datetime_type:
            bnht__sywnz = np.dtype('datetime64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                zqkxe__yrro = scalar_to_arr_len
                A = np.empty(zqkxe__yrro, bnht__sywnz)
                cloje__ouv = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(data))
                aab__rcn = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    cloje__ouv)
                for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                    zqkxe__yrro):
                    A[gwbat__vvnlf] = aab__rcn
                return A
            return impl_ts
        if (data == bodo.hiframes.datetime_timedelta_ext.
            datetime_timedelta_type):
            tbd__onufc = np.dtype('timedelta64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                zqkxe__yrro = scalar_to_arr_len
                A = np.empty(zqkxe__yrro, tbd__onufc)
                xdv__gsbt = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(data))
                for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                    zqkxe__yrro):
                    A[gwbat__vvnlf] = xdv__gsbt
                return A
            return impl_ts
        if data == bodo.hiframes.datetime_date_ext.datetime_date_type:

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                zqkxe__yrro = scalar_to_arr_len
                A = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
                    zqkxe__yrro)
                for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                    zqkxe__yrro):
                    A[gwbat__vvnlf] = data
                return A
            return impl_ts
        if isinstance(data, bodo.hiframes.time_ext.TimeType):

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                zqkxe__yrro = scalar_to_arr_len
                A = bodo.hiframes.time_ext.alloc_time_array(zqkxe__yrro)
                for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                    zqkxe__yrro):
                    A[gwbat__vvnlf] = data
                return A
            return impl_ts
        if data == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            bnht__sywnz = np.dtype('datetime64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                zqkxe__yrro = scalar_to_arr_len
                A = np.empty(scalar_to_arr_len, bnht__sywnz)
                cloje__ouv = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    data.value)
                for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                    zqkxe__yrro):
                    A[gwbat__vvnlf] = cloje__ouv
                return A
            return impl_ts
        dtype = types.unliteral(data)
        if not is_overload_none(use_nullable_array) and isinstance(dtype,
            types.Integer):

            def impl_null_integer(data, error_on_nonarray=True,
                use_nullable_array=None, scalar_to_arr_len=None):
                numba.parfors.parfor.init_prange()
                zqkxe__yrro = scalar_to_arr_len
                uoyak__pszl = bodo.libs.int_arr_ext.alloc_int_array(zqkxe__yrro
                    , dtype)
                for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                    zqkxe__yrro):
                    uoyak__pszl[gwbat__vvnlf] = data
                return uoyak__pszl
            return impl_null_integer
        if not is_overload_none(use_nullable_array) and dtype == types.bool_:

            def impl_null_bool(data, error_on_nonarray=True,
                use_nullable_array=None, scalar_to_arr_len=None):
                numba.parfors.parfor.init_prange()
                zqkxe__yrro = scalar_to_arr_len
                uoyak__pszl = bodo.libs.bool_arr_ext.alloc_bool_array(
                    zqkxe__yrro)
                for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                    zqkxe__yrro):
                    uoyak__pszl[gwbat__vvnlf] = data
                return uoyak__pszl
            return impl_null_bool

        def impl_num(data, error_on_nonarray=True, use_nullable_array=None,
            scalar_to_arr_len=None):
            numba.parfors.parfor.init_prange()
            zqkxe__yrro = scalar_to_arr_len
            uoyak__pszl = np.empty(zqkxe__yrro, dtype)
            for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                zqkxe__yrro):
                uoyak__pszl[gwbat__vvnlf] = data
            return uoyak__pszl
        return impl_num
    if isinstance(data, types.BaseTuple) and all(isinstance(xal__lfj, (
        types.Float, types.Integer)) for xal__lfj in data.types):
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
    yyfuv__iaw = to_nullable_type(unwrap_typeref(arr_type))
    if scalar == types.none:

        def impl(scalar, length, arr_type):
            return bodo.libs.array_kernels.gen_na_array(length, yyfuv__iaw,
                True)
    elif isinstance(scalar, types.Optional):

        def impl(scalar, length, arr_type):
            if scalar is None:
                return bodo.libs.array_kernels.gen_na_array(length,
                    yyfuv__iaw, True)
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
        ) and all(isinstance(xal__lfj, types.StringLiteral) for xal__lfj in
        data.types):
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
        tieh__ddsg = tuple(dtype_to_array_type(xal__lfj) for xal__lfj in
            data.dtype.types)

        def impl_tuple_list(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            zqkxe__yrro = len(data)
            arr = bodo.libs.tuple_arr_ext.pre_alloc_tuple_array(zqkxe__yrro,
                (-1,), tieh__ddsg)
            for gwbat__vvnlf in range(zqkxe__yrro):
                arr[gwbat__vvnlf] = data[gwbat__vvnlf]
            return arr
        return impl_tuple_list
    if isinstance(data, types.List) and (bodo.utils.utils.is_array_typ(data
        .dtype, False) or isinstance(data.dtype, types.List)):
        qyjte__enec = dtype_to_array_type(data.dtype.dtype)

        def impl_array_item_arr(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            zqkxe__yrro = len(data)
            qreu__amzva = init_nested_counts(qyjte__enec)
            for gwbat__vvnlf in range(zqkxe__yrro):
                tglnf__fwpz = bodo.utils.conversion.coerce_to_array(data[
                    gwbat__vvnlf], use_nullable_array=True)
                qreu__amzva = add_nested_counts(qreu__amzva, tglnf__fwpz)
            uoyak__pszl = (bodo.libs.array_item_arr_ext.
                pre_alloc_array_item_array(zqkxe__yrro, qreu__amzva,
                qyjte__enec))
            age__med = bodo.libs.array_item_arr_ext.get_null_bitmap(uoyak__pszl
                )
            for jcuhs__ygysz in range(zqkxe__yrro):
                tglnf__fwpz = bodo.utils.conversion.coerce_to_array(data[
                    jcuhs__ygysz], use_nullable_array=True)
                uoyak__pszl[jcuhs__ygysz] = tglnf__fwpz
                bodo.libs.int_arr_ext.set_bit_to_arr(age__med, jcuhs__ygysz, 1)
            return uoyak__pszl
        return impl_array_item_arr
    if not is_overload_none(scalar_to_arr_len) and isinstance(data, (types.
        UnicodeType, types.StringLiteral)):

        def impl_str(data, error_on_nonarray=True, use_nullable_array=None,
            scalar_to_arr_len=None):
            zqkxe__yrro = scalar_to_arr_len
            ngy__dgsvi = bodo.libs.str_arr_ext.str_arr_from_sequence([data])
            romnu__aumcw = bodo.libs.int_arr_ext.alloc_int_array(zqkxe__yrro,
                np.int32)
            numba.parfors.parfor.init_prange()
            for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                zqkxe__yrro):
                romnu__aumcw[gwbat__vvnlf] = 0
            A = bodo.libs.dict_arr_ext.init_dict_arr(ngy__dgsvi,
                romnu__aumcw, True)
            return A
        return impl_str
    if isinstance(data, types.List) and isinstance(data.dtype, bodo.
        hiframes.pd_timestamp_ext.PandasTimestampType):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
            'coerce_to_array()')

        def impl_list_timestamp(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            zqkxe__yrro = len(data)
            A = np.empty(zqkxe__yrro, np.dtype('datetime64[ns]'))
            for gwbat__vvnlf in range(zqkxe__yrro):
                A[gwbat__vvnlf
                    ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(data
                    [gwbat__vvnlf].value)
            return A
        return impl_list_timestamp
    if isinstance(data, types.List) and data.dtype == bodo.pd_timedelta_type:

        def impl_list_timedelta(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            zqkxe__yrro = len(data)
            A = np.empty(zqkxe__yrro, np.dtype('timedelta64[ns]'))
            for gwbat__vvnlf in range(zqkxe__yrro):
                A[gwbat__vvnlf
                    ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    data[gwbat__vvnlf].value)
            return A
        return impl_list_timedelta
    if isinstance(data, bodo.hiframes.pd_timestamp_ext.PandasTimestampType):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
            'coerce_to_array()')
    if not is_overload_none(scalar_to_arr_len) and data in [bodo.
        pd_timestamp_type, bodo.pd_timedelta_type]:
        rsn__ods = ('datetime64[ns]' if data == bodo.pd_timestamp_type else
            'timedelta64[ns]')

        def impl_timestamp(data, error_on_nonarray=True, use_nullable_array
            =None, scalar_to_arr_len=None):
            zqkxe__yrro = scalar_to_arr_len
            A = np.empty(zqkxe__yrro, rsn__ods)
            data = bodo.utils.conversion.unbox_if_timestamp(data)
            for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                zqkxe__yrro):
                A[gwbat__vvnlf] = data
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
    wvn__ewt = is_overload_true(copy)
    kirtk__ollsy = is_overload_constant_str(new_dtype
        ) and get_overload_const_str(new_dtype) == 'object'
    if is_overload_none(new_dtype) or kirtk__ollsy:
        if wvn__ewt:
            return (lambda data, new_dtype, copy=None, nan_to_str=True,
                from_series=False: data.copy())
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data)
    if isinstance(data, NullableTupleType):
        nb_dtype = bodo.utils.typing.parse_dtype(new_dtype)
        if isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype):
            nb_dtype = nb_dtype.dtype
        ornt__cyb = {types.unicode_type: '', boolean_dtype: False, types.
            bool_: False, types.int8: np.int8(0), types.int16: np.int16(0),
            types.int32: np.int32(0), types.int64: np.int64(0), types.uint8:
            np.uint8(0), types.uint16: np.uint16(0), types.uint32: np.
            uint32(0), types.uint64: np.uint64(0), types.float32: np.
            float32(0), types.float64: np.float64(0), bodo.datetime64ns: pd
            .Timestamp(0), bodo.timedelta64ns: pd.Timedelta(0)}
        khexb__drlhc = {types.unicode_type: str, types.bool_: bool,
            boolean_dtype: bool, types.int8: np.int8, types.int16: np.int16,
            types.int32: np.int32, types.int64: np.int64, types.uint8: np.
            uint8, types.uint16: np.uint16, types.uint32: np.uint32, types.
            uint64: np.uint64, types.float32: np.float32, types.float64: np
            .float64, bodo.datetime64ns: pd.to_datetime, bodo.timedelta64ns:
            pd.to_timedelta}
        rsfo__wnllk = ornt__cyb.keys()
        ajjf__hdfn = list(data._tuple_typ.types)
        if nb_dtype not in rsfo__wnllk:
            raise BodoError(f'type conversion to {nb_dtype} types unsupported.'
                )
        for ispl__bfwj in ajjf__hdfn:
            if ispl__bfwj == bodo.datetime64ns:
                if nb_dtype not in (types.unicode_type, types.int64, types.
                    uint64, bodo.datetime64ns):
                    raise BodoError(
                        f'invalid type conversion from {ispl__bfwj} to {nb_dtype}.'
                        )
            elif ispl__bfwj == bodo.timedelta64ns:
                if nb_dtype not in (types.unicode_type, types.int64, types.
                    uint64, bodo.timedelta64ns):
                    raise BodoError(
                        f'invalid type conversion from {ispl__bfwj} to {nb_dtype}.'
                        )
        hivl__bmia = (
            'def impl(data, new_dtype, copy=None, nan_to_str=True, from_series=False):\n'
            )
        hivl__bmia += '  data_tup = data._data\n'
        hivl__bmia += '  null_tup = data._null_values\n'
        for gwbat__vvnlf in range(len(ajjf__hdfn)):
            hivl__bmia += (
                f'  val_{gwbat__vvnlf} = convert_func(default_value)\n')
            hivl__bmia += f'  if not null_tup[{gwbat__vvnlf}]:\n'
            hivl__bmia += (
                f'    val_{gwbat__vvnlf} = convert_func(data_tup[{gwbat__vvnlf}])\n'
                )
        qsdip__qmb = ', '.join(f'val_{gwbat__vvnlf}' for gwbat__vvnlf in
            range(len(ajjf__hdfn)))
        hivl__bmia += f'  vals_tup = ({qsdip__qmb},)\n'
        hivl__bmia += """  res_tup = bodo.libs.nullable_tuple_ext.build_nullable_tuple(vals_tup, null_tup)
"""
        hivl__bmia += '  return res_tup\n'
        lvlih__ltr = {}
        wzh__pklqx = khexb__drlhc[nb_dtype]
        ldrdm__xpmbd = ornt__cyb[nb_dtype]
        exec(hivl__bmia, {'bodo': bodo, 'np': np, 'pd': pd, 'default_value':
            ldrdm__xpmbd, 'convert_func': wzh__pklqx}, lvlih__ltr)
        impl = lvlih__ltr['impl']
        return impl
    if _is_str_dtype(new_dtype):
        if isinstance(data.dtype, types.Integer):

            def impl_int_str(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                zqkxe__yrro = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(zqkxe__yrro,
                    -1)
                for zby__thym in numba.parfors.parfor.internal_prange(
                    zqkxe__yrro):
                    if bodo.libs.array_kernels.isna(data, zby__thym):
                        if nan_to_str:
                            bodo.libs.str_arr_ext.str_arr_setitem_NA_str(A,
                                zby__thym)
                        else:
                            bodo.libs.array_kernels.setna(A, zby__thym)
                    else:
                        bodo.libs.str_arr_ext.str_arr_setitem_int_to_str(A,
                            zby__thym, data[zby__thym])
                return A
            return impl_int_str
        if data.dtype == bytes_type:

            def impl_binary(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                zqkxe__yrro = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(zqkxe__yrro,
                    -1)
                for zby__thym in numba.parfors.parfor.internal_prange(
                    zqkxe__yrro):
                    if bodo.libs.array_kernels.isna(data, zby__thym):
                        bodo.libs.array_kernels.setna(A, zby__thym)
                    else:
                        A[zby__thym] = ''.join([chr(lgut__sje) for
                            lgut__sje in data[zby__thym]])
                return A
            return impl_binary
        if is_overload_true(from_series) and data.dtype in (bodo.
            datetime64ns, bodo.timedelta64ns):

            def impl_str_dt_series(data, new_dtype, copy=None, nan_to_str=
                True, from_series=False):
                numba.parfors.parfor.init_prange()
                zqkxe__yrro = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(zqkxe__yrro,
                    -1)
                for zby__thym in numba.parfors.parfor.internal_prange(
                    zqkxe__yrro):
                    if bodo.libs.array_kernels.isna(data, zby__thym):
                        if nan_to_str:
                            A[zby__thym] = 'NaT'
                        else:
                            bodo.libs.array_kernels.setna(A, zby__thym)
                        continue
                    A[zby__thym] = str(box_if_dt64(data[zby__thym]))
                return A
            return impl_str_dt_series
        else:

            def impl_str_array(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                zqkxe__yrro = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(zqkxe__yrro,
                    -1)
                for zby__thym in numba.parfors.parfor.internal_prange(
                    zqkxe__yrro):
                    if bodo.libs.array_kernels.isna(data, zby__thym):
                        if nan_to_str:
                            A[zby__thym] = 'nan'
                        else:
                            bodo.libs.array_kernels.setna(A, zby__thym)
                        continue
                    A[zby__thym] = str(data[zby__thym])
                return A
            return impl_str_array
    if isinstance(new_dtype, bodo.hiframes.pd_categorical_ext.
        PDCategoricalDtype):

        def impl_cat_dtype(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            zqkxe__yrro = len(data)
            numba.parfors.parfor.init_prange()
            ylwp__sas = (bodo.hiframes.pd_categorical_ext.
                get_label_dict_from_categories(new_dtype.categories.values))
            A = bodo.hiframes.pd_categorical_ext.alloc_categorical_array(
                zqkxe__yrro, new_dtype)
            kdobn__swr = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A))
            for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                zqkxe__yrro):
                if bodo.libs.array_kernels.isna(data, gwbat__vvnlf):
                    bodo.libs.array_kernels.setna(A, gwbat__vvnlf)
                    continue
                val = data[gwbat__vvnlf]
                if val not in ylwp__sas:
                    bodo.libs.array_kernels.setna(A, gwbat__vvnlf)
                    continue
                kdobn__swr[gwbat__vvnlf] = ylwp__sas[val]
            return A
        return impl_cat_dtype
    if is_overload_constant_str(new_dtype) and get_overload_const_str(new_dtype
        ) == 'category':

        def impl_category(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            oelfi__vspa = bodo.libs.array_kernels.unique(data, dropna=True)
            oelfi__vspa = pd.Series(oelfi__vspa).sort_values().values
            oelfi__vspa = bodo.allgatherv(oelfi__vspa, False)
            lztjj__iul = bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo
                .utils.conversion.index_from_array(oelfi__vspa, None), 
                False, None, None)
            zqkxe__yrro = len(data)
            numba.parfors.parfor.init_prange()
            ylwp__sas = (bodo.hiframes.pd_categorical_ext.
                get_label_dict_from_categories_no_duplicates(oelfi__vspa))
            A = bodo.hiframes.pd_categorical_ext.alloc_categorical_array(
                zqkxe__yrro, lztjj__iul)
            kdobn__swr = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A))
            for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                zqkxe__yrro):
                if bodo.libs.array_kernels.isna(data, gwbat__vvnlf):
                    bodo.libs.array_kernels.setna(A, gwbat__vvnlf)
                    continue
                val = data[gwbat__vvnlf]
                kdobn__swr[gwbat__vvnlf] = ylwp__sas[val]
            return A
        return impl_category
    nb_dtype = bodo.utils.typing.parse_dtype(new_dtype)
    if isinstance(data, bodo.libs.int_arr_ext.IntegerArrayType):
        cgf__rwuv = isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype
            ) and data.dtype == nb_dtype.dtype
    else:
        cgf__rwuv = data.dtype == nb_dtype
    if wvn__ewt and cgf__rwuv:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data.copy())
    if cgf__rwuv:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data)
    if isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype):
        if isinstance(nb_dtype, types.Integer):
            rsn__ods = nb_dtype
        else:
            rsn__ods = nb_dtype.dtype
        if isinstance(data.dtype, types.Float):

            def impl_float(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                zqkxe__yrro = len(data)
                numba.parfors.parfor.init_prange()
                swdo__bwgus = bodo.libs.int_arr_ext.alloc_int_array(zqkxe__yrro
                    , rsn__ods)
                for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                    zqkxe__yrro):
                    if bodo.libs.array_kernels.isna(data, gwbat__vvnlf):
                        bodo.libs.array_kernels.setna(swdo__bwgus, gwbat__vvnlf
                            )
                    else:
                        swdo__bwgus[gwbat__vvnlf] = int(data[gwbat__vvnlf])
                return swdo__bwgus
            return impl_float
        else:
            if data == bodo.dict_str_arr_type:

                def impl_dict(data, new_dtype, copy=None, nan_to_str=True,
                    from_series=False):
                    return bodo.libs.dict_arr_ext.convert_dict_arr_to_int(data,
                        rsn__ods)
                return impl_dict
            if isinstance(data, bodo.hiframes.time_ext.TimeArrayType):

                def impl(data, new_dtype, copy=None, nan_to_str=True,
                    from_series=False):
                    zqkxe__yrro = len(data)
                    numba.parfors.parfor.init_prange()
                    swdo__bwgus = bodo.libs.int_arr_ext.alloc_int_array(
                        zqkxe__yrro, rsn__ods)
                    for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                        zqkxe__yrro):
                        if bodo.libs.array_kernels.isna(data, gwbat__vvnlf):
                            bodo.libs.array_kernels.setna(swdo__bwgus,
                                gwbat__vvnlf)
                        else:
                            swdo__bwgus[gwbat__vvnlf] = cast_time_to_int(data
                                [gwbat__vvnlf])
                    return swdo__bwgus
                return impl

            def impl(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                zqkxe__yrro = len(data)
                numba.parfors.parfor.init_prange()
                swdo__bwgus = bodo.libs.int_arr_ext.alloc_int_array(zqkxe__yrro
                    , rsn__ods)
                for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                    zqkxe__yrro):
                    if bodo.libs.array_kernels.isna(data, gwbat__vvnlf):
                        bodo.libs.array_kernels.setna(swdo__bwgus, gwbat__vvnlf
                            )
                    else:
                        swdo__bwgus[gwbat__vvnlf] = np.int64(data[gwbat__vvnlf]
                            )
                return swdo__bwgus
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
            zqkxe__yrro = len(data)
            numba.parfors.parfor.init_prange()
            swdo__bwgus = bodo.libs.bool_arr_ext.alloc_bool_array(zqkxe__yrro)
            for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                zqkxe__yrro):
                if bodo.libs.array_kernels.isna(data, gwbat__vvnlf):
                    bodo.libs.array_kernels.setna(swdo__bwgus, gwbat__vvnlf)
                else:
                    swdo__bwgus[gwbat__vvnlf] = bool(data[gwbat__vvnlf])
            return swdo__bwgus
        return impl_bool
    if nb_dtype == bodo.datetime_date_type:
        if data.dtype == bodo.datetime64ns:

            def impl_date(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                zqkxe__yrro = len(data)
                uoyak__pszl = (bodo.hiframes.datetime_date_ext.
                    alloc_datetime_date_array(zqkxe__yrro))
                for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                    zqkxe__yrro):
                    if bodo.libs.array_kernels.isna(data, gwbat__vvnlf):
                        bodo.libs.array_kernels.setna(uoyak__pszl, gwbat__vvnlf
                            )
                    else:
                        uoyak__pszl[gwbat__vvnlf
                            ] = bodo.utils.conversion.box_if_dt64(data[
                            gwbat__vvnlf]).date()
                return uoyak__pszl
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
                zqkxe__yrro = len(data)
                numba.parfors.parfor.init_prange()
                uoyak__pszl = np.empty(zqkxe__yrro, dtype=np.dtype(
                    'datetime64[ns]'))
                for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                    zqkxe__yrro):
                    if bodo.libs.array_kernels.isna(data, gwbat__vvnlf):
                        bodo.libs.array_kernels.setna(uoyak__pszl, gwbat__vvnlf
                            )
                    else:
                        uoyak__pszl[gwbat__vvnlf
                            ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                            np.int64(data[gwbat__vvnlf]))
                return uoyak__pszl
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
            if wvn__ewt:

                def impl_numeric(data, new_dtype, copy=None, nan_to_str=
                    True, from_series=False):
                    zqkxe__yrro = len(data)
                    numba.parfors.parfor.init_prange()
                    uoyak__pszl = np.empty(zqkxe__yrro, dtype=np.dtype(
                        'timedelta64[ns]'))
                    for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                        zqkxe__yrro):
                        if bodo.libs.array_kernels.isna(data, gwbat__vvnlf):
                            bodo.libs.array_kernels.setna(uoyak__pszl,
                                gwbat__vvnlf)
                        else:
                            uoyak__pszl[gwbat__vvnlf] = (bodo.hiframes.
                                pd_timestamp_ext.integer_to_timedelta64(np.
                                int64(data[gwbat__vvnlf])))
                    return uoyak__pszl
                return impl_numeric
            else:
                return (lambda data, new_dtype, copy=None, nan_to_str=True,
                    from_series=False: data.view('int64'))
    if nb_dtype == types.int64 and data.dtype in [bodo.datetime64ns, bodo.
        timedelta64ns]:

        def impl_datelike_to_integer(data, new_dtype, copy=None, nan_to_str
            =True, from_series=False):
            zqkxe__yrro = len(data)
            numba.parfors.parfor.init_prange()
            A = np.empty(zqkxe__yrro, types.int64)
            for gwbat__vvnlf in numba.parfors.parfor.internal_prange(
                zqkxe__yrro):
                if bodo.libs.array_kernels.isna(data, gwbat__vvnlf):
                    bodo.libs.array_kernels.setna(A, gwbat__vvnlf)
                else:
                    A[gwbat__vvnlf] = np.int64(data[gwbat__vvnlf])
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
    xteb__kawpk = []
    zqkxe__yrro = len(A)
    for gwbat__vvnlf in range(zqkxe__yrro):
        jfek__kwi = A[gwbat__vvnlf]
        for gvykz__qsi in jfek__kwi:
            xteb__kawpk.append(gvykz__qsi)
    return bodo.utils.conversion.coerce_to_array(xteb__kawpk)


def parse_datetimes_from_strings(data):
    return data


@overload(parse_datetimes_from_strings, no_unliteral=True)
def overload_parse_datetimes_from_strings(data):
    assert is_str_arr_type(data
        ), 'parse_datetimes_from_strings: string array expected'

    def parse_impl(data):
        numba.parfors.parfor.init_prange()
        zqkxe__yrro = len(data)
        mnt__qya = np.empty(zqkxe__yrro, bodo.utils.conversion.NS_DTYPE)
        for gwbat__vvnlf in numba.parfors.parfor.internal_prange(zqkxe__yrro):
            mnt__qya[gwbat__vvnlf
                ] = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(data[
                gwbat__vvnlf])
        return mnt__qya
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
        wfj__ktb = bodo.utils.conversion.coerce_to_array(data)
        return bodo.utils.conversion.index_from_array(wfj__ktb, name)
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
                nww__oion = None
            else:
                nww__oion = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(bodo
                    .utils.indexing.unoptional(val).value)
            return nww__oion
        return impl_optional
    if val == types.Optional(bodo.hiframes.datetime_timedelta_ext.
        pd_timedelta_type):

        def impl_optional_td(val):
            if val is None:
                nww__oion = None
            else:
                nww__oion = (bodo.hiframes.pd_timestamp_ext.
                    integer_to_timedelta64(bodo.utils.indexing.unoptional(
                    val).value))
            return nww__oion
        return impl_optional_td
    return lambda val: val


def to_tuple(val):
    return val


@overload(to_tuple, no_unliteral=True)
def overload_to_tuple(val):
    if not isinstance(val, types.BaseTuple) and is_overload_constant_list(val):
        lmqy__wrgx = len(val.types if isinstance(val, types.LiteralList) else
            get_overload_const_list(val))
        hivl__bmia = 'def f(val):\n'
        wnbz__ihbpd = ','.join(f'val[{gwbat__vvnlf}]' for gwbat__vvnlf in
            range(lmqy__wrgx))
        hivl__bmia += f'  return ({wnbz__ihbpd},)\n'
        lvlih__ltr = {}
        exec(hivl__bmia, {}, lvlih__ltr)
        impl = lvlih__ltr['f']
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
                glcx__kth = bodo.hiframes.pd_index_ext.get_index_data(data)
                return bodo.utils.conversion.coerce_to_array(glcx__kth)
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
            fld__htz = bodo.utils.conversion.coerce_to_array(index)
            return fld__htz
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
    return {icszk__todth: cloje__ouv for icszk__todth, cloje__ouv in zip(
        names, values)}


@overload(struct_if_heter_dict, no_unliteral=True)
def overload_struct_if_heter_dict(values, names):
    if not types.is_homogeneous(*values.types):
        return lambda values, names: bodo.libs.struct_arr_ext.init_struct(
            values, names)
    wxu__vza = len(values.types)
    hivl__bmia = 'def f(values, names):\n'
    wnbz__ihbpd = ','.join("'{}': values[{}]".format(get_overload_const_str
        (names.types[gwbat__vvnlf]), gwbat__vvnlf) for gwbat__vvnlf in
        range(wxu__vza))
    hivl__bmia += '  return {{{}}}\n'.format(wnbz__ihbpd)
    lvlih__ltr = {}
    exec(hivl__bmia, {}, lvlih__ltr)
    impl = lvlih__ltr['f']
    return impl
