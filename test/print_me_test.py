import time

from colour_printing.custom import PrintMe, level_wrap


class NewOne(PrintMe):

    def record(self, record):
        print('1 Vlog', record.__dict__)


class NewTow(NewOne):

    def record(self, record):
        print('2 Vlog', record.__dict__)


m = NewOne(template='{time} :-> {message}')
m2 = NewTow(template='{time} :-> {message}')
# p.log_handler.run()  # 打开日志输出
for i in range(50):
    m.info(i, end='\n')
time.sleep(1)
m.info()
