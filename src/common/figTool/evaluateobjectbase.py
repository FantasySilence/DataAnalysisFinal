# ========================================================================== #
# @Author: Fantasy_Silence                                                   #
# @Time: 2024-04-22                                                          #
# @IDE: Visual Studio Code & PyCharm                                         #
# @Python: 3.9.7                                                             #
# ========================================================================== #
# @Description: Object base class for Various model evaluation indicators    #
# ========================================================================== #
import os
import matplotlib.pyplot as plt

from src.common.fileTool.figuresio import FiguresIO


class EvaluateObjectBase:

    """
    这是一个对象基类，用于评估模型时进行参数初始化
    """

    def __init__(
            self, ax: plt.Axes=None, fig_name: str=None,
            is_show_alone: bool=True, is_show: bool=True, is_save: bool=False,
    ) -> None:
        
        # ------ 创建存放图片的文件夹 ------ #
        self.folder_name = "models_figures"
        data_folder = os.path.join(
            FiguresIO.getFigureSavePath(), self.folder_name
        )
        if not os.path.exists(data_folder):
            os.mkdir(data_folder)
        else:
            pass

        # ------ 绘图参数 ------ #
        self.is_show_alone = is_show_alone
        self.is_show = is_show
        self.is_save = is_save
        self.ax = ax
        self.fig_name = fig_name
        