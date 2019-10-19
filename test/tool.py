from colour_printing import cprint, cword, Fore

# 打印色彩字符
cprint('default')
cprint('hello', Fore.RED)

# 或者只要色彩字符
s1 = cword('I', Fore.YELLOW)
s2 = cword('LOVE', 'China', Fore.RED)

print(s1, s2[0], s2[1])