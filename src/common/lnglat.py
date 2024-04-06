# ======================================================== #
# @Author: Fantasy_Silence                                 #
# @Time: 2024-04-04                                        #
# @IDE: Visual Studio Code & PyCharm                       #
# @Python: 3.9.7                                           #
# ======================================================== #
# @Description:                                            #
# This module encapsulates the class that converts         # 
# addresses to latitude and longitude                      # 
# ======================================================== #
import requests


class GetLongitudeLatitude:

    """
    获取某个地址的经纬度
    """

    def __init__(self, city: str, address: str) -> None:

        """
        初始化参数
        """

        self.url = "https://api.map.baidu.com/geocoding/v3"
        self.ak = "Z5CdwnD18hEKQcHgEgBiGvFYlnrOqGWC"
        self.city = city
        self.address = address
        self.longtitude = None
        self.latitude = None

        try:
            self.get_longitude_latitude()
        except:
            print("请求失败")
    

    def get_longitude_latitude(self) -> None:

        """
        获取经纬度
        """

        params = {
            "address": self.address,
            "city": self.city,
            "output": "json",
            "ak": self.ak
        }
        response = requests.get(url=self.url, params=params)
        res = response.json()
        self.longtitude = res['result']['location']['lng']
        self.latitude = res['result']['location']['lat']