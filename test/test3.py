from colour_printing.custom import PrintMe

p = PrintMe(template='{time}::{message}')
p.info('hello')
p.info('hello')
# p.switch = False
p.filter.append('info')
p.info('hello')
p.info('hello')
p.error('hello')
p.error('hello')
p.error('hello')


