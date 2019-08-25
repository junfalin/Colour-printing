from colour_printing.markers import Markers

default_info = "info"
default_warn = "warn"
default_success = "success"
default_error = "error"


class ColourPrint:
    def __init__(self):
        self.__default_setting()

    def new_flag(self, flag: str):
        setattr(self, flag, Markers(flag))
        if Markers.flag_len < len(flag):
            Markers.flag_len = len(flag)

    def __default_setting(self):
        info = Markers(default_info)
        info.set_flag_style(mode='bold', fore='blue')
        info.set_time_style(mode='invert')
        info.set_str_style(mode='bold', fore='blue')
        setattr(self, default_info, info)

        warn = Markers(default_warn)
        warn.set_flag_style(mode='bold', fore='yellow')
        warn.set_time_style(mode='invert')
        warn.set_str_style(mode='bold', fore='yellow')
        setattr(self, default_warn, warn)

        success = Markers(default_success)
        success.set_flag_style(mode='bold', fore='green')
        success.set_time_style(mode='invert')
        success.set_str_style(mode='bold', fore='green')
        setattr(self, default_success, success)

        error = Markers(default_error)
        error.set_flag_style(mode='bold', fore='red')
        error.set_time_style(mode='invert')
        error.set_str_style(mode='bold', fore='red')
        setattr(self, default_error, error)

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









