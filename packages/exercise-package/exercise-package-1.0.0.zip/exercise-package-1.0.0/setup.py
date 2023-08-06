### 发布包和模块

## 环境准备：安装 setuptools, pip, wheel, twine 三方库

## 项目结构
'''
            项目名称
                    包名称
                            __init__.py
                            模块
                    模块
                    setup.py
                    [ README.rst ]
                    [ LICENSE.txt ]
                    [ MANIFEST.in ]
'''

## setup
#           作用：配置项目信息
#           模块：from distutils.core import setup     或       from setuptools import setup
#           命名：命名全部小写，多个单词以 "-" 分割，不要和已有包名称重复
#           参数：名称，版本，描述信息，需要的包文件列表参数必需传入
'''
                    名称：name = "xxx"
                    版本：version = "A.B.C"
                    描述信息：description = "xxxxxxxx"
                    需要的包文件列表：packages = ["p1", "p2", ...]
                    需要的单文件模块列表：py_modules = ["m1", "m2", ...]
                    作者：author = "xxx"
                    作者邮箱：author_email = "xxx@xxx"
                    长描述：long_description = "xxxxxxxxxxxxxxxxxxxxx"
                    依赖的其他包：install_requires = ["p1>A1.B1.C1", "p2>A2.B2.C2", ...]
                    Python版本限制：python_version = ">=A.B.C"
                    项目主页地址：url = "https://xxx"
                    协议：license = "XXX"
'''

## README.rst
#           作用：使用特定字符描述格式的文本，整个文本内容传给 long_description 参数，供用户参考
#           语法检测：python3 setup.py check -r -s   或者   Pycharm中创建“README.html”预览
#           安装库：python3 -m pip install readme_renderer


## LICENSE.txt
#           作用：声明库的一些使用责任和许可等
#           获取：https://choosealicense.com/


## MANIFEST.in
#           作用：向打包工具指明需要打包的文件
#           语法：include xxx


## 1. 创建一个项目
from  setuptools import setup

def readme_file():
      with open("README.rst", encoding="utf-8") as rm:
            return rm.read()

setup(name="exercise-package", version="1.0.0", description="This is package for exercise!", packages=["package1"],
      py_modules=["tool"], author="ysy", author_email="ysy@qq.com", long_description=readme_file())


## 2. 编译生成发布包：在 setup.py 同级目录中进行
#           python3 setup.py sdist [--formats=(zip/tar/gztar...)] ：生成源码压缩包，可以在任意平台重新编译所有内容
#           python3 setup.py bdist ：生成二进制发行包，是某个特定环境的存档
#           python3 setup.py bdist_egg ：生成 .egg 包
#           python3 setup.py bdist_wheel ：生成 .wheel 包
#   e        python3 setup.py bdist_wininst ：生成windows环境下的安装文件


## 3. 本地安装
#           源码压缩包：解压缩 python3 setup.py install
