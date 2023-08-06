'''
Author: Ruinan Zhang
Version: v1.2
LastEditTime: 2022-07-01 09:33:29
E-mail: 2020801253@stu.njau.edu.cn
Copyright (c) 2022 by Ruinan Zhang, All Rights Reserved. Licensed under the GPL v3.0.
'''
from flask import Flask
import os
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

from facrsa_code.library.web import views,dataApi
