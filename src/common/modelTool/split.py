# ================================================ #
# @Author: Fantasy_Silence                         #
# @Time: 2024-04-22                                #
# @IDE: Visual Studio Code & PyCharm               #
# @Python: 3.9.7                                   #
# ================================================ #
# @Description: The model mentioned in the paper   #
# ================================================ #
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class TargetVaribleSplit(BaseEstimator, TransformerMixin):

    """
    用于分离自变量与目标值
    """

    def __init__(self, target: str="unitPrice") -> None:
        
        self.target_variable = target

    def fit(self, X, y=None):
        return self
    
    def transform(self, X: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:

        y = X[self.target_variable].copy()
        X = X.drop(self.target_variable, axis=1)
        return X, y
