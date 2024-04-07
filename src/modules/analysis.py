# ======================================================= #
# @Author: Fantasy_Silence                                #
# @Time: 2024-04-07                                       #
# @IDE: Visual Studio Code & PyCharm                      #
# @Python: 3.9.7                                          #
# ======================================================= #
# @Description:                                           #
# This module is used for exploratory analysis of data    #
# ======================================================= #
import matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

from src.common.filesio import FilesIO
from src.common.const import CONST_TABLE


class HousingDataExploratoryAnalysis:

    """
    对数据集中的特征变量进行探索性分析
    """

    def __init__(self, city: str) -> None:

        """
        city: 城市名称，例如北京市(city="BJ")
        """
        
        self.city = city

        # ------ 尝试读取数据 ------ #
        try:
            self.data = pd.read_csv(FilesIO.getDataset(
                "%s_housing_data.csv" % self.city
            ))
        except:
            self.data = None
