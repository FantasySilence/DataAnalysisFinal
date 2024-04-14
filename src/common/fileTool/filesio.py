# ========================================================= #
# @Author: Fantasy_Silence                                  #
# @Time: 2024-04-04                                         #
# @IDE: Visual Studio Code & PyCharm                        #
# @Python: 3.9.7                                            #
# ========================================================= #
# @Description:                                             #
# This module is used to automatically extract file paths   #                   
# for easy reading of file data                             # 
# ========================================================= #
import os


class FilesIO:

    """
    实现一个文件IO流类
    """

    @staticmethod
    def getDataset(filename: str=None) -> str:

        """
        获取数据集路径用于读取
        """

        # fileTool文件夹所在路径
        fileTool_path = os.path.dirname(__file__)
        # common文件夹所在路径
        common_path = os.path.dirname(fileTool_path)
        # src文件夹所在路径
        src_path = os.path.dirname(common_path)
        # 项目根路径
        root_path = os.path.dirname(src_path)
        # resources文件夹路径
        resources_path = os.path.join(root_path, "resources")
        # 目标文件路径
        if filename is None:
            dataset_path = os.path.join(resources_path, "datasets")
            # 如果是None, 必然是在找存放数据的文件夹，如果没有就建一个
            if not os.path.exists(dataset_path):
                os.mkdir(dataset_path)
        else:
            dataset_path = os.path.join(resources_path, "datasets", filename)
        return dataset_path


    @staticmethod
    def getHTMLtext(filename: str=None) -> str:

        """
        获取爬取的html文件路径用于解析
        """

        # fileTool文件夹所在路径
        fileTool_path = os.path.dirname(__file__)
        # common文件夹所在路径
        common_path = os.path.dirname(fileTool_path)
        # src文件夹所在路径
        src_path = os.path.dirname(common_path)
        # 项目根路径
        root_path = os.path.dirname(src_path)
        # resources文件夹路径
        resources_path = os.path.join(root_path, "resources")
        # 目标文件路径
        if filename is None:
            htmltext_path = os.path.join(resources_path, "webtexts")
            # 如果是None, 必然是在找存放数据的文件夹，如果没有就建一个
            if not os.path.exists(htmltext_path):
                os.mkdir(htmltext_path)
        else:
            htmltext_path = os.path.join(resources_path, "webtexts", filename)
        return htmltext_path


if __name__ == "__main__":
    
    print(FilesIO.getDataset())
    print(FilesIO.getHTMLtext())
    