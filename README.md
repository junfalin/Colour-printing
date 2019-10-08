# Colour-printing
用颜色区分终端输出信息类型，自定义输出模板，标识出重要信息
```
pip install colour-printing
```
> Support:Python 3.7
- 内置： 
  - info 
  - success 
  - error 
  - warning
  - debug
  

#### 示例默认模板
```
    from colour_printing.default import log
    
    log.info("hello world!")
    log.error("hello world!")
    log.success("hello world!")
    log.warning("hello world!")
    log.debug("hello world!")

    

```


#### 小工具

```
    from colour_printing import cprint,cword

    # 打印色彩字符
    cprint('default')
    cprint('hello', fore=Fore.RED)
    
    #或者只要色彩字符
    s1 = cword('I', fore=Fore.YELLOW)
    s2 = cword('LOVE','China', fore=Fore.RED)
    
    print(s1, s2[0], s2[1])
```


![image](https://github.com/Faithforus/Colour-printing/blob/master/default.png)



### 创建配置模板文件
>> cprint -h # 查看帮助
```
>> cd /home/faith/GIT/Colour-printing

>> cprint (-t template) [-n config_filename]

```

> 需要注意 
- template (模板):  具体由format实现，所以格式要求 “{}{}{}{}”  {**message**}字段必需!



#### 自定义模板/样式/新增level

```
    from colour_printing.custom import PrintMe,level_wrap

    p = PrintMe(cp_config,my_var1='',my_var2='') 
    # cp_config:可通过object或配置文件path导入;可另外载入自定义变量(可选) 
    
    p.log_handler.run(log_name='',log_path='')  
    # 日志输出到文件，参数可选
    
    p.set_default(set_level='info',time='2019')
    # 设置默认值，将会覆盖配置文件值，其中set_level：指定设置的level.不指定则所有

    # p.hide()
    # p.print_filter=['info','error']

    p.info('hello')
    p.error('hello')
    p.warning('hello')
    p.success('hello')

    #新增level
    >>> cprint -l "critical other1 other2"
    
    class NewOne(PrintMe):
    
        @level_wrap
        def critical(self, data:dict):
            """最高优先级,对data的操作会影响后续操作(日志,打印)的输出内容"""


```


#### 输出信息
```
    class VLog(PrintMe):
        def handler_record(self,record: dict):
        """record不受level函数影响,处理日志信息 重写此函数以应用每个不同的使用场景 """
            print("handler_record: ",record)
    
```
