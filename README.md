# Colour-printing
以不同颜色区分终端输出信息类型，标识出重要信息
```
pip install colour_printing
```
> Support:Python 3.5+
- 内置类型： 
  - INFO(默认) 
  - SUCCESS 
  - ERROR 
  - WARN
- 过滤器：
  - Switch.filter : list
- 开关：
  - Switch.signal : bool
#### 示例
```
print('Default Setting!')
  log = ColourPrint()

  log.info("hello world!")

  #Switch.filter.append('SUCCESS') #过滤

  log.error("hello world!")
  log.success("hello world!")

  #Switch.signal=False #关闭

  log.warn("hello world!")

```
#### 自定义style
- 查看样式表： print(ColourPrint())
```
  print('User Setting!')

  class MyColour(ColourPrint):
      def custom(self):
          self.debug = self.Markers('debug').flag_style(model='bold').time_style()
          self.log = self.Markers('log')

  echo = MyColour()
  echo.debug('hello world!')

```


> 参考：[@JeanCheng](https://blog.csdn.net/gatieme/article/details/45439671)
