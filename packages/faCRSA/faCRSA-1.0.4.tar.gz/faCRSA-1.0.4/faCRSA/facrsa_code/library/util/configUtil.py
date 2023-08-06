#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Author: Ruinan Zhang
Version: v1.2
LastEditTime: 2022-07-01 09:37:48
E-mail: 2020801253@stu.njau.edu.cn
Copyright (c) 2022 by Ruinan Zhang, All Rights Reserved. Licensed under the GPL v3.0.
'''
import os
from pathlib import Path


# load config file
def get_config(section):
    local_path = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))).as_posix()
    upload_path = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "static",'upload')).as_posix()
    plugin_path = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),"library","analysis","net")).as_posix()
    config = {'upload_path': upload_path + "/", 'local_path': local_path + "/",'plugin_path':plugin_path}
    return config

