# ======================================================== #
# @Author: Fantasy_Silence                                 #
# @Time: 2024-04-11                                        #
# @IDE: Visual Studio Code & PyCharm                       #
# @Python: 3.9.7                                           #
# ======================================================== #
# Description:                                             #
# A pipeline for preprocessing 58 same city data crawled   #
# ======================================================== #
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import FunctionTransformer
from sklearn.base import BaseEstimator, TransformerMixin

from src.common.fileTool.filesio import FilesIO
from src.common.infoTool.const import CONST_TABLE


class PipeLineFor58HousingData:

    """
    TODO：设计实现58同城房价数据的特征工程
    输入连续变量和分类变量的类名即可
    实现对58同城房价数据的预处理
    """
    
    def __init__(self) -> None:
        
        pass


    def transform(self, data: pd.DataFrame) -> pd.DataFrame:

        pass


class FeatureEngineeringFor58(BaseEstimator, TransformerMixin):

    pass
