# -*- encoding:utf-8 -*-
"""
    计算线atr模块
"""

import numpy as np
import pandas as pd
from ultron.ump.core.helper import pd_ewm_std, pd_rolling_std
from ultron.ump.technical.line import Line


def calc_atr_std(kl_pd, xd=21, ewm=True):
    """
    计算atr移动平均std或者加权移动平均std技术线，使用
    AbuTLine封装技术线实体，不会修改kl_pd，返回AbuTLine对象
    :param kl_pd: 金融时间序列，pd.DataFrame对象
    :param xd: 计算移动平均std或加权移动平均std使用的窗口参数，默认21
    :param ewm: 是否使用加权移动平均std计算
    :return: 返回AbuTLine对象
    """
    pre_atr21 = kl_pd['atr21'].shift(1)
    # noinspection PyTypeChecker
    atr_change = np.where(pre_atr21 == 0, 0,
                          np.log(kl_pd['atr21'] / pre_atr21))

    if ewm:
        atr_roll_std = pd_ewm_std(
            atr_change, span=xd, min_periods=1, adjust=True) * np.sqrt(xd)
    else:
        atr_roll_std = pd_rolling_std(
            atr_change, window=xd, min_periods=1, center=False) * np.sqrt(xd)

    # min_periods=1还是会有两个nan，填了
    atr_roll_std = pd.Series(atr_roll_std).fillna(method='bfill')
    # 主要目的就是通过atr_roll_std构造line
    line = Line(atr_roll_std, 'atr std')
    return line