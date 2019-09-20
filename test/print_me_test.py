import os
import time

from colour_printing.custom import PrintMe, level_wrap


class NewOne(PrintMe):
    @level_wrap
    def info(self, kwargs):
        # print(kwargs)
        kwargs['time'] = '123   '

    def handler_record(self, record):
        print('1 Vlog', record)


m = NewOne()
m.config.from_pyfile(os.getcwd() + "/ss.py")
m.log_handler.run()
for i in range(50):
    m.info(i, end='\n')
time.sleep(1)
m.info('done')
