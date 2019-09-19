from colour_printing.style import setting, Fore, Mode, Back


def cprint(*args, **kwargs):
    """
    :param args: 字符
    :param kwargs: 颜色参数
    :return: list 彩色字符
    sep=' ', end='\n', file=None
    """
    sep = kwargs.pop('sep', " ")
    end = kwargs.pop('end', '\n')
    file = kwargs.pop('file', None)
    str_temp = cword(*args, **kwargs)
    if not isinstance(str_temp, list):
        str_temp = [str_temp]
    if file:
        print(*args, sep=sep, end=end, file=file)
    else:
        print(*str_temp, sep=sep, end=end, file=file)


def cword(*args, **kwargs):
    """
    :param args: 字符
    :param kwargs: 颜色参数
    :return: list 彩色字符
    """
    mode = kwargs.get('mode')
    fore = kwargs.get('fore', Fore.CYAN)
    back = kwargs.get('back')
    style = setting(mode=mode, fore=fore, back=back)
    str_temp = []
    for s in args:
        str_temp.append(f'{style[0]}{s}{style[1]}')
    return str_temp[0] if len(str_temp) == 1 else str_temp
