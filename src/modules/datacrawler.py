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

from src.common.const import CONST_TABLE
from src.common.filesio import FilesIO


class HousingDataScrape:
    
    """
    封装一个数据爬取类，用于爬取网页的html文件
    """

    def __init__(
        self, city: str=None, headers: dict=None, 
        proxies: dict=None, cookie: str=None
    ) -> None:
        
        """
        city: 待爬取城市, 例如北京市(city="BJ")
        headers: 请求头
        proxies: 代理IP
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
        
        self.proxies = proxies
        self.headers = headers
        if cookie is not None:
            self.headers["cookie"] = cookie
        
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

        # BUG: 一个小bug，请求不到数据会尝试直到成功
        # FIXME: 需修复，添加最大请求次数解决陷入死循环的bug
        while True:
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
                break
            else:
                print("ERROR: Failed to get data from page_1. Retry...")


    def _get_rest_of_pages(self) -> None:

        """
        获取其余页面的数据
        """

        for i in range(2, 51):
            # BUG: 一个小bug，请求不到数据会尝试直到成功
            # FIXME: 需修复，添加最大请求次数解决陷入死循环的bug
            while True:

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
                    break
                else:
                    print("ERROR: Failed to get data from page_%d. Retry..." % i)
