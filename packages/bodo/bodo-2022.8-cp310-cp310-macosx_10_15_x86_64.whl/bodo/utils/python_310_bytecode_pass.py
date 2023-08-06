"""
transforms the IR to handle bytecode issues in Python 3.10. This
should be removed once https://github.com/numba/numba/pull/7866
is included in Numba 0.56
"""
import operator
import numba
from numba.core import ir
from numba.core.compiler_machinery import FunctionPass, register_pass
from numba.core.errors import UnsupportedError
from numba.core.ir_utils import dprint_func_ir, get_definition, guard


@register_pass(mutates_CFG=False, analysis_only=False)
class Bodo310ByteCodePass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        dprint_func_ir(state.func_ir,
            'starting Bodo 3.10 Bytecode optimizations pass')
        peep_hole_call_function_ex_to_call_function_kw(state.func_ir)
        peep_hole_fuse_dict_add_updates(state.func_ir)
        peep_hole_fuse_tuple_adds(state.func_ir)
        return True


def peep_hole_fuse_tuple_adds(func_ir):
    for jpm__vdlv in func_ir.blocks.values():
        new_body = []
        kiil__bylp = {}
        for ccu__pvez, xwb__oom in enumerate(jpm__vdlv.body):
            aha__ycb = None
            if isinstance(xwb__oom, ir.Assign) and isinstance(xwb__oom.
                value, ir.Expr):
                way__iaom = xwb__oom.target.name
                if xwb__oom.value.op == 'build_tuple':
                    aha__ycb = way__iaom
                    kiil__bylp[way__iaom] = xwb__oom.value.items
                elif xwb__oom.value.op == 'binop' and xwb__oom.value.fn == operator.add and xwb__oom.value.lhs.name in kiil__bylp and xwb__oom.value.rhs.name in kiil__bylp:
                    aha__ycb = way__iaom
                    new_items = kiil__bylp[xwb__oom.value.lhs.name
                        ] + kiil__bylp[xwb__oom.value.rhs.name]
                    xniwp__lkioa = ir.Expr.build_tuple(new_items, xwb__oom.
                        value.loc)
                    kiil__bylp[way__iaom] = new_items
                    del kiil__bylp[xwb__oom.value.lhs.name]
                    del kiil__bylp[xwb__oom.value.rhs.name]
                    if xwb__oom.value in func_ir._definitions[way__iaom]:
                        func_ir._definitions[way__iaom].remove(xwb__oom.value)
                    func_ir._definitions[way__iaom].append(xniwp__lkioa)
                    xwb__oom = ir.Assign(xniwp__lkioa, xwb__oom.target,
                        xwb__oom.loc)
            for tdd__azjh in xwb__oom.list_vars():
                if tdd__azjh.name in kiil__bylp and tdd__azjh.name != aha__ycb:
                    del kiil__bylp[tdd__azjh.name]
            new_body.append(xwb__oom)
        jpm__vdlv.body = new_body
    return func_ir


def _call_function_ex_replace_kws_small(keyword_expr, new_body, buildmap_idx):
    amtpi__ybeq = keyword_expr.items.copy()
    cxku__ghkxe = keyword_expr.value_indexes
    for efi__xwacl, aclup__kyu in cxku__ghkxe.items():
        amtpi__ybeq[aclup__kyu] = efi__xwacl, amtpi__ybeq[aclup__kyu][1]
    new_body[buildmap_idx] = None
    return amtpi__ybeq


def _call_function_ex_replace_kws_large(body, buildmap_name, buildmap_idx,
    search_end, new_body):
    itj__xgfzi = 'CALL_FUNCTION_EX with **kwargs not supported'
    new_body[buildmap_idx] = None
    amtpi__ybeq = []
    asr__sjyty = buildmap_idx + 1
    while asr__sjyty <= search_end:
        jqi__yey = body[asr__sjyty]
        if not (isinstance(jqi__yey, ir.Assign) and isinstance(jqi__yey.
            value, ir.Const)):
            raise UnsupportedError(itj__xgfzi)
        irjml__xwygl = jqi__yey.target.name
        slghv__hxikf = jqi__yey.value.value
        asr__sjyty += 1
        etap__utqwv = True
        while asr__sjyty <= search_end and etap__utqwv:
            jtfo__ayqs = body[asr__sjyty]
            if (isinstance(jtfo__ayqs, ir.Assign) and isinstance(jtfo__ayqs
                .value, ir.Expr) and jtfo__ayqs.value.op == 'getattr' and 
                jtfo__ayqs.value.value.name == buildmap_name and jtfo__ayqs
                .value.attr == '__setitem__'):
                etap__utqwv = False
            else:
                asr__sjyty += 1
        if etap__utqwv or asr__sjyty == search_end:
            raise UnsupportedError(itj__xgfzi)
        iwzmo__imsrj = body[asr__sjyty + 1]
        if not (isinstance(iwzmo__imsrj, ir.Assign) and isinstance(
            iwzmo__imsrj.value, ir.Expr) and iwzmo__imsrj.value.op ==
            'call' and iwzmo__imsrj.value.func.name == jtfo__ayqs.target.
            name and len(iwzmo__imsrj.value.args) == 2 and iwzmo__imsrj.
            value.args[0].name == irjml__xwygl):
            raise UnsupportedError(itj__xgfzi)
        qwr__crl = iwzmo__imsrj.value.args[1]
        amtpi__ybeq.append((slghv__hxikf, qwr__crl))
        new_body[asr__sjyty] = None
        new_body[asr__sjyty + 1] = None
        asr__sjyty += 2
    return amtpi__ybeq


def _call_function_ex_replace_args_small(tuple_expr, new_body, buildtuple_idx):
    new_body[buildtuple_idx] = None
    return tuple_expr.items


def _call_function_ex_replace_args_large(vararg_stmt, body, new_body,
    search_end):
    itj__xgfzi = 'CALL_FUNCTION_EX with **kwargs not supported'
    asr__sjyty = 0
    flw__nln = []
    if isinstance(vararg_stmt, ir.Assign) and isinstance(vararg_stmt.value,
        ir.Var):
        ekpyi__ice = vararg_stmt.value.name
        new_body[search_end] = None
        search_end -= 1
    else:
        ekpyi__ice = vararg_stmt.target.name
    opk__fom = True
    while search_end >= asr__sjyty and opk__fom:
        nxx__zuae = body[search_end]
        if (isinstance(nxx__zuae, ir.Assign) and nxx__zuae.target.name ==
            ekpyi__ice and isinstance(nxx__zuae.value, ir.Expr) and 
            nxx__zuae.value.op == 'build_tuple' and not nxx__zuae.value.items):
            opk__fom = False
            new_body[search_end] = None
        else:
            if search_end == asr__sjyty or not (isinstance(nxx__zuae, ir.
                Assign) and nxx__zuae.target.name == ekpyi__ice and
                isinstance(nxx__zuae.value, ir.Expr) and nxx__zuae.value.op ==
                'binop' and nxx__zuae.value.fn == operator.add):
                raise UnsupportedError(itj__xgfzi)
            zgs__ekn = nxx__zuae.value.lhs.name
            rjf__lldb = nxx__zuae.value.rhs.name
            oqfuy__uez = body[search_end - 1]
            if not (isinstance(oqfuy__uez, ir.Assign) and isinstance(
                oqfuy__uez.value, ir.Expr) and oqfuy__uez.value.op ==
                'build_tuple' and len(oqfuy__uez.value.items) == 1):
                raise UnsupportedError(itj__xgfzi)
            if oqfuy__uez.target.name == zgs__ekn:
                ekpyi__ice = rjf__lldb
            elif oqfuy__uez.target.name == rjf__lldb:
                ekpyi__ice = zgs__ekn
            else:
                raise UnsupportedError(itj__xgfzi)
            flw__nln.append(oqfuy__uez.value.items[0])
            new_body[search_end] = None
            new_body[search_end - 1] = None
            search_end -= 2
            bgpw__ctv = True
            while search_end >= asr__sjyty and bgpw__ctv:
                emhzl__zoob = body[search_end]
                if isinstance(emhzl__zoob, ir.Assign
                    ) and emhzl__zoob.target.name == ekpyi__ice:
                    bgpw__ctv = False
                else:
                    search_end -= 1
    if opk__fom:
        raise UnsupportedError(itj__xgfzi)
    return flw__nln[::-1]


def peep_hole_call_function_ex_to_call_function_kw(func_ir):
    itj__xgfzi = 'CALL_FUNCTION_EX with **kwargs not supported'
    for jpm__vdlv in func_ir.blocks.values():
        lrmzs__kunfa = False
        new_body = []
        for ccu__pvez, xwb__oom in enumerate(jpm__vdlv.body):
            if (isinstance(xwb__oom, ir.Assign) and isinstance(xwb__oom.
                value, ir.Expr) and xwb__oom.value.op == 'call' and 
                xwb__oom.value.varkwarg is not None):
                lrmzs__kunfa = True
                zomh__hamap = xwb__oom.value
                args = zomh__hamap.args
                amtpi__ybeq = zomh__hamap.kws
                kes__kiu = zomh__hamap.vararg
                pzfo__nfdz = zomh__hamap.varkwarg
                bdaj__cnut = ccu__pvez - 1
                crbjg__xou = bdaj__cnut
                zzb__pwct = None
                noye__eraud = True
                while crbjg__xou >= 0 and noye__eraud:
                    zzb__pwct = jpm__vdlv.body[crbjg__xou]
                    if isinstance(zzb__pwct, ir.Assign
                        ) and zzb__pwct.target.name == pzfo__nfdz.name:
                        noye__eraud = False
                    else:
                        crbjg__xou -= 1
                if amtpi__ybeq or noye__eraud or not (isinstance(zzb__pwct.
                    value, ir.Expr) and zzb__pwct.value.op == 'build_map'):
                    raise UnsupportedError(itj__xgfzi)
                if zzb__pwct.value.items:
                    amtpi__ybeq = _call_function_ex_replace_kws_small(zzb__pwct
                        .value, new_body, crbjg__xou)
                else:
                    amtpi__ybeq = _call_function_ex_replace_kws_large(jpm__vdlv
                        .body, pzfo__nfdz.name, crbjg__xou, ccu__pvez - 1,
                        new_body)
                bdaj__cnut = crbjg__xou
                if kes__kiu is not None:
                    if args:
                        raise UnsupportedError(itj__xgfzi)
                    gnogy__ultl = bdaj__cnut
                    iie__sjjl = None
                    noye__eraud = True
                    while gnogy__ultl >= 0 and noye__eraud:
                        iie__sjjl = jpm__vdlv.body[gnogy__ultl]
                        if isinstance(iie__sjjl, ir.Assign
                            ) and iie__sjjl.target.name == kes__kiu.name:
                            noye__eraud = False
                        else:
                            gnogy__ultl -= 1
                    if noye__eraud:
                        raise UnsupportedError(itj__xgfzi)
                    if isinstance(iie__sjjl.value, ir.Expr
                        ) and iie__sjjl.value.op == 'build_tuple':
                        args = _call_function_ex_replace_args_small(iie__sjjl
                            .value, new_body, gnogy__ultl)
                    else:
                        args = _call_function_ex_replace_args_large(iie__sjjl,
                            jpm__vdlv.body, new_body, gnogy__ultl)
                jba__airk = ir.Expr.call(zomh__hamap.func, args,
                    amtpi__ybeq, zomh__hamap.loc, target=zomh__hamap.target)
                if xwb__oom.target.name in func_ir._definitions and len(func_ir
                    ._definitions[xwb__oom.target.name]) == 1:
                    func_ir._definitions[xwb__oom.target.name].clear()
                func_ir._definitions[xwb__oom.target.name].append(jba__airk)
                xwb__oom = ir.Assign(jba__airk, xwb__oom.target, xwb__oom.loc)
            new_body.append(xwb__oom)
        if lrmzs__kunfa:
            jpm__vdlv.body = [uamn__iwik for uamn__iwik in new_body if 
                uamn__iwik is not None]
    return func_ir


def peep_hole_fuse_dict_add_updates(func_ir):
    for jpm__vdlv in func_ir.blocks.values():
        new_body = []
        lit_old_idx = {}
        lit_new_idx = {}
        map_updates = {}
        lrmzs__kunfa = False
        for ccu__pvez, xwb__oom in enumerate(jpm__vdlv.body):
            syqlf__oitou = True
            wmo__zwx = None
            if isinstance(xwb__oom, ir.Assign) and isinstance(xwb__oom.
                value, ir.Expr):
                if xwb__oom.value.op == 'build_map':
                    wmo__zwx = xwb__oom.target.name
                    lit_old_idx[xwb__oom.target.name] = ccu__pvez
                    lit_new_idx[xwb__oom.target.name] = ccu__pvez
                    map_updates[xwb__oom.target.name
                        ] = xwb__oom.value.items.copy()
                    syqlf__oitou = False
                elif xwb__oom.value.op == 'call' and ccu__pvez > 0:
                    njpm__iktqv = xwb__oom.value.func.name
                    jtfo__ayqs = jpm__vdlv.body[ccu__pvez - 1]
                    args = xwb__oom.value.args
                    if (isinstance(jtfo__ayqs, ir.Assign) and jtfo__ayqs.
                        target.name == njpm__iktqv and isinstance(
                        jtfo__ayqs.value, ir.Expr) and jtfo__ayqs.value.op ==
                        'getattr' and jtfo__ayqs.value.value.name in
                        lit_old_idx):
                        ouk__rvuz = jtfo__ayqs.value.value.name
                        ccpti__ibv = jtfo__ayqs.value.attr
                        if ccpti__ibv == '__setitem__':
                            syqlf__oitou = False
                            map_updates[ouk__rvuz].append(args)
                            new_body[-1] = None
                        elif ccpti__ibv == 'update' and args[0
                            ].name in lit_old_idx:
                            syqlf__oitou = False
                            map_updates[ouk__rvuz].extend(map_updates[args[
                                0].name])
                            new_body[-1] = None
                        if not syqlf__oitou:
                            lit_new_idx[ouk__rvuz] = ccu__pvez
                            func_ir._definitions[jtfo__ayqs.target.name
                                ].remove(jtfo__ayqs.value)
            if not (isinstance(xwb__oom, ir.Assign) and isinstance(xwb__oom
                .value, ir.Expr) and xwb__oom.value.op == 'getattr' and 
                xwb__oom.value.value.name in lit_old_idx and xwb__oom.value
                .attr in ('__setitem__', 'update')):
                for tdd__azjh in xwb__oom.list_vars():
                    if (tdd__azjh.name in lit_old_idx and tdd__azjh.name !=
                        wmo__zwx):
                        _insert_build_map(func_ir, tdd__azjh.name,
                            jpm__vdlv.body, new_body, lit_old_idx,
                            lit_new_idx, map_updates)
            if syqlf__oitou:
                new_body.append(xwb__oom)
            else:
                func_ir._definitions[xwb__oom.target.name].remove(xwb__oom.
                    value)
                lrmzs__kunfa = True
                new_body.append(None)
        qndn__iggsn = list(lit_old_idx.keys())
        for bxec__gveew in qndn__iggsn:
            _insert_build_map(func_ir, bxec__gveew, jpm__vdlv.body,
                new_body, lit_old_idx, lit_new_idx, map_updates)
        if lrmzs__kunfa:
            jpm__vdlv.body = [uamn__iwik for uamn__iwik in new_body if 
                uamn__iwik is not None]
    return func_ir


def _insert_build_map(func_ir, name, old_body, new_body, lit_old_idx,
    lit_new_idx, map_updates):
    gnirl__npad = lit_old_idx[name]
    tkmtg__saiil = lit_new_idx[name]
    owxf__rezxx = map_updates[name]
    new_body[tkmtg__saiil] = _build_new_build_map(func_ir, name, old_body,
        gnirl__npad, owxf__rezxx)
    del lit_old_idx[name]
    del lit_new_idx[name]
    del map_updates[name]


def _build_new_build_map(func_ir, name, old_body, old_lineno, new_items):
    vwl__kqsuk = old_body[old_lineno]
    obgcy__xpuya = vwl__kqsuk.target
    pkh__lne = vwl__kqsuk.value
    rdnf__nfv = []
    iebxq__dxj = []
    for sss__eaxbp in new_items:
        bsv__puvv, gxaak__jxjq = sss__eaxbp
        xrf__gtn = guard(get_definition, func_ir, bsv__puvv)
        if isinstance(xrf__gtn, (ir.Const, ir.Global, ir.FreeVar)):
            rdnf__nfv.append(xrf__gtn.value)
        ujye__yjmdn = guard(get_definition, func_ir, gxaak__jxjq)
        if isinstance(ujye__yjmdn, (ir.Const, ir.Global, ir.FreeVar)):
            iebxq__dxj.append(ujye__yjmdn.value)
        else:
            iebxq__dxj.append(numba.core.interpreter._UNKNOWN_VALUE(
                gxaak__jxjq.name))
    cxku__ghkxe = {}
    if len(rdnf__nfv) == len(new_items):
        nvrou__mqv = {uamn__iwik: kklvd__urtot for uamn__iwik, kklvd__urtot in
            zip(rdnf__nfv, iebxq__dxj)}
        for ccu__pvez, bsv__puvv in enumerate(rdnf__nfv):
            cxku__ghkxe[bsv__puvv] = ccu__pvez
    else:
        nvrou__mqv = None
    dzsxe__qvnmd = ir.Expr.build_map(items=new_items, size=len(new_items),
        literal_value=nvrou__mqv, value_indexes=cxku__ghkxe, loc=pkh__lne.loc)
    func_ir._definitions[name].append(dzsxe__qvnmd)
    return ir.Assign(dzsxe__qvnmd, ir.Var(obgcy__xpuya.scope, name,
        obgcy__xpuya.loc), dzsxe__qvnmd.loc)
