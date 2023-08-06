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
            ntivm__vpxzv = idx
            eap__bucf = df.data
            nrvam__yluq = df.columns
            qzws__wlb = self.replace_range_with_numeric_idx_if_needed(df,
                ntivm__vpxzv)
            lfe__qbq = DataFrameType(eap__bucf, qzws__wlb, nrvam__yluq,
                is_table_format=df.is_table_format)
            return lfe__qbq(*args)
        if isinstance(idx, types.BaseTuple) and len(idx) == 2:
            mfs__jtizg = idx.types[0]
            dvvd__xgqiw = idx.types[1]
            if isinstance(mfs__jtizg, types.Integer):
                if not isinstance(df.index, bodo.hiframes.pd_index_ext.
                    RangeIndexType):
                    raise_bodo_error(
                        'Dataframe.loc[int, col_ind] getitem only supported for dataframes with RangeIndexes'
                        )
                if is_overload_constant_str(dvvd__xgqiw):
                    wkq__ohran = get_overload_const_str(dvvd__xgqiw)
                    if wkq__ohran not in df.columns:
                        raise_bodo_error(
                            'dataframe {} does not include column {}'.
                            format(df, wkq__ohran))
                    jkhig__jpfrf = df.columns.index(wkq__ohran)
                    return df.data[jkhig__jpfrf].dtype(*args)
                if isinstance(dvvd__xgqiw, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                else:
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
                        )
            if is_list_like_index_type(mfs__jtizg
                ) and mfs__jtizg.dtype == types.bool_ or isinstance(mfs__jtizg,
                types.SliceType):
                qzws__wlb = self.replace_range_with_numeric_idx_if_needed(df,
                    mfs__jtizg)
                if is_overload_constant_str(dvvd__xgqiw):
                    lfzqd__gdyh = get_overload_const_str(dvvd__xgqiw)
                    if lfzqd__gdyh not in df.columns:
                        raise_bodo_error(
                            f'dataframe {df} does not include column {lfzqd__gdyh}'
                            )
                    jkhig__jpfrf = df.columns.index(lfzqd__gdyh)
                    tckz__hsias = df.data[jkhig__jpfrf]
                    ityie__dbv = tckz__hsias.dtype
                    bra__ftesh = types.literal(df.columns[jkhig__jpfrf])
                    lfe__qbq = bodo.SeriesType(ityie__dbv, tckz__hsias,
                        qzws__wlb, bra__ftesh)
                    return lfe__qbq(*args)
                if isinstance(dvvd__xgqiw, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                elif is_overload_constant_list(dvvd__xgqiw):
                    ktx__zmn = get_overload_const_list(dvvd__xgqiw)
                    wecy__juddx = types.unliteral(dvvd__xgqiw)
                    if wecy__juddx.dtype == types.bool_:
                        if len(df.columns) != len(ktx__zmn):
                            raise_bodo_error(
                                f'dataframe {df} has {len(df.columns)} columns, but boolean array used with DataFrame.loc[] {ktx__zmn} has {len(ktx__zmn)} values'
                                )
                        tqf__ckv = []
                        gybo__fhp = []
                        for zxa__mff in range(len(ktx__zmn)):
                            if ktx__zmn[zxa__mff]:
                                tqf__ckv.append(df.columns[zxa__mff])
                                gybo__fhp.append(df.data[zxa__mff])
                        uwq__ooe = tuple()
                        nvp__hivkw = df.is_table_format and len(tqf__ckv
                            ) > 0 and len(tqf__ckv
                            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
                        lfe__qbq = DataFrameType(tuple(gybo__fhp),
                            qzws__wlb, tuple(tqf__ckv), is_table_format=
                            nvp__hivkw)
                        return lfe__qbq(*args)
                    elif wecy__juddx.dtype == bodo.string_type:
                        uwq__ooe, gybo__fhp = (
                            get_df_getitem_kept_cols_and_data(df, ktx__zmn))
                        nvp__hivkw = df.is_table_format and len(ktx__zmn
                            ) > 0 and len(ktx__zmn
                            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
                        lfe__qbq = DataFrameType(gybo__fhp, qzws__wlb,
                            uwq__ooe, is_table_format=nvp__hivkw)
                        return lfe__qbq(*args)
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
                tqf__ckv = []
                gybo__fhp = []
                for zxa__mff, ducmp__itff in enumerate(df.columns):
                    if ducmp__itff[0] != ind_val:
                        continue
                    tqf__ckv.append(ducmp__itff[1] if len(ducmp__itff) == 2
                         else ducmp__itff[1:])
                    gybo__fhp.append(df.data[zxa__mff])
                tckz__hsias = tuple(gybo__fhp)
                pvtt__gts = df.index
                hms__whw = tuple(tqf__ckv)
                lfe__qbq = DataFrameType(tckz__hsias, pvtt__gts, hms__whw)
                return lfe__qbq(*args)
            else:
                if ind_val not in df.columns:
                    raise_bodo_error('dataframe {} does not include column {}'
                        .format(df, ind_val))
                jkhig__jpfrf = df.columns.index(ind_val)
                tckz__hsias = df.data[jkhig__jpfrf]
                ityie__dbv = tckz__hsias.dtype
                pvtt__gts = df.index
                bra__ftesh = types.literal(df.columns[jkhig__jpfrf])
                lfe__qbq = bodo.SeriesType(ityie__dbv, tckz__hsias,
                    pvtt__gts, bra__ftesh)
                return lfe__qbq(*args)
        if isinstance(ind, types.Integer) or isinstance(ind, types.UnicodeType
            ):
            raise_bodo_error(
                'df[] getitem selecting a subset of columns requires providing constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        if is_list_like_index_type(ind
            ) and ind.dtype == types.bool_ or isinstance(ind, types.SliceType):
            tckz__hsias = df.data
            pvtt__gts = self.replace_range_with_numeric_idx_if_needed(df, ind)
            hms__whw = df.columns
            lfe__qbq = DataFrameType(tckz__hsias, pvtt__gts, hms__whw,
                is_table_format=df.is_table_format)
            return lfe__qbq(*args)
        elif is_overload_constant_list(ind):
            cpt__epyq = get_overload_const_list(ind)
            hms__whw, tckz__hsias = get_df_getitem_kept_cols_and_data(df,
                cpt__epyq)
            pvtt__gts = df.index
            nvp__hivkw = df.is_table_format and len(cpt__epyq) > 0 and len(
                cpt__epyq) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
            lfe__qbq = DataFrameType(tckz__hsias, pvtt__gts, hms__whw,
                is_table_format=nvp__hivkw)
            return lfe__qbq(*args)
        raise_bodo_error(
            f'df[] getitem using {ind} not supported. If you are trying to select a subset of the columns, you must provide the column names you are selecting as a constant. See https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )

    def replace_range_with_numeric_idx_if_needed(self, df, ind):
        qzws__wlb = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64,
            df.index.name_typ) if not isinstance(ind, types.SliceType
            ) and isinstance(df.index, bodo.hiframes.pd_index_ext.
            RangeIndexType) else df.index
        return qzws__wlb


DataFrameGetItemTemplate._no_unliteral = True


def get_df_getitem_kept_cols_and_data(df, cols_to_keep_list):
    for ixry__mls in cols_to_keep_list:
        if ixry__mls not in df.column_index:
            raise_bodo_error('Column {} not found in dataframe columns {}'.
                format(ixry__mls, df.columns))
    hms__whw = tuple(cols_to_keep_list)
    tckz__hsias = tuple(df.data[df.column_index[hqath__ltb]] for hqath__ltb in
        hms__whw)
    return hms__whw, tckz__hsias


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
            tqf__ckv = []
            gybo__fhp = []
            for zxa__mff, ducmp__itff in enumerate(df.columns):
                if ducmp__itff[0] != ind_val:
                    continue
                tqf__ckv.append(ducmp__itff[1] if len(ducmp__itff) == 2 else
                    ducmp__itff[1:])
                gybo__fhp.append(
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'
                    .format(zxa__mff))
            hgtq__htpcx = 'def impl(df, ind):\n'
            pucps__alo = (
                'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
            return bodo.hiframes.dataframe_impl._gen_init_df(hgtq__htpcx,
                tqf__ckv, ', '.join(gybo__fhp), pucps__alo)
        if ind_val not in df.columns:
            raise_bodo_error('dataframe {} does not include column {}'.
                format(df, ind_val))
        col_no = df.columns.index(ind_val)
        return lambda df, ind: bodo.hiframes.pd_series_ext.init_series(bodo
            .hiframes.pd_dataframe_ext.get_dataframe_data(df, col_no), bodo
            .hiframes.pd_dataframe_ext.get_dataframe_index(df), ind_val)
    if is_overload_constant_list(ind):
        cpt__epyq = get_overload_const_list(ind)
        for ixry__mls in cpt__epyq:
            if ixry__mls not in df.column_index:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(ixry__mls, df.columns))
        xajhe__ixa = None
        if df.is_table_format and len(cpt__epyq) > 0 and len(cpt__epyq
            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD:
            qra__sjqm = [df.column_index[ixry__mls] for ixry__mls in cpt__epyq]
            xajhe__ixa = {'col_nums_meta': bodo.utils.typing.MetaType(tuple
                (qra__sjqm))}
            gybo__fhp = (
                f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, True)'
                )
        else:
            gybo__fhp = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[ixry__mls]}).copy()'
                 for ixry__mls in cpt__epyq)
        hgtq__htpcx = 'def impl(df, ind):\n'
        pucps__alo = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
        return bodo.hiframes.dataframe_impl._gen_init_df(hgtq__htpcx,
            cpt__epyq, gybo__fhp, pucps__alo, extra_globals=xajhe__ixa)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_ or isinstance(
        ind, types.SliceType):
        hgtq__htpcx = 'def impl(df, ind):\n'
        if not isinstance(ind, types.SliceType):
            hgtq__htpcx += (
                '  ind = bodo.utils.conversion.coerce_to_ndarray(ind)\n')
        pucps__alo = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[ind]')
        if df.is_table_format:
            gybo__fhp = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[ind]')
        else:
            gybo__fhp = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[ixry__mls]})[ind]'
                 for ixry__mls in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(hgtq__htpcx, df.
            columns, gybo__fhp, pucps__alo)
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
        hqath__ltb = 'DataFrameILocType({})'.format(df_type)
        super(DataFrameILocType, self).__init__(hqath__ltb)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameILocType)
class DataFrameILocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        fvsy__tdhuz = [('obj', fe_type.df_type)]
        super(DataFrameILocModel, self).__init__(dmm, fe_type, fvsy__tdhuz)


make_attribute_wrapper(DataFrameILocType, 'obj', '_obj')


@intrinsic
def init_dataframe_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        koqfk__whb, = args
        pdxni__aiyal = signature.return_type
        uoqp__uew = cgutils.create_struct_proxy(pdxni__aiyal)(context, builder)
        uoqp__uew.obj = koqfk__whb
        context.nrt.incref(builder, signature.args[0], koqfk__whb)
        return uoqp__uew._getvalue()
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
        qhphl__paatm = len(df.data)
        if is_overload_constant_int(idx.types[1]):
            is_out_series = True
            zpi__otv = get_overload_const_int(idx.types[1])
            if zpi__otv < 0 or zpi__otv >= qhphl__paatm:
                raise BodoError(
                    'df.iloc: column integer must refer to a valid column number'
                    )
            vmt__yzm = [zpi__otv]
        else:
            is_out_series = False
            vmt__yzm = get_overload_const_list(idx.types[1])
            if any(not isinstance(ind, int) or ind < 0 or ind >=
                qhphl__paatm for ind in vmt__yzm):
                raise BodoError(
                    'df.iloc: column list must be integers referring to a valid column number'
                    )
        col_names = tuple(pd.Series(df.columns, dtype=object)[vmt__yzm])
        if isinstance(idx.types[0], types.Integer):
            if isinstance(idx.types[1], types.Integer):
                zpi__otv = vmt__yzm[0]

                def impl(I, idx):
                    df = I._obj
                    return bodo.utils.conversion.box_if_dt64(bodo.hiframes.
                        pd_dataframe_ext.get_dataframe_data(df, zpi__otv)[
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
    hgtq__htpcx = 'def impl(I, idx):\n'
    hgtq__htpcx += '  df = I._obj\n'
    if isinstance(idx_typ, types.SliceType):
        hgtq__htpcx += f'  idx_t = {idx}\n'
    else:
        hgtq__htpcx += (
            f'  idx_t = bodo.utils.conversion.coerce_to_ndarray({idx})\n')
    pucps__alo = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
    xajhe__ixa = None
    if df.is_table_format and not is_out_series:
        qra__sjqm = [df.column_index[ixry__mls] for ixry__mls in col_names]
        xajhe__ixa = {'col_nums_meta': bodo.utils.typing.MetaType(tuple(
            qra__sjqm))}
        gybo__fhp = (
            f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, False)[idx_t]'
            )
    else:
        gybo__fhp = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[ixry__mls]})[idx_t]'
             for ixry__mls in col_names)
    if is_out_series:
        mml__qmts = f"'{col_names[0]}'" if isinstance(col_names[0], str
            ) else f'{col_names[0]}'
        hgtq__htpcx += f"""  return bodo.hiframes.pd_series_ext.init_series({gybo__fhp}, {pucps__alo}, {mml__qmts})
"""
        nuzjd__drhm = {}
        exec(hgtq__htpcx, {'bodo': bodo}, nuzjd__drhm)
        return nuzjd__drhm['impl']
    return bodo.hiframes.dataframe_impl._gen_init_df(hgtq__htpcx, col_names,
        gybo__fhp, pucps__alo, extra_globals=xajhe__ixa)


def _gen_iloc_getitem_row_impl(df, col_names, idx):
    hgtq__htpcx = 'def impl(I, idx):\n'
    hgtq__htpcx += '  df = I._obj\n'
    gru__vdnwm = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[ixry__mls]})[{idx}]'
         for ixry__mls in col_names)
    hgtq__htpcx += f"""  row_idx = bodo.hiframes.pd_index_ext.init_heter_index({gen_const_tup(col_names)}, None)
"""
    hgtq__htpcx += f"""  return bodo.hiframes.pd_series_ext.init_series(({gru__vdnwm},), row_idx, None)
"""
    nuzjd__drhm = {}
    exec(hgtq__htpcx, {'bodo': bodo}, nuzjd__drhm)
    impl = nuzjd__drhm['impl']
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
        hqath__ltb = 'DataFrameLocType({})'.format(df_type)
        super(DataFrameLocType, self).__init__(hqath__ltb)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameLocType)
class DataFrameLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        fvsy__tdhuz = [('obj', fe_type.df_type)]
        super(DataFrameLocModel, self).__init__(dmm, fe_type, fvsy__tdhuz)


make_attribute_wrapper(DataFrameLocType, 'obj', '_obj')


@intrinsic
def init_dataframe_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        koqfk__whb, = args
        efirt__bxob = signature.return_type
        ccyzn__twk = cgutils.create_struct_proxy(efirt__bxob)(context, builder)
        ccyzn__twk.obj = koqfk__whb
        context.nrt.incref(builder, signature.args[0], koqfk__whb)
        return ccyzn__twk._getvalue()
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
        hgtq__htpcx = 'def impl(I, idx):\n'
        hgtq__htpcx += '  df = I._obj\n'
        hgtq__htpcx += (
            '  idx_t = bodo.utils.conversion.coerce_to_ndarray(idx)\n')
        pucps__alo = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
        if df.is_table_format:
            gybo__fhp = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[idx_t]'
                )
        else:
            gybo__fhp = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[ixry__mls]})[idx_t]'
                 for ixry__mls in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(hgtq__htpcx, df.
            columns, gybo__fhp, pucps__alo)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        rysu__cwyjk = idx.types[1]
        if is_overload_constant_str(rysu__cwyjk):
            oxf__qntr = get_overload_const_str(rysu__cwyjk)
            zpi__otv = df.columns.index(oxf__qntr)

            def impl_col_name(I, idx):
                df = I._obj
                pucps__alo = (bodo.hiframes.pd_dataframe_ext.
                    get_dataframe_index(df))
                ffnzg__wghgi = (bodo.hiframes.pd_dataframe_ext.
                    get_dataframe_data(df, zpi__otv))
                return bodo.hiframes.pd_series_ext.init_series(ffnzg__wghgi,
                    pucps__alo, oxf__qntr).loc[idx[0]]
            return impl_col_name
        if is_overload_constant_list(rysu__cwyjk):
            col_idx_list = get_overload_const_list(rysu__cwyjk)
            if len(col_idx_list) > 0 and not isinstance(col_idx_list[0], (
                bool, np.bool_)) and not all(ixry__mls in df.column_index for
                ixry__mls in col_idx_list):
                raise_bodo_error(
                    f'DataFrame.loc[]: invalid column list {col_idx_list}; not all in dataframe columns {df.columns}'
                    )
            return gen_df_loc_col_select_impl(df, col_idx_list)
    raise_bodo_error(
        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
        )


def gen_df_loc_col_select_impl(df, col_idx_list):
    col_names = []
    vmt__yzm = []
    if len(col_idx_list) > 0 and isinstance(col_idx_list[0], (bool, np.bool_)):
        for zxa__mff, qjsf__rscu in enumerate(col_idx_list):
            if qjsf__rscu:
                vmt__yzm.append(zxa__mff)
                col_names.append(df.columns[zxa__mff])
    else:
        col_names = col_idx_list
        vmt__yzm = [df.column_index[ixry__mls] for ixry__mls in col_idx_list]
    xajhe__ixa = None
    if df.is_table_format and len(col_idx_list) > 0 and len(col_idx_list
        ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD:
        xajhe__ixa = {'col_nums_meta': bodo.utils.typing.MetaType(tuple(
            vmt__yzm))}
        gybo__fhp = (
            f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, False)[idx[0]]'
            )
    else:
        gybo__fhp = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {ind})[idx[0]]'
             for ind in vmt__yzm)
    pucps__alo = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx[0]]')
    hgtq__htpcx = 'def impl(I, idx):\n'
    hgtq__htpcx += '  df = I._obj\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(hgtq__htpcx, col_names,
        gybo__fhp, pucps__alo, extra_globals=xajhe__ixa)


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
        hqath__ltb = 'DataFrameIatType({})'.format(df_type)
        super(DataFrameIatType, self).__init__(hqath__ltb)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameIatType)
class DataFrameIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        fvsy__tdhuz = [('obj', fe_type.df_type)]
        super(DataFrameIatModel, self).__init__(dmm, fe_type, fvsy__tdhuz)


make_attribute_wrapper(DataFrameIatType, 'obj', '_obj')


@intrinsic
def init_dataframe_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        koqfk__whb, = args
        olkqk__itgvr = signature.return_type
        hqu__meull = cgutils.create_struct_proxy(olkqk__itgvr)(context, builder
            )
        hqu__meull.obj = koqfk__whb
        context.nrt.incref(builder, signature.args[0], koqfk__whb)
        return hqu__meull._getvalue()
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
        zpi__otv = get_overload_const_int(idx.types[1])

        def impl_col_ind(I, idx):
            df = I._obj
            ffnzg__wghgi = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df
                , zpi__otv)
            return bodo.utils.conversion.box_if_dt64(ffnzg__wghgi[idx[0]])
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
        zpi__otv = get_overload_const_int(idx.types[1])
        if is_immutable_array(I.df_type.data[zpi__otv]):
            raise BodoError(
                f'DataFrame setitem not supported for column with immutable array type {I.df_type.data}'
                )

        def impl_col_ind(I, idx, val):
            df = I._obj
            ffnzg__wghgi = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df
                , zpi__otv)
            ffnzg__wghgi[idx[0]] = bodo.utils.conversion.unbox_if_timestamp(val
                )
        return impl_col_ind
    raise BodoError('df.iat[] setitem using {} not supported'.format(idx))


@lower_cast(DataFrameIatType, DataFrameIatType)
@lower_cast(DataFrameILocType, DataFrameILocType)
@lower_cast(DataFrameLocType, DataFrameLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    hqu__meull = cgutils.create_struct_proxy(fromty)(context, builder, val)
    gece__yfplm = context.cast(builder, hqu__meull.obj, fromty.df_type,
        toty.df_type)
    bdtcm__uhcu = cgutils.create_struct_proxy(toty)(context, builder)
    bdtcm__uhcu.obj = gece__yfplm
    return bdtcm__uhcu._getvalue()
