# ================================================= #
# @Author: Fantasy_Silence                          #
# @Time: 2024-04-11                                 #
# @IDE: Visual Studio Code & PyCharm                #
# @Python: 3.9.7                                    #
# ================================================= #
# Description:                                      #
# A pipeline for preprocessing the paper dataset    #
# ================================================= #
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import FunctionTransformer
from sklearn.base import BaseEstimator, TransformerMixin


class PipeLineForPaperHousingData:

    """
    实现论文中提到的数据的预处理流程
    """

    def __init__(self, is_drop: bool=True, is_replace: bool=True) -> None:
        
        self.is_drop = is_drop
        self.is_replace = is_replace

    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        # ------ 第一步，数据清洗 ------ #
        pipeline_step_1 = Pipeline([
            ("replace_na", ReplaceNAtoNone(self.is_replace)),
            ("drop_columns", DropColumns(self.is_drop)),
        ])
        X = pipeline_step_1.fit_transform(X)

        # ------ 第二步，数据预处理 ------ #
        num_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="mean")),
            ("std_scaler", StandardScaler()),
        ])      # 连续变量处理
        
        cat_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("ordinal_encoder", OrdinalEncoder()),
        ])      # 分类变量处理

        num_attribs = [col for col in X.columns if str(X[col].dtype) == 'float64']
        cat_attribs = [col for col in X.columns if str(X[col].dtype) != 'float64']
        transfer_pipe = ColumnTransformer([
            ("num", num_pipeline, num_attribs),
            ("cat", cat_pipeline, cat_attribs[:-1]),
            ("target", FunctionTransformer(np.log), [cat_attribs[-1]]),
        ])      # 合并上面两个管道
        X = transfer_pipe.fit_transform(X)
        X_df = pd.DataFrame(X, columns=num_attribs + cat_attribs)
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
