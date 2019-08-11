# Colour-printing
> 参考：https://blog.csdn.net/qq_34857250/article/details/79673698    @Mr-Linqx

> 支持：Python version:3.7
#### 示例
```
import time
from printing.log import ColourPrint, Switch



print('Default Setting!')
log = ColourPrint()
log("hello world!")

Switch.category_filter.append('SUCCESS') #过滤


time.sleep(1)
log("hello world!", category='ERROR')
time.sleep(1)



log("hello world!", category='SUCCESS')
time.sleep(1)
Switch.signal=False #关闭

log("hello world!", category='WARRING')

Switch.signal=True #开启

print('User Setting!')
log2 = ColourPrint()

log2.set_category_style(category='Custom', mode='underline')
log2.set_time_style(category='Custom', mode='bold', fore='red')
log2.set_str_style(category='Custom', back='yellow')

log2("hello world!", category='Custom')

```