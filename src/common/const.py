# ======================================================= #
# @Author: Fantasy_Silence                                #
# @Time: 2024-04-03                                       #
# @IDE: Visual Studio Code & PyCharm                      #
# @Python: 3.9.7                                          #
# ======================================================= #
# @Description:                                           #
# This module stores some commonly used constants         #
# ======================================================= #

CONST_TABLE = {
    # ------ 全国12座城市的二手房数据url, 每个有50页数据 ------ #
    "URL": {
        # 北京市数据
        "BJ": "https://bj.58.com/ershoufang/",

        # 上海市数据
        "SH": "https://sh.58.com/ershoufang/",

        # 广州市数据
        "GZ": "https://gz.58.com/ershoufang/",

        # 深圳市数据
        "SZ": "https://sz.58.com/ershoufang/",

        # 成都市数据
        "CD": "https://cd.58.com/ershoufang/",

        # 杭州市数据
        "HZ": "https://hz.58.com/ershoufang/",

        # 南京市数据
        "NJ": "https://nj.58.com/ershoufang/",

        # 天津市数据
        "TJ": "https://sz.58.com/ershoufang/",

        # 武汉市数据
        "WH": "https://wh.58.com/ershoufang/",

        # 重庆市数据
        "CQ": "https://cq.58.com/ershoufang/",

        # 厦门市数据
        "XM": "https://xm.58.com/ershoufang/",

        # 长沙市数据
        "CS": "https://cs.58.com/ershoufang/",

        # 哈尔滨市数据
        "HRB": "https://hrb.58.com/ershoufang/"
    },

    # ------ 解析数据的xpath表达式 ------ #
    "XPATH": {
        # 用于解析房价的xpath表达式
        "HOUSE_PRICE": "//div[@class='property']//div[2]/div[2]//span[@class='property-price-total-num']/text()",

        # 用于解析住房地址的xpath表达式
        "HOUSE_LOCATION": "//div[@class='property']//div[2]/div[1]//section/div[2]/p[2]//text()",

        # 用于解析住房小区地址的xpath表达式
        "COMMUNITY_LOCATION": "//div[@class='property']//div[2]/div[1]//section/div[2]/p[1]//text()",

        # 用于解析房屋面积的xpath表达式
        "HOUSE_AREA": "//div[@class='property']//div[2]/div[1]//section//p[2]/text()",

        # 用于解析每平方米价格的xpath表达式
        "UNIT_PRICE": "//div[@class='property']//div[2]/div[2]/p[2]/text()",

        # 用于解析房间数量的xpath表达式
        "HOUSE_ROOM_NUM": "//div[@class='property']//div[2]//section//p[1]/span/text()",

        # 用于解析卧室数量的xpath表达式
        "HOUSE_BEDROOM_NUM": "//div[@class='property']//div[2]//section//p[1]/span[1]/text()",

        # 用于解析朝向的xpath表达式
        "HOUSE_FACING": "//div[@class='property']//div[2]//section//p[3]/text()",

        # 用于解析房龄的xpath表达式
        "HOUSE_AGE": "//div[@class='property']//div[2]//section//p[last()]/text()",
    },

    # ------ 城市名称 ------ #
    "CITY": {
        # 北京市
        "BJ": "北京市",

        # 上海市
        "SH": "上海市",

        # 广州市
        "GZ": "广州市",

        # 深圳市
        "SZ": "深圳市",

        # 成都市
        "CD": "成都市",

        # 杭州市
        "HZ": "杭州市",

        # 南京市
        "NJ": "南京市",

        # 天津市
        "TJ": "天津市",

        # 武汉市
        "WH": "武汉市",

        # 重庆市
        "CQ": "重庆市",

        # 厦门市
        "XM": "厦门市",

        # 长沙市
        "CS": "长沙市",

        # 哈尔滨市
        "HRB": "哈尔滨市"
    }
}
