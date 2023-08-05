import sys, os
from IPython.display import clear_output
from IPython.display import display
from ipywidgets import FloatProgress

from ultron.kdutils.decorator import warnings_filter


class Progress(object):
    """单进程（主进程）进度显示控制类"""

    @warnings_filter
    def __init__(self, total, a_progress, label=None):
        """
        外部使用eg：
            progess = AbuProgress(stock_df.shape[0], 0, 'merging {}'.format(m))
            for i, symbol in enumerate(stock_df['symbol']):
                progess.show(i + 1)
        :param total: 总任务数量
        :param a_progress: 初始进度
        :param label: 进度显示label
        """
        self._total = total
        self._progress = a_progress
        self._label = label
        self.f = sys.stdout
        self.progress_widget = None

    def __enter__(self):
        """创建子进程做进度显示"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.write('\r')
        if self.progress_widget is not None:
            self.progress_widget.close()

    @property
    def progress(self):
        """property获取self._progress"""
        return self._progress

    @progress.setter
    def progress(self, a_progress):
        """progress.setter设置progress"""
        if a_progress > self._total:
            self._progress = self._total
        elif a_progress < 0:
            self._progress = 0
        else:
            self._progress = a_progress

    def show(self, a_progress=None, ext='', p_format="{}:{}:{}%"):
        """
        进行进度控制显示主方法
        :param ext: 可以添加额外的显示文字，str，默认空字符串
        :param a_progress: 默认None, 即使用类内部计算的迭代次数进行进度显示
        :param p_format: 进度显示格式，默认{}: {}%，即'self._label:round(self._progress / self._total * 100, 2))%'
        """
        self.progress = a_progress if a_progress is not None else self.progress + 1
        ps = round(self._progress / self._total * 100, 2)

        if self._label is not None:
            # 如果初始化label没有就只显示ui进度
            self.f.write('\r')
            self.f.write(p_format.format(self._label, ext, ps))

        if 'IS_IPYTHON' in os.environ and os.environ['IS_IPYTHON']:
            if self.progress_widget is None:
                self.progress_widget = FloatProgress(value=0, min=0, max=100)
                display(self.progress_widget)
            self.progress_widget.value = ps

        # 这样会出现余数结束的情况，还是尽量使用上下文管理器控制结束
        if self._progress == self._total:
            self.f.write('\r')
            if self.progress_widget is not None:
                self.progress_widget.close()
