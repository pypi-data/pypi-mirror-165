"""
Wrapper class for Tuples that supports tracking null entries.
This is primarily used for maintaining null information for
Series values used in df.apply
"""
import operator
import numba
from numba.core import cgutils, types
from numba.extending import box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_method, register_model


class NullableTupleType(types.IterableType):

    def __init__(self, tuple_typ, null_typ):
        self._tuple_typ = tuple_typ
        self._null_typ = null_typ
        super(NullableTupleType, self).__init__(name=
            f'NullableTupleType({tuple_typ}, {null_typ})')

    @property
    def tuple_typ(self):
        return self._tuple_typ

    @property
    def null_typ(self):
        return self._null_typ

    def __getitem__(self, i):
        return self._tuple_typ[i]

    @property
    def key(self):
        return self._tuple_typ

    @property
    def dtype(self):
        return self.tuple_typ.dtype

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def iterator_type(self):
        return self.tuple_typ.iterator_type

    def __len__(self):
        return len(self.tuple_typ)


@register_model(NullableTupleType)
class NullableTupleModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        viave__ate = [('data', fe_type.tuple_typ), ('null_values', fe_type.
            null_typ)]
        super(NullableTupleModel, self).__init__(dmm, fe_type, viave__ate)


make_attribute_wrapper(NullableTupleType, 'data', '_data')
make_attribute_wrapper(NullableTupleType, 'null_values', '_null_values')


@intrinsic
def build_nullable_tuple(typingctx, data_tuple, null_values):
    assert isinstance(data_tuple, types.BaseTuple
        ), "build_nullable_tuple 'data_tuple' argument must be a tuple"
    assert isinstance(null_values, types.BaseTuple
        ), "build_nullable_tuple 'null_values' argument must be a tuple"
    data_tuple = types.unliteral(data_tuple)
    null_values = types.unliteral(null_values)

    def codegen(context, builder, signature, args):
        data_tuple, null_values = args
        xzv__rcq = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        xzv__rcq.data = data_tuple
        xzv__rcq.null_values = null_values
        context.nrt.incref(builder, signature.args[0], data_tuple)
        context.nrt.incref(builder, signature.args[1], null_values)
        return xzv__rcq._getvalue()
    sig = NullableTupleType(data_tuple, null_values)(data_tuple, null_values)
    return sig, codegen


@box(NullableTupleType)
def box_nullable_tuple(typ, val, c):
    qhg__tjm = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val
        )
    c.context.nrt.incref(c.builder, typ.tuple_typ, qhg__tjm.data)
    c.context.nrt.incref(c.builder, typ.null_typ, qhg__tjm.null_values)
    hbj__ouewn = c.pyapi.from_native_value(typ.tuple_typ, qhg__tjm.data, c.
        env_manager)
    hbhf__brls = c.pyapi.from_native_value(typ.null_typ, qhg__tjm.
        null_values, c.env_manager)
    qwu__wsexf = c.context.get_constant(types.int64, len(typ.tuple_typ))
    sokj__rjeox = c.pyapi.list_new(qwu__wsexf)
    with cgutils.for_range(c.builder, qwu__wsexf) as hgzh__grxgs:
        i = hgzh__grxgs.index
        ttsn__bmj = c.pyapi.long_from_longlong(i)
        vzxmu__udlto = c.pyapi.object_getitem(hbhf__brls, ttsn__bmj)
        hwfbg__mxqy = c.pyapi.to_native_value(types.bool_, vzxmu__udlto).value
        with c.builder.if_else(hwfbg__mxqy) as (rqbio__krnh, zrc__xjhlq):
            with rqbio__krnh:
                c.pyapi.list_setitem(sokj__rjeox, i, c.pyapi.make_none())
            with zrc__xjhlq:
                fhrnb__ysusq = c.pyapi.object_getitem(hbj__ouewn, ttsn__bmj)
                c.pyapi.list_setitem(sokj__rjeox, i, fhrnb__ysusq)
        c.pyapi.decref(ttsn__bmj)
        c.pyapi.decref(vzxmu__udlto)
    wcco__nxz = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    bsjx__iidk = c.pyapi.call_function_objargs(wcco__nxz, (sokj__rjeox,))
    c.pyapi.decref(hbj__ouewn)
    c.pyapi.decref(hbhf__brls)
    c.pyapi.decref(wcco__nxz)
    c.pyapi.decref(sokj__rjeox)
    c.context.nrt.decref(c.builder, typ, val)
    return bsjx__iidk


@overload(operator.getitem)
def overload_getitem(A, idx):
    if not isinstance(A, NullableTupleType):
        return
    return lambda A, idx: A._data[idx]


@overload(len)
def overload_len(A):
    if not isinstance(A, NullableTupleType):
        return
    return lambda A: len(A._data)


@lower_builtin('getiter', NullableTupleType)
def nullable_tuple_getiter(context, builder, sig, args):
    xzv__rcq = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].
        tuple_typ))
    return impl(builder, (xzv__rcq.data,))


@overload(operator.eq)
def nullable_tuple_eq(val1, val2):
    if not isinstance(val1, NullableTupleType) or not isinstance(val2,
        NullableTupleType):
        return
    if val1 != val2:
        return lambda val1, val2: False
    thw__wtf = 'def impl(val1, val2):\n'
    thw__wtf += '    data_tup1 = val1._data\n'
    thw__wtf += '    null_tup1 = val1._null_values\n'
    thw__wtf += '    data_tup2 = val2._data\n'
    thw__wtf += '    null_tup2 = val2._null_values\n'
    ils__rosa = val1._tuple_typ
    for i in range(len(ils__rosa)):
        thw__wtf += f'    null1_{i} = null_tup1[{i}]\n'
        thw__wtf += f'    null2_{i} = null_tup2[{i}]\n'
        thw__wtf += f'    data1_{i} = data_tup1[{i}]\n'
        thw__wtf += f'    data2_{i} = data_tup2[{i}]\n'
        thw__wtf += f'    if null1_{i} != null2_{i}:\n'
        thw__wtf += '        return False\n'
        thw__wtf += f'    if null1_{i} and (data1_{i} != data2_{i}):\n'
        thw__wtf += f'        return False\n'
    thw__wtf += f'    return True\n'
    yimka__ctemm = {}
    exec(thw__wtf, {}, yimka__ctemm)
    impl = yimka__ctemm['impl']
    return impl


@overload_method(NullableTupleType, '__hash__')
def nullable_tuple_hash(val):

    def impl(val):
        return _nullable_tuple_hash(val)
    return impl


_PyHASH_XXPRIME_1 = numba.cpython.hashing._PyHASH_XXPRIME_1
_PyHASH_XXPRIME_2 = numba.cpython.hashing._PyHASH_XXPRIME_1
_PyHASH_XXPRIME_5 = numba.cpython.hashing._PyHASH_XXPRIME_1


@numba.generated_jit(nopython=True)
def _nullable_tuple_hash(nullable_tup):
    thw__wtf = 'def impl(nullable_tup):\n'
    thw__wtf += '    data_tup = nullable_tup._data\n'
    thw__wtf += '    null_tup = nullable_tup._null_values\n'
    thw__wtf += '    tl = numba.cpython.hashing._Py_uhash_t(len(data_tup))\n'
    thw__wtf += '    acc = _PyHASH_XXPRIME_5\n'
    ils__rosa = nullable_tup._tuple_typ
    for i in range(len(ils__rosa)):
        thw__wtf += f'    null_val_{i} = null_tup[{i}]\n'
        thw__wtf += f'    null_lane_{i} = hash(null_val_{i})\n'
        thw__wtf += (
            f'    if null_lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n'
            )
        thw__wtf += '        return -1\n'
        thw__wtf += f'    acc += null_lane_{i} * _PyHASH_XXPRIME_2\n'
        thw__wtf += '    acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n'
        thw__wtf += '    acc *= _PyHASH_XXPRIME_1\n'
        thw__wtf += f'    if not null_val_{i}:\n'
        thw__wtf += f'        lane_{i} = hash(data_tup[{i}])\n'
        thw__wtf += (
            f'        if lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n')
        thw__wtf += f'            return -1\n'
        thw__wtf += f'        acc += lane_{i} * _PyHASH_XXPRIME_2\n'
        thw__wtf += (
            '        acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        thw__wtf += '        acc *= _PyHASH_XXPRIME_1\n'
    thw__wtf += """    acc += tl ^ (_PyHASH_XXPRIME_5 ^ numba.cpython.hashing._Py_uhash_t(3527539))
"""
    thw__wtf += '    if acc == numba.cpython.hashing._Py_uhash_t(-1):\n'
    thw__wtf += (
        '        return numba.cpython.hashing.process_return(1546275796)\n')
    thw__wtf += '    return numba.cpython.hashing.process_return(acc)\n'
    yimka__ctemm = {}
    exec(thw__wtf, {'numba': numba, '_PyHASH_XXPRIME_1': _PyHASH_XXPRIME_1,
        '_PyHASH_XXPRIME_2': _PyHASH_XXPRIME_2, '_PyHASH_XXPRIME_5':
        _PyHASH_XXPRIME_5}, yimka__ctemm)
    impl = yimka__ctemm['impl']
    return impl
