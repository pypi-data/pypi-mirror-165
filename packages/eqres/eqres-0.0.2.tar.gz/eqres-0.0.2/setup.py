from setuptools import setup, find_packages
import eqres

setup(
    name=eqres.__name__,
    version="0.0.2",
    keywords=("eqres", "response"),
    description="接口统一返回工具",
    long_description="接口统一返回工具",
    license="MIT Licence",

    url="https://github.com/enqiangjing/eqres",
    author="enqiang",
    author_email="enqiangjing@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[]
)

"""
项目打包
python setup.py bdist_egg     # 生成类似 eqres-0.0.1-py2.7.egg，支持 easy_install 
# 使用此方式
python setup.py sdist         # 生成类似 eqres-0.0.1.tar.gz，支持 pip
# twine 需要安装
twine upload dist/eqres-0.0.2.tar.gz
"""
