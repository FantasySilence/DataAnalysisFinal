# =================================== #
# @Author: Fantasy_Silence            #
# @Time: 2024-04-03                   #
# @IDE: Visual Studio Code & PyCharm  #
# @Python: 3.9.7                      #
# =================================== #
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# 配置import路径信息
ROOTPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOTPATH)

# 测试完整流程，爬取，解析，存储，读取，可视化
from src.common.const import CONST_TABLE
from src.common.filesio import FilesIO
from src.common.randomIPandHeaders import RandomRequestInfoGenerator
from src.modules.datacrawler import HousingDataScrape
from src.modules.dataparser import HousingDataParse

proxies, headers = RandomRequestInfoGenerator.get()
scraper = HousingDataScrape(city="CD", headers=headers, proxies=proxies)
parser = HousingDataParse(city="CD")

CD_data = pd.read_csv(FilesIO.getDataset("CD_housing_data.csv"))
fig, ax = plt.subplots(figsize=(12, 8), dpi=100)
CD_data.plot(
    kind="scatter", x="longitude", y="latitude", alpha=0.6,
    s=CD_data["housePrice"] / 100, label="housePrice",
    c="unitPrice", cmap=plt.get_cmap("jet"), colorbar=True,
    sharex=False, ax=ax
)
ax.plot(
    CONST_TABLE["CITY_CENTER"]["CD"]["LNG"],
    CONST_TABLE["CITY_CENTER"]["CD"]["LAT"],
    "r*", markersize=10, label="city center"
)
ax.set_title("CD Housing Price Distribution")
ax.set_xlabel("longitude")
ax.set_ylabel("latitude")
ax.legend(loc="upper right")
plt.show()
