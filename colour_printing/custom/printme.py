import re
import os
import functools
import sys
import threading
from queue import Queue
from colour_printing.style import setting
from colour_printing.custom.config import Config

stream = sys.stdout
level_list = []


class Term(object):
    def __init__(self, term, **kwargs):
        for t in term:
            setattr(self, t, kwargs.get(t))


def level_wrap(func):
    level_list.append(func.__name__.upper())

    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        level = func.__name__.upper()
        default = self.default.get(level, {})
        data = {}
        # 参数
        for i in self.term:
            data[i] = kwargs.pop(i, default.get(i, lambda: "")())
        data['message'] = " ".join([str(i) for i in args])
        # record
        self.handler_record(Term(self.term, **data))
        # 日志
        if level not in self.log_filter:
            msg = self.raw_template.format(**data) + "\n"
            self.queue.put(msg)
        # 打印
        if self.switch and self.Master_switch and level not in self.print_filter:
            end = kwargs.get('end', '\n')
            self.show(level, data=data, end=end)

    return wrap


class PrintMeError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ColourPrinting(object):
    Master_switch = True

    @level_wrap
    def info(self, *args, **kwargs):
        pass

    @level_wrap
    def debug(self, *args, **kwargs):
        pass

    @level_wrap
    def error(self, *args, **kwargs):
        pass

    @level_wrap
    def warning(self, *args, **kwargs):
        pass

    @level_wrap
    def success(self, *args, **kwargs):
        pass

    def handler_record(self, record):
        pass


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
        :param log_delay: 防止线程阻塞,无消息后延时退出 ,默认2分钟
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
            while self.printme.switch and self.printme.Master_switch:
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

    def __init__(self, template: str):
        self.raw_template = template
        self.term = re.findall(r'(?<=\{)[^}]*(?=\})+', template)
        if "message" not in self.term:
            raise PrintMeError('\n [*]Tip>> template muse have {message} ! ')
        term_wrap = {i: "{%s}{%s}{%s}" % (i + '0', i, i + '1') for i in self.term}
        self.template = template.format(**term_wrap)
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

    def load_config(self):
        """获取py文件中的配置"""
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
        if not self.box:
            msg = self.raw_template.format(**data)
            stream.write(msg)
            stream.write(end)
            return
        # style
        style = self.box.get(level.upper())
        data.update(style)
        msg = self.template.format(**data)
        stream.write(msg)
        stream.write(end)

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
