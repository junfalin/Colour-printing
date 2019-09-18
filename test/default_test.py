from colour_printing.default import log
from colour_printing import Switch, cprint, Back, Fore, Mode

log.info("hello world!")
# Switch.signal=False #关闭

# Switch.filter.append('SUCCESS') #过滤

log.error("hello world!")
log.success("hello world!")

log.warn("hello world!")
log.debug("hello world!")
# 颜料
# 打印色彩字符
print()
cprint('default')
cprint('hello', fore=Fore.RED)
# 或者
print()
s1 = cprint('I', fore=Fore.YELLOW, show=False)
s2 = cprint('LOVE', 'China', fore=Fore.RED, show=False)
cprint(s1, s2[0], s2[1])
