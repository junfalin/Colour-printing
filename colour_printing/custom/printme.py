import re
import os
import functools
import threading
from queue import Queue
from colour_printing.style import setting
from colour_printing.custom.config import Config
import time

INFO = 'INFO'
DEBUG = 'DEBUG'
SUCCESS = 'SUCCESS'
ERROR = 'ERROR'
WARN = 'WARN'
tip = "[*]Tip>> {}"


class PrintMeError(Exception):
    def __init__(self, message):
        super().__init__(message)


def level_wrap(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        if self.switch is False or self.Master_switch is False:
            return
        if func.__name__ in self.filter:
            return
        return func(self, *args, **kwargs)

    return wrap


def log_to(printme, log_name: str):
    count = 5
    path = os.path.join(printme.root_path, log_name)
    print(f'[*]Tip>> 日志文件path: {path}')
    with open(path, 'a+') as f:
        while printme.switch and printme.Master_switch:
            if count < 0:
                print(end='\r')
                print('[*]Tip>> 日志输出关闭')
                break
            if printme.queue.empty():
                print(end='\r')
                print(f'[*]Tip>> 等待输出信息 {count} s', end='')
                time.sleep(1)
                count -= 1
                continue
            f.write(printme.queue.get())
            f.flush()


class PrintMe(object):
    level_list = [INFO, ERROR, SUCCESS, DEBUG, WARN]
    Master_switch = True

    def __init__(self, template: str, config_filename: str = 'colour_printing_config.py', log_output: bool = False,
                 log_name: str = 'colour_printing_log.log'):
        self.raw_template = template
        self.term = re.findall(r'(?<=\{)[^}]*(?=\})+', template)
        if "message" not in self.term:
            raise PrintMeError('\n [*]Tip>> template muse have {message} ! ')
        term_wrap = {i: "{%s}{%s}{%s}" % (i + '0', i, i + '1') for i in self.term}
        self.template = template.format(**term_wrap)
        # store
        self.box = {}
        self.default = {}
        # switch
        self.switch = True
        self.filter = []
        # style config
        self.config_filename = config_filename if config_filename.endswith('.py') else config_filename + '.py'
        self.root_path = os.getcwd()
        self.config = Config(printme=self, root_path=self.root_path)
        self.config.from_pyfile(self.config_filename)
        # log
        self.log_output = log_output
        if log_output:
            self.queue = Queue(-1)
            t = threading.Thread(target=log_to, args=(self, log_name))
            t.start()

    def set_config(self):
        for k, v in self.config.items():
            if k not in self.level_list:
                continue
            default = self.default[k] = {}
            style = self.box[k] = {}
            for t in self.term:
                default.update({t: v[t].pop("DEFAULT", lambda: "")})
                sett = setting(**v[t])
                style.update({f'{t}0': sett[0], f'{t}1': sett[1]})

    def show(self, level, *args, **kwargs):
        style = self.box[level.upper()]
        default = self.default[level.upper()]
        data = {}
        for i in self.term:
            data[i] = kwargs.pop(i, default[i]())
        data['message'] = " ".join([str(i) for i in args])
        if self.log_output:
            msg = self.raw_template.format(**data) + "\n"
            self.queue.put(msg)
        data.update(style)
        data['message'] = " ".join([str(i) for i in args])
        print(self.template.format(**data), sep=kwargs.get('sep', " "), end=kwargs.get('end', "\n"),
              file=kwargs.get('file', None))

    @level_wrap
    def info(self, *args, **kwargs):
        self.show(INFO, *args, **kwargs)

    @level_wrap
    def debug(self, *args, **kwargs):
        self.show(DEBUG, *args, **kwargs)

    @level_wrap
    def error(self, *args, **kwargs):
        self.show(ERROR, *args, **kwargs)

    @level_wrap
    def warn(self, *args, **kwargs):
        self.show(WARN, *args, **kwargs)

    @level_wrap
    def success(self, *args, **kwargs):
        self.show(SUCCESS, *args, **kwargs)
