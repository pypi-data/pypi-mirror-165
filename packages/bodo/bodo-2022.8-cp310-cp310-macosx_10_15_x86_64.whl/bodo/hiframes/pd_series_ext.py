"""
Implement pd.Series typing and data model handling.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import bound_function, signature
from numba.extending import infer_getattr, intrinsic, lower_builtin, lower_cast, models, overload, overload_attribute, overload_method, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.datetime_timedelta_ext import pd_timedelta_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_type
from bodo.io import csv_cpp
from bodo.libs.int_arr_ext import IntDtype
from bodo.libs.pd_datetime_arr_ext import PandasDatetimeTZDtype
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.transform import get_const_func_output_type
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, dtype_to_array_type, get_overload_const_str, get_overload_const_tuple, get_udf_error_msg, get_udf_out_arr_type, is_heterogeneous_tuple_type, is_overload_constant_str, is_overload_constant_tuple, is_overload_false, is_overload_int, is_overload_none, raise_bodo_error, to_nullable_type
_csv_output_is_dir = types.ExternalFunction('csv_output_is_dir', types.int8
    (types.voidptr))
ll.add_symbol('csv_output_is_dir', csv_cpp.csv_output_is_dir)


class SeriesType(types.IterableType, types.ArrayCompatible):
    ndim = 1

    def __init__(self, dtype, data=None, index=None, name_typ=None, dist=None):
        from bodo.hiframes.pd_index_ext import RangeIndexType
        from bodo.transforms.distributed_analysis import Distribution
        data = dtype_to_array_type(dtype) if data is None else data
        dtype = dtype.dtype if isinstance(dtype, IntDtype) else dtype
        self.dtype = dtype
        self.data = data
        name_typ = types.none if name_typ is None else name_typ
        index = RangeIndexType(types.none) if index is None else index
        self.index = index
        self.name_typ = name_typ
        dist = Distribution.OneD_Var if dist is None else dist
        self.dist = dist
        super(SeriesType, self).__init__(name=
            f'series({dtype}, {data}, {index}, {name_typ}, {dist})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self, dtype=None, index=None, dist=None):
        if index is None:
            index = self.index
        if dist is None:
            dist = self.dist
        if dtype is None:
            dtype = self.dtype
            data = self.data
        else:
            data = dtype_to_array_type(dtype)
        return SeriesType(dtype, data, index, self.name_typ, dist)

    @property
    def key(self):
        return self.dtype, self.data, self.index, self.name_typ, self.dist

    def unify(self, typingctx, other):
        from bodo.transforms.distributed_analysis import Distribution
        if isinstance(other, SeriesType):
            dpi__kaql = (self.index if self.index == other.index else self.
                index.unify(typingctx, other.index))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if other.dtype == self.dtype or not other.dtype.is_precise():
                return SeriesType(self.dtype, self.data.unify(typingctx,
                    other.data), dpi__kaql, dist=dist)
        return super(SeriesType, self).unify(typingctx, other)

    def can_convert_to(self, typingctx, other):
        from numba.core.typeconv import Conversion
        if (isinstance(other, SeriesType) and self.dtype == other.dtype and
            self.data == other.data and self.index == other.index and self.
            name_typ == other.name_typ and self.dist != other.dist):
            return Conversion.safe

    def is_precise(self):
        return self.dtype.is_precise()

    @property
    def iterator_type(self):
        return self.data.iterator_type

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class HeterogeneousSeriesType(types.Type):
    ndim = 1

    def __init__(self, data=None, index=None, name_typ=None):
        from bodo.hiframes.pd_index_ext import RangeIndexType
        from bodo.transforms.distributed_analysis import Distribution
        self.data = data
        name_typ = types.none if name_typ is None else name_typ
        index = RangeIndexType(types.none) if index is None else index
        self.index = index
        self.name_typ = name_typ
        self.dist = Distribution.REP
        super(HeterogeneousSeriesType, self).__init__(name=
            f'heter_series({data}, {index}, {name_typ})')

    def copy(self, index=None, dist=None):
        from bodo.transforms.distributed_analysis import Distribution
        assert dist == Distribution.REP, 'invalid distribution for HeterogeneousSeriesType'
        if index is None:
            index = self.index.copy()
        return HeterogeneousSeriesType(self.data, index, self.name_typ)

    @property
    def key(self):
        return self.data, self.index, self.name_typ

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@lower_builtin('getiter', SeriesType)
def series_getiter(context, builder, sig, args):
    pbkt__wnuzj = get_series_payload(context, builder, sig.args[0], args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].data))
    return impl(builder, (pbkt__wnuzj.data,))


@infer_getattr
class HeterSeriesAttribute(OverloadedKeyAttributeTemplate):
    key = HeterogeneousSeriesType

    def generic_resolve(self, S, attr):
        from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
        if self._is_existing_attr(attr):
            return
        if isinstance(S.index, HeterogeneousIndexType
            ) and is_overload_constant_tuple(S.index.data):
            fmc__ohsk = get_overload_const_tuple(S.index.data)
            if attr in fmc__ohsk:
                jhi__uzqz = fmc__ohsk.index(attr)
                return S.data[jhi__uzqz]


def is_str_series_typ(t):
    return isinstance(t, SeriesType) and t.dtype == string_type


def is_dt64_series_typ(t):
    return isinstance(t, SeriesType) and (t.dtype == types.NPDatetime('ns') or
        isinstance(t.dtype, PandasDatetimeTZDtype))


def is_timedelta64_series_typ(t):
    return isinstance(t, SeriesType) and t.dtype == types.NPTimedelta('ns')


def is_datetime_date_series_typ(t):
    return isinstance(t, SeriesType) and t.dtype == datetime_date_type


class SeriesPayloadType(types.Type):

    def __init__(self, series_type):
        self.series_type = series_type
        super(SeriesPayloadType, self).__init__(name=
            f'SeriesPayloadType({series_type})')

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesPayloadType)
class SeriesPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        hbmq__hppy = [('data', fe_type.series_type.data), ('index', fe_type
            .series_type.index), ('name', fe_type.series_type.name_typ)]
        super(SeriesPayloadModel, self).__init__(dmm, fe_type, hbmq__hppy)


@register_model(HeterogeneousSeriesType)
@register_model(SeriesType)
class SeriesModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = SeriesPayloadType(fe_type)
        hbmq__hppy = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(SeriesModel, self).__init__(dmm, fe_type, hbmq__hppy)


def define_series_dtor(context, builder, series_type, payload_type):
    kdypf__ebw = builder.module
    goq__wbq = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    oifc__dlhev = cgutils.get_or_insert_function(kdypf__ebw, goq__wbq, name
        ='.dtor.series.{}'.format(series_type))
    if not oifc__dlhev.is_declaration:
        return oifc__dlhev
    oifc__dlhev.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(oifc__dlhev.append_basic_block())
    tpabn__ywm = oifc__dlhev.args[0]
    zetrg__ganlk = context.get_value_type(payload_type).as_pointer()
    srrcc__dvreq = builder.bitcast(tpabn__ywm, zetrg__ganlk)
    kkz__yewm = context.make_helper(builder, payload_type, ref=srrcc__dvreq)
    context.nrt.decref(builder, series_type.data, kkz__yewm.data)
    context.nrt.decref(builder, series_type.index, kkz__yewm.index)
    context.nrt.decref(builder, series_type.name_typ, kkz__yewm.name)
    builder.ret_void()
    return oifc__dlhev


def construct_series(context, builder, series_type, data_val, index_val,
    name_val):
    payload_type = SeriesPayloadType(series_type)
    pbkt__wnuzj = cgutils.create_struct_proxy(payload_type)(context, builder)
    pbkt__wnuzj.data = data_val
    pbkt__wnuzj.index = index_val
    pbkt__wnuzj.name = name_val
    nyu__kcema = context.get_value_type(payload_type)
    eol__rhmo = context.get_abi_sizeof(nyu__kcema)
    mdw__zstzw = define_series_dtor(context, builder, series_type, payload_type
        )
    yfawa__reads = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, eol__rhmo), mdw__zstzw)
    stgo__gkst = context.nrt.meminfo_data(builder, yfawa__reads)
    smylc__jrwc = builder.bitcast(stgo__gkst, nyu__kcema.as_pointer())
    builder.store(pbkt__wnuzj._getvalue(), smylc__jrwc)
    series = cgutils.create_struct_proxy(series_type)(context, builder)
    series.meminfo = yfawa__reads
    series.parent = cgutils.get_null_value(series.parent.type)
    return series._getvalue()


@intrinsic
def init_series(typingctx, data, index, name=None):
    from bodo.hiframes.pd_index_ext import is_pd_index_type
    from bodo.hiframes.pd_multi_index_ext import MultiIndexType
    assert is_pd_index_type(index) or isinstance(index, MultiIndexType)
    name = types.none if name is None else name

    def codegen(context, builder, signature, args):
        data_val, index_val, name_val = args
        series_type = signature.return_type
        iyvt__sntjf = construct_series(context, builder, series_type,
            data_val, index_val, name_val)
        context.nrt.incref(builder, signature.args[0], data_val)
        context.nrt.incref(builder, signature.args[1], index_val)
        context.nrt.incref(builder, signature.args[2], name_val)
        return iyvt__sntjf
    if is_heterogeneous_tuple_type(data):
        hebvv__kef = HeterogeneousSeriesType(data, index, name)
    else:
        dtype = data.dtype
        data = if_series_to_array_type(data)
        hebvv__kef = SeriesType(dtype, data, index, name)
    sig = signature(hebvv__kef, data, index, name)
    return sig, codegen


def init_series_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) >= 2 and not kws
    data = args[0]
    index = args[1]
    wjbbk__tnzs = self.typemap[data.name]
    if is_heterogeneous_tuple_type(wjbbk__tnzs) or isinstance(wjbbk__tnzs,
        types.BaseTuple):
        return None
    tjqk__idc = self.typemap[index.name]
    if not isinstance(tjqk__idc, HeterogeneousIndexType
        ) and equiv_set.has_shape(data) and equiv_set.has_shape(index):
        equiv_set.insert_equiv(data, index)
    if equiv_set.has_shape(data):
        return ArrayAnalysis.AnalyzeResult(shape=data, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_series_ext_init_series = (
    init_series_equiv)


def get_series_payload(context, builder, series_type, value):
    yfawa__reads = cgutils.create_struct_proxy(series_type)(context,
        builder, value).meminfo
    payload_type = SeriesPayloadType(series_type)
    kkz__yewm = context.nrt.meminfo_data(builder, yfawa__reads)
    zetrg__ganlk = context.get_value_type(payload_type).as_pointer()
    kkz__yewm = builder.bitcast(kkz__yewm, zetrg__ganlk)
    return context.make_helper(builder, payload_type, ref=kkz__yewm)


@intrinsic
def get_series_data(typingctx, series_typ=None):

    def codegen(context, builder, signature, args):
        pbkt__wnuzj = get_series_payload(context, builder, signature.args[0
            ], args[0])
        return impl_ret_borrowed(context, builder, series_typ.data,
            pbkt__wnuzj.data)
    hebvv__kef = series_typ.data
    sig = signature(hebvv__kef, series_typ)
    return sig, codegen


@intrinsic
def get_series_index(typingctx, series_typ=None):

    def codegen(context, builder, signature, args):
        pbkt__wnuzj = get_series_payload(context, builder, signature.args[0
            ], args[0])
        return impl_ret_borrowed(context, builder, series_typ.index,
            pbkt__wnuzj.index)
    hebvv__kef = series_typ.index
    sig = signature(hebvv__kef, series_typ)
    return sig, codegen


@intrinsic
def get_series_name(typingctx, series_typ=None):

    def codegen(context, builder, signature, args):
        pbkt__wnuzj = get_series_payload(context, builder, signature.args[0
            ], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            pbkt__wnuzj.name)
    sig = signature(series_typ.name_typ, series_typ)
    return sig, codegen


def get_series_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    eycuw__awyo = args[0]
    wjbbk__tnzs = self.typemap[eycuw__awyo.name].data
    if is_heterogeneous_tuple_type(wjbbk__tnzs) or isinstance(wjbbk__tnzs,
        types.BaseTuple):
        return None
    if equiv_set.has_shape(eycuw__awyo):
        return ArrayAnalysis.AnalyzeResult(shape=eycuw__awyo, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_series_ext_get_series_data
    ) = get_series_data_equiv


def get_series_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    eycuw__awyo = args[0]
    tjqk__idc = self.typemap[eycuw__awyo.name].index
    if isinstance(tjqk__idc, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(eycuw__awyo):
        return ArrayAnalysis.AnalyzeResult(shape=eycuw__awyo, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_series_ext_get_series_index
    ) = get_series_index_equiv


def alias_ext_init_series(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    if len(args) > 1:
        numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
            arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_series',
    'bodo.hiframes.pd_series_ext'] = alias_ext_init_series


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_series_data',
    'bodo.hiframes.pd_series_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_series_index',
    'bodo.hiframes.pd_series_ext'] = alias_ext_dummy_func


def is_series_type(typ):
    return isinstance(typ, SeriesType)


def if_series_to_array_type(typ):
    if isinstance(typ, SeriesType):
        return typ.data
    return typ


@lower_cast(SeriesType, SeriesType)
def cast_series(context, builder, fromty, toty, val):
    if fromty.copy(index=toty.index) == toty and isinstance(fromty.index,
        bodo.hiframes.pd_index_ext.RangeIndexType) and isinstance(toty.
        index, bodo.hiframes.pd_index_ext.NumericIndexType):
        pbkt__wnuzj = get_series_payload(context, builder, fromty, val)
        dpi__kaql = context.cast(builder, pbkt__wnuzj.index, fromty.index,
            toty.index)
        context.nrt.incref(builder, fromty.data, pbkt__wnuzj.data)
        context.nrt.incref(builder, fromty.name_typ, pbkt__wnuzj.name)
        return construct_series(context, builder, toty, pbkt__wnuzj.data,
            dpi__kaql, pbkt__wnuzj.name)
    if (fromty.dtype == toty.dtype and fromty.data == toty.data and fromty.
        index == toty.index and fromty.name_typ == toty.name_typ and fromty
        .dist != toty.dist):
        return val
    return val


@infer_getattr
class SeriesAttribute(OverloadedKeyAttributeTemplate):
    key = SeriesType

    @bound_function('series.head')
    def resolve_head(self, ary, args, kws):
        lvef__zvzkf = 'Series.head'
        tuboh__ded = 'n',
        qfejv__zzpo = {'n': 5}
        pysig, fyfc__hqet = bodo.utils.typing.fold_typing_args(lvef__zvzkf,
            args, kws, tuboh__ded, qfejv__zzpo)
        wll__wbfv = fyfc__hqet[0]
        if not is_overload_int(wll__wbfv):
            raise BodoError(f"{lvef__zvzkf}(): 'n' must be an Integer")
        jaju__hqfcr = ary
        return jaju__hqfcr(*fyfc__hqet).replace(pysig=pysig)

    def _resolve_map_func(self, ary, func, pysig, fname, f_args=None, kws=None
        ):
        dtype = ary.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(ary,
            'Series.map()')
        if dtype == types.NPDatetime('ns'):
            dtype = pd_timestamp_type
        if dtype == types.NPTimedelta('ns'):
            dtype = pd_timedelta_type
        jwbvg__fqi = dtype,
        if f_args is not None:
            jwbvg__fqi += tuple(f_args.types)
        if kws is None:
            kws = {}
        pccml__hdg = False
        rpll__hsuie = True
        if fname == 'map' and isinstance(func, types.DictType):
            rksrg__pryod = func.value_type
            pccml__hdg = True
        else:
            try:
                if types.unliteral(func) == types.unicode_type:
                    if not is_overload_constant_str(func):
                        raise BodoError(
                            f'Series.apply(): string argument (for builtins) must be a compile time constant'
                            )
                    rksrg__pryod = (bodo.utils.transform.
                        get_udf_str_return_type(ary, get_overload_const_str
                        (func), self.context, 'Series.apply'))
                    rpll__hsuie = False
                elif bodo.utils.typing.is_numpy_ufunc(func):
                    rksrg__pryod = func.get_call_type(self.context, (ary,), {}
                        ).return_type
                    rpll__hsuie = False
                else:
                    rksrg__pryod = get_const_func_output_type(func,
                        jwbvg__fqi, kws, self.context, numba.core.registry.
                        cpu_target.target_context)
            except Exception as qmtrk__enw:
                raise BodoError(get_udf_error_msg(f'Series.{fname}()',
                    qmtrk__enw))
        if rpll__hsuie:
            if isinstance(rksrg__pryod, (SeriesType, HeterogeneousSeriesType)
                ) and rksrg__pryod.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(rksrg__pryod, HeterogeneousSeriesType):
                rzf__ifyoz, shoqv__oqu = rksrg__pryod.const_info
                if isinstance(rksrg__pryod.data, bodo.libs.
                    nullable_tuple_ext.NullableTupleType):
                    eivkj__pel = rksrg__pryod.data.tuple_typ.types
                elif isinstance(rksrg__pryod.data, types.Tuple):
                    eivkj__pel = rksrg__pryod.data.types
                diars__qgsn = tuple(to_nullable_type(dtype_to_array_type(t)
                    ) for t in eivkj__pel)
                shzo__aenff = bodo.DataFrameType(diars__qgsn, ary.index,
                    shoqv__oqu)
            elif isinstance(rksrg__pryod, SeriesType):
                ilxqj__eiw, shoqv__oqu = rksrg__pryod.const_info
                diars__qgsn = tuple(to_nullable_type(dtype_to_array_type(
                    rksrg__pryod.dtype)) for rzf__ifyoz in range(ilxqj__eiw))
                shzo__aenff = bodo.DataFrameType(diars__qgsn, ary.index,
                    shoqv__oqu)
            else:
                rtq__aghk = get_udf_out_arr_type(rksrg__pryod, pccml__hdg)
                shzo__aenff = SeriesType(rtq__aghk.dtype, rtq__aghk, ary.
                    index, ary.name_typ)
        else:
            shzo__aenff = rksrg__pryod
        return signature(shzo__aenff, (func,)).replace(pysig=pysig)

    @bound_function('series.map', no_unliteral=True)
    def resolve_map(self, ary, args, kws):
        kws = dict(kws)
        func = args[0] if len(args) > 0 else kws['arg']
        kws.pop('arg', None)
        na_action = args[1] if len(args) > 1 else kws.pop('na_action',
            types.none)
        bss__osqnz = dict(na_action=na_action)
        crtsv__elayg = dict(na_action=None)
        check_unsupported_args('Series.map', bss__osqnz, crtsv__elayg,
            package_name='pandas', module_name='Series')

        def map_stub(arg, na_action=None):
            pass
        pysig = numba.core.utils.pysignature(map_stub)
        return self._resolve_map_func(ary, func, pysig, 'map')

    @bound_function('series.apply', no_unliteral=True)
    def resolve_apply(self, ary, args, kws):
        kws = dict(kws)
        func = args[0] if len(args) > 0 else kws['func']
        kws.pop('func', None)
        tde__pqfpn = args[1] if len(args) > 1 else kws.pop('convert_dtype',
            types.literal(True))
        f_args = args[2] if len(args) > 2 else kws.pop('args', None)
        bss__osqnz = dict(convert_dtype=tde__pqfpn)
        jpjae__oky = dict(convert_dtype=True)
        check_unsupported_args('Series.apply', bss__osqnz, jpjae__oky,
            package_name='pandas', module_name='Series')
        xeix__lak = ', '.join("{} = ''".format(kjw__syhqp) for kjw__syhqp in
            kws.keys())
        wtwq__uqs = (
            f'def apply_stub(func, convert_dtype=True, args=(), {xeix__lak}):\n'
            )
        wtwq__uqs += '    pass\n'
        wgbt__giaj = {}
        exec(wtwq__uqs, {}, wgbt__giaj)
        ggt__dtw = wgbt__giaj['apply_stub']
        pysig = numba.core.utils.pysignature(ggt__dtw)
        return self._resolve_map_func(ary, func, pysig, 'apply', f_args, kws)

    def _resolve_combine_func(self, ary, args, kws):
        kwargs = dict(kws)
        other = args[0] if len(args) > 0 else types.unliteral(kwargs['other'])
        func = args[1] if len(args) > 1 else kwargs['func']
        fill_value = args[2] if len(args) > 2 else types.unliteral(kwargs.
            get('fill_value', types.none))

        def combine_stub(other, func, fill_value=None):
            pass
        pysig = numba.core.utils.pysignature(combine_stub)
        wto__snshg = ary.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(ary,
            'Series.combine()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
            'Series.combine()')
        if wto__snshg == types.NPDatetime('ns'):
            wto__snshg = pd_timestamp_type
        jyqsq__betav = other.dtype
        if jyqsq__betav == types.NPDatetime('ns'):
            jyqsq__betav = pd_timestamp_type
        rksrg__pryod = get_const_func_output_type(func, (wto__snshg,
            jyqsq__betav), {}, self.context, numba.core.registry.cpu_target
            .target_context)
        sig = signature(SeriesType(rksrg__pryod, index=ary.index, name_typ=
            types.none), (other, func, fill_value))
        return sig.replace(pysig=pysig)

    @bound_function('series.combine', no_unliteral=True)
    def resolve_combine(self, ary, args, kws):
        return self._resolve_combine_func(ary, args, kws)

    @bound_function('series.pipe', no_unliteral=True)
    def resolve_pipe(self, ary, args, kws):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(ary,
            'Series.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, ary,
            args, kws, 'Series')

    def generic_resolve(self, S, attr):
        from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
        if self._is_existing_attr(attr):
            return
        if isinstance(S.index, HeterogeneousIndexType
            ) and is_overload_constant_tuple(S.index.data):
            fmc__ohsk = get_overload_const_tuple(S.index.data)
            if attr in fmc__ohsk:
                jhi__uzqz = fmc__ohsk.index(attr)
                return S.data[jhi__uzqz]


series_binary_ops = tuple(op for op in numba.core.typing.npydecl.
    NumpyRulesArrayOperator._op_map.keys() if op not in (operator.lshift,
    operator.rshift))
series_inplace_binary_ops = tuple(op for op in numba.core.typing.npydecl.
    NumpyRulesInplaceArrayOperator._op_map.keys() if op not in (operator.
    ilshift, operator.irshift, operator.itruediv))
inplace_binop_to_imm = {operator.iadd: operator.add, operator.isub:
    operator.sub, operator.imul: operator.mul, operator.ifloordiv: operator
    .floordiv, operator.imod: operator.mod, operator.ipow: operator.pow,
    operator.iand: operator.and_, operator.ior: operator.or_, operator.ixor:
    operator.xor}
series_unary_ops = operator.neg, operator.invert, operator.pos
str2str_methods = ('capitalize', 'lower', 'lstrip', 'rstrip', 'strip',
    'swapcase', 'title', 'upper')
str2bool_methods = ('isalnum', 'isalpha', 'isdigit', 'isspace', 'islower',
    'isupper', 'istitle', 'isnumeric', 'isdecimal')


@overload(pd.Series, no_unliteral=True)
def pd_series_overload(data=None, index=None, dtype=None, name=None, copy=
    False, fastpath=False):
    if not is_overload_false(fastpath):
        raise BodoError("pd.Series(): 'fastpath' argument not supported.")
    abm__zrind = is_overload_none(data)
    qquuw__nxnn = is_overload_none(index)
    htaiz__wqgto = is_overload_none(dtype)
    if abm__zrind and qquuw__nxnn and htaiz__wqgto:
        raise BodoError(
            'pd.Series() requires at least 1 of data, index, and dtype to not be none'
            )
    if is_series_type(data) and not qquuw__nxnn:
        raise BodoError(
            'pd.Series() does not support index value when input data is a Series'
            )
    if isinstance(data, types.DictType):
        raise_bodo_error(
            'pd.Series(): When intializing series with a dictionary, it is required that the dict has constant keys'
            )
    if is_heterogeneous_tuple_type(data) and is_overload_none(dtype):
        ezhy__kssb = tuple(len(data) * [False])

        def impl_heter(data=None, index=None, dtype=None, name=None, copy=
            False, fastpath=False):
            oheuh__nqry = bodo.utils.conversion.extract_index_if_none(data,
                index)
            belv__yynfu = bodo.utils.conversion.to_tuple(data)
            data_val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(
                belv__yynfu, ezhy__kssb)
            return bodo.hiframes.pd_series_ext.init_series(data_val, bodo.
                utils.conversion.convert_to_index(oheuh__nqry), name)
        return impl_heter
    if abm__zrind:
        if htaiz__wqgto:

            def impl(data=None, index=None, dtype=None, name=None, copy=
                False, fastpath=False):
                iuko__atm = bodo.utils.conversion.extract_name_if_none(data,
                    name)
                oheuh__nqry = bodo.utils.conversion.extract_index_if_none(data,
                    index)
                numba.parfors.parfor.init_prange()
                oxmk__fnsua = len(oheuh__nqry)
                belv__yynfu = np.empty(oxmk__fnsua, np.float64)
                for xbjj__tpxln in numba.parfors.parfor.internal_prange(
                    oxmk__fnsua):
                    bodo.libs.array_kernels.setna(belv__yynfu, xbjj__tpxln)
                return bodo.hiframes.pd_series_ext.init_series(belv__yynfu,
                    bodo.utils.conversion.convert_to_index(oheuh__nqry),
                    iuko__atm)
            return impl
        if bodo.utils.conversion._is_str_dtype(dtype):
            hoymf__jxq = bodo.string_array_type
        else:
            ero__xpc = bodo.utils.typing.parse_dtype(dtype, 'pandas.Series')
            if isinstance(ero__xpc, bodo.libs.int_arr_ext.IntDtype):
                hoymf__jxq = bodo.IntegerArrayType(ero__xpc.dtype)
            elif ero__xpc == bodo.libs.bool_arr_ext.boolean_dtype:
                hoymf__jxq = bodo.boolean_array
            elif isinstance(ero__xpc, types.Number) or ero__xpc in [bodo.
                datetime64ns, bodo.timedelta64ns]:
                hoymf__jxq = types.Array(ero__xpc, 1, 'C')
            else:
                raise BodoError(
                    'pd.Series with dtype: {dtype} not currently supported')
        if qquuw__nxnn:

            def impl(data=None, index=None, dtype=None, name=None, copy=
                False, fastpath=False):
                iuko__atm = bodo.utils.conversion.extract_name_if_none(data,
                    name)
                oheuh__nqry = bodo.hiframes.pd_index_ext.init_range_index(0,
                    0, 1, None)
                numba.parfors.parfor.init_prange()
                oxmk__fnsua = len(oheuh__nqry)
                belv__yynfu = bodo.utils.utils.alloc_type(oxmk__fnsua,
                    hoymf__jxq, (-1,))
                return bodo.hiframes.pd_series_ext.init_series(belv__yynfu,
                    oheuh__nqry, iuko__atm)
            return impl
        else:

            def impl(data=None, index=None, dtype=None, name=None, copy=
                False, fastpath=False):
                iuko__atm = bodo.utils.conversion.extract_name_if_none(data,
                    name)
                oheuh__nqry = bodo.utils.conversion.extract_index_if_none(data,
                    index)
                numba.parfors.parfor.init_prange()
                oxmk__fnsua = len(oheuh__nqry)
                belv__yynfu = bodo.utils.utils.alloc_type(oxmk__fnsua,
                    hoymf__jxq, (-1,))
                for xbjj__tpxln in numba.parfors.parfor.internal_prange(
                    oxmk__fnsua):
                    bodo.libs.array_kernels.setna(belv__yynfu, xbjj__tpxln)
                return bodo.hiframes.pd_series_ext.init_series(belv__yynfu,
                    bodo.utils.conversion.convert_to_index(oheuh__nqry),
                    iuko__atm)
            return impl

    def impl(data=None, index=None, dtype=None, name=None, copy=False,
        fastpath=False):
        iuko__atm = bodo.utils.conversion.extract_name_if_none(data, name)
        oheuh__nqry = bodo.utils.conversion.extract_index_if_none(data, index)
        jjukj__kktsc = bodo.utils.conversion.coerce_to_array(data, True,
            scalar_to_arr_len=len(oheuh__nqry))
        ejvoi__yeae = bodo.utils.conversion.fix_arr_dtype(jjukj__kktsc,
            dtype, None, False)
        return bodo.hiframes.pd_series_ext.init_series(ejvoi__yeae, bodo.
            utils.conversion.convert_to_index(oheuh__nqry), iuko__atm)
    return impl


@overload_method(SeriesType, 'to_csv', no_unliteral=True)
def to_csv_overload(series, path_or_buf=None, sep=',', na_rep='',
    float_format=None, columns=None, header=True, index=True, index_label=
    None, mode='w', encoding=None, compression='infer', quoting=None,
    quotechar='"', line_terminator=None, chunksize=None, date_format=None,
    doublequote=True, escapechar=None, decimal='.', errors='strict',
    _bodo_file_prefix='part-', _is_parallel=False):
    if not (is_overload_none(path_or_buf) or is_overload_constant_str(
        path_or_buf) or path_or_buf == string_type):
        raise BodoError(
            "Series.to_csv(): 'path_or_buf' argument should be None or string")
    if is_overload_none(path_or_buf):

        def _impl(series, path_or_buf=None, sep=',', na_rep='',
            float_format=None, columns=None, header=True, index=True,
            index_label=None, mode='w', encoding=None, compression='infer',
            quoting=None, quotechar='"', line_terminator=None, chunksize=
            None, date_format=None, doublequote=True, escapechar=None,
            decimal='.', errors='strict', _bodo_file_prefix='part-',
            _is_parallel=False):
            with numba.objmode(D='unicode_type'):
                D = series.to_csv(None, sep, na_rep, float_format, columns,
                    header, index, index_label, mode, encoding, compression,
                    quoting, quotechar, line_terminator, chunksize,
                    date_format, doublequote, escapechar, decimal, errors)
            return D
        return _impl

    def _impl(series, path_or_buf=None, sep=',', na_rep='', float_format=
        None, columns=None, header=True, index=True, index_label=None, mode
        ='w', encoding=None, compression='infer', quoting=None, quotechar=
        '"', line_terminator=None, chunksize=None, date_format=None,
        doublequote=True, escapechar=None, decimal='.', errors='strict',
        _bodo_file_prefix='part-', _is_parallel=False):
        if _is_parallel:
            header &= (bodo.libs.distributed_api.get_rank() == 0
                ) | _csv_output_is_dir(unicode_to_utf8(path_or_buf))
        with numba.objmode(D='unicode_type'):
            D = series.to_csv(None, sep, na_rep, float_format, columns,
                header, index, index_label, mode, encoding, compression,
                quoting, quotechar, line_terminator, chunksize, date_format,
                doublequote, escapechar, decimal, errors)
        bodo.io.fs_io.csv_write(path_or_buf, D, _bodo_file_prefix, _is_parallel
            )
    return _impl


@lower_constant(SeriesType)
def lower_constant_series(context, builder, series_type, pyval):
    if isinstance(series_type.data, bodo.DatetimeArrayType):
        kbqrk__nhj = pyval.array
    else:
        kbqrk__nhj = pyval.values
    data_val = context.get_constant_generic(builder, series_type.data,
        kbqrk__nhj)
    index_val = context.get_constant_generic(builder, series_type.index,
        pyval.index)
    name_val = context.get_constant_generic(builder, series_type.name_typ,
        pyval.name)
    kkz__yewm = lir.Constant.literal_struct([data_val, index_val, name_val])
    kkz__yewm = cgutils.global_constant(builder, '.const.payload', kkz__yewm
        ).bitcast(cgutils.voidptr_t)
    lsgn__gch = context.get_constant(types.int64, -1)
    udhsi__gri = context.get_constant_null(types.voidptr)
    yfawa__reads = lir.Constant.literal_struct([lsgn__gch, udhsi__gri,
        udhsi__gri, kkz__yewm, lsgn__gch])
    yfawa__reads = cgutils.global_constant(builder, '.const.meminfo',
        yfawa__reads).bitcast(cgutils.voidptr_t)
    iyvt__sntjf = lir.Constant.literal_struct([yfawa__reads, udhsi__gri])
    return iyvt__sntjf


series_unsupported_attrs = {'axes', 'array', 'flags', 'at', 'is_unique',
    'sparse', 'attrs'}
series_unsupported_methods = ('set_flags', 'convert_dtypes', 'bool',
    'to_period', 'to_timestamp', '__array__', 'get', 'at', '__iter__',
    'items', 'iteritems', 'pop', 'item', 'xs', 'combine_first', 'agg',
    'aggregate', 'transform', 'expanding', 'ewm', 'clip', 'factorize',
    'mode', 'align', 'drop', 'droplevel', 'reindex', 'reindex_like',
    'sample', 'set_axis', 'truncate', 'add_prefix', 'add_suffix', 'filter',
    'interpolate', 'argmin', 'argmax', 'reorder_levels', 'swaplevel',
    'unstack', 'searchsorted', 'ravel', 'squeeze', 'view', 'compare',
    'update', 'asfreq', 'asof', 'resample', 'tz_convert', 'tz_localize',
    'at_time', 'between_time', 'tshift', 'slice_shift', 'plot', 'hist',
    'to_pickle', 'to_excel', 'to_xarray', 'to_hdf', 'to_sql', 'to_json',
    'to_string', 'to_clipboard', 'to_latex', 'to_markdown')


def _install_series_unsupported():
    for lfkkg__xwmq in series_unsupported_attrs:
        qpyxc__rfg = 'Series.' + lfkkg__xwmq
        overload_attribute(SeriesType, lfkkg__xwmq)(create_unsupported_overload
            (qpyxc__rfg))
    for fname in series_unsupported_methods:
        qpyxc__rfg = 'Series.' + fname
        overload_method(SeriesType, fname, no_unliteral=True)(
            create_unsupported_overload(qpyxc__rfg))


_install_series_unsupported()
heter_series_unsupported_attrs = {'axes', 'array', 'dtype', 'nbytes',
    'memory_usage', 'hasnans', 'dtypes', 'flags', 'at', 'is_unique',
    'is_monotonic', 'is_monotonic_increasing', 'is_monotonic_decreasing',
    'dt', 'str', 'cat', 'sparse', 'attrs'}
heter_series_unsupported_methods = {'set_flags', 'convert_dtypes',
    'infer_objects', 'copy', 'bool', 'to_numpy', 'to_period',
    'to_timestamp', 'to_list', 'tolist', '__array__', 'get', 'at', 'iat',
    'iloc', 'loc', '__iter__', 'items', 'iteritems', 'keys', 'pop', 'item',
    'xs', 'add', 'sub', 'mul', 'div', 'truediv', 'floordiv', 'mod', 'pow',
    'radd', 'rsub', 'rmul', 'rdiv', 'rtruediv', 'rfloordiv', 'rmod', 'rpow',
    'combine', 'combine_first', 'round', 'lt', 'gt', 'le', 'ge', 'ne', 'eq',
    'product', 'dot', 'apply', 'agg', 'aggregate', 'transform', 'map',
    'groupby', 'rolling', 'expanding', 'ewm', 'pipe', 'abs', 'all', 'any',
    'autocorr', 'between', 'clip', 'corr', 'count', 'cov', 'cummax',
    'cummin', 'cumprod', 'cumsum', 'describe', 'diff', 'factorize', 'kurt',
    'mad', 'max', 'mean', 'median', 'min', 'mode', 'nlargest', 'nsmallest',
    'pct_change', 'prod', 'quantile', 'rank', 'sem', 'skew', 'std', 'sum',
    'var', 'kurtosis', 'unique', 'nunique', 'value_counts', 'align', 'drop',
    'droplevel', 'drop_duplicates', 'duplicated', 'equals', 'first', 'head',
    'idxmax', 'idxmin', 'isin', 'last', 'reindex', 'reindex_like', 'rename',
    'rename_axis', 'reset_index', 'sample', 'set_axis', 'take', 'tail',
    'truncate', 'where', 'mask', 'add_prefix', 'add_suffix', 'filter',
    'backfill', 'bfill', 'dropna', 'ffill', 'fillna', 'interpolate', 'isna',
    'isnull', 'notna', 'notnull', 'pad', 'replace', 'argsort', 'argmin',
    'argmax', 'reorder_levels', 'sort_values', 'sort_index', 'swaplevel',
    'unstack', 'explode', 'searchsorted', 'ravel', 'repeat', 'squeeze',
    'view', 'append', 'compare', 'update', 'asfreq', 'asof', 'shift',
    'first_valid_index', 'last_valid_index', 'resample', 'tz_convert',
    'tz_localize', 'at_time', 'between_time', 'tshift', 'slice_shift',
    'plot', 'hist', 'to_pickle', 'to_csv', 'to_dict', 'to_excel',
    'to_frame', 'to_xarray', 'to_hdf', 'to_sql', 'to_json', 'to_string',
    'to_clipboard', 'to_latex', 'to_markdown'}


def _install_heter_series_unsupported():
    for lfkkg__xwmq in heter_series_unsupported_attrs:
        qpyxc__rfg = 'HeterogeneousSeries.' + lfkkg__xwmq
        overload_attribute(HeterogeneousSeriesType, lfkkg__xwmq)(
            create_unsupported_overload(qpyxc__rfg))
    for fname in heter_series_unsupported_methods:
        qpyxc__rfg = 'HeterogeneousSeries.' + fname
        overload_method(HeterogeneousSeriesType, fname, no_unliteral=True)(
            create_unsupported_overload(qpyxc__rfg))


_install_heter_series_unsupported()
