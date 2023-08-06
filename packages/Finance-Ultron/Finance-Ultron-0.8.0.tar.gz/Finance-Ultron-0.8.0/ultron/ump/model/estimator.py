# -*- encoding:utf-8 -*-
"""
中间层，从上层拿到x，y，df
拥有create estimator

"""
import functools
import pandas as pd
import numpy as np
from enum import Enum
from sklearn.preprocessing import label_binarize, StandardScaler, binarize
from ultron.ump.core.fixes import train_test_split, cross_val_score, mean_squared_error_scorer, six
from ultron.ump.core.fixes import six
from ultron.ump.core.fixes import mean_squared_error_scorer
from ultron.ump.model.creater import MLCreater


class _EMLScoreType(Enum):
    """针对有监督学习的度量支持enum"""
    """有监督学习度量准确率"""
    E_SCORE_ACCURACY = 'accuracy'
    """有监督学习度量mse"""
    E_SCORE_MSE = mean_squared_error_scorer
    """有监督学习度量roc_auc"""
    E_SCORE_ROC_AUC = 'roc_auc'


class EMLFitType(Enum):
    """支持常使用的学习器类别enum"""
    """有监督学习：自动选择，根据y的label数量，> 10使用回归否则使用分类"""
    E_FIT_AUTO = 'auto'
    """有监督学习：回归"""
    E_FIT_REG = 'reg'
    """有监督学习：分类"""
    E_FIT_CLF = 'clf'
    """无监督学习：HMM"""
    E_FIT_HMM = 'hmm'
    """无监督学习：PCA"""
    E_FIT_PCA = 'pca'
    """无监督学习：KMEAN"""
    E_FIT_KMEAN = 'kmean'


def entry_wrapper(support=(EMLFitType.E_FIT_CLF, EMLFitType.E_FIT_REG,
                           EMLFitType.E_FIT_HMM, EMLFitType.E_FIT_PCA,
                           EMLFitType.E_FIT_KMEAN)):
    """
    类装饰器函数，对关键字参数中的fiter_type进行标准化，eg，fiter_type参数是'clf'， 转换为EMLFitType(fiter_type)
    赋予self.fiter_type，检测当前使用的具体学习器不在support参数中不执行被装饰的func函数了，打个log返回

    :param support: 默认 support=(EMLFitType.E_FIT_CLF, EMLFitType.E_FIT_REG, EMLFitType.E_FIT_HMM,
                           EMLFitType.E_FIT_PCA, EMLFitType.E_FIT_KMEAN)
                    即支持所有，被装饰的函数根据自身特性选择装饰参数
    """

    def decorate(func):

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            org_fiter_type = self.fiter_type
            if 'fiter_type' in kwargs:
                # 如果传递了fiter_type参数，pop出来
                fiter_type = kwargs.pop('fiter_type')
                # 如果传递的fiter_type参数是str，eg：'clf'， 转换为EMLFitType(fiter_type)
                if isinstance(fiter_type, six.string_types):
                    fiter_type = EMLFitType(fiter_type)
                self.fiter_type = fiter_type

            check_support = self.fiter_type
            if self.fiter_type == EMLFitType.E_FIT_AUTO:
                # 把auto的归到具体的分类或者回归
                check_y = self.y
                if 'y' in kwargs:
                    check_y = kwargs['y']
                check_support = EMLFitType.E_FIT_CLF if len(
                    np.unique(check_y)) <= 10 else EMLFitType.E_FIT_REG
            if check_support not in support:
                # 当前使用的具体学习器不在support参数中不执行被装饰的func函数了，打个log返回
                self.log_func('{} not support {}!'.format(
                    func.__name__, check_support.value))
                # 如果没能成功执行把类型再切换回来
                self.fiter_type = org_fiter_type
                return

            return func(self, *args, **kwargs)

        return wrapper

    return decorate


class Estimator(object):
    """封装有简单学习及无监督学习方法以及相关操作类"""

    def __init__(self, x, y, df, fiter_type=EMLFitType.E_FIT_AUTO):
        """
        AbuML属于中间层需要所有原料都配齐，x, y, df，构造方式参考
        create_test_fiter方法中的实行流程

        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param df: 拆分x，y使用的pd.DataFrame对象
        :param fiter_type: 使用的学习器类型，默认使用E_FIT_AUTO即根据y的label数量选择分类或者回归
        """
        self.estimator = MLCreater()
        # 如果传递进来的是字符串类型，转换为EMLFitType
        if isinstance(fiter_type, six.string_types):
            fiter_type = EMLFitType(fiter_type)
        self.x = x
        self.y = y
        self.df = df
        # ipython notebook下使用logging.info
        self.log_func = print  #logging.info if ABuEnv.g_is_ipython else print
        self.fiter_type = fiter_type

    def is_supervised_learning(self):
        """
        返回self.fiter_type所使用的是有监督学习还是无监督学习
        :return: bool，True: 有监督，False: 无监督
        """
        return self.fiter_type == EMLFitType.E_FIT_REG or self.fiter_type == EMLFitType.E_FIT_CLF or \
            self.fiter_type == EMLFitType.E_FIT_AUTO

    def echo_info(self, fiter=None):
        """
        显示fiter class信息，self.df信息包括，head，tail，describe
        eg：
            fiter class is: DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=None,
                max_features=None, max_leaf_nodes=None,
                min_impurity_split=1e-07, min_samples_leaf=1,
                min_samples_split=2, min_weight_fraction_leaf=0.0,
                presort=False, random_state=None, splitter='best')
            describe:
                          y        x0        x1        x2        x3
            count  150.0000  150.0000  150.0000  150.0000  150.0000
            mean     1.0000    5.8433    3.0540    3.7587    1.1987
            std      0.8192    0.8281    0.4336    1.7644    0.7632
            min      0.0000    4.3000    2.0000    1.0000    0.1000
            25%      0.0000    5.1000    2.8000    1.6000    0.3000
            50%      1.0000    5.8000    3.0000    4.3500    1.3000
            75%      2.0000    6.4000    3.3000    5.1000    1.8000
            max      2.0000    7.9000    4.4000    6.9000    2.5000
        :param fiter:
        :return:
        """
        if fiter is None:
            fiter = self.get_fiter()
        self.log_func('fiter class is: {}'.format(fiter))
        self.log_func('describe:\n{}'.format(self.df.describe()))
        self.log_func('head:\n{}'.format(self.df.head()))
        self.log_func('tail:\n{}'.format(self.df.tail()))

    def get_fiter(self):
        """
        根据self.fiter_type的类型选择从self.estimator返回学习器对象

        self.fiter_type == EMLFitType.E_FIT_AUTO：
            自动选择有简单学习，当y的label数量 < 10个使用分类self.estimator.clf，否则回归self.estimator.reg
        self.fiter_type == EMLFitType.E_FIT_REG:
            使用有监督学习回归self.estimator.reg
        self.fiter_type == EMLFitType.E_FIT_CLF:
            使用有监督学习分类self.estimator.clf
        self.fiter_type == EMLFitType.E_FIT_HMM:
            使用无监督学习hmm，self.estimator.hmm
        self.fiter_type == EMLFitType.E_FIT_PCA:
            使用无监督学习pca，self.estimator.pca
        self.fiter_type == EMLFitType.E_FIT_KMEAN:
            使用无监督学习kmean，self.estimator.kmean
        :return: 返回学习器对象
        """
        if self.fiter_type == EMLFitType.E_FIT_AUTO:
            if len(np.unique(self.y)) <= 10:
                # 小于等于10个class的y就认为是要用分类了
                fiter = self.estimator.clf
            else:
                fiter = self.estimator.reg
        elif self.fiter_type == EMLFitType.E_FIT_REG:
            fiter = self.estimator.reg
        elif self.fiter_type == EMLFitType.E_FIT_CLF:
            fiter = self.estimator.clf
        elif self.fiter_type == EMLFitType.E_FIT_HMM:
            if self.estimator.hmm is None:
                self.estimator.hmm_gaussian()
            fiter = self.estimator.hmm
        elif self.fiter_type == EMLFitType.E_FIT_PCA:
            if self.estimator.pca is None:
                self.estimator.pca_decomposition()
            fiter = self.estimator.pca
        elif self.fiter_type == EMLFitType.E_FIT_KMEAN:
            if self.estimator.kmean is None:
                self.estimator.kmean_cluster()
            fiter = self.estimator.kmean
        else:
            raise TypeError('self.fiter_type = {}, is error type'.format(
                self.fiter_type))

        return fiter

    @entry_wrapper(support=(EMLFitType.E_FIT_CLF, ))
    def cross_val_accuracy_score(self, cv=10, **kwargs):
        """
        被装饰器entry_wrapper(support=(EMLFitType.E_FIT_CLF,))装饰，
        即只支持有监督学习分类，使用cross_val_score对数据进行accuracy度量
        :param cv: 透传cross_val_score的参数，默认10
        :param kwargs: 外部可以传递x, y, 通过
                                x = kwargs.pop('x', self.x)
                                y = kwargs.pop('y', self.y)
                       确定传递self._do_cross_val_score中参数x，y，
                       装饰器使用的fiter_type，eg：ttn_abu.cross_val_accuracy_score(fiter_type=ml.EMLFitType.E_FIT_CLF)
        :return: cross_val_score返回的score序列，
                 eg: array([ 1.  ,  0.9 ,  1.  ,  0.9 ,  1.  ,  0.9 ,  1.  ,  0.9 ,  0.95,  1.  ])
        """
        x = kwargs.pop('x', self.x)
        y = kwargs.pop('y', self.y)
        return self._do_cross_val_score(x, y, cv,
                                        _EMLScoreType.E_SCORE_ACCURACY.value)

    def _do_cross_val_score(self, x, y, cv, scoring):
        """
        封装sklearn中cross_val_score方法， 参数x, y, cv, scoring透传cross_val_score
        :param x: 训练集x矩阵，numpy矩阵
        :param y: 训练集y序列，numpy序列
        :param cv: 透传cross_val_score，cv参数，int
        :param scoring: 透传cross_val_score, 使用的度量方法
        :return: cross_val_score返回的score序列，
                 eg: array([ 1.  ,  0.9 ,  1.  ,  0.9 ,  1.  ,  0.9 ,  1.  ,  0.9 ,  0.95,  1.  ])
        """
        fiter = self.get_fiter()
        """
            eg: fiter
            DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=None,
                                    max_features=None, max_leaf_nodes=None,
                                    min_impurity_split=1e-07, min_samples_leaf=1,
                                    min_samples_split=2, min_weight_fraction_leaf=0.0,
                                    presort=False, random_state=None, splitter='best')
        """
        if scoring == _EMLScoreType.E_SCORE_ROC_AUC.value and len(
                np.unique(y)) != 2:
            # roc auc的度量下且y的label数量不是2项分类，首先使用label_binarize进行处理
            y_label_binarize = label_binarize(y, classes=np.unique(y))
            """
                eg：
                    np.unique(y) ＝ array([0, 1, 2])
                    y_label_binarize:
                    array([[1, 0, 0],
                           [1, 0, 0],
                           [1, 0, 0],
                           [1, 0, 0],
                           [1, 0, 0],
                           .........
                           [0, 1, 0],
                           [0, 1, 0],
                           [0, 1, 0],
                           [0, 1, 0],
                           [0, 1, 0],
                           [0, 1, 0],
                           [0, 1, 0],
                           [0, 1, 0],
                           .........
                           [0, 0, 1],
                           [0, 0, 1],
                           [0, 0, 1],
                           [0, 0, 1],
                           [0, 0, 1],
                           [0, 0, 1]])
            """
            label_cnt = len(np.unique(y))
            # one vs rest的score平均值的和
            mean_sum = 0
            # one vs rest中的最好score平均值
            best_mean = 0
            # 最好score平均值(best_mean)的score序列，做为结果返回
            scores = list()
            for ind in np.arange(0, label_cnt):
                # 开始 one vs rest
                _y = y_label_binarize[:, ind]
                """
                    eg: _y
                    array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                           1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                """
                tmp_scores = cross_val_score(fiter,
                                             x,
                                             _y,
                                             cv=cv,
                                             scoring=scoring)
                tmp_mean = np.mean(tmp_scores)
                # one vs rest的score平均值进行叠加sum
                mean_sum += tmp_mean
                if len(scores) == 0 or tmp_mean > best_mean:
                    scores = tmp_scores
            # one vs rest的score平均值的和 / label_cnt
            mean_sc = mean_sum / label_cnt
        else:
            scores = cross_val_score(fiter, x, y, cv=cv, scoring=scoring)
            # 计算度量的score平均值，做为log输出，结果返回的仍然是scores
            mean_sc = -np.mean(np.sqrt(-scores)) if scoring == mean_squared_error_scorer \
                else np.mean(scores)
        self.log_func('{} score mean: {}'.format(fiter.__class__.__name__,
                                                 mean_sc))

        return scores
