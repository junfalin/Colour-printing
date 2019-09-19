# Colour-printing
用颜色区分终端输出信息类型，自定义输出模板，标识出重要信息
```
pip install colour-printing
```
> Support:Python 3.5+
- 内置： 
  - info 
  - success 
  - error 
  - warn
  - debug
- 过滤器：(用于默认模板)
  - Switch.filter : list
  - Switch.signal : bool

#### 示例
```
    from colour_printing.default import log, Switch, Back, Fore, Mode
    from colour_printing import cprint
    
    
    log.info("hello world!")

    # Switch.signal=False #关闭
    # Switch.filter.append('SUCCESS') #过滤
    
    log.error("hello world!")
    log.success("hello world!")
    log.warn("hello world!")
    log.debug("hello world!")
    # 打印色彩字符
    cprint('default')
    cprint('hello', fore=Fore.RED)
    #或者
    s1 = cprint('I', fore=Fore.YELLOW, show=False)
    s2 = cprint('LOVE','China', fore=Fore.RED, show=False)
    cprint(s1, s2[0], s2[1])
    
    

```
![image](https://github.com/Faithforus/Colour-printing/blob/master/default.png)
#### 默认模板修改 style
- 查看样式表： 
```
  print(log)
```
```
    from colour_printing.default import ColourPrint, Back, Fore, Mode    
    class MyColour(ColourPrint):
        def custom(self):
            self.test = self.Markers('test')
                        .flag_style(fore=Fore.CYAN)
                        .time_style(mode=Mode.UNDERLINE)
                        .message_style(fore=Fore.YELLOW)
    
    echo = MyColour()
    echo.test('hello world!')


```

![image](https://github.com/Faithforus/Colour-printing/blob/master/style.png)

#### 自定义模板/style

```
    from colour_printing.custom import PrintMe

    p = PrintMe(template='{time} {message}'
                config_filename,='',
                log_output=True,#日志文件输出
                log_name='',#日志文件名
                log_delay=5)#日志关闭延迟
    # p.switch = False
    # p.filter.append('info')
    p.info('hello')
    p.error('hello')
    p.success('hello')
    p.debug('hello')
    p.warn('hello')


```
> 需要注意 
- template (模板):  具体由format实现，所以格式要求 “{}{}{}{message}”  ！{message}必需！
- colour_printing_config.py (配置文件):  DEFAULT ：lambda or function name ;具体查看test/colour_printing_config.py


