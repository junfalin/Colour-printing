import re
import sys
import argparse
import os
from colour_printing import cword
from colour_printing.helper import check

stream = sys.stdout
parser = argparse.ArgumentParser()
parser.description = cword("***** Colour-printing ***** github@Faithforus ", fore="cyan")
parser.add_argument('-n', '--filename', default="colour_printing_config.py", help='配置文件名.py')
parser.add_argument('-t', '--template', help="信息模板,例: {}{}{message}")
parser.add_argument('-l', '--newLevel', help="新增level,配合@level_wrap使用,多个用分号隔开")


def tip(msg):
    stream.write("[*]Tip>> {msg}".format(msg=msg))
    stream.write('\n')


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
\"""\n\n"""

lk = '{'
rk = '}'
dy = "\"\""
tab = " " * 4


def lib_template(template):
    return """
from colour_printing.config import CPConfig, Term\n
from datetime import datetime\n
from colour_printing import Mode, Fore, Back\n
get_time = lambda: datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')[:-3]\n
TEMPLATE = "{template}"
CP = CPConfig(TEMPLATE)  # 从其他地方导入我
""".format(template=template)


def cls_template(level_list, terms):
    result = """
class Paper(object):"""
    for level in level_list:
        result += """\n
{tab}@CP.wrap
{tab}def {level}(self):""".format(tab=tab, level=level)
        for term in terms:
            result += """
{tab}self.{term} = Term()""".format(tab=tab * 2, term=term)
    return result


def assemble(level_list, terms, template):
    result = header
    result += lib_template(template)
    result += cls_template(level_list, terms)
    return result


def create_py_file(file_path, level_list, terms, template):
    ns = assemble(level_list, terms, template)
    with open(file_path, 'w')as f:
        f.write(ns)
    tip(f'创建配置模板文件完成-->  {file_path}')
    return 0


def template_handle(template):
    # template
    terms = re.findall(r'(?<=\{)[^}]*(?=\})+', template)
    e = check(terms)
    if e:
        tip(e)
        sys.exit(2)
    return terms


def execute():
    if len(sys.argv) <= 1:
        tip("cprint -h 查看帮助")
        sys.exit(0)
    args = parser.parse_args()
    template = args.template
    name = args.filename
    new_level = args.newLevel
    # handle
    terms = template_handle(template)
    # filepath
    name = name if name.endswith('.py') else name + '.py'
    file_path = os.getcwd() + '/' + name
    if os.path.exists(file_path):
        tip("{name}该配置文件已存在,确认要覆写吗?将配置丢失".format(name=name))
        if input("[Y/n]:") != "Y":
            tip('cancel!')
            sys.exit(0)
    # level
    level_list = ['info', 'success', 'warning', 'error', 'debug']
    if new_level:
        level_list += [l.strip() for l in new_level.split(";") if l.strip()]
    tip(u'创建配置模板文件中....')
    code = create_py_file(file_path, level_list, terms, template)
    sys.exit(code)


if __name__ == '__main__':
    execute()
