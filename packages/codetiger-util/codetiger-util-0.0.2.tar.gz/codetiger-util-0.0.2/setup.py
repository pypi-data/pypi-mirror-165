# -*- coding: UTF-8 -*-
"""
    @program: utils
    @filename: setup
    @author: codetiger
    @create: 2022/8/26 21:58
"""
from setuptools import setup, find_packages

setup(
    name="codetiger-util",
    version="0.0.2",
    author="codetiger",
    author_email="admin@gybyt.cn",
    description="一些python工具类",
    # install_requires=[''],
    # 项目主页
    url="https://gybyt.cn",

    # 安装过程中，需要安装的静态文件，如配置文件、service文件、图片等
    # data_files=[
    #    ('', ['conf/*.conf']),
    #    ('/usr/lib/systemd/system/', ['bin/*.service']),
    #           ],

    # 希望被打包的文件
    # package_data={
    #    '':['*.txt'],
    #    'bandwidth_reporter':['*.txt']
    #           },
    # 不打包某些文件
    # exclude_package_data={
    #    'bandwidth_reporter':['*.txt']
    #           }
    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    packages=['codetiger', 'codetiger.util'],
    # py_modules=['需要安装的模块'],
    # 将 bin/foo.sh 和 bar.py 脚本，生成到系统 PATH中
    # 执行 python setup.py install 后
    # 会生成 如 /usr/bin/foo.sh 和 如 /usr/bin/bar.py
    # scripts=['bin/foo.sh', 'bar.py']
)
