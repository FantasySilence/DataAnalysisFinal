# ===================================================================== #
# @Author: Fantasy_Silence                                              #
# @Time: 2024-04-30                                                     #
# @IDE: Visual Studio Code & PyCharm                                    #
# @Python: 3.9.7                                                        #
# ===================================================================== #
# @Description: Draw the distribution of subway around the house        #
# ===================================================================== #
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

from src.common.infoTool.const import CONST_TABLE
from src.common.fileTool.figuresio import FiguresIO
from src.common.figTool.plotobjectbase import PlotObjectBase


class DrawHouseSubway(PlotObjectBase):
    
    def __init__(self, city: str = None) -> None:
        super().__init__(city)


    def draw(
        self, is_show: bool=True, is_save: bool=False, 
        is_show_alone: bool=True, ax: Axes=None
    ) -> None:
        
        """
        房子周围地铁站
        is_show：是否显示
        is_show_alone：是否显示于单独的画布上. 如果想单独显示，设置为True，如果想作为子图
                       与其他图片一起显示，自行设置画布(至少1x1)并将该参数设置为False
        is_save：是否以png格式保存图片，设置为True将保存于项目根路径下的figures文件夹中
        """

        if self.data is None:
            print("ERROR: 周围地铁站情况绘制失败, 没有该城市的数据集...")
            return
        if is_show_alone:
            _, ax = plt.subplots(
                nrows=1, ncols=1, figsize=(12, 8), dpi=100, facecolor="w"
            )
        
        # ------ 绘制周围地铁站情况 ------ #
        sns.countplot(x='subwayAround', data=self.data, ax=ax)
        ax.set_title(
            '周围地铁站情况\n——基于%s58二手房数据' % CONST_TABLE["CITY"][self.city], 
            fontsize=16
        )
        ax.set_xlabel('地铁站数量', fontsize=12)
        ax.set_ylabel('样本数量', fontsize=12)

        plt.tight_layout()
        if is_save:
            path = FiguresIO.getFigureSavePath(
                "%s/%s_Visualize_HouseSurroundings.png" % 
                (self.folder_name, self.city)
            )
            plt.savefig(path, dpi=300)
        if is_show_alone and is_show:
            plt.show()
        