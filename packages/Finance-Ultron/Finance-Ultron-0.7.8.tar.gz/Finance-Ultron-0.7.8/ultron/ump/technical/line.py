# -*- encoding:utf-8 -*-
"""
    技术线对象，对外执行，输出模块
"""
import math
import numpy as np
import pandas as pd
from ultron.kdutils.lazy import LazyFunc
from ultron.ump.core.base import FreezeAttrMixin
from ultron.kdutils.decorator import arr_to_numpy
from ultron.kdutils import regression
"""step_x_to_step函数中序列步长的常数单元值"""
g_step_unit = 10


class Line(FreezeAttrMixin):
    """技术线封装执行对外操作的对象类"""

    def __init__(self, line, line_name, **kwargs):
        """
        :param line: 技术线可迭代序列，内部会通过arr_to_numpy统一转换numpy
        :param line_name: 技术线名称，str对象
        :param kwargs mean: 外部可选择通过kwargs设置mean，如不设置line.mean()
        :param kwargs std: 外部可选择通过kwargs设置std，如不设置line.std()
        :param kwargs high: 外部可选择通过kwargs设置high，如不设置self.mean + self.std
        :param kwargs low: 外部可选择通过kwargs设置low，如不设置self.mean - self.std
        :param kwargs close: 外部可选择通过kwargs设置close，如不设置line[-1]
        """
        # 把序列的nan进行填充，实际上应该是外面根据数据逻辑把nan进行填充好了再传递进来，这里只能都使用bfill填了
        line = pd.Series(line).fillna(method='bfill')
        self.tl = arr_to_numpy(line)
        self.mean = kwargs.pop('mean', self.tl.mean())
        self.std = kwargs.pop('std', self.tl.std())
        self.high = kwargs.pop('high', self.mean + self.std)
        self.low = kwargs.pop('low', self.mean - self.std)
        self.close = kwargs.pop('close', self.tl[-1])

        self.x = np.arange(0, self.tl.shape[0])
        self.line_name = line_name

        for k, v in kwargs:
            # 需要设置什么都通过kwargs设置进来，不然_freeze后无法设置
            setattr(self, k, v)
        # 需要进行定稿，初始化好就不能动
        self._freeze()

    @LazyFunc
    def score(self):
        """
        被LazyFunc装饰：
        score代表当前技术线值在当前的位置， (self.close - self.low) / (self.high - self.low)
        eg：
            self.high ＝ 100， self.low＝0，self.close＝80
            －> (self.close - self.low) / (self.high - self.low) = 0.8
            即代表当前位置在整体的0.8位置上

        :return: 技术线当前score, 返回值在0-1之间
        """
        if self.high == self.low:
            score = 0.8 if self.close > self.low else 0.2
        else:
            score = (self.close - self.low) / (self.high - self.low)
        return score

    @LazyFunc
    def y_zoom(self):
        """
        被LazyFunc装饰：
        获取对象技术线tl被self.x缩放后的序列y_zoom
        :return: 放后的序列y_zoom
        """
        zoom_factor = self.x.max() / self.tl.max()
        y_zoom = zoom_factor * self.tl
        return y_zoom

    def step_x_to_step(self, step_x):
        """
        针对技术线的时间范围步长选择函数，在show_shift_distance，show_regress_trend_channel，
        show_skeleton_channel等涉及时间步长的函数中用来控制步长范围
        :param step_x: 时间步长控制参数，float
        :return: 最终输出被控制在2-len(self.tl), int
        """
        if step_x <= 0:
            # 不正常step_x规范到正常范围中
            #log_func(
            #    'input step_x={} is error, change to step_x=1'.format(step_x))
            step_x = 1
        # 如果需要调整更细的粒度，调整g_step_unit的值
        step = int(math.floor(len(self.tl) / g_step_unit / step_x))
        # 输出被控制在2-len(self.tl)
        step = len(self.tl) if step > len(self.tl) else step
        step = 2 if step < 2 else step
        return step

    def is_up_trend(self, up_deg_threshold=5):
        """
        判断走势是否符合上升走势：
        1. 判断走势是否可以使用一次拟合进行描述
        2. 如果可以使用1次拟合进行描述，计算一次拟合趋势角度
        3. 如果1次拟合趋势角度 >= up_deg_threshold判定上升
        :param up_deg_threshold: 判定一次拟合趋势角度为上升趋势的阀值角度，默认5
        :return: 是否上升趋势
        """
        valid = regression.valid_poly(self.tl, poly=1)
        if valid:
            deg = regression.calc_regress_deg(self.tl)
            if deg >= up_deg_threshold:
                return True
        return False

    def is_down_trend(self, down_deg_threshold=-5):
        """
        判断走势是否符合下降走势：
        1. 判断走势是否可以使用一次拟合进行描述
        2. 如果可以使用1次拟合进行描述，计算一次拟合趋势角度
        3. 如果1次拟合趋势角度 <= down_deg_threshold判定下降
        :param down_deg_threshold: 判定一次拟合趋势角度为下降趋势的阀值角度，默认－5
        :return: 是否下降趋势
        """
        valid = regression.valid_poly(self.tl, poly=1)
        if valid:
            deg = regression.calc_regress_deg(self.tl)
            if deg <= down_deg_threshold:
                return True
        return False