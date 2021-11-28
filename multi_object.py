#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Yanshee机器人
opencv图像识别
轮廓检测
图形识别
蓝红多颜色检测
使用例
"""
__author__ = "Shiina""&""Old Yellow"
__date__ = "2021/11/11"
__version__ = "1.0.0"

from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
# define resolution
resX = 640
resY = 480

myColors = [[169, 151, 32,179, 255, 210],  # 红色
            [88, 146, 66, 113, 231, 246],  # 蓝色
            [57,76,0,100,255,255],
            [90,48,0,118,255,255]]
myColorValues = ['red',         # BGR
                 'blue',
                 [0,255,0],
                 [255,0,0]]

# 轮廓检测
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def getContours(img, imgContour):
    image, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
    while true
        if area > 500:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            objCor = len(approx)
            if objCor == 3:
                objectType = "Tri"
            elif objCor == 4:
                aspRatio = w / float(h)
                if 0.95 < aspRatio < 1.05:
                    objectType = "square"
                else:
                    objectType = "Rectangle"
            elif objCor > 4:
                objectType = "Circle"
            else:
                objectType = "None"

            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 0, 0), 2)  # 方框
            cv2.putText(imgContour, objectType, (x + (w // 2) - 10, y + (h // 2) - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                        (0, 0, 0), 2)  # 形状

    return x + w // 2, y, w, h


def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y, w, h = getContours(mask, imgContour)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
            cv2.putText(imgContour, str(myColorValues[count]), (x + (w // 2) - 10, y + (h // 2) - 20),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 2)  # 形状

        count += 1

        # cv2.imshow(str(color[0]),mask)
    return newPoints


count = 0
# 版本管理
print("当前版本：", __version__)
# 初始化摄像头
camera = PiCamera()
camera.resolution = (resX, resY)
camera.framerate = 30
# Use this as our output
rawCapture = PiRGBArray(camera, size=(resX, resY))

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img = frame.array

    imgContour = img.copy()

    findColor(imgContour, myColors, myColorValues)
    cv2.imshow("res", imgContour)

    # if the `q` key was pressed, break from the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if key == ord("s"):
        count = count + 1
        cv2.imwrite("testbak" + str(count) + ".jpg", image)
        print("save success")

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

# When everything done, release the capture
cv2.destroyAllWindows()
camera.close()
# 蓝色十米内不丢失
# 红色五米内不丢失

