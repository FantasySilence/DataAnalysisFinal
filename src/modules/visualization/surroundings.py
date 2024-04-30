# ======================================================================= #
# @Author: Fantasy_Silence                                                #
# @Time: 2024-04-30                                                       #
# @IDE: Visual Studio Code & PyCharm                                      #
# @Python: 3.9.7                                                          #
# ======================================================================= #
# @Description: Draw the infrastructure situation around the house        #
# ======================================================================= #
import matplotlib
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

from src.common.infoTool.const import CONST_TABLE
from src.common.fileTool.figuresio import FiguresIO
from src.common.figTool.plotobjectbase import PlotObjectBase


class DrawHouseSurroundings(PlotObjectBase):
    
    def __init__(self, city: str = None) -> None:
        super().__init__(city)


    def draw(
        self, is_show: bool=True, is_save: bool=False, 
        is_show_alone: bool=True, axes: np.ndarray[Axes]=None
    ) -> None:
        
        """
        房间周围基础设施
        is_show：是否显示
        is_show_alone：是否显示于单独的画布上. 如果想单独显示，设置为True，如果想作为子图
                       与其他图片一起显示，自行设置画布(至少2x2)并将该参数设置为False
        is_save：是否以png格式保存图片，设置为True将保存于项目根路径下的figures文件夹中
        """

        if self.data is None:
            print("ERROR: 房子周围基础设施情况绘制失败, 没有该城市的数据集...")
            return
        if is_show_alone:
            _, axes = plt.subplots(
                nrows=2, ncols=2, figsize=(16, 16), dpi=100, facecolor="w"
            )

        # ------ 绘制周围公交站数量 ------ #
        sns.countplot(x="busAround", data=self.data, ax=axes[0, 0])
        axes[0, 0].set_title("周围公交站情况", fontsize=16)
        axes[0, 0].set_xlabel("公交站数量", fontsize=12)
        axes[0, 0].set_ylabel("样本数量", fontsize=12)

        # ------ 绘制周围学校数量 ------ #
        sns.countplot(x="schoolAround", data=self.data, ax=axes[0, 1])
        axes[0, 1].set_title("周围学校情况", fontsize=16)
        axes[0, 1].set_xlabel("学校数量", fontsize=12)
        axes[0, 1].set_ylabel("样本数量", fontsize=12)

        # ------ 绘制周围公园数量 ------ #
        sns.countplot(x="parkAround", data=self.data, ax=axes[1, 0])
        axes[1, 0].set_title("周围公园情况", fontsize=16)
        axes[1, 0].set_xlabel("公园数量", fontsize=12)
        axes[1, 0].set_ylabel("样本数量", fontsize=12)

        # ------ 绘制周围购物商场数量 ------ #
        sns.countplot(x="shopping_mallAround", data=self.data, ax=axes[1, 1])
        axes[1, 1].set_title("周围购物商场情况", fontsize=16)
        axes[1, 1].set_xlabel("购物商场数量", fontsize=12)
        axes[1, 1].set_ylabel("样本数量", fontsize=12)

        plt.suptitle(
            "房子周围基础设施情况\n——基于%s58二手房数据" % CONST_TABLE["CITY"][self.city], 
            fontsize=20
        )
        plt.subplots_adjust(top=0.9)
        plt.tight_layout()
        if is_save:
            path = FiguresIO.getFigureSavePath(
                "%s/%s_Visualize_HouseSurroundings.png" % 
                (self.folder_name, self.city)
            )
            plt.savefig(path, dpi=300)
        if is_show_alone and is_show:
            plt.show()
