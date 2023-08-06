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
    vwwol__rhgsy = context.get_python_api(builder)
    return vwwol__rhgsy.unserialize(vwwol__rhgsy.serialize_object(pyval))


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
        nfio__xungi = ', '.join('e{}'.format(xnn__buacb) for xnn__buacb in
            range(len(args)))
        if nfio__xungi:
            nfio__xungi += ', '
        gvo__inx = ', '.join("{} = ''".format(kwue__jxtqn) for kwue__jxtqn in
            kws.keys())
        iiqv__xvfw = f'def format_stub(string, {nfio__xungi} {gvo__inx}):\n'
        iiqv__xvfw += '    pass\n'
        hxxi__rmsxb = {}
        exec(iiqv__xvfw, {}, hxxi__rmsxb)
        wdeoa__nvsx = hxxi__rmsxb['format_stub']
        ltti__ady = numba.core.utils.pysignature(wdeoa__nvsx)
        jhvy__mrhjl = (logger_typ,) + args + tuple(kws.values())
        return signature(logger_typ, jhvy__mrhjl).replace(pysig=ltti__ady)
    func_names = ('debug', 'warning', 'warn', 'info', 'error', 'exception',
        'critical', 'log', 'setLevel')
    for mjh__yuupt in ('logging.Logger', 'logging.RootLogger'):
        for ldx__fnd in func_names:
            tpdb__sivt = f'@bound_function("{mjh__yuupt}.{ldx__fnd}")\n'
            tpdb__sivt += (
                f'def resolve_{ldx__fnd}(self, logger_typ, args, kws):\n')
            tpdb__sivt += (
                '    return self._resolve_helper(logger_typ, args, kws)')
            exec(tpdb__sivt)


logging_logger_unsupported_attrs = {'filters', 'handlers', 'manager'}
logging_logger_unsupported_methods = {'addHandler', 'callHandlers', 'fatal',
    'findCaller', 'getChild', 'getEffectiveLevel', 'handle', 'hasHandlers',
    'isEnabledFor', 'makeRecord', 'removeHandler'}


def _install_logging_logger_unsupported_objects():
    for kubtf__swbqx in logging_logger_unsupported_attrs:
        wxate__ftaxu = 'logging.Logger.' + kubtf__swbqx
        overload_attribute(LoggingLoggerType, kubtf__swbqx)(
            create_unsupported_overload(wxate__ftaxu))
    for buito__ifd in logging_logger_unsupported_methods:
        wxate__ftaxu = 'logging.Logger.' + buito__ifd
        overload_method(LoggingLoggerType, buito__ifd)(
            create_unsupported_overload(wxate__ftaxu))


_install_logging_logger_unsupported_objects()
