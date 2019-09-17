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
from datetime import datetime
from colour_printing import Mode, Fore, Back


get_time = lambda : datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')[:-3]

TIME_DEFAULT = lambda: ""

MESSAGE_DEFAULT = lambda: ""

INFO = {
    'time': {
        "fore": Fore,
        "back": Back,
        "mode": Mode,
    },

    'message': {
        "fore": Fore,
        "back": Back,
        "mode": Mode,
    },
}

ERROR = {
    'time': {
        "fore": Fore,
        "back": Back,
        "mode": Mode,
    },

    'message': {
        "fore": Fore,
        "back": Back,
        "mode": Mode,
    },
}

SUCCESS = {
    'time': {
        "fore": Fore,
        "back": Back,
        "mode": Mode,
    },

    'message': {
        "fore": Fore,
        "back": Back,
        "mode": Mode,
    },
}

DEBUG = {
    'time': {
        "fore": Fore,
        "back": Back,
        "mode": Mode,
    },

    'message': {
        "fore": Fore,
        "back": Back,
        "mode": Mode,
    },
}

WARN = {
    'time': {
        "fore": Fore,
        "back": Back,
        "mode": Mode,
    },

    'message': {
        "fore": Fore,
        "back": Back,
        "mode": Mode,
    },
}
