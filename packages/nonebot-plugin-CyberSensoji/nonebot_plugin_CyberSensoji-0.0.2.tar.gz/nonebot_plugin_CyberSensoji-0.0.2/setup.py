#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="nonebot_plugin_CyberSensoji",
    version="0.0.2",
    keywords=["pip", "CyberSensoji"],			# 关键字
    description="A plugin for nonebot", 	# 描述
    long_description="A plugin for nonebot",
    license="MIT Licence",		# 许可证

    # 项目相关文件地址，一般是github项目地址即可
    url="https://github.com/Raidenneox/nonebot_plugin_CyberSensoji",
    author="Raidenneox",			# 作者
    author_email="longahead@outlook.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["nonebot2", "nonebot-adapter-onebot"]  # 这个项目依赖的第三方库
)
