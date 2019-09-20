import re
import sys
import os

from colour_printing import Fore, Back, Mode
from colour_printing.custom.config import Config

stream = sys.stdout

lk = '{'
rk = '}'
header = """\"""
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
\"""
"""


def default_template(term, template):
    # default
    res = f'TEMPLATE = "{template}"\n'
    for t in term:
        res += '''%s_default = ""\n\n''' % t
    return res


def lib_template():
    return f"""from datetime import datetime
from colour_printing import Mode, Fore, Back\n
get_time = lambda: datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')[:-3]\n
"""


def tip(msg):
    stream.write(f"[*]Tip>> {msg}")
    stream.write('\n')


def term_template(term, kw: dict):
    DEFAULT = kw[term]['DEFAULT']
    fore = kw[term]['fore']
    back = kw[term]['back']
    mode = kw[term]['mode']
    print(fore)
    if str(fore) == str(Fore):
        fore = Fore
    if str(back) == str(Back):
        back = Back
    if str(mode) == str(Mode):
        mode = Mode
    return f"""
        "{term}":{lk}
            "DEFAULT":{DEFAULT if DEFAULT else f"{term}_default"},
            "fore":{fore},
            "back":{back},
            "mode":{mode}
        {rk}
"""


def term_model(term):
    return {term: {
        "DEFAULT": f"{term}_default",
        "fore": "Fore",
        "back": "Back",
        "mode": "Mode"
    }
    }


def level_template(level_list, term_list, config):
    res = ""
    for level in level_list:
        res += level + " = {"
        for term in term_list:
            res += term_template(term, config.get(level, term_model(term)))
        res += "}\n"
    return res


def new_pyfile_template(config):
    term = config['term']
    template = config['template']
    level_list = config['level_list']
    res = header
    # lib
    res += lib_template()
    res += default_template(term, template)
    # style
    res += level_template(level_list, term, config)
    return res


def create_py_file(file_path, level_list, term, template):
    config = dict(level_list=level_list, term=term, template=template)
    if os.path.exists(file_path):
        cfg = Config()
        cfg.from_pyfile(file_path)
        config.update(cfg)

    ns = new_pyfile_template(config)
    with open(file_path, 'w')as f:
        f.write(ns)
    tip(f'创建配置模板文件完成-->  {file_path}')
    return 0


def execute(argv=None):
    if argv is None:
        argv = sys.argv
    # template
    try:
        template = str(argv[1])
    except IndexError:
        tip('Usage: cprint (template) [filename] [new_level]')
        exit(2)
    term = re.findall(r'(?<=\{)[^}]*(?=\})+', template)
    for t in term:
        if t.strip() == '':
            tip('Template have {} ! ')
            sys.exit(2)
    if "message" not in term:
        tip('template muse have {message} ! ')
        sys.exit(2)
    # filepath
    try:
        name = str(argv[2])
        name = name if name.endswith('.py') else name + '.py'
        file_path = f'{os.getcwd()}/{name}'
    except IndexError:
        file_path = f'{os.getcwd()}/colour_printing_config.py'

    try:
        new_level = argv[3:]
    except IndexError:
        new_level = []
    level_list = ['INFO', 'SUCCESS', 'WARNING', 'ERROR', 'DEBUG'] + new_level
    tip('创建配置模板文件中....')
    code = create_py_file(file_path, level_list, term, template)
    sys.exit(code)


if __name__ == "__main__":
    execute(["", "{message}"])
