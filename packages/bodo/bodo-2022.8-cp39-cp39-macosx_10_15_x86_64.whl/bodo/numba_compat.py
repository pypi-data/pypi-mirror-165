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
    scnog__lqis = numba.core.bytecode.FunctionIdentity.from_function(func)
    udy__gsg = numba.core.interpreter.Interpreter(scnog__lqis)
    ppywt__wjq = numba.core.bytecode.ByteCode(func_id=scnog__lqis)
    func_ir = udy__gsg.interpret(ppywt__wjq)
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
        xymld__bgn = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        xymld__bgn.run()
    ocn__uvv = numba.core.postproc.PostProcessor(func_ir)
    ocn__uvv.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, hnubv__udjjx in visit_vars_extensions.items():
        if isinstance(stmt, t):
            hnubv__udjjx(stmt, callback, cbdata)
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
    xvpdo__ngt = ['ravel', 'transpose', 'reshape']
    for czgmz__bam in blocks.values():
        for eyk__aquv in czgmz__bam.body:
            if type(eyk__aquv) in alias_analysis_extensions:
                hnubv__udjjx = alias_analysis_extensions[type(eyk__aquv)]
                hnubv__udjjx(eyk__aquv, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(eyk__aquv, ir.Assign):
                ogx__dzd = eyk__aquv.value
                accd__ldgr = eyk__aquv.target.name
                if is_immutable_type(accd__ldgr, typemap):
                    continue
                if isinstance(ogx__dzd, ir.Var
                    ) and accd__ldgr != ogx__dzd.name:
                    _add_alias(accd__ldgr, ogx__dzd.name, alias_map,
                        arg_aliases)
                if isinstance(ogx__dzd, ir.Expr) and (ogx__dzd.op == 'cast' or
                    ogx__dzd.op in ['getitem', 'static_getitem']):
                    _add_alias(accd__ldgr, ogx__dzd.value.name, alias_map,
                        arg_aliases)
                if isinstance(ogx__dzd, ir.Expr
                    ) and ogx__dzd.op == 'inplace_binop':
                    _add_alias(accd__ldgr, ogx__dzd.lhs.name, alias_map,
                        arg_aliases)
                if isinstance(ogx__dzd, ir.Expr
                    ) and ogx__dzd.op == 'getattr' and ogx__dzd.attr in ['T',
                    'ctypes', 'flat']:
                    _add_alias(accd__ldgr, ogx__dzd.value.name, alias_map,
                        arg_aliases)
                if isinstance(ogx__dzd, ir.Expr
                    ) and ogx__dzd.op == 'getattr' and ogx__dzd.attr not in [
                    'shape'] and ogx__dzd.value.name in arg_aliases:
                    _add_alias(accd__ldgr, ogx__dzd.value.name, alias_map,
                        arg_aliases)
                if isinstance(ogx__dzd, ir.Expr
                    ) and ogx__dzd.op == 'getattr' and ogx__dzd.attr in ('loc',
                    'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(accd__ldgr, ogx__dzd.value.name, alias_map,
                        arg_aliases)
                if isinstance(ogx__dzd, ir.Expr) and ogx__dzd.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(accd__ldgr, typemap):
                    for lzf__tbt in ogx__dzd.items:
                        _add_alias(accd__ldgr, lzf__tbt.name, alias_map,
                            arg_aliases)
                if isinstance(ogx__dzd, ir.Expr) and ogx__dzd.op == 'call':
                    tdsxj__qna = guard(find_callname, func_ir, ogx__dzd,
                        typemap)
                    if tdsxj__qna is None:
                        continue
                    jst__sjr, fdxmp__eoaj = tdsxj__qna
                    if tdsxj__qna in alias_func_extensions:
                        fxn__kxq = alias_func_extensions[tdsxj__qna]
                        fxn__kxq(accd__ldgr, ogx__dzd.args, alias_map,
                            arg_aliases)
                    if fdxmp__eoaj == 'numpy' and jst__sjr in xvpdo__ngt:
                        _add_alias(accd__ldgr, ogx__dzd.args[0].name,
                            alias_map, arg_aliases)
                    if isinstance(fdxmp__eoaj, ir.Var
                        ) and jst__sjr in xvpdo__ngt:
                        _add_alias(accd__ldgr, fdxmp__eoaj.name, alias_map,
                            arg_aliases)
    opx__dhgle = copy.deepcopy(alias_map)
    for lzf__tbt in opx__dhgle:
        for nine__qycie in opx__dhgle[lzf__tbt]:
            alias_map[lzf__tbt] |= alias_map[nine__qycie]
        for nine__qycie in opx__dhgle[lzf__tbt]:
            alias_map[nine__qycie] = alias_map[lzf__tbt]
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
    oppk__wvzkw = compute_cfg_from_blocks(func_ir.blocks)
    dozu__yvv = compute_use_defs(func_ir.blocks)
    yutd__qahbe = compute_live_map(oppk__wvzkw, func_ir.blocks, dozu__yvv.
        usemap, dozu__yvv.defmap)
    rjpmr__zdu = True
    while rjpmr__zdu:
        rjpmr__zdu = False
        for label, block in func_ir.blocks.items():
            lives = {lzf__tbt.name for lzf__tbt in block.terminator.list_vars()
                }
            for vsny__tqcaq, cfgjg__ily in oppk__wvzkw.successors(label):
                lives |= yutd__qahbe[vsny__tqcaq]
            tzl__zeg = [block.terminator]
            for stmt in reversed(block.body[:-1]):
                if isinstance(stmt, ir.Assign):
                    accd__ldgr = stmt.target
                    rvjkf__tpy = stmt.value
                    if accd__ldgr.name not in lives:
                        if isinstance(rvjkf__tpy, ir.Expr
                            ) and rvjkf__tpy.op == 'make_function':
                            continue
                        if isinstance(rvjkf__tpy, ir.Expr
                            ) and rvjkf__tpy.op == 'getattr':
                            continue
                        if isinstance(rvjkf__tpy, ir.Const):
                            continue
                        if typemap and isinstance(typemap.get(accd__ldgr,
                            None), types.Function):
                            continue
                        if isinstance(rvjkf__tpy, ir.Expr
                            ) and rvjkf__tpy.op == 'build_map':
                            continue
                        if isinstance(rvjkf__tpy, ir.Expr
                            ) and rvjkf__tpy.op == 'build_tuple':
                            continue
                    if isinstance(rvjkf__tpy, ir.Var
                        ) and accd__ldgr.name == rvjkf__tpy.name:
                        continue
                if isinstance(stmt, ir.Del):
                    if stmt.value not in lives:
                        continue
                if type(stmt) in analysis.ir_extension_usedefs:
                    bjfb__ounwa = analysis.ir_extension_usedefs[type(stmt)]
                    nef__tyyil, mwi__awmf = bjfb__ounwa(stmt)
                    lives -= mwi__awmf
                    lives |= nef__tyyil
                else:
                    lives |= {lzf__tbt.name for lzf__tbt in stmt.list_vars()}
                    if isinstance(stmt, ir.Assign):
                        lives.remove(accd__ldgr.name)
                tzl__zeg.append(stmt)
            tzl__zeg.reverse()
            if len(block.body) != len(tzl__zeg):
                rjpmr__zdu = True
            block.body = tzl__zeg


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    avqxk__ebc = getattr(func, '__name__', str(func))
    name = 'OverloadTemplate_%s' % (avqxk__ebc,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    enooh__shmgx = dict(key=func, _overload_func=staticmethod(overload_func
        ), _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(name, (base,), enooh__shmgx)


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
            for jops__she in fnty.templates:
                self._inline_overloads.update(jops__she._inline_overloads)
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
    enooh__shmgx = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(name, (base,), enooh__shmgx)
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
    edeo__ibmbs, wph__kuhpz = self._get_impl(args, kws)
    if edeo__ibmbs is None:
        return
    ggr__jupa = types.Dispatcher(edeo__ibmbs)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        vtuxp__ddrle = edeo__ibmbs._compiler
        flags = compiler.Flags()
        qnd__sgu = vtuxp__ddrle.targetdescr.typing_context
        hneg__drof = vtuxp__ddrle.targetdescr.target_context
        nhkvj__hdxxf = vtuxp__ddrle.pipeline_class(qnd__sgu, hneg__drof,
            None, None, None, flags, None)
        wonh__fubsg = InlineWorker(qnd__sgu, hneg__drof, vtuxp__ddrle.
            locals, nhkvj__hdxxf, flags, None)
        gov__oat = ggr__jupa.dispatcher.get_call_template
        jops__she, mvaep__mjgi, kve__fvkom, kws = gov__oat(wph__kuhpz, kws)
        if kve__fvkom in self._inline_overloads:
            return self._inline_overloads[kve__fvkom]['iinfo'].signature
        ir = wonh__fubsg.run_untyped_passes(ggr__jupa.dispatcher.py_func,
            enable_ssa=True)
        typemap, return_type, calltypes, _ = typed_passes.type_inference_stage(
            self.context, hneg__drof, ir, kve__fvkom, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(return_type, kve__fvkom, None)
        self._inline_overloads[sig.args] = {'folded_args': kve__fvkom}
        ylmh__kldq = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = ylmh__kldq
        if not self._inline.is_always_inline:
            sig = ggr__jupa.get_call_type(self.context, wph__kuhpz, kws)
            self._compiled_overloads[sig.args] = ggr__jupa.get_overload(sig)
        zfmy__ibo = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': kve__fvkom,
            'iinfo': zfmy__ibo}
    else:
        sig = ggr__jupa.get_call_type(self.context, wph__kuhpz, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = ggr__jupa.get_overload(sig)
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
    glkq__bfyj = [True, False]
    qpas__eox = [False, True]
    wtds__ansig = _ResolutionFailures(context, self, args, kws, depth=self.
        _depth)
    from numba.core.target_extension import get_local_target
    uhdl__ubmxn = get_local_target(context)
    bujmv__vnuf = utils.order_by_target_specificity(uhdl__ubmxn, self.
        templates, fnkey=self.key[0])
    self._depth += 1
    for cydgc__ocwa in bujmv__vnuf:
        diigk__ywf = cydgc__ocwa(context)
        ykdea__xnug = glkq__bfyj if diigk__ywf.prefer_literal else qpas__eox
        ykdea__xnug = [True] if getattr(diigk__ywf, '_no_unliteral', False
            ) else ykdea__xnug
        for phe__uid in ykdea__xnug:
            try:
                if phe__uid:
                    sig = diigk__ywf.apply(args, kws)
                else:
                    ofdli__zbv = tuple([_unlit_non_poison(a) for a in args])
                    pud__oiuj = {hocul__rbp: _unlit_non_poison(lzf__tbt) for
                        hocul__rbp, lzf__tbt in kws.items()}
                    sig = diigk__ywf.apply(ofdli__zbv, pud__oiuj)
            except Exception as e:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                else:
                    sig = None
                    wtds__ansig.add_error(diigk__ywf, False, e, phe__uid)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = diigk__ywf.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    ewbtm__ktxwq = getattr(diigk__ywf, 'cases', None)
                    if ewbtm__ktxwq is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            ewbtm__ktxwq)
                    else:
                        msg = 'No match.'
                    wtds__ansig.add_error(diigk__ywf, True, msg, phe__uid)
    wtds__ansig.raise_error()


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
    jops__she = self.template(context)
    hdv__uge = None
    dhh__tlm = None
    uzom__wym = None
    ykdea__xnug = [True, False] if jops__she.prefer_literal else [False, True]
    ykdea__xnug = [True] if getattr(jops__she, '_no_unliteral', False
        ) else ykdea__xnug
    for phe__uid in ykdea__xnug:
        if phe__uid:
            try:
                uzom__wym = jops__she.apply(args, kws)
            except Exception as ufyy__cnln:
                if isinstance(ufyy__cnln, errors.ForceLiteralArg):
                    raise ufyy__cnln
                hdv__uge = ufyy__cnln
                uzom__wym = None
            else:
                break
        else:
            gvzwi__afon = tuple([_unlit_non_poison(a) for a in args])
            jwhvn__qyj = {hocul__rbp: _unlit_non_poison(lzf__tbt) for 
                hocul__rbp, lzf__tbt in kws.items()}
            gajqt__birug = gvzwi__afon == args and kws == jwhvn__qyj
            if not gajqt__birug and uzom__wym is None:
                try:
                    uzom__wym = jops__she.apply(gvzwi__afon, jwhvn__qyj)
                except Exception as ufyy__cnln:
                    from numba.core import utils
                    if utils.use_new_style_errors() and not isinstance(
                        ufyy__cnln, errors.NumbaError):
                        raise ufyy__cnln
                    if isinstance(ufyy__cnln, errors.ForceLiteralArg):
                        if jops__she.prefer_literal:
                            raise ufyy__cnln
                    dhh__tlm = ufyy__cnln
                else:
                    break
    if uzom__wym is None and (dhh__tlm is not None or hdv__uge is not None):
        oevb__lec = '- Resolution failure for {} arguments:\n{}\n'
        mzu__yeyw = _termcolor.highlight(oevb__lec)
        if numba.core.config.DEVELOPER_MODE:
            vpp__ohq = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    bwzkf__optj = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    bwzkf__optj = ['']
                fttyh__japi = '\n{}'.format(2 * vpp__ohq)
                tgh__slepo = _termcolor.reset(fttyh__japi + fttyh__japi.
                    join(_bt_as_lines(bwzkf__optj)))
                return _termcolor.reset(tgh__slepo)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            nwm__nwnco = str(e)
            nwm__nwnco = nwm__nwnco if nwm__nwnco else str(repr(e)) + add_bt(e)
            yrjn__goryr = errors.TypingError(textwrap.dedent(nwm__nwnco))
            return mzu__yeyw.format(literalness, str(yrjn__goryr))
        import bodo
        if isinstance(hdv__uge, bodo.utils.typing.BodoError):
            raise hdv__uge
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', hdv__uge) +
                nested_msg('non-literal', dhh__tlm))
        else:
            if 'missing a required argument' in hdv__uge.msg:
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
            raise errors.TypingError(msg, loc=hdv__uge.loc)
    return uzom__wym


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
    jst__sjr = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=jst__sjr)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            dsn__cpx = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), dsn__cpx)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    sln__iuqz = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            sln__iuqz.append(types.Omitted(a.value))
        else:
            sln__iuqz.append(self.typeof_pyval(a))
    dyb__ssko = None
    try:
        error = None
        dyb__ssko = self.compile(tuple(sln__iuqz))
    except errors.ForceLiteralArg as e:
        puxq__zdvw = [i for i in e.requested_args if isinstance(args[i],
            types.Literal) and not isinstance(args[i], types.LiteralStrKeyDict)
            ]
        if puxq__zdvw:
            lmy__qfty = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            sau__ysjvm = ', '.join('Arg #{} is {}'.format(i, args[i]) for i in
                sorted(puxq__zdvw))
            raise errors.CompilerError(lmy__qfty.format(sau__ysjvm))
        wph__kuhpz = []
        try:
            for i, lzf__tbt in enumerate(args):
                if i in e.requested_args:
                    if i in e.file_infos:
                        wph__kuhpz.append(types.FilenameType(args[i], e.
                            file_infos[i]))
                    else:
                        wph__kuhpz.append(types.literal(args[i]))
                else:
                    wph__kuhpz.append(args[i])
            args = wph__kuhpz
        except (OSError, FileNotFoundError) as gclw__zymk:
            error = FileNotFoundError(str(gclw__zymk) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                dyb__ssko = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        buapy__lptgq = []
        for i, jzml__kavd in enumerate(args):
            val = jzml__kavd.value if isinstance(jzml__kavd, numba.core.
                dispatcher.OmittedArg) else jzml__kavd
            try:
                rwze__nixi = typeof(val, Purpose.argument)
            except ValueError as axv__rwzy:
                buapy__lptgq.append((i, str(axv__rwzy)))
            else:
                if rwze__nixi is None:
                    buapy__lptgq.append((i,
                        f'cannot determine Numba type of value {val}'))
        if buapy__lptgq:
            jsidx__vbyt = '\n'.join(f'- argument {i}: {ghwkq__wnn}' for i,
                ghwkq__wnn in buapy__lptgq)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{jsidx__vbyt}
"""
            e.patch_message(msg)
        if "Cannot determine Numba type of <class 'numpy.ufunc'>" in e.msg:
            msg = 'Unsupported Numpy ufunc encountered in JIT code'
            error = bodo.utils.typing.BodoError(msg, loc=e.loc)
        elif not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                oxvep__agnx = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'Failed at nopython',
                    'Overload', 'lowering']
                lwut__fvc = False
                for bcrtl__etz in oxvep__agnx:
                    if bcrtl__etz in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        lwut__fvc = True
                        break
                if not lwut__fvc:
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
                dsn__cpx = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), dsn__cpx)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return dyb__ssko


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
    for fmxui__fhfj in cres.library._codegen._engine._defined_symbols:
        if fmxui__fhfj.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in fmxui__fhfj and (
            'bodo_gb_udf_update_local' in fmxui__fhfj or 
            'bodo_gb_udf_combine' in fmxui__fhfj or 'bodo_gb_udf_eval' in
            fmxui__fhfj or 'bodo_gb_apply_general_udfs' in fmxui__fhfj):
            gb_agg_cfunc_addr[fmxui__fhfj
                ] = cres.library.get_pointer_to_function(fmxui__fhfj)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for fmxui__fhfj in cres.library._codegen._engine._defined_symbols:
        if fmxui__fhfj.startswith('cfunc') and ('get_join_cond_addr' not in
            fmxui__fhfj or 'bodo_join_gen_cond' in fmxui__fhfj):
            join_gen_cond_cfunc_addr[fmxui__fhfj
                ] = cres.library.get_pointer_to_function(fmxui__fhfj)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    import bodo
    edeo__ibmbs = self._get_dispatcher_for_current_target()
    if edeo__ibmbs is not self:
        return edeo__ibmbs.compile(sig)
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
            kqp__sgtih = self.overloads.get(tuple(args))
            if kqp__sgtih is not None:
                return kqp__sgtih.entry_point
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
            nlurm__asz = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=nlurm__asz):
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
                ejr__xdu = bodo.get_nodes_first_ranks()
                if bodo.get_rank() in ejr__xdu:
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
    yfahf__mkhq = self._final_module
    gybv__chtdi = []
    mxmch__kigw = 0
    for fn in yfahf__mkhq.functions:
        mxmch__kigw += 1
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
            gybv__chtdi.append(fn.name)
    if mxmch__kigw == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if gybv__chtdi:
        yfahf__mkhq = yfahf__mkhq.clone()
        for name in gybv__chtdi:
            yfahf__mkhq.get_function(name).linkage = 'linkonce_odr'
    self._shared_module = yfahf__mkhq
    return yfahf__mkhq


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
    for tgc__ylr in self.constraints:
        loc = tgc__ylr.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                tgc__ylr(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                ofzm__modh = numba.core.errors.TypingError(str(e), loc=
                    tgc__ylr.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(ofzm__modh, e))
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
                    ofzm__modh = numba.core.errors.TypingError(msg.format(
                        con=tgc__ylr, err=str(e)), loc=tgc__ylr.loc,
                        highlighting=False)
                    errors.append(utils.chain_exception(ofzm__modh, e))
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
    for bmp__glb in self._failures.values():
        for fmmpe__kkjvd in bmp__glb:
            if isinstance(fmmpe__kkjvd.error, ForceLiteralArg):
                raise fmmpe__kkjvd.error
            if isinstance(fmmpe__kkjvd.error, bodo.utils.typing.BodoError):
                raise fmmpe__kkjvd.error
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
    eodij__maz = False
    tzl__zeg = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        fvr__aowm = set()
        dzs__jotoa = lives & alias_set
        for lzf__tbt in dzs__jotoa:
            fvr__aowm |= alias_map[lzf__tbt]
        lives_n_aliases = lives | fvr__aowm | arg_aliases
        if type(stmt) in remove_dead_extensions:
            hnubv__udjjx = remove_dead_extensions[type(stmt)]
            stmt = hnubv__udjjx(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                eodij__maz = True
                continue
        if isinstance(stmt, ir.Assign):
            accd__ldgr = stmt.target
            rvjkf__tpy = stmt.value
            if accd__ldgr.name not in lives:
                if has_no_side_effect(rvjkf__tpy, lives_n_aliases, call_table):
                    eodij__maz = True
                    continue
                if isinstance(rvjkf__tpy, ir.Expr
                    ) and rvjkf__tpy.op == 'call' and call_table[rvjkf__tpy
                    .func.name] == ['astype']:
                    ryuh__pnw = guard(get_definition, func_ir, rvjkf__tpy.func)
                    if (ryuh__pnw is not None and ryuh__pnw.op == 'getattr' and
                        isinstance(typemap[ryuh__pnw.value.name], types.
                        Array) and ryuh__pnw.attr == 'astype'):
                        eodij__maz = True
                        continue
            if saved_array_analysis and accd__ldgr.name in lives and is_expr(
                rvjkf__tpy, 'getattr'
                ) and rvjkf__tpy.attr == 'shape' and is_array_typ(typemap[
                rvjkf__tpy.value.name]) and rvjkf__tpy.value.name not in lives:
                jncd__gqevx = {lzf__tbt: hocul__rbp for hocul__rbp,
                    lzf__tbt in func_ir.blocks.items()}
                if block in jncd__gqevx:
                    label = jncd__gqevx[block]
                    yhx__fuken = saved_array_analysis.get_equiv_set(label)
                    qixl__heo = yhx__fuken.get_equiv_set(rvjkf__tpy.value)
                    if qixl__heo is not None:
                        for lzf__tbt in qixl__heo:
                            if lzf__tbt.endswith('#0'):
                                lzf__tbt = lzf__tbt[:-2]
                            if lzf__tbt in typemap and is_array_typ(typemap
                                [lzf__tbt]) and lzf__tbt in lives:
                                rvjkf__tpy.value = ir.Var(rvjkf__tpy.value.
                                    scope, lzf__tbt, rvjkf__tpy.value.loc)
                                eodij__maz = True
                                break
            if isinstance(rvjkf__tpy, ir.Var
                ) and accd__ldgr.name == rvjkf__tpy.name:
                eodij__maz = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                eodij__maz = True
                continue
        if isinstance(stmt, ir.SetItem):
            name = stmt.target.name
            if name not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            bjfb__ounwa = analysis.ir_extension_usedefs[type(stmt)]
            nef__tyyil, mwi__awmf = bjfb__ounwa(stmt)
            lives -= mwi__awmf
            lives |= nef__tyyil
        else:
            lives |= {lzf__tbt.name for lzf__tbt in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                xytq__ghldu = set()
                if isinstance(rvjkf__tpy, ir.Expr):
                    xytq__ghldu = {lzf__tbt.name for lzf__tbt in rvjkf__tpy
                        .list_vars()}
                if accd__ldgr.name not in xytq__ghldu:
                    lives.remove(accd__ldgr.name)
        tzl__zeg.append(stmt)
    tzl__zeg.reverse()
    block.body = tzl__zeg
    return eodij__maz


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            lzefr__pgf, = args
            if isinstance(lzefr__pgf, types.IterableType):
                dtype = lzefr__pgf.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), lzefr__pgf)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    zggtg__ngizf = 'reflected set' if reflected else 'set'
    name = '%s(%s)' % (zggtg__ngizf, self.dtype)
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
        except LiteralTypingError as hil__jjy:
            return
    try:
        return literal(value)
    except LiteralTypingError as hil__jjy:
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
        yrgnw__uech = py_func.__qualname__
    except AttributeError as hil__jjy:
        yrgnw__uech = py_func.__name__
    obw__xdhp = inspect.getfile(py_func)
    for cls in self._locator_classes:
        ysbr__okr = cls.from_function(py_func, obw__xdhp)
        if ysbr__okr is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (yrgnw__uech, obw__xdhp))
    self._locator = ysbr__okr
    nugkt__owlj = inspect.getfile(py_func)
    qpftp__gmfh = os.path.splitext(os.path.basename(nugkt__owlj))[0]
    if obw__xdhp.startswith('<ipython-'):
        begpe__ulgpd = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)',
            '\\1\\3', qpftp__gmfh, count=1)
        if begpe__ulgpd == qpftp__gmfh:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        qpftp__gmfh = begpe__ulgpd
    hsfgj__iwis = '%s.%s' % (qpftp__gmfh, yrgnw__uech)
    uhyfq__jldto = getattr(sys, 'abiflags', '')
    from bodo import __version__ as bodo_version
    self._filename_base = self.get_filename_base(hsfgj__iwis, uhyfq__jldto
        ) + 'bodo' + bodo_version


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    fsr__vrww = list(filter(lambda a: self._istuple(a.name), args))
    if len(fsr__vrww) == 2 and fn.__name__ == 'add':
        gbv__erugh = self.typemap[fsr__vrww[0].name]
        obih__vazah = self.typemap[fsr__vrww[1].name]
        if gbv__erugh.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                fsr__vrww[1]))
        if obih__vazah.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                fsr__vrww[0]))
        try:
            mecu__bub = [equiv_set.get_shape(x) for x in fsr__vrww]
            if None in mecu__bub:
                return None
            spqnn__qxe = sum(mecu__bub, ())
            return ArrayAnalysis.AnalyzeResult(shape=spqnn__qxe)
        except GuardException as hil__jjy:
            return None
    zmkg__hehm = list(filter(lambda a: self._isarray(a.name), args))
    require(len(zmkg__hehm) > 0)
    zlv__opq = [x.name for x in zmkg__hehm]
    srzkr__aanqk = [self.typemap[x.name].ndim for x in zmkg__hehm]
    wvqfl__ctv = max(srzkr__aanqk)
    require(wvqfl__ctv > 0)
    mecu__bub = [equiv_set.get_shape(x) for x in zmkg__hehm]
    if any(a is None for a in mecu__bub):
        return ArrayAnalysis.AnalyzeResult(shape=zmkg__hehm[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, zmkg__hehm))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, mecu__bub,
        zlv__opq)


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
    dlcs__ina = code_obj.code
    oujeu__ljofb = len(dlcs__ina.co_freevars)
    acz__pyb = dlcs__ina.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        pgd__iyzxa, op = ir_utils.find_build_sequence(caller_ir, code_obj.
            closure)
        assert op == 'build_tuple'
        acz__pyb = [lzf__tbt.name for lzf__tbt in pgd__iyzxa]
    aabmg__udey = caller_ir.func_id.func.__globals__
    try:
        aabmg__udey = getattr(code_obj, 'globals', aabmg__udey)
    except KeyError as hil__jjy:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/api_docs/udfs/."
        )
    iqd__gtbs = []
    for x in acz__pyb:
        try:
            hquru__vcwqt = caller_ir.get_definition(x)
        except KeyError as hil__jjy:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(hquru__vcwqt, (ir.Const, ir.Global, ir.FreeVar)):
            val = hquru__vcwqt.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                avqxk__ebc = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                aabmg__udey[avqxk__ebc] = bodo.jit(distributed=False)(val)
                aabmg__udey[avqxk__ebc].is_nested_func = True
                val = avqxk__ebc
            if isinstance(val, CPUDispatcher):
                avqxk__ebc = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                aabmg__udey[avqxk__ebc] = val
                val = avqxk__ebc
            iqd__gtbs.append(val)
        elif isinstance(hquru__vcwqt, ir.Expr
            ) and hquru__vcwqt.op == 'make_function':
            iedxw__ofu = convert_code_obj_to_function(hquru__vcwqt, caller_ir)
            avqxk__ebc = ir_utils.mk_unique_var('nested_func').replace('.', '_'
                )
            aabmg__udey[avqxk__ebc] = bodo.jit(distributed=False)(iedxw__ofu)
            aabmg__udey[avqxk__ebc].is_nested_func = True
            iqd__gtbs.append(avqxk__ebc)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    rvgpj__slo = '\n'.join([('\tc_%d = %s' % (i, x)) for i, x in enumerate(
        iqd__gtbs)])
    sdn__zvt = ','.join([('c_%d' % i) for i in range(oujeu__ljofb)])
    ikp__udh = list(dlcs__ina.co_varnames)
    qbt__evi = 0
    ibh__zlbvx = dlcs__ina.co_argcount
    eybl__pefaj = caller_ir.get_definition(code_obj.defaults)
    if eybl__pefaj is not None:
        if isinstance(eybl__pefaj, tuple):
            d = [caller_ir.get_definition(x).value for x in eybl__pefaj]
            cqw__uux = tuple(d)
        else:
            d = [caller_ir.get_definition(x).value for x in eybl__pefaj.items]
            cqw__uux = tuple(d)
        qbt__evi = len(cqw__uux)
    khhbk__lmnw = ibh__zlbvx - qbt__evi
    glhji__fae = ','.join([('%s' % ikp__udh[i]) for i in range(khhbk__lmnw)])
    if qbt__evi:
        pnoij__biu = [('%s = %s' % (ikp__udh[i + khhbk__lmnw], cqw__uux[i])
            ) for i in range(qbt__evi)]
        glhji__fae += ', '
        glhji__fae += ', '.join(pnoij__biu)
    return _create_function_from_code_obj(dlcs__ina, rvgpj__slo, glhji__fae,
        sdn__zvt, aabmg__udey)


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
    for ihlla__lwlly, (kujh__hjvyq, irn__vnh) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % irn__vnh)
            iioy__mdabw = _pass_registry.get(kujh__hjvyq).pass_inst
            if isinstance(iioy__mdabw, CompilerPass):
                self._runPass(ihlla__lwlly, iioy__mdabw, state)
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
                    pipeline_name, irn__vnh)
                mkn__eok = self._patch_error(msg, e)
                raise mkn__eok
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
    ymf__rhcj = None
    mwi__awmf = {}

    def lookup(var, already_seen, varonly=True):
        val = mwi__awmf.get(var.name, None)
        if isinstance(val, ir.Var):
            if val.name in already_seen:
                return var
            already_seen.add(val.name)
            return lookup(val, already_seen, varonly)
        else:
            return var if varonly or val is None else val
    name = reduction_node.name
    bhhq__gex = reduction_node.unversioned_name
    for i, stmt in enumerate(nodes):
        accd__ldgr = stmt.target
        rvjkf__tpy = stmt.value
        mwi__awmf[accd__ldgr.name] = rvjkf__tpy
        if isinstance(rvjkf__tpy, ir.Var) and rvjkf__tpy.name in mwi__awmf:
            rvjkf__tpy = lookup(rvjkf__tpy, set())
        if isinstance(rvjkf__tpy, ir.Expr):
            bno__mlmy = set(lookup(lzf__tbt, set(), True).name for lzf__tbt in
                rvjkf__tpy.list_vars())
            if name in bno__mlmy:
                args = [(x.name, lookup(x, set(), True)) for x in
                    get_expr_args(rvjkf__tpy)]
                sdg__nkqe = [x for x, qce__npb in args if qce__npb.name != name
                    ]
                args = [(x, qce__npb) for x, qce__npb in args if x !=
                    qce__npb.name]
                wul__kwzbk = dict(args)
                if len(sdg__nkqe) == 1:
                    wul__kwzbk[sdg__nkqe[0]] = ir.Var(accd__ldgr.scope, 
                        name + '#init', accd__ldgr.loc)
                replace_vars_inner(rvjkf__tpy, wul__kwzbk)
                ymf__rhcj = nodes[i:]
                break
    return ymf__rhcj


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
        hiheh__nap = expand_aliases({lzf__tbt.name for lzf__tbt in stmt.
            list_vars()}, alias_map, arg_aliases)
        wfooe__xxhy = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        dtd__efp = expand_aliases({lzf__tbt.name for lzf__tbt in next_stmt.
            list_vars()}, alias_map, arg_aliases)
        ncedt__owaa = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(wfooe__xxhy & dtd__efp | ncedt__owaa & hiheh__nap) == 0:
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
    ieb__eeuuv = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            ieb__eeuuv.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                ieb__eeuuv.update(get_parfor_writes(stmt, func_ir))
    return ieb__eeuuv


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    ieb__eeuuv = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        ieb__eeuuv.add(stmt.target.name)
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        ieb__eeuuv = {lzf__tbt.name for lzf__tbt in stmt.out_vars}
    if isinstance(stmt, (bodo.ir.join.Join, bodo.ir.aggregate.Aggregate)):
        ieb__eeuuv = {lzf__tbt.name for lzf__tbt in stmt.get_live_out_vars()}
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            ieb__eeuuv.update({lzf__tbt.name for lzf__tbt in stmt.
                get_live_out_vars()})
    if is_call_assign(stmt):
        tdsxj__qna = guard(find_callname, func_ir, stmt.value)
        if tdsxj__qna in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'),
            ('setna', 'bodo.libs.array_kernels'), (
            'str_arr_item_to_numeric', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_int_to_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_NA_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_set_not_na', 'bodo.libs.str_arr_ext'), (
            'get_str_arr_item_copy', 'bodo.libs.str_arr_ext'), (
            'set_bit_to_arr', 'bodo.libs.int_arr_ext')):
            ieb__eeuuv.add(stmt.value.args[0].name)
        if tdsxj__qna == ('generate_table_nbytes', 'bodo.utils.table_utils'):
            ieb__eeuuv.add(stmt.value.args[1].name)
    return ieb__eeuuv


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
        hnubv__udjjx = _termcolor.errmsg('{0}') + _termcolor.filename(
            'During: {1}')
        qxqrd__mvsc = hnubv__udjjx.format(self, msg)
        self.args = qxqrd__mvsc,
    else:
        hnubv__udjjx = _termcolor.errmsg('{0}')
        qxqrd__mvsc = hnubv__udjjx.format(self)
        self.args = qxqrd__mvsc,
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
        for mrkyv__ykt in options['distributed']:
            dist_spec[mrkyv__ykt] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for mrkyv__ykt in options['distributed_block']:
            dist_spec[mrkyv__ykt] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    mslj__uxu = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, ukd__jfu in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(ukd__jfu)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    jtp__ylwue = {}
    for cila__qsv in reversed(inspect.getmro(cls)):
        jtp__ylwue.update(cila__qsv.__dict__)
    jcu__vwz, mmqs__jfwj, fxf__yyr, mzuog__bfek = {}, {}, {}, {}
    for hocul__rbp, lzf__tbt in jtp__ylwue.items():
        if isinstance(lzf__tbt, pytypes.FunctionType):
            jcu__vwz[hocul__rbp] = lzf__tbt
        elif isinstance(lzf__tbt, property):
            mmqs__jfwj[hocul__rbp] = lzf__tbt
        elif isinstance(lzf__tbt, staticmethod):
            fxf__yyr[hocul__rbp] = lzf__tbt
        else:
            mzuog__bfek[hocul__rbp] = lzf__tbt
    cra__iccak = (set(jcu__vwz) | set(mmqs__jfwj) | set(fxf__yyr)) & set(spec)
    if cra__iccak:
        raise NameError('name shadowing: {0}'.format(', '.join(cra__iccak)))
    unuc__siu = mzuog__bfek.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(mzuog__bfek)
    if mzuog__bfek:
        msg = 'class members are not yet supported: {0}'
        dpksl__hifk = ', '.join(mzuog__bfek.keys())
        raise TypeError(msg.format(dpksl__hifk))
    for hocul__rbp, lzf__tbt in mmqs__jfwj.items():
        if lzf__tbt.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(hocul__rbp))
    jit_methods = {hocul__rbp: bodo.jit(returns_maybe_distributed=mslj__uxu
        )(lzf__tbt) for hocul__rbp, lzf__tbt in jcu__vwz.items()}
    jit_props = {}
    for hocul__rbp, lzf__tbt in mmqs__jfwj.items():
        enooh__shmgx = {}
        if lzf__tbt.fget:
            enooh__shmgx['get'] = bodo.jit(lzf__tbt.fget)
        if lzf__tbt.fset:
            enooh__shmgx['set'] = bodo.jit(lzf__tbt.fset)
        jit_props[hocul__rbp] = enooh__shmgx
    jit_static_methods = {hocul__rbp: bodo.jit(lzf__tbt.__func__) for 
        hocul__rbp, lzf__tbt in fxf__yyr.items()}
    buakr__dpdnq = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    wok__nrm = dict(class_type=buakr__dpdnq, __doc__=unuc__siu)
    wok__nrm.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), wok__nrm)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, buakr__dpdnq)
    targetctx = numba.core.registry.cpu_target.target_context
    builder(buakr__dpdnq, typingctx, targetctx).register()
    as_numba_type.register(cls, buakr__dpdnq.instance_type)
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
    oltlt__satjs = ','.join('{0}:{1}'.format(hocul__rbp, lzf__tbt) for 
        hocul__rbp, lzf__tbt in struct.items())
    glm__xggyt = ','.join('{0}:{1}'.format(hocul__rbp, lzf__tbt) for 
        hocul__rbp, lzf__tbt in dist_spec.items())
    name = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), oltlt__satjs, glm__xggyt)
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
    qawux__tln = numba.core.typeinfer.fold_arg_vars(typevars, self.args,
        self.vararg, self.kws)
    if qawux__tln is None:
        return
    ffpzt__egs, srgso__xbzd = qawux__tln
    for a in itertools.chain(ffpzt__egs, srgso__xbzd.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, ffpzt__egs, srgso__xbzd)
    except ForceLiteralArg as e:
        kmxhc__ikbhu = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(kmxhc__ikbhu, self.kws)
        oeofk__uvqx = set()
        wyh__dhkm = set()
        ewu__zxmq = {}
        for ihlla__lwlly in e.requested_args:
            bkmai__tvxh = typeinfer.func_ir.get_definition(folded[ihlla__lwlly]
                )
            if isinstance(bkmai__tvxh, ir.Arg):
                oeofk__uvqx.add(bkmai__tvxh.index)
                if bkmai__tvxh.index in e.file_infos:
                    ewu__zxmq[bkmai__tvxh.index] = e.file_infos[bkmai__tvxh
                        .index]
            else:
                wyh__dhkm.add(ihlla__lwlly)
        if wyh__dhkm:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif oeofk__uvqx:
            raise ForceLiteralArg(oeofk__uvqx, loc=self.loc, file_infos=
                ewu__zxmq)
    if sig is None:
        pqnce__kuny = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in ffpzt__egs]
        args += [('%s=%s' % (hocul__rbp, lzf__tbt)) for hocul__rbp,
            lzf__tbt in sorted(srgso__xbzd.items())]
        vqwgs__lqnf = pqnce__kuny.format(fnty, ', '.join(map(str, args)))
        yrxci__bgsui = context.explain_function_type(fnty)
        msg = '\n'.join([vqwgs__lqnf, yrxci__bgsui])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        dlfn__ogzv = context.unify_pairs(sig.recvr, fnty.this)
        if dlfn__ogzv is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if dlfn__ogzv is not None and dlfn__ogzv.is_precise():
            qpz__mamux = fnty.copy(this=dlfn__ogzv)
            typeinfer.propagate_refined_type(self.func, qpz__mamux)
    if not sig.return_type.is_precise():
        target = typevars[self.target]
        if target.defined:
            medn__hsm = target.getone()
            if context.unify_pairs(medn__hsm, sig.return_type) == medn__hsm:
                sig = sig.replace(return_type=medn__hsm)
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
        lmy__qfty = '*other* must be a {} but got a {} instead'
        raise TypeError(lmy__qfty.format(ForceLiteralArg, type(other)))
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
    ssb__fxapk = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for hocul__rbp, lzf__tbt in kwargs.items():
        wvmi__xdgx = None
        try:
            ummt__lscri = ir.Var(ir.Scope(None, loc), ir_utils.
                mk_unique_var('dummy'), loc)
            func_ir._definitions[ummt__lscri.name] = [lzf__tbt]
            wvmi__xdgx = get_const_value_inner(func_ir, ummt__lscri)
            func_ir._definitions.pop(ummt__lscri.name)
            if isinstance(wvmi__xdgx, str):
                wvmi__xdgx = sigutils._parse_signature_string(wvmi__xdgx)
            if isinstance(wvmi__xdgx, types.abstract._TypeMetaclass):
                raise BodoError(
                    f"""objmode type annotations require full data types, not just data type classes. For example, 'bodo.DataFrameType((bodo.float64[::1],), bodo.RangeIndexType(), ('A',))' is a valid data type but 'bodo.DataFrameType' is not.
Variable {hocul__rbp} is annotated as type class {wvmi__xdgx}."""
                    )
            assert isinstance(wvmi__xdgx, types.Type)
            if isinstance(wvmi__xdgx, (types.List, types.Set)):
                wvmi__xdgx = wvmi__xdgx.copy(reflected=False)
            ssb__fxapk[hocul__rbp] = wvmi__xdgx
        except BodoError as hil__jjy:
            raise
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(wvmi__xdgx, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(lzf__tbt, ir.Global):
                    msg = f'Global {lzf__tbt.name!r} is not defined.'
                if isinstance(lzf__tbt, ir.FreeVar):
                    msg = f'Freevar {lzf__tbt.name!r} is not defined.'
            if isinstance(lzf__tbt, ir.Expr) and lzf__tbt.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=hocul__rbp, msg=msg, loc=loc)
    for name, typ in ssb__fxapk.items():
        self._legalize_arg_type(name, typ, loc)
    return ssb__fxapk


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
    nuf__btzex = inst.arg
    assert nuf__btzex > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(nuf__btzex)]))
    tmps = [state.make_temp() for _ in range(nuf__btzex - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    hfll__yles = ir.Global('format', format, loc=self.loc)
    self.store(value=hfll__yles, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    xxqw__kyb = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=xxqw__kyb, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    nuf__btzex = inst.arg
    assert nuf__btzex > 0, 'invalid BUILD_STRING count'
    yqmrl__tum = self.get(strings[0])
    for other, tim__ulzec in zip(strings[1:], tmps):
        other = self.get(other)
        ogx__dzd = ir.Expr.binop(operator.add, lhs=yqmrl__tum, rhs=other,
            loc=self.loc)
        self.store(ogx__dzd, tim__ulzec)
        yqmrl__tum = self.get(tim__ulzec)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite import ir as lir
    kep__kxk = self.context.insert_const_string(self.module, attr)
    fnty = lir.FunctionType(lir.IntType(32), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, kep__kxk])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


def _created_inlined_var_name(function_name, var_name):
    tdr__ylwb = mk_unique_var(f'{var_name}')
    pgag__oeaoq = tdr__ylwb.replace('<', '_').replace('>', '_')
    pgag__oeaoq = pgag__oeaoq.replace('.', '_').replace('$', '_v')
    return pgag__oeaoq


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
                ltpl__cau = get_overload_const_str(val2)
                if ltpl__cau != 'ns':
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
        sttq__jje = states['defmap']
        if len(sttq__jje) == 0:
            jlk__bvily = assign.target
            numba.core.ssa._logger.debug('first assign: %s', jlk__bvily)
            if jlk__bvily.name not in scope.localvars:
                jlk__bvily = scope.define(assign.target.name, loc=assign.loc)
        else:
            jlk__bvily = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=jlk__bvily, value=assign.value, loc=
            assign.loc)
        sttq__jje[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    okrre__vlth = []
    for hocul__rbp, lzf__tbt in typing.npydecl.registry.globals:
        if hocul__rbp == func:
            okrre__vlth.append(lzf__tbt)
    for hocul__rbp, lzf__tbt in typing.templates.builtin_registry.globals:
        if hocul__rbp == func:
            okrre__vlth.append(lzf__tbt)
    if len(okrre__vlth) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return okrre__vlth


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    bats__ror = {}
    erj__iijz = find_topo_order(blocks)
    yqi__mtp = {}
    for label in erj__iijz:
        block = blocks[label]
        tzl__zeg = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                accd__ldgr = stmt.target.name
                rvjkf__tpy = stmt.value
                if (rvjkf__tpy.op == 'getattr' and rvjkf__tpy.attr in
                    arr_math and isinstance(typemap[rvjkf__tpy.value.name],
                    types.npytypes.Array)):
                    rvjkf__tpy = stmt.value
                    ecus__gsnux = rvjkf__tpy.value
                    bats__ror[accd__ldgr] = ecus__gsnux
                    scope = ecus__gsnux.scope
                    loc = ecus__gsnux.loc
                    pbqmi__pvqb = ir.Var(scope, mk_unique_var('$np_g_var'), loc
                        )
                    typemap[pbqmi__pvqb.name] = types.misc.Module(numpy)
                    bubx__hvm = ir.Global('np', numpy, loc)
                    mzvkp__gqb = ir.Assign(bubx__hvm, pbqmi__pvqb, loc)
                    rvjkf__tpy.value = pbqmi__pvqb
                    tzl__zeg.append(mzvkp__gqb)
                    func_ir._definitions[pbqmi__pvqb.name] = [bubx__hvm]
                    func = getattr(numpy, rvjkf__tpy.attr)
                    ubssk__bhch = get_np_ufunc_typ_lst(func)
                    yqi__mtp[accd__ldgr] = ubssk__bhch
                if (rvjkf__tpy.op == 'call' and rvjkf__tpy.func.name in
                    bats__ror):
                    ecus__gsnux = bats__ror[rvjkf__tpy.func.name]
                    uyboa__edms = calltypes.pop(rvjkf__tpy)
                    avaq__qrnsm = uyboa__edms.args[:len(rvjkf__tpy.args)]
                    zprab__ldax = {name: typemap[lzf__tbt.name] for name,
                        lzf__tbt in rvjkf__tpy.kws}
                    zkx__iumi = yqi__mtp[rvjkf__tpy.func.name]
                    lsyqp__nub = None
                    for fcy__rgb in zkx__iumi:
                        try:
                            lsyqp__nub = fcy__rgb.get_call_type(typingctx, 
                                [typemap[ecus__gsnux.name]] + list(
                                avaq__qrnsm), zprab__ldax)
                            typemap.pop(rvjkf__tpy.func.name)
                            typemap[rvjkf__tpy.func.name] = fcy__rgb
                            calltypes[rvjkf__tpy] = lsyqp__nub
                            break
                        except Exception as hil__jjy:
                            pass
                    if lsyqp__nub is None:
                        raise TypeError(
                            f'No valid template found for {rvjkf__tpy.func.name}'
                            )
                    rvjkf__tpy.args = [ecus__gsnux] + rvjkf__tpy.args
            tzl__zeg.append(stmt)
        block.body = tzl__zeg


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    kwuv__iwj = ufunc.nin
    mwy__mpsom = ufunc.nout
    khhbk__lmnw = ufunc.nargs
    assert khhbk__lmnw == kwuv__iwj + mwy__mpsom
    if len(args) < kwuv__iwj:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), kwuv__iwj))
    if len(args) > khhbk__lmnw:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args),
            khhbk__lmnw))
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    udnwv__fsz = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    lei__nfn = max(udnwv__fsz)
    gzvr__tlz = args[kwuv__iwj:]
    if not all(d == lei__nfn for d in udnwv__fsz[kwuv__iwj:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(gni__qnepk, types.ArrayCompatible) and not
        isinstance(gni__qnepk, types.Bytes) for gni__qnepk in gzvr__tlz):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(gni__qnepk.mutable for gni__qnepk in gzvr__tlz):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    xren__ucub = [(x.dtype if isinstance(x, types.ArrayCompatible) and not
        isinstance(x, types.Bytes) else x) for x in args]
    wyzw__xhs = None
    if lei__nfn > 0 and len(gzvr__tlz) < ufunc.nout:
        wyzw__xhs = 'C'
        spk__hmolr = [(x.layout if isinstance(x, types.ArrayCompatible) and
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in spk__hmolr and 'F' in spk__hmolr:
            wyzw__xhs = 'F'
    return xren__ucub, gzvr__tlz, lei__nfn, wyzw__xhs


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
        hxnj__lcyrc = 'Dict.key_type cannot be of type {}'
        raise TypingError(hxnj__lcyrc.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        hxnj__lcyrc = 'Dict.value_type cannot be of type {}'
        raise TypingError(hxnj__lcyrc.format(valty))
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
    bxaka__kzi = self.context, tuple(args), tuple(kws.items())
    try:
        impl, args = self._impl_cache[bxaka__kzi]
        return impl, args
    except KeyError as hil__jjy:
        pass
    impl, args = self._build_impl(bxaka__kzi, args, kws)
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
    rjpmr__zdu = False
    blocks = parfor.loop_body.copy()
    for label, block in blocks.items():
        if len(block.body):
            iqlk__bnr = block.body[-1]
            if isinstance(iqlk__bnr, ir.Branch):
                if len(blocks[iqlk__bnr.truebr].body) == 1 and len(blocks[
                    iqlk__bnr.falsebr].body) == 1:
                    iimad__uas = blocks[iqlk__bnr.truebr].body[0]
                    tis__psfbl = blocks[iqlk__bnr.falsebr].body[0]
                    if isinstance(iimad__uas, ir.Jump) and isinstance(
                        tis__psfbl, ir.Jump
                        ) and iimad__uas.target == tis__psfbl.target:
                        parfor.loop_body[label].body[-1] = ir.Jump(iimad__uas
                            .target, iqlk__bnr.loc)
                        rjpmr__zdu = True
                elif len(blocks[iqlk__bnr.truebr].body) == 1:
                    iimad__uas = blocks[iqlk__bnr.truebr].body[0]
                    if isinstance(iimad__uas, ir.Jump
                        ) and iimad__uas.target == iqlk__bnr.falsebr:
                        parfor.loop_body[label].body[-1] = ir.Jump(iimad__uas
                            .target, iqlk__bnr.loc)
                        rjpmr__zdu = True
                elif len(blocks[iqlk__bnr.falsebr].body) == 1:
                    tis__psfbl = blocks[iqlk__bnr.falsebr].body[0]
                    if isinstance(tis__psfbl, ir.Jump
                        ) and tis__psfbl.target == iqlk__bnr.truebr:
                        parfor.loop_body[label].body[-1] = ir.Jump(tis__psfbl
                            .target, iqlk__bnr.loc)
                        rjpmr__zdu = True
    return rjpmr__zdu


def remove_dead_parfor(parfor, lives, lives_n_aliases, arg_aliases,
    alias_map, func_ir, typemap):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    from numba.core.ir_utils import find_topo_order
    from numba.parfors.parfor import _add_liveness_return_block, _update_parfor_get_setitems, dummy_return_in_loop_body, get_index_var, remove_dead_parfor_recursive, simplify_parfor_body_CFG
    with dummy_return_in_loop_body(parfor.loop_body):
        ftp__gia = find_topo_order(parfor.loop_body)
    gcske__veyu = ftp__gia[0]
    itwn__wqkgc = {}
    _update_parfor_get_setitems(parfor.loop_body[gcske__veyu].body, parfor.
        index_var, alias_map, itwn__wqkgc, lives_n_aliases)
    trjan__qoft = set(itwn__wqkgc.keys())
    for ohcsx__vbm in ftp__gia:
        if ohcsx__vbm == gcske__veyu:
            continue
        for stmt in parfor.loop_body[ohcsx__vbm].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            wjcs__wpps = set(lzf__tbt.name for lzf__tbt in stmt.list_vars())
            jjb__pfn = wjcs__wpps & trjan__qoft
            for a in jjb__pfn:
                itwn__wqkgc.pop(a, None)
    for ohcsx__vbm in ftp__gia:
        if ohcsx__vbm == gcske__veyu:
            continue
        block = parfor.loop_body[ohcsx__vbm]
        yuwo__uns = itwn__wqkgc.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            yuwo__uns, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    xzz__hug = max(blocks.keys())
    vxvs__pkg, bwtq__mjpnn = _add_liveness_return_block(blocks,
        lives_n_aliases, typemap)
    mtm__intvj = ir.Jump(vxvs__pkg, ir.Loc('parfors_dummy', -1))
    blocks[xzz__hug].body.append(mtm__intvj)
    oppk__wvzkw = compute_cfg_from_blocks(blocks)
    dozu__yvv = compute_use_defs(blocks)
    yutd__qahbe = compute_live_map(oppk__wvzkw, blocks, dozu__yvv.usemap,
        dozu__yvv.defmap)
    alias_set = set(alias_map.keys())
    for label, block in blocks.items():
        tzl__zeg = []
        tuku__sekp = {lzf__tbt.name for lzf__tbt in block.terminator.
            list_vars()}
        for vsny__tqcaq, cfgjg__ily in oppk__wvzkw.successors(label):
            tuku__sekp |= yutd__qahbe[vsny__tqcaq]
        for stmt in reversed(block.body):
            fvr__aowm = tuku__sekp & alias_set
            for lzf__tbt in fvr__aowm:
                tuku__sekp |= alias_map[lzf__tbt]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in tuku__sekp and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                tdsxj__qna = guard(find_callname, func_ir, stmt.value)
                if tdsxj__qna == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in tuku__sekp and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            tuku__sekp |= {lzf__tbt.name for lzf__tbt in stmt.list_vars()}
            tzl__zeg.append(stmt)
        tzl__zeg.reverse()
        block.body = tzl__zeg
    typemap.pop(bwtq__mjpnn.name)
    blocks[xzz__hug].body.pop()
    rjpmr__zdu = True
    while rjpmr__zdu:
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
        rjpmr__zdu = trim_empty_parfor_branches(parfor)
    qdzn__grd = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        qdzn__grd &= len(block.body) == 0
    if qdzn__grd:
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
    jpzjv__znbye = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                jpzjv__znbye += 1
                parfor = stmt
                olnsx__fgfw = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = olnsx__fgfw.scope
                loc = ir.Loc('parfors_dummy', -1)
                hgvrc__auw = ir.Var(scope, mk_unique_var('$const'), loc)
                olnsx__fgfw.body.append(ir.Assign(ir.Const(0, loc),
                    hgvrc__auw, loc))
                olnsx__fgfw.body.append(ir.Return(hgvrc__auw, loc))
                oppk__wvzkw = compute_cfg_from_blocks(parfor.loop_body)
                for uuxyq__ioavb in oppk__wvzkw.dead_nodes():
                    del parfor.loop_body[uuxyq__ioavb]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                olnsx__fgfw = parfor.loop_body[max(parfor.loop_body.keys())]
                olnsx__fgfw.body.pop()
                olnsx__fgfw.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return jpzjv__znbye


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.simplify_parfor_body_CFG)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '437ae96a5e8ec64a2b69a4f23ba8402a1d170262a5400aa0aa7bfe59e03bf726':
        warnings.warn('simplify_parfor_body_CFG has changed')
numba.parfors.parfor.simplify_parfor_body_CFG = simplify_parfor_body_CFG


def simplify_CFG(blocks):
    from numba.core.analysis import compute_cfg_from_blocks
    from numba.core.ir_utils import merge_adjacent_blocks, rename_labels
    oppk__wvzkw = compute_cfg_from_blocks(blocks)

    def find_single_branch(label):
        block = blocks[label]
        return len(block.body) == 1 and isinstance(block.body[0], ir.Branch
            ) and label != oppk__wvzkw.entry_point()
    srtm__rczo = list(filter(find_single_branch, blocks.keys()))
    jiybs__ofzm = set()
    for label in srtm__rczo:
        inst = blocks[label].body[0]
        rnu__dip = oppk__wvzkw.predecessors(label)
        oesa__uqfr = True
        for rgggu__ztzlw, eimg__yfaj in rnu__dip:
            block = blocks[rgggu__ztzlw]
            if isinstance(block.body[-1], ir.Jump):
                block.body[-1] = copy.copy(inst)
            else:
                oesa__uqfr = False
        if oesa__uqfr:
            jiybs__ofzm.add(label)
    for label in jiybs__ofzm:
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
            kqp__sgtih = self.overloads.get(tuple(args))
            if kqp__sgtih is not None:
                return kqp__sgtih.entry_point
            self._pre_compile(args, return_type, flags)
            guqz__vgo = self.func_ir
            nlurm__asz = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=nlurm__asz):
                cres = compiler.compile_ir(typingctx=self.typingctx,
                    targetctx=self.targetctx, func_ir=guqz__vgo, args=args,
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
        wva__jjk = copy.deepcopy(flags)
        wva__jjk.no_rewrites = True

        def compile_local(the_ir, the_flags):
            chf__cst = pipeline_class(typingctx, targetctx, library, args,
                return_type, the_flags, locals)
            return chf__cst.compile_ir(func_ir=the_ir, lifted=lifted,
                lifted_from=lifted_from)
        hvb__widr = compile_local(func_ir, wva__jjk)
        gxq__szii = None
        if not flags.no_rewrites:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', errors.NumbaWarning)
                try:
                    gxq__szii = compile_local(func_ir, flags)
                except Exception as hil__jjy:
                    pass
        if gxq__szii is not None:
            cres = gxq__szii
        else:
            cres = hvb__widr
        return cres
    else:
        chf__cst = pipeline_class(typingctx, targetctx, library, args,
            return_type, flags, locals)
        return chf__cst.compile_ir(func_ir=func_ir, lifted=lifted,
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
    zssws__ihbm = self.get_data_type(typ.dtype)
    eizl__hjp = 10 ** 7
    if self.allow_dynamic_globals and (typ.layout not in 'FC' or ary.nbytes >
        eizl__hjp):
        zjsr__vvqvp = ary.ctypes.data
        qhu__zvh = self.add_dynamic_addr(builder, zjsr__vvqvp, info=str(
            type(zjsr__vvqvp)))
        xxa__noopc = self.add_dynamic_addr(builder, id(ary), info=str(type(
            ary)))
        self.global_arrays.append(ary)
    else:
        wyq__qqngs = ary.flatten(order=typ.layout)
        if isinstance(typ.dtype, (types.NPDatetime, types.NPTimedelta)):
            wyq__qqngs = wyq__qqngs.view('int64')
        val = bytearray(wyq__qqngs.data)
        uqnu__lmx = lir.Constant(lir.ArrayType(lir.IntType(8), len(val)), val)
        qhu__zvh = cgutils.global_constant(builder, '.const.array.data',
            uqnu__lmx)
        qhu__zvh.align = self.get_abi_alignment(zssws__ihbm)
        xxa__noopc = None
    sdrwi__kexqq = self.get_value_type(types.intp)
    fxlck__zzfe = [self.get_constant(types.intp, wazf__viav) for wazf__viav in
        ary.shape]
    vqp__viu = lir.Constant(lir.ArrayType(sdrwi__kexqq, len(fxlck__zzfe)),
        fxlck__zzfe)
    oxxl__usgh = [self.get_constant(types.intp, wazf__viav) for wazf__viav in
        ary.strides]
    drgkk__vsegm = lir.Constant(lir.ArrayType(sdrwi__kexqq, len(oxxl__usgh)
        ), oxxl__usgh)
    kajan__gov = self.get_constant(types.intp, ary.dtype.itemsize)
    ujyrj__jhgy = self.get_constant(types.intp, math.prod(ary.shape))
    return lir.Constant.literal_struct([self.get_constant_null(types.
        MemInfoPointer(typ.dtype)), self.get_constant_null(types.pyobject),
        ujyrj__jhgy, kajan__gov, qhu__zvh.bitcast(self.get_value_type(types
        .CPointer(typ.dtype))), vqp__viu, drgkk__vsegm])


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
    pdxgm__ezeu = lir.FunctionType(_word_type, [_word_type.as_pointer()])
    slfk__cuh = lir.Function(module, pdxgm__ezeu, name='nrt_atomic_{0}'.
        format(op))
    [qvtrm__etyn] = slfk__cuh.args
    rmdd__sspf = slfk__cuh.append_basic_block()
    builder = lir.IRBuilder(rmdd__sspf)
    ijel__ozuxh = lir.Constant(_word_type, 1)
    if False:
        que__uxwic = builder.atomic_rmw(op, qvtrm__etyn, ijel__ozuxh,
            ordering=ordering)
        res = getattr(builder, op)(que__uxwic, ijel__ozuxh)
        builder.ret(res)
    else:
        que__uxwic = builder.load(qvtrm__etyn)
        irxfw__ikys = getattr(builder, op)(que__uxwic, ijel__ozuxh)
        sou__cah = builder.icmp_signed('!=', que__uxwic, lir.Constant(
            que__uxwic.type, -1))
        with cgutils.if_likely(builder, sou__cah):
            builder.store(irxfw__ikys, qvtrm__etyn)
        builder.ret(irxfw__ikys)
    return slfk__cuh


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
        jbtji__dhoy = state.targetctx.codegen()
        state.library = jbtji__dhoy.create_library(state.func_id.func_qualname)
        state.library.enable_object_caching()
    library = state.library
    targetctx = state.targetctx
    udy__gsg = state.func_ir
    typemap = state.typemap
    sil__rozha = state.return_type
    calltypes = state.calltypes
    flags = state.flags
    metadata = state.metadata
    ygzbx__mpj = llvm.passmanagers.dump_refprune_stats()
    msg = 'Function %s failed at nopython mode lowering' % (state.func_id.
        func_name,)
    with fallback_context(state, msg):
        fndesc = funcdesc.PythonFunctionDescriptor.from_specialized_function(
            udy__gsg, typemap, sil__rozha, calltypes, mangler=targetctx.
            mangler, inline=flags.forceinline, noalias=flags.noalias,
            abi_tags=[flags.get_mangle_string()])
        targetctx.global_arrays = []
        with targetctx.push_code_library(library):
            yshw__kdbb = lowering.Lower(targetctx, library, fndesc,
                udy__gsg, metadata=metadata)
            yshw__kdbb.lower()
            if not flags.no_cpython_wrapper:
                yshw__kdbb.create_cpython_wrapper(flags.release_gil)
            if not flags.no_cfunc_wrapper:
                for t in state.args:
                    if isinstance(t, (types.Omitted, types.Generator)):
                        break
                else:
                    if isinstance(sil__rozha, (types.Optional, types.Generator)
                        ):
                        pass
                    else:
                        yshw__kdbb.create_cfunc_wrapper()
            env = yshw__kdbb.env
            zspu__sqv = yshw__kdbb.call_helper
            del yshw__kdbb
        from numba.core.compiler import _LowerResult
        if flags.no_compile:
            state['cr'] = _LowerResult(fndesc, zspu__sqv, cfunc=None, env=env)
        else:
            egh__fvt = targetctx.get_executable(library, fndesc, env)
            targetctx.insert_user_function(egh__fvt, fndesc, [library])
            state['cr'] = _LowerResult(fndesc, zspu__sqv, cfunc=egh__fvt,
                env=env)
        metadata['global_arrs'] = targetctx.global_arrays
        targetctx.global_arrays = []
        squp__hdmp = llvm.passmanagers.dump_refprune_stats()
        metadata['prune_stats'] = squp__hdmp - ygzbx__mpj
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
        gpiu__uus = nth.typeof(itemobj)
        with c.builder.if_then(cgutils.is_null(c.builder, gpiu__uus),
            likely=False):
            c.builder.store(cgutils.true_bit, errorptr)
            sftwf__lrdd.do_break()
        bepo__fqewr = c.builder.icmp_signed('!=', gpiu__uus, expected_typobj)
        if not isinstance(typ.dtype, types.Optional):
            with c.builder.if_then(bepo__fqewr, likely=False):
                c.builder.store(cgutils.true_bit, errorptr)
                c.pyapi.err_format('PyExc_TypeError',
                    "can't unbox heterogeneous list: %S != %S",
                    expected_typobj, gpiu__uus)
                c.pyapi.decref(gpiu__uus)
                sftwf__lrdd.do_break()
        c.pyapi.decref(gpiu__uus)
    dilf__kgpj, list = listobj.ListInstance.allocate_ex(c.context, c.
        builder, typ, size)
    with c.builder.if_else(dilf__kgpj, likely=True) as (uqc__opav, mwcls__vxfr
        ):
        with uqc__opav:
            list.size = size
            clwg__haacd = lir.Constant(size.type, 0)
            with c.builder.if_then(c.builder.icmp_signed('>', size,
                clwg__haacd), likely=True):
                with _NumbaTypeHelper(c) as nth:
                    expected_typobj = nth.typeof(c.pyapi.list_getitem(obj,
                        clwg__haacd))
                    with cgutils.for_range(c.builder, size) as sftwf__lrdd:
                        itemobj = c.pyapi.list_getitem(obj, sftwf__lrdd.index)
                        check_element_type(nth, itemobj, expected_typobj)
                        xma__lqmc = c.unbox(typ.dtype, itemobj)
                        with c.builder.if_then(xma__lqmc.is_error, likely=False
                            ):
                            c.builder.store(cgutils.true_bit, errorptr)
                            sftwf__lrdd.do_break()
                        list.setitem(sftwf__lrdd.index, xma__lqmc.value,
                            incref=False)
                    c.pyapi.decref(expected_typobj)
            if typ.reflected:
                list.parent = obj
            with c.builder.if_then(c.builder.not_(c.builder.load(errorptr)),
                likely=False):
                c.pyapi.object_set_private_data(obj, list.meminfo)
            list.set_dirty(False)
            c.builder.store(list.value, listptr)
        with mwcls__vxfr:
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
    bfvqz__sand, bwa__onmpc, jlf__aumhz, zos__flzut, toyr__jfzh = (
        compile_time_get_string_data(literal_string))
    yfahf__mkhq = builder.module
    gv = context.insert_const_bytes(yfahf__mkhq, bfvqz__sand)
    return lir.Constant.literal_struct([gv, context.get_constant(types.intp,
        bwa__onmpc), context.get_constant(types.int32, jlf__aumhz), context
        .get_constant(types.uint32, zos__flzut), context.get_constant(
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
    mcx__pok = None
    if isinstance(shape, types.Integer):
        mcx__pok = 1
    elif isinstance(shape, (types.Tuple, types.UniTuple)):
        if all(isinstance(wazf__viav, (types.Integer, types.IntEnumMember)) for
            wazf__viav in shape):
            mcx__pok = len(shape)
    return mcx__pok


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
            mcx__pok = typ.ndim if isinstance(typ, types.ArrayCompatible
                ) else len(typ)
            if mcx__pok == 0:
                return name,
            else:
                return tuple('{}#{}'.format(name, i) for i in range(mcx__pok))
        else:
            return name,
    elif isinstance(obj, ir.Const):
        if isinstance(obj.value, tuple):
            return obj.value
        else:
            return obj.value,
    elif isinstance(obj, tuple):

        def get_names(x):
            zlv__opq = self._get_names(x)
            if len(zlv__opq) != 0:
                return zlv__opq[0]
            return zlv__opq
        return tuple(get_names(x) for x in obj)
    elif isinstance(obj, int):
        return obj,
    return ()


def get_equiv_const(self, obj):
    zlv__opq = self._get_names(obj)
    if len(zlv__opq) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_const(zlv__opq[0])


def get_equiv_set(self, obj):
    zlv__opq = self._get_names(obj)
    if len(zlv__opq) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_set(zlv__opq[0])


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
    pde__vlsbi = []
    for aig__dtiq in func_ir.arg_names:
        if aig__dtiq in typemap and isinstance(typemap[aig__dtiq], types.
            containers.UniTuple) and typemap[aig__dtiq].count > 1000:
            msg = (
                """Tuple '{}' length must be smaller than 1000.
Large tuples lead to the generation of a prohibitively large LLVM IR which causes excessive memory pressure and large compile times.
As an alternative, the use of a 'list' is recommended in place of a 'tuple' as lists do not suffer from this problem."""
                .format(aig__dtiq))
            raise errors.UnsupportedError(msg, func_ir.loc)
    for wkgwu__lfce in func_ir.blocks.values():
        for stmt in wkgwu__lfce.find_insts(ir.Assign):
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'make_function':
                    val = stmt.value
                    fbijl__nkhs = getattr(val, 'code', None)
                    if fbijl__nkhs is not None:
                        if getattr(val, 'closure', None) is not None:
                            qbani__ccd = '<creating a function from a closure>'
                            ogx__dzd = ''
                        else:
                            qbani__ccd = fbijl__nkhs.co_name
                            ogx__dzd = '(%s) ' % qbani__ccd
                    else:
                        qbani__ccd = '<could not ascertain use case>'
                        ogx__dzd = ''
                    msg = (
                        'Numba encountered the use of a language feature it does not support in this context: %s (op code: make_function not supported). If the feature is explicitly supported it is likely that the result of the expression %sis being used in an unsupported manner.'
                         % (qbani__ccd, ogx__dzd))
                    raise errors.UnsupportedError(msg, stmt.value.loc)
            if isinstance(stmt.value, (ir.Global, ir.FreeVar)):
                val = stmt.value
                val = getattr(val, 'value', None)
                if val is None:
                    continue
                qugks__flvxp = False
                if isinstance(val, pytypes.FunctionType):
                    qugks__flvxp = val in {numba.gdb, numba.gdb_init}
                if not qugks__flvxp:
                    qugks__flvxp = getattr(val, '_name', '') == 'gdb_internal'
                if qugks__flvxp:
                    pde__vlsbi.append(stmt.loc)
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'getattr' and stmt.value.attr == 'view':
                    var = stmt.value.value.name
                    if isinstance(typemap[var], types.Array):
                        continue
                    gzgj__tsycf = func_ir.get_definition(var)
                    vvzwo__cadd = guard(find_callname, func_ir, gzgj__tsycf)
                    if vvzwo__cadd and vvzwo__cadd[1] == 'numpy':
                        ty = getattr(numpy, vvzwo__cadd[0])
                        if numpy.issubdtype(ty, numpy.integer
                            ) or numpy.issubdtype(ty, numpy.floating):
                            continue
                    uzyz__erxee = '' if var.startswith('$'
                        ) else "'{}' ".format(var)
                    raise TypingError(
                        "'view' can only be called on NumPy dtypes, try wrapping the variable {}with 'np.<dtype>()'"
                        .format(uzyz__erxee), loc=stmt.loc)
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
    if len(pde__vlsbi) > 1:
        msg = """Calling either numba.gdb() or numba.gdb_init() more than once in a function is unsupported (strange things happen!), use numba.gdb_breakpoint() to create additional breakpoints instead.

Relevant documentation is available here:
https://numba.pydata.org/numba-doc/latest/user/troubleshoot.html/troubleshoot.html#using-numba-s-direct-gdb-bindings-in-nopython-mode

Conflicting calls found at:
 %s"""
        fwrqx__kmnw = '\n'.join([x.strformat() for x in pde__vlsbi])
        raise errors.UnsupportedError(msg % fwrqx__kmnw)


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
    hocul__rbp, lzf__tbt = next(iter(val.items()))
    qyuu__egb = typeof_impl(hocul__rbp, c)
    blyy__hiacr = typeof_impl(lzf__tbt, c)
    if qyuu__egb is None or blyy__hiacr is None:
        raise ValueError(
            f'Cannot type dict element type {type(hocul__rbp)}, {type(lzf__tbt)}'
            )
    return types.DictType(qyuu__egb, blyy__hiacr)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    wpc__awqh = cgutils.alloca_once_value(c.builder, val)
    qwss__muom = c.pyapi.object_hasattr_string(val, '_opaque')
    jbs__crb = c.builder.icmp_unsigned('==', qwss__muom, lir.Constant(
        qwss__muom.type, 0))
    xcdc__jcnmm = typ.key_type
    zpsq__soi = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(xcdc__jcnmm, zpsq__soi)

    def copy_dict(out_dict, in_dict):
        for hocul__rbp, lzf__tbt in in_dict.items():
            out_dict[hocul__rbp] = lzf__tbt
    with c.builder.if_then(jbs__crb):
        qsz__tqzgs = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        tpaq__wticv = c.pyapi.call_function_objargs(qsz__tqzgs, [])
        aoem__rieme = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(aoem__rieme, [tpaq__wticv, val])
        c.builder.store(tpaq__wticv, wpc__awqh)
    val = c.builder.load(wpc__awqh)
    veco__cmxxs = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    skyvv__glyc = c.pyapi.object_type(val)
    jgyx__nsjh = c.builder.icmp_unsigned('==', skyvv__glyc, veco__cmxxs)
    with c.builder.if_else(jgyx__nsjh) as (vlz__gzb, iaxs__jjw):
        with vlz__gzb:
            hvet__fxvc = c.pyapi.object_getattr_string(val, '_opaque')
            wtn__dht = types.MemInfoPointer(types.voidptr)
            xma__lqmc = c.unbox(wtn__dht, hvet__fxvc)
            mi = xma__lqmc.value
            sln__iuqz = wtn__dht, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *sln__iuqz)
            vsly__wpd = context.get_constant_null(sln__iuqz[1])
            args = mi, vsly__wpd
            mmn__ami, bbscm__nmsv = c.pyapi.call_jit_code(convert, sig, args)
            c.context.nrt.decref(c.builder, typ, bbscm__nmsv)
            c.pyapi.decref(hvet__fxvc)
            vbio__rem = c.builder.basic_block
        with iaxs__jjw:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", skyvv__glyc, veco__cmxxs)
            vsp__yeqs = c.builder.basic_block
    otu__jge = c.builder.phi(bbscm__nmsv.type)
    larm__bvecv = c.builder.phi(mmn__ami.type)
    otu__jge.add_incoming(bbscm__nmsv, vbio__rem)
    otu__jge.add_incoming(bbscm__nmsv.type(None), vsp__yeqs)
    larm__bvecv.add_incoming(mmn__ami, vbio__rem)
    larm__bvecv.add_incoming(cgutils.true_bit, vsp__yeqs)
    c.pyapi.decref(veco__cmxxs)
    c.pyapi.decref(skyvv__glyc)
    with c.builder.if_then(jbs__crb):
        c.pyapi.decref(val)
    return NativeValue(otu__jge, is_error=larm__bvecv)


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
    fwhm__zqny = ir.Expr.getattr(target, 'update', loc=self.loc)
    self.store(value=fwhm__zqny, name=updatevar)
    ypbqb__niox = ir.Expr.call(self.get(updatevar), (value,), (), loc=self.loc)
    self.store(value=ypbqb__niox, name=res)


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
        for hocul__rbp, lzf__tbt in other.items():
            d[hocul__rbp] = lzf__tbt
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
    ogx__dzd = ir.Expr.call(func, [], [], loc=self.loc, vararg=vararg,
        varkwarg=varkwarg)
    self.store(ogx__dzd, res)


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
    uklm__mphz = PassManager(name)
    if state.func_ir is None:
        uklm__mphz.add_pass(TranslateByteCode, 'analyzing bytecode')
        if PYVERSION == (3, 10):
            uklm__mphz.add_pass(Bodo310ByteCodePass,
                'Apply Python 3.10 bytecode changes')
        uklm__mphz.add_pass(FixupArgs, 'fix up args')
    uklm__mphz.add_pass(IRProcessing, 'processing IR')
    uklm__mphz.add_pass(WithLifting, 'Handle with contexts')
    uklm__mphz.add_pass(InlineClosureLikes,
        'inline calls to locally defined closures')
    if not state.flags.no_rewrites:
        uklm__mphz.add_pass(RewriteSemanticConstants,
            'rewrite semantic constants')
        uklm__mphz.add_pass(DeadBranchPrune, 'dead branch pruning')
        uklm__mphz.add_pass(GenericRewrites, 'nopython rewrites')
    uklm__mphz.add_pass(MakeFunctionToJitFunction,
        'convert make_function into JIT functions')
    uklm__mphz.add_pass(InlineInlinables, 'inline inlinable functions')
    if not state.flags.no_rewrites:
        uklm__mphz.add_pass(DeadBranchPrune, 'dead branch pruning')
    uklm__mphz.add_pass(FindLiterallyCalls, 'find literally calls')
    uklm__mphz.add_pass(LiteralUnroll, 'handles literal_unroll')
    if state.flags.enable_ssa:
        uklm__mphz.add_pass(ReconstructSSA, 'ssa')
    uklm__mphz.add_pass(LiteralPropagationSubPipelinePass,
        'Literal propagation')
    uklm__mphz.finalize()
    return uklm__mphz


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
    a, fqg__camm = args
    if isinstance(a, types.List) and isinstance(fqg__camm, types.Integer):
        return signature(a, a, types.intp)
    elif isinstance(a, types.Integer) and isinstance(fqg__camm, types.List):
        return signature(fqg__camm, types.intp, fqg__camm)


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
        dhtz__waac, vwnsv__frrg = 0, 1
    else:
        dhtz__waac, vwnsv__frrg = 1, 0
    spn__wwx = ListInstance(context, builder, sig.args[dhtz__waac], args[
        dhtz__waac])
    ioz__kmr = spn__wwx.size
    lxrat__wtr = args[vwnsv__frrg]
    clwg__haacd = lir.Constant(lxrat__wtr.type, 0)
    lxrat__wtr = builder.select(cgutils.is_neg_int(builder, lxrat__wtr),
        clwg__haacd, lxrat__wtr)
    ujyrj__jhgy = builder.mul(lxrat__wtr, ioz__kmr)
    snarc__oxply = ListInstance.allocate(context, builder, sig.return_type,
        ujyrj__jhgy)
    snarc__oxply.size = ujyrj__jhgy
    with cgutils.for_range_slice(builder, clwg__haacd, ujyrj__jhgy,
        ioz__kmr, inc=True) as (iqdfb__uii, _):
        with cgutils.for_range(builder, ioz__kmr) as sftwf__lrdd:
            value = spn__wwx.getitem(sftwf__lrdd.index)
            snarc__oxply.setitem(builder.add(sftwf__lrdd.index, iqdfb__uii),
                value, incref=True)
    return impl_ret_new_ref(context, builder, sig.return_type, snarc__oxply
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
    tclp__vuyav = first.unify(self, second)
    if tclp__vuyav is not None:
        return tclp__vuyav
    tclp__vuyav = second.unify(self, first)
    if tclp__vuyav is not None:
        return tclp__vuyav
    thgya__wszww = self.can_convert(fromty=first, toty=second)
    if thgya__wszww is not None and thgya__wszww <= Conversion.safe:
        return second
    thgya__wszww = self.can_convert(fromty=second, toty=first)
    if thgya__wszww is not None and thgya__wszww <= Conversion.safe:
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
    ujyrj__jhgy = payload.used
    listobj = c.pyapi.list_new(ujyrj__jhgy)
    dilf__kgpj = cgutils.is_not_null(c.builder, listobj)
    with c.builder.if_then(dilf__kgpj, likely=True):
        index = cgutils.alloca_once_value(c.builder, ir.Constant(
            ujyrj__jhgy.type, 0))
        with payload._iterate() as sftwf__lrdd:
            i = c.builder.load(index)
            item = sftwf__lrdd.entry.key
            c.context.nrt.incref(c.builder, typ.dtype, item)
            itemobj = c.box(typ.dtype, item)
            c.pyapi.list_setitem(listobj, i, itemobj)
            i = c.builder.add(i, ir.Constant(i.type, 1))
            c.builder.store(i, index)
    return dilf__kgpj, listobj


def _lookup(self, item, h, for_insert=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    yiw__cvhjk = h.type
    vbh__zbck = self.mask
    dtype = self._ty.dtype
    qnd__sgu = context.typing_context
    fnty = qnd__sgu.resolve_value_type(operator.eq)
    sig = fnty.get_call_type(qnd__sgu, (dtype, dtype), {})
    mwe__rwkd = context.get_function(fnty, sig)
    zar__axq = ir.Constant(yiw__cvhjk, 1)
    sxfhg__xjetd = ir.Constant(yiw__cvhjk, 5)
    grn__cnc = cgutils.alloca_once_value(builder, h)
    index = cgutils.alloca_once_value(builder, builder.and_(h, vbh__zbck))
    if for_insert:
        vbp__udzw = vbh__zbck.type(-1)
        wows__dqgbi = cgutils.alloca_once_value(builder, vbp__udzw)
    phqj__xlk = builder.append_basic_block('lookup.body')
    pbn__opn = builder.append_basic_block('lookup.found')
    meby__ymk = builder.append_basic_block('lookup.not_found')
    itbhl__msw = builder.append_basic_block('lookup.end')

    def check_entry(i):
        entry = self.get_entry(i)
        prx__jadj = entry.hash
        with builder.if_then(builder.icmp_unsigned('==', h, prx__jadj)):
            wyqxk__rtu = mwe__rwkd(builder, (item, entry.key))
            with builder.if_then(wyqxk__rtu):
                builder.branch(pbn__opn)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, prx__jadj)):
            builder.branch(meby__ymk)
        if for_insert:
            with builder.if_then(numba.cpython.setobj.is_hash_deleted(
                context, builder, prx__jadj)):
                ojov__jkh = builder.load(wows__dqgbi)
                ojov__jkh = builder.select(builder.icmp_unsigned('==',
                    ojov__jkh, vbp__udzw), i, ojov__jkh)
                builder.store(ojov__jkh, wows__dqgbi)
    with cgutils.for_range(builder, ir.Constant(yiw__cvhjk, numba.cpython.
        setobj.LINEAR_PROBES)):
        i = builder.load(index)
        check_entry(i)
        i = builder.add(i, zar__axq)
        i = builder.and_(i, vbh__zbck)
        builder.store(i, index)
    builder.branch(phqj__xlk)
    with builder.goto_block(phqj__xlk):
        i = builder.load(index)
        check_entry(i)
        rgggu__ztzlw = builder.load(grn__cnc)
        rgggu__ztzlw = builder.lshr(rgggu__ztzlw, sxfhg__xjetd)
        i = builder.add(zar__axq, builder.mul(i, sxfhg__xjetd))
        i = builder.and_(vbh__zbck, builder.add(i, rgggu__ztzlw))
        builder.store(i, index)
        builder.store(rgggu__ztzlw, grn__cnc)
        builder.branch(phqj__xlk)
    with builder.goto_block(meby__ymk):
        if for_insert:
            i = builder.load(index)
            ojov__jkh = builder.load(wows__dqgbi)
            i = builder.select(builder.icmp_unsigned('==', ojov__jkh,
                vbp__udzw), i, ojov__jkh)
            builder.store(i, index)
        builder.branch(itbhl__msw)
    with builder.goto_block(pbn__opn):
        builder.branch(itbhl__msw)
    builder.position_at_end(itbhl__msw)
    qugks__flvxp = builder.phi(ir.IntType(1), 'found')
    qugks__flvxp.add_incoming(cgutils.true_bit, pbn__opn)
    qugks__flvxp.add_incoming(cgutils.false_bit, meby__ymk)
    return qugks__flvxp, builder.load(index)


def _add_entry(self, payload, entry, item, h, do_resize=True):
    context = self._context
    builder = self._builder
    lfxw__kbwc = entry.hash
    entry.hash = h
    context.nrt.incref(builder, self._ty.dtype, item)
    entry.key = item
    zbx__deze = payload.used
    zar__axq = ir.Constant(zbx__deze.type, 1)
    zbx__deze = payload.used = builder.add(zbx__deze, zar__axq)
    with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
        builder, lfxw__kbwc), likely=True):
        payload.fill = builder.add(payload.fill, zar__axq)
    if do_resize:
        self.upsize(zbx__deze)
    self.set_dirty(True)


def _add_key(self, payload, item, h, do_resize=True):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    qugks__flvxp, i = payload._lookup(item, h, for_insert=True)
    rgdm__hcgx = builder.not_(qugks__flvxp)
    with builder.if_then(rgdm__hcgx):
        entry = payload.get_entry(i)
        lfxw__kbwc = entry.hash
        entry.hash = h
        context.nrt.incref(builder, self._ty.dtype, item)
        entry.key = item
        zbx__deze = payload.used
        zar__axq = ir.Constant(zbx__deze.type, 1)
        zbx__deze = payload.used = builder.add(zbx__deze, zar__axq)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, lfxw__kbwc), likely=True):
            payload.fill = builder.add(payload.fill, zar__axq)
        if do_resize:
            self.upsize(zbx__deze)
        self.set_dirty(True)


def _remove_entry(self, payload, entry, do_resize=True):
    from llvmlite import ir
    entry.hash = ir.Constant(entry.hash.type, numba.cpython.setobj.DELETED)
    self._context.nrt.decref(self._builder, self._ty.dtype, entry.key)
    zbx__deze = payload.used
    zar__axq = ir.Constant(zbx__deze.type, 1)
    zbx__deze = payload.used = self._builder.sub(zbx__deze, zar__axq)
    if do_resize:
        self.downsize(zbx__deze)
    self.set_dirty(True)


def pop(self):
    context = self._context
    builder = self._builder
    tdex__rzh = context.get_value_type(self._ty.dtype)
    key = cgutils.alloca_once(builder, tdex__rzh)
    payload = self.payload
    with payload._next_entry() as entry:
        builder.store(entry.key, key)
        context.nrt.incref(builder, self._ty.dtype, entry.key)
        self._remove_entry(payload, entry)
    return builder.load(key)


def _resize(self, payload, nentries, errmsg):
    context = self._context
    builder = self._builder
    uytko__yutgz = payload
    dilf__kgpj = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(dilf__kgpj), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (errmsg,))
    payload = self.payload
    with uytko__yutgz._iterate() as sftwf__lrdd:
        entry = sftwf__lrdd.entry
        self._add_key(payload, entry.key, entry.hash, do_resize=False)
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(uytko__yutgz.ptr)


def _replace_payload(self, nentries):
    context = self._context
    builder = self._builder
    with self.payload._iterate() as sftwf__lrdd:
        entry = sftwf__lrdd.entry
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(self.payload.ptr)
    dilf__kgpj = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(dilf__kgpj), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (
            'cannot reallocate set',))


def _allocate_payload(self, nentries, realloc=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    dilf__kgpj = cgutils.alloca_once_value(builder, cgutils.true_bit)
    yiw__cvhjk = context.get_value_type(types.intp)
    clwg__haacd = ir.Constant(yiw__cvhjk, 0)
    zar__axq = ir.Constant(yiw__cvhjk, 1)
    xiwg__zxfx = context.get_data_type(types.SetPayload(self._ty))
    inkw__vib = context.get_abi_sizeof(xiwg__zxfx)
    sicc__ejceb = self._entrysize
    inkw__vib -= sicc__ejceb
    xynan__jxsio, vdd__uavp = cgutils.muladd_with_overflow(builder,
        nentries, ir.Constant(yiw__cvhjk, sicc__ejceb), ir.Constant(
        yiw__cvhjk, inkw__vib))
    with builder.if_then(vdd__uavp, likely=False):
        builder.store(cgutils.false_bit, dilf__kgpj)
    with builder.if_then(builder.load(dilf__kgpj), likely=True):
        if realloc:
            kkxmr__xcz = self._set.meminfo
            qvtrm__etyn = context.nrt.meminfo_varsize_alloc(builder,
                kkxmr__xcz, size=xynan__jxsio)
            lvbcb__eqtx = cgutils.is_null(builder, qvtrm__etyn)
        else:
            sebx__lmzcz = _imp_dtor(context, builder.module, self._ty)
            kkxmr__xcz = context.nrt.meminfo_new_varsize_dtor(builder,
                xynan__jxsio, builder.bitcast(sebx__lmzcz, cgutils.voidptr_t))
            lvbcb__eqtx = cgutils.is_null(builder, kkxmr__xcz)
        with builder.if_else(lvbcb__eqtx, likely=False) as (chjr__hul,
            uqc__opav):
            with chjr__hul:
                builder.store(cgutils.false_bit, dilf__kgpj)
            with uqc__opav:
                if not realloc:
                    self._set.meminfo = kkxmr__xcz
                    self._set.parent = context.get_constant_null(types.pyobject
                        )
                payload = self.payload
                cgutils.memset(builder, payload.ptr, xynan__jxsio, 255)
                payload.used = clwg__haacd
                payload.fill = clwg__haacd
                payload.finger = clwg__haacd
                uuht__ajtdu = builder.sub(nentries, zar__axq)
                payload.mask = uuht__ajtdu
    return builder.load(dilf__kgpj)


def _copy_payload(self, src_payload):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    dilf__kgpj = cgutils.alloca_once_value(builder, cgutils.true_bit)
    yiw__cvhjk = context.get_value_type(types.intp)
    clwg__haacd = ir.Constant(yiw__cvhjk, 0)
    zar__axq = ir.Constant(yiw__cvhjk, 1)
    xiwg__zxfx = context.get_data_type(types.SetPayload(self._ty))
    inkw__vib = context.get_abi_sizeof(xiwg__zxfx)
    sicc__ejceb = self._entrysize
    inkw__vib -= sicc__ejceb
    vbh__zbck = src_payload.mask
    nentries = builder.add(zar__axq, vbh__zbck)
    xynan__jxsio = builder.add(ir.Constant(yiw__cvhjk, inkw__vib), builder.
        mul(ir.Constant(yiw__cvhjk, sicc__ejceb), nentries))
    with builder.if_then(builder.load(dilf__kgpj), likely=True):
        sebx__lmzcz = _imp_dtor(context, builder.module, self._ty)
        kkxmr__xcz = context.nrt.meminfo_new_varsize_dtor(builder,
            xynan__jxsio, builder.bitcast(sebx__lmzcz, cgutils.voidptr_t))
        lvbcb__eqtx = cgutils.is_null(builder, kkxmr__xcz)
        with builder.if_else(lvbcb__eqtx, likely=False) as (chjr__hul,
            uqc__opav):
            with chjr__hul:
                builder.store(cgutils.false_bit, dilf__kgpj)
            with uqc__opav:
                self._set.meminfo = kkxmr__xcz
                payload = self.payload
                payload.used = src_payload.used
                payload.fill = src_payload.fill
                payload.finger = clwg__haacd
                payload.mask = vbh__zbck
                cgutils.raw_memcpy(builder, payload.entries, src_payload.
                    entries, nentries, sicc__ejceb)
                with src_payload._iterate() as sftwf__lrdd:
                    context.nrt.incref(builder, self._ty.dtype, sftwf__lrdd
                        .entry.key)
    return builder.load(dilf__kgpj)


def _imp_dtor(context, module, set_type):
    from llvmlite import ir
    yybnm__jqavp = context.get_value_type(types.voidptr)
    zsnau__plumo = context.get_value_type(types.uintp)
    fnty = ir.FunctionType(ir.VoidType(), [yybnm__jqavp, zsnau__plumo,
        yybnm__jqavp])
    jst__sjr = f'_numba_set_dtor_{set_type}'
    fn = cgutils.get_or_insert_function(module, fnty, name=jst__sjr)
    if fn.is_declaration:
        fn.linkage = 'linkonce_odr'
        builder = ir.IRBuilder(fn.append_basic_block())
        mnzx__vagjr = builder.bitcast(fn.args[0], cgutils.voidptr_t.
            as_pointer())
        payload = numba.cpython.setobj._SetPayload(context, builder,
            set_type, mnzx__vagjr)
        with payload._iterate() as sftwf__lrdd:
            entry = sftwf__lrdd.entry
            context.nrt.decref(builder, set_type.dtype, entry.key)
        builder.ret_void()
    return fn


@lower_builtin(set, types.IterableType)
def set_constructor(context, builder, sig, args):
    set_type = sig.return_type
    tlca__qkmm, = sig.args
    pgd__iyzxa, = args
    gswn__vxj = numba.core.imputils.call_len(context, builder, tlca__qkmm,
        pgd__iyzxa)
    inst = numba.cpython.setobj.SetInstance.allocate(context, builder,
        set_type, gswn__vxj)
    with numba.core.imputils.for_iter(context, builder, tlca__qkmm, pgd__iyzxa
        ) as sftwf__lrdd:
        inst.add(sftwf__lrdd.value)
        context.nrt.decref(builder, set_type.dtype, sftwf__lrdd.value)
    return numba.core.imputils.impl_ret_new_ref(context, builder, set_type,
        inst.value)


@lower_builtin('set.update', types.Set, types.IterableType)
def set_update(context, builder, sig, args):
    inst = numba.cpython.setobj.SetInstance(context, builder, sig.args[0],
        args[0])
    tlca__qkmm = sig.args[1]
    pgd__iyzxa = args[1]
    gswn__vxj = numba.core.imputils.call_len(context, builder, tlca__qkmm,
        pgd__iyzxa)
    if gswn__vxj is not None:
        xos__rneu = builder.add(inst.payload.used, gswn__vxj)
        inst.upsize(xos__rneu)
    with numba.core.imputils.for_iter(context, builder, tlca__qkmm, pgd__iyzxa
        ) as sftwf__lrdd:
        feco__vcws = context.cast(builder, sftwf__lrdd.value, tlca__qkmm.
            dtype, inst.dtype)
        inst.add(feco__vcws)
        context.nrt.decref(builder, tlca__qkmm.dtype, sftwf__lrdd.value)
    if gswn__vxj is not None:
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
    fodwg__sab = {key: value for key, value in self.metadata.items() if (
        'distributed' in key or 'replicated' in key) and key !=
        'distributed_diagnostics'}
    return (libdata, self.fndesc, self.environment, self.signature, self.
        objectmode, self.lifted, typeann, fodwg__sab, self.reload_init,
        tuple(referenced_envs))


@classmethod
def _rebuild(cls, target_context, libdata, fndesc, env, signature,
    objectmode, lifted, typeann, metadata, reload_init, referenced_envs):
    if reload_init:
        for fn in reload_init:
            fn()
    library = target_context.codegen().unserialize_library(libdata)
    egh__fvt = target_context.get_executable(library, fndesc, env)
    dcb__vgzj = cls(target_context=target_context, typing_context=
        target_context.typing_context, library=library, environment=env,
        entry_point=egh__fvt, fndesc=fndesc, type_annotation=typeann,
        signature=signature, objectmode=objectmode, lifted=lifted,
        typing_error=None, call_helper=None, metadata=metadata, reload_init
        =reload_init, referenced_envs=referenced_envs)
    for env in referenced_envs:
        library.codegen.set_env(env.env_name, env)
    return dcb__vgzj


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
        orole__rvk = MPI.COMM_WORLD
        if orole__rvk.Get_rank() == 0:
            kdad__kss = self.get_cache_path()
            os.makedirs(kdad__kss, exist_ok=True)
            tempfile.TemporaryFile(dir=kdad__kss).close()
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
    kmu__zhs = cgutils.create_struct_proxy(charseq.bytes_type)
    stc__xbkj = kmu__zhs(context, builder)
    if isinstance(nbytes, int):
        nbytes = ir.Constant(stc__xbkj.nitems.type, nbytes)
    stc__xbkj.meminfo = context.nrt.meminfo_alloc(builder, nbytes)
    stc__xbkj.nitems = nbytes
    stc__xbkj.itemsize = ir.Constant(stc__xbkj.itemsize.type, 1)
    stc__xbkj.data = context.nrt.meminfo_data(builder, stc__xbkj.meminfo)
    stc__xbkj.parent = cgutils.get_null_value(stc__xbkj.parent.type)
    stc__xbkj.shape = cgutils.pack_array(builder, [stc__xbkj.nitems],
        context.get_value_type(types.intp))
    stc__xbkj.strides = cgutils.pack_array(builder, [ir.Constant(stc__xbkj.
        strides.type.element, 1)], context.get_value_type(types.intp))
    return stc__xbkj


if _check_numba_change:
    lines = inspect.getsource(charseq._make_constant_bytes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b3ed23ad58baff7b935912e3e22f4d8af67423d8fd0e5f1836ba0b3028a6eb18':
        warnings.warn('charseq._make_constant_bytes has changed')
charseq._make_constant_bytes = _make_constant_bytes
