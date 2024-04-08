# ===================================================== #
# @Author: Fantasy_Silence                              #
# @Time: 2024-04-04                                     #                  
# @IDE: Visual Studio Code & PyCharm                    #
# @Python: 3.9.7                                        #
# ===================================================== #
# @Description:                                         #
# This module is used to randomly generate request      #
# information from the IP list and Headers list         #
# ===================================================== #
import random


class RandomRequestInfoGenerator:
    
    """
    TODO: 修改：这个模块需要修改，或将修改为反爬工具类
    实现一个随机生成请求信息的类
    """

    @staticmethod
    def get():

        """
        随机获取ip和headers
        """

        # IP列表，10个IP
        ip_list = [
            "36.6.144.153:8089",
            "117.69.237.24:8089",
            "183.164.242.5:8089",
            "114.106.146.5:8089",
            "117.71.149.130:8089",
            "36.6.145.85:8089",
            "114.104.135.72:41122",
            "117.69.233.126:8089",
            "36.6.145.177:8089",
            "117.69.236.60:8089"
        ]

        # headers列表，10个headers
        headers_list = [
            "Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
            "Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        ]

        # ip_list和head_list，两两组合
        ip_and_headers_list = []
        for ip in ip_list:
            for header in headers_list:
                ip_and_headers_list.append((ip, header))

        # 随机选取一个ip和headers
        myChoice = random.choice(ip_and_headers_list)
        proxies = {"https://": myChoice[0]}
        headers = {"User-Agent": myChoice[1]}
        return proxies, headers
