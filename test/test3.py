from configparser import ConfigParser
config = ConfigParser()
config.read('zh_cn.config', encoding='UTF-8')
print('sections:', config.sections())