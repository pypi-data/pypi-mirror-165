# -*- encoding:utf-8 -*-
"""
    对各个依赖库不同版本，不同系统的规范进行统一以及问题修正模块
"""
import warnings
import sklearn
import numpy as np


def _parse_version(version_string):
    """
    根据库中的__version__字段，转换为tuple，eg. '1.11.3'->(1, 11, 3)
    :param version_string: __version__字符串对象
    :return: tuple 对象
    """
    version = []
    for x in version_string.split('.'):
        try:
            version.append(int(x))
        except ValueError:
            version.append(x)
    return tuple(version)


skl_version = _parse_version(sklearn.__version__)

try:
    import six as six
except ImportError:
    warnings.warn("not installed six")

try:
    from functools import partial
except ImportError:
    warnings.warn("not installed functools partial")

try:
    from six.moves import xrange
except ImportError:
    warnings.warn("not installed functools partial")

try:
    from inspect import signature, Parameter
except ImportError:
    try:
        from funcsigs import signature, Parameter
    except ImportError:
        warnings.warn("not installed funcsigs")

try:
    # noinspection all
    from six.moves import cPickle as pickle
except ImportError:
    # noinspection all
    from six.moves import cPickle as pickle

if six.PY3:
    # noinspection PyProtectedMember
    Unpickler = pickle._Unpickler
    # noinspection PyProtectedMember
    Pickler = pickle._Pickler
else:
    Unpickler = pickle.Unpickler
    Pickler = pickle.Pickler

if six.PY3:

    def as_bytes(s):
        if isinstance(s, bytes):
            return s
        return s.encode('latin1')
else:
    as_bytes = str

try:
    skl_ver_big = skl_version >= (0, 18, 0)
except:
    skl_ver_big = True

if skl_ver_big:
    mean_squared_error_scorer = 'neg_mean_squared_error'
    mean_absolute_error_scorer = 'neg_mean_absolute_error'
    median_absolute_error_scorer = 'neg_median_absolute_error'
    log_loss = 'neg_log_loss'

    try:
        from sklearn.model_selection import train_test_split
        from sklearn.model_selection import learning_curve
        from sklearn.model_selection import cross_val_score
        from sklearn.model_selection import GridSearchCV
        # noinspection PyPep8Naming
        from sklearn.mixture import GaussianMixture as GMM

        class KFold(object):
            """
                sklearn将KFold移动到了model_selection，而且改变了用法，暂时不需要
                这么复杂的功能，将sklearn中关键代码简单实现，不from sklearn.model_selection import KFold
            """

            def __init__(self, n, n_folds=3, shuffle=False, random_state=None):
                if abs(n - int(n)) >= np.finfo('f').eps:
                    raise ValueError("n must be an integer")
                self.n = int(n)

                if abs(n_folds - int(n_folds)) >= np.finfo('f').eps:
                    raise ValueError("n_folds must be an integer")
                self.n_folds = n_folds = int(n_folds)

                if n_folds <= 1:
                    raise ValueError(
                        "k-fold cross validation requires at least one"
                        " train / test split by setting n_folds=2 or more,"
                        " got n_folds={0}.".format(n_folds))
                if n_folds > self.n:
                    raise ValueError(
                        ("Cannot have number of folds n_folds={0} greater"
                         " than the number of samples: {1}.").format(
                             n_folds, n))

                if not isinstance(shuffle, bool):
                    raise TypeError("shuffle must be True or False;"
                                    " got {0}".format(shuffle))
                self.shuffle = shuffle
                self.random_state = random_state

                self.idxs = np.arange(n)
                if shuffle:
                    rng = check_random_state(self.random_state)
                    rng.shuffle(self.idxs)

            def __iter__(self):
                ind = np.arange(self.n)
                for test_index in self._iter_test_masks():
                    train_index = np.logical_not(test_index)
                    train_index = ind[train_index]
                    test_index = ind[test_index]
                    yield train_index, test_index

            def _iter_test_masks(self):
                for test_index in self._iter_test_indices():
                    test_mask = self._empty_mask()
                    test_mask[test_index] = True
                    yield test_mask

            def _empty_mask(self):
                return np.zeros(self.n, dtype=np.bool)

            def _iter_test_indices(self):
                n = self.n
                n_folds = self.n_folds
                fold_sizes = (n // n_folds) * np.ones(n_folds, dtype=np.int)
                fold_sizes[:n % n_folds] += 1
                current = 0
                for fold_size in fold_sizes:
                    start, stop = current, current + fold_size
                    yield self.idxs[start:stop]
                    current = stop

            def __repr__(self):
                return '%s.%s(n=%i, n_folds=%i, shuffle=%s, random_state=%s)' % (
                    self.__class__.__module__,
                    self.__class__.__name__,
                    self.n,
                    self.n_folds,
                    self.shuffle,
                    self.random_state,
                )

            def __len__(self):
                return self.n_folds

    except ImportError:
        from sklearn.cross_validation import train_test_split
        from sklearn.cross_validation import KFold
        from sklearn.cross_validation import cross_val_score
        from sklearn.learning_curve import learning_curve
        from sklearn import cross_validation
        from sklearn.grid_search import GridSearchCV
        from sklearn.mixture import GMM
else:
    mean_squared_error_scorer = 'mean_squared_error'
    mean_absolute_error_scorer = 'mean_absolute_error'
    median_absolute_error_scorer = 'median_absolute_error'
    log_loss = 'log_loss'

    # noinspection PyUnresolvedReferences, PyDeprecation
    from sklearn.cross_validation import train_test_split
    # noinspection PyUnresolvedReferences, PyDeprecation
    from sklearn.cross_validation import KFold
    # noinspection PyUnresolvedReferences, PyDeprecation
    from sklearn.cross_validation import cross_val_score
    # noinspection PyUnresolvedReferences, PyDeprecation
    from sklearn.learning_curve import learning_curve
    # noinspection PyUnresolvedReferences, PyDeprecation
    from sklearn import cross_validation
    # noinspection PyUnresolvedReferences, PyDeprecation
    from sklearn.grid_search import GridSearchCV
    # noinspection PyUnresolvedReferences, PyDeprecation
    from sklearn.mixture import GMM
