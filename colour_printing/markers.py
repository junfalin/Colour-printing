from datetime import datetime
from colour_printing.style import STYLE, MESSAGE_STYLE, FLAG_STYLE, TIME_STYLE
from colour_printing.switch import Switch


class Markers:
    __get_time = lambda _: datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    __template = '{flag_style0}{flag}{flag_style1}{time_style0}{time}{time_style1}' \
                 '{message_style0}{string}{message_style1}'
    __flag_len = 7

    def __init__(self, flag_name: str):
        self.__flag_name = flag_name.upper()
        self.__config = {}
        self.__cal_flag_len()
        self.__hide = []

    def __cal_flag_len(self):
        if Markers.__flag_len < len(self.__flag_name):
            Markers.__flag_len = len(self.__flag_name)

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

    def message_style(self, mode='', fore='', back=''):
        self.__config[MESSAGE_STYLE] = self.__setting(mode=mode, fore=fore, back=back)
        return self

    def time_style(self, mode='', fore='', back=''):
        if mode == 'hide':
            self.__hide.append('time')
        else:
            self.__config[TIME_STYLE] = self.__setting(mode=mode, fore=fore, back=back)
        return self

    def flag_style(self, mode='', fore='', back=''):
        if mode == 'hide':
            self.__hide.append('flag')
        else:
            self.__config[FLAG_STYLE] = self.__setting(mode=mode, fore=fore, back=back)
        return self

    def __user_setting(self):
        message_style = self.__config.get(MESSAGE_STYLE, self.__setting())
        time_style = self.__config.get(TIME_STYLE, self.__setting())
        flag_style = self.__config.get(FLAG_STYLE, self.__setting())
        return self.__template.format(flag_style0=flag_style[0],
                                      flag=f"[{self.__flag_name.center(self.__flag_len, '-')}] "
                                      if 'flag' not in self.__hide else "",
                                      flag_style1=flag_style[1],
                                      time_style0=time_style[0],
                                      time=f"{self.__get_time()} " if 'time' not in self.__hide else '',
                                      time_style1=time_style[1],
                                      message_style0=message_style[0],
                                      string='{}',
                                      message_style1=message_style[1])

    def __call__(self, *args):
        if not Switch.signal or self.__flag_name.lower() in Switch.filter or \
                self.__flag_name in Switch.filter:
            return
        template = self.__user_setting().replace('{}', len(args) * '{} ')
        print(template.format(*args))
