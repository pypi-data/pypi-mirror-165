from numba.core import cgutils, types
from numba.extending import NativeValue, box, make_attribute_wrapper, models, register_model, typeof_impl, unbox


def install_py_obj_class(types_name, module, python_type=None, class_name=
    None, model_name=None):
    class_name = ''.join(map(str.title, types_name.split('_'))
        ) if class_name is None else class_name
    model_name = f'{class_name}Model' if model_name is None else model_name
    cxgs__rlu = f'class {class_name}(types.Opaque):\n'
    cxgs__rlu += f'    def __init__(self):\n'
    cxgs__rlu += f"       types.Opaque.__init__(self, name='{class_name}')\n"
    cxgs__rlu += f'    def __reduce__(self):\n'
    cxgs__rlu += (
        f"        return (types.Opaque, ('{class_name}',), self.__dict__)\n")
    fiw__nzo = {}
    exec(cxgs__rlu, {'types': types, 'models': models}, fiw__nzo)
    yoymv__bos = fiw__nzo[class_name]
    setattr(module, class_name, yoymv__bos)
    class_instance = yoymv__bos()
    setattr(types, types_name, class_instance)
    cxgs__rlu = f'class {model_name}(models.StructModel):\n'
    cxgs__rlu += f'    def __init__(self, dmm, fe_type):\n'
    cxgs__rlu += f'        members = [\n'
    cxgs__rlu += (
        f"            ('meminfo', types.MemInfoPointer({types_name})),\n")
    cxgs__rlu += f"            ('pyobj', types.voidptr),\n"
    cxgs__rlu += f'        ]\n'
    cxgs__rlu += (
        f'        models.StructModel.__init__(self, dmm, fe_type, members)\n')
    exec(cxgs__rlu, {'types': types, 'models': models, types_name:
        class_instance}, fiw__nzo)
    hjucj__uux = fiw__nzo[model_name]
    setattr(module, model_name, hjucj__uux)
    register_model(yoymv__bos)(hjucj__uux)
    make_attribute_wrapper(yoymv__bos, 'pyobj', '_pyobj')
    if python_type is not None:
        typeof_impl.register(python_type)(lambda val, c: class_instance)
    unbox(yoymv__bos)(unbox_py_obj)
    box(yoymv__bos)(box_py_obj)
    return yoymv__bos


def box_py_obj(typ, val, c):
    wya__zjyws = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    obj = wya__zjyws.pyobj
    c.pyapi.incref(obj)
    c.context.nrt.decref(c.builder, typ, val)
    return obj


def unbox_py_obj(typ, obj, c):
    wya__zjyws = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    wya__zjyws.meminfo = c.pyapi.nrt_meminfo_new_from_pyobject(c.context.
        get_constant_null(types.voidptr), obj)
    wya__zjyws.pyobj = obj
    return NativeValue(wya__zjyws._getvalue())
