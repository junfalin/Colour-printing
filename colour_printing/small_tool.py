from colour_printing.style import setting, CPStyle


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
    str_temp = cword(*args)
    if not isinstance(str_temp, list):
        str_temp = [str_temp]
    if file:
        temp = []
        for i in args:
            if not isinstance(i, CPStyle):
                temp.append(i)
        print(*temp, sep=sep, end=end, file=file)
    else:
        print(*str_temp, sep=sep, end=end)


def cword(*args):
    """
    :param args: 字符
    :param kwargs: 颜色参数
    :return: list 彩色字符
    """
    data = {}
    temp = []
    for i in args:
        if isinstance(i, CPStyle):
            data[i.name] = i.value
        else:
            temp.append(i)
    style = setting(**data)
    str_temp = []
    for s in temp:
        str_temp.append('{s0}{s}{s1}'.format(s0=style[0], s=s, s1=style[1]))
    return str_temp[0] if len(str_temp) == 1 else str_temp
