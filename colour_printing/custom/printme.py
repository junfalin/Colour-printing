import re
import os
import functools
import sys
import threading
from copy import deepcopy
from inspect import isfunction
from pprint import pprint
from queue import Queue
from colour_printing.style import setting
from colour_printing.custom.config import Config

stream = sys.stdout
level_list = []


def level_wrap(func):
    level_list.append(func.__name__.upper())

    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        level = func.__name__.upper()
        default = self.default.get(level, {})
        data = {}
        # 参数
        for i in self.term:
            w = kwargs.get(i)
            if w:
                data[i] = w
            else:
                dd = default.get(i, lambda: "")
                if isfunction(dd):
                    data[i] = dd()
                else:
                    data[i] = dd
        sep = kwargs.get('sep', " ")
        data['message'] = sep.join([str(i) for i in args])
        # record
        self.handler_record(deepcopy(data))
        # 最高优先级,对data的操作会影响后续操作的输出内容
        res = func(self, data)
        # 日志
        if level not in self.log_filter:
            msg = self.raw_template.format(**data) + "\n"
            self.queue.put(msg)
        # 打印
        if self.switch and self.Master_switch and level not in self.print_filter:
            end = kwargs.get('end', '\n')
            self.show(level, data=data, end=end)
        return res

    return wrap


class PrintMeError(Exception):
    def __init__(self, message):
        super().__init__(f"\n[*]Tip>> {message}")


class ColourPrinting(object):
    Master_switch = True

    @level_wrap
    def info(self, data):
        """最高优先级,对data的操作会影响后续操作(日志,打印)的输出内容"""

    @level_wrap
    def debug(self, data):
        """最高优先级,对data的操作会影响后续操作(日志,打印)的输出内容"""

    @level_wrap
    def error(self, data):
        """最高优先级,对data的操作会影响后续操作(日志,打印)的输出内容"""

    @level_wrap
    def warning(self, data):
        """最高优先级,对data的操作会影响后续操作(日志,打印)的输出内容"""

    @level_wrap
    def success(self, data):
        """最高优先级,对data的操作会影响后续操作(日志,打印)的输出内容"""

    def handler_record(self, record):
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


def make_default():
    r = {
        "DEFAULT": lambda: "",  # 默认值<-- Must be function name or lambda expression
        "fore": "blue",  # 前景色
        "back": "",  # 背景色
        "mode": "",  # 模式
    }
    return r


def make_level_default(term):
    r = {}
    for t in term:
        r.update({t: make_default()})
    return r


class PrintMe(ColourPrinting):

    def __init__(self, **kwargs):
        self.raw_template = ''
        self.term = []
        self.template = ''
        # store
        self.level_list = level_list
        self.box = {}
        self.default = {}
        # switch
        self.__switch = True
        self.__print_filter = []
        self.__log_filter = []
        # style config
        self.config = Config(printme=self)
        # log
        self.queue = Queue()
        self.log_handler = LogHandler(printme=self)
        for k, v in kwargs.items():
            if k in dir(self):
                raise PrintMeError(f'变量名"{k}"已被定义,请更换')
            setattr(self, k, v)

    def load_config(self):
        """获取py文件中的配置"""
        # template 检查
        template = self.config.get('TEMPLATE')
        if not template:
            raise PrintMeError(f"'{self.config.filename}' Can't find TEMPLATE = '' ")
        self.raw_template = template
        self.term = re.findall(r'(?<=\{)[^}]*(?=\})+', template)
        for t in self.term:
            if t.strip() == '':
                raise PrintMeError('Template have {} ! ')
        if "message" not in self.term:
            raise PrintMeError('Template muse have {message} ! ')
        term_wrap = {i: "{%s}{%s}{%s}" % (i + '0', i, i + '1') for i in self.term}
        self.template = template.format(**term_wrap)
        # style map
        for level in self.level_list:
            default = self.default[level] = {}
            style = self.box[level] = {}
            terms = self.config.get(level, make_level_default(self.term))  # 获取每个level里的字段
            for t in self.term:
                cfg = terms.get(t, make_default())  # 获取每个字段的default,fore,mode,back
                default.update({t: cfg.get("DEFAULT")})
                sett = setting(fore=cfg.get('fore'), back=cfg.get('back'), mode=cfg.get('mode'))
                style.update({f'{t}0': sett[0], f'{t}1': sett[1]})

    def show(self, level: str, data: dict, end: str):
        # style
        if not self.box:
            msg = self.raw_template.format(**data)
        else:
            style = self.box.get(level.upper())
            data.update(style)
            msg = self.template.format(**data)
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
            if level.upper() in self.level_list:
                for k, v in kwargs.items():
                    self.default[level.upper()].update({k: v})
        else:
            for level in self.level_list:
                for k, v in kwargs.items():
                    self.default[level.upper()].update({k: v})

    @property
    def switch(self):
        return self.__switch

    @switch.setter
    def switch(self, val):
        self.__switch = val

    @property
    def print_filter(self):
        return self.__print_filter

    @print_filter.setter
    def print_filter(self, val):
        if not isinstance(val, list):
            val = [val]
        self.__print_filter = [i.upper() for i in val]

    @property
    def log_filter(self):
        return self.__log_filter

    @log_filter.setter
    def log_filter(self, val):
        if not isinstance(val, list):
            val = [val]
        self.__log_filter = [i.upper() for i in val]
