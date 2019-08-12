from datetime import datetime
from colour_printing.style import STYLE, STR_STYLE, FLAG_STYLE, TIME_STYLE


class Switch:
    signal: bool = True  # 总开关
    filter: list = []  # 过滤,指定那些种类不打印


class ColourPrint:
    """
        @format：
                【flag】time string
        @usage:
            default: INFO, ERROR, WARRING, SUCCESS
                >> log=ColourPrint()

                >> log('hello')

                >> [INFO] 2019-08-11 17:38:20 hello

                >> log('hello',flag='ERROR')

                >> [ERROR] 2019-08-11 17:53:27 hello

            user: flag_name
                >> log=ColourPrint()

                >> log.set_str_style(flag=flag_name,mode='',fore='',back='')

                >> log.set_time_style(...)

                >> log.set_flag_style(...)

        @help:
                >> print(ColourPrint())

        @attr:
                self.config={
                            flag:{
                                    'str_style':(style,end),
                                    'flag_style':(style,end),
                                    'time_style':(style,end),
                            }
                }
    """

    time = lambda _: datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    template = '{flag_style0}[{flag}]{flag_style1} {time_style0}{time}{time_style1} {str_style0}{string}{str_style1}'

    def __init__(self):
        self.switch = Switch
        self.config = {}
        self.__default_setting()

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

    def set_str_style(self, flag, mode='', fore='', back=''):
        self.config.setdefault(flag, {})[STR_STYLE] = self.__setting(mode=mode, fore=fore, back=back)

    def set_time_style(self, flag, mode='', fore='', back=''):
        self.config.setdefault(flag, {})[TIME_STYLE] = self.__setting(mode=mode, fore=fore, back=back)

    def set_flag_style(self, flag, mode='', fore='', back=''):
        self.config.setdefault(flag, {})[FLAG_STYLE] = self.__setting(mode=mode, fore=fore, back=back)

    def __default_setting(self):
        self.config.setdefault('INFO', {})[STR_STYLE] = self.__setting(mode='bold', fore='blue')
        self.config.setdefault('INFO', {})[TIME_STYLE] = self.__setting(mode='invert')
        self.config.setdefault('INFO', {})[FLAG_STYLE] = self.__setting(mode='bold', fore='blue')

        self.config.setdefault('WARRING', {})[STR_STYLE] = self.__setting(mode='bold', fore='yellow')
        self.config.setdefault('WARRING', {})[TIME_STYLE] = self.__setting(mode='invert')
        self.config.setdefault('WARRING', {})[FLAG_STYLE] = self.__setting(mode='bold', fore='yellow')

        self.config.setdefault('SUCCESS', {})[STR_STYLE] = self.__setting(mode='bold', fore='green')
        self.config.setdefault('SUCCESS', {})[TIME_STYLE] = self.__setting(mode='invert')
        self.config.setdefault('SUCCESS', {})[FLAG_STYLE] = self.__setting(mode='bold', fore='green')

        self.config.setdefault('ERROR', {})[STR_STYLE] = self.__setting(mode='bold', fore='red')
        self.config.setdefault('ERROR', {})[TIME_STYLE] = self.__setting(mode='invert')
        self.config.setdefault('ERROR', {})[FLAG_STYLE] = self.__setting(mode='bold', fore='red')

    def __user_setting(self, flag):
        style = self.config.get(flag)
        if not style:
            raise KeyError('未知flag<{}>，自定义set_str_style(),set_time_style()...'.format(flag))
        str_style = style.get(STR_STYLE, self.__setting())
        time_style = style.get(TIME_STYLE, self.__setting())
        flag_style = style.get(FLAG_STYLE, self.__setting())
        return self.template.format(flag_style0=flag_style[0],
                                    flag=flag,
                                    flag_style1=flag_style[1],
                                    time_style0=time_style[0],
                                    time=self.time(),
                                    time_style1=time_style[1],
                                    str_style0=str_style[0],
                                    string='{}',
                                    str_style1=str_style[1])

    def __call__(self, *args, **kwargs):
        flag = kwargs.pop('flag', 'INFO')
        if not self.switch.signal or flag in self.switch.filter:
            return
        template = self.__user_setting(flag).replace('{}', len(args) * '{} ')
        print(template.format(*args))

    def __str__(self):
        return """{
            'fore':
                {  # 前景色
                    'black': 30,  # 黑色
                    'red': 31,  # 红色
                    'green': 32,  # 绿色
                    'yellow': 33,  # 黄色
                    'blue': 34,  # 蓝色
                    'purple': 35,  # 紫红色
                    'cyan': 36,  # 青蓝色
                    'white': 37,  # 白色
                },

            'back':
                {  # 背景
                    'black': 40,  # 黑色
                    'red': 41,  # 红色
                    'green': 42,  # 绿色
                    'yellow': 43,  # 黄色
                    'blue': 44,  # 蓝色
                    'purple': 45,  # 紫红色
                    'cyan': 46,  # 青蓝色
                    'white': 47,  # 白色
                },

            'mode':
                {  # 显示模式
                    'mormal': 0,  # 终端默认设置
                    'bold': 1,  # 高亮显示
                    'underline': 4,  # 使用下划线
                    'blink': 5,  # 闪烁
                    'invert': 7,  # 反白显示
                    'hide': 8,  # 不可见
                },

        }"""
