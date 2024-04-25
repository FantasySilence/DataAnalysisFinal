# ========================================= #
# @Author: Fantasy_Silence                  #
# @Time: 2024-04-04                         #
# @IDE: Visual Studio Code & PyCharm        #
# @Python: 3.9.7                            #
# ========================================= #
# @Description:                             #
# This module is used for parsing HTML data #
# ========================================= #
import os
import numpy as np
import pandas as pd
from lxml import etree
from functools import reduce

from src.common.fileTool.filesio import FilesIO
from src.common.infoTool.const import CONST_TABLE
from src.common.locTool.lnglat import GetLongitudeLatitude


class HousingDataParser:

    """
    封装一个数据解析类，用于解析爬取网页的html文件
    """

    def __init__(self, city: str=None) -> None:

        """
        city: 待解析数据的城市名称，如北京(city="BJ")
        """
        
        # ------ 检查输入 ------ #
        if city is None or type(city) != str:
            print("ERROR: Inappropriate input of city name...")
            exit(1)
        elif city not in list(CONST_TABLE["CITY"].keys()):
            print("ERROR: City name not included, please add it in const.py")
            exit(1)
        else:
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

        # ------ 创建存放数据的文件夹 ------ #
        folder_name = "rowdata"
        data_folder = os.path.join(FilesIO.getDataset(), folder_name)
        if not os.path.exists(data_folder):
            os.mkdir(data_folder)
        else:
            pass

        # ------ 存入csv文件中 ------ #
        self.df.to_csv(
            FilesIO.getDataset(
                "%s/%s_housing_data.csv" % (folder_name, self.city)
            ), index=False, encoding="utf-8-sig"
        )
    

    def _parse_data(self) -> None:

        """
        解析html文件，并将信息存储到列表中
        """

        print("Parsing data...")
        for j in range(1, 51):

            # ------ 读取并解析html文件 ------ #
            path = FilesIO.getHTMLtext(
                "%s_htmls/%s_page_%d.html" % (self.city, self.city, j)
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

            # ------ 解析进度 ------ #
            print(
                "Parsing...", 
                f'|{"■" * ((j + 1) * 50 // 51):50}|', 
                f'{(j + 1) * 100 // 51}%', end='\r'
            )

        # ------ 临时存入DataFrame, 用于去重 ------ #
        self.df = pd.DataFrame({
            "houseLoc": self.house_loc_list, "unitPrice": self.unit_price_list, 
            "housePrice": self.house_price_list, "houseArea": self.house_area_list,  
            "houseBedroom": self.house_bedroom_list, "houseRoom": self.house_room_list, 
            "houseOrientation": self.house_orientation_list, "houseAge": self.house_age_list, 
        })
        self.df.drop_duplicates(inplace=True, subset=["houseLoc"], keep="first")
        print("\nParsing complete...")
            
    
    def _parse_loc_to_lnglat(self):

        """
        将房屋的地址信息转换为经纬度
        """

        print("Parsing location to longitude and latitude...")
        # ------ 转换 ------ #
        for i in range(len(self.df["houseLoc"].tolist())):
            lnglat = GetLongitudeLatitude(
                city=CONST_TABLE["CITY"][self.city], 
                address=self.df["houseLoc"].tolist()[i]
            )
            self.longitude_list.append(lnglat.longtitude)
            self.latitude_list.append(lnglat.latitude)
            
            # ------ 解析进度 ------ #
            print(
                "Parsing...", 
                f'|{"■" * ((i + 1) * 50 // len(self.df["houseLoc"].tolist())):50}|', 
                f'{(i + 1) * 100 // len(self.df["houseLoc"].tolist())}%', end='\r'
            )
        
        # ------ 生成最终的DataFrame ------ #
        self.df.insert(1, "longitude", self.longitude_list)
        self.df.insert(2, "latitude", self.latitude_list)
        self.df.insert(0, "ID", range(1, len(self.df) + 1))
        print("\nParsing complete...")
    

    @staticmethod
    def parse_more(city: str) -> None:

        """
        用于解析更多信息的接口
        """

        # ------ 重新读取之前解析好的信息 ------ #
        data = pd.read_csv(FilesIO.getDataset(
            "row_data/%s_housing_data.csv" % city
        ))
        
        # ------ 初始化存储爬取信息的列表，便于存入csv ------ #
        key_house_loc_list = []         # 作为键值用于合并
        house_subway_list = []          # 存储房子是否临近地铁
        house_floor_type_list = []      # 存储房子所在楼层高低
        house_floor_sum_list = []       # 存储房子所在楼层总数
        house_housing_period_list = []  # 存储房子房本年限

        print("Parsing more data...")
        for j in range(1, 51):

            # ------ 重新读取html文件 ------ #
            path = FilesIO.getHTMLtext(
                "%s_htmls/%s_page_%d.html" % (city, city, j)
            )

            # ------ 解析存储信息的div标签 ------ #
            parser = etree.HTMLParser(encoding="utf-8")
            tree = etree.parse(path, parser=parser)
            divs = tree.xpath(CONST_TABLE["XPATH"]["ROOT_PATH"])

            # ------ 解析房屋地址信息，并作为键值存储 ------ #
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
            key_house_loc_list.extend(house_loc)

            # ------ 信息存储在房屋信息的tag中，提取这些tag ------ #
            tag_info = []
            for div in divs:
                spans = div.xpath(CONST_TABLE["XPATH"]["HOUSE_TAG"])
                near_metro = []
                for span in spans:
                    near_metro.append("".join(span.split()))
                tag_info.append(near_metro)
            
            # ------ 解析房屋是否近地铁 ------ #
            is_near_metro = [
                1 if "近地铁" in item else 0 
                for item in tag_info
            ]
            house_subway_list.extend(is_near_metro)

            # ------ 解析房屋的房本年限 ------ #
            fangben_info = []
            for item in tag_info:
                if "满五年" in item:
                    fangben_info.append("满五年")
                elif "满二年" in item:
                    fangben_info.append("满二年")
                else:
                    fangben_info.append(np.nan)
            house_housing_period_list.extend(fangben_info)

            # ------ 解析房屋的楼层(高中低)与楼层总数 ------ #
            info_list = []      # 获取存储信息的div标签中的所有文字
            for div in range(len(divs)):
                ps = divs[div].xpath(CONST_TABLE["XPATH"]["HOUSE_FLOOR"])
                sub_info_list = []
                for text in ps:
                    sub_info_list.append("".join(text.split()))
                info_list.append(sub_info_list)

            for item in info_list:
                try:
                    # 获取楼层高低以及总层数
                    if item[2][:2] in ["低层", "中层", "高层"]:
                        house_floor_type_list.append(item[2][:2])
                        house_floor_sum_list.append(
                            int("".join([i for i in item[2] if i.isdigit()]))
                        )
                    else:
                        # 楼层高低可能缺失
                        house_floor_type_list.append(np.nan)
                        house_floor_sum_list.append(
                            int("".join([i for i in item[2] if i.isdigit()]))
                        )
                # 楼层高低可能缺失，总层数也可能缺失
                except IndexError:
                    house_floor_type_list.append(np.nan)
                    house_floor_sum_list.append(np.nan)
            
            # ------ 解析进度 ------ #
            print(
                "Parsing...", 
                f'|{"■" * ((j + 1) * 50 // 51):50}|', 
                f'{(j + 1) * 100 // 51}%', end='\r'
            )
        
        # ------ 与data合并重新储存 ------ #
        # 临时创建DataFrame存储
        df = pd.DataFrame({
            "houseLoc": key_house_loc_list, "houseSubway": house_subway_list,
            "houseHousingPeriod": house_housing_period_list,
            "houseFloorType": house_floor_type_list, 
            "houseFloorSum": house_floor_sum_list
        })
        df.drop_duplicates(inplace=True, subset=["houseLoc"], keep="first")
        
        # 以houseLoc为键值进行合并
        res = pd.merge(data, df, on="houseLoc")
        res.to_csv(
            FilesIO.getDataset("%s_housing_data.csv" % city), 
            index=False, encoding="utf-8-sig"
        )
        print("\nParsing complete...")
        