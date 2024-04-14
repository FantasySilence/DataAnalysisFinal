import matplotlib
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

from src.common.infoTool.const import CONST_TABLE
from src.common.fileTool.figuresio import FiguresIO
from src.common.figTool.objectbase import PlotObjectBase


class DrawRelationBetweenAgeAndPrice(PlotObjectBase):

    def __init__(self, city: str = None) -> None:
        super().__init__(city)
    

    def draw(
            self, is_show_alone: bool=True, is_save: bool=True, 
            is_show: bool=True, axes: np.ndarray=None
    ) -> None:

        """
        价格与房屋年龄的关系
        is_show：是否显示
        is_show_alone：是否显示于单独的画布上. 如果想单独显示，设置为True，如果想作为子图
                       与其他图片一起显示，自行设置画布(至少1x2)并将该参数设置为False
        is_save：是否以png格式保存图片，设置为True将保存于项目根路径下的figures文件夹中
        """

        if self.data is None:
            print("ERROR: 价格与房屋年龄的关系图绘制失败, 没有该城市的数据集...")
            return
        if is_show_alone:
            _, axes = plt.subplots(
                nrows=1, ncols=2, figsize=(15, 7), dpi=80, facecolor="w"
            )

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
        axes[0].set_title(
            "每平方米房价 VS 房龄\n——基于%s58二手房数据" % 
            CONST_TABLE["CITY"][self.city], 
            fontsize=16
        )
        axes[0].set_xlabel("房龄(年)", fontsize=13)
        axes[0].set_ylabel("每平方米房价(元/平方米)", fontsize=13)

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
        axes[1].set_title(
            "房屋总价 VS 房龄\n——基于%s58二手房数据" % 
            CONST_TABLE["CITY"][self.city], 
            fontsize=16
        )
        axes[1].set_xlabel("房龄(年)", fontsize=13)
        axes[1].set_ylabel("房屋总价(万元)", fontsize=13)

        plt.tight_layout()
        if is_save:
            path = FiguresIO.getFigureSavePath(
                "%s/%s_Visualize_AgeVsPrice.png" % 
                (self.folder_name, self.city)
            )
            plt.savefig(path, dpi=300)
        if is_show_alone and is_show:
            plt.show()
