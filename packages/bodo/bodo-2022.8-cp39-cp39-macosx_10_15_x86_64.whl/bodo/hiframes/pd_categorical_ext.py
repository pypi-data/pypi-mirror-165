import enum
import operator
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.utils.typing import NOT_CONSTANT, BodoError, MetaType, check_unsupported_args, dtype_to_array_type, get_literal_value, get_overload_const, get_overload_const_bool, is_common_scalar_dtype, is_iterable_type, is_list_like_index_type, is_literal_type, is_overload_constant_bool, is_overload_none, is_overload_true, is_scalar_type, raise_bodo_error


class PDCategoricalDtype(types.Opaque):

    def __init__(self, categories, elem_type, ordered, data=None, int_type=None
        ):
        self.categories = categories
        self.elem_type = elem_type
        self.ordered = ordered
        self.data = _get_cat_index_type(elem_type) if data is None else data
        self.int_type = int_type
        pfa__pnglb = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=pfa__pnglb)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    ogbar__jaddz = tuple(val.categories.values)
    elem_type = None if len(ogbar__jaddz) == 0 else bodo.typeof(val.
        categories.values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(ogbar__jaddz, elem_type, val.ordered, bodo.
        typeof(val.categories), int_type)


def _get_cat_index_type(elem_type):
    elem_type = bodo.string_type if elem_type is None else elem_type
    return bodo.utils.typing.get_index_type_from_dtype(elem_type)


@lower_constant(PDCategoricalDtype)
def lower_constant_categorical_type(context, builder, typ, pyval):
    categories = context.get_constant_generic(builder, bodo.typeof(pyval.
        categories), pyval.categories)
    ordered = context.get_constant(types.bool_, pyval.ordered)
    return lir.Constant.literal_struct([categories, ordered])


@register_model(PDCategoricalDtype)
class PDCategoricalDtypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ldf__zxwu = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, ldf__zxwu)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type,
    cat_vals_typ=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ
        ), 'init_cat_dtype requires index type for categories'
    assert is_overload_constant_bool(ordered_typ
        ), 'init_cat_dtype requires constant ordered flag'
    grwx__hwao = None if is_overload_none(int_type) else int_type.dtype
    assert is_overload_none(cat_vals_typ) or isinstance(cat_vals_typ, types
        .TypeRef), 'init_cat_dtype requires constant category values'
    ejyi__opdfe = None if is_overload_none(cat_vals_typ
        ) else cat_vals_typ.instance_type.meta

    def codegen(context, builder, sig, args):
        categories, ordered, dbk__fobb, dbk__fobb = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    qntd__ewfkr = PDCategoricalDtype(ejyi__opdfe, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, grwx__hwao)
    return qntd__ewfkr(categories_typ, ordered_typ, int_type, cat_vals_typ
        ), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    aab__feqxm = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, aab__feqxm).value
    c.pyapi.decref(aab__feqxm)
    frkgi__gaddg = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, frkgi__gaddg
        ).value
    c.pyapi.decref(frkgi__gaddg)
    tib__czgxe = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=tib__czgxe)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    aab__feqxm = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    zwwem__ymk = c.pyapi.from_native_value(typ.data, cat_dtype.categories,
        c.env_manager)
    hqxk__lzwkz = c.context.insert_const_string(c.builder.module, 'pandas')
    cjrm__rgh = c.pyapi.import_module_noblock(hqxk__lzwkz)
    yfhud__ojwxh = c.pyapi.call_method(cjrm__rgh, 'CategoricalDtype', (
        zwwem__ymk, aab__feqxm))
    c.pyapi.decref(aab__feqxm)
    c.pyapi.decref(zwwem__ymk)
    c.pyapi.decref(cjrm__rgh)
    c.context.nrt.decref(c.builder, typ, val)
    return yfhud__ojwxh


@overload_attribute(PDCategoricalDtype, 'nbytes')
def pd_categorical_nbytes_overload(A):
    return lambda A: A.categories.nbytes + bodo.io.np_io.get_dtype_size(types
        .bool_)


class CategoricalArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(CategoricalArrayType, self).__init__(name=
            f'CategoricalArrayType({dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return CategoricalArrayType(self.dtype)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.Categorical)
def _typeof_pd_cat(val, c):
    return CategoricalArrayType(bodo.typeof(val.dtype))


@register_model(CategoricalArrayType)
class CategoricalArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wkm__iug = get_categories_int_type(fe_type.dtype)
        ldf__zxwu = [('dtype', fe_type.dtype), ('codes', types.Array(
            wkm__iug, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, ldf__zxwu)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    tesx__ghxa = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), tesx__ghxa
        ).value
    c.pyapi.decref(tesx__ghxa)
    yfhud__ojwxh = c.pyapi.object_getattr_string(val, 'dtype')
    crto__crxda = c.pyapi.to_native_value(typ.dtype, yfhud__ojwxh).value
    c.pyapi.decref(yfhud__ojwxh)
    lfvdm__uojct = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lfvdm__uojct.codes = codes
    lfvdm__uojct.dtype = crto__crxda
    return NativeValue(lfvdm__uojct._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    lpfw__qnir = get_categories_int_type(typ.dtype)
    iem__jps = context.get_constant_generic(builder, types.Array(lpfw__qnir,
        1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    return lir.Constant.literal_struct([cat_dtype, iem__jps])


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    xhwx__sejtl = len(cat_dtype.categories)
    if xhwx__sejtl < np.iinfo(np.int8).max:
        dtype = types.int8
    elif xhwx__sejtl < np.iinfo(np.int16).max:
        dtype = types.int16
    elif xhwx__sejtl < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    hqxk__lzwkz = c.context.insert_const_string(c.builder.module, 'pandas')
    cjrm__rgh = c.pyapi.import_module_noblock(hqxk__lzwkz)
    wkm__iug = get_categories_int_type(dtype)
    quw__hmia = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    perui__yjh = types.Array(wkm__iug, 1, 'C')
    c.context.nrt.incref(c.builder, perui__yjh, quw__hmia.codes)
    tesx__ghxa = c.pyapi.from_native_value(perui__yjh, quw__hmia.codes, c.
        env_manager)
    c.context.nrt.incref(c.builder, dtype, quw__hmia.dtype)
    yfhud__ojwxh = c.pyapi.from_native_value(dtype, quw__hmia.dtype, c.
        env_manager)
    eqycf__pjyop = c.pyapi.borrow_none()
    rmnh__vuuqz = c.pyapi.object_getattr_string(cjrm__rgh, 'Categorical')
    oio__cke = c.pyapi.call_method(rmnh__vuuqz, 'from_codes', (tesx__ghxa,
        eqycf__pjyop, eqycf__pjyop, yfhud__ojwxh))
    c.pyapi.decref(rmnh__vuuqz)
    c.pyapi.decref(tesx__ghxa)
    c.pyapi.decref(yfhud__ojwxh)
    c.pyapi.decref(cjrm__rgh)
    c.context.nrt.decref(c.builder, typ, val)
    return oio__cke


def _to_readonly(t):
    from bodo.hiframes.pd_index_ext import DatetimeIndexType, NumericIndexType, TimedeltaIndexType
    if isinstance(t, CategoricalArrayType):
        return CategoricalArrayType(_to_readonly(t.dtype))
    if isinstance(t, PDCategoricalDtype):
        return PDCategoricalDtype(t.categories, t.elem_type, t.ordered,
            _to_readonly(t.data), t.int_type)
    if isinstance(t, types.Array):
        return types.Array(t.dtype, t.ndim, 'C', True)
    if isinstance(t, NumericIndexType):
        return NumericIndexType(t.dtype, t.name_typ, _to_readonly(t.data))
    if isinstance(t, (DatetimeIndexType, TimedeltaIndexType)):
        return t.__class__(t.name_typ, _to_readonly(t.data))
    return t


@lower_cast(CategoricalArrayType, CategoricalArrayType)
def cast_cat_arr(context, builder, fromty, toty, val):
    if _to_readonly(toty) == fromty:
        return val
    raise BodoError(f'Cannot cast from {fromty} to {toty}')


def create_cmp_op_overload(op):

    def overload_cat_arr_cmp(A, other):
        if not isinstance(A, CategoricalArrayType):
            return
        if A.dtype.categories and is_literal_type(other) and types.unliteral(
            other) == A.dtype.elem_type:
            val = get_literal_value(other)
            dlvf__izdhm = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                aucf__xrr = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), dlvf__izdhm)
                return aucf__xrr
            return impl_lit

        def impl(A, other):
            dlvf__izdhm = get_code_for_value(A.dtype, other)
            aucf__xrr = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), dlvf__izdhm)
            return aucf__xrr
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        xuxds__dta = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(xuxds__dta)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    quw__hmia = cat_dtype.categories
    n = len(quw__hmia)
    for dol__sfjlh in range(n):
        if quw__hmia[dol__sfjlh] == val:
            return dol__sfjlh
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True, _bodo_nan_to_str=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    xrvh__ocv = bodo.utils.typing.parse_dtype(dtype, 'CategoricalArray.astype')
    if xrvh__ocv != A.dtype.elem_type and xrvh__ocv != types.unicode_type:
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    if xrvh__ocv == types.unicode_type:

        def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
            codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(
                A)
            categories = A.dtype.categories
            n = len(codes)
            aucf__xrr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
            for dol__sfjlh in numba.parfors.parfor.internal_prange(n):
                rwo__zhao = codes[dol__sfjlh]
                if rwo__zhao == -1:
                    if _bodo_nan_to_str:
                        bodo.libs.str_arr_ext.str_arr_setitem_NA_str(aucf__xrr,
                            dol__sfjlh)
                    else:
                        bodo.libs.array_kernels.setna(aucf__xrr, dol__sfjlh)
                    continue
                aucf__xrr[dol__sfjlh] = str(bodo.utils.conversion.
                    unbox_if_timestamp(categories[rwo__zhao]))
            return aucf__xrr
        return impl
    perui__yjh = dtype_to_array_type(xrvh__ocv)

    def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        aucf__xrr = bodo.utils.utils.alloc_type(n, perui__yjh, (-1,))
        for dol__sfjlh in numba.parfors.parfor.internal_prange(n):
            rwo__zhao = codes[dol__sfjlh]
            if rwo__zhao == -1:
                bodo.libs.array_kernels.setna(aucf__xrr, dol__sfjlh)
                continue
            aucf__xrr[dol__sfjlh] = bodo.utils.conversion.unbox_if_timestamp(
                categories[rwo__zhao])
        return aucf__xrr
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        rwkts__cvkiq, crto__crxda = args
        quw__hmia = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        quw__hmia.codes = rwkts__cvkiq
        quw__hmia.dtype = crto__crxda
        context.nrt.incref(builder, signature.args[0], rwkts__cvkiq)
        context.nrt.incref(builder, signature.args[1], crto__crxda)
        return quw__hmia._getvalue()
    yow__grnw = CategoricalArrayType(cat_dtype)
    sig = yow__grnw(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    dirs__rpylm = args[0]
    if equiv_set.has_shape(dirs__rpylm):
        return ArrayAnalysis.AnalyzeResult(shape=dirs__rpylm, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    wkm__iug = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, wkm__iug)
        return init_categorical_array(codes, cat_dtype)
    return impl


def alloc_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_alloc_categorical_array
    ) = alloc_categorical_array_equiv


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_categorical_arr_codes(A):
    return lambda A: A.codes


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_categorical_array',
    'bodo.hiframes.pd_categorical_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_categorical_arr_codes',
    'bodo.hiframes.pd_categorical_ext'] = alias_ext_dummy_func


@overload_method(CategoricalArrayType, 'copy', no_unliteral=True)
def cat_arr_copy_overload(arr):
    return lambda arr: init_categorical_array(arr.codes.copy(), arr.dtype)


def build_replace_dicts(to_replace, value, categories):
    return dict(), np.empty(len(categories) + 1), 0


@overload(build_replace_dicts, no_unliteral=True)
def _build_replace_dicts(to_replace, value, categories):
    if isinstance(to_replace, types.Number) or to_replace == bodo.string_type:

        def impl(to_replace, value, categories):
            return build_replace_dicts([to_replace], value, categories)
        return impl
    else:

        def impl(to_replace, value, categories):
            n = len(categories)
            ghvx__enwei = {}
            iem__jps = np.empty(n + 1, np.int64)
            udi__gnedk = {}
            uxi__jrhhu = []
            ncg__ljnua = {}
            for dol__sfjlh in range(n):
                ncg__ljnua[categories[dol__sfjlh]] = dol__sfjlh
            for mzkms__lgtu in to_replace:
                if mzkms__lgtu != value:
                    if mzkms__lgtu in ncg__ljnua:
                        if value in ncg__ljnua:
                            ghvx__enwei[mzkms__lgtu] = mzkms__lgtu
                            rmmi__ngkd = ncg__ljnua[mzkms__lgtu]
                            udi__gnedk[rmmi__ngkd] = ncg__ljnua[value]
                            uxi__jrhhu.append(rmmi__ngkd)
                        else:
                            ghvx__enwei[mzkms__lgtu] = value
                            ncg__ljnua[value] = ncg__ljnua[mzkms__lgtu]
            msv__gtnq = np.sort(np.array(uxi__jrhhu))
            hvvvu__qqfhr = 0
            quoz__oog = []
            for jlpvf__xwu in range(-1, n):
                while hvvvu__qqfhr < len(msv__gtnq) and jlpvf__xwu > msv__gtnq[
                    hvvvu__qqfhr]:
                    hvvvu__qqfhr += 1
                quoz__oog.append(hvvvu__qqfhr)
            for lqj__zchp in range(-1, n):
                gfg__rxpn = lqj__zchp
                if lqj__zchp in udi__gnedk:
                    gfg__rxpn = udi__gnedk[lqj__zchp]
                iem__jps[lqj__zchp + 1] = gfg__rxpn - quoz__oog[gfg__rxpn + 1]
            return ghvx__enwei, iem__jps, len(msv__gtnq)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for dol__sfjlh in range(len(new_codes_arr)):
        new_codes_arr[dol__sfjlh] = codes_map_arr[old_codes_arr[dol__sfjlh] + 1
            ]


@overload_method(CategoricalArrayType, 'replace', inline='always',
    no_unliteral=True)
def overload_replace(arr, to_replace, value):

    def impl(arr, to_replace, value):
        return bodo.hiframes.pd_categorical_ext.cat_replace(arr, to_replace,
            value)
    return impl


def cat_replace(arr, to_replace, value):
    return


@overload(cat_replace, no_unliteral=True)
def cat_replace_overload(arr, to_replace, value):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(to_replace,
        'CategoricalArray.replace()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'CategoricalArray.replace()')
    kuyvv__yuvgb = arr.dtype.ordered
    rmvbe__rfu = arr.dtype.elem_type
    zkcjd__bfiz = get_overload_const(to_replace)
    sktz__ykyja = get_overload_const(value)
    if (arr.dtype.categories is not None and zkcjd__bfiz is not
        NOT_CONSTANT and sktz__ykyja is not NOT_CONSTANT):
        isbz__norq, codes_map_arr, dbk__fobb = python_build_replace_dicts(
            zkcjd__bfiz, sktz__ykyja, arr.dtype.categories)
        if len(isbz__norq) == 0:
            return lambda arr, to_replace, value: arr.copy()
        zjd__gtm = []
        for aniyl__pjyoc in arr.dtype.categories:
            if aniyl__pjyoc in isbz__norq:
                bglrn__txq = isbz__norq[aniyl__pjyoc]
                if bglrn__txq != aniyl__pjyoc:
                    zjd__gtm.append(bglrn__txq)
            else:
                zjd__gtm.append(aniyl__pjyoc)
        bvn__lawl = bodo.utils.utils.create_categorical_type(zjd__gtm, arr.
            dtype.data.data, kuyvv__yuvgb)
        xxxxb__ujc = MetaType(tuple(bvn__lawl))

        def impl_dtype(arr, to_replace, value):
            zzx__pjg = init_cat_dtype(bodo.utils.conversion.
                index_from_array(bvn__lawl), kuyvv__yuvgb, None, xxxxb__ujc)
            quw__hmia = alloc_categorical_array(len(arr.codes), zzx__pjg)
            reassign_codes(quw__hmia.codes, arr.codes, codes_map_arr)
            return quw__hmia
        return impl_dtype
    rmvbe__rfu = arr.dtype.elem_type
    if rmvbe__rfu == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            ghvx__enwei, codes_map_arr, annas__rhqqy = build_replace_dicts(
                to_replace, value, categories.values)
            if len(ghvx__enwei) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), kuyvv__yuvgb,
                    None, None))
            n = len(categories)
            bvn__lawl = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                annas__rhqqy, -1)
            gnkin__tav = 0
            for jlpvf__xwu in range(n):
                fpei__kezv = categories[jlpvf__xwu]
                if fpei__kezv in ghvx__enwei:
                    fiqc__mdwyj = ghvx__enwei[fpei__kezv]
                    if fiqc__mdwyj != fpei__kezv:
                        bvn__lawl[gnkin__tav] = fiqc__mdwyj
                        gnkin__tav += 1
                else:
                    bvn__lawl[gnkin__tav] = fpei__kezv
                    gnkin__tav += 1
            quw__hmia = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                bvn__lawl), kuyvv__yuvgb, None, None))
            reassign_codes(quw__hmia.codes, arr.codes, codes_map_arr)
            return quw__hmia
        return impl_str
    etg__dharo = dtype_to_array_type(rmvbe__rfu)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        ghvx__enwei, codes_map_arr, annas__rhqqy = build_replace_dicts(
            to_replace, value, categories.values)
        if len(ghvx__enwei) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), kuyvv__yuvgb, None, None))
        n = len(categories)
        bvn__lawl = bodo.utils.utils.alloc_type(n - annas__rhqqy,
            etg__dharo, None)
        gnkin__tav = 0
        for dol__sfjlh in range(n):
            fpei__kezv = categories[dol__sfjlh]
            if fpei__kezv in ghvx__enwei:
                fiqc__mdwyj = ghvx__enwei[fpei__kezv]
                if fiqc__mdwyj != fpei__kezv:
                    bvn__lawl[gnkin__tav] = fiqc__mdwyj
                    gnkin__tav += 1
            else:
                bvn__lawl[gnkin__tav] = fpei__kezv
                gnkin__tav += 1
        quw__hmia = alloc_categorical_array(len(arr.codes), init_cat_dtype(
            bodo.utils.conversion.index_from_array(bvn__lawl), kuyvv__yuvgb,
            None, None))
        reassign_codes(quw__hmia.codes, arr.codes, codes_map_arr)
        return quw__hmia
    return impl


@overload(len, no_unliteral=True)
def overload_cat_arr_len(A):
    if isinstance(A, CategoricalArrayType):
        return lambda A: len(A.codes)


@overload_attribute(CategoricalArrayType, 'shape')
def overload_cat_arr_shape(A):
    return lambda A: (len(A.codes),)


@overload_attribute(CategoricalArrayType, 'ndim')
def overload_cat_arr_ndim(A):
    return lambda A: 1


@overload_attribute(CategoricalArrayType, 'nbytes')
def cat_arr_nbytes_overload(A):
    return lambda A: A.codes.nbytes + A.dtype.nbytes


@register_jitable
def get_label_dict_from_categories(vals):
    kgo__dczs = dict()
    xkmp__blzk = 0
    for dol__sfjlh in range(len(vals)):
        val = vals[dol__sfjlh]
        if val in kgo__dczs:
            continue
        kgo__dczs[val] = xkmp__blzk
        xkmp__blzk += 1
    return kgo__dczs


@register_jitable
def get_label_dict_from_categories_no_duplicates(vals):
    kgo__dczs = dict()
    for dol__sfjlh in range(len(vals)):
        val = vals[dol__sfjlh]
        kgo__dczs[val] = dol__sfjlh
    return kgo__dczs


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    rmww__pawn = dict(fastpath=fastpath)
    gxg__rgq = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', rmww__pawn, gxg__rgq)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        quy__jypyv = get_overload_const(categories)
        if quy__jypyv is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                nvpup__yvhp = False
            else:
                nvpup__yvhp = get_overload_const_bool(ordered)
            jpo__atp = pd.CategoricalDtype(pd.array(quy__jypyv), nvpup__yvhp
                ).categories.array
            xwia__oyjdu = MetaType(tuple(jpo__atp))

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                zzx__pjg = init_cat_dtype(bodo.utils.conversion.
                    index_from_array(jpo__atp), nvpup__yvhp, None, xwia__oyjdu)
                return bodo.utils.conversion.fix_arr_dtype(data, zzx__pjg)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            ogbar__jaddz = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                ogbar__jaddz, ordered, None, None)
            return bodo.utils.conversion.fix_arr_dtype(data, cat_dtype)
        return impl_cats
    elif is_overload_none(ordered):

        def impl_auto(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, 'category')
        return impl_auto
    raise BodoError(
        f'pd.Categorical(): argument combination not supported yet: {values}, {categories}, {ordered}, {dtype}'
        )


@overload(operator.getitem, no_unliteral=True)
def categorical_array_getitem(arr, ind):
    if not isinstance(arr, CategoricalArrayType):
        return
    if isinstance(ind, types.Integer):

        def categorical_getitem_impl(arr, ind):
            ody__jrp = arr.codes[ind]
            return arr.dtype.categories[max(ody__jrp, 0)]
        return categorical_getitem_impl
    if is_list_like_index_type(ind) or isinstance(ind, types.SliceType):

        def impl_bool(arr, ind):
            return init_categorical_array(arr.codes[ind], arr.dtype)
        return impl_bool
    raise BodoError(
        f'getitem for CategoricalArrayType with indexing type {ind} not supported.'
        )


class CategoricalMatchingValues(enum.Enum):
    DIFFERENT_TYPES = -1
    DONT_MATCH = 0
    MAY_MATCH = 1
    DO_MATCH = 2


def categorical_arrs_match(arr1, arr2):
    if not (isinstance(arr1, CategoricalArrayType) and isinstance(arr2,
        CategoricalArrayType)):
        return CategoricalMatchingValues.DIFFERENT_TYPES
    if arr1.dtype.categories is None or arr2.dtype.categories is None:
        return CategoricalMatchingValues.MAY_MATCH
    return (CategoricalMatchingValues.DO_MATCH if arr1.dtype.categories ==
        arr2.dtype.categories and arr1.dtype.ordered == arr2.dtype.ordered else
        CategoricalMatchingValues.DONT_MATCH)


@register_jitable
def cat_dtype_equal(dtype1, dtype2):
    if dtype1.ordered != dtype2.ordered or len(dtype1.categories) != len(dtype2
        .categories):
        return False
    arr1 = dtype1.categories.values
    arr2 = dtype2.categories.values
    for dol__sfjlh in range(len(arr1)):
        if arr1[dol__sfjlh] != arr2[dol__sfjlh]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    dszpi__lktfw = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    szys__line = not isinstance(val, CategoricalArrayType
        ) and is_iterable_type(val) and is_common_scalar_dtype([val.dtype,
        arr.dtype.elem_type]) and not (isinstance(arr.dtype.elem_type,
        types.Integer) and isinstance(val.dtype, types.Float))
    uib__hse = categorical_arrs_match(arr, val)
    yibqd__gfd = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    fkvkw__czkj = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not dszpi__lktfw:
            raise BodoError(yibqd__gfd)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            ody__jrp = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = ody__jrp
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (dszpi__lktfw or szys__line or uib__hse !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(yibqd__gfd)
        if uib__hse == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(fkvkw__czkj)
        if dszpi__lktfw:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                olriq__whsz = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for jlpvf__xwu in range(n):
                    arr.codes[ind[jlpvf__xwu]] = olriq__whsz
            return impl_scalar
        if uib__hse == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for dol__sfjlh in range(n):
                    arr.codes[ind[dol__sfjlh]] = val.codes[dol__sfjlh]
            return impl_arr_ind_mask
        if uib__hse == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(fkvkw__czkj)
                n = len(val.codes)
                for dol__sfjlh in range(n):
                    arr.codes[ind[dol__sfjlh]] = val.codes[dol__sfjlh]
            return impl_arr_ind_mask
        if szys__line:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for jlpvf__xwu in range(n):
                    yiykd__vyl = bodo.utils.conversion.unbox_if_timestamp(val
                        [jlpvf__xwu])
                    if yiykd__vyl not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    ody__jrp = categories.get_loc(yiykd__vyl)
                    arr.codes[ind[jlpvf__xwu]] = ody__jrp
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (dszpi__lktfw or szys__line or uib__hse !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(yibqd__gfd)
        if uib__hse == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(fkvkw__czkj)
        if dszpi__lktfw:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                olriq__whsz = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for jlpvf__xwu in range(n):
                    if ind[jlpvf__xwu]:
                        arr.codes[jlpvf__xwu] = olriq__whsz
            return impl_scalar
        if uib__hse == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                szvzq__atffu = 0
                for dol__sfjlh in range(n):
                    if ind[dol__sfjlh]:
                        arr.codes[dol__sfjlh] = val.codes[szvzq__atffu]
                        szvzq__atffu += 1
            return impl_bool_ind_mask
        if uib__hse == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(fkvkw__czkj)
                n = len(ind)
                szvzq__atffu = 0
                for dol__sfjlh in range(n):
                    if ind[dol__sfjlh]:
                        arr.codes[dol__sfjlh] = val.codes[szvzq__atffu]
                        szvzq__atffu += 1
            return impl_bool_ind_mask
        if szys__line:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                szvzq__atffu = 0
                categories = arr.dtype.categories
                for jlpvf__xwu in range(n):
                    if ind[jlpvf__xwu]:
                        yiykd__vyl = bodo.utils.conversion.unbox_if_timestamp(
                            val[szvzq__atffu])
                        if yiykd__vyl not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        ody__jrp = categories.get_loc(yiykd__vyl)
                        arr.codes[jlpvf__xwu] = ody__jrp
                        szvzq__atffu += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (dszpi__lktfw or szys__line or uib__hse !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(yibqd__gfd)
        if uib__hse == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(fkvkw__czkj)
        if dszpi__lktfw:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                olriq__whsz = arr.dtype.categories.get_loc(val)
                hotu__stwsa = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                for jlpvf__xwu in range(hotu__stwsa.start, hotu__stwsa.stop,
                    hotu__stwsa.step):
                    arr.codes[jlpvf__xwu] = olriq__whsz
            return impl_scalar
        if uib__hse == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if uib__hse == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(fkvkw__czkj)
                arr.codes[ind] = val.codes
            return impl_arr
        if szys__line:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                hotu__stwsa = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                szvzq__atffu = 0
                for jlpvf__xwu in range(hotu__stwsa.start, hotu__stwsa.stop,
                    hotu__stwsa.step):
                    yiykd__vyl = bodo.utils.conversion.unbox_if_timestamp(val
                        [szvzq__atffu])
                    if yiykd__vyl not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    ody__jrp = categories.get_loc(yiykd__vyl)
                    arr.codes[jlpvf__xwu] = ody__jrp
                    szvzq__atffu += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
