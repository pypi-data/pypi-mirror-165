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
            ooyuk__rqnit = set()
            cak__sujvh = list(self.context._get_attribute_templates(self.key))
            xpde__urfe = cak__sujvh.index(self) + 1
            for uknpc__vux in range(xpde__urfe, len(cak__sujvh)):
                if isinstance(cak__sujvh[uknpc__vux], numba.core.typing.
                    templates._OverloadAttributeTemplate):
                    ooyuk__rqnit.add(cak__sujvh[uknpc__vux]._attr)
            self._attr_set = ooyuk__rqnit
        return attr_name in self._attr_set
