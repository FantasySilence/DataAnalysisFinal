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
import matplotlib.pyplot as plt

from src.common.infoTool.const import CONST_TABLE
from src.modules.datapreparation.dataparser import HousingDataParser
from src.modules.datapreparation.datacrawler import HousingDataSpider
from src.modules.visualization.geo_distribute import DrawGeoDistribution
from src.common.infoTool.randomIPandHeaders import RandomRequestInfoGenerator
from src.modules.visualization.house_characteristics import DrawCharacteristicsOfHouse
from src.modules.visualization.age_price_relation import DrawRelationBetweenAgeAndPrice
from src.modules.visualization.price_area_relation import DrawRelationBetweenPriceAndArea


# ================
# 0.数据爬取与解析
# ================
# warning: This part requires nice net and takes a loooong time.
print("=" * 50)
print("0.数据爬取与解析")
print("=" * 50)
start_time = time.time()
for city in CONST_TABLE["CITY"].keys():
    proxies, headers = RandomRequestInfoGenerator.get()
    HousingDataSpider(city=city, headers=headers, proxies=proxies)
    HousingDataParser(city=city)
end_time = time.time()
print(
    "完成'数据爬取与解析', 用时%.3fms" % 
    ((end_time - start_time) * 1000), end="\n\n"
)

# ================
# 1.数据可视化(以北上广以及成都市为例)
# TODO: 这只是一个Demo，后续会更加详细
# ================
print("=" * 50)
print("1.数据可视化")
print("=" * 50)
start_time = time.time()

# 图1(一些特征的分布)
fig, axes = plt.subplots(4, 4, figsize=(16, 16), dpi=100)
DrawCharacteristicsOfHouse(city="CD").draw(
    is_show=False, is_show_alone=False, is_save=False, axes=axes[:2, :2]
)
DrawCharacteristicsOfHouse(city="BJ").draw(
    is_show=False, is_show_alone=False, is_save=False, axes=axes[2:, :2]
)
DrawCharacteristicsOfHouse(city="SH").draw(
    is_show=False, is_show_alone=False, is_save=False, axes=axes[:2, 2:]
)
DrawCharacteristicsOfHouse(city="GZ").draw(
    is_show=False, is_show_alone=False, is_save=False, axes=axes[2:, 2:]
)
plt.tight_layout()

# 图2(地理分布图)
fig, axes = plt.subplots(2, 2, figsize=(20, 16), dpi=100)
DrawGeoDistribution(city="CD").draw(
    is_show=False, is_show_alone=False, is_save=False, ax=axes[0, 0]
)
DrawGeoDistribution(city="BJ").draw(
    is_show=False, is_show_alone=False, is_save=False, ax=axes[0, 1]
)
DrawGeoDistribution(city="SH").draw(
    is_show=False, is_show_alone=False, is_save=False, ax=axes[1, 0]
)
DrawGeoDistribution(city="GZ").draw(
    is_show=False, is_show_alone=False, is_save=False, ax=axes[1, 1]
)
plt.tight_layout()
plt.show()

# 为地理分布图添加地图
cities = ["BJ", "CD", "SH", "GZ"]
for city in cities:
    DrawGeoDistribution(city=city).draw(
        is_show=False, is_save=False, is_map_show=True
    )

end_time = time.time()
print(
    "完成'数据可视化', 用时%.3fms" % 
    ((end_time - start_time) * 1000), end="\n\n"
)

# =====================
# 2.数据预处理与特征工程
# =====================

# ================
# 3.模型训练
# ================
# TODO: 可能会使用到的模型List:
"""
我计划直接根据近期的房产数据预测某个位置的房价
但实际中这可能较难做到。不过消费者可以很清楚的知道该市房价的平均水平
因此可以将房价划分为两类，进行分类任务，预测某个位置的房价是否高于平均水平
一、计划使用的回归模型
1. XGBoost Regressor
2. AdaBoost Regressor
3. Gradient Boosting Regressor
4. Random Forest Regressor
5. Decision Tree Regressor
6. SVM Regressor
7. SGD Regressor
8. Linear Regressor
9. Elastic Net Regressor
二、计划使用的分类模型(二分类)
1. XGBClassifier
2. AdaBoostClassifier
3. GradientBoostingClassifier
4. RandomForestClassifier
5. DecisionTreeClassifier
6. SVC
7. SGDClassifier
8. LinearDiscriminantAnalysis
9. LogisticRegression
"""
