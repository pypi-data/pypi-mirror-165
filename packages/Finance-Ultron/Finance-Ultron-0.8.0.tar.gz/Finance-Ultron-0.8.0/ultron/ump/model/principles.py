# -*- encoding:utf-8 -*-
"""封装ML为业务逻辑层进行规范模块"""
from abc import ABCMeta, abstractmethod
from ultron.ump.core.fixes import six
from ultron.ump.model.estimator import Estimator
import pandas as pd
import numpy as np


class Principles(six.with_metaclass(ABCMeta, object)):
    """封装AbuML的上层具体业务逻辑类"""

    def __init__(self, **kwarg):
        """
        从kwarg中输入数据或者，make_xy中本身生产数据，在做完
        make_xy之后，类变量中一定要有x，y和df，使用AbuML继续
        构造self.fiter
        :param kwarg: 直接透传给make_xy的关键子参数，没有必须的参数
        """
        self.make_xy(**kwarg)
        if not hasattr(self, 'x') or not hasattr(self, 'y') \
                or not hasattr(self, 'df'):
            raise ValueError('make_xy failed! x, y not exist!')
        # noinspection PyUnresolvedReferences
        self.fiter = Estimator(self.x, self.y, self.df)

    @abstractmethod
    def make_xy(self, **kwarg):
        """
        子类需要完成的abstractmethod方法，可以从**kwarg中得到数据
        或者make_xy中本身生产数据，但在make_xy之后，类变量中一定要有
        x，y和df
        """
        pass

    def __getattr__(self, item):
        """
        使用ABuML对象self.fiter做为方法代理:
            return getattr(self.fiter, item)
        即AbuMLPd中可以使用ABuML类对象中任何方法
        """
        if item.startswith('__'):
            # noinspection PyUnresolvedReferences
            return super().__getattr__(item)
        return getattr(self.fiter, item)

    def __call__(self):
        """
        方便外面直接call，不用每次去get
        :return: self.fiter
        """
        return self.fiter