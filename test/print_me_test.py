import time

from colour_printing.custom import PrintMe, level_wrap


class NewOne(PrintMe):
    @level_wrap
    def critical(self, *args, **kwargs):
        pass


p = NewOne(template='{time} :-> {message}')
p.log_handler.run()  # 打开日志输出
for i in range(50):
    p.info(i, end='\n')
time.sleep(1)
p.critical(p.level_list)
