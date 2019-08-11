# Colour-printing
以不同颜色区分终端输出信息类型，让终端输出不再单调
> 参考：https://blog.csdn.net/gatieme/article/details/45439671    @JeanCheng

> version:Python 3.7
- 内置类型： INFO(默认) SUCCESS ERROR WARRING 
- 过滤器：Switch.category_filter -> list
- 开关：Switch.signal -> bool
#### 示例
```
import time
from printing.log import ColourPrint, Switch


print('Default Setting!')
log = ColourPrint()

log("hello world!")
#Switch.category_filter.append('SUCCESS') #过滤
time.sleep(1)
log("hello world!", category='ERROR')
time.sleep(1)
log("hello world!", category='SUCCESS')
time.sleep(1)
#Switch.signal=False #关闭
log("hello world!", category='WARRING')

```
#### 自定义style
- 查看样式表： print(ColourPrint())
```
print('User Setting!')

echo = ColourPrint()
#可选
echo.set_category_style(category='Custom', mode='underline')
echo.set_time_style(category='Custom', mode='bold', fore='red')
echo.set_str_style(category='Custom', back='yellow')

echo("hello world!", category='Custom')

```