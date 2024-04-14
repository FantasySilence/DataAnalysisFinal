import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

from src.common.const import CONST_TABLE
from src.common.figuresio import FiguresIO
from src.common.objectbase import PlotObjectBase


class DrawCategoryVaribles(PlotObjectBase):

    def __init__(self, city: str = None) -> None:
        super().__init__(city)
    

    def draw(
            self, is_show_alone: bool=True, is_save: bool=False, 
            is_show: bool=True, axes: np.ndarray=None
    ) -> None:

        """
        绘制分类变量
        """

        if self.data is None:
            print("ERROR: 分类变量探索绘制失败, 没有该城市的数据集...")
            return
        if is_show_alone:
            _, axes = plt.subplots(
                nrows=2, ncols=3, figsize=(25, 18), dpi=80, facecolor="w"
            )   
        data = self.data.drop(columns=["ID", "houseLoc"])
        data["roomCategory"] = data["houseRoom"].apply(
            lambda x: '≥13' if x >= 13 else str(x)
        )
        quantiles = self.data["housePrice"].quantile([0.25, 0.75])
        data["housePriceCategory"] = pd.cut(
            self.data["housePrice"], 
            bins=[
                0, quantiles[0.25], self.data["housePrice"].median(), 
                quantiles[0.75], self.data["housePrice"].max()
            ],
            labels=["较低", "低", "中等", "高"]
        )

        # ------ 房子朝向(houseOrientation) ------ #
        sns.countplot(
            x="houseOrientation", hue="housePriceCategory", 
            data=data, ax=axes[0, 0]
        )
        sns.boxplot(
            x="houseOrientation", y="housePrice", data=data, ax=axes[1, 0]
        )
        axes[0, 0].set_title(
            "房子朝向\n——基于%s58二手房数据"%CONST_TABLE["CITY"][self.city],
            fontsize=16
        )
        axes[0, 0].xaxis.set_tick_params(labelsize=12)
        axes[0, 0].yaxis.set_tick_params(labelsize=12)
        axes[0, 0].set_xlabel("朝向", fontsize=14)
        axes[0, 0].set_ylabel("样本数", fontsize=14)
        axes[1, 0].xaxis.set_tick_params(labelsize=12)
        axes[1, 0].yaxis.set_tick_params(labelsize=12)
        axes[1, 0].set_xlabel("朝向", fontsize=14)
        axes[1, 0].set_ylabel("房价", fontsize=14)

        # ------ 房子房间数量(houseRoom) ------ #
        sns.countplot(
            x="roomCategory", hue="housePriceCategory", data=data, ax=axes[0, 1],
            order=sorted(
                data['roomCategory'].unique(), 
                key=lambda x: float('inf') if x == '≥13' else int(x)
            )
        )
        sns.boxplot(
            x="roomCategory", y="housePrice", data=data, ax=axes[1, 1],
            order=sorted(
                data['roomCategory'].unique(), 
                key=lambda x: float('inf') if x == '≥13' else int(x)
            )
        )
        axes[0, 1].set_title(
            "房间数量\n——基于%s58二手房数据"%CONST_TABLE["CITY"][self.city],
            fontsize=16
        )
        axes[0, 1].xaxis.set_tick_params(labelsize=12)
        axes[0, 1].yaxis.set_tick_params(labelsize=12)
        axes[0, 1].set_xlabel("房间数量", fontsize=14)
        axes[0, 1].set_ylabel("样本数", fontsize=14)
        axes[1, 1].xaxis.set_tick_params(labelsize=12)
        axes[1, 1].yaxis.set_tick_params(labelsize=12)
        axes[1, 1].set_xlabel("房间数量", fontsize=14)
        axes[1, 1].set_ylabel("房价", fontsize=14)

        # ------ 房子卧室数量(houseBedroom) ------ #
        sns.countplot(
            x="houseBedroom", hue="housePriceCategory", data=data, 
            ax=axes[0, 2]
        )
        sns.boxplot(
            x="houseBedroom", y="housePrice", data=data, ax=axes[1, 2]
        )
        axes[0, 2].set_title(
            "卧室数量\n——基于%s58二手房数据"%CONST_TABLE["CITY"][self.city],
            fontsize=16
        )
        axes[0, 2].xaxis.set_tick_params(labelsize=12)
        axes[0, 2].yaxis.set_tick_params(labelsize=12)
        axes[0, 2].set_xlabel("卧室数量", fontsize=14)
        axes[0, 2].set_ylabel("样本数", fontsize=14)
        axes[1, 2].xaxis.set_tick_params(labelsize=12)
        axes[1, 2].yaxis.set_tick_params(labelsize=12)
        axes[1, 2].set_xlabel("卧室数量", fontsize=14)
        axes[1, 2].set_ylabel("房价", fontsize=14)

        plt.tight_layout()
        if is_save:
            path = FiguresIO.getFigureSavePath(
                "%s/%s_Analysis_CategoryVar.png" % 
                (self.folder_name, self.city)
            )
            plt.savefig(path, dpi=300)
        if is_show_alone and is_show:
            plt.show()
