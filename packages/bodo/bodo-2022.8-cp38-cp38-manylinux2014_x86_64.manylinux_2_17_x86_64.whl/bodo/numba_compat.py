"""
Numba monkey patches to fix issues related to Bodo. Should be imported before any
other module in bodo package.
"""
import copy
import functools
import hashlib
import inspect
import itertools
import operator
import os
import re
import sys
import textwrap
import traceback
import types as pytypes
import warnings
from collections import OrderedDict
from collections.abc import Sequence
from contextlib import ExitStack
import numba
import numba.core.boxing
import numba.core.inline_closurecall
import numba.core.typing.listdecl
import numba.np.linalg
from numba.core import analysis, cgutils, errors, ir, ir_utils, types
from numba.core.compiler import Compiler
from numba.core.errors import ForceLiteralArg, LiteralTypingError, TypingError
from numba.core.ir_utils import GuardException, _create_function_from_code_obj, analysis, build_definitions, find_callname, get_definition, guard, has_no_side_effect, mk_unique_var, remove_dead_extensions, replace_vars_inner, require, visit_vars_extensions, visit_vars_inner
from numba.core.types import literal
from numba.core.types.functions import _bt_as_lines, _ResolutionFailures, _termcolor, _unlit_non_poison
from numba.core.typing.templates import AbstractTemplate, Signature, _EmptyImplementationEntry, _inline_info, _OverloadAttributeTemplate, infer_global, signature
from numba.core.typing.typeof import Purpose, typeof
from numba.experimental.jitclass import base as jitclass_base
from numba.experimental.jitclass import decorators as jitclass_decorators
from numba.extending import NativeValue, lower_builtin, typeof_impl
from numba.parfors.parfor import get_expr_args
from bodo.utils.python_310_bytecode_pass import Bodo310ByteCodePass, peep_hole_call_function_ex_to_call_function_kw, peep_hole_fuse_dict_add_updates, peep_hole_fuse_tuple_adds
from bodo.utils.typing import BodoError, get_overload_const_str, is_overload_constant_str, raise_bodo_error
_check_numba_change = False
numba.core.typing.templates._IntrinsicTemplate.prefer_literal = True


def run_frontend(func, inline_closures=False, emit_dels=False):
    from numba.core.utils import PYVERSION
    fmus__xuah = numba.core.bytecode.FunctionIdentity.from_function(func)
    skheq__hnzyl = numba.core.interpreter.Interpreter(fmus__xuah)
    qfw__mzuo = numba.core.bytecode.ByteCode(func_id=fmus__xuah)
    func_ir = skheq__hnzyl.interpret(qfw__mzuo)
    if PYVERSION == (3, 10):
        func_ir = peep_hole_call_function_ex_to_call_function_kw(func_ir)
        func_ir = peep_hole_fuse_dict_add_updates(func_ir)
        func_ir = peep_hole_fuse_tuple_adds(func_ir)
    if inline_closures:
        from numba.core.inline_closurecall import InlineClosureCallPass


        class DummyPipeline:

            def __init__(self, f_ir):
                self.state = numba.core.compiler.StateDict()
                self.state.typingctx = None
                self.state.targetctx = None
                self.state.args = None
                self.state.func_ir = f_ir
                self.state.typemap = None
                self.state.return_type = None
                self.state.calltypes = None
        numba.core.rewrites.rewrite_registry.apply('before-inference',
            DummyPipeline(func_ir).state)
        jkm__dwnz = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        jkm__dwnz.run()
    aqnk__jok = numba.core.postproc.PostProcessor(func_ir)
    aqnk__jok.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, nymxr__ekktz in visit_vars_extensions.items():
        if isinstance(stmt, t):
            nymxr__ekktz(stmt, callback, cbdata)
            return
    if isinstance(stmt, ir.Assign):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Arg):
        stmt.name = visit_vars_inner(stmt.name, callback, cbdata)
    elif isinstance(stmt, ir.Return):
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Raise):
        stmt.exception = visit_vars_inner(stmt.exception, callback, cbdata)
    elif isinstance(stmt, ir.Branch):
        stmt.cond = visit_vars_inner(stmt.cond, callback, cbdata)
    elif isinstance(stmt, ir.Jump):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
    elif isinstance(stmt, ir.Del):
        var = ir.Var(None, stmt.value, stmt.loc)
        var = visit_vars_inner(var, callback, cbdata)
        stmt.value = var.name
    elif isinstance(stmt, ir.DelAttr):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.attr = visit_vars_inner(stmt.attr, callback, cbdata)
    elif isinstance(stmt, ir.SetAttr):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.attr = visit_vars_inner(stmt.attr, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.DelItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index = visit_vars_inner(stmt.index, callback, cbdata)
    elif isinstance(stmt, ir.StaticSetItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index_var = visit_vars_inner(stmt.index_var, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.SetItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index = visit_vars_inner(stmt.index, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Print):
        stmt.args = [visit_vars_inner(x, callback, cbdata) for x in stmt.args]
        stmt.vararg = visit_vars_inner(stmt.vararg, callback, cbdata)
    else:
        pass
    return


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.visit_vars_stmt)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '52b7b645ba65c35f3cf564f936e113261db16a2dff1e80fbee2459af58844117':
        warnings.warn('numba.core.ir_utils.visit_vars_stmt has changed')
numba.core.ir_utils.visit_vars_stmt = visit_vars_stmt
old_run_pass = numba.core.typed_passes.InlineOverloads.run_pass


def InlineOverloads_run_pass(self, state):
    import bodo
    bodo.compiler.bodo_overload_inline_pass(state.func_ir, state.typingctx,
        state.targetctx, state.typemap, state.calltypes)
    return old_run_pass(self, state)


numba.core.typed_passes.InlineOverloads.run_pass = InlineOverloads_run_pass
from numba.core.ir_utils import _add_alias, alias_analysis_extensions, alias_func_extensions
_immutable_type_class = (types.Number, types.scalars._NPDatetimeBase, types
    .iterators.RangeType, types.UnicodeType)


def is_immutable_type(var, typemap):
    if typemap is None or var not in typemap:
        return False
    typ = typemap[var]
    if isinstance(typ, _immutable_type_class):
        return True
    if isinstance(typ, types.BaseTuple) and all(isinstance(t,
        _immutable_type_class) for t in typ.types):
        return True
    return False


def find_potential_aliases(blocks, args, typemap, func_ir, alias_map=None,
    arg_aliases=None):
    if alias_map is None:
        alias_map = {}
    if arg_aliases is None:
        arg_aliases = set(a for a in args if not is_immutable_type(a, typemap))
    func_ir._definitions = build_definitions(func_ir.blocks)
    bek__wtgkr = ['ravel', 'transpose', 'reshape']
    for juotj__wto in blocks.values():
        for zar__npua in juotj__wto.body:
            if type(zar__npua) in alias_analysis_extensions:
                nymxr__ekktz = alias_analysis_extensions[type(zar__npua)]
                nymxr__ekktz(zar__npua, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(zar__npua, ir.Assign):
                vxi__gcf = zar__npua.value
                ijcu__zuhlc = zar__npua.target.name
                if is_immutable_type(ijcu__zuhlc, typemap):
                    continue
                if isinstance(vxi__gcf, ir.Var
                    ) and ijcu__zuhlc != vxi__gcf.name:
                    _add_alias(ijcu__zuhlc, vxi__gcf.name, alias_map,
                        arg_aliases)
                if isinstance(vxi__gcf, ir.Expr) and (vxi__gcf.op == 'cast' or
                    vxi__gcf.op in ['getitem', 'static_getitem']):
                    _add_alias(ijcu__zuhlc, vxi__gcf.value.name, alias_map,
                        arg_aliases)
                if isinstance(vxi__gcf, ir.Expr
                    ) and vxi__gcf.op == 'inplace_binop':
                    _add_alias(ijcu__zuhlc, vxi__gcf.lhs.name, alias_map,
                        arg_aliases)
                if isinstance(vxi__gcf, ir.Expr
                    ) and vxi__gcf.op == 'getattr' and vxi__gcf.attr in ['T',
                    'ctypes', 'flat']:
                    _add_alias(ijcu__zuhlc, vxi__gcf.value.name, alias_map,
                        arg_aliases)
                if isinstance(vxi__gcf, ir.Expr
                    ) and vxi__gcf.op == 'getattr' and vxi__gcf.attr not in [
                    'shape'] and vxi__gcf.value.name in arg_aliases:
                    _add_alias(ijcu__zuhlc, vxi__gcf.value.name, alias_map,
                        arg_aliases)
                if isinstance(vxi__gcf, ir.Expr
                    ) and vxi__gcf.op == 'getattr' and vxi__gcf.attr in ('loc',
                    'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(ijcu__zuhlc, vxi__gcf.value.name, alias_map,
                        arg_aliases)
                if isinstance(vxi__gcf, ir.Expr) and vxi__gcf.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(ijcu__zuhlc, typemap):
                    for ssho__wfokk in vxi__gcf.items:
                        _add_alias(ijcu__zuhlc, ssho__wfokk.name, alias_map,
                            arg_aliases)
                if isinstance(vxi__gcf, ir.Expr) and vxi__gcf.op == 'call':
                    ofi__rhs = guard(find_callname, func_ir, vxi__gcf, typemap)
                    if ofi__rhs is None:
                        continue
                    rdwiq__izgt, nldmc__guvh = ofi__rhs
                    if ofi__rhs in alias_func_extensions:
                        oqor__sozuh = alias_func_extensions[ofi__rhs]
                        oqor__sozuh(ijcu__zuhlc, vxi__gcf.args, alias_map,
                            arg_aliases)
                    if nldmc__guvh == 'numpy' and rdwiq__izgt in bek__wtgkr:
                        _add_alias(ijcu__zuhlc, vxi__gcf.args[0].name,
                            alias_map, arg_aliases)
                    if isinstance(nldmc__guvh, ir.Var
                        ) and rdwiq__izgt in bek__wtgkr:
                        _add_alias(ijcu__zuhlc, nldmc__guvh.name, alias_map,
                            arg_aliases)
    pouh__kvyey = copy.deepcopy(alias_map)
    for ssho__wfokk in pouh__kvyey:
        for jgpr__pxbi in pouh__kvyey[ssho__wfokk]:
            alias_map[ssho__wfokk] |= alias_map[jgpr__pxbi]
        for jgpr__pxbi in pouh__kvyey[ssho__wfokk]:
            alias_map[jgpr__pxbi] = alias_map[ssho__wfokk]
    return alias_map, arg_aliases


if _check_numba_change:
    lines = inspect.getsource(ir_utils.find_potential_aliases)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'e6cf3e0f502f903453eb98346fc6854f87dc4ea1ac62f65c2d6aef3bf690b6c5':
        warnings.warn('ir_utils.find_potential_aliases has changed')
ir_utils.find_potential_aliases = find_potential_aliases
numba.parfors.array_analysis.find_potential_aliases = find_potential_aliases
if _check_numba_change:
    lines = inspect.getsource(ir_utils.dead_code_elimination)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '40a8626300a1a17523944ec7842b093c91258bbc60844bbd72191a35a4c366bf':
        warnings.warn('ir_utils.dead_code_elimination has changed')


def mini_dce(func_ir, typemap=None, alias_map=None, arg_aliases=None):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    rdf__vljky = compute_cfg_from_blocks(func_ir.blocks)
    rpu__uyfy = compute_use_defs(func_ir.blocks)
    vva__hrd = compute_live_map(rdf__vljky, func_ir.blocks, rpu__uyfy.
        usemap, rpu__uyfy.defmap)
    otru__omn = True
    while otru__omn:
        otru__omn = False
        for label, block in func_ir.blocks.items():
            lives = {ssho__wfokk.name for ssho__wfokk in block.terminator.
                list_vars()}
            for ygx__wzs, fqjz__buzx in rdf__vljky.successors(label):
                lives |= vva__hrd[ygx__wzs]
            nwx__hhf = [block.terminator]
            for stmt in reversed(block.body[:-1]):
                if isinstance(stmt, ir.Assign):
                    ijcu__zuhlc = stmt.target
                    xokam__bbrce = stmt.value
                    if ijcu__zuhlc.name not in lives:
                        if isinstance(xokam__bbrce, ir.Expr
                            ) and xokam__bbrce.op == 'make_function':
                            continue
                        if isinstance(xokam__bbrce, ir.Expr
                            ) and xokam__bbrce.op == 'getattr':
                            continue
                        if isinstance(xokam__bbrce, ir.Const):
                            continue
                        if typemap and isinstance(typemap.get(ijcu__zuhlc,
                            None), types.Function):
                            continue
                        if isinstance(xokam__bbrce, ir.Expr
                            ) and xokam__bbrce.op == 'build_map':
                            continue
                        if isinstance(xokam__bbrce, ir.Expr
                            ) and xokam__bbrce.op == 'build_tuple':
                            continue
                    if isinstance(xokam__bbrce, ir.Var
                        ) and ijcu__zuhlc.name == xokam__bbrce.name:
                        continue
                if isinstance(stmt, ir.Del):
                    if stmt.value not in lives:
                        continue
                if type(stmt) in analysis.ir_extension_usedefs:
                    jyna__nhazp = analysis.ir_extension_usedefs[type(stmt)]
                    kymf__mzq, drmpa__nvqw = jyna__nhazp(stmt)
                    lives -= drmpa__nvqw
                    lives |= kymf__mzq
                else:
                    lives |= {ssho__wfokk.name for ssho__wfokk in stmt.
                        list_vars()}
                    if isinstance(stmt, ir.Assign):
                        lives.remove(ijcu__zuhlc.name)
                nwx__hhf.append(stmt)
            nwx__hhf.reverse()
            if len(block.body) != len(nwx__hhf):
                otru__omn = True
            block.body = nwx__hhf


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    oubrs__wuqj = getattr(func, '__name__', str(func))
    name = 'OverloadTemplate_%s' % (oubrs__wuqj,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    nlza__gqmtr = dict(key=func, _overload_func=staticmethod(overload_func),
        _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(name, (base,), nlza__gqmtr)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        make_overload_template)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '7f6974584cb10e49995b652827540cc6732e497c0b9f8231b44fd83fcc1c0a83':
        warnings.warn(
            'numba.core.typing.templates.make_overload_template has changed')
numba.core.typing.templates.make_overload_template = make_overload_template


def _resolve(self, typ, attr):
    if self._attr != attr:
        return None
    if isinstance(typ, types.TypeRef):
        assert typ == self.key
    else:
        assert isinstance(typ, self.key)


    class MethodTemplate(AbstractTemplate):
        key = self.key, attr
        _inline = self._inline
        _no_unliteral = getattr(self, '_no_unliteral', False)
        _overload_func = staticmethod(self._overload_func)
        _inline_overloads = self._inline_overloads
        prefer_literal = self.prefer_literal

        def generic(_, args, kws):
            args = (typ,) + tuple(args)
            fnty = self._get_function_type(self.context, typ)
            sig = self._get_signature(self.context, fnty, args, kws)
            sig = sig.replace(pysig=numba.core.utils.pysignature(self.
                _overload_func))
            for mqy__hyfyb in fnty.templates:
                self._inline_overloads.update(mqy__hyfyb._inline_overloads)
            if sig is not None:
                return sig.as_method()
    return types.BoundFunction(MethodTemplate, typ)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadMethodTemplate._resolve)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'ce8e0935dc939d0867ef969e1ed2975adb3533a58a4133fcc90ae13c4418e4d6':
        warnings.warn(
            'numba.core.typing.templates._OverloadMethodTemplate._resolve has changed'
            )
numba.core.typing.templates._OverloadMethodTemplate._resolve = _resolve


def make_overload_attribute_template(typ, attr, overload_func, inline,
    prefer_literal=False, base=_OverloadAttributeTemplate, **kwargs):
    assert isinstance(typ, types.Type) or issubclass(typ, types.Type)
    name = 'OverloadAttributeTemplate_%s_%s' % (typ, attr)
    no_unliteral = kwargs.pop('no_unliteral', False)
    nlza__gqmtr = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(name, (base,), nlza__gqmtr)
    return obj


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        make_overload_attribute_template)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f066c38c482d6cf8bf5735a529c3264118ba9b52264b24e58aad12a6b1960f5d':
        warnings.warn(
            'numba.core.typing.templates.make_overload_attribute_template has changed'
            )
numba.core.typing.templates.make_overload_attribute_template = (
    make_overload_attribute_template)


def generic(self, args, kws):
    from numba.core.typed_passes import PreLowerStripPhis
    lhrq__acswx, tpa__twaki = self._get_impl(args, kws)
    if lhrq__acswx is None:
        return
    mabo__gtfub = types.Dispatcher(lhrq__acswx)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        sfyg__ial = lhrq__acswx._compiler
        flags = compiler.Flags()
        nov__yrfql = sfyg__ial.targetdescr.typing_context
        fole__xaldq = sfyg__ial.targetdescr.target_context
        wmjv__yqer = sfyg__ial.pipeline_class(nov__yrfql, fole__xaldq, None,
            None, None, flags, None)
        wmcvg__qcl = InlineWorker(nov__yrfql, fole__xaldq, sfyg__ial.locals,
            wmjv__yqer, flags, None)
        ftd__xivj = mabo__gtfub.dispatcher.get_call_template
        mqy__hyfyb, eahx__ywr, gce__iyjnd, kws = ftd__xivj(tpa__twaki, kws)
        if gce__iyjnd in self._inline_overloads:
            return self._inline_overloads[gce__iyjnd]['iinfo'].signature
        ir = wmcvg__qcl.run_untyped_passes(mabo__gtfub.dispatcher.py_func,
            enable_ssa=True)
        typemap, return_type, calltypes, _ = typed_passes.type_inference_stage(
            self.context, fole__xaldq, ir, gce__iyjnd, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(return_type, gce__iyjnd, None)
        self._inline_overloads[sig.args] = {'folded_args': gce__iyjnd}
        iggk__xfmw = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = iggk__xfmw
        if not self._inline.is_always_inline:
            sig = mabo__gtfub.get_call_type(self.context, tpa__twaki, kws)
            self._compiled_overloads[sig.args] = mabo__gtfub.get_overload(sig)
        ezb__sae = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': gce__iyjnd,
            'iinfo': ezb__sae}
    else:
        sig = mabo__gtfub.get_call_type(self.context, tpa__twaki, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = mabo__gtfub.get_overload(sig)
    return sig


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadFunctionTemplate.generic)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5d453a6d0215ebf0bab1279ff59eb0040b34938623be99142ce20acc09cdeb64':
        warnings.warn(
            'numba.core.typing.templates._OverloadFunctionTemplate.generic has changed'
            )
numba.core.typing.templates._OverloadFunctionTemplate.generic = generic


def bound_function(template_key, no_unliteral=False):

    def wrapper(method_resolver):

        @functools.wraps(method_resolver)
        def attribute_resolver(self, ty):


            class MethodTemplate(AbstractTemplate):
                key = template_key

                def generic(_, args, kws):
                    sig = method_resolver(self, ty, args, kws)
                    if sig is not None and sig.recvr is None:
                        sig = sig.replace(recvr=ty)
                    return sig
            MethodTemplate._no_unliteral = no_unliteral
            return types.BoundFunction(MethodTemplate, ty)
        return attribute_resolver
    return wrapper


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.bound_function)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a2feefe64eae6a15c56affc47bf0c1d04461f9566913442d539452b397103322':
        warnings.warn('numba.core.typing.templates.bound_function has changed')
numba.core.typing.templates.bound_function = bound_function


def get_call_type(self, context, args, kws):
    from numba.core import utils
    nktr__xexap = [True, False]
    scpk__nczfl = [False, True]
    qanwk__kdek = _ResolutionFailures(context, self, args, kws, depth=self.
        _depth)
    from numba.core.target_extension import get_local_target
    kqna__uagy = get_local_target(context)
    utr__cqwg = utils.order_by_target_specificity(kqna__uagy, self.
        templates, fnkey=self.key[0])
    self._depth += 1
    for oisap__gbovg in utr__cqwg:
        wqah__thsw = oisap__gbovg(context)
        rpl__xfzip = nktr__xexap if wqah__thsw.prefer_literal else scpk__nczfl
        rpl__xfzip = [True] if getattr(wqah__thsw, '_no_unliteral', False
            ) else rpl__xfzip
        for myz__pca in rpl__xfzip:
            try:
                if myz__pca:
                    sig = wqah__thsw.apply(args, kws)
                else:
                    bkme__rsi = tuple([_unlit_non_poison(a) for a in args])
                    mkupf__uzn = {ikm__tie: _unlit_non_poison(ssho__wfokk) for
                        ikm__tie, ssho__wfokk in kws.items()}
                    sig = wqah__thsw.apply(bkme__rsi, mkupf__uzn)
            except Exception as e:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                else:
                    sig = None
                    qanwk__kdek.add_error(wqah__thsw, False, e, myz__pca)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = wqah__thsw.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    qzj__ljsib = getattr(wqah__thsw, 'cases', None)
                    if qzj__ljsib is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            qzj__ljsib)
                    else:
                        msg = 'No match.'
                    qanwk__kdek.add_error(wqah__thsw, True, msg, myz__pca)
    qanwk__kdek.raise_error()


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.BaseFunction.
        get_call_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '25f038a7216f8e6f40068ea81e11fd9af8ad25d19888f7304a549941b01b7015':
        warnings.warn(
            'numba.core.types.functions.BaseFunction.get_call_type has changed'
            )
numba.core.types.functions.BaseFunction.get_call_type = get_call_type
bodo_typing_error_info = """
This is often caused by the use of unsupported features or typing issues.
See https://docs.bodo.ai/
"""


def get_call_type2(self, context, args, kws):
    mqy__hyfyb = self.template(context)
    gqd__vrwg = None
    flysf__zdb = None
    nuz__zgt = None
    rpl__xfzip = [True, False] if mqy__hyfyb.prefer_literal else [False, True]
    rpl__xfzip = [True] if getattr(mqy__hyfyb, '_no_unliteral', False
        ) else rpl__xfzip
    for myz__pca in rpl__xfzip:
        if myz__pca:
            try:
                nuz__zgt = mqy__hyfyb.apply(args, kws)
            except Exception as iksx__qoxy:
                if isinstance(iksx__qoxy, errors.ForceLiteralArg):
                    raise iksx__qoxy
                gqd__vrwg = iksx__qoxy
                nuz__zgt = None
            else:
                break
        else:
            niuqt__yic = tuple([_unlit_non_poison(a) for a in args])
            mzzsg__fsr = {ikm__tie: _unlit_non_poison(ssho__wfokk) for 
                ikm__tie, ssho__wfokk in kws.items()}
            cbnmt__guh = niuqt__yic == args and kws == mzzsg__fsr
            if not cbnmt__guh and nuz__zgt is None:
                try:
                    nuz__zgt = mqy__hyfyb.apply(niuqt__yic, mzzsg__fsr)
                except Exception as iksx__qoxy:
                    from numba.core import utils
                    if utils.use_new_style_errors() and not isinstance(
                        iksx__qoxy, errors.NumbaError):
                        raise iksx__qoxy
                    if isinstance(iksx__qoxy, errors.ForceLiteralArg):
                        if mqy__hyfyb.prefer_literal:
                            raise iksx__qoxy
                    flysf__zdb = iksx__qoxy
                else:
                    break
    if nuz__zgt is None and (flysf__zdb is not None or gqd__vrwg is not None):
        osinc__ylf = '- Resolution failure for {} arguments:\n{}\n'
        stgn__ulbne = _termcolor.highlight(osinc__ylf)
        if numba.core.config.DEVELOPER_MODE:
            fva__rlld = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    aye__wgort = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    aye__wgort = ['']
                ucc__uxyuj = '\n{}'.format(2 * fva__rlld)
                kcj__kvkyp = _termcolor.reset(ucc__uxyuj + ucc__uxyuj.join(
                    _bt_as_lines(aye__wgort)))
                return _termcolor.reset(kcj__kvkyp)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            mre__vqdj = str(e)
            mre__vqdj = mre__vqdj if mre__vqdj else str(repr(e)) + add_bt(e)
            qpi__guyba = errors.TypingError(textwrap.dedent(mre__vqdj))
            return stgn__ulbne.format(literalness, str(qpi__guyba))
        import bodo
        if isinstance(gqd__vrwg, bodo.utils.typing.BodoError):
            raise gqd__vrwg
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', gqd__vrwg) +
                nested_msg('non-literal', flysf__zdb))
        else:
            if 'missing a required argument' in gqd__vrwg.msg:
                msg = 'missing a required argument'
            else:
                msg = 'Compilation error for '
                if isinstance(self.this, bodo.hiframes.pd_dataframe_ext.
                    DataFrameType):
                    msg += 'DataFrame.'
                elif isinstance(self.this, bodo.hiframes.pd_series_ext.
                    SeriesType):
                    msg += 'Series.'
                msg += f'{self.typing_key[1]}().{bodo_typing_error_info}'
            raise errors.TypingError(msg, loc=gqd__vrwg.loc)
    return nuz__zgt


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.BoundFunction.
        get_call_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '502cd77c0084452e903a45a0f1f8107550bfbde7179363b57dabd617ce135f4a':
        warnings.warn(
            'numba.core.types.functions.BoundFunction.get_call_type has changed'
            )
numba.core.types.functions.BoundFunction.get_call_type = get_call_type2


def string_from_string_and_size(self, string, size):
    from llvmlite import ir as lir
    fnty = lir.FunctionType(self.pyobj, [self.cstring, self.py_ssize_t])
    rdwiq__izgt = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=rdwiq__izgt)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            ylxy__jkspn = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), ylxy__jkspn)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    rsi__ohpek = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            rsi__ohpek.append(types.Omitted(a.value))
        else:
            rsi__ohpek.append(self.typeof_pyval(a))
    akb__uqfr = None
    try:
        error = None
        akb__uqfr = self.compile(tuple(rsi__ohpek))
    except errors.ForceLiteralArg as e:
        kmi__brjb = [i for i in e.requested_args if isinstance(args[i],
            types.Literal) and not isinstance(args[i], types.LiteralStrKeyDict)
            ]
        if kmi__brjb:
            pldj__bgz = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            zxpd__bmfq = ', '.join('Arg #{} is {}'.format(i, args[i]) for i in
                sorted(kmi__brjb))
            raise errors.CompilerError(pldj__bgz.format(zxpd__bmfq))
        tpa__twaki = []
        try:
            for i, ssho__wfokk in enumerate(args):
                if i in e.requested_args:
                    if i in e.file_infos:
                        tpa__twaki.append(types.FilenameType(args[i], e.
                            file_infos[i]))
                    else:
                        tpa__twaki.append(types.literal(args[i]))
                else:
                    tpa__twaki.append(args[i])
            args = tpa__twaki
        except (OSError, FileNotFoundError) as jqhu__sxy:
            error = FileNotFoundError(str(jqhu__sxy) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                akb__uqfr = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        arj__zzkc = []
        for i, yfnd__ikqq in enumerate(args):
            val = yfnd__ikqq.value if isinstance(yfnd__ikqq, numba.core.
                dispatcher.OmittedArg) else yfnd__ikqq
            try:
                nosun__ghi = typeof(val, Purpose.argument)
            except ValueError as yxr__mrnb:
                arj__zzkc.append((i, str(yxr__mrnb)))
            else:
                if nosun__ghi is None:
                    arj__zzkc.append((i,
                        f'cannot determine Numba type of value {val}'))
        if arj__zzkc:
            lujzd__nlpzs = '\n'.join(f'- argument {i}: {tnjrj__xfn}' for i,
                tnjrj__xfn in arj__zzkc)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{lujzd__nlpzs}
"""
            e.patch_message(msg)
        if "Cannot determine Numba type of <class 'numpy.ufunc'>" in e.msg:
            msg = 'Unsupported Numpy ufunc encountered in JIT code'
            error = bodo.utils.typing.BodoError(msg, loc=e.loc)
        elif not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                acqq__aat = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'Failed at nopython',
                    'Overload', 'lowering']
                winn__plcw = False
                for lon__has in acqq__aat:
                    if lon__has in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        winn__plcw = True
                        break
                if not winn__plcw:
                    msg = f'{str(e)}'
                msg += '\n' + e.loc.strformat() + '\n'
                e.patch_message(msg)
        error_rewrite(e, 'typing')
    except errors.UnsupportedError as e:
        error_rewrite(e, 'unsupported_error')
    except (errors.NotDefinedError, errors.RedefinedError, errors.
        VerificationError) as e:
        error_rewrite(e, 'interpreter')
    except errors.ConstantInferenceError as e:
        error_rewrite(e, 'constant_inference')
    except bodo.utils.typing.BodoError as e:
        error = bodo.utils.typing.BodoError(str(e))
    except Exception as e:
        if numba.core.config.SHOW_HELP:
            if hasattr(e, 'patch_message'):
                ylxy__jkspn = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), ylxy__jkspn)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return akb__uqfr


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher._DispatcherBase.
        _compile_for_args)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5cdfbf0b13a528abf9f0408e70f67207a03e81d610c26b1acab5b2dc1f79bf06':
        warnings.warn(
            'numba.core.dispatcher._DispatcherBase._compile_for_args has changed'
            )
numba.core.dispatcher._DispatcherBase._compile_for_args = _compile_for_args


def resolve_gb_agg_funcs(cres):
    from bodo.ir.aggregate import gb_agg_cfunc_addr
    for jzva__sdwjv in cres.library._codegen._engine._defined_symbols:
        if jzva__sdwjv.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in jzva__sdwjv and (
            'bodo_gb_udf_update_local' in jzva__sdwjv or 
            'bodo_gb_udf_combine' in jzva__sdwjv or 'bodo_gb_udf_eval' in
            jzva__sdwjv or 'bodo_gb_apply_general_udfs' in jzva__sdwjv):
            gb_agg_cfunc_addr[jzva__sdwjv
                ] = cres.library.get_pointer_to_function(jzva__sdwjv)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for jzva__sdwjv in cres.library._codegen._engine._defined_symbols:
        if jzva__sdwjv.startswith('cfunc') and ('get_join_cond_addr' not in
            jzva__sdwjv or 'bodo_join_gen_cond' in jzva__sdwjv):
            join_gen_cond_cfunc_addr[jzva__sdwjv
                ] = cres.library.get_pointer_to_function(jzva__sdwjv)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    import bodo
    lhrq__acswx = self._get_dispatcher_for_current_target()
    if lhrq__acswx is not self:
        return lhrq__acswx.compile(sig)
    with ExitStack() as scope:
        cres = None

        def cb_compiler(dur):
            if cres is not None:
                self._callback_add_compiler_timer(dur, cres)

        def cb_llvm(dur):
            if cres is not None:
                self._callback_add_llvm_timer(dur, cres)
        scope.enter_context(ev.install_timer('numba:compiler_lock',
            cb_compiler))
        scope.enter_context(ev.install_timer('numba:llvm_lock', cb_llvm))
        scope.enter_context(global_compiler_lock)
        if not self._can_compile:
            raise RuntimeError('compilation disabled')
        with self._compiling_counter:
            args, return_type = sigutils.normalize_signature(sig)
            wry__ulcl = self.overloads.get(tuple(args))
            if wry__ulcl is not None:
                return wry__ulcl.entry_point
            cres = self._cache.load_overload(sig, self.targetctx)
            if cres is not None:
                resolve_gb_agg_funcs(cres)
                resolve_join_general_cond_funcs(cres)
                self._cache_hits[sig] += 1
                if not cres.objectmode:
                    self.targetctx.insert_user_function(cres.entry_point,
                        cres.fndesc, [cres.library])
                self.add_overload(cres)
                return cres.entry_point
            self._cache_misses[sig] += 1
            uvmi__vrc = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=uvmi__vrc):
                try:
                    cres = self._compiler.compile(args, return_type)
                except errors.ForceLiteralArg as e:

                    def folded(args, kws):
                        return self._compiler.fold_argument_types(args, kws)[1]
                    raise e.bind_fold_arguments(folded)
                self.add_overload(cres)
            if os.environ.get('BODO_PLATFORM_CACHE_LOCATION') is not None:
                if bodo.get_rank() == 0:
                    self._cache.save_overload(sig, cres)
            else:
                jcjn__cygqn = bodo.get_nodes_first_ranks()
                if bodo.get_rank() in jcjn__cygqn:
                    self._cache.save_overload(sig, cres)
            return cres.entry_point


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.Dispatcher.compile)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '934ec993577ea3b1c7dd2181ac02728abf8559fd42c17062cc821541b092ff8f':
        warnings.warn('numba.core.dispatcher.Dispatcher.compile has changed')
numba.core.dispatcher.Dispatcher.compile = compile


def _get_module_for_linking(self):
    import llvmlite.binding as ll
    self._ensure_finalized()
    if self._shared_module is not None:
        return self._shared_module
    hnkyp__ovtf = self._final_module
    jtak__maom = []
    poc__gujx = 0
    for fn in hnkyp__ovtf.functions:
        poc__gujx += 1
        if not fn.is_declaration and fn.linkage == ll.Linkage.external:
            if 'get_agg_udf_addr' not in fn.name:
                if 'bodo_gb_udf_update_local' in fn.name:
                    continue
                if 'bodo_gb_udf_combine' in fn.name:
                    continue
                if 'bodo_gb_udf_eval' in fn.name:
                    continue
                if 'bodo_gb_apply_general_udfs' in fn.name:
                    continue
            if 'get_join_cond_addr' not in fn.name:
                if 'bodo_join_gen_cond' in fn.name:
                    continue
            jtak__maom.append(fn.name)
    if poc__gujx == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if jtak__maom:
        hnkyp__ovtf = hnkyp__ovtf.clone()
        for name in jtak__maom:
            hnkyp__ovtf.get_function(name).linkage = 'linkonce_odr'
    self._shared_module = hnkyp__ovtf
    return hnkyp__ovtf


if _check_numba_change:
    lines = inspect.getsource(numba.core.codegen.CPUCodeLibrary.
        _get_module_for_linking)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '56dde0e0555b5ec85b93b97c81821bce60784515a1fbf99e4542e92d02ff0a73':
        warnings.warn(
            'numba.core.codegen.CPUCodeLibrary._get_module_for_linking has changed'
            )
numba.core.codegen.CPUCodeLibrary._get_module_for_linking = (
    _get_module_for_linking)


def propagate(self, typeinfer):
    import bodo
    errors = []
    for upf__lhl in self.constraints:
        loc = upf__lhl.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                upf__lhl(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                ewtby__fxua = numba.core.errors.TypingError(str(e), loc=
                    upf__lhl.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(ewtby__fxua, e))
            except bodo.utils.typing.BodoError as e:
                if loc not in e.locs_in_msg:
                    errors.append(bodo.utils.typing.BodoError(str(e.msg) +
                        '\n' + loc.strformat() + '\n', locs_in_msg=e.
                        locs_in_msg + [loc]))
                else:
                    errors.append(bodo.utils.typing.BodoError(e.msg,
                        locs_in_msg=e.locs_in_msg))
            except Exception as e:
                from numba.core import utils
                if utils.use_old_style_errors():
                    numba.core.typeinfer._logger.debug('captured error',
                        exc_info=e)
                    msg = """Internal error at {con}.
{err}
Enable logging at debug level for details."""
                    ewtby__fxua = numba.core.errors.TypingError(msg.format(
                        con=upf__lhl, err=str(e)), loc=upf__lhl.loc,
                        highlighting=False)
                    errors.append(utils.chain_exception(ewtby__fxua, e))
                elif utils.use_new_style_errors():
                    raise e
                else:
                    msg = (
                        f"Unknown CAPTURED_ERRORS style: '{numba.core.config.CAPTURED_ERRORS}'."
                        )
                    assert 0, msg
    return errors


if _check_numba_change:
    lines = inspect.getsource(numba.core.typeinfer.ConstraintNetwork.propagate)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1e73635eeba9ba43cb3372f395b747ae214ce73b729fb0adba0a55237a1cb063':
        warnings.warn(
            'numba.core.typeinfer.ConstraintNetwork.propagate has changed')
numba.core.typeinfer.ConstraintNetwork.propagate = propagate


def raise_error(self):
    import bodo
    for zori__ftbhd in self._failures.values():
        for buw__pgdy in zori__ftbhd:
            if isinstance(buw__pgdy.error, ForceLiteralArg):
                raise buw__pgdy.error
            if isinstance(buw__pgdy.error, bodo.utils.typing.BodoError):
                raise buw__pgdy.error
    raise TypingError(self.format())


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.
        _ResolutionFailures.raise_error)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '84b89430f5c8b46cfc684804e6037f00a0f170005cd128ad245551787b2568ea':
        warnings.warn(
            'numba.core.types.functions._ResolutionFailures.raise_error has changed'
            )
numba.core.types.functions._ResolutionFailures.raise_error = raise_error


def bodo_remove_dead_block(block, lives, call_table, arg_aliases, alias_map,
    alias_set, func_ir, typemap):
    from bodo.transforms.distributed_pass import saved_array_analysis
    from bodo.utils.utils import is_array_typ, is_expr
    cny__qtiur = False
    nwx__hhf = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        lrsum__xive = set()
        muw__fguwe = lives & alias_set
        for ssho__wfokk in muw__fguwe:
            lrsum__xive |= alias_map[ssho__wfokk]
        lives_n_aliases = lives | lrsum__xive | arg_aliases
        if type(stmt) in remove_dead_extensions:
            nymxr__ekktz = remove_dead_extensions[type(stmt)]
            stmt = nymxr__ekktz(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                cny__qtiur = True
                continue
        if isinstance(stmt, ir.Assign):
            ijcu__zuhlc = stmt.target
            xokam__bbrce = stmt.value
            if ijcu__zuhlc.name not in lives:
                if has_no_side_effect(xokam__bbrce, lives_n_aliases, call_table
                    ):
                    cny__qtiur = True
                    continue
                if isinstance(xokam__bbrce, ir.Expr
                    ) and xokam__bbrce.op == 'call' and call_table[xokam__bbrce
                    .func.name] == ['astype']:
                    qcjv__eknd = guard(get_definition, func_ir,
                        xokam__bbrce.func)
                    if (qcjv__eknd is not None and qcjv__eknd.op ==
                        'getattr' and isinstance(typemap[qcjv__eknd.value.
                        name], types.Array) and qcjv__eknd.attr == 'astype'):
                        cny__qtiur = True
                        continue
            if saved_array_analysis and ijcu__zuhlc.name in lives and is_expr(
                xokam__bbrce, 'getattr'
                ) and xokam__bbrce.attr == 'shape' and is_array_typ(typemap
                [xokam__bbrce.value.name]
                ) and xokam__bbrce.value.name not in lives:
                ypuez__wmj = {ssho__wfokk: ikm__tie for ikm__tie,
                    ssho__wfokk in func_ir.blocks.items()}
                if block in ypuez__wmj:
                    label = ypuez__wmj[block]
                    mgscx__rwdg = saved_array_analysis.get_equiv_set(label)
                    jmkfi__aevjn = mgscx__rwdg.get_equiv_set(xokam__bbrce.value
                        )
                    if jmkfi__aevjn is not None:
                        for ssho__wfokk in jmkfi__aevjn:
                            if ssho__wfokk.endswith('#0'):
                                ssho__wfokk = ssho__wfokk[:-2]
                            if ssho__wfokk in typemap and is_array_typ(typemap
                                [ssho__wfokk]) and ssho__wfokk in lives:
                                xokam__bbrce.value = ir.Var(xokam__bbrce.
                                    value.scope, ssho__wfokk, xokam__bbrce.
                                    value.loc)
                                cny__qtiur = True
                                break
            if isinstance(xokam__bbrce, ir.Var
                ) and ijcu__zuhlc.name == xokam__bbrce.name:
                cny__qtiur = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                cny__qtiur = True
                continue
        if isinstance(stmt, ir.SetItem):
            name = stmt.target.name
            if name not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            jyna__nhazp = analysis.ir_extension_usedefs[type(stmt)]
            kymf__mzq, drmpa__nvqw = jyna__nhazp(stmt)
            lives -= drmpa__nvqw
            lives |= kymf__mzq
        else:
            lives |= {ssho__wfokk.name for ssho__wfokk in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                uop__aibuq = set()
                if isinstance(xokam__bbrce, ir.Expr):
                    uop__aibuq = {ssho__wfokk.name for ssho__wfokk in
                        xokam__bbrce.list_vars()}
                if ijcu__zuhlc.name not in uop__aibuq:
                    lives.remove(ijcu__zuhlc.name)
        nwx__hhf.append(stmt)
    nwx__hhf.reverse()
    block.body = nwx__hhf
    return cny__qtiur


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            zuwbj__gvbk, = args
            if isinstance(zuwbj__gvbk, types.IterableType):
                dtype = zuwbj__gvbk.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), zuwbj__gvbk)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    fol__ehpi = 'reflected set' if reflected else 'set'
    name = '%s(%s)' % (fol__ehpi, self.dtype)
    super(types.Set, self).__init__(name=name)


types.Set.__init__ = Set__init__


@lower_builtin(operator.eq, types.UnicodeType, types.UnicodeType)
def eq_str(context, builder, sig, args):
    func = numba.cpython.unicode.unicode_eq(*sig.args)
    return context.compile_internal(builder, func, sig, args)


numba.parfors.parfor.push_call_vars = (lambda blocks, saved_globals,
    saved_getattrs, typemap, nested=False: None)


def maybe_literal(value):
    if isinstance(value, (list, dict, pytypes.FunctionType)):
        return
    if isinstance(value, tuple):
        try:
            return types.Tuple([literal(x) for x in value])
        except LiteralTypingError as hegol__cwyf:
            return
    try:
        return literal(value)
    except LiteralTypingError as hegol__cwyf:
        return


if _check_numba_change:
    lines = inspect.getsource(types.maybe_literal)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8fb2fd93acf214b28e33e37d19dc2f7290a42792ec59b650553ac278854b5081':
        warnings.warn('types.maybe_literal has changed')
types.maybe_literal = maybe_literal
types.misc.maybe_literal = maybe_literal


def CacheImpl__init__(self, py_func):
    self._lineno = py_func.__code__.co_firstlineno
    try:
        vcxw__jami = py_func.__qualname__
    except AttributeError as hegol__cwyf:
        vcxw__jami = py_func.__name__
    ybq__dhcrq = inspect.getfile(py_func)
    for cls in self._locator_classes:
        gdjiq__njht = cls.from_function(py_func, ybq__dhcrq)
        if gdjiq__njht is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (vcxw__jami, ybq__dhcrq))
    self._locator = gdjiq__njht
    tcv__itom = inspect.getfile(py_func)
    eazts__jnd = os.path.splitext(os.path.basename(tcv__itom))[0]
    if ybq__dhcrq.startswith('<ipython-'):
        qqdzt__mfox = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)',
            '\\1\\3', eazts__jnd, count=1)
        if qqdzt__mfox == eazts__jnd:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        eazts__jnd = qqdzt__mfox
    jpitb__kszw = '%s.%s' % (eazts__jnd, vcxw__jami)
    lpbr__yvg = getattr(sys, 'abiflags', '')
    from bodo import __version__ as bodo_version
    self._filename_base = self.get_filename_base(jpitb__kszw, lpbr__yvg
        ) + 'bodo' + bodo_version


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    hwv__qur = list(filter(lambda a: self._istuple(a.name), args))
    if len(hwv__qur) == 2 and fn.__name__ == 'add':
        nhle__fes = self.typemap[hwv__qur[0].name]
        lkh__mkwho = self.typemap[hwv__qur[1].name]
        if nhle__fes.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                hwv__qur[1]))
        if lkh__mkwho.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                hwv__qur[0]))
        try:
            pgwkj__hgmc = [equiv_set.get_shape(x) for x in hwv__qur]
            if None in pgwkj__hgmc:
                return None
            vqw__tvr = sum(pgwkj__hgmc, ())
            return ArrayAnalysis.AnalyzeResult(shape=vqw__tvr)
        except GuardException as hegol__cwyf:
            return None
    iinx__odt = list(filter(lambda a: self._isarray(a.name), args))
    require(len(iinx__odt) > 0)
    rlyek__txrdd = [x.name for x in iinx__odt]
    pmh__csb = [self.typemap[x.name].ndim for x in iinx__odt]
    vlt__bdk = max(pmh__csb)
    require(vlt__bdk > 0)
    pgwkj__hgmc = [equiv_set.get_shape(x) for x in iinx__odt]
    if any(a is None for a in pgwkj__hgmc):
        return ArrayAnalysis.AnalyzeResult(shape=iinx__odt[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, iinx__odt))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, pgwkj__hgmc,
        rlyek__txrdd)


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.array_analysis.ArrayAnalysis.
        _analyze_broadcast)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '6c91fec038f56111338ea2b08f5f0e7f61ebdab1c81fb811fe26658cc354e40f':
        warnings.warn(
            'numba.parfors.array_analysis.ArrayAnalysis._analyze_broadcast has changed'
            )
numba.parfors.array_analysis.ArrayAnalysis._analyze_broadcast = (
    _analyze_broadcast)


def slice_size(self, index, dsize, equiv_set, scope, stmts):
    return None, None


numba.parfors.array_analysis.ArrayAnalysis.slice_size = slice_size


def convert_code_obj_to_function(code_obj, caller_ir):
    import bodo
    eamda__lserz = code_obj.code
    dfilp__rrlo = len(eamda__lserz.co_freevars)
    qtvuo__edvni = eamda__lserz.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        hkl__fosc, op = ir_utils.find_build_sequence(caller_ir, code_obj.
            closure)
        assert op == 'build_tuple'
        qtvuo__edvni = [ssho__wfokk.name for ssho__wfokk in hkl__fosc]
    jjbk__xutwj = caller_ir.func_id.func.__globals__
    try:
        jjbk__xutwj = getattr(code_obj, 'globals', jjbk__xutwj)
    except KeyError as hegol__cwyf:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/api_docs/udfs/."
        )
    lnz__kuodj = []
    for x in qtvuo__edvni:
        try:
            oztk__nqaff = caller_ir.get_definition(x)
        except KeyError as hegol__cwyf:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(oztk__nqaff, (ir.Const, ir.Global, ir.FreeVar)):
            val = oztk__nqaff.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                oubrs__wuqj = ir_utils.mk_unique_var('nested_func').replace('.'
                    , '_')
                jjbk__xutwj[oubrs__wuqj] = bodo.jit(distributed=False)(val)
                jjbk__xutwj[oubrs__wuqj].is_nested_func = True
                val = oubrs__wuqj
            if isinstance(val, CPUDispatcher):
                oubrs__wuqj = ir_utils.mk_unique_var('nested_func').replace('.'
                    , '_')
                jjbk__xutwj[oubrs__wuqj] = val
                val = oubrs__wuqj
            lnz__kuodj.append(val)
        elif isinstance(oztk__nqaff, ir.Expr
            ) and oztk__nqaff.op == 'make_function':
            qky__xajnl = convert_code_obj_to_function(oztk__nqaff, caller_ir)
            oubrs__wuqj = ir_utils.mk_unique_var('nested_func').replace('.',
                '_')
            jjbk__xutwj[oubrs__wuqj] = bodo.jit(distributed=False)(qky__xajnl)
            jjbk__xutwj[oubrs__wuqj].is_nested_func = True
            lnz__kuodj.append(oubrs__wuqj)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    ccpb__tepu = '\n'.join([('\tc_%d = %s' % (i, x)) for i, x in enumerate(
        lnz__kuodj)])
    ihbp__keq = ','.join([('c_%d' % i) for i in range(dfilp__rrlo)])
    xcu__anc = list(eamda__lserz.co_varnames)
    ssa__zuwx = 0
    csffq__xwe = eamda__lserz.co_argcount
    dvgx__muiqe = caller_ir.get_definition(code_obj.defaults)
    if dvgx__muiqe is not None:
        if isinstance(dvgx__muiqe, tuple):
            d = [caller_ir.get_definition(x).value for x in dvgx__muiqe]
            ghnag__wjglj = tuple(d)
        else:
            d = [caller_ir.get_definition(x).value for x in dvgx__muiqe.items]
            ghnag__wjglj = tuple(d)
        ssa__zuwx = len(ghnag__wjglj)
    zfc__hqp = csffq__xwe - ssa__zuwx
    wmhho__qglar = ','.join([('%s' % xcu__anc[i]) for i in range(zfc__hqp)])
    if ssa__zuwx:
        eahcm__icek = [('%s = %s' % (xcu__anc[i + zfc__hqp], ghnag__wjglj[i
            ])) for i in range(ssa__zuwx)]
        wmhho__qglar += ', '
        wmhho__qglar += ', '.join(eahcm__icek)
    return _create_function_from_code_obj(eamda__lserz, ccpb__tepu,
        wmhho__qglar, ihbp__keq, jjbk__xutwj)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.convert_code_obj_to_function)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b840769812418d589460e924a15477e83e7919aac8a3dcb0188ff447344aa8ac':
        warnings.warn(
            'numba.core.ir_utils.convert_code_obj_to_function has changed')
numba.core.ir_utils.convert_code_obj_to_function = convert_code_obj_to_function
numba.core.untyped_passes.convert_code_obj_to_function = (
    convert_code_obj_to_function)


def passmanager_run(self, state):
    from numba.core.compiler import _EarlyPipelineCompletion
    if not self.finalized:
        raise RuntimeError('Cannot run non-finalised pipeline')
    from numba.core.compiler_machinery import CompilerPass, _pass_registry
    import bodo
    for jblc__timdo, (hyx__uyf, pjo__vgan) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % pjo__vgan)
            jag__wsl = _pass_registry.get(hyx__uyf).pass_inst
            if isinstance(jag__wsl, CompilerPass):
                self._runPass(jblc__timdo, jag__wsl, state)
            else:
                raise BaseException('Legacy pass in use')
        except _EarlyPipelineCompletion as e:
            raise e
        except bodo.utils.typing.BodoError as e:
            raise
        except Exception as e:
            if numba.core.config.DEVELOPER_MODE:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                msg = 'Failed in %s mode pipeline (step: %s)' % (self.
                    pipeline_name, pjo__vgan)
                ypbi__yrqmf = self._patch_error(msg, e)
                raise ypbi__yrqmf
            else:
                raise e


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler_machinery.PassManager.run)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '43505782e15e690fd2d7e53ea716543bec37aa0633502956864edf649e790cdb':
        warnings.warn(
            'numba.core.compiler_machinery.PassManager.run has changed')
numba.core.compiler_machinery.PassManager.run = passmanager_run
if _check_numba_change:
    lines = inspect.getsource(numba.np.ufunc.parallel._launch_threads)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a57ef28c4168fdd436a5513bba4351ebc6d9fba76c5819f44046431a79b9030f':
        warnings.warn('numba.np.ufunc.parallel._launch_threads has changed')
numba.np.ufunc.parallel._launch_threads = lambda : None


def get_reduce_nodes(reduction_node, nodes, func_ir):
    cwhm__gcg = None
    drmpa__nvqw = {}

    def lookup(var, already_seen, varonly=True):
        val = drmpa__nvqw.get(var.name, None)
        if isinstance(val, ir.Var):
            if val.name in already_seen:
                return var
            already_seen.add(val.name)
            return lookup(val, already_seen, varonly)
        else:
            return var if varonly or val is None else val
    name = reduction_node.name
    xnhcl__weki = reduction_node.unversioned_name
    for i, stmt in enumerate(nodes):
        ijcu__zuhlc = stmt.target
        xokam__bbrce = stmt.value
        drmpa__nvqw[ijcu__zuhlc.name] = xokam__bbrce
        if isinstance(xokam__bbrce, ir.Var
            ) and xokam__bbrce.name in drmpa__nvqw:
            xokam__bbrce = lookup(xokam__bbrce, set())
        if isinstance(xokam__bbrce, ir.Expr):
            effkt__tloxi = set(lookup(ssho__wfokk, set(), True).name for
                ssho__wfokk in xokam__bbrce.list_vars())
            if name in effkt__tloxi:
                args = [(x.name, lookup(x, set(), True)) for x in
                    get_expr_args(xokam__bbrce)]
                drwk__xxwtk = [x for x, uatqu__lio in args if uatqu__lio.
                    name != name]
                args = [(x, uatqu__lio) for x, uatqu__lio in args if x !=
                    uatqu__lio.name]
                kyj__bdnae = dict(args)
                if len(drwk__xxwtk) == 1:
                    kyj__bdnae[drwk__xxwtk[0]] = ir.Var(ijcu__zuhlc.scope, 
                        name + '#init', ijcu__zuhlc.loc)
                replace_vars_inner(xokam__bbrce, kyj__bdnae)
                cwhm__gcg = nodes[i:]
                break
    return cwhm__gcg


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_reduce_nodes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a05b52aff9cb02e595a510cd34e973857303a71097fc5530567cb70ca183ef3b':
        warnings.warn('numba.parfors.parfor.get_reduce_nodes has changed')
numba.parfors.parfor.get_reduce_nodes = get_reduce_nodes


def _can_reorder_stmts(stmt, next_stmt, func_ir, call_table, alias_map,
    arg_aliases):
    from numba.parfors.parfor import Parfor, expand_aliases, is_assert_equiv
    if isinstance(stmt, Parfor) and not isinstance(next_stmt, Parfor
        ) and not isinstance(next_stmt, ir.Print) and (not isinstance(
        next_stmt, ir.Assign) or has_no_side_effect(next_stmt.value, set(),
        call_table) or guard(is_assert_equiv, func_ir, next_stmt.value)):
        yxc__cni = expand_aliases({ssho__wfokk.name for ssho__wfokk in stmt
            .list_vars()}, alias_map, arg_aliases)
        lsgih__tmhf = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        pls__tyjhy = expand_aliases({ssho__wfokk.name for ssho__wfokk in
            next_stmt.list_vars()}, alias_map, arg_aliases)
        gysvd__oex = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(lsgih__tmhf & pls__tyjhy | gysvd__oex & yxc__cni) == 0:
            return True
    return False


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor._can_reorder_stmts)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '18caa9a01b21ab92b4f79f164cfdbc8574f15ea29deedf7bafdf9b0e755d777c':
        warnings.warn('numba.parfors.parfor._can_reorder_stmts has changed')
numba.parfors.parfor._can_reorder_stmts = _can_reorder_stmts


def get_parfor_writes(parfor, func_ir):
    from numba.parfors.parfor import Parfor
    assert isinstance(parfor, Parfor)
    cyv__wksw = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            cyv__wksw.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                cyv__wksw.update(get_parfor_writes(stmt, func_ir))
    return cyv__wksw


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    cyv__wksw = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        cyv__wksw.add(stmt.target.name)
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        cyv__wksw = {ssho__wfokk.name for ssho__wfokk in stmt.out_vars}
    if isinstance(stmt, (bodo.ir.join.Join, bodo.ir.aggregate.Aggregate)):
        cyv__wksw = {ssho__wfokk.name for ssho__wfokk in stmt.
            get_live_out_vars()}
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            cyv__wksw.update({ssho__wfokk.name for ssho__wfokk in stmt.
                get_live_out_vars()})
    if is_call_assign(stmt):
        ofi__rhs = guard(find_callname, func_ir, stmt.value)
        if ofi__rhs in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'), (
            'setna', 'bodo.libs.array_kernels'), ('str_arr_item_to_numeric',
            'bodo.libs.str_arr_ext'), ('str_arr_setitem_int_to_str',
            'bodo.libs.str_arr_ext'), ('str_arr_setitem_NA_str',
            'bodo.libs.str_arr_ext'), ('str_arr_set_not_na',
            'bodo.libs.str_arr_ext'), ('get_str_arr_item_copy',
            'bodo.libs.str_arr_ext'), ('set_bit_to_arr',
            'bodo.libs.int_arr_ext')):
            cyv__wksw.add(stmt.value.args[0].name)
        if ofi__rhs == ('generate_table_nbytes', 'bodo.utils.table_utils'):
            cyv__wksw.add(stmt.value.args[1].name)
    return cyv__wksw


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.get_stmt_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1a7a80b64c9a0eb27e99dc8eaae187bde379d4da0b74c84fbf87296d87939974':
        warnings.warn('numba.core.ir_utils.get_stmt_writes has changed')


def patch_message(self, new_message):
    self.msg = new_message
    self.args = (new_message,) + self.args[1:]


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.NumbaError.patch_message)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'ed189a428a7305837e76573596d767b6e840e99f75c05af6941192e0214fa899':
        warnings.warn('numba.core.errors.NumbaError.patch_message has changed')
numba.core.errors.NumbaError.patch_message = patch_message


def add_context(self, msg):
    if numba.core.config.DEVELOPER_MODE:
        self.contexts.append(msg)
        nymxr__ekktz = _termcolor.errmsg('{0}') + _termcolor.filename(
            'During: {1}')
        dteiq__xraxl = nymxr__ekktz.format(self, msg)
        self.args = dteiq__xraxl,
    else:
        nymxr__ekktz = _termcolor.errmsg('{0}')
        dteiq__xraxl = nymxr__ekktz.format(self)
        self.args = dteiq__xraxl,
    return self


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.NumbaError.add_context)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '6a388d87788f8432c2152ac55ca9acaa94dbc3b55be973b2cf22dd4ee7179ab8':
        warnings.warn('numba.core.errors.NumbaError.add_context has changed')
numba.core.errors.NumbaError.add_context = add_context


def _get_dist_spec_from_options(spec, **options):
    from bodo.transforms.distributed_analysis import Distribution
    dist_spec = {}
    if 'distributed' in options:
        for wzav__gij in options['distributed']:
            dist_spec[wzav__gij] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for wzav__gij in options['distributed_block']:
            dist_spec[wzav__gij] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    hdwbg__inox = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, vxp__hamz in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(vxp__hamz)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    vrb__fznvh = {}
    for yrbd__roc in reversed(inspect.getmro(cls)):
        vrb__fznvh.update(yrbd__roc.__dict__)
    oya__rgeoq, gst__tmghm, ods__uvbyy, jqni__rxnnj = {}, {}, {}, {}
    for ikm__tie, ssho__wfokk in vrb__fznvh.items():
        if isinstance(ssho__wfokk, pytypes.FunctionType):
            oya__rgeoq[ikm__tie] = ssho__wfokk
        elif isinstance(ssho__wfokk, property):
            gst__tmghm[ikm__tie] = ssho__wfokk
        elif isinstance(ssho__wfokk, staticmethod):
            ods__uvbyy[ikm__tie] = ssho__wfokk
        else:
            jqni__rxnnj[ikm__tie] = ssho__wfokk
    pqeli__ngzt = (set(oya__rgeoq) | set(gst__tmghm) | set(ods__uvbyy)) & set(
        spec)
    if pqeli__ngzt:
        raise NameError('name shadowing: {0}'.format(', '.join(pqeli__ngzt)))
    vyw__xmb = jqni__rxnnj.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(jqni__rxnnj)
    if jqni__rxnnj:
        msg = 'class members are not yet supported: {0}'
        jrm__ccgko = ', '.join(jqni__rxnnj.keys())
        raise TypeError(msg.format(jrm__ccgko))
    for ikm__tie, ssho__wfokk in gst__tmghm.items():
        if ssho__wfokk.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(ikm__tie))
    jit_methods = {ikm__tie: bodo.jit(returns_maybe_distributed=hdwbg__inox
        )(ssho__wfokk) for ikm__tie, ssho__wfokk in oya__rgeoq.items()}
    jit_props = {}
    for ikm__tie, ssho__wfokk in gst__tmghm.items():
        nlza__gqmtr = {}
        if ssho__wfokk.fget:
            nlza__gqmtr['get'] = bodo.jit(ssho__wfokk.fget)
        if ssho__wfokk.fset:
            nlza__gqmtr['set'] = bodo.jit(ssho__wfokk.fset)
        jit_props[ikm__tie] = nlza__gqmtr
    jit_static_methods = {ikm__tie: bodo.jit(ssho__wfokk.__func__) for 
        ikm__tie, ssho__wfokk in ods__uvbyy.items()}
    afis__gxbz = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    gmsj__qdzc = dict(class_type=afis__gxbz, __doc__=vyw__xmb)
    gmsj__qdzc.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), gmsj__qdzc)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, afis__gxbz)
    targetctx = numba.core.registry.cpu_target.target_context
    builder(afis__gxbz, typingctx, targetctx).register()
    as_numba_type.register(cls, afis__gxbz.instance_type)
    return cls


if _check_numba_change:
    lines = inspect.getsource(jitclass_base.register_class_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '005e6e2e89a47f77a19ba86305565050d4dbc2412fc4717395adf2da348671a9':
        warnings.warn('jitclass_base.register_class_type has changed')
jitclass_base.register_class_type = register_class_type


def ClassType__init__(self, class_def, ctor_template_cls, struct,
    jit_methods, jit_props, jit_static_methods, dist_spec=None):
    if dist_spec is None:
        dist_spec = {}
    self.class_name = class_def.__name__
    self.class_doc = class_def.__doc__
    self._ctor_template_class = ctor_template_cls
    self.jit_methods = jit_methods
    self.jit_props = jit_props
    self.jit_static_methods = jit_static_methods
    self.struct = struct
    self.dist_spec = dist_spec
    kzsln__upmhu = ','.join('{0}:{1}'.format(ikm__tie, ssho__wfokk) for 
        ikm__tie, ssho__wfokk in struct.items())
    akzhf__mezv = ','.join('{0}:{1}'.format(ikm__tie, ssho__wfokk) for 
        ikm__tie, ssho__wfokk in dist_spec.items())
    name = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), kzsln__upmhu, akzhf__mezv)
    super(types.misc.ClassType, self).__init__(name)


if _check_numba_change:
    lines = inspect.getsource(types.misc.ClassType.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '2b848ea82946c88f540e81f93ba95dfa7cd66045d944152a337fe2fc43451c30':
        warnings.warn('types.misc.ClassType.__init__ has changed')
types.misc.ClassType.__init__ = ClassType__init__


def jitclass(cls_or_spec=None, spec=None, **options):
    if cls_or_spec is not None and spec is None and not isinstance(cls_or_spec,
        type):
        spec = cls_or_spec
        cls_or_spec = None

    def wrap(cls):
        if numba.core.config.DISABLE_JIT:
            return cls
        else:
            from numba.experimental.jitclass.base import ClassBuilder
            return register_class_type(cls, spec, types.ClassType,
                ClassBuilder, **options)
    if cls_or_spec is None:
        return wrap
    else:
        return wrap(cls_or_spec)


if _check_numba_change:
    lines = inspect.getsource(jitclass_decorators.jitclass)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '265f1953ee5881d1a5d90238d3c932cd300732e41495657e65bf51e59f7f4af5':
        warnings.warn('jitclass_decorators.jitclass has changed')


def CallConstraint_resolve(self, typeinfer, typevars, fnty):
    assert fnty
    context = typeinfer.context
    azkf__ttlu = numba.core.typeinfer.fold_arg_vars(typevars, self.args,
        self.vararg, self.kws)
    if azkf__ttlu is None:
        return
    qdjvj__iycl, ewzg__tnso = azkf__ttlu
    for a in itertools.chain(qdjvj__iycl, ewzg__tnso.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, qdjvj__iycl, ewzg__tnso)
    except ForceLiteralArg as e:
        jdxg__nhj = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(jdxg__nhj, self.kws)
        bpioo__elbzy = set()
        wpbuf__uyb = set()
        rpf__qussd = {}
        for jblc__timdo in e.requested_args:
            lymq__lptgf = typeinfer.func_ir.get_definition(folded[jblc__timdo])
            if isinstance(lymq__lptgf, ir.Arg):
                bpioo__elbzy.add(lymq__lptgf.index)
                if lymq__lptgf.index in e.file_infos:
                    rpf__qussd[lymq__lptgf.index] = e.file_infos[lymq__lptgf
                        .index]
            else:
                wpbuf__uyb.add(jblc__timdo)
        if wpbuf__uyb:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif bpioo__elbzy:
            raise ForceLiteralArg(bpioo__elbzy, loc=self.loc, file_infos=
                rpf__qussd)
    if sig is None:
        rfvh__gcout = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in qdjvj__iycl]
        args += [('%s=%s' % (ikm__tie, ssho__wfokk)) for ikm__tie,
            ssho__wfokk in sorted(ewzg__tnso.items())]
        oxc__wyluf = rfvh__gcout.format(fnty, ', '.join(map(str, args)))
        omt__zcpt = context.explain_function_type(fnty)
        msg = '\n'.join([oxc__wyluf, omt__zcpt])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        gozoz__olfmz = context.unify_pairs(sig.recvr, fnty.this)
        if gozoz__olfmz is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if gozoz__olfmz is not None and gozoz__olfmz.is_precise():
            ejw__ptqy = fnty.copy(this=gozoz__olfmz)
            typeinfer.propagate_refined_type(self.func, ejw__ptqy)
    if not sig.return_type.is_precise():
        target = typevars[self.target]
        if target.defined:
            kthy__wcdg = target.getone()
            if context.unify_pairs(kthy__wcdg, sig.return_type) == kthy__wcdg:
                sig = sig.replace(return_type=kthy__wcdg)
    self.signature = sig
    self._add_refine_map(typeinfer, typevars, sig)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typeinfer.CallConstraint.resolve)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c78cd8ffc64b836a6a2ddf0362d481b52b9d380c5249920a87ff4da052ce081f':
        warnings.warn('numba.core.typeinfer.CallConstraint.resolve has changed'
            )
numba.core.typeinfer.CallConstraint.resolve = CallConstraint_resolve


def ForceLiteralArg__init__(self, arg_indices, fold_arguments=None, loc=
    None, file_infos=None):
    super(ForceLiteralArg, self).__init__(
        'Pseudo-exception to force literal arguments in the dispatcher',
        loc=loc)
    self.requested_args = frozenset(arg_indices)
    self.fold_arguments = fold_arguments
    if file_infos is None:
        self.file_infos = {}
    else:
        self.file_infos = file_infos


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b241d5e36a4cf7f4c73a7ad3238693612926606c7a278cad1978070b82fb55ef':
        warnings.warn('numba.core.errors.ForceLiteralArg.__init__ has changed')
numba.core.errors.ForceLiteralArg.__init__ = ForceLiteralArg__init__


def ForceLiteralArg_bind_fold_arguments(self, fold_arguments):
    e = ForceLiteralArg(self.requested_args, fold_arguments, loc=self.loc,
        file_infos=self.file_infos)
    return numba.core.utils.chain_exception(e, self)


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.
        bind_fold_arguments)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1e93cca558f7c604a47214a8f2ec33ee994104cb3e5051166f16d7cc9315141d':
        warnings.warn(
            'numba.core.errors.ForceLiteralArg.bind_fold_arguments has changed'
            )
numba.core.errors.ForceLiteralArg.bind_fold_arguments = (
    ForceLiteralArg_bind_fold_arguments)


def ForceLiteralArg_combine(self, other):
    if not isinstance(other, ForceLiteralArg):
        pldj__bgz = '*other* must be a {} but got a {} instead'
        raise TypeError(pldj__bgz.format(ForceLiteralArg, type(other)))
    return ForceLiteralArg(self.requested_args | other.requested_args,
        file_infos={**self.file_infos, **other.file_infos})


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.combine)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '49bf06612776f5d755c1c7d1c5eb91831a57665a8fed88b5651935f3bf33e899':
        warnings.warn('numba.core.errors.ForceLiteralArg.combine has changed')
numba.core.errors.ForceLiteralArg.combine = ForceLiteralArg_combine


def _get_global_type(self, gv):
    from bodo.utils.typing import FunctionLiteral
    ty = self._lookup_global(gv)
    if ty is not None:
        return ty
    if isinstance(gv, pytypes.ModuleType):
        return types.Module(gv)
    if isinstance(gv, pytypes.FunctionType):
        return FunctionLiteral(gv)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.context.BaseContext.
        _get_global_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8ffe6b81175d1eecd62a37639b5005514b4477d88f35f5b5395041ac8c945a4a':
        warnings.warn(
            'numba.core.typing.context.BaseContext._get_global_type has changed'
            )
numba.core.typing.context.BaseContext._get_global_type = _get_global_type


def _legalize_args(self, func_ir, args, kwargs, loc, func_globals,
    func_closures):
    from numba.core import sigutils
    from bodo.utils.transform import get_const_value_inner
    if args:
        raise errors.CompilerError(
            "objectmode context doesn't take any positional arguments")
    xfio__aeb = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for ikm__tie, ssho__wfokk in kwargs.items():
        snp__zph = None
        try:
            dtujy__hrtkk = ir.Var(ir.Scope(None, loc), ir_utils.
                mk_unique_var('dummy'), loc)
            func_ir._definitions[dtujy__hrtkk.name] = [ssho__wfokk]
            snp__zph = get_const_value_inner(func_ir, dtujy__hrtkk)
            func_ir._definitions.pop(dtujy__hrtkk.name)
            if isinstance(snp__zph, str):
                snp__zph = sigutils._parse_signature_string(snp__zph)
            if isinstance(snp__zph, types.abstract._TypeMetaclass):
                raise BodoError(
                    f"""objmode type annotations require full data types, not just data type classes. For example, 'bodo.DataFrameType((bodo.float64[::1],), bodo.RangeIndexType(), ('A',))' is a valid data type but 'bodo.DataFrameType' is not.
Variable {ikm__tie} is annotated as type class {snp__zph}."""
                    )
            assert isinstance(snp__zph, types.Type)
            if isinstance(snp__zph, (types.List, types.Set)):
                snp__zph = snp__zph.copy(reflected=False)
            xfio__aeb[ikm__tie] = snp__zph
        except BodoError as hegol__cwyf:
            raise
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(snp__zph, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(ssho__wfokk, ir.Global):
                    msg = f'Global {ssho__wfokk.name!r} is not defined.'
                if isinstance(ssho__wfokk, ir.FreeVar):
                    msg = f'Freevar {ssho__wfokk.name!r} is not defined.'
            if isinstance(ssho__wfokk, ir.Expr
                ) and ssho__wfokk.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=ikm__tie, msg=msg, loc=loc)
    for name, typ in xfio__aeb.items():
        self._legalize_arg_type(name, typ, loc)
    return xfio__aeb


if _check_numba_change:
    lines = inspect.getsource(numba.core.withcontexts._ObjModeContextType.
        _legalize_args)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '867c9ba7f1bcf438be56c38e26906bb551f59a99f853a9f68b71208b107c880e':
        warnings.warn(
            'numba.core.withcontexts._ObjModeContextType._legalize_args has changed'
            )
numba.core.withcontexts._ObjModeContextType._legalize_args = _legalize_args


def op_FORMAT_VALUE_byteflow(self, state, inst):
    flags = inst.arg
    if flags & 3 != 0:
        msg = 'str/repr/ascii conversion in f-strings not supported yet'
        raise errors.UnsupportedError(msg, loc=self.get_debug_loc(inst.lineno))
    format_spec = None
    if flags & 4 == 4:
        format_spec = state.pop()
    value = state.pop()
    fmtvar = state.make_temp()
    res = state.make_temp()
    state.append(inst, value=value, res=res, fmtvar=fmtvar, format_spec=
        format_spec)
    state.push(res)


def op_BUILD_STRING_byteflow(self, state, inst):
    onnj__quqt = inst.arg
    assert onnj__quqt > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(onnj__quqt)]))
    tmps = [state.make_temp() for _ in range(onnj__quqt - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    ori__ynqt = ir.Global('format', format, loc=self.loc)
    self.store(value=ori__ynqt, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    jge__ucsik = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=jge__ucsik, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    onnj__quqt = inst.arg
    assert onnj__quqt > 0, 'invalid BUILD_STRING count'
    dov__qzuh = self.get(strings[0])
    for other, iaxta__xnvb in zip(strings[1:], tmps):
        other = self.get(other)
        vxi__gcf = ir.Expr.binop(operator.add, lhs=dov__qzuh, rhs=other,
            loc=self.loc)
        self.store(vxi__gcf, iaxta__xnvb)
        dov__qzuh = self.get(iaxta__xnvb)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite import ir as lir
    brws__uoh = self.context.insert_const_string(self.module, attr)
    fnty = lir.FunctionType(lir.IntType(32), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, brws__uoh])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


def _created_inlined_var_name(function_name, var_name):
    cndpd__uhozf = mk_unique_var(f'{var_name}')
    lnd__mvp = cndpd__uhozf.replace('<', '_').replace('>', '_')
    lnd__mvp = lnd__mvp.replace('.', '_').replace('$', '_v')
    return lnd__mvp


if _check_numba_change:
    lines = inspect.getsource(numba.core.inline_closurecall.
        _created_inlined_var_name)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '0d91aac55cd0243e58809afe9d252562f9ae2899cde1112cc01a46804e01821e':
        warnings.warn(
            'numba.core.inline_closurecall._created_inlined_var_name has changed'
            )
numba.core.inline_closurecall._created_inlined_var_name = (
    _created_inlined_var_name)


def resolve_number___call__(self, classty):
    import numpy as np
    from numba.core.typing.templates import make_callable_template
    import bodo
    ty = classty.instance_type
    if isinstance(ty, types.NPDatetime):

        def typer(val1, val2):
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(val1,
                'numpy.datetime64')
            if val1 == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
                if not is_overload_constant_str(val2):
                    raise_bodo_error(
                        "datetime64(): 'units' must be a 'str' specifying 'ns'"
                        )
                xmo__gmi = get_overload_const_str(val2)
                if xmo__gmi != 'ns':
                    raise BodoError("datetime64(): 'units' must be 'ns'")
                return types.NPDatetime('ns')
    else:

        def typer(val):
            if isinstance(val, (types.BaseTuple, types.Sequence)):
                fnty = self.context.resolve_value_type(np.array)
                sig = fnty.get_call_type(self.context, (val, types.DType(ty
                    )), {})
                return sig.return_type
            elif isinstance(val, (types.Number, types.Boolean, types.
                IntEnumMember)):
                return ty
            elif val == types.unicode_type:
                return ty
            elif isinstance(val, (types.NPDatetime, types.NPTimedelta)):
                if ty.bitwidth == 64:
                    return ty
                else:
                    msg = (
                        f'Cannot cast {val} to {ty} as {ty} is not 64 bits wide.'
                        )
                    raise errors.TypingError(msg)
            elif isinstance(val, types.Array
                ) and val.ndim == 0 and val.dtype == ty:
                return ty
            else:
                msg = f'Casting {val} to {ty} directly is unsupported.'
                if isinstance(val, types.Array):
                    msg += f" Try doing '<array>.astype(np.{ty})' instead"
                raise errors.TypingError(msg)
    return types.Function(make_callable_template(key=ty, typer=typer))


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.builtins.
        NumberClassAttribute.resolve___call__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'fdaf0c7d0820130481bb2bd922985257b9281b670f0bafffe10e51cabf0d5081':
        warnings.warn(
            'numba.core.typing.builtins.NumberClassAttribute.resolve___call__ has changed'
            )
numba.core.typing.builtins.NumberClassAttribute.resolve___call__ = (
    resolve_number___call__)


def on_assign(self, states, assign):
    if assign.target.name == states['varname']:
        scope = states['scope']
        dui__cszok = states['defmap']
        if len(dui__cszok) == 0:
            qpkkd__dxmj = assign.target
            numba.core.ssa._logger.debug('first assign: %s', qpkkd__dxmj)
            if qpkkd__dxmj.name not in scope.localvars:
                qpkkd__dxmj = scope.define(assign.target.name, loc=assign.loc)
        else:
            qpkkd__dxmj = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=qpkkd__dxmj, value=assign.value, loc=
            assign.loc)
        dui__cszok[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    zpeif__fntux = []
    for ikm__tie, ssho__wfokk in typing.npydecl.registry.globals:
        if ikm__tie == func:
            zpeif__fntux.append(ssho__wfokk)
    for ikm__tie, ssho__wfokk in typing.templates.builtin_registry.globals:
        if ikm__tie == func:
            zpeif__fntux.append(ssho__wfokk)
    if len(zpeif__fntux) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return zpeif__fntux


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    gtzx__lmcl = {}
    yfzim__uwi = find_topo_order(blocks)
    ihx__dgzvo = {}
    for label in yfzim__uwi:
        block = blocks[label]
        nwx__hhf = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                ijcu__zuhlc = stmt.target.name
                xokam__bbrce = stmt.value
                if (xokam__bbrce.op == 'getattr' and xokam__bbrce.attr in
                    arr_math and isinstance(typemap[xokam__bbrce.value.name
                    ], types.npytypes.Array)):
                    xokam__bbrce = stmt.value
                    btpg__rwp = xokam__bbrce.value
                    gtzx__lmcl[ijcu__zuhlc] = btpg__rwp
                    scope = btpg__rwp.scope
                    loc = btpg__rwp.loc
                    ctk__zzk = ir.Var(scope, mk_unique_var('$np_g_var'), loc)
                    typemap[ctk__zzk.name] = types.misc.Module(numpy)
                    koypa__fexv = ir.Global('np', numpy, loc)
                    gbvln__rsocw = ir.Assign(koypa__fexv, ctk__zzk, loc)
                    xokam__bbrce.value = ctk__zzk
                    nwx__hhf.append(gbvln__rsocw)
                    func_ir._definitions[ctk__zzk.name] = [koypa__fexv]
                    func = getattr(numpy, xokam__bbrce.attr)
                    mtm__enr = get_np_ufunc_typ_lst(func)
                    ihx__dgzvo[ijcu__zuhlc] = mtm__enr
                if (xokam__bbrce.op == 'call' and xokam__bbrce.func.name in
                    gtzx__lmcl):
                    btpg__rwp = gtzx__lmcl[xokam__bbrce.func.name]
                    ovnwm__aaxzs = calltypes.pop(xokam__bbrce)
                    hwfz__qrem = ovnwm__aaxzs.args[:len(xokam__bbrce.args)]
                    kpbq__ivne = {name: typemap[ssho__wfokk.name] for name,
                        ssho__wfokk in xokam__bbrce.kws}
                    yef__dsjq = ihx__dgzvo[xokam__bbrce.func.name]
                    upr__aoc = None
                    for qnxb__ryggr in yef__dsjq:
                        try:
                            upr__aoc = qnxb__ryggr.get_call_type(typingctx,
                                [typemap[btpg__rwp.name]] + list(hwfz__qrem
                                ), kpbq__ivne)
                            typemap.pop(xokam__bbrce.func.name)
                            typemap[xokam__bbrce.func.name] = qnxb__ryggr
                            calltypes[xokam__bbrce] = upr__aoc
                            break
                        except Exception as hegol__cwyf:
                            pass
                    if upr__aoc is None:
                        raise TypeError(
                            f'No valid template found for {xokam__bbrce.func.name}'
                            )
                    xokam__bbrce.args = [btpg__rwp] + xokam__bbrce.args
            nwx__hhf.append(stmt)
        block.body = nwx__hhf


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    eyw__xyn = ufunc.nin
    yolp__onx = ufunc.nout
    zfc__hqp = ufunc.nargs
    assert zfc__hqp == eyw__xyn + yolp__onx
    if len(args) < eyw__xyn:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), eyw__xyn))
    if len(args) > zfc__hqp:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), zfc__hqp))
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    dcs__warrq = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    rvly__nve = max(dcs__warrq)
    gqj__thglc = args[eyw__xyn:]
    if not all(d == rvly__nve for d in dcs__warrq[eyw__xyn:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(ygla__hahl, types.ArrayCompatible) and not
        isinstance(ygla__hahl, types.Bytes) for ygla__hahl in gqj__thglc):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(ygla__hahl.mutable for ygla__hahl in gqj__thglc):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    mvrdx__kfg = [(x.dtype if isinstance(x, types.ArrayCompatible) and not
        isinstance(x, types.Bytes) else x) for x in args]
    xij__ihpp = None
    if rvly__nve > 0 and len(gqj__thglc) < ufunc.nout:
        xij__ihpp = 'C'
        npw__fwmvp = [(x.layout if isinstance(x, types.ArrayCompatible) and
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in npw__fwmvp and 'F' in npw__fwmvp:
            xij__ihpp = 'F'
    return mvrdx__kfg, gqj__thglc, rvly__nve, xij__ihpp


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.npydecl.Numpy_rules_ufunc.
        _handle_inputs)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4b97c64ad9c3d50e082538795054f35cf6d2fe962c3ca40e8377a4601b344d5c':
        warnings.warn('Numpy_rules_ufunc._handle_inputs has changed')
numba.core.typing.npydecl.Numpy_rules_ufunc._handle_inputs = (
    _Numpy_Rules_ufunc_handle_inputs)
numba.np.ufunc.dufunc.npydecl.Numpy_rules_ufunc._handle_inputs = (
    _Numpy_Rules_ufunc_handle_inputs)


def DictType__init__(self, keyty, valty, initial_value=None):
    from numba.types import DictType, InitialValue, NoneType, Optional, Tuple, TypeRef, unliteral
    assert not isinstance(keyty, TypeRef)
    assert not isinstance(valty, TypeRef)
    keyty = unliteral(keyty)
    valty = unliteral(valty)
    if isinstance(keyty, (Optional, NoneType)):
        qdfra__eetgb = 'Dict.key_type cannot be of type {}'
        raise TypingError(qdfra__eetgb.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        qdfra__eetgb = 'Dict.value_type cannot be of type {}'
        raise TypingError(qdfra__eetgb.format(valty))
    self.key_type = keyty
    self.value_type = valty
    self.keyvalue_type = Tuple([keyty, valty])
    name = '{}[{},{}]<iv={}>'.format(self.__class__.__name__, keyty, valty,
        initial_value)
    super(DictType, self).__init__(name)
    InitialValue.__init__(self, initial_value)


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.containers.DictType.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '475acd71224bd51526750343246e064ff071320c0d10c17b8b8ac81d5070d094':
        warnings.warn('DictType.__init__ has changed')
numba.core.types.containers.DictType.__init__ = DictType__init__


def _legalize_arg_types(self, args):
    for i, a in enumerate(args, start=1):
        if isinstance(a, types.Dispatcher):
            msg = (
                'Does not support function type inputs into with-context for arg {}'
                )
            raise errors.TypingError(msg.format(i))


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.ObjModeLiftedWith.
        _legalize_arg_types)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4793f44ebc7da8843e8f298e08cd8a5428b4b84b89fd9d5c650273fdb8fee5ee':
        warnings.warn('ObjModeLiftedWith._legalize_arg_types has changed')
numba.core.dispatcher.ObjModeLiftedWith._legalize_arg_types = (
    _legalize_arg_types)


def _overload_template_get_impl(self, args, kws):
    lyha__axkc = self.context, tuple(args), tuple(kws.items())
    try:
        impl, args = self._impl_cache[lyha__axkc]
        return impl, args
    except KeyError as hegol__cwyf:
        pass
    impl, args = self._build_impl(lyha__axkc, args, kws)
    return impl, args


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadFunctionTemplate._get_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4e27d07b214ca16d6e8ed88f70d886b6b095e160d8f77f8df369dd4ed2eb3fae':
        warnings.warn(
            'numba.core.typing.templates._OverloadFunctionTemplate._get_impl has changed'
            )
numba.core.typing.templates._OverloadFunctionTemplate._get_impl = (
    _overload_template_get_impl)


def trim_empty_parfor_branches(parfor):
    otru__omn = False
    blocks = parfor.loop_body.copy()
    for label, block in blocks.items():
        if len(block.body):
            pqcu__qna = block.body[-1]
            if isinstance(pqcu__qna, ir.Branch):
                if len(blocks[pqcu__qna.truebr].body) == 1 and len(blocks[
                    pqcu__qna.falsebr].body) == 1:
                    djw__tepl = blocks[pqcu__qna.truebr].body[0]
                    mxnik__edcct = blocks[pqcu__qna.falsebr].body[0]
                    if isinstance(djw__tepl, ir.Jump) and isinstance(
                        mxnik__edcct, ir.Jump
                        ) and djw__tepl.target == mxnik__edcct.target:
                        parfor.loop_body[label].body[-1] = ir.Jump(djw__tepl
                            .target, pqcu__qna.loc)
                        otru__omn = True
                elif len(blocks[pqcu__qna.truebr].body) == 1:
                    djw__tepl = blocks[pqcu__qna.truebr].body[0]
                    if isinstance(djw__tepl, ir.Jump
                        ) and djw__tepl.target == pqcu__qna.falsebr:
                        parfor.loop_body[label].body[-1] = ir.Jump(djw__tepl
                            .target, pqcu__qna.loc)
                        otru__omn = True
                elif len(blocks[pqcu__qna.falsebr].body) == 1:
                    mxnik__edcct = blocks[pqcu__qna.falsebr].body[0]
                    if isinstance(mxnik__edcct, ir.Jump
                        ) and mxnik__edcct.target == pqcu__qna.truebr:
                        parfor.loop_body[label].body[-1] = ir.Jump(mxnik__edcct
                            .target, pqcu__qna.loc)
                        otru__omn = True
    return otru__omn


def remove_dead_parfor(parfor, lives, lives_n_aliases, arg_aliases,
    alias_map, func_ir, typemap):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    from numba.core.ir_utils import find_topo_order
    from numba.parfors.parfor import _add_liveness_return_block, _update_parfor_get_setitems, dummy_return_in_loop_body, get_index_var, remove_dead_parfor_recursive, simplify_parfor_body_CFG
    with dummy_return_in_loop_body(parfor.loop_body):
        akdgp__ingp = find_topo_order(parfor.loop_body)
    xtjo__nphr = akdgp__ingp[0]
    ujx__qbfcb = {}
    _update_parfor_get_setitems(parfor.loop_body[xtjo__nphr].body, parfor.
        index_var, alias_map, ujx__qbfcb, lives_n_aliases)
    ghy__gmsn = set(ujx__qbfcb.keys())
    for zwrd__ilntb in akdgp__ingp:
        if zwrd__ilntb == xtjo__nphr:
            continue
        for stmt in parfor.loop_body[zwrd__ilntb].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            tuxxm__vfol = set(ssho__wfokk.name for ssho__wfokk in stmt.
                list_vars())
            oytc__mfj = tuxxm__vfol & ghy__gmsn
            for a in oytc__mfj:
                ujx__qbfcb.pop(a, None)
    for zwrd__ilntb in akdgp__ingp:
        if zwrd__ilntb == xtjo__nphr:
            continue
        block = parfor.loop_body[zwrd__ilntb]
        cpeg__qgj = ujx__qbfcb.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            cpeg__qgj, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    epmmo__flid = max(blocks.keys())
    udio__pqja, myuol__xxz = _add_liveness_return_block(blocks,
        lives_n_aliases, typemap)
    zky__zyb = ir.Jump(udio__pqja, ir.Loc('parfors_dummy', -1))
    blocks[epmmo__flid].body.append(zky__zyb)
    rdf__vljky = compute_cfg_from_blocks(blocks)
    rpu__uyfy = compute_use_defs(blocks)
    vva__hrd = compute_live_map(rdf__vljky, blocks, rpu__uyfy.usemap,
        rpu__uyfy.defmap)
    alias_set = set(alias_map.keys())
    for label, block in blocks.items():
        nwx__hhf = []
        mzhu__nsk = {ssho__wfokk.name for ssho__wfokk in block.terminator.
            list_vars()}
        for ygx__wzs, fqjz__buzx in rdf__vljky.successors(label):
            mzhu__nsk |= vva__hrd[ygx__wzs]
        for stmt in reversed(block.body):
            lrsum__xive = mzhu__nsk & alias_set
            for ssho__wfokk in lrsum__xive:
                mzhu__nsk |= alias_map[ssho__wfokk]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in mzhu__nsk and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                ofi__rhs = guard(find_callname, func_ir, stmt.value)
                if ofi__rhs == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in mzhu__nsk and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            mzhu__nsk |= {ssho__wfokk.name for ssho__wfokk in stmt.list_vars()}
            nwx__hhf.append(stmt)
        nwx__hhf.reverse()
        block.body = nwx__hhf
    typemap.pop(myuol__xxz.name)
    blocks[epmmo__flid].body.pop()
    otru__omn = True
    while otru__omn:
        """
        Process parfor body recursively.
        Note that this is the only place in this function that uses the
        argument lives instead of lives_n_aliases.  The former does not
        include the aliases of live variables but only the live variable
        names themselves.  See a comment in this function for how that
        is used.
        """
        remove_dead_parfor_recursive(parfor, lives, arg_aliases, alias_map,
            func_ir, typemap)
        simplify_parfor_body_CFG(func_ir.blocks)
        otru__omn = trim_empty_parfor_branches(parfor)
    obyhq__whm = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        obyhq__whm &= len(block.body) == 0
    if obyhq__whm:
        return None
    return parfor


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.remove_dead_parfor)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1c9b008a7ead13e988e1efe67618d8f87f0b9f3d092cc2cd6bfcd806b1fdb859':
        warnings.warn('remove_dead_parfor has changed')
numba.parfors.parfor.remove_dead_parfor = remove_dead_parfor
numba.core.ir_utils.remove_dead_extensions[numba.parfors.parfor.Parfor
    ] = remove_dead_parfor


def simplify_parfor_body_CFG(blocks):
    from numba.core.analysis import compute_cfg_from_blocks
    from numba.parfors.parfor import Parfor
    ybvkk__glaez = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                ybvkk__glaez += 1
                parfor = stmt
                omo__khvff = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = omo__khvff.scope
                loc = ir.Loc('parfors_dummy', -1)
                bjfzv__xuzu = ir.Var(scope, mk_unique_var('$const'), loc)
                omo__khvff.body.append(ir.Assign(ir.Const(0, loc),
                    bjfzv__xuzu, loc))
                omo__khvff.body.append(ir.Return(bjfzv__xuzu, loc))
                rdf__vljky = compute_cfg_from_blocks(parfor.loop_body)
                for zqv__imx in rdf__vljky.dead_nodes():
                    del parfor.loop_body[zqv__imx]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                omo__khvff = parfor.loop_body[max(parfor.loop_body.keys())]
                omo__khvff.body.pop()
                omo__khvff.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return ybvkk__glaez


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.simplify_parfor_body_CFG)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '437ae96a5e8ec64a2b69a4f23ba8402a1d170262a5400aa0aa7bfe59e03bf726':
        warnings.warn('simplify_parfor_body_CFG has changed')
numba.parfors.parfor.simplify_parfor_body_CFG = simplify_parfor_body_CFG


def simplify_CFG(blocks):
    from numba.core.analysis import compute_cfg_from_blocks
    from numba.core.ir_utils import merge_adjacent_blocks, rename_labels
    rdf__vljky = compute_cfg_from_blocks(blocks)

    def find_single_branch(label):
        block = blocks[label]
        return len(block.body) == 1 and isinstance(block.body[0], ir.Branch
            ) and label != rdf__vljky.entry_point()
    pwdx__eyhj = list(filter(find_single_branch, blocks.keys()))
    dmbh__hdcd = set()
    for label in pwdx__eyhj:
        inst = blocks[label].body[0]
        zrjx__udr = rdf__vljky.predecessors(label)
        rehcq__qeq = True
        for xjkb__fte, lksuk__igh in zrjx__udr:
            block = blocks[xjkb__fte]
            if isinstance(block.body[-1], ir.Jump):
                block.body[-1] = copy.copy(inst)
            else:
                rehcq__qeq = False
        if rehcq__qeq:
            dmbh__hdcd.add(label)
    for label in dmbh__hdcd:
        del blocks[label]
    merge_adjacent_blocks(blocks)
    return rename_labels(blocks)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.simplify_CFG)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '0b3f2add05e5691155f08fc5945956d5cca5e068247d52cff8efb161b76388b7':
        warnings.warn('numba.core.ir_utils.simplify_CFG has changed')
numba.core.ir_utils.simplify_CFG = simplify_CFG


def _lifted_compile(self, sig):
    import numba.core.event as ev
    from numba.core import compiler, sigutils
    from numba.core.compiler_lock import global_compiler_lock
    from numba.core.ir_utils import remove_dels
    with ExitStack() as scope:
        cres = None

        def cb_compiler(dur):
            if cres is not None:
                self._callback_add_compiler_timer(dur, cres)

        def cb_llvm(dur):
            if cres is not None:
                self._callback_add_llvm_timer(dur, cres)
        scope.enter_context(ev.install_timer('numba:compiler_lock',
            cb_compiler))
        scope.enter_context(ev.install_timer('numba:llvm_lock', cb_llvm))
        scope.enter_context(global_compiler_lock)
        with self._compiling_counter:
            flags = self.flags
            args, return_type = sigutils.normalize_signature(sig)
            wry__ulcl = self.overloads.get(tuple(args))
            if wry__ulcl is not None:
                return wry__ulcl.entry_point
            self._pre_compile(args, return_type, flags)
            qcup__txtb = self.func_ir
            uvmi__vrc = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=uvmi__vrc):
                cres = compiler.compile_ir(typingctx=self.typingctx,
                    targetctx=self.targetctx, func_ir=qcup__txtb, args=args,
                    return_type=return_type, flags=flags, locals=self.
                    locals, lifted=(), lifted_from=self.lifted_from,
                    is_lifted_loop=True)
                if cres.typing_error is not None and not flags.enable_pyobject:
                    raise cres.typing_error
                self.add_overload(cres)
            remove_dels(self.func_ir.blocks)
            return cres.entry_point


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.LiftedCode.compile)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1351ebc5d8812dc8da167b30dad30eafb2ca9bf191b49aaed6241c21e03afff1':
        warnings.warn('numba.core.dispatcher.LiftedCode.compile has changed')
numba.core.dispatcher.LiftedCode.compile = _lifted_compile


def compile_ir(typingctx, targetctx, func_ir, args, return_type, flags,
    locals, lifted=(), lifted_from=None, is_lifted_loop=False, library=None,
    pipeline_class=Compiler):
    if is_lifted_loop:
        dkqc__aej = copy.deepcopy(flags)
        dkqc__aej.no_rewrites = True

        def compile_local(the_ir, the_flags):
            yebl__gono = pipeline_class(typingctx, targetctx, library, args,
                return_type, the_flags, locals)
            return yebl__gono.compile_ir(func_ir=the_ir, lifted=lifted,
                lifted_from=lifted_from)
        lls__ydoq = compile_local(func_ir, dkqc__aej)
        wobec__snjme = None
        if not flags.no_rewrites:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', errors.NumbaWarning)
                try:
                    wobec__snjme = compile_local(func_ir, flags)
                except Exception as hegol__cwyf:
                    pass
        if wobec__snjme is not None:
            cres = wobec__snjme
        else:
            cres = lls__ydoq
        return cres
    else:
        yebl__gono = pipeline_class(typingctx, targetctx, library, args,
            return_type, flags, locals)
        return yebl__gono.compile_ir(func_ir=func_ir, lifted=lifted,
            lifted_from=lifted_from)


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.compile_ir)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c48ce5493f4c43326e8cbdd46f3ea038b2b9045352d9d25894244798388e5e5b':
        warnings.warn('numba.core.compiler.compile_ir has changed')
numba.core.compiler.compile_ir = compile_ir


def make_constant_array(self, builder, typ, ary):
    import math
    from llvmlite import ir as lir
    sviwa__sgjxk = self.get_data_type(typ.dtype)
    ygwrx__hpr = 10 ** 7
    if self.allow_dynamic_globals and (typ.layout not in 'FC' or ary.nbytes >
        ygwrx__hpr):
        yii__vsb = ary.ctypes.data
        wuhhn__knfst = self.add_dynamic_addr(builder, yii__vsb, info=str(
            type(yii__vsb)))
        ocx__ubgba = self.add_dynamic_addr(builder, id(ary), info=str(type(
            ary)))
        self.global_arrays.append(ary)
    else:
        mnpnl__xqrb = ary.flatten(order=typ.layout)
        if isinstance(typ.dtype, (types.NPDatetime, types.NPTimedelta)):
            mnpnl__xqrb = mnpnl__xqrb.view('int64')
        val = bytearray(mnpnl__xqrb.data)
        aut__uql = lir.Constant(lir.ArrayType(lir.IntType(8), len(val)), val)
        wuhhn__knfst = cgutils.global_constant(builder, '.const.array.data',
            aut__uql)
        wuhhn__knfst.align = self.get_abi_alignment(sviwa__sgjxk)
        ocx__ubgba = None
    sgnt__ivvu = self.get_value_type(types.intp)
    khev__zwlph = [self.get_constant(types.intp, kwvs__kvf) for kwvs__kvf in
        ary.shape]
    pceqa__uaipw = lir.Constant(lir.ArrayType(sgnt__ivvu, len(khev__zwlph)),
        khev__zwlph)
    lijcf__rnwxz = [self.get_constant(types.intp, kwvs__kvf) for kwvs__kvf in
        ary.strides]
    qzji__vzu = lir.Constant(lir.ArrayType(sgnt__ivvu, len(lijcf__rnwxz)),
        lijcf__rnwxz)
    wrtws__txv = self.get_constant(types.intp, ary.dtype.itemsize)
    qunsy__regy = self.get_constant(types.intp, math.prod(ary.shape))
    return lir.Constant.literal_struct([self.get_constant_null(types.
        MemInfoPointer(typ.dtype)), self.get_constant_null(types.pyobject),
        qunsy__regy, wrtws__txv, wuhhn__knfst.bitcast(self.get_value_type(
        types.CPointer(typ.dtype))), pceqa__uaipw, qzji__vzu])


if _check_numba_change:
    lines = inspect.getsource(numba.core.base.BaseContext.make_constant_array)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5721b5360b51f782f79bd794f7bf4d48657911ecdc05c30db22fd55f15dad821':
        warnings.warn(
            'numba.core.base.BaseContext.make_constant_array has changed')
numba.core.base.BaseContext.make_constant_array = make_constant_array


def _define_atomic_inc_dec(module, op, ordering):
    from llvmlite import ir as lir
    from numba.core.runtime.nrtdynmod import _word_type
    yophx__aoznj = lir.FunctionType(_word_type, [_word_type.as_pointer()])
    ewbw__pouut = lir.Function(module, yophx__aoznj, name='nrt_atomic_{0}'.
        format(op))
    [fns__wvz] = ewbw__pouut.args
    aaar__efj = ewbw__pouut.append_basic_block()
    builder = lir.IRBuilder(aaar__efj)
    mja__kdskb = lir.Constant(_word_type, 1)
    if False:
        onbmm__flcxp = builder.atomic_rmw(op, fns__wvz, mja__kdskb,
            ordering=ordering)
        res = getattr(builder, op)(onbmm__flcxp, mja__kdskb)
        builder.ret(res)
    else:
        onbmm__flcxp = builder.load(fns__wvz)
        zben__xsu = getattr(builder, op)(onbmm__flcxp, mja__kdskb)
        dzx__xrix = builder.icmp_signed('!=', onbmm__flcxp, lir.Constant(
            onbmm__flcxp.type, -1))
        with cgutils.if_likely(builder, dzx__xrix):
            builder.store(zben__xsu, fns__wvz)
        builder.ret(zben__xsu)
    return ewbw__pouut


if _check_numba_change:
    lines = inspect.getsource(numba.core.runtime.nrtdynmod.
        _define_atomic_inc_dec)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '9cc02c532b2980b6537b702f5608ea603a1ff93c6d3c785ae2cf48bace273f48':
        warnings.warn(
            'numba.core.runtime.nrtdynmod._define_atomic_inc_dec has changed')
numba.core.runtime.nrtdynmod._define_atomic_inc_dec = _define_atomic_inc_dec


def NativeLowering_run_pass(self, state):
    from llvmlite import binding as llvm
    from numba.core import funcdesc, lowering
    from numba.core.typed_passes import fallback_context
    if state.library is None:
        gdbng__sspwk = state.targetctx.codegen()
        state.library = gdbng__sspwk.create_library(state.func_id.func_qualname
            )
        state.library.enable_object_caching()
    library = state.library
    targetctx = state.targetctx
    skheq__hnzyl = state.func_ir
    typemap = state.typemap
    jhc__ycauy = state.return_type
    calltypes = state.calltypes
    flags = state.flags
    metadata = state.metadata
    emqb__cfmvn = llvm.passmanagers.dump_refprune_stats()
    msg = 'Function %s failed at nopython mode lowering' % (state.func_id.
        func_name,)
    with fallback_context(state, msg):
        fndesc = funcdesc.PythonFunctionDescriptor.from_specialized_function(
            skheq__hnzyl, typemap, jhc__ycauy, calltypes, mangler=targetctx
            .mangler, inline=flags.forceinline, noalias=flags.noalias,
            abi_tags=[flags.get_mangle_string()])
        targetctx.global_arrays = []
        with targetctx.push_code_library(library):
            qiv__ruv = lowering.Lower(targetctx, library, fndesc,
                skheq__hnzyl, metadata=metadata)
            qiv__ruv.lower()
            if not flags.no_cpython_wrapper:
                qiv__ruv.create_cpython_wrapper(flags.release_gil)
            if not flags.no_cfunc_wrapper:
                for t in state.args:
                    if isinstance(t, (types.Omitted, types.Generator)):
                        break
                else:
                    if isinstance(jhc__ycauy, (types.Optional, types.Generator)
                        ):
                        pass
                    else:
                        qiv__ruv.create_cfunc_wrapper()
            env = qiv__ruv.env
            slz__bst = qiv__ruv.call_helper
            del qiv__ruv
        from numba.core.compiler import _LowerResult
        if flags.no_compile:
            state['cr'] = _LowerResult(fndesc, slz__bst, cfunc=None, env=env)
        else:
            zwlfx__hlyj = targetctx.get_executable(library, fndesc, env)
            targetctx.insert_user_function(zwlfx__hlyj, fndesc, [library])
            state['cr'] = _LowerResult(fndesc, slz__bst, cfunc=zwlfx__hlyj,
                env=env)
        metadata['global_arrs'] = targetctx.global_arrays
        targetctx.global_arrays = []
        nesi__yavk = llvm.passmanagers.dump_refprune_stats()
        metadata['prune_stats'] = nesi__yavk - emqb__cfmvn
        metadata['llvm_pass_timings'] = library.recorded_timings
    return True


if _check_numba_change:
    lines = inspect.getsource(numba.core.typed_passes.NativeLowering.run_pass)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a777ce6ce1bb2b1cbaa3ac6c2c0e2adab69a9c23888dff5f1cbb67bfb176b5de':
        warnings.warn(
            'numba.core.typed_passes.NativeLowering.run_pass has changed')
numba.core.typed_passes.NativeLowering.run_pass = NativeLowering_run_pass


def _python_list_to_native(typ, obj, c, size, listptr, errorptr):
    from llvmlite import ir as lir
    from numba.core.boxing import _NumbaTypeHelper
    from numba.cpython import listobj

    def check_element_type(nth, itemobj, expected_typobj):
        rnmgg__cylaw = nth.typeof(itemobj)
        with c.builder.if_then(cgutils.is_null(c.builder, rnmgg__cylaw),
            likely=False):
            c.builder.store(cgutils.true_bit, errorptr)
            poewn__fsbel.do_break()
        hfp__tyl = c.builder.icmp_signed('!=', rnmgg__cylaw, expected_typobj)
        if not isinstance(typ.dtype, types.Optional):
            with c.builder.if_then(hfp__tyl, likely=False):
                c.builder.store(cgutils.true_bit, errorptr)
                c.pyapi.err_format('PyExc_TypeError',
                    "can't unbox heterogeneous list: %S != %S",
                    expected_typobj, rnmgg__cylaw)
                c.pyapi.decref(rnmgg__cylaw)
                poewn__fsbel.do_break()
        c.pyapi.decref(rnmgg__cylaw)
    fqj__sgo, list = listobj.ListInstance.allocate_ex(c.context, c.builder,
        typ, size)
    with c.builder.if_else(fqj__sgo, likely=True) as (qoag__ttio, mkj__lyh):
        with qoag__ttio:
            list.size = size
            indyj__uwgj = lir.Constant(size.type, 0)
            with c.builder.if_then(c.builder.icmp_signed('>', size,
                indyj__uwgj), likely=True):
                with _NumbaTypeHelper(c) as nth:
                    expected_typobj = nth.typeof(c.pyapi.list_getitem(obj,
                        indyj__uwgj))
                    with cgutils.for_range(c.builder, size) as poewn__fsbel:
                        itemobj = c.pyapi.list_getitem(obj, poewn__fsbel.index)
                        check_element_type(nth, itemobj, expected_typobj)
                        fol__quq = c.unbox(typ.dtype, itemobj)
                        with c.builder.if_then(fol__quq.is_error, likely=False
                            ):
                            c.builder.store(cgutils.true_bit, errorptr)
                            poewn__fsbel.do_break()
                        list.setitem(poewn__fsbel.index, fol__quq.value,
                            incref=False)
                    c.pyapi.decref(expected_typobj)
            if typ.reflected:
                list.parent = obj
            with c.builder.if_then(c.builder.not_(c.builder.load(errorptr)),
                likely=False):
                c.pyapi.object_set_private_data(obj, list.meminfo)
            list.set_dirty(False)
            c.builder.store(list.value, listptr)
        with mkj__lyh:
            c.builder.store(cgutils.true_bit, errorptr)
    with c.builder.if_then(c.builder.load(errorptr)):
        c.context.nrt.decref(c.builder, typ, list.value)


if _check_numba_change:
    lines = inspect.getsource(numba.core.boxing._python_list_to_native)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f8e546df8b07adfe74a16b6aafb1d4fddbae7d3516d7944b3247cc7c9b7ea88a':
        warnings.warn('numba.core.boxing._python_list_to_native has changed')
numba.core.boxing._python_list_to_native = _python_list_to_native


def make_string_from_constant(context, builder, typ, literal_string):
    from llvmlite import ir as lir
    from numba.cpython.hashing import _Py_hash_t
    from numba.cpython.unicode import compile_time_get_string_data
    uui__aoin, mesrj__nye, vex__qxc, zcure__phc, uyvp__emlrz = (
        compile_time_get_string_data(literal_string))
    hnkyp__ovtf = builder.module
    gv = context.insert_const_bytes(hnkyp__ovtf, uui__aoin)
    return lir.Constant.literal_struct([gv, context.get_constant(types.intp,
        mesrj__nye), context.get_constant(types.int32, vex__qxc), context.
        get_constant(types.uint32, zcure__phc), context.get_constant(
        _Py_hash_t, -1), context.get_constant_null(types.MemInfoPointer(
        types.voidptr)), context.get_constant_null(types.pyobject)])


if _check_numba_change:
    lines = inspect.getsource(numba.cpython.unicode.make_string_from_constant)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '525bd507383e06152763e2f046dae246cd60aba027184f50ef0fc9a80d4cd7fa':
        warnings.warn(
            'numba.cpython.unicode.make_string_from_constant has changed')
numba.cpython.unicode.make_string_from_constant = make_string_from_constant


def parse_shape(shape):
    kxg__dny = None
    if isinstance(shape, types.Integer):
        kxg__dny = 1
    elif isinstance(shape, (types.Tuple, types.UniTuple)):
        if all(isinstance(kwvs__kvf, (types.Integer, types.IntEnumMember)) for
            kwvs__kvf in shape):
            kxg__dny = len(shape)
    return kxg__dny


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.npydecl.parse_shape)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'e62e3ff09d36df5ac9374055947d6a8be27160ce32960d3ef6cb67f89bd16429':
        warnings.warn('numba.core.typing.npydecl.parse_shape has changed')
numba.core.typing.npydecl.parse_shape = parse_shape


def _get_names(self, obj):
    if isinstance(obj, ir.Var) or isinstance(obj, str):
        name = obj if isinstance(obj, str) else obj.name
        if name not in self.typemap:
            return name,
        typ = self.typemap[name]
        if isinstance(typ, (types.BaseTuple, types.ArrayCompatible)):
            kxg__dny = typ.ndim if isinstance(typ, types.ArrayCompatible
                ) else len(typ)
            if kxg__dny == 0:
                return name,
            else:
                return tuple('{}#{}'.format(name, i) for i in range(kxg__dny))
        else:
            return name,
    elif isinstance(obj, ir.Const):
        if isinstance(obj.value, tuple):
            return obj.value
        else:
            return obj.value,
    elif isinstance(obj, tuple):

        def get_names(x):
            rlyek__txrdd = self._get_names(x)
            if len(rlyek__txrdd) != 0:
                return rlyek__txrdd[0]
            return rlyek__txrdd
        return tuple(get_names(x) for x in obj)
    elif isinstance(obj, int):
        return obj,
    return ()


def get_equiv_const(self, obj):
    rlyek__txrdd = self._get_names(obj)
    if len(rlyek__txrdd) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_const(rlyek__txrdd[0])


def get_equiv_set(self, obj):
    rlyek__txrdd = self._get_names(obj)
    if len(rlyek__txrdd) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_set(rlyek__txrdd[0])


if _check_numba_change:
    for name, orig, new, hash in ((
        'numba.parfors.array_analysis.ShapeEquivSet._get_names', numba.
        parfors.array_analysis.ShapeEquivSet._get_names, _get_names,
        '8c9bf136109028d5445fd0a82387b6abeb70c23b20b41e2b50c34ba5359516ee'),
        ('numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const',
        numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const,
        get_equiv_const,
        'bef410ca31a9e29df9ee74a4a27d339cc332564e4a237828b8a4decf625ce44e'),
        ('numba.parfors.array_analysis.ShapeEquivSet.get_equiv_set', numba.
        parfors.array_analysis.ShapeEquivSet.get_equiv_set, get_equiv_set,
        'ec936d340c488461122eb74f28a28b88227cb1f1bca2b9ba3c19258cfe1eb40a')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
numba.parfors.array_analysis.ShapeEquivSet._get_names = _get_names
numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const = get_equiv_const
numba.parfors.array_analysis.ShapeEquivSet.get_equiv_set = get_equiv_set


def raise_on_unsupported_feature(func_ir, typemap):
    import numpy
    jnid__aqfdq = []
    for hui__czq in func_ir.arg_names:
        if hui__czq in typemap and isinstance(typemap[hui__czq], types.
            containers.UniTuple) and typemap[hui__czq].count > 1000:
            msg = (
                """Tuple '{}' length must be smaller than 1000.
Large tuples lead to the generation of a prohibitively large LLVM IR which causes excessive memory pressure and large compile times.
As an alternative, the use of a 'list' is recommended in place of a 'tuple' as lists do not suffer from this problem."""
                .format(hui__czq))
            raise errors.UnsupportedError(msg, func_ir.loc)
    for nig__pwks in func_ir.blocks.values():
        for stmt in nig__pwks.find_insts(ir.Assign):
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'make_function':
                    val = stmt.value
                    ptpkf__gbq = getattr(val, 'code', None)
                    if ptpkf__gbq is not None:
                        if getattr(val, 'closure', None) is not None:
                            kumf__jiaq = '<creating a function from a closure>'
                            vxi__gcf = ''
                        else:
                            kumf__jiaq = ptpkf__gbq.co_name
                            vxi__gcf = '(%s) ' % kumf__jiaq
                    else:
                        kumf__jiaq = '<could not ascertain use case>'
                        vxi__gcf = ''
                    msg = (
                        'Numba encountered the use of a language feature it does not support in this context: %s (op code: make_function not supported). If the feature is explicitly supported it is likely that the result of the expression %sis being used in an unsupported manner.'
                         % (kumf__jiaq, vxi__gcf))
                    raise errors.UnsupportedError(msg, stmt.value.loc)
            if isinstance(stmt.value, (ir.Global, ir.FreeVar)):
                val = stmt.value
                val = getattr(val, 'value', None)
                if val is None:
                    continue
                nmm__hjfn = False
                if isinstance(val, pytypes.FunctionType):
                    nmm__hjfn = val in {numba.gdb, numba.gdb_init}
                if not nmm__hjfn:
                    nmm__hjfn = getattr(val, '_name', '') == 'gdb_internal'
                if nmm__hjfn:
                    jnid__aqfdq.append(stmt.loc)
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'getattr' and stmt.value.attr == 'view':
                    var = stmt.value.value.name
                    if isinstance(typemap[var], types.Array):
                        continue
                    sipq__yoa = func_ir.get_definition(var)
                    lhn__agzac = guard(find_callname, func_ir, sipq__yoa)
                    if lhn__agzac and lhn__agzac[1] == 'numpy':
                        ty = getattr(numpy, lhn__agzac[0])
                        if numpy.issubdtype(ty, numpy.integer
                            ) or numpy.issubdtype(ty, numpy.floating):
                            continue
                    saxy__ztw = '' if var.startswith('$') else "'{}' ".format(
                        var)
                    raise TypingError(
                        "'view' can only be called on NumPy dtypes, try wrapping the variable {}with 'np.<dtype>()'"
                        .format(saxy__ztw), loc=stmt.loc)
            if isinstance(stmt.value, ir.Global):
                ty = typemap[stmt.target.name]
                msg = (
                    "The use of a %s type, assigned to variable '%s' in globals, is not supported as globals are considered compile-time constants and there is no known way to compile a %s type as a constant."
                    )
                if isinstance(ty, types.ListType):
                    raise TypingError(msg % (ty, stmt.value.name, ty), loc=
                        stmt.loc)
            if isinstance(stmt.value, ir.Yield) and not func_ir.is_generator:
                msg = 'The use of generator expressions is unsupported.'
                raise errors.UnsupportedError(msg, loc=stmt.loc)
    if len(jnid__aqfdq) > 1:
        msg = """Calling either numba.gdb() or numba.gdb_init() more than once in a function is unsupported (strange things happen!), use numba.gdb_breakpoint() to create additional breakpoints instead.

Relevant documentation is available here:
https://numba.pydata.org/numba-doc/latest/user/troubleshoot.html/troubleshoot.html#using-numba-s-direct-gdb-bindings-in-nopython-mode

Conflicting calls found at:
 %s"""
        mjf__zigr = '\n'.join([x.strformat() for x in jnid__aqfdq])
        raise errors.UnsupportedError(msg % mjf__zigr)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.raise_on_unsupported_feature)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '237a4fe8395a40899279c718bc3754102cd2577463ef2f48daceea78d79b2d5e':
        warnings.warn(
            'numba.core.ir_utils.raise_on_unsupported_feature has changed')
numba.core.ir_utils.raise_on_unsupported_feature = raise_on_unsupported_feature
numba.core.typed_passes.raise_on_unsupported_feature = (
    raise_on_unsupported_feature)


@typeof_impl.register(dict)
def _typeof_dict(val, c):
    if len(val) == 0:
        raise ValueError('Cannot type empty dict')
    ikm__tie, ssho__wfokk = next(iter(val.items()))
    hnijb__ifd = typeof_impl(ikm__tie, c)
    lbfj__floa = typeof_impl(ssho__wfokk, c)
    if hnijb__ifd is None or lbfj__floa is None:
        raise ValueError(
            f'Cannot type dict element type {type(ikm__tie)}, {type(ssho__wfokk)}'
            )
    return types.DictType(hnijb__ifd, lbfj__floa)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    qcuso__skb = cgutils.alloca_once_value(c.builder, val)
    yfvjl__zqfik = c.pyapi.object_hasattr_string(val, '_opaque')
    bwu__mii = c.builder.icmp_unsigned('==', yfvjl__zqfik, lir.Constant(
        yfvjl__zqfik.type, 0))
    zbj__hlsc = typ.key_type
    nofh__zrws = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(zbj__hlsc, nofh__zrws)

    def copy_dict(out_dict, in_dict):
        for ikm__tie, ssho__wfokk in in_dict.items():
            out_dict[ikm__tie] = ssho__wfokk
    with c.builder.if_then(bwu__mii):
        naz__tgwv = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        may__lsz = c.pyapi.call_function_objargs(naz__tgwv, [])
        oqgm__cqq = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(oqgm__cqq, [may__lsz, val])
        c.builder.store(may__lsz, qcuso__skb)
    val = c.builder.load(qcuso__skb)
    jqjp__ebe = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    zli__zbd = c.pyapi.object_type(val)
    djavn__ynj = c.builder.icmp_unsigned('==', zli__zbd, jqjp__ebe)
    with c.builder.if_else(djavn__ynj) as (yuv__qep, ogpjt__nps):
        with yuv__qep:
            hltwl__dmg = c.pyapi.object_getattr_string(val, '_opaque')
            orlrv__duetv = types.MemInfoPointer(types.voidptr)
            fol__quq = c.unbox(orlrv__duetv, hltwl__dmg)
            mi = fol__quq.value
            rsi__ohpek = orlrv__duetv, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *rsi__ohpek)
            vtup__rbjis = context.get_constant_null(rsi__ohpek[1])
            args = mi, vtup__rbjis
            fdh__migp, fzd__twnso = c.pyapi.call_jit_code(convert, sig, args)
            c.context.nrt.decref(c.builder, typ, fzd__twnso)
            c.pyapi.decref(hltwl__dmg)
            vcxgh__beu = c.builder.basic_block
        with ogpjt__nps:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", zli__zbd, jqjp__ebe)
            kqu__niy = c.builder.basic_block
    zvweq__gln = c.builder.phi(fzd__twnso.type)
    bfn__anm = c.builder.phi(fdh__migp.type)
    zvweq__gln.add_incoming(fzd__twnso, vcxgh__beu)
    zvweq__gln.add_incoming(fzd__twnso.type(None), kqu__niy)
    bfn__anm.add_incoming(fdh__migp, vcxgh__beu)
    bfn__anm.add_incoming(cgutils.true_bit, kqu__niy)
    c.pyapi.decref(jqjp__ebe)
    c.pyapi.decref(zli__zbd)
    with c.builder.if_then(bwu__mii):
        c.pyapi.decref(val)
    return NativeValue(zvweq__gln, is_error=bfn__anm)


import numba.typed.typeddict
if _check_numba_change:
    lines = inspect.getsource(numba.core.pythonapi._unboxers.functions[
        numba.core.types.DictType])
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5f6f183b94dc57838538c668a54c2476576c85d8553843f3219f5162c61e7816':
        warnings.warn('unbox_dicttype has changed')
numba.core.pythonapi._unboxers.functions[types.DictType] = unbox_dicttype


def op_DICT_UPDATE_byteflow(self, state, inst):
    value = state.pop()
    index = inst.arg
    target = state.peek(index)
    updatevar = state.make_temp()
    res = state.make_temp()
    state.append(inst, target=target, value=value, updatevar=updatevar, res=res
        )


if _check_numba_change:
    if hasattr(numba.core.byteflow.TraceRunner, 'op_DICT_UPDATE'):
        warnings.warn(
            'numba.core.byteflow.TraceRunner.op_DICT_UPDATE has changed')
numba.core.byteflow.TraceRunner.op_DICT_UPDATE = op_DICT_UPDATE_byteflow


def op_DICT_UPDATE_interpreter(self, inst, target, value, updatevar, res):
    from numba.core import ir
    target = self.get(target)
    value = self.get(value)
    lhiin__woyj = ir.Expr.getattr(target, 'update', loc=self.loc)
    self.store(value=lhiin__woyj, name=updatevar)
    yupnm__tsdx = ir.Expr.call(self.get(updatevar), (value,), (), loc=self.loc)
    self.store(value=yupnm__tsdx, name=res)


if _check_numba_change:
    if hasattr(numba.core.interpreter.Interpreter, 'op_DICT_UPDATE'):
        warnings.warn(
            'numba.core.interpreter.Interpreter.op_DICT_UPDATE has changed')
numba.core.interpreter.Interpreter.op_DICT_UPDATE = op_DICT_UPDATE_interpreter


@numba.extending.overload_method(numba.core.types.DictType, 'update')
def ol_dict_update(d, other):
    if not isinstance(d, numba.core.types.DictType):
        return
    if not isinstance(other, numba.core.types.DictType):
        return

    def impl(d, other):
        for ikm__tie, ssho__wfokk in other.items():
            d[ikm__tie] = ssho__wfokk
    return impl


if _check_numba_change:
    if hasattr(numba.core.interpreter.Interpreter, 'ol_dict_update'):
        warnings.warn('numba.typed.dictobject.ol_dict_update has changed')


def op_CALL_FUNCTION_EX_byteflow(self, state, inst):
    from numba.core.utils import PYVERSION
    if inst.arg & 1 and PYVERSION != (3, 10):
        errmsg = 'CALL_FUNCTION_EX with **kwargs not supported'
        raise errors.UnsupportedError(errmsg)
    if inst.arg & 1:
        varkwarg = state.pop()
    else:
        varkwarg = None
    vararg = state.pop()
    func = state.pop()
    res = state.make_temp()
    state.append(inst, func=func, vararg=vararg, varkwarg=varkwarg, res=res)
    state.push(res)


if _check_numba_change:
    lines = inspect.getsource(numba.core.byteflow.TraceRunner.
        op_CALL_FUNCTION_EX)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '349e7cfd27f5dab80fe15a7728c5f098f3f225ba8512d84331e39d01e863c6d4':
        warnings.warn(
            'numba.core.byteflow.TraceRunner.op_CALL_FUNCTION_EX has changed')
numba.core.byteflow.TraceRunner.op_CALL_FUNCTION_EX = (
    op_CALL_FUNCTION_EX_byteflow)


def op_CALL_FUNCTION_EX_interpreter(self, inst, func, vararg, varkwarg, res):
    func = self.get(func)
    vararg = self.get(vararg)
    if varkwarg is not None:
        varkwarg = self.get(varkwarg)
    vxi__gcf = ir.Expr.call(func, [], [], loc=self.loc, vararg=vararg,
        varkwarg=varkwarg)
    self.store(vxi__gcf, res)


if _check_numba_change:
    lines = inspect.getsource(numba.core.interpreter.Interpreter.
        op_CALL_FUNCTION_EX)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '84846e5318ab7ccc8f9abaae6ab9e0ca879362648196f9d4b0ffb91cf2e01f5d':
        warnings.warn(
            'numba.core.interpreter.Interpreter.op_CALL_FUNCTION_EX has changed'
            )
numba.core.interpreter.Interpreter.op_CALL_FUNCTION_EX = (
    op_CALL_FUNCTION_EX_interpreter)


@classmethod
def ir_expr_call(cls, func, args, kws, loc, vararg=None, varkwarg=None,
    target=None):
    assert isinstance(func, ir.Var)
    assert isinstance(loc, ir.Loc)
    op = 'call'
    return cls(op=op, loc=loc, func=func, args=args, kws=kws, vararg=vararg,
        varkwarg=varkwarg, target=target)


if _check_numba_change:
    lines = inspect.getsource(ir.Expr.call)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '665601d0548d4f648d454492e542cb8aa241107a8df6bc68d0eec664c9ada738':
        warnings.warn('ir.Expr.call has changed')
ir.Expr.call = ir_expr_call


@staticmethod
def define_untyped_pipeline(state, name='untyped'):
    from numba.core.compiler_machinery import PassManager
    from numba.core.untyped_passes import DeadBranchPrune, FindLiterallyCalls, FixupArgs, GenericRewrites, InlineClosureLikes, InlineInlinables, IRProcessing, LiteralPropagationSubPipelinePass, LiteralUnroll, MakeFunctionToJitFunction, ReconstructSSA, RewriteSemanticConstants, TranslateByteCode, WithLifting
    from numba.core.utils import PYVERSION
    ihoji__wjx = PassManager(name)
    if state.func_ir is None:
        ihoji__wjx.add_pass(TranslateByteCode, 'analyzing bytecode')
        if PYVERSION == (3, 10):
            ihoji__wjx.add_pass(Bodo310ByteCodePass,
                'Apply Python 3.10 bytecode changes')
        ihoji__wjx.add_pass(FixupArgs, 'fix up args')
    ihoji__wjx.add_pass(IRProcessing, 'processing IR')
    ihoji__wjx.add_pass(WithLifting, 'Handle with contexts')
    ihoji__wjx.add_pass(InlineClosureLikes,
        'inline calls to locally defined closures')
    if not state.flags.no_rewrites:
        ihoji__wjx.add_pass(RewriteSemanticConstants,
            'rewrite semantic constants')
        ihoji__wjx.add_pass(DeadBranchPrune, 'dead branch pruning')
        ihoji__wjx.add_pass(GenericRewrites, 'nopython rewrites')
    ihoji__wjx.add_pass(MakeFunctionToJitFunction,
        'convert make_function into JIT functions')
    ihoji__wjx.add_pass(InlineInlinables, 'inline inlinable functions')
    if not state.flags.no_rewrites:
        ihoji__wjx.add_pass(DeadBranchPrune, 'dead branch pruning')
    ihoji__wjx.add_pass(FindLiterallyCalls, 'find literally calls')
    ihoji__wjx.add_pass(LiteralUnroll, 'handles literal_unroll')
    if state.flags.enable_ssa:
        ihoji__wjx.add_pass(ReconstructSSA, 'ssa')
    ihoji__wjx.add_pass(LiteralPropagationSubPipelinePass,
        'Literal propagation')
    ihoji__wjx.finalize()
    return ihoji__wjx


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'fc5a0665658cc30588a78aca984ac2d323d5d3a45dce538cc62688530c772896':
        warnings.warn(
            'numba.core.compiler.DefaultPassBuilder.define_untyped_pipeline has changed'
            )
numba.core.compiler.DefaultPassBuilder.define_untyped_pipeline = (
    define_untyped_pipeline)


def mul_list_generic(self, args, kws):
    a, eua__ksixs = args
    if isinstance(a, types.List) and isinstance(eua__ksixs, types.Integer):
        return signature(a, a, types.intp)
    elif isinstance(a, types.Integer) and isinstance(eua__ksixs, types.List):
        return signature(eua__ksixs, types.intp, eua__ksixs)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.listdecl.MulList.generic)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '95882385a8ffa67aa576e8169b9ee6b3197e0ad3d5def4b47fa65ce8cd0f1575':
        warnings.warn('numba.core.typing.listdecl.MulList.generic has changed')
numba.core.typing.listdecl.MulList.generic = mul_list_generic


@lower_builtin(operator.mul, types.Integer, types.List)
def list_mul(context, builder, sig, args):
    from llvmlite import ir as lir
    from numba.core.imputils import impl_ret_new_ref
    from numba.cpython.listobj import ListInstance
    if isinstance(sig.args[0], types.List):
        iih__njp, lvkn__tpmx = 0, 1
    else:
        iih__njp, lvkn__tpmx = 1, 0
    idj__rmux = ListInstance(context, builder, sig.args[iih__njp], args[
        iih__njp])
    eudi__nggef = idj__rmux.size
    dmfaj__escvu = args[lvkn__tpmx]
    indyj__uwgj = lir.Constant(dmfaj__escvu.type, 0)
    dmfaj__escvu = builder.select(cgutils.is_neg_int(builder, dmfaj__escvu),
        indyj__uwgj, dmfaj__escvu)
    qunsy__regy = builder.mul(dmfaj__escvu, eudi__nggef)
    jybfi__dfkqq = ListInstance.allocate(context, builder, sig.return_type,
        qunsy__regy)
    jybfi__dfkqq.size = qunsy__regy
    with cgutils.for_range_slice(builder, indyj__uwgj, qunsy__regy,
        eudi__nggef, inc=True) as (mfsa__xhbub, _):
        with cgutils.for_range(builder, eudi__nggef) as poewn__fsbel:
            value = idj__rmux.getitem(poewn__fsbel.index)
            jybfi__dfkqq.setitem(builder.add(poewn__fsbel.index,
                mfsa__xhbub), value, incref=True)
    return impl_ret_new_ref(context, builder, sig.return_type, jybfi__dfkqq
        .value)


def unify_pairs(self, first, second):
    from numba.core.typeconv import Conversion
    if first == second:
        return first
    if first is types.undefined:
        return second
    elif second is types.undefined:
        return first
    if first is types.unknown or second is types.unknown:
        return types.unknown
    eyph__hms = first.unify(self, second)
    if eyph__hms is not None:
        return eyph__hms
    eyph__hms = second.unify(self, first)
    if eyph__hms is not None:
        return eyph__hms
    jvmp__ihtp = self.can_convert(fromty=first, toty=second)
    if jvmp__ihtp is not None and jvmp__ihtp <= Conversion.safe:
        return second
    jvmp__ihtp = self.can_convert(fromty=second, toty=first)
    if jvmp__ihtp is not None and jvmp__ihtp <= Conversion.safe:
        return first
    if isinstance(first, types.Literal) or isinstance(second, types.Literal):
        first = types.unliteral(first)
        second = types.unliteral(second)
        return self.unify_pairs(first, second)
    return None


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.context.BaseContext.unify_pairs
        )
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f0eaf4cfdf1537691de26efd24d7e320f7c3f10d35e9aefe70cb946b3be0008c':
        warnings.warn(
            'numba.core.typing.context.BaseContext.unify_pairs has changed')
numba.core.typing.context.BaseContext.unify_pairs = unify_pairs


def _native_set_to_python_list(typ, payload, c):
    from llvmlite import ir
    qunsy__regy = payload.used
    listobj = c.pyapi.list_new(qunsy__regy)
    fqj__sgo = cgutils.is_not_null(c.builder, listobj)
    with c.builder.if_then(fqj__sgo, likely=True):
        index = cgutils.alloca_once_value(c.builder, ir.Constant(
            qunsy__regy.type, 0))
        with payload._iterate() as poewn__fsbel:
            i = c.builder.load(index)
            item = poewn__fsbel.entry.key
            c.context.nrt.incref(c.builder, typ.dtype, item)
            itemobj = c.box(typ.dtype, item)
            c.pyapi.list_setitem(listobj, i, itemobj)
            i = c.builder.add(i, ir.Constant(i.type, 1))
            c.builder.store(i, index)
    return fqj__sgo, listobj


def _lookup(self, item, h, for_insert=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    nubsu__oywxu = h.type
    yyy__opbdp = self.mask
    dtype = self._ty.dtype
    nov__yrfql = context.typing_context
    fnty = nov__yrfql.resolve_value_type(operator.eq)
    sig = fnty.get_call_type(nov__yrfql, (dtype, dtype), {})
    munr__ypd = context.get_function(fnty, sig)
    pihad__wdh = ir.Constant(nubsu__oywxu, 1)
    invqo__bnb = ir.Constant(nubsu__oywxu, 5)
    xehku__kjkac = cgutils.alloca_once_value(builder, h)
    index = cgutils.alloca_once_value(builder, builder.and_(h, yyy__opbdp))
    if for_insert:
        xzr__pdus = yyy__opbdp.type(-1)
        lrrlt__gyc = cgutils.alloca_once_value(builder, xzr__pdus)
    rymk__avn = builder.append_basic_block('lookup.body')
    zpu__jipqv = builder.append_basic_block('lookup.found')
    yvam__biy = builder.append_basic_block('lookup.not_found')
    wmoz__mwawz = builder.append_basic_block('lookup.end')

    def check_entry(i):
        entry = self.get_entry(i)
        axau__uveyy = entry.hash
        with builder.if_then(builder.icmp_unsigned('==', h, axau__uveyy)):
            ghxjh__owc = munr__ypd(builder, (item, entry.key))
            with builder.if_then(ghxjh__owc):
                builder.branch(zpu__jipqv)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, axau__uveyy)):
            builder.branch(yvam__biy)
        if for_insert:
            with builder.if_then(numba.cpython.setobj.is_hash_deleted(
                context, builder, axau__uveyy)):
                vnjcq__dfd = builder.load(lrrlt__gyc)
                vnjcq__dfd = builder.select(builder.icmp_unsigned('==',
                    vnjcq__dfd, xzr__pdus), i, vnjcq__dfd)
                builder.store(vnjcq__dfd, lrrlt__gyc)
    with cgutils.for_range(builder, ir.Constant(nubsu__oywxu, numba.cpython
        .setobj.LINEAR_PROBES)):
        i = builder.load(index)
        check_entry(i)
        i = builder.add(i, pihad__wdh)
        i = builder.and_(i, yyy__opbdp)
        builder.store(i, index)
    builder.branch(rymk__avn)
    with builder.goto_block(rymk__avn):
        i = builder.load(index)
        check_entry(i)
        xjkb__fte = builder.load(xehku__kjkac)
        xjkb__fte = builder.lshr(xjkb__fte, invqo__bnb)
        i = builder.add(pihad__wdh, builder.mul(i, invqo__bnb))
        i = builder.and_(yyy__opbdp, builder.add(i, xjkb__fte))
        builder.store(i, index)
        builder.store(xjkb__fte, xehku__kjkac)
        builder.branch(rymk__avn)
    with builder.goto_block(yvam__biy):
        if for_insert:
            i = builder.load(index)
            vnjcq__dfd = builder.load(lrrlt__gyc)
            i = builder.select(builder.icmp_unsigned('==', vnjcq__dfd,
                xzr__pdus), i, vnjcq__dfd)
            builder.store(i, index)
        builder.branch(wmoz__mwawz)
    with builder.goto_block(zpu__jipqv):
        builder.branch(wmoz__mwawz)
    builder.position_at_end(wmoz__mwawz)
    nmm__hjfn = builder.phi(ir.IntType(1), 'found')
    nmm__hjfn.add_incoming(cgutils.true_bit, zpu__jipqv)
    nmm__hjfn.add_incoming(cgutils.false_bit, yvam__biy)
    return nmm__hjfn, builder.load(index)


def _add_entry(self, payload, entry, item, h, do_resize=True):
    context = self._context
    builder = self._builder
    xjocr__gmwmr = entry.hash
    entry.hash = h
    context.nrt.incref(builder, self._ty.dtype, item)
    entry.key = item
    tmh__lbaek = payload.used
    pihad__wdh = ir.Constant(tmh__lbaek.type, 1)
    tmh__lbaek = payload.used = builder.add(tmh__lbaek, pihad__wdh)
    with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
        builder, xjocr__gmwmr), likely=True):
        payload.fill = builder.add(payload.fill, pihad__wdh)
    if do_resize:
        self.upsize(tmh__lbaek)
    self.set_dirty(True)


def _add_key(self, payload, item, h, do_resize=True):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    nmm__hjfn, i = payload._lookup(item, h, for_insert=True)
    qguui__ktot = builder.not_(nmm__hjfn)
    with builder.if_then(qguui__ktot):
        entry = payload.get_entry(i)
        xjocr__gmwmr = entry.hash
        entry.hash = h
        context.nrt.incref(builder, self._ty.dtype, item)
        entry.key = item
        tmh__lbaek = payload.used
        pihad__wdh = ir.Constant(tmh__lbaek.type, 1)
        tmh__lbaek = payload.used = builder.add(tmh__lbaek, pihad__wdh)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, xjocr__gmwmr), likely=True):
            payload.fill = builder.add(payload.fill, pihad__wdh)
        if do_resize:
            self.upsize(tmh__lbaek)
        self.set_dirty(True)


def _remove_entry(self, payload, entry, do_resize=True):
    from llvmlite import ir
    entry.hash = ir.Constant(entry.hash.type, numba.cpython.setobj.DELETED)
    self._context.nrt.decref(self._builder, self._ty.dtype, entry.key)
    tmh__lbaek = payload.used
    pihad__wdh = ir.Constant(tmh__lbaek.type, 1)
    tmh__lbaek = payload.used = self._builder.sub(tmh__lbaek, pihad__wdh)
    if do_resize:
        self.downsize(tmh__lbaek)
    self.set_dirty(True)


def pop(self):
    context = self._context
    builder = self._builder
    agxx__albw = context.get_value_type(self._ty.dtype)
    key = cgutils.alloca_once(builder, agxx__albw)
    payload = self.payload
    with payload._next_entry() as entry:
        builder.store(entry.key, key)
        context.nrt.incref(builder, self._ty.dtype, entry.key)
        self._remove_entry(payload, entry)
    return builder.load(key)


def _resize(self, payload, nentries, errmsg):
    context = self._context
    builder = self._builder
    bdpfl__omzh = payload
    fqj__sgo = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(fqj__sgo), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (errmsg,))
    payload = self.payload
    with bdpfl__omzh._iterate() as poewn__fsbel:
        entry = poewn__fsbel.entry
        self._add_key(payload, entry.key, entry.hash, do_resize=False)
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(bdpfl__omzh.ptr)


def _replace_payload(self, nentries):
    context = self._context
    builder = self._builder
    with self.payload._iterate() as poewn__fsbel:
        entry = poewn__fsbel.entry
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(self.payload.ptr)
    fqj__sgo = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(fqj__sgo), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (
            'cannot reallocate set',))


def _allocate_payload(self, nentries, realloc=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    fqj__sgo = cgutils.alloca_once_value(builder, cgutils.true_bit)
    nubsu__oywxu = context.get_value_type(types.intp)
    indyj__uwgj = ir.Constant(nubsu__oywxu, 0)
    pihad__wdh = ir.Constant(nubsu__oywxu, 1)
    ltmi__rfwy = context.get_data_type(types.SetPayload(self._ty))
    expjs__ibg = context.get_abi_sizeof(ltmi__rfwy)
    jbcx__nkjga = self._entrysize
    expjs__ibg -= jbcx__nkjga
    vqdi__gfr, oqrus__prg = cgutils.muladd_with_overflow(builder, nentries,
        ir.Constant(nubsu__oywxu, jbcx__nkjga), ir.Constant(nubsu__oywxu,
        expjs__ibg))
    with builder.if_then(oqrus__prg, likely=False):
        builder.store(cgutils.false_bit, fqj__sgo)
    with builder.if_then(builder.load(fqj__sgo), likely=True):
        if realloc:
            kzyu__biacj = self._set.meminfo
            fns__wvz = context.nrt.meminfo_varsize_alloc(builder,
                kzyu__biacj, size=vqdi__gfr)
            egfhk__rqw = cgutils.is_null(builder, fns__wvz)
        else:
            dka__kgze = _imp_dtor(context, builder.module, self._ty)
            kzyu__biacj = context.nrt.meminfo_new_varsize_dtor(builder,
                vqdi__gfr, builder.bitcast(dka__kgze, cgutils.voidptr_t))
            egfhk__rqw = cgutils.is_null(builder, kzyu__biacj)
        with builder.if_else(egfhk__rqw, likely=False) as (ftehs__avwy,
            qoag__ttio):
            with ftehs__avwy:
                builder.store(cgutils.false_bit, fqj__sgo)
            with qoag__ttio:
                if not realloc:
                    self._set.meminfo = kzyu__biacj
                    self._set.parent = context.get_constant_null(types.pyobject
                        )
                payload = self.payload
                cgutils.memset(builder, payload.ptr, vqdi__gfr, 255)
                payload.used = indyj__uwgj
                payload.fill = indyj__uwgj
                payload.finger = indyj__uwgj
                tbh__tqw = builder.sub(nentries, pihad__wdh)
                payload.mask = tbh__tqw
    return builder.load(fqj__sgo)


def _copy_payload(self, src_payload):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    fqj__sgo = cgutils.alloca_once_value(builder, cgutils.true_bit)
    nubsu__oywxu = context.get_value_type(types.intp)
    indyj__uwgj = ir.Constant(nubsu__oywxu, 0)
    pihad__wdh = ir.Constant(nubsu__oywxu, 1)
    ltmi__rfwy = context.get_data_type(types.SetPayload(self._ty))
    expjs__ibg = context.get_abi_sizeof(ltmi__rfwy)
    jbcx__nkjga = self._entrysize
    expjs__ibg -= jbcx__nkjga
    yyy__opbdp = src_payload.mask
    nentries = builder.add(pihad__wdh, yyy__opbdp)
    vqdi__gfr = builder.add(ir.Constant(nubsu__oywxu, expjs__ibg), builder.
        mul(ir.Constant(nubsu__oywxu, jbcx__nkjga), nentries))
    with builder.if_then(builder.load(fqj__sgo), likely=True):
        dka__kgze = _imp_dtor(context, builder.module, self._ty)
        kzyu__biacj = context.nrt.meminfo_new_varsize_dtor(builder,
            vqdi__gfr, builder.bitcast(dka__kgze, cgutils.voidptr_t))
        egfhk__rqw = cgutils.is_null(builder, kzyu__biacj)
        with builder.if_else(egfhk__rqw, likely=False) as (ftehs__avwy,
            qoag__ttio):
            with ftehs__avwy:
                builder.store(cgutils.false_bit, fqj__sgo)
            with qoag__ttio:
                self._set.meminfo = kzyu__biacj
                payload = self.payload
                payload.used = src_payload.used
                payload.fill = src_payload.fill
                payload.finger = indyj__uwgj
                payload.mask = yyy__opbdp
                cgutils.raw_memcpy(builder, payload.entries, src_payload.
                    entries, nentries, jbcx__nkjga)
                with src_payload._iterate() as poewn__fsbel:
                    context.nrt.incref(builder, self._ty.dtype,
                        poewn__fsbel.entry.key)
    return builder.load(fqj__sgo)


def _imp_dtor(context, module, set_type):
    from llvmlite import ir
    gpoh__vbso = context.get_value_type(types.voidptr)
    drzaw__qvf = context.get_value_type(types.uintp)
    fnty = ir.FunctionType(ir.VoidType(), [gpoh__vbso, drzaw__qvf, gpoh__vbso])
    rdwiq__izgt = f'_numba_set_dtor_{set_type}'
    fn = cgutils.get_or_insert_function(module, fnty, name=rdwiq__izgt)
    if fn.is_declaration:
        fn.linkage = 'linkonce_odr'
        builder = ir.IRBuilder(fn.append_basic_block())
        hwcyd__hzm = builder.bitcast(fn.args[0], cgutils.voidptr_t.as_pointer()
            )
        payload = numba.cpython.setobj._SetPayload(context, builder,
            set_type, hwcyd__hzm)
        with payload._iterate() as poewn__fsbel:
            entry = poewn__fsbel.entry
            context.nrt.decref(builder, set_type.dtype, entry.key)
        builder.ret_void()
    return fn


@lower_builtin(set, types.IterableType)
def set_constructor(context, builder, sig, args):
    set_type = sig.return_type
    txhd__wgwcr, = sig.args
    hkl__fosc, = args
    dry__dxrhk = numba.core.imputils.call_len(context, builder, txhd__wgwcr,
        hkl__fosc)
    inst = numba.cpython.setobj.SetInstance.allocate(context, builder,
        set_type, dry__dxrhk)
    with numba.core.imputils.for_iter(context, builder, txhd__wgwcr, hkl__fosc
        ) as poewn__fsbel:
        inst.add(poewn__fsbel.value)
        context.nrt.decref(builder, set_type.dtype, poewn__fsbel.value)
    return numba.core.imputils.impl_ret_new_ref(context, builder, set_type,
        inst.value)


@lower_builtin('set.update', types.Set, types.IterableType)
def set_update(context, builder, sig, args):
    inst = numba.cpython.setobj.SetInstance(context, builder, sig.args[0],
        args[0])
    txhd__wgwcr = sig.args[1]
    hkl__fosc = args[1]
    dry__dxrhk = numba.core.imputils.call_len(context, builder, txhd__wgwcr,
        hkl__fosc)
    if dry__dxrhk is not None:
        yaw__xrqr = builder.add(inst.payload.used, dry__dxrhk)
        inst.upsize(yaw__xrqr)
    with numba.core.imputils.for_iter(context, builder, txhd__wgwcr, hkl__fosc
        ) as poewn__fsbel:
        egqgt__wts = context.cast(builder, poewn__fsbel.value, txhd__wgwcr.
            dtype, inst.dtype)
        inst.add(egqgt__wts)
        context.nrt.decref(builder, txhd__wgwcr.dtype, poewn__fsbel.value)
    if dry__dxrhk is not None:
        inst.downsize(inst.payload.used)
    return context.get_dummy_value()


if _check_numba_change:
    for name, orig, hash in ((
        'numba.core.boxing._native_set_to_python_list', numba.core.boxing.
        _native_set_to_python_list,
        'b47f3d5e582c05d80899ee73e1c009a7e5121e7a660d42cb518bb86933f3c06f'),
        ('numba.cpython.setobj._SetPayload._lookup', numba.cpython.setobj.
        _SetPayload._lookup,
        'c797b5399d7b227fe4eea3a058b3d3103f59345699388afb125ae47124bee395'),
        ('numba.cpython.setobj.SetInstance._add_entry', numba.cpython.
        setobj.SetInstance._add_entry,
        'c5ed28a5fdb453f242e41907cb792b66da2df63282c17abe0b68fc46782a7f94'),
        ('numba.cpython.setobj.SetInstance._add_key', numba.cpython.setobj.
        SetInstance._add_key,
        '324d6172638d02a361cfa0ca7f86e241e5a56a008d4ab581a305f9ae5ea4a75f'),
        ('numba.cpython.setobj.SetInstance._remove_entry', numba.cpython.
        setobj.SetInstance._remove_entry,
        '2c441b00daac61976e673c0e738e8e76982669bd2851951890dd40526fa14da1'),
        ('numba.cpython.setobj.SetInstance.pop', numba.cpython.setobj.
        SetInstance.pop,
        '1a7b7464cbe0577f2a38f3af9acfef6d4d25d049b1e216157275fbadaab41d1b'),
        ('numba.cpython.setobj.SetInstance._resize', numba.cpython.setobj.
        SetInstance._resize,
        '5ca5c2ba4f8c4bf546fde106b9c2656d4b22a16d16e163fb64c5d85ea4d88746'),
        ('numba.cpython.setobj.SetInstance._replace_payload', numba.cpython
        .setobj.SetInstance._replace_payload,
        'ada75a6c85828bff69c8469538c1979801f560a43fb726221a9c21bf208ae78d'),
        ('numba.cpython.setobj.SetInstance._allocate_payload', numba.
        cpython.setobj.SetInstance._allocate_payload,
        '2e80c419df43ebc71075b4f97fc1701c10dbc576aed248845e176b8d5829e61b'),
        ('numba.cpython.setobj.SetInstance._copy_payload', numba.cpython.
        setobj.SetInstance._copy_payload,
        '0885ac36e1eb5a0a0fc4f5d91e54b2102b69e536091fed9f2610a71d225193ec'),
        ('numba.cpython.setobj.set_constructor', numba.cpython.setobj.
        set_constructor,
        '3d521a60c3b8eaf70aa0f7267427475dfddd8f5e5053b5bfe309bb5f1891b0ce'),
        ('numba.cpython.setobj.set_update', numba.cpython.setobj.set_update,
        '965c4f7f7abcea5cbe0491b602e6d4bcb1800fa1ec39b1ffccf07e1bc56051c3')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
        orig = new
numba.core.boxing._native_set_to_python_list = _native_set_to_python_list
numba.cpython.setobj._SetPayload._lookup = _lookup
numba.cpython.setobj.SetInstance._add_entry = _add_entry
numba.cpython.setobj.SetInstance._add_key = _add_key
numba.cpython.setobj.SetInstance._remove_entry = _remove_entry
numba.cpython.setobj.SetInstance.pop = pop
numba.cpython.setobj.SetInstance._resize = _resize
numba.cpython.setobj.SetInstance._replace_payload = _replace_payload
numba.cpython.setobj.SetInstance._allocate_payload = _allocate_payload
numba.cpython.setobj.SetInstance._copy_payload = _copy_payload


def _reduce(self):
    libdata = self.library.serialize_using_object_code()
    typeann = str(self.type_annotation)
    fndesc = self.fndesc
    fndesc.typemap = fndesc.calltypes = None
    referenced_envs = self._find_referenced_environments()
    wzt__rmn = {key: value for key, value in self.metadata.items() if (
        'distributed' in key or 'replicated' in key) and key !=
        'distributed_diagnostics'}
    return (libdata, self.fndesc, self.environment, self.signature, self.
        objectmode, self.lifted, typeann, wzt__rmn, self.reload_init, tuple
        (referenced_envs))


@classmethod
def _rebuild(cls, target_context, libdata, fndesc, env, signature,
    objectmode, lifted, typeann, metadata, reload_init, referenced_envs):
    if reload_init:
        for fn in reload_init:
            fn()
    library = target_context.codegen().unserialize_library(libdata)
    zwlfx__hlyj = target_context.get_executable(library, fndesc, env)
    bzwu__fchos = cls(target_context=target_context, typing_context=
        target_context.typing_context, library=library, environment=env,
        entry_point=zwlfx__hlyj, fndesc=fndesc, type_annotation=typeann,
        signature=signature, objectmode=objectmode, lifted=lifted,
        typing_error=None, call_helper=None, metadata=metadata, reload_init
        =reload_init, referenced_envs=referenced_envs)
    for env in referenced_envs:
        library.codegen.set_env(env.env_name, env)
    return bzwu__fchos


if _check_numba_change:
    for name, orig, hash in (('numba.core.compiler.CompileResult._reduce',
        numba.core.compiler.CompileResult._reduce,
        '5f86eacfa5202c202b3dc200f1a7a9b6d3f9d1ec16d43a52cb2d580c34fbfa82'),
        ('numba.core.compiler.CompileResult._rebuild', numba.core.compiler.
        CompileResult._rebuild,
        '44fa9dc2255883ab49195d18c3cca8c0ad715d0dd02033bd7e2376152edc4e84')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
        orig = new
numba.core.compiler.CompileResult._reduce = _reduce
numba.core.compiler.CompileResult._rebuild = _rebuild
if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._IPythonCacheLocator.
        get_cache_path)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'eb33b7198697b8ef78edddcf69e58973c44744ff2cb2f54d4015611ad43baed0':
        warnings.warn(
            'numba.core.caching._IPythonCacheLocator.get_cache_path has changed'
            )
if os.environ.get('BODO_PLATFORM_CACHE_LOCATION') is not None:

    def _get_cache_path(self):
        return numba.config.CACHE_DIR
    numba.core.caching._IPythonCacheLocator.get_cache_path = _get_cache_path
if _check_numba_change:
    lines = inspect.getsource(numba.core.types.containers.Bytes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '977423d833eeb4b8fd0c87f55dce7251c107d8d10793fe5723de6e5452da32e2':
        warnings.warn('numba.core.types.containers.Bytes has changed')
numba.core.types.containers.Bytes.slice_is_copy = True
if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheLocator.
        ensure_cache_path)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '906b6f516f76927dfbe69602c335fa151b9f33d40dfe171a9190c0d11627bc03':
        warnings.warn(
            'numba.core.caching._CacheLocator.ensure_cache_path has changed')
if os.environ.get('BODO_PLATFORM_CACHE_LOCATION') is not None:
    import tempfile

    def _ensure_cache_path(self):
        from mpi4py import MPI
        kkwj__ctz = MPI.COMM_WORLD
        if kkwj__ctz.Get_rank() == 0:
            xbl__zzwn = self.get_cache_path()
            os.makedirs(xbl__zzwn, exist_ok=True)
            tempfile.TemporaryFile(dir=xbl__zzwn).close()
    numba.core.caching._CacheLocator.ensure_cache_path = _ensure_cache_path


def _analyze_op_call_builtins_len(self, scope, equiv_set, loc, args, kws):
    from numba.parfors.array_analysis import ArrayAnalysis
    require(len(args) == 1)
    var = args[0]
    typ = self.typemap[var.name]
    require(isinstance(typ, types.ArrayCompatible))
    require(not isinstance(typ, types.Bytes))
    shape = equiv_set._get_shape(var)
    return ArrayAnalysis.AnalyzeResult(shape=shape[0], rhs=shape[0])


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.array_analysis.ArrayAnalysis.
        _analyze_op_call_builtins_len)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '612cbc67e8e462f25f348b2a5dd55595f4201a6af826cffcd38b16cd85fc70f7':
        warnings.warn(
            'numba.parfors.array_analysis.ArrayAnalysis._analyze_op_call_builtins_len has changed'
            )
(numba.parfors.array_analysis.ArrayAnalysis._analyze_op_call_builtins_len
    ) = _analyze_op_call_builtins_len


def generic(self, args, kws):
    assert not kws
    val, = args
    if isinstance(val, (types.Buffer, types.BaseTuple)) and not isinstance(val,
        types.Bytes):
        return signature(types.intp, val)
    elif isinstance(val, types.RangeType):
        return signature(val.dtype, val)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.builtins.Len.generic)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '88d54238ebe0896f4s69b7347105a6a68dec443036a61f9e494c1630c62b0fa76':
        warnings.warn('numba.core.typing.builtins.Len.generic has changed')
numba.core.typing.builtins.Len.generic = generic
from numba.cpython import charseq


def _make_constant_bytes(context, builder, nbytes):
    from llvmlite import ir
    ayisi__vfdl = cgutils.create_struct_proxy(charseq.bytes_type)
    erfz__nai = ayisi__vfdl(context, builder)
    if isinstance(nbytes, int):
        nbytes = ir.Constant(erfz__nai.nitems.type, nbytes)
    erfz__nai.meminfo = context.nrt.meminfo_alloc(builder, nbytes)
    erfz__nai.nitems = nbytes
    erfz__nai.itemsize = ir.Constant(erfz__nai.itemsize.type, 1)
    erfz__nai.data = context.nrt.meminfo_data(builder, erfz__nai.meminfo)
    erfz__nai.parent = cgutils.get_null_value(erfz__nai.parent.type)
    erfz__nai.shape = cgutils.pack_array(builder, [erfz__nai.nitems],
        context.get_value_type(types.intp))
    erfz__nai.strides = cgutils.pack_array(builder, [ir.Constant(erfz__nai.
        strides.type.element, 1)], context.get_value_type(types.intp))
    return erfz__nai


if _check_numba_change:
    lines = inspect.getsource(charseq._make_constant_bytes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b3ed23ad58baff7b935912e3e22f4d8af67423d8fd0e5f1836ba0b3028a6eb18':
        warnings.warn('charseq._make_constant_bytes has changed')
charseq._make_constant_bytes = _make_constant_bytes
