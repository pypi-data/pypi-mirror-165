"""Support for MultiIndex type of Pandas
"""
import operator
import numba
import pandas as pd
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, register_model, typeof_impl, unbox
from bodo.utils.conversion import ensure_contig_if_np
from bodo.utils.typing import BodoError, check_unsupported_args, dtype_to_array_type, get_val_type_maybe_str_literal, is_overload_none


class MultiIndexType(types.ArrayCompatible):

    def __init__(self, array_types, names_typ=None, name_typ=None):
        names_typ = (types.none,) * len(array_types
            ) if names_typ is None else names_typ
        name_typ = types.none if name_typ is None else name_typ
        self.array_types = array_types
        self.names_typ = names_typ
        self.name_typ = name_typ
        super(MultiIndexType, self).__init__(name=
            'MultiIndexType({}, {}, {})'.format(array_types, names_typ,
            name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return MultiIndexType(self.array_types, self.names_typ, self.name_typ)

    @property
    def nlevels(self):
        return len(self.array_types)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(MultiIndexType)
class MultiIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        uwzeh__oovwq = [('data', types.Tuple(fe_type.array_types)), (
            'names', types.Tuple(fe_type.names_typ)), ('name', fe_type.
            name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, uwzeh__oovwq)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[tragu__nspjy].values) for
        tragu__nspjy in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (khaf__qqsp) for khaf__qqsp in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    sfk__rpun = c.context.insert_const_string(c.builder.module, 'pandas')
    mxd__qlcox = c.pyapi.import_module_noblock(sfk__rpun)
    wlxk__bfcx = c.pyapi.object_getattr_string(mxd__qlcox, 'MultiIndex')
    mwo__xtq = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types), mwo__xtq.data
        )
    seyst__ywr = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        mwo__xtq.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ), mwo__xtq.names)
    efvmh__nxo = c.pyapi.from_native_value(types.Tuple(typ.names_typ),
        mwo__xtq.names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, mwo__xtq.name)
    rumb__ikrmm = c.pyapi.from_native_value(typ.name_typ, mwo__xtq.name, c.
        env_manager)
    tzdb__lbqhy = c.pyapi.borrow_none()
    qdga__cjnt = c.pyapi.call_method(wlxk__bfcx, 'from_arrays', (seyst__ywr,
        tzdb__lbqhy, efvmh__nxo))
    c.pyapi.object_setattr_string(qdga__cjnt, 'name', rumb__ikrmm)
    c.pyapi.decref(seyst__ywr)
    c.pyapi.decref(efvmh__nxo)
    c.pyapi.decref(rumb__ikrmm)
    c.pyapi.decref(mxd__qlcox)
    c.pyapi.decref(wlxk__bfcx)
    c.context.nrt.decref(c.builder, typ, val)
    return qdga__cjnt


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    ohv__cpc = []
    scfm__zlq = []
    for tragu__nspjy in range(typ.nlevels):
        dqg__qddph = c.pyapi.unserialize(c.pyapi.serialize_object(tragu__nspjy)
            )
        xrk__vrmz = c.pyapi.call_method(val, 'get_level_values', (dqg__qddph,))
        buc__txk = c.pyapi.object_getattr_string(xrk__vrmz, 'values')
        c.pyapi.decref(xrk__vrmz)
        c.pyapi.decref(dqg__qddph)
        hlrbt__ozdwp = c.pyapi.to_native_value(typ.array_types[tragu__nspjy
            ], buc__txk).value
        ohv__cpc.append(hlrbt__ozdwp)
        scfm__zlq.append(buc__txk)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, ohv__cpc)
    else:
        data = cgutils.pack_struct(c.builder, ohv__cpc)
    efvmh__nxo = c.pyapi.object_getattr_string(val, 'names')
    vtwfi__prg = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    llraw__fdg = c.pyapi.call_function_objargs(vtwfi__prg, (efvmh__nxo,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), llraw__fdg
        ).value
    rumb__ikrmm = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, rumb__ikrmm).value
    mwo__xtq = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mwo__xtq.data = data
    mwo__xtq.names = names
    mwo__xtq.name = name
    for buc__txk in scfm__zlq:
        c.pyapi.decref(buc__txk)
    c.pyapi.decref(efvmh__nxo)
    c.pyapi.decref(vtwfi__prg)
    c.pyapi.decref(llraw__fdg)
    c.pyapi.decref(rumb__ikrmm)
    return NativeValue(mwo__xtq._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    tdvu__krfsx = 'pandas.MultiIndex.from_product'
    uhmft__wof = dict(sortorder=sortorder)
    dnpg__zysz = dict(sortorder=None)
    check_unsupported_args(tdvu__krfsx, uhmft__wof, dnpg__zysz,
        package_name='pandas', module_name='Index')
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{tdvu__krfsx}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{tdvu__krfsx}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{tdvu__krfsx}: iterables and names must be of the same length.')


def from_product(iterable, sortorder=None, names=None):
    pass


@overload(from_product)
def from_product_overload(iterables, sortorder=None, names=None):
    from_product_error_checking(iterables, sortorder, names)
    array_types = tuple(dtype_to_array_type(iterable.dtype) for iterable in
        iterables)
    if is_overload_none(names):
        names_typ = tuple([types.none] * len(iterables))
    else:
        names_typ = names.types
    dhzci__ifv = MultiIndexType(array_types, names_typ)
    gglns__fsadl = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, gglns__fsadl, dhzci__ifv)
    heibx__qpo = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{gglns__fsadl}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    xswa__ohsox = {}
    exec(heibx__qpo, globals(), xswa__ohsox)
    wnuxq__cimsa = xswa__ohsox['impl']
    return wnuxq__cimsa


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        gqjy__lroc, ggi__dzyk, gixt__yjcc = args
        dstsk__bwju = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        dstsk__bwju.data = gqjy__lroc
        dstsk__bwju.names = ggi__dzyk
        dstsk__bwju.name = gixt__yjcc
        context.nrt.incref(builder, signature.args[0], gqjy__lroc)
        context.nrt.incref(builder, signature.args[1], ggi__dzyk)
        context.nrt.incref(builder, signature.args[2], gixt__yjcc)
        return dstsk__bwju._getvalue()
    wqry__lea = MultiIndexType(data.types, names.types, name)
    return wqry__lea(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        hdbvi__gmocf = len(I.array_types)
        heibx__qpo = 'def impl(I, ind):\n'
        heibx__qpo += '  data = I._data\n'
        heibx__qpo += ('  return init_multi_index(({},), I._names, I._name)\n'
            .format(', '.join(
            f'ensure_contig_if_np(data[{tragu__nspjy}][ind])' for
            tragu__nspjy in range(hdbvi__gmocf))))
        xswa__ohsox = {}
        exec(heibx__qpo, {'init_multi_index': init_multi_index,
            'ensure_contig_if_np': ensure_contig_if_np}, xswa__ohsox)
        wnuxq__cimsa = xswa__ohsox['impl']
        return wnuxq__cimsa


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    anjt__pfrv, bpos__qyz = sig.args
    if anjt__pfrv != bpos__qyz:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
