"""
Implement pd.DataFrame typing and data model handling.
"""
import json
import operator
import time
from functools import cached_property
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import AbstractTemplate, bound_function, infer_global, signature
from numba.cpython.listobj import ListInstance
from numba.extending import infer_getattr, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.hiframes.pd_index_ext import HeterogeneousIndexType, NumericIndexType, RangeIndexType, is_pd_index_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.hiframes.series_indexing import SeriesIlocType
from bodo.hiframes.table import Table, TableType, decode_if_dict_table, get_table_data, set_table_data_codegen
from bodo.hiframes.time_ext import TimeArrayType
from bodo.io import json_cpp
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_info_decref_array, delete_table, delete_table_decref_arrays, info_from_table, info_to_array, py_table_to_cpp_table, shuffle_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import str_arr_from_sequence
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils import tracing
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.conversion import fix_arr_dtype, index_to_array
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.transform import get_const_func_output_type
from bodo.utils.typing import BodoError, BodoWarning, ColNamesMetaType, check_unsupported_args, create_unsupported_overload, decode_if_dict_array, dtype_to_array_type, get_index_data_arr_types, get_literal_value, get_overload_const, get_overload_const_bool, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_udf_error_msg, get_udf_out_arr_type, is_heterogeneous_tuple_type, is_iterable_type, is_literal_type, is_overload_bool, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_str, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_str_arr_type, is_tuple_like_type, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array
from bodo.utils.utils import is_null_pointer
_json_write = types.ExternalFunction('json_write', types.void(types.voidptr,
    types.voidptr, types.int64, types.int64, types.bool_, types.bool_,
    types.voidptr, types.voidptr))
ll.add_symbol('json_write', json_cpp.json_write)


class DataFrameType(types.ArrayCompatible):
    ndim = 2

    def __init__(self, data=None, index=None, columns=None, dist=None,
        is_table_format=False):
        from bodo.transforms.distributed_analysis import Distribution
        self.data = data
        if index is None:
            index = RangeIndexType(types.none)
        self.index = index
        self.columns = columns
        dist = Distribution.OneD_Var if dist is None else dist
        self.dist = dist
        self.is_table_format = is_table_format
        if columns is None:
            assert is_table_format, 'Determining columns at runtime is only supported for DataFrame with table format'
            self.table_type = TableType(tuple(data[:-1]), True)
        else:
            self.table_type = TableType(data) if is_table_format else None
        super(DataFrameType, self).__init__(name=
            f'dataframe({data}, {index}, {columns}, {dist}, {is_table_format}, {self.has_runtime_cols})'
            )

    def __str__(self):
        if not self.has_runtime_cols and len(self.columns) > 20:
            xrq__svrx = f'{len(self.data)} columns of types {set(self.data)}'
            gvon__gfbk = (
                f"('{self.columns[0]}', '{self.columns[1]}', ..., '{self.columns[-1]}')"
                )
            return (
                f'dataframe({xrq__svrx}, {self.index}, {gvon__gfbk}, {self.dist}, {self.is_table_format}, {self.has_runtime_cols})'
                )
        return super().__str__()

    def copy(self, data=None, index=None, columns=None, dist=None,
        is_table_format=None):
        if data is None:
            data = self.data
        if columns is None:
            columns = self.columns
        if index is None:
            index = self.index
        if dist is None:
            dist = self.dist
        if is_table_format is None:
            is_table_format = self.is_table_format
        return DataFrameType(data, index, columns, dist, is_table_format)

    @property
    def has_runtime_cols(self):
        return self.columns is None

    @cached_property
    def column_index(self):
        return {crsf__qrtc: i for i, crsf__qrtc in enumerate(self.columns)}

    @property
    def runtime_colname_typ(self):
        return self.data[-1] if self.has_runtime_cols else None

    @property
    def runtime_data_types(self):
        return self.data[:-1] if self.has_runtime_cols else self.data

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    @property
    def key(self):
        return (self.data, self.index, self.columns, self.dist, self.
            is_table_format)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    def unify(self, typingctx, other):
        from bodo.transforms.distributed_analysis import Distribution
        if (isinstance(other, DataFrameType) and len(other.data) == len(
            self.data) and other.columns == self.columns and other.
            has_runtime_cols == self.has_runtime_cols):
            ehvgf__dreoz = (self.index if self.index == other.index else
                self.index.unify(typingctx, other.index))
            data = tuple(uzlt__sfloq.unify(typingctx, quej__djwwl) if 
                uzlt__sfloq != quej__djwwl else uzlt__sfloq for uzlt__sfloq,
                quej__djwwl in zip(self.data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if ehvgf__dreoz is not None and None not in data:
                return DataFrameType(data, ehvgf__dreoz, self.columns, dist,
                    self.is_table_format)
        if isinstance(other, DataFrameType) and len(self.data
            ) == 0 and not self.has_runtime_cols:
            return other

    def can_convert_to(self, typingctx, other):
        from numba.core.typeconv import Conversion
        if (isinstance(other, DataFrameType) and self.data == other.data and
            self.index == other.index and self.columns == other.columns and
            self.dist != other.dist and self.has_runtime_cols == other.
            has_runtime_cols):
            return Conversion.safe

    def is_precise(self):
        return all(uzlt__sfloq.is_precise() for uzlt__sfloq in self.data
            ) and self.index.is_precise()

    def replace_col_type(self, col_name, new_type):
        if col_name not in self.columns:
            raise ValueError(
                f"DataFrameType.replace_col_type replaced column must be found in the DataFrameType. '{col_name}' not found in DataFrameType with columns {self.columns}"
                )
        fdckd__wpv = self.columns.index(col_name)
        num__gxhpi = tuple(list(self.data[:fdckd__wpv]) + [new_type] + list
            (self.data[fdckd__wpv + 1:]))
        return DataFrameType(num__gxhpi, self.index, self.columns, self.
            dist, self.is_table_format)


def check_runtime_cols_unsupported(df, func_name):
    if isinstance(df, DataFrameType) and df.has_runtime_cols:
        raise BodoError(
            f'{func_name} on DataFrames with columns determined at runtime is not yet supported. Please return the DataFrame to regular Python to update typing information.'
            )


class DataFramePayloadType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        super(DataFramePayloadType, self).__init__(name=
            f'DataFramePayloadType({df_type})')

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(DataFramePayloadType)
class DataFramePayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        data_typ = types.Tuple(fe_type.df_type.data)
        if fe_type.df_type.is_table_format:
            data_typ = types.Tuple([fe_type.df_type.table_type])
        bxqs__jslq = [('data', data_typ), ('index', fe_type.df_type.index),
            ('parent', types.pyobject)]
        if fe_type.df_type.has_runtime_cols:
            bxqs__jslq.append(('columns', fe_type.df_type.runtime_colname_typ))
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, bxqs__jslq)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        bxqs__jslq = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, bxqs__jslq)


make_attribute_wrapper(DataFrameType, 'meminfo', '_meminfo')


@infer_getattr
class DataFrameAttribute(OverloadedKeyAttributeTemplate):
    key = DataFrameType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])

    @bound_function('df.head')
    def resolve_head(self, df, args, kws):
        func_name = 'DataFrame.head'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        lepu__xcti = 'n',
        fktql__nghc = {'n': 5}
        vfdvn__bbdf, miz__adre = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, lepu__xcti, fktql__nghc)
        lxn__xdkh = miz__adre[0]
        if not is_overload_int(lxn__xdkh):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        iol__fvrgl = df.copy()
        return iol__fvrgl(*miz__adre).replace(pysig=vfdvn__bbdf)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        aoa__wxn = (df,) + args
        lepu__xcti = 'df', 'method', 'min_periods'
        fktql__nghc = {'method': 'pearson', 'min_periods': 1}
        tgzqd__rkq = 'method',
        vfdvn__bbdf, miz__adre = bodo.utils.typing.fold_typing_args(func_name,
            aoa__wxn, kws, lepu__xcti, fktql__nghc, tgzqd__rkq)
        irbme__qirt = miz__adre[2]
        if not is_overload_int(irbme__qirt):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        xkwf__rzoq = []
        ybo__osoj = []
        for crsf__qrtc, vywp__pyxx in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(vywp__pyxx.dtype):
                xkwf__rzoq.append(crsf__qrtc)
                ybo__osoj.append(types.Array(types.float64, 1, 'A'))
        if len(xkwf__rzoq) == 0:
            raise_bodo_error('DataFrame.corr(): requires non-empty dataframe')
        ybo__osoj = tuple(ybo__osoj)
        xkwf__rzoq = tuple(xkwf__rzoq)
        index_typ = bodo.utils.typing.type_col_to_index(xkwf__rzoq)
        iol__fvrgl = DataFrameType(ybo__osoj, index_typ, xkwf__rzoq)
        return iol__fvrgl(*miz__adre).replace(pysig=vfdvn__bbdf)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.apply()')
        kws = dict(kws)
        gqp__hkac = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        ysuit__qtui = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        ytw__jtg = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        kmkfv__rjgc = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        iiop__khrjj = dict(raw=ysuit__qtui, result_type=ytw__jtg)
        mdkkb__bwrwu = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', iiop__khrjj, mdkkb__bwrwu,
            package_name='pandas', module_name='DataFrame')
        finei__cws = True
        if types.unliteral(gqp__hkac) == types.unicode_type:
            if not is_overload_constant_str(gqp__hkac):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            finei__cws = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        wrpee__ccpe = get_overload_const_int(axis)
        if finei__cws and wrpee__ccpe != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif wrpee__ccpe not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        plde__wuie = []
        for arr_typ in df.data:
            lgjac__fkg = SeriesType(arr_typ.dtype, arr_typ, df.index,
                string_type)
            vccs__wqh = self.context.resolve_function_type(operator.getitem,
                (SeriesIlocType(lgjac__fkg), types.int64), {}).return_type
            plde__wuie.append(vccs__wqh)
        ynsh__nmzlb = types.none
        cpjro__tzu = HeterogeneousIndexType(types.BaseTuple.from_types(
            tuple(types.literal(crsf__qrtc) for crsf__qrtc in df.columns)),
            None)
        nim__qynbm = types.BaseTuple.from_types(plde__wuie)
        wcqq__xpb = types.Tuple([types.bool_] * len(nim__qynbm))
        iim__cmd = bodo.NullableTupleType(nim__qynbm, wcqq__xpb)
        xjzab__esoiw = df.index.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df.index,
            'DataFrame.apply()')
        if xjzab__esoiw == types.NPDatetime('ns'):
            xjzab__esoiw = bodo.pd_timestamp_type
        if xjzab__esoiw == types.NPTimedelta('ns'):
            xjzab__esoiw = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(nim__qynbm):
            pgcy__ulcw = HeterogeneousSeriesType(iim__cmd, cpjro__tzu,
                xjzab__esoiw)
        else:
            pgcy__ulcw = SeriesType(nim__qynbm.dtype, iim__cmd, cpjro__tzu,
                xjzab__esoiw)
        djew__mhr = pgcy__ulcw,
        if kmkfv__rjgc is not None:
            djew__mhr += tuple(kmkfv__rjgc.types)
        try:
            if not finei__cws:
                qwm__hrl = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(gqp__hkac), self.context,
                    'DataFrame.apply', axis if wrpee__ccpe == 1 else None)
            else:
                qwm__hrl = get_const_func_output_type(gqp__hkac, djew__mhr,
                    kws, self.context, numba.core.registry.cpu_target.
                    target_context)
        except Exception as qsaib__ggq:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()', qsaib__ggq)
                )
        if finei__cws:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(qwm__hrl, (SeriesType, HeterogeneousSeriesType)
                ) and qwm__hrl.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(qwm__hrl, HeterogeneousSeriesType):
                ihv__tvfw, aqq__rzw = qwm__hrl.const_info
                if isinstance(qwm__hrl.data, bodo.libs.nullable_tuple_ext.
                    NullableTupleType):
                    efpa__vbvx = qwm__hrl.data.tuple_typ.types
                elif isinstance(qwm__hrl.data, types.Tuple):
                    efpa__vbvx = qwm__hrl.data.types
                else:
                    raise_bodo_error(
                        'df.apply(): Unexpected Series return type for Heterogeneous data'
                        )
                cvy__kly = tuple(to_nullable_type(dtype_to_array_type(
                    kkpkq__ulfg)) for kkpkq__ulfg in efpa__vbvx)
                xgqlo__obl = DataFrameType(cvy__kly, df.index, aqq__rzw)
            elif isinstance(qwm__hrl, SeriesType):
                oym__zcprq, aqq__rzw = qwm__hrl.const_info
                cvy__kly = tuple(to_nullable_type(dtype_to_array_type(
                    qwm__hrl.dtype)) for ihv__tvfw in range(oym__zcprq))
                xgqlo__obl = DataFrameType(cvy__kly, df.index, aqq__rzw)
            else:
                ozp__kwdlc = get_udf_out_arr_type(qwm__hrl)
                xgqlo__obl = SeriesType(ozp__kwdlc.dtype, ozp__kwdlc, df.
                    index, None)
        else:
            xgqlo__obl = qwm__hrl
        ndn__uku = ', '.join("{} = ''".format(uzlt__sfloq) for uzlt__sfloq in
            kws.keys())
        zba__aggv = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {ndn__uku}):
"""
        zba__aggv += '    pass\n'
        nksvu__xjzdm = {}
        exec(zba__aggv, {}, nksvu__xjzdm)
        xvqx__acrjx = nksvu__xjzdm['apply_stub']
        vfdvn__bbdf = numba.core.utils.pysignature(xvqx__acrjx)
        sker__mdoe = (gqp__hkac, axis, ysuit__qtui, ytw__jtg, kmkfv__rjgc
            ) + tuple(kws.values())
        return signature(xgqlo__obl, *sker__mdoe).replace(pysig=vfdvn__bbdf)

    @bound_function('df.plot', no_unliteral=True)
    def resolve_plot(self, df, args, kws):
        func_name = 'DataFrame.plot'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        lepu__xcti = ('x', 'y', 'kind', 'figsize', 'ax', 'subplots',
            'sharex', 'sharey', 'layout', 'use_index', 'title', 'grid',
            'legend', 'style', 'logx', 'logy', 'loglog', 'xticks', 'yticks',
            'xlim', 'ylim', 'rot', 'fontsize', 'colormap', 'table', 'yerr',
            'xerr', 'secondary_y', 'sort_columns', 'xlabel', 'ylabel',
            'position', 'stacked', 'mark_right', 'include_bool', 'backend')
        fktql__nghc = {'x': None, 'y': None, 'kind': 'line', 'figsize':
            None, 'ax': None, 'subplots': False, 'sharex': None, 'sharey': 
            False, 'layout': None, 'use_index': True, 'title': None, 'grid':
            None, 'legend': True, 'style': None, 'logx': False, 'logy': 
            False, 'loglog': False, 'xticks': None, 'yticks': None, 'xlim':
            None, 'ylim': None, 'rot': None, 'fontsize': None, 'colormap':
            None, 'table': False, 'yerr': None, 'xerr': None, 'secondary_y':
            False, 'sort_columns': False, 'xlabel': None, 'ylabel': None,
            'position': 0.5, 'stacked': False, 'mark_right': True,
            'include_bool': False, 'backend': None}
        tgzqd__rkq = ('subplots', 'sharex', 'sharey', 'layout', 'use_index',
            'grid', 'style', 'logx', 'logy', 'loglog', 'xlim', 'ylim',
            'rot', 'colormap', 'table', 'yerr', 'xerr', 'sort_columns',
            'secondary_y', 'colorbar', 'position', 'stacked', 'mark_right',
            'include_bool', 'backend')
        vfdvn__bbdf, miz__adre = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, lepu__xcti, fktql__nghc, tgzqd__rkq)
        hlok__sjohr = miz__adre[2]
        if not is_overload_constant_str(hlok__sjohr):
            raise BodoError(
                f"{func_name}: kind must be a constant string and one of ('line', 'scatter')."
                )
        gbzw__dui = miz__adre[0]
        if not is_overload_none(gbzw__dui) and not (is_overload_int(
            gbzw__dui) or is_overload_constant_str(gbzw__dui)):
            raise BodoError(
                f'{func_name}: x must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(gbzw__dui):
            scf__atgbt = get_overload_const_str(gbzw__dui)
            if scf__atgbt not in df.columns:
                raise BodoError(f'{func_name}: {scf__atgbt} column not found.')
        elif is_overload_int(gbzw__dui):
            xbn__zcmh = get_overload_const_int(gbzw__dui)
            if xbn__zcmh > len(df.columns):
                raise BodoError(
                    f'{func_name}: x: {xbn__zcmh} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            gbzw__dui = df.columns[gbzw__dui]
        yoxb__mcqr = miz__adre[1]
        if not is_overload_none(yoxb__mcqr) and not (is_overload_int(
            yoxb__mcqr) or is_overload_constant_str(yoxb__mcqr)):
            raise BodoError(
                'df.plot(): y must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(yoxb__mcqr):
            qtoa__jjtvl = get_overload_const_str(yoxb__mcqr)
            if qtoa__jjtvl not in df.columns:
                raise BodoError(f'{func_name}: {qtoa__jjtvl} column not found.'
                    )
        elif is_overload_int(yoxb__mcqr):
            avwo__mht = get_overload_const_int(yoxb__mcqr)
            if avwo__mht > len(df.columns):
                raise BodoError(
                    f'{func_name}: y: {avwo__mht} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            yoxb__mcqr = df.columns[yoxb__mcqr]
        lhin__iwbg = miz__adre[3]
        if not is_overload_none(lhin__iwbg) and not is_tuple_like_type(
            lhin__iwbg):
            raise BodoError(
                f'{func_name}: figsize must be a constant numeric tuple (width, height) or None.'
                )
        lcxoe__brix = miz__adre[10]
        if not is_overload_none(lcxoe__brix) and not is_overload_constant_str(
            lcxoe__brix):
            raise BodoError(
                f'{func_name}: title must be a constant string or None.')
        zhfiq__tczua = miz__adre[12]
        if not is_overload_bool(zhfiq__tczua):
            raise BodoError(f'{func_name}: legend must be a boolean type.')
        aig__wbv = miz__adre[17]
        if not is_overload_none(aig__wbv) and not is_tuple_like_type(aig__wbv):
            raise BodoError(
                f'{func_name}: xticks must be a constant tuple or None.')
        zfhbk__zchjq = miz__adre[18]
        if not is_overload_none(zfhbk__zchjq) and not is_tuple_like_type(
            zfhbk__zchjq):
            raise BodoError(
                f'{func_name}: yticks must be a constant tuple or None.')
        iye__rkjj = miz__adre[22]
        if not is_overload_none(iye__rkjj) and not is_overload_int(iye__rkjj):
            raise BodoError(
                f'{func_name}: fontsize must be an integer or None.')
        iijt__cbndv = miz__adre[29]
        if not is_overload_none(iijt__cbndv) and not is_overload_constant_str(
            iijt__cbndv):
            raise BodoError(
                f'{func_name}: xlabel must be a constant string or None.')
        etsco__txb = miz__adre[30]
        if not is_overload_none(etsco__txb) and not is_overload_constant_str(
            etsco__txb):
            raise BodoError(
                f'{func_name}: ylabel must be a constant string or None.')
        jwk__osb = types.List(types.mpl_line_2d_type)
        hlok__sjohr = get_overload_const_str(hlok__sjohr)
        if hlok__sjohr == 'scatter':
            if is_overload_none(gbzw__dui) and is_overload_none(yoxb__mcqr):
                raise BodoError(
                    f'{func_name}: {hlok__sjohr} requires an x and y column.')
            elif is_overload_none(gbzw__dui):
                raise BodoError(
                    f'{func_name}: {hlok__sjohr} x column is missing.')
            elif is_overload_none(yoxb__mcqr):
                raise BodoError(
                    f'{func_name}: {hlok__sjohr} y column is missing.')
            jwk__osb = types.mpl_path_collection_type
        elif hlok__sjohr != 'line':
            raise BodoError(
                f'{func_name}: {hlok__sjohr} plot is not supported.')
        return signature(jwk__osb, *miz__adre).replace(pysig=vfdvn__bbdf)

    def generic_resolve(self, df, attr):
        if self._is_existing_attr(attr):
            return
        check_runtime_cols_unsupported(df,
            'Acessing DataFrame columns by attribute')
        if attr in df.columns:
            zwtkh__lfp = df.columns.index(attr)
            arr_typ = df.data[zwtkh__lfp]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            uwuw__hmx = []
            num__gxhpi = []
            ngu__zqwr = False
            for i, yar__rvbfp in enumerate(df.columns):
                if yar__rvbfp[0] != attr:
                    continue
                ngu__zqwr = True
                uwuw__hmx.append(yar__rvbfp[1] if len(yar__rvbfp) == 2 else
                    yar__rvbfp[1:])
                num__gxhpi.append(df.data[i])
            if ngu__zqwr:
                return DataFrameType(tuple(num__gxhpi), df.index, tuple(
                    uwuw__hmx))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        bnot__pukq = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(bnot__pukq)
        return lambda tup, idx: tup[val_ind]


def decref_df_data(context, builder, payload, df_type):
    if df_type.is_table_format:
        context.nrt.decref(builder, df_type.table_type, builder.
            extract_value(payload.data, 0))
        context.nrt.decref(builder, df_type.index, payload.index)
        if df_type.has_runtime_cols:
            context.nrt.decref(builder, df_type.data[-1], payload.columns)
        return
    for i in range(len(df_type.data)):
        mwir__kbyx = builder.extract_value(payload.data, i)
        context.nrt.decref(builder, df_type.data[i], mwir__kbyx)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    vii__jjm = builder.module
    xkhvc__sdf = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    bfe__byge = cgutils.get_or_insert_function(vii__jjm, xkhvc__sdf, name=
        '.dtor.df.{}'.format(df_type))
    if not bfe__byge.is_declaration:
        return bfe__byge
    bfe__byge.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(bfe__byge.append_basic_block())
    unodu__lhev = bfe__byge.args[0]
    yjt__euaxm = context.get_value_type(payload_type).as_pointer()
    fsvxx__iilr = builder.bitcast(unodu__lhev, yjt__euaxm)
    payload = context.make_helper(builder, payload_type, ref=fsvxx__iilr)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        mjx__zsmt = context.get_python_api(builder)
        evw__wsgs = mjx__zsmt.gil_ensure()
        mjx__zsmt.decref(payload.parent)
        mjx__zsmt.gil_release(evw__wsgs)
    builder.ret_void()
    return bfe__byge


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    parent=None, colnames=None):
    payload_type = DataFramePayloadType(df_type)
    bozgl__dvs = cgutils.create_struct_proxy(payload_type)(context, builder)
    bozgl__dvs.data = data_tup
    bozgl__dvs.index = index_val
    if colnames is not None:
        assert df_type.has_runtime_cols, 'construct_dataframe can only provide colnames if columns are determined at runtime'
        bozgl__dvs.columns = colnames
    jpy__ypul = context.get_value_type(payload_type)
    ugwt__knxv = context.get_abi_sizeof(jpy__ypul)
    wrq__skqly = define_df_dtor(context, builder, df_type, payload_type)
    duss__oxm = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, ugwt__knxv), wrq__skqly)
    wuimm__csv = context.nrt.meminfo_data(builder, duss__oxm)
    cjqtf__igzj = builder.bitcast(wuimm__csv, jpy__ypul.as_pointer())
    pajyn__zpxq = cgutils.create_struct_proxy(df_type)(context, builder)
    pajyn__zpxq.meminfo = duss__oxm
    if parent is None:
        pajyn__zpxq.parent = cgutils.get_null_value(pajyn__zpxq.parent.type)
    else:
        pajyn__zpxq.parent = parent
        bozgl__dvs.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            mjx__zsmt = context.get_python_api(builder)
            evw__wsgs = mjx__zsmt.gil_ensure()
            mjx__zsmt.incref(parent)
            mjx__zsmt.gil_release(evw__wsgs)
    builder.store(bozgl__dvs._getvalue(), cjqtf__igzj)
    return pajyn__zpxq._getvalue()


@intrinsic
def init_runtime_cols_dataframe(typingctx, data_typ, index_typ,
    colnames_index_typ=None):
    assert isinstance(data_typ, types.BaseTuple) and isinstance(data_typ.
        dtype, TableType
        ) and data_typ.dtype.has_runtime_cols, 'init_runtime_cols_dataframe must be called with a table that determines columns at runtime.'
    assert bodo.hiframes.pd_index_ext.is_pd_index_type(colnames_index_typ
        ) or isinstance(colnames_index_typ, bodo.hiframes.
        pd_multi_index_ext.MultiIndexType), 'Column names must be an index'
    if isinstance(data_typ.dtype.arr_types, types.UniTuple):
        ailu__mequw = [data_typ.dtype.arr_types.dtype] * len(data_typ.dtype
            .arr_types)
    else:
        ailu__mequw = [kkpkq__ulfg for kkpkq__ulfg in data_typ.dtype.arr_types]
    ohh__ery = DataFrameType(tuple(ailu__mequw + [colnames_index_typ]),
        index_typ, None, is_table_format=True)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup, index, col_names = args
        parent = None
        xzmx__dju = construct_dataframe(context, builder, df_type, data_tup,
            index, parent, col_names)
        context.nrt.incref(builder, data_typ, data_tup)
        context.nrt.incref(builder, index_typ, index)
        context.nrt.incref(builder, colnames_index_typ, col_names)
        return xzmx__dju
    sig = signature(ohh__ery, data_typ, index_typ, colnames_index_typ)
    return sig, codegen


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    oym__zcprq = len(data_tup_typ.types)
    if oym__zcprq == 0:
        column_names = ()
    lja__tpyn = col_names_typ.instance_type if isinstance(col_names_typ,
        types.TypeRef) else col_names_typ
    assert isinstance(lja__tpyn, ColNamesMetaType) and isinstance(lja__tpyn
        .meta, tuple
        ), 'Third argument to init_dataframe must be of type ColNamesMetaType, and must contain a tuple of column names'
    column_names = lja__tpyn.meta
    if oym__zcprq == 1 and isinstance(data_tup_typ.types[0], TableType):
        oym__zcprq = len(data_tup_typ.types[0].arr_types)
    assert len(column_names
        ) == oym__zcprq, 'init_dataframe(): number of column names does not match number of columns'
    is_table_format = False
    kdl__vvq = data_tup_typ.types
    if oym__zcprq != 0 and isinstance(data_tup_typ.types[0], TableType):
        kdl__vvq = data_tup_typ.types[0].arr_types
        is_table_format = True
    ohh__ery = DataFrameType(kdl__vvq, index_typ, column_names,
        is_table_format=is_table_format)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        parent = None
        if is_table_format:
            xtu__xwcdf = cgutils.create_struct_proxy(ohh__ery.table_type)(
                context, builder, builder.extract_value(data_tup, 0))
            parent = xtu__xwcdf.parent
        xzmx__dju = construct_dataframe(context, builder, df_type, data_tup,
            index_val, parent, None)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return xzmx__dju
    sig = signature(ohh__ery, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):
    check_runtime_cols_unsupported(df, 'has_parent')

    def codegen(context, builder, sig, args):
        pajyn__zpxq = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, pajyn__zpxq.parent)
    return signature(types.bool_, df), codegen


@intrinsic
def _column_needs_unboxing(typingctx, df_typ, i_typ=None):
    check_runtime_cols_unsupported(df_typ, '_column_needs_unboxing')
    assert isinstance(df_typ, DataFrameType) and is_overload_constant_int(i_typ
        )

    def codegen(context, builder, sig, args):
        bozgl__dvs = get_dataframe_payload(context, builder, df_typ, args[0])
        ilspw__fmacu = get_overload_const_int(i_typ)
        arr_typ = df_typ.data[ilspw__fmacu]
        if df_typ.is_table_format:
            xtu__xwcdf = cgutils.create_struct_proxy(df_typ.table_type)(context
                , builder, builder.extract_value(bozgl__dvs.data, 0))
            jmvm__ajecq = df_typ.table_type.type_to_blk[arr_typ]
            auoe__eston = getattr(xtu__xwcdf, f'block_{jmvm__ajecq}')
            qxvty__zwzru = ListInstance(context, builder, types.List(
                arr_typ), auoe__eston)
            qni__qvp = context.get_constant(types.int64, df_typ.table_type.
                block_offsets[ilspw__fmacu])
            mwir__kbyx = qxvty__zwzru.getitem(qni__qvp)
        else:
            mwir__kbyx = builder.extract_value(bozgl__dvs.data, ilspw__fmacu)
        wdnrw__rttg = cgutils.alloca_once_value(builder, mwir__kbyx)
        wfcu__ymbyv = cgutils.alloca_once_value(builder, context.
            get_constant_null(arr_typ))
        return is_ll_eq(builder, wdnrw__rttg, wfcu__ymbyv)
    return signature(types.bool_, df_typ, i_typ), codegen


def get_dataframe_payload(context, builder, df_type, value):
    duss__oxm = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, duss__oxm)
    yjt__euaxm = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, yjt__euaxm)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, '_get_dataframe_data')
    ohh__ery = types.Tuple(df_typ.data)
    if df_typ.is_table_format:
        ohh__ery = types.Tuple([TableType(df_typ.data)])
    sig = signature(ohh__ery, df_typ)

    def codegen(context, builder, signature, args):
        bozgl__dvs = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            bozgl__dvs.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):

    def codegen(context, builder, signature, args):
        bozgl__dvs = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index, bozgl__dvs
            .index)
    ohh__ery = df_typ.index
    sig = signature(ohh__ery, df_typ)
    return sig, codegen


def get_dataframe_data(df, i):
    return df[i]


@infer_global(get_dataframe_data)
class GetDataFrameDataInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        if not is_overload_constant_int(args[1]):
            raise_bodo_error(
                'Selecting a DataFrame column requires a constant column label'
                )
        df = args[0]
        check_runtime_cols_unsupported(df, 'get_dataframe_data')
        i = get_overload_const_int(args[1])
        iol__fvrgl = df.data[i]
        return iol__fvrgl(*args)


GetDataFrameDataInfer.prefer_literal = True


def get_dataframe_data_impl(df, i):
    if df.is_table_format:

        def _impl(df, i):
            if has_parent(df) and _column_needs_unboxing(df, i):
                bodo.hiframes.boxing.unbox_dataframe_column(df, i)
            return get_table_data(_get_dataframe_data(df)[0], i)
        return _impl

    def _impl(df, i):
        if has_parent(df) and _column_needs_unboxing(df, i):
            bodo.hiframes.boxing.unbox_dataframe_column(df, i)
        return _get_dataframe_data(df)[i]
    return _impl


@intrinsic
def get_dataframe_table(typingctx, df_typ=None):
    assert df_typ.is_table_format, 'get_dataframe_table() expects table format'

    def codegen(context, builder, signature, args):
        bozgl__dvs = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.table_type,
            builder.extract_value(bozgl__dvs.data, 0))
    return df_typ.table_type(df_typ), codegen


def get_dataframe_all_data(df):
    return df.data


def get_dataframe_all_data_impl(df):
    if df.is_table_format:

        def _impl(df):
            return get_dataframe_table(df)
        return _impl
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for i in
        range(len(df.columns)))
    dfxm__njkgx = ',' if len(df.columns) > 1 else ''
    return eval(f'lambda df: ({data}{dfxm__njkgx})', {'bodo': bodo})


@infer_global(get_dataframe_all_data)
class GetDataFrameAllDataInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        df_type = args[0]
        check_runtime_cols_unsupported(df_type, 'get_dataframe_data')
        iol__fvrgl = (df_type.table_type if df_type.is_table_format else
            types.BaseTuple.from_types(df_type.data))
        return iol__fvrgl(*args)


@lower_builtin(get_dataframe_all_data, DataFrameType)
def lower_get_dataframe_all_data(context, builder, sig, args):
    impl = get_dataframe_all_data_impl(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@intrinsic
def get_dataframe_column_names(typingctx, df_typ=None):
    assert df_typ.has_runtime_cols, 'get_dataframe_column_names() expects columns to be determined at runtime'

    def codegen(context, builder, signature, args):
        bozgl__dvs = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.
            runtime_colname_typ, bozgl__dvs.columns)
    return df_typ.runtime_colname_typ(df_typ), codegen


@lower_builtin(get_dataframe_data, DataFrameType, types.IntegerLiteral)
def lower_get_dataframe_data(context, builder, sig, args):
    impl = get_dataframe_data_impl(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_dataframe_data',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_index',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_table',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_all_data',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func


def alias_ext_init_dataframe(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 3
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_dataframe',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_init_dataframe


def init_dataframe_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 3 and not kws
    data_tup = args[0]
    index = args[1]
    nim__qynbm = self.typemap[data_tup.name]
    if any(is_tuple_like_type(kkpkq__ulfg) for kkpkq__ulfg in nim__qynbm.types
        ):
        return None
    if equiv_set.has_shape(data_tup):
        epeg__bewc = equiv_set.get_shape(data_tup)
        if len(epeg__bewc) > 1:
            equiv_set.insert_equiv(*epeg__bewc)
        if len(epeg__bewc) > 0:
            cpjro__tzu = self.typemap[index.name]
            if not isinstance(cpjro__tzu, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(epeg__bewc[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(epeg__bewc[0], len(
                epeg__bewc)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    elp__emum = args[0]
    data_types = self.typemap[elp__emum.name].data
    if any(is_tuple_like_type(kkpkq__ulfg) for kkpkq__ulfg in data_types):
        return None
    if equiv_set.has_shape(elp__emum):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            elp__emum)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    elp__emum = args[0]
    cpjro__tzu = self.typemap[elp__emum.name].index
    if isinstance(cpjro__tzu, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(elp__emum):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            elp__emum)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


def get_dataframe_table_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    elp__emum = args[0]
    if equiv_set.has_shape(elp__emum):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            elp__emum), pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_table
    ) = get_dataframe_table_equiv


def get_dataframe_column_names_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    elp__emum = args[0]
    if equiv_set.has_shape(elp__emum):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            elp__emum)[1], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_column_names
    ) = get_dataframe_column_names_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    check_runtime_cols_unsupported(df_typ, 'set_dataframe_data')
    assert is_overload_constant_int(c_ind_typ)
    ilspw__fmacu = get_overload_const_int(c_ind_typ)
    if df_typ.data[ilspw__fmacu] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        nzhvs__ofz, ihv__tvfw, jybjn__ddcn = args
        bozgl__dvs = get_dataframe_payload(context, builder, df_typ, nzhvs__ofz
            )
        if df_typ.is_table_format:
            xtu__xwcdf = cgutils.create_struct_proxy(df_typ.table_type)(context
                , builder, builder.extract_value(bozgl__dvs.data, 0))
            jmvm__ajecq = df_typ.table_type.type_to_blk[arr_typ]
            auoe__eston = getattr(xtu__xwcdf, f'block_{jmvm__ajecq}')
            qxvty__zwzru = ListInstance(context, builder, types.List(
                arr_typ), auoe__eston)
            qni__qvp = context.get_constant(types.int64, df_typ.table_type.
                block_offsets[ilspw__fmacu])
            qxvty__zwzru.setitem(qni__qvp, jybjn__ddcn, True)
        else:
            mwir__kbyx = builder.extract_value(bozgl__dvs.data, ilspw__fmacu)
            context.nrt.decref(builder, df_typ.data[ilspw__fmacu], mwir__kbyx)
            bozgl__dvs.data = builder.insert_value(bozgl__dvs.data,
                jybjn__ddcn, ilspw__fmacu)
            context.nrt.incref(builder, arr_typ, jybjn__ddcn)
        pajyn__zpxq = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=nzhvs__ofz)
        payload_type = DataFramePayloadType(df_typ)
        fsvxx__iilr = context.nrt.meminfo_data(builder, pajyn__zpxq.meminfo)
        yjt__euaxm = context.get_value_type(payload_type).as_pointer()
        fsvxx__iilr = builder.bitcast(fsvxx__iilr, yjt__euaxm)
        builder.store(bozgl__dvs._getvalue(), fsvxx__iilr)
        return impl_ret_borrowed(context, builder, df_typ, nzhvs__ofz)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):
    check_runtime_cols_unsupported(df_t, 'set_df_index')

    def codegen(context, builder, signature, args):
        voof__hlmc = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        kpl__dda = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=voof__hlmc)
        hiii__jqcjq = get_dataframe_payload(context, builder, df_typ,
            voof__hlmc)
        pajyn__zpxq = construct_dataframe(context, builder, signature.
            return_type, hiii__jqcjq.data, index_val, kpl__dda.parent, None)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), hiii__jqcjq.data)
        return pajyn__zpxq
    ohh__ery = DataFrameType(df_t.data, index_t, df_t.columns, df_t.dist,
        df_t.is_table_format)
    sig = signature(ohh__ery, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    check_runtime_cols_unsupported(df_type, 'set_df_column_with_reflect')
    assert is_literal_type(cname_type), 'constant column name expected'
    col_name = get_literal_value(cname_type)
    oym__zcprq = len(df_type.columns)
    cxyg__bewlo = oym__zcprq
    fwo__zaca = df_type.data
    column_names = df_type.columns
    index_typ = df_type.index
    mobr__quak = col_name not in df_type.columns
    ilspw__fmacu = oym__zcprq
    if mobr__quak:
        fwo__zaca += arr_type,
        column_names += col_name,
        cxyg__bewlo += 1
    else:
        ilspw__fmacu = df_type.columns.index(col_name)
        fwo__zaca = tuple(arr_type if i == ilspw__fmacu else fwo__zaca[i] for
            i in range(oym__zcprq))

    def codegen(context, builder, signature, args):
        nzhvs__ofz, ihv__tvfw, jybjn__ddcn = args
        in_dataframe_payload = get_dataframe_payload(context, builder,
            df_type, nzhvs__ofz)
        eqa__dugxw = cgutils.create_struct_proxy(df_type)(context, builder,
            value=nzhvs__ofz)
        if df_type.is_table_format:
            reh__sdo = df_type.table_type
            cjgkm__fpp = builder.extract_value(in_dataframe_payload.data, 0)
            jbks__dbku = TableType(fwo__zaca)
            awry__nhrd = set_table_data_codegen(context, builder, reh__sdo,
                cjgkm__fpp, jbks__dbku, arr_type, jybjn__ddcn, ilspw__fmacu,
                mobr__quak)
            data_tup = context.make_tuple(builder, types.Tuple([jbks__dbku]
                ), [awry__nhrd])
        else:
            kdl__vvq = [(builder.extract_value(in_dataframe_payload.data, i
                ) if i != ilspw__fmacu else jybjn__ddcn) for i in range(
                oym__zcprq)]
            if mobr__quak:
                kdl__vvq.append(jybjn__ddcn)
            for elp__emum, uva__rng in zip(kdl__vvq, fwo__zaca):
                context.nrt.incref(builder, uva__rng, elp__emum)
            data_tup = context.make_tuple(builder, types.Tuple(fwo__zaca),
                kdl__vvq)
        index_val = in_dataframe_payload.index
        context.nrt.incref(builder, index_typ, index_val)
        pwtfj__imrv = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, eqa__dugxw.parent, None)
        if not mobr__quak and arr_type == df_type.data[ilspw__fmacu]:
            decref_df_data(context, builder, in_dataframe_payload, df_type)
            payload_type = DataFramePayloadType(df_type)
            fsvxx__iilr = context.nrt.meminfo_data(builder, eqa__dugxw.meminfo)
            yjt__euaxm = context.get_value_type(payload_type).as_pointer()
            fsvxx__iilr = builder.bitcast(fsvxx__iilr, yjt__euaxm)
            ojpe__edtna = get_dataframe_payload(context, builder, df_type,
                pwtfj__imrv)
            builder.store(ojpe__edtna._getvalue(), fsvxx__iilr)
            context.nrt.incref(builder, index_typ, index_val)
            if df_type.is_table_format:
                context.nrt.incref(builder, jbks__dbku, builder.
                    extract_value(data_tup, 0))
            else:
                for elp__emum, uva__rng in zip(kdl__vvq, fwo__zaca):
                    context.nrt.incref(builder, uva__rng, elp__emum)
        has_parent = cgutils.is_not_null(builder, eqa__dugxw.parent)
        with builder.if_then(has_parent):
            mjx__zsmt = context.get_python_api(builder)
            evw__wsgs = mjx__zsmt.gil_ensure()
            tfkp__qdoj = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, jybjn__ddcn)
            crsf__qrtc = numba.core.pythonapi._BoxContext(context, builder,
                mjx__zsmt, tfkp__qdoj)
            obvfi__rnack = crsf__qrtc.pyapi.from_native_value(arr_type,
                jybjn__ddcn, crsf__qrtc.env_manager)
            if isinstance(col_name, str):
                lut__wif = context.insert_const_string(builder.module, col_name
                    )
                lgay__rhca = mjx__zsmt.string_from_string(lut__wif)
            else:
                assert isinstance(col_name, int)
                lgay__rhca = mjx__zsmt.long_from_longlong(context.
                    get_constant(types.intp, col_name))
            mjx__zsmt.object_setitem(eqa__dugxw.parent, lgay__rhca,
                obvfi__rnack)
            mjx__zsmt.decref(obvfi__rnack)
            mjx__zsmt.decref(lgay__rhca)
            mjx__zsmt.gil_release(evw__wsgs)
        return pwtfj__imrv
    ohh__ery = DataFrameType(fwo__zaca, index_typ, column_names, df_type.
        dist, df_type.is_table_format)
    sig = signature(ohh__ery, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    check_runtime_cols_unsupported(df_type, 'lowering a constant DataFrame')
    oym__zcprq = len(pyval.columns)
    kdl__vvq = []
    for i in range(oym__zcprq):
        rjulu__wwz = pyval.iloc[:, i]
        if isinstance(df_type.data[i], bodo.DatetimeArrayType):
            obvfi__rnack = rjulu__wwz.array
        else:
            obvfi__rnack = rjulu__wwz.values
        kdl__vvq.append(obvfi__rnack)
    kdl__vvq = tuple(kdl__vvq)
    if df_type.is_table_format:
        xtu__xwcdf = context.get_constant_generic(builder, df_type.
            table_type, Table(kdl__vvq))
        data_tup = lir.Constant.literal_struct([xtu__xwcdf])
    else:
        data_tup = lir.Constant.literal_struct([context.
            get_constant_generic(builder, df_type.data[i], yar__rvbfp) for 
            i, yar__rvbfp in enumerate(kdl__vvq)])
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    lzga__dfjo = context.get_constant_null(types.pyobject)
    payload = lir.Constant.literal_struct([data_tup, index_val, lzga__dfjo])
    payload = cgutils.global_constant(builder, '.const.payload', payload
        ).bitcast(cgutils.voidptr_t)
    dcvk__uvhpf = context.get_constant(types.int64, -1)
    sazo__judpv = context.get_constant_null(types.voidptr)
    duss__oxm = lir.Constant.literal_struct([dcvk__uvhpf, sazo__judpv,
        sazo__judpv, payload, dcvk__uvhpf])
    duss__oxm = cgutils.global_constant(builder, '.const.meminfo', duss__oxm
        ).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([duss__oxm, lzga__dfjo])


@lower_cast(DataFrameType, DataFrameType)
def cast_df_to_df(context, builder, fromty, toty, val):
    if (fromty.data == toty.data and fromty.index == toty.index and fromty.
        columns == toty.columns and fromty.is_table_format == toty.
        is_table_format and fromty.dist != toty.dist and fromty.
        has_runtime_cols == toty.has_runtime_cols):
        return val
    if not fromty.has_runtime_cols and not toty.has_runtime_cols and len(fromty
        .data) == 0 and len(toty.columns):
        return _cast_empty_df(context, builder, toty)
    if len(fromty.data) != len(toty.data) or fromty.data != toty.data and any(
        context.typing_context.unify_pairs(fromty.data[i], toty.data[i]) is
        None for i in range(len(fromty.data))
        ) or fromty.has_runtime_cols != toty.has_runtime_cols:
        raise BodoError(f'Invalid dataframe cast from {fromty} to {toty}')
    in_dataframe_payload = get_dataframe_payload(context, builder, fromty, val)
    if isinstance(fromty.index, RangeIndexType) and isinstance(toty.index,
        NumericIndexType):
        ehvgf__dreoz = context.cast(builder, in_dataframe_payload.index,
            fromty.index, toty.index)
    else:
        ehvgf__dreoz = in_dataframe_payload.index
        context.nrt.incref(builder, fromty.index, ehvgf__dreoz)
    if (fromty.is_table_format == toty.is_table_format and fromty.data ==
        toty.data):
        num__gxhpi = in_dataframe_payload.data
        if fromty.is_table_format:
            context.nrt.incref(builder, types.Tuple([fromty.table_type]),
                num__gxhpi)
        else:
            context.nrt.incref(builder, types.BaseTuple.from_types(fromty.
                data), num__gxhpi)
    elif not fromty.is_table_format and toty.is_table_format:
        num__gxhpi = _cast_df_data_to_table_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and not toty.is_table_format:
        num__gxhpi = _cast_df_data_to_tuple_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and toty.is_table_format:
        num__gxhpi = _cast_df_data_keep_table_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    else:
        num__gxhpi = _cast_df_data_keep_tuple_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    return construct_dataframe(context, builder, toty, num__gxhpi,
        ehvgf__dreoz, in_dataframe_payload.parent, None)


def _cast_empty_df(context, builder, toty):
    hqlfe__gdxg = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        hfj__mtg = get_index_data_arr_types(toty.index)[0]
        uwkvu__oamr = bodo.utils.transform.get_type_alloc_counts(hfj__mtg) - 1
        tstvl__nzos = ', '.join('0' for ihv__tvfw in range(uwkvu__oamr))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(tstvl__nzos, ', ' if uwkvu__oamr == 1 else ''))
        hqlfe__gdxg['index_arr_type'] = hfj__mtg
    ealuq__bnlc = []
    for i, arr_typ in enumerate(toty.data):
        uwkvu__oamr = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        tstvl__nzos = ', '.join('0' for ihv__tvfw in range(uwkvu__oamr))
        hnmu__ihov = ('bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'.
            format(i, tstvl__nzos, ', ' if uwkvu__oamr == 1 else ''))
        ealuq__bnlc.append(hnmu__ihov)
        hqlfe__gdxg[f'arr_type{i}'] = arr_typ
    ealuq__bnlc = ', '.join(ealuq__bnlc)
    zba__aggv = 'def impl():\n'
    ezt__qkumi = bodo.hiframes.dataframe_impl._gen_init_df(zba__aggv, toty.
        columns, ealuq__bnlc, index, hqlfe__gdxg)
    df = context.compile_internal(builder, ezt__qkumi, toty(), [])
    return df


def _cast_df_data_to_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame to table format')
    kzl__wcqc = toty.table_type
    xtu__xwcdf = cgutils.create_struct_proxy(kzl__wcqc)(context, builder)
    xtu__xwcdf.parent = in_dataframe_payload.parent
    for kkpkq__ulfg, jmvm__ajecq in kzl__wcqc.type_to_blk.items():
        pxtt__kqc = context.get_constant(types.int64, len(kzl__wcqc.
            block_to_arr_ind[jmvm__ajecq]))
        ihv__tvfw, rkn__hrx = ListInstance.allocate_ex(context, builder,
            types.List(kkpkq__ulfg), pxtt__kqc)
        rkn__hrx.size = pxtt__kqc
        setattr(xtu__xwcdf, f'block_{jmvm__ajecq}', rkn__hrx.value)
    for i, kkpkq__ulfg in enumerate(fromty.data):
        xno__cktjy = toty.data[i]
        if kkpkq__ulfg != xno__cktjy:
            obrqa__ngiyr = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*obrqa__ngiyr)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        mwir__kbyx = builder.extract_value(in_dataframe_payload.data, i)
        if kkpkq__ulfg != xno__cktjy:
            jhpam__zyak = context.cast(builder, mwir__kbyx, kkpkq__ulfg,
                xno__cktjy)
            awz__onwf = False
        else:
            jhpam__zyak = mwir__kbyx
            awz__onwf = True
        jmvm__ajecq = kzl__wcqc.type_to_blk[kkpkq__ulfg]
        auoe__eston = getattr(xtu__xwcdf, f'block_{jmvm__ajecq}')
        qxvty__zwzru = ListInstance(context, builder, types.List(
            kkpkq__ulfg), auoe__eston)
        qni__qvp = context.get_constant(types.int64, kzl__wcqc.block_offsets[i]
            )
        qxvty__zwzru.setitem(qni__qvp, jhpam__zyak, awz__onwf)
    data_tup = context.make_tuple(builder, types.Tuple([kzl__wcqc]), [
        xtu__xwcdf._getvalue()])
    return data_tup


def _cast_df_data_keep_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame columns')
    kdl__vvq = []
    for i in range(len(fromty.data)):
        if fromty.data[i] != toty.data[i]:
            obrqa__ngiyr = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*obrqa__ngiyr)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
            mwir__kbyx = builder.extract_value(in_dataframe_payload.data, i)
            jhpam__zyak = context.cast(builder, mwir__kbyx, fromty.data[i],
                toty.data[i])
            awz__onwf = False
        else:
            jhpam__zyak = builder.extract_value(in_dataframe_payload.data, i)
            awz__onwf = True
        if awz__onwf:
            context.nrt.incref(builder, toty.data[i], jhpam__zyak)
        kdl__vvq.append(jhpam__zyak)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), kdl__vvq)
    return data_tup


def _cast_df_data_keep_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting table format DataFrame columns')
    reh__sdo = fromty.table_type
    cjgkm__fpp = cgutils.create_struct_proxy(reh__sdo)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    jbks__dbku = toty.table_type
    awry__nhrd = cgutils.create_struct_proxy(jbks__dbku)(context, builder)
    awry__nhrd.parent = in_dataframe_payload.parent
    for kkpkq__ulfg, jmvm__ajecq in jbks__dbku.type_to_blk.items():
        pxtt__kqc = context.get_constant(types.int64, len(jbks__dbku.
            block_to_arr_ind[jmvm__ajecq]))
        ihv__tvfw, rkn__hrx = ListInstance.allocate_ex(context, builder,
            types.List(kkpkq__ulfg), pxtt__kqc)
        rkn__hrx.size = pxtt__kqc
        setattr(awry__nhrd, f'block_{jmvm__ajecq}', rkn__hrx.value)
    for i in range(len(fromty.data)):
        uvdqb__ghl = fromty.data[i]
        xno__cktjy = toty.data[i]
        if uvdqb__ghl != xno__cktjy:
            obrqa__ngiyr = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*obrqa__ngiyr)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        yrlno__giaf = reh__sdo.type_to_blk[uvdqb__ghl]
        gnrxx__wne = getattr(cjgkm__fpp, f'block_{yrlno__giaf}')
        boqxd__wcz = ListInstance(context, builder, types.List(uvdqb__ghl),
            gnrxx__wne)
        hdnh__itxuf = context.get_constant(types.int64, reh__sdo.
            block_offsets[i])
        mwir__kbyx = boqxd__wcz.getitem(hdnh__itxuf)
        if uvdqb__ghl != xno__cktjy:
            jhpam__zyak = context.cast(builder, mwir__kbyx, uvdqb__ghl,
                xno__cktjy)
            awz__onwf = False
        else:
            jhpam__zyak = mwir__kbyx
            awz__onwf = True
        zqfj__mgrm = jbks__dbku.type_to_blk[kkpkq__ulfg]
        rkn__hrx = getattr(awry__nhrd, f'block_{zqfj__mgrm}')
        zaepx__rziz = ListInstance(context, builder, types.List(xno__cktjy),
            rkn__hrx)
        nbtl__pprd = context.get_constant(types.int64, jbks__dbku.
            block_offsets[i])
        zaepx__rziz.setitem(nbtl__pprd, jhpam__zyak, awz__onwf)
    data_tup = context.make_tuple(builder, types.Tuple([jbks__dbku]), [
        awry__nhrd._getvalue()])
    return data_tup


def _cast_df_data_to_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(fromty,
        'casting table format to traditional DataFrame')
    kzl__wcqc = fromty.table_type
    xtu__xwcdf = cgutils.create_struct_proxy(kzl__wcqc)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    kdl__vvq = []
    for i, kkpkq__ulfg in enumerate(toty.data):
        uvdqb__ghl = fromty.data[i]
        if kkpkq__ulfg != uvdqb__ghl:
            obrqa__ngiyr = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*obrqa__ngiyr)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        jmvm__ajecq = kzl__wcqc.type_to_blk[uvdqb__ghl]
        auoe__eston = getattr(xtu__xwcdf, f'block_{jmvm__ajecq}')
        qxvty__zwzru = ListInstance(context, builder, types.List(uvdqb__ghl
            ), auoe__eston)
        qni__qvp = context.get_constant(types.int64, kzl__wcqc.block_offsets[i]
            )
        mwir__kbyx = qxvty__zwzru.getitem(qni__qvp)
        if kkpkq__ulfg != uvdqb__ghl:
            jhpam__zyak = context.cast(builder, mwir__kbyx, uvdqb__ghl,
                kkpkq__ulfg)
        else:
            jhpam__zyak = mwir__kbyx
            context.nrt.incref(builder, kkpkq__ulfg, jhpam__zyak)
        kdl__vvq.append(jhpam__zyak)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), kdl__vvq)
    return data_tup


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    zuf__vqa, ealuq__bnlc, index_arg = _get_df_args(data, index, columns,
        dtype, copy)
    tleou__obkoe = ColNamesMetaType(tuple(zuf__vqa))
    zba__aggv = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    zba__aggv += (
        """  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, __col_name_meta_value_pd_overload)
"""
        .format(ealuq__bnlc, index_arg))
    nksvu__xjzdm = {}
    exec(zba__aggv, {'bodo': bodo, 'np': np,
        '__col_name_meta_value_pd_overload': tleou__obkoe}, nksvu__xjzdm)
    bjh__xrqr = nksvu__xjzdm['_init_df']
    return bjh__xrqr


@intrinsic
def _tuple_to_table_format_decoded(typingctx, df_typ):
    assert not df_typ.is_table_format, '_tuple_to_table_format requires a tuple format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    ohh__ery = DataFrameType(to_str_arr_if_dict_array(df_typ.data), df_typ.
        index, df_typ.columns, dist=df_typ.dist, is_table_format=True)
    sig = signature(ohh__ery, df_typ)
    return sig, codegen


@intrinsic
def _table_to_tuple_format_decoded(typingctx, df_typ):
    assert df_typ.is_table_format, '_tuple_to_table_format requires a table format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    ohh__ery = DataFrameType(to_str_arr_if_dict_array(df_typ.data), df_typ.
        index, df_typ.columns, dist=df_typ.dist, is_table_format=False)
    sig = signature(ohh__ery, df_typ)
    return sig, codegen


def _get_df_args(data, index, columns, dtype, copy):
    vsgeb__kes = ''
    if not is_overload_none(dtype):
        vsgeb__kes = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        oym__zcprq = (len(data.types) - 1) // 2
        pwlza__dnsrk = [kkpkq__ulfg.literal_value for kkpkq__ulfg in data.
            types[1:oym__zcprq + 1]]
        data_val_types = dict(zip(pwlza__dnsrk, data.types[oym__zcprq + 1:]))
        kdl__vvq = ['data[{}]'.format(i) for i in range(oym__zcprq + 1, 2 *
            oym__zcprq + 1)]
        data_dict = dict(zip(pwlza__dnsrk, kdl__vvq))
        if is_overload_none(index):
            for i, kkpkq__ulfg in enumerate(data.types[oym__zcprq + 1:]):
                if isinstance(kkpkq__ulfg, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(oym__zcprq + 1 + i))
                    index_is_none = False
                    break
    elif is_overload_none(data):
        data_dict = {}
        data_val_types = {}
    else:
        if not (isinstance(data, types.Array) and data.ndim == 2):
            raise BodoError(
                'pd.DataFrame() only supports constant dictionary and array input'
                )
        if is_overload_none(columns):
            raise BodoError(
                "pd.DataFrame() 'columns' argument is required when an array is passed as data"
                )
        khj__hksru = '.copy()' if copy else ''
        epd__fqlup = get_overload_const_list(columns)
        oym__zcprq = len(epd__fqlup)
        data_val_types = {crsf__qrtc: data.copy(ndim=1) for crsf__qrtc in
            epd__fqlup}
        kdl__vvq = ['data[:,{}]{}'.format(i, khj__hksru) for i in range(
            oym__zcprq)]
        data_dict = dict(zip(epd__fqlup, kdl__vvq))
    if is_overload_none(columns):
        col_names = data_dict.keys()
    else:
        col_names = get_overload_const_list(columns)
    df_len = _get_df_len_from_info(data_dict, data_val_types, col_names,
        index_is_none, index_arg)
    _fill_null_arrays(data_dict, col_names, df_len, dtype)
    if index_is_none:
        if is_overload_none(data):
            index_arg = (
                'bodo.hiframes.pd_index_ext.init_binary_str_index(bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0))'
                )
        else:
            index_arg = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, {}, 1, None)'
                .format(df_len))
    ealuq__bnlc = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[crsf__qrtc], df_len, vsgeb__kes) for crsf__qrtc in
        col_names))
    if len(col_names) == 0:
        ealuq__bnlc = '()'
    return col_names, ealuq__bnlc, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for crsf__qrtc in col_names:
        if crsf__qrtc in data_dict and is_iterable_type(data_val_types[
            crsf__qrtc]):
            df_len = 'len({})'.format(data_dict[crsf__qrtc])
            break
    if df_len == '0':
        if not index_is_none:
            df_len = f'len({index_arg})'
        elif data_dict:
            raise BodoError(
                'Internal Error: Unable to determine length of DataFrame Index. If this is unexpected, please try passing an index value.'
                )
    return df_len


def _fill_null_arrays(data_dict, col_names, df_len, dtype):
    if all(crsf__qrtc in data_dict for crsf__qrtc in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    bmi__wej = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len,
        dtype)
    for crsf__qrtc in col_names:
        if crsf__qrtc not in data_dict:
            data_dict[crsf__qrtc] = bmi__wej


@infer_global(len)
class LenTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        if isinstance(args[0], (DataFrameType, bodo.TableType)):
            return types.int64(*args)


@lower_builtin(len, DataFrameType)
def table_len_lower(context, builder, sig, args):
    impl = df_len_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def df_len_overload(df):
    if not isinstance(df, DataFrameType):
        return
    if df.has_runtime_cols:

        def impl(df):
            if is_null_pointer(df._meminfo):
                return 0
            kkpkq__ulfg = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df
                )
            return len(kkpkq__ulfg)
        return impl
    if len(df.columns) == 0:

        def impl(df):
            if is_null_pointer(df._meminfo):
                return 0
            return len(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
        return impl

    def impl(df):
        if is_null_pointer(df._meminfo):
            return 0
        return len(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, 0))
    return impl


@infer_global(operator.getitem)
class GetItemTuple(AbstractTemplate):
    key = operator.getitem

    def generic(self, args, kws):
        tup, idx = args
        if not isinstance(tup, types.BaseTuple) or not isinstance(idx,
            types.IntegerLiteral):
            return
        mxfer__cfwo = idx.literal_value
        if isinstance(mxfer__cfwo, int):
            iol__fvrgl = tup.types[mxfer__cfwo]
        elif isinstance(mxfer__cfwo, slice):
            iol__fvrgl = types.BaseTuple.from_types(tup.types[mxfer__cfwo])
        return signature(iol__fvrgl, *args)


GetItemTuple.prefer_literal = True


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    amdb__iqk, idx = sig.args
    idx = idx.literal_value
    tup, ihv__tvfw = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(amdb__iqk)
        if not 0 <= idx < len(amdb__iqk):
            raise IndexError('cannot index at %d in %s' % (idx, amdb__iqk))
        rkitm__zynra = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        khody__lcbo = cgutils.unpack_tuple(builder, tup)[idx]
        rkitm__zynra = context.make_tuple(builder, sig.return_type, khody__lcbo
            )
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, rkitm__zynra)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, csvfe__hiwc, suffix_x,
            suffix_y, is_join, indicator, ihv__tvfw, ihv__tvfw) = args
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        vvrr__wdws = {crsf__qrtc: i for i, crsf__qrtc in enumerate(left_on)}
        hmbjk__nplfs = {crsf__qrtc: i for i, crsf__qrtc in enumerate(right_on)}
        ajhdz__lbygc = set(left_on) & set(right_on)
        spb__mlog = set(left_df.columns) & set(right_df.columns)
        tbg__aovnz = spb__mlog - ajhdz__lbygc
        pcap__fgr = '$_bodo_index_' in left_on
        mksf__svwrq = '$_bodo_index_' in right_on
        how = get_overload_const_str(csvfe__hiwc)
        cqt__yov = how in {'left', 'outer'}
        ptg__vfoid = how in {'right', 'outer'}
        columns = []
        data = []
        if pcap__fgr:
            dlu__iexn = bodo.utils.typing.get_index_data_arr_types(left_df.
                index)[0]
        else:
            dlu__iexn = left_df.data[left_df.column_index[left_on[0]]]
        if mksf__svwrq:
            vhf__xuhw = bodo.utils.typing.get_index_data_arr_types(right_df
                .index)[0]
        else:
            vhf__xuhw = right_df.data[right_df.column_index[right_on[0]]]
        if pcap__fgr and not mksf__svwrq and not is_join.literal_value:
            rsfar__drtxz = right_on[0]
            if rsfar__drtxz in left_df.column_index:
                columns.append(rsfar__drtxz)
                if (vhf__xuhw == bodo.dict_str_arr_type and dlu__iexn ==
                    bodo.string_array_type):
                    yzeav__igy = bodo.string_array_type
                else:
                    yzeav__igy = vhf__xuhw
                data.append(yzeav__igy)
        if mksf__svwrq and not pcap__fgr and not is_join.literal_value:
            vtrh__yqqj = left_on[0]
            if vtrh__yqqj in right_df.column_index:
                columns.append(vtrh__yqqj)
                if (dlu__iexn == bodo.dict_str_arr_type and vhf__xuhw ==
                    bodo.string_array_type):
                    yzeav__igy = bodo.string_array_type
                else:
                    yzeav__igy = dlu__iexn
                data.append(yzeav__igy)
        for uvdqb__ghl, rjulu__wwz in zip(left_df.data, left_df.columns):
            columns.append(str(rjulu__wwz) + suffix_x.literal_value if 
                rjulu__wwz in tbg__aovnz else rjulu__wwz)
            if rjulu__wwz in ajhdz__lbygc:
                if uvdqb__ghl == bodo.dict_str_arr_type:
                    uvdqb__ghl = right_df.data[right_df.column_index[
                        rjulu__wwz]]
                data.append(uvdqb__ghl)
            else:
                if (uvdqb__ghl == bodo.dict_str_arr_type and rjulu__wwz in
                    vvrr__wdws):
                    if mksf__svwrq:
                        uvdqb__ghl = vhf__xuhw
                    else:
                        dld__euiko = vvrr__wdws[rjulu__wwz]
                        jqcb__mxn = right_on[dld__euiko]
                        uvdqb__ghl = right_df.data[right_df.column_index[
                            jqcb__mxn]]
                if ptg__vfoid:
                    uvdqb__ghl = to_nullable_type(uvdqb__ghl)
                data.append(uvdqb__ghl)
        for uvdqb__ghl, rjulu__wwz in zip(right_df.data, right_df.columns):
            if rjulu__wwz not in ajhdz__lbygc:
                columns.append(str(rjulu__wwz) + suffix_y.literal_value if 
                    rjulu__wwz in tbg__aovnz else rjulu__wwz)
                if (uvdqb__ghl == bodo.dict_str_arr_type and rjulu__wwz in
                    hmbjk__nplfs):
                    if pcap__fgr:
                        uvdqb__ghl = dlu__iexn
                    else:
                        dld__euiko = hmbjk__nplfs[rjulu__wwz]
                        dtvrt__mpfwl = left_on[dld__euiko]
                        uvdqb__ghl = left_df.data[left_df.column_index[
                            dtvrt__mpfwl]]
                if cqt__yov:
                    uvdqb__ghl = to_nullable_type(uvdqb__ghl)
                data.append(uvdqb__ghl)
        wcp__yvuqo = get_overload_const_bool(indicator)
        if wcp__yvuqo:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        rjzwc__wkof = False
        if pcap__fgr and mksf__svwrq and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            rjzwc__wkof = True
        elif pcap__fgr and not mksf__svwrq:
            index_typ = right_df.index
            rjzwc__wkof = True
        elif mksf__svwrq and not pcap__fgr:
            index_typ = left_df.index
            rjzwc__wkof = True
        if rjzwc__wkof and isinstance(index_typ, bodo.hiframes.pd_index_ext
            .RangeIndexType):
            index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64
                )
        adjzq__jyxwg = DataFrameType(tuple(data), index_typ, tuple(columns),
            is_table_format=True)
        return signature(adjzq__jyxwg, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    pajyn__zpxq = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return pajyn__zpxq._getvalue()


@overload(pd.concat, inline='always', no_unliteral=True)
def concat_overload(objs, axis=0, join='outer', join_axes=None,
    ignore_index=False, keys=None, levels=None, names=None,
    verify_integrity=False, sort=None, copy=True):
    if not is_overload_constant_int(axis):
        raise BodoError("pd.concat(): 'axis' should be a constant integer")
    if not is_overload_constant_bool(ignore_index):
        raise BodoError(
            "pd.concat(): 'ignore_index' should be a constant boolean")
    axis = get_overload_const_int(axis)
    ignore_index = is_overload_true(ignore_index)
    iiop__khrjj = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    fktql__nghc = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pandas.concat', iiop__khrjj, fktql__nghc,
        package_name='pandas', module_name='General')
    zba__aggv = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        tjat__cojnv = 0
        ealuq__bnlc = []
        names = []
        for i, goqo__zuyc in enumerate(objs.types):
            assert isinstance(goqo__zuyc, (SeriesType, DataFrameType))
            check_runtime_cols_unsupported(goqo__zuyc, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                goqo__zuyc, 'pandas.concat()')
            if isinstance(goqo__zuyc, SeriesType):
                names.append(str(tjat__cojnv))
                tjat__cojnv += 1
                ealuq__bnlc.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(goqo__zuyc.columns)
                for umu__fumnq in range(len(goqo__zuyc.data)):
                    ealuq__bnlc.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, umu__fumnq))
        return bodo.hiframes.dataframe_impl._gen_init_df(zba__aggv, names,
            ', '.join(ealuq__bnlc), index)
    if axis != 0:
        raise_bodo_error('pd.concat(): axis must be 0 or 1')
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(kkpkq__ulfg, DataFrameType) for kkpkq__ulfg in
            objs.types)
        wzy__ryfcm = []
        for df in objs.types:
            check_runtime_cols_unsupported(df, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
                'pandas.concat()')
            wzy__ryfcm.extend(df.columns)
        wzy__ryfcm = list(dict.fromkeys(wzy__ryfcm).keys())
        ailu__mequw = {}
        for tjat__cojnv, crsf__qrtc in enumerate(wzy__ryfcm):
            for i, df in enumerate(objs.types):
                if crsf__qrtc in df.column_index:
                    ailu__mequw[f'arr_typ{tjat__cojnv}'] = df.data[df.
                        column_index[crsf__qrtc]]
                    break
        assert len(ailu__mequw) == len(wzy__ryfcm)
        ilix__gia = []
        for tjat__cojnv, crsf__qrtc in enumerate(wzy__ryfcm):
            args = []
            for i, df in enumerate(objs.types):
                if crsf__qrtc in df.column_index:
                    ilspw__fmacu = df.column_index[crsf__qrtc]
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, ilspw__fmacu))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, tjat__cojnv))
            zba__aggv += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'
                .format(tjat__cojnv, ', '.join(args)))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(A0), 1, None)'
                )
        else:
            index = (
                """bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)) if len(objs[i].
                columns) > 0)))
        return bodo.hiframes.dataframe_impl._gen_init_df(zba__aggv,
            wzy__ryfcm, ', '.join('A{}'.format(i) for i in range(len(
            wzy__ryfcm))), index, ailu__mequw)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(kkpkq__ulfg, SeriesType) for kkpkq__ulfg in
            objs.types)
        zba__aggv += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'
            .format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            zba__aggv += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            zba__aggv += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        zba__aggv += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        nksvu__xjzdm = {}
        exec(zba__aggv, {'bodo': bodo, 'np': np, 'numba': numba}, nksvu__xjzdm)
        return nksvu__xjzdm['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        check_runtime_cols_unsupported(objs.dtype, 'pandas.concat()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(objs.
            dtype, 'pandas.concat()')
        df_type = objs.dtype
        for tjat__cojnv, crsf__qrtc in enumerate(df_type.columns):
            zba__aggv += '  arrs{} = []\n'.format(tjat__cojnv)
            zba__aggv += '  for i in range(len(objs)):\n'
            zba__aggv += '    df = objs[i]\n'
            zba__aggv += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(tjat__cojnv))
            zba__aggv += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(tjat__cojnv))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            zba__aggv += '  arrs_index = []\n'
            zba__aggv += '  for i in range(len(objs)):\n'
            zba__aggv += '    df = objs[i]\n'
            zba__aggv += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            if objs.dtype.index.name_typ == types.none:
                name = None
            else:
                name = objs.dtype.index.name_typ.literal_value
            index = f"""bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index), {name!r})
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(zba__aggv, df_type
            .columns, ', '.join('out_arr{}'.format(i) for i in range(len(
            df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        zba__aggv += '  arrs = []\n'
        zba__aggv += '  for i in range(len(objs)):\n'
        zba__aggv += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        zba__aggv += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            zba__aggv += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            zba__aggv += '  arrs_index = []\n'
            zba__aggv += '  for i in range(len(objs)):\n'
            zba__aggv += '    S = objs[i]\n'
            zba__aggv += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            zba__aggv += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        zba__aggv += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        nksvu__xjzdm = {}
        exec(zba__aggv, {'bodo': bodo, 'np': np, 'numba': numba}, nksvu__xjzdm)
        return nksvu__xjzdm['impl']
    raise BodoError('pd.concat(): input type {} not supported yet'.format(objs)
        )


def sort_values_dummy(df, by, ascending, inplace, na_position):
    return df.sort_values(by, ascending=ascending, inplace=inplace,
        na_position=na_position)


@infer_global(sort_values_dummy)
class SortDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, by, ascending, inplace, na_position = args
        index = df.index
        if isinstance(index, bodo.hiframes.pd_index_ext.RangeIndexType):
            index = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64)
        ohh__ery = df.copy(index=index)
        return signature(ohh__ery, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    rknxp__uanq = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return rknxp__uanq._getvalue()


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    check_runtime_cols_unsupported(df, 'DataFrame.itertuples()')
    iiop__khrjj = dict(index=index, name=name)
    fktql__nghc = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', iiop__khrjj, fktql__nghc,
        package_name='pandas', module_name='DataFrame')

    def _impl(df, index=True, name='Pandas'):
        return bodo.hiframes.pd_dataframe_ext.itertuples_dummy(df)
    return _impl


def itertuples_dummy(df):
    return df


@infer_global(itertuples_dummy)
class ItertuplesDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, = args
        assert 'Index' not in df.columns
        columns = ('Index',) + df.columns
        ailu__mequw = (types.Array(types.int64, 1, 'C'),) + df.data
        zfg__ntf = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(columns,
            ailu__mequw)
        return signature(zfg__ntf, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    rknxp__uanq = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return rknxp__uanq._getvalue()


def query_dummy(df, expr):
    return df.eval(expr)


@infer_global(query_dummy)
class QueryDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(SeriesType(types.bool_, index=RangeIndexType(types
            .none)), *args)


@lower_builtin(query_dummy, types.VarArg(types.Any))
def lower_query_dummy(context, builder, sig, args):
    rknxp__uanq = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return rknxp__uanq._getvalue()


def val_isin_dummy(S, vals):
    return S in vals


def val_notin_dummy(S, vals):
    return S not in vals


@infer_global(val_isin_dummy)
@infer_global(val_notin_dummy)
class ValIsinTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(SeriesType(types.bool_, index=args[0].index), *args)


@lower_builtin(val_isin_dummy, types.VarArg(types.Any))
@lower_builtin(val_notin_dummy, types.VarArg(types.Any))
def lower_val_isin_dummy(context, builder, sig, args):
    rknxp__uanq = cgutils.create_struct_proxy(sig.return_type)(context, builder
        )
    return rknxp__uanq._getvalue()


@numba.generated_jit(nopython=True)
def pivot_impl(index_tup, columns_tup, values_tup, pivot_values,
    index_names, columns_name, value_names, check_duplicates=True,
    is_already_shuffled=False, _constant_pivot_values=None, parallel=False):
    if not is_overload_constant_bool(check_duplicates):
        raise BodoError(
            'pivot_impl(): check_duplicates must be a constant boolean')
    smmy__uje = get_overload_const_bool(check_duplicates)
    jqmu__zdjk = not get_overload_const_bool(is_already_shuffled)
    lqj__pcg = not is_overload_none(_constant_pivot_values)
    index_names = index_names.instance_type if isinstance(index_names,
        types.TypeRef) else index_names
    columns_name = columns_name.instance_type if isinstance(columns_name,
        types.TypeRef) else columns_name
    value_names = value_names.instance_type if isinstance(value_names,
        types.TypeRef) else value_names
    _constant_pivot_values = (_constant_pivot_values.instance_type if
        isinstance(_constant_pivot_values, types.TypeRef) else
        _constant_pivot_values)
    gjlh__fdk = len(value_names) > 1
    kom__gnu = None
    guoqh__bcp = None
    qwlx__fygr = None
    jxtcg__krs = None
    mfktp__jqpsg = isinstance(values_tup, types.UniTuple)
    if mfktp__jqpsg:
        oiim__lqor = [to_str_arr_if_dict_array(to_nullable_type(values_tup.
            dtype))]
    else:
        oiim__lqor = [to_str_arr_if_dict_array(to_nullable_type(uva__rng)) for
            uva__rng in values_tup]
    zba__aggv = 'def impl(\n'
    zba__aggv += """    index_tup, columns_tup, values_tup, pivot_values, index_names, columns_name, value_names, check_duplicates=True, is_already_shuffled=False, _constant_pivot_values=None, parallel=False
"""
    zba__aggv += '):\n'
    zba__aggv += "    ev = tracing.Event('pivot_impl', is_parallel=parallel)\n"
    if jqmu__zdjk:
        zba__aggv += '    if parallel:\n'
        zba__aggv += (
            "        ev_shuffle = tracing.Event('shuffle_pivot_index')\n")
        hwse__rnxy = ', '.join([f'array_to_info(index_tup[{i}])' for i in
            range(len(index_tup))] + [f'array_to_info(columns_tup[{i}])' for
            i in range(len(columns_tup))] + [
            f'array_to_info(values_tup[{i}])' for i in range(len(values_tup))])
        zba__aggv += f'        info_list = [{hwse__rnxy}]\n'
        zba__aggv += '        cpp_table = arr_info_list_to_table(info_list)\n'
        zba__aggv += f"""        out_cpp_table = shuffle_table(cpp_table, {len(index_tup)}, parallel, 0)
"""
        dkhj__qnd = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i}), index_tup[{i}])'
             for i in range(len(index_tup))])
        zdoq__wwsa = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup)}), columns_tup[{i}])'
             for i in range(len(columns_tup))])
        gynjv__rtaf = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup) + len(columns_tup)}), values_tup[{i}])'
             for i in range(len(values_tup))])
        zba__aggv += f'        index_tup = ({dkhj__qnd},)\n'
        zba__aggv += f'        columns_tup = ({zdoq__wwsa},)\n'
        zba__aggv += f'        values_tup = ({gynjv__rtaf},)\n'
        zba__aggv += '        delete_table(cpp_table)\n'
        zba__aggv += '        delete_table(out_cpp_table)\n'
        zba__aggv += '        ev_shuffle.finalize()\n'
    zba__aggv += '    columns_arr = columns_tup[0]\n'
    if mfktp__jqpsg:
        zba__aggv += '    values_arrs = [arr for arr in values_tup]\n'
    zba__aggv += (
        "    ev_unique = tracing.Event('pivot_unique_index_map', is_parallel=parallel)\n"
        )
    zba__aggv += """    unique_index_arr_tup, row_vector = bodo.libs.array_ops.array_unique_vector_map(
"""
    zba__aggv += '        index_tup\n'
    zba__aggv += '    )\n'
    zba__aggv += '    n_rows = len(unique_index_arr_tup[0])\n'
    zba__aggv += '    num_values_arrays = len(values_tup)\n'
    zba__aggv += '    n_unique_pivots = len(pivot_values)\n'
    if mfktp__jqpsg:
        zba__aggv += '    n_cols = num_values_arrays * n_unique_pivots\n'
    else:
        zba__aggv += '    n_cols = n_unique_pivots\n'
    zba__aggv += '    col_map = {}\n'
    zba__aggv += '    for i in range(n_unique_pivots):\n'
    zba__aggv += '        if bodo.libs.array_kernels.isna(pivot_values, i):\n'
    zba__aggv += '            raise ValueError(\n'
    zba__aggv += """                "DataFrame.pivot(): NA values in 'columns' array not supported\"
"""
    zba__aggv += '            )\n'
    zba__aggv += '        col_map[pivot_values[i]] = i\n'
    zba__aggv += '    ev_unique.finalize()\n'
    zba__aggv += (
        "    ev_alloc = tracing.Event('pivot_alloc', is_parallel=parallel)\n")
    tes__kuc = False
    for i, tyv__ptpsd in enumerate(oiim__lqor):
        if is_str_arr_type(tyv__ptpsd):
            tes__kuc = True
            zba__aggv += (
                f'    len_arrs_{i} = [np.zeros(n_rows, np.int64) for _ in range(n_cols)]\n'
                )
            zba__aggv += f'    total_lens_{i} = np.zeros(n_cols, np.int64)\n'
    if tes__kuc:
        if smmy__uje:
            zba__aggv += '    nbytes = (n_rows + 7) >> 3\n'
            zba__aggv += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
        zba__aggv += '    for i in range(len(columns_arr)):\n'
        zba__aggv += '        col_name = columns_arr[i]\n'
        zba__aggv += '        pivot_idx = col_map[col_name]\n'
        zba__aggv += '        row_idx = row_vector[i]\n'
        if smmy__uje:
            zba__aggv += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
            zba__aggv += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
            zba__aggv += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
            zba__aggv += '        else:\n'
            zba__aggv += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
        if mfktp__jqpsg:
            zba__aggv += '        for j in range(num_values_arrays):\n'
            zba__aggv += (
                '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
            zba__aggv += '            len_arr = len_arrs_0[col_idx]\n'
            zba__aggv += '            values_arr = values_arrs[j]\n'
            zba__aggv += (
                '            if not bodo.libs.array_kernels.isna(values_arr, i):\n'
                )
            zba__aggv += """                str_val_len = bodo.libs.str_arr_ext.get_str_arr_item_length(values_arr, i)
"""
            zba__aggv += '                len_arr[row_idx] = str_val_len\n'
            zba__aggv += (
                '                total_lens_0[col_idx] += str_val_len\n')
        else:
            for i, tyv__ptpsd in enumerate(oiim__lqor):
                if is_str_arr_type(tyv__ptpsd):
                    zba__aggv += f"""        if not bodo.libs.array_kernels.isna(values_tup[{i}], i):
"""
                    zba__aggv += f"""            str_val_len_{i} = bodo.libs.str_arr_ext.get_str_arr_item_length(values_tup[{i}], i)
"""
                    zba__aggv += (
                        f'            len_arrs_{i}[pivot_idx][row_idx] = str_val_len_{i}\n'
                        )
                    zba__aggv += (
                        f'            total_lens_{i}[pivot_idx] += str_val_len_{i}\n'
                        )
    zba__aggv += f"    ev_alloc.add_attribute('num_rows', n_rows)\n"
    for i, tyv__ptpsd in enumerate(oiim__lqor):
        if is_str_arr_type(tyv__ptpsd):
            zba__aggv += f'    data_arrs_{i} = [\n'
            zba__aggv += (
                '        bodo.libs.str_arr_ext.gen_na_str_array_lens(\n')
            zba__aggv += (
                f'            n_rows, total_lens_{i}[i], len_arrs_{i}[i]\n')
            zba__aggv += '        )\n'
            zba__aggv += '        for i in range(n_cols)\n'
            zba__aggv += '    ]\n'
            zba__aggv += f'    if tracing.is_tracing():\n'
            zba__aggv += '         for i in range(n_cols):'
            zba__aggv += f"""            ev_alloc.add_attribute('total_str_chars_out_column_{i}_' + str(i), total_lens_{i}[i])
"""
        else:
            zba__aggv += f'    data_arrs_{i} = [\n'
            zba__aggv += (
                f'        bodo.libs.array_kernels.gen_na_array(n_rows, data_arr_typ_{i})\n'
                )
            zba__aggv += '        for _ in range(n_cols)\n'
            zba__aggv += '    ]\n'
    if not tes__kuc and smmy__uje:
        zba__aggv += '    nbytes = (n_rows + 7) >> 3\n'
        zba__aggv += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
    zba__aggv += '    ev_alloc.finalize()\n'
    zba__aggv += (
        "    ev_fill = tracing.Event('pivot_fill_data', is_parallel=parallel)\n"
        )
    zba__aggv += '    for i in range(len(columns_arr)):\n'
    zba__aggv += '        col_name = columns_arr[i]\n'
    zba__aggv += '        pivot_idx = col_map[col_name]\n'
    zba__aggv += '        row_idx = row_vector[i]\n'
    if not tes__kuc and smmy__uje:
        zba__aggv += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
        zba__aggv += (
            '        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):\n'
            )
        zba__aggv += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
        zba__aggv += '        else:\n'
        zba__aggv += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)\n'
            )
    if mfktp__jqpsg:
        zba__aggv += '        for j in range(num_values_arrays):\n'
        zba__aggv += (
            '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
        zba__aggv += '            col_arr = data_arrs_0[col_idx]\n'
        zba__aggv += '            values_arr = values_arrs[j]\n'
        zba__aggv += (
            '            if bodo.libs.array_kernels.isna(values_arr, i):\n')
        zba__aggv += (
            '                bodo.libs.array_kernels.setna(col_arr, row_idx)\n'
            )
        zba__aggv += '            else:\n'
        zba__aggv += '                col_arr[row_idx] = values_arr[i]\n'
    else:
        for i, tyv__ptpsd in enumerate(oiim__lqor):
            zba__aggv += f'        col_arr_{i} = data_arrs_{i}[pivot_idx]\n'
            zba__aggv += (
                f'        if bodo.libs.array_kernels.isna(values_tup[{i}], i):\n'
                )
            zba__aggv += (
                f'            bodo.libs.array_kernels.setna(col_arr_{i}, row_idx)\n'
                )
            zba__aggv += f'        else:\n'
            zba__aggv += (
                f'            col_arr_{i}[row_idx] = values_tup[{i}][i]\n')
    if len(index_names) == 1:
        zba__aggv += """    index = bodo.utils.conversion.index_from_array(unique_index_arr_tup[0], index_names_lit)
"""
        kom__gnu = index_names.meta[0]
    else:
        zba__aggv += """    index = bodo.hiframes.pd_multi_index_ext.init_multi_index(unique_index_arr_tup, index_names_lit, None)
"""
        kom__gnu = tuple(index_names.meta)
    zba__aggv += f'    if tracing.is_tracing():\n'
    zba__aggv += f'        index_nbytes = index.nbytes\n'
    zba__aggv += f"        ev.add_attribute('index_nbytes', index_nbytes)\n"
    if not lqj__pcg:
        qwlx__fygr = columns_name.meta[0]
        if gjlh__fdk:
            zba__aggv += (
                f'    num_rows = {len(value_names)} * len(pivot_values)\n')
            guoqh__bcp = value_names.meta
            if all(isinstance(crsf__qrtc, str) for crsf__qrtc in guoqh__bcp):
                guoqh__bcp = pd.array(guoqh__bcp, 'string')
            elif all(isinstance(crsf__qrtc, int) for crsf__qrtc in guoqh__bcp):
                guoqh__bcp = np.array(guoqh__bcp, 'int64')
            else:
                raise BodoError(
                    f"pivot(): column names selected for 'values' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
                    )
            if isinstance(guoqh__bcp.dtype, pd.StringDtype):
                zba__aggv += '    total_chars = 0\n'
                zba__aggv += f'    for i in range({len(value_names)}):\n'
                zba__aggv += """        value_name_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(value_names_lit, i)
"""
                zba__aggv += '        total_chars += value_name_str_len\n'
                zba__aggv += """    new_value_names = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(pivot_values))
"""
            else:
                zba__aggv += """    new_value_names = bodo.utils.utils.alloc_type(num_rows, value_names_lit, (-1,))
"""
            if is_str_arr_type(pivot_values):
                zba__aggv += '    total_chars = 0\n'
                zba__aggv += '    for i in range(len(pivot_values)):\n'
                zba__aggv += """        pivot_val_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(pivot_values, i)
"""
                zba__aggv += '        total_chars += pivot_val_str_len\n'
                zba__aggv += f"""    new_pivot_values = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * {len(value_names)})
"""
            else:
                zba__aggv += """    new_pivot_values = bodo.utils.utils.alloc_type(num_rows, pivot_values, (-1,))
"""
            zba__aggv += f'    for i in range({len(value_names)}):\n'
            zba__aggv += '        for j in range(len(pivot_values)):\n'
            zba__aggv += """            new_value_names[(i * len(pivot_values)) + j] = value_names_lit[i]
"""
            zba__aggv += """            new_pivot_values[(i * len(pivot_values)) + j] = pivot_values[j]
"""
            zba__aggv += """    column_index = bodo.hiframes.pd_multi_index_ext.init_multi_index((new_value_names, new_pivot_values), (None, columns_name_lit), None)
"""
        else:
            zba__aggv += """    column_index =  bodo.utils.conversion.index_from_array(pivot_values, columns_name_lit)
"""
    zba__aggv += '    ev_fill.finalize()\n'
    kzl__wcqc = None
    if lqj__pcg:
        if gjlh__fdk:
            iild__kkii = []
            for xlr__pnv in _constant_pivot_values.meta:
                for yojlv__rhqg in value_names.meta:
                    iild__kkii.append((xlr__pnv, yojlv__rhqg))
            column_names = tuple(iild__kkii)
        else:
            column_names = tuple(_constant_pivot_values.meta)
        jxtcg__krs = ColNamesMetaType(column_names)
        vib__suhn = []
        for uva__rng in oiim__lqor:
            vib__suhn.extend([uva__rng] * len(_constant_pivot_values))
        mhx__esjcv = tuple(vib__suhn)
        kzl__wcqc = TableType(mhx__esjcv)
        zba__aggv += (
            f'    table = bodo.hiframes.table.init_table(table_type, False)\n')
        zba__aggv += (
            f'    table = bodo.hiframes.table.set_table_len(table, n_rows)\n')
        for i, uva__rng in enumerate(oiim__lqor):
            zba__aggv += f"""    table = bodo.hiframes.table.set_table_block(table, data_arrs_{i}, {kzl__wcqc.type_to_blk[uva__rng]})
"""
        zba__aggv += (
            '    result = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
        zba__aggv += '        (table,), index, columns_typ\n'
        zba__aggv += '    )\n'
    else:
        zvln__jdv = ', '.join(f'data_arrs_{i}' for i in range(len(oiim__lqor)))
        zba__aggv += f"""    table = bodo.hiframes.table.init_runtime_table_from_lists(({zvln__jdv},), n_rows)
"""
        zba__aggv += (
            '    result = bodo.hiframes.pd_dataframe_ext.init_runtime_cols_dataframe(\n'
            )
        zba__aggv += '        (table,), index, column_index\n'
        zba__aggv += '    )\n'
    zba__aggv += '    ev.finalize()\n'
    zba__aggv += '    return result\n'
    nksvu__xjzdm = {}
    vjx__dfe = {f'data_arr_typ_{i}': tyv__ptpsd for i, tyv__ptpsd in
        enumerate(oiim__lqor)}
    trtb__set = {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'info_from_table': info_from_table, 'table_type':
        kzl__wcqc, 'columns_typ': jxtcg__krs, 'index_names_lit': kom__gnu,
        'value_names_lit': guoqh__bcp, 'columns_name_lit': qwlx__fygr, **
        vjx__dfe, 'tracing': tracing}
    exec(zba__aggv, trtb__set, nksvu__xjzdm)
    impl = nksvu__xjzdm['impl']
    return impl


def gen_pandas_parquet_metadata(column_names, data_types, index,
    write_non_range_index_to_metadata, write_rangeindex_to_metadata,
    partition_cols=None, is_runtime_columns=False):
    vzokq__qbai = {}
    vzokq__qbai['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for col_name, rctu__yzxnb in zip(column_names, data_types):
        if col_name in partition_cols:
            continue
        vmaec__lgd = None
        if isinstance(rctu__yzxnb, bodo.DatetimeArrayType):
            gje__qycx = 'datetimetz'
            shojo__ktb = 'datetime64[ns]'
            if isinstance(rctu__yzxnb.tz, int):
                mff__gbv = bodo.libs.pd_datetime_arr_ext.nanoseconds_to_offset(
                    rctu__yzxnb.tz)
            else:
                mff__gbv = pd.DatetimeTZDtype(tz=rctu__yzxnb.tz).tz
            vmaec__lgd = {'timezone': pa.lib.tzinfo_to_string(mff__gbv)}
        elif isinstance(rctu__yzxnb, types.Array
            ) or rctu__yzxnb == boolean_array:
            gje__qycx = shojo__ktb = rctu__yzxnb.dtype.name
            if shojo__ktb.startswith('datetime'):
                gje__qycx = 'datetime'
        elif is_str_arr_type(rctu__yzxnb):
            gje__qycx = 'unicode'
            shojo__ktb = 'object'
        elif rctu__yzxnb == binary_array_type:
            gje__qycx = 'bytes'
            shojo__ktb = 'object'
        elif isinstance(rctu__yzxnb, DecimalArrayType):
            gje__qycx = shojo__ktb = 'object'
        elif isinstance(rctu__yzxnb, IntegerArrayType):
            apvv__yjtfn = rctu__yzxnb.dtype.name
            if apvv__yjtfn.startswith('int'):
                gje__qycx = 'Int' + apvv__yjtfn[3:]
            elif apvv__yjtfn.startswith('uint'):
                gje__qycx = 'UInt' + apvv__yjtfn[4:]
            else:
                if is_runtime_columns:
                    col_name = 'Runtime determined column of type'
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(col_name, rctu__yzxnb))
            shojo__ktb = rctu__yzxnb.dtype.name
        elif rctu__yzxnb == datetime_date_array_type:
            gje__qycx = 'datetime'
            shojo__ktb = 'object'
        elif isinstance(rctu__yzxnb, TimeArrayType):
            gje__qycx = 'datetime'
            shojo__ktb = 'object'
        elif isinstance(rctu__yzxnb, (StructArrayType, ArrayItemArrayType)):
            gje__qycx = 'object'
            shojo__ktb = 'object'
        else:
            if is_runtime_columns:
                col_name = 'Runtime determined column of type'
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(col_name, rctu__yzxnb))
        hwy__opj = {'name': col_name, 'field_name': col_name, 'pandas_type':
            gje__qycx, 'numpy_type': shojo__ktb, 'metadata': vmaec__lgd}
        vzokq__qbai['columns'].append(hwy__opj)
    if write_non_range_index_to_metadata:
        if isinstance(index, MultiIndexType):
            raise BodoError('to_parquet: MultiIndex not supported yet')
        if 'none' in index.name:
            elzr__kqox = '__index_level_0__'
            dnu__smlyg = None
        else:
            elzr__kqox = '%s'
            dnu__smlyg = '%s'
        vzokq__qbai['index_columns'] = [elzr__kqox]
        vzokq__qbai['columns'].append({'name': dnu__smlyg, 'field_name':
            elzr__kqox, 'pandas_type': index.pandas_type_name, 'numpy_type':
            index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        vzokq__qbai['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        vzokq__qbai['index_columns'] = []
    vzokq__qbai['pandas_version'] = pd.__version__
    return vzokq__qbai


@overload_method(DataFrameType, 'to_parquet', no_unliteral=True)
def to_parquet_overload(df, path, engine='auto', compression='snappy',
    index=None, partition_cols=None, storage_options=None, row_group_size=-
    1, _bodo_file_prefix='part-', _bodo_timestamp_tz=None, _is_parallel=False):
    check_unsupported_args('DataFrame.to_parquet', {'storage_options':
        storage_options}, {'storage_options': None}, package_name='pandas',
        module_name='IO')
    if df.has_runtime_cols and not is_overload_none(partition_cols):
        raise BodoError(
            f"DataFrame.to_parquet(): Providing 'partition_cols' on DataFrames with columns determined at runtime is not yet supported. Please return the DataFrame to regular Python to update typing information."
            )
    if not is_overload_none(engine) and get_overload_const_str(engine) not in (
        'auto', 'pyarrow'):
        raise BodoError('DataFrame.to_parquet(): only pyarrow engine supported'
            )
    if not is_overload_none(compression) and get_overload_const_str(compression
        ) not in {'snappy', 'gzip', 'brotli'}:
        raise BodoError('to_parquet(): Unsupported compression: ' + str(
            get_overload_const_str(compression)))
    if not is_overload_none(partition_cols):
        partition_cols = get_overload_const_list(partition_cols)
        mqi__suqxg = []
        for vxoza__kde in partition_cols:
            try:
                idx = df.columns.index(vxoza__kde)
            except ValueError as xwdi__uares:
                raise BodoError(
                    f'Partition column {vxoza__kde} is not in dataframe')
            mqi__suqxg.append(idx)
    else:
        partition_cols = None
    if not is_overload_none(index) and not is_overload_constant_bool(index):
        raise BodoError('to_parquet(): index must be a constant bool or None')
    if not is_overload_int(row_group_size):
        raise BodoError('to_parquet(): row_group_size must be integer')
    if not is_overload_none(_bodo_timestamp_tz) and (not
        is_overload_constant_str(_bodo_timestamp_tz) or not
        get_overload_const_str(_bodo_timestamp_tz)):
        raise BodoError(
            'to_parquet(): _bodo_timestamp_tz must be None or a constant string'
            )
    from bodo.io.parquet_pio import parquet_write_table_cpp, parquet_write_table_partitioned_cpp
    jtjl__qcyde = isinstance(df.index, bodo.hiframes.pd_index_ext.
        RangeIndexType)
    aeky__sco = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not jtjl__qcyde)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not jtjl__qcyde or
        is_overload_true(_is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and jtjl__qcyde and not is_overload_true(_is_parallel)
    if df.has_runtime_cols:
        if isinstance(df.runtime_colname_typ, MultiIndexType):
            raise BodoError(
                'DataFrame.to_parquet(): Not supported with MultiIndex runtime column names. Please return the DataFrame to regular Python to update typing information.'
                )
        if not isinstance(df.runtime_colname_typ, bodo.hiframes.
            pd_index_ext.StringIndexType):
            raise BodoError(
                'DataFrame.to_parquet(): parquet must have string column names. Please return the DataFrame with runtime column names to regular Python to modify column names.'
                )
        icno__myah = df.runtime_data_types
        bfa__zzpcg = len(icno__myah)
        vmaec__lgd = gen_pandas_parquet_metadata([''] * bfa__zzpcg,
            icno__myah, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=True)
        uqzev__vbwgg = vmaec__lgd['columns'][:bfa__zzpcg]
        vmaec__lgd['columns'] = vmaec__lgd['columns'][bfa__zzpcg:]
        uqzev__vbwgg = [json.dumps(gbzw__dui).replace('""', '{0}') for
            gbzw__dui in uqzev__vbwgg]
        huqnb__yrzmu = json.dumps(vmaec__lgd)
        fuykq__ccb = '"columns": ['
        klnz__pie = huqnb__yrzmu.find(fuykq__ccb)
        if klnz__pie == -1:
            raise BodoError(
                'DataFrame.to_parquet(): Unexpected metadata string for runtime columns.  Please return the DataFrame to regular Python to update typing information.'
                )
        scqmd__ern = klnz__pie + len(fuykq__ccb)
        rclap__vnxr = huqnb__yrzmu[:scqmd__ern]
        huqnb__yrzmu = huqnb__yrzmu[scqmd__ern:]
        zevy__zmnv = len(vmaec__lgd['columns'])
    else:
        huqnb__yrzmu = json.dumps(gen_pandas_parquet_metadata(df.columns,
            df.data, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=False))
    if not is_overload_true(_is_parallel) and jtjl__qcyde:
        huqnb__yrzmu = huqnb__yrzmu.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            huqnb__yrzmu = huqnb__yrzmu.replace('"%s"', '%s')
    if not df.is_table_format:
        ealuq__bnlc = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
            .format(i) for i in range(len(df.columns)))
    zba__aggv = """def df_to_parquet(df, path, engine='auto', compression='snappy', index=None, partition_cols=None, storage_options=None, row_group_size=-1, _bodo_file_prefix='part-', _bodo_timestamp_tz=None, _is_parallel=False):
"""
    if df.is_table_format:
        zba__aggv += '    py_table = get_dataframe_table(df)\n'
        zba__aggv += (
            '    table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        zba__aggv += '    info_list = [{}]\n'.format(ealuq__bnlc)
        zba__aggv += '    table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        zba__aggv += '    columns_index = get_dataframe_column_names(df)\n'
        zba__aggv += '    names_arr = index_to_array(columns_index)\n'
        zba__aggv += '    col_names = array_to_info(names_arr)\n'
    else:
        zba__aggv += '    col_names = array_to_info(col_names_arr)\n'
    if is_overload_true(index) or is_overload_none(index) and aeky__sco:
        zba__aggv += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        oax__lnc = True
    else:
        zba__aggv += '    index_col = array_to_info(np.empty(0))\n'
        oax__lnc = False
    if df.has_runtime_cols:
        zba__aggv += '    columns_lst = []\n'
        zba__aggv += '    num_cols = 0\n'
        for i in range(len(df.runtime_data_types)):
            zba__aggv += f'    for _ in range(len(py_table.block_{i})):\n'
            zba__aggv += f"""        columns_lst.append({uqzev__vbwgg[i]!r}.replace('{{0}}', '"' + names_arr[num_cols] + '"'))
"""
            zba__aggv += '        num_cols += 1\n'
        if zevy__zmnv:
            zba__aggv += "    columns_lst.append('')\n"
        zba__aggv += '    columns_str = ", ".join(columns_lst)\n'
        zba__aggv += ('    metadata = """' + rclap__vnxr +
            '""" + columns_str + """' + huqnb__yrzmu + '"""\n')
    else:
        zba__aggv += '    metadata = """' + huqnb__yrzmu + '"""\n'
    zba__aggv += '    if compression is None:\n'
    zba__aggv += "        compression = 'none'\n"
    zba__aggv += '    if _bodo_timestamp_tz is None:\n'
    zba__aggv += "        _bodo_timestamp_tz = ''\n"
    zba__aggv += '    if df.index.name is not None:\n'
    zba__aggv += '        name_ptr = df.index.name\n'
    zba__aggv += '    else:\n'
    zba__aggv += "        name_ptr = 'null'\n"
    zba__aggv += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(path, parallel=_is_parallel)
"""
    jxg__sdpq = None
    if partition_cols:
        jxg__sdpq = pd.array([col_name for col_name in df.columns if 
            col_name not in partition_cols])
        nqb__gvafu = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in mqi__suqxg)
        if nqb__gvafu:
            zba__aggv += '    cat_info_list = [{}]\n'.format(nqb__gvafu)
            zba__aggv += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            zba__aggv += '    cat_table = table\n'
        zba__aggv += (
            '    col_names_no_partitions = array_to_info(col_names_no_parts_arr)\n'
            )
        zba__aggv += (
            f'    part_cols_idxs = np.array({mqi__suqxg}, dtype=np.int32)\n')
        zba__aggv += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(path),\n')
        zba__aggv += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        zba__aggv += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        zba__aggv += (
            '                            unicode_to_utf8(compression),\n')
        zba__aggv += '                            _is_parallel,\n'
        zba__aggv += (
            '                            unicode_to_utf8(bucket_region),\n')
        zba__aggv += '                            row_group_size,\n'
        zba__aggv += (
            '                            unicode_to_utf8(_bodo_file_prefix))\n'
            )
        zba__aggv += '    delete_table_decref_arrays(table)\n'
        zba__aggv += '    delete_info_decref_array(index_col)\n'
        zba__aggv += '    delete_info_decref_array(col_names_no_partitions)\n'
        zba__aggv += '    delete_info_decref_array(col_names)\n'
        if nqb__gvafu:
            zba__aggv += '    delete_table_decref_arrays(cat_table)\n'
    elif write_rangeindex_to_metadata:
        zba__aggv += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        zba__aggv += (
            '                            table, col_names, index_col,\n')
        zba__aggv += '                            ' + str(oax__lnc) + ',\n'
        zba__aggv += '                            unicode_to_utf8(metadata),\n'
        zba__aggv += (
            '                            unicode_to_utf8(compression),\n')
        zba__aggv += (
            '                            _is_parallel, 1, df.index.start,\n')
        zba__aggv += (
            '                            df.index.stop, df.index.step,\n')
        zba__aggv += '                            unicode_to_utf8(name_ptr),\n'
        zba__aggv += (
            '                            unicode_to_utf8(bucket_region),\n')
        zba__aggv += '                            row_group_size,\n'
        zba__aggv += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        zba__aggv += (
            '                            unicode_to_utf8(_bodo_timestamp_tz))\n'
            )
        zba__aggv += '    delete_table_decref_arrays(table)\n'
        zba__aggv += '    delete_info_decref_array(index_col)\n'
        zba__aggv += '    delete_info_decref_array(col_names)\n'
    else:
        zba__aggv += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        zba__aggv += (
            '                            table, col_names, index_col,\n')
        zba__aggv += '                            ' + str(oax__lnc) + ',\n'
        zba__aggv += '                            unicode_to_utf8(metadata),\n'
        zba__aggv += (
            '                            unicode_to_utf8(compression),\n')
        zba__aggv += '                            _is_parallel, 0, 0, 0, 0,\n'
        zba__aggv += '                            unicode_to_utf8(name_ptr),\n'
        zba__aggv += (
            '                            unicode_to_utf8(bucket_region),\n')
        zba__aggv += '                            row_group_size,\n'
        zba__aggv += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        zba__aggv += (
            '                            unicode_to_utf8(_bodo_timestamp_tz))\n'
            )
        zba__aggv += '    delete_table_decref_arrays(table)\n'
        zba__aggv += '    delete_info_decref_array(index_col)\n'
        zba__aggv += '    delete_info_decref_array(col_names)\n'
    nksvu__xjzdm = {}
    if df.has_runtime_cols:
        yne__xps = None
    else:
        for rjulu__wwz in df.columns:
            if not isinstance(rjulu__wwz, str):
                raise BodoError(
                    'DataFrame.to_parquet(): parquet must have string column names'
                    )
        yne__xps = pd.array(df.columns)
    exec(zba__aggv, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array, 'delete_info_decref_array':
        delete_info_decref_array, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'col_names_arr': yne__xps,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'get_dataframe_table': get_dataframe_table,
        'col_names_no_parts_arr': jxg__sdpq, 'get_dataframe_column_names':
        get_dataframe_column_names, 'fix_arr_dtype': fix_arr_dtype,
        'decode_if_dict_array': decode_if_dict_array,
        'decode_if_dict_table': decode_if_dict_table}, nksvu__xjzdm)
    tkany__onjk = nksvu__xjzdm['df_to_parquet']
    return tkany__onjk


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_table_create=False, _is_parallel=False):
    lkc__djceo = 'all_ok'
    bawe__euxz, olgiy__yrlbv = bodo.ir.sql_ext.parse_dbtype(con)
    if _is_parallel and bodo.get_rank() == 0:
        eakk__wejty = 100
        if chunksize is None:
            asv__gnnxl = eakk__wejty
        else:
            asv__gnnxl = min(chunksize, eakk__wejty)
        if _is_table_create:
            df = df.iloc[:asv__gnnxl, :]
        else:
            df = df.iloc[asv__gnnxl:, :]
            if len(df) == 0:
                return lkc__djceo
    yas__rnatr = df.columns
    try:
        if bawe__euxz == 'oracle':
            import os
            import sqlalchemy as sa
            from sqlalchemy.dialects.oracle import VARCHAR2
            ptjoy__kob = os.environ.get('BODO_DISABLE_ORACLE_VARCHAR2', None)
            xiu__cnsxh = bodo.typeof(df)
            rnzbu__vmt = {}
            for crsf__qrtc, gclkg__uttu in zip(xiu__cnsxh.columns,
                xiu__cnsxh.data):
                if df[crsf__qrtc].dtype == 'object':
                    if gclkg__uttu == datetime_date_array_type:
                        rnzbu__vmt[crsf__qrtc] = sa.types.Date
                    elif gclkg__uttu in (bodo.string_array_type, bodo.
                        dict_str_arr_type) and (not ptjoy__kob or 
                        ptjoy__kob == '0'):
                        rnzbu__vmt[crsf__qrtc] = VARCHAR2(4000)
            dtype = rnzbu__vmt
        try:
            df.to_sql(name, con, schema, if_exists, index, index_label,
                chunksize, dtype, method)
        except Exception as qsaib__ggq:
            lkc__djceo = qsaib__ggq.args[0]
            if bawe__euxz == 'oracle' and 'ORA-12899' in lkc__djceo:
                lkc__djceo += """
                String is larger than VARCHAR2 maximum length.
                Please set environment variable `BODO_DISABLE_ORACLE_VARCHAR2` to
                disable Bodo's optimziation use of VARCHA2.
                NOTE: Oracle `to_sql` with CLOB datatypes is known to be really slow.
                """
        return lkc__djceo
    finally:
        df.columns = yas__rnatr


@numba.njit
def to_sql_exception_guard_encaps(df, name, con, schema=None, if_exists=
    'fail', index=True, index_label=None, chunksize=None, dtype=None,
    method=None, _is_table_create=False, _is_parallel=False):
    with numba.objmode(out='unicode_type'):
        out = to_sql_exception_guard(df, name, con, schema, if_exists,
            index, index_label, chunksize, dtype, method, _is_table_create,
            _is_parallel)
    return out


@overload_method(DataFrameType, 'to_sql')
def to_sql_overload(df, name, con, schema=None, if_exists='fail', index=
    True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_parallel=False):
    import warnings
    check_runtime_cols_unsupported(df, 'DataFrame.to_sql()')
    df: DataFrameType = df
    if is_overload_none(schema):
        if bodo.get_rank() == 0:
            import warnings
            warnings.warn(BodoWarning(
                f'DataFrame.to_sql(): schema argument is recommended to avoid permission issues when writing the table.'
                ))
    if not (is_overload_none(chunksize) or isinstance(chunksize, types.Integer)
        ):
        raise BodoError(
            "DataFrame.to_sql(): 'chunksize' argument must be an integer if provided."
            )
    from bodo.io.helpers import exception_propagating_thread_type
    from bodo.io.parquet_pio import parquet_write_table_cpp
    from bodo.io.snowflake import snowflake_connector_cursor_python_type
    try:
        from bodo import snowflake_sqlalchemy_compat
    except ImportError as xwdi__uares:
        pass
    if df.has_runtime_cols:
        yne__xps = None
    else:
        for rjulu__wwz in df.columns:
            if not isinstance(rjulu__wwz, str):
                raise BodoError(
                    'DataFrame.to_sql(): input dataframe must have string column names. Please return the DataFrame with runtime column names to regular Python to modify column names.'
                    )
        yne__xps = pd.array(df.columns)
    zba__aggv = 'def df_to_sql(\n'
    zba__aggv += '    df, name, con,\n'
    zba__aggv += (
        "    schema=None, if_exists='fail', index=True, index_label=None,\n")
    zba__aggv += (
        '    chunksize=None, dtype=None, method=None, _is_parallel=False,\n')
    zba__aggv += '):\n'
    zba__aggv += f"    if con.startswith('iceberg'):\n"
    zba__aggv += (
        f'        con_str = bodo.io.iceberg.format_iceberg_conn_njit(con)\n')
    zba__aggv += f'        if schema is None:\n'
    zba__aggv += f"""            raise ValueError('DataFrame.to_sql(): schema must be provided when writing to an Iceberg table.')
"""
    zba__aggv += f'        if chunksize is not None:\n'
    zba__aggv += f"""            raise ValueError('DataFrame.to_sql(): chunksize not supported for Iceberg tables.')
"""
    zba__aggv += f'        if index and bodo.get_rank() == 0:\n'
    zba__aggv += (
        f"            warnings.warn('index is not supported for Iceberg tables.')      \n"
        )
    zba__aggv += (
        f'        if index_label is not None and bodo.get_rank() == 0:\n')
    zba__aggv += (
        f"            warnings.warn('index_label is not supported for Iceberg tables.')\n"
        )
    if df.is_table_format:
        zba__aggv += f'        py_table = get_dataframe_table(df)\n'
        zba__aggv += (
            f'        table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        ealuq__bnlc = ', '.join(
            f'array_to_info(get_dataframe_data(df, {i}))' for i in range(
            len(df.columns)))
        zba__aggv += f'        info_list = [{ealuq__bnlc}]\n'
        zba__aggv += f'        table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        zba__aggv += (
            f'        columns_index = get_dataframe_column_names(df)\n')
        zba__aggv += f'        names_arr = index_to_array(columns_index)\n'
        zba__aggv += f'        col_names = array_to_info(names_arr)\n'
    else:
        zba__aggv += f'        col_names = array_to_info(col_names_arr)\n'
    zba__aggv += """        bodo.io.iceberg.iceberg_write(
            name, con_str, schema, table, col_names, if_exists,
            _is_parallel, pyarrow_table_schema,
        )
"""
    zba__aggv += f'        delete_table_decref_arrays(table)\n'
    zba__aggv += f'        delete_info_decref_array(col_names)\n'
    zba__aggv += "    elif con.startswith('snowflake'):\n"
    zba__aggv += """        if index and bodo.get_rank() == 0:
            warnings.warn('index is not supported for Snowflake tables.')      
        if index_label is not None and bodo.get_rank() == 0:
            warnings.warn('index_label is not supported for Snowflake tables.')
        ev = tracing.Event('snowflake_write_impl')
"""
    zba__aggv += "        location = ''\n"
    if not is_overload_none(schema):
        zba__aggv += '        location += \'"\' + schema + \'".\'\n'
    zba__aggv += '        location += \'"\' + name + \'"\'\n'
    zba__aggv += '        my_rank = bodo.get_rank()\n'
    zba__aggv += """        with bodo.objmode(
            cursor='snowflake_connector_cursor_type',
            tmp_folder='temporary_directory_type',
            stage_name='unicode_type',
            parquet_path='unicode_type',
            upload_using_snowflake_put='boolean',
            old_creds='DictType(unicode_type, unicode_type)',
        ):
            (
                cursor, tmp_folder, stage_name, parquet_path, upload_using_snowflake_put, old_creds
            ) = bodo.io.snowflake.connect_and_get_upload_info(con)
"""
    zba__aggv += '        bodo.barrier()\n'
    zba__aggv += '        if chunksize is None:\n'
    zba__aggv += """            ev_estimate_chunksize = tracing.Event('estimate_chunksize')          
"""
    if df.is_table_format and len(df.columns) > 0:
        zba__aggv += f"""            nbytes_arr = np.empty({len(df.columns)}, np.int64)
            table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, 0)
            memory_usage = np.sum(nbytes_arr)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        dfxm__njkgx = ',' if len(df.columns) == 1 else ''
        zba__aggv += (
            f'            memory_usage = np.array(({data}{dfxm__njkgx}), np.int64).sum()\n'
            )
    zba__aggv += """            nsplits = int(max(1, memory_usage / bodo.io.snowflake.SF_WRITE_PARQUET_CHUNK_SIZE))
            chunksize = max(1, (len(df) + nsplits - 1) // nsplits)
            ev_estimate_chunksize.finalize()
"""
    if df.has_runtime_cols:
        zba__aggv += '        columns_index = get_dataframe_column_names(df)\n'
        zba__aggv += '        names_arr = index_to_array(columns_index)\n'
        zba__aggv += '        col_names = array_to_info(names_arr)\n'
    else:
        zba__aggv += '        col_names = array_to_info(col_names_arr)\n'
    zba__aggv += '        index_col = array_to_info(np.empty(0))\n'
    zba__aggv += """        bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(parquet_path, parallel=_is_parallel)
"""
    zba__aggv += """        ev_upload_df = tracing.Event('upload_df', is_parallel=False)           
"""
    zba__aggv += '        upload_threads_in_progress = []\n'
    zba__aggv += """        for chunk_idx, i in enumerate(range(0, len(df), chunksize)):           
"""
    zba__aggv += """            chunk_name = f'file{chunk_idx}_rank{my_rank}_{bodo.io.helpers.uuid4_helper()}.parquet'
"""
    zba__aggv += '            chunk_path = parquet_path + chunk_name\n'
    zba__aggv += (
        '            chunk_path = chunk_path.replace("\\\\", "\\\\\\\\")\n')
    zba__aggv += (
        '            chunk_path = chunk_path.replace("\'", "\\\\\'")\n')
    zba__aggv += """            ev_to_df_table = tracing.Event(f'to_df_table_{chunk_idx}', is_parallel=False)
"""
    zba__aggv += '            chunk = df.iloc[i : i + chunksize]\n'
    if df.is_table_format:
        zba__aggv += (
            '            py_table_chunk = get_dataframe_table(chunk)\n')
        zba__aggv += """            table_chunk = py_table_to_cpp_table(py_table_chunk, py_table_typ)
"""
    else:
        gxh__eyory = ', '.join(
            f'array_to_info(get_dataframe_data(chunk, {i}))' for i in range
            (len(df.columns)))
        zba__aggv += (
            f'            table_chunk = arr_info_list_to_table([{gxh__eyory}])     \n'
            )
    zba__aggv += '            ev_to_df_table.finalize()\n'
    zba__aggv += """            ev_pq_write_cpp = tracing.Event(f'pq_write_cpp_{chunk_idx}', is_parallel=False)
            ev_pq_write_cpp.add_attribute('chunk_start', i)
            ev_pq_write_cpp.add_attribute('chunk_end', i + len(chunk))
            ev_pq_write_cpp.add_attribute('chunk_size', len(chunk))
            ev_pq_write_cpp.add_attribute('chunk_path', chunk_path)
            parquet_write_table_cpp(
                unicode_to_utf8(chunk_path),
                table_chunk, col_names, index_col,
                False,
                unicode_to_utf8('null'),
                unicode_to_utf8(bodo.io.snowflake.SF_WRITE_PARQUET_COMPRESSION),
                False,
                0,
                0, 0, 0,
                unicode_to_utf8('null'),
                unicode_to_utf8(bucket_region),
                chunksize,
                unicode_to_utf8('null'),
                unicode_to_utf8('UTC'),
            )
            ev_pq_write_cpp.finalize()
            delete_table_decref_arrays(table_chunk)
            if upload_using_snowflake_put:
                with bodo.objmode(upload_thread='types.optional(exception_propagating_thread_type)'):
                    upload_thread = bodo.io.snowflake.do_upload_and_cleanup(
                        cursor, chunk_idx, chunk_path, stage_name,
                    )
                if bodo.io.snowflake.SF_WRITE_OVERLAP_UPLOAD:
                    upload_threads_in_progress.append(upload_thread)
        delete_info_decref_array(index_col)
        delete_info_decref_array(col_names)
        if bodo.io.snowflake.SF_WRITE_OVERLAP_UPLOAD:
            with bodo.objmode():
                bodo.io.helpers.join_all_threads(upload_threads_in_progress)
        ev_upload_df.finalize()
"""
    zba__aggv += '        bodo.barrier()\n'
    zba__aggv += """        df_columns = df.columns
        with bodo.objmode():
            bodo.io.snowflake.create_table_copy_into(
                cursor, stage_name, location, df_columns, if_exists, old_creds, tmp_folder,
            )
"""
    zba__aggv += '        ev.finalize(sync=False)\n'
    zba__aggv += '    else:\n'
    zba__aggv += '        rank = bodo.libs.distributed_api.get_rank()\n'
    zba__aggv += "        err_msg = 'unset'\n"
    zba__aggv += '        if rank != 0:\n'
    zba__aggv += """            err_msg = bodo.libs.distributed_api.bcast_scalar(err_msg)          
"""
    zba__aggv += '        elif rank == 0:\n'
    zba__aggv += '            err_msg = to_sql_exception_guard_encaps(\n'
    zba__aggv += """                          df, name, con, schema, if_exists, index, index_label,
"""
    zba__aggv += '                          chunksize, dtype, method,\n'
    zba__aggv += '                          True, _is_parallel,\n'
    zba__aggv += '                      )\n'
    zba__aggv += """            err_msg = bodo.libs.distributed_api.bcast_scalar(err_msg)          
"""
    zba__aggv += "        if_exists = 'append'\n"
    zba__aggv += "        if _is_parallel and err_msg == 'all_ok':\n"
    zba__aggv += '            err_msg = to_sql_exception_guard_encaps(\n'
    zba__aggv += """                          df, name, con, schema, if_exists, index, index_label,
"""
    zba__aggv += '                          chunksize, dtype, method,\n'
    zba__aggv += '                          False, _is_parallel,\n'
    zba__aggv += '                      )\n'
    zba__aggv += "        if err_msg != 'all_ok':\n"
    zba__aggv += "            print('err_msg=', err_msg)\n"
    zba__aggv += (
        "            raise ValueError('error in to_sql() operation')\n")
    nksvu__xjzdm = {}
    trtb__set = globals().copy()
    trtb__set.update({'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info, 'bodo': bodo, 'col_names_arr':
        yne__xps, 'delete_info_decref_array': delete_info_decref_array,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'get_dataframe_column_names': get_dataframe_column_names,
        'get_dataframe_data': get_dataframe_data, 'get_dataframe_table':
        get_dataframe_table, 'index_to_array': index_to_array, 'np': np,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'pyarrow_table_schema': bodo.io.iceberg.pyarrow_schema(
        df), 'time': time, 'to_sql_exception_guard_encaps':
        to_sql_exception_guard_encaps, 'tracing': tracing,
        'unicode_to_utf8': unicode_to_utf8, 'warnings': warnings})
    exec(zba__aggv, trtb__set, nksvu__xjzdm)
    _impl = nksvu__xjzdm['df_to_sql']
    return _impl


@overload_method(DataFrameType, 'to_csv', no_unliteral=True)
def to_csv_overload(df, path_or_buf=None, sep=',', na_rep='', float_format=
    None, columns=None, header=True, index=True, index_label=None, mode='w',
    encoding=None, compression=None, quoting=None, quotechar='"',
    line_terminator=None, chunksize=None, date_format=None, doublequote=
    True, escapechar=None, decimal='.', errors='strict', storage_options=
    None, _bodo_file_prefix='part-'):
    check_runtime_cols_unsupported(df, 'DataFrame.to_csv()')
    check_unsupported_args('DataFrame.to_csv', {'encoding': encoding,
        'mode': mode, 'errors': errors, 'storage_options': storage_options},
        {'encoding': None, 'mode': 'w', 'errors': 'strict',
        'storage_options': None}, package_name='pandas', module_name='IO')
    if not (is_overload_none(path_or_buf) or is_overload_constant_str(
        path_or_buf) or path_or_buf == string_type):
        raise BodoError(
            "DataFrame.to_csv(): 'path_or_buf' argument should be None or string"
            )
    if not is_overload_none(compression):
        raise BodoError(
            "DataFrame.to_csv(): 'compression' argument supports only None, which is the default in JIT code."
            )
    if is_overload_constant_str(path_or_buf):
        xfo__calt = get_overload_const_str(path_or_buf)
        if xfo__calt.endswith(('.gz', '.bz2', '.zip', '.xz')):
            import warnings
            from bodo.utils.typing import BodoWarning
            warnings.warn(BodoWarning(
                "DataFrame.to_csv(): 'compression' argument defaults to None in JIT code, which is the only supported value."
                ))
    if not (is_overload_none(columns) or isinstance(columns, (types.List,
        types.Tuple))):
        raise BodoError(
            "DataFrame.to_csv(): 'columns' argument must be list a or tuple type."
            )
    if is_overload_none(path_or_buf):

        def _impl(df, path_or_buf=None, sep=',', na_rep='', float_format=
            None, columns=None, header=True, index=True, index_label=None,
            mode='w', encoding=None, compression=None, quoting=None,
            quotechar='"', line_terminator=None, chunksize=None,
            date_format=None, doublequote=True, escapechar=None, decimal=
            '.', errors='strict', storage_options=None, _bodo_file_prefix=
            'part-'):
            with numba.objmode(D='unicode_type'):
                D = df.to_csv(path_or_buf, sep, na_rep, float_format,
                    columns, header, index, index_label, mode, encoding,
                    compression, quoting, quotechar, line_terminator,
                    chunksize, date_format, doublequote, escapechar,
                    decimal, errors, storage_options)
            return D
        return _impl

    def _impl(df, path_or_buf=None, sep=',', na_rep='', float_format=None,
        columns=None, header=True, index=True, index_label=None, mode='w',
        encoding=None, compression=None, quoting=None, quotechar='"',
        line_terminator=None, chunksize=None, date_format=None, doublequote
        =True, escapechar=None, decimal='.', errors='strict',
        storage_options=None, _bodo_file_prefix='part-'):
        with numba.objmode(D='unicode_type'):
            D = df.to_csv(None, sep, na_rep, float_format, columns, header,
                index, index_label, mode, encoding, compression, quoting,
                quotechar, line_terminator, chunksize, date_format,
                doublequote, escapechar, decimal, errors, storage_options)
        bodo.io.fs_io.csv_write(path_or_buf, D, _bodo_file_prefix)
    return _impl


@overload_method(DataFrameType, 'to_json', no_unliteral=True)
def to_json_overload(df, path_or_buf=None, orient='records', date_format=
    None, double_precision=10, force_ascii=True, date_unit='ms',
    default_handler=None, lines=True, compression='infer', index=True,
    indent=None, storage_options=None, _bodo_file_prefix='part-'):
    check_runtime_cols_unsupported(df, 'DataFrame.to_json()')
    check_unsupported_args('DataFrame.to_json', {'storage_options':
        storage_options}, {'storage_options': None}, package_name='pandas',
        module_name='IO')
    if path_or_buf is None or path_or_buf == types.none:

        def _impl(df, path_or_buf=None, orient='records', date_format=None,
            double_precision=10, force_ascii=True, date_unit='ms',
            default_handler=None, lines=True, compression='infer', index=
            True, indent=None, storage_options=None, _bodo_file_prefix='part-'
            ):
            with numba.objmode(D='unicode_type'):
                D = df.to_json(path_or_buf, orient, date_format,
                    double_precision, force_ascii, date_unit,
                    default_handler, lines, compression, index, indent,
                    storage_options)
            return D
        return _impl

    def _impl(df, path_or_buf=None, orient='records', date_format=None,
        double_precision=10, force_ascii=True, date_unit='ms',
        default_handler=None, lines=True, compression='infer', index=True,
        indent=None, storage_options=None, _bodo_file_prefix='part-'):
        with numba.objmode(D='unicode_type'):
            D = df.to_json(None, orient, date_format, double_precision,
                force_ascii, date_unit, default_handler, lines, compression,
                index, indent, storage_options)
        xwgpf__qwip = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(xwgpf__qwip), unicode_to_utf8(
                _bodo_file_prefix))
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(xwgpf__qwip), unicode_to_utf8(
                _bodo_file_prefix))
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    gnd__omfo = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    owig__obn = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pandas.get_dummies', gnd__omfo, owig__obn,
        package_name='pandas', module_name='General')
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pandas.get_dummies() only support categorical data types with explicitly known categories'
            )
    zba__aggv = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        diuz__wtbgz = data.data.dtype.categories
        zba__aggv += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        diuz__wtbgz = data.dtype.categories
        zba__aggv += '  data_values = data\n'
    oym__zcprq = len(diuz__wtbgz)
    zba__aggv += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    zba__aggv += '  numba.parfors.parfor.init_prange()\n'
    zba__aggv += '  n = len(data_values)\n'
    for i in range(oym__zcprq):
        zba__aggv += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    zba__aggv += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    zba__aggv += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for umu__fumnq in range(oym__zcprq):
        zba__aggv += '          data_arr_{}[i] = 0\n'.format(umu__fumnq)
    zba__aggv += '      else:\n'
    for ilo__sxys in range(oym__zcprq):
        zba__aggv += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            ilo__sxys)
    ealuq__bnlc = ', '.join(f'data_arr_{i}' for i in range(oym__zcprq))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    if isinstance(diuz__wtbgz[0], np.datetime64):
        diuz__wtbgz = tuple(pd.Timestamp(crsf__qrtc) for crsf__qrtc in
            diuz__wtbgz)
    elif isinstance(diuz__wtbgz[0], np.timedelta64):
        diuz__wtbgz = tuple(pd.Timedelta(crsf__qrtc) for crsf__qrtc in
            diuz__wtbgz)
    return bodo.hiframes.dataframe_impl._gen_init_df(zba__aggv, diuz__wtbgz,
        ealuq__bnlc, index)


def categorical_can_construct_dataframe(val):
    if isinstance(val, CategoricalArrayType):
        return val.dtype.categories is not None
    elif isinstance(val, SeriesType) and isinstance(val.data,
        CategoricalArrayType):
        return val.data.dtype.categories is not None
    return False


def handle_inplace_df_type_change(inplace, _bodo_transformed, func_name):
    if is_overload_false(_bodo_transformed
        ) and bodo.transforms.typing_pass.in_partial_typing and (
        is_overload_true(inplace) or not is_overload_constant_bool(inplace)):
        bodo.transforms.typing_pass.typing_transform_required = True
        raise Exception('DataFrame.{}(): transform necessary for inplace'.
            format(func_name))


pd_unsupported = (pd.read_pickle, pd.read_table, pd.read_fwf, pd.
    read_clipboard, pd.ExcelFile, pd.read_html, pd.read_xml, pd.read_hdf,
    pd.read_feather, pd.read_orc, pd.read_sas, pd.read_spss, pd.
    read_sql_query, pd.read_gbq, pd.read_stata, pd.ExcelWriter, pd.
    json_normalize, pd.merge_ordered, pd.factorize, pd.wide_to_long, pd.
    bdate_range, pd.period_range, pd.infer_freq, pd.interval_range, pd.eval,
    pd.test, pd.Grouper)
pd_util_unsupported = pd.util.hash_array, pd.util.hash_pandas_object
dataframe_unsupported = ['set_flags', 'convert_dtypes', 'bool', '__iter__',
    'items', 'iteritems', 'keys', 'iterrows', 'lookup', 'pop', 'xs', 'get',
    'add', 'sub', 'mul', 'div', 'truediv', 'floordiv', 'mod', 'pow', 'dot',
    'radd', 'rsub', 'rmul', 'rdiv', 'rtruediv', 'rfloordiv', 'rmod', 'rpow',
    'lt', 'gt', 'le', 'ge', 'ne', 'eq', 'combine', 'combine_first',
    'subtract', 'divide', 'multiply', 'applymap', 'agg', 'aggregate',
    'transform', 'expanding', 'ewm', 'all', 'any', 'clip', 'corrwith',
    'cummax', 'cummin', 'eval', 'kurt', 'kurtosis', 'mad', 'mode', 'round',
    'sem', 'skew', 'value_counts', 'add_prefix', 'add_suffix', 'align',
    'at_time', 'between_time', 'equals', 'reindex', 'reindex_like',
    'rename_axis', 'set_axis', 'truncate', 'backfill', 'bfill', 'ffill',
    'interpolate', 'pad', 'droplevel', 'reorder_levels', 'nlargest',
    'nsmallest', 'swaplevel', 'stack', 'unstack', 'swapaxes', 'squeeze',
    'to_xarray', 'T', 'transpose', 'compare', 'update', 'asfreq', 'asof',
    'slice_shift', 'tshift', 'first_valid_index', 'last_valid_index',
    'resample', 'to_period', 'to_timestamp', 'tz_convert', 'tz_localize',
    'boxplot', 'hist', 'from_dict', 'from_records', 'to_pickle', 'to_hdf',
    'to_dict', 'to_excel', 'to_html', 'to_feather', 'to_latex', 'to_stata',
    'to_gbq', 'to_records', 'to_clipboard', 'to_markdown', 'to_xml']
dataframe_unsupported_attrs = ['at', 'attrs', 'axes', 'flags', 'style',
    'sparse']


def _install_pd_unsupported(mod_name, pd_unsupported):
    for huzd__ltj in pd_unsupported:
        fyinv__lwxp = mod_name + '.' + huzd__ltj.__name__
        overload(huzd__ltj, no_unliteral=True)(create_unsupported_overload(
            fyinv__lwxp))


def _install_dataframe_unsupported():
    for yre__reprg in dataframe_unsupported_attrs:
        sbc__uiwgp = 'DataFrame.' + yre__reprg
        overload_attribute(DataFrameType, yre__reprg)(
            create_unsupported_overload(sbc__uiwgp))
    for fyinv__lwxp in dataframe_unsupported:
        sbc__uiwgp = 'DataFrame.' + fyinv__lwxp + '()'
        overload_method(DataFrameType, fyinv__lwxp)(create_unsupported_overload
            (sbc__uiwgp))


_install_pd_unsupported('pandas', pd_unsupported)
_install_pd_unsupported('pandas.util', pd_util_unsupported)
_install_dataframe_unsupported()
