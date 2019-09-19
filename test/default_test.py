from colour_printing.default import log
from colour_printing import cprint, Back, Fore, Mode, cword

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
s1 = cword('I', fore=Fore.YELLOW)
s2 = cword('LOVE', 'China', fore=Fore.RED)
print(s1, s2[0], s2[1])
