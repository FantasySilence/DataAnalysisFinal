import matplotlib
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

from src.common.const import CONST_TABLE
from src.common.dataonmap import map_plot
from src.common.figuresio import FiguresIO
from src.common.objectbase import PlotObjectBase


class DrawGeoDistribution(PlotObjectBase):

    def __init__(self, city: str = None) -> None:
        super().__init__(city)
        
    

    def draw(
            self, is_show: bool=True, is_map_show:bool=False, 
            is_save: bool=False, is_show_alone: bool=True, ax: Axes=None
    ) -> None:

        """
        地理分布图
        is_show：是否显示
        is_show_alone：是否显示于单独的画布上. 如果想单独显示，设置为True，如果想作为子图
                       与其他图片一起显示，自行设置画布(至少1x1)并将该参数设置为False
        is_save：是否以png格式保存图片，设置为True将保存于项目根路径下的figures文件夹中
        is_map_show：是否将数据与真实地图相结合，设置为True，请科学上网
        """

        if self.data is None:
            print("ERROR: 地理分布图绘制失败, 没有该城市的数据集...")
            return
        if is_show_alone:
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
            "%s二手房房价数据\n——基于58二手房数据"%CONST_TABLE["CITY"][self.city],
            fontsize=16
        )
        ax.set_xlabel("经度", fontsize=13)
        ax.set_ylabel("纬度", fontsize=13)
        ax.legend(loc="upper right")
        plt.tight_layout()
        if is_save:
            path = FiguresIO.getFigureSavePath(
                "%s/%s_Visualize_GeoDistribute.png" % 
                (self.folder_name, self.city)
            )
            plt.savefig(path, dpi=300)
        if is_show_alone and is_show:
            plt.show()

        # ------ 将数据绘制在地图上 ------ #
        if is_map_show:
            map_plot(city=self.city, is_show=is_map_show)
