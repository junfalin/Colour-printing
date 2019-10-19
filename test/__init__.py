from colour_printing.default import log
from colour_printing.custom import PrintMe

PrintMe.DYE = False
# log.info('hello')
# log.success('hello', flag='', level='ss')
# log.error('hello')
# log.warning('hello')
# log.debug('hello')
from colour_printing import cprint, Fore

cprint('sd', Fore.BLUE)
