# -*- encoding:utf-8 -*-
"""
    类基础通用模块
"""


class FreezeAttrMixin(object):
    """冻结对外设置属性混入类，设置抛异常"""

    def _freeze(self):
        """冻结属性设置接口"""
        object.__setattr__(self, "__frozen", True)

    def __setattr__(self, key, value):
        if getattr(
                self, "__frozen",
                False) and not (key in type(self).__dict__ or key == "_cache"):
            raise AttributeError(
                "You cannot add any new attribute '{key}'".format(key=key))
        object.__setattr__(self, key, value)