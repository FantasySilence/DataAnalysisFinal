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
        "BJ": "https://bj.58.com/ershoufang/",
        "SH": "https://sh.58.com/ershoufang/",
        "GZ": "https://gz.58.com/ershoufang/",
        "SZ": "https://sz.58.com/ershoufang/",
        "CD": "https://cd.58.com/ershoufang/",
        "HZ": "https://hz.58.com/ershoufang/",
        "NJ": "https://nj.58.com/ershoufang/",
        "TJ": "https://tj.58.com/ershoufang/",
        "WH": "https://wh.58.com/ershoufang/",
        "CQ": "https://cq.58.com/ershoufang/",
        "XM": "https://xm.58.com/ershoufang/",
        "CS": "https://cs.58.com/ershoufang/",
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
        "BJ": "北京市", "SH": "上海市", "GZ": "广州市",
        "SZ": "深圳市", "CD": "成都市", "HZ": "杭州市",
        "NJ": "南京市", "TJ": "天津市", "WH": "武汉市",
        "CQ": "重庆市", "XM": "厦门市", "CS": "长沙市",
    },

    # ------ 各个城市的市中心的经纬度 ------ #
    "CITY_CENTER": {
        "BJ": {
            "LNG": 116.39134675370828, "LAT": 39.907372429456956
        },
        "SH": {
            "LNG": 121.49533505039834, "LAT": 31.241787725896685
        },
        "CD": {
            "LNG": 104.06332036184781, "LAT": 30.659820156060174
        },
        "GZ": {
            "LNG": 113.31912152885295, "LAT": 23.109060934447577
        },
        "SZ": {
            "LNG": 114.05033438455155, "LAT": 22.53654762108978
        },
        "NJ": {
            "LNG": 118.77969695020998, "LAT": 32.04601840626671
        },
        "HZ": {
            "LNG": 120.15775362566102, "LAT": 30.255664035208536
        },
        "TJ": {
            "LNG": 117.19637735879652, "LAT": 39.12863570674569
        },
        "WH": {
            "LNG": 114.28587566200348, "LAT": 30.581186676510725
        },
        "CQ": {
            "LNG": 106.58418534613907, "LAT": 29.56969092533077
        },
        "XM": {
            "LNG": 118.10291951230721, "LAT": 24.488704693621322
        },
        "CS": {
            "LNG": 112.97183346189286, "LAT": 28.19834354882077
        }
    }
}
