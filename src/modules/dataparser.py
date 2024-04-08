# ========================================= #
# @Author: Fantasy_Silence                  #
# @Time: 2024-04-04                         #
# @IDE: Visual Studio Code & PyCharm        #
# @Python: 3.9.7                            #
# ========================================= #
# @Description:                             #
# This module is used for parsing HTML data #
# ========================================= #
import pandas as pd
import numpy as np
from lxml import etree

from src.common.filesio import FilesIO
from src.common.const import CONST_TABLE
from src.common.lnglat import GetLongitudeLatitude


class HousingDataParse:

    """
    TODO：添加：后续应该会解析更多的信息
    封装一个数据解析类，用于解析爬取网页的html文件
    """

    def __init__(self, city: str) -> None:

        """
        city: 待解析数据的城市名称，如北京(city="BJ")
        """
        
        self.city = city

        # ------ 初始化存储爬取信息的列表，便于存入csv ------ #
        self.house_price_list = []          # 存储房价
        self.unit_price_list = []           # 存储每平方米价格
        self.house_area_list = []           # 存储房子面积
        self.house_loc_list = []            # 存储房子地址
        self.house_bedroom_list = []        # 存储房子卧室数量
        self.house_room_list = []           # 存储房子房间数量
        self.house_orientation_list = []    # 存储房子朝向
        self.house_age_list = []            # 存储房子年龄
        self.longitude_list = []            # 存储房子经度
        self.latitude_list = []             # 存储房子维度

        # ------ 提取 ------ #
        self._parse_data()
        self._parse_loc_to_lnglat()

        # ------ 存入csv文件中 ------ #
        self.df.to_csv(
            FilesIO.getDataset("%s_housing_data.csv" % self.city),
            index=False, encoding="utf-8-sig"
        )
    

    def _parse_data(self) -> None:

        """
        解析html文件，并将信息存储到列表中
        """

        for i in range(1, 51):

            # ------ 读取并解析html文件 ------ #
            path = FilesIO.getHTMLtext(
                "%s_htmls/%s_page_%d.html" % (self.city, self.city, i)
            )

            parser = etree.HTMLParser(encoding="utf-8")
            try:
                tree = etree.parse(path, parser=parser)
            except:
                pass

            # ------ 解析房价信息，并存储 ------ #
            house_price = tree.xpath(CONST_TABLE["XPATH"]["HOUSE_PRICE"])
            house_price_list = [i.strip() for i in house_price]
            self.house_price_list.extend(house_price_list)

            # ------ 解析每平方米房价信息，并存储 ------ #
            unit_price = tree.xpath(CONST_TABLE["XPATH"]["UNIT_PRICE"])
            unit_price_list = [i.strip()[:-3] for i in unit_price]
            self.unit_price_list.extend(unit_price_list)

            # ------ 解析房屋面积信息，并存储 ------ #
            house_area = tree.xpath(CONST_TABLE["XPATH"]["HOUSE_AREA"])
            house_area_list = [i.strip()[:-1] for i in house_area]
            self.house_area_list.extend(house_area_list)

            # ------ 解析房屋地址信息，并存储 ------ #
            community_loc = tree.xpath(CONST_TABLE["XPATH"]["COMMUNITY_LOCATION"])
            house_loc = tree.xpath(CONST_TABLE["XPATH"]["HOUSE_LOCATION"])
            house_loc_list = [i.strip() for i in house_loc]
            i = 2
            house_loc = []
            while i < len(house_loc_list):
                house_loc.append(house_loc_list[i-2] + house_loc_list[i-1] + house_loc_list[i])
                i += 3
            for i in range(len(community_loc)):
                house_loc[i] += community_loc[i]
            self.house_loc_list.extend(house_loc)

            # ------ 解析房屋房间数量信息，并存储 ------ #
            house_room = tree.xpath(CONST_TABLE["XPATH"]["HOUSE_ROOM_NUM"])
            i, house_room_patten_list = 5, []
            while i <= len(house_room):
                room_patten = "".join(house_room[i-5: i+1])
                i += 6
                room_num = sum(int(i) for i in room_patten if i.isdigit())
                house_room_patten_list.append(room_num)
            self.house_room_list.extend(house_room_patten_list)

            # ------ 解析房屋卧室数量信息，并存储 ------ #
            house_bedroom = tree.xpath(CONST_TABLE["XPATH"]["HOUSE_BEDROOM_NUM"])
            house_bedroom_list = [i.strip() for i in house_bedroom]
            self.house_bedroom_list.extend(house_bedroom_list)

            # ------ 解析房屋朝向信息，并存储 ------ #
            house_orientation = tree.xpath(CONST_TABLE["XPATH"]["HOUSE_FACING"])
            house_orientation_list = [i.strip() for i in house_orientation]
            self.house_orientation_list.extend(house_orientation_list)

            # ------ 解析房屋年龄信息，并存储 ------ #
            house_age = tree.xpath(CONST_TABLE["XPATH"]["HOUSE_AGE"])
            house_age_list = [
                2024 - int(i.strip()[:-3]) if i.strip()[0].isdigit() else np.nan 
                for i in house_age
            ]
            self.house_age_list.extend(house_age_list)

        # ------ 临时存入DataFrame, 用于去重 ------ #
        self.df = pd.DataFrame({
            "houseLoc": self.house_loc_list, "unitPrice": self.unit_price_list, 
            "housePrice": self.house_price_list, "houseArea": self.house_area_list,  
            "houseBedroom": self.house_bedroom_list, "houseRoom": self.house_room_list, 
            "houseOrientation": self.house_orientation_list, "houseAge": self.house_age_list, 
        })
        self.df.drop_duplicates(inplace=True, subset=["houseLoc"], keep="first")
            
    
    def _parse_loc_to_lnglat(self):

        """
        将房屋的地址信息转换为经纬度
        """

        # ------ 转换 ------ #
        for loc in self.df["houseLoc"].tolist():
            lnglat = GetLongitudeLatitude(
                city=CONST_TABLE["CITY"][self.city], address=loc
            )
            print(lnglat.longtitude, lnglat.latitude)
            self.longitude_list.append(lnglat.longtitude)
            self.latitude_list.append(lnglat.latitude)
        
        # ------ 生成最终的DataFrame ------ #
        self.df.insert(1, "longitude", self.longitude_list)
        self.df.insert(2, "latitude", self.latitude_list)
        self.df.insert(0, "ID", range(1, len(self.df) + 1))
