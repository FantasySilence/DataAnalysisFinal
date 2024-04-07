# =================================================== #
# @Author: Fantasy_Silence                            #
# @Time: 2024-04-06                                   #
# @IDE: Visual Studio Code & PyCharm                  #
# @Python: 3.9.7                                      #
# =================================================== #
# @Description:                                       #
# This module is used to visualize the crawled data   #
# =================================================== #
import os
import matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

from src.common.filesio import FilesIO
from src.common.const import CONST_TABLE
from src.common.dataonmap import map_plot
from src.common.figuresio import FiguresIO


class HousingDataVisualize:
    
    """
    对爬取的数据进行可视化
    """

    def __init__(self, city: str) -> None:

        """
        可视化模块v2
        city: 城市名称，例如北京市(city="BJ")
        """
        
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
        
    
    def geodistribute(
            self, is_show: bool=True, is_map_show:bool=False, 
            is_save: bool=False
    ) -> None:

        """
        地理分布图
        """

        if self.data is None:
            print("ERROR: 没有该城市的数据集...")
            return
        _, ax = plt.subplots(figsize=(12, 8), dpi=100, facecolor="w")
        self.data.plot(
            kind="scatter", x="longitude", y="latitude", alpha=0.6,
            s=self.data["housePrice"] / 100, label="housePrice",
            c="unitPrice", cmap=plt.get_cmap("jet"), colorbar=True,
            sharex=False, ax=ax
        )
        ax.plot(
            CONST_TABLE["CITY_CENTER"][self.city]["LNG"],
            CONST_TABLE["CITY_CENTER"][self.city]["LAT"],
            "r*", markersize=10, label="city center"
        )

        ax.set_title(
            "%s二手房房价数据\n——基于58二手房数据"%CONST_TABLE["CITY"][self.city]
        )
        ax.set_xlabel("经度")
        ax.set_ylabel("纬度")
        ax.legend(loc="upper right")
        plt.tight_layout()
        if is_save:
            path = FiguresIO.getFigureSavePath(
                "%s/%s_Visualize_GeoDistribute.png" % 
                (self.folder_name, self.city)
            )
            plt.savefig(path)
        if is_show:
            plt.show()

        # ------ 将数据绘制在地图上 ------ #
        if is_map_show:
            map_plot(city=self.city, is_show=is_map_show)
    

    def pricearearelation(self, is_show: bool=True, is_save: bool=False) -> None:

        """
        每平方米房价与面积关系图
        """

        if self.data is None:
            print("ERROR: 没有该城市的数据集...")
            return
        _, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 7), 
                             dpi=100, facecolor="w")

        self.data.plot(
            kind="scatter", x="unitPrice", y="houseArea", alpha=0.6,
            c="unitPrice", cmap=plt.get_cmap("jet"), colorbar=False,
            sharex=False, ax=ax[0], s=5
        )
        ax[0].set_xlabel("每平方米价格(元/每平方米)")
        ax[0].set_ylabel("房屋面积(平方米)")

        quantiles = self.data["houseArea"].quantile([0.25, 0.75])
        self.data["areaCategory"] = pd.cut(
            self.data["houseArea"], 
            bins=[
                0, quantiles[0.25], self.data["houseArea"].median(), 
                quantiles[0.75], self.data["houseArea"].max()
            ],
            labels=["非常小", "小", "中等", "大"]
        )
        sns.boxplot(
            x="areaCategory", y="housePrice", data=self.data, ax=ax[1],
            order=["非常小", "小", "中等", "大"], 
            palette=sns.color_palette("hls", 4)
        )   
        ax[1].set_xlabel("房屋面积(平方米)")
        ax[1].set_ylabel("房屋总价(万元)")
        plt.suptitle(
            "%s每平方米房价与面积关系图\n——基于58二手房数据"%
            CONST_TABLE["CITY"][self.city]
        )
        plt.subplots_adjust(wspace=0.3)
        plt.tight_layout()
        if is_save:
            path = FiguresIO.getFigureSavePath(
                "%s/%s_Visualize_PriceVsArea.png" % 
                (self.folder_name, self.city)
            )
            plt.savefig(path)
        if is_show:
            plt.show()
    

    def housecharacteristics(self, is_show: bool=True, is_save:bool=False) -> None:

        """
        房屋特征分布图
        分别绘制卧室数量与房间数量分布，房子朝向分布，房屋年龄分布
        """
        
        if self.data is None:
            print("ERROR: 没有该城市的数据集...")
            return
        _, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 12), 
                               dpi=80, facecolor="w")
        
        # ------ 卧室数量分布 ------ #
        sns.histplot(
            self.data["houseBedroom"], 
            bins=max(self.data["houseBedroom"]) - min(self.data["houseBedroom"]),
            kde=False, ax=axes[0, 0], color="skyblue"
        )
        axes[0, 0].set_title('卧室数量分布', fontsize=14)
        axes[0, 0].set_xlabel('卧室数量(间)', fontsize=12)
        axes[0, 0].set_ylabel('样本数', fontsize=12)
        axes[0, 0].xaxis.set_tick_params(labelsize=12)
        axes[0, 0].yaxis.set_tick_params(labelsize=12)

        # ------ 房间数量分布 ------ #
        sns.histplot(
            self.data["houseRoom"],
            bins=max(self.data["houseRoom"]) - min(self.data["houseRoom"]),
            kde=False, ax=axes[0, 1], color="lightgreen"
        )
        axes[0, 1].set_title('房间数量分布', fontsize=14)
        axes[0, 1].set_xlabel('房间数量(间)', fontsize=12)
        axes[0, 1].set_ylabel('样本数', fontsize=12)
        axes[0, 1].xaxis.set_tick_params(labelsize=12)
        axes[0, 1].yaxis.set_tick_params(labelsize=12)

        # ------ 房子朝向分布 ------ #
        sns.countplot(
            x="houseOrientation", data=self.data, ax=axes[1, 0],
            color="gold"
        )
        axes[1, 0].set_title('房子朝向分布', fontsize=14)
        axes[1, 0].set_xlabel('房子朝向', fontsize=12)
        axes[1, 0].set_ylabel('样本数', fontsize=12)
        axes[1, 0].xaxis.set_tick_params(labelsize=12)
        axes[1, 0].yaxis.set_tick_params(labelsize=12)

        # ------ 房屋年龄分布 ------ #
        sns.histplot(
            self.data["houseAge"].dropna(),
            kde=True, ax=axes[1, 1], color="salmon", 
        )
        axes[1, 1].set_title('房屋年龄分布', fontsize=14)
        axes[1, 1].set_xlabel('房屋年龄（年）', fontsize=12)
        axes[1, 1].set_ylabel('样本数', fontsize=12)
        axes[1, 1].xaxis.set_tick_params(labelsize=12)
        axes[1, 1].yaxis.set_tick_params(labelsize=12)

        plt.suptitle(
            "%s房屋特征分布图\n——基于58二手房数据"%CONST_TABLE["CITY"][self.city],
            fontsize=16
        )
        plt.tight_layout()
        if is_save:
            path = FiguresIO.getFigureSavePath(
                "%s/%s_Visualize_Characteristics.png" % 
                (self.folder_name, self.city)
            )
            plt.savefig(path)
        if is_show:
            plt.show()


    def houseageprice(self, is_show: bool=True, is_save: bool=True) -> None:

        """
        价格与房屋年龄的关系
        """

        if self.data is None:
            print("ERROR: 没有该城市的数据集...")
            return
        _, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 7), 
                               dpi=80, facecolor="w")

        self.data.plot(
            kind="scatter", x="houseAge", y="unitPrice", alpha=0.6,
            c="unitPrice", cmap=plt.get_cmap("jet"), colorbar=False,
            sharex=False, ax=axes[0], s=5
        )
        sns.regplot(
            data=self.data,
            x="houseAge", y="unitPrice",
            scatter=False,
            line_kws={'color': 'darkcyan'}, ax=axes[0]
        )
        axes[0].set_title("每平方米房价 VS 房龄", fontsize=14)
        axes[0].set_xlabel("房龄(年)", fontsize=12)
        axes[0].set_ylabel("每平方米房价(元/平方米)", fontsize=12)

        self.data.plot(
            kind="scatter", x="houseAge", y="housePrice", alpha=0.6,
            c="housePrice", cmap=plt.get_cmap("jet"), colorbar=False,
            sharex=False, ax=axes[1], s=5
        )
        sns.regplot(
            data=self.data,
            x="houseAge", y="housePrice",
            scatter=False, 
            line_kws={'color': 'darkcyan'}, ax=axes[1]
        )
        axes[1].set_title("房屋总价 VS 房龄", fontsize=14)
        axes[1].set_xlabel("房龄(年)", fontsize=12)
        axes[1].set_ylabel("房屋总价(万元)", fontsize=12)

        plt.suptitle(
            "%s价格与房屋年龄的关系\n——基于58二手房数据"%
            CONST_TABLE["CITY"][self.city],
            fontsize=16
        )
        plt.tight_layout()
        if is_save:
            path = FiguresIO.getFigureSavePath(
                "%s/%s_Visualize_AgeVsPrice.png" % 
                (self.folder_name, self.city)
            )
            plt.savefig(path)
        if is_show:
            plt.show()