# -*- encoding:utf-8 -*-
"""度量模块基础"""

import functools, logging
import numpy as np
import pandas as pd
import seaborn as sns
from ultron.factor.empyrical import stats
from ultron.kdutils import date as date_util
from ultron.kdutils import stats as stats_util
"""市场中1年交易日，默认250日"""
g_market_trade_year = 250


def valid_check(func):
    """检测度量的输入是否正常，非正常显示info，正常继续执行被装饰方法"""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.valid:
            return func(self, *args, **kwargs)
        else:
            logging.info('metrics input is invalid or zero order gen!')

    return wrapper


class Base(object):

    def __init__(self,
                 orders_pd,
                 action_pd,
                 capital,
                 benchmark,
                 enable_stocks_full_rate_factor=False):
        """
        :param orders_pd: 回测结果生成的交易订单构成的pd.DataFrame对象
        :param action_pd: 回测结果生成的交易行为构成的pd.DataFrame对象
        :param capital: 资金类AbuCapital实例化对象
        :param benchmark: 交易基准对象，AbuBenchmark实例对象
        :param enable_stocks_full_rate_factor: 是否开启满仓乘数
        """
        self.capital = capital
        self.orders_pd = orders_pd
        self.action_pd = action_pd
        self.benchmark = benchmark
        """
            满仓乘数，如果设置为True, 针对度量信息如收益等需要除self.stocks_full_rate_factor
        """
        self.enable_stocks_full_rate_factor = enable_stocks_full_rate_factor
        self.valid = False
        if self.orders_pd is not None and self.capital is not None and 'capital_blance' in self.capital.capital_pd:
            self.valid = True
        # ipython notebook下使用logging.info
        self.log_func = print  #logging.info if ABuEnv.g_is_ipython else print

    @valid_check
    def fit_metrics(self):
        """执行所有度量函数"""
        # TODO 根据ORDER数量大于一定阀值启动进度条
        # with AbuProgress(100, 0, label='metrics progress...') as pg:
        # pg.show(5)
        self._metrics_base_stats()
        # pg.show(50)
        self._metrics_sell_stats()
        # pg.show(80)
        self._metrics_action_stats()
        # pg.show(95)
        self._metrics_extend_stats()

    def fit_metrics_order(self):
        """对外接口，并非度量真实成交了的结果，只度量orders_pd，即不涉及资金的度量"""
        self._metrics_sell_stats()

    def _metrics_base_stats(self):
        """度量真实成交了的capital_pd，即涉及资金的度量"""
        # 平均资金利用率
        self.cash_utilization = 1 - (
            self.capital.capital_pd.cash_blance /
            self.capital.capital_pd.capital_blance).mean()

        # 默认不使用满仓乘数即stocks_full_rate_factor＝1
        self.stocks_full_rate_factor = 1
        if self.enable_stocks_full_rate_factor:
            # 计算满仓比例
            stocks_full_rate = (self.capital.capital_pd.stocks_blance /
                                self.capital.capital_pd.capital_blance)
            # 避免除0
            stocks_full_rate[stocks_full_rate == 0] = 1
            # 倒数得到满仓乘数
            self.stocks_full_rate_factor = (1 / stocks_full_rate)

        # 收益数据
        self.benchmark_returns = np.round(
            self.benchmark.kl_pd.close.pct_change(), 3)
        # 如果enable_stocks_full_rate_factor 则 * self.stocks_full_rate_factor的意义为随时都是满仓
        self.algorithm_returns = np.round(
            self.capital.capital_pd['capital_blance'].pct_change(),
            3) * self.stocks_full_rate_factor

        # 收益cum数据
        # noinspection PyTypeChecker
        self.algorithm_cum_returns = stats.cum_returns(self.algorithm_returns)
        self.benchmark_cum_returns = stats.cum_returns(self.benchmark_returns)

        # 最后一日的cum return
        self.benchmark_period_returns = self.benchmark_cum_returns[-1]
        self.algorithm_period_returns = self.algorithm_cum_returns[-1]

        # 交易天数
        self.num_trading_days = len(self.benchmark_returns)

        # 年化收益
        self.algorithm_annualized_returns = \
            (g_market_trade_year / self.num_trading_days) * self.algorithm_period_returns
        self.benchmark_annualized_returns = \
            (g_market_trade_year / self.num_trading_days) * self.benchmark_period_returns

        # 策略平均收益
        # noinspection PyUnresolvedReferences
        self.mean_algorithm_returns = self.algorithm_returns.cumsum(
        ) / np.arange(1, self.num_trading_days + 1, dtype=np.float64)
        # 波动率
        self.benchmark_volatility = stats.annual_volatility(
            self.benchmark_returns)
        # noinspection PyTypeChecker
        self.algorithm_volatility = stats.annual_volatility(
            self.algorithm_returns)

        # 夏普比率
        self.benchmark_sharpe = stats.sharpe_ratio(self.benchmark_returns)
        # noinspection PyTypeChecker
        self.algorithm_sharpe = stats.sharpe_ratio(self.algorithm_returns)

        # 信息比率
        # noinspection PyUnresolvedReferences
        self.information = stats.information_ratio(
            self.algorithm_returns.values, self.benchmark_returns.values)

        # 阿尔法, 贝塔
        # noinspection PyUnresolvedReferences
        self.alpha, self.beta = stats.alpha_beta_aligned(
            self.algorithm_returns.values, self.benchmark_returns.values)

        # 最大回撤
        # noinspection PyUnresolvedReferences
        self.max_drawdown = stats.max_drawdown(self.algorithm_returns.values)

    def _metrics_sell_stats(self):
        """并非度量真实成交了的结果，只度量orders_pd，即认为没有仓位管理和资金量限制前提下的表现"""
        # 根据order中的数据，计算盈利比例
        self.orders_pd['profit_cg'] = self.orders_pd['profit'] / (
            self.orders_pd['buy_price'] * self.orders_pd['buy_cnt'])
        # 为了显示方便及明显
        self.orders_pd['profit_cg_hunder'] = self.orders_pd['profit_cg'] * 100
        # 成交了的pd isin win or loss
        deal_pd = self.orders_pd[self.orders_pd['sell_type'].isin(
            ['win', 'loss'])]
        # 卖出原因get_dummies进行离散化
        dumm_sell = pd.get_dummies(deal_pd.sell_type_extra)
        dumm_sell_t = dumm_sell.T
        # 为plot_sell_factors函数生成卖出生效因子分布
        self.dumm_sell_t_sum = dumm_sell_t.sum(axis=1)

        # 买入因子唯一名称get_dummies进行离散化
        dumm_buy = pd.get_dummies(deal_pd.buy_factor)
        dumm_buy = dumm_buy.T
        # 为plot_buy_factors函数生成卖出生效因子分布
        self.dumm_buy_t_sum = dumm_buy.sum(axis=1)

        self.orders_pd['buy_date'] = self.orders_pd['buy_date'].astype(int)
        self.orders_pd[self.orders_pd['result'] != 0]['sell_date'].astype(
            int, copy=False)
        # 因子的单子的持股时间长度计算
        self.orders_pd['keep_days'] = self.orders_pd.apply(
            lambda x: date_util.diff(
                x['buy_date'],
                date_util.current_date_int()
                if x['result'] == 0 else x['sell_date']),
            axis=1)
        # 筛出已经成交了的单子
        self.order_has_ret = self.orders_pd[self.orders_pd['result'] != 0]

        # 筛出未成交的单子
        self.order_keep = self.orders_pd[self.orders_pd['result'] == 0]

        xt = self.order_has_ret.result.value_counts()
        # 计算胜率
        if xt.shape[0] == 2:
            win_rate = xt[1] / xt.sum()
        elif xt.shape[0] == 1:
            win_rate = xt.index[0]
        else:
            win_rate = 0
        self.win_rate = win_rate
        # 策略持股天数平均值
        self.keep_days_mean = self.orders_pd['keep_days'].mean()
        # 策略持股天数中位数
        self.keep_days_median = self.orders_pd['keep_days'].median()

        # 策略期望收益
        self.gains_mean = self.order_has_ret[
            self.order_has_ret['profit_cg'] > 0].profit_cg.mean()
        if np.isnan(self.gains_mean):
            self.gains_mean = 0.0
        # 策略期望亏损
        self.losses_mean = self.order_has_ret[
            self.order_has_ret['profit_cg'] < 0].profit_cg.mean()
        if np.isnan(self.losses_mean):
            self.losses_mean = 0.0

        # 忽略仓位控的前提下，即假设每一笔交易使用相同的资金，策略的总获利交易获利比例和
        profit_cg_win_sum = self.order_has_ret[
            self.order_has_ret['profit_cg'] > 0].profit.sum()
        # 忽略仓位控的前提下，即假设每一笔交易使用相同的资金，策略的总亏损交易亏损比例和
        profit_cg_loss_sum = self.order_has_ret[
            self.order_has_ret['profit_cg'] < 0].profit.sum()

        if profit_cg_win_sum * profit_cg_loss_sum == 0 and profit_cg_win_sum + profit_cg_loss_sum > 0:
            # 其中有一个是0的，要转换成一个最小统计单位计算盈亏比，否则不需要
            if profit_cg_win_sum == 0:
                profit_cg_win_sum = 0.01
            if profit_cg_loss_sum == 0:
                profit_cg_win_sum = 0.01

        #  忽略仓位控的前提下，计算盈亏比
        self.win_loss_profit_rate = 0 if profit_cg_loss_sum == 0 else -round(
            profit_cg_win_sum / profit_cg_loss_sum, 4)
        #  忽略仓位控的前提下，计算所有交易单的盈亏总会
        self.all_profit = self.order_has_ret['profit'].sum()

    def _metrics_action_stats(self):
        """度量真实成交了的action_pd 计算买入资金的分布平均性，及是否有良好的分布"""
        action_pd = self.action_pd
        # 只选生效的, 由于忽略非交易日, 大概有多出0.6的误差
        self.act_buy = action_pd[action_pd.action.isin(['buy'])
                                 & action_pd.deal.isin([True])]
        # drop重复的日期上的行为，只保留一个，cp_date形如下所示
        cp_date = self.act_buy['Date'].drop_duplicates()
        """
            cp_date
            0      20141024
            2      20141029
            20     20150127
            21     20150205
            23     20150213
            25     20150218
            31     20150310
            34     20150401
            36     20150409
            39     20150422
            41     20150423
            44     20150428
            58     20150609
            59     20150610
            63     20150624
            66     20150715
            67     20150717
        """
        dt_fmt = cp_date.apply(
            lambda order: date_util.str_to_datetime(str(order), '%Y%m%d'))
        dt_fmt = dt_fmt.apply(lambda order: (order - dt_fmt.iloc[0]).days)
        # 前后两两生效交易时间相减
        self.diff_dt = dt_fmt - dt_fmt.shift(1)
        # 计算平均生效间隔时间
        self.effect_mean_day = self.diff_dt.mean()

        if self.act_buy.empty:
            self.act_buy['cost'] = 0
            self.cost_stats = 0
            self.buy_deal_rate = 0
        else:
            self.act_buy['cost'] = self.act_buy.apply(
                lambda order: order.Price * order.Cnt, axis=1)
            # 计算cost各种统计度量值
            self.cost_stats = stats_util.stats_namedtuple(self.act_buy['cost'])

            buy_action_pd = action_pd[action_pd['action'] == 'buy']
            buy_action_pd_deal = buy_action_pd['deal']
            # 计算资金对应的成交比例
            self.buy_deal_rate = buy_action_pd_deal.sum(
            ) / buy_action_pd_deal.count()

    def _metrics_extend_stats(self):
        """子类可扩展的metrics方法，子类在此方法中可定义自己需要度量的值"""
        pass