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
    xrnf__quge = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    foxx__dasv = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    pgfjc__vhj = builder.gep(null_bitmap_ptr, [xrnf__quge], inbounds=True)
    vdm__rap = builder.load(pgfjc__vhj)
    weug__oacy = lir.ArrayType(lir.IntType(8), 8)
    hfdvj__amvud = cgutils.alloca_once_value(builder, lir.Constant(
        weug__oacy, (1, 2, 4, 8, 16, 32, 64, 128)))
    gjj__sxuhl = builder.load(builder.gep(hfdvj__amvud, [lir.Constant(lir.
        IntType(64), 0), foxx__dasv], inbounds=True))
    if val:
        builder.store(builder.or_(vdm__rap, gjj__sxuhl), pgfjc__vhj)
    else:
        gjj__sxuhl = builder.xor(gjj__sxuhl, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(vdm__rap, gjj__sxuhl), pgfjc__vhj)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    xrnf__quge = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    foxx__dasv = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    vdm__rap = builder.load(builder.gep(null_bitmap_ptr, [xrnf__quge],
        inbounds=True))
    weug__oacy = lir.ArrayType(lir.IntType(8), 8)
    hfdvj__amvud = cgutils.alloca_once_value(builder, lir.Constant(
        weug__oacy, (1, 2, 4, 8, 16, 32, 64, 128)))
    gjj__sxuhl = builder.load(builder.gep(hfdvj__amvud, [lir.Constant(lir.
        IntType(64), 0), foxx__dasv], inbounds=True))
    return builder.and_(vdm__rap, gjj__sxuhl)


def pyarray_check(builder, context, obj):
    fwpkm__eepv = context.get_argument_type(types.pyobject)
    bkht__unab = lir.FunctionType(lir.IntType(32), [fwpkm__eepv])
    xryx__sygqj = cgutils.get_or_insert_function(builder.module, bkht__unab,
        name='is_np_array')
    return builder.call(xryx__sygqj, [obj])


def pyarray_getitem(builder, context, arr_obj, ind):
    fwpkm__eepv = context.get_argument_type(types.pyobject)
    vgbp__izc = context.get_value_type(types.intp)
    gebxa__wiq = lir.FunctionType(lir.IntType(8).as_pointer(), [fwpkm__eepv,
        vgbp__izc])
    llpqh__kjjix = cgutils.get_or_insert_function(builder.module,
        gebxa__wiq, name='array_getptr1')
    hig__rtk = lir.FunctionType(fwpkm__eepv, [fwpkm__eepv, lir.IntType(8).
        as_pointer()])
    rbjp__brc = cgutils.get_or_insert_function(builder.module, hig__rtk,
        name='array_getitem')
    embq__pkj = builder.call(llpqh__kjjix, [arr_obj, ind])
    return builder.call(rbjp__brc, [arr_obj, embq__pkj])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    fwpkm__eepv = context.get_argument_type(types.pyobject)
    vgbp__izc = context.get_value_type(types.intp)
    gebxa__wiq = lir.FunctionType(lir.IntType(8).as_pointer(), [fwpkm__eepv,
        vgbp__izc])
    llpqh__kjjix = cgutils.get_or_insert_function(builder.module,
        gebxa__wiq, name='array_getptr1')
    ywi__job = lir.FunctionType(lir.VoidType(), [fwpkm__eepv, lir.IntType(8
        ).as_pointer(), fwpkm__eepv])
    rtty__azis = cgutils.get_or_insert_function(builder.module, ywi__job,
        name='array_setitem')
    embq__pkj = builder.call(llpqh__kjjix, [arr_obj, ind])
    builder.call(rtty__azis, [arr_obj, embq__pkj, val_obj])


def seq_getitem(builder, context, obj, ind):
    fwpkm__eepv = context.get_argument_type(types.pyobject)
    vgbp__izc = context.get_value_type(types.intp)
    ubyja__ytjpy = lir.FunctionType(fwpkm__eepv, [fwpkm__eepv, vgbp__izc])
    frqst__pqsrk = cgutils.get_or_insert_function(builder.module,
        ubyja__ytjpy, name='seq_getitem')
    return builder.call(frqst__pqsrk, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    fwpkm__eepv = context.get_argument_type(types.pyobject)
    klsnx__hsbp = lir.FunctionType(lir.IntType(32), [fwpkm__eepv, fwpkm__eepv])
    powyp__ncldr = cgutils.get_or_insert_function(builder.module,
        klsnx__hsbp, name='is_na_value')
    return builder.call(powyp__ncldr, [val, C_NA])


def list_check(builder, context, obj):
    fwpkm__eepv = context.get_argument_type(types.pyobject)
    vygv__tshv = context.get_value_type(types.int32)
    vjfeq__emn = lir.FunctionType(vygv__tshv, [fwpkm__eepv])
    ucxux__qif = cgutils.get_or_insert_function(builder.module, vjfeq__emn,
        name='list_check')
    return builder.call(ucxux__qif, [obj])


def dict_keys(builder, context, obj):
    fwpkm__eepv = context.get_argument_type(types.pyobject)
    vjfeq__emn = lir.FunctionType(fwpkm__eepv, [fwpkm__eepv])
    ucxux__qif = cgutils.get_or_insert_function(builder.module, vjfeq__emn,
        name='dict_keys')
    return builder.call(ucxux__qif, [obj])


def dict_values(builder, context, obj):
    fwpkm__eepv = context.get_argument_type(types.pyobject)
    vjfeq__emn = lir.FunctionType(fwpkm__eepv, [fwpkm__eepv])
    ucxux__qif = cgutils.get_or_insert_function(builder.module, vjfeq__emn,
        name='dict_values')
    return builder.call(ucxux__qif, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    fwpkm__eepv = context.get_argument_type(types.pyobject)
    vjfeq__emn = lir.FunctionType(lir.VoidType(), [fwpkm__eepv, fwpkm__eepv])
    ucxux__qif = cgutils.get_or_insert_function(builder.module, vjfeq__emn,
        name='dict_merge_from_seq2')
    builder.call(ucxux__qif, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    wby__cdwt = cgutils.alloca_once_value(builder, val)
    pms__mublj = list_check(builder, context, val)
    ksrda__hic = builder.icmp_unsigned('!=', pms__mublj, lir.Constant(
        pms__mublj.type, 0))
    with builder.if_then(ksrda__hic):
        vwaq__kjz = context.insert_const_string(builder.module, 'numpy')
        mhocn__dzm = c.pyapi.import_module_noblock(vwaq__kjz)
        lnel__xttsr = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            lnel__xttsr = str(typ.dtype)
        yccf__aqs = c.pyapi.object_getattr_string(mhocn__dzm, lnel__xttsr)
        rnfqo__dvwuj = builder.load(wby__cdwt)
        xemk__piohj = c.pyapi.call_method(mhocn__dzm, 'asarray', (
            rnfqo__dvwuj, yccf__aqs))
        builder.store(xemk__piohj, wby__cdwt)
        c.pyapi.decref(mhocn__dzm)
        c.pyapi.decref(yccf__aqs)
    val = builder.load(wby__cdwt)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        hygi__dvfo = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        jnodx__oxrlh, wywo__bgq = c.pyapi.call_jit_code(lambda a:
            get_utf8_size(a), types.int64(bodo.string_type), [hygi__dvfo])
        context.nrt.decref(builder, typ, hygi__dvfo)
        return cgutils.pack_array(builder, [wywo__bgq])
    if isinstance(typ, (StructType, types.BaseTuple)):
        vwaq__kjz = context.insert_const_string(builder.module, 'pandas')
        bmja__uizvc = c.pyapi.import_module_noblock(vwaq__kjz)
        C_NA = c.pyapi.object_getattr_string(bmja__uizvc, 'NA')
        sltg__tvg = bodo.utils.transform.get_type_alloc_counts(typ)
        uqclj__sqg = context.make_tuple(builder, types.Tuple(sltg__tvg * [
            types.int64]), sltg__tvg * [context.get_constant(types.int64, 0)])
        mjc__mmxzz = cgutils.alloca_once_value(builder, uqclj__sqg)
        semo__kayjf = 0
        casp__hmwnv = typ.data if isinstance(typ, StructType) else typ.types
        for wsb__vrt, t in enumerate(casp__hmwnv):
            hwtn__dauws = bodo.utils.transform.get_type_alloc_counts(t)
            if hwtn__dauws == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    wsb__vrt])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, wsb__vrt)
            cobw__zgdal = is_na_value(builder, context, val_obj, C_NA)
            urec__yyvlg = builder.icmp_unsigned('!=', cobw__zgdal, lir.
                Constant(cobw__zgdal.type, 1))
            with builder.if_then(urec__yyvlg):
                uqclj__sqg = builder.load(mjc__mmxzz)
                vogjh__frc = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for wsb__vrt in range(hwtn__dauws):
                    wucz__ttpvd = builder.extract_value(uqclj__sqg, 
                        semo__kayjf + wsb__vrt)
                    eimpt__bqfyq = builder.extract_value(vogjh__frc, wsb__vrt)
                    uqclj__sqg = builder.insert_value(uqclj__sqg, builder.
                        add(wucz__ttpvd, eimpt__bqfyq), semo__kayjf + wsb__vrt)
                builder.store(uqclj__sqg, mjc__mmxzz)
            semo__kayjf += hwtn__dauws
        c.pyapi.decref(bmja__uizvc)
        c.pyapi.decref(C_NA)
        return builder.load(mjc__mmxzz)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    vwaq__kjz = context.insert_const_string(builder.module, 'pandas')
    bmja__uizvc = c.pyapi.import_module_noblock(vwaq__kjz)
    C_NA = c.pyapi.object_getattr_string(bmja__uizvc, 'NA')
    sltg__tvg = bodo.utils.transform.get_type_alloc_counts(typ)
    uqclj__sqg = context.make_tuple(builder, types.Tuple(sltg__tvg * [types
        .int64]), [n] + (sltg__tvg - 1) * [context.get_constant(types.int64,
        0)])
    mjc__mmxzz = cgutils.alloca_once_value(builder, uqclj__sqg)
    with cgutils.for_range(builder, n) as sgown__jtnmz:
        cwjy__eofm = sgown__jtnmz.index
        aiw__qvn = seq_getitem(builder, context, arr_obj, cwjy__eofm)
        cobw__zgdal = is_na_value(builder, context, aiw__qvn, C_NA)
        urec__yyvlg = builder.icmp_unsigned('!=', cobw__zgdal, lir.Constant
            (cobw__zgdal.type, 1))
        with builder.if_then(urec__yyvlg):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                uqclj__sqg = builder.load(mjc__mmxzz)
                vogjh__frc = get_array_elem_counts(c, builder, context,
                    aiw__qvn, typ.dtype)
                for wsb__vrt in range(sltg__tvg - 1):
                    wucz__ttpvd = builder.extract_value(uqclj__sqg, 
                        wsb__vrt + 1)
                    eimpt__bqfyq = builder.extract_value(vogjh__frc, wsb__vrt)
                    uqclj__sqg = builder.insert_value(uqclj__sqg, builder.
                        add(wucz__ttpvd, eimpt__bqfyq), wsb__vrt + 1)
                builder.store(uqclj__sqg, mjc__mmxzz)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                semo__kayjf = 1
                for wsb__vrt, t in enumerate(typ.data):
                    hwtn__dauws = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if hwtn__dauws == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(aiw__qvn, wsb__vrt)
                    else:
                        val_obj = c.pyapi.dict_getitem_string(aiw__qvn, typ
                            .names[wsb__vrt])
                    cobw__zgdal = is_na_value(builder, context, val_obj, C_NA)
                    urec__yyvlg = builder.icmp_unsigned('!=', cobw__zgdal,
                        lir.Constant(cobw__zgdal.type, 1))
                    with builder.if_then(urec__yyvlg):
                        uqclj__sqg = builder.load(mjc__mmxzz)
                        vogjh__frc = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for wsb__vrt in range(hwtn__dauws):
                            wucz__ttpvd = builder.extract_value(uqclj__sqg,
                                semo__kayjf + wsb__vrt)
                            eimpt__bqfyq = builder.extract_value(vogjh__frc,
                                wsb__vrt)
                            uqclj__sqg = builder.insert_value(uqclj__sqg,
                                builder.add(wucz__ttpvd, eimpt__bqfyq), 
                                semo__kayjf + wsb__vrt)
                        builder.store(uqclj__sqg, mjc__mmxzz)
                    semo__kayjf += hwtn__dauws
            else:
                assert isinstance(typ, MapArrayType), typ
                uqclj__sqg = builder.load(mjc__mmxzz)
                tqs__epjnm = dict_keys(builder, context, aiw__qvn)
                jjpp__ehg = dict_values(builder, context, aiw__qvn)
                jkr__gge = get_array_elem_counts(c, builder, context,
                    tqs__epjnm, typ.key_arr_type)
                wyfy__aml = bodo.utils.transform.get_type_alloc_counts(typ.
                    key_arr_type)
                for wsb__vrt in range(1, wyfy__aml + 1):
                    wucz__ttpvd = builder.extract_value(uqclj__sqg, wsb__vrt)
                    eimpt__bqfyq = builder.extract_value(jkr__gge, wsb__vrt - 1
                        )
                    uqclj__sqg = builder.insert_value(uqclj__sqg, builder.
                        add(wucz__ttpvd, eimpt__bqfyq), wsb__vrt)
                hfyx__yoz = get_array_elem_counts(c, builder, context,
                    jjpp__ehg, typ.value_arr_type)
                for wsb__vrt in range(wyfy__aml + 1, sltg__tvg):
                    wucz__ttpvd = builder.extract_value(uqclj__sqg, wsb__vrt)
                    eimpt__bqfyq = builder.extract_value(hfyx__yoz, 
                        wsb__vrt - wyfy__aml)
                    uqclj__sqg = builder.insert_value(uqclj__sqg, builder.
                        add(wucz__ttpvd, eimpt__bqfyq), wsb__vrt)
                builder.store(uqclj__sqg, mjc__mmxzz)
                c.pyapi.decref(tqs__epjnm)
                c.pyapi.decref(jjpp__ehg)
        c.pyapi.decref(aiw__qvn)
    c.pyapi.decref(bmja__uizvc)
    c.pyapi.decref(C_NA)
    return builder.load(mjc__mmxzz)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    snjq__too = n_elems.type.count
    assert snjq__too >= 1
    cjqb__gkgq = builder.extract_value(n_elems, 0)
    if snjq__too != 1:
        olmi__jkdra = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, wsb__vrt) for wsb__vrt in range(1, snjq__too)])
        hvz__iynm = types.Tuple([types.int64] * (snjq__too - 1))
    else:
        olmi__jkdra = context.get_dummy_value()
        hvz__iynm = types.none
    owaf__kun = types.TypeRef(arr_type)
    luwl__pst = arr_type(types.int64, owaf__kun, hvz__iynm)
    args = [cjqb__gkgq, context.get_dummy_value(), olmi__jkdra]
    aqm__xwtvw = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        jnodx__oxrlh, vfp__wltqt = c.pyapi.call_jit_code(aqm__xwtvw,
            luwl__pst, args)
    else:
        vfp__wltqt = context.compile_internal(builder, aqm__xwtvw,
            luwl__pst, args)
    return vfp__wltqt


def is_ll_eq(builder, val1, val2):
    coqpj__qlhn = val1.type.pointee
    wipt__pxaim = val2.type.pointee
    assert coqpj__qlhn == wipt__pxaim, 'invalid llvm value comparison'
    if isinstance(coqpj__qlhn, (lir.BaseStructType, lir.ArrayType)):
        n_elems = len(coqpj__qlhn.elements) if isinstance(coqpj__qlhn, lir.
            BaseStructType) else coqpj__qlhn.count
        rip__vmmi = lir.Constant(lir.IntType(1), 1)
        for wsb__vrt in range(n_elems):
            wyzmo__shna = lir.IntType(32)(0)
            bdx__cegqz = lir.IntType(32)(wsb__vrt)
            aujsc__jlqmh = builder.gep(val1, [wyzmo__shna, bdx__cegqz],
                inbounds=True)
            mhfz__xivcc = builder.gep(val2, [wyzmo__shna, bdx__cegqz],
                inbounds=True)
            rip__vmmi = builder.and_(rip__vmmi, is_ll_eq(builder,
                aujsc__jlqmh, mhfz__xivcc))
        return rip__vmmi
    jbcsw__cfqx = builder.load(val1)
    mgyw__cfb = builder.load(val2)
    if jbcsw__cfqx.type in (lir.FloatType(), lir.DoubleType()):
        lpxj__oyayv = 32 if jbcsw__cfqx.type == lir.FloatType() else 64
        jbcsw__cfqx = builder.bitcast(jbcsw__cfqx, lir.IntType(lpxj__oyayv))
        mgyw__cfb = builder.bitcast(mgyw__cfb, lir.IntType(lpxj__oyayv))
    return builder.icmp_unsigned('==', jbcsw__cfqx, mgyw__cfb)
