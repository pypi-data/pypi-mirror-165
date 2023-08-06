from numba.core import cgutils, types
from numba.extending import NativeValue, box, make_attribute_wrapper, models, register_model, typeof_impl, unbox


def install_py_obj_class(types_name, module, python_type=None, class_name=
    None, model_name=None):
    class_name = ''.join(map(str.title, types_name.split('_'))
        ) if class_name is None else class_name
    model_name = f'{class_name}Model' if model_name is None else model_name
    wai__otou = f'class {class_name}(types.Opaque):\n'
    wai__otou += f'    def __init__(self):\n'
    wai__otou += f"       types.Opaque.__init__(self, name='{class_name}')\n"
    wai__otou += f'    def __reduce__(self):\n'
    wai__otou += (
        f"        return (types.Opaque, ('{class_name}',), self.__dict__)\n")
    qrtk__zqi = {}
    exec(wai__otou, {'types': types, 'models': models}, qrtk__zqi)
    almpt__dcx = qrtk__zqi[class_name]
    setattr(module, class_name, almpt__dcx)
    class_instance = almpt__dcx()
    setattr(types, types_name, class_instance)
    wai__otou = f'class {model_name}(models.StructModel):\n'
    wai__otou += f'    def __init__(self, dmm, fe_type):\n'
    wai__otou += f'        members = [\n'
    wai__otou += (
        f"            ('meminfo', types.MemInfoPointer({types_name})),\n")
    wai__otou += f"            ('pyobj', types.voidptr),\n"
    wai__otou += f'        ]\n'
    wai__otou += (
        f'        models.StructModel.__init__(self, dmm, fe_type, members)\n')
    exec(wai__otou, {'types': types, 'models': models, types_name:
        class_instance}, qrtk__zqi)
    zxkk__abfe = qrtk__zqi[model_name]
    setattr(module, model_name, zxkk__abfe)
    register_model(almpt__dcx)(zxkk__abfe)
    make_attribute_wrapper(almpt__dcx, 'pyobj', '_pyobj')
    if python_type is not None:
        typeof_impl.register(python_type)(lambda val, c: class_instance)
    unbox(almpt__dcx)(unbox_py_obj)
    box(almpt__dcx)(box_py_obj)
    return almpt__dcx


def box_py_obj(typ, val, c):
    itnur__bfklz = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    obj = itnur__bfklz.pyobj
    c.pyapi.incref(obj)
    c.context.nrt.decref(c.builder, typ, val)
    return obj


def unbox_py_obj(typ, obj, c):
    itnur__bfklz = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    itnur__bfklz.meminfo = c.pyapi.nrt_meminfo_new_from_pyobject(c.context.
        get_constant_null(types.voidptr), obj)
    itnur__bfklz.pyobj = obj
    return NativeValue(itnur__bfklz._getvalue())
