Colour-printing
==================

以不同颜色区分终端输出信息类型，标识出重要信息
==============================================

Python version: 3.5+

- 内置

  + info
  + success
  + error
  + warning
  + debug



小工具
=======

::

    # 打印色彩字符
    cprint('default')
    cprint('hello', fore=Fore.RED)
    #或者只要色彩字符
    s1 = cword('I', fore=Fore.YELLOW)
    s2 = cword('LOVE','China', fore=Fore.RED)
    print(s1, s2[0], s2[1])

创建配置模板文件
================

::

    >> cd [path]
    >> cprint (template) [config_filename]
    # cprint "{time}: {message}" "style"



需要注意

  + template (模板):  具体由format实现，所以格式要求 “{}{}{}{message}”  ！{message}必需！

  + colour_printing_config.py (配置文件):  DEFAULT ：lambda or function name




默认模板示例
============

::

    from colour_printing.default import log, Switch, Back, Fore, Mode
    from colour_printing import cprint

    log.info("hello world!")

    # Switch.signal=False #关闭
    # Switch.filter.append('SUCCESS') #过滤

    log.error("hello world!")
    log.success("hello world!")
    log.warn("hello world!")
    log.debug("hello world!")





自定义模板/style/新增level
==========================

::

    from colour_printing.custom import PrintMe,level_wrap

    p = PrintMe( template ='{time} {message}')
    log.config.from_pyfile(filename = '') # 载入配置
    #log.config.from_object(instance = '') # 载入配置
    p.log_handler.run(log_name='',log_path='')  # 日志输出到文件

    # p.switch = False
    # p.prtin_filter=['info','error']

    p.info('hello')
    p.error('hello')
    p.warn('hello')
    p.success('hello')
    #新增level
    class NewOne(PrintMe):
        @level_wrap
        def critical(self, *args, **kwargs):
            """不执行"""
            pass

    n = NewOne(template='{time} {message}')
    n.critical('new')


输出信息
===========

::

    class VLog(PrintMe):
        def record(self,record: object):
        """ 继承后可获得输出信息,自定义操作 """
            print(type(record))

    vlog = VLog(template='{time} {message}')
    vlog.info('this is message')



