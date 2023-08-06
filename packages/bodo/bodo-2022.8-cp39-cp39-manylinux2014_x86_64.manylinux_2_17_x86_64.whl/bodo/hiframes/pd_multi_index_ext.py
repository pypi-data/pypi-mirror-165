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
        tjtt__ruo = [('data', types.Tuple(fe_type.array_types)), ('names',
            types.Tuple(fe_type.names_typ)), ('name', fe_type.name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, tjtt__ruo)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[xsy__uvtyn].values) for
        xsy__uvtyn in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (lla__hykii) for lla__hykii in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    fbb__sczn = c.context.insert_const_string(c.builder.module, 'pandas')
    xke__azr = c.pyapi.import_module_noblock(fbb__sczn)
    vub__etxot = c.pyapi.object_getattr_string(xke__azr, 'MultiIndex')
    spzrx__xcrx = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types),
        spzrx__xcrx.data)
    pmwkq__svn = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        spzrx__xcrx.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ), spzrx__xcrx
        .names)
    pcfl__zty = c.pyapi.from_native_value(types.Tuple(typ.names_typ),
        spzrx__xcrx.names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, spzrx__xcrx.name)
    kinr__yvve = c.pyapi.from_native_value(typ.name_typ, spzrx__xcrx.name,
        c.env_manager)
    vkp__qpya = c.pyapi.borrow_none()
    svyl__asraf = c.pyapi.call_method(vub__etxot, 'from_arrays', (
        pmwkq__svn, vkp__qpya, pcfl__zty))
    c.pyapi.object_setattr_string(svyl__asraf, 'name', kinr__yvve)
    c.pyapi.decref(pmwkq__svn)
    c.pyapi.decref(pcfl__zty)
    c.pyapi.decref(kinr__yvve)
    c.pyapi.decref(xke__azr)
    c.pyapi.decref(vub__etxot)
    c.context.nrt.decref(c.builder, typ, val)
    return svyl__asraf


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    nqys__vlpzt = []
    aghd__fwtko = []
    for xsy__uvtyn in range(typ.nlevels):
        rohtx__wczq = c.pyapi.unserialize(c.pyapi.serialize_object(xsy__uvtyn))
        nmde__ylm = c.pyapi.call_method(val, 'get_level_values', (rohtx__wczq,)
            )
        gvq__rsbs = c.pyapi.object_getattr_string(nmde__ylm, 'values')
        c.pyapi.decref(nmde__ylm)
        c.pyapi.decref(rohtx__wczq)
        ywk__avqgb = c.pyapi.to_native_value(typ.array_types[xsy__uvtyn],
            gvq__rsbs).value
        nqys__vlpzt.append(ywk__avqgb)
        aghd__fwtko.append(gvq__rsbs)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, nqys__vlpzt)
    else:
        data = cgutils.pack_struct(c.builder, nqys__vlpzt)
    pcfl__zty = c.pyapi.object_getattr_string(val, 'names')
    iicz__qji = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    qrs__suw = c.pyapi.call_function_objargs(iicz__qji, (pcfl__zty,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), qrs__suw).value
    kinr__yvve = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, kinr__yvve).value
    spzrx__xcrx = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    spzrx__xcrx.data = data
    spzrx__xcrx.names = names
    spzrx__xcrx.name = name
    for gvq__rsbs in aghd__fwtko:
        c.pyapi.decref(gvq__rsbs)
    c.pyapi.decref(pcfl__zty)
    c.pyapi.decref(iicz__qji)
    c.pyapi.decref(qrs__suw)
    c.pyapi.decref(kinr__yvve)
    return NativeValue(spzrx__xcrx._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    tei__xldvp = 'pandas.MultiIndex.from_product'
    ycpw__eghl = dict(sortorder=sortorder)
    rpd__ilpok = dict(sortorder=None)
    check_unsupported_args(tei__xldvp, ycpw__eghl, rpd__ilpok, package_name
        ='pandas', module_name='Index')
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{tei__xldvp}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{tei__xldvp}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{tei__xldvp}: iterables and names must be of the same length.')


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
    oway__mbuuj = MultiIndexType(array_types, names_typ)
    nbr__eehgf = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, nbr__eehgf, oway__mbuuj)
    gxg__sngg = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{nbr__eehgf}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    qpl__kxjyr = {}
    exec(gxg__sngg, globals(), qpl__kxjyr)
    hmbj__mkhb = qpl__kxjyr['impl']
    return hmbj__mkhb


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        ypibd__cifsv, tdqc__qunob, ziqz__cgsbu = args
        nvrsc__pdzs = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        nvrsc__pdzs.data = ypibd__cifsv
        nvrsc__pdzs.names = tdqc__qunob
        nvrsc__pdzs.name = ziqz__cgsbu
        context.nrt.incref(builder, signature.args[0], ypibd__cifsv)
        context.nrt.incref(builder, signature.args[1], tdqc__qunob)
        context.nrt.incref(builder, signature.args[2], ziqz__cgsbu)
        return nvrsc__pdzs._getvalue()
    nfl__rtn = MultiIndexType(data.types, names.types, name)
    return nfl__rtn(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        bhocv__xrp = len(I.array_types)
        gxg__sngg = 'def impl(I, ind):\n'
        gxg__sngg += '  data = I._data\n'
        gxg__sngg += ('  return init_multi_index(({},), I._names, I._name)\n'
            .format(', '.join(
            f'ensure_contig_if_np(data[{xsy__uvtyn}][ind])' for xsy__uvtyn in
            range(bhocv__xrp))))
        qpl__kxjyr = {}
        exec(gxg__sngg, {'init_multi_index': init_multi_index,
            'ensure_contig_if_np': ensure_contig_if_np}, qpl__kxjyr)
        hmbj__mkhb = qpl__kxjyr['impl']
        return hmbj__mkhb


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    jsdn__kuv, ynlm__buy = sig.args
    if jsdn__kuv != ynlm__buy:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
