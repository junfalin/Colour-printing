import os
import time

from colour_printing.custom import PrintMe, level_wrap


class NewOne(PrintMe):
    @level_wrap
    def info(self, kwargs):
        # print(kwargs)
        kwargs['time'] = '123   '
        pass

    def handler_record(self, record):
        # print('1 Vlog', record)
        pass

m = NewOne()
m.config.from_pyfile(os.getcwd() + "/ss.py")
m.log_handler.run()
for i in range(50):
    m.info(i, end='\n')
    m.error(i, end='\n')

