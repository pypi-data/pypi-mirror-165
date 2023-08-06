#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Author: Ruinan Zhang
Version: v1.2
LastEditTime: 2022-07-01 09:36:09
E-mail: 2020801253@stu.njau.edu.cn
Copyright (c) 2022 by Ruinan Zhang, All Rights Reserved. Licensed under the GPL v3.0.
"""
import os
import cv2 as cv
import numpy as np
import shutil
import re
import base64
import zipfile


class imgProcessing(object):
    def __init__(self, conf):
        self.initial = os.listdir(conf["initial_path"])
        self.conf = conf
        self.file_array = self.convert_image_format()

    def convert_image_format(self):
        allow_file = ['zip']
        for name in self.initial:
            if name.rsplit('.', 1)[1].lower() in allow_file:
                fz = zipfile.ZipFile(os.path.join(self.conf["initial_path"], name), 'r')
                for file in fz.namelist():
                    fz.extract(file, self.conf["initial_path"])
                fz.close()
                os.remove(self.conf["initial_path"] + name)
        self.initial = os.listdir(self.conf["initial_path"])
        file_array = {}
        previous = os.path.dirname(os.path.abspath(self.conf["initial_path"]))
        os.mkdir(previous + "/convert")
        os.mkdir(previous + "/original")
        for img_name in self.initial:
            temp_name = base64.b64encode(bytes(img_name, encoding="utf8"))
            img_name_new = str(temp_name).split('\'')[1] + str(temp_name).split('\'')[2]
            shutil.copyfile(self.conf["initial_path"] + img_name, previous + "/original/" + img_name)
            os.rename(self.conf["initial_path"] + img_name, self.conf["initial_path"] + img_name_new + ".jpg")
            shutil.move(self.conf["initial_path"] + img_name_new + ".jpg",
                        previous + "/convert/" + img_name_new + ".jpg")
            file_array.update({img_name_new: img_name})
        rename_list = os.listdir(previous + "/convert/")
        for file in rename_list:
            shutil.move(previous + "/convert/" + file, previous + "/initial/" + file)
        self.initial = rename_list
        return file_array

    def get_file_array(self):
        return self.file_array

    def get_imglist(self, type):
        if type == 0:
            self.cut_img()
            imglist = os.listdir(self.conf["predict_out_path"] + "temp")
            return imglist
        elif type == 1:
            shutil.rmtree(self.conf["predict_out_path"] + "temp", True)
            shutil.rmtree(self.conf["predict_out_path"] + "ptemp", True)
            return os.listdir(self.conf["predict_out_path"])

    def cut_img(self):
        os.mkdir(self.conf["predict_out_path"] + "temp")
        temp = self.conf["predict_out_path"] + "temp/"
        for name in self.initial:
            img = cv.imread(self.conf["initial_path"] + name)
            jpgname = name.split(".")[0]
            h, w, c = img.shape
            n = int(h / 3)
            m = int(w / 2)
            img0 = img[0:n, 0:m]
            img1 = img[0:n, m:m * 2]
            img2 = img[n:n * 2, 0:m]
            img3 = img[n:n * 2, m:m * 2]
            img4 = img[n * 2:n * 3, 0:m]
            img5 = img[n * 2:n * 3, m:m * 2]
            cv.imwrite(temp + jpgname + '-1.jpg', img0)
            cv.imwrite(temp + jpgname + '-2.jpg', img1)
            cv.imwrite(temp + jpgname + '-3.jpg', img2)
            cv.imwrite(temp + jpgname + '-4.jpg', img3)
            cv.imwrite(temp + jpgname + '-5.jpg', img4)
            cv.imwrite(temp + jpgname + '-6.jpg', img5)

    def initial_merge_img(self, merge_type):
        img_type = os.listdir(self.conf["predict_out_path"] + "ptemp")
        self.merge_img(img_type, "", merge_type)

    def merge_img(self, file_list, folder, merge_type):
        if merge_type == 0:
            for name in file_list:
                if name.split("_")[-1] == "C.jpg" or name.split("_")[-1] == "MW.jpg" or name.split("_")[-1] == "MC.jpg":
                    file_list.remove(name)
            img_type = "_out_B_M_W.jpg"
        elif merge_type == 1:
            for name in file_list:
                if name.split("_")[-1] == "W.jpg" or name.split("_")[-1] == "MW.jpg" or name.split("_")[-1] == "MC.jpg":
                    file_list.remove(name)
            img_type = "_out_B_M_C.jpg"
        elif merge_type == 2:
            for name in file_list:
                if name.split("_")[-1] == "C.jpg" or name.split("_")[-1] == "MW.jpg" or name.split("_")[-1] == "W.jpg":
                    file_list.remove(name)
            img_type = "_out_MW.jpg"
        elif merge_type == 3:
            for name in file_list:
                if name.split("_")[-1] == "C.jpg" or name.split("_")[-1] == "W.jpg" or name.split("_")[-1] == "MC.jpg":
                    file_list.remove(name)
            img_type = "_out_MC.jpg"
        if folder == '':
            df_okc = "ptemp/"
        else:
            df_okc = folder + "/ptemp/"
        for file in file_list:
            addStr = re.findall('-[0-9]_out\S*', file)[0]
            name = file.replace(addStr, "", 1)
            img1 = cv.imread(self.conf["predict_out_path"] + df_okc + name + "-1" + img_type)
            img2 = cv.imread(self.conf["predict_out_path"] + df_okc + name + "-3" + img_type)
            img3 = cv.imread(self.conf["predict_out_path"] + df_okc + name + "-5" + img_type)
            h = img1.shape[0] + img2.shape[0] + img3.shape[0]
            arr1 = np.zeros((h, img1.shape[1], 3), np.uint8)
            arr1[0:img1.shape[0], 0:img1.shape[1]] = img1
            arr1[img1.shape[0]:img1.shape[0] + img2.shape[0], 0:img1.shape[1]] = img2
            arr1[img1.shape[0] + img2.shape[0]:h, 0:img1.shape[1]] = img3

            img4 = cv.imread(self.conf["predict_out_path"] + df_okc + name + "-2" + img_type)
            img5 = cv.imread(self.conf["predict_out_path"] + df_okc + name + "-4" + img_type)
            img6 = cv.imread(self.conf["predict_out_path"] + df_okc + name + "-6" + img_type)
            h2 = img4.shape[0] + img5.shape[0] + img6.shape[0]
            arr2 = np.zeros((h2, img4.shape[1], 3), np.uint8)
            arr2[0:img4.shape[0], 0:img4.shape[1]] = img4
            arr2[img4.shape[0]:img4.shape[0] + img5.shape[0], 0:img4.shape[1]] = img5
            arr2[img4.shape[0] + img5.shape[0]:h, 0:img4.shape[1]] = img6

            res = np.zeros((arr2.shape[0], arr2.shape[1] * 2, 3), np.uint8)
            res[0:arr1.shape[0], 0:arr1.shape[1]] = arr1
            res[0:arr2.shape[0], arr1.shape[1]: arr1.shape[1] + arr2.shape[1]] = arr2
            cv.imwrite(self.conf["predict_out_path"] + folder + "/" + name + img_type, res)
