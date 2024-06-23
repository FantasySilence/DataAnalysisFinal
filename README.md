# DataAnalysisFinal
2023-2024-2学期学习数据分析的期末项目

### 一、Setup

> 非常建议使用vscode打开本项目，不过得确定你已经在vscode中配置好Python以及Jupyter notebook的环境
>
> Python版本为3.9.7

1.(如果有git的话)打开Git Bash，输入`git clone git@github.com:FantasySilence/DataAnalysisFinal.git`，获取项目源代码。

2.在vscode中打开对应文件夹，然后右键点击文件夹，选择"在集成终端中打开"。

![setup_1.png](README_img/setup_1.png)

3.在终端中输入 `python -m venv venv`创建虚拟环境。

![setup_2.png](README_img/setup_2.png)

4.创建完成后继续在终端中输入`.\venv\Scripts\Activate.ps1`激活虚拟环境，当发现终端显示的文字信息中出现"(venv)"时，激活成功。

![setup_3.png](README_img/setup_3.png)

5.激活成功后继续在终端输入` pip install -r .\requirements.txt`安装环境依赖。

![setup_4.png](README_img/setup_4.png)

6.等观察到Successfully...字样时，就可以愉快的运行啦\o/。

![setup_5.png](README_img/setup_5.png)

>在配置环境时可能会出现以下问题：
>
>1.配置环境时，可能会遇到pandas等Python库安装失败，这主要是因为我使用的Python版本是3.9.7，这些包的版本也相对较低。只需要重新下载这些包就可以了。
>
>2.创建虚拟环境时，输入`python -m venv venv`命令时可能会没有反应，这主要是因为Windows Powershell没有权限。请以管理员身份运行Windows Powershell，并输入`Set-ExecutionPolicy RemoteSigned`，一路点击确定并重启IDE即可。具体可以参考这篇[博客](https://blog.csdn.net/lsdaini/article/details/132778970)

### 二、注意事项

#### 1. 数据的获取

数据的获取使用到了爬虫，请确保网络连接正确以及及时输入验证码避免反爬虫。

#### 2. 数据解析部分

数据解析部分使用了百度地图开发者API用于将门牌地址转换为经纬度坐标以及地点检索，请自行按照百度地图开发者API中的[地理编码](https://lbsyun.baidu.com/faq/api?title=webapi/guide/webservice-geocoding)和[地点检索](https://lbsyun.baidu.com/faq/api?title=webapi/guide/webservice-placeapi)，生成应用，并修改[这里](src/common/infoTool/const.py)的ak密钥，程序中给出的密钥只是一个示例无法运行。

#### 3. 结果复现

只需要运行`main_paper.py`就可以获得全部复现的结果，运行`main_mymodule.py`即可获取我所做工作的全部结果。

> 注意：包含网格搜索的内容运行时间极长，请注意运行时间！！！

#### 4. 项目结构

本项目的项目结构如下，可以根据所需对源代码进行查阅，相关注释都十分详尽：
![structure.png](README_img/structure.png)

### 技术栈

Python | Jupyter notebook

### LICENSE

GPL-3.0 license
