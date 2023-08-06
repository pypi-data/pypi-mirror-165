#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Author: Ruinan Zhang
Version: v1.2
LastEditTime: 2022-07-01 09:36:01
E-mail: 2020801253@stu.njau.edu.cn
Copyright (c) 2022 by Ruinan Zhang, All Rights Reserved. Licensed under the GPL v3.0.
"""
import logging

from PIL import Image
import numpy as np
import random
import os

# hide tensorflow log (info level)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import copy
import tensorflow as tf
import time
import importlib
from facrsa_code.library.analysis.net.rootseg.RootSeg import RootSeg

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)


class imgPredict(object):
    def __init__(self, conf):
        self.NCLASSES = 2
        self.HEIGHT = 512
        self.WIDTH = 512
        self.class_colors = [[0, 0, 0], [0, 255, 0]]
        self.class_colors2 = [[0, 0, 0], [255, 255, 255]]
        self.conf = conf
        model_file_m = "main.h5"
        model_file_b_m = "all.h5"
        # use default model to segment  primary  root.
        # Todo: allow researcher to segment primary root by private plugins
        self.model_m = RootSeg(n_classes=self.NCLASSES, input_height=self.HEIGHT, input_width=self.WIDTH)
        self.model_m.load_weights(os.path.dirname(os.path.abspath(__file__)) + "/net/rootseg/weight/" + model_file_m)
        # this command will be convert to <code> from 'net.conf['uid'].conf['pid'].network import
        if conf['pid'] == '1':
            self.model_b_m = RootSeg(n_classes=2, input_height=self.HEIGHT, input_width=self.WIDTH)
            self.model_b_m.load_weights(
                os.path.dirname(os.path.abspath(__file__)) + "/net/rootseg/weight/" + model_file_b_m)
        else:
            logging.info("Loading private plugin")
            self.model_b_m = importlib.import_module(
                'facrsa_code.library.analysis.net.{}.{}.{}'.format(conf['uid'], conf['pid'], "network")).main()
            self.model_b_m.load_weights(
                os.path.join(os.getcwd(), "facrsa_code", "library", "analysis", "net", str(conf['uid']),
                             str(conf['pid']), "weight.h5"))

    def initial_predict(self, img_list):
        random.seed(0)
        os.mkdir(self.conf["predict_out_path"] + "ptemp")
        temp_list = os.listdir(self.conf["predict_out_path"] + "/temp")
        self.predict(temp_list, "")

    def predict(self, temp_list, folder):
        time_res = []
        for jpg in temp_list:
            img = Image.open(self.conf["predict_out_path"] + folder + "/temp/" + jpg)
            old_img = copy.deepcopy(img)
            orininal_h = np.array(img).shape[0]
            orininal_w = np.array(img).shape[1]
            img = img.resize((self.WIDTH, self.HEIGHT))
            img = np.array(img)
            img = img / 255
            img = img.reshape(-1, self.HEIGHT, self.WIDTH, 3)
            start = time.time()
            pr1 = self.model_m.predict(img)[0]
            end = time.time()
            alltime = end - start
            time_res.append(alltime)
            pr2 = self.model_b_m.predict(img)[0]
            pr1 = pr1.reshape((int(self.HEIGHT), int(self.WIDTH), self.NCLASSES)).argmax(axis=-1)
            pr2 = pr2.reshape((int(self.HEIGHT), int(self.WIDTH), self.NCLASSES)).argmax(axis=-1)
            seg_img1 = np.zeros((int(self.HEIGHT), int(self.WIDTH), 3))
            seg_img2 = np.zeros((int(self.HEIGHT), int(self.WIDTH), 3))
            seg_img3 = np.zeros((int(self.HEIGHT), int(self.WIDTH), 3))
            seg_img4 = np.zeros((int(self.HEIGHT), int(self.WIDTH), 3))
            colors = self.class_colors
            colors2 = self.class_colors2
            for c in range(self.NCLASSES):
                seg_img1[:, :, 0] += ((pr1[:, :] == c) * (colors[c][0])).astype('uint8')
                seg_img1[:, :, 1] += ((pr1[:, :] == c) * (colors[c][1])).astype('uint8')
                seg_img1[:, :, 2] += ((pr1[:, :] == c) * (colors[c][2])).astype('uint8')
            for d in range(self.NCLASSES):
                seg_img2[:, :, 0] += ((pr1[:, :] == d) * (colors2[d][0])).astype('uint8')
                seg_img2[:, :, 1] += ((pr1[:, :] == d) * (colors2[d][1])).astype('uint8')
                seg_img2[:, :, 2] += ((pr1[:, :] == d) * (colors2[d][2])).astype('uint8')
            for c in range(self.NCLASSES):
                seg_img3[:, :, 0] += ((pr2[:, :] == c) * (colors[c][0])).astype('uint8')
                seg_img3[:, :, 1] += ((pr2[:, :] == c) * (colors[c][1])).astype('uint8')
                seg_img3[:, :, 2] += ((pr2[:, :] == c) * (colors[c][2])).astype('uint8')
            for d in range(self.NCLASSES):
                seg_img4[:, :, 0] += ((pr2[:, :] == d) * (colors2[d][0])).astype('uint8')
                seg_img4[:, :, 1] += ((pr2[:, :] == d) * (colors2[d][1])).astype('uint8')
                seg_img4[:, :, 2] += ((pr2[:, :] == d) * (colors2[d][2])).astype('uint8')
            seg_img1 = Image.fromarray(np.uint8(seg_img1)).resize((orininal_w, orininal_h))
            seg_img2 = Image.fromarray(np.uint8(seg_img2)).resize((orininal_w, orininal_h))
            seg_img3 = Image.fromarray(np.uint8(seg_img3)).resize((orininal_w, orininal_h))
            seg_img4 = Image.fromarray(np.uint8(seg_img4)).resize((orininal_w, orininal_h))
            image1 = Image.blend(old_img, seg_img1, 0.3)
            image2 = Image.blend(old_img, seg_img3, 0.3)
            name1 = jpg.split(".jpg")[0] + "_out_MC.jpg"
            name2 = jpg.split(".jpg")[0] + "_out_MW.jpg"
            name3 = jpg.split(".jpg")[0] + "_out_B_M_C.jpg"
            name4 = jpg.split(".jpg")[0] + "_out_B_M_W.jpg"
            image1.save(self.conf["predict_out_path"] + folder + "/ptemp/" + name1)
            image2.save(self.conf["predict_out_path"] + folder + "/ptemp/" + name3)
            seg_img2.save(self.conf["predict_out_path"] + folder + "/ptemp/" + name2)
            seg_img4.save(self.conf["predict_out_path"] + folder + "/ptemp/" + name4)
