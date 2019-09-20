lk = '{'
rk = '}'
a = """"{term}":{lk}
    "DEFAULT":{DEFAULT},
    "fore":{fore},
    "back":{back},
    "mode":{mode}
    {rk}""".format(lk=lk, rk=rk, **kwargs)
print(a)
