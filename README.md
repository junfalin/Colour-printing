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

#### 示例默认模板
```
    from colour_printing.default import log
    from colour_printing import cprint,cword
    
    
    log.info("hello world!")
    log.error("hello world!")
    log.success("hello world!")
    log.warn("hello world!")
    log.debug("hello world!")
    # 打印色彩字符
    cprint('default')
    cprint('hello', fore=Fore.RED)
    #或者
    s1 = cword('I', fore=Fore.YELLOW)
    s2 = cword('LOVE','China', fore=Fore.RED)
    print(s1, s2[0], s2[1])
    
    

```
![image](https://github.com/Faithforus/Colour-printing/blob/master/default.png)
#### 自定义模板/样式

```
    from colour_printing.custom import PrintMe

    p = PrintMe( template ='{time} {message}'
                 config_filename ='' ,
                 log_output = True , # 日志文件输出
                 log_name = '' , # 日志文件名
                 log_delay = 5 ) # 日志关闭延迟

    # p.switch = False
    # p.filter.append('info')

    p.info('hello')

```
> 需要注意 
- template (模板):  具体由format实现，所以格式要求 “{}{}{}{message}”  ！{message}必需！
- colour_printing_config.py (配置文件):  DEFAULT ：lambda or function name ;具体查看test/colour_printing_config.py


