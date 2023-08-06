#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Author: Ruinan Zhang
Version: v1.2
LastEditTime: 2022-08-06 15:25:20
E-mail: 2020801253@stu.njau.edu.cn
Copyright (c) 2022 by Ruinan Zhang, All Rights Reserved. Licensed under the GPL v3.0.
"""
import cv2 as cv
import numpy as np
from skimage import measure
import pandas as pd
import math
from skimage.morphology import convex_hull_image, skeletonize
from facrsa_code.library.analysis.database.writermysql import update_schedule, update_task_error
from facrsa_code.library.analysis.errorcheck import send_mail_user


class rootAnalysis():
    def __init__(self, img_list, conf, file_array, tid):
        self.conf = conf
        self.tid = tid
        self.df = pd.DataFrame(
            columns=["Image_Name", "Total_Root_Length(cm)", "Total_Root_Projected_Area(cm2)",
                     'Total_Surface_Area(cm2)',
                     'Total_Root_Volume(cm3)', "Primary_Root_Length(cm)", "Primary_Root_Projected_Area(cm2)",
                     "Primary_Root_Surface_Area(cm2)", "Primary_Root_Volume(cm3)",
                     'Convex_Hull_Area(cm2)', 'Max_Root_Depth(cm)', 'Angle_Left(°)', 'Angle_Center(°)',
                     'Angle_Right(°)'])
        self.file_array = file_array
        temp_list = []
        for name in img_list:
            if (name.split("_")[-1] == "W.jpg"):
                temp_list.append(name)
        for img in temp_list:
            self.img_analysis_b_m(img)
        self.df.to_csv(self.conf["out_path"] + "/" + "result.csv", index=False)

    def check_pxiel(self, src):
        check_res = np.where(src > 10)
        if int(check_res[0].shape[0]) == 0:
            return 0
        else:
            return 1

    def img_analysis_b_m(self, img):
        src = cv.imread(self.conf["predict_out_path"] + img)
        r, new = cv.threshold(src, 127, 255, cv.THRESH_BINARY)
        gray_img = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
        try:
            check_res = self.check_pxiel(gray_img)
            if check_res == 0:
                raise ValueError("None root pixels")
        except ValueError as e:
            # If the root system is not segmented, this message is returned and all processes are terminated
            msg = "We did not detect any root pixels. Please check the uploaded images and resubmit the task."
            send_mail_user(msg, self.conf)
            update_task_error(self.tid)
            exit()
        else:
            # Analysis of the connectivity domain
            parr, imgxx = self.draw_connect(src, 0)
            # Image Skeleton Extraction
            thinimg = self.img_thin(new)
            # root length (primary root + branched root)
            all_length, all_pnum_l = self.count_length(thinimg)
            # root projected area (primary root + branched root)
            all_area, all_pnum_a = self.count_area(parr)
            r, new2 = cv.threshold(gray_img, 100, 255, cv.THRESH_BINARY)
            # root surface area (primary root + branched root)
            all_surface_area = self.count_surface_area(new2)
            convex_area = self.count_convex_hull_area(gray_img)
            max_root_depth = self.count_depth(new2)
            volume = self.count_volume(all_surface_area, all_length)
            angle_left, angle_center, angle_right = self.count_angle(new)

            imgname = img.split("_out_B_M_W.jpg")[0] + "_out_MW.jpg"
            m_src = cv.imread(self.conf["predict_out_path"] + imgname)
            r1, t1 = cv.threshold(m_src, 127, 255, cv.THRESH_BINARY)
            # Analysis of the connectivity domain
            m_parr, m_imgxx = self.draw_connect(t1, 0)
            # Image Skeleton Extraction
            m_thinimg = self.img_thin(t1)
            # root length (primary root)
            m_length, m_pnum_l = self.count_length(m_thinimg)
            # root projected area (primary root)
            m_area, m_pnum_a = self.count_area(t1)
            # root surface area (primary root)
            m_surface_area = self.count_surface_area(t1)
            m_volume = self.count_volume(m_surface_area, m_length)
            data = {
                "Image_Name": self.file_array[img.split("_out_B_M_W.jpg")[0]],
                "Total_Root_Length(cm)": round(all_length, 3),
                "Total_Root_Projected_Area(cm2)": round(all_area, 3),
                'Total_Surface_Area(cm2)': round(all_surface_area, 3),
                'Total_Root_Volume(cm3)': round(volume, 3),
                "Primary_Root_Length(cm)": round(m_length, 3),
                "Primary_Root_Projected_Area(cm2)": round(m_area, 3),
                'Primary_Root_Surface_Area(cm2)': round(m_surface_area, 3),
                'Primary_Root_Volume(cm3)': round(m_volume, 3),
                'Convex_Hull_Area(cm2)': round(convex_area, 3),
                'Max_Root_Depth(cm)': round(max_root_depth, 3),
                'Angle_Left(°)': round(angle_left, 2),
                'Angle_Center(°)': round(angle_center, 2),
                'Angle_Right(°)': round(angle_right, 2)
            }
            self.df = self.df.append(data, ignore_index=True)

    def draw_connect(self, image, type):
        if type == 1:
            gray = image.copy()
        else:
            gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
        ret, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
        imgxx = image.copy()
        lable = measure.label(binary, connectivity=2)
        props = measure.regionprops(lable, intensity_image=None, cache=True)
        parr = []
        for i in range(len(props)):
            parr.append([i, props[i].coords])
        return parr, imgxx

    def img_thin(self, img):
        skeleton = skeletonize(img)
        gray = cv.cvtColor(skeleton, cv.COLOR_RGB2GRAY)
        gray = np.where(gray > 1, 255, 0)
        return gray

    def count_length(self, thinimg):
        pixelnum = (thinimg[:, :] == 255).sum()
        length = pixelnum * self.conf["length_ratio"]
        return length, pixelnum

    def count_area(self, parr):
        pixelnum = 0
        for p in range(0, len(parr)):
            pixelnum = pixelnum + len(parr[p][1])
        area = pixelnum * self.conf["area_ratio"]
        return area, pixelnum

    def count_depth(self, img):
        first = np.where(img == 255)[0][0] * self.conf["length_ratio"]
        last = np.where(img == 255)[0][-1] * self.conf["length_ratio"]
        depth = last - first
        return depth

    def count_volume(self, surface_area, all_length):
        volume = 3.1415927 * surface_area * surface_area / 4 / all_length * 0.1
        return volume

    def count_surface_area(self, img):
        can = cv.Canny(img, 1, 255)
        area = np.where(img == 255)[0].shape[0]
        edge = np.where(can == 255)[0].shape[0]
        surface_area = (area - (edge / 2 + 1)) * 3.1415927 * self.conf["area_ratio"]
        return surface_area

    def count_convex_hull_area(self, img):
        points = convex_hull_image(img)
        convexhull_area = np.where(points == True)[0].shape[0] * self.conf["area_ratio"]
        return convexhull_area

    def count_angle(self, initial):
        t = cv.cvtColor(initial * 255, cv.COLOR_BGR2GRAY) * 255
        edge = cv.Canny(t[0:200, :], 50, 150, apertureSize=3)
        try:
            line_points_plus = []
            line_points_minus = []
            lines = cv.HoughLines(edge, 1, np.pi / 180, 40)
            for line in lines:
                rho, theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                if y1 > 0:
                    line_points_plus.append([x1, y1, x2, y2])
                else:
                    line_points_minus.append([x1, y1, x2, y2])
            cross_point_res = []
            for plus in line_points_plus:
                for minus in line_points_minus:
                    cross_point_res.append(self.cross_point(plus, minus))
            for i in range(0, len(cross_point_res)):
                for j in range(0, 2):
                    cross_point_res[i][j] = int(cross_point_res[i][j])
            need_to_fit = np.array(cross_point_res)
            first_line = 0
            t_line_index = 0
            for t_line in t[0:200, :]:
                res = [i for i in np.where(t_line > 100)[0]]
                if len(res) > 0:
                    first_line = t_line_index
                    break
                t_line_index += 1
            temp = [list(i) for i in need_to_fit if i[1] > 0]
            temp_1 = []
            for value in temp:
                temp_1.append(value[1])
            best_near = temp[temp_1.index(min(temp_1, key=lambda x: abs(x - 94)))]
            while best_near[1] > first_line:
                temp.remove(best_near)
                temp_1 = []
                for value in temp:
                    temp_1.append(value[1])
                best_near = temp[temp_1.index(min(temp_1, key=lambda x: abs(x - 94)))]
            best_near_copy = best_near
            if abs(best_near_copy[1] - first_line) > 20:
                best_near_copy[1] = first_line
            search_array = np.where(t[best_near_copy[1]:best_near_copy[1] + 200, :] > 150)
            right = [max(list(search_array[1])),
                     search_array[0][list(search_array[1]).index(max(list(search_array[1])))] + best_near[1]]
            left = [min(list(search_array[1])), search_array[0][-1] + best_near[1]]
            L1 = [left, best_near_copy]
            L2 = [right, best_near_copy]
            L3 = [[best_near_copy[0] - 20, best_near_copy[1]], [best_near_copy[0] + 20, best_near_copy[1]]]
            angle_left = self.angle_3(L1, L3)
            angle_right = self.angle_3(L2, L3)
            angle_center = 180 - angle_left - angle_right
            return angle_left, angle_center, angle_right
        except BaseException as e:
            logging.error(e)
            return 0, 0, 0

    def append_df(self, file, length, area, pnum_l, pnum_a):
        file = file.split("_out_MW")[0] + file.split("_out_MW")[1]
        data = {
            'Image Name': file,
            'Root Length(mm)': length,
            'Root Area(mm²)': area,
            'Pixels number(L)': pnum_l,
            'Pixels number(A)': pnum_a
        }
        self.df = self.df.append(data, ignore_index=True)

    def append_df_b_m(self, data):
        self.df = self.df.append(data, ignore_index=True)

    # 计算交点函数
    def cross_point(self, line1, line2):
        # 取直线坐标两点的x和y值
        x1 = line1[0]
        y1 = line1[1]
        x2 = line1[2]
        y2 = line1[3]

        x3 = line2[0]
        y3 = line2[1]
        x4 = line2[2]
        y4 = line2[3]

        # L2直线斜率不存在操作
        if (x4 - x3) == 0:
            k2 = None
            b2 = 0
            x = x3
            # 计算k1,由于点均为整数，需要进行浮点数转化
            k1 = (y2 - y1) * 1.0 / (x2 - x1)
            # 整型转浮点型是关键
            b1 = y1 * 1.0 - x1 * k1 * 1.0
            y = k1 * x * 1.0 + b1 * 1.0
        elif (x2 - x1) == 0:
            k1 = None
            b1 = 0
            x = x1
            k2 = (y4 - y3) * 1.0 / (x4 - x3)
            b2 = y3 * 1.0 - x3 * k2 * 1.0
            y = k2 * x * 1.0 + b2 * 1.0
        else:
            # 计算k1,由于点均为整数，需要进行浮点数转化
            k1 = (y2 - y1) * 1.0 / (x2 - x1)
            # 斜率存在操作
            k2 = (y4 - y3) * 1.0 / (x4 - x3)
            # 整型转浮点型是关键
            b1 = y1 * 1.0 - x1 * k1 * 1.0
            b2 = y3 * 1.0 - x3 * k2 * 1.0
            x = (b2 - b1) * 1.0 / (k1 - k2)
            y = k1 * x * 1.0 + b1 * 1.0
        return [x, y]

    def angle_3(self, L1, L2):
        a = L1[0]
        b = L1[1]
        c = L2[1]
        ang = math.degrees(
            math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
        temp = ang + 360 if ang < 0 else ang
        angle = abs(180 - temp)
        return angle if angle < 90 else 180 - angle
