# -*- encoding:utf-8 -*-
"""
    跳空缺口模块
"""
import numpy as np
import pandas as pd
from ultron.ump.core.helper import pd_resample
from ultron.kdutils.date import fmt_date


def calc_jump(kl_pd, jump_diff_factor=1):
    """
    通过对比交易日当月的成交量，和当月的振幅来确定交易日当日的跳空阀值，
    分别组装跳空方向，跳空能量，跳空距离等数据进入pd.DataFrame对象返回
    :param kl_pd: 金融时间序列，pd.DataFrame对象
    :param jump_diff_factor: 参数通过设置jump_diff_factor来调节跳空阀值的大小，默认jump_diff_factor＝1
    :param show: 是否对结果跳空点进行可视化
    :return: pd.DataFrame对象
    """
    # 由于过程会修改金融时间序列，所以先copy一个再处理
    kl_pd = kl_pd.copy()
    # 将日change取abs变成日振幅保存在kl_pd新列abs_pct_change
    kl_pd['abs_pct_change'] = np.abs(kl_pd['p_change'])
    # 日振幅取平均做为第一层判断是否达成跳空的条件，即跳空最起码要振幅超过日振幅平均值
    change_ratio_min = kl_pd['abs_pct_change'].mean()

    # 提取月振幅volume_mean
    # TODO 做为参数可修改21d
    change_mean = pd_resample(kl_pd.abs_pct_change, '21D', how='mean')
    """
        eg: change_mean形如
        2014-07-23    0.7940
        2014-08-13    0.6536
        2014-09-03    0.8120
        2014-09-24    1.2673
        2014-10-15    1.1007
                       ...
        2016-04-13    1.2080
        2016-05-04    0.9093
        2016-05-25    0.6208
        2016-06-15    1.1831
        2016-07-06    0.6693
    """
    # 提取月成交量均值volume_mean
    volume_mean = pd_resample(kl_pd.volume, '21D', how='mean')
    """
        eg：volume_mean形如
        2014-07-23    1350679
        2014-08-13    1256093
        2014-09-03    1593358
        2014-09-24    1816544
        2014-10-15    2362897
                       ...
        2016-04-13    2341972
        2016-05-04    1633200
        2016-05-25    1372525
        2016-06-15    2071612
        2016-07-06    1136278
    """
    # 使用使用kl_pd没有resample之前的index和change_mean进行loc操作，为了把没有的index都变成nan
    change_mean = change_mean.loc[kl_pd.index.intersection(change_mean.index)]
    # 有nan之后开始填充nan
    change_mean.fillna(method='pad', inplace=True)
    # bfill再来一遍只是为了填充最前面的nan
    change_mean.fillna(method='bfill', inplace=True)
    """
        loc以及填充nan后change_mean形如：change_mean
        2014-07-23    0.7940
        2014-07-24    0.7940
        2014-07-25    0.7940
        2014-07-28    0.7940
        2014-07-29    0.7940
        2014-07-30    0.7940
        2014-07-31    0.7940
        2014-08-01    0.7940
        2014-08-04    0.7940
        2014-08-05    0.7940
                       ...
        2016-07-13    0.6693
        2016-07-14    0.6693
        2016-07-15    0.6693
        2016-07-18    0.6693
        2016-07-19    0.6693
        2016-07-20    0.6693
        2016-07-21    0.6693
        2016-07-22    0.6693
        2016-07-25    0.6693
        2016-07-26    0.6693
    """
    # 使用使用kl_pd没有resample之前的index和change_mean进行loc操作，为了把没有的index都变成nan
    volume_mean = volume_mean.loc[kl_pd.index.intersection(volume_mean.index)]
    # 有nan之后开始填充nan
    volume_mean.fillna(method='pad', inplace=True)
    # bfill再来一遍只是为了填充最前面的nan
    volume_mean.fillna(method='bfill', inplace=True)
    """
        loc以及填充nan后volume_mean形如：change_mean
        2014-07-23    1350679.0
        2014-07-24    1350679.0
        2014-07-25    1350679.0
        2014-07-28    1350679.0
        2014-07-29    1350679.0
        2014-07-30    1350679.0
        2014-07-31    1350679.0
        2014-08-01    1350679.0
        2014-08-04    1350679.0
        2014-08-05    1350679.0
                        ...
        2016-07-13    1136278.0
        2016-07-14    1136278.0
        2016-07-15    1136278.0
        2016-07-18    1136278.0
        2016-07-19    1136278.0
        2016-07-20    1136278.0
        2016-07-21    1136278.0
        2016-07-22    1136278.0
        2016-07-25    1136278.0
        2016-07-26    1136278.0
    """
    jump_pd = pd.DataFrame()

    # 迭代金融时间序列，即针对每一个交易日分析跳空
    for kl_index in np.arange(0, kl_pd.shape[0]):
        today = kl_pd.iloc[kl_index]

        if today.abs_pct_change <= change_ratio_min:
            # 第一层判断：跳空最起码要振幅超过日振幅平均值
            continue

        date = fmt_date(today.date)
        if date not in volume_mean.index:
            continue
        if today.volume <= volume_mean.loc[date]:
            # 第二层判断：跳空当日的成交量起码要超过当月平均值
            continue

        # 获取今天对应的月振幅, 做为今天判断是否跳空的价格阀值百分比
        jump_threshold = np.abs(change_mean.loc[date])
        if today.pre_close == 0 or jump_threshold == 0:
            # 只是为避免异常数据
            continue

        # 计算跳空距离阀值，即以昨天收盘为基数乘以跳空阀值比例除100得到和高开低收相同单位的价格阀值jump_diff
        # 参数通过设置jump_diff_factor来调节跳空阀值的大小，默认jump_diff_factor＝1
        jump_diff = today.pre_close * jump_threshold / 100 * jump_diff_factor
        # 第三层判断：根据向上向下跳空选择跳空计算
        if today.p_change > 0 and (today.low - today.pre_close) > jump_diff:
            # 注意向上跳空判断使用today.low，向上跳空 1
            today['jump'] = 1
            # 月振幅跳空阀值
            today['jump_threshold'] = jump_threshold
            # 跳空距离阀值
            today['jump_diff'] = jump_diff
            # 计算出跳空缺口强度
            today['jump_power'] = (today.low - today.pre_close) / jump_diff

            jump_pd = jump_pd.append(today)
        elif today.p_change < 0 and (today.pre_close - today.high) > jump_diff:
            # 注意向下跳空判断使用today.high，向下跳空 －1
            today['jump'] = -1
            # 月振幅跳空阀值
            today['jump_threshold'] = jump_threshold
            # 跳空距离阀值
            today['jump_diff'] = jump_diff
            # 计算出跳空缺口强度
            today['jump_power'] = (today.pre_close - today.high) / jump_diff
            jump_pd = jump_pd.append(today)
    return jump_pd