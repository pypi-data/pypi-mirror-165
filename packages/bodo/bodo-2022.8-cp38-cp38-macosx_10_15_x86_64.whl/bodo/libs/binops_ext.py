""" Implementation of binary operators for the different types.
    Currently implemented operators:
        arith: add, sub, mul, truediv, floordiv, mod, pow
        cmp: lt, le, eq, ne, ge, gt
"""
import operator
import numba
from numba.core import types
from numba.core.imputils import lower_builtin
from numba.core.typing.builtins import machine_ints
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import overload
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type, datetime_date_type, datetime_timedelta_type
from bodo.hiframes.datetime_timedelta_ext import datetime_datetime_type, datetime_timedelta_array_type, pd_timedelta_type
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import DatetimeIndexType, HeterogeneousIndexType, is_index_type
from bodo.hiframes.pd_offsets_ext import date_offset_type, month_begin_type, month_end_type, week_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_type
from bodo.hiframes.series_impl import SeriesType
from bodo.hiframes.time_ext import TimeType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import Decimal128Type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_ext import string_type
from bodo.utils.typing import BodoError, is_overload_bool, is_str_arr_type, is_timedelta_type


class SeriesCmpOpTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        lhs, rhs = args
        if cmp_timeseries(lhs, rhs) or (isinstance(lhs, DataFrameType) or
            isinstance(rhs, DataFrameType)) or not (isinstance(lhs,
            SeriesType) or isinstance(rhs, SeriesType)):
            return
        kjl__amz = lhs.data if isinstance(lhs, SeriesType) else lhs
        anuuq__crz = rhs.data if isinstance(rhs, SeriesType) else rhs
        if kjl__amz in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and anuuq__crz.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            kjl__amz = anuuq__crz.dtype
        elif anuuq__crz in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and kjl__amz.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            anuuq__crz = kjl__amz.dtype
        olibk__rhpj = kjl__amz, anuuq__crz
        zroz__dfie = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            tvebk__krdrp = self.context.resolve_function_type(self.key,
                olibk__rhpj, {}).return_type
        except Exception as nrsd__xot:
            raise BodoError(zroz__dfie)
        if is_overload_bool(tvebk__krdrp):
            raise BodoError(zroz__dfie)
        pei__vrrk = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        nutf__mhrzk = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        ycdmw__susst = types.bool_
        fpbc__hgwg = SeriesType(ycdmw__susst, tvebk__krdrp, pei__vrrk,
            nutf__mhrzk)
        return fpbc__hgwg(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        udkx__mofxa = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if udkx__mofxa is None:
            udkx__mofxa = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, udkx__mofxa, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        kjl__amz = lhs.data if isinstance(lhs, SeriesType) else lhs
        anuuq__crz = rhs.data if isinstance(rhs, SeriesType) else rhs
        olibk__rhpj = kjl__amz, anuuq__crz
        zroz__dfie = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            tvebk__krdrp = self.context.resolve_function_type(self.key,
                olibk__rhpj, {}).return_type
        except Exception as isvb__jpiq:
            raise BodoError(zroz__dfie)
        pei__vrrk = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        nutf__mhrzk = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        ycdmw__susst = tvebk__krdrp.dtype
        fpbc__hgwg = SeriesType(ycdmw__susst, tvebk__krdrp, pei__vrrk,
            nutf__mhrzk)
        return fpbc__hgwg(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        udkx__mofxa = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if udkx__mofxa is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                udkx__mofxa = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, udkx__mofxa, sig, args)
    return lower_and_or_impl


def overload_add_operator_scalars(lhs, rhs):
    if lhs == week_type or rhs == week_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_week_offset_type(lhs, rhs))
    if lhs == month_begin_type or rhs == month_begin_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_month_begin_offset_type(lhs, rhs))
    if lhs == month_end_type or rhs == month_end_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_month_end_offset_type(lhs, rhs))
    if lhs == date_offset_type or rhs == date_offset_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_date_offset_type(lhs, rhs))
    if add_timestamp(lhs, rhs):
        return bodo.hiframes.pd_timestamp_ext.overload_add_operator_timestamp(
            lhs, rhs)
    if add_dt_td_and_dt_date(lhs, rhs):
        return (bodo.hiframes.datetime_date_ext.
            overload_add_operator_datetime_date(lhs, rhs))
    if add_datetime_and_timedeltas(lhs, rhs):
        return (bodo.hiframes.datetime_timedelta_ext.
            overload_add_operator_datetime_timedelta(lhs, rhs))
    raise_error_if_not_numba_supported(operator.add, lhs, rhs)


def overload_sub_operator_scalars(lhs, rhs):
    if sub_offset_to_datetime_or_timestamp(lhs, rhs):
        return bodo.hiframes.pd_offsets_ext.overload_sub_operator_offsets(lhs,
            rhs)
    if lhs == pd_timestamp_type and rhs in [pd_timestamp_type,
        datetime_timedelta_type, pd_timedelta_type]:
        return bodo.hiframes.pd_timestamp_ext.overload_sub_operator_timestamp(
            lhs, rhs)
    if sub_dt_or_td(lhs, rhs):
        return (bodo.hiframes.datetime_date_ext.
            overload_sub_operator_datetime_date(lhs, rhs))
    if sub_datetime_and_timedeltas(lhs, rhs):
        return (bodo.hiframes.datetime_timedelta_ext.
            overload_sub_operator_datetime_timedelta(lhs, rhs))
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:
        return (bodo.hiframes.datetime_datetime_ext.
            overload_sub_operator_datetime_datetime(lhs, rhs))
    raise_error_if_not_numba_supported(operator.sub, lhs, rhs)


def create_overload_arith_op(op):

    def overload_arith_operator(lhs, rhs):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lhs,
            f'{op} operator')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rhs,
            f'{op} operator')
        if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType):
            return bodo.hiframes.dataframe_impl.create_binary_op_overload(op)(
                lhs, rhs)
        if time_series_operation(lhs, rhs) and op in [operator.add,
            operator.sub]:
            return bodo.hiframes.series_dt_impl.create_bin_op_overload(op)(lhs,
                rhs)
        if isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType):
            return bodo.hiframes.series_impl.create_binary_op_overload(op)(lhs,
                rhs)
        if sub_dt_index_and_timestamp(lhs, rhs) and op == operator.sub:
            return (bodo.hiframes.pd_index_ext.
                overload_sub_operator_datetime_index(lhs, rhs))
        if operand_is_index(lhs) or operand_is_index(rhs):
            return bodo.hiframes.pd_index_ext.create_binary_op_overload(op)(lhs
                , rhs)
        if args_td_and_int_array(lhs, rhs):
            return bodo.libs.int_arr_ext.get_int_array_op_pd_td(op)(lhs, rhs)
        if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
            IntegerArrayType):
            return bodo.libs.int_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if lhs == boolean_array or rhs == boolean_array:
            return bodo.libs.bool_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if op == operator.add and (is_str_arr_type(lhs) or types.unliteral(
            lhs) == string_type):
            return bodo.libs.str_arr_ext.overload_add_operator_string_array(lhs
                , rhs)
        if op == operator.add:
            return overload_add_operator_scalars(lhs, rhs)
        if op == operator.sub:
            return overload_sub_operator_scalars(lhs, rhs)
        if op == operator.mul:
            if mul_timedelta_and_int(lhs, rhs):
                return (bodo.hiframes.datetime_timedelta_ext.
                    overload_mul_operator_timedelta(lhs, rhs))
            if mul_string_arr_and_int(lhs, rhs):
                return bodo.libs.str_arr_ext.overload_mul_operator_str_arr(lhs,
                    rhs)
            if mul_date_offset_and_int(lhs, rhs):
                return (bodo.hiframes.pd_offsets_ext.
                    overload_mul_date_offset_types(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op in [operator.truediv, operator.floordiv]:
            if div_timedelta_and_int(lhs, rhs):
                if op == operator.truediv:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_truediv_operator_pd_timedelta(lhs, rhs))
                else:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_floordiv_operator_pd_timedelta(lhs, rhs))
            if div_datetime_timedelta(lhs, rhs):
                if op == operator.truediv:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_truediv_operator_dt_timedelta(lhs, rhs))
                else:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_floordiv_operator_dt_timedelta(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op == operator.mod:
            if mod_timedeltas(lhs, rhs):
                return (bodo.hiframes.datetime_timedelta_ext.
                    overload_mod_operator_timedeltas(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op == operator.pow:
            raise_error_if_not_numba_supported(op, lhs, rhs)
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_arith_operator


def create_overload_cmp_operator(op):

    def overload_cmp_operator(lhs, rhs):
        if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType):
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lhs,
                f'{op} operator')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rhs,
                f'{op} operator')
            return bodo.hiframes.dataframe_impl.create_binary_op_overload(op)(
                lhs, rhs)
        if cmp_timeseries(lhs, rhs):
            return bodo.hiframes.series_dt_impl.create_cmp_op_overload(op)(lhs,
                rhs)
        if isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType):
            return
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lhs,
            f'{op} operator')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rhs,
            f'{op} operator')
        if lhs == datetime_date_array_type or rhs == datetime_date_array_type:
            return bodo.hiframes.datetime_date_ext.create_cmp_op_overload_arr(
                op)(lhs, rhs)
        if (lhs == datetime_timedelta_array_type or rhs ==
            datetime_timedelta_array_type):
            udkx__mofxa = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return udkx__mofxa(lhs, rhs)
        if is_str_arr_type(lhs) or is_str_arr_type(rhs):
            return bodo.libs.str_arr_ext.create_binary_op_overload(op)(lhs, rhs
                )
        if isinstance(lhs, Decimal128Type) and isinstance(rhs, Decimal128Type):
            return bodo.libs.decimal_arr_ext.decimal_create_cmp_op_overload(op
                )(lhs, rhs)
        if lhs == boolean_array or rhs == boolean_array:
            return bodo.libs.bool_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
            IntegerArrayType):
            return bodo.libs.int_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if binary_array_cmp(lhs, rhs):
            return bodo.libs.binary_arr_ext.create_binary_cmp_op_overload(op)(
                lhs, rhs)
        if cmp_dt_index_to_string(lhs, rhs):
            return bodo.hiframes.pd_index_ext.overload_binop_dti_str(op)(lhs,
                rhs)
        if operand_is_index(lhs) or operand_is_index(rhs):
            return bodo.hiframes.pd_index_ext.create_binary_op_overload(op)(lhs
                , rhs)
        if lhs == datetime_date_type and rhs == datetime_date_type:
            return bodo.hiframes.datetime_date_ext.create_cmp_op_overload(op)(
                lhs, rhs)
        if isinstance(lhs, TimeType) and isinstance(rhs, TimeType):
            return bodo.hiframes.time_ext.create_cmp_op_overload(op)(lhs, rhs)
        if can_cmp_date_datetime(lhs, rhs, op):
            return (bodo.hiframes.datetime_date_ext.
                create_datetime_date_cmp_op_overload(op)(lhs, rhs))
        if lhs == datetime_datetime_type and rhs == datetime_datetime_type:
            return bodo.hiframes.datetime_datetime_ext.create_cmp_op_overload(
                op)(lhs, rhs)
        if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:
            return bodo.hiframes.datetime_timedelta_ext.create_cmp_op_overload(
                op)(lhs, rhs)
        if cmp_timedeltas(lhs, rhs):
            udkx__mofxa = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return udkx__mofxa(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    mmekf__gvum = lhs == datetime_timedelta_type and rhs == datetime_date_type
    yuptk__waa = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return mmekf__gvum or yuptk__waa


def add_timestamp(lhs, rhs):
    aadw__qlm = lhs == pd_timestamp_type and is_timedelta_type(rhs)
    rjgzo__lpp = is_timedelta_type(lhs) and rhs == pd_timestamp_type
    return aadw__qlm or rjgzo__lpp


def add_datetime_and_timedeltas(lhs, rhs):
    vnx__dnzf = [datetime_timedelta_type, pd_timedelta_type]
    dppr__auu = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    iqpw__hylsf = lhs in vnx__dnzf and rhs in vnx__dnzf
    hyvd__wdfw = (lhs == datetime_datetime_type and rhs in vnx__dnzf or rhs ==
        datetime_datetime_type and lhs in vnx__dnzf)
    return iqpw__hylsf or hyvd__wdfw


def mul_string_arr_and_int(lhs, rhs):
    anuuq__crz = isinstance(lhs, types.Integer) and is_str_arr_type(rhs)
    kjl__amz = is_str_arr_type(lhs) and isinstance(rhs, types.Integer)
    return anuuq__crz or kjl__amz


def mul_timedelta_and_int(lhs, rhs):
    mmekf__gvum = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    yuptk__waa = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return mmekf__gvum or yuptk__waa


def mul_date_offset_and_int(lhs, rhs):
    bdcoq__zore = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    twejx__ukz = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return bdcoq__zore or twejx__ukz


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    htuxs__ichi = [datetime_datetime_type, pd_timestamp_type,
        datetime_date_type]
    vnu__cqnw = [date_offset_type, month_begin_type, month_end_type, week_type]
    return rhs in vnu__cqnw and lhs in htuxs__ichi


def sub_dt_index_and_timestamp(lhs, rhs):
    wgxsa__dsvsf = isinstance(lhs, DatetimeIndexType
        ) and rhs == pd_timestamp_type
    awdlv__khvc = isinstance(rhs, DatetimeIndexType
        ) and lhs == pd_timestamp_type
    return wgxsa__dsvsf or awdlv__khvc


def sub_dt_or_td(lhs, rhs):
    cyruy__uiz = lhs == datetime_date_type and rhs == datetime_timedelta_type
    epytd__imfkx = lhs == datetime_date_type and rhs == datetime_date_type
    ylare__wfp = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return cyruy__uiz or epytd__imfkx or ylare__wfp


def sub_datetime_and_timedeltas(lhs, rhs):
    urin__olcm = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    gze__rul = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return urin__olcm or gze__rul


def div_timedelta_and_int(lhs, rhs):
    iqpw__hylsf = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    asu__cmbvz = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return iqpw__hylsf or asu__cmbvz


def div_datetime_timedelta(lhs, rhs):
    iqpw__hylsf = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    asu__cmbvz = lhs == datetime_timedelta_type and rhs == types.int64
    return iqpw__hylsf or asu__cmbvz


def mod_timedeltas(lhs, rhs):
    ozc__ixdr = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    daad__tav = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return ozc__ixdr or daad__tav


def cmp_dt_index_to_string(lhs, rhs):
    wgxsa__dsvsf = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    awdlv__khvc = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return wgxsa__dsvsf or awdlv__khvc


def cmp_timestamp_or_date(lhs, rhs):
    bjxo__yssw = (lhs == pd_timestamp_type and rhs == bodo.hiframes.
        datetime_date_ext.datetime_date_type)
    hzgc__jpfn = (lhs == bodo.hiframes.datetime_date_ext.datetime_date_type and
        rhs == pd_timestamp_type)
    szq__cefl = lhs == pd_timestamp_type and rhs == pd_timestamp_type
    nqjf__xbj = lhs == pd_timestamp_type and rhs == bodo.datetime64ns
    migih__yoqdw = rhs == pd_timestamp_type and lhs == bodo.datetime64ns
    return bjxo__yssw or hzgc__jpfn or szq__cefl or nqjf__xbj or migih__yoqdw


def cmp_timeseries(lhs, rhs):
    hdnx__qnr = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (bodo
        .utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs.
        str_ext.string_type or lhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    xrpp__usnjt = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (bodo
        .utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs.
        str_ext.string_type or rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    jen__wfx = hdnx__qnr or xrpp__usnjt
    qdi__ehb = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    lgbs__rlpki = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    dyter__tyel = qdi__ehb or lgbs__rlpki
    return jen__wfx or dyter__tyel


def cmp_timedeltas(lhs, rhs):
    iqpw__hylsf = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in iqpw__hylsf and rhs in iqpw__hylsf


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    jaqjy__hxa = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_type]
    return jaqjy__hxa


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    ptioq__qmy = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    stdac__ronw = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    eonv__bgpec = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    acav__wxc = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return ptioq__qmy or stdac__ronw or eonv__bgpec or acav__wxc


def args_td_and_int_array(lhs, rhs):
    biydh__kjhrp = (isinstance(lhs, IntegerArrayType) or isinstance(lhs,
        types.Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance
        (rhs, IntegerArrayType) or isinstance(rhs, types.Array) and
        isinstance(rhs.dtype, types.Integer))
    yit__dvfs = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return biydh__kjhrp and yit__dvfs


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        yuptk__waa = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        mmekf__gvum = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        cpoho__gzhm = yuptk__waa or mmekf__gvum
        zizp__rxoj = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        ysoh__nouny = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        wmvf__axfam = zizp__rxoj or ysoh__nouny
        mthe__nmjk = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        lqm__ykofh = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        xwthd__qurg = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        etjko__non = mthe__nmjk or lqm__ykofh or xwthd__qurg
        vfzje__jyw = isinstance(lhs, types.List) and isinstance(rhs, types.
            Integer) or isinstance(lhs, types.Integer) and isinstance(rhs,
            types.List)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        klmf__rxhq = isinstance(lhs, tys) or isinstance(rhs, tys)
        dqrt__lxal = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (cpoho__gzhm or wmvf__axfam or etjko__non or vfzje__jyw or
            klmf__rxhq or dqrt__lxal)
    if op == operator.pow:
        nvbg__rxkyw = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        ixuig__zzn = isinstance(lhs, types.Float) and isinstance(rhs, (
            types.IntegerLiteral, types.Float, types.Integer) or rhs in
            types.unsigned_domain or rhs in types.signed_domain)
        xwthd__qurg = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        dqrt__lxal = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return nvbg__rxkyw or ixuig__zzn or xwthd__qurg or dqrt__lxal
    if op == operator.floordiv:
        lqm__ykofh = lhs in types.real_domain and rhs in types.real_domain
        mthe__nmjk = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        sekpi__lspzg = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        iqpw__hylsf = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        dqrt__lxal = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (lqm__ykofh or mthe__nmjk or sekpi__lspzg or iqpw__hylsf or
            dqrt__lxal)
    if op == operator.truediv:
        dgmvm__oqkv = lhs in machine_ints and rhs in machine_ints
        lqm__ykofh = lhs in types.real_domain and rhs in types.real_domain
        xwthd__qurg = (lhs in types.complex_domain and rhs in types.
            complex_domain)
        mthe__nmjk = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        sekpi__lspzg = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        cufwo__qtzrv = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        iqpw__hylsf = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        dqrt__lxal = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (dgmvm__oqkv or lqm__ykofh or xwthd__qurg or mthe__nmjk or
            sekpi__lspzg or cufwo__qtzrv or iqpw__hylsf or dqrt__lxal)
    if op == operator.mod:
        dgmvm__oqkv = lhs in machine_ints and rhs in machine_ints
        lqm__ykofh = lhs in types.real_domain and rhs in types.real_domain
        mthe__nmjk = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        sekpi__lspzg = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        dqrt__lxal = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (dgmvm__oqkv or lqm__ykofh or mthe__nmjk or sekpi__lspzg or
            dqrt__lxal)
    if op == operator.add or op == operator.sub:
        cpoho__gzhm = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        qub__lht = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        uzq__qctqa = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        qozvk__cnf = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
        mthe__nmjk = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        lqm__ykofh = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        xwthd__qurg = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        etjko__non = mthe__nmjk or lqm__ykofh or xwthd__qurg
        dqrt__lxal = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        tsur__dxnw = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        vfzje__jyw = isinstance(lhs, types.List) and isinstance(rhs, types.List
            )
        kwil__kyzm = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeType)
        edbi__lqum = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs,
            types.UnicodeType)
        qxlq__mclho = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeCharSeq)
        yfsns__nand = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        qswqc__zkiqk = kwil__kyzm or edbi__lqum or qxlq__mclho or yfsns__nand
        wmvf__axfam = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        uljc__kimhf = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        bwvob__mctw = wmvf__axfam or uljc__kimhf
        itq__dfj = lhs == types.NPTimedelta and rhs == types.NPDatetime
        ein__opcql = (tsur__dxnw or vfzje__jyw or qswqc__zkiqk or
            bwvob__mctw or itq__dfj)
        sjc__inj = op == operator.add and ein__opcql
        return (cpoho__gzhm or qub__lht or uzq__qctqa or qozvk__cnf or
            etjko__non or dqrt__lxal or sjc__inj)


def cmp_op_supported_by_numba(lhs, rhs):
    dqrt__lxal = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    vfzje__jyw = isinstance(lhs, types.ListType) and isinstance(rhs, types.
        ListType)
    cpoho__gzhm = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
        types.NPTimedelta)
    pctxp__neke = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
        types.NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    wmvf__axfam = isinstance(lhs, unicode_types) and isinstance(rhs,
        unicode_types)
    tsur__dxnw = isinstance(lhs, types.BaseTuple) and isinstance(rhs, types
        .BaseTuple)
    qozvk__cnf = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    etjko__non = isinstance(lhs, types.Number) and isinstance(rhs, types.Number
        )
    nxa__qmdk = isinstance(lhs, types.Boolean) and isinstance(rhs, types.
        Boolean)
    yregv__yxdyq = isinstance(lhs, types.NoneType) or isinstance(rhs, types
        .NoneType)
    aujs__cgnoc = isinstance(lhs, types.DictType) and isinstance(rhs, types
        .DictType)
    icz__fmp = isinstance(lhs, types.EnumMember) and isinstance(rhs, types.
        EnumMember)
    bbeem__knp = isinstance(lhs, types.Literal) and isinstance(rhs, types.
        Literal)
    return (vfzje__jyw or cpoho__gzhm or pctxp__neke or wmvf__axfam or
        tsur__dxnw or qozvk__cnf or etjko__non or nxa__qmdk or yregv__yxdyq or
        aujs__cgnoc or dqrt__lxal or icz__fmp or bbeem__knp)


def raise_error_if_not_numba_supported(op, lhs, rhs):
    if arith_op_supported_by_numba(op, lhs, rhs):
        return
    raise BodoError(
        f'{op} operator not supported for data types {lhs} and {rhs}.')


def _install_series_and_or():
    for op in (operator.or_, operator.and_):
        infer_global(op)(SeriesAndOrTyper)
        lower_impl = lower_series_and_or(op)
        lower_builtin(op, SeriesType, SeriesType)(lower_impl)
        lower_builtin(op, SeriesType, types.Any)(lower_impl)
        lower_builtin(op, types.Any, SeriesType)(lower_impl)


_install_series_and_or()


def _install_cmp_ops():
    for op in (operator.lt, operator.eq, operator.ne, operator.ge, operator
        .gt, operator.le):
        infer_global(op)(SeriesCmpOpTemplate)
        lower_impl = series_cmp_op_lower(op)
        lower_builtin(op, SeriesType, SeriesType)(lower_impl)
        lower_builtin(op, SeriesType, types.Any)(lower_impl)
        lower_builtin(op, types.Any, SeriesType)(lower_impl)
        ekc__hostk = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(ekc__hostk)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        ekc__hostk = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(ekc__hostk)


install_arith_ops()
