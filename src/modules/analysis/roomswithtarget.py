# =============================================================== #
# @Author: Fantasy_Silence                                        #
# @Time: 2024-04-30                                               #
# @IDE: Visual Studio Code & PyCharm                              #
# @Python: 3.9.7                                                  #
# =============================================================== #
# @Description: Draw the relationship between the interior        #  
# characteristics of the room and the price per square meter      #
# =============================================================== #
import matplotlib
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

from src.common.fileTool.figuresio import FiguresIO
from src.common.figTool.plotobjectbase import PlotObjectBase


class DrawRoomWithTarget(PlotObjectBase):
    
    def __init__(self, city: str = None) -> None:
        super().__init__(city)


    def draw(
        self, is_show: bool=True, is_save: bool=False, 
        is_show_alone: bool=True, axes: np.ndarray[Axes]=None
    ) -> None:
        
        """
        房子内部房间与目标变量之间的关系
        is_show：是否显示
        is_show_alone：是否显示于单独的画布上. 如果想单独显示，设置为True，如果想作为子图
                       与其他图片一起显示，自行设置画布(至少1x3)并将该参数设置为False
        is_save：是否以png格式保存图片，设置为True将保存于项目根路径下的figures文件夹中
        """

        if self.data is None:
            print("ERROR: 房子内部房间与目标变量之间的关系绘制失败, 没有该城市的数据集...")
            return
        if is_show_alone:
            _, axes = plt.subplots(
                nrows=1, ncols=3, figsize=(24, 8), dpi=80, facecolor="w"
            )
        
        # ------ 绘制房间卧室与每平方米价格之间的箱线图 ------ #
        sns.boxplot(x="houseBedroom", y="unitPrice", data=self.data, ax=axes[0])
        axes[0].set_title("房间卧室与每平方米价格", fontsize=16)
        axes[0].set_xlabel('卧室的数量', fontsize=12)
        axes[0].set_ylabel('每平方米价格', fontsize=12)

        # ------ 绘制房间卫生间与每平方米价格之间的箱线图 ------ #
        sns.boxplot(x="houseBathroom", y="unitPrice", data=self.data, ax=axes[1])
        axes[1].set_title("房间卫生间与每平方米价格", fontsize=16)
        axes[1].set_xlabel('卫生间的数量', fontsize=12)
        axes[1].set_ylabel('每平方米价格', fontsize=12)

        # ------ 绘制房间客厅与每平方米价格之间的箱线图 ------ #
        sns.boxplot(x="houseLivingRoom", y="unitPrice", data=self.data, ax=axes[2])
        axes[2].set_title("房间客厅与每平方米价格", fontsize=16)
        axes[2].set_xlabel('客厅的数量', fontsize=12)
        axes[2].set_ylabel('每平方米价格', fontsize=12)

        plt.tight_layout()
        if is_save:
            path = FiguresIO.getFigureSavePath(
                "%s/%s_Analysis_RoomsWithTarget.png" % 
                (self.folder_name, self.city)
            )
            plt.savefig(path, dpi=300)
        if is_show_alone and is_show:
            plt.show()
