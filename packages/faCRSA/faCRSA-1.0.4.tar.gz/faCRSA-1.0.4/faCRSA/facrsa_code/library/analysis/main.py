#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Author: Ruinan Zhang
Version: v1.2
LastEditTime: 2022-07-01 09:35:39
E-mail: 2020801253@stu.njau.edu.cn
Copyright (c) 2022 by Ruinan Zhang, All Rights Reserved. Licensed under the GPL v3.0.
"""
from facrsa_code.library.analysis import start
from facrsa_code.library.analysis import config
from facrsa_code.library.analysis import interact


def web_action(uid, tid):
    data_interact = interact.interact(uid, tid, 0)
    factor, mail, private_plugin = data_interact.initial_analysis()
    conf = config.return_config(factor, mail, private_plugin, uid, tid)
    start.start(conf, uid, tid)


