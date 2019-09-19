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
  
#### 小工具

```
    from colour_printing import cprint,cword

    # 打印色彩字符
    cprint('default')
    cprint('hello', fo re=Fore.RED)
    #或者只要色彩字符
    s1 = cword('I', fore=Fore.YELLOW)
    s2 = cword('LOVE','China', fore=Fore.RED)
    print(s1, s2[0], s2[1])
```


#### 示例默认模板
```
    from colour_printing.default import log
    
    log.info("hello world!")
    log.error("hello world!")
    log.success("hello world!")
    log.warn("hello world!")
    log.debug("hello world!")

    

```
![image](https://github.com/Faithforus/Colour-printing/blob/master/default.png)
#### 自定义模板/样式/新增level

```
    from colour_printing.custom import PrintMe,level_wrap

    p = PrintMe( template ='{time} {message}'
                 config_filename ='' ,
                 config_path = '',) 
    # 实例化后会生成默认配置文件 ××_config.py
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

```
> 需要注意 
- template (模板):  具体由format实现，所以格式要求 “{}{}{}{**message**}”  {**message**}字段必需!
- colour_printing_config.py (配置文件):  DEFAULT ：**lambda** or **function name** ;具体查看test/colour_printing_config.py


