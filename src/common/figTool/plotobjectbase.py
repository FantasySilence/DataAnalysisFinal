# ====================================================================== #
# @Author: Fantasy_Silence                                               #
# @Time: 2024-04-22                                                      #
# @IDE: Visual Studio Code & PyCharm                                     #
# @Python: 3.9.7                                                         #
# ====================================================================== #
# @Description: Object base class for Various visualizations of data     #
# ====================================================================== #
import os
import pandas as pd

from src.common.fileTool.filesio import FilesIO
from src.common.infoTool.const import CONST_TABLE
from src.common.fileTool.figuresio import FiguresIO


class PlotObjectBase:
    
    """
    这是一个对象基类, 用于向绘图工具初始化信息
    """

    def __init__(self, city: str=None) -> None:

        """
        city: 城市名称，例如北京市(city="BJ")
        """
        
        # ------ 检查输入 ------ #
        if city is None or type(city) != str:
            print("ERROR: Inappropriate input of city name...")
            exit(1)
        elif city not in list(CONST_TABLE["CITY"].keys()) or\
             city not in list(CONST_TABLE["URL"].keys()) or\
             city not in list(CONST_TABLE["CITY_CENTER"].keys()):
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
                "row_data/%s_housing_data.csv" % self.city
            ))
        except:
            self.data = None
            