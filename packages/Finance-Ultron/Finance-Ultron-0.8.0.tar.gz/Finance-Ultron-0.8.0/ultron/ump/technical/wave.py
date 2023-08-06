# -*- encoding:utf-8 -*-
"""
    量化波动程度模块
"""
import numpy as np
import pandas as pd
from ultron.ump.technical.line import Line
from ultron.ump.core.helper import pd_ewm_std, pd_rolling_std


def calc_wave_std(kl_pd, xd=21, ewm=True):
    """
    计算收益的移动平均std或者加权移动平均std技术线，使用
    Line封装技术线实体，不会修改kl_pd，返回AbuTLine对象
    :param kl_pd: 金融时间序列，pd.DataFrame对象
    :param xd: 计算移动平均std或加权移动平均std使用的窗口参数，默认21
    :param ewm: 是否使用加权移动平均std计算
    :return: 返回Line对象
    """
    pre_close = kl_pd['close'].shift(1)
    change = np.where(pre_close == 0, 0, np.log(kl_pd['close'] / pre_close))
    if ewm:
        roll_std = pd_ewm_std(change, span=xd, min_periods=1,
                              adjust=True) * np.sqrt(xd)
    else:
        roll_std = pd_rolling_std(
            change, window=xd, min_periods=1, center=False) * np.sqrt(xd)

    # min_periods=1还是会有两个nan，填了
    roll_std = pd.Series(roll_std).fillna(method='bfill')
    line = Line(roll_std, 'wave std')
    return line