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
        uft__xyr = 'bodo' if distributed else 'bodo_seq'
        uft__xyr = uft__xyr + '_inline' if inline_calls_pass else uft__xyr
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state, uft__xyr)
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
    for rtj__fac, (czlzm__agv, ejyc__mwbz) in enumerate(pm.passes):
        if czlzm__agv == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(rtj__fac, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for rtj__fac, (czlzm__agv, ejyc__mwbz) in enumerate(pm.passes):
        if czlzm__agv == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[rtj__fac] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for rtj__fac, (czlzm__agv, ejyc__mwbz) in enumerate(pm.passes):
        if czlzm__agv == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(rtj__fac)
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
    lxm__fuw = guard(get_definition, func_ir, rhs.func)
    if isinstance(lxm__fuw, (ir.Global, ir.FreeVar, ir.Const)):
        fwx__ajyv = lxm__fuw.value
    else:
        gboe__kxsbr = guard(find_callname, func_ir, rhs)
        if not (gboe__kxsbr and isinstance(gboe__kxsbr[0], str) and
            isinstance(gboe__kxsbr[1], str)):
            return
        func_name, func_mod = gboe__kxsbr
        try:
            import importlib
            iojlt__nrtjj = importlib.import_module(func_mod)
            fwx__ajyv = getattr(iojlt__nrtjj, func_name)
        except:
            return
    if isinstance(fwx__ajyv, CPUDispatcher) and issubclass(fwx__ajyv.
        _compiler.pipeline_class, BodoCompiler
        ) and fwx__ajyv._compiler.pipeline_class != BodoCompilerUDF:
        fwx__ajyv._compiler.pipeline_class = BodoCompilerUDF
        fwx__ajyv.recompile()


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for kwal__tfrch in block.body:
                if is_call_assign(kwal__tfrch):
                    _convert_bodo_dispatcher_to_udf(kwal__tfrch.value,
                        state.func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        tga__scaxl = UntypedPass(state.func_ir, state.typingctx, state.args,
            state.locals, state.metadata, state.flags)
        tga__scaxl.run()
        return True


def _update_definitions(func_ir, node_list):
    nsr__buf = ir.Loc('', 0)
    xbkpg__pkta = ir.Block(ir.Scope(None, nsr__buf), nsr__buf)
    xbkpg__pkta.body = node_list
    build_definitions({(0): xbkpg__pkta}, func_ir._definitions)


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
        lrzl__cqyeu = 'overload_series_' + rhs.attr
        mue__yedn = getattr(bodo.hiframes.series_impl, lrzl__cqyeu)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        lrzl__cqyeu = 'overload_dataframe_' + rhs.attr
        mue__yedn = getattr(bodo.hiframes.dataframe_impl, lrzl__cqyeu)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    gxyh__kna = mue__yedn(rhs_type)
    xcnv__lvz = TypingInfo(typingctx, targetctx, typemap, calltypes, stmt.loc)
    zxu__oot = compile_func_single_block(gxyh__kna, (rhs.value,), stmt.
        target, xcnv__lvz)
    _update_definitions(func_ir, zxu__oot)
    new_body += zxu__oot
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
        sqqf__mkgc = tuple(typemap[rgvw__kcmr.name] for rgvw__kcmr in rhs.args)
        gzpjn__zaosa = {uft__xyr: typemap[rgvw__kcmr.name] for uft__xyr,
            rgvw__kcmr in dict(rhs.kws).items()}
        gxyh__kna = getattr(bodo.hiframes.series_impl, 'overload_series_' +
            func_name)(*sqqf__mkgc, **gzpjn__zaosa)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        sqqf__mkgc = tuple(typemap[rgvw__kcmr.name] for rgvw__kcmr in rhs.args)
        gzpjn__zaosa = {uft__xyr: typemap[rgvw__kcmr.name] for uft__xyr,
            rgvw__kcmr in dict(rhs.kws).items()}
        gxyh__kna = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*sqqf__mkgc, **gzpjn__zaosa)
    else:
        return False
    ljuy__mfg = replace_func(pass_info, gxyh__kna, rhs.args, pysig=numba.
        core.utils.pysignature(gxyh__kna), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    vxmuv__amwwu, ejyc__mwbz = inline_closure_call(func_ir, ljuy__mfg.glbls,
        block, len(new_body), ljuy__mfg.func, typingctx=typingctx,
        targetctx=targetctx, arg_typs=ljuy__mfg.arg_types, typemap=typemap,
        calltypes=calltypes, work_list=work_list)
    for diqrk__itqbu in vxmuv__amwwu.values():
        diqrk__itqbu.loc = rhs.loc
        update_locs(diqrk__itqbu.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    afda__jacm = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = afda__jacm(func_ir, typemap)
    qshkh__lejk = func_ir.blocks
    work_list = list((hpr__bxol, qshkh__lejk[hpr__bxol]) for hpr__bxol in
        reversed(qshkh__lejk.keys()))
    while work_list:
        bziff__wpa, block = work_list.pop()
        new_body = []
        jge__slpa = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                gboe__kxsbr = guard(find_callname, func_ir, rhs, typemap)
                if gboe__kxsbr is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = gboe__kxsbr
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    jge__slpa = True
                    break
            new_body.append(stmt)
        if not jge__slpa:
            qshkh__lejk[bziff__wpa].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        bots__ompp = DistributedPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.return_type,
            state.metadata, state.flags)
        state.return_type = bots__ompp.run()
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        etbt__ixr = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.locals)
        mefw__sap = etbt__ixr.run()
        pje__fllbv = mefw__sap
        if pje__fllbv:
            pje__fllbv = etbt__ixr.run()
        if pje__fllbv:
            etbt__ixr.run()
        return mefw__sap


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        ktma__gio = 0
        fcuk__vri = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            ktma__gio = int(os.environ[fcuk__vri])
        except:
            pass
        if ktma__gio > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(ktma__gio, state
                .metadata)
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
        xcnv__lvz = TypingInfo(state.typingctx, state.targetctx, state.
            typemap, state.calltypes, state.func_ir.loc)
        remove_dead_table_columns(state.func_ir, state.typemap, xcnv__lvz)
        for block in state.func_ir.blocks.values():
            new_body = []
            for kwal__tfrch in block.body:
                if type(kwal__tfrch) in distributed_run_extensions:
                    fro__mty = distributed_run_extensions[type(kwal__tfrch)]
                    qxuet__ntb = fro__mty(kwal__tfrch, None, state.typemap,
                        state.calltypes, state.typingctx, state.targetctx)
                    new_body += qxuet__ntb
                elif is_call_assign(kwal__tfrch):
                    rhs = kwal__tfrch.value
                    gboe__kxsbr = guard(find_callname, state.func_ir, rhs)
                    if gboe__kxsbr == ('gatherv', 'bodo') or gboe__kxsbr == (
                        'allgatherv', 'bodo'):
                        casei__ruxo = state.typemap[kwal__tfrch.target.name]
                        ohxx__gqrr = state.typemap[rhs.args[0].name]
                        if isinstance(ohxx__gqrr, types.Array) and isinstance(
                            casei__ruxo, types.Array):
                            eyk__teh = ohxx__gqrr.copy(readonly=False)
                            kdjhv__ysvpv = casei__ruxo.copy(readonly=False)
                            if eyk__teh == kdjhv__ysvpv:
                                new_body += compile_func_single_block(eval(
                                    'lambda data: data.copy()'), (rhs.args[
                                    0],), kwal__tfrch.target, xcnv__lvz)
                                continue
                        if (casei__ruxo != ohxx__gqrr and 
                            to_str_arr_if_dict_array(casei__ruxo) ==
                            to_str_arr_if_dict_array(ohxx__gqrr)):
                            new_body += compile_func_single_block(eval(
                                'lambda data: decode_if_dict_array(data)'),
                                (rhs.args[0],), kwal__tfrch.target,
                                xcnv__lvz, extra_globals={
                                'decode_if_dict_array': decode_if_dict_array})
                            continue
                        else:
                            kwal__tfrch.value = rhs.args[0]
                    new_body.append(kwal__tfrch)
                else:
                    new_body.append(kwal__tfrch)
            block.body = new_body
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoTableColumnDelPass(AnalysisPass):
    _name = 'bodo_table_column_del_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        ugcdq__dqqeq = TableColumnDelPass(state.func_ir, state.typingctx,
            state.targetctx, state.typemap, state.calltypes)
        return ugcdq__dqqeq.run()


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    axzzu__hoex = set()
    while work_list:
        bziff__wpa, block = work_list.pop()
        axzzu__hoex.add(bziff__wpa)
        for i, xxvf__brv in enumerate(block.body):
            if isinstance(xxvf__brv, ir.Assign):
                edrg__pcqde = xxvf__brv.value
                if isinstance(edrg__pcqde, ir.Expr
                    ) and edrg__pcqde.op == 'call':
                    lxm__fuw = guard(get_definition, func_ir, edrg__pcqde.func)
                    if isinstance(lxm__fuw, (ir.Global, ir.FreeVar)
                        ) and isinstance(lxm__fuw.value, CPUDispatcher
                        ) and issubclass(lxm__fuw.value._compiler.
                        pipeline_class, BodoCompiler):
                        bqsp__ylcrd = lxm__fuw.value.py_func
                        arg_types = None
                        if typingctx:
                            hopt__qxh = dict(edrg__pcqde.kws)
                            mebz__edypd = tuple(typemap[rgvw__kcmr.name] for
                                rgvw__kcmr in edrg__pcqde.args)
                            vhk__dmnnq = {bij__gkhps: typemap[rgvw__kcmr.
                                name] for bij__gkhps, rgvw__kcmr in
                                hopt__qxh.items()}
                            ejyc__mwbz, arg_types = (lxm__fuw.value.
                                fold_argument_types(mebz__edypd, vhk__dmnnq))
                        ejyc__mwbz, momdo__nhgv = inline_closure_call(func_ir,
                            bqsp__ylcrd.__globals__, block, i, bqsp__ylcrd,
                            typingctx=typingctx, targetctx=targetctx,
                            arg_typs=arg_types, typemap=typemap, calltypes=
                            calltypes, work_list=work_list)
                        _locals.update((momdo__nhgv[bij__gkhps].name,
                            rgvw__kcmr) for bij__gkhps, rgvw__kcmr in
                            lxm__fuw.value.locals.items() if bij__gkhps in
                            momdo__nhgv)
                        break
    return axzzu__hoex


def udf_jit(signature_or_function=None, **options):
    kmx__skkld = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    return numba.njit(signature_or_function, parallel=kmx__skkld,
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
    for rtj__fac, (czlzm__agv, ejyc__mwbz) in enumerate(pm.passes):
        if czlzm__agv == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:rtj__fac + 1]
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
    ztais__manyp = None
    yurqu__dwu = None
    _locals = {}
    qse__hvyu = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(qse__hvyu, arg_types,
        kw_types)
    zxoh__moypn = numba.core.compiler.Flags()
    ckqvs__dwfz = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    brfxr__vrxsv = {'nopython': True, 'boundscheck': False, 'parallel':
        ckqvs__dwfz}
    numba.core.registry.cpu_target.options.parse_as_flags(zxoh__moypn,
        brfxr__vrxsv)
    bmqjc__yydk = TyperCompiler(typingctx, targetctx, ztais__manyp, args,
        yurqu__dwu, zxoh__moypn, _locals)
    return bmqjc__yydk.compile_extra(func)
