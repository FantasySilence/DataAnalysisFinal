import matplotlib
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

from src.common.infoTool.const import CONST_TABLE
from src.common.fileTool.figuresio import FiguresIO
from src.common.figTool.objectbase import PlotObjectBase


class DrawCharacteristicsOfHouse(PlotObjectBase):

    def __init__(self, city: str = None) -> None:
        super().__init__(city)

    
    def draw(
            self, is_show_alone: bool=True, is_save:bool=False, 
            is_show: bool=True, axes: np.ndarray=None
    ) -> None:

        """
        房屋特征分布图
        分别绘制卧室数量与房间数量分布，房子朝向分布，房屋年龄分布
        is_show：是否显示
        is_show_alone：是否显示于单独的画布上. 如果想单独显示，设置为True，如果想作为子图
                       与其他图片一起显示，自行设置画布(至少1x2)并将该参数设置为False
        is_save：是否以png格式保存图片，设置为True将保存于项目根路径下的figures文件夹中
        """
        
        if self.data is None:
            print("ERROR: 房屋特征分布图绘制失败, 没有该城市的数据集...")
            return
        if is_show_alone:
            _, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 12), 
                                dpi=80, facecolor="w")
        
        # ------ 卧室数量分布 ------ #
        sns.histplot(
            self.data["houseBedroom"], 
            bins=max(self.data["houseBedroom"]) - min(self.data["houseBedroom"]),
            kde=False, ax=axes[0, 0], color="skyblue"
        )
        axes[0, 0].set_title(
            '%s卧室数量分布' % CONST_TABLE["CITY"][self.city], 
            fontsize=16
        )
        axes[0, 0].set_xlabel('卧室数量(间)', fontsize=13)
        axes[0, 0].set_ylabel('样本数', fontsize=13)
        axes[0, 0].xaxis.set_tick_params(labelsize=13)
        axes[0, 0].yaxis.set_tick_params(labelsize=13)

        # ------ 房间数量分布 ------ #
        sns.histplot(
            self.data["houseRoom"],
            bins=max(self.data["houseRoom"]) - min(self.data["houseRoom"]),
            kde=False, ax=axes[0, 1], color="lightgreen"
        )
        axes[0, 1].set_title(
            '%s房间数量分布' % CONST_TABLE["CITY"][self.city], 
            fontsize=16
        )
        axes[0, 1].set_xlabel('房间数量(间)', fontsize=13)
        axes[0, 1].set_ylabel('样本数', fontsize=13)
        axes[0, 1].xaxis.set_tick_params(labelsize=13)
        axes[0, 1].yaxis.set_tick_params(labelsize=13)

        # ------ 房子朝向分布 ------ #
        sns.countplot(
            x="houseOrientation", data=self.data, ax=axes[1, 0],
            color="gold"
        )
        axes[1, 0].set_title(
            '%s房子朝向分布' % CONST_TABLE["CITY"][self.city], 
            fontsize=16
        )
        axes[1, 0].set_xlabel('房子朝向', fontsize=13)
        axes[1, 0].set_ylabel('样本数', fontsize=13)
        axes[1, 0].xaxis.set_tick_params(labelsize=12)
        axes[1, 0].yaxis.set_tick_params(labelsize=12)

        # ------ 房屋年龄分布 ------ #
        sns.histplot(
            self.data["houseAge"].dropna(),
            kde=True, ax=axes[1, 1], color="salmon", 
        )
        axes[1, 1].set_title(
            '%s房屋年龄分布' % CONST_TABLE["CITY"][self.city], 
            fontsize=16
        )
        axes[1, 1].set_xlabel('房屋年龄（年）', fontsize=13)
        axes[1, 1].set_ylabel('样本数', fontsize=13)
        axes[1, 1].xaxis.set_tick_params(labelsize=13)
        axes[1, 1].yaxis.set_tick_params(labelsize=13)

        plt.tight_layout()
        if is_save:
            path = FiguresIO.getFigureSavePath(
                "%s/%s_Visualize_Characteristics.png" % 
                (self.folder_name, self.city)
            )
            plt.savefig(path, dpi=300)
        if is_show_alone and is_show:
            plt.show()
            