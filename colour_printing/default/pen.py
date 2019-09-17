from datetime import datetime
from colour_printing.style import setting
from colour_printing.switch import Switch

MESSAGE_STYLE = 'message_style'
FLAG_STYLE = 'flag_style'
TIME_STYLE = 'time_style'


class Pen(object):
    __get_time = lambda _: datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')[:-3]
    __flag_len = 7

    def __init__(self, flag_name: str):
        self.__flag_name = flag_name.upper()
        self.__config = {}
        self.__cal_flag_len()

    def __cal_flag_len(self):
        if Pen.__flag_len < len(self.__flag_name):
            Pen.__flag_len = len(self.__flag_name)

    def message_style(self, mode='', fore='', back=''):
        self.__config[MESSAGE_STYLE] = setting(mode=mode, fore=fore, back=back)
        return self

    def time_style(self, mode='', fore='', back=''):
        self.__config[TIME_STYLE] = setting(mode=mode, fore=fore, back=back)
        return self

    def flag_style(self, mode='', fore='', back=''):
        self.__config[FLAG_STYLE] = setting(mode=mode, fore=fore, back=back)
        return self

    def __user_setting(self):
        message_style = self.__config.get(MESSAGE_STYLE, setting())
        time_style = self.__config.get(TIME_STYLE, setting())
        flag_style = self.__config.get(FLAG_STYLE, setting())
        flag = '{0}{1}{2}'.format(flag_style[0], f"{self.__flag_name.center(self.__flag_len, ' ')}", flag_style[1])
        time = '{0}{1}{2}'.format(time_style[0], self.__get_time(), time_style[1])
        return flag, time, message_style

    def __call__(self, *args, **kwargs):
        if not Switch.signal or self.__flag_name.lower() in Switch.filter or self.__flag_name in Switch.filter:
            return
        flag, time, message_style = self.__user_setting()
        str_temp = []
        for s in args:
            str_temp.append(f'{message_style[0]}{s}{message_style[1]}')
        print(time, flag, *str_temp, **kwargs)
