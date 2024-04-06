# =================================================== #
# @Author: Fantasy_Silence                            #
# @Time: 2024-04-06                                   #
# @IDE: Visual Studio Code & PyCharm                  #
# @Python: 3.9.7                                      #
# =================================================== #
# @Description:                                       #
# This module is used to visualize the crawled data   #
# =================================================== #
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

from src.common.filesio import FilesIO
from src.common.const import CONST_TABLE
from src.common.dataonmap import map_plot


class HousingDataVisualize:
    
    """
    对爬取的数据进行可视化
    """

    def __init__(self, city: str, is_map_show:bool=True) -> None:

        """
        可视化模块v1
        city: 城市名称，例如北京市(city="BJ")
        is_map_show: 是否绘制地图
        """
        
        self.city = city
        self.is_map_show = is_map_show
        self.__plot__()
        
    
    def __plot__(self):

        """
        可视化主函数
        """

        try:
            data = pd.read_csv(FilesIO.getDataset(
                "%s_housing_data.csv" % self.city
            ))
        except:
            print("没有该文件")
            return
        
        _, ax = plt.subplots(figsize=(12, 8), dpi=100)
        data.plot(
            kind="scatter", x="longitude", y="latitude", alpha=0.6,
            s=data["housePrice"] / 100, label="housePrice",
            c="unitPrice", cmap=plt.get_cmap("jet"), colorbar=True,
            sharex=False, ax=ax
        )
        ax.plot(
            CONST_TABLE["CITY_CENTER"][self.city]["LNG"],
            CONST_TABLE["CITY_CENTER"][self.city]["LAT"],
            "r*", markersize=10, label="city center"
        )

        ax.set_title(
            "%s二手房房价数据\n——基于58二手房"%CONST_TABLE["CITY"][self.city]
        )
        ax.set_xlabel("经度")
        ax.set_ylabel("纬度")
        ax.legend(loc="upper right")
        plt.show()

        map_plot(city=self.city, is_show=self.is_map_show)
