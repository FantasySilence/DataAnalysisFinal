# =========================================================== #
# @Author: Fantasy_Silence                                    #
# @Time: 2024-04-30                                           #
# @IDE: Visual Studio Code & PyCharm                          #
# @Python: 3.9.7                                              #
# =========================================================== #
# @Description: Draw a heatmap of the correlation matrix      #
# =========================================================== #
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

from src.common.infoTool.const import CONST_TABLE
from src.common.fileTool.figuresio import FiguresIO
from src.common.figTool.plotobjectbase import PlotObjectBase


class DrawHeatMapWithRelativityAmongVaribles(PlotObjectBase):

    def __init__(self, city: str = None) -> None:
        super().__init__(city)

    
    def draw(
            self, is_show_alone: bool=True, is_save: bool=False, 
            is_show: bool=True, ax: Axes=None
    ) -> None:

        """
        绘制热力图
        is_show：是否显示
        is_show_alone：是否显示于单独的画布上. 如果想单独显示，设置为True，如果想作为子图
                       与其他图片一起显示，自行设置画布(至少1x1)并将该参数设置为False
        is_save：是否以png格式保存图片，设置为True将保存于项目根路径下的figures文件夹中
        """

        if self.data is None:
            print("ERROR: 热力图绘制失败,没有该城市的数据集...")
            return
        data = self.data.drop(columns=["housePrice", "ID", "houseLoc"])
        if is_show_alone:
            _, ax = plt.subplots(figsize=(12, 8), dpi=80, facecolor="w")

        sns.heatmap(
            data.corr(), annot=True, fmt=".2f", cmap="Blues", ax=ax,
            annot_kws={'size':12, 'weight':'bold'}
        )
        ax.set_title(
            "相关系数矩阵\n——%s房价数据"%CONST_TABLE["CITY"][self.city], 
            fontsize=16
        )
        plt.xticks(rotation=45, fontsize=14)
        plt.yticks(rotation=0, fontsize=14)
        plt.tight_layout()
        if is_save:
            path = FiguresIO.getFigureSavePath(
                "%s/%s_Analysis_Heatmap.png" % 
                (self.folder_name, self.city)
            )
            plt.savefig(path, dpi=300)
        if is_show_alone and is_show:
            plt.show()
