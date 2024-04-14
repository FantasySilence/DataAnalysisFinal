# ======================================================================= #
# @Author: Fantasy_Silence                                                #
# @Time: 2024-04-06                                                       #
# @IDE: Visual Studio Code & PyCharm                                      #
# @Python: 3.9.7                                                          #
# ======================================================================= #
# @Description:                                                           #
# This module realizes the conversion of Baidu coordinate system (BD-09)  #
# to Mars coordinate system (GCJ-02), and the conversion from Mars        #
# coordinate system (GCJ-02) to WGS84 coordinate system                   #
# ======================================================================= #
import math

# ------ 一些常量 ------ #
X_PI = 3.14159265358979324 * 3000.0 / 180.0
PI = 3.1415926535897932384626                   # π
LONG_SEMIAXIS = 6378245.0                       # 长半轴
ECCENTRICITY_SQUARED = 0.00669342162296594323   # 偏心率平方


class CoordTransformer:

    """
    参考自GitHub上项目
    https://github.com/wandergis/coordTransform_py
    将百度坐标系(BD-09)转换为火星坐标系(GCJ-02)，
    并从火星坐标系(GCJ-02)转换为WGS84坐标系
    """

    def __init__(self, lng: float, lat: float) -> None:
        
        """
        lng: 百度坐标系下的经度
        lat: 百度坐标系下的纬度
        """

        self.lng = lng
        self.lat = lat
        self.res_lng, self.res_lat = self.__transform__()


    @staticmethod
    def __pre_trans_lat__(lng: float, lat: float) -> float:
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * PI) + 20.0 * math.sin(2.0 * lng * PI)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * PI) + 40.0 * math.sin(lat / 3.0 * PI)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * PI) + 320 * math.sin(lat * PI / 30.0)) * 2.0 / 3.0
        return ret
    

    @staticmethod
    def __pre_trans_lng__(lng: float, lat: float) -> float:
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * PI) + 20.0 * math.sin(2.0 * lng * PI)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * PI) + 40.0 * math.sin(lng / 3.0 * PI)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * PI) + 300.0 * math.sin(lng / 30.0 * PI)) * 2.0 / 3.0
        return ret


    def __transform__(self) -> tuple[float, float]:

        """
        坐标转换主函数
        """

        # ------ 从百度坐标系(BD-09)转换为火星坐标系(GCJ-02) ------ #
        x = self.lng - 0.0065
        y = self.lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * X_PI)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * X_PI)
        gg_lng = z * math.cos(theta)
        gg_lat = z * math.sin(theta)

        # ------ 从火星坐标系(GCJ-02)转换为WGS84坐标系 ------ #
        dlat = self.__pre_trans_lat__(gg_lng - 105.0, gg_lat - 35.0)
        dlng = self.__pre_trans_lng__(gg_lng - 105.0, gg_lat - 35.0)
        radlat = gg_lat / 180.0 * PI
        magic = math.sin(radlat)
        magic = 1 - ECCENTRICITY_SQUARED * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((LONG_SEMIAXIS * (1 - ECCENTRICITY_SQUARED)) / (magic * sqrtmagic) * PI)
        dlng = (dlng * 180.0) / (LONG_SEMIAXIS / sqrtmagic * math.cos(radlat) * PI)
        mglat = gg_lat + dlat
        mglng = gg_lng + dlng
        return gg_lng * 2 - mglng, gg_lat * 2 - mglat
