import os
from colour_printing.custom import PrintMe

log = PrintMe(template='{time} {flag} {message}', config_filename='default_colour_printing_config',
              config_path=os.path.split(__file__)[0])
