import matplotlib
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

from src.common.infoTool.const import CONST_TABLE
from src.common.fileTool.figuresio import FiguresIO
from src.common.figTool.objectbase import PlotObjectBase


class DrawContinuitysVaribles(PlotObjectBase):

    def __init__(self, city: str = None) -> None:
        super().__init__(city)
    

    def draw(
            self, is_show_alone: bool=True, is_save: bool=False, 
            is_show: bool=True, axes: np.ndarray=None
    ) -> None:

        """
        绘制连续变量
        """

        if self.data is None:
            print("ERROR: 连续变量探索绘制失败, 没有该城市的数据集...")
            return
        data = self.data.drop(columns=["ID", "houseLoc"])
        if is_show_alone:
            _, axes = plt.subplots(
                nrows=2, ncols=3, figsize=(25, 18), dpi=80, facecolor="w"
            )

        # ------ longitude ------ #
        sns.histplot(
            x="longitude", data=data, ax=axes[0, 0], color="skyblue",
            kde=True
        )
        axes[0, 0].set_title(
            "经度(longitude)\n——基于%s58二手房数据" % 
            CONST_TABLE["CITY"][self.city], 
            fontsize=16
        )
        axes[0, 0].xaxis.set_tick_params(labelsize=12)
        axes[0, 0].yaxis.set_tick_params(labelsize=12)

        # ------ latitude ------ #
        sns.histplot(
            x="latitude", data=data, ax=axes[1, 0], color="limegreen",
            kde=True
        )
        axes[1, 0].set_title(
            "纬度(latitude)\n——基于%s58二手房数据" % 
            CONST_TABLE["CITY"][self.city], 
            fontsize=16
        )
        axes[1, 0].xaxis.set_tick_params(labelsize=12)
        axes[1, 0].yaxis.set_tick_params(labelsize=12)

        # ------ unitPrice ------ #
        sns.histplot(
            x="unitPrice", data=data, ax=axes[0, 1], color="violet",
            kde=True
        )
        axes[0, 1].set_title(
            "每平方米价格(unitPrice)\n——基于%s58二手房数据" % 
            CONST_TABLE["CITY"][self.city], 
            fontsize=16
        )
        axes[0, 1].xaxis.set_tick_params(labelsize=12)
        axes[0, 1].yaxis.set_tick_params(labelsize=12)

        # ------ housePrice ------ #
        sns.histplot(
            x="housePrice", data=data, ax=axes[1, 1], color="darkorange",
            kde=True
        )
        axes[1, 1].set_title(
            "总价(housePrice)\n——基于%s58二手房数据" % 
            CONST_TABLE["CITY"][self.city], 
            fontsize=16
        )
        axes[1, 1].xaxis.set_tick_params(labelsize=12)
        axes[1, 1].yaxis.set_tick_params(labelsize=12)

        # ------ houseArea ------ #
        sns.histplot(
            x="houseArea", data=data, ax=axes[0, 2], color="lime",
            kde=True
        )
        axes[0, 2].set_title(
            "房子面积(houseArea)\n——基于%s58二手房数据" % 
            CONST_TABLE["CITY"][self.city], 
            fontsize=16
        )
        axes[0, 2].xaxis.set_tick_params(labelsize=12)
        axes[0, 2].yaxis.set_tick_params(labelsize=12)

        # ------ houseAge ------ #
        sns.histplot(
            x="houseAge", data=data, ax=axes[1, 2], color="red",
            kde=True
        )
        axes[1, 2].set_title(
            "房龄(houseAge)\n——基于%s58二手房数据" % 
            CONST_TABLE["CITY"][self.city], 
            fontsize=16
        )
        axes[1, 2].xaxis.set_tick_params(labelsize=12)
        axes[1, 2].yaxis.set_tick_params(labelsize=12)

        plt.tight_layout()
        if is_save:
            path = FiguresIO.getFigureSavePath(
                "%s/%s_Analysis_ContinuousVar.png" % 
                (self.folder_name, self.city)
            )
            plt.savefig(path, dpi=300)
        if is_show_alone and is_show:
            plt.show()
