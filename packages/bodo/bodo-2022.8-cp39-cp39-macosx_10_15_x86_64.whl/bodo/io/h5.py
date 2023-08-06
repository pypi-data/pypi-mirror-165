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
        mhe__rbnfo = self._get_h5_type(lhs, rhs)
        if mhe__rbnfo is not None:
            etzu__dbzd = str(mhe__rbnfo.dtype)
            wtff__mqqn = 'def _h5_read_impl(dset, index):\n'
            wtff__mqqn += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(mhe__rbnfo.ndim, etzu__dbzd))
            iwuse__lufy = {}
            exec(wtff__mqqn, {}, iwuse__lufy)
            bnr__caqrt = iwuse__lufy['_h5_read_impl']
            trys__bqs = compile_to_numba_ir(bnr__caqrt, {'bodo': bodo}
                ).blocks.popitem()[1]
            oeeqf__vbu = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(trys__bqs, [rhs.value, oeeqf__vbu])
            btdn__mlpb = trys__bqs.body[:-3]
            btdn__mlpb[-1].target = assign.target
            return btdn__mlpb
        return None

    def _get_h5_type(self, lhs, rhs):
        mhe__rbnfo = self._get_h5_type_locals(lhs)
        if mhe__rbnfo is not None:
            return mhe__rbnfo
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        oeeqf__vbu = rhs.index if rhs.op == 'getitem' else rhs.index_var
        jhdkd__aljz = guard(find_const, self.func_ir, oeeqf__vbu)
        require(not isinstance(jhdkd__aljz, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            iil__luuu = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            dktb__bjdf = get_const_value_inner(self.func_ir, iil__luuu,
                arg_types=self.arg_types)
            obj_name_list.append(dktb__bjdf)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        vrqt__vtzq = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        wos__hwdp = h5py.File(vrqt__vtzq, 'r')
        bexv__orea = wos__hwdp
        for dktb__bjdf in obj_name_list:
            bexv__orea = bexv__orea[dktb__bjdf]
        require(isinstance(bexv__orea, h5py.Dataset))
        pxhka__alpx = len(bexv__orea.shape)
        gwt__pjej = numba.np.numpy_support.from_dtype(bexv__orea.dtype)
        wos__hwdp.close()
        return types.Array(gwt__pjej, pxhka__alpx, 'C')

    def _get_h5_type_locals(self, varname):
        urh__vhl = self.locals.pop(varname, None)
        if urh__vhl is None and varname is not None:
            urh__vhl = self.flags.h5_types.get(varname, None)
        return urh__vhl
