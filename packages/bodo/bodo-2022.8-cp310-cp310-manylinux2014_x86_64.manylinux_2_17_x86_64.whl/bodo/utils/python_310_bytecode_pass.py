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
    for tjbn__bzxf in func_ir.blocks.values():
        new_body = []
        ead__oylwu = {}
        for dhpf__csrxy, qgn__pshd in enumerate(tjbn__bzxf.body):
            qetna__wxddb = None
            if isinstance(qgn__pshd, ir.Assign) and isinstance(qgn__pshd.
                value, ir.Expr):
                wgp__nozt = qgn__pshd.target.name
                if qgn__pshd.value.op == 'build_tuple':
                    qetna__wxddb = wgp__nozt
                    ead__oylwu[wgp__nozt] = qgn__pshd.value.items
                elif qgn__pshd.value.op == 'binop' and qgn__pshd.value.fn == operator.add and qgn__pshd.value.lhs.name in ead__oylwu and qgn__pshd.value.rhs.name in ead__oylwu:
                    qetna__wxddb = wgp__nozt
                    new_items = ead__oylwu[qgn__pshd.value.lhs.name
                        ] + ead__oylwu[qgn__pshd.value.rhs.name]
                    ypiw__vmvem = ir.Expr.build_tuple(new_items, qgn__pshd.
                        value.loc)
                    ead__oylwu[wgp__nozt] = new_items
                    del ead__oylwu[qgn__pshd.value.lhs.name]
                    del ead__oylwu[qgn__pshd.value.rhs.name]
                    if qgn__pshd.value in func_ir._definitions[wgp__nozt]:
                        func_ir._definitions[wgp__nozt].remove(qgn__pshd.value)
                    func_ir._definitions[wgp__nozt].append(ypiw__vmvem)
                    qgn__pshd = ir.Assign(ypiw__vmvem, qgn__pshd.target,
                        qgn__pshd.loc)
            for hzgj__tfrc in qgn__pshd.list_vars():
                if (hzgj__tfrc.name in ead__oylwu and hzgj__tfrc.name !=
                    qetna__wxddb):
                    del ead__oylwu[hzgj__tfrc.name]
            new_body.append(qgn__pshd)
        tjbn__bzxf.body = new_body
    return func_ir


def _call_function_ex_replace_kws_small(keyword_expr, new_body, buildmap_idx):
    dofev__bwkiu = keyword_expr.items.copy()
    turj__hokv = keyword_expr.value_indexes
    for ydfx__tuxmk, sqxg__fnoh in turj__hokv.items():
        dofev__bwkiu[sqxg__fnoh] = ydfx__tuxmk, dofev__bwkiu[sqxg__fnoh][1]
    new_body[buildmap_idx] = None
    return dofev__bwkiu


def _call_function_ex_replace_kws_large(body, buildmap_name, buildmap_idx,
    search_end, new_body):
    dwopw__qavb = 'CALL_FUNCTION_EX with **kwargs not supported'
    new_body[buildmap_idx] = None
    dofev__bwkiu = []
    por__uqm = buildmap_idx + 1
    while por__uqm <= search_end:
        wkn__lqisp = body[por__uqm]
        if not (isinstance(wkn__lqisp, ir.Assign) and isinstance(wkn__lqisp
            .value, ir.Const)):
            raise UnsupportedError(dwopw__qavb)
        cql__qzwl = wkn__lqisp.target.name
        maas__nhowm = wkn__lqisp.value.value
        por__uqm += 1
        tqma__qnu = True
        while por__uqm <= search_end and tqma__qnu:
            qxtjj__jaiq = body[por__uqm]
            if (isinstance(qxtjj__jaiq, ir.Assign) and isinstance(
                qxtjj__jaiq.value, ir.Expr) and qxtjj__jaiq.value.op ==
                'getattr' and qxtjj__jaiq.value.value.name == buildmap_name and
                qxtjj__jaiq.value.attr == '__setitem__'):
                tqma__qnu = False
            else:
                por__uqm += 1
        if tqma__qnu or por__uqm == search_end:
            raise UnsupportedError(dwopw__qavb)
        emjo__bbizd = body[por__uqm + 1]
        if not (isinstance(emjo__bbizd, ir.Assign) and isinstance(
            emjo__bbizd.value, ir.Expr) and emjo__bbizd.value.op == 'call' and
            emjo__bbizd.value.func.name == qxtjj__jaiq.target.name and len(
            emjo__bbizd.value.args) == 2 and emjo__bbizd.value.args[0].name ==
            cql__qzwl):
            raise UnsupportedError(dwopw__qavb)
        tme__sqc = emjo__bbizd.value.args[1]
        dofev__bwkiu.append((maas__nhowm, tme__sqc))
        new_body[por__uqm] = None
        new_body[por__uqm + 1] = None
        por__uqm += 2
    return dofev__bwkiu


def _call_function_ex_replace_args_small(tuple_expr, new_body, buildtuple_idx):
    new_body[buildtuple_idx] = None
    return tuple_expr.items


def _call_function_ex_replace_args_large(vararg_stmt, body, new_body,
    search_end):
    dwopw__qavb = 'CALL_FUNCTION_EX with **kwargs not supported'
    por__uqm = 0
    umk__bawng = []
    if isinstance(vararg_stmt, ir.Assign) and isinstance(vararg_stmt.value,
        ir.Var):
        qgpq__deeoj = vararg_stmt.value.name
        new_body[search_end] = None
        search_end -= 1
    else:
        qgpq__deeoj = vararg_stmt.target.name
    eaxqt__fio = True
    while search_end >= por__uqm and eaxqt__fio:
        nylfr__jeaae = body[search_end]
        if (isinstance(nylfr__jeaae, ir.Assign) and nylfr__jeaae.target.
            name == qgpq__deeoj and isinstance(nylfr__jeaae.value, ir.Expr) and
            nylfr__jeaae.value.op == 'build_tuple' and not nylfr__jeaae.
            value.items):
            eaxqt__fio = False
            new_body[search_end] = None
        else:
            if search_end == por__uqm or not (isinstance(nylfr__jeaae, ir.
                Assign) and nylfr__jeaae.target.name == qgpq__deeoj and
                isinstance(nylfr__jeaae.value, ir.Expr) and nylfr__jeaae.
                value.op == 'binop' and nylfr__jeaae.value.fn == operator.add):
                raise UnsupportedError(dwopw__qavb)
            jlat__dmdo = nylfr__jeaae.value.lhs.name
            pxb__weu = nylfr__jeaae.value.rhs.name
            bvmc__mii = body[search_end - 1]
            if not (isinstance(bvmc__mii, ir.Assign) and isinstance(
                bvmc__mii.value, ir.Expr) and bvmc__mii.value.op ==
                'build_tuple' and len(bvmc__mii.value.items) == 1):
                raise UnsupportedError(dwopw__qavb)
            if bvmc__mii.target.name == jlat__dmdo:
                qgpq__deeoj = pxb__weu
            elif bvmc__mii.target.name == pxb__weu:
                qgpq__deeoj = jlat__dmdo
            else:
                raise UnsupportedError(dwopw__qavb)
            umk__bawng.append(bvmc__mii.value.items[0])
            new_body[search_end] = None
            new_body[search_end - 1] = None
            search_end -= 2
            tjham__erxnf = True
            while search_end >= por__uqm and tjham__erxnf:
                npl__hynrv = body[search_end]
                if isinstance(npl__hynrv, ir.Assign
                    ) and npl__hynrv.target.name == qgpq__deeoj:
                    tjham__erxnf = False
                else:
                    search_end -= 1
    if eaxqt__fio:
        raise UnsupportedError(dwopw__qavb)
    return umk__bawng[::-1]


def peep_hole_call_function_ex_to_call_function_kw(func_ir):
    dwopw__qavb = 'CALL_FUNCTION_EX with **kwargs not supported'
    for tjbn__bzxf in func_ir.blocks.values():
        tfhi__kfy = False
        new_body = []
        for dhpf__csrxy, qgn__pshd in enumerate(tjbn__bzxf.body):
            if (isinstance(qgn__pshd, ir.Assign) and isinstance(qgn__pshd.
                value, ir.Expr) and qgn__pshd.value.op == 'call' and 
                qgn__pshd.value.varkwarg is not None):
                tfhi__kfy = True
                ylesk__rstxs = qgn__pshd.value
                args = ylesk__rstxs.args
                dofev__bwkiu = ylesk__rstxs.kws
                vcsj__mftt = ylesk__rstxs.vararg
                dtm__ymebg = ylesk__rstxs.varkwarg
                ozw__srnmc = dhpf__csrxy - 1
                avq__ywxnc = ozw__srnmc
                wktpf__fzj = None
                yyk__nlqq = True
                while avq__ywxnc >= 0 and yyk__nlqq:
                    wktpf__fzj = tjbn__bzxf.body[avq__ywxnc]
                    if isinstance(wktpf__fzj, ir.Assign
                        ) and wktpf__fzj.target.name == dtm__ymebg.name:
                        yyk__nlqq = False
                    else:
                        avq__ywxnc -= 1
                if dofev__bwkiu or yyk__nlqq or not (isinstance(wktpf__fzj.
                    value, ir.Expr) and wktpf__fzj.value.op == 'build_map'):
                    raise UnsupportedError(dwopw__qavb)
                if wktpf__fzj.value.items:
                    dofev__bwkiu = _call_function_ex_replace_kws_small(
                        wktpf__fzj.value, new_body, avq__ywxnc)
                else:
                    dofev__bwkiu = _call_function_ex_replace_kws_large(
                        tjbn__bzxf.body, dtm__ymebg.name, avq__ywxnc, 
                        dhpf__csrxy - 1, new_body)
                ozw__srnmc = avq__ywxnc
                if vcsj__mftt is not None:
                    if args:
                        raise UnsupportedError(dwopw__qavb)
                    gsmnh__tfr = ozw__srnmc
                    ajns__ivu = None
                    yyk__nlqq = True
                    while gsmnh__tfr >= 0 and yyk__nlqq:
                        ajns__ivu = tjbn__bzxf.body[gsmnh__tfr]
                        if isinstance(ajns__ivu, ir.Assign
                            ) and ajns__ivu.target.name == vcsj__mftt.name:
                            yyk__nlqq = False
                        else:
                            gsmnh__tfr -= 1
                    if yyk__nlqq:
                        raise UnsupportedError(dwopw__qavb)
                    if isinstance(ajns__ivu.value, ir.Expr
                        ) and ajns__ivu.value.op == 'build_tuple':
                        args = _call_function_ex_replace_args_small(ajns__ivu
                            .value, new_body, gsmnh__tfr)
                    else:
                        args = _call_function_ex_replace_args_large(ajns__ivu,
                            tjbn__bzxf.body, new_body, gsmnh__tfr)
                mtf__bwwyz = ir.Expr.call(ylesk__rstxs.func, args,
                    dofev__bwkiu, ylesk__rstxs.loc, target=ylesk__rstxs.target)
                if qgn__pshd.target.name in func_ir._definitions and len(
                    func_ir._definitions[qgn__pshd.target.name]) == 1:
                    func_ir._definitions[qgn__pshd.target.name].clear()
                func_ir._definitions[qgn__pshd.target.name].append(mtf__bwwyz)
                qgn__pshd = ir.Assign(mtf__bwwyz, qgn__pshd.target,
                    qgn__pshd.loc)
            new_body.append(qgn__pshd)
        if tfhi__kfy:
            tjbn__bzxf.body = [tcsuf__jjqdx for tcsuf__jjqdx in new_body if
                tcsuf__jjqdx is not None]
    return func_ir


def peep_hole_fuse_dict_add_updates(func_ir):
    for tjbn__bzxf in func_ir.blocks.values():
        new_body = []
        lit_old_idx = {}
        lit_new_idx = {}
        map_updates = {}
        tfhi__kfy = False
        for dhpf__csrxy, qgn__pshd in enumerate(tjbn__bzxf.body):
            oxs__ovjz = True
            acpob__ajx = None
            if isinstance(qgn__pshd, ir.Assign) and isinstance(qgn__pshd.
                value, ir.Expr):
                if qgn__pshd.value.op == 'build_map':
                    acpob__ajx = qgn__pshd.target.name
                    lit_old_idx[qgn__pshd.target.name] = dhpf__csrxy
                    lit_new_idx[qgn__pshd.target.name] = dhpf__csrxy
                    map_updates[qgn__pshd.target.name
                        ] = qgn__pshd.value.items.copy()
                    oxs__ovjz = False
                elif qgn__pshd.value.op == 'call' and dhpf__csrxy > 0:
                    zwvi__jvw = qgn__pshd.value.func.name
                    qxtjj__jaiq = tjbn__bzxf.body[dhpf__csrxy - 1]
                    args = qgn__pshd.value.args
                    if (isinstance(qxtjj__jaiq, ir.Assign) and qxtjj__jaiq.
                        target.name == zwvi__jvw and isinstance(qxtjj__jaiq
                        .value, ir.Expr) and qxtjj__jaiq.value.op ==
                        'getattr' and qxtjj__jaiq.value.value.name in
                        lit_old_idx):
                        utlg__deb = qxtjj__jaiq.value.value.name
                        didu__azqh = qxtjj__jaiq.value.attr
                        if didu__azqh == '__setitem__':
                            oxs__ovjz = False
                            map_updates[utlg__deb].append(args)
                            new_body[-1] = None
                        elif didu__azqh == 'update' and args[0
                            ].name in lit_old_idx:
                            oxs__ovjz = False
                            map_updates[utlg__deb].extend(map_updates[args[
                                0].name])
                            new_body[-1] = None
                        if not oxs__ovjz:
                            lit_new_idx[utlg__deb] = dhpf__csrxy
                            func_ir._definitions[qxtjj__jaiq.target.name
                                ].remove(qxtjj__jaiq.value)
            if not (isinstance(qgn__pshd, ir.Assign) and isinstance(
                qgn__pshd.value, ir.Expr) and qgn__pshd.value.op ==
                'getattr' and qgn__pshd.value.value.name in lit_old_idx and
                qgn__pshd.value.attr in ('__setitem__', 'update')):
                for hzgj__tfrc in qgn__pshd.list_vars():
                    if (hzgj__tfrc.name in lit_old_idx and hzgj__tfrc.name !=
                        acpob__ajx):
                        _insert_build_map(func_ir, hzgj__tfrc.name,
                            tjbn__bzxf.body, new_body, lit_old_idx,
                            lit_new_idx, map_updates)
            if oxs__ovjz:
                new_body.append(qgn__pshd)
            else:
                func_ir._definitions[qgn__pshd.target.name].remove(qgn__pshd
                    .value)
                tfhi__kfy = True
                new_body.append(None)
        ubvi__xeia = list(lit_old_idx.keys())
        for ybl__pmhym in ubvi__xeia:
            _insert_build_map(func_ir, ybl__pmhym, tjbn__bzxf.body,
                new_body, lit_old_idx, lit_new_idx, map_updates)
        if tfhi__kfy:
            tjbn__bzxf.body = [tcsuf__jjqdx for tcsuf__jjqdx in new_body if
                tcsuf__jjqdx is not None]
    return func_ir


def _insert_build_map(func_ir, name, old_body, new_body, lit_old_idx,
    lit_new_idx, map_updates):
    vknw__svh = lit_old_idx[name]
    yrpel__wautw = lit_new_idx[name]
    hru__phljj = map_updates[name]
    new_body[yrpel__wautw] = _build_new_build_map(func_ir, name, old_body,
        vknw__svh, hru__phljj)
    del lit_old_idx[name]
    del lit_new_idx[name]
    del map_updates[name]


def _build_new_build_map(func_ir, name, old_body, old_lineno, new_items):
    marh__bstrg = old_body[old_lineno]
    dvm__rfjr = marh__bstrg.target
    bsn__wnepd = marh__bstrg.value
    vixlm__rdavr = []
    eva__esz = []
    for spay__xjtvv in new_items:
        esm__rph, ikjw__wyv = spay__xjtvv
        rvxi__puout = guard(get_definition, func_ir, esm__rph)
        if isinstance(rvxi__puout, (ir.Const, ir.Global, ir.FreeVar)):
            vixlm__rdavr.append(rvxi__puout.value)
        nzcx__wyqdt = guard(get_definition, func_ir, ikjw__wyv)
        if isinstance(nzcx__wyqdt, (ir.Const, ir.Global, ir.FreeVar)):
            eva__esz.append(nzcx__wyqdt.value)
        else:
            eva__esz.append(numba.core.interpreter._UNKNOWN_VALUE(ikjw__wyv
                .name))
    turj__hokv = {}
    if len(vixlm__rdavr) == len(new_items):
        qbhak__tflpv = {tcsuf__jjqdx: lxr__zkjpi for tcsuf__jjqdx,
            lxr__zkjpi in zip(vixlm__rdavr, eva__esz)}
        for dhpf__csrxy, esm__rph in enumerate(vixlm__rdavr):
            turj__hokv[esm__rph] = dhpf__csrxy
    else:
        qbhak__tflpv = None
    xal__moorp = ir.Expr.build_map(items=new_items, size=len(new_items),
        literal_value=qbhak__tflpv, value_indexes=turj__hokv, loc=
        bsn__wnepd.loc)
    func_ir._definitions[name].append(xal__moorp)
    return ir.Assign(xal__moorp, ir.Var(dvm__rfjr.scope, name, dvm__rfjr.
        loc), xal__moorp.loc)
