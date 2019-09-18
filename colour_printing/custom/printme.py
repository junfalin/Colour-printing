import re
import os
import functools
from colour_printing.style import setting
from colour_printing.custom.config import Config


class PrintMeError(Exception):
    def __init__(self, message):
        super().__init__(message)


def level_wrap(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        if self.switch is False:
            return
        if func.__name__ in self.filter:
            return
        return func(self, *args, **kwargs)

    return wrap


class PrintMe(object):
    def __init__(self, template: str, config_filename: str = None):
        self.term = re.findall(r'(?<=\{)[^}]*(?=\})+', template)
        if "message" not in self.term:
            raise PrintMeError('\n [*]Tip:: template muse have {message} ! ')
        self.__term_wrap = {i: "{%s}{%s}{%s}" % (i + '0', i, i + '1') for i in self.term}
        self.template = template.format(**self.__term_wrap)
        self.box = {}
        self.default = {}
        # switch
        self.switch = True
        self.filter = []
        # style config
        if not config_filename:
            config_filename = 'colour_printing_config'
        self.config = Config(self, os.getcwd())
        self.config.from_pyfile(config_filename)

    def set_config(self):
        for k, v in self.config.items():
            default = self.default[k] = {}
            style = self.box[k] = {}
            for t in self.term:
                default.update({t: v[t].pop("DEFAULT", "")})
                sett = setting(**v[t])
                style.update({f'{t}0': sett[0], f'{t}1': sett[1]})


    def show(self, level, *args, **kwargs):
        style = self.box[level]
        default = self.default[level]
        data = {}
        for i in self.term:
            data[i] = kwargs.pop(i, default[i]())
        data.update(style)
        data['message'] = " ".join([str(i) for i in args])
        print(self.template.format(**data), sep=kwargs.get('sep', " "), end=kwargs.get('end', "\n"),
              file=kwargs.get('file', None))

    @level_wrap
    def info(self, *args, **kwargs):
        self.show('INFO', *args, **kwargs)

    @level_wrap
    def debug(self, *args, **kwargs):
        self.show('DEBUG', *args, **kwargs)

    @level_wrap
    def error(self, *args, **kwargs):
        self.show('ERROR', *args, **kwargs)

    @level_wrap
    def warn(self, *args, **kwargs):
        self.show('WARN', *args, **kwargs)

    @level_wrap
    def success(self, *args, **kwargs):
        self.show('SUCCESS', *args, **kwargs)
