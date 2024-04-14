# =============================================== #
# @Author: Fantasy_Silence                        #
# @Time: 2024-04-06                               #
# @IDE: Visual Studio Code & PyCharm              #
# @Python: 3.9.7                                  #
# =============================================== #
# @Description:                                   #
# Implement a function to combine data with maps  #
# =============================================== #
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.common.fileTool.filesio import FilesIO
from src.common.infoTool.const import CONST_TABLE


def map_plot(city: str, is_show: bool = True) -> None:

    """
    city: 城市名称，例如北京市(city="BJ")
    is_show: 是否显示图形
    """

    # ------ 读取对应的城市房价数据 ------ #
    data = pd.read_csv(FilesIO.getDataset("%s_housing_data.csv" % city))

    # ------ 获取上四分位数，下四分位数 ------ #
    quantiles = data["unitPrice"].quantile([0.25, 0.75])

    # ------ 绘制主图 ------ #
    fig = px.scatter_mapbox(
        data,
        lat="latitude",
        lon="longitude",
        color="unitPrice",
        color_discrete_sequence=["unitPrice"],
        color_continuous_scale="jet",
        range_color=[quantiles[0.25], quantiles[0.75]],
        zoom=8,
        height=800,
    )
    fig.update_layout(mapbox_style="open-street-map")  # 开启街道网格
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})  # 设置边距为0

    # ------ 添加城市市中心 ------ #
    new_latitude = CONST_TABLE["CITY_CENTER"][city]["LAT"]
    new_longitude = CONST_TABLE["CITY_CENTER"][city]["LNG"]

    # ------ 添加新的点 ------ #
    fig.add_trace(
        go.Scattermapbox(
            lat=[new_latitude],
            lon=[new_longitude],
            marker=go.scattermapbox.Marker(
                size=14,
                color="black",
            ),
            showlegend=False,
        )
    )
    if is_show:
        fig.show()
