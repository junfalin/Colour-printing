import re

from colour_printing.exception import PrintMeError
from colour_printing.helper import check
from colour_printing.style import setting


class Term(object):
    def __init__(self, *args, default=''):
        self.default = default
        data = {}
        for i in args:
            if isinstance(i, dict):
                data[i['type']] = i['value']
        self.style = setting(**data)  # list


class CPConfig(object):
    def __init__(self, template):
        self._box = {}
        self._default = {}
        self._levels = []
        self.check(template)

    def check(self, template):
        self._rawtemplate = template
        self._terms = re.findall(r'(?<=\{)[^}]*(?=\})+', template)
        e = check(self._terms)
        if e:
            raise PrintMeError(e)
        term_wrap = {}
        for t in self._terms:
            term_wrap[t] = "{%s}{%s}{%s}" % (t + '0', t, t + '1')
        self._template = self._rawtemplate.format(**term_wrap)

    def wrap(self, func):
        func(self)
        self.__fill(func.__name__.upper())

    def __fill(self, level_name):
        self._levels.append(level_name)
        for t in self._terms:
            term = getattr(self, t, Term())
            self._box.setdefault(level_name, {}).update({f"{t}0": term.style[0], f"{t}1": term.style[1]})
            self._default.setdefault(level_name, {}).update({t: term.default})
            if hasattr(self, t):
                delattr(self, t)
