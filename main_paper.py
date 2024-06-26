# =================================================================== #
# @Author: Fantasy_Silence                                            #
# @Time: 2024-04-24                                                   #
# @IDE: Visual Studio Code & PyCharm                                  #
# @Python: 3.9.7                                                      #
# =================================================================== #
# @Description: Reproduction of the entire process of the paper       #
# =================================================================== #
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, ShuffleSplit

from src.common.fileTool.filesio import FilesIO
from src.common.modelTool.modelsio import ModelsIO
from src.common.modelTool.split import TargetVaribleSplit
from src.modules.evaluation.pr_tradeoff import PRTradeOffCurve
from src.modules.evaluation.learning_curve import LearningCurve
from src.modules.evaluation.confusion_matrix import ConfusionMatrix
from src.modules.evaluation.feature_importance import FeatureImportance
from src.modules.visualization.target_in_paper import DrawTargetInPaper
from src.modules.datapreparation.pipelinepaper import PipeLineForPaperHousingData

# ==========
# 0.读取数据并处理
# ==========
print("=" * 50)
print("0.读取数据并处理")
print("=" * 50)
start_time = time.time()
row_data = pd.read_csv(FilesIO.getDataset(
    "house-prices-advanced-regression-techniques/train.csv"
))
pipe = Pipeline([
    ('prep', PipeLineForPaperHousingData()),
    ('split', TargetVaribleSplit(target="SalePrice")),
])
X_train, X_test, y_train, y_test = train_test_split(
    *pipe.fit_transform(row_data), test_size=0.3, random_state=42
)
X_train = X_train.drop(
    columns=["Exterior1st", "GarageQual", "GarageYrBlt", "1stFlrSF"],
)
X_test = X_test.drop(
    columns=["Exterior1st", "GarageQual", "GarageYrBlt", "1stFlrSF"],
)
end_time = time.time()
print(
    "完成'读取数据并处理', 用时%.3fms" % 
    ((end_time - start_time) * 1000), end="\n\n"
)

# ==========
# 1.计算文中提到的相关系数并绘制目标变量分布
# ==========
print("=" * 50)
print("1.计算文中提到的相关系数并绘制目标变量分布")
print("=" * 50)
start_time = time.time()
data_processed = PipeLineForPaperHousingData(is_drop=False).transform(row_data)
# 第一个相关系数
print(
    data_processed[
        ["GarageYrBlt", "YearBuilt", "1stFlrSF", "TotalBsmtSF"]
    ].corr(method="pearson"), end="\n\n"
)
# 第二个相关系数
print(
    data_processed[
        ["GarageYrBlt", "YearBuilt", "1stFlrSF", "TotalBsmtSF", "SalePrice"]
    ].corr(method="pearson")["SalePrice"], end="\n\n"
)
# 第三个相关系数
print(
    data_processed[
        ["Exterior1st", "Exterior2nd", "GarageCond", "GarageQual"]
    ].corr(method="kendall"), end="\n\n"
)
# 第四个相关系数
print(
    data_processed[
        ["Exterior1st", "Exterior2nd", "GarageCond", "GarageQual", "SalePrice"]
    ].corr(method="spearman")["SalePrice"], end="\n\n"
)
# 绘制目标变量分布情况
DrawTargetInPaper.draw(is_show=True, is_save=True)
end_time = time.time()
print(
    "完成'计算文中提到的相关系数并绘制目标变量分布', 用时%.3fms" % 
    ((end_time - start_time) * 1000), end="\n\n"
)

# ==========
# 2.训练决策树回归模型
# ==========
# Warning: This is a very long process.
# # RF_Regressor网格搜索
# from sklearn.model_selection import GridSearchCV
# from sklearn.ensemble import RandomForestRegressor
# param_grid_rf_regressor = {
#     "n_estimators": [100, 200, 300, 400, 500],
#     "max_features": [0.2, 0.4, 0.6, 0.8, 1],
#     "max_samples": [0.2, 0.4, 0.6, 0.8, 1],
#     "criterion": ['squared_error', 'absolute_error', 'friedman_mse', 'poisson'],
# }
# rf_grid_regressor = GridSearchCV(
#     estimator=RandomForestRegressor(), param_grid=param_grid_rf_regressor, 
#     cv=5, n_jobs=-1
# )
# rf_grid_regressor.fit(X_train, y_train)
# print(rf_grid_regressor.best_params_)

print("=" * 50)
print("2.训练决策树回归模型")
print("=" * 50)
start_time = time.time()
rf_model_paper = RandomForestRegressor(
    n_estimators=500, max_features=0.4, max_samples=0.8, 
    criterion="friedman_mse", random_state=42
)
rf_model_paper.fit(X_train, y_train)
y_pred = rf_model_paper.predict(X_test)

print("MSE(RandomForestRegressor):", mean_squared_error(y_test, y_pred))
print("R2(RandomForestRegressor):", r2_score(y_test, y_pred))

# 保存模型
ModelsIO.saveModel(rf_model_paper, "rf_regressor_paper.pkl")

FeatureImportance(
    rf_model_paper.feature_importances_, X_train.columns, 
    is_save=True, fig_name="RF_feature_importance_paper.png"
)
top30 = list(X_train.columns[
    rf_model_paper.feature_importances_.argsort()[-30:][::-1]
])
end_time = time.time()
print(
    "完成'训练决策树回归模型', 用时%.3fms" % 
    ((end_time - start_time) * 1000), end="\n\n"
)

# ==========
# 3.绘制学习曲线
# ==========
print("=" * 50)
print("3.绘制决策树回归模型的学习曲线")
print("=" * 50)
start_time = time.time()
cv = KFold(n_splits=5, shuffle=True, random_state=42)
_, ax = plt.subplots(figsize=(12, 8), dpi=100)
LearningCurve(
    rf_model_paper, X_train, y_train, cv=cv,
    train_sizes=np.linspace(0.1, 1.0, 10),
    scoring="neg_mean_squared_error", is_show_alone=False, ax=ax
)
ax.set_title("Learning Curve")
plt.tight_layout()
plt.show()
end_time = time.time()
print(
    "完成'绘制决策树回归模型的学习曲线', 用时%.3fms" % 
    ((end_time - start_time) * 1000), end="\n\n"
)

# ==========
# 4.训练XGBoost回归模型
# ==========
# Warning: This is a very long process.
# # XGB_Regressor网格搜索
# from xgboost import XGBRegressor
# from sklearn.model_selection import GridSearchCV
# param_grid_xgb_regressor = {
#     "n_estimators": [100, 200, 300],
#     "max_depth": [6, 7, 8],
#     "learning_rate": [0.1, 0.2, 0.3],
#     "objective": ["reg:squarederror", "reg:gamma"],
# }
# xgb_grid_regressor = GridSearchCV(
#     estimator=XGBRegressor(), param_grid=param_grid_xgb_regressor, 
#     cv=5, n_jobs=-1
# )
# xgb_grid_regressor.fit(X_train, y_train)
# print(xgb_grid_regressor.best_params_)

print("=" * 50)
print("4.训练XGBoost回归模型")
print("=" * 50)
start_time = time.time()
X_train_top30, X_test_top30 = X_train[top30], X_test[top30]

xgb_model_paper_best = XGBRegressor(
    max_depth=6, learning_rate=0.1, n_estimators=300, 
    objective='reg:gamma', random_state=42
)
xgb_model_paper_best.fit(X_train_top30, y_train)
y_pred = xgb_model_paper_best.predict(X_test_top30)

print("MSE(XGBRegressor):", mean_squared_error(y_test, y_pred))
print("R2(XGBRegressor):", r2_score(y_test, y_pred))

# 保存模型
ModelsIO.saveModel(xgb_model_paper_best, "xgb_regressor_paper.pkl")

FeatureImportance(
    xgb_model_paper_best.feature_importances_, X_train_top30.columns, 
    is_save=True, fig_name="XGB_feature_importance_paper.png"
)
end_time = time.time()
print(
    "完成'训练XGBoost回归模型', 用时%.3fms" % 
    ((end_time - start_time) * 1000), end="\n\n"
)

# ==========
# 5.绘制学习曲线
# ==========
print("=" * 50)
print("5.绘制XGBoost回归模型的学习曲线")
print("=" * 50)
start_time = time.time()
cv = KFold(n_splits=5, shuffle=True, random_state=42)
_, ax = plt.subplots(figsize=(12, 8), dpi=100)
LearningCurve(
    xgb_model_paper_best, X_train_top30, y_train, cv=cv,
    train_sizes=np.linspace(0.1, 1.0, 10),
    scoring="neg_mean_squared_error", is_show_alone=False, ax=ax
)
ax.set_title("Learning Curve")
plt.tight_layout()
plt.show()
end_time = time.time()
print(
    "完成'绘制XGBoost回归模型的学习曲线', 用时%.3fms" % 
    ((end_time - start_time) * 1000), end="\n\n"
)

# ==========
# 6.更换目标变量，并训练XGBClassifier
# ==========
print("=" * 50)
print("6.更换目标变量，并训练XGBClassifier")
print("=" * 50)
start_time = time.time()
# 提取的标签
binary_label = row_data.SalePrice < row_data.SalePrice.median()
binary_label = binary_label.astype(int)

# 修改已经处理好的数据
data_piped = PipeLineForPaperHousingData().transform(row_data)
data_for_classification = data_piped.copy()
data_for_classification["SalePrice"] = binary_label

# 分离目标与自变量
X, y = TargetVaribleSplit(target="SalePrice").transform(data_for_classification)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Warning: This is a very long process.
# # XGB_Classifier网格搜索
# from xgboost import XGBClassifier
# from sklearn.model_selection import GridSearchCV
# param_grid_xgb_classifier = {
#     "n_estimators": [100, 200, 300],
#     "max_depth": [6, 7, 8],
#     "learning_rate": [0.1, 0.2, 0.3],
#     "eval_metric": ["auc", "error", "logloss"]
# }
# xgb_grid_classifier = GridSearchCV(
#     estimator=XGBClassifier(), param_grid=param_grid_xgb_classifier,
#     cv=5, n_jobs=-1
# )
# xgb_grid_classifier.fit(X_train, y_train)
# print(xgb_grid_classifier.best_params_)

# 训练模型
clf_xgb = XGBClassifier(
    # n_estimators=200, max_depth=7, learning_rate=0.3, 
    # eval_metric="auc", random_state=42
    n_estimators=100, max_depth=8, learning_rate=0.1,
    eval_metric="auc", random_state=42
)
clf_xgb.fit(X_train, y_train)

# 预测并计算相关指标
y_pred = clf_xgb.predict(X_test)
y_score = clf_xgb.predict_proba(X_test)
print("\nClassification Report: \n", classification_report(y_test, y_pred))

# 保存模型
ModelsIO.saveModel(clf_xgb, "xgb_classifier_paper.pkl")

# 可视化混淆矩阵
label_mapping = {0: "Low House Price", 1: "High House Price"}
ConfusionMatrix(y_test, y_pred, label_map=list(label_mapping.values()))

# 绘制出特征重要性
FeatureImportance(
    clf_xgb.feature_importances_, X_train.columns, 
    is_save=True, fig_name="XGB_feature_importance_paper_cls.png"
)

# 绘制Precision和Recall曲线
PRTradeOffCurve(y_test, y_score, is_save=True, fig_name="XGB_PR_paper.png")

# 绘制学习曲线
cv = ShuffleSplit(n_splits=10, test_size=0.3, random_state=42)
LearningCurve(clf_xgb, X_train, y_train, cv=cv, scoring="accuracy")
end_time = time.time()
print(
    "完成'更换目标变量，并训练XGBClassifier', 用时%.3fms" % 
    ((end_time - start_time) * 1000), end="\n\n"
)
