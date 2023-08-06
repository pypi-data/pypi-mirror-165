#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Author: Ruinan Zhang
Version: v1.2
LastEditTime: 2022-07-01 09:34:38
E-mail: 2020801253@stu.njau.edu.cn
Copyright (c) 2022 by Ruinan Zhang, All Rights Reserved. Licensed under the GPL v3.0.
'''
import os
from pathlib import Path


def return_config(factor, mail, private_plugin, uid, tid):
    base_path = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "static/upload",
                     str(uid), str(tid)).as_posix()
    initial_path = base_path + "/initial/"
    predict_out_path = base_path + "/predictout/"
    out_path = base_path + "/output/"
    length_ratio = factor
    area_ratio = factor * factor
    mail = mail
    if mail == "":
        mail = "2020801253@stu.njau.edu.cn"
    os.mkdir(predict_out_path)
    os.mkdir(out_path)
    data = {
        'base_path': base_path,
        'initial_path': initial_path,
        'predict_out_path': predict_out_path,
        'out_path': out_path,
        'length_ratio': length_ratio,
        'area_ratio': area_ratio,
        'mail': mail,
        'uid': str(uid),
        'tid': str(tid),
        'pid': str(private_plugin)
    }
    return data
