import os
import threading
from datetime import datetime

from framework.browser.browser import Browser
from framework.utils.datetime_util import DatetimeUtil
from framework.utils.logger import Logger
from framework.utils.config_reader import PathProvider


class Screenshooter:
    __session_dir = None
    __screen_number = 1
    __screen_dir = PathProvider.get_screenshots_path()
    FORMAT_DATETIME_FOR_SCREEN = "%d-%m-%Y_%H-%M-%S"
    FILE_FORMAT_PNG = ".png"

    @staticmethod
    def set_session_screen_dir():
        lock = threading.Lock()
        lock.acquire()
        try:
            if not os.path.exists(Screenshooter.__screen_dir):
                Logger.get_logger().info("Creating folder for screenshots: " + Screenshooter.__screen_dir.as_posix())
                os.makedirs(Screenshooter.__screen_dir)

            new_screen_path = os.path.join(
                Screenshooter.__screen_dir,
                "Session_" + DatetimeUtil.get_str_datetime(Screenshooter.FORMAT_DATETIME_FOR_SCREEN))

            if Screenshooter.__session_dir is None and not os.path.exists(new_screen_path):
                Screenshooter.__session_dir = new_screen_path
            else:
                Screenshooter.__session_dir = new_screen_path + "." + str(datetime.now().microsecond)

            Logger.get_logger().info("Folder creating " + new_screen_path)
            os.makedirs(Screenshooter.__session_dir)
        finally:
            lock.release()

    @staticmethod
    def get_screen_file_name(file_format=FILE_FORMAT_PNG):
        scr_number = str(Screenshooter.__screen_number)
        Screenshooter.__screen_number += 1
        return "Screenshot_" + scr_number + file_format

    @staticmethod
    def take_screenshot():
        screen_name = Screenshooter.get_screen_file_name()
        save_screen_path = os.path.join(Screenshooter.__session_dir, screen_name)

        Logger.get_logger().info("Making screenshot to file " + screen_name)
        Browser.get_driver().save_screenshot(save_screen_path)
