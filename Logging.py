import logging
import os


class Logging():

    def __init__(self, username=None, level="DEBUG"):
        # 创建日志对象
        path = "D:\\log\\"
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        self.log = logging.getLogger(username)
        self.log.setLevel(level)

    def ConsoleHandle(self, level="WARNING"):
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(self.get_formatter()[0])
        return console_handler

    def FileHandle(self, path, level="INFO"):
        # 创建文件处理器
        file_handler = logging.FileHandler(path, encoding='gbk')
        file_handler.setLevel(level)
        file_handler.setFormatter(self.get_formatter()[1])
        return file_handler

    def get_formatter(self):
        # 日志文本格式
        ConsoleHandle = logging.Formatter(fmt="[%(name)s][%(levelname)s][%(asctime)s][%(lineno)s][%(message)s]")
        FileHandle = logging.Formatter(fmt="[%(name)s][%(levelname)s][%(asctime)s][%(lineno)s][%(message)s]")
        return ConsoleHandle, FileHandle

    def get_log(self, path):
        self.log.addHandler(self.ConsoleHandle())
        self.log.addHandler(self.FileHandle(path))
        return self.log
