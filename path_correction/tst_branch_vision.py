#!/bin/python3

import cv2
import numpy as np

class RoadControl:
    img = np.array([])

    centre = ()
    vec1 = []
    vec2 = []

    window_size = [15, 15] 

    img_road_area_height = 400

    def setup(self):
        self.centre = (int(self.img.shape[1] / 2), int(self.img_road_area_height / 2))

        self.vec1 = [-2, -1, 90]
        self.vec2 = [2, -1, 90]

        #TODO: normalize vectors 

    def filterImg(self):
        img = self.img.copy()[-self.img_road_area_height:]
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #ret, filtered_img = cv2.threshold(gray_img, 210, 255, cv2.THRESH_BINARY)
        gaussian_blur_img = cv2.GaussianBlur(gray_img, (5, 3), 1)
        median_blur_img = cv2.medianBlur(gray_img, 5)
        treshold_img = cv2.threshold(median_blur_img, 210, 255, cv2.THRESH_BINARY)[1]

        lines_img = np.zeros(treshold_img.shape)

        lines = cv2.HoughLinesP(treshold_img, 1, np.pi / 180, 20, minLineLength = 5, maxLineGap = 190)

        if (type(lines) != type(None)):
            for coords in lines:
                cv2.line(lines_img, (coords[0][0], coords[0][1]), (coords[0][2], coords[0][3]), 255, thickness = 3)
                #for DBG purposes only!!!
                cv2.line(self.img, 
                        (coords[0][0], coords[0][1] + self.img.shape[0] - self.img_road_area_height),
                        (coords[0][2], coords[0][3] + self.img.shape[0] - self.img_road_area_height), 
                        (0, 255, 0), thickness = 3)

        cv2.imshow("tresh", treshold_img)

        return lines_img

    def poke(self, visualize = False):
        filtered_img = self.filterImg()
        
        leftAlarm = False
        rightAlarm = False

        for i in range(0, self.vec1[2]):
            if (filtered_img[self.centre[1] + self.vec1[1] * i][self.centre[0] + self.vec1[0] * i]  == 255):
                leftAlarm = True

        cv2.line(self.img, (self.centre[0], self.img.shape[0] - self.centre[1]),
                (self.centre[0] + self.vec1[0] * self.vec1[2], self.img.shape[0] - self.centre[1] + self.vec1[1] * self.vec1[2]),
                (255, 0, 0), thickness = 3)
 
        #cv2.line(filtered_img, (self.centre[0], self.centre[1]),
        #        (self.centre[0] + self.vec1[0] * self.vec1[2], self.centre[1] + self.vec1[1] * self.vec1[2]),
        #        255, thickness = 3)

        for i in range(0, self.vec2[2]):
            if (filtered_img[self.centre[1] + self.vec2[1] * i][self.centre[0] + self.vec2[0] * i] == 255):
                rightAlarm = True
        
        cv2.line(self.img, (self.centre[0], self.img.shape[0] - self.centre[1]),
                (self.centre[0] + self.vec2[0] * self.vec2[2], self.img.shape[0] - self.centre[1] + self.vec2[1] * self.vec2[2]), 
                (0, 0, 255), thickness = 3)

        #cv2.line(filtered_img, (self.centre[0], self.centre[1]),
        #        (self.centre[0] + self.vec2[0] * self.vec2[2], self.centre[1] + self.vec2[1] * self.vec2[2]), 
        #        255, thickness = 3)

        alarm = 0

        if (leftAlarm == True):
            alarm += 2

        if (rightAlarm == True):
            alarm += 1

        if (visualize):
            cv2.imshow('filtered_img', filtered_img)
            cv2.imshow('car_vision', self.img)

#            print(filtered_img.shape)

        return alarm

tst = RoadControl()

vidcap = cv2.VideoCapture('mov.mp4')

while (True):
    tst.img = vidcap.read()[1]

#    print(tst.centre)
#    print(tst.img.shape)

    tst.setup()

    print(tst.poke(visualize = True))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
