# ========================================== #
# @Author: Fantasy_Silence                   #
# @Time: 2024-04-23                          #
# @IDE: Visual Studio Code & PyCharm         #
# @Python: 3.9.7                             #
# ========================================== #
# @Description: Used to draw PR curve        #
# ========================================== #
import numpy as np
from typing import Sequence
import matplotlib.pyplot as plt

from src.common.fileTool.figuresio import FiguresIO
from src.common.figTool.evaluateobjectbase import EvaluateObjectBase


class PRCurve(EvaluateObjectBase):
    """
    绘制PR曲线
    """

    def __init__(
        self, y_true: Sequence, y_score: Sequence, label: str = None,
        is_show_alone: bool = True, is_show: bool = True, is_save: bool = False,
        ax: plt.Axes = None, fig_name: str = None,
    ) -> None:
        
        """
        y_true: 真实值(二分类可能为0,1; 多分类可能为0,1,2,...)
        y_score: 预测值, 概率
        is_show_alone: 是否显示于单独的画布上. 如果想单独显示，设置为True，
        如果想作为子图与其他图片一起显示，自行设置画布并将该参数设置为False
        is_show: 是否显示
        is_save: 是否以png格式保存图片，设置为True将保存于项目根路径下的figures文件夹中
        """

        super().__init__(
            ax=ax, fig_name=fig_name,
            is_show_alone=is_show_alone, is_show=is_show, is_save=is_save,
        )

        self.label = label
        self.y_true = np.asarray(y_true, dtype=np.int64)
        self.y_score = np.asarray(y_score, dtype=np.float64)
        self.n_samples, self.n_class = self.y_score.shape
        if self.n_class > 2:
            # 对真实类别进行one-hot编码
            self.y_true = self.__label_one_hot__()  
        else:
            self.y_true = self.y_true.reshape(-1)
        self.draw()
    

    def draw(self) -> None:

        # ------ 计算PR ------ #
        pr_array = self.__cal_PR__()

        # ------ 可视化PR曲线 ------ #
        ap = (pr_array[1:, 0] - pr_array[:-1, 0]).dot(pr_array[1:, 1])
        if self.is_show_alone:
            fig, self.ax = plt.subplots(figsize=(12, 8), dpi=100, facecolor="w")
        if self.label is not None:
            self.ax.step(
                pr_array[:, 0], pr_array[:, 1], "-", 
                where="post", lw=2, label=self.label+", AP = %.3f"%ap
            )
        else:
            self.ax.step(
                pr_array[:, 0], pr_array[:, 1], "-", where="post", lw=2
            )
        self.ax.set_title("PR Curve(AP=%.5f)"%ap, fontdict={"fontsize":14})
        self.ax.set_xlabel("Recall", fontdict={"fontsize":12})
        self.ax.set_ylabel("Precision", fontdict={"fontsize":12})
        self.ax.grid(ls=":")
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1.05)
        plt.legend(frameon=True,fontsize=12,loc="lower right")
        plt.tight_layout()

        # ------ 存储图片 ------ #
        if self.is_save:
            if self.fig_name is not None:
                path = FiguresIO.getFigureSavePath(
                    "%s/%s PR Curve.png" % (self.folder_name, self.fig_name)
                )
            else:
                path = FiguresIO.getFigureSavePath(
                    "%s/PR Curve.png" % self.folder_name
                )
            plt.savefig(path, dpi=300)

        if self.is_show_alone and self.is_show:
            plt.show()


    def __cal_sub_metrics__(
            self, y_true_sort: Sequence, n: int
    ) -> tuple[int, int, int, int]:

        """
        计算TP，NP，FP，TN
        y_true_sort: 排序后的真实值类别
        n: 以第n个样本的概率为阀值
        """

        if self.n_class == 2:
            pre_label = np.r_[
                np.zeros(n, dtype=np.int64), 
                np.ones(self.n_samples - n, dtype=np.int64)
            ]
            # 真正例
            tp = len(pre_label[(pre_label == 0) & (pre_label == y_true_sort)]) 
            # 真反例
            tn = len(pre_label[(pre_label == 1) & (pre_label == y_true_sort)])
            fp = np.sum(y_true_sort) - tn       # 假正例
            fn = self.n_samples - tp - tn - fp  # 假反例
        else:
            pre_label = np.r_[
                np.ones(n, dtype=np.int64), 
                np.zeros(self.n_samples - n, dtype=np.int64)
            ]
            # 真正例
            tp = len(pre_label[(pre_label == 1) & (pre_label == y_true_sort)])
            # 真反例
            tn = len(pre_label[(pre_label == 0) & (pre_label == y_true_sort)])  
            fn = np.sum(y_true_sort) - tp       # 假正例
            fp = self.n_samples - tp - tn - fn  # 假反例

        return tp, tn, fn, fp


    @staticmethod
    def __sort_positive__(y_score: Sequence) -> np.ndarray[int]:

        """
        按照预测为正例的概率进行降序排序，并返回排序的索引向量
        """

        idx = np.argsort(y_score)[::-1]  # 降序排列
        return idx
    

    def __label_one_hot__(self) -> np.ndarray:

        """
        对真实类别标签进行one-hot编码，编码后的维度与模型预测概率维度相同
        """

        y_true_lab = np.zeros((self.n_samples, self.n_class))
        for i in range(self.n_samples):
            y_true_lab[i, self.y_true[i]] = 1
        return y_true_lab


    def __cal_PR__(self) -> np.ndarray:

        """
        计算PR
        """

        # 用于存储每个样本预测概率作为阀值时的P和R指标
        pr_array = np.zeros((self.n_samples, 2))   
        # 二分类   
        if self.n_class == 2:   
            idx = self.__sort_positive__(self.y_score[:, 0])
            # 真值类别标签按照排序索引进行排序
            y_true = self.y_true[idx]       
            # 针对每个样本，把预测概率作为阀值，计算P和R指标
            for i in range(self.n_samples):
                tp, tn, fn, fp = self.__cal_sub_metrics__(y_true, i + 1)
                pr_array[i,:] = tp / (tp + fn), tp / (tp + fp)
        # 多分类        
        else:   
            precision = np.zeros((self.n_samples, self.n_class))    # 查准率
            recall = np.zeros((self.n_samples, self.n_class))       # 查全率
            for k in range(self.n_class):
                # 针对每个类别，分别计算P，R指标，然后平均
                idx = self.__sort_positive__(self.y_score[:, k])
                # 真值类别第k列
                y_true_k = self.y_true[:, k]     
                # 真值类别第k列按照排序索引进行排序
                y_true = y_true_k[idx]       
                # 针对每个样本，把预测概率作为阀值，计算P和R指标
                for i in range(self.n_samples):
                    tp, tn, fn, fp = self.__cal_sub_metrics__(y_true, i + 1)
                    precision[i,k] = tp / (tp + fp)     # 查准率
                    recall[i,k] = tp / (tp + fn)       # 查全率
            # 宏查准率和宏查全率
            pr_array = np.array([
                np.mean(recall, axis=1), np.mean(precision, axis=1)
            ]).T
        return pr_array
