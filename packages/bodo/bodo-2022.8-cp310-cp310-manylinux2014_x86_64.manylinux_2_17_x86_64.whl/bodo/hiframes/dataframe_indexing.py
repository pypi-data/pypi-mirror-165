"""
Indexing support for pd.DataFrame type.
"""
import operator
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported
from bodo.utils.transform import gen_const_tup
from bodo.utils.typing import BodoError, get_overload_const_int, get_overload_const_list, get_overload_const_str, is_immutable_array, is_list_like_index_type, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, raise_bodo_error


@infer_global(operator.getitem)
class DataFrameGetItemTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        check_runtime_cols_unsupported(args[0], 'DataFrame getitem (df[])')
        if isinstance(args[0], DataFrameType):
            return self.typecheck_df_getitem(args)
        elif isinstance(args[0], DataFrameLocType):
            return self.typecheck_loc_getitem(args)
        else:
            return

    def typecheck_loc_getitem(self, args):
        I = args[0]
        idx = args[1]
        df = I.df_type
        if isinstance(df.columns[0], tuple):
            raise_bodo_error(
                'DataFrame.loc[] getitem (location-based indexing) with multi-indexed columns not supported yet'
                )
        if is_list_like_index_type(idx) and idx.dtype == types.bool_:
            suaz__hbl = idx
            qytj__dnakt = df.data
            fzpii__veat = df.columns
            ykwap__jbii = self.replace_range_with_numeric_idx_if_needed(df,
                suaz__hbl)
            dcm__onu = DataFrameType(qytj__dnakt, ykwap__jbii, fzpii__veat,
                is_table_format=df.is_table_format)
            return dcm__onu(*args)
        if isinstance(idx, types.BaseTuple) and len(idx) == 2:
            pffbi__bik = idx.types[0]
            myz__gvdt = idx.types[1]
            if isinstance(pffbi__bik, types.Integer):
                if not isinstance(df.index, bodo.hiframes.pd_index_ext.
                    RangeIndexType):
                    raise_bodo_error(
                        'Dataframe.loc[int, col_ind] getitem only supported for dataframes with RangeIndexes'
                        )
                if is_overload_constant_str(myz__gvdt):
                    ycdij__jwa = get_overload_const_str(myz__gvdt)
                    if ycdij__jwa not in df.columns:
                        raise_bodo_error(
                            'dataframe {} does not include column {}'.
                            format(df, ycdij__jwa))
                    afkww__eqxi = df.columns.index(ycdij__jwa)
                    return df.data[afkww__eqxi].dtype(*args)
                if isinstance(myz__gvdt, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                else:
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
                        )
            if is_list_like_index_type(pffbi__bik
                ) and pffbi__bik.dtype == types.bool_ or isinstance(pffbi__bik,
                types.SliceType):
                ykwap__jbii = self.replace_range_with_numeric_idx_if_needed(df,
                    pffbi__bik)
                if is_overload_constant_str(myz__gvdt):
                    bjnu__dbey = get_overload_const_str(myz__gvdt)
                    if bjnu__dbey not in df.columns:
                        raise_bodo_error(
                            f'dataframe {df} does not include column {bjnu__dbey}'
                            )
                    afkww__eqxi = df.columns.index(bjnu__dbey)
                    rcefn__pnscm = df.data[afkww__eqxi]
                    vzsl__ysz = rcefn__pnscm.dtype
                    bhmgd__uhlc = types.literal(df.columns[afkww__eqxi])
                    dcm__onu = bodo.SeriesType(vzsl__ysz, rcefn__pnscm,
                        ykwap__jbii, bhmgd__uhlc)
                    return dcm__onu(*args)
                if isinstance(myz__gvdt, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                elif is_overload_constant_list(myz__gvdt):
                    otow__xpa = get_overload_const_list(myz__gvdt)
                    hwwu__eisuz = types.unliteral(myz__gvdt)
                    if hwwu__eisuz.dtype == types.bool_:
                        if len(df.columns) != len(otow__xpa):
                            raise_bodo_error(
                                f'dataframe {df} has {len(df.columns)} columns, but boolean array used with DataFrame.loc[] {otow__xpa} has {len(otow__xpa)} values'
                                )
                        qenix__eas = []
                        lhto__jxk = []
                        for gsyk__ywqh in range(len(otow__xpa)):
                            if otow__xpa[gsyk__ywqh]:
                                qenix__eas.append(df.columns[gsyk__ywqh])
                                lhto__jxk.append(df.data[gsyk__ywqh])
                        btb__aphsx = tuple()
                        efl__oar = df.is_table_format and len(qenix__eas
                            ) > 0 and len(qenix__eas
                            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
                        dcm__onu = DataFrameType(tuple(lhto__jxk),
                            ykwap__jbii, tuple(qenix__eas), is_table_format
                            =efl__oar)
                        return dcm__onu(*args)
                    elif hwwu__eisuz.dtype == bodo.string_type:
                        btb__aphsx, lhto__jxk = (
                            get_df_getitem_kept_cols_and_data(df, otow__xpa))
                        efl__oar = df.is_table_format and len(otow__xpa
                            ) > 0 and len(otow__xpa
                            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
                        dcm__onu = DataFrameType(lhto__jxk, ykwap__jbii,
                            btb__aphsx, is_table_format=efl__oar)
                        return dcm__onu(*args)
        raise_bodo_error(
            f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet. If you are trying to select a subset of the columns by passing a list of column names, that list must be a compile time constant. See https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )

    def typecheck_df_getitem(self, args):
        df = args[0]
        ind = args[1]
        if is_overload_constant_str(ind) or is_overload_constant_int(ind):
            ind_val = get_overload_const_str(ind) if is_overload_constant_str(
                ind) else get_overload_const_int(ind)
            if isinstance(df.columns[0], tuple):
                qenix__eas = []
                lhto__jxk = []
                for gsyk__ywqh, ngqdu__azwbz in enumerate(df.columns):
                    if ngqdu__azwbz[0] != ind_val:
                        continue
                    qenix__eas.append(ngqdu__azwbz[1] if len(ngqdu__azwbz) ==
                        2 else ngqdu__azwbz[1:])
                    lhto__jxk.append(df.data[gsyk__ywqh])
                rcefn__pnscm = tuple(lhto__jxk)
                kkrr__ybx = df.index
                zsq__zxr = tuple(qenix__eas)
                dcm__onu = DataFrameType(rcefn__pnscm, kkrr__ybx, zsq__zxr)
                return dcm__onu(*args)
            else:
                if ind_val not in df.columns:
                    raise_bodo_error('dataframe {} does not include column {}'
                        .format(df, ind_val))
                afkww__eqxi = df.columns.index(ind_val)
                rcefn__pnscm = df.data[afkww__eqxi]
                vzsl__ysz = rcefn__pnscm.dtype
                kkrr__ybx = df.index
                bhmgd__uhlc = types.literal(df.columns[afkww__eqxi])
                dcm__onu = bodo.SeriesType(vzsl__ysz, rcefn__pnscm,
                    kkrr__ybx, bhmgd__uhlc)
                return dcm__onu(*args)
        if isinstance(ind, types.Integer) or isinstance(ind, types.UnicodeType
            ):
            raise_bodo_error(
                'df[] getitem selecting a subset of columns requires providing constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        if is_list_like_index_type(ind
            ) and ind.dtype == types.bool_ or isinstance(ind, types.SliceType):
            rcefn__pnscm = df.data
            kkrr__ybx = self.replace_range_with_numeric_idx_if_needed(df, ind)
            zsq__zxr = df.columns
            dcm__onu = DataFrameType(rcefn__pnscm, kkrr__ybx, zsq__zxr,
                is_table_format=df.is_table_format)
            return dcm__onu(*args)
        elif is_overload_constant_list(ind):
            wcu__wzgmq = get_overload_const_list(ind)
            zsq__zxr, rcefn__pnscm = get_df_getitem_kept_cols_and_data(df,
                wcu__wzgmq)
            kkrr__ybx = df.index
            efl__oar = df.is_table_format and len(wcu__wzgmq) > 0 and len(
                wcu__wzgmq) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
            dcm__onu = DataFrameType(rcefn__pnscm, kkrr__ybx, zsq__zxr,
                is_table_format=efl__oar)
            return dcm__onu(*args)
        raise_bodo_error(
            f'df[] getitem using {ind} not supported. If you are trying to select a subset of the columns, you must provide the column names you are selecting as a constant. See https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )

    def replace_range_with_numeric_idx_if_needed(self, df, ind):
        ykwap__jbii = bodo.hiframes.pd_index_ext.NumericIndexType(types.
            int64, df.index.name_typ) if not isinstance(ind, types.SliceType
            ) and isinstance(df.index, bodo.hiframes.pd_index_ext.
            RangeIndexType) else df.index
        return ykwap__jbii


DataFrameGetItemTemplate._no_unliteral = True


def get_df_getitem_kept_cols_and_data(df, cols_to_keep_list):
    for rqq__suyxn in cols_to_keep_list:
        if rqq__suyxn not in df.column_index:
            raise_bodo_error('Column {} not found in dataframe columns {}'.
                format(rqq__suyxn, df.columns))
    zsq__zxr = tuple(cols_to_keep_list)
    rcefn__pnscm = tuple(df.data[df.column_index[hzs__rbu]] for hzs__rbu in
        zsq__zxr)
    return zsq__zxr, rcefn__pnscm


@lower_builtin(operator.getitem, DataFrameType, types.Any)
def getitem_df_lower(context, builder, sig, args):
    impl = df_getitem_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def df_getitem_overload(df, ind):
    if not isinstance(df, DataFrameType):
        return
    if is_overload_constant_str(ind) or is_overload_constant_int(ind):
        ind_val = get_overload_const_str(ind) if is_overload_constant_str(ind
            ) else get_overload_const_int(ind)
        if isinstance(df.columns[0], tuple):
            qenix__eas = []
            lhto__jxk = []
            for gsyk__ywqh, ngqdu__azwbz in enumerate(df.columns):
                if ngqdu__azwbz[0] != ind_val:
                    continue
                qenix__eas.append(ngqdu__azwbz[1] if len(ngqdu__azwbz) == 2
                     else ngqdu__azwbz[1:])
                lhto__jxk.append(
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'
                    .format(gsyk__ywqh))
            lkm__yckrp = 'def impl(df, ind):\n'
            hxu__pezd = (
                'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
            return bodo.hiframes.dataframe_impl._gen_init_df(lkm__yckrp,
                qenix__eas, ', '.join(lhto__jxk), hxu__pezd)
        if ind_val not in df.columns:
            raise_bodo_error('dataframe {} does not include column {}'.
                format(df, ind_val))
        col_no = df.columns.index(ind_val)
        return lambda df, ind: bodo.hiframes.pd_series_ext.init_series(bodo
            .hiframes.pd_dataframe_ext.get_dataframe_data(df, col_no), bodo
            .hiframes.pd_dataframe_ext.get_dataframe_index(df), ind_val)
    if is_overload_constant_list(ind):
        wcu__wzgmq = get_overload_const_list(ind)
        for rqq__suyxn in wcu__wzgmq:
            if rqq__suyxn not in df.column_index:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(rqq__suyxn, df.columns))
        reex__xukx = None
        if df.is_table_format and len(wcu__wzgmq) > 0 and len(wcu__wzgmq
            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD:
            pauh__ftzr = [df.column_index[rqq__suyxn] for rqq__suyxn in
                wcu__wzgmq]
            reex__xukx = {'col_nums_meta': bodo.utils.typing.MetaType(tuple
                (pauh__ftzr))}
            lhto__jxk = (
                f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, True)'
                )
        else:
            lhto__jxk = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[rqq__suyxn]}).copy()'
                 for rqq__suyxn in wcu__wzgmq)
        lkm__yckrp = 'def impl(df, ind):\n'
        hxu__pezd = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
        return bodo.hiframes.dataframe_impl._gen_init_df(lkm__yckrp,
            wcu__wzgmq, lhto__jxk, hxu__pezd, extra_globals=reex__xukx)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_ or isinstance(
        ind, types.SliceType):
        lkm__yckrp = 'def impl(df, ind):\n'
        if not isinstance(ind, types.SliceType):
            lkm__yckrp += (
                '  ind = bodo.utils.conversion.coerce_to_ndarray(ind)\n')
        hxu__pezd = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[ind]')
        if df.is_table_format:
            lhto__jxk = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[ind]')
        else:
            lhto__jxk = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[rqq__suyxn]})[ind]'
                 for rqq__suyxn in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(lkm__yckrp, df.
            columns, lhto__jxk, hxu__pezd)
    raise_bodo_error('df[] getitem using {} not supported'.format(ind))


@overload(operator.setitem, no_unliteral=True)
def df_setitem_overload(df, idx, val):
    check_runtime_cols_unsupported(df, 'DataFrame setitem (df[])')
    if not isinstance(df, DataFrameType):
        return
    raise_bodo_error('DataFrame setitem: transform necessary')


class DataFrameILocType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        hzs__rbu = 'DataFrameILocType({})'.format(df_type)
        super(DataFrameILocType, self).__init__(hzs__rbu)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameILocType)
class DataFrameILocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        htsqv__sjlr = [('obj', fe_type.df_type)]
        super(DataFrameILocModel, self).__init__(dmm, fe_type, htsqv__sjlr)


make_attribute_wrapper(DataFrameILocType, 'obj', '_obj')


@intrinsic
def init_dataframe_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        oqmjz__shrpe, = args
        mez__yibkn = signature.return_type
        pkwuo__faq = cgutils.create_struct_proxy(mez__yibkn)(context, builder)
        pkwuo__faq.obj = oqmjz__shrpe
        context.nrt.incref(builder, signature.args[0], oqmjz__shrpe)
        return pkwuo__faq._getvalue()
    return DataFrameILocType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'iloc')
def overload_dataframe_iloc(df):
    check_runtime_cols_unsupported(df, 'DataFrame.iloc')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_iloc(df)


@overload(operator.getitem, no_unliteral=True)
def overload_iloc_getitem(I, idx):
    if not isinstance(I, DataFrameILocType):
        return
    df = I.df_type
    if isinstance(idx, types.Integer):
        return _gen_iloc_getitem_row_impl(df, df.columns, 'idx')
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and not isinstance(
        idx[1], types.SliceType):
        if not (is_overload_constant_list(idx.types[1]) or
            is_overload_constant_int(idx.types[1])):
            raise_bodo_error(
                'idx2 in df.iloc[idx1, idx2] should be a constant integer or constant list of integers. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        zyoy__dtxr = len(df.data)
        if is_overload_constant_int(idx.types[1]):
            is_out_series = True
            uhh__llr = get_overload_const_int(idx.types[1])
            if uhh__llr < 0 or uhh__llr >= zyoy__dtxr:
                raise BodoError(
                    'df.iloc: column integer must refer to a valid column number'
                    )
            ymcli__tzbmm = [uhh__llr]
        else:
            is_out_series = False
            ymcli__tzbmm = get_overload_const_list(idx.types[1])
            if any(not isinstance(ind, int) or ind < 0 or ind >= zyoy__dtxr for
                ind in ymcli__tzbmm):
                raise BodoError(
                    'df.iloc: column list must be integers referring to a valid column number'
                    )
        col_names = tuple(pd.Series(df.columns, dtype=object)[ymcli__tzbmm])
        if isinstance(idx.types[0], types.Integer):
            if isinstance(idx.types[1], types.Integer):
                uhh__llr = ymcli__tzbmm[0]

                def impl(I, idx):
                    df = I._obj
                    return bodo.utils.conversion.box_if_dt64(bodo.hiframes.
                        pd_dataframe_ext.get_dataframe_data(df, uhh__llr)[
                        idx[0]])
                return impl
            return _gen_iloc_getitem_row_impl(df, col_names, 'idx[0]')
        if is_list_like_index_type(idx.types[0]) and isinstance(idx.types[0
            ].dtype, (types.Integer, types.Boolean)) or isinstance(idx.
            types[0], types.SliceType):
            return _gen_iloc_getitem_bool_slice_impl(df, col_names, idx.
                types[0], 'idx[0]', is_out_series)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, (types.
        Integer, types.Boolean)) or isinstance(idx, types.SliceType):
        return _gen_iloc_getitem_bool_slice_impl(df, df.columns, idx, 'idx',
            False)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):
        raise_bodo_error(
            'slice2 in df.iloc[slice1,slice2] should be constant. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )
    raise_bodo_error(f'df.iloc[] getitem using {idx} not supported')


def _gen_iloc_getitem_bool_slice_impl(df, col_names, idx_typ, idx,
    is_out_series):
    lkm__yckrp = 'def impl(I, idx):\n'
    lkm__yckrp += '  df = I._obj\n'
    if isinstance(idx_typ, types.SliceType):
        lkm__yckrp += f'  idx_t = {idx}\n'
    else:
        lkm__yckrp += (
            f'  idx_t = bodo.utils.conversion.coerce_to_ndarray({idx})\n')
    hxu__pezd = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]'
    reex__xukx = None
    if df.is_table_format and not is_out_series:
        pauh__ftzr = [df.column_index[rqq__suyxn] for rqq__suyxn in col_names]
        reex__xukx = {'col_nums_meta': bodo.utils.typing.MetaType(tuple(
            pauh__ftzr))}
        lhto__jxk = (
            f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, False)[idx_t]'
            )
    else:
        lhto__jxk = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[rqq__suyxn]})[idx_t]'
             for rqq__suyxn in col_names)
    if is_out_series:
        rhp__nvak = f"'{col_names[0]}'" if isinstance(col_names[0], str
            ) else f'{col_names[0]}'
        lkm__yckrp += f"""  return bodo.hiframes.pd_series_ext.init_series({lhto__jxk}, {hxu__pezd}, {rhp__nvak})
"""
        ijl__son = {}
        exec(lkm__yckrp, {'bodo': bodo}, ijl__son)
        return ijl__son['impl']
    return bodo.hiframes.dataframe_impl._gen_init_df(lkm__yckrp, col_names,
        lhto__jxk, hxu__pezd, extra_globals=reex__xukx)


def _gen_iloc_getitem_row_impl(df, col_names, idx):
    lkm__yckrp = 'def impl(I, idx):\n'
    lkm__yckrp += '  df = I._obj\n'
    czt__bsbhk = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[rqq__suyxn]})[{idx}]'
         for rqq__suyxn in col_names)
    lkm__yckrp += f"""  row_idx = bodo.hiframes.pd_index_ext.init_heter_index({gen_const_tup(col_names)}, None)
"""
    lkm__yckrp += f"""  return bodo.hiframes.pd_series_ext.init_series(({czt__bsbhk},), row_idx, None)
"""
    ijl__son = {}
    exec(lkm__yckrp, {'bodo': bodo}, ijl__son)
    impl = ijl__son['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def df_iloc_setitem_overload(df, idx, val):
    if not isinstance(df, DataFrameILocType):
        return
    raise_bodo_error(
        f'DataFrame.iloc setitem unsupported for dataframe {df.df_type}, index {idx}, value {val}'
        )


class DataFrameLocType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        hzs__rbu = 'DataFrameLocType({})'.format(df_type)
        super(DataFrameLocType, self).__init__(hzs__rbu)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameLocType)
class DataFrameLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        htsqv__sjlr = [('obj', fe_type.df_type)]
        super(DataFrameLocModel, self).__init__(dmm, fe_type, htsqv__sjlr)


make_attribute_wrapper(DataFrameLocType, 'obj', '_obj')


@intrinsic
def init_dataframe_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        oqmjz__shrpe, = args
        kedlz__coy = signature.return_type
        wvpk__fctt = cgutils.create_struct_proxy(kedlz__coy)(context, builder)
        wvpk__fctt.obj = oqmjz__shrpe
        context.nrt.incref(builder, signature.args[0], oqmjz__shrpe)
        return wvpk__fctt._getvalue()
    return DataFrameLocType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'loc')
def overload_dataframe_loc(df):
    check_runtime_cols_unsupported(df, 'DataFrame.loc')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_loc(df)


@lower_builtin(operator.getitem, DataFrameLocType, types.Any)
def loc_getitem_lower(context, builder, sig, args):
    impl = overload_loc_getitem(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def overload_loc_getitem(I, idx):
    if not isinstance(I, DataFrameLocType):
        return
    df = I.df_type
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        lkm__yckrp = 'def impl(I, idx):\n'
        lkm__yckrp += '  df = I._obj\n'
        lkm__yckrp += (
            '  idx_t = bodo.utils.conversion.coerce_to_ndarray(idx)\n')
        hxu__pezd = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
        if df.is_table_format:
            lhto__jxk = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[idx_t]'
                )
        else:
            lhto__jxk = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[rqq__suyxn]})[idx_t]'
                 for rqq__suyxn in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(lkm__yckrp, df.
            columns, lhto__jxk, hxu__pezd)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        wnrv__yoocw = idx.types[1]
        if is_overload_constant_str(wnrv__yoocw):
            ywvto__psjl = get_overload_const_str(wnrv__yoocw)
            uhh__llr = df.columns.index(ywvto__psjl)

            def impl_col_name(I, idx):
                df = I._obj
                hxu__pezd = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
                    df)
                mfmgj__cgttn = (bodo.hiframes.pd_dataframe_ext.
                    get_dataframe_data(df, uhh__llr))
                return bodo.hiframes.pd_series_ext.init_series(mfmgj__cgttn,
                    hxu__pezd, ywvto__psjl).loc[idx[0]]
            return impl_col_name
        if is_overload_constant_list(wnrv__yoocw):
            col_idx_list = get_overload_const_list(wnrv__yoocw)
            if len(col_idx_list) > 0 and not isinstance(col_idx_list[0], (
                bool, np.bool_)) and not all(rqq__suyxn in df.column_index for
                rqq__suyxn in col_idx_list):
                raise_bodo_error(
                    f'DataFrame.loc[]: invalid column list {col_idx_list}; not all in dataframe columns {df.columns}'
                    )
            return gen_df_loc_col_select_impl(df, col_idx_list)
    raise_bodo_error(
        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
        )


def gen_df_loc_col_select_impl(df, col_idx_list):
    col_names = []
    ymcli__tzbmm = []
    if len(col_idx_list) > 0 and isinstance(col_idx_list[0], (bool, np.bool_)):
        for gsyk__ywqh, skgwi__vyib in enumerate(col_idx_list):
            if skgwi__vyib:
                ymcli__tzbmm.append(gsyk__ywqh)
                col_names.append(df.columns[gsyk__ywqh])
    else:
        col_names = col_idx_list
        ymcli__tzbmm = [df.column_index[rqq__suyxn] for rqq__suyxn in
            col_idx_list]
    reex__xukx = None
    if df.is_table_format and len(col_idx_list) > 0 and len(col_idx_list
        ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD:
        reex__xukx = {'col_nums_meta': bodo.utils.typing.MetaType(tuple(
            ymcli__tzbmm))}
        lhto__jxk = (
            f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, False)[idx[0]]'
            )
    else:
        lhto__jxk = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {ind})[idx[0]]'
             for ind in ymcli__tzbmm)
    hxu__pezd = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx[0]]')
    lkm__yckrp = 'def impl(I, idx):\n'
    lkm__yckrp += '  df = I._obj\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(lkm__yckrp, col_names,
        lhto__jxk, hxu__pezd, extra_globals=reex__xukx)


@overload(operator.setitem, no_unliteral=True)
def df_loc_setitem_overload(df, idx, val):
    if not isinstance(df, DataFrameLocType):
        return
    raise_bodo_error(
        f'DataFrame.loc setitem unsupported for dataframe {df.df_type}, index {idx}, value {val}'
        )


class DataFrameIatType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        hzs__rbu = 'DataFrameIatType({})'.format(df_type)
        super(DataFrameIatType, self).__init__(hzs__rbu)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameIatType)
class DataFrameIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        htsqv__sjlr = [('obj', fe_type.df_type)]
        super(DataFrameIatModel, self).__init__(dmm, fe_type, htsqv__sjlr)


make_attribute_wrapper(DataFrameIatType, 'obj', '_obj')


@intrinsic
def init_dataframe_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        oqmjz__shrpe, = args
        obsv__jxx = signature.return_type
        gma__aqra = cgutils.create_struct_proxy(obsv__jxx)(context, builder)
        gma__aqra.obj = oqmjz__shrpe
        context.nrt.incref(builder, signature.args[0], oqmjz__shrpe)
        return gma__aqra._getvalue()
    return DataFrameIatType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'iat')
def overload_dataframe_iat(df):
    check_runtime_cols_unsupported(df, 'DataFrame.iat')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_iat(df)


@overload(operator.getitem, no_unliteral=True)
def overload_iat_getitem(I, idx):
    if not isinstance(I, DataFrameIatType):
        return
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        if not isinstance(idx.types[0], types.Integer):
            raise BodoError(
                'DataFrame.iat: iAt based indexing can only have integer indexers'
                )
        if not is_overload_constant_int(idx.types[1]):
            raise_bodo_error(
                'DataFrame.iat getitem: column index must be a constant integer. For more informaton, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        uhh__llr = get_overload_const_int(idx.types[1])

        def impl_col_ind(I, idx):
            df = I._obj
            mfmgj__cgttn = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df
                , uhh__llr)
            return bodo.utils.conversion.box_if_dt64(mfmgj__cgttn[idx[0]])
        return impl_col_ind
    raise BodoError('df.iat[] getitem using {} not supported'.format(idx))


@overload(operator.setitem, no_unliteral=True)
def overload_iat_setitem(I, idx, val):
    if not isinstance(I, DataFrameIatType):
        return
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        if not isinstance(idx.types[0], types.Integer):
            raise BodoError(
                'DataFrame.iat: iAt based indexing can only have integer indexers'
                )
        if not is_overload_constant_int(idx.types[1]):
            raise_bodo_error(
                'DataFrame.iat setitem: column index must be a constant integer. For more informaton, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        uhh__llr = get_overload_const_int(idx.types[1])
        if is_immutable_array(I.df_type.data[uhh__llr]):
            raise BodoError(
                f'DataFrame setitem not supported for column with immutable array type {I.df_type.data}'
                )

        def impl_col_ind(I, idx, val):
            df = I._obj
            mfmgj__cgttn = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df
                , uhh__llr)
            mfmgj__cgttn[idx[0]] = bodo.utils.conversion.unbox_if_timestamp(val
                )
        return impl_col_ind
    raise BodoError('df.iat[] setitem using {} not supported'.format(idx))


@lower_cast(DataFrameIatType, DataFrameIatType)
@lower_cast(DataFrameILocType, DataFrameILocType)
@lower_cast(DataFrameLocType, DataFrameLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    gma__aqra = cgutils.create_struct_proxy(fromty)(context, builder, val)
    duyyo__hhdym = context.cast(builder, gma__aqra.obj, fromty.df_type,
        toty.df_type)
    hxd__pmh = cgutils.create_struct_proxy(toty)(context, builder)
    hxd__pmh.obj = duyyo__hhdym
    return hxd__pmh._getvalue()
