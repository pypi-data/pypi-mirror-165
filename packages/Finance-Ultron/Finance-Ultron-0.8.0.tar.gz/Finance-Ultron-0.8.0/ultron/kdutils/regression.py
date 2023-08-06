# -*- encoding:utf-8 -*-
"""
    拟合工具模块
"""
import math
import numpy as np
from statsmodels import api as sm, regression
from sklearn import metrics
from ultron.ump.core.helper import pd_rolling_mean


def regress_xy(x, y, mode=True, zoom=False):
    """
    使用statsmodels.regression.linear_model进行简单拟合操作，返回model和y_fit
    :param x: 可迭代序列
    :param y: 可迭代序列
    :param mode: 是否需要mode结果，在只需要y_fit且效率需要高时应设置False, 效率差异：
                 mode=False: 1000 loops, best of 3: 778 µs per loop
                 mode=True:  1000 loops, best of 3: 1.23 ms per loop
    :param zoom: 是否缩放x,y
    :param show: 是否可视化结果
    :return: model, y_fit, 如果mode=False，返回的model=None
    """
    if zoom:
        # 将y值 zoom到与x一个级别，不可用ABuScalerUtil.scaler_xy, 因为不管x > y还y > x都拿 x.max() / y.max()
        # TODO ABuScalerUtil中添加使用固定轴进行缩放的功能
        zoom_factor = x.max() / y.max()
        y = zoom_factor * y

    if mode:
        # 加常数1列
        x = sm.add_constant(x)
        model = regression.linear_model.OLS(y, x).fit()

        intercept = model.params[0]
        rad = model.params[1]
        # y = kx + b, x取x[:, 1]，因为add_constant
        y_fit = x[:, 1] * rad + intercept
    else:
        # noinspection PyCallingNonCallable
        y_fit = np.polynomial.Chebyshev.fit(x, y, 1)(x)
        model = None
    return model, y_fit


def regress_y(y, mode=True, zoom=False):
    """
    使用statsmodels.regression.linear_model进行简单拟合操作, 参数中只提供y序列，
    x使用np.arange(0, len(y))填充
    :param y: 可迭代序列
    :param mode: 是否需要mode结果，在只需要y_fit且效率需要高时应设置False, 效率差异：
             mode=False: 1000 loops, best of 3: 778 µs per loop
             mode=True:  1000 loops, best of 3: 1.23 ms per loop
    :param zoom: 是否缩放x,y
    :param show: 是否可视化结果
    :return: model, y_fit, 如果mode=False，返回的model=None
    """
    x = np.arange(0, len(y))
    return regress_xy(x, y, mode=mode, zoom=zoom)


def calc_regress_deg(y):
    """
    将y值 zoom到与x一个级别，之后再fit出弧度转成角度
    1 多个的趋势比较提供量化基础，只要同一个时间范围，就可以比较
    2 接近视觉感受到的角度
    :param y:  可迭代序列
    :param show: 是否可视化结果
    :return: deg角度float值
    """
    # 将y值 zoom到与x一个级别
    model, _ = regress_y(y, mode=True, zoom=True)
    rad = model.params[1]
    # fit出弧度转成角度
    deg = np.rad2deg(rad)
    return deg


def metrics_rmse(y, y_fit):
    """
    度量原始序列和拟合后的y_fit的RMSE：
         RMSE = np.sqrt(sum(np.square(y - y_fit)) / len(y))
    :param y: 原始可迭代序列
    :param y_fit: 拟合可迭代序列
    :return: 返回RMSE值，float
    """
    rmse = np.sqrt(metrics.mean_squared_error(y, y_fit))
    return rmse


def regress_xy_polynomial(x, y, poly=1, zoom=False):
    """
    多项式拟合, 根据参数poly决定，返回拟合后的y_fit
    :param x: 可迭代序列
    :param y: 可迭代序列
    :param poly: 几次拟合参数，int
    :param zoom: 是否对数据进行缩放
    :param show: 是否可视化显示拟合结果
    :return: y_fit
    """
    if zoom:
        # 将y值 zoom到与x一个级别，不可用ABuScalerUtil.scaler_xy, 因为不管x > y还y > x都拿 x.max() / y.max()
        zoom_factor = x.max() / y.max()
        y = zoom_factor * y

    polynomial = np.polynomial.Chebyshev.fit(x, y, poly)
    # noinspection PyCallingNonCallable
    y_fit = polynomial(x)
    return y_fit


def valid_poly(y, poly=1, zoom=False, metrics_func=metrics_rmse):
    """
    验证poly（默认＝1）次多项式拟合回归的趋势曲线是否能代表原始曲线y的走势，
    基础思路：
             1. 对原始曲线y进行窗口均线计算，窗口的大小＝ math.ceil(len(y) / 4)
             eg：
                原始y序列＝504 －> rolling_window = math.ceil(len(y) / 4) = 126
             2. 通过pd_rolling_mean计算出均线的值y_roll_mean
             3  使用metrics_func方法度量原始y值和均线y_roll_mean的距离distance_mean
             3. 通过计算regress_xy_polynomial计算多项式拟合回归的趋势曲线y_fit
             4. 使用metrics_func方法度量原始y值和拟合回归的趋势曲线y_fit的距离distance_fit
             5. 如果distance_fit <= distance_mean即代表拟合曲线可以代表原始曲线y的走势
    :param y: 原始可迭代序列
    :param poly: 几次拟合参数，int
    :param zoom: 是否对y数据进行缩放
    :param show: 是否原始曲线y，均线，以及拟合曲线可视化
    :param metrics_func: 度量始y值和均线y_roll_mean的距离和原始y值和
                         拟合回归的趋势曲线y_fit的距离的方法，默认使用metrics_rmse
    :return: 是否poly次拟合曲线可以代表原始曲线y的走势
    """
    valid = False
    x = np.arange(0, len(y))
    if zoom:
        # 将y值 zoom到与x一个级别，不可用ABuScalerUtil.scaler_xy, 因为不管x > y还y > x都拿 x.max() / y.max()
        zoom_factor = x.max() / y.max()
        y = zoom_factor * y
    # 对原始曲线y进行窗口均线计算，窗口的大小＝ math.ceil(len(y) / 4)
    rolling_window = int(math.ceil(len(y) / 4))
    # 通过pd_rolling_mean计算出均线的值y_roll_mean
    y_roll_mean = pd_rolling_mean(y, window=rolling_window, min_periods=1)
    # 使用metrics_func方法度量原始y值和均线y_roll_mean的距离distance_mean
    distance_mean = metrics_func(y, y_roll_mean, show=False)

    # 通过计算regress_xy_polynomial计算多项式拟合回归的趋势曲线y_fit, 外面做zoom了所以zoom=False
    y_fit = regress_xy_polynomial(x, y, poly=poly, zoom=False)

    # 使用metrics_func方法度量原始y值和拟合回归的趋势曲线y_fit的距离distance_fit
    distance_fit = metrics_func(y, y_fit)

    # 如果distance_fit <= distance_mean即代表拟合曲线可以代表原始曲线y的走势
    if distance_fit <= distance_mean:
        valid = True

    return valid
