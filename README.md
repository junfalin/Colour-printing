# Colour-printing
以不同颜色区分终端输出信息类型，标识出重要信息
> Python version: 3
- 内置类型： INFO(默认) SUCCESS ERROR WARRING 
- 过滤器：Switch.filter -> list
- 开关：Switch.signal -> bool
#### 示例
```
import time
from printing.log import ColourPrint, Switch


print('Default Setting!')
log = ColourPrint()

log("hello world!")
#Switch.filter.append('SUCCESS') #过滤
time.sleep(1)
log("hello world!", flag='ERROR')
time.sleep(1)
log("hello world!", flag='SUCCESS')
time.sleep(1)
#Switch.signal=False #关闭
log("hello world!", flag='WARRING')

```
#### 自定义style
- 查看样式表： print(ColourPrint())
```
print('User Setting!')

echo = ColourPrint()
#可选
echo.set_flag_style(flag='Custom', mode='underline')
echo.set_time_style(flag='Custom', mode='bold', fore='red')
echo.set_str_style(flag='Custom', back='yellow')

echo("hello world!", flag='Custom')

```


> 参考：[@JeanCheng](https://blog.csdn.net/gatieme/article/details/45439671)
