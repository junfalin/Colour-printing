import time

from colour_printing import log, Switch, cprint, Back, Fore, Mode

log.info("hello world!")
# Switch.signal=False #关闭

# Switch.filter.append('SUCCESS') #过滤

log.error("hello world!")
log.success("hello world!")


log.warn("hello world!")
log.debug("hello world!")
# 颜料
cprint('default')
cprint('hello', fore=Fore.RED)
