# ========================================== #
# @Author: Fantasy_Silence                   #
# @Time: 2024-04-23                          #
# @IDE: Visual Studio Code & PyCharm         #
# @Python: 3.9.7                             #
# ========================================== #
# @Description: Used to draw PR curve        #
# ========================================== #
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from typing import Literal, Sequence
from sklearn.preprocessing import label_binarize
from sklearn.metrics import f1_score, precision_recall_curve

matplotlib.rcParams['font.sans-serif'] = ['STsong']
matplotlib.rcParams['axes.unicode_minus'] = False

from src.common.fileTool.figuresio import FiguresIO
from src.common.figTool.evaluateobjectbase import EvaluateObjectBase


class PRCurve(EvaluateObjectBase):
    
    """
    TODO: 实现寻找最佳的Precision和Recall
    绘制PR曲线
    """

    def __init__(
            self, y_true: Sequence, y_score: Sequence,
            is_show_alone: bool=True, is_show: bool=True, is_save: bool=False,
            ax: plt.Axes=None, fig_name: str=None, label: str=None,
            avg_method: Literal["macro", "micro"]="macro"
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
            ax=ax, fig_name=fig_name, is_show_alone=is_show_alone,
            is_show=is_show, is_save=is_save
        )

        self.y_true = np.asarray(y_true, dtype=np.int64)
        self.y_score = np.asarray(y_score, dtype=np.float64)
        self.label = label  
        self.avg_method = avg_method
        self.n_samples, self.n_class = self.y_score.shape
        self.draw()


    def draw(self) -> None:

        # ------ 微平均 ------ #
        if self.avg_method == "micro":

            # 合并所有类的预测概率和真实标签
            y_pred = np.argmax(self.y_score, axis=1)
            f1_scores = f1_score(self.y_true, y_pred, average="micro")
            self.y_true = label_binarize(self.y_true, classes=np.unique(self.y_true)).ravel()
            self.y_score = self.y_score.ravel()

            # 计算Precision, Recall, Thresholds
            precision, recall, thresholds = precision_recall_curve(self.y_true, self.y_score)

            # 绘制Precision和Recall随Thresholds变化的曲线
            if self.is_show_alone:
                _, self.ax = plt.subplots(figsize=(12, 8), dpi=100, facecolor="w")
            if self.label is not None:
                self.ax.plot(
                    thresholds, precision[:-1], 'b--', 
                    label='%s Precision(F1_score: %.4f)' % (self.label, f1_scores)
                )
                self.ax.plot(
                    thresholds, recall[:-1], 'g-', 
                    label='%s Recall(F1_score: %.4f)' % (self.label, f1_scores)
                )
            else:
                self.ax.plot(
                    thresholds, precision[:-1], 'b--', 
                    label='Precision(F1_score: %.4f)' % f1_scores
                )
                self.ax.plot(
                    thresholds, recall[:-1], 'g-', 
                    label='Recall(F1_score: %.4f)' % f1_scores
                )
            self.ax.set_xlabel('Thresholds', fontsize=14)
            self.ax.set_ylabel('Precision/Recall', fontsize=14)
            self.ax.set_title('PR Curve', fontsize=16)
            self.ax.grid(":")
            self.ax.legend(loc='best')
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1.05)

        # ------ 宏平均 ------ #
        elif self.avg_method == "macro":
            y_pred = np.argmax(self.y_score, axis=1)
            f1_scores = f1_score(self.y_true, y_pred, average="macro")
            precision_avg, recall_avg = [], []

            # 遍历每个类别，计算Precision和Recall
            for i in range(self.n_class):
                precision, recall, thresholds = precision_recall_curve(self.y_true == i, self.y_score[:, i])
                precision_avg.append(np.interp(np.linspace(0, 1, 100), thresholds, precision[:-1]))
                recall_avg.append(np.interp(np.linspace(0, 1, 100), thresholds, recall[:-1]))
            
            # 计算宏平均Precision和Recall
            precision_macro = np.mean(precision_avg, axis=0)
            recall_macro = np.mean(recall_avg, axis=0)
            thresholds_macro = np.linspace(0, 1, 100)
            
            # 绘制Precision和Recall随Thresholds变化的曲线
            if self.is_show_alone:
                _, self.ax = plt.subplots(figsize=(12, 8), dpi=100, facecolor="w")
            if self.label is not None:
                self.ax.plot(
                    thresholds_macro, precision_macro, 'b--', 
                    label='%s Precision(F1_score: %.4f)' % (self.label, f1_scores)
                )
                self.ax.plot(
                    thresholds_macro, recall_macro, 'g-', 
                    label='%s Recall(F1_score: %.4f)' % (self.label, f1_scores)
                )
            else:
                self.ax.plot(
                    thresholds_macro, precision_macro, 'b--', 
                    label='Precision(F1_score: %.4f)' % f1_scores
                )
                self.ax.plot(
                    thresholds_macro, recall_macro, 'g-', 
                    label='Recall(F1_score: %.4f)' % f1_scores
                )
            self.ax.set_xlabel('Thresholds', fontsize=14)
            self.ax.set_ylabel('Precision/Recall', fontsize=14)
            self.ax.set_title('PR Curve', fontsize=16)
            self.ax.grid(":")
            self.ax.legend(loc='best')
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1.05)

        else:
            raise ValueError("avg_method must be 'micro' or 'macro'")
        
        # ------ 存储图片 ------ #
        if self.is_save:
            if self.fig_name is not None:
                path = FiguresIO.getFigureSavePath(
                    "%s/%s PR Curve.png" % 
                    (self.folder_name, self.fig_name)
                )
            else:
                path = FiguresIO.getFigureSavePath(
                    "%s/PR Curve.png" % self.folder_name
                )
            plt.savefig(path, dpi=300)
        
        if self.is_show and self.is_show_alone:
            plt.show()
