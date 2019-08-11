from datetime import datetime
from printing.style import STYLE, STR_STYLE, CATEGORY_STYLE, TIME_STYLE


class Switch:
    signal = True  # 总开关
    category_filter = []  # 过滤,指定那些种类不打印


class ColourPrint:
    time = lambda _: datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    template = '{category_style0}[{category}]{category_style1} {time_style0}{time}{time_style1} {str_style0}{string}{str_style1}'

    def __init__(self):
        """
        self.config={
                    category:{
                            'str_style':(style,end),
                            'category_style':(style,end),
                            'time_style':(style,end),
                    }
        }
        """
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

    def set_str_style(self, category, mode='', fore='', back=''):
        self.config.setdefault(category, {})[STR_STYLE] = self.__setting(mode=mode, fore=fore, back=back)

    def set_time_style(self, category, mode='', fore='', back=''):
        self.config.setdefault(category, {})[TIME_STYLE] = self.__setting(mode=mode, fore=fore, back=back)

    def set_category_style(self, category, mode='', fore='', back=''):
        self.config.setdefault(category, {})[CATEGORY_STYLE] = self.__setting(mode=mode, fore=fore, back=back)

    def __default_setting(self):
        self.config.setdefault('INFO', {})[STR_STYLE] = self.__setting(mode='bold', fore='blue')
        self.config.setdefault('INFO', {})[TIME_STYLE] = self.__setting(mode='invert')
        self.config.setdefault('INFO', {})[CATEGORY_STYLE] = self.__setting(mode='bold', fore='blue')

        self.config.setdefault('WARRING', {})[STR_STYLE] = self.__setting(mode='bold', fore='yellow')
        self.config.setdefault('WARRING', {})[TIME_STYLE] = self.__setting(mode='invert')
        self.config.setdefault('WARRING', {})[CATEGORY_STYLE] = self.__setting(mode='bold', fore='yellow')

        self.config.setdefault('SUCCESS', {})[STR_STYLE] = self.__setting(mode='bold', fore='green')
        self.config.setdefault('SUCCESS', {})[TIME_STYLE] = self.__setting(mode='invert')
        self.config.setdefault('SUCCESS', {})[CATEGORY_STYLE] = self.__setting(mode='bold', fore='green')

        self.config.setdefault('ERROR', {})[STR_STYLE] = self.__setting(mode='bold', fore='red')
        self.config.setdefault('ERROR', {})[TIME_STYLE] = self.__setting(mode='invert')
        self.config.setdefault('ERROR', {})[CATEGORY_STYLE] = self.__setting(mode='bold', fore='red')

    def __user_setting(self, category):
        style = self.config.get(category)
        if not style:
            raise KeyError('还未设定此类型，请set_str_style,set_time_style')
        str_style = style.pop(STR_STYLE, self.__setting())
        time_style = style.pop(TIME_STYLE, self.__setting())
        category_style = style.pop(CATEGORY_STYLE, self.__setting())
        return self.template.format(category_style0=category_style[0],
                                    category=category,
                                    category_style1=category_style[1],
                                    time_style0=time_style[0],
                                    time=self.time(),
                                    time_style1=time_style[1],
                                    str_style0=str_style[0],
                                    string='{}',
                                    str_style1=str_style[1])

    def __call__(self, data, category='INFO'):
        if not self.switch.signal or category in self.switch.category_filter:
            return
        template = self.__user_setting(category)
        print(template.format(data))
