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
        beux__mwwcn = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=beux__mwwcn)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    rdrk__thd = tuple(val.categories.values)
    elem_type = None if len(rdrk__thd) == 0 else bodo.typeof(val.categories
        .values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(rdrk__thd, elem_type, val.ordered, bodo.
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
        ukshc__didl = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, ukshc__didl)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type,
    cat_vals_typ=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ
        ), 'init_cat_dtype requires index type for categories'
    assert is_overload_constant_bool(ordered_typ
        ), 'init_cat_dtype requires constant ordered flag'
    qht__errs = None if is_overload_none(int_type) else int_type.dtype
    assert is_overload_none(cat_vals_typ) or isinstance(cat_vals_typ, types
        .TypeRef), 'init_cat_dtype requires constant category values'
    efrt__vdku = None if is_overload_none(cat_vals_typ
        ) else cat_vals_typ.instance_type.meta

    def codegen(context, builder, sig, args):
        categories, ordered, jqaez__bwl, jqaez__bwl = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    ktrz__tsun = PDCategoricalDtype(efrt__vdku, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, qht__errs)
    return ktrz__tsun(categories_typ, ordered_typ, int_type, cat_vals_typ
        ), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lgxf__kzz = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, lgxf__kzz).value
    c.pyapi.decref(lgxf__kzz)
    ikcm__jwggr = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, ikcm__jwggr).value
    c.pyapi.decref(ikcm__jwggr)
    fec__nqq = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=fec__nqq)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    lgxf__kzz = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered, c
        .env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    ohjf__hhddb = c.pyapi.from_native_value(typ.data, cat_dtype.categories,
        c.env_manager)
    hxr__kful = c.context.insert_const_string(c.builder.module, 'pandas')
    euzyv__vggx = c.pyapi.import_module_noblock(hxr__kful)
    jvuhi__oaiic = c.pyapi.call_method(euzyv__vggx, 'CategoricalDtype', (
        ohjf__hhddb, lgxf__kzz))
    c.pyapi.decref(lgxf__kzz)
    c.pyapi.decref(ohjf__hhddb)
    c.pyapi.decref(euzyv__vggx)
    c.context.nrt.decref(c.builder, typ, val)
    return jvuhi__oaiic


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
        acoeu__wzvae = get_categories_int_type(fe_type.dtype)
        ukshc__didl = [('dtype', fe_type.dtype), ('codes', types.Array(
            acoeu__wzvae, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, ukshc__didl)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    pcc__vpir = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), pcc__vpir
        ).value
    c.pyapi.decref(pcc__vpir)
    jvuhi__oaiic = c.pyapi.object_getattr_string(val, 'dtype')
    pmoj__weyvq = c.pyapi.to_native_value(typ.dtype, jvuhi__oaiic).value
    c.pyapi.decref(jvuhi__oaiic)
    heu__riza = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    heu__riza.codes = codes
    heu__riza.dtype = pmoj__weyvq
    return NativeValue(heu__riza._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    yvbvf__amw = get_categories_int_type(typ.dtype)
    xncmw__ovdmx = context.get_constant_generic(builder, types.Array(
        yvbvf__amw, 1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    return lir.Constant.literal_struct([cat_dtype, xncmw__ovdmx])


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    xqj__kaw = len(cat_dtype.categories)
    if xqj__kaw < np.iinfo(np.int8).max:
        dtype = types.int8
    elif xqj__kaw < np.iinfo(np.int16).max:
        dtype = types.int16
    elif xqj__kaw < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    hxr__kful = c.context.insert_const_string(c.builder.module, 'pandas')
    euzyv__vggx = c.pyapi.import_module_noblock(hxr__kful)
    acoeu__wzvae = get_categories_int_type(dtype)
    ftjd__kevx = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    phip__sugx = types.Array(acoeu__wzvae, 1, 'C')
    c.context.nrt.incref(c.builder, phip__sugx, ftjd__kevx.codes)
    pcc__vpir = c.pyapi.from_native_value(phip__sugx, ftjd__kevx.codes, c.
        env_manager)
    c.context.nrt.incref(c.builder, dtype, ftjd__kevx.dtype)
    jvuhi__oaiic = c.pyapi.from_native_value(dtype, ftjd__kevx.dtype, c.
        env_manager)
    apl__wht = c.pyapi.borrow_none()
    rhniy__fferp = c.pyapi.object_getattr_string(euzyv__vggx, 'Categorical')
    ckak__mdv = c.pyapi.call_method(rhniy__fferp, 'from_codes', (pcc__vpir,
        apl__wht, apl__wht, jvuhi__oaiic))
    c.pyapi.decref(rhniy__fferp)
    c.pyapi.decref(pcc__vpir)
    c.pyapi.decref(jvuhi__oaiic)
    c.pyapi.decref(euzyv__vggx)
    c.context.nrt.decref(c.builder, typ, val)
    return ckak__mdv


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
            jis__hyyh = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                mio__urwvy = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), jis__hyyh)
                return mio__urwvy
            return impl_lit

        def impl(A, other):
            jis__hyyh = get_code_for_value(A.dtype, other)
            mio__urwvy = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), jis__hyyh)
            return mio__urwvy
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        ckodu__fycpj = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(ckodu__fycpj)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    ftjd__kevx = cat_dtype.categories
    n = len(ftjd__kevx)
    for dvtj__xjm in range(n):
        if ftjd__kevx[dvtj__xjm] == val:
            return dvtj__xjm
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True, _bodo_nan_to_str=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    eyfu__koqqw = bodo.utils.typing.parse_dtype(dtype,
        'CategoricalArray.astype')
    if eyfu__koqqw != A.dtype.elem_type and eyfu__koqqw != types.unicode_type:
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    if eyfu__koqqw == types.unicode_type:

        def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
            codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(
                A)
            categories = A.dtype.categories
            n = len(codes)
            mio__urwvy = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
            for dvtj__xjm in numba.parfors.parfor.internal_prange(n):
                ctlf__jiwf = codes[dvtj__xjm]
                if ctlf__jiwf == -1:
                    if _bodo_nan_to_str:
                        bodo.libs.str_arr_ext.str_arr_setitem_NA_str(mio__urwvy
                            , dvtj__xjm)
                    else:
                        bodo.libs.array_kernels.setna(mio__urwvy, dvtj__xjm)
                    continue
                mio__urwvy[dvtj__xjm] = str(bodo.utils.conversion.
                    unbox_if_timestamp(categories[ctlf__jiwf]))
            return mio__urwvy
        return impl
    phip__sugx = dtype_to_array_type(eyfu__koqqw)

    def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        mio__urwvy = bodo.utils.utils.alloc_type(n, phip__sugx, (-1,))
        for dvtj__xjm in numba.parfors.parfor.internal_prange(n):
            ctlf__jiwf = codes[dvtj__xjm]
            if ctlf__jiwf == -1:
                bodo.libs.array_kernels.setna(mio__urwvy, dvtj__xjm)
                continue
            mio__urwvy[dvtj__xjm] = bodo.utils.conversion.unbox_if_timestamp(
                categories[ctlf__jiwf])
        return mio__urwvy
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        caciv__cjddp, pmoj__weyvq = args
        ftjd__kevx = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        ftjd__kevx.codes = caciv__cjddp
        ftjd__kevx.dtype = pmoj__weyvq
        context.nrt.incref(builder, signature.args[0], caciv__cjddp)
        context.nrt.incref(builder, signature.args[1], pmoj__weyvq)
        return ftjd__kevx._getvalue()
    idajv__xdqow = CategoricalArrayType(cat_dtype)
    sig = idajv__xdqow(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    qrg__ofq = args[0]
    if equiv_set.has_shape(qrg__ofq):
        return ArrayAnalysis.AnalyzeResult(shape=qrg__ofq, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    acoeu__wzvae = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, acoeu__wzvae)
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
            odegu__xemz = {}
            xncmw__ovdmx = np.empty(n + 1, np.int64)
            pmxxi__gbajq = {}
            semim__zitph = []
            zjifc__mhdlz = {}
            for dvtj__xjm in range(n):
                zjifc__mhdlz[categories[dvtj__xjm]] = dvtj__xjm
            for mmvjy__lxqvp in to_replace:
                if mmvjy__lxqvp != value:
                    if mmvjy__lxqvp in zjifc__mhdlz:
                        if value in zjifc__mhdlz:
                            odegu__xemz[mmvjy__lxqvp] = mmvjy__lxqvp
                            qbsw__ofi = zjifc__mhdlz[mmvjy__lxqvp]
                            pmxxi__gbajq[qbsw__ofi] = zjifc__mhdlz[value]
                            semim__zitph.append(qbsw__ofi)
                        else:
                            odegu__xemz[mmvjy__lxqvp] = value
                            zjifc__mhdlz[value] = zjifc__mhdlz[mmvjy__lxqvp]
            ackr__mrl = np.sort(np.array(semim__zitph))
            igu__iqio = 0
            hoelc__npey = []
            for nbae__ajywz in range(-1, n):
                while igu__iqio < len(ackr__mrl) and nbae__ajywz > ackr__mrl[
                    igu__iqio]:
                    igu__iqio += 1
                hoelc__npey.append(igu__iqio)
            for regao__houi in range(-1, n):
                xyjjm__ccxp = regao__houi
                if regao__houi in pmxxi__gbajq:
                    xyjjm__ccxp = pmxxi__gbajq[regao__houi]
                xncmw__ovdmx[regao__houi + 1] = xyjjm__ccxp - hoelc__npey[
                    xyjjm__ccxp + 1]
            return odegu__xemz, xncmw__ovdmx, len(ackr__mrl)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for dvtj__xjm in range(len(new_codes_arr)):
        new_codes_arr[dvtj__xjm] = codes_map_arr[old_codes_arr[dvtj__xjm] + 1]


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
    dpylf__coy = arr.dtype.ordered
    boj__mzzp = arr.dtype.elem_type
    kwqvz__kph = get_overload_const(to_replace)
    ezokz__llgpp = get_overload_const(value)
    if (arr.dtype.categories is not None and kwqvz__kph is not NOT_CONSTANT and
        ezokz__llgpp is not NOT_CONSTANT):
        knxux__kdnr, codes_map_arr, jqaez__bwl = python_build_replace_dicts(
            kwqvz__kph, ezokz__llgpp, arr.dtype.categories)
        if len(knxux__kdnr) == 0:
            return lambda arr, to_replace, value: arr.copy()
        sqci__pls = []
        for gdog__ipggp in arr.dtype.categories:
            if gdog__ipggp in knxux__kdnr:
                mzz__ags = knxux__kdnr[gdog__ipggp]
                if mzz__ags != gdog__ipggp:
                    sqci__pls.append(mzz__ags)
            else:
                sqci__pls.append(gdog__ipggp)
        xkaj__psc = bodo.utils.utils.create_categorical_type(sqci__pls, arr
            .dtype.data.data, dpylf__coy)
        fsgmi__mqtf = MetaType(tuple(xkaj__psc))

        def impl_dtype(arr, to_replace, value):
            ybopn__kyfv = init_cat_dtype(bodo.utils.conversion.
                index_from_array(xkaj__psc), dpylf__coy, None, fsgmi__mqtf)
            ftjd__kevx = alloc_categorical_array(len(arr.codes), ybopn__kyfv)
            reassign_codes(ftjd__kevx.codes, arr.codes, codes_map_arr)
            return ftjd__kevx
        return impl_dtype
    boj__mzzp = arr.dtype.elem_type
    if boj__mzzp == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            odegu__xemz, codes_map_arr, bwtr__xlj = build_replace_dicts(
                to_replace, value, categories.values)
            if len(odegu__xemz) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), dpylf__coy,
                    None, None))
            n = len(categories)
            xkaj__psc = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                bwtr__xlj, -1)
            zrwje__vrn = 0
            for nbae__ajywz in range(n):
                juvf__qwyw = categories[nbae__ajywz]
                if juvf__qwyw in odegu__xemz:
                    sxlpm__xic = odegu__xemz[juvf__qwyw]
                    if sxlpm__xic != juvf__qwyw:
                        xkaj__psc[zrwje__vrn] = sxlpm__xic
                        zrwje__vrn += 1
                else:
                    xkaj__psc[zrwje__vrn] = juvf__qwyw
                    zrwje__vrn += 1
            ftjd__kevx = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                xkaj__psc), dpylf__coy, None, None))
            reassign_codes(ftjd__kevx.codes, arr.codes, codes_map_arr)
            return ftjd__kevx
        return impl_str
    wzyl__eqpoy = dtype_to_array_type(boj__mzzp)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        odegu__xemz, codes_map_arr, bwtr__xlj = build_replace_dicts(to_replace,
            value, categories.values)
        if len(odegu__xemz) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), dpylf__coy, None, None))
        n = len(categories)
        xkaj__psc = bodo.utils.utils.alloc_type(n - bwtr__xlj, wzyl__eqpoy,
            None)
        zrwje__vrn = 0
        for dvtj__xjm in range(n):
            juvf__qwyw = categories[dvtj__xjm]
            if juvf__qwyw in odegu__xemz:
                sxlpm__xic = odegu__xemz[juvf__qwyw]
                if sxlpm__xic != juvf__qwyw:
                    xkaj__psc[zrwje__vrn] = sxlpm__xic
                    zrwje__vrn += 1
            else:
                xkaj__psc[zrwje__vrn] = juvf__qwyw
                zrwje__vrn += 1
        ftjd__kevx = alloc_categorical_array(len(arr.codes), init_cat_dtype
            (bodo.utils.conversion.index_from_array(xkaj__psc), dpylf__coy,
            None, None))
        reassign_codes(ftjd__kevx.codes, arr.codes, codes_map_arr)
        return ftjd__kevx
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
    vhiue__hzpop = dict()
    gjm__eexf = 0
    for dvtj__xjm in range(len(vals)):
        val = vals[dvtj__xjm]
        if val in vhiue__hzpop:
            continue
        vhiue__hzpop[val] = gjm__eexf
        gjm__eexf += 1
    return vhiue__hzpop


@register_jitable
def get_label_dict_from_categories_no_duplicates(vals):
    vhiue__hzpop = dict()
    for dvtj__xjm in range(len(vals)):
        val = vals[dvtj__xjm]
        vhiue__hzpop[val] = dvtj__xjm
    return vhiue__hzpop


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    noff__fkgoz = dict(fastpath=fastpath)
    izibp__eko = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', noff__fkgoz, izibp__eko)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        wkpru__cyb = get_overload_const(categories)
        if wkpru__cyb is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                dtrsj__cbi = False
            else:
                dtrsj__cbi = get_overload_const_bool(ordered)
            hjo__bwykr = pd.CategoricalDtype(pd.array(wkpru__cyb), dtrsj__cbi
                ).categories.array
            zanc__hixe = MetaType(tuple(hjo__bwykr))

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                ybopn__kyfv = init_cat_dtype(bodo.utils.conversion.
                    index_from_array(hjo__bwykr), dtrsj__cbi, None, zanc__hixe)
                return bodo.utils.conversion.fix_arr_dtype(data, ybopn__kyfv)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            rdrk__thd = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                rdrk__thd, ordered, None, None)
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
            vyk__jzgcz = arr.codes[ind]
            return arr.dtype.categories[max(vyk__jzgcz, 0)]
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
    for dvtj__xjm in range(len(arr1)):
        if arr1[dvtj__xjm] != arr2[dvtj__xjm]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    lnx__ikyh = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    kiq__zlfjx = not isinstance(val, CategoricalArrayType
        ) and is_iterable_type(val) and is_common_scalar_dtype([val.dtype,
        arr.dtype.elem_type]) and not (isinstance(arr.dtype.elem_type,
        types.Integer) and isinstance(val.dtype, types.Float))
    soewg__jim = categorical_arrs_match(arr, val)
    xnixz__aap = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    mlzzr__jwy = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not lnx__ikyh:
            raise BodoError(xnixz__aap)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            vyk__jzgcz = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = vyk__jzgcz
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (lnx__ikyh or kiq__zlfjx or soewg__jim !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(xnixz__aap)
        if soewg__jim == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(mlzzr__jwy)
        if lnx__ikyh:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                nbqj__zenx = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for nbae__ajywz in range(n):
                    arr.codes[ind[nbae__ajywz]] = nbqj__zenx
            return impl_scalar
        if soewg__jim == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for dvtj__xjm in range(n):
                    arr.codes[ind[dvtj__xjm]] = val.codes[dvtj__xjm]
            return impl_arr_ind_mask
        if soewg__jim == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(mlzzr__jwy)
                n = len(val.codes)
                for dvtj__xjm in range(n):
                    arr.codes[ind[dvtj__xjm]] = val.codes[dvtj__xjm]
            return impl_arr_ind_mask
        if kiq__zlfjx:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for nbae__ajywz in range(n):
                    rowkf__ytsx = bodo.utils.conversion.unbox_if_timestamp(val
                        [nbae__ajywz])
                    if rowkf__ytsx not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    vyk__jzgcz = categories.get_loc(rowkf__ytsx)
                    arr.codes[ind[nbae__ajywz]] = vyk__jzgcz
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (lnx__ikyh or kiq__zlfjx or soewg__jim !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(xnixz__aap)
        if soewg__jim == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(mlzzr__jwy)
        if lnx__ikyh:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                nbqj__zenx = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for nbae__ajywz in range(n):
                    if ind[nbae__ajywz]:
                        arr.codes[nbae__ajywz] = nbqj__zenx
            return impl_scalar
        if soewg__jim == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                xzc__uab = 0
                for dvtj__xjm in range(n):
                    if ind[dvtj__xjm]:
                        arr.codes[dvtj__xjm] = val.codes[xzc__uab]
                        xzc__uab += 1
            return impl_bool_ind_mask
        if soewg__jim == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(mlzzr__jwy)
                n = len(ind)
                xzc__uab = 0
                for dvtj__xjm in range(n):
                    if ind[dvtj__xjm]:
                        arr.codes[dvtj__xjm] = val.codes[xzc__uab]
                        xzc__uab += 1
            return impl_bool_ind_mask
        if kiq__zlfjx:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                xzc__uab = 0
                categories = arr.dtype.categories
                for nbae__ajywz in range(n):
                    if ind[nbae__ajywz]:
                        rowkf__ytsx = bodo.utils.conversion.unbox_if_timestamp(
                            val[xzc__uab])
                        if rowkf__ytsx not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        vyk__jzgcz = categories.get_loc(rowkf__ytsx)
                        arr.codes[nbae__ajywz] = vyk__jzgcz
                        xzc__uab += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (lnx__ikyh or kiq__zlfjx or soewg__jim !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(xnixz__aap)
        if soewg__jim == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(mlzzr__jwy)
        if lnx__ikyh:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                nbqj__zenx = arr.dtype.categories.get_loc(val)
                ppcfu__uxuy = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                for nbae__ajywz in range(ppcfu__uxuy.start, ppcfu__uxuy.
                    stop, ppcfu__uxuy.step):
                    arr.codes[nbae__ajywz] = nbqj__zenx
            return impl_scalar
        if soewg__jim == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if soewg__jim == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(mlzzr__jwy)
                arr.codes[ind] = val.codes
            return impl_arr
        if kiq__zlfjx:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                ppcfu__uxuy = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                xzc__uab = 0
                for nbae__ajywz in range(ppcfu__uxuy.start, ppcfu__uxuy.
                    stop, ppcfu__uxuy.step):
                    rowkf__ytsx = bodo.utils.conversion.unbox_if_timestamp(val
                        [xzc__uab])
                    if rowkf__ytsx not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    vyk__jzgcz = categories.get_loc(rowkf__ytsx)
                    arr.codes[nbae__ajywz] = vyk__jzgcz
                    xzc__uab += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
