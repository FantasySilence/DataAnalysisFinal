# ======================================================= #
# @Author: Fantasy_Silence                                #
# @Time: 2024-04-22                                       #
# @IDE: Visual Studio Code & PyCharm                      #
# @Python: 3.9.7                                          #
# ======================================================= #
# @Description: Used to visualize feature importance      #
# ======================================================= #
import matplotlib
import pandas as pd
from typing import Sequence
import matplotlib.pyplot as plt

matplotlib.rcParams['font.sans-serif'] = ['STsong']
matplotlib.rcParams['axes.unicode_minus'] = False

from src.common.fileTool.figuresio import FiguresIO
from src.common.figTool.evaluateobjectbase import EvaluateObjectBase


class FeatureImportance(EvaluateObjectBase):

    """
    可视化特征重要性
    """

    def __init__(
            self, importances: Sequence, feature_names: Sequence,
            is_show_alone: bool=True, is_show: bool=True, is_save: bool=False,
            ax: plt.Axes=None, fig_name: str=None
    ) -> None:
        
        """
        importances: 特征重要性
        feature_name: 特征名称，用于绘图
        is_show_alone: 是否显示于单独的画布上. 如果想单独显示，设置为True，
        如果想作为子图与其他图片一起显示，自行设置画布并将该参数设置为False
        is_show: 是否显示
        is_save: 是否以png格式保存图片，设置为True将保存于项目根路径下的figures文件夹中
        """

        super().__init__(
            ax=ax, fig_name=fig_name, is_show_alone=is_show_alone,
            is_show=is_show, is_save=is_save
        )

        self.importances = importances
        self.feature_names = feature_names
        self.__draw__()
    
    
    def __draw__(self):

        if self.is_show_alone:
            _, self.ax = plt.subplots(
                nrows=1, ncols=1, figsize=(12, 8), dpi=80, facecolor="w"
            )
        weights = pd.Series(self.importances, index=self.feature_names)
        weights.sort_values()[-15:].plot(kind = 'barh', ax=self.ax)
        self.ax.set_title('Feature Importance', fontsize=16)
        self.ax.set_xlabel('Relative Importance', fontsize=14)
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        plt.tight_layout()

        # ------ 存储图片 ------ #
        if self.is_save:
            if self.fig_name is not None:
                path = FiguresIO.getFigureSavePath(
                    "%s/%s Feature Importances.png" % 
                    (self.folder_name, self.fig_name)
                )
            else:
                path = FiguresIO.getFigureSavePath(
                    "%s/Feature Importances.png" % self.folder_name
                )
            plt.savefig(path, dpi=300)
        
        if self.is_show and self.is_show_alone:
            plt.show()
