import re
from datetime import datetime
import logging

from colour_printing.style import setting
from colour_printing.config import Config


class PrintMe(object):
    __get_time = lambda _: datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')[:-3]

    def __init__(self, template: str):
        self.term = re.findall(r'(?<=\{)[^}]*(?=\})+', template)
        self.__term_wrap = {i: "{%s}{%s}{%s}" % (i + '0', i, i + '1') for i in self.term}
        self.template = template.format(**self.__term_wrap)
        self.cfg = {}
        self.default = {}

        self.config = Config(__name__, self.term).config

    def load_config(self):
        for k, v in self.config.items():
            sett = setting(**v['style'])
            self.cfg.update({f'{k}0': sett[0], f'{k}1': sett[1]})
            self.default[k] = v['default']

    def log(self, *args, **kwargs):
        data = {}
        for i in self.term:
            data[i] = kwargs.pop(i, self.default[i])
        data.update(self.cfg)
        data['msg'] = " ".join([str(i) for i in args])
        print(self.template.format(**data))


if __name__ == '__main__':
    log = PrintMe(template='{time}:{name}>{level}  {msg}')
    log.config(time={"default": "2019-09-17 08:40:51.341", 'style': {'back': 'red', 'fore': '', 'mode': ''}},
               name={"default": "jack", 'style': {'back': 'red', 'fore': '', 'mode': ''}},
               level={"default": "info", 'style': {'back': 'red', 'fore': '', 'mode': ''}},
               msg={"default": "hello", 'style': {'back': 'red', 'fore': '', 'mode': ''}}, )
    log.log('123', 123)
    log.log('1232', 123)
    log.log('123233', 123)
    log.log('1213', 123)
