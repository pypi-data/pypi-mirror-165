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
        raq__gmk = lhs.data if isinstance(lhs, SeriesType) else lhs
        vkal__rsg = rhs.data if isinstance(rhs, SeriesType) else rhs
        if raq__gmk in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and vkal__rsg.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            raq__gmk = vkal__rsg.dtype
        elif vkal__rsg in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and raq__gmk.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            vkal__rsg = raq__gmk.dtype
        vqvq__vgqf = raq__gmk, vkal__rsg
        vayc__jad = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            hbg__oflew = self.context.resolve_function_type(self.key,
                vqvq__vgqf, {}).return_type
        except Exception as nlkop__gpi:
            raise BodoError(vayc__jad)
        if is_overload_bool(hbg__oflew):
            raise BodoError(vayc__jad)
        bqhae__szn = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        vjtct__juj = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        itiq__mysd = types.bool_
        dpbmu__zmcwr = SeriesType(itiq__mysd, hbg__oflew, bqhae__szn,
            vjtct__juj)
        return dpbmu__zmcwr(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        gigt__rpp = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if gigt__rpp is None:
            gigt__rpp = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, gigt__rpp, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        raq__gmk = lhs.data if isinstance(lhs, SeriesType) else lhs
        vkal__rsg = rhs.data if isinstance(rhs, SeriesType) else rhs
        vqvq__vgqf = raq__gmk, vkal__rsg
        vayc__jad = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            hbg__oflew = self.context.resolve_function_type(self.key,
                vqvq__vgqf, {}).return_type
        except Exception as pjx__lgqal:
            raise BodoError(vayc__jad)
        bqhae__szn = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        vjtct__juj = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        itiq__mysd = hbg__oflew.dtype
        dpbmu__zmcwr = SeriesType(itiq__mysd, hbg__oflew, bqhae__szn,
            vjtct__juj)
        return dpbmu__zmcwr(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        gigt__rpp = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if gigt__rpp is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                gigt__rpp = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, gigt__rpp, sig, args)
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
            gigt__rpp = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return gigt__rpp(lhs, rhs)
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
            gigt__rpp = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return gigt__rpp(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    vcsb__meieg = lhs == datetime_timedelta_type and rhs == datetime_date_type
    jffh__zrf = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return vcsb__meieg or jffh__zrf


def add_timestamp(lhs, rhs):
    mqf__rzqfx = lhs == pd_timestamp_type and is_timedelta_type(rhs)
    zivyd__hob = is_timedelta_type(lhs) and rhs == pd_timestamp_type
    return mqf__rzqfx or zivyd__hob


def add_datetime_and_timedeltas(lhs, rhs):
    xmhv__owxok = [datetime_timedelta_type, pd_timedelta_type]
    iecfk__shvy = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    btjj__ypbaf = lhs in xmhv__owxok and rhs in xmhv__owxok
    dbr__rey = (lhs == datetime_datetime_type and rhs in xmhv__owxok or rhs ==
        datetime_datetime_type and lhs in xmhv__owxok)
    return btjj__ypbaf or dbr__rey


def mul_string_arr_and_int(lhs, rhs):
    vkal__rsg = isinstance(lhs, types.Integer) and is_str_arr_type(rhs)
    raq__gmk = is_str_arr_type(lhs) and isinstance(rhs, types.Integer)
    return vkal__rsg or raq__gmk


def mul_timedelta_and_int(lhs, rhs):
    vcsb__meieg = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    jffh__zrf = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return vcsb__meieg or jffh__zrf


def mul_date_offset_and_int(lhs, rhs):
    qpunz__vmy = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    iltn__ptwa = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return qpunz__vmy or iltn__ptwa


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    kmfhb__ajw = [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ]
    rsee__oul = [date_offset_type, month_begin_type, month_end_type, week_type]
    return rhs in rsee__oul and lhs in kmfhb__ajw


def sub_dt_index_and_timestamp(lhs, rhs):
    dvlk__tcekq = isinstance(lhs, DatetimeIndexType
        ) and rhs == pd_timestamp_type
    cdyk__jchk = isinstance(rhs, DatetimeIndexType
        ) and lhs == pd_timestamp_type
    return dvlk__tcekq or cdyk__jchk


def sub_dt_or_td(lhs, rhs):
    qhpqk__ztnqf = lhs == datetime_date_type and rhs == datetime_timedelta_type
    fekfm__azpa = lhs == datetime_date_type and rhs == datetime_date_type
    bwb__rsx = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return qhpqk__ztnqf or fekfm__azpa or bwb__rsx


def sub_datetime_and_timedeltas(lhs, rhs):
    jxnnr__uejuc = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    gye__adold = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return jxnnr__uejuc or gye__adold


def div_timedelta_and_int(lhs, rhs):
    btjj__ypbaf = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    xfaz__fqgtr = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return btjj__ypbaf or xfaz__fqgtr


def div_datetime_timedelta(lhs, rhs):
    btjj__ypbaf = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    xfaz__fqgtr = lhs == datetime_timedelta_type and rhs == types.int64
    return btjj__ypbaf or xfaz__fqgtr


def mod_timedeltas(lhs, rhs):
    ewjsz__vnxhl = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    lrsrn__usuhz = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return ewjsz__vnxhl or lrsrn__usuhz


def cmp_dt_index_to_string(lhs, rhs):
    dvlk__tcekq = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    cdyk__jchk = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return dvlk__tcekq or cdyk__jchk


def cmp_timestamp_or_date(lhs, rhs):
    pqrsr__pkpnb = (lhs == pd_timestamp_type and rhs == bodo.hiframes.
        datetime_date_ext.datetime_date_type)
    duri__hljw = (lhs == bodo.hiframes.datetime_date_ext.datetime_date_type and
        rhs == pd_timestamp_type)
    ixy__eop = lhs == pd_timestamp_type and rhs == pd_timestamp_type
    fdm__qkdve = lhs == pd_timestamp_type and rhs == bodo.datetime64ns
    xfgxu__suah = rhs == pd_timestamp_type and lhs == bodo.datetime64ns
    return pqrsr__pkpnb or duri__hljw or ixy__eop or fdm__qkdve or xfgxu__suah


def cmp_timeseries(lhs, rhs):
    gwv__sutjm = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (bodo
        .utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs.
        str_ext.string_type or lhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    hyrya__oxnq = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (bodo
        .utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs.
        str_ext.string_type or rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    mnhkm__ddtmh = gwv__sutjm or hyrya__oxnq
    wupzo__bimtd = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    dtsky__isfdl = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    pcxrn__czg = wupzo__bimtd or dtsky__isfdl
    return mnhkm__ddtmh or pcxrn__czg


def cmp_timedeltas(lhs, rhs):
    btjj__ypbaf = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in btjj__ypbaf and rhs in btjj__ypbaf


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    ggx__ltfh = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_type]
    return ggx__ltfh


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    ytekz__akuu = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    jeyj__vdert = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    spr__gyw = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    uwg__bfzp = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return ytekz__akuu or jeyj__vdert or spr__gyw or uwg__bfzp


def args_td_and_int_array(lhs, rhs):
    xwj__dhcd = (isinstance(lhs, IntegerArrayType) or isinstance(lhs, types
        .Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance(
        rhs, IntegerArrayType) or isinstance(rhs, types.Array) and
        isinstance(rhs.dtype, types.Integer))
    wio__xvf = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return xwj__dhcd and wio__xvf


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        jffh__zrf = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        vcsb__meieg = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        ofy__zub = jffh__zrf or vcsb__meieg
        ocu__kpqob = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        cxfct__mfcr = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        ygghw__rycxm = ocu__kpqob or cxfct__mfcr
        jqx__sadz = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        dtj__pwz = isinstance(lhs, types.Float) and isinstance(rhs, types.Float
            )
        lccy__mwbx = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        ldriu__kxnx = jqx__sadz or dtj__pwz or lccy__mwbx
        zshp__ksg = isinstance(lhs, types.List) and isinstance(rhs, types.
            Integer) or isinstance(lhs, types.Integer) and isinstance(rhs,
            types.List)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        ayrtn__jlm = isinstance(lhs, tys) or isinstance(rhs, tys)
        dvya__dtsc = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (ofy__zub or ygghw__rycxm or ldriu__kxnx or zshp__ksg or
            ayrtn__jlm or dvya__dtsc)
    if op == operator.pow:
        nrek__qjy = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        qvbld__fyc = isinstance(lhs, types.Float) and isinstance(rhs, (
            types.IntegerLiteral, types.Float, types.Integer) or rhs in
            types.unsigned_domain or rhs in types.signed_domain)
        lccy__mwbx = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        dvya__dtsc = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return nrek__qjy or qvbld__fyc or lccy__mwbx or dvya__dtsc
    if op == operator.floordiv:
        dtj__pwz = lhs in types.real_domain and rhs in types.real_domain
        jqx__sadz = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        pixl__qmpcs = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        btjj__ypbaf = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        dvya__dtsc = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (dtj__pwz or jqx__sadz or pixl__qmpcs or btjj__ypbaf or
            dvya__dtsc)
    if op == operator.truediv:
        msv__xcheg = lhs in machine_ints and rhs in machine_ints
        dtj__pwz = lhs in types.real_domain and rhs in types.real_domain
        lccy__mwbx = (lhs in types.complex_domain and rhs in types.
            complex_domain)
        jqx__sadz = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        pixl__qmpcs = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        evxml__yptni = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        btjj__ypbaf = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        dvya__dtsc = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (msv__xcheg or dtj__pwz or lccy__mwbx or jqx__sadz or
            pixl__qmpcs or evxml__yptni or btjj__ypbaf or dvya__dtsc)
    if op == operator.mod:
        msv__xcheg = lhs in machine_ints and rhs in machine_ints
        dtj__pwz = lhs in types.real_domain and rhs in types.real_domain
        jqx__sadz = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        pixl__qmpcs = isinstance(lhs, types.Float) and isinstance(rhs,
            types.Float)
        dvya__dtsc = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return msv__xcheg or dtj__pwz or jqx__sadz or pixl__qmpcs or dvya__dtsc
    if op == operator.add or op == operator.sub:
        ofy__zub = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        ckuei__xmfmc = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        dxa__whcd = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        auiku__qogcw = isinstance(lhs, types.Set) and isinstance(rhs, types.Set
            )
        jqx__sadz = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        dtj__pwz = isinstance(lhs, types.Float) and isinstance(rhs, types.Float
            )
        lccy__mwbx = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        ldriu__kxnx = jqx__sadz or dtj__pwz or lccy__mwbx
        dvya__dtsc = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        szdjw__djco = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        zshp__ksg = isinstance(lhs, types.List) and isinstance(rhs, types.List)
        tyoj__sxenk = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeType)
        mjzzi__kbjs = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs,
            types.UnicodeType)
        ejzt__nhkr = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeCharSeq)
        smnq__tvxy = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        eky__tfwys = tyoj__sxenk or mjzzi__kbjs or ejzt__nhkr or smnq__tvxy
        ygghw__rycxm = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        azz__grqo = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        fcg__upas = ygghw__rycxm or azz__grqo
        yxza__gvnyc = lhs == types.NPTimedelta and rhs == types.NPDatetime
        iuaw__rtbe = (szdjw__djco or zshp__ksg or eky__tfwys or fcg__upas or
            yxza__gvnyc)
        wvx__fjwmo = op == operator.add and iuaw__rtbe
        return (ofy__zub or ckuei__xmfmc or dxa__whcd or auiku__qogcw or
            ldriu__kxnx or dvya__dtsc or wvx__fjwmo)


def cmp_op_supported_by_numba(lhs, rhs):
    dvya__dtsc = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    zshp__ksg = isinstance(lhs, types.ListType) and isinstance(rhs, types.
        ListType)
    ofy__zub = isinstance(lhs, types.NPTimedelta) and isinstance(rhs, types
        .NPTimedelta)
    eyo__oliyv = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
        types.NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    ygghw__rycxm = isinstance(lhs, unicode_types) and isinstance(rhs,
        unicode_types)
    szdjw__djco = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
        types.BaseTuple)
    auiku__qogcw = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    ldriu__kxnx = isinstance(lhs, types.Number) and isinstance(rhs, types.
        Number)
    xky__zqk = isinstance(lhs, types.Boolean) and isinstance(rhs, types.Boolean
        )
    uapjm__ixdow = isinstance(lhs, types.NoneType) or isinstance(rhs, types
        .NoneType)
    qxk__bcf = isinstance(lhs, types.DictType) and isinstance(rhs, types.
        DictType)
    dyl__jphe = isinstance(lhs, types.EnumMember) and isinstance(rhs, types
        .EnumMember)
    zeygk__cju = isinstance(lhs, types.Literal) and isinstance(rhs, types.
        Literal)
    return (zshp__ksg or ofy__zub or eyo__oliyv or ygghw__rycxm or
        szdjw__djco or auiku__qogcw or ldriu__kxnx or xky__zqk or
        uapjm__ixdow or qxk__bcf or dvya__dtsc or dyl__jphe or zeygk__cju)


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
        ftpht__yfs = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(ftpht__yfs)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        ftpht__yfs = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(ftpht__yfs)


install_arith_ops()
