# ======================================================== #
# @Author: Fantasy_Silence                                 #
# @Time: 2024-04-11                                        #
# @IDE: Visual Studio Code & PyCharm                       #
# @Python: 3.9.7                                           #
# ======================================================== #
# Description:                                             #
# A pipeline for preprocessing 58 same city data crawled   #
# ======================================================== #
import os
import numpy as np
import pandas as pd
from geopy.distance import geodesic
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import FunctionTransformer
from sklearn.base import BaseEstimator, TransformerMixin

from src.common.fileTool.filesio import FilesIO
from src.common.infoTool.const import CONST_TABLE


class PipeLineFor58HousingData(BaseEstimator, TransformerMixin):

    """
    设计实现58同城房价数据的特征工程
    """
    
    def __init__(self, city_name: str=None, is_save: bool=False) -> None:
        
        self.is_save = is_save
        if city_name is not None:
            self.city_name = city_name
        else:
            print("ERROR: City name required...")
            exit(1)
    

    def fit(self, X, y=None):
        return self


    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        # ------ 第一步，数据清洗与特征工程 ------ #
        pipeline_step_1 = Pipeline([
            # 计算并添加距离市中心的距离
            ("distance_to_city_center", DistanceToCityCenter(self.city_name)),
            # 某些NA值并非缺失值，这部分替换为None
            ("replace_na", ReplaceNAtoNone()),
            # 去掉ID和houseLoc列
            ("drop_columns", DropColumns()),
        ])
        X = pipeline_step_1.fit_transform(X)

        # ------ 第二步，数据预处理 ------ #
        num_pipeline = Pipeline([
            # 填充缺失值，填充策略为以均值填充
            ("imputer", SimpleImputer(strategy="mean")),
            # 标准化
            ("std_scaler", StandardScaler()),
        ])      # 连续变量处理
        
        cat_pipeline = Pipeline([
            # 填充缺失值，填充策略为以出现次数最多的类别填充
            ("imputer", SimpleImputer(strategy="most_frequent")),
            # 对分类变量编码
            ("onehot_encoder", OrdinalEncoder()),
        ])      # 分类变量处理

        num_attribs = [
            "longitude", "latitude", "houseArea", "houseAge", 
            "houseFloorSum", "distance"
        ]
        cat_attribs = [
            "houseBedroom", "houseRoom", "houseSubway", "houseOrientation",
            "houseHousingPeriod", "houseFloorType"
        ]
        log_attribs = ["unitPrice"]

        # ------ 第三步，整合为一个管道 ------ #
        pipeline_step_2 = ColumnTransformer([
            ("num", num_pipeline, num_attribs),
            ("cat", cat_pipeline, cat_attribs),
            # 对房价和单位房价取对数
            ("target", FunctionTransformer(np.log), log_attribs),
        ])      
        X = pipeline_step_2.fit_transform(X)

        # ------ 第四步，以DataFrame的形式输出 ------ #
        X_df = pd.DataFrame(X, columns=num_attribs + cat_attribs + log_attribs)

        # ------ 第五步，持久化存储 ------ #
        if self.is_save:
            # 创建存放数据的文件夹
            folder_name = "processed_data"
            data_folder = os.path.join(FilesIO.getDataset(), folder_name)
            if not os.path.exists(data_folder):
                os.mkdir(data_folder)
            else:
                pass

            # 以csv形式存储
            X_df.to_csv(
                FilesIO.getDataset(
                    "%s/%s_housing_data_processed.csv" % 
                    (folder_name, self.city_name)
                ), index=False, encoding="utf-8-sig"
            )
        return X_df


class DistanceToCityCenter(BaseEstimator, TransformerMixin):

    """
    数据处理模块——计算到市中心的距离
    """

    def __init__(self, city_name: str=None) -> None:

        self.city_name = city_name


    def fit(self, X, y=None):
        return self
    

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        """
        计算到市中心的距离
        """

        city_center_location = (
            CONST_TABLE["CITY_CENTER"][self.city_name]["LAT"],
            CONST_TABLE["CITY_CENTER"][self.city_name]["LNG"]
        )
        X.dropna(subset=["latitude", "longitude"], inplace=True)
        X.reset_index(drop=True, inplace=True)
        for i in range(len(X)):
            loc = (X.loc[i, "latitude"], X.loc[i, "longitude"])
            distance = geodesic(loc, city_center_location).kilometers
            X.loc[i, "distance"] = distance
        return X


class DropColumns(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self


    def transform(self, X:pd.DataFrame) -> pd.DataFrame:

        """
        某些列中NA并不代表缺失值，替换为None
        """

        cols_to_drop = ["ID", "houseLoc", "housePrice"]
        X = X.drop(columns=cols_to_drop)
        return X


class ReplaceNAtoNone(BaseEstimator, TransformerMixin):

    """
    数据处理模块——NA值处理
    """

    def fit(self, X, y=None):
        return self


    def transform(self, X:pd.DataFrame) -> pd.DataFrame:

        """
        某些列中NA并不代表缺失值，替换为None
        """

        X["houseHousingPeriod"].fillna("None", inplace=True)
        return X


class AddColumns(BaseEstimator, TransformerMixin):

    """
    数据处理模块——添加新的列
    TODO：添加关于地区的虚拟变量，考虑添加城市特征信息例如GDP等
    """

    pass