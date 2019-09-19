Colour-printing
==================

以不同颜色区分终端输出信息类型，标识出重要信息
==============================================

Python version: 3.5+

- 内置

  + info
  + success
  + error
  + warn
  + debug

- 过滤器

  + Switch.filter : list
  + Switch.signal : bool

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

    p = PrintMe( template ='{time} {message}'
                 config_filename ='' ,
                 config_path = '',)
    p.log_handler.run(log_name='',log_path='',log_delay='')  # 日志输出到文件

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


需要注意

  + template (模板):  具体由format实现，所以格式要求 “{}{}{}{message}”  ！{message}必需！

  + colour_printing_config.py (配置文件):  DEFAULT ：lambda or function name



