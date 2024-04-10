# ============================================================== #
# @Author: Fantasy_Silence                                       #
# @Time: 2024-04-04                                              #
# @IDE: Visual Studio Code & PyCharm                             #
# @Python: 3.9.7                                                 #
# ============================================================== #
# @Description:                                                  #
# This module encapsulates data crawling classes for easy reuse  #
# ============================================================== #
import os
import time
import random
import requests
from lxml import etree

from src.common.filesio import FilesIO
from src.common.const import CONST_TABLE


class HousingDataSpider:
    
    """
    封装一个数据爬取类，用于爬取网页的html文件
    """

    def __init__(
        self, city: str=None, headers: dict=None, 
        proxies: dict=None, cookie: str=None, max_retry: int=None
    ) -> None:
        
        """
        city: 待爬取城市, 例如北京市(city="BJ")
        headers: 请求头
        proxies: 代理IP
        max_retry: 最大重试次数，超过会放弃当前页的获取，默认一直爬直到获取到数据
        """

        # ------ 检查输入 ------ #
        if city is None or type(city) != str:
            print("ERROR: Inappropriate input of city name...")
            exit(1)
        elif city not in list(CONST_TABLE["CITY"].keys()) or\
             city not in list(CONST_TABLE["URL"].keys()) or\
             city not in list(CONST_TABLE["CITY_CENTER"].keys()):
            print("ERROR: City name not included, please add it in const.py")
            exit(1)
        else:
            self.city = city
        
        self.proxies = proxies
        self.headers = headers
        self.requests_num = 0       # 总请求次数，用于max_retry的验证
        if cookie is not None:
            self.headers["cookie"] = cookie

        # ------ 设置最大重试次数 ------ #
        if max_retry is None:
            # 默认一直请求直到获得数据
            self.flag = "True"
        else:
            # 小于等于max_retry时进行请求，超过则不再请求
            self.flag = "self.requests_num <= %d" % max_retry
        
        # ------ 创建存储数据的文件夹 ------ #
        self.folder_name = city + "_htmls"
        data_folder = os.path.join(FilesIO.getHTMLtext(), self.folder_name)
        if not os.path.exists(data_folder):
            os.mkdir(data_folder)
        else:
            pass

        # ------ 获取HTML数据 ------ #
        try:
            self._get_first_page_data()
            time.sleep(random.randint(5, 10))
            self._get_rest_of_pages()
        except:
            print("Error: Failed to get data from %s" % self.city) 


    def _get_first_page_data(self) -> None:

        """
        获取第一页的数据
        """

        while eval(self.flag):
            # 计数，循环每进行一次就会发一次请求
            self.requests_num += 1

            # ------ 设置随机延时避免反爬 ------ #
            time.sleep(random.randint(5, 10))

            # ------ 发送请求并设置编码 ------ #
            response = requests.get(
                url=CONST_TABLE["URL"][self.city],
                headers=self.headers, proxies=self.proxies,
            )
            response.encoding = "utf-8"

            # ------ 获取html文件并储存 ------ #
            tree = etree.HTML(response.text)
            if len(tree.xpath('//div[@class="property"]')) != 0:
                file_name = "%s_page_%d.html" % (self.city, 1)
                path = FilesIO.getHTMLtext("%s/%s" % (self.folder_name, file_name))
                with open(path, "w", encoding="utf-8") as f:
                    f.write(response.text)
                print("Get data from page_%d successfully!" % 1)
                # 数据请求成功，循环即将退出(break)，将该数字重置为0，以便下次继续使用
                self.requests_num = 0
                break
            else:
                print("ERROR: Failed to get data from page_1. Retry...")
        
        else:
            # 请求失败，循环正常退出，没走break
            # 说明达到最大重试次数，退出循环时将该数字重置为0，以便下次继续使用
            self.requests_num = 0
            print("ERROR: When getting data from page_1, max retry exceeded....")


    def _get_rest_of_pages(self) -> None:

        """
        获取其余页面的数据
        """

        for i in range(2, 51):
            while eval(self.flag):
                # 计数，循环每进行一次就会发一次请求
                self.requests_num += 1

                # ------ 设置随机延时避免反爬 ------ #
                time.sleep(random.randint(5, 10))

                # ------ 发送请求并设置编码 ------ #
                response = requests.get(
                    url=CONST_TABLE["URL"][self.city] + "p%d/" % i,
                    headers=self.headers, proxies=self.proxies,
                )
                response.encoding = "utf-8"

                # ------ 获取html文件并储存 ------ #
                tree = etree.HTML(response.text)
                if len(tree.xpath('//div[@class="property"]')) != 0:
                    file_name = "%s_page_%d.html" % (self.city, i)
                    path = FilesIO.getHTMLtext("%s/%s" % (self.folder_name, file_name))
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(response.text)
                    print("Get data from page_%d successfully!" % i)
                    # 数据请求成功，循环即将退出(break)，将该数字重置为0，以便下次继续使用
                    self.requests_num = 0
                    break
                else:
                    print("ERROR: Failed to get data from page_%d. Retry..." % i)

            else:
                # 请求失败，循环正常退出，没走break
                # 说明达到最大重试次数，退出循环时将该数字重置为0，以便下次继续使用
                self.requests_num = 0
                print("ERROR: When getting data from page_%d, max retry exceeded..." % i)
