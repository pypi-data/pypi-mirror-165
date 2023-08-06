"""
Defines Bodo's compiler pipeline.
"""
import os
import warnings
from collections import namedtuple
import numba
from numba.core import ir, ir_utils, types
from numba.core.compiler import DefaultPassBuilder
from numba.core.compiler_machinery import AnalysisPass, FunctionPass, register_pass
from numba.core.errors import NumbaExperimentalFeatureWarning, NumbaPendingDeprecationWarning
from numba.core.inline_closurecall import inline_closure_call
from numba.core.ir_utils import build_definitions, find_callname, get_definition, guard
from numba.core.registry import CPUDispatcher
from numba.core.typed_passes import DumpParforDiagnostics, InlineOverloads, IRLegalization, NopythonTypeInference, ParforPass, PreParforPass
from numba.core.untyped_passes import MakeFunctionToJitFunction, ReconstructSSA, WithLifting
import bodo
import bodo.hiframes.dataframe_indexing
import bodo.hiframes.datetime_datetime_ext
import bodo.hiframes.datetime_timedelta_ext
import bodo.io
import bodo.libs
import bodo.libs.array_kernels
import bodo.libs.int_arr_ext
import bodo.libs.re_ext
import bodo.libs.spark_extra
import bodo.transforms
import bodo.transforms.series_pass
import bodo.transforms.untyped_pass
import bodo.utils
import bodo.utils.table_utils
import bodo.utils.typing
from bodo.transforms.series_pass import SeriesPass
from bodo.transforms.table_column_del_pass import TableColumnDelPass
from bodo.transforms.typing_pass import BodoTypeInference
from bodo.transforms.untyped_pass import UntypedPass
from bodo.utils.utils import is_assign, is_call_assign, is_expr
warnings.simplefilter('ignore', category=NumbaExperimentalFeatureWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)
inline_all_calls = False


class BodoCompiler(numba.core.compiler.CompilerBase):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=True,
            inline_calls_pass=inline_all_calls)

    def _create_bodo_pipeline(self, distributed=True, inline_calls_pass=
        False, udf_pipeline=False):
        drsik__uwulf = 'bodo' if distributed else 'bodo_seq'
        drsik__uwulf = (drsik__uwulf + '_inline' if inline_calls_pass else
            drsik__uwulf)
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state,
            drsik__uwulf)
        if inline_calls_pass:
            pm.add_pass_after(InlinePass, WithLifting)
        if udf_pipeline:
            pm.add_pass_after(ConvertCallsUDFPass, WithLifting)
        add_pass_before(pm, BodoUntypedPass, ReconstructSSA)
        replace_pass(pm, BodoTypeInference, NopythonTypeInference)
        remove_pass(pm, MakeFunctionToJitFunction)
        add_pass_before(pm, BodoSeriesPass, PreParforPass)
        if distributed:
            pm.add_pass_after(BodoDistributedPass, ParforPass)
        else:
            pm.add_pass_after(LowerParforSeq, ParforPass)
            pm.add_pass_after(LowerBodoIRExtSeq, LowerParforSeq)
        add_pass_before(pm, BodoTableColumnDelPass, IRLegalization)
        pm.add_pass_after(BodoDumpDistDiagnosticsPass, DumpParforDiagnostics)
        pm.finalize()
        return [pm]


def add_pass_before(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for epx__zqtv, (obv__xpeq, kcs__ejodv) in enumerate(pm.passes):
        if obv__xpeq == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(epx__zqtv, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for epx__zqtv, (obv__xpeq, kcs__ejodv) in enumerate(pm.passes):
        if obv__xpeq == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[epx__zqtv] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for epx__zqtv, (obv__xpeq, kcs__ejodv) in enumerate(pm.passes):
        if obv__xpeq == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(epx__zqtv)
    pm._finalized = False


@register_pass(mutates_CFG=True, analysis_only=False)
class InlinePass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        inline_calls(state.func_ir, state.locals)
        state.func_ir.blocks = ir_utils.simplify_CFG(state.func_ir.blocks)
        return True


def _convert_bodo_dispatcher_to_udf(rhs, func_ir):
    jhlh__oue = guard(get_definition, func_ir, rhs.func)
    if isinstance(jhlh__oue, (ir.Global, ir.FreeVar, ir.Const)):
        abiaz__fah = jhlh__oue.value
    else:
        zru__ffi = guard(find_callname, func_ir, rhs)
        if not (zru__ffi and isinstance(zru__ffi[0], str) and isinstance(
            zru__ffi[1], str)):
            return
        func_name, func_mod = zru__ffi
        try:
            import importlib
            pgtqj__pfe = importlib.import_module(func_mod)
            abiaz__fah = getattr(pgtqj__pfe, func_name)
        except:
            return
    if isinstance(abiaz__fah, CPUDispatcher) and issubclass(abiaz__fah.
        _compiler.pipeline_class, BodoCompiler
        ) and abiaz__fah._compiler.pipeline_class != BodoCompilerUDF:
        abiaz__fah._compiler.pipeline_class = BodoCompilerUDF
        abiaz__fah.recompile()


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for kufrs__nafrg in block.body:
                if is_call_assign(kufrs__nafrg):
                    _convert_bodo_dispatcher_to_udf(kufrs__nafrg.value,
                        state.func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        cppk__dit = UntypedPass(state.func_ir, state.typingctx, state.args,
            state.locals, state.metadata, state.flags)
        cppk__dit.run()
        return True


def _update_definitions(func_ir, node_list):
    ajg__sav = ir.Loc('', 0)
    wpa__zcr = ir.Block(ir.Scope(None, ajg__sav), ajg__sav)
    wpa__zcr.body = node_list
    build_definitions({(0): wpa__zcr}, func_ir._definitions)


_series_inline_attrs = {'values', 'shape', 'size', 'empty', 'name', 'index',
    'dtype'}
_series_no_inline_methods = {'to_list', 'tolist', 'rolling', 'to_csv',
    'count', 'fillna', 'to_dict', 'map', 'apply', 'pipe', 'combine',
    'bfill', 'ffill', 'pad', 'backfill', 'mask', 'where'}
_series_method_alias = {'isnull': 'isna', 'product': 'prod', 'kurtosis':
    'kurt', 'is_monotonic': 'is_monotonic_increasing', 'notnull': 'notna'}
_dataframe_no_inline_methods = {'apply', 'itertuples', 'pipe', 'to_parquet',
    'to_sql', 'to_csv', 'to_json', 'assign', 'to_string', 'query',
    'rolling', 'mask', 'where'}
TypingInfo = namedtuple('TypingInfo', ['typingctx', 'targetctx', 'typemap',
    'calltypes', 'curr_loc'])


def _inline_bodo_getattr(stmt, rhs, rhs_type, new_body, func_ir, typingctx,
    targetctx, typemap, calltypes):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.utils.transform import compile_func_single_block
    if isinstance(rhs_type, SeriesType) and rhs.attr in _series_inline_attrs:
        ejkz__xbg = 'overload_series_' + rhs.attr
        kqwkk__fggz = getattr(bodo.hiframes.series_impl, ejkz__xbg)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        ejkz__xbg = 'overload_dataframe_' + rhs.attr
        kqwkk__fggz = getattr(bodo.hiframes.dataframe_impl, ejkz__xbg)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    wabd__dgktl = kqwkk__fggz(rhs_type)
    rvk__ygu = TypingInfo(typingctx, targetctx, typemap, calltypes, stmt.loc)
    hmt__ymvvb = compile_func_single_block(wabd__dgktl, (rhs.value,), stmt.
        target, rvk__ygu)
    _update_definitions(func_ir, hmt__ymvvb)
    new_body += hmt__ymvvb
    return True


def _inline_bodo_call(rhs, i, func_mod, func_name, pass_info, new_body,
    block, typingctx, targetctx, calltypes, work_list):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.utils.transform import replace_func, update_locs
    func_ir = pass_info.func_ir
    typemap = pass_info.typemap
    if isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        SeriesType) and func_name not in _series_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        if (func_name in bodo.hiframes.series_impl.explicit_binop_funcs or 
            func_name.startswith('r') and func_name[1:] in bodo.hiframes.
            series_impl.explicit_binop_funcs):
            return False
        rhs.args.insert(0, func_mod)
        srpi__jucg = tuple(typemap[wot__pbjan.name] for wot__pbjan in rhs.args)
        ygrp__qlxw = {drsik__uwulf: typemap[wot__pbjan.name] for 
            drsik__uwulf, wot__pbjan in dict(rhs.kws).items()}
        wabd__dgktl = getattr(bodo.hiframes.series_impl, 'overload_series_' +
            func_name)(*srpi__jucg, **ygrp__qlxw)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        srpi__jucg = tuple(typemap[wot__pbjan.name] for wot__pbjan in rhs.args)
        ygrp__qlxw = {drsik__uwulf: typemap[wot__pbjan.name] for 
            drsik__uwulf, wot__pbjan in dict(rhs.kws).items()}
        wabd__dgktl = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*srpi__jucg, **ygrp__qlxw)
    else:
        return False
    jaynt__afoxv = replace_func(pass_info, wabd__dgktl, rhs.args, pysig=
        numba.core.utils.pysignature(wabd__dgktl), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    cmj__tdhi, kcs__ejodv = inline_closure_call(func_ir, jaynt__afoxv.glbls,
        block, len(new_body), jaynt__afoxv.func, typingctx=typingctx,
        targetctx=targetctx, arg_typs=jaynt__afoxv.arg_types, typemap=
        typemap, calltypes=calltypes, work_list=work_list)
    for gkc__gexev in cmj__tdhi.values():
        gkc__gexev.loc = rhs.loc
        update_locs(gkc__gexev.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    cnlw__nftcb = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = cnlw__nftcb(func_ir, typemap)
    hhhed__fizsz = func_ir.blocks
    work_list = list((kima__mau, hhhed__fizsz[kima__mau]) for kima__mau in
        reversed(hhhed__fizsz.keys()))
    while work_list:
        kosas__upxu, block = work_list.pop()
        new_body = []
        oqxt__mxe = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                zru__ffi = guard(find_callname, func_ir, rhs, typemap)
                if zru__ffi is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = zru__ffi
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    oqxt__mxe = True
                    break
            new_body.append(stmt)
        if not oqxt__mxe:
            hhhed__fizsz[kosas__upxu].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        jdex__wef = DistributedPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.return_type,
            state.metadata, state.flags)
        state.return_type = jdex__wef.run()
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        zlnr__vlayz = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.locals)
        hdfyw__qij = zlnr__vlayz.run()
        ghs__ffdv = hdfyw__qij
        if ghs__ffdv:
            ghs__ffdv = zlnr__vlayz.run()
        if ghs__ffdv:
            zlnr__vlayz.run()
        return hdfyw__qij


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        gcure__qskr = 0
        zunfe__gfyd = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            gcure__qskr = int(os.environ[zunfe__gfyd])
        except:
            pass
        if gcure__qskr > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(gcure__qskr,
                state.metadata)
        return True


class BodoCompilerSeq(BodoCompiler):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=False,
            inline_calls_pass=inline_all_calls)


class BodoCompilerUDF(BodoCompiler):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=False, udf_pipeline=True)


@register_pass(mutates_CFG=False, analysis_only=True)
class LowerParforSeq(FunctionPass):
    _name = 'bodo_lower_parfor_seq_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        bodo.transforms.distributed_pass.lower_parfor_sequential(state.
            typingctx, state.func_ir, state.typemap, state.calltypes, state
            .metadata)
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class LowerBodoIRExtSeq(FunctionPass):
    _name = 'bodo_lower_ir_ext_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        from bodo.transforms.distributed_pass import distributed_run_extensions
        from bodo.transforms.table_column_del_pass import remove_dead_table_columns
        from bodo.utils.transform import compile_func_single_block
        from bodo.utils.typing import decode_if_dict_array, to_str_arr_if_dict_array
        state.func_ir._definitions = build_definitions(state.func_ir.blocks)
        rvk__ygu = TypingInfo(state.typingctx, state.targetctx, state.
            typemap, state.calltypes, state.func_ir.loc)
        remove_dead_table_columns(state.func_ir, state.typemap, rvk__ygu)
        for block in state.func_ir.blocks.values():
            new_body = []
            for kufrs__nafrg in block.body:
                if type(kufrs__nafrg) in distributed_run_extensions:
                    dnqpy__orqji = distributed_run_extensions[type(
                        kufrs__nafrg)]
                    zzz__trcds = dnqpy__orqji(kufrs__nafrg, None, state.
                        typemap, state.calltypes, state.typingctx, state.
                        targetctx)
                    new_body += zzz__trcds
                elif is_call_assign(kufrs__nafrg):
                    rhs = kufrs__nafrg.value
                    zru__ffi = guard(find_callname, state.func_ir, rhs)
                    if zru__ffi == ('gatherv', 'bodo') or zru__ffi == (
                        'allgatherv', 'bodo'):
                        nzrhm__dmlf = state.typemap[kufrs__nafrg.target.name]
                        onym__sie = state.typemap[rhs.args[0].name]
                        if isinstance(onym__sie, types.Array) and isinstance(
                            nzrhm__dmlf, types.Array):
                            clve__hfho = onym__sie.copy(readonly=False)
                            hzw__bbx = nzrhm__dmlf.copy(readonly=False)
                            if clve__hfho == hzw__bbx:
                                new_body += compile_func_single_block(eval(
                                    'lambda data: data.copy()'), (rhs.args[
                                    0],), kufrs__nafrg.target, rvk__ygu)
                                continue
                        if (nzrhm__dmlf != onym__sie and 
                            to_str_arr_if_dict_array(nzrhm__dmlf) ==
                            to_str_arr_if_dict_array(onym__sie)):
                            new_body += compile_func_single_block(eval(
                                'lambda data: decode_if_dict_array(data)'),
                                (rhs.args[0],), kufrs__nafrg.target,
                                rvk__ygu, extra_globals={
                                'decode_if_dict_array': decode_if_dict_array})
                            continue
                        else:
                            kufrs__nafrg.value = rhs.args[0]
                    new_body.append(kufrs__nafrg)
                else:
                    new_body.append(kufrs__nafrg)
            block.body = new_body
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoTableColumnDelPass(AnalysisPass):
    _name = 'bodo_table_column_del_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        uawzt__ltsqe = TableColumnDelPass(state.func_ir, state.typingctx,
            state.targetctx, state.typemap, state.calltypes)
        return uawzt__ltsqe.run()


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    lqy__wpl = set()
    while work_list:
        kosas__upxu, block = work_list.pop()
        lqy__wpl.add(kosas__upxu)
        for i, xrrlb__xwgps in enumerate(block.body):
            if isinstance(xrrlb__xwgps, ir.Assign):
                zehw__yyhty = xrrlb__xwgps.value
                if isinstance(zehw__yyhty, ir.Expr
                    ) and zehw__yyhty.op == 'call':
                    jhlh__oue = guard(get_definition, func_ir, zehw__yyhty.func
                        )
                    if isinstance(jhlh__oue, (ir.Global, ir.FreeVar)
                        ) and isinstance(jhlh__oue.value, CPUDispatcher
                        ) and issubclass(jhlh__oue.value._compiler.
                        pipeline_class, BodoCompiler):
                        ukmzi__bjh = jhlh__oue.value.py_func
                        arg_types = None
                        if typingctx:
                            qzqh__fdbxx = dict(zehw__yyhty.kws)
                            tuha__vfpx = tuple(typemap[wot__pbjan.name] for
                                wot__pbjan in zehw__yyhty.args)
                            oece__snk = {lvvt__vlz: typemap[wot__pbjan.name
                                ] for lvvt__vlz, wot__pbjan in qzqh__fdbxx.
                                items()}
                            kcs__ejodv, arg_types = (jhlh__oue.value.
                                fold_argument_types(tuha__vfpx, oece__snk))
                        kcs__ejodv, lwtqc__gqum = inline_closure_call(func_ir,
                            ukmzi__bjh.__globals__, block, i, ukmzi__bjh,
                            typingctx=typingctx, targetctx=targetctx,
                            arg_typs=arg_types, typemap=typemap, calltypes=
                            calltypes, work_list=work_list)
                        _locals.update((lwtqc__gqum[lvvt__vlz].name,
                            wot__pbjan) for lvvt__vlz, wot__pbjan in
                            jhlh__oue.value.locals.items() if lvvt__vlz in
                            lwtqc__gqum)
                        break
    return lqy__wpl


def udf_jit(signature_or_function=None, **options):
    nrr__qik = {'comprehension': True, 'setitem': False, 'inplace_binop': 
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    return numba.njit(signature_or_function, parallel=nrr__qik,
        pipeline_class=bodo.compiler.BodoCompilerUDF, **options)


def is_udf_call(func_type):
    return isinstance(func_type, numba.core.types.Dispatcher
        ) and func_type.dispatcher._compiler.pipeline_class == BodoCompilerUDF


def is_user_dispatcher(func_type):
    return isinstance(func_type, numba.core.types.functions.ObjModeDispatcher
        ) or isinstance(func_type, numba.core.types.Dispatcher) and issubclass(
        func_type.dispatcher._compiler.pipeline_class, BodoCompiler)


@register_pass(mutates_CFG=False, analysis_only=True)
class DummyCR(FunctionPass):
    _name = 'bodo_dummy_cr'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        state.cr = (state.func_ir, state.typemap, state.calltypes, state.
            return_type)
        return True


def remove_passes_after(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for epx__zqtv, (obv__xpeq, kcs__ejodv) in enumerate(pm.passes):
        if obv__xpeq == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:epx__zqtv + 1]
    pm._finalized = False


class TyperCompiler(BodoCompiler):

    def define_pipelines(self):
        [pm] = self._create_bodo_pipeline()
        remove_passes_after(pm, InlineOverloads)
        pm.add_pass_after(DummyCR, InlineOverloads)
        pm.finalize()
        return [pm]


def get_func_type_info(func, arg_types, kw_types):
    typingctx = numba.core.registry.cpu_target.typing_context
    targetctx = numba.core.registry.cpu_target.target_context
    lxr__lynh = None
    bajg__qhwvv = None
    _locals = {}
    fesrt__pphaf = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(fesrt__pphaf, arg_types,
        kw_types)
    vvz__xwwjc = numba.core.compiler.Flags()
    ixmom__uvdv = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    xra__gwfx = {'nopython': True, 'boundscheck': False, 'parallel':
        ixmom__uvdv}
    numba.core.registry.cpu_target.options.parse_as_flags(vvz__xwwjc, xra__gwfx
        )
    sozqy__zgf = TyperCompiler(typingctx, targetctx, lxr__lynh, args,
        bajg__qhwvv, vvz__xwwjc, _locals)
    return sozqy__zgf.compile_extra(func)
