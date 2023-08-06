"""
Collection of utility functions. Needs to be refactored in separate files.
"""
import hashlib
import inspect
import keyword
import re
import warnings
from enum import Enum
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from mpi4py import MPI
from numba.core import cgutils, ir, ir_utils, types
from numba.core.imputils import lower_builtin, lower_constant
from numba.core.ir_utils import find_callname, find_const, get_definition, guard, mk_unique_var, require
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, overload
from numba.np.arrayobj import get_itemsize, make_array, populate_array
from numba.np.numpy_support import as_dtype
import bodo
from bodo.hiframes.time_ext import TimeArrayType
from bodo.libs.binary_arr_ext import bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import num_total_chars, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import string_type
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.typing import NOT_CONSTANT, BodoError, BodoWarning, MetaType, is_str_arr_type
int128_type = types.Integer('int128', 128)


class CTypeEnum(Enum):
    Int8 = 0
    UInt8 = 1
    Int32 = 2
    UInt32 = 3
    Int64 = 4
    UInt64 = 7
    Float32 = 5
    Float64 = 6
    Int16 = 8
    UInt16 = 9
    STRING = 10
    Bool = 11
    Decimal = 12
    Date = 13
    Time = 14
    Datetime = 15
    Timedelta = 16
    Int128 = 17
    LIST = 19
    STRUCT = 20
    BINARY = 21


_numba_to_c_type_map = {types.int8: CTypeEnum.Int8.value, types.uint8:
    CTypeEnum.UInt8.value, types.int32: CTypeEnum.Int32.value, types.uint32:
    CTypeEnum.UInt32.value, types.int64: CTypeEnum.Int64.value, types.
    uint64: CTypeEnum.UInt64.value, types.float32: CTypeEnum.Float32.value,
    types.float64: CTypeEnum.Float64.value, types.NPDatetime('ns'):
    CTypeEnum.Datetime.value, types.NPTimedelta('ns'): CTypeEnum.Timedelta.
    value, types.bool_: CTypeEnum.Bool.value, types.int16: CTypeEnum.Int16.
    value, types.uint16: CTypeEnum.UInt16.value, int128_type: CTypeEnum.
    Int128.value}
numba.core.errors.error_extras = {'unsupported_error': '', 'typing': '',
    'reportable': '', 'interpreter': '', 'constant_inference': ''}
np_alloc_callnames = 'empty', 'zeros', 'ones', 'full'
CONST_DICT_SLOW_WARN_THRESHOLD = 100
CONST_LIST_SLOW_WARN_THRESHOLD = 100000


def unliteral_all(args):
    return tuple(types.unliteral(a) for a in args)


def get_constant(func_ir, var, default=NOT_CONSTANT):
    ydqe__fizg = guard(get_definition, func_ir, var)
    if ydqe__fizg is None:
        return default
    if isinstance(ydqe__fizg, ir.Const):
        return ydqe__fizg.value
    if isinstance(ydqe__fizg, ir.Var):
        return get_constant(func_ir, ydqe__fizg, default)
    return default


def numba_to_c_type(t):
    if isinstance(t, bodo.libs.decimal_arr_ext.Decimal128Type):
        return CTypeEnum.Decimal.value
    if t == bodo.hiframes.datetime_date_ext.datetime_date_type:
        return CTypeEnum.Date.value
    if isinstance(t, bodo.hiframes.time_ext.TimeType):
        return CTypeEnum.Time.value
    return _numba_to_c_type_map[t]


def is_alloc_callname(func_name, mod_name):
    return isinstance(mod_name, str) and (mod_name == 'numpy' and func_name in
        np_alloc_callnames or func_name == 'empty_inferred' and mod_name in
        ('numba.extending', 'numba.np.unsafe.ndarray') or func_name ==
        'pre_alloc_string_array' and mod_name == 'bodo.libs.str_arr_ext' or
        func_name == 'pre_alloc_binary_array' and mod_name ==
        'bodo.libs.binary_arr_ext' or func_name ==
        'alloc_random_access_string_array' and mod_name ==
        'bodo.libs.str_ext' or func_name == 'pre_alloc_array_item_array' and
        mod_name == 'bodo.libs.array_item_arr_ext' or func_name ==
        'pre_alloc_struct_array' and mod_name == 'bodo.libs.struct_arr_ext' or
        func_name == 'pre_alloc_map_array' and mod_name ==
        'bodo.libs.map_arr_ext' or func_name == 'pre_alloc_tuple_array' and
        mod_name == 'bodo.libs.tuple_arr_ext' or func_name ==
        'alloc_bool_array' and mod_name == 'bodo.libs.bool_arr_ext' or 
        func_name == 'alloc_int_array' and mod_name ==
        'bodo.libs.int_arr_ext' or func_name == 'alloc_datetime_date_array' and
        mod_name == 'bodo.hiframes.datetime_date_ext' or func_name ==
        'alloc_datetime_timedelta_array' and mod_name ==
        'bodo.hiframes.datetime_timedelta_ext' or func_name ==
        'alloc_decimal_array' and mod_name == 'bodo.libs.decimal_arr_ext' or
        func_name == 'alloc_categorical_array' and mod_name ==
        'bodo.hiframes.pd_categorical_ext' or func_name == 'gen_na_array' and
        mod_name == 'bodo.libs.array_kernels')


def find_build_tuple(func_ir, var):
    require(isinstance(var, (ir.Var, str)))
    yqc__pgomf = get_definition(func_ir, var)
    require(isinstance(yqc__pgomf, ir.Expr))
    require(yqc__pgomf.op == 'build_tuple')
    return yqc__pgomf.items


def cprint(*s):
    print(*s)


@infer_global(cprint)
class CprintInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.none, *unliteral_all(args))


typ_to_format = {types.int32: 'd', types.uint32: 'u', types.int64: 'lld',
    types.uint64: 'llu', types.float32: 'f', types.float64: 'lf', types.
    voidptr: 's'}


@lower_builtin(cprint, types.VarArg(types.Any))
def cprint_lower(context, builder, sig, args):
    for ytc__rmuf, val in enumerate(args):
        typ = sig.args[ytc__rmuf]
        if isinstance(typ, types.ArrayCTypes):
            cgutils.printf(builder, '%p ', val)
            continue
        fvgi__zhlq = typ_to_format[typ]
        cgutils.printf(builder, '%{} '.format(fvgi__zhlq), val)
    cgutils.printf(builder, '\n')
    return context.get_dummy_value()


def is_whole_slice(typemap, func_ir, var, accept_stride=False):
    require(typemap[var.name] == types.slice2_type or accept_stride and 
        typemap[var.name] == types.slice3_type)
    ejx__nqa = get_definition(func_ir, var)
    require(isinstance(ejx__nqa, ir.Expr) and ejx__nqa.op == 'call')
    assert len(ejx__nqa.args) == 2 or accept_stride and len(ejx__nqa.args) == 3
    assert find_callname(func_ir, ejx__nqa) == ('slice', 'builtins')
    yylvm__pakz = get_definition(func_ir, ejx__nqa.args[0])
    mqft__ccpbw = get_definition(func_ir, ejx__nqa.args[1])
    require(isinstance(yylvm__pakz, ir.Const) and yylvm__pakz.value == None)
    require(isinstance(mqft__ccpbw, ir.Const) and mqft__ccpbw.value == None)
    return True


def is_slice_equiv_arr(arr_var, index_var, func_ir, equiv_set,
    accept_stride=False):
    zcvzv__gmeh = get_definition(func_ir, index_var)
    require(find_callname(func_ir, zcvzv__gmeh) == ('slice', 'builtins'))
    require(len(zcvzv__gmeh.args) in (2, 3))
    require(find_const(func_ir, zcvzv__gmeh.args[0]) in (0, None))
    require(equiv_set.is_equiv(zcvzv__gmeh.args[1], arr_var.name + '#0'))
    require(accept_stride or len(zcvzv__gmeh.args) == 2 or find_const(
        func_ir, zcvzv__gmeh.args[2]) == 1)
    return True


def get_slice_step(typemap, func_ir, var):
    require(typemap[var.name] == types.slice3_type)
    ejx__nqa = get_definition(func_ir, var)
    require(isinstance(ejx__nqa, ir.Expr) and ejx__nqa.op == 'call')
    assert len(ejx__nqa.args) == 3
    return ejx__nqa.args[2]


def is_array_typ(var_typ, include_index_series=True):
    return is_np_array_typ(var_typ) or var_typ in (string_array_type, bodo.
        binary_array_type, bodo.dict_str_arr_type, bodo.hiframes.split_impl
        .string_array_split_view_type, bodo.hiframes.datetime_date_ext.
        datetime_date_array_type, bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_array_type, boolean_array, bodo.libs.str_ext.
        random_access_string_array, bodo.libs.interval_arr_ext.
        IntervalArrayType) or isinstance(var_typ, (IntegerArrayType, bodo.
        libs.decimal_arr_ext.DecimalArrayType, bodo.hiframes.
        pd_categorical_ext.CategoricalArrayType, bodo.libs.
        array_item_arr_ext.ArrayItemArrayType, bodo.libs.struct_arr_ext.
        StructArrayType, bodo.libs.interval_arr_ext.IntervalArrayType, bodo
        .libs.tuple_arr_ext.TupleArrayType, bodo.libs.map_arr_ext.
        MapArrayType, bodo.libs.csr_matrix_ext.CSRMatrixType, bodo.
        DatetimeArrayType, TimeArrayType)) or include_index_series and (
        isinstance(var_typ, (bodo.hiframes.pd_series_ext.SeriesType, bodo.
        hiframes.pd_multi_index_ext.MultiIndexType)) or bodo.hiframes.
        pd_index_ext.is_pd_index_type(var_typ))


def is_np_array_typ(var_typ):
    return isinstance(var_typ, types.Array)


def is_distributable_typ(var_typ):
    return is_array_typ(var_typ) or isinstance(var_typ, bodo.hiframes.table
        .TableType) or isinstance(var_typ, bodo.hiframes.pd_dataframe_ext.
        DataFrameType) or isinstance(var_typ, types.List
        ) and is_distributable_typ(var_typ.dtype) or isinstance(var_typ,
        types.DictType) and is_distributable_typ(var_typ.value_type)


def is_distributable_tuple_typ(var_typ):
    try:
        from bodosql.context_ext import BodoSQLContextType
    except ImportError as ngh__uxe:
        BodoSQLContextType = None
    return isinstance(var_typ, types.BaseTuple) and any(
        is_distributable_typ(t) or is_distributable_tuple_typ(t) for t in
        var_typ.types) or isinstance(var_typ, types.List
        ) and is_distributable_tuple_typ(var_typ.dtype) or isinstance(var_typ,
        types.DictType) and is_distributable_tuple_typ(var_typ.value_type
        ) or isinstance(var_typ, types.iterators.EnumerateType) and (
        is_distributable_typ(var_typ.yield_type[1]) or
        is_distributable_tuple_typ(var_typ.yield_type[1])
        ) or BodoSQLContextType is not None and isinstance(var_typ,
        BodoSQLContextType) and any([is_distributable_typ(nif__vcpw) for
        nif__vcpw in var_typ.dataframes])


@numba.generated_jit(nopython=True, cache=True)
def build_set_seen_na(A):

    def impl(A):
        s = dict()
        cgsp__fchd = False
        for ytc__rmuf in range(len(A)):
            if bodo.libs.array_kernels.isna(A, ytc__rmuf):
                cgsp__fchd = True
                continue
            s[A[ytc__rmuf]] = 0
        return s, cgsp__fchd
    return impl


def empty_like_type(n, arr):
    return np.empty(n, arr.dtype)


@overload(empty_like_type, no_unliteral=True)
def empty_like_type_overload(n, arr):
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return (lambda n, arr: bodo.hiframes.pd_categorical_ext.
            alloc_categorical_array(n, arr.dtype))
    if isinstance(arr, types.Array):
        return lambda n, arr: np.empty(n, arr.dtype)
    if isinstance(arr, types.List) and arr.dtype == string_type:

        def empty_like_type_str_list(n, arr):
            return [''] * n
        return empty_like_type_str_list
    if isinstance(arr, types.List) and arr.dtype == bytes_type:

        def empty_like_type_binary_list(n, arr):
            return [b''] * n
        return empty_like_type_binary_list
    if isinstance(arr, IntegerArrayType):
        zeqt__bsver = arr.dtype

        def empty_like_type_int_arr(n, arr):
            return bodo.libs.int_arr_ext.alloc_int_array(n, zeqt__bsver)
        return empty_like_type_int_arr
    if arr == boolean_array:

        def empty_like_type_bool_arr(n, arr):
            return bodo.libs.bool_arr_ext.alloc_bool_array(n)
        return empty_like_type_bool_arr
    if arr == bodo.hiframes.datetime_date_ext.datetime_date_array_type:

        def empty_like_type_datetime_date_arr(n, arr):
            return bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(n)
        return empty_like_type_datetime_date_arr
    if isinstance(arr, bodo.hiframes.time_ext.TimeArrayType):

        def empty_like_type_time_arr(n, arr):
            return bodo.hiframes.time_ext.alloc_time_array(n)
        return empty_like_type_time_arr
    if (arr == bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_array_type):

        def empty_like_type_datetime_timedelta_arr(n, arr):
            return (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(n))
        return empty_like_type_datetime_timedelta_arr
    if isinstance(arr, bodo.libs.decimal_arr_ext.DecimalArrayType):
        precision = arr.precision
        scale = arr.scale

        def empty_like_type_decimal_arr(n, arr):
            return bodo.libs.decimal_arr_ext.alloc_decimal_array(n,
                precision, scale)
        return empty_like_type_decimal_arr
    assert arr == string_array_type

    def empty_like_type_str_arr(n, arr):
        xiu__cjxt = 20
        if len(arr) != 0:
            xiu__cjxt = num_total_chars(arr) // len(arr)
        return pre_alloc_string_array(n, n * xiu__cjxt)
    return empty_like_type_str_arr


def _empty_nd_impl(context, builder, arrtype, shapes):
    wochi__hbyq = make_array(arrtype)
    aeiu__kwkxl = wochi__hbyq(context, builder)
    vmzdx__uun = context.get_data_type(arrtype.dtype)
    ytbgc__sgpx = context.get_constant(types.intp, get_itemsize(context,
        arrtype))
    kaubr__zpqdr = context.get_constant(types.intp, 1)
    gfo__fphj = lir.Constant(lir.IntType(1), 0)
    for s in shapes:
        pnwue__uylz = builder.smul_with_overflow(kaubr__zpqdr, s)
        kaubr__zpqdr = builder.extract_value(pnwue__uylz, 0)
        gfo__fphj = builder.or_(gfo__fphj, builder.extract_value(
            pnwue__uylz, 1))
    if arrtype.ndim == 0:
        ham__bhcg = ()
    elif arrtype.layout == 'C':
        ham__bhcg = [ytbgc__sgpx]
        for lgms__izshm in reversed(shapes[1:]):
            ham__bhcg.append(builder.mul(ham__bhcg[-1], lgms__izshm))
        ham__bhcg = tuple(reversed(ham__bhcg))
    elif arrtype.layout == 'F':
        ham__bhcg = [ytbgc__sgpx]
        for lgms__izshm in shapes[:-1]:
            ham__bhcg.append(builder.mul(ham__bhcg[-1], lgms__izshm))
        ham__bhcg = tuple(ham__bhcg)
    else:
        raise NotImplementedError(
            "Don't know how to allocate array with layout '{0}'.".format(
            arrtype.layout))
    vko__qru = builder.smul_with_overflow(kaubr__zpqdr, ytbgc__sgpx)
    jkfi__hxs = builder.extract_value(vko__qru, 0)
    gfo__fphj = builder.or_(gfo__fphj, builder.extract_value(vko__qru, 1))
    with builder.if_then(gfo__fphj, likely=False):
        cgutils.printf(builder,
            'array is too big; `arr.size * arr.dtype.itemsize` is larger than the maximum possible size.'
            )
    dtype = arrtype.dtype
    pvwn__fdmnf = context.get_preferred_array_alignment(dtype)
    prass__nyttg = context.get_constant(types.uint32, pvwn__fdmnf)
    ggcyl__irjjx = context.nrt.meminfo_alloc_aligned(builder, size=
        jkfi__hxs, align=prass__nyttg)
    data = context.nrt.meminfo_data(builder, ggcyl__irjjx)
    jol__fvbn = context.get_value_type(types.intp)
    jgkh__xeln = cgutils.pack_array(builder, shapes, ty=jol__fvbn)
    cntw__wxh = cgutils.pack_array(builder, ham__bhcg, ty=jol__fvbn)
    populate_array(aeiu__kwkxl, data=builder.bitcast(data, vmzdx__uun.
        as_pointer()), shape=jgkh__xeln, strides=cntw__wxh, itemsize=
        ytbgc__sgpx, meminfo=ggcyl__irjjx)
    return aeiu__kwkxl


if bodo.numba_compat._check_numba_change:
    lines = inspect.getsource(numba.np.arrayobj._empty_nd_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b6a998927680caa35917a553c79704e9d813d8f1873d83a5f8513837c159fa29':
        warnings.warn('numba.np.arrayobj._empty_nd_impl has changed')


def alloc_arr_tup(n, arr_tup, init_vals=()):
    rucf__fjky = []
    for yxtj__qjh in arr_tup:
        rucf__fjky.append(np.empty(n, yxtj__qjh.dtype))
    return tuple(rucf__fjky)


@overload(alloc_arr_tup, no_unliteral=True)
def alloc_arr_tup_overload(n, data, init_vals=()):
    wqu__uvjpa = data.count
    cuoqk__sogll = ','.join(['empty_like_type(n, data[{}])'.format(
        ytc__rmuf) for ytc__rmuf in range(wqu__uvjpa)])
    if init_vals != ():
        cuoqk__sogll = ','.join([
            'np.full(n, init_vals[{}], data[{}].dtype)'.format(ytc__rmuf,
            ytc__rmuf) for ytc__rmuf in range(wqu__uvjpa)])
    gagi__sun = 'def f(n, data, init_vals=()):\n'
    gagi__sun += '  return ({}{})\n'.format(cuoqk__sogll, ',' if wqu__uvjpa ==
        1 else '')
    cgvpa__pahtl = {}
    exec(gagi__sun, {'empty_like_type': empty_like_type, 'np': np},
        cgvpa__pahtl)
    clht__nhnu = cgvpa__pahtl['f']
    return clht__nhnu


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def tuple_to_scalar(n):
    if isinstance(n, types.BaseTuple) and len(n.types) == 1:
        return lambda n: n[0]
    return lambda n: n


def create_categorical_type(categories, data, is_ordered):
    if data == bodo.string_array_type or bodo.utils.typing.is_dtype_nullable(
        data):
        new_cats_arr = pd.CategoricalDtype(pd.array(categories), is_ordered
            ).categories.array
        if isinstance(data.dtype, types.Number):
            new_cats_arr = new_cats_arr.astype(data.
                get_pandas_scalar_type_instance)
    else:
        new_cats_arr = pd.CategoricalDtype(categories, is_ordered
            ).categories.values
        if isinstance(data.dtype, types.Number):
            new_cats_arr = new_cats_arr.astype(as_dtype(data.dtype))
    return new_cats_arr


def alloc_type(n, t, s=None):
    return np.empty(n, t.dtype)


@overload(alloc_type)
def overload_alloc_type(n, t, s=None):
    typ = t.instance_type if isinstance(t, types.TypeRef) else t
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(typ,
        'bodo.alloc_type()')
    if is_str_arr_type(typ):
        return (lambda n, t, s=None: bodo.libs.str_arr_ext.
            pre_alloc_string_array(n, s[0]))
    if typ == bodo.binary_array_type:
        return (lambda n, t, s=None: bodo.libs.binary_arr_ext.
            pre_alloc_binary_array(n, s[0]))
    if isinstance(typ, bodo.libs.array_item_arr_ext.ArrayItemArrayType):
        dtype = typ.dtype
        return (lambda n, t, s=None: bodo.libs.array_item_arr_ext.
            pre_alloc_array_item_array(n, s, dtype))
    if isinstance(typ, bodo.libs.struct_arr_ext.StructArrayType):
        dtypes = typ.data
        names = typ.names
        return (lambda n, t, s=None: bodo.libs.struct_arr_ext.
            pre_alloc_struct_array(n, s, dtypes, names))
    if isinstance(typ, bodo.libs.map_arr_ext.MapArrayType):
        struct_typ = bodo.libs.struct_arr_ext.StructArrayType((typ.
            key_arr_type, typ.value_arr_type), ('key', 'value'))
        return lambda n, t, s=None: bodo.libs.map_arr_ext.pre_alloc_map_array(n
            , s, struct_typ)
    if isinstance(typ, bodo.libs.tuple_arr_ext.TupleArrayType):
        dtypes = typ.data
        return (lambda n, t, s=None: bodo.libs.tuple_arr_ext.
            pre_alloc_tuple_array(n, s, dtypes))
    if isinstance(typ, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        if isinstance(t, types.TypeRef):
            if typ.dtype.categories is None:
                raise BodoError(
                    'UDFs or Groupbys that return Categorical values must have categories known at compile time.'
                    )
            is_ordered = typ.dtype.ordered
            int_type = typ.dtype.int_type
            new_cats_arr = create_categorical_type(typ.dtype.categories,
                typ.dtype.data.data, is_ordered)
            new_cats_tup = MetaType(tuple(new_cats_arr))
            return (lambda n, t, s=None: bodo.hiframes.pd_categorical_ext.
                alloc_categorical_array(n, bodo.hiframes.pd_categorical_ext
                .init_cat_dtype(bodo.utils.conversion.index_from_array(
                new_cats_arr), is_ordered, int_type, new_cats_tup)))
        else:
            return (lambda n, t, s=None: bodo.hiframes.pd_categorical_ext.
                alloc_categorical_array(n, t.dtype))
    if typ.dtype == bodo.hiframes.datetime_date_ext.datetime_date_type:
        return (lambda n, t, s=None: bodo.hiframes.datetime_date_ext.
            alloc_datetime_date_array(n))
    if isinstance(typ.dtype, bodo.hiframes.time_ext.TimeType):
        return lambda n, t, s=None: bodo.hiframes.time_ext.alloc_time_array(n)
    if (typ.dtype == bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_type):
        return (lambda n, t, s=None: bodo.hiframes.datetime_timedelta_ext.
            alloc_datetime_timedelta_array(n))
    if isinstance(typ, DecimalArrayType):
        precision = typ.dtype.precision
        scale = typ.dtype.scale
        return (lambda n, t, s=None: bodo.libs.decimal_arr_ext.
            alloc_decimal_array(n, precision, scale))
    dtype = numba.np.numpy_support.as_dtype(typ.dtype)
    if isinstance(typ, IntegerArrayType):
        return lambda n, t, s=None: bodo.libs.int_arr_ext.alloc_int_array(n,
            dtype)
    if typ == boolean_array:
        return lambda n, t, s=None: bodo.libs.bool_arr_ext.alloc_bool_array(n)
    return lambda n, t, s=None: np.empty(n, dtype)


def astype(A, t):
    return A.astype(t.dtype)


@overload(astype, no_unliteral=True)
def overload_astype(A, t):
    typ = t.instance_type if isinstance(t, types.TypeRef) else t
    dtype = typ.dtype
    if A == typ:
        return lambda A, t: A
    if isinstance(A, (types.Array, IntegerArrayType)) and isinstance(typ,
        types.Array):
        return lambda A, t: A.astype(dtype)
    if isinstance(typ, IntegerArrayType):
        return lambda A, t: bodo.libs.int_arr_ext.init_integer_array(A.
            astype(dtype), np.full(len(A) + 7 >> 3, 255, np.uint8))
    if (A == bodo.libs.dict_arr_ext.dict_str_arr_type and typ == bodo.
        string_array_type):
        return lambda A, t: bodo.utils.typing.decode_if_dict_array(A)
    raise BodoError(f'cannot convert array type {A} to {typ}')


def full_type(n, val, t):
    return np.full(n, val, t.dtype)


@overload(full_type, no_unliteral=True)
def overload_full_type(n, val, t):
    typ = t.instance_type if isinstance(t, types.TypeRef) else t
    if isinstance(typ, types.Array):
        dtype = numba.np.numpy_support.as_dtype(typ.dtype)
        return lambda n, val, t: np.full(n, val, dtype)
    if isinstance(typ, IntegerArrayType):
        dtype = numba.np.numpy_support.as_dtype(typ.dtype)
        return lambda n, val, t: bodo.libs.int_arr_ext.init_integer_array(np
            .full(n, val, dtype), np.full(tuple_to_scalar(n) + 7 >> 3, 255,
            np.uint8))
    if typ == boolean_array:
        return lambda n, val, t: bodo.libs.bool_arr_ext.init_bool_array(np.
            full(n, val, np.bool_), np.full(tuple_to_scalar(n) + 7 >> 3, 
            255, np.uint8))
    if typ == string_array_type:

        def impl_str(n, val, t):
            yum__chb = n * bodo.libs.str_arr_ext.get_utf8_size(val)
            A = pre_alloc_string_array(n, yum__chb)
            for ytc__rmuf in range(n):
                A[ytc__rmuf] = val
            return A
        return impl_str

    def impl(n, val, t):
        A = alloc_type(n, typ, (-1,))
        for ytc__rmuf in range(n):
            A[ytc__rmuf] = val
        return A
    return impl


@intrinsic
def is_null_pointer(typingctx, ptr_typ=None):

    def codegen(context, builder, signature, args):
        joixx__lnys, = args
        hrrmf__ztnd = context.get_constant_null(ptr_typ)
        return builder.icmp_unsigned('==', joixx__lnys, hrrmf__ztnd)
    return types.bool_(ptr_typ), codegen


@intrinsic
def is_null_value(typingctx, val_typ=None):

    def codegen(context, builder, signature, args):
        val, = args
        nck__mdzny = cgutils.alloca_once_value(builder, val)
        ocp__rbvr = cgutils.alloca_once_value(builder, context.
            get_constant_null(val_typ))
        return is_ll_eq(builder, nck__mdzny, ocp__rbvr)
    return types.bool_(val_typ), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def tuple_list_to_array(A, data, elem_type):
    elem_type = elem_type.instance_type if isinstance(elem_type, types.TypeRef
        ) else elem_type
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'tuple_list_to_array()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(elem_type,
        'tuple_list_to_array()')
    gagi__sun = 'def impl(A, data, elem_type):\n'
    gagi__sun += '  for i, d in enumerate(data):\n'
    if elem_type == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        gagi__sun += '    A[i] = bodo.utils.conversion.unbox_if_timestamp(d)\n'
    else:
        gagi__sun += '    A[i] = d\n'
    cgvpa__pahtl = {}
    exec(gagi__sun, {'bodo': bodo}, cgvpa__pahtl)
    impl = cgvpa__pahtl['impl']
    return impl


def object_length(c, obj):
    nvmo__qybn = c.context.get_argument_type(types.pyobject)
    yfu__pfsbo = lir.FunctionType(lir.IntType(64), [nvmo__qybn])
    zcxib__ohhr = cgutils.get_or_insert_function(c.builder.module,
        yfu__pfsbo, name='PyObject_Length')
    return c.builder.call(zcxib__ohhr, (obj,))


@intrinsic
def incref(typingctx, data=None):

    def codegen(context, builder, signature, args):
        tpnk__mjm, = args
        context.nrt.incref(builder, signature.args[0], tpnk__mjm)
    return types.void(data), codegen


def gen_getitem(out_var, in_var, ind, calltypes, nodes):
    ibz__sxcrg = out_var.loc
    oiq__oib = ir.Expr.static_getitem(in_var, ind, None, ibz__sxcrg)
    calltypes[oiq__oib] = None
    nodes.append(ir.Assign(oiq__oib, out_var, ibz__sxcrg))


def is_static_getsetitem(node):
    return is_expr(node, 'static_getitem') or isinstance(node, ir.StaticSetItem
        )


def get_getsetitem_index_var(node, typemap, nodes):
    index_var = node.index_var if is_static_getsetitem(node) else node.index
    if index_var is None:
        assert is_static_getsetitem(node)
        try:
            oxyxq__jtv = types.literal(node.index)
        except:
            oxyxq__jtv = numba.typeof(node.index)
        index_var = ir.Var(node.value.scope, ir_utils.mk_unique_var(
            'dummy_index'), node.loc)
        typemap[index_var.name] = oxyxq__jtv
        nodes.append(ir.Assign(ir.Const(node.index, node.loc), index_var,
            node.loc))
    return index_var


import copy
ir.Const.__deepcopy__ = lambda self, memo: ir.Const(self.value, copy.
    deepcopy(self.loc))


def is_call_assign(stmt):
    return isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
        ) and stmt.value.op == 'call'


def is_call(expr):
    return isinstance(expr, ir.Expr) and expr.op == 'call'


def is_var_assign(inst):
    return isinstance(inst, ir.Assign) and isinstance(inst.value, ir.Var)


def is_assign(inst):
    return isinstance(inst, ir.Assign)


def is_expr(val, op):
    return isinstance(val, ir.Expr) and val.op == op


def sanitize_varname(varname):
    if isinstance(varname, (tuple, list)):
        varname = '_'.join(sanitize_varname(v) for v in varname)
    varname = str(varname)
    xze__btyfu = re.sub('\\W+', '_', varname)
    if not xze__btyfu or not xze__btyfu[0].isalpha():
        xze__btyfu = '_' + xze__btyfu
    if not xze__btyfu.isidentifier() or keyword.iskeyword(xze__btyfu):
        xze__btyfu = mk_unique_var('new_name').replace('.', '_')
    return xze__btyfu


def dump_node_list(node_list):
    for n in node_list:
        print('   ', n)


def debug_prints():
    return numba.core.config.DEBUG_ARRAY_OPT == 1


@overload(reversed)
def list_reverse(A):
    if isinstance(A, types.List):

        def impl_reversed(A):
            xmo__yfcfy = len(A)
            for ytc__rmuf in range(xmo__yfcfy):
                yield A[xmo__yfcfy - 1 - ytc__rmuf]
        return impl_reversed


@numba.njit
def count_nonnan(a):
    return np.count_nonzero(~np.isnan(a))


@numba.njit
def nanvar_ddof1(a):
    wziuw__yqmn = count_nonnan(a)
    if wziuw__yqmn <= 1:
        return np.nan
    return np.nanvar(a) * (wziuw__yqmn / (wziuw__yqmn - 1))


@numba.njit
def nanstd_ddof1(a):
    return np.sqrt(nanvar_ddof1(a))


def has_supported_h5py():
    try:
        import h5py
        from bodo.io import _hdf5
    except ImportError as ngh__uxe:
        kzpb__wcz = False
    else:
        kzpb__wcz = h5py.version.hdf5_version_tuple[1] in (10, 12)
    return kzpb__wcz


def check_h5py():
    if not has_supported_h5py():
        raise BodoError("install 'h5py' package to enable hdf5 support")


def has_pyarrow():
    try:
        import pyarrow
    except ImportError as ngh__uxe:
        lnile__onlz = False
    else:
        lnile__onlz = True
    return lnile__onlz


def has_scipy():
    try:
        import scipy
    except ImportError as ngh__uxe:
        dder__jstt = False
    else:
        dder__jstt = True
    return dder__jstt


@intrinsic
def check_and_propagate_cpp_exception(typingctx):

    def codegen(context, builder, sig, args):
        askl__mnjsw = context.get_python_api(builder)
        czc__bvgo = askl__mnjsw.err_occurred()
        tja__sxhn = cgutils.is_not_null(builder, czc__bvgo)
        with builder.if_then(tja__sxhn):
            builder.ret(numba.core.callconv.RETCODE_EXC)
    return types.void(), codegen


def inlined_check_and_propagate_cpp_exception(context, builder):
    askl__mnjsw = context.get_python_api(builder)
    czc__bvgo = askl__mnjsw.err_occurred()
    tja__sxhn = cgutils.is_not_null(builder, czc__bvgo)
    with builder.if_then(tja__sxhn):
        builder.ret(numba.core.callconv.RETCODE_EXC)


@numba.njit
def check_java_installation(fname):
    with numba.objmode():
        check_java_installation_(fname)


def check_java_installation_(fname):
    if not fname.startswith('hdfs://'):
        return
    import shutil
    if not shutil.which('java'):
        sth__del = (
            "Java not found. Make sure openjdk is installed for hdfs. openjdk can be installed by calling 'conda install 'openjdk>=9.0,<12' -c conda-forge'."
            )
        raise BodoError(sth__del)


dt_err = """
        If you are trying to set NULL values for timedelta64 in regular Python, 

        consider using np.timedelta64('nat') instead of None
        """


@lower_constant(types.List)
def lower_constant_list(context, builder, typ, pyval):
    if len(pyval) > CONST_LIST_SLOW_WARN_THRESHOLD:
        warnings.warn(BodoWarning(
            'Using large global lists can result in long compilation times. Please pass large lists as arguments to JIT functions or use arrays.'
            ))
    bpsfa__psyhu = []
    for a in pyval:
        if bodo.typeof(a) != typ.dtype:
            raise BodoError(
                f'Values in list must have the same data type for type stability. Expected: {typ.dtype}, Actual: {bodo.typeof(a)}'
                )
        bpsfa__psyhu.append(context.get_constant_generic(builder, typ.dtype, a)
            )
    ibkw__dmm = context.get_constant_generic(builder, types.int64, len(pyval))
    vvba__gmw = context.get_constant_generic(builder, types.bool_, False)
    ics__ujztk = context.get_constant_null(types.pyobject)
    cdq__jbuty = lir.Constant.literal_struct([ibkw__dmm, ibkw__dmm,
        vvba__gmw] + bpsfa__psyhu)
    cdq__jbuty = cgutils.global_constant(builder, '.const.payload', cdq__jbuty
        ).bitcast(cgutils.voidptr_t)
    jwa__hyl = context.get_constant(types.int64, -1)
    bqvdk__ajc = context.get_constant_null(types.voidptr)
    ggcyl__irjjx = lir.Constant.literal_struct([jwa__hyl, bqvdk__ajc,
        bqvdk__ajc, cdq__jbuty, jwa__hyl])
    ggcyl__irjjx = cgutils.global_constant(builder, '.const.meminfo',
        ggcyl__irjjx).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([ggcyl__irjjx, ics__ujztk])


@lower_constant(types.Set)
def lower_constant_set(context, builder, typ, pyval):
    for a in pyval:
        if bodo.typeof(a) != typ.dtype:
            raise BodoError(
                f'Values in set must have the same data type for type stability. Expected: {typ.dtype}, Actual: {bodo.typeof(a)}'
                )
    idtfh__osv = types.List(typ.dtype)
    plqbk__yazqu = context.get_constant_generic(builder, idtfh__osv, list(
        pyval))
    smxh__jeucs = context.compile_internal(builder, lambda l: set(l), types
        .Set(typ.dtype)(idtfh__osv), [plqbk__yazqu])
    return smxh__jeucs


def lower_const_dict_fast_path(context, builder, typ, pyval):
    from bodo.utils.typing import can_replace
    has__wrarn = pd.Series(pyval.keys()).values
    scedz__wciv = pd.Series(pyval.values()).values
    lov__szttd = bodo.typeof(has__wrarn)
    nzkkr__osk = bodo.typeof(scedz__wciv)
    require(lov__szttd.dtype == typ.key_type or can_replace(typ.key_type,
        lov__szttd.dtype))
    require(nzkkr__osk.dtype == typ.value_type or can_replace(typ.
        value_type, nzkkr__osk.dtype))
    fvats__xohgs = context.get_constant_generic(builder, lov__szttd, has__wrarn
        )
    yao__yxo = context.get_constant_generic(builder, nzkkr__osk, scedz__wciv)

    def create_dict(keys, vals):
        dij__gfez = {}
        for k, v in zip(keys, vals):
            dij__gfez[k] = v
        return dij__gfez
    iqs__arvcy = context.compile_internal(builder, create_dict, typ(
        lov__szttd, nzkkr__osk), [fvats__xohgs, yao__yxo])
    return iqs__arvcy


@lower_constant(types.DictType)
def lower_constant_dict(context, builder, typ, pyval):
    try:
        return lower_const_dict_fast_path(context, builder, typ, pyval)
    except:
        pass
    if len(pyval) > CONST_DICT_SLOW_WARN_THRESHOLD:
        warnings.warn(BodoWarning(
            'Using large global dictionaries can result in long compilation times. Please pass large dictionaries as arguments to JIT functions.'
            ))
    ovx__tuym = typ.key_type
    yrnqt__pwnyc = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(ovx__tuym, yrnqt__pwnyc)
    iqs__arvcy = context.compile_internal(builder, make_dict, typ(), [])

    def set_dict_val(d, k, v):
        d[k] = v
    for k, v in pyval.items():
        yjb__nom = context.get_constant_generic(builder, ovx__tuym, k)
        xylao__ogozg = context.get_constant_generic(builder, yrnqt__pwnyc, v)
        context.compile_internal(builder, set_dict_val, types.none(typ,
            ovx__tuym, yrnqt__pwnyc), [iqs__arvcy, yjb__nom, xylao__ogozg])
    return iqs__arvcy


def synchronize_error(exception_str, error_message):
    if exception_str == 'ValueError':
        fjcx__kkv = ValueError
    else:
        fjcx__kkv = RuntimeError
    rooc__yzx = MPI.COMM_WORLD
    if rooc__yzx.allreduce(error_message != '', op=MPI.LOR):
        for error_message in rooc__yzx.allgather(error_message):
            if error_message:
                raise fjcx__kkv(error_message)


@numba.njit
def synchronize_error_njit(exception_str, error_message):
    with numba.objmode():
        synchronize_error(exception_str, error_message)
