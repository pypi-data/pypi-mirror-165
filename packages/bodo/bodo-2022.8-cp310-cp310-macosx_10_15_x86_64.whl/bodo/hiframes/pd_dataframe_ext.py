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
            qar__bslbh = f'{len(self.data)} columns of types {set(self.data)}'
            eiu__wksvq = (
                f"('{self.columns[0]}', '{self.columns[1]}', ..., '{self.columns[-1]}')"
                )
            return (
                f'dataframe({qar__bslbh}, {self.index}, {eiu__wksvq}, {self.dist}, {self.is_table_format}, {self.has_runtime_cols})'
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
        return {aroc__rhq: i for i, aroc__rhq in enumerate(self.columns)}

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
            lqf__hdc = (self.index if self.index == other.index else self.
                index.unify(typingctx, other.index))
            data = tuple(asu__utvp.unify(typingctx, qrpq__kme) if asu__utvp !=
                qrpq__kme else asu__utvp for asu__utvp, qrpq__kme in zip(
                self.data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if lqf__hdc is not None and None not in data:
                return DataFrameType(data, lqf__hdc, self.columns, dist,
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
        return all(asu__utvp.is_precise() for asu__utvp in self.data
            ) and self.index.is_precise()

    def replace_col_type(self, col_name, new_type):
        if col_name not in self.columns:
            raise ValueError(
                f"DataFrameType.replace_col_type replaced column must be found in the DataFrameType. '{col_name}' not found in DataFrameType with columns {self.columns}"
                )
        wgjdy__gbfp = self.columns.index(col_name)
        xle__nuzck = tuple(list(self.data[:wgjdy__gbfp]) + [new_type] +
            list(self.data[wgjdy__gbfp + 1:]))
        return DataFrameType(xle__nuzck, self.index, self.columns, self.
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
        rilj__rdrlb = [('data', data_typ), ('index', fe_type.df_type.index),
            ('parent', types.pyobject)]
        if fe_type.df_type.has_runtime_cols:
            rilj__rdrlb.append(('columns', fe_type.df_type.runtime_colname_typ)
                )
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, rilj__rdrlb)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        rilj__rdrlb = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, rilj__rdrlb)


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
        luxy__frgfu = 'n',
        ipcab__isw = {'n': 5}
        hqi__hwduc, ftx__fmywr = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, luxy__frgfu, ipcab__isw)
        vdf__mkbm = ftx__fmywr[0]
        if not is_overload_int(vdf__mkbm):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        sopu__pok = df.copy()
        return sopu__pok(*ftx__fmywr).replace(pysig=hqi__hwduc)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        zypru__mfrwt = (df,) + args
        luxy__frgfu = 'df', 'method', 'min_periods'
        ipcab__isw = {'method': 'pearson', 'min_periods': 1}
        xmcub__iivg = 'method',
        hqi__hwduc, ftx__fmywr = bodo.utils.typing.fold_typing_args(func_name,
            zypru__mfrwt, kws, luxy__frgfu, ipcab__isw, xmcub__iivg)
        tkxd__rih = ftx__fmywr[2]
        if not is_overload_int(tkxd__rih):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        jwxcc__axgj = []
        migy__kkg = []
        for aroc__rhq, ukm__ces in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(ukm__ces.dtype):
                jwxcc__axgj.append(aroc__rhq)
                migy__kkg.append(types.Array(types.float64, 1, 'A'))
        if len(jwxcc__axgj) == 0:
            raise_bodo_error('DataFrame.corr(): requires non-empty dataframe')
        migy__kkg = tuple(migy__kkg)
        jwxcc__axgj = tuple(jwxcc__axgj)
        index_typ = bodo.utils.typing.type_col_to_index(jwxcc__axgj)
        sopu__pok = DataFrameType(migy__kkg, index_typ, jwxcc__axgj)
        return sopu__pok(*ftx__fmywr).replace(pysig=hqi__hwduc)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.apply()')
        kws = dict(kws)
        bkhqh__pishf = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        ksm__tolkr = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        vtqjb__fzyb = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        zcni__hqygs = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        diakf__btaud = dict(raw=ksm__tolkr, result_type=vtqjb__fzyb)
        cdfnp__uluy = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', diakf__btaud, cdfnp__uluy,
            package_name='pandas', module_name='DataFrame')
        rsd__uke = True
        if types.unliteral(bkhqh__pishf) == types.unicode_type:
            if not is_overload_constant_str(bkhqh__pishf):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            rsd__uke = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        ada__ymqwc = get_overload_const_int(axis)
        if rsd__uke and ada__ymqwc != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif ada__ymqwc not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        skpyx__uzir = []
        for arr_typ in df.data:
            hyo__fdis = SeriesType(arr_typ.dtype, arr_typ, df.index,
                string_type)
            ljnii__ura = self.context.resolve_function_type(operator.
                getitem, (SeriesIlocType(hyo__fdis), types.int64), {}
                ).return_type
            skpyx__uzir.append(ljnii__ura)
        tjcr__wck = types.none
        dvf__qojj = HeterogeneousIndexType(types.BaseTuple.from_types(tuple
            (types.literal(aroc__rhq) for aroc__rhq in df.columns)), None)
        vif__fik = types.BaseTuple.from_types(skpyx__uzir)
        csrda__ddyg = types.Tuple([types.bool_] * len(vif__fik))
        jkajy__dmz = bodo.NullableTupleType(vif__fik, csrda__ddyg)
        kmtn__effs = df.index.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df.index,
            'DataFrame.apply()')
        if kmtn__effs == types.NPDatetime('ns'):
            kmtn__effs = bodo.pd_timestamp_type
        if kmtn__effs == types.NPTimedelta('ns'):
            kmtn__effs = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(vif__fik):
            zfw__ubzuo = HeterogeneousSeriesType(jkajy__dmz, dvf__qojj,
                kmtn__effs)
        else:
            zfw__ubzuo = SeriesType(vif__fik.dtype, jkajy__dmz, dvf__qojj,
                kmtn__effs)
        mxyyy__uyrf = zfw__ubzuo,
        if zcni__hqygs is not None:
            mxyyy__uyrf += tuple(zcni__hqygs.types)
        try:
            if not rsd__uke:
                sdrlf__yeoct = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(bkhqh__pishf), self.context,
                    'DataFrame.apply', axis if ada__ymqwc == 1 else None)
            else:
                sdrlf__yeoct = get_const_func_output_type(bkhqh__pishf,
                    mxyyy__uyrf, kws, self.context, numba.core.registry.
                    cpu_target.target_context)
        except Exception as lataz__chkc:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()',
                lataz__chkc))
        if rsd__uke:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(sdrlf__yeoct, (SeriesType, HeterogeneousSeriesType)
                ) and sdrlf__yeoct.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(sdrlf__yeoct, HeterogeneousSeriesType):
                xmfj__iktc, adqw__grth = sdrlf__yeoct.const_info
                if isinstance(sdrlf__yeoct.data, bodo.libs.
                    nullable_tuple_ext.NullableTupleType):
                    ycq__rgtx = sdrlf__yeoct.data.tuple_typ.types
                elif isinstance(sdrlf__yeoct.data, types.Tuple):
                    ycq__rgtx = sdrlf__yeoct.data.types
                else:
                    raise_bodo_error(
                        'df.apply(): Unexpected Series return type for Heterogeneous data'
                        )
                dojq__iuvhs = tuple(to_nullable_type(dtype_to_array_type(
                    yia__dek)) for yia__dek in ycq__rgtx)
                lol__ihcy = DataFrameType(dojq__iuvhs, df.index, adqw__grth)
            elif isinstance(sdrlf__yeoct, SeriesType):
                zhhno__ruq, adqw__grth = sdrlf__yeoct.const_info
                dojq__iuvhs = tuple(to_nullable_type(dtype_to_array_type(
                    sdrlf__yeoct.dtype)) for xmfj__iktc in range(zhhno__ruq))
                lol__ihcy = DataFrameType(dojq__iuvhs, df.index, adqw__grth)
            else:
                pfmv__rwnnr = get_udf_out_arr_type(sdrlf__yeoct)
                lol__ihcy = SeriesType(pfmv__rwnnr.dtype, pfmv__rwnnr, df.
                    index, None)
        else:
            lol__ihcy = sdrlf__yeoct
        elsvq__ezclm = ', '.join("{} = ''".format(asu__utvp) for asu__utvp in
            kws.keys())
        uwro__kjzx = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {elsvq__ezclm}):
"""
        uwro__kjzx += '    pass\n'
        zeto__ixtc = {}
        exec(uwro__kjzx, {}, zeto__ixtc)
        lpal__ovs = zeto__ixtc['apply_stub']
        hqi__hwduc = numba.core.utils.pysignature(lpal__ovs)
        dguk__yxzt = (bkhqh__pishf, axis, ksm__tolkr, vtqjb__fzyb, zcni__hqygs
            ) + tuple(kws.values())
        return signature(lol__ihcy, *dguk__yxzt).replace(pysig=hqi__hwduc)

    @bound_function('df.plot', no_unliteral=True)
    def resolve_plot(self, df, args, kws):
        func_name = 'DataFrame.plot'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        luxy__frgfu = ('x', 'y', 'kind', 'figsize', 'ax', 'subplots',
            'sharex', 'sharey', 'layout', 'use_index', 'title', 'grid',
            'legend', 'style', 'logx', 'logy', 'loglog', 'xticks', 'yticks',
            'xlim', 'ylim', 'rot', 'fontsize', 'colormap', 'table', 'yerr',
            'xerr', 'secondary_y', 'sort_columns', 'xlabel', 'ylabel',
            'position', 'stacked', 'mark_right', 'include_bool', 'backend')
        ipcab__isw = {'x': None, 'y': None, 'kind': 'line', 'figsize': None,
            'ax': None, 'subplots': False, 'sharex': None, 'sharey': False,
            'layout': None, 'use_index': True, 'title': None, 'grid': None,
            'legend': True, 'style': None, 'logx': False, 'logy': False,
            'loglog': False, 'xticks': None, 'yticks': None, 'xlim': None,
            'ylim': None, 'rot': None, 'fontsize': None, 'colormap': None,
            'table': False, 'yerr': None, 'xerr': None, 'secondary_y': 
            False, 'sort_columns': False, 'xlabel': None, 'ylabel': None,
            'position': 0.5, 'stacked': False, 'mark_right': True,
            'include_bool': False, 'backend': None}
        xmcub__iivg = ('subplots', 'sharex', 'sharey', 'layout',
            'use_index', 'grid', 'style', 'logx', 'logy', 'loglog', 'xlim',
            'ylim', 'rot', 'colormap', 'table', 'yerr', 'xerr',
            'sort_columns', 'secondary_y', 'colorbar', 'position',
            'stacked', 'mark_right', 'include_bool', 'backend')
        hqi__hwduc, ftx__fmywr = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, luxy__frgfu, ipcab__isw, xmcub__iivg)
        myro__jgfvz = ftx__fmywr[2]
        if not is_overload_constant_str(myro__jgfvz):
            raise BodoError(
                f"{func_name}: kind must be a constant string and one of ('line', 'scatter')."
                )
        ckw__fjoi = ftx__fmywr[0]
        if not is_overload_none(ckw__fjoi) and not (is_overload_int(
            ckw__fjoi) or is_overload_constant_str(ckw__fjoi)):
            raise BodoError(
                f'{func_name}: x must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(ckw__fjoi):
            phl__wcnv = get_overload_const_str(ckw__fjoi)
            if phl__wcnv not in df.columns:
                raise BodoError(f'{func_name}: {phl__wcnv} column not found.')
        elif is_overload_int(ckw__fjoi):
            fayj__mrb = get_overload_const_int(ckw__fjoi)
            if fayj__mrb > len(df.columns):
                raise BodoError(
                    f'{func_name}: x: {fayj__mrb} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            ckw__fjoi = df.columns[ckw__fjoi]
        zoahb__brtk = ftx__fmywr[1]
        if not is_overload_none(zoahb__brtk) and not (is_overload_int(
            zoahb__brtk) or is_overload_constant_str(zoahb__brtk)):
            raise BodoError(
                'df.plot(): y must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(zoahb__brtk):
            xmfcc__syvtl = get_overload_const_str(zoahb__brtk)
            if xmfcc__syvtl not in df.columns:
                raise BodoError(
                    f'{func_name}: {xmfcc__syvtl} column not found.')
        elif is_overload_int(zoahb__brtk):
            hxszf__ffj = get_overload_const_int(zoahb__brtk)
            if hxszf__ffj > len(df.columns):
                raise BodoError(
                    f'{func_name}: y: {hxszf__ffj} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            zoahb__brtk = df.columns[zoahb__brtk]
        vxdfb__xom = ftx__fmywr[3]
        if not is_overload_none(vxdfb__xom) and not is_tuple_like_type(
            vxdfb__xom):
            raise BodoError(
                f'{func_name}: figsize must be a constant numeric tuple (width, height) or None.'
                )
        pnqp__wzztg = ftx__fmywr[10]
        if not is_overload_none(pnqp__wzztg) and not is_overload_constant_str(
            pnqp__wzztg):
            raise BodoError(
                f'{func_name}: title must be a constant string or None.')
        bovrn__ntixz = ftx__fmywr[12]
        if not is_overload_bool(bovrn__ntixz):
            raise BodoError(f'{func_name}: legend must be a boolean type.')
        sqag__llkd = ftx__fmywr[17]
        if not is_overload_none(sqag__llkd) and not is_tuple_like_type(
            sqag__llkd):
            raise BodoError(
                f'{func_name}: xticks must be a constant tuple or None.')
        xjxi__mbrz = ftx__fmywr[18]
        if not is_overload_none(xjxi__mbrz) and not is_tuple_like_type(
            xjxi__mbrz):
            raise BodoError(
                f'{func_name}: yticks must be a constant tuple or None.')
        eonw__ngm = ftx__fmywr[22]
        if not is_overload_none(eonw__ngm) and not is_overload_int(eonw__ngm):
            raise BodoError(
                f'{func_name}: fontsize must be an integer or None.')
        rqoxl__jhm = ftx__fmywr[29]
        if not is_overload_none(rqoxl__jhm) and not is_overload_constant_str(
            rqoxl__jhm):
            raise BodoError(
                f'{func_name}: xlabel must be a constant string or None.')
        lfnk__hwjt = ftx__fmywr[30]
        if not is_overload_none(lfnk__hwjt) and not is_overload_constant_str(
            lfnk__hwjt):
            raise BodoError(
                f'{func_name}: ylabel must be a constant string or None.')
        mgis__lham = types.List(types.mpl_line_2d_type)
        myro__jgfvz = get_overload_const_str(myro__jgfvz)
        if myro__jgfvz == 'scatter':
            if is_overload_none(ckw__fjoi) and is_overload_none(zoahb__brtk):
                raise BodoError(
                    f'{func_name}: {myro__jgfvz} requires an x and y column.')
            elif is_overload_none(ckw__fjoi):
                raise BodoError(
                    f'{func_name}: {myro__jgfvz} x column is missing.')
            elif is_overload_none(zoahb__brtk):
                raise BodoError(
                    f'{func_name}: {myro__jgfvz} y column is missing.')
            mgis__lham = types.mpl_path_collection_type
        elif myro__jgfvz != 'line':
            raise BodoError(
                f'{func_name}: {myro__jgfvz} plot is not supported.')
        return signature(mgis__lham, *ftx__fmywr).replace(pysig=hqi__hwduc)

    def generic_resolve(self, df, attr):
        if self._is_existing_attr(attr):
            return
        check_runtime_cols_unsupported(df,
            'Acessing DataFrame columns by attribute')
        if attr in df.columns:
            zqveo__ucog = df.columns.index(attr)
            arr_typ = df.data[zqveo__ucog]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            pyv__noku = []
            xle__nuzck = []
            vob__yjmbp = False
            for i, mba__koncb in enumerate(df.columns):
                if mba__koncb[0] != attr:
                    continue
                vob__yjmbp = True
                pyv__noku.append(mba__koncb[1] if len(mba__koncb) == 2 else
                    mba__koncb[1:])
                xle__nuzck.append(df.data[i])
            if vob__yjmbp:
                return DataFrameType(tuple(xle__nuzck), df.index, tuple(
                    pyv__noku))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        onjk__ltazd = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(onjk__ltazd)
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
        mct__xxqw = builder.extract_value(payload.data, i)
        context.nrt.decref(builder, df_type.data[i], mct__xxqw)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    plin__ktduj = builder.module
    rmypo__pst = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    fpf__vlaek = cgutils.get_or_insert_function(plin__ktduj, rmypo__pst,
        name='.dtor.df.{}'.format(df_type))
    if not fpf__vlaek.is_declaration:
        return fpf__vlaek
    fpf__vlaek.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(fpf__vlaek.append_basic_block())
    swwfm__ektl = fpf__vlaek.args[0]
    igup__crsk = context.get_value_type(payload_type).as_pointer()
    fkhqm__emoah = builder.bitcast(swwfm__ektl, igup__crsk)
    payload = context.make_helper(builder, payload_type, ref=fkhqm__emoah)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        dhoa__siwig = context.get_python_api(builder)
        hcdfu__bqln = dhoa__siwig.gil_ensure()
        dhoa__siwig.decref(payload.parent)
        dhoa__siwig.gil_release(hcdfu__bqln)
    builder.ret_void()
    return fpf__vlaek


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    parent=None, colnames=None):
    payload_type = DataFramePayloadType(df_type)
    nlfe__uae = cgutils.create_struct_proxy(payload_type)(context, builder)
    nlfe__uae.data = data_tup
    nlfe__uae.index = index_val
    if colnames is not None:
        assert df_type.has_runtime_cols, 'construct_dataframe can only provide colnames if columns are determined at runtime'
        nlfe__uae.columns = colnames
    msfs__eacae = context.get_value_type(payload_type)
    ujdrk__hnsl = context.get_abi_sizeof(msfs__eacae)
    lrj__qyt = define_df_dtor(context, builder, df_type, payload_type)
    djgqa__tgl = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, ujdrk__hnsl), lrj__qyt)
    jonsz__bvsj = context.nrt.meminfo_data(builder, djgqa__tgl)
    xgdwr__eidm = builder.bitcast(jonsz__bvsj, msfs__eacae.as_pointer())
    toz__lufd = cgutils.create_struct_proxy(df_type)(context, builder)
    toz__lufd.meminfo = djgqa__tgl
    if parent is None:
        toz__lufd.parent = cgutils.get_null_value(toz__lufd.parent.type)
    else:
        toz__lufd.parent = parent
        nlfe__uae.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            dhoa__siwig = context.get_python_api(builder)
            hcdfu__bqln = dhoa__siwig.gil_ensure()
            dhoa__siwig.incref(parent)
            dhoa__siwig.gil_release(hcdfu__bqln)
    builder.store(nlfe__uae._getvalue(), xgdwr__eidm)
    return toz__lufd._getvalue()


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
        pcn__fdwfn = [data_typ.dtype.arr_types.dtype] * len(data_typ.dtype.
            arr_types)
    else:
        pcn__fdwfn = [yia__dek for yia__dek in data_typ.dtype.arr_types]
    ekt__ecv = DataFrameType(tuple(pcn__fdwfn + [colnames_index_typ]),
        index_typ, None, is_table_format=True)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup, index, col_names = args
        parent = None
        kvg__knoug = construct_dataframe(context, builder, df_type,
            data_tup, index, parent, col_names)
        context.nrt.incref(builder, data_typ, data_tup)
        context.nrt.incref(builder, index_typ, index)
        context.nrt.incref(builder, colnames_index_typ, col_names)
        return kvg__knoug
    sig = signature(ekt__ecv, data_typ, index_typ, colnames_index_typ)
    return sig, codegen


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    zhhno__ruq = len(data_tup_typ.types)
    if zhhno__ruq == 0:
        column_names = ()
    nsi__dqaq = col_names_typ.instance_type if isinstance(col_names_typ,
        types.TypeRef) else col_names_typ
    assert isinstance(nsi__dqaq, ColNamesMetaType) and isinstance(nsi__dqaq
        .meta, tuple
        ), 'Third argument to init_dataframe must be of type ColNamesMetaType, and must contain a tuple of column names'
    column_names = nsi__dqaq.meta
    if zhhno__ruq == 1 and isinstance(data_tup_typ.types[0], TableType):
        zhhno__ruq = len(data_tup_typ.types[0].arr_types)
    assert len(column_names
        ) == zhhno__ruq, 'init_dataframe(): number of column names does not match number of columns'
    is_table_format = False
    vroe__xkuz = data_tup_typ.types
    if zhhno__ruq != 0 and isinstance(data_tup_typ.types[0], TableType):
        vroe__xkuz = data_tup_typ.types[0].arr_types
        is_table_format = True
    ekt__ecv = DataFrameType(vroe__xkuz, index_typ, column_names,
        is_table_format=is_table_format)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        parent = None
        if is_table_format:
            xvj__flg = cgutils.create_struct_proxy(ekt__ecv.table_type)(context
                , builder, builder.extract_value(data_tup, 0))
            parent = xvj__flg.parent
        kvg__knoug = construct_dataframe(context, builder, df_type,
            data_tup, index_val, parent, None)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return kvg__knoug
    sig = signature(ekt__ecv, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):
    check_runtime_cols_unsupported(df, 'has_parent')

    def codegen(context, builder, sig, args):
        toz__lufd = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, toz__lufd.parent)
    return signature(types.bool_, df), codegen


@intrinsic
def _column_needs_unboxing(typingctx, df_typ, i_typ=None):
    check_runtime_cols_unsupported(df_typ, '_column_needs_unboxing')
    assert isinstance(df_typ, DataFrameType) and is_overload_constant_int(i_typ
        )

    def codegen(context, builder, sig, args):
        nlfe__uae = get_dataframe_payload(context, builder, df_typ, args[0])
        ndvn__bfvc = get_overload_const_int(i_typ)
        arr_typ = df_typ.data[ndvn__bfvc]
        if df_typ.is_table_format:
            xvj__flg = cgutils.create_struct_proxy(df_typ.table_type)(context,
                builder, builder.extract_value(nlfe__uae.data, 0))
            krai__anp = df_typ.table_type.type_to_blk[arr_typ]
            biwg__vla = getattr(xvj__flg, f'block_{krai__anp}')
            evnd__alnwc = ListInstance(context, builder, types.List(arr_typ
                ), biwg__vla)
            kfdhl__fik = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[ndvn__bfvc])
            mct__xxqw = evnd__alnwc.getitem(kfdhl__fik)
        else:
            mct__xxqw = builder.extract_value(nlfe__uae.data, ndvn__bfvc)
        shkad__yxlgk = cgutils.alloca_once_value(builder, mct__xxqw)
        fzya__flz = cgutils.alloca_once_value(builder, context.
            get_constant_null(arr_typ))
        return is_ll_eq(builder, shkad__yxlgk, fzya__flz)
    return signature(types.bool_, df_typ, i_typ), codegen


def get_dataframe_payload(context, builder, df_type, value):
    djgqa__tgl = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, djgqa__tgl)
    igup__crsk = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, igup__crsk)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, '_get_dataframe_data')
    ekt__ecv = types.Tuple(df_typ.data)
    if df_typ.is_table_format:
        ekt__ecv = types.Tuple([TableType(df_typ.data)])
    sig = signature(ekt__ecv, df_typ)

    def codegen(context, builder, signature, args):
        nlfe__uae = get_dataframe_payload(context, builder, signature.args[
            0], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            nlfe__uae.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):

    def codegen(context, builder, signature, args):
        nlfe__uae = get_dataframe_payload(context, builder, signature.args[
            0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index, nlfe__uae.
            index)
    ekt__ecv = df_typ.index
    sig = signature(ekt__ecv, df_typ)
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
        sopu__pok = df.data[i]
        return sopu__pok(*args)


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
        nlfe__uae = get_dataframe_payload(context, builder, signature.args[
            0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.table_type,
            builder.extract_value(nlfe__uae.data, 0))
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
    yagap__nxqv = ',' if len(df.columns) > 1 else ''
    return eval(f'lambda df: ({data}{yagap__nxqv})', {'bodo': bodo})


@infer_global(get_dataframe_all_data)
class GetDataFrameAllDataInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        df_type = args[0]
        check_runtime_cols_unsupported(df_type, 'get_dataframe_data')
        sopu__pok = (df_type.table_type if df_type.is_table_format else
            types.BaseTuple.from_types(df_type.data))
        return sopu__pok(*args)


@lower_builtin(get_dataframe_all_data, DataFrameType)
def lower_get_dataframe_all_data(context, builder, sig, args):
    impl = get_dataframe_all_data_impl(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@intrinsic
def get_dataframe_column_names(typingctx, df_typ=None):
    assert df_typ.has_runtime_cols, 'get_dataframe_column_names() expects columns to be determined at runtime'

    def codegen(context, builder, signature, args):
        nlfe__uae = get_dataframe_payload(context, builder, signature.args[
            0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.
            runtime_colname_typ, nlfe__uae.columns)
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
    vif__fik = self.typemap[data_tup.name]
    if any(is_tuple_like_type(yia__dek) for yia__dek in vif__fik.types):
        return None
    if equiv_set.has_shape(data_tup):
        aazvi__uqzr = equiv_set.get_shape(data_tup)
        if len(aazvi__uqzr) > 1:
            equiv_set.insert_equiv(*aazvi__uqzr)
        if len(aazvi__uqzr) > 0:
            dvf__qojj = self.typemap[index.name]
            if not isinstance(dvf__qojj, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(aazvi__uqzr[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(aazvi__uqzr[0], len(
                aazvi__uqzr)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    izjmz__iawd = args[0]
    data_types = self.typemap[izjmz__iawd.name].data
    if any(is_tuple_like_type(yia__dek) for yia__dek in data_types):
        return None
    if equiv_set.has_shape(izjmz__iawd):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            izjmz__iawd)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    izjmz__iawd = args[0]
    dvf__qojj = self.typemap[izjmz__iawd.name].index
    if isinstance(dvf__qojj, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(izjmz__iawd):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            izjmz__iawd)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


def get_dataframe_table_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    izjmz__iawd = args[0]
    if equiv_set.has_shape(izjmz__iawd):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            izjmz__iawd), pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_table
    ) = get_dataframe_table_equiv


def get_dataframe_column_names_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    izjmz__iawd = args[0]
    if equiv_set.has_shape(izjmz__iawd):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            izjmz__iawd)[1], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_column_names
    ) = get_dataframe_column_names_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    check_runtime_cols_unsupported(df_typ, 'set_dataframe_data')
    assert is_overload_constant_int(c_ind_typ)
    ndvn__bfvc = get_overload_const_int(c_ind_typ)
    if df_typ.data[ndvn__bfvc] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        xyvoi__bkpy, xmfj__iktc, puvyc__rwd = args
        nlfe__uae = get_dataframe_payload(context, builder, df_typ, xyvoi__bkpy
            )
        if df_typ.is_table_format:
            xvj__flg = cgutils.create_struct_proxy(df_typ.table_type)(context,
                builder, builder.extract_value(nlfe__uae.data, 0))
            krai__anp = df_typ.table_type.type_to_blk[arr_typ]
            biwg__vla = getattr(xvj__flg, f'block_{krai__anp}')
            evnd__alnwc = ListInstance(context, builder, types.List(arr_typ
                ), biwg__vla)
            kfdhl__fik = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[ndvn__bfvc])
            evnd__alnwc.setitem(kfdhl__fik, puvyc__rwd, True)
        else:
            mct__xxqw = builder.extract_value(nlfe__uae.data, ndvn__bfvc)
            context.nrt.decref(builder, df_typ.data[ndvn__bfvc], mct__xxqw)
            nlfe__uae.data = builder.insert_value(nlfe__uae.data,
                puvyc__rwd, ndvn__bfvc)
            context.nrt.incref(builder, arr_typ, puvyc__rwd)
        toz__lufd = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=xyvoi__bkpy)
        payload_type = DataFramePayloadType(df_typ)
        fkhqm__emoah = context.nrt.meminfo_data(builder, toz__lufd.meminfo)
        igup__crsk = context.get_value_type(payload_type).as_pointer()
        fkhqm__emoah = builder.bitcast(fkhqm__emoah, igup__crsk)
        builder.store(nlfe__uae._getvalue(), fkhqm__emoah)
        return impl_ret_borrowed(context, builder, df_typ, xyvoi__bkpy)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):
    check_runtime_cols_unsupported(df_t, 'set_df_index')

    def codegen(context, builder, signature, args):
        ovuk__bpmk = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        bulry__spya = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=ovuk__bpmk)
        rkb__lgzot = get_dataframe_payload(context, builder, df_typ, ovuk__bpmk
            )
        toz__lufd = construct_dataframe(context, builder, signature.
            return_type, rkb__lgzot.data, index_val, bulry__spya.parent, None)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), rkb__lgzot.data)
        return toz__lufd
    ekt__ecv = DataFrameType(df_t.data, index_t, df_t.columns, df_t.dist,
        df_t.is_table_format)
    sig = signature(ekt__ecv, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    check_runtime_cols_unsupported(df_type, 'set_df_column_with_reflect')
    assert is_literal_type(cname_type), 'constant column name expected'
    col_name = get_literal_value(cname_type)
    zhhno__ruq = len(df_type.columns)
    emy__xor = zhhno__ruq
    mov__jhq = df_type.data
    column_names = df_type.columns
    index_typ = df_type.index
    pino__ahxoq = col_name not in df_type.columns
    ndvn__bfvc = zhhno__ruq
    if pino__ahxoq:
        mov__jhq += arr_type,
        column_names += col_name,
        emy__xor += 1
    else:
        ndvn__bfvc = df_type.columns.index(col_name)
        mov__jhq = tuple(arr_type if i == ndvn__bfvc else mov__jhq[i] for i in
            range(zhhno__ruq))

    def codegen(context, builder, signature, args):
        xyvoi__bkpy, xmfj__iktc, puvyc__rwd = args
        in_dataframe_payload = get_dataframe_payload(context, builder,
            df_type, xyvoi__bkpy)
        apeyz__vsl = cgutils.create_struct_proxy(df_type)(context, builder,
            value=xyvoi__bkpy)
        if df_type.is_table_format:
            wmet__rjca = df_type.table_type
            nbmo__vuwkd = builder.extract_value(in_dataframe_payload.data, 0)
            zpd__vjidu = TableType(mov__jhq)
            pciju__vekg = set_table_data_codegen(context, builder,
                wmet__rjca, nbmo__vuwkd, zpd__vjidu, arr_type, puvyc__rwd,
                ndvn__bfvc, pino__ahxoq)
            data_tup = context.make_tuple(builder, types.Tuple([zpd__vjidu]
                ), [pciju__vekg])
        else:
            vroe__xkuz = [(builder.extract_value(in_dataframe_payload.data,
                i) if i != ndvn__bfvc else puvyc__rwd) for i in range(
                zhhno__ruq)]
            if pino__ahxoq:
                vroe__xkuz.append(puvyc__rwd)
            for izjmz__iawd, sqdre__fxz in zip(vroe__xkuz, mov__jhq):
                context.nrt.incref(builder, sqdre__fxz, izjmz__iawd)
            data_tup = context.make_tuple(builder, types.Tuple(mov__jhq),
                vroe__xkuz)
        index_val = in_dataframe_payload.index
        context.nrt.incref(builder, index_typ, index_val)
        khyo__tyjcr = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, apeyz__vsl.parent, None)
        if not pino__ahxoq and arr_type == df_type.data[ndvn__bfvc]:
            decref_df_data(context, builder, in_dataframe_payload, df_type)
            payload_type = DataFramePayloadType(df_type)
            fkhqm__emoah = context.nrt.meminfo_data(builder, apeyz__vsl.meminfo
                )
            igup__crsk = context.get_value_type(payload_type).as_pointer()
            fkhqm__emoah = builder.bitcast(fkhqm__emoah, igup__crsk)
            gdj__uatu = get_dataframe_payload(context, builder, df_type,
                khyo__tyjcr)
            builder.store(gdj__uatu._getvalue(), fkhqm__emoah)
            context.nrt.incref(builder, index_typ, index_val)
            if df_type.is_table_format:
                context.nrt.incref(builder, zpd__vjidu, builder.
                    extract_value(data_tup, 0))
            else:
                for izjmz__iawd, sqdre__fxz in zip(vroe__xkuz, mov__jhq):
                    context.nrt.incref(builder, sqdre__fxz, izjmz__iawd)
        has_parent = cgutils.is_not_null(builder, apeyz__vsl.parent)
        with builder.if_then(has_parent):
            dhoa__siwig = context.get_python_api(builder)
            hcdfu__bqln = dhoa__siwig.gil_ensure()
            swcnr__rtz = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, puvyc__rwd)
            aroc__rhq = numba.core.pythonapi._BoxContext(context, builder,
                dhoa__siwig, swcnr__rtz)
            kpa__pysm = aroc__rhq.pyapi.from_native_value(arr_type,
                puvyc__rwd, aroc__rhq.env_manager)
            if isinstance(col_name, str):
                myslp__kneo = context.insert_const_string(builder.module,
                    col_name)
                juj__lhsos = dhoa__siwig.string_from_string(myslp__kneo)
            else:
                assert isinstance(col_name, int)
                juj__lhsos = dhoa__siwig.long_from_longlong(context.
                    get_constant(types.intp, col_name))
            dhoa__siwig.object_setitem(apeyz__vsl.parent, juj__lhsos, kpa__pysm
                )
            dhoa__siwig.decref(kpa__pysm)
            dhoa__siwig.decref(juj__lhsos)
            dhoa__siwig.gil_release(hcdfu__bqln)
        return khyo__tyjcr
    ekt__ecv = DataFrameType(mov__jhq, index_typ, column_names, df_type.
        dist, df_type.is_table_format)
    sig = signature(ekt__ecv, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    check_runtime_cols_unsupported(df_type, 'lowering a constant DataFrame')
    zhhno__ruq = len(pyval.columns)
    vroe__xkuz = []
    for i in range(zhhno__ruq):
        ijgf__mkus = pyval.iloc[:, i]
        if isinstance(df_type.data[i], bodo.DatetimeArrayType):
            kpa__pysm = ijgf__mkus.array
        else:
            kpa__pysm = ijgf__mkus.values
        vroe__xkuz.append(kpa__pysm)
    vroe__xkuz = tuple(vroe__xkuz)
    if df_type.is_table_format:
        xvj__flg = context.get_constant_generic(builder, df_type.table_type,
            Table(vroe__xkuz))
        data_tup = lir.Constant.literal_struct([xvj__flg])
    else:
        data_tup = lir.Constant.literal_struct([context.
            get_constant_generic(builder, df_type.data[i], mba__koncb) for 
            i, mba__koncb in enumerate(vroe__xkuz)])
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    blwkw__nqxbj = context.get_constant_null(types.pyobject)
    payload = lir.Constant.literal_struct([data_tup, index_val, blwkw__nqxbj])
    payload = cgutils.global_constant(builder, '.const.payload', payload
        ).bitcast(cgutils.voidptr_t)
    annh__ixhp = context.get_constant(types.int64, -1)
    gkrqf__bwod = context.get_constant_null(types.voidptr)
    djgqa__tgl = lir.Constant.literal_struct([annh__ixhp, gkrqf__bwod,
        gkrqf__bwod, payload, annh__ixhp])
    djgqa__tgl = cgutils.global_constant(builder, '.const.meminfo', djgqa__tgl
        ).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([djgqa__tgl, blwkw__nqxbj])


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
        lqf__hdc = context.cast(builder, in_dataframe_payload.index, fromty
            .index, toty.index)
    else:
        lqf__hdc = in_dataframe_payload.index
        context.nrt.incref(builder, fromty.index, lqf__hdc)
    if (fromty.is_table_format == toty.is_table_format and fromty.data ==
        toty.data):
        xle__nuzck = in_dataframe_payload.data
        if fromty.is_table_format:
            context.nrt.incref(builder, types.Tuple([fromty.table_type]),
                xle__nuzck)
        else:
            context.nrt.incref(builder, types.BaseTuple.from_types(fromty.
                data), xle__nuzck)
    elif not fromty.is_table_format and toty.is_table_format:
        xle__nuzck = _cast_df_data_to_table_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and not toty.is_table_format:
        xle__nuzck = _cast_df_data_to_tuple_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and toty.is_table_format:
        xle__nuzck = _cast_df_data_keep_table_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    else:
        xle__nuzck = _cast_df_data_keep_tuple_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    return construct_dataframe(context, builder, toty, xle__nuzck, lqf__hdc,
        in_dataframe_payload.parent, None)


def _cast_empty_df(context, builder, toty):
    fot__arx = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        zysr__xfhyh = get_index_data_arr_types(toty.index)[0]
        iskd__ompsr = bodo.utils.transform.get_type_alloc_counts(zysr__xfhyh
            ) - 1
        tahv__qsjh = ', '.join('0' for xmfj__iktc in range(iskd__ompsr))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(tahv__qsjh, ', ' if iskd__ompsr == 1 else ''))
        fot__arx['index_arr_type'] = zysr__xfhyh
    gkmpn__nab = []
    for i, arr_typ in enumerate(toty.data):
        iskd__ompsr = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        tahv__qsjh = ', '.join('0' for xmfj__iktc in range(iskd__ompsr))
        flrtx__nae = ('bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'.
            format(i, tahv__qsjh, ', ' if iskd__ompsr == 1 else ''))
        gkmpn__nab.append(flrtx__nae)
        fot__arx[f'arr_type{i}'] = arr_typ
    gkmpn__nab = ', '.join(gkmpn__nab)
    uwro__kjzx = 'def impl():\n'
    eftw__iaz = bodo.hiframes.dataframe_impl._gen_init_df(uwro__kjzx, toty.
        columns, gkmpn__nab, index, fot__arx)
    df = context.compile_internal(builder, eftw__iaz, toty(), [])
    return df


def _cast_df_data_to_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame to table format')
    oylp__ray = toty.table_type
    xvj__flg = cgutils.create_struct_proxy(oylp__ray)(context, builder)
    xvj__flg.parent = in_dataframe_payload.parent
    for yia__dek, krai__anp in oylp__ray.type_to_blk.items():
        aque__uqab = context.get_constant(types.int64, len(oylp__ray.
            block_to_arr_ind[krai__anp]))
        xmfj__iktc, xsqqj__ovhb = ListInstance.allocate_ex(context, builder,
            types.List(yia__dek), aque__uqab)
        xsqqj__ovhb.size = aque__uqab
        setattr(xvj__flg, f'block_{krai__anp}', xsqqj__ovhb.value)
    for i, yia__dek in enumerate(fromty.data):
        ahrnx__xgf = toty.data[i]
        if yia__dek != ahrnx__xgf:
            fbfb__vnfs = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*fbfb__vnfs)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        mct__xxqw = builder.extract_value(in_dataframe_payload.data, i)
        if yia__dek != ahrnx__xgf:
            vur__fgck = context.cast(builder, mct__xxqw, yia__dek, ahrnx__xgf)
            nil__doge = False
        else:
            vur__fgck = mct__xxqw
            nil__doge = True
        krai__anp = oylp__ray.type_to_blk[yia__dek]
        biwg__vla = getattr(xvj__flg, f'block_{krai__anp}')
        evnd__alnwc = ListInstance(context, builder, types.List(yia__dek),
            biwg__vla)
        kfdhl__fik = context.get_constant(types.int64, oylp__ray.
            block_offsets[i])
        evnd__alnwc.setitem(kfdhl__fik, vur__fgck, nil__doge)
    data_tup = context.make_tuple(builder, types.Tuple([oylp__ray]), [
        xvj__flg._getvalue()])
    return data_tup


def _cast_df_data_keep_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame columns')
    vroe__xkuz = []
    for i in range(len(fromty.data)):
        if fromty.data[i] != toty.data[i]:
            fbfb__vnfs = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*fbfb__vnfs)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
            mct__xxqw = builder.extract_value(in_dataframe_payload.data, i)
            vur__fgck = context.cast(builder, mct__xxqw, fromty.data[i],
                toty.data[i])
            nil__doge = False
        else:
            vur__fgck = builder.extract_value(in_dataframe_payload.data, i)
            nil__doge = True
        if nil__doge:
            context.nrt.incref(builder, toty.data[i], vur__fgck)
        vroe__xkuz.append(vur__fgck)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), vroe__xkuz)
    return data_tup


def _cast_df_data_keep_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting table format DataFrame columns')
    wmet__rjca = fromty.table_type
    nbmo__vuwkd = cgutils.create_struct_proxy(wmet__rjca)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    zpd__vjidu = toty.table_type
    pciju__vekg = cgutils.create_struct_proxy(zpd__vjidu)(context, builder)
    pciju__vekg.parent = in_dataframe_payload.parent
    for yia__dek, krai__anp in zpd__vjidu.type_to_blk.items():
        aque__uqab = context.get_constant(types.int64, len(zpd__vjidu.
            block_to_arr_ind[krai__anp]))
        xmfj__iktc, xsqqj__ovhb = ListInstance.allocate_ex(context, builder,
            types.List(yia__dek), aque__uqab)
        xsqqj__ovhb.size = aque__uqab
        setattr(pciju__vekg, f'block_{krai__anp}', xsqqj__ovhb.value)
    for i in range(len(fromty.data)):
        kdhbn__sauz = fromty.data[i]
        ahrnx__xgf = toty.data[i]
        if kdhbn__sauz != ahrnx__xgf:
            fbfb__vnfs = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*fbfb__vnfs)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        jpvoc__fsvmj = wmet__rjca.type_to_blk[kdhbn__sauz]
        ppqk__cyrws = getattr(nbmo__vuwkd, f'block_{jpvoc__fsvmj}')
        qndrm__qbi = ListInstance(context, builder, types.List(kdhbn__sauz),
            ppqk__cyrws)
        xjopo__qamzh = context.get_constant(types.int64, wmet__rjca.
            block_offsets[i])
        mct__xxqw = qndrm__qbi.getitem(xjopo__qamzh)
        if kdhbn__sauz != ahrnx__xgf:
            vur__fgck = context.cast(builder, mct__xxqw, kdhbn__sauz,
                ahrnx__xgf)
            nil__doge = False
        else:
            vur__fgck = mct__xxqw
            nil__doge = True
        hhmj__tnq = zpd__vjidu.type_to_blk[yia__dek]
        xsqqj__ovhb = getattr(pciju__vekg, f'block_{hhmj__tnq}')
        jic__blb = ListInstance(context, builder, types.List(ahrnx__xgf),
            xsqqj__ovhb)
        izafv__tfkrg = context.get_constant(types.int64, zpd__vjidu.
            block_offsets[i])
        jic__blb.setitem(izafv__tfkrg, vur__fgck, nil__doge)
    data_tup = context.make_tuple(builder, types.Tuple([zpd__vjidu]), [
        pciju__vekg._getvalue()])
    return data_tup


def _cast_df_data_to_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(fromty,
        'casting table format to traditional DataFrame')
    oylp__ray = fromty.table_type
    xvj__flg = cgutils.create_struct_proxy(oylp__ray)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    vroe__xkuz = []
    for i, yia__dek in enumerate(toty.data):
        kdhbn__sauz = fromty.data[i]
        if yia__dek != kdhbn__sauz:
            fbfb__vnfs = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*fbfb__vnfs)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        krai__anp = oylp__ray.type_to_blk[kdhbn__sauz]
        biwg__vla = getattr(xvj__flg, f'block_{krai__anp}')
        evnd__alnwc = ListInstance(context, builder, types.List(kdhbn__sauz
            ), biwg__vla)
        kfdhl__fik = context.get_constant(types.int64, oylp__ray.
            block_offsets[i])
        mct__xxqw = evnd__alnwc.getitem(kfdhl__fik)
        if yia__dek != kdhbn__sauz:
            vur__fgck = context.cast(builder, mct__xxqw, kdhbn__sauz, yia__dek)
        else:
            vur__fgck = mct__xxqw
            context.nrt.incref(builder, yia__dek, vur__fgck)
        vroe__xkuz.append(vur__fgck)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), vroe__xkuz)
    return data_tup


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    exw__mgdzj, gkmpn__nab, index_arg = _get_df_args(data, index, columns,
        dtype, copy)
    lvavt__eqz = ColNamesMetaType(tuple(exw__mgdzj))
    uwro__kjzx = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    uwro__kjzx += (
        """  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, __col_name_meta_value_pd_overload)
"""
        .format(gkmpn__nab, index_arg))
    zeto__ixtc = {}
    exec(uwro__kjzx, {'bodo': bodo, 'np': np,
        '__col_name_meta_value_pd_overload': lvavt__eqz}, zeto__ixtc)
    ire__dkfq = zeto__ixtc['_init_df']
    return ire__dkfq


@intrinsic
def _tuple_to_table_format_decoded(typingctx, df_typ):
    assert not df_typ.is_table_format, '_tuple_to_table_format requires a tuple format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    ekt__ecv = DataFrameType(to_str_arr_if_dict_array(df_typ.data), df_typ.
        index, df_typ.columns, dist=df_typ.dist, is_table_format=True)
    sig = signature(ekt__ecv, df_typ)
    return sig, codegen


@intrinsic
def _table_to_tuple_format_decoded(typingctx, df_typ):
    assert df_typ.is_table_format, '_tuple_to_table_format requires a table format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    ekt__ecv = DataFrameType(to_str_arr_if_dict_array(df_typ.data), df_typ.
        index, df_typ.columns, dist=df_typ.dist, is_table_format=False)
    sig = signature(ekt__ecv, df_typ)
    return sig, codegen


def _get_df_args(data, index, columns, dtype, copy):
    talwn__vwr = ''
    if not is_overload_none(dtype):
        talwn__vwr = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        zhhno__ruq = (len(data.types) - 1) // 2
        qogrn__thons = [yia__dek.literal_value for yia__dek in data.types[1
            :zhhno__ruq + 1]]
        data_val_types = dict(zip(qogrn__thons, data.types[zhhno__ruq + 1:]))
        vroe__xkuz = ['data[{}]'.format(i) for i in range(zhhno__ruq + 1, 2 *
            zhhno__ruq + 1)]
        data_dict = dict(zip(qogrn__thons, vroe__xkuz))
        if is_overload_none(index):
            for i, yia__dek in enumerate(data.types[zhhno__ruq + 1:]):
                if isinstance(yia__dek, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(zhhno__ruq + 1 + i))
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
        diseg__hvu = '.copy()' if copy else ''
        fykbb__bvnn = get_overload_const_list(columns)
        zhhno__ruq = len(fykbb__bvnn)
        data_val_types = {aroc__rhq: data.copy(ndim=1) for aroc__rhq in
            fykbb__bvnn}
        vroe__xkuz = ['data[:,{}]{}'.format(i, diseg__hvu) for i in range(
            zhhno__ruq)]
        data_dict = dict(zip(fykbb__bvnn, vroe__xkuz))
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
    gkmpn__nab = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[aroc__rhq], df_len, talwn__vwr) for aroc__rhq in
        col_names))
    if len(col_names) == 0:
        gkmpn__nab = '()'
    return col_names, gkmpn__nab, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for aroc__rhq in col_names:
        if aroc__rhq in data_dict and is_iterable_type(data_val_types[
            aroc__rhq]):
            df_len = 'len({})'.format(data_dict[aroc__rhq])
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
    if all(aroc__rhq in data_dict for aroc__rhq in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    vysbg__ljvtb = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len
        , dtype)
    for aroc__rhq in col_names:
        if aroc__rhq not in data_dict:
            data_dict[aroc__rhq] = vysbg__ljvtb


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
            yia__dek = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            return len(yia__dek)
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
        indzl__ozom = idx.literal_value
        if isinstance(indzl__ozom, int):
            sopu__pok = tup.types[indzl__ozom]
        elif isinstance(indzl__ozom, slice):
            sopu__pok = types.BaseTuple.from_types(tup.types[indzl__ozom])
        return signature(sopu__pok, *args)


GetItemTuple.prefer_literal = True


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    fqe__ezpzn, idx = sig.args
    idx = idx.literal_value
    tup, xmfj__iktc = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(fqe__ezpzn)
        if not 0 <= idx < len(fqe__ezpzn):
            raise IndexError('cannot index at %d in %s' % (idx, fqe__ezpzn))
        cpcnf__qfbk = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        lgnz__wlhl = cgutils.unpack_tuple(builder, tup)[idx]
        cpcnf__qfbk = context.make_tuple(builder, sig.return_type, lgnz__wlhl)
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, cpcnf__qfbk)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, uzyuf__add, suffix_x,
            suffix_y, is_join, indicator, xmfj__iktc, xmfj__iktc) = args
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        fbgcg__xzul = {aroc__rhq: i for i, aroc__rhq in enumerate(left_on)}
        eean__nfc = {aroc__rhq: i for i, aroc__rhq in enumerate(right_on)}
        sad__sbijj = set(left_on) & set(right_on)
        brygg__kqn = set(left_df.columns) & set(right_df.columns)
        bhmmk__okfmj = brygg__kqn - sad__sbijj
        kqmc__soe = '$_bodo_index_' in left_on
        yvg__falyw = '$_bodo_index_' in right_on
        how = get_overload_const_str(uzyuf__add)
        xut__cmyil = how in {'left', 'outer'}
        agi__tcpo = how in {'right', 'outer'}
        columns = []
        data = []
        if kqmc__soe:
            mlzz__mwuxv = bodo.utils.typing.get_index_data_arr_types(left_df
                .index)[0]
        else:
            mlzz__mwuxv = left_df.data[left_df.column_index[left_on[0]]]
        if yvg__falyw:
            lmwis__uppi = bodo.utils.typing.get_index_data_arr_types(right_df
                .index)[0]
        else:
            lmwis__uppi = right_df.data[right_df.column_index[right_on[0]]]
        if kqmc__soe and not yvg__falyw and not is_join.literal_value:
            sit__esrmu = right_on[0]
            if sit__esrmu in left_df.column_index:
                columns.append(sit__esrmu)
                if (lmwis__uppi == bodo.dict_str_arr_type and mlzz__mwuxv ==
                    bodo.string_array_type):
                    sjajl__ydfzu = bodo.string_array_type
                else:
                    sjajl__ydfzu = lmwis__uppi
                data.append(sjajl__ydfzu)
        if yvg__falyw and not kqmc__soe and not is_join.literal_value:
            psikj__zwjem = left_on[0]
            if psikj__zwjem in right_df.column_index:
                columns.append(psikj__zwjem)
                if (mlzz__mwuxv == bodo.dict_str_arr_type and lmwis__uppi ==
                    bodo.string_array_type):
                    sjajl__ydfzu = bodo.string_array_type
                else:
                    sjajl__ydfzu = mlzz__mwuxv
                data.append(sjajl__ydfzu)
        for kdhbn__sauz, ijgf__mkus in zip(left_df.data, left_df.columns):
            columns.append(str(ijgf__mkus) + suffix_x.literal_value if 
                ijgf__mkus in bhmmk__okfmj else ijgf__mkus)
            if ijgf__mkus in sad__sbijj:
                if kdhbn__sauz == bodo.dict_str_arr_type:
                    kdhbn__sauz = right_df.data[right_df.column_index[
                        ijgf__mkus]]
                data.append(kdhbn__sauz)
            else:
                if (kdhbn__sauz == bodo.dict_str_arr_type and ijgf__mkus in
                    fbgcg__xzul):
                    if yvg__falyw:
                        kdhbn__sauz = lmwis__uppi
                    else:
                        dxco__tdyw = fbgcg__xzul[ijgf__mkus]
                        potg__oquv = right_on[dxco__tdyw]
                        kdhbn__sauz = right_df.data[right_df.column_index[
                            potg__oquv]]
                if agi__tcpo:
                    kdhbn__sauz = to_nullable_type(kdhbn__sauz)
                data.append(kdhbn__sauz)
        for kdhbn__sauz, ijgf__mkus in zip(right_df.data, right_df.columns):
            if ijgf__mkus not in sad__sbijj:
                columns.append(str(ijgf__mkus) + suffix_y.literal_value if 
                    ijgf__mkus in bhmmk__okfmj else ijgf__mkus)
                if (kdhbn__sauz == bodo.dict_str_arr_type and ijgf__mkus in
                    eean__nfc):
                    if kqmc__soe:
                        kdhbn__sauz = mlzz__mwuxv
                    else:
                        dxco__tdyw = eean__nfc[ijgf__mkus]
                        qcrp__gce = left_on[dxco__tdyw]
                        kdhbn__sauz = left_df.data[left_df.column_index[
                            qcrp__gce]]
                if xut__cmyil:
                    kdhbn__sauz = to_nullable_type(kdhbn__sauz)
                data.append(kdhbn__sauz)
        tqn__top = get_overload_const_bool(indicator)
        if tqn__top:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        ksn__kgw = False
        if kqmc__soe and yvg__falyw and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            ksn__kgw = True
        elif kqmc__soe and not yvg__falyw:
            index_typ = right_df.index
            ksn__kgw = True
        elif yvg__falyw and not kqmc__soe:
            index_typ = left_df.index
            ksn__kgw = True
        if ksn__kgw and isinstance(index_typ, bodo.hiframes.pd_index_ext.
            RangeIndexType):
            index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64
                )
        ckd__ysud = DataFrameType(tuple(data), index_typ, tuple(columns),
            is_table_format=True)
        return signature(ckd__ysud, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    toz__lufd = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return toz__lufd._getvalue()


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
    diakf__btaud = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    ipcab__isw = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pandas.concat', diakf__btaud, ipcab__isw,
        package_name='pandas', module_name='General')
    uwro__kjzx = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        dfvpb__kwo = 0
        gkmpn__nab = []
        names = []
        for i, mjntl__fwiu in enumerate(objs.types):
            assert isinstance(mjntl__fwiu, (SeriesType, DataFrameType))
            check_runtime_cols_unsupported(mjntl__fwiu, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                mjntl__fwiu, 'pandas.concat()')
            if isinstance(mjntl__fwiu, SeriesType):
                names.append(str(dfvpb__kwo))
                dfvpb__kwo += 1
                gkmpn__nab.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(mjntl__fwiu.columns)
                for nyvaq__yfkih in range(len(mjntl__fwiu.data)):
                    gkmpn__nab.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, nyvaq__yfkih))
        return bodo.hiframes.dataframe_impl._gen_init_df(uwro__kjzx, names,
            ', '.join(gkmpn__nab), index)
    if axis != 0:
        raise_bodo_error('pd.concat(): axis must be 0 or 1')
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(yia__dek, DataFrameType) for yia__dek in objs
            .types)
        qerg__xkoom = []
        for df in objs.types:
            check_runtime_cols_unsupported(df, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
                'pandas.concat()')
            qerg__xkoom.extend(df.columns)
        qerg__xkoom = list(dict.fromkeys(qerg__xkoom).keys())
        pcn__fdwfn = {}
        for dfvpb__kwo, aroc__rhq in enumerate(qerg__xkoom):
            for i, df in enumerate(objs.types):
                if aroc__rhq in df.column_index:
                    pcn__fdwfn[f'arr_typ{dfvpb__kwo}'] = df.data[df.
                        column_index[aroc__rhq]]
                    break
        assert len(pcn__fdwfn) == len(qerg__xkoom)
        svzxu__faqr = []
        for dfvpb__kwo, aroc__rhq in enumerate(qerg__xkoom):
            args = []
            for i, df in enumerate(objs.types):
                if aroc__rhq in df.column_index:
                    ndvn__bfvc = df.column_index[aroc__rhq]
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, ndvn__bfvc))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, dfvpb__kwo))
            uwro__kjzx += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'
                .format(dfvpb__kwo, ', '.join(args)))
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
        return bodo.hiframes.dataframe_impl._gen_init_df(uwro__kjzx,
            qerg__xkoom, ', '.join('A{}'.format(i) for i in range(len(
            qerg__xkoom))), index, pcn__fdwfn)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(yia__dek, SeriesType) for yia__dek in objs.types)
        uwro__kjzx += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'
            .format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            uwro__kjzx += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            uwro__kjzx += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        uwro__kjzx += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        zeto__ixtc = {}
        exec(uwro__kjzx, {'bodo': bodo, 'np': np, 'numba': numba}, zeto__ixtc)
        return zeto__ixtc['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        check_runtime_cols_unsupported(objs.dtype, 'pandas.concat()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(objs.
            dtype, 'pandas.concat()')
        df_type = objs.dtype
        for dfvpb__kwo, aroc__rhq in enumerate(df_type.columns):
            uwro__kjzx += '  arrs{} = []\n'.format(dfvpb__kwo)
            uwro__kjzx += '  for i in range(len(objs)):\n'
            uwro__kjzx += '    df = objs[i]\n'
            uwro__kjzx += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(dfvpb__kwo))
            uwro__kjzx += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(dfvpb__kwo))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            uwro__kjzx += '  arrs_index = []\n'
            uwro__kjzx += '  for i in range(len(objs)):\n'
            uwro__kjzx += '    df = objs[i]\n'
            uwro__kjzx += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            if objs.dtype.index.name_typ == types.none:
                name = None
            else:
                name = objs.dtype.index.name_typ.literal_value
            index = f"""bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index), {name!r})
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(uwro__kjzx,
            df_type.columns, ', '.join('out_arr{}'.format(i) for i in range
            (len(df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        uwro__kjzx += '  arrs = []\n'
        uwro__kjzx += '  for i in range(len(objs)):\n'
        uwro__kjzx += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        uwro__kjzx += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            uwro__kjzx += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            uwro__kjzx += '  arrs_index = []\n'
            uwro__kjzx += '  for i in range(len(objs)):\n'
            uwro__kjzx += '    S = objs[i]\n'
            uwro__kjzx += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            uwro__kjzx += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        uwro__kjzx += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        zeto__ixtc = {}
        exec(uwro__kjzx, {'bodo': bodo, 'np': np, 'numba': numba}, zeto__ixtc)
        return zeto__ixtc['impl']
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
        ekt__ecv = df.copy(index=index)
        return signature(ekt__ecv, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    yuxvt__emkze = cgutils.create_struct_proxy(sig.return_type)(context,
        builder)
    return yuxvt__emkze._getvalue()


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    check_runtime_cols_unsupported(df, 'DataFrame.itertuples()')
    diakf__btaud = dict(index=index, name=name)
    ipcab__isw = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', diakf__btaud, ipcab__isw,
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
        pcn__fdwfn = (types.Array(types.int64, 1, 'C'),) + df.data
        pox__yaxf = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(columns
            , pcn__fdwfn)
        return signature(pox__yaxf, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    yuxvt__emkze = cgutils.create_struct_proxy(sig.return_type)(context,
        builder)
    return yuxvt__emkze._getvalue()


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
    yuxvt__emkze = cgutils.create_struct_proxy(sig.return_type)(context,
        builder)
    return yuxvt__emkze._getvalue()


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
    yuxvt__emkze = cgutils.create_struct_proxy(sig.return_type)(context,
        builder)
    return yuxvt__emkze._getvalue()


@numba.generated_jit(nopython=True)
def pivot_impl(index_tup, columns_tup, values_tup, pivot_values,
    index_names, columns_name, value_names, check_duplicates=True,
    is_already_shuffled=False, _constant_pivot_values=None, parallel=False):
    if not is_overload_constant_bool(check_duplicates):
        raise BodoError(
            'pivot_impl(): check_duplicates must be a constant boolean')
    brp__jwle = get_overload_const_bool(check_duplicates)
    mysir__syfc = not get_overload_const_bool(is_already_shuffled)
    uafx__xhj = not is_overload_none(_constant_pivot_values)
    index_names = index_names.instance_type if isinstance(index_names,
        types.TypeRef) else index_names
    columns_name = columns_name.instance_type if isinstance(columns_name,
        types.TypeRef) else columns_name
    value_names = value_names.instance_type if isinstance(value_names,
        types.TypeRef) else value_names
    _constant_pivot_values = (_constant_pivot_values.instance_type if
        isinstance(_constant_pivot_values, types.TypeRef) else
        _constant_pivot_values)
    buqf__lcen = len(value_names) > 1
    qnd__uzpv = None
    fhad__lzu = None
    hdxt__itlc = None
    yqtl__wzlp = None
    kciz__wvutk = isinstance(values_tup, types.UniTuple)
    if kciz__wvutk:
        zxp__zrk = [to_str_arr_if_dict_array(to_nullable_type(values_tup.
            dtype))]
    else:
        zxp__zrk = [to_str_arr_if_dict_array(to_nullable_type(sqdre__fxz)) for
            sqdre__fxz in values_tup]
    uwro__kjzx = 'def impl(\n'
    uwro__kjzx += """    index_tup, columns_tup, values_tup, pivot_values, index_names, columns_name, value_names, check_duplicates=True, is_already_shuffled=False, _constant_pivot_values=None, parallel=False
"""
    uwro__kjzx += '):\n'
    uwro__kjzx += (
        "    ev = tracing.Event('pivot_impl', is_parallel=parallel)\n")
    if mysir__syfc:
        uwro__kjzx += '    if parallel:\n'
        uwro__kjzx += (
            "        ev_shuffle = tracing.Event('shuffle_pivot_index')\n")
        gfcy__mxv = ', '.join([f'array_to_info(index_tup[{i}])' for i in
            range(len(index_tup))] + [f'array_to_info(columns_tup[{i}])' for
            i in range(len(columns_tup))] + [
            f'array_to_info(values_tup[{i}])' for i in range(len(values_tup))])
        uwro__kjzx += f'        info_list = [{gfcy__mxv}]\n'
        uwro__kjzx += '        cpp_table = arr_info_list_to_table(info_list)\n'
        uwro__kjzx += f"""        out_cpp_table = shuffle_table(cpp_table, {len(index_tup)}, parallel, 0)
"""
        voca__vjr = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i}), index_tup[{i}])'
             for i in range(len(index_tup))])
        htab__gnsva = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup)}), columns_tup[{i}])'
             for i in range(len(columns_tup))])
        ouk__fyz = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup) + len(columns_tup)}), values_tup[{i}])'
             for i in range(len(values_tup))])
        uwro__kjzx += f'        index_tup = ({voca__vjr},)\n'
        uwro__kjzx += f'        columns_tup = ({htab__gnsva},)\n'
        uwro__kjzx += f'        values_tup = ({ouk__fyz},)\n'
        uwro__kjzx += '        delete_table(cpp_table)\n'
        uwro__kjzx += '        delete_table(out_cpp_table)\n'
        uwro__kjzx += '        ev_shuffle.finalize()\n'
    uwro__kjzx += '    columns_arr = columns_tup[0]\n'
    if kciz__wvutk:
        uwro__kjzx += '    values_arrs = [arr for arr in values_tup]\n'
    uwro__kjzx += (
        "    ev_unique = tracing.Event('pivot_unique_index_map', is_parallel=parallel)\n"
        )
    uwro__kjzx += """    unique_index_arr_tup, row_vector = bodo.libs.array_ops.array_unique_vector_map(
"""
    uwro__kjzx += '        index_tup\n'
    uwro__kjzx += '    )\n'
    uwro__kjzx += '    n_rows = len(unique_index_arr_tup[0])\n'
    uwro__kjzx += '    num_values_arrays = len(values_tup)\n'
    uwro__kjzx += '    n_unique_pivots = len(pivot_values)\n'
    if kciz__wvutk:
        uwro__kjzx += '    n_cols = num_values_arrays * n_unique_pivots\n'
    else:
        uwro__kjzx += '    n_cols = n_unique_pivots\n'
    uwro__kjzx += '    col_map = {}\n'
    uwro__kjzx += '    for i in range(n_unique_pivots):\n'
    uwro__kjzx += '        if bodo.libs.array_kernels.isna(pivot_values, i):\n'
    uwro__kjzx += '            raise ValueError(\n'
    uwro__kjzx += """                "DataFrame.pivot(): NA values in 'columns' array not supported\"
"""
    uwro__kjzx += '            )\n'
    uwro__kjzx += '        col_map[pivot_values[i]] = i\n'
    uwro__kjzx += '    ev_unique.finalize()\n'
    uwro__kjzx += (
        "    ev_alloc = tracing.Event('pivot_alloc', is_parallel=parallel)\n")
    enx__msf = False
    for i, zezzf__dqry in enumerate(zxp__zrk):
        if is_str_arr_type(zezzf__dqry):
            enx__msf = True
            uwro__kjzx += f"""    len_arrs_{i} = [np.zeros(n_rows, np.int64) for _ in range(n_cols)]
"""
            uwro__kjzx += f'    total_lens_{i} = np.zeros(n_cols, np.int64)\n'
    if enx__msf:
        if brp__jwle:
            uwro__kjzx += '    nbytes = (n_rows + 7) >> 3\n'
            uwro__kjzx += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
        uwro__kjzx += '    for i in range(len(columns_arr)):\n'
        uwro__kjzx += '        col_name = columns_arr[i]\n'
        uwro__kjzx += '        pivot_idx = col_map[col_name]\n'
        uwro__kjzx += '        row_idx = row_vector[i]\n'
        if brp__jwle:
            uwro__kjzx += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
            uwro__kjzx += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
            uwro__kjzx += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
            uwro__kjzx += '        else:\n'
            uwro__kjzx += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
        if kciz__wvutk:
            uwro__kjzx += '        for j in range(num_values_arrays):\n'
            uwro__kjzx += (
                '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
            uwro__kjzx += '            len_arr = len_arrs_0[col_idx]\n'
            uwro__kjzx += '            values_arr = values_arrs[j]\n'
            uwro__kjzx += (
                '            if not bodo.libs.array_kernels.isna(values_arr, i):\n'
                )
            uwro__kjzx += """                str_val_len = bodo.libs.str_arr_ext.get_str_arr_item_length(values_arr, i)
"""
            uwro__kjzx += '                len_arr[row_idx] = str_val_len\n'
            uwro__kjzx += (
                '                total_lens_0[col_idx] += str_val_len\n')
        else:
            for i, zezzf__dqry in enumerate(zxp__zrk):
                if is_str_arr_type(zezzf__dqry):
                    uwro__kjzx += f"""        if not bodo.libs.array_kernels.isna(values_tup[{i}], i):
"""
                    uwro__kjzx += f"""            str_val_len_{i} = bodo.libs.str_arr_ext.get_str_arr_item_length(values_tup[{i}], i)
"""
                    uwro__kjzx += f"""            len_arrs_{i}[pivot_idx][row_idx] = str_val_len_{i}
"""
                    uwro__kjzx += (
                        f'            total_lens_{i}[pivot_idx] += str_val_len_{i}\n'
                        )
    uwro__kjzx += f"    ev_alloc.add_attribute('num_rows', n_rows)\n"
    for i, zezzf__dqry in enumerate(zxp__zrk):
        if is_str_arr_type(zezzf__dqry):
            uwro__kjzx += f'    data_arrs_{i} = [\n'
            uwro__kjzx += (
                '        bodo.libs.str_arr_ext.gen_na_str_array_lens(\n')
            uwro__kjzx += (
                f'            n_rows, total_lens_{i}[i], len_arrs_{i}[i]\n')
            uwro__kjzx += '        )\n'
            uwro__kjzx += '        for i in range(n_cols)\n'
            uwro__kjzx += '    ]\n'
            uwro__kjzx += f'    if tracing.is_tracing():\n'
            uwro__kjzx += '         for i in range(n_cols):'
            uwro__kjzx += f"""            ev_alloc.add_attribute('total_str_chars_out_column_{i}_' + str(i), total_lens_{i}[i])
"""
        else:
            uwro__kjzx += f'    data_arrs_{i} = [\n'
            uwro__kjzx += f"""        bodo.libs.array_kernels.gen_na_array(n_rows, data_arr_typ_{i})
"""
            uwro__kjzx += '        for _ in range(n_cols)\n'
            uwro__kjzx += '    ]\n'
    if not enx__msf and brp__jwle:
        uwro__kjzx += '    nbytes = (n_rows + 7) >> 3\n'
        uwro__kjzx += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
    uwro__kjzx += '    ev_alloc.finalize()\n'
    uwro__kjzx += (
        "    ev_fill = tracing.Event('pivot_fill_data', is_parallel=parallel)\n"
        )
    uwro__kjzx += '    for i in range(len(columns_arr)):\n'
    uwro__kjzx += '        col_name = columns_arr[i]\n'
    uwro__kjzx += '        pivot_idx = col_map[col_name]\n'
    uwro__kjzx += '        row_idx = row_vector[i]\n'
    if not enx__msf and brp__jwle:
        uwro__kjzx += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
        uwro__kjzx += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
        uwro__kjzx += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
        uwro__kjzx += '        else:\n'
        uwro__kjzx += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)\n'
            )
    if kciz__wvutk:
        uwro__kjzx += '        for j in range(num_values_arrays):\n'
        uwro__kjzx += (
            '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
        uwro__kjzx += '            col_arr = data_arrs_0[col_idx]\n'
        uwro__kjzx += '            values_arr = values_arrs[j]\n'
        uwro__kjzx += (
            '            if bodo.libs.array_kernels.isna(values_arr, i):\n')
        uwro__kjzx += (
            '                bodo.libs.array_kernels.setna(col_arr, row_idx)\n'
            )
        uwro__kjzx += '            else:\n'
        uwro__kjzx += '                col_arr[row_idx] = values_arr[i]\n'
    else:
        for i, zezzf__dqry in enumerate(zxp__zrk):
            uwro__kjzx += f'        col_arr_{i} = data_arrs_{i}[pivot_idx]\n'
            uwro__kjzx += (
                f'        if bodo.libs.array_kernels.isna(values_tup[{i}], i):\n'
                )
            uwro__kjzx += (
                f'            bodo.libs.array_kernels.setna(col_arr_{i}, row_idx)\n'
                )
            uwro__kjzx += f'        else:\n'
            uwro__kjzx += (
                f'            col_arr_{i}[row_idx] = values_tup[{i}][i]\n')
    if len(index_names) == 1:
        uwro__kjzx += """    index = bodo.utils.conversion.index_from_array(unique_index_arr_tup[0], index_names_lit)
"""
        qnd__uzpv = index_names.meta[0]
    else:
        uwro__kjzx += """    index = bodo.hiframes.pd_multi_index_ext.init_multi_index(unique_index_arr_tup, index_names_lit, None)
"""
        qnd__uzpv = tuple(index_names.meta)
    uwro__kjzx += f'    if tracing.is_tracing():\n'
    uwro__kjzx += f'        index_nbytes = index.nbytes\n'
    uwro__kjzx += f"        ev.add_attribute('index_nbytes', index_nbytes)\n"
    if not uafx__xhj:
        hdxt__itlc = columns_name.meta[0]
        if buqf__lcen:
            uwro__kjzx += (
                f'    num_rows = {len(value_names)} * len(pivot_values)\n')
            fhad__lzu = value_names.meta
            if all(isinstance(aroc__rhq, str) for aroc__rhq in fhad__lzu):
                fhad__lzu = pd.array(fhad__lzu, 'string')
            elif all(isinstance(aroc__rhq, int) for aroc__rhq in fhad__lzu):
                fhad__lzu = np.array(fhad__lzu, 'int64')
            else:
                raise BodoError(
                    f"pivot(): column names selected for 'values' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
                    )
            if isinstance(fhad__lzu.dtype, pd.StringDtype):
                uwro__kjzx += '    total_chars = 0\n'
                uwro__kjzx += f'    for i in range({len(value_names)}):\n'
                uwro__kjzx += """        value_name_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(value_names_lit, i)
"""
                uwro__kjzx += '        total_chars += value_name_str_len\n'
                uwro__kjzx += """    new_value_names = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(pivot_values))
"""
            else:
                uwro__kjzx += """    new_value_names = bodo.utils.utils.alloc_type(num_rows, value_names_lit, (-1,))
"""
            if is_str_arr_type(pivot_values):
                uwro__kjzx += '    total_chars = 0\n'
                uwro__kjzx += '    for i in range(len(pivot_values)):\n'
                uwro__kjzx += """        pivot_val_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(pivot_values, i)
"""
                uwro__kjzx += '        total_chars += pivot_val_str_len\n'
                uwro__kjzx += f"""    new_pivot_values = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * {len(value_names)})
"""
            else:
                uwro__kjzx += """    new_pivot_values = bodo.utils.utils.alloc_type(num_rows, pivot_values, (-1,))
"""
            uwro__kjzx += f'    for i in range({len(value_names)}):\n'
            uwro__kjzx += '        for j in range(len(pivot_values)):\n'
            uwro__kjzx += """            new_value_names[(i * len(pivot_values)) + j] = value_names_lit[i]
"""
            uwro__kjzx += """            new_pivot_values[(i * len(pivot_values)) + j] = pivot_values[j]
"""
            uwro__kjzx += """    column_index = bodo.hiframes.pd_multi_index_ext.init_multi_index((new_value_names, new_pivot_values), (None, columns_name_lit), None)
"""
        else:
            uwro__kjzx += """    column_index =  bodo.utils.conversion.index_from_array(pivot_values, columns_name_lit)
"""
    uwro__kjzx += '    ev_fill.finalize()\n'
    oylp__ray = None
    if uafx__xhj:
        if buqf__lcen:
            vkq__mkll = []
            for bwetj__gtr in _constant_pivot_values.meta:
                for zyv__tyg in value_names.meta:
                    vkq__mkll.append((bwetj__gtr, zyv__tyg))
            column_names = tuple(vkq__mkll)
        else:
            column_names = tuple(_constant_pivot_values.meta)
        yqtl__wzlp = ColNamesMetaType(column_names)
        uyl__sdu = []
        for sqdre__fxz in zxp__zrk:
            uyl__sdu.extend([sqdre__fxz] * len(_constant_pivot_values))
        uzy__sphhl = tuple(uyl__sdu)
        oylp__ray = TableType(uzy__sphhl)
        uwro__kjzx += (
            f'    table = bodo.hiframes.table.init_table(table_type, False)\n')
        uwro__kjzx += (
            f'    table = bodo.hiframes.table.set_table_len(table, n_rows)\n')
        for i, sqdre__fxz in enumerate(zxp__zrk):
            uwro__kjzx += f"""    table = bodo.hiframes.table.set_table_block(table, data_arrs_{i}, {oylp__ray.type_to_blk[sqdre__fxz]})
"""
        uwro__kjzx += (
            '    result = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
        uwro__kjzx += '        (table,), index, columns_typ\n'
        uwro__kjzx += '    )\n'
    else:
        mmd__dfve = ', '.join(f'data_arrs_{i}' for i in range(len(zxp__zrk)))
        uwro__kjzx += f"""    table = bodo.hiframes.table.init_runtime_table_from_lists(({mmd__dfve},), n_rows)
"""
        uwro__kjzx += (
            '    result = bodo.hiframes.pd_dataframe_ext.init_runtime_cols_dataframe(\n'
            )
        uwro__kjzx += '        (table,), index, column_index\n'
        uwro__kjzx += '    )\n'
    uwro__kjzx += '    ev.finalize()\n'
    uwro__kjzx += '    return result\n'
    zeto__ixtc = {}
    qhqtl__wrwr = {f'data_arr_typ_{i}': zezzf__dqry for i, zezzf__dqry in
        enumerate(zxp__zrk)}
    bmec__pmlr = {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'info_from_table': info_from_table, 'table_type':
        oylp__ray, 'columns_typ': yqtl__wzlp, 'index_names_lit': qnd__uzpv,
        'value_names_lit': fhad__lzu, 'columns_name_lit': hdxt__itlc, **
        qhqtl__wrwr, 'tracing': tracing}
    exec(uwro__kjzx, bmec__pmlr, zeto__ixtc)
    impl = zeto__ixtc['impl']
    return impl


def gen_pandas_parquet_metadata(column_names, data_types, index,
    write_non_range_index_to_metadata, write_rangeindex_to_metadata,
    partition_cols=None, is_runtime_columns=False):
    lbu__agny = {}
    lbu__agny['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for col_name, lcg__dkx in zip(column_names, data_types):
        if col_name in partition_cols:
            continue
        vmlpp__zid = None
        if isinstance(lcg__dkx, bodo.DatetimeArrayType):
            dmt__ytt = 'datetimetz'
            watj__bgwwy = 'datetime64[ns]'
            if isinstance(lcg__dkx.tz, int):
                podd__grdup = (bodo.libs.pd_datetime_arr_ext.
                    nanoseconds_to_offset(lcg__dkx.tz))
            else:
                podd__grdup = pd.DatetimeTZDtype(tz=lcg__dkx.tz).tz
            vmlpp__zid = {'timezone': pa.lib.tzinfo_to_string(podd__grdup)}
        elif isinstance(lcg__dkx, types.Array) or lcg__dkx == boolean_array:
            dmt__ytt = watj__bgwwy = lcg__dkx.dtype.name
            if watj__bgwwy.startswith('datetime'):
                dmt__ytt = 'datetime'
        elif is_str_arr_type(lcg__dkx):
            dmt__ytt = 'unicode'
            watj__bgwwy = 'object'
        elif lcg__dkx == binary_array_type:
            dmt__ytt = 'bytes'
            watj__bgwwy = 'object'
        elif isinstance(lcg__dkx, DecimalArrayType):
            dmt__ytt = watj__bgwwy = 'object'
        elif isinstance(lcg__dkx, IntegerArrayType):
            mlxk__tcjsc = lcg__dkx.dtype.name
            if mlxk__tcjsc.startswith('int'):
                dmt__ytt = 'Int' + mlxk__tcjsc[3:]
            elif mlxk__tcjsc.startswith('uint'):
                dmt__ytt = 'UInt' + mlxk__tcjsc[4:]
            else:
                if is_runtime_columns:
                    col_name = 'Runtime determined column of type'
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(col_name, lcg__dkx))
            watj__bgwwy = lcg__dkx.dtype.name
        elif lcg__dkx == datetime_date_array_type:
            dmt__ytt = 'datetime'
            watj__bgwwy = 'object'
        elif isinstance(lcg__dkx, TimeArrayType):
            dmt__ytt = 'datetime'
            watj__bgwwy = 'object'
        elif isinstance(lcg__dkx, (StructArrayType, ArrayItemArrayType)):
            dmt__ytt = 'object'
            watj__bgwwy = 'object'
        else:
            if is_runtime_columns:
                col_name = 'Runtime determined column of type'
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(col_name, lcg__dkx))
        wye__dzw = {'name': col_name, 'field_name': col_name, 'pandas_type':
            dmt__ytt, 'numpy_type': watj__bgwwy, 'metadata': vmlpp__zid}
        lbu__agny['columns'].append(wye__dzw)
    if write_non_range_index_to_metadata:
        if isinstance(index, MultiIndexType):
            raise BodoError('to_parquet: MultiIndex not supported yet')
        if 'none' in index.name:
            kdt__xsqbw = '__index_level_0__'
            aejbg__zfj = None
        else:
            kdt__xsqbw = '%s'
            aejbg__zfj = '%s'
        lbu__agny['index_columns'] = [kdt__xsqbw]
        lbu__agny['columns'].append({'name': aejbg__zfj, 'field_name':
            kdt__xsqbw, 'pandas_type': index.pandas_type_name, 'numpy_type':
            index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        lbu__agny['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        lbu__agny['index_columns'] = []
    lbu__agny['pandas_version'] = pd.__version__
    return lbu__agny


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
        rdkqw__twwc = []
        for pbar__sfhr in partition_cols:
            try:
                idx = df.columns.index(pbar__sfhr)
            except ValueError as zqws__ogd:
                raise BodoError(
                    f'Partition column {pbar__sfhr} is not in dataframe')
            rdkqw__twwc.append(idx)
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
    lsqa__cmm = isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType)
    cjjg__qnrm = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not lsqa__cmm)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not lsqa__cmm or is_overload_true
        (_is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and lsqa__cmm and not is_overload_true(_is_parallel)
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
        mgox__qrd = df.runtime_data_types
        ktv__cbdxg = len(mgox__qrd)
        vmlpp__zid = gen_pandas_parquet_metadata([''] * ktv__cbdxg,
            mgox__qrd, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=True)
        tqmpe__klg = vmlpp__zid['columns'][:ktv__cbdxg]
        vmlpp__zid['columns'] = vmlpp__zid['columns'][ktv__cbdxg:]
        tqmpe__klg = [json.dumps(ckw__fjoi).replace('""', '{0}') for
            ckw__fjoi in tqmpe__klg]
        all__wqygx = json.dumps(vmlpp__zid)
        zifcn__nhqek = '"columns": ['
        drkvr__wkc = all__wqygx.find(zifcn__nhqek)
        if drkvr__wkc == -1:
            raise BodoError(
                'DataFrame.to_parquet(): Unexpected metadata string for runtime columns.  Please return the DataFrame to regular Python to update typing information.'
                )
        xdt__nmrh = drkvr__wkc + len(zifcn__nhqek)
        gvhh__bsrl = all__wqygx[:xdt__nmrh]
        all__wqygx = all__wqygx[xdt__nmrh:]
        nmhl__xfy = len(vmlpp__zid['columns'])
    else:
        all__wqygx = json.dumps(gen_pandas_parquet_metadata(df.columns, df.
            data, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=False))
    if not is_overload_true(_is_parallel) and lsqa__cmm:
        all__wqygx = all__wqygx.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            all__wqygx = all__wqygx.replace('"%s"', '%s')
    if not df.is_table_format:
        gkmpn__nab = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
            .format(i) for i in range(len(df.columns)))
    uwro__kjzx = """def df_to_parquet(df, path, engine='auto', compression='snappy', index=None, partition_cols=None, storage_options=None, row_group_size=-1, _bodo_file_prefix='part-', _bodo_timestamp_tz=None, _is_parallel=False):
"""
    if df.is_table_format:
        uwro__kjzx += '    py_table = get_dataframe_table(df)\n'
        uwro__kjzx += (
            '    table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        uwro__kjzx += '    info_list = [{}]\n'.format(gkmpn__nab)
        uwro__kjzx += '    table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        uwro__kjzx += '    columns_index = get_dataframe_column_names(df)\n'
        uwro__kjzx += '    names_arr = index_to_array(columns_index)\n'
        uwro__kjzx += '    col_names = array_to_info(names_arr)\n'
    else:
        uwro__kjzx += '    col_names = array_to_info(col_names_arr)\n'
    if is_overload_true(index) or is_overload_none(index) and cjjg__qnrm:
        uwro__kjzx += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        xypdh__xmqmt = True
    else:
        uwro__kjzx += '    index_col = array_to_info(np.empty(0))\n'
        xypdh__xmqmt = False
    if df.has_runtime_cols:
        uwro__kjzx += '    columns_lst = []\n'
        uwro__kjzx += '    num_cols = 0\n'
        for i in range(len(df.runtime_data_types)):
            uwro__kjzx += f'    for _ in range(len(py_table.block_{i})):\n'
            uwro__kjzx += f"""        columns_lst.append({tqmpe__klg[i]!r}.replace('{{0}}', '"' + names_arr[num_cols] + '"'))
"""
            uwro__kjzx += '        num_cols += 1\n'
        if nmhl__xfy:
            uwro__kjzx += "    columns_lst.append('')\n"
        uwro__kjzx += '    columns_str = ", ".join(columns_lst)\n'
        uwro__kjzx += ('    metadata = """' + gvhh__bsrl +
            '""" + columns_str + """' + all__wqygx + '"""\n')
    else:
        uwro__kjzx += '    metadata = """' + all__wqygx + '"""\n'
    uwro__kjzx += '    if compression is None:\n'
    uwro__kjzx += "        compression = 'none'\n"
    uwro__kjzx += '    if _bodo_timestamp_tz is None:\n'
    uwro__kjzx += "        _bodo_timestamp_tz = ''\n"
    uwro__kjzx += '    if df.index.name is not None:\n'
    uwro__kjzx += '        name_ptr = df.index.name\n'
    uwro__kjzx += '    else:\n'
    uwro__kjzx += "        name_ptr = 'null'\n"
    uwro__kjzx += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(path, parallel=_is_parallel)
"""
    zwwrf__mkc = None
    if partition_cols:
        zwwrf__mkc = pd.array([col_name for col_name in df.columns if 
            col_name not in partition_cols])
        skdd__akeph = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in rdkqw__twwc)
        if skdd__akeph:
            uwro__kjzx += '    cat_info_list = [{}]\n'.format(skdd__akeph)
            uwro__kjzx += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            uwro__kjzx += '    cat_table = table\n'
        uwro__kjzx += (
            '    col_names_no_partitions = array_to_info(col_names_no_parts_arr)\n'
            )
        uwro__kjzx += (
            f'    part_cols_idxs = np.array({rdkqw__twwc}, dtype=np.int32)\n')
        uwro__kjzx += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(path),\n')
        uwro__kjzx += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        uwro__kjzx += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        uwro__kjzx += (
            '                            unicode_to_utf8(compression),\n')
        uwro__kjzx += '                            _is_parallel,\n'
        uwro__kjzx += (
            '                            unicode_to_utf8(bucket_region),\n')
        uwro__kjzx += '                            row_group_size,\n'
        uwro__kjzx += (
            '                            unicode_to_utf8(_bodo_file_prefix))\n'
            )
        uwro__kjzx += '    delete_table_decref_arrays(table)\n'
        uwro__kjzx += '    delete_info_decref_array(index_col)\n'
        uwro__kjzx += '    delete_info_decref_array(col_names_no_partitions)\n'
        uwro__kjzx += '    delete_info_decref_array(col_names)\n'
        if skdd__akeph:
            uwro__kjzx += '    delete_table_decref_arrays(cat_table)\n'
    elif write_rangeindex_to_metadata:
        uwro__kjzx += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        uwro__kjzx += (
            '                            table, col_names, index_col,\n')
        uwro__kjzx += '                            ' + str(xypdh__xmqmt
            ) + ',\n'
        uwro__kjzx += (
            '                            unicode_to_utf8(metadata),\n')
        uwro__kjzx += (
            '                            unicode_to_utf8(compression),\n')
        uwro__kjzx += (
            '                            _is_parallel, 1, df.index.start,\n')
        uwro__kjzx += (
            '                            df.index.stop, df.index.step,\n')
        uwro__kjzx += (
            '                            unicode_to_utf8(name_ptr),\n')
        uwro__kjzx += (
            '                            unicode_to_utf8(bucket_region),\n')
        uwro__kjzx += '                            row_group_size,\n'
        uwro__kjzx += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        uwro__kjzx += (
            '                            unicode_to_utf8(_bodo_timestamp_tz))\n'
            )
        uwro__kjzx += '    delete_table_decref_arrays(table)\n'
        uwro__kjzx += '    delete_info_decref_array(index_col)\n'
        uwro__kjzx += '    delete_info_decref_array(col_names)\n'
    else:
        uwro__kjzx += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        uwro__kjzx += (
            '                            table, col_names, index_col,\n')
        uwro__kjzx += '                            ' + str(xypdh__xmqmt
            ) + ',\n'
        uwro__kjzx += (
            '                            unicode_to_utf8(metadata),\n')
        uwro__kjzx += (
            '                            unicode_to_utf8(compression),\n')
        uwro__kjzx += '                            _is_parallel, 0, 0, 0, 0,\n'
        uwro__kjzx += (
            '                            unicode_to_utf8(name_ptr),\n')
        uwro__kjzx += (
            '                            unicode_to_utf8(bucket_region),\n')
        uwro__kjzx += '                            row_group_size,\n'
        uwro__kjzx += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        uwro__kjzx += (
            '                            unicode_to_utf8(_bodo_timestamp_tz))\n'
            )
        uwro__kjzx += '    delete_table_decref_arrays(table)\n'
        uwro__kjzx += '    delete_info_decref_array(index_col)\n'
        uwro__kjzx += '    delete_info_decref_array(col_names)\n'
    zeto__ixtc = {}
    if df.has_runtime_cols:
        llv__ussso = None
    else:
        for ijgf__mkus in df.columns:
            if not isinstance(ijgf__mkus, str):
                raise BodoError(
                    'DataFrame.to_parquet(): parquet must have string column names'
                    )
        llv__ussso = pd.array(df.columns)
    exec(uwro__kjzx, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array, 'delete_info_decref_array':
        delete_info_decref_array, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'col_names_arr': llv__ussso,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'get_dataframe_table': get_dataframe_table,
        'col_names_no_parts_arr': zwwrf__mkc, 'get_dataframe_column_names':
        get_dataframe_column_names, 'fix_arr_dtype': fix_arr_dtype,
        'decode_if_dict_array': decode_if_dict_array,
        'decode_if_dict_table': decode_if_dict_table}, zeto__ixtc)
    orj__sfoht = zeto__ixtc['df_to_parquet']
    return orj__sfoht


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_table_create=False, _is_parallel=False):
    smwtm__qxz = 'all_ok'
    etbtc__iep, fuk__nko = bodo.ir.sql_ext.parse_dbtype(con)
    if _is_parallel and bodo.get_rank() == 0:
        jtp__haku = 100
        if chunksize is None:
            fgl__llve = jtp__haku
        else:
            fgl__llve = min(chunksize, jtp__haku)
        if _is_table_create:
            df = df.iloc[:fgl__llve, :]
        else:
            df = df.iloc[fgl__llve:, :]
            if len(df) == 0:
                return smwtm__qxz
    kibvg__rxtxb = df.columns
    try:
        if etbtc__iep == 'oracle':
            import os
            import sqlalchemy as sa
            from sqlalchemy.dialects.oracle import VARCHAR2
            obgul__epn = os.environ.get('BODO_DISABLE_ORACLE_VARCHAR2', None)
            lcq__kijq = bodo.typeof(df)
            xyq__dsb = {}
            for aroc__rhq, zpy__bxm in zip(lcq__kijq.columns, lcq__kijq.data):
                if df[aroc__rhq].dtype == 'object':
                    if zpy__bxm == datetime_date_array_type:
                        xyq__dsb[aroc__rhq] = sa.types.Date
                    elif zpy__bxm in (bodo.string_array_type, bodo.
                        dict_str_arr_type) and (not obgul__epn or 
                        obgul__epn == '0'):
                        xyq__dsb[aroc__rhq] = VARCHAR2(4000)
            dtype = xyq__dsb
        try:
            df.to_sql(name, con, schema, if_exists, index, index_label,
                chunksize, dtype, method)
        except Exception as lataz__chkc:
            smwtm__qxz = lataz__chkc.args[0]
            if etbtc__iep == 'oracle' and 'ORA-12899' in smwtm__qxz:
                smwtm__qxz += """
                String is larger than VARCHAR2 maximum length.
                Please set environment variable `BODO_DISABLE_ORACLE_VARCHAR2` to
                disable Bodo's optimziation use of VARCHA2.
                NOTE: Oracle `to_sql` with CLOB datatypes is known to be really slow.
                """
        return smwtm__qxz
    finally:
        df.columns = kibvg__rxtxb


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
    except ImportError as zqws__ogd:
        pass
    if df.has_runtime_cols:
        llv__ussso = None
    else:
        for ijgf__mkus in df.columns:
            if not isinstance(ijgf__mkus, str):
                raise BodoError(
                    'DataFrame.to_sql(): input dataframe must have string column names. Please return the DataFrame with runtime column names to regular Python to modify column names.'
                    )
        llv__ussso = pd.array(df.columns)
    uwro__kjzx = 'def df_to_sql(\n'
    uwro__kjzx += '    df, name, con,\n'
    uwro__kjzx += (
        "    schema=None, if_exists='fail', index=True, index_label=None,\n")
    uwro__kjzx += (
        '    chunksize=None, dtype=None, method=None, _is_parallel=False,\n')
    uwro__kjzx += '):\n'
    uwro__kjzx += f"    if con.startswith('iceberg'):\n"
    uwro__kjzx += (
        f'        con_str = bodo.io.iceberg.format_iceberg_conn_njit(con)\n')
    uwro__kjzx += f'        if schema is None:\n'
    uwro__kjzx += f"""            raise ValueError('DataFrame.to_sql(): schema must be provided when writing to an Iceberg table.')
"""
    uwro__kjzx += f'        if chunksize is not None:\n'
    uwro__kjzx += f"""            raise ValueError('DataFrame.to_sql(): chunksize not supported for Iceberg tables.')
"""
    uwro__kjzx += f'        if index and bodo.get_rank() == 0:\n'
    uwro__kjzx += (
        f"            warnings.warn('index is not supported for Iceberg tables.')      \n"
        )
    uwro__kjzx += (
        f'        if index_label is not None and bodo.get_rank() == 0:\n')
    uwro__kjzx += (
        f"            warnings.warn('index_label is not supported for Iceberg tables.')\n"
        )
    if df.is_table_format:
        uwro__kjzx += f'        py_table = get_dataframe_table(df)\n'
        uwro__kjzx += (
            f'        table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        gkmpn__nab = ', '.join(
            f'array_to_info(get_dataframe_data(df, {i}))' for i in range(
            len(df.columns)))
        uwro__kjzx += f'        info_list = [{gkmpn__nab}]\n'
        uwro__kjzx += f'        table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        uwro__kjzx += (
            f'        columns_index = get_dataframe_column_names(df)\n')
        uwro__kjzx += f'        names_arr = index_to_array(columns_index)\n'
        uwro__kjzx += f'        col_names = array_to_info(names_arr)\n'
    else:
        uwro__kjzx += f'        col_names = array_to_info(col_names_arr)\n'
    uwro__kjzx += """        bodo.io.iceberg.iceberg_write(
            name, con_str, schema, table, col_names, if_exists,
            _is_parallel, pyarrow_table_schema,
        )
"""
    uwro__kjzx += f'        delete_table_decref_arrays(table)\n'
    uwro__kjzx += f'        delete_info_decref_array(col_names)\n'
    uwro__kjzx += "    elif con.startswith('snowflake'):\n"
    uwro__kjzx += """        if index and bodo.get_rank() == 0:
            warnings.warn('index is not supported for Snowflake tables.')      
        if index_label is not None and bodo.get_rank() == 0:
            warnings.warn('index_label is not supported for Snowflake tables.')
        ev = tracing.Event('snowflake_write_impl')
"""
    uwro__kjzx += "        location = ''\n"
    if not is_overload_none(schema):
        uwro__kjzx += '        location += \'"\' + schema + \'".\'\n'
    uwro__kjzx += '        location += \'"\' + name + \'"\'\n'
    uwro__kjzx += '        my_rank = bodo.get_rank()\n'
    uwro__kjzx += """        with bodo.objmode(
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
    uwro__kjzx += '        bodo.barrier()\n'
    uwro__kjzx += '        if chunksize is None:\n'
    uwro__kjzx += """            ev_estimate_chunksize = tracing.Event('estimate_chunksize')          
"""
    if df.is_table_format and len(df.columns) > 0:
        uwro__kjzx += f"""            nbytes_arr = np.empty({len(df.columns)}, np.int64)
            table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, 0)
            memory_usage = np.sum(nbytes_arr)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        yagap__nxqv = ',' if len(df.columns) == 1 else ''
        uwro__kjzx += f"""            memory_usage = np.array(({data}{yagap__nxqv}), np.int64).sum()
"""
    uwro__kjzx += """            nsplits = int(max(1, memory_usage / bodo.io.snowflake.SF_WRITE_PARQUET_CHUNK_SIZE))
            chunksize = max(1, (len(df) + nsplits - 1) // nsplits)
            ev_estimate_chunksize.finalize()
"""
    if df.has_runtime_cols:
        uwro__kjzx += (
            '        columns_index = get_dataframe_column_names(df)\n')
        uwro__kjzx += '        names_arr = index_to_array(columns_index)\n'
        uwro__kjzx += '        col_names = array_to_info(names_arr)\n'
    else:
        uwro__kjzx += '        col_names = array_to_info(col_names_arr)\n'
    uwro__kjzx += '        index_col = array_to_info(np.empty(0))\n'
    uwro__kjzx += """        bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(parquet_path, parallel=_is_parallel)
"""
    uwro__kjzx += """        ev_upload_df = tracing.Event('upload_df', is_parallel=False)           
"""
    uwro__kjzx += '        upload_threads_in_progress = []\n'
    uwro__kjzx += """        for chunk_idx, i in enumerate(range(0, len(df), chunksize)):           
"""
    uwro__kjzx += """            chunk_name = f'file{chunk_idx}_rank{my_rank}_{bodo.io.helpers.uuid4_helper()}.parquet'
"""
    uwro__kjzx += '            chunk_path = parquet_path + chunk_name\n'
    uwro__kjzx += (
        '            chunk_path = chunk_path.replace("\\\\", "\\\\\\\\")\n')
    uwro__kjzx += (
        '            chunk_path = chunk_path.replace("\'", "\\\\\'")\n')
    uwro__kjzx += """            ev_to_df_table = tracing.Event(f'to_df_table_{chunk_idx}', is_parallel=False)
"""
    uwro__kjzx += '            chunk = df.iloc[i : i + chunksize]\n'
    if df.is_table_format:
        uwro__kjzx += (
            '            py_table_chunk = get_dataframe_table(chunk)\n')
        uwro__kjzx += """            table_chunk = py_table_to_cpp_table(py_table_chunk, py_table_typ)
"""
    else:
        vdi__vpq = ', '.join(
            f'array_to_info(get_dataframe_data(chunk, {i}))' for i in range
            (len(df.columns)))
        uwro__kjzx += (
            f'            table_chunk = arr_info_list_to_table([{vdi__vpq}])     \n'
            )
    uwro__kjzx += '            ev_to_df_table.finalize()\n'
    uwro__kjzx += """            ev_pq_write_cpp = tracing.Event(f'pq_write_cpp_{chunk_idx}', is_parallel=False)
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
    uwro__kjzx += '        bodo.barrier()\n'
    uwro__kjzx += """        df_columns = df.columns
        with bodo.objmode():
            bodo.io.snowflake.create_table_copy_into(
                cursor, stage_name, location, df_columns, if_exists, old_creds, tmp_folder,
            )
"""
    uwro__kjzx += '        ev.finalize(sync=False)\n'
    uwro__kjzx += '    else:\n'
    uwro__kjzx += '        rank = bodo.libs.distributed_api.get_rank()\n'
    uwro__kjzx += "        err_msg = 'unset'\n"
    uwro__kjzx += '        if rank != 0:\n'
    uwro__kjzx += """            err_msg = bodo.libs.distributed_api.bcast_scalar(err_msg)          
"""
    uwro__kjzx += '        elif rank == 0:\n'
    uwro__kjzx += '            err_msg = to_sql_exception_guard_encaps(\n'
    uwro__kjzx += """                          df, name, con, schema, if_exists, index, index_label,
"""
    uwro__kjzx += '                          chunksize, dtype, method,\n'
    uwro__kjzx += '                          True, _is_parallel,\n'
    uwro__kjzx += '                      )\n'
    uwro__kjzx += """            err_msg = bodo.libs.distributed_api.bcast_scalar(err_msg)          
"""
    uwro__kjzx += "        if_exists = 'append'\n"
    uwro__kjzx += "        if _is_parallel and err_msg == 'all_ok':\n"
    uwro__kjzx += '            err_msg = to_sql_exception_guard_encaps(\n'
    uwro__kjzx += """                          df, name, con, schema, if_exists, index, index_label,
"""
    uwro__kjzx += '                          chunksize, dtype, method,\n'
    uwro__kjzx += '                          False, _is_parallel,\n'
    uwro__kjzx += '                      )\n'
    uwro__kjzx += "        if err_msg != 'all_ok':\n"
    uwro__kjzx += "            print('err_msg=', err_msg)\n"
    uwro__kjzx += (
        "            raise ValueError('error in to_sql() operation')\n")
    zeto__ixtc = {}
    bmec__pmlr = globals().copy()
    bmec__pmlr.update({'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info, 'bodo': bodo, 'col_names_arr':
        llv__ussso, 'delete_info_decref_array': delete_info_decref_array,
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
    exec(uwro__kjzx, bmec__pmlr, zeto__ixtc)
    _impl = zeto__ixtc['df_to_sql']
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
        sfaw__pga = get_overload_const_str(path_or_buf)
        if sfaw__pga.endswith(('.gz', '.bz2', '.zip', '.xz')):
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
        ygp__muel = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(ygp__muel), unicode_to_utf8(_bodo_file_prefix))
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(ygp__muel), unicode_to_utf8(_bodo_file_prefix))
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    idvg__kagz = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    byjw__vcyeb = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pandas.get_dummies', idvg__kagz, byjw__vcyeb,
        package_name='pandas', module_name='General')
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pandas.get_dummies() only support categorical data types with explicitly known categories'
            )
    uwro__kjzx = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        mbt__doyd = data.data.dtype.categories
        uwro__kjzx += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        mbt__doyd = data.dtype.categories
        uwro__kjzx += '  data_values = data\n'
    zhhno__ruq = len(mbt__doyd)
    uwro__kjzx += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    uwro__kjzx += '  numba.parfors.parfor.init_prange()\n'
    uwro__kjzx += '  n = len(data_values)\n'
    for i in range(zhhno__ruq):
        uwro__kjzx += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    uwro__kjzx += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    uwro__kjzx += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for nyvaq__yfkih in range(zhhno__ruq):
        uwro__kjzx += '          data_arr_{}[i] = 0\n'.format(nyvaq__yfkih)
    uwro__kjzx += '      else:\n'
    for xfg__lma in range(zhhno__ruq):
        uwro__kjzx += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            xfg__lma)
    gkmpn__nab = ', '.join(f'data_arr_{i}' for i in range(zhhno__ruq))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    if isinstance(mbt__doyd[0], np.datetime64):
        mbt__doyd = tuple(pd.Timestamp(aroc__rhq) for aroc__rhq in mbt__doyd)
    elif isinstance(mbt__doyd[0], np.timedelta64):
        mbt__doyd = tuple(pd.Timedelta(aroc__rhq) for aroc__rhq in mbt__doyd)
    return bodo.hiframes.dataframe_impl._gen_init_df(uwro__kjzx, mbt__doyd,
        gkmpn__nab, index)


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
    for uhxue__mckpk in pd_unsupported:
        tcw__zuu = mod_name + '.' + uhxue__mckpk.__name__
        overload(uhxue__mckpk, no_unliteral=True)(create_unsupported_overload
            (tcw__zuu))


def _install_dataframe_unsupported():
    for sgc__zpw in dataframe_unsupported_attrs:
        byae__hbkp = 'DataFrame.' + sgc__zpw
        overload_attribute(DataFrameType, sgc__zpw)(create_unsupported_overload
            (byae__hbkp))
    for tcw__zuu in dataframe_unsupported:
        byae__hbkp = 'DataFrame.' + tcw__zuu + '()'
        overload_method(DataFrameType, tcw__zuu)(create_unsupported_overload
            (byae__hbkp))


_install_pd_unsupported('pandas', pd_unsupported)
_install_pd_unsupported('pandas.util', pd_util_unsupported)
_install_dataframe_unsupported()
