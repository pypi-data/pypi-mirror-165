"""
Array of intervals corresponding to IntervalArray of Pandas.
Used for IntervalIndex, which is necessary for Series.value_counts() with 'bins'
argument.
"""
import numba
import pandas as pd
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo


class IntervalType(types.Type):

    def __init__(self):
        super(IntervalType, self).__init__('IntervalType()')


class IntervalArrayType(types.ArrayCompatible):

    def __init__(self, arr_type):
        self.arr_type = arr_type
        self.dtype = IntervalType()
        super(IntervalArrayType, self).__init__(name=
            f'IntervalArrayType({arr_type})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return IntervalArrayType(self.arr_type)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(IntervalArrayType)
class IntervalArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ibrk__nsozz = [('left', fe_type.arr_type), ('right', fe_type.arr_type)]
        models.StructModel.__init__(self, dmm, fe_type, ibrk__nsozz)


make_attribute_wrapper(IntervalArrayType, 'left', '_left')
make_attribute_wrapper(IntervalArrayType, 'right', '_right')


@typeof_impl.register(pd.arrays.IntervalArray)
def typeof_interval_array(val, c):
    arr_type = bodo.typeof(val._left)
    return IntervalArrayType(arr_type)


@intrinsic
def init_interval_array(typingctx, left, right=None):
    assert left == right, 'Interval left/right array types should be the same'

    def codegen(context, builder, signature, args):
        ovl__vvs, ist__itxq = args
        ghzat__ydam = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        ghzat__ydam.left = ovl__vvs
        ghzat__ydam.right = ist__itxq
        context.nrt.incref(builder, signature.args[0], ovl__vvs)
        context.nrt.incref(builder, signature.args[1], ist__itxq)
        return ghzat__ydam._getvalue()
    dygxo__thks = IntervalArrayType(left)
    iof__gha = dygxo__thks(left, right)
    return iof__gha, codegen


def init_interval_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    tar__oio = []
    for dit__ckw in args:
        puags__hwk = equiv_set.get_shape(dit__ckw)
        if puags__hwk is not None:
            tar__oio.append(puags__hwk[0])
    if len(tar__oio) > 1:
        equiv_set.insert_equiv(*tar__oio)
    left = args[0]
    if equiv_set.has_shape(left):
        return ArrayAnalysis.AnalyzeResult(shape=left, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_libs_interval_arr_ext_init_interval_array
    ) = init_interval_array_equiv


def alias_ext_init_interval_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_interval_array',
    'bodo.libs.int_arr_ext'] = alias_ext_init_interval_array


@box(IntervalArrayType)
def box_interval_arr(typ, val, c):
    ghzat__ydam = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.arr_type, ghzat__ydam.left)
    lxw__lfi = c.pyapi.from_native_value(typ.arr_type, ghzat__ydam.left, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.arr_type, ghzat__ydam.right)
    kjhpo__tkpph = c.pyapi.from_native_value(typ.arr_type, ghzat__ydam.
        right, c.env_manager)
    jxkil__lrdab = c.context.insert_const_string(c.builder.module, 'pandas')
    tfha__vrc = c.pyapi.import_module_noblock(jxkil__lrdab)
    vuug__sszds = c.pyapi.object_getattr_string(tfha__vrc, 'arrays')
    jxzd__wibii = c.pyapi.object_getattr_string(vuug__sszds, 'IntervalArray')
    lqnc__lzsnk = c.pyapi.call_method(jxzd__wibii, 'from_arrays', (lxw__lfi,
        kjhpo__tkpph))
    c.pyapi.decref(lxw__lfi)
    c.pyapi.decref(kjhpo__tkpph)
    c.pyapi.decref(tfha__vrc)
    c.pyapi.decref(vuug__sszds)
    c.pyapi.decref(jxzd__wibii)
    c.context.nrt.decref(c.builder, typ, val)
    return lqnc__lzsnk


@unbox(IntervalArrayType)
def unbox_interval_arr(typ, val, c):
    lxw__lfi = c.pyapi.object_getattr_string(val, '_left')
    left = c.pyapi.to_native_value(typ.arr_type, lxw__lfi).value
    c.pyapi.decref(lxw__lfi)
    kjhpo__tkpph = c.pyapi.object_getattr_string(val, '_right')
    right = c.pyapi.to_native_value(typ.arr_type, kjhpo__tkpph).value
    c.pyapi.decref(kjhpo__tkpph)
    ghzat__ydam = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ghzat__ydam.left = left
    ghzat__ydam.right = right
    wbv__pzoko = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ghzat__ydam._getvalue(), is_error=wbv__pzoko)


@overload(len, no_unliteral=True)
def overload_interval_arr_len(A):
    if isinstance(A, IntervalArrayType):
        return lambda A: len(A._left)


@overload_attribute(IntervalArrayType, 'shape')
def overload_interval_arr_shape(A):
    return lambda A: (len(A._left),)


@overload_attribute(IntervalArrayType, 'ndim')
def overload_interval_arr_ndim(A):
    return lambda A: 1


@overload_attribute(IntervalArrayType, 'nbytes')
def overload_interval_arr_nbytes(A):
    return lambda A: A._left.nbytes + A._right.nbytes


@overload_method(IntervalArrayType, 'copy', no_unliteral=True)
def overload_interval_arr_copy(A):
    return lambda A: bodo.libs.interval_arr_ext.init_interval_array(A._left
        .copy(), A._right.copy())
