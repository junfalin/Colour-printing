from colour_printing.style import setting, Fore, Mode, Back


def cprint(*args, **kwargs):
    """
    :param args: 字符
    :param kwargs: 颜色参数
    :return: list 彩色字符
    sep=' ', end='\n', file=None
    """
    if not args:
        return print()
    mode = kwargs.get('mode')
    fore = kwargs.get('fore', Fore.CYAN)
    back = kwargs.get('back')
    sep = kwargs.get('sep', " ")
    end = kwargs.get('end', '\n')
    file = kwargs.get('file', None)
    style = setting(mode=mode, fore=fore, back=back)
    str_temp = []
    for s in args:
        str_temp.append(f'{style[0]}{s}{style[1]}')
    if kwargs.get('show', True):
        print(*str_temp, sep=sep, end=end, file=file)
    return str_temp if len(str_temp) > 1 else str_temp[0]
