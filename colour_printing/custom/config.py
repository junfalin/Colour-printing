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
"""从.config文件导入"""  # 暂时搁置
# def new_config_template(term):
#     res = """#                     *Colour-printing Reference*
# #########################################################################################
# #   @'fore': # 前景色         @'back':# 背景              @'mode':# 显示模式               #
# #            'black': 黑色            'black':  黑色              'normal': 终端默认设置   #
# #            'red': 红色              'red':  红色                'bold':  高亮显示        #
# #            'green': 绿色            'green': 绿色               'underline':  使用下划线 #
# #            'yellow': 黄色           'yellow': 黄色              'blink': 闪烁           #
# #            'blue':  蓝色            'blue':  蓝色               'invert': 反白显示       #
# #            'purple':  紫红色        'purple':  紫红色            'hide': 不可见          #
# #            'cyan':  青蓝色          'cyan':  青蓝色                                     #
# #            'white':  白色           'white':  白色                                     #
# #########################################################################################
# """
#     level_list = ['info', 'error', 'success', 'debug', 'warn']
#     for t in term:
#         for l in level_list:
#             temp = f"""
# [{t}_{l}]
# level = {l}
# default =
# back =
# fore =
# mode =
# """
#             res += temp
#     return res

"""从.py文件导入"""


def new_pyfile_template(term):
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
    level_list = ['info', 'error', 'success', 'debug', 'warn']
    # lib
    res += """from datetime import datetime\nfrom colour_printing import Mode, Fore, Back
\n\nget_time = lambda : datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')[:-3]\n\n"""
    # style
    for l in level_list:
        res += "%s = {" % l.upper()
        for t in term:
            temp = """
    '%s': {
        "DEFAULT": lambda: "",
        "fore": Fore.CYAN,
        "back": Back,
        "mode": Mode,
    },
""" % t
            res += temp
        res += "}\n\n"
    return res


class Config(dict):
    def __init__(self, printme, root_path):
        dict.__init__(self)
        self.printme = printme
        self.root_path = root_path

    #     self.config = ConfigParser()

    # def create_config_file(self, term):
    #     with open(self.root_path + '/colour_printing.config', 'w')as f:
    #         f.write(new_config_template(term))

    def create_py_file(self, filename):
        with open(filename, 'w')as f:
            f.write(new_pyfile_template(self.printme.term))

    # def from_config_file(self, filename):
    #     self.config.read(filename)

    def from_pyfile(self, filename, silent=False):
        if not filename.endswith('.py'):
            filename = filename + '.py'
        file_path = os.path.join(self.root_path, filename)
        if not os.path.exists(file_path):
            self.create_py_file(file_path)
            print(f'[*]Tip:: 文件不存在,现已创建at: {file_path}')
        d = types.ModuleType('config')
        d.__file__ = filename
        try:
            with open(filename, mode='rb') as config_file:
                exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
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
        """从实例中导入配置 , 最佳体验为可将配置写在一个dataclass中
        for example:
        class Ext:
            TD_FUNC = True
            MD_FUNC = True
        ext = Ext()
        app.config.from_object(ext)
        """
        if isinstance(obj, string_types):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)
        self.printme.set_config()  # 渲染
