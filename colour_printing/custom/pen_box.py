from colour_printing.custom.markers import Markers

default_info = "info"
default_warn = "warn"
default_success = "success"
default_error = "error"


class ColourPrint:
    Markers = Markers

    def __init__(self):
        self.__default_setting()

    def __init_subclass__(cls, **kwargs):
        cls.custom(cls)

    def custom(self):
        e = '''
        Custom styles need to override this method ! 
        for example : 
            self.debug = self.Markers('debug').flag_style(mode="bold").time_style(...)'''
        raise NotImplementedError(e)

    def __default_setting(self):
        self.info = Markers(default_info) \
            .flag_style(mode='bold', fore='blue').time_style(mode='invert').message_style(mode='bold', fore='blue')

        self.warn = Markers(default_warn) \
            .flag_style(mode='bold', fore='yellow').time_style(mode='invert').message_style(mode='bold', fore='yellow')

        self.success = Markers(default_success) \
            .flag_style(mode='bold', fore='green').time_style(mode='invert').message_style(mode='bold', fore='green')

        self.error = Markers(default_error) \
            .flag_style(mode='bold', fore='red').time_style(mode='invert').message_style(mode='bold', fore='red')

    def __str__(self):
        return """
                @'fore': # 前景色
                        'black': 黑色
                        'red': 红色
                        'green': 绿色
                        'yellow': 黄色
                        'blue':  蓝色
                        'purple':  紫红色
                        'cyan':  青蓝色
                        'white':  白色
                @'back':# 背景
                        'black':  黑色
                        'red':  红色
                        'green': 绿色
                        'yellow':  黄色
                        'blue': 蓝色
                        'purple':  紫红色
                        'cyan':  青蓝色
                        'white': 白色
                @'mode':# 显示模式
                        'normal': 终端默认设置
                        'bold':  高亮显示
                        'underline':  使用下划线
                        'blink': 闪烁
                        'invert': 反白显示
                        'hide': 不可见
            """


log = ColourPrint()
