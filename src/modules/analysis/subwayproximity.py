# ============================================================== #
# @Author: Fantasy_Silence                                       #
# @Time: 2024-05-01                                              #
# @IDE: Visual Studio Code & PyCharm                             #
# @Python: 3.9.7                                                 #
# ============================================================== #
# @Description: Draw the relationship between subway proximity   # 
# and housing prices per square meter                            #
# ============================================================== #
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

from src.common.fileTool.figuresio import FiguresIO
from src.common.figTool.plotobjectbase import PlotObjectBase


class DrawSubwayProximityWithTarget(PlotObjectBase):
    
    def __init__(self, city: str = None) -> None:
        super().__init__(city)


    def draw(
        self, is_show: bool=True, is_save: bool=False, 
        is_show_alone: bool=True, ax: Axes=None
    ) -> None:
        
        """
        房子地铁接近程度与每平方米房价之间的关系
        is_show：是否显示
        is_show_alone：是否显示于单独的画布上. 如果想单独显示，设置为True，如果想作为子图
                       与其他图片一起显示，自行设置画布(至少2x2)并将该参数设置为False
        is_save：是否以png格式保存图片，设置为True将保存于项目根路径下的figures文件夹中
        """

        if self.data is None:
            print("ERROR: 房子地铁接近程度与每平方米房价之间的关系绘制失败, 没有该城市的数据集...")
            return
        if is_show_alone:
            _, ax = plt.subplots(
                nrows=1, ncols=1, figsize=(12, 8), dpi=100, facecolor="w"
            )
        
        # ------ 绘制房子地铁接近程度与每平方米房价之间的关系 ------ #
        sns.boxplot(x='subwayAround', y='unitPrice', data=self.data, ax=ax)
        ax.set_title("地铁接近程度与目标变量", fontsize=16)
        ax.set_xlabel("房子周围地铁站数量", fontsize=12)
        ax.set_ylabel("每平方米价格", fontsize=12)

        plt.tight_layout()
        if is_save:
            path = FiguresIO.getFigureSavePath(
                "%s/%s_Analysis_SubwayProximity.png" % 
                (self.folder_name, self.city)
            )
            plt.savefig(path, dpi=300)
        if is_show_alone and is_show:
            plt.show()