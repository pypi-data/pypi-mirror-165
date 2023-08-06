#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Author: Ruinan Zhang
Version: v1.2
LastEditTime: 2022-07-01 09:35:49
E-mail: 2020801253@stu.njau.edu.cn
Copyright (c) 2022 by Ruinan Zhang, All Rights Reserved. Licensed under the GPL v3.0.
"""
import logging
import os
import shutil
import yagmail
import datetime
from facrsa_code.library.util.sqliteUtil import sqliteUtil
import re
import configparser


class postAction():
    def __init__(self, conf, user, tid, status):
        self.conf = conf
        self.user = user
        self.tid = tid
        self.status = status

    def move_file(self):
        initial_imglist = os.listdir(self.conf["predict_out_path"])
        predict_imglist = os.listdir(self.conf["initial_path"])
        os.mkdir(self.conf["out_path"] + "/images")
        for img in initial_imglist:
            shutil.move(self.conf["predict_out_path"] + img, self.conf["out_path"] + "images/" + img)
        for img in predict_imglist:
            shutil.move(self.conf["initial_path"] + img, self.conf["out_path"] + "images/" + img)
        filelist = os.listdir(self.conf["out_path"])
        os.mkdir(self.conf["out_path"] + "/" + self.conf["uid"] + "_" + self.conf["tid"])
        for file in filelist:
            shutil.move(self.conf["out_path"] + file,
                        self.conf["out_path"] + self.conf["uid"] + "_" + self.conf["tid"] + "/" + file)

    def zipfile(self):
        shutil.make_archive(base_name=self.conf["out_path"] + self.conf["uid"] + "_" + self.conf["tid"], format='zip',
                            root_dir=self.conf["out_path"] + self.conf["uid"] + "_" + self.conf["tid"])

    def moveFileSingle(self, file_array):
        self.restore_image_name(file_array)
        self.remove_folder()

    def remove_folder(self):
        shutil.rmtree(self.conf["initial_path"], True)
        shutil.rmtree(self.conf["predict_out_path"], True)
        shutil.rmtree(os.path.dirname(os.path.abspath(self.conf["initial_path"])) + "/original", True)
        shutil.rmtree(os.path.dirname(os.path.abspath(self.conf["initial_path"])) + "/convert", True)

    def restore_image_name(self, file_array, tid, uid):
        file_list = os.listdir(self.conf["out_path"] + str(uid) + "_" + str(tid) + "/" + "images/")
        new_list = file_list.copy()
        for key in list(file_array.keys()):
            for i in range(0, len(new_list)):
                original_name = re.sub(key, file_array[key], new_list[i])
                try:
                    os.rename(self.conf["out_path"] + str(uid) + "_" + str(tid) + "/" + "images/" + file_list[i],
                              self.conf["out_path"] + str(uid) + "_" + str(tid) + "/" + "images/" + original_name)
                except BaseException:
                    continue

    def change_mail(self, user, password, host):
        config = configparser.ConfigParser()
        config.read("config.ini")
        config.set('mail', 'user', user)
        config.set('mail', 'password', password)
        config.set('mail', 'host', host)
        print(config.sections())
        with open("config.ini", "w+") as f:
            config.write(f)
        f.close()

    def send_mail(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini"))
        try:
            user = config['mail']['user']
            password = config['mail']['password']
            host = config['mail']['host']
            yagmail_server = yagmail.SMTP(user=user, password=password, host=host)
            email_name = self.conf["mail"]
            email_title = ["faCRSA: Your analysis task has been completed."]
            email_content = [
                '<!doctype html><html>	<head>		<meta name="viewport" content="width=device-width">		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">		<title></title>		<style>			@media only screen and (max-width: 620px) { table[class=body] h1 { font-size:			28px !important; margin-bottom: 10px !important; } table[class=body] p,			table[class=body] ul, table[class=body] ol, table[class=body] td, table[class=body]			span, table[class=body] a { font-size: 16px !important; } table[class=body]			.wrapper, table[class=body] .article { padding: 10px !important; } table[class=body]			.content { padding: 0 !important; } table[class=body] .container { padding:			0 !important; width: 100% !important; } table[class=body] .main { border-left-width:			0 !important; border-radius: 0 !important; border-right-width: 0 !important;			} table[class=body] .btn table { width: 100% !important; } table[class=body]			.btn a { width: 100% !important; } table[class=body] .img-responsive {			height: auto !important; max-width: 100% !important; width: auto !important;			} } @media all { .ExternalClass { width: 100%; } .ExternalClass, .ExternalClass			p, .ExternalClass span, .ExternalClass font, .ExternalClass td, .ExternalClass			div { line-height: 100%; } .apple-link a { color: inherit !important; font-family:			inherit !important; font-size: inherit !important; font-weight: inherit			!important; line-height: inherit !important; text-decoration: none !important;			} #MessageViewBody a { color: inherit; text-decoration: none; font-size:			inherit; font-family: inherit; font-weight: inherit; line-height: inherit;			} .btn-primary table td:hover { background-color: #34495e !important; }			.btn-primary a:hover { background-color: #34495e !important; border-color:			#34495e !important; } }		</style>	</head>	<body class="" style="background-color: #f6f6f6; font-family: sans-serif; -webkit-font-smoothing: antialiased; font-size: 14px; line-height: 1.4; margin: 0; padding: 0; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;">		<table border="0" cellpadding="0" cellspacing="0" class="body" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; background-color: #f6f6f6;">			<tr>				<td style="font-family: sans-serif; font-size: 14px; vertical-align: top;">					&nbsp;				</td>				<td class="container" style="font-family: sans-serif; font-size: 14px; vertical-align: top; display: block; Margin: 0 auto; max-width: 580px; padding: 10px; width: 580px;">					<div class="content" style="box-sizing: border-box; display: block; Margin: 0 auto; max-width: 580px; padding: 10px;">						<table class="main" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; background: #ffffff; border-radius: 3px;">							<tr>								<td class="wrapper" style="font-family: sans-serif; font-size: 14px; vertical-align: top; box-sizing: border-box; padding: 20px;">									<table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;">										<tr>											<td style="font-family: sans-serif; font-size: 14px; vertical-align: top;">												<p style="font-family: sans-serif; font-size: 16px; font-weight: normal; margin: 0; Margin-bottom: 15px;">													<b>														Congratulations! 🎉 													</b>												</p>												<p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;">													Your task has been completed. 												</p>												<table border="0" cellpadding="0" cellspacing="0" class="btn btn-primary"												style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; box-sizing: border-box;">													<tbody>														<tr>															<td align="left" style="font-family: sans-serif; font-size: 14px; vertical-align: top; padding-bottom: 15px;">																<table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: auto;">																	<tbody>																		<tr>																									</tr>																	</tbody>																</table>															</td>														</tr>													</tbody>												</table>												<hr />												<p style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;">													If you did not sign up to faCRSA, please ignore this email or contact us													at 2020801253@stu.njau.edu.cn												</p>											</td>										</tr>									</table>								</td>							</tr>						</table>						<div class="footer" style="clear: both; Margin-top: 10px; text-align: center; width: 100%;">							<table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;">								<tr>									<td class="content-block" style="font-family: sans-serif; vertical-align: top; padding-bottom: 10px; padding-top: 10px; font-size: 12px; color: #999999; text-align: center;">										<span class="apple-link" style="color: #999999; font-size: 12px; text-align: center;">											faCRSA TEAM										</span>										<br>										<span class="apple-link" style="color: #999999; font-size: 12px; text-align: center;">		' + datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S') + '								</span>									</td>								</tr>							</table>						</div>					</div>				</td>				<td style="font-family: sans-serif; font-size: 14px; vertical-align: top;">					&nbsp;				</td>			</tr>		</table>	</body></html>']
            yagmail_server.send(to=email_name, subject=email_title, contents=email_content)
            yagmail_server.close()
        except BaseException as e:
            logging.error(e)
