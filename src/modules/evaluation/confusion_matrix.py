# ========================================================= #
# @Author: Fantasy_Silence                                  #
# @Time: 2024-04-22                                         #
# @IDE: Visual Studio Code & PyCharm                        #
# @Python: 3.9.7                                            #
# ========================================================= #
# @Description: Used for visualizing confusion matrices     #
# ========================================================= #
import warnings
import matplotlib
import seaborn as sns
from typing import Sequence
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

warnings.filterwarnings('ignore')
matplotlib.rcParams['font.sans-serif'] = ['STsong']
matplotlib.rcParams['axes.unicode_minus'] = False

from src.common.fileTool.figuresio import FiguresIO
from src.common.figTool.evaluateobjectbase import EvaluateObjectBase


class ConfusionMatrix(EvaluateObjectBase):
    
    """
    可视化混淆矩阵
    """

    def __init__(
            self, y_true: Sequence, y_pred: Sequence, label_map: list[str]=None,  
            is_show_alone: bool=True, is_show: bool=True, is_save: bool=False,
            ax: plt.Axes=None, fig_name: str=None
    ) -> None:
        
        """
        y_true: 真实值
        y_pred: 预测的类别
        label_map: 类别的名字
        is_show_alone: 是否显示于单独的画布上. 如果想单独显示，设置为True，
        如果想作为子图与其他图片一起显示，自行设置画布并将该参数设置为False
        is_show: 是否显示
        is_save: 是否以png格式保存图片，设置为True将保存于项目根路径下的figures文件夹中
        """

        super().__init__(
            ax=ax, fig_name=fig_name, is_show_alone=is_show_alone,
            is_show=is_show, is_save=is_save
        )

        self.y_true = y_true
        self.y_pred = y_pred
        self.label_map = label_map
        self.__draw__()
    

    def __draw__(self):

        if self.is_show_alone:
            _, self.ax = plt.subplots(
                nrows=1, ncols=1, figsize=(10, 8), dpi=80, facecolor="w"
            )
        clf_matrix = confusion_matrix(self.y_true, self.y_pred)
        print("Confusion Matrix:\n", clf_matrix)
        sns.heatmap(
            clf_matrix, annot=True, fmt=".1f", ax=self.ax,
            linewidths=.5, square = True, cmap = 'Blues',
            annot_kws={'size':14, 'weight':'bold'}
        )
        plt.title(
            'Accuracy Score: %.5f' %
            accuracy_score(self.y_true, self.y_pred), size=16
        )
        if self.label_map is not None:
            self.ax.set_xticklabels(self.label_map, fontsize=14)
            self.ax.set_yticklabels(self.label_map, fontsize=14)
        self.ax.set_ylabel('Actual label', fontsize=14)
        self.ax.set_xlabel('Predicted label', fontsize=14)
        plt.tight_layout()

        # ------ 存储图片 ------ #
        if self.is_save:
            if self.fig_name is not None:
                path = FiguresIO.getFigureSavePath(
                    "%s/%s Confusion Matrix.png" % 
                    (self.folder_name, self.fig_name)
                )
            else:
                path = FiguresIO.getFigureSavePath(
                    "%s/Confusion Matrix.png" % self.folder_name
                )
            plt.savefig(path, dpi=300)
        
        if self.is_show and self.is_show_alone:
            plt.show()
