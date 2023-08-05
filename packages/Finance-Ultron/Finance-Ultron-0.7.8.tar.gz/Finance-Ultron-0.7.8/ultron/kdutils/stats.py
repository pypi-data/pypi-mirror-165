# -*- encoding:utf-8 -*-
"""
    统计相关工具模块
"""
import numpy as np
import functools
import scipy.stats as scs
from collections import namedtuple, Iterable


# noinspection PyClassHasNoInit
class MomentsTuple(
        namedtuple(
            'MomentsTuple',
            ('count', 'max', 'min', 'mean', 'std', 'skewness', 'kurtosis'))):
    __slots__ = ()

    def __repr__(self):
        return "count:{}\nmax:{}\nmin:{}\nmean:{}\nstd:{}\nskewness:{}\nkurtosis:{}".format(
            self.count, self.max, self.min, self.mean, self.std, self.skewness,
            self.kurtosis)


def arr_to_numpy(func):
    """
        函数装饰器：定参数装饰器，非通用，通用转换使用ABuDTUtil中的装饰器
        将被装饰函数中的arr序列转换为np.array
    """

    @functools.wraps(func)
    def wrapper(arr, *arg, **kwargs):
        # TODO Iterable和six.string_types的判断抽出来放在一个模块，做为Iterable的判断来使用
        if not isinstance(arr, Iterable) or isinstance(arr, six.string_types):
            # arr必须是可以迭代的对象
            raise TypeError('arr not isinstance of Iterable')

        if not isinstance(arr, np.ndarray):
            if isinstance(arr, pd.DataFrame) or isinstance(arr, pd.Series):
                # 如果是pandas直接拿values
                arr = arr.values
            elif isinstance(arr, dict):
                # 针对dict转换np.array
                arr = np.array(list(arr.values())).T
            else:
                arr = np.array(arr)
        return func(arr, *arg, **kwargs)

    return wrapper


@arr_to_numpy
def stats_namedtuple(arr):
    """
    通过序列构造arr的基础统计信息dict, 被arr_to_numpy装饰，统一输出，且这样使用arr.max(), arr.min()等不需要axis参数区别
    与stats_dict的区别只是返回namedtuple对象
    :param arr: pd.DataFrame or pd.Series or Iterable
    :return: MomentsTuple
                eg:
                    count:504
                    max:286.04
                    min:143.67
                    mean:228.48845238095237
                    std:25.538448192811927
                    skewness:-0.282635248604699
                    kurtosis:0.009313464006726946

    """
    count = arr.shape[0]
    if len(arr.shape) > 1 and arr.shape[1] > 1:
        count = arr.shape[0] * arr.shape[1]

    return MomentsTuple(count, arr.max(), arr.min(), arr.mean(), arr.std(),
                        scs.skew(arr), scs.kurtosis(arr))
