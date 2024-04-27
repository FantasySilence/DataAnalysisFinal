# ========================================================================== #
# @Author: Fantasy_Silence                                                   #
# @Time: 2024-04-27                                                          #
# @IDE: Visual Studio Code & PyCharm                                         #
# @Python: 3.9.7                                                             #
# ========================================================================== #
# @Description: Used to obtain POI information for the current location      #
# ========================================================================== #
import requests


class POICollector:

    """
    用于获取当前位置的poi信息
    主要用于检索当前地点附近的情况
    """

    def __init__(
            self, query: str, lat: float, lng: float, radius: int=2000
    ) -> None:
        
        """
        初始化参数
        query: 检索目标
        lat, lng: 当前位置的坐标
        """

        self.url = "https://api.map.baidu.com/place/v2/search"
        # 这里的ak密钥只是一个示例，请自行替换...
        self.ak = "Z5CdwnD18hEKQcHgEgBiGvFYlnrOqGWC"
        self.query = query
        self.location = f"{lat},{lng}"
        self.radius = radius

        # ------ 检索结果 ------ #
        self.num_of_query = None

        try:
            self.get_poi_info()
        except:
            print("请求失败")


    def get_poi_info(self):

        params = {
            "query": self.query,
            "location": self.location,
            "radius": "%d" % self.radius,
            "output": "json",
            "ak": self.ak,
        }

        response = requests.get(url=self.url, params=params)
        res = response.json()

        # ------ 从返回的json文件中获取结果 ------ #
        if res["status"] == 0:
            self.num_of_query = len(res["results"])
        else:
            self.num_of_query = None
