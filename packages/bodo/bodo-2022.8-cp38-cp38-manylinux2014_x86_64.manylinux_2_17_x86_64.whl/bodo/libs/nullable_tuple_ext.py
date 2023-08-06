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
        rmk__aae = [('data', fe_type.tuple_typ), ('null_values', fe_type.
            null_typ)]
        super(NullableTupleModel, self).__init__(dmm, fe_type, rmk__aae)


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
        axrx__ohctc = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        axrx__ohctc.data = data_tuple
        axrx__ohctc.null_values = null_values
        context.nrt.incref(builder, signature.args[0], data_tuple)
        context.nrt.incref(builder, signature.args[1], null_values)
        return axrx__ohctc._getvalue()
    sig = NullableTupleType(data_tuple, null_values)(data_tuple, null_values)
    return sig, codegen


@box(NullableTupleType)
def box_nullable_tuple(typ, val, c):
    glz__aprl = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    c.context.nrt.incref(c.builder, typ.tuple_typ, glz__aprl.data)
    c.context.nrt.incref(c.builder, typ.null_typ, glz__aprl.null_values)
    fun__pzw = c.pyapi.from_native_value(typ.tuple_typ, glz__aprl.data, c.
        env_manager)
    gcep__efm = c.pyapi.from_native_value(typ.null_typ, glz__aprl.
        null_values, c.env_manager)
    clth__djcci = c.context.get_constant(types.int64, len(typ.tuple_typ))
    zede__pvl = c.pyapi.list_new(clth__djcci)
    with cgutils.for_range(c.builder, clth__djcci) as tgy__jsmh:
        i = tgy__jsmh.index
        hdx__fesp = c.pyapi.long_from_longlong(i)
        fefvd__pvbms = c.pyapi.object_getitem(gcep__efm, hdx__fesp)
        xpo__xjxe = c.pyapi.to_native_value(types.bool_, fefvd__pvbms).value
        with c.builder.if_else(xpo__xjxe) as (igh__yagr, jxpgk__jtl):
            with igh__yagr:
                c.pyapi.list_setitem(zede__pvl, i, c.pyapi.make_none())
            with jxpgk__jtl:
                unfr__msu = c.pyapi.object_getitem(fun__pzw, hdx__fesp)
                c.pyapi.list_setitem(zede__pvl, i, unfr__msu)
        c.pyapi.decref(hdx__fesp)
        c.pyapi.decref(fefvd__pvbms)
    oot__lrisj = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    xja__lcun = c.pyapi.call_function_objargs(oot__lrisj, (zede__pvl,))
    c.pyapi.decref(fun__pzw)
    c.pyapi.decref(gcep__efm)
    c.pyapi.decref(oot__lrisj)
    c.pyapi.decref(zede__pvl)
    c.context.nrt.decref(c.builder, typ, val)
    return xja__lcun


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
    axrx__ohctc = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].
        tuple_typ))
    return impl(builder, (axrx__ohctc.data,))


@overload(operator.eq)
def nullable_tuple_eq(val1, val2):
    if not isinstance(val1, NullableTupleType) or not isinstance(val2,
        NullableTupleType):
        return
    if val1 != val2:
        return lambda val1, val2: False
    nahz__faiuk = 'def impl(val1, val2):\n'
    nahz__faiuk += '    data_tup1 = val1._data\n'
    nahz__faiuk += '    null_tup1 = val1._null_values\n'
    nahz__faiuk += '    data_tup2 = val2._data\n'
    nahz__faiuk += '    null_tup2 = val2._null_values\n'
    dtdf__jbi = val1._tuple_typ
    for i in range(len(dtdf__jbi)):
        nahz__faiuk += f'    null1_{i} = null_tup1[{i}]\n'
        nahz__faiuk += f'    null2_{i} = null_tup2[{i}]\n'
        nahz__faiuk += f'    data1_{i} = data_tup1[{i}]\n'
        nahz__faiuk += f'    data2_{i} = data_tup2[{i}]\n'
        nahz__faiuk += f'    if null1_{i} != null2_{i}:\n'
        nahz__faiuk += '        return False\n'
        nahz__faiuk += f'    if null1_{i} and (data1_{i} != data2_{i}):\n'
        nahz__faiuk += f'        return False\n'
    nahz__faiuk += f'    return True\n'
    neewm__vwaoq = {}
    exec(nahz__faiuk, {}, neewm__vwaoq)
    impl = neewm__vwaoq['impl']
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
    nahz__faiuk = 'def impl(nullable_tup):\n'
    nahz__faiuk += '    data_tup = nullable_tup._data\n'
    nahz__faiuk += '    null_tup = nullable_tup._null_values\n'
    nahz__faiuk += (
        '    tl = numba.cpython.hashing._Py_uhash_t(len(data_tup))\n')
    nahz__faiuk += '    acc = _PyHASH_XXPRIME_5\n'
    dtdf__jbi = nullable_tup._tuple_typ
    for i in range(len(dtdf__jbi)):
        nahz__faiuk += f'    null_val_{i} = null_tup[{i}]\n'
        nahz__faiuk += f'    null_lane_{i} = hash(null_val_{i})\n'
        nahz__faiuk += (
            f'    if null_lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n'
            )
        nahz__faiuk += '        return -1\n'
        nahz__faiuk += f'    acc += null_lane_{i} * _PyHASH_XXPRIME_2\n'
        nahz__faiuk += (
            '    acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        nahz__faiuk += '    acc *= _PyHASH_XXPRIME_1\n'
        nahz__faiuk += f'    if not null_val_{i}:\n'
        nahz__faiuk += f'        lane_{i} = hash(data_tup[{i}])\n'
        nahz__faiuk += (
            f'        if lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n')
        nahz__faiuk += f'            return -1\n'
        nahz__faiuk += f'        acc += lane_{i} * _PyHASH_XXPRIME_2\n'
        nahz__faiuk += (
            '        acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        nahz__faiuk += '        acc *= _PyHASH_XXPRIME_1\n'
    nahz__faiuk += """    acc += tl ^ (_PyHASH_XXPRIME_5 ^ numba.cpython.hashing._Py_uhash_t(3527539))
"""
    nahz__faiuk += '    if acc == numba.cpython.hashing._Py_uhash_t(-1):\n'
    nahz__faiuk += (
        '        return numba.cpython.hashing.process_return(1546275796)\n')
    nahz__faiuk += '    return numba.cpython.hashing.process_return(acc)\n'
    neewm__vwaoq = {}
    exec(nahz__faiuk, {'numba': numba, '_PyHASH_XXPRIME_1':
        _PyHASH_XXPRIME_1, '_PyHASH_XXPRIME_2': _PyHASH_XXPRIME_2,
        '_PyHASH_XXPRIME_5': _PyHASH_XXPRIME_5}, neewm__vwaoq)
    impl = neewm__vwaoq['impl']
    return impl
