import errno
import os
import pkgutil
import sys
import types
from configparser import ConfigParser

from flask._compat import string_types
from werkzeug.utils import import_string


def find_package(import_name):
    root_mod_name = import_name.split('.')[0]
    loader = pkgutil.get_loader(root_mod_name)
    if loader is None or import_name == '__main__':
        package_path = os.getcwd()
    else:
        if hasattr(loader, 'get_filename'):
            filename = loader.get_filename(root_mod_name)
        elif hasattr(loader, 'archive'):
            filename = loader.archive
        else:
            __import__(import_name)
            filename = sys.modules[import_name].__file__
        package_path = os.path.abspath(os.path.dirname(filename))
        if _matching_loader_thinks_module_is_package(
                loader, root_mod_name):
            package_path = os.path.dirname(package_path)

    site_parent, site_folder = os.path.split(package_path)
    py_prefix = os.path.abspath(sys.prefix)
    if package_path.startswith(py_prefix):
        return py_prefix, package_path
    elif site_folder.lower() == 'site-packages':
        parent, folder = os.path.split(site_parent)
        # Windows like installations
        if folder.lower() == 'lib':
            base_dir = parent
        elif os.path.basename(parent).lower() == 'lib':
            base_dir = os.path.dirname(parent)
        else:
            base_dir = site_parent
        return base_dir, package_path
    return None, package_path


def _matching_loader_thinks_module_is_package(loader, mod_name):
    if hasattr(loader, 'is_package'):
        return loader.is_package(mod_name)
    # importlib's namespace loaders do not have this functionality but
    # all the modules it loads are packages, so we can take advantage of
    # this information.
    elif (loader.__class__.__module__ == '_frozen_importlib' and
          loader.__class__.__name__ == 'NamespaceLoader'):
        return True
    # Otherwise we need to fail with an error that explains what went
    # wrong.
    raise AttributeError(
        ('%s.is_package() method is missing but is required by CtpBee of '
         'PEP 302 import hooks.  If you do not use import hooks and '
         'you encounter this error please file a bug against Flask.') %
        loader.__class__.__name__)


def new_config_template(term):
    res = """#                     *Colour-printing Reference*
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
    level_list = ['info', 'error', 'success', 'debug', 'warn']
    for t in term:
        for l in level_list:
            temp = f"""
[{t}_{l}]
level = {l}
default = 
back = 
fore = 
mode = 
"""
            res += temp
    return res


def new_pyfile_template(term):
    res = """#                     *Colour-printing Reference*
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
    level_list = ['info', 'error', 'success', 'debug', 'warn']
    for l in level_list:
        res += "%s = {" % l.upper()
        for t in term:
            temp = """
    '%s': {
        "fore": "",
        "back": "",
        "mode": "",
        "default": "",
    },
""" % t
            res += temp
        res += "}\n\n"
    return res


class Config(object):
    def __init__(self, import_name, term, root_path=None):
        self.import_name = import_name
        self.name = 'yeah'

        if root_path:
            self.root_path = root_path
        else:
            self.root_path = self.auto_find_instance_path()
        self.config = ConfigParser()
        self.create_config_file(term)
        self.create_py_file(term)

    def create_config_file(self, term):
        with open(self.root_path + '/colour_printing.config', 'w')as f:
            f.write(new_config_template(term))

    def create_py_file(self, term):
        with open(self.root_path + '/colour_printing_setting.py', 'w')as f:
            f.write(new_pyfile_template(term))

    def auto_find_instance_path(self):
        prefix, package_path = find_package(self.import_name)
        if prefix is None:
            return os.path.join(package_path)
        return os.path.join(prefix, 'var', self.name + '-instance')

    def from_config_file(self, filename):
        self.config.read(filename)
        print(self.config.items('name_info'))

    def from_pyfile(self, filename, silent=False):
        filename = os.path.join(self.root_path, filename)
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


if __name__ == '__main__':
    c = Config(__name__, ['time', 'name', 'level', 'msg'])
    c.from_config_file('colour_printing.config')
