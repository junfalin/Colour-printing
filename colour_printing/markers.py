from datetime import datetime
from colour_printing.style import STYLE, STR_STYLE, FLAG_STYLE, TIME_STYLE
from colour_printing.switch import Switch

class Markers:
    time = lambda _: datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    template = '{flag_style0}[{flag}]{flag_style1} {time_style0}{time}{time_style1} {str_style0}{string}{str_style1}'
    flag_len = 7

    def __init__(self, flag: str):
        self.flag = flag.upper()
        self.config = {}

    @classmethod
    def __setting(cls, mode='', fore='', back=''):
        """
        linxu:转义序列以ESC开头，即ASCII码下的\033
                   格式: \033[显示方式;前景色;背景色m
        """
        mode = '%s' % STYLE['mode'][mode] if STYLE['mode'].get(mode) else ''

        fore = '%s' % STYLE['fore'][fore] if STYLE['fore'].get(fore) else ''

        back = '%s' % STYLE['back'][back] if STYLE['back'].get(back) else ''

        style = ';'.join([s for s in [mode, fore, back] if s])

        style = '\033[%sm' % style if style else ''

        end = '\033[%sm' % STYLE['default']['end'] if style else ''

        return style, end

    def set_str_style(self, mode='', fore='', back=''):
        self.config[STR_STYLE] = self.__setting(mode=mode, fore=fore, back=back)

    def set_time_style(self, mode='', fore='', back=''):
        self.config[TIME_STYLE] = self.__setting(mode=mode, fore=fore, back=back)

    def set_flag_style(self, mode='', fore='', back=''):
        self.config[FLAG_STYLE] = self.__setting(mode=mode, fore=fore, back=back)

    def __user_setting(self):
        str_style = self.config.get(STR_STYLE, self.__setting())
        time_style = self.config.get(TIME_STYLE, self.__setting())
        flag_style = self.config.get(FLAG_STYLE, self.__setting())
        return self.template.format(flag_style0=flag_style[0],
                                    flag=self.flag.center(self.flag_len, '-'),
                                    flag_style1=flag_style[1],
                                    time_style0=time_style[0],
                                    time=self.time(),
                                    time_style1=time_style[1],
                                    str_style0=str_style[0],
                                    string='{}',
                                    str_style1=str_style[1])

    def __call__(self, *args):
        if not Switch.signal or self.flag.lower() in Switch.filter or \
                self.flag in Switch.filter:
            return
        template = self.__user_setting().replace('{}', len(args) * '{} ')
        print(template.format(*args))
