from setuptools import setup, find_packages

setup(
    name="eqsmart",
    version="0.0.20",
    keywords=("eqsmart", "微服务", "eqlink"),
    description="微服务框架",
    long_description="http server, 支持解析文件上传的post请求",
    license="GPL-2.0",

    url="https://github.com/enqiangjing/eqsmart",
    author="enqiang",
    author_email="enqiangjing@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['eqlink', 'PyYAML==6.0']
)

"""
项目打包
python setup.py bdist_egg     # 生成类似 eqsmart-0.0.1-py2.7.egg，支持 easy_install 
# 使用此方式
python setup.py sdist         # 生成类似 eqsmart-0.0.1.tar.gz，支持 pip
# twine 需要安装
twine upload dist/eqsmart-0.0.20.tar.gz
"""
