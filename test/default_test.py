from colour_printing.default import log
from colour_printing import cprint, Back, Fore, Mode, cword

log.log_handler.run()
log.info("hello world!")
# Switch.signal=False #关闭

# Switch.filter.append('SUCCESS') #过滤

log.error("hello world!")
log.success("hello world!")

log.warn("hello world!")
log.debug("hello world!")
# 颜料

