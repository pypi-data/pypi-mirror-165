#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Author: Ruinan Zhang
Version: v1.2
LastEditTime: 2022-07-01 12:20:29
E-mail: 2020801253@stu.njau.edu.cn
Copyright (c) 2022 by Ruinan Zhang, All Rights Reserved. Licensed under the GPL v3.0.
'''
import configparser
import zipfile

from flask import redirect, session, request, jsonify, url_for, render_template, send_from_directory
from facrsa_code.library.util.sqliteUtil import sqliteUtil
from facrsa_code.library.util.configUtil import get_config
from facrsa_code import app
import hashlib
import datetime
import json
import os

os.environ['NO_PROXY'] = 'facrsa.aiphenomics.com'
import uuid
import sys
import requests

os.path.join(os.path.dirname(__file__), '../../../')
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from tasks import submit_task


@app.route('/api/getMyTask', methods=['GET'])
def get_my_task():
    limit = request.args.get('limit')
    page = request.args.get('page')
    tol = (int(page) - 1) * int(limit)
    sql = 'SELECT * FROM task where del = 0 and uid = ' + "'%s'" % (str(session.get('uid'))) + ' limit ' + "%s" % (
        str(tol)) + ',' + "%s" % (str(limit))
    count = 'SELECT * FROM task where del = 0 and uid = ' + "'%s'" % (str(session.get('uid')))
    data = sqliteUtil().fetch_all(sql)
    data_count = sqliteUtil().fetch_all(count)
    try:
        num = len(data_count)
    except TypeError:
        num = 0
    result = {
        "code": 0,
        'msg': "",
        'count': num,
        "data": data
    }
    return jsonify(result)


@app.route('/api/getMyPlugin', methods=['GET'])
def get_my_plugin():
    limit = request.args.get('limit')
    page = request.args.get('page')
    tol = (int(page) - 1) * int(limit)
    sql = 'SELECT * FROM plugin where del = 0 and uid = ' + "'%s'" % (str(session.get('uid'))) + ' limit ' + "%s" % (
        str(tol)) + ',' + "%s" % (str(limit))
    count = 'SELECT * FROM plugin where del = 0 and uid = ' + "'%s'" % (str(session.get('uid')))
    data = sqliteUtil().fetch_all(sql)
    data_count = sqliteUtil().fetch_all(count)
    try:
        num = len(data_count)
    except TypeError:
        num = 0
    result = {
        "code": 0,
        'msg': "",
        'count': num,
        "data": data
    }
    return jsonify(result)


def get_plugin_count():
    count = 'SELECT * FROM plugin where del = 0 and uid = ' + "'%s'" % (str(session.get('uid')))
    data_count = sqliteUtil().fetch_all(count)
    return data_count


@app.route('/api/checkUserName', methods=['POST'])
def check_username():
    username = str(request.form['username'])
    sql = "SELECT * FROM user  WHERE username = '%s'" % (username)
    result = sqliteUtil().fetch_one(sql)
    if result:
        return str(200)
    else:
        return str(404)


@app.route('/api/login', methods=['POST'])
def user_login():
    if "logged_in" in session:
        return redirect("/")
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        sql = "SELECT * FROM user  WHERE username = '%s'" % (username)
        result = sqliteUtil().fetch_one(sql)
        if result:
            salt = "facrsa2022"
            password = result['password']
            if password == hashlib.md5(
                    bytes(password_candidate + salt, encoding="utf8")).hexdigest():  # 调用verify方法验证，如果为真，验证通过
                session['logged_in'] = True
                session['username'] = username
                session['uid'] = result['uid']
                data = {
                    "code": 200,
                    'msg': "success",
                }

                response = jsonify(data)
                return response
            else:
                data = {
                    "code": 400,
                    'msg': "error (username / pwd)",
                }

                response = jsonify(data)
                return response
        else:
            data = {
                "code": 400,
                'msg': "user not found",
            }

            response = jsonify(data)
            return response


@app.route('/api/register', methods=['POST'])
def user_reg():
    if "logged_in" in session:
        return redirect("/")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        uid = str(uuid.uuid4())
        create_time = datetime.datetime.now()
        salt = "facrsa2022"
        pwd_new = hashlib.md5(bytes(password + salt, encoding="utf8")).hexdigest()
        sql = "INSERT INTO user(uid,username,password,email,create_time) VALUES ('%s','%s', '%s', '%s', '%s')" % (uid,
                                                                                                                  username,
                                                                                                                  pwd_new,
                                                                                                                  "none",
                                                                                                                  create_time)
        result = sqliteUtil().insert(sql)
        if result == "400":
            return str(400)
        else:
            return str(200)


@app.route('/api/changeUserName', methods=['POST'])
def change_user_name():
    if request.method == 'POST':  # 如果提交表单
        username = request.form['username']
        uid = session.get('uid')
        sql = "UPDATE user SET username =" + "'%s'" % (str(username)) + "WHERE uid = " + "'%s'" % (str(uid))
        result = sqliteUtil().update(sql)
        if result == "400":
            return str(400)
        else:
            del session['logged_in']
            del session['username']
            del session['uid']
            return str(200)


@app.route('/api/changePWD', methods=['POST'])
def change_PWD():
    if request.method == 'POST':
        password = request.form['password']
        uid = session.get('uid')
        salt = "facrsa2022"
        pwd_new = hashlib.md5(bytes(password + salt, encoding="utf8")).hexdigest()
        sql = "UPDATE user SET password =" + "'%s'" % (str(pwd_new)) + "WHERE uid = " + "'%s'" % (str(uid))
        result = sqliteUtil().update(sql)
        if result == "400":
            return str(400)
        else:
            del session['logged_in']
            del session['username']
            del session['uid']
            return str(200)


@app.route('/api/addTask/<string:tid>', methods=['POST'])
def add_task(tid):
    if request.method == 'POST':
        name = request.form['name']
        des = request.form['des']
        cf = request.form['cf']
        mail = request.form['mail']
        plugin = request.form['plugin']
        try:
            uid = session.get('uid')
            if uid == None:
                uid = "public"
            create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = "INSERT INTO task(tid,task_name,private_plugin,description,factor,email,create_time,uid) VALUES ('%s','%s', '%s', '%s', '%s','%s', '%s', '%s')" % (
                tid, name, plugin, des, cf, mail, create_time, uid)
            result = sqliteUtil().insert(sql)
            if result == "400":
                data = {
                    "code": 400,
                    'msg': sql,
                }
                return jsonify(data)
            else:
                data = {
                    "code": 200,
                    'tid': tid,
                }
                submit_task(uid, tid)
                return jsonify(data)
        except KeyError:
            data = {
                "code": 400
            }
            return jsonify(data)


@app.route('/api/delTask', methods=['POST'])
def del_task():
    if request.method == 'POST':
        sql = "UPDATE task SET del= 1 WHERE tid='%s' and uid = '%s'" % (request.form['tid'], session.get('uid'))
        result = sqliteUtil().update(sql)
        if result == "400":
            return str(400)
        else:
            return str(200)


@app.route('/test')
def test():
    filename = "1..zip"
    ALLOWED_EXTENSIONS = ['jpg', 'png', 'zip']
    return jsonify('.' in filename and \
                   filename.rsplit('.', 1)[1])


@app.route('/uploadImg/<string:tid>', methods=['POST'])
def upload_img_file(tid):
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'code': -1, 'filename': '', 'msg': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'code': -1, 'filename': '', 'msg': 'No selected file'})
        else:
            try:
                user = session.get('uid')
                if user is None:
                    user = "public"
                user_path = get_config('storage')["upload_path"] + "/" + str(user)
                task_path = user_path + "/" + tid + "/initial"
                if file and allowed_file(file.filename):
                    origin_file_name = file.filename
                    filename = origin_file_name
                    if os.path.exists(user_path):
                        pass
                    else:
                        os.makedirs(user_path)
                    if os.path.exists(task_path):
                        pass
                    else:
                        os.makedirs(task_path)
                    file.save(os.path.join(task_path, filename))
                    return jsonify(
                        {'code': 0, 'filename': origin_file_name, 'msg': os.path.join(task_path, filename)})
                else:
                    return jsonify({'code': -1, 'filename': '', 'msg': 'File not allowed'})
            except Exception as e:
                return jsonify({'code': -1, 'filename': '', 'msg': 'Error occurred'})
    else:
        return jsonify({'code': -1, 'filename': '', 'msg': 'Method not allowed'})


@app.route('/api/delImg/<string:tid>', methods=['POST'])
def del_img_file(tid):
    if request.method == 'POST':
        if "logged_in" in session:
            uid = session.get('uid')
        else:
            uid = "public"
        img_path = get_config('storage')["upload_path"] + "/" + str(uid) + "/" + tid + "/initial/" + request.form['img']
        try:
            os.remove(img_path)
            return jsonify({'code': 200, 'msg': ''})
        except Exception as e:
            print(e)
            return jsonify({'code': 500, 'msg': 'File deleted error'})
    else:
        return ({'code': 500, 'msg': 'Method not allowed'})


@app.route('/uploadPlugin/<string:pid>', methods=['POST'])
def upload_plugin_file(pid):
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'code': -1, 'filename': '', 'msg': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'code': -1, 'filename': '', 'msg': 'No selected file'})
        else:
            try:
                user = session.get('uid')
                plugin_path = get_config('storage')["plugin_path"] + "/" + str(user) + "/" + pid
                if file and allowed_file(file.filename):
                    origin_file_name = file.filename
                    filename = origin_file_name
                    if os.path.exists(plugin_path):
                        pass
                    else:
                        os.makedirs(plugin_path)
                    if os.path.exists(plugin_path):
                        pass
                    else:
                        os.makedirs(plugin_path)
                    file.save(os.path.join(plugin_path, filename))
                    return jsonify(
                        {'code': 0, 'filename': origin_file_name, 'msg': pid})
                else:
                    return jsonify({'code': -1, 'filename': '', 'msg': 'File not allowed'})
            except Exception as e:
                print(e)
                return jsonify({'code': -1, 'filename': '', 'msg': 'Error occurred'})
    else:
        return jsonify({'code': -1, 'filename': '', 'msg': 'Method not allowed'})


@app.route('/api/delPluginFile/<string:pid>', methods=['POST'])
def del_plugin_file(pid):
    if request.method == 'POST':
        plugin_path = get_config('storage')["plugin_path"] + "/" + str(session.get('uid')) + "/" + str(pid) + "/" + \
                      request.form['plugin']
        try:
            os.remove(plugin_path)
            return jsonify({'code': 200, 'msg': ''})
        except Exception as e:
            print(e)
            return jsonify({'code': 500, 'msg': 'File deleted error'})
    else:
        return ({'code': 500, 'msg': 'Method not allowed'})


@app.route('/api/addPlugin/<string:pid>', methods=['POST'])
def add_plugin(pid):
    if request.method == 'POST':
        name = request.form['name']
        des = request.form['des']
        uid = session.get('uid')
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO plugin(pid,plugin_name,description,create_time,uid) VALUES ('%s', '%s', '%s', '%s','%s')" % (
            pid, name, des, create_time, uid)
        result = sqliteUtil().insert(sql)
        if result == "400":
            data = {
                "code": 400,
                'msg': sql,
            }
            return jsonify(data)
        else:
            data = {
                "code": 200,
                'pid': pid,
            }

            plugin_path = get_config('storage')["plugin_path"] + "/" + str(uid) + "/" + str(pid)
            zip_list = os.listdir(plugin_path)
            fz = zipfile.ZipFile(os.path.join(plugin_path, zip_list[0]), 'r')
            for file in fz.namelist():
                fz.extract(file, plugin_path)
            fz.close()
            os.remove(os.path.join(plugin_path, zip_list[0]))
            return jsonify(data)


@app.route('/api/delPlugin', methods=['POST'])
def del_plugin():
    if request.method == 'POST':
        sql = "UPDATE plugin SET del= 1 WHERE pid='%s' and uid = '%s'" % (request.form['pid'], session.get('uid'))
        result = sqliteUtil().update(sql)
        if result == "400":
            return str(400)
        else:
            return str(200)


@app.route('/api/getSchedule/<tid>', methods=['GET'])
def get_task_schedule(tid):
    sql = "select status from task where tid = '%s'" % (tid)
    result = sqliteUtil().fetch_one(sql)
    return jsonify(result)


@app.route('/api/getResult/<tid>', methods=['GET'])
def get_result(tid):
    sql = "select * from result where tid = '%s'" % (tid)
    data = sqliteUtil().fetch_all(sql)
    try:
        num = len(data)
    except TypeError:
        num = 0
    result = {
        "code": 0,
        'msg': "",
        'count': num,
        "data": data
    }
    response = json.dumps(result, default=str)
    return response


@app.route('/api/createDownload/<uid>/<tid>', methods=['GET'])
def create_download(uid, tid):
    try:
        return send_from_directory(get_config('storage')["upload_path"] + uid + "/" + tid + "/output/",
                                   uid + "_" + tid + ".zip", as_attachment=True)
    except Exception as e:
        return jsonify(e)


@app.route('/api/initial', methods=['POST'])
def initial_mail():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        host = request.form['host']
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(os.path.dirname(__file__)), "analysis", "config.ini"))
        config.set('mail', 'user', user)
        config.set('mail', 'password', password)
        config.set('mail', 'host', host)
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "analysis", "config.ini"), "w+") as f:
                config.write(f)
            f.close()
        except BaseException:
            return jsonify({
                "code": 400
            })
        else:
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "install.lock"), "w") as f:
                f.write("installed")
            f.close()
            return jsonify({
                "code": 200
            })


@app.route('/api/skipInitial')
def skip_initial():
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "install.lock"), "w") as f:
        f.write("installed")
    f.close()
    return redirect("/")


def get_task_info(tid):
    sql = "select * from task where tid = '%s'" % (tid)
    result = sqliteUtil().fetch_one(sql)
    return result


def allowed_file(filename):
    ALLOWED_EXTENSIONS = ['jpg', 'png', 'zip']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def check_update():
    check_res = requests.get(url="https://facrsa.aiphenomics.com/update.json")
    return check_res.json()['update']
