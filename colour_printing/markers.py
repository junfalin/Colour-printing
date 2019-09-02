from datetime import datetime
from colour_printing.style import setting
from colour_printing.switch import Switch

MESSAGE_STYLE = 'message_style'
FLAG_STYLE = 'flag_style'
TIME_STYLE = 'time_style'


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

    def message_style(self, mode='', fore='', back=''):
        self.__config[MESSAGE_STYLE] = setting(mode=mode, fore=fore, back=back)
        return self

    def time_style(self, mode='', fore='', back=''):
        if mode == 'hide':
            self.__hide.append('time')
        else:
            self.__config[TIME_STYLE] = setting(mode=mode, fore=fore, back=back)
        return self

    def flag_style(self, mode='', fore='', back=''):
        if mode == 'hide':
            self.__hide.append('flag')
        else:
            self.__config[FLAG_STYLE] = setting(mode=mode, fore=fore, back=back)
        return self

    def __user_setting(self):
        message_style = self.__config.get(MESSAGE_STYLE, setting())
        time_style = self.__config.get(TIME_STYLE, setting())
        flag_style = self.__config.get(FLAG_STYLE, setting())
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
