# ======================================================= #
# @Author: Fantasy_Silence                                #
# @Time: 2024-04-07                                       #
# @IDE: Visual Studio Code & PyCharm                      #
# @Python: 3.9.7                                          #
# ======================================================= #
# @Description:                                           #
# This module is used for exploratory analysis of data    #
# ======================================================= #
import os
import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

from src.common.filesio import FilesIO
from src.common.const import CONST_TABLE
from src.common.figuresio import FiguresIO


class HousingDataExploratoryAnalysis:

    """
    对数据集中的特征变量进行探索性分析
    """

    def __init__(self, city: str=None) -> None:

        """
        city: 城市名称，例如北京市(city="BJ")
        """
        
        # ------ 检查输入 ------ #
        if city is None or type(city) != str:
            print("ERROR: Inappropriate input of city name...")
            exit(1)
        elif city not in list(CONST_TABLE["CITY"].keys()):
            print("ERROR: City name not included, please add it in const.py")
            exit(1)
        else:
            self.city = city

        # ------ 创建存放图片的文件夹 ------ #
        self.folder_name = city + "_figures"
        data_folder = os.path.join(
            FiguresIO.getFigureSavePath(), self.folder_name
        )
        if not os.path.exists(data_folder):
            os.mkdir(data_folder)
        else:
            pass

        # ------ 尝试读取数据 ------ #
        try:
            self.data = pd.read_csv(FilesIO.getDataset(
                "%s_housing_data.csv" % self.city
            ))
        except:
            self.data = None
    

    def draw_heatmap(
            self, is_show_alone: bool=True, is_save: bool=False, 
            is_show: bool=True, ax: Axes=None
    ) -> None:

        """
        绘制热力图
        """

        if self.data is None:
            print("ERROR: 热力图绘制失败,没有该城市的数据集...")
            return
        data = self.data.drop(columns=["housePrice", "ID", "houseLoc"])
        if is_show_alone:
            _, ax = plt.subplots(figsize=(12, 8), dpi=80, facecolor="w")

        sns.heatmap(data.corr(), annot=True, fmt=".2f", cmap="Blues", ax=ax)
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

    
    def draw_relativity(
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
    

    def draw_category(
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
    

    def draw_continuity(
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
