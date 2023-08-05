# -*- encoding:utf-8 -*-
"""
    全局环境配置模块
"""

from enum import Enum


# TODO 缩短 E_MARKET_TARGET_US－>US
class EMarketTargetType(Enum):
    """
        交易品种类型，即市场类型，
        eg. 美股市场, A股市场, 港股市场, 国内期货市场,
            美股期权市场, TC币市场（比特币等
    """
    """美股市场"""
    E_MARKET_TARGET_US = 'us'
    """A股市场"""
    E_MARKET_TARGET_CN = 'hs'
    """港股市场"""
    E_MARKET_TARGET_HK = 'hk'
    """国内期货市场"""
    E_MARKET_TARGET_FUTURES_CN = 'futures_cn'
    """国际期货市场"""
    E_MARKET_TARGET_FUTURES_GLOBAL = 'futures_global'
    """美股期权市场"""
    E_MARKET_TARGET_OPTIONS_US = 'options_us'
    """TC币市场（比特币等）"""
    E_MARKET_TARGET_TC = 'tc'


class EMarketSubType(Enum):
    """
        子市场（交易所）类型定义
    """
    """美股纽交所NYSE"""
    US_N = 'NYSE'
    """美股纳斯达克NASDAQ"""
    US_OQ = 'NASDAQ'
    """美股粉单市场"""
    US_PINK = 'PINK'
    """美股OTCMKTS"""
    US_OTC = 'OTCMKTS'
    """美国证券交易所"""
    US_AMEX = 'AMEX'
    """未上市"""
    US_PREIPO = 'PREIPO'
    """港股hk"""
    HK = 'hk'
    """上证交易所sh"""
    SH = 'sh'
    """深圳交易所sz"""
    SZ = 'sz'
    """大连商品交易所DCE'"""
    DCE = 'DCE'
    """郑州商品交易所ZZCE'"""
    ZZCE = 'ZZCE'
    """上海期货交易所SHFE'"""
    SHFE = 'SHFE'
    """伦敦金属交易所"""
    LME = 'LME'
    """芝加哥商品交易所"""
    CBOT = 'CBOT'
    """纽约商品交易所"""
    NYMEX = 'NYMEX'
    """币类子市场COIN'"""
    COIN = 'COIN'


"""切换目标操作市场，美股，A股，港股，期货，比特币等，默认美股市场"""
g_market_target = EMarketTargetType.E_MARKET_TARGET_US