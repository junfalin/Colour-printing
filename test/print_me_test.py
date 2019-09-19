import time

from colour_printing.custom import PrintMe, level_wrap


class A(PrintMe):
    @level_wrap
    def critical(self, *args, **kwargs):
        pass


p = A(template='{time} :-> {message}')
p.log_output()
for i in range(50):
    p.info(i, end='1\n')

time.sleep(1)
p.critical(p.level_list)
