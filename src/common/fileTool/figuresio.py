# ========================================================= #
# @Author: Fantasy_Silence                                  #
# @Time: 2024-04-04                                         #
# @IDE: Visual Studio Code & PyCharm                        #
# @Python: 3.9.7                                            #
# ========================================================= #
# @Description:                                             #
# This module is used to automatically extract              #  
# image file paths, making it asier to read image file data #
# ========================================================= #
import os


class FiguresIO:

    """
    实现一个图片文件IO流类
    """

    @staticmethod
    def getFigureSavePath(figname: str=None) -> str:

        """
        获取图片文件的保存路径用于图片的保存
        """

        # fileTool文件夹所在路径
        fileTool_path = os.path.dirname(__file__)
        # common文件夹所在路径
        common_path = os.path.dirname(fileTool_path)
        # src文件夹所在路径
        src_path = os.path.dirname(common_path)
        # 项目根路径
        root_path = os.path.dirname(src_path)
        # figures文件夹路径
        figures_path = os.path.join(root_path, "figures")
        # 确保figures文件夹路径存在
        if not os.path.exists(figures_path):
            os.makedirs(figures_path)
        # 目标文件路径
        if figname is None:
            figsave_path = os.path.join(figures_path)
        else:
            figsave_path = os.path.join(figures_path, figname)
        return figsave_path


if __name__ == "__main__":
    
    print(FiguresIO.getFigureSavePath())
    print(FiguresIO.getFigureSavePath("test.png"))
