# -*- encoding:utf-8 -*-
import functools, os, warnings
import numpy as np
import pandas as pd
from collections import Iterable
from ultron.ump.core.fixes import six


def warnings_filter(func):
    """
        作用范围：函数装饰器 (模块函数或者类函数)
        功能：被装饰的函数上的警告不会打印，忽略
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        warnings.simplefilter('ignore')
        ret = func(*args, **kwargs)
        if 'IGNORE_WARNINGS' not in os.environ or not os.environ[
                'IGNORE_WARNINGS']:
            warnings.simplefilter('default')
        return ret

    return wrapper


def arr_to_numpy(arr):
    """
        函数装饰器：将可以迭代的序列转换为np.array，支持pd.DataFrame或者pd.Series
        ，list，dict, list，set，嵌套可迭代序列, 混嵌套可迭代序列
    """
    # TODO Iterable和six.string_types的判断抽出来放在一个模块，做为Iterable的判断来使用
    if not isinstance(arr, Iterable) or isinstance(arr, six.string_types):
        return arr

    if not isinstance(arr, np.ndarray):
        if isinstance(arr, pd.DataFrame) or isinstance(arr, pd.Series):
            # 如果是pandas直接拿values
            arr = arr.values
        elif isinstance(arr, dict):
            # 针对dict转换np.array
            arr = np.array(list(arr.values())).T
        else:
            arr = np.array(arr)
    return arr
