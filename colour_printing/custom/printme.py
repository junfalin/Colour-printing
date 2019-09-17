import re
import time

from colour_printing.style import setting
from colour_printing.custom.config import Config


class PrintMeError(Exception):
    def __init__(self, message):
        super().__init__(message)


class PrintMe(object):
    def __init__(self, template: str, config_filename: str = None):
        self.term = re.findall(r'(?<=\{)[^}]*(?=\})+', template)
        if "message" not in self.term:
            raise PrintMeError('\n      template muse have {message} ! ')
        self.__term_wrap = {i: "{%s}{%s}{%s}" % (i + '0', i, i + '1') for i in self.term}
        self.template = template.format(**self.__term_wrap)
        self.box = {}
        self.default = {}

        # style config
        if not config_filename:
            config_filename = 'colour_printing_setting'
        self.config = Config(__name__, self)
        self.config.from_pyfile(config_filename)

    def set_config(self):
        for k, v in self.config.items():
            if k.endswith('_DEFAULT'):
                self.default[k[:len(k) - 8].lower()] = v
            else:
                style = self.box[k] = {}
                for t in self.term:
                    sett = setting(**v[t])
                    style.update({f'{t}0': sett[0], f'{t}1': sett[1]})

    def info(self, *args, **kwargs):
        style = self.box['INFO']
        data = {}
        for i in self.term:
            data[i] = kwargs.pop(i, self.default[i]())
        data.update(style)
        data['message'] = " ".join([str(i) for i in args])
        print(self.template.format(**data))

    def debug(self, *args, **kwargs):
        style = self.box['DEBUG']
        data = {}
        for i in self.term:
            data[i] = kwargs.pop(i, self.default[i])
        data.update(style)
        data['message'] = " ".join([str(i) for i in args])
        print(self.template.format(**data))

    def error(self, *args, **kwargs):
        style = self.box['ERROR']
        data = {}
        for i in self.term:
            data[i] = kwargs.pop(i, self.default[i])
        data.update(style)
        data['message'] = " ".join([str(i) for i in args])
        print(self.template.format(**data))

    def warn(self, *args, **kwargs):
        style = self.box['WARN']
        data = {}
        for i in self.term:
            data[i] = kwargs.pop(i, self.default[i])
        data.update(style)
        data['message'] = " ".join([str(i) for i in args])
        print(self.template.format(**data))

    def success(self, *args, **kwargs):
        style = self.box['SUCCESS']
        data = {}
        for i in self.term:
            data[i] = kwargs.pop(i, self.default[i])
        data.update(style)
        data['message'] = " ".join([str(i) for i in args])
        print(self.template.format(**data))


if __name__ == '__main__':
    log = PrintMe(template='{time}:{name}>{level}  {message}')
    log.info('sad', name='123')
    time.sleep(1)
    log.info('sad', name='123')
    time.sleep(1)
    log.info('sad', name='123')
