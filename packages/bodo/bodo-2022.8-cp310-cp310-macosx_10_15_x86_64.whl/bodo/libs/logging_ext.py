"""
JIT support for Python's logging module
"""
import logging
import numba
from numba.core import types
from numba.core.imputils import lower_constant
from numba.core.typing.templates import bound_function
from numba.core.typing.templates import AttributeTemplate, infer_getattr, signature
from numba.extending import NativeValue, box, models, overload_attribute, overload_method, register_model, typeof_impl, unbox
from bodo.utils.typing import create_unsupported_overload, gen_objmode_attr_overload


class LoggingLoggerType(types.Type):

    def __init__(self, is_root=False):
        self.is_root = is_root
        super(LoggingLoggerType, self).__init__(name=
            f'LoggingLoggerType(is_root={is_root})')


@typeof_impl.register(logging.RootLogger)
@typeof_impl.register(logging.Logger)
def typeof_logging(val, c):
    if isinstance(val, logging.RootLogger):
        return LoggingLoggerType(is_root=True)
    else:
        return LoggingLoggerType(is_root=False)


register_model(LoggingLoggerType)(models.OpaqueModel)


@box(LoggingLoggerType)
def box_logging_logger(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(LoggingLoggerType)
def unbox_logging_logger(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@lower_constant(LoggingLoggerType)
def lower_constant_logger(context, builder, ty, pyval):
    vkof__tjgy = context.get_python_api(builder)
    return vkof__tjgy.unserialize(vkof__tjgy.serialize_object(pyval))


gen_objmode_attr_overload(LoggingLoggerType, 'level', None, types.int64)
gen_objmode_attr_overload(LoggingLoggerType, 'name', None, 'unicode_type')
gen_objmode_attr_overload(LoggingLoggerType, 'propagate', None, types.boolean)
gen_objmode_attr_overload(LoggingLoggerType, 'disabled', None, types.boolean)
gen_objmode_attr_overload(LoggingLoggerType, 'parent', None,
    LoggingLoggerType())
gen_objmode_attr_overload(LoggingLoggerType, 'root', None,
    LoggingLoggerType(is_root=True))


@infer_getattr
class LoggingLoggerAttribute(AttributeTemplate):
    key = LoggingLoggerType

    def _resolve_helper(self, logger_typ, args, kws):
        kws = dict(kws)
        vjhgh__vkp = ', '.join('e{}'.format(izpb__mkv) for izpb__mkv in
            range(len(args)))
        if vjhgh__vkp:
            vjhgh__vkp += ', '
        walzp__wqk = ', '.join("{} = ''".format(wdmoc__yiunm) for
            wdmoc__yiunm in kws.keys())
        uhspq__csa = f'def format_stub(string, {vjhgh__vkp} {walzp__wqk}):\n'
        uhspq__csa += '    pass\n'
        ifk__kisjj = {}
        exec(uhspq__csa, {}, ifk__kisjj)
        rmr__rkhkx = ifk__kisjj['format_stub']
        way__cfkj = numba.core.utils.pysignature(rmr__rkhkx)
        avpz__xmklz = (logger_typ,) + args + tuple(kws.values())
        return signature(logger_typ, avpz__xmklz).replace(pysig=way__cfkj)
    func_names = ('debug', 'warning', 'warn', 'info', 'error', 'exception',
        'critical', 'log', 'setLevel')
    for nxwm__zqrri in ('logging.Logger', 'logging.RootLogger'):
        for iwm__dnx in func_names:
            dqou__ntsc = f'@bound_function("{nxwm__zqrri}.{iwm__dnx}")\n'
            dqou__ntsc += (
                f'def resolve_{iwm__dnx}(self, logger_typ, args, kws):\n')
            dqou__ntsc += (
                '    return self._resolve_helper(logger_typ, args, kws)')
            exec(dqou__ntsc)


logging_logger_unsupported_attrs = {'filters', 'handlers', 'manager'}
logging_logger_unsupported_methods = {'addHandler', 'callHandlers', 'fatal',
    'findCaller', 'getChild', 'getEffectiveLevel', 'handle', 'hasHandlers',
    'isEnabledFor', 'makeRecord', 'removeHandler'}


def _install_logging_logger_unsupported_objects():
    for dpolh__nkqwc in logging_logger_unsupported_attrs:
        dpvts__tpp = 'logging.Logger.' + dpolh__nkqwc
        overload_attribute(LoggingLoggerType, dpolh__nkqwc)(
            create_unsupported_overload(dpvts__tpp))
    for sax__bwr in logging_logger_unsupported_methods:
        dpvts__tpp = 'logging.Logger.' + sax__bwr
        overload_method(LoggingLoggerType, sax__bwr)(
            create_unsupported_overload(dpvts__tpp))


_install_logging_logger_unsupported_objects()
