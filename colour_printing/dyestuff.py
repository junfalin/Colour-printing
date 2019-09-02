from colour_printing.style import setting


class Dyestuff:
    @classmethod
    def dyestuff(cls, *args, **kwargs):
        """
        :param args: 字符
        :param kwargs: 颜色参数
        :return:  彩色字符
        """
        style = setting(**kwargs)
        temp = f'{style[0]}{("{} " * len(args))}{style[1]}'
        return temp.format(*args)
