import re
import os
import functools
import sys
import threading
from copy import deepcopy
from inspect import isfunction
from queue import Queue
from colour_printing.config import CPConfig
from colour_printing.exception import PrintMeError

stream = sys.stdout


def level_wrap(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        level = func.__name__.upper()
        default = self.cp._default.get(level, {})
        data = {}
        # 参数
        for i in self.cp._terms:
            w = kwargs.get(i)
            if w:
                data[i] = w
            else:
                dd = default.get(i, "")
                if isfunction(dd):
                    data[i] = dd()
                else:
                    data[i] = dd
        sep = kwargs.get('sep', " ")
        if args:
            data['message'] = sep.join([str(i) for i in args])
        # record
        self.handler_record(deepcopy(data))
        # 最高优先级,对data的操作会影响后续操作的输出内容
        res = func(self, data)
        # 日志
        if level not in self.log_filter and self.Master_switch:
            msg = self.cp._rawtemplate.format(**data) + "\n"
            self.queue.put(msg)
        # 打印
        if self.switch and self.Master_switch and level not in self.print_filter:
            end = kwargs.get('end', '\n')
            self.show(level, data=data, end=end)
        return res

    return wrap


class ColourPrinting(object):
    Master_switch = True

    @classmethod
    def shutdown(cls):
        cls.Master_switch = False

    @level_wrap
    def info(self, data: dict):
        """最高优先级,对data的操作会影响后续操作(日志,打印)的输出内容"""

    @level_wrap
    def debug(self, data: dict):
        """最高优先级,对data的操作会影响后续操作(日志,打印)的输出内容"""

    @level_wrap
    def error(self, data: dict):
        """最高优先级,对data的操作会影响后续操作(日志,打印)的输出内容"""

    @level_wrap
    def warning(self, data: dict):
        """最高优先级,对data的操作会影响后续操作(日志,打印)的输出内容"""

    @level_wrap
    def success(self, data: dict):
        """最高优先级,对data的操作会影响后续操作(日志,打印)的输出内容"""

    def handler_record(self, record: dict):
        """record不受level函数影响,处理日志信息 重写此函数以应用每个不同的使用场景 """


class LogHandler(object):
    def __init__(self, printme):
        self.printme = printme
        self.log_path = os.getcwd()
        self.log_name = 'colour_printing_log.log'
        self.log_delay = 60 * 2
        self.main_t = None

    def run(self, log_path: str = '', log_name: str = ''):  # log
        """
        :param log_path: 路径
        :param log_name: 文件名
        :return:
        """
        if log_path:
            self.log_path = log_path
        if log_name:
            self.log_name = log_name
        self.main_t = threading.currentThread()
        t = threading.Thread(target=self.__log_to_file, args=())
        t.start()

    def __log_to_file(self):
        path = os.path.join(self.log_path, self.log_name)
        stream.write(f'[*]Tip>> 日志文件path: {path}\n')
        with open(path, 'a+') as f:
            while True:
                if self.printme.queue.empty():
                    if self.main_t.isAlive():
                        continue
                    else:
                        break
                f.write(self.printme.queue.get())
                f.flush()


class PrintMe(ColourPrinting):

    def __init__(self, cp: CPConfig, **kwargs):
        # store
        # style config
        self.cp = cp
        # switch
        self.__switch = True
        self.__print_filter = []
        self.__log_filter = []
        # log
        self.queue = Queue()
        self.log_handler = LogHandler(printme=self)
        # custom args
        for k, v in kwargs.items():
            if k in dir(self):
                raise PrintMeError(f'变量名"{k}"已被定义咯,请更换其他变量名')
            setattr(self, k, v)

    def show(self, level: str, data: dict, end: str):
        # style
        if not self.cp._box.get(level.upper()):
            msg = self.cp._rawtemplate.format(**data)
        else:
            style = self.cp._box.get(level.upper())
            data.update(style)
            msg = self.cp._template.format(**data)
        stream.write(msg)
        stream.write(end)

    def set_default(self, **kwargs):
        """
        设置默认值
        :param kwargs:
        :return:
        """
        level = kwargs.get('set_level')
        if level:
            if level.upper() in self.cp._levels:
                for k, v in kwargs.items():
                    self.cp._default[level.upper()].update({k: v})
        else:
            for level in self.cp._levels:
                for k, v in kwargs.items():
                    self.cp._default[level.upper()].update({k: v})

    @property
    def switch(self):
        return self.__switch

    def close(self):
        self.__switch = False

    @property
    def print_filter(self):
        return self.__print_filter

    @print_filter.setter
    def print_filter(self, val: list):
        self.__print_filter = [i.upper() for i in val]

    @property
    def log_filter(self):
        return self.__log_filter

    @log_filter.setter
    def log_filter(self, val: list):
        self.__log_filter = [i.upper() for i in val]
