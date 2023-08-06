"""CSR Matrix data type implementation for scipy.sparse.csr_matrix
"""
import operator
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
import bodo
from bodo.utils.typing import BodoError


class CSRMatrixType(types.ArrayCompatible):
    ndim = 2

    def __init__(self, dtype, idx_dtype):
        self.dtype = dtype
        self.idx_dtype = idx_dtype
        super(CSRMatrixType, self).__init__(name=
            f'CSRMatrixType({dtype}, {idx_dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    def copy(self):
        return CSRMatrixType(self.dtype, self.idx_dtype)


@register_model(CSRMatrixType)
class CSRMatrixModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ghgp__jstqu = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, ghgp__jstqu)


make_attribute_wrapper(CSRMatrixType, 'data', 'data')
make_attribute_wrapper(CSRMatrixType, 'indices', 'indices')
make_attribute_wrapper(CSRMatrixType, 'indptr', 'indptr')
make_attribute_wrapper(CSRMatrixType, 'shape', 'shape')


@intrinsic
def init_csr_matrix(typingctx, data_t, indices_t, indptr_t, shape_t=None):
    assert isinstance(data_t, types.Array)
    assert isinstance(indices_t, types.Array) and isinstance(indices_t.
        dtype, types.Integer)
    assert indices_t == indptr_t

    def codegen(context, builder, signature, args):
        hzfhu__pdpw, tgcwu__cjc, dyjni__yyl, hfqfe__xnjwp = args
        bonqe__datog = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        bonqe__datog.data = hzfhu__pdpw
        bonqe__datog.indices = tgcwu__cjc
        bonqe__datog.indptr = dyjni__yyl
        bonqe__datog.shape = hfqfe__xnjwp
        context.nrt.incref(builder, signature.args[0], hzfhu__pdpw)
        context.nrt.incref(builder, signature.args[1], tgcwu__cjc)
        context.nrt.incref(builder, signature.args[2], dyjni__yyl)
        return bonqe__datog._getvalue()
    hvw__dheyv = CSRMatrixType(data_t.dtype, indices_t.dtype)
    plstc__plil = hvw__dheyv(data_t, indices_t, indptr_t, types.UniTuple(
        types.int64, 2))
    return plstc__plil, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    bonqe__datog = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    nupw__ymnr = c.pyapi.object_getattr_string(val, 'data')
    khnvc__klcs = c.pyapi.object_getattr_string(val, 'indices')
    kdrt__hpd = c.pyapi.object_getattr_string(val, 'indptr')
    dgk__hybo = c.pyapi.object_getattr_string(val, 'shape')
    bonqe__datog.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1,
        'C'), nupw__ymnr).value
    bonqe__datog.indices = c.pyapi.to_native_value(types.Array(typ.
        idx_dtype, 1, 'C'), khnvc__klcs).value
    bonqe__datog.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype,
        1, 'C'), kdrt__hpd).value
    bonqe__datog.shape = c.pyapi.to_native_value(types.UniTuple(types.int64,
        2), dgk__hybo).value
    c.pyapi.decref(nupw__ymnr)
    c.pyapi.decref(khnvc__klcs)
    c.pyapi.decref(kdrt__hpd)
    c.pyapi.decref(dgk__hybo)
    pbtq__nby = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(bonqe__datog._getvalue(), is_error=pbtq__nby)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    njq__nxca = c.context.insert_const_string(c.builder.module, 'scipy.sparse')
    gso__neo = c.pyapi.import_module_noblock(njq__nxca)
    bonqe__datog = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        bonqe__datog.data)
    nupw__ymnr = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        bonqe__datog.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        bonqe__datog.indices)
    khnvc__klcs = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1,
        'C'), bonqe__datog.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        bonqe__datog.indptr)
    kdrt__hpd = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'
        ), bonqe__datog.indptr, c.env_manager)
    dgk__hybo = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        bonqe__datog.shape, c.env_manager)
    qyfc__ucjiw = c.pyapi.tuple_pack([nupw__ymnr, khnvc__klcs, kdrt__hpd])
    sdmv__zmphs = c.pyapi.call_method(gso__neo, 'csr_matrix', (qyfc__ucjiw,
        dgk__hybo))
    c.pyapi.decref(qyfc__ucjiw)
    c.pyapi.decref(nupw__ymnr)
    c.pyapi.decref(khnvc__klcs)
    c.pyapi.decref(kdrt__hpd)
    c.pyapi.decref(dgk__hybo)
    c.pyapi.decref(gso__neo)
    c.context.nrt.decref(c.builder, typ, val)
    return sdmv__zmphs


@overload(len, no_unliteral=True)
def overload_csr_matrix_len(A):
    if isinstance(A, CSRMatrixType):
        return lambda A: A.shape[0]


@overload_attribute(CSRMatrixType, 'ndim')
def overload_csr_matrix_ndim(A):
    return lambda A: 2


@overload_method(CSRMatrixType, 'copy', no_unliteral=True)
def overload_csr_matrix_copy(A):

    def copy_impl(A):
        return init_csr_matrix(A.data.copy(), A.indices.copy(), A.indptr.
            copy(), A.shape)
    return copy_impl


@overload(operator.getitem, no_unliteral=True)
def csr_matrix_getitem(A, idx):
    if not isinstance(A, CSRMatrixType):
        return
    acou__edvla = A.dtype
    got__jrvcj = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            yepxu__oqyf, siil__htemc = A.shape
            iwmz__yomg = numba.cpython.unicode._normalize_slice(idx[0],
                yepxu__oqyf)
            wozzr__exq = numba.cpython.unicode._normalize_slice(idx[1],
                siil__htemc)
            if iwmz__yomg.step != 1 or wozzr__exq.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            urve__tyuno = iwmz__yomg.start
            cmgst__hlsj = iwmz__yomg.stop
            ciz__kztar = wozzr__exq.start
            lok__plp = wozzr__exq.stop
            ifzj__yzys = A.indptr
            ixz__gnb = A.indices
            upvk__atrad = A.data
            nle__ezxxw = cmgst__hlsj - urve__tyuno
            msk__qvese = lok__plp - ciz__kztar
            kpgr__nyuk = 0
            boh__ssted = 0
            for dpsa__qxa in range(nle__ezxxw):
                juby__ibhn = ifzj__yzys[urve__tyuno + dpsa__qxa]
                pjx__fbuvx = ifzj__yzys[urve__tyuno + dpsa__qxa + 1]
                for rbdnm__cdi in range(juby__ibhn, pjx__fbuvx):
                    if ixz__gnb[rbdnm__cdi] >= ciz__kztar and ixz__gnb[
                        rbdnm__cdi] < lok__plp:
                        kpgr__nyuk += 1
            pufx__znz = np.empty(nle__ezxxw + 1, got__jrvcj)
            kdmb__zrswy = np.empty(kpgr__nyuk, got__jrvcj)
            urizp__cmowv = np.empty(kpgr__nyuk, acou__edvla)
            pufx__znz[0] = 0
            for dpsa__qxa in range(nle__ezxxw):
                juby__ibhn = ifzj__yzys[urve__tyuno + dpsa__qxa]
                pjx__fbuvx = ifzj__yzys[urve__tyuno + dpsa__qxa + 1]
                for rbdnm__cdi in range(juby__ibhn, pjx__fbuvx):
                    if ixz__gnb[rbdnm__cdi] >= ciz__kztar and ixz__gnb[
                        rbdnm__cdi] < lok__plp:
                        kdmb__zrswy[boh__ssted] = ixz__gnb[rbdnm__cdi
                            ] - ciz__kztar
                        urizp__cmowv[boh__ssted] = upvk__atrad[rbdnm__cdi]
                        boh__ssted += 1
                pufx__znz[dpsa__qxa + 1] = boh__ssted
            return init_csr_matrix(urizp__cmowv, kdmb__zrswy, pufx__znz, (
                nle__ezxxw, msk__qvese))
        return impl
    elif isinstance(idx, types.Array
        ) and idx.ndim == 1 and idx.dtype == got__jrvcj:

        def impl(A, idx):
            yepxu__oqyf, siil__htemc = A.shape
            ifzj__yzys = A.indptr
            ixz__gnb = A.indices
            upvk__atrad = A.data
            nle__ezxxw = len(idx)
            kpgr__nyuk = 0
            boh__ssted = 0
            for dpsa__qxa in range(nle__ezxxw):
                klhyy__tsunk = idx[dpsa__qxa]
                juby__ibhn = ifzj__yzys[klhyy__tsunk]
                pjx__fbuvx = ifzj__yzys[klhyy__tsunk + 1]
                kpgr__nyuk += pjx__fbuvx - juby__ibhn
            pufx__znz = np.empty(nle__ezxxw + 1, got__jrvcj)
            kdmb__zrswy = np.empty(kpgr__nyuk, got__jrvcj)
            urizp__cmowv = np.empty(kpgr__nyuk, acou__edvla)
            pufx__znz[0] = 0
            for dpsa__qxa in range(nle__ezxxw):
                klhyy__tsunk = idx[dpsa__qxa]
                juby__ibhn = ifzj__yzys[klhyy__tsunk]
                pjx__fbuvx = ifzj__yzys[klhyy__tsunk + 1]
                kdmb__zrswy[boh__ssted:boh__ssted + pjx__fbuvx - juby__ibhn
                    ] = ixz__gnb[juby__ibhn:pjx__fbuvx]
                urizp__cmowv[boh__ssted:boh__ssted + pjx__fbuvx - juby__ibhn
                    ] = upvk__atrad[juby__ibhn:pjx__fbuvx]
                boh__ssted += pjx__fbuvx - juby__ibhn
                pufx__znz[dpsa__qxa + 1] = boh__ssted
            tkn__ogjb = init_csr_matrix(urizp__cmowv, kdmb__zrswy,
                pufx__znz, (nle__ezxxw, siil__htemc))
            return tkn__ogjb
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
