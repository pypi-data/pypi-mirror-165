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
        tnueg__rnyx = [('left', fe_type.arr_type), ('right', fe_type.arr_type)]
        models.StructModel.__init__(self, dmm, fe_type, tnueg__rnyx)


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
        aiop__azgm, bkt__fbom = args
        eew__mhtj = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        eew__mhtj.left = aiop__azgm
        eew__mhtj.right = bkt__fbom
        context.nrt.incref(builder, signature.args[0], aiop__azgm)
        context.nrt.incref(builder, signature.args[1], bkt__fbom)
        return eew__mhtj._getvalue()
    nte__aebw = IntervalArrayType(left)
    lwqe__lud = nte__aebw(left, right)
    return lwqe__lud, codegen


def init_interval_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    pbfh__hwkkw = []
    for ipx__msk in args:
        qhdlm__vapwa = equiv_set.get_shape(ipx__msk)
        if qhdlm__vapwa is not None:
            pbfh__hwkkw.append(qhdlm__vapwa[0])
    if len(pbfh__hwkkw) > 1:
        equiv_set.insert_equiv(*pbfh__hwkkw)
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
    eew__mhtj = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.arr_type, eew__mhtj.left)
    yznu__qzwd = c.pyapi.from_native_value(typ.arr_type, eew__mhtj.left, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.arr_type, eew__mhtj.right)
    qcs__zidj = c.pyapi.from_native_value(typ.arr_type, eew__mhtj.right, c.
        env_manager)
    ddclb__byp = c.context.insert_const_string(c.builder.module, 'pandas')
    gjh__ryn = c.pyapi.import_module_noblock(ddclb__byp)
    lyptf__leky = c.pyapi.object_getattr_string(gjh__ryn, 'arrays')
    jzb__crx = c.pyapi.object_getattr_string(lyptf__leky, 'IntervalArray')
    hbvnr__eids = c.pyapi.call_method(jzb__crx, 'from_arrays', (yznu__qzwd,
        qcs__zidj))
    c.pyapi.decref(yznu__qzwd)
    c.pyapi.decref(qcs__zidj)
    c.pyapi.decref(gjh__ryn)
    c.pyapi.decref(lyptf__leky)
    c.pyapi.decref(jzb__crx)
    c.context.nrt.decref(c.builder, typ, val)
    return hbvnr__eids


@unbox(IntervalArrayType)
def unbox_interval_arr(typ, val, c):
    yznu__qzwd = c.pyapi.object_getattr_string(val, '_left')
    left = c.pyapi.to_native_value(typ.arr_type, yznu__qzwd).value
    c.pyapi.decref(yznu__qzwd)
    qcs__zidj = c.pyapi.object_getattr_string(val, '_right')
    right = c.pyapi.to_native_value(typ.arr_type, qcs__zidj).value
    c.pyapi.decref(qcs__zidj)
    eew__mhtj = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    eew__mhtj.left = left
    eew__mhtj.right = right
    vywtc__segpv = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(eew__mhtj._getvalue(), is_error=vywtc__segpv)


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
