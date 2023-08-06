#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Author: Ruinan Zhang
Version: v1.2
LastEditTime: 2022-07-01 09:38:32
E-mail: 2020801253@stu.njau.edu.cn
Copyright (c) 2022 by Ruinan Zhang, All Rights Reserved. Licensed under the GPL v3.0.
"""
import uuid

from flask import render_template, session, redirect
from facrsa_code.library.web.dataApi import get_task_info, get_plugin_count, check_update
from facrsa_code.library.util.sqliteUtil import sqliteUtil
from facrsa_code import app
import traceback
import os


@app.route('/')
def index_page():
    if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "install.lock")):
        uid, user = get_info()
        if check_update() == 1:
            return render_template("index.html", uid=uid, user=user, update=1)
        else:
            return render_template("index.html", uid=uid, user=user)
    return redirect('/initial')


@app.route('/initial')
def initial_page():
    if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "install.lock")):
        return str('Initialize finished! If you want to initialize again, please reinstall faCRSA.')
    try:
        initial_sql = sqliteUtil()
    except Exception as e:
        return render_template('initial.html', error_msg="", success_msg="none")
    else:
        return render_template('initial.html', error_msg="none", success_msg="")


@app.route('/examples')
def examples_page():
    uid, user = get_info()
    return render_template('examples.html', uid=uid, user=user, title="Examples")


@app.route('/faq')
def faq_page():
    uid, user = get_info()
    return render_template('faq.html', uid=uid, user=user, title="FAQ")

@app.route('/install')
def install_page():
    uid, user = get_info()
    return render_template('install.html', uid=uid, user=user, title="Install")

@app.route('/addtask')
def add_task_page():
    tid = str(uuid.uuid4())
    uid, user = get_info()
    plugin_count = get_plugin_count()
    return render_template('addtask.html', uid=uid, user=user, tid=tid, title="Add a task",
                           plugin_list=plugin_count)


@app.route('/addplugin')
def add_plugin_page():
    pid = str(uuid.uuid4())
    uid, user = get_info()
    return render_template('addplugin.html', uid=uid, user=user, pid=pid, title="Add a plugin")


@app.route('/mytask')
def my_task_page():
    if "logged_in" not in session:
        return redirect("/login")
    uid, user = get_info()
    return render_template('mytask.html', uid=uid, user=user, title="My Task")


@app.route('/myplugin')
def my_plugin_page():
    if "logged_in" not in session:
        return redirect("/login")
    uid, user = get_info()
    return render_template('myplugin.html', uid=uid, user=user, title="My Plugin")


@app.route('/setting')
def setting_page():
    if "logged_in" not in session:
        return redirect("/login")
    uid, user = get_info()
    return render_template('setting.html', uid=uid, user=user, title="Account Setting")


@app.route('/login')
def login_page():
    if "logged_in" in session:  # 如果已经登录，则直接跳转到控制台
        return redirect("/")
    uid, user = get_info()
    return render_template('login.html', uid=uid, user=user, title="Login")


@app.route('/register')
def register_page():
    uid, user = get_info()
    return render_template('register.html', uid=uid, user=user, title="Register")


@app.route('/result/<string:tid>', methods=['GET'])
def result_page(tid):
    try:
        task_info = get_task_info(tid)
        if session.get('uid') is None and task_info['uid'] != 'public':
            return render_template('404.html')
        else:
            uid, user = get_info()
        if task_info['status'] == '2':
            return redirect("http://127.0.0.1:5000/status/" + str(tid))
        elif task_info['status'] == '0':
            return redirect("http://127.0.0.1:5000/error/" + str(tid))
        return render_template('result.html', tid=tid, name=task_info['task_name'],
                               des=task_info['description'], title="Result",
                               download='/api/createDownload/' + task_info['uid'] + "/" + task_info['tid'], uid=uid)
    except TypeError:
        return redirect('404.html', title="404")


@app.route('/schedule/<string:tid>', methods=['GET'])
def schedule_page(tid):
    uid, user = get_info()
    url = "http://127.0.0.1:5000/task/" + str(tid)
    try:
        task_info = get_task_info(tid)
        if task_info['status'] == '1':
            return redirect("http://127.0.0.1:5000/result/" + str(tid))
        elif task_info['status'] == '0':
            return redirect("http://127.0.0.1:5000/error/" + str(tid))
        return render_template('schedule.html', tid=tid, uid=uid, user=user, name=task_info['task_name'],
                               mail=task_info['email'], url=url, title="Schedule")
    except TypeError:
        traceback.print_exc()
        return render_template('404.html', title="404")


@app.route('/task/<string:tid>', methods=['GET'])
def task_page(tid):
    try:
        task_info = get_task_info(tid)
        if task_info['status'] == '2':
            url = "http://127.0.0.1:5000/schedule/" + str(tid)
        elif task_info['status'] == '0':
            return redirect("http://127.0.0.1:5000/error/" + str(tid))
        else:
            url = "http://127.0.0.1:5000/result/" + str(tid)
        return redirect(url)
    except TypeError:
        return render_template('404.html', title="404")


@app.route('/error/<string:tid>', methods=['GET'])
def error_page(tid):
    uid, user = get_info()
    try:
        task_info = get_task_info(tid)
        if task_info['status'] == '2':
            return redirect("http://127.0.0.1:5000/status/" + str(tid))
        elif task_info['status'] == '1':
            return redirect("http://127.0.0.1:5000/result/" + str(tid))
        return render_template('error.html', uid=uid, user=user, name=task_info['task_name'],
                               des=task_info['description'], title="Error")
    except TypeError:
        return render_template('404.html', title="404")


@app.route('/showimg/<rid>/<tid>', methods=['GET'])
def show_img_page(rid, tid):
    if "logged_in" in session:
        uid = session.get('uid')
    else:
        uid = "public"
    image = rid.split("*-")[1]
    initial_img = uid + "/" + tid + "/output/" + uid + "_" + tid + "/images/" + image + ".jpg"
    masked_img_BM = uid + "/" + tid + "/output/" + uid + "_" + tid + "/images/" + image + "_out_B_M_C.jpg"
    seg_img_BM = uid + "/" + tid + "/output/" + uid + "_" + tid + "/images/" + image + "_out_B_M_W.jpg"
    return render_template('showimg.html', initial_img=initial_img, masked_img_BM=masked_img_BM, seg_img_BM=seg_img_BM)


@app.route('/logout')
def user_logout():
    try:
        del session['logged_in']
        del session['uid']
        del session['username']
    except KeyError:
        pass
    finally:
        return redirect("/login")


@app.errorhandler(404)
def error_date(error):
    return render_template("404.html", title="404")


def get_info():
    try:
        uid = session.get('uid')
        user = session.get('username')
        return uid, user
    except BaseException as e:
        print(e)
