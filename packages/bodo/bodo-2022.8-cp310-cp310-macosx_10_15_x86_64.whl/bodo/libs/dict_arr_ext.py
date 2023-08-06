"""Dictionary encoded array data type, similar to DictionaryArray of Arrow.
The purpose is to improve memory consumption and performance over string_array_type for
string arrays that have a lot of repetitive values (typical in practice).
Can be extended to be used with types other than strings as well.
See:
https://bodo.atlassian.net/browse/BE-2295
https://bodo.atlassian.net/wiki/spaces/B/pages/993722369/Dictionary-encoded+String+Array+Support+in+Parquet+read+compute+...
https://arrow.apache.org/docs/cpp/api/array.html#dictionary-encoded
"""
import operator
import re
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_new_ref, lower_builtin, lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
import bodo
from bodo.libs import hstr_ext
from bodo.libs.bool_arr_ext import init_bool_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, get_str_arr_item_length, overload_str_arr_astype, pre_alloc_string_array, string_array_type
from bodo.utils.typing import BodoArrayIterator, is_overload_none, raise_bodo_error
from bodo.utils.utils import synchronize_error_njit
ll.add_symbol('box_dict_str_array', hstr_ext.box_dict_str_array)
dict_indices_arr_type = IntegerArrayType(types.int32)


class DictionaryArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self, arr_data_type):
        self.data = arr_data_type
        super(DictionaryArrayType, self).__init__(name=
            f'DictionaryArrayType({arr_data_type})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def iterator_type(self):
        return BodoArrayIterator(self)

    @property
    def dtype(self):
        return self.data.dtype

    def copy(self):
        return DictionaryArrayType(self.data)

    @property
    def indices_type(self):
        return dict_indices_arr_type

    @property
    def indices_dtype(self):
        return dict_indices_arr_type.dtype

    def unify(self, typingctx, other):
        if other == string_array_type:
            return string_array_type


dict_str_arr_type = DictionaryArrayType(string_array_type)


@register_model(DictionaryArrayType)
class DictionaryArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        sep__bxngn = [('data', fe_type.data), ('indices',
            dict_indices_arr_type), ('has_global_dictionary', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, sep__bxngn)


make_attribute_wrapper(DictionaryArrayType, 'data', '_data')
make_attribute_wrapper(DictionaryArrayType, 'indices', '_indices')
make_attribute_wrapper(DictionaryArrayType, 'has_global_dictionary',
    '_has_global_dictionary')
lower_builtin('getiter', dict_str_arr_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_dict_arr(typingctx, data_t, indices_t, glob_dict_t=None):
    assert indices_t == dict_indices_arr_type, 'invalid indices type for dict array'

    def codegen(context, builder, signature, args):
        supn__ttl, vcgs__itjca, swwt__epcwo = args
        pik__zhb = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        pik__zhb.data = supn__ttl
        pik__zhb.indices = vcgs__itjca
        pik__zhb.has_global_dictionary = swwt__epcwo
        context.nrt.incref(builder, signature.args[0], supn__ttl)
        context.nrt.incref(builder, signature.args[1], vcgs__itjca)
        return pik__zhb._getvalue()
    qaz__waw = DictionaryArrayType(data_t)
    ckyil__soliq = qaz__waw(data_t, indices_t, types.bool_)
    return ckyil__soliq, codegen


@typeof_impl.register(pa.DictionaryArray)
def typeof_dict_value(val, c):
    if val.type.value_type == pa.string():
        return dict_str_arr_type


def to_pa_dict_arr(A):
    if isinstance(A, pa.DictionaryArray):
        return A
    for i in range(len(A)):
        if pd.isna(A[i]):
            A[i] = None
    return pa.array(A).dictionary_encode()


@unbox(DictionaryArrayType)
def unbox_dict_arr(typ, val, c):
    if bodo.hiframes.boxing._use_dict_str_type:
        okkwf__csaj = c.pyapi.unserialize(c.pyapi.serialize_object(
            to_pa_dict_arr))
        val = c.pyapi.call_function_objargs(okkwf__csaj, [val])
        c.pyapi.decref(okkwf__csaj)
    pik__zhb = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    pomt__akqf = c.pyapi.object_getattr_string(val, 'dictionary')
    lsh__llmef = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    hunf__svoov = c.pyapi.call_method(pomt__akqf, 'to_numpy', (lsh__llmef,))
    pik__zhb.data = c.unbox(typ.data, hunf__svoov).value
    amuil__vocpm = c.pyapi.object_getattr_string(val, 'indices')
    vzsjx__mdx = c.context.insert_const_string(c.builder.module, 'pandas')
    etei__gjia = c.pyapi.import_module_noblock(vzsjx__mdx)
    vppg__wea = c.pyapi.string_from_constant_string('Int32')
    mbt__sok = c.pyapi.call_method(etei__gjia, 'array', (amuil__vocpm,
        vppg__wea))
    pik__zhb.indices = c.unbox(dict_indices_arr_type, mbt__sok).value
    pik__zhb.has_global_dictionary = c.context.get_constant(types.bool_, False)
    c.pyapi.decref(pomt__akqf)
    c.pyapi.decref(lsh__llmef)
    c.pyapi.decref(hunf__svoov)
    c.pyapi.decref(amuil__vocpm)
    c.pyapi.decref(etei__gjia)
    c.pyapi.decref(vppg__wea)
    c.pyapi.decref(mbt__sok)
    if bodo.hiframes.boxing._use_dict_str_type:
        c.pyapi.decref(val)
    cbiwt__nvvp = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(pik__zhb._getvalue(), is_error=cbiwt__nvvp)


@box(DictionaryArrayType)
def box_dict_arr(typ, val, c):
    pik__zhb = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ == dict_str_arr_type:
        c.context.nrt.incref(c.builder, typ.data, pik__zhb.data)
        ftcr__vxa = c.box(typ.data, pik__zhb.data)
        jvfd__dezn = cgutils.create_struct_proxy(dict_indices_arr_type)(c.
            context, c.builder, pik__zhb.indices)
        rnkk__sgoy = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), c.
            pyapi.pyobj, lir.IntType(32).as_pointer(), lir.IntType(8).
            as_pointer()])
        sifgu__knu = cgutils.get_or_insert_function(c.builder.module,
            rnkk__sgoy, name='box_dict_str_array')
        zdj__qjoj = cgutils.create_struct_proxy(types.Array(types.int32, 1,
            'C'))(c.context, c.builder, jvfd__dezn.data)
        jxyva__askj = c.builder.extract_value(zdj__qjoj.shape, 0)
        ighbz__eacym = zdj__qjoj.data
        kgbu__xvsc = cgutils.create_struct_proxy(types.Array(types.int8, 1,
            'C'))(c.context, c.builder, jvfd__dezn.null_bitmap).data
        hunf__svoov = c.builder.call(sifgu__knu, [jxyva__askj, ftcr__vxa,
            ighbz__eacym, kgbu__xvsc])
        c.pyapi.decref(ftcr__vxa)
    else:
        vzsjx__mdx = c.context.insert_const_string(c.builder.module, 'pyarrow')
        oucj__lhgk = c.pyapi.import_module_noblock(vzsjx__mdx)
        raoq__wqxef = c.pyapi.object_getattr_string(oucj__lhgk,
            'DictionaryArray')
        c.context.nrt.incref(c.builder, typ.data, pik__zhb.data)
        ftcr__vxa = c.box(typ.data, pik__zhb.data)
        c.context.nrt.incref(c.builder, dict_indices_arr_type, pik__zhb.indices
            )
        amuil__vocpm = c.box(dict_indices_arr_type, pik__zhb.indices)
        tls__ymfrc = c.pyapi.call_method(raoq__wqxef, 'from_arrays', (
            amuil__vocpm, ftcr__vxa))
        lsh__llmef = c.pyapi.bool_from_bool(c.context.get_constant(types.
            bool_, False))
        hunf__svoov = c.pyapi.call_method(tls__ymfrc, 'to_numpy', (lsh__llmef,)
            )
        c.pyapi.decref(oucj__lhgk)
        c.pyapi.decref(ftcr__vxa)
        c.pyapi.decref(amuil__vocpm)
        c.pyapi.decref(raoq__wqxef)
        c.pyapi.decref(tls__ymfrc)
        c.pyapi.decref(lsh__llmef)
    c.context.nrt.decref(c.builder, typ, val)
    return hunf__svoov


@overload(len, no_unliteral=True)
def overload_dict_arr_len(A):
    if isinstance(A, DictionaryArrayType):
        return lambda A: len(A._indices)


@overload_attribute(DictionaryArrayType, 'shape')
def overload_dict_arr_shape(A):
    return lambda A: (len(A._indices),)


@overload_attribute(DictionaryArrayType, 'ndim')
def overload_dict_arr_ndim(A):
    return lambda A: 1


@overload_attribute(DictionaryArrayType, 'size')
def overload_dict_arr_size(A):
    return lambda A: len(A._indices)


@overload_method(DictionaryArrayType, 'tolist', no_unliteral=True)
def overload_dict_arr_tolist(A):
    return lambda A: list(A)


overload_method(DictionaryArrayType, 'astype', no_unliteral=True)(
    overload_str_arr_astype)


@overload_method(DictionaryArrayType, 'copy', no_unliteral=True)
def overload_dict_arr_copy(A):

    def copy_impl(A):
        return init_dict_arr(A._data.copy(), A._indices.copy(), A.
            _has_global_dictionary)
    return copy_impl


@overload_attribute(DictionaryArrayType, 'dtype')
def overload_dict_arr_dtype(A):
    return lambda A: A._data.dtype


@overload_attribute(DictionaryArrayType, 'nbytes')
def dict_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._indices.nbytes


@lower_constant(DictionaryArrayType)
def lower_constant_dict_arr(context, builder, typ, pyval):
    if bodo.hiframes.boxing._use_dict_str_type and isinstance(pyval, np.ndarray
        ):
        pyval = pa.array(pyval).dictionary_encode()
    ajpxz__hun = pyval.dictionary.to_numpy(False)
    xgb__yntk = pd.array(pyval.indices, 'Int32')
    ajpxz__hun = context.get_constant_generic(builder, typ.data, ajpxz__hun)
    xgb__yntk = context.get_constant_generic(builder, dict_indices_arr_type,
        xgb__yntk)
    ypmy__uhql = context.get_constant(types.bool_, False)
    rbp__twp = lir.Constant.literal_struct([ajpxz__hun, xgb__yntk, ypmy__uhql])
    return rbp__twp


@overload(operator.getitem, no_unliteral=True)
def dict_arr_getitem(A, ind):
    if not isinstance(A, DictionaryArrayType):
        return
    if isinstance(ind, types.Integer):

        def dict_arr_getitem_impl(A, ind):
            if bodo.libs.array_kernels.isna(A._indices, ind):
                return ''
            anv__kao = A._indices[ind]
            return A._data[anv__kao]
        return dict_arr_getitem_impl
    return lambda A, ind: init_dict_arr(A._data, A._indices[ind], A.
        _has_global_dictionary)


@overload_method(DictionaryArrayType, '_decode', no_unliteral=True)
def overload_dict_arr_decode(A):

    def impl(A):
        supn__ttl = A._data
        vcgs__itjca = A._indices
        jxyva__askj = len(vcgs__itjca)
        jco__isk = [get_str_arr_item_length(supn__ttl, i) for i in range(
            len(supn__ttl))]
        rek__fhd = 0
        for i in range(jxyva__askj):
            if not bodo.libs.array_kernels.isna(vcgs__itjca, i):
                rek__fhd += jco__isk[vcgs__itjca[i]]
        kag__alng = pre_alloc_string_array(jxyva__askj, rek__fhd)
        for i in range(jxyva__askj):
            if bodo.libs.array_kernels.isna(vcgs__itjca, i):
                bodo.libs.array_kernels.setna(kag__alng, i)
                continue
            ind = vcgs__itjca[i]
            if bodo.libs.array_kernels.isna(supn__ttl, ind):
                bodo.libs.array_kernels.setna(kag__alng, i)
                continue
            kag__alng[i] = supn__ttl[ind]
        return kag__alng
    return impl


@overload(operator.setitem)
def dict_arr_setitem(A, idx, val):
    if not isinstance(A, DictionaryArrayType):
        return
    raise_bodo_error(
        "DictionaryArrayType is read-only and doesn't support setitem yet")


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind(arr, val):
    anv__kao = -1
    supn__ttl = arr._data
    for i in range(len(supn__ttl)):
        if bodo.libs.array_kernels.isna(supn__ttl, i):
            continue
        if supn__ttl[i] == val:
            anv__kao = i
            break
    return anv__kao


@numba.njit(no_cpython_wrapper=True)
def dict_arr_eq(arr, val):
    jxyva__askj = len(arr)
    anv__kao = find_dict_ind(arr, val)
    if anv__kao == -1:
        return init_bool_array(np.full(jxyva__askj, False, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices == anv__kao


@numba.njit(no_cpython_wrapper=True)
def dict_arr_ne(arr, val):
    jxyva__askj = len(arr)
    anv__kao = find_dict_ind(arr, val)
    if anv__kao == -1:
        return init_bool_array(np.full(jxyva__askj, True, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices != anv__kao


def get_binary_op_overload(op, lhs, rhs):
    if op == operator.eq:
        if lhs == dict_str_arr_type and types.unliteral(rhs
            ) == bodo.string_type:
            return lambda lhs, rhs: bodo.libs.dict_arr_ext.dict_arr_eq(lhs, rhs
                )
        if rhs == dict_str_arr_type and types.unliteral(lhs
            ) == bodo.string_type:
            return lambda lhs, rhs: bodo.libs.dict_arr_ext.dict_arr_eq(rhs, lhs
                )
    if op == operator.ne:
        if lhs == dict_str_arr_type and types.unliteral(rhs
            ) == bodo.string_type:
            return lambda lhs, rhs: bodo.libs.dict_arr_ext.dict_arr_ne(lhs, rhs
                )
        if rhs == dict_str_arr_type and types.unliteral(lhs
            ) == bodo.string_type:
            return lambda lhs, rhs: bodo.libs.dict_arr_ext.dict_arr_ne(rhs, lhs
                )


def convert_dict_arr_to_int(arr, dtype):
    return arr


@overload(convert_dict_arr_to_int)
def convert_dict_arr_to_int_overload(arr, dtype):

    def impl(arr, dtype):
        uqepk__bqbji = arr._data
        bjq__yurwf = bodo.libs.int_arr_ext.alloc_int_array(len(uqepk__bqbji
            ), dtype)
        for hphen__byro in range(len(uqepk__bqbji)):
            if bodo.libs.array_kernels.isna(uqepk__bqbji, hphen__byro):
                bodo.libs.array_kernels.setna(bjq__yurwf, hphen__byro)
                continue
            bjq__yurwf[hphen__byro] = np.int64(uqepk__bqbji[hphen__byro])
        jxyva__askj = len(arr)
        vcgs__itjca = arr._indices
        kag__alng = bodo.libs.int_arr_ext.alloc_int_array(jxyva__askj, dtype)
        for i in range(jxyva__askj):
            if bodo.libs.array_kernels.isna(vcgs__itjca, i):
                bodo.libs.array_kernels.setna(kag__alng, i)
                continue
            kag__alng[i] = bjq__yurwf[vcgs__itjca[i]]
        return kag__alng
    return impl


def cat_dict_str(arrs, sep):
    pass


@overload(cat_dict_str)
def cat_dict_str_overload(arrs, sep):
    vqq__uvhtn = len(arrs)
    ngiux__hul = 'def impl(arrs, sep):\n'
    ngiux__hul += '  ind_map = {}\n'
    ngiux__hul += '  out_strs = []\n'
    ngiux__hul += '  n = len(arrs[0])\n'
    for i in range(vqq__uvhtn):
        ngiux__hul += f'  indices{i} = arrs[{i}]._indices\n'
    for i in range(vqq__uvhtn):
        ngiux__hul += f'  data{i} = arrs[{i}]._data\n'
    ngiux__hul += (
        '  out_indices = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)\n')
    ngiux__hul += '  for i in range(n):\n'
    asmu__ozr = ' or '.join([f'bodo.libs.array_kernels.isna(arrs[{i}], i)' for
        i in range(vqq__uvhtn)])
    ngiux__hul += f'    if {asmu__ozr}:\n'
    ngiux__hul += '      bodo.libs.array_kernels.setna(out_indices, i)\n'
    ngiux__hul += '      continue\n'
    for i in range(vqq__uvhtn):
        ngiux__hul += f'    ind{i} = indices{i}[i]\n'
    ovdky__wfpk = '(' + ', '.join(f'ind{i}' for i in range(vqq__uvhtn)) + ')'
    ngiux__hul += f'    if {ovdky__wfpk} not in ind_map:\n'
    ngiux__hul += '      out_ind = len(out_strs)\n'
    ngiux__hul += f'      ind_map[{ovdky__wfpk}] = out_ind\n'
    dod__dhey = "''" if is_overload_none(sep) else 'sep'
    zljl__lbnvn = ', '.join([f'data{i}[ind{i}]' for i in range(vqq__uvhtn)])
    ngiux__hul += f'      v = {dod__dhey}.join([{zljl__lbnvn}])\n'
    ngiux__hul += '      out_strs.append(v)\n'
    ngiux__hul += '    else:\n'
    ngiux__hul += f'      out_ind = ind_map[{ovdky__wfpk}]\n'
    ngiux__hul += '    out_indices[i] = out_ind\n'
    ngiux__hul += (
        '  out_str_arr = bodo.libs.str_arr_ext.str_arr_from_sequence(out_strs)\n'
        )
    ngiux__hul += """  return bodo.libs.dict_arr_ext.init_dict_arr(out_str_arr, out_indices, False)
"""
    vpwru__fexyn = {}
    exec(ngiux__hul, {'bodo': bodo, 'numba': numba, 'np': np}, vpwru__fexyn)
    impl = vpwru__fexyn['impl']
    return impl


@lower_cast(DictionaryArrayType, StringArrayType)
def cast_dict_str_arr_to_str_arr(context, builder, fromty, toty, val):
    if fromty != dict_str_arr_type:
        return
    keob__yqte = bodo.utils.typing.decode_if_dict_array_overload(fromty)
    ckyil__soliq = toty(fromty)
    jlf__xgglj = context.compile_internal(builder, keob__yqte, ckyil__soliq,
        (val,))
    return impl_ret_new_ref(context, builder, toty, jlf__xgglj)


@register_jitable
def str_replace(arr, pat, repl, flags, regex):
    ajpxz__hun = arr._data
    bdco__hmvs = len(ajpxz__hun)
    quua__dpvq = pre_alloc_string_array(bdco__hmvs, -1)
    if regex:
        nego__upb = re.compile(pat, flags)
        for i in range(bdco__hmvs):
            if bodo.libs.array_kernels.isna(ajpxz__hun, i):
                bodo.libs.array_kernels.setna(quua__dpvq, i)
                continue
            quua__dpvq[i] = nego__upb.sub(repl=repl, string=ajpxz__hun[i])
    else:
        for i in range(bdco__hmvs):
            if bodo.libs.array_kernels.isna(ajpxz__hun, i):
                bodo.libs.array_kernels.setna(quua__dpvq, i)
                continue
            quua__dpvq[i] = ajpxz__hun[i].replace(pat, repl)
    return init_dict_arr(quua__dpvq, arr._indices.copy(), arr.
        _has_global_dictionary)


@register_jitable
def str_startswith(arr, pat, na):
    pik__zhb = arr._data
    zryir__qdq = len(pik__zhb)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(zryir__qdq)
    for i in range(zryir__qdq):
        dict_arr_out[i] = pik__zhb[i].startswith(pat)
    xgb__yntk = arr._indices
    odey__iiylj = len(xgb__yntk)
    kag__alng = bodo.libs.bool_arr_ext.alloc_bool_array(odey__iiylj)
    for i in range(odey__iiylj):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(kag__alng, i)
        else:
            kag__alng[i] = dict_arr_out[xgb__yntk[i]]
    return kag__alng


@register_jitable
def str_endswith(arr, pat, na):
    pik__zhb = arr._data
    zryir__qdq = len(pik__zhb)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(zryir__qdq)
    for i in range(zryir__qdq):
        dict_arr_out[i] = pik__zhb[i].endswith(pat)
    xgb__yntk = arr._indices
    odey__iiylj = len(xgb__yntk)
    kag__alng = bodo.libs.bool_arr_ext.alloc_bool_array(odey__iiylj)
    for i in range(odey__iiylj):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(kag__alng, i)
        else:
            kag__alng[i] = dict_arr_out[xgb__yntk[i]]
    return kag__alng


@numba.njit
def str_series_contains_regex(arr, pat, case, flags, na, regex):
    pik__zhb = arr._data
    uve__lwfr = pd.Series(pik__zhb)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = uve__lwfr.array._str_contains(pat, case, flags, na,
            regex)
    xgb__yntk = arr._indices
    odey__iiylj = len(xgb__yntk)
    kag__alng = bodo.libs.bool_arr_ext.alloc_bool_array(odey__iiylj)
    for i in range(odey__iiylj):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(kag__alng, i)
        else:
            kag__alng[i] = dict_arr_out[xgb__yntk[i]]
    return kag__alng


@register_jitable
def str_contains_non_regex(arr, pat, case):
    pik__zhb = arr._data
    zryir__qdq = len(pik__zhb)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(zryir__qdq)
    if not case:
        xxu__zwn = pat.upper()
    for i in range(zryir__qdq):
        if case:
            dict_arr_out[i] = pat in pik__zhb[i]
        else:
            dict_arr_out[i] = xxu__zwn in pik__zhb[i].upper()
    xgb__yntk = arr._indices
    odey__iiylj = len(xgb__yntk)
    kag__alng = bodo.libs.bool_arr_ext.alloc_bool_array(odey__iiylj)
    for i in range(odey__iiylj):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(kag__alng, i)
        else:
            kag__alng[i] = dict_arr_out[xgb__yntk[i]]
    return kag__alng


@numba.njit
def str_match(arr, pat, case, flags, na):
    pik__zhb = arr._data
    xgb__yntk = arr._indices
    odey__iiylj = len(xgb__yntk)
    kag__alng = bodo.libs.bool_arr_ext.alloc_bool_array(odey__iiylj)
    uve__lwfr = pd.Series(pik__zhb)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = uve__lwfr.array._str_match(pat, case, flags, na)
    for i in range(odey__iiylj):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(kag__alng, i)
        else:
            kag__alng[i] = dict_arr_out[xgb__yntk[i]]
    return kag__alng


def create_simple_str2str_methods(func_name, func_args):
    ngiux__hul = f"""def str_{func_name}({', '.join(func_args)}):
    data_arr = arr._data
    n_data = len(data_arr)
    out_str_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_data, -1)
    for i in range(n_data):
        if bodo.libs.array_kernels.isna(data_arr, i):
            bodo.libs.array_kernels.setna(out_str_arr, i)
            continue
        out_str_arr[i] = data_arr[i].{func_name}({', '.join(func_args[1:])})
    return init_dict_arr(out_str_arr, arr._indices.copy(), arr._has_global_dictionary)
"""
    vpwru__fexyn = {}
    exec(ngiux__hul, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr}, vpwru__fexyn)
    return vpwru__fexyn[f'str_{func_name}']


def _register_simple_str2str_methods():
    rpn__ptvfu = {**dict.fromkeys(['capitalize', 'lower', 'swapcase',
        'title', 'upper'], ('arr',)), **dict.fromkeys(['lstrip', 'rstrip',
        'strip'], ('arr', 'to_strip')), **dict.fromkeys(['center', 'ljust',
        'rjust'], ('arr', 'width', 'fillchar')), **dict.fromkeys(['zfill'],
        ('arr', 'width'))}
    for func_name in rpn__ptvfu.keys():
        ahoc__wswlw = create_simple_str2str_methods(func_name, rpn__ptvfu[
            func_name])
        ahoc__wswlw = register_jitable(ahoc__wswlw)
        globals()[f'str_{func_name}'] = ahoc__wswlw


_register_simple_str2str_methods()


@register_jitable
def str_index(arr, sub, start, end):
    ajpxz__hun = arr._data
    xgb__yntk = arr._indices
    bdco__hmvs = len(ajpxz__hun)
    odey__iiylj = len(xgb__yntk)
    ciqv__umiz = bodo.libs.int_arr_ext.alloc_int_array(bdco__hmvs, np.int64)
    kag__alng = bodo.libs.int_arr_ext.alloc_int_array(odey__iiylj, np.int64)
    xjsjz__qgi = False
    for i in range(bdco__hmvs):
        if bodo.libs.array_kernels.isna(ajpxz__hun, i):
            bodo.libs.array_kernels.setna(ciqv__umiz, i)
        else:
            ciqv__umiz[i] = ajpxz__hun[i].find(sub, start, end)
    for i in range(odey__iiylj):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(ciqv__umiz, xgb__yntk[i]):
            bodo.libs.array_kernels.setna(kag__alng, i)
        else:
            kag__alng[i] = ciqv__umiz[xgb__yntk[i]]
            if kag__alng[i] == -1:
                xjsjz__qgi = True
    lwg__ttjdu = 'substring not found' if xjsjz__qgi else ''
    synchronize_error_njit('ValueError', lwg__ttjdu)
    return kag__alng


@register_jitable
def str_rindex(arr, sub, start, end):
    ajpxz__hun = arr._data
    xgb__yntk = arr._indices
    bdco__hmvs = len(ajpxz__hun)
    odey__iiylj = len(xgb__yntk)
    ciqv__umiz = bodo.libs.int_arr_ext.alloc_int_array(bdco__hmvs, np.int64)
    kag__alng = bodo.libs.int_arr_ext.alloc_int_array(odey__iiylj, np.int64)
    xjsjz__qgi = False
    for i in range(bdco__hmvs):
        if bodo.libs.array_kernels.isna(ajpxz__hun, i):
            bodo.libs.array_kernels.setna(ciqv__umiz, i)
        else:
            ciqv__umiz[i] = ajpxz__hun[i].rindex(sub, start, end)
    for i in range(odey__iiylj):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(ciqv__umiz, xgb__yntk[i]):
            bodo.libs.array_kernels.setna(kag__alng, i)
        else:
            kag__alng[i] = ciqv__umiz[xgb__yntk[i]]
            if kag__alng[i] == -1:
                xjsjz__qgi = True
    lwg__ttjdu = 'substring not found' if xjsjz__qgi else ''
    synchronize_error_njit('ValueError', lwg__ttjdu)
    return kag__alng


def create_find_methods(func_name):
    ngiux__hul = f"""def str_{func_name}(arr, sub, start, end):
  data_arr = arr._data
  indices_arr = arr._indices
  n_data = len(data_arr)
  n_indices = len(indices_arr)
  tmp_dict_arr = bodo.libs.int_arr_ext.alloc_int_array(n_data, np.int64)
  out_int_arr = bodo.libs.int_arr_ext.alloc_int_array(n_indices, np.int64)
  for i in range(n_data):
    if bodo.libs.array_kernels.isna(data_arr, i):
      bodo.libs.array_kernels.setna(tmp_dict_arr, i)
      continue
    tmp_dict_arr[i] = data_arr[i].{func_name}(sub, start, end)
  for i in range(n_indices):
    if bodo.libs.array_kernels.isna(indices_arr, i) or bodo.libs.array_kernels.isna(
      tmp_dict_arr, indices_arr[i]
    ):
      bodo.libs.array_kernels.setna(out_int_arr, i)
    else:
      out_int_arr[i] = tmp_dict_arr[indices_arr[i]]
  return out_int_arr"""
    vpwru__fexyn = {}
    exec(ngiux__hul, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr, 'np': np}, vpwru__fexyn)
    return vpwru__fexyn[f'str_{func_name}']


def _register_find_methods():
    eydd__jat = ['find', 'rfind']
    for func_name in eydd__jat:
        ahoc__wswlw = create_find_methods(func_name)
        ahoc__wswlw = register_jitable(ahoc__wswlw)
        globals()[f'str_{func_name}'] = ahoc__wswlw


_register_find_methods()


@register_jitable
def str_count(arr, pat, flags):
    ajpxz__hun = arr._data
    xgb__yntk = arr._indices
    bdco__hmvs = len(ajpxz__hun)
    odey__iiylj = len(xgb__yntk)
    ciqv__umiz = bodo.libs.int_arr_ext.alloc_int_array(bdco__hmvs, np.int64)
    mmrma__ruxmh = bodo.libs.int_arr_ext.alloc_int_array(odey__iiylj, np.int64)
    regex = re.compile(pat, flags)
    for i in range(bdco__hmvs):
        if bodo.libs.array_kernels.isna(ajpxz__hun, i):
            bodo.libs.array_kernels.setna(ciqv__umiz, i)
            continue
        ciqv__umiz[i] = bodo.libs.str_ext.str_findall_count(regex,
            ajpxz__hun[i])
    for i in range(odey__iiylj):
        if bodo.libs.array_kernels.isna(xgb__yntk, i
            ) or bodo.libs.array_kernels.isna(ciqv__umiz, xgb__yntk[i]):
            bodo.libs.array_kernels.setna(mmrma__ruxmh, i)
        else:
            mmrma__ruxmh[i] = ciqv__umiz[xgb__yntk[i]]
    return mmrma__ruxmh


@register_jitable
def str_len(arr):
    ajpxz__hun = arr._data
    xgb__yntk = arr._indices
    odey__iiylj = len(xgb__yntk)
    ciqv__umiz = bodo.libs.array_kernels.get_arr_lens(ajpxz__hun, False)
    mmrma__ruxmh = bodo.libs.int_arr_ext.alloc_int_array(odey__iiylj, np.int64)
    for i in range(odey__iiylj):
        if bodo.libs.array_kernels.isna(xgb__yntk, i
            ) or bodo.libs.array_kernels.isna(ciqv__umiz, xgb__yntk[i]):
            bodo.libs.array_kernels.setna(mmrma__ruxmh, i)
        else:
            mmrma__ruxmh[i] = ciqv__umiz[xgb__yntk[i]]
    return mmrma__ruxmh


@register_jitable
def str_slice(arr, start, stop, step):
    ajpxz__hun = arr._data
    bdco__hmvs = len(ajpxz__hun)
    quua__dpvq = bodo.libs.str_arr_ext.pre_alloc_string_array(bdco__hmvs, -1)
    for i in range(bdco__hmvs):
        if bodo.libs.array_kernels.isna(ajpxz__hun, i):
            bodo.libs.array_kernels.setna(quua__dpvq, i)
            continue
        quua__dpvq[i] = ajpxz__hun[i][start:stop:step]
    return init_dict_arr(quua__dpvq, arr._indices.copy(), arr.
        _has_global_dictionary)


@register_jitable
def str_get(arr, i):
    ajpxz__hun = arr._data
    xgb__yntk = arr._indices
    bdco__hmvs = len(ajpxz__hun)
    odey__iiylj = len(xgb__yntk)
    quua__dpvq = pre_alloc_string_array(bdco__hmvs, -1)
    kag__alng = pre_alloc_string_array(odey__iiylj, -1)
    for hphen__byro in range(bdco__hmvs):
        if bodo.libs.array_kernels.isna(ajpxz__hun, hphen__byro) or not -len(
            ajpxz__hun[hphen__byro]) <= i < len(ajpxz__hun[hphen__byro]):
            bodo.libs.array_kernels.setna(quua__dpvq, hphen__byro)
            continue
        quua__dpvq[hphen__byro] = ajpxz__hun[hphen__byro][i]
    for hphen__byro in range(odey__iiylj):
        if bodo.libs.array_kernels.isna(xgb__yntk, hphen__byro
            ) or bodo.libs.array_kernels.isna(quua__dpvq, xgb__yntk[
            hphen__byro]):
            bodo.libs.array_kernels.setna(kag__alng, hphen__byro)
            continue
        kag__alng[hphen__byro] = quua__dpvq[xgb__yntk[hphen__byro]]
    return kag__alng


@register_jitable
def str_repeat_int(arr, repeats):
    ajpxz__hun = arr._data
    bdco__hmvs = len(ajpxz__hun)
    quua__dpvq = pre_alloc_string_array(bdco__hmvs, -1)
    for i in range(bdco__hmvs):
        if bodo.libs.array_kernels.isna(ajpxz__hun, i):
            bodo.libs.array_kernels.setna(quua__dpvq, i)
            continue
        quua__dpvq[i] = ajpxz__hun[i] * repeats
    return init_dict_arr(quua__dpvq, arr._indices.copy(), arr.
        _has_global_dictionary)


def create_str2bool_methods(func_name):
    ngiux__hul = f"""def str_{func_name}(arr):
    data_arr = arr._data
    indices_arr = arr._indices
    n_data = len(data_arr)
    n_indices = len(indices_arr)
    out_dict_arr = bodo.libs.bool_arr_ext.alloc_bool_array(n_data)
    out_bool_arr = bodo.libs.bool_arr_ext.alloc_bool_array(n_indices)
    for i in range(n_data):
        if bodo.libs.array_kernels.isna(data_arr, i):
            bodo.libs.array_kernels.setna(out_dict_arr, i)
            continue
        out_dict_arr[i] = np.bool_(data_arr[i].{func_name}())
    for i in range(n_indices):
        if bodo.libs.array_kernels.isna(indices_arr, i) or bodo.libs.array_kernels.isna(
            data_arr, indices_arr[i]        ):
            bodo.libs.array_kernels.setna(out_bool_arr, i)
        else:
            out_bool_arr[i] = out_dict_arr[indices_arr[i]]
    return out_bool_arr"""
    vpwru__fexyn = {}
    exec(ngiux__hul, {'bodo': bodo, 'numba': numba, 'np': np,
        'init_dict_arr': init_dict_arr}, vpwru__fexyn)
    return vpwru__fexyn[f'str_{func_name}']


def _register_str2bool_methods():
    for func_name in bodo.hiframes.pd_series_ext.str2bool_methods:
        ahoc__wswlw = create_str2bool_methods(func_name)
        ahoc__wswlw = register_jitable(ahoc__wswlw)
        globals()[f'str_{func_name}'] = ahoc__wswlw


_register_str2bool_methods()


@register_jitable
def str_extract(arr, pat, flags, n_cols):
    ajpxz__hun = arr._data
    xgb__yntk = arr._indices
    bdco__hmvs = len(ajpxz__hun)
    odey__iiylj = len(xgb__yntk)
    regex = re.compile(pat, flags=flags)
    ftx__bzk = []
    for gqbb__oaae in range(n_cols):
        ftx__bzk.append(pre_alloc_string_array(bdco__hmvs, -1))
    pfs__vkg = bodo.libs.bool_arr_ext.alloc_bool_array(bdco__hmvs)
    ihxql__nyehl = xgb__yntk.copy()
    for i in range(bdco__hmvs):
        if bodo.libs.array_kernels.isna(ajpxz__hun, i):
            pfs__vkg[i] = True
            for hphen__byro in range(n_cols):
                bodo.libs.array_kernels.setna(ftx__bzk[hphen__byro], i)
            continue
        inmwl__kdw = regex.search(ajpxz__hun[i])
        if inmwl__kdw:
            pfs__vkg[i] = False
            dsp__tgi = inmwl__kdw.groups()
            for hphen__byro in range(n_cols):
                ftx__bzk[hphen__byro][i] = dsp__tgi[hphen__byro]
        else:
            pfs__vkg[i] = True
            for hphen__byro in range(n_cols):
                bodo.libs.array_kernels.setna(ftx__bzk[hphen__byro], i)
    for i in range(odey__iiylj):
        if pfs__vkg[ihxql__nyehl[i]]:
            bodo.libs.array_kernels.setna(ihxql__nyehl, i)
    emxv__pxj = [init_dict_arr(ftx__bzk[i], ihxql__nyehl.copy(), arr.
        _has_global_dictionary) for i in range(n_cols)]
    return emxv__pxj


def create_extractall_methods(is_multi_group):
    iibsb__qfk = '_multi' if is_multi_group else ''
    ngiux__hul = f"""def str_extractall{iibsb__qfk}(arr, regex, n_cols, index_arr):
    data_arr = arr._data
    indices_arr = arr._indices
    n_data = len(data_arr)
    n_indices = len(indices_arr)
    indices_count = [0 for _ in range(n_data)]
    for i in range(n_indices):
        if not bodo.libs.array_kernels.isna(indices_arr, i):
            indices_count[indices_arr[i]] += 1
    dict_group_count = []
    out_dict_len = out_ind_len = 0
    for i in range(n_data):
        if bodo.libs.array_kernels.isna(data_arr, i):
            continue
        m = regex.findall(data_arr[i])
        dict_group_count.append((out_dict_len, len(m)))
        out_dict_len += len(m)
        out_ind_len += indices_count[i] * len(m)
    out_dict_arr_list = []
    for _ in range(n_cols):
        out_dict_arr_list.append(pre_alloc_string_array(out_dict_len, -1))
    out_indices_arr = bodo.libs.int_arr_ext.alloc_int_array(out_ind_len, np.int32)
    out_ind_arr = bodo.utils.utils.alloc_type(out_ind_len, index_arr, (-1,))
    out_match_arr = np.empty(out_ind_len, np.int64)
    curr_ind = 0
    for i in range(n_data):
        if bodo.libs.array_kernels.isna(data_arr, i):
            continue
        m = regex.findall(data_arr[i])
        for s in m:
            for j in range(n_cols):
                out_dict_arr_list[j][curr_ind] = s{'[j]' if is_multi_group else ''}
            curr_ind += 1
    curr_ind = 0
    for i in range(n_indices):
        if bodo.libs.array_kernels.isna(indices_arr, i):
            continue
        n_rows = dict_group_count[indices_arr[i]][1]
        for k in range(n_rows):
            out_indices_arr[curr_ind] = dict_group_count[indices_arr[i]][0] + k
            out_ind_arr[curr_ind] = index_arr[i]
            out_match_arr[curr_ind] = k
            curr_ind += 1
    out_arr_list = [
        init_dict_arr(
            out_dict_arr_list[i], out_indices_arr.copy(), arr._has_global_dictionary
        )
        for i in range(n_cols)
    ]
    return (out_ind_arr, out_match_arr, out_arr_list) 
"""
    vpwru__fexyn = {}
    exec(ngiux__hul, {'bodo': bodo, 'numba': numba, 'np': np,
        'init_dict_arr': init_dict_arr, 'pre_alloc_string_array':
        pre_alloc_string_array}, vpwru__fexyn)
    return vpwru__fexyn[f'str_extractall{iibsb__qfk}']


def _register_extractall_methods():
    for is_multi_group in [True, False]:
        iibsb__qfk = '_multi' if is_multi_group else ''
        ahoc__wswlw = create_extractall_methods(is_multi_group)
        ahoc__wswlw = register_jitable(ahoc__wswlw)
        globals()[f'str_extractall{iibsb__qfk}'] = ahoc__wswlw


_register_extractall_methods()
