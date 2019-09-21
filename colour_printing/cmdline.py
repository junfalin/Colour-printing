import re
import sys
import argparse
import os
from colour_printing.custom.config import Config
from colour_printing import cword

stream = sys.stdout
parser = argparse.ArgumentParser()
parser.description = cword("***** Colour-printing ***** github@Faithforus ", fore="cyan")
parser.add_argument('-n', '--filename', default="colour_printing_config.py", help=u'配置文件名')
parser.add_argument('-t', '--template', help="输出信息模板")
parser.add_argument('-l', '--newLevel', help="新增level")

lk = '{'
rk = '}'
dy = "\"\""

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
    res = f'TEMPLATE = "{template}"\n\n'
    for t in term:
        res += '''%s_default = ""\n''' % t
    return res


def lib_template():
    return f"""
from datetime import datetime
from colour_printing import Mode, Fore, Back\n
get_time = lambda: datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')[:-3]\n
"""


def tip(msg, colour='blue'):
    stream.write(cword(f"[*]Tip>> {msg}", fore=colour))
    stream.write('\n')


def term_template(term, kw: dict):
    style = kw.get(term, term_model(term))
    DEFAULT = style.get('DEFAULT')
    fore = style.get('fore')
    back = style.get('back')
    mode = style.get('mode')
    return f"""
        "{term}": {lk}
            "DEFAULT": {f'"{DEFAULT}"' if DEFAULT and isinstance(DEFAULT, str) else f"{term}_default"},
            "fore": {f'"{fore}"' if fore else dy},
            "back": {f'"{back}"' if back else dy},
            "mode": {f'"{mode}"' if mode else dy}
        {rk},
"""


def term_model(term):
    return {term: {
        "DEFAULT": "",
        "fore": "",
        "back": "",
        "mode": ""
    }}


def level_template(level_list, term_list, config):
    res = "\n"
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
        confirm = input(cword(f"[*]Tip>> 该配置文件已存在,确认要覆写吗?\n"
                              f"(如果覆写则会丢失部分配置)[Y/n]:", fore='yellow'))
        if confirm != "Y":
            tip('已取消')
            sys.exit(0)
        cfg = Config()
        cfg.from_pyfile(file_path)
        config.update(cfg)
    ns = new_pyfile_template(config)
    with open(file_path, 'w')as f:
        f.write(ns)
    tip(f'创建配置模板文件完成-->  {file_path}', colour='green')
    return 0


def execute():
    args = parser.parse_args()
    template = args.template
    name = args.filename
    new_level = args.newLevel
    # template
    if template:
        term = re.findall(r'(?<=\{)[^}]*(?=\})+', template)
        if "message" not in term:
            tip('template muse have {message} ! ', colour='red')
            sys.exit(2)
        for t in term:
            if t.strip() == '':
                tip(f'Unknown {{}} in " {template} " ', colour='red')
                sys.exit(2)
    # filepath
    name = name if name.endswith('.py') else name + '.py'
    file_path = f'{os.getcwd()}/{name}'
    # level
    level_list = ['INFO', 'SUCCESS', 'WARNING', 'ERROR', 'DEBUG']
    if new_level:
        level_list += new_level.split(" ")
    tip(u'创建配置模板文件中....')
    code = create_py_file(file_path, level_list, term, template)
    sys.exit(code)
