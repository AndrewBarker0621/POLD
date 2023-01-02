import cv2
import cv2 as open_cv
import numpy as np
import logging
from drawing_utils import draw_contours
from colors import COLOR_GREEN, COLOR_WHITE, COLOR_BLUE
import os
from txt2coordinate import t2c
from yml2coordinate import y2c
from inter_area import intersection
import time


def empty(path):
    if not os.listdir(path):
        return True
    else:
        return False


class MotionDetector:
    LAPLACIAN = 1.4
    DETECT_DELAY = 1

    def __init__(self, coordinates):
        # self.video = video
        self.coordinates_data = coordinates
        # self.start_frame = start_frame
        self.contours = []
        self.bounds = []
        self.mask = []


    def detect_motion(self):
        # capture = open_cv.VideoCapture(self.video)
        # capture.set(open_cv.CAP_PROP_POS_FRAMES, self.start_frame)

        coordinates_data = self.coordinates_data
        logging.debug("coordinates data: %s", coordinates_data)

        for p in coordinates_data:
            coordinates = self._coordinates(p)
            logging.debug("coordinates: %s", coordinates)

            rect = open_cv.boundingRect(coordinates)
            logging.debug("rect: %s", rect)

            new_coordinates = coordinates.copy()
            new_coordinates[:, 0] = coordinates[:, 0] - rect[0]
            new_coordinates[:, 1] = coordinates[:, 1] - rect[1]
            logging.debug("new_coordinates: %s", new_coordinates)

            self.contours.append(coordinates)
            self.bounds.append(rect)

            mask = open_cv.drawContours(
                np.zeros((rect[3], rect[2]), dtype=np.uint8),
                [new_coordinates],
                contourIdx=-1,
                color=255,
                thickness=-1,
                lineType=open_cv.LINE_8)

            mask = mask == 255
            self.mask.append(mask)
            logging.debug("mask: %s", self.mask)

        statuses = [False] * len(coordinates_data)
        times = [None] * len(coordinates_data)

        root = os.getcwd()
        frame_path = root + '/image/yolov5.png'
        label_path = '/home/yangpeng/yolov5/runs/detect/exp/labels'
        yaml_path = root + '/data/coordinates.yml'

        while True:
            time.sleep(0.5)
            while True:
                try:
                    frame = cv2.imread(frame_path)
                    if frame is not None:
                        break
                except:
                    time.sleep(0.1)
                    continue

            blurred = open_cv.GaussianBlur(frame.copy(), (5, 5), 3)
            grayed = open_cv.cvtColor(blurred, open_cv.COLOR_BGR2GRAY)
            new_frame = frame.copy()
            logging.debug("new_frame: %s", new_frame)

            # position_in_seconds = capture.get(open_cv.CAP_PROP_POS_MSEC) / 1000.0
            position_in_seconds = time.time() * 250
            space = y2c(yaml_path)
            occu = [False] * len(space)

            if empty(label_path) == True:
                for index, c in enumerate(coordinates_data):
                    status = self.__apply(grayed, index, c)

                    if times[index] is not None and self.same_status(statuses, index, status):
                        times[index] = None
                        continue

                    if times[index] is not None and self.status_changed(statuses, index, status):
                        if position_in_seconds - times[index] >= MotionDetector.DETECT_DELAY:
                            statuses[index] = status
                            times[index] = None
                        continue

                    if times[index] is None and self.status_changed(statuses, index, status):
                        times[index] = position_in_seconds
            else:
                for index, c in enumerate(coordinates_data):
                    status = self.__apply(grayed, index, c)

                    if times[index] is not None and self.same_status(statuses, index, status):
                        times[index] = None
                        continue

                    if times[index] is not None and self.status_changed(statuses, index, status):
                        if position_in_seconds - times[index] >= MotionDetector.DETECT_DELAY:
                            statuses[index] = status
                            times[index] = None
                        continue

                    if times[index] is None and self.status_changed(statuses, index, status):
                        times[index] = position_in_seconds
                bbox = t2c(label_path)
                for i in range(len(space)):
                    p1 = space[i].reshape([4,2])
                    size = intersection(p1, p1)
                    flag = 0
                    for j in range(len(bbox)):
                        p2 = [(bbox[j,1], bbox[j,2]), (bbox[j,3], bbox[j,2]), (bbox[j,3], bbox[j,4]), (bbox[j,1], bbox[j,4])]
                        inter_area = intersection(p1, p2)
                        if inter_area >= size * 0.51:
                            flag = 1
                            break
                    if flag == 1:
                        occu[i] = True
                        continue

            i = 0
            for index, p in enumerate(coordinates_data):
                coordinates = self._coordinates(p)
                
                if (statuses[index] == False & occu[i] == True) | occu[i] == True:
                    color = COLOR_BLUE
                else:
                    color = COLOR_GREEN
                i = i + 1
                draw_contours(new_frame, coordinates, str(p["id"] + 1), COLOR_WHITE, color)

            open_cv.imshow('real-time', new_frame)
            k = open_cv.waitKey(1)
            print(time.time() * 250)
            if k == ord("q"):
                break
        open_cv.destroyAllWindows()

    def __apply(self, grayed, index, p):
        coordinates = self._coordinates(p)
        logging.debug("points: %s", coordinates)

        rect = self.bounds[index]
        logging.debug("rect: %s", rect)

        roi_gray = grayed[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])]
        laplacian = open_cv.Laplacian(roi_gray, open_cv.CV_64F)
        logging.debug("laplacian: %s", laplacian)

        coordinates[:, 0] = coordinates[:, 0] - rect[0]
        coordinates[:, 1] = coordinates[:, 1] - rect[1]

        status = np.mean(np.abs(laplacian * self.mask[index])) < MotionDetector.LAPLACIAN
        logging.debug("status: %s", status)

        return status

    @staticmethod
    def _coordinates(p):
        return np.array(p["coordinates"])

    @staticmethod
    def same_status(coordinates_status, index, status):
        return status == coordinates_status[index]

    @staticmethod
    def status_changed(coordinates_status, index, status):
        return status != coordinates_status[index]


class CaptureReadError(Exception):
    pass
