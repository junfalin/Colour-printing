import errno
import os
import sys
import types

stream = sys.stdout


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


class Config(dict):
    def __init__(self, printme=None):
        dict.__init__(self)
        self.printme = printme
        self.config_str = ""
        self.filename = ""

    def from_pyfile(self, file_path, silent=False):
        filename = os.path.split(file_path)[1]
        self.filename = filename
        d = types.ModuleType('config')
        d.__file__ = filename
        try:
            with open(file_path, mode='rb') as config_file:
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
        return self.from_object(d)

    def from_object(self, obj):
        if isinstance(obj, string_types):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)
        if self.printme:
            self.printme.load_config()  # 渲染
        return True
