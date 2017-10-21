from mss import mss
from controls import press_key, W, A, S, D

import numpy as np
import cv2 as cv

import win32gui
import win32con
import time

class GameBot(object):
    def __init__(self, game, screen_num):
        self.game = game
        self.screen_num = screen_num
        self.windows = []
        self.screen_grabs = []
        self.get_window_sizes()

    def get_window_sizes(self):
        '''
        Return a list of tuples (handler, (width, height)) for each real window.
        '''
        def callback(hWnd, windows):
            if not _is_real_window(hWnd):
                return
            rect = win32gui.GetWindowRect(hWnd)
            windows.append((hWnd, (rect[1], rect[0], (rect[2] - rect[0])-17, (rect[3] - rect[1])-10)))
        windows = []
        win32gui.EnumWindows(callback, windows)
        self.windows = windows

    def screen_grab(self):
        with mss() as screen_capture:
            monitor = {'top': self.windows[self.screen_num][1][0],
                       'left': self.windows[self.screen_num][1][1]+10,
                       'width': self.windows[self.screen_num][1][2],
                       'height': self.windows[self.screen_num][1][3]}
            img = np.array(screen_capture.grab(monitor))
            self.screen_grabs.append(img)
            return img

    def run(self):
        last_time = time.time()
        while True:
            press_key(W)
            img = self.screen_grab()
            print('fps: {0}'.format(1 / (time.time() - last_time)))
            cv.imshow('OpenCV/Numpy normal', img)
            if cv.waitKey(25) & 0xFF == ord('q'):
                cv.destroyAllWindows()
                break




def _is_real_window(hWnd):
    '''
    Return True iff given window is a real Windows application window.
    '''
    if not win32gui.IsWindowVisible(hWnd):
        return False
    if win32gui.GetParent(hWnd) != 0:
        return False
    has_no_owner = win32gui.GetWindow(hWnd, win32con.GW_OWNER) == 0
    l_ex_style = win32gui.GetWindowLong(hWnd, win32con.GWL_EXSTYLE)
    if (((l_ex_style & win32con.WS_EX_TOOLWINDOW) == 0 and has_no_owner)
      or ((l_ex_style & win32con.WS_EX_APPWINDOW != 0) and not has_no_owner)):
        if win32gui.GetWindowText(hWnd):
            return True
    return False

