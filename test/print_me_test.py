import time

from colour_printing.custom import PrintMe

p = PrintMe(template='{time} :-> {message}', log_output=True)
# p.switch = False
# p.filter.append('info')
for i in range(50):
    p.info(i,end='1\n')

time.sleep(2)
p.info(1)