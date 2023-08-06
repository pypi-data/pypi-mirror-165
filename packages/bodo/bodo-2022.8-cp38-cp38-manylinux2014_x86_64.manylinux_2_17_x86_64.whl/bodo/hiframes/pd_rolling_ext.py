"""typing for rolling window functions
"""
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, signature
from numba.extending import infer, infer_getattr, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_method, register_model
import bodo
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_type, pd_timedelta_type
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported
from bodo.hiframes.pd_groupby_ext import DataFrameGroupByType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.rolling import supported_rolling_funcs, unsupported_rolling_methods
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, get_literal_value, is_const_func_type, is_literal_type, is_overload_bool, is_overload_constant_str, is_overload_int, is_overload_none, raise_bodo_error


class RollingType(types.Type):

    def __init__(self, obj_type, window_type, on, selection,
        explicit_select=False, series_select=False):
        if isinstance(obj_type, bodo.SeriesType):
            yxy__cin = 'Series'
        else:
            yxy__cin = 'DataFrame'
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(obj_type,
            f'{yxy__cin}.rolling()')
        self.obj_type = obj_type
        self.window_type = window_type
        self.on = on
        self.selection = selection
        self.explicit_select = explicit_select
        self.series_select = series_select
        super(RollingType, self).__init__(name=
            f'RollingType({obj_type}, {window_type}, {on}, {selection}, {explicit_select}, {series_select})'
            )

    def copy(self):
        return RollingType(self.obj_type, self.window_type, self.on, self.
            selection, self.explicit_select, self.series_select)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(RollingType)
class RollingModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ydc__rwb = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, ydc__rwb)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    check_runtime_cols_unsupported(df, 'DataFrame.rolling()')
    xmy__xvn = dict(win_type=win_type, axis=axis, closed=closed)
    opfa__xseo = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', xmy__xvn, opfa__xseo,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(df, window, min_periods, center, on)

    def impl(df, window, min_periods=None, center=False, win_type=None, on=
        None, axis=0, closed=None):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(df, window,
            min_periods, center, on)
    return impl


@overload_method(SeriesType, 'rolling', inline='always', no_unliteral=True)
def overload_series_rolling(S, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    xmy__xvn = dict(win_type=win_type, axis=axis, closed=closed)
    opfa__xseo = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', xmy__xvn, opfa__xseo,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(S, window, min_periods, center, on)

    def impl(S, window, min_periods=None, center=False, win_type=None, on=
        None, axis=0, closed=None):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(S, window,
            min_periods, center, on)
    return impl


@intrinsic
def init_rolling(typingctx, obj_type, window_type, min_periods_type,
    center_type, on_type=None):

    def codegen(context, builder, signature, args):
        qjpvb__ucozb, hqh__sgr, dthxa__fip, dqezi__wqafw, bbixi__zjt = args
        wjpvi__tbyr = signature.return_type
        rjks__ibixf = cgutils.create_struct_proxy(wjpvi__tbyr)(context, builder
            )
        rjks__ibixf.obj = qjpvb__ucozb
        rjks__ibixf.window = hqh__sgr
        rjks__ibixf.min_periods = dthxa__fip
        rjks__ibixf.center = dqezi__wqafw
        context.nrt.incref(builder, signature.args[0], qjpvb__ucozb)
        context.nrt.incref(builder, signature.args[1], hqh__sgr)
        context.nrt.incref(builder, signature.args[2], dthxa__fip)
        context.nrt.incref(builder, signature.args[3], dqezi__wqafw)
        return rjks__ibixf._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    wjpvi__tbyr = RollingType(obj_type, window_type, on, selection, False)
    return wjpvi__tbyr(obj_type, window_type, min_periods_type, center_type,
        on_type), codegen


def _handle_default_min_periods(min_periods, window):
    return min_periods


@overload(_handle_default_min_periods)
def overload_handle_default_min_periods(min_periods, window):
    if is_overload_none(min_periods):
        if isinstance(window, types.Integer):
            return lambda min_periods, window: window
        else:
            return lambda min_periods, window: 1
    else:
        return lambda min_periods, window: min_periods


def _gen_df_rolling_out_data(rolling):
    vlqi__tqlr = not isinstance(rolling.window_type, types.Integer)
    mqpjz__jes = 'variable' if vlqi__tqlr else 'fixed'
    kogw__ttj = 'None'
    if vlqi__tqlr:
        kogw__ttj = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    fitnb__fibc = []
    grp__damn = 'on_arr, ' if vlqi__tqlr else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{mqpjz__jes}(bodo.hiframes.pd_series_ext.get_series_data(df), {grp__damn}index_arr, window, minp, center, func, raw)'
            , kogw__ttj, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    grzut__snyo = rolling.obj_type.data
    out_cols = []
    for aoftc__aqie in rolling.selection:
        bgf__hae = rolling.obj_type.columns.index(aoftc__aqie)
        if aoftc__aqie == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            icg__dsvti = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {bgf__hae})'
                )
            out_cols.append(aoftc__aqie)
        else:
            if not isinstance(grzut__snyo[bgf__hae].dtype, (types.Boolean,
                types.Number)):
                continue
            icg__dsvti = (
                f'bodo.hiframes.rolling.rolling_{mqpjz__jes}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {bgf__hae}), {grp__damn}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(aoftc__aqie)
        fitnb__fibc.append(icg__dsvti)
    return ', '.join(fitnb__fibc), kogw__ttj, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    xmy__xvn = dict(engine=engine, engine_kwargs=engine_kwargs, args=args,
        kwargs=kwargs)
    opfa__xseo = dict(engine=None, engine_kwargs=None, args=None, kwargs=None)
    check_unsupported_args('Rolling.apply', xmy__xvn, opfa__xseo,
        package_name='pandas', module_name='Window')
    if not is_const_func_type(func):
        raise BodoError(
            f"Rolling.apply(): 'func' parameter must be a function, not {func} (builtin functions not supported yet)."
            )
    if not is_overload_bool(raw):
        raise BodoError(
            f"Rolling.apply(): 'raw' parameter must be bool, not {raw}.")
    return _gen_rolling_impl(rolling, 'apply')


@overload_method(DataFrameGroupByType, 'rolling', inline='always',
    no_unliteral=True)
def groupby_rolling_overload(grp, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None, method='single'):
    xmy__xvn = dict(win_type=win_type, axis=axis, closed=closed, method=method)
    opfa__xseo = dict(win_type=None, axis=0, closed=None, method='single')
    check_unsupported_args('GroupBy.rolling', xmy__xvn, opfa__xseo,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(grp, window, min_periods, center, on)

    def _impl(grp, window, min_periods=None, center=False, win_type=None,
        on=None, axis=0, closed=None, method='single'):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(grp, window,
            min_periods, center, on)
    return _impl


def _gen_rolling_impl(rolling, fname, other=None):
    if isinstance(rolling.obj_type, DataFrameGroupByType):
        sir__ljxcy = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        guked__vlhmk = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{aac__zmkzb}'" if
                isinstance(aac__zmkzb, str) else f'{aac__zmkzb}' for
                aac__zmkzb in rolling.selection if aac__zmkzb != rolling.on))
        nsqz__zegh = bgol__rge = ''
        if fname == 'apply':
            nsqz__zegh = 'func, raw, args, kwargs'
            bgol__rge = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            nsqz__zegh = bgol__rge = 'other, pairwise'
        if fname == 'cov':
            nsqz__zegh = bgol__rge = 'other, pairwise, ddof'
        wniyb__damfs = (
            f'lambda df, window, minp, center, {nsqz__zegh}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {guked__vlhmk}){selection}.{fname}({bgol__rge})'
            )
        sir__ljxcy += f"""  return rolling.obj.apply({wniyb__damfs}, rolling.window, rolling.min_periods, rolling.center, {nsqz__zegh})
"""
        kvt__nnbiz = {}
        exec(sir__ljxcy, {'bodo': bodo}, kvt__nnbiz)
        impl = kvt__nnbiz['impl']
        return impl
    nqnh__uxab = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if nqnh__uxab else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if nqnh__uxab else rolling.obj_type.columns
        other_cols = None if nqnh__uxab else other.columns
        fitnb__fibc, kogw__ttj = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        fitnb__fibc, kogw__ttj, out_cols = _gen_df_rolling_out_data(rolling)
    pudrx__jgxv = nqnh__uxab or len(rolling.selection) == (1 if rolling.on is
        None else 2) and rolling.series_select
    bng__wuvl = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    bng__wuvl += '  df = rolling.obj\n'
    bng__wuvl += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if nqnh__uxab else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    yxy__cin = 'None'
    if nqnh__uxab:
        yxy__cin = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif pudrx__jgxv:
        aoftc__aqie = (set(out_cols) - set([rolling.on])).pop()
        yxy__cin = f"'{aoftc__aqie}'" if isinstance(aoftc__aqie, str) else str(
            aoftc__aqie)
    bng__wuvl += f'  name = {yxy__cin}\n'
    bng__wuvl += '  window = rolling.window\n'
    bng__wuvl += '  center = rolling.center\n'
    bng__wuvl += '  minp = rolling.min_periods\n'
    bng__wuvl += f'  on_arr = {kogw__ttj}\n'
    if fname == 'apply':
        bng__wuvl += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        bng__wuvl += f"  func = '{fname}'\n"
        bng__wuvl += f'  index_arr = None\n'
        bng__wuvl += f'  raw = False\n'
    if pudrx__jgxv:
        bng__wuvl += (
            f'  return bodo.hiframes.pd_series_ext.init_series({fitnb__fibc}, index, name)'
            )
        kvt__nnbiz = {}
        rbl__dpbp = {'bodo': bodo}
        exec(bng__wuvl, rbl__dpbp, kvt__nnbiz)
        impl = kvt__nnbiz['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(bng__wuvl, out_cols,
        fitnb__fibc)


def _get_rolling_func_args(fname):
    if fname == 'apply':
        return (
            'func, raw=False, engine=None, engine_kwargs=None, args=None, kwargs=None\n'
            )
    elif fname == 'corr':
        return 'other=None, pairwise=None, ddof=1\n'
    elif fname == 'cov':
        return 'other=None, pairwise=None, ddof=1\n'
    return ''


def create_rolling_overload(fname):

    def overload_rolling_func(rolling):
        return _gen_rolling_impl(rolling, fname)
    return overload_rolling_func


def _install_rolling_methods():
    for fname in supported_rolling_funcs:
        if fname in ('apply', 'corr', 'cov'):
            continue
        tdzty__pxa = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(tdzty__pxa)


def _install_rolling_unsupported_methods():
    for fname in unsupported_rolling_methods:
        overload_method(RollingType, fname, no_unliteral=True)(
            create_unsupported_overload(
            f'pandas.core.window.rolling.Rolling.{fname}()'))


_install_rolling_methods()
_install_rolling_unsupported_methods()


def _get_corr_cov_out_cols(rolling, other, func_name):
    if not isinstance(other, DataFrameType):
        raise_bodo_error(
            f"DataFrame.rolling.{func_name}(): requires providing a DataFrame for 'other'"
            )
    livpt__btlvj = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(livpt__btlvj) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    vlqi__tqlr = not isinstance(window_type, types.Integer)
    kogw__ttj = 'None'
    if vlqi__tqlr:
        kogw__ttj = 'bodo.utils.conversion.index_to_array(index)'
    grp__damn = 'on_arr, ' if vlqi__tqlr else ''
    fitnb__fibc = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {grp__damn}window, minp, center)'
            , kogw__ttj)
    for aoftc__aqie in out_cols:
        if aoftc__aqie in df_cols and aoftc__aqie in other_cols:
            urwg__fju = df_cols.index(aoftc__aqie)
            stasw__demo = other_cols.index(aoftc__aqie)
            icg__dsvti = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {urwg__fju}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {stasw__demo}), {grp__damn}window, minp, center)'
                )
        else:
            icg__dsvti = 'np.full(len(df), np.nan)'
        fitnb__fibc.append(icg__dsvti)
    return ', '.join(fitnb__fibc), kogw__ttj


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None, ddof=1):
    pfpu__qka = {'pairwise': pairwise, 'ddof': ddof}
    phtfv__wxu = {'pairwise': None, 'ddof': 1}
    check_unsupported_args('pandas.core.window.rolling.Rolling.corr',
        pfpu__qka, phtfv__wxu, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    pfpu__qka = {'ddof': ddof, 'pairwise': pairwise}
    phtfv__wxu = {'ddof': 1, 'pairwise': None}
    check_unsupported_args('pandas.core.window.rolling.Rolling.cov',
        pfpu__qka, phtfv__wxu, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, ivgn__uyw = args
        if isinstance(rolling, RollingType):
            livpt__btlvj = rolling.obj_type.selection if isinstance(rolling
                .obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(ivgn__uyw, (tuple, list)):
                if len(set(ivgn__uyw).difference(set(livpt__btlvj))) > 0:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(ivgn__uyw).difference(set(livpt__btlvj))))
                selection = list(ivgn__uyw)
            else:
                if ivgn__uyw not in livpt__btlvj:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(ivgn__uyw))
                selection = [ivgn__uyw]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            nos__axf = RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, tuple(selection), True, series_select)
            return signature(nos__axf, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        livpt__btlvj = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            livpt__btlvj = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            livpt__btlvj = rolling.obj_type.columns
        if attr in livpt__btlvj:
            return RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, (attr,) if rolling.on is None else (attr,
                rolling.on), True, True)


def _validate_rolling_args(obj, window, min_periods, center, on):
    assert isinstance(obj, (SeriesType, DataFrameType, DataFrameGroupByType)
        ), 'invalid rolling obj'
    func_name = 'Series' if isinstance(obj, SeriesType
        ) else 'DataFrame' if isinstance(obj, DataFrameType
        ) else 'DataFrameGroupBy'
    if not (is_overload_int(window) or is_overload_constant_str(window) or 
        window == bodo.string_type or window in (pd_timedelta_type,
        datetime_timedelta_type)):
        raise BodoError(
            f"{func_name}.rolling(): 'window' should be int or time offset (str, pd.Timedelta, datetime.timedelta), not {window}"
            )
    if not is_overload_bool(center):
        raise BodoError(
            f'{func_name}.rolling(): center must be a boolean, not {center}')
    if not (is_overload_none(min_periods) or isinstance(min_periods, types.
        Integer)):
        raise BodoError(
            f'{func_name}.rolling(): min_periods must be an integer, not {min_periods}'
            )
    if isinstance(obj, SeriesType) and not is_overload_none(on):
        raise BodoError(
            f"{func_name}.rolling(): 'on' not supported for Series yet (can use a DataFrame instead)."
            )
    gbmx__wlqjh = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    grzut__snyo = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in gbmx__wlqjh):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        omh__sedlb = grzut__snyo[gbmx__wlqjh.index(get_literal_value(on))]
        if not isinstance(omh__sedlb, types.Array
            ) or omh__sedlb.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(wqwt__jwr.dtype, (types.Boolean, types.Number)) for
        wqwt__jwr in grzut__snyo):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
