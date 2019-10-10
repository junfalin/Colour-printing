"""
#                     *Colour-printing Reference*
#########################################################################################
#   @'fore': # 前景色         @'back':# 背景              @'mode':# 显示模式               # 
#            'black': 黑色            'black':  黑色              'normal': 终端默认设置   # 
#            'red': 红色              'red':  红色                'bold':  高亮显示        # 
#            'green': 绿色            'green': 绿色               'underline':  使用下划线 #
#            'yellow': 黄色           'yellow': 黄色              'blink': 闪烁           # 
#            'blue':  蓝色            'blue':  蓝色               'invert': 反白显示       #    
#            'purple':  紫红色        'purple':  紫红色            'hide': 不可见          #    
#            'cyan':  青蓝色          'cyan':  青蓝色                                     #
#            'white':  白色           'white':  白色                                     #
#########################################################################################
"""

from colour_printing.config import CPConfig, Term

from datetime import datetime
from colour_printing import Mode, Fore, Back

get_time = lambda: datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S.%f")[:-3]
fill = 7

TEMPLATE = "{time} {flag} {message}"
CP = CPConfig(TEMPLATE)


class Paper(object):
    @CP.wrap
    def info(self):
        self.time = Term(default=get_time, fore=Fore.CYAN)
        self.flag = Term(default="INFO".center(fill, "-"), fore=Fore.BLUE, mode=Mode.INVERT)
        self.message = Term(fore=Fore.BLUE)

    @CP.wrap
    def error(self):
        self.time = Term(default=get_time, fore=Fore.CYAN)
        self.flag = Term(default="ERROR".center(fill, "-"), fore=Fore.RED, mode=Mode.INVERT)
        self.message = Term(fore=Fore.RED)

    @CP.wrap
    def success(self):
        self.time = Term(default=get_time, fore=Fore.CYAN)
        self.flag = Term(default="SUCCESS".center(fill, "-"), fore=Fore.GREEN, mode=Mode.INVERT)
        self.message = Term(fore=Fore.GREEN)

    @CP.wrap
    def debug(self):
        self.time = Term(default=get_time, fore=Fore.CYAN)
        self.flag = Term(default="DEBUG".center(fill, "-"), fore=Fore.PURPLE, mode=Mode.INVERT)
        self.message = Term(fore=Fore.PURPLE)

    @CP.wrap
    def warning(self):
        self.time = Term(default=get_time, fore=Fore.CYAN)
        self.flag = Term(default="WARNING".center(fill, "-"), fore=Fore.YELLOW, mode=Mode.INVERT)
        self.message = Term(fore=Fore.YELLOW)
