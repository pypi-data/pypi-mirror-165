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
        fclu__gvpdm = [('data', fe_type.data), ('indices',
            dict_indices_arr_type), ('has_global_dictionary', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, fclu__gvpdm)


make_attribute_wrapper(DictionaryArrayType, 'data', '_data')
make_attribute_wrapper(DictionaryArrayType, 'indices', '_indices')
make_attribute_wrapper(DictionaryArrayType, 'has_global_dictionary',
    '_has_global_dictionary')
lower_builtin('getiter', dict_str_arr_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_dict_arr(typingctx, data_t, indices_t, glob_dict_t=None):
    assert indices_t == dict_indices_arr_type, 'invalid indices type for dict array'

    def codegen(context, builder, signature, args):
        alzgf__bvkt, dxcl__dcc, igj__zuyy = args
        chn__iitvc = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        chn__iitvc.data = alzgf__bvkt
        chn__iitvc.indices = dxcl__dcc
        chn__iitvc.has_global_dictionary = igj__zuyy
        context.nrt.incref(builder, signature.args[0], alzgf__bvkt)
        context.nrt.incref(builder, signature.args[1], dxcl__dcc)
        return chn__iitvc._getvalue()
    rzpe__boolc = DictionaryArrayType(data_t)
    jzle__tcqdq = rzpe__boolc(data_t, indices_t, types.bool_)
    return jzle__tcqdq, codegen


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
        zmxhq__irxr = c.pyapi.unserialize(c.pyapi.serialize_object(
            to_pa_dict_arr))
        val = c.pyapi.call_function_objargs(zmxhq__irxr, [val])
        c.pyapi.decref(zmxhq__irxr)
    chn__iitvc = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ubr__xxx = c.pyapi.object_getattr_string(val, 'dictionary')
    udcj__grp = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_, 
        False))
    agq__fxp = c.pyapi.call_method(ubr__xxx, 'to_numpy', (udcj__grp,))
    chn__iitvc.data = c.unbox(typ.data, agq__fxp).value
    qqj__naemj = c.pyapi.object_getattr_string(val, 'indices')
    fdxvf__uemj = c.context.insert_const_string(c.builder.module, 'pandas')
    opf__wat = c.pyapi.import_module_noblock(fdxvf__uemj)
    put__aso = c.pyapi.string_from_constant_string('Int32')
    nxrsj__eoz = c.pyapi.call_method(opf__wat, 'array', (qqj__naemj, put__aso))
    chn__iitvc.indices = c.unbox(dict_indices_arr_type, nxrsj__eoz).value
    chn__iitvc.has_global_dictionary = c.context.get_constant(types.bool_, 
        False)
    c.pyapi.decref(ubr__xxx)
    c.pyapi.decref(udcj__grp)
    c.pyapi.decref(agq__fxp)
    c.pyapi.decref(qqj__naemj)
    c.pyapi.decref(opf__wat)
    c.pyapi.decref(put__aso)
    c.pyapi.decref(nxrsj__eoz)
    if bodo.hiframes.boxing._use_dict_str_type:
        c.pyapi.decref(val)
    uof__kkon = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(chn__iitvc._getvalue(), is_error=uof__kkon)


@box(DictionaryArrayType)
def box_dict_arr(typ, val, c):
    chn__iitvc = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ == dict_str_arr_type:
        c.context.nrt.incref(c.builder, typ.data, chn__iitvc.data)
        gqvob__xyw = c.box(typ.data, chn__iitvc.data)
        hjle__sdta = cgutils.create_struct_proxy(dict_indices_arr_type)(c.
            context, c.builder, chn__iitvc.indices)
        bbrse__hgk = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), c.
            pyapi.pyobj, lir.IntType(32).as_pointer(), lir.IntType(8).
            as_pointer()])
        bepwg__diwyt = cgutils.get_or_insert_function(c.builder.module,
            bbrse__hgk, name='box_dict_str_array')
        dvy__tplkf = cgutils.create_struct_proxy(types.Array(types.int32, 1,
            'C'))(c.context, c.builder, hjle__sdta.data)
        rmgji__lxnnh = c.builder.extract_value(dvy__tplkf.shape, 0)
        gonwd__cchc = dvy__tplkf.data
        fdxcc__xszcs = cgutils.create_struct_proxy(types.Array(types.int8, 
            1, 'C'))(c.context, c.builder, hjle__sdta.null_bitmap).data
        agq__fxp = c.builder.call(bepwg__diwyt, [rmgji__lxnnh, gqvob__xyw,
            gonwd__cchc, fdxcc__xszcs])
        c.pyapi.decref(gqvob__xyw)
    else:
        fdxvf__uemj = c.context.insert_const_string(c.builder.module, 'pyarrow'
            )
        gykff__tfu = c.pyapi.import_module_noblock(fdxvf__uemj)
        itt__eng = c.pyapi.object_getattr_string(gykff__tfu, 'DictionaryArray')
        c.context.nrt.incref(c.builder, typ.data, chn__iitvc.data)
        gqvob__xyw = c.box(typ.data, chn__iitvc.data)
        c.context.nrt.incref(c.builder, dict_indices_arr_type, chn__iitvc.
            indices)
        qqj__naemj = c.box(dict_indices_arr_type, chn__iitvc.indices)
        zlt__duao = c.pyapi.call_method(itt__eng, 'from_arrays', (
            qqj__naemj, gqvob__xyw))
        udcj__grp = c.pyapi.bool_from_bool(c.context.get_constant(types.
            bool_, False))
        agq__fxp = c.pyapi.call_method(zlt__duao, 'to_numpy', (udcj__grp,))
        c.pyapi.decref(gykff__tfu)
        c.pyapi.decref(gqvob__xyw)
        c.pyapi.decref(qqj__naemj)
        c.pyapi.decref(itt__eng)
        c.pyapi.decref(zlt__duao)
        c.pyapi.decref(udcj__grp)
    c.context.nrt.decref(c.builder, typ, val)
    return agq__fxp


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
    hzmf__mnkk = pyval.dictionary.to_numpy(False)
    zgac__horn = pd.array(pyval.indices, 'Int32')
    hzmf__mnkk = context.get_constant_generic(builder, typ.data, hzmf__mnkk)
    zgac__horn = context.get_constant_generic(builder,
        dict_indices_arr_type, zgac__horn)
    qnwnp__zox = context.get_constant(types.bool_, False)
    phj__jpva = lir.Constant.literal_struct([hzmf__mnkk, zgac__horn,
        qnwnp__zox])
    return phj__jpva


@overload(operator.getitem, no_unliteral=True)
def dict_arr_getitem(A, ind):
    if not isinstance(A, DictionaryArrayType):
        return
    if isinstance(ind, types.Integer):

        def dict_arr_getitem_impl(A, ind):
            if bodo.libs.array_kernels.isna(A._indices, ind):
                return ''
            dih__ued = A._indices[ind]
            return A._data[dih__ued]
        return dict_arr_getitem_impl
    return lambda A, ind: init_dict_arr(A._data, A._indices[ind], A.
        _has_global_dictionary)


@overload_method(DictionaryArrayType, '_decode', no_unliteral=True)
def overload_dict_arr_decode(A):

    def impl(A):
        alzgf__bvkt = A._data
        dxcl__dcc = A._indices
        rmgji__lxnnh = len(dxcl__dcc)
        jxlym__mrhmp = [get_str_arr_item_length(alzgf__bvkt, i) for i in
            range(len(alzgf__bvkt))]
        edq__ojwqj = 0
        for i in range(rmgji__lxnnh):
            if not bodo.libs.array_kernels.isna(dxcl__dcc, i):
                edq__ojwqj += jxlym__mrhmp[dxcl__dcc[i]]
        taw__rjp = pre_alloc_string_array(rmgji__lxnnh, edq__ojwqj)
        for i in range(rmgji__lxnnh):
            if bodo.libs.array_kernels.isna(dxcl__dcc, i):
                bodo.libs.array_kernels.setna(taw__rjp, i)
                continue
            ind = dxcl__dcc[i]
            if bodo.libs.array_kernels.isna(alzgf__bvkt, ind):
                bodo.libs.array_kernels.setna(taw__rjp, i)
                continue
            taw__rjp[i] = alzgf__bvkt[ind]
        return taw__rjp
    return impl


@overload(operator.setitem)
def dict_arr_setitem(A, idx, val):
    if not isinstance(A, DictionaryArrayType):
        return
    raise_bodo_error(
        "DictionaryArrayType is read-only and doesn't support setitem yet")


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind(arr, val):
    dih__ued = -1
    alzgf__bvkt = arr._data
    for i in range(len(alzgf__bvkt)):
        if bodo.libs.array_kernels.isna(alzgf__bvkt, i):
            continue
        if alzgf__bvkt[i] == val:
            dih__ued = i
            break
    return dih__ued


@numba.njit(no_cpython_wrapper=True)
def dict_arr_eq(arr, val):
    rmgji__lxnnh = len(arr)
    dih__ued = find_dict_ind(arr, val)
    if dih__ued == -1:
        return init_bool_array(np.full(rmgji__lxnnh, False, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices == dih__ued


@numba.njit(no_cpython_wrapper=True)
def dict_arr_ne(arr, val):
    rmgji__lxnnh = len(arr)
    dih__ued = find_dict_ind(arr, val)
    if dih__ued == -1:
        return init_bool_array(np.full(rmgji__lxnnh, True, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices != dih__ued


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
        ghv__nudyx = arr._data
        jflui__xujd = bodo.libs.int_arr_ext.alloc_int_array(len(ghv__nudyx),
            dtype)
        for gnrp__jncxe in range(len(ghv__nudyx)):
            if bodo.libs.array_kernels.isna(ghv__nudyx, gnrp__jncxe):
                bodo.libs.array_kernels.setna(jflui__xujd, gnrp__jncxe)
                continue
            jflui__xujd[gnrp__jncxe] = np.int64(ghv__nudyx[gnrp__jncxe])
        rmgji__lxnnh = len(arr)
        dxcl__dcc = arr._indices
        taw__rjp = bodo.libs.int_arr_ext.alloc_int_array(rmgji__lxnnh, dtype)
        for i in range(rmgji__lxnnh):
            if bodo.libs.array_kernels.isna(dxcl__dcc, i):
                bodo.libs.array_kernels.setna(taw__rjp, i)
                continue
            taw__rjp[i] = jflui__xujd[dxcl__dcc[i]]
        return taw__rjp
    return impl


def cat_dict_str(arrs, sep):
    pass


@overload(cat_dict_str)
def cat_dict_str_overload(arrs, sep):
    kir__qqz = len(arrs)
    ljun__lprn = 'def impl(arrs, sep):\n'
    ljun__lprn += '  ind_map = {}\n'
    ljun__lprn += '  out_strs = []\n'
    ljun__lprn += '  n = len(arrs[0])\n'
    for i in range(kir__qqz):
        ljun__lprn += f'  indices{i} = arrs[{i}]._indices\n'
    for i in range(kir__qqz):
        ljun__lprn += f'  data{i} = arrs[{i}]._data\n'
    ljun__lprn += (
        '  out_indices = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)\n')
    ljun__lprn += '  for i in range(n):\n'
    hfb__nker = ' or '.join([f'bodo.libs.array_kernels.isna(arrs[{i}], i)' for
        i in range(kir__qqz)])
    ljun__lprn += f'    if {hfb__nker}:\n'
    ljun__lprn += '      bodo.libs.array_kernels.setna(out_indices, i)\n'
    ljun__lprn += '      continue\n'
    for i in range(kir__qqz):
        ljun__lprn += f'    ind{i} = indices{i}[i]\n'
    gcaj__tszyb = '(' + ', '.join(f'ind{i}' for i in range(kir__qqz)) + ')'
    ljun__lprn += f'    if {gcaj__tszyb} not in ind_map:\n'
    ljun__lprn += '      out_ind = len(out_strs)\n'
    ljun__lprn += f'      ind_map[{gcaj__tszyb}] = out_ind\n'
    xqnyk__ohu = "''" if is_overload_none(sep) else 'sep'
    wtn__uyc = ', '.join([f'data{i}[ind{i}]' for i in range(kir__qqz)])
    ljun__lprn += f'      v = {xqnyk__ohu}.join([{wtn__uyc}])\n'
    ljun__lprn += '      out_strs.append(v)\n'
    ljun__lprn += '    else:\n'
    ljun__lprn += f'      out_ind = ind_map[{gcaj__tszyb}]\n'
    ljun__lprn += '    out_indices[i] = out_ind\n'
    ljun__lprn += (
        '  out_str_arr = bodo.libs.str_arr_ext.str_arr_from_sequence(out_strs)\n'
        )
    ljun__lprn += """  return bodo.libs.dict_arr_ext.init_dict_arr(out_str_arr, out_indices, False)
"""
    guzba__zubv = {}
    exec(ljun__lprn, {'bodo': bodo, 'numba': numba, 'np': np}, guzba__zubv)
    impl = guzba__zubv['impl']
    return impl


@lower_cast(DictionaryArrayType, StringArrayType)
def cast_dict_str_arr_to_str_arr(context, builder, fromty, toty, val):
    if fromty != dict_str_arr_type:
        return
    tfyt__ofgfk = bodo.utils.typing.decode_if_dict_array_overload(fromty)
    jzle__tcqdq = toty(fromty)
    hubzp__afrx = context.compile_internal(builder, tfyt__ofgfk,
        jzle__tcqdq, (val,))
    return impl_ret_new_ref(context, builder, toty, hubzp__afrx)


@register_jitable
def str_replace(arr, pat, repl, flags, regex):
    hzmf__mnkk = arr._data
    giz__ajrq = len(hzmf__mnkk)
    ppsbk__udxpa = pre_alloc_string_array(giz__ajrq, -1)
    if regex:
        royok__bhg = re.compile(pat, flags)
        for i in range(giz__ajrq):
            if bodo.libs.array_kernels.isna(hzmf__mnkk, i):
                bodo.libs.array_kernels.setna(ppsbk__udxpa, i)
                continue
            ppsbk__udxpa[i] = royok__bhg.sub(repl=repl, string=hzmf__mnkk[i])
    else:
        for i in range(giz__ajrq):
            if bodo.libs.array_kernels.isna(hzmf__mnkk, i):
                bodo.libs.array_kernels.setna(ppsbk__udxpa, i)
                continue
            ppsbk__udxpa[i] = hzmf__mnkk[i].replace(pat, repl)
    return init_dict_arr(ppsbk__udxpa, arr._indices.copy(), arr.
        _has_global_dictionary)


@register_jitable
def str_startswith(arr, pat, na):
    chn__iitvc = arr._data
    xcqq__aeg = len(chn__iitvc)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(xcqq__aeg)
    for i in range(xcqq__aeg):
        dict_arr_out[i] = chn__iitvc[i].startswith(pat)
    zgac__horn = arr._indices
    czxav__nslm = len(zgac__horn)
    taw__rjp = bodo.libs.bool_arr_ext.alloc_bool_array(czxav__nslm)
    for i in range(czxav__nslm):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(taw__rjp, i)
        else:
            taw__rjp[i] = dict_arr_out[zgac__horn[i]]
    return taw__rjp


@register_jitable
def str_endswith(arr, pat, na):
    chn__iitvc = arr._data
    xcqq__aeg = len(chn__iitvc)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(xcqq__aeg)
    for i in range(xcqq__aeg):
        dict_arr_out[i] = chn__iitvc[i].endswith(pat)
    zgac__horn = arr._indices
    czxav__nslm = len(zgac__horn)
    taw__rjp = bodo.libs.bool_arr_ext.alloc_bool_array(czxav__nslm)
    for i in range(czxav__nslm):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(taw__rjp, i)
        else:
            taw__rjp[i] = dict_arr_out[zgac__horn[i]]
    return taw__rjp


@numba.njit
def str_series_contains_regex(arr, pat, case, flags, na, regex):
    chn__iitvc = arr._data
    gdl__fjf = pd.Series(chn__iitvc)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = gdl__fjf.array._str_contains(pat, case, flags, na, regex
            )
    zgac__horn = arr._indices
    czxav__nslm = len(zgac__horn)
    taw__rjp = bodo.libs.bool_arr_ext.alloc_bool_array(czxav__nslm)
    for i in range(czxav__nslm):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(taw__rjp, i)
        else:
            taw__rjp[i] = dict_arr_out[zgac__horn[i]]
    return taw__rjp


@register_jitable
def str_contains_non_regex(arr, pat, case):
    chn__iitvc = arr._data
    xcqq__aeg = len(chn__iitvc)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(xcqq__aeg)
    if not case:
        huy__zci = pat.upper()
    for i in range(xcqq__aeg):
        if case:
            dict_arr_out[i] = pat in chn__iitvc[i]
        else:
            dict_arr_out[i] = huy__zci in chn__iitvc[i].upper()
    zgac__horn = arr._indices
    czxav__nslm = len(zgac__horn)
    taw__rjp = bodo.libs.bool_arr_ext.alloc_bool_array(czxav__nslm)
    for i in range(czxav__nslm):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(taw__rjp, i)
        else:
            taw__rjp[i] = dict_arr_out[zgac__horn[i]]
    return taw__rjp


@numba.njit
def str_match(arr, pat, case, flags, na):
    chn__iitvc = arr._data
    zgac__horn = arr._indices
    czxav__nslm = len(zgac__horn)
    taw__rjp = bodo.libs.bool_arr_ext.alloc_bool_array(czxav__nslm)
    gdl__fjf = pd.Series(chn__iitvc)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = gdl__fjf.array._str_match(pat, case, flags, na)
    for i in range(czxav__nslm):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(taw__rjp, i)
        else:
            taw__rjp[i] = dict_arr_out[zgac__horn[i]]
    return taw__rjp


def create_simple_str2str_methods(func_name, func_args):
    ljun__lprn = f"""def str_{func_name}({', '.join(func_args)}):
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
    guzba__zubv = {}
    exec(ljun__lprn, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr}, guzba__zubv)
    return guzba__zubv[f'str_{func_name}']


def _register_simple_str2str_methods():
    zahi__efu = {**dict.fromkeys(['capitalize', 'lower', 'swapcase',
        'title', 'upper'], ('arr',)), **dict.fromkeys(['lstrip', 'rstrip',
        'strip'], ('arr', 'to_strip')), **dict.fromkeys(['center', 'ljust',
        'rjust'], ('arr', 'width', 'fillchar')), **dict.fromkeys(['zfill'],
        ('arr', 'width'))}
    for func_name in zahi__efu.keys():
        vkmv__nqckj = create_simple_str2str_methods(func_name, zahi__efu[
            func_name])
        vkmv__nqckj = register_jitable(vkmv__nqckj)
        globals()[f'str_{func_name}'] = vkmv__nqckj


_register_simple_str2str_methods()


@register_jitable
def str_index(arr, sub, start, end):
    hzmf__mnkk = arr._data
    zgac__horn = arr._indices
    giz__ajrq = len(hzmf__mnkk)
    czxav__nslm = len(zgac__horn)
    higzs__izuw = bodo.libs.int_arr_ext.alloc_int_array(giz__ajrq, np.int64)
    taw__rjp = bodo.libs.int_arr_ext.alloc_int_array(czxav__nslm, np.int64)
    elhl__ydtxo = False
    for i in range(giz__ajrq):
        if bodo.libs.array_kernels.isna(hzmf__mnkk, i):
            bodo.libs.array_kernels.setna(higzs__izuw, i)
        else:
            higzs__izuw[i] = hzmf__mnkk[i].find(sub, start, end)
    for i in range(czxav__nslm):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(higzs__izuw, zgac__horn[i]):
            bodo.libs.array_kernels.setna(taw__rjp, i)
        else:
            taw__rjp[i] = higzs__izuw[zgac__horn[i]]
            if taw__rjp[i] == -1:
                elhl__ydtxo = True
    rrgq__htquz = 'substring not found' if elhl__ydtxo else ''
    synchronize_error_njit('ValueError', rrgq__htquz)
    return taw__rjp


@register_jitable
def str_rindex(arr, sub, start, end):
    hzmf__mnkk = arr._data
    zgac__horn = arr._indices
    giz__ajrq = len(hzmf__mnkk)
    czxav__nslm = len(zgac__horn)
    higzs__izuw = bodo.libs.int_arr_ext.alloc_int_array(giz__ajrq, np.int64)
    taw__rjp = bodo.libs.int_arr_ext.alloc_int_array(czxav__nslm, np.int64)
    elhl__ydtxo = False
    for i in range(giz__ajrq):
        if bodo.libs.array_kernels.isna(hzmf__mnkk, i):
            bodo.libs.array_kernels.setna(higzs__izuw, i)
        else:
            higzs__izuw[i] = hzmf__mnkk[i].rindex(sub, start, end)
    for i in range(czxav__nslm):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(higzs__izuw, zgac__horn[i]):
            bodo.libs.array_kernels.setna(taw__rjp, i)
        else:
            taw__rjp[i] = higzs__izuw[zgac__horn[i]]
            if taw__rjp[i] == -1:
                elhl__ydtxo = True
    rrgq__htquz = 'substring not found' if elhl__ydtxo else ''
    synchronize_error_njit('ValueError', rrgq__htquz)
    return taw__rjp


def create_find_methods(func_name):
    ljun__lprn = f"""def str_{func_name}(arr, sub, start, end):
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
    guzba__zubv = {}
    exec(ljun__lprn, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr, 'np': np}, guzba__zubv)
    return guzba__zubv[f'str_{func_name}']


def _register_find_methods():
    szmbj__ward = ['find', 'rfind']
    for func_name in szmbj__ward:
        vkmv__nqckj = create_find_methods(func_name)
        vkmv__nqckj = register_jitable(vkmv__nqckj)
        globals()[f'str_{func_name}'] = vkmv__nqckj


_register_find_methods()


@register_jitable
def str_count(arr, pat, flags):
    hzmf__mnkk = arr._data
    zgac__horn = arr._indices
    giz__ajrq = len(hzmf__mnkk)
    czxav__nslm = len(zgac__horn)
    higzs__izuw = bodo.libs.int_arr_ext.alloc_int_array(giz__ajrq, np.int64)
    qpd__jjom = bodo.libs.int_arr_ext.alloc_int_array(czxav__nslm, np.int64)
    regex = re.compile(pat, flags)
    for i in range(giz__ajrq):
        if bodo.libs.array_kernels.isna(hzmf__mnkk, i):
            bodo.libs.array_kernels.setna(higzs__izuw, i)
            continue
        higzs__izuw[i] = bodo.libs.str_ext.str_findall_count(regex,
            hzmf__mnkk[i])
    for i in range(czxav__nslm):
        if bodo.libs.array_kernels.isna(zgac__horn, i
            ) or bodo.libs.array_kernels.isna(higzs__izuw, zgac__horn[i]):
            bodo.libs.array_kernels.setna(qpd__jjom, i)
        else:
            qpd__jjom[i] = higzs__izuw[zgac__horn[i]]
    return qpd__jjom


@register_jitable
def str_len(arr):
    hzmf__mnkk = arr._data
    zgac__horn = arr._indices
    czxav__nslm = len(zgac__horn)
    higzs__izuw = bodo.libs.array_kernels.get_arr_lens(hzmf__mnkk, False)
    qpd__jjom = bodo.libs.int_arr_ext.alloc_int_array(czxav__nslm, np.int64)
    for i in range(czxav__nslm):
        if bodo.libs.array_kernels.isna(zgac__horn, i
            ) or bodo.libs.array_kernels.isna(higzs__izuw, zgac__horn[i]):
            bodo.libs.array_kernels.setna(qpd__jjom, i)
        else:
            qpd__jjom[i] = higzs__izuw[zgac__horn[i]]
    return qpd__jjom


@register_jitable
def str_slice(arr, start, stop, step):
    hzmf__mnkk = arr._data
    giz__ajrq = len(hzmf__mnkk)
    ppsbk__udxpa = bodo.libs.str_arr_ext.pre_alloc_string_array(giz__ajrq, -1)
    for i in range(giz__ajrq):
        if bodo.libs.array_kernels.isna(hzmf__mnkk, i):
            bodo.libs.array_kernels.setna(ppsbk__udxpa, i)
            continue
        ppsbk__udxpa[i] = hzmf__mnkk[i][start:stop:step]
    return init_dict_arr(ppsbk__udxpa, arr._indices.copy(), arr.
        _has_global_dictionary)


@register_jitable
def str_get(arr, i):
    hzmf__mnkk = arr._data
    zgac__horn = arr._indices
    giz__ajrq = len(hzmf__mnkk)
    czxav__nslm = len(zgac__horn)
    ppsbk__udxpa = pre_alloc_string_array(giz__ajrq, -1)
    taw__rjp = pre_alloc_string_array(czxav__nslm, -1)
    for gnrp__jncxe in range(giz__ajrq):
        if bodo.libs.array_kernels.isna(hzmf__mnkk, gnrp__jncxe) or not -len(
            hzmf__mnkk[gnrp__jncxe]) <= i < len(hzmf__mnkk[gnrp__jncxe]):
            bodo.libs.array_kernels.setna(ppsbk__udxpa, gnrp__jncxe)
            continue
        ppsbk__udxpa[gnrp__jncxe] = hzmf__mnkk[gnrp__jncxe][i]
    for gnrp__jncxe in range(czxav__nslm):
        if bodo.libs.array_kernels.isna(zgac__horn, gnrp__jncxe
            ) or bodo.libs.array_kernels.isna(ppsbk__udxpa, zgac__horn[
            gnrp__jncxe]):
            bodo.libs.array_kernels.setna(taw__rjp, gnrp__jncxe)
            continue
        taw__rjp[gnrp__jncxe] = ppsbk__udxpa[zgac__horn[gnrp__jncxe]]
    return taw__rjp


@register_jitable
def str_repeat_int(arr, repeats):
    hzmf__mnkk = arr._data
    giz__ajrq = len(hzmf__mnkk)
    ppsbk__udxpa = pre_alloc_string_array(giz__ajrq, -1)
    for i in range(giz__ajrq):
        if bodo.libs.array_kernels.isna(hzmf__mnkk, i):
            bodo.libs.array_kernels.setna(ppsbk__udxpa, i)
            continue
        ppsbk__udxpa[i] = hzmf__mnkk[i] * repeats
    return init_dict_arr(ppsbk__udxpa, arr._indices.copy(), arr.
        _has_global_dictionary)


def create_str2bool_methods(func_name):
    ljun__lprn = f"""def str_{func_name}(arr):
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
    guzba__zubv = {}
    exec(ljun__lprn, {'bodo': bodo, 'numba': numba, 'np': np,
        'init_dict_arr': init_dict_arr}, guzba__zubv)
    return guzba__zubv[f'str_{func_name}']


def _register_str2bool_methods():
    for func_name in bodo.hiframes.pd_series_ext.str2bool_methods:
        vkmv__nqckj = create_str2bool_methods(func_name)
        vkmv__nqckj = register_jitable(vkmv__nqckj)
        globals()[f'str_{func_name}'] = vkmv__nqckj


_register_str2bool_methods()


@register_jitable
def str_extract(arr, pat, flags, n_cols):
    hzmf__mnkk = arr._data
    zgac__horn = arr._indices
    giz__ajrq = len(hzmf__mnkk)
    czxav__nslm = len(zgac__horn)
    regex = re.compile(pat, flags=flags)
    yauv__nwbrn = []
    for itb__xobg in range(n_cols):
        yauv__nwbrn.append(pre_alloc_string_array(giz__ajrq, -1))
    yykpt__thyb = bodo.libs.bool_arr_ext.alloc_bool_array(giz__ajrq)
    ijxq__vyghf = zgac__horn.copy()
    for i in range(giz__ajrq):
        if bodo.libs.array_kernels.isna(hzmf__mnkk, i):
            yykpt__thyb[i] = True
            for gnrp__jncxe in range(n_cols):
                bodo.libs.array_kernels.setna(yauv__nwbrn[gnrp__jncxe], i)
            continue
        rjpp__iao = regex.search(hzmf__mnkk[i])
        if rjpp__iao:
            yykpt__thyb[i] = False
            yzd__qfv = rjpp__iao.groups()
            for gnrp__jncxe in range(n_cols):
                yauv__nwbrn[gnrp__jncxe][i] = yzd__qfv[gnrp__jncxe]
        else:
            yykpt__thyb[i] = True
            for gnrp__jncxe in range(n_cols):
                bodo.libs.array_kernels.setna(yauv__nwbrn[gnrp__jncxe], i)
    for i in range(czxav__nslm):
        if yykpt__thyb[ijxq__vyghf[i]]:
            bodo.libs.array_kernels.setna(ijxq__vyghf, i)
    mwalw__rnj = [init_dict_arr(yauv__nwbrn[i], ijxq__vyghf.copy(), arr.
        _has_global_dictionary) for i in range(n_cols)]
    return mwalw__rnj


def create_extractall_methods(is_multi_group):
    kqsxb__xhtuz = '_multi' if is_multi_group else ''
    ljun__lprn = f"""def str_extractall{kqsxb__xhtuz}(arr, regex, n_cols, index_arr):
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
    guzba__zubv = {}
    exec(ljun__lprn, {'bodo': bodo, 'numba': numba, 'np': np,
        'init_dict_arr': init_dict_arr, 'pre_alloc_string_array':
        pre_alloc_string_array}, guzba__zubv)
    return guzba__zubv[f'str_extractall{kqsxb__xhtuz}']


def _register_extractall_methods():
    for is_multi_group in [True, False]:
        kqsxb__xhtuz = '_multi' if is_multi_group else ''
        vkmv__nqckj = create_extractall_methods(is_multi_group)
        vkmv__nqckj = register_jitable(vkmv__nqckj)
        globals()[f'str_extractall{kqsxb__xhtuz}'] = vkmv__nqckj


_register_extractall_methods()
