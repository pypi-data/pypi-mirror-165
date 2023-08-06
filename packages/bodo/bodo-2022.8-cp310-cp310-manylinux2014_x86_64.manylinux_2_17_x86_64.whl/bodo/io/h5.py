"""
Analysis and transformation for HDF5 support.
"""
import types as pytypes
import numba
from numba.core import ir, types
from numba.core.ir_utils import compile_to_numba_ir, find_callname, find_const, get_definition, guard, replace_arg_nodes, require
import bodo
import bodo.io
from bodo.utils.transform import get_const_value_inner


class H5_IO:

    def __init__(self, func_ir, _locals, flags, arg_types):
        self.func_ir = func_ir
        self.locals = _locals
        self.flags = flags
        self.arg_types = arg_types

    def handle_possible_h5_read(self, assign, lhs, rhs):
        fxog__wlqp = self._get_h5_type(lhs, rhs)
        if fxog__wlqp is not None:
            vev__qth = str(fxog__wlqp.dtype)
            vskc__yaorg = 'def _h5_read_impl(dset, index):\n'
            vskc__yaorg += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(fxog__wlqp.ndim, vev__qth))
            yuwz__wku = {}
            exec(vskc__yaorg, {}, yuwz__wku)
            gnr__jpvxp = yuwz__wku['_h5_read_impl']
            kayru__iwisb = compile_to_numba_ir(gnr__jpvxp, {'bodo': bodo}
                ).blocks.popitem()[1]
            fkp__jrq = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(kayru__iwisb, [rhs.value, fkp__jrq])
            imv__elxl = kayru__iwisb.body[:-3]
            imv__elxl[-1].target = assign.target
            return imv__elxl
        return None

    def _get_h5_type(self, lhs, rhs):
        fxog__wlqp = self._get_h5_type_locals(lhs)
        if fxog__wlqp is not None:
            return fxog__wlqp
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        fkp__jrq = rhs.index if rhs.op == 'getitem' else rhs.index_var
        gmsqc__yurmd = guard(find_const, self.func_ir, fkp__jrq)
        require(not isinstance(gmsqc__yurmd, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            ooxqu__prw = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            nuw__bmz = get_const_value_inner(self.func_ir, ooxqu__prw,
                arg_types=self.arg_types)
            obj_name_list.append(nuw__bmz)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        ucv__ybypr = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        qdt__jdxxb = h5py.File(ucv__ybypr, 'r')
        okl__unnw = qdt__jdxxb
        for nuw__bmz in obj_name_list:
            okl__unnw = okl__unnw[nuw__bmz]
        require(isinstance(okl__unnw, h5py.Dataset))
        dlktr__uvh = len(okl__unnw.shape)
        ogj__xjem = numba.np.numpy_support.from_dtype(okl__unnw.dtype)
        qdt__jdxxb.close()
        return types.Array(ogj__xjem, dlktr__uvh, 'C')

    def _get_h5_type_locals(self, varname):
        rke__ahwra = self.locals.pop(varname, None)
        if rke__ahwra is None and varname is not None:
            rke__ahwra = self.flags.h5_types.get(varname, None)
        return rke__ahwra
