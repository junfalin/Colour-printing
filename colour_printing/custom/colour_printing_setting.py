
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

get_time = lambda _: datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')[:-3]

TIME_DEFAULT = lambda: ""

NAME_DEFAULT = lambda: ""

LEVEL_DEFAULT = lambda: ""

MESSAGE_DEFAULT = lambda: ""

INFO = {
    'time': {
        "fore": "red",
        "back": "",
        "mode": "",
    },

    'name': {
        "fore": "red",
        "back": "",
        "mode": "",
    },

    'level': {
        "fore": "red",
        "back": "",
        "mode": "",
    },

    'message': {
        "fore": "red",
        "back": "",
        "mode": "",
    },
}

ERROR = {
    'time': {
        "fore": "red",
        "back": "",
        "mode": "",
    },

    'name': {
        "fore": "red",
        "back": "",
        "mode": "",
    },

    'level': {
        "fore": "red",
        "back": "",
        "mode": "",
    },

    'message': {
        "fore": "red",
        "back": "",
        "mode": "",
    },
}

SUCCESS = {
    'time': {
        "fore": "red",
        "back": "",
        "mode": "",
    },

    'name': {
        "fore": "red",
        "back": "",
        "mode": "",
    },

    'level': {
        "fore": "red",
        "back": "",
        "mode": "",
    },

    'message': {
        "fore": "red",
        "back": "",
        "mode": "",
    },
}

DEBUG = {
    'time': {
        "fore": "red",
        "back": "",
        "mode": "",
    },

    'name': {
        "fore": "red",
        "back": "",
        "mode": "",
    },

    'level': {
        "fore": "red",
        "back": "",
        "mode": "",
    },

    'message': {
        "fore": "red",
        "back": "",
        "mode": "",
    },
}

WARN = {
    'time': {
        "fore": "red",
        "back": "",
        "mode": "",
    },

    'name': {
        "fore": "red",
        "back": "",
        "mode": "",
    },

    'level': {
        "fore": "red",
        "back": "",
        "mode": "",
    },

    'message': {
        "fore": "red",
        "back": "",
        "mode": "",
    },
}

