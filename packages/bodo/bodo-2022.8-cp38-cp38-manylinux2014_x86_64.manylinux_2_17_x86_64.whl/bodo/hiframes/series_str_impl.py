"""
Support for Series.str methods
"""
import operator
import re
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import StringIndexType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.split_impl import get_split_view_data_ptr, get_split_view_index, string_array_split_view_type
from bodo.libs.array import get_search_regex
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.str_arr_ext import get_utf8_size, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import str_findall_count
from bodo.utils.typing import BodoError, create_unsupported_overload, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_str_len, is_bin_arr_type, is_list_like_index_type, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true, is_str_arr_type, raise_bodo_error
from bodo.utils.utils import synchronize_error_njit


class SeriesStrMethodType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        sdrnx__qlryy = 'SeriesStrMethodType({})'.format(stype)
        super(SeriesStrMethodType, self).__init__(sdrnx__qlryy)


@register_model(SeriesStrMethodType)
class SeriesStrModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        sxnoz__mtk = [('obj', fe_type.stype)]
        super(SeriesStrModel, self).__init__(dmm, fe_type, sxnoz__mtk)


make_attribute_wrapper(SeriesStrMethodType, 'obj', '_obj')


@intrinsic
def init_series_str_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        byf__wreh, = args
        tyyf__yxr = signature.return_type
        fls__njsld = cgutils.create_struct_proxy(tyyf__yxr)(context, builder)
        fls__njsld.obj = byf__wreh
        context.nrt.incref(builder, signature.args[0], byf__wreh)
        return fls__njsld._getvalue()
    return SeriesStrMethodType(obj)(obj), codegen


def str_arg_check(func_name, arg_name, arg):
    if not isinstance(arg, types.UnicodeType) and not is_overload_constant_str(
        arg):
        raise_bodo_error(
            "Series.str.{}(): parameter '{}' expected a string object, not {}"
            .format(func_name, arg_name, arg))


def int_arg_check(func_name, arg_name, arg):
    if not isinstance(arg, types.Integer) and not is_overload_constant_int(arg
        ):
        raise BodoError(
            "Series.str.{}(): parameter '{}' expected an int object, not {}"
            .format(func_name, arg_name, arg))


def not_supported_arg_check(func_name, arg_name, arg, defval):
    if arg_name == 'na':
        if not isinstance(arg, types.Omitted) and (not isinstance(arg,
            float) or not np.isnan(arg)):
            raise BodoError(
                "Series.str.{}(): parameter '{}' is not supported, default: np.nan"
                .format(func_name, arg_name))
    elif not isinstance(arg, types.Omitted) and arg != defval:
        raise BodoError(
            "Series.str.{}(): parameter '{}' is not supported, default: {}"
            .format(func_name, arg_name, defval))


def common_validate_padding(func_name, width, fillchar):
    if is_overload_constant_str(fillchar):
        if get_overload_const_str_len(fillchar) != 1:
            raise BodoError(
                'Series.str.{}(): fillchar must be a character, not str'.
                format(func_name))
    elif not isinstance(fillchar, types.UnicodeType):
        raise BodoError('Series.str.{}(): fillchar must be a character, not {}'
            .format(func_name, fillchar))
    int_arg_check(func_name, 'width', width)


@overload_attribute(SeriesType, 'str')
def overload_series_str(S):
    if not (is_str_arr_type(S.data) or S.data ==
        string_array_split_view_type or isinstance(S.data,
        ArrayItemArrayType) or is_bin_arr_type(S.data)):
        raise_bodo_error(
            'Series.str: input should be a series of string/binary or arrays')
    return lambda S: bodo.hiframes.series_str_impl.init_series_str_method(S)


@overload_method(SeriesStrMethodType, 'len', inline='always', no_unliteral=True
    )
def overload_str_method_len(S_str):
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_len_dict_impl(S_str):
            S = S_str._obj
            nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
            yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
            sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_len(nswor__aogqk)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                yqo__lqg, sdrnx__qlryy)
        return _str_len_dict_impl

    def impl(S_str):
        S = S_str._obj
        nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
        yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
        sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.array_kernels.get_arr_lens(nswor__aogqk, False)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, yqo__lqg,
            sdrnx__qlryy)
    return impl


@overload_method(SeriesStrMethodType, 'split', inline='always',
    no_unliteral=True)
def overload_str_method_split(S_str, pat=None, n=-1, expand=False):
    if not is_overload_none(pat):
        str_arg_check('split', 'pat', pat)
    int_arg_check('split', 'n', n)
    not_supported_arg_check('split', 'expand', expand, False)
    if is_overload_constant_str(pat) and len(get_overload_const_str(pat)
        ) == 1 and get_overload_const_str(pat).isascii(
        ) and is_overload_constant_int(n) and get_overload_const_int(n
        ) == -1 and S_str.stype.data == string_array_type:

        def _str_split_view_impl(S_str, pat=None, n=-1, expand=False):
            S = S_str._obj
            nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
            yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
            sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.hiframes.split_impl.compute_split_view(nswor__aogqk,
                pat)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                yqo__lqg, sdrnx__qlryy)
        return _str_split_view_impl

    def _str_split_impl(S_str, pat=None, n=-1, expand=False):
        S = S_str._obj
        nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
        yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
        sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.str_ext.str_split(nswor__aogqk, pat, n)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, yqo__lqg,
            sdrnx__qlryy)
    return _str_split_impl


@overload_method(SeriesStrMethodType, 'get', no_unliteral=True)
def overload_str_method_get(S_str, i):
    bpp__hlbx = S_str.stype.data
    if (bpp__hlbx != string_array_split_view_type and not is_str_arr_type(
        bpp__hlbx)) and not isinstance(bpp__hlbx, ArrayItemArrayType):
        raise_bodo_error(
            'Series.str.get(): only supports input type of Series(array(item)) and Series(str)'
            )
    int_arg_check('get', 'i', i)
    if isinstance(bpp__hlbx, ArrayItemArrayType):

        def _str_get_array_impl(S_str, i):
            S = S_str._obj
            nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
            yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
            sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.array_kernels.get(nswor__aogqk, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                yqo__lqg, sdrnx__qlryy)
        return _str_get_array_impl
    if bpp__hlbx == string_array_split_view_type:

        def _str_get_split_impl(S_str, i):
            S = S_str._obj
            nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
            yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
            sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            n = len(nswor__aogqk)
            xuit__ubmn = 0
            for ujge__ewgdq in numba.parfors.parfor.internal_prange(n):
                hjouf__likdm, hjouf__likdm, pkwry__wjglu = (
                    get_split_view_index(nswor__aogqk, ujge__ewgdq, i))
                xuit__ubmn += pkwry__wjglu
            numba.parfors.parfor.init_prange()
            out_arr = pre_alloc_string_array(n, xuit__ubmn)
            for ovpb__isys in numba.parfors.parfor.internal_prange(n):
                qqmev__cgx, vxflp__kyqqq, pkwry__wjglu = get_split_view_index(
                    nswor__aogqk, ovpb__isys, i)
                if qqmev__cgx == 0:
                    bodo.libs.array_kernels.setna(out_arr, ovpb__isys)
                    vlun__qwnme = get_split_view_data_ptr(nswor__aogqk, 0)
                else:
                    bodo.libs.str_arr_ext.str_arr_set_not_na(out_arr,
                        ovpb__isys)
                    vlun__qwnme = get_split_view_data_ptr(nswor__aogqk,
                        vxflp__kyqqq)
                bodo.libs.str_arr_ext.setitem_str_arr_ptr(out_arr,
                    ovpb__isys, vlun__qwnme, pkwry__wjglu)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                yqo__lqg, sdrnx__qlryy)
        return _str_get_split_impl
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_get_dict_impl(S_str, i):
            S = S_str._obj
            nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
            yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
            sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_get(nswor__aogqk, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                yqo__lqg, sdrnx__qlryy)
        return _str_get_dict_impl

    def _str_get_impl(S_str, i):
        S = S_str._obj
        nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
        yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
        sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(nswor__aogqk)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(n, -1)
        for ovpb__isys in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(nswor__aogqk, ovpb__isys
                ) or not len(nswor__aogqk[ovpb__isys]) > i >= -len(nswor__aogqk
                [ovpb__isys]):
                out_arr[ovpb__isys] = ''
                bodo.libs.array_kernels.setna(out_arr, ovpb__isys)
            else:
                out_arr[ovpb__isys] = nswor__aogqk[ovpb__isys][i]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, yqo__lqg,
            sdrnx__qlryy)
    return _str_get_impl


@overload_method(SeriesStrMethodType, 'join', inline='always', no_unliteral
    =True)
def overload_str_method_join(S_str, sep):
    bpp__hlbx = S_str.stype.data
    if (bpp__hlbx != string_array_split_view_type and bpp__hlbx !=
        ArrayItemArrayType(string_array_type) and not is_str_arr_type(
        bpp__hlbx)):
        raise_bodo_error(
            'Series.str.join(): only supports input type of Series(list(str)) and Series(str)'
            )
    str_arg_check('join', 'sep', sep)

    def impl(S_str, sep):
        S = S_str._obj
        mxeat__asi = bodo.hiframes.pd_series_ext.get_series_data(S)
        sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
        yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        n = len(mxeat__asi)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
        for ovpb__isys in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(mxeat__asi, ovpb__isys):
                out_arr[ovpb__isys] = ''
                bodo.libs.array_kernels.setna(out_arr, ovpb__isys)
            else:
                ljug__tddgx = mxeat__asi[ovpb__isys]
                out_arr[ovpb__isys] = sep.join(ljug__tddgx)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, yqo__lqg,
            sdrnx__qlryy)
    return impl


@overload_method(SeriesStrMethodType, 'replace', inline='always',
    no_unliteral=True)
def overload_str_method_replace(S_str, pat, repl, n=-1, case=None, flags=0,
    regex=True):
    not_supported_arg_check('replace', 'n', n, -1)
    not_supported_arg_check('replace', 'case', case, None)
    str_arg_check('replace', 'pat', pat)
    str_arg_check('replace', 'repl', repl)
    int_arg_check('replace', 'flags', flags)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_replace_dict_impl(S_str, pat, repl, n=-1, case=None, flags
            =0, regex=True):
            S = S_str._obj
            nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
            yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
            sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_replace(nswor__aogqk, pat,
                repl, flags, regex)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                yqo__lqg, sdrnx__qlryy)
        return _str_replace_dict_impl
    if is_overload_true(regex):

        def _str_replace_regex_impl(S_str, pat, repl, n=-1, case=None,
            flags=0, regex=True):
            S = S_str._obj
            nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
            yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
            sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            itk__ybhn = re.compile(pat, flags)
            loaqp__hlew = len(nswor__aogqk)
            out_arr = pre_alloc_string_array(loaqp__hlew, -1)
            for ovpb__isys in numba.parfors.parfor.internal_prange(loaqp__hlew
                ):
                if bodo.libs.array_kernels.isna(nswor__aogqk, ovpb__isys):
                    out_arr[ovpb__isys] = ''
                    bodo.libs.array_kernels.setna(out_arr, ovpb__isys)
                    continue
                out_arr[ovpb__isys] = itk__ybhn.sub(repl, nswor__aogqk[
                    ovpb__isys])
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                yqo__lqg, sdrnx__qlryy)
        return _str_replace_regex_impl
    if not is_overload_false(regex):
        raise BodoError('Series.str.replace(): regex argument should be bool')

    def _str_replace_noregex_impl(S_str, pat, repl, n=-1, case=None, flags=
        0, regex=True):
        S = S_str._obj
        nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
        yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
        sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        loaqp__hlew = len(nswor__aogqk)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(loaqp__hlew, -1)
        for ovpb__isys in numba.parfors.parfor.internal_prange(loaqp__hlew):
            if bodo.libs.array_kernels.isna(nswor__aogqk, ovpb__isys):
                out_arr[ovpb__isys] = ''
                bodo.libs.array_kernels.setna(out_arr, ovpb__isys)
                continue
            out_arr[ovpb__isys] = nswor__aogqk[ovpb__isys].replace(pat, repl)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, yqo__lqg,
            sdrnx__qlryy)
    return _str_replace_noregex_impl


@numba.njit
def series_contains_regex(S, pat, case, flags, na, regex):
    with numba.objmode(out_arr=bodo.boolean_array):
        out_arr = S.array._str_contains(pat, case, flags, na, regex)
    return out_arr


@numba.njit
def series_match_regex(S, pat, case, flags, na):
    with numba.objmode(out_arr=bodo.boolean_array):
        out_arr = S.array._str_match(pat, case, flags, na)
    return out_arr


def is_regex_unsupported(pat):
    kte__ijra = ['(?a', '(?i', '(?L', '(?m', '(?s', '(?u', '(?x', '(?#']
    if is_overload_constant_str(pat):
        if isinstance(pat, types.StringLiteral):
            pat = pat.literal_value
        return any([(dlon__wpnzn in pat) for dlon__wpnzn in kte__ijra])
    else:
        return True


@overload_method(SeriesStrMethodType, 'contains', no_unliteral=True)
def overload_str_method_contains(S_str, pat, case=True, flags=0, na=np.nan,
    regex=True):
    not_supported_arg_check('contains', 'na', na, np.nan)
    str_arg_check('contains', 'pat', pat)
    int_arg_check('contains', 'flags', flags)
    if not is_overload_constant_bool(regex):
        raise BodoError(
            "Series.str.contains(): 'regex' argument should be a constant boolean"
            )
    if not is_overload_constant_bool(case):
        raise BodoError(
            "Series.str.contains(): 'case' argument should be a constant boolean"
            )
    ejc__whgmw = re.IGNORECASE.value
    aay__kala = 'def impl(\n'
    aay__kala += '    S_str, pat, case=True, flags=0, na=np.nan, regex=True\n'
    aay__kala += '):\n'
    aay__kala += '  S = S_str._obj\n'
    aay__kala += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    aay__kala += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    aay__kala += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    aay__kala += '  l = len(arr)\n'
    aay__kala += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    if is_overload_true(regex):
        if is_regex_unsupported(pat) or flags:
            if S_str.stype.data == bodo.dict_str_arr_type:
                aay__kala += """  out_arr = bodo.libs.dict_arr_ext.str_series_contains_regex(arr, pat, case, flags, na, regex)
"""
            else:
                aay__kala += """  out_arr = bodo.hiframes.series_str_impl.series_contains_regex(S, pat, case, flags, na, regex)
"""
        else:
            aay__kala += """  get_search_regex(arr, case, False, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        aay__kala += (
            '  out_arr = bodo.libs.dict_arr_ext.str_contains_non_regex(arr, pat, case)\n'
            )
    else:
        aay__kala += '  numba.parfors.parfor.init_prange()\n'
        if is_overload_false(case):
            aay__kala += '  upper_pat = pat.upper()\n'
        aay__kala += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        aay__kala += '      if bodo.libs.array_kernels.isna(arr, i):\n'
        aay__kala += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        aay__kala += '      else: \n'
        if is_overload_true(case):
            aay__kala += '          out_arr[i] = pat in arr[i]\n'
        else:
            aay__kala += '          out_arr[i] = upper_pat in arr[i].upper()\n'
    aay__kala += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    xfdfi__biu = {}
    exec(aay__kala, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': ejc__whgmw, 'get_search_regex':
        get_search_regex}, xfdfi__biu)
    impl = xfdfi__biu['impl']
    return impl


@overload_method(SeriesStrMethodType, 'match', inline='always',
    no_unliteral=True)
def overload_str_method_match(S_str, pat, case=True, flags=0, na=np.nan):
    not_supported_arg_check('match', 'na', na, np.nan)
    str_arg_check('match', 'pat', pat)
    int_arg_check('match', 'flags', flags)
    if not is_overload_constant_bool(case):
        raise BodoError(
            "Series.str.match(): 'case' argument should be a constant boolean")
    ejc__whgmw = re.IGNORECASE.value
    aay__kala = 'def impl(S_str, pat, case=True, flags=0, na=np.nan):\n'
    aay__kala += '        S = S_str._obj\n'
    aay__kala += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    aay__kala += '        l = len(arr)\n'
    aay__kala += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    aay__kala += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    if not is_regex_unsupported(pat) and flags == 0:
        aay__kala += (
            '        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
        aay__kala += """        get_search_regex(arr, case, True, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        aay__kala += """        out_arr = bodo.libs.dict_arr_ext.str_match(arr, pat, case, flags, na)
"""
    else:
        aay__kala += (
            '        out_arr = series_match_regex(S, pat, case, flags, na)\n')
    aay__kala += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    xfdfi__biu = {}
    exec(aay__kala, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': ejc__whgmw, 'get_search_regex':
        get_search_regex}, xfdfi__biu)
    impl = xfdfi__biu['impl']
    return impl


@overload_method(SeriesStrMethodType, 'cat', no_unliteral=True)
def overload_str_method_cat(S_str, others=None, sep=None, na_rep=None, join
    ='left'):
    if not isinstance(others, DataFrameType):
        raise_bodo_error(
            "Series.str.cat(): 'others' must be a DataFrame currently")
    if not is_overload_none(sep):
        str_arg_check('cat', 'sep', sep)
    if not is_overload_constant_str(join) or get_overload_const_str(join
        ) != 'left':
        raise_bodo_error("Series.str.cat(): 'join' not supported yet")
    aay__kala = (
        "def impl(S_str, others=None, sep=None, na_rep=None, join='left'):\n")
    aay__kala += '  S = S_str._obj\n'
    aay__kala += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    aay__kala += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    aay__kala += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    aay__kala += '  l = len(arr)\n'
    for i in range(len(others.columns)):
        aay__kala += (
            f'  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(others, {i})\n'
            )
    if S_str.stype.data == bodo.dict_str_arr_type and all(usv__gxzq == bodo
        .dict_str_arr_type for usv__gxzq in others.data):
        osxs__zcf = ', '.join(f'data{i}' for i in range(len(others.columns)))
        aay__kala += (
            f'  out_arr = bodo.libs.dict_arr_ext.cat_dict_str((arr, {osxs__zcf}), sep)\n'
            )
    else:
        tgr__jsakg = ' or '.join(['bodo.libs.array_kernels.isna(arr, i)'] +
            [f'bodo.libs.array_kernels.isna(data{i}, i)' for i in range(len
            (others.columns))])
        aay__kala += (
            '  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)\n'
            )
        aay__kala += '  numba.parfors.parfor.init_prange()\n'
        aay__kala += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        aay__kala += f'      if {tgr__jsakg}:\n'
        aay__kala += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        aay__kala += '          continue\n'
        nogz__bpalz = ', '.join(['arr[i]'] + [f'data{i}[i]' for i in range(
            len(others.columns))])
        drzed__hvp = "''" if is_overload_none(sep) else 'sep'
        aay__kala += f'      out_arr[i] = {drzed__hvp}.join([{nogz__bpalz}])\n'
    aay__kala += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    xfdfi__biu = {}
    exec(aay__kala, {'bodo': bodo, 'numba': numba}, xfdfi__biu)
    impl = xfdfi__biu['impl']
    return impl


@overload_method(SeriesStrMethodType, 'count', inline='always',
    no_unliteral=True)
def overload_str_method_count(S_str, pat, flags=0):
    str_arg_check('count', 'pat', pat)
    int_arg_check('count', 'flags', flags)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_count_dict_impl(S_str, pat, flags=0):
            S = S_str._obj
            nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
            yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
            sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_count(nswor__aogqk, pat, flags
                )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                yqo__lqg, sdrnx__qlryy)
        return _str_count_dict_impl

    def impl(S_str, pat, flags=0):
        S = S_str._obj
        mxeat__asi = bodo.hiframes.pd_series_ext.get_series_data(S)
        sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
        yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
        itk__ybhn = re.compile(pat, flags)
        numba.parfors.parfor.init_prange()
        loaqp__hlew = len(mxeat__asi)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(loaqp__hlew, np.int64)
        for i in numba.parfors.parfor.internal_prange(loaqp__hlew):
            if bodo.libs.array_kernels.isna(mxeat__asi, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = str_findall_count(itk__ybhn, mxeat__asi[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr, yqo__lqg,
            sdrnx__qlryy)
    return impl


@overload_method(SeriesStrMethodType, 'find', inline='always', no_unliteral
    =True)
def overload_str_method_find(S_str, sub, start=0, end=None):
    str_arg_check('find', 'sub', sub)
    int_arg_check('find', 'start', start)
    if not is_overload_none(end):
        int_arg_check('find', 'end', end)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_find_dict_impl(S_str, sub, start=0, end=None):
            S = S_str._obj
            nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
            yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
            sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_find(nswor__aogqk, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                yqo__lqg, sdrnx__qlryy)
        return _str_find_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        mxeat__asi = bodo.hiframes.pd_series_ext.get_series_data(S)
        sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
        yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        loaqp__hlew = len(mxeat__asi)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(loaqp__hlew, np.int64)
        for i in numba.parfors.parfor.internal_prange(loaqp__hlew):
            if bodo.libs.array_kernels.isna(mxeat__asi, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = mxeat__asi[i].find(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, yqo__lqg,
            sdrnx__qlryy)
    return impl


@overload_method(SeriesStrMethodType, 'rfind', inline='always',
    no_unliteral=True)
def overload_str_method_rfind(S_str, sub, start=0, end=None):
    str_arg_check('rfind', 'sub', sub)
    if start != 0:
        int_arg_check('rfind', 'start', start)
    if not is_overload_none(end):
        int_arg_check('rfind', 'end', end)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_rfind_dict_impl(S_str, sub, start=0, end=None):
            S = S_str._obj
            nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
            yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
            sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_rfind(nswor__aogqk, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                yqo__lqg, sdrnx__qlryy)
        return _str_rfind_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        mxeat__asi = bodo.hiframes.pd_series_ext.get_series_data(S)
        sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
        yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        loaqp__hlew = len(mxeat__asi)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(loaqp__hlew, np.int64)
        for i in numba.parfors.parfor.internal_prange(loaqp__hlew):
            if bodo.libs.array_kernels.isna(mxeat__asi, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = mxeat__asi[i].rfind(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, yqo__lqg,
            sdrnx__qlryy)
    return impl


@overload_method(SeriesStrMethodType, 'index', inline='always',
    no_unliteral=True)
def overload_str_method_index(S_str, sub, start=0, end=None):
    str_arg_check('index', 'sub', sub)
    int_arg_check('index', 'start', start)
    if not is_overload_none(end):
        int_arg_check('index', 'end', end)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_index_dict_impl(S_str, sub, start=0, end=None):
            S = S_str._obj
            nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
            yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
            sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_index(nswor__aogqk, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                yqo__lqg, sdrnx__qlryy)
        return _str_index_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        mxeat__asi = bodo.hiframes.pd_series_ext.get_series_data(S)
        sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
        yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
        loaqp__hlew = len(mxeat__asi)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(loaqp__hlew, np.int64)
        numba.parfors.parfor.init_prange()
        exmd__nhyk = False
        for i in numba.parfors.parfor.internal_prange(loaqp__hlew):
            if bodo.libs.array_kernels.isna(mxeat__asi, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = mxeat__asi[i].find(sub, start, end)
                if out_arr[i] == -1:
                    exmd__nhyk = True
        bqj__husmb = 'substring not found' if exmd__nhyk else ''
        synchronize_error_njit('ValueError', bqj__husmb)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, yqo__lqg,
            sdrnx__qlryy)
    return impl


@overload_method(SeriesStrMethodType, 'rindex', inline='always',
    no_unliteral=True)
def overload_str_method_rindex(S_str, sub, start=0, end=None):
    str_arg_check('rindex', 'sub', sub)
    int_arg_check('rindex', 'start', start)
    if not is_overload_none(end):
        int_arg_check('rindex', 'end', end)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_rindex_dict_impl(S_str, sub, start=0, end=None):
            S = S_str._obj
            nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
            yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
            sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_rindex(nswor__aogqk, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                yqo__lqg, sdrnx__qlryy)
        return _str_rindex_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        mxeat__asi = bodo.hiframes.pd_series_ext.get_series_data(S)
        sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
        yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
        loaqp__hlew = len(mxeat__asi)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(loaqp__hlew, np.int64)
        numba.parfors.parfor.init_prange()
        exmd__nhyk = False
        for i in numba.parfors.parfor.internal_prange(loaqp__hlew):
            if bodo.libs.array_kernels.isna(mxeat__asi, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = mxeat__asi[i].rindex(sub, start, end)
                if out_arr[i] == -1:
                    exmd__nhyk = True
        bqj__husmb = 'substring not found' if exmd__nhyk else ''
        synchronize_error_njit('ValueError', bqj__husmb)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, yqo__lqg,
            sdrnx__qlryy)
    return impl


@overload_method(SeriesStrMethodType, 'slice_replace', inline='always',
    no_unliteral=True)
def overload_str_method_slice_replace(S_str, start=0, stop=None, repl=''):
    int_arg_check('slice_replace', 'start', start)
    if not is_overload_none(stop):
        int_arg_check('slice_replace', 'stop', stop)
    str_arg_check('slice_replace', 'repl', repl)

    def impl(S_str, start=0, stop=None, repl=''):
        S = S_str._obj
        mxeat__asi = bodo.hiframes.pd_series_ext.get_series_data(S)
        sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
        yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        loaqp__hlew = len(mxeat__asi)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(loaqp__hlew, -1)
        for ovpb__isys in numba.parfors.parfor.internal_prange(loaqp__hlew):
            if bodo.libs.array_kernels.isna(mxeat__asi, ovpb__isys):
                bodo.libs.array_kernels.setna(out_arr, ovpb__isys)
            else:
                if stop is not None:
                    yimup__bmni = mxeat__asi[ovpb__isys][stop:]
                else:
                    yimup__bmni = ''
                out_arr[ovpb__isys] = mxeat__asi[ovpb__isys][:start
                    ] + repl + yimup__bmni
        return bodo.hiframes.pd_series_ext.init_series(out_arr, yqo__lqg,
            sdrnx__qlryy)
    return impl


@overload_method(SeriesStrMethodType, 'repeat', inline='always',
    no_unliteral=True)
def overload_str_method_repeat(S_str, repeats):
    if isinstance(repeats, types.Integer) or is_overload_constant_int(repeats):
        if S_str.stype.data == bodo.dict_str_arr_type:

            def _str_repeat_int_dict_impl(S_str, repeats):
                S = S_str._obj
                nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
                yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
                sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
                out_arr = bodo.libs.dict_arr_ext.str_repeat_int(nswor__aogqk,
                    repeats)
                return bodo.hiframes.pd_series_ext.init_series(out_arr,
                    yqo__lqg, sdrnx__qlryy)
            return _str_repeat_int_dict_impl

        def impl(S_str, repeats):
            S = S_str._obj
            mxeat__asi = bodo.hiframes.pd_series_ext.get_series_data(S)
            sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
            yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
            numba.parfors.parfor.init_prange()
            loaqp__hlew = len(mxeat__asi)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(loaqp__hlew,
                -1)
            for ovpb__isys in numba.parfors.parfor.internal_prange(loaqp__hlew
                ):
                if bodo.libs.array_kernels.isna(mxeat__asi, ovpb__isys):
                    bodo.libs.array_kernels.setna(out_arr, ovpb__isys)
                else:
                    out_arr[ovpb__isys] = mxeat__asi[ovpb__isys] * repeats
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                yqo__lqg, sdrnx__qlryy)
        return impl
    elif is_overload_constant_list(repeats):
        hzi__dzpg = get_overload_const_list(repeats)
        oipzg__xwlu = all([isinstance(bflto__yiloo, int) for bflto__yiloo in
            hzi__dzpg])
    elif is_list_like_index_type(repeats) and isinstance(repeats.dtype,
        types.Integer):
        oipzg__xwlu = True
    else:
        oipzg__xwlu = False
    if oipzg__xwlu:

        def impl(S_str, repeats):
            S = S_str._obj
            mxeat__asi = bodo.hiframes.pd_series_ext.get_series_data(S)
            sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
            yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
            qdssn__zoupm = bodo.utils.conversion.coerce_to_array(repeats)
            numba.parfors.parfor.init_prange()
            loaqp__hlew = len(mxeat__asi)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(loaqp__hlew,
                -1)
            for ovpb__isys in numba.parfors.parfor.internal_prange(loaqp__hlew
                ):
                if bodo.libs.array_kernels.isna(mxeat__asi, ovpb__isys):
                    bodo.libs.array_kernels.setna(out_arr, ovpb__isys)
                else:
                    out_arr[ovpb__isys] = mxeat__asi[ovpb__isys
                        ] * qdssn__zoupm[ovpb__isys]
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                yqo__lqg, sdrnx__qlryy)
        return impl
    else:
        raise BodoError(
            'Series.str.repeat(): repeats argument must either be an integer or a sequence of integers'
            )


def create_ljust_rjust_center_overload(func_name):
    aay__kala = f"""def dict_impl(S_str, width, fillchar=' '):
    S = S_str._obj
    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    out_arr = bodo.libs.dict_arr_ext.str_{func_name}(arr, width, fillchar)
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
def impl(S_str, width, fillchar=' '):
    S = S_str._obj
    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    numba.parfors.parfor.init_prange()
    l = len(str_arr)
    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
    for j in numba.parfors.parfor.internal_prange(l):
        if bodo.libs.array_kernels.isna(str_arr, j):
            bodo.libs.array_kernels.setna(out_arr, j)
        else:
            out_arr[j] = str_arr[j].{func_name}(width, fillchar)
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    xfdfi__biu = {}
    yakb__quhd = {'bodo': bodo, 'numba': numba}
    exec(aay__kala, yakb__quhd, xfdfi__biu)
    impl = xfdfi__biu['impl']
    skdsq__xiw = xfdfi__biu['dict_impl']

    def overload_ljust_rjust_center_method(S_str, width, fillchar=' '):
        common_validate_padding(func_name, width, fillchar)
        if S_str.stype.data == bodo.dict_str_arr_type:
            return skdsq__xiw
        return impl
    return overload_ljust_rjust_center_method


def _install_ljust_rjust_center():
    for ucxyu__rcqw in ['ljust', 'rjust', 'center']:
        impl = create_ljust_rjust_center_overload(ucxyu__rcqw)
        overload_method(SeriesStrMethodType, ucxyu__rcqw, inline='always',
            no_unliteral=True)(impl)


_install_ljust_rjust_center()


@overload_method(SeriesStrMethodType, 'pad', no_unliteral=True)
def overload_str_method_pad(S_str, width, side='left', fillchar=' '):
    common_validate_padding('pad', width, fillchar)
    if is_overload_constant_str(side):
        if get_overload_const_str(side) not in ['left', 'right', 'both']:
            raise BodoError('Series.str.pad(): Invalid Side')
    else:
        raise BodoError('Series.str.pad(): Invalid Side')
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_pad_dict_impl(S_str, width, side='left', fillchar=' '):
            S = S_str._obj
            nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
            yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
            sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
            if side == 'left':
                out_arr = bodo.libs.dict_arr_ext.str_rjust(nswor__aogqk,
                    width, fillchar)
            elif side == 'right':
                out_arr = bodo.libs.dict_arr_ext.str_ljust(nswor__aogqk,
                    width, fillchar)
            elif side == 'both':
                out_arr = bodo.libs.dict_arr_ext.str_center(nswor__aogqk,
                    width, fillchar)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                yqo__lqg, sdrnx__qlryy)
        return _str_pad_dict_impl

    def impl(S_str, width, side='left', fillchar=' '):
        S = S_str._obj
        mxeat__asi = bodo.hiframes.pd_series_ext.get_series_data(S)
        sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
        yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        loaqp__hlew = len(mxeat__asi)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(loaqp__hlew, -1)
        for ovpb__isys in numba.parfors.parfor.internal_prange(loaqp__hlew):
            if bodo.libs.array_kernels.isna(mxeat__asi, ovpb__isys):
                out_arr[ovpb__isys] = ''
                bodo.libs.array_kernels.setna(out_arr, ovpb__isys)
            elif side == 'left':
                out_arr[ovpb__isys] = mxeat__asi[ovpb__isys].rjust(width,
                    fillchar)
            elif side == 'right':
                out_arr[ovpb__isys] = mxeat__asi[ovpb__isys].ljust(width,
                    fillchar)
            elif side == 'both':
                out_arr[ovpb__isys] = mxeat__asi[ovpb__isys].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, yqo__lqg,
            sdrnx__qlryy)
    return impl


@overload_method(SeriesStrMethodType, 'zfill', inline='always',
    no_unliteral=True)
def overload_str_method_zfill(S_str, width):
    int_arg_check('zfill', 'width', width)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_zfill_dict_impl(S_str, width):
            S = S_str._obj
            nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
            yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
            sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_zfill(nswor__aogqk, width)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                yqo__lqg, sdrnx__qlryy)
        return _str_zfill_dict_impl

    def impl(S_str, width):
        S = S_str._obj
        mxeat__asi = bodo.hiframes.pd_series_ext.get_series_data(S)
        sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
        yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        loaqp__hlew = len(mxeat__asi)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(loaqp__hlew, -1)
        for ovpb__isys in numba.parfors.parfor.internal_prange(loaqp__hlew):
            if bodo.libs.array_kernels.isna(mxeat__asi, ovpb__isys):
                out_arr[ovpb__isys] = ''
                bodo.libs.array_kernels.setna(out_arr, ovpb__isys)
            else:
                out_arr[ovpb__isys] = mxeat__asi[ovpb__isys].zfill(width)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, yqo__lqg,
            sdrnx__qlryy)
    return impl


@overload_method(SeriesStrMethodType, 'slice', no_unliteral=True)
def overload_str_method_slice(S_str, start=None, stop=None, step=None):
    if not is_overload_none(start):
        int_arg_check('slice', 'start', start)
    if not is_overload_none(stop):
        int_arg_check('slice', 'stop', stop)
    if not is_overload_none(step):
        int_arg_check('slice', 'step', step)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_slice_dict_impl(S_str, start=None, stop=None, step=None):
            S = S_str._obj
            nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
            yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
            sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_slice(nswor__aogqk, start,
                stop, step)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                yqo__lqg, sdrnx__qlryy)
        return _str_slice_dict_impl

    def impl(S_str, start=None, stop=None, step=None):
        S = S_str._obj
        mxeat__asi = bodo.hiframes.pd_series_ext.get_series_data(S)
        sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
        yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        loaqp__hlew = len(mxeat__asi)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(loaqp__hlew, -1)
        for ovpb__isys in numba.parfors.parfor.internal_prange(loaqp__hlew):
            if bodo.libs.array_kernels.isna(mxeat__asi, ovpb__isys):
                out_arr[ovpb__isys] = ''
                bodo.libs.array_kernels.setna(out_arr, ovpb__isys)
            else:
                out_arr[ovpb__isys] = mxeat__asi[ovpb__isys][start:stop:step]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, yqo__lqg,
            sdrnx__qlryy)
    return impl


@overload_method(SeriesStrMethodType, 'startswith', inline='always',
    no_unliteral=True)
def overload_str_method_startswith(S_str, pat, na=np.nan):
    not_supported_arg_check('startswith', 'na', na, np.nan)
    str_arg_check('startswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_startswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
            yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
            sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_startswith(nswor__aogqk,
                pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                yqo__lqg, sdrnx__qlryy)
        return _str_startswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        mxeat__asi = bodo.hiframes.pd_series_ext.get_series_data(S)
        sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
        yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        loaqp__hlew = len(mxeat__asi)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(loaqp__hlew)
        for i in numba.parfors.parfor.internal_prange(loaqp__hlew):
            if bodo.libs.array_kernels.isna(mxeat__asi, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = mxeat__asi[i].startswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, yqo__lqg,
            sdrnx__qlryy)
    return impl


@overload_method(SeriesStrMethodType, 'endswith', inline='always',
    no_unliteral=True)
def overload_str_method_endswith(S_str, pat, na=np.nan):
    not_supported_arg_check('endswith', 'na', na, np.nan)
    str_arg_check('endswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_endswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
            yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
            sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_endswith(nswor__aogqk, pat, na
                )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                yqo__lqg, sdrnx__qlryy)
        return _str_endswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        mxeat__asi = bodo.hiframes.pd_series_ext.get_series_data(S)
        sdrnx__qlryy = bodo.hiframes.pd_series_ext.get_series_name(S)
        yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        loaqp__hlew = len(mxeat__asi)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(loaqp__hlew)
        for i in numba.parfors.parfor.internal_prange(loaqp__hlew):
            if bodo.libs.array_kernels.isna(mxeat__asi, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = mxeat__asi[i].endswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, yqo__lqg,
            sdrnx__qlryy)
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_str_method_getitem(S_str, ind):
    if not isinstance(S_str, SeriesStrMethodType):
        return
    if not isinstance(types.unliteral(ind), (types.SliceType, types.Integer)):
        raise BodoError(
            'index input to Series.str[] should be a slice or an integer')
    if isinstance(ind, types.SliceType):
        return lambda S_str, ind: S_str.slice(ind.start, ind.stop, ind.step)
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda S_str, ind: S_str.get(ind)


@overload_method(SeriesStrMethodType, 'extract', inline='always',
    no_unliteral=True)
def overload_str_method_extract(S_str, pat, flags=0, expand=True):
    if not is_overload_constant_bool(expand):
        raise BodoError(
            "Series.str.extract(): 'expand' argument should be a constant bool"
            )
    ljefw__hoc, regex = _get_column_names_from_regex(pat, flags, 'extract')
    bzslz__fnua = len(ljefw__hoc)
    if S_str.stype.data == bodo.dict_str_arr_type:
        aay__kala = 'def impl(S_str, pat, flags=0, expand=True):\n'
        aay__kala += '  S = S_str._obj\n'
        aay__kala += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        aay__kala += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        aay__kala += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        aay__kala += f"""  out_arr_list = bodo.libs.dict_arr_ext.str_extract(arr, pat, flags, {bzslz__fnua})
"""
        for i in range(bzslz__fnua):
            aay__kala += f'  out_arr_{i} = out_arr_list[{i}]\n'
    else:
        aay__kala = 'def impl(S_str, pat, flags=0, expand=True):\n'
        aay__kala += '  regex = re.compile(pat, flags=flags)\n'
        aay__kala += '  S = S_str._obj\n'
        aay__kala += (
            '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        aay__kala += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        aay__kala += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        aay__kala += '  numba.parfors.parfor.init_prange()\n'
        aay__kala += '  n = len(str_arr)\n'
        for i in range(bzslz__fnua):
            aay__kala += (
                '  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)\n'
                .format(i))
        aay__kala += '  for j in numba.parfors.parfor.internal_prange(n):\n'
        aay__kala += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
        for i in range(bzslz__fnua):
            aay__kala += "          out_arr_{}[j] = ''\n".format(i)
            aay__kala += (
                '          bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
                format(i))
        aay__kala += '      else:\n'
        aay__kala += '          m = regex.search(str_arr[j])\n'
        aay__kala += '          if m:\n'
        aay__kala += '            g = m.groups()\n'
        for i in range(bzslz__fnua):
            aay__kala += '            out_arr_{0}[j] = g[{0}]\n'.format(i)
        aay__kala += '          else:\n'
        for i in range(bzslz__fnua):
            aay__kala += "            out_arr_{}[j] = ''\n".format(i)
            aay__kala += (
                '            bodo.libs.array_kernels.setna(out_arr_{}, j)\n'
                .format(i))
    if is_overload_false(expand) and regex.groups == 1:
        sdrnx__qlryy = "'{}'".format(list(regex.groupindex.keys()).pop()
            ) if len(regex.groupindex.keys()) > 0 else 'name'
        aay__kala += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr_0, index, {})\n'
            .format(sdrnx__qlryy))
        xfdfi__biu = {}
        exec(aay__kala, {'re': re, 'bodo': bodo, 'numba': numba,
            'get_utf8_size': get_utf8_size}, xfdfi__biu)
        impl = xfdfi__biu['impl']
        return impl
    hgpoq__ifuq = ', '.join('out_arr_{}'.format(i) for i in range(bzslz__fnua))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(aay__kala, ljefw__hoc,
        hgpoq__ifuq, 'index', extra_globals={'get_utf8_size': get_utf8_size,
        're': re})
    return impl


@overload_method(SeriesStrMethodType, 'extractall', inline='always',
    no_unliteral=True)
def overload_str_method_extractall(S_str, pat, flags=0):
    ljefw__hoc, hjouf__likdm = _get_column_names_from_regex(pat, flags,
        'extractall')
    bzslz__fnua = len(ljefw__hoc)
    ylw__ejre = isinstance(S_str.stype.index, StringIndexType)
    kwqp__mapuy = bzslz__fnua > 1
    cyl__fskfs = '_multi' if kwqp__mapuy else ''
    if S_str.stype.data == bodo.dict_str_arr_type:
        aay__kala = 'def impl(S_str, pat, flags=0):\n'
        aay__kala += '  S = S_str._obj\n'
        aay__kala += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
        aay__kala += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        aay__kala += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        aay__kala += (
            '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
        aay__kala += (
            '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n'
            )
        aay__kala += '  regex = re.compile(pat, flags=flags)\n'
        aay__kala += '  out_ind_arr, out_match_arr, out_arr_list = '
        aay__kala += f'bodo.libs.dict_arr_ext.str_extractall{cyl__fskfs}(\n'
        aay__kala += f'arr, regex, {bzslz__fnua}, index_arr)\n'
        for i in range(bzslz__fnua):
            aay__kala += f'  out_arr_{i} = out_arr_list[{i}]\n'
        aay__kala += (
            '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n'
            )
        aay__kala += (
            "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n")
    else:
        aay__kala = 'def impl(S_str, pat, flags=0):\n'
        aay__kala += '  regex = re.compile(pat, flags=flags)\n'
        aay__kala += '  S = S_str._obj\n'
        aay__kala += (
            '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        aay__kala += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        aay__kala += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        aay__kala += (
            '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
        aay__kala += (
            '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n'
            )
        aay__kala += '  numba.parfors.parfor.init_prange()\n'
        aay__kala += '  n = len(str_arr)\n'
        aay__kala += '  out_n_l = [0]\n'
        for i in range(bzslz__fnua):
            aay__kala += '  num_chars_{} = 0\n'.format(i)
        if ylw__ejre:
            aay__kala += '  index_num_chars = 0\n'
        aay__kala += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if ylw__ejre:
            aay__kala += (
                '      index_num_chars += get_utf8_size(index_arr[i])\n')
        aay__kala += '      if bodo.libs.array_kernels.isna(str_arr, i):\n'
        aay__kala += '          continue\n'
        aay__kala += '      m = regex.findall(str_arr[i])\n'
        aay__kala += '      out_n_l[0] += len(m)\n'
        for i in range(bzslz__fnua):
            aay__kala += '      l_{} = 0\n'.format(i)
        aay__kala += '      for s in m:\n'
        for i in range(bzslz__fnua):
            aay__kala += '        l_{} += get_utf8_size(s{})\n'.format(i, 
                '[{}]'.format(i) if bzslz__fnua > 1 else '')
        for i in range(bzslz__fnua):
            aay__kala += '      num_chars_{0} += l_{0}\n'.format(i)
        aay__kala += (
            '  out_n = bodo.libs.distributed_api.local_alloc_size(out_n_l[0], str_arr)\n'
            )
        for i in range(bzslz__fnua):
            aay__kala += (
                """  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, num_chars_{0})
"""
                .format(i))
        if ylw__ejre:
            aay__kala += """  out_ind_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, index_num_chars)
"""
        else:
            aay__kala += '  out_ind_arr = np.empty(out_n, index_arr.dtype)\n'
        aay__kala += '  out_match_arr = np.empty(out_n, np.int64)\n'
        aay__kala += '  out_ind = 0\n'
        aay__kala += '  for j in numba.parfors.parfor.internal_prange(n):\n'
        aay__kala += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
        aay__kala += '          continue\n'
        aay__kala += '      m = regex.findall(str_arr[j])\n'
        aay__kala += '      for k, s in enumerate(m):\n'
        for i in range(bzslz__fnua):
            aay__kala += (
                """        bodo.libs.distributed_api.set_arr_local(out_arr_{}, out_ind, s{})
"""
                .format(i, '[{}]'.format(i) if bzslz__fnua > 1 else ''))
        aay__kala += """        bodo.libs.distributed_api.set_arr_local(out_ind_arr, out_ind, index_arr[j])
"""
        aay__kala += (
            '        bodo.libs.distributed_api.set_arr_local(out_match_arr, out_ind, k)\n'
            )
        aay__kala += '        out_ind += 1\n'
        aay__kala += (
            '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n'
            )
        aay__kala += (
            "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n")
    hgpoq__ifuq = ', '.join('out_arr_{}'.format(i) for i in range(bzslz__fnua))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(aay__kala, ljefw__hoc,
        hgpoq__ifuq, 'out_index', extra_globals={'get_utf8_size':
        get_utf8_size, 're': re})
    return impl


def _get_column_names_from_regex(pat, flags, func_name):
    if not is_overload_constant_str(pat):
        raise BodoError(
            "Series.str.{}(): 'pat' argument should be a constant string".
            format(func_name))
    if not is_overload_constant_int(flags):
        raise BodoError(
            "Series.str.{}(): 'flags' argument should be a constant int".
            format(func_name))
    pat = get_overload_const_str(pat)
    flags = get_overload_const_int(flags)
    regex = re.compile(pat, flags=flags)
    if regex.groups == 0:
        raise BodoError(
            'Series.str.{}(): pattern {} contains no capture groups'.format
            (func_name, pat))
    fcj__yfyfm = dict(zip(regex.groupindex.values(), regex.groupindex.keys()))
    ljefw__hoc = [fcj__yfyfm.get(1 + i, i) for i in range(regex.groups)]
    return ljefw__hoc, regex


def create_str2str_methods_overload(func_name):
    ibhvw__ujtn = func_name in ['lstrip', 'rstrip', 'strip']
    aay__kala = f"""def f({'S_str, to_strip=None' if ibhvw__ujtn else 'S_str'}):
    S = S_str._obj
    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    str_arr = decode_if_dict_array(str_arr)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    numba.parfors.parfor.init_prange()
    n = len(str_arr)
    num_chars = {'-1' if ibhvw__ujtn else 'num_total_chars(str_arr)'}
    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, num_chars)
    for j in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(str_arr, j):
            out_arr[j] = ""
            bodo.libs.array_kernels.setna(out_arr, j)
        else:
            out_arr[j] = str_arr[j].{func_name}({'to_strip' if ibhvw__ujtn else ''})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    aay__kala += f"""def _dict_impl({'S_str, to_strip=None' if ibhvw__ujtn else 'S_str'}):
    S = S_str._obj
    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    out_arr = bodo.libs.dict_arr_ext.str_{func_name}({'arr, to_strip' if ibhvw__ujtn else 'arr'})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    xfdfi__biu = {}
    exec(aay__kala, {'bodo': bodo, 'numba': numba, 'num_total_chars': bodo.
        libs.str_arr_ext.num_total_chars, 'get_utf8_size': bodo.libs.
        str_arr_ext.get_utf8_size, 'decode_if_dict_array': bodo.utils.
        typing.decode_if_dict_array}, xfdfi__biu)
    wnu__srg = xfdfi__biu['f']
    tavw__nyr = xfdfi__biu['_dict_impl']
    if ibhvw__ujtn:

        def overload_strip_method(S_str, to_strip=None):
            if not is_overload_none(to_strip):
                str_arg_check(func_name, 'to_strip', to_strip)
            if S_str.stype.data == bodo.dict_str_arr_type:
                return tavw__nyr
            return wnu__srg
        return overload_strip_method
    else:

        def overload_str_method_dict_supported(S_str):
            if S_str.stype.data == bodo.dict_str_arr_type:
                return tavw__nyr
            return wnu__srg
        return overload_str_method_dict_supported


def create_str2bool_methods_overload(func_name):
    aay__kala = 'def dict_impl(S_str):\n'
    aay__kala += '    S = S_str._obj\n'
    aay__kala += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    aay__kala += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    aay__kala += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    aay__kala += f'    out_arr = bodo.libs.dict_arr_ext.str_{func_name}(arr)\n'
    aay__kala += (
        '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    aay__kala += 'def impl(S_str):\n'
    aay__kala += '    S = S_str._obj\n'
    aay__kala += (
        '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    aay__kala += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    aay__kala += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    aay__kala += '    numba.parfors.parfor.init_prange()\n'
    aay__kala += '    l = len(str_arr)\n'
    aay__kala += '    out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    aay__kala += '    for i in numba.parfors.parfor.internal_prange(l):\n'
    aay__kala += '        if bodo.libs.array_kernels.isna(str_arr, i):\n'
    aay__kala += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
    aay__kala += '        else:\n'
    aay__kala += '            out_arr[i] = np.bool_(str_arr[i].{}())\n'.format(
        func_name)
    aay__kala += '    return bodo.hiframes.pd_series_ext.init_series(\n'
    aay__kala += '      out_arr,index, name)\n'
    xfdfi__biu = {}
    exec(aay__kala, {'bodo': bodo, 'numba': numba, 'np': np}, xfdfi__biu)
    impl = xfdfi__biu['impl']
    skdsq__xiw = xfdfi__biu['dict_impl']

    def overload_str2bool_methods(S_str):
        if S_str.stype.data == bodo.dict_str_arr_type:
            return skdsq__xiw
        return impl
    return overload_str2bool_methods


def _install_str2str_methods():
    for bqd__glzak in bodo.hiframes.pd_series_ext.str2str_methods:
        aklzn__qdy = create_str2str_methods_overload(bqd__glzak)
        overload_method(SeriesStrMethodType, bqd__glzak, inline='always',
            no_unliteral=True)(aklzn__qdy)


def _install_str2bool_methods():
    for bqd__glzak in bodo.hiframes.pd_series_ext.str2bool_methods:
        aklzn__qdy = create_str2bool_methods_overload(bqd__glzak)
        overload_method(SeriesStrMethodType, bqd__glzak, inline='always',
            no_unliteral=True)(aklzn__qdy)


_install_str2str_methods()
_install_str2bool_methods()


@overload_attribute(SeriesType, 'cat')
def overload_series_cat(s):
    if not isinstance(s.dtype, bodo.hiframes.pd_categorical_ext.
        PDCategoricalDtype):
        raise BodoError('Can only use .cat accessor with categorical values.')
    return lambda s: bodo.hiframes.series_str_impl.init_series_cat_method(s)


class SeriesCatMethodType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        sdrnx__qlryy = 'SeriesCatMethodType({})'.format(stype)
        super(SeriesCatMethodType, self).__init__(sdrnx__qlryy)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesCatMethodType)
class SeriesCatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        sxnoz__mtk = [('obj', fe_type.stype)]
        super(SeriesCatModel, self).__init__(dmm, fe_type, sxnoz__mtk)


make_attribute_wrapper(SeriesCatMethodType, 'obj', '_obj')


@intrinsic
def init_series_cat_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        byf__wreh, = args
        wvvcb__lso = signature.return_type
        zbdaw__kxjou = cgutils.create_struct_proxy(wvvcb__lso)(context, builder
            )
        zbdaw__kxjou.obj = byf__wreh
        context.nrt.incref(builder, signature.args[0], byf__wreh)
        return zbdaw__kxjou._getvalue()
    return SeriesCatMethodType(obj)(obj), codegen


@overload_attribute(SeriesCatMethodType, 'codes')
def series_cat_codes_overload(S_dt):

    def impl(S_dt):
        S = S_dt._obj
        nswor__aogqk = bodo.hiframes.pd_series_ext.get_series_data(S)
        yqo__lqg = bodo.hiframes.pd_series_ext.get_series_index(S)
        sdrnx__qlryy = None
        return bodo.hiframes.pd_series_ext.init_series(bodo.hiframes.
            pd_categorical_ext.get_categorical_arr_codes(nswor__aogqk),
            yqo__lqg, sdrnx__qlryy)
    return impl


unsupported_cat_attrs = {'categories', 'ordered'}
unsupported_cat_methods = {'rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered'}


def _install_catseries_unsupported():
    for ggl__ouo in unsupported_cat_attrs:
        yqa__fkxqv = 'Series.cat.' + ggl__ouo
        overload_attribute(SeriesCatMethodType, ggl__ouo)(
            create_unsupported_overload(yqa__fkxqv))
    for cuttl__xjxu in unsupported_cat_methods:
        yqa__fkxqv = 'Series.cat.' + cuttl__xjxu
        overload_method(SeriesCatMethodType, cuttl__xjxu)(
            create_unsupported_overload(yqa__fkxqv))


_install_catseries_unsupported()
unsupported_str_methods = {'casefold', 'decode', 'encode', 'findall',
    'fullmatch', 'index', 'match', 'normalize', 'partition', 'rindex',
    'rpartition', 'slice_replace', 'rsplit', 'translate', 'wrap', 'get_dummies'
    }


def _install_strseries_unsupported():
    for cuttl__xjxu in unsupported_str_methods:
        yqa__fkxqv = 'Series.str.' + cuttl__xjxu
        overload_method(SeriesStrMethodType, cuttl__xjxu)(
            create_unsupported_overload(yqa__fkxqv))


_install_strseries_unsupported()
