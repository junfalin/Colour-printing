===============
Colour-printing
===============
以不同颜色区分终端输出信息类型，标识出重要信息
============================================================

Python version: 3.5+

- 内置

  + info
  + success
  + error
  + warn
- 过滤器

  + Switch.filter : list
- 开关

  + Switch.signal : bool

=====
示例
=====

::

  print('Default Setting!')
  log = ColourPrint()

  log.info("hello world!")

  #Switch.filter.append('SUCCESS') #过滤

  log.error("hello world!")
  log.success("hello world!")

  #Switch.signal=False #关闭

  log.warn("hello world!")

  #颜料桶
  s1 = log.dyestuff('this red', fore='red')
  s2 = log.dyestuff('this green', fore='green')
  print(s1, s2)

===========
自定义style
===========

- 查看样式表： print(ColourPrint())

::

  print('User Setting!')

  class MyColour(ColourPrint):
      def custom(self):
          self.debug = self.Markers('debug').flag_style(model='bold')
          self.log = self.Markers('log').flag_style(model='hide')

  echo = MyColour()
  echo.debug('hello world!')
  echo.log('hello world!')
