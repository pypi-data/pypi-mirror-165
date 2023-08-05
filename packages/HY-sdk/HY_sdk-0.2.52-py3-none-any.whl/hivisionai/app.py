# -*- coding: utf-8 -*-

"""
@Time     : 2022/8/27 14:17
@Author   : cuny
@File     : app.py
@Software : PyCharm
@Introduce: 
查看包版本等一系列操作
"""
import sys
from argparse import ArgumentParser
from importlib.metadata import version


def entry_point():
    parser = ArgumentParser()
    parser.add_argument("-v", "--version", action="store_true")

    args = parser.parse_args()

    if args.version:
        print(version("hivisionai"))
        sys.exit()
