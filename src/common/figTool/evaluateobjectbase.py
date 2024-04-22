# ========================================================================== #
# @Author: Fantasy_Silence                                                   #
# @Time: 2024-04-22                                                          #
# @IDE: Visual Studio Code & PyCharm                                         #
# @Python: 3.9.7                                                             #
# ========================================================================== #
# @Description: Object base class for Various model evaluation indicators    #
# ========================================================================== #
import os

from src.common.fileTool.figuresio import FiguresIO


class EvaluateObjectBase:

    """
    这是一个对象基类，用于评估模型时进行参数初始化
    """

    def __init__(self) -> None:
        
        # ------ 创建存放图片的文件夹 ------ #
        self.folder_name = "models_figures"
        data_folder = os.path.join(
            FiguresIO.getFigureSavePath(), self.folder_name
        )
        if not os.path.exists(data_folder):
            os.mkdir(data_folder)
        else:
            pass
    