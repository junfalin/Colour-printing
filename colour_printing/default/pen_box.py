from colour_printing.default.pen import Pen
from colour_printing.style import Mode, Fore

default_info = "info"
default_warn = "warn"
default_success = "success"
default_error = "error"
default_debug = "debug"


class ColourPrint(object):
    Pen = Pen

    def __init__(self):
        self.__default_setting()

    def __init_subclass__(cls, **kwargs):
        cls.custom(cls)

    def custom(self):
        e = '''
        Custom styles need to override this method ! 
        #for example : 
        #    self.debug = self.Markers('debug').flag_style(mode=Mode.BOLD).time_style(...'''
        raise NotImplementedError(e)

    def __default_setting(self):
        self.info = Pen(default_info) \
            .flag_style(mode=Mode.INVERT, fore=Fore.BLUE).time_style(fore=Fore.CYAN).message_style(
            fore=Fore.BLUE)

        self.warn = Pen(default_warn) \
            .flag_style(mode=Mode.INVERT, fore=Fore.YELLOW).time_style(fore=Fore.CYAN).message_style(
            fore=Fore.YELLOW)

        self.success = Pen(default_success) \
            .flag_style(mode=Mode.INVERT, fore=Fore.GREEN).time_style(fore=Fore.CYAN).message_style(
            fore=Fore.GREEN)

        self.error = Pen(default_error) \
            .flag_style(mode=Mode.INVERT, fore=Fore.RED).time_style(fore=Fore.CYAN).message_style(
            fore=Fore.RED)

        self.debug = Pen(default_debug) \
            .flag_style(mode=Mode.INVERT, fore=Fore.PURPLE).time_style(fore=Fore.CYAN).message_style(
            fore=Fore.PURPLE)

    def __str__(self):
        return """
@'fore': # 前景色         @'back':# 背景              @'mode':# 显示模式
        'black': 黑色            'black':  黑色              'normal': 终端默认设置
        'red': 红色              'red':  红色                'bold':  高亮显示
        'green': 绿色            'green': 绿色               'underline':  使用下划线
        'yellow': 黄色           'yellow': 黄色              'blink': 闪烁
        'blue':  蓝色            'blue':  蓝色               'invert': 反白显示
        'purple':  紫红色        'purple':  紫红色            'hide': 不可见
        'cyan':  青蓝色          'cyan':  青蓝色
        'white':  白色           'white':  白色
            """


log = ColourPrint()
