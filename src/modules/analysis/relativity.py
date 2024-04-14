import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

from src.common.infoTool.const import CONST_TABLE
from src.common.fileTool.figuresio import FiguresIO
from src.common.figTool.objectbase import PlotObjectBase


class DrawVariblesRelativityWithTarget(PlotObjectBase):

    def __init__(self, city: str = None) -> None:
        super().__init__(city)
    

    def draw(
            self, is_show_alone: bool=True, is_save: bool=False, 
            is_show: bool=True, ax: Axes=None
    ) -> None:

        """
        绘制相关性图
        """

        if self.data is None:
            print("ERROR: 相关性图绘制失败, 没有该城市的数据集...")
            return
        data = self.data.drop(columns=["ID", "houseLoc"])
        data = pd.get_dummies(data, drop_first=True, dtype=int)
        if is_show_alone:
            _, ax = plt.subplots(figsize=(12, 8), dpi=80, facecolor="w")
        data.corr()["housePrice"].sort_values(ascending=False).plot(
            kind="barh", ax=ax, color="skyblue"
        )
        ax.vlines(x=0, ymin=0, ymax=len(data.corr()["housePrice"]),
                   color="lightskyblue", linestyles="dashed")
        ax.set_xlabel("相关性", fontsize=14)
        ax.set_title(
            "变量之间的相关性\n——基于%s的数据"%CONST_TABLE["CITY"][self.city], 
            fontsize=16
        )
        plt.tight_layout()
        if is_save:
            path = FiguresIO.getFigureSavePath(
                "%s/%s_Analysis_Relativity.png" % 
                (self.folder_name, self.city)
            )
            plt.savefig(path, dpi=300)
        if is_show_alone and is_show:
            plt.show()
