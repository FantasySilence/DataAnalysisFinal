# ======================================================= #
# @Author: Fantasy_Silence                                #
# @Time: 2024-04-30                                       #
# @IDE: Visual Studio Code & PyCharm                      #
# @Python: 3.9.7                                          #
# ======================================================= #
# @Description: Draw other features of the house          #
# ======================================================= #
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


class DrawHouseOtherFeature(PlotObjectBase):
    
    def __init__(self, city: str = None) -> None:
        super().__init__(city)


    def draw(
        self, is_show: bool=True, is_save: bool=False, 
        is_show_alone: bool=True, axes: np.ndarray[Axes]=None
    ) -> None:
        
        """
        房子的其他特征
        is_show：是否显示
        is_show_alone：是否显示于单独的画布上. 如果想单独显示，设置为True，如果想作为子图
                       与其他图片一起显示，自行设置画布(至少1x3)并将该参数设置为False
        is_save：是否以png格式保存图片，设置为True将保存于项目根路径下的figures文件夹中
        """

        if self.data is None:
            print("ERROR: 房子的其他特征绘制失败, 没有该城市的数据集...")
            return
        if is_show_alone:
            _, axes = plt.subplots(
                nrows=2, ncols=3, figsize=(24, 16), dpi=80, facecolor="w"
            )
        
        # ------ 绘制楼层分布 ------ #
        sns.countplot(x='houseFloorType', data=self.data, ax=axes[0, 0])
        axes[0, 0].set_title("楼层分布", fontsize=16)
        axes[0, 0].set_xlabel("楼层类型", fontsize=12)
        axes[0, 0].set_ylabel("样本数量", fontsize=12)

        # ------ 绘制房屋朝向分布 ------ #
        sns.countplot(x='houseOrientation', data=self.data, ax=axes[0, 1])
        axes[0, 1].set_title("房屋朝向分布", fontsize=16)
        axes[0, 1].set_xlabel("朝向", fontsize=12)
        axes[0, 1].set_ylabel("样本数量", fontsize=12)

        # ------ 绘制房本年限分布 ------ #
        sns.countplot(x='houseHousingPeriod', data=self.data, ax=axes[0, 2])
        axes[0, 2].set_title("房本年限分布", fontsize=16)
        axes[0, 2].set_xlabel("房本年限", fontsize=12)
        axes[0, 2].set_ylabel("样本数量", fontsize=12)

        # ------ 绘制房子面积分布 ------ #
        sns.histplot(x='houseArea', data=self.data, ax=axes[1, 0], kde=True)
        axes[1, 0].set_title("房子面积分布", fontsize=16)
        axes[1, 0].set_xlabel("面积", fontsize=12)
        axes[1, 0].set_ylabel("样本数量", fontsize=12)

        # ------ 绘制房龄分布 ------ #
        sns.histplot(x='houseAge', data=self.data, ax=axes[1, 1], kde=True)
        axes[1, 1].set_title("房子年龄分布", fontsize=16)
        axes[1, 1].set_xlabel("年龄", fontsize=12)
        axes[1, 1].set_ylabel("样本数量", fontsize=12)

        # ------ 绘制楼层总数分布 ------ #
        sns.histplot(x='houseFloorSum', data=self.data, ax=axes[1, 2], kde=True)
        axes[1, 2].set_title("楼层总数分布", fontsize=16)
        axes[1, 2].set_xlabel("楼层总数", fontsize=12)
        axes[1, 2].set_ylabel("样本数量", fontsize=12)

        plt.suptitle(
            "房子其他特征\n——基于%s58二手房数据" % CONST_TABLE["CITY"][self.city], 
            fontsize=20
        )
        plt.subplots_adjust(top=0.9)
        plt.tight_layout()
        if is_save:
            path = FiguresIO.getFigureSavePath(
                "%s/%s_Visualize_OtherFeature.png" % 
                (self.folder_name, self.city)
            )
            plt.savefig(path, dpi=300)
        if is_show_alone and is_show:
            plt.show()
