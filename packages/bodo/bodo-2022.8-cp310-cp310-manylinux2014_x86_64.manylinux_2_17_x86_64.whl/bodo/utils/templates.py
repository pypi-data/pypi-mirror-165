"""
Helper functions and classes to simplify Template Generation
for Bodo classes.
"""
import numba
from numba.core.typing.templates import AttributeTemplate


class OverloadedKeyAttributeTemplate(AttributeTemplate):
    _attr_set = None

    def _is_existing_attr(self, attr_name):
        if self._attr_set is None:
            kgxml__ykzu = set()
            bnd__fcmr = list(self.context._get_attribute_templates(self.key))
            rfezp__zpum = bnd__fcmr.index(self) + 1
            for wzrvt__aoo in range(rfezp__zpum, len(bnd__fcmr)):
                if isinstance(bnd__fcmr[wzrvt__aoo], numba.core.typing.
                    templates._OverloadAttributeTemplate):
                    kgxml__ykzu.add(bnd__fcmr[wzrvt__aoo]._attr)
            self._attr_set = kgxml__ykzu
        return attr_name in self._attr_set
