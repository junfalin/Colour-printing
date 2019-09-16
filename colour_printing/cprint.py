from colour_printing.custom.style import setting, Fore, Mode


def cprint(*args, mode=Mode.INVERT, fore=Fore.CYAN, back=''):
    """
    :param args: 字符
    :param kwargs: 颜色参数
    :return:  彩色字符
    """
    style = setting(mode=mode, fore=fore, back=back)
    str_temp = []
    for s in args:
        str_temp.append(f'{style[0]}{s}{style[1]}')
    print(*str_temp)
