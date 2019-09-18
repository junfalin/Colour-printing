import errno
import os
import sys
import types


def import_string(import_name, silent=False):
    import_name = str(import_name).replace(":", ".")
    try:
        try:
            __import__(import_name)
        except ImportError:
            if "." not in import_name:
                raise
        else:
            return sys.modules[import_name]

        module_name, obj_name = import_name.rsplit(".", 1)
        module = __import__(module_name, globals(), locals(), [obj_name])
        try:
            return getattr(module, obj_name)
        except AttributeError as e:
            raise ImportError(e)

    except ImportError as e:
        raise e


string_types = (str,)
integer_types = (int,)

"""从.py文件导入"""


def level_template(level_name, term):
    res = ""
    res += "%s = {" % level_name
    for t in term:
        temp = """
    '%s': {
        "DEFAULT": %s,  # <-- Must be function name or lambda expression
        "fore": Fore.CYAN,
        "back": Back,
        "mode": Mode,
    },
""" % (t, t + "_default")
        res += temp
    res += "}\n\n"
    return res


def new_pyfile_template(level_list, term):
    res = """\"""
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
    # lib
    res += """from datetime import datetime
from colour_printing import Mode, Fore, Back\n
get_time = lambda: datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')[:-3]\n
"""
    # default
    for t in term:
        res += '''%s_default = lambda: ""\n\n''' % t
    # style
    for l in level_list:
        res += level_template(l, term)
    return res


class Config(dict):
    def __init__(self, printme, root_path):
        dict.__init__(self)
        self.printme = printme
        self.root_path = root_path
        self.config_str = ""

    def create_py_file(self, filename):
        with open(filename, 'w')as f:
            f.write(new_pyfile_template(self.printme.level_list, self.printme.term))

    def from_pyfile(self, filename, silent=False):
        file_path = os.path.join(self.root_path, filename)
        if not os.path.exists(file_path):
            self.create_py_file(file_path)
            print(f'[*]Tip>> 文件不存在,现已创建path: {file_path}')
        d = types.ModuleType('config')
        d.__file__ = filename
        try:
            with open(filename, mode='rb') as config_file:
                config = config_file.read()
                self.config_str = config.decode()
                exec(compile(config, filename, 'exec'), d.__dict__)
        except IOError as e:
            if silent and e.errno in (
                    errno.ENOENT, errno.EISDIR, errno.ENOTDIR
            ):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        self.from_object(d)
        return True

    def from_object(self, obj):
        if isinstance(obj, string_types):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)
        self.printme.set_config()  # 渲染
