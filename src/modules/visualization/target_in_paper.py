# ======================================================================== #
# @Author: Fantasy_Silence                                                 #
# @Time: 2024-05-31                                                        #
# @IDE: Visual Studio Code & PyCharm                                       #
# @Python: 3.9.7                                                           #
# ======================================================================== #
# @Description: Visualize the distribution of objectives in the paper      #
# ======================================================================== #
import os
import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

from src.common.fileTool.filesio import FilesIO
from src.common.fileTool.figuresio import FiguresIO


class DrawTargetInPaper:
    
    @staticmethod
    def draw(is_show: bool=True, is_save: bool=False):

        """
        绘制论文中提到的目标变量的分布
        """

        # ------ 读取数据 ------ #
        data = pd.read_csv(FilesIO.getDataset(
            "house-prices-advanced-regression-techniques/train.csv"
        ))

        # ------ 绘制图像 ------ #
        _, ax = plt.subplots(1, 2, figsize=(20, 8), dpi=100)
        # 原始数据
        sns.histplot(
            data["SalePrice"], ax=ax[0], kde=True,
        )
        ax[0].set_title("Original data", fontsize=16)
        # 处理后(取对数)的数据
        sns.histplot(
            data["SalePrice"].apply(lambda x: np.log(x)), ax=ax[1], kde=True
        )
        ax[1].set_title("Transformed data", fontsize=16)
        plt.tight_layout()

        # ------ 创建存放图片的文件夹 ------ #
        folder_name = "paper_figures"
        data_folder = os.path.join(
            FiguresIO.getFigureSavePath(), folder_name
        )
        if not os.path.exists(data_folder):
            os.mkdir(data_folder)
        else:
            pass

        # ------ 是否保存图片 ------ #
        if is_save:
            path = FiguresIO.getFigureSavePath("paper_figures/target_in_paper.png")
            plt.savefig(path, dpi=300)

        # ------ 是否显示图片 ------ #        
        if is_show:
            plt.show()
        