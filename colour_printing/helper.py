def check(terms):
    if "message" not in terms:
        return 'TEMPLATE中未找到 {message} ! '
    for t in terms:
        if t.strip() == '':
            return '未知 {} ! '
        if " " in t:
            return '{{t}} 含空格'.format(t)
    return None
