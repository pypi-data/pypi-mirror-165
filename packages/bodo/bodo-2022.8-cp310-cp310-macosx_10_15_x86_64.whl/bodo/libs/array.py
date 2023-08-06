"""Tools for handling bodo arrays, e.g. passing to C/C++ code
"""
from collections import defaultdict
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.typing.templates import signature
from numba.cpython.listobj import ListInstance
from numba.extending import intrinsic, models, register_model
from numba.np.arrayobj import _getitem_array_single_int
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, get_categories_int_type
from bodo.hiframes.time_ext import TimeArrayType, TimeType
from bodo.libs import array_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayPayloadType, ArrayItemArrayType, _get_array_item_arr_payload, define_array_item_dtor, offset_type
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType, int128_type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType, _get_map_arr_data_type, init_map_arr_codegen
from bodo.libs.str_arr_ext import _get_str_binary_arr_payload, char_arr_type, null_bitmap_arr_type, offset_arr_type, string_array_type
from bodo.libs.struct_arr_ext import StructArrayPayloadType, StructArrayType, StructType, _get_struct_arr_payload, define_struct_arr_dtor
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoError, MetaType, decode_if_dict_array, get_overload_const_int, is_overload_none, is_str_arr_type, raise_bodo_error, type_has_unknown_cats, unwrap_typeref
from bodo.utils.utils import CTypeEnum, check_and_propagate_cpp_exception, numba_to_c_type
ll.add_symbol('list_string_array_to_info', array_ext.list_string_array_to_info)
ll.add_symbol('nested_array_to_info', array_ext.nested_array_to_info)
ll.add_symbol('string_array_to_info', array_ext.string_array_to_info)
ll.add_symbol('dict_str_array_to_info', array_ext.dict_str_array_to_info)
ll.add_symbol('get_nested_info', array_ext.get_nested_info)
ll.add_symbol('get_has_global_dictionary', array_ext.get_has_global_dictionary)
ll.add_symbol('numpy_array_to_info', array_ext.numpy_array_to_info)
ll.add_symbol('categorical_array_to_info', array_ext.categorical_array_to_info)
ll.add_symbol('nullable_array_to_info', array_ext.nullable_array_to_info)
ll.add_symbol('interval_array_to_info', array_ext.interval_array_to_info)
ll.add_symbol('decimal_array_to_info', array_ext.decimal_array_to_info)
ll.add_symbol('time_array_to_info', array_ext.time_array_to_info)
ll.add_symbol('info_to_nested_array', array_ext.info_to_nested_array)
ll.add_symbol('info_to_list_string_array', array_ext.info_to_list_string_array)
ll.add_symbol('info_to_string_array', array_ext.info_to_string_array)
ll.add_symbol('info_to_numpy_array', array_ext.info_to_numpy_array)
ll.add_symbol('info_to_nullable_array', array_ext.info_to_nullable_array)
ll.add_symbol('info_to_interval_array', array_ext.info_to_interval_array)
ll.add_symbol('alloc_numpy', array_ext.alloc_numpy)
ll.add_symbol('alloc_string_array', array_ext.alloc_string_array)
ll.add_symbol('arr_info_list_to_table', array_ext.arr_info_list_to_table)
ll.add_symbol('info_from_table', array_ext.info_from_table)
ll.add_symbol('delete_info_decref_array', array_ext.delete_info_decref_array)
ll.add_symbol('delete_table_decref_arrays', array_ext.
    delete_table_decref_arrays)
ll.add_symbol('decref_table_array', array_ext.decref_table_array)
ll.add_symbol('delete_table', array_ext.delete_table)
ll.add_symbol('shuffle_table', array_ext.shuffle_table)
ll.add_symbol('get_shuffle_info', array_ext.get_shuffle_info)
ll.add_symbol('delete_shuffle_info', array_ext.delete_shuffle_info)
ll.add_symbol('reverse_shuffle_table', array_ext.reverse_shuffle_table)
ll.add_symbol('hash_join_table', array_ext.hash_join_table)
ll.add_symbol('drop_duplicates_table', array_ext.drop_duplicates_table)
ll.add_symbol('sort_values_table', array_ext.sort_values_table)
ll.add_symbol('sample_table', array_ext.sample_table)
ll.add_symbol('shuffle_renormalization', array_ext.shuffle_renormalization)
ll.add_symbol('shuffle_renormalization_group', array_ext.
    shuffle_renormalization_group)
ll.add_symbol('groupby_and_aggregate', array_ext.groupby_and_aggregate)
ll.add_symbol('convert_local_dictionary_to_global', array_ext.
    convert_local_dictionary_to_global)
ll.add_symbol('get_groupby_labels', array_ext.get_groupby_labels)
ll.add_symbol('array_isin', array_ext.array_isin)
ll.add_symbol('get_search_regex', array_ext.get_search_regex)
ll.add_symbol('array_info_getitem', array_ext.array_info_getitem)
ll.add_symbol('array_info_getdata1', array_ext.array_info_getdata1)


class ArrayInfoType(types.Type):

    def __init__(self):
        super(ArrayInfoType, self).__init__(name='ArrayInfoType()')


array_info_type = ArrayInfoType()
register_model(ArrayInfoType)(models.OpaqueModel)


class TableTypeCPP(types.Type):

    def __init__(self):
        super(TableTypeCPP, self).__init__(name='TableTypeCPP()')


table_type = TableTypeCPP()
register_model(TableTypeCPP)(models.OpaqueModel)


@intrinsic
def array_to_info(typingctx, arr_type_t=None):
    return array_info_type(arr_type_t), array_to_info_codegen


def array_to_info_codegen(context, builder, sig, args, incref=True):
    in_arr, = args
    arr_type = sig.args[0]
    if incref:
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, TupleArrayType):
        tsqvx__wbpq = context.make_helper(builder, arr_type, in_arr)
        in_arr = tsqvx__wbpq.data
        arr_type = StructArrayType(arr_type.data, ('dummy',) * len(arr_type
            .data))
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        baqz__kio = context.make_helper(builder, arr_type, in_arr)
        ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='list_string_array_to_info')
        return builder.call(hgavb__vlh, [baqz__kio.meminfo])
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType, StructArrayType)
        ):

        def get_types(arr_typ):
            if isinstance(arr_typ, MapArrayType):
                return get_types(_get_map_arr_data_type(arr_typ))
            elif isinstance(arr_typ, ArrayItemArrayType):
                return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
            elif isinstance(arr_typ, (StructType, StructArrayType)):
                iiq__zaj = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                for liu__zyrh in arr_typ.data:
                    iiq__zaj += get_types(liu__zyrh)
                return iiq__zaj
            elif isinstance(arr_typ, (types.Array, IntegerArrayType)
                ) or arr_typ == boolean_array:
                return get_types(arr_typ.dtype)
            elif arr_typ == string_array_type:
                return [CTypeEnum.STRING.value]
            elif arr_typ == binary_array_type:
                return [CTypeEnum.BINARY.value]
            elif isinstance(arr_typ, DecimalArrayType):
                return [CTypeEnum.Decimal.value, arr_typ.precision, arr_typ
                    .scale]
            else:
                return [numba_to_c_type(arr_typ)]

        def get_lengths(arr_typ, arr):
            bednd__ubxl = context.compile_internal(builder, lambda a: len(a
                ), types.intp(arr_typ), [arr])
            if isinstance(arr_typ, MapArrayType):
                fjp__bvvm = context.make_helper(builder, arr_typ, value=arr)
                ypvbt__qms = get_lengths(_get_map_arr_data_type(arr_typ),
                    fjp__bvvm.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                cqu__ozaa = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                ypvbt__qms = get_lengths(arr_typ.dtype, cqu__ozaa.data)
                ypvbt__qms = cgutils.pack_array(builder, [cqu__ozaa.
                    n_arrays] + [builder.extract_value(ypvbt__qms,
                    egd__vfjr) for egd__vfjr in range(ypvbt__qms.type.count)])
            elif isinstance(arr_typ, StructArrayType):
                cqu__ozaa = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                ypvbt__qms = []
                for egd__vfjr, liu__zyrh in enumerate(arr_typ.data):
                    tfaz__azpm = get_lengths(liu__zyrh, builder.
                        extract_value(cqu__ozaa.data, egd__vfjr))
                    ypvbt__qms += [builder.extract_value(tfaz__azpm,
                        cmo__kdmlg) for cmo__kdmlg in range(tfaz__azpm.type
                        .count)]
                ypvbt__qms = cgutils.pack_array(builder, [bednd__ubxl,
                    context.get_constant(types.int64, -1)] + ypvbt__qms)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType,
                types.Array)) or arr_typ in (boolean_array,
                datetime_date_array_type, string_array_type, binary_array_type
                ):
                ypvbt__qms = cgutils.pack_array(builder, [bednd__ubxl])
            else:
                raise BodoError(
                    f'array_to_info: unsupported type for subarray {arr_typ}')
            return ypvbt__qms

        def get_buffers(arr_typ, arr):
            if isinstance(arr_typ, MapArrayType):
                fjp__bvvm = context.make_helper(builder, arr_typ, value=arr)
                sns__rskg = get_buffers(_get_map_arr_data_type(arr_typ),
                    fjp__bvvm.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                cqu__ozaa = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                ssdl__glc = get_buffers(arr_typ.dtype, cqu__ozaa.data)
                zdii__rjia = context.make_array(types.Array(offset_type, 1,
                    'C'))(context, builder, cqu__ozaa.offsets)
                rnq__vhl = builder.bitcast(zdii__rjia.data, lir.IntType(8).
                    as_pointer())
                jfiew__jbc = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, cqu__ozaa.null_bitmap)
                abt__jmj = builder.bitcast(jfiew__jbc.data, lir.IntType(8).
                    as_pointer())
                sns__rskg = cgutils.pack_array(builder, [rnq__vhl, abt__jmj
                    ] + [builder.extract_value(ssdl__glc, egd__vfjr) for
                    egd__vfjr in range(ssdl__glc.type.count)])
            elif isinstance(arr_typ, StructArrayType):
                cqu__ozaa = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                ssdl__glc = []
                for egd__vfjr, liu__zyrh in enumerate(arr_typ.data):
                    qex__vtkq = get_buffers(liu__zyrh, builder.
                        extract_value(cqu__ozaa.data, egd__vfjr))
                    ssdl__glc += [builder.extract_value(qex__vtkq,
                        cmo__kdmlg) for cmo__kdmlg in range(qex__vtkq.type.
                        count)]
                jfiew__jbc = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, cqu__ozaa.null_bitmap)
                abt__jmj = builder.bitcast(jfiew__jbc.data, lir.IntType(8).
                    as_pointer())
                sns__rskg = cgutils.pack_array(builder, [abt__jmj] + ssdl__glc)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
                ) or arr_typ in (boolean_array, datetime_date_array_type):
                dkm__fuf = arr_typ.dtype
                if isinstance(arr_typ, DecimalArrayType):
                    dkm__fuf = int128_type
                elif arr_typ == datetime_date_array_type:
                    dkm__fuf = types.int64
                arr = cgutils.create_struct_proxy(arr_typ)(context, builder,
                    arr)
                zqxx__itc = context.make_array(types.Array(dkm__fuf, 1, 'C'))(
                    context, builder, arr.data)
                jfiew__jbc = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, arr.null_bitmap)
                amr__evv = builder.bitcast(zqxx__itc.data, lir.IntType(8).
                    as_pointer())
                abt__jmj = builder.bitcast(jfiew__jbc.data, lir.IntType(8).
                    as_pointer())
                sns__rskg = cgutils.pack_array(builder, [abt__jmj, amr__evv])
            elif arr_typ in (string_array_type, binary_array_type):
                cqu__ozaa = _get_str_binary_arr_payload(context, builder,
                    arr, arr_typ)
                uttv__pli = context.make_helper(builder, offset_arr_type,
                    cqu__ozaa.offsets).data
                uvqy__lahz = context.make_helper(builder, char_arr_type,
                    cqu__ozaa.data).data
                tvwnd__con = context.make_helper(builder,
                    null_bitmap_arr_type, cqu__ozaa.null_bitmap).data
                sns__rskg = cgutils.pack_array(builder, [builder.bitcast(
                    uttv__pli, lir.IntType(8).as_pointer()), builder.
                    bitcast(tvwnd__con, lir.IntType(8).as_pointer()),
                    builder.bitcast(uvqy__lahz, lir.IntType(8).as_pointer())])
            elif isinstance(arr_typ, types.Array):
                arr = context.make_array(arr_typ)(context, builder, arr)
                amr__evv = builder.bitcast(arr.data, lir.IntType(8).
                    as_pointer())
                reh__lmgp = lir.Constant(lir.IntType(8).as_pointer(), None)
                sns__rskg = cgutils.pack_array(builder, [reh__lmgp, amr__evv])
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray ' + str(
                    arr_typ))
            return sns__rskg

        def get_field_names(arr_typ):
            opjp__vonh = []
            if isinstance(arr_typ, StructArrayType):
                for fxknm__hfdx, nde__wmi in zip(arr_typ.dtype.names,
                    arr_typ.data):
                    opjp__vonh.append(fxknm__hfdx)
                    opjp__vonh += get_field_names(nde__wmi)
            elif isinstance(arr_typ, ArrayItemArrayType):
                opjp__vonh += get_field_names(arr_typ.dtype)
            elif isinstance(arr_typ, MapArrayType):
                opjp__vonh += get_field_names(_get_map_arr_data_type(arr_typ))
            return opjp__vonh
        iiq__zaj = get_types(arr_type)
        yhd__rsh = cgutils.pack_array(builder, [context.get_constant(types.
            int32, t) for t in iiq__zaj])
        mhv__jccsf = cgutils.alloca_once_value(builder, yhd__rsh)
        ypvbt__qms = get_lengths(arr_type, in_arr)
        lengths_ptr = cgutils.alloca_once_value(builder, ypvbt__qms)
        sns__rskg = get_buffers(arr_type, in_arr)
        hjhbg__hfxpf = cgutils.alloca_once_value(builder, sns__rskg)
        opjp__vonh = get_field_names(arr_type)
        if len(opjp__vonh) == 0:
            opjp__vonh = ['irrelevant']
        vzmvg__llwif = cgutils.pack_array(builder, [context.
            insert_const_string(builder.module, a) for a in opjp__vonh])
        ubvxa__zsiwf = cgutils.alloca_once_value(builder, vzmvg__llwif)
        if isinstance(arr_type, MapArrayType):
            wou__phh = _get_map_arr_data_type(arr_type)
            agvg__awou = context.make_helper(builder, arr_type, value=in_arr)
            aem__xlsfz = agvg__awou.data
        else:
            wou__phh = arr_type
            aem__xlsfz = in_arr
        lvzz__dtym = context.make_helper(builder, wou__phh, aem__xlsfz)
        ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(32).as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='nested_array_to_info')
        txiwx__ith = builder.call(hgavb__vlh, [builder.bitcast(mhv__jccsf,
            lir.IntType(32).as_pointer()), builder.bitcast(hjhbg__hfxpf,
            lir.IntType(8).as_pointer().as_pointer()), builder.bitcast(
            lengths_ptr, lir.IntType(64).as_pointer()), builder.bitcast(
            ubvxa__zsiwf, lir.IntType(8).as_pointer()), lvzz__dtym.meminfo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return txiwx__ith
    if arr_type in (string_array_type, binary_array_type):
        nubqr__uhxk = context.make_helper(builder, arr_type, in_arr)
        vmxqb__vkh = ArrayItemArrayType(char_arr_type)
        baqz__kio = context.make_helper(builder, vmxqb__vkh, nubqr__uhxk.data)
        cqu__ozaa = _get_str_binary_arr_payload(context, builder, in_arr,
            arr_type)
        uttv__pli = context.make_helper(builder, offset_arr_type, cqu__ozaa
            .offsets).data
        uvqy__lahz = context.make_helper(builder, char_arr_type, cqu__ozaa.data
            ).data
        tvwnd__con = context.make_helper(builder, null_bitmap_arr_type,
            cqu__ozaa.null_bitmap).data
        nyv__tgnou = builder.zext(builder.load(builder.gep(uttv__pli, [
            cqu__ozaa.n_arrays])), lir.IntType(64))
        vhjo__coz = context.get_constant(types.int32, int(arr_type ==
            binary_array_type))
        ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='string_array_to_info')
        return builder.call(hgavb__vlh, [cqu__ozaa.n_arrays, nyv__tgnou,
            uvqy__lahz, uttv__pli, tvwnd__con, baqz__kio.meminfo, vhjo__coz])
    if arr_type == bodo.dict_str_arr_type:
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        szafw__cwl = arr.data
        jda__ecqtr = arr.indices
        sig = array_info_type(arr_type.data)
        wsmmj__uhy = array_to_info_codegen(context, builder, sig, (
            szafw__cwl,), False)
        sig = array_info_type(bodo.libs.dict_arr_ext.dict_indices_arr_type)
        tuktp__yrhs = array_to_info_codegen(context, builder, sig, (
            jda__ecqtr,), False)
        ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(32)])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='dict_str_array_to_info')
        zddu__jfxu = builder.zext(arr.has_global_dictionary, lir.IntType(32))
        return builder.call(hgavb__vlh, [wsmmj__uhy, tuktp__yrhs, zddu__jfxu])
    jhpbe__fwlf = False
    if isinstance(arr_type, CategoricalArrayType):
        context.nrt.decref(builder, arr_type, in_arr)
        gofvk__glj = context.compile_internal(builder, lambda a: len(a.
            dtype.categories), types.intp(arr_type), [in_arr])
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).codes
        bir__enu = get_categories_int_type(arr_type.dtype)
        arr_type = types.Array(bir__enu, 1, 'C')
        jhpbe__fwlf = True
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, bodo.DatetimeArrayType):
        if jhpbe__fwlf:
            raise BodoError(
                'array_to_info(): Categorical PandasDatetimeArrayType not supported'
                )
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).data
        arr_type = arr_type.data_array_type
    if isinstance(arr_type, types.Array):
        arr = context.make_array(arr_type)(context, builder, in_arr)
        assert arr_type.ndim == 1, 'only 1D array shuffle supported'
        bednd__ubxl = builder.extract_value(arr.shape, 0)
        mdmw__imx = arr_type.dtype
        wiee__pjev = numba_to_c_type(mdmw__imx)
        ielw__rlk = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), wiee__pjev))
        if jhpbe__fwlf:
            ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(64), lir.IntType(8).as_pointer()])
            hgavb__vlh = cgutils.get_or_insert_function(builder.module,
                ymrbe__mwwp, name='categorical_array_to_info')
            return builder.call(hgavb__vlh, [bednd__ubxl, builder.bitcast(
                arr.data, lir.IntType(8).as_pointer()), builder.load(
                ielw__rlk), gofvk__glj, arr.meminfo])
        else:
            ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer()])
            hgavb__vlh = cgutils.get_or_insert_function(builder.module,
                ymrbe__mwwp, name='numpy_array_to_info')
            return builder.call(hgavb__vlh, [bednd__ubxl, builder.bitcast(
                arr.data, lir.IntType(8).as_pointer()), builder.load(
                ielw__rlk), arr.meminfo])
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType, TimeArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        mdmw__imx = arr_type.dtype
        dkm__fuf = mdmw__imx
        if isinstance(arr_type, DecimalArrayType):
            dkm__fuf = int128_type
        if arr_type == datetime_date_array_type:
            dkm__fuf = types.int64
        zqxx__itc = context.make_array(types.Array(dkm__fuf, 1, 'C'))(context,
            builder, arr.data)
        bednd__ubxl = builder.extract_value(zqxx__itc.shape, 0)
        mmzr__ukok = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, arr.null_bitmap)
        wiee__pjev = numba_to_c_type(mdmw__imx)
        ielw__rlk = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), wiee__pjev))
        if isinstance(arr_type, DecimalArrayType):
            ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer(), lir.IntType(32), lir.
                IntType(32)])
            hgavb__vlh = cgutils.get_or_insert_function(builder.module,
                ymrbe__mwwp, name='decimal_array_to_info')
            return builder.call(hgavb__vlh, [bednd__ubxl, builder.bitcast(
                zqxx__itc.data, lir.IntType(8).as_pointer()), builder.load(
                ielw__rlk), builder.bitcast(mmzr__ukok.data, lir.IntType(8)
                .as_pointer()), zqxx__itc.meminfo, mmzr__ukok.meminfo,
                context.get_constant(types.int32, arr_type.precision),
                context.get_constant(types.int32, arr_type.scale)])
        elif isinstance(arr_type, TimeArrayType):
            ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer(), lir.IntType(32)])
            hgavb__vlh = cgutils.get_or_insert_function(builder.module,
                ymrbe__mwwp, name='time_array_to_info')
            return builder.call(hgavb__vlh, [bednd__ubxl, builder.bitcast(
                zqxx__itc.data, lir.IntType(8).as_pointer()), builder.load(
                ielw__rlk), builder.bitcast(mmzr__ukok.data, lir.IntType(8)
                .as_pointer()), zqxx__itc.meminfo, mmzr__ukok.meminfo, lir.
                Constant(lir.IntType(32), arr_type.precision)])
        else:
            ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer()])
            hgavb__vlh = cgutils.get_or_insert_function(builder.module,
                ymrbe__mwwp, name='nullable_array_to_info')
            return builder.call(hgavb__vlh, [bednd__ubxl, builder.bitcast(
                zqxx__itc.data, lir.IntType(8).as_pointer()), builder.load(
                ielw__rlk), builder.bitcast(mmzr__ukok.data, lir.IntType(8)
                .as_pointer()), zqxx__itc.meminfo, mmzr__ukok.meminfo])
    if isinstance(arr_type, IntervalArrayType):
        assert isinstance(arr_type.arr_type, types.Array
            ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        aplnz__hlgx = context.make_array(arr_type.arr_type)(context,
            builder, arr.left)
        vtqvc__cgmn = context.make_array(arr_type.arr_type)(context,
            builder, arr.right)
        bednd__ubxl = builder.extract_value(aplnz__hlgx.shape, 0)
        wiee__pjev = numba_to_c_type(arr_type.arr_type.dtype)
        ielw__rlk = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), wiee__pjev))
        ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='interval_array_to_info')
        return builder.call(hgavb__vlh, [bednd__ubxl, builder.bitcast(
            aplnz__hlgx.data, lir.IntType(8).as_pointer()), builder.bitcast
            (vtqvc__cgmn.data, lir.IntType(8).as_pointer()), builder.load(
            ielw__rlk), aplnz__hlgx.meminfo, vtqvc__cgmn.meminfo])
    raise_bodo_error(f'array_to_info(): array type {arr_type} is not supported'
        )


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    fqq__rwzbl = cgutils.alloca_once(builder, lir.IntType(64))
    amr__evv = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    qdo__cetu = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    ymrbe__mwwp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    hgavb__vlh = cgutils.get_or_insert_function(builder.module, ymrbe__mwwp,
        name='info_to_numpy_array')
    builder.call(hgavb__vlh, [in_info, fqq__rwzbl, amr__evv, qdo__cetu])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    kkfdp__akev = context.get_value_type(types.intp)
    hgml__ayw = cgutils.pack_array(builder, [builder.load(fqq__rwzbl)], ty=
        kkfdp__akev)
    offc__qlgkr = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    iwsat__pbuwa = cgutils.pack_array(builder, [offc__qlgkr], ty=kkfdp__akev)
    uvqy__lahz = builder.bitcast(builder.load(amr__evv), context.
        get_data_type(arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=uvqy__lahz, shape=hgml__ayw,
        strides=iwsat__pbuwa, itemsize=offc__qlgkr, meminfo=builder.load(
        qdo__cetu))
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    zow__uesr = context.make_helper(builder, arr_type)
    ymrbe__mwwp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    hgavb__vlh = cgutils.get_or_insert_function(builder.module, ymrbe__mwwp,
        name='info_to_list_string_array')
    builder.call(hgavb__vlh, [in_info, zow__uesr._get_ptr_by_name('meminfo')])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return zow__uesr._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    ocr__ujqs = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        kjsp__gvtq = lengths_pos
        fwwox__mnjsr = infos_pos
        tzh__qpkk, lengths_pos, infos_pos = nested_to_array(context,
            builder, arr_typ.dtype, lengths_ptr, array_infos_ptr, 
            lengths_pos + 1, infos_pos + 2)
        njrf__nmw = ArrayItemArrayPayloadType(arr_typ)
        lwh__yyma = context.get_data_type(njrf__nmw)
        tulfs__figp = context.get_abi_sizeof(lwh__yyma)
        swsj__xgx = define_array_item_dtor(context, builder, arr_typ, njrf__nmw
            )
        hhz__uyx = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, tulfs__figp), swsj__xgx)
        cqzsn__hhdnh = context.nrt.meminfo_data(builder, hhz__uyx)
        wrupl__bmbj = builder.bitcast(cqzsn__hhdnh, lwh__yyma.as_pointer())
        cqu__ozaa = cgutils.create_struct_proxy(njrf__nmw)(context, builder)
        cqu__ozaa.n_arrays = builder.extract_value(builder.load(lengths_ptr
            ), kjsp__gvtq)
        cqu__ozaa.data = tzh__qpkk
        cqk__ppt = builder.load(array_infos_ptr)
        ntl__bjloa = builder.bitcast(builder.extract_value(cqk__ppt,
            fwwox__mnjsr), ocr__ujqs)
        cqu__ozaa.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, ntl__bjloa)
        ybkgm__knhww = builder.bitcast(builder.extract_value(cqk__ppt, 
            fwwox__mnjsr + 1), ocr__ujqs)
        cqu__ozaa.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, ybkgm__knhww)
        builder.store(cqu__ozaa._getvalue(), wrupl__bmbj)
        baqz__kio = context.make_helper(builder, arr_typ)
        baqz__kio.meminfo = hhz__uyx
        return baqz__kio._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        mojce__hgxp = []
        fwwox__mnjsr = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for mbm__vjgs in arr_typ.data:
            tzh__qpkk, lengths_pos, infos_pos = nested_to_array(context,
                builder, mbm__vjgs, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            mojce__hgxp.append(tzh__qpkk)
        njrf__nmw = StructArrayPayloadType(arr_typ.data)
        lwh__yyma = context.get_value_type(njrf__nmw)
        tulfs__figp = context.get_abi_sizeof(lwh__yyma)
        swsj__xgx = define_struct_arr_dtor(context, builder, arr_typ, njrf__nmw
            )
        hhz__uyx = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, tulfs__figp), swsj__xgx)
        cqzsn__hhdnh = context.nrt.meminfo_data(builder, hhz__uyx)
        wrupl__bmbj = builder.bitcast(cqzsn__hhdnh, lwh__yyma.as_pointer())
        cqu__ozaa = cgutils.create_struct_proxy(njrf__nmw)(context, builder)
        cqu__ozaa.data = cgutils.pack_array(builder, mojce__hgxp
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, mojce__hgxp)
        cqk__ppt = builder.load(array_infos_ptr)
        ybkgm__knhww = builder.bitcast(builder.extract_value(cqk__ppt,
            fwwox__mnjsr), ocr__ujqs)
        cqu__ozaa.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, ybkgm__knhww)
        builder.store(cqu__ozaa._getvalue(), wrupl__bmbj)
        nbcn__xtr = context.make_helper(builder, arr_typ)
        nbcn__xtr.meminfo = hhz__uyx
        return nbcn__xtr._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        cqk__ppt = builder.load(array_infos_ptr)
        xar__qcj = builder.bitcast(builder.extract_value(cqk__ppt,
            infos_pos), ocr__ujqs)
        nubqr__uhxk = context.make_helper(builder, arr_typ)
        vmxqb__vkh = ArrayItemArrayType(char_arr_type)
        baqz__kio = context.make_helper(builder, vmxqb__vkh)
        ymrbe__mwwp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='info_to_string_array')
        builder.call(hgavb__vlh, [xar__qcj, baqz__kio._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        nubqr__uhxk.data = baqz__kio._getvalue()
        return nubqr__uhxk._getvalue(), lengths_pos + 1, infos_pos + 1
    elif isinstance(arr_typ, types.Array):
        cqk__ppt = builder.load(array_infos_ptr)
        ulsi__snask = builder.bitcast(builder.extract_value(cqk__ppt, 
            infos_pos + 1), ocr__ujqs)
        return _lower_info_to_array_numpy(arr_typ, context, builder,
            ulsi__snask), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
        ) or arr_typ in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        dkm__fuf = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            dkm__fuf = int128_type
        elif arr_typ == datetime_date_array_type:
            dkm__fuf = types.int64
        cqk__ppt = builder.load(array_infos_ptr)
        ybkgm__knhww = builder.bitcast(builder.extract_value(cqk__ppt,
            infos_pos), ocr__ujqs)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, ybkgm__knhww)
        ulsi__snask = builder.bitcast(builder.extract_value(cqk__ppt, 
            infos_pos + 1), ocr__ujqs)
        arr.data = _lower_info_to_array_numpy(types.Array(dkm__fuf, 1, 'C'),
            context, builder, ulsi__snask)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


def info_to_array_codegen(context, builder, sig, args):
    array_type = sig.args[1]
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    in_info, wqpcb__vwsb = args
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        return _lower_info_to_array_list_string_array(arr_type, context,
            builder, in_info)
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType,
        StructArrayType, TupleArrayType)):

        def get_num_arrays(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 1 + get_num_arrays(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_arrays(mbm__vjgs) for mbm__vjgs in
                    arr_typ.data])
            else:
                return 1

        def get_num_infos(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 2 + get_num_infos(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_infos(mbm__vjgs) for mbm__vjgs in
                    arr_typ.data])
            elif arr_typ in (string_array_type, binary_array_type):
                return 1
            else:
                return 2
        if isinstance(arr_type, TupleArrayType):
            bmqhb__docq = StructArrayType(arr_type.data, ('dummy',) * len(
                arr_type.data))
        elif isinstance(arr_type, MapArrayType):
            bmqhb__docq = _get_map_arr_data_type(arr_type)
        else:
            bmqhb__docq = arr_type
        bodwb__cnk = get_num_arrays(bmqhb__docq)
        ypvbt__qms = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), 0) for wqpcb__vwsb in range(bodwb__cnk)])
        lengths_ptr = cgutils.alloca_once_value(builder, ypvbt__qms)
        reh__lmgp = lir.Constant(lir.IntType(8).as_pointer(), None)
        amld__mdx = cgutils.pack_array(builder, [reh__lmgp for wqpcb__vwsb in
            range(get_num_infos(bmqhb__docq))])
        array_infos_ptr = cgutils.alloca_once_value(builder, amld__mdx)
        ymrbe__mwwp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer()])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='info_to_nested_array')
        builder.call(hgavb__vlh, [in_info, builder.bitcast(lengths_ptr, lir
            .IntType(64).as_pointer()), builder.bitcast(array_infos_ptr,
            lir.IntType(8).as_pointer().as_pointer())])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        arr, wqpcb__vwsb, wqpcb__vwsb = nested_to_array(context, builder,
            bmqhb__docq, lengths_ptr, array_infos_ptr, 0, 0)
        if isinstance(arr_type, TupleArrayType):
            tsqvx__wbpq = context.make_helper(builder, arr_type)
            tsqvx__wbpq.data = arr
            context.nrt.incref(builder, bmqhb__docq, arr)
            arr = tsqvx__wbpq._getvalue()
        elif isinstance(arr_type, MapArrayType):
            sig = signature(arr_type, bmqhb__docq)
            arr = init_map_arr_codegen(context, builder, sig, (arr,))
        return arr
    if arr_type in (string_array_type, binary_array_type):
        nubqr__uhxk = context.make_helper(builder, arr_type)
        vmxqb__vkh = ArrayItemArrayType(char_arr_type)
        baqz__kio = context.make_helper(builder, vmxqb__vkh)
        ymrbe__mwwp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='info_to_string_array')
        builder.call(hgavb__vlh, [in_info, baqz__kio._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        nubqr__uhxk.data = baqz__kio._getvalue()
        return nubqr__uhxk._getvalue()
    if arr_type == bodo.dict_str_arr_type:
        ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='get_nested_info')
        wsmmj__uhy = builder.call(hgavb__vlh, [in_info, lir.Constant(lir.
            IntType(32), 1)])
        tuktp__yrhs = builder.call(hgavb__vlh, [in_info, lir.Constant(lir.
            IntType(32), 2)])
        vyce__ywlq = context.make_helper(builder, arr_type)
        sig = arr_type.data(array_info_type, arr_type.data)
        vyce__ywlq.data = info_to_array_codegen(context, builder, sig, (
            wsmmj__uhy, context.get_constant_null(arr_type.data)))
        hrud__bvrfz = bodo.libs.dict_arr_ext.dict_indices_arr_type
        sig = hrud__bvrfz(array_info_type, hrud__bvrfz)
        vyce__ywlq.indices = info_to_array_codegen(context, builder, sig, (
            tuktp__yrhs, context.get_constant_null(hrud__bvrfz)))
        ymrbe__mwwp = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer()])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='get_has_global_dictionary')
        zddu__jfxu = builder.call(hgavb__vlh, [in_info])
        vyce__ywlq.has_global_dictionary = builder.trunc(zddu__jfxu,
            cgutils.bool_t)
        return vyce__ywlq._getvalue()
    if isinstance(arr_type, CategoricalArrayType):
        out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        bir__enu = get_categories_int_type(arr_type.dtype)
        rgjh__nzc = types.Array(bir__enu, 1, 'C')
        out_arr.codes = _lower_info_to_array_numpy(rgjh__nzc, context,
            builder, in_info)
        if isinstance(array_type, types.TypeRef):
            assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
            is_ordered = arr_type.dtype.ordered
            rado__jhn = bodo.utils.utils.create_categorical_type(arr_type.
                dtype.categories, arr_type.dtype.data.data, is_ordered)
            new_cats_tup = MetaType(tuple(rado__jhn))
            int_type = arr_type.dtype.int_type
            lyf__saq = arr_type.dtype.data.data
            tvkr__sfxd = context.get_constant_generic(builder, lyf__saq,
                rado__jhn)
            mdmw__imx = context.compile_internal(builder, lambda c_arr:
                bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo.utils.
                conversion.index_from_array(c_arr), is_ordered, int_type,
                new_cats_tup), arr_type.dtype(lyf__saq), [tvkr__sfxd])
        else:
            mdmw__imx = cgutils.create_struct_proxy(arr_type)(context,
                builder, args[1]).dtype
            context.nrt.incref(builder, arr_type.dtype, mdmw__imx)
        out_arr.dtype = mdmw__imx
        return out_arr._getvalue()
    if isinstance(arr_type, bodo.DatetimeArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        uvqy__lahz = _lower_info_to_array_numpy(arr_type.data_array_type,
            context, builder, in_info)
        arr.data = uvqy__lahz
        return arr._getvalue()
    if isinstance(arr_type, types.Array):
        return _lower_info_to_array_numpy(arr_type, context, builder, in_info)
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType, TimeArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        dkm__fuf = arr_type.dtype
        if isinstance(arr_type, DecimalArrayType):
            dkm__fuf = int128_type
        elif arr_type == datetime_date_array_type:
            dkm__fuf = types.int64
        ucx__fjy = types.Array(dkm__fuf, 1, 'C')
        zqxx__itc = context.make_array(ucx__fjy)(context, builder)
        ofd__txps = types.Array(types.uint8, 1, 'C')
        dgq__twfe = context.make_array(ofd__txps)(context, builder)
        fqq__rwzbl = cgutils.alloca_once(builder, lir.IntType(64))
        zfgy__imusz = cgutils.alloca_once(builder, lir.IntType(64))
        amr__evv = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        flcy__gmy = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        qdo__cetu = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        noi__kbhsn = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        ymrbe__mwwp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer(), lir.IntType(8).as_pointer
            ().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='info_to_nullable_array')
        builder.call(hgavb__vlh, [in_info, fqq__rwzbl, zfgy__imusz,
            amr__evv, flcy__gmy, qdo__cetu, noi__kbhsn])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        kkfdp__akev = context.get_value_type(types.intp)
        hgml__ayw = cgutils.pack_array(builder, [builder.load(fqq__rwzbl)],
            ty=kkfdp__akev)
        offc__qlgkr = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(dkm__fuf)))
        iwsat__pbuwa = cgutils.pack_array(builder, [offc__qlgkr], ty=
            kkfdp__akev)
        uvqy__lahz = builder.bitcast(builder.load(amr__evv), context.
            get_data_type(dkm__fuf).as_pointer())
        numba.np.arrayobj.populate_array(zqxx__itc, data=uvqy__lahz, shape=
            hgml__ayw, strides=iwsat__pbuwa, itemsize=offc__qlgkr, meminfo=
            builder.load(qdo__cetu))
        arr.data = zqxx__itc._getvalue()
        hgml__ayw = cgutils.pack_array(builder, [builder.load(zfgy__imusz)],
            ty=kkfdp__akev)
        offc__qlgkr = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(types.uint8)))
        iwsat__pbuwa = cgutils.pack_array(builder, [offc__qlgkr], ty=
            kkfdp__akev)
        uvqy__lahz = builder.bitcast(builder.load(flcy__gmy), context.
            get_data_type(types.uint8).as_pointer())
        numba.np.arrayobj.populate_array(dgq__twfe, data=uvqy__lahz, shape=
            hgml__ayw, strides=iwsat__pbuwa, itemsize=offc__qlgkr, meminfo=
            builder.load(noi__kbhsn))
        arr.null_bitmap = dgq__twfe._getvalue()
        return arr._getvalue()
    if isinstance(arr_type, IntervalArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        aplnz__hlgx = context.make_array(arr_type.arr_type)(context, builder)
        vtqvc__cgmn = context.make_array(arr_type.arr_type)(context, builder)
        fqq__rwzbl = cgutils.alloca_once(builder, lir.IntType(64))
        ladep__cwsf = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        kyljl__obp = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        umhe__aclos = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        ghk__sfpb = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        ymrbe__mwwp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer()])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='info_to_interval_array')
        builder.call(hgavb__vlh, [in_info, fqq__rwzbl, ladep__cwsf,
            kyljl__obp, umhe__aclos, ghk__sfpb])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        kkfdp__akev = context.get_value_type(types.intp)
        hgml__ayw = cgutils.pack_array(builder, [builder.load(fqq__rwzbl)],
            ty=kkfdp__akev)
        offc__qlgkr = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(arr_type.arr_type.dtype)))
        iwsat__pbuwa = cgutils.pack_array(builder, [offc__qlgkr], ty=
            kkfdp__akev)
        pzcbv__kzld = builder.bitcast(builder.load(ladep__cwsf), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(aplnz__hlgx, data=pzcbv__kzld,
            shape=hgml__ayw, strides=iwsat__pbuwa, itemsize=offc__qlgkr,
            meminfo=builder.load(umhe__aclos))
        arr.left = aplnz__hlgx._getvalue()
        zpnm__erkrq = builder.bitcast(builder.load(kyljl__obp), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(vtqvc__cgmn, data=zpnm__erkrq,
            shape=hgml__ayw, strides=iwsat__pbuwa, itemsize=offc__qlgkr,
            meminfo=builder.load(ghk__sfpb))
        arr.right = vtqvc__cgmn._getvalue()
        return arr._getvalue()
    raise_bodo_error(f'info_to_array(): array type {arr_type} is not supported'
        )


@intrinsic
def info_to_array(typingctx, info_type, array_type):
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    assert info_type == array_info_type, 'info_to_array: expected info type'
    return arr_type(info_type, array_type), info_to_array_codegen


@intrinsic
def test_alloc_np(typingctx, len_typ, arr_type):
    array_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type

    def codegen(context, builder, sig, args):
        bednd__ubxl, wqpcb__vwsb = args
        wiee__pjev = numba_to_c_type(array_type.dtype)
        ielw__rlk = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), wiee__pjev))
        ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='alloc_numpy')
        return builder.call(hgavb__vlh, [bednd__ubxl, builder.load(ielw__rlk)])
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        bednd__ubxl, kxhxx__bdjgo = args
        ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='alloc_string_array')
        return builder.call(hgavb__vlh, [bednd__ubxl, kxhxx__bdjgo])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)
    return table_type(list_arr_info_typ), arr_info_list_to_table_codegen


def arr_info_list_to_table_codegen(context, builder, sig, args):
    giid__pelr, = args
    agl__cutqu = numba.cpython.listobj.ListInstance(context, builder, sig.
        args[0], giid__pelr)
    ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer().as_pointer(), lir.IntType(64)])
    hgavb__vlh = cgutils.get_or_insert_function(builder.module, ymrbe__mwwp,
        name='arr_info_list_to_table')
    return builder.call(hgavb__vlh, [agl__cutqu.data, agl__cutqu.size])


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='info_from_table')
        return builder.call(hgavb__vlh, args)
    return array_info_type(table_t, ind_t), codegen


@intrinsic
def cpp_table_to_py_table(typingctx, cpp_table_t, table_idx_arr_t,
    py_table_type_t):
    assert cpp_table_t == table_type, 'invalid cpp table type'
    assert isinstance(table_idx_arr_t, types.Array
        ) and table_idx_arr_t.dtype == types.int64, 'invalid table index array'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    nvie__johf = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        cpp_table, rzn__klz, wqpcb__vwsb = args
        ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='info_from_table')
        eqn__sxmi = cgutils.create_struct_proxy(nvie__johf)(context, builder)
        eqn__sxmi.parent = cgutils.get_null_value(eqn__sxmi.parent.type)
        vwb__sts = context.make_array(table_idx_arr_t)(context, builder,
            rzn__klz)
        zhxhy__xbp = context.get_constant(types.int64, -1)
        zsdl__llx = context.get_constant(types.int64, 0)
        tddw__rdasm = cgutils.alloca_once_value(builder, zsdl__llx)
        for t, vvkrz__vvaqr in nvie__johf.type_to_blk.items():
            zxbu__cta = context.get_constant(types.int64, len(nvie__johf.
                block_to_arr_ind[vvkrz__vvaqr]))
            wqpcb__vwsb, zazll__fgnoa = ListInstance.allocate_ex(context,
                builder, types.List(t), zxbu__cta)
            zazll__fgnoa.size = zxbu__cta
            lphl__xjgm = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(nvie__johf.block_to_arr_ind[
                vvkrz__vvaqr], dtype=np.int64))
            tzlfr__lcke = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, lphl__xjgm)
            with cgutils.for_range(builder, zxbu__cta) as qwiwr__ntjl:
                egd__vfjr = qwiwr__ntjl.index
                crj__lzcad = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    tzlfr__lcke, egd__vfjr)
                wlc__bzuuc = _getitem_array_single_int(context, builder,
                    types.int64, table_idx_arr_t, vwb__sts, crj__lzcad)
                hexd__ryh = builder.icmp_unsigned('!=', wlc__bzuuc, zhxhy__xbp)
                with builder.if_else(hexd__ryh) as (zqms__dssa, eajje__kttpq):
                    with zqms__dssa:
                        znkoe__hbmch = builder.call(hgavb__vlh, [cpp_table,
                            wlc__bzuuc])
                        arr = context.compile_internal(builder, lambda info:
                            info_to_array(info, t), t(array_info_type), [
                            znkoe__hbmch])
                        zazll__fgnoa.inititem(egd__vfjr, arr, incref=False)
                        bednd__ubxl = context.compile_internal(builder, lambda
                            arr: len(arr), types.int64(t), [arr])
                        builder.store(bednd__ubxl, tddw__rdasm)
                    with eajje__kttpq:
                        atwno__kou = context.get_constant_null(t)
                        zazll__fgnoa.inititem(egd__vfjr, atwno__kou, incref
                            =False)
            setattr(eqn__sxmi, f'block_{vvkrz__vvaqr}', zazll__fgnoa.value)
        eqn__sxmi.len = builder.load(tddw__rdasm)
        return eqn__sxmi._getvalue()
    return nvie__johf(cpp_table_t, table_idx_arr_t, py_table_type_t), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def cpp_table_to_py_data(cpp_table, out_col_inds_t, out_types_t, n_rows_t,
    n_table_cols_t, unknown_cat_arrs_t=None, cat_inds_t=None):
    byy__aoye = out_col_inds_t.instance_type.meta
    nvie__johf = unwrap_typeref(out_types_t.types[0])
    chwoh__eva = [unwrap_typeref(out_types_t.types[egd__vfjr]) for
        egd__vfjr in range(1, len(out_types_t.types))]
    imbh__jwgm = {}
    xlhb__leze = get_overload_const_int(n_table_cols_t)
    xmdo__pykv = {qdoc__ddem: egd__vfjr for egd__vfjr, qdoc__ddem in
        enumerate(byy__aoye)}
    if not is_overload_none(unknown_cat_arrs_t):
        ygat__puuw = {ytedt__cvxvd: egd__vfjr for egd__vfjr, ytedt__cvxvd in
            enumerate(cat_inds_t.instance_type.meta)}
    kwavy__npoel = []
    zfyn__kgi = """def impl(cpp_table, out_col_inds_t, out_types_t, n_rows_t, n_table_cols_t, unknown_cat_arrs_t=None, cat_inds_t=None):
"""
    if isinstance(nvie__johf, bodo.TableType):
        zfyn__kgi += f'  py_table = init_table(py_table_type, False)\n'
        zfyn__kgi += f'  py_table = set_table_len(py_table, n_rows_t)\n'
        for bkqmy__radkf, vvkrz__vvaqr in nvie__johf.type_to_blk.items():
            liotl__xmmla = [xmdo__pykv.get(egd__vfjr, -1) for egd__vfjr in
                nvie__johf.block_to_arr_ind[vvkrz__vvaqr]]
            imbh__jwgm[f'out_inds_{vvkrz__vvaqr}'] = np.array(liotl__xmmla,
                np.int64)
            imbh__jwgm[f'out_type_{vvkrz__vvaqr}'] = bkqmy__radkf
            imbh__jwgm[f'typ_list_{vvkrz__vvaqr}'] = types.List(bkqmy__radkf)
            rkhri__bwglb = f'out_type_{vvkrz__vvaqr}'
            if type_has_unknown_cats(bkqmy__radkf):
                if is_overload_none(unknown_cat_arrs_t):
                    zfyn__kgi += f"""  in_arr_list_{vvkrz__vvaqr} = get_table_block(out_types_t[0], {vvkrz__vvaqr})
"""
                    rkhri__bwglb = f'in_arr_list_{vvkrz__vvaqr}[i]'
                else:
                    imbh__jwgm[f'cat_arr_inds_{vvkrz__vvaqr}'] = np.array([
                        ygat__puuw.get(egd__vfjr, -1) for egd__vfjr in
                        nvie__johf.block_to_arr_ind[vvkrz__vvaqr]], np.int64)
                    rkhri__bwglb = (
                        f'unknown_cat_arrs_t[cat_arr_inds_{vvkrz__vvaqr}[i]]')
            zxbu__cta = len(nvie__johf.block_to_arr_ind[vvkrz__vvaqr])
            zfyn__kgi += f"""  arr_list_{vvkrz__vvaqr} = alloc_list_like(typ_list_{vvkrz__vvaqr}, {zxbu__cta}, False)
"""
            zfyn__kgi += f'  for i in range(len(arr_list_{vvkrz__vvaqr})):\n'
            zfyn__kgi += (
                f'    cpp_ind_{vvkrz__vvaqr} = out_inds_{vvkrz__vvaqr}[i]\n')
            zfyn__kgi += f'    if cpp_ind_{vvkrz__vvaqr} == -1:\n'
            zfyn__kgi += f'      continue\n'
            zfyn__kgi += f"""    arr_{vvkrz__vvaqr} = info_to_array(info_from_table(cpp_table, cpp_ind_{vvkrz__vvaqr}), {rkhri__bwglb})
"""
            zfyn__kgi += (
                f'    arr_list_{vvkrz__vvaqr}[i] = arr_{vvkrz__vvaqr}\n')
            zfyn__kgi += f"""  py_table = set_table_block(py_table, arr_list_{vvkrz__vvaqr}, {vvkrz__vvaqr})
"""
        kwavy__npoel.append('py_table')
    elif nvie__johf != types.none:
        itmy__uadi = xmdo__pykv.get(0, -1)
        if itmy__uadi != -1:
            imbh__jwgm[f'arr_typ_arg0'] = nvie__johf
            rkhri__bwglb = f'arr_typ_arg0'
            if type_has_unknown_cats(nvie__johf):
                if is_overload_none(unknown_cat_arrs_t):
                    rkhri__bwglb = f'out_types_t[0]'
                else:
                    rkhri__bwglb = f'unknown_cat_arrs_t[{ygat__puuw[0]}]'
            zfyn__kgi += f"""  out_arg0 = info_to_array(info_from_table(cpp_table, {itmy__uadi}), {rkhri__bwglb})
"""
            kwavy__npoel.append('out_arg0')
    for egd__vfjr, t in enumerate(chwoh__eva):
        itmy__uadi = xmdo__pykv.get(xlhb__leze + egd__vfjr, -1)
        if itmy__uadi != -1:
            imbh__jwgm[f'extra_arr_type_{egd__vfjr}'] = t
            rkhri__bwglb = f'extra_arr_type_{egd__vfjr}'
            if type_has_unknown_cats(t):
                if is_overload_none(unknown_cat_arrs_t):
                    rkhri__bwglb = f'out_types_t[{egd__vfjr + 1}]'
                else:
                    rkhri__bwglb = (
                        f'unknown_cat_arrs_t[{ygat__puuw[xlhb__leze + egd__vfjr]}]'
                        )
            zfyn__kgi += f"""  out_{egd__vfjr} = info_to_array(info_from_table(cpp_table, {itmy__uadi}), {rkhri__bwglb})
"""
            kwavy__npoel.append(f'out_{egd__vfjr}')
    nau__epnde = ',' if len(kwavy__npoel) == 1 else ''
    zfyn__kgi += f"  return ({', '.join(kwavy__npoel)}{nau__epnde})\n"
    imbh__jwgm.update({'init_table': bodo.hiframes.table.init_table,
        'alloc_list_like': bodo.hiframes.table.alloc_list_like,
        'set_table_block': bodo.hiframes.table.set_table_block,
        'set_table_len': bodo.hiframes.table.set_table_len,
        'get_table_block': bodo.hiframes.table.get_table_block,
        'info_to_array': info_to_array, 'info_from_table': info_from_table,
        'out_col_inds': list(byy__aoye), 'py_table_type': nvie__johf})
    epqey__zeyb = {}
    exec(zfyn__kgi, imbh__jwgm, epqey__zeyb)
    return epqey__zeyb['impl']


@intrinsic
def py_table_to_cpp_table(typingctx, py_table_t, py_table_type_t):
    assert isinstance(py_table_t, bodo.hiframes.table.TableType
        ), 'invalid py table type'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    nvie__johf = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        py_table, wqpcb__vwsb = args
        iboy__thy = cgutils.create_struct_proxy(nvie__johf)(context,
            builder, py_table)
        if nvie__johf.has_runtime_cols:
            fgoi__gxkk = lir.Constant(lir.IntType(64), 0)
            for vvkrz__vvaqr, t in enumerate(nvie__johf.arr_types):
                yjvk__gaun = getattr(iboy__thy, f'block_{vvkrz__vvaqr}')
                ulsmq__uschr = ListInstance(context, builder, types.List(t),
                    yjvk__gaun)
                fgoi__gxkk = builder.add(fgoi__gxkk, ulsmq__uschr.size)
        else:
            fgoi__gxkk = lir.Constant(lir.IntType(64), len(nvie__johf.
                arr_types))
        wqpcb__vwsb, oeka__rrxsn = ListInstance.allocate_ex(context,
            builder, types.List(array_info_type), fgoi__gxkk)
        oeka__rrxsn.size = fgoi__gxkk
        if nvie__johf.has_runtime_cols:
            bfx__hdkff = lir.Constant(lir.IntType(64), 0)
            for vvkrz__vvaqr, t in enumerate(nvie__johf.arr_types):
                yjvk__gaun = getattr(iboy__thy, f'block_{vvkrz__vvaqr}')
                ulsmq__uschr = ListInstance(context, builder, types.List(t),
                    yjvk__gaun)
                zxbu__cta = ulsmq__uschr.size
                with cgutils.for_range(builder, zxbu__cta) as qwiwr__ntjl:
                    egd__vfjr = qwiwr__ntjl.index
                    arr = ulsmq__uschr.getitem(egd__vfjr)
                    phoo__rvj = signature(array_info_type, t)
                    yyvdu__ncj = arr,
                    fysm__ajtfa = array_to_info_codegen(context, builder,
                        phoo__rvj, yyvdu__ncj)
                    oeka__rrxsn.inititem(builder.add(bfx__hdkff, egd__vfjr),
                        fysm__ajtfa, incref=False)
                bfx__hdkff = builder.add(bfx__hdkff, zxbu__cta)
        else:
            for t, vvkrz__vvaqr in nvie__johf.type_to_blk.items():
                zxbu__cta = context.get_constant(types.int64, len(
                    nvie__johf.block_to_arr_ind[vvkrz__vvaqr]))
                yjvk__gaun = getattr(iboy__thy, f'block_{vvkrz__vvaqr}')
                ulsmq__uschr = ListInstance(context, builder, types.List(t),
                    yjvk__gaun)
                lphl__xjgm = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(nvie__johf.
                    block_to_arr_ind[vvkrz__vvaqr], dtype=np.int64))
                tzlfr__lcke = context.make_array(types.Array(types.int64, 1,
                    'C'))(context, builder, lphl__xjgm)
                with cgutils.for_range(builder, zxbu__cta) as qwiwr__ntjl:
                    egd__vfjr = qwiwr__ntjl.index
                    crj__lzcad = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        tzlfr__lcke, egd__vfjr)
                    tdmqn__vxi = signature(types.none, nvie__johf, types.
                        List(t), types.int64, types.int64)
                    azlw__yrx = py_table, yjvk__gaun, egd__vfjr, crj__lzcad
                    bodo.hiframes.table.ensure_column_unboxed_codegen(context,
                        builder, tdmqn__vxi, azlw__yrx)
                    arr = ulsmq__uschr.getitem(egd__vfjr)
                    phoo__rvj = signature(array_info_type, t)
                    yyvdu__ncj = arr,
                    fysm__ajtfa = array_to_info_codegen(context, builder,
                        phoo__rvj, yyvdu__ncj)
                    oeka__rrxsn.inititem(crj__lzcad, fysm__ajtfa, incref=False)
        cwni__jsrt = oeka__rrxsn.value
        xcb__crcok = signature(table_type, types.List(array_info_type))
        zihj__ihe = cwni__jsrt,
        cpp_table = arr_info_list_to_table_codegen(context, builder,
            xcb__crcok, zihj__ihe)
        context.nrt.decref(builder, types.List(array_info_type), cwni__jsrt)
        return cpp_table
    return table_type(nvie__johf, py_table_type_t), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def py_data_to_cpp_table(py_table, extra_arrs_tup, in_col_inds_t,
    n_table_cols_t):
    gpejo__lcg = in_col_inds_t.instance_type.meta
    imbh__jwgm = {}
    xlhb__leze = get_overload_const_int(n_table_cols_t)
    gcuzw__khob = defaultdict(list)
    xmdo__pykv = {}
    for egd__vfjr, qdoc__ddem in enumerate(gpejo__lcg):
        if qdoc__ddem in xmdo__pykv:
            gcuzw__khob[qdoc__ddem].append(egd__vfjr)
        else:
            xmdo__pykv[qdoc__ddem] = egd__vfjr
    zfyn__kgi = (
        'def impl(py_table, extra_arrs_tup, in_col_inds_t, n_table_cols_t):\n')
    zfyn__kgi += (
        f'  cpp_arr_list = alloc_empty_list_type({len(gpejo__lcg)}, array_info_type)\n'
        )
    if py_table != types.none:
        for vvkrz__vvaqr in py_table.type_to_blk.values():
            liotl__xmmla = [xmdo__pykv.get(egd__vfjr, -1) for egd__vfjr in
                py_table.block_to_arr_ind[vvkrz__vvaqr]]
            imbh__jwgm[f'out_inds_{vvkrz__vvaqr}'] = np.array(liotl__xmmla,
                np.int64)
            imbh__jwgm[f'arr_inds_{vvkrz__vvaqr}'] = np.array(py_table.
                block_to_arr_ind[vvkrz__vvaqr], np.int64)
            zfyn__kgi += (
                f'  arr_list_{vvkrz__vvaqr} = get_table_block(py_table, {vvkrz__vvaqr})\n'
                )
            zfyn__kgi += f'  for i in range(len(arr_list_{vvkrz__vvaqr})):\n'
            zfyn__kgi += (
                f'    out_arr_ind_{vvkrz__vvaqr} = out_inds_{vvkrz__vvaqr}[i]\n'
                )
            zfyn__kgi += f'    if out_arr_ind_{vvkrz__vvaqr} == -1:\n'
            zfyn__kgi += f'      continue\n'
            zfyn__kgi += (
                f'    arr_ind_{vvkrz__vvaqr} = arr_inds_{vvkrz__vvaqr}[i]\n')
            zfyn__kgi += f"""    ensure_column_unboxed(py_table, arr_list_{vvkrz__vvaqr}, i, arr_ind_{vvkrz__vvaqr})
"""
            zfyn__kgi += f"""    cpp_arr_list[out_arr_ind_{vvkrz__vvaqr}] = array_to_info(arr_list_{vvkrz__vvaqr}[i])
"""
        for jlqsr__zmsc, bywcy__nnc in gcuzw__khob.items():
            if jlqsr__zmsc < xlhb__leze:
                vvkrz__vvaqr = py_table.block_nums[jlqsr__zmsc]
                hylk__hug = py_table.block_offsets[jlqsr__zmsc]
                for itmy__uadi in bywcy__nnc:
                    zfyn__kgi += f"""  cpp_arr_list[{itmy__uadi}] = array_to_info(arr_list_{vvkrz__vvaqr}[{hylk__hug}])
"""
    for egd__vfjr in range(len(extra_arrs_tup)):
        hrd__wzu = xmdo__pykv.get(xlhb__leze + egd__vfjr, -1)
        if hrd__wzu != -1:
            islbf__labw = [hrd__wzu] + gcuzw__khob.get(xlhb__leze +
                egd__vfjr, [])
            for itmy__uadi in islbf__labw:
                zfyn__kgi += f"""  cpp_arr_list[{itmy__uadi}] = array_to_info(extra_arrs_tup[{egd__vfjr}])
"""
    zfyn__kgi += f'  return arr_info_list_to_table(cpp_arr_list)\n'
    imbh__jwgm.update({'array_info_type': array_info_type,
        'alloc_empty_list_type': bodo.hiframes.table.alloc_empty_list_type,
        'get_table_block': bodo.hiframes.table.get_table_block,
        'ensure_column_unboxed': bodo.hiframes.table.ensure_column_unboxed,
        'array_to_info': array_to_info, 'arr_info_list_to_table':
        arr_info_list_to_table})
    epqey__zeyb = {}
    exec(zfyn__kgi, imbh__jwgm, epqey__zeyb)
    return epqey__zeyb['impl']


delete_info_decref_array = types.ExternalFunction('delete_info_decref_array',
    types.void(array_info_type))
delete_table_decref_arrays = types.ExternalFunction(
    'delete_table_decref_arrays', types.void(table_type))
decref_table_array = types.ExternalFunction('decref_table_array', types.
    void(table_type, types.int32))


@intrinsic
def delete_table(typingctx, table_t=None):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        ymrbe__mwwp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='delete_table')
        builder.call(hgavb__vlh, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='shuffle_table')
        txiwx__ith = builder.call(hgavb__vlh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return txiwx__ith
    return table_type(table_t, types.int64, types.boolean, types.int32
        ), codegen


class ShuffleInfoType(types.Type):

    def __init__(self):
        super(ShuffleInfoType, self).__init__(name='ShuffleInfoType()')


shuffle_info_type = ShuffleInfoType()
register_model(ShuffleInfoType)(models.OpaqueModel)
get_shuffle_info = types.ExternalFunction('get_shuffle_info',
    shuffle_info_type(table_type))


@intrinsic
def delete_shuffle_info(typingctx, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[0] == types.none:
            return
        ymrbe__mwwp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='delete_shuffle_info')
        return builder.call(hgavb__vlh, args)
    return types.void(shuffle_info_t), codegen


@intrinsic
def reverse_shuffle_table(typingctx, table_t, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[-1] == types.none:
            return context.get_constant_null(table_type)
        ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='reverse_shuffle_table')
        return builder.call(hgavb__vlh, args)
    return table_type(table_type, shuffle_info_t), codegen


@intrinsic
def get_null_shuffle_info(typingctx):

    def codegen(context, builder, sig, args):
        return context.get_constant_null(sig.return_type)
    return shuffle_info_type(), codegen


@intrinsic
def hash_join_table(typingctx, left_table_t, right_table_t, left_parallel_t,
    right_parallel_t, n_keys_t, n_data_left_t, n_data_right_t, same_vect_t,
    key_in_out_t, same_need_typechange_t, is_left_t, is_right_t, is_join_t,
    extra_data_col_t, indicator, _bodo_na_equal, cond_func, left_col_nums,
    left_col_nums_len, right_col_nums, right_col_nums_len, num_rows_ptr_t):
    assert left_table_t == table_type
    assert right_table_t == table_type

    def codegen(context, builder, sig, args):
        ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(1), lir
            .IntType(1), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(64), lir.IntType(8).as_pointer()])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='hash_join_table')
        txiwx__ith = builder.call(hgavb__vlh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return txiwx__ith
    return table_type(left_table_t, right_table_t, types.boolean, types.
        boolean, types.int64, types.int64, types.int64, types.voidptr,
        types.voidptr, types.voidptr, types.boolean, types.boolean, types.
        boolean, types.boolean, types.boolean, types.boolean, types.voidptr,
        types.voidptr, types.int64, types.voidptr, types.int64, types.voidptr
        ), codegen


@intrinsic
def sort_values_table(typingctx, table_t, n_keys_t, vect_ascending_t,
    na_position_b_t, dead_keys_t, n_rows_t, parallel_t):
    assert table_t == table_type, 'C++ table type expected'

    def codegen(context, builder, sig, args):
        ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='sort_values_table')
        txiwx__ith = builder.call(hgavb__vlh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return txiwx__ith
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='sample_table')
        txiwx__ith = builder.call(hgavb__vlh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return txiwx__ith
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='shuffle_renormalization')
        txiwx__ith = builder.call(hgavb__vlh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return txiwx__ith
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='shuffle_renormalization_group')
        txiwx__ith = builder.call(hgavb__vlh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return txiwx__ith
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    dropna, drop_local_first):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(1), lir.IntType(1)])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='drop_duplicates_table')
        txiwx__ith = builder.call(hgavb__vlh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return txiwx__ith
    return table_type(table_t, types.boolean, types.int64, types.int64,
        types.boolean, types.boolean), codegen


@intrinsic
def groupby_and_aggregate(typingctx, table_t, n_keys_t, input_has_index,
    ftypes, func_offsets, udf_n_redvars, is_parallel, skipdropna_t,
    shift_periods_t, transform_func, head_n, return_keys, return_index,
    dropna, update_cb, combine_cb, eval_cb, general_udfs_cb,
    udf_table_dummy_t, n_out_rows_t, n_shuffle_keys_t):
    assert table_t == table_type
    assert udf_table_dummy_t == table_type

    def codegen(context, builder, sig, args):
        ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(64), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        hgavb__vlh = cgutils.get_or_insert_function(builder.module,
            ymrbe__mwwp, name='groupby_and_aggregate')
        txiwx__ith = builder.call(hgavb__vlh, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return txiwx__ith
    return table_type(table_t, types.int64, types.boolean, types.voidptr,
        types.voidptr, types.voidptr, types.boolean, types.boolean, types.
        int64, types.int64, types.int64, types.boolean, types.boolean,
        types.boolean, types.voidptr, types.voidptr, types.voidptr, types.
        voidptr, table_t, types.voidptr, types.int64), codegen


_convert_local_dictionary_to_global = types.ExternalFunction(
    'convert_local_dictionary_to_global', types.void(array_info_type, types
    .bool_))


@numba.njit(no_cpython_wrapper=True)
def convert_local_dictionary_to_global(dict_arr, sort_dictionary):
    fhvpv__twtlh = array_to_info(dict_arr)
    _convert_local_dictionary_to_global(fhvpv__twtlh, sort_dictionary)
    check_and_propagate_cpp_exception()
    out_arr = info_to_array(fhvpv__twtlh, bodo.dict_str_arr_type)
    return out_arr


get_groupby_labels = types.ExternalFunction('get_groupby_labels', types.
    int64(table_type, types.voidptr, types.voidptr, types.boolean, types.bool_)
    )
_array_isin = types.ExternalFunction('array_isin', types.void(
    array_info_type, array_info_type, array_info_type, types.bool_))


@numba.njit(no_cpython_wrapper=True)
def array_isin(out_arr, in_arr, in_values, is_parallel):
    in_arr = decode_if_dict_array(in_arr)
    in_values = decode_if_dict_array(in_values)
    zdmzm__vhmco = array_to_info(in_arr)
    pvdjg__zbjm = array_to_info(in_values)
    abt__xwfdx = array_to_info(out_arr)
    wouq__ogtso = arr_info_list_to_table([zdmzm__vhmco, pvdjg__zbjm,
        abt__xwfdx])
    _array_isin(abt__xwfdx, zdmzm__vhmco, pvdjg__zbjm, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(wouq__ogtso)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.bool_, types.voidptr, array_info_type))


@numba.njit(no_cpython_wrapper=True)
def get_search_regex(in_arr, case, match, pat, out_arr):
    zdmzm__vhmco = array_to_info(in_arr)
    abt__xwfdx = array_to_info(out_arr)
    _get_search_regex(zdmzm__vhmco, case, match, pat, abt__xwfdx)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_array_typ, c_ind):
    from llvmlite import ir as lir
    oxot__hfe = col_array_typ.dtype
    if isinstance(oxot__hfe, (types.Number, TimeType)) or oxot__hfe in [bodo
        .datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                eqn__sxmi, bzz__qfgyo = args
                eqn__sxmi = builder.bitcast(eqn__sxmi, lir.IntType(8).
                    as_pointer().as_pointer())
                pvzb__wfai = lir.Constant(lir.IntType(64), c_ind)
                tvnzv__oncwn = builder.load(builder.gep(eqn__sxmi, [
                    pvzb__wfai]))
                tvnzv__oncwn = builder.bitcast(tvnzv__oncwn, context.
                    get_data_type(oxot__hfe).as_pointer())
                return builder.load(builder.gep(tvnzv__oncwn, [bzz__qfgyo]))
            return oxot__hfe(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ in (bodo.string_array_type, bodo.binary_array_type):

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                eqn__sxmi, bzz__qfgyo = args
                eqn__sxmi = builder.bitcast(eqn__sxmi, lir.IntType(8).
                    as_pointer().as_pointer())
                pvzb__wfai = lir.Constant(lir.IntType(64), c_ind)
                tvnzv__oncwn = builder.load(builder.gep(eqn__sxmi, [
                    pvzb__wfai]))
                ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                amc__qrcah = cgutils.get_or_insert_function(builder.module,
                    ymrbe__mwwp, name='array_info_getitem')
                vrukg__qheq = cgutils.alloca_once(builder, lir.IntType(64))
                args = tvnzv__oncwn, bzz__qfgyo, vrukg__qheq
                amr__evv = builder.call(amc__qrcah, args)
                return context.make_tuple(builder, sig.return_type, [
                    amr__evv, builder.load(vrukg__qheq)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.libs.dict_arr_ext.dict_str_arr_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                jlb__ezcp = lir.Constant(lir.IntType(64), 1)
                fwj__idw = lir.Constant(lir.IntType(64), 2)
                eqn__sxmi, bzz__qfgyo = args
                eqn__sxmi = builder.bitcast(eqn__sxmi, lir.IntType(8).
                    as_pointer().as_pointer())
                pvzb__wfai = lir.Constant(lir.IntType(64), c_ind)
                tvnzv__oncwn = builder.load(builder.gep(eqn__sxmi, [
                    pvzb__wfai]))
                ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64)])
                pojmn__qzfsq = cgutils.get_or_insert_function(builder.
                    module, ymrbe__mwwp, name='get_nested_info')
                args = tvnzv__oncwn, fwj__idw
                eecfo__aea = builder.call(pojmn__qzfsq, args)
                ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer()])
                ppf__pxfgb = cgutils.get_or_insert_function(builder.module,
                    ymrbe__mwwp, name='array_info_getdata1')
                args = eecfo__aea,
                dkfx__yapo = builder.call(ppf__pxfgb, args)
                dkfx__yapo = builder.bitcast(dkfx__yapo, context.
                    get_data_type(col_array_typ.indices_dtype).as_pointer())
                vblq__yku = builder.sext(builder.load(builder.gep(
                    dkfx__yapo, [bzz__qfgyo])), lir.IntType(64))
                args = tvnzv__oncwn, jlb__ezcp
                bqegc__pqelc = builder.call(pojmn__qzfsq, args)
                ymrbe__mwwp = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                amc__qrcah = cgutils.get_or_insert_function(builder.module,
                    ymrbe__mwwp, name='array_info_getitem')
                vrukg__qheq = cgutils.alloca_once(builder, lir.IntType(64))
                args = bqegc__pqelc, vblq__yku, vrukg__qheq
                amr__evv = builder.call(amc__qrcah, args)
                return context.make_tuple(builder, sig.return_type, [
                    amr__evv, builder.load(vrukg__qheq)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{oxot__hfe}' column data type not supported"
        )


def _gen_row_na_check_intrinsic(col_array_dtype, c_ind):
    if isinstance(col_array_dtype, bodo.libs.int_arr_ext.IntegerArrayType
        ) or col_array_dtype in (bodo.libs.bool_arr_ext.boolean_array, bodo
        .binary_array_type) or is_str_arr_type(col_array_dtype) or isinstance(
        col_array_dtype, types.Array) and (col_array_dtype.dtype == bodo.
        datetime_date_type or isinstance(col_array_dtype.dtype, bodo.TimeType)
        ):

        @intrinsic
        def checkna_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                ikud__xlxwt, bzz__qfgyo = args
                ikud__xlxwt = builder.bitcast(ikud__xlxwt, lir.IntType(8).
                    as_pointer().as_pointer())
                pvzb__wfai = lir.Constant(lir.IntType(64), c_ind)
                tvnzv__oncwn = builder.load(builder.gep(ikud__xlxwt, [
                    pvzb__wfai]))
                tvwnd__con = builder.bitcast(tvnzv__oncwn, context.
                    get_data_type(types.bool_).as_pointer())
                ddnau__bldy = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    tvwnd__con, bzz__qfgyo)
                aciwg__lewgs = builder.icmp_unsigned('!=', ddnau__bldy, lir
                    .Constant(lir.IntType(8), 0))
                return builder.sext(aciwg__lewgs, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, types.Array):
        oxot__hfe = col_array_dtype.dtype
        if oxot__hfe in [bodo.datetime64ns, bodo.timedelta64ns]:

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    eqn__sxmi, bzz__qfgyo = args
                    eqn__sxmi = builder.bitcast(eqn__sxmi, lir.IntType(8).
                        as_pointer().as_pointer())
                    pvzb__wfai = lir.Constant(lir.IntType(64), c_ind)
                    tvnzv__oncwn = builder.load(builder.gep(eqn__sxmi, [
                        pvzb__wfai]))
                    tvnzv__oncwn = builder.bitcast(tvnzv__oncwn, context.
                        get_data_type(oxot__hfe).as_pointer())
                    udljz__pjran = builder.load(builder.gep(tvnzv__oncwn, [
                        bzz__qfgyo]))
                    aciwg__lewgs = builder.icmp_unsigned('!=', udljz__pjran,
                        lir.Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(aciwg__lewgs, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(oxot__hfe, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    eqn__sxmi, bzz__qfgyo = args
                    eqn__sxmi = builder.bitcast(eqn__sxmi, lir.IntType(8).
                        as_pointer().as_pointer())
                    pvzb__wfai = lir.Constant(lir.IntType(64), c_ind)
                    tvnzv__oncwn = builder.load(builder.gep(eqn__sxmi, [
                        pvzb__wfai]))
                    tvnzv__oncwn = builder.bitcast(tvnzv__oncwn, context.
                        get_data_type(oxot__hfe).as_pointer())
                    udljz__pjran = builder.load(builder.gep(tvnzv__oncwn, [
                        bzz__qfgyo]))
                    gsj__rkba = signature(types.bool_, oxot__hfe)
                    ddnau__bldy = numba.np.npyfuncs.np_real_isnan_impl(context,
                        builder, gsj__rkba, (udljz__pjran,))
                    return builder.not_(builder.sext(ddnau__bldy, lir.
                        IntType(8)))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
