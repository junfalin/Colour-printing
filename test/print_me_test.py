import os
import time

from colour_printing.custom import PrintMe, level_wrap


class NewOne(PrintMe):
    @level_wrap
    def info(self, kwargs):
        # print(kwargs)
        kwargs['time'] = '123   '
        pass


m = NewOne()
# m.config.from_pyfile(os.getcwd() + "/colour_printing_config.py")
# m.set_default(message='111')
# m.log_handler.run()
# for i in range(50):
#     m.info(None)
from colour_printing.custom import PrintMe, level_wrap

p = PrintMe()
p.config.from_pyfile(file_path=os.getcwd() + "/colour_printing_config.py")  # 载入配置
p.log_handler.run(log_name='', log_path='')  # 日志输出到文件
p.set_default(set_level='info', time='2019')  # 设置默认值，将会覆盖配置文件值，其中set_level：指定设置的level.不指定则所有

# p.hide()
p.prtin_filter=['info','error']

p.info('hello')
p.error('hello')
p.warning('hello')
p.success('hello')
