from colour_printing.custom import PrintMe

p = PrintMe(template='{time} {message}')
# p.switch = False
# p.filter.append('info')
p.info('hello')
p.error('hello')
p.success('hello')
p.debug('hello')
p.warn('hello')
