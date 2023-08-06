"""helper functions for code generation with llvmlite
"""
import llvmlite.binding as ll
from llvmlite import ir as lir
from numba.core import cgutils, types
import bodo
from bodo.libs import array_ext, hdist
ll.add_symbol('array_getitem', array_ext.array_getitem)
ll.add_symbol('seq_getitem', array_ext.seq_getitem)
ll.add_symbol('list_check', array_ext.list_check)
ll.add_symbol('dict_keys', array_ext.dict_keys)
ll.add_symbol('dict_values', array_ext.dict_values)
ll.add_symbol('dict_merge_from_seq2', array_ext.dict_merge_from_seq2)
ll.add_symbol('is_na_value', array_ext.is_na_value)


def set_bitmap_bit(builder, null_bitmap_ptr, ind, val):
    wdmt__jurfk = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    bsb__eha = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    msn__pcbyw = builder.gep(null_bitmap_ptr, [wdmt__jurfk], inbounds=True)
    ydpf__yzdcf = builder.load(msn__pcbyw)
    vgk__fhz = lir.ArrayType(lir.IntType(8), 8)
    bqprs__aosyg = cgutils.alloca_once_value(builder, lir.Constant(vgk__fhz,
        (1, 2, 4, 8, 16, 32, 64, 128)))
    hicqf__xilmh = builder.load(builder.gep(bqprs__aosyg, [lir.Constant(lir
        .IntType(64), 0), bsb__eha], inbounds=True))
    if val:
        builder.store(builder.or_(ydpf__yzdcf, hicqf__xilmh), msn__pcbyw)
    else:
        hicqf__xilmh = builder.xor(hicqf__xilmh, lir.Constant(lir.IntType(8
            ), -1))
        builder.store(builder.and_(ydpf__yzdcf, hicqf__xilmh), msn__pcbyw)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    wdmt__jurfk = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    bsb__eha = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    ydpf__yzdcf = builder.load(builder.gep(null_bitmap_ptr, [wdmt__jurfk],
        inbounds=True))
    vgk__fhz = lir.ArrayType(lir.IntType(8), 8)
    bqprs__aosyg = cgutils.alloca_once_value(builder, lir.Constant(vgk__fhz,
        (1, 2, 4, 8, 16, 32, 64, 128)))
    hicqf__xilmh = builder.load(builder.gep(bqprs__aosyg, [lir.Constant(lir
        .IntType(64), 0), bsb__eha], inbounds=True))
    return builder.and_(ydpf__yzdcf, hicqf__xilmh)


def pyarray_check(builder, context, obj):
    vuny__onjgt = context.get_argument_type(types.pyobject)
    iebt__rvlqw = lir.FunctionType(lir.IntType(32), [vuny__onjgt])
    lsutj__kim = cgutils.get_or_insert_function(builder.module, iebt__rvlqw,
        name='is_np_array')
    return builder.call(lsutj__kim, [obj])


def pyarray_getitem(builder, context, arr_obj, ind):
    vuny__onjgt = context.get_argument_type(types.pyobject)
    xqqgg__bcoo = context.get_value_type(types.intp)
    ecx__mlfuy = lir.FunctionType(lir.IntType(8).as_pointer(), [vuny__onjgt,
        xqqgg__bcoo])
    due__lojt = cgutils.get_or_insert_function(builder.module, ecx__mlfuy,
        name='array_getptr1')
    vegao__avwe = lir.FunctionType(vuny__onjgt, [vuny__onjgt, lir.IntType(8
        ).as_pointer()])
    nglbs__xjqu = cgutils.get_or_insert_function(builder.module,
        vegao__avwe, name='array_getitem')
    akqlu__zlpf = builder.call(due__lojt, [arr_obj, ind])
    return builder.call(nglbs__xjqu, [arr_obj, akqlu__zlpf])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    vuny__onjgt = context.get_argument_type(types.pyobject)
    xqqgg__bcoo = context.get_value_type(types.intp)
    ecx__mlfuy = lir.FunctionType(lir.IntType(8).as_pointer(), [vuny__onjgt,
        xqqgg__bcoo])
    due__lojt = cgutils.get_or_insert_function(builder.module, ecx__mlfuy,
        name='array_getptr1')
    ueg__sow = lir.FunctionType(lir.VoidType(), [vuny__onjgt, lir.IntType(8
        ).as_pointer(), vuny__onjgt])
    bvnca__lcml = cgutils.get_or_insert_function(builder.module, ueg__sow,
        name='array_setitem')
    akqlu__zlpf = builder.call(due__lojt, [arr_obj, ind])
    builder.call(bvnca__lcml, [arr_obj, akqlu__zlpf, val_obj])


def seq_getitem(builder, context, obj, ind):
    vuny__onjgt = context.get_argument_type(types.pyobject)
    xqqgg__bcoo = context.get_value_type(types.intp)
    syq__xtc = lir.FunctionType(vuny__onjgt, [vuny__onjgt, xqqgg__bcoo])
    lpgtx__juvt = cgutils.get_or_insert_function(builder.module, syq__xtc,
        name='seq_getitem')
    return builder.call(lpgtx__juvt, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    vuny__onjgt = context.get_argument_type(types.pyobject)
    eqb__ziiv = lir.FunctionType(lir.IntType(32), [vuny__onjgt, vuny__onjgt])
    xcg__zoks = cgutils.get_or_insert_function(builder.module, eqb__ziiv,
        name='is_na_value')
    return builder.call(xcg__zoks, [val, C_NA])


def list_check(builder, context, obj):
    vuny__onjgt = context.get_argument_type(types.pyobject)
    sqoxm__lsqx = context.get_value_type(types.int32)
    vfiwu__mmnww = lir.FunctionType(sqoxm__lsqx, [vuny__onjgt])
    fafwv__tjy = cgutils.get_or_insert_function(builder.module,
        vfiwu__mmnww, name='list_check')
    return builder.call(fafwv__tjy, [obj])


def dict_keys(builder, context, obj):
    vuny__onjgt = context.get_argument_type(types.pyobject)
    vfiwu__mmnww = lir.FunctionType(vuny__onjgt, [vuny__onjgt])
    fafwv__tjy = cgutils.get_or_insert_function(builder.module,
        vfiwu__mmnww, name='dict_keys')
    return builder.call(fafwv__tjy, [obj])


def dict_values(builder, context, obj):
    vuny__onjgt = context.get_argument_type(types.pyobject)
    vfiwu__mmnww = lir.FunctionType(vuny__onjgt, [vuny__onjgt])
    fafwv__tjy = cgutils.get_or_insert_function(builder.module,
        vfiwu__mmnww, name='dict_values')
    return builder.call(fafwv__tjy, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    vuny__onjgt = context.get_argument_type(types.pyobject)
    vfiwu__mmnww = lir.FunctionType(lir.VoidType(), [vuny__onjgt, vuny__onjgt])
    fafwv__tjy = cgutils.get_or_insert_function(builder.module,
        vfiwu__mmnww, name='dict_merge_from_seq2')
    builder.call(fafwv__tjy, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    gwajb__gcza = cgutils.alloca_once_value(builder, val)
    sjp__xlk = list_check(builder, context, val)
    vbvxa__rlq = builder.icmp_unsigned('!=', sjp__xlk, lir.Constant(
        sjp__xlk.type, 0))
    with builder.if_then(vbvxa__rlq):
        vnuy__fwlg = context.insert_const_string(builder.module, 'numpy')
        ywkfz__rwplc = c.pyapi.import_module_noblock(vnuy__fwlg)
        foxcx__aku = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            foxcx__aku = str(typ.dtype)
        zxv__zcgyy = c.pyapi.object_getattr_string(ywkfz__rwplc, foxcx__aku)
        kto__tut = builder.load(gwajb__gcza)
        ixxyv__bfin = c.pyapi.call_method(ywkfz__rwplc, 'asarray', (
            kto__tut, zxv__zcgyy))
        builder.store(ixxyv__bfin, gwajb__gcza)
        c.pyapi.decref(ywkfz__rwplc)
        c.pyapi.decref(zxv__zcgyy)
    val = builder.load(gwajb__gcza)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        vvg__bdig = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        nyx__cxbz, ldbl__bhjm = c.pyapi.call_jit_code(lambda a:
            get_utf8_size(a), types.int64(bodo.string_type), [vvg__bdig])
        context.nrt.decref(builder, typ, vvg__bdig)
        return cgutils.pack_array(builder, [ldbl__bhjm])
    if isinstance(typ, (StructType, types.BaseTuple)):
        vnuy__fwlg = context.insert_const_string(builder.module, 'pandas')
        qsv__kyrxf = c.pyapi.import_module_noblock(vnuy__fwlg)
        C_NA = c.pyapi.object_getattr_string(qsv__kyrxf, 'NA')
        irmlz__kptfv = bodo.utils.transform.get_type_alloc_counts(typ)
        ceo__zgz = context.make_tuple(builder, types.Tuple(irmlz__kptfv * [
            types.int64]), irmlz__kptfv * [context.get_constant(types.int64,
            0)])
        bsc__iqz = cgutils.alloca_once_value(builder, ceo__zgz)
        tvcpz__ixmz = 0
        qnf__jxpt = typ.data if isinstance(typ, StructType) else typ.types
        for ayj__umm, t in enumerate(qnf__jxpt):
            raq__jawbh = bodo.utils.transform.get_type_alloc_counts(t)
            if raq__jawbh == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    ayj__umm])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, ayj__umm)
            akq__ldb = is_na_value(builder, context, val_obj, C_NA)
            vmary__ltf = builder.icmp_unsigned('!=', akq__ldb, lir.Constant
                (akq__ldb.type, 1))
            with builder.if_then(vmary__ltf):
                ceo__zgz = builder.load(bsc__iqz)
                rsa__qxyp = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for ayj__umm in range(raq__jawbh):
                    sofnd__bfba = builder.extract_value(ceo__zgz, 
                        tvcpz__ixmz + ayj__umm)
                    ddclt__ruhfs = builder.extract_value(rsa__qxyp, ayj__umm)
                    ceo__zgz = builder.insert_value(ceo__zgz, builder.add(
                        sofnd__bfba, ddclt__ruhfs), tvcpz__ixmz + ayj__umm)
                builder.store(ceo__zgz, bsc__iqz)
            tvcpz__ixmz += raq__jawbh
        c.pyapi.decref(qsv__kyrxf)
        c.pyapi.decref(C_NA)
        return builder.load(bsc__iqz)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    vnuy__fwlg = context.insert_const_string(builder.module, 'pandas')
    qsv__kyrxf = c.pyapi.import_module_noblock(vnuy__fwlg)
    C_NA = c.pyapi.object_getattr_string(qsv__kyrxf, 'NA')
    irmlz__kptfv = bodo.utils.transform.get_type_alloc_counts(typ)
    ceo__zgz = context.make_tuple(builder, types.Tuple(irmlz__kptfv * [
        types.int64]), [n] + (irmlz__kptfv - 1) * [context.get_constant(
        types.int64, 0)])
    bsc__iqz = cgutils.alloca_once_value(builder, ceo__zgz)
    with cgutils.for_range(builder, n) as wvl__xvmh:
        rdy__sew = wvl__xvmh.index
        gfr__ulgmt = seq_getitem(builder, context, arr_obj, rdy__sew)
        akq__ldb = is_na_value(builder, context, gfr__ulgmt, C_NA)
        vmary__ltf = builder.icmp_unsigned('!=', akq__ldb, lir.Constant(
            akq__ldb.type, 1))
        with builder.if_then(vmary__ltf):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                ceo__zgz = builder.load(bsc__iqz)
                rsa__qxyp = get_array_elem_counts(c, builder, context,
                    gfr__ulgmt, typ.dtype)
                for ayj__umm in range(irmlz__kptfv - 1):
                    sofnd__bfba = builder.extract_value(ceo__zgz, ayj__umm + 1)
                    ddclt__ruhfs = builder.extract_value(rsa__qxyp, ayj__umm)
                    ceo__zgz = builder.insert_value(ceo__zgz, builder.add(
                        sofnd__bfba, ddclt__ruhfs), ayj__umm + 1)
                builder.store(ceo__zgz, bsc__iqz)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                tvcpz__ixmz = 1
                for ayj__umm, t in enumerate(typ.data):
                    raq__jawbh = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if raq__jawbh == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(gfr__ulgmt, ayj__umm)
                    else:
                        val_obj = c.pyapi.dict_getitem_string(gfr__ulgmt,
                            typ.names[ayj__umm])
                    akq__ldb = is_na_value(builder, context, val_obj, C_NA)
                    vmary__ltf = builder.icmp_unsigned('!=', akq__ldb, lir.
                        Constant(akq__ldb.type, 1))
                    with builder.if_then(vmary__ltf):
                        ceo__zgz = builder.load(bsc__iqz)
                        rsa__qxyp = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for ayj__umm in range(raq__jawbh):
                            sofnd__bfba = builder.extract_value(ceo__zgz, 
                                tvcpz__ixmz + ayj__umm)
                            ddclt__ruhfs = builder.extract_value(rsa__qxyp,
                                ayj__umm)
                            ceo__zgz = builder.insert_value(ceo__zgz,
                                builder.add(sofnd__bfba, ddclt__ruhfs), 
                                tvcpz__ixmz + ayj__umm)
                        builder.store(ceo__zgz, bsc__iqz)
                    tvcpz__ixmz += raq__jawbh
            else:
                assert isinstance(typ, MapArrayType), typ
                ceo__zgz = builder.load(bsc__iqz)
                cbvs__kxrkq = dict_keys(builder, context, gfr__ulgmt)
                ocv__upugb = dict_values(builder, context, gfr__ulgmt)
                tztdv__wwk = get_array_elem_counts(c, builder, context,
                    cbvs__kxrkq, typ.key_arr_type)
                txwg__clrw = bodo.utils.transform.get_type_alloc_counts(typ
                    .key_arr_type)
                for ayj__umm in range(1, txwg__clrw + 1):
                    sofnd__bfba = builder.extract_value(ceo__zgz, ayj__umm)
                    ddclt__ruhfs = builder.extract_value(tztdv__wwk, 
                        ayj__umm - 1)
                    ceo__zgz = builder.insert_value(ceo__zgz, builder.add(
                        sofnd__bfba, ddclt__ruhfs), ayj__umm)
                qdy__zpc = get_array_elem_counts(c, builder, context,
                    ocv__upugb, typ.value_arr_type)
                for ayj__umm in range(txwg__clrw + 1, irmlz__kptfv):
                    sofnd__bfba = builder.extract_value(ceo__zgz, ayj__umm)
                    ddclt__ruhfs = builder.extract_value(qdy__zpc, ayj__umm -
                        txwg__clrw)
                    ceo__zgz = builder.insert_value(ceo__zgz, builder.add(
                        sofnd__bfba, ddclt__ruhfs), ayj__umm)
                builder.store(ceo__zgz, bsc__iqz)
                c.pyapi.decref(cbvs__kxrkq)
                c.pyapi.decref(ocv__upugb)
        c.pyapi.decref(gfr__ulgmt)
    c.pyapi.decref(qsv__kyrxf)
    c.pyapi.decref(C_NA)
    return builder.load(bsc__iqz)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    bax__vjiq = n_elems.type.count
    assert bax__vjiq >= 1
    dvm__bgsk = builder.extract_value(n_elems, 0)
    if bax__vjiq != 1:
        cde__rpns = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, ayj__umm) for ayj__umm in range(1, bax__vjiq)])
        lhf__qkr = types.Tuple([types.int64] * (bax__vjiq - 1))
    else:
        cde__rpns = context.get_dummy_value()
        lhf__qkr = types.none
    alc__tatwp = types.TypeRef(arr_type)
    rhkem__gmo = arr_type(types.int64, alc__tatwp, lhf__qkr)
    args = [dvm__bgsk, context.get_dummy_value(), cde__rpns]
    pbfx__eekij = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        nyx__cxbz, ecmuh__nbbs = c.pyapi.call_jit_code(pbfx__eekij,
            rhkem__gmo, args)
    else:
        ecmuh__nbbs = context.compile_internal(builder, pbfx__eekij,
            rhkem__gmo, args)
    return ecmuh__nbbs


def is_ll_eq(builder, val1, val2):
    bbo__jqd = val1.type.pointee
    jyyn__nmavp = val2.type.pointee
    assert bbo__jqd == jyyn__nmavp, 'invalid llvm value comparison'
    if isinstance(bbo__jqd, (lir.BaseStructType, lir.ArrayType)):
        n_elems = len(bbo__jqd.elements) if isinstance(bbo__jqd, lir.
            BaseStructType) else bbo__jqd.count
        mmemh__vnm = lir.Constant(lir.IntType(1), 1)
        for ayj__umm in range(n_elems):
            hqiem__isy = lir.IntType(32)(0)
            zytl__sopbz = lir.IntType(32)(ayj__umm)
            gknii__nyec = builder.gep(val1, [hqiem__isy, zytl__sopbz],
                inbounds=True)
            fsky__idzfd = builder.gep(val2, [hqiem__isy, zytl__sopbz],
                inbounds=True)
            mmemh__vnm = builder.and_(mmemh__vnm, is_ll_eq(builder,
                gknii__nyec, fsky__idzfd))
        return mmemh__vnm
    xebi__fyso = builder.load(val1)
    pyjgo__adda = builder.load(val2)
    if xebi__fyso.type in (lir.FloatType(), lir.DoubleType()):
        zxhjs__pokm = 32 if xebi__fyso.type == lir.FloatType() else 64
        xebi__fyso = builder.bitcast(xebi__fyso, lir.IntType(zxhjs__pokm))
        pyjgo__adda = builder.bitcast(pyjgo__adda, lir.IntType(zxhjs__pokm))
    return builder.icmp_unsigned('==', xebi__fyso, pyjgo__adda)
