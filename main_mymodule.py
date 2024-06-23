# =================================== #
# @Author: Fantasy_Silence            #
# @Time: 2024-04-24                   #
# @IDE: Visual Studio Code & PyCharm  #
# @Python: 3.9.7                      #
# =================================== #
# @Description: Using my data         #
# =================================== #
import time
import pandas as pd
import seaborn as sns
from sklearn.svm import SVR
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression, ElasticNet, SGDRegressor 
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import KFold, cross_val_score, train_test_split, GridSearchCV

from src.common.fileTool.filesio import FilesIO
from src.common.infoTool.const import CONST_TABLE
from src.common.modelTool.split import TargetVaribleSplit
from src.modules.datapreparation.dataparser import HousingDataParser
from src.modules.datapreparation.datacrawler import HousingDataSpider
from src.modules.visualization.geo_distribute import DrawGeoDistribution
from src.modules.datapreparation.pipeline58 import PipeLineFor58HousingData
from src.common.infoTool.randomIPandHeaders import RandomRequestInfoGenerator

# ====================
# 1.数据爬取与解析
# ====================
# warning: This is a long process, please read for more details in README
print("=" * 50)
print("1.数据爬取与解析")
print("=" * 50)
start_time = time.time()
# for city in CONST_TABLE["CITY"].keys():
#     proxies, headers = RandomRequestInfoGenerator.get()
#     HousingDataSpider(city=city, headers=headers, proxies=proxies)
#     HousingDataParser(city=city)
end_time = time.time()
print(
    "完成'数据爬取与解析', 用时%.3fms" % 
    ((end_time - start_time) * 1000), end="\n\n"
)

# ====================
# 2.数据可视化(以成都房价为例)
# ====================
row_data = pd.read_csv(FilesIO.getDataset("row_data/CD_housing_data.csv"))
DrawGeoDistribution("CD").draw(is_show_alone=True, is_show=True)

# ====================
# 2.1.数据预处理并划分训练集
# ====================
print("=" * 50)
print("2.1.数据预处理并划分训练集")
print("=" * 50)
start_time = time.time()
pipe_CD = Pipeline([
    ('prep', PipeLineFor58HousingData(city_name="CD")),
    ('split', TargetVaribleSplit(target="unitPrice")),
])
X_train, X_test, y_train, y_test = train_test_split(
    *pipe_CD.fit_transform(row_data), test_size=0.3, random_state=42
)
end_time = time.time()
print(
    "完成'数据预处理并划分训练集', 用时%.3fms" % 
    ((end_time - start_time) * 1000), end="\n\n"
)

# ====================
# 2.2.寻找最佳的模型
# ====================
print("=" * 50)
print("2.2.寻找最佳的模型")
print("=" * 50)
models = []
models.append(("Tree", DecisionTreeRegressor()))
models.append(("SVM", SVR()))
# 线性模型
models.append(("LR", LinearRegression()))
models.append(("ElasticNet", ElasticNet()))
models.append(("SGD", SGDRegressor()))
# Bagging
models.append(("RF", RandomForestRegressor()))
# Boost
models.append(("GB", GradientBoostingRegressor()))
models.append(("Ada", AdaBoostRegressor()))

results = []
names = []
for name, model in models:
    kfold = KFold(n_splits=10, random_state=42, shuffle=True)
    cv_results = cross_val_score(
        model, X_train, y_train, cv=kfold, 
        scoring="neg_mean_squared_error", n_jobs=-1
    )
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)

fig, ax = plt.subplots(1, 1, figsize=(12, 8), dpi=100)
sns.boxplot(results, ax=ax)
ax.set_title('Algorithm Comparison')
ax.set_xticklabels(names)
plt.show()
end_time = time.time()
print(
    "完成'寻找最佳的模型', 用时%.3fms" % 
    ((end_time - start_time) * 1000), end="\n\n"
)

# ====================
# 2.3.对最佳选择进行网格搜索
# ====================
print("=" * 50)
print("2.3.对最佳选择进行网格搜索")
print("=" * 50)
start_time = time.time()
# param_grid = {
#     "n_estimators": [100, 200, 300, 400, 500],
#     "max_features": [0.2, 0.4, 0.6, 0.8, 1],
#     "max_samples": [0.2, 0.4, 0.6, 0.8, 1],
#     "criterion": ['squared_error', 'absolute_error', 'friedman_mse', 'poisson'],
# }
# kfold = KFold(n_splits=10, random_state=42, shuffle=True)
# grid_search = GridSearchCV(
#     estimator=RandomForestRegressor(random_state=42, n_jobs=-1),
#     param_grid=param_grid, cv=kfold, n_jobs=-1, verbose=2
# )
# grid_search.fit(X_train, y_train)
# print(grid_search.best_params_)
end_time = time.time()
print(
    "完成'对最佳选择进行网格搜索', 用时%.3fms" % 
    ((end_time - start_time) * 1000), end="\n\n"
)

# ====================
# 2.4.使用最佳模型，进行评估
# ====================
print("=" * 50)
print("2.4.使用最佳模型，进行评估")
print("=" * 50)
start_time = time.time()
best_regressor = RandomForestRegressor(
    n_estimators=400, max_features=0.4, max_samples=0.8, criterion="squared_error"
)
best_regressor.fit(X_train, y_train)
y_pred = best_regressor.predict(X_test)
fig, ax = plt.subplots(figsize=(10, 5), dpi=100)
ax.scatter(y_test, y_pred, c="b", alpha=0.5)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "k--", lw=2)
ax.set_title("Actual vs Predicted", fontsize=16)
ax.set_ylabel("Predicted Value", fontsize=12)
ax.set_xlabel("Actual Value", fontsize=12)
end_time = time.time()
print(
    "完成'使用最佳模型，进行评估', 用时%.3fms" % 
    ((end_time - start_time) * 1000), end="\n\n"
)
plt.show()

# =================
# 3.提升模型泛化能力
# =================
print("=" * 50)
print("3.1.重新生成训练集")
print("=" * 50)
start_time = time.time()
train_data = pd.DataFrame()
test_data = pd.DataFrame()
for city in CONST_TABLE["CITY"].keys():

    # ------ 读取数据 ------ #
    df = pd.read_csv(FilesIO.getDataset(f"row_data/{city}_housing_data.csv"))

    # ------ 处理数据 ------ #
    pipe_i = Pipeline([
        ('prep', PipeLineFor58HousingData(city_name=city)),
    ])
    df_processed = pipe_i.fit_transform(df)

    # ------ 随机选择900条组成新的训练集，剩下的为测试集 ------ #
    df_train = df_processed.sample(n=900, replace=False)
    df_test = df_processed.drop(df_train.index)
    train_data = pd.concat([train_data, df_train])
    test_data = pd.concat([test_data, df_test])

# ------ 分离特征与目标变量 ------ #
pipe_all = Pipeline([
    ('split', TargetVaribleSplit(target="unitPrice")),
])
X_train_balanced, y_train_balanced = pipe_all.fit_transform(train_data)
X_test_balanced, y_test_balanced = pipe_all.fit_transform(test_data)
X_train_balanced.fillna(0, inplace=True)
y_train_balanced.fillna(0, inplace=True)
end_time = time.time()
print(
    "完成'重新生成训练集', 用时%.3fms" % 
    ((end_time - start_time) * 1000), end="\n\n"
)

print("=" * 50)
print("3.2.寻找最佳的模型")
print("=" * 50)
start_time = time.time()
models = []
models.append(("Tree", DecisionTreeRegressor()))
models.append(("SVM", SVR()))
# 线性模型
models.append(("LR", LinearRegression()))
models.append(("ElasticNet", ElasticNet()))
models.append(("SGD", SGDRegressor()))
# Bagging
models.append(("RF", RandomForestRegressor()))
# Boost
models.append(("GB", GradientBoostingRegressor()))
models.append(("Ada", AdaBoostRegressor()))

results = []
names = []
for name, model in models:
    kfold = KFold(n_splits=10, random_state=42, shuffle=True)
    cv_results = cross_val_score(
        model, X_train_balanced, y_train_balanced, 
        cv=kfold, scoring="neg_mean_squared_error", n_jobs=-1
    )
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)

fig, ax = plt.subplots(1, 1, figsize=(12, 8), dpi=100)
sns.boxplot(results, ax=ax)
ax.set_title('Algorithm Comparison')
ax.set_xticklabels(names)
end_time = time.time()
print(
    "完成'寻找最佳的模型', 用时%.3fms" % 
    ((end_time - start_time) * 1000), end="\n\n"
)
plt.show()

# ====================
# 3.3.对最佳选择进行网格搜索
# ====================
# warning: this is a very looooooooooooong process
print("=" * 50)
print("3.3.对最佳选择进行网格搜索")
print("=" * 50)
start_time = time.time()
# param_grid = {
#     "n_estimators": [100, 200, 300],
#     "max_features": [0.2, 0.4, 0.6],
#     "max_samples": [0.2, 0.4, 0.6], 
# }
# kfold = KFold(n_splits=5, random_state=42, shuffle=True)
# grid_search = GridSearchCV(
#     estimator=RandomForestRegressor(random_state=42, n_jobs=-1),
#     param_grid=param_grid, cv=kfold, n_jobs=-1, verbose=2
# )
# grid_search.fit(X_train_balanced, y_train_balanced)
# print(grid_search.best_params_)
end_time = time.time()
print(
    "完成'对最佳选择进行网格搜索', 用时%.3fms" %
    ((end_time - start_time) * 1000), end="\n\n"
)

# ====================
# 3.4.评估结果
# ====================
print("=" * 50)
print("3.4.评估结果")
print("=" * 50)
balanced_regressor = RandomForestRegressor(
    n_estimators=200, max_features=0.8, max_samples=0.6, criterion="squared_error"
)
balanced_regressor.fit(X_train, y_train)
y_pred = balanced_regressor.predict(X_test)

fig, ax = plt.subplots(figsize=(10, 5), dpi=100)
ax.scatter(y_test, y_pred, c="b", alpha=0.5)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "k--", lw=2)
ax.set_title("Actual vs Predicted", fontsize=16)
ax.set_ylabel("Predicted Value", fontsize=12)
ax.set_xlabel("Actual Value", fontsize=12)
end_time = time.time()
print(
    "完成'评估结果', 用时%.3fms" %
    ((end_time - start_time) * 1000), end="\n\n"
)
plt.show()
