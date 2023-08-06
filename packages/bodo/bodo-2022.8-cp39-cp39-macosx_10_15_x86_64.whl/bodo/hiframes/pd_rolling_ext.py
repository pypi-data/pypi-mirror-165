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
            ivpq__enp = 'Series'
        else:
            ivpq__enp = 'DataFrame'
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(obj_type,
            f'{ivpq__enp}.rolling()')
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
        idiox__hzj = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, idiox__hzj)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    check_runtime_cols_unsupported(df, 'DataFrame.rolling()')
    wfzmk__zywz = dict(win_type=win_type, axis=axis, closed=closed)
    lfk__fwl = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', wfzmk__zywz, lfk__fwl,
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
    wfzmk__zywz = dict(win_type=win_type, axis=axis, closed=closed)
    lfk__fwl = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', wfzmk__zywz, lfk__fwl,
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
        rngeq__qbau, nzkd__kwnj, dzjom__rvywl, foa__ulji, opvf__keim = args
        glbl__qtxue = signature.return_type
        darvl__yzghg = cgutils.create_struct_proxy(glbl__qtxue)(context,
            builder)
        darvl__yzghg.obj = rngeq__qbau
        darvl__yzghg.window = nzkd__kwnj
        darvl__yzghg.min_periods = dzjom__rvywl
        darvl__yzghg.center = foa__ulji
        context.nrt.incref(builder, signature.args[0], rngeq__qbau)
        context.nrt.incref(builder, signature.args[1], nzkd__kwnj)
        context.nrt.incref(builder, signature.args[2], dzjom__rvywl)
        context.nrt.incref(builder, signature.args[3], foa__ulji)
        return darvl__yzghg._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    glbl__qtxue = RollingType(obj_type, window_type, on, selection, False)
    return glbl__qtxue(obj_type, window_type, min_periods_type, center_type,
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
    rsr__iezfg = not isinstance(rolling.window_type, types.Integer)
    zzyl__ogydj = 'variable' if rsr__iezfg else 'fixed'
    xphrv__kncst = 'None'
    if rsr__iezfg:
        xphrv__kncst = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    azci__gip = []
    ofk__shh = 'on_arr, ' if rsr__iezfg else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{zzyl__ogydj}(bodo.hiframes.pd_series_ext.get_series_data(df), {ofk__shh}index_arr, window, minp, center, func, raw)'
            , xphrv__kncst, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    uggd__brt = rolling.obj_type.data
    out_cols = []
    for jivx__gex in rolling.selection:
        ytb__crpfx = rolling.obj_type.columns.index(jivx__gex)
        if jivx__gex == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            ibwww__cviey = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {ytb__crpfx})'
                )
            out_cols.append(jivx__gex)
        else:
            if not isinstance(uggd__brt[ytb__crpfx].dtype, (types.Boolean,
                types.Number)):
                continue
            ibwww__cviey = (
                f'bodo.hiframes.rolling.rolling_{zzyl__ogydj}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {ytb__crpfx}), {ofk__shh}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(jivx__gex)
        azci__gip.append(ibwww__cviey)
    return ', '.join(azci__gip), xphrv__kncst, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    wfzmk__zywz = dict(engine=engine, engine_kwargs=engine_kwargs, args=
        args, kwargs=kwargs)
    lfk__fwl = dict(engine=None, engine_kwargs=None, args=None, kwargs=None)
    check_unsupported_args('Rolling.apply', wfzmk__zywz, lfk__fwl,
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
    wfzmk__zywz = dict(win_type=win_type, axis=axis, closed=closed, method=
        method)
    lfk__fwl = dict(win_type=None, axis=0, closed=None, method='single')
    check_unsupported_args('GroupBy.rolling', wfzmk__zywz, lfk__fwl,
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
        gkh__htlt = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        htub__xtjih = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{kjb__moh}'" if
                isinstance(kjb__moh, str) else f'{kjb__moh}' for kjb__moh in
                rolling.selection if kjb__moh != rolling.on))
        oper__zdi = hua__xgq = ''
        if fname == 'apply':
            oper__zdi = 'func, raw, args, kwargs'
            hua__xgq = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            oper__zdi = hua__xgq = 'other, pairwise'
        if fname == 'cov':
            oper__zdi = hua__xgq = 'other, pairwise, ddof'
        xemum__iljrm = (
            f'lambda df, window, minp, center, {oper__zdi}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {htub__xtjih}){selection}.{fname}({hua__xgq})'
            )
        gkh__htlt += f"""  return rolling.obj.apply({xemum__iljrm}, rolling.window, rolling.min_periods, rolling.center, {oper__zdi})
"""
        whh__rkxed = {}
        exec(gkh__htlt, {'bodo': bodo}, whh__rkxed)
        impl = whh__rkxed['impl']
        return impl
    dbil__vnwy = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if dbil__vnwy else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if dbil__vnwy else rolling.obj_type.columns
        other_cols = None if dbil__vnwy else other.columns
        azci__gip, xphrv__kncst = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        azci__gip, xphrv__kncst, out_cols = _gen_df_rolling_out_data(rolling)
    jslp__obl = dbil__vnwy or len(rolling.selection) == (1 if rolling.on is
        None else 2) and rolling.series_select
    zdzf__rhh = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    zdzf__rhh += '  df = rolling.obj\n'
    zdzf__rhh += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if dbil__vnwy else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    ivpq__enp = 'None'
    if dbil__vnwy:
        ivpq__enp = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif jslp__obl:
        jivx__gex = (set(out_cols) - set([rolling.on])).pop()
        ivpq__enp = f"'{jivx__gex}'" if isinstance(jivx__gex, str) else str(
            jivx__gex)
    zdzf__rhh += f'  name = {ivpq__enp}\n'
    zdzf__rhh += '  window = rolling.window\n'
    zdzf__rhh += '  center = rolling.center\n'
    zdzf__rhh += '  minp = rolling.min_periods\n'
    zdzf__rhh += f'  on_arr = {xphrv__kncst}\n'
    if fname == 'apply':
        zdzf__rhh += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        zdzf__rhh += f"  func = '{fname}'\n"
        zdzf__rhh += f'  index_arr = None\n'
        zdzf__rhh += f'  raw = False\n'
    if jslp__obl:
        zdzf__rhh += (
            f'  return bodo.hiframes.pd_series_ext.init_series({azci__gip}, index, name)'
            )
        whh__rkxed = {}
        juf__yxvud = {'bodo': bodo}
        exec(zdzf__rhh, juf__yxvud, whh__rkxed)
        impl = whh__rkxed['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(zdzf__rhh, out_cols,
        azci__gip)


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
        miyg__ice = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(miyg__ice)


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
    qvxjd__ztzkq = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(qvxjd__ztzkq) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    rsr__iezfg = not isinstance(window_type, types.Integer)
    xphrv__kncst = 'None'
    if rsr__iezfg:
        xphrv__kncst = 'bodo.utils.conversion.index_to_array(index)'
    ofk__shh = 'on_arr, ' if rsr__iezfg else ''
    azci__gip = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {ofk__shh}window, minp, center)'
            , xphrv__kncst)
    for jivx__gex in out_cols:
        if jivx__gex in df_cols and jivx__gex in other_cols:
            rwzi__svw = df_cols.index(jivx__gex)
            qlp__xcxbd = other_cols.index(jivx__gex)
            ibwww__cviey = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rwzi__svw}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {qlp__xcxbd}), {ofk__shh}window, minp, center)'
                )
        else:
            ibwww__cviey = 'np.full(len(df), np.nan)'
        azci__gip.append(ibwww__cviey)
    return ', '.join(azci__gip), xphrv__kncst


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None, ddof=1):
    uyoej__dzxcz = {'pairwise': pairwise, 'ddof': ddof}
    bqxxy__zqu = {'pairwise': None, 'ddof': 1}
    check_unsupported_args('pandas.core.window.rolling.Rolling.corr',
        uyoej__dzxcz, bqxxy__zqu, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    uyoej__dzxcz = {'ddof': ddof, 'pairwise': pairwise}
    bqxxy__zqu = {'ddof': 1, 'pairwise': None}
    check_unsupported_args('pandas.core.window.rolling.Rolling.cov',
        uyoej__dzxcz, bqxxy__zqu, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, sezk__exfr = args
        if isinstance(rolling, RollingType):
            qvxjd__ztzkq = rolling.obj_type.selection if isinstance(rolling
                .obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(sezk__exfr, (tuple, list)):
                if len(set(sezk__exfr).difference(set(qvxjd__ztzkq))) > 0:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(sezk__exfr).difference(set(qvxjd__ztzkq))))
                selection = list(sezk__exfr)
            else:
                if sezk__exfr not in qvxjd__ztzkq:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(sezk__exfr))
                selection = [sezk__exfr]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            lldv__eku = RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, tuple(selection), True, series_select)
            return signature(lldv__eku, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        qvxjd__ztzkq = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            qvxjd__ztzkq = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            qvxjd__ztzkq = rolling.obj_type.columns
        if attr in qvxjd__ztzkq:
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
    bnnre__kfu = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    uggd__brt = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in bnnre__kfu):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        wutnn__gyegq = uggd__brt[bnnre__kfu.index(get_literal_value(on))]
        if not isinstance(wutnn__gyegq, types.Array
            ) or wutnn__gyegq.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(azc__oxscq.dtype, (types.Boolean, types.Number)) for
        azc__oxscq in uggd__brt):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
