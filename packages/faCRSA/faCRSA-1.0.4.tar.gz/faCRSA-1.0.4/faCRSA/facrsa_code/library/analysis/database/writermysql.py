#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Author: Ruinan Zhang
Version: v1.2
LastEditTime: 2022-07-01 09:37:30
E-mail: 2020801253@stu.njau.edu.cn
Copyright (c) 2022 by Ruinan Zhang, All Rights Reserved. Licensed under the GPL v3.0.
'''
import logging

import pandas as pd
import datetime
import time
from facrsa_code.library.util.sqliteUtil import sqliteUtil


def csv_to_mysql(file_name, tid, user):
    data = pd.read_csv(file_name)
    data = data.astype(object).where(pd.notnull(data), None)
    for image, re_img, trl, trpa, tsa, trv, mrl, mrpa, msa, mrv, cha, mrd, al, ac, ar in zip(
            data['Image_Name'],
            data['Image_Name'],
            data['Total_Root_Length(cm)'],
            data['Total_Root_Projected_Area(cm2)'],
            data['Total_Surface_Area(cm2)'],
            data['Total_Root_Volume(cm3)'],
            data['Primary_Root_Length(cm)'],
            data['Primary_Root_Projected_Area(cm2)'],
            data['Primary_Root_Surface_Area(cm2)'],
            data['Primary_Root_Volume(cm3)'],
            data['Convex_Hull_Area(cm2)'],
            data['Max_Root_Depth(cm)'],
            data['Angle_Left(°)'],
            data['Angle_Center(°)'],
            data['Angle_Right(°)']):
        try:
            insertsql = "insert into result(trl, trpa, tsa, trv, mrl, mrpa, msa, mrv, cha, mrd, al, ac, ar, tid, image, rid) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                trl, trpa, tsa, trv, mrl, mrpa, msa, mrv, cha, mrd, al, ac, ar, tid, image, 'b'+str(time.time()) +"*-" + str(image))
            sqliteUtil().insert(insertsql)
        except Exception as e:
            logging.error(e)


def insert_schedule(tid):
    schedule = 1
    sql = "insert into schedule(tid,schedule) values('%s','%s')" % (tid, schedule)
    res = sqliteUtil().update(sql)


def update_schedule(tid, schedule):
    sql = "update schedule set schedule = '%s' where tid='%s'" % (schedule, tid)
    res = sqliteUtil().update(sql)


def update_task(tid):
    sql = "update task set status = 1 , update_time='%s' where tid='%s'" % (
        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), tid)
    res = sqliteUtil().update(sql)


def update_task_error(tid):
    sql = "update task set status = 0 , update_time='%s' where tid='%s'" % (
        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), tid)
    res = sqliteUtil().update(sql)
