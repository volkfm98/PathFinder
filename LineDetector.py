import cv2
import numpy as np

class RoadControl:
    img = np.array([])

    centre = ()
    vec1 = []
    vec2 = []

    img_road_area_height = 170

    def __init__(self, img, ROI_height, viz):
        self.img_road_area_height = ROI_height
        self.visualize = viz
        self.img = img
        
        self.centre = (int(self.img.shape[1] / 2), int(self.img_road_area_height / 2))

        self.vec1 = [-2, -1, 90]
        self.vec2 = [2, -1, 90]

    def filterImg(self):
        img = self.img.copy()[-self.img_road_area_height:]
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gaussian_blur_img = cv2.GaussianBlur(gray_img, (3, 3), 0)
        median_blur_img = cv2.medianBlur(gaussian_blur_img, 3)
        canny_img = cv2.Canny(median_blur_img, 100, 200)
        
        lines_img = canny_img.copy() #np.zeros(treshold_img.shape)

        lines = cv2.HoughLinesP(canny_img, 1, np.pi / 360, 50, minLineLength = 20, maxLineGap = 180)

        if (type(lines) != type(None)):
            for coords in lines:
                if(coords[0][1] > coords[0][3] + 85):
                    cv2.line(lines_img, (coords[0][0], coords[0][1]), (coords[0][2], coords[0][3]), 255, thickness = 3)
                    #for DBG purposes only.
                    if (self.visualize == True):
                        cv2.line(img, 
                            (coords[0][0], coords[0][1]),
                            (coords[0][2], coords[0][3]), 
                            (0, 255, 0), thickness = 3)
        
        if (self.visualize == True):
            cv2.line(img, (self.centre[0], img.shape[0] - self.centre[1]),
                (self.centre[0] + self.vec1[0] * self.vec1[2], img.shape[0] - self.centre[1] + self.vec1[1] * self.vec1[2]),
                (255, 0, 0), thickness = 3)
            
            cv2.line(img, (self.centre[0], img.shape[0] - self.centre[1]),
                (self.centre[0] + self.vec2[0] * self.vec2[2], img.shape[0] - self.centre[1] + self.vec2[1] * self.vec2[2]), 
                (0, 0, 255), thickness = 3)

        if (self.visualize == True):
            cv2.imshow("canny", canny_img)
            cv2.imshow("triggers", img)

        return lines_img

    def poke(self):
        filtered_img = self.filterImg()
        
        leftAlarm = False
        rightAlarm = False

        for i in range(0, self.vec1[2]):
            if (filtered_img[self.centre[1] + self.vec1[1] * i][self.centre[0] + self.vec1[0] * i]  == 255):
                leftAlarm = True

        for i in range(0, self.vec2[2]):
            if (filtered_img[self.centre[1] + self.vec2[1] * i][self.centre[0] + self.vec2[0] * i] == 255):
                rightAlarm = True

        alarm = 0

        if (leftAlarm == True):
            alarm += 2

        if (rightAlarm == True):
            alarm += 1

#        if (self.visualize == True):
            #cv2.imshow('filtered_img', filtered_img)
            #cv2.imshow('primal', self.img)

        return alarm
