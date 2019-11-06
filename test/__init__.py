# from colour_printing.default import log
from colour_printing.custom import PrintMe
from test.colour_printing_config import CP

if __name__ == '__main__':

    log = PrintMe(CP)
    log.info('hello')
    log.success('hello', flag='', level='ss')
    log.error('hello')
    log.warning('hello')
    log.debug('hello')

