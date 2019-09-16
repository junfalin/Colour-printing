# Colour-printing
以不同颜色区分终端输出信息类型，标识出重要信息
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
- 过滤器：
  - Switch.filter : list
- 开关：
  - Switch.signal : bool
#### 示例
```
    from colour_printing import log, Switch, cprint, Back, Fore, Mode
    
    log.info("hello world!")
    # Switch.signal=False #关闭
    
    # Switch.filter.append('SUCCESS') #过滤
    
    log.error("hello world!")
    log.success("hello world!")
    
    
    log.warn("hello world!")
    log.debug("hello world!")
    # 颜料
    cprint('default')
    cprint('hello', fore=Fore.RED)

```
![image](https://github.com/Faithforus/Colour-printing/blob/master/default.png)
#### 自定义style
- 查看样式表： 
```
  print(log)
```
```
    from colour_printing.custom import ColourPrint, Back, Fore, Mode
    from colour_printing import cprint
    
    
    class MyColour(ColourPrint):
        def custom(self):
            self.test = self.Markers('test').flag_style(fore=Fore.PURPLE, mode=Mode.HIDE).time_style(
                mode=Mode.INVERT).message_style(
                fore=Fore.YELLOW)
    
    
    echo = MyColour()
    echo.test('hello world!')


```

![image](https://github.com/Faithforus/Colour-printing/blob/master/style.png)


> 参考：[@JeanCheng](https://blog.csdn.net/gatieme/article/details/45439671)
