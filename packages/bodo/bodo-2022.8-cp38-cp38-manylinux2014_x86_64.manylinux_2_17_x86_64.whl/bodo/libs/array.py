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
        ouo__deda = context.make_helper(builder, arr_type, in_arr)
        in_arr = ouo__deda.data
        arr_type = StructArrayType(arr_type.data, ('dummy',) * len(arr_type
            .data))
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        cleix__xwjlj = context.make_helper(builder, arr_type, in_arr)
        xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='list_string_array_to_info')
        return builder.call(vyhbj__gvcs, [cleix__xwjlj.meminfo])
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType, StructArrayType)
        ):

        def get_types(arr_typ):
            if isinstance(arr_typ, MapArrayType):
                return get_types(_get_map_arr_data_type(arr_typ))
            elif isinstance(arr_typ, ArrayItemArrayType):
                return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
            elif isinstance(arr_typ, (StructType, StructArrayType)):
                sukj__mfgw = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                for qna__ltw in arr_typ.data:
                    sukj__mfgw += get_types(qna__ltw)
                return sukj__mfgw
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
            bbcc__jivp = context.compile_internal(builder, lambda a: len(a),
                types.intp(arr_typ), [arr])
            if isinstance(arr_typ, MapArrayType):
                xrewu__hwrl = context.make_helper(builder, arr_typ, value=arr)
                epgxe__qtywp = get_lengths(_get_map_arr_data_type(arr_typ),
                    xrewu__hwrl.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                ymu__sfmhy = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                epgxe__qtywp = get_lengths(arr_typ.dtype, ymu__sfmhy.data)
                epgxe__qtywp = cgutils.pack_array(builder, [ymu__sfmhy.
                    n_arrays] + [builder.extract_value(epgxe__qtywp,
                    ysvp__uwowf) for ysvp__uwowf in range(epgxe__qtywp.type
                    .count)])
            elif isinstance(arr_typ, StructArrayType):
                ymu__sfmhy = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                epgxe__qtywp = []
                for ysvp__uwowf, qna__ltw in enumerate(arr_typ.data):
                    cbuj__wsvfb = get_lengths(qna__ltw, builder.
                        extract_value(ymu__sfmhy.data, ysvp__uwowf))
                    epgxe__qtywp += [builder.extract_value(cbuj__wsvfb,
                        xdya__exz) for xdya__exz in range(cbuj__wsvfb.type.
                        count)]
                epgxe__qtywp = cgutils.pack_array(builder, [bbcc__jivp,
                    context.get_constant(types.int64, -1)] + epgxe__qtywp)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType,
                types.Array)) or arr_typ in (boolean_array,
                datetime_date_array_type, string_array_type, binary_array_type
                ):
                epgxe__qtywp = cgutils.pack_array(builder, [bbcc__jivp])
            else:
                raise BodoError(
                    f'array_to_info: unsupported type for subarray {arr_typ}')
            return epgxe__qtywp

        def get_buffers(arr_typ, arr):
            if isinstance(arr_typ, MapArrayType):
                xrewu__hwrl = context.make_helper(builder, arr_typ, value=arr)
                wkg__bzwc = get_buffers(_get_map_arr_data_type(arr_typ),
                    xrewu__hwrl.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                ymu__sfmhy = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                olrjs__xwja = get_buffers(arr_typ.dtype, ymu__sfmhy.data)
                oyufa__zcg = context.make_array(types.Array(offset_type, 1,
                    'C'))(context, builder, ymu__sfmhy.offsets)
                pwbef__uaart = builder.bitcast(oyufa__zcg.data, lir.IntType
                    (8).as_pointer())
                bobh__eyry = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, ymu__sfmhy.null_bitmap)
                uxu__xsb = builder.bitcast(bobh__eyry.data, lir.IntType(8).
                    as_pointer())
                wkg__bzwc = cgutils.pack_array(builder, [pwbef__uaart,
                    uxu__xsb] + [builder.extract_value(olrjs__xwja,
                    ysvp__uwowf) for ysvp__uwowf in range(olrjs__xwja.type.
                    count)])
            elif isinstance(arr_typ, StructArrayType):
                ymu__sfmhy = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                olrjs__xwja = []
                for ysvp__uwowf, qna__ltw in enumerate(arr_typ.data):
                    zdu__ewgd = get_buffers(qna__ltw, builder.extract_value
                        (ymu__sfmhy.data, ysvp__uwowf))
                    olrjs__xwja += [builder.extract_value(zdu__ewgd,
                        xdya__exz) for xdya__exz in range(zdu__ewgd.type.count)
                        ]
                bobh__eyry = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, ymu__sfmhy.null_bitmap)
                uxu__xsb = builder.bitcast(bobh__eyry.data, lir.IntType(8).
                    as_pointer())
                wkg__bzwc = cgutils.pack_array(builder, [uxu__xsb] +
                    olrjs__xwja)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
                ) or arr_typ in (boolean_array, datetime_date_array_type):
                nan__yts = arr_typ.dtype
                if isinstance(arr_typ, DecimalArrayType):
                    nan__yts = int128_type
                elif arr_typ == datetime_date_array_type:
                    nan__yts = types.int64
                arr = cgutils.create_struct_proxy(arr_typ)(context, builder,
                    arr)
                ijop__hcpa = context.make_array(types.Array(nan__yts, 1, 'C'))(
                    context, builder, arr.data)
                bobh__eyry = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, arr.null_bitmap)
                lduas__ntc = builder.bitcast(ijop__hcpa.data, lir.IntType(8
                    ).as_pointer())
                uxu__xsb = builder.bitcast(bobh__eyry.data, lir.IntType(8).
                    as_pointer())
                wkg__bzwc = cgutils.pack_array(builder, [uxu__xsb, lduas__ntc])
            elif arr_typ in (string_array_type, binary_array_type):
                ymu__sfmhy = _get_str_binary_arr_payload(context, builder,
                    arr, arr_typ)
                zplt__yeq = context.make_helper(builder, offset_arr_type,
                    ymu__sfmhy.offsets).data
                xvg__wlr = context.make_helper(builder, char_arr_type,
                    ymu__sfmhy.data).data
                skfq__uzsuv = context.make_helper(builder,
                    null_bitmap_arr_type, ymu__sfmhy.null_bitmap).data
                wkg__bzwc = cgutils.pack_array(builder, [builder.bitcast(
                    zplt__yeq, lir.IntType(8).as_pointer()), builder.
                    bitcast(skfq__uzsuv, lir.IntType(8).as_pointer()),
                    builder.bitcast(xvg__wlr, lir.IntType(8).as_pointer())])
            elif isinstance(arr_typ, types.Array):
                arr = context.make_array(arr_typ)(context, builder, arr)
                lduas__ntc = builder.bitcast(arr.data, lir.IntType(8).
                    as_pointer())
                zrtrl__ujsft = lir.Constant(lir.IntType(8).as_pointer(), None)
                wkg__bzwc = cgutils.pack_array(builder, [zrtrl__ujsft,
                    lduas__ntc])
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray ' + str(
                    arr_typ))
            return wkg__bzwc

        def get_field_names(arr_typ):
            rnr__pcus = []
            if isinstance(arr_typ, StructArrayType):
                for xul__httho, orsxx__rhwf in zip(arr_typ.dtype.names,
                    arr_typ.data):
                    rnr__pcus.append(xul__httho)
                    rnr__pcus += get_field_names(orsxx__rhwf)
            elif isinstance(arr_typ, ArrayItemArrayType):
                rnr__pcus += get_field_names(arr_typ.dtype)
            elif isinstance(arr_typ, MapArrayType):
                rnr__pcus += get_field_names(_get_map_arr_data_type(arr_typ))
            return rnr__pcus
        sukj__mfgw = get_types(arr_type)
        ougi__hekhu = cgutils.pack_array(builder, [context.get_constant(
            types.int32, t) for t in sukj__mfgw])
        iqjl__dls = cgutils.alloca_once_value(builder, ougi__hekhu)
        epgxe__qtywp = get_lengths(arr_type, in_arr)
        lengths_ptr = cgutils.alloca_once_value(builder, epgxe__qtywp)
        wkg__bzwc = get_buffers(arr_type, in_arr)
        gml__rcsex = cgutils.alloca_once_value(builder, wkg__bzwc)
        rnr__pcus = get_field_names(arr_type)
        if len(rnr__pcus) == 0:
            rnr__pcus = ['irrelevant']
        iyslt__dfwu = cgutils.pack_array(builder, [context.
            insert_const_string(builder.module, a) for a in rnr__pcus])
        pix__krfxs = cgutils.alloca_once_value(builder, iyslt__dfwu)
        if isinstance(arr_type, MapArrayType):
            wuwi__imsm = _get_map_arr_data_type(arr_type)
            gpxy__guxt = context.make_helper(builder, arr_type, value=in_arr)
            clfd__zexa = gpxy__guxt.data
        else:
            wuwi__imsm = arr_type
            clfd__zexa = in_arr
        wjupm__udj = context.make_helper(builder, wuwi__imsm, clfd__zexa)
        xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(32).as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='nested_array_to_info')
        kkwfx__twlh = builder.call(vyhbj__gvcs, [builder.bitcast(iqjl__dls,
            lir.IntType(32).as_pointer()), builder.bitcast(gml__rcsex, lir.
            IntType(8).as_pointer().as_pointer()), builder.bitcast(
            lengths_ptr, lir.IntType(64).as_pointer()), builder.bitcast(
            pix__krfxs, lir.IntType(8).as_pointer()), wjupm__udj.meminfo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return kkwfx__twlh
    if arr_type in (string_array_type, binary_array_type):
        vyzsa__yguhe = context.make_helper(builder, arr_type, in_arr)
        ufdo__ucsk = ArrayItemArrayType(char_arr_type)
        cleix__xwjlj = context.make_helper(builder, ufdo__ucsk,
            vyzsa__yguhe.data)
        ymu__sfmhy = _get_str_binary_arr_payload(context, builder, in_arr,
            arr_type)
        zplt__yeq = context.make_helper(builder, offset_arr_type,
            ymu__sfmhy.offsets).data
        xvg__wlr = context.make_helper(builder, char_arr_type, ymu__sfmhy.data
            ).data
        skfq__uzsuv = context.make_helper(builder, null_bitmap_arr_type,
            ymu__sfmhy.null_bitmap).data
        dbrzv__jfgg = builder.zext(builder.load(builder.gep(zplt__yeq, [
            ymu__sfmhy.n_arrays])), lir.IntType(64))
        clrl__ynhp = context.get_constant(types.int32, int(arr_type ==
            binary_array_type))
        xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='string_array_to_info')
        return builder.call(vyhbj__gvcs, [ymu__sfmhy.n_arrays, dbrzv__jfgg,
            xvg__wlr, zplt__yeq, skfq__uzsuv, cleix__xwjlj.meminfo, clrl__ynhp]
            )
    if arr_type == bodo.dict_str_arr_type:
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        nkoy__jbber = arr.data
        vmrin__fekl = arr.indices
        sig = array_info_type(arr_type.data)
        nobr__akwx = array_to_info_codegen(context, builder, sig, (
            nkoy__jbber,), False)
        sig = array_info_type(bodo.libs.dict_arr_ext.dict_indices_arr_type)
        jop__xphg = array_to_info_codegen(context, builder, sig, (
            vmrin__fekl,), False)
        xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(32)])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='dict_str_array_to_info')
        gbdmy__mjzly = builder.zext(arr.has_global_dictionary, lir.IntType(32))
        return builder.call(vyhbj__gvcs, [nobr__akwx, jop__xphg, gbdmy__mjzly])
    slmt__nbvj = False
    if isinstance(arr_type, CategoricalArrayType):
        context.nrt.decref(builder, arr_type, in_arr)
        wkaul__vrqd = context.compile_internal(builder, lambda a: len(a.
            dtype.categories), types.intp(arr_type), [in_arr])
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).codes
        scjrn__rjjk = get_categories_int_type(arr_type.dtype)
        arr_type = types.Array(scjrn__rjjk, 1, 'C')
        slmt__nbvj = True
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, bodo.DatetimeArrayType):
        if slmt__nbvj:
            raise BodoError(
                'array_to_info(): Categorical PandasDatetimeArrayType not supported'
                )
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).data
        arr_type = arr_type.data_array_type
    if isinstance(arr_type, types.Array):
        arr = context.make_array(arr_type)(context, builder, in_arr)
        assert arr_type.ndim == 1, 'only 1D array shuffle supported'
        bbcc__jivp = builder.extract_value(arr.shape, 0)
        bkvt__obna = arr_type.dtype
        efksi__giy = numba_to_c_type(bkvt__obna)
        dyotd__qbb = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), efksi__giy))
        if slmt__nbvj:
            xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(64), lir.IntType(8).as_pointer()])
            vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
                xswa__hvuyk, name='categorical_array_to_info')
            return builder.call(vyhbj__gvcs, [bbcc__jivp, builder.bitcast(
                arr.data, lir.IntType(8).as_pointer()), builder.load(
                dyotd__qbb), wkaul__vrqd, arr.meminfo])
        else:
            xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer()])
            vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
                xswa__hvuyk, name='numpy_array_to_info')
            return builder.call(vyhbj__gvcs, [bbcc__jivp, builder.bitcast(
                arr.data, lir.IntType(8).as_pointer()), builder.load(
                dyotd__qbb), arr.meminfo])
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType, TimeArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        bkvt__obna = arr_type.dtype
        nan__yts = bkvt__obna
        if isinstance(arr_type, DecimalArrayType):
            nan__yts = int128_type
        if arr_type == datetime_date_array_type:
            nan__yts = types.int64
        ijop__hcpa = context.make_array(types.Array(nan__yts, 1, 'C'))(context,
            builder, arr.data)
        bbcc__jivp = builder.extract_value(ijop__hcpa.shape, 0)
        focw__vfjm = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, arr.null_bitmap)
        efksi__giy = numba_to_c_type(bkvt__obna)
        dyotd__qbb = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), efksi__giy))
        if isinstance(arr_type, DecimalArrayType):
            xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer(), lir.IntType(32), lir.
                IntType(32)])
            vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
                xswa__hvuyk, name='decimal_array_to_info')
            return builder.call(vyhbj__gvcs, [bbcc__jivp, builder.bitcast(
                ijop__hcpa.data, lir.IntType(8).as_pointer()), builder.load
                (dyotd__qbb), builder.bitcast(focw__vfjm.data, lir.IntType(
                8).as_pointer()), ijop__hcpa.meminfo, focw__vfjm.meminfo,
                context.get_constant(types.int32, arr_type.precision),
                context.get_constant(types.int32, arr_type.scale)])
        elif isinstance(arr_type, TimeArrayType):
            xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer(), lir.IntType(32)])
            vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
                xswa__hvuyk, name='time_array_to_info')
            return builder.call(vyhbj__gvcs, [bbcc__jivp, builder.bitcast(
                ijop__hcpa.data, lir.IntType(8).as_pointer()), builder.load
                (dyotd__qbb), builder.bitcast(focw__vfjm.data, lir.IntType(
                8).as_pointer()), ijop__hcpa.meminfo, focw__vfjm.meminfo,
                lir.Constant(lir.IntType(32), arr_type.precision)])
        else:
            xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer()])
            vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
                xswa__hvuyk, name='nullable_array_to_info')
            return builder.call(vyhbj__gvcs, [bbcc__jivp, builder.bitcast(
                ijop__hcpa.data, lir.IntType(8).as_pointer()), builder.load
                (dyotd__qbb), builder.bitcast(focw__vfjm.data, lir.IntType(
                8).as_pointer()), ijop__hcpa.meminfo, focw__vfjm.meminfo])
    if isinstance(arr_type, IntervalArrayType):
        assert isinstance(arr_type.arr_type, types.Array
            ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        equr__sgsr = context.make_array(arr_type.arr_type)(context, builder,
            arr.left)
        gqpmw__dwh = context.make_array(arr_type.arr_type)(context, builder,
            arr.right)
        bbcc__jivp = builder.extract_value(equr__sgsr.shape, 0)
        efksi__giy = numba_to_c_type(arr_type.arr_type.dtype)
        dyotd__qbb = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), efksi__giy))
        xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='interval_array_to_info')
        return builder.call(vyhbj__gvcs, [bbcc__jivp, builder.bitcast(
            equr__sgsr.data, lir.IntType(8).as_pointer()), builder.bitcast(
            gqpmw__dwh.data, lir.IntType(8).as_pointer()), builder.load(
            dyotd__qbb), equr__sgsr.meminfo, gqpmw__dwh.meminfo])
    raise_bodo_error(f'array_to_info(): array type {arr_type} is not supported'
        )


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    vjcx__qbdpl = cgutils.alloca_once(builder, lir.IntType(64))
    lduas__ntc = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    tcv__rrfs = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    xswa__hvuyk = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
        xswa__hvuyk, name='info_to_numpy_array')
    builder.call(vyhbj__gvcs, [in_info, vjcx__qbdpl, lduas__ntc, tcv__rrfs])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    rwzz__gchqt = context.get_value_type(types.intp)
    thvzv__ouu = cgutils.pack_array(builder, [builder.load(vjcx__qbdpl)],
        ty=rwzz__gchqt)
    iwqwc__cehm = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    nmwf__pso = cgutils.pack_array(builder, [iwqwc__cehm], ty=rwzz__gchqt)
    xvg__wlr = builder.bitcast(builder.load(lduas__ntc), context.
        get_data_type(arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=xvg__wlr, shape=thvzv__ouu,
        strides=nmwf__pso, itemsize=iwqwc__cehm, meminfo=builder.load(
        tcv__rrfs))
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    fcqn__ybvq = context.make_helper(builder, arr_type)
    xswa__hvuyk = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
        xswa__hvuyk, name='info_to_list_string_array')
    builder.call(vyhbj__gvcs, [in_info, fcqn__ybvq._get_ptr_by_name('meminfo')]
        )
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return fcqn__ybvq._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    gcf__xqpa = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        zuqi__qias = lengths_pos
        korn__lyx = infos_pos
        ncux__puih, lengths_pos, infos_pos = nested_to_array(context,
            builder, arr_typ.dtype, lengths_ptr, array_infos_ptr, 
            lengths_pos + 1, infos_pos + 2)
        apbtv__rvjx = ArrayItemArrayPayloadType(arr_typ)
        fdsg__ixnd = context.get_data_type(apbtv__rvjx)
        nhsll__fmyp = context.get_abi_sizeof(fdsg__ixnd)
        ctr__kfdkh = define_array_item_dtor(context, builder, arr_typ,
            apbtv__rvjx)
        qibm__jbkt = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, nhsll__fmyp), ctr__kfdkh)
        xnr__rhs = context.nrt.meminfo_data(builder, qibm__jbkt)
        bponk__vkd = builder.bitcast(xnr__rhs, fdsg__ixnd.as_pointer())
        ymu__sfmhy = cgutils.create_struct_proxy(apbtv__rvjx)(context, builder)
        ymu__sfmhy.n_arrays = builder.extract_value(builder.load(
            lengths_ptr), zuqi__qias)
        ymu__sfmhy.data = ncux__puih
        lxjjk__qgqs = builder.load(array_infos_ptr)
        rrn__urqz = builder.bitcast(builder.extract_value(lxjjk__qgqs,
            korn__lyx), gcf__xqpa)
        ymu__sfmhy.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, rrn__urqz)
        nmii__ngcs = builder.bitcast(builder.extract_value(lxjjk__qgqs, 
            korn__lyx + 1), gcf__xqpa)
        ymu__sfmhy.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, nmii__ngcs)
        builder.store(ymu__sfmhy._getvalue(), bponk__vkd)
        cleix__xwjlj = context.make_helper(builder, arr_typ)
        cleix__xwjlj.meminfo = qibm__jbkt
        return cleix__xwjlj._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        ebk__oivks = []
        korn__lyx = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for ftmw__zkd in arr_typ.data:
            ncux__puih, lengths_pos, infos_pos = nested_to_array(context,
                builder, ftmw__zkd, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            ebk__oivks.append(ncux__puih)
        apbtv__rvjx = StructArrayPayloadType(arr_typ.data)
        fdsg__ixnd = context.get_value_type(apbtv__rvjx)
        nhsll__fmyp = context.get_abi_sizeof(fdsg__ixnd)
        ctr__kfdkh = define_struct_arr_dtor(context, builder, arr_typ,
            apbtv__rvjx)
        qibm__jbkt = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, nhsll__fmyp), ctr__kfdkh)
        xnr__rhs = context.nrt.meminfo_data(builder, qibm__jbkt)
        bponk__vkd = builder.bitcast(xnr__rhs, fdsg__ixnd.as_pointer())
        ymu__sfmhy = cgutils.create_struct_proxy(apbtv__rvjx)(context, builder)
        ymu__sfmhy.data = cgutils.pack_array(builder, ebk__oivks
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, ebk__oivks)
        lxjjk__qgqs = builder.load(array_infos_ptr)
        nmii__ngcs = builder.bitcast(builder.extract_value(lxjjk__qgqs,
            korn__lyx), gcf__xqpa)
        ymu__sfmhy.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, nmii__ngcs)
        builder.store(ymu__sfmhy._getvalue(), bponk__vkd)
        adytn__mrar = context.make_helper(builder, arr_typ)
        adytn__mrar.meminfo = qibm__jbkt
        return adytn__mrar._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        lxjjk__qgqs = builder.load(array_infos_ptr)
        zwgj__gowix = builder.bitcast(builder.extract_value(lxjjk__qgqs,
            infos_pos), gcf__xqpa)
        vyzsa__yguhe = context.make_helper(builder, arr_typ)
        ufdo__ucsk = ArrayItemArrayType(char_arr_type)
        cleix__xwjlj = context.make_helper(builder, ufdo__ucsk)
        xswa__hvuyk = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='info_to_string_array')
        builder.call(vyhbj__gvcs, [zwgj__gowix, cleix__xwjlj.
            _get_ptr_by_name('meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        vyzsa__yguhe.data = cleix__xwjlj._getvalue()
        return vyzsa__yguhe._getvalue(), lengths_pos + 1, infos_pos + 1
    elif isinstance(arr_typ, types.Array):
        lxjjk__qgqs = builder.load(array_infos_ptr)
        ptbu__wkz = builder.bitcast(builder.extract_value(lxjjk__qgqs, 
            infos_pos + 1), gcf__xqpa)
        return _lower_info_to_array_numpy(arr_typ, context, builder, ptbu__wkz
            ), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
        ) or arr_typ in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        nan__yts = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            nan__yts = int128_type
        elif arr_typ == datetime_date_array_type:
            nan__yts = types.int64
        lxjjk__qgqs = builder.load(array_infos_ptr)
        nmii__ngcs = builder.bitcast(builder.extract_value(lxjjk__qgqs,
            infos_pos), gcf__xqpa)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, nmii__ngcs)
        ptbu__wkz = builder.bitcast(builder.extract_value(lxjjk__qgqs, 
            infos_pos + 1), gcf__xqpa)
        arr.data = _lower_info_to_array_numpy(types.Array(nan__yts, 1, 'C'),
            context, builder, ptbu__wkz)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


def info_to_array_codegen(context, builder, sig, args):
    array_type = sig.args[1]
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    in_info, ccqdu__afhob = args
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
                return 1 + sum([get_num_arrays(ftmw__zkd) for ftmw__zkd in
                    arr_typ.data])
            else:
                return 1

        def get_num_infos(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 2 + get_num_infos(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_infos(ftmw__zkd) for ftmw__zkd in
                    arr_typ.data])
            elif arr_typ in (string_array_type, binary_array_type):
                return 1
            else:
                return 2
        if isinstance(arr_type, TupleArrayType):
            huf__fik = StructArrayType(arr_type.data, ('dummy',) * len(
                arr_type.data))
        elif isinstance(arr_type, MapArrayType):
            huf__fik = _get_map_arr_data_type(arr_type)
        else:
            huf__fik = arr_type
        yrcw__rmcxa = get_num_arrays(huf__fik)
        epgxe__qtywp = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), 0) for ccqdu__afhob in range(yrcw__rmcxa)])
        lengths_ptr = cgutils.alloca_once_value(builder, epgxe__qtywp)
        zrtrl__ujsft = lir.Constant(lir.IntType(8).as_pointer(), None)
        cughm__qijb = cgutils.pack_array(builder, [zrtrl__ujsft for
            ccqdu__afhob in range(get_num_infos(huf__fik))])
        array_infos_ptr = cgutils.alloca_once_value(builder, cughm__qijb)
        xswa__hvuyk = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer()])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='info_to_nested_array')
        builder.call(vyhbj__gvcs, [in_info, builder.bitcast(lengths_ptr,
            lir.IntType(64).as_pointer()), builder.bitcast(array_infos_ptr,
            lir.IntType(8).as_pointer().as_pointer())])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        arr, ccqdu__afhob, ccqdu__afhob = nested_to_array(context, builder,
            huf__fik, lengths_ptr, array_infos_ptr, 0, 0)
        if isinstance(arr_type, TupleArrayType):
            ouo__deda = context.make_helper(builder, arr_type)
            ouo__deda.data = arr
            context.nrt.incref(builder, huf__fik, arr)
            arr = ouo__deda._getvalue()
        elif isinstance(arr_type, MapArrayType):
            sig = signature(arr_type, huf__fik)
            arr = init_map_arr_codegen(context, builder, sig, (arr,))
        return arr
    if arr_type in (string_array_type, binary_array_type):
        vyzsa__yguhe = context.make_helper(builder, arr_type)
        ufdo__ucsk = ArrayItemArrayType(char_arr_type)
        cleix__xwjlj = context.make_helper(builder, ufdo__ucsk)
        xswa__hvuyk = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='info_to_string_array')
        builder.call(vyhbj__gvcs, [in_info, cleix__xwjlj._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        vyzsa__yguhe.data = cleix__xwjlj._getvalue()
        return vyzsa__yguhe._getvalue()
    if arr_type == bodo.dict_str_arr_type:
        xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='get_nested_info')
        nobr__akwx = builder.call(vyhbj__gvcs, [in_info, lir.Constant(lir.
            IntType(32), 1)])
        jop__xphg = builder.call(vyhbj__gvcs, [in_info, lir.Constant(lir.
            IntType(32), 2)])
        heew__qpj = context.make_helper(builder, arr_type)
        sig = arr_type.data(array_info_type, arr_type.data)
        heew__qpj.data = info_to_array_codegen(context, builder, sig, (
            nobr__akwx, context.get_constant_null(arr_type.data)))
        amoxf__kcrqa = bodo.libs.dict_arr_ext.dict_indices_arr_type
        sig = amoxf__kcrqa(array_info_type, amoxf__kcrqa)
        heew__qpj.indices = info_to_array_codegen(context, builder, sig, (
            jop__xphg, context.get_constant_null(amoxf__kcrqa)))
        xswa__hvuyk = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer()])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='get_has_global_dictionary')
        gbdmy__mjzly = builder.call(vyhbj__gvcs, [in_info])
        heew__qpj.has_global_dictionary = builder.trunc(gbdmy__mjzly,
            cgutils.bool_t)
        return heew__qpj._getvalue()
    if isinstance(arr_type, CategoricalArrayType):
        out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        scjrn__rjjk = get_categories_int_type(arr_type.dtype)
        tlqdn__evw = types.Array(scjrn__rjjk, 1, 'C')
        out_arr.codes = _lower_info_to_array_numpy(tlqdn__evw, context,
            builder, in_info)
        if isinstance(array_type, types.TypeRef):
            assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
            is_ordered = arr_type.dtype.ordered
            bsytz__ppsp = bodo.utils.utils.create_categorical_type(arr_type
                .dtype.categories, arr_type.dtype.data.data, is_ordered)
            new_cats_tup = MetaType(tuple(bsytz__ppsp))
            int_type = arr_type.dtype.int_type
            zmcn__xea = arr_type.dtype.data.data
            awqy__ozd = context.get_constant_generic(builder, zmcn__xea,
                bsytz__ppsp)
            bkvt__obna = context.compile_internal(builder, lambda c_arr:
                bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo.utils.
                conversion.index_from_array(c_arr), is_ordered, int_type,
                new_cats_tup), arr_type.dtype(zmcn__xea), [awqy__ozd])
        else:
            bkvt__obna = cgutils.create_struct_proxy(arr_type)(context,
                builder, args[1]).dtype
            context.nrt.incref(builder, arr_type.dtype, bkvt__obna)
        out_arr.dtype = bkvt__obna
        return out_arr._getvalue()
    if isinstance(arr_type, bodo.DatetimeArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        xvg__wlr = _lower_info_to_array_numpy(arr_type.data_array_type,
            context, builder, in_info)
        arr.data = xvg__wlr
        return arr._getvalue()
    if isinstance(arr_type, types.Array):
        return _lower_info_to_array_numpy(arr_type, context, builder, in_info)
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType, TimeArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        nan__yts = arr_type.dtype
        if isinstance(arr_type, DecimalArrayType):
            nan__yts = int128_type
        elif arr_type == datetime_date_array_type:
            nan__yts = types.int64
        brtkc__pfa = types.Array(nan__yts, 1, 'C')
        ijop__hcpa = context.make_array(brtkc__pfa)(context, builder)
        frz__emu = types.Array(types.uint8, 1, 'C')
        rftzj__afap = context.make_array(frz__emu)(context, builder)
        vjcx__qbdpl = cgutils.alloca_once(builder, lir.IntType(64))
        rwoun__yssjp = cgutils.alloca_once(builder, lir.IntType(64))
        lduas__ntc = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        qasr__dbtk = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        tcv__rrfs = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        axf__cdqy = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        xswa__hvuyk = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer(), lir.IntType(8).as_pointer
            ().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='info_to_nullable_array')
        builder.call(vyhbj__gvcs, [in_info, vjcx__qbdpl, rwoun__yssjp,
            lduas__ntc, qasr__dbtk, tcv__rrfs, axf__cdqy])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        rwzz__gchqt = context.get_value_type(types.intp)
        thvzv__ouu = cgutils.pack_array(builder, [builder.load(vjcx__qbdpl)
            ], ty=rwzz__gchqt)
        iwqwc__cehm = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(nan__yts)))
        nmwf__pso = cgutils.pack_array(builder, [iwqwc__cehm], ty=rwzz__gchqt)
        xvg__wlr = builder.bitcast(builder.load(lduas__ntc), context.
            get_data_type(nan__yts).as_pointer())
        numba.np.arrayobj.populate_array(ijop__hcpa, data=xvg__wlr, shape=
            thvzv__ouu, strides=nmwf__pso, itemsize=iwqwc__cehm, meminfo=
            builder.load(tcv__rrfs))
        arr.data = ijop__hcpa._getvalue()
        thvzv__ouu = cgutils.pack_array(builder, [builder.load(rwoun__yssjp
            )], ty=rwzz__gchqt)
        iwqwc__cehm = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(types.uint8)))
        nmwf__pso = cgutils.pack_array(builder, [iwqwc__cehm], ty=rwzz__gchqt)
        xvg__wlr = builder.bitcast(builder.load(qasr__dbtk), context.
            get_data_type(types.uint8).as_pointer())
        numba.np.arrayobj.populate_array(rftzj__afap, data=xvg__wlr, shape=
            thvzv__ouu, strides=nmwf__pso, itemsize=iwqwc__cehm, meminfo=
            builder.load(axf__cdqy))
        arr.null_bitmap = rftzj__afap._getvalue()
        return arr._getvalue()
    if isinstance(arr_type, IntervalArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        equr__sgsr = context.make_array(arr_type.arr_type)(context, builder)
        gqpmw__dwh = context.make_array(arr_type.arr_type)(context, builder)
        vjcx__qbdpl = cgutils.alloca_once(builder, lir.IntType(64))
        etja__aanm = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        abxb__kuih = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        ehwka__fsk = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        qyp__kpfml = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        xswa__hvuyk = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer()])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='info_to_interval_array')
        builder.call(vyhbj__gvcs, [in_info, vjcx__qbdpl, etja__aanm,
            abxb__kuih, ehwka__fsk, qyp__kpfml])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        rwzz__gchqt = context.get_value_type(types.intp)
        thvzv__ouu = cgutils.pack_array(builder, [builder.load(vjcx__qbdpl)
            ], ty=rwzz__gchqt)
        iwqwc__cehm = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(arr_type.arr_type.dtype)))
        nmwf__pso = cgutils.pack_array(builder, [iwqwc__cehm], ty=rwzz__gchqt)
        hho__kwq = builder.bitcast(builder.load(etja__aanm), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(equr__sgsr, data=hho__kwq, shape=
            thvzv__ouu, strides=nmwf__pso, itemsize=iwqwc__cehm, meminfo=
            builder.load(ehwka__fsk))
        arr.left = equr__sgsr._getvalue()
        jokvu__hyd = builder.bitcast(builder.load(abxb__kuih), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(gqpmw__dwh, data=jokvu__hyd, shape
            =thvzv__ouu, strides=nmwf__pso, itemsize=iwqwc__cehm, meminfo=
            builder.load(qyp__kpfml))
        arr.right = gqpmw__dwh._getvalue()
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
        bbcc__jivp, ccqdu__afhob = args
        efksi__giy = numba_to_c_type(array_type.dtype)
        dyotd__qbb = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), efksi__giy))
        xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='alloc_numpy')
        return builder.call(vyhbj__gvcs, [bbcc__jivp, builder.load(dyotd__qbb)]
            )
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        bbcc__jivp, ojt__hoft = args
        xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='alloc_string_array')
        return builder.call(vyhbj__gvcs, [bbcc__jivp, ojt__hoft])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)
    return table_type(list_arr_info_typ), arr_info_list_to_table_codegen


def arr_info_list_to_table_codegen(context, builder, sig, args):
    krr__gyxma, = args
    xihx__dczx = numba.cpython.listobj.ListInstance(context, builder, sig.
        args[0], krr__gyxma)
    xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer().as_pointer(), lir.IntType(64)])
    vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
        xswa__hvuyk, name='arr_info_list_to_table')
    return builder.call(vyhbj__gvcs, [xihx__dczx.data, xihx__dczx.size])


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='info_from_table')
        return builder.call(vyhbj__gvcs, args)
    return array_info_type(table_t, ind_t), codegen


@intrinsic
def cpp_table_to_py_table(typingctx, cpp_table_t, table_idx_arr_t,
    py_table_type_t):
    assert cpp_table_t == table_type, 'invalid cpp table type'
    assert isinstance(table_idx_arr_t, types.Array
        ) and table_idx_arr_t.dtype == types.int64, 'invalid table index array'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    zrnp__craq = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        cpp_table, dnkaj__mrj, ccqdu__afhob = args
        xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='info_from_table')
        kxxhs__qnwcs = cgutils.create_struct_proxy(zrnp__craq)(context, builder
            )
        kxxhs__qnwcs.parent = cgutils.get_null_value(kxxhs__qnwcs.parent.type)
        ebncy__hfqmf = context.make_array(table_idx_arr_t)(context, builder,
            dnkaj__mrj)
        pyp__vmcrn = context.get_constant(types.int64, -1)
        lqks__eifg = context.get_constant(types.int64, 0)
        rtm__nom = cgutils.alloca_once_value(builder, lqks__eifg)
        for t, cyxuw__usgko in zrnp__craq.type_to_blk.items():
            wix__wjobg = context.get_constant(types.int64, len(zrnp__craq.
                block_to_arr_ind[cyxuw__usgko]))
            ccqdu__afhob, bcyur__yrpb = ListInstance.allocate_ex(context,
                builder, types.List(t), wix__wjobg)
            bcyur__yrpb.size = wix__wjobg
            keg__mbj = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(zrnp__craq.block_to_arr_ind[
                cyxuw__usgko], dtype=np.int64))
            nniin__creiq = context.make_array(types.Array(types.int64, 1, 'C')
                )(context, builder, keg__mbj)
            with cgutils.for_range(builder, wix__wjobg) as gicj__hwnm:
                ysvp__uwowf = gicj__hwnm.index
                pjm__eas = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    nniin__creiq, ysvp__uwowf)
                xkcwr__meri = _getitem_array_single_int(context, builder,
                    types.int64, table_idx_arr_t, ebncy__hfqmf, pjm__eas)
                ystjn__dqdew = builder.icmp_unsigned('!=', xkcwr__meri,
                    pyp__vmcrn)
                with builder.if_else(ystjn__dqdew) as (iewbs__krnsl,
                    jtnfo__czxv):
                    with iewbs__krnsl:
                        dteu__iytef = builder.call(vyhbj__gvcs, [cpp_table,
                            xkcwr__meri])
                        arr = context.compile_internal(builder, lambda info:
                            info_to_array(info, t), t(array_info_type), [
                            dteu__iytef])
                        bcyur__yrpb.inititem(ysvp__uwowf, arr, incref=False)
                        bbcc__jivp = context.compile_internal(builder, lambda
                            arr: len(arr), types.int64(t), [arr])
                        builder.store(bbcc__jivp, rtm__nom)
                    with jtnfo__czxv:
                        ugsrr__axa = context.get_constant_null(t)
                        bcyur__yrpb.inititem(ysvp__uwowf, ugsrr__axa,
                            incref=False)
            setattr(kxxhs__qnwcs, f'block_{cyxuw__usgko}', bcyur__yrpb.value)
        kxxhs__qnwcs.len = builder.load(rtm__nom)
        return kxxhs__qnwcs._getvalue()
    return zrnp__craq(cpp_table_t, table_idx_arr_t, py_table_type_t), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def cpp_table_to_py_data(cpp_table, out_col_inds_t, out_types_t, n_rows_t,
    n_table_cols_t, unknown_cat_arrs_t=None, cat_inds_t=None):
    itwgu__pwipe = out_col_inds_t.instance_type.meta
    zrnp__craq = unwrap_typeref(out_types_t.types[0])
    qyid__hpwu = [unwrap_typeref(out_types_t.types[ysvp__uwowf]) for
        ysvp__uwowf in range(1, len(out_types_t.types))]
    omikw__folnj = {}
    rdyw__bwqw = get_overload_const_int(n_table_cols_t)
    gstj__pdgb = {qiwi__tob: ysvp__uwowf for ysvp__uwowf, qiwi__tob in
        enumerate(itwgu__pwipe)}
    if not is_overload_none(unknown_cat_arrs_t):
        dzz__xer = {feu__fyr: ysvp__uwowf for ysvp__uwowf, feu__fyr in
            enumerate(cat_inds_t.instance_type.meta)}
    dtx__evt = []
    pbap__wyb = """def impl(cpp_table, out_col_inds_t, out_types_t, n_rows_t, n_table_cols_t, unknown_cat_arrs_t=None, cat_inds_t=None):
"""
    if isinstance(zrnp__craq, bodo.TableType):
        pbap__wyb += f'  py_table = init_table(py_table_type, False)\n'
        pbap__wyb += f'  py_table = set_table_len(py_table, n_rows_t)\n'
        for wjua__yia, cyxuw__usgko in zrnp__craq.type_to_blk.items():
            slikq__tyllo = [gstj__pdgb.get(ysvp__uwowf, -1) for ysvp__uwowf in
                zrnp__craq.block_to_arr_ind[cyxuw__usgko]]
            omikw__folnj[f'out_inds_{cyxuw__usgko}'] = np.array(slikq__tyllo,
                np.int64)
            omikw__folnj[f'out_type_{cyxuw__usgko}'] = wjua__yia
            omikw__folnj[f'typ_list_{cyxuw__usgko}'] = types.List(wjua__yia)
            bmq__tbym = f'out_type_{cyxuw__usgko}'
            if type_has_unknown_cats(wjua__yia):
                if is_overload_none(unknown_cat_arrs_t):
                    pbap__wyb += f"""  in_arr_list_{cyxuw__usgko} = get_table_block(out_types_t[0], {cyxuw__usgko})
"""
                    bmq__tbym = f'in_arr_list_{cyxuw__usgko}[i]'
                else:
                    omikw__folnj[f'cat_arr_inds_{cyxuw__usgko}'] = np.array([
                        dzz__xer.get(ysvp__uwowf, -1) for ysvp__uwowf in
                        zrnp__craq.block_to_arr_ind[cyxuw__usgko]], np.int64)
                    bmq__tbym = (
                        f'unknown_cat_arrs_t[cat_arr_inds_{cyxuw__usgko}[i]]')
            wix__wjobg = len(zrnp__craq.block_to_arr_ind[cyxuw__usgko])
            pbap__wyb += f"""  arr_list_{cyxuw__usgko} = alloc_list_like(typ_list_{cyxuw__usgko}, {wix__wjobg}, False)
"""
            pbap__wyb += f'  for i in range(len(arr_list_{cyxuw__usgko})):\n'
            pbap__wyb += (
                f'    cpp_ind_{cyxuw__usgko} = out_inds_{cyxuw__usgko}[i]\n')
            pbap__wyb += f'    if cpp_ind_{cyxuw__usgko} == -1:\n'
            pbap__wyb += f'      continue\n'
            pbap__wyb += f"""    arr_{cyxuw__usgko} = info_to_array(info_from_table(cpp_table, cpp_ind_{cyxuw__usgko}), {bmq__tbym})
"""
            pbap__wyb += (
                f'    arr_list_{cyxuw__usgko}[i] = arr_{cyxuw__usgko}\n')
            pbap__wyb += f"""  py_table = set_table_block(py_table, arr_list_{cyxuw__usgko}, {cyxuw__usgko})
"""
        dtx__evt.append('py_table')
    elif zrnp__craq != types.none:
        pkqwr__cuzg = gstj__pdgb.get(0, -1)
        if pkqwr__cuzg != -1:
            omikw__folnj[f'arr_typ_arg0'] = zrnp__craq
            bmq__tbym = f'arr_typ_arg0'
            if type_has_unknown_cats(zrnp__craq):
                if is_overload_none(unknown_cat_arrs_t):
                    bmq__tbym = f'out_types_t[0]'
                else:
                    bmq__tbym = f'unknown_cat_arrs_t[{dzz__xer[0]}]'
            pbap__wyb += f"""  out_arg0 = info_to_array(info_from_table(cpp_table, {pkqwr__cuzg}), {bmq__tbym})
"""
            dtx__evt.append('out_arg0')
    for ysvp__uwowf, t in enumerate(qyid__hpwu):
        pkqwr__cuzg = gstj__pdgb.get(rdyw__bwqw + ysvp__uwowf, -1)
        if pkqwr__cuzg != -1:
            omikw__folnj[f'extra_arr_type_{ysvp__uwowf}'] = t
            bmq__tbym = f'extra_arr_type_{ysvp__uwowf}'
            if type_has_unknown_cats(t):
                if is_overload_none(unknown_cat_arrs_t):
                    bmq__tbym = f'out_types_t[{ysvp__uwowf + 1}]'
                else:
                    bmq__tbym = (
                        f'unknown_cat_arrs_t[{dzz__xer[rdyw__bwqw + ysvp__uwowf]}]'
                        )
            pbap__wyb += f"""  out_{ysvp__uwowf} = info_to_array(info_from_table(cpp_table, {pkqwr__cuzg}), {bmq__tbym})
"""
            dtx__evt.append(f'out_{ysvp__uwowf}')
    gdsvy__cfbkr = ',' if len(dtx__evt) == 1 else ''
    pbap__wyb += f"  return ({', '.join(dtx__evt)}{gdsvy__cfbkr})\n"
    omikw__folnj.update({'init_table': bodo.hiframes.table.init_table,
        'alloc_list_like': bodo.hiframes.table.alloc_list_like,
        'set_table_block': bodo.hiframes.table.set_table_block,
        'set_table_len': bodo.hiframes.table.set_table_len,
        'get_table_block': bodo.hiframes.table.get_table_block,
        'info_to_array': info_to_array, 'info_from_table': info_from_table,
        'out_col_inds': list(itwgu__pwipe), 'py_table_type': zrnp__craq})
    nzwts__ehul = {}
    exec(pbap__wyb, omikw__folnj, nzwts__ehul)
    return nzwts__ehul['impl']


@intrinsic
def py_table_to_cpp_table(typingctx, py_table_t, py_table_type_t):
    assert isinstance(py_table_t, bodo.hiframes.table.TableType
        ), 'invalid py table type'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    zrnp__craq = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        py_table, ccqdu__afhob = args
        qzfw__poa = cgutils.create_struct_proxy(zrnp__craq)(context,
            builder, py_table)
        if zrnp__craq.has_runtime_cols:
            sxuco__lmsm = lir.Constant(lir.IntType(64), 0)
            for cyxuw__usgko, t in enumerate(zrnp__craq.arr_types):
                ywavv__lkm = getattr(qzfw__poa, f'block_{cyxuw__usgko}')
                ozdh__zfcrr = ListInstance(context, builder, types.List(t),
                    ywavv__lkm)
                sxuco__lmsm = builder.add(sxuco__lmsm, ozdh__zfcrr.size)
        else:
            sxuco__lmsm = lir.Constant(lir.IntType(64), len(zrnp__craq.
                arr_types))
        ccqdu__afhob, ywj__olvae = ListInstance.allocate_ex(context,
            builder, types.List(array_info_type), sxuco__lmsm)
        ywj__olvae.size = sxuco__lmsm
        if zrnp__craq.has_runtime_cols:
            gyzx__dtab = lir.Constant(lir.IntType(64), 0)
            for cyxuw__usgko, t in enumerate(zrnp__craq.arr_types):
                ywavv__lkm = getattr(qzfw__poa, f'block_{cyxuw__usgko}')
                ozdh__zfcrr = ListInstance(context, builder, types.List(t),
                    ywavv__lkm)
                wix__wjobg = ozdh__zfcrr.size
                with cgutils.for_range(builder, wix__wjobg) as gicj__hwnm:
                    ysvp__uwowf = gicj__hwnm.index
                    arr = ozdh__zfcrr.getitem(ysvp__uwowf)
                    phpt__osw = signature(array_info_type, t)
                    vpclw__ebkzd = arr,
                    dcjw__pim = array_to_info_codegen(context, builder,
                        phpt__osw, vpclw__ebkzd)
                    ywj__olvae.inititem(builder.add(gyzx__dtab, ysvp__uwowf
                        ), dcjw__pim, incref=False)
                gyzx__dtab = builder.add(gyzx__dtab, wix__wjobg)
        else:
            for t, cyxuw__usgko in zrnp__craq.type_to_blk.items():
                wix__wjobg = context.get_constant(types.int64, len(
                    zrnp__craq.block_to_arr_ind[cyxuw__usgko]))
                ywavv__lkm = getattr(qzfw__poa, f'block_{cyxuw__usgko}')
                ozdh__zfcrr = ListInstance(context, builder, types.List(t),
                    ywavv__lkm)
                keg__mbj = context.make_constant_array(builder, types.Array
                    (types.int64, 1, 'C'), np.array(zrnp__craq.
                    block_to_arr_ind[cyxuw__usgko], dtype=np.int64))
                nniin__creiq = context.make_array(types.Array(types.int64, 
                    1, 'C'))(context, builder, keg__mbj)
                with cgutils.for_range(builder, wix__wjobg) as gicj__hwnm:
                    ysvp__uwowf = gicj__hwnm.index
                    pjm__eas = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        nniin__creiq, ysvp__uwowf)
                    xsjr__qzky = signature(types.none, zrnp__craq, types.
                        List(t), types.int64, types.int64)
                    wwbg__mzblf = py_table, ywavv__lkm, ysvp__uwowf, pjm__eas
                    bodo.hiframes.table.ensure_column_unboxed_codegen(context,
                        builder, xsjr__qzky, wwbg__mzblf)
                    arr = ozdh__zfcrr.getitem(ysvp__uwowf)
                    phpt__osw = signature(array_info_type, t)
                    vpclw__ebkzd = arr,
                    dcjw__pim = array_to_info_codegen(context, builder,
                        phpt__osw, vpclw__ebkzd)
                    ywj__olvae.inititem(pjm__eas, dcjw__pim, incref=False)
        mca__ljj = ywj__olvae.value
        kubt__mjim = signature(table_type, types.List(array_info_type))
        egief__qam = mca__ljj,
        cpp_table = arr_info_list_to_table_codegen(context, builder,
            kubt__mjim, egief__qam)
        context.nrt.decref(builder, types.List(array_info_type), mca__ljj)
        return cpp_table
    return table_type(zrnp__craq, py_table_type_t), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def py_data_to_cpp_table(py_table, extra_arrs_tup, in_col_inds_t,
    n_table_cols_t):
    yifek__ell = in_col_inds_t.instance_type.meta
    omikw__folnj = {}
    rdyw__bwqw = get_overload_const_int(n_table_cols_t)
    gcqns__aiq = defaultdict(list)
    gstj__pdgb = {}
    for ysvp__uwowf, qiwi__tob in enumerate(yifek__ell):
        if qiwi__tob in gstj__pdgb:
            gcqns__aiq[qiwi__tob].append(ysvp__uwowf)
        else:
            gstj__pdgb[qiwi__tob] = ysvp__uwowf
    pbap__wyb = (
        'def impl(py_table, extra_arrs_tup, in_col_inds_t, n_table_cols_t):\n')
    pbap__wyb += (
        f'  cpp_arr_list = alloc_empty_list_type({len(yifek__ell)}, array_info_type)\n'
        )
    if py_table != types.none:
        for cyxuw__usgko in py_table.type_to_blk.values():
            slikq__tyllo = [gstj__pdgb.get(ysvp__uwowf, -1) for ysvp__uwowf in
                py_table.block_to_arr_ind[cyxuw__usgko]]
            omikw__folnj[f'out_inds_{cyxuw__usgko}'] = np.array(slikq__tyllo,
                np.int64)
            omikw__folnj[f'arr_inds_{cyxuw__usgko}'] = np.array(py_table.
                block_to_arr_ind[cyxuw__usgko], np.int64)
            pbap__wyb += (
                f'  arr_list_{cyxuw__usgko} = get_table_block(py_table, {cyxuw__usgko})\n'
                )
            pbap__wyb += f'  for i in range(len(arr_list_{cyxuw__usgko})):\n'
            pbap__wyb += (
                f'    out_arr_ind_{cyxuw__usgko} = out_inds_{cyxuw__usgko}[i]\n'
                )
            pbap__wyb += f'    if out_arr_ind_{cyxuw__usgko} == -1:\n'
            pbap__wyb += f'      continue\n'
            pbap__wyb += (
                f'    arr_ind_{cyxuw__usgko} = arr_inds_{cyxuw__usgko}[i]\n')
            pbap__wyb += f"""    ensure_column_unboxed(py_table, arr_list_{cyxuw__usgko}, i, arr_ind_{cyxuw__usgko})
"""
            pbap__wyb += f"""    cpp_arr_list[out_arr_ind_{cyxuw__usgko}] = array_to_info(arr_list_{cyxuw__usgko}[i])
"""
        for vhv__ziyg, wjwyk__qspv in gcqns__aiq.items():
            if vhv__ziyg < rdyw__bwqw:
                cyxuw__usgko = py_table.block_nums[vhv__ziyg]
                sfgzi__yud = py_table.block_offsets[vhv__ziyg]
                for pkqwr__cuzg in wjwyk__qspv:
                    pbap__wyb += f"""  cpp_arr_list[{pkqwr__cuzg}] = array_to_info(arr_list_{cyxuw__usgko}[{sfgzi__yud}])
"""
    for ysvp__uwowf in range(len(extra_arrs_tup)):
        vmb__axdo = gstj__pdgb.get(rdyw__bwqw + ysvp__uwowf, -1)
        if vmb__axdo != -1:
            busnh__ldyzk = [vmb__axdo] + gcqns__aiq.get(rdyw__bwqw +
                ysvp__uwowf, [])
            for pkqwr__cuzg in busnh__ldyzk:
                pbap__wyb += f"""  cpp_arr_list[{pkqwr__cuzg}] = array_to_info(extra_arrs_tup[{ysvp__uwowf}])
"""
    pbap__wyb += f'  return arr_info_list_to_table(cpp_arr_list)\n'
    omikw__folnj.update({'array_info_type': array_info_type,
        'alloc_empty_list_type': bodo.hiframes.table.alloc_empty_list_type,
        'get_table_block': bodo.hiframes.table.get_table_block,
        'ensure_column_unboxed': bodo.hiframes.table.ensure_column_unboxed,
        'array_to_info': array_to_info, 'arr_info_list_to_table':
        arr_info_list_to_table})
    nzwts__ehul = {}
    exec(pbap__wyb, omikw__folnj, nzwts__ehul)
    return nzwts__ehul['impl']


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
        xswa__hvuyk = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='delete_table')
        builder.call(vyhbj__gvcs, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='shuffle_table')
        kkwfx__twlh = builder.call(vyhbj__gvcs, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return kkwfx__twlh
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
        xswa__hvuyk = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='delete_shuffle_info')
        return builder.call(vyhbj__gvcs, args)
    return types.void(shuffle_info_t), codegen


@intrinsic
def reverse_shuffle_table(typingctx, table_t, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[-1] == types.none:
            return context.get_constant_null(table_type)
        xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='reverse_shuffle_table')
        return builder.call(vyhbj__gvcs, args)
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
        xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(1), lir
            .IntType(1), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(64), lir.IntType(8).as_pointer()])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='hash_join_table')
        kkwfx__twlh = builder.call(vyhbj__gvcs, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return kkwfx__twlh
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
        xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='sort_values_table')
        kkwfx__twlh = builder.call(vyhbj__gvcs, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return kkwfx__twlh
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='sample_table')
        kkwfx__twlh = builder.call(vyhbj__gvcs, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return kkwfx__twlh
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='shuffle_renormalization')
        kkwfx__twlh = builder.call(vyhbj__gvcs, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return kkwfx__twlh
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='shuffle_renormalization_group')
        kkwfx__twlh = builder.call(vyhbj__gvcs, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return kkwfx__twlh
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    dropna, drop_local_first):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(1), lir.IntType(1)])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='drop_duplicates_table')
        kkwfx__twlh = builder.call(vyhbj__gvcs, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return kkwfx__twlh
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
        xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(64), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        vyhbj__gvcs = cgutils.get_or_insert_function(builder.module,
            xswa__hvuyk, name='groupby_and_aggregate')
        kkwfx__twlh = builder.call(vyhbj__gvcs, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return kkwfx__twlh
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
    yjbr__vym = array_to_info(dict_arr)
    _convert_local_dictionary_to_global(yjbr__vym, sort_dictionary)
    check_and_propagate_cpp_exception()
    out_arr = info_to_array(yjbr__vym, bodo.dict_str_arr_type)
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
    moszf__vjh = array_to_info(in_arr)
    trtd__fmqoi = array_to_info(in_values)
    iqg__yrnlc = array_to_info(out_arr)
    jcd__ktax = arr_info_list_to_table([moszf__vjh, trtd__fmqoi, iqg__yrnlc])
    _array_isin(iqg__yrnlc, moszf__vjh, trtd__fmqoi, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(jcd__ktax)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.bool_, types.voidptr, array_info_type))


@numba.njit(no_cpython_wrapper=True)
def get_search_regex(in_arr, case, match, pat, out_arr):
    moszf__vjh = array_to_info(in_arr)
    iqg__yrnlc = array_to_info(out_arr)
    _get_search_regex(moszf__vjh, case, match, pat, iqg__yrnlc)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_array_typ, c_ind):
    from llvmlite import ir as lir
    nfr__qab = col_array_typ.dtype
    if isinstance(nfr__qab, (types.Number, TimeType)) or nfr__qab in [bodo.
        datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                kxxhs__qnwcs, chbr__kydq = args
                kxxhs__qnwcs = builder.bitcast(kxxhs__qnwcs, lir.IntType(8)
                    .as_pointer().as_pointer())
                hfsn__ueeb = lir.Constant(lir.IntType(64), c_ind)
                zepzu__ylarc = builder.load(builder.gep(kxxhs__qnwcs, [
                    hfsn__ueeb]))
                zepzu__ylarc = builder.bitcast(zepzu__ylarc, context.
                    get_data_type(nfr__qab).as_pointer())
                return builder.load(builder.gep(zepzu__ylarc, [chbr__kydq]))
            return nfr__qab(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ in (bodo.string_array_type, bodo.binary_array_type):

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                kxxhs__qnwcs, chbr__kydq = args
                kxxhs__qnwcs = builder.bitcast(kxxhs__qnwcs, lir.IntType(8)
                    .as_pointer().as_pointer())
                hfsn__ueeb = lir.Constant(lir.IntType(64), c_ind)
                zepzu__ylarc = builder.load(builder.gep(kxxhs__qnwcs, [
                    hfsn__ueeb]))
                xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                qsev__tfd = cgutils.get_or_insert_function(builder.module,
                    xswa__hvuyk, name='array_info_getitem')
                faq__flj = cgutils.alloca_once(builder, lir.IntType(64))
                args = zepzu__ylarc, chbr__kydq, faq__flj
                lduas__ntc = builder.call(qsev__tfd, args)
                return context.make_tuple(builder, sig.return_type, [
                    lduas__ntc, builder.load(faq__flj)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.libs.dict_arr_ext.dict_str_arr_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                yojbi__yfk = lir.Constant(lir.IntType(64), 1)
                kard__aui = lir.Constant(lir.IntType(64), 2)
                kxxhs__qnwcs, chbr__kydq = args
                kxxhs__qnwcs = builder.bitcast(kxxhs__qnwcs, lir.IntType(8)
                    .as_pointer().as_pointer())
                hfsn__ueeb = lir.Constant(lir.IntType(64), c_ind)
                zepzu__ylarc = builder.load(builder.gep(kxxhs__qnwcs, [
                    hfsn__ueeb]))
                xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64)])
                bis__tesx = cgutils.get_or_insert_function(builder.module,
                    xswa__hvuyk, name='get_nested_info')
                args = zepzu__ylarc, kard__aui
                eey__ecl = builder.call(bis__tesx, args)
                xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer()])
                ujt__ojt = cgutils.get_or_insert_function(builder.module,
                    xswa__hvuyk, name='array_info_getdata1')
                args = eey__ecl,
                vug__mhmpr = builder.call(ujt__ojt, args)
                vug__mhmpr = builder.bitcast(vug__mhmpr, context.
                    get_data_type(col_array_typ.indices_dtype).as_pointer())
                xdfkg__jhpme = builder.sext(builder.load(builder.gep(
                    vug__mhmpr, [chbr__kydq])), lir.IntType(64))
                args = zepzu__ylarc, yojbi__yfk
                jlejp__pkkz = builder.call(bis__tesx, args)
                xswa__hvuyk = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                qsev__tfd = cgutils.get_or_insert_function(builder.module,
                    xswa__hvuyk, name='array_info_getitem')
                faq__flj = cgutils.alloca_once(builder, lir.IntType(64))
                args = jlejp__pkkz, xdfkg__jhpme, faq__flj
                lduas__ntc = builder.call(qsev__tfd, args)
                return context.make_tuple(builder, sig.return_type, [
                    lduas__ntc, builder.load(faq__flj)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{nfr__qab}' column data type not supported"
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
                qaai__ici, chbr__kydq = args
                qaai__ici = builder.bitcast(qaai__ici, lir.IntType(8).
                    as_pointer().as_pointer())
                hfsn__ueeb = lir.Constant(lir.IntType(64), c_ind)
                zepzu__ylarc = builder.load(builder.gep(qaai__ici, [
                    hfsn__ueeb]))
                skfq__uzsuv = builder.bitcast(zepzu__ylarc, context.
                    get_data_type(types.bool_).as_pointer())
                gmezx__erwhd = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    skfq__uzsuv, chbr__kydq)
                bids__fwsit = builder.icmp_unsigned('!=', gmezx__erwhd, lir
                    .Constant(lir.IntType(8), 0))
                return builder.sext(bids__fwsit, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, types.Array):
        nfr__qab = col_array_dtype.dtype
        if nfr__qab in [bodo.datetime64ns, bodo.timedelta64ns]:

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    kxxhs__qnwcs, chbr__kydq = args
                    kxxhs__qnwcs = builder.bitcast(kxxhs__qnwcs, lir.
                        IntType(8).as_pointer().as_pointer())
                    hfsn__ueeb = lir.Constant(lir.IntType(64), c_ind)
                    zepzu__ylarc = builder.load(builder.gep(kxxhs__qnwcs, [
                        hfsn__ueeb]))
                    zepzu__ylarc = builder.bitcast(zepzu__ylarc, context.
                        get_data_type(nfr__qab).as_pointer())
                    trz__zmwcw = builder.load(builder.gep(zepzu__ylarc, [
                        chbr__kydq]))
                    bids__fwsit = builder.icmp_unsigned('!=', trz__zmwcw,
                        lir.Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(bids__fwsit, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(nfr__qab, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    kxxhs__qnwcs, chbr__kydq = args
                    kxxhs__qnwcs = builder.bitcast(kxxhs__qnwcs, lir.
                        IntType(8).as_pointer().as_pointer())
                    hfsn__ueeb = lir.Constant(lir.IntType(64), c_ind)
                    zepzu__ylarc = builder.load(builder.gep(kxxhs__qnwcs, [
                        hfsn__ueeb]))
                    zepzu__ylarc = builder.bitcast(zepzu__ylarc, context.
                        get_data_type(nfr__qab).as_pointer())
                    trz__zmwcw = builder.load(builder.gep(zepzu__ylarc, [
                        chbr__kydq]))
                    ryh__kxki = signature(types.bool_, nfr__qab)
                    gmezx__erwhd = numba.np.npyfuncs.np_real_isnan_impl(context
                        , builder, ryh__kxki, (trz__zmwcw,))
                    return builder.not_(builder.sext(gmezx__erwhd, lir.
                        IntType(8)))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
