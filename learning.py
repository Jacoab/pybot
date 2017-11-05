import cv2 as cv
import numpy as np


class ImageProcessor(object):
    @staticmethod
    def process_img(original_img):
        processed_img = cv.cvtColor(original_img, cv.COLOR_BGR2GRAY)
        processed_img = cv.Canny(processed_img, threshold1=200, threshold2=300)

        vertices = np.array([[10, 500], [10, 300], [300, 200], [500, 200], [800, 300], [800, 500],
                             ], np.int32)
        processed_img = ImageProcessor.roi(processed_img, [vertices])
        return processed_img

    @staticmethod
    def roi(img, vertices):
        # blank mask:
        mask = np.zeros_like(img)
        # fill the mask
        cv.fillPoly(mask, vertices, 255)
        # now only show the area that is the mask
        masked = cv.bitwise_and(img, mask)
        return masked


# def basic_rule(self, processed_img):
#     '''
#     Simple self driving rule that aims to avoid the white edges created in the process_img()
#     method.  The left and right directions are given scores and each screen grab is analyzed
#
#
#     :param processed_img:
#     '''
#     count = 0
#     window_width = self.windows[self.screen_num][1][2]
#     window_height = self.windows[self.screen_num][1][3]
#     focal_point =[int(window_height/2), int(window_width/2)]
#
#     # w_score = 0
#     # s_score = 0
#     a_score = 0
#     d_score = 0
#
#     for i, row in enumerate(processed_img):
#         for j, pixel in enumerate(row):
#             if pixel > 200:
#                 if (i < focal_point[0] and j < focal_point[1]) or \
#                     (i > focal_point[0] and j > focal_point[1]):
#                     d_score += 1
#                 elif (i < focal_point[0] and j > focal_point[1]) or \
#                         (i > focal_point[0] and j > focal_point[1]):
#                     a_score += 1
#
#     press_key(W)
#     if a_score > d_score:
#         press_key(A)
#     else:
#         press_key(D)