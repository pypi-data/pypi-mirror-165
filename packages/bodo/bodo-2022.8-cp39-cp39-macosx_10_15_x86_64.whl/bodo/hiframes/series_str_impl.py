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
        gsr__skq = 'SeriesStrMethodType({})'.format(stype)
        super(SeriesStrMethodType, self).__init__(gsr__skq)


@register_model(SeriesStrMethodType)
class SeriesStrModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ldk__tnxff = [('obj', fe_type.stype)]
        super(SeriesStrModel, self).__init__(dmm, fe_type, ldk__tnxff)


make_attribute_wrapper(SeriesStrMethodType, 'obj', '_obj')


@intrinsic
def init_series_str_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        jnx__aln, = args
        oadxb__neurk = signature.return_type
        inmzg__kcsdy = cgutils.create_struct_proxy(oadxb__neurk)(context,
            builder)
        inmzg__kcsdy.obj = jnx__aln
        context.nrt.incref(builder, signature.args[0], jnx__aln)
        return inmzg__kcsdy._getvalue()
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
            pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
            odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
            gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_len(pxmrw__ewrws)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                odq__vgcjf, gsr__skq)
        return _str_len_dict_impl

    def impl(S_str):
        S = S_str._obj
        pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
        odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
        gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.array_kernels.get_arr_lens(pxmrw__ewrws, False)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, odq__vgcjf,
            gsr__skq)
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
            pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
            odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
            gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.hiframes.split_impl.compute_split_view(pxmrw__ewrws,
                pat)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                odq__vgcjf, gsr__skq)
        return _str_split_view_impl

    def _str_split_impl(S_str, pat=None, n=-1, expand=False):
        S = S_str._obj
        pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
        odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
        gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.str_ext.str_split(pxmrw__ewrws, pat, n)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, odq__vgcjf,
            gsr__skq)
    return _str_split_impl


@overload_method(SeriesStrMethodType, 'get', no_unliteral=True)
def overload_str_method_get(S_str, i):
    sgrh__rvtpm = S_str.stype.data
    if (sgrh__rvtpm != string_array_split_view_type and not is_str_arr_type
        (sgrh__rvtpm)) and not isinstance(sgrh__rvtpm, ArrayItemArrayType):
        raise_bodo_error(
            'Series.str.get(): only supports input type of Series(array(item)) and Series(str)'
            )
    int_arg_check('get', 'i', i)
    if isinstance(sgrh__rvtpm, ArrayItemArrayType):

        def _str_get_array_impl(S_str, i):
            S = S_str._obj
            pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
            odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
            gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.array_kernels.get(pxmrw__ewrws, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                odq__vgcjf, gsr__skq)
        return _str_get_array_impl
    if sgrh__rvtpm == string_array_split_view_type:

        def _str_get_split_impl(S_str, i):
            S = S_str._obj
            pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
            odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
            gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            n = len(pxmrw__ewrws)
            seh__jsgh = 0
            for qzyfi__ywpvv in numba.parfors.parfor.internal_prange(n):
                pqwn__ekjwb, pqwn__ekjwb, hqbir__awsnq = get_split_view_index(
                    pxmrw__ewrws, qzyfi__ywpvv, i)
                seh__jsgh += hqbir__awsnq
            numba.parfors.parfor.init_prange()
            out_arr = pre_alloc_string_array(n, seh__jsgh)
            for eks__ctuo in numba.parfors.parfor.internal_prange(n):
                kdl__zqgej, fwna__wzi, hqbir__awsnq = get_split_view_index(
                    pxmrw__ewrws, eks__ctuo, i)
                if kdl__zqgej == 0:
                    bodo.libs.array_kernels.setna(out_arr, eks__ctuo)
                    vglru__yvz = get_split_view_data_ptr(pxmrw__ewrws, 0)
                else:
                    bodo.libs.str_arr_ext.str_arr_set_not_na(out_arr, eks__ctuo
                        )
                    vglru__yvz = get_split_view_data_ptr(pxmrw__ewrws,
                        fwna__wzi)
                bodo.libs.str_arr_ext.setitem_str_arr_ptr(out_arr,
                    eks__ctuo, vglru__yvz, hqbir__awsnq)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                odq__vgcjf, gsr__skq)
        return _str_get_split_impl
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_get_dict_impl(S_str, i):
            S = S_str._obj
            pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
            odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
            gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_get(pxmrw__ewrws, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                odq__vgcjf, gsr__skq)
        return _str_get_dict_impl

    def _str_get_impl(S_str, i):
        S = S_str._obj
        pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
        odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
        gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(pxmrw__ewrws)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(n, -1)
        for eks__ctuo in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(pxmrw__ewrws, eks__ctuo
                ) or not len(pxmrw__ewrws[eks__ctuo]) > i >= -len(pxmrw__ewrws
                [eks__ctuo]):
                out_arr[eks__ctuo] = ''
                bodo.libs.array_kernels.setna(out_arr, eks__ctuo)
            else:
                out_arr[eks__ctuo] = pxmrw__ewrws[eks__ctuo][i]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, odq__vgcjf,
            gsr__skq)
    return _str_get_impl


@overload_method(SeriesStrMethodType, 'join', inline='always', no_unliteral
    =True)
def overload_str_method_join(S_str, sep):
    sgrh__rvtpm = S_str.stype.data
    if (sgrh__rvtpm != string_array_split_view_type and sgrh__rvtpm !=
        ArrayItemArrayType(string_array_type) and not is_str_arr_type(
        sgrh__rvtpm)):
        raise_bodo_error(
            'Series.str.join(): only supports input type of Series(list(str)) and Series(str)'
            )
    str_arg_check('join', 'sep', sep)

    def impl(S_str, sep):
        S = S_str._obj
        ofw__uqukt = bodo.hiframes.pd_series_ext.get_series_data(S)
        gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
        odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        n = len(ofw__uqukt)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
        for eks__ctuo in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(ofw__uqukt, eks__ctuo):
                out_arr[eks__ctuo] = ''
                bodo.libs.array_kernels.setna(out_arr, eks__ctuo)
            else:
                opovc__abhs = ofw__uqukt[eks__ctuo]
                out_arr[eks__ctuo] = sep.join(opovc__abhs)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, odq__vgcjf,
            gsr__skq)
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
            pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
            odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
            gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_replace(pxmrw__ewrws, pat,
                repl, flags, regex)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                odq__vgcjf, gsr__skq)
        return _str_replace_dict_impl
    if is_overload_true(regex):

        def _str_replace_regex_impl(S_str, pat, repl, n=-1, case=None,
            flags=0, regex=True):
            S = S_str._obj
            pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
            odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
            gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            fhyz__oduye = re.compile(pat, flags)
            sdo__xfh = len(pxmrw__ewrws)
            out_arr = pre_alloc_string_array(sdo__xfh, -1)
            for eks__ctuo in numba.parfors.parfor.internal_prange(sdo__xfh):
                if bodo.libs.array_kernels.isna(pxmrw__ewrws, eks__ctuo):
                    out_arr[eks__ctuo] = ''
                    bodo.libs.array_kernels.setna(out_arr, eks__ctuo)
                    continue
                out_arr[eks__ctuo] = fhyz__oduye.sub(repl, pxmrw__ewrws[
                    eks__ctuo])
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                odq__vgcjf, gsr__skq)
        return _str_replace_regex_impl
    if not is_overload_false(regex):
        raise BodoError('Series.str.replace(): regex argument should be bool')

    def _str_replace_noregex_impl(S_str, pat, repl, n=-1, case=None, flags=
        0, regex=True):
        S = S_str._obj
        pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
        odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
        gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        sdo__xfh = len(pxmrw__ewrws)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(sdo__xfh, -1)
        for eks__ctuo in numba.parfors.parfor.internal_prange(sdo__xfh):
            if bodo.libs.array_kernels.isna(pxmrw__ewrws, eks__ctuo):
                out_arr[eks__ctuo] = ''
                bodo.libs.array_kernels.setna(out_arr, eks__ctuo)
                continue
            out_arr[eks__ctuo] = pxmrw__ewrws[eks__ctuo].replace(pat, repl)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, odq__vgcjf,
            gsr__skq)
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
    uto__pwl = ['(?a', '(?i', '(?L', '(?m', '(?s', '(?u', '(?x', '(?#']
    if is_overload_constant_str(pat):
        if isinstance(pat, types.StringLiteral):
            pat = pat.literal_value
        return any([(satxd__xnbqo in pat) for satxd__xnbqo in uto__pwl])
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
    fva__ysd = re.IGNORECASE.value
    lipkg__spkxb = 'def impl(\n'
    lipkg__spkxb += (
        '    S_str, pat, case=True, flags=0, na=np.nan, regex=True\n')
    lipkg__spkxb += '):\n'
    lipkg__spkxb += '  S = S_str._obj\n'
    lipkg__spkxb += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    lipkg__spkxb += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    lipkg__spkxb += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    lipkg__spkxb += '  l = len(arr)\n'
    lipkg__spkxb += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    if is_overload_true(regex):
        if is_regex_unsupported(pat) or flags:
            if S_str.stype.data == bodo.dict_str_arr_type:
                lipkg__spkxb += """  out_arr = bodo.libs.dict_arr_ext.str_series_contains_regex(arr, pat, case, flags, na, regex)
"""
            else:
                lipkg__spkxb += """  out_arr = bodo.hiframes.series_str_impl.series_contains_regex(S, pat, case, flags, na, regex)
"""
        else:
            lipkg__spkxb += """  get_search_regex(arr, case, False, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        lipkg__spkxb += """  out_arr = bodo.libs.dict_arr_ext.str_contains_non_regex(arr, pat, case)
"""
    else:
        lipkg__spkxb += '  numba.parfors.parfor.init_prange()\n'
        if is_overload_false(case):
            lipkg__spkxb += '  upper_pat = pat.upper()\n'
        lipkg__spkxb += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        lipkg__spkxb += '      if bodo.libs.array_kernels.isna(arr, i):\n'
        lipkg__spkxb += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        lipkg__spkxb += '      else: \n'
        if is_overload_true(case):
            lipkg__spkxb += '          out_arr[i] = pat in arr[i]\n'
        else:
            lipkg__spkxb += (
                '          out_arr[i] = upper_pat in arr[i].upper()\n')
    lipkg__spkxb += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    shdjj__ijqa = {}
    exec(lipkg__spkxb, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': fva__ysd, 'get_search_regex':
        get_search_regex}, shdjj__ijqa)
    impl = shdjj__ijqa['impl']
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
    fva__ysd = re.IGNORECASE.value
    lipkg__spkxb = 'def impl(S_str, pat, case=True, flags=0, na=np.nan):\n'
    lipkg__spkxb += '        S = S_str._obj\n'
    lipkg__spkxb += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    lipkg__spkxb += '        l = len(arr)\n'
    lipkg__spkxb += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    lipkg__spkxb += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    if not is_regex_unsupported(pat) and flags == 0:
        lipkg__spkxb += (
            '        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
        lipkg__spkxb += """        get_search_regex(arr, case, True, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        lipkg__spkxb += """        out_arr = bodo.libs.dict_arr_ext.str_match(arr, pat, case, flags, na)
"""
    else:
        lipkg__spkxb += (
            '        out_arr = series_match_regex(S, pat, case, flags, na)\n')
    lipkg__spkxb += """        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    shdjj__ijqa = {}
    exec(lipkg__spkxb, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': fva__ysd, 'get_search_regex':
        get_search_regex}, shdjj__ijqa)
    impl = shdjj__ijqa['impl']
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
    lipkg__spkxb = (
        "def impl(S_str, others=None, sep=None, na_rep=None, join='left'):\n")
    lipkg__spkxb += '  S = S_str._obj\n'
    lipkg__spkxb += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    lipkg__spkxb += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    lipkg__spkxb += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    lipkg__spkxb += '  l = len(arr)\n'
    for i in range(len(others.columns)):
        lipkg__spkxb += f"""  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(others, {i})
"""
    if S_str.stype.data == bodo.dict_str_arr_type and all(arbj__zgh == bodo
        .dict_str_arr_type for arbj__zgh in others.data):
        dcyd__ksl = ', '.join(f'data{i}' for i in range(len(others.columns)))
        lipkg__spkxb += f"""  out_arr = bodo.libs.dict_arr_ext.cat_dict_str((arr, {dcyd__ksl}), sep)
"""
    else:
        tfsm__nrki = ' or '.join(['bodo.libs.array_kernels.isna(arr, i)'] +
            [f'bodo.libs.array_kernels.isna(data{i}, i)' for i in range(len
            (others.columns))])
        lipkg__spkxb += (
            '  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)\n'
            )
        lipkg__spkxb += '  numba.parfors.parfor.init_prange()\n'
        lipkg__spkxb += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        lipkg__spkxb += f'      if {tfsm__nrki}:\n'
        lipkg__spkxb += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        lipkg__spkxb += '          continue\n'
        awvq__iiqi = ', '.join(['arr[i]'] + [f'data{i}[i]' for i in range(
            len(others.columns))])
        agjlr__wchng = "''" if is_overload_none(sep) else 'sep'
        lipkg__spkxb += (
            f'      out_arr[i] = {agjlr__wchng}.join([{awvq__iiqi}])\n')
    lipkg__spkxb += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    shdjj__ijqa = {}
    exec(lipkg__spkxb, {'bodo': bodo, 'numba': numba}, shdjj__ijqa)
    impl = shdjj__ijqa['impl']
    return impl


@overload_method(SeriesStrMethodType, 'count', inline='always',
    no_unliteral=True)
def overload_str_method_count(S_str, pat, flags=0):
    str_arg_check('count', 'pat', pat)
    int_arg_check('count', 'flags', flags)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_count_dict_impl(S_str, pat, flags=0):
            S = S_str._obj
            pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
            odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
            gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_count(pxmrw__ewrws, pat, flags
                )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                odq__vgcjf, gsr__skq)
        return _str_count_dict_impl

    def impl(S_str, pat, flags=0):
        S = S_str._obj
        ofw__uqukt = bodo.hiframes.pd_series_ext.get_series_data(S)
        gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
        odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
        fhyz__oduye = re.compile(pat, flags)
        numba.parfors.parfor.init_prange()
        sdo__xfh = len(ofw__uqukt)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(sdo__xfh, np.int64)
        for i in numba.parfors.parfor.internal_prange(sdo__xfh):
            if bodo.libs.array_kernels.isna(ofw__uqukt, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = str_findall_count(fhyz__oduye, ofw__uqukt[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr, odq__vgcjf,
            gsr__skq)
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
            pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
            odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
            gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_find(pxmrw__ewrws, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                odq__vgcjf, gsr__skq)
        return _str_find_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        ofw__uqukt = bodo.hiframes.pd_series_ext.get_series_data(S)
        gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
        odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        sdo__xfh = len(ofw__uqukt)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(sdo__xfh, np.int64)
        for i in numba.parfors.parfor.internal_prange(sdo__xfh):
            if bodo.libs.array_kernels.isna(ofw__uqukt, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = ofw__uqukt[i].find(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, odq__vgcjf,
            gsr__skq)
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
            pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
            odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
            gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_rfind(pxmrw__ewrws, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                odq__vgcjf, gsr__skq)
        return _str_rfind_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        ofw__uqukt = bodo.hiframes.pd_series_ext.get_series_data(S)
        gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
        odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        sdo__xfh = len(ofw__uqukt)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(sdo__xfh, np.int64)
        for i in numba.parfors.parfor.internal_prange(sdo__xfh):
            if bodo.libs.array_kernels.isna(ofw__uqukt, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = ofw__uqukt[i].rfind(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, odq__vgcjf,
            gsr__skq)
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
            pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
            odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
            gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_index(pxmrw__ewrws, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                odq__vgcjf, gsr__skq)
        return _str_index_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        ofw__uqukt = bodo.hiframes.pd_series_ext.get_series_data(S)
        gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
        odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
        sdo__xfh = len(ofw__uqukt)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(sdo__xfh, np.int64)
        numba.parfors.parfor.init_prange()
        zayut__mtkx = False
        for i in numba.parfors.parfor.internal_prange(sdo__xfh):
            if bodo.libs.array_kernels.isna(ofw__uqukt, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = ofw__uqukt[i].find(sub, start, end)
                if out_arr[i] == -1:
                    zayut__mtkx = True
        cmtl__nphnf = 'substring not found' if zayut__mtkx else ''
        synchronize_error_njit('ValueError', cmtl__nphnf)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, odq__vgcjf,
            gsr__skq)
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
            pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
            odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
            gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_rindex(pxmrw__ewrws, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                odq__vgcjf, gsr__skq)
        return _str_rindex_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        ofw__uqukt = bodo.hiframes.pd_series_ext.get_series_data(S)
        gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
        odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
        sdo__xfh = len(ofw__uqukt)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(sdo__xfh, np.int64)
        numba.parfors.parfor.init_prange()
        zayut__mtkx = False
        for i in numba.parfors.parfor.internal_prange(sdo__xfh):
            if bodo.libs.array_kernels.isna(ofw__uqukt, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = ofw__uqukt[i].rindex(sub, start, end)
                if out_arr[i] == -1:
                    zayut__mtkx = True
        cmtl__nphnf = 'substring not found' if zayut__mtkx else ''
        synchronize_error_njit('ValueError', cmtl__nphnf)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, odq__vgcjf,
            gsr__skq)
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
        ofw__uqukt = bodo.hiframes.pd_series_ext.get_series_data(S)
        gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
        odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        sdo__xfh = len(ofw__uqukt)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(sdo__xfh, -1)
        for eks__ctuo in numba.parfors.parfor.internal_prange(sdo__xfh):
            if bodo.libs.array_kernels.isna(ofw__uqukt, eks__ctuo):
                bodo.libs.array_kernels.setna(out_arr, eks__ctuo)
            else:
                if stop is not None:
                    lqy__igmf = ofw__uqukt[eks__ctuo][stop:]
                else:
                    lqy__igmf = ''
                out_arr[eks__ctuo] = ofw__uqukt[eks__ctuo][:start
                    ] + repl + lqy__igmf
        return bodo.hiframes.pd_series_ext.init_series(out_arr, odq__vgcjf,
            gsr__skq)
    return impl


@overload_method(SeriesStrMethodType, 'repeat', inline='always',
    no_unliteral=True)
def overload_str_method_repeat(S_str, repeats):
    if isinstance(repeats, types.Integer) or is_overload_constant_int(repeats):
        if S_str.stype.data == bodo.dict_str_arr_type:

            def _str_repeat_int_dict_impl(S_str, repeats):
                S = S_str._obj
                pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
                odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
                gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
                out_arr = bodo.libs.dict_arr_ext.str_repeat_int(pxmrw__ewrws,
                    repeats)
                return bodo.hiframes.pd_series_ext.init_series(out_arr,
                    odq__vgcjf, gsr__skq)
            return _str_repeat_int_dict_impl

        def impl(S_str, repeats):
            S = S_str._obj
            ofw__uqukt = bodo.hiframes.pd_series_ext.get_series_data(S)
            gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
            odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
            numba.parfors.parfor.init_prange()
            sdo__xfh = len(ofw__uqukt)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(sdo__xfh, -1
                )
            for eks__ctuo in numba.parfors.parfor.internal_prange(sdo__xfh):
                if bodo.libs.array_kernels.isna(ofw__uqukt, eks__ctuo):
                    bodo.libs.array_kernels.setna(out_arr, eks__ctuo)
                else:
                    out_arr[eks__ctuo] = ofw__uqukt[eks__ctuo] * repeats
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                odq__vgcjf, gsr__skq)
        return impl
    elif is_overload_constant_list(repeats):
        qpky__skvqn = get_overload_const_list(repeats)
        hqa__vjcc = all([isinstance(vuisd__uou, int) for vuisd__uou in
            qpky__skvqn])
    elif is_list_like_index_type(repeats) and isinstance(repeats.dtype,
        types.Integer):
        hqa__vjcc = True
    else:
        hqa__vjcc = False
    if hqa__vjcc:

        def impl(S_str, repeats):
            S = S_str._obj
            ofw__uqukt = bodo.hiframes.pd_series_ext.get_series_data(S)
            gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
            odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
            jmi__pby = bodo.utils.conversion.coerce_to_array(repeats)
            numba.parfors.parfor.init_prange()
            sdo__xfh = len(ofw__uqukt)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(sdo__xfh, -1
                )
            for eks__ctuo in numba.parfors.parfor.internal_prange(sdo__xfh):
                if bodo.libs.array_kernels.isna(ofw__uqukt, eks__ctuo):
                    bodo.libs.array_kernels.setna(out_arr, eks__ctuo)
                else:
                    out_arr[eks__ctuo] = ofw__uqukt[eks__ctuo] * jmi__pby[
                        eks__ctuo]
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                odq__vgcjf, gsr__skq)
        return impl
    else:
        raise BodoError(
            'Series.str.repeat(): repeats argument must either be an integer or a sequence of integers'
            )


def create_ljust_rjust_center_overload(func_name):
    lipkg__spkxb = f"""def dict_impl(S_str, width, fillchar=' '):
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
    shdjj__ijqa = {}
    dxtib__rluld = {'bodo': bodo, 'numba': numba}
    exec(lipkg__spkxb, dxtib__rluld, shdjj__ijqa)
    impl = shdjj__ijqa['impl']
    eyxw__evmap = shdjj__ijqa['dict_impl']

    def overload_ljust_rjust_center_method(S_str, width, fillchar=' '):
        common_validate_padding(func_name, width, fillchar)
        if S_str.stype.data == bodo.dict_str_arr_type:
            return eyxw__evmap
        return impl
    return overload_ljust_rjust_center_method


def _install_ljust_rjust_center():
    for hnbc__soqw in ['ljust', 'rjust', 'center']:
        impl = create_ljust_rjust_center_overload(hnbc__soqw)
        overload_method(SeriesStrMethodType, hnbc__soqw, inline='always',
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
            pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
            odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
            gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
            if side == 'left':
                out_arr = bodo.libs.dict_arr_ext.str_rjust(pxmrw__ewrws,
                    width, fillchar)
            elif side == 'right':
                out_arr = bodo.libs.dict_arr_ext.str_ljust(pxmrw__ewrws,
                    width, fillchar)
            elif side == 'both':
                out_arr = bodo.libs.dict_arr_ext.str_center(pxmrw__ewrws,
                    width, fillchar)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                odq__vgcjf, gsr__skq)
        return _str_pad_dict_impl

    def impl(S_str, width, side='left', fillchar=' '):
        S = S_str._obj
        ofw__uqukt = bodo.hiframes.pd_series_ext.get_series_data(S)
        gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
        odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        sdo__xfh = len(ofw__uqukt)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(sdo__xfh, -1)
        for eks__ctuo in numba.parfors.parfor.internal_prange(sdo__xfh):
            if bodo.libs.array_kernels.isna(ofw__uqukt, eks__ctuo):
                out_arr[eks__ctuo] = ''
                bodo.libs.array_kernels.setna(out_arr, eks__ctuo)
            elif side == 'left':
                out_arr[eks__ctuo] = ofw__uqukt[eks__ctuo].rjust(width,
                    fillchar)
            elif side == 'right':
                out_arr[eks__ctuo] = ofw__uqukt[eks__ctuo].ljust(width,
                    fillchar)
            elif side == 'both':
                out_arr[eks__ctuo] = ofw__uqukt[eks__ctuo].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, odq__vgcjf,
            gsr__skq)
    return impl


@overload_method(SeriesStrMethodType, 'zfill', inline='always',
    no_unliteral=True)
def overload_str_method_zfill(S_str, width):
    int_arg_check('zfill', 'width', width)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_zfill_dict_impl(S_str, width):
            S = S_str._obj
            pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
            odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
            gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_zfill(pxmrw__ewrws, width)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                odq__vgcjf, gsr__skq)
        return _str_zfill_dict_impl

    def impl(S_str, width):
        S = S_str._obj
        ofw__uqukt = bodo.hiframes.pd_series_ext.get_series_data(S)
        gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
        odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        sdo__xfh = len(ofw__uqukt)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(sdo__xfh, -1)
        for eks__ctuo in numba.parfors.parfor.internal_prange(sdo__xfh):
            if bodo.libs.array_kernels.isna(ofw__uqukt, eks__ctuo):
                out_arr[eks__ctuo] = ''
                bodo.libs.array_kernels.setna(out_arr, eks__ctuo)
            else:
                out_arr[eks__ctuo] = ofw__uqukt[eks__ctuo].zfill(width)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, odq__vgcjf,
            gsr__skq)
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
            pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
            odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
            gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_slice(pxmrw__ewrws, start,
                stop, step)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                odq__vgcjf, gsr__skq)
        return _str_slice_dict_impl

    def impl(S_str, start=None, stop=None, step=None):
        S = S_str._obj
        ofw__uqukt = bodo.hiframes.pd_series_ext.get_series_data(S)
        gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
        odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        sdo__xfh = len(ofw__uqukt)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(sdo__xfh, -1)
        for eks__ctuo in numba.parfors.parfor.internal_prange(sdo__xfh):
            if bodo.libs.array_kernels.isna(ofw__uqukt, eks__ctuo):
                out_arr[eks__ctuo] = ''
                bodo.libs.array_kernels.setna(out_arr, eks__ctuo)
            else:
                out_arr[eks__ctuo] = ofw__uqukt[eks__ctuo][start:stop:step]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, odq__vgcjf,
            gsr__skq)
    return impl


@overload_method(SeriesStrMethodType, 'startswith', inline='always',
    no_unliteral=True)
def overload_str_method_startswith(S_str, pat, na=np.nan):
    not_supported_arg_check('startswith', 'na', na, np.nan)
    str_arg_check('startswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_startswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
            odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
            gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_startswith(pxmrw__ewrws,
                pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                odq__vgcjf, gsr__skq)
        return _str_startswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        ofw__uqukt = bodo.hiframes.pd_series_ext.get_series_data(S)
        gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
        odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        sdo__xfh = len(ofw__uqukt)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(sdo__xfh)
        for i in numba.parfors.parfor.internal_prange(sdo__xfh):
            if bodo.libs.array_kernels.isna(ofw__uqukt, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = ofw__uqukt[i].startswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, odq__vgcjf,
            gsr__skq)
    return impl


@overload_method(SeriesStrMethodType, 'endswith', inline='always',
    no_unliteral=True)
def overload_str_method_endswith(S_str, pat, na=np.nan):
    not_supported_arg_check('endswith', 'na', na, np.nan)
    str_arg_check('endswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_endswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
            odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
            gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_endswith(pxmrw__ewrws, pat, na
                )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                odq__vgcjf, gsr__skq)
        return _str_endswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        ofw__uqukt = bodo.hiframes.pd_series_ext.get_series_data(S)
        gsr__skq = bodo.hiframes.pd_series_ext.get_series_name(S)
        odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        sdo__xfh = len(ofw__uqukt)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(sdo__xfh)
        for i in numba.parfors.parfor.internal_prange(sdo__xfh):
            if bodo.libs.array_kernels.isna(ofw__uqukt, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = ofw__uqukt[i].endswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, odq__vgcjf,
            gsr__skq)
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
    skama__vjl, regex = _get_column_names_from_regex(pat, flags, 'extract')
    zglhe__rwboh = len(skama__vjl)
    if S_str.stype.data == bodo.dict_str_arr_type:
        lipkg__spkxb = 'def impl(S_str, pat, flags=0, expand=True):\n'
        lipkg__spkxb += '  S = S_str._obj\n'
        lipkg__spkxb += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        lipkg__spkxb += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        lipkg__spkxb += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        lipkg__spkxb += f"""  out_arr_list = bodo.libs.dict_arr_ext.str_extract(arr, pat, flags, {zglhe__rwboh})
"""
        for i in range(zglhe__rwboh):
            lipkg__spkxb += f'  out_arr_{i} = out_arr_list[{i}]\n'
    else:
        lipkg__spkxb = 'def impl(S_str, pat, flags=0, expand=True):\n'
        lipkg__spkxb += '  regex = re.compile(pat, flags=flags)\n'
        lipkg__spkxb += '  S = S_str._obj\n'
        lipkg__spkxb += (
            '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        lipkg__spkxb += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        lipkg__spkxb += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        lipkg__spkxb += '  numba.parfors.parfor.init_prange()\n'
        lipkg__spkxb += '  n = len(str_arr)\n'
        for i in range(zglhe__rwboh):
            lipkg__spkxb += (
                '  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)\n'
                .format(i))
        lipkg__spkxb += '  for j in numba.parfors.parfor.internal_prange(n):\n'
        lipkg__spkxb += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
        for i in range(zglhe__rwboh):
            lipkg__spkxb += "          out_arr_{}[j] = ''\n".format(i)
            lipkg__spkxb += (
                '          bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
                format(i))
        lipkg__spkxb += '      else:\n'
        lipkg__spkxb += '          m = regex.search(str_arr[j])\n'
        lipkg__spkxb += '          if m:\n'
        lipkg__spkxb += '            g = m.groups()\n'
        for i in range(zglhe__rwboh):
            lipkg__spkxb += '            out_arr_{0}[j] = g[{0}]\n'.format(i)
        lipkg__spkxb += '          else:\n'
        for i in range(zglhe__rwboh):
            lipkg__spkxb += "            out_arr_{}[j] = ''\n".format(i)
            lipkg__spkxb += (
                '            bodo.libs.array_kernels.setna(out_arr_{}, j)\n'
                .format(i))
    if is_overload_false(expand) and regex.groups == 1:
        gsr__skq = "'{}'".format(list(regex.groupindex.keys()).pop()) if len(
            regex.groupindex.keys()) > 0 else 'name'
        lipkg__spkxb += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr_0, index, {})\n'
            .format(gsr__skq))
        shdjj__ijqa = {}
        exec(lipkg__spkxb, {'re': re, 'bodo': bodo, 'numba': numba,
            'get_utf8_size': get_utf8_size}, shdjj__ijqa)
        impl = shdjj__ijqa['impl']
        return impl
    mgmjf__lcc = ', '.join('out_arr_{}'.format(i) for i in range(zglhe__rwboh))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(lipkg__spkxb,
        skama__vjl, mgmjf__lcc, 'index', extra_globals={'get_utf8_size':
        get_utf8_size, 're': re})
    return impl


@overload_method(SeriesStrMethodType, 'extractall', inline='always',
    no_unliteral=True)
def overload_str_method_extractall(S_str, pat, flags=0):
    skama__vjl, pqwn__ekjwb = _get_column_names_from_regex(pat, flags,
        'extractall')
    zglhe__rwboh = len(skama__vjl)
    nvq__nzoeg = isinstance(S_str.stype.index, StringIndexType)
    twao__syt = zglhe__rwboh > 1
    gkjwv__njnrv = '_multi' if twao__syt else ''
    if S_str.stype.data == bodo.dict_str_arr_type:
        lipkg__spkxb = 'def impl(S_str, pat, flags=0):\n'
        lipkg__spkxb += '  S = S_str._obj\n'
        lipkg__spkxb += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        lipkg__spkxb += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        lipkg__spkxb += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        lipkg__spkxb += (
            '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
        lipkg__spkxb += (
            '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n'
            )
        lipkg__spkxb += '  regex = re.compile(pat, flags=flags)\n'
        lipkg__spkxb += '  out_ind_arr, out_match_arr, out_arr_list = '
        lipkg__spkxb += (
            f'bodo.libs.dict_arr_ext.str_extractall{gkjwv__njnrv}(\n')
        lipkg__spkxb += f'arr, regex, {zglhe__rwboh}, index_arr)\n'
        for i in range(zglhe__rwboh):
            lipkg__spkxb += f'  out_arr_{i} = out_arr_list[{i}]\n'
        lipkg__spkxb += (
            '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n'
            )
        lipkg__spkxb += (
            "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n")
    else:
        lipkg__spkxb = 'def impl(S_str, pat, flags=0):\n'
        lipkg__spkxb += '  regex = re.compile(pat, flags=flags)\n'
        lipkg__spkxb += '  S = S_str._obj\n'
        lipkg__spkxb += (
            '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        lipkg__spkxb += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        lipkg__spkxb += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        lipkg__spkxb += (
            '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
        lipkg__spkxb += (
            '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n'
            )
        lipkg__spkxb += '  numba.parfors.parfor.init_prange()\n'
        lipkg__spkxb += '  n = len(str_arr)\n'
        lipkg__spkxb += '  out_n_l = [0]\n'
        for i in range(zglhe__rwboh):
            lipkg__spkxb += '  num_chars_{} = 0\n'.format(i)
        if nvq__nzoeg:
            lipkg__spkxb += '  index_num_chars = 0\n'
        lipkg__spkxb += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if nvq__nzoeg:
            lipkg__spkxb += (
                '      index_num_chars += get_utf8_size(index_arr[i])\n')
        lipkg__spkxb += '      if bodo.libs.array_kernels.isna(str_arr, i):\n'
        lipkg__spkxb += '          continue\n'
        lipkg__spkxb += '      m = regex.findall(str_arr[i])\n'
        lipkg__spkxb += '      out_n_l[0] += len(m)\n'
        for i in range(zglhe__rwboh):
            lipkg__spkxb += '      l_{} = 0\n'.format(i)
        lipkg__spkxb += '      for s in m:\n'
        for i in range(zglhe__rwboh):
            lipkg__spkxb += '        l_{} += get_utf8_size(s{})\n'.format(i,
                '[{}]'.format(i) if zglhe__rwboh > 1 else '')
        for i in range(zglhe__rwboh):
            lipkg__spkxb += '      num_chars_{0} += l_{0}\n'.format(i)
        lipkg__spkxb += """  out_n = bodo.libs.distributed_api.local_alloc_size(out_n_l[0], str_arr)
"""
        for i in range(zglhe__rwboh):
            lipkg__spkxb += (
                """  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, num_chars_{0})
"""
                .format(i))
        if nvq__nzoeg:
            lipkg__spkxb += """  out_ind_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, index_num_chars)
"""
        else:
            lipkg__spkxb += (
                '  out_ind_arr = np.empty(out_n, index_arr.dtype)\n')
        lipkg__spkxb += '  out_match_arr = np.empty(out_n, np.int64)\n'
        lipkg__spkxb += '  out_ind = 0\n'
        lipkg__spkxb += '  for j in numba.parfors.parfor.internal_prange(n):\n'
        lipkg__spkxb += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
        lipkg__spkxb += '          continue\n'
        lipkg__spkxb += '      m = regex.findall(str_arr[j])\n'
        lipkg__spkxb += '      for k, s in enumerate(m):\n'
        for i in range(zglhe__rwboh):
            lipkg__spkxb += (
                """        bodo.libs.distributed_api.set_arr_local(out_arr_{}, out_ind, s{})
"""
                .format(i, '[{}]'.format(i) if zglhe__rwboh > 1 else ''))
        lipkg__spkxb += """        bodo.libs.distributed_api.set_arr_local(out_ind_arr, out_ind, index_arr[j])
"""
        lipkg__spkxb += """        bodo.libs.distributed_api.set_arr_local(out_match_arr, out_ind, k)
"""
        lipkg__spkxb += '        out_ind += 1\n'
        lipkg__spkxb += (
            '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n'
            )
        lipkg__spkxb += (
            "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n")
    mgmjf__lcc = ', '.join('out_arr_{}'.format(i) for i in range(zglhe__rwboh))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(lipkg__spkxb,
        skama__vjl, mgmjf__lcc, 'out_index', extra_globals={'get_utf8_size':
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
    lsva__hhbnx = dict(zip(regex.groupindex.values(), regex.groupindex.keys()))
    skama__vjl = [lsva__hhbnx.get(1 + i, i) for i in range(regex.groups)]
    return skama__vjl, regex


def create_str2str_methods_overload(func_name):
    gdpa__jxga = func_name in ['lstrip', 'rstrip', 'strip']
    lipkg__spkxb = f"""def f({'S_str, to_strip=None' if gdpa__jxga else 'S_str'}):
    S = S_str._obj
    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    str_arr = decode_if_dict_array(str_arr)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    numba.parfors.parfor.init_prange()
    n = len(str_arr)
    num_chars = {'-1' if gdpa__jxga else 'num_total_chars(str_arr)'}
    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, num_chars)
    for j in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(str_arr, j):
            out_arr[j] = ""
            bodo.libs.array_kernels.setna(out_arr, j)
        else:
            out_arr[j] = str_arr[j].{func_name}({'to_strip' if gdpa__jxga else ''})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    lipkg__spkxb += f"""def _dict_impl({'S_str, to_strip=None' if gdpa__jxga else 'S_str'}):
    S = S_str._obj
    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    out_arr = bodo.libs.dict_arr_ext.str_{func_name}({'arr, to_strip' if gdpa__jxga else 'arr'})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    shdjj__ijqa = {}
    exec(lipkg__spkxb, {'bodo': bodo, 'numba': numba, 'num_total_chars':
        bodo.libs.str_arr_ext.num_total_chars, 'get_utf8_size': bodo.libs.
        str_arr_ext.get_utf8_size, 'decode_if_dict_array': bodo.utils.
        typing.decode_if_dict_array}, shdjj__ijqa)
    uwuzr__lnps = shdjj__ijqa['f']
    gvj__xphi = shdjj__ijqa['_dict_impl']
    if gdpa__jxga:

        def overload_strip_method(S_str, to_strip=None):
            if not is_overload_none(to_strip):
                str_arg_check(func_name, 'to_strip', to_strip)
            if S_str.stype.data == bodo.dict_str_arr_type:
                return gvj__xphi
            return uwuzr__lnps
        return overload_strip_method
    else:

        def overload_str_method_dict_supported(S_str):
            if S_str.stype.data == bodo.dict_str_arr_type:
                return gvj__xphi
            return uwuzr__lnps
        return overload_str_method_dict_supported


def create_str2bool_methods_overload(func_name):
    lipkg__spkxb = 'def dict_impl(S_str):\n'
    lipkg__spkxb += '    S = S_str._obj\n'
    lipkg__spkxb += (
        '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    lipkg__spkxb += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    lipkg__spkxb += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    lipkg__spkxb += (
        f'    out_arr = bodo.libs.dict_arr_ext.str_{func_name}(arr)\n')
    lipkg__spkxb += (
        '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    lipkg__spkxb += 'def impl(S_str):\n'
    lipkg__spkxb += '    S = S_str._obj\n'
    lipkg__spkxb += (
        '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    lipkg__spkxb += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    lipkg__spkxb += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    lipkg__spkxb += '    numba.parfors.parfor.init_prange()\n'
    lipkg__spkxb += '    l = len(str_arr)\n'
    lipkg__spkxb += (
        '    out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
    lipkg__spkxb += '    for i in numba.parfors.parfor.internal_prange(l):\n'
    lipkg__spkxb += '        if bodo.libs.array_kernels.isna(str_arr, i):\n'
    lipkg__spkxb += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
    lipkg__spkxb += '        else:\n'
    lipkg__spkxb += ('            out_arr[i] = np.bool_(str_arr[i].{}())\n'
        .format(func_name))
    lipkg__spkxb += '    return bodo.hiframes.pd_series_ext.init_series(\n'
    lipkg__spkxb += '      out_arr,index, name)\n'
    shdjj__ijqa = {}
    exec(lipkg__spkxb, {'bodo': bodo, 'numba': numba, 'np': np}, shdjj__ijqa)
    impl = shdjj__ijqa['impl']
    eyxw__evmap = shdjj__ijqa['dict_impl']

    def overload_str2bool_methods(S_str):
        if S_str.stype.data == bodo.dict_str_arr_type:
            return eyxw__evmap
        return impl
    return overload_str2bool_methods


def _install_str2str_methods():
    for ycpb__ydqk in bodo.hiframes.pd_series_ext.str2str_methods:
        ibqzn__oovjq = create_str2str_methods_overload(ycpb__ydqk)
        overload_method(SeriesStrMethodType, ycpb__ydqk, inline='always',
            no_unliteral=True)(ibqzn__oovjq)


def _install_str2bool_methods():
    for ycpb__ydqk in bodo.hiframes.pd_series_ext.str2bool_methods:
        ibqzn__oovjq = create_str2bool_methods_overload(ycpb__ydqk)
        overload_method(SeriesStrMethodType, ycpb__ydqk, inline='always',
            no_unliteral=True)(ibqzn__oovjq)


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
        gsr__skq = 'SeriesCatMethodType({})'.format(stype)
        super(SeriesCatMethodType, self).__init__(gsr__skq)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesCatMethodType)
class SeriesCatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ldk__tnxff = [('obj', fe_type.stype)]
        super(SeriesCatModel, self).__init__(dmm, fe_type, ldk__tnxff)


make_attribute_wrapper(SeriesCatMethodType, 'obj', '_obj')


@intrinsic
def init_series_cat_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        jnx__aln, = args
        kit__tau = signature.return_type
        rxlpj__xug = cgutils.create_struct_proxy(kit__tau)(context, builder)
        rxlpj__xug.obj = jnx__aln
        context.nrt.incref(builder, signature.args[0], jnx__aln)
        return rxlpj__xug._getvalue()
    return SeriesCatMethodType(obj)(obj), codegen


@overload_attribute(SeriesCatMethodType, 'codes')
def series_cat_codes_overload(S_dt):

    def impl(S_dt):
        S = S_dt._obj
        pxmrw__ewrws = bodo.hiframes.pd_series_ext.get_series_data(S)
        odq__vgcjf = bodo.hiframes.pd_series_ext.get_series_index(S)
        gsr__skq = None
        return bodo.hiframes.pd_series_ext.init_series(bodo.hiframes.
            pd_categorical_ext.get_categorical_arr_codes(pxmrw__ewrws),
            odq__vgcjf, gsr__skq)
    return impl


unsupported_cat_attrs = {'categories', 'ordered'}
unsupported_cat_methods = {'rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered'}


def _install_catseries_unsupported():
    for vmyim__hyn in unsupported_cat_attrs:
        hcig__vpr = 'Series.cat.' + vmyim__hyn
        overload_attribute(SeriesCatMethodType, vmyim__hyn)(
            create_unsupported_overload(hcig__vpr))
    for qlpc__jcv in unsupported_cat_methods:
        hcig__vpr = 'Series.cat.' + qlpc__jcv
        overload_method(SeriesCatMethodType, qlpc__jcv)(
            create_unsupported_overload(hcig__vpr))


_install_catseries_unsupported()
unsupported_str_methods = {'casefold', 'decode', 'encode', 'findall',
    'fullmatch', 'index', 'match', 'normalize', 'partition', 'rindex',
    'rpartition', 'slice_replace', 'rsplit', 'translate', 'wrap', 'get_dummies'
    }


def _install_strseries_unsupported():
    for qlpc__jcv in unsupported_str_methods:
        hcig__vpr = 'Series.str.' + qlpc__jcv
        overload_method(SeriesStrMethodType, qlpc__jcv)(
            create_unsupported_overload(hcig__vpr))


_install_strseries_unsupported()
