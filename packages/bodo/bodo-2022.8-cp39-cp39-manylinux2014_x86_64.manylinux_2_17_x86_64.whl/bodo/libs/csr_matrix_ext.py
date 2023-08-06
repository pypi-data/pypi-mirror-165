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
        rsh__rbo = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, rsh__rbo)


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
        zarl__mveql, zvgfd__psikv, rtlmr__yfv, dyx__afom = args
        xjw__dqn = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        xjw__dqn.data = zarl__mveql
        xjw__dqn.indices = zvgfd__psikv
        xjw__dqn.indptr = rtlmr__yfv
        xjw__dqn.shape = dyx__afom
        context.nrt.incref(builder, signature.args[0], zarl__mveql)
        context.nrt.incref(builder, signature.args[1], zvgfd__psikv)
        context.nrt.incref(builder, signature.args[2], rtlmr__yfv)
        return xjw__dqn._getvalue()
    rbhxt__ezftx = CSRMatrixType(data_t.dtype, indices_t.dtype)
    lolrk__plxw = rbhxt__ezftx(data_t, indices_t, indptr_t, types.UniTuple(
        types.int64, 2))
    return lolrk__plxw, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    xjw__dqn = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    zlte__xhxpm = c.pyapi.object_getattr_string(val, 'data')
    uena__scd = c.pyapi.object_getattr_string(val, 'indices')
    yncx__hmh = c.pyapi.object_getattr_string(val, 'indptr')
    uvc__uypzd = c.pyapi.object_getattr_string(val, 'shape')
    xjw__dqn.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1, 'C'),
        zlte__xhxpm).value
    xjw__dqn.indices = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 1,
        'C'), uena__scd).value
    xjw__dqn.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 1,
        'C'), yncx__hmh).value
    xjw__dqn.shape = c.pyapi.to_native_value(types.UniTuple(types.int64, 2),
        uvc__uypzd).value
    c.pyapi.decref(zlte__xhxpm)
    c.pyapi.decref(uena__scd)
    c.pyapi.decref(yncx__hmh)
    c.pyapi.decref(uvc__uypzd)
    fropk__zmdu = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(xjw__dqn._getvalue(), is_error=fropk__zmdu)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    sps__xol = c.context.insert_const_string(c.builder.module, 'scipy.sparse')
    dhkj__deesh = c.pyapi.import_module_noblock(sps__xol)
    xjw__dqn = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        xjw__dqn.data)
    zlte__xhxpm = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        xjw__dqn.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        xjw__dqn.indices)
    uena__scd = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'
        ), xjw__dqn.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        xjw__dqn.indptr)
    yncx__hmh = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'
        ), xjw__dqn.indptr, c.env_manager)
    uvc__uypzd = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        xjw__dqn.shape, c.env_manager)
    nkflg__vmsnl = c.pyapi.tuple_pack([zlte__xhxpm, uena__scd, yncx__hmh])
    crxv__ixjc = c.pyapi.call_method(dhkj__deesh, 'csr_matrix', (
        nkflg__vmsnl, uvc__uypzd))
    c.pyapi.decref(nkflg__vmsnl)
    c.pyapi.decref(zlte__xhxpm)
    c.pyapi.decref(uena__scd)
    c.pyapi.decref(yncx__hmh)
    c.pyapi.decref(uvc__uypzd)
    c.pyapi.decref(dhkj__deesh)
    c.context.nrt.decref(c.builder, typ, val)
    return crxv__ixjc


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
    ykfmw__onss = A.dtype
    inouq__vrn = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            jksrt__enz, kuyx__aef = A.shape
            bogl__xop = numba.cpython.unicode._normalize_slice(idx[0],
                jksrt__enz)
            gvl__rpll = numba.cpython.unicode._normalize_slice(idx[1],
                kuyx__aef)
            if bogl__xop.step != 1 or gvl__rpll.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            qpkbq__gfi = bogl__xop.start
            mwc__eux = bogl__xop.stop
            hqmuc__vscxt = gvl__rpll.start
            dnnis__eqqyp = gvl__rpll.stop
            lnu__txghj = A.indptr
            dca__tzjj = A.indices
            pxrq__uzrjh = A.data
            ccx__bov = mwc__eux - qpkbq__gfi
            gredv__oiqeo = dnnis__eqqyp - hqmuc__vscxt
            ktlba__ivkmo = 0
            zem__ruq = 0
            for oaha__cpw in range(ccx__bov):
                qauu__fno = lnu__txghj[qpkbq__gfi + oaha__cpw]
                ulcob__mta = lnu__txghj[qpkbq__gfi + oaha__cpw + 1]
                for rmg__rdfq in range(qauu__fno, ulcob__mta):
                    if dca__tzjj[rmg__rdfq] >= hqmuc__vscxt and dca__tzjj[
                        rmg__rdfq] < dnnis__eqqyp:
                        ktlba__ivkmo += 1
            orjbi__fwdj = np.empty(ccx__bov + 1, inouq__vrn)
            qmg__wfv = np.empty(ktlba__ivkmo, inouq__vrn)
            osnw__hyo = np.empty(ktlba__ivkmo, ykfmw__onss)
            orjbi__fwdj[0] = 0
            for oaha__cpw in range(ccx__bov):
                qauu__fno = lnu__txghj[qpkbq__gfi + oaha__cpw]
                ulcob__mta = lnu__txghj[qpkbq__gfi + oaha__cpw + 1]
                for rmg__rdfq in range(qauu__fno, ulcob__mta):
                    if dca__tzjj[rmg__rdfq] >= hqmuc__vscxt and dca__tzjj[
                        rmg__rdfq] < dnnis__eqqyp:
                        qmg__wfv[zem__ruq] = dca__tzjj[rmg__rdfq
                            ] - hqmuc__vscxt
                        osnw__hyo[zem__ruq] = pxrq__uzrjh[rmg__rdfq]
                        zem__ruq += 1
                orjbi__fwdj[oaha__cpw + 1] = zem__ruq
            return init_csr_matrix(osnw__hyo, qmg__wfv, orjbi__fwdj, (
                ccx__bov, gredv__oiqeo))
        return impl
    elif isinstance(idx, types.Array
        ) and idx.ndim == 1 and idx.dtype == inouq__vrn:

        def impl(A, idx):
            jksrt__enz, kuyx__aef = A.shape
            lnu__txghj = A.indptr
            dca__tzjj = A.indices
            pxrq__uzrjh = A.data
            ccx__bov = len(idx)
            ktlba__ivkmo = 0
            zem__ruq = 0
            for oaha__cpw in range(ccx__bov):
                sdtvq__lkg = idx[oaha__cpw]
                qauu__fno = lnu__txghj[sdtvq__lkg]
                ulcob__mta = lnu__txghj[sdtvq__lkg + 1]
                ktlba__ivkmo += ulcob__mta - qauu__fno
            orjbi__fwdj = np.empty(ccx__bov + 1, inouq__vrn)
            qmg__wfv = np.empty(ktlba__ivkmo, inouq__vrn)
            osnw__hyo = np.empty(ktlba__ivkmo, ykfmw__onss)
            orjbi__fwdj[0] = 0
            for oaha__cpw in range(ccx__bov):
                sdtvq__lkg = idx[oaha__cpw]
                qauu__fno = lnu__txghj[sdtvq__lkg]
                ulcob__mta = lnu__txghj[sdtvq__lkg + 1]
                qmg__wfv[zem__ruq:zem__ruq + ulcob__mta - qauu__fno
                    ] = dca__tzjj[qauu__fno:ulcob__mta]
                osnw__hyo[zem__ruq:zem__ruq + ulcob__mta - qauu__fno
                    ] = pxrq__uzrjh[qauu__fno:ulcob__mta]
                zem__ruq += ulcob__mta - qauu__fno
                orjbi__fwdj[oaha__cpw + 1] = zem__ruq
            edos__ytf = init_csr_matrix(osnw__hyo, qmg__wfv, orjbi__fwdj, (
                ccx__bov, kuyx__aef))
            return edos__ytf
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
