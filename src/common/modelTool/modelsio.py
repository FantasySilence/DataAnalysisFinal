# ========================================================================= #
# @Author: Fantasy_Silence                                                  #
# @Time: 2024-04-24                                                         #
# @IDE: Visual Studio Code & PyCharm                                        #
# @Python: 3.9.7                                                            #
# ========================================================================= #
# @Description: This module is used to save the trained model and load it   #
# ========================================================================= #
import os
import joblib
from typing import Any


class ModelsIO:

    """
    模型IO流类，用于model的保存和加载
    """

    @staticmethod
    def saveModel(model: Any, model_name: str=None) -> None:

        # modelTool文件夹所在路径
        modelTool_path = os.path.dirname(__file__)
        # common文件夹所在路径
        common_path = os.path.dirname(modelTool_path)
        # src文件夹所在路径
        src_path = os.path.dirname(common_path)
        # 项目根路径
        root_path = os.path.dirname(src_path)
        # resources文件夹路径
        resources_path = os.path.join(root_path, "resources")
        if model_name is None:
            raise ValueError("No model specified...")
        else:
            model_path = os.path.join(resources_path, "models", model_name)
        joblib.dump(model, model_path)


    @staticmethod
    def loadModel(model_name: str=None) -> Any:

        # modelTool文件夹所在路径
        modelTool_path = os.path.dirname(__file__)
        # common文件夹所在路径
        common_path = os.path.dirname(modelTool_path)
        # src文件夹所在路径
        src_path = os.path.dirname(common_path)
        # 项目根路径
        root_path = os.path.dirname(src_path)
        # resources文件夹路径
        resources_path = os.path.join(root_path, "resources")
        if model_name is None:
            raise ValueError("No model specified...")
        else:
            model_path = os.path.join(resources_path, "models", model_name)
            return joblib.load(model_path)
