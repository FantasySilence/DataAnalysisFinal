# ================================================================= #
# @Author: Fantasy_Silence                                          #
# @Time: 2024-04-24                                                 #
# @IDE: Visual Studio Code & PyCharm                                #
# @Python: 3.9.7                                                    #
# ================================================================= #
# @Description: Used to draw learning curve for trained model.      #
# ================================================================= #
import matplotlib
import numpy as np
from typing import Any
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve

matplotlib.rcParams['font.sans-serif'] = ['STsong']
matplotlib.rcParams['axes.unicode_minus'] = False

from src.common.fileTool.figuresio import FiguresIO
from src.common.figTool.evaluateobjectbase import EvaluateObjectBase


class LearningCurve(EvaluateObjectBase):

    def __init__(
        self, model: Any, X_train: np.ndarray, y_train: np.ndarray, cv: Any = None,
        train_sizes: np.ndarray = np.linspace(0.1, 1.0, 10), scoring: str = None,
        is_show_alone: bool = True, is_show: bool = True, is_save: bool = False,
        ax: plt.Axes = None, fig_name: str = None,
    ) -> None:
        
        """
        model: 训练好的模型
        X_train, y_train: 训练集
        cv: 交叉验证方法
        train_sizes: 训练规模，与learning_curve相同
        scoring: 交叉验证分数
        is_show_alone: 是否显示于单独的画布上. 如果想单独显示，设置为True，
        如果想作为子图与其他图片一起显示，自行设置画布并将该参数设置为False
        is_show: 是否显示
        is_save: 是否以png格式保存图片，设置为True将保存于项目根路径下的figures文件夹中
        """

        super().__init__(
            ax=ax, fig_name=fig_name, is_show_alone=is_show_alone,
            is_show=is_show, is_save=is_save
        )
        self.X_train, self.y_train = X_train, y_train
        self.train_sizes = train_sizes
        self.scoring = scoring
        self.model = model
        self.cv = cv
        self.draw()
    

    def draw(self) -> None:

        if self.is_show_alone:
            _, self.ax = plt.subplots(figsize=(12, 8), dpi=100, facecolor="w")
        
        # ------ 生成学习曲线数据 ------ #
        train_sizes, train_scores, test_scores = learning_curve(
            self.model, self.X_train, self.y_train, cv=self.cv,
            train_sizes=self.train_sizes, scoring=self.scoring, n_jobs=-1
        )

        # ------ 计算训练和测试得分的平均值 ------ #
        train_scores_mean = np.mean(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)

        # ------ 绘制学习曲线 ------ #
        # 绘制训练得分
        self.ax.plot(
            train_sizes, train_scores_mean, '-', color="r", 
            label="Training score"
        )
        # 绘制测试得分
        self.ax.plot(
            train_sizes, test_scores_mean, '-', color="g", 
            label="Cross-validation score"
        )

        self.ax.set_xlabel("Training examples", fontsize=12)
        self.ax.set_ylabel("Score", fontsize=12)
        self.ax.legend(loc='best')
        self.ax.grid(ls=":")
        plt.tight_layout()

        # ------ 存储图片 ------ #
        if self.is_save:
            if self.fig_name is not None:
                path = FiguresIO.getFigureSavePath(
                    "%s/%s Learning Curve.png" % 
                    (self.folder_name, self.fig_name)
                )
            else:
                path = FiguresIO.getFigureSavePath(
                    "%s/Learning Curve.png" % self.folder_name
                )
            plt.savefig(path, dpi=300)
        
        if self.is_show and self.is_show_alone:
            self.ax.set_title("Learning Curve", fontsize=14)
            plt.show()
