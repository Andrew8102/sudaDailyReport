# -*- coding:utf-8 -*-
"""
@author: 古时月
@file: main.py
@time: 2021/1/21 11:17

"""
import os
from daka import Daka


if __name__ == "__main__":
    ls = os.listdir()
    jsonfiles = [i for i in ls if os.path.splitext(i)[1] == ".json"]
    for json in jsonfiles:
        student = Daka(json)
        student.run()
        print(json, "完成")
        