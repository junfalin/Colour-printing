import os
from colour_printing.custom import PrintMe

log = PrintMe(template='{time} {flag} {message}')
log.config.from_pyfile(os.path.split(__file__)[0] + '/default_colour_printing_config.py')
