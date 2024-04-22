# ================================================= #
# @Author: Fantasy_Silence                          #
# @Time: 2024-04-11                                 #
# @IDE: Visual Studio Code & PyCharm                #
# @Python: 3.9.7                                    #
# ================================================= #
# Description:                                      #
# A pipeline for preprocessing the paper dataset    #
# ================================================= #
import os
import numpy as np
import pandas as pd
from typing import Literal
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import FunctionTransformer
from sklearn.base import BaseEstimator, TransformerMixin

from src.common.fileTool.filesio import FilesIO


class PipeLineForPaperHousingData(BaseEstimator, TransformerMixin):

    """
    实现论文中提到的数据的预处理流程
    """

    def __init__(
            self,file_name: Literal["train", "test"]="train",
            is_drop: bool=True, is_replace: bool=True, is_save: bool=False, 
    ) -> None:
        
        self.is_save = is_save
        self.is_drop = is_drop
        self.file_name = file_name
        self.is_replace = is_replace
    

    def fit(self, X, y=None):
        return self

    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        # ------ 第一步，数据清洗 ------ #
        pipeline_step_1 = Pipeline([
            # 某些NA值并非缺失值，这部分替换为None
            ("replace_na", ReplaceNAtoNone(self.is_replace)),
            # 去掉重复值太多的列
            ("drop_columns", DropColumns(self.is_drop)),
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
            ("ordinal_encoder", OrdinalEncoder()),
        ])      # 分类变量处理

        # ------ 分别提取连续变量和分类变量的列名 ------ #
        num_attribs = [col for col in X.columns if str(X[col].dtype) == 'float64']
        cat_attribs = [col for col in X.columns if str(X[col].dtype) != 'float64']
        
        # ------ 第三步，整合为一个管道 ------ #
        pipeline_step_2 = ColumnTransformer([
            ("num", num_pipeline, num_attribs),
            ("cat", cat_pipeline, cat_attribs[:-1]),
            # 对目标值取对数
            ("target", FunctionTransformer(np.log), [cat_attribs[-1]]),
        ])      
        X = pipeline_step_2.fit_transform(X)

        # ------ 第四步，以DataFrame的形式输出 ------ #
        X_df = pd.DataFrame(X, columns=num_attribs + cat_attribs)

        # ------ 第五步，持久化存储 ------ #
        if self.is_save:
            # 创建存放数据的文件夹
            folder_name = "house-prices-advanced-regression-techniques"
            data_folder = os.path.join(FilesIO.getDataset(), folder_name)
            if not os.path.exists(data_folder):
                os.mkdir(data_folder)
            else:
                pass

            # 以csv形式存储
            X_df.to_csv(
                FilesIO.getDataset(
                    "%s/%s_housing_data_processed.csv" % 
                    (folder_name, self.file_name)
                ), index=False, encoding="utf-8-sig"
            )
        return X_df
    

class ReplaceNAtoNone(BaseEstimator, TransformerMixin):

    """
    数据处理模块——NA值处理
    """

    def __init__(self, is_replace) -> None:

        self.is_replace = is_replace


    def fit(self, X, y=None):
        return self


    def transform(self, X:pd.DataFrame) -> pd.DataFrame:

        """
        某些列中NA并不代表缺失值，替换为None
        """

        cols_to_replace = [
            "Alley", "BsmtQual", "BsmtCond", "BsmtExposure", "BsmtFinType1",
            "BsmtFinType2", "FireplaceQu", "GarageType", "GarageFinish",
            "GarageQual", "GarageCond", "PoolQC", "Fence", "MiscFeature"
        ]
        if self.is_replace:
            for col in cols_to_replace:
                X[col].fillna("None", inplace=True)
        return X


class DropColumns(BaseEstimator, TransformerMixin):

    """
    数据预处理模块——删除部分数据
    """

    def __init__(self, is_drop: bool) -> None:

        self.is_drop = is_drop
        

    def fit(self, X, y=None):
        return self


    def transform(self, X:pd.DataFrame) -> pd.DataFrame:

        """
        删除重复值占比超过90%的列以及NaN太多的列
        """

        cols_to_drop = []
        for col in X.columns:
            values_count = X[col].value_counts(dropna=False)
            for value in values_count:
                if value / values_count.sum(skipna=False) >= 0.9:
                    cols_to_drop.append(col)
                    break
        cols_to_drop.append('Id')
        if self.is_drop:
            return X.drop(columns=cols_to_drop)
        else:
            return X
